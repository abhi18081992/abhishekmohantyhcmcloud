---
title: "Where to Check Fast Formula Logs — ESS Process Names & Navigation Paths"
description: "A practical guide to finding Fast Formula debug logs in Oracle HCM Cloud — ESS process names, navigation paths, and log locations for Absence, Payroll, Compensation, Benefits and OTL."
pubDate: 2026-03-20
tags: ["Fast Formula", "Debugging", "ESS Logs", "Consolidated Reference"]
---

## Oracle Fast Formula: Where to Check Logs — The One Reference That Should Have Existed Years Ago

You added `ESS_LOG_WRITE` to your formula. You ran the process. Now you're staring at the screen wondering where the output went. This post is for that moment.

Abhishek Mohanty

Every Fast Formula post I've written so far has had `ESS_LOG_WRITE` in the code. And in every post I showed the log output — but I never once explained where I went to *get* that output.

[Roopesh Madan](https://www.linkedin.com/in/roopesh-madan-11b94128/) helped me consolidate this — he sent me a module-by-module breakdown of which logging function works where, which ESS job to run, and where to check the output. That email became the skeleton of this post. Nobody had written the consolidated version. So here it is.

---

## The Full Picture

Scan this first. The details for each module are below.

| Module | ESS Process Names | Where to Check | Prerequisite |
| --- | --- | --- | --- |
| Absence | Calculate Accruals and Balances**Evaluate AbsencesUpdate Accrual Plan Enrollments | Scheduled Processes > Log/Output | "Include trace statements in audit log"** |
| Time & Labor | Timecard Submission**Mass Submit and Approve Time CardsResubmit Time CardsSubmit Queued Time CardsTransfer Time Cards from Time and Labor | Analyze Rule Processing DetailsOr query HWM_RULE_FF_WORK_LOG | None** |
| Payroll | Calculate Payroll**QuickPayCalculate Gross EarningsRecalculate Payroll for Retroactive Changes | Payroll Flow > View ResultsOr Scheduled Processes > Log | Manage Payroll Process Configuration** |
| Compensation | **CWB:** Start Workforce Compensation Cycle**Refresh Workforce Compensation DataTransfer / Back OutTCS:** Generate Total Compensation Statements | **CWB:** Monitor Process > Child Process > ESS_L_xxxxx**TCS:** Monitor Processes and Logs > Subprocess > View Log | **CWB: "Include trace statements in the log file"TCS: "Include trace statements in Audit log"** |
| Benefits | Participation Evaluation**Default EnrollmentClose EnrollmentReevaluate Designee EligibilityUpload Benefit Enrollments | Evaluation & Reporting > Monitor Process Request | None** |
| HCM Extract | Run Extract (Data Exchange > Submit Extracts) | Scheduled Processes > Log/Output | **Logging Category Detailed = GMFZT** |
| Talent Mgmt | No ESS — UI-triggered | Query HWM_RULE_FF_WORK_LOG | **ADD_RLOG — test first, not supported for all FF types** |

---

Section 1

## Workforce Management — Absence & Time and Labor

These are the two modules most HCM technical consultants hit first. And they use completely different logging mechanisms.

### Absence Management

**Where to check:** Scheduled Processes > Search for process > **Log/Output** attachment. **Prerequisite:** Enable **"Include trace statements in audit log"** on the submission page. Without this, ESS_LOG_WRITE output is silently dropped. **Entry Validation shortcut:** Set `VALID = 'N'` and put debug values in `ERROR_MESSAGE` — shows on the UI directly, no ESS needed. Remove before production.

| Formula Type | Linked ESS Job |
| --- | --- |
| Global Absence Accrual | Calculate Accruals and Balances |
| Absence Accrual Matrix | Calculate Accruals and Balances |
| Global Absence Carryover | Calculate Accruals and Balances |
| Global Absence Transfer | Calculate Accruals and Balances |
| Global Absence Type Duration | Evaluate Absences |
| Global Absence Entry Validation | Evaluate Absences (also UI-triggered on absence entry) |
| Participation and Rate Eligibility (absence) | Update Accrual Plan Enrollments |

Ref: Oracle Docs — Administering Fast Formulas > Troubleshooting Tips (24B/24D) • Oracle Docs — Absence Processes (R20B)

### Oracle Time and Labor (OTL)

OTL doesn't use `ESS_LOG_WRITE`. It has its own: `ADD_RLOG` and `ADD_LOG`. No prerequisite. **Where to check:** **Workforce Management > Time Management > Analyze Rule Processing Details** > Search by Rule Set Name > Click Timecard Processing ID. Or query `HWM_RULE_FF_WORK_LOG` via SQL/OTBI.

| Formula Type | Linked ESS Job |
| --- | --- |
| Workforce Management Time Entry Rules | Timecard Submission / Mass Submit and Approve Time Cards |
| Workforce Management Time Calculation Rules | Timecard Submission / Resubmit Time Cards |
| Workforce Management Time Submission Rules | Submit Queued Time Cards / Mass Submit |
| Workforce Management Time Device Event Rules | Generate Time Cards from Time Collection Device |

Ref: Oracle Docs — Using Time and Labor > Scheduled Processes (20C) • tilak-lakshmi.blogspot.com — "How to Debug a Fast Formula"

---

Section 2

## Payroll & Compensation

Both of these run batch processes and both have specific prerequisites you need to enable before logging will work.

### Payroll

Payroll has the most involved logging setup. **Where to check:** Payroll Flow > View Results > Log/Output. Or Scheduled Processes > Log. **Prerequisite:** **Manage Payroll Process Configuration** (My Client Groups > Payroll > Payroll Process Configuration) > Group Overrides > Create group > Add **Logging Category** = `F` and **Formula Execution Logging** = `i`. Select group when submitting. Remove after testing. **QuickPay gotcha:** QuickPay doesn't accept a group — must use **Default Group**. Profile option `ACTION_PARAMETER_GROUPS` controls the default.

| Formula Type | Linked ESS Job |
| --- | --- |
| Payroll Calculation (element formulas) | Calculate Payroll / QuickPay |
| Proration | Calculate Payroll / QuickPay |
| Element Skip | Calculate Payroll / QuickPay |
| Payroll Formula Result Rules | Calculate Payroll / QuickPay |
| Balance Adjustment | Calculate Payroll |
| Gross Earnings calculation formulas | Calculate Gross Earnings |
| Retroactive Proration / Retro component formulas | Recalculate Payroll for Retroactive Changes |

Ref: Oracle Docs — Logging Processing Parameters • Oracle Docs — Payroll Process Configuration Groups (24D) • MOS Doc ID 1559909.1

### Compensation (CWB / TCS / GSP)

Compensation has two different log paths depending on whether you're running Workforce Compensation (CWB) or Total Compensation Statements (TCS).

**CWB (Workforce Compensation):** Compensation > Run Batch Process > **Monitor Process** > Hierarchy ON > **Child Process** > scroll to bottom > `ESS_L_xxxxx` attachment (some releases: "View Log" button). **Prerequisite:** Enable **"Include trace statements in the log file"** on cycle start.

**TCS (Total Compensation Statements):** The TCS Monitor page (*Monitor Total Compensation Statement Processes*) does **not** show formula logs — that's a known limitation. To see logs: click **"Monitor Processes and Logs"** (top right of TCS Monitor page) > takes you to **Manage Scheduled Processes** > find **"Generate Total Compensation Statements: Subprocess"** entries > click **View Log**. **Prerequisite:** Check **"Include trace statements in Audit log"** on the Generate Statements submission page.

**Gotcha:** Compensation Default & Override formulas also fire from the worksheet UI — no ESS log there. Use `ADD_RLOG` and query `HWM_RULE_FF_WORK_LOG` for those (see ADD_RLOG note at the end).

| Formula Type | Linked ESS Job |
| --- | --- |
| Compensation Default and Override | Start Workforce Compensation Cycle / Refresh (also UI-triggered) |
| Compensation Person Selection | Start Workforce Compensation Cycle |
| Compensation Currency Selection | Start Workforce Compensation Cycle |
| Compensation Hierarchy Determination | Start Workforce Compensation Cycle |
| Compensation Start Date | Transfer Workforce Compensation Data to HR |
| Total Compensation Item (TCS) | Generate Total Compensation Statements |
| Participation and Rate Eligibility (TCS) | Generate Total Compensation Statements |
| Compensation Person Selection (TCS) | Generate Total Compensation Statements |

Ref: Oracle Docs — Plan Validation & Starting Workforce Compensation Cycle (24C) • Oracle Docs — Implementing Compensation (25A) • tilak-lakshmi.blogspot.com — "Fast Formula – Compensation Example"

---

Section 3

## Benefits & HCM Extract

### Benefits

Processes run from **Evaluation and Reporting** work area. **Where to check:** Evaluation & Reporting > **Monitor Process Request**. Also check Scheduled Processes for ESS log. **No prerequisite** for ESS_LOG_WRITE. **Formula Tab:** Evaluation & Reporting has a Formula Tab to test a benefits FF for a sample participant without changing data — can't test runtime-dependent FFs like Rate Periodization.

| Formula Type | Linked ESS Job |
| --- | --- |
| Participation and Rate Eligibility | Participation Evaluation |
| Coverage / Rate Determination | Default Enrollment |
| Certification Required | Participation Evaluation |
| Post Election Edit | Close Enrollment |
| Rate Periodization | Participation Evaluation / Default Enrollment |

Ref: Oracle Docs — Manage Benefits Processing and Uploads (R20B) • Benefits Fast Formula Reference Guide (MOS 1456985.1)

### HCM Extract

**Where to check:** Scheduled Processes > Extract run > Download Log. **Prerequisite — GMFZT:** Manage Payroll Process Configuration > **Default Group** tab > "+" > **Logging Category Detailed** = `GMFZT`. Remove after testing — impacts performance. **Known issue:** ESS_LOG_WRITE may produce blank output in Extract Rule FFs — regenerate the extract (Refine HCM Extracts > Select > Generate).

| Formula Type | Linked ESS Job |
| --- | --- |
| Extract Rule | Run Extract (Data Exchange > Submit Extracts) |
| Extract Criteria | Run Extract |
| Extract Advanced Condition | Run Extract |
| Extract Record | Run Extract |

Ref: Oracle Docs — HCM Extracts • fusionhcmknowledgebase.com — "Configure GMFZT Logging for HCM Extract" • Cloud Customer Connect — "Extract Rule FF has debug ess_log_write"

---

Section 4

## Talent Management & A Note on ADD_RLOG

### Talent Management (Performance, Goals, Checklist)

No ESS process. UI-triggered — the formula fires when a manager calculates ratings in a performance document or when a checklist task is evaluated. **ESS_LOG_WRITE does nothing here.** Community blogs report `ADD_RLOG(-123456, seq, 'message')` works for Performance Rating and Checklist formulas — but test it for your specific formula type first.

Ref: Oracle Docs — "How You Use Fast Formulas in Performance Documents" (24D) • iavinash.com — "How to Debug Any Oracle Fast Formula Like a Pro" • fusionhcmforest.com — "Debugging Fast Formula when logs are not generating"

### A Note on ADD_RLOG

`ADD_RLOG` is an OTL function that writes to `HWM_RULE_FF_WORK_LOG`. Community blogs call it a "universal debugger" — but that's not entirely accurate. **It works for many formula types, but not all.**

**Confirmed to work:** OTL formulas (native), Compensation Default and Validation, Checklist, HCM Extract Rule, Performance Rating Calculation. **Reported NOT working:** Participation and Rate Eligibility (Benefits) — per Cloud Customer Connect (May 2025). Oracle has never officially documented ADD_RLOG as a cross-module function.

**Bottom line:** If ESS_LOG_WRITE doesn't work and you want to try ADD_RLOG — test it. If the formula compiles and logs appear in `HWM_RULE_FF_WORK_LOG`, you're good. If not, it's not supported for that formula type.

Ref: Cloud Customer Connect — "How to enable Logging in Fast formulas" (May 2025) • apps2fusion.com — Ashish Harbhajanka

---

Hope this helps.

### Abhishek Mohanty
