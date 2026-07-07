---
title: "Oracle HCM Fast Formula Series:GET_CONTEXT and CHANGE_CONTEXTS: The Two Context Statements You Actually Need"
description: "Fast Formula Context Handling Intermediate Verified Oracle Fast Formula: GET_CONTEXT and CHANGE_CONTEXTS — The Two Context Statements You Actually Need April 2026 · 10 min read · Oracle HCM Cloud Orac"
pubDate: 2026-04-12
tags: ["Fast Formula", "Oracle HCM Cloud"]
---

<div style="margin:12px 0 18px;line-height:2.4"><span style="display:inline-block;color:#fff;padding:10px 22px;font-size:13px;font-weight:700;margin:0 8px 8px 0;border-radius:0;text-transform:uppercase;letter-spacing:0.12em;background:#b8372a">Fast Formula</span><span style="display:inline-block;color:#fff;padding:10px 22px;font-size:13px;font-weight:700;margin:0 8px 8px 0;border-radius:0;text-transform:uppercase;letter-spacing:0.12em;background:#d87f1a">Context Handling</span><span style="display:inline-block;color:#fff;padding:10px 22px;font-size:13px;font-weight:700;margin:0 8px 8px 0;border-radius:0;text-transform:uppercase;letter-spacing:0.12em;background:#8e44ad">Intermediate</span><span style="display:inline-block;color:#fff;padding:10px 22px;font-size:13px;font-weight:700;margin:0 8px 8px 0;border-radius:0;text-transform:uppercase;letter-spacing:0.12em;background:#1f2a36">Verified</span></div>

<h1 style="font-size:24px;font-weight:700;margin:16px 0 8px;line-height:1.3;color:#1a1a1a;word-wrap:break-word">Oracle Fast Formula: GET_CONTEXT and CHANGE_CONTEXTS — The Two Context Statements You Actually Need</h1>

<div style="color:#888;font-size:13px;margin:6px 0 18px">April 2026 · 10 min read · Oracle HCM Cloud</div>

<p>Oracle Fast Formula has two context-handling statements that every developer eventually needs to master: one reads the engine's current context values, the other temporarily overrides them. They look similar but do opposite things — and confusing them is one of the most common sources of silent bugs in production formulas. This post walks through both as diagrams first, code second, with a production-grade example at the end.</p>

<div style="margin:26px 0;padding:22px 0;border-top:2px solid #000;border-bottom:2px solid #000;font-size:15px;display:table;width:100%"><div style="display:table-cell;width:80px;vertical-align:top;padding-right:18px"><div style="width:60px;height:60px;background:linear-gradient(135deg,#f57c3a 0%,#b8372a 100%);color:#fff;text-align:center;line-height:60px;font-weight:700;font-size:18px;border-radius:50%;letter-spacing:0.05em">AM</div></div><div style="display:table-cell;vertical-align:top"><strong>Abhishek Mohanty</strong><span>Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant</span></div></div>

<hr style="border:none;border-top:1px solid #e5e5e5;margin:34px 0">

<h2 style="font-size:22px;font-weight:700;margin:40px 0 14px;color:#1a1a1a">How a DBI Reference Becomes a SQL Query</h2>
<p>Every time you write <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">l_name = PER_PER_FULL_NAME</code>, five things happen in sequence. The calling application populates the context layer. Your DBI reference triggers a route lookup. The route builds SQL. The contexts bind into that SQL as <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">:PID</code> and <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">:EFF</code>. The database returns a value.</p>

