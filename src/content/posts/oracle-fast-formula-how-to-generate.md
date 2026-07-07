---
title: "Oracle Fast Formula: How to Generate Logs in OTL — Setup, Code, and Where to Find the Output"
description: "Fast Formula Time and Labor Logging TER & TCR Oracle Fast Formula: How to Generate Logs in OTL — Setup, Code, and Where to Find the Output Abhishek Mohanty · April 2026 · 14 min read · Oracle HCM Clou"
pubDate: 2026-04-19
tags: ["Fast Formula", "Oracle HCM Cloud", "Debugging"]
---


<span style="display:inline-block;padding:4px 12px;font-size:11px;font-weight:700;letter-spacing:.5px;color:#fff;margin:2px;text-transform:uppercase;background:#c0392b;font-family:'Open Sans',sans-serif">Fast Formula</span>
<span style="display:inline-block;padding:4px 12px;font-size:11px;font-weight:700;letter-spacing:.5px;color:#fff;margin:2px;text-transform:uppercase;background:#2e6b9e;font-family:'Open Sans',sans-serif">Time and Labor</span>
<span style="display:inline-block;padding:4px 12px;font-size:11px;font-weight:700;letter-spacing:.5px;color:#fff;margin:2px;text-transform:uppercase;background:#27795a;font-family:'Open Sans',sans-serif">Logging</span>
<span style="display:inline-block;padding:4px 12px;font-size:11px;font-weight:700;letter-spacing:.5px;color:#fff;margin:2px;text-transform:uppercase;background:#cf6e2c;font-family:'Open Sans',sans-serif">TER & TCR</span>

<div style="font-family:'Open Sans',Helvetica,Arial,sans-serif;color:#2a2a2a;line-height:1.7;max-width:860px;margin:0 auto">



<h1 style="font-size:28px;font-weight:700;color:#1a1a1a;line-height:1.3;margin:18px 0 6px;font-family:'Open Sans',sans-serif">Oracle Fast Formula: How to Generate Logs in OTL — Setup, Code, and Where to Find the Output</h1>

<p style="font-family:'Open Sans',sans-serif;font-size:14px;color:#7f8c8d;margin-bottom:20px">Abhishek Mohanty · April 2026 · 14 min read · Oracle HCM Cloud</p>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px">If you have ever written an OTL Fast Formula, deployed it, saved a timecard, and then opened the rule processing page expecting to see your debug lines — only to find the page empty — this post is for you.</p>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px">OTL logging fails for two reasons. Either the setup chain is incomplete and the formula never fires. Or the visibility switch is off and the engine throws your log lines away before saving them. The order matters. Most posts jump straight to the <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">add_log</code> function call, but if the rule never fires, no function call inside it can ever produce a line.</p>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px">This post walks the chain in the right order: setup first, then the formula, then the profile that makes everything visible.</p>



<hr style="border:0;height:1px;background:#e0dcd6;margin:30px 0">

<h2 style="font-size:22px;font-weight:700;color:#1a1a1a;margin:28px 0 14px;font-family:'Open Sans',sans-serif">TCR Setup — The Calculation Engine</h2>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px">We start with the TCR (Time Calculation Rule) because it is the engine that actually <em>does</em> something. It generates overtime entries, splits hours into pay tiers, and applies premium rates. The TER (Time Entry Rule) comes after, because the TER's job is to validate the inputs the TCR will consume. Build the engine first, then build the gatekeeper to feed it cleanly.</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">TCR Rule Template (Definition tab)</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px"><strong>Where:</strong> <em>Setup and Maintenance → Manage Time Rule Templates → New (or open the existing TCR template) → Definition tab.</em></p>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">Five fields matter on this screen:</p>


<div style="background:#fafafa;border:1px solid #e0dcd6;border-radius:8px;padding:20px;margin:18px 0">
<svg viewBox="0 0 720 460" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;font-family:'Open Sans',sans-serif">
  
  <rect x="10" y="10" width="700" height="440" rx="6" fill="#ffffff" stroke="#cfc9c1" stroke-width="1"/>
  <rect x="10" y="10" width="700" height="36" rx="6" fill="#1a1a1a"/>
  <rect x="10" y="34" width="700" height="12" fill="#1a1a1a"/>
  <circle cx="28" cy="28" r="5" fill="#ff5f57"/>
  <circle cx="46" cy="28" r="5" fill="#febc2e"/>
  <circle cx="64" cy="28" r="5" fill="#28c840"/>
  <text x="360" y="33" text-anchor="middle" fill="#fff" font-size="13" font-weight="700">Manage Time Rule Templates · Definition tab</text>

  
  <text x="40" y="80" font-size="13" fill="#333" font-weight="600">Name</text>
  <rect x="200" y="64" width="280" height="26" rx="4" fill="#fff" stroke="#cfc9c1"/>
  <text x="212" y="82" font-size="12" fill="#2a2a2a" font-family="Consolas,monospace">My_TCR_Template</text>

  <text x="40" y="118" font-size="13" fill="#333" font-weight="600">Template Type</text>
  <rect x="200" y="102" width="280" height="26" rx="4" fill="#fdf3ef" stroke="#c0392b" stroke-width="1.5"/>
  <text x="212" y="120" font-size="12" fill="#c0392b" font-family="Consolas,monospace" font-weight="700">Time Calculation Rule</text>
  <polygon points="466,113 474,113 470,121" fill="#c0392b"/>
  <text x="495" y="120" font-size="12" fill="#27795a" font-style="italic">← pins to TCR</text>

  <text x="40" y="156" font-size="13" fill="#333" font-weight="600">Rule Classification</text>
  <rect x="200" y="140" width="280" height="26" rx="4" fill="#fdf3ef" stroke="#c0392b" stroke-width="1.5"/>
  <text x="212" y="158" font-size="12" fill="#c0392b" font-family="Consolas,monospace" font-weight="700">Threshold / Shift premium</text>
  <polygon points="466,151 474,151 470,159" fill="#c0392b"/>
  <text x="495" y="158" font-size="12" fill="#27795a" font-style="italic">← subtype</text>

  <text x="40" y="194" font-size="13" fill="#333" font-weight="600">Rule Execution Type</text>
  <rect x="200" y="178" width="280" height="26" rx="4" fill="#fdf3ef" stroke="#c0392b" stroke-width="1.5"/>
  <text x="212" y="196" font-size="12" fill="#c0392b" font-family="Consolas,monospace" font-weight="700">Create</text>
  <polygon points="466,189 474,189 470,197" fill="#c0392b"/>
  <text x="495" y="196" font-size="12" fill="#27795a" font-style="italic">← adds hours</text>

  <text x="40" y="232" font-size="13" fill="#333" font-weight="600">Summation Level</text>
  <rect x="200" y="216" width="280" height="26" rx="4" fill="#fdf3ef" stroke="#c0392b" stroke-width="1.5"/>
  <text x="212" y="234" font-size="12" fill="#c0392b" font-family="Consolas,monospace" font-weight="700">Details</text>
  <polygon points="466,225 474,225 470,233" fill="#c0392b"/>
  <text x="495" y="234" font-size="12" fill="#27795a" font-style="italic">← one call per row</text>

  
  <line x1="30" y1="266" x2="690" y2="266" stroke="#e0dcd6"/>
  <text x="40" y="290" font-size="13" fill="#333" font-weight="700">Time Card Events</text>

  <rect x="200" y="278" width="14" height="14" rx="2" fill="#c0392b" stroke="#c0392b"/>
  <polyline points="203,285 207,289 212,281" stroke="#fff" stroke-width="2" fill="none"/>
  <text x="222" y="290" font-size="13" fill="#2a2a2a" font-weight="600">Submit</text>
  <text x="290" y="290" font-size="11" fill="#7f8c8d" font-style="italic">(default)</text>

  <rect x="200" y="304" width="14" height="14" rx="2" fill="#c0392b" stroke="#c0392b"/>
  <polyline points="203,311 207,315 212,307" stroke="#fff" stroke-width="2" fill="none"/>
  <text x="222" y="316" font-size="13" fill="#2a2a2a" font-weight="600">Resubmit</text>
  <text x="290" y="316" font-size="11" fill="#7f8c8d" font-style="italic">(default)</text>

  <rect x="200" y="330" width="14" height="14" rx="2" fill="#fff" stroke="#999"/>
  <text x="222" y="342" font-size="13" fill="#666">Save</text>
  <text x="290" y="342" font-size="11" fill="#7f8c8d" font-style="italic">(editable)</text>

  <rect x="200" y="356" width="14" height="14" rx="2" fill="#fff" stroke="#999"/>
  <text x="222" y="368" font-size="13" fill="#666">Delete</text>
  <text x="290" y="368" font-size="11" fill="#7f8c8d" font-style="italic">(editable)</text>

  
  <line x1="30" y1="395" x2="690" y2="395" stroke="#e0dcd6"/>
  <rect x="475" y="412" width="80" height="28" rx="4" fill="#fff" stroke="#cfc9c1"/>
  <text x="515" y="430" font-size="12" fill="#666" text-anchor="middle">Cancel</text>
  <rect x="565" y="412" width="125" height="28" rx="4" fill="#c0392b"/>
  <text x="627" y="430" font-size="12" fill="#fff" font-weight="700" text-anchor="middle">Save and Next</text>
</svg>
</div>
<p style="font-family:'Open Sans',sans-serif;text-align:center;font-size:13px;color:#7f8c8d;font-style:italic;margin:-4px 0 24px">Fig 1 — The TCR template Definition tab. Highlighted dropdowns and default-checked events are the fields that control engine behaviour.</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;border:2px solid #1a1a1a;overflow:hidden">
  <tr><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:28%">Field</th><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:20%">Value</th><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase">Why This Value</th></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Name</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px"><code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">Pick a clear name</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Use a prefix + verb describing what the rule does. Names cannot be edited after the first save in some Oracle releases — get it right the first time.</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Template Type</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px"><code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">Time Calculation Rule</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Top-level selector that determines which formula types the engine will accept. <strong>Cannot be changed after creation.</strong> A separate <em>Rule Classification</em> dropdown below lets you pick a subtype (Threshold, Shift premium, Meal, Break) within this template type.</td></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Rule Execution Type</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px"><code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">Create</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Most overtime calculations need Create — the engine generates new derived rows alongside the source. See the comparison below.</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Summation Level</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px"><code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">Details</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Engine calls the formula once per detail row. Formula keeps running totals across calls using <code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">set_wrk_num</code> / <code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">get_wrk_num</code>. Day would batch a whole day — you cannot tell which entry caused the cap to be crossed.</td></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px;font-weight:600">Time Card Events</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px"><code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">Submit + Resubmit</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px">Submit and Resubmit are checked by default — overtime must run at submit time when payroll consumes the data. <strong>Save is editable</strong> if you need calculation to run on every keystroke; most teams leave it off so users don't see overtime numbers shifting as they enter time.</td></tr>
</table>


