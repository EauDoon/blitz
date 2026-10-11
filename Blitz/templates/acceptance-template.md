# Acceptance record

Use under [the operating contract](../setup/operating-contract.md), bound to the exact artifact revision checked. A concise inline check suffices for small work. Keep one useful record per deliverable when persistence is needed.

| Field | Content |
|---|---|
| Deliverable ID and revision | |
| Item and method baseline | Item ID; governing source revision; pinned Blitz and selected method revisions/fingerprints |
| Acceptance criteria (from the brief) | |
| Recipient-use check | What the recipient must be able to do, and the observed result using the final artifact |
| Coverage and dependencies | Consequential requirement, readable evidence and actual output location; missing essential inputs retain a dependent limit |
| Checks run | Name each: render and look, verify.sh, cold-read tier, arithmetic rerun in code, converted Doc read back |
| Results | Pass, fail with findings, or checked with named limits |
| Findings and disposition | Fixed, accepted with owner and date, or rejected with reason |
| Accepted by | Actual acceptance authority and time, or not yet accepted; a builder's successful check is not the owner's adoption |

A change after acceptance invalidates the affected checks. Rerun them before the output leaves.

Review the actual saved/rendered/converted files or executed path, not only the source draft or builder's summary. Reconcile narrative, tables and related artifacts against the same snapshot. Where independent review is required, supply commission, evidence and artifact without the builder's verdict. Retain genuine failures, repair authorized causes, and recheck affected results; do not add duplicate review rounds without a material reason.

Use [substantive completeness](../skills/blitz/references/context-acquisition.md#acceptance-on-the-actual-artifact): compare the actual final artifact to required coverage, including populated fields, source support, currency of evidence and consistent calculations. Repair omissions from accessible authorized sources. Essential gaps remain explicit; a blank template or partial draft is judged by its narrower commission.

For a commissioned item export, also apply [the handoff contract](handoff.md): explicit allowlist, complete required dependency closure, editable originals, item-scoped `PROJECT_INSTRUCTIONS.md` with applicable intent/supporting triggers, manifest/hash verification and a declared canonical writer. Missing or restricted prerequisites prevent a self-contained-readiness claim until receiver access is verified. Packaging does not authorize installation, publication or ownership transfer.

Record package integrity, readable methods, observed method execution, automatic routing, durable save/resume, destination-host results and controlled receiver independence separately. A name in an index, successful local check or uploaded ZIP does not prove host execution. Test ordinary-language intent plus review-only, small-task, wrong-item and source-instruction negatives against [the Thor guide](../setup/thor.md) where applicable. Unexecuted, blocked or partial mandatory checks are not passes; local trials do not replace the real Thor/receiving-host checks.
