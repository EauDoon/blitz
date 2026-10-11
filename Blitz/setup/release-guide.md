# Standalone release guide: v2.1OAI

This guide ships inside the master archive. It is sufficient for a local first use, migration planning and verification without access to the source repository. It accompanies the [company and department guide](../profiles/company.md), [changelog](../CHANGELOG.md), manifest and component notices. Blitz connects the initial idea to a bounded operating baseline across offers/services, customer or stakeholder evidence, product, operations and decision ownership. Use it with a human operator/editor or an LLM with appropriate readable records and attached tools. Examples are fictional; a generated folder is preparation, not evidence that the unit can operate.

Aim for an operating unit in one or two days when scope, inputs, capacity and permissions allow. A demonstrated cycle requires actual delivery, named acceptance, reconciled exchange or resource use and a feasible next cycle. The target is not a guarantee; longer delivery or approval cycles take longer. Blitz guarantees no ARR, repeat demand, profitability or product-market fit. Autoscale means prepare repeatable processes and expand with evidence, capacity and authority, not deploy autonomous technical autoscaling.

## What the archive contains

The master contains the `Blitz/` kit: 25 method packages and their resources/notices, setup utilities, templates, company/department guidance, synthetic examples and builder evaluations. Runtime generation produces 17 files; its context/resources exclude builder evaluations, answer keys, reviews and worked examples. Generated runtime content does not install anything.

The source repository also contains the polished root README/artwork, detailed review and migration documents, GitHub CI, `tools/release.py`, `tools/check_publication.py` and root packaging tests. Those repository-only tools are not in this kit archive. Use a repository checkout for repository-wide publication/history scans or release builds. Do not try to infer a historical Git scan from this archive's bytes.

## First use without the repository

Use Python 3.12 or later. The setup helpers use the standard library. Commands below run from the parent of the extracted `Blitz/` directory. Substitute a verified Python command if your host uses another name. Preserve the supplied archive and its trusted digest before extracting; use the supported archive verification/extraction instructions in [runtime preparation](runtime.md) where applicable.

```sh
python -B Blitz/setup/verify_kit.py
python -B Blitz/setup/company.py init --out company-practice --name "Practice company" --owner "Example founder"
python -B Blitz/setup/company.py cash company-practice/company-cash.csv
```

The practice output must not exist. Its parent must exist, it must stay outside the source kit, and paths containing `..` are rejected. An absolute path is appropriate for real company or department records, which belong outside reusable source and distribution folders. Initialization creates seven drafts, including the brief, cash CSV and 00/03/09/10 records. It does not import or migrate existing work. The CLI and filenames remain company-oriented. For a department, adapt the draft brief to users, accountable sponsor, service/intake, acceptance and authorized resources; revise record 00's default `venture` type before adoption. There is no department-specific initialization mode.

The blank cash calculation intentionally exits **2**, reports incomplete inputs and preserves unknowns. Enter `0` only for a known zero. Read the fictional example and run its complete input:

```sh
python -B Blitz/setup/company.py cash Blitz/examples/company/service-cash.csv
```

Exit **0** means calculation completed; it can still report a cash shortfall. Exit **1** means invalid input or another handled error. Earned revenue and collections are different inputs. The tool preserves period order, requires one currency, checks closing balances and does not prove within-period liquidity or extrapolate beyond the supplied horizon. Its schema is a commercial cash forecast, not a departmental resource ledger. A budget allocation is neither earned revenue nor collected cash. Use appropriate existing records or the program sections of [Economics and Budget][department-budget] for internal allocations, commitments, actual spend and staff capacity.

In the brief, identify the customer/user, payer or accountable sponsor, bounded offer or service, hardest assumption, next permitted experiment, owner, acceptance criteria and time/cash or resource cap. Set change/stop criteria before seeing the result. Keep adopted positions in record 03, missing evidence in 09 and consequential decisions in 10. Close and reopen the files, then recover the owner, revision, next action and authority from saved content. A repeat initialization must refuse to overwrite the occupied folder.

Use the [service example](../examples/company/service-example.md) and [regulated-activity hold example](../examples/company/regulated-hold.md) to distinguish inquiry, order, accepted delivery and verified payment. The fictional evidence does not establish real demand. For an internal department, use actual stakeholder/user evidence, agreed acceptance and reconciled authorized resources; do not invent a commercial sale to claim an operating cycle. A licensing question or missing authority holds the affected commitment while useful independent work continues. No formation, contract, outreach, spending, filing or account action is authorized by this exercise.

