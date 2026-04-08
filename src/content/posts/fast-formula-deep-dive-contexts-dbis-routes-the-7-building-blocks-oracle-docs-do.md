---
title: "Fast Formula Deep Dive: Contexts, DBIs, Routes & the 7 Building Blocks Oracle Docs Don't Explain Clearly"
description: "If you've ever tried to write a Fast Formula and wondered what the difference is between a Context, an Input Value, and a Database Item — this post is for you. Let's break down the 7 core building blocks that every FF developer needs to und"
pubDate: 2026-03-14
tags: ["Fast Formula", "Fundamentals"]
---

If you've ever tried to write a Fast Formula and wondered what the difference is between a Context, an Input Value, and a Database Item — this post is for you. Let's break down the 7 core building blocks that every FF developer needs to understand before writing a single line of formula code.

Abhishek Mohanty

Oracle HCM Cloud Consultant & Technical Lead

Before you can write production-ready Fast Formulas in Oracle Fusion HCM Cloud, you need to understand the building blocks that the formula engine relies on. These aren't just theoretical concepts — every compilation error, every runtime failure, and every unexpected result traces back to one of these components being misunderstood or misused.

In this post, I'll walk through the **7 default components of Oracle Fast Formula** — what they are, how they relate to each other, and the practical details that Oracle docs don't always make obvious.

---

## 1. Formula Type

Every Fast Formula belongs to a **Formula Type**. Think of it as the category or classification of the formula. You simply cannot create a formula without selecting a type first — the editor won't let you.

But formula type isn't just an administrative label. It determines everything downstream:

🔹 Which **Contexts** are available to the formula**🔹 Which Input Values** the engine will pass in**🔹 Which Database Items** you can reference**🔹 Where in the product the formula can be attached**

⚠️

Common Mistake

A frequent beginner error is creating a formula under the wrong type. For example, creating a formula with the **Compensation Default and Override Rule** type and then expecting to attach it to a Total Compensation Item — it won't show up. The field that uses the formula restricts selection based on type. Always know your type before you start coding.

---

## 2. Context

A Context is a **predefined parameter value** passed to the formula by the engine at runtime. You don't define contexts — Oracle does. They are tied to the formula type itself.

When Oracle created each formula type, they also defined which contexts would be available. So if you know the formula type, you automatically know what context parameters you'll receive.

Common contexts include:

| Context | What It Provides |
| --- | --- |
| `PERSON_ID` | Identifies which person the formula is processing |
| `HR_ASSIGNMENT_ID` | Identifies the specific assignment record |
| `EFFECTIVE_DATE` | The date for which the formula runs |
| `LEGAL_ENTITY_ID` | The legal entity associated with the assignment |

The critical role of Context: it determines the "who" and "when" of your formula. When a Database Item like PER_ASG_REL_ORIGINAL_DATE_OF_HIRE returns a hire date, how does it know whose hire date? The Context (PERSON_ID / HR_ASSIGNMENT_ID) tells it.

You retrieve context values in your formula using the `GET_CONTEXT()` function:

```text
l_person_id = GET_CONTEXT(PERSON_ID, 0)

l_assignment_id = GET_CONTEXT(HR_ASSIGNMENT_ID, 0)
```

---

## 3. Input Values

Input Values are also parameters passed to the formula — but there's a key difference from Contexts. **Input Values are not predefined by Oracle.** They represent additional information that the developer (or the calling process) decides to pass into the formula at execution time.

Because they're not predefined in Oracle's metadata tables, you won't find them by querying the database. The **only way to know what Input Values are available** for a given formula type is to read the Oracle documentation — specifically the Fast Formula Reference Guide.

📖

Context vs Input Value — What's the Difference?

**Context:** Predefined by Oracle with the formula type. Available in metadata. Determines which Database Items work.**Input Value:** Defined by the developer or calling process. Not in metadata. Additional info passed at runtime. Must read the docs to know what's available.

Input values are declared in your formula with the `INPUTS ARE` statement and always prefixed with `IV_`:

```text
INPUTS ARE

  IV_ACCRUAL,

  IV_ACCRUALPERIODSTARTDATE  (DATE),

  IV_ACCRUALPERIODENDDATE    (DATE)
```

---

## 4. Database Items (DBIs)

Database Items are essentially **predefined variables that hold values from HR tables**. Think of them as Oracle's way of giving your formula read access to employee data without writing SQL.

Each DBI holds one type of value. For example:

| Database Item | What It Returns |
| --- | --- |
| `PER_PER_FIRST_NAME` | Person's first name |
| `PER_PER_LAST_NAME` | Person's last name |
| `PER_ASG_REL_ORIGINAL_DATE_OF_HIRE` | Original hire date |
| `PER_ASG_STATUS_USER_STATUS` | Assignment status (e.g. 'ACTIVE') |

**Two types of Database Items exist:**

