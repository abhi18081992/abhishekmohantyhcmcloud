---
title: "Oracle Fast Formula: Time Entry Rule (Part 2)"
description: "Oracle Fast Formula: Time Entry Rule (Part 1) — Inputs, Contract, and Architecture :root  --ink: #2d2926; --paper: #faf7f2; --rule: #1a1a1a; --accent: #c0392b; --accent-soft: #f4ddd9; --muted: #7a7570"
pubDate: 2026-05-22
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

<div style="font-size:13px; color:#7a7570; margin-bottom:18px;">May 21, 2026 • 15 min read • Oracle HCM Cloud</div>


<div style="background:#f5f1e8; border-left:3px solid #b97417; padding:10px 14px; margin-bottom:24px; border-radius:0 3px 3px 0; font-size:12px;">
  <span style="font-weight:700; color:#b97417; letter-spacing:0.5px; text-transform:uppercase; font-size:10px;">The TER Series</span>
  <span style="color:#5a544e; margin-left:8px;">Part 2 of 4</span>
  <div style="margin-top:6px; color:#7a7570; font-size:11.5px; line-height:1.5;">
    1. OTL Foundations ·
    2. The Input Contract ·
    3. Algorithm: Routing & Overlap ·
    4. The State Machine
  </div>
</div>

<h1>The Input Contract: How OTL Hands Data to Your Formula<br><span style="color:#7a7570; font-size:0.7em; font-weight:400; font-style:italic;">Part 2 of 4 — The TER Series</span></h1>

<div class="byline">
  <div class="avatar">AM</div>

  <div class="author-block">
    <div class="author-name">Abhishek Mohanty</div>

    <div class="author-creds">Oracle ACE Apprentice · AIOUG Member · Oracle HCM Cloud Consultant & Technical Lead</div>

  </div>
</div>

<div class="opening">In Part 1 we saw what TER does and where it fits in OTL's submission flow. Now we look at the data the framework hands your formula — the input array contract, the seven input variables, and the naming conventions that keep production code readable.</div>

<h2>The Input Array Contract</h2>

<p>Here's the single most important thing to internalise before you write any code: <strong>the timecard the worker sees is not the timecard your formula receives</strong>. OTL inserts extra rows between the worker's entries to mark structural boundaries — where each day starts, where it ends, where the whole period closes out. Miss this distinction and your loop counter, your day-buffer logic, and your <code>.exists()</code> guards will all be subtly wrong. Get it right, and the rest of the formula falls into place naturally.</p>

<p>I'll show you both views, then a transformation diagram that bridges them, then the formal contract.</p>

<h3>The view the worker sees</h3>

<p>When Sarah opens her timecard, she's looking at a spreadsheet-like grid. She types entries one row at a time. Here's what her week looks like after she's done entering Tuesday and Wednesday:</p>

<div class="excel-wrap">
  <div class="excel-titlebar">
    <span class="filename">My_Timecard_Week_14Apr2026.xlsx</span>
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
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="row-num">1</td>
        <td>14-Apr-2026 (Tue)</td>
        <td>Regular Hours</td>
        <td class="time-cell">09:00</td>
        <td class="time-cell">12:00</td>
        <td class="num">3.0</td>
      </tr>
      <tr>
        <td class="row-num">2</td>
        <td>14-Apr-2026 (Tue)</td>
        <td>Meal Break</td>
        <td class="time-cell">12:00</td>
        <td class="time-cell">13:00</td>
        <td class="num">1.0</td>
      </tr>
      <tr>
        <td class="row-num">3</td>
        <td>14-Apr-2026 (Tue)</td>
        <td>Regular Hours</td>
        <td class="time-cell">13:00</td>
        <td class="time-cell">18:00</td>
        <td class="num">5.0</td>
      </tr>
      <tr>
        <td class="row-num">4</td>
        <td>15-Apr-2026 (Wed)</td>
        <td>Regular Hours</td>
        <td class="time-cell">09:00</td>
        <td class="time-cell">18:00</td>
        <td class="num">8.0</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="excel-caption">Four entries across two days — this is exactly what Sarah types into OTL. Clean, simple, no surprises.</div>

<h3>What OTL does between submission and your formula</h3>

<p>The moment Sarah hits Submit, OTL's pre-processor wakes up. It can't just hand the formula four rows of data — the formula needs to know where day boundaries fall, where the period ends, and where to pause for day-level processing like overlap detection. So OTL inserts <strong>marker rows</strong> at the structural breakpoints. The diagram below shows exactly what changes:</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<svg viewBox="0 0 760 440" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:760px; display:block; margin:0 auto;" font-family="Calibri, sans-serif">

  <text x="380" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#2d2926">From Worker's View to Formula's View</text>
  <text x="380" y="40" text-anchor="middle" font-size="11" fill="#7a7570">OTL injects three kinds of markers before your formula runs</text>

  
  <text x="170" y="68" text-anchor="middle" font-size="12" font-weight="700" fill="#4472c4">WORKER'S VIEW · 4 rows</text>
  <text x="170" y="82" text-anchor="middle" font-size="9.5" fill="#5a544e" font-style="italic">What Sarah sees on the timecard screen</text>

  
  <g transform="translate(40, 96)">
    <rect x="0" y="0" width="260" height="32" rx="2" fill="#fff" stroke="#4472c4" stroke-width="1"/>
    <text x="10" y="14" font-size="9.5" font-weight="700" fill="#4472c4">Row 1</text>
    <text x="10" y="26" font-size="10" fill="#2d2926">Tue 14-Apr · Reg Hours · 09:00–12:00</text>

    <rect x="0" y="38" width="260" height="32" rx="2" fill="#fff" stroke="#4472c4" stroke-width="1"/>
    <text x="10" y="52" font-size="9.5" font-weight="700" fill="#4472c4">Row 2</text>
    <text x="10" y="64" font-size="10" fill="#2d2926">Tue 14-Apr · Meal Break · 12:00–13:00</text>

    <rect x="0" y="76" width="260" height="32" rx="2" fill="#fff" stroke="#4472c4" stroke-width="1"/>
    <text x="10" y="90" font-size="9.5" font-weight="700" fill="#4472c4">Row 3</text>
    <text x="10" y="102" font-size="10" fill="#2d2926">Tue 14-Apr · Reg Hours · 13:00–18:00</text>

    <rect x="0" y="114" width="260" height="32" rx="2" fill="#fff" stroke="#4472c4" stroke-width="1"/>
    <text x="10" y="128" font-size="9.5" font-weight="700" fill="#4472c4">Row 4</text>
    <text x="10" y="140" font-size="10" fill="#2d2926">Wed 15-Apr · Reg Hours · 09:00–18:00</text>
  </g>

  
  <g transform="translate(310, 144)">
    <line x1="0" y1="0" x2="40" y2="0" stroke="#b97417" stroke-width="3" marker-end="url(#arrowT1)"/>
    <text x="20" y="-10" text-anchor="middle" font-size="11" font-weight="700" fill="#b97417">OTL inserts</text>
    <text x="20" y="20" text-anchor="middle" font-size="11" font-weight="700" fill="#b97417">markers</text>
  </g>

  
  <text x="580" y="68" text-anchor="middle" font-size="12" font-weight="700" fill="#c0392b">FORMULA'S VIEW · 8 indexes</text>
  <text x="580" y="82" text-anchor="middle" font-size="9.5" fill="#5a544e" font-style="italic">What your TER formula receives via INPUTS ARE</text>

  <g transform="translate(380, 96)">
    
    <rect x="0" y="0" width="380" height="32" rx="2" fill="#fff3e0" stroke="#b97417" stroke-width="1.5"/>
    <text x="10" y="14" font-size="9.5" font-weight="700" fill="#b97417">[1] HEADER</text>
    <text x="10" y="26" font-size="10" fill="#2d2926" font-style="italic">Marker · "timecard begins"</text>

    
    <rect x="0" y="38" width="380" height="32" rx="2" fill="#fff" stroke="#7a7570" stroke-width="1"/>
    <text x="10" y="52" font-size="9.5" font-weight="700" fill="#5a544e">[2]  —  (was Row 1)</text>
    <text x="10" y="64" font-size="10" fill="#2d2926">Reg Hours · 09:00–12:00</text>

    
    <rect x="0" y="76" width="380" height="32" rx="2" fill="#fff" stroke="#7a7570" stroke-width="1"/>
    <text x="10" y="90" font-size="9.5" font-weight="700" fill="#5a544e">[3]  —  (was Row 2)</text>
    <text x="10" y="102" font-size="10" fill="#2d2926">Meal Break · 12:00–13:00</text>

    
    <rect x="0" y="114" width="380" height="32" rx="2" fill="#fff" stroke="#7a7570" stroke-width="1"/>
    <text x="10" y="128" font-size="9.5" font-weight="700" fill="#5a544e">[4]  —  (was Row 3)</text>
    <text x="10" y="140" font-size="10" fill="#2d2926">Reg Hours · 13:00–18:00</text>

    
    <rect x="0" y="152" width="380" height="32" rx="2" fill="#fce8e8" stroke="#c0392b" stroke-width="1.5"/>
    <text x="10" y="166" font-size="9.5" font-weight="700" fill="#c0392b">[5] END_DAY</text>
    <text x="10" y="178" font-size="10" fill="#2d2926" font-style="italic">Marker · "Tuesday is complete — run day-level checks now"</text>

    
    <rect x="0" y="190" width="380" height="32" rx="2" fill="#fff" stroke="#7a7570" stroke-width="1"/>
    <text x="10" y="204" font-size="9.5" font-weight="700" fill="#5a544e">[6]  —  (was Row 4)</text>
    <text x="10" y="216" font-size="10" fill="#2d2926">Reg Hours · 09:00–18:00 (Wed)</text>

    
    <rect x="0" y="228" width="380" height="32" rx="2" fill="#fce8e8" stroke="#c0392b" stroke-width="1.5"/>
    <text x="10" y="242" font-size="9.5" font-weight="700" fill="#c0392b">[7] END_DAY</text>
    <text x="10" y="254" font-size="10" fill="#2d2926" font-style="italic">Marker · "Wednesday is complete — run day-level checks now"</text>

    
    <rect x="0" y="266" width="380" height="32" rx="2" fill="#fce8e8" stroke="#c0392b" stroke-width="1.5"/>
    <text x="10" y="280" font-size="9.5" font-weight="700" fill="#c0392b">[8] END_PERIOD</text>
    <text x="10" y="292" font-size="10" fill="#2d2926" font-style="italic">Marker · "Whole timecard is complete — loop ends"</text>
  </g>

  
  <line x1="300" y1="120" x2="380" y2="146" stroke="#7a7570" stroke-width="0.7" stroke-dasharray="2,2"/>
  <line x1="300" y1="156" x2="380" y2="184" stroke="#7a7570" stroke-width="0.7" stroke-dasharray="2,2"/>
  <line x1="300" y1="194" x2="380" y2="222" stroke="#7a7570" stroke-width="0.7" stroke-dasharray="2,2"/>
  <line x1="300" y1="232" x2="380" y2="298" stroke="#7a7570" stroke-width="0.7" stroke-dasharray="2,2"/>

  
  <rect x="40" y="404" width="700" height="32" rx="3" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
  <text x="56" y="420" font-size="10.5" font-weight="700" fill="#c0392b">KEY INSIGHT</text>
  <text x="56" y="434" font-size="11" fill="#2d2926">The worker's "row 1" is the formula's "index [2]". Always remember the offset — loop counters start at 1 because of the HEADER.</text>

  <defs>
    <marker id="arrowT1" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M0,0 L0,8 L8,4 z" fill="#b97417"/>
    </marker>
  </defs>

</svg>

</div>

<p>Three things to take away from this diagram:</p>

<ul>
  <li><strong>HEADER always sits at index [1].</strong> Your loop counter starts at 1, but you'll never read real worker data at that index. The first real entry begins at [2].</li>
  <li><strong>END_DAY appears wherever a calendar day ends.</strong> If the timecard period covers seven days, expect seven END_DAY markers (one for each day, even if some days have zero worker entries).</li>
  <li><strong>END_PERIOD always sits at the very last index.</strong> When your formula's loop sees END_PERIOD, you're done.</li>
</ul>

<p>Here's the same eight-row view as a table, with the original column names OTL uses:</p>

<h3>The view the formula sees, as a table</h3>

<div class="excel-wrap">
  <div class="excel-titlebar">
    <span class="filename">As_The_Formula_Sees_It.xlsx</span>
    <span class="app">Excel</span>
  </div>

  <table class="excel-sheet">
    <thead>
      <tr>
        <th style="min-width:36px; white-space:nowrap; background:#e8e8e8; color:#555;">Idx</th>
        <th>Record Position</th>
        <th>Time Type</th>
        <th>Start Time</th>
        <th>Stop Time</th>
        <th>Hours</th>
      </tr>
    </thead>
    <tbody>
      <tr style="background:#fff3e0;">
        <td class="row-num" style="background:#ffd180;">[1]</td>
        <td><strong>HEADER</strong></td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
      </tr>
      <tr>
        <td class="row-num">[2]</td>
        <td style="color:#999;">—</td>
        <td>Regular Hours</td>
        <td class="time-cell">09:00</td>
        <td class="time-cell">12:00</td>
        <td class="num">3.0</td>
      </tr>
      <tr>
        <td class="row-num">[3]</td>
        <td style="color:#999;">—</td>
        <td>Meal Break</td>
        <td class="time-cell">12:00</td>
        <td class="time-cell">13:00</td>
        <td class="num">1.0</td>
      </tr>
      <tr>
        <td class="row-num">[4]</td>
        <td style="color:#999;">—</td>
        <td>Regular Hours</td>
        <td class="time-cell">13:00</td>
        <td class="time-cell">18:00</td>
        <td class="num">5.0</td>
      </tr>
      <tr style="background:#fce8e8;">
        <td class="row-num" style="background:#f5cccc;">[5]</td>
        <td style="color:#c0392b;"><strong>END_DAY</strong></td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
      </tr>
      <tr>
        <td class="row-num">[6]</td>
        <td style="color:#999;">—</td>
        <td>Regular Hours</td>
        <td class="time-cell">09:00</td>
        <td class="time-cell">18:00</td>
        <td class="num">8.0</td>
      </tr>
      <tr style="background:#fce8e8;">
        <td class="row-num" style="background:#f5cccc;">[7]</td>
        <td style="color:#c0392b;"><strong>END_DAY</strong></td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
      </tr>
      <tr style="background:#fce8e8;">
        <td class="row-num" style="background:#f5cccc;">[8]</td>
        <td style="color:#c0392b;"><strong>END_PERIOD</strong></td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="excel-caption">Same four entries, now wrapped with HEADER, END_DAY, and END_PERIOD marker rows. Notice the dashes — marker rows have no time-type, no punches, no hours. Trying to read those slots will crash your formula.</div>

<h3>How the formula reads it — three questions per row</h3>

<p>For every index from [1] to [N], your formula asks the same three questions in order. The answers determine the entire flow of validation logic:</p>

<p><strong>Question 1: Is this a marker row?</strong> Read <code>RECORD_POSITIONS[idx]</code>. If it's HEADER, skip everything; if it's END_DAY, run day-level checks (overlap detection, day buffer reset); if it's END_PERIOD, the loop ends; if it's empty, this is a real worker entry — proceed to Question 2.</p>

<p><strong>Question 2: What kind of time type?</strong> Read <code>PayrollTimeType[idx]</code>. Regular Hours go through the continuous-work tracker and the day buffer for overlap testing. Meal Break runs through the schedule-window check and signals "the worker took a break." Other types (Annual Leave, Sick Leave) typically pass through with no validation.</p>

<p><strong>Question 3: What are the exact punch times?</strong> Read <code>StartTime[idx]</code> and <code>StopTime[idx]</code>. Use them for stretch tracking, overlap math, qty-only detection, and any time-window checks.</p>

<div style="background:#fff5f0; border-left:4px solid #c0392b; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
  <div style="font-size:9.5px; letter-spacing:1.6px; color:#c0392b; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Production trap</div>

  Marker rows are why you can't read input arrays directly. <code>StartTime[1]</code> doesn't exist as a value — HEADER rows have no punch time. Read it without protection and Fast Formula throws a runtime error and crashes the whole submission. Every read in the formula must be wrapped in <code>.exists()</code>:
  <div style="background:#1f1c19; color:#e6e1d8; padding:10px 14px; margin-top:10px; border-radius:3px; font-family:'JetBrains Mono', monospace; font-size:11px;">
IF (StartTime.exists(nidx)) THEN ( aiStartTime = StartTime[nidx] )
  </div>

  Skip this guard and the formula passes UAT cleanly — test data rarely covers the edge case — then breaks day one in production when a real submission arrives. <strong>This is the single most common reason a TER formula goes live and immediately blocks every submission</strong>. Don't be that consultant.
</div>

<h3>The Formula's Contract: What Goes In, What Comes Out</h3>

<p class="section-lead">A Time Entry Rule formula is like a checkpoint at the airport. The OTL framework hands it a stack of paperwork (the timecard rows), the formula inspects every page, and hands back a list of which pages have problems. The framework defines exactly what shape that paperwork arrives in and exactly what shape the response must take — that's the <strong>contract</strong>. Neither side can deviate.</p>

<div class="excel-wrap">
  <div class="excel-titlebar">
    <span class="filename">The_Contract_at_a_Glance.xlsx</span>
    <span class="app">Excel</span>
  </div>

  <table class="excel-sheet">
    <thead>
      <tr>
        <th>Direction</th>
        <th>Variable</th>
        <th>Type</th>
        <th>What it represents</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong style="color:#4472c4;">IN</strong></td>
        <td><code>HWM_CTXARY_RECORD_POSITIONS</code></td>
        <td>Text array</td>
        <td>Which rows are markers (HEADER, END_DAY) vs real entries</td>
      </tr>
      <tr style="opacity:0.6;">
        <td><strong style="color:#4472c4;">IN</strong></td>
        <td><code>HWM_CTXARY_HWM_MEASURE_DAY</code></td>
        <td>Number array</td>
        <td>Day-aggregated total (declared but unused by this formula)</td>
      </tr>
      <tr>
        <td><strong style="color:#4472c4;">IN</strong></td>
        <td><code>measure</code></td>
        <td>Number array</td>
        <td>Hours value for each row</td>
      </tr>
      <tr>
        <td><strong style="color:#4472c4;">IN</strong></td>
        <td><code>PayrollTimeType</code></td>
        <td>Text array</td>
        <td>What kind of time (Regular Hours, Meal Break, Annual Leave...)</td>
      </tr>
      <tr>
        <td><strong style="color:#4472c4;">IN</strong></td>
        <td><code>StartTime</code></td>
        <td>Date array</td>
        <td>Punch-in timestamp for each row</td>
      </tr>
      <tr>
        <td><strong style="color:#4472c4;">IN</strong></td>
        <td><code>StopTime</code></td>
        <td>Date array</td>
        <td>Punch-out timestamp for each row</td>
      </tr>
      <tr style="background:#fce8e8;">
        <td><strong style="color:#c0392b;">OUT</strong></td>
        <td><code>OUT_MSG</code></td>
        <td>Text array (sparse)</td>
        <td>Error message for each flagged row, empty for clean rows</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="excel-caption">Six inputs in. One output out. The framework enforces these names exactly — misspell one, omit one, return anything else, and the formula won't even compile.</div>

<h4>Three things to understand before reading further</h4>

