---
title: "Oracle Fast Formula: Time Entry Rule (Part 1)"
description: "Oracle Fast Formula: Time Entry Rule (Part 1) — Inputs, Contract, and Architecture :root  --ink: #2d2926; --paper: #faf7f2; --rule: #1a1a1a; --accent: #c0392b; --accent-soft: #f4ddd9; --muted: #7a7570"
pubDate: 2026-05-21
tags: ["Fast Formula", "Oracle HCM Cloud", "TER", "Time Entry Rule", "OTL"]
---

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Oracle Fast Formula: Time Entry Rule (Part 1) — Inputs, Contract, and Architecture</title>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

</head><body>
</head><body>

<div class="container">


<div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">Fast Formula</span>
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">Time Entry Rule</span>
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">OTL</span>
<span style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px;">Hands-On</span>
</div>

<div style="font-size:13px; color:#7a7570; margin-bottom:18px;">May 21, 2026 • 14 min read • Oracle HCM Cloud</div>


<div style="background:#f5f1e8; border-left:3px solid #b97417; padding:10px 14px; margin-bottom:24px; border-radius:0 3px 3px 0; font-size:12px;">
<span style="font-weight:700; color:#b97417; letter-spacing:0.5px; text-transform:uppercase; font-size:10px;">The TER Series</span>
<span style="color:#5a544e; margin-left:8px;">Part 1 of 4</span>
<div style="margin-top:6px; color:#7a7570; font-size:11.5px; line-height:1.5;">
    1. OTL Foundations ·
    2. The Input Contract ·
    3. Algorithm: Routing & Overlap ·
    4. The State Machine
</div>
</div>

<h1>Oracle OTL and Where Time Entry Rules Fit<br><span style="color:#7a7570; font-size:0.7em; font-weight:400; font-style:italic;">Part 1 of 4 — The TER Series</span></h1>

<div class="byline">
<div class="avatar">AM</div>

<div class="author-block">
<div class="author-name">Abhishek Mohanty</div>

<div class="author-creds">Oracle ACE Apprentice · AIOUG Member · Oracle HCM Cloud Consultant & Technical Lead</div>

</div>
</div>


<div class="opening">
  Time Entry Rule (TER) formulas live inside Oracle's Time and Labor module — the part of HCM Cloud that workers use to log their hours. This first post in the series introduces what OTL is, where TER sits in its submission flow, and why this is the validation layer where the real business logic lives.
</div>

<h2>What OTL Is</h2>

<p>Oracle Time and Labor (OTL) is the time-tracking module inside Oracle HCM Cloud. Workers log their hours into it through a timecard layout. Managers approve those timecards. The approved data flows downstream to payroll, project costing, or wherever the hours need to land. That's the loop at its simplest.</p>

<p>What makes OTL interesting from a developer's point of view is the extensibility model. Between the worker hitting Submit and the data landing in payroll, OTL runs the timecard through a series of <strong>rule formulas</strong> that you, as the implementer, can write. Each formula type plays a different role:</p>

<ul>
<li><strong>Time Entry Rules (TER)</strong> — run when the worker tries to save or submit. They validate the data and either let it through or flag it with messages the worker can see. <em>This is what the series is about.</em></li>
<li><strong>Time Calculation Rules (TCR)</strong> — run after validation passes. They derive new values from the worker's entries: overtime, premium pay, shift differentials. The worker's original entries stay untouched; TCR adds calculated rows on top.</li>
<li><strong>Time Device Rules (TDR)</strong> — handle integration with physical badge readers and punch clocks. They map raw punch events into the OTL data model.</li>
</ul>

<p>Each rule type sees a different shape of data, gets different inputs from the framework, and is allowed to do different things. TER is the strictest of the three because it runs <em>before</em> the data is accepted — its job is to be a guard. Calculations and device integration come later.</p>

<h2>Why TER Is the Hard One</h2>

<p>OTL's framework gives you some validation for free. If a worker leaves a required field blank, OTL catches it. If they type letters into a numeric field, OTL catches that too. These are <em>declarative validations</em> — you configure them in the timecard layout, and the framework enforces them with no code.</p>

<p>But declarative validation can only check one cell at a time. The validations that actually matter in production are about relationships between cells, between rows, and between days. Things like:</p>

