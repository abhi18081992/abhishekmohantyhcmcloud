---
title: "Oracle HCM Cloud Fast Formula: Regular and OT Bucket Allocation in a TCR — The Day-Type Branch, the l_total Threshold Cascade, and the l_ot_counter Tracking Pattern"
description: "ORACLE HCM CLOUD · TCR DEEP DIVE · PART 5 OF 12"
pubDate: 2026-07-02
tags: ["Fast Formula", "Oracle HCM Cloud", "TCR", "OTL", "Time and Labor", "TER", "Time Entry Rule"]
---

ORACLE HCM CLOUD · TCR DEEP DIVE · PART 5 OF 12


# Oracle HCM Cloud Fast Formula: Regular and OT Bucket Allocation in a TCR — The Day-Type Branch, the l_total Threshold Cascade, and the l_ot_counter Tracking Pattern


How the worked-time branch of the DETAIL iteration decides whether each hour goes to `Out_Measure_RegHours`, `Out_Measure_OT_150_Hours`, or `Out_Measure_OT_200_Hours` — driven by the day type (PH / SAT / SUN / Weekday), the daily threshold compare against `l_total`, and the spillover logic that splits a single entry across multiple buckets when it straddles a threshold.


  FAST FORMULA
  OTL
  OVERTIME ALLOCATION
  THRESHOLD CASCADE



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant




Part 4 covered the absence side of the DETAIL fork — when `AbsenceType.exists(nidx)` returns true. This post covers the other side: when it returns false and the entry represents **worked time**. That's where the bulk of the TCR's allocation logic lives.


The worked-time branch has one job — decide which output bucket every hour belongs in. The decision rests on two inputs: the **day type** (public holiday, Saturday, Sunday, or weekday) determined via Part 2's day-type branching logic, and the **running daily total** held in `l_total`. Day type controls which thresholds apply; `l_total` controls whether the current entry has already crossed them.


A worked example threads the whole post: a single Wednesday on which a worker logs **two DETAIL entries** — a 4-hour morning shift (09:00–13:00) and an 8-hour afternoon shift (14:00–22:00), for a 12-hour day. The daily thresholds are 8 hours for Regular and 10 hours for OT 150%, above which everything is OT 200%. The formula's job is to split those 12 hours across three buckets correctly: 8 Regular, 2 OT 150%, 2 OT 200% — even though no single entry is split that way in isolation.


## The Worked-Time Branch — Where the DETAIL Decision Tree Leads


Inside every DETAIL iteration, the formula first checks `AbsenceType.exists(nidx)`. If true, the absence branch (Part 4) fires. If false, control flows here — into a sequence of four steps that map an entry's hours onto the right output buckets:







FIGURE 01 · CONTROL FLOW


The Worked-Time Branch in the Iteration Loop




four sequential gates













DETAIL ITERATION (worked path)


aiRecPosition = 'DETAIL'


AbsenceType.exists(nidx) = false







▼








1




DETERMINE DAY TYPE


Branch on PH / SAT / SUN / Weekday (per Part 2 logic)









▼








2




COMPARE l_total VS THRESHOLDS


Determine remaining Regular capacity and OT 150 capacity for the day









▼








3




SPLIT MEASURE ACROSS BUCKETS


Allocate first to Regular, spillover to OT 150, then OT 200









▼








4




UPDATE l_total AND l_ot_counter


Advance the daily total and OT-allocated counter for the next iteration









▼








OUTPUT BUCKETS UPDATED


RegHours · OT_150_Hours · OT_200_Hours














READ →


Four gates fire in strict order. Skip step 1 and the wrong thresholds apply. Skip step 2 and you allocate hours that should have been OT into Regular. Skip step 4 and the next iteration sees stale state. Each gate is one or two lines of code — and each one matters.






## The Four-Way Day-Type Branch — One Rule Set Per Day Category


Day type changes everything about allocation. The same worked hour on a Wednesday is Regular pay; on a Sunday it's OT at 200%; on a public holiday it's a different output bucket entirely. Part 2 covered the day-type detection logic (`GET_DATE_DAY_OF_WEEK`, the FRI-anchored weekly compare, and the holiday calendar lookup). Part 5 uses the result:







FIGURE 02 · ALLOCATION RULES


Multiplier Logic by Day Type






BRANCHES


