---
title: "Oracle Fast Formula: Post Election Edit — How to Validate Cross-Plan Dependencies Using CHANGE_CONTEXTS and BEN_PEN Array DBIs"
description: "Oracle Fast Formula: Post Election Edit — Cross-Plan Enrollment Validation with Waiting Period Logic"
pubDate: 2026-04-06
---

Fast Formula
  Benefits
  Post Election Edit
  CHANGE_CONTEXTS
  BEN_PEN Array DBI
  ESS_LOG_WRITE
  Waiting Period

Oracle Fast Formula: Post Election Edit — Cross-Plan Enrollment Validation with Waiting Period Logic

Blocking Child Life enrollment when Employee Life isn't elected, using BEN_PEN array DBIs, CHANGE_CONTEXTS with a calculated future effective date, and ESS_LOG_WRITE tracing

April 2026 · 14 min read · Oracle HCM Cloud

  *

Abhishek Mohanty

This Formula at a Glance

| 1
        Calculate Future Date
        Life event + waiting period → coverage start date | 2
        Read Enrollment at Future
        CHANGE_CONTEXTS → loop BEN_PEN → set flags | 3
        Validate Plan Presence
        Child=Y + Employee=N → BLOCK | 4
        Validate Amounts
        Child $ > Employee $ → BLOCK |
| --- | --- | --- | --- |

The Business Rule

    Child Life
    requires
    Employee Life

No employee coverage → no child coverage. Standard US group life rule.

    Child Life $
    ≤
    Employee Life $

Child coverage amount can't exceed employee coverage. Only a formula can compare dollar amounts.

The business rule is straightforward: **an employee can't enroll in Voluntary Child Life insurance unless they also carry Voluntary Employee Life.** The child doesn't get coverage if the employee doesn't have coverage. This is standard across US group life insurance plans.

In Oracle Benefits, the employee makes all their elections in a single enrollment window — Medical, Dental, Employee Life, Child Life — and submits everything at once. A **Post Election Edit** formula fires at that point to validate whether the combination of elections is allowed.

Here's where it gets tricky. The formula validates elections by reading `BEN_PEN_PL_NAME_TN` — an array DBI that returns **active enrollment results**, meaning plans where the employee is currently enrolled and coverage is in effect. It does not* return the elections the employee is submitting right now. Those elections are still in flight — they haven't been written as enrollment results yet.

This creates a timing gap. If the formula checks enrollment at **today's** effective date, it sees the employee's *current* state — not the state that will exist after the new elections take effect. And that leads to a serious validation hole.

Let's look at four employees making elections during the same enrollment window:

| Employee | Current Enrollment (today) | New Election (submitting now) | What the formula sees at today's date |
| --- | --- | --- | --- |
| **James** (new hire) | Nothing — he just joined | Employee Life + Child Life | Child Life = N, Employee Life = N. **Passes** — but only because neither flag is set. The validation didn't actually check anything meaningful. |
| **Sarah** (existing employee, Open Enrollment) | Employee Life only | Adding Child Life | Child Life = N, Employee Life = Y. **Passes** — happens to be correct, but the formula is reading Sarah's old enrollment, not her new election. |
| **Mike** (existing employee, dropping coverage) | Employee Life + Child Life | Dropping Employee Life, keeping Child Life | Child Life = Y, Employee Life = Y. **Passes — and this is wrong.** Mike is dropping Employee Life, but the formula doesn't know that because `BEN_PEN` still reflects his current enrollment. |
| **Lisa** (existing employee, changing amounts) | Employee Life $200K + Child Life $50K | Reducing Employee Life to $100K, increasing Child Life to $150K | Child Life $50K, Employee Life $200K. **Passes — and this is wrong.** At the future date, Child Life ($150K) will exceed Employee Life ($100K). But today's data still shows the old amounts. |