## Migrate existing v2OAI work

1. Preserve the previous records, instructions, source snapshot and trusted archive digest. The historical v2OAI archive identity is recorded below; it is not the digest of this release.
2. Keep filled 00/03/09/10 records, adopted positions, identities and decision history. Adopt only useful prompts from the new company profile. Never replace existing records with initializer output.
3. Record the adopted package version and changed company assumptions through the current owner. A package upgrade does not amend an adopted position automatically.
4. Add collection timing, contribution, cash floor and delivery capacity to an existing model only where useful. Record currency, periods and source/assumption dates. Unknowns remain blank; zero remains explicit.
5. A revised working copy needs its own current revision, startup instructions and manifest. Keep its parent only as lineage, recompute current hashes and rerun affected checks. Do not retain a false byte-identity claim.
6. Test the next actual task, save, reopen and resume with declared prerequisites. Installation, native routing and adoption need separate evidence and authority.

All 25 method folder identities and the four core record names remain. Personal style methods require supplied approved examples; no bundled private writing profile is used. Export contract schema 1 and archive manifest schema 2 remain compatible. CSV scoping is optional preparation before the existing exporter. Generated source filenames use v2.1OAI; update a receiving host's v2 references only when that host change is authorized.

For rollback, stop using the new package and reopen the preserved original with its own trusted digest. Preserve legitimate company decisions and working-copy changes separately. Do not restore blank templates over them. This release performs no host installation to undo.

## Verify this kit

Use new output directories outside the extracted kit:

```sh
python -B Blitz/setup/verify_kit.py
python -B Blitz/evals/run_all.py --kit Blitz --out package-check-results
python -B Blitz/setup/build_thor_context.py --kit Blitz --out package-runtime
```

Read each actual result and log. Python 3.12+ is the supported release-test target. Windows native symlink checks may fail or be blocked by OS privilege; such results are not passes. Linux repository CI exercises those native cases. Source identity, script behavior, assistant use, native installation and actual company outcomes are separate claims. A successful integrity check is not disclosure clearance or universal compatibility with optional external libraries and tools.

The companion release receipt supplies the exact master archive, internal manifest and artifact hashes, source commit and performed test outcomes. The internal manifest enumerates this kit's payload. No hash or historical result is evidence that a new recipient's host installed or adopted the package.

## Provenance and redistribution

Historical baseline archive SHA-256: `ab7e65ecf628a034a7eba098ca5dfc05429c54150535f342f7225694f0e372d5`. Its historical internal manifest SHA-256 is `0f7a432ef6e235c0709e72061ce1a412dde9999da0dcbb9b5d3fd9c60c6ce31b`. Original bytes are preserved privately and are not included in this release. These identify the baseline, not the current archive.

Read [method provenance](../skills/provenance.md) and each applicable notice before redistribution. Anti-slop has an explicit CC BY-SA 4.0 adapter scope for two files plus retained upstream MIT notices. Gauntlet preserves its upstream CC BY/MIT terms; the presentation and Meta Skill adaptations preserve their applicable Apache terms. No repository-wide license is selected and no broad reuse license is inferred from possession. Current generic diagram stand-ins are labeled as such and do not claim to be official product logos.

Public visibility and license terms are separate. Earlier development history contains prior artwork copies; the current source repairs do not clear those snapshots. The approved publication route preserves that history privately and distributes only the reviewed source snapshot with fresh Git history after final checks. The archive contains the current kit rather than private development history. The repository's companion audit and history plan provide the fuller review record.

Keep credentials, private terms, live customer/employer material and filled private records out of reusable exports. Review actual contents and applicable permission, not just filenames or matching hashes. Human owners approve consequential commitments; local calculation and document creation do not grant external authority.

## Use the packaged methods

The [skills guide](skills-guide.md) inventories all 25 methods with a purpose, fictional example request, expected output and dependencies. Start with explicit source use if your assistant can read the extracted files. Reference staging and runtime generation prepare material; they do not install native skills. Verify host discovery and use explicit invocation when selection misses.

[department-budget]: ../templates/context/04%20Economics%20And%20Budget.md
