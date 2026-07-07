---
title: "Oracle Fast Formula: Time Entry Rule (Part 2)"
description: "Oracle Fast Formula: Time Entry Rule (Part 1) — Inputs, Contract, and Architecture"
pubDate: 2026-05-22
tags: ["Fast Formula", "Oracle HCM Cloud", "TER", "Time Entry Rule", "OTL"]
---

Oracle Fast Formula: Time Entry Rule (Part 1) — Inputs, Contract, and Architecture
- Fast Formula
  Time Entry Rule
  OTL
  Hands-On


May 21, 2026 • 15 min read • Oracle HCM Cloud


  The TER Series
  Part 2 of 4

    1. OTL Foundations ·
    2. The Input Contract ·
    3. Algorithm: Routing & Overlap ·
    4. The State Machine



# The Input Contract: How OTL Hands Data to Your FormulaPart 2 of 4 — The TER Series


  AM

    Abhishek Mohanty
    Oracle ACE Apprentice · AIOUG Member · Oracle HCM Cloud Consultant & Technical Lead



In Part 1 we saw what TER does and where it fits in OTL's submission flow. Now we look at the data the framework hands your formula — the input array contract, the seven input variables, and the naming conventions that keep production code readable.


## The Input Array Contract


Here's the single most important thing to internalise before you write any code: **the timecard the worker sees is not the timecard your formula receives**. OTL inserts extra rows between the worker's entries to mark structural boundaries — where each day starts, where it ends, where the whole period closes out. Miss this distinction and your loop counter, your day-buffer logic, and your `.exists()` guards will all be subtly wrong. Get it right, and the rest of the formula falls into place naturally.

I'll show you both views, then a transformation diagram that bridges them, then the formal contract.


### The view the worker sees


When Sarah opens her timecard, she's looking at a spreadsheet-like grid. She types entries one row at a time. Here's what her week looks like after she's done entering Tuesday and Wednesday:



    My_Timecard_Week_14Apr2026.xlsx
    Excel




         
        Date
        Time Type
        Start Time
        Stop Time
        Hours




        1
        14-Apr-2026 (Tue)
        Regular Hours
        09:00
        12:00
        3.0


        2
        14-Apr-2026 (Tue)
        Meal Break
        12:00
        13:00
        1.0


        3
        14-Apr-2026 (Tue)
        Regular Hours
        13:00
        18:00
        5.0


        4
        15-Apr-2026 (Wed)
        Regular Hours
        09:00
        18:00
        8.0




Four entries across two days — this is exactly what Sarah types into OTL. Clean, simple, no surprises.


### What OTL does between submission and your formula


The moment Sarah hits Submit, OTL's pre-processor wakes up. It can't just hand the formula four rows of data — the formula needs to know where day boundaries fall, where the period ends, and where to pause for day-level processing like overlap detection. So OTL inserts **marker rows** at the structural breakpoints. The diagram below shows exactly what changes:


  From Worker's View to Formula's View
  OTL injects three kinds of markers before your formula runs


  WORKER'S VIEW · 4 rows
  What Sarah sees on the timecard screen




    Row 1
    Tue 14-Apr · Reg Hours · 09:00–12:00


    Row 2
    Tue 14-Apr · Meal Break · 12:00–13:00


    Row 3
    Tue 14-Apr · Reg Hours · 13:00–18:00


    Row 4
    Wed 15-Apr · Reg Hours · 09:00–18:00





    OTL inserts
    markers



  FORMULA'S VIEW · 8 indexes
  What your TER formula receives via INPUTS ARE




    [1] HEADER
    Marker · "timecard begins"



    [2]  —  (was Row 1)
    Reg Hours · 09:00–12:00



    [3]  —  (was Row 2)
    Meal Break · 12:00–13:00



    [4]  —  (was Row 3)
    Reg Hours · 13:00–18:00



    [5] END_DAY
    Marker · "Tuesday is complete — run day-level checks now"



    [6]  —  (was Row 4)
    Reg Hours · 09:00–18:00 (Wed)



    [7] END_DAY
    Marker · "Wednesday is complete — run day-level checks now"



    [8] END_PERIOD
    Marker · "Whole timecard is complete — loop ends"










  KEY INSIGHT
  The worker's "row 1" is the formula's "index [2]". Always remember the offset — loop counters start at 1 because of the HEADER.








Three things to take away from this diagram:


  **HEADER always sits at index [1].** Your loop counter starts at 1, but you'll never read real worker data at that index. The first real entry begins at [2].

  - **END_DAY appears wherever a calendar day ends.** If the timecard period covers seven days, expect seven END_DAY markers (one for each day, even if some days have zero worker entries).

  - **END_PERIOD always sits at the very last index.** When your formula's loop sees END_PERIOD, you're done.


Here's the same eight-row view as a table, with the original column names OTL uses:


### The view the formula sees, as a table




    As_The_Formula_Sees_It.xlsx
    Excel




    | Idx
        | Record Position
        | Time Type
        | Start Time
        | Stop Time
        | Hours
      |




        | [1]
        | **HEADER**
        | —
        | —
        | —
        | —
      |


        | [2]
        | —
        | Regular Hours
        | 09:00
        | 12:00
        | 3.0
      |


        | [3]
        | —
        | Meal Break
        | 12:00
        | 13:00
        | 1.0
      |


        | [4]
        | —
        | Regular Hours
        | 13:00
        | 18:00
        | 5.0
      |


        | [5]
        | **END_DAY**
        | —
        | —
        | —
        | —
      |


        | [6]
        | —
        | Regular Hours
        | 09:00
        | 18:00
        | 8.0
      |


        | [7]
        | **END_DAY**
        | —
        | —
        | —
        | —
      |


        | [8]
        | **END_PERIOD**
        | —
        | —
        | —
        | —
      |





Same four entries, now wrapped with HEADER, END_DAY, and END_PERIOD marker rows. Notice the dashes — marker rows have no time-type, no punches, no hours. Trying to read those slots will crash your formula.


### How the formula reads it — three questions per row


For every index from [1] to [N], your formula asks the same three questions in order. The answers determine the entire flow of validation logic:


**Question 1: Is this a marker row?** Read `RECORD_POSITIONS[idx]`. If it's HEADER, skip everything; if it's END_DAY, run day-level checks (overlap detection, day buffer reset); if it's END_PERIOD, the loop ends; if it's empty, this is a real worker entry — proceed to Question 2.


**Question 2: What kind of time type?** Read `PayrollTimeType[idx]`. Regular Hours go through the continuous-work tracker and the day buffer for overlap testing. Meal Break runs through the schedule-window check and signals "the worker took a break." Other types (Annual Leave, Sick Leave) typically pass through with no validation.


**Question 3: What are the exact punch times?** Read `StartTime[idx]` and `StopTime[idx]`. Use them for stretch tracking, overlap math, qty-only detection, and any time-window checks.



Production trap

  Marker rows are why you can't read input arrays directly. `StartTime[1]` doesn't exist as a value — HEADER rows have no punch time. Read it without protection and Fast Formula throws a runtime error and crashes the whole submission. Every read in the formula must be wrapped in `.exists()`:


IF (StartTime.exists(nidx)) THEN ( aiStartTime = StartTime[nidx] )


  Skip this guard and the formula passes UAT cleanly — test data rarely covers the edge case — then breaks day one in production when a real submission arrives. **This is the single most common reason a TER formula goes live and immediately blocks every submission**. Don't be that consultant.


### The Formula's Contract: What Goes In, What Comes Out


A Time Entry Rule formula is like a checkpoint at the airport. The OTL framework hands it a stack of paperwork (the timecard rows), the formula inspects every page, and hands back a list of which pages have problems. The framework defines exactly what shape that paperwork arrives in and exactly what shape the response must take — that's the **contract**. Neither side can deviate.




    The_Contract_at_a_Glance.xlsx
    Excel




    | Direction
        | Variable
        | Type
        | What it represents
      |




        | **IN**
        | `HWM_CTXARY_RECORD_POSITIONS`
        | Text array
        | Which rows are markers (HEADER, END_DAY) vs real entries
      |


        | **IN**
        | `HWM_CTXARY_HWM_MEASURE_DAY`
        | Number array
        | Day-aggregated total (declared but unused by this formula)
      |


        | **IN**
        | `measure`
        | Number array
        | Hours value for each row
      |


        | **IN**
        | `PayrollTimeType`
        | Text array
        | What kind of time (Regular Hours, Meal Break, Annual Leave...)
      |


        | **IN**
        | `StartTime`
        | Date array
        | Punch-in timestamp for each row
      |


        | **IN**
        | `StopTime`
        | Date array
        | Punch-out timestamp for each row
      |


        | **OUT**
        | `OUT_MSG`
        | Text array (sparse)
        | Error message for each flagged row, empty for clean rows
      |





