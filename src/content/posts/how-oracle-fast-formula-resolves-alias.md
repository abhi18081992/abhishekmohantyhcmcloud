---
title: "How Oracle Fast Formula resolves ALIAS at compile time: statement order, reference-vs-snapshot semantics, CHANGE_CONTEXTS re-evaluation, and the three compiler errors."
description: "The ALIAS Statement in Oracle Fast Formula — Compile-Time Reference, Statement Order, CHANGECONTEXTS Re-evaluation, and the Three Compiler Errors Every HCM Cloud Consultant Must Know"
pubDate: 2026-05-16
tags: ["Fast Formula", "Oracle HCM Cloud", "Null Handling", "DBI", "CHANGE_CONTEXTS"]
---

The ALIAS Statement in Oracle Fast Formula — Compile-Time Reference, Statement Order, CHANGE_CONTEXTS Re-evaluation, and the Three Compiler Errors Every HCM Cloud Consultant Must Know
- FAST FORMULA
  ALIAS STATEMENT
  DEEP DIVE


# Oracle Fast Formula ALIAS: How the Compiler Resolves Long DBI Names at Parse Time and Why It's Not Just a Typing Convenience


A definitive walkthrough of compile-time reference semantics, statement ordering, the reference-vs-snapshot distinction, CHANGE_CONTEXTS re-evaluation, and the three compiler errors every Fast Formula author has hit at least once.

May 8, 2026 • 16 min read • Oracle HCM Cloud

Database item names in Fusion HCM Fast Formulas routinely run past thirty characters. `PER_ASG_REL_LENGTH_OF_SERVICE`. `CMP_ASSIGNMENT_RGE_SALARY_CHANGE_AMOUNT`. `PER_HIST_ASG_EFFECTIVE_START_DATE`. Reference one of these eight times in a single formula and the calculation logic disappears under the noise. Oracle's documented answer is the `ALIAS` statement — a single keyword, an `AS` clause, a target identifier. But ALIAS is more than a typing shortcut. It's a compile-time reference, not a runtime variable, and that distinction matters more than most authors realise.


  AM
  **Abhishek Mohanty**Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant


Fast Formula has no debugger. It also has no convenient way to fold a 38-character DBI reference into something readable — except for ALIAS. Authors who reach for `L_VAR = LONG_DBI_NAME` instead end up with a snapshot variable that silently breaks under `CHANGE_CONTEXTS`, and they don't find out until a salary delta computes to zero in production.

This post covers what ALIAS actually does at the language level, where it must sit in your statement order, why it's not interchangeable with a local-variable assignment, the three compiler errors you'll hit, and the production conventions that keep aliased formulas readable six months after go-live.


## ALIAS in the Five-Section Formula Structure


Before going deep into ALIAS semantics, it helps to see where ALIAS sits in the larger Fast Formula skeleton. Every formula you'll ever write follows the same five-section template, in exactly this order:


PositionSectionPurpose

**1**`ALIAS`Shortens long DBI names. Compile-time symbol binding.
**2**`DEFAULT FOR`Null-handling for database items, including aliased ones.
**3**`INPUTS ARE`Typed parameters passed in by the calling formula type.
**4**Calculation bodyAssignments, IF / THEN / ELSE, function calls — the actual logic.
**5**`RETURN`One or more values handed back to the calling application.


A complete minimal formula showing all five sections in order:

ALIAS CMP_ASSIGNMENT_SALARY_AMOUNT AS ASG_SAL        /* 1. ALIAS — shortens the DBI         */
ALIAS ASG_HR_ASG_ID                AS ASG_ID         /*    one alias per line               */

DEFAULT FOR ASG_SAL IS 0                              /* 2. DEFAULT — null handling          */
DEFAULT FOR ASG_ID  IS 0

INPUTS ARE BONUS_PERCENTAGE                          /* 3. INPUTS — typed parameters        */

L_BONUS = ASG_SAL * (BONUS_PERCENTAGE / 100)              /* 4. CALCULATION — the logic itself   */

RETURN L_BONUS, ASG_ID                                 /* 5. RETURN — values passed back      */

One structural fact about ALIAS matters for understanding everything that follows: **ALIAS resolution happens at compile time, not at runtime.** By the time the runtime execution begins, every alias has already been substituted with the underlying DBI's fetch logic. The alias has no independent existence at runtime — it's a label the compiler removes.

