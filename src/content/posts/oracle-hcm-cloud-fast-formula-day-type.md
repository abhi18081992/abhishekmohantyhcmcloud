---
title: "Oracle HCM Cloud Fast Formula: Day-Type Branching in TCR Calculations with GET_DATE_DAY_OF_WEEK, CALL_FORMULA Holiday Resolution, and the PER_ASG_FULL_PART_TIME Fork_TCR Part-2"
description: "ORACLE HCM CLOUD · TCR DEEP DIVE · PART 2 OF 12"
pubDate: 2026-06-09
tags: ["Fast Formula", "Oracle HCM Cloud", "TCR", "OTL", "Time and Labor"]
---

ORACLE HCM CLOUD · TCR DEEP DIVE · PART 2 OF 12


# Oracle HCM Cloud Fast Formula: Day-Type Branching in TCR Calculations with GET_DATE_DAY_OF_WEEK, CALL_FORMULA Holiday Resolution, and the PER_ASG_FULL_PART_TIME Fork


How a Time Calculation Rule formula picks the right OT bucket — examining `GET_DATE_DAY_OF_WEEK` return values, the FRI-anchored weekly compare via `ADD_DAYS` in a `WHILE 1=1` loop, the `CALL_FORMULA` bind syntax for holiday resolution, and the four-way day-type fork.


  FAST FORMULA
  OTL
  TIME CALCULATION RULE
  CALL_FORMULA



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant




In Part 1 the formula derived `l_working_hours` and `l_monthly_hours` — the daily and monthly thresholds. Knowing the threshold isn't enough. **The same hour worked on a Tuesday afternoon doesn't pay the same as that hour worked on a Sunday or on a public holiday.**


Most OT regimes have at least four distinct day types — regular weekday, Saturday, Sunday, and gazetted public holiday — and each one routes worked hours into a different OT bucket. `GET_DATE_DAY_OF_WEEK` alone doesn't distinguish a regular Wednesday from Wednesday-when-Diwali-falls-on-a-Wednesday. The formula has to do that disambiguation itself.


This post walks through the four Oracle HCM Cloud constructs the formula uses to make that decision: the day-of-week function, an `ADD_DAYS`-based scan for the next Friday, a `CALL_FORMULA` invocation that resolves the public holiday calendar, and a text-DBI fork on `PER_ASG_FULL_PART_TIME`.


## GET_DATE_DAY_OF_WEEK Return Values and Date-to-Day-Name Conversion


`GET_DATE_DAY_OF_WEEK` is a built-in Fast Formula function that takes a date and returns the corresponding day name as a three-letter uppercase string. It is locale-independent — the return values do not change with the user's session language:



RETURN VALUES — FIXED, LOCALE-INDEPENDENT






'SUN'






'MON'






'TUE'






'WED'






'THU'






'FRI'






'SAT'






Every comparison in the day-type branch must use uppercase three-letter literals: `l_week_day = 'SAT'`, never `'Sat'` or `'Saturday'`. Mismatched case silently fails the IF branch and the formula falls through to weekday logic.


The TCR formula calls it once per measure period entry against the timecard's start time:


l_week_day = GET_DATE_DAY_OF_WEEK(aiStartTime)

flog = add_log(ffs_id, '>>> ffName: ' || ffName || ' l_week_day ' || l_week_day)


From here, every subsequent branch in the formula compares against `l_week_day` using equality on those exact string literals.


## The FRI-Anchored Weekly Compare with ADD_DAYS and WHILE 1=1 LOOP


Day-of-week alone tells you what day it is. It doesn't tell you whether you've crossed into a new *OT week*. Most OT regimes accumulate worked hours against a weekly cap that resets every Friday at midnight — so the formula needs to know when "this Friday" passes to clear the running weekly counter.


The pattern used here is a `WHILE 1=1 LOOP` that walks forward day by day from the current timecard entry until it lands on a Friday, then stores that date as the reset boundary:


IF ((aiStartTime > l_date_compare) AND (l_week_day <> 'SAT') AND (l_week_day <> 'SUN')) THEN

( l_weekly_reg = 0 )


IF (l_week_day = 'SAT' OR l_week_day = 'SUN') THEN

( l_weekly_reg = 0 )

ELSE

(

  j = 1

  WHILE( 1=1 ) LOOP

  (

    l_temp_date = ADD_DAYS(aiStartTime, j)

    l_temp_week_day = GET_DATE_DAY_OF_WEEK(l_temp_date)

    IF (l_temp_week_day = 'FRI') THEN

    (

      l_date_compare = l_temp_date

      EXIT

    )

    ELSE

      j = j + 1

  )

)


