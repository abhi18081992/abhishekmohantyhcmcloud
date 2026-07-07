---
title: "Oracle HCM Cloud Fast Formula: The Main Iteration Loop in a TCR — HWM_CTXARY Parallel Arrays, aiRecPosition Phase Markers, and the Defensive raise_error Guard"
description: "ORACLE HCM CLOUD · TCR DEEP DIVE · PART 3 OF 12"
pubDate: 2026-06-18
tags: ["Fast Formula", "Oracle HCM Cloud", "TCR", "OTL", "Time and Labor", "TER", "Time Entry Rule", "DBI"]
---

ORACLE HCM CLOUD · TCR DEEP DIVE · PART 3 OF 12


# Oracle HCM Cloud Fast Formula: The Main Iteration Loop in a TCR — HWM_CTXARY Parallel Arrays, aiRecPosition Phase Markers, and the Defensive raise_error Guard


How a Time Calculation Rule walks the timecard one entry at a time — the `HWM_CTXARY_*` array DBI family, the `.count` / `.exists()` array methods, the `DETAIL` / `END_DAY` phase fork, and the `raise_error` safety net that catches runaway loops.


  FAST FORMULA
  OTL
  TIME CALCULATION RULE
  ARRAY DBIs



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant




A TCR formula doesn't run once per worker. It runs once per **measure period entry** — and a single timecard week can produce dozens of those entries (start/stop pairs, breaks, absences, end-of-day markers, period summaries). The formula has to walk all of them, allocate hours into the right output buckets, and emerge with consistent totals.


The walking is done with a `WHILE` loop over Oracle's `HWM_CTXARY_*` array database items. The arrays are *parallel*: position 1 in one array refers to the same timecard entry as position 1 in every other array. That single design choice shapes how the rest of the formula reads.


This post walks through the iteration mechanics: how the arrays are sized, how positions are accessed safely, what the `aiRecPosition` phase marker means at each step, and why every well-written TCR closes the loop with a defensive `raise_error` trap.


## The HWM_CTXARY Array DBI Family — Per-Entry Data Surfaced as Parallel Tracks


Oracle's Time and Labor framework exposes the current measure period's data to the formula as a set of **indexed array DBIs**, all named with the `HWM_CTXARY_` prefix (HWM = Workforce Management, CTXARY = context array). Common members of the family:


  - `HWM_CTXARY_RECORD_POSITIONS` — text array; each cell holds a phase marker like `'DETAIL'`, `'END_DAY'`, or a higher-level boundary marker.

  - `HWM_CTXARY_HWM_MEASURE_DAY` — number array; the day-of-period to which each entry belongs (1, 2, 3 …).

  - Per-entry input variables — `measure`, `StartTime`, `StopTime`, `PayrollTimeType`, `AbsenceType` — declared in the `INPUTS ARE` block and exposed as arrays.


All of them share the same indexing. Position 1 of `RECORD_POSITIONS` tells you the phase of timecard entry 1; position 1 of `StartTime` tells you when that same entry began; position 1 of `measure` tells you its hour value. The loop's job is to step through positions 1 through N and assemble a per-entry picture from these parallel tracks.








FIGURE 01 · DATA STRUCTURE


The Flattening Transformation




timecard → array












1




INPUT


Calendar view — what the worker enters












DAY 3


09:00 – 12:00


3.0 hours · Regular






DAY 3


13:00 – 17:00


4.0 hours · Regular






DAY 8


09:00 – 17:00


8.0 hours · Regular














        ▼
        FRAMEWORK FLATTENS · INSERTS PHASE MARKERS
        ▼












2




OUTPUT


Array view — what the TCR formula iterates over













nidx = 1




DETAIL


3.0h









nidx = 2




DETAIL


4.0h









nidx = 3




END_DAY


marker









nidx = 4




DETAIL


8.0h









nidx = 5




END_DAY


marker









nidx = 6




END_PERIOD


marker
















        **DETAIL** — worked time entry with measure data







        **Phase marker** — boundary, no measure data













READ →


Three worked-time entries become six array positions. The framework inserts `END_DAY` between same-day entries and `END_PERIOD` to close the iteration. Both carry no measure data — the reason every read inside the loop needs an `.exists()` guard.












FIGURE 02 · DATA INDEX


Parallel Arrays — One nidx, Many Tracks






SHARED INDEX


nidx = 1 … 6














TRACK NAME


