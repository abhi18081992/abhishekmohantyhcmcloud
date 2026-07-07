---
title: "Fast Formula Deep Dive: Contexts, DBIs, Routes & the 7 Building Blocks Oracle Docs Don't Explain Clearly"
pubDate: 2026-03-14
description: "Fast Formula Deep Dive: Contexts, DBIs, Routes & the 7 Building Blocks Oracle Docs Don't Explain Clearly"
tags: ["Fast Formula", "Oracle HCM Cloud"]
author: "Abhishek Mohanty"
draft: false
---

<p> </p><div style="font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;color:#1a1a1a;line-height:1.8;max-width:780px;margin:0 auto;">

<span style="display:inline-block;background:#c0392b;color:#fff;padding:4px 14px;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;border-radius:2px;margin-bottom:6px;margin-right:6px;">Fast Formula</span>

<span style="display:inline-block;background:#2c3e50;color:#fff;padding:4px 14px;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;border-radius:2px;margin-bottom:6px;margin-right:6px;">Fundamentals</span>

<div style="font-size:13px;color:#888;margin-bottom:25px;letter-spacing:0.5px;">March 14, 2026 • 10 min read • Oracle HCM Cloud</div>

<div style="font-size:17px;color:#666;line-height:1.7;margin-bottom:30px;font-style:italic;border-left:4px solid #c0392b;padding-left:18px;">

If you've ever tried to write a Fast Formula and wondered what the difference is between a Context, an Input Value, and a Database Item — this post is for you. Let's break down the 7 core building blocks that every FF developer needs to understand before writing a single line of formula code.

</div>

<div style="display:flex;align-items:center;gap:14px;padding:20px 0;border-top:2px solid #1a1a1a;border-bottom:2px solid #1a1a1a;margin-bottom:35px;">

<div style="width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#c0392b,#e67e22);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px;flex-shrink:0;">AM</div>

<div>

<div style="font-weight:700;font-size:15px;">Abhishek Mohanty</div>

<div style="font-size:13px;color:#888;">Oracle HCM Cloud Consultant & Technical Lead</div>

</div>

</div>

<!-- ==================== INTRO ==================== -->

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">Before you can write production-ready Fast Formulas in Oracle Fusion HCM Cloud, you need to understand the building blocks that the formula engine relies on. These aren't just theoretical concepts — every compilation error, every runtime failure, and every unexpected result traces back to one of these components being misunderstood or misused.</p>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">In this post, I'll walk through the <b>7 default components of Oracle Fast Formula</b> — what they are, how they relate to each other, and the practical details that Oracle docs don't always make obvious.</p>

<hr style="border:none;border-top:1px solid #e0dcd6;margin:35px 0;"/>

<!-- ==================== 1. FORMULA TYPE ==================== -->

<div style="font-size:24px;font-weight:700;color:#1a1a1a;margin:40px 0 18px;padding-left:16px;border-left:4px solid #c0392b;line-height:1.3;">1. Formula Type</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">Every Fast Formula belongs to a <b>Formula Type</b>. Think of it as the category or classification of the formula. You simply cannot create a formula without selecting a type first — the editor won't let you.</p>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">But formula type isn't just an administrative label. It determines everything downstream:</p>

<p style="font-size:15px;color:#2a2a2a;line-height:1.65;padding-left:10px;">🔹 Which <b>Contexts</b> are available to the formula<br/>🔹 Which <b>Input Values</b> the engine will pass in<br/>🔹 Which <b>Database Items</b> you can reference<br/>🔹 Where in the product the formula can be <b>attached</b></p>

<div style="display:flex;gap:14px;background:#fff;border:1px solid #e0dcd6;border-radius:6px;padding:22px;margin:24px 0;align-items:flex-start;">

<div style="font-size:22px;flex-shrink:0;">⚠️</div>

<div>

<div style="font-size:15px;font-weight:700;margin:0 0 6px;">Common Mistake</div>

<div style="font-size:14px;color:#666;margin:0;line-height:1.6;">A frequent beginner error is creating a formula under the wrong type. For example, creating a formula with the <b>Compensation Default and Override Rule</b> type and then expecting to attach it to a Total Compensation Item — it won't show up. The field that uses the formula restricts selection based on type. Always know your type before you start coding.</div>

