---
title: "HDL Transformation Fast Formula — Part 1: OPERATION Routing, METADATA Arrays & WSA Caching"
description: "Step-by-step walkthrough of an Oracle HCM Cloud HDL Transformation Fast Formula covering OPERATION routing, METADATA arrays, MAP steps, WSA caching, LINEREPEATNO, and ElementEntry output."
pubDate: 2026-03-25
tags: []
---

Vendor Deduction Interface | ElementEntry + ElementEntryValue

This is **Part 1** of a 3-part series on HDL Transformation Formulas. This post covers the concepts end-to-end — what each section of the formula does and why. No code to copy-paste here. Just the understanding you need before writing a single line.

HDL Transformation Formula Series

Pure Concepts ← You are here

What each section of the formula does. INPUTS, OPERATION, METADATA, MAP (5 steps), WSA, LINEREPEATNO, RETURN. Zero code to memorize — just understanding.

Code Walkthrough Coming soon

The actual formula code, explained line-by-line. Value set definitions, WSA implementation, date conversions, ISNULL patterns, ESS_LOG_WRITE debugging. Moderate complexity — you'll be able to read any HDL formula after this.

Build Your Own Coming soon

Full implementation guide. Setting up the formula in Oracle, creating the value sets, configuring the HDL integration, testing with real data, debugging production issues. Copy-paste ready.

Abhishek Mohanty

Before we go section by section, here's what this formula does end to end:

Vendor CSV File**SSN, Date, Code, Amounts

HDL Transformation
This Formula

ElementEntry .dat
Header + Value rows

A third-party benefits administration vendor (BenAdmin) sends a CSV with deduction and employer contribution amounts. This formula transforms each row into Oracle HDL format — resolving SSNs to Assignment Numbers, mapping vendor codes to Oracle Element Names, managing MultipleEntryCount, and generating both ElementEntry (header) and ElementEntryValue (detail) rows.

---

The vendor manages employee benefit enrollments — medical, dental, vision, life insurance, FSA, HSA, loans. Every pay period, they send a flat CSV file with deduction details to load into Oracle as Element Entries.

The Raw Input File Layout

Each row in the vendor file maps to one set of delimited columns. The HDL engine reads these into POSITION variables:

| Column | Position | Description | Example |
| --- | --- | --- | --- |
| SSN | POSITION1 | Employee Social Security Number | 123-45-6789 |
| EFFECTIVE_DATE | POSITION2 | Date the deduction applies (YYYY-MM-DD) | 2024-01-15 |
| BENEFIT_PLAN_CODE | POSITION3 | Vendor’s internal code for the benefit plan | DENTAL01 |
| DEDUCTION_TYPE | POSITION4 | Controls LINEREPEATNO branches and how many input values are loaded | LOAN, PRE, POST, CU |
| AMOUNT | POSITION5 | Deduction amount (InputValueName = ‘Amount’) | 150.00 |
| PERIOD_TYPE | POSITION6 | Period type for the deduction | (varies) |
| PERCENTAGE | POSITION7 | Percentage for PRE/POST type deductions | (blank or value) |
| LOAN_NUMBER | POSITION8 | Loan number (LOAN type only) | (blank or value) |
| POSITION9–10 | POSITION9–10 | Reserved / additional fields | (varies) |
| STATUS | POSITION11 | C = Cancel/End-date, blank = Active/New | (blank) |

Key point:** POSITION4 (Deduction Type) is the most important field after SSN and Date. It controls the formula's branching logic — which LINEREPEATNO passes execute, which input values get loaded (Amount, Period Type, Percentage, Loan Number, Total Owed, Deduction Amount), and even whether the formula generates output on certain passes. A LOAN type deduction goes through 7 passes. A regular deduction goes through fewer.

How One Vendor Row Becomes Multiple Input Values

A single vendor row carries multiple amounts for the same deduction. The formula uses LINEREPEATNO to load each input value in a separate pass. For a LOAN type deduction, one source row generates up to 7 output rows:

```text
/* One vendor row: */
123-45-6789,2024-01-15,DENTAL01,LOAN,150.00,Monthly,5.5,LN-001,,,,

/* Formula generates (up to 7 passes): */
Pass 1 (LINEREPEATNO=1): ElementEntry header
Pass 2 (LINEREPEATNO=2): ElementEntryValue → Amount = 150.00
Pass 3 (LINEREPEATNO=3): ElementEntryValue → Period Type = Monthly
Pass 4 (LINEREPEATNO=4): ElementEntryValue → Loan Number = LN-001
Pass 5 (LINEREPEATNO=5): ElementEntryValue → Total Owed = ...
Pass 6 (LINEREPEATNO=6): ElementEntryValue → Percentage = 5.5
Pass 7 (LINEREPEATNO=7): ElementEntryValue → Deduction Amount = ...
```

Not every deduction type needs all 7 passes. The formula checks POSITION4 on each pass — if the type doesn't apply (e.g. Percentage only runs for PRE/POST types), it returns `LINEREPEAT = 'Y'` with no output, effectively skipping that pass.

Understanding MultipleEntryCount

Oracle HCM draws a fundamental distinction between **recurring** and **non-recurring** elements when it comes to MultipleEntryCount:

Monthly salary, standing allowance

MultipleEntryCount is **not required** as a key when using SourceSystemId.

*"You don't need to supply the MultipleEntryCount attribute as source keys to uniquely identify the records."* — Oracle Docs

Benefits deductions (our vendor elements)

MultipleEntryCount **must be incremented** for each entry of the same assignment + element within the same payroll period.

*"You must increment the value of MultipleEntryCount for each entry of the same assignment and element."* — Oracle Docs

The vendor interface loads **non-recurring elements that allow multiple entries**. This means the formula must query the cloud for the current highest MultipleEntryCount before assigning the next one — and track assigned values across rows within the same batch using WSA.

**Key Takeaway:** Three benefit plan rows (Dental, Medical, Vision) for the same employee map to three **different elements**, so they each get independent entries with their own MultipleEntryCount. MultipleEntryCount is needed when the **same non-recurring element** requires **multiple entries** for the **same assignment within the same payroll period**.

---

The vendor file gives us an **SSN** and an **Vendor Deduction Code**. Oracle HCM needs an **Assignment Number** and an **Oracle Element Name**. These are completely different identifiers in completely different systems. Value Sets act as the bridge — SQL-backed lookup functions that run inside the Fast Formula engine.

VENDOR ENVIRONMENT

SSN: 123-45-6789

Code: DENTAL01

VALUE SETS

→

ORACLE WORLD

Asg#: E12345

Element: Dental EE Deduction

The formula uses 11 value sets. Here's what each one does:

| # | Value Set | What It Does | Returns |
| --- | --- | --- | --- |
| 1 | XXVA_DEDUCTION_CODES | Maps vendor plan code (DENTAL01) to Oracle Element Name | Element Name |
| 2 | XXVA_DEDUCTION_CODES_INPUT | Gets Input Value Name for the element (e.g. Amount) | Input Value Name |
| 3 | XXVA_GET_LATEST_ASSIGNMENT_NUMBER | Resolves SSN + date → Assignment Number | Assignment# (E12345) |
| 4 | XXVA_GET_PERSON_NUMBER | Resolves SSN → Person Number | Person# (100045) |
| 5 | MAX_MULTI_ENTRY_COUNT | Gets highest existing MultipleEntryCount for Person+Element+Date | Max count (or NULL) |
| 6–7 | GET_ELEMENT_ENTRY_SOURCE_SYSTEM_ID / _OWNER | Retrieves existing SourceSystemId/Owner for MERGE key reuse | Existing SSID/SSO |
| 8–9 | GET_ELEMENT_ENTRY_VALUE_SOURCE_SYSTEM_ID / _OWNER | Same but at Element Entry Value level | ElementEntryValue-level SSID/SSO |
| 10 | GET_ELEMENT_ENTRY_START_DATE | For Cancel rows — gets original start date | Original start date |
| 11 | GET_ELEMENT_ENTRY_INPUT_START_DATE | Same but at ElementEntryValue level (date-tracked scenarios) | ElementEntryValue original start date |

Translate vendor codes → Oracle element names. Called once per row regardless. No caching benefit.

Resolve SSN/Person data. Same SSN appears across multiple rows — **WSA caching saves significant performance here.**

---

```text
INPUTS ARE OPERATION (TEXT),
LINEREPEATNO (NUMBER),
LINENO (NUMBER),
POSITION1 (TEXT), POSITION2 (TEXT), POSITION3 (TEXT),
POSITION4 (TEXT), POSITION5 (TEXT), POSITION6 (TEXT),
POSITION7 (TEXT), POSITION8 (TEXT),
POSITION9 (TEXT), POSITION10 (TEXT), POSITION11 (TEXT)

DEFAULT FOR LINENO IS 1
DEFAULT FOR LINEREPEATNO IS 1
DEFAULT FOR POSITION1 IS 'NO DATA'
DEFAULT FOR POSITION2 IS 'NO DATA'
/* ... same for POSITION3 through POSITION11 ... */
```

| Variable | What It Does |
| --- | --- |
| OPERATION | The HDL engine calls the formula multiple times with different values: FILETYPE, DELIMITER, READ, NUMBEROFBUSINESSOBJECTS, METADATALINEINFORMATION, then MAP per row. The formula is a router. |
| LINEREPEATNO | The repeat counter. When formula sets `LINEREPEAT = 'Y'`, HDL re-invokes for the same row with incremented LINEREPEATNO. One input row can generate up to 7 HDL output rows: 1 ElementEntry header (pass 1) + up to 6 ElementEntryValue rows (passes 2–7), one per input value (Amount, Period Type, Loan Number, Total Owed, Percentage, Deduction Amount). The deduction type (POSITION4) controls how many passes run. |
| LINENO | Line number from the source file (1-based). Useful for error tracing. |
| POSITION1–11 | Map directly to CSV columns in order. HDL engine splits each line by delimiter and populates these. |

**Why DEFAULT FOR is required:** When HDL calls the formula for non-MAP operations (like FILETYPE), the POSITION variables aren't populated — no source row is being processed. Without defaults, the formula throws a null reference error at runtime.

---

| Input | HDL engine asks: "What file type? What delimiter? How many objects?" |
| --- | --- |
| Formula returns | DELIMITED, comma, NONE, 2 |
| HDL output | Nothing written to .dat yet — engine is just being configured |

```text
IF OPERATION = 'FILETYPE' THEN
    OUTPUTVALUE = 'DELIMITED'
ELSE IF OPERATION = 'DELIMITER' THEN
    OUTPUTVALUE = ','
ELSE IF OPERATION = 'READ' THEN
    OUTPUTVALUE = 'NONE'
ELSE IF OPERATION = 'NUMBEROFBUSINESSOBJECTS' THEN
(
    OUTPUTVALUE = '2'
    RETURN OUTPUTVALUE
)
```

FILETYPE**DELIMITED

DELIMITER
,

READ
NONE

OBJECTS
2

METADATA

MAP
(per row)

| Operation | Engine Asks | Our Answer | Why |
| --- | --- | --- | --- |
| FILETYPE | "What kind of file?" | DELIMITED | Only valid option for HDL transformation |
| DELIMITER | "What separates values?" | , | the vendor sends CSV. Default is pipe (\|), so we override. |
| READ | "Skip header rows?" | NONE | vendor file has no header row — process every line. |
| NUMBEROF... | "How many HDL objects?" | 2 | ElementEntry (header) + ElementEntryValue (detail with amount) |

---

| Input | HDL engine asks: "What columns does each object have?" |
| --- | --- |
| Formula returns | METADATA1[ ] array, METADATA2[ ] array |
| HDL writes to .dat | METADATA\|ElementEntry\|LegislativeDataGroupName\|EffectiveStartDate\|...METADATA\|ElementEntryValue\|LegislativeDataGroupName\|EffectiveStartDate\|... |

After the setup handshake, the HDL engine calls the formula with `OPERATION = 'METADATALINEINFORMATION'`. This is where the formula defines the column headers** for the .dat output file. These become the METADATA rows you see at the top of each block in the .dat file.

The .dat File Has Two METADATA Header Rows

Since we told the engine `NUMBEROFBUSINESSOBJECTS = 2` (ElementEntry + ElementEntryValue), the formula must define two METADATA arrays — one per object. These become the two header rows in the .dat file:

```text
/* This header row in the .dat file: */
METADATA|ElementEntry|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|CreatorType|EffectiveEndDate|EntryType|MultipleEntryCount

/* Is generated by this code: */
```

The Code — METADATA1 (ElementEntry Header)

The formula uses an **array variable** called `METADATA1`. Each array position maps to a column in the .dat header. Positions [1] and [2] are reserved by the HDL engine for FileName and FileDiscriminator — the formula starts filling from position [3].

```text
ELSE IF OPERATION = 'METADATALINEINFORMATION' THEN
(
    /* ================================================= */
    /* METADATA1 — ElementEntry column definitions        */
    /* [1] = FileName (auto-filled by HDL engine)         */
    /* [2] = FileDiscriminator (auto-filled by HDL engine)*/
    /* [3] onwards = we define                            */
    /* ================================================= */

    METADATA1[3]  = 'LegislativeDataGroupName'
    METADATA1[4]  = 'EffectiveStartDate'
    METADATA1[5]  = 'ElementName'
    METADATA1[6]  = 'AssignmentNumber'
    METADATA1[7]  = 'CreatorType'
    METADATA1[8]  = 'EffectiveEndDate'
    METADATA1[9]  = 'EntryType'
    METADATA1[10] = 'MultipleEntryCount'
    METADATA1[11] = 'SourceSystemOwner'
    METADATA1[12] = 'SourceSystemId'
    METADATA1[13] = 'ReplaceLastEffectiveEndDate'
```

The HDL engine reads this array and writes the following row to the .dat file:

```text
METADATA|ElementEntry|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|CreatorType|EffectiveEndDate|EntryType|MultipleEntryCount|SourceSystemOwner|SourceSystemId|ReplaceLastEffectiveEndDate
```

The Code — METADATA2 (ElementEntryValue Header)

Same pattern. `METADATA2` array defines the columns for the ElementEntryValue block:

```text
    /* ================================================= */
    /* METADATA2 — ElementEntryValue column definitions   */
    /* ================================================= */

    METADATA2[3]  = 'LegislativeDataGroupName'
    METADATA2[4]  = 'EffectiveStartDate'
    METADATA2[5]  = 'ElementName'
    METADATA2[6]  = 'AssignmentNumber'
    METADATA2[7]  = 'InputValueName'              /* ← changes per pass */
    METADATA2[8]  = 'EffectiveEndDate'
    METADATA2[9]  = 'EntryType'
    METADATA2[10] = 'MultipleEntryCount'
    METADATA2[11] = 'ScreenEntryValue'            /* ← the actual value */
    METADATA2[12] = '"ElementEntryId(SourceSystemId)"'  /* parent link */
    METADATA2[13] = 'SourceSystemOwner'
    METADATA2[14] = 'SourceSystemId'
    METADATA2[15] = 'ReplaceLastEffectiveEndDate'

    RETURN METADATA1, METADATA2
)
```

This generates the second header row in the .dat file:

```text
METADATA|ElementEntryValue|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|InputValueName|EffectiveEndDate|EntryType|MultipleEntryCount|ScreenEntryValue|ElementEntryId(SSID)|SourceSystemOwner|SourceSystemId|ReplaceLastEffectiveEndDate
```

How METADATA Links to RETURN in Sections 7 and 8

The column names in the METADATA arrays directly map to the **named output variables** in the formula's RETURN statement. Here's the connection:

```text
/* METADATA defines the column header: */
METADATA1[5] = 'ElementName'

/* In the MAP block, the formula assigns the named variable: */
ElementName  = l_ElementName              /* = 'Dental EE Deduction' */

/* And includes it in the RETURN: */
RETURN ..., ElementName, ...

/* Result in .dat file:                                                */
/* METADATA |ElementEntry|...|ElementName                    |...      */
/* MERGE    |ElementEntry|...|Dental EE Deduction   |...      */
/*                             ↑ matched by variable name             */
```

**The mapping rule:**

`METADATA1[N]` defines column N header name for object 1 (ElementEntry)**
In the MAP block, you assign a variable with that exact same name** and include it in the RETURN statement**