<p>Before walking through each input one by one, hold these three properties in mind. Every line of code in this formula respects all three; understanding them now means the source reads naturally later.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:18px 0;">
  <div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram · The three properties of the input/output shape</div>

  <svg viewBox="0 0 720 600" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:720px; display:block;" font-family="Calibri, sans-serif">

    
    <text x="20" y="20" font-size="11" font-weight="700" fill="#4472c4">PROPERTY 1 · Six parallel arrays, not records — one row spans six columns at the same index</text>

    
    <g transform="translate(20, 36)">
      
      <rect x="0" y="0" width="40" height="22" fill="#1f1c19"/>
      <text x="20" y="15" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">Idx</text>

      
      <rect x="40" y="0" width="106" height="22" fill="#dbe5f4" stroke="#4472c4" stroke-width="0.8"/>
      <text x="93" y="15" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">RECORD_POSITIONS</text>
      <rect x="146" y="0" width="106" height="22" fill="#dbe5f4" stroke="#4472c4" stroke-width="0.8"/>
      <text x="199" y="15" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">PayrollTimeType</text>
      <rect x="252" y="0" width="106" height="22" fill="#dbe5f4" stroke="#4472c4" stroke-width="0.8"/>
      <text x="305" y="15" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">StartTime</text>
      <rect x="358" y="0" width="106" height="22" fill="#dbe5f4" stroke="#4472c4" stroke-width="0.8"/>
      <text x="411" y="15" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">StopTime</text>
      <rect x="464" y="0" width="106" height="22" fill="#dbe5f4" stroke="#4472c4" stroke-width="0.8"/>
      <text x="517" y="15" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">measure</text>
      <rect x="570" y="0" width="106" height="22" fill="#dbe5f4" stroke="#4472c4" stroke-width="0.8"/>
      <text x="623" y="15" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">HWM_MEASURE_DAY</text>

      
      <rect x="0" y="22" width="40" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="20" y="42" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">[3]</text>

      <rect x="40" y="22" width="106" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="93" y="42" text-anchor="middle" font-size="9.5" fill="#999" font-style="italic">empty</text>
      <rect x="146" y="22" width="106" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="199" y="42" text-anchor="middle" font-size="9.5" fill="#2d2926">Meal Break</text>
      <rect x="252" y="22" width="106" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="305" y="42" text-anchor="middle" font-size="9.5" fill="#2d2926">12:00</text>
      <rect x="358" y="22" width="106" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="411" y="42" text-anchor="middle" font-size="9.5" fill="#2d2926">13:00</text>
      <rect x="464" y="22" width="106" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="517" y="42" text-anchor="middle" font-size="9.5" fill="#2d2926">1.0</text>
      <rect x="570" y="22" width="106" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="623" y="42" text-anchor="middle" font-size="9.5" fill="#999" font-style="italic">unused</text>
    </g>

    <text x="20" y="100" font-size="10" fill="#5a544e">To work with row 3, the formula reads <tspan font-family="JetBrains Mono, monospace" fill="#c0392b">RECORD_POSITIONS[3]</tspan>, <tspan font-family="JetBrains Mono, monospace" fill="#c0392b">PayrollTimeType[3]</tspan>, <tspan font-family="JetBrains Mono, monospace" fill="#c0392b">StartTime[3]</tspan>...</text>
    <text x="20" y="116" font-size="10" fill="#5a544e">across all six arrays. There's no single row object — each row is reassembled at read time from the parallel slices.</text>

    
    <text x="20" y="148" font-size="11" font-weight="700" fill="#4472c4">PROPERTY 2 · Not every row populates every column — marker rows are sparse</text>

    
    <g transform="translate(20, 164)">
      <rect x="0" y="0" width="40" height="22" fill="#e8e8e8" stroke="#999"/>
      <text x="20" y="15" text-anchor="middle" font-size="9.5" font-weight="700" fill="#5a544e">Idx</text>

      <rect x="40" y="0" width="106" height="22" fill="#dbe5f4" stroke="#4472c4"/>
      <text x="93" y="15" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">RECORD_POSITIONS</text>
      <rect x="146" y="0" width="424" height="22" fill="#dbe5f4" stroke="#4472c4"/>
      <text x="358" y="15" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">All other arrays (PayrollTimeType, StartTime, StopTime, measure, HWM_MEASURE_DAY)</text>

      
      <rect x="0" y="22" width="40" height="22" fill="#fff8e7" stroke="#999"/>
      <text x="20" y="37" text-anchor="middle" font-size="9.5" font-weight="700" fill="#5a544e">[1]</text>
      <rect x="40" y="22" width="106" height="22" fill="#fff8e7" stroke="#b97417"/>
      <text x="93" y="37" text-anchor="middle" font-size="9" font-weight="700" fill="#b97417">HEADER</text>
      <rect x="146" y="22" width="424" height="22" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
      <text x="358" y="37" text-anchor="middle" font-size="9.5" font-style="italic" fill="#c0392b">missing — reading any of these crashes with FFL-09100</text>

      
      <rect x="0" y="44" width="40" height="22" fill="#fff" stroke="#999"/>
      <text x="20" y="59" text-anchor="middle" font-size="9.5" font-weight="700" fill="#5a544e">[2]</text>
      <rect x="40" y="44" width="106" height="22" fill="#fff" stroke="#999"/>
      <text x="93" y="59" text-anchor="middle" font-size="9.5" fill="#999" font-style="italic">empty</text>
      <rect x="146" y="44" width="424" height="22" fill="#fff" stroke="#999"/>
      <text x="358" y="59" text-anchor="middle" font-size="9.5" fill="#27704a">all populated — safe to read</text>

      
      <rect x="0" y="66" width="40" height="22" fill="#fce8e8" stroke="#999"/>
      <text x="20" y="81" text-anchor="middle" font-size="9.5" font-weight="700" fill="#5a544e">[5]</text>
      <rect x="40" y="66" width="106" height="22" fill="#fce8e8" stroke="#c0392b"/>
      <text x="93" y="81" text-anchor="middle" font-size="9" font-weight="700" fill="#c0392b">END_DAY</text>
      <rect x="146" y="66" width="424" height="22" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
      <text x="358" y="81" text-anchor="middle" font-size="9.5" font-style="italic" fill="#c0392b">missing — reading any of these crashes with FFL-09100</text>
    </g>

    <text x="20" y="270" font-size="10" fill="#5a544e">Every read in the formula must be wrapped in <tspan font-family="JetBrains Mono, monospace" fill="#c0392b">.exists(nidx)</tspan> — check first, then read.</text>

    
    <rect x="20" y="284" width="680" height="22" rx="3" fill="#1f1c19"/>
    <text x="34" y="300" font-size="10" font-family="JetBrains Mono, monospace" fill="#7fc8a0">IF (StartTime.exists(nidx)) THEN aiStartTime = StartTime[nidx]</text>

    
    <text x="20" y="332" font-size="11" font-weight="700" fill="#4472c4">PROPERTY 3 · The output is sparse, not dense — only flagged rows get an entry</text>

    
    <g transform="translate(20, 348)">
      
      <text x="100" y="14" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">5 timecard rows</text>

      <rect x="0" y="22" width="200" height="24" fill="#fff" stroke="#27704a"/>
      <text x="100" y="38" text-anchor="middle" font-size="9.5" fill="#27704a">[1] HEADER — clean</text>

      <rect x="0" y="48" width="200" height="24" fill="#fff" stroke="#27704a"/>
      <text x="100" y="64" text-anchor="middle" font-size="9.5" fill="#27704a">[2] Reg 09—12 — clean</text>

      <rect x="0" y="74" width="200" height="24" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
      <text x="100" y="90" text-anchor="middle" font-size="9.5" fill="#c0392b" font-weight="700">[3] Meal — outside hours</text>

      <rect x="0" y="100" width="200" height="24" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
      <text x="100" y="116" text-anchor="middle" font-size="9.5" fill="#c0392b" font-weight="700">[4] Reg — overlaps row 2</text>

      <rect x="0" y="126" width="200" height="24" fill="#fff" stroke="#27704a"/>
      <text x="100" y="142" text-anchor="middle" font-size="9.5" fill="#27704a">[5] END_DAY — clean</text>

      
      <line x1="200" y1="86" x2="280" y2="86" stroke="#7a7570" stroke-width="1.5" marker-end="url(#arrowP3)"/>
      <text x="240" y="80" text-anchor="middle" font-size="9" fill="#7a7570" font-style="italic">flag rows</text>
      <text x="240" y="92" text-anchor="middle" font-size="9" fill="#7a7570" font-style="italic">3 and 4 only</text>

      
      <text x="500" y="14" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">OUT_MSG · only 2 entries</text>

      <rect x="290" y="22" width="60" height="24" fill="#f5f5f5" stroke="#999"/>
      <text x="320" y="38" text-anchor="middle" font-size="9" fill="#7a7570">[1]</text>
      <rect x="350" y="22" width="350" height="24" fill="#f5f5f5" stroke="#999"/>
      <text x="525" y="38" text-anchor="middle" font-size="9" fill="#999" font-style="italic">no entry — row stayed clean</text>

      <rect x="290" y="48" width="60" height="24" fill="#f5f5f5" stroke="#999"/>
      <text x="320" y="64" text-anchor="middle" font-size="9" fill="#7a7570">[2]</text>
      <rect x="350" y="48" width="350" height="24" fill="#f5f5f5" stroke="#999"/>
      <text x="525" y="64" text-anchor="middle" font-size="9" fill="#999" font-style="italic">no entry — row stayed clean</text>

      <rect x="290" y="74" width="60" height="24" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
      <text x="320" y="90" text-anchor="middle" font-size="9" fill="#c0392b" font-weight="700">[3]</text>
      <rect x="350" y="74" width="350" height="24" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
      <text x="360" y="90" font-size="9" fill="#2d2926">"Break outside working hours"</text>

      <rect x="290" y="100" width="60" height="24" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
      <text x="320" y="116" text-anchor="middle" font-size="9" fill="#c0392b" font-weight="700">[4]</text>
      <rect x="350" y="100" width="350" height="24" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
      <text x="360" y="116" font-size="9" fill="#2d2926">"Overlapping entries"</text>

      <rect x="290" y="126" width="60" height="24" fill="#f5f5f5" stroke="#999"/>
      <text x="320" y="142" text-anchor="middle" font-size="9" fill="#7a7570">[5]</text>
      <rect x="350" y="126" width="350" height="24" fill="#f5f5f5" stroke="#999"/>
      <text x="525" y="142" text-anchor="middle" font-size="9" fill="#999" font-style="italic">no entry — row stayed clean</text>
    </g>

    <text x="20" y="514" font-size="10" fill="#5a544e">The framework reads OUT_MSG when the formula returns and renders red error markers on whatever indexes appear.</text>
    <text x="20" y="528" font-size="10" fill="#5a544e"><tspan font-weight="700">Quiet rows stay quiet.</tspan> Clean rows have nothing to say — so they say nothing.</text>

    
    <rect x="20" y="552" width="680" height="34" rx="3" fill="#1f1c19"/>
    <text x="34" y="570" font-size="10.5" font-family="JetBrains Mono, monospace" fill="#e6e1d8">SUMMARY:</text>
    <text x="120" y="570" font-size="10" fill="#a8a39c">Six parallel arrays in. One sparse array out. Wrap every read in .exists().</text>
    <text x="34" y="582" font-size="10" fill="#e6e1d8">Internalise these three properties — the entire formula source is a direct expression of them.</text>

    <defs>
      <marker id="arrowP3" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto" markerUnits="userSpaceOnUse">
        <path d="M0,0 L0,9 L9,4.5 z" fill="#7a7570"/>
      </marker>
    </defs>

  </svg>
</div>

<p><strong>1. The inputs are parallel arrays, not records.</strong> Most languages would express a row of timecard data as a single object with named fields: <code>{type, start, stop, hours}</code>. Fast Formula doesn't have records like that. Instead, the framework gives the formula six separate arrays, all sharing the same row index. Row 3 of the timecard is <code>RECORD_POSITIONS[3]</code>, <code>StartTime[3]</code>, <code>StopTime[3]</code>, <code>PayrollTimeType[3]</code>, and <code>measure[3]</code>, each holding one column of that row's data. To work with a single row, you read the same index across all six arrays.</p>

<p><strong>2. Not every row populates every column.</strong> Marker rows (HEADER, END_DAY, END_PERIOD) only fill <code>RECORD_POSITIONS</code> — the other arrays have no slot at those indexes. Trying to read <code>StartTime[1]</code> on a HEADER row would crash. This is why every read in the formula is wrapped in <code>.exists(nidx)</code> — the formula has to check whether a slot is populated before reading from it.</p>

<p><strong>3. The output is sparse, not dense.</strong> <code>OUT_MSG</code> doesn't have one entry per timecard row — it only has entries for the rows the formula chose to flag. A clean row leaves its slot empty. The framework reads <code>OUT_MSG</code> when the formula returns and renders red error markers next to whatever row indexes appear in the array. Quiet rows stay quiet.</p>

<h4>The expert's view: framing the inputs before reading the names</h4>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:18px 22px; margin:24px 0; font-size:14px; line-height:1.7; color:#2d2926; border-radius:0 4px 4px 0;">
  <div style="font-size:10px; letter-spacing:1.8px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Expert framing</div>

  <p style="margin-top:0;">When I'm reviewing a junior developer's first TER formula, the question I always hear is: <em>"Why are some inputs called <code>HWM_CTXARY_RECORD_POSITIONS</code> and others just <code>StartTime</code>?"</em> The answer isn't really about names — it's about <strong>what kind of data each input represents</strong>, and Oracle's naming conventions reflect that distinction once you see the pattern.</p>
  <p style="margin-bottom:0;">Fast Formula isn't a general-purpose programming language. It's a <strong>rule engine plugged into specific HCM modules</strong>. Each module (Payroll, Absence, Time and Labor, Benefits) defines its own <em>formula types</em>, and each formula type is a contract: <em>"If you write a formula of this type, you'll receive these inputs and you must return these outputs."</em> The TER formula type is one such contract, defined inside OTL. The six inputs we're about to dissect aren't arbitrary — they're exactly what OTL's validation pipeline hands every TER formula by design.</p>
</div>

<h4>How a TER formula fits into OTL's bigger picture</h4>

<p>To understand the inputs, you first need to see where the formula fires within OTL. A TER formula doesn't run in isolation — it sits inside a five-stage pipeline that begins the moment a worker clicks Submit on their timecard:</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<svg viewBox="0 0 760 420" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:760px; display:block; margin:0 auto;" font-family="Calibri, sans-serif">

  <text x="380" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#2d2926">OTL Validation Pipeline — Where TER Formulas Run</text>
  <text x="380" y="40" text-anchor="middle" font-size="11" fill="#7a7570">Five stages from worker submission to UI feedback. The TER formula fires in Stage 3.</text>

  
  <rect x="30" y="70" width="130" height="80" rx="4" fill="#fff" stroke="#4472c4" stroke-width="1.5"/>
  <rect x="30" y="70" width="130" height="20" rx="4" fill="#4472c4"/>
  <text x="95" y="85" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">STAGE 1</text>
  <text x="95" y="108" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">Worker submits</text>
  <text x="95" y="124" text-anchor="middle" font-size="10" fill="#5a544e">Timecard rows</text>
  <text x="95" y="138" text-anchor="middle" font-size="10" fill="#5a544e">leave the UI</text>

  
  <line x1="160" y1="110" x2="178" y2="110" stroke="#7a7570" stroke-width="2" marker-end="url(#arrow2)"/>

  
  <rect x="180" y="70" width="130" height="80" rx="4" fill="#fff" stroke="#4472c4" stroke-width="1.5"/>
  <rect x="180" y="70" width="130" height="20" rx="4" fill="#4472c4"/>
  <text x="245" y="85" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">STAGE 2</text>
  <text x="245" y="108" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">OTL pre-processes</text>
  <text x="245" y="124" text-anchor="middle" font-size="10" fill="#5a544e">Inserts markers,</text>
  <text x="245" y="138" text-anchor="middle" font-size="10" fill="#5a544e">shapes data into arrays</text>

  
  <line x1="310" y1="110" x2="328" y2="110" stroke="#7a7570" stroke-width="2" marker-end="url(#arrow2)"/>

  
  <rect x="330" y="62" width="160" height="96" rx="4" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
  <rect x="330" y="62" width="160" height="22" rx="4" fill="#c0392b"/>
  <text x="410" y="78" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">STAGE 3 · YOUR FORMULA</text>
  <text x="410" y="106" text-anchor="middle" font-size="12" font-weight="700" fill="#c0392b">TER formula runs</text>
  <text x="410" y="122" text-anchor="middle" font-size="10" fill="#5a544e">Reads the 6 input arrays,</text>
  <text x="410" y="136" text-anchor="middle" font-size="10" fill="#5a544e">populates OUT_MSG,</text>
  <text x="410" y="150" text-anchor="middle" font-size="10" fill="#5a544e">returns to OTL</text>

  
  <line x1="490" y1="110" x2="508" y2="110" stroke="#7a7570" stroke-width="2" marker-end="url(#arrow2)"/>

  
  <rect x="510" y="70" width="130" height="80" rx="4" fill="#fff" stroke="#27704a" stroke-width="1.5"/>
  <rect x="510" y="70" width="130" height="20" rx="4" fill="#27704a"/>
  <text x="575" y="85" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">STAGE 4</text>
  <text x="575" y="108" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">OTL collects results</text>
  <text x="575" y="124" text-anchor="middle" font-size="10" fill="#5a544e">Reads OUT_MSG,</text>
  <text x="575" y="138" text-anchor="middle" font-size="10" fill="#5a544e">aggregates with other rules</text>

  
  <line x1="575" y1="155" x2="575" y2="195" stroke="#7a7570" stroke-width="2" marker-end="url(#arrow2)"/>

  
  <rect x="510" y="200" width="130" height="80" rx="4" fill="#fff" stroke="#27704a" stroke-width="1.5"/>
  <rect x="510" y="200" width="130" height="20" rx="4" fill="#27704a"/>
  <text x="575" y="215" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">STAGE 5</text>
  <text x="575" y="238" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">UI renders feedback</text>
  <text x="575" y="254" text-anchor="middle" font-size="10" fill="#5a544e">Red error markers</text>
  <text x="575" y="268" text-anchor="middle" font-size="10" fill="#5a544e">on flagged rows</text>

  
  <rect x="30" y="200" width="450" height="200" rx="4" fill="#f5f1e8" stroke="#b97417" stroke-width="1"/>
  <rect x="30" y="200" width="450" height="22" rx="4" fill="#b97417"/>
  <text x="40" y="216" font-size="10" font-weight="700" fill="#fff">ZOOM: STAGE 3 INTERNAL FLOW — What your formula does between input and output</text>

  <text x="44" y="243" font-size="11" fill="#2d2926"><tspan font-weight="700">1.</tspan>  Receive the six input arrays from OTL (read-only)</text>
  <text x="44" y="265" font-size="11" fill="#2d2926"><tspan font-weight="700">2.</tspan>  Initialise OUT_MSG as an empty array (will hold error messages)</text>
  <text x="44" y="287" font-size="11" fill="#2d2926"><tspan font-weight="700">3.</tspan>  Loop through every row index from 1 to N</text>
  <text x="60" y="305" font-size="10.5" fill="#5a544e">• Read all six arrays at the current index (parallel read)</text>
  <text x="60" y="320" font-size="10.5" fill="#5a544e">• Apply your validation logic (overlap, continuous-hours, etc.)</text>
  <text x="60" y="335" font-size="10.5" fill="#5a544e">• If anything fails, write a message into OUT_MSG[idx]</text>
  <text x="44" y="358" font-size="11" fill="#2d2926"><tspan font-weight="700">4.</tspan>  When the loop finishes, OTL reads OUT_MSG and acts on it</text>

  <text x="255" y="385" text-anchor="middle" font-size="10" font-style="italic" fill="#7a7570">The 6 inputs and 1 output define the contract. Everything else is your logic.</text>

  
  <defs>
    <marker id="arrow2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M0,0 L0,8 L8,4 z" fill="#7a7570"/>
    </marker>
  </defs>

</svg>

</div>

<p>Stage 3 is where your formula has agency. Stages 1, 2, 4, and 5 belong to OTL. The contract you're working against is: <em>OTL gives you six well-defined arrays; you give back one well-defined array; everything else is your business logic.</em></p>

<h4>Decoding the input names — what each part means</h4>

<p>Now that we know <em>where</em> the inputs come from, let's decode <em>why they're named the way they are</em>. Oracle's naming is structural, not arbitrary. Every prefix carries meaning. Here's the breakdown:</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<svg viewBox="0 0 720 470" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:720px; display:block; margin:0 auto;" font-family="Calibri, sans-serif">

  <text x="360" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#2d2926">Anatomy of the Input Names</text>
  <text x="360" y="40" text-anchor="middle" font-size="11" fill="#7a7570">Reading the prefix tells you what kind of data the input represents</text>

  
  <text x="360" y="78" text-anchor="middle" font-size="12" font-weight="700" fill="#4472c4">Long-prefix names — structural metadata from OTL's framework</text>

  
  <g transform="translate(80, 100)">
    <rect x="0" y="0" width="80" height="32" fill="#dbe5f4" stroke="#4472c4" stroke-width="1"/>
    <rect x="80" y="0" width="84" height="32" fill="#a8c1e0" stroke="#4472c4" stroke-width="1"/>
    <rect x="164" y="0" width="396" height="32" fill="#fff" stroke="#4472c4" stroke-width="1"/>

    <text x="40" y="20" text-anchor="middle" font-size="14" font-weight="700" fill="#2d2926" font-family="JetBrains Mono, monospace">HWM_</text>
    <text x="122" y="20" text-anchor="middle" font-size="14" font-weight="700" fill="#2d2926" font-family="JetBrains Mono, monospace">CTXARY_</text>
    <text x="362" y="20" text-anchor="middle" font-size="14" font-weight="700" fill="#2d2926" font-family="JetBrains Mono, monospace">RECORD_POSITIONS</text>

    
    <line x1="40" y1="38" x2="40" y2="58" stroke="#4472c4" stroke-width="1"/>
    <text x="40" y="74" text-anchor="middle" font-size="9.5" font-weight="700" fill="#4472c4">"HWM"</text>
    <text x="40" y="86" text-anchor="middle" font-size="9" fill="#5a544e">HCM Workforce</text>
    <text x="40" y="98" text-anchor="middle" font-size="9" fill="#5a544e">Management</text>

    <line x1="122" y1="38" x2="122" y2="58" stroke="#4472c4" stroke-width="1"/>
    <text x="122" y="74" text-anchor="middle" font-size="9.5" font-weight="700" fill="#4472c4">"CTXARY"</text>
    <text x="122" y="86" text-anchor="middle" font-size="9" fill="#5a544e">Context Array</text>
    <text x="122" y="98" text-anchor="middle" font-size="9" fill="#5a544e">(per-row metadata)</text>

    <line x1="362" y1="38" x2="362" y2="58" stroke="#4472c4" stroke-width="1"/>
    <text x="362" y="74" text-anchor="middle" font-size="9.5" font-weight="700" fill="#4472c4">"RECORD_POSITIONS"</text>
    <text x="362" y="86" text-anchor="middle" font-size="9" fill="#5a544e">What this array actually holds</text>
    <text x="362" y="98" text-anchor="middle" font-size="9" fill="#5a544e">(marker text per row)</text>
  </g>

  <text x="360" y="218" text-anchor="middle" font-size="10.5" fill="#5a544e" font-style="italic">Read aloud: "HCM Workforce Management's context array of record positions"</text>

  
  <line x1="80" y1="240" x2="640" y2="240" stroke="#d4d4d4" stroke-width="1" stroke-dasharray="4,4"/>

  
  <text x="360" y="266" text-anchor="middle" font-size="12" font-weight="700" fill="#b97417">Short-name inputs — per-row time data</text>
  <text x="360" y="282" text-anchor="middle" font-size="10.5" fill="#5a544e" font-style="italic">No prefix needed — these are the original TER inputs from OTL's earliest design</text>

  
  <g transform="translate(80, 300)">
    <rect x="0" y="0" width="135" height="60" rx="3" fill="#fff" stroke="#b97417" stroke-width="1"/>
    <text x="67.5" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="#2d2926" font-family="JetBrains Mono, monospace">measure</text>
    <text x="67.5" y="40" text-anchor="middle" font-size="9.5" fill="#5a544e">Hours value</text>
    <text x="67.5" y="52" text-anchor="middle" font-size="9.5" fill="#5a544e">per row</text>

    <rect x="142" y="0" width="135" height="60" rx="3" fill="#fff" stroke="#b97417" stroke-width="1"/>
    <text x="209.5" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="#2d2926" font-family="JetBrains Mono, monospace">PayrollTimeType</text>
    <text x="209.5" y="40" text-anchor="middle" font-size="9.5" fill="#5a544e">Time-type label</text>
    <text x="209.5" y="52" text-anchor="middle" font-size="9.5" fill="#5a544e">per row</text>

    <rect x="284" y="0" width="135" height="60" rx="3" fill="#fff" stroke="#b97417" stroke-width="1"/>
    <text x="351.5" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="#2d2926" font-family="JetBrains Mono, monospace">StartTime</text>
    <text x="351.5" y="40" text-anchor="middle" font-size="9.5" fill="#5a544e">Punch-in</text>
    <text x="351.5" y="52" text-anchor="middle" font-size="9.5" fill="#5a544e">timestamp per row</text>

    <rect x="426" y="0" width="135" height="60" rx="3" fill="#fff" stroke="#b97417" stroke-width="1"/>
    <text x="493.5" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="#2d2926" font-family="JetBrains Mono, monospace">StopTime</text>
    <text x="493.5" y="40" text-anchor="middle" font-size="9.5" fill="#5a544e">Punch-out</text>
    <text x="493.5" y="52" text-anchor="middle" font-size="9.5" fill="#5a544e">timestamp per row</text>
  </g>

  
  <rect x="80" y="395" width="560" height="60" rx="4" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
  <text x="92" y="415" font-size="10.5" font-weight="700" fill="#c0392b">KEY INSIGHT</text>
  <text x="92" y="432" font-size="11" fill="#2d2926">Long-prefix inputs carry <tspan font-weight="700">structural metadata</tspan> (where in the timecard structure are we?).</text>
  <text x="92" y="448" font-size="11" fill="#2d2926">Short-name inputs carry <tspan font-weight="700">the actual time data</tspan> (what did the worker enter on this row?).</text>

