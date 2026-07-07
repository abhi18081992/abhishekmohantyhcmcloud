---
title: "Oracle Fast Formula: Time Entry Rule (Part 1)"
description: "Oracle Fast Formula: Time Entry Rule (Part 1) — Inputs, Contract, and Architecture"
pubDate: 2026-05-21
tags: ["Fast Formula", "Oracle HCM Cloud", "TER", "Time Entry Rule", "OTL"]
---

Oracle Fast Formula: Time Entry Rule (Part 1) — Inputs, Contract, and Architecture
- Fast Formula
  Time Entry Rule
  OTL
  Hands-On


May 21, 2026 • 14 min read • Oracle HCM Cloud


  The TER Series
  Part 1 of 4

    1. OTL Foundations ·
    2. The Input Contract ·
    3. Algorithm: Routing & Overlap ·
    4. The State Machine



# Oracle OTL and Where Time Entry Rules FitPart 1 of 4 — The TER Series


  AM

    Abhishek Mohanty
    Oracle ACE Apprentice · AIOUG Member · Oracle HCM Cloud Consultant & Technical Lead



  Time Entry Rule (TER) formulas live inside Oracle's Time and Labor module — the part of HCM Cloud that workers use to log their hours. This first post in the series introduces what OTL is, where TER sits in its submission flow, and why this is the validation layer where the real business logic lives.


## What OTL Is


Oracle Time and Labor (OTL) is the time-tracking module inside Oracle HCM Cloud. Workers log their hours into it through a timecard layout. Managers approve those timecards. The approved data flows downstream to payroll, project costing, or wherever the hours need to land. That's the loop at its simplest.

What makes OTL interesting from a developer's point of view is the extensibility model. Between the worker hitting Submit and the data landing in payroll, OTL runs the timecard through a series of **rule formulas** that you, as the implementer, can write. Each formula type plays a different role:


  **Time Entry Rules (TER)** — run when the worker tries to save or submit. They validate the data and either let it through or flag it with messages the worker can see. *This is what the series is about.*

  - **Time Calculation Rules (TCR)** — run after validation passes. They derive new values from the worker's entries: overtime, premium pay, shift differentials. The worker's original entries stay untouched; TCR adds calculated rows on top.

  - **Time Device Rules (TDR)** — handle integration with physical badge readers and punch clocks. They map raw punch events into the OTL data model.


Each rule type sees a different shape of data, gets different inputs from the framework, and is allowed to do different things. TER is the strictest of the three because it runs *before* the data is accepted — its job is to be a guard. Calculations and device integration come later.


## Why TER Is the Hard One


OTL's framework gives you some validation for free. If a worker leaves a required field blank, OTL catches it. If they type letters into a numeric field, OTL catches that too. These are *declarative validations* — you configure them in the timecard layout, and the framework enforces them with no code.


But declarative validation can only check one cell at a time. The validations that actually matter in production are about relationships between cells, between rows, and between days. Things like:


  - "Did this worker take a meal break after 6 hours of continuous work?" — spans multiple rows on the same day

  - "Do any of these entries overlap with each other?" — pairwise comparison across rows

  - "Is this meal break inside the worker's scheduled hours?" — requires reading the schedule, which lives elsewhere in HCM

  - "Has this worker exceeded their weekly hours cap?" — cumulative across days


None of these can be expressed in declarative configuration. They need code that loops, remembers, and compares. That's where TER formulas earn their place — and that's where most teams either skip the validation entirely or get it subtly wrong.


This series walks through one production TER formula end-to-end, using a real five-rule validation example. By the end of Part 4 you'll know how the framework hands data to the formula, how the formula loops through it, and how to encode every common validation pattern you'll encounter on a TER implementation.


## What This Formula Does


The job is straightforward to describe and surprisingly subtle to build. When a worker submits their timecard, OTL needs to verify that what they entered makes sense — not just structurally (which the framework handles for free), but according to the company's actual labour rules.








Five rules.


One enforces them all.






WHAT THIS FORMULA DOES


