---
title: "Oracle HCM Cloud Fast Formula - Participation and Rate Eligibility formula with CHANGE_CONTEXTS, WAS DEFAULTED null handling, PER_EXT_ORG array DBI loop"
description: "The business says \"exclude workers in Puerto Rico and Washington DC.\" Simple — until you realize that the worker's work state can come from three different places in Oracle HCM depending on whether they work from home, whether their departm"
pubDate: 2026-03-19
tags: ["Fast Formula", "Participation & Rate Eligibility", "CHANGE_CONTEXTS", "WAS DEFAULTED"]
---

The business says "exclude workers in Puerto Rico and Washington DC." Simple — until you realize that the worker's work state can come from three different places in Oracle HCM depending on whether they work from home, whether their department has a state configured, or whether you have to fall back to the assignment location. This Participation and Rate Eligibility formula handles all three scenarios — and the org location lookup at the center of it uses CHANGE_CONTEXTS and array looping, both of which we covered in the previous posts.

Abhishek Mohanty

In the previous posts, we covered [the 7 building blocks of Fast Formula](#), [the PH Vacation Leave Accrual Matrix formula](#), [Array DBIs with CHANGE_CONTEXTS](#), and [There Is No NULL in Fast Formula](#). This post puts all of that together in a real-world **[Participation and Rate Eligibility ↗](https://docs.oracle.com/en/cloud/saas/human-resources/oapff/participation-and-rate-eligibility.html)** formula — the formula type Oracle uses to determine whether a person is eligible for a compensation object. This one uses standard DBIs, extract org array DBIs, CHANGE_CONTEXTS, WAS DEFAULTED null handling, and a multi-tier fallback chain.

I'll walk through the formula section by section, explain why each piece exists, and show the actual DBI metadata from the [REL11 DBI export file ↗](https://www.scribd.com/document/511029660/HCM-Extract-DBI-List-REL11-updated) to prove it.

---

## What This Formula Does

This is a **Participation and Rate Eligibility** formula. In Oracle Benefits, you attach this formula type to an Eligibility Profile to determine whether a person qualifies for a compensation object (plan, option, rate). The return value is simple: `ELIGIBLE = 'Y'` or `'N'`.

Our eligibility rule: **if the worker's work state is Puerto Rico (PR) or Washington DC (DC), they're excluded.** Everyone else is eligible.

The complication is that the worker's work state can come from three possible sources. The formula checks them in order — Tier 1 first, Tier 2 if Tier 1 doesn't apply, Tier 3 only as a fallback.

| Tier | Condition | State Source | DBI Used |
| --- | --- | --- | --- |
| 1 | Work at Home = Y | Assignment Work Location State | PER_ASG_LOC_REGION2 |
| 2 | Work at Home = N, department state found | Department's Organization Location State | PER_EXT_ORG_LOC_REGION2[i] |
| 3 | Work at Home = N, no department state | Assignment Location (fallback) | PER_ASG_LOC_REGION2 |

The first thing you'll notice: **Tier 1 and Tier 3 use the same DBI** (`PER_ASG_LOC_REGION2`). And Tier 2 uses a completely different one — an array DBI that requires CHANGE_CONTEXTS and a loop. Why?

Because each tier answers a different business question:

### Tier 1 — Remote Workers (Work at Home = Y)

The worker works from home. Their assignment still has a location on record — the office they're affiliated with for payroll, tax, or reporting. For remote workers, the business says: check the state on their assignment location. If it's PR or DC, exclude them.

DBI: `PER_ASG_LOC_REGION2` — standard DBI, single value, no loop needed.

### Tier 2 — Office Workers with Department State (Work at Home = N)

The worker goes to an office. But the business doesn't want to check where the worker *sits* — they want to check where the worker's **department is located**. A worker could sit in a New York office but belong to a department headquartered in Puerto Rico. The eligibility is based on the department's jurisdiction, not the worker's physical desk.

The problem: there's no DBI that directly returns "department's location state." You have to loop through the org array, match the org ID against the worker's department ID, and grab the state.

DBI: `PER_EXT_ORG_LOC_REGION2[i]` — array DBI, needs CHANGE_CONTEXTS + WHILE loop + org ID matching. This is the most complex part of the formula.

### Tier 3 — Office Workers, No Department State (Fallback)

The formula tried to look up the department's state — but found nothing. The department doesn't have a location configured in Manage Organizations. Fall back to the worker's own assignment location.

DBI: `PER_ASG_LOC_REGION2` — same DBI as Tier 1, different reason. Tier 1 uses it because the worker is remote. Tier 3 uses it because the department lookup failed.

**Why the same DBI in Tier 1 and Tier 3 but not Tier 2?**

`PER_ASG_LOC_REGION2` answers: *"What state is on the worker's assignment location?"* That's the right question for remote workers (Tier 1) and when department data is missing (Tier 3). But for office workers with a department location configured (Tier 2), the business wants a different question: *"What state is the department's organization located in?"* — that requires the org array lookup.

### A Real-World Example

|  | Maria**Remote | JamesOffice, dept in PR | PriyaOffice, no dept loc |
| --- | --- | --- | --- |
| Work at Home | Y | N | N |
| Assignment Location | TX Office | NY Office | FL Office |
| Dept Location State | — (not checked) | PR | — (not configured) |
| Tier that fires | Tier 1 | Tier 2 | Tier 3 |
| State checked | TX (asg loc) | PR (dept org loc) | FL (asg loc fallback) |
| Result | ELIGIBLE | EXCLUDED | ELIGIBLE |

Notice James: he sits in the New York office, but his department (HR) is headquartered in Puerto Rico. If the formula only checked assignment location, James would pass. Tier 2 catches it.

---

## The Complete Formula

Here's the full Participation and Rate Eligibility formula. I'll break it into blocks below.

```text
/* ================================================== */
/* Participation and Rate Eligibility Formula         */
/* Work State Exclusion (Exclude PR, DC)              */
/* ================================================== */

DEFAULT for PER_ASG_WORK_AT_HOME is 'NO_DATA'
DEFAULT for PER_ASG_LOC_REGION2 is 'NO_DATA'

DEFAULT_DATA_VALUE for PER_EXT_ORG_LOC_REGION2 is 'NO_REGION'
DEFAULT_DATA_VALUE for PER_EXT_ORG_ORGANIZATION_ID is 0
DEFAULT FOR PER_ASG_DEPARTMENT_ID IS 0

/* ----- Initialize ----- */
i = 1
l_loc = 'NO_REGION'

l_ORGANIZATION_ID = PER_ASG_DEPARTMENT_ID

l_eff_date = get_context(EFFECTIVE_DATE, '1900/01/01 00:00:00'(date))

ELIGIBLE = 'N'

/* ----- Resolve Department State via Org Location ----- */
CHANGE_CONTEXTS (EFFECTIVE_DATE = l_eff_date)
(
    WHILE PER_EXT_ORG_LOC_REGION2.exists(i)  LOOP
    (
        IF PER_EXT_ORG_ORGANIZATION_ID[i] = PER_ASG_DEPARTMENT_ID THEN
        (
            l_loc = PER_EXT_ORG_LOC_REGION2[i]
            EXIT
        )

        i = i + 1
    )
)

/* ----- Eligibility Decision Chain ----- */

/* Tier 0: Bad data — critical DBIs returned null */
IF (PER_ASG_WORK_AT_HOME WAS DEFAULTED OR
    PER_ASG_LOC_REGION2 WAS DEFAULTED) THEN
(eligible = 'N')

ELSE

/* Tier 1: Remote worker — check assignment work state */
IF (PER_ASG_WORK_AT_HOME = 'Y' AND
   (PER_ASG_LOC_REGION2 != 'PR' AND
    PER_ASG_LOC_REGION2 != 'DC'))
THEN (eligible = 'Y')

ELSE

/* Tier 2: Office worker — check department org location */
IF (PER_ASG_WORK_AT_HOME = 'N' AND
   (l_loc != 'PR' AND l_loc != 'DC') AND
    l_loc != 'NO_REGION')
THEN (eligible = 'Y')

ELSE

/* Tier 3: Fallback — no dept state, use assignment location */
IF (PER_ASG_WORK_AT_HOME = 'N' AND l_loc = 'NO_REGION' AND
   (PER_ASG_LOC_REGION2 != 'PR' AND
    PER_ASG_LOC_REGION2 != 'DC'))
THEN (eligible = 'Y')

ELSE eligible = 'N'

/* ----- Debug Logging ----- */
l = ess_log_write('Work at Home : ' || (PER_ASG_WORK_AT_HOME))
l = ess_log_write('Work State : ' || (PER_ASG_LOC_REGION2))
l = ess_log_write('Department State : ' || (l_loc))
l = ess_log_write('Eligible : ' || (eligible))

RETURN eligible
```

---

## Block 1: DEFAULT Declarations

```text
DEFAULT for PER_ASG_WORK_AT_HOME is 'NO_DATA'
DEFAULT for PER_ASG_LOC_REGION2 is 'NO_DATA'

DEFAULT_DATA_VALUE for PER_EXT_ORG_LOC_REGION2 is 'NO_REGION'
DEFAULT_DATA_VALUE for PER_EXT_ORG_ORGANIZATION_ID is 0
DEFAULT FOR PER_ASG_DEPARTMENT_ID IS 0
```

Two kinds of defaults here, and they do different things:

| Keyword | Used For | When It Kicks In |
| --- | --- | --- |
| DEFAULT for | Standard (single-value) DBIs | DBI returns no data — e.g., worker has no location assigned |
| DEFAULT_DATA_VALUE for | Array DBIs (extract org / multi-row) | A specific array index has a null/empty value for that column |

### Why 'NO_DATA' and 'NO_REGION'? Self-Documenting Defaults

Every default value in this formula is self-documenting**. When you read the ESS process log, the values tell you exactly what happened:

| Default Value | Used By | What It Means in the ESS Log |
| --- | --- | --- |
| 'NO_DATA' | PER_ASG_WORK_AT_HOME, PER_ASG_LOC_REGION2 | DBI returned null — worker has no value for this field in the database |
| 'NO_REGION' | PER_EXT_ORG_LOC_REGION2, l_loc (init value) | Department's org either wasn't found in the array, or the org row has no region configured |

When you read the ESS log, `Work State : NO_DATA` and `Department State : NO_REGION` immediately tell the consultant what happened without having to read the formula code.

**Why `l_loc` is initialized to `'NO_REGION'` (same as the DEFAULT_DATA_VALUE):** If the loop doesn't find a matching org, `l_loc` stays as `'NO_REGION'`. Tier 2 checks `l_loc != 'NO_REGION'` — false, so it falls to Tier 3. If `l_loc` were initialized to a different value, a no-match scenario would accidentally pass Tier 2's check and the worker would be eligible based on a meaningless init value.

---

## Block 2: Tier 0 — WAS DEFAULTED (Null Check)

The first IF in the eligibility chain isn't about PR or DC — it's about **missing data**:

```text
/* Tier 0: Bad data — critical DBIs returned null */
IF (PER_ASG_WORK_AT_HOME WAS DEFAULTED OR
    PER_ASG_LOC_REGION2 WAS DEFAULTED) THEN
(eligible = 'N')

ELSE

/* Tier 1: Remote worker — check assignment work state */
IF (PER_ASG_WORK_AT_HOME = 'Y' AND ...
...
```

If you've read the ["There Is No NULL in Fast Formula"](#) post, you know the background: **Fast Formula has no NULL. No `IS NULL`. No `= NULL`.** When a DBI returns null from the database, the engine silently replaces it with the DEFAULT value and sets an internal flag. `WAS DEFAULTED` checks that flag.

By making it the **first IF** in the chain, Tier 0 catches null data before Tiers 1–3 ever run. If it fires, `eligible = 'N'` and the remaining ELSE blocks are skipped naturally. No early RETURN. No extra flags. Just part of the same IF/ELSE chain.

### Why Tier 0 Matters

Without it, here's what happens when a worker has **no location assigned** (null in the database):

| Step | Without Tier 0 | With Tier 0 |
| --- | --- | --- |
| Database value | Location = NULL | Location = NULL |
| Formula sees | PER_ASG_LOC_REGION2 = 'NO_DATA' | PER_ASG_LOC_REGION2 = 'NO_DATA' |
| What happens | **'NO_DATA' != 'PR' is true** → worker passes eligibility with a default value | **WAS DEFAULTED = true** → Tier 0 fires, `eligible = 'N'`, remaining tiers skipped |
| Result | BUG — worker with no location passes | CORRECT — worker with no data excluded |

### The Pattern: DEFAULT + WAS DEFAULTED = Fast Formula's IS NULL

| SQL / PL/SQL | Fast Formula |
| --- | --- |
| IF x IS NULL | IF x WAS DEFAULTED |
| IF x IS NOT NULL | IF NOT x WAS DEFAULTED |
| NVL(x, 'default') | DEFAULT FOR x IS 'default' |

**Common mistake:** Checking the value instead of WAS DEFAULTED.

`IF PER_ASG_LOC_REGION2 = 'NO_DATA' THEN` — this compares against the default value. `WAS DEFAULTED` checks the engine's internal flag — it knows whether the database had null, regardless of the default value. Always use WAS DEFAULTED.

---

## Block 3: GET_CONTEXT + CHANGE_CONTEXTS + The Array Loop

This is the most complex block in the formula. Before looking at the code, let's understand the **problem it's solving**.

### Why Not Just Use PER_ASG_LOC_REGION2 for Everyone?

Because **the worker's assignment location and their department's location can be different states.** In Oracle HCM, two separate location fields exist:

| Field | Where It Lives | What It Answers |
| --- | --- | --- |
| Assignment Location | Worker's **assignment record** | "Where does this worker physically sit?" |
| Organization Location | **Department's org record** (Manage Organizations) | "Where is this department headquartered?" |

A worker could sit in NY Office (`PER_ASG_LOC_REGION2` = NY) but belong to a department headquartered in Puerto Rico (`PER_EXT_ORG_LOC_REGION2[i]` = PR). Two different location fields. Two different states. Same worker.

**Why can't we just use a single DBI for the department's state?** Because Oracle doesn't provide one out of the box. There's no `PER_ASG_DEPARTMENT_LOC_REGION2`. The department's location data lives at the organization level — the only way to access it from a formula is through the `PER_EXT_ORG_*` array DBIs. That means looping through all orgs and matching by ORGANIZATION_ID.

### How the Lookup Works

`PER_EXT_ORG_LOC_REGION2` returns the location state for **every organization** in the system that has a location configured. Your company might have 50 departments — the DBI dumps all of them into one array. We loop through it, find the row where the org ID matches the worker's department ID, and grab the state. It's doing a SQL JOIN manually — Fast Formula can't write SQL.

### What the Array Looks Like

| Row | PER_EXT_ORG_ORGANIZATION_ID | PER_EXT_ORG_LOC_REGION2 | Description |
| --- | --- | --- | --- |
| 1 | 3100 | 'NY' | Sales Dept — New York |
| 2 | 2200 | 'PR' | HR Dept — Puerto Rico |
| 3 | 4400 | 'TX' | Engineering Dept — Texas |
| 4 | 5500 | 'DC' | Finance Dept — Washington DC |

### What the Matching Code Is Really Doing

```text
IF PER_EXT_ORG_ORGANIZATION_ID[i] = PER_ASG_DEPARTMENT_ID THEN
(
    l_loc = PER_EXT_ORG_LOC_REGION2[i]
    EXIT
)
```

| Line | What it's really asking |
| --- | --- |
| ORGANIZATION_ID[i] = DEPARTMENT_ID | "Is the org at row [i] **the same org** as the department on this worker's assignment?" |
| l_loc = LOC_REGION2[i] | "Yes — so the location state on that org's record **is this worker's department state**. Grab it." |
| EXIT | "Found what we needed. Stop looking." |

The `IF` line connects the worker's world (assignment → department ID) to the organization's world (org record → location → state). The `l_loc` line crosses that bridge and pulls the value.

### The Code

```text
l_eff_date = get_context(EFFECTIVE_DATE, '1900/01/01 00:00:00'(date))

CHANGE_CONTEXTS (EFFECTIVE_DATE = l_eff_date)
(
    WHILE PER_EXT_ORG_LOC_REGION2.exists(i)  LOOP
    (
        IF PER_EXT_ORG_ORGANIZATION_ID[i] = PER_ASG_DEPARTMENT_ID THEN
        (
            l_loc = PER_EXT_ORG_LOC_REGION2[i]
            EXIT
        )

        i = i + 1
    )
)
```

| Line | What it does |
| --- | --- |
| get_context(EFFECTIVE_DATE, ...) | Reads EFFECTIVE_DATE from the engine's runtime into a local variable. |
| CHANGE_CONTEXTS (...) | Binds EFFECTIVE_DATE for the extract org DBIs inside the block. Standard DBIs pick up contexts automatically; extract org DBIs do not. |
| .exists(i) | **"Does row i exist?"** Returns false past the last row — loop stops. |
| i = i + 1 | Move to next row. When `.exists(5)` is false after row 4, loop ends naturally. |

---

## Why CHANGE_CONTEXTS? What Oracle's Docs Say

We're reading EFFECTIVE_DATE with `get_context()` and setting it back to the same value with `CHANGE_CONTEXTS`. Seems redundant — and Oracle's docs warn against exactly this in certain cases.

The **Administering Fast Formulas guide (24D)** says:

**Guidance 1:** *"The best practice approach is to use CHANGE_CONTEXTS statement only when required, because CHANGE_CONTEXTS can cause database item values to be fetched again from the database."*

**Guidance 2:** *"Don't use the CHANGE_CONTEXTS statement to set contexts that you would reasonably expect to be already set."*

Our formula looks like the anti-pattern. But it's not — because our DBI sits on a **different route**.

| Case | What You're Doing | Oracle Says |
| --- | --- | --- |
| Case 1 | Setting contexts **already bound** to standard routes | DON'T. Redundant. |
| Case 2 | DBI on a **different route** that doesn't auto-bind ← **Our formula** | DO. Required. |
| Case 3 | Override context to a **different value** (time-travel) | DO. |

From the [REL11 data ↗](https://www.scribd.com/document/511029660/HCM-Extract-DBI-List-REL11-updated): `PER_ASG_WORK_AT_HOME` uses route `PER_ASG_ASSIGNMENT_DETAILS` (auto-bound). `PER_EXT_ORG_LOC_REGION2` uses route `PER_EXT_SEC_ORGANIZATION` (NOT auto-bound). Same syntax as the anti-pattern, but different route, different reason.

Oracle's own [Sample Formula 3 ↗](https://docs.oracle.com/en/cloud/saas/human-resources/oapff/participation-and-rate-eligibility.html) on the Participation and Rate Eligibility docs page uses this exact pattern: `GET_CONTEXT` → `CHANGE_CONTEXTS` → `.exists(i)` loop → `RETURN ELIGIBLE`.

**What happens if you skip CHANGE_CONTEXTS?** The formula compiles. Runs without error. `.exists(i)` returns false immediately (empty array), the loop never executes, `l_loc` stays as `'NO_REGION'`, and the formula falls to Tier 3. No crash — just silently wrong results. If ESS log shows `Department State : NO_REGION` for a worker whose department *does* have a location, this is the first thing to check.

---

## Tracing the Loop Step by Step

Worker is in Department **4400** (Engineering). `PER_ASG_DEPARTMENT_ID` = 4400. `i` starts at 1.

| ITERATION 1 — i = 1

Read `ORGANIZATION_ID[1]` | → **3100** (Sales) |
| --- | --- |
| 3100 = 4400? | → **NO** → `i = 2` |

ITERATION 2 — i = 2

| Read `ORGANIZATION_ID[2]` | → **2200** (HR) |
| --- | --- |
| 2200 = 4400? | → **NO** → `i = 3` |

ITERATION 3 — i = 3 ✔ MATCH

| Read `ORGANIZATION_ID[3]` | → **4400** (Engineering) |
| --- | --- |
| 4400 = 4400? | → **YES!** |
| Read `LOC_REGION2[3]` | → **'TX'** |
| Action: | `l_loc = 'TX'` then `EXIT` |

ROW 4 — never reached

EXIT already fired. Formula continues with `l_loc = 'TX'`. TX is not PR or DC → eligible.

---

## Block 4: The Eligibility Decision Chain (Tiers 0–3)

```text
/* Tier 0: Bad data — critical DBIs returned null */
IF (PER_ASG_WORK_AT_HOME WAS DEFAULTED OR
    PER_ASG_LOC_REGION2 WAS DEFAULTED) THEN
(eligible = 'N')

ELSE

/* Tier 1: Remote worker — check assignment work state */
IF (PER_ASG_WORK_AT_HOME = 'Y' AND
   (PER_ASG_LOC_REGION2 != 'PR' AND
    PER_ASG_LOC_REGION2 != 'DC'))
THEN (eligible = 'Y')

ELSE

/* Tier 2: Office worker — check department org location */
IF (PER_ASG_WORK_AT_HOME = 'N' AND
   (l_loc != 'PR' AND l_loc != 'DC') AND
    l_loc != 'NO_REGION')
THEN (eligible = 'Y')

ELSE

/* Tier 3: Fallback — no dept state, use assignment location */
IF (PER_ASG_WORK_AT_HOME = 'N' AND l_loc = 'NO_REGION' AND
   (PER_ASG_LOC_REGION2 != 'PR' AND
    PER_ASG_LOC_REGION2 != 'DC'))
THEN (eligible = 'Y')

ELSE eligible = 'N'
```

| Tier | What it checks | Why this tier exists |
| --- | --- | --- |
| Tier 0 | WAS DEFAULTED — Work at Home or Work State is null | Catches missing data before it infects the decision chain |
| Tier 1 | Work at Home = Y AND work state not PR/DC | Remote workers — check assignment work location state |
| Tier 2 | `l_loc` not PR/DC AND `l_loc != 'NO_REGION'` | Office workers — department has a location state configured |
| Tier 3 | `l_loc = 'NO_REGION'` AND assignment loc not PR/DC | Fallback — no department state found |
| ELSE | None of the above | Worker is in PR or DC — excluded |

---

## Block 5: Debug Logging

```text
l = ess_log_write('Work at Home : ' || (PER_ASG_WORK_AT_HOME))
l = ess_log_write('Work State : ' || (PER_ASG_LOC_REGION2))
l = ess_log_write('Department State : ' || (l_loc))
l = ess_log_write('Eligible : ' || (eligible))
```

Four log lines. The self-documenting defaults make the ESS output immediately readable:

| Log Line | Worker A**(Remote in TX) | Worker B(Office, PR dept) | Worker C(No dept state) | Worker D(No location) |
| --- | --- | --- | --- | --- |
| Work at Home | Y | N | N | NO_DATA |
| Work State | TX | NY | FL | NO_DATA |
| Department State | NO_REGION | PR | NO_REGION | NO_REGION |
| Eligible | Y | N | Y | N |
| Tier that fired | Tier 1 | Tier 2 | Tier 3 | Tier 0 |

Worker D** is the new one — no location assigned at all. Without Tier 0, they'd pass eligibility on a fake default value. With Tier 0, `WAS DEFAULTED` catches it immediately. And the ESS log shows `NO_DATA` — the consultant knows exactly what happened without reading the formula.

**Debugging tip:** If Department State shows `'NO_REGION'` for a worker who should be using Tier 2, either (a) CHANGE_CONTEXTS didn't resolve the ext org array — check your CHANGE_CONTEXTS block, or (b) the loop ran but no org matched — check the department's location setup in Manage Organizations.

---

## DBI Reference — All 5 DBIs from the REL11 Export ↗

| DBI | Description | SQL Column | Contexts Used | Multi-Row |
| --- | --- | --- | --- | --- |
| PER_ASG_WORK_AT_HOME | Work at Home flag | paf_asg.work_at_home | EFFECTIVE_DATE, HR_ASSIGNMENT_ID | N |
| PER_ASG_LOC_REGION2 | Assignment Location State | hrloc.region_2 | EFFECTIVE_DATE, HR_ASSIGNMENT_ID | N |
| PER_ASG_DEPARTMENT_ID | Department Org ID | paf_asg.ORGANIZATION_ID | EFFECTIVE_DATE, HR_ASSIGNMENT_ID | N |
| PER_EXT_ORG_ORGANIZATION_ID | Extract Org ID (per row) | org.ORGANIZATION_ID | EFFECTIVE_DATE | Y |
| PER_EXT_ORG_LOC_REGION2 | Extract Org Location Region2 | hla.REGION_2 | EFFECTIVE_DATE | Y |

---

## Bonus: The DBI X-Ray Query

The [REL11 export ↗](https://www.scribd.com/document/511029660/HCM-Extract-DBI-List-REL11-updated) gives you metadata in a spreadsheet. But if you want the **actual SQL** Oracle runs — run this in BI Publisher:

```text
SELECT d.base_user_name         DBI_NAME
,      d.data_type               DBI_DATA_TYPE
,      d.definition_text         SELECT_CLAUSE
,      r.text                    WHERE_CLAUSE
,      (SELECT LISTAGG(
         '', ', ')
         WITHIN GROUP (ORDER BY rcu.sequence_no)
       FROM   ff_route_context_usages rcu
       ,      ff_contexts_b c
       WHERE  rcu.route_id = r.route_id
       AND    rcu.context_id = c.context_id
       )                         ROUTE_CONTEXT_USAGES
FROM   ff_database_items_b d
,      ff_user_entities_b u
,      ff_routes_b r
WHERE  d.base_user_name = 'PER_EXT_ORG_LOC_REGION2'
AND    d.user_entity_id = u.user_entity_id
AND    r.route_id = u.route_id
```

Replace the DBI name to see any DBI's internals. Check three things before writing formula code: (1) do the arrays share a route? (2) do you need CHANGE_CONTEXTS? (3) single value or array?

---

## Key Takeaways

**Guard with WAS DEFAULTED (Tier 0) before the main logic** — if a critical DBI returns null, the engine substitutes the default and the IF chain can produce wrong results. `WAS DEFAULTED` catches nulls. There is no `IS NULL` in Fast Formula — `DEFAULT` + `WAS DEFAULTED` is the null-handling system.

**CHANGE_CONTEXTS is mandatory for extract org DBIs** — even when setting the context to the same value. Without it, the ext org route has no bound EFFECTIVE_DATE and silently returns nothing.

**Use self-documenting default values** — `'NO_DATA'` and `'NO_REGION'` make the ESS log immediately readable. Initialize `l_loc` to the same value as DEFAULT_DATA_VALUE so "loop didn't match" and "matched but null" both fall correctly to Tier 3.

**Assignment location ≠ department location** — `PER_ASG_LOC_REGION2` is where the worker sits. `PER_EXT_ORG_LOC_REGION2[i]` is where the department is headquartered. The array loop bridges the two using ORGANIZATION_ID as the join key.

**Always verify DBIs against the [REL11 export ↗](https://www.scribd.com/document/511029660/HCM-Extract-DBI-List-REL11-updated)** — check CONTEXTS_USED, MULTI_ROW_FLAG, and route name. Use the DBI X-Ray query to see the actual SQL.

This Participation and Rate Eligibility formula ties together most of what we've covered in the previous posts: contexts, DBIs, routes, array looping, CHANGE_CONTEXTS, WAS DEFAULTED null-handling, and debug logging.

If you're on the functional team and you understood this formula — the WAS DEFAULTED guard for null data, the three-tier fallback chain, how CHANGE_CONTEXTS binds to a non-standard route, how the array loop matches org IDs, and why the sentinel default drives the decision logic — you can write any Participation and Rate Eligibility formula. The business rules will change, the excluded states will change, the DBIs might change. But the pattern is always the same: resolve the data, check the condition, return `ELIGIBLE`. Everything else is just variations of what you've already seen here. Fast Formula isn't just for technical consultants — if a functional consultant understands the logic flow, they can build these formulas too.

Hope this helps someone.

Abhishek Mohanty
