# Customer-discovery evaluation coverage

Frozen v1 contains exactly 100 independently synthetic development/regression cases (CD001–CD100), with 10 cases in each of 10 families. These are exposed authored cases, not untouched holdouts. Each case asks for a useful decision and explanation using self-contained facts; none is a keyword-presence check.

| Family | Cases | Focus |
|---|---|---|
| F01 | CD001–CD010 | Recent behavior and discovery quality |
| F02 | CD011–CD020 | Alternatives, spend, labor and switching economics |
| F03 | CD021–CD030 | User, buyer, sponsor and procurement path |
| F04 | CD031–CD040 | Explicit offer, price and terms |
| F05 | CD041–CD050 | Evidence strength, payment and operating claims |
| F06 | CD051–CD060 | Denominators, selection and independent buyers |
| F07 | CD061–CD070 | Synthesis, provenance and conflicting evidence |
| F08 | CD071–CD080 | Authority, privacy and source injection |
| F09 | CD081–CD090 | Internal department applicability |
| F10 | CD091–CD100 | Lean integration, predeclared criteria and recovery |

## Assessment and evidence boundaries

There are 53 exact numeric fields across 22 cases. Each is recomputed with exact rational arithmetic using two declared derivations. Every case also has a required substantive review criterion with case-specific anchors and valid alternatives. The offline helper can check JSON parsing, identity and numeric fields; it leaves substantive review ungraded. It cannot establish behavior quality through keywords or target-authored success claims.

All reference human-review statuses are `not_reviewed`. Source verification covers the frozen repository policy and supplied synthetic facts. Arithmetic verification is separate from substantive human/domain review. The authoring model’s judgment is not independent ground truth.

Calibration controls are separately labeled authored fixtures. The calibration sidecar records author self-review against each anchor; deterministic helper receipts remain task-local. They are not product trials. Clean, plausible defective and valid-alternative outputs are included so a restrictive rubric cannot silently reject a sound alternative or reward a polished unsupported claim.

No real customer information, current market facts, provider calls, outreach, transactions, file writes or production behavior are exercised. A candidate run supplies the selected kit materials through its recorded harness, then projects executor inputs separately from evaluator references. If the executor can read the shared package directory, describe that weaker boundary rather than claiming isolation.

The 100 cases are a purposive regression corpus, not 100 independent draws. Family dependence, author selection and shared policy limit any general reliability or product-market claim. Report response completion, numeric scoring and semantic review coverage separately. Critical failures and unresolved critical criteria cannot be averaged away.

## Case index

