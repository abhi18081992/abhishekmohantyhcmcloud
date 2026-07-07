---
title: "Oracle Fast Formula: How to Generate Logs in OTL — Setup, Code, and Where to Find the Output"
description: "Abhishek Mohanty · April 2026 · 14 min read · Oracle HCM Cloud"
pubDate: 2026-04-19
tags: ["Fast Formula", "Oracle HCM Cloud", "Debugging"]
---

Fast Formula
Time and Labor
Logging
TER & TCR


# Oracle Fast Formula: How to Generate Logs in OTL — Setup, Code, and Where to Find the Output


Abhishek Mohanty · April 2026 · 14 min read · Oracle HCM Cloud


If you have ever written an OTL Fast Formula, deployed it, saved a timecard, and then opened the rule processing page expecting to see your debug lines — only to find the page empty — this post is for you.


OTL logging fails for two reasons. Either the setup chain is incomplete and the formula never fires. Or the visibility switch is off and the engine throws your log lines away before saving them. The order matters. Most posts jump straight to the `add_log` function call, but if the rule never fires, no function call inside it can ever produce a line.


This post walks the chain in the right order: setup first, then the formula, then the profile that makes everything visible.


## TCR Setup — The Calculation Engine


We start with the TCR (Time Calculation Rule) because it is the engine that actually *does* something. It generates overtime entries, splits hours into pay tiers, and applies premium rates. The TER (Time Entry Rule) comes after, because the TER's job is to validate the inputs the TCR will consume. Build the engine first, then build the gatekeeper to feed it cleanly.


### TCR Rule Template (Definition tab)


**Where:** *Setup and Maintenance → Manage Time Rule Templates → New (or open the existing TCR template) → Definition tab.*


Five fields matter on this screen:









  Manage Time Rule Templates · Definition tab


  Name

  My_TCR_Template

  Template Type

  Time Calculation Rule


  ← pins to TCR

  Rule Classification

  Threshold / Shift premium


  ← subtype

  Rule Execution Type

  Create


  ← adds hours

  Summation Level

  Details


  ← one call per row



  Time Card Events




  Submit
  (default)




  Resubmit
  (default)


  Save
  (editable)


  Delete
  (editable)




  Cancel

  Save and Next


Fig 1 — The TCR template Definition tab. Highlighted dropdowns and default-checked events are the fields that control engine behaviour.


  | Field | Value | Why This Value |

  | Name | `Pick a clear name` | Use a prefix + verb describing what the rule does. Names cannot be edited after the first save in some Oracle releases — get it right the first time. |

  | Template Type | `Time Calculation Rule` | Top-level selector that determines which formula types the engine will accept. **Cannot be changed after creation.** A separate *Rule Classification* dropdown below lets you pick a subtype (Threshold, Shift premium, Meal, Break) within this template type. |

  | Rule Execution Type | `Create` | Most overtime calculations need Create — the engine generates new derived rows alongside the source. See the comparison below. |

  | Summation Level | `Details` | Engine calls the formula once per detail row. Formula keeps running totals across calls using `set_wrk_num` / `get_wrk_num`. Day would batch a whole day — you cannot tell which entry caused the cap to be crossed. |

  | Time Card Events | `Submit + Resubmit` | Submit and Resubmit are checked by default — overtime must run at submit time when payroll consumes the data. **Save is editable** if you need calculation to run on every keystroke; most teams leave it off so users don't see overtime numbers shifting as they enter time. |



📌 Execution Type — Update vs Create (per Oracle guide p. 156)


Oracle's official distinction is about *total hours*. **Create adds NEW premium hours on top of reported time — total goes UP** (10 reported → 12 total = 10 reg + 2 added premium). **Update redistributes the SAME reported hours into different pay categories — total stays the SAME** (10 reported → 10 total = 8 reg + 2 OT). Pick the value that matches whether your formula is *adding* hours or *reclassifying* them.




  CREATE
  adds new hours → total goes UP


  Before

  Regular = 10 hrs


  After

  Regular = 10 hrs

  +2 hrs
  = 12 hrs



  UPDATE
  reclassifies existing hours → total stays SAME


  Before

  Regular = 10 hrs


  After

  Regular = 8 hrs

  OT = 2 hrs
  = 10 hrs


Fig 2 — Create adds hours on top (total increases). Update splits existing hours into different pay buckets (total unchanged).


### Time Category (Conditions tab)


**Where:** *Setup and Maintenance → Manage Time Categories → open (or create) your category → Conditions tab.*


The Time Category is a reusable filter. It tells the rule which Payroll Time Types to look at and which to ignore. The principle: **one rule, one job**. Do not let the TCR see entries it has no business processing.