4 day types


















W




DAY TYPE


Weekday (Mon–Fri)








CASCADE



            0 – 8 hrs   → Regular

            8 – 10 hrs  → OT 150%

            10+ hrs    → OT 200%













S




DAY TYPE


Saturday








RULE



            0+ hrs    → OT 150%



Weekend day with elevated rate from the first hour. No Regular allocation possible.












S




DAY TYPE


Sunday








RULE



            0+ hrs    → OT 200%



Mandatory day of rest. All worked hours at the higher OT rate.












P




DAY TYPE


Public Holiday








RULE



            0+ hrs    → OT 200% (Holiday bucket)



Routes to a separate holiday output bucket downstream — payroll often pays this at a different rate than Sunday OT 200.

















READ →


Only the Weekday branch has a cascade across three buckets. SAT, SUN, and PH all route every worked hour to a single bucket — which makes them simpler to allocate, but more sensitive to day-type misdetection. Get day type wrong and an entire day's hours land in the wrong bucket.






## The l_total Threshold Cascade — Where Each Hour Lands


The Weekday branch is the only one with a true threshold cascade, so it's the one worth visualizing. `l_total` holds the running daily total of worked hours (introduced in Part 3, reset at every `END_DAY` phase marker). The cascade asks one question for every incoming hour: *where is `l_total` sitting right now relative to the two thresholds?*







FIGURE 03 · BUCKET ZONES


The Weekday Threshold Cascade






DAY TYPE


Weekday


















REG CAP · 8 hrs










OT 150 CAP · 10 hrs












REGULAR · 0 – 8 hrs



OT 150



OT 200








0


2


4


6


8


10


12 (hrs)














        **Regular zone** · Out_Measure_RegHours







        **OT 150 zone** · Out_Measure_OT_150_Hours







        **OT 200 zone** · Out_Measure_OT_200_Hours









HOW TO READ THE CASCADE


Each incoming worked hour is placed in the zone where `l_total` currently sits, then `l_total` advances by one. A single multi-hour entry whose measure straddles a threshold gets split — the part below the threshold goes to one bucket, the part above to the next. That's the spillover logic Figure 04 traces.












READ →


The 8 and 10 thresholds are configuration values held in rule input parameters, not hardcoded. Different jurisdictions and contracts set different caps — the formula reads them via `get_rvalue_number(rule_id, 'DAILY_REG_CAP', 8)` at the top of the formula.






## The Spillover Logic — One Entry Crossing Multiple Thresholds


The interesting case is when a single DETAIL entry's measure straddles a threshold. Walk through the worked example. The second entry is 8 hours long, but `l_total` already sits at 4 from the first entry. There are 4 hours of Regular capacity left, then 2 hours of OT 150 capacity, then everything above goes to OT 200. The 8-hour measure has to split three ways:


/* Compute remaining capacity in each zone */

l_reg_remaining    = GREATEST(0, l_daily_reg_cap - l_total)

l_ot150_remaining = GREATEST(0, l_daily_ot_cap - GREATEST(l_total, l_daily_reg_cap))

l_remaining = l_measure


/* Regular portion */

l_reg_alloc = LEAST(l_remaining, l_reg_remaining)

Out_Measure_RegHours = Out_Measure_RegHours + l_reg_alloc

l_total      = l_total + l_reg_alloc

l_remaining = l_remaining - l_reg_alloc


/* OT 150 portion */

l_ot150_alloc = LEAST(l_remaining, l_ot150_remaining)

Out_Measure_OT_150_Hours = Out_Measure_OT_150_Hours + l_ot150_alloc

l_total      = l_total + l_ot150_alloc

l_ot_counter = l_ot_counter + l_ot150_alloc

l_remaining = l_remaining - l_ot150_alloc


/* OT 200 portion — whatever is left */

IF (l_remaining > 0) THEN

(

  Out_Measure_OT_200_Hours = Out_Measure_OT_200_Hours + l_remaining

  l_total      = l_total + l_remaining

  l_ot_counter = l_ot_counter + l_remaining

)


`LEAST` and `GREATEST` are delivered Fast Formula functions — they're the idiomatic way to clamp values without nested IF blocks. The pattern reads as: "give the current zone as much as it can take, then move on." Figure 04 traces every step:







FIGURE 04 · ALLOCATION TRACE


