---
title: "Oracle Recruiting Cloud Fast Formulas — The Complete Guide"
description: "Every CSP (Candidate Selection Process) Fast Formula type in Oracle Recruiting Cloud, with worked examples for scoring, routing and validation."
pubDate: 2026-04-02
tags: ["Fast Formula", "Recruiting", "CSP", "DBIs"]
---

Oracle Fast Formula: The Complete Guide to Recruiting CSP Formulas

DBIs, Contexts, Value Sets, Array Indexing, Debugging Patterns, and Production-Ready Code

Abhishek Mohanty

Oracle HCM Cloud Consultant — Fast Formulas, Absence, Recruiting, Core HR, Redwood, HDL, OTBI

Recruiting CSP formulas are powerful — but the documentation is scattered. This post is the reference I wished I had. Every DBI, every context, every code pattern — in one place.

What CSP Formulas Can Do

CSP formulas are the automation engine behind Oracle Recruiting Cloud. They evaluate conditions at every stage of the candidate journey and decide what happens next.

| Capability | What It Does | Key DBI / Function |
| --- | --- | --- |
| Auto-Move Candidates | Automatically advance or route candidates between phases and states when formula returns Y. No recruiter action needed. | Action Condition on CSP state |
| Gate Manual Moves | Block recruiters from manually moving a candidate until the formula returns Y. Used for compliance gates. | Move Condition on CSP state |
| Geography Routing | Route candidates into different CSP paths based on requisition location, country, or geography hierarchy level. | IS_REQ_BELOW_IN_GEO_HIERARCHY |
| Prescreening Validation | Check specific answers to prescreening questions. Auto-disqualify or fast-track candidates based on responses. | IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_ANSWER_CODE[] |
| Candidate Type Detection | Distinguish internal vs external candidates. Detect ex-employees via Value Sets querying SYSTEM_PERSON_TYPE. | IRC_CSP_JOBAPP_INTERNAL, GET_VALUE_SET |
| Assessment Gate | Hold candidates until all assessment partners return a passing result. Block on fail or pending. | IRC_CSP_ASSMNT_PACKAGE_CODE[] |
| Request Info Validation | Block progression until the candidate completes a Request for Information flow. | IRC_CSP_REQUEST_INFO_STATUS_CODE |
| Interview Completion | React to interview events (scheduled, completed, cancelled). Auto-advance when interviews finish. | GET_CONTEXT(IRC_INTRVW_OPERATION) |
| Openings Control | Stop processing when all positions on a requisition are filled. | IRC_CSP_REQ_NUMBER_TO_HIRE, IRC_CSP_REQUISITION_NUMBER_OF_HIRES |
| Computed Fields | Calculate values displayed in job application grid views and Extra Info tab. Value stored via CONDITION_MESSAGE into Extensible Flexfields. | Formula type: Recruiting Job Application Computed Field |

Every formula follows the same skeleton: read DBIs and context, run your logic, return **Y** (condition met) or **N** (skip). The rest of this post shows you how to build each of these patterns.

The Skeleton

Formula type: `Recruiting Candidate Selection Process`. Return `CONDITION_RESULT` with Y to indicate the condition is met. Optionally return `CONDITION_MESSAGE` for debugging (max 255 chars).

1CONDITION_RESULT  = 'N' REQUIRED

2CONDITION_MESSAGE = '' OPTIONAL

3/* your logic goes here */

4RETURN CONDITION_RESULT, CONDITION_MESSAGE RETURN

| **Step 1**   **Candidate Applies** — job application created with a unique SUBMISSION_ID |
| --- |
|  |
| **Step 2**   **Enters Phase & State** — lands on a CSP state with an action configured |
|  |
| **Step 3**   **Fast Formula Evaluates** — ESS job runs the formula, checks CONDITION_RESULT |
|  |
| **Y →**   **Action fires** — candidate moves, notification sends, assessment triggers |
| **N →**   **Action skipped** — candidate stays, nothing happens |

DBI + Context — How the Formula Gets Its Data

**DBI** = a named variable that reads from Oracle's database. **Context** = tells the engine *which record* to fetch. You never write SQL in the formula.

| Trigger | Candidate applies → Job Application **45678** created |
| --- | --- |
| Context | Oracle auto-sets **SUBMISSION_ID = 45678**. Every DBI resolves from this value. |
| DBIs Load | All DBIs populate — business unit, internal flag, assessments, prescreening answers, requisition details. |
| Result | Formula evaluates and returns **Y** or **N**. |

1/* SUBMISSION_ID — the job application ID */

2/* Oracle sets it auto. All DBIs chain from this. */

3l_sub_id = GET_CONTEXT(SUBMISSION_ID, 0) CONTEXT

4/* Force English for consistent string matching */

5CHANGE_CONTEXTS(LANGUAGE = 'US') LOCALE

6l_bu = IRC_CSP_REQ_BUSINESS_UNIT_NAME

Exhaustive DBI Reference

