---
title: "Step-by-step WSA implementation and complete code of Oracle HCM Cloud HDL Transformation Fast Formula — WSA_EXISTS, WSA_GET, WSA_SET for Person caching and MultipleEntryCount tracking, full formula with INPUTS ARE, OPERATION routing, METADATA, GET_VALUE_SET, SourceSystemId, LINEREPEATNO, and ElementEntry .dat output. Part 3 of 3."
description: "WSA Implementation and Complete HDL Transformation Fast Formula Code"
pubDate: 2026-03-27
---

Fast Formula
HCM Data Loader
Transformation Formula
WSA
Series Part 3 of 3

WSA Implementation and Complete HDL Transformation Fast Formula Code

Part 3 of 3 — WSA_EXISTS, WSA_GET, WSA_SET, and the Full Formula End-to-End

This is **Part 3** — the final post in this series. Part 1 explained the concepts. Part 2 walked through the code line by line. This post adds WSA caching into the formula and then gives you the **complete formula in one code block** — ready to adapt for your own implementation.

### HDL Transformation Formula Series

1
Pure Concepts

INPUTS, OPERATION, METADATA, MAP, WSA, LINEREPEATNO, RETURN.

2
Code Walkthrough

GET_VALUE_SET, ISNULL, SourceSystemId, ESS_LOG_WRITE, LINEREPEATNO.

3
WSA + Complete Formula ← You are here

WSA caching code, then the full formula assembled end-to-end.

Abhishek Mohanty

---

## Why WSA Is Needed in This Formula

Part 1 explained this in detail. Here's the short version with a quick visual.

Fast Formula has no memory between rows. The engine calls the formula once per row, then destroys all local variables. WSA (Working Storage Area) is an in-memory storage that **survives between calls**. You write a value on Row 1, and you can read it on Row 500.

This formula uses WSA for two reasons:

Reason 1 — Performance

Same person appears in multiple rows (Dental, Medical, Vision). Without WSA, the formula calls GET_VALUE_SET for the same person 3 times and gets the same answer 3 times. With WSA, it calls once and reads from cache for the rest.

WSA keys: `PER__` and `ASG__`

Reason 2 — Correctness

Two rows for the same person + element in the same batch. Both query the database for MultipleEntryCount and get the same MAX. Both assign the same count. Data is lost. WSA tracks what was already assigned so each row gets a unique count.

WSA key: `MEC___`

**Reason 1 is optional** — remove it and the formula still works, just slower. **Reason 2 is mandatory** — remove it and the formula produces wrong data.

---

## The WSA API — Three Functions

WSA has only three functions. Every usage in this formula follows the same pattern:

WSA Pattern — Check → Hit or Miss → Store

```text
 1/* Step 1: Check — does WSA already have this value? */
 2IF WSA_EXISTS(l_key) THEN
 3(
 4    /* Step 2a: HIT — read from memory */
 5    l_value = WSA_GET(l_key, ' ')
 6)
 7ELSE
 8(
 9    /* Step 2b: MISS — call the database */
10    l_value = GET_VALUE_SET(...)
11
12    /* Step 3: Store — save for next row */
13    WSA_SET(l_key, l_value)
14)
```

**WSA_EXISTS(key)** — Returns TRUE if the key exists in memory. Always check before reading.