<div style="border-left:4px solid #c0392b;background:#fff7f5;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#c0392b;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">📌 Execution Type — Update vs Create (per Oracle guide p. 156)</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a">Oracle's official distinction is about <em>total hours</em>. <strong>Create adds NEW premium hours on top of reported time — total goes UP</strong> (10 reported → 12 total = 10 reg + 2 added premium). <strong>Update redistributes the SAME reported hours into different pay categories — total stays the SAME</strong> (10 reported → 10 total = 8 reg + 2 OT). Pick the value that matches whether your formula is <em>adding</em> hours or <em>reclassifying</em> them.</p>
</div>


<div style="background:#fafafa;border:1px solid #e0dcd6;border-radius:8px;padding:20px;margin:18px 0">
<svg viewBox="0 0 680 320" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;font-family:'Open Sans',sans-serif">

  
  <rect x="20" y="15" width="640" height="130" rx="6" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
  <text x="40" y="42" font-size="16" font-weight="700" fill="#c0392b" letter-spacing="1">CREATE</text>
  <text x="140" y="42" font-size="13" fill="#666">adds new hours → total goes UP</text>

  
  <text x="40" y="72" font-size="12" fill="#888">Before</text>
  <rect x="100" y="58" width="400" height="24" rx="4" fill="#e8e0d8"/>
  <text x="300" y="75" text-anchor="middle" font-size="12" fill="#2a2a2a" font-weight="600">Regular = 10 hrs</text>

  
  <text x="40" y="114" font-size="12" fill="#888">After</text>
  <rect x="100" y="100" width="400" height="24" rx="4" fill="#e8e0d8"/>
  <text x="300" y="117" text-anchor="middle" font-size="12" fill="#2a2a2a" font-weight="600">Regular = 10 hrs</text>
  <rect x="500" y="100" width="80" height="24" rx="4" fill="#c0392b"/>
  <text x="540" y="117" text-anchor="middle" font-size="11" fill="#fff" font-weight="700">+2 hrs</text>
  <text x="600" y="117" font-size="13" fill="#c0392b" font-weight="700">= 12 hrs</text>

  
  <rect x="20" y="170" width="640" height="130" rx="6" fill="#fff" stroke="#2e6b9e" stroke-width="1.5"/>
  <text x="40" y="197" font-size="16" font-weight="700" fill="#2e6b9e" letter-spacing="1">UPDATE</text>
  <text x="145" y="197" font-size="13" fill="#666">reclassifies existing hours → total stays SAME</text>

  
  <text x="40" y="227" font-size="12" fill="#888">Before</text>
  <rect x="100" y="213" width="400" height="24" rx="4" fill="#e8e0d8"/>
  <text x="300" y="230" text-anchor="middle" font-size="12" fill="#2a2a2a" font-weight="600">Regular = 10 hrs</text>

  
  <text x="40" y="269" font-size="12" fill="#888">After</text>
  <rect x="100" y="255" width="320" height="24" rx="4" fill="#c8d6e2"/>
  <text x="260" y="272" text-anchor="middle" font-size="12" fill="#1a1a1a" font-weight="600">Regular = 8 hrs</text>
  <rect x="420" y="255" width="80" height="24" rx="4" fill="#2e6b9e"/>
  <text x="460" y="272" text-anchor="middle" font-size="11" fill="#fff" font-weight="700">OT = 2 hrs</text>
  <text x="520" y="272" font-size="13" fill="#2e6b9e" font-weight="700">= 10 hrs</text>

</svg>
</div>
<p style="font-family:'Open Sans',sans-serif;text-align:center;font-size:13px;color:#7f8c8d;font-style:italic;margin:-4px 0 24px">Fig 2 — Create adds hours on top (total increases). Update splits existing hours into different pay buckets (total unchanged).</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">Time Category (Conditions tab)</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px"><strong>Where:</strong> <em>Setup and Maintenance → Manage Time Categories → open (or create) your category → Conditions tab.</em></p>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">The Time Category is a reusable filter. It tells the rule which Payroll Time Types to look at and which to ignore. The principle: <strong>one rule, one job</strong>. Do not let the TCR see entries it has no business processing.</p>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">For example, if the TER already validates meal breaks, the TCR has no reason to see them. Pulling Meal Break out of the category fixes two problems with one save: noisy log lines disappear, and meal hours stop inflating the daily worked-hours total.</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;border:2px solid #1a1a1a;overflow:hidden">
  <tr><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:65%">Time Type</th><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase">Include?</th></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Regular Hours</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;color:#27795a;font-weight:600">✓ Include</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Overtime tiers (1.5x, 2x, etc.)</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;color:#27795a;font-weight:600">✓ Include</td></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Holiday / Rest Day premiums</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;color:#27795a;font-weight:600">✓ Include</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Meal Break / Unpaid Break</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;color:#c0392b;font-weight:600">✗ Remove</td></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px">Absence entries / anything the TER handles</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px;color:#c0392b;font-weight:600">✗ Remove</td></tr>
</table>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px">The exact list depends on your design. The principle is what matters: include only what this rule needs to process.</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">TCR Rule (Parameters tab)</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px"><strong>Where:</strong> <em>Setup and Maintenance → Manage Time Calculation Rules → open your rule → Parameters tab.</em></p>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">The rule is an instance of the template with parameter values filled in. The most important parameter is <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">WORKED_TIME_CONDITION</code> — this is the link between the rule and the Time Category. Without it, the engine processes <em>all</em> time types regardless of what your category says. Set it on the rule, not the rule set, not the template.</p>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">Threshold parameters (daily regular cap, weekly cap, OT cap) are <em>custom</em> — you choose the names and values when you build the rule template. Set them to match your local labour law or company policy. The advantage of parameters over hardcoding: a functional consultant can edit the value in the UI without ever touching the formula.</p>

<div style="border-left:4px solid #cf6e2c;background:#fff8f0;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#cf6e2c;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">⚠️ Always verify the binding visually</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a">"Confirmed" in a chat message is not the same as "I see it on screen". Open the rule's Parameters tab, screenshot it, and attach it to your design document.</p>
</div>

<div style="border-left:4px solid #c0392b;background:#fff7f5;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#c0392b;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">📌 Time Category can also bind at the Rule Set level</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a">The implementation guide (p. 87) also lets you attach a Time Category to a rule set member. Use rule-level binding via <code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">WORKED_TIME_CONDITION</code> when the category scopes which entries one rule processes. Use rule-set-level binding when the category gates whether the entire rule set member runs at all.</p>
</div>



<hr style="border:0;height:1px;background:#e0dcd6;margin:30px 0">

<h2 style="font-size:22px;font-weight:700;color:#1a1a1a;margin:28px 0 14px;font-family:'Open Sans',sans-serif">TER Setup — The Gatekeeper</h2>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px">The TER (Time Entry Rule) validates entries before the TCR sees them. Different rule type, different needs.</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">TER Rule Template (Definition tab)</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px"><strong>Where:</strong> <em>Setup and Maintenance → Manage Time Rule Templates → open (or create) the TER template → Definition tab.</em></p>


<div style="background:#fafafa;border:1px solid #e0dcd6;border-radius:8px;padding:20px;margin:18px 0">
<svg viewBox="0 0 720 480" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;font-family:'Open Sans',sans-serif">
  
  <rect x="10" y="10" width="700" height="460" rx="6" fill="#ffffff" stroke="#cfc9c1" stroke-width="1"/>
  <rect x="10" y="10" width="700" height="36" rx="6" fill="#1a1a1a"/>
  <rect x="10" y="34" width="700" height="12" fill="#1a1a1a"/>
  <circle cx="28" cy="28" r="5" fill="#ff5f57"/>
  <circle cx="46" cy="28" r="5" fill="#febc2e"/>
  <circle cx="64" cy="28" r="5" fill="#28c840"/>
  <text x="360" y="33" text-anchor="middle" fill="#fff" font-size="13" font-weight="700">Manage Time Rule Templates · Definition tab</text>

  
  <text x="40" y="80" font-size="13" fill="#333" font-weight="600">Name</text>
  <rect x="200" y="64" width="280" height="26" rx="4" fill="#fff" stroke="#cfc9c1"/>
  <text x="212" y="82" font-size="12" fill="#2a2a2a" font-family="Consolas,monospace">My_TER_Template</text>

  <text x="40" y="118" font-size="13" fill="#333" font-weight="600">Template Type</text>
  <rect x="200" y="102" width="280" height="26" rx="4" fill="#fdf3ef" stroke="#c0392b" stroke-width="1.5"/>
  <text x="212" y="120" font-size="12" fill="#c0392b" font-family="Consolas,monospace" font-weight="700">Time Entry Rule</text>
  <polygon points="466,113 474,113 470,121" fill="#c0392b"/>
  <text x="495" y="120" font-size="12" fill="#27795a" font-style="italic">← pins to TER</text>

  <text x="40" y="156" font-size="13" fill="#333" font-weight="600">Rule Classification</text>
  <rect x="200" y="140" width="280" height="26" rx="4" fill="#fdf3ef" stroke="#c0392b" stroke-width="1.5"/>
  <text x="212" y="158" font-size="12" fill="#c0392b" font-family="Consolas,monospace" font-weight="700">Business message / Variance</text>
  <polygon points="466,151 474,151 470,159" fill="#c0392b"/>
  <text x="495" y="158" font-size="12" fill="#27795a" font-style="italic">← subtype</text>

  <text x="40" y="194" font-size="13" fill="#333" font-weight="600">Summation Level</text>
  <rect x="200" y="178" width="280" height="26" rx="4" fill="#fdf3ef" stroke="#c0392b" stroke-width="1.5"/>
  <text x="212" y="196" font-size="12" fill="#c0392b" font-family="Consolas,monospace" font-weight="700">Day</text>
  <polygon points="466,189 474,189 470,197" fill="#c0392b"/>
  <text x="495" y="196" font-size="12" fill="#27795a" font-style="italic">← or Time Card</text>

  <text x="40" y="232" font-size="13" fill="#333" font-weight="600">Reporting Level</text>
  <rect x="200" y="216" width="280" height="26" rx="4" fill="#fdf3ef" stroke="#c0392b" stroke-width="1.5"/>
  <text x="212" y="234" font-size="12" fill="#c0392b" font-family="Consolas,monospace" font-weight="700">Day</text>
  <polygon points="466,225 474,225 470,233" fill="#c0392b"/>
  <text x="495" y="234" font-size="12" fill="#27795a" font-style="italic">← match summation</text>

  
  <line x1="30" y1="266" x2="690" y2="266" stroke="#e0dcd6"/>
  <text x="40" y="290" font-size="13" fill="#333" font-weight="700">Time Card Events</text>
  <text x="220" y="290" font-size="11" fill="#cf6e2c" font-style="italic">all editable — tune per rule</text>

  <rect x="200" y="304" width="14" height="14" rx="2" fill="#c0392b" stroke="#c0392b"/>
  <polyline points="203,311 207,315 212,307" stroke="#fff" stroke-width="2" fill="none"/>
  <text x="222" y="316" font-size="13" fill="#2a2a2a" font-weight="600">Save</text>
  <text x="290" y="316" font-size="11" fill="#7f8c8d" font-style="italic">(default — immediate validation)</text>

  <rect x="200" y="330" width="14" height="14" rx="2" fill="#c0392b" stroke="#c0392b"/>
  <polyline points="203,337 207,341 212,333" stroke="#fff" stroke-width="2" fill="none"/>
  <text x="222" y="342" font-size="13" fill="#2a2a2a" font-weight="600">Submit</text>
  <text x="290" y="342" font-size="11" fill="#7f8c8d" font-style="italic">(default)</text>

  <rect x="200" y="356" width="14" height="14" rx="2" fill="#c0392b" stroke="#c0392b"/>
  <polyline points="203,363 207,367 212,359" stroke="#fff" stroke-width="2" fill="none"/>
  <text x="222" y="368" font-size="13" fill="#2a2a2a" font-weight="600">Resubmit</text>
  <text x="290" y="368" font-size="11" fill="#7f8c8d" font-style="italic">(default)</text>

  <rect x="200" y="382" width="14" height="14" rx="2" fill="#fff" stroke="#999"/>
  <text x="222" y="394" font-size="13" fill="#666">Delete</text>
  <text x="290" y="394" font-size="11" fill="#7f8c8d" font-style="italic">(off by default)</text>

  
  <line x1="30" y1="415" x2="690" y2="415" stroke="#e0dcd6"/>
  <rect x="475" y="432" width="80" height="28" rx="4" fill="#fff" stroke="#cfc9c1"/>
  <text x="515" y="450" font-size="12" fill="#666" text-anchor="middle">Cancel</text>
  <rect x="565" y="432" width="125" height="28" rx="4" fill="#c0392b"/>
  <text x="627" y="450" font-size="12" fill="#fff" font-weight="700" text-anchor="middle">Save and Next</text>