Every DBI for `Recruiting CSP` and `Computed Field` formulas across 16 domains. A = Array (use `DBI[i]` + `.EXISTS(i)`), D = Date, N = Number. Source: MOS **2723251.1**, Release 23C.

Job Application — 16

| IRC_CSP_JOBAPP_ACTIVE | Indicates if the job application is active - Y, N |
| --- | --- |
| IRC_CSP_JOBAPP_CAREERSITE_NUMBER | Career site where the job application was submitted - Number |
| IRC_CSP_JOBAPP_CSP_STATE_CODE | Current state of the job application - Code |
| IRC_CSP_JOBAPP_CSP_STATE_NAME | Current state of the job application - Name |
| IRC_CSP_JOBAPP_DISQUALIFIED | Indicates if the job application is disqualified - Y, N |
| D IRC_CSP_JOBAPP_INTERACTION_LAST_DATE | Date of the last interaction entered for the job application |
| IRC_CSP_JOBAPP_INTERNAL | Indicates if the job application is internal - Y, N |
| IRC_CSP_JOBAPP_LANGUAGE_CODE | Language of the job application - Code |
| IRC_CSP_JOBAPP_PHASE_CODE | Current phase of the job application - Code |
| IRC_CSP_JOBAPP_PHASE_NAME | Current phase of the job application - Name |
| N IRC_CSP_JOBAPP_PIPELINE_JOBAPP_ID | Job application on the associated pipeline requisition - Internal ID |
| IRC_CSP_JOBAPP_PRESCREEN_ANSWERED | Indicates if the candidate answered a prescreening questionnaire - Y, N |
| N IRC_CSP_JOBAPP_PRESCREEN_MAX_SCORE | Maximum prescreening score of the questionnaire |
| N IRC_CSP_JOBAPP_PRESCREEN_SCORE | Prescreening score of the job application |
| IRC_CSP_JOBAPP_RESTRICTED | Indicates if the job application is on a restricted phase - Y, N |
| IRC_CSP_JOBAPP_CANDIDATE_TYPE | Candidate type for the candidate applying to the job requisition |

Candidate — 6

| IRC_CSP_CANDIDATE_CITY | City of the candidate |
| --- | --- |
| IRC_CSP_CANDIDATE_COUNTRY | Country of the candidate |
| IRC_CSP_CANDIDATE_DISPLAYNAME | Display name of the candidate |
| IRC_CSP_CANDIDATE_EMAIL | Email address of the candidate |
| IRC_CSP_CANDIDATE_POSTALCODE | Postal code of the candidate |
| IRC_CSP_CANDIDATE_STATE | State of residence of the candidate |

Assessment — 10

| A IRC_CSP_ASSMNT_PACKAGE_CODE | Assessment package - Code |
| --- | --- |
| A IRC_CSP_ASSMNT_PACKAGE_NAME | Assessment package - Name |
| A IRC_CSP_ASSMNT_PACKAGE_STATUS_CODE | Status of the assessment request - Code |
| A IRC_CSP_ASSMNT_PARTNER_NAME | Assessment partner - Name |
| A IRC_CSP_ASSMNT_REQUEST_DATE | Date when the assessment was requested |
| A IRC_CSP_ASSMNT_RESULT_BAND | Result of the assessment - Band |
| A IRC_CSP_ASSMNT_RESULT_COMMENTS | Result of the assessment - Comments |
| A IRC_CSP_ASSMNT_RESULT_PERCENTILE | Result of the assessment - Percentile |
| A IRC_CSP_ASSMNT_RESULT_SCORE | Result of the assessment - Score |
| A IRC_CSP_ASSMNT_TRY_COUNT | Number of times the assessment request was sent |

Answers to Prescreening Questions — 8

| A IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_ANSWER_CODE | Answer provided by the candidate to a prescreening question - Code |
| --- | --- |
| A IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_ANSWER_SCORE | Score for an answer to a prescreening question |
| A IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_QSTN_CODE | Prescreening question answered by the candidate - Code |
| A IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_QSTN_SCORE | Score obtained by the candidate for a prescreening question |
| A IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_QSTN_VERSION | Prescreening question answered by the candidate - Version |
| A IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_QSTNR_CODE | Prescreening questionnaire answered by the candidate - Code |
| A IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_QSTNR_VERSION | Prescreening questionnaire answered by the candidate - Version |
| A IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_TEXT | Text provided by the candidate to answer a prescreening question |

Answers to Request for Information Questions — 7

| A IRC_CSP_JOBAPP_RIF_RESPONSE_ANSWER_CODE | Answer provided by the candidate to a request information flow question - Code |
| --- | --- |
| A IRC_CSP_JOBAPP_RIF_RESPONSE_ANSWER_SCORE | Score for an answer to a request information flow question |
| A IRC_CSP_JOBAPP_RIF_RESPONSE_QSTN_CODE | Request information flow question answered by the candidate - Code |
| A IRC_CSP_JOBAPP_RIF_RESPONSE_QSTN_VERSION | Request information flow question answered by the candidate - Version |
| A IRC_CSP_JOBAPP_RIF_RESPONSE_QSTNR_CODE | Request information questionnaire answered by the candidate - Code |
| A IRC_CSP_JOBAPP_RIF_RESPONSE_QSTNR_VERSION | Prescreening questionnaire answered by the candidate - Version |
| A IRC_CSP_JOBAPP_RIF_RESPONSE_TEXT | Text provided by the candidate to answer a request information flow questio |

