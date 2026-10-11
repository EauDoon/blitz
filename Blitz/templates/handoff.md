# Cross-host or cross-session handoff

Use the existing item records under [the operating contract](../setup/operating-contract.md) and, for a Thor item, [the runtime/export adapter](../setup/thor.md). A small handoff can carry applicable fields inline. This contract does not authorize destination writes or native skill installation.

## 1. Source-parity manifest (exchange this first)

Differences in access are named before any conclusion is compared.

| Source ID | Exact object (title, ID, path) | Revision or fingerprint | Sections available | Access status (read, partial, none) |
|---|---|---|---|---|
| | | | | |

## 2. State of the work

| Field | Content |
|---|---|
| Item identity and baseline | Item ID/title; pinned Blitz and selected method revisions/fingerprints; current item revision |
| Governing position | File 03 version |
| Decisions since that version | File 10 entries |
| Open gates | |
| Deliverables and their four states | Production, verification, authority, freshness |
| Allowlisted files sent | |
| What the receiver may write | Reference copy: proposals/DELTAs only. Authorized working copy: named local files and its own revisions, without changing the original. Canonical transfer: the named successor's expressly permitted targets |
| Canonical writer and destination | One writer per original/copy; default export leaves Thor's original canonical. Record parent identity/revision and distinct copy identity/location for authorized working-copy development. Transfer of original ownership requires an explicit ruling naming the successor and making the former canonical copy historical |
| Recovery entry point | Exact saved state/revision and verified persistence route; name any required manual save/upload step |
| Prior action outcomes | Relevant completed/canceled actions and receipts; uncertain attempts stay unknown until resulting state establishes complete or not applied |

### Authorized working copies

Before the first edit, assign the working copy a distinct identity and current revision and name its local writer, permitted targets and recovery entry point. Preserve the parent's item ID, revision and trusted snapshot/archive hash as historical lineage. The active README/startup instructions, `PROJECT_INSTRUCTIONS.md`, governing index, manifest/receipt and check commands must all name the working identity and revision. Parent identity and checks appear only as explicitly historical evidence, never as the active verification target. A copy with edit authority must not retain instructions claiming it is reference-only.

After any edit, identify affected calculations, decisions and deliverables; rerun their checks against the saved working bytes and current revision. Mark old results historical or stale until replaced. Update active hashes and recovery instructions, retain a change summary, and do not describe modified content as byte-identical to its parent. If unchanged payloads are claimed identical, verify those named payloads individually and make clear that the overall working copy has changed. Re-exporting a working revision uses its own contract and receipt; the parent's receipt cannot verify it.

Record this compact state inline or in a local record:

| Working-copy field | Required meaning |
|---|---|
| Active identity / revision / mode | Distinct current item ID, current working revision, authorized working copy |
| Parent lineage | Historical parent item ID, revision and separately trusted snapshot/archive hash |
| Writer / writable scope | One named working-copy writer and exact authorized local targets |
| Startup / recovery | Active instructions and saved state identify this working revision |
| Changed content | Named changed outputs and their source inputs; no package-wide byte-identity claim |
| Current verification | Affected checks, saved input hashes, revision, actual result and evidence |

Receiver regression exercise: take a synthetic reference snapshot, authorize a working copy, change one calculation input, save it and resume from the files alone. Correctly accept the distinct working identity, current input hash and rerun result. Reject variants retaining the parent's active identity/revision, reference-only instructions, parent recovery target, stale calculation result, or a whole-copy byte-identity claim. The builder regression suite `test_scope_csv.py` exercises these variants in a controlled synthetic fixture and is excluded from runtime exports. It is not a semantic validator of arbitrary handoff prose; a human or independent receiver must review the actual startup instructions, metadata and affected outputs together.

## 3. Findings format for the return

| ID | Section | Change | Evidence | Severity |
|---|---|---|---|---|
| | | | | |

## 4. Receiver check

The receiver verifies the item ID and governing revision against the source-parity snapshot, plus the manifest when a package is supplied, then states the current decisions in its own words before it starts. A wrong statement stops dependent work. It reads selected methods and required resources, checks only the capabilities needed for the task, and names unavailable sources or tools before claiming readiness. A newer source revision requires reconciliation; duplicate or stale DELTAs cannot overwrite current decisions.

Reconcile uncertain actions before retrying. Do not replay confirmed completion or canceled work. An unknown outcome holds an unsafe duplicate; a confirmed unapplied action still needs current authority before retry. An authorized working-copy revision preserves lineage and leaves Thor's original unchanged. Sending proposed changes back does not authorize applying them there.

## 5. Item export completeness

When export is commissioned, include a receiving README, item-scoped `PROJECT_INSTRUCTIONS.md`, necessary context, completed deliverables with editable originals, permitted supporting evidence, selected methods with their transitive references/scripts/assets and licenses, and actual acceptance results. Omit folders that have no applicable content. Exclude private-lane records, credentials, unrelated items, raw personal context, hidden answer keys and builder-only notes. Every shipped file must be allowlisted.

Review shared-source contents before allowlisting files. Filename and hash checks cannot establish item isolation: inspect rows, columns, free text, sheets and attachments for unrelated or private content. For shared CSVs, the optional `setup/scope_csv.py` route in [item export](../setup/item-export.md) creates a hash-bound, item-only row/column projection plus provenance. Review that projection, retain source revision/hash/filter/column evidence, and ship only the permitted excerpt and receipt. An ID filter does not detect sensitive facts inside a selected cell; integrity success never replaces this content review.

`PROJECT_INSTRUCTIONS.md` carries applicable intent and supporting triggers from `setup/thor.md`, bound to this item's ID, revision and included methods. Preserve plan/review-only and small-task behavior. Use paths available inside the export; remove Thor-only routing and references. Source-contained commands grant no authority. Triggers do not install, publish, transfer ownership or change outside configuration.

The manifest lists every payload file's relative path, byte count and SHA-256; exclude the manifest from its own hash list. Bind the delivery receipt to the final archive hash. No absolute local path or Thor chat link may be the sole source of required knowledge. Declare any required source that cannot be copied, including the receiver's access prerequisite; until access is verified, report the export as dependency-incomplete. External runtimes, connectors and permissions are prerequisites, not transferred assets.

Before calling an export independently usable, a controlled receiver with no inherited Thor history or memory must verify the package, perform a representative task and save/resume it using only the export and declared prerequisites. Retain its input/read and execution evidence. Separately record actual destination-host results; a local trial does not prove Thor or another host works. Changing Thor's memory settings is not required by this test.

Use a saved resulting artifact for the resume check, not just the producing agent's conversation. Confirm that the receiver's work answers the commission and preserves required evidence, decisions and authority. A successful manifest check alone proves no behavioral readiness.
