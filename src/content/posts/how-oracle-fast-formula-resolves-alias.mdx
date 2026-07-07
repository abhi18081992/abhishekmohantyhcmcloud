---
title: "How Oracle Fast Formula resolves ALIAS at compile time: statement order, reference-vs-snapshot semantics, CHANGE_CONTEXTS re-evaluation, and the three compiler errors."
description: "The ALIAS Statement in Oracle Fast Formula — Compile-Time Reference, Statement Order, CHANGE_CONTEXTS Re-evaluation, and the Three Compiler Errors Every HCM Cloud Consultant Must Know :root{ --bg:#f5f"
pubDate: 2026-05-16
tags: ["Fast Formula", "Oracle HCM Cloud", "Null Handling", "DBI", "CHANGE_CONTEXTS"]
---


<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The ALIAS Statement in Oracle Fast Formula — Compile-Time Reference, Statement Order, CHANGE_CONTEXTS Re-evaluation, and the Three Compiler Errors Every HCM Cloud Consultant Must Know</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f5f3ef;
  --page:#ffffff;
  --text:#1f1d1b;
  --soft:#5a5651;
  --muted:#8a857f;
  --rule:#dcd6cc;
  --rule-soft:#e8e2d6;
  --accent:#b73a2c;
  --accent-soft:#f4ddd7;
  --code-bg:#f0ece4;
  --code-text:#3a3631;
  --tbl-head:#5a1810;
  --tbl-head-text:#f4ede0;
  --tbl-zebra:#faf7f0;
}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{
  font-family:'Lato',Arial,Helvetica,sans-serif;
  background:var(--bg);
  color:var(--text);
  line-height:1.7;
  font-size:17px;
  -webkit-font-smoothing:antialiased;
}

/* page container */
.post{
  max-width:760px;
  margin:0 auto;
  background:var(--page);
  padding:54px 52px 64px;
  border-left:1px solid var(--rule);
  border-right:1px solid var(--rule);
  min-height:100vh;
}

