# Synthetic company example: bounded reporting service

**SYNTHETIC FIXTURE ONLY.** Every business, person, order, decision, receipt and date below is fictional and intentionally supplied in this file. No customer was contacted, no payment occurred, and no company was formed. The example demonstrates how to reason from evidence; it provides no live business validation. Dollar amounts are USD. Dates use DD-MM-YYYY.

## Commission and position

Fixture company `Sample Reporting Service` offers one fixed-scope cleanup of a customer's permitted, nonsensitive order export. A fictional human founder, `Sample Founder`, is accountable and owns the working records. The fictional customer and payer is `Sample Shop`. The user is its operations lead.

The offer is USD 600 for a cleaned CSV and a reconciliation note, delivered within three business days after complete inputs. Acceptance requires unique order IDs, normalized amounts, an explicit exception list, and a total reconciling to the valid unique input rows. The customer remains responsible for underlying transactions and decisions. The offer excludes personal data, payment execution, tax advice, accounting assurance and ongoing system access. Failed acceptance receives one scoped correction; inability to meet scope triggers the agreed refund. These terms are fixture facts, not recommended legal terms.

The initial sales route is one incoming inquiry from the fictional shop's operations lead. The concrete ask is acceptance of one USD 600 fixed-scope job; the metric is one ordered, accepted and paid job within the predeclared seven-day horizon. Sample Founder owns the reply and commercial decision. The assistant is authorized only to prepare the local sample and draft proposal. The fixture assumes the founder handles the reply and signing; it supplies no authority for the assistant to send a message or prospect for more customers. An incoming lead proves no scalable acquisition channel.

Minimum requirements are limited to this offer: read the two declared input fields; normalize IDs and explicit USD amounts; detect exact versus conflicting duplicates; produce the clean CSV and reconciliation; and preserve only the permitted input/output needed for acceptance and recovery. Each input row must resolve to one retained row, a documented identical duplicate or an explicit unresolved exception. A conflicting duplicate, unreadable amount, absent field, unsupported data permission or unreconciled total fails acceptance and holds delivery. These requirements are checked on the artifact below, without a separate product requirements document.

File 03 would hold this adopted position and its dated decision reference. File 00 would link this brief, source register, cash schedule and output. File 09 would contain the material open questions below. File 10 would retain the supplied decisions and gate outcomes. The example keeps those views together because separate duplicated files add no value here.

## Supplied evidence excerpts

The following excerpts are the entire evidence available to this example. Do not infer any additional transaction, interview, qualification or jurisdiction finding.

| ID | Date and type | Exact evidence supplied in the fixture | Establishes and limits |
|---|---|---|---|
| S1 | 01-10-2026, incoming customer inquiry | Operations lead: "I spend six hours correcting order exports each month. Can you help? I can accept a clean file if IDs are unique and its total reconciles." | One incoming lead, reported problem and acceptance preference. It does not verify time saved, willingness to pay or scalable acquisition. |
| S2 | 01-10-2026, founder decision | Sample Founder adopts the offer above and authorizes the operator to prepare and check a local sample only, with six hours of work. The founder will handle any customer contact, contract or payment. | A bounded preparation mandate. It grants the assistant no outreach, signing, upload or payment authority. |
| S3 | 02-10-2026, fictional accepted order | Sample Shop orders the stated cleanup for USD 600 under the exact acceptance and refund terms above; Sample Founder signs within the fixture. | Commitment for one job only. It does not prove collection, acceptance or repeat demand. |
| S4 | 03-10-2026, fictional delivery record | Customer's permitted input contains the rows below. Operator records six delivery hours, USD 60 vendor cost and USD 18 processing cost, all paid. | Inputs and actual cost/time for this fixture cycle. It does not establish costs at scale. |
| S5 | 03-10-2026, fictional customer acceptance | Operations lead: "Accepted. Three unique orders, USD 600 total, one duplicate removed, no unresolved exceptions." | Acceptance of this deliverable. It does not prove six hours saved or wider usefulness. |
| S6 | 03-10-2026, fictional payment evidence | Receipt matches the USD 600 invoice and unrestricted business cash account entry. Received USD 600; paid processing fee USD 18 is separately in S4; no refund paid or due at this snapshot. | This one collected payment, with gross versus fee treatment explicit. No claim about future collections. |
| S7 | 04-10-2026, founder operating decision | Sample Founder approves only a next-cycle internal plan: 20 available delivery hours per monthly period, USD 1,500 cash floor, no new spend/contact authority. Beginning unrestricted cash is USD 2,000. Fixed cash costs are USD 250 each period and initial setup is USD 200. | Planning constraints and stated cash inputs. Period 1 amounts are supplied fixture actuals; later periods remain assumptions. |
| S8 | 04-10-2026, scoped issue check | Fixture premise: a current qualified review and the customer's data owner have resolved the necessary permission, contract, registration and tax questions for this exact nonsensitive service and location. No live advice or jurisdiction is supplied. Expansion, personal data and new markets require a new review. | A synthetic prerequisite solely for exercising the successful path. It is not portable legal clearance or a basis for a real company to operate. |

For live work, S6 would require readable payment evidence reconciled to the actual transaction, and S8 would need the actual scoped source/advice and permissions. A founder assertion that these exist would not substitute for them.

## Delivered artifact within the fixture

The agreed normalization trims outer whitespace, parses explicit USD amounts to two decimals, and removes a repeated order ID only when every normalized field matches. Conflicting duplicates would be exceptions held for the customer's ruling; they would not be silently deleted.

Input:

```csv
order_id,amount_usd
O-001,100.00
 O-002 ,200
O-002,200.00
O-003,300.00
```

Accepted output:

```csv
order_id,amount_usd
O-001,100.00
O-002,200.00
O-003,300.00
```

Reconciliation note: four input rows; one identical normalized duplicate excluded; three unique output rows; input row sum USD 800; duplicate adjustment USD 200; output total USD 600; unresolved exceptions zero. This is the sample artifact S5 accepts. It verifies the stated data transformation, not the underlying economic validity of the orders.

## Predeclared test and gate decisions

On 01-10-2026, the fictional founder fixed the test before seeing the result: within seven days, this identified payer orders one USD 600 job, the first job satisfies the listed acceptance tests within six delivery hours, direct variable costs do not exceed USD 100, and payment is evidenced. Hold the affected commitment if input permissions, refund obligations or scoped activity requirements are unresolved. Stop or amend the offer if no order arrives within the horizon; retain the observed failure if criteria change.

| Gate | Evidence and outcome |
|---|---|
| Frame | S1 and S2 establish a narrow problem, offer, owner and permitted sample. Proceed with local preparation only. |
| Test | S3 establishes one commercial commitment against the original threshold. Proceed to the fictional founder-authorized delivery, with collection still unresolved until S6. |
| Deliver | The sample artifact, S4 and S5 establish acceptance at six hours and USD 78 variable cost. S8 supplies the scoped prerequisite for this synthetic path. Proceed for this completed delivery; do not infer authority for a new live delivery. |
| Operate | S6 establishes exchange; S7 and the cash assumptions support a bounded next-cycle plan, subject to collection and capacity limits. MVC is demonstrated **inside this fixture for this one service cycle only**. Repeat demand and scale remain unproven. |

The real kit's status is unchanged by this table. All gate outcomes are fictional fixture outcomes.

## Economics and cash

[service-cash.csv](service-cash.csv) is a complete synthetic input schedule in chronological row order. Each period is one month; Period 1 is supplied fixture actuals, Period 2 and Period 3 are planning assumptions. The basis is S4, S6 and S7 plus these explicit assumptions: one job delivered in each later period at USD 600; each costs USD 78 and six founder hours; the Period 2 invoice collects in Period 3, alongside Period 3's invoice; no financing or refunds; USD 100 tax payment in Period 3 as a planning input, not a calculated tax liability. All costs and obligations assumed for this bounded fixture are included; real use must discover its own omissions.

| Calculation | Result and meaning |
|---|---|
| Unit contribution | USD 600 earned revenue - USD 78 variable incurred cost = USD 522 per delivered job. Margin is 87%. Fixed cost, tax and unpaid founder labor are excluded from this contribution. |
| Founder time | Six hours per job out of 20 available delivery hours in each period = 30% utilization. Spare hours do not establish additional demand or prove costs scale linearly. |
| Optional economic labor view | At an explicitly assumed USD 30/hour opportunity cost, unpaid founder time is USD 180 per job; contribution after that imputed cost is USD 342, or 57%. This imputation is not a cash payment. |
| Period 1 cash | USD 2,000 + USD 600 - USD 78 - USD 250 - USD 200 = USD 2,072 closing cash. |
| Period 2 cash | USD 2,072 + USD 0 - USD 78 - USD 250 = USD 1,744 closing cash, despite USD 600 earned revenue. |
| Period 3 cash | USD 1,744 + USD 1,200 - USD 78 - USD 250 - USD 100 = USD 2,516 closing cash. |
| Cash-floor margin | Minimum closing cash is USD 1,744, USD 244 above the USD 1,500 floor. A floor is not an additional cost. |
| Collection stress | If all Period 3 receipts slip beyond the horizon while the planned delivery costs remain payable, Period 3 closing cash is USD 1,316, USD 184 below the floor. Hold additional discretionary commitments and resolve collection/timing before extending the plan. This does not authorize sending a collection message or obtaining finance. |

Positive contribution and a positive closing balance do not establish accounting profit or unrestricted ability to spend. The floor stress is a concrete reason to revisit terms or scope. Read the complete helper output and its limits if using `setup/company.py cash`; an exit status never supplies the underlying business evidence.

## Next-cycle procedure and unresolved questions

1. The human owner confirms the next order, permitted inputs, applicable scope and action authority. Reuse existing explicit authorization where valid.
2. The operator validates the input fields and duplicates, prepares the cleaned file and reconciliation, and checks acceptance against the actual output.
3. The authorized delivery owner shares only the permitted artifact and retains acceptance or failure evidence. A failed check is corrected within scope or referred to the named refund decision owner.
4. Reconcile the invoice, gross receipt, fee, refunds and delivery costs. Update the relevant cash periods and actual founder hours; compare against the floor and available capacity.
5. Continue only the next authorized cycle. Hold on a permission gap, conflicting duplicate, unresolved acceptance dispute, unaffordable obligation or cash-floor breach. Preserve the result and receipt before retrying an interrupted external action.

Open question E1: will any customer buy again? Evidence needed: a new independently observed order and fulfilled exchange, not an intention stated after delivery. Open question A1: will the assumed Period 2 and 3 invoices collect on the forecast dates? Evidence needed: actual terms, due dates and reconciled receipts. Open question D1: will a materially larger or messier file fit six hours? Evidence needed: scoped delivery data from that workload.

The fixture ends with a completed sample cycle, a feasible but collection-sensitive plan, and explicit unknowns. It does not create a deck, company departments or a claim that the same service will work in reality.