<div style="margin:24px 0;padding:20px;background:#fafafa;border:1px solid #e5e5e5;border-radius:4px;text-align:center"><svg viewBox="0 0 620 360" xmlns="http://www.w3.org/2000/svg" font-family="'Open Sans',sans-serif" font-size="12">
<defs><marker id="a1" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#555"/></marker></defs>
<rect x="20" y="20" width="170" height="60" fill="#fff" stroke="#c0392b" stroke-width="2" rx="4"/>
<text x="105" y="40" text-anchor="middle" font-weight="700" fill="#c0392b">Calling Application</text>
<text x="105" y="58" text-anchor="middle" fill="#555">Absence · OTL · Comp</text>
<text x="105" y="72" text-anchor="middle" fill="#555" font-size="11">injects context values</text>
<line x1="190" y1="50" x2="240" y2="50" stroke="#555" stroke-width="1.5" marker-end="url(#a1)"/>
<rect x="240" y="20" width="170" height="60" fill="#fff" stroke="#2c5282" stroke-width="2" rx="4"/>
<text x="325" y="40" text-anchor="middle" font-weight="700" fill="#2c5282">Context Layer</text>
<text x="325" y="58" text-anchor="middle" fill="#555" font-family="Consolas" font-size="11">PERSON_ID = 4001</text>
<text x="325" y="72" text-anchor="middle" fill="#555" font-family="Consolas" font-size="11">EFF_DATE = 15-Mar-26</text>
<line x1="410" y1="50" x2="460" y2="50" stroke="#555" stroke-width="1.5" marker-end="url(#a1)"/>
<rect x="460" y="20" width="140" height="60" fill="#fff" stroke="#2e7d32" stroke-width="2" rx="4"/>
<text x="530" y="40" text-anchor="middle" font-weight="700" fill="#2e7d32">Your Formula</text>
<text x="530" y="60" text-anchor="middle" font-family="Consolas" font-size="10" fill="#555">l_name =</text>
<text x="530" y="74" text-anchor="middle" font-family="Consolas" font-size="10" fill="#555">PER_PER_FULL_NAME</text>
<line x1="530" y1="80" x2="530" y2="125" stroke="#555" stroke-width="1.5" marker-end="url(#a1)"/>
<text x="545" y="108" fill="#555" font-size="11" font-style="italic">triggers DBI</text>
<rect x="240" y="130" width="290" height="100" fill="#0d1117" stroke="#0d1117" rx="4"/>
<text x="385" y="150" text-anchor="middle" fill="#79c0ff" font-weight="700" font-size="11">HIDDEN SQL ROUTE</text>
<text x="250" y="168" fill="#e6edf3" font-family="Consolas" font-size="10">SELECT full_name</text>
<text x="250" y="181" fill="#e6edf3" font-family="Consolas" font-size="10">FROM   per_person_names_f</text>
<text x="250" y="194" fill="#e6edf3" font-family="Consolas" font-size="10">WHERE  person_id = :PID</text>
<text x="250" y="207" fill="#e6edf3" font-family="Consolas" font-size="10">AND    name_type = 'GLOBAL'</text>
<text x="250" y="220" fill="#e6edf3" font-family="Consolas" font-size="10">AND    :EFF BETWEEN eff_start_date AND eff_end_date</text>
<line x1="325" y1="80" x2="325" y2="125" stroke="#555" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#a1)"/>
<text x="175" y="108" fill="#555" font-size="11" font-style="italic">contexts bind as :PID, :EFF</text>
<line x1="385" y1="230" x2="385" y2="255" stroke="#555" stroke-width="1.5" marker-end="url(#a1)"/>
<rect x="240" y="260" width="290" height="60" fill="#fff" stroke="#c0392b" stroke-width="2" rx="4"/>
<text x="385" y="282" text-anchor="middle" font-weight="700" fill="#c0392b">Database</text>
<text x="385" y="302" text-anchor="middle" fill="#555">returns "Priya Patel"</text>
<text x="385" y="316" text-anchor="middle" fill="#555" font-size="11">back into l_name</text>
</svg><div style="font-size:12px;color:#777;font-style:italic;margin-top:12px;text-align:center">Fig 1 — Contexts act as SQL bind variables between your formula and the database</div></div>

<p>This happens thousands of times per formula run, invisible to you — and it's why context statements matter. They're the only way to inspect or manipulate the bind-variable layer. Two statements do the real work: GET_CONTEXT reads, CHANGE_CONTEXTS writes.</p>

<hr style="border:none;border-top:1px solid #e5e5e5;margin:34px 0">

<h2 style="font-size:22px;font-weight:700;margin:40px 0 14px;color:#1a1a1a">GET_CONTEXT vs CHANGE_CONTEXTS — Read vs Write</h2>

<p>The first question developers ask: if GET_CONTEXT reads the current value and CHANGE_CONTEXTS overrides it, why not use just one of them? Because they solve opposite problems. One captures the state the engine injected. The other temporarily substitutes different state so your DBIs can resolve data from a different viewpoint.</p>

<div style="margin:24px 0;padding:20px;background:#fafafa;border:1px solid #e5e5e5;border-radius:4px;text-align:center"><svg viewBox="0 0 620 340" xmlns="http://www.w3.org/2000/svg" font-family="'Open Sans',sans-serif" font-size="12">
<text x="310" y="22" text-anchor="middle" font-weight="700" font-size="13" fill="#1a1a1a">Same context, opposite operations</text>


<rect x="180" y="45" width="260" height="60" fill="#fff" stroke="#2c5282" stroke-width="2" rx="4"/>
<text x="310" y="65" text-anchor="middle" font-weight="700" fill="#2c5282" font-size="12">Context Layer (engine-managed)</text>
<text x="310" y="84" text-anchor="middle" font-family="Consolas" font-size="11" fill="#555">EFFECTIVE_DATE = 15-Mar-2026</text>
<text x="310" y="97" text-anchor="middle" fill="#888" font-size="10" font-style="italic">injected by the calling application</text>


<defs><marker id="rd" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#c0392b"/></marker><marker id="wr" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#6a1b9a"/></marker></defs>
<line x1="220" y1="105" x2="150" y2="175" stroke="#c0392b" stroke-width="2" marker-end="url(#rd)"/>
<line x1="400" y1="105" x2="470" y2="175" stroke="#6a1b9a" stroke-width="2" marker-end="url(#wr)"/>


