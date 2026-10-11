# Blitz v2.1OAI

**Minimum Viable Company kit**

Listen, collect, sprint.  
Reduce cycle time.

Blitz helps founders and small teams quickly establish a minimum viable company (MVC) or internal department. It connects an initial idea to a bounded offer or service, evidence, delivery and an accountable owner. Work directly with an editor and the records, or use an LLM with readable sources and appropriate attached tools.

Target an operating baseline in one or two days when scope, inputs, people and permissions allow. Demonstrate one delivered and accepted cycle, reconcile its exchange or resource use, and establish a feasible next cycle with an accountable owner. Actual evidence governs readiness; longer delivery or approval cycles take longer. A folder or plan is preparation. The kit guarantees no ARR, repeat demand, profitability or product-market fit.

Autoscale here means make the process repeatable and expand with evidence, capacity and authority. It does not deploy infrastructure autoscaling or autonomous operations. See [the company and department guide](profiles/company.md) for definitions, internal stakeholder/sponsor/resource counterparts and proportional gates.

For standalone archive use, read the [release guide](setup/release-guide.md): first use, migration, verification, package boundaries and component rights are included offline.

## Start

Use a verified Python 3.12+ interpreter. The local utilities use only the standard library. From the parent of this Blitz directory:

```sh
python -B Blitz/setup/verify_kit.py
python -B Blitz/setup/company.py init --out my-company --name "My company" --owner "Founder"
python -B Blitz/setup/company.py cash my-company/company-cash.csv
```

The output directory must be new. Blank cash inputs remain unknown; this calculation reports incomplete inputs and exits with code **2**. The initializer creates unadopted company-oriented drafts. It does not establish a functioning operating unit or grant permission to act.

For a department, adapt the brief to users, an accountable sponsor, service acceptance and authorized resources. Change record 00's default `venture` type before adoption. Company filenames and command names stay unchanged.

You can instead fill the [company brief](templates/company-brief.md) and [cash template](templates/company-cash.csv) manually, or reuse equivalent existing records. The fictional [examples](examples/company/) illustrate evidence standards; they supply no real validation.

## Preserve the useful core

The [operating contract](setup/operating-contract.md) connects outcome, evidence, execution, acceptance, recovery and portable export. Ordinary work stays lean: one owner, one workstream and the requested deliverable. Read the relevant method from the 25 packages only when needed. No native installation, account configuration or scheduler is required.

Project skills are optional. Applicable QA remains required; an untested new skill blocks its own release and dependent use while independent work continues. Use [Operating Loop](skills/blitz/references/operating-loop.md) for uncertain continuation and [context acquisition](skills/blitz/references/context-acquisition.md) for missing required evidence.

Keep the four core 00/03/09/10 records when continuation needs them, with one canonical writer and revision-bound changes. The [entrypoint](ENTRYPOINT.md), [operator guide](setup/operator-guide.md) and [playbook](PLAYBOOK.md) retain ordinary-work routing and selected comprehensive/pilot workflows. A 72-hour target applies only to a specifically commissioned measured pilot, never company readiness.

## Tools and boundaries

`setup/company.py` initializes local company-oriented drafts and computes a commercial cash forecast. It has no department-specific mode or budget/resource allocator. Use existing department records or the program sections of [Economics and Budget][department-budget] for allocations, commitments, actual spend and staff capacity; a budget approval is not revenue or collected cash. `setup/scope_csv.py` projects explicit item rows/columns from shared CSV sources with provenance. Neither verifies source truth, operating readiness or disclosure rights.

`setup/export_item.py` packages reviewed allowlisted item content; see [item export](setup/item-export.md). Integrity and content relevance are separate checks. Working copies need current startup instructions and their own identity/revision, with the parent retained only as lineage. Export does not authorize publication or transfer canonical ownership.

`setup/build_thor_context.py` compiles the optional 17-file Thor source set, with runtime scripts, method dependencies and notices. The Thor name is a compatibility surface, not a requirement to use this package. [Runtime preparation](setup/runtime.md) describes verification and opening. Builder `evals/`, `reviews/` and answer keys stay out of runtime; their absence is not a reason to fetch the master during ordinary work.

```sh
python -B Blitz/evals/run_all.py --out new-check-results
python -B Blitz/setup/build_thor_context.py --out new-thor-sources
```

Outputs must be new and outside the kit. Read actual logs and results. A platform limitation is not a pass. Package integrity, script execution, assistant behavior, native installation and actual receiving-host success are separate claims.

## Scope

Use synthetic examples and only authorized evidence. No credentials, private personal history, unrelated company rows, employer material or live project cases belong in reusable artifacts. Human owners approve consequential commitments; AI can prepare, calculate and review within the task's authority. Jurisdiction-specific legal/tax/licensing review is guidance and must be resolved before affected commitments, without an automatic compliance claim.

See [CHANGELOG](CHANGELOG.md), the manifest and release evidence. v2.1 is an explicitly commissioned successor to the immutable v2 original. Ordinary company or departmental work never silently changes the package, host settings, global skills or other projects.

## Choose a method

Read the [skills guide](setup/skills-guide.md) for all 25 packaged methods, example requests, expected outputs and host dependencies. It distinguishes explicit source use, reference staging and native skill installation. Source availability and implicit-invocation metadata do not prove discovery or reliable automatic selection in a host.

[department-budget]: templates/context/04%20Economics%20And%20Budget.md