For example, if the TER already validates meal breaks, the TCR has no reason to see them. Pulling Meal Break out of the category fixes two problems with one save: noisy log lines disappear, and meal hours stop inflating the daily worked-hours total.


  | Time Type | Include? |

  | Regular Hours | ✓ Include |

  | Overtime tiers (1.5x, 2x, etc.) | ✓ Include |

  | Holiday / Rest Day premiums | ✓ Include |

  | Meal Break / Unpaid Break | ✗ Remove |

  | Absence entries / anything the TER handles | ✗ Remove |


The exact list depends on your design. The principle is what matters: include only what this rule needs to process.


### TCR Rule (Parameters tab)


**Where:** *Setup and Maintenance → Manage Time Calculation Rules → open your rule → Parameters tab.*


The rule is an instance of the template with parameter values filled in. The most important parameter is `WORKED_TIME_CONDITION` — this is the link between the rule and the Time Category. Without it, the engine processes *all* time types regardless of what your category says. Set it on the rule, not the rule set, not the template.


Threshold parameters (daily regular cap, weekly cap, OT cap) are *custom* — you choose the names and values when you build the rule template. Set them to match your local labour law or company policy. The advantage of parameters over hardcoding: a functional consultant can edit the value in the UI without ever touching the formula.



⚠️ Always verify the binding visually


"Confirmed" in a chat message is not the same as "I see it on screen". Open the rule's Parameters tab, screenshot it, and attach it to your design document.



📌 Time Category can also bind at the Rule Set level


The implementation guide (p. 87) also lets you attach a Time Category to a rule set member. Use rule-level binding via `WORKED_TIME_CONDITION` when the category scopes which entries one rule processes. Use rule-set-level binding when the category gates whether the entire rule set member runs at all.


## TER Setup — The Gatekeeper


The TER (Time Entry Rule) validates entries before the TCR sees them. Different rule type, different needs.


### TER Rule Template (Definition tab)


**Where:** *Setup and Maintenance → Manage Time Rule Templates → open (or create) the TER template → Definition tab.*









  Manage Time Rule Templates · Definition tab


  Name

  My_TER_Template

  Template Type

  Time Entry Rule


  ← pins to TER

  Rule Classification

  Business message / Variance


  ← subtype

  Summation Level

  Day


  ← or Time Card

  Reporting Level

  Day


  ← match summation



  Time Card Events
  all editable — tune per rule




  Save
  (default — immediate validation)




  Submit
  (default)




  Resubmit
  (default)


  Delete
  (off by default)




  Cancel

  Save and Next


Fig 3 — The TER template Definition tab. Summation Level and Reporting Level are two independent dropdowns — they can hold different values.


  | Field | Value | Why This Value |

  | Template Type | `Time Entry Rule` | Top-level selector that gives the formula access to entry-level context arrays. The *Rule Classification* dropdown below lets you pick a subtype (Business message, Comparison validation, Hours entered, Variance) within this template type. |

  | Summation Level | `Day or Time Card` | **Day** — engine bundles all detail rows for one day + END_DAY marker. Good for overlap, continuous stretch, meal break checks. **Time Card** — engine bundles the entire period. Good for weekly max hours, min days worked. See the *Day vs Time Card Summation* section below for code differences. |

  | Reporting Level | `Match your summation` | Where the error message appears: Details = row-level, Day = day banner, Time Card = period banner. Independent of Summation Level — they are two separate dropdowns and people mix them up. |

  | Time Card Events | `Save · Submit · Resubmit` | Save, Submit, and Resubmit are typically checked for TER templates so validation fires on every user action. All four events are editable — untick Save if validation is expensive and you only want it at submission time. |



⚠️ Regenerate after changing the template


Changing Summation Level on the template does not take effect until you click through the wizard to Review and re-save. The rule built from the template also needs regeneration. Skip either step and the engine behaves as if nothing changed.




  DAY
  — formula called once per day
  5 calls




    Mon


    FF


    Tue


    FF


    Wed


    FF


    Thu


    FF


    Fri


    FF



  Each call is independent — state resets between days
  Simpler code · good for daily validations



  TIME CARD
  — formula called once for the whole period
  1 call



    Mon
    Tue
    Wed
    Thu
    Fri










    FF



  All days in one array — state accumulates across the week
  More code · needed for weekly totals and cross-day checks


Fig 4 — Day mode runs the formula 5 separate times. Time Card mode runs it once with everything bundled together.


### TER Rule (Parameters tab)


