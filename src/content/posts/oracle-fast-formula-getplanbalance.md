---
title: "Oracle Fast Formula: GET_PLAN_BALANCE, GET_ABSENCE_COUNTS, and the Two Traps That Quietly Ship the Wrong Number"
description: "am-post  font-family: Open Sans, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif; color: #1c1c1a; line-height: 1"
pubDate: 2026-04-28
tags: ["Fast Formula", "Oracle HCM Cloud", "Absence Management"]
---

<p> </p>



<div class="am-post">

<div class="am-meta">
<a href="https://abhishekmohanty-hcm.blogspot.com/2026/04/" style="color:#c0392b;text-decoration:none;font-weight:600;">April 28, 2026</a>
</div>

<div class="am-tags">
<span class="am-tag">Fast Formula</span>
<span class="am-tag">Absence Management</span>
<span class="am-tag">GET_PLAN_BALANCE</span>
<span class="am-tag">DBI</span>
</div>

<h1>Oracle Fast Formula: Reading Absence Balance — Four Mechanisms, the Naming Traps, and a Recipe That Actually Works</h1>

<div class="am-meta">
<strong>Abhishek Mohanty</strong> · April 2026 · 14 min read · Oracle HCM Cloud
</div>

<p>If you have ever written an absence Fast Formula, deployed it, watched it compile cleanly, and then opened the timecard or the absence record only to find a wrong balance — this post is for you.</p>

<p>Reading absence balance fails for two reasons. Either the function you picked reads from the wrong place — the saved snapshot when you needed live, or vice versa. Or the filter you wrote does nothing because of a status-column naming asymmetry that is easy to miss. Most blogs jump straight to the function call. But if the mechanism does not match the use case, no amount of tweaking inside it will produce the right number.</p>

<p>This post walks through all four mechanisms in order: what each one queries under the hood, when it works, when it silently fails, and the production-ready composite recipe that combines two of them into a balance reader you can defend in audit.</p>

<div class="am-fig">
<p class="am-fig-title">FORMULA CONTEXT · THE QUESTION</p>
<div style="text-align:center;">
<svg viewBox="0 0 880 360" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Open Sans', system-ui, sans-serif;">
  <defs>
    <marker id="arrowSlim" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#5a5856" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <marker id="arrowAccent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#c0392b" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>

  
  <rect x="0" y="0" width="880" height="360" fill="#fafafa"/>

  
  <text x="40" y="30" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1.5">FORMULA CONTEXT</text>

  
  <g filter="url(#cardShadow)">
    <rect x="40" y="50" width="190" height="38" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="40" y="50" width="3" height="38" fill="#4a5d8f"/>
    <text x="55" y="74" font-size="13" fill="#2d2926" font-weight="500">Plan Use Rate FF</text>
  </g>
  <g filter="url(#cardShadow)">
    <rect x="40" y="98" width="190" height="38" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="40" y="98" width="3" height="38" fill="#4a5d8f"/>
    <text x="55" y="122" font-size="13" fill="#2d2926" font-weight="500">Entry Validation FF</text>
  </g>
  <g filter="url(#cardShadow)">
    <rect x="40" y="146" width="190" height="38" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="40" y="146" width="3" height="38" fill="#4a5d8f"/>
    <text x="55" y="170" font-size="13" fill="#2d2926" font-weight="500">Type Duration FF</text>
  </g>
  <g filter="url(#cardShadow)">
    <rect x="40" y="194" width="190" height="38" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="40" y="194" width="3" height="38" fill="#4a5d8f"/>
    <text x="55" y="218" font-size="13" fill="#2d2926" font-weight="500">Carryover FF</text>
  </g>
  <g filter="url(#cardShadow)">
    <rect x="40" y="242" width="190" height="38" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="40" y="242" width="3" height="38" fill="#4a5d8f"/>
    <text x="55" y="266" font-size="13" fill="#2d2926" font-weight="500">Custom Accrual FF</text>
  </g>

  
  <path d="M 230 69 L 250 69 L 250 261 L 230 261" stroke="#b8b4ae" stroke-width="1" fill="none"/>
  <line x1="250" y1="165" x2="285" y2="165" stroke="#5a5856" stroke-width="1.3" marker-end="url(#arrowSlim)"/>

  
  <g filter="url(#cardShadow)">
    <rect x="290" y="100" width="300" height="130" rx="6" fill="#ffffff" stroke="#c0392b" stroke-width="1.2"/>
    <text x="440" y="130" text-anchor="middle" font-size="11" fill="#7a2418" font-weight="700" letter-spacing="1.2">THE RECURRING QUESTION</text>
    <text x="440" y="160" text-anchor="middle" font-size="15" fill="#1c1c1a" font-weight="600">What is this person's</text>
    <text x="440" y="183" text-anchor="middle" font-size="15" fill="#1c1c1a" font-weight="600">accrual balance right now?</text>
    <line x1="320" y1="200" x2="560" y2="200" stroke="#ede4e0" stroke-width="1"/>
    <text x="440" y="219" text-anchor="middle" font-size="12" fill="#6b6b6b" font-style="italic">...and how much have they already consumed?</text>
  </g>

  
  <text x="610" y="30" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1.5">AVAILABLE MECHANISMS</text>

  <line x1="590" y1="165" x2="625" y2="100" stroke="#b8b4ae" stroke-width="1" fill="none"/>
  <line x1="590" y1="165" x2="625" y2="148" stroke="#b8b4ae" stroke-width="1" fill="none"/>
  <line x1="590" y1="165" x2="625" y2="196" stroke="#b8b4ae" stroke-width="1" fill="none"/>
  <line x1="590" y1="165" x2="625" y2="244" stroke="#c0392b" stroke-width="1.4" fill="none" marker-end="url(#arrowAccent)"/>

  <g>
    <rect x="630" y="80" width="210" height="40" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <text x="645" y="98" font-size="11" fill="#8e8b87" letter-spacing="0.8">MECHANISM 1</text>
    <text x="645" y="113" font-size="12.5" fill="#2d2926" font-weight="600" font-family="'Fira Code', monospace">GET_PLAN_BALANCE</text>
  </g>
  <g>
    <rect x="630" y="128" width="210" height="40" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <text x="645" y="146" font-size="11" fill="#8e8b87" letter-spacing="0.8">MECHANISM 2</text>
    <text x="645" y="161" font-size="12.5" fill="#2d2926" font-weight="600" font-family="'Fira Code', monospace">GET_ABSENCE_COUNTS</text>
  </g>
  <g>
    <rect x="630" y="176" width="210" height="40" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <text x="645" y="194" font-size="11" fill="#8e8b87" letter-spacing="0.8">MECHANISM 3</text>
    <text x="645" y="209" font-size="12" fill="#2d2926" font-weight="600" font-family="'Fira Code', monospace">GET_ABSENCE_DAYS_PER_TYPE</text>
  </g>
  <g>
    <rect x="630" y="224" width="210" height="40" rx="4" fill="#ecf6f1" stroke="#0d7377" stroke-width="1.2"/>
    <text x="645" y="242" font-size="11" fill="#0a5a5d" letter-spacing="0.8" font-weight="700">MECHANISM 4 · RECOMMENDED</text>
    <text x="645" y="257" font-size="12" fill="#0a5a5d" font-weight="600">DBI driver array + scalars</text>
  </g>

  
  <line x1="40" y1="310" x2="840" y2="310" stroke="#ede4e0" stroke-width="1"/>
  <text x="40" y="335" font-size="12" fill="#6b6b6b" font-weight="600">Pick wrong</text>
  <text x="120" y="335" font-size="12" fill="#6b6b6b">→ no compile error · no warning · the formula returns a number, just not the right one.</text>
</svg>
</div>
<p class="am-fig-caption"><strong>Fig 1 —</strong> Five formula contexts converge on the same sub-question. Four mechanisms can answer it, but the silent failure mode — wrong number, no compile error — is what makes the choice load-bearing.</p>
</div>

<hr>

<h2>The Four Mechanisms — Side by Side</h2>

<p>Before we go deep on each one, here is the quick reference table. Keep it open when you are halfway through writing a formula and trying to remember which function fits the use case.</p>

<table>
<thead><tr><th>Mechanism</th><th>Reads From</th><th>Sees In-Progress</th><th>Filter Visible</th><th>Best For</th></tr></thead>
<tbody>
<tr><td><code>GET_PLAN_BALANCE</code></td><td>Saved balance</td><td><span class="am-pill am-pill-red">No</span></td><td><span class="am-pill am-pill-yellow">N/A</span></td><td>Carryover, period-end reports, snapshot anchor</td></tr>
<tr><td><code>GET_ABSENCE_COUNTS</code></td><td>Live entries</td><td><span class="am-pill am-pill-green">Yes</span></td><td><span class="am-pill am-pill-red">No</span></td><td>"Applied for" occurrence rules</td></tr>
<tr><td><code>GET_ABSENCE_DAYS_PER_TYPE</code></td><td>Live entries</td><td><span class="am-pill am-pill-green">Yes</span></td><td><span class="am-pill am-pill-red">Hidden</span></td><td>Indicative reports only</td></tr>
<tr><td>Read each entry yourself <em>(recommended)</em></td><td>Live entries</td><td><span class="am-pill am-pill-green">Yes</span></td><td><span class="am-pill am-pill-green">Yes</span></td><td>Real-time decisions, audit-grade rules</td></tr>
</tbody>
</table>

