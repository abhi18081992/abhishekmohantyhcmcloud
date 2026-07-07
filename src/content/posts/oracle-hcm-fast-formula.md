---
title: "Oracle HCM Fast Formula Series:GET_CONTEXT and CHANGE_CONTEXTS: The Two Context Statements You Actually Need"
description: "Fast FormulaContext HandlingIntermediateVerified"
pubDate: 2026-04-12
tags: ["Fast Formula", "Oracle HCM Cloud", "DBI", "CHANGE_CONTEXTS"]
---

Fast FormulaContext HandlingIntermediateVerified


# Oracle Fast Formula: GET_CONTEXT and CHANGE_CONTEXTS — The Two Context Statements You Actually Need


April 2026 · 10 min read · Oracle HCM Cloud


Oracle Fast Formula has two context-handling statements that every developer eventually needs to master: one reads the engine's current context values, the other temporarily overrides them. They look similar but do opposite things — and confusing them is one of the most common sources of silent bugs in production formulas. This post walks through both as diagrams first, code second, with a production-grade example at the end.


AM


**Abhishek Mohanty**Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant


## How a DBI Reference Becomes a SQL Query


Every time you write `l_name = PER_PER_FULL_NAME`, five things happen in sequence. The calling application populates the context layer. Your DBI reference triggers a route lookup. The route builds SQL. The contexts bind into that SQL as `:PID` and `:EFF`. The database returns a value.


Calling Application
Absence · OTL · Comp
injects context values


Context Layer
PERSON_ID = 4001
EFF_DATE = 15-Mar-26


Your Formula
l_name =
PER_PER_FULL_NAME

triggers DBI

HIDDEN SQL ROUTE
SELECT full_name
FROM   per_person_names_f
WHERE  person_id = :PID
AND    name_type = 'GLOBAL'
AND    :EFF BETWEEN eff_start_date AND eff_end_date

contexts bind as :PID, :EFF


Database
returns "Priya Patel"
back into l_name

Fig 1 — Contexts act as SQL bind variables between your formula and the database


This happens thousands of times per formula run, invisible to you — and it's why context statements matter. They're the only way to inspect or manipulate the bind-variable layer. Two statements do the real work: GET_CONTEXT reads, CHANGE_CONTEXTS writes.


## GET_CONTEXT vs CHANGE_CONTEXTS — Read vs Write


The first question developers ask: if GET_CONTEXT reads the current value and CHANGE_CONTEXTS overrides it, why not use just one of them? Because they solve opposite problems. One captures the state the engine injected. The other temporarily substitutes different state so your DBIs can resolve data from a different viewpoint.


Same context, opposite operations


Context Layer (engine-managed)
EFFECTIVE_DATE = 15-Mar-2026
injected by the calling application


GET_CONTEXT — READ
copies current value into
a local variable

l_eff = GET_CONTEXT(EFFECTIVE_DATE, d)
context layer unchanged


CHANGE_CONTEXTS — WRITE
temporarily overrides value
inside a scoped block

CHANGE_CONTEXTS(EFFECTIVE_DATE=d2)(...)
auto-reverts on block exit

Fig 2 — GET_CONTEXT pulls the current value out. CHANGE_CONTEXTS pushes a new value in (scoped).


The rest of this post walks through each statement in depth, then puts them together in an end-to-end example from absence management.


## GET_CONTEXT — Reading the Engine's Current State


GET_CONTEXT takes two arguments: the context name (unquoted) and a typed default that matches the context's data type. Use `0` for numbers, `' '` for text, `'4712/12/31 00:00:00' (date)` for dates. Forget the default and the formula won't compile.


The returned value lives in your local variable from that point until you overwrite it. GET_CONTEXT is purely a reader — it never modifies the context layer, so it's safe to call repeatedly and in any order.


### Real Example — Capturing contexts at the top of a formula