</div>

</div>

<hr style="border:none;border-top:1px solid #e0dcd6;margin:35px 0;"/>

<!-- ==================== 2. CONTEXT ==================== -->

<div style="font-size:24px;font-weight:700;color:#1a1a1a;margin:40px 0 18px;padding-left:16px;border-left:4px solid #c0392b;line-height:1.3;">2. Context</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">A Context is a <b>predefined parameter value</b> passed to the formula by the engine at runtime. You don't define contexts — Oracle does. They are tied to the formula type itself.</p>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">When Oracle created each formula type, they also defined which contexts would be available. So if you know the formula type, you automatically know what context parameters you'll receive.</p>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">Common contexts include:</p>

<table style="width:100%;border-collapse:collapse;font-size:14px;margin:20px 0;">

<tr><th style="background:#2d2926;color:#f5ebe0;padding:12px 16px;text-align:left;">Context</th><th style="background:#2d2926;color:#f5ebe0;padding:12px 16px;text-align:left;">What It Provides</th></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;"><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">PERSON_ID</code></td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Identifies which person the formula is processing</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;"><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">HR_ASSIGNMENT_ID</code></td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Identifies the specific assignment record</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;"><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">EFFECTIVE_DATE</code></td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">The date for which the formula runs</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;"><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">LEGAL_ENTITY_ID</code></td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">The legal entity associated with the assignment</td></tr>

</table>

<div style="margin:28px 0;padding:22px 25px 22px 28px;background:#fdf6f0;border-left:5px solid #c0392b;font-size:17px;font-style:italic;color:#333;line-height:1.7;">

The critical role of Context: it determines the "who" and "when" of your formula. When a Database Item like PER_ASG_REL_ORIGINAL_DATE_OF_HIRE returns a hire date, how does it know whose hire date? The Context (PERSON_ID / HR_ASSIGNMENT_ID) tells it.

</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">You retrieve context values in your formula using the <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">GET_CONTEXT()</code> function:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px">l_person_id = <span style="color:#6cacec;">GET_CONTEXT</span>(PERSON_ID, 0)

l_assignment_id = <span style="color:#6cacec;">GET_CONTEXT</span>(HR_ASSIGNMENT_ID, 0)</pre>

<hr style="border:none;border-top:1px solid #e0dcd6;margin:35px 0;"/>

<!-- ==================== 3. INPUT VALUES ==================== -->

<div style="font-size:24px;font-weight:700;color:#1a1a1a;margin:40px 0 18px;padding-left:16px;border-left:4px solid #c0392b;line-height:1.3;">3. Input Values</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">Input Values are also parameters passed to the formula — but there's a key difference from Contexts. <b>Input Values are not predefined by Oracle.</b> They represent additional information that the developer (or the calling process) decides to pass into the formula at execution time.</p>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">Because they're not predefined in Oracle's metadata tables, you won't find them by querying the database. The <b>only way to know what Input Values are available</b> for a given formula type is to read the Oracle documentation — specifically the Fast Formula Reference Guide.</p>

<div style="display:flex;gap:14px;background:#fff;border:1px solid #e0dcd6;border-radius:6px;padding:22px;margin:24px 0;align-items:flex-start;">

<div style="font-size:22px;flex-shrink:0;">📖</div>

<div>

<div style="font-size:15px;font-weight:700;margin:0 0 6px;">Context vs Input Value — What's the Difference?</div>

<div style="font-size:14px;color:#666;margin:0;line-height:1.6;"><b>Context:</b> Predefined by Oracle with the formula type. Available in metadata. Determines which Database Items work.<br/><b>Input Value:</b> Defined by the developer or calling process. Not in metadata. Additional info passed at runtime. Must read the docs to know what's available.</div>

</div>

</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">Input values are declared in your formula with the <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">INPUTS ARE</code> statement and always prefixed with <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">IV_</code>:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#e67e22;">INPUTS ARE</span>

  IV_ACCRUAL,

  IV_ACCRUALPERIODSTARTDATE  (<span style="color:#e67e22;">DATE</span>),

  IV_ACCRUALPERIODENDDATE    (<span style="color:#e67e22;">DATE</span>)</pre>

