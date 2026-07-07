---
title: "Oracle HCM Cloud Fast Formula: Night OT Spillover in a TCR — IS_DATE_BETWEEN, the StopTime+24 Midnight Wrap, and the Four-Bucket Night Allocation"
description: "ORACLE HCM CLOUD · TCR DEEP DIVE · PART 7 OF 12"
pubDate: 2026-07-07
tags: ["Fast Formula", "Oracle HCM Cloud", "TCR", "OTL", "Time and Labor"]
---

ORACLE HCM CLOUD · TCR DEEP DIVE · PART 7 OF 12


# Oracle HCM Cloud Fast Formula: Night OT Spillover in a TCR — IS_DATE_BETWEEN, the StopTime+24 Midnight Wrap, and the Four-Bucket Night Allocation


The second night-detection path — how the formula catches night hours that aren't tagged as such by `PayrollTimeType`, how `IS_DATE_BETWEEN` plus the `StopTime + 24` unwrap handle a shift that crosses midnight, and how the resulting night hours split across four output buckets based on day type and the Part 5 tier they fell into.


  FAST FORMULA
  OTL
  NIGHT SPILLOVER
  MIDNIGHT CROSSING



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant




Part 6 covered the easy case — the timecard entry is tagged as `PayrollTimeType = 'Night'` and the TCR just needs to detect the tag. Part 7 covers the case that gives engineers pause: **the entry isn't tagged, but its physical clock time falls squarely inside the night window**. A shift stamped `'Regular'` can still owe night differential if it runs from 22:00 through the small hours.


The TCR has to detect the overlap between the shift and the configured night window purely from `StartTime` and `StopTime`. And because shifts routinely cross midnight — 22:00 to 06:00 is one of the most common patterns in a 24/7 operation — the arithmetic has to handle a stop-time that's numerically *less than* the start-time. That's where `StopTime + 24` comes in.


The worked example threading through the post: a worker logs **one shift starting at 20:00 Wednesday and ending at 08:00 Thursday** — 12 hours total, tagged `PayrollTimeType = 'Regular'`. Part 6's detection sees nothing to do. Part 7's detection finds **8 hours in the night window** — from 22:00 Wednesday to 06:00 Thursday — and has to split those 8 hours across the four night buckets based on which Part 5 tier each hour fell into. The final allocation: **6 Regular-Night + 2 OT-150-Night + 0 OT-200-Night + 0 Weekend-Night**.


## The Untagged Night Entry Problem