A 12-Hour Wednesday Across Two Entries






TOTAL


12 hrs worked











      | STEP
          | l_total(start)
          | REGalloc
          | OT 150alloc
          | OT 200alloc
          | l_total(end)
        |




          | ENTRY 1
            09:00–13:00 · 4 hrs
          | 0
          | +4
          | 0
          | 0
          | 4
        |


          | ENTRY 2 · PASS 1
            Regular fill (4→8)
          | 4
          | +4
          | 0
          | 0
          | 8
        |


          | ENTRY 2 · PASS 2
            OT 150 fill (8→10)
          | 8
          | 0
          | +2
          | 0
          | 10
        |


          | ENTRY 2 · PASS 3
            OT 200 fill (10→12)
          | 10
          | 0
          | 0
          | +2
          | 12
        |


          | END_DAY
            Final totals
          | 12
          | 8
          | 2
          | 2
          | → reset
        |









CONSERVATION INVARIANT


At every step: `REG + OT_150 + OT_200 = sum of measures consumed`. Final totals: 8 + 2 + 2 = 12, matching the worked-time input exactly. No hour is double-counted; no hour is dropped.












READ →


Entry 2 fires three internal passes — not three loop iterations. The DETAIL iteration for nidx=2 runs the spillover allocation block once; the block itself does the three-stage split using `LEAST` and `GREATEST` arithmetic.






## The l_ot_counter — A Running Tally for the Downstream Cascade


Alongside `l_total`, the formula maintains a second running counter: `l_ot_counter`. It increments only when OT hours (150 or 200) are allocated. `l_total` tracks how much was worked; `l_ot_counter` tracks how much of that was OT.


Why a separate counter? Because Part 9 introduces a twelve-tier OT_200_counter cascade that fires once for every cumulative OT hour accumulated across the period — and that cascade needs an exact running count, not a derived value. Maintaining the counter inline during allocation is cheaper than recomputing it later from the output buckets.


Unlike `l_total`, `l_ot_counter` is **not** reset at `END_DAY`. It accumulates across the entire period because the downstream cascade is period-level, not daily.


## The Output Buckets — Where Worked Hours Land


Three output arrays capture the worked-time classification for the period. Together with the `Out_Abs_*` buckets from Part 4, they form the complete picture of compensable time the formula returns to payroll:







FIGURE 05 · OUTPUT REFERENCE


Worked-Time Output Buckets






BUCKETS


3 worked-time




















R


Out_Measure_RegHours




Hours at standard rate


BASE










FED BY


Hours where `l_total` sits below the daily Regular cap. Weekday days only — SAT/SUN/PH never feed this bucket.






EXAMPLE VALUE


8 hrs after the 12-hour Wednesday — the first 8 hours of worked time.


















★


Out_Measure_OT_150_Hours




Overtime at 150% rate


FIRST-TIER OT










FED BY


Weekday hours where `l_total` sits between the Reg cap and the OT cap, plus all Saturday hours, plus the absence back-fill (Part 4).






EXAMPLE VALUE


2 hrs from the Wednesday cascade — hours 9 and 10 of the worked day.


















★★


Out_Measure_OT_200_Hours




Overtime at 200% rate


SECOND-TIER OT










FED BY


Weekday hours above the OT cap, plus all Sunday hours, plus all Public Holiday hours. Feeds the Part 9 cascade trigger.






EXAMPLE VALUE


2 hrs from the Wednesday cascade — hours 11 and 12 of the worked day.





















READ →


Three worked-time buckets, three rates. Add the two absence buckets from Part 4 and that's the full set of outputs the worked-time and absence branches produce. The next two parts add night-surcharge and night-overtime detection on top of these — without modifying any of the existing bucket allocations.







NEXT IN THE SERIES


### Part 6 — Night Surcharge Detection with the Night-Time Code Match and the Monthly Night Accumulator


A second classification layered on top of the day-type allocation — how the formula identifies night-time hours by matching `PayrollTimeType` against a configured night-time code, why `l_daily_night_total` resets on `END_DAY` while `l_period_night_total` doesn't, and how night-surcharge hours stack alongside the Reg/OT-150/OT-200 buckets without disturbing them.



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.





TCR DEEP DIVE · PART 5 / 10


Series tag: #TCRDeepDive