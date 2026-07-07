---
title: "Oracle HCM Cloud Fast Formula: Absence Integration in a TCR — The AbsenceType Array, the GET_VALUE_SET Claim Lookup, and the Back-Fill WHILE Loop"
description: "ORACLE HCM CLOUD · TCR DEEP DIVE · PART 4 OF 12"
pubDate: 2026-06-25
tags: ["Fast Formula", "Oracle HCM Cloud", "TCR", "OTL", "Time and Labor", "Absence Management", "DBI", "CHANGE_CONTEXTS"]
---

ORACLE HCM CLOUD · TCR DEEP DIVE · PART 4 OF 12


# Oracle HCM Cloud Fast Formula: Absence Integration in a TCR — The AbsenceType Array, the GET_VALUE_SET Claim Lookup, and the Back-Fill WHILE Loop


How worked hours and absence hours share the same monthly bucket — the `AbsenceType` array as a sparse parallel track, the `GET_VALUE_SET` lookup that resolves the OT-eligibility claim, the `Out_Abs_Cd` / `Out_Abs_Hours` output buckets, and the retroactive `WHILE` loop that reclassifies regular hours as overtime when an absence pushes the worker over the monthly cap.


  FAST FORMULA
  OTL
  ABSENCE MANAGEMENT
  BACK-FILL PATTERN



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant




A TCR doesn't only track worked hours. Absence hours — sick leave, vacation, jury duty, bereavement — flow through the same parallel-array iteration framework, share the same monthly threshold arithmetic, and end up affecting the same output buckets. The formula has to handle them as first-class citizens of the period, not as a parallel pipeline.


This post walks through the absence integration pattern: how the `AbsenceType` array surfaces absence entries to the TCR, how `GET_VALUE_SET` resolves each absence to its OT-eligibility claim, how the `Out_Abs_*` output buckets carry the data downstream to payroll, and — the most interesting move in the whole formula — how the TCR retroactively reclassifies already-allocated regular hours as overtime when an absence pushes the worker over the monthly threshold.


A single worked example threads through the post: a worker with **156 worked hours**, **8 hours of OT-eligible absence**, against a **160 hour monthly threshold**. Total counted time: 164 hours. The 4 hours over threshold have to become OT — but the absence portion can't be "OT" because it's not worked time. So four of the previously-allocated worked hours have to be reclassified.


## AbsenceType — The Sparse Track in the Parallel Array Stack


Part 3 introduced the `HWM_CTXARY_*` parallel-array family — multiple DBIs and input variables co-indexed by `nidx` so that position 1 across every track refers to the same timecard entry. `AbsenceType` joins that stack as a sixth parallel track.


It behaves differently from the worked-time tracks in one important way: it's **sparse**. The framework populates `AbsenceType[nidx]` only on positions that represent absence transactions. Worked-time entries leave it empty. Phase markers leave it empty. The first move inside the loop body — before any allocation logic fires — is checking whether this position is an absence.








FIGURE 01 · DATA STRUCTURE


AbsenceType — The Sparse Track






POPULATED


1 of 6 cells












      | DBI · INPUT
          | nidx 1
            DETAIL
          | nidx 2
            DETAIL
          | nidx 3
            ABSENCE
          | nidx 4
            END_DAY
        |




          | PHASE TRACK
            HWM_CTXARY_RECORD_POSITIONS
          | DETAIL
          | DETAIL
          | DETAIL
          | END_DAY
        |


          | MEASURE TRACK
            measure
          | 3.0
          | 5.0
          | 8.0
          | empty
        |


          | TIME TRACK
            StartTime
          | 09:00
          | 13:00
          | empty
          | empty
        |


          | CLASSIFICATION
            PayrollTimeType
          | Regular
          | Regular
          | empty
          | empty
        |


          | ABSENCE TRACK
            AbsenceType
          | empty
          | empty
          | SICK
          | empty
        |










**ABSENCE TRACK — sparse, populated only on absence entries**












READ →


At `nidx 3` the worker has 8 hours of sick leave. The measure track carries the duration, but the time tracks and classification track are empty — absence entries don't have a start/stop time the way worked entries do. `AbsenceType[3] = 'SICK'` is the only signal that distinguishes this position from a worked entry.






The detection pattern is a straightforward `.EXISTS()` check at the top of the loop body:


IF (aiRecPosition = 'DETAIL') THEN

(

  IF (AbsenceType.exists(nidx)) THEN

  (

    l_absence_code   = AbsenceType[nidx]

    l_absence_hours  = measure[nidx]

    /* Absence branch — claim lookup + bucket population */

  )

  ELSE

  (

    /* Worked-time branch — covered in Part 5 */

  )

)


## The Absence Claim ID Lookup with GET_VALUE_SET


Detecting that an entry is an absence is only the first step. Not every absence counts toward the worker's OT calculation — that's a configuration decision, defined per absence type and per worker eligibility profile. Sick leave might count toward the monthly cap. Unpaid leave might not. Bereavement might be excluded entirely.


