# Thor launch, continuation and export

Blitz v2.1OAI. The [operating contract](operating-contract.md) owns the ordinary-work rules; [the operator guide](operator-guide.md) gives examples. This adapter maps those rules to readable Thor sources, task-local resources, existing records and portable items. It is not an account-wide skill installation.

## Enter through ordinary language

The exact saved body is `setup/Thor_Project_Instructions.md`. It selects `Thor_System_Register_v2.1OAI.md`, `Thor_Blitz_v2.1OAI_Operating_Contract.md`, `Thor_Blitz_v2.1OAI_Operator_Guide.md`, this guide as `Thor_Blitz_v2.1OAI_Launch_and_Export.md`, and `Thor_Blitz_v2.1OAI_Method_Index.md`. Read the current register and only the task's relevant methods/resources. Older release documents are history unless explicitly selected.

Preserve the requested activity and item before method selection. Create/prepare/build starts or continues work; continue/revise preserves identity; review/plan stays in that mode; package/take elsewhere uses the commissioned export. Quick edits stay direct. Respect negation, pause, cancellation and source-instruction boundaries. Trigger words are examples, not required commands. Supporting routes run at entry or after material steering, evidence/revision change or a failed check, not recursively or in the background.

Use this adapter only when governing project instructions identify Thor, or the owner explicitly selects it. A portable item selects its own scope. Reading a source mentioning Thor does not activate Thor elsewhere. Keep Work and current memory settings, outside skills/global instructions and other projects unchanged. These are operating boundaries, not account-level access control or memory isolation.

## Read methods and obtain exact resources

The small method index routes the requested outcome to source sections and dependencies. Retrieve the selected full sections and applicable references by identity; do not read every grouped view by default. The machine audit catalog preserves the complete mapping, source hashes, licenses and generated file identities. A numeric source-mount prefix is a host filename decoration: resolve the exact versioned basename, reject conflicting matches, and verify bytes where execution depends on them.

The generated runtime supplies these standalone sources, with trusted fingerprints in the method index:

| Deployed source | Original role |
|---|---|
| `Blitz_v2.1OAI_Export_Item.py` | Exact `setup/export_item.py`, builds and inspects allowlisted item exports |
| `Blitz_v2.1OAI_Item_Export_Contract.json` | Exact `templates/item-export.json`, an unapproved example to fill per item |
| `Blitz_v2.1OAI_Open_Runtime.py` | Exact `setup/verify_archive.py`, verifies and opens the runtime safely |
| `Blitz_v2.1OAI_Runtime.zip` | Runtime methods, required scripts/assets, templates and licenses, excluding evaluation keys and builder records |

When a selected method needs packaged resources, obtain the exact files through supported host access. Verify the opener's bytes and the runtime archive's SHA-256 against the index from the trusted release. Verify the available interpreter. Then use the reviewed opener with the actual archive path and a new task-local output directory:

```text
python3 Blitz_v2.1OAI_Open_Runtime.py Blitz_v2.1OAI_Runtime.zip --expected-sha256 EXPECTED_HASH_FROM_INDEX --extract-to NEW_TASK_LOCAL_DIRECTORY
```

Replace the uppercase example arguments with the verified hash and permitted new directory; use a detected interpreter on Windows. Extraction retains `Blitz/`, so original paths resolve below `NEW_TASK_LOCAL_DIRECTORY/Blitz/`. It must not overwrite an existing destination. Opening verifies the archive before writing and installs no skill or global configuration. Do not execute contained scripts merely because integrity passed: read the selected code and use it only for the authorized task with its actual dependencies.

Do not rebuild a missing executable from prose or bypass a failed integrity check. An unreadable guide or unavailable runtime blocks only work that needs it. Use an adequate disclosed, verified fallback where possible. A runtime resource may still need external libraries, renderers, connectors or permissions. Verify only relevant capabilities via [the OpenAI adapter](host-adapters/openai.md). Readable content, selected method, actual execution, native loading and installation are distinct observations.