Validation rules at a glance










    RULE 01
    RULE 02
    RULE 03
    RULE 04 · THE HARD ONE
    RULE 05







      - REGHOURS
    INTEGRITY
    real punches
    required









    NO
    OVERLAPS
    pairwise interval
    test














    MEAL BREAK
    WINDOW
    inside scheduled
    hours












    CONTINUOUS-
    WORK CAP
    hard error at 6h










    CONTINUOUS-
    WORK WARN
    soft warning at 5h









      Multi-row state is what makes it hard






    Rules 1 and 3 only need a single row. Rules 2, 4, and 5 are **multi-row validations** — they need to know about other rows on the same day, or remember state from earlier iterations. That single architectural requirement — *seeing more than one row at a time* — is what separates TER from anything you can do with declarative configuration.



  Expert framing
  Rules 4 and 5 (the continuous-work checks) are the genuinely hard ones — not because the maths is complex, but because they require **state that persists across loop iterations**. You can't just look at row 3 and decide whether continuous work has been exceeded; you need to know what rows 1 and 2 said, whether a meal break has been logged yet, and whether yesterday's data has been correctly cleared.
  Most TER implementations I've reviewed in client environments either get this wrong (the formula incorrectly extends a stretch across a meal break) or skip it entirely (declaring the validation "out of scope" and pushing it to a manager-review step). Both outcomes are bad. By the end of Part 2, you'll know exactly how to do it right.


### Where TER fits in OTL's processing chain


Before we get into the formula's internals, it helps to know where TER sits in OTL's bigger picture. When a worker hits Submit on their timecard, OTL runs through a sequence of stages — and TER is just one of them. Understanding the sequence tells you why TER receives the data it does, and why your validation logic belongs here and not somewhere else.


  OTL's Submission Pipeline — Where TER Fits In
  Each stage runs in order. Failures in earlier stages stop the chain.



  START
  Worker submits
  Timecard data leaves UI







  STAGE 1 · AUTOMATIC
  Built-in validations
  Required fields, data types,
  payroll time type existence



  data shape ok




  STAGE 2 · YOUR FORMULA RUNS HERE
  Time Entry Rule (TER)
  Cross-row validation, calendar
  context, state machines



  all rules pass




  STAGE 3 · DERIVATION
  Time Calculation Rule
  Overtime, shift premiums,
  allowances from valid time







  STAGE 4 · HUMAN REVIEW
  Approval workflow
  Manager review, exception
  handling, sign-off






  FINISH
  Time repository
  Data persisted, payroll-ready



  if invalid


  if rules fail




  FAILURE PATH · TIMECARD RETURNS TO WORKER
  Red error markers appear next to flagged rows.
  Worker must fix all errors before resubmission is accepted.



  Where to put each kind of validation logic


  DECLARATIVE CONFIG
  Required-field rules,
  type checks → Stage 1


  FAST FORMULA — TER
  Cross-row, calendar,
  stateful logic → Stage 2


  FAST FORMULA — TCR
  Derivations from
  valid data → Stage 3


  WORKFLOW
  Manager judgement,
  exceptions → Stage 4












The pipeline is sequential and the failure paths are unforgiving. If built-in validations reject the data, your TER never even runs — the timecard bounces back to the worker before reaching Stage 2. If your TER returns errors, the timecard bounces back at Stage 2, before Stages 3 and 4 ever execute. Only when every stage passes does the data land in the time repository where payroll can pick it up.

This sequencing has practical consequences for what your TER should and shouldn't try to do:


  **Don't reimplement Stage 1.** Built-in validations already check that required fields are filled and types are correct. Your TER will never see malformed data, so don't waste code defending against it. Trust the framework.

  - **Don't try to do Stage 3's job.** Calculations like overtime, shift premiums, and allowances belong in TCR formulas, not TER. TER's job is "is this data valid?" — not "what should we pay them?"

  - **Don't push Stage 2 logic into Stage 4.** If a rule has a clear yes/no answer, validate it here. Sending every borderline case to a manager for sign-off creates an approval bottleneck that becomes the team's full-time job.


TER is the right home for everything in our five-rule list above — cross-row, calendar-aware, stateful checks with deterministic answers. With that placement clear, let's look at what an actual problem timecard looks like.


## A Real World Example


The fastest way to understand what a TER formula actually does is to watch one fail a timecard. Abstract talk about "validation rules" and "stateful checks" doesn't stick; a real broken submission does. Let me introduce you to Sarah, a software engineer at a product company. Her workday is scheduled 9:00 AM to 6:00 PM, and her employer has one labour-policy rule worth knowing: **no worker may log more than 6 hours of continuous Regular Hours without a meal break in between**.


Tuesday is a deadline day. Sarah gets pulled into a code review at 10 AM and forgets to take lunch. By 6:15 PM she sits down to fill in her timecard, looks at the half-finished entries she made earlier, decides the rows look "messy," and tries to fix things by adding one big block covering the whole day. Then she clicks Submit.