**Mike and Lisa are the scenarios this formula exists to catch.** Mike has Child Life without Employee Life — a plan-level violation. Lisa has both plans but her Child Life amount exceeds Employee Life — an amount-level violation. When the formula reads `BEN_PEN_PL_NAME_TN` at today's effective date, it sees both plans as active. Why? Because Mike's decision to drop Employee Life doesn't take effect today. It takes effect on the *future coverage start date* — the date after the waiting period ends.

That's the critical distinction. `BEN_PEN` returns enrollment results **as of the effective date you give it**:

| Effective Date | What BEN_PEN Returns for Mike | Why |
| --- | --- | --- |
| **Today** (election day) | Employee Life = active, Child Life = active | Mike's current enrollments are still in force. His drop hasn't taken effect — it won't until the coverage start date. |
| **Future coverage date** (after waiting period) | Employee Life = gone, Child Life = active | Oracle has projected the new elections to this date. The drop is now reflected. Only Child Life remains. |

| ❌ Checking at Today's Date
        BEN_PEN sees:
        Employee Life ✓
        Child Life ✓
        → Both active → PASSES (wrong!) | ✓ Checking at Future Coverage Date
        BEN_PEN sees:
        Employee Life
        Child Life ✓
        → Child without Employee → BLOCKED ✓ |
| --- | --- |

**The fix:** instead of checking enrollment at today's date, the formula first calculates the future coverage effective date — factoring in the employer's waiting period — and then uses `CHANGE_CONTEXTS(EFFECTIVE_DATE = l_cvg_eff_date)` to shift the lookup forward to that date. Now `BEN_PEN` returns the second row from the table above: Employee Life is gone, Child Life is the only active plan. The formula sees Child Life = Y, Employee Life = N → **blocked**. Exactly as it should be.

That's why this formula has a waiting period calculation and a `CHANGE_CONTEXTS` shift. Without them, the formula validates against stale enrollment data and lets Mike through — missing the exact scenario it was built to prevent.

## What This Formula Does

This is a **Post Election Edit** formula. Oracle calls it after the employee submits their benefit elections during enrollment. The formula validates the elections and either allows them to proceed or blocks them with an error message.

| Return Variable | Type | What It Means |
| --- | --- | --- |
| `SUCCESSFUL` | Character | `'Y'` = elections are valid, proceed. `'N'` = elections are invalid, block. |
| `ERROR_MESSAGE` | Character | Message shown to the employee when blocked. Only matters when `SUCCESSFUL = 'N'`. |

The formula does three things in sequence:

| Step | What It Does | Why It's Needed |
| --- | --- | --- |
| **1. Calculate coverage effective date** | Read the life event date. Apply waiting period logic. Compute the future date when coverage will actually start. | Elections are made today but coverage starts later. Validation must check enrollment state at the future date, not today. |
| **2. Read enrollment results at future date** | Use `CHANGE_CONTEXTS` to shift effective date forward. Loop through `BEN_PEN_PL_NAME_TN` array DBI to check which plans the employee is enrolled in. | The array DBI returns all plan enrollments for this person. The formula needs to find two specific plans in this list. |
| **3. Validate the combination** | If Child Life = Y and Employee Life = N → block. Every other combination → allow. | The only invalid combination is having child coverage without employee coverage. |

The first thing you'll notice: **Step 1 is the complex part.** Steps 2 and 3 are the standard array loop and IF/ELSE that you've seen in previous posts. Step 1 is unique to this formula — it calculates a waiting period and builds a future effective date before any enrollment data is read.

## The Waiting Period — When Does Coverage Actually Start?

Life insurance coverage doesn't always start on the life event date. Many employers require a waiting period — employees must wait before coverage kicks in. This isn't a US federal requirement. There's no law mandating a waiting period for group life insurance. Some employers start coverage on day 1, others use a 30-day or 60-day wait. In this scenario, the employer uses a two-month wait with coverage starting on the 1st of a month.

The formula needs to know this exact coverage start date because that's the date it will use with `CHANGE_CONTEXTS` to check enrollment. Different employer, different waiting period, different date calculation — but the same formula structure.