The TER rule typically does not need a Time Category binding — validation runs across all time types. Its parameters are the validation thresholds (schedule start/end hour, maximum continuous hours before warning or error). Set these on the rule, not the template.


### Bind Both Rules into Rule Sets and Profile


The remaining setup is the same for both TER and TCR — five steps, and all five must be in place or the formula never fires:





  1
  Add the Rule to a Rule Set
  Manage Time Calculation Rule Sets (TCR) or Time Entry Rule Sets (TER)









  2
  Attach Rule Set to a Worker Time Processing Profile
  Entry rule set and Calculation rule set go on the same profile








  3
  Assign the Profile to an HCM Group
  The group defines which workers this profile applies to








  4
  Run Evaluate HCM Group Membership
  Tools → Scheduled Processes — run it manually or schedule it








  5
  Worker saves a timecard → formula fires
  If everything above is in place, the engine will invoke your formula



  ⚠ Skip step 4 and the formula never fires — this is the most commonly missed step


Fig 5 — The setup chain. All five steps must be in place or the formula never fires.


## Logging Inside the Formula


Setup chain done. The engine will now call your formula when a user saves a timecard. Time to write the lines that capture what is happening inside. OTL exposes **two functions** for this — both work, both write to the same place.


### The Two Logging Functions


  | Function | Arguments | When to Use |

  | `add_log` | `(ffs_id, message)` | The shorter form. The rule_id is figured out automatically by the engine. Works in standard TER and TCR formulas. |

  | `add_rlog` | `(ffs_id, rule_id, message)` | The longer form with rule_id passed explicitly. Use when the auto-determined rule_id is not behaving the way you expect. |


Both functions return a number. Fast Formula requires every expression to be assigned, so we write `flog = add_log(...)` — the value of `flog` is never used.


### The Two Required Contexts


Both functions need `ffs_id`. `add_rlog` also needs `rule_id`. Both come from contexts the engine populates before calling your formula:


```
ffs_id  = GET_CONTEXT(HWM_FFS_ID, 0)
rule_id = GET_CONTEXT(HWM_RULE_ID, 0)
```



📌 The HWM_ prefix matters


Older posts show `HXT_FFS_ID` or `HXT_RULE_ID` — those are leftover names from the on-premises HXT module. In Oracle Fusion HCM Cloud, the contexts are **HWM_**. Mixing them up gives you a NULL ffs_id and every `add_log` call silently writes nothing.


### Where the Lines Actually Go


Both functions produce log lines that you view on the **Analyze Rule Processing Details** page — that is the supported way to read OTL formula logs.




  Your Formula
  add_log() / add_rlog()





  logs appear on



  Analyze Rule
  Processing Details


`ESS_LOG_WRITE` only works when the formula runs inside an ESS batch job — it stays silent on UI-triggered saves. Stick with `add_rlog` for universal coverage.



⚠️ For those who used to query the table directly


In earlier releases, consultants would query `HWM_RULE_FF_WORK_LOG` via BI Publisher SQL data models as a debugging shortcut. From 2025 onward, Oracle has decommissioned this table — it is no longer reliably populated and is not exposed in OTBI. The **Analyze Rule Processing Details** UI page is the only supported path.


### A Useful Convention: The >>> Prefix


The rule processing log mixes Oracle's own engine messages with your custom lines. Prefix every message with `>>>` so you can Ctrl+F straight to your lines and ignore the noise:


```
flog = add_log(ffs_id, '>>> Enter ' || ffName || ' v1.0')
flog = add_log(ffs_id, '>>> idx=' || to_char(nidx) || ' qty=' || to_char(aiMeasure))
flog = add_log(ffs_id, '>>> Exit ' || ffName)
```


## The Profile Option That Controls Everything


Until somebody flips this, every `add_log` call you wrote is the equivalent of waving at a camera nobody is recording.


### ORA_HWM_RULES_LOG_LEVEL



  ORA_HWM_RULES_LOG_LEVEL


  MORE





  LESS



  Finest
  ← use this for testing





  everything for every rule type



  Finer




  + individual rule logs (TER and TCR)



  Fine




  rule set logs only



  Incident
  ← default (almost nothing)




  only when processing fails


  retention level
  what gets kept in the log


Fig 7 — At the default **Incident** level, the engine throws away almost everything. **Finest** keeps the full trace — what you want during testing.


  | Level | What Gets Kept |

  | Incident | **Default.** Keeps logs only when processing fails. Successful runs leave no trace. |

  | Fine | Keeps rule set logs (TCR and entry rule sets). No individual rule logs. |

  | Finer | Adds individual rule logs for time calculation and entry rules. |

  | Finest ← use this | **Keeps everything for every rule type.** This is what you want during testing. |