<div class="am-fig">
<p class="am-fig-title">CAPABILITY MATRIX</p>
<div style="text-align:center;">
<svg viewBox="0 0 900 360" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Open Sans', system-ui, sans-serif;">
  <defs>
    <filter id="matrixShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="900" height="360" fill="#fafafa"/>

  
  <g filter="url(#matrixShadow)">
    <rect x="30" y="20" width="240" height="60" rx="4" fill="#faf6f3" stroke="#ede4e0" stroke-width="0.8"/>
  </g>
  <text x="50" y="48" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1">CAPABILITY</text>
  <text x="50" y="68" font-size="12" fill="#6b6b6b">Compare across mechanisms</text>

  <g filter="url(#matrixShadow)">
    <rect x="278" y="20" width="148" height="60" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
  </g>
  <text x="352" y="42" text-anchor="middle" font-size="10" fill="#8e8b87" letter-spacing="0.8">MECHANISM 1</text>
  <text x="352" y="60" text-anchor="middle" font-size="11.5" fill="#1c1c1a" font-weight="700" font-family="'Fira Code', monospace">GET_PLAN_BALANCE</text>
  <rect x="278" y="74" width="148" height="3" fill="#4a5d8f"/>

  <g filter="url(#matrixShadow)">
    <rect x="434" y="20" width="148" height="60" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
  </g>
  <text x="508" y="42" text-anchor="middle" font-size="10" fill="#8e8b87" letter-spacing="0.8">MECHANISM 2</text>
  <text x="508" y="60" text-anchor="middle" font-size="11" fill="#1c1c1a" font-weight="700" font-family="'Fira Code', monospace">GET_ABSENCE_COUNTS</text>
  <rect x="434" y="74" width="148" height="3" fill="#b8860b"/>

  <g filter="url(#matrixShadow)">
    <rect x="590" y="20" width="148" height="60" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
  </g>
  <text x="664" y="42" text-anchor="middle" font-size="10" fill="#8e8b87" letter-spacing="0.8">MECHANISM 3</text>
  <text x="664" y="58" text-anchor="middle" font-size="10" fill="#1c1c1a" font-weight="700" font-family="'Fira Code', monospace">GET_ABSENCE_DAYS</text>
  <text x="664" y="70" text-anchor="middle" font-size="10" fill="#1c1c1a" font-weight="700" font-family="'Fira Code', monospace">_PER_TYPE</text>
  <rect x="590" y="74" width="148" height="3" fill="#c0392b"/>

  <g filter="url(#matrixShadow)">
    <rect x="746" y="20" width="124" height="60" rx="4" fill="#ecf6f1" stroke="#0d7377" stroke-width="1.4"/>
  </g>
  <text x="808" y="42" text-anchor="middle" font-size="10" fill="#0a5a5d" letter-spacing="0.8" font-weight="700">RECOMMENDED</text>
  <text x="808" y="60" text-anchor="middle" font-size="11" fill="#0a5a5d" font-weight="700">Driver + Scalars</text>

  
  <g font-size="13" fill="#2d2926">
    <text x="50" y="115" font-weight="500">Source table</text>
    <text x="50" y="155" font-weight="500">Sees in-flight entries</text>
    <text x="50" y="195" font-weight="500">Status filter visible</text>
    <text x="50" y="235" font-weight="500">Status filter overridable</text>
    <text x="50" y="275" font-weight="500">Audit-defensible</text>
    <text x="50" y="315" font-weight="500">Suitable for live decisions</text>
  </g>

  
  <line x1="30" y1="125" x2="870" y2="125" stroke="#ede4e0" stroke-width="0.6"/>
  <line x1="30" y1="165" x2="870" y2="165" stroke="#ede4e0" stroke-width="0.6"/>
  <line x1="30" y1="205" x2="870" y2="205" stroke="#ede4e0" stroke-width="0.6"/>
  <line x1="30" y1="245" x2="870" y2="245" stroke="#ede4e0" stroke-width="0.6"/>
  <line x1="30" y1="285" x2="870" y2="285" stroke="#ede4e0" stroke-width="0.6"/>

  
  <text x="352" y="112" text-anchor="middle" font-size="10.5" fill="#4a5d8f" font-family="'Fira Code', monospace">ACRL_ENTRY_DTLS</text>
  <text x="352" y="152" text-anchor="middle" font-size="13" fill="#c0392b" font-weight="700">No</text>
  <text x="352" y="192" text-anchor="middle" font-size="13" fill="#0d7377" font-weight="700">N/A</text>
  <text x="352" y="232" text-anchor="middle" font-size="13" fill="#0d7377" font-weight="700">N/A</text>
  <text x="352" y="272" text-anchor="middle" font-size="13" fill="#0d7377" font-weight="700">Yes (snapshot)</text>
  <text x="352" y="312" text-anchor="middle" font-size="13" fill="#c0392b" font-weight="700">No</text>

  
  <text x="508" y="112" text-anchor="middle" font-size="10.5" fill="#0d7377" font-family="'Fira Code', monospace">ABS_ENTRIES</text>
  <text x="508" y="152" text-anchor="middle" font-size="13" fill="#0d7377" font-weight="700">Yes</text>
  <text x="508" y="192" text-anchor="middle" font-size="13" fill="#c0392b" font-weight="700">No</text>
  <text x="508" y="232" text-anchor="middle" font-size="13" fill="#c0392b" font-weight="700">No</text>
  <text x="508" y="272" text-anchor="middle" font-size="13" fill="#b8860b" font-weight="700">Partial</text>
  <text x="508" y="312" text-anchor="middle" font-size="13" fill="#b8860b" font-weight="700">Occurrence rules</text>

  
  <text x="664" y="112" text-anchor="middle" font-size="10.5" fill="#0d7377" font-family="'Fira Code', monospace">ABS_ENTRIES</text>
  <text x="664" y="152" text-anchor="middle" font-size="13" fill="#0d7377" font-weight="700">Yes</text>
  <text x="664" y="192" text-anchor="middle" font-size="13" fill="#c0392b" font-weight="700">No (opaque)</text>
  <text x="664" y="232" text-anchor="middle" font-size="13" fill="#c0392b" font-weight="700">No</text>
  <text x="664" y="272" text-anchor="middle" font-size="13" fill="#c0392b" font-weight="700">No</text>
  <text x="664" y="312" text-anchor="middle" font-size="13" fill="#c0392b" font-weight="700">No</text>

  
  <rect x="746" y="93" width="124" height="240" fill="#ecf6f1" opacity="0.4"/>
  <text x="808" y="112" text-anchor="middle" font-size="10.5" fill="#0d7377" font-family="'Fira Code', monospace">ABS_ENTRIES</text>
  <text x="808" y="152" text-anchor="middle" font-size="13" fill="#0d7377" font-weight="700">Yes</text>
  <text x="808" y="192" text-anchor="middle" font-size="13" fill="#0d7377" font-weight="700">Yes (in code)</text>
  <text x="808" y="232" text-anchor="middle" font-size="13" fill="#0d7377" font-weight="700">Yes</text>
  <text x="808" y="272" text-anchor="middle" font-size="13" fill="#0d7377" font-weight="700">Yes</text>
  <text x="808" y="312" text-anchor="middle" font-size="13" fill="#0d7377" font-weight="700">Yes</text>
</svg>
</div>
<p class="am-fig-caption"><strong>Fig 2 —</strong> Capability matrix across all four mechanisms. Mechanism 4 is the only path that earns a "yes" on every dimension — at the cost of around fifty lines of structural setup that the other three avoid.</p>
</div>

<div class="am-call note">
<span class="am-call-tag">📌 Why this is harder than it should be</span>
The four functions all return a number related to absence consumption. They all compile. The differences only show up in specific lifecycle states — in-progress requests, withdrawn entries, post-batch lag — which UAT often does not exercise systematically. The bug ships and surfaces three months later when an auditor asks why the numbers do not reconcile.
</div>

<hr>

<h2>Mechanism 1 — <code>GET_PLAN_BALANCE</code> (the saved snapshot)</h2>

<p>The default reach for anyone who has read the Oracle documentation. Returns a clean numeric balance, well-named, and works perfectly in unit tests. It is also the most frequent root cause of broken Entry Validation rules in production.</p>

<p class="am-where"><strong>Where the data comes from:</strong> <em>ANC_PER_ACRL_ENTRY_DTLS — the committed accrual ledger, refreshed only when the absence accrual engine runs (typically nightly batch).</em></p>

<h3>Scenario from the UI</h3>

<p>Open <strong>Me > Time and Absences > Absence Balance</strong>. The plan balance shown there comes from the latest accrual run — signed off and stable. But if a leave was submitted this morning, you will not see its impact here until the next batch runs. <code>GET_PLAN_BALANCE</code> reads from the exact same place.</p>

<div class="am-fig">
<p class="am-fig-title">SEQUENCE DIAGRAM · A DAY IN THE LIFE OF A BALANCE</p>
<div style="text-align:center;">
<svg viewBox="0 0 900 460" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Open Sans', system-ui, sans-serif;">
  <defs>
    <filter id="seqShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.08"/>
    </filter>
    <pattern id="staleHatch" x="0" y="0" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="#c0392b" stroke-width="0.8" opacity="0.25"/>
    </pattern>
    <marker id="seqArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#5a5856" stroke-width="1.4" stroke-linecap="round"/>
    </marker>
    <marker id="seqArrowRed" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#c0392b" stroke-width="1.4" stroke-linecap="round"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="900" height="460" fill="#fafafa"/>

  <text x="40" y="28" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1.5">SEQUENCE DIAGRAM</text>
  <text x="40" y="46" font-size="14" fill="#1c1c1a" font-weight="600">A day in the life of an Annual Leave balance</text>

  
  <g font-size="11.5" fill="#2d2926" font-weight="600">
    <text x="155" y="90" text-anchor="end">Employee</text>
    <text x="155" y="148" text-anchor="end">UI / Self-Service</text>
    <text x="155" y="206" text-anchor="end">ANC_PER_ABS_ENTRIES</text>
    <text x="155" y="220" text-anchor="end" font-size="10" fill="#8e8b87" font-weight="400">(live)</text>
    <text x="155" y="270" text-anchor="end">Accrual Engine</text>
    <text x="155" y="284" text-anchor="end" font-size="10" fill="#8e8b87" font-weight="400">(batch)</text>
    <text x="155" y="332" text-anchor="end">ANC_PER_ACRL_ENTRY_DTLS</text>
    <text x="155" y="346" text-anchor="end" font-size="10" fill="#8e8b87" font-weight="400">(snapshot ledger)</text>
    <text x="155" y="394" text-anchor="end">GET_PLAN_BALANCE</text>
    <text x="155" y="408" text-anchor="end" font-size="10" fill="#8e8b87" font-weight="400">(your formula)</text>
  </g>

  
  <g stroke="#ede4e0" stroke-width="0.6" stroke-dasharray="2 3">
    <line x1="170" y1="85" x2="870" y2="85"/>
    <line x1="170" y1="143" x2="870" y2="143"/>
    <line x1="170" y1="201" x2="870" y2="201"/>
    <line x1="170" y1="265" x2="870" y2="265"/>
    <line x1="170" y1="327" x2="870" y2="327"/>
    <line x1="170" y1="389" x2="870" y2="389"/>
  </g>

  
  <line x1="170" y1="425" x2="870" y2="425" stroke="#5a5856" stroke-width="1"/>

  
  <g font-size="11" fill="#5a5856">
    <line x1="240" y1="421" x2="240" y2="429" stroke="#5a5856"/>
    <text x="240" y="445" text-anchor="middle" font-weight="500">Last night 02:00</text>
    <text x="240" y="458" text-anchor="middle" font-size="10" fill="#8e8b87">batch ran</text>

    <line x1="430" y1="421" x2="430" y2="429" stroke="#5a5856"/>
    <text x="430" y="445" text-anchor="middle" font-weight="500">Today 14:00</text>
    <text x="430" y="458" text-anchor="middle" font-size="10" fill="#8e8b87">leave submitted</text>

    <line x1="600" y1="421" x2="600" y2="429" stroke="#c0392b"/>
    <text x="600" y="445" text-anchor="middle" font-weight="700" fill="#c0392b">Today 15:00</text>
    <text x="600" y="458" text-anchor="middle" font-size="10" fill="#c0392b">formula runs</text>

    <line x1="800" y1="421" x2="800" y2="429" stroke="#5a5856"/>
    <text x="800" y="445" text-anchor="middle" font-weight="500">Tonight 02:00</text>
    <text x="800" y="458" text-anchor="middle" font-size="10" fill="#8e8b87">next batch</text>
  </g>

  
  <rect x="430" y="60" width="370" height="345" fill="url(#staleHatch)"/>
  <text x="615" y="75" text-anchor="middle" font-size="10" fill="#c0392b" font-weight="600" letter-spacing="0.8">STALE DATA WINDOW</text>

  
  <g filter="url(#seqShadow)">
    <rect x="195" y="316" width="90" height="22" rx="3" fill="#ffffff" stroke="#4a5d8f" stroke-width="0.8"/>
    <text x="240" y="331" text-anchor="middle" font-size="11" fill="#2f3e63" font-weight="600">Balance: 5.0</text>
  </g>
  <line x1="240" y1="338" x2="240" y2="385" stroke="#4a5d8f" stroke-width="1" stroke-dasharray="3 3"/>

  
  <circle cx="430" cy="85" r="5" fill="#1c1c1a"/>
  <line x1="430" y1="90" x2="430" y2="138" stroke="#5a5856" stroke-width="1.2" marker-end="url(#seqArrow)"/>
  <text x="442" y="115" font-size="10.5" fill="#5a5856">submits 3-day AL</text>

  
  <line x1="430" y1="148" x2="430" y2="196" stroke="#5a5856" stroke-width="1.2" marker-end="url(#seqArrow)"/>
  <text x="442" y="175" font-size="10.5" fill="#5a5856">INSERT entry (Submitted)</text>

  <g filter="url(#seqShadow)">
    <rect x="395" y="195" width="100" height="22" rx="3" fill="#ffffff" stroke="#0d7377" stroke-width="0.8"/>
    <text x="445" y="210" text-anchor="middle" font-size="11" fill="#0a5a5d" font-weight="600">+1 row written</text>
  </g>

  
  <g>
    <path d="M 445 217 Q 445 270 470 270 L 590 270" stroke="#c0392b" stroke-width="1" fill="none" stroke-dasharray="4 3"/>
    <text x="500" y="252" font-size="10" fill="#c0392b" font-weight="600">no engine run</text>
    <text x="500" y="263" font-size="10" fill="#c0392b" font-style="italic">→ ledger unchanged</text>
  </g>

  
  <line x1="600" y1="389" x2="600" y2="345" stroke="#c0392b" stroke-width="1.4" marker-end="url(#seqArrowRed)"/>
  <text x="612" y="372" font-size="10.5" fill="#c0392b" font-weight="600">read ledger</text>

  <g filter="url(#seqShadow)">
    <rect x="555" y="316" width="90" height="22" rx="3" fill="#fdf2f0" stroke="#c0392b" stroke-width="0.8"/>
    <text x="600" y="331" text-anchor="middle" font-size="11" fill="#7a2418" font-weight="700">Returns 5.0</text>
  </g>

  
  <g filter="url(#seqShadow)">
    <rect x="555" y="195" width="90" height="22" rx="3" fill="#fdf6e3" stroke="#b8860b" stroke-width="0.8"/>
    <text x="600" y="210" text-anchor="middle" font-size="11" fill="#7a5800" font-weight="700">Live: 2.0</text>
  </g>

  
  <g>
    <line x1="649" y1="206" x2="685" y2="206" stroke="#c0392b" stroke-width="0.8" stroke-dasharray="2 2"/>
    <line x1="649" y1="327" x2="685" y2="327" stroke="#c0392b" stroke-width="0.8" stroke-dasharray="2 2"/>
    <line x1="685" y1="206" x2="685" y2="327" stroke="#c0392b" stroke-width="0.8"/>
    <line x1="685" y1="266" x2="710" y2="266" stroke="#c0392b" stroke-width="0.8"/>
    <text x="715" y="262" font-size="11" fill="#7a2418" font-weight="700">Δ = 3.0 days</text>
    <text x="715" y="276" font-size="10" fill="#7a2418" font-style="italic">silent gap</text>
  </g>

  
  <line x1="800" y1="265" x2="800" y2="320" stroke="#5a5856" stroke-width="1.2" marker-end="url(#seqArrow)"/>
  <g filter="url(#seqShadow)">
    <rect x="770" y="259" width="60" height="14" rx="2" fill="#ffffff" stroke="#4a5d8f" stroke-width="0.6"/>
    <text x="800" y="269" text-anchor="middle" font-size="9.5" fill="#2f3e63">batch run</text>
  </g>
  <g filter="url(#seqShadow)">
    <rect x="755" y="316" width="90" height="22" rx="3" fill="#ffffff" stroke="#4a5d8f" stroke-width="0.8"/>
    <text x="800" y="331" text-anchor="middle" font-size="11" fill="#2f3e63" font-weight="600">Balance: 2.0</text>
  </g>