Background Check — 8

| IRC_CSP_BGCHECK_COMMENTS | Result of the background check - Comments |
| --- | --- |
| IRC_CSP_BGCHECK_ERROR | Error received for the background check |
| IRC_CSP_BGCHECK_PARTNER_NAME | Background check partner - Name |
| IRC_CSP_BGCHECK_PARTNER_NAME | Overall status of the background check - Code |
| IRC_CSP_BGCHECK_PKG_CODE | Background check package - Code |
| IRC_CSP_BGCHECK_PKG_ERROR | Error received for the background check request |
| IRC_CSP_BGCHECK_PKG_NAME | Background check package - Name |
| IRC_CSP_BGCHECK_PKG_STATUS_CODE | Status of the background check request - Code |

EFFs on Job Applications — 1

| A IRC_CSP_JOBAPP_ATTRIBUTE_PEI_INFORMATION_CATEGORY | Context of the attribute |
| --- | --- |

+ 3 DFF/attribute range DBIs: PEI_INFORMATION ranges

Interview Feedback — 5

| A IRC_CSP_INTFEEDBACK_QUESTIONNAIRE_CODE | Questionnaire used for the interview feedback request - Code |
| --- | --- |
| A IRC_CSP_INTFEEDBACK_STATUS | Status of the interview feedback request |
| IRC_CSP_INTFEEDBK_QSTNR_NAME | Questionnaire used for the interview feedback request - Name |
| N IRC_CSP_INTFEEDBK_QSTNR_MAX_SCORE | Maximum score of the questionnaire used for the interview feedback request |
| N IRC_CSP_INTFEEDBK_QSTNR_AVG_SCORE | Average score of the questionnaire used for the interview feedback request acros |

Rehire Eligibility — 2

| IRC_CSP_CANDIDATE_REHIRE_ELIGIBLE | Indicates if the candidate is eligible for rehire - Y, N, ORA_NS |
| --- | --- |
| IRC_CSP_CANDIDATE_REHIRE_ELIGIBLE_REASON_CODE | Reason associated to the rehire eligibility - Code |

Request for Information — 3

| A IRC_CSP_REQUEST_INFO_APPFLOW_CODE | Application flow used for the request for information - Code |
| --- | --- |
| A IRC_CSP_REQUEST_INFO_APPFLOW_VERSION_NAME | Application flow used for the request for information - Version Name |
| A IRC_CSP_REQUEST_INFO_STATUS_CODE | Status of the request for information - Code |

Requisition — 65