This is what her timecard looks like at the moment of submission — four rows in OTL's grid, exactly as the framework will hand them to your formula:




    Sarah_Timecard_14Apr2026.xlsx
    Excel




    |
        | Date
        | Time Type
        | Start Time
        | Stop Time
        | Hours
        | What the formula does
      |




        | 1
        | 14-Apr-2026
        | Regular Hours
        | 08:30
        | 10:00
        | 1.5
        | ✓ Clean — no flag
      |


        | 2
        | 14-Apr-2026
        | Regular Hours
        | 10:00
        | 14:45
        | 4.75
        | ✗ Continuous work over 6 hours
      |


        | 3
        | 14-Apr-2026
        | Meal Break
        | 19:00
        | 20:00
        | 1.0
        | ✗ Break outside working hours
      |


        | 4
        | 14-Apr-2026
        | Regular Hours
        | 08:00
        | 20:00
        | 12.0
        | ✗ Overlapping entries
      |





Sarah's submission — one clean row, three problem rows. Before reading the analysis below, take a moment to spot the three errors yourself. They're all visible if you know what to look for.


### The day, drawn on a timeline


Tables are good for precise data; timelines are better for understanding the *shape* of a day. Here's Sarah's same four rows plotted against the actual hours of Tuesday, 14 April. The schedule window (9 AM to 6 PM, in pale orange) shows when she was supposed to be working. Each row from the timecard sits as a coloured bar where she logged it:


  Sarah's Tuesday, 14-Apr-2026 — What the formula sees
  Three problems are visible the moment you draw the rows on a timeline





  SCHEDULE WINDOW · 09:00 — 18:00


  CONTINUOUS WORK · 6h 15m — over the 6h cap





  - 06:00
  07:00
  08:00
  09:00
  10:00
  11:00
  12:00
  13:00
  14:00
  15:00
  16:00
  17:00
  18:00
  19:00
  20:00
  21:00
  22:00

























  Row 1
  Reg Hours

  Row 2
  Reg Hours

  Row 3
  Meal Break

  Row 4
  Reg Hours



  08:30 – 10:00



  10:00 – 14:45 (4h 45m)



  19–20



  08:00 – 20:00 (12h block, overlaps everything)









  outside
  schedule






  Clean entry


  Flagged entry


  Schedule window


  Continuous-work span


The picture makes the violations visible at a glance:


  **Rows 1 and 2 touch.** Row 1 ends at 10:00 and row 2 starts at 10:00 — no gap. From the formula's perspective this is a single 6h 15m stretch of continuous work, sitting clearly above the 6-hour cap.

  - **Row 3 sits outside the schedule window.** The shaded amber band shows where Sarah was scheduled to work (9 AM to 6 PM). Her meal break at 19:00–20:00 falls a full hour past the schedule's edge. Whatever she was doing then, it wasn't a workplace meal break.

  - **Row 4 covers the entire day in one massive bar.** You can see it physically overlap with rows 1, 2, and 3 simultaneously. This is the consolidated entry Sarah added without removing the originals — three overlap conflicts in a single row.



Practitioner's tip

  When I'm sketching out a TER's behaviour for a client, I always start with a timeline like this one. Tables hide temporal relationships; timelines surface them. If you're explaining to a non-technical stakeholder why their data is producing strange results, draw a timeline. Five minutes of pen-and-paper sketching will save you an hour of meeting time.


#### The same data as a row-by-hour grid


The timeline above shows *where* the entries sit. The grid below shows *how each entry occupies hours* — one row per timecard entry, one column per hour. Cells light up where the entry is active. The cell numbers count consecutive hours within each entry, so you can see at a glance when an entry crosses a threshold.



  Sarah's Tuesday — Row by Hour Grid
  Each row's lifecycle across the day. Numbers count cumulative hours within the entry.



  SCHEDULE WINDOW (09:00 — 18:00)





  ENTRY





  06
  07
  08
  09
  10
  11
  12
  13
  14
  15
  16
  17
  18
  19
  20
  21
  22

  RESULT































  Row 1
  Reg Hrs




  RU



  1


  CLEAN
  08:30 – 10:00




  Row 2
  Reg Hrs




  RU



  1



  2



  3



  4







  6h cap breached at 14:30


  FLAGGED
  cont > 6h




  Row 3
  Meal




  RU


  FLAGGED
  outside hours


  Row 4
  Reg Hrs



  RU


  1


  2


  3


  4


  5


  6


  7


  8


  9


  10


  11


  FLAGGED
  overlaps 1, 2, 3





  Clean cell


  Flagged cell

  RU
  = row's start hour

  1, 2, 3...
  = cumulative hours within entry


  Schedule window (09:00 — 18:00)



  HOW TO READ:
  Each row's lifecycle runs left to right. Row 2 hits hour 4 of continuous work at 14:00 — the 6h cap fires
  at the next cell. Row 3's only cell sits past 18:00, outside the schedule. Row 4 occupies the same hours as rows 1, 2, and 3.









