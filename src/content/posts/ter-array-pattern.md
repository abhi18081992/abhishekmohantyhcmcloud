---
title: "An array-processing pattern for Time Entry Rule validation formulas"
description: "How I structure TER validation formulas in Taiwan and other APAC implementations so that the same skeleton handles single-day and bulk submissions cleanly."
pubDate: 2026-03-22
module: "Time and Labor"
tags: ["Fast Formula", "Time and Labor", "Taiwan", "TER", "APAC"]
---

When you write a **Time Entry Rule (TER)** validation formula in Oracle Time and Labor, the input you receive is not a single time card row — it is an array of measures keyed by attribute. The first time you write one, the temptation is to treat it like a payroll formula: pull a couple of named inputs, do a comparison, return a message. That works for the simplest cases. It falls apart the second a user submits a week of entries and you need to validate each row independently.

The skeleton below is the one I now reach for by default on Taiwan TER work, and it has held up across half a dozen day-type variants.

## The skeleton

```text
/* ============================================
   Time Entry Rule — Validation
   Author : Abhishek Mohanty
   ============================================ */

INPUTS ARE
  MEASURES        (text_array),
  DAY_OF_WEEK     (text),
  ASSIGNMENT_ID   (number)

l_idx        = 1
l_count      = MEASURES.COUNT
l_error_msg  = ' '
l_error_flag = 'N'

WHILE l_idx <= l_count LOOP
(
  l_measure = MEASURES(l_idx)

  /* ---- per-row validation goes here ---- */
  IF l_measure > 24 THEN
  (
    l_error_flag = 'Y'
    l_error_msg  = 'Row ' || TO_CHAR(l_idx)
                 || ' exceeds 24 hours.'
  )

  l_idx = l_idx + 1
)

IF l_error_flag = 'Y' THEN
(
  RETURN_VALUE = 'ERROR'
  RETURN_MESSAGE = l_error_msg
)
ELSE
(
  RETURN_VALUE = 'SUCCESS'
  RETURN_MESSAGE = ' '
)

RETURN RETURN_VALUE, RETURN_MESSAGE
```

## Why I like it

Three things that this skeleton gets right, that I've watched other versions get wrong:

1. **It walks the array explicitly with an index**, instead of relying on a single named input. You'd be amazed how often the "single named input" version of a TER formula passes UAT and then breaks the first time a user submits two days at once.
2. **The error message carries the row index.** When the validation fires, the user sees "Row 3 exceeds 24 hours" rather than a generic "invalid time entry" — which dramatically cuts the support load.
3. **The success path returns a space, not a null.** Empty strings in Fast Formula message returns are a perennial source of "why did the validation pass but no message show" tickets. Just return a space.

## Things I learned the hard way

A few notes I wish I had on day one:

- **Debug logging in TER formulas uses `ADD_RLOG`**, not `ESS_LOG_WRITE`. The contexts you'll want set are `HWM_FFS_ID` and `HWM_RULE_ID` — both are populated automatically by the calling process, you just need to read them.
- **Don't initialize `MEASURES` with a `DEFAULT FOR` statement.** The compiler will accept it, the formula will run, and the array will silently be empty. Pass the array in via `INPUTS ARE` only.
- **The `DAY_OF_WEEK` context is text, not number.** The values are `MONDAY`, `TUESDAY`, etc., uppercase. If you compare against `'Mon'` you will get a hilarious bug where the validation never fires on Mondays.

I'll write up the **Time Calculation Rule (TCR)** variant of this skeleton next — same array shape, different return contract.