</svg>
</div>
<p class="am-fig-caption"><strong>Fig 3 —</strong> Sequence diagram of the lag mechanism. The 14:00 absence submission writes to the live table immediately, but the snapshot ledger is not updated until the next batch run at 02:00. Any formula calling <code>GET_PLAN_BALANCE</code> in the intervening 12-hour window reads stale data, and the absence engine provides no callback to invalidate it.</p>
</div>

<h3>The signature most authors get wrong</h3>

<p>The function takes <strong>one explicit argument</strong> — the plan name. Person, assignment, plan ID, effective date, and LDG must already be in scope as <strong>contexts</strong>. The PL/SQL-style three-argument call is a common carry-over from data-warehouse SQL habits, and it is wrong.</p>

<pre><code>/* Correct call */
g_balance = GET_PLAN_BALANCE('Annual Leave Plan')

/* These must be in scope as contexts — you do NOT pass them as arguments:
   PERSON_ID
   HR_ASSIGNMENT_ID
   EFFECTIVE_DATE
   ACCRUAL_PLAN_ID
   LEGISLATIVE_DATA_GROUP_ID                                              */</code></pre>

<div class="am-call success">
<span class="am-call-tag">✅ Use it for</span>
Carryover formulas (where you want the snapshot — that is precisely the point), period-end reporting, accrual statements, and as the "starting balance" inside the composite recipe later in this post. Do <strong>not</strong> use it stand-alone for any decision that must reflect the current moment.
</div>

<hr>

<h2>Mechanism 2 — <code>GET_ABSENCE_COUNTS</code> (counts everything, even withdrawn)</h2>

<p>Reads the live absence collection. Counts entries in a date range and returns six duration totals via OUT parameters. Useful, with one well-known catch: it applies <strong>no status filter at all</strong>. Withdrawn entries count. Denied entries count. Approved entries count. They are all the same to this function.</p>

<p class="am-where"><strong>Where the data comes from:</strong> <em>ANC_PER_ABS_ENTRIES — the live absence collection, updated transactionally on every Submit, Approve, or Withdraw.</em></p>

<h3>Scenario from the UI</h3>

<p>Switch to <strong>Me > Time and Absences > Existing Absences</strong>. It lists every absence the employee ever recorded — submitted, approved, withdrawn, denied, all of them. If you simply count the rows, you get a true count of entries, but not a count of leave actually consumed. <code>GET_ABSENCE_COUNTS</code> works the same way.</p>

<div class="am-fig">
<p class="am-fig-title">DATA VIEW · GET_ABSENCE_COUNTS</p>
<div style="text-align:center;">
<svg viewBox="0 0 900 380" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Open Sans', system-ui, sans-serif;">
  <defs>
    <filter id="rowShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="1" stdDeviation="2" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="900" height="380" fill="#fafafa"/>

  <text x="40" y="28" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1.5">DATA VIEW</text>
  <text x="40" y="46" font-size="14" fill="#1c1c1a" font-weight="600">An employee's three Annual Leave entries this quarter</text>

  
  <g filter="url(#rowShadow)">
    <rect x="40" y="68" width="500" height="32" fill="#1f1d1c" rx="4 4 0 0"/>
    <text x="60" y="88" font-size="11" fill="#f0ebe6" font-weight="600" letter-spacing="0.6">ENTRY_ID</text>
    <text x="160" y="88" font-size="11" fill="#f0ebe6" font-weight="600" letter-spacing="0.6">DATES</text>
    <text x="280" y="88" font-size="11" fill="#f0ebe6" font-weight="600" letter-spacing="0.6">DURATION</text>
    <text x="370" y="88" font-size="11" fill="#f0ebe6" font-weight="600" letter-spacing="0.6">STATUS</text>
  </g>

  
  <g filter="url(#rowShadow)">
    <rect x="40" y="100" width="500" height="44" fill="#ffffff" stroke="#ede4e0" stroke-width="0.6"/>
    <text x="60" y="127" font-size="12" fill="#2d2926" font-family="'Fira Code', monospace">300012345</text>
    <text x="160" y="127" font-size="12" fill="#2d2926">15-Jan → 19-Jan</text>
    <text x="290" y="127" font-size="12" fill="#2d2926" font-weight="600">5 days</text>
    <rect x="368" y="113" width="84" height="20" rx="10" fill="#ecf6f1" stroke="#0d7377" stroke-width="0.6"/>
    <text x="410" y="127" text-anchor="middle" font-size="10.5" fill="#0a5a5d" font-weight="700">APPROVED</text>
  </g>

  
  <g filter="url(#rowShadow)">
    <rect x="40" y="144" width="500" height="44" fill="#ffffff" stroke="#ede4e0" stroke-width="0.6"/>
    <text x="60" y="171" font-size="12" fill="#2d2926" font-family="'Fira Code', monospace">300012451</text>
    <text x="160" y="171" font-size="12" fill="#2d2926">22-Mar → 22-Mar</text>
    <text x="290" y="171" font-size="12" fill="#2d2926" font-weight="600">1 day</text>
    <rect x="368" y="157" width="84" height="20" rx="10" fill="#fdf6e3" stroke="#b8860b" stroke-width="0.6"/>
    <text x="410" y="171" text-anchor="middle" font-size="10.5" fill="#7a5800" font-weight="700">SUBMITTED</text>
  </g>

  
  <g filter="url(#rowShadow)">
    <rect x="40" y="188" width="500" height="44" fill="#fdf2f0" stroke="#c0392b" stroke-width="0.6"/>
    <text x="60" y="215" font-size="12" fill="#2d2926" font-family="'Fira Code', monospace">300012612</text>
    <text x="160" y="215" font-size="12" fill="#2d2926">02-Mar → 03-Mar</text>
    <text x="290" y="215" font-size="12" fill="#2d2926" font-weight="600">2 days</text>
    <rect x="368" y="201" width="84" height="20" rx="10" fill="#fdf2f0" stroke="#c0392b" stroke-width="0.8"/>
    <text x="410" y="215" text-anchor="middle" font-size="10.5" fill="#7a2418" font-weight="700">WITHDRAWN</text>
  </g>

  
  <line x1="455" y1="210" x2="490" y2="210" stroke="#c0392b" stroke-width="1" stroke-dasharray="3 2"/>
  <text x="495" y="207" font-size="10.5" fill="#7a2418" font-weight="600">should be excluded</text>
  <text x="495" y="220" font-size="10.5" fill="#7a2418" font-style="italic">in most rules</text>

  
  <g filter="url(#rowShadow)">
    <rect x="600" y="100" width="270" height="180" rx="6" fill="#1f1d1c"/>
    <text x="615" y="125" font-size="10" fill="#8e8b87" letter-spacing="0.8">FORMULA CALL</text>
    <text x="615" y="148" font-size="11.5" fill="#f0ebe6" font-family="'Fira Code', monospace">GET_ABSENCE_COUNTS(</text>
    <text x="630" y="166" font-size="11.5" fill="#f0ebe6" font-family="'Fira Code', monospace">person_id,</text>
    <text x="630" y="184" font-size="11.5" fill="#f0ebe6" font-family="'Fira Code', monospace">'AL', '',</text>
    <text x="630" y="202" font-size="11.5" fill="#f0ebe6" font-family="'Fira Code', monospace">'01-Jan', '31-Mar',</text>
    <text x="630" y="220" font-size="11.5" fill="#f0ebe6" font-family="'Fira Code', monospace">l_count, l_days, ...</text>
    <text x="615" y="238" font-size="11.5" fill="#f0ebe6" font-family="'Fira Code', monospace">)</text>
    <line x1="615" y1="248" x2="855" y2="248" stroke="#3a3836" stroke-width="0.6"/>
    <text x="615" y="268" font-size="11" fill="#fdf2f0" font-family="'Fira Code', monospace">l_count = 3 ← all rows</text>
  </g>

  
  <g filter="url(#rowShadow)">
    <rect x="40" y="306" width="830" height="50" rx="6" fill="#fdf2f0" stroke="#c0392b" stroke-width="0.8"/>
    <text x="60" y="328" font-size="11" fill="#7a2418" font-weight="700" letter-spacing="0.6">DOCUMENTED LIMITATION · MOS Doc ID 2899647.1</text>
    <text x="60" y="346" font-size="12.5" fill="#5e1d12">"Need To Exclude Denied And Withdrawn Absences From GET_ABSENCE_COUNTS Results" — the function provides no parameter to filter on lifecycle state.</text>
  </g>
</svg>
</div>
<p class="am-fig-caption"><strong>Fig 4 —</strong> Three live entries on <code>ANC_PER_ABS_ENTRIES</code>; <code>GET_ABSENCE_COUNTS</code> returns 3 regardless of how many should logically count. The withdrawn entry inflates every consumption-derived metric you build on top of this number.</p>
</div>

<div class="am-call warn">
<span class="am-call-tag">⚠️ Documented limitation — MOS Doc ID 2899647.1</span>
<em>"Need To Exclude Denied And Withdrawn Absences From GET_ABSENCE_COUNTS Results"</em> — Oracle has confirmed this. There is no setting to filter; you have to live with what it returns or switch to Mechanism 4.
</div>

<div class="am-call note">
<span class="am-call-tag">📌 Hidden capability most authors miss</span>
Despite the name, the function returns <em>seven</em> values via OUT parameters — occurrence count plus six duration totals (days, hours, calendar days, weeks, months, years). If you only read the count, you are throwing away half its value.
</div>

<div class="am-call success">
<span class="am-call-tag">✅ Use it for</span>
"Applied for" rules — e.g. <em>"no more than 5 sick leave applications per quarter, regardless of approval"</em>. Do <strong>not</strong> use it for consumption arithmetic where withdrawn or denied entries must be excluded.
</div>

<hr>

<h2>Mechanism 3 — <code>GET_ABSENCE_DAYS_PER_TYPE</code> (the opaque sum)</h2>

<p>Looks like the obvious answer. Returns days consumed for a given type, in a given window, for a given person. Three arguments, one numeric output, no setup required. The catch is what happens between input and output.</p>

<h3>Scenario from the UI</h3>

<p>Run the seeded <strong>Absence Records OTBI report</strong> for the same employee. The "Absence Days" column shows a number, but the report has hidden filters baked into the subject area — you cannot see which entries got included. After the next quarterly upgrade, the same employee might show a different total. <code>GET_ABSENCE_DAYS_PER_TYPE</code> has the same problem.</p>