✅ How to flip the dial


Setup and Maintenance → search "Manage Administrator Profile Values" → search profile code `ORA_HWM_RULES_LOG` → set `ORA_HWM_RULES_LOG_LEVEL` to **Finest** at Site level → also set `ORA_HWM_RULES_LOG_MONTHS_TO_KEEP` to **1** at Site level → Save and Close → **sign out completely and sign back in**.


### Data Role and Security Profile


Setting the profile is necessary but not enough. The user viewing Analyze Rule Processing Details also needs a data role: **Time and Labor Administrator** job role, with security profiles for View All Organizations, View All Positions, View All LDGs, and **View All People** (not "View All Workers" — that is different).



📌 MOS Doc 2120220.1


If the profile is Finest, the formula compiles, the chain is intact, and you still see "No data to display" — the cause is almost always the data role gap. Oracle MOS Doc **2120220.1** documents this exact situation.


## Framework of the Code — TER Skeletons


Two skeletons below. The first is a **minimal logging-only TER** — drop it in to confirm your setup chain works. The second is the **production skeleton** with all the guards. Between them, the *Day vs Time Card Summation* section explains what changes in the code depending on whether you chose Day or Time Card summation.


### Minimal TER Logging Skeleton


The smallest TER formula that produces useful logs. Deploy this first after enabling `ORA_HWM_RULES_LOG_LEVEL = Finest`. If you save a timecard and see these lines on Analyze Rule Processing Details, every link in the chain is working.


```
/******************************************************************
  FORMULA: MY_TER_LOG_TEST
  TYPE   : Time Entry Rule
  PURPOSE: Smallest TER that produces useful logs.
           Deploy this first to confirm logging works end-to-end.
******************************************************************/

DEFAULT FOR HWM_CTXARY_RECORD_POSITIONS IS EMPTY_TEXT_NUMBER
DEFAULT FOR measure                     IS EMPTY_NUMBER_NUMBER
DEFAULT FOR PayrollTimeType             IS EMPTY_TEXT_NUMBER

INPUTS ARE
  HWM_CTXARY_RECORD_POSITIONS,
  measure, PayrollTimeType

ffName  = 'MY_TER_LOG_TEST'
ffs_id  = GET_CONTEXT(HWM_FFS_ID, 0)
rule_id = GET_CONTEXT(HWM_RULE_ID, 0)
asg_id  = GET_CONTEXT(HWM_SUBRESOURCE_ID, 0)

flog = add_log(ffs_id, '>>> Enter ' || ffName)
flog = add_log(ffs_id, '>>> ffs_id=' || to_char(ffs_id))
flog = add_log(ffs_id, '>>> rule_id=' || to_char(rule_id))

CHANGE_CONTEXTS(HR_ASSIGNMENT_ID = asg_id)
(
  wMaAry = HWM_CTXARY_RECORD_POSITIONS.count
  flog = add_log(ffs_id, '>>> Total rows: ' || to_char(wMaAry))

  nidx = 0
  WHILE (nidx LOOP
  (
    nidx = nidx + 1
    aiRecPos = HWM_CTXARY_RECORD_POSITIONS[nidx]
    aiType   = '**NULL**'
    IF (PayrollTimeType.exists(nidx)) THEN  aiType = PayrollTimeType[nidx]

    flog = add_log(ffs_id,
             '>>> idx=' || to_char(nidx) ||
             ' pos='   || aiRecPos ||
             ' type=[' || aiType || ']')
  )
)

flog = add_log(ffs_id, '>>> Exit ' || ffName)
RETURN OUT_MSG
```



💡 What you should see


`>>> Enter MY_TER_LOG_TEST`, the two context IDs as non-zero numbers, the row count, one `>>> idx=` line per timecard entry, and `>>> Exit MY_TER_LOG_TEST`. If anything is missing, walk the checklist in the *30-Second Checklist* below.


### What Changes in the Code: Day vs Time Card Summation


The Summation Level you set on the rule template changes *what the engine sends* to the formula. The code must be written differently depending on which one you pick.


  | Aspect | Day Summation | Time Card Summation |

  | When formula is called | Once per day | Once for the entire period |

  | Array contains | DETAIL rows + END_DAY | DETAIL rows + END_DAY per day + END_PERIOD at the end |

  | Day-level state reset? | No — formula starts fresh each call | Yes — clear at END_DAY or Monday leaks into Tuesday |

  | END_PERIOD handling? | Not needed — no END_PERIOD marker | Yes — run period-level checks here |

  | Cross-day totals (weekly max)? | Not possible (no memory between calls) | Built in — running totals accumulate naturally |