<ul>
<li>"Did this worker take a meal break after 6 hours of continuous work?" — spans multiple rows on the same day</li>
<li>"Do any of these entries overlap with each other?" — pairwise comparison across rows</li>
<li>"Is this meal break inside the worker's scheduled hours?" — requires reading the schedule, which lives elsewhere in HCM</li>
<li>"Has this worker exceeded their weekly hours cap?" — cumulative across days</li>
</ul>

<p>None of these can be expressed in declarative configuration. They need code that loops, remembers, and compares. That's where TER formulas earn their place — and that's where most teams either skip the validation entirely or get it subtly wrong.</p>

<p>This series walks through one production TER formula end-to-end, using a real five-rule validation example. By the end of Part 4 you'll know how the framework hands data to the formula, how the formula loops through it, and how to encode every common validation pattern you'll encounter on a TER implementation.</p>
<h2>What This Formula Does</h2>

<p>The job is straightforward to describe and surprisingly subtle to build. When a worker submits their timecard, OTL needs to verify that what they entered makes sense — not just structurally (which the framework handles for free), but according to the company's actual labour rules.</p>

<div style="background:#fff; padding:48px 36px 56px 36px; margin:32px 0 24px 0; border-radius:8px; border:1px solid #e8e3d8;">

  
<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:36px; flex-wrap:wrap; gap:16px;">
<div>
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:34px; line-height:1.2; font-weight:300; color:#1f5fa8; letter-spacing:-0.5px;">Five rules.</div>

<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:34px; line-height:1.2; font-weight:300; color:#2d2926; letter-spacing:-0.5px; margin-top:4px;">One enforces them all.</div>

</div>

<div style="text-align:right;">
<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:14px; font-weight:700; color:#2d2926; letter-spacing:0.5px;">WHAT THIS FORMULA DOES</div>

<div style="font-family:'Manrope', -apple-system, sans-serif; font-size:11px; color:#7a7570; margin-top:2px; letter-spacing:0.5px;">Validation rules at a glance</div>

</div>

</div>

  

<img src="/diagrams/oracle-fast-formula-time-entry-rule-part-1-fig1.png" alt="Figure 1" style="width:100%;max-width:820px;display:block;margin:24px auto;" />


  
<p style="margin:24px 0 0 0; font-size:13px; color:#5a544e; line-height:1.65; text-align:center;">
    Rules 1 and 3 only need a single row. Rules 2, 4, and 5 are <strong>multi-row validations</strong> — they need to know about other rows on the same day, or remember state from earlier iterations. That single architectural requirement — <em>seeing more than one row at a time</em> — is what separates TER from anything you can do with declarative configuration.
</p>

</div>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:18px 22px; margin:24px 0; font-size:14px; line-height:1.7; color:#2d2926; border-radius:0 4px 4px 0;">
<div style="font-size:10px; letter-spacing:1.8px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Expert framing</div>

<p style="margin-top:0;">Rules 4 and 5 (the continuous-work checks) are the genuinely hard ones — not because the maths is complex, but because they require <strong>state that persists across loop iterations</strong>. You can't just look at row 3 and decide whether continuous work has been exceeded; you need to know what rows 1 and 2 said, whether a meal break has been logged yet, and whether yesterday's data has been correctly cleared.</p>
<p style="margin-bottom:0;">Most TER implementations I've reviewed in client environments either get this wrong (the formula incorrectly extends a stretch across a meal break) or skip it entirely (declaring the validation "out of scope" and pushing it to a manager-review step). Both outcomes are bad. By the end of Part 2, you'll know exactly how to do it right.</p>
</div>

<h3>Where TER fits in OTL's processing chain</h3>

<p>Before we get into the formula's internals, it helps to know where TER sits in OTL's bigger picture. When a worker hits Submit on their timecard, OTL runs through a sequence of stages — and TER is just one of them. Understanding the sequence tells you why TER receives the data it does, and why your validation logic belongs here and not somewhere else.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">


<img src="/diagrams/oracle-fast-formula-time-entry-rule-part-1-fig2.png" alt="Figure 2" style="width:100%;max-width:820px;display:block;margin:24px auto;" />


</div>

