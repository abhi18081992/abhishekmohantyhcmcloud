---
title: "Oracle Fast Formula: Post Election Edit — How to Validate Cross-Plan Dependencies Using CHANGE_CONTEXTS and BEN_PEN Array DBIs"
description: "Oracle Fast Formula — Post Election Edit :root { --bg-primary: #ffffff; --bg-secondary: #f7f7f8; --bg-card: #f2f2f3; --bg-code: #1a1a1a; --text-primary: #000000; --text-secondary: #666666; --text-head"
pubDate: 2026-04-06
tags: ["Fast Formula", "Oracle HCM Cloud", "Benefits", "DBI", "CHANGE_CONTEXTS"]
---


<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Oracle Fast Formula — Post Election Edit</title>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Source+Code+Pro:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-primary: #ffffff; --bg-secondary: #f7f7f8; --bg-card: #f2f2f3; --bg-code: #1a1a1a;
    --text-primary: #000000; --text-secondary: #666666; --text-heading: #111111;
    --accent-red: #d63031; --accent-blue: #0984e3; --accent-green: #00b894;
    --accent-yellow: #d4a017; --accent-purple: #6c5ce7; --accent-cyan: #00838f;
    --accent-orange: #e17055; --border-red: #c0392b; --border-subtle: #e0e0e0;
    --tag-bg: #f0f0f0; --tag-text: #555555;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Open Sans', sans-serif; background: var(--bg-primary); color: #000; line-height: 1.8; font-size: 15px; }
  .container { max-width: 780px; margin: 0 auto; padding: 40px 20px; }

  /* ── Tags ── */
  .tags-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
  .tag { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; padding: 5px 12px; border-radius: 0; background: var(--tag-bg); color: var(--tag-text); border: 1px solid var(--border-subtle); }
  .tag.hl { background: rgba(192,57,43,0.08); color: var(--border-red); border-color: rgba(192,57,43,0.25); }

  /* ── Title block ── */
  h1 { font-size: 24px; font-weight: 700; color: var(--text-heading); line-height: 1.35; margin-bottom: 10px; }
  .subtitle { font-size: 14px; color: #000; margin-bottom: 10px; line-height: 1.5; }
  .meta { font-size: 13px; color: #000; margin-bottom: 28px; padding-bottom: 16px; border-bottom: 1px solid var(--border-subtle); }

  /* ── Author card ── */
  .author-card { display: flex; align-items: center; gap: 16px; margin-bottom: 32px; padding: 14px 16px; background: var(--bg-secondary); border-radius: 6px; border-left: 3px solid var(--border-red); }
  .av { width: 42px; height: 42px; border-radius: 50%; background: var(--border-red); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 15px; color: #fff; flex-shrink: 0; }
  .author-card .name { font-weight: 700; color: var(--text-heading); font-size: 14px; }
  .author-card .role { font-size: 12px; color: #000; line-height: 1.5; }

  /* ── Headings ── */
  h2 { font-size: 19px; font-weight: 700; color: var(--text-heading); margin-top: 40px; margin-bottom: 14px; padding-bottom: 6px; border-bottom: 2px solid var(--border-red); }
  h3 { font-size: 15px; font-weight: 700; color: var(--text-heading); margin-top: 26px; margin-bottom: 10px; }

  /* ── Body text ── */
  p { margin-bottom: 13px; }
  strong { color: var(--text-heading); }
  em { color: var(--accent-orange); font-style: normal; }
  code { font-family: 'Source Code Pro', monospace; font-size: 12.5px; background: #f0ece6; padding: 2px 6px; border-radius: 3px; color: #c0392b; }
  hr { border: none; border-top: 1px solid var(--border-subtle); margin: 32px 0; }
  a { color: var(--accent-blue); text-decoration: none; }
  a:hover { text-decoration: underline; }

  /* ── Tables ── */
  table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13.5px; }
  th { background: #1a1a1a; color: #ffffff; padding: 10px 14px; text-align: left; font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 0.3px; border-bottom: 2px solid var(--border-red); }
  td { padding: 9px 14px; border-bottom: 1px solid var(--border-subtle); vertical-align: top; line-height: 1.6; color: #000; }
  tr:hover td { background: rgba(0,0,0,0.02); }

  /* ── Callout boxes ── */
  .cb { padding: 14px 18px; border-radius: 4px; margin: 18px 0; border-left: 4px solid; font-size: 14px; }
  .cb.red { background: #fef2f2; border-color: var(--border-red); }
  .cb.blue { background: #eff6ff; border-color: var(--accent-blue); }
  .cb.yellow { background: #fefce8; border-color: var(--accent-yellow); }
  .cb .cb-t { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px; }
  .cb.red .cb-t { color: var(--border-red); }
  .cb.blue .cb-t { color: var(--accent-blue); }
  .cb.yellow .cb-t { color: #92700c; }

  /* ── Code blocks — CSP style ── */
  .cbl { background: #0A0A0A; border-radius: 6px; margin: 16px 0; overflow-x: hidden; border: none; border-left: 3px solid #FF9D00; }
  .cbl .ch { padding: 7px 12px; background: #1A1A1A; border-bottom: none; font-size: 10px; font-weight: 600; color: #666; text-transform: uppercase; letter-spacing: 0.5px; }
  .cbl pre { padding: 6px 0; color: #D4D4D4; font-family: Consolas, 'Courier New', monospace; font-size: 12.5px; font-weight: 700; line-height: 1.35; overflow-x: hidden; counter-reset: ln; white-space: pre-wrap; word-wrap: break-word; }
  .cbl .l { display: block; padding: 0px 10px 0px 2.4em; position: relative; min-height: 1.1em; }
  .cbl .l::before { counter-increment: ln; content: counter(ln); position: absolute; left: 0; width: 1.8em; text-align: right; color: #444; font-size: 10px; line-height: inherit; }
  .cbl .l:hover { background: rgba(255,255,255,0.03); }
  .cbl .l.hl { padding: 1px 10px 1px 2.4em; background: rgba(255,157,0,0.1); border-left: 3px solid #FF9D00; margin: 0; }

  /* Syntax colors — CSP palette */
  .kw { color: #FF9D00; }
  .fn { color: #FFEE80; }
  .s { color: #3AD900; }
  .c { color: #FFD700; font-style: italic; }
  .n { color: #FF628C; }
  .v { color: #D4D4D4; }
  .d { color: #D4D4D4; }

  /* ── Code annotation labels ── */
  .lbl { float: right; font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; padding: 2px 8px; border-radius: 3px; margin-left: 12px; font-family: 'Open Sans', sans-serif; font-style: normal; }
  .lbl-req { background: rgba(192,57,43,0.1); color: #c0392b; }
  .lbl-opt { background: rgba(0,184,148,0.1); color: #00896a; }
  .lbl-ret { background: rgba(108,92,231,0.1); color: #6c5ce7; }
  .lbl-ctx { background: rgba(9,132,227,0.1); color: #0984e3; }
  .lbl-dbi { background: rgba(212,160,23,0.1); color: #92700c; }
  .lbl-log { background: rgba(0,131,143,0.1); color: #00838f; }

  /* ── Labels inside code blocks — CSP style ── */
  .cbl .lbl { font-style: normal; font-size: 8px; padding: 1px 5px; border-radius: 2px; font-weight: 700; letter-spacing: 0.3px; margin-left: 6px; white-space: nowrap; font-family: 'Open Sans', sans-serif; vertical-align: middle; }
  .cbl .lbl-req { background: #c0392b; color: #fff; }
  .cbl .lbl-opt { background: #c0392b; color: #fff; }
  .cbl .lbl-ret { background: #c0392b; color: #fff; }
  .cbl .lbl-ctx { background: #c0392b; color: #fff; }
  .cbl .lbl-dbi { background: #c0392b; color: #fff; }
  .cbl .lbl-log { background: #c0392b; color: #fff; }

  /* ── Footer ── */
  .footer { margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--border-subtle); font-size: 12px; color: var(--text-secondary); text-align: center; }
</style>
</head>
<body>
<div class="container">

<div class="tags-row">
  <span class="tag hl">Fast Formula</span>
  <span class="tag hl">Benefits</span>
  <span class="tag">Post Election Edit</span>
  <span class="tag">CHANGE_CONTEXTS</span>
  <span class="tag">BEN_PEN Array DBI</span>
  <span class="tag">ESS_LOG_WRITE</span>
  <span class="tag">Waiting Period</span>
</div>

<h1>Oracle Fast Formula: Post Election Edit — Cross-Plan Enrollment Validation with Waiting Period Logic</h1>
<p class="subtitle">Blocking Child Life enrollment when Employee Life isn't elected, using BEN_PEN array DBIs, CHANGE_CONTEXTS with a calculated future effective date, and ESS_LOG_WRITE tracing</p>
<p class="meta">April 2026 · 14 min read · Oracle HCM Cloud</p>

<div class="author-card">
  <img src="data:image/jpeg;base64,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" style="width:46px;height:46px;border-radius:50%;object-fit:cover;flex-shrink:0;" alt="Abhishek Mohanty">
  <div>
    <div class="name">Abhishek Mohanty</div>
    <div class="role">Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant</div>
  </div>
</div>


<div style="margin:28px 0;border:2px solid var(--border-red);border-radius:8px;overflow:hidden;">
  <div style="background:#1a1a1a;padding:12px 18px;font-size:12px;font-weight:700;color:#fff;letter-spacing:1px;text-transform:uppercase;">This Formula at a Glance</div>
  <table style="margin:0;border:none;">
    <tr>
      <td style="width:25%;padding:16px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);">
        <div style="width:48px;height:48px;border-radius:50%;background:#0984e3;color:#fff;font-weight:700;font-size:20px;line-height:48px;margin:0 auto 10px;">1</div>
        <div style="font-size:13px;font-weight:700;color:var(--text-heading);margin-bottom:4px;">Calculate Future Date</div>
        <div style="font-size:12px;color:var(--text-secondary);">Life event + waiting period → coverage start date</div>
      </td>
      <td style="width:25%;padding:16px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);">
        <div style="width:48px;height:48px;border-radius:50%;background:#c0392b;color:#fff;font-weight:700;font-size:20px;line-height:48px;margin:0 auto 10px;">2</div>
        <div style="font-size:13px;font-weight:700;color:var(--text-heading);margin-bottom:4px;">Read Enrollment at Future</div>
        <div style="font-size:12px;color:var(--text-secondary);">CHANGE_CONTEXTS → loop BEN_PEN → set flags</div>
      </td>
      <td style="width:25%;padding:16px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);">
        <div style="width:44px;height:44px;border-radius:50%;background:#00b894;color:#fff;font-weight:700;font-size:18px;line-height:44px;margin:0 auto 8px;">3</div>
        <div style="font-size:12px;font-weight:700;color:var(--text-heading);margin-bottom:4px;">Validate Plan Presence</div>
        <div style="font-size:11px;color:var(--text-secondary);">Child=Y + Employee=N → BLOCK</div>
      </td>
      <td style="width:25%;padding:16px;text-align:center;border-bottom:none;">
        <div style="width:44px;height:44px;border-radius:50%;background:#e67e22;color:#fff;font-weight:700;font-size:18px;line-height:44px;margin:0 auto 8px;">4</div>
        <div style="font-size:12px;font-weight:700;color:var(--text-heading);margin-bottom:4px;">Validate Amounts</div>
        <div style="font-size:11px;color:var(--text-secondary);">Child $ > Employee $ → BLOCK</div>
      </td>
    </tr>
  </table>
</div>


<div style="margin:20px 0 28px;padding:18px 22px;background:#fef2f2;border:2px solid #c0392b;border-radius:8px;text-align:center;">
  <div style="font-size:11px;font-weight:700;color:#c0392b;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">The Business Rule</div>
  <div style="font-size:17px;color:#1a1a1a;line-height:1.5;">
    <span style="display:inline-block;padding:4px 12px;background:#c0392b;color:#fff;border-radius:4px;font-weight:700;font-size:14px;">Child Life</span>
    <span style="font-size:20px;color:#c0392b;font-weight:700;margin:0 8px;">requires</span>
    <span style="display:inline-block;padding:4px 12px;background:#0984e3;color:#fff;border-radius:4px;font-weight:700;font-size:14px;">Employee Life</span>
  </div>
  <div style="font-size:13px;color:#666;margin-top:8px;">No employee coverage → no child coverage. Standard US group life rule.</div>
  <div style="font-size:15px;color:#1a1a1a;line-height:1.5;margin-top:12px;padding-top:12px;border-top:1px solid rgba(192,57,43,0.2);">
    <span style="display:inline-block;padding:4px 12px;background:#c0392b;color:#fff;border-radius:4px;font-weight:700;font-size:14px;">Child Life $</span>
    <span style="font-size:20px;color:#c0392b;font-weight:700;margin:0 8px;">≤</span>
    <span style="display:inline-block;padding:4px 12px;background:#0984e3;color:#fff;border-radius:4px;font-weight:700;font-size:14px;">Employee Life $</span>
  </div>
  <div style="font-size:13px;color:#666;margin-top:6px;">Child coverage amount can't exceed employee coverage. Only a formula can compare dollar amounts.</div>
</div>

<p>
The business rule is straightforward: <strong>an employee can't enroll in Voluntary Child Life insurance unless they also carry Voluntary Employee Life.</strong> The child doesn't get coverage if the employee doesn't have coverage. This is standard across US group life insurance plans.
</p>

<p>
In Oracle Benefits, the employee makes all their elections in a single enrollment window — Medical, Dental, Employee Life, Child Life — and submits everything at once. A <strong>Post Election Edit</strong> formula fires at that point to validate whether the combination of elections is allowed.
</p>

<p>
Here's where it gets tricky. The formula validates elections by reading <code>BEN_PEN_PL_NAME_TN</code> — an array DBI that returns <strong>active enrollment results</strong>, meaning plans where the employee is currently enrolled and coverage is in effect. It does <em>not</em> return the elections the employee is submitting right now. Those elections are still in flight — they haven't been written as enrollment results yet.
</p>

<p>
This creates a timing gap. If the formula checks enrollment at <strong>today's</strong> effective date, it sees the employee's <em>current</em> state — not the state that will exist after the new elections take effect. And that leads to a serious validation hole.
</p>

<p>
Let's look at four employees making elections during the same enrollment window:
</p>

<table>
  <tr><th>Employee</th><th>Current Enrollment (today)</th><th>New Election (submitting now)</th><th>What the formula sees at today's date</th></tr>
  <tr><td><strong>James</strong> (new hire)</td><td>Nothing — he just joined</td><td>Employee Life + Child Life</td><td>Child Life = N, Employee Life = N. <strong>Passes</strong> — but only because neither flag is set. The validation didn't actually check anything meaningful.</td></tr>
  <tr><td><strong>Sarah</strong> (existing employee, Open Enrollment)</td><td>Employee Life only</td><td>Adding Child Life</td><td>Child Life = N, Employee Life = Y. <strong>Passes</strong> — happens to be correct, but the formula is reading Sarah's old enrollment, not her new election.</td></tr>
  <tr><td><strong>Mike</strong> (existing employee, dropping coverage)</td><td>Employee Life + Child Life</td><td>Dropping Employee Life, keeping Child Life</td><td>Child Life = Y, Employee Life = Y. <strong>Passes — and this is wrong.</strong> Mike is dropping Employee Life, but the formula doesn't know that because <code>BEN_PEN</code> still reflects his current enrollment.</td></tr>
  <tr><td><strong>Lisa</strong> (existing employee, changing amounts)</td><td>Employee Life $200K + Child Life $50K</td><td>Reducing Employee Life to $100K, increasing Child Life to $150K</td><td>Child Life $50K, Employee Life $200K. <strong>Passes — and this is wrong.</strong> At the future date, Child Life ($150K) will exceed Employee Life ($100K). But today's data still shows the old amounts.</td></tr>
</table>

<p>
<strong>Mike and Lisa are the scenarios this formula exists to catch.</strong> Mike has Child Life without Employee Life — a plan-level violation. Lisa has both plans but her Child Life amount exceeds Employee Life — an amount-level violation. When the formula reads <code>BEN_PEN_PL_NAME_TN</code> at today's effective date, it sees both plans as active. Why? Because Mike's decision to drop Employee Life doesn't take effect today. It takes effect on the <em>future coverage start date</em> — the date after the waiting period ends.
</p>

<p>
That's the critical distinction. <code>BEN_PEN</code> returns enrollment results <strong>as of the effective date you give it</strong>:
</p>

<table>
  <tr><th>Effective Date</th><th>What BEN_PEN Returns for Mike</th><th>Why</th></tr>
  <tr><td><strong>Today</strong> (election day)</td><td>Employee Life = active, Child Life = active</td><td>Mike's current enrollments are still in force. His drop hasn't taken effect — it won't until the coverage start date.</td></tr>
  <tr><td><strong>Future coverage date</strong> (after waiting period)</td><td>Employee Life = gone, Child Life = active</td><td>Oracle has projected the new elections to this date. The drop is now reflected. Only Child Life remains.</td></tr>
</table>


<div style="margin:24px 0;overflow:hidden;border-radius:8px;border:2px solid var(--border-subtle);">
  <table style="margin:0;">
    <tr>
      <td style="width:50%;padding:20px;background:#fef2f2;border-bottom:none;border-right:2px solid var(--border-subtle);vertical-align:top;">
        <div style="font-size:11px;font-weight:700;color:#c0392b;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">❌ Checking at Today's Date</div>
        <div style="font-size:14px;color:#333;margin-bottom:8px;">BEN_PEN sees:</div>
        <div style="display:inline-block;padding:4px 10px;background:#0984e3;color:#fff;border-radius:3px;font-size:12px;font-weight:600;margin:2px;">Employee Life ✓</div>
        <div style="display:inline-block;padding:4px 10px;background:#c0392b;color:#fff;border-radius:3px;font-size:12px;font-weight:600;margin:2px;">Child Life ✓</div>
        <div style="font-size:13px;color:#c0392b;margin-top:10px;font-weight:700;">→ Both active → PASSES (wrong!)</div>
      </td>
      <td style="width:50%;padding:20px;background:#f0fdf4;border-bottom:none;vertical-align:top;">
        <div style="font-size:11px;font-weight:700;color:#00896a;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">✓ Checking at Future Coverage Date</div>
        <div style="font-size:14px;color:#333;margin-bottom:8px;">BEN_PEN sees:</div>
        <div style="display:inline-block;padding:4px 10px;background:#ddd;color:#888;border-radius:3px;font-size:12px;font-weight:600;margin:2px;text-decoration:line-through;">Employee Life</div>
        <div style="display:inline-block;padding:4px 10px;background:#c0392b;color:#fff;border-radius:3px;font-size:12px;font-weight:600;margin:2px;">Child Life ✓</div>
        <div style="font-size:13px;color:#00896a;margin-top:10px;font-weight:700;">→ Child without Employee → BLOCKED ✓</div>
      </td>
    </tr>
  </table>
</div>

<p>
<strong>The fix:</strong> instead of checking enrollment at today's date, the formula first calculates the future coverage effective date — factoring in the employer's waiting period — and then uses <code>CHANGE_CONTEXTS(EFFECTIVE_DATE = l_cvg_eff_date)</code> to shift the lookup forward to that date. Now <code>BEN_PEN</code> returns the second row from the table above: Employee Life is gone, Child Life is the only active plan. The formula sees Child Life = Y, Employee Life = N → <strong>blocked</strong>. Exactly as it should be.
</p>

<p>
That's why this formula has a waiting period calculation and a <code>CHANGE_CONTEXTS</code> shift. Without them, the formula validates against stale enrollment data and lets Mike through — missing the exact scenario it was built to prevent.
</p>


<h2>What This Formula Does</h2>

<p>
This is a <strong>Post Election Edit</strong> formula. Oracle calls it after the employee submits their benefit elections during enrollment. The formula validates the elections and either allows them to proceed or blocks them with an error message.
</p>

<table>
  <tr><th>Return Variable</th><th>Type</th><th>What It Means</th></tr>
  <tr><td><code>SUCCESSFUL</code></td><td>Character</td><td><code>'Y'</code> = elections are valid, proceed. <code>'N'</code> = elections are invalid, block.</td></tr>
  <tr><td><code>ERROR_MESSAGE</code></td><td>Character</td><td>Message shown to the employee when blocked. Only matters when <code>SUCCESSFUL = 'N'</code>.</td></tr>
</table>

<p>
The formula does three things in sequence:
</p>

<table>
  <tr><th>Step</th><th>What It Does</th><th>Why It's Needed</th></tr>
  <tr><td><strong>1. Calculate coverage effective date</strong></td><td>Read the life event date. Apply waiting period logic. Compute the future date when coverage will actually start.</td><td>Elections are made today but coverage starts later. Validation must check enrollment state at the future date, not today.</td></tr>
  <tr><td><strong>2. Read enrollment results at future date</strong></td><td>Use <code>CHANGE_CONTEXTS</code> to shift effective date forward. Loop through <code>BEN_PEN_PL_NAME_TN</code> array DBI to check which plans the employee is enrolled in.</td><td>The array DBI returns all plan enrollments for this person. The formula needs to find two specific plans in this list.</td></tr>
  <tr><td><strong>3. Validate the combination</strong></td><td>If Child Life = Y and Employee Life = N → block. Every other combination → allow.</td><td>The only invalid combination is having child coverage without employee coverage.</td></tr>
</table>

<p>
The first thing you'll notice: <strong>Step 1 is the complex part.</strong> Steps 2 and 3 are the standard array loop and IF/ELSE that you've seen in previous posts. Step 1 is unique to this formula — it calculates a waiting period and builds a future effective date before any enrollment data is read.
</p>


<h2>The Waiting Period — When Does Coverage Actually Start?</h2>

<p>
Life insurance coverage doesn't always start on the life event date. Many employers require a waiting period — employees must wait before coverage kicks in. This isn't a US federal requirement. There's no law mandating a waiting period for group life insurance. Some employers start coverage on day 1, others use a 30-day or 60-day wait. In this scenario, the employer uses a two-month wait with coverage starting on the 1st of a month.
</p>

<p>
The formula needs to know this exact coverage start date because that's the date it will use with <code>CHANGE_CONTEXTS</code> to check enrollment. Different employer, different waiting period, different date calculation — but the same formula structure.
</p>

<p>
<strong>James</strong> was hired on <strong>March 15</strong>. He didn't join on the 1st of the month, so the waiting period applies. March is a partial month — doesn't count. April is the first full month — that's month one of the wait. May is month two. Coverage starts on the <strong>1st of June</strong>.
</p>

<p>
<strong>Sarah's</strong> Open Enrollment event date is <strong>January 1</strong>. She's on the 1st of the month — no extended wait needed. Coverage starts on the <strong>1st of February</strong>, the very next month.
</p>




<div style="margin:24px 0 12px;border:2px solid var(--border-subtle);border-radius:8px;overflow:hidden;">
  <div style="background:#1a1a1a;padding:10px 16px;font-size:12px;font-weight:700;color:#fff;letter-spacing:1px;text-transform:uppercase;">James (New Hire) — Event on March 15</div>
  <table style="margin:0;">
    <tr>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);background:#fef2f2;">
        <div style="font-size:11px;font-weight:700;color:#c0392b;letter-spacing:0.5px;">MAR 15</div>
        <div style="font-size:12px;color:#333;margin-top:4px;">Event date</div>
        <div style="font-size:11px;color:#888;">Partial month</div>
      </td>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);">
        <div style="font-size:11px;font-weight:700;color:#666;">APR</div>
        <div style="font-size:12px;color:#333;margin-top:4px;">Wait month 1</div>
        <div style="font-size:16px;color:#ccc;">⏳</div>
      </td>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);">
        <div style="font-size:11px;font-weight:700;color:#666;">MAY</div>
        <div style="font-size:12px;color:#333;margin-top:4px;">Wait month 2</div>
        <div style="font-size:16px;color:#ccc;">⏳</div>
      </td>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;background:#f0fdf4;">
        <div style="font-size:11px;font-weight:700;color:#00896a;">JUN 1</div>
        <div style="font-size:12px;color:#333;margin-top:4px;font-weight:700;">Coverage starts</div>
        <div style="font-size:11px;color:#00896a;font-weight:600;">Formula checks here</div>
      </td>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;background:#f0fdf4;">
        <div style="font-size:24px;">✅</div>
        <div style="font-size:11px;color:#00896a;font-weight:700;margin-top:2px;">PASSES</div>
        <div style="font-size:10px;color:#888;">Both plans elected</div>
      </td>
    </tr>
  </table>
</div>


<div style="margin:12px 0;border:2px solid var(--border-subtle);border-radius:8px;overflow:hidden;">
  <div style="background:#1a1a1a;padding:10px 16px;font-size:12px;font-weight:700;color:#fff;letter-spacing:1px;text-transform:uppercase;">Sarah (Open Enrollment) — Event on January 1</div>
  <table style="margin:0;">
    <tr>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);background:#eff6ff;">
        <div style="font-size:11px;font-weight:700;color:#0984e3;letter-spacing:0.5px;">JAN 1</div>
        <div style="font-size:12px;color:#333;margin-top:4px;">Event date</div>
        <div style="font-size:11px;color:#0984e3;font-weight:600;">On the 1st!</div>
      </td>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);background:#f0fdf4;">
        <div style="font-size:11px;font-weight:700;color:#00896a;">FEB 1</div>
        <div style="font-size:12px;color:#333;margin-top:4px;font-weight:700;">Coverage starts</div>
        <div style="font-size:11px;color:#00896a;font-weight:600;">Formula checks here</div>
      </td>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;background:#f0fdf4;" colspan="2">
        <div style="font-size:12px;color:#888;font-style:italic;">No extended wait — event was on the 1st</div>
      </td>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;background:#f0fdf4;">
        <div style="font-size:24px;">✅</div>
        <div style="font-size:11px;color:#00896a;font-weight:700;margin-top:2px;">PASSES</div>
        <div style="font-size:10px;color:#888;">Has Employee Life</div>
      </td>
    </tr>
  </table>
</div>


<div style="margin:12px 0 24px;border:2px solid #c0392b;border-radius:8px;overflow:hidden;">
  <div style="background:#c0392b;padding:10px 16px;font-size:12px;font-weight:700;color:#fff;letter-spacing:1px;text-transform:uppercase;">⚠ Mike (Dropping Coverage) — Event on April 10</div>
  <table style="margin:0;">
    <tr>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);background:#fef2f2;">
        <div style="font-size:11px;font-weight:700;color:#c0392b;letter-spacing:0.5px;">APR 10</div>
        <div style="font-size:12px;color:#333;margin-top:4px;">Event date</div>
        <div style="font-size:11px;color:#888;">Partial month</div>
      </td>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);">
        <div style="font-size:11px;font-weight:700;color:#666;">MAY</div>
        <div style="font-size:12px;color:#333;margin-top:4px;">Wait month 1</div>
        <div style="font-size:16px;color:#ccc;">⏳</div>
      </td>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);">
        <div style="font-size:11px;font-weight:700;color:#666;">JUN</div>
        <div style="font-size:12px;color:#333;margin-top:4px;">Wait month 2</div>
        <div style="font-size:16px;color:#ccc;">⏳</div>
      </td>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);background:#f0fdf4;">
        <div style="font-size:11px;font-weight:700;color:#00896a;">JUL 1</div>
        <div style="font-size:12px;color:#333;margin-top:4px;font-weight:700;">Coverage starts</div>
        <div style="font-size:11px;color:#00896a;font-weight:600;">Formula checks here</div>
      </td>
      <td style="width:20%;padding:14px;text-align:center;border-bottom:none;background:#fef2f2;">
        <div style="font-size:24px;">🚫</div>
        <div style="font-size:11px;color:#c0392b;font-weight:700;margin-top:2px;">BLOCKED</div>
        <div style="font-size:10px;color:#c0392b;">Child Life without<br>Employee Life</div>
      </td>
    </tr>
  </table>
</div>


<div style="margin:12px 0 24px;border:2px solid #e67e22;border-radius:8px;overflow:hidden;">
  <div style="background:#e67e22;padding:10px 16px;font-size:12px;font-weight:700;color:#fff;letter-spacing:1px;text-transform:uppercase;">⚠ Lisa (Changing Amounts) — Event on March 20</div>
  <table style="margin:0;">
    <tr>
      <td style="width:16%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);background:#fef9f0;">
        <div style="font-size:11px;font-weight:700;color:#e67e22;letter-spacing:0.5px;">MAR 20</div>
        <div style="font-size:12px;color:#333;margin-top:4px;">Event date</div>
      </td>
      <td style="width:12%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);">
        <div style="font-size:11px;font-weight:700;color:#666;">APR</div>
        <div style="font-size:16px;color:#ccc;">⏳</div>
      </td>
      <td style="width:12%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);">
        <div style="font-size:11px;font-weight:700;color:#666;">MAY</div>
        <div style="font-size:16px;color:#ccc;">⏳</div>
      </td>
      <td style="width:16%;padding:14px;text-align:center;border-bottom:none;border-right:1px solid var(--border-subtle);background:#f0fdf4;">
        <div style="font-size:11px;font-weight:700;color:#00896a;">JUN 1</div>
        <div style="font-size:12px;color:#333;font-weight:700;">Checks here</div>
      </td>
      <td style="width:44%;padding:14px;text-align:center;border-bottom:none;background:#fef2f2;">
        <div style="font-size:13px;font-weight:700;color:#e67e22;margin-bottom:6px;">🚫 BLOCKED — Amount Violation</div>
        <div style="display:inline-block;padding:4px 10px;background:#c0392b;color:#fff;border-radius:4px;font-size:11px;font-weight:700;margin:2px;">Child $150K</div>
        <div style="display:inline-block;font-size:14px;color:#c0392b;font-weight:700;margin:0 4px;">></div>
        <div style="display:inline-block;padding:4px 10px;background:#0984e3;color:#fff;border-radius:4px;font-size:11px;font-weight:700;margin:2px;">Employee $100K</div>
      </td>
    </tr>
  </table>
</div>

<p>
<strong>Mike's</strong> divorce was on <strong>April 10</strong>. Same as James — he didn't join on the 1st. April is partial, May is month one, June is month two. Coverage starts on the <strong>1st of July</strong>. This is the date the formula will use to check whether Mike still has Employee Life.
</p>

<p>
<strong>Lisa's</strong> qualifying event was on <strong>March 20</strong>. She currently has Employee Life at $200K and Child Life at $50K. She's reducing Employee Life to $100K and increasing Child Life to $150K. After the waiting period, coverage starts on the <strong>1st of June</strong>. At that date, the formula reads the new amounts: Child Life $150K, Employee Life $100K. <strong>$150K > $100K — blocked.</strong> This is the scenario that only the formula can catch. Plan Dependency sees both plans are enrolled and allows it. The formula sees the amounts don't comply.
</p>

<table>
  <tr><th>Employee</th><th>Event Date</th><th>On the 1st?</th><th>Coverage Starts</th><th>Formula Checks BEN_PEN At</th></tr>
  <tr><td><strong>James</strong></td><td>15-Mar-2025</td><td>No</td><td><strong>01-Jun-2025</strong></td><td>01-Jun-2025</td></tr>
  <tr><td><strong>Sarah</strong></td><td>01-Jan-2025</td><td>Yes</td><td><strong>01-Feb-2025</strong></td><td>01-Feb-2025</td></tr>
  <tr><td><strong>Mike</strong></td><td>10-Apr-2025</td><td>No</td><td><strong>01-Jul-2025</strong></td><td>01-Jul-2025</td></tr>
  <tr style="background:#fef9f0;"><td><strong>Lisa</strong></td><td>20-Mar-2025</td><td>No</td><td><strong>01-Jun-2025</strong></td><td>01-Jun-2025</td></tr>
</table>

<p>
That last column is the whole point. The coverage start date becomes the <code>EFFECTIVE_DATE</code> for <code>CHANGE_CONTEXTS</code>. The formula reads <code>BEN_PEN</code> at that date — not today — to see the projected enrollment state.
</p>

<div class="cb yellow">
  <div class="cb-t">How the Formula Calculates This Date</div>
  <p>Fast Formula can't set the day of a date to "01" directly — there's no such function. So it uses a workaround: <code>ADD_MONTHS(date, 2)</code> moves forward 2 months → <code>LAST_DAY()</code> jumps to the end of that month → <code>ADD_DAYS(, 1)</code> lands on the 1st of the next month. For Mike: 10-Apr + 2 months = 10-Jun → last day of Jun = 30-Jun → +1 = <strong>01-Jul</strong>. You'll see this <code>LAST_DAY + ADD_DAYS(1)</code> trick throughout Oracle Benefits formulas wherever a "1st of the month" date is needed.</p>
</div>

<div class="cb blue">
  <div class="cb-t">The Role of the Waiting Period in This Formula</div>
  <p>The waiting period here is <strong>not controlling when coverage starts</strong> — Oracle's built-in waiting period configuration on the plan enrollment page handles that. You can set "30 days" or "first of the month following 60 days" in plan setup without any formula.</p>
  <p>In this formula, the waiting period answers one question: <strong>"As of what date should I check whether this employee still has Employee Life?"</strong> Without this date, the formula falls back to today's effective date — and that's exactly how Mike's scenario slips through.</p>
</div>


<h2>Why CHANGE_CONTEXTS Is Needed Here</h2>

<p>
I covered the "why" in the intro with Mike's scenario. Here's the technical "how."
</p>

<p>
The formula uses <code>CHANGE_CONTEXTS(EFFECTIVE_DATE = l_cvg_eff_date)</code> to shift the context forward to the coverage effective date. Every DBI read inside this block returns values <em>as of that future date</em> — including the projected enrollment results after the current elections are finalized.
</p>

<div class="cbl">
  <div class="ch">The Context Shift — Today vs Future</div>
  <pre>
<span class="l"><span class="c">/* Without CHANGE_CONTEXTS — reads enrollment as of TODAY     */</span></span>
<span class="l"><span class="c">/* Result: might not see the new elections yet                */</span></span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l"><span class="c">/* With CHANGE_CONTEXTS — reads enrollment as of JUNE 1       */</span></span>
<span class="l"><span class="c">/* Result: sees the new elections the employee just submitted  */</span></span>
<span class="l hl"><span class="fn">CHANGE_CONTEXTS</span>(EFFECTIVE_DATE = l_cvg_eff_date)<span class="lbl lbl-ctx">CONTEXT</span></span>
<span class="l">(</span>
<span class="l">    <span class="c">/* Now BEN_PEN_PL_NAME_TN returns enrollments as of Jun 1 */</span></span>
<span class="l">    <span class="c">/* This includes the elections being made right now       */</span></span>
<span class="l">)</span>
</pre>
</div>

<p>
Without <code>CHANGE_CONTEXTS</code>, the formula validates against stale enrollment data — the Mike scenario from the intro.
</p>


<h2>The Array DBI Loop — What BEN_PEN Gives You</h2>

<p>
<code>BEN_PEN_PL_NAME_TN</code> and <code>BEN_PEN_OPT_NAME_TN</code> are <strong>array DBIs</strong>. Each index <code>[i]</code> represents a different plan enrollment for this person. The loop walks through all of them looking for two specific plans.
</p>

<p>
Here's what the array might contain for an employee enrolled in three plans:
</p>

<table>
  <tr><th>Index [i]</th><th>BEN_PEN_PL_NAME_TN[i]</th><th>BEN_PEN_OPT_NAME_TN[i]</th></tr>
  <tr><td>1</td><td>Medical PPO</td><td>Employee + Family</td></tr>
  <tr><td>2</td><td>Voluntary Employee Life and AD&D</td><td>10,000 - 500,000</td></tr>
  <tr><td>3</td><td>Voluntary Child Life and AD&D</td><td>1,000 - 10,000</td></tr>
  <tr><td>4</td><td>Dental</td><td>Employee Only</td></tr>
</table>

<p>
The formula doesn't know in advance how many enrollments exist or what order they're in. It loops from <code>i = 1</code> until <code>BEN_PEN_PL_NAME_TN.exists(i)</code> returns false. At each index, it checks the plan name and option name. If it finds a match, it sets a flag.
</p>

<table>
  <tr><th>Flag</th><th>Set to 'Y' When</th><th>Meaning</th></tr>
  <tr><td><code>l_child_flag</code></td><td>Plan = <code>'Voluntary Child Life and AD&D'</code> AND Option = <code>'1,000 - 10,000'</code></td><td>Employee is enrolling in Child Life</td></tr>
  <tr><td><code>l_emp_flag</code></td><td>Plan = <code>'Voluntary Employee Life and AD&D'</code> AND Option = <code>'10,000 - 500,000'</code></td><td>Employee is enrolled in Employee Life</td></tr>
</table>

<div class="cb yellow">
  <div class="cb-t">Watch Out — Hardcoded Option Names</div>
  <p>The formula checks for exact option names: <code>'1,000 - 10,000'</code> and <code>'10,000 - 500,000'</code>. If the plan configuration changes — say the option range is updated to <code>'10,000 - 600,000'</code> — the formula won't match it. It will treat the employee as not enrolled in Employee Life and block Child Life elections incorrectly. The option names in the formula must exactly match the option names configured in Plan Configuration. A safer approach would be to check only the plan name and ignore the option name — unless the business specifically requires option-level validation.</p>
</div>


<h2>The Validation Matrix</h2>


<div style="margin:24px 0;">

  
  <div style="margin-bottom:8px;padding:16px 20px;background:#f0fdf4;border-radius:8px;border:1px solid rgba(0,137,106,0.2);">
    <div style="font-size:11px;font-weight:700;color:#00896a;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;">✓ Valid Combinations — PASS</div>
    <table style="margin:0;">
      <tr>
        <td style="width:30%;padding:10px 14px;border-bottom:1px solid rgba(0,137,106,0.15);font-size:13px;">
          <span style="display:inline-block;padding:2px 8px;background:#e0e0e0;color:#666;border-radius:3px;font-size:11px;font-weight:700;">Child N</span>
          <span style="display:inline-block;padding:2px 8px;background:#e0e0e0;color:#666;border-radius:3px;font-size:11px;font-weight:700;">Emp N</span>
        </td>
        <td style="padding:10px 14px;border-bottom:1px solid rgba(0,137,106,0.15);font-size:13px;color:#333;">Waiving both plans — nothing to validate</td>
      </tr>
      <tr>
        <td style="width:30%;padding:10px 14px;border-bottom:1px solid rgba(0,137,106,0.15);font-size:13px;">
          <span style="display:inline-block;padding:2px 8px;background:#e0e0e0;color:#666;border-radius:3px;font-size:11px;font-weight:700;">Child N</span>
          <span style="display:inline-block;padding:2px 8px;background:#0984e3;color:#fff;border-radius:3px;font-size:11px;font-weight:700;">Emp Y</span>
        </td>
        <td style="padding:10px 14px;border-bottom:1px solid rgba(0,137,106,0.15);font-size:13px;color:#333;">Employee Life only — no dependency issue</td>
      </tr>
      <tr>
        <td style="width:30%;padding:10px 14px;font-size:13px;">
          <span style="display:inline-block;padding:2px 8px;background:#c0392b;color:#fff;border-radius:3px;font-size:11px;font-weight:700;">Child Y $50K</span>
          <span style="display:inline-block;padding:2px 8px;background:#0984e3;color:#fff;border-radius:3px;font-size:11px;font-weight:700;">Emp Y $200K</span>
        </td>
        <td style="padding:10px 14px;font-size:13px;color:#333;">Both enrolled, <strong>$50K ≤ $200K</strong> — amounts OK</td>
      </tr>
    </table>
  </div>

  
  <div style="margin-bottom:8px;padding:16px 20px;background:#fef2f2;border-radius:8px;border:2px solid #c0392b;">
    <table style="margin:0;">
      <tr>
        <td style="width:30%;padding:10px 14px;border-bottom:none;vertical-align:middle;">
          <span style="display:inline-block;padding:2px 8px;background:#c0392b;color:#fff;border-radius:3px;font-size:11px;font-weight:700;">Child Y</span>
          <span style="display:inline-block;padding:2px 8px;background:#e0e0e0;color:#666;border-radius:3px;font-size:11px;font-weight:700;text-decoration:line-through;">Emp N</span>
        </td>
        <td style="padding:10px 14px;border-bottom:none;vertical-align:middle;">
          <div style="font-size:14px;font-weight:700;color:#c0392b;">🚫 BLOCKED — Step 3 (Mike)</div>
          <div style="font-size:12px;color:#666;margin-top:4px;">Child Life without Employee Life. Plan Dependency also catches this at the UI.</div>
        </td>
      </tr>
    </table>
  </div>

  
  <div style="padding:16px 20px;background:#fef9f0;border-radius:8px;border:2px solid #e67e22;">
    <table style="margin:0;">
      <tr>
        <td style="width:30%;padding:10px 14px;border-bottom:none;vertical-align:middle;">
          <span style="display:inline-block;padding:2px 8px;background:#c0392b;color:#fff;border-radius:3px;font-size:11px;font-weight:700;">Child Y $150K</span>
          <span style="display:inline-block;padding:2px 8px;background:#0984e3;color:#fff;border-radius:3px;font-size:11px;font-weight:700;">Emp Y $100K</span>
        </td>
        <td style="padding:10px 14px;border-bottom:none;vertical-align:middle;">
          <div style="font-size:14px;font-weight:700;color:#e67e22;">🚫 BLOCKED — Step 4 (Lisa)</div>
          <div style="font-size:12px;color:#666;margin-top:4px;">Both enrolled but <strong>$150K > $100K</strong>. Child coverage exceeds employee coverage. <em>Only the formula catches this — no configuration can compare amounts.</em></div>
        </td>
      </tr>
    </table>
  </div>

</div>

<p>
After the loop, the formula has two flags and two amounts. There are five possible combinations. Two are invalid — one caught by plan presence (Step 3), one by amount comparison (Step 4).
</p>

<table>
  <tr><th>l_child_flag (Child Life)</th><th>l_emp_flag (Employee Life)</th><th>SUCCESSFUL</th><th>Why</th></tr>
  <tr><td>N</td><td>N</td><td>Y</td><td>Waiving both — valid</td></tr>
  <tr><td>N</td><td>Y</td><td>Y</td><td>Employee Life only — valid</td></tr>
  <tr><td>Y</td><td>Y</td><td>Y</td><td>Both enrolled — valid</td></tr>
  <tr><td><strong>Y</strong></td><td><strong>N</strong></td><td><strong>N</strong></td><td><strong>Child Life without Employee Life — blocked</strong></td></tr>
</table>

<p>
The formula only returns <code>SUCCESSFUL = 'N'</code> for the fourth combination. In all other cases, <code>SUCCESSFUL</code> stays at its initial value of <code>'Y'</code> and the enrollment proceeds.
</p>


<h2>The Complete Formula</h2>

<p>
Here's the full Post Election Edit formula. I'll break it into blocks below.
</p>

<div class="cbl">
  <div class="ch">XX_VOL_LIFE_CROSS_PLAN_EDIT — Post Election Edit</div>
  <pre>
<span class="l"><span class="c">/*************************************************************</span></span>
<span class="l"><span class="c">FORMULA NAME : XX_VOL_LIFE_CROSS_PLAN_EDIT</span></span>
<span class="l"><span class="c">FORMULA TYPE : Post Election Edit</span></span>
<span class="l"><span class="c">DESCRIPTION  : Block Child Life enrollment if Employee Life</span></span>
<span class="l"><span class="c">               is not elected. Check at coverage effective</span></span>
<span class="l"><span class="c">               date after waiting period.</span></span>
<span class="l"><span class="c">*************************************************************/</span></span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l"><span class="c">/* ── Defaults ── */</span></span>
<span class="l"><span class="kw">DEFAULT_DATA_VALUE FOR</span> <span class="d">BEN_PEN_PL_NAME_TN</span> <span class="kw">IS</span> <span class="s">'My-Default'</span><span class="lbl lbl-dbi">ARRAY DBI</span></span>
<span class="l"><span class="kw">DEFAULT_DATA_VALUE FOR</span> <span class="d">BEN_PEN_OPT_NAME_TN</span> <span class="kw">IS</span> <span class="s">'My-Default'</span><span class="lbl lbl-dbi">ARRAY DBI</span></span>
<span class="l"><span class="kw">DEFAULT_DATA_VALUE FOR</span> <span class="d">BEN_PEN_BNFT_AMT_NN</span> <span class="kw">IS</span> <span class="n">0</span><span class="lbl lbl-dbi">ARRAY DBI</span></span>
<span class="l"><span class="kw">DEFAULT FOR</span> <span class="d">BEN_PIL_LF_EVT_OCRD_DT</span> <span class="kw">IS</span> <span class="s">'1951/01/01 00:00:00'</span> (<span class="kw">DATE</span>)<span class="lbl lbl-dbi">DBI</span></span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l"><span class="c">/* ── Initialize ── */</span></span>
<span class="l hl"><span class="v">SUCCESSFUL</span> = <span class="s">'Y'</span><span class="lbl lbl-req">REQUIRED</span></span>
<span class="l">l_child_flag = <span class="s">'N'</span></span>
<span class="l">l_emp_flag = <span class="s">'N'</span></span>
<span class="l">l_child_amt = <span class="n">0</span>    <span class="c">/* Child Life coverage amount */</span></span>
<span class="l">l_emp_amt = <span class="n">0</span>      <span class="c">/* Employee Life coverage amount */</span></span>
<span class="l hl"><span class="v">ERROR_MESSAGE</span> = <span class="s">' '</span><span class="lbl lbl-opt">OPTIONAL</span></span>
<span class="l">i = <span class="n">1</span></span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l">l_cvg_eff_date = <span class="fn">GET_CONTEXT</span>(EFFECTIVE_DATE,<span class="lbl lbl-ctx">CONTEXT</span></span>
<span class="l">                        <span class="fn">TO_DATE</span>(<span class="s">'1951/01/01 00:00:00'</span>))</span>
<span class="l">l_event_dt = <span class="d">BEN_PIL_LF_EVT_OCRD_DT</span></span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l">l_dbg = <span class="fn">ESS_LOG_WRITE</span>(<span class="s">'l_event_dt is '</span><span class="lbl lbl-log">LOG</span></span>
<span class="l">    || <span class="fn">TO_CHAR</span>(l_event_dt, <span class="s">'MM/DD/YYYY'</span>))</span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l"><span class="c">/* ═════════════════════════════════════════════ */</span></span>
<span class="l"><span class="c">/*  STEP 1: WAITING PERIOD → COVERAGE EFF DATE  */</span><span class="lbl lbl-req">STEP 1</span></span>
<span class="l"><span class="c">/* ═════════════════════════════════════════════ */</span></span>
<span class="l hl"><span class="kw">IF</span> (<span class="fn">TO_CHAR</span>(l_event_dt, <span class="s">'DD'</span>)) = <span class="s">'01'</span> <span class="kw">THEN</span></span>
<span class="l">(</span>
<span class="l">    <span class="c">/* Event on 1st → coverage starts next month */</span></span>
<span class="l">    l_wait_dt = <span class="fn">ADD_MONTHS</span>(l_event_dt, <span class="n">1</span>)</span>
<span class="l">    l_cvg_eff_date = l_wait_dt</span>
<span class="l">)</span>
<span class="l"><span class="kw">ELSE</span></span>
<span class="l">(</span>
<span class="l">    <span class="c">/* Event not on 1st → 1st of month after 2-month wait */</span></span>
<span class="l">    l_wait_dt = <span class="fn">ADD_MONTHS</span>(l_event_dt, <span class="n">2</span>)</span>
<span class="l">    l_wait_end_dt = <span class="fn">LAST_DAY</span>(l_wait_dt)</span>
<span class="l">    l_cvg_eff_date = <span class="fn">ADD_DAYS</span>(l_wait_end_dt, <span class="n">1</span>)</span>
<span class="l">)</span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l">l_dbg = <span class="fn">ESS_LOG_WRITE</span>(<span class="s">'l_cvg_eff_date is '</span><span class="lbl lbl-log">LOG</span></span>
<span class="l">    || <span class="fn">TO_CHAR</span>(l_cvg_eff_date, <span class="s">'MM/DD/YYYY'</span>))</span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l"><span class="c">/* ═════════════════════════════════════════════ */</span></span>
<span class="l"><span class="c">/*  STEP 2: READ ENROLLMENTS AT FUTURE DATE     */</span><span class="lbl lbl-ctx">STEP 2</span></span>
<span class="l"><span class="c">/* ═════════════════════════════════════════════ */</span></span>
<span class="l hl"><span class="fn">CHANGE_CONTEXTS</span>(EFFECTIVE_DATE = l_cvg_eff_date)<span class="lbl lbl-ctx">CONTEXT</span></span>
<span class="l">(</span>
<span class="l hl">    <span class="kw">WHILE</span> <span class="d">BEN_PEN_PL_NAME_TN</span>.exists(i) <span class="kw">LOOP</span></span>
<span class="l">    (</span>
<span class="l">        <span class="kw">IF</span> (<span class="d">BEN_PEN_PL_NAME_TN</span>[i] = <span class="s">'Voluntary Child Life and AD&D'</span></span>
<span class="l">            <span class="kw">AND</span> <span class="d">BEN_PEN_OPT_NAME_TN</span>[i] = <span class="s">'1,000 - 10,000'</span>)</span>
<span class="l">        <span class="kw">THEN</span></span>
<span class="l">        (</span>
<span class="l">            l_child_flag = <span class="s">'Y'</span></span>
<span class="l">            l_child_amt = <span class="d">BEN_PEN_BNFT_AMT_NN</span>[i]<span class="lbl lbl-dbi">AMOUNT</span></span>
<span class="l">        )</span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l">        <span class="kw">IF</span> (<span class="d">BEN_PEN_PL_NAME_TN</span>[i] = <span class="s">'Voluntary Employee Life and AD&D'</span></span>
<span class="l">            <span class="kw">AND</span> <span class="d">BEN_PEN_OPT_NAME_TN</span>[i] = <span class="s">'10,000 - 500,000'</span>)</span>
<span class="l">        <span class="kw">THEN</span></span>
<span class="l">        (</span>
<span class="l">            l_emp_flag = <span class="s">'Y'</span></span>
<span class="l">            l_emp_amt = <span class="d">BEN_PEN_BNFT_AMT_NN</span>[i]<span class="lbl lbl-dbi">AMOUNT</span></span>
<span class="l">        )</span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l">        i = i + <span class="n">1</span></span>
<span class="l">    )</span>
<span class="l">)</span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l">l_dbg = <span class="fn">ESS_LOG_WRITE</span>(<span class="s">'Child Life = '</span> || l_child_flag<span class="lbl lbl-log">LOG</span></span>
<span class="l">    || <span class="s">' Amt = '</span> || <span class="fn">TO_CHAR</span>(l_child_amt))</span>
<span class="l">l_dbg = <span class="fn">ESS_LOG_WRITE</span>(<span class="s">'Employee Life = '</span> || l_emp_flag</span>
<span class="l">    || <span class="s">' Amt = '</span> || <span class="fn">TO_CHAR</span>(l_emp_amt))</span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l"><span class="c">/* ═════════════════════════════════════════════ */</span></span>
<span class="l"><span class="c">/*  STEP 3: VALIDATE CROSS-PLAN COMBINATION     */</span><span class="lbl lbl-opt">STEP 3</span></span>
<span class="l"><span class="c">/* ═════════════════════════════════════════════ */</span></span>
<span class="l hl"><span class="kw">IF</span> (l_child_flag = <span class="s">'Y'</span> <span class="kw">AND</span> l_emp_flag = <span class="s">'N'</span>) <span class="kw">THEN</span></span>
<span class="l">(</span>
<span class="l hl">    <span class="v">SUCCESSFUL</span> = <span class="s">'N'</span></span>
<span class="l">    <span class="v">ERROR_MESSAGE</span> = <span class="s">'Enrollment in Voluntary Child Life'</span></span>
<span class="l">        || <span class="s">' requires an active Voluntary Employee Life'</span></span>
<span class="l">        || <span class="s">' election. Please update your selections'</span></span>
<span class="l">        || <span class="s">' before submitting.'</span></span>
<span class="l">)</span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l"><span class="c">/* ═════════════════════════════════════════════ */</span></span>
<span class="l"><span class="c">/*  STEP 4: VALIDATE COVERAGE AMOUNTS          */</span><span class="lbl lbl-opt">STEP 4</span></span>
<span class="l"><span class="c">/* ═════════════════════════════════════════════ */</span></span>
<span class="l hl"><span class="kw">ELSE IF</span> (l_child_flag = <span class="s">'Y'</span> <span class="kw">AND</span> l_emp_flag = <span class="s">'Y'</span></span>
<span class="l hl">    <span class="kw">AND</span> l_child_amt > l_emp_amt) <span class="kw">THEN</span></span>
<span class="l">(</span>
<span class="l hl">    <span class="v">SUCCESSFUL</span> = <span class="s">'N'</span></span>
<span class="l">    <span class="v">ERROR_MESSAGE</span> = <span class="s">'Child Life coverage ($'</span></span>
<span class="l">        || <span class="fn">TO_CHAR</span>(l_child_amt)</span>
<span class="l">        || <span class="s">') cannot exceed Employee Life ($'</span></span>
<span class="l">        || <span class="fn">TO_CHAR</span>(l_emp_amt)</span>
<span class="l">        || <span class="s">'). Please adjust your elections.'</span></span>
<span class="l">)</span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l">l_dbg = <span class="fn">ESS_LOG_WRITE</span>(<span class="s">'SUCCESSFUL = '</span> || <span class="v">SUCCESSFUL</span>)<span class="lbl lbl-log">LOG</span></span>
<span class="l">l_dbg = <span class="fn">ESS_LOG_WRITE</span>(<span class="s">'ERROR_MESSAGE = '</span> || <span class="v">ERROR_MESSAGE</span>)</span>
<span class="l" style="min-height:0.4em;"></span>
<span class="l hl"><span class="kw">RETURN</span> <span class="v">SUCCESSFUL</span>, <span class="v">ERROR_MESSAGE</span><span class="lbl lbl-ret">RETURN</span></span>
</pre>
</div>


<h2>Block-by-Block Walkthrough</h2>

<div style="margin:20px 0 14px;padding:12px 16px;background:var(--bg-secondary);border-left:4px solid #0984e3;border-radius:0 6px 6px 0;"><span style="display:inline-block;width:28px;height:28px;border-radius:50%;background:#0984e3;color:#fff;font-weight:700;font-size:13px;line-height:28px;text-align:center;margin-right:10px;">1</span><strong style="font-size:15px;">Defaults and Initialization</strong></div>

<p>
<code>BEN_PEN_PL_NAME_TN</code> and <code>BEN_PEN_OPT_NAME_TN</code> are array DBIs — the <code>_TN</code> suffix indicates translated name. They need <code>DEFAULT_DATA_VALUE</code> (not <code>DEFAULT FOR</code>) because they're array DBIs. The default <code>'My-Default'</code> is never actually matched in the IF conditions — it's just a required syntactic safeguard.
</p>

<p>
<code>BEN_PIL_LF_EVT_OCRD_DT</code> is the life event occurred date — the date of the event that triggered enrollment (hire, open enrollment, qualifying life event). This is a regular DBI, not an array, so it uses <code>DEFAULT FOR</code>.
</p>

<p>
<code>SUCCESSFUL</code> starts as <code>'Y'</code>. The formula only changes it to <code>'N'</code> if the invalid combination is found. If none of the IF conditions fire, the employee passes validation by default. This is intentional — the formula should only block, never accidentally reject valid elections.
</p>

<div style="margin:20px 0 14px;padding:12px 16px;background:var(--bg-secondary);border-left:4px solid #c0392b;border-radius:0 6px 6px 0;"><span style="display:inline-block;width:28px;height:28px;border-radius:50%;background:#c0392b;color:#fff;font-weight:700;font-size:13px;line-height:28px;text-align:center;margin-right:10px;">2</span><strong style="font-size:15px;">Waiting Period Calculation</strong></div>

<p>
The formula extracts the day of the month using <code>TO_CHAR(date, 'DD')</code>. Two paths:
</p>

<p>
<strong>Path A — Event on the 1st:</strong> <code>ADD_MONTHS(date, 1)</code>. Coverage starts on the 1st of the next month. Simple.
</p>

<p>
<strong>Path B — Event on any other day:</strong> Three date functions chained together: <code>ADD_MONTHS(date, 2)</code> moves forward 2 months, <code>LAST_DAY()</code> goes to the end of that month, <code>ADD_DAYS(, 1)</code> moves to the 1st of the following month. This is the <code>LAST_DAY + ADD_DAYS(1)</code> pattern explained in the waiting period section above.
</p>

<div style="margin:20px 0 14px;padding:12px 16px;background:var(--bg-secondary);border-left:4px solid #6c5ce7;border-radius:0 6px 6px 0;"><span style="display:inline-block;width:28px;height:28px;border-radius:50%;background:#6c5ce7;color:#fff;font-weight:700;font-size:13px;line-height:28px;text-align:center;margin-right:10px;">3</span><strong style="font-size:15px;">Enrollment Result Array Loop</strong></div>

<p>
<code>CHANGE_CONTEXTS(EFFECTIVE_DATE = l_cvg_eff_date)</code> shifts the context forward to the coverage effective date. Every DBI read inside this block returns values as of that future date.
</p>

<p>
The <code>WHILE BEN_PEN_PL_NAME_TN.exists(i) LOOP</code> iterates through all plan enrollments for this person. The formula doesn't know how many there are — could be 2, could be 10. The <code>.exists(i)</code> check stops the loop when there are no more enrollments.
</p>

<p>
Inside the loop, two separate IF statements (not IF/ELSE). This is important — both conditions are checked at every index. If index 2 is Employee Life and index 3 is Child Life, both flags get set in separate iterations. If you used IF/ELSE, finding Child Life at index 2 would skip the Employee Life check at index 3.
</p>

<div style="margin:20px 0 14px;padding:12px 16px;background:var(--bg-secondary);border-left:4px solid #00b894;border-radius:0 6px 6px 0;"><span style="display:inline-block;width:28px;height:28px;border-radius:50%;background:#00b894;color:#fff;font-weight:700;font-size:13px;line-height:28px;text-align:center;margin-right:10px;">4</span><strong style="font-size:15px;">Cross-Plan Validation (Plan Presence + Coverage Amounts)</strong></div>

<p>
Two IF conditions, checked in order. <strong>Step 3</strong> is the plan-presence check — <code>l_child_flag = 'Y' AND l_emp_flag = 'N'</code> — Child Life elected but Employee Life not. This is Mike's scenario. <strong>Step 4</strong> is the amount check — <code>l_child_amt > l_emp_amt</code> — both plans elected but Child Life amount exceeds Employee Life. This is Lisa's scenario. The <code>ELSE IF</code> structure ensures Step 4 only runs when both plans are present.
</p>

<p>
There's no final ELSE. If neither condition matches, <code>SUCCESSFUL</code> stays at <code>'Y'</code> from initialization and the enrollment proceeds.
</p>


<h2>The ESS Log Output</h2>

<p>
Here's what the log looks like for Mike — dropping Employee Life but keeping Child Life, life event on April 10:
</p>

<div class="cbl">
  <div class="ch">ESS Log — Mike: Child Life Without Employee Life (Blocked — Step 3)</div>
  <pre>
<span class="l"><span class="s">l_event_dt is 04/10/2025</span><span class="lbl lbl-log">LOG</span></span>
<span class="l"><span class="s">l_cvg_eff_date is 07/01/2025</span>          <span class="c">/* 2-month wait → Jul 1 */</span></span>
<span class="l"><span class="s">Child Life = Y  Amt = 50000</span></span>
<span class="l"><span class="s">Employee Life = N  Amt = 0</span></span>
<span class="l"><span class="s">SUCCESSFUL = N</span></span>
<span class="l"><span class="s">ERROR_MESSAGE = Enrollment in Voluntary Child Life requires...</span></span>
</pre>
</div>

<p>
And for Lisa — both plans enrolled but Child Life amount exceeds Employee Life, event on March 20:
</p>

<div class="cbl">
  <div class="ch">ESS Log — Lisa: Child Amount Exceeds Employee (Blocked — Step 4)</div>
  <pre>
<span class="l"><span class="s">l_event_dt is 03/20/2025</span><span class="lbl lbl-log">LOG</span></span>
<span class="l"><span class="s">l_cvg_eff_date is 06/01/2025</span>          <span class="c">/* 2-month wait → Jun 1 */</span><span class="lbl lbl-log">LOG</span></span>
<span class="l"><span class="s">Child Life = Y  Amt = 150000</span></span>
<span class="l"><span class="s">Employee Life = Y  Amt = 100000</span></span>
<span class="l"><span class="s">SUCCESSFUL = N</span></span>
<span class="l"><span class="s">ERROR_MESSAGE = Child Life coverage ($150000) cannot exceed...</span></span>
</pre>
</div>

<p>
And for Sarah — existing Employee Life, adding Child Life within limits, event on January 1:
</p>

<div class="cbl">
  <div class="ch">ESS Log — Sarah: Both Plans, Amounts OK (Allowed)</div>
  <pre>
<span class="l"><span class="s">l_event_dt is 01/01/2025</span><span class="lbl lbl-log">LOG</span></span>
<span class="l"><span class="s">l_cvg_eff_date is 02/01/2025</span>          <span class="c">/* event on 1st → next month */</span></span>
<span class="l"><span class="s">Child Life = Y  Amt = 50000</span></span>
<span class="l"><span class="s">Employee Life = Y  Amt = 200000</span></span>
<span class="l"><span class="s">SUCCESSFUL = Y</span></span>
<span class="l"><span class="s">ERROR_MESSAGE = </span></span>
</pre>
</div>

<p>
The formula logs at every key stage: the life event date, the calculated effective date, the flags and amounts after the loop, and the final result. For deeper debugging, add <code>ESS_LOG_WRITE('Plan[' || TO_CHAR(i) || '] = ' || BEN_PEN_PL_NAME_TN[i])</code> inside the loop to print every plan in the array.
</p>

<div class="cb yellow">
  <div class="cb-t">Debugging Tip</div>
  <p>If the formula is blocking elections that should be allowed, add <code>ESS_LOG_WRITE('Plan[' || TO_CHAR(i) || '] = ' || BEN_PEN_PL_NAME_TN[i])</code> inside the loop. This prints every plan in the array. The most common issue is a plan name mismatch — the formula checks for <code>'Voluntary Employee Life and AD&D'</code> but the plan is configured as <code>'Voluntary Employee Life & AD&D'</code> (ampersand vs "and"). One character difference and the flag never gets set.</p>
</div>

<div class="cb yellow">
  <div class="cb-t">Edge Case — Zero Amounts</div>
  <p>If <code>BEN_PEN_BNFT_AMT_NN</code> returns the default value <code>0</code> for both plans (missing data, configuration issue, or non-monetary plan), the comparison <code>0 > 0</code> evaluates to FALSE — so the formula passes the employee through. This is intentional: <strong>don't block elections when you can't determine amounts.</strong> If your business requires blocking on zero amounts, add an explicit check: <code>IF (l_child_amt = 0 OR l_emp_amt = 0) THEN</code> with a separate error message.</p>
</div>

<div class="cb blue">
  <div class="cb-t">About the Code Labels</div>
  <p>The colored labels in the formula code (<code style="background:#c0392b;color:#fff;padding:1px 5px;border-radius:2px;font-size:10px;">REQUIRED</code> <code style="background:#c0392b;color:#fff;padding:1px 5px;border-radius:2px;font-size:10px;">CONTEXT</code> <code style="background:#c0392b;color:#fff;padding:1px 5px;border-radius:2px;font-size:10px;">LOG</code> <code style="background:#c0392b;color:#fff;padding:1px 5px;border-radius:2px;font-size:10px;">STEP 1</code> etc.) are <strong>blog annotations only</strong> — they highlight what each line does. <strong>Strip them before pasting into the formula editor.</strong> The formula editor will reject any text that isn't valid Fast Formula syntax.</p>
</div>


<h2>Where This Formula Is Attached</h2>

<table>
  <tr><th>Step</th><th>Where</th><th>What to Set</th></tr>
  <tr><td>1</td><td>Plan Configuration → Program or Plan → Enrollment</td><td>Select the plan in the plan hierarchy</td></tr>
  <tr><td>2</td><td>Further Details section → Post Election Edit</td><td>Select <code>XX_VOL_LIFE_CROSS_PLAN_EDIT</code></td></tr>
</table>

<p>
You can attach the formula at the plan level, plan type level, or option level depending on the scope. For this scenario — where the validation is between two plans — attach it at the <strong>plan type level</strong> so it fires for any plan within the Voluntary Life plan type.
</p>


<h2>Same Pattern, Different Plans</h2>

<p>
The cross-plan dependency pattern isn't limited to Life insurance. Any business rule that says "you can't enroll in Plan B without Plan A" uses the same formula structure.
</p>

<table>
  <tr><th>Plan A (Required)</th><th>Plan B (Dependent)</th><th>Business Rule</th></tr>
  <tr><td>HDHP Medical</td><td>HSA</td><td>Can't contribute to HSA without HDHP enrollment</td></tr>
  <tr><td>Voluntary Employee Life</td><td>Voluntary Spouse Life</td><td>Can't cover spouse without employee coverage</td></tr>
  <tr><td>Voluntary Employee Life</td><td>Voluntary Child Life</td><td>Can't cover children without employee coverage (this post)</td></tr>
  <tr><td>Medical Plan</td><td>Dependent Care FSA</td><td>Some employers require medical enrollment before FSA</td></tr>
  <tr><td>Dental</td><td>Orthodontia Rider</td><td>Can't add rider without base dental plan</td></tr>
</table>

<p>
In each case, the formula is identical in structure: loop through <code>BEN_PEN_PL_NAME_TN</code>, set flags for Plan A and Plan B, validate the combination. The plan names and error message change. The pattern doesn't.
</p>

<hr>


<h2>Recap</h2>

<p>
<strong>Post Election Edit</strong> formulas fire after election submission and return <code>SUCCESSFUL</code> = Y or N. They're the right tool for cross-plan dependency validation.
</p>
<p>
The formula in this post adds one layer of complexity: a <strong>waiting period calculation</strong> that computes a future effective date, then uses <code>CHANGE_CONTEXTS</code> to read enrollment results at that future date. Without this, the formula would check enrollment at the wrong point in time and produce false negatives.
</p>
<p>
Three things to watch when adapting this formula: <strong>(1)</strong> plan and option names must exactly match what's in Plan Configuration, <strong>(2)</strong> the waiting period logic must match your client's actual waiting period rules, and <strong>(3)</strong> use two separate IF statements inside the loop (not IF/ELSE) so both flags can be set in the same pass.
</p>

<hr>


<h2>References</h2>

<table>
  <tr><th>#</th><th>Source</th><th>What I Used From It</th></tr>
  <tr><td>1</td><td><a href="https://docs.oracle.com/en/cloud/saas/human-resources/24d/oapff/post-election-edit.html" style="color:var(--accent-blue);">Administering Fast Formulas — Post Election Edit ↗</a></td><td>Formula type contract: <code>SUCCESSFUL</code> and <code>ERROR_MESSAGE</code> return variables, available contexts, BEN_PEN array DBIs</td></tr>
  <tr><td>2</td><td><a href="https://docs.oracle.com/en/cloud/saas/human-resources/24d/fabdi/enrollment-rules.html" style="color:var(--accent-blue);">Implementing Benefits — Enrollment Rules ↗</a></td><td>Post Election Edit attachment point in Plan Configuration, plan type vs plan level vs option level scope</td></tr>
</table>

<div class="cb blue">
  <div class="cb-t">A Note on the Formula</div>
  <p>The formula in this post is based on a production Post Election Edit formula from a US Oracle HCM Cloud implementation. Plan and option names are unchanged to illustrate the exact-match sensitivity — in your implementation, replace them with your configured plan and option names. The waiting period logic, CHANGE_CONTEXTS pattern, and array DBI loop structure are reusable across any cross-plan dependency scenario.</p>
</div>

<hr>

<div class="author-card">
  <img src="data:image/jpeg;base64,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" style="width:46px;height:46px;border-radius:50%;object-fit:cover;flex-shrink:0;" alt="Abhishek Mohanty">
  <div>
    <div class="name">Abhishek Mohanty</div>
    <div class="role">Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.</div>
  </div>
</div>

<div class="tags-row">
  <span class="tag">Fast Formula</span>
  <span class="tag">Benefits</span>
  <span class="tag">Post Election Edit</span>
  <span class="tag">BEN_PEN_PL_NAME_TN</span>
  <span class="tag">CHANGE_CONTEXTS</span>
  <span class="tag">ESS_LOG_WRITE</span>
  <span class="tag">Waiting Period</span>
  <span class="tag">Cross-Plan Validation</span>
  <span class="tag">Voluntary Life</span>
  <span class="tag">Array DBI</span>
  <span class="tag">Oracle HCM Cloud</span>
</div>

<div class="footer">© 2026 Abhishek Mohanty — Oracle HCM Cloud Insights</div>

</div>
</body></html>