**James** was hired on **March 15**. He didn't join on the 1st of the month, so the waiting period applies. March is a partial month — doesn't count. April is the first full month — that's month one of the wait. May is month two. Coverage starts on the **1st of June**.

**Sarah's** Open Enrollment event date is **January 1**. She's on the 1st of the month — no extended wait needed. Coverage starts on the **1st of February**, the very next month.

James (New Hire) — Event on March 15

| MAR 15
        Event date
        Partial month | APR
        Wait month 1
        ⏳ | MAY
        Wait month 2
        ⏳ | JUN 1
        Coverage starts
        Formula checks here | ✅
        PASSES
        Both plans elected |
| --- | --- | --- | --- | --- |

Sarah (Open Enrollment) — Event on January 1

| JAN 1
        Event date
        On the 1st! | FEB 1
        Coverage starts
        Formula checks here | No extended wait — event was on the 1st | ✅
        PASSES
        Has Employee Life |
| --- | --- | --- | --- |

⚠ Mike (Dropping Coverage) — Event on April 10

| APR 10
        Event date
        Partial month | MAY
        Wait month 1
        ⏳ | JUN
        Wait month 2
        ⏳ | JUL 1
        Coverage starts
        Formula checks here | 🚫
        BLOCKED
        Child Life without**Employee Life |
| --- | --- | --- | --- | --- |

⚠ Lisa (Changing Amounts) — Event on March 20

| MAR 20
        Event date | APR
        ⏳ | MAY
        ⏳ | JUN 1
        Checks here | 🚫 BLOCKED — Amount Violation
        Child $150K
        >
        Employee $100K |
| --- | --- | --- | --- | --- |

Mike's** divorce was on **April 10**. Same as James — he didn't join on the 1st. April is partial, May is month one, June is month two. Coverage starts on the **1st of July**. This is the date the formula will use to check whether Mike still has Employee Life.

**Lisa's** qualifying event was on **March 20**. She currently has Employee Life at $200K and Child Life at $50K. She's reducing Employee Life to $100K and increasing Child Life to $150K. After the waiting period, coverage starts on the **1st of June**. At that date, the formula reads the new amounts: Child Life $150K, Employee Life $100K. **$150K > $100K — blocked.** This is the scenario that only the formula can catch. Plan Dependency sees both plans are enrolled and allows it. The formula sees the amounts don't comply.

| Employee | Event Date | On the 1st? | Coverage Starts | Formula Checks BEN_PEN At |
| --- | --- | --- | --- | --- |
| **James** | 15-Mar-2025 | No | **01-Jun-2025** | 01-Jun-2025 |
| **Sarah** | 01-Jan-2025 | Yes | **01-Feb-2025** | 01-Feb-2025 |
| **Mike** | 10-Apr-2025 | No | **01-Jul-2025** | 01-Jul-2025 |
| **Lisa** | 20-Mar-2025 | No | **01-Jun-2025** | 01-Jun-2025 |

That last column is the whole point. The coverage start date becomes the `EFFECTIVE_DATE` for `CHANGE_CONTEXTS`. The formula reads `BEN_PEN` at that date — not today — to see the projected enrollment state.

How the Formula Calculates This Date

Fast Formula can't set the day of a date to "01" directly — there's no such function. So it uses a workaround: `ADD_MONTHS(date, 2)` moves forward 2 months → `LAST_DAY()` jumps to the end of that month → `ADD_DAYS(, 1)` lands on the 1st of the next month. For Mike: 10-Apr + 2 months = 10-Jun → last day of Jun = 30-Jun → +1 = **01-Jul**. You'll see this `LAST_DAY + ADD_DAYS(1)` trick throughout Oracle Benefits formulas wherever a "1st of the month" date is needed.

The Role of the Waiting Period in This Formula

The waiting period here is **not controlling when coverage starts** — Oracle's built-in waiting period configuration on the plan enrollment page handles that. You can set "30 days" or "first of the month following 60 days" in plan setup without any formula.