Three Oracle HCM Cloud constructs are worth pausing on here:


  - **`ADD_DAYS(date, integer)`** — adds the integer to the date and returns a date. Negative integers walk backwards. Fast Formula evaluates this purely as arithmetic on the underlying date column; there is no calendar consultation, no holiday awareness, no DST adjustment.

  - **`WHILE 1=1 LOOP`** — Fast Formula has no native FOR-loop construct that increments by 1. The idiomatic pattern is an infinite WHILE with manual counter advance and an explicit `EXIT` when the termination condition is met. This is safer than `WHILE (j

## CALL_FORMULA Pattern for Worker Holiday Schedule Resolution


Knowing it's a Wednesday isn't enough. The formula has to know whether *this* Wednesday is also a public holiday — and the public holiday list lives in a Worker Holiday Calendar attached to the worker's LDG, not in any DBI the TCR formula can read directly.


The escape hatch is `CALL_FORMULA`, which invokes another Fast Formula and binds its inputs and outputs by name. The TCR delegates holiday resolution to a utility formula:


CALL_FORMULA ('XX_HOLIDAY_LOOKUP_FF'

  , ffs_id            > 'ffs_id'

  , rule_id           > 'rule_id'

  , l_holiday_cat   > 'holiday_category'

  , l_start_time    > 'start_date_override'

  , l_stop_time     > 'end_date_override'

  , l_holiday_count 'OUT_COUNT'  DEFAULT 0

  , l_holiday_dates 'OUT_DATES'  DEFAULT EMPTY_DATE_NUMBER

)


The syntax is non-obvious if you've never seen it before. The two arrow operators distinguish input bindings from output bindings:





>


**Input binding.** Local variable on the left flows into the called formula's input parameter (named on the right). The local must already be populated.





A NOTE ON DEFAULT FOR OUTPUT BINDINGS


Unlike the `DEFAULT FOR  IS` declaration at the top of the formula, the `DEFAULT` clause inside a `CALL_FORMULA` bind is required, not optional. Omit it and the formula will compile but fail at runtime with *"output parameter must specify DEFAULT value"*. The default has to match the declared type of the local variable — `0` for number, `EMPTY_DATE_NUMBER` for date arrays, `' '` for text.


## Inside the Called Formula — How Bindings Map to INPUTS and RETURN


For the `CALL_FORMULA` bindings to resolve cleanly, the called formula must declare its inputs and return its outputs using exactly the labels the caller specifies. Here's the skeleton of `XX_HOLIDAY_LOOKUP_FF` showing both sides of the contract:


/****************************************************************

 * FORMULA NAME : XX_HOLIDAY_LOOKUP_FF

 * FORMULA TYPE : Time Calculation Rules

 * DESCRIPTION  : Returns the count and date list of public holidays

 *              for a worker over a date range, filtered by

 *              a configurable holiday category code.

 ****************************************************************/


INPUTS ARE

  ffs_id              (number),

  rule_id             (number),

  holiday_category    (text),

  start_date_override (date),

  end_date_override   (date)


/* Local declarations */

ffName      = 'XX_HOLIDAY_LOOKUP_FF'

l_person_id = GET_CONTEXT(HWM_RESOURCE_ID, 0)

OUT_COUNT   = 0

OUT_DATES   = EMPTY_DATE_NUMBER


/* Fetch the count via a parameterized value set that queries the

   calendar event repository for the worker's holiday eligibility */

l_params = '|=P_PERSON_ID='''   || TO_CHAR(l_person_id)

        || '''|P_START_DATE=''' || TO_CHAR(start_date_override, 'YYYY-MM-DD')

        || '''|P_END_DATE='''   || TO_CHAR(end_date_override,   'YYYY-MM-DD')

        || '''|P_CATEGORY='''    || holiday_category || ''''


OUT_COUNT = TO_NUMBER(GET_VALUE_SET('XX_HOLIDAY_COUNT_VS', l_params))


/* OUT_DATES would be populated similarly via a date-array value set

   or a holiday DBI iteration loop. Omitted here for brevity. */


RETURN OUT_COUNT, OUT_DATES


Three contracts to notice between the caller and the called formula:


  - **Input names match the caller's bind labels.** The caller writes `l_holiday_cat > 'holiday_category'`, so the called formula must declare `holiday_category` in its INPUTS block with a matching type. Typos here fail at runtime, not at compile time.

  - **Output names match the caller's bind labels.** The caller writes `l_holiday_count

## Externalizing the Public Holiday Category via a Rule Input Parameter


The holiday category bind is the one parameter most engineers miss. The Worker Holiday Calendar can hold multiple *categories* of non-working days — gazetted public holidays, optional restricted holidays, bridge days, company-declared shutdowns. Each category has its own OT treatment.


The TCR formula reads which category counts as a "real" holiday for OT purposes from a rule input parameter, populated when the rule is configured under *Setup and Maintenance → Manage Time Calculation Rules*:


/* Fixed Values from Rule Input parameters */

l_holiday_cat = get_rvalue_text(rule_id, 'HOLIDAY_CATEGORY_CODE', 'PH')