🔹 **Single-value DBIs** — return one value (e.g., a person's first name)**🔹 Range (array) DBIs** — return multiple values of the same type (e.g., a list of element entries)

Key concept: The value a DBI returns is determined by the Context. If the context passes PERSON_ID = 12345, then PER_PER_FIRST_NAME returns the first name of person 12345. Without context, the DBI has no idea whose data to fetch.

---

## 5. Routes

Routes are the **source behind Database Items**. If a DBI is the variable, the Route is the SQL query that populates it. Think of it as the table or SELECT statement that tells the engine where to fetch the data from.

Here's how Routes, Contexts, and DBIs connect:

```text
/* Conceptually, this is what happens behind the scenes: */

Database Item:  PER_PER_FIRST_NAME

Route (Source): PER_PERSONS table

Context (WHERE): WHERE person_id = CONTEXT(PERSON_ID)

/* The context acts as the WHERE clause that restricts

   which row the route (table) returns data from */
```

You'll never need to define routes yourself — they're part of Oracle's internal metadata. But understanding that they exist helps you debug when a DBI returns unexpected data. If a DBI isn't returning what you expect, it's usually because the context isn't set correctly, which means the route is querying the wrong row.

---

## 6. Functions

Functions in Fast Formula come in **two categories**:

🟢 **Seeded (Oracle-provided) functions** — built-in functions you can use directly. These include TO_CHAR, TO_NUMBER, TO_DATE, ADD_MONTHS, MONTHS_BETWEEN, DAYS_BETWEEN, ESS_LOG_WRITE, GET_CONTEXT, and many more.**
🔴 Custom (user-defined) functions** — in the E-Business Suite (EBS) on-premise world, customers could create their own functions by accessing the function definition tables and linking PL/SQL code. **This is NOT available in Oracle Cloud.**

☁️

Cloud Limitation

In Oracle Fusion Cloud, you **cannot create custom functions** because you don't have direct database access. You can only use the seeded functions that Oracle provides. This is a major difference from EBS and on-premise deployments where customers had the ability to create and register their own functions.

---

## 7. Return Variables

The final component is the **Return Variable** — the value(s) your formula sends back to the calling process. This is where many beginners get tripped up, because the rules around return variables are inconsistent across formula types.

There are **three patterns** for how return variables work:

Pattern 1: Variable Name Doesn't Matter

When the formula returns a single character value (like 'Y' or 'N'), most calling processes don't care what you name the variable. They just grab whatever character value comes back. You could name it `RETVAL`, `RESULT`, or anything — it works.

Pattern 2: Variable Name Is Critical

Some formula types require a **specific variable name**. The classic example is the **Benefits Eligibility** formula — the return variable *must* be called `ELIGIBLE` (in capitals). If you return the right value ('Y' or 'N') but in a differently-named variable, the engine either throws an error or falls back to default behavior.

Pattern 3: Multiple Named Return Variables

When returning multiple values (e.g., in a Total Compensation Item formula), each value has a **specific variable name** — one for date, one for value, one for assignment ID, one for legal employer, etc. The order doesn't matter, but the names do. The engine maps return values by variable name, not position.

```text
/* Pattern 1: Name doesn't matter */

RETVAL = 'Y'

RETURN RETVAL

/* Pattern 2: Name MUST be 'ELIGIBLE' */

ELIGIBLE = 'Y'

RETURN ELIGIBLE

/* Pattern 3: Multiple named variables */

COMPENSATION_DATES = '2026/01/31'

VALUES = '50000'

LEGALEMPLOYERS = '301'

ASSIGNMENTS = '12345'

RETURN COMPENSATION_DATES, VALUES, LEGALEMPLOYERS, ASSIGNMENTS
```

📖

Where to Find This Information

The FF engine doesn't enforce variable names — the **calling product** does. So the docs for each product (Benefits, Compensation, Absence, etc.) tell you what variable names they expect. Always check the **Oracle Fast Formula Reference Guide** for your specific formula type.

One more thing on return values: even when the variable name doesn't matter, the **format often does**. Most products expect dates in `YYYY/MM/DD` format. Always check the docs for the expected format of each return value.

---

## Bonus: User Entities

User Entities are a grouping mechanism for Database Items, primarily used in **HCM Extract** formulas. They bundle related DBIs together for extract operations. For most FF developers working on absence, compensation, or payroll formulas, you won't interact with User Entities directly — but it's worth knowing they exist as part of the component architecture.

---

---

## Putting It All Together

Here's how all 7 components connect in the Fast Formula engine:

    FORMULA TYPE

    determines

    ▶

    CONTEXTS

    available

    CONTEXTS

    act as WHERE clause for

    ▶

    ROUTES

    ROUTES

    return data into

    ▶

    DATABASE ITEMS

    INPUT VALUES

    ◀

    additional params from the calling process

    FUNCTIONS

    ◀

    built-in operations (TO_CHAR, DAYS_BETWEEN, etc.)

    Your formula logic

    ▶

    RETURN VARIABLES

    (output)

| Component | Predefined? | Where to Find Info |
| --- | --- | --- |
| Formula Type | Yes, by Oracle | Formula editor dropdown |
| Contexts | Yes, tied to type | Oracle metadata / docs |
| Input Values | No, developer-defined | FF Reference Guide only |
| Database Items | Yes, by Oracle | DBI lookup in formula editor |
| Routes | Yes, internal | Not user-facing |
| Functions | Yes (Cloud: seeded only) | FF Reference Guide |
| Return Variables | Depends on type | Product-specific docs |

---

## Key Takeaways

Understanding these 7 components before writing your first line of formula code will save you hours of debugging. The most common FF issues — compilation errors, missing data, wrong return values — almost always trace back to one of these being misunderstood.

Recommendations for FF Beginners

1

**Always identify your Formula Type first** — everything else flows from it

2

**Read the FF Reference Guide** for your formula type before coding — it tells you available contexts, input values, and expected return variables

3

**DEFAULT every DBI and Input Value** — no nulls in FF, missing defaults cause hard runtime errors

4

**Check exact return variable names** — some are strict (ELIGIBLE for Benefits), others are flexible

5

**No custom functions in Cloud** — plan your logic using seeded functions only (unlike EBS where you could register PL/SQL)

In the next post, we'll dive deeper into the formula syntax and walk through a real formula line by line. Stay tuned.

### Abhishek Mohanty

Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Core HR, Redwood, HDL, OTBI.