</svg>
</div>
<p style="font-family:'Open Sans',sans-serif;text-align:center;font-size:13px;color:#7f8c8d;font-style:italic;margin:-4px 0 24px">Fig 3 — The TER template Definition tab. Summation Level and Reporting Level are two independent dropdowns — they can hold different values.</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;border:2px solid #1a1a1a;overflow:hidden">
  <tr><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:28%">Field</th><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:22%">Value</th><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase">Why This Value</th></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Template Type</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px"><code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">Time Entry Rule</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Top-level selector that gives the formula access to entry-level context arrays. The <em>Rule Classification</em> dropdown below lets you pick a subtype (Business message, Comparison validation, Hours entered, Variance) within this template type.</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Summation Level</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px"><code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">Day or Time Card</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px"><strong>Day</strong> — engine bundles all detail rows for one day + END_DAY marker. Good for overlap, continuous stretch, meal break checks. <strong>Time Card</strong> — engine bundles the entire period. Good for weekly max hours, min days worked. See the <em>Day vs Time Card Summation</em> section below for code differences.</td></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Reporting Level</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px"><code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">Match your summation</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Where the error message appears: Details = row-level, Day = day banner, Time Card = period banner. Independent of Summation Level — they are two separate dropdowns and people mix them up.</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px;font-weight:600">Time Card Events</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px"><code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">Save · Submit · Resubmit</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px">Save, Submit, and Resubmit are typically checked for TER templates so validation fires on every user action. All four events are editable — untick Save if validation is expensive and you only want it at submission time.</td></tr>
</table>

<div style="border-left:4px solid #cf6e2c;background:#fff8f0;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#cf6e2c;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">⚠️ Regenerate after changing the template</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a">Changing Summation Level on the template does not take effect until you click through the wizard to Review and re-save. The rule built from the template also needs regeneration. Skip either step and the engine behaves as if nothing changed.</p>
</div>


<div style="background:#fafafa;border:1px solid #e0dcd6;border-radius:8px;padding:20px;margin:18px 0">
<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;font-family:'Open Sans',sans-serif">

  
  <rect x="20" y="10" width="640" height="145" rx="6" fill="#fff" stroke="#2e6b9e" stroke-width="1.5"/>
  <text x="40" y="36" font-size="15" font-weight="700" fill="#2e6b9e" letter-spacing="1">DAY</text>
  <text x="85" y="36" font-size="13" fill="#666">— formula called once per day</text>
  <text x="560" y="36" font-size="14" fill="#2e6b9e" font-weight="700">5 calls</text>

  
  <g font-size="11" font-weight="600">
    
    <rect x="40" y="55" width="52" height="30" rx="4" fill="#2e6b9e"/><text x="66" y="75" text-anchor="middle" fill="#fff">Mon</text>
    <line x1="92" y1="70" x2="112" y2="70" stroke="#2e6b9e" stroke-width="1.5"/><polygon points="110,66 116,70 110,74" fill="#2e6b9e"/>
    <rect x="116" y="60" width="24" height="20" rx="3" fill="#f2f5f8" stroke="#2e6b9e"/><text x="128" y="74" text-anchor="middle" fill="#2e6b9e" font-size="8" font-weight="700">FF</text>

    
    <rect x="160" y="55" width="52" height="30" rx="4" fill="#2e6b9e"/><text x="186" y="75" text-anchor="middle" fill="#fff">Tue</text>
    <line x1="212" y1="70" x2="232" y2="70" stroke="#2e6b9e" stroke-width="1.5"/><polygon points="230,66 236,70 230,74" fill="#2e6b9e"/>
    <rect x="236" y="60" width="24" height="20" rx="3" fill="#f2f5f8" stroke="#2e6b9e"/><text x="248" y="74" text-anchor="middle" fill="#2e6b9e" font-size="8" font-weight="700">FF</text>

    
    <rect x="280" y="55" width="52" height="30" rx="4" fill="#2e6b9e"/><text x="306" y="75" text-anchor="middle" fill="#fff">Wed</text>
    <line x1="332" y1="70" x2="352" y2="70" stroke="#2e6b9e" stroke-width="1.5"/><polygon points="350,66 356,70 350,74" fill="#2e6b9e"/>
    <rect x="356" y="60" width="24" height="20" rx="3" fill="#f2f5f8" stroke="#2e6b9e"/><text x="368" y="74" text-anchor="middle" fill="#2e6b9e" font-size="8" font-weight="700">FF</text>

    
    <rect x="400" y="55" width="52" height="30" rx="4" fill="#2e6b9e"/><text x="426" y="75" text-anchor="middle" fill="#fff">Thu</text>
    <line x1="452" y1="70" x2="472" y2="70" stroke="#2e6b9e" stroke-width="1.5"/><polygon points="470,66 476,70 470,74" fill="#2e6b9e"/>
    <rect x="476" y="60" width="24" height="20" rx="3" fill="#f2f5f8" stroke="#2e6b9e"/><text x="488" y="74" text-anchor="middle" fill="#2e6b9e" font-size="8" font-weight="700">FF</text>

    
    <rect x="520" y="55" width="52" height="30" rx="4" fill="#2e6b9e"/><text x="546" y="75" text-anchor="middle" fill="#fff">Fri</text>
    <line x1="572" y1="70" x2="592" y2="70" stroke="#2e6b9e" stroke-width="1.5"/><polygon points="590,66 596,70 590,74" fill="#2e6b9e"/>
    <rect x="596" y="60" width="24" height="20" rx="3" fill="#f2f5f8" stroke="#2e6b9e"/><text x="608" y="74" text-anchor="middle" fill="#2e6b9e" font-size="8" font-weight="700">FF</text>
  </g>

  
  <text x="340" y="116" text-anchor="middle" font-size="12" fill="#1a1a1a" font-weight="700">Each call is independent — state resets between days</text>
  <text x="340" y="136" text-anchor="middle" font-size="11" fill="#27795a" font-weight="600">Simpler code · good for daily validations</text>

  
  <rect x="20" y="180" width="640" height="145" rx="6" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
  <text x="40" y="206" font-size="15" font-weight="700" fill="#c0392b" letter-spacing="1">TIME CARD</text>
  <text x="145" y="206" font-size="13" fill="#666">— formula called once for the whole period</text>
  <text x="565" y="206" font-size="14" fill="#c0392b" font-weight="700">1 call</text>

  
  <g font-size="11" font-weight="600">
    <rect x="40" y="225" width="52" height="30" rx="4" fill="#c0392b"/><text x="66" y="245" text-anchor="middle" fill="#fff">Mon</text>
    <rect x="96" y="225" width="52" height="30" rx="4" fill="#c0392b"/><text x="122" y="245" text-anchor="middle" fill="#fff">Tue</text>
    <rect x="152" y="225" width="52" height="30" rx="4" fill="#c0392b"/><text x="178" y="245" text-anchor="middle" fill="#fff">Wed</text>
    <rect x="208" y="225" width="52" height="30" rx="4" fill="#c0392b"/><text x="234" y="245" text-anchor="middle" fill="#fff">Thu</text>
    <rect x="264" y="225" width="52" height="30" rx="4" fill="#c0392b"/><text x="290" y="245" text-anchor="middle" fill="#fff">Fri</text>

    
    <path d="M38,222 L38,258 M38,258 L318,258 M318,258 L318,222" fill="none" stroke="#c0392b" stroke-width="1.5"/>

    
    <line x1="318" y1="240" x2="380" y2="240" stroke="#c0392b" stroke-width="2"/>
    <polygon points="378,235 386,240 378,245" fill="#c0392b"/>
    <rect x="390" y="225" width="60" height="30" rx="4" fill="#fdf3ef" stroke="#c0392b" stroke-width="1.5"/>
    <text x="420" y="245" text-anchor="middle" fill="#c0392b" font-size="12" font-weight="700">FF</text>
  </g>

  
  <text x="340" y="286" text-anchor="middle" font-size="12" fill="#1a1a1a" font-weight="700">All days in one array — state accumulates across the week</text>
  <text x="340" y="306" text-anchor="middle" font-size="11" fill="#cf6e2c" font-weight="600">More code · needed for weekly totals and cross-day checks</text>

</svg>
</div>
<p style="font-family:'Open Sans',sans-serif;text-align:center;font-size:13px;color:#7f8c8d;font-style:italic;margin:-4px 0 24px">Fig 4 — Day mode runs the formula 5 separate times. Time Card mode runs it once with everything bundled together.</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">TER Rule (Parameters tab)</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px">The TER rule typically does not need a Time Category binding — validation runs across all time types. Its parameters are the validation thresholds (schedule start/end hour, maximum continuous hours before warning or error). Set these on the rule, not the template.</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">Bind Both Rules into Rule Sets and Profile</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">The remaining setup is the same for both TER and TCR — five steps, and all five must be in place or the formula never fires:</p>