The TCR resolves this through a value-set lookup that takes the worker's person ID and the absence type code, and returns the **absence claim ID** — a reference to the OT plan configuration that governs how this particular absence interacts with threshold arithmetic. A non-zero return means the absence is OT-eligible and should accumulate toward the monthly bucket. A zero return means it flows to the `Out_Abs_*` buckets for payroll but is excluded from the OT calculation.


l_params = '|=P_PERSON_ID='''  || TO_CHAR(l_person_id)

        || '''|P_ABS_CODE=''' || l_absence_code || ''''


l_abs_claim_id = TO_NUMBER(GET_VALUE_SET('XX_ABS_CLAIM_LOOKUP_VS', l_params))


IF (l_abs_claim_id > 0) THEN

(

  l_is_ot_eligible = 'Y'

)

ELSE

(

  l_is_ot_eligible = 'N'

)


The value set itself joins the absence plan configuration tables against the worker's plan enrollment, returning the claim ID if a match exists and zero otherwise. Keeping the SQL inside the value set (rather than inside the formula) lets the database optimizer cache the query plan and lets administrators update eligibility rules without touching the Fast Formula.


## Populating the Out_Abs Output Buckets


Two output arrays carry absence data out of the TCR and into downstream payroll processing:


  - `Out_Abs_Cd[nidx]` — the absence type code (`'SICK'`, `'VAC'`, `'BEREAVE'`) so the payroll element for that absence type fires.

  - `Out_Abs_Hours[nidx]` — the absence duration so the element receives a quantity to pay.


Both arrays are populated unconditionally for every detected absence entry, regardless of whether the absence is OT-eligible. The payroll downstream needs both values to issue absence pay; OT eligibility only affects the threshold arithmetic.


Out_Abs_Cd[nidx]    = l_absence_code

Out_Abs_Hours[nidx] = l_absence_hours


## The Monthly Accumulator — Why Absence Hours Count Toward OT


This is the design choice that catches most engineers off guard the first time they trace through the formula: `l_period_regular` accumulates **both worked hours and OT-eligible absence hours**. Not just worked hours.


The reasoning is regulatory. Many OT regimes treat paid absence as "working time" for the purpose of calculating whether a worker has exceeded the period threshold — the rationale being that the worker would have been earning regular hours during that time if they hadn't been on leave, so excluding leave from the threshold would unfairly punish workers who take statutory time off. The TCR encodes this by adding eligible-absence hours to the same period accumulator that tracks worked hours:


IF (l_is_ot_eligible = 'Y') THEN

(

  l_period_regular = l_period_regular + l_absence_hours

)


The same line gets executed during the worked-time branch (covered in Part 5) for each worked hour. By the time the loop reaches `END_PERIOD`, `l_period_regular` holds the combined total: worked + OT-eligible-absence.


## The Threshold Crossover Problem


Walk through the worked example. The worker accumulates:


  - **156 worked hours** across the month, each one initially classified as Regular and added to `Out_Measure_RegHours` during DETAIL iterations.

  - **8 hours of sick leave** entered on one day, OT-eligible (claim ID returned non-zero), added to `l_period_regular` alongside the worked hours.

  - **Monthly threshold: 160 hours**.


Total combined time: 156 + 8 = **164 hours**. Over threshold by 4.







FIGURE 02 · THRESHOLD ARITHMETIC


Monthly Hours vs Threshold






CAP


160 hrs















WORKED


156 hrs






ABSENCE


8 hrs






OVER THRESHOLD


+4 hrs















THRESHOLD · 160 hrs













156 hrs worked



8 abs

















0



40



80



120



160



164



200














        **Worked hours** · 156 hrs classified as Regular







        **OT-eligible absence** · 8 hrs of sick leave







        **Threshold line** · 160 hr cap









THE PROBLEM


The 4 over-threshold hours need to become OT 150% — but the absence portion can't be OT because it's not worked time. So four hours of the 156 already-classified worked hours must be reclassified from Regular to OT 150% by the back-fill WHILE loop at END_PERIOD.












READ →


The formula doesn't know about the 8 hrs of sick leave until it reaches that `nidx` position — possibly long after the worked hours have already been allocated to `Out_Measure_RegHours`. The misclassification has to be corrected after the fact.






## The Back-Fill WHILE Loop — Retroactive Reclassification


The correction happens at `END_PERIOD` — the final position in the iteration loop, where the formula has visibility into the total counted time. The over-threshold amount is computed, and a `WHILE` loop runs that decrements `Out_Measure_RegHours` and increments `Out_Measure_OT_150_Hours` by an equal amount, one hour at a time, until the over-threshold amount has been fully redistributed:


IF (aiRecPosition = 'END_PERIOD') THEN

(

  l_over_threshold = l_period_regular - l_monthly_threshold


  IF (l_over_threshold > 0) THEN

  (

    l_remaining_adjustment = l_over_threshold


    WHILE (l_remaining_adjustment > 0) LOOP

    (

      Out_Measure_RegHours    = Out_Measure_RegHours - 1

      Out_Measure_OT_150_Hours = Out_Measure_OT_150_Hours + 1

      l_remaining_adjustment   = l_remaining_adjustment - 1

    )

  )

)


The total worked hours stay constant — only the classification changes. 156 worked = (152 Regular) + (4 OT 150%). The 8 absence hours remain in their own buckets, untouched.







FIGURE 03 · CONTROL FLOW


The Absence Branch in the Iteration Loop




detect → allocate → adjust













DETAIL ITERATION


aiRecPosition = 'DETAIL'







▼








DECISION


AbsenceType.exists(nidx)?












YES ⤹ ABSENCE PATH






NO → WORKED PATH (Part 5)
















ABSENCE BRANCH


Four steps fire in sequence








STEP 1


GET_VALUE_SET claim lookup




▼




STEP 2


Populate Out_Abs_Cd, Out_Abs_Hours




▼




STEP 3


IF eligible → add to l_period_regular




▼




STEP 4


Continue to next nidx














WORKED BRANCH


Covered in Part 5





          The four-way day-type branch (PH/SAT/SUN/Weekday), the l_ovt_150 and l_ovt_200 calculation, and the l_OT_counter mechanics that determine which worked hours get classified as Regular versus OT during the DETAIL pass.

Both branches converge at l_period_regular — the same period accumulator that drives the threshold check.










▼






AT END_PERIOD


Back-fill if l_period_regular > threshold














READ →


The absence branch and the worked branch both feed the same accumulator — which is what makes the threshold compare at `END_PERIOD` meaningful. Decouple them and the OT calculation drifts.











FIGURE 04 · BACK-FILL TRACE


Step-by-Step Reclassification






ITERATIONS


4 to redistribute











      | ITERATION
          | l_remaining_adjustment
          | Out_Measure_RegHours
          | Out_Measure_OT_150_Hours
        |




          | ENTRY
            Pre-loop state
          | 4
          | 156
          | 0
        |


          | STEP 1
            First swap
          | 3
          | 155
          | 1
        |


          | STEP 2
            Second swap
          | 2
          | 154
          | 2
        |


          | STEP 3
            Third swap
          | 1
          | 153
          | 3
        |


          | STEP 4
            Final swap · LOOP EXITS
          | 0
          | 152
          | 4
        |








CONSERVATION INVARIANT


At every step: `Out_Measure_RegHours + Out_Measure_OT_150_Hours = 156`. Total worked hours never change. Only the classification mix shifts as hours migrate from Regular into OT 150%.












READ →


The one-hour-at-a-time decrement looks inefficient — and at the formula level, it is. A single subtraction would produce the same final values. The iterative form exists because a higher-tier overtime cascade (Part 9) needs an intermediate trigger for each unit of OT 150 added.






## The Output Bucket Reference


Four output buckets carry the full picture of the worker's month downstream to payroll. Each one represents a different category of compensable time, and the back-fill loop is what guarantees the four sums add up correctly:







FIGURE 05 · OUTPUT REFERENCE


Where Each Hour Lands






BUCKETS


4 outputs




















#


Out_Abs_Cd




Absence type code per entry


METADATA










FIRES WHEN


Absence detection inside the DETAIL branch.






CONSUMER


Payroll element selector — picks the absence element by type code.


















∑


Out_Abs_Hours




Absence duration per entry


QUANTITY










FIRES WHEN


Set to `measure[nidx]` alongside the type code.






CONSUMER


Quantity input to the absence payroll element — drives the pay calculation.


















R


Out_Measure_RegHours




Regular worked hours (post-adjustment)


ADJUSTED










FIRES WHEN


Accumulates during DETAIL worked-time iterations, then decremented by the back-fill loop at END_PERIOD.






FINAL VALUE


152 hours (was 156 before reclassification).


















★


Out_Measure_OT_150_Hours




Overtime at 150% rate


BACK-FILLED










FIRES WHEN


Incremented by the back-fill WHILE loop and by direct worked-OT detection (Part 5).






FINAL VALUE


4 hours from this back-fill (more added in later parts).





















READ →


Four output buckets, two flows. The `Out_Abs_*` buckets carry absence data to payroll's absence pay calculation. The `Out_Measure_*` buckets carry worked-time classification to payroll's earnings element resolution. The back-fill loop is the bridge that keeps the worked-time buckets in sync with the threshold arithmetic.







NEXT IN THE SERIES


### Part 5 — Regular and OT Bucket Allocation with the Day-Type Branch, l_ovt_150 / l_ovt_200, and the l_OT_counter Cascade


The worked-time branch of the DETAIL iteration — how the formula decides, for every worked hour as it streams through the loop, whether to allocate it to `Out_Measure_RegHours`, `Out_Measure_OT_150_Hours`, or `Out_Measure_OT_200_Hours` based on the day type (public holiday, Saturday, Sunday, weekday) and the running daily total.



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.





TCR DEEP DIVE · PART 4 / 10


Series tag: #TCRDeepDive