This second point is the key insight the rest of this post unpacks. Because ALIAS is resolved before the formula body even starts running, the alias inherits the semantic properties of the underlying DBI — lazy evaluation, context-sensitive re-fetching, `WAS DEFAULTED` compatibility — that a local-variable assignment cannot reproduce.


## How the Compiler Resolves an Alias


The Oracle *Administering Fast Formulas* guide defines ALIAS as a statement that gives a Database Item a shorter, formula-local name. The guide explicitly recommends ALIAS over assigning a DBI to a local variable for the purpose of shortening — because the alias is a reference, not a copy.

The binding happens at compile time. The compiler builds a symbol table that maps both the long DBI name and your short alias to the same metadata handle:


Database ItemAlias

`PER_ASG_REL_LENGTH_OF_SERVICE``ASG_LOS`
`CMP_ASSIGNMENT_SALARY_AMOUNT``ASG_SAL`
`PER_ASG_JOB_NAME``ASG_JOB`
`ASG_HR_ASG_ID``ASG_ID`


Figure 1 · Compile-Time Binding

  declared by ALIAS

  CMP_ASSIGNMENT_SALARY_AMOUNT

  ASG_SAL




  resolves to

  ONE METADATA
  HANDLE

  Both names share the same route, user-entity, and context dependency.

**One handle, two labels.** Reading either name at runtime triggers the same DBI fetch under whichever contexts are active.


Four things happen behind the scenes when you write the ALIAS line:


What the compiler does with each ALIAS declaration

STEP 1You write the ALIAS line: `ALIAS PER_ASG_REL_LENGTH_OF_SERVICE AS ASG_LOS` at the top of the formula.
STEP 2The compiler records both names — long DBI and short alias — as labels pointing to the same route and user-entity in the formula metadata. They become two names for one underlying handle.
STEP 3Every later reference to the alias in the formula body resolves to the exact same DBI fetch logic that the long name would have produced. The substitution is complete before any runtime execution.


The alias is a label processed at compile time. There is no runtime storage allocated to it, and no separate value held against it. Every reference is a fresh evaluation of the underlying DBI under whatever contexts are active at the point of reference.


## Syntax and the Reserved Identifier List


The form is fixed. One alias declaration per line:

ALIAS DATABASE_ITEM_NAME AS SHORT_NAME

Three things to know about the syntax:


**The `AS` keyword is required.** Both `ALIAS` and `AS` are reserved — neither can be used as a variable name elsewhere in the formula.

- **Case-insensitive.** `ALIAS x AS Y` and `alias X as y` compile identically. Pick a casing convention and apply it consistently.

- **One alias per line.** No comma-separated multi-alias declarations.


The alias name on the right of `AS` can't collide with any reserved word in the language. The reserved identifiers fall into six categories:


| Category | Reserved identifiers |


| **Declaration & section statements** | `ALIAS`, `AS`, `DEFAULT`, `DEFAULT_DATA_VALUE`, `DEFAULTED`, `FOR`, `INPUTS`, `ARE`, `USING`, `RETURN` |

| **Control flow** | `IF`, `THEN`, `ELSE`, `WHILE`, `LOOP`, `EXIT` |

| **Logical & comparison operators** | `AND`, `OR`, `NOT`, `IS`, `LIKE`, `WAS` |

| **Context management** | `CHANGE_CONTEXTS`, `GET_CONTEXT`, `CONTEXT_IS_SET`, `NEED_CONTEXT` |

| **Formula execution & I/O** | `EXECUTE`, `IS_EXECUTABLE`, `SET_INPUT`, `GET_OUTPUT` |

| **Working storage area** | `WSA_GET`, `WSA_SET`, `WSA_EXISTS`, `WSA_DELETE` |


If your formula won't compile and you've named your alias something like `DEFAULT`, `FOR`, or `IS` — that's why. Add a prefix or suffix to escape: `L_DEFAULT`, `FOR_DT`, `IS_FLAG`.


## Statement Order: Why ALIAS Comes First


Fast Formula enforces a strict ordering of declarative statement sections. The order is documented in the Oracle *Administering Fast Formulas* guide, and the compiler will reject your formula with *"Incorrect Statement Order"* if you break it.