In this formula, the waiting period answers one question: **"As of what date should I check whether this employee still has Employee Life?"** Without this date, the formula falls back to today's effective date — and that's exactly how Mike's scenario slips through.

## Why CHANGE_CONTEXTS Is Needed Here

I covered the "why" in the intro with Mike's scenario. Here's the technical "how."

The formula uses `CHANGE_CONTEXTS(EFFECTIVE_DATE = l_cvg_eff_date)` to shift the context forward to the coverage effective date. Every DBI read inside this block returns values *as of that future date* — including the projected enrollment results after the current elections are finalized.

The Context Shift — Today vs Future

```text
/* Without CHANGE_CONTEXTS — reads enrollment as of TODAY     */
/* Result: might not see the new elections yet                */

/* With CHANGE_CONTEXTS — reads enrollment as of JUNE 1       */
/* Result: sees the new elections the employee just submitted  */
CHANGE_CONTEXTS(EFFECTIVE_DATE = l_cvg_eff_date)CONTEXT
(
    /* Now BEN_PEN_PL_NAME_TN returns enrollments as of Jun 1 */
    /* This includes the elections being made right now       */
)
```

Without `CHANGE_CONTEXTS`, the formula validates against stale enrollment data — the Mike scenario from the intro.

## The Array DBI Loop — What BEN_PEN Gives You

`BEN_PEN_PL_NAME_TN` and `BEN_PEN_OPT_NAME_TN` are **array DBIs**. Each index `[i]` represents a different plan enrollment for this person. The loop walks through all of them looking for two specific plans.

Here's what the array might contain for an employee enrolled in three plans:

| Index [i] | BEN_PEN_PL_NAME_TN[i] | BEN_PEN_OPT_NAME_TN[i] |
| --- | --- | --- |
| 1 | Medical PPO | Employee + Family |
| 2 | Voluntary Employee Life and AD&D | 10,000 - 500,000 |
| 3 | Voluntary Child Life and AD&D | 1,000 - 10,000 |
| 4 | Dental | Employee Only |

The formula doesn't know in advance how many enrollments exist or what order they're in. It loops from `i = 1` until `BEN_PEN_PL_NAME_TN.exists(i)` returns false. At each index, it checks the plan name and option name. If it finds a match, it sets a flag.

| Flag | Set to 'Y' When | Meaning |
| --- | --- | --- |
| `l_child_flag` | Plan = `'Voluntary Child Life and AD&D'` AND Option = `'1,000 - 10,000'` | Employee is enrolling in Child Life |
| `l_emp_flag` | Plan = `'Voluntary Employee Life and AD&D'` AND Option = `'10,000 - 500,000'` | Employee is enrolled in Employee Life |

Watch Out — Hardcoded Option Names

The formula checks for exact option names: `'1,000 - 10,000'` and `'10,000 - 500,000'`. If the plan configuration changes — say the option range is updated to `'10,000 - 600,000'` — the formula won't match it. It will treat the employee as not enrolled in Employee Life and block Child Life elections incorrectly. The option names in the formula must exactly match the option names configured in Plan Configuration. A safer approach would be to check only the plan name and ignore the option name — unless the business specifically requires option-level validation.

## The Validation Matrix

✓ Valid Combinations — PASS

| Child N
          Emp N | Waiving both plans — nothing to validate |
| --- | --- |
| Child N
          Emp Y | Employee Life only — no dependency issue |
| Child Y $50K
          Emp Y $200K | Both enrolled, **$50K ≤ $200K** — amounts OK |

| Child Y
          Emp N | 🚫 BLOCKED — Step 3 (Mike)
          Child Life without Employee Life. Plan Dependency also catches this at the UI. |
| --- | --- |

| Child Y $150K
          Emp Y $100K | 🚫 BLOCKED — Step 4 (Lisa)
          Both enrolled but **$150K > $100K**. Child coverage exceeds employee coverage. *Only the formula catches this — no configuration can compare amounts.* |
| --- | --- |