<rect x="20" y="180" width="260" height="140" fill="#fff5f2" stroke="#c0392b" stroke-width="2" rx="4"/>
<text x="150" y="203" text-anchor="middle" font-weight="700" fill="#c0392b" font-size="14">GET_CONTEXT — READ</text>
<text x="150" y="222" text-anchor="middle" fill="#555" font-size="11">copies current value into</text>
<text x="150" y="236" text-anchor="middle" fill="#555" font-size="11">a local variable</text>
<rect x="40" y="250" width="220" height="32" fill="#fff" stroke="#c0392b" rx="3"/>
<text x="150" y="270" text-anchor="middle" font-family="Consolas" font-size="11" fill="#c0392b">l_eff = GET_CONTEXT(EFFECTIVE_DATE, d)</text>
<text x="150" y="300" text-anchor="middle" fill="#888" font-size="10" font-style="italic">context layer unchanged</text>


<rect x="340" y="180" width="260" height="140" fill="#f8f0fa" stroke="#6a1b9a" stroke-width="2" rx="4"/>
<text x="470" y="203" text-anchor="middle" font-weight="700" fill="#6a1b9a" font-size="14">CHANGE_CONTEXTS — WRITE</text>
<text x="470" y="222" text-anchor="middle" fill="#555" font-size="11">temporarily overrides value</text>
<text x="470" y="236" text-anchor="middle" fill="#555" font-size="11">inside a scoped block</text>
<rect x="360" y="250" width="220" height="32" fill="#fff" stroke="#6a1b9a" rx="3"/>
<text x="470" y="270" text-anchor="middle" font-family="Consolas" font-size="10" fill="#6a1b9a">CHANGE_CONTEXTS(EFFECTIVE_DATE=d2)(...)</text>
<text x="470" y="300" text-anchor="middle" fill="#888" font-size="10" font-style="italic">auto-reverts on block exit</text>
</svg><div style="font-size:12px;color:#777;font-style:italic;margin-top:12px;text-align:center">Fig 2 — GET_CONTEXT pulls the current value out. CHANGE_CONTEXTS pushes a new value in (scoped).</div></div>

<p>The rest of this post walks through each statement in depth, then puts them together in an end-to-end example from absence management.</p>

<hr style="border:none;border-top:1px solid #e5e5e5;margin:34px 0">

<h2 style="font-size:22px;font-weight:700;margin:40px 0 14px;color:#1a1a1a">GET_CONTEXT — Reading the Engine's Current State</h2>

<p>GET_CONTEXT takes two arguments: the context name (unquoted) and a typed default that matches the context's data type. Use <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">0</code> for numbers, <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">' '</code> for text, <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">'4712/12/31 00:00:00' (date)</code> for dates. Forget the default and the formula won't compile.</p>

<p>The returned value lives in your local variable from that point until you overwrite it. GET_CONTEXT is purely a reader — it never modifies the context layer, so it's safe to call repeatedly and in any order.</p>

<h3 style="font-size:16px;font-weight:700;margin:22px 0 10px;color:#1a1a1a;font-style:italic">Real Example — Capturing contexts at the top of a formula</h3>

<pre style="background:#f8f8f8;color:#222;padding:12px 16px;border:1px solid #ddd;border-left:3px solid #888;font-family:Consolas,monospace;font-size:12px;line-height:1.6;white-space:pre-wrap;word-break:break-word;margin:14px 0;max-width:100%;box-sizing:border-box">l_person_id = GET_CONTEXT(PERSON_ID, 0)
l_asg_id    = GET_CONTEXT(HR_ASSIGNMENT_ID, 0)
l_eff_dt    = GET_CONTEXT(EFFECTIVE_DATE, '4712/12/31 00:00:00' (date))</pre>

<p>Three reads into three locals. From this point onward, any branching logic can use these values — including decisions about whether to enter a CHANGE_CONTEXTS block and with what override values.</p>

<hr style="border:none;border-top:1px solid #e5e5e5;margin:34px 0">

<h2 style="font-size:22px;font-weight:700;margin:40px 0 14px;color:#1a1a1a">CHANGE_CONTEXTS — Temporarily Overriding State</h2>

<p>CHANGE_CONTEXTS temporarily overrides one or more context values inside a scoped block. Every DBI fetch and function call that runs inside the block uses the overridden values. The moment execution exits the closing parenthesis, the context layer reverts to whatever it was before. You never write restore code — the engine handles it.</p>

<pre style="background:#f8f8f8;color:#222;padding:12px 16px;border:1px solid #ddd;border-left:3px solid #888;font-family:Consolas,monospace;font-size:12px;line-height:1.6;white-space:pre-wrap;word-break:break-word;margin:14px 0;max-width:100%;box-sizing:border-box">CHANGE_CONTEXTS(PERSON_ID = l_mgr_pid, EFFECTIVE_DATE = l_target_date)
(
  /* Inside this block, all DBIs resolve for the manager as of target date */
  l_mgr_name      = PER_PER_FULL_NAME
  l_mgr_hire_date = PER_PERSON_ENTERPRISE_HIRE_DATE
)
/* Out here, contexts are back to the original values */</pre>

<h3 style="font-size:16px;font-weight:700;margin:22px 0 10px;color:#1a1a1a;font-style:italic">About the brackets — read carefully</h3>

