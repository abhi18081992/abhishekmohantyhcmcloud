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

  
<svg viewBox="0 0 760 320" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:760px; display:block;" font-family="Manrope, -apple-system, sans-serif">

    
<text x="70" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="1.5">RULE 01</text>
<text x="210" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="1.5">RULE 02</text>
<text x="350" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="1.5">RULE 03</text>
<text x="500" y="20" text-anchor="middle" font-size="10" font-weight="700" fill="#1f5fa8" letter-spacing="1">RULE 04 · THE HARD ONE</text>
<text x="690" y="20" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="1.5">RULE 05</text>

    
<rect x="15" y="34" width="110" height="160" fill="#f0ebe0" opacity="0.5"/>
<rect x="29" y="48" width="82" height="82" fill="none" stroke="#c8c2b8" stroke-width="1"/>
    
<g transform="translate(70, 89)" stroke="#a8a39c" stroke-width="1.3" fill="none">
<circle cx="0" cy="0" r="22"/>
<line x1="0" y1="0" x2="0" y2="-14"/>
<line x1="0" y1="0" x2="10" y2="6"/>
</g>
<text x="70" y="150" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">REGHOURS</text>
<text x="70" y="162" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">INTEGRITY</text>
<text x="70" y="180" text-anchor="middle" font-size="8" fill="#a8a39c" font-style="italic">real punches</text>
<text x="70" y="190" text-anchor="middle" font-size="8" fill="#a8a39c" font-style="italic">required</text>

    
<rect x="155" y="34" width="110" height="160" fill="#f0ebe0" opacity="0.5"/>
<rect x="169" y="48" width="82" height="82" fill="none" stroke="#c8c2b8" stroke-width="1"/>
    
<g transform="translate(210, 89)" stroke="#a8a39c" stroke-width="1.3" fill="none">
<rect x="-22" y="-10" width="28" height="8"/>
<rect x="-6" y="2" width="28" height="8"/>
</g>
<text x="210" y="150" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">NO</text>
<text x="210" y="162" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">OVERLAPS</text>
<text x="210" y="180" text-anchor="middle" font-size="8" fill="#a8a39c" font-style="italic">pairwise interval</text>
<text x="210" y="190" text-anchor="middle" font-size="8" fill="#a8a39c" font-style="italic">test</text>

    
<rect x="295" y="34" width="110" height="160" fill="#f0ebe0" opacity="0.5"/>
<rect x="309" y="48" width="82" height="82" fill="none" stroke="#c8c2b8" stroke-width="1"/>
    
<g transform="translate(350, 89)" stroke="#a8a39c" stroke-width="1.3" fill="none">
<line x1="-22" y1="-12" x2="-22" y2="12"/>
<line x1="22" y1="-12" x2="22" y2="12"/>
<line x1="-22" y1="-12" x2="-15" y2="-12"/>
<line x1="-22" y1="12" x2="-15" y2="12"/>
<line x1="22" y1="-12" x2="15" y2="-12"/>
<line x1="22" y1="12" x2="15" y2="12"/>
<rect x="-8" y="-4" width="16" height="8"/>
</g>
<text x="350" y="150" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">MEAL BREAK</text>
<text x="350" y="162" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">WINDOW</text>
<text x="350" y="180" text-anchor="middle" font-size="8" fill="#a8a39c" font-style="italic">inside scheduled</text>
<text x="350" y="190" text-anchor="middle" font-size="8" fill="#a8a39c" font-style="italic">hours</text>

    
<rect x="435" y="26" width="130" height="176" fill="#1f5fa8"/>
<rect x="449" y="40" width="102" height="102" fill="none" stroke="#fff" stroke-width="1.5"/>
    
