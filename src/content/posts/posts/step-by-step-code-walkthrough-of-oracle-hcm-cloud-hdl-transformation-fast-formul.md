---
title: "Step-by-step code walkthrough of Oracle HCM Cloud HDL Transformation Fast Formula — INPUTS ARE declaration, GET_VALUE_SET parameter construction, ISNULL checking, SourceSystemId resolution, ESS_LOG_WRITE tracing, LINEREPEATNO pass logic for ElementEntry and ElementEntryValue, and Cancel end-dating with ReplaceLastEffectiveEndDate. Part 2 of 3."
description: "Oracle HCM Cloud HDL Transformation Fast Formula — Line-by-Line Code Walkthrough"
pubDate: 2026-03-26
---

Fast Formula
HCM Data Loader
Transformation Formula
ESS_LOG_WRITE
Series Part 2 of 3

Oracle HCM Cloud HDL Transformation Fast Formula — Line-by-Line Code Walkthrough

Vendor Deduction Interface | ElementEntry + ElementEntryValue

This is **Part 2** of a 3-part series on HDL Transformation Formulas. Part 1 covered the concepts — what each section does and why. This post opens the actual code. Every line is explained in simple English with visuals showing what the Fast Formula engine does at each step.

### HDL Transformation Formula Series

1
Pure Concepts

INPUTS, OPERATION, METADATA, MAP, WSA, LINEREPEATNO, RETURN. Zero code.

2
Code Walkthrough ← You are here

Actual code, line-by-line. Value set calls, ISNULL, SourceSystemId, ESS_LOG_WRITE, Cancel branching.

3
Build Your Own Soon

WSA code, HDL config, test loads, production debugging.

Abhishek Mohanty

## OPERATION Routing in HDL Transformation Formula — FILETYPE, DELIMITER, METADATA

The HDL engine calls your formula many times. The OPERATION variable tells the formula *why* it's being called. Here's the routing code that handles each call:

OPERATION Routing — Setup Handshake

```text
 1IF OPERATION = 'FILETYPE' THEN
 2   OUTPUTVALUE = 'DELIMITED'
 3ELSE IF OPERATION = 'DELIMITER' THEN
 4   OUTPUTVALUE = ','
 5ELSE IF OPERATION = 'READ' THEN
 6   OUTPUTVALUE = 'NONE'
 7ELSE IF OPERATION = 'NUMBEROFBUSINESSOBJECTS' THEN
 8(
 9   OUTPUTVALUE = '2'                              /* ElementEntry + ElementEntryValue */
10   RETURN OUTPUTVALUE
11)
```

OPERATION Routing — METADATA Header Definitions

```text
12ELSE IF OPERATION = 'METADATALINEINFORMATION' THEN
13(
14    /* Object 1: ElementEntry columns */
15    METADATA1[1] = 'ElementEntry'               /* FileName (reserved)        */
16    METADATA1[2] = 'ElementEntry'               /* FileDiscriminator (reserved)*/
17    METADATA1[3] = 'LegislativeDataGroupName'
18    METADATA1[4] = 'EffectiveStartDate'
19    METADATA1[5] = 'ElementName'
20    METADATA1[6] = 'AssignmentNumber'
21    METADATA1[7] = 'CreatorType'
22    METADATA1[8] = 'EntryType'
23    METADATA1[9] = 'MultipleEntryCount'
24    METADATA1[10] = 'SourceSystemOwner'
25    METADATA1[11] = 'SourceSystemId'
26
27    /* Object 2: ElementEntryValue columns */
28    METADATA2[1] = 'ElementEntry'               /* FileName (reserved)        */
29    METADATA2[2] = 'ElementEntryValue'          /* FileDiscriminator (reserved)*/
30    METADATA2[3] = 'LegislativeDataGroupName'
31    METADATA2[4] = 'EffectiveStartDate'
32    METADATA2[5] = 'ElementName'
33    METADATA2[6] = 'AssignmentNumber'
34    METADATA2[7] = 'InputValueName'
35    METADATA2[8] = 'EntryType'
36    METADATA2[9] = 'MultipleEntryCount'
37    METADATA2[10] = 'ScreenEntryValue'           /* the actual dollar amount    */
38    METADATA2[11] = 'ElementEntryId(SourceSystemId)'  /* parent link */
39    METADATA2[12] = 'SourceSystemOwner'
40    METADATA2[13] = 'SourceSystemId'
41
42    RETURN METADATA1, METADATA2
43)
```