| Required statement order — top to bottom |


| FIRST**ALIAS** — all alias declarations, grouped together at the top of the formula. |

| SECOND**DEFAULT FOR** and **DEFAULT_DATA_VALUE FOR** — scalar and array DBI defaults. |

| THIRD**INPUTS ARE** — single block, all input parameters typed. |

| FOURTH**Body and RETURN** — logic, control flow, assignments, and the return statement. |


### What going out of order looks like


The mistake is genuinely common when you're refactoring an existing formula and adding an alias mid-file. Wrong:


DEFAULT FOR ASG_HR_ASG_ID IS 0      /* DEFAULT before ALIAS */

ALIAS PER_ASG_JOB_NAME AS ASG_JOB     /* ← raises the error */

INPUTS ARE EFFECTIVE_DATE_FROM (DATE)


Incorrect Statement Order — ALIAS, DEFAULT, or INPUT statements come after other statements.


Right:


ALIAS PER_ASG_JOB_NAME AS ASG_JOB

DEFAULT FOR ASG_HR_ASG_ID IS 0
DEFAULT FOR ASG_JOB IS ' '

INPUTS ARE EFFECTIVE_DATE_FROM (DATE)


When adding a new alias to an existing formula, scroll to the top, find the existing ALIAS block, and add the line there. Never insert it next to the DEFAULT or DBI it relates to — that breaks the ordering rule.


## What You Can & Cannot Alias


The Fusion 24D *Administering Fast Formulas* guide narrows ALIAS to one target type: database items. The compiler diagnostic for invalid targets is unambiguous: *"you can use an ALIAS statement only for a database item."* The practical test is the Database Items picker in the formula editor — if the identifier appears there for your current formula type, it's aliasable; if it doesn't, it isn't.


### What ALIAS will accept


| Aliasable | Notes |


| **Scalar DBIs** | The standard case. Any DBI returning a single text, number, or date value under the formula type's contexts. |

| **Array DBIs** | Grammatically aliasable. Oracle docs are silent — no worked example in the 24D guide — but the language accepts it. Test in your environment before relying on it. |


### What ALIAS will not accept


Five identifier categories produce compilation failures. The diagnostic, the cause, and a reproduction case for each:


#### 1. Local variables


Local variables don't exist until the formula's first assignment statement creates them. ALIAS lines run before any assignment, so the symbol has no metadata to bind to.


ALIAS L_TEMP_VALUE AS TMP        /* L_TEMP_VALUE is a local var, not a DBI */


Misuse of ALIAS Statement — you can use an ALIAS statement only for a database item.


#### 2. Inputs from INPUTS ARE


Inputs are bound to the formula via the formula type definition. They're not DBIs and they're already short. There's no metadata layer to alias.


ALIAS EFFECTIVE_DATE_FROM AS EFF_DT   /* declared in INPUTS ARE */


Misuse of ALIAS Statement — you can use an ALIAS statement only for a database item.


#### 3. Contexts


Contexts like `HR_ASSIGNMENT_ID`, `EFFECTIVE_DATE`, `ABSENCE_PLAN_ID`, `PERSON_ID` are language-level handles for the current evaluation state, not data records. Read them via `GET_CONTEXT`.


ALIAS HR_ASSIGNMENT_ID AS AID         /* contexts are not DBIs */

/* Correct method for context access: */
L_AID = GET_CONTEXT(HR_ASSIGNMENT_ID, -1)


Misuse of ALIAS Statement — you can use an ALIAS statement only for a database item.


#### 4. Formula functions


Functions like `GET_VALUE_SET`, `DAYS_BETWEEN`, `ESS_LOG_WRITE`, `GET_RATE`, `TO_CHAR`, `SUBSTR` are callable, not data. They take parameters and return values; they don't *have* a value to alias.


ALIAS DAYS_BETWEEN AS DB             /* functions cannot be aliased */


Misuse of ALIAS Statement — you can use an ALIAS statement only for a database item.


#### 5. DBIs not visible to your formula type


The trickiest case because it *looks* correct. The DBI exists in the dictionary somewhere. But your current formula type doesn't supply the contexts the DBI's route needs, so for your formula it doesn't exist. The diagnostic differs — the compiler reports *"Unknown Variable"* on the long name itself.


