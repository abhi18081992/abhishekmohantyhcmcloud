---
title: "Oracle Fast Formula: Time Entry Rule (Part 3)"
description: "Oracle Fast Formula: Time Entry Rule (Part 1) — Inputs, Contract, and Architecture"
pubDate: 2026-05-29
tags: ["Fast Formula", "Oracle HCM Cloud", "TER", "Time Entry Rule", "OTL"]
---

Oracle Fast Formula: Time Entry Rule (Part 1) — Inputs, Contract, and Architecture
- Fast Formula
  Time Entry Rule
  OTL
  Hands-On


May 21, 2026 • 15 min read • Oracle HCM Cloud


  The TER Series
  Part 3 of 4

    1. OTL Foundations ·
    2. The Input Contract ·
    3. Algorithm: Routing & Overlap ·
    4. The State Machine



# The Algorithm: Setup, Routing, and Overlap DetectionPart 3 of 4 — The TER Series


  AM

    Abhishek Mohanty
    Oracle ACE Apprentice · AIOUG Member · Oracle HCM Cloud Consultant & Technical Lead



Parts 1 and 2 covered what TER does and the data it receives. Now we get into the algorithm. This post covers the setup phase, the per-line routing logic that decides which checks apply to which rows, and the day-boundary pairwise overlap test. Part 4 will finish with the state machine.


## Setup — What Runs Before the Loop


Five blocks of scaffolding run once at the top of the formula, before the loop touches a single timecard line. Each block has one job:


  **Block 1** declares the input arrays so the formula won't crash on an empty slot.

  - **Block 2** grabs identifiers from the framework and writes a startup log line.

  - **Block 3** binds the worker's assignment context once for the entire formula body.

  - **Block 4** reads tunable values from the rule configuration so the formula stays portable across legal entities.

  - **Block 5** initialises the variables the loop will need — output array, counters, day buffer, stretch tracker, meal flag.


Each annotated block below pairs the actual code with a numbered breakdown of what it does and, where helpful, a short Excel snippet showing the data being shaped.




    Setup phase · Blocks 1–5
    Annotated









```
DEFAULT FOR RECORD_POSITIONS IS EMPTY_TEXT_NUMBER
DEFAULT FOR measure          IS EMPTY_NUMBER_NUMBER
DEFAULT FOR PayrollTimeType  IS EMPTY_TEXT_NUMBER
DEFAULT FOR StartTime        IS EMPTY_DATE_NUMBER
DEFAULT FOR StopTime         IS EMPTY_DATE_NUMBER

INPUTS ARE RECORD_POSITIONS, measure, PayrollTimeType,
           StartTime, StopTime
```




        Block 1 · Crash prevention




Diagram for this annotation · Three concepts together




Part 1 · The shape: six parallel arrays sharing row indexes






            | Idx
                | RECORD_POSITIONS
                | measure
                | PayrollTimeType
                | StartTime
                | StopTime
              |




                | [1]
                | HEADER
                | missing
                | missing
                | missing
                | missing
              |


                | [2]
                | empty
                | 1.5
                | Reg Hours
                | 08:30
                | 10:00
              |


                | [3]
                | empty
                | 4.75
                | Reg Hours
                | 10:00
                | 14:45
              |


                | [4]
                | END_DAY
                | missing
                | missing
                | missing
                | missing
              |







Marker rows ([1] HEADER, [4] END_DAY) carry a value only in RECORD_POSITIONS — the other columns are **genuinely missing**, not blank, not zero.




Part 2 · What DEFAULT FOR does at runtime







WITHOUT DEFAULT FOR — CRASH




Code:


aiStartTime = StartTime[1]


Result:


✗ Fast Formula has no instruction
✗ Throws FFL-09100
✗ Crashes the entire submission


Worker sees: "Submission failed, contact administrator"








WITH DEFAULT FOR — SAFE




Code:


DEFAULT FOR StartTime IS
  EMPTY_DATE_NUMBER


Result:


✓ FF treats array as empty
✓ .exists(1) returns FALSE
✓ Formula skips and continues










Part 3 · The naming convention: EMPTY__







EMPTY_


prefix






TEXT_


value-type






NUMBER


key-type










            | Constant
                | Use it for
              |



              | EMPTY_TEXT_NUMBER | RECORD_POSITIONS, PayrollTimeType |

              | EMPTY_DATE_NUMBER | StartTime, StopTime |

              | EMPTY_NUMBER_NUMBER | measure |










            TAKEAWAY: Every framework array needs its own DEFAULT FOR matched to its data type. One line saved → production crash. One line spent → submission survives marker rows.












1The shape of the input



              - When a worker submits a timecard, OTL doesn't pass the rows one-by-one to the formula. It hands over **six parallel arrays** — one per data column — that all share the same row indexes.

              - Picture this as a giant spreadsheet: each row in the timecard becomes one slot across all six arrays. Slot [3] in `StartTime` describes the same row as slot [3] in `PayrollTimeType` and `StopTime`.

              - The catch: **not every row fills every column**. Boundary rows like HEADER, END_DAY, and END_PERIOD only carry a value in `RECORD_POSITIONS`; their slots in the other five arrays are genuinely missing — not blank, not zero, but absent.

              - If your formula reads `StartTime[1]` on a HEADER row, you're asking for data that isn't there. Fast Formula will not silently return null. It will crash the entire submission with `FFL-09100`.








2What DEFAULT FOR actually does



              - `DEFAULT FOR ... IS EMPTY_TEXT_NUMBER` tells Fast Formula: *"this is an array variable. If it shows up empty at runtime, give me an empty array, not an error."*

              - Without it, the moment the formula starts and Fast Formula tries to bind the input variable, it has no instruction for how to handle an empty array. Compilation succeeds (the syntax is fine) but execution dies on first read.

              - Worse, the failure is opaque to the worker. They don't see *"missing default declaration on input array"*. They see *"submission failed, please contact your administrator"*. Hours of investigation follow.

              - The cost of adding the declaration is one line per input. The cost of skipping it is a production incident.








3The naming convention, decoded



              - The constant names look cryptic but follow a strict pattern: *{value-type}_{key-type}*.

              - `EMPTY_TEXT_NUMBER` is an array of **text values** indexed by **numbers**. That's what `RECORD_POSITIONS` needs — values like 'HEADER' and 'END_DAY' keyed by row number.

              - `EMPTY_DATE_NUMBER` matches `StartTime` and `StopTime`: dates indexed by row number.

              - `EMPTY_NUMBER_NUMBER` matches `measure`: numeric quantities indexed by row number.

              - Pick the wrong constant and you get a type-mismatch error at compile time — loud and easy to fix. The truly dangerous bug is forgetting the declaration entirely, which compiles silently.






Every framework array needs its own `DEFAULT FOR` declaration matched to its data type. The cost is one line; skipping it ships a formula that compiles fine but crashes the first time it meets a real-world timecard with marker rows.













```
ffName  = 'XX_TER_CONTINUOUS_HOURS_VALIDATION'
ffs_id  = GET_CONTEXT(HWM_FFS_ID, 0)
rule_id = GET_CONTEXT(HWM_RULE_ID, 0)

NullDate = '01-JAN-1900' (DATE)
NullText = '**FF_NULL**'

rLog = add_rlog(ffs_id, rule_id,
                '>>> Enter ' || ffName)
```




        Block 2 · Self-identification



Analyze_Rule_Processing_Details.xlsxExcel



            | Time | Worker | Log Line |


              | 18:15:02 | Sarah B. | `>>> Enter XX_TER_CONTINUOUS_HOURS_VALIDATION` |

              | 18:15:02 | Sarah B. | idx=2 type=Reg start=08:30 stop=10:00 |

              | 18:15:02 | Sarah B. | FLAG idx=3: contHrs=6.25 |







Each `add_rlog` call surfaces here, scoped by `ffs_id` and `rule_id`.





Diagram for this annotation · Three concepts together




Part 1 · The formula introduces itself — capture identity from framework







ffName · YOUR LOCAL VAR




'XX_TER_CONTINUOUS_
  HOURS_VALIDATION'


Return-address stamp. Travels with every log line.








ffs_id · FROM GET_CONTEXT




GET_CONTEXT(
  HWM_FFS_ID, 0)


Unique per submission. Set when worker clicks Submit.








rule_id · FROM GET_CONTEXT




GET_CONTEXT(
  HWM_RULE_ID, 0)


Identifies which rule triggered this run.








**Together, ffs_id + rule_id form the address** the support team uses to filter production logs to just this worker's submission.




Part 2 · Sentinel values — standing in for "logically empty"







THE FAST FORMULA QUIRK




Once a slot exists, it MUST hold a value.


There is no "declared but contains nothing" state. It either holds something or doesn't exist at all.


The problem this creates:


Need a way to say "this variable is logically empty" while it still holds something.








THE SENTINEL FIX




Pick impossible values as stand-ins.


NullDate = '01-JAN-1900'


NullText = '**FF_NULL**'


A date a century in the past or text with double-asterisks — values real data could **never** produce. If one reaches a worker's screen, the bug is visible.










Part 3 · The opening log line — three segments, each with a job









>>>






Enter






XX_TER_CONTINUOUS_HOURS_VALIDATION










grep prefix


filter for entry/exit






verb


"started running"






formula name (ffName)


return-address stamp on every log line in production











            TAKEAWAY: Capture session and rule IDs in scope. Tag every log line with the formula name. Future-you, debugging at 11 PM under deadline, will thank present-you for the extra minute.












1The formula introduces itself



              - The formula starts by recording its own name in a local variable (`ffName`). This name will travel through every log line the formula writes — effectively a return-address stamp on each entry so you can grep production logs and find every line this specific formula produced.

              - Two more values come from the framework via `GET_CONTEXT`. `ffs_id` is a unique identifier for this *specific submission* — assigned by OTL the moment the worker clicks Submit. `rule_id` identifies the validation rule that triggered this formula run.

              - Together these two IDs are **the address used to look up this run's logs later**. When a worker reports an issue, the support team filters logs by `ffs_id` and the noise of every other concurrent submission disappears, leaving just this worker's run.

              - Without these IDs in scope, every `add_rlog` call that follows would have nowhere to anchor itself — the logs would be untraceable.