| IRC_CSP_REQ_APPLY_WHEN_NOT_POSTED | Indicates if candidates can apply to the requisition when not posted - Y, N |
| --- | --- |
| IRC_CSP_REQ_ATTRIBUTE_CATEGORY | Context of the attribute |
| IRC_CSP_REQ_BUDGET_CURRENCY_CODE | Budget currency of the requisition - Code |
| IRC_CSP_REQ_BUSINESS_UNIT_NAME | Business unit of the requisition - Code |
| D IRC_CSP_REQ_CREATION_DATE | Creation date of the requisition |
| IRC_CSP_REQ_DEPARTMENT_NAME | Department of the requisition - Code |
| N IRC_CSP_REQ_EMPLOYEE_REFERRAL_BONUS | Employee referral bonus of the requisition |
| IRC_CSP_REQ_FULL_PART_TIME | Full time or part time value of the requisition |
| IRC_CSP_REQ_GRADE_CODE | Grade of the requisition - Code |
| IRC_CSP_REQ_JOB_CODE | Job of the requisition - Code |
| IRC_CSP_REQ_JOB_FAMILY_CODE | Job family of the requisition - Code |
| IRC_CSP_REQ_JOB_FUNCTION_CODE | Job function of the requisition - Code |
| IRC_CSP_REQ_JOB_SHIFT_CODE | Job shift of the requisition - Code |
| IRC_CSP_REQ_JOB_TYPE_CODE | Job type of the requisition - Code |
| IRC_CSP_REQ_JUSTIFICATION_CODE | Justification of the requisition - Code |
| IRC_CSP_REQ_LEGAL_EMPLOYER_NAME | Legal employer of the requisition - Code |
| A IRC_CSP_REQ_LOCATION_OTH_CODE | Other locations of the requisition - Codes |
| A IRC_CSP_REQ_LOCATION_OTH_GEOGRAPHY_TYPE | Geography types of the other locations of the requisition |
| A IRC_CSP_REQ_LOCATION_OTH_NAME | Other locations of the requisition - Names |
| IRC_CSP_REQ_LOCATION_PRIM_CODE | Primary location of the requisition - Primary code |
| IRC_CSP_REQ_LOCATION_PRIM_GEOGRAPHY_TYPE | Geography type of the primary location of the requisition |
| IRC_CSP_REQ_LOCATION_PRIM_NAME | Primary location of the requisition - Name |
| IRC_CSP_REQ_MANAGEMENT_LEVEL | Management level of the requisition |
| N IRC_CSP_REQ_MAX_SALARY | Maximum salary of the requisition |
| N IRC_CSP_REQ_MIN_SALARY | Minimum salary of the requisition |
| IRC_CSP_REQ_NUMBER | Number of the requisition |
| N IRC_CSP_REQ_NUMBER_TO_HIRE | Number of openings of the requisition |
| IRC_CSP_REQ_ORGANIZATION_NAME | Organization of the requisition - Name |
| IRC_CSP_REQ_PHASE_CODE | Current phase of the requisition - Code |
| IRC_CSP_REQ_PHASE_NAME | Current phase of the requisition - Name |
| IRC_CSP_REQ_PIPELINE | Indicates if the requisition is a pipeline requisition - Y, N |
| IRC_CSP_REQ_POSITION_CODE | Position of the requisition - Code |
| IRC_CSP_REQ_POSITION_JOB_CODE | Job associated to the position of the requisition - Code |
| IRC_CSP_REQ_POSTING_EXT_STATUS | Posting status of the requisition on external career sites |
| IRC_CSP_REQ_POSTING_INT_STATUS | Posting status of the requisition on internal career sites |
| IRC_CSP_REQ_RECRUITING_TYPE_CODE | Recruiting type of the requisition - Code |
| IRC_CSP_REQ_REGULAR_TEMPORARY | Regular or temporary value of the requisition |
| N IRC_CSP_REQ_RELOCATION_BUDGET | Relocation budget of the requisition |
| IRC_CSP_REQ_SALARY_CURRENCY_CODE | Compensation currency of the requisition - Code |
| IRC_CSP_REQ_SALARY_FREQUENCY_CODE | Pay frequency of the requisition - Code |
| N IRC_CSP_REQ_SOURCING_BUDGET | Sourcing budget of the requisition |
| IRC_CSP_REQ_STATE_CODE | Current state of the requisition - Code |
| IRC_CSP_REQ_STATE_NAME | Current state of the requisition - Name |
| IRC_CSP_REQ_STUDY_LEVEL_CODE | Education level of the requisition - Code |
| IRC_CSP_REQ_TEMPLATE_CODE | Requisition template of the requisition - Code |
| N IRC_CSP_REQ_TRAVEL_BUDGET | Travel budget of the requisition |
| IRC_CSP_REQ_UNLIMITED_HIRE | Indicates if the requisition allows an unlimited number of hires - Y, N |
| IRC_CSP_REQ_WORKER_TYPE_CODE | Worker type of the requisition - Code |
| A IRC_CSP_REQ_WORKLOCATION_OTH_CITY | Cities of the other work locations of the requisition |
| A IRC_CSP_REQ_WORKLOCATION_OTH_CODE | Other work locations of the requisition - Codes |
| A IRC_CSP_REQ_WORKLOCATION_OTH_COUNTRY | Countries of the other work locations of the requisition |
| A IRC_CSP_REQ_WORKLOCATION_OTH_COUNTY | Counties of the other work locations of the requisition |
| A IRC_CSP_REQ_WORKLOCATION_OTH_POSTALCODE | Postal codes of the other work locations of the requisition |
| A IRC_CSP_REQ_WORKLOCATION_OTH_PROVINCE | Provinces of the other work locations of the requisition |
| A IRC_CSP_REQ_WORKLOCATION_OTH_STATE | States of the other work locations of the requisition |
| IRC_CSP_REQ_WORKLOCATION_PRIM_CITY | City of the primary work location of the requisition |
| IRC_CSP_REQ_WORKLOCATION_PRIM_CODE | Primary work location of the requisition - Code |
| IRC_CSP_REQ_WORKLOCATION_PRIM_COUNTRY | Country of the primary work location of the requisition |
| IRC_CSP_REQ_WORKLOCATION_PRIM_COUNTY | County of the primary work location of the requisition |
| IRC_CSP_REQ_WORKLOCATION_PRIM_POSTALCODE | Postal code of the primary work location of the requisition |
| IRC_CSP_REQ_WORKLOCATION_PRIM_PROVINCE | Province of the primary work location of the requisition |
| IRC_CSP_REQ_WORKLOCATION_PRIM_STATE | State of the primary work location of the requisition |
| IRC_CSP_REQ_WORKPLACE_TYPE_CODE | Workplace type code in the requisition. |
| IRC_CSP_REQUISITION_DISPLAY_IN_ORG_CHART | Indicates if the requisition is displayed in the organization chart - Y, N |
| N IRC_CSP_REQUISITION_NUMBER_OF_HIRES | Number of hires on the requisition |