/* In an Absence Entry Validation formula, no benefits contexts are supplied. */
/* The DBI exists in the dictionary but is invisible to this formula type.   */
ALIAS BEN_PEN_BNFT_AMT_NN AS BNFT_AMT


Unknown Variable: BEN_PEN_BNFT_AMT_NN


**Diagnostic heuristic:** "Misuse of ALIAS Statement" means the left-hand identifier is recognised by the compiler but isn't a DBI (input, context, function, local variable). "Unknown Variable" means the name simply doesn't resolve in your formula type — typo, wrong formula type, or a DBI requiring contexts you don't have.


### Should I alias this? — three quick checks


| The three-question decision |


| CHECK 1Is the identifier in the Database Items picker for this formula type? If no — stop. ALIAS will fail. |

| CHECK 2Will I reference it more than once, OR is its name longer than ~25 characters? If neither — don't bother. The alias adds noise without paying for itself. |

| CHECK 3Have I picked a short, project-consistent, non-reserved alias name? If no — go back to your project's naming convention. |


Three yeses → declare the alias in the ALIAS block at the top of the formula. Add a one-line trailing comment describing what the DBI represents in business terms. Use the alias name uniformly in body references, in `DEFAULT FOR`, and in any `WAS DEFAULTED` checks.


## The Reference vs Snapshot Distinction


ALIAS and `L_VAR = LONG_DBI_NAME` are not equivalent. They have different runtime behaviour, and one of them silently produces wrong answers under `CHANGE_CONTEXTS`.


### The local-variable pattern (anti-pattern for shortening)


DEFAULT FOR PER_ASG_REL_LENGTH_OF_SERVICE IS 0

/* Read the DBI once into a local variable for shorter access */
L_ASG_LOS = PER_ASG_REL_LENGTH_OF_SERVICE

IF L_ASG_LOS >= 5 THEN
   L_FLAG = 'Y'


Two things happen on the assignment line that are not always evident from the source: the DBI is fetched eagerly at that point regardless of whether the value is later read, and the local variable holds a snapshot under whichever contexts were active at assignment — any later `CHANGE_CONTEXTS` block does not update it.


### The ALIAS pattern


ALIAS PER_ASG_REL_LENGTH_OF_SERVICE AS ASG_LOS

DEFAULT FOR ASG_LOS IS 0

IF ASG_LOS >= 5 THEN
   L_FLAG = 'Y'


Functionally similar in this isolated case. But four behavioural differences matter:


| Property | Local-variable assignment | ALIAS |


| **DBI evaluation timing** | Eager — fetched at assignment, regardless of later use. | Lazy — fetched only when a code path actually evaluates the alias. |

| **Behaviour under CHANGE_CONTEXTS** | Frozen at original assignment context. Reads inside CHANGE_CONTEXTS return the original value. | Re-evaluates. Reads inside CHANGE_CONTEXTS fetch under the new context. |

| **Runtime memory** | Allocates a variable slot in the generated PL/SQL package. | No runtime allocation; resolved at compile time. |

| **WAS DEFAULTED compatibility** | Not supported. The check requires DBI metadata, lost in assignment. | Fully supported. Behaves identically to the underlying DBI. |


Figure 2 · Reference vs Snapshot — Same Logic, Different Runtime Behaviour



  LOCAL VARIABLE  ·  SNAPSHOT

  ALIAS  ·  REFERENCE


  Line 4 — initial context active
  L_SAL = CMP_ASSIGNMENT_SALARY_AMOUNT
  → fetched · stored as $75,000


  Line 4 — declaration only
  ALIAS CMP_..._SALARY_AMOUNT AS ASG_SAL
  → no fetch yet · label only


  inside CHANGE_CONTEXTS (start_dt)
  L_START_SAL = L_SAL
  → $75,000  (frozen — original ctx)


  inside CHANGE_CONTEXTS (start_dt)
  L_START_SAL = ASG_SAL
  → $75,000  (fresh fetch under start_dt)


  inside CHANGE_CONTEXTS (end_dt)
  L_END_SAL = L_SAL
  → $75,000  (still frozen — wrong)


  inside CHANGE_CONTEXTS (end_dt)
  L_END_SAL = ASG_SAL
  → $82,500  (fresh fetch under end_dt)


  L_DELTA = $0  →  WRONG


  L_DELTA = $7,500  →  CORRECT