Six inputs in. One output out. The framework enforces these names exactly — misspell one, omit one, return anything else, and the formula won't even compile.


#### Three things to understand before reading further


Before walking through each input one by one, hold these three properties in mind. Every line of code in this formula respects all three; understanding them now means the source reads naturally later.



Diagram · The three properties of the input/output shape




    PROPERTY 1 · Six parallel arrays, not records — one row spans six columns at the same index





      Idx



      RECORD_POSITIONS

      PayrollTimeType

      StartTime

      StopTime

      measure

      HWM_MEASURE_DAY



      [3]


      empty

      Meal Break

      12:00

      13:00

      1.0

      unused


    To work with row 3, the formula reads RECORD_POSITIONS[3], PayrollTimeType[3], StartTime[3]...
    across all six arrays. There's no single row object — each row is reassembled at read time from the parallel slices.


    PROPERTY 2 · Not every row populates every column — marker rows are sparse




      Idx


      RECORD_POSITIONS

      All other arrays (PayrollTimeType, StartTime, StopTime, measure, HWM_MEASURE_DAY)



      [1]

      HEADER

      missing — reading any of these crashes with FFL-09100



      [2]

      empty

      all populated — safe to read



      [5]

      END_DAY

      missing — reading any of these crashes with FFL-09100


    Every read in the formula must be wrapped in .exists(nidx) — check first, then read.



    IF (StartTime.exists(nidx)) THEN aiStartTime = StartTime[nidx]


    PROPERTY 3 · The output is sparse, not dense — only flagged rows get an entry




      5 timecard rows


      [1] HEADER — clean


      [2] Reg 09—12 — clean


      [3] Meal — outside hours


      [4] Reg — overlaps row 2


      [5] END_DAY — clean


      - flag rows
      3 and 4 only


      OUT_MSG · only 2 entries


      [1]

      no entry — row stayed clean


      [2]

      no entry — row stayed clean


      [3]

      "Break outside working hours"


      [4]

      "Overlapping entries"


      [5]

      no entry — row stayed clean


    The framework reads OUT_MSG when the formula returns and renders red error markers on whatever indexes appear.
    Quiet rows stay quiet. Clean rows have nothing to say — so they say nothing.



    SUMMARY:
    Six parallel arrays in. One sparse array out. Wrap every read in .exists().
    Internalise these three properties — the entire formula source is a direct expression of them.










**1. The inputs are parallel arrays, not records.** Most languages would express a row of timecard data as a single object with named fields: `{type, start, stop, hours}`. Fast Formula doesn't have records like that. Instead, the framework gives the formula six separate arrays, all sharing the same row index. Row 3 of the timecard is `RECORD_POSITIONS[3]`, `StartTime[3]`, `StopTime[3]`, `PayrollTimeType[3]`, and `measure[3]`, each holding one column of that row's data. To work with a single row, you read the same index across all six arrays.

**2. Not every row populates every column.** Marker rows (HEADER, END_DAY, END_PERIOD) only fill `RECORD_POSITIONS` — the other arrays have no slot at those indexes. Trying to read `StartTime[1]` on a HEADER row would crash. This is why every read in the formula is wrapped in `.exists(nidx)` — the formula has to check whether a slot is populated before reading from it.

**3. The output is sparse, not dense.** `OUT_MSG` doesn't have one entry per timecard row — it only has entries for the rows the formula chose to flag. A clean row leaves its slot empty. The framework reads `OUT_MSG` when the formula returns and renders red error markers next to whatever row indexes appear in the array. Quiet rows stay quiet.


#### The expert's view: framing the inputs before reading the names


  Expert framing
  When I'm reviewing a junior developer's first TER formula, the question I always hear is: *"Why are some inputs called `HWM_CTXARY_RECORD_POSITIONS` and others just `StartTime`?"* The answer isn't really about names — it's about **what kind of data each input represents**, and Oracle's naming conventions reflect that distinction once you see the pattern.
  Fast Formula isn't a general-purpose programming language. It's a **rule engine plugged into specific HCM modules**. Each module (Payroll, Absence, Time and Labor, Benefits) defines its own *formula types*, and each formula type is a contract: *"If you write a formula of this type, you'll receive these inputs and you must return these outputs."* The TER formula type is one such contract, defined inside OTL. The six inputs we're about to dissect aren't arbitrary — they're exactly what OTL's validation pipeline hands every TER formula by design.


#### How a TER formula fits into OTL's bigger picture


To understand the inputs, you first need to see where the formula fires within OTL. A TER formula doesn't run in isolation — it sits inside a five-stage pipeline that begins the moment a worker clicks Submit on their timecard:


  OTL Validation Pipeline — Where TER Formulas Run
  Five stages from worker submission to UI feedback. The TER formula fires in Stage 3.




  STAGE 1
  Worker submits
  Timecard rows
  leave the UI







  STAGE 2
  OTL pre-processes
  Inserts markers,
  shapes data into arrays







  STAGE 3 · YOUR FORMULA
  TER formula runs
  Reads the 6 input arrays,
  populates OUT_MSG,
  returns to OTL







  STAGE 4
  OTL collects results
  Reads OUT_MSG,
  aggregates with other rules







  STAGE 5
  UI renders feedback
  Red error markers
  on flagged rows




  ZOOM: STAGE 3 INTERNAL FLOW — What your formula does between input and output

  1.  Receive the six input arrays from OTL (read-only)
  2.  Initialise OUT_MSG as an empty array (will hold error messages)
  3.  Loop through every row index from 1 to N
  • Read all six arrays at the current index (parallel read)
  • Apply your validation logic (overlap, continuous-hours, etc.)
  • If anything fails, write a message into OUT_MSG[idx]
  4.  When the loop finishes, OTL reads OUT_MSG and acts on it

  The 6 inputs and 1 output define the contract. Everything else is your logic.









Stage 3 is where your formula has agency. Stages 1, 2, 4, and 5 belong to OTL. The contract you're working against is: *OTL gives you six well-defined arrays; you give back one well-defined array; everything else is your business logic.*


#### Decoding the input names — what each part means


Now that we know *where* the inputs come from, let's decode *why they're named the way they are*. Oracle's naming is structural, not arbitrary. Every prefix carries meaning. Here's the breakdown:


  Anatomy of the Input Names
  Reading the prefix tells you what kind of data the input represents


  Long-prefix names — structural metadata from OTL's framework







    HWM_
    CTXARY_
    RECORD_POSITIONS



    "HWM"
    HCM Workforce
    Management


    "CTXARY"
    Context Array
    (per-row metadata)


    "RECORD_POSITIONS"
    What this array actually holds
    (marker text per row)


  Read aloud: "HCM Workforce Management's context array of record positions"





  Short-name inputs — per-row time data
  No prefix needed — these are the original TER inputs from OTL's earliest design




    measure
    Hours value
    per row


    PayrollTimeType
    Time-type label
    per row


    StartTime
    Punch-in
    timestamp per row


    StopTime
    Punch-out
    timestamp per row




  KEY INSIGHT
  Long-prefix inputs carry structural metadata (where in the timecard structure are we?).
  Short-name inputs carry the actual time data (what did the worker enter on this row?).


Once you see this split, the naming makes sense. The `HWM_CTXARY_` prefix is Oracle saying *"this input is structural metadata that the framework needs to manage the iteration."* The short names (`measure`, `PayrollTimeType`, `StartTime`, `StopTime`) are saying *"this input is the worker's actual time data, the same names we've used since the OTL was first designed."*


  Expert insight
  You'll see this same `HWM_` prefix convention across other OTL formula types too — calculation rules, time-calculation formulas, time-card validation formulas. Once you internalise that `HWM_` means "framework-supplied" and `HWM_CTXARY_` means "framework-supplied per-row metadata", you can read any OTL formula and immediately know which variables come from the framework versus which ones the author created. **This pattern recognition is what separates a fluent OTL developer from someone still puzzling over the syntax.**


#### How to read one timecard row from the parallel arrays


