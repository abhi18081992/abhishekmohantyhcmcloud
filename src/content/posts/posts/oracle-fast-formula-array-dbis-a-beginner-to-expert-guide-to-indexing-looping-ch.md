---
title: "Oracle Fast Formula Array DBIs: A Beginner-to-Expert Guide to Indexing, Looping & CHANGE_CONTEXTS"
description: "Most Fast Formulas work with single values — one hire date, one assignment status, one accrual amount. But what happens when a person has multiple assignments, multiple date-tracked rows, or matrix bands with multiple accrual tiers? That's "
pubDate: 2026-03-16
tags: ["Fast Formula", "Array DBIs", "Advanced"]
---

Most Fast Formulas work with single values — one hire date, one assignment status, one accrual amount. But what happens when a person has multiple assignments, multiple date-tracked rows, or matrix bands with multiple accrual tiers? That's where Array Database Items come in — and they change everything about how formula logic works.

|  | Abhishek Mohanty |
| --- | --- |

In the previous posts, we covered the 7 pillars of Fast Formula and saw them in action with a single-value accrual formula. But single-value DBIs only get you so far. The moment your business logic needs to iterate over multiple records, you need **Array DBIs**.

This post covers how arrays work in Oracle HCM Cloud Fast Formula, the functions available to traverse them, and real examples using the PH Vacation Leave Accrual Matrix formula.

---

## What Are Array DBIs?

A regular DBI is like a single cell in a spreadsheet — it holds one value. An array DBI is like an entire column — it holds many values, each sitting in a numbered row.

How to tell the difference? Look at the data type. Single-value DBIs have types like DATE, NUMBER, or TEXT. Array DBIs have **two-part types**:

| DBI Type | Meaning | Example |
| --- | --- | --- |
| `NUMBER_NUMBER` | Number indexed by number | Assignment IDs |
| `DATE_NUMBER` | Date indexed by number | Start dates |
| `TEXT_NUMBER` | Text indexed by number | Statuses |

Two data types separated by an underscore = array. The first part is the value type, the second is how it's indexed.

---

## Where Can Arrays Be Used?

Arrays appear in four places within Fast Formula:

| Database Items | Read multiple rows from HR tables |
| --- | --- |
| Input Values | Receive arrays from the calling process |
| Variables | Create and manipulate arrays inside formulas |
| Return Values | Send arrays back to the calling process |

**Limitation:** Functions cannot return array values. Arrays work everywhere else, but seeded or custom functions cannot output them.

---

## How Array Indexing Works

If you've worked with arrays in C or any programming language, the concept is familiar. An array stores multiple values and you access each one using an index number in square brackets:

```text
/* In C programming */
int salary[3] = {40000, 25000, 60000};

salary[0]  →  40000
salary[1]  →  25000
salary[2]  →  60000
```

Fast Formula arrays work the same way — with two key differences:

|  | C | Fast Formula |
| --- | --- | --- |
| Index starts at | 0 | 1 (or any number) |
| Indexes are | Always 0, 1, 2, 3... | Can have gaps: 5, 12, 47 |
| Access syntax | `array[0]` | `array[1]` |
| Navigate with | for (i=0; i -1
LOOP
(
  /* Read the value at this row */
  l_value = my_array[l_idx]

  /* Move to next row */
  l_idx = my_array.NEXT(l_idx, -1)
)
```

| What each line does |
| --- |
| `.FIRST(-1)` | Jump to the first row. If array is empty, return -1. |
| `WHILE l_idx <> -1` | Keep looping as long as there are rows left. |
| `my_array[l_idx]` | Read the value at the current row number. |
| `.NEXT(l_idx, -1)` | Move to the next row. If at the end, return -1 → loop stops. |

---

## Tracing the Loop Step by Step

Let's trace exactly what happens when the loop runs against our PH formula's matrix bands:

| Data passed by the accrual engine |
| --- |
| Index | Event Date | Accrual |
| 1 | 01-Jan-25 | 0 |
| 2 | 01-Jul-25 | 1.25 |
| 3 | 01-Jan-26 | 15 |

The loop code:

```text
l_idx = IV_EVENT_DATES.FIRST(-1)

WHILE l_idx <> -1
LOOP
(
  l_date    = IV_EVENT_DATES[l_idx]
  l_accrual = IV_ACCRUAL_VALUES[l_idx]

  l_log = ESS_LOG_WRITE(
    'Band ' || TO_CHAR(l_idx)
    || ' date=' || TO_CHAR(l_date, 'DD-MON-YYYY')
    || ' accrual=' || TO_CHAR(l_accrual))

  l_idx = IV_EVENT_DATES.NEXT(l_idx, -1)
)
```

Here's what happens at each step:

| Execution trace |
| --- |
| BEFORE THE LOOP
    `.FIRST(-1)` → **l_idx = 1**
    First row exists. 1 ≠ -1 → enter loop. |
| ITERATION 1 — index = 1

      idx=1
      2
      3

    Reads: date = **01-Jan-25**, accrual = **0**
    `.NEXT(1, -1)` → **l_idx = 2** → continue |
| ITERATION 2 — index = 2

      1
      idx=2
      3

    Reads: date = **01-Jul-25**, accrual = **1.25**
    `.NEXT(2, -1)` → **l_idx = 3** → continue |
| ITERATION 3 — index = 3

      1
      2
      idx=3

    Reads: date = **01-Jan-26**, accrual = **15**
    `.NEXT(3, -1)` → **l_idx = -1** (no more rows) |
| EXIT
    **-1 ≠ -1** → false → loop ends. |

Three things to notice:

**The index variable does double duty** — it holds the current position AND controls whether the loop continues. When NEXT returns -1, both the data access and the loop exit are handled by the same variable.

**NEXT must be the last line inside the loop** — if placed at the top, the first row gets skipped. If placed in the middle, code below it runs with the wrong index.

**Empty array? Loop never runs** — if FIRST returns -1, the WHILE condition is immediately false. No iterations, no errors.

## The Same-Route Rule

When looping through one array and reading values from other arrays at the same row number, all those arrays **must come from the same route** (the same underlying data source).

If they don't, Row 1 in one array might describe a completely different record than Row 1 in another. The formula won't error — it will just silently return wrong results.

Same route = rows line up. Different route = data mismatch. Always verify your array DBIs share the same route before cross-referencing at the same index.

---

## Arrays in the PH Vacation Leave Accrual Formula

The accrual engine passes two arrays to our formula. These represent the **bands** from the absence plan's matrix configuration:

| Matrix bands passed to the formula |
| --- |
| Band | Event Date | Accrual Value |
| 1 | 01-Jan-2025 | 0 (probation) |
| 2 | 01-Jul-2025 | 1.25 per month |
| 3 | 01-Jan-2026 | 15 (lump sum) |

Our formula ignores these and calculates accrual using custom phase logic. But we **still must declare and default them** — otherwise the formula crashes:

```text
/* "Empty array" constants — FF's way of defaulting arrays */
DEFAULT FOR IV_EVENT_DATES IS EMPTY_DATE_NUMBER
DEFAULT FOR IV_ACCRUAL_VALUES IS EMPTY_NUMBER_NUMBER

INPUTS ARE
  IV_ACCRUAL,
  IV_EVENT_DATES              (DATE_NUMBER),
  IV_ACCRUAL_VALUES           (NUMBER_NUMBER)
```

| What each line does |
| --- |
| `EMPTY_DATE_NUMBER` | Built-in constant = "this array has zero rows" |
| `EMPTY_NUMBER_NUMBER` | Same, but for numeric arrays |
| `(DATE_NUMBER)` | Declares the input as a date array, not a single date |

---

## CHANGE_CONTEXTS: Checking Data at a Different Date

Every absence accrual formula receives a set of **contexts** from the accrual engine before it runs. One of the most important is `EFFECTIVE_DATE` — it tells every DBI "return data as of this date."

The engine also passes input values like `IV_ACCRUAL_START_DATE` (the first day of the current accrual period) and `IV_ACCRUAL_END_DATE` (the last day). The EFFECTIVE_DATE context is usually set to the **period end date**.

This means when the formula reads any DBI — like hire date, FTE, or assignment status — it gets the value as of the **last day** of the period. That's fine most of the time. But what if an employee changed from part-time to full-time mid-month? The formula would only see the end-of-month FTE (1.0) and miss that they were part-time (0.5) at the start.

`CHANGE_CONTEXTS` solves this. It temporarily overrides a context value, lets you read DBIs at a different point in time, then automatically reverts when the block ends.

Here's the scenario: January 2026 accrual period. The engine sets EFFECTIVE_DATE to 31-Jan-2026. We want to check whether the FTE changed during the month.

```text
/* These are passed by the accrual engine: */
/* EFFECTIVE_DATE context = 31-Jan-2026 (period end) */
/* IV_ACCRUAL_START_DATE  = 01-Jan-2026 (period start) */
/* IV_ACCRUAL_END_DATE    = 31-Jan-2026 (period end) */

/* Step 1: Read the FTE at period END (uses EFFECTIVE_DATE) */
l_current_fte = PER_ASG_FTE_VALUE
/* → 1.0 (full-time as of 31-Jan-2026) */

/* Step 2: Temporarily switch to period START date */
CHANGE_CONTEXTS(EFFECTIVE_DATE = IV_ACCRUAL_START_DATE)
(
  /* Now all DBIs return data as of 01-Jan-2026 */
  l_start_fte = PER_ASG_FTE_VALUE
  /* → 0.5 (was part-time at start of month) */
)
/* Context automatically reverts to 31-Jan-2026 here */

/* Step 3: Compare and decide */
IF (l_start_fte <> l_current_fte) THEN
(
  /* FTE changed during the month — prorate */
  accrual = 1.25 * l_current_fte
)
ELSE
(
  /* No change — standard accrual */
  accrual = 1.25
)
```

Here's what happened step by step:

| January 2026 accrual period |
| --- |
| Step 1 — Read at period end | EFFECTIVE_DATE = **31-Jan-2026** (set by engine)PER_ASG_FTE_VALUE returns **1.0** (full-time now) |
| Step 2 — CHANGE_CONTEXTS | Temporarily switches to **01-Jan-2026** (IV_ACCRUAL_START_DATE)PER_ASG_FTE_VALUE now returns **0.5** (part-time at month start) |
| Step 3 — Auto revert | Context reverts to **31-Jan-2026** automaticallyNo manual cleanup needed |
| Result | FTE changed 0.5 → 1.0 mid-month → prorate: **1.25 × 1.0 = 1.25 days** |

CHANGE_CONTEXTS works with any context the formula has access to. In absence formulas, EFFECTIVE_DATE is the most common one to override — it lets you "time-travel" to any date and read what the data looked like then.

---

## Bonus: The DBI X-Ray Query

Ever wondered what actually happens when your formula reads a DBI? There's a SQL query that lets you see exactly how Oracle resolves any Database Item — what table it reads from, what joins it performs, and which contexts it needs.

```text
SELECT d.base_user_name         DBI_NAME
,      d.data_type               DBI_DATA_TYPE
,      d.definition_text         SELECT_CLAUSE
,      r.text                    WHERE_CLAUSE
,      (SELECT LISTAGG(
         ' || rcu.sequence_no || ','
         || c.base_context_name || '>', ', ')
         WITHIN GROUP (ORDER BY rcu.sequence_no)
       FROM   ff_route_context_usages rcu
       ,      ff_contexts_b c
       WHERE  rcu.route_id = r.route_id
       AND    rcu.context_id = c.context_id
       )                         ROUTE_CONTEXT_USAGES
FROM   ff_database_items_b d
,      ff_user_entities_b u
,      ff_routes_b r
WHERE  d.base_user_name = 'PER_ASG_LOCATION_NAME'
AND    d.user_entity_id = u.user_entity_id
AND    r.route_id = u.route_id
```

Run this in BI Publisher or any SQL tool connected to your HCM Cloud database. Replace `PER_ASG_LOCATION_NAME` with any DBI name to see its internals. Here's what each column returns:

| What the query returns |
| --- |
| DBI_NAME | The DBI you searched for |
| DBI_DATA_TYPE | T = text, N = number, D = date. Two-part type means array. |
| SELECT_CLAUSE | The actual column expression Oracle reads — this is the value your formula gets. |
| WHERE_CLAUSE | The full route SQL — tables, joins, filters, bind variables. This controls which row gets returned. |
| ROUTE_CONTEXT_USAGES | Which contexts the route needs and their bind order. |

### Real Output: PER_ASG_LOCATION_NAME

Here's what the query actually returned when run in BI Publisher:

| Actual result from Oracle HCM Cloud |
| --- |
| DBI_NAMEPER_ASG_LOCATION_NAME |
| DBI_DATA_TYPET (Text — single value, not an array) |
| SELECT_CLAUSE`hrloc.location_name`
    Reads the location_name column from the hr_locations table (aliased as hrloc) |
| ROUTE_CONTEXT_USAGES
    , |

### Decoding the Bind Variables

The ROUTE_CONTEXT_USAGES column is to determine the route for DBI. It tells you which context maps to which bind variable in the WHERE clause:

| How bind variables connect to contexts |
| --- |
| Bind Variable | Context | What it does in the WHERE clause |
| `&B1` | HR_ASSIGNMENT_ID | Filters to the specific assignment |
| `&B2` | EFFECTIVE_DATE | Filters date-tracked rows to the right date |

The sequence number tells you which bind variable (`&B1`, `&B2`) in the WHERE clause maps to which context. So `&B1` = HR_ASSIGNMENT_ID, `&B2` = EFFECTIVE_DATE.

### Why This Matters for Array DBIs

Remember the same-route rule from earlier? When looping through an array and reading other array DBIs at the same index, they all must share the same route. But how do you **verify** that two DBIs share a route?

Run this query for each DBI. If the WHERE_CLAUSE is identical, they share the same route — and their indexes are aligned. If the WHERE_CLAUSE is different, they come from different SQL queries, and the same index might point to completely different records.

| STEP 1Run the query for the DBI you're looping throughExample: PER_ASG_ASSIGNMENT_ID → note the WHERE_CLAUSE |
| --- |
| STEP 2Run it again for the DBI you want to cross-reference
    Example: PER_ASG_STATUS_TYPE → compare the WHERE_CLAUSE |
| SAME WHERE_CLAUSE?
    Same route → indexes are aligned → safe to use at the same index |
| DIFFERENT WHERE_CLAUSE?Different route → indexes don't match → do not cross-reference |

This is the practical way to apply the same-route rule. Instead of guessing whether two array DBIs are aligned, you can confirm it in SQL before writing a single line of formula code.

This query is your debugging tool. When a DBI returns unexpected data, it shows you the exact SQL Oracle runs. When building array loops, it lets you verify the same-route rule. Swap the DBI name and run it for any Database Item.

---

## Key Takeaways

**Two-part type = array** — NUMBER_NUMBER, DATE_NUMBER, TEXT_NUMBER. Single types are single-value.

**FIRST and NEXT are your loop** — start with .FIRST(-1), advance with .NEXT(idx, -1), stop when you get -1.

**Same route or wrong data** — when cross-referencing arrays at the same index, they must share the same route.

**Declare arrays even if unused** — IV_EVENT_DATES and IV_ACCRUAL_VALUES must be declared with defaults or the formula crashes.

**CHANGE_CONTEXTS for time-travel** — temporarily switch the effective date to read DBI values at a different point in time.

**Functions can't return arrays** — arrays work as DBIs, inputs, variables, and returns, but not as function outputs.

Array DBIs unlock the ability to work with multi-row data in Oracle HCM Cloud Fast Formula. Master the FIRST → NEXT loop pattern and the same-route rule, and you can handle virtually any multi-row scenario.

|  | ### Abhishek Mohanty |
| --- | --- |