<div style="background:#fafafa;border:1px solid #e0dcd6;border-radius:8px;padding:20px;margin:18px 0">
<svg viewBox="0 0 620 370" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;font-family:'Open Sans',sans-serif">

  
  <rect x="20" y="10" width="580" height="44" rx="6" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
  <circle cx="48" cy="32" r="14" fill="#c0392b"/>
  <text x="48" y="37" text-anchor="middle" font-size="13" fill="#fff" font-weight="700">1</text>
  <text x="75" y="28" font-size="13" fill="#1a1a1a" font-weight="700">Add the Rule to a Rule Set</text>
  <text x="75" y="44" font-size="11" fill="#666">Manage Time Calculation Rule Sets (TCR) or Time Entry Rule Sets (TER)</text>

  
  <line x1="310" y1="54" x2="310" y2="68" stroke="#cfc9c1" stroke-width="2"/>
  <polygon points="305,66 315,66 310,72" fill="#cfc9c1"/>

  
  <rect x="20" y="74" width="580" height="44" rx="6" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
  <circle cx="48" cy="96" r="14" fill="#c0392b"/>
  <text x="48" y="101" text-anchor="middle" font-size="13" fill="#fff" font-weight="700">2</text>
  <text x="75" y="92" font-size="13" fill="#1a1a1a" font-weight="700">Attach Rule Set to a Worker Time Processing Profile</text>
  <text x="75" y="108" font-size="11" fill="#666">Entry rule set and Calculation rule set go on the same profile</text>

  <line x1="310" y1="118" x2="310" y2="132" stroke="#cfc9c1" stroke-width="2"/>
  <polygon points="305,130 315,130 310,136" fill="#cfc9c1"/>

  
  <rect x="20" y="138" width="580" height="44" rx="6" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
  <circle cx="48" cy="160" r="14" fill="#c0392b"/>
  <text x="48" y="165" text-anchor="middle" font-size="13" fill="#fff" font-weight="700">3</text>
  <text x="75" y="156" font-size="13" fill="#1a1a1a" font-weight="700">Assign the Profile to an HCM Group</text>
  <text x="75" y="172" font-size="11" fill="#666">The group defines which workers this profile applies to</text>

  <line x1="310" y1="182" x2="310" y2="196" stroke="#cfc9c1" stroke-width="2"/>
  <polygon points="305,194 315,194 310,200" fill="#cfc9c1"/>

  
  <rect x="20" y="202" width="580" height="44" rx="6" fill="#fff" stroke="#c0392b" stroke-width="1.5"/>
  <circle cx="48" cy="224" r="14" fill="#c0392b"/>
  <text x="48" y="229" text-anchor="middle" font-size="13" fill="#fff" font-weight="700">4</text>
  <text x="75" y="220" font-size="13" fill="#1a1a1a" font-weight="700">Run Evaluate HCM Group Membership</text>
  <text x="75" y="236" font-size="11" fill="#666">Tools → Scheduled Processes — run it manually or schedule it</text>

  <line x1="310" y1="246" x2="310" y2="260" stroke="#cfc9c1" stroke-width="2"/>
  <polygon points="305,258 315,258 310,264" fill="#cfc9c1"/>

  
  <rect x="20" y="266" width="580" height="44" rx="6" fill="#f3faf6" stroke="#27795a" stroke-width="2"/>
  <circle cx="48" cy="288" r="14" fill="#27795a"/>
  <text x="48" y="293" text-anchor="middle" font-size="13" fill="#fff" font-weight="700">5</text>
  <text x="75" y="284" font-size="13" fill="#1a1a1a" font-weight="700">Worker saves a timecard → formula fires</text>
  <text x="75" y="300" font-size="11" fill="#27795a">If everything above is in place, the engine will invoke your formula</text>

  
  <rect x="20" y="326" width="580" height="34" rx="4" fill="#fdf3ef" stroke="#c0392b" stroke-width="1"/>
  <text x="310" y="348" text-anchor="middle" font-size="12" fill="#c0392b" font-weight="600">⚠ Skip step 4 and the formula never fires — this is the most commonly missed step</text>

</svg>
</div>
<p style="font-family:'Open Sans',sans-serif;text-align:center;font-size:13px;color:#7f8c8d;font-style:italic;margin:-4px 0 24px">Fig 5 — The setup chain. All five steps must be in place or the formula never fires.</p>



<hr style="border:0;height:1px;background:#e0dcd6;margin:30px 0">

<h2 style="font-size:22px;font-weight:700;color:#1a1a1a;margin:28px 0 14px;font-family:'Open Sans',sans-serif">Logging Inside the Formula</h2>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px">Setup chain done. The engine will now call your formula when a user saves a timecard. Time to write the lines that capture what is happening inside. OTL exposes <strong>two functions</strong> for this — both work, both write to the same place.</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">The Two Logging Functions</h3>

<table style="width:100%;border-collapse:collapse;margin:18px 0;border:2px solid #1a1a1a;overflow:hidden">
  <tr><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:22%">Function</th><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:30%">Arguments</th><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase">When to Use</th></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600"><code style="font-size:13px;color:#c0392b">add_log</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px"><code style="font-size:13px">(ffs_id, message)</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">The shorter form. The rule_id is figured out automatically by the engine. Works in standard TER and TCR formulas.</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px;font-weight:600"><code style="font-size:13px;color:#c0392b">add_rlog</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px"><code style="font-size:13px">(ffs_id, rule_id, message)</code></td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px">The longer form with rule_id passed explicitly. Use when the auto-determined rule_id is not behaving the way you expect.</td></tr>
</table>

<p style="font-family:'Open Sans',sans-serif;font-size:15px;margin-bottom:18px;color:#666">Both functions return a number. Fast Formula requires every expression to be assigned, so we write <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">flog = add_log(...)</code> — the value of <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">flog</code> is never used.</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">The Two Required Contexts</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">Both functions need <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">ffs_id</code>. <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">add_rlog</code> also needs <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">rule_id</code>. Both come from contexts the engine populates before calling your formula:</p>

<pre style="background:#fafafa;border-left:3px solid #c0392b;padding:16px 20px;margin:18px 0;font-family:Consolas,Monaco,monospace;font-size:13px;color:#2a2a2a;line-height:1.7;overflow-x:auto;white-space:pre-wrap">ffs_id  = GET_CONTEXT(HWM_FFS_ID, 0)
rule_id = GET_CONTEXT(HWM_RULE_ID, 0)</pre>

<div style="border-left:4px solid #cf6e2c;background:#fff8f0;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#cf6e2c;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">📌 The HWM_ prefix matters</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a">Older posts show <code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">HXT_FFS_ID</code> or <code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">HXT_RULE_ID</code> — those are leftover names from the on-premises HXT module. In Oracle Fusion HCM Cloud, the contexts are <strong>HWM_</strong>. Mixing them up gives you a NULL ffs_id and every <code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">add_log</code> call silently writes nothing.</p>
</div>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">Where the Lines Actually Go</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">Both functions produce log lines that you view on the <strong>Analyze Rule Processing Details</strong> page — that is the supported way to read OTL formula logs.</p>


<div style="background:#fafafa;border:1px solid #e0dcd6;border-radius:8px;padding:20px;margin:18px 0">
<svg viewBox="0 0 520 90" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;font-family:'Open Sans',sans-serif">
  
  <rect x="10" y="10" width="200" height="70" rx="6" fill="#fff" stroke="#c0392b" stroke-width="2"/>
  <text x="110" y="38" text-anchor="middle" font-size="13" font-weight="700" fill="#1a1a1a">Your Formula</text>
  <text x="110" y="58" text-anchor="middle" font-size="12" fill="#c0392b" font-family="Consolas,monospace">add_log() / add_rlog()</text>

  
  <line x1="210" y1="45" x2="290" y2="45" stroke="#666" stroke-width="2"/>
  <polygon points="288,40 296,45 288,50" fill="#666"/>
  <text x="250" y="38" text-anchor="middle" font-size="10" fill="#888">logs appear on</text>

  
  <rect x="296" y="10" width="210" height="70" rx="6" fill="#f3faf6" stroke="#27795a" stroke-width="2"/>
  <text x="401" y="38" text-anchor="middle" font-size="13" font-weight="700" fill="#27795a">Analyze Rule</text>
  <text x="401" y="56" text-anchor="middle" font-size="13" font-weight="700" fill="#27795a">Processing Details</text>
</svg>
</div>

<p style="font-family:'Open Sans',sans-serif;font-size:15px;margin-bottom:18px;color:#666"><code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">ESS_LOG_WRITE</code> only works when the formula runs inside an ESS batch job — it stays silent on UI-triggered saves. Stick with <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">add_rlog</code> for universal coverage.</p>

<div style="border-left:4px solid #cf6e2c;background:#fff8f0;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#cf6e2c;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">⚠️ For those who used to query the table directly</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a">In earlier releases, consultants would query <code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">HWM_RULE_FF_WORK_LOG</code> via BI Publisher SQL data models as a debugging shortcut. From 2025 onward, Oracle has decommissioned this table — it is no longer reliably populated and is not exposed in OTBI. The <strong>Analyze Rule Processing Details</strong> UI page is the only supported path.</p>
</div>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">A Useful Convention: The <code style="font-size:16px">>>></code> Prefix</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">The rule processing log mixes Oracle's own engine messages with your custom lines. Prefix every message with <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">>>></code> so you can Ctrl+F straight to your lines and ignore the noise:</p>

<pre style="background:#fafafa;border-left:3px solid #c0392b;padding:16px 20px;margin:18px 0;font-family:Consolas,Monaco,monospace;font-size:13px;color:#2a2a2a;line-height:1.7;overflow-x:auto;white-space:pre-wrap">flog = add_log(ffs_id, '>>> Enter ' || ffName || ' v1.0')
flog = add_log(ffs_id, '>>> idx=' || to_char(nidx) || ' qty=' || to_char(aiMeasure))
flog = add_log(ffs_id, '>>> Exit ' || ffName)</pre>



<hr style="border:0;height:1px;background:#e0dcd6;margin:30px 0">

<h2 style="font-size:22px;font-weight:700;color:#1a1a1a;margin:28px 0 14px;font-family:'Open Sans',sans-serif">The Profile Option That Controls Everything</h2>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px">Until somebody flips this, every <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">add_log</code> call you wrote is the equivalent of waving at a camera nobody is recording.</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">ORA_HWM_RULES_LOG_LEVEL</h3>