**The same three references, two different runtime behaviours.** Local-variable assignment captures the value once at the assignment line; ALIAS re-evaluates the underlying DBI at every reference, under whatever context is active.


For shortening identifiers, ALIAS is the correct choice every time. Use local-variable assignment from a DBI only when a snapshot value is the explicit requirement — for instance, capturing a value at one context for comparison after a deliberate context change. In that case, name the variable accordingly: `L_SAL_AT_PERIOD_START` tells the next maintainer this is a snapshot.


## DEFAULT FOR and WAS DEFAULTED Against the Alias


Once an alias is declared, the rest of the formula — including `DEFAULT FOR` and `WAS DEFAULTED` — should reference the alias name. The compiler folds the alias and the underlying DBI into the same symbol, so writing the default against either resolves to the same metadata. Consistency is a maintenance discipline, not a compiler requirement:


ALIAS PER_ASG_JOB_NAME              AS ASG_JOB
ALIAS CMP_ASSIGNMENT_SALARY_AMOUNT AS ASG_SAL
ALIAS ASG_HR_ASG_ID                AS ASG_ID

/* Defaults written against the alias names */
DEFAULT FOR ASG_JOB IS ' '
DEFAULT FOR ASG_SAL IS 0
DEFAULT FOR ASG_ID  IS 0

INPUTS ARE EFFECTIVE_PERIOD_END (DATE)

/* WAS DEFAULTED check against the alias */
IF ASG_SAL WAS DEFAULTED THEN
   L_MSG = 'Salary DBI returned NULL — defaulted to 0'


The `WAS DEFAULTED` check inspects whether the underlying DBI fetch returned NULL and triggered the `DEFAULT FOR` substitution. Because the alias and the DBI share a single metadata handle, asking `ASG_SAL WAS DEFAULTED` gives the same answer as asking the long name.


**Don't mix names.** Technically the compiler accepts `DEFAULT FOR PER_ASG_JOB_NAME IS ' '` followed by `IF ASG_JOB WAS DEFAULTED`. But it's a maintenance nightmare. Pick the alias and use it consistently.


## ALIAS Inside CHANGE_CONTEXTS


The reference-vs-snapshot distinction has its biggest payoff inside `CHANGE_CONTEXTS` blocks. Because the alias compiles to a DBI fetch operation, evaluating it under a different context produces a fresh fetch under that context — exactly as if you'd written the long DBI name explicitly:


ALIAS CMP_ASSIGNMENT_SALARY_AMOUNT AS ASG_SAL

DEFAULT FOR ASG_SAL IS 0

INPUTS ARE PERIOD_START_DT (DATE), PERIOD_END_DT (DATE)

CHANGE_CONTEXTS (EFFECTIVE_DATE = PERIOD_START_DT)
(
   L_START_SAL = ASG_SAL          /* fetch under PERIOD_START_DT */
)

CHANGE_CONTEXTS (EFFECTIVE_DATE = PERIOD_END_DT)
(
   L_END_SAL = ASG_SAL            /* re-fetch under PERIOD_END_DT */
)

L_DELTA = L_END_SAL - L_START_SAL


Two reads of the same alias `ASG_SAL`, each fetching under a different `EFFECTIVE_DATE`, each producing a different value:


Figure 3 · ALIAS Re-Evaluates Under Each Context



  ASG_SAL
  one alias identifier · two code paths







  EFFECTIVE_DATE
  = PERIOD_START_DT


  EFFECTIVE_DATE
  = PERIOD_END_DT








  $ 75,000
  $ 82,500


**Same alias, two contexts, two distinct values.** Each evaluation is an independent DBI fetch under whichever context is active at that point in the code.


If the same logic were written using local-variable assignment at the top of the formula — `L_SAL = CMP_ASSIGNMENT_SALARY_AMOUNT` before any `CHANGE_CONTEXTS` block — the DBI would be fetched once under the formula's initial contexts. Reads of `L_SAL` inside both blocks would return the original frozen value. `L_DELTA` would silently evaluate to zero. No compiler diagnostic. No error message. Wrong answer.


**Performance note:** Every alias evaluation inside `CHANGE_CONTEXTS` is a potential database fetch. Use `CHANGE_CONTEXTS` only where context modification is required for correctness. Wrapping speculative or large code blocks in `CHANGE_CONTEXTS` introduces unnecessary re-fetches.