Now the practical part. Inside the formula's loop, each iteration processes one row. To get all the data for that row, you read all six arrays at the same index. Here's a visual showing how the parallel arrays line up:


  Six arrays, one shared index space
  Read all six at index [3] to reconstruct row 3 of Sarah's timecard



  Idx



  HWM_CTXARY_
  RECORD_POSITIONS


  HWM_CTXARY_
  HWM_MEASURE_DAY


  measure


  PayrollTimeType


  StartTime


  StopTime



  [1]


  HEADER


  —


  —


  —


  —


  —



  [2]


  (empty)


  6.25


  1.5


  Regular Hours


  08:30


  10:00



  [3]


  (empty)


  6.25


  4.75


  Regular Hours


  10:00


  14:45



  [4]


  END_DAY


  —


  —


  —


  —


  —



  ← current iteration (nidx = 3)



  /* read all six arrays at index 3 to reconstruct row 3 */
  aiRecPos     = HWM_CTXARY_RECORD_POSITIONS[3]   // '' (empty)
  aiMeasureDay = HWM_CTXARY_HWM_MEASURE_DAY[3]    // 6.25 (not used)
  aiMeasure    = measure[3]                       // 4.75
  aiTimeType   = PayrollTimeType[3]               // 'Regular Hours'









Six arrays, six reads, one row reconstructed. The formula's WHILE loop does this on every iteration, walking the index from 1 to N (where N is the total row count returned by `HWM_CTXARY_RECORD_POSITIONS.count`). On marker rows like [1] and [4], several of the reads return empty — which is why each read in the formula is wrapped in a `.exists()` guard.


  Practitioner's tip
  When debugging a TER formula in production, the first thing I check is the `HWM_CTXARY_RECORD_POSITIONS` array length. If `.count = 0`, the formula received nothing to validate — the bug is upstream in the OTL configuration, not in your formula logic. If `.count` is non-zero but no validations fire, your loop counter or your `.exists()` guards are wrong. **Always log `.count` at the top of the formula via `add_rlog`** — it'll save you hours of guessing.


#### Now: each input in detail


With the framing in place — how the formula fits in OTL's pipeline, what the names mean, how parallel access works — the cards below cover all six inputs (plus the `OUT_MSG` output) one by one. Each card shows what kind of values the input holds, the actual formula code that reads it, and what the formula does with the value.



    Input 01 · Text Array
    HWM_CTXARY_RECORD_POSITIONS

  "What kind of row is this?"

    RECORD_POSITIONS_examples.xlsxExcel

      Possible valueMeaning

        (empty)Real worker entry — check the data columns
        **HEADER**System marker at the top of the timecard
        **END_DAY**System marker at the end of each day — trigger day-level work
        **END_PERIOD**System marker at the end of the whole timecard period



  Four possible values. Empty means real data; non-empty is a system-inserted marker telling the formula something about structure.


    Diagram · Where each marker value appears in the array






        [1]
        HEADER



        [2]
        empty



        [3]
        empty



        [4]
        empty



        [5]
        END_DAY



        [6]
        empty



        [7]
        END_DAY



        [8]
        END_PERIOD



        Always at [1]
        Skip silently


        Day 1 entries
        Process normally


        Trigger Block 7
        Day-level work


        Day 2 entries


        Trigger Block 7


        Loop ends
        Always last index




        How the formula reads RECORD_POSITIONS:

        aiRecPos = RECORD_POSITIONS[nidx]
        IF aiRecPos = 'END_DAY' OR aiRecPos = 'END_PERIOD' THEN ...
        /* HEADER is silently skipped — no branch needed */





How the formula reads it/* read the marker for this index */
IF (HWM_CTXARY_RECORD_POSITIONS.exists(nidx)) THEN
  aiRecPos = HWM_CTXARY_RECORD_POSITIONS[nidx]

/* branch on what kind of row this is */
IF (aiRecPos = 'END_DAY'
    OR aiRecPos = 'END_PERIOD') THEN
  /* run pairwise overlap, reset day buffer */
  Empty value at this index → real worker entry, so the formula reads the data columns. Non-empty (HEADER, END_DAY, END_PERIOD) → system marker, so skip the data columns and trigger boundary logic if applicable. **This is the first thing the formula reads every iteration** — it decides everything else.



    Input 02 · Number Array · Reserved
    HWM_CTXARY_HWM_MEASURE_DAY

  "Is this input actually used?" — **No, but it must be declared.**


    Diagram · The "declared but unused" pattern





      REQUIRED · INPUTS ARE declaration

      INPUTS ARE
      HWM_CTXARY_RECORD_POSITIONS,

      HWM_CTXARY_HWM_MEASURE_DAY,
      measure, PayrollTimeType,
      StartTime, StopTime

      ✓ Must be present
      Otherwise framework throws
      a binding error at runtime




      FORMULA BODY · never reads it

      Block 1 — DEFAULT FOR
      /* not referenced */

      Block 6 — per-line read
      /* not referenced */

      Block 7 — day-level work
      /* not referenced */

      Block 8 — state machine
      /* not referenced */



      contract gap
      declare, ignore



      Required by contract · Read by zero blocks · Pure compliance checkbox





    This input would hold day-level totals if the formula needed them. The framework hands it over because the TER formula type's contract requires it — **but this particular formula never reads it**. Three things to know:

      **You must declare it** in the `INPUTS ARE` statement, otherwise the framework throws a binding error and the formula won't even start.

      - **You don't read from it.** The validations work entirely off per-row punches (`StartTime`, `StopTime`) and per-row `measure`, never from day-level aggregates.

      - **You can ignore it from here on.** It plays no role in any of Block 6, 7, or 8. A different formula type (like a calculation rule) might consume it; this one simply lists it and moves on.









Input 03 · Number Array


measure




"How many hours on this row?"




measure_examples.xlsxExcel



      | Sample value | What it represents |


        | 2.5 | 2 hours 30 minutes — real punch interval |

        | 8.0 | 8 hours — could be real or a qty-only placeholder |

        | 0.5 | 30 minutes — short break or partial shift |

        | (no value) | Marker rows have no `measure` — not applicable |







Always a number when present. The same value can come from real punches or from a qty-only placeholder — `measure` alone can't tell which.





Diagram · Real punches vs qty-only — same measure, different intent






      CASE 1 · REAL PUNCHES

      Worker entered:

      Reg Hours · 09:00 → 17:00

      Framework gives the formula:

      StartTime[i] = 09:00
      StopTime[i]  = 17:00
      measure[i]   = 8.0

      ✓ Use punches directly
      measure is just StopTime − StartTime




      CASE 2 · QTY-ONLY PLACEHOLDER

      Worker entered:

      Reg Hours · 8 hours (no punches)

      Framework gives the formula:

      StartTime[i] = 00:00 ← fake
      StopTime[i]  = 23:59 ← fake
      measure[i]   = 8.0  ← the truth

      ✗ Punches are placeholders
      Trust measure, ignore the punches



      Detection: if StartTime ≈ 00:00 AND StopTime ≈ 23:59 → this is qty-only







How the formula reads it/* per-line measure, used for qty-only entries */
IF (measure.exists(nidx)) THEN
  aiMeasure = measure[nidx]


**The formula uses this mainly for qty-only detection.** If a worker types just "8 hours" without entering punch times, OTL fills `StartTime` as `00:00` and `StopTime` as `23:59` — the `measure` tells you the real intended hours (8) without needing to compute it from the placeholder punches. When the punches are genuine, `measure` simply equals `StopTime − StartTime` in hours, and the formula uses the punches directly anyway.





Input 04 · Text Array · Routing Key


PayrollTimeType




"What kind of time?"




PayrollTimeType_routes.xlsxExcel



      | Time type value | Where the formula sends it |


        | Regular Hours | Stretch tracker + Day buffer for overlap |

        | Meal Break | Schedule-window check + Reset stretch |

        | Annual Leave | Skipped — no validation path |

        | Sick Leave | Skipped — no validation path |

        | Public Holiday | Skipped — no validation path |







The string value drives the entire routing decision. Reg Hours and Meal Break have validation paths; everything else falls through silently.





Diagram · Time-type values fan out to validation paths





      aiTimeType
      a string value per row





      "Regular Hours"
      → Stretch tracker + Day buffer (overlap)




      "Meal Break"
      → Schedule-window check + reset stretch




      "Annual Leave"
      → (skipped — no path)




      "Sick Leave"
      → (skipped — no path)




      "Public Holiday"
      → (skipped — no path)


      = p_reg_type
      = p_break_type














How the formula reads it/* read the type, then route */
IF (PayrollTimeType.exists(nidx)) THEN
  aiTimeType = PayrollTimeType[nidx]

IF (aiTimeType = p_reg_type) THEN
  /* → stretch tracker + day buffer */

IF (aiTimeType = p_break_type) THEN
  /* → schedule window + reset stretch */