<div class="am-fig">
<p class="am-fig-title">FILTER VISIBILITY · THE OPAQUE-FILTER PROBLEM</p>
<div style="text-align:center;">
<svg viewBox="0 0 900 380" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Open Sans', system-ui, sans-serif;">
  <defs>
    <pattern id="opacityHatch" x="0" y="0" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="8" stroke="#5a5856" stroke-width="1" opacity="0.4"/>
    </pattern>
    <filter id="boxShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.1"/>
    </filter>
    <marker id="opaqueArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#5a5856" stroke-width="1.4" stroke-linecap="round"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="900" height="380" fill="#fafafa"/>

  <text x="40" y="28" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1.5">FILTER VISIBILITY</text>
  <text x="40" y="46" font-size="14" fill="#1c1c1a" font-weight="600">The opaque-filter problem</text>

  
  <text x="40" y="80" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="0.8">INPUTS</text>
  <g filter="url(#boxShadow)">
    <rect x="40" y="92" width="160" height="32" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <text x="55" y="113" font-size="11.5" fill="#2d2926" font-family="'Fira Code', monospace">person_id</text>
  </g>
  <g filter="url(#boxShadow)">
    <rect x="40" y="132" width="160" height="32" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <text x="55" y="153" font-size="11.5" fill="#2d2926" font-family="'Fira Code', monospace">absence_type_id</text>
  </g>
  <g filter="url(#boxShadow)">
    <rect x="40" y="172" width="160" height="32" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <text x="55" y="193" font-size="11.5" fill="#2d2926" font-family="'Fira Code', monospace">range_start</text>
  </g>
  <g filter="url(#boxShadow)">
    <rect x="40" y="212" width="160" height="32" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <text x="55" y="233" font-size="11.5" fill="#2d2926" font-family="'Fira Code', monospace">range_end</text>
  </g>

  
  <line x1="205" y1="108" x2="345" y2="160" stroke="#5a5856" stroke-width="1" marker-end="url(#opaqueArrow)"/>
  <line x1="205" y1="148" x2="345" y2="170" stroke="#5a5856" stroke-width="1" marker-end="url(#opaqueArrow)"/>
  <line x1="205" y1="188" x2="345" y2="180" stroke="#5a5856" stroke-width="1" marker-end="url(#opaqueArrow)"/>
  <line x1="205" y1="228" x2="345" y2="190" stroke="#5a5856" stroke-width="1" marker-end="url(#opaqueArrow)"/>

  
  <g filter="url(#boxShadow)">
    <rect x="350" y="80" width="220" height="200" rx="6" fill="#1f1d1c"/>
    <rect x="350" y="80" width="220" height="200" rx="6" fill="url(#opacityHatch)" opacity="0.3"/>
    <text x="460" y="115" text-anchor="middle" font-size="11" fill="#8e8b87" letter-spacing="1.5">UNDOCUMENTED</text>
    <text x="460" y="148" text-anchor="middle" font-size="14" fill="#f0ebe6" font-weight="700">Internal status filter</text>
    <line x1="380" y1="165" x2="540" y2="165" stroke="#3a3836" stroke-width="0.6"/>
    <text x="460" y="188" text-anchor="middle" font-size="11.5" fill="#c4c0b8">Sums DURATION column</text>
    <text x="460" y="206" text-anchor="middle" font-size="11.5" fill="#c4c0b8">from ANC_PER_ABS_ENTRIES</text>
    <text x="460" y="228" text-anchor="middle" font-size="11.5" fill="#c4c0b8">Applies internal filter</text>
    <text x="460" y="246" text-anchor="middle" font-size="11.5" fill="#c4c0b8" font-style="italic">filter rule: not published</text>
    <text x="460" y="266" text-anchor="middle" font-size="11.5" fill="#c4c0b8" font-style="italic">filter rule: not stable</text>
  </g>

  
  <line x1="575" y1="180" x2="715" y2="180" stroke="#5a5856" stroke-width="1.4" marker-end="url(#opaqueArrow)"/>

  
  <text x="720" y="80" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="0.8">POSSIBLE OUTPUTS</text>

  <g filter="url(#boxShadow)">
    <rect x="720" y="100" width="150" height="50" rx="4" fill="#fdf2f0" stroke="#c0392b" stroke-width="0.8"/>
    <text x="795" y="120" text-anchor="middle" font-size="10.5" fill="#7a2418" letter-spacing="0.6">SCENARIO A</text>
    <text x="795" y="138" text-anchor="middle" font-size="13" fill="#7a2418" font-weight="700">Returns 8 days</text>
  </g>
  <g filter="url(#boxShadow)">
    <rect x="720" y="158" width="150" height="50" rx="4" fill="#fdf2f0" stroke="#c0392b" stroke-width="0.8"/>
    <text x="795" y="178" text-anchor="middle" font-size="10.5" fill="#7a2418" letter-spacing="0.6">SCENARIO B</text>
    <text x="795" y="196" text-anchor="middle" font-size="13" fill="#7a2418" font-weight="700">Returns 5 days</text>
  </g>
  <g filter="url(#boxShadow)">
    <rect x="720" y="216" width="150" height="50" rx="4" fill="#fdf2f0" stroke="#c0392b" stroke-width="0.8"/>
    <text x="795" y="236" text-anchor="middle" font-size="10.5" fill="#7a2418" letter-spacing="0.6">NEXT QUARTERLY</text>
    <text x="795" y="254" text-anchor="middle" font-size="12.5" fill="#7a2418" font-weight="700">Possibly different</text>
  </g>

  
  <line x1="40" y1="310" x2="870" y2="310" stroke="#ede4e0" stroke-width="1"/>
  <g>
    <rect x="40" y="324" width="830" height="40" rx="4" fill="#fdf6e3" stroke="#b8860b" stroke-width="0.6"/>
    <text x="55" y="343" font-size="11" fill="#7a5800" font-weight="700" letter-spacing="0.5">SOX & AUDIT IMPLICATION</text>
    <text x="55" y="358" font-size="12" fill="#5e4500">If you cannot certify what a function does on every release, it is not safe for governance rules. Prefer mechanisms where the filter is visible in your formula text.</text>
  </g>
</svg>
</div>
<p class="am-fig-caption"><strong>Fig 5 —</strong> The function sums <code>DURATION</code> from <code>ANC_PER_ABS_ENTRIES</code>, but applies an internal filter that Oracle does not document. The same query against the same data could return a different number after a quarterly upgrade, with no compile error to surface the change.</p>
</div>

<div class="am-call warn">
<span class="am-call-tag">⚠️ SOX and audit implication</span>
If you cannot certify what a function does on every release, it is not safe for governance rules. Prefer mechanisms where the filter is visible in your formula text.
</div>

<div class="am-call success">
<span class="am-call-tag">✅ Use it for</span>
Indicative day totals in management reports or debug logging. Do <strong>not</strong> use it for any rule where state-by-state correctness must be certified or audited.
</div>

<hr>

<h2>Mechanism 4 — Read each entry yourself <em>(recommended)</em></h2>

<p>This is the pattern the previous three mechanisms exist as shortcuts for. Verbose, careful with defaults, deliberate with the iteration. In return, it gives you the only path where the filter logic lives <em>inside</em> your formula text and survives quarterly upgrades unchanged.</p>

<h3>Scenario from the UI</h3>

<p>Go back to <strong>Existing Absences</strong>. The page first loads a list of absences — just dates and types. To see the duration breakdown, approval history, or comments for any one of them, you click that row. List first, full details one at a time — that is exactly how Oracle exposes live absence data inside Fast Formula.</p>

<h3>The two-step structure</h3>

<p>If I had seen this diagram three years ago, I would have saved a lot of compile errors. The DBI dictionary for absence entries is <em>not</em> seven parallel arrays you can index by a shared loop counter. It is one list-DBI of entry IDs, plus a set of scalar DBIs that resolve per-entry once you set the right context.</p>

<div class="am-fig">
<p class="am-fig-title">DBI ARCHITECTURE · TWO-STEP MODEL</p>
<div style="text-align:center;">
<svg viewBox="0 0 900 540" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Open Sans', system-ui, sans-serif;">
  <defs>
    <filter id="tierShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
    <marker id="dbiArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#5a5856" stroke-width="1.4" stroke-linecap="round"/>
    </marker>
    <marker id="dbiArrowAccent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#0d7377" stroke-width="1.4" stroke-linecap="round"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="900" height="540" fill="#fafafa"/>

  <text x="40" y="28" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1.5">DBI ARCHITECTURE</text>
  <text x="40" y="46" font-size="14" fill="#1c1c1a" font-weight="600">Two-tier model: one array of IDs, scalar DBIs resolved per-entry</text>

  
  <g filter="url(#tierShadow)">
    <rect x="40" y="68" width="820" height="80" rx="6" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="40" y="68" width="820" height="28" rx="6 6 0 0" fill="#1f1d1c"/>
    <text x="58" y="86" font-size="11" fill="#8e8b87" letter-spacing="1">SOURCE TABLE</text>
    <text x="190" y="86" font-size="12" fill="#f0ebe6" font-weight="600" font-family="'Fira Code', monospace">ANC_PER_ABS_ENTRIES</text>
    <text x="58" y="118" font-size="12" fill="#2d2926">Live absence rows. Updated on every Submit, Approve, Withdraw, Update.</text>
    <text x="58" y="136" font-size="12" fill="#5a5856">Columns: ABSENCE_ENTRY_ID, ABSENCE_TYPE_ID, START_DATE, END_DATE, ABSENCE_STATUS_CD, APPROVAL_STATUS_CD, DURATION, ...</text>
  </g>

  
  <line x1="450" y1="155" x2="450" y2="180" stroke="#5a5856" stroke-width="1.4" marker-end="url(#dbiArrow)"/>
  <text x="460" y="172" font-size="11" fill="#5a5856" font-style="italic">resolved by</text>

  
  <g filter="url(#tierShadow)">
    <rect x="40" y="190" width="820" height="100" rx="6" fill="#f0f3fa" stroke="#4a5d8f" stroke-width="1"/>
    <rect x="40" y="190" width="820" height="28" rx="6 6 0 0" fill="#4a5d8f"/>
    <text x="58" y="208" font-size="11" fill="#dde3f0" letter-spacing="1">TIER 1 · DRIVER ARRAY DBI</text>
    <text x="58" y="240" font-size="12" fill="#2f3e63" font-family="'Fira Code', monospace" font-weight="600">ANC_PER_ABS_ENTRS_ABSENCE_ENTRY_ID_ARR</text>
    <text x="58" y="262" font-size="11.5" fill="#283452">→ resolved inside CHANGE_CONTEXTS(PERSON_ID, EFFECTIVE_DATE [, START_DATE, END_DATE])</text>

    
    <rect x="430" y="232" width="420" height="44" rx="4" fill="#ffffff" stroke="#a8b2c8" stroke-width="0.6"/>
    <text x="445" y="252" font-size="11" fill="#8e8b87" letter-spacing="0.5">arr_entry_id =</text>
    <text x="445" y="268" font-size="11.5" fill="#2f3e63" font-family="'Fira Code', monospace">[ 300012345, 300012451, 300012612, 300012805 ]</text>
  </g>

  
  <line x1="450" y1="297" x2="450" y2="322" stroke="#0d7377" stroke-width="1.4" marker-end="url(#dbiArrowAccent)"/>
  <text x="460" y="314" font-size="11" fill="#0a5a5d" font-style="italic" font-weight="600">for each id, set context, then read scalars</text>

  
  <g filter="url(#tierShadow)">
    <rect x="40" y="332" width="820" height="190" rx="6" fill="#ecf6f1" stroke="#0d7377" stroke-width="1"/>
    <rect x="40" y="332" width="820" height="28" rx="6 6 0 0" fill="#0d7377"/>
    <text x="58" y="350" font-size="11" fill="#dcefe9" letter-spacing="1">TIER 2 · SCALAR DBIs (per-entry, resolved via inner CHANGE_CONTEXTS)</text>

    
    <rect x="58" y="375" width="784" height="34" rx="4" fill="#ffffff" stroke="#7eb5b3" stroke-width="0.8"/>
    <text x="70" y="396" font-size="11.5" fill="#0a5a5d" font-family="'Fira Code', monospace" font-weight="600">CHANGE_CONTEXTS(ABSENCE_ENTRY_ID = 300012345) ( ... read scalars here ... )</text>

    
    <g font-family="'Fira Code', monospace" font-size="11">
      <rect x="58" y="425" width="240" height="28" rx="14" fill="#ffffff" stroke="#0d7377" stroke-width="0.6"/>
      <text x="178" y="443" text-anchor="middle" fill="#0a5a5d" font-weight="600">ANC_ABS_ENTRS_ABSENCE_TYPE_ID</text>

      <rect x="308" y="425" width="240" height="28" rx="14" fill="#ffffff" stroke="#0d7377" stroke-width="0.6"/>
      <text x="428" y="443" text-anchor="middle" fill="#0a5a5d" font-weight="600">ANC_ABS_ENTRS_START_DATE</text>

      <rect x="558" y="425" width="240" height="28" rx="14" fill="#ffffff" stroke="#0d7377" stroke-width="0.6"/>
      <text x="678" y="443" text-anchor="middle" fill="#0a5a5d" font-weight="600">ANC_ABS_ENTRS_END_DATE</text>

      <rect x="58" y="461" width="240" height="28" rx="14" fill="#ffffff" stroke="#0d7377" stroke-width="0.6"/>
      <text x="178" y="479" text-anchor="middle" fill="#0a5a5d" font-weight="600">ANC_ABS_ENTRS_DURATION</text>

      <rect x="308" y="461" width="240" height="28" rx="14" fill="#ffffff" stroke="#0d7377" stroke-width="0.6"/>
      <text x="428" y="479" text-anchor="middle" fill="#0a5a5d" font-weight="600">ANC_ABS_ENTRS_ABSENCE_STATUS_CD</text>

      <rect x="558" y="461" width="240" height="28" rx="14" fill="#ffffff" stroke="#0d7377" stroke-width="0.6"/>
      <text x="678" y="479" text-anchor="middle" fill="#0a5a5d" font-weight="600">ANC_ABS_ENTRS_APPROVAL_STATUS_CD</text>
    </g>

    <text x="58" y="510" font-size="11" fill="#08474a" font-style="italic">Note the prefix shift: <tspan font-family="'Fira Code', monospace" font-weight="600">ANC_PER_ABS_ENTRS_</tspan> for the array, <tspan font-family="'Fira Code', monospace" font-weight="600">ANC_ABS_ENTRS_</tspan> for the scalars. No PER, no _ARR.</text>
  </g>
