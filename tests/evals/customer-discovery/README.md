# Blitz customer-discovery behavioral evals, v1

This package was authored and frozen before implementing the bounded optional discovery/pricing/synthesis update. It contains exactly 100 synthetic development/regression cases, CD001–CD100, organized into ten families. See COVERAGE.md for the case map and limitations.

`cases.jsonl` is the executor task corpus. `evaluator/references.jsonl` contains separate case-specific review anchors, valid alternatives and verification provenance. `evaluator/scorers.json` uses deterministic checks for identity and exact requested arithmetic, and required `review` criteria for substantive behavior. `sources.jsonl` indexes immutable repository snapshots and synthetic policy. `contract.json` states the scope and acceptance boundaries. `minimal-contract.json` is an unchanged copy of the eval-workflow starter used to author the contract.

Use the eval-workflow offline helper to validate and project inputs. Do not pass evaluator files, controls, gold answers, diagnostic family labels or previous outputs to the answer-generating executor. The supplied helper does not enforce filesystem isolation. Any shared-mount limitation must be recorded in the run report.

A run must record its selected baseline or candidate kit content and digests. Baseline source is EauDoon/blitz commit `0001346002eff505b4f20b78674fc0763768bbc2`. The authoring source snapshots are provenance, not evidence of a target run. The 100 tasks do not require external facts or real actions; the target should return a single bounded JSON object under each case's explicit output contract.

Semantic review lives in a separate evidence-backed assessment sidecar. Inspect each case's actual response against every anchor and its valid alternatives. Record the exact evidence and reviewer limitations. Partial, failed, unresolved and disputed judgments remain distinct; helper numeric acceptance does not establish semantic correctness. No human review has been claimed for the authored references or controls.

The package's `controls` are synthetic rubric-calibration fixtures, not product output. Detailed helper execution receipts and later target runs stay outside this portable corpus. `SHA256SUMS` identifies the frozen bytes; it does not certify usefulness, independence, permissions or real business results.