<hr style="border:none;border-top:1px solid #e0dcd6;margin:35px 0;"/>

<!-- ==================== 4. DATABASE ITEMS ==================== -->

<div style="font-size:24px;font-weight:700;color:#1a1a1a;margin:40px 0 18px;padding-left:16px;border-left:4px solid #c0392b;line-height:1.3;">4. Database Items (DBIs)</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">Database Items are essentially <b>predefined variables that hold values from HR tables</b>. Think of them as Oracle's way of giving your formula read access to employee data without writing SQL.</p>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">Each DBI holds one type of value. For example:</p>

<table style="width:100%;border-collapse:collapse;font-size:14px;margin:20px 0;">

<tr><th style="background:#2d2926;color:#f5ebe0;padding:12px 16px;text-align:left;">Database Item</th><th style="background:#2d2926;color:#f5ebe0;padding:12px 16px;text-align:left;">What It Returns</th></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;"><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">PER_PER_FIRST_NAME</code></td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Person's first name</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;"><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">PER_PER_LAST_NAME</code></td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Person's last name</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;"><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">PER_ASG_REL_ORIGINAL_DATE_OF_HIRE</code></td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Original hire date</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;"><code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">PER_ASG_STATUS_USER_STATUS</code></td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Assignment status (e.g. 'ACTIVE')</td></tr>

</table>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;"><b>Two types of Database Items exist:</b></p>