</svg>

</div>

<p>Once you see this split, the naming makes sense. The <code>HWM_CTXARY_</code> prefix is Oracle saying <em>"this input is structural metadata that the framework needs to manage the iteration."</em> The short names (<code>measure</code>, <code>PayrollTimeType</code>, <code>StartTime</code>, <code>StopTime</code>) are saying <em>"this input is the worker's actual time data, the same names we've used since the OTL was first designed."</em></p>

<div style="background:#fff5f0; border-left:4px solid #c0392b; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
  <div style="font-size:9.5px; letter-spacing:1.6px; color:#c0392b; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Expert insight</div>

  You'll see this same <code>HWM_</code> prefix convention across other OTL formula types too — calculation rules, time-calculation formulas, time-card validation formulas. Once you internalise that <code>HWM_</code> means "framework-supplied" and <code>HWM_CTXARY_</code> means "framework-supplied per-row metadata", you can read any OTL formula and immediately know which variables come from the framework versus which ones the author created. <strong>This pattern recognition is what separates a fluent OTL developer from someone still puzzling over the syntax.</strong>
</div>

<h4>How to read one timecard row from the parallel arrays</h4>

<p>Now the practical part. Inside the formula's loop, each iteration processes one row. To get all the data for that row, you read all six arrays at the same index. Here's a visual showing how the parallel arrays line up:</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:24px; margin:24px 0; box-shadow:0 2px 12px rgba(0,0,0,0.04);">

<svg viewBox="0 0 760 360" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:760px; display:block; margin:0 auto;" font-family="Calibri, sans-serif">

  <text x="380" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#2d2926">Six arrays, one shared index space</text>
  <text x="380" y="40" text-anchor="middle" font-size="11" fill="#7a7570">Read all six at index [3] to reconstruct row 3 of Sarah's timecard</text>

  
  <rect x="30" y="65" width="50" height="30" fill="#e8e8e8" stroke="#999" stroke-width="1"/>
  <text x="55" y="85" text-anchor="middle" font-size="11" font-weight="700" fill="#5a544e">Idx</text>

  
  <rect x="80" y="65" width="115" height="30" fill="#dbe5f4" stroke="#4472c4" stroke-width="1"/>
  <text x="137.5" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">HWM_CTXARY_</text>
  <text x="137.5" y="91" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">RECORD_POSITIONS</text>

  <rect x="195" y="65" width="115" height="30" fill="#dbe5f4" stroke="#4472c4" stroke-width="1"/>
  <text x="252.5" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">HWM_CTXARY_</text>
  <text x="252.5" y="91" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">HWM_MEASURE_DAY</text>

  <rect x="310" y="65" width="80" height="30" fill="#fff3e0" stroke="#b97417" stroke-width="1"/>
  <text x="350" y="85" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">measure</text>

  <rect x="390" y="65" width="120" height="30" fill="#fff3e0" stroke="#b97417" stroke-width="1"/>
  <text x="450" y="85" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">PayrollTimeType</text>

  <rect x="510" y="65" width="100" height="30" fill="#fff3e0" stroke="#b97417" stroke-width="1"/>
  <text x="560" y="85" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">StartTime</text>

  <rect x="610" y="65" width="100" height="30" fill="#fff3e0" stroke="#b97417" stroke-width="1"/>
  <text x="660" y="85" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">StopTime</text>

  
  <rect x="30" y="95" width="50" height="28" fill="#fff8e7" stroke="#999" stroke-width="0.5"/>
  <text x="55" y="113" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">[1]</text>

  <rect x="80" y="95" width="115" height="28" fill="#fff8e7" stroke="#999" stroke-width="0.5"/>
  <text x="137.5" y="113" text-anchor="middle" font-size="10" font-weight="700" fill="#b97417">HEADER</text>

  <rect x="195" y="95" width="115" height="28" fill="#fff8e7" stroke="#999" stroke-width="0.5"/>
  <text x="252.5" y="113" text-anchor="middle" font-size="10" fill="#999">—</text>

  <rect x="310" y="95" width="80" height="28" fill="#fff8e7" stroke="#999" stroke-width="0.5"/>
  <text x="350" y="113" text-anchor="middle" font-size="10" fill="#999">—</text>

  <rect x="390" y="95" width="120" height="28" fill="#fff8e7" stroke="#999" stroke-width="0.5"/>
  <text x="450" y="113" text-anchor="middle" font-size="10" fill="#999">—</text>

  <rect x="510" y="95" width="100" height="28" fill="#fff8e7" stroke="#999" stroke-width="0.5"/>
  <text x="560" y="113" text-anchor="middle" font-size="10" fill="#999">—</text>

  <rect x="610" y="95" width="100" height="28" fill="#fff8e7" stroke="#999" stroke-width="0.5"/>
  <text x="660" y="113" text-anchor="middle" font-size="10" fill="#999">—</text>

  
  <rect x="30" y="123" width="50" height="28" fill="#fff" stroke="#999" stroke-width="0.5"/>
  <text x="55" y="141" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">[2]</text>

  <rect x="80" y="123" width="115" height="28" fill="#fff" stroke="#999" stroke-width="0.5"/>
  <text x="137.5" y="141" text-anchor="middle" font-size="10" fill="#999">(empty)</text>

  <rect x="195" y="123" width="115" height="28" fill="#fff" stroke="#999" stroke-width="0.5"/>
  <text x="252.5" y="141" text-anchor="middle" font-size="10" fill="#5a544e">6.25</text>

  <rect x="310" y="123" width="80" height="28" fill="#fff" stroke="#999" stroke-width="0.5"/>
  <text x="350" y="141" text-anchor="middle" font-size="10" fill="#5a544e">1.5</text>

  <rect x="390" y="123" width="120" height="28" fill="#fff" stroke="#999" stroke-width="0.5"/>
  <text x="450" y="141" text-anchor="middle" font-size="10" fill="#5a544e">Regular Hours</text>

  <rect x="510" y="123" width="100" height="28" fill="#fff" stroke="#999" stroke-width="0.5"/>
  <text x="560" y="141" text-anchor="middle" font-size="10" fill="#5a544e">08:30</text>

  <rect x="610" y="123" width="100" height="28" fill="#fff" stroke="#999" stroke-width="0.5"/>
  <text x="660" y="141" text-anchor="middle" font-size="10" fill="#5a544e">10:00</text>

  
  <rect x="30" y="151" width="50" height="32" fill="#ffd180" stroke="#c0392b" stroke-width="2"/>
  <text x="55" y="172" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">[3]</text>

  <rect x="80" y="151" width="115" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
  <text x="137.5" y="172" text-anchor="middle" font-size="10" fill="#999">(empty)</text>

  <rect x="195" y="151" width="115" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
  <text x="252.5" y="172" text-anchor="middle" font-size="10" fill="#5a544e">6.25</text>

  <rect x="310" y="151" width="80" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
  <text x="350" y="172" text-anchor="middle" font-size="10" font-weight="700" fill="#2d2926">4.75</text>

  <rect x="390" y="151" width="120" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
  <text x="450" y="172" text-anchor="middle" font-size="10" font-weight="700" fill="#2d2926">Regular Hours</text>

  <rect x="510" y="151" width="100" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
  <text x="560" y="172" text-anchor="middle" font-size="10" font-weight="700" fill="#2d2926">10:00</text>

  <rect x="610" y="151" width="100" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
  <text x="660" y="172" text-anchor="middle" font-size="10" font-weight="700" fill="#2d2926">14:45</text>

  
  <rect x="30" y="183" width="50" height="28" fill="#fce8e8" stroke="#999" stroke-width="0.5"/>
  <text x="55" y="201" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">[4]</text>

  <rect x="80" y="183" width="115" height="28" fill="#fce8e8" stroke="#999" stroke-width="0.5"/>
  <text x="137.5" y="201" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">END_DAY</text>

  <rect x="195" y="183" width="115" height="28" fill="#fce8e8" stroke="#999" stroke-width="0.5"/>
  <text x="252.5" y="201" text-anchor="middle" font-size="10" fill="#999">—</text>

  <rect x="310" y="183" width="80" height="28" fill="#fce8e8" stroke="#999" stroke-width="0.5"/>
  <text x="350" y="201" text-anchor="middle" font-size="10" fill="#999">—</text>

  <rect x="390" y="183" width="120" height="28" fill="#fce8e8" stroke="#999" stroke-width="0.5"/>
  <text x="450" y="201" text-anchor="middle" font-size="10" fill="#999">—</text>

  <rect x="510" y="183" width="100" height="28" fill="#fce8e8" stroke="#999" stroke-width="0.5"/>
  <text x="560" y="201" text-anchor="middle" font-size="10" fill="#999">—</text>

  <rect x="610" y="183" width="100" height="28" fill="#fce8e8" stroke="#999" stroke-width="0.5"/>
  <text x="660" y="201" text-anchor="middle" font-size="10" fill="#999">—</text>

  
  <rect x="30" y="151" width="680" height="32" fill="none" stroke="#c0392b" stroke-width="2.5" stroke-dasharray="4,3"/>
  <text x="700" y="146" text-anchor="end" font-size="10" font-weight="700" fill="#c0392b">← current iteration (nidx = 3)</text>

  
  <rect x="30" y="240" width="700" height="100" rx="3" fill="#1f1c19"/>
  <text x="44" y="260" font-size="10" font-weight="700" fill="#a8a39c" font-family="JetBrains Mono, monospace">/* read all six arrays at index 3 to reconstruct row 3 */</text>
  <text x="44" y="280" font-size="11" fill="#e6e1d8" font-family="JetBrains Mono, monospace">aiRecPos     = HWM_CTXARY_RECORD_POSITIONS[3]   <tspan fill="#a8a39c">// '' (empty)</tspan></text>
  <text x="44" y="296" font-size="11" fill="#e6e1d8" font-family="JetBrains Mono, monospace">aiMeasureDay = HWM_CTXARY_HWM_MEASURE_DAY[3]    <tspan fill="#a8a39c">// 6.25 (not used)</tspan></text>
  <text x="44" y="312" font-size="11" fill="#e6e1d8" font-family="JetBrains Mono, monospace">aiMeasure    = measure[3]                       <tspan fill="#a8a39c">// 4.75</tspan></text>
  <text x="44" y="328" font-size="11" fill="#e6e1d8" font-family="JetBrains Mono, monospace">aiTimeType   = PayrollTimeType[3]               <tspan fill="#a8a39c">// 'Regular Hours'</tspan></text>

  
  <defs>
    <marker id="arrow3" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse">
      <path d="M0,0 L0,8 L8,4 z" fill="#c0392b"/>
    </marker>
  </defs>

</svg>

</div>

<p>Six arrays, six reads, one row reconstructed. The formula's WHILE loop does this on every iteration, walking the index from 1 to N (where N is the total row count returned by <code>HWM_CTXARY_RECORD_POSITIONS.count</code>). On marker rows like [1] and [4], several of the reads return empty — which is why each read in the formula is wrapped in a <code>.exists()</code> guard.</p>

<div style="background:#f5f1e8; border-left:4px solid #b97417; padding:14px 20px; margin:20px 0; border-radius:0 4px 4px 0; font-size:13px; line-height:1.65;">
  <div style="font-size:9.5px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Practitioner's tip</div>

  When debugging a TER formula in production, the first thing I check is the <code>HWM_CTXARY_RECORD_POSITIONS</code> array length. If <code>.count = 0</code>, the formula received nothing to validate — the bug is upstream in the OTL configuration, not in your formula logic. If <code>.count</code> is non-zero but no validations fire, your loop counter or your <code>.exists()</code> guards are wrong. <strong>Always log <code>.count</code> at the top of the formula via <code>add_rlog</code></strong> — it'll save you hours of guessing.
</div>

<h4>Now: each input in detail</h4>

<p>With the framing in place — how the formula fits in OTL's pipeline, what the names mean, how parallel access works — the cards below cover all six inputs (plus the <code>OUT_MSG</code> output) one by one. Each card shows what kind of values the input holds, the actual formula code that reads it, and what the formula does with the value.</p>




<div class="input-card">
  <div class="ic-head">
    <div class="ic-eyebrow">Input 01 · Text Array</div>

    <div class="ic-name">HWM_CTXARY_RECORD_POSITIONS</div>

  </div>

  <div class="ic-question">"What kind of row is this?"</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>RECORD_POSITIONS_examples.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Possible value</th><th>Meaning</th></tr></thead>
      <tbody>
        <tr><td class="empty">(empty)</td><td>Real worker entry — check the data columns</td></tr>
        <tr><td><strong>HEADER</strong></td><td>System marker at the top of the timecard</td></tr>
        <tr><td><strong>END_DAY</strong></td><td>System marker at the end of each day — trigger day-level work</td></tr>
        <tr><td><strong>END_PERIOD</strong></td><td>System marker at the end of the whole timecard period</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-mini-excel-cap">Four possible values. Empty means real data; non-empty is a system-inserted marker telling the formula something about structure.</div>

  <div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
    <div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · Where each marker value appears in the array</div>

    <svg viewBox="0 0 680 240" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:680px; display:block;" font-family="Calibri, sans-serif">

      
      <g transform="translate(40, 40)">
        
        <rect x="0" y="0" width="60" height="50" fill="#fff3e0" stroke="#b97417" stroke-width="1.5"/>
        <text x="30" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">[1]</text>
        <text x="30" y="35" text-anchor="middle" font-size="10" font-weight="700" fill="#b97417">HEADER</text>

        
        <rect x="60" y="0" width="60" height="50" fill="#fff" stroke="#7a7570" stroke-width="1"/>
        <text x="90" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">[2]</text>
        <text x="90" y="35" text-anchor="middle" font-size="10" fill="#999" font-style="italic">empty</text>

        
        <rect x="120" y="0" width="60" height="50" fill="#fff" stroke="#7a7570" stroke-width="1"/>
        <text x="150" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">[3]</text>
        <text x="150" y="35" text-anchor="middle" font-size="10" fill="#999" font-style="italic">empty</text>

        
        <rect x="180" y="0" width="60" height="50" fill="#fff" stroke="#7a7570" stroke-width="1"/>
        <text x="210" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">[4]</text>
        <text x="210" y="35" text-anchor="middle" font-size="10" fill="#999" font-style="italic">empty</text>

        
        <rect x="240" y="0" width="60" height="50" fill="#fce8e8" stroke="#c0392b" stroke-width="1.5"/>
        <text x="270" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">[5]</text>
        <text x="270" y="35" text-anchor="middle" font-size="9" font-weight="700" fill="#c0392b">END_DAY</text>

        
        <rect x="300" y="0" width="60" height="50" fill="#fff" stroke="#7a7570" stroke-width="1"/>
        <text x="330" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">[6]</text>
        <text x="330" y="35" text-anchor="middle" font-size="10" fill="#999" font-style="italic">empty</text>

        
        <rect x="360" y="0" width="60" height="50" fill="#fce8e8" stroke="#c0392b" stroke-width="1.5"/>
        <text x="390" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">[7]</text>
        <text x="390" y="35" text-anchor="middle" font-size="9" font-weight="700" fill="#c0392b">END_DAY</text>

        
        <rect x="420" y="0" width="80" height="50" fill="#fce8e8" stroke="#c0392b" stroke-width="1.5"/>
        <text x="460" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">[8]</text>
        <text x="460" y="35" text-anchor="middle" font-size="9" font-weight="700" fill="#c0392b">END_PERIOD</text>

        
        <line x1="30" y1="55" x2="30" y2="78" stroke="#b97417" stroke-width="1"/>
        <text x="30" y="92" text-anchor="middle" font-size="9.5" font-weight="700" fill="#b97417">Always at [1]</text>
        <text x="30" y="104" text-anchor="middle" font-size="9" fill="#5a544e">Skip silently</text>

        <line x1="150" y1="55" x2="150" y2="78" stroke="#27704a" stroke-width="1"/>
        <text x="150" y="92" text-anchor="middle" font-size="9.5" font-weight="700" fill="#27704a">Day 1 entries</text>
        <text x="150" y="104" text-anchor="middle" font-size="9" fill="#5a544e">Process normally</text>

        <line x1="270" y1="55" x2="270" y2="78" stroke="#c0392b" stroke-width="1"/>
        <text x="270" y="92" text-anchor="middle" font-size="9.5" font-weight="700" fill="#c0392b">Trigger Block 7</text>
        <text x="270" y="104" text-anchor="middle" font-size="9" fill="#5a544e">Day-level work</text>

        <line x1="330" y1="55" x2="330" y2="78" stroke="#27704a" stroke-width="1"/>
        <text x="330" y="92" text-anchor="middle" font-size="9.5" font-weight="700" fill="#27704a">Day 2 entries</text>

        <line x1="390" y1="55" x2="390" y2="78" stroke="#c0392b" stroke-width="1"/>
        <text x="390" y="92" text-anchor="middle" font-size="9.5" font-weight="700" fill="#c0392b">Trigger Block 7</text>

        <line x1="460" y1="55" x2="460" y2="78" stroke="#c0392b" stroke-width="1"/>
        <text x="460" y="92" text-anchor="middle" font-size="9.5" font-weight="700" fill="#c0392b">Loop ends</text>
        <text x="460" y="104" text-anchor="middle" font-size="9" fill="#5a544e">Always last index</text>
      </g>

      
      <g transform="translate(40, 158)">
        <text x="0" y="0" font-size="11" font-weight="700" fill="#2d2926">How the formula reads RECORD_POSITIONS:</text>
        <rect x="0" y="14" width="600" height="56" rx="3" fill="#1f1c19"/>
        <text x="14" y="34" font-size="10.5" fill="#a8a39c" font-family="JetBrains Mono, monospace">aiRecPos = RECORD_POSITIONS[nidx]</text>
        <text x="14" y="52" font-size="10.5" fill="#e6e1d8" font-family="JetBrains Mono, monospace">IF aiRecPos = 'END_DAY' OR aiRecPos = 'END_PERIOD' THEN ...</text>
        <text x="14" y="68" font-size="10" fill="#a8a39c" font-family="JetBrains Mono, monospace">/* HEADER is silently skipped — no branch needed */</text>
      </g>
    </svg>

  </div>

  <div class="ic-snippet">