</svg>
</div>
<p class="am-fig-caption"><strong>Fig 6 —</strong> The documented Oracle DBI model for live absence entries. <strong>One</strong> array DBI (Tier 1), <strong>six</strong> scalar DBIs (Tier 2). The trap that catches most authors is reaching for parallel <code>_ARR</code> siblings — <code>ANC_PER_ABS_ENTRS_START_DATE_ARR</code>, <code>..._APPROVAL_STATUS_CD_ARR</code>, and so on — which do not exist in the dictionary. Code that references them looks plausible but does not compile.</p>
</div>

<h3>Going through the list one entry at a time</h3>

<p>Once you have the list of IDs, you walk through it one ID at a time. For each ID, you switch focus to that entry, read its details, decide if it counts, and add to your running total. Then move to the next ID.</p>

<div class="am-fig">
<p class="am-fig-title">FLOWCHART · LIVE-LOOP CONTROL FLOW</p>
<div style="text-align:center;">
<svg viewBox="0 0 900 520" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Open Sans', system-ui, sans-serif;">
  <defs>
    <filter id="flowShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-opacity="0.1"/>
    </filter>
    <marker id="flowArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#5a5856" stroke-width="1.5" stroke-linecap="round"/>
    </marker>
    <marker id="flowArrowGreen" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#0d7377" stroke-width="1.5" stroke-linecap="round"/>
    </marker>
    <marker id="flowArrowRed" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#c0392b" stroke-width="1.5" stroke-linecap="round"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="900" height="520" fill="#fafafa"/>

  <text x="40" y="28" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1.5">FLOWCHART · LIVE-LOOP CONTROL FLOW</text>
  <text x="40" y="46" font-size="14" fill="#1c1c1a" font-weight="600">Iterating the driver array with proper guards</text>

  
  <g filter="url(#flowShadow)">
    <ellipse cx="160" cy="100" rx="70" ry="22" fill="#1f1d1c"/>
    <text x="160" y="105" text-anchor="middle" font-size="12" fill="#f0ebe6" font-weight="600" letter-spacing="0.6">START</text>
  </g>

  
  <line x1="160" y1="123" x2="160" y2="148" stroke="#5a5856" stroke-width="1.4" marker-end="url(#flowArrow)"/>
  <g filter="url(#flowShadow)">
    <rect x="65" y="150" width="190" height="56" rx="4" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <text x="160" y="172" text-anchor="middle" font-size="12" fill="#2d2926" font-weight="600">Init: g_consumed = 0</text>
    <text x="160" y="190" text-anchor="middle" font-size="11" fill="#5a5856" font-family="'Fira Code', monospace">NI = arr.FIRST(-1)</text>
  </g>

  
  <line x1="160" y1="207" x2="160" y2="232" stroke="#5a5856" stroke-width="1.4" marker-end="url(#flowArrow)"/>
  <g filter="url(#flowShadow)">
    <polygon points="160,235 270,295 160,355 50,295" fill="#fdf6e3" stroke="#b8860b" stroke-width="1"/>
    <text x="160" y="290" text-anchor="middle" font-size="12" fill="#7a5800" font-weight="600">arr.EXISTS(NI)?</text>
    <text x="160" y="308" text-anchor="middle" font-size="10.5" fill="#7a5800" font-family="'Fira Code', monospace">while-loop guard</text>
  </g>

  
  <line x1="270" y1="295" x2="320" y2="295" stroke="#0d7377" stroke-width="1.4" marker-end="url(#flowArrowGreen)"/>
  <text x="278" y="287" font-size="11" fill="#0a5a5d" font-weight="700">NO</text>
  <g filter="url(#flowShadow)">
    <ellipse cx="395" cy="295" rx="75" ry="22" fill="#0d7377"/>
    <text x="395" y="300" text-anchor="middle" font-size="12" fill="#ffffff" font-weight="600" letter-spacing="0.4">RETURN total</text>
  </g>

  
  <line x1="160" y1="356" x2="160" y2="380" stroke="#5a5856" stroke-width="1.4" marker-end="url(#flowArrow)"/>
  <text x="118" y="367" font-size="11" fill="#5a5856" font-weight="700">YES</text>

  <g filter="url(#flowShadow)">
    <rect x="65" y="382" width="190" height="46" rx="4" fill="#f0f3fa" stroke="#4a5d8f" stroke-width="0.8"/>
    <text x="160" y="402" text-anchor="middle" font-size="11.5" fill="#2f3e63" font-weight="600">Set ABSENCE_ENTRY_ID ctx</text>
    <text x="160" y="418" text-anchor="middle" font-size="10.5" fill="#2f3e63" font-family="'Fira Code', monospace">CHANGE_CONTEXTS(...)</text>
  </g>

  
  <line x1="255" y1="405" x2="305" y2="405" stroke="#5a5856" stroke-width="1.4" marker-end="url(#flowArrow)"/>
  <g filter="url(#flowShadow)">
    <rect x="307" y="382" width="180" height="46" rx="4" fill="#ecf6f1" stroke="#0d7377" stroke-width="0.8"/>
    <text x="397" y="402" text-anchor="middle" font-size="11.5" fill="#0a5a5d" font-weight="600">Read 6 scalar DBIs</text>
    <text x="397" y="418" text-anchor="middle" font-size="10.5" fill="#0a5a5d">type, dates, status, duration</text>
  </g>

  
  <line x1="487" y1="405" x2="540" y2="405" stroke="#5a5856" stroke-width="1.4" marker-end="url(#flowArrow)"/>
  <g filter="url(#flowShadow)">
    <polygon points="640,378 720,408 640,438 560,408" fill="#fdf2f0" stroke="#c0392b" stroke-width="1"/>
    <text x="640" y="404" text-anchor="middle" font-size="11.5" fill="#7a2418" font-weight="600">Filter:</text>
    <text x="640" y="420" text-anchor="middle" font-size="10.5" fill="#7a2418">type? not-self?</text>
    <text x="640" y="432" text-anchor="middle" font-size="10.5" fill="#7a2418">status valid?</text>
  </g>

  
  <line x1="640" y1="378" x2="640" y2="160" stroke="#c0392b" stroke-width="1.2" stroke-dasharray="4 3"/>
  <line x1="640" y1="160" x2="280" y2="160" stroke="#c0392b" stroke-width="1.2" stroke-dasharray="4 3"/>
  <line x1="280" y1="160" x2="280" y2="200" stroke="#c0392b" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#flowArrowRed)"/>
  <text x="650" y="270" font-size="11" fill="#7a2418" font-weight="700">NO</text>
  <text x="650" y="285" font-size="10.5" fill="#7a2418" font-style="italic">skip entry</text>

  
  <line x1="720" y1="408" x2="755" y2="408" stroke="#0d7377" stroke-width="1.4" marker-end="url(#flowArrowGreen)"/>
  <text x="725" y="400" font-size="11" fill="#0a5a5d" font-weight="700">YES</text>

  <g filter="url(#flowShadow)">
    <rect x="755" y="385" width="120" height="46" rx="4" fill="#ecf6f1" stroke="#0d7377" stroke-width="0.8"/>
    <text x="815" y="404" text-anchor="middle" font-size="11.5" fill="#0a5a5d" font-weight="600">g_consumed +=</text>
    <text x="815" y="420" text-anchor="middle" font-size="11.5" fill="#0a5a5d" font-weight="600">duration</text>
  </g>

  
  <line x1="815" y1="431" x2="815" y2="475" stroke="#5a5856" stroke-width="1.4"/>
  <line x1="815" y1="475" x2="160" y2="475" stroke="#5a5856" stroke-width="1.4"/>
  <line x1="160" y1="475" x2="160" y2="358" stroke="#5a5856" stroke-width="1.4" marker-end="url(#flowArrow)"/>

  
  <g>
    <rect x="380" y="465" width="200" height="20" rx="3" fill="#fafafa" stroke="none"/>
    <text x="480" y="479" text-anchor="middle" font-size="10.5" fill="#5a5856" font-family="'Fira Code', monospace">NI = arr.NEXT(NI, -1)</text>
  </g>

  
  <g transform="translate(40, 502)">
    <rect x="0" y="-10" width="14" height="14" rx="2" fill="#1f1d1c"/>
    <text x="22" y="0" font-size="11" fill="#5a5856">Terminal</text>

    <rect x="100" y="-10" width="14" height="14" rx="2" fill="#ffffff" stroke="#d4cdc6"/>
    <text x="122" y="0" font-size="11" fill="#5a5856">Process</text>

    <polygon points="200,-10 214,-3 200,4 186,-3" fill="#fdf6e3" stroke="#b8860b"/>
    <text x="222" y="0" font-size="11" fill="#5a5856">Decision</text>

    <line x1="298" y1="-3" x2="328" y2="-3" stroke="#c0392b" stroke-width="1.2" stroke-dasharray="4 3"/>
    <text x="336" y="0" font-size="11" fill="#5a5856">Skip path</text>
  </g>
</svg>
</div>
<p class="am-fig-caption"><strong>Fig 7 —</strong> Loop control flow with proper UML/BPMN symbology. Five distinct guards shape the path: array existence (top diamond), entry-type match, self-exclusion (the entry being validated must not count itself), absence-status filter, and approval-status filter. Failure on any guard skips the entry without aborting the loop.</p>
</div>

<h3>Two syntactic landmines</h3>

<p>Get these two wrong and your formula will not compile. Both are easy to copy from older blogs that show pre-current syntax.</p>

<table>
<thead><tr><th>Looks plausible · will not compile</th><th>Documented Oracle pattern</th></tr></thead>
<tbody>
<tr>
<td><code>FIRST_INDEX('N', arr)</code><br><code>NEXT_INDEX('N', arr, i)</code><br><code>WHILE i WAS NOT DEFAULTED</code></td>
<td><code>arr.FIRST(-1)</code><br><code>arr.NEXT(i, -1)</code><br><code>WHILE arr.EXISTS(i)</code></td>
</tr>
<tr>
<td><code>EMPTY_NUMBER_DATE</code><br><span style="font-size:12px;color:#7a2418;">DATE cannot be an index type</span></td>
<td><code>EMPTY_DATE_NUMBER</code><br><span style="font-size:12px;color:#0a5a5d;">format: <code>EMPTY_<data>_<index></code></span></td>
</tr>
</tbody>
</table>

<div class="am-call success">
<span class="am-call-tag">✅ Use it for</span>
Any rule that needs an accurate live balance — real-time validation, audit-grade governance, anything where you need to defend the number. The verbosity is the price; correctness is what you buy.
</div>

<hr>

