---
title: "Debugging Oracle Fast Formula: 5 Logging Patterns Every HCM Cloud Consultant Must Know"
description: "Your formula compiled successfully. It even runs without errors. But the result is wrong — and you have no idea why. Welcome to the world of Fast Formula debugging, where the only tool you have is a single function: ESS_LOG_WRITE."
pubDate: 2026-03-17
tags: ["Fast Formula", "Debugging", "Essential"]
---

Your formula compiled successfully. It even runs without errors. But the result is wrong — and you have no idea why. Welcome to the world of Fast Formula debugging, where the only tool you have is a single function: ESS_LOG_WRITE.

|  | Abhishek Mohanty |
| --- | --- |

Fast Formula has no debugger. No breakpoints. No step-through execution. No variable watch window. The only way to see what's happening inside a running formula is to write messages to the ESS process log using `ESS_LOG_WRITE`.

This post covers how the function works, the patterns that make debug logs actually useful, and real examples from production absence formulas.

---

## The Basics: How ESS_LOG_WRITE Works

`ESS_LOG_WRITE` is a built-in function that writes a text message to the Enterprise Scheduler Service (ESS) log. When the formula runs as part of a scheduled process (like accrual calculation or absence validation), the message appears in the process output log.

There's one quirk: the function returns a number, so you must assign its result to a variable — even though you'll never use that variable for anything else:

```text
/* The basic syntax */
l_debug = ESS_LOG_WRITE('Hello from my formula')

/* l_debug is a throwaway variable — declare it once */
l_debug = 0  /* initialize at the top of your formula */
```

The message can include any text. To include variable values, concatenate them with `||` and convert non-text values using `TO_CHAR`:

```text
/* Log a text variable */
l_debug = ESS_LOG_WRITE('Status = ' || l_status)

/* Log a number — must convert to text first */
l_debug = ESS_LOG_WRITE('Months of service = ' || TO_CHAR(l_months))

/* Log a date — specify the format */
l_debug = ESS_LOG_WRITE('Hire date = ' || TO_CHAR(l_hire_date, 'DD-MON-YYYY'))

/* Log multiple values in one line */
l_debug = ESS_LOG_WRITE(
  'Person=' || l_person_number
  || ' | Hire=' || TO_CHAR(l_hire_date, 'DD-MON-YYYY')
  || ' | FTE=' || TO_CHAR(l_fte))
```

| Quick reference: TO_CHAR conversions |
| --- |
| `TO_CHAR(l_number)` — number to text |
| `TO_CHAR(l_date, 'DD-MON-YYYY')` — date to text |
| `TO_CHAR(l_date, 'DD/MM/YYYY HH24:MI:SS')` — date with time |

---

## Where to Find the Log Output

The messages only appear when the formula runs inside a scheduled process. Here's how to find them:

| Steps to view formula logs |
| --- |
| STEP 1
    Go to **Tools → Scheduled Processes** |
| STEP 2
    Find the process that ran your formula (e.g. **Evaluate Absence Management Accruals**) |
| STEP 3
    Click on the completed process → **View Log and Output** |
| STEP 4
    Search the log for your formula name or a unique string from your log messages |

ESS_LOG_WRITE messages only appear in ESS process logs — not in the formula editor, not in the browser console, and not in standard application logs. If you're testing from the formula editor's "Run" button, you won't see the output.

---

## Pattern 1: Section Markers

The most basic and most useful pattern. Wrap your formula in START and END markers so you can instantly find where your formula's output begins and ends in a log that might contain output from dozens of formulas:

```text
/* From an Annual Leave Carryover formula */

l_debug = ESS_LOG_WRITE(
  '******** Absence Carryover - Formula Start ********')

/* ... all formula logic here ... */

l_debug = ESS_LOG_WRITE(
  '******** Absence Carryover - Formula End ********')
```

In the ESS log, this looks like:

```text
... hundreds of other log lines ...
******** Absence Carryover - Formula Start ********
FTE: 1
Plan Name = DHB_REGULAR_25D
CarryOver Date: 23/01/2026
CarryOver From UDT: 5
CarryOver: 5
******** Absence Carryover - Formula End ********
... more log lines ...
```