## The Three Compiler Errors You'll Actually See


The Oracle *Administering Fast Formulas* compilation-errors table lists several diagnostics that mention ALIAS. In practice, you'll bump into three of them repeatedly.


### Error 1 — Incorrect Statement Order


Incorrect Statement Order — ALIAS, DEFAULT, or INPUT statements come after other statements.


DEFAULT FOR ASG_HR_ASG_ID IS 0      /* DEFAULT precedes ALIAS — invalid */

ALIAS PER_ASG_JOB_NAME AS ASG_JOB     /* ← raises the diagnostic */

INPUTS ARE EFFECTIVE_DATE_FROM (DATE)


**Fix:** Reorder so that all ALIAS declarations precede all DEFAULT declarations. The required order is ALIAS → DEFAULT → INPUTS → body, every time.


### Error 2 — Misuse of ALIAS Statement


Misuse of ALIAS Statement — you can use an ALIAS statement only for a database item.


/* Aliasing a context — invalid */
ALIAS HR_ASSIGNMENT_ID AS ASG_ID         /* ← context, not a DBI */

/* Aliasing an input — invalid */
ALIAS EFFECTIVE_DATE_FROM AS EFF_DT      /* ← input parameter */

/* Aliasing an unknown identifier — invalid */
ALIAS SOME_RANDOM_NAME AS SHORT_NAME      /* ← unrecognised */


**Fix:** Confirm the left-hand identifier is a DBI listed in the Database Items picker. Contexts are read with `GET_CONTEXT`; inputs are declared with `INPUTS ARE`; unknown identifiers are typos.


### Error 3 — Unknown Variable on the DBI Identifier


Unknown Variable: CMP_ASSIGNMENT_SALARY_AMOUNT


/* The DBI exists in the dictionary but is not visible to this formula type */
/* because the formula type doesn't supply HR_ASSIGNMENT_ID as a context.   */
ALIAS CMP_ASSIGNMENT_SALARY_AMOUNT AS ASG_SAL


**Fix:** Open the Database Items picker for the specific formula type currently being authored — Absence Accrual, OTL Time Entry Rule, Compensation Default and Override, Payroll, whichever applies — and confirm the DBI is listed. If it isn't, your formula type doesn't supply the contexts the DBI's route needs, and aliasing won't fix it.


## Production Conventions for ALIAS


| Seven principles that pay off across every formula |


| RULE 1**Group all ALIAS declarations at the top of the formula**, immediately after the header comment. Satisfies the ordering rule and presents the data dependencies in one block. |

| RULE 2**Apply ALIAS only when the DBI is referenced more than once or longer than ~25 characters.** A single short reference doesn't warrant the declaration overhead. |

| RULE 3**Use a project-wide naming convention.** Strip product prefixes and abbreviate consistently: `PER_ASG_REL_LENGTH_OF_SERVICE` → `ASG_LOS`, `ASG_HR_ASG_ID` → `ASG_ID`, `CMP_ASSIGNMENT_SALARY_AMOUNT` → `ASG_SAL`. |

| RULE 4**Annotate each alias with a one-line trailing comment** describing what the DBI represents in business terms. |

| RULE 5**Default to ALIAS over local-variable assignment** for shortening. Use local assignment only when snapshot semantics are explicitly required, with a name that signals the snapshot intent. |

| RULE 6**Restrict ALIAS targets to database items.** Inputs are short by design. Contexts are accessed through GET_CONTEXT. Local variables are named directly. |

| RULE 7**Apply consistent identifier casing.** The compiler is case-insensitive, but mixing `ASG_LOS` and `Ot_Qls` across one formula degrades readability. |


## Before vs After — The Readability Payoff


Same logic, written twice. Once without aliases, once with. Watch how the body changes character.


### Without ALIAS


/*========================================================================
   FORMULA NAME : XX_OT_ELIG_WITHOUT_ALIAS
   FORMULA TYPE : Element Iterative Calculator
   PURPOSE      : OT eligibility flag & multiplier from qualifying LOS
                  and assignment salary.
========================================================================*/

