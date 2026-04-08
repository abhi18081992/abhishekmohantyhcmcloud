---
title: "Oracle Fast Formula: NULL Doesn't Exist — Use WAS DEFAULTED"
description: "A big shoutout to Mr. Scott Klein — who, after reading my Fast Formula blog series, pointed out a concept that every developer searches for but never finds in the docs: how to check for NULL. This one's inspired by that conversation."
pubDate: 2026-03-22
tags: ["Fast Formula", "Fun Fact", "WAS DEFAULTED", "Must Know"]
---

A big shoutout to Mr. Scott Klein — who, after reading my Fast Formula blog series, pointed out a concept that every developer searches for but never finds in the docs: how to check for NULL. This one's inspired by that conversation.

Abhishek Mohanty

---

## The Problem Every Developer Runs Into

You come from SQL, PL/SQL, Java, or Python. You need to check if an employee has a termination date. You try everything you know:

| Background | What you try | Result |
| --- | --- | --- |
| SQL | IF l_term_date IS NULL THEN | ✘ Compile Error |
| PL/SQL | IF l_term_date = NULL THEN | ✘ Compile Error |
| Java | IF (l_term_date == null) | ✘ Compile Error |
| Guess | IF l_term_date IS EMPTY | ✘ Compile Error |
| Guess | IF l_grade_name = '' | ⚠ Compiles — but never matches |

You Google "fast formula null check" — and find nothing useful.

**Fun Fact:** There is no NULL *keyword* in Oracle Fast Formula. You can't write `IF x IS NULL` or `x = NULL`. And for DBIs declared with `DEFAULT FOR`, the engine never lets you see a null — it substitutes the default instead.

---

## How Fast Formula Handles Missing Data

The database absolutely has null values. An employee might not have a termination date, a grade, or a location. For DBIs declared with `DEFAULT FOR`, Fast Formula never lets you see the null directly — it uses a two-step mechanism instead:

### How the Fast Formula engine handles NULL — step by step

1

SELECT termination_date FROM per_all_assignments
→
NULL

▼ Engine intercepts the null before your formula sees it

2

NULL
→ replaced with →
31-Dec-4712

Internal flag set:
⚑ DEFAULTED = TRUE

▼ Your formula receives the default value — never sees null

3

IF PER_ASG_TERMINATION_DATE WAS DEFAULTED THEN**
  /* Engine checks flag → TRUE → database had null */

Result:
TRUE
→ you now know the database had null

### Two Scenarios, Same Formula

No termination date in the database

DATABASE
NULL

ENGINE REPLACES

FORMULA SEES
31-Dec-4712

INTERNAL FLAG
⚑ DEFAULTED = TRUE

WAS DEFAULTED?
TRUE ✔

Real termination date exists

DATABASE
15-Aug-2025

REAL VALUE — NO REPLACEMENT

FORMULA SEES
15-Aug-2025

INTERNAL FLAG
DEFAULTED = FALSE

WAS DEFAULTED?
FALSE ✘

Here's the mental model for DBIs and input values — translate what you know into what Fast Formula uses:

| In SQL / PL/SQL | In Fast Formula |
| --- | --- |
| ✘ IF x IS NULL | IF x WAS DEFAULTED ✔ |
| ✘ IF x IS NOT NULL | IF NOT x WAS DEFAULTED ✔ |

---

## Real Example: Is This Employee Terminated?

In absence accrual formulas, you need to check if the employee is still active. An active employee has no termination date in the database — that column is null. Here's how you check:

```text
/* Step 1: Declare a default for the termination date DBI.
   If the database has null, the engine will use this date. */
DEFAULT FOR PER_ASG_TERMINATION_DATE IS '4712/12/31 00:00:00' (date)

/* Step 2: Read the DBI. If the employee has no termination
   date, l_term_date will silently become 31-Dec-4712. */
l_term_date = PER_ASG_TERMINATION_DATE

/* Step 3: Check if it WAS DEFAULTED (= database had null) */
IF PER_ASG_TERMINATION_DATE WAS DEFAULTED THEN
(
    /* No termination date exists → employee is ACTIVE */
    l_debug = ESS_LOG_WRITE('Employee is active (no term date)')
    l_process = 'Y'
)
ELSE
(
    /* Real termination date exists → employee IS terminated */
    l_debug = ESS_LOG_WRITE('Terminated: '
              || TO_CHAR(l_term_date, 'DD-MON-YYYY'))
    l_process = 'N'
)
```

---

## It Works on Input Values Too

WAS DEFAULTED isn't limited to DBIs. It also works on input values — useful when the calling process doesn't always pass every input:

```text
DEFAULT FOR IV_OVERRIDE_AMOUNT IS 0

INPUTS ARE IV_OVERRIDE_AMOUNT

IF IV_OVERRIDE_AMOUNT WAS DEFAULTED THEN
(
    /* No override passed → use the calculated value */
    accrual = l_calculated_accrual
)
ELSE
(
    /* Override was explicitly passed → use it */
    accrual = IV_OVERRIDE_AMOUNT
)
```

Without WAS DEFAULTED, you couldn't distinguish between "the process passed 0 as the override" and "the process didn't pass an override at all." Both would show as 0 in the formula. WAS DEFAULTED tells you which case you're in.

---

## How to Check "IS NOT NULL" — The NOT Operator

Checking for null is one thing. But in most formulas, you actually want to check the opposite: "does this DBI have a real value?"** — the equivalent of SQL's `IF x IS NOT NULL`.

Oracle's documentation confirms that you can combine conditions using the logical operators **AND, OR, NOT**. From the **Oracle FastFormula User Guide**:

*"You can combine conditions using the logical operators AND, OR, NOT. Use NOT if you want an action to occur when a condition is not true."*

### WAS DEFAULTED vs NOT WAS DEFAULTED — Visual

Database had no value

IF MY_DBI WAS DEFAULTED THEN

Database:
NULL

Engine flag:
⚑ DEFAULTED

Condition:
TRUE → enters THEN

Database had a real value

IF NOT MY_DBI WAS DEFAULTED THEN

Database:
Grade A

Engine flag:
NOT DEFAULTED

Condition:
TRUE → enters THEN

Fast Formula supports two valid syntaxes for the NOT NULL check:

| Syntax | Style | Valid? |
| --- | --- | --- |
| IF NOT MY_DBI WAS DEFAULTED | NOT operator before the DBI name | ✔ |
| IF MY_DBI WAS NOT DEFAULTED | WAS NOT DEFAULTED as one comparator | ✔ |

Both compile and both work. Use whichever reads more naturally to you.

### Real Example: Only Process Workers Who Have a Grade

```text
DEFAULT FOR PER_ASG_GRADE_NAME IS 'NO_GRADE'

l_grade = PER_ASG_GRADE_NAME

/* IS NOT NULL check — only process if grade exists */
IF NOT PER_ASG_GRADE_NAME WAS DEFAULTED THEN
(
    /* Grade has a real value — process it */
    l_debug = ESS_LOG_WRITE('Grade: ' || l_grade)
    l_process = 'Y'
)
ELSE
(
    /* Grade is null in the database — skip */
    l_debug = ESS_LOG_WRITE('No grade assigned — skipping')
    l_process = 'N'
)
```

### Real Example: Use Work-Relationship Hire Date, Fall Back to Enterprise Hire Date

```text
DEFAULT FOR PER_ASG_REL_ORIGINAL_DATE_OF_HIRE IS '1900/01/01 00:00:00' (date)
DEFAULT FOR PER_PERSON_ENTERPRISE_HIRE_DATE IS '1900/01/01 00:00:00' (date)

/* Prefer work-relationship original hire date if it exists (IS NOT NULL) */
IF NOT PER_ASG_REL_ORIGINAL_DATE_OF_HIRE WAS DEFAULTED THEN
(
    l_anchor_date = PER_ASG_REL_ORIGINAL_DATE_OF_HIRE
    l_debug = ESS_LOG_WRITE('Using work-relationship original hire date')
)
ELSE
(
    /* No work-relationship hire date — fall back to enterprise hire date */
    l_anchor_date = PER_PERSON_ENTERPRISE_HIRE_DATE
    l_debug = ESS_LOG_WRITE('Falling back to enterprise hire date')
)
```