<g transform="translate(500, 91)" stroke="#fff" stroke-width="1.6" fill="none">
<circle cx="0" cy="2" r="22"/>
<line x1="0" y1="-26" x2="0" y2="-20"/>
<rect x="-5" y="-28" width="10" height="3"/>
<line x1="0" y1="2" x2="0" y2="-10"/>
<line x1="0" y1="2" x2="11" y2="11"/>
</g>
<text x="500" y="160" text-anchor="middle" font-size="11" font-weight="700" fill="#fff" letter-spacing="0.5">CONTINUOUS-</text>
<text x="500" y="174" text-anchor="middle" font-size="11" font-weight="700" fill="#fff" letter-spacing="0.5">WORK CAP</text>
<text x="500" y="190" text-anchor="middle" font-size="9" fill="#cfdfff" font-style="italic">hard error at 6h</text>

    
<rect x="635" y="34" width="110" height="160" fill="#f0ebe0" opacity="0.5"/>
<rect x="649" y="48" width="82" height="82" fill="none" stroke="#c8c2b8" stroke-width="1"/>
    
<g transform="translate(690, 89)" stroke="#a8a39c" stroke-width="1.3" fill="none">
<path d="M 0,-22 L 22,16 L -22,16 Z"/>
<line x1="0" y1="-8" x2="0" y2="6"/>
<circle cx="0" cy="11" r="1.2" fill="#a8a39c"/>
</g>
<text x="690" y="150" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">CONTINUOUS-</text>
<text x="690" y="162" text-anchor="middle" font-size="9" font-weight="700" fill="#7a7570" letter-spacing="0.4">WORK WARN</text>
<text x="690" y="180" text-anchor="middle" font-size="8" fill="#a8a39c" font-style="italic">soft warning at 5h</text>

    
<g transform="translate(560, 116)" fill="#1a1a1a">
<path d="M 0,0 L 0,16 L 4,13 L 8,20 L 11,19 L 7,11 L 13,11 Z" stroke="#fff" stroke-width="0.5"/>
</g>

    
<g transform="translate(240, 250)">
<rect x="0" y="0" width="280" height="36" fill="#fff" stroke="#1f5fa8" stroke-width="1.5" rx="2"/>
<text x="140" y="23" text-anchor="middle" font-size="13" font-weight="700" fill="#1f5fa8">Multi-row state is what makes it hard</text>
</g>

</svg>

  
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

<svg viewBox="0 0 760 540" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:760px; display:block; margin:0 auto;" font-family="Calibri, sans-serif">

