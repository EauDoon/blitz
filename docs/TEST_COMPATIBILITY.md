# v2.1 compatibility checks

The original `Blitz/evals/lean-baseline-contract.json` remains unchanged. Its
historical byte hashes identify the earlier release; they are not claims that
authorized v2.1 wording changes retained identical bytes. The v2.1 contract
records the verified v2 archive/manifest hashes and the original source hashes.

| Changed lock | Why it changed | Preserved invariant and negative evidence |
|---|---|---|
| Four record byte hashes | The founder-facing setup is proportionate and owner-neutral. | Exact original headings, table columns, named fields and status/format lines; required authority, adoption, evidence, append-only and private-lane rules. Mutants deleting decision rights, adoption permission, allowlist limits, evidence provenance, source ID or isolation rules fail. |
| Original 42-test byte hash | Three account-specific optional capability labels became generic role labels. | All 42 test identities and the complete executable AST remain exact after normalizing only those three literals. Their current labels are checked separately. Renaming a security test or inverting its source-authority assertion fails. Native symlink tests are unchanged. |
| Router evaluation byte hash | A dated personal spending decision became an explicit spending-authority requirement. | Generic routing and negative-routing files retain their byte hashes. The router fixture retains all cases, order, expected behavior and positive 2-of-3/negative 3-of-3 thresholds; only the spending sentence is normalized. Dropping a case, relaxing the positive threshold or removing a negative restriction fails. |

`compatibility_errors` is the same pure function used for current candidate bytes
and mutated in-memory copies. Mutations never edit source files. It also protects
the referenced source/claim records and item scope gate, so preserved headings
cannot conceal a dropped provenance or cross-item isolation rule.

Run `python -B Blitz/evals/test_oai_lean.py`. These are static and synthetic checks;
they do not establish successful native routing, live model behavior or permission
to act. Original baseline results remain separate, including the native Windows
symlink privilege errors; no failure is relabeled as a pass by this revision.