The most important routing decision in the formula. Reg Hours go into the continuous-stretch tracker and the day buffer for overlap testing. Meal Break runs through the schedule-window check and resets the stretch tracker. Other types (Annual Leave, Sick, etc) silently skip both paths.





Input 05 · Date Array


StartTime




"When did this row begin?"




StartTime_uses.xlsxExcel



      | Used in | What for |


        | Stretch tracker | Compared to previous stretchEnd → decide EXTEND or RESTART |

        | Pairwise overlap test | Combined with StopTime to define each row's interval |

        | Schedule window check | Compared to `p_sched_start` for Meal Break entries |

        | Qty-only detection | If start



      TIMESTAMP ANATOMY:
      14-Apr-2026 10:00:00
      A single value combining date AND time of day. Fast Formula's DATE type holds both — you don't get them as separate fields.



      aiStartTime
      DATE per row





      USE 1 · STRETCH TRACKER (Block 8)
      aiStartTime = stretchEnd ? → EXTEND : RESTART




      USE 2 · OVERLAP TEST (Block 7)
      aiStartTime + aiStopTime define this row's interval




      USE 3 · SCHEDULE WINDOW (Block 6e)
      aiStartTime




      USE 4 · QTY-ONLY DETECTION (Block 6b)
      aiStartTime near 00:00 ? → placeholder, not real punch














How the formula reads itIF (StartTime.exists(nidx)) THEN
  aiStartTime = StartTime[nidx]

/* used in EXTEND vs RESTART decision */
IF (aiStartTime = stretchEnd) THEN
  stretchEnd = aiStopTime      // EXTEND
ELSE
  stretchStart = aiStartTime  // RESTART

/* and in pairwise overlap test */
IF (dayStarts[i]  dayStops[j]
    AND dayStarts[j]  dayStops[i]) THEN


Two jobs. **Stretch tracking:** compared against the previous stretch's end — if it matches, the worker continued seamlessly (extend); if there's a gap, a new stretch begins (restart). **Overlap detection:** paired with StopTime to define the row's interval; the strict-less-than test catches collisions while allowing back-to-back handovers.





Input 06 · Date Array


StopTime




"When did this row end?"




StopTime_uses.xlsxExcel



      | Used in | What for |


        | Stretch tracker | Becomes the new `stretchEnd` when extending or restarting |

        | Pairwise overlap test | Combined with StartTime to define each row's interval |

        | Schedule window check | Compared to `p_sched_end` for Meal Break entries |

        | Continuous-hours math | Feeds the `contHrs` calculation alongside `stretchStart` |







Always partnered with StartTime to define an interval, but it has its own role in the schedule-window check too.





Diagram · StopTime — partnered with StartTime, standalone for schedule check




      An entry's interval = StartTime ↔ StopTime


      aiStartTime
      14-Apr 10:00


      interval


      aiStopTime
      14-Apr 14:45


      Three places StopTime appears in the formula




      USE 1 · OVERLAP TEST
      Partnered with StartTime
      Together they define the row's
      interval. Block 7 compares this
      interval pairwise against every
      other row's interval.
      starts[i]




      USE 2 · STRETCH TRACKER
      Becomes the new stretchEnd
      Block 8 stores this value as
      the running boundary of the
      continuous-work stretch.
      stretchEnd = aiStopTime
      contHrs = end - start




      USE 3 · SCHEDULE WINDOW
      Standalone (no StartTime)
      Block 6e checks if a Meal Break
      ends after the worker's
      scheduled end time.
      if aiStopTime >
           p_sched_end → flag



      Most uses pair Start+Stop, but the schedule window only needs StopTime







How the formula reads itIF (StopTime.exists(nidx)) THEN
  aiStopTime = StopTime[nidx]

/* schedule window check (Meal Break only) */
IF (aiStopTime > p_sched_end) THEN
  OUT_MSG[nidx] = 'Break outside hours'

/* contHrs calculation */
contHrs = (stretchEnd - stretchStart) * 24


With StartTime, defines the row's interval for overlap testing. Drives the schedule-window check — if a Meal Break ends after `sched_end`, the row gets flagged. Also feeds the continuous-hours calculation as the running stretchEnd.


↓   FORMULA RUNS   ↓





Output · Text Array (Sparse)


OUT_MSG




"Which rows are bad and why?"




OUT_MSG_messages.xlsxExcel



      | Possible message | Fired by |


        | (slot left empty) | Clean row — no validation issue |

        | "Continuous work exceeds 6 hours" | Block 8 (state machine) |

        | "Overlapping entries" | Block 7 (overlap test) |

        | "Break outside working hours" | Block 6e (schedule window) |

        | "RegHours start/stop required" | Block 6c (hard requirement) |







Sparse array indexed by row number. The framework reads each populated slot and renders a red error marker next to that row in the timecard UI; empty slots stay clean.





Diagram · Sparse output — only flagged rows have entries




      Sarah's timecard
      5 rows in OTL grid



        Row 1 · Reg Hours 08:30–10:00


        Row 2 · Reg Hours 10:00–14:45


        Row 3 · Meal Break 19:00–20:00


        Row 4 · Reg Hours 08:00–20:00


        Row 5 · Annual Leave








      OUT_MSG · sparse array
      indexed by row number



        [1]

        empty · row passed all checks


        [2]

        "Continuous work exceeds 6 hours"


        [3]

        "Break outside working hours"


        [4]

        "Overlapping entries"


        [5]

        empty · row passed all checks




      framework reads array


      Result on Sarah's screen:
      Rows 2, 3, 4 get red markers. Rows 1 and 5 stay clean. Sarah sees exactly which entries to fix.














How the formula writes it/* declared at the top of the loop */
OUT_MSG = EMPTY_TEXT_NUMBER

/* populated only for flagged rows */
IF (contHrs > p_max_cont_err) THEN
  OUT_MSG[nidx] = get_msg_attribute('StartTime')
                 || get_output_msg('HXT', p_msg_cont_err)

/* returned implicitly at end of formula */
RETURN OUT_MSG


**Mandatory return.** Sparse — only flagged rows have entries; clean rows leave their slot empty. The framework reads the array after the formula finishes and renders red error markers next to those line numbers in the worker's timecard UI.


#### How the Six Inputs Fit Together: Six Columns of One Spreadsheet


The six inputs aren't independent values — they're **six parallel arrays sharing one index space**. Picture a spreadsheet: each input is a column, and every timecard row occupies the same row index across all six columns at once. Reading all six arrays at index [3] gives the complete picture of one timecard row.



Diagram · Six arrays, one shared index space




    The mental model — six arrays, each holding one type of data, all keyed by the same row index





      RECORD_POSITIONS
      array of TEXT


      PayrollTimeType
      array of TEXT


      StartTime
      array of DATE


      StopTime
      array of DATE


      measure
      array of NUMBER


      HWM_MEASURE_DAY
      array of NUMBER



      'HEADER'

      missing

      missing

      missing

      missing

      missing



      empty

      'Regular Hours'

      09:00

      12:00

      3.0

      unused



      empty

      'Meal Break'

      12:00

      13:00

      1.0

      unused



      empty

      'Regular Hours'

      13:00

      17:00

      4.0

      unused


      [1]
      [2]
      [3]
      [4]




    SHARED INDEX SPACE:
    All six arrays use the SAME index numbers. Read row [3] across all six and you get the full picture of one timecard row.
    No row "object" exists — each row is reassembled at the moment of reading from the six parallel slices.


    How the formula reassembles row [3] inside the loop


    // nidx = 3 in this iteration
    aiRecPos    = RECORD_POSITIONS[nidx]   // empty — this is a real entry
    aiTimeType  = PayrollTimeType[nidx]    // 'Meal Break'
    aiStartTime = StartTime[nidx]          // 12:00
    aiStopTime  = StopTime[nidx]           // 13:00

    The single index nidx walks every array in sync. This is the parallel-arrays idiom in action.
    Once you internalise it, you'll see it everywhere across OTL formula types — the pattern is consistent.



    Six arrays in · One shared index space · No row objects · Reassemble at read time






    Six_Arrays_One_Spreadsheet.xlsx
    Excel




    | Idx
        | RECORD_POSITIONS
        | PayrollTimeType
        | StartTime
        | StopTime
        | measure
      |




        | [1]
        | **HEADER**
        | —
        | —
        | —
        | —
      |


        | [2]
        | (empty)
        | Regular Hours
        | 09:00
        | 12:00
        | 3.0
      |


        | [3]
        | (empty)
        | Meal Break
        | 12:00
        | 13:00
        | 1.0
      |


        | [4]
        | (empty)
        | Regular Hours
        | 13:00
        | 17:00
        | 4.0
      |


        | [5]
        | **END_DAY**
        | —
        | —
        | —
        | —
      |





