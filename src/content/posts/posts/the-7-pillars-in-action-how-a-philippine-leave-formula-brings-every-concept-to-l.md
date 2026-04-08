---
title: "The 7 Pillars in Action: How a Philippine Leave Formula Brings Every Concept to Life"
description: "You can't write a formula without a Formula Type. You can't attach it without knowing which column expects it. And you can't debug it without understanding the contexts and input variables tied to it. In this post, I'll use a real-world Abs"
pubDate: 2026-03-16
tags: ["Fast Formula", "Formula Types", "Hands-On"]
---

You can't write a formula without a Formula Type. You can't attach it without knowing which column expects it. And you can't debug it without understanding the contexts and input variables tied to it. In this post, I'll use a real-world Absence Accrual Matrix formula — one I built for Philippine vacation leave — to explain every concept hands-on.

Abhishek Mohanty

Oracle HCM Cloud Consultant & Technical Lead

In the **previous post**, we covered the 7 default components of Fast Formula — what each building block is and how they relate. In this post, we go hands-on using a real production formula: `PH_VACATION_LEAVE_ACCRUAL_MATRIX` — a Philippine vacation leave accrual formula I built that handles probation periods, monthly accruals, and one-time lump sum credits.

Instead of a toy "return Y" example, we'll use this formula to see how Formula Types, Contexts, Input Values, and the type-to-column linkage work in a real-world scenario.

---

## Formula Type: The Decision That Shapes Everything

For our Philippine leave formula, the type is **Absence Accrual Matrix Formula**. That single selection determined:

    Absence Accrual Matrix

    automatically gave us:

    PERSON_ID context

    HR_ASSIGNMENT_ID context

    IV_ACCRUAL input

    IV_ACCRUALPERIOD dates

    PER_ASG_ DBIs

    Single RETURN accrual

If I had accidentally chosen **Compensation Person Selection** instead, none of the absence-specific inputs (IV_ACCRUAL, IV_ACCRUALPERIODSTARTDATE, etc.) would be available, the formula couldn't attach to an absence plan, and the PER_ASG_ DBIs might behave differently due to different context availability.

⚠️

The Trap

The formula editor will let you create and compile a formula under the wrong type with zero errors. It only breaks when you try to attach it or run the process. By then you've wasted hours debugging something that was wrong from step one.

---

## Contexts in Action: How Our Formula Knows "Whose" Data to Fetch

Look at this line from our accrual formula:

```text
l_hire_date = PER_ASG_REL_ORIGINAL_DATE_OF_HIRE
```

This DBI returns a hire date — but *whose* hire date? The answer is: whoever the `HR_ASSIGNMENT_ID` context points to.

When the absence accrual process runs for 500 employees, it calls this formula 500 times. Each time, it sets a different HR_ASSIGNMENT_ID context. The DBI automatically returns that specific employee's hire date. You never write SQL — the context-route-DBI chain handles it.

```text
/* We also retrieved context values directly: */

l_person_id     = GET_CONTEXT(PERSON_ID, 0)

l_assignment_id = GET_CONTEXT(HR_ASSIGNMENT_ID, 0)

/* These DBIs work BECAUSE the context is set: */

l_hire_date  = PER_ASG_REL_ORIGINAL_DATE_OF_HIRE

l_term_date  = PER_ASG_REL_ACTUAL_TERMINATION_DATE

l_asg_status = PER_ASG_STATUS_USER_STATUS
```

No context = no data. If HR_ASSIGNMENT_ID isn't set as a context for your formula type, PER_ASG_ DBIs will fail at runtime. This is why the formula type matters — it determines which contexts are available, which determines which DBIs work.

---

## Input Values: What the Accrual Engine Passes to Our Formula

Here's the INPUTS ARE block from our formula:

```text
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
```

These aren't random — they're defined in the Oracle FF Reference Guide (pages 16-17) specifically for the Absence Accrual Matrix formula type. The accrual engine populates them automatically at runtime.

| Input Value | What Our Formula Does With It |
| --- | --- |
| `IV_ACCRUAL` | Matrix engine's pre-calculated value — **we completely override it** with our own logic |
| `IV_ACCRUALPERIODSTARTDATE` | Used to determine which month we're processing and calculate months of service |
| `IV_ACCRUALPERIODENDDATE` | End of current period — critical for the MONTHS_BETWEEN calculation |
| `IV_PLANENROLLMENTSTARTDATE` | When the employee enrolled — used in eligibility checks |
| `IV_EVENT_DATES` | Array type — declared but not used in our logic (still must be declared) |

💡

Same Formula Type, Different Inputs

If the same formula type is used by a different process (like a different absence plan configuration), the input values may differ. Always check the FF Reference Guide for **your specific process**, not just the formula type.

---

## DEFAULTs: What Happens When Data Doesn't Exist

Every DBI and input value in our formula has a DEFAULT. This isn't optional — it's the difference between a working formula and a runtime crash:

```text
/* What if the employee has no termination date? */

DEFAULT FOR PER_ASG_REL_ACTUAL_TERMINATION_DATE

  IS '4712/12/31 00:00:00' (date)

/* What if the matrix engine sends no accrual value? */

DEFAULT FOR IV_ACCRUAL IS 0

/* What if assignment status DBI returns nothing? */

DEFAULT FOR PER_ASG_STATUS_USER_STATUS IS 'NA'
```

In our formula, the `4712/12/31` default for termination date is clever — later in the logic, we check if `l_term_date = TO_DATE('4712/12/31...')` to determine "is this person active?" If they are active, the DBI returns empty, the DEFAULT kicks in with 4712, and our check correctly identifies them as active.

DEFAULTs aren't just safety nets — they're part of your business logic. Choose default values that make your downstream conditions work correctly, not just arbitrary placeholders.

---

## Write Formulas vs. Validate Formulas

All Fast Formulas do one of two things:

Write Formula

### Calculates and returns a value

Our PH accrual formula returns a number — 0, 1.25, or 15 — depending on months of service. Other examples: Total Compensation Items, Salary calculations.

Validate Formula

### Checks a condition and returns Y or N

Should this person be included? Is this employee eligible? Examples: Person Selection, Benefits Eligibility, Participation Rules.

```text
/* Write — returns a number */

RETURN accrual  /* 0, 1.25, or 15 */

/* Validate — returns Y or N */

RETURN l_value  /* 'Y' or 'N' */
```

---

## The Column Trap: Why Your Formula Doesn't Show Up

You wrote a formula. It compiled. Green checkmark. But when you go to attach it to a setup field — it's not in the dropdown. You search, refresh, recompile. Nothing.

The reason: every formula has a **type**, and every setup field expects a **specific type**. If they don't match — the formula simply won't appear. No error, no warning. It's just invisible.

**A real mistake I've seen:**

A consultant needed to write an absence accrual formula. They went to the formula editor and accidentally selected **Absence Accrual** instead of **Absence Accrual Matrix**. Two very similar-sounding types — but different.

    **What happened:** The formula compiled fine. No errors. But when they went to the Absence Plan → Accrual Matrix Formula field — their formula was not in the dropdown. The field expected **Absence Accrual Matrix**. The formula was created as **Absence Accrual**. Close — but not the same type.

    **The fix:** They recreated the formula under the correct type — **Absence Accrual Matrix**. Same code, same logic. Now it appeared instantly.

If your formula isn't showing up in a dropdown, it's almost always the wrong type. You can't change a formula's type after creation — the fix is to create a new formula under the correct type.

---

## Creating and Compiling: The Step-by-Step

Here's how I created the PH accrual formula.

### Step 1 — Navigate

Go to **Setup and Maintenance**, search for **"Fast Formulas"**, and open the Fast Formulas task.

### Step 2 — Fill in the header

Formula Type

Absence Accrual Matrix Formula

Name

`PH_VACATION_LEAVE_ACCRUAL_MATRIX`

LDG

**Required** — Absence formulas need LDG

Effective Date

`01/01/2000` — far past for safety

**Why a far-past date?** If the absence process runs for a past period (Jan 2024) but the formula was created with today's date, it won't be found. Using 01/01/2000 ensures it's always available.

### Step 3 — Save, Submit, Compile

01

**Save** — stores the formula, still editable

02

**Submit** — locks the formula for compilation

03

**Compile** — triggers an ESS background job

04

Check status — green means ready, red means fix errors

---

## LDG: When You Need It and When You Don't

Our PH formula required an LDG because Absence formulas are country-specific. Here's the general rule:

LDG Required

**Absence** and **Payroll** — anything touching country-specific legislation

LDG Optional

**Compensation** and **Benefits** — if skipped, formula becomes global

---

## The Complete Workflow

Every formula follows this path from idea to production:

  Identify the correct Type**

  ↓

  Check if LDG is required

  ↓

  Write the formula code — DEFAULTs, INPUTS ARE, logic, RETURN

  ↓

  Save → Submit → Compile — wait for green status

  ↓

  Verify attachment — confirm the formula appears in the correct setup field

---

## Key Takeaways

What our PH Accrual Formula taught us:

Formula Type shapes everything** — Absence Accrual Matrix gave us IV_ACCRUAL, period dates, and PER_ASG_ DBIs

**Contexts make DBIs work** — PER_ASG_REL_ORIGINAL_DATE_OF_HIRE only returns the right data because HR_ASSIGNMENT_ID tells it whose data to fetch

**DEFAULTs are business logic** — 4712/12/31 isn't arbitrary, it's how we detect active employees

**The Column Trap is real** — wrong type means formula compiles but never shows up where you need it

**Absence formulas need LDG** — country-specific formulas require Legislative Data Group, Compensation doesn't

Want to see the full formula code with line-by-line explanation? Check out my detailed breakdown: **Breaking Down a PH Vacation Leave Accrual Matrix Formula — Section by Section**.

### Abhishek Mohanty

Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Core HR, Redwood, HDL, OTBI.