This is a common pattern in absence accrual formulas — the work-relationship original hire date isn't always populated (especially for migrated employees or post-Global Transfer scenarios), so you check if it has a real value before using it. If it's null (WAS DEFAULTED), fall back to the enterprise hire date.

### Combining NOT with AND / OR

You can combine `NOT WAS DEFAULTED` with other conditions using AND and OR:

```text
/* Only check the state if the DBI actually has data */
IF (NOT PER_ASG_LOC_REGION2 WAS DEFAULTED AND
    PER_ASG_LOC_REGION2 != 'PR' AND
    PER_ASG_LOC_REGION2 != 'DC') THEN
(
    eligible = 'Y'
)
```

Oracle's docs note that `NOT` has the **highest precedence** among logical operators. Here's the evaluation order:

So `NOT PER_ASG_LOC_REGION2 WAS DEFAULTED AND ...` evaluates the NOT first, then the AND — which is exactly what we want.

### Quick Reference

SQL

↓

FAST FORMULA

SQL

↓

FAST FORMULA

ALTERNATE SYNTAX

↓

FAST FORMULA

---

## Common Mistakes

MISTAKE 1: Checking the value instead of WAS DEFAULTED

`IF l_term_date = '4712/12/31'` — This compares against the default value, but what if someone's actual date happens to be that value? Always use WAS DEFAULTED instead.

MISTAKE 2: Forgetting the DEFAULT declaration

If you don't declare a DEFAULT and the DBI returns null, the formula **crashes at runtime**. No compile error — it compiles fine. The crash happens when the process runs for an employee whose data is null.

MISTAKE 3: Using WAS DEFAULTED on a variable

WAS DEFAULTED only works on **DBIs and input values** — not on local variables. `IF l_my_var WAS DEFAULTED` doesn't give you the answer you want, because the engine's internal default-substitution flag is only set on DBIs and inputs that have a `DEFAULT` declaration. Local variables don't carry that flag.

---

## The Cheat Sheet

Next time you need to check for null in Fast Formula, follow this pattern:

```text
/* 1. Declare a default */
DEFAULT FOR MY_DBI_NAME IS 'some_safe_value'

/* 2. Read the value */
l_value = MY_DBI_NAME

/* 3. Check if it was null in the database */
IF MY_DBI_NAME WAS DEFAULTED THEN
(
    /* database had NULL */
)
ELSE
(
    /* database had a real value */
)
```

That's it. Three lines replace what every other language does with `IS NULL`.

**DEFAULT** is not just a safety net. **DEFAULT + WAS DEFAULTED** together are Fast Formula's null-handling system for DBIs and input values. If you're coming from SQL or PL/SQL and looking for IS NULL on a DBI — this is it.

---

## What Oracle Documentation Says

This isn't a workaround or a hack — it's Oracle's official design. Here's what the docs say:

From Oracle's official Fast Formula documentation

**Oracle HRMS FastFormula User Guide*****"There is a special comparator called WAS DEFAULTED that you can use to test database items and input values. If there is no value available for an input value or database item, the formula uses a default value. The condition containing the WAS DEFAULTED comparator is True if a default value was used."*

Oracle Cloud HCM — Understanding Fast Formula Structure*****"You can use the WAS DEFAULTED statement to determine if a database item or input is null."*

Critical warning from Oracle:** *"You must use the Default statement for database items that can be empty."*

Translation: if you skip the DEFAULT and the DBI returns null, your formula crashes at runtime.

---

Hope this helps someone.

Abhishek Mohanty