A simple one-day timecard. Marker rows ([1] HEADER and [5] END_DAY) only fill the `RECORD_POSITIONS` column; their other slots are blank. Real worker entries leave RECORD_POSITIONS empty and fill the data columns. The formula reads `RECORD_POSITIONS` first to decide which path to take.


The formula's WHILE loop walks the index from 1 to N, reading the same index across all six arrays each iteration. There's no concept of a "row object" — each row is reassembled at the moment of reading from the parallel slices. This pattern is consistent across all of OTL's formula types, so once you internalise it once, you'll see it everywhere.


Return anything other than `OUT_MSG` — an extra variable, a misspelled name — and the OTL submission throws a contract error. Return exactly this and nothing else.


## The Complete Formula


Here it is in full. Every line in this listing is exactly what gets pasted into **Manage Fast Formulas**. Read it once top-to-bottom — don't try to understand every line yet. We'll walk through it block by block in the next section.


XX_TER_CONTINUOUS_HOURS_VALIDATION.ffTime Entry Rule


```
/* ============================================================
   Formula Name: XX_TER_CONTINUOUS_HOURS_VALIDATION
   Formula Type: Time Entry Rules
   Description: The Fast formula is required to validate the entry of timecard
                and show error or warning messages if entries are not accurate
                according to the requirements.
   ============================================================ */
DEFAULT FOR HWM_CTXARY_RECORD_POSITIONS IS EMPTY_TEXT_NUMBER
DEFAULT FOR HWM_CTXARY_HWM_MEASURE_DAY  IS EMPTY_NUMBER_NUMBER
DEFAULT FOR HWM_PER_ASG_ASSIGNMENT_ID   IS 0
DEFAULT FOR measure         IS EMPTY_NUMBER_NUMBER
DEFAULT FOR PayrollTimeType IS EMPTY_TEXT_NUMBER
DEFAULT FOR StartTime       IS EMPTY_DATE_NUMBER
DEFAULT FOR StopTime        IS EMPTY_DATE_NUMBER

INPUTS ARE
  HWM_CTXARY_RECORD_POSITIONS,
  HWM_CTXARY_HWM_MEASURE_DAY,
  measure,
  PayrollTimeType,
  StartTime,
  StopTime

ffName  = 'XX_TER_CONTINUOUS_HOURS_VALIDATION'
ffs_id  = GET_CONTEXT(HWM_FFS_ID, 0)
rule_id = GET_CONTEXT(HWM_RULE_ID, 0)

NullDate = '01-JAN-1900' (DATE)
NullText = '**FF_NULL**'

rLog = add_rlog(ffs_id, rule_id, '>>> Enter ' || ffName)

CHANGE_CONTEXTS(HR_ASSIGNMENT_ID = HWM_PER_ASG_ASSIGNMENT_ID)
(
  sumLvl = Get_Hdr_Text(rule_id, 'RUN_SUMMATION_LEVEL', 'DAY')
  rLog = add_rlog(ffs_id, rule_id, '>>> sumLvl=' || sumLvl)

  p_break_type = 'Meal Break'
  p_reg_type   = 'Regular Hours'

  p_sched_start   = get_rvalue_number(rule_id, 'SCHEDULE_START_HOUR',     9)
  p_sched_end     = get_rvalue_number(rule_id, 'SCHEDULE_END_HOUR',      18)
  p_max_cont_err  = get_rvalue_number(rule_id, 'MAX_CONTINUOUS_HRS_ERR',  6)
  p_max_cont_warn = get_rvalue_number(rule_id, 'MAX_CONTINUOUS_HRS_WARN', 5)

  p_msg_break     = 'XX_BREAK_OUTSIDE_HOURS_ERR'
  p_msg_cont_err  = 'XX_CONT_HOURS_ERR_MSG'
  p_msg_cont_warn = 'XX_CONT_HOURS_WRN_MSG'
  p_msg_overlap   = 'XX_OVERLAP_ENTRIES_MSG'
  p_msg_reghrs    = 'XX_REG_HOURS_PUNCHES_REQUIRED'

  rLog = add_rlog(ffs_id, rule_id,
                  '>>> Parms sched=' || TO_CHAR(p_sched_start) || '-' || TO_CHAR(p_sched_end) ||
                  ' cErr='  || TO_CHAR(p_max_cont_err) ||
                  ' cWarn=' || TO_CHAR(p_max_cont_warn))

  OUT_MSG = EMPTY_TEXT_NUMBER

  wMaAry = HWM_CTXARY_RECORD_POSITIONS.count
  rLog = add_rlog(ffs_id, rule_id, '>>> Start bulk wMaAry=' || TO_CHAR(wMaAry))

  cntr = 0
  nidx = 0

  dayStarts = EMPTY_DATE_NUMBER
  dayStops  = EMPTY_DATE_NUMBER
  dayIdxs   = EMPTY_NUMBER_NUMBER
  dayCnt    = 0

  stretchStart = NullDate
  stretchEnd   = NullDate
  inStretch    = 'N'

  l_meal_taken = 'N'

  WHILE (cntr  wMaAry) LOOP
  (
    cntr = cntr + 1
    nidx = nidx + 1

    aiRecPos    = NullText
    aiMeasure   = 0
    aiTimeType  = NullText
    aiStartTime = NullDate
    aiStopTime  = NullDate
    l_qty_only  = 'N'

    aiRecPos = HWM_CTXARY_RECORD_POSITIONS[nidx]

    IF (aiRecPos = 'HEADER') THEN
    (
      rLog = add_rlog(ffs_id, rule_id, '>>> HEADER skipped idx=' || TO_CHAR(nidx))
    )
    ELSE
    (
      IF (MEASURE.exists(nidx))         THEN ( aiMeasure   = MEASURE[nidx] )
      IF (PayrollTimeType.exists(nidx)) THEN ( aiTimeType  = PayrollTimeType[nidx] )
      IF (StartTime.exists(nidx))       THEN ( aiStartTime = StartTime[nidx] )
      IF (StopTime.exists(nidx))        THEN ( aiStopTime  = StopTime[nidx] )

      rLog = add_rlog(ffs_id, rule_id,
                      '>>> idx='  || TO_CHAR(nidx)        ||
                      ' pos='     || aiRecPos             ||
                      ' type=['   || aiTimeType   || ']'  ||
                      ' st='      || TO_CHAR(aiStartTime) ||
                      ' sp='      || TO_CHAR(aiStopTime)  ||
                      ' m='       || TO_CHAR(aiMeasure))

      IF (aiRecPos = 'END_DAY' OR aiRecPos = 'END_PERIOD') THEN
      (
        rLog = add_rlog(ffs_id, rule_id, '>>> Boundary dayCnt=' || TO_CHAR(dayCnt))

        IF (dayCnt > 1) THEN
        ( i = 1
          WHILE (i  dayCnt) LOOP
          ( j = i + 1
            WHILE (j  dayCnt) LOOP
            ( IF (dayStarts[i]  dayStops[j] AND dayStarts[j]  dayStops[i]) THEN
              ( flagIdx = dayIdxs[j]
                OUT_MSG[flagIdx] = get_msg_attribute('StartTime') || get_output_msg('HXT', p_msg_overlap)
                rLog = add_rlog(ffs_id, rule_id, '>>> OVERLAP fired idx=' || TO_CHAR(flagIdx))
              )
              j = j + 1
            )
            i = i + 1
          )
        )

        dayStarts    = EMPTY_DATE_NUMBER
        dayStops     = EMPTY_DATE_NUMBER
        dayIdxs      = EMPTY_NUMBER_NUMBER
        dayCnt       = 0
        stretchStart = NullDate
        stretchEnd   = NullDate
        inStretch    = 'N'
        l_meal_taken = 'N'
      )
      ELSE
      (
        /* QTY-ONLY DETECTION */
        IF (aiTimeType = p_reg_type AND aiStartTime <> NullDate AND aiStopTime <> NullDate) THEN
        ( l_st_hr = TO_NUMBER(TO_CHAR(aiStartTime, 'HH24')) + TO_NUMBER(TO_CHAR(aiStartTime, 'MI'))/60
          l_sp_hr = TO_NUMBER(TO_CHAR(aiStopTime,  'HH24')) + TO_NUMBER(TO_CHAR(aiStopTime,  'MI'))/60
          IF (l_st_hr  0.01 AND l_sp_hr > 23.9) THEN
          ( l_qty_only = 'Y'
            rLog = add_rlog(ffs_id, rule_id, '>>> QTY-ONLY detected idx=' || TO_CHAR(nidx))
          )
        )

        /* Overlap collection - skip qty-only */
        IF (l_qty_only = 'N' AND aiStartTime <> NullDate AND aiStopTime <> NullDate) THEN
        ( dayCnt = dayCnt + 1
          dayStarts[dayCnt] = aiStartTime
          dayStops[dayCnt]  = aiStopTime
          dayIdxs[dayCnt]   = nidx
        )

        /* Reg Hours qty-only */
        IF (aiTimeType = p_reg_type AND l_qty_only = 'Y') THEN
        ( OUT_MSG[nidx] = get_msg_attribute('StartTime') || get_output_msg('HXT', p_msg_reghrs)
          rLog = add_rlog(ffs_id, rule_id, '>>> REGHRS QTY-ONLY fired idx=' || TO_CHAR(nidx))
        )

        /* Reg Hours null start/stop */
        IF (aiTimeType = p_reg_type AND (aiStartTime = NullDate OR aiStopTime = NullDate)) THEN
        ( OUT_MSG[nidx] = get_msg_attribute('StartTime') || get_output_msg('HXT', p_msg_reghrs)
          rLog = add_rlog(ffs_id, rule_id, '>>> REGHRS NULL fired idx=' || TO_CHAR(nidx))
        )

        /* Meal break stretch reset */
        IF (aiTimeType = p_break_type) THEN
        ( stretchStart = NullDate
          stretchEnd   = NullDate
          inStretch    = 'N'
          l_meal_taken = 'Y'
          rLog = add_rlog(ffs_id, rule_id, '>>> MEAL RESET idx=' || TO_CHAR(nidx))
        )

        l_day = TO_CHAR(aiStartTime, 'DY')

        l_sch_date_day = get_date_day_of_week(aiStartTime)
        l_dow_char     = UPPER(TO_CHAR(aiStartTime, 'DY'))
        hol = GET_VALUE_SET('XX_HOLIDAY_CALENDAR_VS',
                            '|=p_date=''' || to_char(aiStartTime, 'YYYY/MM/DD') || '''')

        rLog = add_rlog(ffs_id, rule_id,
                        'dow_fn='    || l_sch_date_day ||
                        ' dow_char=' || l_dow_char     ||
                        ' hol='      || hol)

        /* Break outside working hours */
        IF (aiTimeType = p_break_type AND aiStartTime <> NullDate AND aiStopTime <> NullDate) THEN
        ( bkStart = TO_NUMBER(TO_CHAR(aiStartTime, 'HH24')) + TO_NUMBER(TO_CHAR(aiStartTime, 'MI'))/60
          bkEnd   = TO_NUMBER(TO_CHAR(aiStopTime,  'HH24')) + TO_NUMBER(TO_CHAR(aiStopTime,  'MI'))/60
          IF ((bkStart  p_sched_start OR bkEnd > p_sched_end)
              AND l_day <> 'SAT' AND l_day <> 'SUN' AND length(hol) = 0) THEN
          ( OUT_MSG[nidx] = get_msg_attribute('StartTime') || get_output_msg('HXT', p_msg_break)
            rLog = add_rlog(ffs_id, rule_id, '>>> BREAK OUT fired idx=' || TO_CHAR(nidx))
          )
        )

        /* Continuous stretch */
        IF (aiTimeType = p_reg_type AND aiStartTime <> NullDate AND aiStopTime <> NullDate
            AND l_qty_only = 'N' AND l_meal_taken = 'N') THEN
        (
          IF (inStretch = 'N') THEN
          ( stretchStart = aiStartTime
            stretchEnd   = aiStopTime
            inStretch    = 'Y'
          )
          ELSE
          ( IF (aiStartTime = stretchEnd) THEN
            ( stretchEnd = aiStopTime )
            ELSE
            ( stretchStart = aiStartTime
              stretchEnd   = aiStopTime
            )
          )

          endMins = TO_NUMBER(TO_CHAR(stretchEnd,   'J'))*1440
                  + TO_NUMBER(TO_CHAR(stretchEnd,   'HH24'))*60
                  + TO_NUMBER(TO_CHAR(stretchEnd,   'MI'))
          stMins  = TO_NUMBER(TO_CHAR(stretchStart, 'J'))*1440
                  + TO_NUMBER(TO_CHAR(stretchStart, 'HH24'))*60
                  + TO_NUMBER(TO_CHAR(stretchStart, 'MI'))
          contHrs = (endMins - stMins) / 60

          rLog = add_rlog(ffs_id, rule_id, '>>> ContHrs=' || TO_CHAR(contHrs) || ' idx=' || TO_CHAR(nidx))

          IF (contHrs > p_max_cont_err
              AND l_day <> 'SAT' AND l_day <> 'SUN' AND length(hol) = 0) THEN
          ( OUT_MSG[nidx] = get_msg_attribute('StartTime') || get_output_msg('HXT', p_msg_cont_err)
            rLog = add_rlog(ffs_id, rule_id, '>>> CONT ERR fired idx=' || TO_CHAR(nidx))
          )
          ELSE
          ( IF (contHrs > p_max_cont_warn
                AND l_day <> 'SAT' AND l_day <> 'SUN' AND length(hol) = 0) THEN
            ( OUT_MSG[nidx] = get_msg_attribute('StartTime') || get_output_msg('HXT', p_msg_cont_warn)
              rLog = add_rlog(ffs_id, rule_id, '>>> CONT WARN fired idx=' || TO_CHAR(nidx))
            )
          )
        )
      ) /* end ELSE - non-boundary processing */
    ) /* end ELSE - non-HEADER */

    IF (nidx > 1000) THEN
    ( ex = raise_error(ffs_id, rule_id, 'Formula ' || ffName || ' terminated - possible endless loop.') )

    rLog = add_rlog(ffs_id, rule_id, '>>> End bulk ' || ffName)
  ) /* end WHILE body */
) /* end CHANGE_CONTEXTS */

RETURN OUT_MSG
```