DEFAULT FOR PER_ASG_REL_LENGTH_OF_SERVICE IS 0
DEFAULT FOR CMP_ASSIGNMENT_SALARY_AMOUNT          IS 0
DEFAULT FOR PER_ASG_JOB_NAME                      IS ' '

INPUTS ARE EFFECTIVE_PERIOD_END (DATE)

L_FLAG       = 'N'
L_MULTIPLIER = 1

CHANGE_CONTEXTS (EFFECTIVE_DATE = EFFECTIVE_PERIOD_END)
(
   IF PER_ASG_REL_LENGTH_OF_SERVICE >= 5
      AND CMP_ASSIGNMENT_SALARY_AMOUNT > 0
      AND PER_ASG_JOB_NAME <> ' '
   THEN
      ( L_FLAG       = 'Y'
        L_MULTIPLIER = 1.5 )

   IF PER_ASG_REL_LENGTH_OF_SERVICE >= 10 THEN
      L_MULTIPLIER = 2.0
)

RETURN L_FLAG, L_MULTIPLIER


### With ALIAS


/*========================================================================
   FORMULA NAME : XX_OT_ELIG_WITH_ALIAS
   FORMULA TYPE : Element Iterative Calculator
   NOTES        : ALIAS block sits FIRST. Each alias is a reference to
                  its underlying DBI; evaluation is lazy and re-fetches
                  under any CHANGE_CONTEXTS block.
========================================================================*/

ALIAS PER_ASG_REL_LENGTH_OF_SERVICE AS ASG_LOS    /* qualifying LOS, years */
ALIAS CMP_ASSIGNMENT_SALARY_AMOUNT  AS ASG_SAL    /* current annual salary */
ALIAS PER_ASG_JOB_NAME              AS ASG_JOB    /* assignment job name   */

DEFAULT FOR ASG_LOS IS 0
DEFAULT FOR ASG_SAL IS 0
DEFAULT FOR ASG_JOB IS ' '

INPUTS ARE EFFECTIVE_PERIOD_END (DATE)

L_FLAG       = 'N'
L_MULTIPLIER = 1

CHANGE_CONTEXTS (EFFECTIVE_DATE = EFFECTIVE_PERIOD_END)
(
   IF ASG_LOS >= 5 AND ASG_SAL > 0 AND ASG_JOB <> ' ' THEN
      ( L_FLAG       = 'Y'
        L_MULTIPLIER = 1.5 )

   IF ASG_LOS >= 10 THEN
      L_MULTIPLIER = 2.0
)

IF ASG_SAL WAS DEFAULTED THEN
   L_MSG = 'Salary DBI returned NULL — defaulted to 0'

RETURN L_FLAG, L_MULTIPLIER


Compare the eligibility test in the aliased version to the unaliased one. Same logical condition, but in the aliased version you can read the rule out loud: "if qualifying service is at least 5 and salary is positive and job is not blank" — without your eyes filtering through DBI prefixes. That readability is the entire point.


The aliased version also adds the `WAS DEFAULTED` diagnostic on the salary check, which is unavailable through local-variable assignment.


## Key Takeaways


**ALIAS is a compile-time reference, not a runtime variable.** The alias and the underlying DBI share a single metadata handle. No separate runtime allocation occurs.


**Statement ordering is enforced.** The required sequence is ALIAS → DEFAULT → INPUTS → body → RETURN. Violations produce *"Incorrect Statement Order."*


**ALIAS interacts correctly with WAS DEFAULTED and CHANGE_CONTEXTS.** Local-variable assignment from a DBI does not — that produces a snapshot, not a reference, and silently breaks salary deltas, before/after comparisons, and any logic that re-evaluates a value under a different context.


**ALIAS targets are restricted to database items in current Fusion releases.** Inputs, contexts, functions, and global values are not valid targets.


  | AM
  | **Abhishek Mohanty**Oracle ACE Apprentice | AIOUG Member | Oracle HCM Cloud Consultant & Technical Lead — Fast Formulas, Absence Management, Time & Labor, Core HR, Redwood, HDL, OTBI.
|


[Fast Formula](#)
[ALIAS](#)
[Oracle HCM Cloud](#)
[DBI](#)
[CHANGE_CONTEXTS](#)
[WAS_DEFAULTED](#)
[Statement Order](#)
[Compilation Errors](#)
[Oracle Cloud](#)