<div style="background:#fafafa;border:1px solid #e0dcd6;border-radius:8px;padding:20px;margin:18px 0">
<svg viewBox="0 0 720 340" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;font-family:'Open Sans',sans-serif">
  
  <text x="360" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="#1a1a1a" font-family="Consolas,monospace">ORA_HWM_RULES_LOG_LEVEL</text>

  
  <text x="40" y="70" font-size="11" font-weight="700" fill="#27795a" letter-spacing="2">MORE</text>
  <line x1="55" y1="80" x2="55" y2="280" stroke="#cfc9c1" stroke-width="2"/>
  <polygon points="49,82 61,82 55,72" fill="#27795a"/>
  <polygon points="49,278 61,278 55,288" fill="#999"/>
  <text x="40" y="300" font-size="11" font-weight="700" fill="#999" letter-spacing="2">LESS</text>

  
  <rect x="100" y="60" width="500" height="50" rx="4" fill="#fdf3ef" stroke="#c0392b" stroke-width="2"/>
  <text x="120" y="80" font-size="14" font-weight="700" fill="#c0392b" font-family="Consolas,monospace">Finest</text>
  <text x="120" y="98" font-size="11" font-weight="700" fill="#c0392b">← use this for testing</text>
  
  <rect x="290" y="73" width="20" height="22" rx="2" fill="#c0392b"/>
  <rect x="315" y="73" width="20" height="22" rx="2" fill="#c0392b"/>
  <rect x="340" y="73" width="20" height="22" rx="2" fill="#c0392b"/>
  <rect x="365" y="73" width="20" height="22" rx="2" fill="#c0392b"/>
  <text x="410" y="89" font-size="12" fill="#3a3a3a">everything for every rule type</text>

  
  <rect x="100" y="120" width="500" height="50" rx="4" fill="#fff8f0" stroke="#cf6e2c" stroke-width="1.5"/>
  <text x="120" y="140" font-size="14" font-weight="700" fill="#cf6e2c" font-family="Consolas,monospace">Finer</text>
  <rect x="290" y="133" width="20" height="22" rx="2" fill="#cf6e2c"/>
  <rect x="315" y="133" width="20" height="22" rx="2" fill="#cf6e2c"/>
  <rect x="340" y="133" width="20" height="22" rx="2" fill="#cf6e2c"/>
  <rect x="365" y="133" width="20" height="22" rx="2" fill="#fff" stroke="#e0dcd6"/>
  <text x="410" y="149" font-size="12" fill="#3a3a3a">+ individual rule logs (TER and TCR)</text>

  
  <rect x="100" y="180" width="500" height="50" rx="4" fill="#faf5ec" stroke="#a07530" stroke-width="1.5"/>
  <text x="120" y="200" font-size="14" font-weight="700" fill="#a07530" font-family="Consolas,monospace">Fine</text>
  <rect x="290" y="193" width="20" height="22" rx="2" fill="#a07530"/>
  <rect x="315" y="193" width="20" height="22" rx="2" fill="#a07530"/>
  <rect x="340" y="193" width="20" height="22" rx="2" fill="#fff" stroke="#e0dcd6"/>
  <rect x="365" y="193" width="20" height="22" rx="2" fill="#fff" stroke="#e0dcd6"/>
  <text x="410" y="209" font-size="12" fill="#3a3a3a">rule set logs only</text>

  
  <rect x="100" y="240" width="500" height="50" rx="4" fill="#f8f5f1" stroke="#999" stroke-width="1.5"/>
  <text x="120" y="260" font-size="14" font-weight="700" fill="#666" font-family="Consolas,monospace">Incident</text>
  <text x="120" y="278" font-size="11" fill="#999">← default (almost nothing)</text>
  <rect x="290" y="253" width="20" height="22" rx="2" fill="#999"/>
  <rect x="315" y="253" width="20" height="22" rx="2" fill="#fff" stroke="#e0dcd6"/>
  <rect x="340" y="253" width="20" height="22" rx="2" fill="#fff" stroke="#e0dcd6"/>
  <rect x="365" y="253" width="20" height="22" rx="2" fill="#fff" stroke="#e0dcd6"/>
  <text x="410" y="269" font-size="12" fill="#3a3a3a">only when processing fails</text>

  
  <text x="335" y="312" text-anchor="middle" font-size="10" fill="#7f8c8d" font-style="italic">retention level</text>
  <text x="500" y="312" text-anchor="middle" font-size="10" fill="#7f8c8d" font-style="italic">what gets kept in the log</text>
</svg>
</div>
<p style="font-family:'Open Sans',sans-serif;text-align:center;font-size:13px;color:#7f8c8d;font-style:italic;margin:-4px 0 24px">Fig 7 — At the default <strong>Incident</strong> level, the engine throws away almost everything. <strong>Finest</strong> keeps the full trace — what you want during testing.</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;border:2px solid #1a1a1a;overflow:hidden">
  <tr><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:20%">Level</th><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase">What Gets Kept</th></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Incident</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px"><strong>Default.</strong> Keeps logs only when processing fails. Successful runs leave no trace.</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Fine</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Keeps rule set logs (TCR and entry rule sets). No individual rule logs.</td></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Finer</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Adds individual rule logs for time calculation and entry rules.</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px;font-weight:600;color:#c0392b">Finest ← use this</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px"><strong>Keeps everything for every rule type.</strong> This is what you want during testing.</td></tr>
</table>

<div style="border-left:4px solid #27795a;background:#f3faf6;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#27795a;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">✅ How to flip the dial</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a">Setup and Maintenance → search "Manage Administrator Profile Values" → search profile code <code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">ORA_HWM_RULES_LOG</code> → set <code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">ORA_HWM_RULES_LOG_LEVEL</code> to <strong>Finest</strong> at Site level → also set <code style="background:#f0ece6;padding:2px 6px;border-radius:3px;font-size:13px;color:#c0392b">ORA_HWM_RULES_LOG_MONTHS_TO_KEEP</code> to <strong>1</strong> at Site level → Save and Close → <strong>sign out completely and sign back in</strong>.</p>
</div>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">Data Role and Security Profile</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">Setting the profile is necessary but not enough. The user viewing Analyze Rule Processing Details also needs a data role: <strong>Time and Labor Administrator</strong> job role, with security profiles for View All Organizations, View All Positions, View All LDGs, and <strong>View All People</strong> (not "View All Workers" — that is different).</p>

<div style="border-left:4px solid #cf6e2c;background:#fff8f0;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#cf6e2c;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">📌 MOS Doc 2120220.1</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a">If the profile is Finest, the formula compiles, the chain is intact, and you still see "No data to display" — the cause is almost always the data role gap. Oracle MOS Doc <strong>2120220.1</strong> documents this exact situation.</p>
</div>



<hr style="border:0;height:1px;background:#e0dcd6;margin:30px 0">

<h2 style="font-size:22px;font-weight:700;color:#1a1a1a;margin:28px 0 14px;font-family:'Open Sans',sans-serif">Framework of the Code — TER Skeletons</h2>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px">Two skeletons below. The first is a <strong>minimal logging-only TER</strong> — drop it in to confirm your setup chain works. The second is the <strong>production skeleton</strong> with all the guards. Between them, the <em>Day vs Time Card Summation</em> section explains what changes in the code depending on whether you chose Day or Time Card summation.</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">Minimal TER Logging Skeleton</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">The smallest TER formula that produces useful logs. Deploy this first after enabling <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">ORA_HWM_RULES_LOG_LEVEL = Finest</code>. If you save a timecard and see these lines on Analyze Rule Processing Details, every link in the chain is working.</p>

<pre style="background:#fafafa;border-left:3px solid #c0392b;padding:16px 20px;margin:18px 0;font-family:Consolas,Monaco,monospace;font-size:13px;color:#2a2a2a;line-height:1.7;overflow-x:auto;white-space:pre-wrap"><span style="color:#800000;font-style:italic">/******************************************************************
  FORMULA: MY_TER_LOG_TEST
  TYPE   : Time Entry Rule
  PURPOSE: Smallest TER that produces useful logs.
           Deploy this first to confirm logging works end-to-end.
******************************************************************/</span>

<span style="color:#2a2a2a">DEFAULT FOR</span> HWM_CTXARY_RECORD_POSITIONS <span style="color:#2a2a2a">IS</span> EMPTY_TEXT_NUMBER
<span style="color:#2a2a2a">DEFAULT FOR</span> measure                     <span style="color:#2a2a2a">IS</span> EMPTY_NUMBER_NUMBER
<span style="color:#2a2a2a">DEFAULT FOR</span> PayrollTimeType             <span style="color:#2a2a2a">IS</span> EMPTY_TEXT_NUMBER

<span style="color:#2a2a2a">INPUTS ARE</span>
  HWM_CTXARY_RECORD_POSITIONS,
  measure, PayrollTimeType

ffName  = <span style="color:#2a2a2a">'MY_TER_LOG_TEST'</span>
ffs_id  = <span style="color:#2a2a2a">GET_CONTEXT</span>(HWM_FFS_ID, 0)
rule_id = <span style="color:#2a2a2a">GET_CONTEXT</span>(HWM_RULE_ID, 0)
asg_id  = <span style="color:#2a2a2a">GET_CONTEXT</span>(HWM_SUBRESOURCE_ID, 0)

flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> Enter '</span> || ffName)
flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> ffs_id='</span> || <span style="color:#2a2a2a">to_char</span>(ffs_id))
flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> rule_id='</span> || <span style="color:#2a2a2a">to_char</span>(rule_id))

<span style="color:#2a2a2a">CHANGE_CONTEXTS</span>(HR_ASSIGNMENT_ID = asg_id)
(
  wMaAry = HWM_CTXARY_RECORD_POSITIONS.count
  flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> Total rows: '</span> || <span style="color:#2a2a2a">to_char</span>(wMaAry))

  nidx = 0
  <span style="color:#2a2a2a">WHILE</span> (nidx < wMaAry) <span style="color:#2a2a2a">LOOP</span>
  (
    nidx = nidx + 1
    aiRecPos = HWM_CTXARY_RECORD_POSITIONS[nidx]
    aiType   = <span style="color:#2a2a2a">'**NULL**'</span>
    <span style="color:#2a2a2a">IF</span> (PayrollTimeType.exists(nidx)) <span style="color:#2a2a2a">THEN</span>  aiType = PayrollTimeType[nidx]

    flog = <span style="color:#2a2a2a">add_log</span>(ffs_id,
             <span style="color:#2a2a2a">'>>> idx='</span> || <span style="color:#2a2a2a">to_char</span>(nidx) ||
             <span style="color:#2a2a2a">' pos='</span>   || aiRecPos ||
             <span style="color:#2a2a2a">' type=['</span> || aiType || <span style="color:#2a2a2a">']'</span>)
  )
)

flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> Exit '</span> || ffName)
<span style="color:#2a2a2a">RETURN</span> OUT_MSG</pre>

<div style="border-left:4px solid #c0392b;background:#fff7f5;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#c0392b;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">💡 What you should see</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a"><code style="font-size:13px">>>> Enter MY_TER_LOG_TEST</code>, the two context IDs as non-zero numbers, the row count, one <code style="font-size:13px">>>> idx=</code> line per timecard entry, and <code style="font-size:13px">>>> Exit MY_TER_LOG_TEST</code>. If anything is missing, walk the checklist in the <em>30-Second Checklist</em> below.</p>
</div>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">What Changes in the Code: Day vs Time Card Summation</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">The Summation Level you set on the rule template changes <em>what the engine sends</em> to the formula. The code must be written differently depending on which one you pick.</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;border:2px solid #1a1a1a;overflow:hidden">
  <tr><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:30%">Aspect</th><th style="font-family:'Open Sans',sans-serif;background:#2e6b9e;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:35%">Day Summation</th><th style="font-family:'Open Sans',sans-serif;background:#c0392b;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase">Time Card Summation</th></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">When formula is called</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Once per day</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Once for the entire period</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Array contains</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">DETAIL rows + END_DAY</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">DETAIL rows + END_DAY per day + END_PERIOD at the end</td></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">Day-level state reset?</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;color:#27795a;font-weight:600">No — formula starts fresh each call</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;color:#c0392b;font-weight:600">Yes — clear at END_DAY or Monday leaks into Tuesday</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:600">END_PERIOD handling?</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;color:#27795a;font-weight:600">Not needed — no END_PERIOD marker</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;color:#c0392b;font-weight:600">Yes — run period-level checks here</td></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px;font-weight:600">Cross-day totals (weekly max)?</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px">Not possible (no memory between calls)</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px;color:#27795a;font-weight:600">Built in — running totals accumulate naturally</td></tr>