<p>Without parentheses, CHANGE_CONTEXTS applies its override to exactly the next single statement. It does not silently fail. It just scopes very narrowly. The moment you have two or more statements that need the new context, you must enclose them in <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">( )</code>. In practice, always use brackets. Single-statement scoping is a trap that breaks the instant someone adds a second line.</p>

<h3 style="font-size:16px;font-weight:700;margin:22px 0 10px;color:#1a1a1a;font-style:italic">Combine, don't nest</h3>

<p>If you need to change three contexts, put them all in one CHANGE_CONTEXTS call. Oracle's Administering Fast Formulas guide is explicit: <em>"Use CHANGE_CONTEXTS only when required, because CHANGE_CONTEXTS can cause database item values to be fetched again from the database. You can perform multiple context changes using a single CHANGE_CONTEXTS statement, instead of calling CHANGE_CONTEXTS from other CHANGE_CONTEXTS blocks."</em></p>

<p>Every context you change forces the engine to invalidate cached DBI values for routes that use that context. Changing PERSON_ID when you only need to change EFFECTIVE_DATE is a hidden performance penalty.</p>

<h3 style="font-size:16px;font-weight:700;margin:22px 0 10px;color:#1a1a1a;font-style:italic">The lifecycle</h3>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:13px;border:1px solid #ddd;table-layout:fixed;word-wrap:break-word"><tr><th style="background:#f5f5f5;padding:10px 12px;text-align:left;font-weight:700;border:1px solid #ddd;font-size:12px;text-transform:uppercase;letter-spacing:0.04em">Phase</th><th style="background:#f5f5f5;padding:10px 12px;text-align:left;font-weight:700;border:1px solid #ddd;font-size:12px;text-transform:uppercase;letter-spacing:0.04em">What happens</th></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">1. Before</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">Original contexts: PERSON_ID = 4001, EFFECTIVE_DATE = 2026-03-15</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">2. Enter</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">CHANGE_CONTEXTS(PERSON_ID = 5002, EFFECTIVE_DATE = 2024-01-01)</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">3. Inside</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">Every DBI resolves for person 5002 as of January 2024</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">4. Exit</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">Closing parenthesis reached</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">5. After</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">Auto-restored to PERSON_ID = 4001, EFFECTIVE_DATE = 2026-03-15</td></tr></table>

<hr style="border:none;border-top:1px solid #e5e5e5;margin:34px 0">

<h2 style="font-size:22px;font-weight:700;margin:40px 0 14px;color:#1a1a1a">End-to-End Example — Compassionate Leave Manager Tenure Check</h2>

<p>The client policy: when an employee applies for Compassionate Leave, verify that the line manager has been employed for at least 90 days as of the absence start date. If the manager is too new, reject the submission with an informative message so BPM approval routing can re-route the request through the skip-level chain.</p>

<p>This is a <strong>Global Absence Entry Validation</strong> formula. The calling application sets PERSON_ID, HR_ASSIGNMENT_ID, and EFFECTIVE_DATE contexts automatically, plus a set of standard input values (IV_START_DATE, IV_END_DATE, IV_ABSENCE_TYPE_ID, and others) passed into the formula. The contract with the engine is strict: the formula must return exactly two predefined variables — <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">VALID</code> (<code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">'Y'</code> or <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">'N'</code>) and <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">ERROR_MESSAGE</code> (the text shown to the user on rejection). Everything else is your own logic.</p>

<p>We need the manager's hire date — but the manager's data sits behind a different PERSON_ID than the one the engine injected. That's exactly what CHANGE_CONTEXTS exists for. We also need to read the hire date <em>as of the absence start date</em>, not as of today — which means overriding EFFECTIVE_DATE inside the same block.</p>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:13px;border:1px solid #ddd;table-layout:fixed;word-wrap:break-word"><tr><th style="background:#f5f5f5;padding:10px 12px;text-align:left;font-weight:700;border:1px solid #ddd;font-size:12px;text-transform:uppercase;letter-spacing:0.04em;width:8%">Step</th><th style="background:#f5f5f5;padding:10px 12px;text-align:left;font-weight:700;border:1px solid #ddd;font-size:12px;text-transform:uppercase;letter-spacing:0.04em">What it does</th><th style="background:#f5f5f5;padding:10px 12px;text-align:left;font-weight:700;border:1px solid #ddd;font-size:12px;text-transform:uppercase;letter-spacing:0.04em">Statement / DBI</th></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">1</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">Declare INPUTS and DEFAULT FOR every DBI, input, and return variable used</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">INPUTS ARE / DEFAULT FOR</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">2</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">Read PERSON_ID for traceability — EFFECTIVE_DATE is implicit and will be overridden later</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">GET_CONTEXT</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">3</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">Fetch the manager's person ID in the original employee context</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">PER_ASG_MANAGER_PERSON_ID <em>(verify in your pod via DBI X-Ray query)</em></td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">4</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">Initialise VALID and ERROR_MESSAGE to approval defaults — reject only on explicit failure</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">VALID = 'Y'</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">5</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">If no manager on assignment, reject with an informative message</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">IF l_mgr_pid = 0 THEN</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">6</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">Otherwise, switch context to manager + absence start date, read hire date, compute tenure</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">CHANGE_CONTEXTS</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">7</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">Return VALID and ERROR_MESSAGE — the Global Absence Entry Validation return contract</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">RETURN VALID, ERROR_MESSAGE</td></tr></table>