+ 70 DFF/attribute range DBIs: ATTRIBUTE_CHAR1-30, ATTRIBUTE_DATE1-10, ATTRIBUTE_NUMBER1-20, ATTRIBUTE_TIMESTAMP1-10

Tax Credit — 24

| A IRC_CSP_TAXCREDIT_OTHER_CREDIT_PACKAGE_CODE | Other tax credit package - Code |
| --- | --- |
| A IRC_CSP_TAXCREDIT_OTHER_CREDIT_PACKAGE_NAME | Other tax credit package - Name |
| A IRC_CSP_TAXCREDIT_OTHER_CREDIT_PACKAGE_STATUS_CODE | Status of the other tax credit request - Code |
| A IRC_CSP_TAXCREDIT_OTHER_CREDIT_PARTNER_NAME | Other tax credit partner - Name |
| A IRC_CSP_TAXCREDIT_PACKAGE_CODE | Tax credit package - Code |
| A IRC_CSP_TAXCREDIT_PACKAGE_NAME | Tax credit package - Name |
| A IRC_CSP_TAXCREDIT_PACKAGE_STATUS_CODE | Status of the tax credit request - Code |
| A IRC_CSP_TAXCREDIT_PARTNER_NAME | Tax credit partner - Name |
| A IRC_CSP_TAXCREDIT_RESULT_COMMENTS | Result of the tax credit request - Comments |
| A IRC_CSP_TAXCREDIT_RESULT_ELIGIBLE | Result of the tax credit request - Eligibility |
| A IRC_CSP_TAXCREDIT_RESULT_ESTIMATE_CURRENCY_CODE | Result of the tax credit request - Currency Code of Estimate |
| A IRC_CSP_TAXCREDIT_RESULT_FEDERAL_CREDIT_ESTIMATE | Result of the tax credit request - Federal Credit Estimate |
| A IRC_CSP_TAXCREDIT_RESULT_FEDERAL_CREDIT_ID | Result of the tax credit request - Federal Credit Identifier |
| A IRC_CSP_TAXCREDIT_RESULT_FEDERAL_ELIGIBLE | Result of the tax credit request - Federal Eligibility |
| A IRC_CSP_TAXCREDIT_RESULT_OTHER_CREDIT_COMMENTS | Result of the other tax credit request - Comments |
| A IRC_CSP_TAXCREDIT_RESULT_OTHER_CREDIT_ELIGIBLE | Result of the tax credit request - Other Credit Eligibility |
| A IRC_CSP_TAXCREDIT_RESULT_OTHER_CREDIT_ESTIMATE | Result of the tax credit request - Other Credit Estimate |
| A IRC_CSP_TAXCREDIT_RESULT_OTHER_CREDIT_ESTIMATE_CURRENCY_CODE | Result of the tax credit request - Currency Code of Other Credit Estimate |
| A IRC_CSP_TAXCREDIT_RESULT_OTHER_CREDIT_ID | Result of the tax credit request - Other Credit Identifier |
| A IRC_CSP_TAXCREDIT_RESULT_OTHER_CREDIT_NAME | Result of the tax credit request - Other Credit Name |
| A IRC_CSP_TAXCREDIT_RESULT_STATE_CREDIT_ESTIMATE | Result of the tax credit request - State Credit Estimate |
| A IRC_CSP_TAXCREDIT_RESULT_STATE_CREDIT_ID | Result of the tax credit request - State Credit Identifier |
| A IRC_CSP_TAXCREDIT_RESULT_STATE_ELIGIBLE | Result of the tax credit request - State Eligibility |
| A IRC_CSP_TAXCREDIT_RESULT_TOTAL_CREDITS_ESTIMATE | Result of the tax credit request - Total Credits Estimate |

Candidate Interview — 24

