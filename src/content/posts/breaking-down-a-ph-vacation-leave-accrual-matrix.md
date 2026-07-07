---
title: "Breaking Down a PH Vacation Leave Accrual Matrix Formula — Section by Section"
pubDate: 2026-03-14
description: "Breaking Down a PH Vacation Leave Accrual Matrix Formula — Section by Section"
tags: ["Absence Management", "Fast Formula", "Oracle HCM Cloud"]
author: "Abhishek Mohanty"
draft: false
---

<p> </p><!-- 
BLOGGER PASTE-READY VERSION
============================
Post Title: Breaking Down a PH Vacation Leave Accrual Matrix Formula — Section by Section
Labels: Oracle HCM, Fast Formula, Absence Management, Oracle Cloud, Accrual

Instructions: 
1. In Blogger, click + New Post
2. Enter the title above
3. Switch to HTML view (pencil icon → HTML)
4. Copy everything below and paste
5. Add labels, then Publish
-->

<style>
.am-blog{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;color:#1a1a1a;line-height:1.8;max-width:780px;margin:0 auto}
.am-blog p{font-size:16px;margin-bottom:18px;color:#2a2a2a}
.am-tag{display:inline-block;background:#c0392b;color:#fff;padding:4px 14px;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;border-radius:2px;margin-bottom:6px;margin-right:6px}
.am-tag.blue{background:#2c3e50}
.am-meta{font-size:13px;color:#888;margin-bottom:25px;letter-spacing:0.5px}
.am-intro{font-size:17px;color:#666;line-height:1.7;margin-bottom:30px;font-style:italic;border-left:4px solid #c0392b;padding-left:18px}
.am-author-box{display:flex;align-items:center;gap:14px;padding:20px 0;border-top:2px solid #1a1a1a;border-bottom:2px solid #1a1a1a;margin-bottom:35px}
.am-avatar{width:50px;height:50px;border-radius:50%;background:linear-gradient(135deg,#c0392b,#e67e22);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px;flex-shrink:0}
.am-author-name{font-weight:700;font-size:15px}
.am-author-role{font-size:13px;color:#888}
.am-h2{font-size:24px;font-weight:700;color:#1a1a1a;margin:40px 0 18px;padding-left:16px;border-left:4px solid #c0392b;line-height:1.3}
.am-h3{font-size:19px;font-weight:700;color:#1a1a1a;margin:28px 0 12px}
.am-hr{border:none;border-top:1px solid #e0dcd6;margin:35px 0}
.am-code{background:#2d2926;border-radius:6px;padding:20px 24px;margin:20px 0;font-family:'Courier New',Consolas,monospace;font-size:13px;color:#f5ebe0;line-height:1.7;overflow-x:auto;white-space:pre-wrap;word-wrap:break-word}
.am-code .cm{color:#6b8e6b;font-style:italic}
.am-code .kw{color:#e67e22}
.am-code .str{color:#8bc48b}
.am-code .fn{color:#6cacec}
.am-inline-code{background:#f0ece6;padding:2px 7px;border-radius:3px;font-family:'Courier New',Consolas,monospace;font-size:14px;color:#c0392b}
.am-callout{display:flex;gap:14px;background:#fff;border:1px solid #e0dcd6;border-radius:6px;padding:22px;margin:24px 0;align-items:flex-start}
.am-callout-icon{font-size:22px;flex-shrink:0}
.am-callout h4{font-size:15px;font-weight:700;margin:0 0 6px}
.am-callout p{font-size:14px;color:#666;margin:0;line-height:1.6}
.am-pullquote{margin:28px 0;padding:22px 25px 22px 28px;background:#fdf6f0;border-left:5px solid #c0392b;font-size:17px;font-style:italic;color:#333;line-height:1.7}
.am-table-wrap{overflow-x:auto;margin:20px 0}
.am-table{width:100%;border-collapse:collapse;font-size:14px}
.am-table th{background:#2d2926;color:#f5ebe0;padding:12px 16px;text-align:left;font-weight:600;font-size:13px;letter-spacing:0.5px;text-transform:uppercase}
.am-table td{padding:10px 16px;border-bottom:1px solid #e0dcd6;color:#333;vertical-align:top}
.am-table tr:hover td{background:#fdf6f0}
.am-table code{background:#f0ece6;padding:1px 5px;border-radius:3px;font-family:'Courier New',monospace;font-size:13px;color:#c0392b}
.am-list{margin:16px 0;padding-left:0;list-style:none}
.am-list li{position:relative;padding-left:22px;margin-bottom:10px;font-size:15px;color:#2a2a2a;line-height:1.65}
.am-list li::before{content:'';position:absolute;left:0;top:8px;width:8px;height:8px;background:#c0392b;border-radius:50%}
.am-syntax-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:20px 0}
.am-syntax-card{background:#fff;border:1px solid #e0dcd6;padding:16px;border-radius:6px;font-size:14px}
.am-syntax-card strong{display:block;margin-bottom:4px;color:#c0392b;font-size:13px;text-transform:uppercase;letter-spacing:0.5px}
.am-syntax-card p{margin:0;color:#555;line-height:1.55;font-size:13.5px}
.am-phase-badge{display:inline-block;background:#c0392b;color:#fff;padding:3px 12px;border-radius:3px;font-size:12px;font-weight:700;letter-spacing:1px;margin-bottom:10px}
.am-phase-badge.bridge{background:#e67e22}
.am-phase-badge.lump{background:#27ae60}
.am-phase-badge.done{background:#7f8c8d}
.am-footer-box{display:flex;align-items:center;gap:16px;padding-top:25px;border-top:2px solid #1a1a1a;margin-top:40px}
.am-footer-avatar{width:65px;height:65px;border-radius:50%;background:linear-gradient(135deg,#c0392b,#e67e22);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:22px;flex-shrink:0}
.am-footer-name{font-size:18px;font-weight:700}
.am-footer-bio{font-size:14px;color:#666;line-height:1.6}
@media(max-width:600px){
.am-author-box,.am-footer-box{flex-direction:column;text-align:center}
.am-syntax-grid{grid-template-columns:1fr}
.am-code{font-size:12px;padding:14px 16px}
}
</style>

<div class="am-blog">

<span class="am-tag">Fast Formula</span>
<span class="am-tag blue">Absence Management</span>
<div class="am-meta">March 14, 2026  •  15 min read  •  Oracle HCM Cloud</div>

<div class="am-intro">
My first blog post so bear with me. I wanted to write this because when I started learning Fast Formula I couldn't find anyone explaining the actual concepts behind each block. So here we go.
</div>

<div class="am-author-box">
<div class="am-avatar">AM</div>
<div>
<div class="am-author-name">Abhishek Mohanty</div>
<div class="am-author-role">Oracle HCM Cloud Consultant & Technical Lead</div>
</div>
</div>

<!-- ==================== SECTION: WHAT IS IT ==================== -->

<div class="am-h2">What Even Is an Accrual Matrix Formula?</div>

<p>Before jumping into the code, quick context. In Oracle Absence Management there are different formula types. This one is <b>Absence Accrual Matrix Formula</b>. What that means is — the absence plan already has a matrix table configured (like a grid with bands based on years of service or grade etc), and the matrix engine calculates an accrual value and passes it to this formula as <span class="am-inline-code">IV_ACCRUAL</span>.</p>

<p>The formula's job is to either accept that value or override it. In our case we're completely ignoring <span class="am-inline-code">IV_ACCRUAL</span> and doing our own calculation. That's the whole point of a matrix formula — you get a hook to intercept and customize.</p>

<p>This specific formula implements <b>Philippine vacation leave rules</b>:</p>

<ul class="am-list">
<li><b>0 to 6 months</b> — nothing (probation)</li>
<li><b>6 to 12 months</b> — 1.25 days per month</li>
<li><b>After 12 months</b> — one-time 15 day credit in January, then nothing after</li>
</ul>

<p>OK let's get into it.</p>

<hr class="am-hr"/>

<!-- ==================== SECTION: HEADER ==================== -->

<div class="am-h2">The Header Block</div>

<div class="am-code"><span class="cm">/*************************************************************
FORMULA NAME: PH_VACATION_LEAVE_ACCRUAL_MATRIX
FORMULA TYPE: Absence Accrual Matrix Formula
DESCRIPTION: Philippine Vacation Leave Accrual Matrix Formula
- First 6 months (probation): No accrual
- Month 6 to 12: Accrue 1.25 days per month
- Post regularization (12 months), from subsequent
January: 15 days credited ONE TIME only
- If regularized in January, credit that same January
- After the one-time credit, no further accrual

VERSION: 13.2

REFERENCE: Oracle HCM Cloud Absence Management
Fast Formula Reference Guide (pages 15-19)
This formula overrides IV_ACCRUAL from the matrix
engine with custom phase-based calculation.
RETURN accrual matches Oracle sample on page 19.

HR_ASSIGNMENT_ID is a context, so PER_ASG_ DBIs
work directly without array loops.

MUST be paired with MONTHLY processing frequency.
*************************************************************/</span></div>

<p>This is just a comment block but don't skip it. It tells you the formula type (which determines available inputs and returns), the business rules, the Oracle doc reference, and the processing frequency requirement. The note about monthly frequency is important — the formula has a guard for this later.</p>

<hr class="am-hr"/>

<!-- ==================== SECTION: DEFAULTS ==================== -->

<div class="am-h2">DEFAULT Statements — Why They Exist in FF</div>

<div class="am-code"><span class="cm">/* DBI defaults - HR_ASSIGNMENT_ID context available */</span>
<span class="kw">DEFAULT FOR</span> PER_ASG_REL_ORIGINAL_DATE_OF_HIRE <span class="kw">IS</span> <span class="str">'4712/12/31 00:00:00'</span> (date)
<span class="kw">DEFAULT FOR</span> PER_ASG_REL_ACTUAL_TERMINATION_DATE <span class="kw">IS</span> <span class="str">'4712/12/31 00:00:00'</span> (date)
<span class="kw">DEFAULT FOR</span> PER_ASG_STATUS_USER_STATUS <span class="kw">IS</span> <span class="str">'NA'</span>
<span class="kw">DEFAULT FOR</span> PER_ASG_FTE_VALUE <span class="kw">IS</span> 1
<span class="kw">DEFAULT FOR</span> ANC_ABS_PLN_NAME <span class="kw">IS</span> <span class="str">'NA'</span>

<span class="cm">/* Input value defaults per Oracle doc page 16-17 */</span>
<span class="kw">DEFAULT FOR</span> IV_ACCRUAL <span class="kw">IS</span> 0
<span class="kw">DEFAULT FOR</span> IV_CARRYOVER <span class="kw">IS</span> 0
<span class="kw">DEFAULT FOR</span> IV_CEILING <span class="kw">IS</span> 0
<span class="kw">DEFAULT FOR</span> IV_ACCRUAL_CEILING <span class="kw">IS</span> 0
<span class="kw">DEFAULT FOR</span> IV_ACCRUALPERIODSTARTDATE <span class="kw">IS</span> <span class="str">'4712/12/31 00:00:00'</span> (date)
<span class="kw">DEFAULT FOR</span> IV_ACCRUALPERIODENDDATE <span class="kw">IS</span> <span class="str">'4712/12/31 00:00:00'</span> (date)
<span class="kw">DEFAULT FOR</span> IV_CALENDARSTARTDATE <span class="kw">IS</span> <span class="str">'4712/12/31 00:00:00'</span> (date)
<span class="kw">DEFAULT FOR</span> IV_CALENDARENDDATE <span class="kw">IS</span> <span class="str">'4712/12/31 00:00:00'</span> (date)
<span class="kw">DEFAULT FOR</span> IV_PLANENROLLMENTSTARTDATE <span class="kw">IS</span> <span class="str">'4712/12/31 00:00:00'</span> (date)
<span class="kw">DEFAULT FOR</span> IV_PLANENROLLMENTENDDATE <span class="kw">IS</span> <span class="str">'4712/12/31 00:00:00'</span> (date)
<span class="kw">DEFAULT FOR</span> IV_EVENT_DATES <span class="kw">IS</span> EMPTY_DATE_NUMBER
<span class="kw">DEFAULT FOR</span> IV_ACCRUAL_VALUES <span class="kw">IS</span> EMPTY_NUMBER_NUMBER</div>

<p>In Fast Formula there is no null. If a database item (DBI) or input value returns nothing and you haven't declared a DEFAULT, the formula errors out at runtime. Not a warning — a <b>hard error</b>. The whole ESS process will show that employee as failed.</p>

<p>So DEFAULT is mandatory for every DBI and every input value you reference.</p>

<div class="am-callout">
<div class="am-callout-icon">💡</div>
<div>
<h4>The 4712/12/31 Date</h4>
<p>This is Oracle's "end of time" constant. It's used across all Oracle products to represent "no value" for dates. For example, <code>DEFAULT FOR PER_ASG_REL_ACTUAL_TERMINATION_DATE IS '4712/12/31'</code> means if the employee has no termination date (i.e. they're active), the formula uses 4712/12/31 instead of crashing.</p>
</div>
</div>

<p><b>Two categories of defaults here:</b></p>

<p><span class="am-inline-code">PER_ASG_</span> prefixed ones are <b>Database Items</b>. These pull from HR tables at runtime using the context (HR_ASSIGNMENT_ID). The formula doesn't query the DB directly — Oracle resolves the DBI behind the scenes.</p>

<p><span class="am-inline-code">IV_</span> prefixed ones are <b>Input Values</b>. These come from the absence accrual engine. Oracle populates them automatically when the formula runs as part of the accrual process.</p>

<p><span class="am-inline-code">EMPTY_DATE_NUMBER</span> and <span class="am-inline-code">EMPTY_NUMBER_NUMBER</span> are special FF constants for array-type inputs. Their empty defaults use these built-in constants.</p>

<div class="am-pullquote">
Key concept: In FF you must declare the data type in the DEFAULT if it's not a number. Numbers are the default type. Date defaults need <code>(date)</code> at the end. Strings are inferred from the quotes.
</div>

<hr class="am-hr"/>

<!-- ==================== SECTION: INPUTS ==================== -->

<div class="am-h2">INPUTS ARE — Declaring What the Engine Passes In</div>

<div class="am-code"><span class="kw">INPUTS ARE</span>
IV_ACCRUAL,
IV_CARRYOVER,
IV_CEILING,
IV_ACCRUAL_CEILING,
IV_ACCRUALPERIODSTARTDATE        (<span class="kw">DATE</span>),
IV_ACCRUALPERIODENDDATE          (<span class="kw">DATE</span>),
IV_CALENDARSTARTDATE             (<span class="kw">DATE</span>),
IV_CALENDARENDDATE               (<span class="kw">DATE</span>),
IV_PLANENROLLMENTSTARTDATE       (<span class="kw">DATE</span>),
IV_PLANENROLLMENTENDDATE         (<span class="kw">DATE</span>),
IV_EVENT_DATES                   (<span class="kw">DATE_NUMBER</span>),
IV_ACCRUAL_VALUES                (<span class="kw">NUMBER_NUMBER</span>)</div>

<p>This block declares the input values the accrual engine will pass into the formula. You have to list every input even if you don't use it. Oracle reference guide pages 16-17 lists all the available inputs for each formula type.</p>

<p><b>Data type declarations:</b> Notice <span class="am-inline-code">(DATE)</span> after the date inputs and <span class="am-inline-code">(DATE_NUMBER)</span>, <span class="am-inline-code">(NUMBER_NUMBER)</span> for the array types. Numbers don't need a type declaration — FF assumes numeric by default. This is a common source of compilation errors for beginners — forget the <span class="am-inline-code">(DATE)</span> and FF treats it as a number and compilation fails.</p>

<div class="am-table-wrap">
<table class="am-table">
<thead>
<tr><th>Input</th><th>What It Is</th></tr>
</thead>
<tbody>
<tr><td><code>IV_ACCRUAL</code></td><td>The value the matrix engine pre-calculated. We override this.</td></tr>
<tr><td><code>IV_ACCRUALPERIODSTARTDATE / ENDDATE</code></td><td>The current processing period (e.g. Jan 1 to Jan 31)</td></tr>
<tr><td><code>IV_CALENDARSTARTDATE / ENDDATE</code></td><td>The plan calendar year (usually Jan 1 to Dec 31)</td></tr>
<tr><td><code>IV_PLANENROLLMENTSTARTDATE</code></td><td>When the employee enrolled in the absence plan</td></tr>
<tr><td><code>IV_EVENT_DATES</code></td><td>Array of event dates (band change dates etc)</td></tr>
<tr><td><code>IV_ACCRUAL_VALUES</code></td><td>Array of accrual values per band from the matrix</td></tr>
</tbody>
</table>
</div>

<p>For this formula the important ones are the period dates and <span class="am-inline-code">IV_ACCRUAL</span> (which we override). The arrays aren't used in the logic but still must be declared.</p>

<hr class="am-hr"/>

<!-- ==================== SECTION: INITIALIZATION ==================== -->

<div class="am-h2">Initialization — Variable Setup and Context DBIs</div>

<div class="am-code"><span class="cm">/*=============== INITIALIZATION ===============*/</span>
l_debug_flag = <span class="str">'Y'</span>

accrual = 0
l_process = <span class="str">'Y'</span>

l_acc_st_dt   = IV_ACCRUALPERIODSTARTDATE
l_acc_end_dt  = IV_ACCRUALPERIODENDDATE
l_cal_st_dt   = IV_CALENDARSTARTDATE
l_cal_end_dt  = IV_CALENDARENDDATE
l_enroll_st_dt = IV_PLANENROLLMENTSTARTDATE

l_abs_plan_name = ANC_ABS_PLN_NAME
l_person_id     = <span class="fn">GET_CONTEXT</span>(PERSON_ID, 0)
l_assignment_id = <span class="fn">GET_CONTEXT</span>(HR_ASSIGNMENT_ID, 0)

<span class="cm">/* PER_ASG_ DBIs - HR_ASSIGNMENT_ID is a context */</span>
l_hire_date   = PER_ASG_REL_ORIGINAL_DATE_OF_HIRE
l_term_date   = PER_ASG_REL_ACTUAL_TERMINATION_DATE
l_asg_status  = PER_ASG_STATUS_USER_STATUS

l_acc_st_month  = <span class="fn">TO_NUMBER</span>(<span class="fn">TO_CHAR</span>(l_acc_st_dt, <span class="str">'MM'</span>))
l_acc_st_year   = <span class="fn">TO_NUMBER</span>(<span class="fn">TO_CHAR</span>(l_acc_st_dt, <span class="str">'YYYY'</span>))
l_acc_end_month = <span class="fn">TO_NUMBER</span>(<span class="fn">TO_CHAR</span>(l_acc_end_dt, <span class="str">'MM'</span>))
l_acc_end_year  = <span class="fn">TO_NUMBER</span>(<span class="fn">TO_CHAR</span>(l_acc_end_dt, <span class="str">'YYYY'</span>))</div>

<p><b>GET_CONTEXT()</b> retrieves context values that Oracle sets before running the formula. For absence formulas, <span class="am-inline-code">PERSON_ID</span> and <span class="am-inline-code">HR_ASSIGNMENT_ID</span> are always available. The second parameter (0) is the default if the context isn't set.</p>

<p><b>PER_ASG_ DBIs</b> are "Person Assignment" level database items. They work because <span class="am-inline-code">HR_ASSIGNMENT_ID</span> is a context. Oracle uses the context to know WHICH assignment to pull data for. In absence formulas Oracle sets this context automatically.</p>

<div class="am-callout">
<div class="am-callout-icon">🔍</div>
<div>
<h4>Date Extraction Pattern</h4>
<p>FF has no direct "get month from date" function. The workaround is <code>TO_CHAR</code> with a format mask to get the string, then <code>TO_NUMBER</code> to convert to integer. <code>'MM'</code> gives two-digit month (01-12), <code>'YYYY'</code> gives four-digit year. You'll use this pattern constantly.</p>
</div>
</div>

<p><b>The <span class="am-inline-code">l_process</span> flag</b> — initialized to <span class="am-inline-code">'Y'</span>. This is an important FF pattern. Since FF doesn't support early returns mid-formula (you can only RETURN at the very end), you use a flag variable to control flow. Each validation check can set <span class="am-inline-code">l_process = 'N'</span>, and all subsequent logic checks it before executing. It's the FF equivalent of guard clauses.</p>

<hr class="am-hr"/>

<!-- ==================== SECTION: LOGGING ==================== -->

<div class="am-h2">ESS_LOG_WRITE — The Only Debugging Tool You Have</div>

<div class="am-code"><span class="kw">IF</span> (l_debug_flag = <span class="str">'Y'</span>) <span class="kw">THEN</span>
(
l_log = <span class="fn">ESS_LOG_WRITE</span>(<span class="str">'Starting PH Vacation Leave accrual matrix calculation'</span>)
l_log = <span class="fn">ESS_LOG_WRITE</span>(<span class="str">'Person '</span> || <span class="fn">TO_CHAR</span>(l_person_id) 
|| <span class="str">', assignment '</span> || <span class="fn">TO_CHAR</span>(l_assignment_id) 
|| <span class="str">', plan '</span> || l_abs_plan_name)
l_log = <span class="fn">ESS_LOG_WRITE</span>(<span class="str">'Hire date '</span> || <span class="fn">TO_CHAR</span>(l_hire_date, <span class="str">'DD-MON-YYYY'</span>))
l_log = <span class="fn">ESS_LOG_WRITE</span>(<span class="str">'Assignment status '</span> || l_asg_status)
)</div>

<p>FF has no debugger, no breakpoints, no console. <span class="am-inline-code">ESS_LOG_WRITE</span> is it. It writes a line to the Enterprise Scheduler (ESS) job output log.</p>

<div class="am-callout">
<div class="am-callout-icon">⚠️</div>
<div>
<h4>Important FF Syntax Rule</h4>
<p>You <b>MUST</b> assign the return to a variable. You cannot just call <code>ESS_LOG_WRITE('...')</code> as a standalone statement. FF requires all function calls to be assigned. <code>l_log</code> is a throwaway variable — its value doesn't matter.</p>
</div>
</div>

<p><b>String concatenation with <span class="am-inline-code">||</span></b> — the <span class="am-inline-code">||</span> operator joins strings. <span class="am-inline-code">TO_CHAR</span> converts numbers and dates to strings for concatenation. For dates you can pass a format mask like <span class="am-inline-code">'DD-MON-YYYY'</span>.</p>

<p>The formula wraps all logging in <span class="am-inline-code">IF (l_debug_flag = 'Y')</span> so you can turn it off in production by changing one variable. In testing environments keep it on.</p>

<hr class="am-hr"/>

<!-- ==================== SECTION: MONTHLY GUARD ==================== -->

<div class="am-h2">Monthly Frequency Guard — A Defensive Pattern</div>

<div class="am-code"><span class="cm">/*=============== MONTHLY FREQUENCY GUARD ===============*/</span>

l_period_days = <span class="fn">DAYS_BETWEEN</span>(l_acc_end_dt, l_acc_st_dt) + 1

<span class="kw">IF</span> (l_period_days < 28) <span class="kw">THEN</span>
(
l_process = <span class="str">'N'</span>
<span class="kw">IF</span> (l_debug_flag = <span class="str">'Y'</span>) <span class="kw">THEN</span>
(
l_log = <span class="fn">ESS_LOG_WRITE</span>(<span class="str">'This formula requires monthly processing, current period is '</span> 
|| <span class="fn">TO_CHAR</span>(l_period_days) || <span class="str">' days, skipping'</span>)
)
)</div>

<p><span class="am-inline-code">DAYS_BETWEEN(date1, date2)</span> returns the number of days between two dates. The <span class="am-inline-code">+1</span> is because it's exclusive — Jan 1 to Jan 31 gives 30, but the actual period is 31 days.</p>

<p>Why this guard exists: this formula assumes monthly processing. The accrual logic returns 1.25 days per period. If the plan is misconfigured to process weekly, the employee would get 1.25 days per WEEK instead of per month. This check catches that by rejecting any period shorter than 28 days (February being the shortest month).</p>

<div class="am-pullquote">
This is a good defensive pattern to reuse. If your formula assumes a specific frequency, validate it. Also notice it logs the actual period days in the skip message — helpful for diagnosing the misconfiguration.
</div>

<hr class="am-hr"/>

<!-- ==================== SECTION: ELIGIBILITY ==================== -->

<div class="am-h2">Eligibility Checks — Cascading Flag Pattern</div>

<div class="am-code"><span class="cm">/*=============== ELIGIBILITY ===============*/</span>

<span class="cm">/* Check 1: Hire date exists */</span>
<span class="kw">IF</span> (l_process = <span class="str">'Y'</span> <span class="kw">AND</span>
l_hire_date = <span class="fn">TO_DATE</span>(<span class="str">'4712/12/31 00:00:00'</span>, <span class="str">'YYYY/MM/DD HH24:MI:SS'</span>)) <span class="kw">THEN</span>
(  l_process = <span class="str">'N'</span>  )

<span class="cm">/* Check 2: Period is after hire date */</span>
<span class="kw">IF</span> (l_process = <span class="str">'Y'</span> <span class="kw">AND</span> l_acc_end_dt < l_hire_date) <span class="kw">THEN</span>
(  l_process = <span class="str">'N'</span>  )

<span class="cm">/* Check 3: Not terminated before period */</span>
<span class="kw">IF</span> (l_process = <span class="str">'Y'</span> <span class="kw">AND</span>
l_term_date < l_acc_st_dt <span class="kw">AND</span>
l_term_date <> <span class="fn">TO_DATE</span>(<span class="str">'4712/12/31 00:00:00'</span>, <span class="str">'YYYY/MM/DD HH24:MI:SS'</span>)) <span class="kw">THEN</span>
(  l_process = <span class="str">'N'</span>  )

<span class="cm">/* Check 4: Assignment is active */</span>
<span class="kw">IF</span> (l_process = <span class="str">'Y'</span> <span class="kw">AND</span> l_asg_status <> <span class="str">'ACTIVE'</span>) <span class="kw">THEN</span>
(  l_process = <span class="str">'N'</span>  )</div>

<p>Four checks, all using the same pattern. Each one checks <span class="am-inline-code">l_process = 'Y'</span> first — once any check sets it to <span class="am-inline-code">'N'</span>, all remaining checks are skipped automatically.</p>

<ul class="am-list">
<li><b>Check 1:</b> Hire date is 4712 = hire date DBI returned empty = no hire date on record. Skip.</li>
<li><b>Check 2:</b> Period end date is before hire date = this accrual period is before the employee was hired. Skip.</li>
<li><b>Check 3:</b> Termination date is before period start AND termination date is not 4712. The second condition is critical — without it, you'd compare the 4712 default against the period start for every active employee.</li>
<li><b>Check 4:</b> Assignment user status must be exactly <span class="am-inline-code">'ACTIVE'</span>. FF string comparison is <b>case-sensitive</b>. If your Oracle instance uses <span class="am-inline-code">'Active'</span> or <span class="am-inline-code">'Active - Payroll Eligible'</span>, this check will fail for everyone. Always verify the exact string value in your setup.</li>
</ul>

<div class="am-callout">
<div class="am-callout-icon">🚨</div>
<div>
<h4>FF Concept — TO_DATE()</h4>
<p>The format mask <code>'YYYY/MM/DD HH24:MI:SS'</code> must match the string format exactly. <code>HH24</code> is 24-hour time. FF is strict — wrong format mask = runtime error.</p>
</div>
</div>

<hr class="am-hr"/>

<!-- ==================== SECTION: ACCRUAL LOGIC ==================== -->

<div class="am-h2">Accrual Logic — The Core Calculation</div>

<div class="am-code"><span class="cm">/*=============== ACCRUAL LOGIC ===============*/</span>

<span class="kw">IF</span> (l_process = <span class="str">'Y'</span>) <span class="kw">THEN</span>
(
l_months_of_service = <span class="fn">MONTHS_BETWEEN</span>(l_acc_end_dt, l_hire_date)
)</div>

<p>This is where <span class="am-inline-code">IV_ACCRUAL</span> gets overridden. <span class="am-inline-code">MONTHS_BETWEEN(date1, date2)</span> returns a decimal. If someone was hired on Mar 15 and the period ends on Sep 15, it returns exactly 6. If the period ends on Sep 10, it returns something like 5.83.</p>

<!-- Phase 1 -->
<div class="am-h3"><span class="am-phase-badge">PHASE 1</span> Probation (< 6 months)</div>

<div class="am-code"><span class="kw">IF</span> (l_months_of_service < 6) <span class="kw">THEN</span>
(
accrual = 0
<span class="cm">/* Employee is still in probation, no vacation accrual */</span>
)</div>

<p>Straightforward. Less than 6 months of service? Accrual stays at 0.</p>

<!-- Phase 2 -->
<div class="am-h3"><span class="am-phase-badge bridge">PHASE 2</span> Monthly Accrual (6 to 12 months)</div>

<div class="am-code"><span class="kw">IF</span> (l_months_of_service >= 6 <span class="kw">AND</span> l_months_of_service < 12) <span class="kw">THEN</span>
(
accrual = 1.25
<span class="cm">/* Accruing 1.25 days this period */</span>
)</div>

<p>1.25 days per monthly period. Since the formula runs once per month and returns 1.25, the engine accumulates 1.25 each month. 6 months × 1.25 = <b>7.5 days</b> by regularization.</p>

<!-- Phase 3 -->
<div class="am-h3"><span class="am-phase-badge lump">PHASE 3</span> Post-Regularization (≥ 12 months)</div>

<p>This is the most complex part. It has sub-phases. First, calculate the one-time credit date:</p>

<div class="am-code">l_reg_date  = <span class="fn">ADD_MONTHS</span>(l_hire_date, 12)
l_reg_year  = <span class="fn">TO_NUMBER</span>(<span class="fn">TO_CHAR</span>(l_reg_date, <span class="str">'YYYY'</span>))
l_reg_month = <span class="fn">TO_NUMBER</span>(<span class="fn">TO_CHAR</span>(l_reg_date, <span class="str">'MM'</span>))

<span class="cm">/* If regularized IN January, credit that same January
Otherwise credit the following year January */</span>
<span class="kw">IF</span> (l_reg_month = 1) <span class="kw">THEN</span>
(  l_first_jan_year = l_reg_year  )
<span class="kw">ELSE</span>
(  l_first_jan_year = l_reg_year + 1  )

l_first_jan_date = <span class="fn">TO_DATE</span>(<span class="str">'01/01/'</span> || <span class="fn">TO_CHAR</span>(l_first_jan_year), <span class="str">'DD/MM/YYYY'</span>)</div>

<p>The business rule: the 15-day credit happens in January. If regularization falls IN January, use that same January. Otherwise use the NEXT January:</p>

<div class="am-table-wrap">
<table class="am-table">
<thead>
<tr><th>Hire Date</th><th>Regularization Date</th><th>First Eligible January</th></tr>
</thead>
<tbody>
<tr><td>Jan 15, 2024</td><td>Jan 15, 2025</td><td><b>January 2025</b></td></tr>
<tr><td>Mar 10, 2024</td><td>Mar 10, 2025</td><td><b>January 2026</b></td></tr>
<tr><td>Dec 1, 2023</td><td>Dec 1, 2024</td><td><b>January 2025</b></td></tr>
</tbody>
</table>
</div>

<!-- Sub-phase 3A -->
<p><b><span class="am-phase-badge bridge">3A</span> Bridge Period</b> — Between regularization and first eligible January, keep accruing 1.25/month:</p>

<div class="am-code"><span class="kw">IF</span> (l_acc_end_dt < l_first_jan_date) <span class="kw">THEN</span>
(
accrual = 1.25
<span class="cm">/* First January not reached yet, continuing monthly 1.25 days */</span>
)</div>

<!-- Sub-phase 3B -->
<p><b><span class="am-phase-badge lump">3B</span> One-Time Lump Sum</b> — ONLY the first eligible January. Both period start and end must be in the same January:</p>

<div class="am-code"><span class="kw">IF</span> (l_acc_st_month = 1 <span class="kw">AND</span>
l_acc_st_year = l_first_jan_year <span class="kw">AND</span>
l_acc_end_month = 1 <span class="kw">AND</span>
l_acc_end_year = l_first_jan_year) <span class="kw">THEN</span>
(
accrual = 15
<span class="cm">/* One-time January credit: 15 days */</span>
)</div>

<div class="am-pullquote">
Why this doesn't need a "already credited" flag: only one monthly period can ever have both start and end in January of a specific year. The date conditions themselves guarantee it fires exactly once. The math is the guard.
</div>

<!-- Sub-phase 3C -->
<p><b><span class="am-phase-badge done">3C</span> After the Credit</b> — Any period after the first eligible January returns zero:</p>

<div class="am-code"><span class="kw">IF</span> (l_acc_end_year > l_first_jan_year <span class="kw">OR</span>
(l_acc_end_year = l_first_jan_year <span class="kw">AND</span> l_acc_end_month > 1)) <span class="kw">THEN</span>
(
accrual = 0
<span class="cm">/* One-time 15 day credit was already given, no further accrual */</span>
)</div>

<hr class="am-hr"/>

<!-- ==================== SECTION: RETURN ==================== -->

<div class="am-h2">RETURN — The Formula Output</div>

<div class="am-code"><span class="cm">/*=============== SINGLE RETURN per Oracle Doc page 19 ===============*/</span>

<span class="kw">IF</span> (l_debug_flag = <span class="str">'Y'</span>) <span class="kw">THEN</span>
(
l_log = <span class="fn">ESS_LOG_WRITE</span>(<span class="str">'Returning accrual '</span> || <span class="fn">TO_CHAR</span>(accrual))
)

<span class="kw">RETURN</span> accrual</div>

<p>For accrual matrix formulas, you return a single numeric value called <span class="am-inline-code">accrual</span>. The engine takes this value and adds it to the employee's leave balance for the period.</p>

<div class="am-callout">
<div class="am-callout-icon">🔒</div>
<div>
<h4>FF Concept</h4>
<p>You can only have ONE return statement and it must be the <b>last executable statement</b>. You cannot return early mid-formula. That's why the entire flow uses the <code>l_process</code> flag and nested IFs to control which value <code>accrual</code> gets set to.</p>
</div>
</div>

<hr class="am-hr"/>

<!-- ==================== SECTION: SYNTAX REFERENCE ==================== -->

<div class="am-h2">FF Syntax Things to Remember</div>

<p>Since this post is for people learning FF, here are the syntax rules that this formula demonstrates:</p>

<div class="am-syntax-grid">
<div class="am-syntax-card">
<strong>= for Everything</strong>
<p><code>=</code> is used for both assignment and comparison. Context determines which. Inside IF conditions it's comparison, outside it's assignment. There is no <code>==</code>.</p>
</div>
<div class="am-syntax-card">
<strong>Parentheses Required</strong>
<p><code>IF (condition) THEN ( statements )</code>. Remove the parens around the body and compilation fails.</p>
</div>
<div class="am-syntax-card">
<strong>No ELSE IF</strong>
<p>Use nested IF inside ELSE, or independent IF blocks with a flag. There is no <code>ELSIF</code> keyword.</p>
</div>
<div class="am-syntax-card">
<strong>Case-Sensitive Strings</strong>
<p><code>'ACTIVE' <> 'Active'</code>. Always verify the exact string value in your Oracle setup.</p>
</div>
<div class="am-syntax-card">
<strong>Must Assign Functions</strong>
<p>Every function call must be assigned to a variable, even void-like functions like <code>ESS_LOG_WRITE</code>.</p>
</div>
<div class="am-syntax-card">
<strong>|| is Concatenation</strong>
<p>Not logical OR. Logical OR is the word <code>OR</code>. Use <code>||</code> only for string joining.</p>
</div>
<div class="am-syntax-card">
<strong>RETURN Must Be Last</strong>
<p>No early returns allowed. Use flag variables to control flow and return only at the end.</p>
</div>
<div class="am-syntax-card">
<strong>No Semicolons</strong>
<p>FF statements are not terminated with <code>;</code>. Line breaks and parser context determine boundaries.</p>
</div>
</div>

<hr class="am-hr"/>

<!-- ==================== SECTION: WRAP UP ==================== -->

<div class="am-h2">Wrapping Up</div>

<p>That's the whole formula broken down. The key FF concepts it covers: DEFAULT handling, DBI vs input values, GET_CONTEXT, date manipulation with TO_CHAR / TO_NUMBER / TO_DATE / ADD_MONTHS / MONTHS_BETWEEN / DAYS_BETWEEN, ESS_LOG_WRITE debugging, the process flag pattern for flow control, and RETURN behavior.</p>

<p>If you're new to FF, I'd suggest actually typing this formula out yourself in the formula editor rather than copy-pasting. You'll catch the syntax patterns faster that way.</p>

<p>Hope this helps someone. First blog post done.</p>

<!-- ==================== FOOTER ==================== -->

<div class="am-footer-box">
<div class="am-footer-avatar">AM</div>
<div>
<div class="am-footer-name">Abhishek Mohanty</div>
<div class="am-footer-bio">Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Core HR, Redwood migrations, HDL, and OTBI reporting. Follow me for more Oracle HCM deep dives.</div>
</div>
</div>

</div>