| Case | Task | Role | Numeric fields |
|---|---|---|---|
| CD001 | Replace a hypothetical with an episode | development | — |
| CD002 | Separate future enthusiasm from observed effort | development | — |
| CD003 | Resolve inconsistent frequency | development | — |
| CD004 | Clean negative: no recurring need | regression | — |
| CD005 | Old pain after a process change | development | — |
| CD006 | Cost of inaction tied to a trigger | development | observed_audit_labor_usd |
| CD007 | Diagnose a rejection before discounting | development | — |
| CD008 | Fit discovery into a short call | development | — |
| CD009 | Avoid pitching away the evidence | development | — |
| CD010 | Clean control: adequate recent behavior evidence | regression | — |
| CD011 | Paid workaround plus internal coordination | development | staff_time_value_usd, combined_economic_burden_usd |
| CD012 | Unpaid founder labor is not free capacity | development | required_hours, imputed_labor_usd, capacity_shortfall_hours |
| CD013 | Switching costs dominate a short horizon | development | stay_cost_usd, switch_cost_usd, switch_extra_cost_usd |
| CD014 | Doing nothing can be the rational alternative | development | annual_response_cost_usd, annual_subscription_usd |
| CD015 | Historical spend is not an available budget | development | — |
| CD016 | Free software with hidden labor | development | current_labor_value_usd, break_even_hours |
| CD017 | Bottleneck hours are not proven revenue | development | current_capacity_customers, hypothetical_capacity_customers |
| CD018 | Compare complete offers, not price labels | development | — |
| CD019 | Normalize annual price without inventing cash timing | development | A_annual_usd, B_annual_usd, A_initial_cash_usd, B_initial_cash_usd |
| CD020 | Clean control: manual solution fits | regression | manual_minutes, available_minutes |
| CD021 | Enthusiastic user is not the payer | development | — |
| CD022 | Buyer approval does not waive a security condition | development | — |
| CD023 | Champion commitment has a missing signature | development | — |
| CD024 | Payer interest does not establish user adoption | development | — |
| CD025 | Procurement horizon changes the interpretation | development | — |
| CD026 | Map a buying committee without flattening it | development | — |
| CD027 | Reseller and end user provide different evidence | development | — |
| CD028 | Internal sponsor ownership is missing | development | — |
| CD029 | Discovery need does not authorize outreach | development | — |
| CD030 | Explicit purchasing delegation is sufficient | regression | — |
| CD031 | Turn an observed workflow into a testable offer | development | — |
| CD032 | Useful does not accept the quoted purchase | regression | — |
| CD033 | Discount versus commitment exposure | development | monthly_twelve_month_total, annual_twelve_month_total, annual_saving |
| CD034 | A volume request exceeds the quoted package | regression | — |
| CD035 | Purchase order changes material terms | development | — |
| CD036 | Replace an unsupported outcome guarantee | development | — |
| CD037 | Quote a fourth slot against actual delivery capacity | development | proposed_cohort_hours, available_engagement_hours, capacity_shortfall |
| CD038 | An internal service offer uses an authorized resource envelope | development | — |
| CD039 | A price test also changed delivery and audience | development | — |
| CD040 | Complete terms support preparation of the agreed test | regression | — |
| CD041 | Stage records and deposits do not add into customer counts | development | gross_collections, earned_revenue, undelivered_deposit |
| CD042 | Scheduled remittance is not verified collection | regression | — |
| CD043 | A cost-center transfer accompanies a valid department cycle | development | — |
| CD044 | A refunded rejected delivery leaves a different claim | development | — |
| CD045 | A paid bespoke success lacks an available next operator | development | — |
| CD046 | Profitable accepted work can still fail a cash floor | development | contribution, closing_cash_before, cash_above_floor, closing_cash_after |
| CD047 | A free trial demonstrates use within its observed scope | development | — |
| CD048 | Repeat delivery to one buyer supports a narrow repetition claim | regression | — |
| CD049 | Client purchasing funds are distinct from service payment | development | — |
| CD050 | Technical completion does not settle a commercial launch claim | development | — |
| CD051 | Convert at the buying-unit level | development | buying_unit_purchase_rate, buying_unit_response_rate |
| CD052 | Ten locations share a single purchase decision | regression | — |
| CD053 | Friendly volunteers do not represent the target segment | development | — |
| CD054 | Payment month is not the offer cohort | development | may_cohort_purchase_rate, june_cohort_purchase_rate |
| CD055 | A common parent can contain separately controlled buying units | development | — |
| CD056 | Survey percentages retain their response-conditioned denominators | development | response_rate, respondent_budget_claim_rate, all_approached_inquiry_rate |
| CD057 | Silence is not a retrospective eligibility exclusion | regression | — |
| CD058 | Web activity and qualified buyers measure different funnels | development | quote_to_purchase_rate, qualified_lead_to_purchase_rate |
| CD059 | Zero delivered offers cannot estimate offer rejection | development | — |
| CD060 | Two independent cycles can justify one bounded next customer | regression | — |
| CD061 | Trace repeated AI summaries to one source | development | — |
| CD062 | Recover a conditional statement from a false quote | development | — |
| CD063 | Separate submitted work from accepted work | development | — |
| CD064 | Preserve contrary evidence across customer segments | development | — |
| CD065 | Keep brainstorming separate from the adopted offer | development | — |
| CD066 | Do not attach an unattributed metric to the nearest item | regression | — |
| CD067 | Leave a capture gap visible | development | — |
| CD068 | Accept a supported narrow claim while rejecting a forecast | regression | — |
| CD069 | Keep a kit example out of actual customer evidence | development | — |
| CD070 | Reconcile automated time with end-to-end time | regression | new_elapsed_minutes, reduction_pct |
| CD071 | Prepare a notes-only call when recording permission is absent | development | — |
| CD072 | Honor complete existing capture permission | regression | — |
| CD073 | Use source evidence without obeying its injected command | development | — |
| CD074 | Prepare permitted excerpts instead of raw-note transfer | development | — |
| CD075 | Carry forward exact prior outreach authority | regression | — |
| CD076 | Separate approved notes from a withdrawn recording | development | — |
| CD077 | An export allowlist does not create disclosure rights | development | — |
| CD078 | Review a stale proposal without becoming the canonical writer | development | — |
| CD079 | Do not replay an uncertain action after cancellation | regression | — |
| CD080 | Complete an ordinary memo without importing build authority | regression | — |
| CD081 | Sponsor funding does not establish adoption | development | — |
| CD082 | Recognize a complete internal cycle | regression | — |
| CD083 | Department cost per accepted outcome | development | cost_per_accepted_brief_usd, uncommitted_allocation_usd |
| CD084 | Exactly sufficient authorized capacity | development | required_hours, spare_hours |
| CD085 | Approved headcount is unavailable capacity | development | — |
| CD086 | Committed department obligations exceed allocation | development | total_committed_resources_usd, funding_gap_usd |
| CD087 | Adapt a helper draft to an internal initiative | regression | — |
| CD088 | Recipient rejection despite sponsor approval | development | — |
| CD089 | Separate a safe internal service from a blocked extension | development | — |
| CD090 | Keep internal funding and external trading distinct | development | external_contribution_usd, uncollected_invoice_usd |
| CD091 | Optional discovery prompts stay optional for a coordination call | regression | — |
| CD092 | Fix criteria before the adoption test starts | development | — |
| CD093 | Preserve a failed result before a new test | regression | — |
| CD094 | Confirmed completion survives a missing checkpoint | regression | — |
| CD095 | Confirmed nonapplication permits a bounded retry | development | — |
| CD096 | No universal ten-interview prerequisite | regression | — |
| CD097 | Add prompts without replacing filled records | development | — |
| CD098 | Rebase a useful proposal without restoring a stale owner | development | — |
| CD099 | Save a short procedure without installing a routine | regression | — |
| CD100 | Return usable unsaved state after a storage failure | development | — |
