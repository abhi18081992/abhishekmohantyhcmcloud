---
title: "Why ESS_LOG_WRITE breaks Global Absence Carryover formulas in 26A"
description: "A short note on a compilation error that bit me in a Malaysia carryover formula, and the debug pattern I switched to instead."
pubDate: 2026-04-08
module: "Absence Management"
tags: ["Fast Formula", "Absence Management", "Debug Logging", "Release 26A", "Malaysia"]
---

If you've recently upgraded to **Release 26A** and your **Global Absence Carryover** formulas have suddenly stopped compiling, the chances are very good that the culprit is a stray `ESS_LOG_WRITE` call you put in for debugging during build. This one cost me an afternoon on a Malaysia carryover formula, so I'm writing it down.

## What the error looks like

The compilation message is unhelpful — something to the effect of *"function ESS_LOG_WRITE not defined for this formula type"* — and on first read it sounds like a missing package or a bad import. It is neither. The function genuinely does not exist for the **Global Absence Carryover** formula type from 26A onwards, even though the same call works happily in **Global Absence Plan Use Rate**, **Global Absence Entry Validation**, and most of the other Absence formula types you'll touch on the same project.

## Why this is annoying

The whole reason most of us reach for `ESS_LOG_WRITE` in Absence formulas is that it's the one debug channel Oracle gives you that survives the ESS request log. So when it's quietly removed from one specific formula type, the natural reaction is to start sprinkling more `ESS_LOG_WRITE` calls to figure out what's going on — which makes the compilation error worse, not better.

## The pattern I switched to

In Carryover formulas I now use a **debug flag pattern** driven by a UDT row, and I emit the values into a context variable that I read back from the calling process log. The skeleton looks like this:

```text
/* ============================================
   Global Absence Carryover — Malaysia
   Author : Abhishek Mohanty
   Notes  : 26A-safe debug, no ESS_LOG_WRITE
   ============================================ */

DEFAULT FOR PER_PERSON_ID                IS 0
DEFAULT FOR IV_ACCRUAL                   IS 0
DEFAULT FOR IV_CEILING                   IS 0
DEFAULT FOR IV_CARRYOVER_LIMIT           IS 0

INPUTS ARE IV_ACCRUAL, IV_CEILING, IV_CARRYOVER_LIMIT

/* ---- debug flag from a UDT row, default OFF ---- */
l_debug = GET_VALUE_SET(
  'XX_HCM_DEBUG_FLAG_VS',
  '|=FORMULA_NAME='''
  || 'XX_MY_CARRYOVER_FF'
  || ''''
)

IF l_debug = 'Y' THEN
(
  /* park the trace into a context the parent process picks up */
  l_trace = 'IV_ACCRUAL=' || TO_CHAR(IV_ACCRUAL)
            || '|IV_CEILING=' || TO_CHAR(IV_CEILING)
            || '|LIMIT=' || TO_CHAR(IV_CARRYOVER_LIMIT)
)
ELSE
(
  l_trace = ' '
)

l_carryover = LEAST(IV_ACCRUAL, IV_CARRYOVER_LIMIT)

RETURN l_carryover
```

A few things worth flagging in the snippet above:

1. **`GET_VALUE_SET` always returns text.** If you're comparing the result against a number you need to wrap it in `TO_NUMBER`. For a `Y/N` debug flag it's fine to leave it as text.
2. **`IV_ACCRUAL` is the matrix accrual rate**, not the net year-end balance. I keep tripping over this, because the intuitive read of "accrual" is "what the employee earned this year". It is not. Treat it as a rate.
3. The trace string is deliberately built into a single delimited line. When you eventually pull it out of the parent ESS log, a delimited string is much easier to grep and split than multi-line output.

## What I should have done from the start

In hindsight the lesson is the older one: in any formula type that runs inside an ESS-scheduled process, **don't reach for `ESS_LOG_WRITE` as your first debug tool**. Use a debug flag from a UDT, build your trace into a string, and emit it through a return path that survives the formula type's compile contract. That way a release upgrade in some random formula type can't take your whole carryover offline.

> If you're still on 25D or earlier and your Carryover formulas use `ESS_LOG_WRITE`, this is the one to refactor *before* you take the 26A upgrade in the test environment. Do not wait to be surprised.

I'll add a Philippines and a Hong Kong variant of this skeleton in a follow-up post.
