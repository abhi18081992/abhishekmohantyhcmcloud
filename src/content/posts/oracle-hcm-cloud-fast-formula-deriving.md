---
title: "Oracle HCM Cloud Fast Formula: Deriving Daily Working Hours from PER_ASG_WORK_SCH_WORKDAY_PATTERN in TCR Calculations"
description: "ORACLE HCM CLOUD · TCR DEEP DIVE · PART 1 OF 12"
pubDate: 2026-06-05
tags: ["Fast Formula", "Oracle HCM Cloud", "TCR", "OTL", "Time and Labor", "TER", "Time Entry Rule"]
---

ORACLE HCM CLOUD · TCR DEEP DIVE · PART 1 OF 12


# Oracle HCM Cloud Fast Formula: Deriving Daily Working Hours from PER_ASG_WORK_SCH_WORKDAY_PATTERN in TCR Calculations


A breakdown of how Time Calculation Rule formulas parse the workday pattern DBI with INSTR + SUBSTR, guard null schedules with `WAS NOT DEFAULTED`, and compute the monthly norm via `GET_PAY_AVAILABILITY`.


  FAST FORMULA
  OTL
  TIME CALCULATION RULE
  DBI



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant




Before a TCR formula calculates a single hour of overtime, it has to answer one question: **how many hours is this worker supposed to put in on a normal day?**


You'd think this comes from a DBI. It doesn't — not reliably. `PER_ASG_STANDARD_WORKING_HOURS` exists, but it returns *weekly* hours. For a worker on a compressed schedule — say, four 10-hour days — dividing that by 5 gives you the wrong answer. The daily threshold isn't 8. It's 10.


So the formula does something the documentation never mentions: it parses the worker's **workday pattern string**, one character at a time, seven times in a row.


## The PER_ASG_WORK_SCH_WORKDAY_PATTERN DBI Structure


Oracle stores a worker's weekly schedule shape in `PER_ASG_WORK_SCH_WORKDAY_PATTERN` as a hyphen-delimited string. The format is one slot per day, Sunday through Saturday:



RAW DBI VALUE


0 - 8 - 8 - 8 - 8 - 8 - 0






SUN


0






MON


8






TUE


8






WED


8






THU


8






FRI


8






SAT


0






5 WORKING DAYS · 40 WEEKLY HOURS · 8 HRS/DAY


For a compressed-week worker (Mon–Thu, 10 hours each), the same DBI holds `0-10-10-10-10-0-0`. Four working days, 40 weekly hours, but **10 hours/day** is the threshold for overtime — not 8.


This is the number the formula needs to derive at runtime.


## Iterative String Parsing with INSTR and SUBSTR in Fast Formula


The implementation is brute-force elegant. Three local variables hold the state:


  - `l_wrk_pattern` — the remaining string, shrinking left-to-right with each pass

  - `l_count` — count of working days seen so far (slots where value ≠ '0')

  - `l_normal_hours` — running sum of hours from those working days


Each iteration finds the next hyphen, extracts the slot before it, decides whether to count it, then trims the slot off the front of the string. Seven iterations cover all seven days. The seventh uses `length(l_wrk_pattern)` instead of `l_indicate-1` because the final slot has no trailing hyphen.


/* Iteration 1 — first slot */

l_wrk_pattern = PER_ASG_WORK_SCH_WORKDAY_PATTERN

l_indicate    = INSTR(l_wrk_pattern, '-')

l_wrk_day     = SUBSTR(l_wrk_pattern, 1, l_indicate-1)

IF (l_wrk_day <> '0') THEN

( l_count       = l_count + 1

  l_normal_hours = l_normal_hours + to_number(l_wrk_day) )


/* Iterations 2–6 — shift left, repeat */

l_wrk_pattern = SUBSTR(l_wrk_pattern, l_indicate+1)

l_indicate    = INSTR(l_wrk_pattern, '-')

l_wrk_day     = SUBSTR(l_wrk_pattern, 1, l_indicate-1)

/* ...same IF block... */


/* Iteration 7 — last slot, no trailing hyphen */

l_wrk_pattern = SUBSTR(l_wrk_pattern, l_indicate+1)

l_wrk_day     = SUBSTR(l_wrk_pattern, 1, length(l_wrk_pattern))

/* ...final IF block... */


l_working_hours = ROUNDUP((l_normal_hours/l_count), 2)


## Parser Execution Trace — Local Variable State per Iteration