<p style="font-size:15px;color:#2a2a2a;line-height:1.65;padding-left:10px;">🔹 <b>Single-value DBIs</b> — return one value (e.g., a person's first name)<br/>🔹 <b>Range (array) DBIs</b> — return multiple values of the same type (e.g., a list of element entries)</p>

<div style="margin:28px 0;padding:22px 25px 22px 28px;background:#fdf6f0;border-left:5px solid #c0392b;font-size:17px;font-style:italic;color:#333;line-height:1.7;">

Key concept: The value a DBI returns is determined by the Context. If the context passes PERSON_ID = 12345, then PER_PER_FIRST_NAME returns the first name of person 12345. Without context, the DBI has no idea whose data to fetch.

</div>

<hr style="border:none;border-top:1px solid #e0dcd6;margin:35px 0;"/>

<!-- ==================== 5. ROUTES ==================== -->

<div style="font-size:24px;font-weight:700;color:#1a1a1a;margin:40px 0 18px;padding-left:16px;border-left:4px solid #c0392b;line-height:1.3;">5. Routes</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">Routes are the <b>source behind Database Items</b>. If a DBI is the variable, the Route is the SQL query that populates it. Think of it as the table or SELECT statement that tells the engine where to fetch the data from.</p>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">Here's how Routes, Contexts, and DBIs connect:</p>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#6b8e6b;font-style:italic;">/* Conceptually, this is what happens behind the scenes: */</span>

<span style="color:#6cacec;">Database Item:</span>  PER_PER_FIRST_NAME

<span style="color:#6cacec;">Route (Source):</span> PER_PERSONS table

<span style="color:#6cacec;">Context (WHERE):</span> WHERE person_id = <span style="color:#e67e22;">CONTEXT(PERSON_ID)</span>

<span style="color:#6b8e6b;font-style:italic;">/* The context acts as the WHERE clause that restricts

   which row the route (table) returns data from */</span></pre>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">You'll never need to define routes yourself — they're part of Oracle's internal metadata. But understanding that they exist helps you debug when a DBI returns unexpected data. If a DBI isn't returning what you expect, it's usually because the context isn't set correctly, which means the route is querying the wrong row.</p>

<hr style="border:none;border-top:1px solid #e0dcd6;margin:35px 0;"/>

<!-- ==================== 6. FUNCTIONS ==================== -->

<div style="font-size:24px;font-weight:700;color:#1a1a1a;margin:40px 0 18px;padding-left:16px;border-left:4px solid #c0392b;line-height:1.3;">6. Functions</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">Functions in Fast Formula come in <b>two categories</b>:</p>

<p style="font-size:15px;color:#2a2a2a;line-height:1.65;padding-left:10px;">🟢 <b>Seeded (Oracle-provided) functions</b> — built-in functions you can use directly. These include TO_CHAR, TO_NUMBER, TO_DATE, ADD_MONTHS, MONTHS_BETWEEN, DAYS_BETWEEN, ESS_LOG_WRITE, GET_CONTEXT, and many more.<br/><br/>🔴 <b>Custom (user-defined) functions</b> — in the E-Business Suite (EBS) on-premise world, customers could create their own functions by accessing the function definition tables and linking PL/SQL code. <b>This is NOT available in Oracle Cloud.</b></p>

<div style="display:flex;gap:14px;background:#fff;border:1px solid #e0dcd6;border-radius:6px;padding:22px;margin:24px 0;align-items:flex-start;">

<div style="font-size:22px;flex-shrink:0;">☁️</div>

<div>

<div style="font-size:15px;font-weight:700;margin:0 0 6px;">Cloud Limitation</div>

<div style="font-size:14px;color:#666;margin:0;line-height:1.6;">In Oracle Fusion Cloud, you <b>cannot create custom functions</b> because you don't have direct database access. You can only use the seeded functions that Oracle provides. This is a major difference from EBS and on-premise deployments where customers had the ability to create and register their own functions.</div>

</div>

</div>

<hr style="border:none;border-top:1px solid #e0dcd6;margin:35px 0;"/>

<!-- ==================== 7. VARIABLES ==================== --><div style="font-size:24px;font-weight:700;color:#1a1a1a;margin:40px 0 18px;padding-left:16px;border-left:4px solid #c0392b;line-height:1.3;">7. Return Variables</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">The final component is the <b>Return Variable</b> — the value(s) your formula sends back to the calling process. This is where many beginners get tripped up, because the rules around return variables are inconsistent across formula types.</p>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">There are <b>three patterns</b> for how return variables work:</p>

<!-- Pattern 1 -->

<div style="background:#fff;border:1px solid #e0dcd6;border-radius:6px;padding:22px;margin:16px 0;">

<div style="font-size:15px;font-weight:700;margin:0 0 8px;color:#c0392b;">Pattern 1: Variable Name Doesn't Matter</div>

<div style="font-size:14px;color:#555;line-height:1.6;">When the formula returns a single character value (like 'Y' or 'N'), most calling processes don't care what you name the variable. They just grab whatever character value comes back. You could name it <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">RETVAL</code>, <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">RESULT</code>, or anything — it works.</div>

</div>

<!-- Pattern 2 -->

<div style="background:#fff;border:1px solid #e0dcd6;border-radius:6px;padding:22px;margin:16px 0;">

<div style="font-size:15px;font-weight:700;margin:0 0 8px;color:#c0392b;">Pattern 2: Variable Name Is Critical</div>

<div style="font-size:14px;color:#555;line-height:1.6;">Some formula types require a <b>specific variable name</b>. The classic example is the <b>Benefits Eligibility</b> formula — the return variable <i>must</i> be called <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">ELIGIBLE</code> (in capitals). If you return the right value ('Y' or 'N') but in a differently-named variable, the engine either throws an error or falls back to default behavior.</div>

</div>

<!-- Pattern 3 -->

<div style="background:#fff;border:1px solid #e0dcd6;border-radius:6px;padding:22px;margin:16px 0;">

<div style="font-size:15px;font-weight:700;margin:0 0 8px;color:#c0392b;">Pattern 3: Multiple Named Return Variables</div>

<div style="font-size:14px;color:#555;line-height:1.6;">When returning multiple values (e.g., in a Total Compensation Item formula), each value has a <b>specific variable name</b> — one for date, one for value, one for assignment ID, one for legal employer, etc. The order doesn't matter, but the names do. The engine maps return values by variable name, not position.</div>

</div>

<pre style="background:#2d2926;border-left:3px solid #c0392b;padding:18px 22px;margin:22px 0;font-family:Consolas,'JetBrains Mono',Monaco,monospace;font-size:13.5px;color:#e8e6e3;line-height:1.7;overflow-x:auto;white-space:pre-wrap;border-radius:4px"><span style="color:#6b8e6b;font-style:italic;">/* Pattern 1: Name doesn't matter */</span>

RETVAL = <span style="color:#8bc48b;">'Y'</span>

<span style="color:#e67e22;">RETURN</span> RETVAL

<span style="color:#6b8e6b;font-style:italic;">/* Pattern 2: Name MUST be 'ELIGIBLE' */</span>

ELIGIBLE = <span style="color:#8bc48b;">'Y'</span>

<span style="color:#e67e22;">RETURN</span> ELIGIBLE

<span style="color:#6b8e6b;font-style:italic;">/* Pattern 3: Multiple named variables */</span>

COMPENSATION_DATES = <span style="color:#8bc48b;">'2026/01/31'</span>

VALUES = <span style="color:#8bc48b;">'50000'</span>

LEGALEMPLOYERS = <span style="color:#8bc48b;">'301'</span>

ASSIGNMENTS = <span style="color:#8bc48b;">'12345'</span>

<span style="color:#e67e22;">RETURN</span> COMPENSATION_DATES, VALUES, LEGALEMPLOYERS, ASSIGNMENTS</pre>

<div style="display:flex;gap:14px;background:#fff;border:1px solid #e0dcd6;border-radius:6px;padding:22px;margin:24px 0;align-items:flex-start;">

<div style="font-size:22px;flex-shrink:0;">📖</div>

<div>

<div style="font-size:15px;font-weight:700;margin:0 0 6px;">Where to Find This Information</div>

<div style="font-size:14px;color:#666;margin:0;line-height:1.6;">The FF engine doesn't enforce variable names — the <b>calling product</b> does. So the docs for each product (Benefits, Compensation, Absence, etc.) tell you what variable names they expect. Always check the <b>Oracle Fast Formula Reference Guide</b> for your specific formula type.</div>

</div>

</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">One more thing on return values: even when the variable name doesn't matter, the <b>format often does</b>. Most products expect dates in <code style="background:#3a352f;color:#e8944f;padding:2px 7px;border-radius:3px;font-size:13px;font-family:Consolas,'JetBrains Mono',monospace">YYYY/MM/DD</code> format. Always check the docs for the expected format of each return value.</p>

<hr style="border:none;border-top:1px solid #e0dcd6;margin:35px 0;"/>

<!-- ==================== BONUS: USER ENTITIES ==================== -->

<div style="font-size:24px;font-weight:700;color:#1a1a1a;margin:40px 0 18px;padding-left:16px;border-left:4px solid #c0392b;line-height:1.3;">Bonus: User Entities</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">User Entities are a grouping mechanism for Database Items, primarily used in <b>HCM Extract</b> formulas. They bundle related DBIs together for extract operations. For most FF developers working on absence, compensation, or payroll formulas, you won't interact with User Entities directly — but it's worth knowing they exist as part of the component architecture.</p>

<hr style="border:none;border-top:1px solid #e0dcd6;margin:35px 0;"/>

<hr style="border:none;border-top:1px solid #e0dcd6;margin:35px 0;"/>

<!-- ==================== WORKFLOW DIAGRAM ==================== -->

<div style="font-size:24px;font-weight:700;color:#1a1a1a;margin:40px 0 18px;padding-left:16px;border-left:4px solid #c0392b;line-height:1.3;">Putting It All Together</div>

<p style="font-size:16px;margin-bottom:24px;color:#2a2a2a;">Here's how all 7 components connect in the Fast Formula engine:</p>

<div style="background:#1e1e1e;border-radius:10px;padding:30px 28px;margin:20px 0;color:#f5ebe0;font-family:'Segoe UI',Tahoma,sans-serif;">

<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px;">

<span style="background:#c0392b;color:#fff;padding:6px 14px;border-radius:4px;font-size:13px;font-weight:700;letter-spacing:0.5px;">FORMULA TYPE</span>

<span style="color:#888;font-size:13px;">determines</span>

<span style="color:#555;font-size:16px;">▶</span>

<span style="background:#e67e22;color:#fff;padding:6px 14px;border-radius:4px;font-size:13px;font-weight:700;letter-spacing:0.5px;">CONTEXTS</span>

<span style="color:#888;font-size:13px;">available</span>

</div>

<div style="margin-left:56px;padding:4px 0;">

<div style="width:2px;height:18px;background:#444;margin-left:50px;"></div>

</div>

<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px;margin-left:56px;">

<span style="background:#e67e22;color:#fff;padding:6px 14px;border-radius:4px;font-size:13px;font-weight:700;letter-spacing:0.5px;">CONTEXTS</span>

<span style="color:#888;font-size:13px;">act as WHERE clause for</span>

<span style="color:#555;font-size:16px;">▶</span>

<span style="background:#27ae60;color:#fff;padding:6px 14px;border-radius:4px;font-size:13px;font-weight:700;letter-spacing:0.5px;">ROUTES</span>

</div>

<div style="margin-left:56px;padding:4px 0;">

<div style="width:2px;height:18px;background:#444;margin-left:50px;"></div>

</div>

<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px;margin-left:56px;">

<span style="background:#27ae60;color:#fff;padding:6px 14px;border-radius:4px;font-size:13px;font-weight:700;letter-spacing:0.5px;">ROUTES</span>

<span style="color:#888;font-size:13px;">return data into</span>

<span style="color:#555;font-size:16px;">▶</span>

<span style="background:#2980b9;color:#fff;padding:6px 14px;border-radius:4px;font-size:13px;font-weight:700;letter-spacing:0.5px;">DATABASE ITEMS</span>

</div>

<div style="border-top:1px dashed #333;margin:20px 0;"></div>

<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:16px;">

<span style="background:#8e44ad;color:#fff;padding:6px 14px;border-radius:4px;font-size:13px;font-weight:700;letter-spacing:0.5px;">INPUT VALUES</span>

<span style="color:#555;font-size:16px;">◀</span>

<span style="color:#888;font-size:13px;">additional params from the calling process</span>

</div>

<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:16px;">

<span style="background:#2c3e50;color:#fff;padding:6px 14px;border-radius:4px;font-size:13px;font-weight:700;letter-spacing:0.5px;">FUNCTIONS</span>

<span style="color:#555;font-size:16px;">◀</span>

<span style="color:#888;font-size:13px;">built-in operations (TO_CHAR, DAYS_BETWEEN, etc.)</span>

</div>

<div style="border-top:1px dashed #333;margin:20px 0;"></div>

<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">

<span style="color:#aaa;font-size:13px;">Your formula logic</span>

<span style="color:#555;font-size:16px;">▶</span>

<span style="background:#c0392b;color:#fff;padding:6px 14px;border-radius:4px;font-size:13px;font-weight:700;letter-spacing:0.5px;">RETURN VARIABLES</span>

<span style="color:#888;font-size:13px;">(output)</span>

</div>

</div>

<!-- SUMMARY TABLE -->

<table style="width:100%;border-collapse:collapse;font-size:14px;margin:24px 0;">

<tr><th style="background:#2d2926;color:#f5ebe0;padding:12px 16px;text-align:left;">Component</th><th style="background:#2d2926;color:#f5ebe0;padding:12px 16px;text-align:left;">Predefined?</th><th style="background:#2d2926;color:#f5ebe0;padding:12px 16px;text-align:left;">Where to Find Info</th></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;font-weight:700;">Formula Type</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Yes, by Oracle</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Formula editor dropdown</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;font-weight:700;">Contexts</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Yes, tied to type</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Oracle metadata / docs</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;font-weight:700;">Input Values</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">No, developer-defined</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">FF Reference Guide only</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;font-weight:700;">Database Items</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Yes, by Oracle</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">DBI lookup in formula editor</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;font-weight:700;">Routes</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Yes, internal</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Not user-facing</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;font-weight:700;">Functions</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Yes (Cloud: seeded only)</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">FF Reference Guide</td></tr>

<tr><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;font-weight:700;">Return Variables</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Depends on type</td><td style="padding:10px 16px;border-bottom:1px solid #e0dcd6;">Product-specific docs</td></tr>

</table>

<hr style="border:none;border-top:1px solid #e0dcd6;margin:35px 0;"/>

<!-- ==================== KEY TAKEAWAYS ==================== -->

<div style="font-size:24px;font-weight:700;color:#1a1a1a;margin:40px 0 18px;padding-left:16px;border-left:4px solid #c0392b;line-height:1.3;">Key Takeaways</div>

<p style="font-size:16px;margin-bottom:22px;color:#2a2a2a;">Understanding these 7 components before writing your first line of formula code will save you hours of debugging. The most common FF issues — compilation errors, missing data, wrong return values — almost always trace back to one of these being misunderstood.</p>

<div style="border:1px solid #e0dcd6;border-radius:8px;overflow:hidden;margin:24px 0;">

<div style="background:#2d2926;padding:14px 20px;">

<div style="font-size:14px;font-weight:700;color:#f5ebe0;letter-spacing:1px;text-transform:uppercase;">Recommendations for FF Beginners</div>

</div>

<div style="padding:0;">

<div style="display:flex;align-items:flex-start;gap:14px;padding:16px 20px;border-bottom:1px solid #f0ece6;">

<div style="width:28px;height:28px;border-radius:50%;background:#c0392b;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:12px;flex-shrink:0;">1</div>

<div style="font-size:15px;color:#2a2a2a;line-height:1.55;padding-top:3px;"><b>Always identify your Formula Type first</b> — everything else flows from it</div>

</div>

<div style="display:flex;align-items:flex-start;gap:14px;padding:16px 20px;border-bottom:1px solid #f0ece6;">

<div style="width:28px;height:28px;border-radius:50%;background:#c0392b;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:12px;flex-shrink:0;">2</div>

<div style="font-size:15px;color:#2a2a2a;line-height:1.55;padding-top:3px;"><b>Read the FF Reference Guide</b> for your formula type before coding — it tells you available contexts, input values, and expected return variables</div>

</div>

<div style="display:flex;align-items:flex-start;gap:14px;padding:16px 20px;border-bottom:1px solid #f0ece6;">

<div style="width:28px;height:28px;border-radius:50%;background:#c0392b;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:12px;flex-shrink:0;">3</div>

<div style="font-size:15px;color:#2a2a2a;line-height:1.55;padding-top:3px;"><b>DEFAULT every DBI and Input Value</b> — no nulls in FF, missing defaults cause hard runtime errors</div>

</div>

<div style="display:flex;align-items:flex-start;gap:14px;padding:16px 20px;border-bottom:1px solid #f0ece6;">

<div style="width:28px;height:28px;border-radius:50%;background:#c0392b;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:12px;flex-shrink:0;">4</div>

<div style="font-size:15px;color:#2a2a2a;line-height:1.55;padding-top:3px;"><b>Check exact return variable names</b> — some are strict (ELIGIBLE for Benefits), others are flexible</div>

</div>

<div style="display:flex;align-items:flex-start;gap:14px;padding:16px 20px;">

<div style="width:28px;height:28px;border-radius:50%;background:#c0392b;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:12px;flex-shrink:0;">5</div>

<div style="font-size:15px;color:#2a2a2a;line-height:1.55;padding-top:3px;"><b>No custom functions in Cloud</b> — plan your logic using seeded functions only (unlike EBS where you could register PL/SQL)</div>

</div>

</div>

</div>

<p style="font-size:16px;margin-bottom:18px;color:#2a2a2a;">In the next post, we'll dive deeper into the formula syntax and walk through a real formula line by line. Stay tuned.</p>


<!-- ==================== FOOTER ==================== -->

<div style="display:flex;align-items:center;gap:16px;padding-top:25px;border-top:2px solid #1a1a1a;margin-top:40px;">

<div style="width:65px;height:65px;border-radius:50%;background:linear-gradient(135deg,#c0392b,#e67e22);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:22px;flex-shrink:0;">AM</div>

<div>

<div style="font-size:18px;font-weight:700;">Abhishek Mohanty</div>

<div style="font-size:14px;color:#666;line-height:1.6;">Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Core HR, Redwood, HDL, OTBI.</div>

</div>

</div>

</div>