**Lines 1–11:** Setup handshake. The engine asks config questions, the formula answers. Same in every HDL formula.

**Lines 14–25:** METADATA1 defines the .dat columns for ElementEntry. Lines 28–40: METADATA2 defines columns for ElementEntryValue. The column names here must exactly match the variable names in the RETURN statement later.

### What This Post Covers

| 1 | Full INPUTS ARE Block | Every POSITION mapped to its vendor column. |
| --- | --- | --- |
| 2 | GET_VALUE_SET Calls | How the formula talks to the database. |
| 3 | SourceSystemId Logic | "Am I updating old or creating new?" |
| 4 | ESS_LOG_WRITE Debugging | Printing debug messages to the log. |
| 5 | LINEREPEATNO Output Logic | Pass 1 (ElementEntry), Pass 2 (ElementEntryValue), and Cancel End-Dating |

**Not in this post:** WSA caching code. Part 1 explained the concept. Part 3 will show the full WSA_EXISTS / WSA_GET / WSA_SET implementation.

---

## INPUTS ARE and DEFAULT FOR — Declaring POSITION Variables in Fast Formula

Every formula starts by declaring what data it expects. The HDL engine reads your CSV file and puts each column into a POSITION variable — column 1 → POSITION1, column 2 → POSITION2, and so on.

How the Engine Maps CSV Columns to POSITION Variables

/* Your CSV row: */  1,DENTAL01,2024-01-15,100045,E12345,150.00,...

COL 1

1

POSITION1

COL 2 ★

DENTAL01

POSITION2

COL 3 ★

2024-01-15

POSITION3

COL 4 ★

100045

POSITION4

COL 5

E12345

POSITION5

COL 6 ★

150.00

POSITION6

★ Columns actively used in the MAP logic. Others are declared but not referenced.

Here's the actual declaration code:

XXTAV_HDL_ACCRUAL_INBOUND — Input Declaration

```text
 1INPUTS ARE OPERATION (TEXT),          /* Engine control signal                          */
 2LINEREPEATNO (NUMBER),                   /* Which pass: 1 = header, 2 = value row          */
 3LINENO (NUMBER),                         /* Source file line number                         */
 4POSITION1 (TEXT),                         /* LINE_SEQUENCE                                   */
 5POSITION2 (TEXT),                         /* XXTAV_CODE — vendor pay code              ★    */
 6POSITION3 (TEXT),                         /* EFFECTIVE_START_DATE — YYYY-MM-DD          ★    */
 7POSITION4 (TEXT),                         /* PERSON_NUMBER                              ★    */
 8POSITION5 (TEXT),                         /* ASSIGNMENT_NUMBER                               */
 9POSITION6 (TEXT),                         /* XXTAV_PTO_BALANCE — the dollar amount         ★    */
10POSITION7 (TEXT),  POSITION8 (TEXT),    /* AMOUNT, EARNED_DATE                             */
11POSITION9 (TEXT),  POSITION10 (TEXT),  /* LOC, LOB                                        */
12POSITION11 (TEXT)                         /* DEPARTMENT                                      */
```

**In plain English:** This block says: "Engine, when you call me, give me three system variables (OPERATION, LINEREPEATNO, LINENO) and eleven data variables (POSITION1–11) — one for each column in my CSV." The ★ marks show which four columns the formula actually uses. The rest are declared because the engine fills them regardless.

