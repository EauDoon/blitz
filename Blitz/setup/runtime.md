# Blitz v2.1OAI-r1 task-local runtime

The readable Blitz views support method selection. `Blitz_v2.1OAI-r1_Runtime.zip` supplies the exact selected local files those methods can require, including scripts, assets, licenses, shared templates, and setup helpers. It is a resource archive, not a native skill installation or proof that every tool works on this host.

## Open only when the selected task needs resources

1. Read the current `Blitz_v2.1OAI-r1_Method_Index.md`. It supplies exact names and SHA-256 fingerprints for the runtime, standalone opener, exporter, and export contract. Obtain these supplied files through the current host's supported file route. A filename or successful search hit alone does not prove matching bytes.
2. Verify the downloaded opener's SHA-256 against that trusted index before executing it. Use an observed Python 3.9 or later interpreter. Verify the runtime against the pinned archive hash with the opener. Choose a new task-local destination whose parent exists, outside live skill, plugin, or configuration directories.
3. Invoke `python Blitz_v2.1OAI-r1_Open_Runtime.py ARCHIVE --expected-sha256 HASH_FROM_INDEX --extract-to NEW_TASK_DIRECTORY`. Substitute the actual verified interpreter, archive, trusted fingerprint, and destination. Existing targets are rejected. Failed validation publishes nothing. Successful opening preserves the `Blitz/` prefix and executes no resource scripts.
4. Read the selected original method and its required references under the opened `Blitz/` directory. Inspect executable resources and actual capabilities before running them. Do not reconstruct scripts from prose views, assume platform-specific paths exist, or install dependencies without applicable authority.

For a normal item export, the standalone `Blitz_v2.1OAI-r1_Export_Item.py` and `Blitz_v2.1OAI-r1_Item_Export_Contract.json` are directly supplied. Verify their fingerprints from the index and follow [item export](item-export.md). They do not require opening the full runtime. The JSON is an unapproved template; fill it for the actual authorized item.

## What travels and what does not

The compiler includes all 25 selected method subtrees except evaluation cases, fixtures, answer keys, generated outputs, hidden folders, dependency caches, and builder history. Supporting scripts used by a method to evaluate a user's work remain ordinary resources. All available selected local dependencies and licenses travel together. The internal manifest lists every payload file and hash; the manifest itself is excluded from its own hash list. The trusted archive fingerprint covers the manifest too.

External Python/Node libraries, browsers, fonts, document or image renderers, media encoders, connectors, credentials, host APIs, native agents, and outside stores are not bundled or granted. Check the selected method, source code, and manifest dependency notes. Local-resource completeness is not a guarantee about dynamic imports, generated files, unavailable external tools, or execution on an untested host.

Missing required resources block only the dependent operation. Use an adequate available alternative when it meets the commission, or state the exact missing dependency and preserve usable work. Never claim a render, save, native load, upload, or install happened because the method describes it.

## Reproduce the Blitz source set

From a complete master kit, use `python setup/build_context.py --kit KIT --out NEW_OUTPUT_DIRECTORY`; `--dry-run` validates without writing. The parent directory must exist. The complete source set is staged and verified, then published atomically without replacing an occupied target. Ordinary failure removes only this run's temporary sibling; abrupt termination can leave a hidden `.source-context-*` scratch directory, never a completed output.

Every direct alias is copied from source bytes. The compact index pins executable aliases and the runtime archive; `Blitz_v2.1OAI-r1_Context_Manifest.json` pins every generated artifact except itself and carries the complete source/reference audit. The enclosing release manifest pins that JSON. Generation does not advance deployment or adoption status, execute methods, alter memory, install skills, or write outside the selected new output directory.