Use the formula name in the markers — when multiple formulas run in the same process, you can search for yours instantly.

---

## Pattern 2: Variable Dump at Key Decision Points

Don't just log at the start and end. Log the values that feed into every IF/ELSE decision. When the result is wrong, the log tells you exactly which branch was taken and why:

```text
/* From a PH Vacation Leave Accrual formula */

l_debug = ESS_LOG_WRITE('=== PH Accrual Start ===')
l_debug = ESS_LOG_WRITE('Person: ' || PER_ASG_PERSON_NUMBER)
l_debug = ESS_LOG_WRITE('Hire date: '
  || TO_CHAR(l_hire_date, 'DD-MON-YYYY'))
l_debug = ESS_LOG_WRITE('Months of service: '
  || TO_CHAR(l_months))
l_debug = ESS_LOG_WRITE('Termination date: '
  || TO_CHAR(l_term_date, 'DD-MON-YYYY'))

/* Now the decision — log BEFORE and AFTER */
l_debug = ESS_LOG_WRITE('Checking phase...')

IF (l_months THEN
(
  l_debug = ESS_LOG_WRITE('Phase 1: PROBATION → accrual = 0')
  accrual = 0
)
ELSE IF (l_months THEN
(
  l_debug = ESS_LOG_WRITE('Phase 2: MONTHLY → accrual = 1.25')
  accrual = 1.25
)
ELSE
(
  l_debug = ESS_LOG_WRITE('Phase 3: ANNUAL → accrual = 15')
  accrual = 15
)

l_debug = ESS_LOG_WRITE('Final accrual = '
  || TO_CHAR(accrual))
l_debug = ESS_LOG_WRITE('=== PH Accrual End ===')
```

In the ESS log:

```text
=== PH Accrual Start ===
Person: 1042
Hire date: 15-JUL-2025
Months of service: 7
Termination date: 31-DEC-4712
Checking phase...
Phase 2: MONTHLY → accrual = 1.25
Final accrual = 1.25
=== PH Accrual End ===
```

Now if someone says "this employee should be getting 15 days, not 1.25" — you open the log and immediately see: months of service = 7, which triggered Phase 2 instead of Phase 3. The data tells the story.

---

## Pattern 3: Validation Pass/Fail Logging

For absence entry validation formulas, log the rule being checked, the values being compared, and whether it passed or failed:

```text
/* From a Leave Entry Validation formula */

l_debug = ESS_LOG_WRITE('=== Leave Validation Start ===')
l_debug = ESS_LOG_WRITE('Duration requested: '
  || TO_CHAR(l_duration) || ' days')
l_debug = ESS_LOG_WRITE('Max per instance: '
  || TO_CHAR(l_max_per_instance))
l_debug = ESS_LOG_WRITE('Year-to-date used: '
  || TO_CHAR(l_ytd_used))
l_debug = ESS_LOG_WRITE('Annual limit: '
  || TO_CHAR(l_annual_limit))

/* Rule 1: Single instance check */
IF (l_duration > l_max_per_instance) THEN
(
  l_debug = ESS_LOG_WRITE('FAIL: '
    || TO_CHAR(l_duration)
    || ' exceeds max '
    || TO_CHAR(l_max_per_instance))
  VALID = 'N'
)
ELSE
(
  l_debug = ESS_LOG_WRITE('PASS: Instance check OK')

  /* Rule 2: Annual limit check */
  IF (l_ytd_used + l_duration > l_annual_limit) THEN
  (
    l_debug = ESS_LOG_WRITE('FAIL: YTD '
      || TO_CHAR(l_ytd_used) || ' + '
      || TO_CHAR(l_duration) || ' = '
      || TO_CHAR(l_ytd_used + l_duration)
      || ' exceeds annual '
      || TO_CHAR(l_annual_limit))
    VALID = 'N'
  )
  ELSE
  (
    l_debug = ESS_LOG_WRITE('PASS: Annual limit check OK')
    VALID = 'Y'
  )
)
```