2Sentinel values explained



              - Fast Formula has a quirk that catches people coming from other languages: **once an array slot exists, it must hold a value**. There is no concept of "this slot has been declared but contains nothing." It either holds something or it doesn't exist at all.

              - That makes a problem. The formula needs to express "this variable is logically empty" while still holding *something*. The conventional fix is a sentinel — an impossible value that real data could never produce, used as a stand-in for emptiness.

              - `NullDate = '01-JAN-1900'` picks a date so far in the past it could never appear on a real timecard. `NullText = '**FF_NULL**'` uses a string with double-asterisk markers that wouldn't survive any real data-entry process.

              - The choice of sentinel is deliberate. If you saw `'01-JAN-1900'` reach a worker's screen, you'd know immediately something went wrong — the value should have been overwritten before output. The sentinel is also a debugging tool: it makes broken code *visible* instead of letting it propagate silently as `NULL` would in other languages.








3The opening log line


What appears in production logs>>> Enter XX_TER_CONTINUOUS_HOURS_VALIDATION



              - This single line writes a record to the OTL Formula Run Log announcing that the formula has started executing. The triple-arrow prefix (`>>>`) is a convention that makes log entries grep-friendly — you can filter for entry/exit lines and ignore intermediate ones.

              - The verb *"Enter"* is paired with a corresponding *"Exit"* log line at the bottom of the formula, so a complete run shows up as a clean entry-exit pair in the log. Anything between them is intermediate work; anything outside them is somebody else's formula.

              - The formula name (`ffName`) acts as a return-address stamp on every subsequent log line. When you have ten formulas attached to one timecard run, this is what tells you which line came from which formula.

              - Together these three pieces — prefix, verb, formula name — turn a stream of log noise into a structured, filterable trail. The cost is one line of code; the payoff is hours saved during production triage.






Capture session and rule IDs in scope so every subsequent log line can be traced back to its origin. Tag every log line with the formula name. Future-you, debugging a production issue with a tight deadline, will be glad present-you took the extra minute.













```
CHANGE_CONTEXTS(HR_ASSIGNMENT_ID = HWM_PER_ASG_ASSIGNMENT_ID)
(
  /* entire body lives inside this block */
```




        Block 3 · Single context wrap




Diagram for this annotation · Three concepts together




Part 1 · CHANGE_CONTEXTS = signing in to the worker's session







SIGN IN


load profile, set permissions




→




DO WORK


read DBI, value sets, etc.




→




SIGN OUT


teardown session






Sign-in & sign-out are fixed costs (~2 ms), paid every wrap.




Part 2 · Two strategies, same work — the wrap pattern matters







STRATEGY A · PER-DBI WRAP — WRONG




CHANGE_CONTEXTS(...) ( DBI[1] )
CHANGE_CONTEXTS(...) ( DBI[2] )
CHANGE_CONTEXTS(...) ( DBI[3] )
    ...
CHANGE_CONTEXTS(...) ( DBI[200] )



200 wraps × ~2 ms each


= ~400 ms wasted on overhead


Most of the time isn't doing work — it's signing in and out, repeatedly.








STRATEGY B · SINGLE OUTER WRAP — RIGHT




CHANGE_CONTEXTS(...)
(
  DBI[1]  DBI[2]  DBI[3]
  ...
  DBI[200]
)



1 wrap × ~2 ms total


= ~2 ms total overhead


Sign in once, do all the work, sign out at the end.










Part 3 · The performance numbers, in real terms







Strategy A:





~400 ms






Strategy B:









~2 ms





              0 ms200 ms400 ms








SCALE IMPLICATION:


A pay run processes tens of thousands of timecards. At 400 ms wasted per submission, that's **hours of CPU time and database session pressure** across a single batch — enough to delay payroll cutoff.







            TAKEAWAY: One outer CHANGE_CONTEXTS wrap. Tag the closing paren so you can find it 200 lines later. The change is invisible to readers but saves hundreds of milliseconds per submission — and adds up fast across a pay run.












1What CHANGE_CONTEXTS actually does



              - `CHANGE_CONTEXTS` binds an HCM context value — in this case, `HR_ASSIGNMENT_ID` — for everything that runs inside its parentheses. Any DBI fetch, any value-set lookup, any worker-specific resolution that happens within the block automatically gets evaluated against this assignment.

              - Think of it like signing in to an application. Every sign-in carries a fixed cost: load the profile, validate the session, set up permissions, prime the personalisation cache. None of these are heavy individually, but they add up.

              - If you signed in, fetched one piece of data, signed out, and repeated this hundreds of times in sequence, most of your time would go to the sign-in/sign-out cycle — not the actual work. The pattern is wasteful.

              - Database queries inside Fast Formula behave the same way. Each `CHANGE_CONTEXTS` call has fixed setup and teardown overhead, perhaps two milliseconds. Inside a 200-iteration loop, that overhead compounds.








2Why one outer wrap beats many inner wraps



              - The architectural choice is to wrap **the entire formula body** in one outer `CHANGE_CONTEXTS` at the top, rather than wrapping each individual DBI fetch as it appears.

              - The formula effectively "signs in" once at the top and stays signed in for the rest of its execution. Every database lookup, every holiday calendar query (`GET_VALUE_SET`), every `PER_*` DBI fetch, every worker-specific resolution that happens anywhere in the body automatically uses the same binding without re-binding.

              - The framework internally optimises for this pattern. A single deep context binding is far cheaper than 200 shallow ones, because most of the binding cost is paid once.

              - The trade-off is structural: your entire formula body now sits inside one giant pair of parentheses, which can make the code feel disconnected from where it opens. Mitigate by tagging the closing paren with a comment so you can find it when scrolling 200 lines later.