After the loop, the formula has two flags and two amounts. There are five possible combinations. Two are invalid — one caught by plan presence (Step 3), one by amount comparison (Step 4).

| l_child_flag (Child Life) | l_emp_flag (Employee Life) | SUCCESSFUL | Why |
| --- | --- | --- | --- |
| N | N | Y | Waiving both — valid |
| N | Y | Y | Employee Life only — valid |
| Y | Y | Y | Both enrolled — valid |
| **Y** | **N** | **N** | **Child Life without Employee Life — blocked** |

The formula only returns `SUCCESSFUL = 'N'` for the fourth combination. In all other cases, `SUCCESSFUL` stays at its initial value of `'Y'` and the enrollment proceeds.

## The Complete Formula

Here's the full Post Election Edit formula. I'll break it into blocks below.

XX_VOL_LIFE_CROSS_PLAN_EDIT — Post Election Edit

```text
/*************************************************************
FORMULA NAME : XX_VOL_LIFE_CROSS_PLAN_EDIT
FORMULA TYPE : Post Election Edit
DESCRIPTION  : Block Child Life enrollment if Employee Life
               is not elected. Check at coverage effective
               date after waiting period.
*************************************************************/

/* ── Defaults ── */
DEFAULT_DATA_VALUE FOR BEN_PEN_PL_NAME_TN IS 'My-Default'ARRAY DBI
DEFAULT_DATA_VALUE FOR BEN_PEN_OPT_NAME_TN IS 'My-Default'ARRAY DBI
DEFAULT_DATA_VALUE FOR BEN_PEN_BNFT_AMT_NN IS 0ARRAY DBI
DEFAULT FOR BEN_PIL_LF_EVT_OCRD_DT IS '1951/01/01 00:00:00' (DATE)DBI

/* ── Initialize ── */
SUCCESSFUL = 'Y'REQUIRED
l_child_flag = 'N'
l_emp_flag = 'N'
l_child_amt = 0    /* Child Life coverage amount */
l_emp_amt = 0      /* Employee Life coverage amount */
ERROR_MESSAGE = ' 'OPTIONAL
i = 1

l_cvg_eff_date = GET_CONTEXT(EFFECTIVE_DATE,CONTEXT
                        TO_DATE('1951/01/01 00:00:00'))
l_event_dt = BEN_PIL_LF_EVT_OCRD_DT

l_dbg = ESS_LOG_WRITE('l_event_dt is 'LOG
    || TO_CHAR(l_event_dt, 'MM/DD/YYYY'))

/* ═════════════════════════════════════════════ */
/*  STEP 1: WAITING PERIOD → COVERAGE EFF DATE  */STEP 1
/* ═════════════════════════════════════════════ */
IF (TO_CHAR(l_event_dt, 'DD')) = '01' THEN
(
    /* Event on 1st → coverage starts next month */
    l_wait_dt = ADD_MONTHS(l_event_dt, 1)
    l_cvg_eff_date = l_wait_dt
)
ELSE
(
    /* Event not on 1st → 1st of month after 2-month wait */
    l_wait_dt = ADD_MONTHS(l_event_dt, 2)
    l_wait_end_dt = LAST_DAY(l_wait_dt)
    l_cvg_eff_date = ADD_DAYS(l_wait_end_dt, 1)
)

l_dbg = ESS_LOG_WRITE('l_cvg_eff_date is 'LOG
    || TO_CHAR(l_cvg_eff_date, 'MM/DD/YYYY'))

/* ═════════════════════════════════════════════ */
/*  STEP 2: READ ENROLLMENTS AT FUTURE DATE     */STEP 2
/* ═════════════════════════════════════════════ */
CHANGE_CONTEXTS(EFFECTIVE_DATE = l_cvg_eff_date)CONTEXT
(
    WHILE BEN_PEN_PL_NAME_TN.exists(i) LOOP
    (
        IF (BEN_PEN_PL_NAME_TN[i] = 'Voluntary Child Life and AD&D'
            AND BEN_PEN_OPT_NAME_TN[i] = '1,000 - 10,000')
        THEN
        (
            l_child_flag = 'Y'
            l_child_amt = BEN_PEN_BNFT_AMT_NN[i]AMOUNT
        )

        IF (BEN_PEN_PL_NAME_TN[i] = 'Voluntary Employee Life and AD&D'
            AND BEN_PEN_OPT_NAME_TN[i] = '10,000 - 500,000')
        THEN
        (
            l_emp_flag = 'Y'
            l_emp_amt = BEN_PEN_BNFT_AMT_NN[i]AMOUNT
        )

        i = i + 1
    )
)

l_dbg = ESS_LOG_WRITE('Child Life = ' || l_child_flagLOG
    || ' Amt = ' || TO_CHAR(l_child_amt))
l_dbg = ESS_LOG_WRITE('Employee Life = ' || l_emp_flag
    || ' Amt = ' || TO_CHAR(l_emp_amt))

/* ═════════════════════════════════════════════ */
/*  STEP 3: VALIDATE CROSS-PLAN COMBINATION     */STEP 3
/* ═════════════════════════════════════════════ */
IF (l_child_flag = 'Y' AND l_emp_flag = 'N') THEN
(
    SUCCESSFUL = 'N'
    ERROR_MESSAGE = 'Enrollment in Voluntary Child Life'
        || ' requires an active Voluntary Employee Life'
        || ' election. Please update your selections'
        || ' before submitting.'
)

/* ═════════════════════════════════════════════ */
/*  STEP 4: VALIDATE COVERAGE AMOUNTS          */STEP 4
/* ═════════════════════════════════════════════ */
ELSE IF (l_child_flag = 'Y' AND l_emp_flag = 'Y'
    AND l_child_amt > l_emp_amt) THEN
(
    SUCCESSFUL = 'N'
    ERROR_MESSAGE = 'Child Life coverage ($'
        || TO_CHAR(l_child_amt)
        || ') cannot exceed Employee Life ($'
        || TO_CHAR(l_emp_amt)
        || '). Please adjust your elections.'
)

l_dbg = ESS_LOG_WRITE('SUCCESSFUL = ' || SUCCESSFUL)LOG
l_dbg = ESS_LOG_WRITE('ERROR_MESSAGE = ' || ERROR_MESSAGE)

RETURN SUCCESSFUL, ERROR_MESSAGERETURN
```