</table>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px"><strong>Day Summation</strong> — the simpler pattern. No manual state reset needed, no END_PERIOD handler. Good for overlap, continuous stretch, meal break, daily max checks:</p>

<pre style="background:#fafafa;border-left:3px solid #c0392b;padding:16px 20px;margin:18px 0;font-family:Consolas,Monaco,monospace;font-size:13px;color:#2a2a2a;line-height:1.7;overflow-x:auto;white-space:pre-wrap"><span style="color:#800000;font-style:italic">/* ═══ DAY SUMMATION — simpler pattern ═══
   Engine calls once per day.
   Array = DETAIL rows for one day + END_DAY.
   No END_PERIOD. State resets between calls. */</span>

<span style="color:#2a2a2a">WHILE</span> (nidx < wMaAry) <span style="color:#2a2a2a">LOOP</span>
(
  nidx = nidx + 1
  aiRecPos = HWM_CTXARY_RECORD_POSITIONS[nidx]

  <span style="color:#2a2a2a">IF</span> (aiRecPos = <span style="color:#2a2a2a">'DETAIL'</span>) <span style="color:#2a2a2a">THEN</span>
  (
    <span style="color:#800000;font-style:italic">/* Read entry data, log it, business logic */</span>
    flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> idx='</span> || <span style="color:#2a2a2a">to_char</span>(nidx) || <span style="color:#2a2a2a">' type=['</span> || aiType || <span style="color:#2a2a2a">']'</span>)
  )

  <span style="color:#2a2a2a">IF</span> (aiRecPos = <span style="color:#2a2a2a">'END_DAY'</span>) <span style="color:#2a2a2a">THEN</span>
  (
    <span style="color:#800000;font-style:italic">/* Run day-level checks (overlap, daily total) */</span>
    flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> END_DAY checks done'</span>)
    <span style="color:#800000;font-style:italic">/* No state reset needed — next call starts fresh */</span>
  )
)</pre>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px"><strong>Time Card Summation</strong> — adds two extra blocks (marked with ★):</p>

<pre style="background:#fafafa;border-left:3px solid #c0392b;padding:16px 20px;margin:18px 0;font-family:Consolas,Monaco,monospace;font-size:13px;color:#2a2a2a;line-height:1.7;overflow-x:auto;white-space:pre-wrap"><span style="color:#800000;font-style:italic">/* ═══ TIME CARD SUMMATION — fuller pattern ═══
   Engine calls once for the entire period.
   Array = DETAIL rows + END_DAY per day + END_PERIOD at the end. */</span>

<span style="color:#2a2a2a">WHILE</span> (nidx < wMaAry) <span style="color:#2a2a2a">LOOP</span>
(
  nidx = nidx + 1
  aiRecPos = HWM_CTXARY_RECORD_POSITIONS[nidx]

  <span style="color:#2a2a2a">IF</span> (aiRecPos = <span style="color:#2a2a2a">'DETAIL'</span>) <span style="color:#2a2a2a">THEN</span>
  (
    <span style="color:#800000;font-style:italic">/* Same as Day pattern — read, log, business logic */</span>
    flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> idx='</span> || <span style="color:#2a2a2a">to_char</span>(nidx) || <span style="color:#2a2a2a">' type=['</span> || aiType || <span style="color:#2a2a2a">']'</span>)
    l_week_total = l_week_total + aiMeasure
  )

  <span style="color:#2a2a2a">IF</span> (aiRecPos = <span style="color:#2a2a2a">'END_DAY'</span>) <span style="color:#2a2a2a">THEN</span>
  (
    <span style="color:#800000;font-style:italic">/* Run day-level checks — same as Day pattern */</span>

    <span style="color:#800000;font-style:italic">/* ★ EXTRA 1: Manual state reset — without this Monday leaks into Tuesday */</span>
    l_day_total     = 0
    l_stretch_start = NullDate
    l_stretch_end   = NullDate
    l_in_stretch    = <span style="color:#2a2a2a">'N'</span>
    l_day_count     = 0
    flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> END_DAY reset done'</span>)
  )

  <span style="color:#800000;font-style:italic">/* ★ EXTRA 2: END_PERIOD — period-level final checks */</span>
  <span style="color:#2a2a2a">IF</span> (aiRecPos = <span style="color:#2a2a2a">'END_PERIOD'</span>) <span style="color:#2a2a2a">THEN</span>
  (
    <span style="color:#2a2a2a">IF</span> (l_week_total > l_weekly_max) <span style="color:#2a2a2a">THEN</span>
    (
      OUT_MSG[nidx] = <span style="color:#2a2a2a">'Weekly hours exceed maximum'</span>
    )
    flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> END_PERIOD weekTotal='</span> || <span style="color:#2a2a2a">to_char</span>(l_week_total))
  )
)</pre>