That's the entire formula. ~200 lines, three nested control structures, one state machine, and five validations all in one pass through the array. Now let's break it down piece by piece.


## The Formula's Architecture


Before reading the code line-by-line, it helps to see the shape of the whole thing. The formula has eight blocks that fall into **two clean halves**: the first five blocks run *once* as scaffolding (set up arrays, capture identity, bind context, read configuration, initialise state), and the last three blocks run *repeatedly* inside the WHILE loop where the actual validation happens. Every line of code belongs to exactly one of these eight blocks.



Diagram · Eight blocks, two halves — data flow from input arrays to OUT_MSG return




    Six input arrays enter the formula



      RECORD_
      POSITIONS


      PayrollTime
      Type


      StartTime


      StopTime


      measure


      HWM_MEASURE
      DAY







    SETUP HALF · runs ONCE at the top of the formula
    scaffolding — preparing everything the loop will need




      BLOCK 1
      Crash
      prevention
      DEFAULT FOR


      BLOCK 2
      Self-
      identification
      ffName, ids, log


      BLOCK 3
      Single context
      wrap
      CHANGE_CONTEXTS


      BLOCK 4
      Per-LE
      configuration
      get_rvalue_number


      BLOCK 5
      Three lifetimes
      init
      OUT_MSG, buffers




    scaffolding done → enter loop



    LOOP HALF · runs ONCE PER TIMECARD ROW (N times total)
    the actual validation work — classify, accumulate, judge




      BLOCK 6 · Per-line routing
      Read row, classify by type,
      route to validation path
      qty-only / hard requirement
      day buffer / schedule check


      BLOCK 7 · Day boundary
      Only fires at END_DAY:
      pairwise overlap test
      strict less-than check
      reset day-level state


      BLOCK 8 · State machine
      Continuous-hours tracker:
      EXTEND / RESTART / RESET
      Julian Day arithmetic
      error wins over warning





    WHILE (cntr



    loop ends → return



    OUT_MSG returned to OTL framework
    sparse array of error messages, one per flagged row












Architecture · eight blocks, two halves


From input array to OUT_MSG return










Stage 01


Block 1









Initruns once


Declare inputs and their empty-array defaults


`DEFAULT FOR` for every input prevents `FFL-09100` at runtime when the framework hands over a sparse array.











Stage 02


Block 2









Initruns once


Capture identity, define sentinels, log entry


Capture `ffs_id` and `rule_id` from context, declare `NullDate` and `NullText` sentinels, and write the formula's first log line so every subsequent message is scoped and traceable.











Stage 03


Block 3









Initruns once


Wrap the body in `CHANGE_CONTEXTS`


One outer wrap binds `HR_ASSIGNMENT_ID` for every DBI and value-set lookup inside — **200× faster** than re-binding per iteration.











Stage 04


Block 4









Initruns once


Read configuration via `get_rvalue_number`


Schedule bounds and continuous-hours thresholds come from the rule definition. **One formula serves every LE** — per-entity variation lives in the rule, not the source.











Stage 05


Block 5









Initruns once


Initialise day buffer, stretch tracker, OUT_MSG


Three pieces of state with three different lifetimes — per-line, per-day, per-formula. The lifecycle distinction is what makes the rest of the formula correct.











Stage 06


Block 6









Per linein WHILE loop


Read line, classify, route by time type


Detect qty-only placeholders (`00:00–23:59`), buffer Reg Hours for overlap, route Meal Breaks to the schedule-window check.











Stage 07


Block 7









Per dayat END_DAY marker


Pairwise overlap test on the day buffer


Strict less-than (`Per linecross-iteration state


Continuous-hours state machine


Idle ↔ Active. EXTEND when adjacent, RESTART on gap, RESET on meal break. Compares `contHrs` against soft-warn (5h) and hard-error (6h) thresholds.











Return


OUT_MSG









Exitframework reads sparse array


Sparse array of error messages by line index


Empty slots = clean rows. Populated slots become red error markers in the worker's timecard UI.









The first five blocks (Stages 01–05) make up the **setup half** — they run exactly once at the top of the formula, before any timecard row is processed. The last three (Stages 06–08) make up the **loop half** — they execute once per row inside the WHILE loop, with Block 7 firing only at day boundaries. Every line in the formula source belongs to one of these eight blocks. The Part 2 walkthrough goes through each block in detail; for now, this overview is enough to navigate the complete code listing above.


## Variable Naming Conventions in This Formula


Fast Formula doesn't enforce naming rules — you can call any variable anything — but the formula in this post follows a deliberate convention. **Each prefix signals the variable's role**: where its value comes from, what its lifetime is, what code is allowed to write to it. Once you internalise the prefixes, the rest of the formula reads itself. This section is worth a few minutes upfront because Part 2 of this series uses these prefixes throughout the code walkthrough.


Seven naming patterns do all the work in this formula. The reference table below summarises them; the cards that follow explain each one in detail.




    Naming_Conventions_Reference.xlsx
    Excel




    | Prefix
        | Means
        | Examples in this formula
        | Lifetime
        | Who writes to it?
      |




        | `HWM_*`
        | Framework-supplied context or input
        | `HWM_FFS_ID`, `HWM_RULE_ID`, `HWM_PER_ASG_ASSIGNMENT_ID`
        | Whole formula
        | The OTL framework (read-only)
      |


        | `HWM_CTXARY_*`
        | Framework input *array* (one slot per timecard row)
        | `HWM_CTXARY_RECORD_POSITIONS`, `HWM_CTXARY_HWM_MEASURE_DAY`
        | Whole formula
        | The framework (read-only)
      |


        | `p_*`
        | Parameter read from rule configuration
        | `p_sched_start`, `p_max_cont_err`, `p_msg_overlap`
        | Whole formula
        | Set once in Block 4, read everywhere
      |


        | `ai*`
        | "Array input" — per-row local snapshot of input data
        | `aiTimeType`, `aiStartTime`, `aiStopTime`, `aiRecPos`
        | One iteration
        | Reset at top of every loop iteration
      |


        | `l_*`
        | Local working variable or flag
        | `l_qty_only`, `l_meal_taken`, `l_day`, `l_st_hr`
        | Per-row or per-day
        | Set inside the loop body
      |


        | `day*` / `stretch*`
        | State variables with named lifetimes
        | `dayStarts`, `dayCnt`, `stretchStart`, `inStretch`
        | Per-day / per-stretch
        | Updated inside loop, reset at boundaries
      |


        | `OUT_MSG`
        | The formula's return value (sparse error array)
        | `OUT_MSG`
        | Whole formula
        | Written only when a row needs flagging
      |





Seven naming patterns. Each one signals a different role and lifetime, making the formula's intent visible without reading the surrounding code.


Now the prefixes in detail, with examples and the reasoning behind each convention:





Prefix 01 · Framework Context


HWM_*




"Where does this value come from?" → The OTL framework, before the formula even runs.




HWM_Examples.xlsxExcel



      | Variable | What it holds | Set by |


        | `HWM_FFS_ID` | This run's session ID | Framework, on submission |

        | `HWM_RULE_ID` | The rule that triggered this formula | Framework, on rule binding |

        | `HWM_PER_ASG_ASSIGNMENT_ID` | The worker's HR assignment ID | Framework, from worker context |







The `HWM_` prefix — short for *HCM Workforce Management* — marks variables the OTL framework injects into the formula's scope. They're not declared by the formula author; they appear automatically when the formula runs. The values are read-only from the formula's perspective; trying to assign to them does nothing useful and can break the binding.

Their purpose is to give the formula access to **contextual information about the current run**: whose timecard is being validated (`HWM_PER_ASG_ASSIGNMENT_ID`), which rule fired the formula (`HWM_RULE_ID`), and what unique session ID identifies this specific submission for log tracing (`HWM_FFS_ID`). Block 2 captures these into shorter local variables (`ffs_id`, `rule_id`) for convenience throughout the rest of the formula.





Prefix 02 · Framework Input Array


HWM_CTXARY_*




"Is this a single value or a parallel array indexed by row number?" → An array, one slot per timecard row.




HWM_CTXARY_Examples.xlsxExcel



      | Variable | Holds (per row) | Type |


        | `HWM_CTXARY_RECORD_POSITIONS` | Marker text or empty | TEXT_NUMBER array |

        | `HWM_CTXARY_HWM_MEASURE_DAY` | Day-aggregated quantity | NUMBER_NUMBER array |







The `HWM_CTXARY_` prefix — short for *HCM Workforce Management Context Array* — marks the framework's **parallel input arrays**. Where `HWM_*` holds a single value, `HWM_CTXARY_*` holds one slot per timecard row, all indexed by the same row number.

You access them like arrays: `HWM_CTXARY_RECORD_POSITIONS[3]` retrieves the value for row 3. The naming feels heavy, but it's deliberately verbose so you can never mistake a per-row array for a single-value context. Confusing the two would cause type errors at compile time — loud and easy to fix — so the convention pays off.

Note that some inputs in the `INPUTS ARE` declaration (like `measure`, `StartTime`, `StopTime`) *also* behave as parallel arrays but use cleaner names. They're framework arrays too; they just don't use the `HWM_CTXARY_` prefix because OTL's design predates the convention. Treat them the same way: per-row, indexed by row number, read-only.





Prefix 03 · Parameter


p_*




"Is this value tunable per legal entity?" → Yes — read once from the rule, then used as a constant.




p_Examples.xlsxExcel



      | Variable | Source | Purpose |


        | `p_sched_start` | Rule param SCHEDULE_START_HOUR | Schedule window check |

        | `p_max_cont_err` | Rule param MAX_CONTINUOUS_HRS_ERR | Hard cap on continuous work |

        | `p_max_cont_warn` | Rule param MAX_CONTINUOUS_HRS_WARN | Soft warning threshold |

        | `p_msg_overlap` | Hardcoded message name | Error message lookup key |

        | `p_break_type` | Hardcoded layout label | Time-type matching |







The `p_` prefix marks **parameter-style variables** — values set once in Block 4 and used throughout the rest of the formula as effectively constant. The lowercase `p` distinguishes them from framework-supplied values (`HWM_*`) and per-row scratch (`ai*`, `l_*`).

Most `p_*` variables are read from the rule configuration via `get_rvalue_number`, which fetches numeric parameters that legal entities can tune independently — this is how one entity can use a 5-hour cap while another uses 6 with the same formula source. A few `p_*` variables (the message names like `p_msg_overlap`, the time-type labels like `p_break_type`) are hardcoded because they don't vary across the rollout.

The convention serves a code-review purpose: when you see `p_*` being assigned anywhere outside Block 4, that's a code smell — parameters should be set once at setup and treated as constant during the loop. Mutation indicates a bug or a misuse.





Prefix 04 · Array Input Snapshot


ai*




"Is this a per-row local copy of input data?" → Yes — refreshed at the top of every iteration.




ai_Examples.xlsxExcel



      | Variable | Source array | Used for |


        | `aiRecPos` | RECORD_POSITIONS[nidx] | Row-type routing (HEADER vs END_DAY vs data) |

        | `aiTimeType` | PayrollTimeType[nidx] | Validation routing (Reg Hours vs Meal Break) |

        | `aiStartTime` | StartTime[nidx] | Stretch tracking, overlap testing |

        | `aiStopTime` | StopTime[nidx] | Stretch tracking, overlap testing |







The `ai` prefix stands for **"array input"** — per-row local snapshots of values pulled from the framework's input arrays. At the top of every loop iteration, the formula reads from the input arrays (with `.exists()` guards) and copies the values into matching `ai*` locals.

Why copy rather than reading the input arrays directly throughout the iteration? Three reasons. First, it creates a **consistent snapshot**: the rest of the iteration always sees the same values for "this row", even if downstream code logic gets restructured. Second, it provides a single place to apply guards (the `.exists()` checks in the read block) so you can never accidentally trigger an unguarded read elsewhere. Third, it makes the data flow obvious in code review — seeing `ai*` on the left of an assignment in the read block flags it as the "snapshot point", and the rest of the iteration cleanly works from those locals.

The `ai*` variables are reset at the top of every iteration to their sentinel values (`NullText`, `NullDate`) before the new row's reads happen. This explicit reset prevents the stale-value bug discussed in Block 5.





Prefix 05 · Local Working Variable


l_*




"Is this a temporary working value or flag inside the loop body?" → Yes.




l_Examples.xlsxExcel



      | Variable | Type | Lifetime & purpose |


        | `l_qty_only` | 'Y'/'N' flag | Per-row: was this row detected as a qty-only placeholder? |

        | `l_meal_taken` | 'Y'/'N' flag | Per-day: has the worker logged a meal break yet today? |

        | `l_day` | 3-letter day code | Per-row: 'MON', 'SAT', etc., for weekend exception checks |

        | `l_st_hr` / `l_sp_hr` | fractional hour | Per-row: punch times converted to decimal hours |







The `l_` prefix marks **local working variables** created inside the loop body for intermediate computation or state-tracking. Some are per-row (computed fresh each iteration), some are per-day (set once on a triggering event and persisting until the next day boundary).

The prefix's main job is to distinguish working state from input snapshots (`ai*`) and parameters (`p_*`). A formula reader scanning the code can immediately tell `l_qty_only` is a flag the formula sets itself, not data from the framework or a configuration value.

Within `l_*` there's an unwritten sub-convention: variables that hold `'Y'`/`'N'` flags use names ending in past-tense or descriptive adjectives (`l_meal_taken`, `l_qty_only`), while variables that hold computed numeric or string values use abbreviated names (`l_st_hr`, `l_day`). The convention isn't enforced, but consistency makes the code easier to scan.





Prefix 06 · Named-Lifetime State


day*  ·  stretch*




"Does this variable have a specific multi-row lifetime tied to a domain concept?" → Yes.




State_Group_Examples.xlsxExcel



      | Group | Variables | Resets when |


        | **day*** | `dayStarts`, `dayStops`, `dayIdxs`, `dayCnt` | At END_DAY/END_PERIOD marker |

        | **stretch*** | `stretchStart`, `stretchEnd`, `inStretch` | On meal break or END_DAY |







Some variables can't be neatly classified as "per-row" or "whole-formula" — they live for a domain-specific period that the formula explicitly manages. The convention here is to **group these by domain prefix**: `day*` for variables related to a single day's accumulated state, `stretch*` for variables tracking the current continuous-work stretch.

The grouping makes the code's structure self-documenting. When a reader sees `dayStarts`, `dayStops`, `dayIdxs`, and `dayCnt` together, they immediately recognise these as the day buffer — four pieces of one logical structure. Same for `stretchStart`, `stretchEnd`, `inStretch` as the stretch tracker.

The grouping also signals that these variables must be **reset together**. Block 7c (the END_DAY reset) clears all four day buffer variables in one block, and clears the stretch tracker variables in the same block. Resetting some without others would corrupt state. The naming makes it obvious which variables belong in the same reset block.





Prefix 07 · Formula Output (Reserved Name)


OUT_MSG




"Is this the value the formula returns to the framework?" → Yes — and the name is reserved.




OUT_MSG_Behaviour.xlsxExcel



      | Idx | OUT_MSG content | Meaning |


        | [2] | (no entry) | clean row |

        | [3] | "Continuous work exceeds 6 hours" | flagged row |

        | [5] | "Overlapping entries" | flagged row |

        | [6] | (no entry) | clean row |







`OUT_MSG` is the only variable in this formula whose name is **not chosen by the author** — it's reserved by the TER formula type contract. The framework expects the formula to write error messages into a variable with this exact name, and reads from it after the formula returns.

The naming is uppercase to signal "framework-reserved", distinguishing it from the lowercase prefixes (`p_`, `ai`, `l_`, `day`, `stretch`) used for author-chosen names. The pattern carries over to other formula types: payroll formulas have their own reserved output names, absence formulas have theirs.

The `_MSG` suffix hints at the data type (a sparse array of message strings indexed by row number). The combination — uppercase name plus underscore-separated suffix — is a strong visual signal that this variable is a contract surface, not a working variable. Treat it as such: write to it sparingly, only for rows that need flagging, and never reset it during the run.


### Why these conventions matter beyond style


Naming conventions might feel like decoration, but in Fast Formula they carry real engineering value. Three benefits worth being explicit about:


**Self-documenting role.** Fast Formula has no type signatures, no scope modifiers, no access controls. Every variable looks the same to the compiler. The naming convention is the only signal a reader has about whether they're looking at framework data, parameter config, per-row input, working state, or output. Without conventions, you'd have to read the variable's declaration site to understand its role — which is often hundreds of lines away.


**Code-review heuristics.** When reviewing TER formulas, certain patterns are immediately suspicious. `p_*` being assigned outside Block 4 means a parameter is being mutated mid-loop — almost certainly a bug. `HWM_*` being assigned anywhere means someone tried to write to a framework value — broken. `ai*` being read without first being reset means stale data leakage. The conventions turn code review into a pattern-matching exercise; you can spot bugs by shape before reading the logic.


**Onboarding cost.** A developer joining the team can read this convention table in two minutes and then read the formula's variables fluently. Without conventions, every new variable is a small puzzle — "what does `x` do? where does `y` come from?" — and onboarding takes weeks instead of days.



A note on consistency across formulas

  Different teams use different conventions, and Oracle's documentation doesn't mandate any specific style. The patterns shown here (`HWM_`, `p_`, `ai`, `l_`, `day*`, `stretch*`, `OUT_MSG`) are common in OTL implementations but you'll see variations elsewhere. The principle that matters is *consistency within a project*. Pick a convention, document it, and apply it uniformly. The specific letters matter less than the discipline of using them.








Same formula.


The algorithm in detail.






PART 2 OF 2


Coming next



















    SETUP
    PHASE













    PER-LINE
    ROUTING








    DAY
    BOUNDARY












    STATE
    MACHINE










    SETUP
    DEPENDENCIES











    WORKED
    EXAMPLE










      Continue to Part 2 →














    Part 2 walks through every block of the formula in detail — with the **continuous-hours state machine** as the centrepiece. You'll also get the per-line routing decisions, the day-boundary overlap test, the setup dependencies that must exist for the formula to fire, and a worked end-to-end trace of Sarah's full timecard.




Next in The TER Series


Part 3 — The Algorithm: Setup, Routing, and Overlap Detection


The data shape is settled. Now the algorithm. Part 3 walks through the formula's setup phase (crash prevention, identity capture, per-LE configuration), the per-line routing that decides which checks apply to each row, and the day-boundary pairwise overlap test — the first half of the eight-block algorithm.



AM




Abhishek Mohanty


Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Time and Labor, Absence Management, Core HR, Redwood, HDL, OTBI.




  [Fast Formula](https://abhishekmohanty-hcm.blogspot.com/search/label/Fast%20Formula)
  [Time Entry Rule](https://abhishekmohanty-hcm.blogspot.com/search/label/Time%20Entry%20Rule)
  [OTL](https://abhishekmohanty-hcm.blogspot.com/search/label/OTL)
  [Time and Labor](https://abhishekmohanty-hcm.blogspot.com/search/label/Time%20and%20Labor)
  [Oracle HCM Cloud](https://abhishekmohanty-hcm.blogspot.com/search/label/Oracle%20HCM%20Cloud)