### DEFAULT FOR — Why Every POSITION Variable Needs a Default

```text
DEFAULT FOR LINENO IS 1
DEFAULT FOR LINEREPEATNO IS 1
DEFAULT FOR POSITION1 IS 'NO DATA'
/* ... same for POSITION2 through POSITION11 ... */
DEFAULT FOR POSITION11 IS 'NO DATA'
```

**Why?** Look at the engine timeline above. The first five calls (FILETYPE, DELIMITER, etc.) happen *before* any CSV row is read. POSITION variables are empty during those calls. Without defaults, the formula crashes with a null error before it even reaches the MAP block.

---

## GET_VALUE_SET in Fast Formula — Parameter String Syntax, Pipe Delimiters, ISNULL Checks

The vendor gives us a code like `DENTAL01`. Oracle doesn't know it. We need to ask the database: "What Element Name does DENTAL01 map to?" GET_VALUE_SET runs a SQL query and brings the answer back.

How GET_VALUE_SET Works

Your Formula

GET_VALUE_SET(**'XXTAV_ACCRUAL_ELEMENTS',
'DENTAL01')

Value Set

Looks up vendor code
in the mapping table
and returns the Oracle
element name

Result

Dental EE Deduction

### GET_VALUE_SET Call 1 — Resolving Person Number to Assignment Number

```text
l_AssignmentNumber = GET_VALUE_SET(
    'XXTAV_GET_LATEST_ASSIGNMENT_NUMBER',
    '|=P_PERSON_NUMBER=''' || POSITION4 || ''''
 || '|P_EFFECTIVE_START_DATE='''
 || TO_CHAR(TO_DATE(POSITION3,'YYYY-MM-DD'),'YYYY-MM-DD')
 || '''')
```

