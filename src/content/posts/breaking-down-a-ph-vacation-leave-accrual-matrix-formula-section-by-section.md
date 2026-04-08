---
title: "Breaking Down a PH Vacation Leave Accrual Matrix Formula — Section by Section"
description: "A detailed section-by-section breakdown of a Philippines vacation leave accrual matrix formula covering eligibility, tenure bands, and proration logic."
pubDate: 2026-03-14
tags: []
---

My first blog post so bear with me. I wanted to write this because when I started learning Fast Formula I couldn't find anyone explaining the actual concepts behind each block. So here we go.

AM

Abhishek Mohanty

Oracle HCM Cloud Consultant & Technical Lead

What Even Is an Accrual Matrix Formula?

Before jumping into the code, quick context. In Oracle Absence Management there are different formula types. This one is **Absence Accrual Matrix Formula**. What that means is — the absence plan already has a matrix table configured (like a grid with bands based on years of service or grade etc), and the matrix engine calculates an accrual value and passes it to this formula as IV_ACCRUAL.

The formula's job is to either accept that value or override it. In our case we're completely ignoring IV_ACCRUAL and doing our own calculation. That's the whole point of a matrix formula — you get a hook to intercept and customize.

This specific formula implements **Philippine vacation leave rules**:

- **0 to 6 months** — nothing (probation)
- **6 to 12 months** — 1.25 days per month
- **After 12 months** — one-time 15 day credit in January, then nothing after

OK let's get into it.

---

The Header Block

/*************************************************************
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
*************************************************************/

This is just a comment block but don't skip it. It tells you the formula type (which determines available inputs and returns), the business rules, the Oracle doc reference, and the processing frequency requirement. The note about monthly frequency is important — the formula has a guard for this later.

---

DEFAULT Statements — Why They Exist in FF

/* DBI defaults - HR_ASSIGNMENT_ID context available */
DEFAULT FOR PER_ASG_REL_ORIGINAL_DATE_OF_HIRE IS '4712/12/31 00:00:00' (date)
DEFAULT FOR PER_ASG_REL_ACTUAL_TERMINATION_DATE IS '4712/12/31 00:00:00' (date)
DEFAULT FOR PER_ASG_STATUS_USER_STATUS IS 'NA'
DEFAULT FOR PER_ASG_FTE_VALUE IS 1
DEFAULT FOR ANC_ABS_PLN_NAME IS 'NA'

/* Input value defaults per Oracle doc page 16-17 */
DEFAULT FOR IV_ACCRUAL IS 0
DEFAULT FOR IV_CARRYOVER IS 0
DEFAULT FOR IV_CEILING IS 0
DEFAULT FOR IV_ACCRUAL_CEILING IS 0
DEFAULT FOR IV_ACCRUALPERIODSTARTDATE IS '4712/12/31 00:00:00' (date)
DEFAULT FOR IV_ACCRUALPERIODENDDATE IS '4712/12/31 00:00:00' (date)
DEFAULT FOR IV_CALENDARSTARTDATE IS '4712/12/31 00:00:00' (date)
DEFAULT FOR IV_CALENDARENDDATE IS '4712/12/31 00:00:00' (date)
DEFAULT FOR IV_PLANENROLLMENTSTARTDATE IS '4712/12/31 00:00:00' (date)
DEFAULT FOR IV_PLANENROLLMENTENDDATE IS '4712/12/31 00:00:00' (date)
DEFAULT FOR IV_EVENT_DATES IS EMPTY_DATE_NUMBER
DEFAULT FOR IV_ACCRUAL_VALUES IS EMPTY_NUMBER_NUMBER

In Fast Formula there is no null. If a database item (DBI) or input value returns nothing and you haven't declared a DEFAULT, the formula errors out at runtime. Not a warning — a **hard error**. The whole ESS process will show that employee as failed.

So DEFAULT is mandatory for every DBI and every input value you reference.

💡

#### The 4712/12/31 Date