<text x="380" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#2d2926">OTL's Submission Pipeline — Where TER Fits In</text>
<text x="380" y="40" text-anchor="middle" font-size="11" fill="#7a7570">Each stage runs in order. Failures in earlier stages stop the chain.</text>

  
<rect x="40" y="68" width="160" height="62" rx="4" fill="#fff" stroke="#7a7570" stroke-width="1.5"/>
<text x="120" y="88" text-anchor="middle" font-size="10" font-weight="700" fill="#5a544e">START</text>
<text x="120" y="106" text-anchor="middle" font-size="12" font-weight="700" fill="#2d2926">Worker submits</text>
<text x="120" y="120" text-anchor="middle" font-size="10" fill="#5a544e">Timecard data leaves UI</text>

  
<line x1="120" y1="135" x2="120" y2="158" stroke="#7a7570" stroke-width="2" marker-end="url(#arrowS1)"/>

  
<rect x="40" y="160" width="160" height="74" rx="4" fill="#fff" stroke="#7a7570" stroke-width="1.5"/>
<rect x="40" y="160" width="160" height="20" rx="4" fill="#7a7570"/>
<text x="120" y="175" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">STAGE 1 · AUTOMATIC</text>
<text x="120" y="198" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">Built-in validations</text>
<text x="120" y="214" text-anchor="middle" font-size="9.5" fill="#5a544e">Required fields, data types,</text>
<text x="120" y="226" text-anchor="middle" font-size="9.5" fill="#5a544e">payroll time type existence</text>

  
<line x1="200" y1="197" x2="240" y2="197" stroke="#7a7570" stroke-width="2" marker-end="url(#arrowS1)"/>
<text x="220" y="190" text-anchor="middle" font-size="9" fill="#7a7570" font-style="italic">data shape ok</text>

  
<rect x="244" y="155" width="200" height="84" rx="4" fill="#fff5f0" stroke="#c0392b" stroke-width="2.5"/>
<rect x="244" y="155" width="200" height="22" rx="4" fill="#c0392b"/>
<text x="344" y="171" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">STAGE 2 · YOUR FORMULA RUNS HERE</text>
<text x="344" y="194" text-anchor="middle" font-size="13" font-weight="700" fill="#c0392b">Time Entry Rule (TER)</text>
<text x="344" y="212" text-anchor="middle" font-size="10" fill="#2d2926">Cross-row validation, calendar</text>
<text x="344" y="225" text-anchor="middle" font-size="10" fill="#2d2926">context, state machines</text>

  
<line x1="444" y1="197" x2="484" y2="197" stroke="#7a7570" stroke-width="2" marker-end="url(#arrowS1)"/>
<text x="464" y="190" text-anchor="middle" font-size="9" fill="#7a7570" font-style="italic">all rules pass</text>

  
<rect x="488" y="160" width="160" height="74" rx="4" fill="#fff" stroke="#7a7570" stroke-width="1.5"/>
<rect x="488" y="160" width="160" height="20" rx="4" fill="#7a7570"/>
<text x="568" y="175" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">STAGE 3 · DERIVATION</text>
<text x="568" y="198" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">Time Calculation Rule</text>
<text x="568" y="214" text-anchor="middle" font-size="9.5" fill="#5a544e">Overtime, shift premiums,</text>
<text x="568" y="226" text-anchor="middle" font-size="9.5" fill="#5a544e">allowances from valid time</text>

  
<line x1="568" y1="235" x2="568" y2="258" stroke="#7a7570" stroke-width="2" marker-end="url(#arrowS1)"/>

  
<rect x="488" y="260" width="160" height="74" rx="4" fill="#fff" stroke="#7a7570" stroke-width="1.5"/>
<rect x="488" y="260" width="160" height="20" rx="4" fill="#7a7570"/>
<text x="568" y="275" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">STAGE 4 · HUMAN REVIEW</text>
<text x="568" y="298" text-anchor="middle" font-size="11" font-weight="700" fill="#2d2926">Approval workflow</text>
<text x="568" y="314" text-anchor="middle" font-size="9.5" fill="#5a544e">Manager review, exception</text>
<text x="568" y="326" text-anchor="middle" font-size="9.5" fill="#5a544e">handling, sign-off</text>

  
<line x1="568" y1="335" x2="568" y2="358" stroke="#7a7570" stroke-width="2" marker-end="url(#arrowS1)"/>

  
<rect x="488" y="360" width="160" height="62" rx="4" fill="#e8f4ea" stroke="#27704a" stroke-width="1.5"/>
<text x="568" y="380" text-anchor="middle" font-size="10" font-weight="700" fill="#27704a">FINISH</text>
<text x="568" y="398" text-anchor="middle" font-size="12" font-weight="700" fill="#2d2926">Time repository</text>
<text x="568" y="412" text-anchor="middle" font-size="10" fill="#5a544e">Data persisted, payroll-ready</text>

  
<line x1="120" y1="234" x2="120" y2="290" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowFail)"/>
<text x="130" y="265" font-size="9.5" fill="#c0392b" font-style="italic">if invalid</text>

<line x1="344" y1="239" x2="344" y2="290" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrowFail)"/>
<text x="354" y="265" font-size="9.5" fill="#c0392b" font-style="italic">if rules fail</text>

  
<rect x="40" y="294" width="404" height="64" rx="4" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
<rect x="40" y="294" width="404" height="20" rx="4" fill="#c0392b"/>
<text x="242" y="309" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">FAILURE PATH · TIMECARD RETURNS TO WORKER</text>
<text x="242" y="332" text-anchor="middle" font-size="11" fill="#2d2926">Red error markers appear next to flagged rows.</text>
<text x="242" y="348" text-anchor="middle" font-size="11" fill="#2d2926">Worker must fix all errors before resubmission is accepted.</text>

  
<line x1="40" y1="448" x2="720" y2="448" stroke="#e8e3d8" stroke-width="1"/>
<text x="380" y="472" text-anchor="middle" font-size="12" font-weight="700" fill="#2d2926">Where to put each kind of validation logic</text>