<span class="lbl">How the formula reads it</span><span class="c">/* read the marker for this index */</span>
<span class="k">IF</span> (<span class="v">HWM_CTXARY_RECORD_POSITIONS</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
  <span class="v">aiRecPos</span> <span class="op">=</span> <span class="v">HWM_CTXARY_RECORD_POSITIONS</span>[<span class="v">nidx</span>]

<span class="c">/* branch on what kind of row this is */</span>
<span class="k">IF</span> (<span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'END_DAY'</span>
    <span class="k">OR</span> <span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'END_PERIOD'</span>) <span class="k">THEN</span>
  <span class="c">/* run pairwise overlap, reset day buffer */</span></div>

  <div class="ic-explain">Empty value at this index → real worker entry, so the formula reads the data columns. Non-empty (HEADER, END_DAY, END_PERIOD) → system marker, so skip the data columns and trigger boundary logic if applicable. <strong>This is the first thing the formula reads every iteration</strong> — it decides everything else.</div>
</div>


<div class="input-card reserved">
  <div class="ic-head">
    <div class="ic-eyebrow">Input 02 · Number Array · Reserved</div>

    <div class="ic-name">HWM_CTXARY_HWM_MEASURE_DAY</div>

  </div>

  <div class="ic-question">"Is this input actually used?" — <strong>No, but it must be declared.</strong></div>

  <div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
    <div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · The "declared but unused" pattern</div>

    <svg viewBox="0 0 680 260" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:680px; display:block;" font-family="Calibri, sans-serif">

      
      <rect x="20" y="30" width="280" height="190" rx="4" fill="#e8f4ea" stroke="#27704a" stroke-width="1.5"/>
      <rect x="20" y="30" width="280" height="22" rx="4" fill="#27704a"/>
      <text x="160" y="46" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">REQUIRED · INPUTS ARE declaration</text>

      <text x="34" y="76" font-size="11" font-family="JetBrains Mono, monospace" fill="#2d2926">INPUTS ARE</text>
      <text x="50" y="94" font-size="10" font-family="JetBrains Mono, monospace" fill="#2d2926">HWM_CTXARY_RECORD_POSITIONS,</text>
      <rect x="46" y="100" width="244" height="18" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
      <text x="50" y="114" font-size="10" font-family="JetBrains Mono, monospace" fill="#c0392b" font-weight="700">HWM_CTXARY_HWM_MEASURE_DAY,</text>
      <text x="50" y="132" font-size="10" font-family="JetBrains Mono, monospace" fill="#2d2926">measure, PayrollTimeType,</text>
      <text x="50" y="150" font-size="10" font-family="JetBrains Mono, monospace" fill="#2d2926">StartTime, StopTime</text>

      <text x="34" y="180" font-size="10" fill="#27704a" font-weight="700">✓ Must be present</text>
      <text x="34" y="195" font-size="9.5" fill="#5a544e">Otherwise framework throws</text>
      <text x="34" y="208" font-size="9.5" fill="#5a544e">a binding error at runtime</text>

      
      <rect x="380" y="30" width="280" height="190" rx="4" fill="#fef7f0" stroke="#b97417" stroke-width="1.5"/>
      <rect x="380" y="30" width="280" height="22" rx="4" fill="#b97417"/>
      <text x="520" y="46" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">FORMULA BODY · never reads it</text>

      <text x="394" y="76" font-size="11" font-family="JetBrains Mono, monospace" fill="#2d2926">Block 1 — DEFAULT FOR</text>
      <text x="394" y="92" font-size="10" font-family="JetBrains Mono, monospace" fill="#7a7570">/* not referenced */</text>

      <text x="394" y="116" font-size="11" font-family="JetBrains Mono, monospace" fill="#2d2926">Block 6 — per-line read</text>
      <text x="394" y="132" font-size="10" font-family="JetBrains Mono, monospace" fill="#7a7570">/* not referenced */</text>

      <text x="394" y="156" font-size="11" font-family="JetBrains Mono, monospace" fill="#2d2926">Block 7 — day-level work</text>
      <text x="394" y="172" font-size="10" font-family="JetBrains Mono, monospace" fill="#7a7570">/* not referenced */</text>

      <text x="394" y="196" font-size="11" font-family="JetBrains Mono, monospace" fill="#2d2926">Block 8 — state machine</text>
      <text x="394" y="208" font-size="10" font-family="JetBrains Mono, monospace" fill="#7a7570">/* not referenced */</text>

      
      <line x1="300" y1="125" x2="380" y2="125" stroke="#7a7570" stroke-width="1" stroke-dasharray="3,2"/>
      <text x="340" y="118" text-anchor="middle" font-size="9" fill="#7a7570" font-style="italic">contract gap</text>
      <text x="340" y="134" text-anchor="middle" font-size="9" fill="#7a7570" font-style="italic">declare, ignore</text>

      
      <rect x="20" y="234" width="640" height="20" rx="3" fill="#1f1c19"/>
      <text x="340" y="248" text-anchor="middle" font-size="10.5" font-family="JetBrains Mono, monospace" fill="#e6e1d8">Required by contract · Read by zero blocks · Pure compliance checkbox</text>

    </svg>

  </div>

  <div class="ic-explain">
    <p style="margin-top:0;">This input would hold day-level totals if the formula needed them. The framework hands it over because the TER formula type's contract requires it — <strong>but this particular formula never reads it</strong>. Three things to know:</p>
    <ul style="margin:8px 0 0 0; padding-left:22px;">
      <li><strong>You must declare it</strong> in the <code>INPUTS ARE</code> statement, otherwise the framework throws a binding error and the formula won't even start.</li>
      <li><strong>You don't read from it.</strong> The validations work entirely off per-row punches (<code>StartTime</code>, <code>StopTime</code>) and per-row <code>measure</code>, never from day-level aggregates.</li>
      <li><strong>You can ignore it from here on.</strong> It plays no role in any of Block 6, 7, or 8. A different formula type (like a calculation rule) might consume it; this one simply lists it and moves on.</li>
    </ul>
  </div>
</div>


<div class="input-card">
  <div class="ic-head">
    <div class="ic-eyebrow">Input 03 · Number Array</div>

    <div class="ic-name">measure</div>

  </div>

  <div class="ic-question">"How many hours on this row?"</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>measure_examples.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Sample value</th><th>What it represents</th></tr></thead>
      <tbody>
        <tr><td class="tc">2.5</td><td>2 hours 30 minutes — real punch interval</td></tr>
        <tr><td class="tc">8.0</td><td>8 hours — could be real or a qty-only placeholder</td></tr>
        <tr><td class="tc">0.5</td><td>30 minutes — short break or partial shift</td></tr>
        <tr><td class="empty">(no value)</td><td>Marker rows have no <code>measure</code> — not applicable</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-mini-excel-cap">Always a number when present. The same value can come from real punches or from a qty-only placeholder — <code>measure</code> alone can't tell which.</div>

  <div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
    <div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · Real punches vs qty-only — same measure, different intent</div>

    <svg viewBox="0 0 680 250" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:680px; display:block;" font-family="Calibri, sans-serif">

      
      <rect x="20" y="20" width="300" height="200" rx="4" fill="#e8f4ea" stroke="#27704a" stroke-width="1.5"/>
      <rect x="20" y="20" width="300" height="22" rx="4" fill="#27704a"/>
      <text x="170" y="36" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">CASE 1 · REAL PUNCHES</text>

      <text x="34" y="62" font-size="10" font-weight="700" fill="#5a544e">Worker entered:</text>
      <rect x="34" y="68" width="270" height="22" fill="#fff" stroke="#27704a" stroke-width="0.8"/>
      <text x="44" y="83" font-size="10" font-family="JetBrains Mono, monospace" fill="#2d2926">Reg Hours · 09:00 → 17:00</text>

      <text x="34" y="108" font-size="10" font-weight="700" fill="#5a544e">Framework gives the formula:</text>
      <rect x="34" y="114" width="270" height="60" fill="#fff" stroke="#27704a" stroke-width="0.8"/>
      <text x="44" y="130" font-size="10" font-family="JetBrains Mono, monospace" fill="#2d2926">StartTime[i] = 09:00</text>
      <text x="44" y="146" font-size="10" font-family="JetBrains Mono, monospace" fill="#2d2926">StopTime[i]  = 17:00</text>
      <text x="44" y="162" font-size="10" font-family="JetBrains Mono, monospace" fill="#27704a" font-weight="700">measure[i]   = 8.0</text>

      <text x="34" y="194" font-size="10" fill="#27704a" font-weight="700">✓ Use punches directly</text>
      <text x="34" y="208" font-size="9.5" fill="#5a544e">measure is just StopTime − StartTime</text>

      
      <rect x="360" y="20" width="300" height="200" rx="4" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
      <rect x="360" y="20" width="300" height="22" rx="4" fill="#c0392b"/>
      <text x="510" y="36" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">CASE 2 · QTY-ONLY PLACEHOLDER</text>

      <text x="374" y="62" font-size="10" font-weight="700" fill="#5a544e">Worker entered:</text>
      <rect x="374" y="68" width="270" height="22" fill="#fff" stroke="#c0392b" stroke-width="0.8"/>
      <text x="384" y="83" font-size="10" font-family="JetBrains Mono, monospace" fill="#2d2926">Reg Hours · 8 hours (no punches)</text>

      <text x="374" y="108" font-size="10" font-weight="700" fill="#5a544e">Framework gives the formula:</text>
      <rect x="374" y="114" width="270" height="60" fill="#fff" stroke="#c0392b" stroke-width="0.8"/>
      <text x="384" y="130" font-size="10" font-family="JetBrains Mono, monospace" fill="#c0392b" font-weight="700">StartTime[i] = 00:00 ← fake</text>
      <text x="384" y="146" font-size="10" font-family="JetBrains Mono, monospace" fill="#c0392b" font-weight="700">StopTime[i]  = 23:59 ← fake</text>
      <text x="384" y="162" font-size="10" font-family="JetBrains Mono, monospace" fill="#27704a" font-weight="700">measure[i]   = 8.0  ← the truth</text>

      <text x="374" y="194" font-size="10" fill="#c0392b" font-weight="700">✗ Punches are placeholders</text>
      <text x="374" y="208" font-size="9.5" fill="#5a544e">Trust measure, ignore the punches</text>

      
      <rect x="20" y="232" width="640" height="14" rx="3" fill="#1f1c19"/>
      <text x="340" y="243" text-anchor="middle" font-size="9.5" font-family="JetBrains Mono, monospace" fill="#e6e1d8">Detection: if StartTime ≈ 00:00 AND StopTime ≈ 23:59 → this is qty-only</text>

    </svg>

  </div>

  <div class="ic-snippet">
<span class="lbl">How the formula reads it</span><span class="c">/* per-line measure, used for qty-only entries */</span>
<span class="k">IF</span> (<span class="v">measure</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
  <span class="v">aiMeasure</span> <span class="op">=</span> <span class="v">measure</span>[<span class="v">nidx</span>]</div>

  <div class="ic-explain"><strong>The formula uses this mainly for qty-only detection.</strong> If a worker types just "8 hours" without entering punch times, OTL fills <code>StartTime</code> as <code>00:00</code> and <code>StopTime</code> as <code>23:59</code> — the <code>measure</code> tells you the real intended hours (8) without needing to compute it from the placeholder punches. When the punches are genuine, <code>measure</code> simply equals <code>StopTime − StartTime</code> in hours, and the formula uses the punches directly anyway.</div>
</div>


<div class="input-card">
  <div class="ic-head">
    <div class="ic-eyebrow">Input 04 · Text Array · Routing Key</div>

    <div class="ic-name">PayrollTimeType</div>

  </div>

  <div class="ic-question">"What kind of time?"</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>PayrollTimeType_routes.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Time type value</th><th>Where the formula sends it</th></tr></thead>
      <tbody>
        <tr class="row-pass"><td>Regular Hours</td><td class="tag">Stretch tracker + Day buffer for overlap</td></tr>
        <tr><td>Meal Break</td><td style="color:#b97417;">Schedule-window check + Reset stretch</td></tr>
        <tr><td>Annual Leave</td><td style="color:#7a7570;">Skipped — no validation path</td></tr>
        <tr><td>Sick Leave</td><td style="color:#7a7570;">Skipped — no validation path</td></tr>
        <tr><td>Public Holiday</td><td style="color:#7a7570;">Skipped — no validation path</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-mini-excel-cap">The string value drives the entire routing decision. Reg Hours and Meal Break have validation paths; everything else falls through silently.</div>

  <div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
    <div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · Time-type values fan out to validation paths</div>

    <svg viewBox="0 0 680 280" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:680px; display:block;" font-family="Calibri, sans-serif">

      
      <rect x="20" y="116" width="160" height="48" rx="4" fill="#1f1c19" stroke="#1f1c19"/>
      <text x="100" y="135" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">aiTimeType</text>
      <text x="100" y="152" text-anchor="middle" font-size="9.5" fill="#a8a39c">a string value per row</text>

      
      
      <line x1="180" y1="135" x2="280" y2="40" stroke="#27704a" stroke-width="1.5" marker-end="url(#arrowPT)"/>
      <rect x="284" y="20" width="280" height="42" rx="4" fill="#e8f4ea" stroke="#27704a" stroke-width="1.5"/>
      <text x="294" y="36" font-size="10" font-weight="700" fill="#27704a">"Regular Hours"</text>
      <text x="294" y="52" font-size="10" fill="#2d2926">→ Stretch tracker + Day buffer (overlap)</text>

      
      <line x1="180" y1="140" x2="280" y2="92" stroke="#4472c4" stroke-width="1.5" marker-end="url(#arrowPT)"/>
      <rect x="284" y="72" width="280" height="42" rx="4" fill="#f0f4fa" stroke="#4472c4" stroke-width="1.5"/>
      <text x="294" y="88" font-size="10" font-weight="700" fill="#4472c4">"Meal Break"</text>
      <text x="294" y="104" font-size="10" fill="#2d2926">→ Schedule-window check + reset stretch</text>

      
      <line x1="180" y1="145" x2="280" y2="144" stroke="#7a7570" stroke-width="1" stroke-dasharray="3,2" marker-end="url(#arrowPT)"/>
      <rect x="284" y="124" width="280" height="42" rx="4" fill="#f5f5f5" stroke="#999" stroke-width="1"/>
      <text x="294" y="140" font-size="10" font-weight="700" fill="#7a7570">"Annual Leave"</text>
      <text x="294" y="156" font-size="10" fill="#5a544e">→ (skipped — no path)</text>

      
      <line x1="180" y1="150" x2="280" y2="196" stroke="#7a7570" stroke-width="1" stroke-dasharray="3,2" marker-end="url(#arrowPT)"/>
      <rect x="284" y="176" width="280" height="42" rx="4" fill="#f5f5f5" stroke="#999" stroke-width="1"/>
      <text x="294" y="192" font-size="10" font-weight="700" fill="#7a7570">"Sick Leave"</text>
      <text x="294" y="208" font-size="10" fill="#5a544e">→ (skipped — no path)</text>

      
      <line x1="180" y1="155" x2="280" y2="248" stroke="#7a7570" stroke-width="1" stroke-dasharray="3,2" marker-end="url(#arrowPT)"/>
      <rect x="284" y="228" width="280" height="42" rx="4" fill="#f5f5f5" stroke="#999" stroke-width="1"/>
      <text x="294" y="244" font-size="10" font-weight="700" fill="#7a7570">"Public Holiday"</text>
      <text x="294" y="260" font-size="10" fill="#5a544e">→ (skipped — no path)</text>

      
      <text x="200" y="116" font-size="9" fill="#27704a" font-weight="700">= p_reg_type</text>
      <text x="240" y="180" font-size="9" fill="#4472c4" font-weight="700">= p_break_type</text>

      <defs>
        <marker id="arrowPT" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto" markerUnits="userSpaceOnUse">
          <path d="M0,0 L0,9 L9,4.5 z" fill="currentColor"/>
        </marker>
      </defs>

    </svg>

  </div>

  <div class="ic-snippet">
<span class="lbl">How the formula reads it</span><span class="c">/* read the type, then route */</span>
<span class="k">IF</span> (<span class="v">PayrollTimeType</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
  <span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">PayrollTimeType</span>[<span class="v">nidx</span>]

<span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span>) <span class="k">THEN</span>
  <span class="c">/* → stretch tracker + day buffer */</span>

<span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_break_type</span>) <span class="k">THEN</span>
  <span class="c">/* → schedule window + reset stretch */</span></div>

  <div class="ic-explain">The most important routing decision in the formula. Reg Hours go into the continuous-stretch tracker and the day buffer for overlap testing. Meal Break runs through the schedule-window check and resets the stretch tracker. Other types (Annual Leave, Sick, etc) silently skip both paths.</div>
</div>


<div class="input-card">
  <div class="ic-head">
    <div class="ic-eyebrow">Input 05 · Date Array</div>

    <div class="ic-name">StartTime</div>

  </div>

  <div class="ic-question">"When did this row begin?"</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>StartTime_uses.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Used in</th><th>What for</th></tr></thead>
      <tbody>
        <tr><td>Stretch tracker</td><td>Compared to previous stretchEnd → decide EXTEND or RESTART</td></tr>
        <tr><td>Pairwise overlap test</td><td>Combined with StopTime to define each row's interval</td></tr>
        <tr><td>Schedule window check</td><td>Compared to <code>p_sched_start</code> for Meal Break entries</td></tr>
        <tr><td>Qty-only detection</td><td>If start < 0.01 (near midnight), entry is a placeholder</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-mini-excel-cap">A single date value, but it feeds four different validation paths depending on the time type.</div>

  <div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
    <div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · StartTime feeds four validation paths</div>

    <svg viewBox="0 0 680 290" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:680px; display:block;" font-family="Calibri, sans-serif">

      
      <rect x="20" y="14" width="640" height="42" rx="4" fill="#fff3e0" stroke="#b97417" stroke-width="1"/>
      <text x="34" y="32" font-size="10" font-weight="700" fill="#b97417">TIMESTAMP ANATOMY:</text>
      <text x="160" y="32" font-size="11" font-family="JetBrains Mono, monospace" fill="#2d2926" font-weight="700">14-Apr-2026 10:00:00</text>
      <text x="34" y="48" font-size="9.5" fill="#5a544e">A single value combining date AND time of day. Fast Formula's DATE type holds both — you don't get them as separate fields.</text>

      
      <rect x="20" y="146" width="160" height="48" rx="4" fill="#1f1c19"/>
      <text x="100" y="166" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">aiStartTime</text>
      <text x="100" y="182" text-anchor="middle" font-size="9.5" fill="#a8a39c">DATE per row</text>

      
      
      <line x1="180" y1="160" x2="280" y2="84" stroke="#c0392b" stroke-width="1.5" marker-end="url(#arrowST)"/>
      <rect x="284" y="64" width="380" height="42" rx="4" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
      <text x="294" y="80" font-size="10" font-weight="700" fill="#c0392b">USE 1 · STRETCH TRACKER (Block 8)</text>
      <text x="294" y="96" font-size="10" fill="#2d2926">aiStartTime = stretchEnd ? → EXTEND : RESTART</text>

      
      <line x1="180" y1="165" x2="280" y2="136" stroke="#4472c4" stroke-width="1.5" marker-end="url(#arrowST)"/>
      <rect x="284" y="116" width="380" height="42" rx="4" fill="#f0f4fa" stroke="#4472c4" stroke-width="1.5"/>
      <text x="294" y="132" font-size="10" font-weight="700" fill="#4472c4">USE 2 · OVERLAP TEST (Block 7)</text>
      <text x="294" y="148" font-size="10" fill="#2d2926">aiStartTime + aiStopTime define this row's interval</text>

      
      <line x1="180" y1="175" x2="280" y2="188" stroke="#b97417" stroke-width="1.5" marker-end="url(#arrowST)"/>
      <rect x="284" y="168" width="380" height="42" rx="4" fill="#fff3e0" stroke="#b97417" stroke-width="1.5"/>
      <text x="294" y="184" font-size="10" font-weight="700" fill="#b97417">USE 3 · SCHEDULE WINDOW (Block 6e)</text>
      <text x="294" y="200" font-size="10" fill="#2d2926">aiStartTime < p_sched_start ? → flag meal break</text>

      
      <line x1="180" y1="180" x2="280" y2="240" stroke="#27704a" stroke-width="1.5" marker-end="url(#arrowST)"/>
      <rect x="284" y="220" width="380" height="42" rx="4" fill="#e8f4ea" stroke="#27704a" stroke-width="1.5"/>
      <text x="294" y="236" font-size="10" font-weight="700" fill="#27704a">USE 4 · QTY-ONLY DETECTION (Block 6b)</text>
      <text x="294" y="252" font-size="10" fill="#2d2926">aiStartTime near 00:00 ? → placeholder, not real punch</text>

      <defs>
        <marker id="arrowST" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto" markerUnits="userSpaceOnUse">
          <path d="M0,0 L0,9 L9,4.5 z" fill="currentColor"/>
        </marker>
      </defs>

    </svg>

  </div>

  <div class="ic-snippet">
<span class="lbl">How the formula reads it</span><span class="k">IF</span> (<span class="v">StartTime</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
  <span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">StartTime</span>[<span class="v">nidx</span>]

<span class="c">/* used in EXTEND vs RESTART decision */</span>
<span class="k">IF</span> (<span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">stretchEnd</span>) <span class="k">THEN</span>
  <span class="v">stretchEnd</span> <span class="op">=</span> <span class="v">aiStopTime</span>      <span class="c">// EXTEND</span>
<span class="k">ELSE</span>
  <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">aiStartTime</span>  <span class="c">// RESTART</span>

<span class="c">/* and in pairwise overlap test */</span>
<span class="k">IF</span> (<span class="v">dayStarts</span>[<span class="v">i</span>] <span class="op"><</span> <span class="v">dayStops</span>[<span class="v">j</span>]
    <span class="k">AND</span> <span class="v">dayStarts</span>[<span class="v">j</span>] <span class="op"><</span> <span class="v">dayStops</span>[<span class="v">i</span>]) <span class="k">THEN</span></div>

  <div class="ic-explain">Two jobs. <strong>Stretch tracking:</strong> compared against the previous stretch's end — if it matches, the worker continued seamlessly (extend); if there's a gap, a new stretch begins (restart). <strong>Overlap detection:</strong> paired with StopTime to define the row's interval; the strict-less-than test catches collisions while allowing back-to-back handovers.</div>
</div>


<div class="input-card">
  <div class="ic-head">
    <div class="ic-eyebrow">Input 06 · Date Array</div>

    <div class="ic-name">StopTime</div>

  </div>

  <div class="ic-question">"When did this row end?"</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>StopTime_uses.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Used in</th><th>What for</th></tr></thead>
      <tbody>
        <tr><td>Stretch tracker</td><td>Becomes the new <code>stretchEnd</code> when extending or restarting</td></tr>
        <tr><td>Pairwise overlap test</td><td>Combined with StartTime to define each row's interval</td></tr>
        <tr><td>Schedule window check</td><td>Compared to <code>p_sched_end</code> for Meal Break entries</td></tr>
        <tr><td>Continuous-hours math</td><td>Feeds the <code>contHrs</code> calculation alongside <code>stretchStart</code></td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-mini-excel-cap">Always partnered with StartTime to define an interval, but it has its own role in the schedule-window check too.</div>

  <div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
    <div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · StopTime — partnered with StartTime, standalone for schedule check</div>

    <svg viewBox="0 0 680 280" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:680px; display:block;" font-family="Calibri, sans-serif">

      
      <text x="340" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">An entry's interval = StartTime ↔ StopTime</text>

      <rect x="100" y="36" width="100" height="40" rx="3" fill="#1f1c19"/>
      <text x="150" y="54" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">aiStartTime</text>
      <text x="150" y="68" text-anchor="middle" font-size="9.5" fill="#a8a39c">14-Apr 10:00</text>

      <line x1="200" y1="56" x2="480" y2="56" stroke="#7a7570" stroke-width="2"/>
      <text x="340" y="50" text-anchor="middle" font-size="10" fill="#5a544e" font-style="italic">interval</text>

      <rect x="480" y="36" width="100" height="40" rx="3" fill="#1f1c19"/>
      <text x="530" y="54" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">aiStopTime</text>
      <text x="530" y="68" text-anchor="middle" font-size="9.5" fill="#a8a39c">14-Apr 14:45</text>

      
      <text x="340" y="110" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">Three places StopTime appears in the formula</text>

      
      <rect x="20" y="126" width="200" height="120" rx="4" fill="#f0f4fa" stroke="#4472c4" stroke-width="1.5"/>
      <rect x="20" y="126" width="200" height="22" rx="4" fill="#4472c4"/>
      <text x="120" y="142" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">USE 1 · OVERLAP TEST</text>
      <text x="34" y="166" font-size="10" font-weight="700" fill="#4472c4">Partnered with StartTime</text>
      <text x="34" y="184" font-size="9.5" fill="#5a544e">Together they define the row's</text>
      <text x="34" y="196" font-size="9.5" fill="#5a544e">interval. Block 7 compares this</text>
      <text x="34" y="208" font-size="9.5" fill="#5a544e">interval pairwise against every</text>
      <text x="34" y="220" font-size="9.5" fill="#5a544e">other row's interval.</text>
      <text x="34" y="238" font-size="9" font-family="JetBrains Mono, monospace" fill="#4472c4">starts[i] < stops[j]</text>

      
      <rect x="240" y="126" width="200" height="120" rx="4" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
      <rect x="240" y="126" width="200" height="22" rx="4" fill="#c0392b"/>
      <text x="340" y="142" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">USE 2 · STRETCH TRACKER</text>
      <text x="254" y="166" font-size="10" font-weight="700" fill="#c0392b">Becomes the new stretchEnd</text>
      <text x="254" y="184" font-size="9.5" fill="#5a544e">Block 8 stores this value as</text>
      <text x="254" y="196" font-size="9.5" fill="#5a544e">the running boundary of the</text>
      <text x="254" y="208" font-size="9.5" fill="#5a544e">continuous-work stretch.</text>
      <text x="254" y="226" font-size="9" font-family="JetBrains Mono, monospace" fill="#c0392b">stretchEnd = aiStopTime</text>
      <text x="254" y="240" font-size="9" font-family="JetBrains Mono, monospace" fill="#c0392b">contHrs = end - start</text>

      
      <rect x="460" y="126" width="200" height="120" rx="4" fill="#fff3e0" stroke="#b97417" stroke-width="1.5"/>
      <rect x="460" y="126" width="200" height="22" rx="4" fill="#b97417"/>
      <text x="560" y="142" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">USE 3 · SCHEDULE WINDOW</text>
      <text x="474" y="166" font-size="10" font-weight="700" fill="#b97417">Standalone (no StartTime)</text>
      <text x="474" y="184" font-size="9.5" fill="#5a544e">Block 6e checks if a Meal Break</text>
      <text x="474" y="196" font-size="9.5" fill="#5a544e">ends after the worker's</text>
      <text x="474" y="208" font-size="9.5" fill="#5a544e">scheduled end time.</text>
      <text x="474" y="228" font-size="9" font-family="JetBrains Mono, monospace" fill="#b97417">if aiStopTime ></text>
      <text x="474" y="240" font-size="9" font-family="JetBrains Mono, monospace" fill="#b97417">     p_sched_end → flag</text>

      
      <rect x="20" y="258" width="640" height="14" rx="3" fill="#1f1c19"/>
      <text x="340" y="269" text-anchor="middle" font-size="9.5" font-family="JetBrains Mono, monospace" fill="#e6e1d8">Most uses pair Start+Stop, but the schedule window only needs StopTime</text>

    </svg>

  </div>

  <div class="ic-snippet">
<span class="lbl">How the formula reads it</span><span class="k">IF</span> (<span class="v">StopTime</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span>
  <span class="v">aiStopTime</span> <span class="op">=</span> <span class="v">StopTime</span>[<span class="v">nidx</span>]

<span class="c">/* schedule window check (Meal Break only) */</span>
<span class="k">IF</span> (<span class="v">aiStopTime</span> <span class="op">></span> <span class="v">p_sched_end</span>) <span class="k">THEN</span>
  <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="s">'Break outside hours'</span>

<span class="c">/* contHrs calculation */</span>
<span class="v">contHrs</span> <span class="op">=</span> (<span class="v">stretchEnd</span> <span class="op">-</span> <span class="v">stretchStart</span>) <span class="op">*</span> <span class="n">24</span></div>

  <div class="ic-explain">With StartTime, defines the row's interval for overlap testing. Drives the schedule-window check — if a Meal Break ends after <code>sched_end</code>, the row gets flagged. Also feeds the continuous-hours calculation as the running stretchEnd.</div>
</div>

<div class="phase-divider">↓   FORMULA RUNS   ↓</div>


<div class="input-card output">
  <div class="ic-head">
    <div class="ic-eyebrow">Output · Text Array (Sparse)</div>

    <div class="ic-name">OUT_MSG</div>

  </div>

  <div class="ic-question">"Which rows are bad and why?"</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>OUT_MSG_messages.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Possible message</th><th>Fired by</th></tr></thead>
      <tbody>
        <tr class="row-pass"><td class="empty">(slot left empty)</td><td class="tag">Clean row — no validation issue</td></tr>
        <tr class="row-fail"><td class="msg">"Continuous work exceeds 6 hours"</td><td class="tag">Block 8 (state machine)</td></tr>
        <tr class="row-fail"><td class="msg">"Overlapping entries"</td><td class="tag">Block 7 (overlap test)</td></tr>
        <tr class="row-fail"><td class="msg">"Break outside working hours"</td><td class="tag">Block 6e (schedule window)</td></tr>
        <tr class="row-fail"><td class="msg">"RegHours start/stop required"</td><td class="tag">Block 6c (hard requirement)</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-mini-excel-cap">Sparse array indexed by row number. The framework reads each populated slot and renders a red error marker next to that row in the timecard UI; empty slots stay clean.</div>

  <div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:16px 0;">
    <div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:10px;">Diagram · Sparse output — only flagged rows have entries</div>

    <svg viewBox="0 0 680 320" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:680px; display:block;" font-family="Calibri, sans-serif">

      
      <text x="120" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="#4472c4">Sarah's timecard</text>
      <text x="120" y="36" text-anchor="middle" font-size="9.5" fill="#5a544e" font-style="italic">5 rows in OTL grid</text>

      <g transform="translate(20, 50)">
        <rect x="0" y="0" width="200" height="32" rx="2" fill="#fff" stroke="#27704a" stroke-width="1.5"/>
        <text x="10" y="20" font-size="9.5" font-weight="700" fill="#27704a">Row 1 · Reg Hours 08:30–10:00</text>

        <rect x="0" y="38" width="200" height="32" rx="2" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
        <text x="10" y="58" font-size="9.5" font-weight="700" fill="#c0392b">Row 2 · Reg Hours 10:00–14:45</text>

        <rect x="0" y="76" width="200" height="32" rx="2" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
        <text x="10" y="96" font-size="9.5" font-weight="700" fill="#c0392b">Row 3 · Meal Break 19:00–20:00</text>

        <rect x="0" y="114" width="200" height="32" rx="2" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
        <text x="10" y="134" font-size="9.5" font-weight="700" fill="#c0392b">Row 4 · Reg Hours 08:00–20:00</text>

        <rect x="0" y="152" width="200" height="32" rx="2" fill="#fff" stroke="#27704a" stroke-width="1.5"/>
        <text x="10" y="172" font-size="9.5" font-weight="700" fill="#27704a">Row 5 · Annual Leave</text>
      </g>

      
      <line x1="220" y1="66" x2="290" y2="106" stroke="#7a7570" stroke-width="1" stroke-dasharray="3,2"/>
      <line x1="220" y1="104" x2="290" y2="144" stroke="#7a7570" stroke-width="1" stroke-dasharray="3,2"/>
      <line x1="220" y1="142" x2="290" y2="182" stroke="#7a7570" stroke-width="1" stroke-dasharray="3,2"/>

      
      <text x="500" y="22" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">OUT_MSG · sparse array</text>
      <text x="500" y="36" text-anchor="middle" font-size="9.5" fill="#5a544e" font-style="italic">indexed by row number</text>

      <g transform="translate(310, 50)">
        <rect x="0" y="0" width="60" height="32" fill="#f5f5f5" stroke="#7a7570" stroke-width="0.8"/>
        <text x="30" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="#7a7570">[1]</text>
        <rect x="60" y="0" width="290" height="32" fill="#f5f5f5" stroke="#7a7570" stroke-width="0.8"/>
        <text x="205" y="20" text-anchor="middle" font-size="10" fill="#7a7570" font-style="italic">empty · row passed all checks</text>

        <rect x="0" y="38" width="60" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
        <text x="30" y="58" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">[2]</text>
        <rect x="60" y="38" width="290" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
        <text x="68" y="58" font-size="10" fill="#2d2926">"Continuous work exceeds 6 hours"</text>

        <rect x="0" y="76" width="60" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
        <text x="30" y="96" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">[3]</text>
        <rect x="60" y="76" width="290" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
        <text x="68" y="96" font-size="10" fill="#2d2926">"Break outside working hours"</text>

        <rect x="0" y="114" width="60" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
        <text x="30" y="134" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">[4]</text>
        <rect x="60" y="114" width="290" height="32" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
        <text x="68" y="134" font-size="10" fill="#2d2926">"Overlapping entries"</text>

        <rect x="0" y="152" width="60" height="32" fill="#f5f5f5" stroke="#7a7570" stroke-width="0.8"/>
        <text x="30" y="172" text-anchor="middle" font-size="10" font-weight="700" fill="#7a7570">[5]</text>
        <rect x="60" y="152" width="290" height="32" fill="#f5f5f5" stroke="#7a7570" stroke-width="0.8"/>
        <text x="205" y="172" text-anchor="middle" font-size="10" fill="#7a7570" font-style="italic">empty · row passed all checks</text>
      </g>

      
      <line x1="340" y1="248" x2="340" y2="266" stroke="#7a7570" stroke-width="2" marker-end="url(#arrowOM)"/>
      <text x="350" y="262" font-size="10" fill="#7a7570" font-style="italic">framework reads array</text>

      <rect x="20" y="270" width="640" height="40" rx="4" fill="#1f1c19"/>
      <text x="34" y="288" font-size="10" font-weight="700" fill="#e6e1d8">Result on Sarah's screen:</text>
      <text x="34" y="302" font-size="10" fill="#a8a39c">Rows 2, 3, 4 get red markers. Rows 1 and 5 stay clean. Sarah sees exactly which entries to fix.</text>

      <defs>
        <marker id="arrowOM" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto" markerUnits="userSpaceOnUse">
          <path d="M0,0 L0,9 L9,4.5 z" fill="#7a7570"/>
        </marker>
      </defs>

    </svg>

  </div>

  <div class="ic-snippet">
<span class="lbl">How the formula writes it</span><span class="c">/* declared at the top of the loop */</span>
<span class="v">OUT_MSG</span> <span class="op">=</span> <span class="v">EMPTY_TEXT_NUMBER</span>

<span class="c">/* populated only for flagged rows */</span>
<span class="k">IF</span> (<span class="v">contHrs</span> <span class="op">></span> <span class="v">p_max_cont_err</span>) <span class="k">THEN</span>
  <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>)
                 <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_cont_err</span>)

<span class="c">/* returned implicitly at end of formula */</span>
<span class="k">RETURN</span> <span class="v">OUT_MSG</span></div>

  <div class="ic-explain"><strong>Mandatory return.</strong> Sparse — only flagged rows have entries; clean rows leave their slot empty. The framework reads the array after the formula finishes and renders red error markers next to those line numbers in the worker's timecard UI.</div>
</div>

<h4>How the Six Inputs Fit Together: Six Columns of One Spreadsheet</h4>

<p>The six inputs aren't independent values — they're <strong>six parallel arrays sharing one index space</strong>. Picture a spreadsheet: each input is a column, and every timecard row occupies the same row index across all six columns at once. Reading all six arrays at index [3] gives the complete picture of one timecard row.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:18px 0;">
  <div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram · Six arrays, one shared index space</div>

  <svg viewBox="0 0 720 460" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:720px; display:block;" font-family="Calibri, sans-serif">

    
    <text x="20" y="20" font-size="11" font-weight="700" fill="#4472c4">The mental model — six arrays, each holding one type of data, all keyed by the same row index</text>

    
    <g transform="translate(20, 36)">
      
      <rect x="0" y="0" width="106" height="32" fill="#1f1c19"/>
      <text x="53" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">RECORD_POSITIONS</text>
      <text x="53" y="26" text-anchor="middle" font-size="8" fill="#a8a39c">array of TEXT</text>

      <rect x="113" y="0" width="106" height="32" fill="#1f1c19"/>
      <text x="166" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">PayrollTimeType</text>
      <text x="166" y="26" text-anchor="middle" font-size="8" fill="#a8a39c">array of TEXT</text>

      <rect x="226" y="0" width="106" height="32" fill="#1f1c19"/>
      <text x="279" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">StartTime</text>
      <text x="279" y="26" text-anchor="middle" font-size="8" fill="#a8a39c">array of DATE</text>

      <rect x="339" y="0" width="106" height="32" fill="#1f1c19"/>
      <text x="392" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">StopTime</text>
      <text x="392" y="26" text-anchor="middle" font-size="8" fill="#a8a39c">array of DATE</text>

      <rect x="452" y="0" width="106" height="32" fill="#1f1c19"/>
      <text x="505" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">measure</text>
      <text x="505" y="26" text-anchor="middle" font-size="8" fill="#a8a39c">array of NUMBER</text>

      <rect x="565" y="0" width="106" height="32" fill="#1f1c19"/>
      <text x="618" y="14" text-anchor="middle" font-size="9" font-weight="700" fill="#fff">HWM_MEASURE_DAY</text>
      <text x="618" y="26" text-anchor="middle" font-size="8" fill="#a8a39c">array of NUMBER</text>

      
      <rect x="0" y="32" width="106" height="26" fill="#fff8e7" stroke="#b97417"/>
      <text x="53" y="49" text-anchor="middle" font-size="9" font-weight="700" fill="#b97417">'HEADER'</text>
      <rect x="113" y="32" width="106" height="26" fill="#fff5f0" stroke="#c0392b"/>
      <text x="166" y="49" text-anchor="middle" font-size="9" fill="#c0392b" font-style="italic">missing</text>
      <rect x="226" y="32" width="106" height="26" fill="#fff5f0" stroke="#c0392b"/>
      <text x="279" y="49" text-anchor="middle" font-size="9" fill="#c0392b" font-style="italic">missing</text>
      <rect x="339" y="32" width="106" height="26" fill="#fff5f0" stroke="#c0392b"/>
      <text x="392" y="49" text-anchor="middle" font-size="9" fill="#c0392b" font-style="italic">missing</text>
      <rect x="452" y="32" width="106" height="26" fill="#fff5f0" stroke="#c0392b"/>
      <text x="505" y="49" text-anchor="middle" font-size="9" fill="#c0392b" font-style="italic">missing</text>
      <rect x="565" y="32" width="106" height="26" fill="#fff5f0" stroke="#c0392b"/>
      <text x="618" y="49" text-anchor="middle" font-size="9" fill="#c0392b" font-style="italic">missing</text>

      
      <rect x="0" y="58" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="53" y="75" text-anchor="middle" font-size="9" fill="#999" font-style="italic">empty</text>
      <rect x="113" y="58" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="166" y="75" text-anchor="middle" font-size="9" fill="#2d2926">'Regular Hours'</text>
      <rect x="226" y="58" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="279" y="75" text-anchor="middle" font-size="9" fill="#2d2926">09:00</text>
      <rect x="339" y="58" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="392" y="75" text-anchor="middle" font-size="9" fill="#2d2926">12:00</text>
      <rect x="452" y="58" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="505" y="75" text-anchor="middle" font-size="9" fill="#2d2926">3.0</text>
      <rect x="565" y="58" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="618" y="75" text-anchor="middle" font-size="9" fill="#999" font-style="italic">unused</text>

      
      <rect x="0" y="84" width="106" height="26" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="53" y="101" text-anchor="middle" font-size="9" fill="#999" font-style="italic">empty</text>
      <rect x="113" y="84" width="106" height="26" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="166" y="101" text-anchor="middle" font-size="9" fill="#2d2926" font-weight="700">'Meal Break'</text>
      <rect x="226" y="84" width="106" height="26" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="279" y="101" text-anchor="middle" font-size="9" fill="#2d2926" font-weight="700">12:00</text>
      <rect x="339" y="84" width="106" height="26" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="392" y="101" text-anchor="middle" font-size="9" fill="#2d2926" font-weight="700">13:00</text>
      <rect x="452" y="84" width="106" height="26" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="505" y="101" text-anchor="middle" font-size="9" fill="#2d2926" font-weight="700">1.0</text>
      <rect x="565" y="84" width="106" height="26" fill="#fff5f0" stroke="#c0392b" stroke-width="2"/>
      <text x="618" y="101" text-anchor="middle" font-size="9" fill="#999" font-style="italic">unused</text>

      
      <rect x="0" y="110" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="53" y="127" text-anchor="middle" font-size="9" fill="#999" font-style="italic">empty</text>
      <rect x="113" y="110" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="166" y="127" text-anchor="middle" font-size="9" fill="#2d2926">'Regular Hours'</text>
      <rect x="226" y="110" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="279" y="127" text-anchor="middle" font-size="9" fill="#2d2926">13:00</text>
      <rect x="339" y="110" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="392" y="127" text-anchor="middle" font-size="9" fill="#2d2926">17:00</text>
      <rect x="452" y="110" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="505" y="127" text-anchor="middle" font-size="9" fill="#2d2926">4.0</text>
      <rect x="565" y="110" width="106" height="26" fill="#fff" stroke="#999"/>
      <text x="618" y="127" text-anchor="middle" font-size="9" fill="#999" font-style="italic">unused</text>

      
      <text x="-5" y="49" text-anchor="end" font-size="11" font-weight="700" fill="#b97417">[1]</text>
      <text x="-5" y="75" text-anchor="end" font-size="11" font-weight="700" fill="#5a544e">[2]</text>
      <text x="-5" y="101" text-anchor="end" font-size="13" font-weight="700" fill="#c0392b">[3]</text>
      <text x="-5" y="127" text-anchor="end" font-size="11" font-weight="700" fill="#5a544e">[4]</text>
    </g>

    
    <rect x="20" y="186" width="680" height="40" rx="4" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
    <text x="34" y="204" font-size="10" font-weight="700" fill="#c0392b">SHARED INDEX SPACE:</text>
    <text x="180" y="204" font-size="10" fill="#2d2926">All six arrays use the SAME index numbers. Read row [3] across all six and you get the full picture of one timecard row.</text>
    <text x="34" y="220" font-size="10" fill="#5a544e" font-style="italic">No row "object" exists — each row is reassembled at the moment of reading from the six parallel slices.</text>

    
    <text x="20" y="252" font-size="11" font-weight="700" fill="#4472c4">How the formula reassembles row [3] inside the loop</text>

    <rect x="20" y="266" width="680" height="100" rx="4" fill="#1f1c19"/>
    <text x="34" y="286" font-size="10" font-family="JetBrains Mono, monospace" fill="#a8a39c">// nidx = 3 in this iteration</text>
    <text x="34" y="304" font-size="11" font-family="JetBrains Mono, monospace" fill="#e6e1d8">aiRecPos    = RECORD_POSITIONS[nidx]   // empty — this is a real entry</text>
    <text x="34" y="320" font-size="11" font-family="JetBrains Mono, monospace" fill="#e6e1d8">aiTimeType  = PayrollTimeType[nidx]    // 'Meal Break'</text>
    <text x="34" y="336" font-size="11" font-family="JetBrains Mono, monospace" fill="#e6e1d8">aiStartTime = StartTime[nidx]          // 12:00</text>
    <text x="34" y="352" font-size="11" font-family="JetBrains Mono, monospace" fill="#e6e1d8">aiStopTime  = StopTime[nidx]           // 13:00</text>

    <text x="20" y="386" font-size="10" fill="#5a544e">The single index <tspan font-family="JetBrains Mono, monospace" fill="#c0392b">nidx</tspan> walks every array in sync. <tspan font-weight="700">This is the parallel-arrays idiom in action.</tspan></text>
    <text x="20" y="402" font-size="10" fill="#5a544e">Once you internalise it, you'll see it everywhere across OTL formula types — the pattern is consistent.</text>

    
    <rect x="20" y="424" width="680" height="22" rx="3" fill="#1f1c19"/>
    <text x="34" y="440" font-size="9.5" font-family="JetBrains Mono, monospace" fill="#e6e1d8">Six arrays in · One shared index space · No row objects · Reassemble at read time</text>

  </svg>
</div>

<div class="excel-wrap">
  <div class="excel-titlebar">
    <span class="filename">Six_Arrays_One_Spreadsheet.xlsx</span>
    <span class="app">Excel</span>
  </div>

  <table class="excel-sheet">
    <thead>
      <tr>
        <th style="min-width:36px; white-space:nowrap; background:#e8e8e8; color:#555;">Idx</th>
        <th>RECORD_POSITIONS</th>
        <th>PayrollTimeType</th>
        <th>StartTime</th>
        <th>StopTime</th>
        <th>measure</th>
      </tr>
    </thead>
    <tbody>
      <tr style="background:#fff3e0;">
        <td class="row-num" style="background:#ffd180;">[1]</td>
        <td><strong>HEADER</strong></td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
      </tr>
      <tr>
        <td class="row-num">[2]</td>
        <td style="color:#999;">(empty)</td>
        <td>Regular Hours</td>
        <td class="time-cell">09:00</td>
        <td class="time-cell">12:00</td>
        <td class="num">3.0</td>
      </tr>
      <tr>
        <td class="row-num">[3]</td>
        <td style="color:#999;">(empty)</td>
        <td>Meal Break</td>
        <td class="time-cell">12:00</td>
        <td class="time-cell">13:00</td>
        <td class="num">1.0</td>
      </tr>
      <tr>
        <td class="row-num">[4]</td>
        <td style="color:#999;">(empty)</td>
        <td>Regular Hours</td>
        <td class="time-cell">13:00</td>
        <td class="time-cell">17:00</td>
        <td class="num">4.0</td>
      </tr>
      <tr style="background:#fce8e8;">
        <td class="row-num" style="background:#f5cccc;">[5]</td>
        <td style="color:#c0392b;"><strong>END_DAY</strong></td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
        <td style="color:#999;">—</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="excel-caption">A simple one-day timecard. Marker rows ([1] HEADER and [5] END_DAY) only fill the <code>RECORD_POSITIONS</code> column; their other slots are blank. Real worker entries leave RECORD_POSITIONS empty and fill the data columns. The formula reads <code>RECORD_POSITIONS</code> first to decide which path to take.</div>

<p>The formula's WHILE loop walks the index from 1 to N, reading the same index across all six arrays each iteration. There's no concept of a "row object" — each row is reassembled at the moment of reading from the parallel slices. This pattern is consistent across all of OTL's formula types, so once you internalise it once, you'll see it everywhere.</p>

<p>Return anything other than <code>OUT_MSG</code> — an extra variable, a misspelled name — and the OTL submission throws a contract error. Return exactly this and nothing else.</p>


<h2>The Complete Formula</h2>

<p>Here it is in full. Every line in this listing is exactly what gets pasted into <strong>Manage Fast Formulas</strong>. Read it once top-to-bottom — don't try to understand every line yet. We'll walk through it block by block in the next section.</p>

<div class="code-wrap">

<div class="code-header"><span>XX_TER_CONTINUOUS_HOURS_VALIDATION.ff</span><span class="label-right">Time Entry Rule</span></div>
<pre><code><span class="c">/* ============================================================
   Formula Name: XX_TER_CONTINUOUS_HOURS_VALIDATION
   Formula Type: Time Entry Rules
   Description: The Fast formula is required to validate the entry of timecard
                and show error or warning messages if entries are not accurate
                according to the requirements.
   ============================================================ */</span>
<span class="k">DEFAULT FOR</span> <span class="v">HWM_CTXARY_RECORD_POSITIONS</span> <span class="k">IS</span> <span class="v">EMPTY_TEXT_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">HWM_CTXARY_HWM_MEASURE_DAY</span>  <span class="k">IS</span> <span class="v">EMPTY_NUMBER_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">HWM_PER_ASG_ASSIGNMENT_ID</span>   <span class="k">IS</span> <span class="n">0</span>
<span class="k">DEFAULT FOR</span> <span class="v">measure</span>         <span class="k">IS</span> <span class="v">EMPTY_NUMBER_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">PayrollTimeType</span> <span class="k">IS</span> <span class="v">EMPTY_TEXT_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">StartTime</span>       <span class="k">IS</span> <span class="v">EMPTY_DATE_NUMBER</span>
<span class="k">DEFAULT FOR</span> <span class="v">StopTime</span>        <span class="k">IS</span> <span class="v">EMPTY_DATE_NUMBER</span>

<span class="k">INPUTS ARE</span>
  <span class="v">HWM_CTXARY_RECORD_POSITIONS</span>,
  <span class="v">HWM_CTXARY_HWM_MEASURE_DAY</span>,
  <span class="v">measure</span>,
  <span class="v">PayrollTimeType</span>,
  <span class="v">StartTime</span>,
  <span class="v">StopTime</span>

<span class="v">ffName</span>  <span class="op">=</span> <span class="s">'XX_TER_CONTINUOUS_HOURS_VALIDATION'</span>
<span class="v">ffs_id</span>  <span class="op">=</span> <span class="f">GET_CONTEXT</span>(<span class="v">HWM_FFS_ID</span>, <span class="n">0</span>)
<span class="v">rule_id</span> <span class="op">=</span> <span class="f">GET_CONTEXT</span>(<span class="v">HWM_RULE_ID</span>, <span class="n">0</span>)

<span class="v">NullDate</span> <span class="op">=</span> <span class="s">'01-JAN-1900'</span> (<span class="k">DATE</span>)
<span class="v">NullText</span> <span class="op">=</span> <span class="s">'**FF_NULL**'</span>

<span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> Enter '</span> <span class="op">||</span> <span class="v">ffName</span>)

<span class="k">CHANGE_CONTEXTS</span>(<span class="v">HR_ASSIGNMENT_ID</span> <span class="op">=</span> <span class="v">HWM_PER_ASG_ASSIGNMENT_ID</span>)
(
  <span class="v">sumLvl</span> <span class="op">=</span> <span class="f">Get_Hdr_Text</span>(<span class="v">rule_id</span>, <span class="s">'RUN_SUMMATION_LEVEL'</span>, <span class="s">'DAY'</span>)
  <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> sumLvl='</span> <span class="op">||</span> <span class="v">sumLvl</span>)

  <span class="v">p_break_type</span> <span class="op">=</span> <span class="s">'Meal Break'</span>
  <span class="v">p_reg_type</span>   <span class="op">=</span> <span class="s">'Regular Hours'</span>

  <span class="v">p_sched_start</span>   <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>, <span class="s">'SCHEDULE_START_HOUR'</span>,     <span class="n">9</span>)
  <span class="v">p_sched_end</span>     <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>, <span class="s">'SCHEDULE_END_HOUR'</span>,      <span class="n">18</span>)
  <span class="v">p_max_cont_err</span>  <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>, <span class="s">'MAX_CONTINUOUS_HRS_ERR'</span>,  <span class="n">6</span>)
  <span class="v">p_max_cont_warn</span> <span class="op">=</span> <span class="f">get_rvalue_number</span>(<span class="v">rule_id</span>, <span class="s">'MAX_CONTINUOUS_HRS_WARN'</span>, <span class="n">5</span>)

  <span class="v">p_msg_break</span>     <span class="op">=</span> <span class="s">'XX_BREAK_OUTSIDE_HOURS_ERR'</span>
  <span class="v">p_msg_cont_err</span>  <span class="op">=</span> <span class="s">'XX_CONT_HOURS_ERR_MSG'</span>
  <span class="v">p_msg_cont_warn</span> <span class="op">=</span> <span class="s">'XX_CONT_HOURS_WRN_MSG'</span>
  <span class="v">p_msg_overlap</span>   <span class="op">=</span> <span class="s">'XX_OVERLAP_ENTRIES_MSG'</span>
  <span class="v">p_msg_reghrs</span>    <span class="op">=</span> <span class="s">'XX_REG_HOURS_PUNCHES_REQUIRED'</span>

  <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>,
                  <span class="s">'>>> Parms sched='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">p_sched_start</span>) <span class="op">||</span> <span class="s">'-'</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">p_sched_end</span>) <span class="op">||</span>
                  <span class="s">' cErr='</span>  <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">p_max_cont_err</span>) <span class="op">||</span>
                  <span class="s">' cWarn='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">p_max_cont_warn</span>))

  <span class="v">OUT_MSG</span> <span class="op">=</span> <span class="v">EMPTY_TEXT_NUMBER</span>

  <span class="v">wMaAry</span> <span class="op">=</span> <span class="v">HWM_CTXARY_RECORD_POSITIONS</span>.<span class="f">count</span>
  <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> Start bulk wMaAry='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">wMaAry</span>))

  <span class="v">cntr</span> <span class="op">=</span> <span class="n">0</span>
  <span class="v">nidx</span> <span class="op">=</span> <span class="n">0</span>

  <span class="v">dayStarts</span> <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
  <span class="v">dayStops</span>  <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
  <span class="v">dayIdxs</span>   <span class="op">=</span> <span class="v">EMPTY_NUMBER_NUMBER</span>
  <span class="v">dayCnt</span>    <span class="op">=</span> <span class="n">0</span>

  <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">NullDate</span>
  <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">NullDate</span>
  <span class="v">inStretch</span>    <span class="op">=</span> <span class="s">'N'</span>

  <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'N'</span>

  <span class="k">WHILE</span> (<span class="v">cntr</span> <span class="op"><</span> <span class="v">wMaAry</span>) <span class="k">LOOP</span>
  (
    <span class="v">cntr</span> <span class="op">=</span> <span class="v">cntr</span> <span class="op">+</span> <span class="n">1</span>
    <span class="v">nidx</span> <span class="op">=</span> <span class="v">nidx</span> <span class="op">+</span> <span class="n">1</span>

    <span class="v">aiRecPos</span>    <span class="op">=</span> <span class="v">NullText</span>
    <span class="v">aiMeasure</span>   <span class="op">=</span> <span class="n">0</span>
    <span class="v">aiTimeType</span>  <span class="op">=</span> <span class="v">NullText</span>
    <span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">NullDate</span>
    <span class="v">aiStopTime</span>  <span class="op">=</span> <span class="v">NullDate</span>
    <span class="v">l_qty_only</span>  <span class="op">=</span> <span class="s">'N'</span>

    <span class="v">aiRecPos</span> <span class="op">=</span> <span class="v">HWM_CTXARY_RECORD_POSITIONS</span>[<span class="v">nidx</span>]

    <span class="k">IF</span> (<span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'HEADER'</span>) <span class="k">THEN</span>
    (
      <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> HEADER skipped idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
    )
    <span class="k">ELSE</span>
    (
      <span class="k">IF</span> (<span class="v">MEASURE</span>.<span class="f">exists</span>(<span class="v">nidx</span>))         <span class="k">THEN</span> ( <span class="v">aiMeasure</span>   <span class="op">=</span> <span class="v">MEASURE</span>[<span class="v">nidx</span>] )
      <span class="k">IF</span> (<span class="v">PayrollTimeType</span>.<span class="f">exists</span>(<span class="v">nidx</span>)) <span class="k">THEN</span> ( <span class="v">aiTimeType</span>  <span class="op">=</span> <span class="v">PayrollTimeType</span>[<span class="v">nidx</span>] )
      <span class="k">IF</span> (<span class="v">StartTime</span>.<span class="f">exists</span>(<span class="v">nidx</span>))       <span class="k">THEN</span> ( <span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">StartTime</span>[<span class="v">nidx</span>] )
      <span class="k">IF</span> (<span class="v">StopTime</span>.<span class="f">exists</span>(<span class="v">nidx</span>))        <span class="k">THEN</span> ( <span class="v">aiStopTime</span>  <span class="op">=</span> <span class="v">StopTime</span>[<span class="v">nidx</span>] )

      <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>,
                      <span class="s">'>>> idx='</span>  <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>)        <span class="op">||</span>
                      <span class="s">' pos='</span>     <span class="op">||</span> <span class="v">aiRecPos</span>             <span class="op">||</span>
                      <span class="s">' type=['</span>   <span class="op">||</span> <span class="v">aiTimeType</span>   <span class="op">||</span> <span class="s">']'</span>  <span class="op">||</span>
                      <span class="s">' st='</span>      <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>) <span class="op">||</span>
                      <span class="s">' sp='</span>      <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>)  <span class="op">||</span>
                      <span class="s">' m='</span>       <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">aiMeasure</span>))

      <span class="k">IF</span> (<span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'END_DAY'</span> <span class="k">OR</span> <span class="v">aiRecPos</span> <span class="op">=</span> <span class="s">'END_PERIOD'</span>) <span class="k">THEN</span>
      (
        <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> Boundary dayCnt='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">dayCnt</span>))

        <span class="k">IF</span> (<span class="v">dayCnt</span> <span class="op">></span> <span class="n">1</span>) <span class="k">THEN</span>
        ( <span class="v">i</span> <span class="op">=</span> <span class="n">1</span>
          <span class="k">WHILE</span> (<span class="v">i</span> <span class="op"><</span> <span class="v">dayCnt</span>) <span class="k">LOOP</span>
          ( <span class="v">j</span> <span class="op">=</span> <span class="v">i</span> <span class="op">+</span> <span class="n">1</span>
            <span class="k">WHILE</span> (<span class="v">j</span> <span class="op"><=</span> <span class="v">dayCnt</span>) <span class="k">LOOP</span>
            ( <span class="k">IF</span> (<span class="v">dayStarts</span>[<span class="v">i</span>] <span class="op"><</span> <span class="v">dayStops</span>[<span class="v">j</span>] <span class="k">AND</span> <span class="v">dayStarts</span>[<span class="v">j</span>] <span class="op"><</span> <span class="v">dayStops</span>[<span class="v">i</span>]) <span class="k">THEN</span>
              ( <span class="v">flagIdx</span> <span class="op">=</span> <span class="v">dayIdxs</span>[<span class="v">j</span>]
                <span class="v">OUT_MSG</span>[<span class="v">flagIdx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_overlap</span>)
                <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> OVERLAP fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">flagIdx</span>))
              )
              <span class="v">j</span> <span class="op">=</span> <span class="v">j</span> <span class="op">+</span> <span class="n">1</span>
            )
            <span class="v">i</span> <span class="op">=</span> <span class="v">i</span> <span class="op">+</span> <span class="n">1</span>
          )
        )

        <span class="v">dayStarts</span>    <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
        <span class="v">dayStops</span>     <span class="op">=</span> <span class="v">EMPTY_DATE_NUMBER</span>
        <span class="v">dayIdxs</span>      <span class="op">=</span> <span class="v">EMPTY_NUMBER_NUMBER</span>
        <span class="v">dayCnt</span>       <span class="op">=</span> <span class="n">0</span>
        <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">NullDate</span>
        <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">NullDate</span>
        <span class="v">inStretch</span>    <span class="op">=</span> <span class="s">'N'</span>
        <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'N'</span>
      )
      <span class="k">ELSE</span>
      (
        <span class="c">/* QTY-ONLY DETECTION */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span> <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span> <span class="k">AND</span> <span class="v">aiStopTime</span> <span class="op"><></span> <span class="v">NullDate</span>) <span class="k">THEN</span>
        ( <span class="v">l_st_hr</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'HH24'</span>)) <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'MI'</span>))<span class="op">/</span><span class="n">60</span>
          <span class="v">l_sp_hr</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>,  <span class="s">'HH24'</span>)) <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>,  <span class="s">'MI'</span>))<span class="op">/</span><span class="n">60</span>
          <span class="k">IF</span> (<span class="v">l_st_hr</span> <span class="op"><</span> <span class="n">0.01</span> <span class="k">AND</span> <span class="v">l_sp_hr</span> <span class="op">></span> <span class="n">23.9</span>) <span class="k">THEN</span>
          ( <span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'Y'</span>
            <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> QTY-ONLY detected idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
          )
        )

        <span class="c">/* Overlap collection - skip qty-only */</span>
        <span class="k">IF</span> (<span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'N'</span> <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span> <span class="k">AND</span> <span class="v">aiStopTime</span> <span class="op"><></span> <span class="v">NullDate</span>) <span class="k">THEN</span>
        ( <span class="v">dayCnt</span> <span class="op">=</span> <span class="v">dayCnt</span> <span class="op">+</span> <span class="n">1</span>
          <span class="v">dayStarts</span>[<span class="v">dayCnt</span>] <span class="op">=</span> <span class="v">aiStartTime</span>
          <span class="v">dayStops</span>[<span class="v">dayCnt</span>]  <span class="op">=</span> <span class="v">aiStopTime</span>
          <span class="v">dayIdxs</span>[<span class="v">dayCnt</span>]   <span class="op">=</span> <span class="v">nidx</span>
        )

        <span class="c">/* Reg Hours qty-only */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span> <span class="k">AND</span> <span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'Y'</span>) <span class="k">THEN</span>
        ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_reghrs</span>)
          <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> REGHRS QTY-ONLY fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
        )

        <span class="c">/* Reg Hours null start/stop */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span> <span class="k">AND</span> (<span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">NullDate</span> <span class="k">OR</span> <span class="v">aiStopTime</span> <span class="op">=</span> <span class="v">NullDate</span>)) <span class="k">THEN</span>
        ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_reghrs</span>)
          <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> REGHRS NULL fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
        )

        <span class="c">/* Meal break stretch reset */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_break_type</span>) <span class="k">THEN</span>
        ( <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">NullDate</span>
          <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">NullDate</span>
          <span class="v">inStretch</span>    <span class="op">=</span> <span class="s">'N'</span>
          <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'Y'</span>
          <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> MEAL RESET idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
        )

        <span class="v">l_day</span> <span class="op">=</span> <span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'DY'</span>)

        <span class="v">l_sch_date_day</span> <span class="op">=</span> <span class="f">get_date_day_of_week</span>(<span class="v">aiStartTime</span>)
        <span class="v">l_dow_char</span>     <span class="op">=</span> <span class="f">UPPER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'DY'</span>))
        <span class="v">hol</span> <span class="op">=</span> <span class="f">GET_VALUE_SET</span>(<span class="s">'XX_HOLIDAY_CALENDAR_VS'</span>,
                            <span class="s">'|=p_date='''</span> <span class="op">||</span> <span class="f">to_char</span>(<span class="v">aiStartTime</span>, <span class="s">'YYYY/MM/DD'</span>) <span class="op">||</span> <span class="s">''''</span>)

        <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>,
                        <span class="s">'dow_fn='</span>    <span class="op">||</span> <span class="v">l_sch_date_day</span> <span class="op">||</span>
                        <span class="s">' dow_char='</span> <span class="op">||</span> <span class="v">l_dow_char</span>     <span class="op">||</span>
                        <span class="s">' hol='</span>      <span class="op">||</span> <span class="v">hol</span>)

        <span class="c">/* Break outside working hours */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_break_type</span> <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span> <span class="k">AND</span> <span class="v">aiStopTime</span> <span class="op"><></span> <span class="v">NullDate</span>) <span class="k">THEN</span>
        ( <span class="v">bkStart</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'HH24'</span>)) <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStartTime</span>, <span class="s">'MI'</span>))<span class="op">/</span><span class="n">60</span>
          <span class="v">bkEnd</span>   <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>,  <span class="s">'HH24'</span>)) <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">aiStopTime</span>,  <span class="s">'MI'</span>))<span class="op">/</span><span class="n">60</span>
          <span class="k">IF</span> ((<span class="v">bkStart</span> <span class="op"><</span> <span class="v">p_sched_start</span> <span class="k">OR</span> <span class="v">bkEnd</span> <span class="op">></span> <span class="v">p_sched_end</span>)
              <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SAT'</span> <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SUN'</span> <span class="k">AND</span> <span class="f">length</span>(<span class="v">hol</span>) <span class="op">=</span> <span class="n">0</span>) <span class="k">THEN</span>
          ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_break</span>)
            <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> BREAK OUT fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
          )
        )

        <span class="c">/* Continuous stretch */</span>
        <span class="k">IF</span> (<span class="v">aiTimeType</span> <span class="op">=</span> <span class="v">p_reg_type</span> <span class="k">AND</span> <span class="v">aiStartTime</span> <span class="op"><></span> <span class="v">NullDate</span> <span class="k">AND</span> <span class="v">aiStopTime</span> <span class="op"><></span> <span class="v">NullDate</span>
            <span class="k">AND</span> <span class="v">l_qty_only</span> <span class="op">=</span> <span class="s">'N'</span> <span class="k">AND</span> <span class="v">l_meal_taken</span> <span class="op">=</span> <span class="s">'N'</span>) <span class="k">THEN</span>
        (
          <span class="k">IF</span> (<span class="v">inStretch</span> <span class="op">=</span> <span class="s">'N'</span>) <span class="k">THEN</span>
          ( <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">aiStartTime</span>
            <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">aiStopTime</span>
            <span class="v">inStretch</span>    <span class="op">=</span> <span class="s">'Y'</span>
          )
          <span class="k">ELSE</span>
          ( <span class="k">IF</span> (<span class="v">aiStartTime</span> <span class="op">=</span> <span class="v">stretchEnd</span>) <span class="k">THEN</span>
            ( <span class="v">stretchEnd</span> <span class="op">=</span> <span class="v">aiStopTime</span> )
            <span class="k">ELSE</span>
            ( <span class="v">stretchStart</span> <span class="op">=</span> <span class="v">aiStartTime</span>
              <span class="v">stretchEnd</span>   <span class="op">=</span> <span class="v">aiStopTime</span>
            )
          )

          <span class="v">endMins</span> <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchEnd</span>,   <span class="s">'J'</span>))<span class="op">*</span><span class="n">1440</span>
                  <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchEnd</span>,   <span class="s">'HH24'</span>))<span class="op">*</span><span class="n">60</span>
                  <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchEnd</span>,   <span class="s">'MI'</span>))
          <span class="v">stMins</span>  <span class="op">=</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchStart</span>, <span class="s">'J'</span>))<span class="op">*</span><span class="n">1440</span>
                  <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchStart</span>, <span class="s">'HH24'</span>))<span class="op">*</span><span class="n">60</span>
                  <span class="op">+</span> <span class="f">TO_NUMBER</span>(<span class="f">TO_CHAR</span>(<span class="v">stretchStart</span>, <span class="s">'MI'</span>))
          <span class="v">contHrs</span> <span class="op">=</span> (<span class="v">endMins</span> <span class="op">-</span> <span class="v">stMins</span>) <span class="op">/</span> <span class="n">60</span>

          <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> ContHrs='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">contHrs</span>) <span class="op">||</span> <span class="s">' idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))

          <span class="k">IF</span> (<span class="v">contHrs</span> <span class="op">></span> <span class="v">p_max_cont_err</span>
              <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SAT'</span> <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SUN'</span> <span class="k">AND</span> <span class="f">length</span>(<span class="v">hol</span>) <span class="op">=</span> <span class="n">0</span>) <span class="k">THEN</span>
          ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_cont_err</span>)
            <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> CONT ERR fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
          )
          <span class="k">ELSE</span>
          ( <span class="k">IF</span> (<span class="v">contHrs</span> <span class="op">></span> <span class="v">p_max_cont_warn</span>
                <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SAT'</span> <span class="k">AND</span> <span class="v">l_day</span> <span class="op"><></span> <span class="s">'SUN'</span> <span class="k">AND</span> <span class="f">length</span>(<span class="v">hol</span>) <span class="op">=</span> <span class="n">0</span>) <span class="k">THEN</span>
            ( <span class="v">OUT_MSG</span>[<span class="v">nidx</span>] <span class="op">=</span> <span class="f">get_msg_attribute</span>(<span class="s">'StartTime'</span>) <span class="op">||</span> <span class="f">get_output_msg</span>(<span class="s">'HXT'</span>, <span class="v">p_msg_cont_warn</span>)
              <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> CONT WARN fired idx='</span> <span class="op">||</span> <span class="f">TO_CHAR</span>(<span class="v">nidx</span>))
            )
          )
        )
      ) <span class="c">/* end ELSE - non-boundary processing */</span>
    ) <span class="c">/* end ELSE - non-HEADER */</span>

    <span class="k">IF</span> (<span class="v">nidx</span> <span class="op">></span> <span class="n">1000</span>) <span class="k">THEN</span>
    ( <span class="v">ex</span> <span class="op">=</span> <span class="f">raise_error</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'Formula '</span> <span class="op">||</span> <span class="v">ffName</span> <span class="op">||</span> <span class="s">' terminated - possible endless loop.'</span>) )

    <span class="v">rLog</span> <span class="op">=</span> <span class="f">add_rlog</span>(<span class="v">ffs_id</span>, <span class="v">rule_id</span>, <span class="s">'>>> End bulk '</span> <span class="op">||</span> <span class="v">ffName</span>)
  ) <span class="c">/* end WHILE body */</span>
) <span class="c">/* end CHANGE_CONTEXTS */</span>

<span class="k">RETURN</span> <span class="v">OUT_MSG</span></code></pre>
</div>

<p>That's the entire formula. ~200 lines, three nested control structures, one state machine, and five validations all in one pass through the array. Now let's break it down piece by piece.</p>


<h2>The Formula's Architecture</h2>

<p class="section-lead">Before reading the code line-by-line, it helps to see the shape of the whole thing. The formula has eight blocks that fall into <strong>two clean halves</strong>: the first five blocks run <em>once</em> as scaffolding (set up arrays, capture identity, bind context, read configuration, initialise state), and the last three blocks run <em>repeatedly</em> inside the WHILE loop where the actual validation happens. Every line of code belongs to exactly one of these eight blocks.</p>

<div style="background:#fafaf7; border:1px solid #e8e3d8; border-radius:6px; padding:18px; margin:18px 0;">
  <div style="font-size:10px; letter-spacing:1.5px; color:#7a7570; text-transform:uppercase; font-weight:700; margin-bottom:12px;">Diagram · Eight blocks, two halves — data flow from input arrays to OUT_MSG return</div>

  <svg viewBox="0 0 720 540" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:720px; display:block;" font-family="Calibri, sans-serif">

    
    <text x="20" y="20" font-size="11" font-weight="700" fill="#4472c4">Six input arrays enter the formula</text>

    <g transform="translate(20, 32)">
      <rect x="0" y="0" width="106" height="32" rx="3" fill="#dbe5f4" stroke="#4472c4"/>
      <text x="53" y="14" text-anchor="middle" font-size="8.5" font-weight="700" fill="#2d2926">RECORD_</text>
      <text x="53" y="26" text-anchor="middle" font-size="8.5" font-weight="700" fill="#2d2926">POSITIONS</text>

      <rect x="113" y="0" width="106" height="32" rx="3" fill="#dbe5f4" stroke="#4472c4"/>
      <text x="166" y="14" text-anchor="middle" font-size="8.5" font-weight="700" fill="#2d2926">PayrollTime</text>
      <text x="166" y="26" text-anchor="middle" font-size="8.5" font-weight="700" fill="#2d2926">Type</text>

      <rect x="226" y="0" width="106" height="32" rx="3" fill="#dbe5f4" stroke="#4472c4"/>
      <text x="279" y="22" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">StartTime</text>

      <rect x="339" y="0" width="106" height="32" rx="3" fill="#dbe5f4" stroke="#4472c4"/>
      <text x="392" y="22" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">StopTime</text>

      <rect x="452" y="0" width="106" height="32" rx="3" fill="#dbe5f4" stroke="#4472c4"/>
      <text x="505" y="22" text-anchor="middle" font-size="9" font-weight="700" fill="#2d2926">measure</text>

      <rect x="565" y="0" width="106" height="32" rx="3" fill="#dbe5f4" stroke="#4472c4"/>
      <text x="618" y="14" text-anchor="middle" font-size="8.5" font-weight="700" fill="#2d2926">HWM_MEASURE</text>
      <text x="618" y="26" text-anchor="middle" font-size="8.5" font-weight="700" fill="#2d2926">DAY</text>
    </g>

    
    <line x1="360" y1="68" x2="360" y2="92" stroke="#4472c4" stroke-width="2" marker-end="url(#arrowArch)"/>

    
    <rect x="20" y="98" width="680" height="138" rx="6" fill="#fef7f0" stroke="#b97417" stroke-width="2"/>
    <text x="34" y="116" font-size="11" font-weight="700" fill="#b97417">SETUP HALF · runs ONCE at the top of the formula</text>
    <text x="34" y="130" font-size="9.5" fill="#5a544e" font-style="italic">scaffolding — preparing everything the loop will need</text>

    
    <g transform="translate(34, 142)">
      <rect x="0" y="0" width="125" height="80" rx="4" fill="#fff" stroke="#b97417" stroke-width="1.5"/>
      <text x="62.5" y="16" text-anchor="middle" font-size="10" font-weight="700" fill="#b97417">BLOCK 1</text>
      <text x="62.5" y="34" text-anchor="middle" font-size="9.5" fill="#2d2926">Crash</text>
      <text x="62.5" y="46" text-anchor="middle" font-size="9.5" fill="#2d2926">prevention</text>
      <text x="62.5" y="68" text-anchor="middle" font-size="8" fill="#7a7570" font-family="JetBrains Mono, monospace">DEFAULT FOR</text>

      <rect x="131" y="0" width="125" height="80" rx="4" fill="#fff" stroke="#b97417" stroke-width="1.5"/>
      <text x="193.5" y="16" text-anchor="middle" font-size="10" font-weight="700" fill="#b97417">BLOCK 2</text>
      <text x="193.5" y="34" text-anchor="middle" font-size="9.5" fill="#2d2926">Self-</text>
      <text x="193.5" y="46" text-anchor="middle" font-size="9.5" fill="#2d2926">identification</text>
      <text x="193.5" y="68" text-anchor="middle" font-size="8" fill="#7a7570" font-family="JetBrains Mono, monospace">ffName, ids, log</text>

      <rect x="262" y="0" width="125" height="80" rx="4" fill="#fff" stroke="#b97417" stroke-width="1.5"/>
      <text x="324.5" y="16" text-anchor="middle" font-size="10" font-weight="700" fill="#b97417">BLOCK 3</text>
      <text x="324.5" y="34" text-anchor="middle" font-size="9.5" fill="#2d2926">Single context</text>
      <text x="324.5" y="46" text-anchor="middle" font-size="9.5" fill="#2d2926">wrap</text>
      <text x="324.5" y="68" text-anchor="middle" font-size="8" fill="#7a7570" font-family="JetBrains Mono, monospace">CHANGE_CONTEXTS</text>

      <rect x="393" y="0" width="125" height="80" rx="4" fill="#fff" stroke="#b97417" stroke-width="1.5"/>
      <text x="455.5" y="16" text-anchor="middle" font-size="10" font-weight="700" fill="#b97417">BLOCK 4</text>
      <text x="455.5" y="34" text-anchor="middle" font-size="9.5" fill="#2d2926">Per-LE</text>
      <text x="455.5" y="46" text-anchor="middle" font-size="9.5" fill="#2d2926">configuration</text>
      <text x="455.5" y="68" text-anchor="middle" font-size="8" fill="#7a7570" font-family="JetBrains Mono, monospace">get_rvalue_number</text>

      <rect x="524" y="0" width="125" height="80" rx="4" fill="#fff" stroke="#b97417" stroke-width="1.5"/>
      <text x="586.5" y="16" text-anchor="middle" font-size="10" font-weight="700" fill="#b97417">BLOCK 5</text>
      <text x="586.5" y="34" text-anchor="middle" font-size="9.5" fill="#2d2926">Three lifetimes</text>
      <text x="586.5" y="46" text-anchor="middle" font-size="9.5" fill="#2d2926">init</text>
      <text x="586.5" y="68" text-anchor="middle" font-size="8" fill="#7a7570" font-family="JetBrains Mono, monospace">OUT_MSG, buffers</text>
    </g>

    
    <line x1="360" y1="240" x2="360" y2="264" stroke="#4472c4" stroke-width="2" marker-end="url(#arrowArch)"/>
    <text x="380" y="258" font-size="9" fill="#4472c4" font-style="italic">scaffolding done → enter loop</text>

    
    <rect x="20" y="270" width="680" height="170" rx="6" fill="#f0f4fa" stroke="#4472c4" stroke-width="2"/>
    <text x="34" y="288" font-size="11" font-weight="700" fill="#4472c4">LOOP HALF · runs ONCE PER TIMECARD ROW (N times total)</text>
    <text x="34" y="302" font-size="9.5" fill="#5a544e" font-style="italic">the actual validation work — classify, accumulate, judge</text>

    
    <g transform="translate(34, 314)">
      <rect x="0" y="0" width="208" height="100" rx="4" fill="#fff" stroke="#4472c4" stroke-width="1.5"/>
      <text x="104" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#4472c4">BLOCK 6 · Per-line routing</text>
      <text x="104" y="36" text-anchor="middle" font-size="9.5" fill="#2d2926">Read row, classify by type,</text>
      <text x="104" y="50" text-anchor="middle" font-size="9.5" fill="#2d2926">route to validation path</text>
      <text x="104" y="74" text-anchor="middle" font-size="8.5" fill="#5a544e">qty-only / hard requirement</text>
      <text x="104" y="86" text-anchor="middle" font-size="8.5" fill="#5a544e">day buffer / schedule check</text>

      <rect x="214" y="0" width="208" height="100" rx="4" fill="#fff" stroke="#4472c4" stroke-width="1.5"/>
      <text x="318" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#4472c4">BLOCK 7 · Day boundary</text>
      <text x="318" y="36" text-anchor="middle" font-size="9.5" fill="#2d2926">Only fires at END_DAY:</text>
      <text x="318" y="50" text-anchor="middle" font-size="9.5" fill="#2d2926">pairwise overlap test</text>
      <text x="318" y="74" text-anchor="middle" font-size="8.5" fill="#5a544e">strict less-than check</text>
      <text x="318" y="86" text-anchor="middle" font-size="8.5" fill="#5a544e">reset day-level state</text>

      <rect x="428" y="0" width="208" height="100" rx="4" fill="#fff" stroke="#4472c4" stroke-width="1.5"/>
      <text x="532" y="18" text-anchor="middle" font-size="10" font-weight="700" fill="#4472c4">BLOCK 8 · State machine</text>
      <text x="532" y="36" text-anchor="middle" font-size="9.5" fill="#2d2926">Continuous-hours tracker:</text>
      <text x="532" y="50" text-anchor="middle" font-size="9.5" fill="#2d2926">EXTEND / RESTART / RESET</text>
      <text x="532" y="74" text-anchor="middle" font-size="8.5" fill="#5a544e">Julian Day arithmetic</text>
      <text x="532" y="86" text-anchor="middle" font-size="8.5" fill="#5a544e">error wins over warning</text>
    </g>

    
    <path d="M 670,364 C 700,364 700,470 360,470 C 60,470 60,364 70,364" fill="none" stroke="#4472c4" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowArch)"/>
    <text x="360" y="465" text-anchor="middle" font-size="9" font-weight="700" fill="#4472c4">WHILE (cntr < wMaAry) — loop back for next row</text>

    
    <line x1="360" y1="444" x2="360" y2="490" stroke="#27704a" stroke-width="2" marker-end="url(#arrowArch)"/>
    <text x="375" y="478" font-size="9" fill="#27704a" font-style="italic">loop ends → return</text>

    
    <rect x="240" y="496" width="240" height="36" rx="4" fill="#e8f4ea" stroke="#27704a" stroke-width="2"/>
    <text x="360" y="512" text-anchor="middle" font-size="11" font-weight="700" fill="#27704a">OUT_MSG returned to OTL framework</text>
    <text x="360" y="526" text-anchor="middle" font-size="9" fill="#5a544e" font-style="italic">sparse array of error messages, one per flagged row</text>

    <defs>
      <marker id="arrowArch" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto" markerUnits="userSpaceOnUse">
        <path d="M0,0 L0,10 L10,5 z" fill="#4472c4"/>
      </marker>
    </defs>

  </svg>
</div>

<div class="arch-flow">
  <div class="arch-eyebrow">Architecture · eight blocks, two halves</div>

  <div class="arch-title">From input array to OUT_MSG return</div>

  <div class="arch-stages">

    <div class="arch-stage active">
      <div class="stage-label">
        <div class="stage-num">Stage 01</div>

        <div class="stage-name">Block 1</div>

      </div>

      <div class="stage-rail"><div class="stage-dot"></div></div>

      <div class="stage-body">
        <div><span class="stage-pill scope-init">Init</span><span class="stage-pill">runs once</span></div>

        <div class="stage-headline" style="margin-top:6px;">Declare inputs and their empty-array defaults</div>

        <div class="stage-meta"><code>DEFAULT FOR</code> for every input prevents <code>FFL-09100</code> at runtime when the framework hands over a sparse array.</div>

      </div>

    </div>

    <div class="arch-stage active">
      <div class="stage-label">
        <div class="stage-num">Stage 02</div>

        <div class="stage-name">Block 2</div>

      </div>

      <div class="stage-rail"><div class="stage-dot"></div></div>

      <div class="stage-body">
        <div><span class="stage-pill scope-init">Init</span><span class="stage-pill">runs once</span></div>

        <div class="stage-headline" style="margin-top:6px;">Capture identity, define sentinels, log entry</div>

        <div class="stage-meta">Capture <code>ffs_id</code> and <code>rule_id</code> from context, declare <code>NullDate</code> and <code>NullText</code> sentinels, and write the formula's first log line so every subsequent message is scoped and traceable.</div>

      </div>

    </div>

    <div class="arch-stage active">
      <div class="stage-label">
        <div class="stage-num">Stage 03</div>

        <div class="stage-name">Block 3</div>

      </div>

      <div class="stage-rail"><div class="stage-dot"></div></div>

      <div class="stage-body">
        <div><span class="stage-pill scope-init">Init</span><span class="stage-pill">runs once</span></div>

        <div class="stage-headline" style="margin-top:6px;">Wrap the body in <code>CHANGE_CONTEXTS</code></div>

        <div class="stage-meta">One outer wrap binds <code>HR_ASSIGNMENT_ID</code> for every DBI and value-set lookup inside — <strong>200× faster</strong> than re-binding per iteration.</div>

      </div>

    </div>

    <div class="arch-stage active">
      <div class="stage-label">
        <div class="stage-num">Stage 04</div>

        <div class="stage-name">Block 4</div>

      </div>

      <div class="stage-rail"><div class="stage-dot"></div></div>

      <div class="stage-body">
        <div><span class="stage-pill scope-init">Init</span><span class="stage-pill">runs once</span></div>

        <div class="stage-headline" style="margin-top:6px;">Read configuration via <code>get_rvalue_number</code></div>

        <div class="stage-meta">Schedule bounds and continuous-hours thresholds come from the rule definition. <strong>One formula serves every LE</strong> — per-entity variation lives in the rule, not the source.</div>

      </div>

    </div>

    <div class="arch-stage active">
      <div class="stage-label">
        <div class="stage-num">Stage 05</div>

        <div class="stage-name">Block 5</div>

      </div>

      <div class="stage-rail"><div class="stage-dot"></div></div>

      <div class="stage-body">
        <div><span class="stage-pill scope-init">Init</span><span class="stage-pill">runs once</span></div>

        <div class="stage-headline" style="margin-top:6px;">Initialise day buffer, stretch tracker, OUT_MSG</div>

        <div class="stage-meta">Three pieces of state with three different lifetimes — per-line, per-day, per-formula. The lifecycle distinction is what makes the rest of the formula correct.</div>

      </div>

    </div>

    <div class="arch-stage">
      <div class="stage-label">
        <div class="stage-num">Stage 06</div>

        <div class="stage-name">Block 6</div>

      </div>

      <div class="stage-rail"><div class="stage-dot"></div></div>

      <div class="stage-body">
        <div><span class="stage-pill scope-loop">Per line</span><span class="stage-pill">in WHILE loop</span></div>

        <div class="stage-headline" style="margin-top:6px;">Read line, classify, route by time type</div>

        <div class="stage-meta">Detect qty-only placeholders (<code>00:00–23:59</code>), buffer Reg Hours for overlap, route Meal Breaks to the schedule-window check.</div>

      </div>

    </div>

    <div class="arch-stage">
      <div class="stage-label">
        <div class="stage-num">Stage 07</div>

        <div class="stage-name">Block 7</div>

      </div>

      <div class="stage-rail"><div class="stage-dot"></div></div>

      <div class="stage-body">
        <div><span class="stage-pill scope-loop">Per day</span><span class="stage-pill">at END_DAY marker</span></div>

        <div class="stage-headline" style="margin-top:6px;">Pairwise overlap test on the day buffer</div>

        <div class="stage-meta">Strict less-than (<code><</code>) intersection test. Catches collisions; allows back-to-back 12:00→12:00 handovers without false flags.</div>

      </div>

    </div>

    <div class="arch-stage">
      <div class="stage-label">
        <div class="stage-num">Stage 08</div>

        <div class="stage-name">Block 8</div>

      </div>

      <div class="stage-rail"><div class="stage-dot"></div></div>

      <div class="stage-body">
        <div><span class="stage-pill scope-loop">Per line</span><span class="stage-pill">cross-iteration state</span></div>

        <div class="stage-headline" style="margin-top:6px;">Continuous-hours state machine</div>

        <div class="stage-meta">Idle ↔ Active. EXTEND when adjacent, RESTART on gap, RESET on meal break. Compares <code>contHrs</code> against soft-warn (5h) and hard-error (6h) thresholds.</div>

      </div>

    </div>

    <div class="arch-stage">
      <div class="stage-label">
        <div class="stage-num">Return</div>

        <div class="stage-name" style="color:var(--accent);">OUT_MSG</div>

      </div>

      <div class="stage-rail"><div class="stage-dot" style="background:var(--accent);"></div></div>

      <div class="stage-body">
        <div><span class="stage-pill scope-exit">Exit</span><span class="stage-pill">framework reads sparse array</span></div>

        <div class="stage-headline" style="margin-top:6px;">Sparse array of error messages by line index</div>

        <div class="stage-meta">Empty slots = clean rows. Populated slots become red error markers in the worker's timecard UI.</div>

      </div>

    </div>

  </div>
</div>

<p>The first five blocks (Stages 01–05) make up the <strong>setup half</strong> — they run exactly once at the top of the formula, before any timecard row is processed. The last three (Stages 06–08) make up the <strong>loop half</strong> — they execute once per row inside the WHILE loop, with Block 7 firing only at day boundaries. Every line in the formula source belongs to one of these eight blocks. The Part 2 walkthrough goes through each block in detail; for now, this overview is enough to navigate the complete code listing above.</p>

<h2>Variable Naming Conventions in This Formula</h2>

<p class="section-lead">Fast Formula doesn't enforce naming rules — you can call any variable anything — but the formula in this post follows a deliberate convention. <strong>Each prefix signals the variable's role</strong>: where its value comes from, what its lifetime is, what code is allowed to write to it. Once you internalise the prefixes, the rest of the formula reads itself. This section is worth a few minutes upfront because Part 2 of this series uses these prefixes throughout the code walkthrough.</p>

<p>Seven naming patterns do all the work in this formula. The reference table below summarises them; the cards that follow explain each one in detail.</p>

<div class="excel-wrap">
  <div class="excel-titlebar">
    <span class="filename">Naming_Conventions_Reference.xlsx</span>
    <span class="app">Excel</span>
  </div>

  <table class="excel-sheet">
    <thead>
      <tr>
        <th>Prefix</th>
        <th>Means</th>
        <th>Examples in this formula</th>
        <th>Lifetime</th>
        <th>Who writes to it?</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>HWM_*</code></td>
        <td>Framework-supplied context or input</td>
        <td><code>HWM_FFS_ID</code>, <code>HWM_RULE_ID</code>, <code>HWM_PER_ASG_ASSIGNMENT_ID</code></td>
        <td>Whole formula</td>
        <td>The OTL framework (read-only)</td>
      </tr>
      <tr>
        <td><code>HWM_CTXARY_*</code></td>
        <td>Framework input <em>array</em> (one slot per timecard row)</td>
        <td><code>HWM_CTXARY_RECORD_POSITIONS</code>, <code>HWM_CTXARY_HWM_MEASURE_DAY</code></td>
        <td>Whole formula</td>
        <td>The framework (read-only)</td>
      </tr>
      <tr>
        <td><code>p_*</code></td>
        <td>Parameter read from rule configuration</td>
        <td><code>p_sched_start</code>, <code>p_max_cont_err</code>, <code>p_msg_overlap</code></td>
        <td>Whole formula</td>
        <td>Set once in Block 4, read everywhere</td>
      </tr>
      <tr>
        <td><code>ai*</code></td>
        <td>"Array input" — per-row local snapshot of input data</td>
        <td><code>aiTimeType</code>, <code>aiStartTime</code>, <code>aiStopTime</code>, <code>aiRecPos</code></td>
        <td>One iteration</td>
        <td>Reset at top of every loop iteration</td>
      </tr>
      <tr>
        <td><code>l_*</code></td>
        <td>Local working variable or flag</td>
        <td><code>l_qty_only</code>, <code>l_meal_taken</code>, <code>l_day</code>, <code>l_st_hr</code></td>
        <td>Per-row or per-day</td>
        <td>Set inside the loop body</td>
      </tr>
      <tr>
        <td><code>day*</code> / <code>stretch*</code></td>
        <td>State variables with named lifetimes</td>
        <td><code>dayStarts</code>, <code>dayCnt</code>, <code>stretchStart</code>, <code>inStretch</code></td>
        <td>Per-day / per-stretch</td>
        <td>Updated inside loop, reset at boundaries</td>
      </tr>
      <tr style="background:#fce8e8;">
        <td><code>OUT_MSG</code></td>
        <td>The formula's return value (sparse error array)</td>
        <td><code>OUT_MSG</code></td>
        <td style="color:#c0392b;">Whole formula</td>
        <td>Written only when a row needs flagging</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="excel-caption">Seven naming patterns. Each one signals a different role and lifetime, making the formula's intent visible without reading the surrounding code.</div>

<p>Now the prefixes in detail, with examples and the reasoning behind each convention:</p>


<div class="input-card">
  <div class="ic-head">
    <div class="ic-eyebrow">Prefix 01 · Framework Context</div>

    <div class="ic-name">HWM_*</div>

  </div>

  <div class="ic-question">"Where does this value come from?" → The OTL framework, before the formula even runs.</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>HWM_Examples.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Variable</th><th>What it holds</th><th>Set by</th></tr></thead>
      <tbody>
        <tr><td><code>HWM_FFS_ID</code></td><td>This run's session ID</td><td>Framework, on submission</td></tr>
        <tr><td><code>HWM_RULE_ID</code></td><td>The rule that triggered this formula</td><td>Framework, on rule binding</td></tr>
        <tr><td><code>HWM_PER_ASG_ASSIGNMENT_ID</code></td><td>The worker's HR assignment ID</td><td>Framework, from worker context</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-explain">The <code>HWM_</code> prefix — short for <em>HCM Workforce Management</em> — marks variables the OTL framework injects into the formula's scope. They're not declared by the formula author; they appear automatically when the formula runs. The values are read-only from the formula's perspective; trying to assign to them does nothing useful and can break the binding.<br><br>Their purpose is to give the formula access to <strong>contextual information about the current run</strong>: whose timecard is being validated (<code>HWM_PER_ASG_ASSIGNMENT_ID</code>), which rule fired the formula (<code>HWM_RULE_ID</code>), and what unique session ID identifies this specific submission for log tracing (<code>HWM_FFS_ID</code>). Block 2 captures these into shorter local variables (<code>ffs_id</code>, <code>rule_id</code>) for convenience throughout the rest of the formula.</div>
</div>


<div class="input-card">
  <div class="ic-head">
    <div class="ic-eyebrow">Prefix 02 · Framework Input Array</div>

    <div class="ic-name">HWM_CTXARY_*</div>

  </div>

  <div class="ic-question">"Is this a single value or a parallel array indexed by row number?" → An array, one slot per timecard row.</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>HWM_CTXARY_Examples.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Variable</th><th>Holds (per row)</th><th>Type</th></tr></thead>
      <tbody>
        <tr><td><code>HWM_CTXARY_RECORD_POSITIONS</code></td><td>Marker text or empty</td><td>TEXT_NUMBER array</td></tr>
        <tr><td><code>HWM_CTXARY_HWM_MEASURE_DAY</code></td><td>Day-aggregated quantity</td><td>NUMBER_NUMBER array</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-explain">The <code>HWM_CTXARY_</code> prefix — short for <em>HCM Workforce Management Context Array</em> — marks the framework's <strong>parallel input arrays</strong>. Where <code>HWM_*</code> holds a single value, <code>HWM_CTXARY_*</code> holds one slot per timecard row, all indexed by the same row number.<br><br>You access them like arrays: <code>HWM_CTXARY_RECORD_POSITIONS[3]</code> retrieves the value for row 3. The naming feels heavy, but it's deliberately verbose so you can never mistake a per-row array for a single-value context. Confusing the two would cause type errors at compile time — loud and easy to fix — so the convention pays off.<br><br>Note that some inputs in the <code>INPUTS ARE</code> declaration (like <code>measure</code>, <code>StartTime</code>, <code>StopTime</code>) <em>also</em> behave as parallel arrays but use cleaner names. They're framework arrays too; they just don't use the <code>HWM_CTXARY_</code> prefix because OTL's design predates the convention. Treat them the same way: per-row, indexed by row number, read-only.</div>
</div>


<div class="input-card">
  <div class="ic-head">
    <div class="ic-eyebrow">Prefix 03 · Parameter</div>

    <div class="ic-name">p_*</div>

  </div>

  <div class="ic-question">"Is this value tunable per legal entity?" → Yes — read once from the rule, then used as a constant.</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>p_Examples.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Variable</th><th>Source</th><th>Purpose</th></tr></thead>
      <tbody>
        <tr><td><code>p_sched_start</code></td><td>Rule param SCHEDULE_START_HOUR</td><td>Schedule window check</td></tr>
        <tr><td><code>p_max_cont_err</code></td><td>Rule param MAX_CONTINUOUS_HRS_ERR</td><td>Hard cap on continuous work</td></tr>
        <tr><td><code>p_max_cont_warn</code></td><td>Rule param MAX_CONTINUOUS_HRS_WARN</td><td>Soft warning threshold</td></tr>
        <tr><td><code>p_msg_overlap</code></td><td>Hardcoded message name</td><td>Error message lookup key</td></tr>
        <tr><td><code>p_break_type</code></td><td>Hardcoded layout label</td><td>Time-type matching</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-explain">The <code>p_</code> prefix marks <strong>parameter-style variables</strong> — values set once in Block 4 and used throughout the rest of the formula as effectively constant. The lowercase <code>p</code> distinguishes them from framework-supplied values (<code>HWM_*</code>) and per-row scratch (<code>ai*</code>, <code>l_*</code>).<br><br>Most <code>p_*</code> variables are read from the rule configuration via <code>get_rvalue_number</code>, which fetches numeric parameters that legal entities can tune independently — this is how one entity can use a 5-hour cap while another uses 6 with the same formula source. A few <code>p_*</code> variables (the message names like <code>p_msg_overlap</code>, the time-type labels like <code>p_break_type</code>) are hardcoded because they don't vary across the rollout.<br><br>The convention serves a code-review purpose: when you see <code>p_*</code> being assigned anywhere outside Block 4, that's a code smell — parameters should be set once at setup and treated as constant during the loop. Mutation indicates a bug or a misuse.</div>
</div>


<div class="input-card">
  <div class="ic-head">
    <div class="ic-eyebrow">Prefix 04 · Array Input Snapshot</div>

    <div class="ic-name">ai*</div>

  </div>

  <div class="ic-question">"Is this a per-row local copy of input data?" → Yes — refreshed at the top of every iteration.</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>ai_Examples.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Variable</th><th>Source array</th><th>Used for</th></tr></thead>
      <tbody>
        <tr><td><code>aiRecPos</code></td><td>RECORD_POSITIONS[nidx]</td><td>Row-type routing (HEADER vs END_DAY vs data)</td></tr>
        <tr><td><code>aiTimeType</code></td><td>PayrollTimeType[nidx]</td><td>Validation routing (Reg Hours vs Meal Break)</td></tr>
        <tr><td><code>aiStartTime</code></td><td>StartTime[nidx]</td><td>Stretch tracking, overlap testing</td></tr>
        <tr><td><code>aiStopTime</code></td><td>StopTime[nidx]</td><td>Stretch tracking, overlap testing</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-explain">The <code>ai</code> prefix stands for <strong>"array input"</strong> — per-row local snapshots of values pulled from the framework's input arrays. At the top of every loop iteration, the formula reads from the input arrays (with <code>.exists()</code> guards) and copies the values into matching <code>ai*</code> locals.<br><br>Why copy rather than reading the input arrays directly throughout the iteration? Three reasons. First, it creates a <strong>consistent snapshot</strong>: the rest of the iteration always sees the same values for "this row", even if downstream code logic gets restructured. Second, it provides a single place to apply guards (the <code>.exists()</code> checks in the read block) so you can never accidentally trigger an unguarded read elsewhere. Third, it makes the data flow obvious in code review — seeing <code>ai*</code> on the left of an assignment in the read block flags it as the "snapshot point", and the rest of the iteration cleanly works from those locals.<br><br>The <code>ai*</code> variables are reset at the top of every iteration to their sentinel values (<code>NullText</code>, <code>NullDate</code>) before the new row's reads happen. This explicit reset prevents the stale-value bug discussed in Block 5.</div>
</div>


<div class="input-card">
  <div class="ic-head">
    <div class="ic-eyebrow">Prefix 05 · Local Working Variable</div>

    <div class="ic-name">l_*</div>

  </div>

  <div class="ic-question">"Is this a temporary working value or flag inside the loop body?" → Yes.</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>l_Examples.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Variable</th><th>Type</th><th>Lifetime & purpose</th></tr></thead>
      <tbody>
        <tr><td><code>l_qty_only</code></td><td>'Y'/'N' flag</td><td>Per-row: was this row detected as a qty-only placeholder?</td></tr>
        <tr><td><code>l_meal_taken</code></td><td>'Y'/'N' flag</td><td>Per-day: has the worker logged a meal break yet today?</td></tr>
        <tr><td><code>l_day</code></td><td>3-letter day code</td><td>Per-row: 'MON', 'SAT', etc., for weekend exception checks</td></tr>
        <tr><td><code>l_st_hr</code> / <code>l_sp_hr</code></td><td>fractional hour</td><td>Per-row: punch times converted to decimal hours</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-explain">The <code>l_</code> prefix marks <strong>local working variables</strong> created inside the loop body for intermediate computation or state-tracking. Some are per-row (computed fresh each iteration), some are per-day (set once on a triggering event and persisting until the next day boundary).<br><br>The prefix's main job is to distinguish working state from input snapshots (<code>ai*</code>) and parameters (<code>p_*</code>). A formula reader scanning the code can immediately tell <code>l_qty_only</code> is a flag the formula sets itself, not data from the framework or a configuration value.<br><br>Within <code>l_*</code> there's an unwritten sub-convention: variables that hold <code>'Y'</code>/<code>'N'</code> flags use names ending in past-tense or descriptive adjectives (<code>l_meal_taken</code>, <code>l_qty_only</code>), while variables that hold computed numeric or string values use abbreviated names (<code>l_st_hr</code>, <code>l_day</code>). The convention isn't enforced, but consistency makes the code easier to scan.</div>
</div>


<div class="input-card">
  <div class="ic-head">
    <div class="ic-eyebrow">Prefix 06 · Named-Lifetime State</div>

    <div class="ic-name">day*  ·  stretch*</div>

  </div>

  <div class="ic-question">"Does this variable have a specific multi-row lifetime tied to a domain concept?" → Yes.</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>State_Group_Examples.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Group</th><th>Variables</th><th>Resets when</th></tr></thead>
      <tbody>
        <tr><td><strong>day*</strong></td><td><code>dayStarts</code>, <code>dayStops</code>, <code>dayIdxs</code>, <code>dayCnt</code></td><td>At END_DAY/END_PERIOD marker</td></tr>
        <tr><td><strong>stretch*</strong></td><td><code>stretchStart</code>, <code>stretchEnd</code>, <code>inStretch</code></td><td>On meal break or END_DAY</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-explain">Some variables can't be neatly classified as "per-row" or "whole-formula" — they live for a domain-specific period that the formula explicitly manages. The convention here is to <strong>group these by domain prefix</strong>: <code>day*</code> for variables related to a single day's accumulated state, <code>stretch*</code> for variables tracking the current continuous-work stretch.<br><br>The grouping makes the code's structure self-documenting. When a reader sees <code>dayStarts</code>, <code>dayStops</code>, <code>dayIdxs</code>, and <code>dayCnt</code> together, they immediately recognise these as the day buffer — four pieces of one logical structure. Same for <code>stretchStart</code>, <code>stretchEnd</code>, <code>inStretch</code> as the stretch tracker.<br><br>The grouping also signals that these variables must be <strong>reset together</strong>. Block 7c (the END_DAY reset) clears all four day buffer variables in one block, and clears the stretch tracker variables in the same block. Resetting some without others would corrupt state. The naming makes it obvious which variables belong in the same reset block.</div>
</div>


<div class="input-card output">
  <div class="ic-head">
    <div class="ic-eyebrow">Prefix 07 · Formula Output (Reserved Name)</div>

    <div class="ic-name">OUT_MSG</div>

  </div>

  <div class="ic-question">"Is this the value the formula returns to the framework?" → Yes — and the name is reserved.</div>

  <div class="ic-mini-excel">
    <div class="me-bar"><span>OUT_MSG_Behaviour.xlsx</span><span class="app">Excel</span></div>

    <table>
      <thead><tr><th>Idx</th><th>OUT_MSG content</th><th>Meaning</th></tr></thead>
      <tbody>
        <tr class="row-clean"><td>[2]</td><td class="empty">(no entry)</td><td class="tag">clean row</td></tr>
        <tr class="row-flagged"><td>[3]</td><td class="msg">"Continuous work exceeds 6 hours"</td><td class="tag">flagged row</td></tr>
        <tr class="row-flagged"><td>[5]</td><td class="msg">"Overlapping entries"</td><td class="tag">flagged row</td></tr>
        <tr class="row-clean"><td>[6]</td><td class="empty">(no entry)</td><td class="tag">clean row</td></tr>
      </tbody>
    </table>
  </div>

  <div class="ic-explain"><code>OUT_MSG</code> is the only variable in this formula whose name is <strong>not chosen by the author</strong> — it's reserved by the TER formula type contract. The framework expects the formula to write error messages into a variable with this exact name, and reads from it after the formula returns.<br><br>The naming is uppercase to signal "framework-reserved", distinguishing it from the lowercase prefixes (<code>p_</code>, <code>ai</code>, <code>l_</code>, <code>day</code>, <code>stretch</code>) used for author-chosen names. The pattern carries over to other formula types: payroll formulas have their own reserved output names, absence formulas have theirs.<br><br>The <code>_MSG</code> suffix hints at the data type (a sparse array of message strings indexed by row number). The combination — uppercase name plus underscore-separated suffix — is a strong visual signal that this variable is a contract surface, not a working variable. Treat it as such: write to it sparingly, only for rows that need flagging, and never reset it during the run.</div>
</div>

<h3>Why these conventions matter beyond style</h3>

<p>Naming conventions might feel like decoration, but in Fast Formula they carry real engineering value. Three benefits worth being explicit about:</p>

<p><strong>Self-documenting role.</strong> Fast Formula has no type signatures, no scope modifiers, no access controls. Every variable looks the same to the compiler. The naming convention is the only signal a reader has about whether they're looking at framework data, parameter config, per-row input, working state, or output. Without conventions, you'd have to read the variable's declaration site to understand its role — which is often hundreds of lines away.</p>

<p><strong>Code-review heuristics.</strong> When reviewing TER formulas, certain patterns are immediately suspicious. <code>p_*</code> being assigned outside Block 4 means a parameter is being mutated mid-loop — almost certainly a bug. <code>HWM_*</code> being assigned anywhere means someone tried to write to a framework value — broken. <code>ai*</code> being read without first being reset means stale data leakage. The conventions turn code review into a pattern-matching exercise; you can spot bugs by shape before reading the logic.</p>

<p><strong>Onboarding cost.</strong> A developer joining the team can read this convention table in two minutes and then read the formula's variables fluently. Without conventions, every new variable is a small puzzle — "what does <code>x</code> do? where does <code>y</code> come from?" — and onboarding takes weeks instead of days.</p>

<div class="aside">
  <div class="head">A note on consistency across formulas</div>

  Different teams use different conventions, and Oracle's documentation doesn't mandate any specific style. The patterns shown here (<code>HWM_</code>, <code>p_</code>, <code>ai</code>, <code>l_</code>, <code>day*</code>, <code>stretch*</code>, <code>OUT_MSG</code>) are common in OTL implementations but you'll see variations elsewhere. The principle that matters is <em>consistency within a project</em>. Pick a convention, document it, and apply it uniformly. The specific letters matter less than the discipline of using them.
</div>

<div style="background:#fff; padding:48px 36px 56px 36px; margin:48px 0 24px 0; border-radius:8px; border:1px solid #e8e3d8;">

  
  <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:36px; flex-wrap:wrap; gap:16px;">
    <div>
      <div style="font-family:'Manrope', -apple-system, sans-serif; font-size:34px; line-height:1.2; font-weight:300; color:#1f5fa8; letter-spacing:-0.5px;">Same formula.</div>

      <div style="font-family:'Manrope', -apple-system, sans-serif; font-size:34px; line-height:1.2; font-weight:300; color:#2d2926; letter-spacing:-0.5px; margin-top:4px;">The algorithm in detail.</div>

    </div>

    <div style="text-align:right;">
      <div style="font-family:'Manrope', -apple-system, sans-serif; font-size:14px; font-weight:700; color:#2d2926; letter-spacing:0.5px;">PART 2 OF 2</div>

      <div style="font-family:'Manrope', -apple-system, sans-serif; font-size:11px; color:#7a7570; margin-top:2px; letter-spacing:0.5px;">Coming next</div>

    </div>

  </div>

  
  <svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:800px; display:block;" font-family="Manrope, -apple-system, sans-serif">

    
    <rect x="10" y="20" width="110" height="110" fill="#f0ebe0" opacity="0.5"/>
    <rect x="24" y="34" width="82" height="82" fill="none" stroke="#c8c2b8" stroke-width="1"/>
    <g transform="translate(65, 60)" stroke="#a8a39c" stroke-width="1.3" fill="none">
      <ellipse cx="0" cy="0" rx="18" ry="5"/>
      <ellipse cx="0" cy="8" rx="18" ry="5"/>
      <ellipse cx="0" cy="16" rx="18" ry="5"/>
      <line x1="-18" y1="0" x2="-18" y2="16"/>
      <line x1="18" y1="0" x2="18" y2="16"/>
    </g>
    <text x="65" y="142" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">SETUP</text>
    <text x="65" y="154" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">PHASE</text>

    
    <rect x="140" y="20" width="110" height="110" fill="#f0ebe0" opacity="0.5"/>
    <rect x="154" y="34" width="82" height="82" fill="none" stroke="#c8c2b8" stroke-width="1"/>
    <g transform="translate(195, 75)" stroke="#a8a39c" stroke-width="1.3" fill="none">
      <circle cx="0" cy="-12" r="4"/>
      <circle cx="-14" cy="12" r="4"/>
      <circle cx="0" cy="12" r="4"/>
      <circle cx="14" cy="12" r="4"/>
      <line x1="0" y1="-8" x2="-12" y2="8"/>
      <line x1="0" y1="-8" x2="0" y2="8"/>
      <line x1="0" y1="-8" x2="12" y2="8"/>
    </g>
    <text x="195" y="142" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">PER-LINE</text>
    <text x="195" y="154" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">ROUTING</text>

    
    <rect x="270" y="20" width="110" height="110" fill="#f0ebe0" opacity="0.5"/>
    <rect x="284" y="34" width="82" height="82" fill="none" stroke="#c8c2b8" stroke-width="1"/>
    <g transform="translate(325, 75)" stroke="#a8a39c" stroke-width="1.3" fill="none">
      <rect x="-18" y="-8" width="22" height="6"/>
      <rect x="-4" y="2" width="22" height="6"/>
    </g>
    <text x="325" y="142" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">DAY</text>
    <text x="325" y="154" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">BOUNDARY</text>

    
    <rect x="400" y="14" width="125" height="125" fill="#1f5fa8"/>
    <rect x="414" y="28" width="97" height="97" fill="none" stroke="#fff" stroke-width="1.5"/>
    <g transform="translate(462, 70)" stroke="#fff" stroke-width="1.5" fill="none">
      <circle cx="-14" cy="0" r="9"/>
      <circle cx="14" cy="0" r="9"/>
      <path d="M -5,-4 Q 0,-12 5,-4" marker-end="url(#tileArrow)"/>
      <path d="M 5,4 Q 0,12 -5,4" marker-end="url(#tileArrow)"/>
    </g>
    <text x="462" y="146" text-anchor="middle" font-size="10" font-weight="700" fill="#fff" letter-spacing="0.5">STATE</text>
    <text x="462" y="158" text-anchor="middle" font-size="10" font-weight="700" fill="#fff" letter-spacing="0.5">MACHINE</text>

    
    <rect x="545" y="20" width="110" height="110" fill="#f0ebe0" opacity="0.5"/>
    <rect x="559" y="34" width="82" height="82" fill="none" stroke="#c8c2b8" stroke-width="1"/>
    <g transform="translate(600, 75)" stroke="#a8a39c" stroke-width="1.3" fill="none">
      <circle cx="-4" cy="-4" r="8"/>
      <circle cx="-4" cy="-4" r="3"/>
      <line x1="6" y1="6" x2="14" y2="14"/>
      <rect x="11" y="11" width="6" height="3" transform="rotate(45 14 12.5)"/>
    </g>
    <text x="600" y="142" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">SETUP</text>
    <text x="600" y="154" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">DEPENDENCIES</text>

    
    <rect x="675" y="20" width="110" height="110" fill="#f0ebe0" opacity="0.5"/>
    <rect x="689" y="34" width="82" height="82" fill="none" stroke="#c8c2b8" stroke-width="1"/>
    <g transform="translate(730, 75)" stroke="#a8a39c" stroke-width="1.3" fill="none">
      <rect x="-12" y="-16" width="24" height="28"/>
      <rect x="-6" y="-19" width="12" height="6"/>
      <line x1="-8" y1="-8" x2="8" y2="-8"/>
      <line x1="-8" y1="-2" x2="8" y2="-2"/>
      <line x1="-8" y1="4" x2="4" y2="4"/>
    </g>
    <text x="730" y="142" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">WORKED</text>
    <text x="730" y="154" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">EXAMPLE</text>

    
    <g transform="translate(516, 96)" fill="#1a1a1a">
      <path d="M 0,0 L 0,16 L 4,13 L 8,20 L 11,19 L 7,11 L 13,11 Z" stroke="#fff" stroke-width="0.5"/>
    </g>

    
    <g transform="translate(260, 220)">
      <rect x="0" y="0" width="280" height="40" fill="#fff" stroke="#1f5fa8" stroke-width="1.5" rx="2"/>
      <text x="140" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="#1f5fa8">Continue to Part 2 →</text>
    </g>

    <defs>
      <marker id="tileArrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto" markerUnits="userSpaceOnUse">
        <path d="M0,0 L0,6 L6,3 z" fill="#fff"/>
      </marker>
    </defs>

  </svg>

  
  <p style="margin:24px 0 0 0; font-size:13px; color:#5a544e; line-height:1.6; text-align:center;">
    Part 2 walks through every block of the formula in detail — with the <strong style="color:#1f5fa8;">continuous-hours state machine</strong> as the centrepiece. You'll also get the per-line routing decisions, the day-boundary overlap test, the setup dependencies that must exist for the formula to fire, and a worked end-to-end trace of Sarah's full timecard.
  </p>

</div>





<div style="background:#fff8e8; border:1px solid #b97417; border-radius:6px; padding:20px 24px; margin:40px 0 32px 0;">
  <div style="font-size:10px; letter-spacing:1.6px; color:#b97417; text-transform:uppercase; font-weight:700; margin-bottom:6px;">Next in The TER Series</div>

  <div style="font-size:18px; font-weight:700; color:#2d2926; margin-bottom:8px;">Part 3 — The Algorithm: Setup, Routing, and Overlap Detection</div>

  <div style="font-size:13.5px; color:#5a544e; line-height:1.6;">The data shape is settled. Now the algorithm. Part 3 walks through the formula's setup phase (crash prevention, identity capture, per-LE configuration), the per-line routing that decides which checks apply to each row, and the day-boundary pairwise overlap test — the first half of the eight-block algorithm.</div>
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