```
l_person_id = GET_CONTEXT(PERSON_ID, 0)
l_asg_id    = GET_CONTEXT(HR_ASSIGNMENT_ID, 0)
l_eff_dt    = GET_CONTEXT(EFFECTIVE_DATE, '4712/12/31 00:00:00' (date))
```


Three reads into three locals. From this point onward, any branching logic can use these values — including decisions about whether to enter a CHANGE_CONTEXTS block and with what override values.


## CHANGE_CONTEXTS — Temporarily Overriding State


CHANGE_CONTEXTS temporarily overrides one or more context values inside a scoped block. Every DBI fetch and function call that runs inside the block uses the overridden values. The moment execution exits the closing parenthesis, the context layer reverts to whatever it was before. You never write restore code — the engine handles it.


```
CHANGE_CONTEXTS(PERSON_ID = l_mgr_pid, EFFECTIVE_DATE = l_target_date)
(
  /* Inside this block, all DBIs resolve for the manager as of target date */
  l_mgr_name      = PER_PER_FULL_NAME
  l_mgr_hire_date = PER_PERSON_ENTERPRISE_HIRE_DATE
)
/* Out here, contexts are back to the original values */
```


### About the brackets — read carefully


Without parentheses, CHANGE_CONTEXTS applies its override to exactly the next single statement. It does not silently fail. It just scopes very narrowly. The moment you have two or more statements that need the new context, you must enclose them in `( )`. In practice, always use brackets. Single-statement scoping is a trap that breaks the instant someone adds a second line.


### Combine, don't nest


If you need to change three contexts, put them all in one CHANGE_CONTEXTS call. Oracle's Administering Fast Formulas guide is explicit: *"Use CHANGE_CONTEXTS only when required, because CHANGE_CONTEXTS can cause database item values to be fetched again from the database. You can perform multiple context changes using a single CHANGE_CONTEXTS statement, instead of calling CHANGE_CONTEXTS from other CHANGE_CONTEXTS blocks."*


Every context you change forces the engine to invalidate cached DBI values for routes that use that context. Changing PERSON_ID when you only need to change EFFECTIVE_DATE is a hidden performance penalty.


### The lifecycle


| Phase | What happens |

| 1. Before | Original contexts: PERSON_ID = 4001, EFFECTIVE_DATE = 2026-03-15 |

| 2. Enter | CHANGE_CONTEXTS(PERSON_ID = 5002, EFFECTIVE_DATE = 2024-01-01) |

| 3. Inside | Every DBI resolves for person 5002 as of January 2024 |

| 4. Exit | Closing parenthesis reached |

| 5. After | Auto-restored to PERSON_ID = 4001, EFFECTIVE_DATE = 2026-03-15 |


## End-to-End Example — Compassionate Leave Manager Tenure Check


The client policy: when an employee applies for Compassionate Leave, verify that the line manager has been employed for at least 90 days as of the absence start date. If the manager is too new, reject the submission with an informative message so BPM approval routing can re-route the request through the skip-level chain.


This is a **Global Absence Entry Validation** formula. The calling application sets PERSON_ID, HR_ASSIGNMENT_ID, and EFFECTIVE_DATE contexts automatically, plus a set of standard input values (IV_START_DATE, IV_END_DATE, IV_ABSENCE_TYPE_ID, and others) passed into the formula. The contract with the engine is strict: the formula must return exactly two predefined variables — `VALID` (`'Y'` or `'N'`) and `ERROR_MESSAGE` (the text shown to the user on rejection). Everything else is your own logic.


We need the manager's hire date — but the manager's data sits behind a different PERSON_ID than the one the engine injected. That's exactly what CHANGE_CONTEXTS exists for. We also need to read the hire date *as of the absence start date*, not as of today — which means overriding EFFECTIVE_DATE inside the same block.


| Step | What it does | Statement / DBI |

| 1 | Declare INPUTS and DEFAULT FOR every DBI, input, and return variable used | INPUTS ARE / DEFAULT FOR |

| 2 | Read PERSON_ID for traceability — EFFECTIVE_DATE is implicit and will be overridden later | GET_CONTEXT |