<rect x="40" y="484" width="170" height="56" rx="3" fill="#f5f1e8" stroke="#7a7570" stroke-width="1"/>
<text x="125" y="500" text-anchor="middle" font-size="10" font-weight="700" fill="#7a7570">DECLARATIVE CONFIG</text>
<text x="125" y="518" text-anchor="middle" font-size="10" fill="#2d2926">Required-field rules,</text>
<text x="125" y="531" text-anchor="middle" font-size="10" fill="#2d2926">type checks → Stage 1</text>

<rect x="220" y="484" width="170" height="56" rx="3" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
<text x="305" y="500" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">FAST FORMULA — TER</text>
<text x="305" y="518" text-anchor="middle" font-size="10" fill="#2d2926">Cross-row, calendar,</text>
<text x="305" y="531" text-anchor="middle" font-size="10" fill="#2d2926">stateful logic → Stage 2</text>

<rect x="400" y="484" width="170" height="56" rx="3" fill="#f5f1e8" stroke="#7a7570" stroke-width="1"/>
<text x="485" y="500" text-anchor="middle" font-size="10" font-weight="700" fill="#7a7570">FAST FORMULA — TCR</text>
<text x="485" y="518" text-anchor="middle" font-size="10" fill="#2d2926">Derivations from</text>
<text x="485" y="531" text-anchor="middle" font-size="10" fill="#2d2926">valid data → Stage 3</text>

<rect x="580" y="484" width="160" height="56" rx="3" fill="#f5f1e8" stroke="#7a7570" stroke-width="1"/>
<text x="660" y="500" text-anchor="middle" font-size="10" font-weight="700" fill="#7a7570">WORKFLOW</text>
<text x="660" y="518" text-anchor="middle" font-size="10" fill="#2d2926">Manager judgement,</text>
<text x="660" y="531" text-anchor="middle" font-size="10" fill="#2d2926">exceptions → Stage 4</text>

  
<defs>
<marker id="arrowS1" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse">
<path d="M0,0 L0,8 L8,4 z" fill="#7a7570"/>
</marker>
<marker id="arrowFail" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse">
<path d="M0,0 L0,8 L8,4 z" fill="#c0392b"/>
</marker>
</defs>

</svg>

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

<svg viewBox="0 0 760 360" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:760px; display:block; margin:0 auto;" font-family="Calibri, sans-serif">