| A IRC_CSP_INTRVW_END_DATE | End date of the interview |
| --- | --- |
| A IRC_CSP_INTRVW_ID | ID of the interview |
| A IRC_CSP_INTRVW_LOCATION_TYPE | Location type of the interview - Code |
| A IRC_CSP_INTRVW_NUMBER_OF_CANDIDATES | Number of candidates for the interview |
| A IRC_CSP_INTRVW_SCHEDULE_ID | Interview schedule of the interview - ID |
| A IRC_CSP_INTRVW_START_DATE | Start date of the interview |
| A IRC_CSP_INTRVW_STATUS | Status of the interview |
| A IRC_CSP_INTRVWRQST_CREATION_DATE | Creation date of the interview request |
| A IRC_CSP_INTRVWRQST_ID | ID of the interview request |
| A IRC_CSP_INTRVWRQST_INTERVIEW_ID | Interview of the interview request - ID |
| A IRC_CSP_INTRVWRQST_LAST_UPDATE_DATE | Last update date of the interview request |
| A IRC_CSP_INTRVWRQST_RESCHEDULE_COUNT | Number of times the interview was rescheduled |
| A IRC_CSP_INTRVWRQST_RESCHEDULE_REQUESTED | Indicates if a request to reschedule the interview was requested - Y, N |
| A IRC_CSP_INTRVWRQST_SCHEDULE_ID | Interview schedule of the interview request - ID |
| A IRC_CSP_INTRVWRQST_STATUS | Status of the interview request |
| A IRC_CSP_INTRVWSCHED_ID | ID of the interview schedule |
| A IRC_CSP_INTRVWSCHED_LOCATION_TYPE | Location type of the interview schedule - Code |
| A IRC_CSP_INTRVWSCHED_REQUISITION_ID | Requisition of the interview schedule - ID |
| A IRC_CSP_INTRVWSCHED_SCHEDULE_TYPE | Schedule type of the interview schedule - Code |
| A IRC_CSP_INTRVWSCHED_STATUS | Status of the interview schedule |
| A IRC_CSP_INTRVWSCHED_TEMPLATE_ID | Template of the interview schedule - ID |
| A IRC_CSP_INTRVWSCHED_TEMPLATE_TITLE | Template of the interview schedule - Title |
| A IRC_CSP_INTRVWSCHED_TITLE | Title of the interview schedule |

Offer — 1

| IRC_CSP_JOBOFFER_MERGED_FLAG | Indicates if job offer is merged after the accepted offer was a duplicate - Y, N |
| --- | --- |

Candidate Legislative Information — 12 of 81

| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_1 | Candidate legislative information - Gender - Code |
| --- | --- |
| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_10 | Attribute 10 of the candidate legislative information |
| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_11 | Attribute 11 of the candidate legislative information |
| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_12 | Attribute 12 of the candidate legislative information |
| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_13 | Attribute 13 of the candidate legislative information |
| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_14 | Attribute 14 of the candidate legislative information |
| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_15 | Attribute 15 of the candidate legislative information |
| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_16 | Attribute 16 of the candidate legislative information |
| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_17 | Attribute 17 of the candidate legislative information |
| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_18 | Attribute 18 of the candidate legislative information |
| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_19 | Attribute 19 of the candidate legislative information |
| IRC_CANDIDATE_LEGISLATIVE_INFORMATION_ATTRIBUTE_2 | Candidate legislative information - Ethnicity - Code |

+ 69 more DBIs. + 130 DFF/attribute range DBIs: DFF_ATTRIBUTE1-30, DFF_ATTRIBUTE_DATE1-15, DFF_ATTRIBUTE_NUMBER1-20, PER_INFORMATION1-30, PER_INFORMATION_DATE1-15, PER_INFORMATION_NUMBER1-20

Source Tracking — 15 of 53

| N IRC_CSP_JOBAPP_SOURCETRACK_ID | Source tracking record of the job application - Internal ID |
| --- | --- |
| IRC_CSP_JOBAPP_SOURCETRACK_SOURCE_LEVEL | Source level of the source tracking record |
| N IRC_CSP_JOBAPP_SOURCETRACK_DIMENSION_ID | Dimension of the source tracking record - Internal ID |
| IRC_CSP_JOBAPP_SOURCETRACK_CAMPAIGN_NUMBER | Campaign from which the job application was added - Number |
| N IRC_CSP_JOBAPP_SOURCETRACK_REQUISITION_ID | Requisition to which the job application was added - Internal ID |
| N IRC_CSP_JOBAPP_SOURCETRACK_SOURCE_REQUISITION_ID | Requisition from which the job application was added - Internal ID |
| N IRC_CSP_JOBAPP_SOURCETRACK_TOKEN_ID | Validation token of the source tracking record - Internal ID |
| N IRC_CSP_JOBAPP_SOURCETRACK_JOBAPP_ID | Job application of the candidate - Internal ID |
| N IRC_CSP_JOBAPP_SOURCETRACK_PROSPECT_ID | Prospect from which the job application was added - Internal ID |
| N IRC_CSP_JOBAPP_SOURCETRACK_REFERRAL_ID | Referral record of the source tracking record - Internal ID |
| N IRC_CSP_JOBAPP_SOURCETRACK_RECRUITER_ID | Recruiter who added the job application - Internal ID |
| IRC_CSP_JOBAPP_SOURCETRACK_CANDIDATE_NUMBER | Candidate who applied to the requisition - Number |
| N IRC_CSP_JOBAPP_SOURCETRACK_SHARE_ID | Job sharing record of the source tracking record - Internal ID |
| N IRC_CSP_JOBAPP_SOURCETRACK_PARENT_SOURCETRACK_ID | Parent source tracking record - Internal ID |
| D IRC_CSP_JOBAPP_SOURCETRACK_CREATION_DATE | Creation date of the source tracking record |

+ 38 more DBIs. See MOS 2723251.1 for full list.

Array Indexing