| 3 | Fetch the manager's person ID in the original employee context | PER_ASG_MANAGER_PERSON_ID *(verify in your pod via DBI X-Ray query)* |

| 4 | Initialise VALID and ERROR_MESSAGE to approval defaults — reject only on explicit failure | VALID = 'Y' |

| 5 | If no manager on assignment, reject with an informative message | IF l_mgr_pid = 0 THEN |

| 6 | Otherwise, switch context to manager + absence start date, read hire date, compute tenure | CHANGE_CONTEXTS |

| 7 | Return VALID and ERROR_MESSAGE — the Global Absence Entry Validation return contract | RETURN VALID, ERROR_MESSAGE |


### Real Example — XX_COMPASSIONATE_LV_ENTRY_VAL


```
/******************************************************
 * FORMULA : XX_COMPASSIONATE_LV_ENTRY_VAL
 * TYPE    : Global Absence Entry Validation
 * RETURNS : VALID ('Y'/'N') + ERROR_MESSAGE (text)
 * NOTE    : DBI names should be verified in your pod via
 *           the DBI X-Ray query.
 ******************************************************/

/*=========== INPUTS ==============================================*/
INPUTS ARE IV_START_DATE      (date),
           IV_END_DATE        (date),
           IV_ABSENCE_TYPE_ID (number)

/*=========== DBI DEFAULTS ========================================*/
DEFAULT FOR PER_ASG_MANAGER_PERSON_ID       IS 0
DEFAULT FOR PER_PER_FULL_NAME                IS 'Unknown'
DEFAULT FOR PER_PERSON_ENTERPRISE_HIRE_DATE IS '1901/01/01 00:00:00' (date)

/*=========== RETURN + INPUT DEFAULTS =============================*/
DEFAULT FOR VALID              IS 'Y'
DEFAULT FOR ERROR_MESSAGE      IS ' '
DEFAULT FOR IV_START_DATE      IS '4712/12/31 00:00:00' (date)
DEFAULT FOR IV_END_DATE        IS '4712/12/31 00:00:00' (date)
DEFAULT FOR IV_ABSENCE_TYPE_ID IS 0

/*=========== CONSTANTS ===========================================*/
l_threshold = 90

/*=========== CALCULATION =========================================*/

/* Step 1: Read PERSON_ID context */
l_emp_pid  = GET_CONTEXT(PERSON_ID, 0)
l_emp_name = PER_PER_FULL_NAME

/* Step 2: Fetch manager ID in the original employee context */
l_mgr_pid = PER_ASG_MANAGER_PERSON_ID

/* Step 3: Initialise return variables — default to approval */
VALID         = 'Y'
ERROR_MESSAGE = ' '

/* Step 4: Branch on whether a manager exists on the assignment */
IF l_mgr_pid = 0 THEN
(
  VALID         = 'N'
  ERROR_MESSAGE = 'Your assignment does not have a reporting manager. '
               || 'Please contact HR before applying for Compassionate Leave.'
)
ELSE
(
  /* Step 5: Switch to manager context, read hire date as of absence start date */
  CHANGE_CONTEXTS(PERSON_ID = l_mgr_pid, EFFECTIVE_DATE = IV_START_DATE)
  (
    l_mgr_name      = PER_PER_FULL_NAME
    l_mgr_hire_date = PER_PERSON_ENTERPRISE_HIRE_DATE
    l_tenure_days   = DAYS_BETWEEN(IV_START_DATE, l_mgr_hire_date)

    IF l_tenure_days


Same employee, same manager, different EFFECTIVE_DATE = different tenure


Nov 2, 2025
manager hired


Jan 5, 2026
user submits leave request
(EFFECTIVE_DATE)


Feb 10, 2026
absence starts
(IV_START_DATE)


64 days


100 days


— 90 day policy threshold —


✗ Without override
EFFECTIVE_DATE = Jan 5, 2026
Manager tenure =
64 days

Below 90 → VALID = 'N'
but this isn't the right answer


✓ With CHANGE_CONTEXTS override
EFFECTIVE_DATE = Feb 10, 2026
Manager tenure =
100 days

Above 90 → VALID = 'Y'
which is the correct answer

Fig 3 — Manager hired Nov 2, 2025. As of the submission date the tenure is 64 days; as of the absence start date it's 100 days. The business rule cares about the latter.


**Why the formula rejects instead of routing.** Global Absence Entry Validation has a strict binary contract: `VALID = 'Y'` lets the submission proceed, `VALID = 'N'` blocks it and shows `ERROR_MESSAGE` to the user. The formula cannot re-route the request on its own — that's what BPM approval rules are for. The correct pattern is: reject with a clear message, and configure the BPM approval rule to recognise the rejection and trigger the skip-level routing. Trying to route from inside the formula itself is a category error that breaks the formula-type contract.


Two layers, two responsibilities — don't mix them

Layer 1 — Formula (what your Fast Formula does)

Entry Validation
checks tenure
sets VALID + MESSAGE


Absence engine
reads VALID = 'N'
surfaces ERROR_MESSAGE


User sees message
"Manager tenure
below 90 days..."

Formula finishes here. BPM starts here.

Layer 2 — BPM (what the approval rule does)

Approval rule
detects rejection pattern
in ERROR_MESSAGE text


Skip-level routing
bypasses direct manager
sends to grandmanager


Approved
by skip-level
manager

Fig 4 — Formula returns VALID / ERROR_MESSAGE. BPM reads the rejection and handles routing separately.


## Pitfalls to Avoid


| # | Pitfall |

| 1 | **Omitting brackets after CHANGE_CONTEXTS** when more than one statement needs the override. Only the immediately following statement runs under the new context. Always use brackets. |

| 2 | **Nesting when combining would suffice.** Two separate nested calls can almost always be replaced with one combined call. |

| 3 | **Restating already-set contexts.** Achieves nothing functionally but forces unnecessary DBI cache invalidation. |

| 4 | **Forgetting the default in GET_CONTEXT.** Compile error if you omit the second argument. |

| 5 | **Using a context the formula type does not support.** Runtime error. Check the formula type documentation first. |

| 6 | **Overriding PERSON_ID when you only need to change EFFECTIVE_DATE.** Every context you override forces DBI cache invalidation for every route that uses that context. Change only what you need. |


## A brief mention — CONTEXT_IS_SET


For completeness: Oracle Fast Formula also exposes a third context-handling statement called `CONTEXT_IS_SET(name)`. It takes a single argument and returns TRUE or FALSE depending on whether the calling application populated the context. It's narrower in scope than GET_CONTEXT and CHANGE_CONTEXTS — most production formulas never need it — but it's worth knowing the keyword exists so you recognise it in legacy code. The practical rule: if your formula type supports a given context, the calling application will set it; if it doesn't support that context, CHANGE_CONTEXTS is how you provide a value. CONTEXT_IS_SET fills the narrow gap where you need to distinguish "set to zero" from "never set at all" — a distinction that matters in a small number of edge cases, typically around optional plan or payroll contexts.


## Key Takeaways


**Two statements, two directions.** GET_CONTEXT reads. CHANGE_CONTEXTS writes. Every context-handling pattern in Fast Formula is built from these two operations.


**GET_CONTEXT needs two arguments, always.** The context name and a typed default. Forget the default and the formula won't compile.


**CHANGE_CONTEXTS auto-restores.** Never write restore code. The engine handles save-and-swap on entry and restore on exit. Trust the scoping.


**Combine, don't nest.** One CHANGE_CONTEXTS call with multiple assignments beats nested calls every time. Oracle's docs say so explicitly, and the cache-invalidation cost makes it a real best practice.


**Change only what you need.** Every overridden context invalidates DBI caches. Be surgical.


AM


**Abhishek Mohanty**Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time and Labor, Core HR, Redwood, HDL, OTBI.