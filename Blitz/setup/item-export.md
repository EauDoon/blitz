# Export one item

Use `setup/export_item.py` with a verified Python 3.10 or newer interpreter. It uses the standard library and does not extract archives, follow links, run packaged scripts, install skills, or modify project instructions. It handles item archives; the separate `verify_archive.py` handles Blitz master/runtime archives and offers explicitly requested trusted-hash extraction.

## Review shared sources at the content level

An allowlisted filename can still contain rows, columns, comments, worksheets or attachments belonging to another item. Before approving export, the reviewer checks the actual content against the named item and destination. A valid manifest cannot detect that mistake. For a shared CSV, make a new item-only projection instead of shipping the whole source. Review both the selected rows and each selected column, including free-text cells that may mention other items or private information. Projection does not establish permission or detect sensitive text inside an otherwise selected cell.

`setup/scope_csv.py` is an optional, runnable preparation tool. It uses Python's standard library and the path/publication guards in `setup/verify_archive.py`; keep those two files together in a trusted Blitz checkout. It accepts one UTF-8 CSV (optional BOM), a separately trusted source SHA-256, a caller-supplied source revision, an exact case-sensitive item-ID column/value and an explicit ordered list of output columns. The item-ID column must remain in that list so the resulting rows can be checked. There is no prefix matching, inferred dialect, automatic column selection or interpretation of cell contents as instructions.

```text
python3 setup/scope_csv.py create --source work/shared.csv --expected-sha256 TRUSTED_SOURCE_SHA256 --source-revision shared-r07 --item-column item_id --item-id SYNTHETIC-A --column item_id --column amount --column description --output work/scoped-a-r01
python3 setup/scope_csv.py inspect work/scoped-a-r01 --expected-receipt-sha256 TRUSTED_RECEIPT_SHA256
```

Replace the two uppercase hash placeholders with separately trusted lowercase SHA-256 values. Record the `receipt_sha256` returned by `create` outside the projection, then use it for `inspect`. The new directory contains only `projected.csv` and `provenance.json`. The receipt records original source hash/revision, input bytes and row count, the exact filter, selected columns, output row count/bytes/hash and the tool's limits. It contains no raw source, source pathname, unselected row values or unselected column names. Source revision is the caller's assertion; the tool binds it to the supplied bytes but cannot establish its truth.

The output parent must already exist. The destination must be new, with no source/output overlap, symlink or reparse component. Both files are prepared and checked before atomic no-replace directory publication on Windows or Linux. Unsupported publication primitives fail closed. Existing files/directories are not replaced; the shared source stays unchanged. Bounds are 64 MiB per input/output, 250,000 data rows, 256 columns and 1 MiB per field. The fixed dialect rejects duplicate or case-colliding headers, missing/blank/padded names, ragged or ambiguous quoting, empty/padded item IDs, zero matching rows, and mixed IDs in a checked output. It accepts quoted commas, escaped quotes, multiline cells, and LF or CRLF line endings; bare CR is rejected.

The receipt hash protects its declarations from later change only when obtained independently. `inspect` checks those declarations and output bytes, not the original source or the truth of permission/revision claims. Spreadsheet formulas and instruction-like cells remain unchanged data. Do not run cells or rely on this tool to make a spreadsheet safe to open. A reviewer still checks semantic isolation and sensitive content. Keep the shared original under its original access controls, then stage only the approved projection and receipt and pin each file's hash in the item-export contract below. File integrity and content review are both required. Use a stable local filesystem with source and output parents frozen during execution; path guards do not sandbox a malicious process concurrently changing those directories.

## Prepare the explicit contract

Stage only the permitted item files under one directory. Preserve the existing commission, records, and handoff meanings. Include `README.md` and `PROJECT_INSTRUCTIONS.md` at its root. The latter must bind ordinary-language and supporting triggers to this item, its included methods, its current authority, and its named destination. Root instructions must not depend on Thor history or global skill installation.

Copy `templates/item-export.json` into a working contract outside the staged files. The template is a synthetic shape example, with reviews deliberately unapproved. Replace its identity, destination, file rows, and hashes using the actual reviewed item. A reviewer records the real export and dependency review before setting its two review booleans to true. These statements are provenance, not proof of legal permission or automated content review.

Every file row requires:

- `path`: exact relative POSIX file path, including case. No directories, globs, absolute paths, aliases, or generated manifest row.
- `sha256`: lowercase SHA-256 of the exact approved file bytes. Hashes are pinned before packaging, never silently refreshed by the exporter.
- `revision`: the file's source revision or snapshot identity. The item `revision` must match the explicitly supplied expected revision.
- `classification`: `public` or `permitted`, based on actual export permission. Private material and credentials are prohibited.
- `role`: `record`, `deliverable`, `source`, `method`, `license`, `verification`, or `runtime`.
- `dependencies`: explicit paths of all required local dependencies, including nested method references, scripts, assets, and licenses. An external dependency uses `external:ID`.

`required_paths` lists any additional files the acceptance contract requires, such as editable originals or a governing record. README and project instructions remain mandatory even if omitted from this list. Nothing outside the allowlist is copied. File hashes cannot prove that an omitted deliverable is unnecessary, so coverage against the commission remains a separate review.