<p>The pipeline is sequential and the failure paths are unforgiving. If built-in validations reject the data, your TER never even runs — the timecard bounces back to the worker before reaching Stage 2. If your TER returns errors, the timecard bounces back at Stage 2, before Stages 3 and 4 ever execute. Only when every stage passes does the data land in the time repository where payroll can pick it up.</p>

<p>This sequencing has practical consequences for what your TER should and shouldn't try to do:</p>

<ul>
<li><strong>Don't reimplement Stage 1.</strong> Built-in validations already check that required fields are filled and types are correct. Your TER will never see malformed data, so don't waste code defending against it. Trust the framework.</li>
<li><strong>Don't try to do Stage 3's job.</strong> Calculations like overtime, shift premiums, and allowances belong in TCR formulas, not TER. TER's job is "is this data valid?" — not "what should we pay them?"</li>
<li><strong>Don't push Stage 2 logic into Stage 4.</strong> If a rule has a clear yes/no answer, validate it here. Sending every borderline case to a manager for sign-off creates an approval bottleneck that becomes the team's full-time job.</li>
</ul>

<p>TER is the right home for everything in our five-rule list above — cross-row, calendar-aware, stateful checks with deterministic answers. With that placement clear, let's look at what an actual problem timecard looks like.</p>


<h2>A Real World Example</h2>

<p>The fastest way to understand what a TER formula actually does is to watch one fail a timecard. Abstract talk about "validation rules" and "stateful checks" doesn't stick; a real broken submission does. Let me introduce you to Sarah, a software engineer at a product company. Her workday is scheduled 9:00 AM to 6:00 PM, and her employer has one labour-policy rule worth knowing: <strong>no worker may log more than 6 hours of continuous Regular Hours without a meal break in between</strong>.</p>

<p>Tuesday is a deadline day. Sarah gets pulled into a code review at 10 AM and forgets to take lunch. By 6:15 PM she sits down to fill in her timecard, looks at the half-finished entries she made earlier, decides the rows look "messy," and tries to fix things by adding one big block covering the whole day. Then she clicks Submit.</p>

<p>This is what her timecard looks like at the moment of submission — four rows in OTL's grid, exactly as the framework will hand them to your formula:</p>

<div class="excel-wrap">
<div class="excel-titlebar">
<span class="filename">Sarah_Timecard_14Apr2026.xlsx</span>
<span class="app">Excel</span>
</div>

<table class="excel-sheet">
<thead>
<tr>
<th style="min-width:36px; white-space:nowrap; background:#e8e8e8; color:#555;"> </th>
<th>Date</th>
<th>Time Type</th>
<th>Start Time</th>
<th>Stop Time</th>
<th>Hours</th>
<th>What the formula does</th>
</tr>
</thead>
<tbody>
<tr class="row-clean">
<td class="row-num">1</td>
<td>14-Apr-2026</td>
<td>Regular Hours</td>
<td class="time-cell">08:30</td>
<td class="time-cell">10:00</td>
<td class="num">1.5</td>
<td class="status-cell">✓ Clean — no flag</td>
</tr>
<tr class="row-flagged">
<td class="row-num">2</td>
<td>14-Apr-2026</td>
<td>Regular Hours</td>
<td class="time-cell">10:00</td>
<td class="time-cell">14:45</td>
<td class="num">4.75</td>
<td class="status-cell">✗ Continuous work over 6 hours</td>
</tr>
<tr class="row-flagged">
<td class="row-num">3</td>
<td>14-Apr-2026</td>
<td>Meal Break</td>
<td class="time-cell">19:00</td>
<td class="time-cell">20:00</td>
<td class="num">1.0</td>
<td class="status-cell">✗ Break outside working hours</td>
</tr>
<tr class="row-flagged">
<td class="row-num">4</td>
<td>14-Apr-2026</td>
<td>Regular Hours</td>
<td class="time-cell">08:00</td>
<td class="time-cell">20:00</td>
<td class="num">12.0</td>
<td class="status-cell">✗ Overlapping entries</td>
</tr>
</tbody>
</table>
</div>

<div class="excel-caption">Sarah's submission — one clean row, three problem rows. Before reading the analysis below, take a moment to spot the three errors yourself. They're all visible if you know what to look for.</div>

<h3>The day, drawn on a timeline</h3>

