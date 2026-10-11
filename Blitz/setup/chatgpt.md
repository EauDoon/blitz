# Setup on ChatGPT / OpenAI, v2.1OAI-r1

For Blitz, use [the final operating contract](operating-contract.md), [the Blitz adapter](source-use.md) and the complete source generator described in [runtime preparation](runtime.md). The account-role comparison below remains guidance for separately authorized host adaptation, not a requirement to install global skills for Blitz.

Use this guide when OpenAI is the canonical host, or a second host works from an allowlisted snapshot. The original 45-minute setup estimate is a planning assumption, not a measured OAI result. Preparation, checks, installation and adoption are separate decisions.

## Blitz source-based route

For Blitz, follow [setup/source-use.md](source-use.md). Keep Work, current memory settings, existing outside skills and global instructions unchanged. Apply only an explicitly authorized Blitz source/instruction write set. The packaged `setup/Blitz_Project_Instructions.md` is the exact instruction body; verify its saved readback after authorized application. Its compact intent rules bootstrap ordinary-language requests and point to the directly readable, versioned guide. Do not depend on opening the ZIP before routing can start.

Read the selected method's actual instructions and required resources, then use observed tools. This route requires no account-wide Blitz installation or broad staging of the 25 skills. Method names, generated source views and uploaded archives do not prove native loading or live execution. Record directly readable content, executable dependencies and actual routing separately. The native installation workflow below applies only when separately requested for a named host.

For commissioned item exports, reuse the existing records, commission and handoff. The item carries its own scoped `PROJECT_INSTRUCTIONS.md`, applicable automatic triggers, pinned methods and complete required dependencies. The source project remains canonical unless an explicit transfer changes the sole writer. Verified persistence is required for continuation: if direct project-file writes are unavailable, return a versioned state bundle and name the required save/upload step. A chat link or memory recall does not establish durable state or receiver access.

## Preserve host adaptations

A reference stage now carries one exact master snapshot at `_blitz-source/Blitz` alongside the 24 mapped candidates. Keep the stage together so transitive context, resources and notices resolve. The snapshot is source comparison material, including builder tests/examples; it is not installed runtime or a second maintained source. Runtime compilation continues to exclude builder material. Read `STAGE.md` and verify `stage-report.json`.

The portable kit supplies methods, not authority to replace current skills. Default sequence: inventory, compare, merge necessary changes, isolated checks, separately authorized installation. Keep a recoverable baseline and preserve each host-adapted skill's supported save/install route. A current adapted skill can differ materially from these Claude-derived source copies, including review roles and tool handling.

1. Read the installed listing through the supported read-only host route. Capture names, roles, versions/hashes if observable, observation time, and supported save/install paths. `setup/host-inventory.example.json` is a synthetic shape, not a current listing. `setup/name-map.json` is historical name guidance only.
2. Inspect without writes: `python3 setup/chatgpt_stage.py --out ../new-reference-stage --dry-run`. To compare an inventory, add `--inventory observed-inventory.json`. The output must be a new non-live folder outside the kit, even for a dry-run; occupied, ancestor, source-alias and known live-skill paths are rejected. A dry-run performs no account or filesystem writes.
3. To prepare reference files after a successful dry-run, rerun without `--dry-run` using a new output path. Staging validates all transformed copies before publication. It does not install, replace or delete existing destinations. Only its own temporary sibling may be cleaned up; an unexpected final copy failure can leave an incomplete new output, which is not a verified stage.
4. Compare each reference candidate with the existing same-role adaptation. `same`/`renamed` is not a replacement instruction. Preserve the installed role name, native tool handling and supported save/install path. Merge only the needed method changes into a separately reviewed candidate. An `unknown` row requires role comparison before proposing a new skill; an unresolved role is not an invitation to create a duplicate.
5. Resolve required, optional and unavailable dependencies using `setup/host-adapters/openai.md` and the current capability manifest. Staged packages carry this adapter as `references/blitz-host-adapter.md`. Names/frontmatter/cross-reference rewrites do not establish behavioral compatibility. A native-role skip still requires a capability observation.
6. Run package, explicit method, native load, fresh routing and installed-integrity checks as distinct stages on the named authorized target. Verify transformed staged hashes, not untransformed source hashes. No paid routing tests. No account installation follows from staging or package success; the owner or the named release owner controls installation authority.