For an external prerequisite, record `id`, `locator`, `required`, `status`, and `evidence`. Allowed statuses are `verified`, `unavailable`, and `not_tested`. Required prerequisites must be verified with evidence of the intended receiver's access or capability. Verified optional prerequisites also need evidence. An unavailable required prerequisite prevents building a complete export. Produce a gap report instead of marking it verified. Software runtimes, tools, and account permissions are not transferred by a ZIP. The manifest records when required external access remains part of the bundle's operating requirements.

`reference_exceptions` permits only explicitly reviewed, nonrequired examples. Each entry identifies the exact `source`, raw link `target`, `kind: "nonrequired_example"`, and a meaningful `reason`. Do not use this escape hatch for missing required knowledge, private data, or an inaccessible required Thor reference. No exception can authorize exporting a prohibited file. Unknown contract fields are rejected so unreviewed metadata cannot quietly enter the manifest alongside the allowlist.

## Build and inspect

Example commands assume `python3` is the already verified interpreter on the receiving host. On Windows, substitute a detected interpreter or its absolute executable path.

```text
python3 setup/export_item.py build --root work/item-r01 --contract work/item-export.json --output exports/item-r01.zip --expected-revision r01
python3 setup/export_item.py inspect exports/item-r01.zip --expected-item-id EXAMPLE-ITEM --expected-revision r01
```

The output directory must already exist and be outside the staged item. Existing destinations are never overwritten. The exporter snapshots the allowlisted bytes, checks their approved hashes, writes a deterministic archive to a temporary file, inspects it, then publishes it atomically using a filesystem hard link. Filesystems without that primitive fail rather than use a partially visible or overwriting fallback. Temporary files are removed on ordinary success or failure; interruption can leave a `.item-export-*.zip` scratch file, which is never a completed export.

The JSON result includes the archive SHA-256. Record it in the separate delivery receipt. Independently compare that trusted receipt before accepting a received ZIP, or supply its exact value using `inspect --expected-sha256 HEX`: a self-contained manifest detects inconsistency, not malicious replacement of both files and their hashes. Successful `inspect` verifies declared identity, paths, hashes, sizes, and dependencies. It does not establish correct decisions, permission, runtime behavior, or successful adoption.

Receivers use the same script from a trusted Blitz release or a separately verified copy. Packaging it as `runtime/export_item.py` is optional and requires an explicit file row like any other dependency. Merely including a checker in an untrusted archive does not make it trustworthy; do not execute supplied scripts as part of inspection.

## Checks and limits

Both build and inspection reject duplicate or case-colliding paths, Windows reserved names, unsafe characters, traversal, links or reparse points, special archive entries, encryption, payload changes, missing required paths or dependencies, incomplete required prerequisites, and unlisted archive entries. Build rejects hardlinked source files and the contract itself as payload. Each file is limited to 64 MiB, total payload to 256 MiB, and the allowlist to 4,096 files. The manifest is excluded from its own payload-hash list.

Known private, credential, evaluation-fixture, answer-key, and builder-note path patterns are prohibited. The original filled context lanes 06, 07, and 08 are excluded. These controls are not exhaustive secret detection: a credential or private fact can appear inside an innocently named document or binary. Human source/export review remains required, and no positive result means “secret free.” Source classification is a declaration, not a security boundary.

The checker conservatively resolves common inline Markdown links, reference-link definitions, angle-bracket HTTP/HTTPS/mailto autolinks, and quoted HTML `href`/`src` attributes in Markdown. It decodes HTML entities before classifying references and decodes URL paths when recognizing project links. Missing local link destinations fail, including nested method links; documented nonrequired examples need exact exceptions. A Markdown directory link is not a file dependency and must be replaced by an explicit file or reviewed as a nonrequired example. Quoted code examples are still scanned. Unsupported or ambiguous Markdown may fail and should be rewritten unambiguously, not silently ignored.

This is not a complete Markdown parser or a program dependency analyzer. Bare path mentions, dynamic imports, script-generated paths, non-Markdown resources, CSS assets, remote HTTP links, and semantic dependencies require explicit review and declarations. Standard HTTP/HTTPS/mailto links are accepted as references, not checked for availability or treated automatically as required inputs. Known ChatGPT project, chat, and share links are stricter: supply an exact prerequisite `locator` (compared after HTML entity decoding), mark it required with verified receiving-access evidence, and add its `external:ID` dependency to the source file row, or declare an exact raw-target nonrequired-example exception. Any required remote source must be declared as a verified external prerequisite or replaced by a permitted local copy. The review must catch reference forms the scanner does not recognize.

Dependency declarations must include the selected method's complete required closure; copying only `SKILL.md` is insufficient when it uses other files. Packaging never crawls a folder or retrieves undeclared sources to repair an incomplete allowlist. A passing archive is a reviewed export candidate. Apply the handoff receiver check, actual capability checks, representative execution, and save/resume test before claiming the item works in its destination.

Paths and reads are checked on a normal, stable local filesystem. This script is not a sandbox against another process adversarially changing path components during execution. Freeze the staging directory and output parent for the duration of the build.