/* ── HERO BLOCK ── */
.pill-tags{
  display:flex;
  flex-wrap:wrap;
  gap:8px;
  margin-bottom:22px;
}
.pill{
  display:inline-block;
  padding:11px 18px;
  font-family:'Lato',Arial,Helvetica,sans-serif;
  font-size:12.5px;
  font-weight:700;
  color:#ffffff;
  text-transform:uppercase;
  letter-spacing:1.6px;
  border-radius:5px;
  line-height:1;
  white-space:nowrap;
}
.pill-red{background:#c2392b}
.pill-navy{background:#1f2d3d}
.pill-purple{background:#7e3da3}
.pill-teal{background:#1a6b6b}
.pill-amber{background:#a06814}
h1.title{
  font-family:'Lato',Arial,Helvetica,sans-serif;
  font-size:36px;
  font-weight:800;
  line-height:1.2;
  letter-spacing:-0.5px;
  color:#2a0f0a;
  margin-bottom:14px;
}
.subtitle{
  font-family:'Lato',Arial,Helvetica,sans-serif;
  font-size:20px;
  font-weight:400;
  line-height:1.5;
  color:#5a4338;
  font-style:italic;
  margin-bottom:18px;
}
.meta{
  font-size:14px;
  color:var(--muted);
  margin-bottom:24px;
  letter-spacing:0.2px;
}
.meta .sep{margin:0 6px;color:var(--rule)}

.lede{
  font-size:18px;
  line-height:1.65;
  color:var(--text);
  margin-bottom:28px;
}

/* ── BYLINE TABLE (the signature element) ── */
table.byline{
  width:100%;
  border-collapse:collapse;
  margin:8px 0 36px;
  border:1px solid var(--rule);
  background:#fbf8f1;
}
table.byline td{
  padding:14px 18px;
  vertical-align:middle;
}
table.byline td.avatar{
  width:64px;
  text-align:center;
  background:var(--accent);
  color:#fff;
  font-weight:700;
  font-size:16px;
  letter-spacing:1.5px;
  border-right:1px solid var(--accent);
  font-family:'Lato',Arial,Helvetica,sans-serif;
}
table.byline td.name{font-size:14.5px;line-height:1.55}
table.byline td.name strong{
  display:block;
  font-size:15.5px;
  color:#0e0c0a;
  margin-bottom:2px;
  font-weight:700;
}
table.byline td.name span{color:var(--soft);font-size:13.5px}

/* ── BODY TYPOGRAPHY ── */
h2{
  font-family:'Lato',Arial,Helvetica,sans-serif;
  font-size:25px;
  font-weight:700;
  line-height:1.3;
  letter-spacing:-0.3px;
  color:#9c2818;
  margin:42px 0 16px;
  padding-bottom:8px;
  border-bottom:2px solid #ead6c8;
  position:relative;
}
h2::after{
  content:'';
  position:absolute;
  left:0;
  bottom:-2px;
  width:54px;
  height:2px;
  background:#c2392b;
}
h3{
  font-family:'Lato',Arial,Helvetica,sans-serif;
  font-size:20px;
  font-weight:600;
  line-height:1.35;
  color:#1e3a5e;
  margin:32px 0 12px;
}
h4{
  font-family:'Lato',Arial,Helvetica,sans-serif;
  font-size:16px;
  font-weight:700;
  color:#b73a2c;
  margin:24px 0 10px;
  letter-spacing:0.1px;
}
p{margin-bottom:16px;line-height:1.7}
strong{font-weight:700;color:#0e0c0a}
em{font-style:italic}
a{color:var(--accent);text-decoration:underline;text-underline-offset:3px}

ul,ol{margin:0 0 18px 22px}
li{margin-bottom:7px;line-height:1.65}

/* ── INLINE CODE ── */
code{
  font-family:'JetBrains Mono',monospace;
  font-size:0.86em;
  background:var(--code-bg);
  color:#7a2618;
  padding:1.5px 6px;
  border-radius:2px;
  font-weight:500;
  letter-spacing:-0.3px;
}
h1 code,h2 code,h3 code,h4 code{font-size:0.78em;background:var(--accent-soft)}

/* ── CODE BLOCKS — simple indented look ── */
.codeblock{
  background:var(--code-bg);
  border-left:3px solid var(--rule);
  padding:16px 20px;
  margin:18px 0;
  font-family:'JetBrains Mono',monospace;
  font-size:13.5px;
  line-height:1.7;
  color:var(--code-text);
  overflow-x:auto;
  white-space:pre;
  border-radius:2px;
}
.codeblock .cm{color:#9a8a78;font-style:italic}
.codeblock .kw{color:#7a2618;font-weight:600}
.codeblock .st{color:#7a5a18}
.codeblock .nm{color:#a04020}

/* ── REFERENCE TABLES (signature element) ── */
.tblwrap{margin:22px 0;overflow-x:auto}
table.ref{
  width:100%;
  border-collapse:collapse;
  border:1px solid var(--rule);
  background:var(--page);
  font-size:14.5px;
  line-height:1.55;
}
table.ref th{
  background:var(--tbl-head);
  color:var(--tbl-head-text);
  text-align:left;
  padding:11px 16px;
  font-weight:600;
  font-size:13.5px;
  letter-spacing:0.2px;
}
table.ref td{
  padding:11px 16px;
  border-top:1px solid var(--rule);
  vertical-align:top;
  color:var(--text);
}
table.ref tr:nth-child(even) td{background:var(--tbl-zebra)}
table.ref td code{font-size:0.92em}
table.ref td strong{color:#0e0c0a}

/* Single-column reference table with title row */
table.ref.single th{font-style:italic;font-weight:600}
table.ref.single td:only-child{padding:11px 16px}

/* Step row — flex layout for reliable pill alignment */
table.ref td .step-row{
  display:flex;
  align-items:flex-start;
  gap:14px;
}
table.ref td .step-row .step-num{
  flex-shrink:0;
  display:inline-block;
  font-family:'JetBrains Mono',monospace;
  font-size:11.5px;
  font-weight:700;
  color:#ffffff;
  background:#9c2818;
  padding:5px 11px;
  border-radius:3px;
  letter-spacing:0.8px;
  white-space:nowrap;
  line-height:1.3;
  min-width:74px;
  text-align:center;
}
table.ref td .step-row .step-body{
  flex:1;
  line-height:1.65;
  padding-top:1px;
}
table.ref td .step-row .step-body code{font-size:0.9em}

/* ── HR DIVIDER ── */
hr{
  border:none;
  border-top:1px solid var(--rule);
  margin:32px 0;
  position:relative;
}

/* ── INLINE NOTE / ITALIC PULL ── */
.italic-note{
  font-style:italic;
  color:var(--soft);
  font-size:15.5px;
  margin:18px 0;
  padding-left:18px;
  border-left:2px solid var(--rule);
  line-height:1.65;
}

/* ── ERROR DISPLAY ── */
.error-line{
  font-family:'JetBrains Mono',monospace;
  font-size:13px;
  background:#2c2925;
  color:#f4a8a0;
  padding:11px 16px;
  border-radius:2px;
  margin:10px 0 18px;
  font-style:italic;
  line-height:1.55;
}
.error-line::before{
  content:'FF Compile Error  ';
  font-style:normal;
  font-weight:700;
  color:#f4ede0;
  font-size:11px;
  letter-spacing:1px;
  text-transform:uppercase;
}

/* ── TAGS AT FOOTER ── */
.tags{
  margin:34px 0 0;
  padding-top:20px;
  border-top:1px solid var(--rule);
  font-size:14px;
}
.tags a{
  color:var(--accent);
  text-decoration:none;
  margin-right:14px;
  letter-spacing:0.1px;
}
.tags a:hover{text-decoration:underline}

/* mobile */
@media(max-width:680px){
  .post{padding:32px 22px 48px;border-left:none;border-right:none}
  h1.title{font-size:27px}
  .subtitle{font-size:17px}
  h2{font-size:22px}
  h3{font-size:18px}
  body{font-size:16px}
  .codeblock{font-size:12.5px;padding:13px 16px}
  table.ref{font-size:13.5px}
  table.ref th,table.ref td{padding:10px 12px}
  table.byline td{padding:11px 14px}
  table.byline td.avatar{width:50px;font-size:14px}
}

/* ── DIAGRAMS ── */
.figure{
  margin:28px 0;
  padding:22px 22px 16px;
  background:#fbf8f1;
  border:1px solid #e8dfd0;
  border-radius:6px;
}
.figure-title{
  font-family:'Lato',Arial,sans-serif;
  font-size:11.5px;
  font-weight:700;
  color:#5a4338;
  text-transform:uppercase;
  letter-spacing:1.6px;
  text-align:center;
  margin-bottom:14px;
}
.figure-caption{
  font-family:'Lato',Arial,sans-serif;
  font-size:13px;
  color:#5a5651;
  font-style:italic;
  text-align:center;
  margin-top:12px;
  line-height:1.55;
  padding:0 10px;
}
.figure-caption strong{color:#1f1d1b;font-style:normal;font-weight:600}
.svg-figure{width:100%;height:auto;display:block}
.svg-title{font:700 12px 'Lato',Arial,sans-serif;fill:#5a4338;letter-spacing:1.4px}
.svg-label{font:600 10.5px 'Lato',Arial,sans-serif;fill:#5a4338;letter-spacing:1.1px}
.svg-label-tag{font:italic 500 11px 'Lato',Arial,sans-serif;fill:#8a857f}
.svg-label-context{font:700 10.5px 'Lato',Arial,sans-serif;fill:#1c3960;letter-spacing:0.8px}
.svg-code{font:500 13px 'JetBrains Mono',monospace;fill:#1f1d1b}
.svg-code-sm{font:500 11.5px 'JetBrains Mono',monospace;fill:#1f1d1b}
.svg-text{font:400 12.5px 'Lato',Arial,sans-serif;fill:#1f1d1b}
.svg-text-sm{font:400 11.5px 'Lato',Arial,sans-serif;fill:#5a5651}
.svg-handle{font:700 11.5px 'Lato',Arial,sans-serif;fill:#ffffff;letter-spacing:1.2px}
.svg-header{font:700 11.5px 'Lato',Arial,sans-serif;fill:#ffffff;letter-spacing:1.3px}
.svg-value-good{font:600 12px 'JetBrains Mono',monospace;fill:#2e6b3a}
.svg-value-bad{font:600 12px 'JetBrains Mono',monospace;fill:#b73a2c}
.svg-value-big{font:700 17px 'JetBrains Mono',monospace;fill:#9c2818;letter-spacing:0.4px}
.svg-result-good{font:700 13px 'JetBrains Mono',monospace;fill:#2e6b3a;letter-spacing:0.4px}
.svg-result-bad{font:700 13px 'JetBrains Mono',monospace;fill:#b73a2c;letter-spacing:0.4px}
</style>
</head>
<body>

<article class="post">


<div class="pill-tags">
  <span class="pill pill-red">FAST FORMULA</span>
  <span class="pill pill-navy">ALIAS STATEMENT</span>
  <span class="pill pill-purple">DEEP DIVE</span>
</div>

<h1 class="title">Oracle Fast Formula ALIAS: How the Compiler Resolves Long DBI Names at Parse Time and Why It's Not Just a Typing Convenience</h1>

<div class="subtitle">A definitive walkthrough of compile-time reference semantics, statement ordering, the reference-vs-snapshot distinction, CHANGE_CONTEXTS re-evaluation, and the three compiler errors every Fast Formula author has hit at least once.</div>

<div class="meta">May 8, 2026 <span class="sep">•</span> 16 min read <span class="sep">•</span> Oracle HCM Cloud</div>

<p class="lede">Database item names in Fusion HCM Fast Formulas routinely run past thirty characters. <code>PER_ASG_REL_LENGTH_OF_SERVICE</code>. <code>CMP_ASSIGNMENT_RGE_SALARY_CHANGE_AMOUNT</code>. <code>PER_HIST_ASG_EFFECTIVE_START_DATE</code>. Reference one of these eight times in a single formula and the calculation logic disappears under the noise. Oracle's documented answer is the <code>ALIAS</code> statement — a single keyword, an <code>AS</code> clause, a target identifier. But ALIAS is more than a typing shortcut. It's a compile-time reference, not a runtime variable, and that distinction matters more than most authors realise.</p>

<table class="byline">
<tr>
  <td class="avatar">AM</td>
  <td class="name"><strong>Abhishek Mohanty</strong><span>Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant</span></td>
</tr>
</table>

<p>Fast Formula has no debugger. It also has no convenient way to fold a 38-character DBI reference into something readable — except for ALIAS. Authors who reach for <code>L_VAR = LONG_DBI_NAME</code> instead end up with a snapshot variable that silently breaks under <code>CHANGE_CONTEXTS</code>, and they don't find out until a salary delta computes to zero in production.</p>

<p>This post covers what ALIAS actually does at the language level, where it must sit in your statement order, why it's not interchangeable with a local-variable assignment, the three compiler errors you'll hit, and the production conventions that keep aliased formulas readable six months after go-live.</p>

<hr>


<h2>ALIAS in the Five-Section Formula Structure</h2>

<p>Before going deep into ALIAS semantics, it helps to see where ALIAS sits in the larger Fast Formula skeleton. Every formula you'll ever write follows the same five-section template, in exactly this order:</p>

<div class="tblwrap">
<table class="ref">
<thead><tr><th>Position</th><th>Section</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><strong>1</strong></td><td><code>ALIAS</code></td><td>Shortens long DBI names. Compile-time symbol binding.</td></tr>
<tr><td><strong>2</strong></td><td><code>DEFAULT FOR</code></td><td>Null-handling for database items, including aliased ones.</td></tr>
<tr><td><strong>3</strong></td><td><code>INPUTS ARE</code></td><td>Typed parameters passed in by the calling formula type.</td></tr>
<tr><td><strong>4</strong></td><td>Calculation body</td><td>Assignments, IF / THEN / ELSE, function calls — the actual logic.</td></tr>
<tr><td><strong>5</strong></td><td><code>RETURN</code></td><td>One or more values handed back to the calling application.</td></tr>
</tbody>
</table>
</div>

<p>A complete minimal formula showing all five sections in order:</p>

<div class="codeblock"><span class="kw">ALIAS</span> CMP_ASSIGNMENT_SALARY_AMOUNT <span class="kw">AS</span> ASG_SAL        <span class="cm">/* 1. ALIAS — shortens the DBI         */</span>
<span class="kw">ALIAS</span> ASG_HR_ASG_ID                <span class="kw">AS</span> ASG_ID         <span class="cm">/*    one alias per line               */</span>

<span class="kw">DEFAULT FOR</span> ASG_SAL <span class="kw">IS</span> <span class="nm">0</span>                              <span class="cm">/* 2. DEFAULT — null handling          */</span>
<span class="kw">DEFAULT FOR</span> ASG_ID  <span class="kw">IS</span> <span class="nm">0</span>

<span class="kw">INPUTS ARE</span> BONUS_PERCENTAGE                          <span class="cm">/* 3. INPUTS — typed parameters        */</span>

L_BONUS = ASG_SAL * (BONUS_PERCENTAGE / <span class="nm">100</span>)              <span class="cm">/* 4. CALCULATION — the logic itself   */</span>

<span class="kw">RETURN</span> L_BONUS, ASG_ID                                 <span class="cm">/* 5. RETURN — values passed back      */</span></div>

<p>One structural fact about ALIAS matters for understanding everything that follows: <strong>ALIAS resolution happens at compile time, not at runtime.</strong> By the time the runtime execution begins, every alias has already been substituted with the underlying DBI's fetch logic. The alias has no independent existence at runtime — it's a label the compiler removes.</p>

<p class="italic-note">This second point is the key insight the rest of this post unpacks. Because ALIAS is resolved before the formula body even starts running, the alias inherits the semantic properties of the underlying DBI — lazy evaluation, context-sensitive re-fetching, <code>WAS DEFAULTED</code> compatibility — that a local-variable assignment cannot reproduce.</p>

<hr>


<h2>How the Compiler Resolves an Alias</h2>

<p>The Oracle <em>Administering Fast Formulas</em> guide defines ALIAS as a statement that gives a Database Item a shorter, formula-local name. The guide explicitly recommends ALIAS over assigning a DBI to a local variable for the purpose of shortening — because the alias is a reference, not a copy.</p>

<p>The binding happens at compile time. The compiler builds a symbol table that maps both the long DBI name and your short alias to the same metadata handle:</p>

<div class="tblwrap">
<table class="ref">
<thead><tr><th>Database Item</th><th>Alias</th></tr></thead>
<tbody>
<tr><td><code>PER_ASG_REL_LENGTH_OF_SERVICE</code></td><td><code>ASG_LOS</code></td></tr>
<tr><td><code>CMP_ASSIGNMENT_SALARY_AMOUNT</code></td><td><code>ASG_SAL</code></td></tr>
<tr><td><code>PER_ASG_JOB_NAME</code></td><td><code>ASG_JOB</code></td></tr>
<tr><td><code>ASG_HR_ASG_ID</code></td><td><code>ASG_ID</code></td></tr>
</tbody>
</table>
</div>

<div class="figure">
<div class="figure-title">Figure 1 · Compile-Time Binding</div>
<svg class="svg-figure" viewBox="0 0 660 220" xmlns="http://www.w3.org/2000/svg">
  <text x="160" y="28" text-anchor="middle" class="svg-label-tag">declared by ALIAS</text>
  <rect x="20" y="44" width="280" height="38" rx="3" fill="#ffffff" stroke="#c8c0b4" stroke-width="1.2"/>
  <text x="160" y="68" text-anchor="middle" class="svg-code">CMP_ASSIGNMENT_SALARY_AMOUNT</text>
  <rect x="20" y="124" width="280" height="38" rx="3" fill="#ffffff" stroke="#c8c0b4" stroke-width="1.2"/>
  <text x="160" y="148" text-anchor="middle" class="svg-code">ASG_SAL</text>
  <path d="M 305 63 Q 380 63 412 100" fill="none" stroke="#5a4338" stroke-width="1.5"/>
  <path d="M 305 143 Q 380 143 412 110" fill="none" stroke="#5a4338" stroke-width="1.5"/>
  <polygon points="408,97 418,104 412,107" fill="#5a4338"/>
  <polygon points="408,113 418,106 412,103" fill="#5a4338"/>
  <text x="525" y="70" text-anchor="middle" class="svg-label-tag">resolves to</text>
  <rect x="420" y="84" width="210" height="56" rx="4" fill="#9c2818"/>
  <text x="525" y="108" text-anchor="middle" class="svg-handle">ONE METADATA</text>
  <text x="525" y="126" text-anchor="middle" class="svg-handle">HANDLE</text>
  <line x1="20" y1="184" x2="640" y2="184" stroke="#e0d8c8" stroke-width="1"/>
  <text x="330" y="206" text-anchor="middle" class="svg-text-sm">Both names share the same route, user-entity, and context dependency.</text>
</svg>
<div class="figure-caption"><strong>One handle, two labels.</strong> Reading either name at runtime triggers the same DBI fetch under whichever contexts are active.</div>
</div>

<p>Four things happen behind the scenes when you write the ALIAS line:</p>

<div class="tblwrap">
<table class="ref single">
<thead><tr><th>What the compiler does with each ALIAS declaration</th></tr></thead>
<tbody>
<tr><td><div class="step-row"><span class="step-num">STEP 1</span><div class="step-body">You write the ALIAS line: <code>ALIAS PER_ASG_REL_LENGTH_OF_SERVICE AS ASG_LOS</code> at the top of the formula.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">STEP 2</span><div class="step-body">The compiler records both names — long DBI and short alias — as labels pointing to the same route and user-entity in the formula metadata. They become two names for one underlying handle.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">STEP 3</span><div class="step-body">Every later reference to the alias in the formula body resolves to the exact same DBI fetch logic that the long name would have produced. The substitution is complete before any runtime execution.</div></div></td></tr>
</tbody>
</table>
</div>

<p class="italic-note">The alias is a label processed at compile time. There is no runtime storage allocated to it, and no separate value held against it. Every reference is a fresh evaluation of the underlying DBI under whatever contexts are active at the point of reference.</p>

<hr>


<h2>Syntax and the Reserved Identifier List</h2>

<p>The form is fixed. One alias declaration per line:</p>

<div class="codeblock"><span class="kw">ALIAS</span> DATABASE_ITEM_NAME <span class="kw">AS</span> SHORT_NAME</div>

<p>Three things to know about the syntax:</p>

<ol>
<li><strong>The <code>AS</code> keyword is required.</strong> Both <code>ALIAS</code> and <code>AS</code> are reserved — neither can be used as a variable name elsewhere in the formula.</li>
<li><strong>Case-insensitive.</strong> <code>ALIAS x AS Y</code> and <code>alias X as y</code> compile identically. Pick a casing convention and apply it consistently.</li>
<li><strong>One alias per line.</strong> No comma-separated multi-alias declarations.</li>
</ol>

<p>The alias name on the right of <code>AS</code> can't collide with any reserved word in the language. The reserved identifiers fall into six categories:</p>

<div class="tblwrap">
<table class="ref">
<thead><tr><th>Category</th><th>Reserved identifiers</th></tr></thead>
<tbody>
<tr><td><strong>Declaration & section statements</strong></td><td><code>ALIAS</code>, <code>AS</code>, <code>DEFAULT</code>, <code>DEFAULT_DATA_VALUE</code>, <code>DEFAULTED</code>, <code>FOR</code>, <code>INPUTS</code>, <code>ARE</code>, <code>USING</code>, <code>RETURN</code></td></tr>
<tr><td><strong>Control flow</strong></td><td><code>IF</code>, <code>THEN</code>, <code>ELSE</code>, <code>WHILE</code>, <code>LOOP</code>, <code>EXIT</code></td></tr>
<tr><td><strong>Logical & comparison operators</strong></td><td><code>AND</code>, <code>OR</code>, <code>NOT</code>, <code>IS</code>, <code>LIKE</code>, <code>WAS</code></td></tr>
<tr><td><strong>Context management</strong></td><td><code>CHANGE_CONTEXTS</code>, <code>GET_CONTEXT</code>, <code>CONTEXT_IS_SET</code>, <code>NEED_CONTEXT</code></td></tr>
<tr><td><strong>Formula execution & I/O</strong></td><td><code>EXECUTE</code>, <code>IS_EXECUTABLE</code>, <code>SET_INPUT</code>, <code>GET_OUTPUT</code></td></tr>
<tr><td><strong>Working storage area</strong></td><td><code>WSA_GET</code>, <code>WSA_SET</code>, <code>WSA_EXISTS</code>, <code>WSA_DELETE</code></td></tr>
</tbody>
</table>
</div>

<p>If your formula won't compile and you've named your alias something like <code>DEFAULT</code>, <code>FOR</code>, or <code>IS</code> — that's why. Add a prefix or suffix to escape: <code>L_DEFAULT</code>, <code>FOR_DT</code>, <code>IS_FLAG</code>.</p>

<hr>


<h2>Statement Order: Why ALIAS Comes First</h2>

<p>Fast Formula enforces a strict ordering of declarative statement sections. The order is documented in the Oracle <em>Administering Fast Formulas</em> guide, and the compiler will reject your formula with <em>"Incorrect Statement Order"</em> if you break it.</p>

<div class="tblwrap">
<table class="ref single">
<thead><tr><th>Required statement order — top to bottom</th></tr></thead>
<tbody>
<tr><td><div class="step-row"><span class="step-num">FIRST</span><div class="step-body"><strong>ALIAS</strong> — all alias declarations, grouped together at the top of the formula.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">SECOND</span><div class="step-body"><strong>DEFAULT FOR</strong> and <strong>DEFAULT_DATA_VALUE FOR</strong> — scalar and array DBI defaults.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">THIRD</span><div class="step-body"><strong>INPUTS ARE</strong> — single block, all input parameters typed.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">FOURTH</span><div class="step-body"><strong>Body and RETURN</strong> — logic, control flow, assignments, and the return statement.</div></div></td></tr>
</tbody>
</table>
</div>

<h3>What going out of order looks like</h3>

<p>The mistake is genuinely common when you're refactoring an existing formula and adding an alias mid-file. Wrong:</p>

<div class="codeblock"><span class="kw">DEFAULT FOR</span> ASG_HR_ASG_ID <span class="kw">IS</span> <span class="nm">0</span>      <span class="cm">/* DEFAULT before ALIAS */</span>

<span class="kw">ALIAS</span> PER_ASG_JOB_NAME <span class="kw">AS</span> ASG_JOB     <span class="cm">/* ← raises the error */</span>

<span class="kw">INPUTS ARE</span> EFFECTIVE_DATE_FROM (<span class="kw">DATE</span>)</div>

<div class="error-line">Incorrect Statement Order — ALIAS, DEFAULT, or INPUT statements come after other statements.</div>

<p>Right:</p>

<div class="codeblock"><span class="kw">ALIAS</span> PER_ASG_JOB_NAME <span class="kw">AS</span> ASG_JOB

<span class="kw">DEFAULT FOR</span> ASG_HR_ASG_ID <span class="kw">IS</span> <span class="nm">0</span>
<span class="kw">DEFAULT FOR</span> ASG_JOB <span class="kw">IS</span> <span class="st">' '</span>

<span class="kw">INPUTS ARE</span> EFFECTIVE_DATE_FROM (<span class="kw">DATE</span>)</div>

<p class="italic-note">When adding a new alias to an existing formula, scroll to the top, find the existing ALIAS block, and add the line there. Never insert it next to the DEFAULT or DBI it relates to — that breaks the ordering rule.</p>

<hr>


<h2>What You Can & Cannot Alias</h2>

<p>The Fusion 24D <em>Administering Fast Formulas</em> guide narrows ALIAS to one target type: database items. The compiler diagnostic for invalid targets is unambiguous: <em>"you can use an ALIAS statement only for a database item."</em> The practical test is the Database Items picker in the formula editor — if the identifier appears there for your current formula type, it's aliasable; if it doesn't, it isn't.</p>

<h3>What ALIAS will accept</h3>

<div class="tblwrap">
<table class="ref">
<thead><tr><th>Aliasable</th><th>Notes</th></tr></thead>
<tbody>
<tr><td><strong>Scalar DBIs</strong></td><td>The standard case. Any DBI returning a single text, number, or date value under the formula type's contexts.</td></tr>
<tr><td><strong>Array DBIs</strong></td><td>Grammatically aliasable. Oracle docs are silent — no worked example in the 24D guide — but the language accepts it. Test in your environment before relying on it.</td></tr>
</tbody>
</table>
</div>

<h3>What ALIAS will not accept</h3>

<p>Five identifier categories produce compilation failures. The diagnostic, the cause, and a reproduction case for each:</p>

<h4>1. Local variables</h4>

<p>Local variables don't exist until the formula's first assignment statement creates them. ALIAS lines run before any assignment, so the symbol has no metadata to bind to.</p>

<div class="codeblock"><span class="kw">ALIAS</span> L_TEMP_VALUE <span class="kw">AS</span> TMP        <span class="cm">/* L_TEMP_VALUE is a local var, not a DBI */</span></div>

<div class="error-line">Misuse of ALIAS Statement — you can use an ALIAS statement only for a database item.</div>

<h4>2. Inputs from INPUTS ARE</h4>

<p>Inputs are bound to the formula via the formula type definition. They're not DBIs and they're already short. There's no metadata layer to alias.</p>

<div class="codeblock"><span class="kw">ALIAS</span> EFFECTIVE_DATE_FROM <span class="kw">AS</span> EFF_DT   <span class="cm">/* declared in INPUTS ARE */</span></div>

<div class="error-line">Misuse of ALIAS Statement — you can use an ALIAS statement only for a database item.</div>

<h4>3. Contexts</h4>

<p>Contexts like <code>HR_ASSIGNMENT_ID</code>, <code>EFFECTIVE_DATE</code>, <code>ABSENCE_PLAN_ID</code>, <code>PERSON_ID</code> are language-level handles for the current evaluation state, not data records. Read them via <code>GET_CONTEXT</code>.</p>

<div class="codeblock"><span class="kw">ALIAS</span> HR_ASSIGNMENT_ID <span class="kw">AS</span> AID         <span class="cm">/* contexts are not DBIs */</span>

<span class="cm">/* Correct method for context access: */</span>
L_AID = GET_CONTEXT(HR_ASSIGNMENT_ID, <span class="nm">-1</span>)</div>

<div class="error-line">Misuse of ALIAS Statement — you can use an ALIAS statement only for a database item.</div>

<h4>4. Formula functions</h4>

<p>Functions like <code>GET_VALUE_SET</code>, <code>DAYS_BETWEEN</code>, <code>ESS_LOG_WRITE</code>, <code>GET_RATE</code>, <code>TO_CHAR</code>, <code>SUBSTR</code> are callable, not data. They take parameters and return values; they don't <em>have</em> a value to alias.</p>

<div class="codeblock"><span class="kw">ALIAS</span> DAYS_BETWEEN <span class="kw">AS</span> DB             <span class="cm">/* functions cannot be aliased */</span></div>

<div class="error-line">Misuse of ALIAS Statement — you can use an ALIAS statement only for a database item.</div>

<h4>5. DBIs not visible to your formula type</h4>

<p>The trickiest case because it <em>looks</em> correct. The DBI exists in the dictionary somewhere. But your current formula type doesn't supply the contexts the DBI's route needs, so for your formula it doesn't exist. The diagnostic differs — the compiler reports <em>"Unknown Variable"</em> on the long name itself.</p>

<div class="codeblock"><span class="cm">/* In an Absence Entry Validation formula, no benefits contexts are supplied. */</span>
<span class="cm">/* The DBI exists in the dictionary but is invisible to this formula type.   */</span>
<span class="kw">ALIAS</span> BEN_PEN_BNFT_AMT_NN <span class="kw">AS</span> BNFT_AMT</div>

<div class="error-line">Unknown Variable: BEN_PEN_BNFT_AMT_NN</div>

<p class="italic-note"><strong>Diagnostic heuristic:</strong> "Misuse of ALIAS Statement" means the left-hand identifier is recognised by the compiler but isn't a DBI (input, context, function, local variable). "Unknown Variable" means the name simply doesn't resolve in your formula type — typo, wrong formula type, or a DBI requiring contexts you don't have.</p>

<h3>Should I alias this? — three quick checks</h3>

<div class="tblwrap">
<table class="ref single">
<thead><tr><th>The three-question decision</th></tr></thead>
<tbody>
<tr><td><div class="step-row"><span class="step-num">CHECK 1</span><div class="step-body">Is the identifier in the Database Items picker for this formula type? If no — stop. ALIAS will fail.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">CHECK 2</span><div class="step-body">Will I reference it more than once, OR is its name longer than ~25 characters? If neither — don't bother. The alias adds noise without paying for itself.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">CHECK 3</span><div class="step-body">Have I picked a short, project-consistent, non-reserved alias name? If no — go back to your project's naming convention.</div></div></td></tr>
</tbody>
</table>
</div>

<p>Three yeses → declare the alias in the ALIAS block at the top of the formula. Add a one-line trailing comment describing what the DBI represents in business terms. Use the alias name uniformly in body references, in <code>DEFAULT FOR</code>, and in any <code>WAS DEFAULTED</code> checks.</p>

<hr>


<h2>The Reference vs Snapshot Distinction</h2>

<p>ALIAS and <code>L_VAR = LONG_DBI_NAME</code> are not equivalent. They have different runtime behaviour, and one of them silently produces wrong answers under <code>CHANGE_CONTEXTS</code>.</p>

<h3>The local-variable pattern (anti-pattern for shortening)</h3>

<div class="codeblock"><span class="kw">DEFAULT FOR</span> PER_ASG_REL_LENGTH_OF_SERVICE <span class="kw">IS</span> <span class="nm">0</span>

<span class="cm">/* Read the DBI once into a local variable for shorter access */</span>
L_ASG_LOS = PER_ASG_REL_LENGTH_OF_SERVICE

<span class="kw">IF</span> L_ASG_LOS >= <span class="nm">5</span> <span class="kw">THEN</span>
   L_FLAG = <span class="st">'Y'</span></div>

<p>Two things happen on the assignment line that are not always evident from the source: the DBI is fetched eagerly at that point regardless of whether the value is later read, and the local variable holds a snapshot under whichever contexts were active at assignment — any later <code>CHANGE_CONTEXTS</code> block does not update it.</p>

<h3>The ALIAS pattern</h3>

<div class="codeblock"><span class="kw">ALIAS</span> PER_ASG_REL_LENGTH_OF_SERVICE <span class="kw">AS</span> ASG_LOS

<span class="kw">DEFAULT FOR</span> ASG_LOS <span class="kw">IS</span> <span class="nm">0</span>

<span class="kw">IF</span> ASG_LOS >= <span class="nm">5</span> <span class="kw">THEN</span>
   L_FLAG = <span class="st">'Y'</span></div>

<p>Functionally similar in this isolated case. But four behavioural differences matter:</p>

<div class="tblwrap">
<table class="ref">
<thead><tr><th>Property</th><th>Local-variable assignment</th><th>ALIAS</th></tr></thead>
<tbody>
<tr><td><strong>DBI evaluation timing</strong></td><td>Eager — fetched at assignment, regardless of later use.</td><td>Lazy — fetched only when a code path actually evaluates the alias.</td></tr>
<tr><td><strong>Behaviour under CHANGE_CONTEXTS</strong></td><td>Frozen at original assignment context. Reads inside CHANGE_CONTEXTS return the original value.</td><td>Re-evaluates. Reads inside CHANGE_CONTEXTS fetch under the new context.</td></tr>
<tr><td><strong>Runtime memory</strong></td><td>Allocates a variable slot in the generated PL/SQL package.</td><td>No runtime allocation; resolved at compile time.</td></tr>
<tr><td><strong>WAS DEFAULTED compatibility</strong></td><td>Not supported. The check requires DBI metadata, lost in assignment.</td><td>Fully supported. Behaves identically to the underlying DBI.</td></tr>
</tbody>
</table>
</div>

<div class="figure">
<div class="figure-title">Figure 2 · Reference vs Snapshot — Same Logic, Different Runtime Behaviour</div>
<svg class="svg-figure" viewBox="0 0 680 360" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="14" width="310" height="32" rx="3" fill="#7a3a2b"/>
  <text x="175" y="35" text-anchor="middle" class="svg-header">LOCAL VARIABLE  ·  SNAPSHOT</text>
  <rect x="350" y="14" width="310" height="32" rx="3" fill="#9c2818"/>
  <text x="505" y="35" text-anchor="middle" class="svg-header">ALIAS  ·  REFERENCE</text>

  <rect x="20" y="62" width="310" height="68" rx="3" fill="#ffffff" stroke="#c8c0b4" stroke-width="1"/>
  <text x="32" y="80" class="svg-label-tag">Line 4 — initial context active</text>
  <text x="32" y="100" class="svg-code-sm">L_SAL = CMP_ASSIGNMENT_SALARY_AMOUNT</text>
  <text x="32" y="120" class="svg-value-bad">→ fetched · stored as $75,000</text>

  <rect x="350" y="62" width="310" height="68" rx="3" fill="#ffffff" stroke="#c8c0b4" stroke-width="1"/>
  <text x="362" y="80" class="svg-label-tag">Line 4 — declaration only</text>
  <text x="362" y="100" class="svg-code-sm">ALIAS CMP_..._SALARY_AMOUNT AS ASG_SAL</text>
  <text x="362" y="120" class="svg-value-good">→ no fetch yet · label only</text>

  <rect x="20" y="142" width="310" height="68" rx="3" fill="#fdf3f1" stroke="#c8c0b4" stroke-width="1"/>
  <text x="32" y="160" class="svg-label-tag">inside CHANGE_CONTEXTS (start_dt)</text>
  <text x="32" y="180" class="svg-code-sm">L_START_SAL = L_SAL</text>
  <text x="32" y="200" class="svg-value-bad">→ $75,000  (frozen — original ctx)</text>

  <rect x="350" y="142" width="310" height="68" rx="3" fill="#f3f8f4" stroke="#c8c0b4" stroke-width="1"/>
  <text x="362" y="160" class="svg-label-tag">inside CHANGE_CONTEXTS (start_dt)</text>
  <text x="362" y="180" class="svg-code-sm">L_START_SAL = ASG_SAL</text>
  <text x="362" y="200" class="svg-value-good">→ $75,000  (fresh fetch under start_dt)</text>

  <rect x="20" y="222" width="310" height="68" rx="3" fill="#fdf3f1" stroke="#c8c0b4" stroke-width="1"/>
  <text x="32" y="240" class="svg-label-tag">inside CHANGE_CONTEXTS (end_dt)</text>
  <text x="32" y="260" class="svg-code-sm">L_END_SAL = L_SAL</text>
  <text x="32" y="280" class="svg-value-bad">→ $75,000  (still frozen — wrong)</text>

  <rect x="350" y="222" width="310" height="68" rx="3" fill="#f3f8f4" stroke="#c8c0b4" stroke-width="1"/>
  <text x="362" y="240" class="svg-label-tag">inside CHANGE_CONTEXTS (end_dt)</text>
  <text x="362" y="260" class="svg-code-sm">L_END_SAL = ASG_SAL</text>
  <text x="362" y="280" class="svg-value-good">→ $82,500  (fresh fetch under end_dt)</text>

  <rect x="20" y="306" width="310" height="38" rx="3" fill="#fbecea" stroke="#b73a2c" stroke-width="1.2"/>
  <text x="175" y="330" text-anchor="middle" class="svg-result-bad">L_DELTA = $0  →  WRONG</text>

  <rect x="350" y="306" width="310" height="38" rx="3" fill="#eaf4ec" stroke="#2e6b3a" stroke-width="1.2"/>
  <text x="505" y="330" text-anchor="middle" class="svg-result-good">L_DELTA = $7,500  →  CORRECT</text>
</svg>
<div class="figure-caption"><strong>The same three references, two different runtime behaviours.</strong> Local-variable assignment captures the value once at the assignment line; ALIAS re-evaluates the underlying DBI at every reference, under whatever context is active.</div>
</div>

<p class="italic-note">For shortening identifiers, ALIAS is the correct choice every time. Use local-variable assignment from a DBI only when a snapshot value is the explicit requirement — for instance, capturing a value at one context for comparison after a deliberate context change. In that case, name the variable accordingly: <code>L_SAL_AT_PERIOD_START</code> tells the next maintainer this is a snapshot.</p>

<hr>


<h2>DEFAULT FOR and WAS DEFAULTED Against the Alias</h2>

<p>Once an alias is declared, the rest of the formula — including <code>DEFAULT FOR</code> and <code>WAS DEFAULTED</code> — should reference the alias name. The compiler folds the alias and the underlying DBI into the same symbol, so writing the default against either resolves to the same metadata. Consistency is a maintenance discipline, not a compiler requirement:</p>

<div class="codeblock"><span class="kw">ALIAS</span> PER_ASG_JOB_NAME              <span class="kw">AS</span> ASG_JOB
<span class="kw">ALIAS</span> CMP_ASSIGNMENT_SALARY_AMOUNT <span class="kw">AS</span> ASG_SAL
<span class="kw">ALIAS</span> ASG_HR_ASG_ID                <span class="kw">AS</span> ASG_ID

<span class="cm">/* Defaults written against the alias names */</span>
<span class="kw">DEFAULT FOR</span> ASG_JOB <span class="kw">IS</span> <span class="st">' '</span>
<span class="kw">DEFAULT FOR</span> ASG_SAL <span class="kw">IS</span> <span class="nm">0</span>
<span class="kw">DEFAULT FOR</span> ASG_ID  <span class="kw">IS</span> <span class="nm">0</span>

<span class="kw">INPUTS ARE</span> EFFECTIVE_PERIOD_END (<span class="kw">DATE</span>)

<span class="cm">/* WAS DEFAULTED check against the alias */</span>
<span class="kw">IF</span> ASG_SAL <span class="kw">WAS DEFAULTED</span> <span class="kw">THEN</span>
   L_MSG = <span class="st">'Salary DBI returned NULL — defaulted to 0'</span></div>

<p>The <code>WAS DEFAULTED</code> check inspects whether the underlying DBI fetch returned NULL and triggered the <code>DEFAULT FOR</code> substitution. Because the alias and the DBI share a single metadata handle, asking <code>ASG_SAL WAS DEFAULTED</code> gives the same answer as asking the long name.</p>

<p class="italic-note"><strong>Don't mix names.</strong> Technically the compiler accepts <code>DEFAULT FOR PER_ASG_JOB_NAME IS ' '</code> followed by <code>IF ASG_JOB WAS DEFAULTED</code>. But it's a maintenance nightmare. Pick the alias and use it consistently.</p>

<hr>


<h2>ALIAS Inside CHANGE_CONTEXTS</h2>

<p>The reference-vs-snapshot distinction has its biggest payoff inside <code>CHANGE_CONTEXTS</code> blocks. Because the alias compiles to a DBI fetch operation, evaluating it under a different context produces a fresh fetch under that context — exactly as if you'd written the long DBI name explicitly:</p>

<div class="codeblock"><span class="kw">ALIAS</span> CMP_ASSIGNMENT_SALARY_AMOUNT <span class="kw">AS</span> ASG_SAL

<span class="kw">DEFAULT FOR</span> ASG_SAL <span class="kw">IS</span> <span class="nm">0</span>

<span class="kw">INPUTS ARE</span> PERIOD_START_DT (<span class="kw">DATE</span>), PERIOD_END_DT (<span class="kw">DATE</span>)

<span class="kw">CHANGE_CONTEXTS</span> (EFFECTIVE_DATE = PERIOD_START_DT)
(
   L_START_SAL = ASG_SAL          <span class="cm">/* fetch under PERIOD_START_DT */</span>
)

<span class="kw">CHANGE_CONTEXTS</span> (EFFECTIVE_DATE = PERIOD_END_DT)
(
   L_END_SAL = ASG_SAL            <span class="cm">/* re-fetch under PERIOD_END_DT */</span>
)

L_DELTA = L_END_SAL - L_START_SAL</div>

<p>Two reads of the same alias <code>ASG_SAL</code>, each fetching under a different <code>EFFECTIVE_DATE</code>, each producing a different value:</p>

<div class="figure">
<div class="figure-title">Figure 3 · ALIAS Re-Evaluates Under Each Context</div>
<svg class="svg-figure" viewBox="0 0 660 260" xmlns="http://www.w3.org/2000/svg">
  <rect x="260" y="20" width="140" height="42" rx="4" fill="#9c2818"/>
  <text x="330" y="46" text-anchor="middle" class="svg-handle">ASG_SAL</text>
  <text x="330" y="82" text-anchor="middle" class="svg-label-tag">one alias identifier · two code paths</text>

  <line x1="330" y1="96" x2="330" y2="110" stroke="#5a4338" stroke-width="1.5"/>
  <line x1="155" y1="110" x2="505" y2="110" stroke="#5a4338" stroke-width="1.5"/>
  <line x1="155" y1="110" x2="155" y2="126" stroke="#5a4338" stroke-width="1.5"/>
  <line x1="505" y1="110" x2="505" y2="126" stroke="#5a4338" stroke-width="1.5"/>

  <rect x="40" y="130" width="230" height="50" rx="4" fill="#ffffff" stroke="#1e3a5e" stroke-width="1.3"/>
  <text x="155" y="150" text-anchor="middle" class="svg-label-context">EFFECTIVE_DATE</text>
  <text x="155" y="169" text-anchor="middle" class="svg-code-sm">= PERIOD_START_DT</text>

  <rect x="390" y="130" width="230" height="50" rx="4" fill="#ffffff" stroke="#1e3a5e" stroke-width="1.3"/>
  <text x="505" y="150" text-anchor="middle" class="svg-label-context">EFFECTIVE_DATE</text>
  <text x="505" y="169" text-anchor="middle" class="svg-code-sm">= PERIOD_END_DT</text>

  <line x1="155" y1="184" x2="155" y2="206" stroke="#5a4338" stroke-width="1.5"/>
  <polygon points="150,202 160,202 155,212" fill="#5a4338"/>
  <line x1="505" y1="184" x2="505" y2="206" stroke="#5a4338" stroke-width="1.5"/>
  <polygon points="500,202 510,202 505,212" fill="#5a4338"/>

  <text x="155" y="240" text-anchor="middle" class="svg-value-big">$ 75,000</text>
  <text x="505" y="240" text-anchor="middle" class="svg-value-big">$ 82,500</text>
</svg>
<div class="figure-caption"><strong>Same alias, two contexts, two distinct values.</strong> Each evaluation is an independent DBI fetch under whichever context is active at that point in the code.</div>
</div>

<p>If the same logic were written using local-variable assignment at the top of the formula — <code>L_SAL = CMP_ASSIGNMENT_SALARY_AMOUNT</code> before any <code>CHANGE_CONTEXTS</code> block — the DBI would be fetched once under the formula's initial contexts. Reads of <code>L_SAL</code> inside both blocks would return the original frozen value. <code>L_DELTA</code> would silently evaluate to zero. No compiler diagnostic. No error message. Wrong answer.</p>

<p class="italic-note"><strong>Performance note:</strong> Every alias evaluation inside <code>CHANGE_CONTEXTS</code> is a potential database fetch. Use <code>CHANGE_CONTEXTS</code> only where context modification is required for correctness. Wrapping speculative or large code blocks in <code>CHANGE_CONTEXTS</code> introduces unnecessary re-fetches.</p>

<hr>


<h2>The Three Compiler Errors You'll Actually See</h2>

<p>The Oracle <em>Administering Fast Formulas</em> compilation-errors table lists several diagnostics that mention ALIAS. In practice, you'll bump into three of them repeatedly.</p>

<h3>Error 1 — Incorrect Statement Order</h3>

<div class="error-line">Incorrect Statement Order — ALIAS, DEFAULT, or INPUT statements come after other statements.</div>

<div class="codeblock"><span class="kw">DEFAULT FOR</span> ASG_HR_ASG_ID <span class="kw">IS</span> <span class="nm">0</span>      <span class="cm">/* DEFAULT precedes ALIAS — invalid */</span>

<span class="kw">ALIAS</span> PER_ASG_JOB_NAME <span class="kw">AS</span> ASG_JOB     <span class="cm">/* ← raises the diagnostic */</span>

<span class="kw">INPUTS ARE</span> EFFECTIVE_DATE_FROM (<span class="kw">DATE</span>)</div>

<p><strong>Fix:</strong> Reorder so that all ALIAS declarations precede all DEFAULT declarations. The required order is ALIAS → DEFAULT → INPUTS → body, every time.</p>

<h3>Error 2 — Misuse of ALIAS Statement</h3>

<div class="error-line">Misuse of ALIAS Statement — you can use an ALIAS statement only for a database item.</div>

<div class="codeblock"><span class="cm">/* Aliasing a context — invalid */</span>
<span class="kw">ALIAS</span> HR_ASSIGNMENT_ID <span class="kw">AS</span> ASG_ID         <span class="cm">/* ← context, not a DBI */</span>

<span class="cm">/* Aliasing an input — invalid */</span>
<span class="kw">ALIAS</span> EFFECTIVE_DATE_FROM <span class="kw">AS</span> EFF_DT      <span class="cm">/* ← input parameter */</span>

<span class="cm">/* Aliasing an unknown identifier — invalid */</span>
<span class="kw">ALIAS</span> SOME_RANDOM_NAME <span class="kw">AS</span> SHORT_NAME      <span class="cm">/* ← unrecognised */</span></div>

<p><strong>Fix:</strong> Confirm the left-hand identifier is a DBI listed in the Database Items picker. Contexts are read with <code>GET_CONTEXT</code>; inputs are declared with <code>INPUTS ARE</code>; unknown identifiers are typos.</p>

<h3>Error 3 — Unknown Variable on the DBI Identifier</h3>

<div class="error-line">Unknown Variable: CMP_ASSIGNMENT_SALARY_AMOUNT</div>

<div class="codeblock"><span class="cm">/* The DBI exists in the dictionary but is not visible to this formula type */</span>
<span class="cm">/* because the formula type doesn't supply HR_ASSIGNMENT_ID as a context.   */</span>
<span class="kw">ALIAS</span> CMP_ASSIGNMENT_SALARY_AMOUNT <span class="kw">AS</span> ASG_SAL</div>

<p><strong>Fix:</strong> Open the Database Items picker for the specific formula type currently being authored — Absence Accrual, OTL Time Entry Rule, Compensation Default and Override, Payroll, whichever applies — and confirm the DBI is listed. If it isn't, your formula type doesn't supply the contexts the DBI's route needs, and aliasing won't fix it.</p>

<hr>


<h2>Production Conventions for ALIAS</h2>

<div class="tblwrap">
<table class="ref single">
<thead><tr><th>Seven principles that pay off across every formula</th></tr></thead>
<tbody>
<tr><td><div class="step-row"><span class="step-num">RULE 1</span><div class="step-body"><strong>Group all ALIAS declarations at the top of the formula</strong>, immediately after the header comment. Satisfies the ordering rule and presents the data dependencies in one block.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">RULE 2</span><div class="step-body"><strong>Apply ALIAS only when the DBI is referenced more than once or longer than ~25 characters.</strong> A single short reference doesn't warrant the declaration overhead.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">RULE 3</span><div class="step-body"><strong>Use a project-wide naming convention.</strong> Strip product prefixes and abbreviate consistently: <code>PER_ASG_REL_LENGTH_OF_SERVICE</code> → <code>ASG_LOS</code>, <code>ASG_HR_ASG_ID</code> → <code>ASG_ID</code>, <code>CMP_ASSIGNMENT_SALARY_AMOUNT</code> → <code>ASG_SAL</code>.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">RULE 4</span><div class="step-body"><strong>Annotate each alias with a one-line trailing comment</strong> describing what the DBI represents in business terms.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">RULE 5</span><div class="step-body"><strong>Default to ALIAS over local-variable assignment</strong> for shortening. Use local assignment only when snapshot semantics are explicitly required, with a name that signals the snapshot intent.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">RULE 6</span><div class="step-body"><strong>Restrict ALIAS targets to database items.</strong> Inputs are short by design. Contexts are accessed through GET_CONTEXT. Local variables are named directly.</div></div></td></tr>
<tr><td><div class="step-row"><span class="step-num">RULE 7</span><div class="step-body"><strong>Apply consistent identifier casing.</strong> The compiler is case-insensitive, but mixing <code>ASG_LOS</code> and <code>Ot_Qls</code> across one formula degrades readability.</div></div></td></tr>
</tbody>
</table>
</div>

<hr>


<h2>Before vs After — The Readability Payoff</h2>

<p>Same logic, written twice. Once without aliases, once with. Watch how the body changes character.</p>

<h3>Without ALIAS</h3>

<div class="codeblock"><span class="cm">/*========================================================================
   FORMULA NAME : XX_OT_ELIG_WITHOUT_ALIAS
   FORMULA TYPE : Element Iterative Calculator
   PURPOSE      : OT eligibility flag & multiplier from qualifying LOS
                  and assignment salary.
========================================================================*/</span>

<span class="kw">DEFAULT FOR</span> PER_ASG_REL_LENGTH_OF_SERVICE <span class="kw">IS</span> <span class="nm">0</span>
<span class="kw">DEFAULT FOR</span> CMP_ASSIGNMENT_SALARY_AMOUNT          <span class="kw">IS</span> <span class="nm">0</span>
<span class="kw">DEFAULT FOR</span> PER_ASG_JOB_NAME                      <span class="kw">IS</span> <span class="st">' '</span>

<span class="kw">INPUTS ARE</span> EFFECTIVE_PERIOD_END (<span class="kw">DATE</span>)

L_FLAG       = <span class="st">'N'</span>
L_MULTIPLIER = <span class="nm">1</span>

<span class="kw">CHANGE_CONTEXTS</span> (EFFECTIVE_DATE = EFFECTIVE_PERIOD_END)
(
   <span class="kw">IF</span> PER_ASG_REL_LENGTH_OF_SERVICE >= <span class="nm">5</span>
      <span class="kw">AND</span> CMP_ASSIGNMENT_SALARY_AMOUNT > <span class="nm">0</span>
      <span class="kw">AND</span> PER_ASG_JOB_NAME <> <span class="st">' '</span>
   <span class="kw">THEN</span>
      ( L_FLAG       = <span class="st">'Y'</span>
        L_MULTIPLIER = <span class="nm">1.5</span> )

   <span class="kw">IF</span> PER_ASG_REL_LENGTH_OF_SERVICE >= <span class="nm">10</span> <span class="kw">THEN</span>
      L_MULTIPLIER = <span class="nm">2.0</span>
)

<span class="kw">RETURN</span> L_FLAG, L_MULTIPLIER</div>

<h3>With ALIAS</h3>

<div class="codeblock"><span class="cm">/*========================================================================
   FORMULA NAME : XX_OT_ELIG_WITH_ALIAS
   FORMULA TYPE : Element Iterative Calculator
   NOTES        : ALIAS block sits FIRST. Each alias is a reference to
                  its underlying DBI; evaluation is lazy and re-fetches
                  under any CHANGE_CONTEXTS block.
========================================================================*/</span>

<span class="kw">ALIAS</span> PER_ASG_REL_LENGTH_OF_SERVICE <span class="kw">AS</span> ASG_LOS    <span class="cm">/* qualifying LOS, years */</span>
<span class="kw">ALIAS</span> CMP_ASSIGNMENT_SALARY_AMOUNT  <span class="kw">AS</span> ASG_SAL    <span class="cm">/* current annual salary */</span>
<span class="kw">ALIAS</span> PER_ASG_JOB_NAME              <span class="kw">AS</span> ASG_JOB    <span class="cm">/* assignment job name   */</span>

<span class="kw">DEFAULT FOR</span> ASG_LOS <span class="kw">IS</span> <span class="nm">0</span>
<span class="kw">DEFAULT FOR</span> ASG_SAL <span class="kw">IS</span> <span class="nm">0</span>
<span class="kw">DEFAULT FOR</span> ASG_JOB <span class="kw">IS</span> <span class="st">' '</span>

<span class="kw">INPUTS ARE</span> EFFECTIVE_PERIOD_END (<span class="kw">DATE</span>)

L_FLAG       = <span class="st">'N'</span>
L_MULTIPLIER = <span class="nm">1</span>

<span class="kw">CHANGE_CONTEXTS</span> (EFFECTIVE_DATE = EFFECTIVE_PERIOD_END)
(
   <span class="kw">IF</span> ASG_LOS >= <span class="nm">5</span> <span class="kw">AND</span> ASG_SAL > <span class="nm">0</span> <span class="kw">AND</span> ASG_JOB <> <span class="st">' '</span> <span class="kw">THEN</span>
      ( L_FLAG       = <span class="st">'Y'</span>
        L_MULTIPLIER = <span class="nm">1.5</span> )

   <span class="kw">IF</span> ASG_LOS >= <span class="nm">10</span> <span class="kw">THEN</span>
      L_MULTIPLIER = <span class="nm">2.0</span>
)

<span class="kw">IF</span> ASG_SAL <span class="kw">WAS DEFAULTED</span> <span class="kw">THEN</span>
   L_MSG = <span class="st">'Salary DBI returned NULL — defaulted to 0'</span>

<span class="kw">RETURN</span> L_FLAG, L_MULTIPLIER</div>

<p>Compare the eligibility test in the aliased version to the unaliased one. Same logical condition, but in the aliased version you can read the rule out loud: "if qualifying service is at least 5 and salary is positive and job is not blank" — without your eyes filtering through DBI prefixes. That readability is the entire point.</p>

<p>The aliased version also adds the <code>WAS DEFAULTED</code> diagnostic on the salary check, which is unavailable through local-variable assignment.</p>

<hr>


<h2>Key Takeaways</h2>

<p><strong>ALIAS is a compile-time reference, not a runtime variable.</strong> The alias and the underlying DBI share a single metadata handle. No separate runtime allocation occurs.</p>

<p><strong>Statement ordering is enforced.</strong> The required sequence is ALIAS → DEFAULT → INPUTS → body → RETURN. Violations produce <em>"Incorrect Statement Order."</em></p>

<p><strong>ALIAS interacts correctly with WAS DEFAULTED and CHANGE_CONTEXTS.</strong> Local-variable assignment from a DBI does not — that produces a snapshot, not a reference, and silently breaks salary deltas, before/after comparisons, and any logic that re-evaluates a value under a different context.</p>

<p><strong>ALIAS targets are restricted to database items in current Fusion releases.</strong> Inputs, contexts, functions, and global values are not valid targets.</p>


<table class="byline">
<tr>
  <td class="avatar">AM</td>
  <td class="name"><strong>Abhishek Mohanty</strong><span>Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.</span></td>
</tr>
</table>


<div class="tags">
<a href="#">Fast Formula</a>
<a href="#">ALIAS</a>
<a href="#">Oracle HCM Cloud</a>
<a href="#">DBI</a>
<a href="#">CHANGE_CONTEXTS</a>
<a href="#">WAS_DEFAULTED</a>
<a href="#">Statement Order</a>
<a href="#">Compilation Errors</a>
<a href="#">Oracle Cloud</a>
</div>

</article>

</body>
</html>