## Block-by-Block Walkthrough

1**Defaults and Initialization**

`BEN_PEN_PL_NAME_TN` and `BEN_PEN_OPT_NAME_TN` are array DBIs — the `_TN` suffix indicates translated name. They need `DEFAULT_DATA_VALUE` (not `DEFAULT FOR`) because they're array DBIs. The default `'My-Default'` is never actually matched in the IF conditions — it's just a required syntactic safeguard.

`BEN_PIL_LF_EVT_OCRD_DT` is the life event occurred date — the date of the event that triggered enrollment (hire, open enrollment, qualifying life event). This is a regular DBI, not an array, so it uses `DEFAULT FOR`.

`SUCCESSFUL` starts as `'Y'`. The formula only changes it to `'N'` if the invalid combination is found. If none of the IF conditions fire, the employee passes validation by default. This is intentional — the formula should only block, never accidentally reject valid elections.

2**Waiting Period Calculation**

The formula extracts the day of the month using `TO_CHAR(date, 'DD')`. Two paths:

**Path A — Event on the 1st:** `ADD_MONTHS(date, 1)`. Coverage starts on the 1st of the next month. Simple.

**Path B — Event on any other day:** Three date functions chained together: `ADD_MONTHS(date, 2)` moves forward 2 months, `LAST_DAY()` goes to the end of that month, `ADD_DAYS(, 1)` moves to the 1st of the following month. This is the `LAST_DAY + ADD_DAYS(1)` pattern explained in the waiting period section above.

3**Enrollment Result Array Loop**

`CHANGE_CONTEXTS(EFFECTIVE_DATE = l_cvg_eff_date)` shifts the context forward to the coverage effective date. Every DBI read inside this block returns values as of that future date.

