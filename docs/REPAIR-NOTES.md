# v2.1OAI-r1 repair map

This content revision keeps one maintained Blitz source and one primary master archive. Start at `Blitz/START.md` in the extracted master. The source compiler, 25 methods and host staging remain optional. No installer or company formation service is added.

| Finding | Repair and regression evidence |
|---|---|
| Preview boundary | Explicit loopback bind; canonical containment before reads; traversal, malformed URL, symlink, read and stream failure cases in `tests/node/test_preview.mjs`. |
| ZIP scan gaps | Bounded inspection of bodies, names, comments, prefixes, trailers and supported metadata; unsupported or opaque structures require review. Synthetic cases in `tests/test_audit_security.py`. |
| Incomplete history | Shallow repositories fail with a machine-readable reason, without fetching. Full-history removed-marker and clean-history controls remain. |
| Collection and recording | Copy-ready templates scope evidence and disclosure authority, recipients, transfer, redaction, recording permission, notes fallback and retention responsibility. |
| Unknown permissions | Unknown and confirmed denial are separate schema values and visible states; omitted cells remain unknown. |
| Contrast | Ordinary text requires 4.5:1; the 3:1 large-text exception uses 24 CSS px regular or 14pt bold (about 18.67 CSS px). |
| SVG export | DOM selection preserves the outer SVG and nested icons, resolves computed presentation styles and rejects unsupported active/external dependencies. The browser regression compares the saved standalone image with its styled source. |
| Diagram geometry | Documented data-flow, security-matrix, state, timeline and medallion geometry agrees with the existing linter. Negative controls remain; all 105 shipped HTML assets are invoked, including two explicitly skipped galleries. |
| JavaScript checks | Both recipes use one HTML parser helper. It checks each classic/module body, distinguishes data blocks, rejects invalid syntax and reports unchecked external scripts. It does not execute scripts. |
| Pyramid example | The fictional rewrite retains supplied facts and identifies missing decision evidence. |
| Staging links | Each stage carries a byte-identical source snapshot and rewritten links to required context. Tests check all 24 candidates and transitive Markdown links. The snapshot is comparison/source material, not a native installation payload. |

The master adds a short company/department entry route. Both routes require delivered and accepted work, an accountable owner and a feasible next cycle. Company cash and department budget/resource reconciliation remain distinct. Existing license terms, notices and the four core record names are preserved.

The current source, filenames and emitted source sets use standalone Blitz naming. Historical Git objects and original archives are preserved. Migration paths and renamed compiler entry points are in [MIGRATION.md](MIGRATION.md). Artwork changes and inspection evidence are summarized in [the artwork receipt](assets/README.md).

## Reproduce the checks

Use Python 3.12+, Node.js 24 and Chrome for the browser regression. From the repository root:

```sh
python -B tools/check_publication.py
python -B Blitz/setup/verify_kit.py
python -B Blitz/evals/run_all.py --kit Blitz --out .verification/local
python -B -m unittest discover -s tests -p 'test_*.py' -v
python -B tools/release.py build --out .dist/first
python -B tools/release.py build --out .dist/second
python -B tools/release.py compare .dist/first .dist/second
python -B tools/check_identity.py --root .dist/first --artifacts
```

Create `.verification` and `.dist` first; each output directory must be new. Publication scanning needs complete local history. On Windows without symlink privilege, the kit's symlink fixtures error and two preview cases explicitly skip; this is not an all-green run. Linux CI must execute them. The browser regression requires Chrome and does not silently skip a missing browser.

The source identity checker reports binary material for visual review; it cannot read text inside images. The reviewed artwork receipt pins the current GIF. Heuristic publication scanning is not proof that arbitrary content is secret-free. Syntax, integrity, staging, rendering and packaging checks do not prove demand, compliance, host installation or business readiness.

Release results belong to the immutable candidate's CI run, release manifest and independent review. Do not substitute this repair map for those results or reuse results after changing the candidate.