<h3 style="font-size:16px;font-weight:700;margin:22px 0 10px;color:#1a1a1a;font-style:italic">Real Example — XX_COMPASSIONATE_LV_ENTRY_VAL</h3>

<pre style="background:#f8f8f8;color:#222;padding:12px 16px;border:1px solid #ddd;border-left:3px solid #888;font-family:Consolas,monospace;font-size:12px;line-height:1.6;white-space:pre-wrap;word-break:break-word;margin:14px 0;max-width:100%;box-sizing:border-box">/******************************************************
 * FORMULA : XX_COMPASSIONATE_LV_ENTRY_VAL
 * TYPE    : Global Absence Entry Validation
 * RETURNS : VALID ('Y'/'N') + ERROR_MESSAGE (text)
 * NOTE    : DBI names should be verified in your pod via
 *           the DBI X-Ray query.
 ******************************************************/

/*=========== INPUTS ==============================================*/
INPUTS ARE IV_START_DATE      (date),
           IV_END_DATE        (date),
           IV_ABSENCE_TYPE_ID (number)

/*=========== DBI DEFAULTS ========================================*/
DEFAULT FOR PER_ASG_MANAGER_PERSON_ID       IS 0
DEFAULT FOR PER_PER_FULL_NAME                IS 'Unknown'
DEFAULT FOR PER_PERSON_ENTERPRISE_HIRE_DATE IS '1901/01/01 00:00:00' (date)

/*=========== RETURN + INPUT DEFAULTS =============================*/
DEFAULT FOR VALID              IS 'Y'
DEFAULT FOR ERROR_MESSAGE      IS ' '
DEFAULT FOR IV_START_DATE      IS '4712/12/31 00:00:00' (date)
DEFAULT FOR IV_END_DATE        IS '4712/12/31 00:00:00' (date)
DEFAULT FOR IV_ABSENCE_TYPE_ID IS 0

/*=========== CONSTANTS ===========================================*/
l_threshold = 90

/*=========== CALCULATION =========================================*/

/* Step 1: Read PERSON_ID context */
l_emp_pid  = GET_CONTEXT(PERSON_ID, 0)
l_emp_name = PER_PER_FULL_NAME

/* Step 2: Fetch manager ID in the original employee context */
l_mgr_pid = PER_ASG_MANAGER_PERSON_ID

/* Step 3: Initialise return variables — default to approval */
VALID         = 'Y'
ERROR_MESSAGE = ' '

/* Step 4: Branch on whether a manager exists on the assignment */
IF l_mgr_pid = 0 THEN
(
  VALID         = 'N'
  ERROR_MESSAGE = 'Your assignment does not have a reporting manager. '
               || 'Please contact HR before applying for Compassionate Leave.'
)
ELSE
(
  /* Step 5: Switch to manager context, read hire date as of absence start date */
  CHANGE_CONTEXTS(PERSON_ID = l_mgr_pid, EFFECTIVE_DATE = IV_START_DATE)
  (
    l_mgr_name      = PER_PER_FULL_NAME
    l_mgr_hire_date = PER_PERSON_ENTERPRISE_HIRE_DATE
    l_tenure_days   = DAYS_BETWEEN(IV_START_DATE, l_mgr_hire_date)

    IF l_tenure_days < l_threshold THEN
    (
      VALID         = 'N'
      ERROR_MESSAGE = 'Your reporting manager (' || l_mgr_name
                   || ') has only ' || TO_CHAR(l_tenure_days)
                   || ' days of tenure (minimum 90 required for Compassionate Leave). '
                   || 'Please re-submit through your skip-level manager.'
    )
  )
  /* Context auto-reverts here */
)

RETURN VALID, ERROR_MESSAGE</pre>

<p><strong>Why the EFFECTIVE_DATE override matters.</strong> The engine-injected EFFECTIVE_DATE is the date the user hit Submit, but the business rule cares about the absence start date — passed in as <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">IV_START_DATE</code>. Switching EFFECTIVE_DATE to IV_START_DATE inside the CHANGE_CONTEXTS block ensures the manager's hire-date DBI resolves as of the leave start date — exactly the moment we care about for the 90-day rule. Both overrides happen in a single CHANGE_CONTEXTS call, following the combine-don't-nest best practice.</p>

<div style="margin:24px 0;padding:20px;background:#fafafa;border:1px solid #e5e5e5;border-radius:4px;text-align:center"><svg viewBox="0 0 620 380" xmlns="http://www.w3.org/2000/svg" font-family="'Open Sans',sans-serif" font-size="12">
<defs><marker id="a7" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#555"/></marker></defs>
<text x="310" y="20" text-anchor="middle" font-weight="700" font-size="13" fill="#1a1a1a">Same employee, same manager, different EFFECTIVE_DATE = different tenure</text>


