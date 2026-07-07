---
title: "Oracle Fast Formula: GET_PLAN_BALANCE, GET_ABSENCE_COUNTS, and the Two Traps That Quietly Ship the Wrong Number"
description: "April 28, 2026(https://abhishekmohanty-hcm.blogspot.com/2026/04/)"
pubDate: 2026-04-28
tags: ["Fast Formula", "Oracle HCM Cloud", "Absence Management"]
---

[April 28, 2026](https://abhishekmohanty-hcm.blogspot.com/2026/04/)


Fast Formula
Absence Management
GET_PLAN_BALANCE
DBI


# Oracle Fast Formula: Reading Absence Balance — Four Mechanisms, the Naming Traps, and a Recipe That Actually Works


**Abhishek Mohanty** · April 2026 · 14 min read · Oracle HCM Cloud


If you have ever written an absence Fast Formula, deployed it, watched it compile cleanly, and then opened the timecard or the absence record only to find a wrong balance — this post is for you.


Reading absence balance fails for two reasons. Either the function you picked reads from the wrong place — the saved snapshot when you needed live, or vice versa. Or the filter you wrote does nothing because of a status-column naming asymmetry that is easy to miss. Most blogs jump straight to the function call. But if the mechanism does not match the use case, no amount of tweaking inside it will produce the right number.


This post walks through all four mechanisms in order: what each one queries under the hood, when it works, when it silently fails, and the production-ready composite recipe that combines two of them into a balance reader you can defend in audit.


FORMULA CONTEXT · THE QUESTION




















  FORMULA CONTEXT





    Plan Use Rate FF




    Entry Validation FF




    Type Duration FF




    Carryover FF




    Custom Accrual FF










    THE RECURRING QUESTION
    What is this person's
    accrual balance right now?

    ...and how much have they already consumed?



  AVAILABLE MECHANISMS








    MECHANISM 1
    GET_PLAN_BALANCE



    MECHANISM 2
    GET_ABSENCE_COUNTS



    MECHANISM 3
    GET_ABSENCE_DAYS_PER_TYPE



    MECHANISM 4 · RECOMMENDED
    DBI driver array + scalars




  Pick wrong
  → no compile error · no warning · the formula returns a number, just not the right one.


**Fig 1 —** Five formula contexts converge on the same sub-question. Four mechanisms can answer it, but the silent failure mode — wrong number, no compile error — is what makes the choice load-bearing.


## The Four Mechanisms — Side by Side


Before we go deep on each one, here is the quick reference table. Keep it open when you are halfway through writing a formula and trying to remember which function fits the use case.


| Mechanism | Reads From | Sees In-Progress | Filter Visible | Best For |


| `GET_PLAN_BALANCE` | Saved balance | No | N/A | Carryover, period-end reports, snapshot anchor |

| `GET_ABSENCE_COUNTS` | Live entries | Yes | No | "Applied for" occurrence rules |

| `GET_ABSENCE_DAYS_PER_TYPE` | Live entries | Yes | Hidden | Indicative reports only |

| Read each entry yourself *(recommended)* | Live entries | Yes | Yes | Real-time decisions, audit-grade rules |


CAPABILITY MATRIX














  CAPABILITY
  Compare across mechanisms




  MECHANISM 1
  GET_PLAN_BALANCE





  MECHANISM 2
  GET_ABSENCE_COUNTS





  MECHANISM 3
  GET_ABSENCE_DAYS
  _PER_TYPE





  RECOMMENDED
  Driver + Scalars



    Source table
    Sees in-flight entries
    Status filter visible
    Status filter overridable
    Audit-defensible
    Suitable for live decisions










  ACRL_ENTRY_DTLS
  No
  N/A
  N/A
  Yes (snapshot)
  No


  ABS_ENTRIES
  Yes
  No
  No
  Partial
  Occurrence rules


  ABS_ENTRIES
  Yes
  No (opaque)
  No
  No
  No



  ABS_ENTRIES
  Yes
  Yes (in code)
  Yes
  Yes
  Yes


**Fig 2 —** Capability matrix across all four mechanisms. Mechanism 4 is the only path that earns a "yes" on every dimension — at the cost of around fifty lines of structural setup that the other three avoid.


📌 Why this is harder than it should be
The four functions all return a number related to absence consumption. They all compile. The differences only show up in specific lifecycle states — in-progress requests, withdrawn entries, post-batch lag — which UAT often does not exercise systematically. The bug ships and surfaces three months later when an auditor asks why the numbers do not reconcile.


## Mechanism 1 — GET_PLAN_BALANCE (the saved snapshot)


The default reach for anyone who has read the Oracle documentation. Returns a clean numeric balance, well-named, and works perfectly in unit tests. It is also the most frequent root cause of broken Entry Validation rules in production.


**Where the data comes from:** *ANC_PER_ACRL_ENTRY_DTLS — the committed accrual ledger, refreshed only when the absence accrual engine runs (typically nightly batch).*


### Scenario from the UI


Open **Me > Time and Absences > Absence Balance**. The plan balance shown there comes from the latest accrual run — signed off and stable. But if a leave was submitted this morning, you will not see its impact here until the next batch runs. `GET_PLAN_BALANCE` reads from the exact same place.


SEQUENCE DIAGRAM · A DAY IN THE LIFE OF A BALANCE






















  SEQUENCE DIAGRAM
  A day in the life of an Annual Leave balance



    Employee
    UI / Self-Service
    ANC_PER_ABS_ENTRIES
    (live)
    Accrual Engine
    (batch)
    ANC_PER_ACRL_ENTRY_DTLS
    (snapshot ledger)
    GET_PLAN_BALANCE
    (your formula)


















    Last night 02:00
    batch ran


    Today 14:00
    leave submitted


    Today 15:00
    formula runs


    Tonight 02:00
    next batch




  STALE DATA WINDOW




    Balance: 5.0






  submits 3-day AL



  INSERT entry (Submitted)



    +1 row written






    no engine run
    → ledger unchanged




  read ledger



    Returns 5.0





    Live: 2.0








    Δ = 3.0 days
    silent gap






    batch run



    Balance: 2.0



**Fig 3 —** Sequence diagram of the lag mechanism. The 14:00 absence submission writes to the live table immediately, but the snapshot ledger is not updated until the next batch run at 02:00. Any formula calling `GET_PLAN_BALANCE` in the intervening 12-hour window reads stale data, and the absence engine provides no callback to invalidate it.


### The signature most authors get wrong


The function takes **one explicit argument** — the plan name. Person, assignment, plan ID, effective date, and LDG must already be in scope as **contexts**. The PL/SQL-style three-argument call is a common carry-over from data-warehouse SQL habits, and it is wrong.


```
/* Correct call */
g_balance = GET_PLAN_BALANCE('Annual Leave Plan')

/* These must be in scope as contexts — you do NOT pass them as arguments:
   PERSON_ID
   HR_ASSIGNMENT_ID
   EFFECTIVE_DATE
   ACCRUAL_PLAN_ID
   LEGISLATIVE_DATA_GROUP_ID                                              */
```


✅ Use it for
Carryover formulas (where you want the snapshot — that is precisely the point), period-end reporting, accrual statements, and as the "starting balance" inside the composite recipe later in this post. Do **not** use it stand-alone for any decision that must reflect the current moment.


## Mechanism 2 — GET_ABSENCE_COUNTS (counts everything, even withdrawn)


Reads the live absence collection. Counts entries in a date range and returns six duration totals via OUT parameters. Useful, with one well-known catch: it applies **no status filter at all**. Withdrawn entries count. Denied entries count. Approved entries count. They are all the same to this function.


**Where the data comes from:** *ANC_PER_ABS_ENTRIES — the live absence collection, updated transactionally on every Submit, Approve, or Withdraw.*


### Scenario from the UI


Switch to **Me > Time and Absences > Existing Absences**. It lists every absence the employee ever recorded — submitted, approved, withdrawn, denied, all of them. If you simply count the rows, you get a true count of entries, but not a count of leave actually consumed. `GET_ABSENCE_COUNTS` works the same way.


DATA VIEW · GET_ABSENCE_COUNTS










  DATA VIEW
  An employee's three Annual Leave entries this quarter




    ENTRY_ID
    DATES
    DURATION
    STATUS





    300012345
    15-Jan → 19-Jan
    5 days

    APPROVED





    300012451
    22-Mar → 22-Mar
    1 day

    SUBMITTED





    300012612
    02-Mar → 03-Mar
    2 days

    WITHDRAWN




  should be excluded
  in most rules




    FORMULA CALL
    GET_ABSENCE_COUNTS(
    person_id,
    'AL', '',
    '01-Jan', '31-Mar',
    l_count, l_days, ...
    )

    l_count = 3 ← all rows





    DOCUMENTED LIMITATION · MOS Doc ID 2899647.1
    "Need To Exclude Denied And Withdrawn Absences From GET_ABSENCE_COUNTS Results" — the function provides no parameter to filter on lifecycle state.



**Fig 4 —** Three live entries on `ANC_PER_ABS_ENTRIES`; `GET_ABSENCE_COUNTS` returns 3 regardless of how many should logically count. The withdrawn entry inflates every consumption-derived metric you build on top of this number.


⚠️ Documented limitation — MOS Doc ID 2899647.1
*"Need To Exclude Denied And Withdrawn Absences From GET_ABSENCE_COUNTS Results"* — Oracle has confirmed this. There is no setting to filter; you have to live with what it returns or switch to Mechanism 4.


📌 Hidden capability most authors miss
Despite the name, the function returns *seven* values via OUT parameters — occurrence count plus six duration totals (days, hours, calendar days, weeks, months, years). If you only read the count, you are throwing away half its value.


✅ Use it for
"Applied for" rules — e.g. *"no more than 5 sick leave applications per quarter, regardless of approval"*. Do **not** use it for consumption arithmetic where withdrawn or denied entries must be excluded.


## Mechanism 3 — GET_ABSENCE_DAYS_PER_TYPE (the opaque sum)


Looks like the obvious answer. Returns days consumed for a given type, in a given window, for a given person. Three arguments, one numeric output, no setup required. The catch is what happens between input and output.


### Scenario from the UI


Run the seeded **Absence Records OTBI report** for the same employee. The "Absence Days" column shows a number, but the report has hidden filters baked into the subject area — you cannot see which entries got included. After the next quarterly upgrade, the same employee might show a different total. `GET_ABSENCE_DAYS_PER_TYPE` has the same problem.


FILTER VISIBILITY · THE OPAQUE-FILTER PROBLEM


















  FILTER VISIBILITY
  The opaque-filter problem


  INPUTS


    person_id



    absence_type_id



    range_start



    range_end












    UNDOCUMENTED
    Internal status filter

    Sums DURATION column
    from ANC_PER_ABS_ENTRIES
    Applies internal filter
    filter rule: not published
    filter rule: not stable






  POSSIBLE OUTPUTS



    SCENARIO A
    Returns 8 days



    SCENARIO B
    Returns 5 days



    NEXT QUARTERLY
    Possibly different






    SOX & AUDIT IMPLICATION
    If you cannot certify what a function does on every release, it is not safe for governance rules. Prefer mechanisms where the filter is visible in your formula text.



**Fig 5 —** The function sums `DURATION` from `ANC_PER_ABS_ENTRIES`, but applies an internal filter that Oracle does not document. The same query against the same data could return a different number after a quarterly upgrade, with no compile error to surface the change.


⚠️ SOX and audit implication
If you cannot certify what a function does on every release, it is not safe for governance rules. Prefer mechanisms where the filter is visible in your formula text.


✅ Use it for
Indicative day totals in management reports or debug logging. Do **not** use it for any rule where state-by-state correctness must be certified or audited.


## Mechanism 4 — Read each entry yourself (recommended)


This is the pattern the previous three mechanisms exist as shortcuts for. Verbose, careful with defaults, deliberate with the iteration. In return, it gives you the only path where the filter logic lives *inside* your formula text and survives quarterly upgrades unchanged.


### Scenario from the UI


Go back to **Existing Absences**. The page first loads a list of absences — just dates and types. To see the duration breakdown, approval history, or comments for any one of them, you click that row. List first, full details one at a time — that is exactly how Oracle exposes live absence data inside Fast Formula.


### The two-step structure


If I had seen this diagram three years ago, I would have saved a lot of compile errors. The DBI dictionary for absence entries is *not* seven parallel arrays you can index by a shared loop counter. It is one list-DBI of entry IDs, plus a set of scalar DBIs that resolve per-entry once you set the right context.


DBI ARCHITECTURE · TWO-STEP MODEL


















  DBI ARCHITECTURE
  Two-tier model: one array of IDs, scalar DBIs resolved per-entry





    SOURCE TABLE
    ANC_PER_ABS_ENTRIES
    Live absence rows. Updated on every Submit, Approve, Withdraw, Update.
    Columns: ABSENCE_ENTRY_ID, ABSENCE_TYPE_ID, START_DATE, END_DATE, ABSENCE_STATUS_CD, APPROVAL_STATUS_CD, DURATION, ...




  resolved by





    TIER 1 · DRIVER ARRAY DBI
    ANC_PER_ABS_ENTRS_ABSENCE_ENTRY_ID_ARR
    → resolved inside CHANGE_CONTEXTS(PERSON_ID, EFFECTIVE_DATE [, START_DATE, END_DATE])



    arr_entry_id =
    [ 300012345, 300012451, 300012612, 300012805 ]




  for each id, set context, then read scalars





    TIER 2 · SCALAR DBIs (per-entry, resolved via inner CHANGE_CONTEXTS)



    CHANGE_CONTEXTS(ABSENCE_ENTRY_ID = 300012345) ( ... read scalars here ... )




      ANC_ABS_ENTRS_ABSENCE_TYPE_ID


      ANC_ABS_ENTRS_START_DATE


      ANC_ABS_ENTRS_END_DATE


      ANC_ABS_ENTRS_DURATION


      ANC_ABS_ENTRS_ABSENCE_STATUS_CD


      ANC_ABS_ENTRS_APPROVAL_STATUS_CD


    Note the prefix shift: ANC_PER_ABS_ENTRS_ for the array, ANC_ABS_ENTRS_ for the scalars. No PER, no _ARR.



**Fig 6 —** The documented Oracle DBI model for live absence entries. **One** array DBI (Tier 1), **six** scalar DBIs (Tier 2). The trap that catches most authors is reaching for parallel `_ARR` siblings — `ANC_PER_ABS_ENTRS_START_DATE_ARR`, `..._APPROVAL_STATUS_CD_ARR`, and so on — which do not exist in the dictionary. Code that references them looks plausible but does not compile.


### Going through the list one entry at a time


Once you have the list of IDs, you walk through it one ID at a time. For each ID, you switch focus to that entry, read its details, decide if it counts, and add to your running total. Then move to the next ID.


FLOWCHART · LIVE-LOOP CONTROL FLOW






















  FLOWCHART · LIVE-LOOP CONTROL FLOW
  Iterating the driver array with proper guards




    START






    Init: g_consumed = 0
    NI = arr.FIRST(-1)







    arr.EXISTS(NI)?
    while-loop guard


   exit -->

  NO


    RETURN total


   set context -->

  YES



    Set ABSENCE_ENTRY_ID ctx
    CHANGE_CONTEXTS(...)






    Read 6 scalar DBIs
    type, dates, status, duration







    Filter:
    type? not-self?
    status valid?


   back to top of loop -->



  NO
  skip entry

   accumulate -->

  YES



    g_consumed +=
    duration










    NI = arr.NEXT(NI, -1)





    Terminal


    Process



    Decision


    Skip path



**Fig 7 —** Loop control flow with proper UML/BPMN symbology. Five distinct guards shape the path: array existence (top diamond), entry-type match, self-exclusion (the entry being validated must not count itself), absence-status filter, and approval-status filter. Failure on any guard skips the entry without aborting the loop.


### Two syntactic landmines


Get these two wrong and your formula will not compile. Both are easy to copy from older blogs that show pre-current syntax.


| Looks plausible · will not compile | Documented Oracle pattern |


| `FIRST_INDEX('N', arr)``NEXT_INDEX('N', arr, i)``WHILE i WAS NOT DEFAULTED`
| `arr.FIRST(-1)``arr.NEXT(i, -1)``WHILE arr.EXISTS(i)`
|


| `EMPTY_NUMBER_DATE`DATE cannot be an index type
| `EMPTY_DATE_NUMBER`format: `EMPTY__`
|


✅ Use it for
Any rule that needs an accurate live balance — real-time validation, audit-grade governance, anything where you need to defend the number. The verbosity is the price; correctness is what you buy.


## Snapshot vs Live — The Architectural Split


The four mechanisms split cleanly across two underlying data sources. This is the diagnostic question to ask before writing any balance formula.


DATA TOPOLOGY · SNAPSHOT VS LIVE














  DATA TOPOLOGY
  Two worlds, periodically reconciled by the absence engine





    SNAPSHOT WORLD
    Updated by batch


  ANC_PER_ACRL_ENTRY_DTLS
  Committed accrual ledger




    Updated only when accrual engine runs

    Lags reality by 12 to 24 hours

    Aggregated, fast, contractually stable

    Reflects only finalised consumption




  CONSUMED BY

  GET_PLAN_BALANCE

  USE WHEN
  Carryover, period-end, opening anchor





    LIVE WORLD
    Updated transactionally


  ANC_PER_ABS_ENTRIES
  Real-time absence collection



    Updated on every Submit / Approve / Withdraw

    Reflects this instant, no lag

    Granular, current, volatile

    No lifecycle filter applied at storage




  CONSUMED BY


    GET_ABSENCE_COUNTS


    GET_ABSENCE_DAYS_PER_TYPE


    DBI driver + scalars · recommended


  Real-time decisions, audit-grade governance



  batch
  reconciles


**Fig 8 —** The two data worlds. The accrual engine periodically reconciles the live collection into the snapshot ledger, but between engine runs the two are out of sync — which is why the same person can have a different "balance" depending on which world your formula reads.


📌 Diagnostic question
If a user submits an absence and immediately submits a second one, does my formula need to *see* the first submission? If yes — live world. If no — snapshot world is fine, and the simpler `GET_PLAN_BALANCE` path is appropriate.


## The Status-Code Naming Trap


Of all the silent bugs in this domain, this one accounts for more support tickets than the rest combined. Two columns describe an absence's status. They use *different* naming conventions. A filter that looks correct against one column is a no-op against the other.


DIAGNOSTIC · THE STATUS-CODE NAMING TRAP










  DIAGNOSTIC
  Two status columns, two naming conventions, one common bug





    ABSENCE_STATUS_CD


  LOOKUP FRAMEWORK
  ANC_PER_ABS_ENT_DISPLAY_STATUS
  Display lookup for the absence lifecycle column

  PREFIX CONVENTION


    ORA_


  STORED VALUES

    ORA_SUBMITTED
    ORA_COMPLETED
    ORA_WITHDRAWN
    ORA_IN_PROGRESS






    APPROVAL_STATUS_CD


  LOOKUP FRAMEWORK
  AMX approval framework
  Workflow status maintained by the AMX engine

  PREFIX CONVENTION


    (none)


  STORED VALUES

    SUBMITTED
    APPROVED
    WITHDRAWN
    DENIED





    THE COMMON BUG

    IF arr_app_status[i] <> 'ORA_WITHDRAWN' THEN  ...



    Always TRUE. APPROVAL_STATUS_CD never carries the ORA_ prefix.
    The filter is silently a no-op. Withdrawn entries pass through. The formula compiles and ships.



**Fig 9 —** The asymmetry is structural — the two columns originate in different framework layers and follow different conventions. There is no Oracle plan to reconcile them. The defensive practice is to filter on both columns with both naming conventions, every time.


⚠️ The bug everyone ships at least once
Writing `IF arr_app_status[i] <> 'ORA_WITHDRAWN'` on the approval column is always TRUE — because that column never carries the `ORA_` prefix. The filter is a silent no-op. Withdrawn entries pass through. The formula compiles and ships.


📌 Edge case worth knowing — MOS 2624787.1
The two columns can drift in administrative-cancellation paths. An absence reaching `ABSENCE_STATUS_CD = 'ORA_COMPLETED'` can be retroactively cancelled in error/expiry flows such that only `APPROVAL_STATUS_CD` updates. A two-pronged filter catches both paths; a single-column filter misses them.


The defensive pattern, every time:


```
IF abs_status <> 'ORA_WITHDRAWN'
   AND app_status <> 'WITHDRAWN'
   AND app_status <> 'DENIED' THEN
  /* this entry counts towards consumption */
END IF
```


## The Composite Pattern — Snapshot Anchor + Live Loop


For accurate live balance, the working practitioner pattern combines two of the four mechanisms. `GET_PLAN_BALANCE` gives you the starting balance. Mechanism 4 gives you the live adjustment. The result is a balance that is both contractually stable and current to this instant.


COMPOSITE PATTERN · END-TO-END


















  COMPOSITE PATTERN
  Snapshot anchor + early-exit guard + live loop = correct balance






    1
    SNAPSHOT ANCHOR

    GET_PLAN_BALANCE
    ('AL Plan')

    opening = 5.0









    2
    EARLY-EXIT GUARD

    IF opening
    THEN return 0

    skip live loop




  if 0








    3
    LIVE LOOP

    Driver array → scalars
    → filter → accumulate

    consumed = 3.0









    4
    RECONCILE

    live = opening
    - consumed

    live = 2.0









    RETURN g_live_balance





    PERFORMANCE NOTE
    In Q4 peak load, ~30% of employees
    have exhausted balance and exit at step 2.



**Fig 10 —** The composite pattern, end-to-end. Step 2 is not just hygiene — on plans with high consumption rates it short-circuits a non-trivial fraction of formula executions, which matters at year-end peak load.


### The Production-Ready Recipe


Below is the full reader. It returns `g_live_balance` for whatever calling formula type wraps it — Entry Validation will use it to drive a `VALID`/`ERROR_MESSAGE` decision, a Plan Use Rate formula will use it to compute deduction, a Type Duration formula will use it to constrain the duration calculation. Only the way you consume the final number changes.


```
/******************************************************************
  RECIPE  : LIVE_ABSENCE_BALANCE_READER
  PURPOSE : Return live balance = snapshot anchor minus
            in-flight consumption, using documented Oracle
            DBI patterns.
  USE IN  : Any Absence FF type that needs accurate live
            balance (Entry Validation, Plan Use Rate,
            Type Duration, custom Accrual logic, etc.).
******************************************************************/

/* A. DEFAULTS — input contexts */
DEFAULT FOR EFFECTIVE_DATE              IS '4712/12/31' (date)
DEFAULT_DATA_VALUE FOR PERSON_ID        IS 0
DEFAULT_DATA_VALUE FOR ABSENCE_ENTRY_ID IS -1

/* B. DEFAULTS — the list-DBI (Step 1) */
DEFAULT FOR ANC_PER_ABS_ENTRS_ABSENCE_ENTRY_ID_ARR
                                        IS EMPTY_NUMBER_NUMBER

/* C. DEFAULTS — the per-entry scalars (Step 2) */
DEFAULT FOR ANC_ABS_ENTRS_ABSENCE_TYPE_ID    IS 0
DEFAULT FOR ANC_ABS_ENTRS_START_DATE         IS '1900/01/01' (date)
DEFAULT FOR ANC_ABS_ENTRS_END_DATE           IS '4712/12/31' (date)
DEFAULT FOR ANC_ABS_ENTRS_ABSENCE_STATUS_CD  IS 'ORA_COMPLETED'
DEFAULT FOR ANC_ABS_ENTRS_APPROVAL_STATUS_CD IS 'APPROVED'
DEFAULT FOR ANC_ABS_ENTRS_DURATION           IS 0

INPUTS ARE iv_target_type_id (number), iv_window_start (date)

/* D. CONTEXT INIT */
l_self_entry_id = GET_CONTEXT(ABSENCE_ENTRY_ID, -1)
l_person        = GET_CONTEXT(PERSON_ID, 0)
l_eff_date      = GET_CONTEXT(EFFECTIVE_DATE, iv_window_start)
c_plan_name     = 'Annual Leave Plan'

/* E. SNAPSHOT ANCHOR */
g_opening = GET_PLAN_BALANCE(c_plan_name)

/* F. EARLY-EXIT GUARD */
IF g_opening  l_self_entry_id THEN
    (
      IF l_abs_status <> 'ORA_WITHDRAWN' THEN
      (
        IF l_app_status <> 'WITHDRAWN'
           AND l_app_status <> 'DENIED' THEN
        (
          g_consumed = g_consumed + l_duration
        )
      )
    )
  )

  NI = arr_entry_id.NEXT(NI, -1)
)

/* I. RECONCILE */
g_live_balance = g_opening - g_consumed
IF g_live_balance ✅ What this recipe covers
**Snapshot anchor** — `GET_PLAN_BALANCE` for the stable starting number. **Early-exit guard** — cheap short-circuit when nothing remains to subtract from. **Step 1 + Step 2 DBI pattern** — list of IDs, then per-entry scalar reads inside `CHANGE_CONTEXTS`. **Self-exclusion** — the entry being validated does not count itself. **Both-column status filter** — ORA_ on lifecycle, no prefix on approval. **Reconciliation** — floor at zero. Every guard is explicit and auditable.


## Anti-Pattern Catalogue — Five Mistakes That Ship Silently


If you have written Absence Fast Formulas long enough, you have seen all five — usually in code you wrote yourself a year earlier. Numbers 1, 3, and 4 surface as compile errors or empty results eventually. Numbers 2 and 5 are the silent ones — the formula compiles, runs, and returns subtly wrong numbers.


ANTI-PATTERN CATALOGUE










  FIVE WAYS TO SHIP A SILENT BUG
  Anti-pattern catalogue





    1
    Three-arg call to GET_PLAN_BALANCE
    GET_PLAN_BALANCE(person, plan, date)

    FIX
    GET_PLAN_BALANCE('Annual Leave Plan')
    Person/date are contexts, not arguments






    2
    Indexing parallel _ARR DBIs that don't exist
    arr_status[i] = ANC_PER_ABS_ENTRS_..._CD_ARR

    FIX
    Only entry-id has _ARR. Read scalars inside
    CHANGE_CONTEXTS(ABSENCE_ENTRY_ID = ...)






    3
    Phantom iteration verbs
    i = FIRST_INDEX('N', arr)
    WHILE i WAS NOT DEFAULTED LOOP

    FIX
    i = arr.FIRST(-1)
    WHILE arr.EXISTS(i) LOOP






    4
    Wrong empty-array constant
    DEFAULT FOR arr IS EMPTY_NUMBER_DATE
    DATE cannot be an index type

    FIX
    EMPTY_DATE_NUMBER
    Format: EMPTY__






    5
    Single-column status filter
    IF arr_app_status[i] <> 'ORA_WITHDRAWN' THEN  ← always TRUE, no-op

    FIX
    IF abs_status <> 'ORA_WITHDRAWN'
    AND app_status <> 'WITHDRAWN'
    AND app_status <> 'DENIED' THEN
    Both columns, both prefix conventions, every time.



**Fig 11 —** The five highest-frequency anti-patterns in this domain. Numbers 1, 3, and 4 are syntactic and surface eventually as compile errors or empty results. Numbers 2 and 5 are silent — the formula compiles and runs, returning subtly wrong numbers.


## The 30-Second Checklist


If your absence formula compiles cleanly but returns the wrong number, walk this checklist in order.


| # | Check | Where |


| 1 | Mechanism matches use case (snapshot vs live) | This post — sections on Mechanism 1 vs 4 |

| 2 | `GET_PLAN_BALANCE` called with one argument, not three | Inside the formula |

| 3 | List-DBI prefix `ANC_PER_ABS_ENTRS_` · scalar prefix `ANC_ABS_ENTRS_` | Inside the formula |

| 4 | Iteration uses `arr.FIRST(-1)` / `arr.EXISTS(i)` / `arr.NEXT(i, -1)` | Loop body |

| 5 | Empty-array default uses `EMPTY__` format | DEFAULT FOR section |

| 6 | Both `ABSENCE_STATUS_CD` and `APPROVAL_STATUS_CD` filtered, with their own prefix conventions | Filter chain |

| 7 | Self-exclusion guard (`l_entry_id <> l_self_entry_id`) | Filter chain — only inside Entry Validation |

| 8 | Snapshot anchor + early-exit guard if performance matters | Step E and F of the recipe |


## Quick Reference Card


| Function | Source | Filter Behaviour | Use For |


| `GET_PLAN_BALANCE` | Snapshot ledger | Only finalised consumption | Carryover, reporting, snapshot anchor |

| `GET_ABSENCE_COUNTS` | Live entries | No filter (MOS 2899647.1) | "Applied for" occurrence rules |

| `GET_ABSENCE_DAYS_PER_TYPE` | Live entries | Hidden internal filter | Indicative reports only |

| List-DBI + per-entry scalars | Live entries | Filter visible in your formula | Real-time, audit-grade rules |


## Key Takeaways


**Pick the mechanism by use case, not by familiarity.** The default function (`GET_PLAN_BALANCE`) is right for snapshot questions and wrong for live ones. Reaching for it by reflex is the most common reason Entry Validation rules break in production.


**The DBI model is two-step, not parallel arrays.** One list of entry IDs (Step 1), then per-entry scalar reads inside `CHANGE_CONTEXTS(ABSENCE_ENTRY_ID = ...)` (Step 2). Code written against parallel `_ARR` siblings does not match the published dictionary — will not compile.


**Both status columns, both prefix conventions.** `ABSENCE_STATUS_CD` uses the `ORA_` prefix; `APPROVAL_STATUS_CD` does not. Filter on both, every time, regardless of how confident you are that the entries you care about only ever update one column.


**The composite recipe is the production pattern.** Snapshot anchor + early-exit guard + live loop + reconcile. Drop it in, replace the plan name and the input parameters, and you have a balance reader you can defend in audit.


Next in this series: the equivalent function reference for OTL Time Entry Rules — where the live data lives in the `HWM_*` schema, the available functions are substantially different, and the lifecycle states map onto a different framework altogether.


AM


Abhishek Mohanty


Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time and Labor, Core HR, Redwood, HDL, OTBI.


Fast Formula
Absence Management
GET_PLAN_BALANCE
GET_ABSENCE_COUNTS
CHANGE_CONTEXTS
DBI
Oracle HCM 26A