An OpenAI-only candidate may be prepared and checked against OpenAI capabilities without Claude access. Applicable OpenAI native checks are required for an OpenAI runtime claim. Cross-host compatibility remains unverified until the Claude and OpenAI checks each exist. An unavailable Claude host does not block candidate preparation, and never becomes a Claude pass.

Each source package carries `agents/openai.yaml`; invocation policy and listing paths must still be observed on the actual target surface. A copied config does not prove native skill selection or automatic routing. Use the supported host install route rather than inventing one from source-platform instructions.

## Profile-aware setup

Use `ENTRYPOINT.md` and choose lean/comprehensive against the commission. Lean starts with one owner, one workstream and the requested deliverable. Keep the existing 00/03/09/10 names and schemas; small tasks may keep the relevant fields inline until persistence is needed. Only applicable capability rows need observations. Instructions and file 00 can bootstrap a run without router installation or broad staging. Source-based automatic routing needs observed positive/negative cases on the named host; native-load/install gates apply only to a native installation claim. Never mark an unexecuted check passed.

## Project setup

| Step | Who | Action | Done when |
|---|---|---|---|
| 1 | the owner | Name the project/type and choose canonical or second-host role | Role named |
| 2 | OpenAI | Run `python3 setup/verify_kit.py` | Prints `KIT OK`; limits recorded |
| 3 | OpenAI | Fill the capability manifest and resolve the adapter | Every applicable row has an observation or named gap |
| 4 | the owner/release owner | Create the project and authorize filled `templates/project-instructions-chatgpt.md` | Full readback and tail match |
| 5 | Canonical scribe | Write files 00, 03, 09 and 10 from the context templates; second host reads only its named allowlisted snapshot | Authorized files listed |
| 6 | Canonical host | Create the agreed Drive tree only if authorized and available, as in Claude step 6 | Folder IDs recorded, or named destination gap |
| 7 | OpenAI | Draft the counterparty file prompt only when needed to obtain task inputs and drafting is authorized | the owner reviews/sends it, or not applicable recorded |
| 8 | OpenAI | In an authorized local workspace, use the commission and acceptance criteria for ordinary outputs. Only for an actual project skill build, copy the scoped operating rules, filled build contract and exported build-input allowlist to the assigned repository | Skill build: `AGENTS.md`, `BUILD_PACK.md`, `ALLOWLIST.md` exist. Ordinary output: applicable commission and checks recorded; no mandatory BUILD_PACK |
| 9 | Authorized host tester | For a separately authorized native/runtime claim, run fresh manual positive/negative smoke cases | Expected methods visible; no project routing, project facts or build-lane tools on negatives; router-load recorded separately |
| 10 | Both | Continue Ingestion in the playbook | Gate recorded in file 10 |

A correctly declining router passes an unrelated request even if the host loads it at session start. Leakage or build-lane work fails the invariant regardless of visible load traces. Record the observer, actual model/configuration, source/candidate hashes and any missing instrumentation. No fresh-session pass is inferred from this document.

## Second-host rules and rollback

Work from the allowlisted snapshot and return revision-bound DELTAs. Never edit canonical context from a second-host session unless an explicit transfer has made it the sole canonical writer. Exchange a source-parity manifest before reconciliation; reject duplicate DELTAs and reconcile stale source revisions before applying changes. Keep the prior verified package, instruction body and any actual application/installation receipt. If a later authorized application or install fails integrity or mandatory smoke checks, the release owner restores the affected prior files/body through its supported host route; staging alone has changed no account state to roll back. Restoring content does not imply restoration of original platform object IDs.