VALUE AT EACH POSITION






      | DBI · INPUT
          | nidx 1
            DETAIL
          | nidx 2
            DETAIL
          | nidx 3
            END_DAY
          | nidx 4
            DETAIL
          | nidx 5
            END_DAY
          | nidx 6
            END_PERIOD
        |





          | PHASE TRACK
            HWM_CTXARY_RECORD_POSITIONS
          | DETAIL
          | DETAIL
          | END_DAY
          | DETAIL
          | END_DAY
          | END_PERIOD
        |



          | DAY TRACK
            HWM_CTXARY_HWM_MEASURE_DAY
          | 3
          | 3
          | 3
          | 8
          | 8
          | empty
        |



          | TIME TRACK
            StartTime
          | 09:00
          | 13:00
          | empty
          | 09:00
          | empty
          | empty
        |


          | TIME TRACK
            StopTime
          | 12:00
          | 17:00
          | empty
          | 17:00
          | empty
          | empty
        |



          | MEASURE TRACK
            measure
          | 3.0
          | 4.0
          | empty
          | 8.0
          | empty
          | empty
        |



          | CLASSIFICATION
            PayrollTimeType
          | Regular
          | Regular
          | empty
          | Regular
          | empty
          | empty
        |











**PHASE**




**DAY**




**TIME**




**MEASURE**




**CLASSIFICATION**












READ →


Read this table **column by column**, not row by row. Each column is a complete timecard entry assembled from its parallel array cells. Empty cells appear at every phase-marker column — the explicit visual signature of why `.exists()` guards belong in the loop.






## Array Cardinality with .count and the WHILE Loop Skeleton


Fast Formula array DBIs expose a `.count` method that returns the number of populated positions. The TCR captures this once at the top and uses it as the loop's upper bound:


/* Capture the array bound once. Calling .count inside

   the loop would re-resolve the DBI on every iteration. */

wMaAry = HWM_CTXARY_RECORD_POSITIONS.count

nidx   = 0