`get_rvalue_text` reads a text parameter off the rule definition by name (`'HOLIDAY_CATEGORY_CODE'`), falling back to `'PH'` if the parameter wasn't configured. The same formula deployed for two different LDGs can therefore treat different calendar categories as the "real" holiday set — without recompiling.


This is one of the cleanest separations of policy and code in the Fast Formula language. The rule parameter is the policy. The formula is the engine. Reuse follows naturally.


## The PER_ASG_FULL_PART_TIME Fork — Why Default 'X' Matters


Even after day-type is resolved, the formula has one more fork: **part-time workers don't trigger the monthly threshold the same way full-time workers do**. A part-timer's "normal" daily hours might be 4. A full-timer's might be 8. Both can rack up OT, but the bucket-fill mechanics differ.


The split is gated by `PER_ASG_FULL_PART_TIME`, a text DBI whose values are `'FULL_TIME'` or `'PART_TIME'` drawn from the worker's assignment record. Notice the default at the top of the formula:


DEFAULT FOR PER_ASG_FULL_PART_TIME IS 'X'


The fallback is `'X'`, not `' '`. The reason is deliberate. Both branches in the fork compare against specific values:


IF (PER_ASG_FULL_PART_TIME = 'FULL_TIME') THEN

( /* monthly threshold logic */ )

ELSE

( /* part-time / public holiday logic */ )


If the DBI is null and the default was a blank string, the comparison `' ' = 'FULL_TIME'` returns false and the ELSE branch fires — silently routing a worker with missing data through the part-time path. `'X'` as the sentinel makes the missing-data case explicit in logs — `PER_ASG_FULL_PART_TIME: X` in the rule execution log is a clear signal that the worker's assignment is incomplete and the calculation should be reviewed.


This is a small thing. It saves hours of debugging in production.


## Day-Type Branching Flow — SAT, SUN, Weekday, and Public Holiday Paths


With all four constructs in hand — day-of-week, weekly compare, holiday count, full-time flag — the formula assembles them into a four-way fork. Once the call to `CALL_FORMULA` returns and `l_holiday_count` is populated, the decision tree fires:




    | CONDITION
        | PATH
        | BUCKET FILLED
      |




        | l_holiday_count = 1
        | **Public Holiday**
        | All worked hours → OT 200%
      |


        | l_week_day = 'SAT'
        | **Saturday**
        | First `l_working_hours` → OT 200%; surplus → OT 150%
      |


        | l_week_day = 'SUN'
        | **Sunday**
        | All worked hours → OT 200%
      |


        | Weekday + FULL_TIME
        | **Regular Weekday**
        | Worked hours → Regular until monthly cap; surplus → OT 150%
      |





The cascade is evaluated top-down with `IF / ELSE IF / ELSE`. **The public holiday check is the outermost gate because a holiday that falls on a Sunday is still a holiday** — the formula must not let Sunday's OT 200% logic override the holiday's OT 200% logic just because the comparison happens to produce the same multiplier. The two paths fill different output buckets downstream, which matters for payroll element mapping in Part 4.


Each branch ends by zeroing `l_reg` (regular hours), since worked hours on a non-regular day don't contribute to the weekly or monthly normal-time accumulator. Only the weekday branch can leave `l_reg` populated.


## Why Use CALL_FORMULA Instead of Inlining the Holiday Lookup


A reasonable question — why route through a separate utility formula at all? The TCR could read the holiday calendar inline with array DBIs like `PER_HOLIDAY_DATE_LIST` and avoid the call overhead.


The separation pays for itself three ways:


  - **Reuse.** The same holiday-resolution formula is called from absence accrual matrices, entry validations, and other TCR rules. Centralizing it means changes to the calendar interpretation (new category filters, date-range adjustments) ripple to all callers without touching them.

  - **Testability.** The utility formula can be unit-tested by directly executing it from the Fast Formula UI with sample input values — much easier than running an entire TCR for one date.

  - **Compilation scope.** Array DBIs like `PER_HOLIDAY_DATE_LIST` require specific contexts (LDG_ID, EFFECTIVE_DATE) that not every formula type supplies. Putting them in a dedicated formula with the right type isolates the context dependency to one place.


`CALL_FORMULA` has overhead — every call instantiates a new evaluation context. For a TCR that fires once per measure period entry, that overhead is negligible. For a payroll batch processing tens of thousands of assignments, you'd profile before relying on it heavily.



NEXT IN THE SERIES


### Part 3 — The Main Iteration Loop with HWM_CTXARY_RECORD_POSITIONS, aiRecPosition, and the Infinite-Loop Guard


How a TCR walks the timecard one entry at a time — array iteration via `HWM_CTXARY_RECORD_POSITIONS`, the `aiRecPosition = 'DETAIL'` vs `'END_DAY'` branch, the `HWM_CTXARY_HWM_MEASURE_DAY` companion array, and the defensive `raise_error` at nidx > 1000 that saves your rule from a runaway loop.



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.





TCR DEEP DIVE · PART 2 / 10


Series tag: #TCRDeepDive