**Day Summation** — the simpler pattern. No manual state reset needed, no END_PERIOD handler. Good for overlap, continuous stretch, meal break, daily max checks:


```
/* ═══ DAY SUMMATION — simpler pattern ═══
   Engine calls once per day.
   Array = DETAIL rows for one day + END_DAY.
   No END_PERIOD. State resets between calls. */

WHILE (nidx LOOP
(
  nidx = nidx + 1
  aiRecPos = HWM_CTXARY_RECORD_POSITIONS[nidx]

  IF (aiRecPos = 'DETAIL') THEN
  (
    /* Read entry data, log it, business logic */
    flog = add_log(ffs_id, '>>> idx=' || to_char(nidx) || ' type=[' || aiType || ']')
  )

  IF (aiRecPos = 'END_DAY') THEN
  (
    /* Run day-level checks (overlap, daily total) */
    flog = add_log(ffs_id, '>>> END_DAY checks done')
    /* No state reset needed — next call starts fresh */
  )
)
```


**Time Card Summation** — adds two extra blocks (marked with ★):


```
/* ═══ TIME CARD SUMMATION — fuller pattern ═══
   Engine calls once for the entire period.
   Array = DETAIL rows + END_DAY per day + END_PERIOD at the end. */

WHILE (nidx LOOP
(
  nidx = nidx + 1
  aiRecPos = HWM_CTXARY_RECORD_POSITIONS[nidx]

  IF (aiRecPos = 'DETAIL') THEN
  (
    /* Same as Day pattern — read, log, business logic */
    flog = add_log(ffs_id, '>>> idx=' || to_char(nidx) || ' type=[' || aiType || ']')
    l_week_total = l_week_total + aiMeasure
  )

  IF (aiRecPos = 'END_DAY') THEN
  (
    /* Run day-level checks — same as Day pattern */

    /* ★ EXTRA 1: Manual state reset — without this Monday leaks into Tuesday */
    l_day_total     = 0
    l_stretch_start = NullDate
    l_stretch_end   = NullDate
    l_in_stretch    = 'N'
    l_day_count     = 0
    flog = add_log(ffs_id, '>>> END_DAY reset done')
  )

  /* ★ EXTRA 2: END_PERIOD — period-level final checks */
  IF (aiRecPos = 'END_PERIOD') THEN
  (
    IF (l_week_total > l_weekly_max) THEN
    (
      OUT_MSG[nidx] = 'Weekly hours exceed maximum'
    )
    flog = add_log(ffs_id, '>>> END_PERIOD weekTotal=' || to_char(l_week_total))
  )
)
```



📌 Summary of the two extras


Time Card adds exactly two code blocks Day does not need: **★ EXTRA 1** — Manual state reset inside END_DAY (so Monday's totals don't leak into Tuesday). **★ EXTRA 2** — END_PERIOD handler for period-level checks. The DETAIL processing is identical between the two. Start with Day, add these two if you later switch to Time Card.


### Production-Ready Skeleton


Once logging works, build on this. It adds runaway-loop protection, header-attribute readback, parameter logging, and explicit business-logic placement. The formula name (`MY_TER_FORMULA`) and parameter names are placeholders — replace them. Oracle-defined names (`HWM_FFS_ID`, `OUT_MSG`, etc.) must stay exactly as shown.