<text x="380" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#2d2926">Sarah's Tuesday, 14-Apr-2026 — What the formula sees</text>
<text x="380" y="40" text-anchor="middle" font-size="11" fill="#7a7570">Three problems are visible the moment you draw the rows on a timeline</text>

  
  

  
<text x="360" y="58" text-anchor="middle" font-size="10" fill="#b97417" font-weight="700">SCHEDULE WINDOW · 09:00 — 18:00</text>

  
<text x="285" y="78" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">CONTINUOUS WORK · 6h 15m — over the 6h cap</text>

  
<rect x="180" y="100" width="360" height="180" fill="#fff3e0" opacity="0.5"/>

  
<line x1="60" y1="100" x2="700" y2="100" stroke="#999" stroke-width="0.5"/>
<line x1="60" y1="280" x2="700" y2="280" stroke="#999" stroke-width="1.5"/>

  
<text x="60" y="298" text-anchor="middle" font-size="10" fill="#5a544e">06:00</text>
<text x="100" y="298" text-anchor="middle" font-size="10" fill="#5a544e">07:00</text>
<text x="140" y="298" text-anchor="middle" font-size="10" fill="#5a544e">08:00</text>
<text x="180" y="298" text-anchor="middle" font-size="10" fill="#b97417" font-weight="700">09:00</text>
<text x="220" y="298" text-anchor="middle" font-size="10" fill="#5a544e">10:00</text>
<text x="260" y="298" text-anchor="middle" font-size="10" fill="#5a544e">11:00</text>
<text x="300" y="298" text-anchor="middle" font-size="10" fill="#5a544e">12:00</text>
<text x="340" y="298" text-anchor="middle" font-size="10" fill="#5a544e">13:00</text>
<text x="380" y="298" text-anchor="middle" font-size="10" fill="#5a544e">14:00</text>
<text x="420" y="298" text-anchor="middle" font-size="10" fill="#5a544e">15:00</text>
<text x="460" y="298" text-anchor="middle" font-size="10" fill="#5a544e">16:00</text>
<text x="500" y="298" text-anchor="middle" font-size="10" fill="#5a544e">17:00</text>
<text x="540" y="298" text-anchor="middle" font-size="10" fill="#b97417" font-weight="700">18:00</text>
<text x="580" y="298" text-anchor="middle" font-size="10" fill="#5a544e">19:00</text>
<text x="620" y="298" text-anchor="middle" font-size="10" fill="#5a544e">20:00</text>
<text x="660" y="298" text-anchor="middle" font-size="10" fill="#5a544e">21:00</text>
<text x="700" y="298" text-anchor="middle" font-size="10" fill="#5a544e">22:00</text>

  
<g stroke="#e8e3d8" stroke-width="0.5">
<line x1="100" y1="100" x2="100" y2="280"/>
<line x1="140" y1="100" x2="140" y2="280"/>
<line x1="180" y1="100" x2="180" y2="280"/>
<line x1="220" y1="100" x2="220" y2="280"/>
<line x1="260" y1="100" x2="260" y2="280"/>
<line x1="300" y1="100" x2="300" y2="280"/>
<line x1="340" y1="100" x2="340" y2="280"/>
<line x1="380" y1="100" x2="380" y2="280"/>
<line x1="420" y1="100" x2="420" y2="280"/>
<line x1="460" y1="100" x2="460" y2="280"/>
<line x1="500" y1="100" x2="500" y2="280"/>
<line x1="540" y1="100" x2="540" y2="280"/>
<line x1="580" y1="100" x2="580" y2="280"/>
<line x1="620" y1="100" x2="620" y2="280"/>
<line x1="660" y1="100" x2="660" y2="280"/>
</g>

  
<line x1="180" y1="100" x2="180" y2="280" stroke="#b97417" stroke-width="1.5" stroke-dasharray="3,2"/>
<line x1="540" y1="100" x2="540" y2="280" stroke="#b97417" stroke-width="1.5" stroke-dasharray="3,2"/>

  
<text x="50" y="126" text-anchor="end" font-size="10" font-weight="700" fill="#27704a">Row 1</text>
<text x="50" y="140" text-anchor="end" font-size="9" fill="#5a544e">Reg Hours</text>

<text x="50" y="166" text-anchor="end" font-size="10" font-weight="700" fill="#c0392b">Row 2</text>
<text x="50" y="180" text-anchor="end" font-size="9" fill="#5a544e">Reg Hours</text>

<text x="50" y="206" text-anchor="end" font-size="10" font-weight="700" fill="#c0392b">Row 3</text>
<text x="50" y="220" text-anchor="end" font-size="9" fill="#5a544e">Meal Break</text>