<h2>Snapshot vs Live — The Architectural Split</h2>

<p>The four mechanisms split cleanly across two underlying data sources. This is the diagnostic question to ask before writing any balance formula.</p>

<div class="am-fig">
<p class="am-fig-title">DATA TOPOLOGY · SNAPSHOT VS LIVE</p>
<div style="text-align:center;">
<svg viewBox="0 0 900 420" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Open Sans', system-ui, sans-serif;">
  <defs>
    <filter id="worldShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-opacity="0.08"/>
    </filter>
    <marker id="syncArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#8e8b87" stroke-width="1.4" stroke-linecap="round"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="900" height="420" fill="#fafafa"/>

  <text x="40" y="28" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1.5">DATA TOPOLOGY</text>
  <text x="40" y="46" font-size="14" fill="#1c1c1a" font-weight="600">Two worlds, periodically reconciled by the absence engine</text>

  
  <g filter="url(#worldShadow)">
    <rect x="40" y="76" width="380" height="320" rx="8" fill="#ffffff" stroke="#4a5d8f" stroke-width="1"/>
    <rect x="40" y="76" width="380" height="44" rx="8 8 0 0" fill="#4a5d8f"/>
    <text x="60" y="104" font-size="11" fill="#dde3f0" letter-spacing="1.2">SNAPSHOT WORLD</text>
    <text x="240" y="104" font-size="11" fill="#dde3f0" letter-spacing="0.5" text-anchor="end" opacity="0.7" transform="translate(160, 0)">Updated by batch</text>
  </g>

  <text x="60" y="148" font-size="13" fill="#2f3e63" font-weight="700" font-family="'Fira Code', monospace">ANC_PER_ACRL_ENTRY_DTLS</text>
  <text x="60" y="166" font-size="11" fill="#5a5856">Committed accrual ledger</text>

  
  <g font-size="12" fill="#2d2926">
    <circle cx="68" cy="200" r="2" fill="#4a5d8f"/>
    <text x="78" y="204">Updated only when accrual engine runs</text>
    <circle cx="68" cy="222" r="2" fill="#4a5d8f"/>
    <text x="78" y="226">Lags reality by 12 to 24 hours</text>
    <circle cx="68" cy="244" r="2" fill="#4a5d8f"/>
    <text x="78" y="248">Aggregated, fast, contractually stable</text>
    <circle cx="68" cy="266" r="2" fill="#4a5d8f"/>
    <text x="78" y="270">Reflects only finalised consumption</text>
  </g>

  <line x1="60" y1="290" x2="400" y2="290" stroke="#ede4e0" stroke-width="0.8"/>

  <text x="60" y="310" font-size="10.5" fill="#8e8b87" letter-spacing="0.8" font-weight="600">CONSUMED BY</text>
  <rect x="60" y="318" width="170" height="26" rx="13" fill="#f0f3fa" stroke="#4a5d8f" stroke-width="0.6"/>
  <text x="145" y="335" text-anchor="middle" font-size="11" fill="#2f3e63" font-family="'Fira Code', monospace" font-weight="600">GET_PLAN_BALANCE</text>

  <text x="60" y="370" font-size="10.5" fill="#8e8b87" letter-spacing="0.8" font-weight="600">USE WHEN</text>
  <text x="60" y="386" font-size="12" fill="#2d2926" font-style="italic">Carryover, period-end, opening anchor</text>

  
  <g filter="url(#worldShadow)">
    <rect x="480" y="76" width="380" height="320" rx="8" fill="#ffffff" stroke="#0d7377" stroke-width="1"/>
    <rect x="480" y="76" width="380" height="44" rx="8 8 0 0" fill="#0d7377"/>
    <text x="500" y="104" font-size="11" fill="#dcefe9" letter-spacing="1.2">LIVE WORLD</text>
    <text x="840" y="104" font-size="11" fill="#dcefe9" letter-spacing="0.5" text-anchor="end" opacity="0.7">Updated transactionally</text>
  </g>

  <text x="500" y="148" font-size="13" fill="#0a5a5d" font-weight="700" font-family="'Fira Code', monospace">ANC_PER_ABS_ENTRIES</text>
  <text x="500" y="166" font-size="11" fill="#5a5856">Real-time absence collection</text>

  <g font-size="12" fill="#2d2926">
    <circle cx="508" cy="200" r="2" fill="#0d7377"/>
    <text x="518" y="204">Updated on every Submit / Approve / Withdraw</text>
    <circle cx="508" cy="222" r="2" fill="#0d7377"/>
    <text x="518" y="226">Reflects this instant, no lag</text>
    <circle cx="508" cy="244" r="2" fill="#0d7377"/>
    <text x="518" y="248">Granular, current, volatile</text>
    <circle cx="508" cy="266" r="2" fill="#0d7377"/>
    <text x="518" y="270">No lifecycle filter applied at storage</text>
  </g>

  <line x1="500" y1="290" x2="840" y2="290" stroke="#ede4e0" stroke-width="0.8"/>

  <text x="500" y="310" font-size="10.5" fill="#8e8b87" letter-spacing="0.8" font-weight="600">CONSUMED BY</text>
  <g font-family="'Fira Code', monospace" font-size="10">
    <rect x="500" y="318" width="105" height="22" rx="11" fill="#fdf2f0" stroke="#c0392b" stroke-width="0.6"/>
    <text x="552" y="333" text-anchor="middle" fill="#7a2418" font-weight="600">GET_ABSENCE_COUNTS</text>

    <rect x="612" y="318" width="120" height="22" rx="11" fill="#fdf2f0" stroke="#c0392b" stroke-width="0.6"/>
    <text x="672" y="333" text-anchor="middle" fill="#7a2418" font-weight="600">GET_ABSENCE_DAYS_PER_TYPE</text>

    <rect x="500" y="346" width="170" height="22" rx="11" fill="#ecf6f1" stroke="#0d7377" stroke-width="0.8"/>
    <text x="585" y="361" text-anchor="middle" fill="#0a5a5d" font-weight="700">DBI driver + scalars · recommended</text>
  </g>

  <text x="500" y="385" font-size="12" fill="#2d2926" font-style="italic">Real-time decisions, audit-grade governance</text>

  
  <line x1="425" y1="240" x2="475" y2="240" stroke="#8e8b87" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#syncArrow)"/>
  <text x="450" y="232" text-anchor="middle" font-size="10" fill="#8e8b87">batch</text>
  <text x="450" y="258" text-anchor="middle" font-size="10" fill="#8e8b87" font-style="italic">reconciles</text>
</svg>
</div>
<p class="am-fig-caption"><strong>Fig 8 —</strong> The two data worlds. The accrual engine periodically reconciles the live collection into the snapshot ledger, but between engine runs the two are out of sync — which is why the same person can have a different "balance" depending on which world your formula reads.</p>
</div>

<div class="am-call note">
<span class="am-call-tag">📌 Diagnostic question</span>
If a user submits an absence and immediately submits a second one, does my formula need to <em>see</em> the first submission? If yes — live world. If no — snapshot world is fine, and the simpler <code>GET_PLAN_BALANCE</code> path is appropriate.
</div>

<hr>

<h2>The Status-Code Naming Trap</h2>

<p>Of all the silent bugs in this domain, this one accounts for more support tickets than the rest combined. Two columns describe an absence's status. They use <em>different</em> naming conventions. A filter that looks correct against one column is a no-op against the other.</p>

<div class="am-fig">
<p class="am-fig-title">DIAGNOSTIC · THE STATUS-CODE NAMING TRAP</p>
<div style="text-align:center;">
<svg viewBox="0 0 900 440" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Open Sans', system-ui, sans-serif;">
  <defs>
    <filter id="trapShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="900" height="440" fill="#fafafa"/>

  <text x="40" y="28" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1.5">DIAGNOSTIC</text>
  <text x="40" y="46" font-size="14" fill="#1c1c1a" font-weight="600">Two status columns, two naming conventions, one common bug</text>

  
  <g filter="url(#trapShadow)">
    <rect x="40" y="74" width="390" height="240" rx="6" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="40" y="74" width="390" height="36" rx="6 6 0 0" fill="#faf6f3"/>
    <text x="60" y="97" font-size="13" fill="#1c1c1a" font-weight="700" font-family="'Fira Code', monospace">ABSENCE_STATUS_CD</text>
  </g>

  <text x="60" y="135" font-size="11" fill="#8e8b87" letter-spacing="0.6" font-weight="600">LOOKUP FRAMEWORK</text>
  <text x="60" y="153" font-size="12" fill="#2d2926" font-family="'Fira Code', monospace">ANC_PER_ABS_ENT_DISPLAY_STATUS</text>
  <text x="60" y="170" font-size="11" fill="#6b6b6b" font-style="italic">Display lookup for the absence lifecycle column</text>

  <text x="60" y="197" font-size="11" fill="#8e8b87" letter-spacing="0.6" font-weight="600">PREFIX CONVENTION</text>
  <g filter="url(#trapShadow)">
    <rect x="60" y="207" width="80" height="28" rx="14" fill="#fdf2f0" stroke="#c0392b" stroke-width="1.2"/>
    <text x="100" y="225" text-anchor="middle" font-size="13" fill="#7a2418" font-weight="700" font-family="'Fira Code', monospace">ORA_</text>
  </g>

  <text x="60" y="265" font-size="11" fill="#8e8b87" letter-spacing="0.6" font-weight="600">STORED VALUES</text>
  <g font-family="'Fira Code', monospace" font-size="11.5" fill="#2d2926">
    <text x="60" y="284">ORA_SUBMITTED</text>
    <text x="220" y="284">ORA_COMPLETED</text>
    <text x="60" y="302">ORA_WITHDRAWN</text>
    <text x="220" y="302">ORA_IN_PROGRESS</text>
  </g>

  
  <g filter="url(#trapShadow)">
    <rect x="470" y="74" width="390" height="240" rx="6" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="470" y="74" width="390" height="36" rx="6 6 0 0" fill="#faf6f3"/>
    <text x="490" y="97" font-size="13" fill="#1c1c1a" font-weight="700" font-family="'Fira Code', monospace">APPROVAL_STATUS_CD</text>
  </g>

  <text x="490" y="135" font-size="11" fill="#8e8b87" letter-spacing="0.6" font-weight="600">LOOKUP FRAMEWORK</text>
  <text x="490" y="153" font-size="12" fill="#2d2926">AMX approval framework</text>
  <text x="490" y="170" font-size="11" fill="#6b6b6b" font-style="italic">Workflow status maintained by the AMX engine</text>

  <text x="490" y="197" font-size="11" fill="#8e8b87" letter-spacing="0.6" font-weight="600">PREFIX CONVENTION</text>
  <g filter="url(#trapShadow)">
    <rect x="490" y="207" width="80" height="28" rx="14" fill="#fdf6e3" stroke="#b8860b" stroke-width="1.2"/>
    <text x="530" y="225" text-anchor="middle" font-size="12" fill="#7a5800" font-weight="700">(none)</text>
  </g>

  <text x="490" y="265" font-size="11" fill="#8e8b87" letter-spacing="0.6" font-weight="600">STORED VALUES</text>
  <g font-family="'Fira Code', monospace" font-size="11.5" fill="#2d2926">
    <text x="490" y="284">SUBMITTED</text>
    <text x="650" y="284">APPROVED</text>
    <text x="490" y="302">WITHDRAWN</text>
    <text x="650" y="302">DENIED</text>
  </g>

  
  <g filter="url(#trapShadow)">
    <rect x="40" y="332" width="820" height="92" rx="6" fill="#1f1d1c"/>
    <text x="60" y="356" font-size="11" fill="#8e8b87" letter-spacing="1.2">THE COMMON BUG</text>

    <text x="60" y="380" font-size="12" fill="#fdf2f0" font-family="'Fira Code', monospace">IF arr_app_status[i] <> 'ORA_WITHDRAWN' THEN  ...</text>

    <line x1="60" y1="392" x2="385" y2="392" stroke="#c0392b" stroke-width="2"/>

    <text x="60" y="408" font-size="11.5" fill="#f4a59a">Always TRUE. APPROVAL_STATUS_CD never carries the ORA_ prefix.</text>
    <text x="60" y="421" font-size="11.5" fill="#f4a59a">The filter is silently a no-op. Withdrawn entries pass through. The formula compiles and ships.</text>
  </g>