Not every organization tags night shifts at the timecard entry layer. Some rely purely on `PayrollTimeType` for classification (Part 6's world). Others let workers submit everything as `'Regular'` and expect the TCR to figure out night eligibility from the clock time. A robust TCR runs *both* detection paths — one for the tag, one for the time — so the formula works regardless of how the timecard is configured downstream.







FIGURE 01 · DETECTION PATHS


Two Paths, One Bucket Family




tag · clock · guard

















        - DETAIL ENTRY (worked path)
      measure · StartTime · StopTime · PTT












      PATH A · PART 6
      Tag Match
      PayrollTimeType = 'Night'
      catches tagged entries only



      PATH B · PART 7
      Clock-Time Overlap
      IS_DATE_BETWEEN(clock)
      catches untagged entries




      DEDUP GUARD
      Path A skip → Path B








      CONVERGES AT · FIVE NIGHT BUCKETS




        Reg_Night
        base rate + night


        OT_150_Night
        first-tier OT + night


        OT_200_Night
        second-tier OT + night


        Weekend_Night
        weekend + night


        Night
        aggregate




      4 NEW




      TWO PATHS · ONE POLICY
      Both paths feed the same bucket family. The dedup guard makes them mutually exclusive per entry: if Path A already fired for this `nidx`, Path B skips it — otherwise the same night hours would be counted twice.






      READ →
      Part 6's single `Out_Measure_Night_Hours` stays as an aggregate. Part 7 adds four *granular* buckets that split night hours by day-type and OT tier — because payroll needs the granularity to apply different rate elements.




## The Night Window as a Rule Parameter


The night window's start and end hours aren't hardcoded — they're rule input parameters. Different jurisdictions define night hours differently (22:00–06:00 is common but not universal), and even within one jurisdiction the definition can differ by contract:


/* Read once at the top of the formula */
l_night_start = get_rvalue_number(rule_id, 'NIGHT_WINDOW_START', 22)
l_night_end   = get_rvalue_number(rule_id, 'NIGHT_WINDOW_END',   6)


Two numbers held in decimal hours. `22` means 22:00 (10 PM); `6` means 06:00 (6 AM). The formula treats these as anchors on a 24-hour clock — with the understanding that when `end


## IS_DATE_BETWEEN and the StopTime + 24 Unwrap


A shift from 22:00 Wednesday to 06:00 Thursday is 8 hours long. But if you subtract `StopTime - StartTime` naively, you get `6 - 22 = -16`. Negative. Because the numeric clock resets to zero at midnight, and any arithmetic that ignores day boundaries collapses. The **StopTime + 24 unwrap** is the standard fix: if the stop-time is numerically less than the start-time, add 24 to it. Now the shift runs from `22` to `30` on an extended clock, and every subsequent calculation works.




      FIGURE 02 · TIME ARITHMETIC
      The Midnight-Crossing Unwrap


      EXTENDED CLOCK
      0 → 30







      ✗ WITHOUT UNWRAP
      StopTime − StartTime = 6 − 22 = −16 hrs · nonsense



      00
      06
      12
      18
      22
      24 / 0
      ?












      ← runs backward on a bounded 24-hr clock


      MIDNIGHT


      ✓ WITH UNWRAP · StopTime + 24 = 30
      Adjusted duration = 30 − 22 = 8 hrs · correct




      00
      06
      12
      18
      22
      24
      30












      8 hr night shift



      EXTENDED CLOCK ZONE


      midnight





IF (l_stop THEN
  l_stop_adj = l_stop + 24  /* shift wrapped past midnight */
ELSE
  l_stop_adj = l_stop






      READ →
      The `+ 24` trick works because everything downstream — the night window compare, the overlap arithmetic, all of it — operates on the *same* extended clock. As long as both `l_stop_adj` and the night-window end are consistently unwrapped, day boundaries stop mattering.




## Computing the Night-Window Overlap


Once the shift's clock times are unwrapped, computing the overlap with the night window is a two-line clamp. `GREATEST` and `LEAST` — same idiom Part 5 used for spillover — do the whole job:


/* Night window on the extended clock: 22:00 to 06:00 next day = 22 to 30 */
l_win_start = l_night_start        /* 22 */
l_win_end   = l_night_end + 24  /* 6 + 24 = 30 */
/* Overlap interval between (l_start, l_stop_adj) and (l_win_start, l_win_end) */
l_overlap_start = GREATEST(l_start,    l_win_start)
l_overlap_end   = LEAST   (l_stop_adj, l_win_end)
l_night_hours = GREATEST(0, l_overlap_end - l_overlap_start)


Plug in the worked example — `l_start = 20`, `l_stop_adj = 32`, `l_win_start = 22`, `l_win_end = 30`. Overlap runs from `MAX(20,22) = 22` to `MIN(32,30) = 30`, so night hours detected = `30 - 22 = 8`. The shift includes 2 hours before the night window (20:00–22:00) and 2 hours after (06:00–08:00) that don't qualify.




      FIGURE 03 · OVERLAP DETECTION
      Shift × Night Window Intersection


      OVERLAP
      8 of 12 hrs






    SHIFT · 12 hrs from Wed 20:00 to Thu 08:00






      12 hrs · PayrollTimeType = 'Regular'



    NIGHT WINDOW · 22:00 to 06:00 (extended: 22 → 30)





      8 hrs



    OVERLAP · GREATEST(20,22) to LEAST(32,30) = 22 to 30



      8 hrs detected as night




      18
      20Wed
      22
      24
      26
      28
      30= 06 Thu
      32= 08 Thu




      FOUR CASES · ONE CLAMP
      The same `GREATEST/LEAST` pair handles all four possible cases without a single `IF`: shift entirely inside the window, window entirely inside the shift (this example), partial overlap on either side, and no overlap at all. The final `GREATEST(0, ...)` clamps negatives to zero for the no-overlap case.






      READ →
      The gold overlap bar sits inside the shift bar because the night window is entirely contained within the shift. Change the shift to 04:00–14:00 and the overlap shrinks to 2 hours — the arithmetic still holds. The clamp is scenario-agnostic.




## Allocating Night Hours Across Four Buckets


The 8 detected night hours can't all go into one bucket. Payroll needs to know which tier each night hour belonged to under Part 5's cascade — because a night hour that's *also* an OT 200 hour pays at a different combined rate than a night hour that's still Regular. Four output buckets carry the split:


  `Out_Measure_Reg_Night_Hours` — weekday night hours in the Regular tier (below the daily OT threshold)

  - `Out_Measure_OT_150_Night_Hours` — weekday night hours in the OT 150 tier

  - `Out_Measure_OT_200_Night_Hours` — weekday night hours in the OT 200 tier

  - `Out_Measure_Weekend_Night_Hours` — all night hours on Saturday, Sunday, or Public Holiday (day-type takes precedence over tier)


In the worked example the shift is on a Wednesday (weekday), so the Weekend_Night bucket stays at zero. The remaining 8 night hours split by Part 5 tier — specifically, where each night hour falls in the shift's running `l_total` position:







FIGURE 04 · TIER × NIGHT SPLIT


Where Each Night Hour Lands






SPLIT


6 + 2 + 0 + 0











12 SHIFT HOURS · CLOCK TIMES ACROSS THE DAY BOUNDARY




20


21


22


23


00


01


02


03


04


05


06


07







Wed


Wed


Wed


Wed


Thu ↓


Thu


Thu


Thu


Thu


Thu


Thu


Thu








A


PART 5 CASCADE · REG / OT-150 / OT-200






8 hrs REGULAR


2 · 150


2 · 200











B


PART 7 NIGHT WINDOW · 22:00 – 06:00






not night


8 hrs NIGHT


not night








CROSS-PRODUCT · TIER × NIGHT = FOUR BUCKETS







REG × NIGHT


6


Reg_Night_Hours







OT-150 × NIGHT


2


OT_150_Night_Hours







OT-200 × NIGHT


0


OT_200_Night_Hours







WEEKEND × NIGHT


0


Weekend_Night_Hours






Sum = 8 · matches Layer B total · no double count












READ →


Overlay Layer A on Layer B and read where the dark night band intersects each cascade tier. Regular tier ends at hour 8 (clock 04:00). The night window ends at hour 10 (clock 06:00). Six night hours land in Regular (22:00–04:00), two in OT-150 (04:00–06:00), zero in OT-200 (which starts at 06:00 — after the window closed).






## Deduplication with Part 6 Detection


If both detection paths were allowed to fire on the same entry, the same night hours would be counted twice — once via Part 6's tag match and once via Part 7's clock-time overlap. The formula prevents that by giving Part 6 priority: if the entry is tagged as night, Part 7 skips the entry entirely. A local flag set inside Part 6's branch does the guarding:


/* Part 6 detection sets this flag when a tag match fires */

IF (l_time_type = UPPER(l_night_code)) THEN

(

  /* ... existing Part 6 logic ... */

  l_night_detected = 'Y'

)


/* Part 7 detection skips if Part 6 already handled it */

IF (l_night_detected = 'N') THEN

(

  /* Run IS_DATE_BETWEEN + overlap + four-bucket allocation */

)


The flag is reset at every new DETAIL iteration. Two paths, one policy, zero double-counts.


## The Updated Output Portfolio


Four new buckets join the running inventory. The output-array count is now ten — two absence, three worked-time, one aggregate night, and four granular night buckets:







FIGURE 05 · UPDATED PORTFOLIO


Ten Output Buckets After Part 7






TOTAL


10 buckets












PORTFOLIO STATE · AFTER PART 7 EXAMPLE · 10 OUTPUT BUCKETS









12


9


6


3


0


hrs











































            → NEW · PART 7






            0



            0



            8



            2



            2



            0



            6



            2



            0



            0









Abs_Cd






Abs_Hrs






RegHours






OT_150






OT_200






Night






Reg_Ngt


NEW






OT150_Ngt


NEW






OT200_Ngt


NEW






Wknd_Ngt


NEW


















          **not activated** · exists but unfilled in this scenario







          **Part 7 addition** · gold border indicates new bucket















READ →


The gold dashed vertical divider separates Parts 1–6 buckets (left) from Part 7's four new additions (right). Note that in this scenario `Out_Measure_Night_Hours` stays at 0 — the Part 6 tag match didn't fire because the entry was tagged 'Regular'. The clock-time overlap detection did all the work.







NEXT IN THE SERIES


### Part 8 — OT Claim Reconciliation with GET_PLAN_BALANCE Inside a CHANGE_CONTEXTS Block


How the TCR reconciles OT hours it just allocated against previously-claimed OT balances stored in the absence plan — using `GET_PLAN_BALANCE` inside a `CHANGE_CONTEXTS` block so the balance function reads under the right effective-date and legislation code, and why doing it outside the CHANGE_CONTEXTS block returns silently wrong values.



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.





TCR DEEP DIVE · PART 7 / 11


Series tag: #TCRDeepDive