The `WHILE BEN_PEN_PL_NAME_TN.exists(i) LOOP` iterates through all plan enrollments for this person. The formula doesn't know how many there are — could be 2, could be 10. The `.exists(i)` check stops the loop when there are no more enrollments.

Inside the loop, two separate IF statements (not IF/ELSE). This is important — both conditions are checked at every index. If index 2 is Employee Life and index 3 is Child Life, both flags get set in separate iterations. If you used IF/ELSE, finding Child Life at index 2 would skip the Employee Life check at index 3.

4**Cross-Plan Validation (Plan Presence + Coverage Amounts)**

Two IF conditions, checked in order. **Step 3** is the plan-presence check — `l_child_flag = 'Y' AND l_emp_flag = 'N'` — Child Life elected but Employee Life not. This is Mike's scenario. **Step 4** is the amount check — `l_child_amt > l_emp_amt` — both plans elected but Child Life amount exceeds Employee Life. This is Lisa's scenario. The `ELSE IF` structure ensures Step 4 only runs when both plans are present.

There's no final ELSE. If neither condition matches, `SUCCESSFUL` stays at `'Y'` from initialization and the enrollment proceeds.

## The ESS Log Output

Here's what the log looks like for Mike — dropping Employee Life but keeping Child Life, life event on April 10:

ESS Log — Mike: Child Life Without Employee Life (Blocked — Step 3)

```text
l_event_dt is 04/10/2025LOG
l_cvg_eff_date is 07/01/2025          /* 2-month wait → Jul 1 */
Child Life = Y  Amt = 50000
Employee Life = N  Amt = 0
SUCCESSFUL = N
ERROR_MESSAGE = Enrollment in Voluntary Child Life requires...
```

And for Lisa — both plans enrolled but Child Life amount exceeds Employee Life, event on March 20:

ESS Log — Lisa: Child Amount Exceeds Employee (Blocked — Step 4)

```text
l_event_dt is 03/20/2025LOG
l_cvg_eff_date is 06/01/2025          /* 2-month wait → Jun 1 */LOG
Child Life = Y  Amt = 150000
Employee Life = Y  Amt = 100000
SUCCESSFUL = N
ERROR_MESSAGE = Child Life coverage ($150000) cannot exceed...
```

And for Sarah — existing Employee Life, adding Child Life within limits, event on January 1:

ESS Log — Sarah: Both Plans, Amounts OK (Allowed)

```text
l_event_dt is 01/01/2025LOG
l_cvg_eff_date is 02/01/2025          /* event on 1st → next month */
Child Life = Y  Amt = 50000
Employee Life = Y  Amt = 200000
SUCCESSFUL = Y
ERROR_MESSAGE =
```

The formula logs at every key stage: the life event date, the calculated effective date, the flags and amounts after the loop, and the final result. For deeper debugging, add `ESS_LOG_WRITE('Plan[' || TO_CHAR(i) || '] = ' || BEN_PEN_PL_NAME_TN[i])` inside the loop to print every plan in the array.

Debugging Tip

If the formula is blocking elections that should be allowed, add `ESS_LOG_WRITE('Plan[' || TO_CHAR(i) || '] = ' || BEN_PEN_PL_NAME_TN[i])` inside the loop. This prints every plan in the array. The most common issue is a plan name mismatch — the formula checks for `'Voluntary Employee Life and AD&D'` but the plan is configured as `'Voluntary Employee Life & AD&D'` (ampersand vs "and"). One character difference and the flag never gets set.

Edge Case — Zero Amounts

If `BEN_PEN_BNFT_AMT_NN` returns the default value `0` for both plans (missing data, configuration issue, or non-monetary plan), the comparison `0 > 0` evaluates to FALSE — so the formula passes the employee through. This is intentional: **don't block elections when you can't determine amounts.** If your business requires blocking on zero amounts, add an explicit check: `IF (l_child_amt = 0 OR l_emp_amt = 0) THEN` with a separate error message.