| Index | QSTN_CODE | ANSWER_CODE | .EXISTS |
| --- | --- | --- | --- |
| [1] | JAVA_SKILL_LEVEL | EXPERT | TRUE |
| [2] | YEARS_EXPERIENCE | 5_PLUS | TRUE |
| [3] | WILLING_RELOCATE | skipped | TRUE |
| [4] | *end of data — loop stops here* | FALSE |

SCENARIO

Prescreening Answer Check

Check if the candidate answered 'EXPERT' to the JAVA_SKILL_LEVEL question. The trap: ISNULL() won't work because DEFAULT sets a space character.

1

Default the array DBIs

Array DBIs need DEFAULT_DATA_VALUE. The default is a space — this is why ISNULL() fails.

1DEFAULT_DATA_VALUE FOR

2  IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_ANSWER_CODE IS ' '

3DEFAULT_DATA_VALUE FOR

4  IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_QSTN_CODE IS ' '

2

Loop with .EXISTS(i)

Returns TRUE while index i has data. FALSE = loop ends.

1i = 1

2WHILE ...QSTN_CODE.EXISTS(i) LOOP

3(

4    l_q = ...QSTN_CODE[i]

5    l_a = ...ANSWER_CODE[i]

3

Use WAS_DEFAULTED, not ISNULL

WAS_DEFAULTED returns 'N' when real data exists. This is the correct check when DEFAULT set a space.

1    IF (WAS_DEFAULTED(...ANSWER_CODE[i]) = 'N') THEN KEY CHECK

2    (

3        IF (l_q = 'JAVA_SKILL_LEVEL'

4            AND l_a = 'EXPERT') THEN

5            l_found = 'Y'

6    )

7    i = i + 1

8)

4

Return with debug trail

1IF (l_found = 'Y') THEN CONDITION_RESULT = 'Y'

2CONDITION_MESSAGE = 'java='||l_found DEBUG

3RETURN CONDITION_RESULT, CONDITION_MESSAGE RETURN

Interview Contexts

When you configure a CSP action to fire on **Interview Updated**, Oracle doesn't just tell you "something changed." It passes a specific operation value into the formula's context, telling you exactly what happened to the interview. This is not a DBI — you can't reference it like a database item. You read it using GET_CONTEXT.

l_operation = GET_CONTEXT(IRC_INTRVW_OPERATION, 'NONE')

The value returned will be one of the following, depending on what the recruiter or candidate did:

| Operation Value | What Triggered It | Typical Use in Formula |
| --- | --- | --- |
| REQUEST_SENT | Recruiter sent an interview invite to the candidate | Trigger a notification or update a tracking field |
| SCHEDULED | Interview date and time confirmed by both parties | Log the schedule or notify the hiring manager |
| RESCHEDULED | Previously scheduled interview moved to a new date | Track reschedule count via IRC_CSP_INTRVWRQST_RESCHEDULE_COUNT |
| CANCELLED | Interview cancelled by recruiter or candidate | Block auto-advance, flag for recruiter review |
| UPDATED | Any other change to the interview record (catch-all) | Rarely used alone — usually combined with DBI checks |
| COMPLETED | All interviewers have finished — interview is done | Most common — auto-advance candidate to next phase after interview finishes |

In practice, **COMPLETED** is the one you'll use in 90% of interview-based CSP formulas. The typical pattern is: check if the operation is COMPLETED, then optionally verify the feedback score or schedule status using the Interview DBIs before returning Y.

/* Auto-advance only when interview is completed */
l_operation = GET_CONTEXT(IRC_INTRVW_OPERATION, 'NONE')

IF (l_operation = 'COMPLETED') THEN
    CONDITION_RESULT = 'Y'

RETURN CONDITION_RESULT

One important detail — these context values are only available when the CSP action is triggered by an **Interview Updated** event. If your formula is attached to a different trigger (like a manual move or assessment completion), GET_CONTEXT will return the default value you specified.

The GET_VALUE_SET Pattern

When no seeded DBI exists, build a **Table-type Value Set** (Module: Recruiting). Specify FROM, Value Column, and WHERE with bind params like `{PARAMETER.SUBMISSION_ID}`.

FORMULA

GET_CONTEXT

→

GET_VALUE_SET

→

SQL

FROM → WHERE

→

value

SCENARIO

Ex-Employee Routing

Route former employees differently. Value Set queries IRC_SUBMISSIONS for SYSTEM_PERSON_TYPE.

1

Get context + call Value Set

Pipe-equals syntax passes the bind parameter.

1l_sub_id = GET_CONTEXT(SUBMISSION_ID, -1) CONTEXT

2l_person_type = GET_VALUE_SET( VALUE SET

3    'XX_GET_PERSON_TYPE_VS',

4    '|=SUBMISSION_ID=' || TO_CHAR(l_sub_id))

2

Check and return

EX_EMP = ex-employee in Oracle's system person type codes.

1IF (l_person_type = 'EX_EMP') THEN

2    CONDITION_RESULT = 'Y'

3RETURN CONDITION_RESULT, CONDITION_MESSAGE RETURN

Debugging — Two Approaches

CONDITION_MESSAGE