Walking the parser through `0-8-8-8-8-8-0`:




    | ITER
        | l_wrk_pattern
        | l_wrk_day
        | l_count
        | l_normal_hours
      |




        | 1
        | 0-8-8-8-8-8-0
        | '0' (skip)
        | 0
        | 0
      |


        | 2
        | 8-8-8-8-8-0
        | '8'
        | 1
        | 8
      |


        | 3
        | 8-8-8-8-0
        | '8'
        | 2
        | 16
      |


        | 4
        | 8-8-8-0
        | '8'
        | 3
        | 24
      |


        | 5
        | 8-8-0
        | '8'
        | 4
        | 32
      |


        | 6
        | 8-0
        | '8'
        | 5
        | 40
      |


        | 7
        | 0
        | '0' (skip)
        | 5
        | 40
      |






RESULT


l_working_hours = ROUNDUP(40 / 5, 2) = 8.00


Switch the same worker to four 10-hour days (`0-10-10-10-10-0-0`) and the same parser yields `40 / 4 = 10.00`. The downstream OT threshold logic shifts automatically — no rule parameter change, no recompile.


## Null-Safe DBI Reads with the WAS NOT DEFAULTED Guard


The parser sits inside a guard:


IF (PER_ASG_WORK_SCH_WORKDAY_PATTERN WAS NOT DEFAULTED)

THEN (

  /* ...7-iteration parser... */

)

ELSE

  l_working_hours = 8


If the worker has no schedule attached — common for new hires before the OTL admin assigns one — the DBI defaults, the IF skips, and the formula assumes a standard 8-hour day. The worker doesn't crash the timecard. They just calculate against a safe default.


This pattern matters because `WAS NOT DEFAULTED` is only valid on input variables and DBIs — not on locally computed variables. The check has to happen *before* the parser tries to `INSTR` a null string. Get this guard wrong and you'll see `ORA-01403: no data found` bubble through the rule execution log with no clear pointer back to the source line.


## Computing Monthly Working Hours with GET_PAY_AVAILABILITY


The daily threshold is only half the answer. When OT also has a **monthly cap** — hours beyond the monthly working norm spill into OT 150% buckets regardless of which day they fall on — the formula needs to extend the daily number into a monthly target. Three lines do it:


l_month_start_date = periodStartDate

l_month_end_date   = periodEndDate

l_working_days = GET_PAY_AVAILABILITY('ASSIGN',

               l_month_start_date, l_month_end_date,

               'Y','Y','Y','Y','D')

l_monthly_hours = l_working_hours * l_working_days


`GET_PAY_AVAILABILITY` walks the period and returns the working day count, honoring the worker's schedule and the holiday calendar attached to the LDG. The five trailing flags — `'Y','Y','Y','Y','D'` — toggle weekday inclusion (Mon/Tue/Wed/Thu/Fri) and the return unit ('D' for days, 'H' for hours).


Multiply daily threshold by working days and you have the monthly norm. For an 8-hour worker in a 22-working-day month: **176 monthly hours**. Cross that, and the OT 150 cascade fires downstream.



A NOTE ON ROUNDUP


Fast Formula doesn't ship with a native `ROUNDUP`. The line `l_working_hours = ROUNDUP((l_normal_hours/l_count),2)` only compiles if a custom function with that name has been registered at the instance level (via Setup & Maintenance → *Manage Formula Functions*). If you lift this parser into your own formula, swap `ROUNDUP` for `ROUND(...)` or build a CEIL-based equivalent — otherwise the compile will fail with a function-not-found error and the rule will refuse to validate.


## Why Fast Formula Lacks a String Array Type — and Loop Unrolling as the Workaround


The parser is verbose, repetitive, and could absolutely be a `WHILE` loop. The original developer chose explicit unrolling for one reason: **Fast Formula has no string array type**. You can't split on a delimiter into a collection. You can't `FOR EACH` over the slots. You can only INSTR + SUBSTR your way through, one slot at a time. Unrolling the loop makes the seven-day boundary visible to anyone reading the code six months later — and seven is a hard ceiling, so the loop guard would be a magic number anyway.


That's the broader pattern this series will keep returning to: in a long TCR formula, the boring code is often the load-bearing code. The clever parts get rewritten. The ugly parts run for a decade.



NEXT IN THE SERIES


### Part 2 — Day-Type Branching with GET_DATE_DAY_OF_WEEK, Public Holiday Override, and the FULL_TIME Fork


Why `GET_DATE_DAY_OF_WEEK` alone isn't enough to fork OT logic — the formula needs a FRI-anchored weekly compare, a `pOvrdPubCat` rule parameter for public holiday overrides, and a `PER_ASG_FULL_PART_TIME` DBI check before threshold logic activates.



AM




Abhishek Mohanty


Oracle ACE Associate  |  AIOUG Member  |  Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.





TCR DEEP DIVE · PART 1 / 5


Series tag: #TCRDeepDive