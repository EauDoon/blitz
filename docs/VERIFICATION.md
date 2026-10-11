# Verification contract

Source identity, deterministic script behavior, assistant use, host installation and actual company outcomes are separate claims.

## Commands

Use a verified Python 3.12+ executable from repository root and new output directories:

```sh
python -B Blitz/setup/verify_kit.py
python -B Blitz/evals/run_all.py --out .verification/local
mkdir .dist
python -B tools/release.py build --out .dist/release
python -B tools/check_publication.py
```

The release runner records each suite command, result and output. Nonzero, blocked, skipped and unrun checks must not be reported as passes. Local logs may contain machine paths and remain ignored; the release receipt summarizes relevant results without personal paths.

Run the meaningful repository packaging tests as specified by CI, including two identical builds and source-drift/output-boundary failures. CI uses a fresh Linux checkout so native symlink defenses are exercised. The Windows baseline run is recorded separately, including OS privilege limits.

## Review layers

1. Verify the recovered original before editing and retain a before/after inventory.
2. Validate the new kit manifest, archive safety, method/resource closure, 17-source regeneration and runtime exclusion of evaluations/answer keys.
3. Exercise local company initialization and cash calculations, including unknown inputs, collection delays, reserve shortfalls, negative/nonfinite values, currency and period errors, and occupied/path-unsafe outputs.
4. Exercise shared CSV row/column isolation and trusted provenance, including mixed-item data, malformed input and tampering. Review truthful working-copy startup/lineage separately from file hashes.
5. Perform the first-user walkthrough from the saved candidate with a fresh reader who has not authored it. Record actual use and limitations; synthetic inputs do not validate a real company.
6. Review the exact saved commit independently, then confirm the same commit was pushed to the private repository and its CI result. Scan reachable history as well as current files before publication.

No paid model benchmark, natural-routing population claim, native installation, actual external business action or real founder adoption is part of this release's verification.
