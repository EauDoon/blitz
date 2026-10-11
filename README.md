<picture>
  <source media="(prefers-reduced-motion: no-preference)" srcset="docs/assets/blitz-motion.gif">
  <img src="docs/assets/blitz-motion-poster.svg" alt="Blitz. Minimum Viable Company kit. Listen, collect, sprint. Reduce cycle time. Input becomes evidence for a bounded output." width="100%">
</picture>

# Blitz

**Minimum Viable Company kit**

Listen, collect, sprint.  
Reduce cycle time.

Build the smallest company that can make a promise, deliver it, get paid and run the next cycle.

[Verification workflow](https://github.com/EauDoon/blitz/actions/workflows/verify.yml)

Version **v2.1OAI** · Python **3.12+** · Editable records and local tools

Frame → Test → Deliver → Operate. [Static illustration](docs/assets/blitz-motion-poster.svg).

[Start](#first-use) · [Outputs](#what-you-can-make) · [Run a cycle](#run-a-cycle) · [25 skills](#using-the-skills) · [Verification](#verification) · [Rights](#rights-and-distribution)

Blitz is an operating kit for founders and small teams building a **minimum viable company**. It connects the offer, customer evidence, delivery, cash and decision owner in one manageable process. Use it with an editor and a human operator, or give the relevant guide and records to an assistant with appropriate tools.

The aim is a demonstrated customer cycle and a feasible next one. A generated folder, prototype, incorporation or polished business plan is useful preparation; none establishes that a business can operate. One successful cycle also does not establish repeat demand, profitability or product-market fit.

## Who it is for

Use Blitz when you are:

- A founder turning a customer problem into one testable offer.
- An operator checking whether delivery, payment and the next cycle fit together.
- A small team consolidating scattered evidence, responsibilities and decisions.

Start with one owner, one offer and one workstream. Add a document, specialist or tool when the work needs it.

This repository supplies a workflow and utilities. It does not host your business, install autonomous agents, schedule background work, form entities, send outreach, move money or determine legal compliance. A small request can remain a small request; you do not need to complete every template.

## What you can make

| Output | How you produce it | What it is for |
|---|---|---|
| Company brief | Edit the generated `company-brief.md` or its template | Define customer, payer, offer, owner, constraints and next experiment |
| Evidence and decision record | Maintain the four generated `context/` files | Separate adopted positions, unresolved questions and consequential decisions |
| Cash forecast | Fill `company-cash.csv`; run the cash command | Compare earned revenue, collections, costs and the closing cash floor |
| Experiment or delivery record | Use the brief and relevant existing records | Fix criteria, save actual observations and decide the next commitment |
| Specialist work product | Select a relevant packaged skill | Draft a research memo, proposal, workbook, diagram, presentation or review; dependencies vary |
| Scoped handoff | Use the CSV scope or item-export tools | Share selected material with provenance and a clear authority boundary |

The starter creates drafts. You supply evidence, adopt decisions and approve commitments. A skill supplies a method; producing its output also requires suitable tools and inputs.

## First use

Get a working copy using Git:

```sh
git clone https://github.com/EauDoon/blitz.git
cd blitz
```

Or choose **Code → Download ZIP** on GitHub, extract it, and open a terminal in the extracted repository folder. You should see `README.md` and the `Blitz/` directory. If you received the standalone `Blitz_v2.1OAI.zip`, follow its [release guide](Blitz/setup/release-guide.md) instead.

Use **Python 3.12 or later**. The setup, calculation and packaging helpers use the standard library; no package installation is needed for this exercise. Examples use `python`; substitute your verified Python 3 command where necessary. Run commands from the repository root.

First verify the kit and create a fictional practice workspace:

```sh
python -B Blitz/setup/verify_kit.py
python -B -c "from pathlib import Path; Path('.work').mkdir(exist_ok=True)"
python -B Blitz/setup/company.py init --out .work/my-company --name "My company" --owner "Example founder"
```

Initialization emits a JSON receipt and creates seven draft files:

```text
.work/my-company/
  README.md
  company-brief.md
  company-cash.csv
  context/
    00 Read Me First.md
    03 Position Of Record.md
    09 Open Questions.md
    10 Decision Log.md
```

Open the generated brief. Name the customer and payer, bounded offer, initial sales route, minimum delivery requirements, hardest assumption and next permitted experiment. Fix its success, change and stop criteria before observing the result. Use `03` for an actually adopted position, `09` for missing evidence and `10` for consequential decisions. Keep one canonical writer.

Calculate the blank cash template to see how missing inputs behave:

```sh
python -B Blitz/setup/company.py cash .work/my-company/company-cash.csv
```

This intentionally reports **incomplete**, with exit code **2**. Fill supported values and label their sources and assumptions in the brief; enter `0` only when zero is known. Run the complete fictional example next:

```sh
python -B Blitz/setup/company.py cash Blitz/examples/company/service-cash.csv
```

Output directories must be **new**, their parents must exist, and initialization must stay outside the `Blitz/` source kit. Occupied targets and paths containing `..` are rejected. Reuse `.work` but choose a new company directory on another initialization. The practice folder is ignored by Git. Keep real company records outside this source repository, using an explicit absolute output path.

Prefer working manually? Copy the [company brief](Blitz/templates/company-brief.md) and [cash template](Blitz/templates/company-cash.csv), or use sufficient existing records. The [company guide](Blitz/profiles/company.md) and [first-user walkthrough](docs/FIRST_USER.md) explain the next steps without requiring the CLI.

## Workflow

<picture>
  <source media="(max-width: 820px)" srcset="docs/assets/workflow-mobile.svg">
  <img src="docs/assets/workflow.svg" alt="Frame the offer, Test the assumption, Deliver the promise, then Operate the next cycle. At each gate the owner checks evidence and authority, then records Proceed, Hold or Walk. Return to the affected gate when evidence changes." width="100%">
</picture>

The four gates describe **business evidence**, with thresholds proportionate to the next commitment's risk:

| Gate | What you establish | Useful evidence |
|---|---|---|
| **Frame** | A customer, payer, problem, bounded offer, accountable owner and permitted test | Observed problem, clear price/scope, acceptance criteria, time and cash cap |
| **Test** | Whether the hardest assumption survives an actual experiment | Customer behavior against predeclared criteria; distinguish interest, orders and payment |
| **Deliver** | Whether the promised result was delivered and accepted | Actual output, customer acceptance, delivery costs, support and failure/refund route |
| **Operate** | Whether the exchange is reconciled and the next cycle is feasible | Receipts, obligations, contribution, cash timing, capacity, owner and repeatable procedure |

Record **Proceed, Hold or Walk** for the specific next commitment. A Hold pauses the dependent action while useful authorized work continues. Advancing a gate does not grant permission to spend, sign, publish or contact anyone.

These gates are separate from the optional work stages in the [playbook](Blitz/PLAYBOOK.md): Ingestion, Firming, Mandate, Blitzing and Delivering. There is no mandatory 72-hour company deadline. A prepared experiment, a demonstrated MVC and demonstrated repetition are different claims.

## Run a cycle

Use the [synthetic service example](Blitz/examples/company/service-example.md) to practise these steps. Real work needs its own evidence and authority.

1. **Frame one offer.** Fill the brief with the customer, payer, result, price, scope and owner. Identify the hardest assumption. Set the next experiment's success, change and stop criteria, with a time and cash cap.
2. **Test that assumption.** Conduct only the permitted experiment. Save observations and source dates. Separate interest, orders, payment and accepted delivery. Record missing evidence in `09 Open Questions.md`.
3. **Decide the next commitment.** Compare the result with the criteria. Record Proceed, Hold or Walk, its basis and owner in `10 Decision Log.md`. Adopt an actual position in `03 Position Of Record.md`; do not turn an unapproved draft into one.
4. **Deliver within the agreed scope.** Retain the promised result, acceptance evidence, actual costs and failure or refund route. A completed internal artifact alone does not establish customer acceptance.
5. **Check the next operating cycle.** Reconcile collections and obligations. Update the cash forecast, capacity and delivery procedure. A complete cash calculation can still show a shortfall. Decide whether the next cycle is feasible.
6. **Leave recoverable work.** Update `00 Read Me First.md` with the governing records, owner and next permitted action. Close and reopen the records. Another session should recover the position and authority boundary without relying on chat memory.

Move back to the affected gate when evidence changes. Keep the record proportionate: a useful existing document can replace another template.

To work with an assistant, first give it readable access to the kit and a scoped practice folder. A starting request is:

> Read `Blitz/README.md` and `Blitz/profiles/company.md`. Help me frame a fictional fixed-scope reporting service. Produce one draft offer and the smallest useful test. Label assumptions, specify the evidence to collect, and leave consequential actions for human approval. Use a relevant packaged method only when needed, and identify what you read.

Then ask it to review supplied experiment evidence, prepare a delivery checklist or inspect your saved handoff. Confirm the actual files and calculations. Do not treat its completion claim as evidence that an external action happened.

## Worked example

The [synthetic reporting service](Blitz/examples/company/service-example.md) sells one fixed-scope CSV cleanup for **USD 600**. Its supplied fixture includes the incoming inquiry, order, input/output, acceptance and payment. Everything is fictional; the example demonstrates the method, not real customer demand.

Each job incurs USD 78 of variable cost and six founder hours. Contribution is **USD 522**, or **87%**, before fixed costs, tax and unpaid founder labor. The cash schedule makes collection timing visible:

| Monthly period | Earned revenue | Cash collected | Closing cash |
|---|---:|---:|---:|
| 1 | USD 600 | USD 600 | USD 2,072 |
| 2 | USD 600 | USD 0 | USD 1,744 |
| 3 | USD 600 | USD 1,200 | USD 2,516 |

If Period 3 collections slip beyond the forecast horizon, its closing cash falls to **USD 1,316**, **USD 184 below** the founder's USD 1,500 floor. Positive contribution does not remove that funding problem. Read the example for all costs, assumptions and the next-cycle procedure.

The [regulated-activity example](Blitz/examples/company/regulated-hold.md) shows a different result: an options memo and simulation can be complete while a proposed customer-funds activity remains on Hold.

## Using the skills

The kit contains **25 method packages**. The [skills guide](Blitz/setup/skills-guide.md#all-25-packaged-skills) lists every method, its purpose, a fictional example request, expected output and dependencies. Pick a method for a concrete task; you do not need all 25 for every company.

| Your task | Start with | Typical output |
|---|---|---|
| Investigate an offer or compare options | `research-protocol`, `reasoning-core` | Sourced findings, assumptions and a decision basis |
| Make the economics inspectable | `calc-workbook` | An editable calculation workbook, when spreadsheet tools are available |
| Explain or present the work | `my-writing-style`, `diagram-design`, `slide-design` | A draft, diagram or presentation suited to its audience |
| Build a focused web surface | `frontend-taste`, `frontend-mockup`, `frontend-scroll-craft` | Design direction, a mockup or implementation, depending on tools and scope |
| Check a consequential artifact | [gauntlet-verify](https://github.com/EauDoon/gauntlet-verify) | Independent findings and a bounded review result when its review mechanism is available |

### Do they trigger automatically?

**Sometimes, on a host that has discovered the skill. Cloning this repository does not install the methods.**

- **Source use:** ask the assistant to read the relevant `Blitz/skills/<name>/SKILL.md` and its applicable resources. This works only when it can access those files. It is an explicit source workflow.
- **Reference staging or Thor runtime:** the setup tools prepare files and a method index for a host. They do not register native skills. The operator must make those sources available and confirm they can be read.
- **Native host use:** separately install or expose selected methods using that host's supported route, after checking names, existing skills and dependencies. Confirm the host lists the intended version before testing selection.

Each packaged method has a frontmatter description, and all 25 `agents/openai.yaml` files permit implicit invocation. These describe intended selection; they cannot guarantee that a host discovers or chooses the skill. OpenAI documents explicit selection as well as description-based matching. See the [current skill documentation](https://learn.chatgpt.com/docs/build-skills), checked 11 October 2026.

If automatic selection misses, use the host's skill picker or explicit invocation. If it is not installed, request the source directly:

> Read `Blitz/skills/research-protocol/SKILL.md` and its applicable references. Apply it to this fictional customer-research question. State which files you could read and which evidence remains missing.

Staged OpenAI reference names include `calculation-workbook` for `calc-workbook` and `web-design-taste` for `frontend-taste`. `google-slides` requires a host capability check and is skipped by that staging tool. See the [setup and selection guide](Blitz/setup/skills-guide.md) before relying on aliases or tools.

This release makes no measured automatic-selection claim for Blitz. Package validation, a metadata flag and tests of separately installed personal skills cannot establish Blitz's routing reliability. Verify selection in your actual host and retain the explicit fallback.

## Tools and contents

| Location | Purpose |
|---|---|
| [Company profile](Blitz/profiles/company.md) | Founder workflow, evidence gates, roles, economics and scoped jurisdiction questions |
| [Templates](Blitz/templates/) | Editable brief, cash inputs and working records; create only what is useful |
| [25 method packages](Blitz/setup/skills-guide.md) | Research, reasoning, writing, economics, design, building and review methods with their resources and notices |
| [Setup tools](Blitz/setup/) | Local company initialization/calculation, CSV scoping, archive verification and item export |
| [Runtime guide](Blitz/setup/runtime.md) | Optional 17-file Thor-compatible source set and resource archive; generation does not install anything |
| [Examples](Blitz/examples/company/), [evaluations](Blitz/evals/) and [tests](tests/) | Synthetic demonstrations and builder checks, separate from runtime context |
| [Verification](docs/VERIFICATION.md), [migration](docs/MIGRATION.md) and [changelog](Blitz/CHANGELOG.md) | Check contracts, upgrade boundaries and release history |

The cash command emits JSON. **0** means a complete calculation, even if it reports a shortfall; **2** means incomplete inputs; **1** means invalid input or another handled error. It preserves supplied period order, requires one currency per forecast, and distinguishes earned revenue from collections. It checks closing balances, not cash movements within each period, and does not extrapolate runway beyond the supplied horizon.

For a shared CSV, the scope utility selects exact rows and named columns. After the first-use setup, this runnable example keeps only Period 1 and three columns from the verified synthetic source:

```sh
python -B Blitz/setup/scope_csv.py create --source Blitz/examples/company/service-cash.csv --output .work/period-1 --expected-sha256 1c7d3b6a645f3d8b4534144c50b0d9eee07c67bce5d0266ebc232bd3a9b65ecc --source-revision v2.1OAI --item-column period --item-id "Period 1" --column period --column currency --column earned_revenue
```

It writes `projected.csv` and `provenance.json`, with source, filter and hash evidence. The pinned hash belongs to this exact example. Use a separately trusted source hash for other inputs and retain the returned receipt hash for inspection. `python -B Blitz/setup/scope_csv.py inspect --help` shows the verification interface. A projection and matching hash do not establish that arbitrary cell content is appropriate to disclose.

Selected methods may need external libraries, document renderers, fonts, browsers, connectors or host tools. These are not bundled or granted. Check the method's actual dependencies before use. Source availability does not establish native installation, automatic routing or execution on your host.

## Privacy and authority

Keep credentials, real customer records, private terms and company instances out of tracked files. Use explicit allowlists for exports, inspect their actual contents, and follow the [item-export contract](Blitz/setup/item-export.md). A private filename is a label, not access control.

Evidence informs decisions; a human owns consequential commitments. Company formation, contracts, spending, outreach, account changes and deployment require applicable authority. Activity and jurisdiction determine which legal, tax, licensing, data and insurance questions need current evidence or qualified review. A founder's approval cannot supply a missing permission. Interrupted external actions must be reconciled before retrying.

## Verification

From the repository root, use new output directories for each run:

```sh
python -B -c "from pathlib import Path; [Path(p).mkdir(exist_ok=True) for p in ('.verification', '.dist')]"
python -B Blitz/setup/verify_kit.py
python -B Blitz/evals/run_all.py --kit Blitz --out .verification/readme-check
python -B -m unittest discover -s tests -p "test_*.py" -v
python -B tools/release.py build --out .dist/readme-release
python -B tools/check_publication.py
```

The build produces the versioned master ZIP, runtime source set and `release-manifest.json`. The master contains a self-contained [release guide](Blitz/setup/release-guide.md) for archive users; repository-only CI and release tooling remain in this checkout. It does not publish or install them. The [CI workflow](.github/workflows/verify.yml) runs kit, regression, publication and packaging checks on Linux. Read the [verification contract](docs/VERIFICATION.md) for what each result establishes. Passing checks proves their stated behavior and file identities, not business success or universal disclosure safety.

## Contributing

Propose a concrete user problem and the smallest change that addresses it. Follow [repository instructions](AGENTS.md), preserve useful existing interfaces and method notices, and keep examples independently synthetic. Include affected checks and actual results with the change. Do not attach real company data or credentials to an issue, pull request or fixture. A method or document should earn its place through a task, dependency or demonstrated failure.

## Rights and distribution

This edition carries component-specific license and attribution notices, plus original generic symbols in place of product logos. Public distribution uses a reviewed source snapshot with fresh Git history; earlier development history and source originals remain private. Read the [rights audit](docs/PUBLICATION_AUDIT.md) and [publication record](docs/PUBLICATION_PLAN.md). No repository-wide license has been selected; this edition is not represented as open source.

Blitz derives from the v2OAI package; this edition preserves its method identities and reviewed mechanisms while replacing private material with reusable guidance and synthetic fixtures. Read [rights and provenance](docs/PROVENANCE.md) and the applicable component notices before redistribution. Publication checks are bounded checks of reviewed content and history, not clearance for arbitrary future inputs.