The ESS log for a failed validation:

```text
=== Leave Validation Start ===
Duration requested: 4 days
Max per instance: 3
Year-to-date used: 5
Annual limit: 7
FAIL: 4 exceeds max 3
=== Leave Validation End ===
```

One glance and you know exactly which rule failed and why. Without the log, you'd just see "leave request rejected" with no explanation of the data behind the decision.

---

## Pattern 4: Bracket Wrapping for Hidden Characters

One of the most frustrating bugs: a value looks correct in the log but doesn't match. The culprit is usually trailing spaces, invisible characters, or null values that display as blank. Wrap suspicious values in square brackets to expose them:

```text
/* Bad — can't see trailing spaces */
l_debug = ESS_LOG_WRITE('Plan name = ' || l_plan_name)
/* Log shows: Plan name = DHB_REGULAR_25D
   But actual value might be: DHB_REGULAR_25D   (with spaces) */

/* Good — brackets expose the exact value */
l_debug = ESS_LOG_WRITE('Plan name = [' || l_plan_name || ']')
/* Log shows: Plan name = [DHB_REGULAR_25D   ]
   Now you can see the trailing spaces! */

/* Also useful: log the length */
l_debug = ESS_LOG_WRITE('Plan name = [' || l_plan_name || '] length='
  || TO_CHAR(LENGTH(l_plan_name)))
```

This is especially useful when debugging UDT lookups and DBI values that don't match expected strings.

---

## Pattern 5: Loop Iteration Logging

When looping through array DBIs (as covered in the previous blog post), log each iteration with its index and values. Without this, you're blind to what the loop is actually processing:

```text
l_debug = ESS_LOG_WRITE('Array count: '
  || TO_CHAR(IV_EVENT_DATES.COUNT))

l_idx = IV_EVENT_DATES.FIRST(-1)
l_iteration = 0

WHILE l_idx <> -1
LOOP
(
  l_iteration = l_iteration + 1
  l_date    = IV_EVENT_DATES[l_idx]
  l_accrual = IV_ACCRUAL_VALUES[l_idx]

  l_debug = ESS_LOG_WRITE(
    '  Loop #' || TO_CHAR(l_iteration)
    || ' idx=' || TO_CHAR(l_idx)
    || ' date=' || TO_CHAR(l_date, 'DD-MON-YYYY')
    || ' accrual=' || TO_CHAR(l_accrual))

  l_idx = IV_EVENT_DATES.NEXT(l_idx, -1)
)

l_debug = ESS_LOG_WRITE('Loop complete. Iterations: '
  || TO_CHAR(l_iteration))
```

ESS log output:

```text
Array count: 3
  Loop #1 idx=1 date=01-JAN-2025 accrual=0
  Loop #2 idx=2 date=01-JUL-2025 accrual=1.25
  Loop #3 idx=3 date=01-JAN-2026 accrual=15
Loop complete. Iterations: 3
```

Notice the two-space indent on loop lines. Small detail, but it makes the log structure immediately scannable.

---

## Beyond ESS_LOG_WRITE: Other Debug Methods

ESS_LOG_WRITE is the most common method, but Oracle provides different debug functions depending on which module runs the formula. Here's the complete reference:

| Method | Module | Where logs appear |
| --- | --- | --- |
| `ESS_LOG_WRITE` | All modules (most common) | ESS process log |
| `PAY_INTERNAL_LOG_WRITE` | Payroll only | ESS log (with F flag for Payroll debug) |
| `ADD_RLOG` | OTL (Time and Labor) | OTL Rule Processing Details page |
| `ADD_LOG` | OTL (subset of ADD_RLOG) | OTL Rule Processing Details page |

Here's the syntax for each:

```text
/* ESS_LOG_WRITE — works everywhere, logs to ESS */
l_debug = ESS_LOG_WRITE('Test message')

/* PAY_INTERNAL_LOG_WRITE — Payroll only */
l_debug = PAY_INTERNAL_LOG_WRITE('Test message')
/* Enable with F flag in Payroll debug settings */

/* ADD_RLOG — OTL only, needs formula and rule IDs */
l_log = ADD_RLOG(ffs_id, rule_id, 'Test message')
/* ffs_id from context HWM_FFS_ID
   rule_id from context HWM_RULE_ID */

/* ADD_LOG — OTL shorthand (rule_id auto-determined) */
l_log = ADD_LOG(ffs_id, 'Test message')
```

### OTL Logging: Where to Find Logs

OTL formulas (Time Calculation Rules) use `ADD_RLOG` or `ADD_LOG` instead of ESS_LOG_WRITE. The logs don't go to the ESS process log — they go to a dedicated OTL page:

| Viewing OTL formula logs |
| --- |
| STEP 1
    Navigator → **Workforce Management** → **Time Management** |
| STEP 2
    Select **Analyze Rule Processing Details** |
| STEP 3
    Search by **Rule Set Name** → click the **Time Card Processing ID** |
| STEP 4
    View the **Rule Processing Log** on the detail page |

### Which Method Should You Use?

For most consultants, the decision is simple:

| If your formula runs in... | Use this |
| --- | --- |
| Absence, Compensation, Benefits, Core HR | `ESS_LOG_WRITE` |
| Payroll | `PAY_INTERNAL_LOG_WRITE` or `ESS_LOG_WRITE` |
| Time and Labor (OTL) | `ADD_LOG` or `ADD_RLOG` |

When in doubt, start with ESS_LOG_WRITE. It works across all modules and the logs are easy to find in Scheduled Processes. For Payroll, use PAY_INTERNAL_LOG_WRITE. For OTL, use ADD_LOG or ADD_RLOG. For formulas that don't generate any logs, use the ADD_RLOG trick in the next section.

---

## The Hidden Trick: Debugging Formulas That Don't Generate Logs

Some formula types don't run through a scheduled process at all. They fire from the UI — when a user submits a form, triggers a checklist, or enters a compensation value. Examples include Checklist formulas, Compensation Default and Validation formulas, and many others.

For these formulas, `ESS_LOG_WRITE` does nothing — there's no ESS process, so there's no log to write to. This is one of the most frustrating situations in Fast Formula development.

The workaround: use `ADD_RLOG` with a fake formula ID. Even though ADD_RLOG is designed for OTL, it writes to a database table that you can query directly from BI Publisher — regardless of which module triggered the formula.

Here's a full-scale example — a Compensation Validation formula with ADD_RLOG logging at every step:

```text
/* ********************************************************
   FORMULA: XX_COMP_SALARY_VALIDATION_FF
   TYPE:    Compensation Validation
   NOTE:    ESS_LOG_WRITE won't work here — this formula
            fires from the Compensation worksheet UI.
            Using ADD_RLOG to write to HWM_RULE_FF_WORK_LOG.
   ******************************************************** */

/* ========== DEFAULTS ========== */
DEFAULT FOR PER_ASG_PERSON_NUMBER IS 'UNKNOWN'
DEFAULT FOR PER_ASG_GRADE_NAME IS 'NO_GRADE'

/* ========== INPUTS ========== */
INPUTS ARE IV_PROPOSED_SALARY

/* ========== DEBUG SETUP ==========
   -999001 = unique fake ID for this formula
   seq     = increments to preserve log order */
l_ffs_id = -999001
seq = 1

/* ========== LOG: START ========== */
l = ADD_RLOG(l_ffs_id, seq,
  '======== XX_COMP_SALARY_VALIDATION Start ========')
seq = seq + 1

/* ========== LOG: INPUT VALUES ========== */
l_person = PER_ASG_PERSON_NUMBER
l_grade  = PER_ASG_GRADE_NAME

l = ADD_RLOG(l_ffs_id, seq,
  'Person: ' || l_person)
seq = seq + 1

l = ADD_RLOG(l_ffs_id, seq,
  'Grade: [' || l_grade || ']')
seq = seq + 1

l = ADD_RLOG(l_ffs_id, seq,
  'Proposed salary: ' || TO_CHAR(IV_PROPOSED_SALARY))
seq = seq + 1

/* ========== LOOKUP: Get salary range from UDT ========== */
l_min = TO_NUMBER(GET_TABLE_VALUE(
  'XX_SALARY_RANGE_UDT', 'MIN_SALARY', l_grade, '0'))
l_max = TO_NUMBER(GET_TABLE_VALUE(
  'XX_SALARY_RANGE_UDT', 'MAX_SALARY', l_grade, '0'))

l = ADD_RLOG(l_ffs_id, seq,
  'UDT range: min=' || TO_CHAR(l_min)
  || ' max=' || TO_CHAR(l_max))
seq = seq + 1

/* ========== VALIDATION ========== */
IF (l_min = 0 AND l_max = 0) THEN
(
  l = ADD_RLOG(l_ffs_id, seq,
    'WARN: No UDT row for grade [' || l_grade
    || '] — skipping validation')
  seq = seq + 1
  VALID = 'Y'
)
ELSE IF (IV_PROPOSED_SALARY THEN
(
  l = ADD_RLOG(l_ffs_id, seq,
    'FAIL: ' || TO_CHAR(IV_PROPOSED_SALARY)
    || ' below min ' || TO_CHAR(l_min))
  seq = seq + 1
  VALID = 'N'
  ERROR_MESSAGE = 'Salary below minimum for grade'
)
ELSE IF (IV_PROPOSED_SALARY > l_max) THEN
(
  l = ADD_RLOG(l_ffs_id, seq,
    'FAIL: ' || TO_CHAR(IV_PROPOSED_SALARY)
    || ' above max ' || TO_CHAR(l_max))
  seq = seq + 1
  VALID = 'N'
  ERROR_MESSAGE = 'Salary exceeds maximum for grade'
)
ELSE
(
  l = ADD_RLOG(l_ffs_id, seq,
    'PASS: Salary within range')
  seq = seq + 1
  VALID = 'Y'
)

/* ========== LOG: END ========== */
l = ADD_RLOG(l_ffs_id, seq,
  'Result: VALID=' || VALID)
seq = seq + 1

l = ADD_RLOG(l_ffs_id, seq,
  '======== XX_COMP_SALARY_VALIDATION End ========')

RETURN VALID
```

Key things to notice in the code above:

| ADD_RLOG anatomy |
| --- |
| `l_ffs_id = -999001` — a unique negative number for this formula. Use a different number for each formula you're debugging so logs don't mix. |
| `seq = seq + 1` — must increment after every ADD_RLOG call. Without this, log rows have the same sequence and the ORDER BY won't preserve your message order. |
| `l = ADD_RLOG(...)` — returns the number 1. Must assign to a variable (same pattern as ESS_LOG_WRITE). |
| **Bracket wrapping** — notice `'['` around the grade value. UDT lookups fail silently on trailing spaces — the brackets expose them. |

After the formula runs (when a manager submits a salary on the Compensation worksheet), query the logs from BI Publisher:

```text
SELECT log_text
FROM   HWM_RULE_FF_WORK_LOG
WHERE  ffs_id = -999001
ORDER BY log_id, rule_id
```

The query returns something like this:

```text
======== XX_COMP_SALARY_VALIDATION Start ========
Person: 1042
Grade: [IC3]
Proposed salary: 85000
UDT range: min=60000 max=95000
PASS: Salary within range
Result: VALID=Y
======== XX_COMP_SALARY_VALIDATION End ========
```

And for a failed validation:

```text
======== XX_COMP_SALARY_VALIDATION Start ========
Person: 2087
Grade: [IC5]
Proposed salary: 150000
UDT range: min=80000 max=120000
FAIL: 150000 above max 120000
Result: VALID=N
======== XX_COMP_SALARY_VALIDATION End ========
```

The logs accumulate in the table over time. To clean up, you have two options: raise an SR with Oracle to purge the rows, or add a cleanup step at the **start** of your formula that limits how many rows you keep. In practice, most consultants simply leave the logs — the table handles it. Just use different negative ffs_id values for different formulas so logs don't mix.