**WSA_GET(key, default)** — Reads the stored value. The second parameter is a default that's returned if the key doesn't exist (but we always check with WSA_EXISTS first, so the default is never used — it's just required syntax).

**WSA_SET(key, value)** — Stores a value. Overwrites if the key already exists.

---

## WSA for Person and Assignment Lookup (Performance)

Instead of calling GET_VALUE_SET every time, the formula checks WSA first. If this person was already looked up on a previous row, read from memory:

WSA — Person + Assignment Number Caching

```text
 1/* Build a unique key from Person Number + Date */
 2l_wsa_per_key = 'PER_' || POSITION4 || '_' || POSITION3
 3l_wsa_asg_key = 'ASG_' || POSITION4 || '_' || POSITION3
 4
 5IF WSA_EXISTS(l_wsa_per_key) THEN
 6(
 7    /* HIT — person was already looked up on a previous row */
 8    L_PersonNumber     = WSA_GET(l_wsa_per_key, ' ')
 9    l_AssignmentNumber = WSA_GET(l_wsa_asg_key, ' ')
10)
11ELSE
12(
13    /* MISS — first time seeing this person. Call the database. */
14    l_AssignmentNumber = GET_VALUE_SET(
15        'XXTAV_GET_LATEST_ASSIGNMENT_NUMBER', ...)
16    L_PersonNumber     = GET_VALUE_SET(
17        'XXTAV_GET_PERSON_NUMBER', ...)
18
19    /* Save to WSA — next row with same person skips the DB */
20    WSA_SET(l_wsa_per_key, L_PersonNumber)
21    WSA_SET(l_wsa_asg_key, l_AssignmentNumber)
22)
```

**Line 2:** The key is built from Person Number + Date. Example: `PER_100045_2024-01-15`. If 3 rows have the same person and date (Dental, Medical, Vision), they all share this key.

**Lines 5–9:** WSA has this key → read from memory. Zero database calls.

**Lines 13–21:** WSA doesn't have this key → call the database, then save the result so the next row with the same person reads from cache.

---

## WSA for MultipleEntryCount (Correctness)

This is the critical one. Without it, two rows for the same person + element in the same batch get the same count — and one overwrites the other.

WSA — MultipleEntryCount Tracking

```text
 1/* Key includes Person + Element + Date — unique per combo */
 2l_wsa_mec_key = 'MEC_' || L_PersonNumber || '_'
 3             || l_ElementName || '_' || POSITION3
 4
 5IF WSA_EXISTS(l_wsa_mec_key) THEN
 6(
 7    /* A previous row already assigned a count for this combo */
 8    /* Read it and add 1                                      */
 9    l_MultipleEntryCount = TO_CHAR(
10        TO_NUMBER(WSA_GET(l_wsa_mec_key, '0')) + 1)
11)
12ELSE
13(
14    /* First row for this combo. Ask the database. */
15    l_db_max = GET_VALUE_SET(
16        'XXTAV_MAX_MULTI_ENTRY_COUNT', ...)
17
18    IF ISNULL(l_db_max) = 'N' THEN
19        l_MultipleEntryCount = '1'          /* nothing in cloud → start at 1 */
20    ELSE
21        l_MultipleEntryCount = TO_CHAR(
22            TO_NUMBER(l_db_max) + 1)    /* cloud has 1 → assign 2        */
23)
24
25/* Save what we assigned — next row reads this instead of DB */
26WSA_SET(l_wsa_mec_key, l_MultipleEntryCount)
```

**Lines 5–10:** WSA has a value → a previous row already got a count for this person + element + date. Read it and add 1. Row 5 got count 2, so Row 8 gets count 3.

**Lines 14–22:** WSA is empty → first row for this combo. Ask the database what's already in cloud. If cloud has nothing, start at 1. If cloud has MAX = 1, assign 2.

**Line 26:** Save whatever we assigned. This is the critical line. Without it, the next row for the same combo queries the stale database again and gets the same MAX.

---

## WSA Requires Single Thread — Set Threads = 1

WSA memory is per-thread. If "Load Data from File" runs with multiple threads, each thread gets its own empty WSA. The MEC counter breaks — two threads assign the same count.

Before running "Load Data from File":

My Client Groups → Payroll → Payroll Process Configuration → **Threads = 1**

---

## The Complete Formula — All Sections Assembled

Everything from Parts 1, 2, and 3 combined into one formula. OPERATION routing, METADATA, MAP block with WSA caching, GET_VALUE_SET calls, SourceSystemId resolution, LINEREPEATNO passes, and Cancel end-dating. This is the full, working code.

XXTAV_HDL_ACCRUAL_INBOUND — Complete Formula

```text
  1/**************************************************************
  2FORMULA NAME : XXTAV_HDL_ACCRUAL_INBOUND
  3FORMULA TYPE : HCM Data Loader
  4DESCRIPTION  : Transform vendor accrual file into HDL format
  5****************************************************************/
  6
  7/* ═══════════════════════════════════════════════════════════ */
  8/*  INPUTS                                                     */
  9/* ═══════════════════════════════════════════════════════════ */
 10INPUTS ARE OPERATION (TEXT),
 11LINEREPEATNO (NUMBER),
 12LINENO (NUMBER),
 13POSITION1 (TEXT), POSITION2 (TEXT), POSITION3 (TEXT),
 14POSITION4 (TEXT), POSITION5 (TEXT), POSITION6 (TEXT),
 15POSITION7 (TEXT), POSITION8 (TEXT),
 16POSITION9 (TEXT), POSITION10 (TEXT), POSITION11 (TEXT)
 17
 18DEFAULT FOR LINENO IS 1
 19DEFAULT FOR LINEREPEATNO IS 1
 20DEFAULT FOR POSITION1 IS 'NO DATA'
 21DEFAULT FOR POSITION2 IS 'NO DATA'
 22DEFAULT FOR POSITION3 IS 'NO DATA'
 23DEFAULT FOR POSITION4 IS 'NO DATA'
 24DEFAULT FOR POSITION5 IS 'NO DATA'
 25DEFAULT FOR POSITION6 IS 'NO DATA'
 26DEFAULT FOR POSITION7 IS 'NO DATA'
 27DEFAULT FOR POSITION8 IS 'NO DATA'
 28DEFAULT FOR POSITION9 IS 'NO DATA'
 29DEFAULT FOR POSITION10 IS 'NO DATA'
 30DEFAULT FOR POSITION11 IS 'NO DATA'
 31
 32/* ═══════════════════════════════════════════════════════════ */
 33/*  OPERATION ROUTING                                          */
 34/* ═══════════════════════════════════════════════════════════ */
 35IF OPERATION = 'FILETYPE' THEN
 36   OUTPUTVALUE = 'DELIMITED'
 37ELSE IF OPERATION = 'DELIMITER' THEN
 38   OUTPUTVALUE = ','
 39ELSE IF OPERATION = 'READ' THEN
 40   OUTPUTVALUE = 'NONE'
 41ELSE IF OPERATION = 'NUMBEROFBUSINESSOBJECTS' THEN
 42(  OUTPUTVALUE = '2'
 43   RETURN OUTPUTVALUE
 44)
 45
 46/* ═══════════════════════════════════════════════════════════ */
 47/*  METADATA                                                   */
 48/* ═══════════════════════════════════════════════════════════ */
 49ELSE IF OPERATION = 'METADATALINEINFORMATION' THEN
 50(
 51    METADATA1[1] = 'ElementEntry'
 52    METADATA1[2] = 'ElementEntry'
 53    METADATA1[3] = 'LegislativeDataGroupName'
 54    METADATA1[4] = 'EffectiveStartDate'
 55    METADATA1[5] = 'ElementName'
 56    METADATA1[6] = 'AssignmentNumber'
 57    METADATA1[7] = 'CreatorType'
 58    METADATA1[8] = 'EntryType'
 59    METADATA1[9] = 'MultipleEntryCount'
 60    METADATA1[10] = 'SourceSystemOwner'
 61    METADATA1[11] = 'SourceSystemId'
 62    METADATA2[1] = 'ElementEntry'
 63    METADATA2[2] = 'ElementEntryValue'
 64    METADATA2[3] = 'LegislativeDataGroupName'
 65    METADATA2[4] = 'EffectiveStartDate'
 66    METADATA2[5] = 'ElementName'
 67    METADATA2[6] = 'AssignmentNumber'
 68    METADATA2[7] = 'InputValueName'
 69    METADATA2[8] = 'EntryType'
 70    METADATA2[9] = 'MultipleEntryCount'
 71    METADATA2[10] = 'ScreenEntryValue'
 72    METADATA2[11] = 'ElementEntryId(SourceSystemId)'
 73    METADATA2[12] = 'SourceSystemOwner'
 74    METADATA2[13] = 'SourceSystemId'
 75    RETURN METADATA1, METADATA2
 76)
 77
 78/* ═══════════════════════════════════════════════════════════ */
 79/*  MAP BLOCK — Core Transformation                            */
 80/* ═══════════════════════════════════════════════════════════ */
 81ELSE IF OPERATION = 'MAP' THEN
 82(
 83    /* ─── Static values ─── */
 84    l_InputValueName           = 'XXTAV_PTO BALANCE'
 85    l_LegislativeDataGroupName = 'United States LDG'
 86    l_entry_type               = 'E'
 87    l_MultipleEntryCount       = '1'
 88    l_CreatorType              = 'H'
 89
 90    /* ═══════════════════════════════════════════════════════ */
 91    /*  WSA: Person + Assignment Number (Performance Cache)    */
 92    /* ═══════════════════════════════════════════════════════ */
 93    l_wsa_per_key = 'PER_' || POSITION4 || '_' || POSITION3
 94    l_wsa_asg_key = 'ASG_' || POSITION4 || '_' || POSITION3
 95
 96    IF WSA_EXISTS(l_wsa_per_key) THEN
 97    (
 98        /* HIT — read from cache */
 99        L_PersonNumber     = WSA_GET(l_wsa_per_key, ' ')
100        l_AssignmentNumber = WSA_GET(l_wsa_asg_key, ' ')
101    )
102    ELSE
103    (
104        /* MISS — call database, then cache */
105        l_AssignmentNumber = GET_VALUE_SET(
106            'XXTAV_GET_LATEST_ASSIGNMENT_NUMBER',
107            '|=P_PERSON_NUMBER=''' || POSITION4 || ''''
108         || '|P_EFFECTIVE_START_DATE='''
109         || TO_CHAR(TO_DATE(POSITION3,'YYYY-MM-DD'),'YYYY-MM-DD')
110         || '''')
111        L_PersonNumber = POSITION4
112
113        WSA_SET(l_wsa_per_key, L_PersonNumber)
114        WSA_SET(l_wsa_asg_key, l_AssignmentNumber)
115    )
116
117    /* ─── GET_VALUE_SET: Element Name ─── */
118    l_ElementName = GET_VALUE_SET(
119        'XXTAV_ACCRUAL_ELEMENTS TEST',
120        '|=P_PAY_CODE=''' || TRIM(POSITION2) || '''')
121
122    /* ═══════════════════════════════════════════════════════ */
123    /*  WSA: MultipleEntryCount (Correctness — Mandatory)      */
124    /* ═══════════════════════════════════════════════════════ */
125    l_wsa_mec_key = 'MEC_' || L_PersonNumber || '_'
126                 || l_ElementName || '_' || POSITION3
127
128    IF WSA_EXISTS(l_wsa_mec_key) THEN
129    (
130        /* Previous row already assigned a count — increment */
131        l_MultipleEntryCount = TO_CHAR(
132            TO_NUMBER(WSA_GET(l_wsa_mec_key, '0')) + 1)
133    )
134    ELSE
135    (
136        /* First row for this combo — ask the database */
137        l_db_max = GET_VALUE_SET(
138            'XXTAV_MAX_MULTI_ENTRY_COUNT',
139            '|=P_PERSON_NUMBER=''' || POSITION4 || ''''
140         || '|P_EFFECTIVE_START_DATE='''
141         || TO_CHAR(TO_DATE(POSITION3,'YYYY/MM/DD'),'YYYY-MM-DD')
142         || ''''
143         || '|P_ELEMENT_NAME=''' || l_ElementName || '''')
144
145        IF ISNULL(l_db_max) = 'N' THEN
146            l_MultipleEntryCount = '1'
147        ELSE
148            l_MultipleEntryCount = TO_CHAR(
149                TO_NUMBER(l_db_max) + 1)
150    )
151
152    /* Save MEC to WSA — next row reads this, not the stale DB */
153    WSA_SET(l_wsa_mec_key, l_MultipleEntryCount)
154
155    /* ─── SourceSystemId: Lookup or Construct ─── */
156    l_SourceSystemId = GET_VALUE_SET(
157        'XXTAV_GET_ELEMENT_ENTRY_SOURCE_SYSTEM_ID',
158        '|=P_PERSON_NUMBER=''' || POSITION4 || ''''
159     || '|P_EFFECTIVE_START_DATE='''
160     || TO_CHAR(TO_DATE(POSITION3,'YYYY-MM-DD'),'YYYY-MM-DD')
161     || ''''
162     || '|P_ELEMENT_NAME=''' || l_ElementName || '''')
163    l_SourceSystemOwner = GET_VALUE_SET(
164        'XXTAV_GET_ELEMENT_ENTRY_SOURCE_SYSTEM_OWNER',
165        '|=P_PERSON_NUMBER=''' || POSITION4 || ''''
166     || '|P_EFFECTIVE_START_DATE='''
167     || TO_CHAR(TO_DATE(POSITION3,'YYYY-MM-DD'),'YYYY-MM-DD')
168     || ''''
169     || '|P_ELEMENT_NAME=''' || l_ElementName || '''')
170
171    /* ─── EEV SourceSystemId ─── */
172    l_EEV_SourceSystemId = GET_VALUE_SET(
173        'XXTAV_GET_ELEMENT_ENTRY_VALUE_SOURCE_SYSTEM_ID',
174        '|=P_PERSON_NUMBER=''' || POSITION4 || ''''
175     || '|P_EFFECTIVE_START_DATE='''
176     || TO_CHAR(TO_DATE(POSITION3,'YYYY-MM-DD'),'YYYY-MM-DD')
177     || ''''
178     || '|P_ELEMENT_NAME=''' || l_ElementName || ''''
179     || '|P_INPUT_VALUE_NAME=''' || l_InputValueName || '''')
180    l_EEV_SourceSystemOwner = GET_VALUE_SET(
181        'XXTAV_GET_ELEMENT_ENTRY_VALUE_SOURCE_SYSTEM_OWNER',
182        '|=P_PERSON_NUMBER=''' || POSITION4 || ''''
183     || '|P_EFFECTIVE_START_DATE='''
184     || TO_CHAR(TO_DATE(POSITION3,'YYYY-MM-DD'),'YYYY-MM-DD')
185     || ''''
186     || '|P_ELEMENT_NAME=''' || l_ElementName || ''''
187     || '|P_INPUT_VALUE_NAME=''' || l_InputValueName || '''')
188
189    /* ─── Construct if not found ─── */
190    IF ISNULL(l_SourceSystemId) = 'N' THEN
191    (   l_SourceSystemId = 'XXTAV_HDL' || l_AssignmentNumber
192            || '_EE_' || POSITION4 || '_' || POSITION2
193            || '_' || POSITION3   )
194    IF ISNULL(l_EEV_SourceSystemId) = 'N' THEN
195    (   l_EEV_SourceSystemId = 'XXTAV_HDL' || l_AssignmentNumber
196            || '_EEV_' || POSITION4 || '_' || POSITION2
197            || '_' || POSITION3   )
198    IF ISNULL(l_SourceSystemOwner) = 'N' THEN
199    (   l_SourceSystemOwner = 'XXTAV_HDL'   )
200    IF ISNULL(l_EEV_SourceSystemOwner) = 'N' THEN
201    (   l_EEV_SourceSystemOwner = 'XXTAV_HDL'   )
202
203    /* ═══════════════════════════════════════════════════════ */
204    /*  LINEREPEATNO = 1 — ElementEntry header                 */
205    /* ═══════════════════════════════════════════════════════ */
206    IF LINEREPEATNO = 1 THEN
207    (
208        FileName                 = 'ElementEntry'
209        BusinessOperation        = 'MERGE'
210        FileDiscriminator        = 'ElementEntry'
211        LegislativeDataGroupName = l_LegislativeDataGroupName
212        AssignmentNumber         = l_AssignmentNumber
213        ElementName              = l_ElementName
214        EffectiveStartDate       = TO_CHAR(TO_DATE(POSITION3,'YYYY-MM-DD'),'YYYY/MM/DD')
215        MultipleEntryCount       = l_MultipleEntryCount
216        EntryType                = l_entry_type
217        CreatorType              = l_CreatorType
218        SourceSystemOwner        = l_SourceSystemOwner
219        SourceSystemId           = l_SourceSystemId
220        LINEREPEAT               = 'Y'
221
222        IF ISNULL(l_ElementName) = 'N' THEN
223        (   RETURN LINEREPEAT, LINEREPEATNO   )
224        ELSE
225        (   RETURN BusinessOperation, FileName, FileDiscriminator,
226                   MultipleEntryCount, CreatorType,
227                   EffectiveStartDate, ElementName,
228                   LegislativeDataGroupName, EntryType,
229                   AssignmentNumber, SourceSystemOwner,
230                   SourceSystemId,
231                   LINEREPEAT, LINEREPEATNO   )
232    )
233
234    /* ═══════════════════════════════════════════════════════ */
235    /*  LINEREPEATNO = 2 — ElementEntryValue (amount)          */
236    /* ═══════════════════════════════════════════════════════ */
237    ELSE IF (LINEREPEATNO = 2) THEN
238    (
239        l_ScreenEntryValue = RTRIM(RTRIM(TRIM(POSITION6),'0'),'.')
240
241        IF ISNULL(l_ScreenEntryValue) = 'N' THEN
242        (   l_ScreenEntryValue = '0'   )
243
244        FileName              = 'ElementEntry'
245        BusinessOperation     = 'MERGE'
246        FileDiscriminator     = 'ElementEntryValue'
247        AssignmentNumber      = l_AssignmentNumber
248        LegislativeDataGroupName = l_LegislativeDataGroupName
249        ElementName           = l_ElementName
250        EntryType             = l_entry_type
251        EffectiveStartDate    = TO_CHAR(TO_DATE(POSITION3,'YYYY-MM-DD'),'YYYY/MM/DD')
252        MultipleEntryCount    = l_MultipleEntryCount
253        SourceSystemId        = l_EEV_SourceSystemId
254        SourceSystemOwner     = l_EEV_SourceSystemOwner
255        InputValueName        = l_InputValueName
256        ScreenEntryValue      = l_ScreenEntryValue
257        LINEREPEAT            = 'N'
258
259        IF ISNULL(l_ElementName) = 'N' THEN
260        (   RETURN LINEREPEAT, LINEREPEATNO   )
261        ELSE
262        (   RETURN BusinessOperation, FileName, FileDiscriminator,
263                   AssignmentNumber, EffectiveStartDate,
264                   ElementName, EntryType,
265                   LegislativeDataGroupName, MultipleEntryCount,
266                   InputValueName, ScreenEntryValue,
267                   SourceSystemOwner, SourceSystemId,
268                   LINEREPEAT, LINEREPEATNO   )
269    )
270)
271ELSE
272   OUTPUTVALUE = 'NONE'
273RETURN OUTPUTVALUE
274/* End Formula Text */
```

---

## Series Complete

That's all three parts.

**Part 1** gave you the mental model — what each section of the formula does and why. **Part 2** walked through the code line by line — GET_VALUE_SET syntax, ISNULL patterns, SourceSystemId logic, ESS_LOG_WRITE debugging, LINEREPEATNO passes. **Part 3** added WSA caching and assembled the complete formula.

You should now be able to read any HDL Transformation Formula, understand every line, and build your own by adapting the code above to your vendor file layout and value set definitions.

Part 1: Pure Concepts

→

Part 2: Code Walkthrough

→

Part 3: WSA + Complete Formula ← This post

Abhishek Mohanty