The grid view makes two things obvious that the timeline doesn't. **First,** the 6-hour cap breach in Row 2 is visible as soon as the cumulative-hour counter passes 6 — you can *see* the exact cell where the rule fires. **Second,** Row 4's overlap problem is undeniable: its row of red cells sits directly below the same hour-columns occupied by rows 1, 2, and 3. The timeline shows the same data; the grid surfaces the relationships between rows in a way bars stacked vertically can't.


### What the formula does, row by row


Now we trace the algorithm's response. When Sarah hits Submit, OTL packages her four rows into the input arrays we'll dissect later in this post and hands them to your TER formula. The formula walks the rows one at a time, applies its checks, and decides what to flag:


**Row 1 (Regular Hours, 08:30–10:00).** The first real entry. The formula starts a "continuous work" tracker at 8:30, with the stretch currently at 1.5 hours — well below any threshold. Nothing to flag.


**Row 2 (Regular Hours, 10:00–14:45).** The formula looks at this row's start time and sees it matches the previous row's stop time exactly. That's not "two separate work blocks" — that's *continuation of the same block*. The tracker extends the stretch from 8:30 to 14:45, which totals 6 hours and 15 minutes. The continuous-work cap is 6 hours. The formula flags row 2: *"Continuous work exceeds 6 hours."*


**Row 3 (Meal Break, 19:00–20:00).** The formula checks every meal break against the schedule window. Sarah's schedule is 09:00 to 18:00. Her meal at 19:00–20:00 falls outside that window. Row 3 flagged: *"Break outside working hours."*


**Row 4 (Regular Hours, 08:00–20:00).** At every day boundary, the formula compares each Regular Hours entry against every other one to detect overlapping intervals. Row 4 spans 08:00–20:00, which contains row 1's interval, row 2's interval, and row 3's interval. Three overlaps. Row 4 flagged: *"Overlapping entries."*



Expert insight

  Notice that the formula always flags the *later* row in any conflict. Row 1 is clean even though row 4 collides with it — because row 1 was already there when row 4 was added. This matches Sarah's mental model: *the entry I just added is the one that's wrong*. Flagging row 1 instead would turn a previously-correct entry red, which is profoundly confusing for the worker. It's a small UX choice that reflects a deep understanding of how people use timecard software.


### What Sarah sees on screen


The formula's output is a single sparse array called `OUT_MSG`, indexed by row number. Most slots stay empty — those rows passed every check. The flagged rows have error message strings in their slots:


Formula return · sparse output arrayOUT_MSG


```
/* Row 1 has no entry — it's clean. */
OUT_MSG[2] = "Continuous work exceeds 6 hours"
OUT_MSG[3] = "Break outside working hours"
OUT_MSG[4] = "Overlapping entries"
```


The OTL framework reads this array, walks it, and renders red error markers next to rows 2, 3, and 4 in Sarah's timecard screen. Row 1 has no marker because its slot is empty. Sarah now sees clearly which entries are wrong and what each problem is.


She fixes them — deletes row 4 entirely, moves the meal break to a real lunch slot like 12:00–13:00, and breaks up the long stretch by inserting that meal break. Then she resubmits. The formula re-runs from scratch on the corrected timecard. This time, every row passes. The submission goes through to approval, and on to payroll.


That's the entire job of a TER formula in one example: **catch problems early, tell the worker exactly what's wrong, let them fix it before bad data lands in payroll**. Now we'll look at how the formula actually does this internally, starting with the most important thing: the data shape it works with.



Next in The TER Series


Part 2 — The Input Contract


OTL doesn't hand your formula a timecard object. It hands you six parallel arrays with shared row indexes, plus a strict contract about what goes in and what must come out. Part 2 dissects the data shape, every input variable, and the naming conventions that keep production TER code maintainable.



AM




Abhishek Mohanty


Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Time and Labor, Absence Management, Core HR, Redwood, HDL, OTBI.




  [Fast Formula](https://abhishekmohanty-hcm.blogspot.com/search/label/Fast%20Formula)
  [Time Entry Rule](https://abhishekmohanty-hcm.blogspot.com/search/label/Time%20Entry%20Rule)
  [OTL](https://abhishekmohanty-hcm.blogspot.com/search/label/OTL)
  [Time and Labor](https://abhishekmohanty-hcm.blogspot.com/search/label/Time%20and%20Labor)
  [Oracle HCM Cloud](https://abhishekmohanty-hcm.blogspot.com/search/label/Oracle%20HCM%20Cloud)