<text x="50" y="246" text-anchor="end" font-size="10" font-weight="700" fill="#c0392b">Row 4</text>
<text x="50" y="260" text-anchor="end" font-size="9" fill="#5a544e">Reg Hours</text>

  
<rect x="160" y="112" width="60" height="24" rx="2" fill="#27704a" opacity="0.85"/>
<text x="190" y="128" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">08:30 – 10:00</text>

  
<rect x="220" y="152" width="190" height="24" rx="2" fill="#c0392b" opacity="0.85"/>
<text x="315" y="168" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">10:00 – 14:45 (4h 45m)</text>

  
<rect x="580" y="192" width="40" height="24" rx="2" fill="#c0392b" opacity="0.85"/>
<text x="600" y="208" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">19–20</text>

  
<rect x="140" y="232" width="480" height="24" rx="2" fill="#c0392b" opacity="0.6" stroke="#c0392b" stroke-width="2"/>
<text x="380" y="248" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">08:00 – 20:00 (12h block, overlaps everything)</text>

  

  
<line x1="160" y1="112" x2="160" y2="92" stroke="#c0392b" stroke-width="1" stroke-dasharray="3,2"/>
<line x1="410" y1="152" x2="410" y2="92" stroke="#c0392b" stroke-width="1" stroke-dasharray="3,2"/>
<line x1="160" y1="92" x2="410" y2="92" stroke="#c0392b" stroke-width="2"/>

  
<text x="600" y="186" text-anchor="middle" font-size="9" fill="#c0392b" font-style="italic">outside</text>
<text x="600" y="236" text-anchor="middle" font-size="9" fill="#c0392b" font-style="italic">schedule</text>

  
<rect x="140" y="228" width="480" height="32" fill="none" stroke="#c0392b" stroke-width="1" stroke-dasharray="4,3"/>

  
<rect x="60" y="316" width="14" height="12" fill="#27704a" opacity="0.85"/>
<text x="80" y="326" font-size="10" fill="#2d2926">Clean entry</text>

<rect x="160" y="316" width="14" height="12" fill="#c0392b" opacity="0.85"/>
<text x="180" y="326" font-size="10" fill="#2d2926">Flagged entry</text>

<rect x="270" y="316" width="14" height="12" fill="#fff3e0" stroke="#b97417" stroke-width="0.5"/>
<text x="290" y="326" font-size="10" fill="#2d2926">Schedule window</text>

<line x1="395" y1="322" x2="415" y2="322" stroke="#c0392b" stroke-width="1" stroke-dasharray="3,2"/>
<text x="420" y="326" font-size="10" fill="#2d2926">Continuous-work span</text>

</svg>

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

<svg viewBox="0 0 920 360" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:920px; display:block; margin:0 auto;" font-family="Manrope, sans-serif">

  
<text x="460" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#2d2926">Sarah's Tuesday — Row by Hour Grid</text>
<text x="460" y="40" text-anchor="middle" font-size="11" fill="#7a7570">Each row's lifecycle across the day. Numbers count cumulative hours within the entry.</text>

  
<rect x="222" y="56" width="450" height="14" fill="#fff3e0" stroke="#b97417" stroke-width="1" stroke-dasharray="3,2"/>
<text x="447" y="67" text-anchor="middle" font-size="10" font-weight="700" fill="#b97417">SCHEDULE WINDOW (09:00 — 18:00)</text>

  
  
  
<rect x="14" y="74" width="780" height="26" fill="#2d2926"/>
<text x="64" y="92" text-anchor="middle" font-size="10" font-weight="700" fill="#fff" letter-spacing="0.5">ENTRY</text>

  
  
  
  
<text x="141" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">06</text>
<text x="180" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">07</text>
<text x="219" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">08</text>
<text x="258" y="92" text-anchor="middle" font-size="10" font-weight="700" fill="#fff8e8">09</text>
<text x="297" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">10</text>
<text x="336" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">11</text>
<text x="375" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">12</text>
<text x="414" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">13</text>
<text x="453" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">14</text>
<text x="492" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">15</text>
<text x="531" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">16</text>
<text x="570" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">17</text>
<text x="609" y="92" text-anchor="middle" font-size="10" font-weight="700" fill="#fff8e8">18</text>
<text x="648" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">19</text>
<text x="687" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">20</text>
<text x="726" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">21</text>
<text x="765" y="92" text-anchor="middle" font-size="10" font-weight="600" fill="#fff">22</text>