```
/* A. DEFAULTS — array types matching the template contract */
DEFAULT FOR HWM_CTXARY_RECORD_POSITIONS IS EMPTY_TEXT_NUMBER
DEFAULT FOR HWM_CTXARY_HWM_MEASURE_DAY  IS EMPTY_NUMBER_NUMBER
DEFAULT FOR measure                     IS EMPTY_NUMBER_NUMBER
DEFAULT FOR PayrollTimeType             IS EMPTY_TEXT_NUMBER
DEFAULT FOR StartTime                   IS EMPTY_DATE_NUMBER
DEFAULT FOR StopTime                    IS EMPTY_DATE_NUMBER

INPUTS ARE
  HWM_CTXARY_RECORD_POSITIONS, HWM_CTXARY_HWM_MEASURE_DAY,
  measure, PayrollTimeType, StartTime, StopTime

/* B. CONTEXT INIT */
ffName  = 'MY_TER_FORMULA'
ffs_id  = GET_CONTEXT(HWM_FFS_ID, 0)
rule_id = GET_CONTEXT(HWM_RULE_ID, 0)
asg_id  = GET_CONTEXT(HWM_SUBRESOURCE_ID, 0)
NullDate = '01-JAN-1900'(DATE)
NullText = '**FF_NULL**'

/* C. ENTRY MARKER */
flog = add_log(ffs_id, '>>> Enter ' || ffName || ' v1.0')
flog = add_log(ffs_id, '>>> ffs_id=' || to_char(ffs_id) || ' rule_id=' || to_char(rule_id))

/* D. ASSIGNMENT CONTEXT WRAPPER */
CHANGE_CONTEXTS(HR_ASSIGNMENT_ID = asg_id)
(
  /* E. Read & log header attributes */
  rptLvl = Get_Hdr_Text(rule_id, 'RUN_TBB_LEVEL', 'DAY')
  flog = add_log(ffs_id, '>>> rptLvl=' || rptLvl)

  /* F. Read rule parameters & log them */
  p_sched_start = get_rvalue_number(rule_id, 'SCHEDULE_START_HOUR', 0)
  p_sched_end   = get_rvalue_number(rule_id, 'SCHEDULE_END_HOUR',   0)
  flog = add_log(ffs_id, '>>> sched=' || to_char(p_sched_start) || '-' || to_char(p_sched_end))

  /* G. Loop with guards */
  nidx   = 0
  wMaAry = HWM_CTXARY_RECORD_POSITIONS.count
  flog = add_log(ffs_id, '>>> Total rows: ' || to_char(wMaAry))

  WHILE (nidx LOOP
  (
    nidx = nidx + 1
    IF (nidx > 1000) THEN ( flog = add_log(ffs_id, '>>> ABORT runaway')  RETURN OUT_MSG )

    aiRecPos = HWM_CTXARY_RECORD_POSITIONS[nidx]

    IF (aiRecPos = 'DETAIL') THEN
    (
      aiMeasure = 0
      aiType    = NullText
      IF (measure.exists(nidx))         THEN  aiMeasure = measure[nidx]
      IF (PayrollTimeType.exists(nidx)) THEN  aiType    = PayrollTimeType[nidx]

      flog = add_log(ffs_id,
               '>>> idx=' || to_char(nidx) || ' pos=' || aiRecPos ||
               ' type=[' || aiType || ']' || ' qty=' || to_char(aiMeasure))

      /* === Your business logic goes here === */
    )
    IF (aiRecPos = 'END_DAY') THEN
    (  flog = add_log(ffs_id, '>>> END_DAY checks here')  )
    IF (aiRecPos = 'END_PERIOD') THEN
    (  flog = add_log(ffs_id, '>>> END_PERIOD checks here')  )
  )
)

/* H. EXIT MARKER */
flog = add_log(ffs_id, '>>> Exit ' || ffName)
RETURN OUT_MSG
```


## Framework of the Code — TCR Skeletons


TCR formulas calculate or reclassify hours — they do not validate. The structure depends on the **Summation Level** you chose on the template. At **Details** level (the most common for TCR), the engine calls your formula once per matched time entry row, passing *scalar* values — not arrays. That makes TCR formulas shorter than TER formulas.


### Minimal TCR Logging Skeleton


The smallest TCR formula that logs the incoming time entry. Deploy this first to confirm your TCR setup chain works. It creates no new entries — it just logs and exits.


```
/******************************************************************
  FORMULA: MY_TCR_LOG_TEST
  TYPE   : Time Calculation Rule (Create · Details)
  PURPOSE: Smallest TCR that produces useful logs.
           Creates nothing — just confirms the engine calls it.
******************************************************************/

DEFAULT FOR measure         IS 0
DEFAULT FOR PayrollTimeType IS ' '
DEFAULT FOR StartTime       IS '01-JAN-1900 00:00:00'(DATE)
DEFAULT FOR StopTime        IS '01-JAN-1900 00:00:00'(DATE)

INPUTS ARE
  measure, PayrollTimeType, StartTime, StopTime

ffName  = 'MY_TCR_LOG_TEST'
ffs_id  = GET_CONTEXT(HWM_FFS_ID, 0)
rule_id = GET_CONTEXT(HWM_RULE_ID, 0)

flog = add_log(ffs_id, '>>> Enter ' || ffName)
flog = add_log(ffs_id, '>>> measure=' || to_char(measure))
flog = add_log(ffs_id, '>>> type=' || PayrollTimeType)
flog = add_log(ffs_id, '>>> start=' || to_char(StartTime, 'DD-MON-YYYY HH24:MI'))
flog = add_log(ffs_id, '>>> stop=' || to_char(StopTime, 'DD-MON-YYYY HH24:MI'))

/* No calculation — just logging to confirm the formula fires */

flog = add_log(ffs_id, '>>> Exit ' || ffName)
RETURN
```