<line x1="50" y1="80" x2="570" y2="80" stroke="#888" stroke-width="2"/>


<circle cx="90" cy="80" r="6" fill="#2e7d32"/>
<text x="90" y="62" text-anchor="middle" font-weight="700" fill="#2e7d32" font-size="11">Nov 2, 2025</text>
<text x="90" y="102" text-anchor="middle" fill="#555" font-size="10">manager hired</text>


<circle cx="320" cy="80" r="6" fill="#2c5282"/>
<text x="320" y="62" text-anchor="middle" font-weight="700" fill="#2c5282" font-size="11">Jan 5, 2026</text>
<text x="320" y="102" text-anchor="middle" fill="#555" font-size="10">user submits leave request</text>
<text x="320" y="115" text-anchor="middle" fill="#555" font-size="10" font-style="italic">(EFFECTIVE_DATE)</text>


<circle cx="500" cy="80" r="6" fill="#c0392b"/>
<text x="500" y="62" text-anchor="middle" font-weight="700" fill="#c0392b" font-size="11">Feb 10, 2026</text>
<text x="500" y="102" text-anchor="middle" fill="#555" font-size="10">absence starts</text>
<text x="500" y="115" text-anchor="middle" fill="#555" font-size="10" font-style="italic">(IV_START_DATE)</text>



<line x1="90" y1="140" x2="320" y2="140" stroke="#c0392b" stroke-width="2"/>
<line x1="90" y1="135" x2="90" y2="145" stroke="#c0392b" stroke-width="2"/>
<line x1="320" y1="135" x2="320" y2="145" stroke="#c0392b" stroke-width="2"/>
<text x="205" y="133" text-anchor="middle" fill="#c0392b" font-weight="700" font-size="11">64 days</text>


<line x1="90" y1="165" x2="500" y2="165" stroke="#2e7d32" stroke-width="2"/>
<line x1="90" y1="160" x2="90" y2="170" stroke="#2e7d32" stroke-width="2"/>
<line x1="500" y1="160" x2="500" y2="170" stroke="#2e7d32" stroke-width="2"/>
<text x="295" y="180" text-anchor="middle" fill="#2e7d32" font-weight="700" font-size="11">100 days</text>


<line x1="50" y1="200" x2="570" y2="200" stroke="#d4a017" stroke-width="1" stroke-dasharray="4,3"/>
<text x="565" y="197" text-anchor="end" fill="#d4a017" font-size="10" font-style="italic">— 90 day policy threshold —</text>


<rect x="30" y="215" width="270" height="150" fill="#fff5f2" stroke="#c0392b" stroke-width="2" rx="4"/>
<text x="165" y="238" text-anchor="middle" font-weight="700" fill="#c0392b" font-size="13">✗ Without override</text>
<text x="165" y="258" text-anchor="middle" fill="#555" font-size="11">EFFECTIVE_DATE = Jan 5, 2026</text>
<text x="165" y="278" text-anchor="middle" fill="#555" font-size="11">Manager tenure =</text>
<text x="165" y="300" text-anchor="middle" fill="#c0392b" font-weight="800" font-size="22">64 days</text>
<line x1="80" y1="318" x2="250" y2="318" stroke="#c0392b" stroke-width="1" stroke-dasharray="3,2"/>
<text x="165" y="338" text-anchor="middle" fill="#c0392b" font-size="11" font-weight="700">Below 90 → VALID = 'N'</text>
<text x="165" y="354" text-anchor="middle" fill="#555" font-size="10" font-style="italic">but this isn't the right answer</text>


<rect x="320" y="215" width="270" height="150" fill="#f0f9f0" stroke="#2e7d32" stroke-width="2" rx="4"/>
<text x="455" y="238" text-anchor="middle" font-weight="700" fill="#2e7d32" font-size="13">✓ With CHANGE_CONTEXTS override</text>
<text x="455" y="258" text-anchor="middle" fill="#555" font-size="11">EFFECTIVE_DATE = Feb 10, 2026</text>
<text x="455" y="278" text-anchor="middle" fill="#555" font-size="11">Manager tenure =</text>
<text x="455" y="300" text-anchor="middle" fill="#2e7d32" font-weight="800" font-size="22">100 days</text>
<line x1="370" y1="318" x2="540" y2="318" stroke="#2e7d32" stroke-width="1" stroke-dasharray="3,2"/>
<text x="455" y="338" text-anchor="middle" fill="#2e7d32" font-size="11" font-weight="700">Above 90 → VALID = 'Y'</text>
<text x="455" y="354" text-anchor="middle" fill="#555" font-size="10" font-style="italic">which is the correct answer</text>
</svg><div style="font-size:12px;color:#777;font-style:italic;margin-top:12px;text-align:center">Fig 3 — Manager hired Nov 2, 2025. As of the submission date the tenure is 64 days; as of the absence start date it's 100 days. The business rule cares about the latter.</div></div>