| When to use the ADD_RLOG trick |
| --- |
| **Checklist formulas** — triggered when a user opens or completes a checklist task |
| **Compensation Default & Validation formulas** — fire when a manager enters comp values on the worksheet |
| **Person Selection formulas** — triggered during eligibility checks from the UI |
| **Any formula that runs from the UI** — where ESS_LOG_WRITE produces no output |

This is the only way to get debug output from formulas that don't run through scheduled processes. Use a unique negative ffs_id for each formula you're debugging, and remember to clean up the table after debugging (or the logs accumulate).

---

## Oracle's Recommended Troubleshooting Steps

When a formula doesn't return the correct values, Oracle's official documentation recommends a systematic approach — start simple, then add complexity back:

| Diagnosis steps (in order) |
| --- |
| STEP 1 — Test seeded behavior first
    Remove your custom formula temporarily and test the seeded (out-of-the-box) functionality. This confirms whether the issue is in your formula or in the setup. |
| STEP 2 — Hardcode values
    Replace all DBI reads and function calls with hardcoded values. If the formula works with hardcoded values, the issue is in the data, not the logic. |
| STEP 3 — Replace functions with hardcoded values
    If your formula uses custom functions (SET_INPUT/EXECUTE/GET_OUTPUT), replace them one at a time with hardcoded values to isolate which function is returning unexpected data. |
| STEP 4 — Trace the formula
    Add ESS_LOG_WRITE (or the appropriate debug method) to trace every variable value at every decision point. This is where the logging patterns from this post come in. |
| STEP 5 — Provide results to Oracle Support
    If the above steps don't resolve the issue, document the results from each step and raise an SR with Oracle. The trace output from Step 4 will be the first thing they ask for. |

### Critical Warnings from Oracle Documentation

These are from Oracle's official Fast Formula administration guide — ignore them at your peril:

**Never delete a formula that's been attached to a Benefits plan design** — especially after the plan has been processed and participants have been found eligible. Deleting it will break the plan's processing chain.

**Never recreate a formula with the same name after deleting** — it doesn't reinstate the old behavior. You'll get runtime errors. Instead, edit the existing formula or create a new formula with a different name and reattach it.

---

## Best Practices

**Always use section markers** — START and END with the formula name. In a log with 50+ formulas running for 200+ employees, this is the only way to find your output.

**Log inputs before decisions** — dump every variable that feeds into an IF/ELSE before the condition is evaluated. When the result is wrong, the input values tell you why.

**Log which branch was taken** — inside every IF and ELSE block, log a message identifying which path executed. Don't make the reader guess from the data.

**Use brackets for string comparisons** — when a lookup or comparison fails unexpectedly, bracket-wrap both sides to expose trailing spaces and hidden characters.

**Include the person identifier** — when the process runs for multiple employees, include the person number or assignment number in at least the START marker so you can search for a specific person.

**Log the RETURN value** — always log the final value being returned, right before the RETURN statement. This confirms what the formula actually sent back, not what you think it sent back.

**Keep logs in production** — don't remove debug logging after go-live. You'll need it again when the first support ticket comes in. The performance impact of ESS_LOG_WRITE is negligible.

---

## Key Takeaways

**ESS_LOG_WRITE is your only debugging tool** — no debugger, no breakpoints, no watch window. Log everything you need to understand what happened.

**Must assign to a variable** — `l_debug = ESS_LOG_WRITE('...')` because the function returns a number.

**Convert non-text with TO_CHAR** — numbers need `TO_CHAR(n)`, dates need `TO_CHAR(d, 'DD-MON-YYYY')`.

**Find logs in Scheduled Processes** — Tools → Scheduled Processes → View Log and Output. Not visible from the formula editor.

**Five patterns to master** — section markers, variable dumps at decisions, pass/fail validation, bracket wrapping, and loop iteration logging.

A well-logged formula is a formula you can fix. A formula without logs is a formula you'll rewrite from scratch when something goes wrong six months after go-live.

|  | ### Abhishek Mohanty |
| --- | --- |