<p>Tables are good for precise data; timelines are better for understanding the <em>shape</em> of a day. Here's Sarah's same four rows plotted against the actual hours of Tuesday, 14 April. The schedule window (9 AM to 6 PM, in pale orange) shows when she was supposed to be working. Each row from the timecard sits as a coloured bar where she logged it:</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">


<img src="/diagrams/oracle-fast-formula-time-entry-rule-part-1-fig3.png" alt="Figure 3" style="width:100%;max-width:820px;display:block;margin:24px auto;" />


</div>

<p>The picture makes the violations visible at a glance:</p>

<ul>
<li><strong>Rows 1 and 2 touch.</strong> Row 1 ends at 10:00 and row 2 starts at 10:00 — no gap. From the formula's perspective this is a single 6h 15m stretch of continuous work, sitting clearly above the 6-hour cap.</li>
<li><strong>Row 3 sits outside the schedule window.</strong> The shaded amber band shows where Sarah was scheduled to work (9 AM to 6 PM). Her meal break at 19:00–20:00 falls a full hour past the schedule's edge. Whatever she was doing then, it wasn't a workplace meal break.</li>
<li><strong>Row 4 covers the entire day in one massive bar.</strong> You can see it physically overlap with rows 1, 2, and 3 simultaneously. This is the consolidated entry Sarah added without removing the originals — three overlap conflicts in a single row.</li>
</ul>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
<div style="font-size:9.5px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Practitioner's tip</div>

  When I'm sketching out a TER's behaviour for a client, I always start with a timeline like this one. Tables hide temporal relationships; timelines surface them. If you're explaining to a non-technical stakeholder why their data is producing strange results, draw a timeline. Five minutes of pen-and-paper sketching will save you an hour of meeting time.
</div>

<h4>The same data as a row-by-hour grid</h4>

<p>The timeline above shows <em>where</em> the entries sit. The grid below shows <em>how each entry occupies hours</em> — one row per timecard entry, one column per hour. Cells light up where the entry is active. The cell numbers count consecutive hours within each entry, so you can see at a glance when an entry crosses a threshold.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04); overflow-x:auto;">


<img src="/diagrams/oracle-fast-formula-time-entry-rule-part-1-fig4.png" alt="Figure 4" style="width:100%;max-width:820px;display:block;margin:24px auto;" />


</div>

<p>The grid view makes two things obvious that the timeline doesn't. <strong>First,</strong> the 6-hour cap breach in Row 2 is visible as soon as the cumulative-hour counter passes 6 — you can <em>see</em> the exact cell where the rule fires. <strong>Second,</strong> Row 4's overlap problem is undeniable: its row of red cells sits directly below the same hour-columns occupied by rows 1, 2, and 3. The timeline shows the same data; the grid surfaces the relationships between rows in a way bars stacked vertically can't.</p>

<h3>What the formula does, row by row</h3>

<p>Now we trace the algorithm's response. When Sarah hits Submit, OTL packages her four rows into the input arrays we'll dissect later in this post and hands them to your TER formula. The formula walks the rows one at a time, applies its checks, and decides what to flag:</p>

<p><strong>Row 1 (Regular Hours, 08:30–10:00).</strong> The first real entry. The formula starts a "continuous work" tracker at 8:30, with the stretch currently at 1.5 hours — well below any threshold. Nothing to flag.</p>

<p><strong>Row 2 (Regular Hours, 10:00–14:45).</strong> The formula looks at this row's start time and sees it matches the previous row's stop time exactly. That's not "two separate work blocks" — that's <em>continuation of the same block</em>. The tracker extends the stretch from 8:30 to 14:45, which totals 6 hours and 15 minutes. The continuous-work cap is 6 hours. The formula flags row 2: <em>"Continuous work exceeds 6 hours."</em></p>

<p><strong>Row 3 (Meal Break, 19:00–20:00).</strong> The formula checks every meal break against the schedule window. Sarah's schedule is 09:00 to 18:00. Her meal at 19:00–20:00 falls outside that window. Row 3 flagged: <em>"Break outside working hours."</em></p>