l_AssignmentNumber = GET_VALUE_SET(

Store the answer here

  'XXTAV_GET_LATEST_ASSIGNMENT_NUMBER',

Which value set to call

  '|=P_PERSON_NUMBER=''' || POSITION4 || ''''

Param 1: Person# (100045)

 || TO_CHAR(TO_DATE(POSITION3,...),'YYYY-MM-DD')

Param 2: Date (normalized)

TO_DATE → TO_CHAR: Date Normalization Pipeline

Raw Input

POSITION3

'2024-01-15' or '2024/01/15'

TO_DATE( )

Parse string → date object

15-JAN-2024

TO_CHAR( )

Date object → clean string

2024-01-15

Clean Output

Ready to pass into
the value set

Why convert twice?** The vendor might change date formats. TO_DATE reads whatever arrives. TO_CHAR writes it in the exact format the value set expects. Your formula works either way without code changes.

### GET_VALUE_SET Call 2 — Mapping Vendor Code to Oracle Element Name

```text
l_ElementName = GET_VALUE_SET(
    'XXTAV_ACCRUAL_ELEMENTS TEST',
    '|=P_PAY_CODE=''' || TRIM(POSITION2) || '''')
```

**Simplest call — one parameter.** Takes the vendor code from POSITION2, strips whitespace with TRIM(), and asks: "What Oracle Element Name does this map to?" If the vendor sends `' DENTAL01 '` with spaces, TRIM cleans it first.

### ISNULL in Fast Formula — Why 'N' Means Null (Not What You Expect)

```text
IF ISNULL(l_MultipleEntryCount) = 'N' THEN
(
    l_MultipleEntryCount = '1'     /* default to 1 */
)
```

ISNULL(x) = 'Y' → value exists ✓

l_MEC = **'3'****
ISNULL('3') → 'Y'

Is 'Y' = 'N'? → No****
→ Skip IF. Keep '3'.

ISNULL(x) = 'N' → value is null ✗

l_MEC = (null)****
ISNULL(null) → 'N'

Is 'N' = 'N'? → Yes****
→ Enter IF. Set to '1'.

Memory trick:** Think of ISNULL as asking "Does this have data? Yes/No." — `'Y'` = Yes, it has data. `'N'` = No data. So `= 'N'` means "nothing found."

### Value Set Dependency Chain — Why Call Order Matters in the MAP Block

These GET_VALUE_SET calls are not independent. Each one depends on the result of a previous one. The formula resolves values in a specific order because later calls need the output of earlier ones as input:

Value Set Resolution Chain — Each Step Feeds the Next

Call 1 — Element Name

Uses: **POSITION2** (vendor code)**Produces: l_ElementName**

DENTAL01 → 'Dental EE Deduction'

No dependencies — this call only needs the raw vendor code from the CSV.

Call 2 — Assignment Number

Uses: **POSITION4** (person#) + **POSITION3** (date)**Produces: l_AssignmentNumber**

100045 + 2024-01-15 → 'E12345'

No dependencies — uses raw CSV values directly.

Call 3 — MultipleEntryCount

Uses: **POSITION4** + **POSITION3** + **l_ElementName** ← *from Call 1***Produces: l_MultipleEntryCount**

100045 + 2024-01-15 + 'Dental EE Deduction' → '1'

Depends on Call 1. If you swap the order, l_ElementName is empty and this call returns wrong results.

Call 4 — SourceSystemId

Uses: **POSITION4** + **POSITION3** + **l_ElementName** ← *from Call 1***Produces: l_SourceSystemId**

Lookup existing SSID or construct new one

Depends on Call 1. Also uses l_AssignmentNumber from Call 2 when constructing a new ID.

**The key insight:** Call 1 (Element Name) and Call 2 (Assignment Number) can run in any order — they only use raw POSITION values from the CSV. But Calls 3 and 4 **must** come after Call 1 because they pass `l_ElementName` as a parameter. If you rearrange the formula and move Call 3 above Call 1, the element name variable will be empty and the value set will return the wrong result — or nothing at all.

This is a common mistake when modifying someone else's formula. The calls look independent, but they chain.

---

## SourceSystemId in HDL — Lookup-or-Construct Pattern for MERGE

Every element entry has a SourceSystemId — a unique name tag. During MERGE, Oracle checks: "Do I already have an entry with this tag?" If yes → update. If no → create. The formula follows a two-step pattern:

SourceSystemId Resolution Flow

Step 1 — Ask the cloud

"Does a SourceSystemId already exist for this person + element + date?"

GET_VALUE_SET('XXTAV_GET_ELEMENT_ENTRY_SOURCE_SYSTEM_ID', ...)

Step 2 — Check what came back

Found → Reuse it

Oracle will UPDATE the existing entry

Not found → Build a new one

Oracle will INSERT a new entry

```text
/* Step 1: Try cloud lookup */
l_SourceSystemId = GET_VALUE_SET(
    'XXTAV_GET_ELEMENT_ENTRY_SOURCE_SYSTEM_ID',
    '|=P_PERSON_NUMBER=''' || POSITION4 || ''''
 || '|P_EFFECTIVE_START_DATE=''' || ... || ''''
 || '|P_ELEMENT_NAME=''' || l_ElementName || '''')

/* Step 2: If null → build new */
IF ISNULL(l_SourceSystemId) = 'N' THEN
(
    l_SourceSystemId = 'XXTAV_HDL' || l_AssignmentNumber
        || '_EE_' || POSITION4
        || '_'    || POSITION2
        || '_'    || POSITION3
)
```

SourceSystemId — Assembled from parts

XXTAV_HDLprefix

E12345Assignment#

_EE_marker

100045Person#

DENTAL01Code

2024-01-15Date

ElementEntry: XXTAV_HDL...**_EE_**...

EntryValue: XXTAV_HDL...**_EEV_**...

Only difference between header and value ID: **_EE_** vs **_EEV_**

---

## ESS_LOG_WRITE in HDL Fast Formula — Adding Debug Trace Logs to the MAP Block

You can't step through a Fast Formula with a debugger. The only way to see what's happening inside is to write trace messages to the ESS job log. `ESS_LOG_WRITE` prints a message each time the formula passes through it — so you know exactly which step ran, what value it produced, and where it stopped if something fails.

Place one after every major step in the MAP block. Here's how that looks:

XXTAV_HDL_ACCRUAL_INBOUND — Debug Trace Logs

```text
 1/* ─────────────────────────────────────────────── */
 2/*  STEP 1: Log the raw input from the CSV row    */
 3/* ─────────────────────────────────────────────── */
 4ESS_LOG_WRITE('XXTAV > START'
 5    || ' | Line='   || TO_CHAR(LINENO)
 6    || ' | Code='   || POSITION2
 7    || ' | Person=' || POSITION4)
 8
 9/*  STEP 2: After the element name lookup         */
10ESS_LOG_WRITE('XXTAV > ELEMENT = ' || l_ElementName)
11
12/*  STEP 3: After the assignment number lookup    */
13ESS_LOG_WRITE('XXTAV > ASSIGNMENT = ' || l_AssignmentNumber)
14
15/*  STEP 4: Final resolved values before output   */
16ESS_LOG_WRITE('XXTAV > MEC=' || l_MultipleEntryCount
17    || ' | SSID=' || l_SourceSystemId)
```

After running **Load Data from File**, open the ESS job log: **Scheduled Processes → your job → Log tab**. You will see output like this:

ESS Job Log — Output for Row 1

```text
› XXTAV > START | Line=1 | Code=DENTAL01 | Person=100045
› XXTAV > ELEMENT = Dental EE Deduction
› XXTAV > ASSIGNMENT = E12345
› XXTAV > MEC=1 | SSID=XXTAV_HDLE12345_EE_100045_DENTAL01_2024-01-15
```

**How to read it:** Each line is one trace log from a step in your formula. If the formula fails at the assignment lookup, you'll see Steps 1 and 2 in the log but not Step 3 — so you know exactly where it broke. The `XXTAV >` prefix makes it easy to search for your formula's output in a log that might contain messages from other formulas running in the same batch.

**Before production:** Remove or comment out all ESS_LOG_WRITE calls. With 10,000 rows and 4 log calls per row, that's 40,000 extra write operations slowing down your load.

---

## LINEREPEATNO — How the Formula Generates ElementEntry and ElementEntryValue Output Rows

The vendor uses a status field: blank = Active (create/update), `'C'` = Cancel (end-date). The formula handles these two paths completely differently.

Active (POSITION11 = blank)

**EffectiveStartDate** = vendor date (POSITION3)**
EffectiveEndDate** = not set**
LINEREPEAT** = 'Y' → Pass 2 follows**
Oracle creates or updates the entry

Cancel (POSITION11 = 'C')

EffectiveStartDate** = fetched from cloud**
EffectiveEndDate** = vendor's cancel date**
LINEREPEAT** = 'N' → Done, no Pass 2**
Oracle end-dates the entry

### LINEREPEATNO = 1 — Active Path: Creating the ElementEntry Row

On the first pass, the formula sets all output variables for the ElementEntry header. Each variable name must match a METADATA1 column name exactly — that's how the engine knows which .dat column to write it into.

Active Path — LINEREPEATNO = 1 — Create ElementEntry

```text
 1IF LINEREPEATNO = 1 THEN
 2(
 3    FileName                 = 'ElementEntry'
 4    BusinessOperation        = 'MERGE'
 5    FileDiscriminator        = 'ElementEntry'        /* ← tells engine: use METADATA1 */
 6    LegislativeDataGroupName = l_LegislativeDataGroupName
 7    AssignmentNumber         = l_AssignmentNumber     /* from GET_VALUE_SET Call 1      */
 8    ElementName              = l_ElementName          /* from GET_VALUE_SET Call 2      */
 9    EffectiveStartDate       = TO_CHAR(TO_DATE(POSITION3,'YYYY-MM-DD'),'YYYY/MM/DD')
10                                                    /* ↑ input YYYY-MM-DD → output YYYY/MM/DD */
11    MultipleEntryCount       = l_MultipleEntryCount   /* from GET_VALUE_SET Call 3      */
12    EntryType                = l_entry_type           /* 'E' = normal entry             */
13    CreatorType              = l_CreatorType          /* 'H' = HDL created              */
14    SourceSystemOwner        = l_SourceSystemOwner    /* from Section 3 lookup          */
15    SourceSystemId           = l_SourceSystemId       /* from Section 3 lookup-or-build */
16    LINEREPEAT               = 'Y'                    /* ← KEY: tells engine to call    */
17                                                    /*   formula again with            */
18                                                    /*   LINEREPEATNO = 2              */
```

Line 5:** `FileDiscriminator = 'ElementEntry'` tells the engine to use the METADATA1 column layout for this row. In Pass 2, this switches to `'ElementEntryValue'` — which uses METADATA2 instead.

**Lines 16–18:** This is the entire LINEREPEAT mechanism. Setting `LINEREPEAT = 'Y'` tells the engine: "I have more output rows for this same CSV row. Call me again." The engine re-invokes the formula with LINEREPEATNO incremented to 2.

After setting the variables, the formula decides what to RETURN. This is the guard logic — if the element lookup failed, skip the row:

The ISNULL Guard — Two Different RETURN Paths

```text
19    /* ─── GUARD: Did the element lookup return a valid name? ─── */
20
21    IF ISNULL(l_ElementName) = 'N' THEN
22    (
23        /* Element IS null → vendor code not in value set mapping.      */
24        /* Return only LINEREPEAT + LINEREPEATNO — no data variables.   */
25        /* Engine writes nothing to .dat for this row. Silent skip.     */
26        RETURN LINEREPEAT, LINEREPEATNO
27    )
28    ELSE
29    (
30        /* Element found → return all output variables.                 */
31        /* Engine writes one MERGE|ElementEntry|... row to the .dat     */
32        RETURN BusinessOperation, FileName, FileDiscriminator,
33               MultipleEntryCount, CreatorType, EffectiveStartDate,
34               ElementName, LegislativeDataGroupName, EntryType,
35               AssignmentNumber, SourceSystemOwner, SourceSystemId,
36               LINEREPEAT, LINEREPEATNO
37    )
38)
```

**Line 26 vs Lines 32–36 — the key difference:** When the element is null (line 26), the formula returns *only* LINEREPEAT and LINEREPEATNO — no data variables at all. The engine writes nothing to the .dat file and moves on. When the element exists (lines 32–36), the formula returns all the output variables. The engine matches each variable name to the METADATA1 column name and writes a full `MERGE|ElementEntry|...` row.

One Vendor Row → Two .dat Rows (Full Journey)

Vendor CSV Row

1, DENTAL01, 2024-01-15, 100045, E12345, **150.00**, ...

Pass 1 (LINEREPEATNO = 1) → ElementEntry

MERGE|ElementEntry|US LDG|2024/01/15|Dental EE Deduction|E12345|H|E|1|XXTAV_HDL|XXTAV_HDL...

LINEREPEAT = 'Y' → engine increments LINEREPEATNO to 2, calls formula again

Pass 2 (LINEREPEATNO = 2) → ElementEntryValue

MERGE|ElementEntryValue|US LDG|2024/01/15|Dental EE Deduction|E12345|XXTAV_PTO BALANCE|E|1|**150**|...

LINEREPEAT = 'N' → engine moves to next CSV row

### LINEREPEATNO = 1 — Cancel Path: End-Dating with GET_VALUE_SET for Original Start Date

The vendor only sends the *cancellation date*. Oracle also needs the *original start date*. So the formula fetches it from the cloud:

Cancel Path — POSITION11 = 'C' — End-Date Entry

```text
 1IF (TRIM(POSITION11) = 'C') THEN
 2(
 3    /* Fetch original start date from cloud */
 4    l_Effective_Start_Date = GET_VALUE_SET(
 5        'XXTAV_GET_ELEMENT_ENTRY_START_DATE', ...)
 6
 7    EffectiveStartDate = TO_CHAR(TO_DATE(
 8        l_Effective_Start_Date,'YYYY-MM-DD'),'YYYY/MM/DD')
 9                                          /* ↑ from cloud */
10    EffectiveEndDate = TO_CHAR(TO_DATE(
11        TRIM(POSITION3),'YYYY-MM-DD'),'YYYY/MM/DD')
12                                          /* ↑ from vendor */
13    ReplaceLastEffectiveEndDate = 'Y'       /* override existing */
14    /* ... same other vars ... */
15    LINEREPEAT = 'N'                        /* done. no pass 2. */
16
17    RETURN ..., EffectiveStartDate, EffectiveEndDate,
18           ReplaceLastEffectiveEndDate, LINEREPEAT, LINEREPEATNO
19)
```

Cancel Path — Where Each Date Comes From

EffectiveStartDate

Source: **Oracle Cloud**

GET_VALUE_SET('XXTAV_GET_EE_START_DATE')

When the entry **originally started**

2024/01/01

EffectiveEndDate

Source: **Vendor File**

POSITION3 (cancellation date)

When the entry **should end**

2024/03/15

### Pass 2: Loading the Dollar Amount (LINEREPEATNO = 2)

The engine calls the formula again. Same CSV row. But LINEREPEATNO is now 2.

**First — clean the amount:**

Pass 2 — Clean the Dollar Amount

```text
1ELSE IF (LINEREPEATNO = 2) THEN
2(
3    l_ScreenEntryValue = RTRIM(RTRIM(TRIM(POSITION6),'0'),'.')
4
5    IF ISNULL(l_ScreenEntryValue) = 'N' THEN
6    (   l_ScreenEntryValue = '0'   )
```

Line 3 strips trailing zeros and dots. If the result is empty, line 5 defaults to '0'.

What line 3 does to different amounts

| 150.00 | → 150 |
| --- | --- |
| 75.50 | → 75.5 |
| 200.00 | → 200 |

**Then — set output variables.** Most are the same as Pass 1. Only three things change:

Pass 2 — The Three Things That Change

```text
 7    /* Change 1: Switch to ElementEntryValue layout */
 8    FileDiscriminator     = 'ElementEntryValue'
 9
10    /* Change 2: Two new variables — the value data */
11    InputValueName        = l_InputValueName         /* 'XXTAV_PTO BALANCE' */
12    ScreenEntryValue      = l_ScreenEntryValue       /* '150' (cleaned)    */
13
14    /* Change 3: Done with this row */
15    LINEREPEAT            = 'N'
16
17    /* Everything else — same as Pass 1 */
18    SourceSystemId        = l_EEV_SourceSystemId
19    SourceSystemOwner     = l_EEV_SourceSystemOwner
20    /* ... AssignmentNumber, ElementName, etc. — same ... */
```

**Finally — RETURN:**

Pass 2 — RETURN

```text
21    RETURN BusinessOperation, FileName, FileDiscriminator,
22           AssignmentNumber, EffectiveStartDate,
23           ElementName, EntryType,
24           LegislativeDataGroupName, MultipleEntryCount,
25           InputValueName, ScreenEntryValue,
26           SourceSystemOwner, SourceSystemId,
27           LINEREPEAT, LINEREPEATNO
28)
```

The engine writes this to the .dat file:

MERGE|ElementEntryValue|United States LDG|2024/01/15|Dental EE Deduction|E12345|XXTAV_PTO BALANCE|E|1|**150**

**That's it for one row.** Pass 1 creates the header. Pass 2 creates the value. Now the engine moves to the next CSV row and the whole cycle repeats.

### Putting It All Together — How the Engine Processes a 3-Row File

Here's a vendor file with 3 rows. Two active deductions and one cancellation. Watch how the engine and formula talk to each other for each row:

vendor_accrual_file.csv

```text
Row 1:  1,DENTAL01,2024-01-15,100045,E12345,150.00,...
Row 2:  2,MEDICAL01,2024-01-15,100045,E12345,200.00,...
Row 3:  3,VISION01,2024-03-15,100045,E12345,,C
```

ROW 1
DENTAL01  ·  100045  ·  $150.00

ACTIVE

PASS 1

Engine sends LINEREPEATNO = 1**
Formula creates → ElementEntry** header for Dental EE Deduction

FORMULA RETURNS

LINEREPEAT = 'Y'

↓ engine calls again

PASS 2

Engine sends LINEREPEATNO = 2**
Formula creates → ElementEntryValue** with amount $150

FORMULA RETURNS

LINEREPEAT = 'N'

→ next row

ROW 2
MEDICAL01  ·  100045  ·  $200.00

ACTIVE

PASS 1

Engine sends LINEREPEATNO = 1**
Formula creates → ElementEntry** header for Medical EE Deduction

FORMULA RETURNS

LINEREPEAT = 'Y'

↓ engine calls again

PASS 2

Engine sends LINEREPEATNO = 2**
Formula creates → ElementEntryValue** with amount $200

FORMULA RETURNS

LINEREPEAT = 'N'

→ next row

ROW 3
VISION01  ·  100045  ·  Status = C

CANCEL

PASS 1

Engine sends LINEREPEATNO = 1**
Formula creates → ElementEntry** with end-date for Vision EE Deduction**
No Pass 2 — cancellation has no dollar amount to load

FORMULA RETURNS

LINEREPEAT = 'N'

→ done

3 CSV rows → 5 engine calls.** Active rows get 2 calls (header + value). Cancel rows get 1 call (header only). The formula controls this entirely through `LINEREPEAT`: return `'Y'` to say "call me again", return `'N'` to say "move on."

#### The Final .dat Output

After all 5 calls, the engine writes this file:

ElementEntry.dat — Generated Output

```text
/* ElementEntry block */
METADATA|ElementEntry|LDG|EffStart|ElementName|Asg#|Creator|Entry|MEC
MERGE|ElementEntry|US LDG|2024/01/15|Dental EE Deduction|E12345|H|E|1
MERGE|ElementEntry|US LDG|2024/01/15|Medical EE Deduction|E12345|H|E|1
MERGE|ElementEntry|US LDG|2024/01/01|Vision EE Deduction|E12345|H|2024/03/15|E|1

/* ElementEntryValue block */
METADATA|ElementEntryValue|LDG|EffStart|ElementName|Asg#|InputValue|Entry|MEC|ScreenValue
MERGE|ElementEntryValue|US LDG|2024/01/15|Dental EE|E12345|XXTAV_PTO BALANCE|E|1|150
MERGE|ElementEntryValue|US LDG|2024/01/15|Medical EE|E12345|XXTAV_PTO BALANCE|E|1|200
/* ↑ No row for Vision — cancel has no dollar amount */
```

---

## What You Can Now Do After Part 1 and Part 2

After Part 1 and Part 2, you can open any HDL Transformation Formula and read it. You know the engine calls the formula many times — first for setup, then per row, then per pass. You can decode the triple-quote syntax in GET_VALUE_SET calls. You know `ISNULL(x) = 'N'` means the value IS null. You understand lookup-or-construct for SourceSystemId. You know where to put ESS_LOG_WRITE. And you can follow the Cancel vs Active branching.

**Left for Part 3:** WSA implementation (WSA_EXISTS / WSA_GET / WSA_SET code), the complete formula assembled end-to-end, and the step-by-step build-your-own guide.

---

Part 1: Pure Concepts

→

Part 2: Code Walkthrough ← This post

→

Part 3: Build Your Own Soon

Abhishek Mohanty