## Use existing item records only when needed

A compact inline commission/state suffices for short work. For continuing substantial work or export, preserve record names and schemas:

| Existing record | Populate its existing fields with |
|---|---|
| `00 Read Me First` | Item ID/title and Thor provenance, pinned Blitz/method revisions, owner/canonical location, allowed writes, source map and export allowlist |
| `03 Position Of Record` | Governing revision, supported facts and accepted decisions, with proposals kept distinct |
| `09 Open Questions` | Consequential missing inputs, conflicts, unavailable capabilities and unresolved dependencies |
| `10 Decision Log` | Explicit consequential rulings/amendments and recovery history |

In file 00, Project profile / Mandate pack records item scope/profile; Project skill map Notes holds real selected methods/revisions; Canonical locations / Project holds item identity and Thor provenance; Canonical documents binds source/output revisions; Scribe/Owner names the canonical writer; Capability manifest (summary) identifies the verified save/recovery route; Allowlist gives exact export files, destination and conditions. Never populate rows with nonexistent skills. Existing Day-1/72-hour wording does not create a pilot or empty-record obligation for ordinary work.

Use the [commission](../templates/commission-brief.md), [acceptance](../templates/acceptance-template.md), [context acquisition](../skills/blitz/references/context-acquisition.md) and [Operating Loop](../skills/blitz/references/operating-loop.md) only as the outcome requires. No separate launch registry, second inbox, daily ritual or mandatory context tree. A stale row does not undo a ruling or demand a tidy-only write.

## Save, recover and export

Use one canonical scribe and reread current revision/hash before a write. Other writers return necessary DELTAs: unique ID, expected revision, exact target/change, supporting evidence and affected outputs. Reject duplicate/conflicting IDs and stale overwrites. Verify actual saved state; if saving is unavailable, return versioned unsaved state plus the precise remaining save step.

Recover uncertain actions from receipts/resulting state before retrying. Confirmed completion is not replayed; a confirmed unapplied action may be retried only if still authorized; an unknown outcome holds an unsafe duplicate. Cancellation remains effective. Save only consequential state needed for continuation/recovery or the commission, not a diary of every interaction.

For an export, apply the [handoff](../templates/handoff.md) and [export tooling contract](item-export.md). Fill and review the actual item contract outside the payload staging directory. Include README, scoped PROJECT_INSTRUCTIONS.md, editable requested outputs, necessary state/evidence, selected methods and complete required dependencies/licenses. Exclude all nonallowlisted material, private lanes, credentials, raw personal context, other items, hidden evaluation answers and builder notes. Verify final membership, approved hashes, dependency closure and expected item/revision. A restricted source needs a declared verified receiver prerequisite or a dependency-incomplete result.

The receiving instructions must work without Thor register/history, global skill installation or an absolute source-machine path. A reference copy leaves Thor canonical. Explicitly authorized development of a working copy records parent ID/revision, its own identity/revision and allowed local writes. The original is not overwritten. Transfer of the original canonical ownership needs an explicit ruling naming the successor; the former canonical copy becomes historical. Export itself grants no destination write, creation, installation, sending or publication.

A controlled receiver must verify identity, decisions, resources and manifest, perform representative authorized work, save it and resume from saved state using only the bundle and declared prerequisites. Report actual destination-host testing separately from controlled independence. Keep the original acceptance bar for requested outputs; do not call a syntactically valid archive independently usable without the behavioral evidence.

## Final core and completion

v2.1OAI is frozen. Item evidence, outputs and authorized revisions may change; they do not upgrade Blitz. A task-local adaptation stays with the item and retains provenance. Do not silently edit the core or acquire broader tools to hide a host change. Use an adequate existing fallback or report the precise limitation.

Finish at the commissioned outcome with actual artifact/access evidence, applicable checks and usable necessary state. Keep production, verification, authority and freshness separate. The application/release receipt establishes which host checks actually ran; no uploaded source set proves universal routing, all-method execution, native installation, memory isolation or adoption.