<p><strong>Row 4 (Regular Hours, 08:00–20:00).</strong> At every day boundary, the formula compares each Regular Hours entry against every other one to detect overlapping intervals. Row 4 spans 08:00–20:00, which contains row 1's interval, row 2's interval, and row 3's interval. Three overlaps. Row 4 flagged: <em>"Overlapping entries."</em></p>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
<div style="font-size:9.5px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Expert insight</div>

  Notice that the formula always flags the <em>later</em> row in any conflict. Row 1 is clean even though row 4 collides with it — because row 1 was already there when row 4 was added. This matches Sarah's mental model: <em>the entry I just added is the one that's wrong</em>. Flagging row 1 instead would turn a previously-correct entry red, which is profoundly confusing for the worker. It's a small UX choice that reflects a deep understanding of how people use timecard software.
</div>

<h3>What Sarah sees on screen</h3>

<p>The formula's output is a single sparse array called <code>OUT_MSG</code>, indexed by row number. Most slots stay empty — those rows passed every check. The flagged rows have error message strings in their slots:</p>

<div class="code-wrap">

<div class="code-header"><span>Formula return · sparse output array</span><span class="label-right">OUT_MSG</span></div>
<pre><code><span class="cm">/* Row 1 has no entry — it's clean. */</span>
<span class="v">OUT_MSG[2]</span> = <span class="s">"Continuous work exceeds 6 hours"</span>
<span class="v">OUT_MSG[3]</span> = <span class="s">"Break outside working hours"</span>
<span class="v">OUT_MSG[4]</span> = <span class="s">"Overlapping entries"</span></code></pre>
</div>

<p>The OTL framework reads this array, walks it, and renders red error markers next to rows 2, 3, and 4 in Sarah's timecard screen. Row 1 has no marker because its slot is empty. Sarah now sees clearly which entries are wrong and what each problem is.</p>

<p>She fixes them — deletes row 4 entirely, moves the meal break to a real lunch slot like 12:00–13:00, and breaks up the long stretch by inserting that meal break. Then she resubmits. The formula re-runs from scratch on the corrected timecard. This time, every row passes. The submission goes through to approval, and on to payroll.</p>

<p>That's the entire job of a TER formula in one example: <strong>catch problems early, tell the worker exactly what's wrong, let them fix it before bad data lands in payroll</strong>. Now we'll look at how the formula actually does this internally, starting with the most important thing: the data shape it works with.</p>






<div style="background:#fff8e8; border:1px solid #b97417; border-radius:6px; padding:20px 24px; margin:40px 0 32px 0;">
<div style="font-size:10px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Next in The TER Series</div>

<div style="font-size:18px; font-weight:700; color:#2d2926; margin-bottom:8px;">Part 2 — The Input Contract</div>

<div style="font-size:13.5px; color:#5a544e; line-height:1.6;">OTL doesn't hand your formula a timecard object. It hands you six parallel arrays with shared row indexes, plus a strict contract about what goes in and what must come out. Part 2 dissects the data shape, every input variable, and the naming conventions that keep production TER code maintainable.</div>
</div>


<hr style="margin:48px 0 32px 0; border:none; border-top:1px solid #e8e3d8;">

<div class="byline">
<div class="avatar">AM</div>

<div class="author-block">
<div class="author-name">Abhishek Mohanty</div>

<div class="author-creds">Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Time and Labor, Absence Management, Core HR, Redwood, HDL, OTBI.</div>

</div>
</div>

<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:24px;">
<a href="https://abhishekmohanty-hcm.blogspot.com/search/label/Fast%20Formula" style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px; text-decoration:none;">Fast Formula</a>
<a href="https://abhishekmohanty-hcm.blogspot.com/search/label/Time%20Entry%20Rule" style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px; text-decoration:none;">Time Entry Rule</a>
<a href="https://abhishekmohanty-hcm.blogspot.com/search/label/OTL" style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px; text-decoration:none;">OTL</a>
<a href="https://abhishekmohanty-hcm.blogspot.com/search/label/Time%20and%20Labor" style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px; text-decoration:none;">Time and Labor</a>
<a href="https://abhishekmohanty-hcm.blogspot.com/search/label/Oracle%20HCM%20Cloud" style="display:inline-block; padding:4px 10px; background:#f5f1e8; color:#2d2926; font-size:11px; font-weight:700; letter-spacing:0.5px; border-radius:2px; text-decoration:none;">Oracle HCM Cloud</a>
</div>

</div>
</body>
</html>