💡 What you should see


`>>> Enter MY_TCR_LOG_TEST`, the measure value (hours), payroll time type, start/stop timestamps, and `>>> Exit MY_TCR_LOG_TEST`. One set of lines per matched time entry row. If you see nothing, walk the *30-Second Checklist* below.



📌 TER vs TCR — key structural difference


**TER** receives arrays (`HWM_CTXARY_RECORD_POSITIONS`, `measure[]`) and loops through them. **TCR at Details level** receives scalar values (`measure`, `PayrollTimeType`) — no loop needed. The engine calls the formula once per matched row and passes one row's worth of data each time.


### Production-Ready TCR Skeleton (Create · Threshold)


A full TCR skeleton with array defaults, header-level rule reads, execution-type guard, null-safe checks, and a two-row output split. The formula name (`XX_GENERIC_TCR_SKELETON`) and parameter names are placeholders — replace them with your own.


```
/* A. DEFAULTS */
DEFAULT FOR HWM_CTXARY_RECORD_POSITIONS  IS EMPTY_TEXT_NUMBER
DEFAULT FOR HWM_CTXARY_HWM_MEASURE_DAY   IS EMPTY_NUMBER_NUMBER

DEFAULT FOR MEASURE                      IS EMPTY_NUMBER_NUMBER
DEFAULT FOR PayrollTimeType              IS EMPTY_TEXT_NUMBER
DEFAULT FOR StartTime                    IS EMPTY_DATE_NUMBER
DEFAULT FOR StopTime                     IS EMPTY_DATE_NUMBER

/* B. INPUTS */
INPUTS ARE
    HWM_CTXARY_RECORD_POSITIONS,
    HWM_CTXARY_HWM_MEASURE_DAY,
    MEASURE,
    PayrollTimeType,
    StartTime,
    StopTime

/* C. CONTEXT INIT + NULL GUARDS */
ffName        = 'XX_GENERIC_TCR_SKELETON'
ffs_id        = GET_CONTEXT(HWM_FFS_ID,  0)
rule_id       = GET_CONTEXT(HWM_RULE_ID, 0)

NullDate      = '01-JAN-1900'(DATE)
NullDateTime  = '1900/01/01 00:00:00'(DATE)
NullText      = '**FF_NULL**'

/* D. HEADER-LEVEL RULE READS */
l_hdr_sum_lvl   = Get_Hdr_Text(rule_id, 'RUN_SUMMATION_LEVEL', 'TIMECARD')
l_hdr_ExecType  = Get_Hdr_Text(rule_id, 'RULE_EXEC_TYPE',      'CREATE')

flog = ADD_RLOG(ffs_id, '>>> Enter ' || ffName || ' v1.0')
flog = ADD_RLOG(ffs_id, '>>> ExecType=' || l_hdr_ExecType ||
                         ' SumLvl=' || l_hdr_sum_lvl)

/* Only proceed on CREATE pass — skip VALIDATE to avoid duplicates */
IF (l_hdr_ExecType = 'CREATE') THEN
(
  /* E. READ RULE PARAMETERS */
  p_threshold = GET_RVALUE_NUMBER(rule_id, 'DAILY_THRESHOLD',        0)
  p_ot_type   = GET_RVALUE_TEXT  (rule_id, 'OT_PAYROLL_TIME_TYPE', ' ')

  flog = ADD_RLOG(ffs_id, '>>> threshold=' || TO_CHAR(p_threshold) ||
                           ' ot_type='     || p_ot_type)

  /* F. PROCESS CURRENT MEASURE */
  flog = ADD_RLOG(ffs_id, '>>> measure=' || TO_CHAR(MEASURE) ||
                           ' type='      || PayrollTimeType)

  IF (MEASURE WAS NOT DEFAULTED AND PayrollTimeType <> NullText) THEN
  (
    l_excess = MEASURE - p_threshold

    IF (l_excess > 0) THEN
    (
      flog = ADD_RLOG(ffs_id, '>>> SPLIT: reg=' || TO_CHAR(p_threshold) ||
                               ' ot=' || TO_CHAR(l_excess))

      /* Row 1 — regular hours capped at threshold */
      out_measure[1]         = p_threshold
      out_PayrollTimeType[1] = PayrollTimeType
      out_StartTime[1]       = StartTime
      out_StopTime[1]        = StopTime

      /* Row 2 — overtime hours */
      out_measure[2]         = l_excess
      out_PayrollTimeType[2] = p_ot_type
      out_StartTime[2]       = StartTime
      out_StopTime[2]        = StopTime
    )
    ELSE
    (
      flog = ADD_RLOG(ffs_id, '>>> PASSTHROUGH: measure )

      out_measure[1]         = MEASURE
      out_PayrollTimeType[1] = PayrollTimeType
      out_StartTime[1]       = StartTime
      out_StopTime[1]        = StopTime
    )
  )
  ELSE
  (
    flog = ADD_RLOG(ffs_id, '>>> SKIP: null measure or type')
  )
)
ELSE
(
  flog = ADD_RLOG(ffs_id, '>>> Skipping — ExecType=' || l_hdr_ExecType)
)

/* G. EXIT */
flog = ADD_RLOG(ffs_id, '>>> Exit ' || ffName)

RETURN out_measure,
       out_PayrollTimeType,
       out_StartTime,
       out_StopTime
```