About the Code Labels

The colored labels in the formula code (`REQUIRED` `CONTEXT` `LOG` `STEP 1` etc.) are **blog annotations only** — they highlight what each line does. **Strip them before pasting into the formula editor.** The formula editor will reject any text that isn't valid Fast Formula syntax.

## Where This Formula Is Attached

| Step | Where | What to Set |
| --- | --- | --- |
| 1 | Plan Configuration → Program or Plan → Enrollment | Select the plan in the plan hierarchy |
| 2 | Further Details section → Post Election Edit | Select `XX_VOL_LIFE_CROSS_PLAN_EDIT` |

You can attach the formula at the plan level, plan type level, or option level depending on the scope. For this scenario — where the validation is between two plans — attach it at the **plan type level** so it fires for any plan within the Voluntary Life plan type.

## Same Pattern, Different Plans

The cross-plan dependency pattern isn't limited to Life insurance. Any business rule that says "you can't enroll in Plan B without Plan A" uses the same formula structure.

| Plan A (Required) | Plan B (Dependent) | Business Rule |
| --- | --- | --- |
| HDHP Medical | HSA | Can't contribute to HSA without HDHP enrollment |
| Voluntary Employee Life | Voluntary Spouse Life | Can't cover spouse without employee coverage |
| Voluntary Employee Life | Voluntary Child Life | Can't cover children without employee coverage (this post) |
| Medical Plan | Dependent Care FSA | Some employers require medical enrollment before FSA |
| Dental | Orthodontia Rider | Can't add rider without base dental plan |

In each case, the formula is identical in structure: loop through `BEN_PEN_PL_NAME_TN`, set flags for Plan A and Plan B, validate the combination. The plan names and error message change. The pattern doesn't.

---

## Recap

**Post Election Edit** formulas fire after election submission and return `SUCCESSFUL` = Y or N. They're the right tool for cross-plan dependency validation.

The formula in this post adds one layer of complexity: a **waiting period calculation** that computes a future effective date, then uses `CHANGE_CONTEXTS` to read enrollment results at that future date. Without this, the formula would check enrollment at the wrong point in time and produce false negatives.

Three things to watch when adapting this formula: **(1)** plan and option names must exactly match what's in Plan Configuration, **(2)** the waiting period logic must match your client's actual waiting period rules, and **(3)** use two separate IF statements inside the loop (not IF/ELSE) so both flags can be set in the same pass.

---

## References

| # | Source | What I Used From It |
| --- | --- | --- |
| 1 | [Administering Fast Formulas — Post Election Edit ↗](https://docs.oracle.com/en/cloud/saas/human-resources/24d/oapff/post-election-edit.html) | Formula type contract: `SUCCESSFUL` and `ERROR_MESSAGE` return variables, available contexts, BEN_PEN array DBIs |
| 2 | [Implementing Benefits — Enrollment Rules ↗](https://docs.oracle.com/en/cloud/saas/human-resources/24d/fabdi/enrollment-rules.html) | Post Election Edit attachment point in Plan Configuration, plan type vs plan level vs option level scope |

A Note on the Formula

The formula in this post is based on a production Post Election Edit formula from a US Oracle HCM Cloud implementation. Plan and option names are unchanged to illustrate the exact-match sensitivity — in your implementation, replace them with your configured plan and option names. The waiting period logic, CHANGE_CONTEXTS pattern, and array DBI loop structure are reusable across any cross-plan dependency scenario.

---

  ![Abhishek Mohanty](data:image/jpeg;base64,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)

Abhishek Mohanty

  Fast Formula
  Benefits
  Post Election Edit
  BEN_PEN_PL_NAME_TN
  CHANGE_CONTEXTS
  ESS_LOG_WRITE
  Waiting Period
  Cross-Plan Validation
  Voluntary Life
  Array DBI
  Oracle HCM Cloud

© 2026 Abhishek Mohanty — Oracle HCM Cloud Insights