</svg>
</div>
<p class="am-fig-caption"><strong>Fig 9 —</strong> The asymmetry is structural — the two columns originate in different framework layers and follow different conventions. There is no Oracle plan to reconcile them. The defensive practice is to filter on both columns with both naming conventions, every time.</p>
</div>

<div class="am-call warn">
<span class="am-call-tag">⚠️ The bug everyone ships at least once</span>
Writing <code>IF arr_app_status[i] <> 'ORA_WITHDRAWN'</code> on the approval column is always TRUE — because that column never carries the <code>ORA_</code> prefix. The filter is a silent no-op. Withdrawn entries pass through. The formula compiles and ships.
</div>

<div class="am-call note">
<span class="am-call-tag">📌 Edge case worth knowing — MOS 2624787.1</span>
The two columns can drift in administrative-cancellation paths. An absence reaching <code>ABSENCE_STATUS_CD = 'ORA_COMPLETED'</code> can be retroactively cancelled in error/expiry flows such that only <code>APPROVAL_STATUS_CD</code> updates. A two-pronged filter catches both paths; a single-column filter misses them.
</div>

<p>The defensive pattern, every time:</p>

<pre><code>IF abs_status <> 'ORA_WITHDRAWN'
   AND app_status <> 'WITHDRAWN'
   AND app_status <> 'DENIED' THEN
  /* this entry counts towards consumption */
END IF</code></pre>

<hr>

<h2>The Composite Pattern — Snapshot Anchor + Live Loop</h2>

<p>For accurate live balance, the working practitioner pattern combines two of the four mechanisms. <code>GET_PLAN_BALANCE</code> gives you the starting balance. Mechanism 4 gives you the live adjustment. The result is a balance that is both contractually stable and current to this instant.</p>

<div class="am-fig">
<p class="am-fig-title">COMPOSITE PATTERN · END-TO-END</p>
<div style="text-align:center;">
<svg viewBox="0 0 900 380" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Open Sans', system-ui, sans-serif;">
  <defs>
    <filter id="stepShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
    <marker id="stepArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#5a5856" stroke-width="1.5" stroke-linecap="round"/>
    </marker>
    <marker id="exitArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M2 1 L9 5 L2 9" fill="none" stroke="#0d7377" stroke-width="1.5" stroke-linecap="round"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="900" height="380" fill="#fafafa"/>

  <text x="40" y="28" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1.5">COMPOSITE PATTERN</text>
  <text x="40" y="46" font-size="14" fill="#1c1c1a" font-weight="600">Snapshot anchor + early-exit guard + live loop = correct balance</text>

  
  <g filter="url(#stepShadow)">
    <rect x="40" y="80" width="190" height="120" rx="6" fill="#ffffff" stroke="#4a5d8f" stroke-width="0.8"/>
    <rect x="40" y="80" width="190" height="32" rx="6 6 0 0" fill="#4a5d8f"/>
    <circle cx="62" cy="96" r="11" fill="#ffffff"/>
    <text x="62" y="100" text-anchor="middle" font-size="12" fill="#2f3e63" font-weight="700">1</text>
    <text x="80" y="100" font-size="11" fill="#dde3f0" letter-spacing="0.6" font-weight="600">SNAPSHOT ANCHOR</text>

    <text x="135" y="138" text-anchor="middle" font-size="11.5" fill="#1c1c1a" font-weight="600" font-family="'Fira Code', monospace">GET_PLAN_BALANCE</text>
    <text x="135" y="156" text-anchor="middle" font-size="11.5" fill="#1c1c1a" font-family="'Fira Code', monospace">('AL Plan')</text>
    <line x1="60" y1="170" x2="210" y2="170" stroke="#ede4e0" stroke-width="0.8"/>
    <text x="135" y="188" text-anchor="middle" font-size="11.5" fill="#0a5a5d" font-weight="700">opening = 5.0</text>
  </g>

  <line x1="232" y1="140" x2="262" y2="140" stroke="#5a5856" stroke-width="1.5" marker-end="url(#stepArrow)"/>

  
  <g filter="url(#stepShadow)">
    <rect x="265" y="80" width="190" height="120" rx="6" fill="#ffffff" stroke="#b8860b" stroke-width="0.8"/>
    <rect x="265" y="80" width="190" height="32" rx="6 6 0 0" fill="#b8860b"/>
    <circle cx="287" cy="96" r="11" fill="#ffffff"/>
    <text x="287" y="100" text-anchor="middle" font-size="12" fill="#7a5800" font-weight="700">2</text>
    <text x="305" y="100" font-size="11" fill="#fdf6e3" letter-spacing="0.6" font-weight="600">EARLY-EXIT GUARD</text>

    <text x="360" y="138" text-anchor="middle" font-size="11.5" fill="#1c1c1a" font-family="'Fira Code', monospace">IF opening <= 0</text>
    <text x="360" y="156" text-anchor="middle" font-size="11.5" fill="#1c1c1a" font-family="'Fira Code', monospace">THEN return 0</text>
    <line x1="285" y1="170" x2="435" y2="170" stroke="#ede4e0" stroke-width="0.8"/>
    <text x="360" y="188" text-anchor="middle" font-size="11" fill="#7a5800" font-style="italic">skip live loop</text>
  </g>

  
  <line x1="360" y1="201" x2="360" y2="270" stroke="#0d7377" stroke-width="1.5" stroke-dasharray="4 3" marker-end="url(#exitArrow)"/>
  <text x="370" y="240" font-size="10.5" fill="#0a5a5d" font-style="italic">if 0</text>

  <line x1="457" y1="140" x2="487" y2="140" stroke="#5a5856" stroke-width="1.5" marker-end="url(#stepArrow)"/>

  
  <g filter="url(#stepShadow)">
    <rect x="490" y="80" width="190" height="120" rx="6" fill="#ffffff" stroke="#0d7377" stroke-width="0.8"/>
    <rect x="490" y="80" width="190" height="32" rx="6 6 0 0" fill="#0d7377"/>
    <circle cx="512" cy="96" r="11" fill="#ffffff"/>
    <text x="512" y="100" text-anchor="middle" font-size="12" fill="#0a5a5d" font-weight="700">3</text>
    <text x="530" y="100" font-size="11" fill="#dcefe9" letter-spacing="0.6" font-weight="600">LIVE LOOP</text>

    <text x="585" y="138" text-anchor="middle" font-size="11" fill="#1c1c1a">Driver array → scalars</text>
    <text x="585" y="156" text-anchor="middle" font-size="11" fill="#1c1c1a">→ filter → accumulate</text>
    <line x1="510" y1="170" x2="660" y2="170" stroke="#ede4e0" stroke-width="0.8"/>
    <text x="585" y="188" text-anchor="middle" font-size="11.5" fill="#0a5a5d" font-weight="700">consumed = 3.0</text>
  </g>

  <line x1="682" y1="140" x2="712" y2="140" stroke="#5a5856" stroke-width="1.5" marker-end="url(#stepArrow)"/>

  
  <g filter="url(#stepShadow)">
    <rect x="715" y="80" width="155" height="120" rx="6" fill="#ffffff" stroke="#c0392b" stroke-width="1.2"/>
    <rect x="715" y="80" width="155" height="32" rx="6 6 0 0" fill="#c0392b"/>
    <circle cx="737" cy="96" r="11" fill="#ffffff"/>
    <text x="737" y="100" text-anchor="middle" font-size="12" fill="#7a2418" font-weight="700">4</text>
    <text x="755" y="100" font-size="11" fill="#fdf2f0" letter-spacing="0.6" font-weight="600">RECONCILE</text>

    <text x="792" y="138" text-anchor="middle" font-size="11.5" fill="#1c1c1a" font-family="'Fira Code', monospace">live = opening</text>
    <text x="792" y="155" text-anchor="middle" font-size="11.5" fill="#1c1c1a" font-family="'Fira Code', monospace">- consumed</text>
    <line x1="730" y1="170" x2="855" y2="170" stroke="#ede4e0" stroke-width="0.8"/>
    <text x="792" y="190" text-anchor="middle" font-size="13" fill="#7a2418" font-weight="700">live = 2.0</text>
  </g>

  
  <line x1="792" y1="201" x2="792" y2="280" stroke="#5a5856" stroke-width="1.5"/>
  <line x1="360" y1="280" x2="792" y2="280" stroke="#5a5856" stroke-width="1.5"/>
  <line x1="576" y1="280" x2="576" y2="305" stroke="#5a5856" stroke-width="1.5" marker-end="url(#stepArrow)"/>

  <g filter="url(#stepShadow)">
    <ellipse cx="576" cy="328" rx="160" ry="22" fill="#1f1d1c"/>
    <text x="576" y="333" text-anchor="middle" font-size="12" fill="#f0ebe6" font-weight="600" letter-spacing="0.6">RETURN g_live_balance</text>
  </g>

  
  <g>
    <rect x="40" y="245" width="280" height="58" rx="4" fill="#ecf6f1" stroke="#0d7377" stroke-width="0.6"/>
    <text x="55" y="263" font-size="10.5" fill="#0a5a5d" letter-spacing="0.6" font-weight="700">PERFORMANCE NOTE</text>
    <text x="55" y="280" font-size="11" fill="#08474a">In Q4 peak load, ~30% of employees</text>
    <text x="55" y="295" font-size="11" fill="#08474a">have exhausted balance and exit at step 2.</text>
  </g>
</svg>
</div>
<p class="am-fig-caption"><strong>Fig 10 —</strong> The composite pattern, end-to-end. Step 2 is not just hygiene — on plans with high consumption rates it short-circuits a non-trivial fraction of formula executions, which matters at year-end peak load.</p>
</div>

<h3>The Production-Ready Recipe</h3>

<p>Below is the full reader. It returns <code>g_live_balance</code> for whatever calling formula type wraps it — Entry Validation will use it to drive a <code>VALID</code>/<code>ERROR_MESSAGE</code> decision, a Plan Use Rate formula will use it to compute deduction, a Type Duration formula will use it to constrain the duration calculation. Only the way you consume the final number changes.</p>

<pre><code>/******************************************************************
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
IF g_opening <= 0 THEN
(
  g_live_balance = 0
  RETURN g_live_balance
)

/* G. STEP 1 — resolve the list of entry IDs */
CHANGE_CONTEXTS(PERSON_ID      = l_person,
                EFFECTIVE_DATE = l_eff_date)
(
  arr_entry_id = ANC_PER_ABS_ENTRS_ABSENCE_ENTRY_ID_ARR
)

/* H. STEP 2 — loop through, read scalars per entry, filter, accumulate */
g_consumed = 0
NI = arr_entry_id.FIRST(-1)