255 char limit · stored in CSP tables

CONDITION_MESSAGE =
  'sub=' || TO_CHAR(l_id)
  || ' result=' || CONDITION_RESULT

add_rlog

Unlimited · writes to HWM_RULE_FF_WORK_LOG

l_msg = add_rlog(1001, 1,
  'Sub=' || TO_CHAR(l_id))

/* SELECT * FROM HWM_RULE_FF_WORK_LOG
   ORDER BY CREATION_DATE DESC */

More Formulas

SCENARIO

All Assessments Passed

Auto-advance only if every assessment returned ORA_COMPLETED_PASS. Any non-PASS blocks the move.

1CONDITION_RESULT = 'Y' OPTIMISTIC

2i = 1

3WHILE IRC_CSP_ASSMNT_PARTNER_NAME.EXISTS(i) LOOP

4(

5    IF (IRC_CSP_ASSMNT_PACKAGE_CODE[i]

6        != 'ORA_COMPLETED_PASS') THEN FAIL CHECK

7        CONDITION_RESULT = 'N'

8    i = i + 1

9)

10RETURN CONDITION_RESULT RETURN

SCENARIO

Request Info Complete

Block progression until Request Info is done.

ORA_TRIGGERED — waiting

ORA_SUBMITTED — done

ORA_NOT_REQUIRED — on file

1l_status = IRC_CSP_REQUEST_INFO_STATUS_CODE

2IF (l_status = 'ORA_SUBMITTED'

3    OR l_status = 'ORA_NOT_REQUIRED') THEN

4    CONDITION_RESULT = 'Y'

5RETURN CONDITION_RESULT RETURN

Things to Know

Works on first phase/state

All DBIs including prescreening and EFF values are available at the very beginning of the CSP.

DBIs are read-only

Writing to a DBI causes a compilation error. Output is always CONDITION_RESULT + CONDITION_MESSAGE.

Destination runs first

Actions on the destination phase/state execute *before* the status updates.

Two ESS Jobs Must Be Running

ESS JOB 1

Perform Recruiting CSP Actions

Evaluates conditions, processes moves.

Every 5-10 min

ESS JOB 2

Send Job Application Notification

Notifications for first phase/state.

Every 5 min

**If either job is not scheduled, formulas and notifications silently do nothing.**

Other types: **Recruiting Job Requisition** (auto-unpost) and **Recruiting Job Application Computed Field** (grid values via CONDITION_MESSAGE + EFF).

Real Formula Walkthrough — Prescreening Answer Validation

This formula loops through all prescreening answers for a job application. If the candidate actually answered at least one question (not just skipped it), the formula returns Y. This is used to auto-advance candidates who completed the prescreening questionnaire.

/* Prescreening Answer Validation
   Returns Y if the candidate answered at least one question.
   Uses WAS_DEFAULTED to distinguish real answers from defaults. */

DEFAULT_DATA_VALUE FOR
  IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_ANSWER_CODE IS ' '
DEFAULT_DATA_VALUE FOR
  IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_QSTN_CODE IS ' '

CONDITION_RESULT  = 'N'
CONDITION_MESSAGE = ''

j = 1
WHILE IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_QSTN_CODE.EXISTS(j) LOOP
(
  IF (WAS_DEFAULTED(IRC_CSP_JOBAPP_PRESCREEN_RESPONSE_ANSWER_CODE[j]) = 'N') THEN
  (
    CONDITION_RESULT = 'Y'
    CONDITION_MESSAGE = 'Prescreen answered at question ' || TO_CHAR(j)
    RETURN CONDITION_RESULT, CONDITION_MESSAGE
  )

  j = j + 1
)

CONDITION_MESSAGE = 'No prescreen response found after ' || TO_CHAR(j - 1) || ' questions'
RETURN CONDITION_RESULT, CONDITION_MESSAGE

### How this formula works

**DEFAULT_DATA_VALUE** — Prescreening DBIs are arrays. When a candidate skips a question, Oracle doesn't leave the field null. It fills it with the default value you specify here (a space character). This is important for how we check the data later.

**WHILE .EXISTS(j) LOOP** — Loops through each prescreening question. Index 1 is the first question, index 2 is the second, and so on. When .EXISTS returns FALSE, we've gone past the last question and the loop ends.

**WAS_DEFAULTED() = 'N'** — This is the key check. WAS_DEFAULTED returns 'Y' if the value came from the DEFAULT (meaning the candidate skipped the question), and 'N' if the value is real data (meaning the candidate actually answered). When it returns 'N', we know we have a genuine response.

**Early RETURN** — The moment we find one valid answer, we return Y immediately and stop. No need to scan the rest. The message tells you exactly which question had the response — useful when a recruiter asks "did the formula actually check the answers?"

**Fallback RETURN** — If the loop finishes without finding any real answer, the formula returns N. The message confirms how many questions were checked, so you can verify the formula ran through the entire questionnaire and didn't exit early by mistake.

---

### Abhishek Mohanty