<p><strong>Why the formula rejects instead of routing.</strong> Global Absence Entry Validation has a strict binary contract: <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">VALID = 'Y'</code> lets the submission proceed, <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">VALID = 'N'</code> blocks it and shows <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">ERROR_MESSAGE</code> to the user. The formula cannot re-route the request on its own — that's what BPM approval rules are for. The correct pattern is: reject with a clear message, and configure the BPM approval rule to recognise the rejection and trigger the skip-level routing. Trying to route from inside the formula itself is a category error that breaks the formula-type contract.</p>

<div style="margin:24px 0;padding:20px;background:#fafafa;border:1px solid #e5e5e5;border-radius:4px;text-align:center"><svg viewBox="0 0 620 340" xmlns="http://www.w3.org/2000/svg" font-family="'Open Sans',sans-serif" font-size="12">
<defs><marker id="a8" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#555"/></marker></defs>
<text x="310" y="22" text-anchor="middle" font-weight="700" font-size="13" fill="#1a1a1a">Two layers, two responsibilities — don't mix them</text>
<rect x="20" y="45" width="580" height="125" fill="#fff5f2" stroke="#c0392b" stroke-width="2" rx="4"/>
<text x="40" y="68" font-weight="700" fill="#c0392b" font-size="13">Layer 1 — Formula (what your Fast Formula does)</text>
<rect x="40" y="80" width="140" height="70" fill="#fff" stroke="#c0392b" rx="3"/>
<text x="110" y="100" text-anchor="middle" font-weight="700" fill="#c0392b" font-size="11">Entry Validation</text>
<text x="110" y="118" text-anchor="middle" fill="#555" font-size="10">checks tenure</text>
<text x="110" y="132" text-anchor="middle" fill="#555" font-size="10">sets VALID + MESSAGE</text>
<line x1="180" y1="115" x2="230" y2="115" stroke="#555" stroke-width="1.5" marker-end="url(#a8)"/>
<rect x="230" y="80" width="160" height="70" fill="#fff" stroke="#c0392b" rx="3"/>
<text x="310" y="100" text-anchor="middle" font-weight="700" fill="#c0392b" font-size="11">Absence engine</text>
<text x="310" y="118" text-anchor="middle" fill="#555" font-size="10">reads VALID = 'N'</text>
<text x="310" y="132" text-anchor="middle" fill="#555" font-size="10">surfaces ERROR_MESSAGE</text>
<line x1="390" y1="115" x2="440" y2="115" stroke="#555" stroke-width="1.5" marker-end="url(#a8)"/>
<rect x="440" y="80" width="140" height="70" fill="#fff" stroke="#c0392b" rx="3"/>
<text x="510" y="100" text-anchor="middle" font-weight="700" fill="#c0392b" font-size="11">User sees message</text>
<text x="510" y="118" text-anchor="middle" fill="#555" font-size="10">"Manager tenure</text>
<text x="510" y="132" text-anchor="middle" fill="#555" font-size="10">below 90 days..."</text>
<line x1="20" y1="185" x2="600" y2="185" stroke="#888" stroke-width="1" stroke-dasharray="4,3"/>
<text x="310" y="200" text-anchor="middle" fill="#888" font-size="11" font-style="italic">Formula finishes here. BPM starts here.</text>
<rect x="20" y="210" width="580" height="120" fill="#f0f5fa" stroke="#2c5282" stroke-width="2" rx="4"/>
<text x="40" y="232" font-weight="700" fill="#2c5282" font-size="13">Layer 2 — BPM (what the approval rule does)</text>
<rect x="40" y="246" width="160" height="70" fill="#fff" stroke="#2c5282" rx="3"/>
<text x="120" y="266" text-anchor="middle" font-weight="700" fill="#2c5282" font-size="11">Approval rule</text>
<text x="120" y="284" text-anchor="middle" fill="#555" font-size="10">detects rejection pattern</text>
<text x="120" y="298" text-anchor="middle" fill="#555" font-size="10">in ERROR_MESSAGE text</text>
<line x1="200" y1="281" x2="250" y2="281" stroke="#555" stroke-width="1.5" marker-end="url(#a8)"/>
<rect x="250" y="246" width="160" height="70" fill="#fff" stroke="#2c5282" rx="3"/>
<text x="330" y="266" text-anchor="middle" font-weight="700" fill="#2c5282" font-size="11">Skip-level routing</text>
<text x="330" y="284" text-anchor="middle" fill="#555" font-size="10">bypasses direct manager</text>
<text x="330" y="298" text-anchor="middle" fill="#555" font-size="10">sends to grandmanager</text>
<line x1="410" y1="281" x2="460" y2="281" stroke="#555" stroke-width="1.5" marker-end="url(#a8)"/>
<rect x="460" y="246" width="120" height="70" fill="#fff" stroke="#2c5282" rx="3"/>
<text x="520" y="266" text-anchor="middle" font-weight="700" fill="#2c5282" font-size="11">Approved</text>
<text x="520" y="284" text-anchor="middle" fill="#555" font-size="10">by skip-level</text>
<text x="520" y="298" text-anchor="middle" fill="#555" font-size="10">manager</text>
</svg><div style="font-size:12px;color:#777;font-style:italic;margin-top:12px;text-align:center">Fig 4 — Formula returns VALID / ERROR_MESSAGE. BPM reads the rejection and handles routing separately.</div></div>