WHILE arr_entry_id.EXISTS(NI) LOOP
(
  l_entry_id = arr_entry_id[NI]

  CHANGE_CONTEXTS(ABSENCE_ENTRY_ID = l_entry_id)
  (
    l_type_id    = ANC_ABS_ENTRS_ABSENCE_TYPE_ID
    l_abs_status = ANC_ABS_ENTRS_ABSENCE_STATUS_CD
    l_app_status = ANC_ABS_ENTRS_APPROVAL_STATUS_CD
    l_duration   = ANC_ABS_ENTRS_DURATION
  )

  /* Nested IFs — guaranteed skip, no short-circuit assumption */
  IF l_type_id = iv_target_type_id THEN
  (
    IF l_entry_id <> l_self_entry_id THEN
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
IF g_live_balance < 0 THEN g_live_balance = 0

RETURN g_live_balance
</code></pre>

<div class="am-call success">
<span class="am-call-tag">✅ What this recipe covers</span>
<strong>Snapshot anchor</strong> — <code>GET_PLAN_BALANCE</code> for the stable starting number. <strong>Early-exit guard</strong> — cheap short-circuit when nothing remains to subtract from. <strong>Step 1 + Step 2 DBI pattern</strong> — list of IDs, then per-entry scalar reads inside <code>CHANGE_CONTEXTS</code>. <strong>Self-exclusion</strong> — the entry being validated does not count itself. <strong>Both-column status filter</strong> — ORA_ on lifecycle, no prefix on approval. <strong>Reconciliation</strong> — floor at zero. Every guard is explicit and auditable.
</div>

<hr>

<h2>Anti-Pattern Catalogue — Five Mistakes That Ship Silently</h2>

<p>If you have written Absence Fast Formulas long enough, you have seen all five — usually in code you wrote yourself a year earlier. Numbers 1, 3, and 4 surface as compile errors or empty results eventually. Numbers 2 and 5 are the silent ones — the formula compiles, runs, and returns subtly wrong numbers.</p>

<div class="am-fig">
<p class="am-fig-title">ANTI-PATTERN CATALOGUE</p>
<div style="text-align:center;">
<svg viewBox="0 0 900 480" xmlns="http://www.w3.org/2000/svg" style="font-family: 'Open Sans', system-ui, sans-serif;">
  <defs>
    <filter id="apShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="900" height="480" fill="#fafafa"/>

  <text x="40" y="28" font-size="11" fill="#8e8b87" font-weight="600" letter-spacing="1.5">FIVE WAYS TO SHIP A SILENT BUG</text>
  <text x="40" y="46" font-size="14" fill="#1c1c1a" font-weight="600">Anti-pattern catalogue</text>

  
  <g filter="url(#apShadow)">
    <rect x="40" y="76" width="410" height="120" rx="6" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="40" y="76" width="34" height="120" rx="6 0 0 6" fill="#c0392b"/>
    <text x="57" y="142" text-anchor="middle" font-size="22" fill="#ffffff" font-weight="700">1</text>
    <text x="86" y="100" font-size="13" fill="#1c1c1a" font-weight="700">Three-arg call to GET_PLAN_BALANCE</text>
    <text x="86" y="120" font-size="11.5" fill="#5a5856" font-family="'Fira Code', monospace">GET_PLAN_BALANCE(person, plan, date)</text>
    <line x1="86" y1="135" x2="430" y2="135" stroke="#ede4e0" stroke-width="0.6"/>
    <text x="86" y="155" font-size="11" fill="#5a5856" letter-spacing="0.5" font-weight="600">FIX</text>
    <text x="86" y="172" font-size="11.5" fill="#0a5a5d" font-family="'Fira Code', monospace">GET_PLAN_BALANCE('Annual Leave Plan')</text>
    <text x="86" y="187" font-size="10.5" fill="#5a5856" font-style="italic">Person/date are contexts, not arguments</text>
  </g>

  
  <g filter="url(#apShadow)">
    <rect x="470" y="76" width="410" height="120" rx="6" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="470" y="76" width="34" height="120" rx="6 0 0 6" fill="#c0392b"/>
    <text x="487" y="142" text-anchor="middle" font-size="22" fill="#ffffff" font-weight="700">2</text>
    <text x="516" y="100" font-size="13" fill="#1c1c1a" font-weight="700">Indexing parallel _ARR DBIs that don't exist</text>
    <text x="516" y="120" font-size="10.5" fill="#5a5856" font-family="'Fira Code', monospace">arr_status[i] = ANC_PER_ABS_ENTRS_..._CD_ARR</text>
    <line x1="516" y1="135" x2="860" y2="135" stroke="#ede4e0" stroke-width="0.6"/>
    <text x="516" y="155" font-size="11" fill="#5a5856" letter-spacing="0.5" font-weight="600">FIX</text>
    <text x="516" y="172" font-size="11" fill="#0a5a5d">Only entry-id has _ARR. Read scalars inside</text>
    <text x="516" y="186" font-size="11" fill="#0a5a5d" font-family="'Fira Code', monospace">CHANGE_CONTEXTS(ABSENCE_ENTRY_ID = ...)</text>
  </g>

  
  <g filter="url(#apShadow)">
    <rect x="40" y="208" width="410" height="120" rx="6" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="40" y="208" width="34" height="120" rx="6 0 0 6" fill="#c0392b"/>
    <text x="57" y="274" text-anchor="middle" font-size="22" fill="#ffffff" font-weight="700">3</text>
    <text x="86" y="232" font-size="13" fill="#1c1c1a" font-weight="700">Phantom iteration verbs</text>
    <text x="86" y="252" font-size="11.5" fill="#5a5856" font-family="'Fira Code', monospace">i = FIRST_INDEX('N', arr)</text>
    <text x="86" y="266" font-size="11.5" fill="#5a5856" font-family="'Fira Code', monospace">WHILE i WAS NOT DEFAULTED LOOP</text>
    <line x1="86" y1="278" x2="430" y2="278" stroke="#ede4e0" stroke-width="0.6"/>
    <text x="86" y="295" font-size="11" fill="#5a5856" letter-spacing="0.5" font-weight="600">FIX</text>
    <text x="86" y="311" font-size="11.5" fill="#0a5a5d" font-family="'Fira Code', monospace">i = arr.FIRST(-1)</text>
    <text x="86" y="324" font-size="11.5" fill="#0a5a5d" font-family="'Fira Code', monospace">WHILE arr.EXISTS(i) LOOP</text>
  </g>

  
  <g filter="url(#apShadow)">
    <rect x="470" y="208" width="410" height="120" rx="6" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="470" y="208" width="34" height="120" rx="6 0 0 6" fill="#c0392b"/>
    <text x="487" y="274" text-anchor="middle" font-size="22" fill="#ffffff" font-weight="700">4</text>
    <text x="516" y="232" font-size="13" fill="#1c1c1a" font-weight="700">Wrong empty-array constant</text>
    <text x="516" y="252" font-size="11.5" fill="#5a5856" font-family="'Fira Code', monospace">DEFAULT FOR arr IS EMPTY_NUMBER_DATE</text>
    <text x="516" y="268" font-size="10.5" fill="#7a2418" font-style="italic">DATE cannot be an index type</text>
    <line x1="516" y1="278" x2="860" y2="278" stroke="#ede4e0" stroke-width="0.6"/>
    <text x="516" y="295" font-size="11" fill="#5a5856" letter-spacing="0.5" font-weight="600">FIX</text>
    <text x="516" y="311" font-size="11.5" fill="#0a5a5d" font-family="'Fira Code', monospace">EMPTY_DATE_NUMBER</text>
    <text x="516" y="324" font-size="10.5" fill="#0a5a5d" font-style="italic">Format: EMPTY_<data>_<index></text>
  </g>

  
  <g filter="url(#apShadow)">
    <rect x="40" y="340" width="840" height="120" rx="6" fill="#ffffff" stroke="#d4cdc6" stroke-width="0.8"/>
    <rect x="40" y="340" width="34" height="120" rx="6 0 0 6" fill="#c0392b"/>
    <text x="57" y="406" text-anchor="middle" font-size="22" fill="#ffffff" font-weight="700">5</text>
    <text x="86" y="364" font-size="13" fill="#1c1c1a" font-weight="700">Single-column status filter</text>
    <text x="86" y="384" font-size="11.5" fill="#5a5856" font-family="'Fira Code', monospace">IF arr_app_status[i] <> 'ORA_WITHDRAWN' THEN  ← always TRUE, no-op</text>
    <line x1="86" y1="398" x2="860" y2="398" stroke="#ede4e0" stroke-width="0.6"/>
    <text x="86" y="416" font-size="11" fill="#5a5856" letter-spacing="0.5" font-weight="600">FIX</text>
    <text x="86" y="432" font-size="11.5" fill="#0a5a5d" font-family="'Fira Code', monospace">IF abs_status <> 'ORA_WITHDRAWN'</text>
    <text x="280" y="432" font-size="11.5" fill="#0a5a5d" font-family="'Fira Code', monospace">AND app_status <> 'WITHDRAWN'</text>
    <text x="500" y="432" font-size="11.5" fill="#0a5a5d" font-family="'Fira Code', monospace">AND app_status <> 'DENIED' THEN</text>
    <text x="86" y="448" font-size="10.5" fill="#5a5856" font-style="italic">Both columns, both prefix conventions, every time.</text>
  </g>
</svg>
</div>
<p class="am-fig-caption"><strong>Fig 11 —</strong> The five highest-frequency anti-patterns in this domain. Numbers 1, 3, and 4 are syntactic and surface eventually as compile errors or empty results. Numbers 2 and 5 are silent — the formula compiles and runs, returning subtly wrong numbers.</p>
</div>

<hr>

<h2>The 30-Second Checklist</h2>

<p>If your absence formula compiles cleanly but returns the wrong number, walk this checklist in order.</p>

<table>
<thead><tr><th>#</th><th>Check</th><th>Where</th></tr></thead>
<tbody>
<tr><td>1</td><td>Mechanism matches use case (snapshot vs live)</td><td>This post — sections on Mechanism 1 vs 4</td></tr>
<tr><td>2</td><td><code>GET_PLAN_BALANCE</code> called with one argument, not three</td><td>Inside the formula</td></tr>
<tr><td>3</td><td>List-DBI prefix <code>ANC_PER_ABS_ENTRS_</code> · scalar prefix <code>ANC_ABS_ENTRS_</code></td><td>Inside the formula</td></tr>
<tr><td>4</td><td>Iteration uses <code>arr.FIRST(-1)</code> / <code>arr.EXISTS(i)</code> / <code>arr.NEXT(i, -1)</code></td><td>Loop body</td></tr>
<tr><td>5</td><td>Empty-array default uses <code>EMPTY_<data>_<index></code> format</td><td>DEFAULT FOR section</td></tr>
<tr><td>6</td><td>Both <code>ABSENCE_STATUS_CD</code> and <code>APPROVAL_STATUS_CD</code> filtered, with their own prefix conventions</td><td>Filter chain</td></tr>
<tr><td>7</td><td>Self-exclusion guard (<code>l_entry_id <> l_self_entry_id</code>)</td><td>Filter chain — only inside Entry Validation</td></tr>
<tr><td>8</td><td>Snapshot anchor + early-exit guard if performance matters</td><td>Step E and F of the recipe</td></tr>
</tbody>
</table>

<hr>

<h2>Quick Reference Card</h2>

<table>
<thead><tr><th>Function</th><th>Source</th><th>Filter Behaviour</th><th>Use For</th></tr></thead>
<tbody>
<tr><td><code>GET_PLAN_BALANCE</code></td><td>Snapshot ledger</td><td>Only finalised consumption</td><td>Carryover, reporting, snapshot anchor</td></tr>
<tr><td><code>GET_ABSENCE_COUNTS</code></td><td>Live entries</td><td>No filter (MOS 2899647.1)</td><td>"Applied for" occurrence rules</td></tr>
<tr><td><code>GET_ABSENCE_DAYS_PER_TYPE</code></td><td>Live entries</td><td>Hidden internal filter</td><td>Indicative reports only</td></tr>
<tr><td>List-DBI + per-entry scalars</td><td>Live entries</td><td>Filter visible in your formula</td><td>Real-time, audit-grade rules</td></tr>
</tbody>
</table>

<hr>

<h2>Key Takeaways</h2>

<p><strong>Pick the mechanism by use case, not by familiarity.</strong> The default function (<code>GET_PLAN_BALANCE</code>) is right for snapshot questions and wrong for live ones. Reaching for it by reflex is the most common reason Entry Validation rules break in production.</p>

<p><strong>The DBI model is two-step, not parallel arrays.</strong> One list of entry IDs (Step 1), then per-entry scalar reads inside <code>CHANGE_CONTEXTS(ABSENCE_ENTRY_ID = ...)</code> (Step 2). Code written against parallel <code>_ARR</code> siblings does not match the published dictionary — will not compile.</p>

<p><strong>Both status columns, both prefix conventions.</strong> <code>ABSENCE_STATUS_CD</code> uses the <code>ORA_</code> prefix; <code>APPROVAL_STATUS_CD</code> does not. Filter on both, every time, regardless of how confident you are that the entries you care about only ever update one column.</p>

<p><strong>The composite recipe is the production pattern.</strong> Snapshot anchor + early-exit guard + live loop + reconcile. Drop it in, replace the plan name and the input parameters, and you have a balance reader you can defend in audit.</p>

<p>Next in this series: the equivalent function reference for OTL Time Entry Rules — where the live data lives in the <code>HWM_*</code> schema, the available functions are substantially different, and the lifecycle states map onto a different framework altogether.</p>

<div class="am-bio">
<div class="am-bio-avatar">AM</div>
<div>
<div class="am-bio-name">Abhishek Mohanty</div>
<div class="am-bio-role">Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time and Labor, Core HR, Redwood, HDL, OTBI.</div>
</div>
</div>

<div class="am-tags" style="margin-top:18px;">
<span class="am-tag">Fast Formula</span>
<span class="am-tag">Absence Management</span>
<span class="am-tag">GET_PLAN_BALANCE</span>
<span class="am-tag">GET_ABSENCE_COUNTS</span>
<span class="am-tag">CHANGE_CONTEXTS</span>
<span class="am-tag">DBI</span>
<span class="am-tag">Oracle HCM 26A</span>
</div>

</div>