<text x="850" y="92" text-anchor="middle" font-size="10" font-weight="700" fill="#fff" letter-spacing="0.5">RESULT</text>

  
<g stroke="#e8e3d8" stroke-width="0.5">
<line x1="122" y1="100" x2="122" y2="276"/>
<line x1="161" y1="100" x2="161" y2="276"/>
<line x1="200" y1="100" x2="200" y2="276"/>
<line x1="239" y1="100" x2="239" y2="276"/>
<line x1="278" y1="100" x2="278" y2="276"/>
<line x1="317" y1="100" x2="317" y2="276"/>
<line x1="356" y1="100" x2="356" y2="276"/>
<line x1="395" y1="100" x2="395" y2="276"/>
<line x1="434" y1="100" x2="434" y2="276"/>
<line x1="473" y1="100" x2="473" y2="276"/>
<line x1="512" y1="100" x2="512" y2="276"/>
<line x1="551" y1="100" x2="551" y2="276"/>
<line x1="590" y1="100" x2="590" y2="276"/>
<line x1="629" y1="100" x2="629" y2="276"/>
<line x1="668" y1="100" x2="668" y2="276"/>
<line x1="707" y1="100" x2="707" y2="276"/>
<line x1="746" y1="100" x2="746" y2="276"/>
<line x1="785" y1="100" x2="785" y2="276"/>
</g>

  
<line x1="239" y1="100" x2="239" y2="276" stroke="#b97417" stroke-width="1" stroke-dasharray="3,2"/>
<line x1="590" y1="100" x2="590" y2="276" stroke="#b97417" stroke-width="1" stroke-dasharray="3,2"/>

  
<rect x="14" y="100" width="780" height="40" fill="#f5f1e8" opacity="0.3"/>
<line x1="14" y1="140" x2="794" y2="140" stroke="#e8e3d8" stroke-width="1"/>

<text x="64" y="118" text-anchor="middle" font-size="10" font-weight="700" fill="#27704a">Row 1</text>
<text x="64" y="131" text-anchor="middle" font-size="9" fill="#5a544e">Reg Hrs</text>

  
  
<rect x="200" y="106" width="39" height="28" fill="#e8f4ea" stroke="#27704a" stroke-width="1"/>
<text x="219" y="125" text-anchor="middle" font-size="11" font-weight="700" fill="#27704a">RU</text>

  
<rect x="239" y="106" width="39" height="28" fill="#e8f4ea" stroke="#27704a" stroke-width="1"/>
<text x="258" y="125" text-anchor="middle" font-size="11" font-weight="700" fill="#27704a">1</text>

  
<text x="850" y="120" text-anchor="middle" font-size="10" font-weight="700" fill="#27704a">CLEAN</text>
<text x="850" y="132" text-anchor="middle" font-size="9" fill="#5a544e">08:30 – 10:00</text>

  
<line x1="14" y1="180" x2="794" y2="180" stroke="#e8e3d8" stroke-width="1"/>

<text x="64" y="158" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">Row 2</text>
<text x="64" y="171" text-anchor="middle" font-size="9" fill="#5a544e">Reg Hrs</text>

  
  
<rect x="278" y="146" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="297" y="165" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">RU</text>

  
<rect x="317" y="146" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="336" y="165" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">1</text>

  
<rect x="356" y="146" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="375" y="165" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">2</text>

  
<rect x="395" y="146" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="414" y="165" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">3</text>

  
<rect x="434" y="146" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="453" y="165" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">4</text>

  
  
<rect x="434" y="146" width="39" height="28" fill="none" stroke="#c0392b" stroke-width="2.5"/>

  
<line x1="465" y1="178" x2="495" y2="200" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrowGrid)"/>
<text x="540" y="204" text-anchor="middle" font-size="9" fill="#c0392b" font-style="italic">6h cap breached at 14:30</text>

  
<text x="850" y="160" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">FLAGGED</text>
<text x="850" y="172" text-anchor="middle" font-size="9" fill="#5a544e">cont > 6h</text>

  
<line x1="14" y1="220" x2="794" y2="220" stroke="#e8e3d8" stroke-width="1"/>

