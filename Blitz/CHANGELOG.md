# Changelog

## Unreleased tool input fixes, 27-11-2026

Fixes three tool defects found by running the commands with malformed input. `company.py stress` now reports a deeply nested scenario file as a handled error with exit code 1; it previously ended in an uncaught `RecursionError` traceback. The shared `verify_archive.load_json` helper converts the same condition to a `ValueError`, so `scope_csv.py inspect` reports a deeply nested receipt as a failed check. The repository tool `tools/update_manifest.py` now parses its arguments before writing, so `--help` or a mistyped flag no longer rewrites `manifest.json`. The root README states that directory-creating commands support Windows and Linux only and that paths with a `.` or `..` component are rejected. Calculations, schemas, method identities and record names are unchanged. This is an unreleased source change; published v2.1OAI-r1 archives remain unchanged.

## Unreleased delivery capacity, 13-11-2026

Added a separate read-only resource planning module for ventures and departments. `company.py capacity` assesses supplied hours across shared resources and ordered periods, reports capacity overloads with contributing work, compares required effort with planned and by-due hours, and checks finish-to-start dependencies. Strict versioned JSON rejects ambiguous references, cycles, duplicates and misspelled fields. Unknown capacity and effort remain explicit; known conflicts remain visible alongside missing inputs. Calculations use exact decimals and include an input digest. Added a synthetic plan, schema/interpretation guide and regression coverage for hours, dependencies, unknowns and CLI exits. This is an unreleased source addition; published v2.1OAI-r1 archives remain unchanged.

## Unreleased cash scenarios, 13-11-2026

Adds a read-only `company.py stress` command with named collection-delay, receipt-multiplier and cash-cost scenarios. Reports complete period calculations, deferred collections, baseline differences and closing reserve gaps. Reuses the Decimal forecast engine, validates baseline cash continuity, retains unknown amounts and leaves input files unchanged. Includes a synthetic scenario set, usage guide and regression tests. This source change does not replace tagged archives or publish a release.

## Unreleased source update, 24-10-2026

Adds an optional customer-discovery and price-testing guide within the existing Frame/Test gates, selected past-behavior prompts in the call card, and commercial experiment fields for exact offers, buying units, evidence and objections. Distinguishes billing dates, payment due dates and collections when comparing cash timing. Clarifies that the call-card debrief clock belongs to a selected measured pilot. Preserves the lean default, department route, 25 method identities, four core record names and source/authority/recovery rules.

The 100 synthetic behavioral cases in `tests/evals/customer-discovery` were frozen before implementation. Case authoring, actual runs and semantic review are distinct evidence; results are reported separately. This is a source revision on main, not a replacement of the v2.1OAI-r1 tag, published archives or installed host copies.

## v2.1OAI-r1, 11-10-2026

Repairs the independent audit findings: preview containment/error handling; ZIP metadata and complete-history publication checks; scoped collection and recording; explicit unknown permissions; contrast thresholds; nested/styled SVG export; reference geometry; classic/module JavaScript checking; evidence-faithful rewriting; and transitive staging context. Adds a company/department START route, smaller graphic headings and inclusive resource wording.

Uses standalone Blitz naming across current guides, compiler entrypoint, generated startup/runtime files and references. Existing public history is preserved. This content revision has distinct archive/tag identities; it does not replace earlier bytes. Licensing terms, 25 method identities, core record names, no-overwrite safeguards and human approval boundaries remain. Actual check results are recorded against the saved candidate separately.

## v2.1OAI, 11-10-2026

Presentation update: identifies Blitz as the Minimum Viable Company kit with the tagline “Listen, collect, sprint. / Reduce cycle time.” Adds an explicit founder walkthrough, output map and complete 25-method skills guide. Distinguishes source use, reference staging and native invocation without claiming measured automatic-selection reliability. Replaces repository artwork with an original responsive visual system and bounded motion, preserving the four business gates and all tool behavior.

Founder edition based on the verified v2OAI master. Adds a proportionate minimum viable company workflow, editable brief/cash inputs, local starter and cash calculation, independently synthetic examples and first-user checks. Adds shared-CSV scope/provenance tooling and truthful working-copy handoff guidance.

Preserves the 25 method identities, four core record names, evidence/authority/recovery rules, archive safety, explicit item export and reproducible Blitz-compatible runtime. Generalizes owner/host wording and removes personal profiles, private account history, live-case-derived examples and unneeded private environment dependencies from the reusable edition. Original v2 bytes remain separate and unchanged.

Adds reproducible release packaging, CI, regression/adversarial cases and publication checks over tracked content and reachable Git history. Test outcomes are recorded separately against the actual candidate; this changelog does not certify them.

Publication preparation adds a founder-facing repository README and original responsive workflow artwork. Component notice repairs retain the verified Gauntlet CC BY/MIT and presentation/Meta Skill Apache terms. Anti-slop carries an explicit CC BY-SA 4.0 adapter scope for its two adapted instruction files and the verified upstream notices. The 37 product entries use newly drawn, labeled generic symbols, including two former placeholders; copied product artwork is replaced throughout the bundled examples. The 50 generic Tabler entries, all 87 catalog keys and all 25 method identities remain. A standalone release guide brings first use, migration, verification and rights boundaries into the kit archive. The README uses its readable vertical workflow through 820-pixel viewports. The README also includes an original 4.8-second motion illustration with a static fallback. Public distribution uses a fresh reviewed source snapshot; these changes do not authorize publication of earlier Git snapshots.

## v2OAI, 02-10-2026

Unified operating contract, natural request routing guidance, complete source compiler, runtime closure, archive integrity and safe extraction, and reference/working-copy export rules. Historical release identity is recorded in the new manifest. Historical live application or test results do not transfer to v2.1.

## Earlier lineage

v1.1 through v1.5 developed lean execution, context acquisition, operating-loop recovery and item exports. Source originals preserve the full audit history. This repository begins with a sanitized v2.1 tree and does not import personal source histories.