3The performance numbers, in real terms



              - Per-DBI wrap on a typical biweekly timecard with 200 entries: roughly **400 milliseconds wasted on context-binding overhead alone**, before any actual validation work happens.

              - Single outer wrap: about **2 milliseconds total**. The same work, 200× faster.

              - This sounds like a micro-optimisation, but it isn't. A pay run might process tens of thousands of timecards. At 400 ms wasted per submission, that's hours of CPU time and database session pressure across a single batch — enough to delay payroll cutoff in busy enterprises.

              - The fix costs nothing in code complexity (it's actually simpler), and the performance benefit scales with timecard size.






One outer `CHANGE_CONTEXTS` wrap binds the assignment context once for the entire formula body. Tag the closing paren with a comment so you can find it later. The change is invisible to readers but saves hundreds of milliseconds per submission — and adds up fast across an entire pay run.













```
  p_break_type    = 'Meal Break'
  p_reg_type      = 'Regular Hours'

  p_sched_start   = get_rvalue_number(rule_id,
                       'SCHEDULE_START_HOUR', 9)
  p_sched_end     = get_rvalue_number(rule_id,
                       'SCHEDULE_END_HOUR', 18)
  p_max_cont_err  = get_rvalue_number(rule_id,
                       'MAX_CONTINUOUS_HRS_ERR', 6)
  p_max_cont_warn = get_rvalue_number(rule_id,
                       'MAX_CONTINUOUS_HRS_WARN', 5)
```




        Block 4 · Per-LE configuration



Per_LE_Parameter_Values.xlsxExcel



            | Parameter | SG | HK | IN |


              | SCHEDULE_END_HOUR | 18 | 17 | 18.5 |

              | MAX_CONT_HRS_ERR | 5 | 6 | 5 |

              | MAX_CONT_HRS_WARN | 4.5 | 5 | 4.5 |







Same formula. Three rules. Three sets of values. No source change needed.





Diagram for this annotation · Three concepts together




Part 1 · Two categories of values — what to hardcode vs what to parameterise







HARDCODED · shared across rollout




Examples in this formula:


p_break_type = 'Meal Break'


p_reg_type   = 'Regular Hours'


**Why hardcode is correct here:**


These labels come from OTL's timecard layout, which is identical across every entity.








RULE-DRIVEN · varies per LE




Examples in this formula:


p_max_cont_err = get_rvalue_number(...)


p_sched_start  = get_rvalue_number(...)


**Why parameterise here:**


Legal thresholds vary per entity. Must be tunable per LE without touching source.










Part 2 · Same formula source, three legal entities, three behaviours




            ONE FORMULA SOURCE: XX_TER_CONTINUOUS_HOURS_VALIDATION

              IF (contHrs > p_max_cont_err) THEN flag




↓ ↓ ↓







ENTITY A · RULE




Statutory 5h cap


MAX_CONT_ERR = 5


Worker flagged at 5h








ENTITY B · RULE




Self-imposed 6h policy


MAX_CONT_ERR = 6


Worker flagged at 6h








ENTITY C · SUB-RULES




Multiple rules, not IF/ELSIF


R1:5 / R2:6 / R3:6


One rule per region








**No source code change between entities.** Configuration scales; conditional code does not.




Part 3 · The fallback argument — safety net, not production default




            get_rvalue_number(rule_id, 'MAX_CONTINUOUS_HRS_ERR', 6)



↑ FALLBACK · the third arg







✓ Rule configured properly


Returns the configured value (e.g. 5 for Entity A). Fallback never used. *This is normal.*






✗ Rule mis-configured / parameter missing


Returns 6. Formula keeps running, doesn't crash. *This means a configuration gap to fix.*









            Hardcode shared layout. Parameterise per-LE variation. One source, many entities.












1The formula's settings page



              - This block is where the formula declares everything that varies across runs — the values it needs but doesn't want to hardcode. Think of it as the settings page for the formula.

              - Crucially, the values fall into **two distinct categories**, and the difference matters for the formula's portability across legal entities.

              - **Hardcoded values** are written directly into the source: time-type names like `'Meal Break'` and `'Regular Hours'`. These match the labels in the OTL timecard layout, which is shared across every entity in the rollout. Hardcoding them is correct because they genuinely don't vary.

              - **Rule-driven values** come from `get_rvalue_number`, which reads from the rule's parameter configuration: schedule start hour, schedule end hour, continuous-work caps. These values change per legal entity, so they must be tunable without touching the formula source.








2Why this separation makes the formula multi-entity



              - The principle: **parameterise per-LE variation; hardcode shared layout.** Get this distinction right and one formula source serves the entire rollout. Get it wrong and you're maintaining one formula per legal entity, with bug-fixes to apply N times.

              - Consider an entity whose local labour law caps continuous work at 5 hours. Its rule sets `MAX_CONTINUOUS_HRS_ERR = 5`, and the formula honours that limit for those workers automatically.

              - Another entity might have no statutory cap; the employer self-imposes 6 hours as company policy. Its rule sets the parameter to 6 and the same formula behaves differently for those workers, without a single line of source change.

              - A third entity might have nuance: a labour code that varies by region or sub-jurisdiction. The architectural answer is multiple rules, one per sub-jurisdiction, each parameterised independently — never an `IF region = 'A' THEN ... ELSIF region = 'B' THEN ... ELSIF` chain inside the formula. Configuration scales; conditional code doesn't.








3The fallback argument explained


The third argumentget_rvalue_number(rule_id, 'MAX_CONTINUOUS_HRS_ERR', 6)
                                                          ↑
                                                       fallback



              - The third argument to `get_rvalue_number` is the fallback value — what the formula uses if the parameter wasn't configured on the rule attached to the worker's processing profile.

              - The fallback exists as a safety net, not as the production default. Pick a defensible number (here, 6 reflects the most permissive cap in the rollout) so that an accidentally unconfigured rule doesn't break submission entirely — the formula still runs, just with a generic threshold.

              - But **never rely on the fallback in production**. Always set the parameter explicitly on every LE rule, with the value the legal team has signed off on. The fallback is your last line of defence against a configuration mistake, not a substitute for proper setup.

              - A useful sanity check during go-live: query the rule configuration for every LE that should be active and confirm the threshold values match your rollout plan. If any LE shows the fallback value, that's a configuration gap.






Hardcode what's shared (layout-driven names). Parameterise what varies (legal thresholds and schedule bounds). One formula source, one rule per legal entity, configuration that scales. Hardcoding a numeric threshold locks the formula to one entity and is the most common architectural mistake in TER design.













```
  OUT_MSG = EMPTY_TEXT_NUMBER

  wMaAry = HWM_CTXARY_RECORD_POSITIONS.count
  rLog = add_rlog(ffs_id, rule_id,
                  '>>> Start bulk wMaAry=' || TO_CHAR(wMaAry))

  cntr = 0
  nidx = 0

  /* day buffer — per-day lifetime */
  dayStarts = EMPTY_DATE_NUMBER
  dayStops  = EMPTY_DATE_NUMBER
  dayIdxs   = EMPTY_NUMBER_NUMBER
  dayCnt    = 0

  /* stretch tracker — per-stretch lifetime */
  stretchStart = NullDate
  stretchEnd   = NullDate
  inStretch    = 'N'

  l_meal_taken = 'N'

  WHILE (cntr  wMaAry) LOOP (
    cntr = cntr + 1
    /* per-line reset only */
    aiTimeType  = NullText
    aiStartTime = NullDate
    ...
```




        Block 5 · Three lifetimes




Diagram for this annotation · Three lifetimes coexist in one block




Part 1 · Three groups of variables, three different reset triggers







PER-ROW SCRATCH




Variables:


aiTimeType
aiStartTime, aiStopTime
aiRecPos, aiMeasure
l_qty_only


Reset trigger:


Every iteration of WHILE loop


at the top, before reading row








PER-DAY STATE




Variables:


dayStarts, dayStops
dayIdxs, dayCnt
stretchStart, stretchEnd
inStretch, l_meal_taken


Reset trigger:


END_DAY marker (Block 7)


stretch also resets on Meal Break








FORMULA-WIDE




Variables:


OUT_MSG
cntr, nidx
wMaAry


Reset trigger:


Never reset after init


persist until formula returns










Part 2 · Timeline view — when each group resets through Sarah's submission






            | Iter:
                | [1] HEADER
                | [2] Reg
                | [3] Reg
                | [4] Meal
                | [5] END_DAY
                | [6] Reg
                | [7] END_PERIOD
                |
              |




                | Row:
                | R
                | R
                | R
                | R
                | R
                | R
                | R
                | every iter
              |


                | Day:
                | ·
                | ·
                | ·
                | ·
                | R
                | ·
                | ·
                | at END_DAY
              |


                | F:
                | ·
                | ·
                | ·
                | ·
                | ·
                | ·
                | ·
                | never
              |







Legend: **R** = reset happens here. Each row's pattern shows the cadence for that group's variables.




Part 3 · What goes wrong if you reset the wrong group





THE BUG: forgetting to reset per-row variables between iterations




Scenario:


Iteration 4 reads a Reg Hours row and sets `aiTimeType = 'Regular Hours'`.


Iteration 5 hits a HEADER row that has *no* time type.


The read in iteration 5 doesn't overwrite `aiTimeType`...



                // iteration 5, HEADER row read:

                IF (PayrollTimeType.exists(5)) THEN aiTimeType = ... // skipped, no value



Result: aiTimeType STILL holds 'Regular Hours' from iteration 4.


Downstream checks evaluate against stale data and silently produce wrong results.


No crash. No error. Just wrong validation, hard to trace.








Part 4 · The fix — reset per-row scratch at the loop top




            aiTimeType = NullText; aiStartTime = NullDate; aiStopTime = NullDate; l_qty_only = 'N'



Reset only per-row scratch. Day-level state stays alive across iterations — that's intentional.











1Initialising the output array


OUT_MSG = EMPTY_TEXT_NUMBER



              - `OUT_MSG` is the formula's return value — a sparse array indexed by timecard row number, where each populated slot becomes a red error marker on the worker's screen.

              - Initialising it as `EMPTY_TEXT_NUMBER` means the array exists but holds no entries. Validation logic later in the loop only writes to slots where it finds problems — clean rows never get a slot at all.

              - This **sparse output pattern** is intentional. A dense array (one entry per row, with empty strings for clean rows) would force the framework to walk every slot looking for messages. The sparse array lets the framework iterate only over flagged rows, which is faster and cleaner.

              - The formula doesn't explicitly return `OUT_MSG` at the bottom — Fast Formula returns it implicitly because it's declared as the output of this formula type. The framework reads whatever's in `OUT_MSG` at the moment the formula completes.








2Measuring the input and announcing the run


wMaAry = HWM_CTXARY_RECORD_POSITIONS.count
rLog   = add_rlog(..., '>>> Start bulk wMaAry=' || TO_CHAR(wMaAry))



              - `.count` on a Fast Formula array returns the number of populated slots. `wMaAry` is short for "while-max-array" — the upper bound for the WHILE loop. Without this, the loop wouldn't know when to stop.

              - The framework guarantees `RECORD_POSITIONS` is populated for every row the worker has on their timecard, including marker rows. So `RECORD_POSITIONS.count` reliably gives the total row count for any timecard.

              - The "Start bulk" log line is more useful than it looks. In production, this is the line that confirms *the formula actually received data and how much*. If a worker reports a problem and the log shows `wMaAry = 0`, you immediately know the timecard arrived empty — the bug isn't in your validation logic, it's upstream.

              - The `>>>` prefix is a grep-friendly convention. Filtering production logs for entry/exit lines becomes a one-second task.








3Why two counters, not one


cntr = 0   // drives loop termination
nidx = 0   // indexes into input arrays



              - In this version of the formula, `cntr` and `nidx` always advance together — both increment by 1 every iteration. So why have two?

              - The reason is intent-based separation. `cntr` describes *"how many iterations have I completed?"* — it drives loop termination. `nidx` describes *"which row am I currently reading?"* — it's an index into the input arrays.

              - Today these are the same number, but they encode different ideas. Future enhancements that add skip-ahead logic (for example, processing a HEADER row's children together as a unit) would advance `nidx` without advancing `cntr`, or vice versa. Maintaining the distinction now leaves room for those changes without restructuring the loop.

              - This is a small example of writing code that documents its own intent. The variables are named for what they *mean*, not what they *do* — and the naming pays dividends when the code evolves.








4The day buffer — per-day lifetime


dayStarts = EMPTY_DATE_NUMBER
dayStops  = EMPTY_DATE_NUMBER
dayIdxs   = EMPTY_NUMBER_NUMBER
dayCnt    = 0



              - The day buffer is a holding area for Regular Hours entries within a single day. As the loop encounters real Reg Hours rows, it appends each one's start time, stop time, and original row index to these three parallel arrays.

              - The buffer accumulates across iterations until the loop hits an `END_DAY` marker. At that point, Block 7 takes over: it tests every pair of buffered entries for time overlap, fires errors on conflicts, and clears the buffer for the next day.

              - **`dayIdxs` is the architectural insight in this group.** The buffer's internal indexing is sequential (1, 2, 3...) but those indexes don't match the worker's view. On a real timecard, the same Reg Hours entries might appear at row positions [2], [4], and [7] — with markers and other time types in between.

              - Without `dayIdxs`, when the overlap test detects a conflict between buffer entries 2 and 3, the formula would have no way to translate that back into the worker's row numbers. Errors would land on the wrong rows, confusing the worker. `dayIdxs` is the chain of custody that connects buffer indexes to original timecard indexes.








5The stretch tracker — per-stretch lifetime


stretchStart = NullDate
stretchEnd   = NullDate
inStretch    = 'N'



              - The stretch tracker measures the longest unbroken run of Regular Hours work, used by Block 8 to enforce the continuous-work cap (legally typically 5 or 6 hours).

              - Unlike the day buffer, the stretch tracker has a **different reset trigger**. It resets when one of two things happens: the worker takes a meal break (proving continuous work was interrupted) or the day ends.

              - This dual-reset behaviour mirrors the legal definition. The cap measures uninterrupted work; eating interrupts it; the next stretch is a fresh start. Resetting only at end-of-day would miss the meal-break case and produce a falsely-too-large stretch value.

              - The three variables work as a unit: `inStretch` is the on/off switch ('Y' means a stretch is currently active), and `stretchStart`/`stretchEnd` hold the start and end times of that stretch. When all three reset, the tracker is off and waiting for the next qualifying entry.








6The day-level meal flag


l_meal_taken = 'N'



              - This single-character flag has outsized importance. It tracks whether the worker has logged a meal break *at any point during the current day*.

              - When Block 6 detects a meal break, it flips this flag to `'Y'`. Block 8's continuous-hours gate checks this flag; if it's `'Y'`, the gate stays closed and the stretch tracker silently stops counting for the rest of the day.

              - The reasoning is legal: the cap measures continuous work *before a meal*. Once the meal happens, the worker has interrupted the run that mattered for compliance. Continuing to track stretches afterward would generate noise without legal meaning.

              - The flag resets at every `END_DAY` so each new day starts fresh — tomorrow's tracking is independent of today's meal status.








7The per-row reset inside the loop


WHILE (cntr

  Block 6 Routing Tree — What happens to each row
  Two questions. Five outcomes. Every iteration ends in exactly one path.



  Read row [nidx]
  into local vars (ai*)


  - aiRecPos
  empty?



  no — marker


  PATH 1 · MARKER ROW
  If END_DAY/END_PERIOD →
  trigger Block 7



  yes — real entry



  aiTimeType
  = ?



  Reg Hours,
  qty-only


  PATH 2 · QTY-ONLY
  Flag immediately:
  "real punches required"



  Reg Hours,
  real punches


  PATH 3 · REG HOURS
  Add to day buffer (Block 7)
  + feed stretch tracker (Block 8)



  Meal Break


  PATH 4 · MEAL BREAK
  Schedule-window check
  + flip l_meal_taken = 'Y'



  Other
  (Annual Leave, Sick, ...)


  PATH 5 · SKIP
  No validation, continue loop








Five paths, each with clear next-steps. Path 1 (markers) routes to Block 7 for day-boundary work. Paths 2 and 4 fire flags directly inside Block 6. Path 3 (the most common) feeds the day buffer and the state machine. Path 5 is the silent default for time types this formula doesn't validate.


  Practitioner's tip
  Path 5 is where most TER scope-creep comes from. A client says "we also need to validate Annual Leave is at least 0.5 days" and the developer's reflex is to add a fifth or sixth time-type branch to Block 6. **Resist this.** Each new path adds complexity and obscures the existing logic. If you have multiple validation domains, write multiple TER formulas and attach them via separate rules — OTL supports this cleanly. Keep each formula's routing tree small enough to fit on one diagram.


#### The annotated code


With the routing tree in mind, here's the actual code, annotated block by block:



    Block 6 · Per-line processing
    Annotated





```
/* read this row's data into local variables */
IF (RECORD_POSITIONS.exists(nidx)) THEN
  aiRecPos = RECORD_POSITIONS[nidx]
IF (PayrollTimeType.exists(nidx)) THEN
  aiTimeType = PayrollTimeType[nidx]
IF (StartTime.exists(nidx)) THEN
  aiStartTime = StartTime[nidx]
IF (StopTime.exists(nidx)) THEN
  aiStopTime = StopTime[nidx]
```


        Block 6a · Defensive reads


          Diagram for this annotation · Three concepts together


          Part 1 · What the .exists() guard is protecting against



              NAIVE READ — CRASHES

                Code:
                aiStartTime = StartTime[1]
                [1] is HEADER — no value:
                ✗ FF doesn't return null✗ FF throws an exception✗ Submission lost
                Worker must re-enter everything



              GUARDED READ — SAFE

                Code:
                IF (StartTime.exists(1)) THEN  aiStartTime = StartTime[1]
                [1] is HEADER — no value:
                ✓ .exists(1) returns FALSE✓ Read is skipped✓ aiStartTime keeps sentinel





          Part 2 · Why both DEFAULT FOR and .exists() — two layers, two failure modes




                LAYER 1
                DEFAULT FOR
                at INPUTS ARE level


                Protects against:
                The whole array variable being unbound or empty.
                Without this, the formula can't even start.







                LAYER 2
                .exists(idx)
                at per-slot level


                Protects against:
                Individual slots being absent within a valid array.
                The array is bound; this index just isn't populated.




          **Belt and braces:** in code that gates payroll, redundancy is a feature. Both layers are cheap; both are non-negotiable.


          Part 3 · The ai* naming convention — snapshot pattern



              FRAMEWORK INPUT
              StartTime[nidx]
              read once

            →

              LOCAL SNAPSHOT
              aiStartTime
              "array input"

            →

              REST OF ITERATION
              Block 6b/c/d/e, Block 7, Block 8
              all reference aiStartTime, never StartTime




            **Why copy? Three reasons:**
            • **Consistent snapshot** — rest of iteration sees one value, not whatever the array might be next time
            • **Single source of update** — if framework input changes, only the read block needs editing
            • **Code review signal** — `ai*` on the left of an assignment instantly tells reader "this is per-row data"






            1What the guard is protecting against

              Recall the input shape from Block 1: the framework hands the formula six parallel arrays, but not every row populates every array. Marker rows (HEADER, END_DAY, END_PERIOD) only carry a value in `RECORD_POSITIONS`. Their slots in `StartTime`, `StopTime`, `PayrollTimeType`, and `measure` are simply absent.

              - If the formula naively reads `StartTime[nidx]` when `nidx` points at a marker row, it's asking for data that isn't there. **Fast Formula doesn't return null in that case — it throws.** The submission fails with an unhandled exception, and you've lost the worker's timecard.

              - The `.exists(nidx)` method is the safe-read pattern. It asks *"does this array actually have a value at this index?"* as a boolean. If yes, read; if no, skip the read entirely and let the local variable keep its previously-reset value (which Block 5's per-row reset just made into a clean sentinel).

              - Notice every input read in this block follows the same pattern: check first, then read. There's no shortcut path that skips the check — the discipline is total because the cost of forgetting it is total (a crashed run).








2Why both DEFAULT FOR and .exists()



              - Block 1's `DEFAULT FOR` declarations and these `.exists()` checks might seem redundant — both protect against the same problem. But they operate at different levels of the stack and catch different failure modes.

              - **DEFAULT FOR** protects against the array variable itself being unbound or empty at runtime. Without it, the formula can't even start the loop — the framework can't bind the input.

              - **.exists()** protects against individual slots being unpopulated within an otherwise valid array. The array is bound and has some data; this particular index just isn't one of them.

              - Belt and braces. In safety-critical code paths — and validation that gates payroll qualifies — redundancy is a feature, not a bug. The runtime cost is negligible; the safety benefit is total.








3The "ai" naming convention and why it matters



              - The variables that receive the read values use an `ai` prefix — `aiRecPos`, `aiTimeType`, `aiStartTime`, `aiStopTime`. The prefix stands for **"array input"**, signalling at a glance that these are local copies of input array values for the current iteration.

              - Why copy at all? Why not just read directly from the input arrays everywhere? Because copying creates a **consistent snapshot**. Once the read block finishes, the rest of the iteration uses these local variables. If anywhere later in the loop body something tweaks the read pattern (or someone refactors), there's a single place to update — the read block at the top of the iteration — not 30 scattered references.

              - The convention also reads well in code review. Seeing `ai*` on the left of an assignment in the read block is one signal; using those same locals everywhere else carries that signal forward. The naming makes the data flow obvious.

              - If the framework's input array structure ever changes (a future OTL release renames or restructures something), only this read block needs updating. The downstream code, already working in terms of `ai*` locals, doesn't need to know.






Every input array read in this formula is wrapped in `.exists()`, and every read populates a local `ai*` variable rather than working directly off the input. Two patterns; both contribute to robustness. Forget the guard on even one read and the next marker row crashes the submission — and marker rows are guaranteed to appear in any production timecard.













```
/* qty-only detection — placeholder vs real punch */
IF (aiTimeType = p_reg_type
    AND aiStartTime <> NullDate
    AND aiStopTime <> NullDate) THEN
( l_st_hr = TO_NUMBER(TO_CHAR(aiStartTime, 'HH24'))
            + TO_NUMBER(TO_CHAR(aiStartTime, 'MI'))/60
  l_sp_hr = TO_NUMBER(TO_CHAR(aiStopTime,  'HH24'))
            + TO_NUMBER(TO_CHAR(aiStopTime,  'MI'))/60
  IF (l_st_hr  0.01 AND l_sp_hr > 23.9) THEN
  ( l_qty_only = 'Y' )
)
```




        Block 6b · Pattern match




Diagram for this annotation · Four concepts together




Part 1 · The two data shapes — same hours, different reality







REAL PUNCH (clean shape)




Worker entered:


Reg Hours · 09:00 → 17:00 · 8h


✓ Specific work at specific times


Real interval. Goes to overlap test, stretch tracker.








QTY-ONLY (placeholder shape)




Worker entered:


Reg Hours · 8h (no times)


✗ Layout fills 00:00 → 23:59


Fake interval. Hides overlaps from later blocks.










Part 2 · The fractional-hour conversion trick




            l_st_hr = TO_NUMBER(TO_CHAR(t,'HH24')) + TO_NUMBER(TO_CHAR(t,'MI'))/60







09:30


becomes **9.5**






17:45


becomes **17.75**






00:00


becomes **0.0**






Single decimal number means a single comparison can detect the qty-only pattern.




Part 3 · Why *0.01* and *23.9*, not exactly 0 and 24




            What *should* be 0.0 after TO_NUMBER conversion can end up as 0.0000003 due to IEEE 754 floating-point drift. Strict equality `l_st_hr = 0` would silently fail.




            IF (l_st_hr  23.9) THEN l_qty_only = 'Y'




            Buffer windows: anything from `00:00:00` to `~00:00:36` reads as "near zero"; anything from `23:54` onward reads as "near end". Wide enough to absorb drift, narrow enough that no real punch can fall there.





Part 4 · What happens after the flag — one detector, three consumers





Detector


l_qty_only = 'Y'


single-char flag, set once









CONSUMER 1


Block 6c


Fires error: *"real punches required"*. Treats qty-only as missing punch.






CONSUMER 2


Block 6d


Excludes from day buffer. No fake interval in overlap test.






CONSUMER 3


Block 8


Excludes from stretch tracker. Don't count placeholder hours.






One detector decides; three consumers respond. Each block stays focused on its own logic.











1The data shape this block exists to detect



              - OTL's timecard layout typically allows two ways to log Regular Hours. The clean way is to enter explicit punch times: start at 09:00, stop at 17:30. The shortcut way is to enter just a quantity — "8 hours" — and let the system figure out the rest.

              - The system can't really figure out the rest, of course. It needs *something* in the StartTime and StopTime fields because the database column is non-null. So OTL writes a default range: start `00:00` (very beginning of day), stop `23:59` (very end of day).

              - The end result is a row that *looks* like a 24-hour shift but isn't. The hours value (8) is correct; the punch times are decorative. The formula needs to recognise this shape because qty-only entries shouldn't be treated as real work intervals — they don't represent specific work happening at specific times.

              - Without detection, the formula would put a 24-hour interval into the day buffer, which would falsely overlap with every other entry on the day. Cascading errors would flag rows that aren't actually wrong.








2The fractional-hour conversion


l_st_hr = TO_NUMBER(TO_CHAR(t,'HH24')) + TO_NUMBER(TO_CHAR(t,'MI'))/60



              - Times in Fast Formula are stored as Oracle dates, which are awkward to compare directly. The trick is to extract the time-of-day as a single decimal number representing hours-since-midnight.

              - `TO_CHAR(t, 'HH24')` pulls out the hour (0–23), and `TO_CHAR(t, 'MI')` pulls out the minutes (0–59). Dividing minutes by 60 converts them into the fractional part of an hour. Add the two together and you get a single number: `09:30` becomes `9.5`, `17:45` becomes `17.75`, `00:00` becomes `0.0`.

              - This makes the qty-only check a single comparison: *"is start near zero AND is stop near 24?"* Without this conversion, you'd need to compare hours and minutes separately and combine the results — verbose and error-prone.

              - The pattern is reusable elsewhere too. Block 8's continuous-hours calculation uses a similar approach (with the addition of Julian Day arithmetic for cross-midnight handling).








3Why 0.01 and 23.9 instead of exactly 0 and 24



              - The intuition might say to test `l_st_hr = 0 AND l_sp_hr = 23.9833` for an exact match against the qty-only pattern. The intuition is wrong, because computers don't store decimals perfectly.

              - This is IEEE 754 floating-point representation, the same maths that means `0.1 + 0.2` equals `0.30000000000000004` in most languages. A value that should be `0.0` can end up as `0.0000003` due to representation drift through TO_NUMBER conversion.

              - The buffers `0.01` and `23.9` absorb that imprecision. Anything from `00:00:00.000` to roughly `00:00:36` reads as start "near zero"; anything from `23:54` onward reads as stop "near end". Real timecards never enter punches in those windows because layouts don't permit it.

              - The chosen buffers are wide enough to absorb floating-point drift but narrow enough that no real punch can ever cross them — eliminating false positives entirely.








4What happens once an entry is flagged qty-only



              - Setting `l_qty_only = 'Y'` doesn't generate an error message by itself — it sets a flag that affects how subsequent blocks treat this row.

              - Block 6c (the RegHours hard requirement) treats qty-only entries the same as missing punches and fires an explicit error so the worker knows real times are needed.

              - Block 6d (the day buffer) excludes qty-only entries from overlap testing — the formula doesn't pretend a placeholder represents real work.

              - Block 8 (the stretch tracker) excludes qty-only entries from continuous-hours counting, for the same reason.

              - The flag is a single character but its effects ripple through the rest of the formula. This is composition working correctly — one detector, multiple consumers.






The pattern `(start  23.9)` reliably distinguishes a qty-only placeholder from a real punch, even with floating-point imprecision. The detection happens once; the flag it sets affects three downstream blocks. Composition like this keeps each block's logic focused while the overall formula stays correct.













```
/* RegHours start/stop missing — flag the row */
IF (aiTimeType = p_reg_type
    AND (aiStartTime = NullDate
         OR aiStopTime = NullDate
         OR l_qty_only = 'Y')) THEN
( OUT_MSG[nidx] =
    get_msg_attribute('StartTime') ||
    get_output_msg('HXT', p_msg_reghrs)
)
```




        Block 6c · Hard requirement




Diagram for this annotation · Three concepts together




Part 1 · The hard requirement — three failure modes, all flagged





Rule:


Every Regular Hours entry must carry **both** a real start time and a real stop time. No exceptions, no warnings — this is a blocker.









FAILURE 1


Missing start time


start = NullDate
stop = 17:00






FAILURE 2


Missing stop time


start = 09:00
stop = NullDate






FAILURE 3


Qty-only (no real punches)


l_qty_only = 'Y'








Part 2 · The message-prefix convention — vague vs targeted errors







WITHOUT PREFIX — vague




OUT_MSG[nidx] = get_output_msg(...)


**✗ Worker sees:**


Generic red marker on row. *"start time required"* — but the worker thinks *"my start time IS filled, what's wrong?"*








WITH PREFIX — targeted




get_msg_attribute('StartTime') || get_output_msg(...)


**✓ Worker sees:**


StartTime column itself lights up red. Eye goes straight to the field. Fix is obvious.










Part 3 · Why Reg Hours and Meal Break have different rules







REG HOURS


Both punches required


Logic: *"I worked from X to Y."* Work has a beginning AND an end. Both endpoints matter for time accounting. **Hard requirement — no exceptions.**






MEAL BREAK


Flexible (Block 6e)


Logic: *"I took a break."* Some companies record only when break starts (event marker rather than interval). Layout decides — **tolerant.**







            **Architectural lesson:** not every time type follows the same validation rules. Resist applying uniform requirements across all rows.












1The rule, stated plainly



              - Every Regular Hours entry must carry **both** a real start time and a real stop time. The formula treats this as a non-negotiable hard requirement — not a warning, not a suggestion, but a blocker that prevents submission.

              - Three failure modes trigger the flag: start time is missing, stop time is missing, or the entry was flagged as qty-only by Block 6b.

              - The qty-only case is interesting because the entry technically *has* punch times — OTL filled them in as 00:00 and 23:59. But the previous block detected those as placeholders, not real punches. From this block's perspective, qty-only is functionally equivalent to "no real punch times" and gets the same treatment.

              - Why is this a hard requirement? Because Regular Hours represents work intervals on the timecard, and intervals need both endpoints to be meaningful. A start time without a stop is "I started working but never finished" — which the formula cannot interpret. Forcing real punches keeps the rest of the validation logic well-defined.








2Telling OTL which column to highlight


OUT_MSG[nidx] = get_msg_attribute('StartTime') || get_output_msg(...)



              - Notice the structure of the assignment to `OUT_MSG`. It's not just the message text — it's a concatenation of `get_msg_attribute('StartTime')` with `get_output_msg(...)`. The first piece is doing something subtle but important.

              - `get_msg_attribute('StartTime')` tells the OTL framework **which timecard column to highlight** when the worker sees this error. The function returns a special prefix string that the UI parses out and uses for visual targeting.

              - Without this prefix, the worker sees a generic red error marker on the row but no indication of which field caused it. They'd have to read the message text and guess: *"the message says 'start time required' — but my start time is filled in, what's wrong?"*

              - With the prefix, the StartTime column itself lights up red on that row. The worker's eye goes straight to the column that needs attention. The fix is obvious; the friction disappears.

              - This is a small UX detail that makes a huge difference in worker experience. Every error message your formula generates should include the field-attribute prefix where it's relevant.








3The asymmetry between Reg Hours and Meal Break



              - This is the **only validation in the entire formula** that demands both start and stop punches. Block 6e's schedule-window check on Meal Break uses different logic that can tolerate just a start time, depending on the layout configuration.

              - The asymmetry mirrors real-life timekeeping. *"I worked from X to Y"* intrinsically needs both endpoints — the work has a beginning and an end, and both matter for accurate time accounting.

              - A meal break is more flexible. Some companies record only when the break starts (treating it as an event marker rather than an interval) and rely on schedule defaults to fill in the duration. Others insist on both. The formula respects whatever the OTL layout has been configured to allow.

              - The architectural lesson: **not every time type follows the same validation rules**. Resist the urge to apply uniform requirements across all types — the rules differ for legitimate reasons, and the formula should reflect that.






When generating an error message, always tell OTL which column to highlight via `get_msg_attribute`. A vague error frustrates the worker; a specific one lets them fix it instantly. And remember that not every time type needs the same validation — Reg Hours demands both punches; Meal Break may not.













```
/* buffer Reg Hours into the day-level buffer */
IF (aiTimeType = p_reg_type
    AND l_qty_only = 'N'
    AND aiStartTime <> NullDate
    AND aiStopTime <> NullDate) THEN
( dayCnt = dayCnt + 1
  dayStarts[dayCnt] = aiStartTime
  dayStops[dayCnt]  = aiStopTime
  dayIdxs[dayCnt]   = nidx
)
```




        Block 6d · Buffer for overlap



Day_Buffer_Accumulating.xlsxExcel



            | Iter | dayCnt | dayStarts[] | dayStops[] |


              | [2] | 1 | 08:30 | 10:00 |

              | [3] | 2 | 08:30, 10:00 | 10:00, 14:45 |

              | [4] | 3 | 08:30, 10:00, 15:00 | 10:00, 14:45, 18:00 |







Each Reg Hours line appends to the parallel arrays. END_DAY triggers pairwise overlap on this buffer.





Diagram for this annotation · Four concepts together




Part 1 · Evidence-gathering — what gets included, what stays out




            // the gate

            IF aiTimeType = p_reg_type AND l_qty_only = 'N'

               AND aiStartTime <> NullDate AND aiStopTime <> NullDate








INCLUDED — goes into buffer




✓ Real Reg Hours rows only


Time type = 'Regular Hours'
Both punches present
Not a qty-only placeholder


These are the rows that compete for the same time








EXCLUDED — deliberately filtered out




✗ Marker rows (HEADER, END_DAY)
✗ Qty-only placeholders
✗ Meal Breaks


If Meal Break went in, it would falsely overlap with adjacent Reg Hours by construction.










Part 2 · Three parallel arrays, all written together




            // dayCnt increments first, then all three writes go to the same slot

            dayCnt = dayCnt + 1; dayStarts[dayCnt]=aiStartTime; dayStops[dayCnt]=aiStopTime; dayIdxs[dayCnt]=nidx








dayStarts[ ]



                slot 1: 08:30

                slot 2: 10:00

                slot 3: 15:00







dayStops[ ]



                slot 1: 10:00

                slot 2: 14:45

                slot 3: 18:00







dayIdxs[ ] · chain of custody



                slot 1: [2] *← original*

                slot 2: [4] *← original*

                slot 3: [7] *← original*







All three arrays use the same internal indexing (1, 2, 3...). Three writes per row. Always in lockstep.




Part 3 · Why dayIdxs matters — buffer index ≠ timecard row





Buffer indexing (sequential, 1, 2, 3):




1


2


3


via dayIdxs[]




↓ ↓ ↓


Worker's actual timecard rows:




[2]


[4]


[7]


positions 3, 5, 6 are markers/meal — not in buffer








            Without dayIdxs: Block 7 detects buffer entries 2 & 3 overlap, but it would put the error on rows [2] and [3]:

            **✗ Worker baffled. Wrong rows highlighted. Bug impossible to debug.**

            **✓ With dayIdxs: error correctly lands on rows [4] and [7] — matches what the worker entered.**





Part 4 · Per-day lifecycle — accumulate, judge, reset





Accumulate


→


END_DAY hits → Block 7


→


Pairwise overlap test


→


Reset to empty













1The role this block plays



              - This block doesn't fire any errors itself. Its job is to **collect evidence** for the overlap test that will fire later in Block 7. Think of it as evidence-gathering before a trial — the actual judgment happens elsewhere.

              - What gets collected: every *real* Regular Hours entry. The qualifier "real" is doing important work here. The block deliberately excludes anything that shouldn't participate in overlap testing — marker rows (HEADER, END_DAY), qty-only placeholders (which don't represent real time intervals), and Meal Breaks (which have their own validation path in Block 6e).

              - What stays excluded matters as much as what gets included. If Meal Breaks went into the day buffer, they'd overlap with their adjacent Reg Hours rows by construction (a 12:00–13:00 lunch overlaps with the 09:00–12:00 morning shift if you treat it as just another interval). The formula would generate noise instead of signal.

              - This selective collection is a small architectural decision with large consequences. It's the difference between a formula that works correctly on real data and one that fires constantly false flags.








2The three parallel arrays, in detail


dayStarts[dayCnt] = aiStartTime
dayStops[dayCnt]  = aiStopTime
dayIdxs[dayCnt]   = nidx



              - Each qualifying entry adds three items in lockstep: a start time, a stop time, and a row index. `dayCnt` increments first so all three writes go to the same new slot.

              - `dayStarts` and `dayStops` together describe the time interval for each entry. These are what the overlap test in Block 7 actually compares pairwise to detect collisions.

              - `dayIdxs` is the metadata that ties each buffered entry back to its original timecard row. Block 7 uses this to identify *which* row to flag when an overlap is detected.

              - Storing these as three parallel arrays (rather than one array of records) is a Fast Formula idiom — the language doesn't have native record types, so parallel arrays serve the same purpose. The three arrays must always be kept in sync (same length, same indexing), which is why every append updates all three at once.








3The crucial role of dayIdxs



              - Why bother storing the original row index at all? Couldn't the formula just use the buffer's internal indexing? The answer is no, and the reason reveals a subtle aspect of the formula's correctness.

              - The buffer's internal indexing starts at 1 and increments sequentially as entries are added. So buffer position 1 might be the day's first Reg Hours entry, position 2 the second, and so on.

              - But the worker's view of the timecard is different. On a real timecard, those Reg Hours entries might appear at row positions [2], [4], and [7] — with marker rows and Meal Break rows interleaved between them. The buffer indexing (1, 2, 3) and the timecard indexing ([2], [4], [7]) don't match.

              - When Block 7 detects that buffer entries 2 and 3 overlap, it can't just put the error on rows [2] and [3]. It needs to translate buffer indexes back to timecard indexes. `dayIdxs` is that translation table.

              - Without it, error messages would land on the wrong rows. The worker would see *"row 2 overlaps with row 3"* when actually rows [4] and [7] are the conflicting ones — baffling, ungrounded, impossible to debug.








4Lifetime: when the buffer resets



              - The buffer accumulates across iterations as the loop processes more rows of the same day. It doesn't get touched again by this block — further additions just keep extending it.

              - The buffer's life ends at the next `END_DAY` or `END_PERIOD` marker, where Block 7 takes over. Block 7 runs the pairwise overlap test, fires flags on conflicting rows (using `dayIdxs` to target correctly), and then resets all three arrays back to empty.

              - The next day starts with empty lists, ready to accumulate again. The cycle repeats for every day in the timecard period.

              - This **per-day lifecycle** is what keeps the formula correct across multi-day timecards. Without the reset, day 2's overlap test would also see day 1's entries, producing nonsense results.






The day buffer is evidence-gathering for Block 7's overlap trial. The selective inclusion (real Reg Hours only) prevents false flags. `dayIdxs` is the chain of custody that connects the evidence to the right timecard row in the worker's view. Three pieces of metadata, one purpose — correct and actionable error messages.













```
/* Meal Break — schedule window check */
IF (aiTimeType = p_break_type
    AND aiStartTime <> NullDate) THEN
( bk_st = TO_NUMBER(TO_CHAR(aiStartTime, 'HH24'))
  bk_sp = TO_NUMBER(TO_CHAR(aiStopTime,  'HH24'))
  IF ((bk_st  p_sched_start
       OR bk_sp > p_sched_end)
      AND l_day <> 'SAT'
      AND l_day <> 'SUN') THEN
  ( OUT_MSG[nidx] = ... p_msg_break )
  l_meal_taken = 'Y'
)
```




        Block 6e · Schedule window




Diagram for this annotation · Four concepts together




Part 1 · The rule — meal break must fall inside scheduled hours (weekdays only)





SCHEDULE WINDOW · 09:00 — 18:00








7:30


12-13


19-20





              060809111315182022








**✓ Inside (12–13)**
— passes


**✗ After 18 (19–20)**
— flag


**✗ Before 9 (07:30)**
— flag




Weekend exception: validation suspended on Saturday and Sunday.




Part 2 · The operator-precedence trap — AND binds tighter than OR




            // In Fast Formula, AND binds tighter than OR — just like × binds tighter than +

            2 + 3 × 4 = 14, not 20   //   A OR B AND C = A OR (B AND C)






THE BUG — missing parens




IF bk_st  sched_end AND l_day <> 'SAT' AND l_day <> 'SUN'


Parsed as: `(start-too-early) OR (stop-too-late AND weekday)`


✗ Saturday 07:30 break: first OR clause TRUE → OR short-circuits → weekend never checked → FALSE FLAG








Part 3 · The fix — one pair of parentheses around the OR





THE FIX — explicit grouping




IF (bk_st  sched_end) AND l_day <> 'SAT' AND l_day <> 'SUN'


Now reads as: `(out-of-window) AND weekday`


✓ Saturday 07:30: out-of-window TRUE, weekday FALSE → AND short-circuits → no flag → CORRECT






**General rule:** any time you mix AND and OR in the same expression, wrap the OR clause explicitly. Trust nothing to default precedence.




Part 4 · The l_meal_taken side-effect — nervous-system signalling







BLOCK 6e · sets the flag




l_meal_taken = 'Y'


set even if validation failed (worker did eat regardless)






→




BLOCK 8 · reads the flag




if l_meal_taken='Y' →


gate stays closed


stretch tracker stops counting






→




BLOCK 7c




l_meal_taken = 'N'


resets at day boundary — tomorrow starts fresh










            **Why set the flag even on validation failure?** The worker did eat — even if they entered the wrong time. Treating an invalid meal as "didn't happen" would let the stretch tracker keep counting past lunch, generating cascading false errors.



Cross-block coordination via shared flags. Each block does its own job; the flags are the connective tissue.











1The validation this block enforces



              - This block handles meal break entries with one rule: **a meal break should fall within scheduled working hours**. The schedule is defined by the rule parameters `p_sched_start` (typically 9) and `p_sched_end` (typically 18).

              - Examples that fail: a meal logged at 19:00–20:00 (after the 18:00 schedule end), a meal at 07:30–08:00 (before the 09:00 schedule start), a meal at 22:00–23:00 (well outside any normal workday).

              - Why does this rule matter? Two reasons. First, a meal outside working hours strongly suggests the worker mis-entered the time — perhaps they meant 12:00–13:00 instead of 19:00–20:00. Second, a meal break that doesn't interrupt actual work doesn't satisfy the legal purpose of the meal break (giving the worker rest during their shift).

              - The validation is suspended on weekends. If the worker is logging hours on Saturday, the schedule-window check doesn't apply — weekend work has its own logic and shouldn't be falsely blocked by weekday assumptions.








2The operator-precedence trap that catches everyone



              - Fast Formula evaluates logical operators in a specific order: `AND` binds tighter than `OR`. This mirrors how multiplication binds tighter than addition in arithmetic — `2 + 3 × 4` equals 14, not 20.

              - Apply that to a logical expression. `bkStart  sched_end AND l_day <> 'SAT' AND l_day <> 'SUN'` — without parentheses — gets parsed as *"start-too-early OR (stop-too-late AND weekday)"*.

              - Now picture a Saturday morning early break: a worker logs `07:30–08:00` on a Saturday. The first condition (`bkStart 3The fix is one pair of parentheses


IF (bk_st  p_sched_end)
   AND l_day <> 'SAT' AND l_day <> 'SUN' THEN ...



              - Wrapping `(bkStart  sched_end)` in parentheses forces the OR to evaluate first. Now the expression reads as *"(out-of-window) AND weekday"*.

              - The Saturday morning early break: the inner OR fires TRUE, but the outer AND requires the weekend exception to also be true. `l_day = 'SAT'`, so the weekend guard fails, the AND short-circuits, and no flag fires. Correct behaviour.

              - The fix is two characters added to the source. The bug it prevents would have been buried, hard to reproduce, and might survive several rounds of UAT before someone tested a Saturday timecard.

              - The general lesson: **any time your formula mixes `AND` and `OR` in the same expression, wrap the OR clause in explicit parentheses**. Don't trust default precedence to match your intent. The parens cost nothing; missing them costs production bugs.








4The l_meal_taken side-effect



              - The very last line in this block is `l_meal_taken = 'Y'`. It's tucked away after the schedule check, easy to overlook, but it has consequences that reach across the formula.

              - Block 8 (the continuous-hours state machine) checks this flag at the top of its gate. If `l_meal_taken = 'Y'`, the gate stays closed and the stretch tracker stops counting for the rest of the day.

              - The reasoning is legal: the continuous-work cap measures work *before* a meal break. The meal itself proves continuity was interrupted. Any work after the meal is fresh and doesn't accumulate against the pre-meal stretch.

              - Notice that the flag is set *regardless of whether the meal break passed validation*. Even a meal logged outside hours flips the flag — the formula trusts that the worker did eat, even if they entered the time wrong, because the alternative (treating an invalid meal as if it didn't happen) would generate cascading errors.

              - This kind of cross-block coordination is why the formula has so many shared state variables. Each block does its own job, but they coordinate through shared flags like `l_meal_taken`, `l_qty_only`, and `inStretch`. The flags are the formula's nervous system.






One pair of parentheses is the difference between the formula working on weekends and falsely flagging legitimate weekend entries. The general rule: any time you mix `AND` and `OR` in a single condition, wrap the OR clause explicitly. Trust nothing to default precedence.












### Day Boundary & Pairwise Overlap


Block 7 is the only block in the formula that runs *conditionally*. While Blocks 6 and 8 fire on every iteration, Block 7 only activates when the loop hits an `END_DAY` or `END_PERIOD` marker. That's a deliberate design choice with a real performance benefit: overlap detection is an O(n²) operation, and running it on every row would scale badly for workers with 30+ entries per timecard. By batching the work to fire once per day, we keep the cost bounded.


#### The sequence: what fires when END_DAY hits


When the loop reaches an END_DAY marker, five things happen in order. The buffer that's been quietly filling up across previous iterations gets read, tested, and cleared.


  Block 7 — What happens when END_DAY fires
  Top to bottom, in order. The buffer fills earlier; it gets consumed here.




  1
  TRIGGER
  Loop reads a row where
  RECORD_POSITIONS = 'END_DAY'


  - 2
  READ THE BUFFER
  The day buffer holds every Reg Hours entry
  from earlier iterations — e.g.
  3 entries from Sarah's day: rows [2], [3], [5]






  3
  TEST EVERY PAIR
  Compare each pair of entries (i, j):
  starts[j]  starts[i]?
  if true → entries overlap (continue to step 4)


  if overlap




  4
  FLAG THE LATER ENTRY
  Write to OUT_MSG so the worker sees it:
  OUT_MSG[dayIdxs[j]] = "Overlapping entries"






  5
  RESET DAY STATE
  Clear the buffer, reset the stretch tracker,
  set l_meal_taken = 'N'. Tomorrow starts clean.


  Loop continues to the next row.








Three things worth holding on to:


  **The buffer fills earlier, drains here.** Block 6d adds entries to the buffer on every Reg Hours row. Block 7 just consumes what Block 6d collected.

  - **Use strict `Block 7 · Pairwise overlap test
    Annotated









```
/* fire on day or period boundary */
IF (aiRecPos = 'END_DAY'
    OR aiRecPos = 'END_PERIOD') THEN
(
  i = 1
  WHILE (i  dayCnt) LOOP
  ( j = i + 1
    WHILE (j  dayCnt) LOOP
    (
      ...
```




        Block 7a · Trigger on marker




Diagram for this annotation · Three concepts together




Part 1 · The trigger gates everything — only fires at day or period boundary









[1] HEADER


silent






[2] Reg


silent






[3] Reg


silent






[4] Meal


silent






[5] END_DAY


FIRES ⚡






[6] Reg


silent






[7] END_PERIOD


FIRES ⚡










            Block 6d quietly accumulates entries into the buffer on every Reg Hours iteration.

            Block 7 stays silent until a marker arrives. **Marker = clean checkpoint — every entry has been collected.**





Part 2 · The pairwise loop — every pair tested once, no duplicates



**Buffer has 4 entries (dayCnt = 4):**




A


B


C


D





**Six comparisons fire — in this order:**





i=1 (A):




A vs B


A vs C


A vs D


(j=2,3,4)








i=2 (B):




B vs C


B vs D


(j=3,4) — A vs B done








i=3 (C):




C vs D


(j=4) — others done







Six unique pairs from four entries: `n(n-1)/2 = 4×3/2 = 6`.


If j started at 1, every pair would be tested twice and entries would compare against themselves — false flags everywhere.




Part 3 · The performance reality — pairwise is O(n²)






            | Buffer entries (n)
                | Comparisons
                | Cost (rough)
                | Verdict
              |




                | Typical day: 5
                | 10
                | trivial
                | ✓ comfortably fast
              |


                | Heavy day: 30
                | 435
                | manageable
                | ⚠ still OK
              |


                | Edge case: 100
                | 4,950
                | noticeable
                | ✗ would need attention
              |









            In real production, day buffers rarely exceed 5–10 entries.

            By batching the work to fire **once per day** instead of row-by-row, the cost stays bounded for realistic timecards.





            DESIGN INSIGHT: Marker-driven activation keeps an O(n²) algorithm safe in practice. Same algorithm running per-row would multiply this cost by the number of iterations — unacceptable.












1The trigger condition that gates everything



              - This entire block sits behind a single guard: `IF (aiRecPos = 'END_DAY' OR aiRecPos = 'END_PERIOD') THEN`. Nothing inside fires unless that condition is true.

              - The result is that overlap testing happens **only at day boundaries**, never row-by-row. As the loop processes Reg Hours rows in the middle of a day, Block 6d quietly accumulates them into the day buffer. This block stays silent.

              - Then the loop encounters an `END_DAY` marker. The buffer at this moment holds every Reg Hours entry from the day just completed. Now the block fires — this is the moment of truth, where every pair gets checked against every other pair.

              - Why batch the work this way instead of testing each new entry against existing entries as it arrives? Because the marker-driven approach guarantees every entry has been collected before testing begins. There's no risk of testing entry A against entry B before realising entry C will arrive next and complicate the picture. The day boundary is a clean checkpoint.








2The pairwise loop pattern, walked through


i = 1
WHILE (i  i` is what guarantees every unordered pair is tested exactly once.

              - The progression for a 4-entry buffer: i=1 pairs with j=2,3,4. Then i=2 pairs with j=3,4. Then i=3 pairs with j=4. Six total comparisons, each pair seen once. (1,3) is tested but (3,1) isn't — that would be redundant since overlap is symmetric.

              - The pattern would be wrong if `j` started at 1 instead of `i+1` — that would test every pair twice (once as A,B and once as B,A) and also test entries against themselves (A,A always overlaps trivially), generating false flags.








3The performance reality check



              - The pairwise pattern is **O(n²)** — for n entries, it does n(n−1)/2 comparisons. In computer science, anything quadratic is suspicious because it scales badly: 100 entries means 4,950 comparisons, 1000 entries means 499,500.

              - Should we worry about this here? No, and the reason is the constraint on `n`. The buffer holds Reg Hours entries for *one day only*. A worker logging 10 separate Reg Hours entries on a single day is already unusual. 20 would be extreme. 100 entries on one day doesn't happen on real timecards.

              - Doing the maths at realistic scales: 5 entries → 10 comparisons. 10 entries → 45 comparisons. 20 entries (extremely unusual) → 190 comparisons. All execute in well under a millisecond.

              - This is a case where understanding the data shape matters more than understanding algorithmic complexity. Quadratic is fine when n is bounded by problem constraints — trying to optimise with sorted-interval tricks (sweep-line algorithms, interval trees) would add real complexity for zero measurable gain. Premature optimisation; resist it.






Pairwise comparison is the right pattern when `n` is small by definition (one day's entries). The marker-driven trigger gives a clean checkpoint where every entry has been collected before testing begins. Don't be tempted to optimise for n² here — the problem constraints already keep `n` manageable.













```
      /* the intersection test, once */
      IF (dayStarts[i]  dayStops[j]
          AND dayStarts[j]  dayStops[i]) THEN
      ( flagIdx = dayIdxs[j]
        OUT_MSG[flagIdx] =
            get_msg_attribute('StartTime') ||
            get_output_msg('HXT', p_msg_overlap)
      )
      j = j + 1
    )
    i = i + 1
  )
```




        Block 7b · Strict less-than




Diagram for this annotation · Four concepts together




Part 1 · The interval intersection rule — one test, every case covered




            IF (dayStarts[j]  dayStarts[i]) THEN overlap




            Two intervals overlap if — and only if — each one starts before the other ends. One rule covers every case.





Part 2 · The three cases — overlap, touching, disjoint









CASE A · OVERLAP


✗ Flagged




Entry i: 09:00 → 12:00    Entry j: 11:00 → 14:00


j starts (11:00) before i ends (12:00), j ends (14:00) after i starts (09:00).








CASE B · TOUCHING


✓ Clean




Entry i: 09:00 → 12:00    Entry j: 12:00 → 14:00


Strict `

Part 3 · Why strict `

Part 4 · Which entry gets the flag — always the later one







// j is always > i, so dayIdxs[j] is the entry added more recently


flagIdx = dayIdxs[j]   // the LATER entry — matches worker's mental model





              The pairwise loop uses `i 1The interval intersection rule, derived



              - The fundamental insight powering this entire block fits in one sentence: **two intervals overlap if and only if each one starts before the other ends**. That single rule covers every possible case — touching boundaries, partial overlap, complete containment, disjoint intervals.

              - Why this rule works can be derived geometrically. Place two intervals A and B on a timeline. If they don't overlap, one of two things must be true: A ends before B starts, or B ends before A starts. Equivalently — flipping each — A.start is at-or-after B.stop, or B.start is at-or-after A.stop. Negate both for "they DO overlap": A.start 2A worked example to ground the rule


A: 09:00–12:00     B: 10:00–13:00

A.start 3The single character that decides everything



              - The `4Which entry gets the flag, and why it matters


flagIdx = dayIdxs[j]   // the LATER entry



              - When an overlap is detected, the formula has to choose *which* of the two entries to flag. Both rows are involved in the conflict; only one gets the error message. The choice is not arbitrary.

              - The code uses `dayIdxs[j]` — the later entry in the pair. Recall that `j` always starts past `i`, so when the formula gets here, `j` is the entry that was added to the buffer *after* entry `i`. In other words, `j` is what the worker added more recently.

              - This matches how workers think about their own data. When they see an error, the natural assumption is *"the row I just added is the problem"*, not *"a row I added earlier is suddenly broken"*. Flagging `j` aligns with that mental model.

              - If the formula flagged `i` instead (the earlier entry), the worker would see something deeply unsettling: a row that was fine a moment ago suddenly turning red because of an entry they made later. They'd waste time looking at the flagged row, trying to figure out what's wrong with it — when the actual problem is the new entry that caused the conflict.

              - Choosing the later entry is a small UX detail with a large effect on debuggability. Small decisions in error-messaging compound; respect the user's mental model.






Two intervals overlap if and only if each one starts before the other ends. Strict less-than (`Block 7c · Boundary reset




Diagram for this annotation · Three concepts together




Part 1 · Seven lines, one atomic group — what gets reset, what doesn't




            // runs at every END_DAY / END_PERIOD

            dayStarts    = EMPTY_DATE_NUMBER

            dayStops     = EMPTY_DATE_NUMBER

            dayIdxs      = EMPTY_NUMBER_NUMBER

            dayCnt       = 0 ← clear day buffer (4 lines)

            l_meal_taken = 'N' ← reset the meal flag

            stretchStart = NullDate

            inStretch    = 'N' ← clear stretch tracker (2 lines)


            // OUT_MSG is NOT reset — it must persist across all days, until RETURN





Part 2 · What goes wrong if you forget any one of these resets







FORGET DAY BUFFER




Symptom: false flags


Day 2 entries appended on top of yesterday's leftovers. Pairwise test sees mixed days. 09:00 day-1 falsely overlaps 11:00 day-2 (date ignored).


Over-flag — visible noise








FORGET l_meal_taken




Symptom: NO flags (worst)


Once flag flips 'Y' on day 1, stays 'Y' for entire timecard. Block 8's gate stays closed. Stretch tracker silently dies. Workers exceed legal cap freely.


Under-flag — legally dangerous








FORGET STRETCH TRACKER




Cross-day false flags


Day-1 stretch survives into day 2. Day-2 first entry extends or restarts that ghost. contHrs calculations include yesterday's hours. Falsely 13+h.


Over-flag — wrong metrics








Each missing reset breaks the formula in a different way. None crash. All ship to production silently.




Part 3 · Why this category of bug evades testing







UAT — bug stays dormant



                Test timecards: 1–2 days only

                Single-day data never crosses END_DAY

                Reset code never executes

                **✓ Tests pass — sign-off given**







PRODUCTION — bug fires immediately



                Real timecards: 10–14 days (biweekly)

                END_DAY hits on day 2, then every day

                Missing reset fires on first multi-day

                **✗ Production incident on day 1**










THE DEFENCE — treat the reset block as atomic



              Every day-level state variable declared anywhere in the formula **must** appear in this reset.

              Code review for this block: scan for any per-day state that's missing from the reset list.

              *More careful testing won't catch this. The fix is structural — never edit one line of the reset without considering the others.*














1The reset block, line by line


dayStarts    = EMPTY_DATE_NUMBER
dayStops     = EMPTY_DATE_NUMBER
dayIdxs      = EMPTY_NUMBER_NUMBER
dayCnt       = 0
l_meal_taken = 'N'
stretchStart = NullDate
inStretch    = 'N'



              - This sequence runs immediately after the pairwise overlap test fires (or doesn't). Whatever flags the test produced have already landed in `OUT_MSG`; this block's job is to prepare the formula's state for the next day's data.

              - The first four lines clear the day buffer. Reassigning `dayStarts`, `dayStops`, and `dayIdxs` to their empty array constants discards every entry the buffer accumulated during the day just completed. `dayCnt` resets to zero so the next append-and-increment cycle starts fresh at position 1.

              - The fifth line resets `l_meal_taken` to `'N'`. This flag has been tracking whether the worker logged a meal break today; tomorrow is a new day with a new meal-tracking cycle, so the flag must reset.

              - The last two lines clear the stretch tracker. `stretchStart` goes back to `NullDate` (the sentinel for "no active stretch"), and `inStretch` flips to `'N'` to signal the tracker is currently idle.

              - Notice that `OUT_MSG` is *not* reset here. That array accumulates flags across the entire formula run and persists until the formula returns. Resetting it here would erase every flag generated so far — a catastrophic bug.








2What each missing reset would silently break



              - **Forget the day buffer reset:** Day 1's Reg Hours entries stay in the buffer when day 2 starts. Block 6d on day 2 appends new entries on top of yesterday's leftovers. The pairwise overlap test now sees entries from two different days mixed together. Time intervals from different days can falsely overlap (a 09:00 entry on day 1 conflicts with an 11:00 entry on day 2 if you ignore the date component). Cascading false flags follow, all impossible to debug because the bug is in *state*, not in *logic*.

              - **Forget `l_meal_taken`:** Once the worker logs a meal on day 1, this flag flips to `'Y'`. Without the reset, it stays `'Y'` for every subsequent day in the timecard period. Block 8's continuous-hours gate checks this flag and stays closed forever. The formula stops tracking continuous work entirely from day 2 onwards. **Workers can exceed the legal cap by hours and the formula won't notice**, because tracking is silently disabled. This is the most dangerous of the missing-reset bugs because it produces *under*-flagging, not over-flagging — the lack of errors looks like the formula is working correctly.

              - **Forget the stretch tracker reset:** Day 1's final stretch stays alive into day 2. The first Reg Hours entry on day 2 either extends or restarts that stretch, but either way the resulting `contHrs` calculation includes time from yesterday. False flags fire on day-2 entries because the tracked stretch falsely appears to span 13+ hours.

              - The takeaway: **each missing reset breaks the formula in a different way**. Some over-flag (false positives, annoying), some under-flag (false negatives, dangerous), some produce nonsense. None of them crash. All of them ship to production silently.








3Why this category of bug evades testing



              - UAT timecards are typically constructed for specific test scenarios — one day of work, two days at most. Test data is curated to exercise particular validation paths cleanly.

              - A missing reset only misbehaves when the formula crosses a day boundary. **Single-day test timecards never cross that boundary**, so the bug stays dormant. UAT passes. Sign-off happens. The formula goes to production.

              - Then real workers submit real biweekly timecards. Real biweekly timecards have 10 to 14 days of data. The missing reset fires on day 2, and every day after that. The bug surfaces on the very first real submission, but by then it's a production incident.

              - The defence against this category of bug isn't more careful testing — it's **treating the reset block as atomic**. Every state variable that has a per-day lifetime must be reset at every day boundary. Code review for this block should specifically look for any day-level state declared elsewhere in the formula but missing from this reset.






Every reset line in this block is part of one atomic group. They live together; they reset together. The bug type they prevent is uniquely dangerous because it produces wrong-but-not-crashing behaviour that survives single-day UAT and only surfaces on the first multi-day production submission. Treat the reset block as sacred — never edit one line without considering the others.













Next in The TER Series


Part 4 — The State Machine


The hardest part of the formula is the continuous-hours tracker — a two-state machine with four transitions that survives across loop iterations. Part 4 walks through every transition (START, EXTEND, RESTART, RESET), the setup dependencies in OTL that must exist for the formula to fire, and a full end-to-end trace of Sarah's broken timecard.



AM




Abhishek Mohanty


Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Time and Labor, Absence Management, Core HR, Redwood, HDL, OTBI.




  [Fast Formula](https://abhishekmohanty-hcm.blogspot.com/search/label/Fast%20Formula)
  [Time Entry Rule](https://abhishekmohanty-hcm.blogspot.com/search/label/Time%20Entry%20Rule)
  [OTL](https://abhishekmohanty-hcm.blogspot.com/search/label/OTL)
  [Time and Labor](https://abhishekmohanty-hcm.blogspot.com/search/label/Time%20and%20Labor)
  [Oracle HCM Cloud](https://abhishekmohanty-hcm.blogspot.com/search/label/Oracle%20HCM%20Cloud)