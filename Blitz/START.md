# Start with Blitz

**Minimum Viable Company kit**

Listen, collect, sprint.<br>
Reduce cycle time.

Build one bounded company or department operating cycle: a useful result delivered and accepted, its exchange or resource use reconciled, and an accountable owner with a feasible next cycle. Preparation alone does not demonstrate operation. Aim for one or two days when scope, inputs, people and permissions allow; external cycles may take longer. No ARR, demand or profitability is guaranteed.

Before use, check the [license eligibility and permission terms](setup/licensing/LICENSE) and [component exceptions](setup/licensing/NOTICE.md). Public availability does not grant every use. Keep applicable notices and credit with your authorized copy.

## Choose your starting point

| Company | Department |
|---|---|
| Name one customer/user, payer and accountable owner. | Name one internal user, accepting stakeholder, sponsor and accountable owner. |
| Define a bounded offer, price hypothesis, delivery promise and next test. | Define a bounded internal service, intake route, acceptance and next test. |
| Bound time, cash obligations and delivery capacity. | Establish who may commit budget and people; bound resource use and obligations. |
| Test observed customer/payer behavior, then deliver and obtain acceptance. | Test actual user/sponsor need, then deliver and obtain the agreed acceptance. |
| Reconcile actual exchange, cash timing and obligations; assess the next cycle. | Reconcile authorized budget, actual spend/resource use and obligations; assess the next cycle. An allocation is not revenue. |

At each gate, the human owner records **Proceed, Hold or Walk** for the specific next commitment using evidence and existing authority. Missing permission holds the affected action. Forming a company, making payments, outreach, signing, filing and account changes need their own authority. Identify relevant jurisdiction-specific legal, tax or licensing questions before affected commitments; this kit does not determine compliance.

## Read only what you need

Start with this page and the [company and department profile](profiles/company.md). When using an assistant, also supply the short [operating contract](setup/operating-contract.md). The 25 methods, source compiler and host staging are optional advanced routes; you do not need them all to begin.

Keep useful state in existing records, or use the [brief](templates/company-brief.md) and four core records: **00 Read Me First**, **03 Position Of Record**, **09 Open Questions**, **10 Decision Log**. Preserve these names. Record source locations/owner/next action in 00, adopted positions in 03, consequential gaps in 09 and actual rulings in 10. Do not create paperwork without a decision or recovery need. Keep filled records outside the source kit with one canonical writer.

For a fictional practice workspace, use Python 3.12+ from the parent of the extracted `Blitz/` directory:

```sh
python -B Blitz/setup/verify_kit.py
python -B Blitz/setup/company.py init --out company-practice --name "Practice company" --owner "Example owner"
```

The output must be new and its parent must exist. The initializer creates seven unadopted, company-oriented drafts. For a department, adapt the brief to the right-hand column above and change record 00's `venture` type before adoption; use existing resource records or [Economics and Budget][budget]. The CLI does not allocate staff or budgets. You can fill the templates manually instead.

Company cash check:

```sh
python -B Blitz/setup/company.py cash company-practice/company-cash.csv
```

Blank inputs intentionally produce **incomplete**, exit 2. Unknown is not zero. The command calculates supplied commercial cash inputs; it does not verify their truth or prove readiness. Departments should not enter allocations as customer receipts. See the [release guide](setup/release-guide.md) for complete examples, exit codes and limitations.

## Use an assistant with explicit sources

Give the assistant readable copies of the named kit files and only authorized records. Replace the brackets before use:

```text
Use Blitz for [company OR department] and this bounded task: [outcome].
Read the supplied Blitz/START.md, Blitz/profiles/company.md and
Blitz/setup/operating-contract.md, then these authorized records: [exact files].
Confirm which files you could actually read. Missing source bytes are a gap;
do not reconstruct them from a filename, prior chat or an index.
Prepare [first offer/service and smallest useful test] with evidence,
assumptions, acceptance/stop criteria, time/cash/resource caps and an owner.
Keep consequential commitments for the named human decision maker.
Use an optional method only if needed; read its full instructions and required
resources, report missing tools, and do not install skills or alter settings.
Save only to [authorized working directory], preserve existing records, then
reopen the result and identify the next permitted action and unresolved gaps.
```

Close and reopen your work. Another authorized operator should recover the offer/service, owner, evidence, obligations, next action and stop conditions. Test one real scoped cycle before claiming a demonstrated MVC; test repetition before expansion. Here autoscale means repeat and expand with evidence, capacity and authority, not autonomous infrastructure scaling.

## When you need more

- [Skills guide](setup/skills-guide.md): choose a relevant method and inspect its dependencies.
- [Source use](setup/source-use.md) and [runtime preparation](setup/runtime.md): optional generated sources, no native installation.
- [Release guide](setup/release-guide.md): verification, migration and rollback. Never overwrite filled records with an initializer or upgrade.
- [Item export](setup/item-export.md): commissioned, allowlisted handoff; it grants no disclosure or receiving-host authority.

[budget]: templates/context/04%20Economics%20And%20Budget.md