WHILE (nidx LOOP

(

  nidx = nidx + 1

  aiRecPosition = HWM_CTXARY_RECORD_POSITIONS[nidx]


  /* ...per-entry processing... */

)


A few details worth flagging:


  - **1-based indexing.** Fast Formula arrays start at index 1, not 0. `nidx = 0` with increment-then-access inside the loop yields positions 1, 2, 3 ... wMaAry — the increment happens *before* any array access, which is the safe pattern.

  - **Capture .count once.** Reading `HWM_CTXARY_RECORD_POSITIONS.count` inside the loop condition would force the DBI to resolve on every iteration. Capturing it in `wMaAry` beforehand cuts the DBI resolution cost to one call. Oracle's own Fast Formula performance guidance specifically calls this out.

  - **No FOR loop in Fast Formula.** The language has no `FOR i IN 1..N` construct. `WHILE` with manual counter advance is the idiomatic substitute. Forgetting the increment is the most common cause of runaway loops — which is exactly the failure mode the `raise_error` guard at the end of the loop catches.


## Null-Safe Array Access with the .exists() Method


Parallel arrays don't always carry data at every position. Look back at the visualization: at `nidx=3` the position is `'END_DAY'` — a phase marker — but `measure`, `StartTime`, `StopTime` have no values there. Reading `measure[3]` directly would raise *"no data found"* and abort the rule.








FIGURE 03 · CONTROL FLOW


A One-Line Guard, Two Outcomes




measure[nidx] at END_DAY














ITERATION ENTRY


nidx = 3


aiRecPosition = 'END_DAY'












⤹  DIRECT READ






GUARDED READ  ⤸


















!




PATH A


Without .exists() guard













STEP 1 · ACCESS


l_measure = measure[3]




▼





STEP 2 · RAISE


ORA-01403


no data found




▼





OUTCOME


FORMULA ABORTS
















✓




PATH B


With .exists() guard













STEP 1 · CHECK


IF measure.exists(3)




▼





STEP 2 · SKIP


FALSE → bypass


block not executed




▼





OUTCOME


CONTINUE TO nidx = 4



















READ →


The same `measure[3]` read either crashes the rule or quietly skips, depending on a one-line guard. In a long-running payroll batch the crash version surfaces hours after submission, attributed to the worker whose timecard contained the phase marker — not the engineer who wrote the formula.






The defensive read is the `.exists()` method, which returns true only when the array has a populated cell at the given index:


/* Always check .exists() before parallel-array access */

IF (HWM_CTXARY_HWM_MEASURE_DAY.exists(nidx)) THEN

(

  aiMeasureDay = HWM_CTXARY_HWM_MEASURE_DAY[nidx]

)


IF (measure.exists(nidx)) THEN

(

  l_measure = measure[nidx]

)


IF (STARTTIME.exists(nidx)) THEN

(

  aiStartTime = STARTTIME[nidx]

)


A common shortcut is to assume that if `RECORD_POSITIONS` exists at a given index, all parallel arrays must too. **Don't.** Phase markers like `END_DAY` and `END_PERIOD` deliberately leave the data tracks empty. `.exists()` is cheap; the runtime error from a wrong assumption is not.



.exists() VS DEFAULT FOR — WHEN TO USE WHICH


The top-of-formula declaration `DEFAULT FOR measure IS EMPTY_NUMBER_NUMBER` tells the compiler what to substitute if the *whole array DBI* isn't populated. It does **not** protect you from accessing an unpopulated *index* within an otherwise populated array. `.exists()` is the per-index guard; `DEFAULT FOR` is the per-DBI guard. Both are needed for a robust loop.


## The aiRecPosition Phase Markers — DETAIL, END_DAY, and Period Boundaries


The single most important value in the loop is `aiRecPosition`. It tells the formula what kind of position the current `nidx` represents, and therefore which branch of the formula's logic should run:








FIGURE 04 · STATE REFERENCE


aiRecPosition Phase Markers






STATES


3 values
























▶


'DETAIL'




Worked time entry


DATA-BEARING








All per-entry input variables (`measure`, `StartTime`, `StopTime`, `PayrollTimeType`) are populated at this position.






FIRES WHEN


A worker submits a start/stop pair, break, or absence entry on the timecard.






TRIGGERS


Allocation logic — day-type branch, OT bucket assignment, night-time detection.



















⏷


'END_DAY'




Daily summary boundary


PHASE MARKER







Fired once after the last `DETAIL` entry of a day. Carries no measure or time data — every per-entry input is empty at this position.






FIRES WHEN


A day's DETAIL entries have all been emitted and the framework inserts a closing boundary.






TRIGGERS


Daily accumulator resets — `l_total`, `l_daily_night_total` back to zero.



















■


'END_PERIOD'




Period summary boundary


TERMINAL







Final position in the array. The loop's next iteration check (`nidx 





READ →


Only `DETAIL` carries data. The other two are control signals — empty rows whose only job is to mark *where you are* in the period so the formula knows when to reset and when to seal.






The canonical phase-branch inside the loop reads like this:


IF (aiRecPosition = 'DETAIL' AND aiMeasureDay > 0) THEN

(

  /* Allocate worked hours into OT buckets:

     day-type branch, night-time detection,

     threshold crossing, bucket spillover */

)


IF (aiRecPosition = 'END_DAY') THEN

(

  /* Reset daily accumulators */

  l_total = 0

  l_daily_night_total = 0

)


Note the `aiMeasureDay > 0` guard alongside the DETAIL check. Some installations populate `DETAIL` phase markers with placeholder rows that have no actual measure day — typically header or pre-allocation records. Skipping those keeps the allocation logic from running against null data.


## The END_DAY Reset Pattern — Why l_total Returns to Zero Mid-Iteration


The `l_total` reset on `END_DAY` is one of those patterns that looks wrong at first glance. Why zero the daily total in the middle of a loop?


Because `l_total` is a **per-day** accumulator, not a per-period one. It builds up during the DETAIL entries of one calendar day, gets compared against the daily threshold to determine OT, and must start fresh on the next day's DETAIL entries. The `END_DAY` position is the only safe place to do the reset, because:


  - Resetting inside the DETAIL branch would zero out partial-day accumulations before they were used.

  - Resetting at the start of the next day's first DETAIL would require knowing it's the first one, which means tracking yet another flag.

  - Resetting on every iteration would prevent any same-day accumulation at all.


The `END_DAY` marker exists precisely so the framework can give formulas a cheap, deterministic reset point. Period-level accumulators (`l_period_regular`, `l_period_night_total`) are deliberately *not* reset on END_DAY — they keep accumulating across days and only end with the formula execution itself.








FIGURE 05 · ACCUMULATOR TRACE


l_total Across the Iteration Loop






UNIT


hours






















8


6


4


2


0





































3











7












↓ RESET


0











8











↓ RESET


0











0

























nidx 1


DETAIL






nidx 2


DETAIL






nidx 3


END_DAY






nidx 4


DETAIL






nidx 5


END_DAY






nidx 6


END_PERIOD










l_total (hrs)












        **Accumulating** — DETAIL iteration adds to l_total







        **Reset** — END_DAY/END_PERIOD zeroes l_total









KEY INSIGHT


Day 3 climbs to 7 hours, the END_DAY reset zeroes it, then Day 8 starts fresh and accumulates to 8. Without the reset, Day 8's threshold compare would fire against `7 + 8 = 15` hours and misclassify regular time as overtime.













READ →


The sawtooth pattern is the visible signature of correct daily accumulator handling. Period-level accumulators (`l_period_regular`) would climb monotonically across the same iteration range — no resets — and that's intentional too.






## The Infinite-Loop Guard — raise_error at nidx > 1000


Fast Formula has no compile-time loop termination analysis. A `WHILE` loop whose increment line is accidentally inside an `IF` branch that never fires will run until the runtime governor terminates the rule with a vague *"formula execution exceeded threshold"* error — long after the timecard submission has already failed for the user.


A defensive ceiling check inside the loop catches this earlier, with a useful error message:


/* Defensive ceiling — fires before the runtime governor does */

IF (nidx > 1000) THEN

(

  ex = raise_error(ffs_id, rule_id,

                  'Formula ' || ffName ||

                  ' terminated due to possible end-less loop.')

)


Why `1000`? It's a sanity ceiling, not a hard requirement. A single worker's measure period entries rarely exceed 200 in normal use (semi-monthly period × multiple daily entries × phase markers). Anything past 1000 means something is wrong upstream — either the loop counter isn't advancing, or the array has unexpected entries.


Four practical notes on `raise_error`:


  - It takes `ffs_id` and `rule_id` as required parameters so the OTL audit log can attribute the error to the specific Fast Formula session and rule instance.

  - The return value (`ex`) is assigned but never used — the call's side effect is the error raise. Some installations omit the assignment; both work.

  - The error message string is what the worker sees in the timecard submission failure. Concatenating `ffName` into it makes diagnosis dramatically faster when multiple TCRs are chained together.

  - Once raised, `raise_error` terminates the entire formula execution. Logs written via `add_log` before the raise are flushed to the audit trail; logs after are lost.


## The Complete Loop Skeleton


Putting all five elements together — array cardinality capture, the WHILE bound, increment-before-access, .exists()-guarded reads, phase-branch logic, daily reset, and the runaway guard:


/* Cardinality capture */

wMaAry = HWM_CTXARY_RECORD_POSITIONS.count

nidx   = 0


WHILE (nidx LOOP

(

  nidx = nidx + 1

  aiRecPosition = HWM_CTXARY_RECORD_POSITIONS[nidx]


  /* Null-safe reads of parallel arrays */

  IF (HWM_CTXARY_HWM_MEASURE_DAY.exists(nidx)) THEN

    aiMeasureDay = HWM_CTXARY_HWM_MEASURE_DAY[nidx]


  /* Phase branch — DETAIL entries trigger allocation */

  IF (aiRecPosition = 'DETAIL' AND aiMeasureDay > 0) THEN

  (

    /* ...per-entry allocation logic... */

  )


  /* Daily reset on END_DAY phase marker */

  IF (aiRecPosition = 'END_DAY') THEN

  (

    l_total = 0

    l_daily_night_total = 0

  )


  /* Defensive ceiling */

  IF (nidx > 1000) THEN

  (

    ex = raise_error(ffs_id, rule_id,

                    'Formula ' || ffName ||

                    ' terminated due to possible end-less loop.')

  )

)


Every line earns its place. The cardinality capture cuts DBI calls. The 1-based increment-then-access avoids off-by-one errors. The `.exists()` guard prevents *no data found* crashes on phase-marker rows. The DETAIL+aiMeasureDay compound condition keeps allocation logic from running against placeholders. The END_DAY reset prevents accumulator bleed-through. The 1000-iteration ceiling catches runaway loops before the runtime governor does.


Strip any one of these out and the TCR still compiles. Skip enough of them and it will quietly produce wrong totals in production — the failure mode the next post in this series picks up.



NEXT IN THE SERIES


### Part 4 — Absence Integration in a TCR with AbsenceType, GET_VALUE_SET, and the Monthly Back-Fill


How worked hours and absence hours share the same monthly bucket — the `AbsenceType` array, a `GET_VALUE_SET` lookup that excludes certain absence types from OT, the `Out_Abs_Cd` / `Out_Abs_Hours` output buckets, and the back-fill WHILE loop that retroactively reclassifies regular hours as OT when an absence pushes the worker over the monthly cap.



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.





TCR DEEP DIVE · PART 3 / 10


Series tag: #TCRDeepDive