<hr style="border:none;border-top:1px solid #e5e5e5;margin:34px 0">

<h2 style="font-size:22px;font-weight:700;margin:40px 0 14px;color:#1a1a1a">Pitfalls to Avoid</h2>

<table style="width:100%;border-collapse:collapse;margin:18px 0;font-size:13px;border:1px solid #ddd;table-layout:fixed;word-wrap:break-word"><tr><th style="background:#f5f5f5;padding:10px 12px;text-align:left;font-weight:700;border:1px solid #ddd;font-size:12px;text-transform:uppercase;letter-spacing:0.04em;width:8%">#</th><th style="background:#f5f5f5;padding:10px 12px;text-align:left;font-weight:700;border:1px solid #ddd;font-size:12px;text-transform:uppercase;letter-spacing:0.04em">Pitfall</th></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">1</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top"><strong>Omitting brackets after CHANGE_CONTEXTS</strong> when more than one statement needs the override. Only the immediately following statement runs under the new context. Always use brackets.</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">2</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top"><strong>Nesting when combining would suffice.</strong> Two separate nested calls can almost always be replaced with one combined call.</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">3</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top"><strong>Restating already-set contexts.</strong> Achieves nothing functionally but forces unnecessary DBI cache invalidation.</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">4</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top"><strong>Forgetting the default in GET_CONTEXT.</strong> Compile error if you omit the second argument.</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">5</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top"><strong>Using a context the formula type does not support.</strong> Runtime error. Check the formula type documentation first.</td></tr>
<tr><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top">6</td><td style="padding:10px 12px;border:1px solid #e5e5e5;vertical-align:top"><strong>Overriding PERSON_ID when you only need to change EFFECTIVE_DATE.</strong> Every context you override forces DBI cache invalidation for every route that uses that context. Change only what you need.</td></tr></table>

<hr style="border:none;border-top:1px solid #e5e5e5;margin:34px 0">

<h2 style="font-size:22px;font-weight:700;margin:40px 0 14px;color:#1a1a1a">A brief mention — CONTEXT_IS_SET</h2>

<p>For completeness: Oracle Fast Formula also exposes a third context-handling statement called <code style="background:#f0f0f0;padding:2px 6px;border-radius:2px;font-family:Consolas,monospace;font-size:13px;color:#c0392b">CONTEXT_IS_SET(name)</code>. It takes a single argument and returns TRUE or FALSE depending on whether the calling application populated the context. It's narrower in scope than GET_CONTEXT and CHANGE_CONTEXTS — most production formulas never need it — but it's worth knowing the keyword exists so you recognise it in legacy code. The practical rule: if your formula type supports a given context, the calling application will set it; if it doesn't support that context, CHANGE_CONTEXTS is how you provide a value. CONTEXT_IS_SET fills the narrow gap where you need to distinguish "set to zero" from "never set at all" — a distinction that matters in a small number of edge cases, typically around optional plan or payroll contexts.</p>

<hr style="border:none;border-top:1px solid #e5e5e5;margin:34px 0">

<h2 style="font-size:22px;font-weight:700;margin:40px 0 14px;color:#1a1a1a">Key Takeaways</h2>

<p><strong>Two statements, two directions.</strong> GET_CONTEXT reads. CHANGE_CONTEXTS writes. Every context-handling pattern in Fast Formula is built from these two operations.</p>

<p><strong>GET_CONTEXT needs two arguments, always.</strong> The context name and a typed default. Forget the default and the formula won't compile.</p>

<p><strong>CHANGE_CONTEXTS auto-restores.</strong> Never write restore code. The engine handles save-and-swap on entry and restore on exit. Trust the scoping.</p>

<p><strong>Combine, don't nest.</strong> One CHANGE_CONTEXTS call with multiple assignments beats nested calls every time. Oracle's docs say so explicitly, and the cache-invalidation cost makes it a real best practice.</p>

<p><strong>Change only what you need.</strong> Every overridden context invalidates DBI caches. Be surgical.</p>

<div style="margin:26px 0;padding:22px 0;border-top:2px solid #000;border-bottom:2px solid #000;font-size:15px;display:table;width:100%;margin-top:40px"><div style="display:table-cell;width:80px;vertical-align:top;padding-right:18px"><div style="width:60px;height:60px;background:linear-gradient(135deg,#f57c3a 0%,#b8372a 100%);color:#fff;text-align:center;line-height:60px;font-weight:700;font-size:18px;border-radius:50%;letter-spacing:0.05em">AM</div></div><div style="display:table-cell;vertical-align:top"><strong>Abhishek Mohanty</strong><span>Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time and Labor, Core HR, Redwood, HDL, OTBI.</span></div></div>