The HDL engine matches the RETURN variable name to the METADATA column name and writes the value into the correct position in the .dat file. The `FileDiscriminator` value (`'ElementEntry'` vs `'ElementEntryValue'`) tells the engine which METADATA block to use.

---

The reference vendor row used in all examples below:

Vendor Input Row

| POSITION1 | SSN | 123-45-6789 |
| --- | --- | --- |
| POSITION2 | Effective Date | 2024-01-15 |
| POSITION3 | Benefit Plan | DENTAL01 |
| POSITION4 | Deduction Type | PRE |
| POSITION5 | Amount | 150.00 |
| POSITION6 | Period Type | Monthly |
| POSITION7 | Percentage | 5.5 |
| POSITION8 | Loan Number | LN-001 |
| POSITION11 | Status | (blank = Active) |

This is the heart of the formula. When the HDL engine reaches a source row, it calls `OPERATION = 'MAP'`. The formula receives the raw CSV data in POSITION1–11 and must return Oracle HDL attributes. Five steps run in sequence.

Here's what the formula needs to figure out for each row:

| Question | Vendor Gives Us | Oracle Needs | Step |
| --- | --- | --- | --- |
| What type of deduction? | POSITION4 (Deduction Type) | PRE / POST / LOAN / CU | Step 1 |
| Which Oracle Element? | DENTAL01 | Dental EE Deduction | Step 2 |
| Which employee? | 123-45-6789 (SSN) | E12345 (Assignment#) | Step 3 |
| How many entries already exist? | (doesn't know) | MultipleEntryCount = 2 | Step 4 |
| New or existing entry? | (doesn't know) | SourceSystemId for MERGE | Step 5 |

STEP 1
Element Type

STEP 2
Element Lookup

STEP 3
Person / Assignment

STEP 4
MultipleEntryCount

STEP 5
SourceSystemId

Step 1: Read Input Values from POSITION Fields

| POSITION4 = PRE | → l_DeductionType = 'PRE' |
| --- | --- |
| POSITION5 = 150.00 | → l_Amount = '150.00' |
| POSITION6 = Monthly | → l_PeriodType = 'Monthly' |
| POSITION7 = 5.5 | → l_Percentage = '5.5' |
| POSITION8 = LN-001 | → l_LoanNumber = 'LN-001' |

The formula reads the deduction type from POSITION4 and the amount from POSITION5. It also captures other input values (Period Type, Percentage, Loan Number) from their respective positions for later LINEREPEATNO passes:

```text
/* Read the key fields from the vendor row */
l_DeductionType    = TRIM(POSITION4)     /* 'PRE', 'POST', 'LOAN', 'CU' */
l_Amount           = TRIM(POSITION5)     /* '150.00' */
l_PeriodType       = TRIM(POSITION6)     /* 'Monthly' */
l_Percentage       = TRIM(POSITION7)     /* '5.5' (PRE/POST only) */
l_LoanNumber       = TRIM(POSITION8)     /* 'LN-001' (LOAN only) */
```

After this step: `l_DeductionType = 'PRE'` and `l_Amount = '150.00'`

Step 2: Resolve Element Name from Benefit Plan Code

| POSITION3 = DENTAL01 | → Value Set lookup |
| --- | --- |
|  | → l_ElementName = 'Dental EE Deduction' |
|  | → l_InputValueName = 'Amount' |

The vendor uses its own benefit plan codes (DENTAL01, MEDICAL01, VISION01). Oracle doesn't know these codes. The formula passes the vendor code to two value sets that translate it into Oracle terms:

```text
/* Step 2: Translate vendor plan code → Oracle Element Name */

L_VendorPayCode = TRIM(POSITION3)
/* e.g. 'DENTAL01' */

/* Value set 1: vendor code → Oracle Element Name */
l_ElementName = GET_VALUE_SET('XXVA_DEDUCTION_CODES',
    '|=P_PAY_CODE=''' || L_VendorPayCode || '''')
/* 'DENTAL01' → 'Dental EE Deduction' */

/* Value set 2: vendor code → Input Value Name */
l_InputValueName = INITCAP(GET_VALUE_SET('XXVA_DEDUCTION_CODES_INPUT',
    '|=P_PAY_CODE=''' || L_VendorPayCode || ''''))
/* 'DENTAL01' → 'Amount' */
```

These are code-based** lookups — the value set definition maps each vendor code to its Oracle element. No person data is involved, so no WSA caching is needed here.

Value Set Translation

| Vendor Code (POSITION3) | Oracle Element Name | Input Value Name |
| --- | --- | --- |
| DENTAL01 | Dental EE Deduction | Amount |
| MEDICAL01 | Medical EE Deduction | Amount |
| VISION01 | Vision EE Deduction | Amount |

This mapping is defined in the value set configuration — not in the formula code. Adding a new benefit plan just means adding a row to the value set.

After Step 2: `l_ElementName = 'Dental EE Deduction'` and `l_InputValueName = 'Amount'`

Step 3: Resolve Person & Assignment

| POSITION1 = 123-45-6789 | → GET_VALUE_SET → L_PersonNumber = '100045' |
| --- | --- |
| POSITION2 = 2024-01-15 | → GET_VALUE_SET → l_AssignmentNumber = 'E12345' |

Oracle HDL doesn't understand SSN. It needs two things: **Person Number** and **Assignment Number**. Step 3 translates one into the other.

VENDOR FILE GIVES US

123-45-6789

SSN (POSITION1)

→

Value Set**calls DB

ORACLE HDL NEEDS

Person# 100045

Assignment# E12345

Two value sets do this translation:

| XXVA_GET_PERSON_NUMBER | Takes SSN + Date → returns Person Number (100045) |
| --- | --- |
| XXVA_GET_LATEST_ASSIGNMENT_NUMBER | Takes SSN + Date → returns Assignment Number (E12345) |

That's the simple version. But there's a performance problem.

The Problem: Same SSN, Three Rows, Three Identical DB Calls

One employee can have multiple rows in the vendor file — one per benefit plan. If an employee has 3 benefit plans (Dental, Medical, Vision), the file has 3 rows with the same SSN**. Without optimization, the formula calls the value set 3 times for the exact same SSN and gets the exact same answer 3 times.

Without caching — 3 rows, same SSN

**Row 1 (DENTAL01):** SSN 123-45-6789 → call DB → Person# 100045 [OK]**
Row 2 (MEDICAL01):** SSN 123-45-6789 → call DB again → Person# 100045 ← same SSN, wasted call**
Row 3 (VISION01):** SSN 123-45-6789 → call DB again → Person# 100045 ← same SSN, wasted call

The Fix: Cache with WSA

The formula uses WSA to remember the answer (explained in the WSA Deep Dive after Step 4). The logic is simple:

Did I already look up this SSN?

WSA_EXISTS('PER_123-45-6789_2024-01-15')

YES → Read from cache

WSA_GET('PER_123-45-6789_2024-01-15', ' ')**→ 100045. Done. No DB call.

NO → Call DB, then save to cache

GET_VALUE_SET(...) → 100045
WSA_SET('PER_123-45-6789_2024-01-15', 100045)

With WSA caching — same 3 rows, same SSN

Row 1 (DENTAL01):** WSA_EXISTS? **NO** → call DB → 100045 → WSA_SET (save it) [OK]**
Row 2 (MEDICAL01):** WSA_EXISTS? **YES** → WSA_GET → 100045. Zero DB calls. [OK]**
Row 3 (VISION01):** WSA_EXISTS? **YES** → WSA_GET → 100045. Zero DB calls. [OK]

Here's what the actual code looks like:

```text
/* Build a unique WSA key from SSN + Date */
/* e.g. 'PER_123-45-6789_2024-01-15' */

IF WSA_EXISTS('PER_' || POSITION1 || '_' || POSITION2) THEN
(
    /* Cache hit — read stored values */
    L_PersonNumber     = WSA_GET('PER_' || POSITION1 || '_' || POSITION2, ' ')
    l_AssignmentNumber = WSA_GET('ASG_' || POSITION1 || '_' || POSITION2, ' ')
)
ELSE
(
    /* Cache miss — call value sets (hits DB) */
    l_AssignmentNumber = GET_VALUE_SET('XXVA_GET_LATEST_ASSIGNMENT_NUMBER', ...)
    L_PersonNumber     = GET_VALUE_SET('XXVA_GET_PERSON_NUMBER', ...)

    /* Save to WSA — next row with same SSN skips DB */
    WSA_SET('PER_' || POSITION1 || '_' || POSITION2, L_PersonNumber)
    WSA_SET('ASG_' || POSITION1 || '_' || POSITION2, l_AssignmentNumber)
)
```

After Step 3: `L_PersonNumber = '100045'` and `l_AssignmentNumber = 'E12345'`

Step 4: MultipleEntryCount

| Person 100045 + Element Dental EE Deduction + Date 2024-01-15 | → l_MultipleEntryCount = 1 (or 2, 3... if entries already exist) |
| --- | --- |

What Is It?

When the same person has multiple entries of the **same element** in the **same payroll period**, Oracle needs a sequence number to tell them apart. That number is MultipleEntryCount.

When does this happen in the vendor interface? Each pay period, the vendor sends a new deduction file. If person 100045 already has a Dental EE Deduction entry from a previous load, and this batch sends another one (maybe a mid-period adjustment), the new entry needs a higher count.

If you know SQL, it's this:

```text
ROW_NUMBER() OVER (PARTITION BY person, element, payroll_period)  =  MultipleEntryCount
```

Here's what it looks like in `PAY_ELEMENT_ENTRIES_F` after multiple loads:

| Person# | Element | EffectiveStartDate | Amount | MultipleEntryCount | Source |
| --- | --- | --- | --- | --- | --- |
| 100045 | Dental EE Deduction | 2024-01-15 | $150.00 | 1 | January batch |
| 100045 | Dental EE Deduction | 2024-01-20 | $25.00 | 2 | Mid-period adjustment |
| 100045 | Medical EE Deduction | 2024-01-15 | $200.00 | 1 | ← different element, count resets to 1 |

The partition key is **Person + Element + Payroll Period**. Same person + same element = same group, count increments. Different element = new group, count resets to 1. If two entries in the same group get the **same** count, Oracle overwrites the first one — data is lost.

The Problem: Fast Formula Has No Memory

In PL/SQL, you'd do this in a loop. The counter variable lives across iterations:

```text
-- PL/SQL: variable persists across loop iterations
l_counter := 0;
FOR rec IN cursor LOOP
    l_counter := l_counter + 1;
    -- Row 1: l_counter = 1
    -- Row 2: l_counter = 2  ← remembers what happened in Row 1
END LOOP;
```

Fast Formula is **not** a loop. The HDL engine calls the formula once per row as a **separate, independent invocation**. All local variables are destroyed after each call. It's like calling a standalone function 10,000 times — each call starts from zero with no memory of the previous call.

So the formula has to ask the database: *"What's the highest count that already exists?"* The value set runs something like this behind the scenes against `PAY_ELEMENT_ENTRIES_F`:

```text
SELECT MAX(pee.MULTIPLE_ENTRY_COUNT)
FROM   PAY_ELEMENT_ENTRIES_F  pee
      ,PAY_ELEMENT_TYPES_F    pet
      ,PER_ALL_ASSIGNMENTS_M  paam
WHERE  pee.ELEMENT_TYPE_ID  = pet.ELEMENT_TYPE_ID
AND    pee.PERSON_ID         = paam.PERSON_ID
AND    pet.ELEMENT_NAME      = 'Dental EE Deduction'
AND    paam.PERSON_NUMBER    = '100045'
AND    '2024-10-15' BETWEEN pee.EFFECTIVE_START_DATE AND pee.EFFECTIVE_END_DATE
```

This works fine when each batch has only one row per person+element. But what if the batch has two?

The Bug: Two Rows Read the Same Stale MAX

Here's what's already in `PAY_ELEMENT_ENTRIES_F` from last month's load:

| ELEMENT_ENTRY_ID | PERSON_ID | ELEMENT_TYPE_ID | EFFECTIVE_START_DATE | MULTIPLE_ENTRY_COUNT | ENTRY_TYPE |
| --- | --- | --- | --- | --- | --- |
| 300000012345 | 100045 | 50001 (Dental EE Deduction) | 01-Oct-2024 | 1 | E |

Now our vendor batch has two new Dental EE Deduction rows for the same person. The formula runs `SELECT MAX(MULTIPLE_ENTRY_COUNT)` for each — but the problem is Row 5's INSERT hasn't reached the table yet when Row 8 queries it:

Row 5 processes — formula queries the table:

```text
SELECT MAX(MULTIPLE_ENTRY_COUNT) FROM PAY_ELEMENT_ENTRIES_F
WHERE PERSON_ID = 100045 AND ELEMENT_TYPE_ID = 50001  → Returns 1
```

Formula assigns: 1 + 1 = 2   ← this row is still in the HDL batch, NOT yet inserted into PAY_ELEMENT_ENTRIES_F

Row 8 processes — formula queries the SAME table:

```text
SELECT MAX(MULTIPLE_ENTRY_COUNT) FROM PAY_ELEMENT_ENTRIES_F
WHERE PERSON_ID = 100045 AND ELEMENT_TYPE_ID = 50001  → STILL returns 1!
```

Formula assigns: 1 + 1 = 2   ← SAME count as Row 5!

What the generated .dat file looks like — both rows got the same count:

ElementEntry.dat — FAIL output

Existing entry (already in Oracle):

| ElementName | Dental EE Deduction |
| --- | --- |
| MultipleEntryCount | 1 |

Row 5 output ($175.00):

| ElementName | Dental EE Deduction |
| --- | --- |
| MultipleEntryCount | 2 |

Row 8 output ($200.00) — SAME count!

__DARK_0__

**BUG:** Two rows in the .dat file with MultipleEntryCount = 2. When Oracle loads this file, Row 8 overwrites Row 5. $175.00 entry is lost.

The Fix: WSA Tracks What the Table Can't See Yet

WSA acts as an in-memory counter that survives between formula calls. Row 5 saves its assigned count to WSA. When Row 8 runs, it reads from WSA instead of querying the table:

| Row | WSA has data? | Source of MAX | Assigns | Saves to WSA |
| --- | --- | --- | --- | --- |
| Row 5 | NO | PAY_ELEMENT_ENTRIES_F → MAX = 1 | 2 | WSA_SET(2) |
| Row 8 | YES → 2 | WSA memory (skips table) | 3 | WSA_SET(3) |

What the .dat file looks like — each row gets a unique count:

ElementEntry.dat — PASS output

Existing entry (already in Oracle):

| ElementName | Dental EE Deduction |
| --- | --- |
| MultipleEntryCount | 1 |

Row 5 output ($175.00):

| ElementName | Dental EE Deduction |
| --- | --- |
| MultipleEntryCount | 2 [OK] |

Row 8 output ($200.00):

__DARK_1__

PASS Three unique MultipleEntryCount values (1, 2, 3) in the .dat file. Oracle loads all three entries successfully.

The Fast Formula Code

```text
/* Check: did a previous row already assign a count for this combo? */
IF WSA_EXISTS('MEC_' || L_PersonNumber || '_' || l_ElementName || '_' || POSITION2) THEN
(
    /* YES — read last assigned count and add 1 */
    l_MultipleEntryCount = WSA_GET('MEC_' || ..., 0) + 1
)
ELSE
(
    /* NO — first row for this combo. Ask the database. */
    l_db_max = GET_VALUE_SET('MAX_MULTI_ENTRY_COUNT', ...)

    IF ISNULL(l_db_max) = 'N' THEN
        l_MultipleEntryCount = 1              /* Nothing in cloud → start at 1 */
    ELSE
        l_MultipleEntryCount = l_db_max + 1  /* Cloud has 1 → assign 2 */
)

/* Save what we assigned — next row reads this instead of hitting DB */
WSA_SET('MEC_' || L_PersonNumber || '_' || l_ElementName || '_' || POSITION2, l_MultipleEntryCount)
```

**Summary in one line:** WSA is a working storage area that persists across formula invocations — like a PL/SQL package variable. The formula writes the assigned count to WSA, so the next row with the same combo reads from memory instead of hitting a stale database. The formula writes the assigned count to WSA, so the next row with the same combo reads from memory instead of hitting a stale database.

After Step 4: `l_MultipleEntryCount = 2` (cloud had 1, so we assigned 1 + 1)

WSA in This Formula — Connecting Step 3 and Step 4

You've now seen WSA used twice in the MAP block, but for **two completely different reasons**. Let's connect them before moving to Step 5.

| Step | WSA Key | What It Stores | Why | What Breaks Without It |
| --- | --- | --- | --- | --- |
| Step 3 | PER_<SSN>_<Date>**ASG_<SSN>_<Date> | Person NumberAssignment Number | Performance | Same SSN queried 3x instead of 1x. Slow but correct. |
| Step 4 | MEC_<Person>_<Element>_<Date> | Last assigned MultipleEntryCount | Correctness | Duplicate MULTIPLE_ENTRY_COUNT in PAY_ELEMENT_ENTRIES_F. Data lost. |

This is the key distinction:

Removes WSA from Step 3 → formula still works correctly**

It just runs **slower** (3 DB calls instead of 1 per SSN group)

Remove WSA from Step 4 → formula **produces wrong output**

Duplicate counts → rows overwrite each other in PAY_ELEMENT_ENTRIES_F

Both use the same WSA methods (`WSA_EXISTS`, `WSA_GET`, `WSA_SET`), same pattern (check → hit or miss → store), but different purposes. Step 3 is optional optimization. Step 4 is mandatory for data integrity.

---

You've now seen WSA used in Step 3 and Step 4. Let's go deeper into how it works, what this formula caches, and one critical deployment rule you can't skip.

What Is WSA?

WSA (Working Storage Area) is, per Oracle documentation, **a mechanism for storing global values across formulas**. Local variables die after each formula invocation, but WSA values persist across calls within the same session. You write a value on Row 1, and you can read it back on Row 500. WSA names are **case-independent** — `'PER_123'` and `'per_123'` refer to the same item.

In PL/SQL terms: WSA is a package-level associative array (`TABLE OF VARCHAR2 INDEX BY VARCHAR2`). It persists across function calls within the same session.

The API — Four Methods

| Method | PL/SQL Equivalent | What It Does |
| --- | --- | --- |
| WSA_EXISTS(item [, type]) | g_cache.EXISTS(key) | Tests whether item exists in the storage area. Optional `type` parameter restricts to a specific data type (TEXT, NUMBER, DATE, TEXT_TEXT, TEXT_NUMBER, etc.) |
| WSA_GET(item, default-value) | l_val := g_cache(key) | Retrieves the stored value. If item doesn't exist, returns the **default-value** instead. The data type of default-value determines the expected data type. |
| WSA_SET(item, value) | g_cache(key) := val | Sets the value for item. Any existing item of the same name is **overwritten**. |
| WSA_DELETE([item]) | g_cache.DELETE(key) | Deletes item from storage. If no name specified, **all storage area data is deleted**. Not used in this vendor formula, but important for cleanup scenarios. |

**Key detail from Oracle docs:** `WSA_GET` always requires a **default-value** parameter. The formula always calls `WSA_EXISTS` first and only calls `WSA_GET` when the item is known to exist — so the default is never actually used, but it must still be provided. The data type of the default tells the engine what data type to expect.

Every WSA usage in this formula follows the same pattern. You already saw it twice:

```text
/* THE PATTERN — same in Step 3, Step 4, and everywhere else */

IF WSA_EXISTS(l_key) THEN            /* 1. Check memory */
    l_value = WSA_GET(l_key, ' ')    /* 2a. HIT  — read from memory (default never used) */
ELSE
    l_value = GET_VALUE_SET(...)      /* 2b. MISS — call the database */
    WSA_SET(l_key, l_value)          /* 3.  SAVE — store for next row */
```

Where You Already Saw This Pattern

| Key: | 'PER_123-45-6789_2024-01-15' |
| --- | --- |
| Stores: | Person Number (100045) |
| DB call saved: | GET_VALUE_SET('XXVA_GET_PERSON_NUMBER') |
| Purpose: | Performance — same SSN in 3 rows, only 1 DB call |

| Key: | 'MEC_100045_Dental EE Deduction_2024-01-15' |
| --- | --- |
| Stores: | Last assigned count (2, then 3, then 4...) |
| DB call saved: | GET_VALUE_SET('MAX_MULTI_ENTRY_COUNT') |
| Purpose: | Correctness — prevents duplicate MULTIPLE_ENTRY_COUNT |

All WSA Keys This Formula Uses

Steps 3 and 4 are the two main ones, but the formula caches more. Here's the complete list:

| WSA Key | Stores | Used In | Type |
| --- | --- | --- | --- |
| PER_<SSN>_<Date> | Person Number | Step 3 | Performance |
| ASG_<SSN>_<Date> | Assignment Number | Step 3 | Performance |
| MEC_<Person>_<Element>_<Date> | Last assigned MultipleEntryCount | Step 4 | Correctness |
| SSID_, SSO_, EEVID_, EEVO_ | SourceSystemId/Owner lookups | Step 5 | Performance |
| HDR_<Person>_<Element>_<Date> | Flag: ElementEntry header already generated | Section 7 | Correctness |

**Pattern:** Performance keys (PER_, ASG_, SSID_) can be removed and the formula still works — just slower. Correctness keys (MEC_, HDR_) cannot be removed — the formula produces wrong data without them.

Traced Example: 3 Benefit Plan Rows, Same Employee

Watch Step 3 and Step 4 WSA caching in action across three rows for SSN 123-45-6789:

Vendor Input File — 3 rows for the same employee (SSN 123-45-6789)

| Row | POS1 (SSN) | POS2 (Date) | POS3 (Plan) | POS4 (Type) | POS5 (Amt) |
| --- | --- | --- | --- | --- | --- |
| Row 1 | 123-45-6789 | 2024-01-15 | DENTAL01 | PRE | 150.00 |
| Row 2 | 123-45-6789 | 2024-01-15 | MEDICAL01 | PRE | 75.50 |
| Row 3 | 123-45-6789 | 2024-01-15 | VISION01 | PRE | 12.30 |

Same SSN, same date — but **different benefit plans**. This is typical: one employee enrolled in Dental + Medical + Vision.

Now let's trace what happens when the formula processes each row:

STEP 3
Person & Assignment Lookup

| WSA Check | WSA_EXISTS('PER_123-45-6789_2024-01-15') | MISS |
| --- | --- | --- |
| Action | Call DB → Person# = **100045**, Asg# = **E12345** |
| WSA Save | WSA_SET('PER_...', 100045)   WSA_SET('ASG_...', E12345) |

STEP 4
MultipleEntryCount

| WSA Check | WSA_EXISTS('MEC_100045_Dental EE Deduction_2024') | MISS |
| --- | --- | --- |
| Action | Call DB → MAX = NULL (no existing entry) |
| Result | MultipleEntryCount = 1   → WSA_SET('MEC_...Dental...', 1) |

DB calls: **11** — all cache misses (first time seeing this SSN)

STEP 3
Person & Assignment Lookup

| WSA Check | WSA_EXISTS('PER_123-45-6789_2024-01-15') | HIT! |
| --- | --- | --- |
| Action | WSA_GET → Person# 100045, Asg# E12345 — zero DB calls |

STEP 4
MultipleEntryCount
— different element name = new WSA key

| WSA Check | WSA_EXISTS('MEC_100045_**Medical** EE Deduction_2024') | MISS |
| --- | --- | --- |
| Action | Call DB → MAX = NULL |
| Result | MultipleEntryCount = 1   → WSA_SET('MEC_...Medical...', 1) |

DB calls: **4** — Step 3 saved 2 calls (cache hit), Step 4 missed (different element)

STEP 3
Person & Assignment Lookup

| WSA Check | WSA_EXISTS('PER_123-45-6789_2024-01-15') | HIT! |
| --- | --- | --- |
| Action | WSA_GET → Person# 100045, Asg# E12345 — zero DB calls |

STEP 4
MultipleEntryCount
— yet another element = yet another WSA key

| WSA Check | WSA_EXISTS('MEC_100045_**Vision** EE Deduction_2024') | MISS |
| --- | --- | --- |
| Action | Call DB → MAX = NULL |
| Result | MultipleEntryCount = 1 |

DB calls: **4** — same pattern as Row 2

The Pattern:

|  | Step 3 (Person lookup) | Step 4 (MEC) |
| --- | --- | --- |
| Row 1 | MISS — call DB | MISS — call DB |
| Row 2 | HIT — zero DB calls | MISS — different element |
| Row 3 | HIT — zero DB calls | MISS — different element |

Step 3 always hits after Row 1 (same SSN = same key). Step 4 always misses here because each row maps to a different element. Step 4 WSA becomes critical when the batch has multiple rows for the **same person + same element**.

Performance at Scale

For 10,000 vendor rows where employees average 3 benefit plans each:

value set calls (10K × 11 per row)

63% reduction — Step 3 caching saves ~7 calls per duplicate SSN

Critical Rule: Set Threads = 1

There's one deployment rule for WSA that you absolutely cannot skip:

If "Load Data from File" runs with 4 threads, each thread gets its **own independent WSA**:

| Step 3 breaks: | Thread 1 caches Person# for SSN 123. Thread 2 gets a different row for the same SSN — but Thread 2's WSA is empty. It calls the value set again. (Wastes performance, but data is still correct.) |
| --- | --- |
| Step 4 breaks: | Thread 1 assigns MultipleEntryCount = 2 and saves to its WSA. Thread 2 gets another row for the same person+element — but Thread 2's WSA is empty. It queries the DB, gets MAX = 1, assigns count = 2. **Duplicate. Data lost.** |

**The fix:**

My Client Groups
→
Payroll
→
Payroll Process Configuration
→
Threads = 1

Set thread count to 1 before running "Load Data from File." All rows process sequentially in one thread. WSA works as a true shared cache across every row.

---

Step 5: SourceSystemId Resolution

| All resolved values from Steps 1–4 | → l_SourceSystemId = 'HDL_XXVA_E12345_EE_100045_Dental EE Deduction_20240115' |
| --- | --- |

Oracle HDL uses SourceSystemId as the MERGE key. If an entry already exists in cloud, the formula reuses its SourceSystemId (so HDL updates it). If not, it constructs one:

```text
/* For active employees — construct using PersonNumber */
'HDL_XXVA' || l_AssignmentNumber || '_EE_' || L_PersonNumber || '_' || l_ElementName || '_' || POSITION2

/* For terminated employees (PersonNumber unavailable) — use SSN */
'HDL_XXVA' || l_AssignmentNumber || '_EE_' || POSITION1 || '_' || l_ElementName || '_' || POSITION2
```

After all five steps, the formula has everything it needs: Element Name, Assignment Number, Person Number, MultipleEntryCount, SourceSystemId, and the dollar amount. Now it generates the HDL output rows (Sections 7 and 8).

---

Vendor Input (what the formula receives):

| POSITION1 | SSN | 123-45-6789 |
| --- | --- | --- |
| POSITION2 | Date | 2024-01-15 |
| POSITION3 | Plan Code | DENTAL01 |
| POSITION4 | Ded Type | PRE |
| POSITION5 | Amount | 150.00 |
| POSITION11 | Status | (blank = Active) |

### ↓ Formula transforms (Steps 1–5 + LINEREPEATNO=1) ↓

HDL .dat Output (ElementEntry):

| BusinessOperation | MERGE |
| --- | --- |
| FileDiscriminator | ElementEntry |
| LegislativeDataGroupName | 570 |
| EffectiveStartDate | 2024/01/15 |
| ElementName | Dental EE Deduction |
| AssignmentNumber | E12345 |
| CreatorType | H |
| EntryType | E |
| MultipleEntryCount | 1 |
| SourceSystemOwner | HDL_XXVA |
| SourceSystemId | HDL_XXVA_E12345_EE_... |

After the five MAP steps, the formula has all the values it needs. Now it generates the actual HDL output. Each vendor source row produces **multiple** HDL output rows — one ElementEntry header on pass 1, followed by one ElementEntryValue per input value on passes 2 through 7. LINEREPEATNO controls which one gets generated on each pass.

How LINEREPEAT Works

The HDL engine calls the formula once per source row with `LINEREPEATNO = 1`. If the formula returns `LINEREPEAT = 'Y'`, the engine calls the formula **again for the same row** — this time with `LINEREPEATNO = 2`.

```text
/* HDL engine processes one vendor source row: */

/* Pass 1: LINEREPEATNO = 1 → ElementEntry header */
Formula outputs →  MERGE|ElementEntry|...|Dental EE Deduction|...
Formula returns →  LINEREPEAT = 'Y'   ← call me again

/* Pass 2: LINEREPEATNO = 2 → EEV: Amount = 150.00 */
Formula outputs →  MERGE|ElementEntryValue|...|Amount|...|150.00
Formula returns →  LINEREPEAT = 'Y'   ← call me again (more input values)

/* Pass 3: LINEREPEATNO = 3 → EEV: Period Type = Monthly */
Formula outputs →  MERGE|ElementEntryValue|...|Period Type|...|Monthly
Formula returns →  LINEREPEAT = 'Y'   ← call me again

/* ... passes 4–6 for Loan Number, Total Owed, Percentage (if applicable) ... */

/* Pass 7: LINEREPEATNO = 7 → EEV: Deduction Amount (last pass) */
Formula outputs →  MERGE|ElementEntryValue|...|Deduction Amount|...
Formula returns →  LINEREPEAT = 'N'   ← done, move to next source row
```

One source row → multiple output rows (1 ElementEntry + up to 6 ElementEntryValues). The HDL engine groups all ElementEntry rows together and all ElementEntryValue rows together in the final `.dat` file, separated by their METADATA header rows.

The .dat Output Structure

The final .dat file has two blocks. Each block starts with a METADATA row that defines the columns, followed by the MERGE data rows:

Block 1 — ElementEntryValue (generated by LINEREPEATNO = 2–7)

```text
A         B                C    D           E                  F               G               J                  K
METADATA  ElementEntryVal  LDG  EffStart    ElementName        AssignmentNum   InputValueName  MultipleEntryCount ScreenEntryValue
MERGE     ElementEntryVal  570  22-09-2019  Dental EE Deduct   123141402543    Amount          3                  150.00
MERGE     ElementEntryVal  222  22-09-2019  Dental EE Deduct   123141402554    Amount          6                  25.72
MERGE     ElementEntryVal  570  22-09-2019  Dental EE Deduct   123141402543    Amount          1                  150.00
...       more rows
```

Block 2 — ElementEntry (generated by LINEREPEATNO = 1)

```text
A         B             C    D           E                  F               G           I          J
METADATA  ElementEntry  LDG  EffStart    ElementName        AssignmentNum   CreatorType EntryType  MultipleEntryCount
MERGE     ElementEntry  570  22-09-2019  Dental EE Deduct   123141402543    H           E          3
MERGE     ElementEntry  222  22-09-2019  Dental EE Deduct   123141402554    H           E          6
...       more rows
```

The key columns to notice: ElementEntry has **CreatorType** and **EntryType** but no dollar amount. ElementEntryValue has **InputValueName** (always "Amount") and **ScreenEntryValue** (the actual dollar amount like 150.00). Both carry **MultipleEntryCount** from Step 4.

What LINEREPEATNO = 1 Generates

On the first pass, the formula checks POSITION11 (the STATUS column from the vendor file). This decides whether we're creating a new entry or end-dating an existing one:

| POSITION11 | ElementEntry row generated | LINEREPEAT |
| --- | --- | --- |
| Blank (Active) | `MERGE\|ElementEntry\|570\|22-09-2019\|Dental EE Deduction\|123141402543\|H\|\|E\|1`**
EffectiveStartDate = POSITION2. No EndDate. CreatorType = H. EntryType = E. | 'Y'→ needs pass 2 |
| C (Cancel) | `MERGE\|ElementEntry\|570\|22-09-2019\|Dental EE Deduction\|123141402543\|H\|2019/09/22\|E\|1\|...\|Y`
Fetches original StartDate from cloud. Sets EndDate = cancellation date. Appends ReplaceLastEffectiveEndDate = Y. | 'N'→ no detail needed |

How the Code Actually Writes the ElementEntry Row

The formula does not** use positional output variables like `HDL_LINE1_N`. Instead, it assigns values to **named output variables** that match the METADATA column names. Then an explicit `RETURN` statement tells the HDL engine which variables to pick up and in what order.

Here's the Active path (POSITION11 is blank):

```text
IF LINEREPEATNO = 1 THEN
(
    /* ======================================== */
    /* ACTIVE entry — create new ElementEntry   */
    /* ======================================== */

    FileName                    = 'ElementEntry'
    BusinessOperation           = 'MERGE'
    FileDiscriminator           = 'ElementEntry'
    LegislativeDataGroupName    = l_LegislativeDataGroupName
    AssignmentNumber            = l_AssignmentNumber
    ElementName                 = l_ElementName
    EffectiveStartDate          = TO_CHAR(TO_DATE(TRIM(POSITION2),'YYYY/MM/DD'),'YYYY/MM/DD')
    EntryType                   = l_entry_type
    CreatorType                 = l_CreatorType
    SourceSystemOwner           = l_SourceSystemOwner
    SourceSystemId              = l_SourceSystemId
    LINEREPEAT                  = 'Y'             /* ← call me again for ElementEntryValue */

    RETURN BusinessOperation, FileName, FileDiscriminator,
           CreatorType, EffectiveStartDate, ElementName,
           LegislativeDataGroupName, EntryType, AssignmentNumber,
           SourceSystemOwner, SourceSystemId,
           LINEREPEAT, LINEREPEATNO
)
```

**How the RETURN works:** The variable names in the RETURN statement must match the METADATA column names exactly. The HDL engine maps each returned variable to its corresponding METADATA position and writes the pipe-delimited row in that order. `FileName` and `FileDiscriminator` go to positions [1] and [2]. The rest map by name to the METADATA array you defined in Section 5.

For a **Cancel** row (POSITION11 = 'C'), the formula fetches the original start date from the cloud, sets an end date, and returns `LINEREPEAT = 'N'` (no pass 2 needed — you don't need an ElementEntryValue for a cancellation):

```text
IF (TRIM(POSITION11) = 'C') THEN
(
    /* Fetch the original start date from cloud */
    l_Effective_Start_Date = GET_VALUE_SET('XXVA_GET_EE_START_DATE', ...)

    /* Same named variables, but with end date + replace flag */
    FileName                    = 'ElementEntry'
    BusinessOperation           = 'MERGE'
    FileDiscriminator           = 'ElementEntry'
    EffectiveStartDate          = TO_CHAR(TO_DATE(l_Effective_Start_Date,...),'YYYY/MM/DD')
    EffectiveEndDate            = TO_CHAR(TO_DATE(TRIM(POSITION2),...),'YYYY/MM/DD')
    ReplaceLastEffectiveEndDate = 'Y'
    LINEREPEAT                  = 'N'              /* ← no pass 2 for cancel */
    /* ...same other variables as Active... */

    RETURN BusinessOperation, FileName, FileDiscriminator,
           CreatorType, EffectiveStartDate, EffectiveEndDate,
           ElementName, LegislativeDataGroupName, EntryType,
           AssignmentNumber, SourceSystemOwner, SourceSystemId,
           ReplaceLastEffectiveEndDate,
           LINEREPEAT, LINEREPEATNO
)
```

Notice the Cancel RETURN includes `EffectiveEndDate` and `ReplaceLastEffectiveEndDate` — both absent from the Active RETURN.

Duplicate Header Prevention (WSA)

One person can have multiple vendor rows (Dental, Medical, Vision) that all map to different elements. Each element needs exactly one ElementEntry row. But if two vendor rows map to the **same** element, the formula must not generate a duplicate header. It checks WSA:

```text
IF WSA_EXISTS('HDR_' || L_PersonNumber || '_' || l_ElementName || '_' || POSITION2) THEN
(
    /* Header already generated for this combo — skip to pass 2 */
    LINEREPEAT = 'Y'
    RETURN
)
/* First time for this combo — generate header, then mark in WSA */
WSA_SET('HDR_' || ..., 1)
```

Watch out: ISNULL is inverted

The formula checks `ISNULL(l_ElementName) = 'N'` before generating anything. In Fast Formula, `'N'` means the value IS null (not found). If the vendor code didn't map to any element, the formula skips the row silently.

---

Same Vendor Input Row → multiple ElementEntryValue outputs (one per input value):

### ↓ Each pass loads a different InputValueName ↓

Pass 2 — ElementEntryValue (Amount):

| InputValueName | Amount |
| --- | --- |
| ScreenEntryValue | 150.00 |
| ElementEntryId(SSID) | HDL_XXVA_E12345_EE_... (links to parent ElementEntry) |

Pass 3 — ElementEntryValue (Period Type):

| InputValueName | Period Type |
| --- | --- |
| ScreenEntryValue | Monthly |

Pass 6 — ElementEntryValue (Percentage):

| InputValueName | Percentage |
| --- | --- |
| ScreenEntryValue | 5.5 |

Passes 4, 5, 7 skipped — PRE type doesn't use Loan Number, Total Owed, or Deduction Amount. The formula returns `LINEREPEAT = 'Y'` with no output data on those passes.

Passes 2 through 7 each generate one ElementEntryValue row. Each pass loads a different input value. The deduction type (POSITION4) controls which passes produce output and which ones skip.

What LINEREPEATNO = 2 Generates

Each ElementEntryValue pass sets `InputValueName` to a different value and loads the corresponding data into `ScreenEntryValue`:

| Column | Value | Source |
| --- | --- | --- |
| LINEREPEATNO | InputValueName | ScreenEntryValue source |
| 2 | Amount | l_Amount (POSITION5) = 150.00 |
| 3 | Period Type | l_PeriodType (POSITION6) = Monthly |
| 4 | Loan Number | POSITION8 — LOAN type only |
| 5 | Total Owed | l_TotalOwed — LOAN type only |
| 6 | Percentage | l_Percentage (POSITION7) — PRE/POST type only |
| 7 | Deduction Amount | l_DeductionAmount — CU type only |

How the Code Actually Writes the ElementEntryValue Row

Each pass from 2 to 7 follows the same structure. The key difference is the skip logic: each pass checks POSITION4 (deduction type) to decide whether to generate output or just return `LINEREPEAT = 'Y'` with no data (effectively skipping to the next pass). Same pattern — named output variables + explicit RETURN. But now `FileDiscriminator = 'ElementEntryValue'` (not 'ElementEntry'), and the RETURN includes `InputValueName`, `ScreenEntryValue`, and the parent link `"ElementEntryId(SourceSystemId)"`.

```text
ELSE IF (LINEREPEATNO = 2) THEN
(
    l_InputValueName = 'Amount'

    /* Look up ElementEntryValue SourceSystemId from cloud (or construct new one) */
    l_EEV_SourceSystemId = GET_VALUE_SET(
        'XXVA_GET_EEV_SOURCE_SYSTEM_ID', ...)
    l_EEV_SourceSystemOwner = GET_VALUE_SET(
        'XXVA_GET_EEV_SOURCE_SYSTEM_OWNER', ...)

    /* If no existing SSID found, construct a new one */
    IF ISNULL(l_EEV_SourceSystemId) = 'N' THEN
    (
        l_EEV_SourceSystemId = 'HDL_XXVA' || l_AssignmentNumber
            || '_EEV_' || L_PersonNumber
            || '_' || l_ElementName
            || '_' || l_InputValueName
            || '_' || TO_CHAR(TO_DATE(TRIM(POSITION2),...),'YYYYMMDD')
    )

    /* ============================================= */
    /* Set the output variables for ElementEntryValue */
    /* ============================================= */

    FileName                          = 'ElementEntry'        /* always ElementEntry */
    BusinessOperation                 = 'MERGE'
    FileDiscriminator                 = 'ElementEntryValue'   /* ← THIS is the key difference */
    LegislativeDataGroupName          = l_LegislativeDataGroupName
    AssignmentNumber                  = l_AssignmentNumber
    ElementName                       = l_ElementName
    EntryType                         = l_entry_type
    EffectiveStartDate                = TO_CHAR(...)
    "ElementEntryId(SourceSystemId)"  = l_SourceSystemId      /* ← links to parent ElementEntry */
    SourceSystemId                    = l_EEV_SourceSystemId  /* ← EEV's own SSID */
    SourceSystemOwner                 = l_EEV_SourceSystemOwner
    InputValueName                    = l_InputValueName      /* 'Amount' */
    ScreenEntryValue                  = To_Char(TO_NUM(TRIM(l_Amount)))
    LINEREPEAT                        = 'Y'                  /* more passes to come (pass 7 returns 'N') */

    RETURN BusinessOperation, FileName, FileDiscriminator,
           AssignmentNumber, EffectiveStartDate, ElementName,
           EntryType, LegislativeDataGroupName,
           "ElementEntryId(SourceSystemId)",
           InputValueName, ScreenEntryValue,
           SourceSystemOwner, SourceSystemId,
           LINEREPEAT, LINEREPEATNO
)
```

**Three things to notice:**

**1.** `FileName` is still `'ElementEntry'` — NOT `'ElementEntryValue'`. Only the `FileDiscriminator` changes to `'ElementEntryValue'`. This is how HDL knows the row goes into the ElementEntryValue block of the .dat file.**

2.** `"ElementEntryId(SourceSystemId)"` is set to the **ElementEntry's** SourceSystemId (`l_SourceSystemId`). This is the parent-child link. The variable name contains parentheses, so it must be double-quoted in the formula code.**

3.** The ElementEntryValue has its **own** SourceSystemId (`l_EEV_SourceSystemId`), different from the parent ElementEntry's. The formula first tries to find an existing one from the cloud via value set. If not found (`ISNULL = 'N'`), it constructs one with the pattern: `HDL_XXVA + AssignmentNumber + _EEV_ + PersonNumber + _ElementName + _InputValueName + _Date`.

The Parent-Child Link

The ElementEntryValue row must reference its parent ElementEntry row. HDL uses SourceSystemId to link them:

ElementEntry (Pass 1)

SourceSystemId = HDL_XXVA_E12345_EE_...

## →

ElementEntryValue (Pass 2)

ElementEntryId(SSID) = HDL_XXVA_E12345_EE_...

SourceSystemId = HDL_XXVA_E12345_EEV_...

The ElementEntryValue's `ElementEntryId(SourceSystemId)` matches the ElementEntry's `SourceSystemId`. This is how HDL knows which entry this value belongs to.

The RTRIM Trick for Clean Numbers

the vendor sends amounts like `150.00`, but Oracle elements expect clean numbers. The formula strips trailing zeros:

```text
RTRIM(RTRIM(TRIM(l_Amount), '0'), '.')

/* 150.00 → 150 | 75.50 → 75.5 | 12.30 → 12.3 | 150.00 → 150.00 */
```

The inner RTRIM strips trailing zeros. The outer RTRIM strips the decimal point if nothing is left after it.

---

**Vendor CSV Row:** `123-45-6789,2024-01-15,DENTAL01,150.00,,,`

STEP 1: Type → ER, Amount → 150.00

STEP 2: Key → DENTAL01 → Dental EE Deduction

STEP 3: SSN → Person# 100045, Asg# E12345 (WSA)

STEP 4: MultipleEntryCount = 1

STEP 5: SourceSystemId constructed

LINEREPEATNO=1 → ElementEntry:

```text
MERGE|ElementEntry|570|2019/09/22|Dental EE Deduction|123141402543|H||E|1
```

LINEREPEATNO=2 → ElementEntryValue (Amount):

```text
MERGE|ElementEntryValue|570|2019/09/22|Dental EE Deduction|123141402543|Amount||E||1|150.00
```

---

If you've read this far, you can now explain — without looking at any code — how an HDL Transformation Formula works end-to-end. You know what each OPERATION does, why METADATA arrays define the .dat column headers, how the MAP block transforms source data in 5 steps, why WSA exists (performance + correctness), how LINEREPEATNO generates multiple output rows (1 ElementEntry + up to 6 ElementEntryValues) from one source row, and how named RETURN variables map to METADATA columns.

That's the foundation. The concepts don't change whether you're building an vendor deduction interface, a benefits enrollment loader, or a payroll costing feed. Every HDL Transformation Formula follows this same structure.

Coming Next — Part 2: Code Walkthrough

Part 2 takes every concept from this post and shows you the actual Fast Formula code that implements it. Line by line, with the Notepad++ syntax highlighting you've been seeing in the code snippets here.

What Part 2 will cover:

| Full INPUTS ARE block | Every POSITION mapped to its vendor column, every DEFAULT FOR explained |
| --- | --- |
| GET_VALUE_SET calls | The exact parameter string construction with pipe delimiters, date conversions, and ISNULL checking |
| WSA implementation | Real WSA_EXISTS / WSA_GET / WSA_SET code with key construction patterns |
| SourceSystemId logic | The full lookup-or-construct pattern for both ElementEntry and ElementEntryValue SourceSystemIds |
| ESS_LOG_WRITE debugging | Adding trace logs at each step so you can debug formula execution in real time |
| Cancel vs Active branching | The complete IF POSITION11 = 'C' block with date fetching from cloud |

Later — Part 3: Build Your Own

Part 3 is the implementation guide. You'll build an HDL Transformation Formula from scratch — from creating the formula in Oracle Cloud, defining all 11 value sets, configuring the HDL integration, running test loads, reading ESS logs, and troubleshooting the errors you'll hit in production.

After Part 3, you'll have a working formula you can adapt for any inbound payroll interface — not just one vendor.

Series Roadmap

Part 1: Pure Concepts ← This post

→

Part 2: Code Walkthrough Coming soon

→

Part 3: Build Your Own Coming soon

Abhishek Mohanty

```text
ELEMENT_ENTRY_ID  PERSON_ID  ELEMENT_TYPE_ID         EFFECTIVE_START_DATE  MULTIPLE_ENTRY_COUNT  ENTRY_TYPE
300000012345      100045     50001 (Dental EE Ded)   01-Oct-2024           1                     E
```

https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap");

@media (prefers-color-scheme: dark) {
  .hdl-blog { background: #12131A !important; color: #C8C9D4 !important; }
  .hdl-blog p, .hdl-blog li { color: #C8C9D4 !important; }
  .hdl-blog strong { color: #EAEBF0 !important; }
  .hdl-blog em { color: #C8C9D4 !important; }
  .hdl-blog code { background: #1E1F2B !important; color: #D4D5DE !important; }
  .hdl-blog hr { border-color: #2A2B38 !important; }

  .hdl-blog [style*="background:linear-gradient(135deg,#1B4965"] { background: linear-gradient(135deg,#0D2B3E,#081C2B) !important; box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important; }
  .hdl-blog [style*="font-size:17px"][style*="font-weight:700"] { color: #EAEBF0 !important; }
  .hdl-blog [style*="font-size:15px"][style*="font-weight:700"][style*="border-left"] { color: #D4D5DE !important; }

  .hdl-blog [style*="background:#fff"] { background: #1A1B26 !important; }
  .hdl-blog [style*="background:#F5F3EF"] { background: #16171F !important; }
  .hdl-blog [style*="background:#FDF5ED"] { background: #1C1812 !important; border-color: #3D3224 !important; }
  .hdl-blog [style*="background:#FCF0F0"] { background: #1C1414 !important; }
  .hdl-blog [style*="background:#EDE8E0"] { background: #1E1F2B !important; }

  .hdl-blog [style*="#DDD8D0"] { border-color: #2A2B38 !important; }
  .hdl-blog td, .hdl-blog th, .hdl-blog tr { border-color: #2A2B38 !important; }

  .hdl-blog td { color: #C8C9D4 !important; }
  .hdl-blog th { color: #fff !important; }
  .hdl-blog td[style*="font-weight:700"] { color: #EAEBF0 !important; }
  .hdl-blog td[style*="font-weight:600"] { color: #D4D5DE !important; }
  .hdl-blog td[style*="font-weight:800"] { color: #EAEBF0 !important; }

  .hdl-blog [style*="color:#D4622B"] { color: #E89060 !important; }
  .hdl-blog td[style*="color:#D4622B"] { color: #E89060 !important; }
  .hdl-blog [style*="background:#D4622B"], .hdl-blog [style*="background:linear-gradient(135deg,#D4622B"] { color: #fff !important; }

  .hdl-blog [style*="color:#2D8B6F"] { color: #5CC4A0 !important; }
  .hdl-blog [style*="background:#2D8B6F"] { background: #1A5C47 !important; }

  .hdl-blog [style*="color:#C13B3B"] { color: #F08080 !important; }
  .hdl-blog [style*="background:#C13B3B"] { background: #8B2020 !important; }
  .hdl-blog [style*="border"][style*="#C13B3B"] { border-color: #5C1A1A !important; }

  .hdl-blog [style*="color:#8B8FA8"] { color: #6B6F88 !important; }

  .hdl-blog pre { background: #0D0E14 !important; border-color: #1E1F2B !important; }

  .hdl-blog [style*="background:#1E1E1E"] { background: #0D0E14 !important; }
  .hdl-blog [style*="background:#1E1E1E"] td[style*="color:#8B8FA8"] { color: #6B6F88 !important; }
  .hdl-blog [style*="background:#1E1E1E"] td[style*="color:#B5CEA8"] { color: #B5CEA8 !important; }
  .hdl-blog [style*="background:#1E1E1E"] td[style*="color:#CE9178"] { color: #CE9178 !important; }
  .hdl-blog [style*="background:#1E1E1E"] td[style*="color:#2D8B6F"] { color: #5CC4A0 !important; }
  .hdl-blog [style*="background:#1E1E1E"] td[style*="color:#C13B3B"] { color: #F08080 !important; }

  .hdl-blog [style*="background:#1B4965"] { background: #0D2B3E !important; }

  .hdl-blog [style*="font-size:28px"][style*="color:#C13B3B"] { color: #F08080 !important; }
  .hdl-blog [style*="font-size:28px"][style*="color:#D4622B"] { color: #E89060 !important; }

  .hdl-blog [style*="background:#eee"] { background: #2A2B38 !important; color: #8B8FA8 !important; }

  .hdl-blog span[style*="border-radius:10px"] { color: #fff !important; }
  .hdl-blog span[style*="border-radius:12px"] { color: #fff !important; }

  .hdl-blog [style*="font-size:30px"][style*="font-weight:800"] { color: #F0F1F5 !important; }

  .hdl-blog td[style*="font-family:monospace"] { color: #C8C9D4 !important; }

  .hdl-blog [style*="color:#1A1A2E"] { color: #EAEBF0 !important; }
  .hdl-blog [style*="color:#3D3D5C"] { color: #C8C9D4 !important; }
}

.hdl-blog table { min-width: 400px; }

.hdl-blog .block-table { font-size: 11px !important; }
.hdl-blog .block-table td, .hdl-blog .block-table th { padding: 5px 6px !important; font-size: 11px !important; white-space: nowrap !important; }
.hdl-blog .db-table { font-size: 11px !important; }
.hdl-blog .db-table td, .hdl-blog .db-table th { padding: 5px 6px !important; font-size: 11px !important; white-space: nowrap !important; }

.hdl-blog div[style*="overflow:hidden"] { overflow-x: auto !important; }

Vendor Deduction Interface | ElementEntry + ElementEntryValue

This is **Part 1** of a 3-part series on HDL Transformation Formulas. This post covers the concepts end-to-end — what each section of the formula does and why. No code to copy-paste here. Just the understanding you need before writing a single line.

HDL Transformation Formula Series

Pure Concepts ← You are here

What each section of the formula does. INPUTS, OPERATION, METADATA, MAP (5 steps), WSA, LINEREPEATNO, RETURN. Zero code to memorize — just understanding.

Code Walkthrough Coming soon

The actual formula code, explained line-by-line. Value set definitions, WSA implementation, date conversions, ISNULL patterns, ESS_LOG_WRITE debugging. Moderate complexity — you'll be able to read any HDL formula after this.

Build Your Own Coming soon

Full implementation guide. Setting up the formula in Oracle, creating the value sets, configuring the HDL integration, testing with real data, debugging production issues. Copy-paste ready.

Abhishek Mohanty

Before we go section by section, here's what this formula does end to end:

Vendor CSV File**SSN, Date, Code, Amounts

HDL Transformation
This Formula

ElementEntry .dat
Header + Value rows

A third-party benefits administration vendor (BenAdmin) sends a CSV with deduction and employer contribution amounts. This formula transforms each row into Oracle HDL format — resolving SSNs to Assignment Numbers, mapping vendor codes to Oracle Element Names, managing MultipleEntryCount, and generating both ElementEntry (header) and ElementEntryValue (detail) rows.

---

The vendor manages employee benefit enrollments — medical, dental, vision, life insurance, FSA, HSA, loans. Every pay period, they send a flat CSV file with deduction details to load into Oracle as Element Entries.

The Raw Input File Layout

Each row in the vendor file maps to one set of delimited columns. The HDL engine reads these into POSITION variables:

| Column | Position | Description | Example |
| --- | --- | --- | --- |
| SSN | POSITION1 | Employee Social Security Number | 123-45-6789 |
| EFFECTIVE_DATE | POSITION2 | Date the deduction applies (YYYY-MM-DD) | 2024-01-15 |
| BENEFIT_PLAN_CODE | POSITION3 | Vendor’s internal code for the benefit plan | DENTAL01 |
| DEDUCTION_TYPE | POSITION4 | Controls LINEREPEATNO branches and how many input values are loaded | LOAN, PRE, POST, CU |
| AMOUNT | POSITION5 | Deduction amount (InputValueName = ‘Amount’) | 150.00 |
| PERIOD_TYPE | POSITION6 | Period type for the deduction | (varies) |
| PERCENTAGE | POSITION7 | Percentage for PRE/POST type deductions | (blank or value) |
| LOAN_NUMBER | POSITION8 | Loan number (LOAN type only) | (blank or value) |
| POSITION9–10 | POSITION9–10 | Reserved / additional fields | (varies) |
| STATUS | POSITION11 | C = Cancel/End-date, blank = Active/New | (blank) |

Key point:** POSITION4 (Deduction Type) is the most important field after SSN and Date. It controls the formula's branching logic — which LINEREPEATNO passes execute, which input values get loaded (Amount, Period Type, Percentage, Loan Number, Total Owed, Deduction Amount), and even whether the formula generates output on certain passes. A LOAN type deduction goes through 7 passes. A regular deduction goes through fewer.

How One Vendor Row Becomes Multiple Input Values

A single vendor row carries multiple amounts for the same deduction. The formula uses LINEREPEATNO to load each input value in a separate pass. For a LOAN type deduction, one source row generates up to 7 output rows:

```text
/* One vendor row: */
123-45-6789,2024-01-15,DENTAL01,LOAN,150.00,Monthly,5.5,LN-001,,,,

/* Formula generates (up to 7 passes): */
Pass 1 (LINEREPEATNO=1): ElementEntry header
Pass 2 (LINEREPEATNO=2): ElementEntryValue → Amount = 150.00
Pass 3 (LINEREPEATNO=3): ElementEntryValue → Period Type = Monthly
Pass 4 (LINEREPEATNO=4): ElementEntryValue → Loan Number = LN-001
Pass 5 (LINEREPEATNO=5): ElementEntryValue → Total Owed = ...
Pass 6 (LINEREPEATNO=6): ElementEntryValue → Percentage = 5.5
Pass 7 (LINEREPEATNO=7): ElementEntryValue → Deduction Amount = ...
```

Not every deduction type needs all 7 passes. The formula checks POSITION4 on each pass — if the type doesn't apply (e.g. Percentage only runs for PRE/POST types), it returns `LINEREPEAT = 'Y'` with no output, effectively skipping that pass.

Understanding MultipleEntryCount

Oracle HCM draws a fundamental distinction between **recurring** and **non-recurring** elements when it comes to MultipleEntryCount:

Monthly salary, standing allowance

MultipleEntryCount is **not required** as a key when using SourceSystemId.

*"You don't need to supply the MultipleEntryCount attribute as source keys to uniquely identify the records."* — Oracle Docs

Benefits deductions (our vendor elements)

MultipleEntryCount **must be incremented** for each entry of the same assignment + element within the same payroll period.

*"You must increment the value of MultipleEntryCount for each entry of the same assignment and element."* — Oracle Docs

The vendor interface loads **non-recurring elements that allow multiple entries**. This means the formula must query the cloud for the current highest MultipleEntryCount before assigning the next one — and track assigned values across rows within the same batch using WSA.

**Key Takeaway:** Three benefit plan rows (Dental, Medical, Vision) for the same employee map to three **different elements**, so they each get independent entries with their own MultipleEntryCount. MultipleEntryCount is needed when the **same non-recurring element** requires **multiple entries** for the **same assignment within the same payroll period**.

---

The vendor file gives us an **SSN** and an **Vendor Deduction Code**. Oracle HCM needs an **Assignment Number** and an **Oracle Element Name**. These are completely different identifiers in completely different systems. Value Sets act as the bridge — SQL-backed lookup functions that run inside the Fast Formula engine.

VENDOR ENVIRONMENT

SSN: 123-45-6789

Code: DENTAL01

VALUE SETS

→

ORACLE WORLD

Asg#: E12345

Element: Dental EE Deduction

The formula uses 11 value sets. Here's what each one does:

| # | Value Set | What It Does | Returns |
| --- | --- | --- | --- |
| 1 | XXVA_DEDUCTION_CODES | Maps vendor plan code (DENTAL01) to Oracle Element Name | Element Name |
| 2 | XXVA_DEDUCTION_CODES_INPUT | Gets Input Value Name for the element (e.g. Amount) | Input Value Name |
| 3 | XXVA_GET_LATEST_ASSIGNMENT_NUMBER | Resolves SSN + date → Assignment Number | Assignment# (E12345) |
| 4 | XXVA_GET_PERSON_NUMBER | Resolves SSN → Person Number | Person# (100045) |
| 5 | MAX_MULTI_ENTRY_COUNT | Gets highest existing MultipleEntryCount for Person+Element+Date | Max count (or NULL) |
| 6–7 | GET_ELEMENT_ENTRY_SOURCE_SYSTEM_ID / _OWNER | Retrieves existing SourceSystemId/Owner for MERGE key reuse | Existing SSID/SSO |
| 8–9 | GET_ELEMENT_ENTRY_VALUE_SOURCE_SYSTEM_ID / _OWNER | Same but at Element Entry Value level | ElementEntryValue-level SSID/SSO |
| 10 | GET_ELEMENT_ENTRY_START_DATE | For Cancel rows — gets original start date | Original start date |
| 11 | GET_ELEMENT_ENTRY_INPUT_START_DATE | Same but at ElementEntryValue level (date-tracked scenarios) | ElementEntryValue original start date |

Translate vendor codes → Oracle element names. Called once per row regardless. No caching benefit.

Resolve SSN/Person data. Same SSN appears across multiple rows — **WSA caching saves significant performance here.**

---

```text
INPUTS ARE OPERATION (TEXT),
LINEREPEATNO (NUMBER),
LINENO (NUMBER),
POSITION1 (TEXT), POSITION2 (TEXT), POSITION3 (TEXT),
POSITION4 (TEXT), POSITION5 (TEXT), POSITION6 (TEXT),
POSITION7 (TEXT), POSITION8 (TEXT),
POSITION9 (TEXT), POSITION10 (TEXT), POSITION11 (TEXT)

DEFAULT FOR LINENO IS 1
DEFAULT FOR LINEREPEATNO IS 1
DEFAULT FOR POSITION1 IS 'NO DATA'
DEFAULT FOR POSITION2 IS 'NO DATA'
/* ... same for POSITION3 through POSITION11 ... */
```

| Variable | What It Does |
| --- | --- |
| OPERATION | The HDL engine calls the formula multiple times with different values: FILETYPE, DELIMITER, READ, NUMBEROFBUSINESSOBJECTS, METADATALINEINFORMATION, then MAP per row. The formula is a router. |
| LINEREPEATNO | The repeat counter. When formula sets `LINEREPEAT = 'Y'`, HDL re-invokes for the same row with incremented LINEREPEATNO. One input row can generate up to 7 HDL output rows: 1 ElementEntry header (pass 1) + up to 6 ElementEntryValue rows (passes 2–7), one per input value (Amount, Period Type, Loan Number, Total Owed, Percentage, Deduction Amount). The deduction type (POSITION4) controls how many passes run. |
| LINENO | Line number from the source file (1-based). Useful for error tracing. |
| POSITION1–11 | Map directly to CSV columns in order. HDL engine splits each line by delimiter and populates these. |

**Why DEFAULT FOR is required:** When HDL calls the formula for non-MAP operations (like FILETYPE), the POSITION variables aren't populated — no source row is being processed. Without defaults, the formula throws a null reference error at runtime.

---

| Input | HDL engine asks: "What file type? What delimiter? How many objects?" |
| --- | --- |
| Formula returns | DELIMITED, comma, NONE, 2 |
| HDL output | Nothing written to .dat yet — engine is just being configured |

```text
IF OPERATION = 'FILETYPE' THEN
    OUTPUTVALUE = 'DELIMITED'
ELSE IF OPERATION = 'DELIMITER' THEN
    OUTPUTVALUE = ','
ELSE IF OPERATION = 'READ' THEN
    OUTPUTVALUE = 'NONE'
ELSE IF OPERATION = 'NUMBEROFBUSINESSOBJECTS' THEN
(
    OUTPUTVALUE = '2'
    RETURN OUTPUTVALUE
)
```

FILETYPE**DELIMITED

DELIMITER
,

READ
NONE

OBJECTS
2

METADATA

MAP
(per row)

| Operation | Engine Asks | Our Answer | Why |
| --- | --- | --- | --- |
| FILETYPE | "What kind of file?" | DELIMITED | Only valid option for HDL transformation |
| DELIMITER | "What separates values?" | , | the vendor sends CSV. Default is pipe (\|), so we override. |
| READ | "Skip header rows?" | NONE | vendor file has no header row — process every line. |
| NUMBEROF... | "How many HDL objects?" | 2 | ElementEntry (header) + ElementEntryValue (detail with amount) |

---

| Input | HDL engine asks: "What columns does each object have?" |
| --- | --- |
| Formula returns | METADATA1[ ] array, METADATA2[ ] array |
| HDL writes to .dat | METADATA\|ElementEntry\|LegislativeDataGroupName\|EffectiveStartDate\|...METADATA\|ElementEntryValue\|LegislativeDataGroupName\|EffectiveStartDate\|... |

After the setup handshake, the HDL engine calls the formula with `OPERATION = 'METADATALINEINFORMATION'`. This is where the formula defines the column headers** for the .dat output file. These become the METADATA rows you see at the top of each block in the .dat file.

The .dat File Has Two METADATA Header Rows

Since we told the engine `NUMBEROFBUSINESSOBJECTS = 2` (ElementEntry + ElementEntryValue), the formula must define two METADATA arrays — one per object. These become the two header rows in the .dat file:

```text
/* This header row in the .dat file: */
METADATA|ElementEntry|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|CreatorType|EffectiveEndDate|EntryType|MultipleEntryCount

/* Is generated by this code: */
```

The Code — METADATA1 (ElementEntry Header)

The formula uses an **array variable** called `METADATA1`. Each array position maps to a column in the .dat header. Positions [1] and [2] are reserved by the HDL engine for FileName and FileDiscriminator — the formula starts filling from position [3].

```text
ELSE IF OPERATION = 'METADATALINEINFORMATION' THEN
(
    /* ================================================= */
    /* METADATA1 — ElementEntry column definitions        */
    /* [1] = FileName (auto-filled by HDL engine)         */
    /* [2] = FileDiscriminator (auto-filled by HDL engine)*/
    /* [3] onwards = we define                            */
    /* ================================================= */

    METADATA1[3]  = 'LegislativeDataGroupName'
    METADATA1[4]  = 'EffectiveStartDate'
    METADATA1[5]  = 'ElementName'
    METADATA1[6]  = 'AssignmentNumber'
    METADATA1[7]  = 'CreatorType'
    METADATA1[8]  = 'EffectiveEndDate'
    METADATA1[9]  = 'EntryType'
    METADATA1[10] = 'MultipleEntryCount'
    METADATA1[11] = 'SourceSystemOwner'
    METADATA1[12] = 'SourceSystemId'
    METADATA1[13] = 'ReplaceLastEffectiveEndDate'
```

The HDL engine reads this array and writes the following row to the .dat file:

```text
METADATA|ElementEntry|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|CreatorType|EffectiveEndDate|EntryType|MultipleEntryCount|SourceSystemOwner|SourceSystemId|ReplaceLastEffectiveEndDate
```

The Code — METADATA2 (ElementEntryValue Header)

Same pattern. `METADATA2` array defines the columns for the ElementEntryValue block:

```text
    /* ================================================= */
    /* METADATA2 — ElementEntryValue column definitions   */
    /* ================================================= */

    METADATA2[3]  = 'LegislativeDataGroupName'
    METADATA2[4]  = 'EffectiveStartDate'
    METADATA2[5]  = 'ElementName'
    METADATA2[6]  = 'AssignmentNumber'
    METADATA2[7]  = 'InputValueName'              /* ← changes per pass */
    METADATA2[8]  = 'EffectiveEndDate'
    METADATA2[9]  = 'EntryType'
    METADATA2[10] = 'MultipleEntryCount'
    METADATA2[11] = 'ScreenEntryValue'            /* ← the actual value */
    METADATA2[12] = '"ElementEntryId(SourceSystemId)"'  /* parent link */
    METADATA2[13] = 'SourceSystemOwner'
    METADATA2[14] = 'SourceSystemId'
    METADATA2[15] = 'ReplaceLastEffectiveEndDate'

    RETURN METADATA1, METADATA2
)
```

This generates the second header row in the .dat file:

```text
METADATA|ElementEntryValue|LegislativeDataGroupName|EffectiveStartDate|ElementName|AssignmentNumber|InputValueName|EffectiveEndDate|EntryType|MultipleEntryCount|ScreenEntryValue|ElementEntryId(SSID)|SourceSystemOwner|SourceSystemId|ReplaceLastEffectiveEndDate
```

How METADATA Links to RETURN in Sections 7 and 8

The column names in the METADATA arrays directly map to the **named output variables** in the formula's RETURN statement. Here's the connection:

```text
/* METADATA defines the column header: */
METADATA1[5] = 'ElementName'

/* In the MAP block, the formula assigns the named variable: */
ElementName  = l_ElementName              /* = 'Dental EE Deduction' */

/* And includes it in the RETURN: */
RETURN ..., ElementName, ...

/* Result in .dat file:                                                */
/* METADATA |ElementEntry|...|ElementName                    |...      */
/* MERGE    |ElementEntry|...|Dental EE Deduction   |...      */
/*                             ↑ matched by variable name             */
```

**The mapping rule:**

`METADATA1[N]` defines column N header name for object 1 (ElementEntry)**
In the MAP block, you assign a variable with that exact same name** and include it in the RETURN statement**

The HDL engine matches the RETURN variable name to the METADATA column name and writes the value into the correct position in the .dat file. The `FileDiscriminator` value (`'ElementEntry'` vs `'ElementEntryValue'`) tells the engine which METADATA block to use.

---

The reference vendor row used in all examples below:

Vendor Input Row

| POSITION1 | SSN | 123-45-6789 |
| --- | --- | --- |
| POSITION2 | Effective Date | 2024-01-15 |
| POSITION3 | Benefit Plan | DENTAL01 |
| POSITION4 | Deduction Type | PRE |
| POSITION5 | Amount | 150.00 |
| POSITION6 | Period Type | Monthly |
| POSITION7 | Percentage | 5.5 |
| POSITION8 | Loan Number | LN-001 |
| POSITION11 | Status | (blank = Active) |

This is the heart of the formula. When the HDL engine reaches a source row, it calls `OPERATION = 'MAP'`. The formula receives the raw CSV data in POSITION1–11 and must return Oracle HDL attributes. Five steps run in sequence.

Here's what the formula needs to figure out for each row:

| Question | Vendor Gives Us | Oracle Needs | Step |
| --- | --- | --- | --- |
| What type of deduction? | POSITION4 (Deduction Type) | PRE / POST / LOAN / CU | Step 1 |
| Which Oracle Element? | DENTAL01 | Dental EE Deduction | Step 2 |
| Which employee? | 123-45-6789 (SSN) | E12345 (Assignment#) | Step 3 |
| How many entries already exist? | (doesn't know) | MultipleEntryCount = 2 | Step 4 |
| New or existing entry? | (doesn't know) | SourceSystemId for MERGE | Step 5 |

STEP 1
Element Type

STEP 2
Element Lookup

STEP 3
Person / Assignment

STEP 4
MultipleEntryCount

STEP 5
SourceSystemId

Step 1: Read Input Values from POSITION Fields

| POSITION4 = PRE | → l_DeductionType = 'PRE' |
| --- | --- |
| POSITION5 = 150.00 | → l_Amount = '150.00' |
| POSITION6 = Monthly | → l_PeriodType = 'Monthly' |
| POSITION7 = 5.5 | → l_Percentage = '5.5' |
| POSITION8 = LN-001 | → l_LoanNumber = 'LN-001' |

The formula reads the deduction type from POSITION4 and the amount from POSITION5. It also captures other input values (Period Type, Percentage, Loan Number) from their respective positions for later LINEREPEATNO passes:

```text
/* Read the key fields from the vendor row */
l_DeductionType    = TRIM(POSITION4)     /* 'PRE', 'POST', 'LOAN', 'CU' */
l_Amount           = TRIM(POSITION5)     /* '150.00' */
l_PeriodType       = TRIM(POSITION6)     /* 'Monthly' */
l_Percentage       = TRIM(POSITION7)     /* '5.5' (PRE/POST only) */
l_LoanNumber       = TRIM(POSITION8)     /* 'LN-001' (LOAN only) */
```

After this step: `l_DeductionType = 'PRE'` and `l_Amount = '150.00'`

Step 2: Resolve Element Name from Benefit Plan Code

| POSITION3 = DENTAL01 | → Value Set lookup |
| --- | --- |
|  | → l_ElementName = 'Dental EE Deduction' |
|  | → l_InputValueName = 'Amount' |

The vendor uses its own benefit plan codes (DENTAL01, MEDICAL01, VISION01). Oracle doesn't know these codes. The formula passes the vendor code to two value sets that translate it into Oracle terms:

```text
/* Step 2: Translate vendor plan code → Oracle Element Name */

L_VendorPayCode = TRIM(POSITION3)
/* e.g. 'DENTAL01' */

/* Value set 1: vendor code → Oracle Element Name */
l_ElementName = GET_VALUE_SET('XXVA_DEDUCTION_CODES',
    '|=P_PAY_CODE=''' || L_VendorPayCode || '''')
/* 'DENTAL01' → 'Dental EE Deduction' */

/* Value set 2: vendor code → Input Value Name */
l_InputValueName = INITCAP(GET_VALUE_SET('XXVA_DEDUCTION_CODES_INPUT',
    '|=P_PAY_CODE=''' || L_VendorPayCode || ''''))
/* 'DENTAL01' → 'Amount' */
```

These are code-based** lookups — the value set definition maps each vendor code to its Oracle element. No person data is involved, so no WSA caching is needed here.

Value Set Translation

| Vendor Code (POSITION3) | Oracle Element Name | Input Value Name |
| --- | --- | --- |
| DENTAL01 | Dental EE Deduction | Amount |
| MEDICAL01 | Medical EE Deduction | Amount |
| VISION01 | Vision EE Deduction | Amount |

This mapping is defined in the value set configuration — not in the formula code. Adding a new benefit plan just means adding a row to the value set.

After Step 2: `l_ElementName = 'Dental EE Deduction'` and `l_InputValueName = 'Amount'`

Step 3: Resolve Person & Assignment

| POSITION1 = 123-45-6789 | → GET_VALUE_SET → L_PersonNumber = '100045' |
| --- | --- |
| POSITION2 = 2024-01-15 | → GET_VALUE_SET → l_AssignmentNumber = 'E12345' |

Oracle HDL doesn't understand SSN. It needs two things: **Person Number** and **Assignment Number**. Step 3 translates one into the other.

VENDOR FILE GIVES US

123-45-6789

SSN (POSITION1)

→

Value Set**calls DB

ORACLE HDL NEEDS

Person# 100045

Assignment# E12345

Two value sets do this translation:

| XXVA_GET_PERSON_NUMBER | Takes SSN + Date → returns Person Number (100045) |
| --- | --- |
| XXVA_GET_LATEST_ASSIGNMENT_NUMBER | Takes SSN + Date → returns Assignment Number (E12345) |

That's the simple version. But there's a performance problem.

The Problem: Same SSN, Three Rows, Three Identical DB Calls

One employee can have multiple rows in the vendor file — one per benefit plan. If an employee has 3 benefit plans (Dental, Medical, Vision), the file has 3 rows with the same SSN**. Without optimization, the formula calls the value set 3 times for the exact same SSN and gets the exact same answer 3 times.

Without caching — 3 rows, same SSN

**Row 1 (DENTAL01):** SSN 123-45-6789 → call DB → Person# 100045 [OK]**
Row 2 (MEDICAL01):** SSN 123-45-6789 → call DB again → Person# 100045 ← same SSN, wasted call**
Row 3 (VISION01):** SSN 123-45-6789 → call DB again → Person# 100045 ← same SSN, wasted call

The Fix: Cache with WSA

The formula uses WSA to remember the answer (explained in the WSA Deep Dive after Step 4). The logic is simple:

Did I already look up this SSN?

WSA_EXISTS('PER_123-45-6789_2024-01-15')

YES → Read from cache

WSA_GET('PER_123-45-6789_2024-01-15', ' ')**→ 100045. Done. No DB call.

NO → Call DB, then save to cache

GET_VALUE_SET(...) → 100045
WSA_SET('PER_123-45-6789_2024-01-15', 100045)

With WSA caching — same 3 rows, same SSN

Row 1 (DENTAL01):** WSA_EXISTS? **NO** → call DB → 100045 → WSA_SET (save it) [OK]**
Row 2 (MEDICAL01):** WSA_EXISTS? **YES** → WSA_GET → 100045. Zero DB calls. [OK]**
Row 3 (VISION01):** WSA_EXISTS? **YES** → WSA_GET → 100045. Zero DB calls. [OK]

Here's what the actual code looks like:

```text
/* Build a unique WSA key from SSN + Date */
/* e.g. 'PER_123-45-6789_2024-01-15' */

IF WSA_EXISTS('PER_' || POSITION1 || '_' || POSITION2) THEN
(
    /* Cache hit — read stored values */
    L_PersonNumber     = WSA_GET('PER_' || POSITION1 || '_' || POSITION2, ' ')
    l_AssignmentNumber = WSA_GET('ASG_' || POSITION1 || '_' || POSITION2, ' ')
)
ELSE
(
    /* Cache miss — call value sets (hits DB) */
    l_AssignmentNumber = GET_VALUE_SET('XXVA_GET_LATEST_ASSIGNMENT_NUMBER', ...)
    L_PersonNumber     = GET_VALUE_SET('XXVA_GET_PERSON_NUMBER', ...)

    /* Save to WSA — next row with same SSN skips DB */
    WSA_SET('PER_' || POSITION1 || '_' || POSITION2, L_PersonNumber)
    WSA_SET('ASG_' || POSITION1 || '_' || POSITION2, l_AssignmentNumber)
)
```

After Step 3: `L_PersonNumber = '100045'` and `l_AssignmentNumber = 'E12345'`

Step 4: MultipleEntryCount

| Person 100045 + Element Dental EE Deduction + Date 2024-01-15 | → l_MultipleEntryCount = 1 (or 2, 3... if entries already exist) |
| --- | --- |

What Is It?

When the same person has multiple entries of the **same element** in the **same payroll period**, Oracle needs a sequence number to tell them apart. That number is MultipleEntryCount.

When does this happen in the vendor interface? Each pay period, the vendor sends a new deduction file. If person 100045 already has a Dental EE Deduction entry from a previous load, and this batch sends another one (maybe a mid-period adjustment), the new entry needs a higher count.

If you know SQL, it's this:

```text
ROW_NUMBER() OVER (PARTITION BY person, element, payroll_period)  =  MultipleEntryCount
```

Here's what it looks like in `PAY_ELEMENT_ENTRIES_F` after multiple loads:

| Person# | Element | EffectiveStartDate | Amount | MultipleEntryCount | Source |
| --- | --- | --- | --- | --- | --- |
| 100045 | Dental EE Deduction | 2024-01-15 | $150.00 | 1 | January batch |
| 100045 | Dental EE Deduction | 2024-01-20 | $25.00 | 2 | Mid-period adjustment |
| 100045 | Medical EE Deduction | 2024-01-15 | $200.00 | 1 | ← different element, count resets to 1 |

The partition key is **Person + Element + Payroll Period**. Same person + same element = same group, count increments. Different element = new group, count resets to 1. If two entries in the same group get the **same** count, Oracle overwrites the first one — data is lost.

The Problem: Fast Formula Has No Memory

In PL/SQL, you'd do this in a loop. The counter variable lives across iterations:

```text
-- PL/SQL: variable persists across loop iterations
l_counter := 0;
FOR rec IN cursor LOOP
    l_counter := l_counter + 1;
    -- Row 1: l_counter = 1
    -- Row 2: l_counter = 2  ← remembers what happened in Row 1
END LOOP;
```

Fast Formula is **not** a loop. The HDL engine calls the formula once per row as a **separate, independent invocation**. All local variables are destroyed after each call. It's like calling a standalone function 10,000 times — each call starts from zero with no memory of the previous call.

So the formula has to ask the database: *"What's the highest count that already exists?"* The value set runs something like this behind the scenes against `PAY_ELEMENT_ENTRIES_F`:

```text
SELECT MAX(pee.MULTIPLE_ENTRY_COUNT)
FROM   PAY_ELEMENT_ENTRIES_F  pee
      ,PAY_ELEMENT_TYPES_F    pet
      ,PER_ALL_ASSIGNMENTS_M  paam
WHERE  pee.ELEMENT_TYPE_ID  = pet.ELEMENT_TYPE_ID
AND    pee.PERSON_ID         = paam.PERSON_ID
AND    pet.ELEMENT_NAME      = 'Dental EE Deduction'
AND    paam.PERSON_NUMBER    = '100045'
AND    '2024-10-15' BETWEEN pee.EFFECTIVE_START_DATE AND pee.EFFECTIVE_END_DATE
```

This works fine when each batch has only one row per person+element. But what if the batch has two?

The Bug: Two Rows Read the Same Stale MAX

Here's what's already in `PAY_ELEMENT_ENTRIES_F` from last month's load:

| ELEMENT_ENTRY_ID | PERSON_ID | ELEMENT_TYPE_ID | EFFECTIVE_START_DATE | MULTIPLE_ENTRY_COUNT | ENTRY_TYPE |
| --- | --- | --- | --- | --- | --- |
| 300000012345 | 100045 | 50001 (Dental EE Deduction) | 01-Oct-2024 | 1 | E |

Now our vendor batch has two new Dental EE Deduction rows for the same person. The formula runs `SELECT MAX(MULTIPLE_ENTRY_COUNT)` for each — but the problem is Row 5's INSERT hasn't reached the table yet when Row 8 queries it:

Row 5 processes — formula queries the table:

```text
SELECT MAX(MULTIPLE_ENTRY_COUNT) FROM PAY_ELEMENT_ENTRIES_F
WHERE PERSON_ID = 100045 AND ELEMENT_TYPE_ID = 50001  → Returns 1
```

Formula assigns: 1 + 1 = 2   ← this row is still in the HDL batch, NOT yet inserted into PAY_ELEMENT_ENTRIES_F

Row 8 processes — formula queries the SAME table:

```text
SELECT MAX(MULTIPLE_ENTRY_COUNT) FROM PAY_ELEMENT_ENTRIES_F
WHERE PERSON_ID = 100045 AND ELEMENT_TYPE_ID = 50001  → STILL returns 1!
```

Formula assigns: 1 + 1 = 2   ← SAME count as Row 5!

What the generated .dat file looks like — both rows got the same count:

ElementEntry.dat — FAIL output

Existing entry (already in Oracle):

| ElementName | Dental EE Deduction |
| --- | --- |
| MultipleEntryCount | 1 |

Row 5 output ($175.00):

| ElementName | Dental EE Deduction |
| --- | --- |
| MultipleEntryCount | 2 |

Row 8 output ($200.00) — SAME count!

__DARK_0__

**BUG:** Two rows in the .dat file with MultipleEntryCount = 2. When Oracle loads this file, Row 8 overwrites Row 5. $175.00 entry is lost.

The Fix: WSA Tracks What the Table Can't See Yet

WSA acts as an in-memory counter that survives between formula calls. Row 5 saves its assigned count to WSA. When Row 8 runs, it reads from WSA instead of querying the table:

| Row | WSA has data? | Source of MAX | Assigns | Saves to WSA |
| --- | --- | --- | --- | --- |
| Row 5 | NO | PAY_ELEMENT_ENTRIES_F → MAX = 1 | 2 | WSA_SET(2) |
| Row 8 | YES → 2 | WSA memory (skips table) | 3 | WSA_SET(3) |

What the .dat file looks like — each row gets a unique count:

ElementEntry.dat — PASS output

Existing entry (already in Oracle):

| ElementName | Dental EE Deduction |
| --- | --- |
| MultipleEntryCount | 1 |

Row 5 output ($175.00):

| ElementName | Dental EE Deduction |
| --- | --- |
| MultipleEntryCount | 2 [OK] |

Row 8 output ($200.00):

__DARK_1__

PASS Three unique MultipleEntryCount values (1, 2, 3) in the .dat file. Oracle loads all three entries successfully.

The Fast Formula Code

```text
/* Check: did a previous row already assign a count for this combo? */
IF WSA_EXISTS('MEC_' || L_PersonNumber || '_' || l_ElementName || '_' || POSITION2) THEN
(
    /* YES — read last assigned count and add 1 */
    l_MultipleEntryCount = WSA_GET('MEC_' || ..., 0) + 1
)
ELSE
(
    /* NO — first row for this combo. Ask the database. */
    l_db_max = GET_VALUE_SET('MAX_MULTI_ENTRY_COUNT', ...)

    IF ISNULL(l_db_max) = 'N' THEN
        l_MultipleEntryCount = 1              /* Nothing in cloud → start at 1 */
    ELSE
        l_MultipleEntryCount = l_db_max + 1  /* Cloud has 1 → assign 2 */
)

/* Save what we assigned — next row reads this instead of hitting DB */
WSA_SET('MEC_' || L_PersonNumber || '_' || l_ElementName || '_' || POSITION2, l_MultipleEntryCount)
```

**Summary in one line:** WSA is a working storage area that persists across formula invocations — like a PL/SQL package variable. The formula writes the assigned count to WSA, so the next row with the same combo reads from memory instead of hitting a stale database. The formula writes the assigned count to WSA, so the next row with the same combo reads from memory instead of hitting a stale database.

After Step 4: `l_MultipleEntryCount = 2` (cloud had 1, so we assigned 1 + 1)

WSA in This Formula — Connecting Step 3 and Step 4

You've now seen WSA used twice in the MAP block, but for **two completely different reasons**. Let's connect them before moving to Step 5.

| Step | WSA Key | What It Stores | Why | What Breaks Without It |
| --- | --- | --- | --- | --- |
| Step 3 | PER_<SSN>_<Date>**ASG_<SSN>_<Date> | Person NumberAssignment Number | Performance | Same SSN queried 3x instead of 1x. Slow but correct. |
| Step 4 | MEC_<Person>_<Element>_<Date> | Last assigned MultipleEntryCount | Correctness | Duplicate MULTIPLE_ENTRY_COUNT in PAY_ELEMENT_ENTRIES_F. Data lost. |

This is the key distinction:

Removes WSA from Step 3 → formula still works correctly**

It just runs **slower** (3 DB calls instead of 1 per SSN group)

Remove WSA from Step 4 → formula **produces wrong output**

Duplicate counts → rows overwrite each other in PAY_ELEMENT_ENTRIES_F

Both use the same WSA methods (`WSA_EXISTS`, `WSA_GET`, `WSA_SET`), same pattern (check → hit or miss → store), but different purposes. Step 3 is optional optimization. Step 4 is mandatory for data integrity.

---

You've now seen WSA used in Step 3 and Step 4. Let's go deeper into how it works, what this formula caches, and one critical deployment rule you can't skip.

What Is WSA?

WSA (Working Storage Area) is, per Oracle documentation, **a mechanism for storing global values across formulas**. Local variables die after each formula invocation, but WSA values persist across calls within the same session. You write a value on Row 1, and you can read it back on Row 500. WSA names are **case-independent** — `'PER_123'` and `'per_123'` refer to the same item.

In PL/SQL terms: WSA is a package-level associative array (`TABLE OF VARCHAR2 INDEX BY VARCHAR2`). It persists across function calls within the same session.

The API — Four Methods

| Method | PL/SQL Equivalent | What It Does |
| --- | --- | --- |
| WSA_EXISTS(item [, type]) | g_cache.EXISTS(key) | Tests whether item exists in the storage area. Optional `type` parameter restricts to a specific data type (TEXT, NUMBER, DATE, TEXT_TEXT, TEXT_NUMBER, etc.) |
| WSA_GET(item, default-value) | l_val := g_cache(key) | Retrieves the stored value. If item doesn't exist, returns the **default-value** instead. The data type of default-value determines the expected data type. |
| WSA_SET(item, value) | g_cache(key) := val | Sets the value for item. Any existing item of the same name is **overwritten**. |
| WSA_DELETE([item]) | g_cache.DELETE(key) | Deletes item from storage. If no name specified, **all storage area data is deleted**. Not used in this vendor formula, but important for cleanup scenarios. |

**Key detail from Oracle docs:** `WSA_GET` always requires a **default-value** parameter. The formula always calls `WSA_EXISTS` first and only calls `WSA_GET` when the item is known to exist — so the default is never actually used, but it must still be provided. The data type of the default tells the engine what data type to expect.

Every WSA usage in this formula follows the same pattern. You already saw it twice:

```text
/* THE PATTERN — same in Step 3, Step 4, and everywhere else */

IF WSA_EXISTS(l_key) THEN            /* 1. Check memory */
    l_value = WSA_GET(l_key, ' ')    /* 2a. HIT  — read from memory (default never used) */
ELSE
    l_value = GET_VALUE_SET(...)      /* 2b. MISS — call the database */
    WSA_SET(l_key, l_value)          /* 3.  SAVE — store for next row */
```

Where You Already Saw This Pattern

| Key: | 'PER_123-45-6789_2024-01-15' |
| --- | --- |
| Stores: | Person Number (100045) |
| DB call saved: | GET_VALUE_SET('XXVA_GET_PERSON_NUMBER') |
| Purpose: | Performance — same SSN in 3 rows, only 1 DB call |

| Key: | 'MEC_100045_Dental EE Deduction_2024-01-15' |
| --- | --- |
| Stores: | Last assigned count (2, then 3, then 4...) |
| DB call saved: | GET_VALUE_SET('MAX_MULTI_ENTRY_COUNT') |
| Purpose: | Correctness — prevents duplicate MULTIPLE_ENTRY_COUNT |

All WSA Keys This Formula Uses

Steps 3 and 4 are the two main ones, but the formula caches more. Here's the complete list:

| WSA Key | Stores | Used In | Type |
| --- | --- | --- | --- |
| PER_<SSN>_<Date> | Person Number | Step 3 | Performance |
| ASG_<SSN>_<Date> | Assignment Number | Step 3 | Performance |
| MEC_<Person>_<Element>_<Date> | Last assigned MultipleEntryCount | Step 4 | Correctness |
| SSID_, SSO_, EEVID_, EEVO_ | SourceSystemId/Owner lookups | Step 5 | Performance |
| HDR_<Person>_<Element>_<Date> | Flag: ElementEntry header already generated | Section 7 | Correctness |

**Pattern:** Performance keys (PER_, ASG_, SSID_) can be removed and the formula still works — just slower. Correctness keys (MEC_, HDR_) cannot be removed — the formula produces wrong data without them.

Traced Example: 3 Benefit Plan Rows, Same Employee

Watch Step 3 and Step 4 WSA caching in action across three rows for SSN 123-45-6789:

Vendor Input File — 3 rows for the same employee (SSN 123-45-6789)

| Row | POS1 (SSN) | POS2 (Date) | POS3 (Plan) | POS4 (Type) | POS5 (Amt) |
| --- | --- | --- | --- | --- | --- |
| Row 1 | 123-45-6789 | 2024-01-15 | DENTAL01 | PRE | 150.00 |
| Row 2 | 123-45-6789 | 2024-01-15 | MEDICAL01 | PRE | 75.50 |
| Row 3 | 123-45-6789 | 2024-01-15 | VISION01 | PRE | 12.30 |

Same SSN, same date — but **different benefit plans**. This is typical: one employee enrolled in Dental + Medical + Vision.

Now let's trace what happens when the formula processes each row:

STEP 3
Person & Assignment Lookup

| WSA Check | WSA_EXISTS('PER_123-45-6789_2024-01-15') | MISS |
| --- | --- | --- |
| Action | Call DB → Person# = **100045**, Asg# = **E12345** |
| WSA Save | WSA_SET('PER_...', 100045)   WSA_SET('ASG_...', E12345) |

STEP 4
MultipleEntryCount

| WSA Check | WSA_EXISTS('MEC_100045_Dental EE Deduction_2024') | MISS |
| --- | --- | --- |
| Action | Call DB → MAX = NULL (no existing entry) |
| Result | MultipleEntryCount = 1   → WSA_SET('MEC_...Dental...', 1) |

DB calls: **11** — all cache misses (first time seeing this SSN)

STEP 3
Person & Assignment Lookup

| WSA Check | WSA_EXISTS('PER_123-45-6789_2024-01-15') | HIT! |
| --- | --- | --- |
| Action | WSA_GET → Person# 100045, Asg# E12345 — zero DB calls |

STEP 4
MultipleEntryCount
— different element name = new WSA key

| WSA Check | WSA_EXISTS('MEC_100045_**Medical** EE Deduction_2024') | MISS |
| --- | --- | --- |
| Action | Call DB → MAX = NULL |
| Result | MultipleEntryCount = 1   → WSA_SET('MEC_...Medical...', 1) |

DB calls: **4** — Step 3 saved 2 calls (cache hit), Step 4 missed (different element)

STEP 3
Person & Assignment Lookup

| WSA Check | WSA_EXISTS('PER_123-45-6789_2024-01-15') | HIT! |
| --- | --- | --- |
| Action | WSA_GET → Person# 100045, Asg# E12345 — zero DB calls |

STEP 4
MultipleEntryCount
— yet another element = yet another WSA key

| WSA Check | WSA_EXISTS('MEC_100045_**Vision** EE Deduction_2024') | MISS |
| --- | --- | --- |
| Action | Call DB → MAX = NULL |
| Result | MultipleEntryCount = 1 |

DB calls: **4** — same pattern as Row 2

The Pattern:

|  | Step 3 (Person lookup) | Step 4 (MEC) |
| --- | --- | --- |
| Row 1 | MISS — call DB | MISS — call DB |
| Row 2 | HIT — zero DB calls | MISS — different element |
| Row 3 | HIT — zero DB calls | MISS — different element |

Step 3 always hits after Row 1 (same SSN = same key). Step 4 always misses here because each row maps to a different element. Step 4 WSA becomes critical when the batch has multiple rows for the **same person + same element**.

Performance at Scale

For 10,000 vendor rows where employees average 3 benefit plans each:

value set calls (10K × 11 per row)

63% reduction — Step 3 caching saves ~7 calls per duplicate SSN

Critical Rule: Set Threads = 1

There's one deployment rule for WSA that you absolutely cannot skip:

If "Load Data from File" runs with 4 threads, each thread gets its **own independent WSA**:

| Step 3 breaks: | Thread 1 caches Person# for SSN 123. Thread 2 gets a different row for the same SSN — but Thread 2's WSA is empty. It calls the value set again. (Wastes performance, but data is still correct.) |
| --- | --- |
| Step 4 breaks: | Thread 1 assigns MultipleEntryCount = 2 and saves to its WSA. Thread 2 gets another row for the same person+element — but Thread 2's WSA is empty. It queries the DB, gets MAX = 1, assigns count = 2. **Duplicate. Data lost.** |

**The fix:**

My Client Groups
→
Payroll
→
Payroll Process Configuration
→
Threads = 1

Set thread count to 1 before running "Load Data from File." All rows process sequentially in one thread. WSA works as a true shared cache across every row.

---

Step 5: SourceSystemId Resolution

| All resolved values from Steps 1–4 | → l_SourceSystemId = 'HDL_XXVA_E12345_EE_100045_Dental EE Deduction_20240115' |
| --- | --- |

Oracle HDL uses SourceSystemId as the MERGE key. If an entry already exists in cloud, the formula reuses its SourceSystemId (so HDL updates it). If not, it constructs one:

```text
/* For active employees — construct using PersonNumber */
'HDL_XXVA' || l_AssignmentNumber || '_EE_' || L_PersonNumber || '_' || l_ElementName || '_' || POSITION2

/* For terminated employees (PersonNumber unavailable) — use SSN */
'HDL_XXVA' || l_AssignmentNumber || '_EE_' || POSITION1 || '_' || l_ElementName || '_' || POSITION2
```

After all five steps, the formula has everything it needs: Element Name, Assignment Number, Person Number, MultipleEntryCount, SourceSystemId, and the dollar amount. Now it generates the HDL output rows (Sections 7 and 8).

---

Vendor Input (what the formula receives):

| POSITION1 | SSN | 123-45-6789 |
| --- | --- | --- |
| POSITION2 | Date | 2024-01-15 |
| POSITION3 | Plan Code | DENTAL01 |
| POSITION4 | Ded Type | PRE |
| POSITION5 | Amount | 150.00 |
| POSITION11 | Status | (blank = Active) |

### ↓ Formula transforms (Steps 1–5 + LINEREPEATNO=1) ↓

HDL .dat Output (ElementEntry):

| BusinessOperation | MERGE |
| --- | --- |
| FileDiscriminator | ElementEntry |
| LegislativeDataGroupName | 570 |
| EffectiveStartDate | 2024/01/15 |
| ElementName | Dental EE Deduction |
| AssignmentNumber | E12345 |
| CreatorType | H |
| EntryType | E |
| MultipleEntryCount | 1 |
| SourceSystemOwner | HDL_XXVA |
| SourceSystemId | HDL_XXVA_E12345_EE_... |

After the five MAP steps, the formula has all the values it needs. Now it generates the actual HDL output. Each vendor source row produces **multiple** HDL output rows — one ElementEntry header on pass 1, followed by one ElementEntryValue per input value on passes 2 through 7. LINEREPEATNO controls which one gets generated on each pass.

How LINEREPEAT Works

The HDL engine calls the formula once per source row with `LINEREPEATNO = 1`. If the formula returns `LINEREPEAT = 'Y'`, the engine calls the formula **again for the same row** — this time with `LINEREPEATNO = 2`.

```text
/* HDL engine processes one vendor source row: */

/* Pass 1: LINEREPEATNO = 1 → ElementEntry header */
Formula outputs →  MERGE|ElementEntry|...|Dental EE Deduction|...
Formula returns →  LINEREPEAT = 'Y'   ← call me again

/* Pass 2: LINEREPEATNO = 2 → EEV: Amount = 150.00 */
Formula outputs →  MERGE|ElementEntryValue|...|Amount|...|150.00
Formula returns →  LINEREPEAT = 'Y'   ← call me again (more input values)

/* Pass 3: LINEREPEATNO = 3 → EEV: Period Type = Monthly */
Formula outputs →  MERGE|ElementEntryValue|...|Period Type|...|Monthly
Formula returns →  LINEREPEAT = 'Y'   ← call me again

/* ... passes 4–6 for Loan Number, Total Owed, Percentage (if applicable) ... */

/* Pass 7: LINEREPEATNO = 7 → EEV: Deduction Amount (last pass) */
Formula outputs →  MERGE|ElementEntryValue|...|Deduction Amount|...
Formula returns →  LINEREPEAT = 'N'   ← done, move to next source row
```

One source row → multiple output rows (1 ElementEntry + up to 6 ElementEntryValues). The HDL engine groups all ElementEntry rows together and all ElementEntryValue rows together in the final `.dat` file, separated by their METADATA header rows.

The .dat Output Structure

The final .dat file has two blocks. Each block starts with a METADATA row that defines the columns, followed by the MERGE data rows:

Block 1 — ElementEntryValue (generated by LINEREPEATNO = 2–7)

```text
A         B                C    D           E                  F               G               J                  K
METADATA  ElementEntryVal  LDG  EffStart    ElementName        AssignmentNum   InputValueName  MultipleEntryCount ScreenEntryValue
MERGE     ElementEntryVal  570  22-09-2019  Dental EE Deduct   123141402543    Amount          3                  150.00
MERGE     ElementEntryVal  222  22-09-2019  Dental EE Deduct   123141402554    Amount          6                  25.72
MERGE     ElementEntryVal  570  22-09-2019  Dental EE Deduct   123141402543    Amount          1                  150.00
...       more rows
```

Block 2 — ElementEntry (generated by LINEREPEATNO = 1)

```text
A         B             C    D           E                  F               G           I          J
METADATA  ElementEntry  LDG  EffStart    ElementName        AssignmentNum   CreatorType EntryType  MultipleEntryCount
MERGE     ElementEntry  570  22-09-2019  Dental EE Deduct   123141402543    H           E          3
MERGE     ElementEntry  222  22-09-2019  Dental EE Deduct   123141402554    H           E          6
...       more rows
```

The key columns to notice: ElementEntry has **CreatorType** and **EntryType** but no dollar amount. ElementEntryValue has **InputValueName** (always "Amount") and **ScreenEntryValue** (the actual dollar amount like 150.00). Both carry **MultipleEntryCount** from Step 4.

What LINEREPEATNO = 1 Generates

On the first pass, the formula checks POSITION11 (the STATUS column from the vendor file). This decides whether we're creating a new entry or end-dating an existing one:

| POSITION11 | ElementEntry row generated | LINEREPEAT |
| --- | --- | --- |
| Blank (Active) | `MERGE\|ElementEntry\|570\|22-09-2019\|Dental EE Deduction\|123141402543\|H\|\|E\|1`**
EffectiveStartDate = POSITION2. No EndDate. CreatorType = H. EntryType = E. | 'Y'→ needs pass 2 |
| C (Cancel) | `MERGE\|ElementEntry\|570\|22-09-2019\|Dental EE Deduction\|123141402543\|H\|2019/09/22\|E\|1\|...\|Y`
Fetches original StartDate from cloud. Sets EndDate = cancellation date. Appends ReplaceLastEffectiveEndDate = Y. | 'N'→ no detail needed |

How the Code Actually Writes the ElementEntry Row

The formula does not** use positional output variables like `HDL_LINE1_N`. Instead, it assigns values to **named output variables** that match the METADATA column names. Then an explicit `RETURN` statement tells the HDL engine which variables to pick up and in what order.

Here's the Active path (POSITION11 is blank):

```text
IF LINEREPEATNO = 1 THEN
(
    /* ======================================== */
    /* ACTIVE entry — create new ElementEntry   */
    /* ======================================== */

    FileName                    = 'ElementEntry'
    BusinessOperation           = 'MERGE'
    FileDiscriminator           = 'ElementEntry'
    LegislativeDataGroupName    = l_LegislativeDataGroupName
    AssignmentNumber            = l_AssignmentNumber
    ElementName                 = l_ElementName
    EffectiveStartDate          = TO_CHAR(TO_DATE(TRIM(POSITION2),'YYYY/MM/DD'),'YYYY/MM/DD')
    EntryType                   = l_entry_type
    CreatorType                 = l_CreatorType
    SourceSystemOwner           = l_SourceSystemOwner
    SourceSystemId              = l_SourceSystemId
    LINEREPEAT                  = 'Y'             /* ← call me again for ElementEntryValue */

    RETURN BusinessOperation, FileName, FileDiscriminator,
           CreatorType, EffectiveStartDate, ElementName,
           LegislativeDataGroupName, EntryType, AssignmentNumber,
           SourceSystemOwner, SourceSystemId,
           LINEREPEAT, LINEREPEATNO
)
```

**How the RETURN works:** The variable names in the RETURN statement must match the METADATA column names exactly. The HDL engine maps each returned variable to its corresponding METADATA position and writes the pipe-delimited row in that order. `FileName` and `FileDiscriminator` go to positions [1] and [2]. The rest map by name to the METADATA array you defined in Section 5.

For a **Cancel** row (POSITION11 = 'C'), the formula fetches the original start date from the cloud, sets an end date, and returns `LINEREPEAT = 'N'` (no pass 2 needed — you don't need an ElementEntryValue for a cancellation):

```text
IF (TRIM(POSITION11) = 'C') THEN
(
    /* Fetch the original start date from cloud */
    l_Effective_Start_Date = GET_VALUE_SET('XXVA_GET_EE_START_DATE', ...)

    /* Same named variables, but with end date + replace flag */
    FileName                    = 'ElementEntry'
    BusinessOperation           = 'MERGE'
    FileDiscriminator           = 'ElementEntry'
    EffectiveStartDate          = TO_CHAR(TO_DATE(l_Effective_Start_Date,...),'YYYY/MM/DD')
    EffectiveEndDate            = TO_CHAR(TO_DATE(TRIM(POSITION2),...),'YYYY/MM/DD')
    ReplaceLastEffectiveEndDate = 'Y'
    LINEREPEAT                  = 'N'              /* ← no pass 2 for cancel */
    /* ...same other variables as Active... */

    RETURN BusinessOperation, FileName, FileDiscriminator,
           CreatorType, EffectiveStartDate, EffectiveEndDate,
           ElementName, LegislativeDataGroupName, EntryType,
           AssignmentNumber, SourceSystemOwner, SourceSystemId,
           ReplaceLastEffectiveEndDate,
           LINEREPEAT, LINEREPEATNO
)
```

Notice the Cancel RETURN includes `EffectiveEndDate` and `ReplaceLastEffectiveEndDate` — both absent from the Active RETURN.

Duplicate Header Prevention (WSA)

One person can have multiple vendor rows (Dental, Medical, Vision) that all map to different elements. Each element needs exactly one ElementEntry row. But if two vendor rows map to the **same** element, the formula must not generate a duplicate header. It checks WSA:

```text
IF WSA_EXISTS('HDR_' || L_PersonNumber || '_' || l_ElementName || '_' || POSITION2) THEN
(
    /* Header already generated for this combo — skip to pass 2 */
    LINEREPEAT = 'Y'
    RETURN
)
/* First time for this combo — generate header, then mark in WSA */
WSA_SET('HDR_' || ..., 1)
```

Watch out: ISNULL is inverted

The formula checks `ISNULL(l_ElementName) = 'N'` before generating anything. In Fast Formula, `'N'` means the value IS null (not found). If the vendor code didn't map to any element, the formula skips the row silently.

---

Same Vendor Input Row → multiple ElementEntryValue outputs (one per input value):

### ↓ Each pass loads a different InputValueName ↓

Pass 2 — ElementEntryValue (Amount):

| InputValueName | Amount |
| --- | --- |
| ScreenEntryValue | 150.00 |
| ElementEntryId(SSID) | HDL_XXVA_E12345_EE_... (links to parent ElementEntry) |

Pass 3 — ElementEntryValue (Period Type):

| InputValueName | Period Type |
| --- | --- |
| ScreenEntryValue | Monthly |

Pass 6 — ElementEntryValue (Percentage):

| InputValueName | Percentage |
| --- | --- |
| ScreenEntryValue | 5.5 |

Passes 4, 5, 7 skipped — PRE type doesn't use Loan Number, Total Owed, or Deduction Amount. The formula returns `LINEREPEAT = 'Y'` with no output data on those passes.

Passes 2 through 7 each generate one ElementEntryValue row. Each pass loads a different input value. The deduction type (POSITION4) controls which passes produce output and which ones skip.

What LINEREPEATNO = 2 Generates

Each ElementEntryValue pass sets `InputValueName` to a different value and loads the corresponding data into `ScreenEntryValue`:

| Column | Value | Source |
| --- | --- | --- |
| LINEREPEATNO | InputValueName | ScreenEntryValue source |
| 2 | Amount | l_Amount (POSITION5) = 150.00 |
| 3 | Period Type | l_PeriodType (POSITION6) = Monthly |
| 4 | Loan Number | POSITION8 — LOAN type only |
| 5 | Total Owed | l_TotalOwed — LOAN type only |
| 6 | Percentage | l_Percentage (POSITION7) — PRE/POST type only |
| 7 | Deduction Amount | l_DeductionAmount — CU type only |

How the Code Actually Writes the ElementEntryValue Row

Each pass from 2 to 7 follows the same structure. The key difference is the skip logic: each pass checks POSITION4 (deduction type) to decide whether to generate output or just return `LINEREPEAT = 'Y'` with no data (effectively skipping to the next pass). Same pattern — named output variables + explicit RETURN. But now `FileDiscriminator = 'ElementEntryValue'` (not 'ElementEntry'), and the RETURN includes `InputValueName`, `ScreenEntryValue`, and the parent link `"ElementEntryId(SourceSystemId)"`.

```text
ELSE IF (LINEREPEATNO = 2) THEN
(
    l_InputValueName = 'Amount'

    /* Look up ElementEntryValue SourceSystemId from cloud (or construct new one) */
    l_EEV_SourceSystemId = GET_VALUE_SET(
        'XXVA_GET_EEV_SOURCE_SYSTEM_ID', ...)
    l_EEV_SourceSystemOwner = GET_VALUE_SET(
        'XXVA_GET_EEV_SOURCE_SYSTEM_OWNER', ...)

    /* If no existing SSID found, construct a new one */
    IF ISNULL(l_EEV_SourceSystemId) = 'N' THEN
    (
        l_EEV_SourceSystemId = 'HDL_XXVA' || l_AssignmentNumber
            || '_EEV_' || L_PersonNumber
            || '_' || l_ElementName
            || '_' || l_InputValueName
            || '_' || TO_CHAR(TO_DATE(TRIM(POSITION2),...),'YYYYMMDD')
    )

    /* ============================================= */
    /* Set the output variables for ElementEntryValue */
    /* ============================================= */

    FileName                          = 'ElementEntry'        /* always ElementEntry */
    BusinessOperation                 = 'MERGE'
    FileDiscriminator                 = 'ElementEntryValue'   /* ← THIS is the key difference */
    LegislativeDataGroupName          = l_LegislativeDataGroupName
    AssignmentNumber                  = l_AssignmentNumber
    ElementName                       = l_ElementName
    EntryType                         = l_entry_type
    EffectiveStartDate                = TO_CHAR(...)
    "ElementEntryId(SourceSystemId)"  = l_SourceSystemId      /* ← links to parent ElementEntry */
    SourceSystemId                    = l_EEV_SourceSystemId  /* ← EEV's own SSID */
    SourceSystemOwner                 = l_EEV_SourceSystemOwner
    InputValueName                    = l_InputValueName      /* 'Amount' */
    ScreenEntryValue                  = To_Char(TO_NUM(TRIM(l_Amount)))
    LINEREPEAT                        = 'Y'                  /* more passes to come (pass 7 returns 'N') */

    RETURN BusinessOperation, FileName, FileDiscriminator,
           AssignmentNumber, EffectiveStartDate, ElementName,
           EntryType, LegislativeDataGroupName,
           "ElementEntryId(SourceSystemId)",
           InputValueName, ScreenEntryValue,
           SourceSystemOwner, SourceSystemId,
           LINEREPEAT, LINEREPEATNO
)
```

**Three things to notice:**

**1.** `FileName` is still `'ElementEntry'` — NOT `'ElementEntryValue'`. Only the `FileDiscriminator` changes to `'ElementEntryValue'`. This is how HDL knows the row goes into the ElementEntryValue block of the .dat file.**

2.** `"ElementEntryId(SourceSystemId)"` is set to the **ElementEntry's** SourceSystemId (`l_SourceSystemId`). This is the parent-child link. The variable name contains parentheses, so it must be double-quoted in the formula code.**

3.** The ElementEntryValue has its **own** SourceSystemId (`l_EEV_SourceSystemId`), different from the parent ElementEntry's. The formula first tries to find an existing one from the cloud via value set. If not found (`ISNULL = 'N'`), it constructs one with the pattern: `HDL_XXVA + AssignmentNumber + _EEV_ + PersonNumber + _ElementName + _InputValueName + _Date`.

The Parent-Child Link

The ElementEntryValue row must reference its parent ElementEntry row. HDL uses SourceSystemId to link them:

ElementEntry (Pass 1)

SourceSystemId = HDL_XXVA_E12345_EE_...

## →

ElementEntryValue (Pass 2)

ElementEntryId(SSID) = HDL_XXVA_E12345_EE_...

SourceSystemId = HDL_XXVA_E12345_EEV_...

The ElementEntryValue's `ElementEntryId(SourceSystemId)` matches the ElementEntry's `SourceSystemId`. This is how HDL knows which entry this value belongs to.

The RTRIM Trick for Clean Numbers

the vendor sends amounts like `150.00`, but Oracle elements expect clean numbers. The formula strips trailing zeros:

```text
RTRIM(RTRIM(TRIM(l_Amount), '0'), '.')

/* 150.00 → 150 | 75.50 → 75.5 | 12.30 → 12.3 | 150.00 → 150.00 */
```

The inner RTRIM strips trailing zeros. The outer RTRIM strips the decimal point if nothing is left after it.

---

**Vendor CSV Row:** `123-45-6789,2024-01-15,DENTAL01,150.00,,,`

STEP 1: Type → ER, Amount → 150.00

STEP 2: Key → DENTAL01 → Dental EE Deduction

STEP 3: SSN → Person# 100045, Asg# E12345 (WSA)

STEP 4: MultipleEntryCount = 1

STEP 5: SourceSystemId constructed

LINEREPEATNO=1 → ElementEntry:

```text
MERGE|ElementEntry|570|2019/09/22|Dental EE Deduction|123141402543|H||E|1
```

LINEREPEATNO=2 → ElementEntryValue (Amount):

```text
MERGE|ElementEntryValue|570|2019/09/22|Dental EE Deduction|123141402543|Amount||E||1|150.00
```

---

If you've read this far, you can now explain — without looking at any code — how an HDL Transformation Formula works end-to-end. You know what each OPERATION does, why METADATA arrays define the .dat column headers, how the MAP block transforms source data in 5 steps, why WSA exists (performance + correctness), how LINEREPEATNO generates multiple output rows (1 ElementEntry + up to 6 ElementEntryValues) from one source row, and how named RETURN variables map to METADATA columns.

That's the foundation. The concepts don't change whether you're building an vendor deduction interface, a benefits enrollment loader, or a payroll costing feed. Every HDL Transformation Formula follows this same structure.

Coming Next — Part 2: Code Walkthrough

Part 2 takes every concept from this post and shows you the actual Fast Formula code that implements it. Line by line, with the Notepad++ syntax highlighting you've been seeing in the code snippets here.

What Part 2 will cover:

| Full INPUTS ARE block | Every POSITION mapped to its vendor column, every DEFAULT FOR explained |
| --- | --- |
| GET_VALUE_SET calls | The exact parameter string construction with pipe delimiters, date conversions, and ISNULL checking |
| WSA implementation | Real WSA_EXISTS / WSA_GET / WSA_SET code with key construction patterns |
| SourceSystemId logic | The full lookup-or-construct pattern for both ElementEntry and ElementEntryValue SourceSystemIds |
| ESS_LOG_WRITE debugging | Adding trace logs at each step so you can debug formula execution in real time |
| Cancel vs Active branching | The complete IF POSITION11 = 'C' block with date fetching from cloud |

Later — Part 3: Build Your Own

Part 3 is the implementation guide. You'll build an HDL Transformation Formula from scratch — from creating the formula in Oracle Cloud, defining all 11 value sets, configuring the HDL integration, running test loads, reading ESS logs, and troubleshooting the errors you'll hit in production.

After Part 3, you'll have a working formula you can adapt for any inbound payroll interface — not just one vendor.

Series Roadmap

Part 1: Pure Concepts ← This post

→

Part 2: Code Walkthrough Coming soon

→

Part 3: Build Your Own Coming soon

Abhishek Mohanty