✅ What this skeleton covers


**Execution-type guard** — only runs on the CREATE pass, skips VALIDATE to avoid duplicate entries. **WAS NOT DEFAULTED** — null-safe check so the formula doesn't process empty rows. **Two-row output** — Row 1 caps regular hours at the threshold, Row 2 holds the overtime excess. If hours are under the threshold, the formula passes through a single row unchanged. Every decision is logged with `ADD_RLOG` so you can trace exactly which branch fired.


## Summary — Where the Logs Land and How to Read Them


### Viewing the Logs (UI)


**1.** My Client Groups → Time Management → Tasks panel → **Analyze Rule Processing Details** → **2.** Search by employee or rule set name + timecard date range → **3.** Click the most recent processing run row → **4.** In Processing Results, click **Rule Processing Log** → search for your `>>>` prefix.


### Sample Log Output


```
>>> Enter MY_TER_FORMULA v1.0
>>> ffs_id= rule_id=
>>> rptLvl=DAY
>>> Total rows: 3
>>> idx=1 pos=DETAIL   type=[Regular Hours] qty=
>>> idx=2 pos=DETAIL   type=[Meal Break]    qty=
>>> idx=3 pos=END_DAY  type=[**FF_NULL**]   qty=0
>>> Exit MY_TER_FORMULA
```


### The Forced-Error Trick


If you have done everything right and still see nothing, you can push diagnostic data straight into the validation message that surfaces on the timecard. The exact output variable name (`OUT_MSG` in the example below) varies by template — some Oracle samples use `out_msg_ary`. Check your template's output spec before borrowing the snippet:


```
/* DEBUG MODE — push diagnostic payload into the user-facing message */
OUT_MSG[1] = 'DEBUG: idx=1 type=' || aiType || ' qty=' || to_char(aiMeasure)
RETURN OUT_MSG
```



Your future self will thank you for removing this before UAT. Your functional lead will not thank you if you don't.


### The 30-Second Checklist


If logs do not appear, walk these in order:


  | # | Check | Where |

  | 1 | TCR template — Execution Type + Summation Level correct | Manage Time Rule Templates → TCR template |

  | 2 | TER template — Summation Level + Reporting Level correct | Manage Time Rule Templates → TER template |

  | 3 | Time Category cleaned — only what the rule needs | Manage Time Categories → Conditions tab |

  | 4 | WORKED_TIME_CONDITION bound to the category | Manage Time Calculation Rules → Parameters tab |

  | 5 | Rule sets → Profile → HCM Group → Evaluate Membership | Worker Time Processing Profiles + Scheduled Processes |

  | 6 | add_log / add_rlog with correct HWM_ contexts | Inside the Fast Formula |

  | 7 | ORA_HWM_RULES_LOG_LEVEL = Finest + sign-out / sign-in | Manage Administrator Profile Values |

  | 8 | Data role: View All People + Orgs + Positions + LDGs | Manage Data Role and Security Profiles (MOS 2120220.1) |


## Key Takeaways


**Setup before code, code before profile, profile before debugging.** Most of us start at the wrong end — writing `add_log` calls and then wondering why nothing shows up — when the answer is usually one screen away.


**Two functions, same destination.** `add_log` (2 args) and `add_rlog` (3 args) both write to an internal log table. View the output on the Analyze Rule Processing Details page. Nothing else works for UI-triggered timecard saves.


**Day vs Time Card — two extras.** Time Card summation needs manual state reset at END_DAY and an END_PERIOD handler. Day does not. Start with Day for daily validations, switch to Time Card only when you need period-level checks.


**The skeleton is the starting point.** Drop the minimal TER skeleton in, confirm logs appear, then graduate to the production skeleton with all the guards. Business logic goes on top.



AM




Abhishek Mohanty


Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time and Labor, Core HR, Redwood, HDL, OTBI.