<text x="64" y="198" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">Row 3</text>
<text x="64" y="211" text-anchor="middle" font-size="9" fill="#5a544e">Meal</text>

  
  
<rect x="629" y="186" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1.5"/>
<text x="648" y="205" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">RU</text>

  
<text x="850" y="200" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">FLAGGED</text>
<text x="850" y="212" text-anchor="middle" font-size="9" fill="#5a544e">outside hours</text>

  
<text x="64" y="240" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">Row 4</text>
<text x="64" y="253" text-anchor="middle" font-size="9" fill="#5a544e">Reg Hrs</text>

  
<rect x="200" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="219" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">RU</text>

<rect x="239" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="258" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">1</text>

<rect x="278" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="297" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">2</text>

<rect x="317" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="336" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">3</text>

<rect x="356" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="375" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">4</text>

<rect x="395" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="414" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">5</text>

<rect x="434" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="453" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">6</text>

<rect x="473" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="492" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">7</text>

<rect x="512" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="531" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">8</text>

<rect x="551" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="570" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">9</text>

<rect x="590" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="609" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">10</text>

<rect x="629" y="226" width="39" height="28" fill="#fff5f0" stroke="#c0392b" stroke-width="1"/>
<text x="648" y="245" text-anchor="middle" font-size="11" font-weight="700" fill="#c0392b">11</text>

  
<text x="850" y="240" text-anchor="middle" font-size="10" font-weight="700" fill="#c0392b">FLAGGED</text>
<text x="850" y="252" text-anchor="middle" font-size="9" fill="#5a544e">overlaps 1, 2, 3</text>

  
<line x1="14" y1="280" x2="794" y2="280" stroke="#e8e3d8" stroke-width="1"/>

<rect x="20" y="296" width="14" height="12" fill="#e8f4ea" stroke="#27704a" stroke-width="0.8"/>
<text x="40" y="306" font-size="10" fill="#2d2926">Clean cell</text>

<rect x="120" y="296" width="14" height="12" fill="#fff5f0" stroke="#c0392b" stroke-width="0.8"/>
<text x="140" y="306" font-size="10" fill="#2d2926">Flagged cell</text>

<text x="220" y="306" font-size="10" font-family="JetBrains Mono, monospace" font-weight="700" fill="#2d2926">RU</text>
<text x="240" y="306" font-size="10" fill="#2d2926">= row's start hour</text>

<text x="380" y="306" font-size="10" font-weight="700" fill="#2d2926">1, 2, 3...</text>
<text x="425" y="306" font-size="10" fill="#2d2926">= cumulative hours within entry</text>

<rect x="620" y="296" width="14" height="12" fill="#fff3e0" stroke="#b97417" stroke-width="0.8"/>
<text x="640" y="306" font-size="10" fill="#2d2926">Schedule window (09:00 — 18:00)</text>

  
<rect x="14" y="318" width="780" height="34" rx="3" fill="#fff8e8" stroke="#b97417" stroke-width="1"/>
<text x="28" y="332" font-size="10" font-weight="700" fill="#b97417" letter-spacing="0.4">HOW TO READ:</text>
<text x="120" y="332" font-size="10" fill="#2d2926">Each row's lifecycle runs left to right. Row 2 hits hour 4 of continuous work at 14:00 — the 6h cap fires</text>
<text x="28" y="346" font-size="10" fill="#2d2926">at the next cell. Row 3's only cell sits past 18:00, outside the schedule. Row 4 occupies the same hours as rows 1, 2, and 3.</text>

<defs>
<marker id="arrowGrid" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto" markerUnits="userSpaceOnUse">
<path d="M0,0 L0,9 L9,4.5 z" fill="#c0392b"/>
</marker>
</defs>

</svg>

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