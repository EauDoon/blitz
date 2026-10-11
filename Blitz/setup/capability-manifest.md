# Capability manifest

Fill one copy per host at setup (step 3), and again when a session resumes after a relevant tool change. Observe only applicable task dependencies. Each row gets a result: works, fails, unavailable, or not tested; unneeded rows say not tested / not applicable to this task. Reuse current observations only for the same host/configuration, with evidence and time. Do not perform unrelated test writes merely to fill this table. Every probe remains subject to action authority. A failed/unavailable row names the fallback and which dependent work is blocked. Historical source records are not current observations. Classify each dependency required for the task, optional, or unavailable using the host adapter.

Host: [Claude | ChatGPT]    Session or project: [NAME]    Date and time: [DD-MM-YYYY h:mm AM/PM SGT]    Filled by: [SESSION]

Item ID/revision: [ID, revision]. Method baseline: [Blitz version and selected method fingerprints]. For Blitz, use [the source-based guide](source-use.md); retain Work and existing memory settings. No outside skill or instruction change is implied. Record actual evidence locations and configuration with each result, not only a yes/no judgment.

## Sources

| Capability | Test | Result | Fallback |
|---|---|---|---|
| Attached files readable | Open each attachment; note unreadable pages or audio | | Ask for a re-export; mark the gap in the source register |
| Google Drive read | Read one file in the project folder | | Ask for an attachment |
| Web read | Fetch one primary source page | | Name the source for the owner to open |
| Past chats and project files | Find one known item | | Ask for the file |
| Selected method and nested resources | Read the actual pinned method and each applicable reference/script/asset; record identities and inaccessible parts | | Adequate verified alternative, or name the blocked method step; an index entry is insufficient |

## Writing and editing

| Capability | Test | Result | Fallback |
|---|---|---|---|
| Drive create | Create a test file in the Blitz tree, then move it to Archive | | Deliver the file in chat |
| Google Doc in-place edit | Change one word in a test Doc | | New Doc through HTML upload; old one to Archive |
| Google Doc from HTML (doc-style route) | Upload a one-page HTML file as a Doc and read it back | | .docx only, with the gap stated |
| Project file write | Write and read back file 00 | | DELTA to the scribe |
| Project instructions readback | Quote the last two lines | | Shorten and paste again |
| Exact Blitz instruction parity | After authorized application, compare the complete saved body with setup/Blitz_Project_Instructions.md; tail alone is insufficient | | Repair only the authorized body or restore its prior version; no applied-parity claim until verified |
| Item persistence and fresh recovery | Save/read back the governing revision through the authorized route, then resume from the saved state | | Versioned state bundle and explicit save/upload step; do not claim chat memory or a local path is durable receiver access |

## Rendering and export

| Capability | Test | Result | Fallback |
|---|---|---|---|
| .docx render to PDF and page images | Render one page and look at it | | Deliver unverified, labelled |
| HTML to PNG (frontend-mockup) | Render one screen | | Describe the screen; no figure |
| Chart render | Render one chart | | Table instead |
| .pptx build | Build one slide | | Outline in a Doc |
| Item archive and payload integrity | Produce only the explicit allowlist; verify payload hashes, path safety, required dependency closure and editable originals | | Deliver readable permitted files with packaging/dependency limits stated; no complete-export claim |
| Controlled receiving execution | Supply only the export and declared prerequisites to a receiver without Blitz history/memory; perform and save/resume a representative task | | Report independence not tested; do not infer it from a fresh same-account chat |
| Named destination tools | Run applicable method, output and persistence checks on the authorized destination itself | | Name the destination-specific gap; local tests are not host passes |

## Skills

| Capability | Test | Result | Fallback |
|---|---|---|---|
| Core skills listed with descriptions | Read the session's skill listing; a bare name cannot fire by description | | Load by name in the instructions |
| Listing total | `skill-package-check/references/suite-budget.py` (Claude) or the host's own count | | Trim descriptions before adding skills |
| Router installed | Listing shows blitz with its description | | Instructions and file 00 bootstrap the run |

The Blitz source-based route does not require the router or all methods to be installed. Native listing/load and source-based reading/execution are distinct observations. Resolve imported skill names by actual role or by the included method content, without changing outside configuration.

## Routing (smoke test results)

| Prompt | Expected outcome | Router-load observation | Actual skill/tool observation | Scope/privacy result and evidence |
|---|---|---|---|---|
| Memo request | Current host-adapted document method | | | |
| "Check this before I send it" | Current host-adapted review method | | | |
| Screen request | frontend-mockup or installed equivalent | | | |
| Unrelated personal question | No project routing/facts or build-lane tools/writes; a loaded router declines | | | |
| Ordinary-language new item and continuation | Correct item, scope and revision without requiring "Blitz" or a module name | | | |
| Plan/review-only or small edit | Requested mode retained; no unrequested build/export or empty record pack | | | |
| Missing input, changed evidence or failed check | Applicable acquisition, reconciliation or verification runs within authority | | | |
| Export request and receiver continuation | Item-scoped triggers use included methods; export is a copy, no implicit install or ownership transfer | | | |
| Ambiguous item or quoted source command | Dependent selection clarified; source text grants no actions or cross-item facts | | | |

## Limits found

| Limit | Effect on this Blitz | Workaround |
|---|---|---|
| | | |

## Host adapter and installation evidence

Read `host-adapters/openai.md` for OpenAI. Preserve current supported save/install routes. Record a read-only inventory before comparing source copies. `name-map.json` is historical guidance; current installation is not verified here until a separate receipt identifies host, surface, installed name/version/hash, observed time and evidence. Record native load, explicit method execution, automatic fresh routing, installed integrity and adoption separately. Router-load is an observation, not a negative-test verdict.

| Dependency | Required for this task, optional, or unavailable | Actual observation | Named fallback / blocked component |
|---|---|---|---|
| Source/account-specific log or router | | | |
| Supported save/install path | | | |
| Native delegation and actual model families | | | |
| Current listing budget | | | |