This is Oracle's "end of time" constant. It's used across all Oracle products to represent "no value" for dates. For example, `DEFAULT FOR PER_ASG_REL_ACTUAL_TERMINATION_DATE IS '4712/12/31'` means if the employee has no termination date (i.e. they're active), the formula uses 4712/12/31 instead of crashing.

**Two categories of defaults here:**

PER_ASG_ prefixed ones are **Database Items**. These pull from HR tables at runtime using the context (HR_ASSIGNMENT_ID). The formula doesn't query the DB directly — Oracle resolves the DBI behind the scenes.

IV_ prefixed ones are **Input Values**. These come from the absence accrual engine. Oracle populates them automatically when the formula runs as part of the accrual process.

EMPTY_DATE_NUMBER and EMPTY_NUMBER_NUMBER are special FF constants for array-type inputs. Their empty defaults use these built-in constants.

Key concept: In FF you must declare the data type in the DEFAULT if it's not a number. Numbers are the default type. Date defaults need `(date)` at the end. Strings are inferred from the quotes.

---

INPUTS ARE — Declaring What the Engine Passes In

INPUTS ARE
  IV_ACCRUAL,
  IV_CARRYOVER,
  IV_CEILING,
  IV_ACCRUAL_CEILING,
  IV_ACCRUALPERIODSTARTDATE        (DATE),
  IV_ACCRUALPERIODENDDATE          (DATE),
  IV_CALENDARSTARTDATE             (DATE),
  IV_CALENDARENDDATE               (DATE),
  IV_PLANENROLLMENTSTARTDATE       (DATE),
  IV_PLANENROLLMENTENDDATE         (DATE),
  IV_EVENT_DATES                   (DATE_NUMBER),
  IV_ACCRUAL_VALUES                (NUMBER_NUMBER)

This block declares the input values the accrual engine will pass into the formula. You have to list every input even if you don't use it. Oracle reference guide pages 16-17 lists all the available inputs for each formula type.

**Data type declarations:** Notice (DATE) after the date inputs and (DATE_NUMBER), (NUMBER_NUMBER) for the array types. Numbers don't need a type declaration — FF assumes numeric by default. This is a common source of compilation errors for beginners — forget the (DATE) and FF treats it as a number and compilation fails.

| Input | What It Is |
| --- | --- |
| `IV_ACCRUAL` | The value the matrix engine pre-calculated. We override this. |
| `IV_ACCRUALPERIODSTARTDATE / ENDDATE` | The current processing period (e.g. Jan 1 to Jan 31) |
| `IV_CALENDARSTARTDATE / ENDDATE` | The plan calendar year (usually Jan 1 to Dec 31) |
| `IV_PLANENROLLMENTSTARTDATE` | When the employee enrolled in the absence plan |
| `IV_EVENT_DATES` | Array of event dates (band change dates etc) |
| `IV_ACCRUAL_VALUES` | Array of accrual values per band from the matrix |

For this formula the important ones are the period dates and IV_ACCRUAL (which we override). The arrays aren't used in the logic but still must be declared.

---

Initialization — Variable Setup and Context DBIs

/*=============== INITIALIZATION ===============*/
l_debug_flag = 'Y'

accrual = 0
l_process = 'Y'

l_acc_st_dt   = IV_ACCRUALPERIODSTARTDATE
l_acc_end_dt  = IV_ACCRUALPERIODENDDATE
l_cal_st_dt   = IV_CALENDARSTARTDATE
l_cal_end_dt  = IV_CALENDARENDDATE
l_enroll_st_dt = IV_PLANENROLLMENTSTARTDATE

l_abs_plan_name = ANC_ABS_PLN_NAME
l_person_id     = GET_CONTEXT(PERSON_ID, 0)
l_assignment_id = GET_CONTEXT(HR_ASSIGNMENT_ID, 0)

/* PER_ASG_ DBIs - HR_ASSIGNMENT_ID is a context */
l_hire_date   = PER_ASG_REL_ORIGINAL_DATE_OF_HIRE
l_term_date   = PER_ASG_REL_ACTUAL_TERMINATION_DATE
l_asg_status  = PER_ASG_STATUS_USER_STATUS

l_acc_st_month  = TO_NUMBER(TO_CHAR(l_acc_st_dt, 'MM'))
l_acc_st_year   = TO_NUMBER(TO_CHAR(l_acc_st_dt, 'YYYY'))
l_acc_end_month = TO_NUMBER(TO_CHAR(l_acc_end_dt, 'MM'))
l_acc_end_year  = TO_NUMBER(TO_CHAR(l_acc_end_dt, 'YYYY'))

**GET_CONTEXT()** retrieves context values that Oracle sets before running the formula. For absence formulas, PERSON_ID and HR_ASSIGNMENT_ID are always available. The second parameter (0) is the default if the context isn't set.

**PER_ASG_ DBIs** are "Person Assignment" level database items. They work because HR_ASSIGNMENT_ID is a context. Oracle uses the context to know WHICH assignment to pull data for. In absence formulas Oracle sets this context automatically.

🔍

#### Date Extraction Pattern

FF has no direct "get month from date" function. The workaround is `TO_CHAR` with a format mask to get the string, then `TO_NUMBER` to convert to integer. `'MM'` gives two-digit month (01-12), `'YYYY'` gives four-digit year. You'll use this pattern constantly.

**The l_process flag** — initialized to 'Y'. This is an important FF pattern. Since FF doesn't support early returns mid-formula (you can only RETURN at the very end), you use a flag variable to control flow. Each validation check can set l_process = 'N', and all subsequent logic checks it before executing. It's the FF equivalent of guard clauses.

---

ESS_LOG_WRITE — The Only Debugging Tool You Have

IF (l_debug_flag = 'Y') THEN
(
  l_log = ESS_LOG_WRITE('Starting PH Vacation Leave accrual matrix calculation')
  l_log = ESS_LOG_WRITE('Person ' || TO_CHAR(l_person_id)
          || ', assignment ' || TO_CHAR(l_assignment_id)
          || ', plan ' || l_abs_plan_name)
  l_log = ESS_LOG_WRITE('Hire date ' || TO_CHAR(l_hire_date, 'DD-MON-YYYY'))
  l_log = ESS_LOG_WRITE('Assignment status ' || l_asg_status)
)

FF has no debugger, no breakpoints, no console. ESS_LOG_WRITE is it. It writes a line to the Enterprise Scheduler (ESS) job output log.

⚠️

#### Important FF Syntax Rule

You **MUST** assign the return to a variable. You cannot just call `ESS_LOG_WRITE('...')` as a standalone statement. FF requires all function calls to be assigned. `l_log` is a throwaway variable — its value doesn't matter.

**String concatenation with ||** — the || operator joins strings. TO_CHAR converts numbers and dates to strings for concatenation. For dates you can pass a format mask like 'DD-MON-YYYY'.

The formula wraps all logging in IF (l_debug_flag = 'Y') so you can turn it off in production by changing one variable. In testing environments keep it on.

---

Monthly Frequency Guard — A Defensive Pattern

/*=============== MONTHLY FREQUENCY GUARD ===============*/

l_period_days = DAYS_BETWEEN(l_acc_end_dt, l_acc_st_dt) + 1

IF (l_period_days < 28) THEN
(
  l_process = 'N'
  IF (l_debug_flag = 'Y') THEN
  (
    l_log = ESS_LOG_WRITE('This formula requires monthly processing, current period is '
            || TO_CHAR(l_period_days) || ' days, skipping')
  )
)

DAYS_BETWEEN(date1, date2) returns the number of days between two dates. The +1 is because it's exclusive — Jan 1 to Jan 31 gives 30, but the actual period is 31 days.

Why this guard exists: this formula assumes monthly processing. The accrual logic returns 1.25 days per period. If the plan is misconfigured to process weekly, the employee would get 1.25 days per WEEK instead of per month. This check catches that by rejecting any period shorter than 28 days (February being the shortest month).

This is a good defensive pattern to reuse. If your formula assumes a specific frequency, validate it. Also notice it logs the actual period days in the skip message — helpful for diagnosing the misconfiguration.

---

Eligibility Checks — Cascading Flag Pattern

/*=============== ELIGIBILITY ===============*/

/* Check 1: Hire date exists */
IF (l_process = 'Y' AND
    l_hire_date = TO_DATE('4712/12/31 00:00:00', 'YYYY/MM/DD HH24:MI:SS')) THEN
(  l_process = 'N'  )

/* Check 2: Period is after hire date */
IF (l_process = 'Y' AND l_acc_end_dt < l_hire_date) THEN
(  l_process = 'N'  )

/* Check 3: Not terminated before period */
IF (l_process = 'Y' AND
    l_term_date < l_acc_st_dt AND
    l_term_date <> TO_DATE('4712/12/31 00:00:00', 'YYYY/MM/DD HH24:MI:SS')) THEN
(  l_process = 'N'  )

/* Check 4: Assignment is active */
IF (l_process = 'Y' AND l_asg_status <> 'ACTIVE') THEN
(  l_process = 'N'  )

Four checks, all using the same pattern. Each one checks l_process = 'Y' first — once any check sets it to 'N', all remaining checks are skipped automatically.

- **Check 1:** Hire date is 4712 = hire date DBI returned empty = no hire date on record. Skip.
- **Check 2:** Period end date is before hire date = this accrual period is before the employee was hired. Skip.
- **Check 3:** Termination date is before period start AND termination date is not 4712. The second condition is critical — without it, you'd compare the 4712 default against the period start for every active employee.
- **Check 4:** Assignment user status must be exactly 'ACTIVE'. FF string comparison is **case-sensitive**. If your Oracle instance uses 'Active' or 'Active - Payroll Eligible', this check will fail for everyone. Always verify the exact string value in your setup.

🚨

#### FF Concept — TO_DATE()

The format mask `'YYYY/MM/DD HH24:MI:SS'` must match the string format exactly. `HH24` is 24-hour time. FF is strict — wrong format mask = runtime error.

---

Accrual Logic — The Core Calculation

/*=============== ACCRUAL LOGIC ===============*/

IF (l_process = 'Y') THEN
(
  l_months_of_service = MONTHS_BETWEEN(l_acc_end_dt, l_hire_date)
)

This is where IV_ACCRUAL gets overridden. MONTHS_BETWEEN(date1, date2) returns a decimal. If someone was hired on Mar 15 and the period ends on Sep 15, it returns exactly 6. If the period ends on Sep 10, it returns something like 5.83.

PHASE 1 Probation (< 6 months)

IF (l_months_of_service < 6) THEN
(
  accrual = 0
  /* Employee is still in probation, no vacation accrual */
)

Straightforward. Less than 6 months of service? Accrual stays at 0.

PHASE 2 Monthly Accrual (6 to 12 months)

IF (l_months_of_service >= 6 AND l_months_of_service < 12) THEN
(
  accrual = 1.25
  /* Accruing 1.25 days this period */
)

1.25 days per monthly period. Since the formula runs once per month and returns 1.25, the engine accumulates 1.25 each month. 6 months × 1.25 = **7.5 days** by regularization.

PHASE 3 Post-Regularization (≥ 12 months)

This is the most complex part. It has sub-phases. First, calculate the one-time credit date:

l_reg_date  = ADD_MONTHS(l_hire_date, 12)
l_reg_year  = TO_NUMBER(TO_CHAR(l_reg_date, 'YYYY'))
l_reg_month = TO_NUMBER(TO_CHAR(l_reg_date, 'MM'))

/* If regularized IN January, credit that same January
   Otherwise credit the following year January */
IF (l_reg_month = 1) THEN
(  l_first_jan_year = l_reg_year  )
ELSE
(  l_first_jan_year = l_reg_year + 1  )

l_first_jan_date = TO_DATE('01/01/' || TO_CHAR(l_first_jan_year), 'DD/MM/YYYY')

The business rule: the 15-day credit happens in January. If regularization falls IN January, use that same January. Otherwise use the NEXT January:

| Hire Date | Regularization Date | First Eligible January |
| --- | --- | --- |
| Jan 15, 2024 | Jan 15, 2025 | **January 2025** |
| Mar 10, 2024 | Mar 10, 2025 | **January 2026** |
| Dec 1, 2023 | Dec 1, 2024 | **January 2025** |

**3A Bridge Period** — Between regularization and first eligible January, keep accruing 1.25/month:

IF (l_acc_end_dt < l_first_jan_date) THEN
(
  accrual = 1.25
  /* First January not reached yet, continuing monthly 1.25 days */
)

**3B One-Time Lump Sum** — ONLY the first eligible January. Both period start and end must be in the same January:

IF (l_acc_st_month = 1 AND
    l_acc_st_year = l_first_jan_year AND
    l_acc_end_month = 1 AND
    l_acc_end_year = l_first_jan_year) THEN
(
  accrual = 15
  /* One-time January credit: 15 days */
)

Why this doesn't need a "already credited" flag: only one monthly period can ever have both start and end in January of a specific year. The date conditions themselves guarantee it fires exactly once. The math is the guard.

**3C After the Credit** — Any period after the first eligible January returns zero:

IF (l_acc_end_year > l_first_jan_year OR
    (l_acc_end_year = l_first_jan_year AND l_acc_end_month > 1)) THEN
(
  accrual = 0
  /* One-time 15 day credit was already given, no further accrual */
)

---

RETURN — The Formula Output

/*=============== SINGLE RETURN per Oracle Doc page 19 ===============*/

IF (l_debug_flag = 'Y') THEN
(
  l_log = ESS_LOG_WRITE('Returning accrual ' || TO_CHAR(accrual))
)

RETURN accrual

For accrual matrix formulas, you return a single numeric value called accrual. The engine takes this value and adds it to the employee's leave balance for the period.

🔒

#### FF Concept

You can only have ONE return statement and it must be the **last executable statement**. You cannot return early mid-formula. That's why the entire flow uses the `l_process` flag and nested IFs to control which value `accrual` gets set to.

---

FF Syntax Things to Remember

Since this post is for people learning FF, here are the syntax rules that this formula demonstrates:

    **= for Everything**

`=` is used for both assignment and comparison. Context determines which. Inside IF conditions it's comparison, outside it's assignment. There is no `==`.

    **Parentheses Required**

`IF (condition) THEN ( statements )`. Remove the parens around the body and compilation fails.

    **No ELSE IF**

Use nested IF inside ELSE, or independent IF blocks with a flag. There is no `ELSIF` keyword.

    **Case-Sensitive Strings**

`'ACTIVE' <> 'Active'`. Always verify the exact string value in your Oracle setup.

    **Must Assign Functions**

Every function call must be assigned to a variable, even void-like functions like `ESS_LOG_WRITE`.

    **|| is Concatenation**

Not logical OR. Logical OR is the word `OR`. Use `||` only for string joining.

    **RETURN Must Be Last**

No early returns allowed. Use flag variables to control flow and return only at the end.

    **No Semicolons**

FF statements are not terminated with `;`. Line breaks and parser context determine boundaries.

---

Wrapping Up

That's the whole formula broken down. The key FF concepts it covers: DEFAULT handling, DBI vs input values, GET_CONTEXT, date manipulation with TO_CHAR / TO_NUMBER / TO_DATE / ADD_MONTHS / MONTHS_BETWEEN / DAYS_BETWEEN, ESS_LOG_WRITE debugging, the process flag pattern for flow control, and RETURN behavior.

If you're new to FF, I'd suggest actually typing this formula out yourself in the formula editor rather than copy-pasting. You'll catch the syntax patterns faster that way.

Hope this helps someone. First blog post done.

AM

Abhishek Mohanty

Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Core HR, Redwood migrations, HDL, and OTBI reporting. Follow me for more Oracle HCM deep dives.