<div style="border-left:4px solid #c0392b;background:#fff7f5;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#c0392b;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">📌 Summary of the two extras</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a">Time Card adds exactly two code blocks Day does not need: <strong>★ EXTRA 1</strong> — Manual state reset inside END_DAY (so Monday's totals don't leak into Tuesday). <strong>★ EXTRA 2</strong> — END_PERIOD handler for period-level checks. The DETAIL processing is identical between the two. Start with Day, add these two if you later switch to Time Card.</p>
</div>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">Production-Ready Skeleton</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">Once logging works, build on this. It adds runaway-loop protection, header-attribute readback, parameter logging, and explicit business-logic placement. The formula name (<code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">MY_TER_FORMULA</code>) and parameter names are placeholders — replace them. Oracle-defined names (<code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">HWM_FFS_ID</code>, <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">OUT_MSG</code>, etc.) must stay exactly as shown.</p>

<pre style="background:#fafafa;border-left:3px solid #c0392b;padding:16px 20px;margin:18px 0;font-family:Consolas,Monaco,monospace;font-size:13px;color:#2a2a2a;line-height:1.7;overflow-x:auto;white-space:pre-wrap"><span style="color:#800000;font-style:italic">/* A. DEFAULTS — array types matching the template contract */</span>
<span style="color:#2a2a2a">DEFAULT FOR</span> HWM_CTXARY_RECORD_POSITIONS <span style="color:#2a2a2a">IS</span> EMPTY_TEXT_NUMBER
<span style="color:#2a2a2a">DEFAULT FOR</span> HWM_CTXARY_HWM_MEASURE_DAY  <span style="color:#2a2a2a">IS</span> EMPTY_NUMBER_NUMBER
<span style="color:#2a2a2a">DEFAULT FOR</span> measure                     <span style="color:#2a2a2a">IS</span> EMPTY_NUMBER_NUMBER
<span style="color:#2a2a2a">DEFAULT FOR</span> PayrollTimeType             <span style="color:#2a2a2a">IS</span> EMPTY_TEXT_NUMBER
<span style="color:#2a2a2a">DEFAULT FOR</span> StartTime                   <span style="color:#2a2a2a">IS</span> EMPTY_DATE_NUMBER
<span style="color:#2a2a2a">DEFAULT FOR</span> StopTime                    <span style="color:#2a2a2a">IS</span> EMPTY_DATE_NUMBER

<span style="color:#2a2a2a">INPUTS ARE</span>
  HWM_CTXARY_RECORD_POSITIONS, HWM_CTXARY_HWM_MEASURE_DAY,
  measure, PayrollTimeType, StartTime, StopTime

<span style="color:#800000;font-style:italic">/* B. CONTEXT INIT */</span>
ffName  = <span style="color:#2a2a2a">'MY_TER_FORMULA'</span>
ffs_id  = <span style="color:#2a2a2a">GET_CONTEXT</span>(HWM_FFS_ID, 0)
rule_id = <span style="color:#2a2a2a">GET_CONTEXT</span>(HWM_RULE_ID, 0)
asg_id  = <span style="color:#2a2a2a">GET_CONTEXT</span>(HWM_SUBRESOURCE_ID, 0)
NullDate = <span style="color:#2a2a2a">'01-JAN-1900'</span>(DATE)
NullText = <span style="color:#2a2a2a">'**FF_NULL**'</span>

<span style="color:#800000;font-style:italic">/* C. ENTRY MARKER */</span>
flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> Enter '</span> || ffName || <span style="color:#2a2a2a">' v1.0'</span>)
flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> ffs_id='</span> || <span style="color:#2a2a2a">to_char</span>(ffs_id) || <span style="color:#2a2a2a">' rule_id='</span> || <span style="color:#2a2a2a">to_char</span>(rule_id))

<span style="color:#800000;font-style:italic">/* D. ASSIGNMENT CONTEXT WRAPPER */</span>
<span style="color:#2a2a2a">CHANGE_CONTEXTS</span>(HR_ASSIGNMENT_ID = asg_id)
(
  <span style="color:#800000;font-style:italic">/* E. Read & log header attributes */</span>
  rptLvl = <span style="color:#2a2a2a">Get_Hdr_Text</span>(rule_id, <span style="color:#2a2a2a">'RUN_TBB_LEVEL'</span>, <span style="color:#2a2a2a">'DAY'</span>)
  flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> rptLvl='</span> || rptLvl)

  <span style="color:#800000;font-style:italic">/* F. Read rule parameters & log them */</span>
  p_sched_start = <span style="color:#2a2a2a">get_rvalue_number</span>(rule_id, <span style="color:#2a2a2a">'SCHEDULE_START_HOUR'</span>, 0)
  p_sched_end   = <span style="color:#2a2a2a">get_rvalue_number</span>(rule_id, <span style="color:#2a2a2a">'SCHEDULE_END_HOUR'</span>,   0)
  flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> sched='</span> || <span style="color:#2a2a2a">to_char</span>(p_sched_start) || <span style="color:#2a2a2a">'-'</span> || <span style="color:#2a2a2a">to_char</span>(p_sched_end))

  <span style="color:#800000;font-style:italic">/* G. Loop with guards */</span>
  nidx   = 0
  wMaAry = HWM_CTXARY_RECORD_POSITIONS.count
  flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> Total rows: '</span> || <span style="color:#2a2a2a">to_char</span>(wMaAry))

  <span style="color:#2a2a2a">WHILE</span> (nidx < wMaAry) <span style="color:#2a2a2a">LOOP</span>
  (
    nidx = nidx + 1
    <span style="color:#2a2a2a">IF</span> (nidx > 1000) <span style="color:#2a2a2a">THEN</span> ( flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> ABORT runaway'</span>)  <span style="color:#2a2a2a">RETURN</span> OUT_MSG )

    aiRecPos = HWM_CTXARY_RECORD_POSITIONS[nidx]

    <span style="color:#2a2a2a">IF</span> (aiRecPos = <span style="color:#2a2a2a">'DETAIL'</span>) <span style="color:#2a2a2a">THEN</span>
    (
      aiMeasure = 0
      aiType    = NullText
      <span style="color:#2a2a2a">IF</span> (measure.exists(nidx))         <span style="color:#2a2a2a">THEN</span>  aiMeasure = measure[nidx]
      <span style="color:#2a2a2a">IF</span> (PayrollTimeType.exists(nidx)) <span style="color:#2a2a2a">THEN</span>  aiType    = PayrollTimeType[nidx]

      flog = <span style="color:#2a2a2a">add_log</span>(ffs_id,
               <span style="color:#2a2a2a">'>>> idx='</span> || <span style="color:#2a2a2a">to_char</span>(nidx) || <span style="color:#2a2a2a">' pos='</span> || aiRecPos ||
               <span style="color:#2a2a2a">' type=['</span> || aiType || <span style="color:#2a2a2a">']'</span> || <span style="color:#2a2a2a">' qty='</span> || <span style="color:#2a2a2a">to_char</span>(aiMeasure))

      <span style="color:#800000;font-style:italic">/* === Your business logic goes here === */</span>
    )
    <span style="color:#2a2a2a">IF</span> (aiRecPos = <span style="color:#2a2a2a">'END_DAY'</span>) <span style="color:#2a2a2a">THEN</span>
    (  flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> END_DAY checks here'</span>)  )
    <span style="color:#2a2a2a">IF</span> (aiRecPos = <span style="color:#2a2a2a">'END_PERIOD'</span>) <span style="color:#2a2a2a">THEN</span>
    (  flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> END_PERIOD checks here'</span>)  )
  )
)

<span style="color:#800000;font-style:italic">/* H. EXIT MARKER */</span>
flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> Exit '</span> || ffName)
<span style="color:#2a2a2a">RETURN</span> OUT_MSG</pre>



<hr style="border:0;height:1px;background:#e0dcd6;margin:30px 0">

<h2 style="font-size:22px;font-weight:700;color:#1a1a1a;margin:28px 0 14px;font-family:'Open Sans',sans-serif">Framework of the Code — TCR Skeletons</h2>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px">TCR formulas calculate or reclassify hours — they do not validate. The structure depends on the <strong>Summation Level</strong> you chose on the template. At <strong>Details</strong> level (the most common for TCR), the engine calls your formula once per matched time entry row, passing <em>scalar</em> values — not arrays. That makes TCR formulas shorter than TER formulas.</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">Minimal TCR Logging Skeleton</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">The smallest TCR formula that logs the incoming time entry. Deploy this first to confirm your TCR setup chain works. It creates no new entries — it just logs and exits.</p>

<pre style="background:#fafafa;border-left:3px solid #c0392b;padding:16px 20px;margin:18px 0;font-family:Consolas,Monaco,monospace;font-size:13px;color:#2a2a2a;line-height:1.7;overflow-x:auto;white-space:pre-wrap"><span style="color:#800000;font-style:italic">/******************************************************************
  FORMULA: MY_TCR_LOG_TEST
  TYPE   : Time Calculation Rule (Create · Details)
  PURPOSE: Smallest TCR that produces useful logs.
           Creates nothing — just confirms the engine calls it.
******************************************************************/</span>

<span style="color:#2a2a2a">DEFAULT FOR</span> measure         <span style="color:#2a2a2a">IS</span> <span style="color:#2a2a2a">0</span>
<span style="color:#2a2a2a">DEFAULT FOR</span> PayrollTimeType <span style="color:#2a2a2a">IS</span> <span style="color:#2a2a2a">' '</span>
<span style="color:#2a2a2a">DEFAULT FOR</span> StartTime       <span style="color:#2a2a2a">IS</span> <span style="color:#2a2a2a">'01-JAN-1900 00:00:00'</span>(DATE)
<span style="color:#2a2a2a">DEFAULT FOR</span> StopTime        <span style="color:#2a2a2a">IS</span> <span style="color:#2a2a2a">'01-JAN-1900 00:00:00'</span>(DATE)

<span style="color:#2a2a2a">INPUTS ARE</span>
  measure, PayrollTimeType, StartTime, StopTime

ffName  = <span style="color:#2a2a2a">'MY_TCR_LOG_TEST'</span>
ffs_id  = <span style="color:#2a2a2a">GET_CONTEXT</span>(HWM_FFS_ID, 0)
rule_id = <span style="color:#2a2a2a">GET_CONTEXT</span>(HWM_RULE_ID, 0)

flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> Enter '</span> || ffName)
flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> measure='</span> || <span style="color:#2a2a2a">to_char</span>(measure))
flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> type='</span> || PayrollTimeType)
flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> start='</span> || <span style="color:#2a2a2a">to_char</span>(StartTime, <span style="color:#2a2a2a">'DD-MON-YYYY HH24:MI'</span>))
flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> stop='</span> || <span style="color:#2a2a2a">to_char</span>(StopTime, <span style="color:#2a2a2a">'DD-MON-YYYY HH24:MI'</span>))

<span style="color:#800000;font-style:italic">/* No calculation — just logging to confirm the formula fires */</span>

flog = <span style="color:#2a2a2a">add_log</span>(ffs_id, <span style="color:#2a2a2a">'>>> Exit '</span> || ffName)
<span style="color:#2a2a2a">RETURN</span></pre>

<div style="border-left:4px solid #c0392b;background:#fff7f5;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#c0392b;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">💡 What you should see</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a"><code style="font-size:13px">>>> Enter MY_TCR_LOG_TEST</code>, the measure value (hours), payroll time type, start/stop timestamps, and <code style="font-size:13px">>>> Exit MY_TCR_LOG_TEST</code>. One set of lines per matched time entry row. If you see nothing, walk the <em>30-Second Checklist</em> below.</p>
</div>

<div style="border-left:4px solid #2e6b9e;background:#f2f6fa;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#2e6b9e;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">📌 TER vs TCR — key structural difference</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a"><strong>TER</strong> receives arrays (<code style="font-size:13px">HWM_CTXARY_RECORD_POSITIONS</code>, <code style="font-size:13px">measure[]</code>) and loops through them. <strong>TCR at Details level</strong> receives scalar values (<code style="font-size:13px">measure</code>, <code style="font-size:13px">PayrollTimeType</code>) — no loop needed. The engine calls the formula once per matched row and passes one row's worth of data each time.</p>
</div>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">Production-Ready TCR Skeleton (Create · Threshold)</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">A full TCR skeleton with array defaults, header-level rule reads, execution-type guard, null-safe checks, and a two-row output split. The formula name (<code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">XX_GENERIC_TCR_SKELETON</code>) and parameter names are placeholders — replace them with your own.</p>

<pre style="background:#fafafa;border-left:3px solid #c0392b;padding:16px 20px;margin:18px 0;font-family:Consolas,Monaco,monospace;font-size:13px;color:#2a2a2a;line-height:1.7;overflow-x:auto;white-space:pre-wrap"><span style="color:#800000;font-style:italic">/* A. DEFAULTS */</span>
<span style="color:#2a2a2a">DEFAULT FOR</span> HWM_CTXARY_RECORD_POSITIONS  <span style="color:#2a2a2a">IS</span> EMPTY_TEXT_NUMBER
<span style="color:#2a2a2a">DEFAULT FOR</span> HWM_CTXARY_HWM_MEASURE_DAY   <span style="color:#2a2a2a">IS</span> EMPTY_NUMBER_NUMBER

<span style="color:#2a2a2a">DEFAULT FOR</span> MEASURE                      <span style="color:#2a2a2a">IS</span> EMPTY_NUMBER_NUMBER
<span style="color:#2a2a2a">DEFAULT FOR</span> PayrollTimeType              <span style="color:#2a2a2a">IS</span> EMPTY_TEXT_NUMBER
<span style="color:#2a2a2a">DEFAULT FOR</span> StartTime                    <span style="color:#2a2a2a">IS</span> EMPTY_DATE_NUMBER
<span style="color:#2a2a2a">DEFAULT FOR</span> StopTime                     <span style="color:#2a2a2a">IS</span> EMPTY_DATE_NUMBER

<span style="color:#800000;font-style:italic">/* B. INPUTS */</span>
<span style="color:#2a2a2a">INPUTS ARE</span>
    HWM_CTXARY_RECORD_POSITIONS,
    HWM_CTXARY_HWM_MEASURE_DAY,
    MEASURE,
    PayrollTimeType,
    StartTime,
    StopTime

<span style="color:#800000;font-style:italic">/* C. CONTEXT INIT + NULL GUARDS */</span>
ffName        = <span style="color:#2a2a2a">'XX_GENERIC_TCR_SKELETON'</span>
ffs_id        = <span style="color:#2a2a2a">GET_CONTEXT</span>(HWM_FFS_ID,  0)
rule_id       = <span style="color:#2a2a2a">GET_CONTEXT</span>(HWM_RULE_ID, 0)

NullDate      = <span style="color:#2a2a2a">'01-JAN-1900'</span>(DATE)
NullDateTime  = <span style="color:#2a2a2a">'1900/01/01 00:00:00'</span>(DATE)
NullText      = <span style="color:#2a2a2a">'**FF_NULL**'</span>

<span style="color:#800000;font-style:italic">/* D. HEADER-LEVEL RULE READS */</span>
l_hdr_sum_lvl   = <span style="color:#2a2a2a">Get_Hdr_Text</span>(rule_id, <span style="color:#2a2a2a">'RUN_SUMMATION_LEVEL'</span>, <span style="color:#2a2a2a">'TIMECARD'</span>)
l_hdr_ExecType  = <span style="color:#2a2a2a">Get_Hdr_Text</span>(rule_id, <span style="color:#2a2a2a">'RULE_EXEC_TYPE'</span>,      <span style="color:#2a2a2a">'CREATE'</span>)

flog = <span style="color:#2a2a2a">ADD_RLOG</span>(ffs_id, <span style="color:#2a2a2a">'>>> Enter '</span> || ffName || <span style="color:#2a2a2a">' v1.0'</span>)
flog = <span style="color:#2a2a2a">ADD_RLOG</span>(ffs_id, <span style="color:#2a2a2a">'>>> ExecType='</span> || l_hdr_ExecType ||
                         <span style="color:#2a2a2a">' SumLvl='</span> || l_hdr_sum_lvl)

<span style="color:#800000;font-style:italic">/* Only proceed on CREATE pass — skip VALIDATE to avoid duplicates */</span>
<span style="color:#2a2a2a">IF</span> (l_hdr_ExecType = <span style="color:#2a2a2a">'CREATE'</span>) <span style="color:#2a2a2a">THEN</span>
(
  <span style="color:#800000;font-style:italic">/* E. READ RULE PARAMETERS */</span>
  p_threshold = <span style="color:#2a2a2a">GET_RVALUE_NUMBER</span>(rule_id, <span style="color:#2a2a2a">'DAILY_THRESHOLD'</span>,        <span style="color:#2a2a2a">0</span>)
  p_ot_type   = <span style="color:#2a2a2a">GET_RVALUE_TEXT</span>  (rule_id, <span style="color:#2a2a2a">'OT_PAYROLL_TIME_TYPE'</span>, <span style="color:#2a2a2a">' '</span>)

  flog = <span style="color:#2a2a2a">ADD_RLOG</span>(ffs_id, <span style="color:#2a2a2a">'>>> threshold='</span> || <span style="color:#2a2a2a">TO_CHAR</span>(p_threshold) ||
                           <span style="color:#2a2a2a">' ot_type='</span>     || p_ot_type)

  <span style="color:#800000;font-style:italic">/* F. PROCESS CURRENT MEASURE */</span>
  flog = <span style="color:#2a2a2a">ADD_RLOG</span>(ffs_id, <span style="color:#2a2a2a">'>>> measure='</span> || <span style="color:#2a2a2a">TO_CHAR</span>(MEASURE) ||
                           <span style="color:#2a2a2a">' type='</span>      || PayrollTimeType)

  <span style="color:#2a2a2a">IF</span> (MEASURE <span style="color:#2a2a2a">WAS NOT DEFAULTED</span> <span style="color:#2a2a2a">AND</span> PayrollTimeType <> NullText) <span style="color:#2a2a2a">THEN</span>
  (
    l_excess = MEASURE - p_threshold

    <span style="color:#2a2a2a">IF</span> (l_excess > <span style="color:#2a2a2a">0</span>) <span style="color:#2a2a2a">THEN</span>
    (
      flog = <span style="color:#2a2a2a">ADD_RLOG</span>(ffs_id, <span style="color:#2a2a2a">'>>> SPLIT: reg='</span> || <span style="color:#2a2a2a">TO_CHAR</span>(p_threshold) ||
                               <span style="color:#2a2a2a">' ot='</span> || <span style="color:#2a2a2a">TO_CHAR</span>(l_excess))

      <span style="color:#800000;font-style:italic">/* Row 1 — regular hours capped at threshold */</span>
      out_measure[1]         = p_threshold
      out_PayrollTimeType[1] = PayrollTimeType
      out_StartTime[1]       = StartTime
      out_StopTime[1]        = StopTime

      <span style="color:#800000;font-style:italic">/* Row 2 — overtime hours */</span>
      out_measure[2]         = l_excess
      out_PayrollTimeType[2] = p_ot_type
      out_StartTime[2]       = StartTime
      out_StopTime[2]        = StopTime
    )
    <span style="color:#2a2a2a">ELSE</span>
    (
      flog = <span style="color:#2a2a2a">ADD_RLOG</span>(ffs_id, <span style="color:#2a2a2a">'>>> PASSTHROUGH: measure <= threshold'</span>)

      out_measure[1]         = MEASURE
      out_PayrollTimeType[1] = PayrollTimeType
      out_StartTime[1]       = StartTime
      out_StopTime[1]        = StopTime
    )
  )
  <span style="color:#2a2a2a">ELSE</span>
  (
    flog = <span style="color:#2a2a2a">ADD_RLOG</span>(ffs_id, <span style="color:#2a2a2a">'>>> SKIP: null measure or type'</span>)
  )
)
<span style="color:#2a2a2a">ELSE</span>
(
  flog = <span style="color:#2a2a2a">ADD_RLOG</span>(ffs_id, <span style="color:#2a2a2a">'>>> Skipping — ExecType='</span> || l_hdr_ExecType)
)

<span style="color:#800000;font-style:italic">/* G. EXIT */</span>
flog = <span style="color:#2a2a2a">ADD_RLOG</span>(ffs_id, <span style="color:#2a2a2a">'>>> Exit '</span> || ffName)

<span style="color:#2a2a2a">RETURN</span> out_measure,
       out_PayrollTimeType,
       out_StartTime,
       out_StopTime</pre>

<div style="border-left:4px solid #27795a;background:#f3faf6;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0">
  <div style="font-family:'Open Sans',sans-serif;font-size:13px;font-weight:700;color:#27795a;letter-spacing:1px;margin-bottom:6px;text-transform:uppercase">✅ What this skeleton covers</div>
  <p style="font-family:'Open Sans',sans-serif;margin:0;font-size:15px;color:#3a3a3a"><strong>Execution-type guard</strong> — only runs on the CREATE pass, skips VALIDATE to avoid duplicate entries. <strong>WAS NOT DEFAULTED</strong> — null-safe check so the formula doesn't process empty rows. <strong>Two-row output</strong> — Row 1 caps regular hours at the threshold, Row 2 holds the overtime excess. If hours are under the threshold, the formula passes through a single row unchanged. Every decision is logged with <code style="font-size:13px">ADD_RLOG</code> so you can trace exactly which branch fired.</p>
</div>



<hr style="border:0;height:1px;background:#e0dcd6;margin:30px 0">

<h2 style="font-size:22px;font-weight:700;color:#1a1a1a;margin:28px 0 14px;font-family:'Open Sans',sans-serif">Summary — Where the Logs Land and How to Read Them</h2>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">Viewing the Logs (UI)</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px"><strong>1.</strong> My Client Groups → Time Management → Tasks panel → <strong>Analyze Rule Processing Details</strong> → <strong>2.</strong> Search by employee or rule set name + timecard date range → <strong>3.</strong> Click the most recent processing run row → <strong>4.</strong> In Processing Results, click <strong>Rule Processing Log</strong> → search for your <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">>>></code> prefix.</p>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">Sample Log Output</h3>

<pre style="background:#fafafa;border-left:3px solid #c0392b;padding:16px 20px;margin:18px 0;font-family:Consolas,Monaco,monospace;font-size:13px;color:#2a2a2a;line-height:1.7;overflow-x:auto;white-space:pre-wrap">>>> Enter MY_TER_FORMULA v1.0
>>> ffs_id=<session_id> rule_id=<rule_id>
>>> rptLvl=DAY
>>> Total rows: 3
>>> idx=1 pos=DETAIL   type=[Regular Hours] qty=<hours>
>>> idx=2 pos=DETAIL   type=[Meal Break]    qty=<hours>
>>> idx=3 pos=END_DAY  type=[**FF_NULL**]   qty=0
>>> Exit MY_TER_FORMULA</pre>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">The Forced-Error Trick</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">If you have done everything right and still see nothing, you can push diagnostic data straight into the validation message that surfaces on the timecard. The exact output variable name (<code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">OUT_MSG</code> in the example below) varies by template — some Oracle samples use <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">out_msg_ary</code>. Check your template's output spec before borrowing the snippet:</p>

<pre style="background:#fafafa;border-left:3px solid #c0392b;padding:16px 20px;margin:18px 0;font-family:Consolas,Monaco,monospace;font-size:13px;color:#2a2a2a;line-height:1.7;overflow-x:auto;white-space:pre-wrap"><span style="color:#800000;font-style:italic">/* DEBUG MODE — push diagnostic payload into the user-facing message */</span>
OUT_MSG[1] = <span style="color:#2a2a2a">'DEBUG: idx=1 type='</span> || aiType || <span style="color:#2a2a2a">' qty='</span> || <span style="color:#2a2a2a">to_char</span>(aiMeasure)
<span style="color:#2a2a2a">RETURN</span> OUT_MSG</pre>

<div style="background:#fff8f0;border-left:4px solid #cf6e2c;padding:14px 18px;margin:20px 0;border-radius:0 6px 6px 0;font-family:'Open Sans',sans-serif">
  <p style="margin:0;font-size:15px;color:#3a3a3a;font-style:italic;font-family:'Open Sans',sans-serif">Your future self will thank you for removing this before UAT. <span style="font-weight:700;color:#c0392b;font-style:normal">Your functional lead will not thank you if you don't.</span></p>
</div>

<h3 style="font-family:'Open Sans',sans-serif;font-size:18px;font-weight:700;color:#c0392b;margin:24px 0 12px">The 30-Second Checklist</h3>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:12px">If logs do not appear, walk these in order:</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;border:2px solid #1a1a1a;overflow:hidden">
  <tr><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:8%">#</th><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase;width:48%">Check</th><th style="font-family:'Open Sans',sans-serif;background:#1a1a1a;color:#fff;padding:10px 14px;font-size:12px;font-weight:700;letter-spacing:1px;text-align:left;text-transform:uppercase">Where</th></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:700">1</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">TCR template — Execution Type + Summation Level correct</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-style:italic;color:#666">Manage Time Rule Templates → TCR template</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:700">2</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">TER template — Summation Level + Reporting Level correct</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-style:italic;color:#666">Manage Time Rule Templates → TER template</td></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:700">3</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Time Category cleaned — only what the rule needs</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-style:italic;color:#666">Manage Time Categories → Conditions tab</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:700">4</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">WORKED_TIME_CONDITION bound to the category</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-style:italic;color:#666">Manage Time Calculation Rules → Parameters tab</td></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:700">5</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">Rule sets → Profile → HCM Group → Evaluate Membership</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-style:italic;color:#666">Worker Time Processing Profiles + Scheduled Processes</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:700">6</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">add_log / add_rlog with correct HWM_ contexts</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-style:italic;color:#666">Inside the Fast Formula</td></tr>
  <tr><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-weight:700">7</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px">ORA_HWM_RULES_LOG_LEVEL = Finest + sign-out / sign-in</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;border-bottom:1px solid #e0dcd6;font-size:14px;font-style:italic;color:#666">Manage Administrator Profile Values</td></tr>
  <tr style="background:#faf7f3"><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px;font-weight:700">8</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px">Data role: View All People + Orgs + Positions + LDGs</td><td style="font-family:'Open Sans',sans-serif;padding:10px 14px;font-size:14px;font-style:italic;color:#666">Manage Data Role and Security Profiles (MOS 2120220.1)</td></tr>
</table>



<hr style="border:0;height:1px;background:#e0dcd6;margin:30px 0">

<h2 style="font-size:22px;font-weight:700;color:#1a1a1a;margin:28px 0 14px;font-family:'Open Sans',sans-serif">Key Takeaways</h2>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px"><strong>Setup before code, code before profile, profile before debugging.</strong> Most of us start at the wrong end — writing <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">add_log</code> calls and then wondering why nothing shows up — when the answer is usually one screen away.</p>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px"><strong>Two functions, same destination.</strong> <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">add_log</code> (2 args) and <code style="background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:monospace;font-size:14px;color:#c0392b">add_rlog</code> (3 args) both write to an internal log table. View the output on the Analyze Rule Processing Details page. Nothing else works for UI-triggered timecard saves.</p>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px"><strong>Day vs Time Card — two extras.</strong> Time Card summation needs manual state reset at END_DAY and an END_PERIOD handler. Day does not. Start with Day for daily validations, switch to Time Card only when you need period-level checks.</p>

<p style="font-family:'Open Sans',sans-serif;font-size:16px;margin-bottom:18px"><strong>The skeleton is the starting point.</strong> Drop the minimal TER skeleton in, confirm logs appear, then graduate to the production skeleton with all the guards. Business logic goes on top.</p>


<div style="display:flex;align-items:center;gap:14px;margin:28px 0;padding:14px 0;border-top:1px solid #e0dcd6;border-bottom:1px solid #e0dcd6">
  <div style="width:44px;height:44px;background:#c0392b;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;flex-shrink:0;font-family:'Open Sans',sans-serif">AM</div>
  <div>
    <div style="font-weight:700;font-size:15px;color:#1a1a1a">Abhishek Mohanty</div>
    <div style="font-family:'Open Sans',sans-serif;font-size:13px;color:#666">Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time and Labor, Core HR, Redwood, HDL, OTBI.</div>
  </div>
</div>

</div>