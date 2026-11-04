# skill-package-check adaptation record

## v2.1OAI-r1 fix 2, 04-11-2026

Modified by EauDoon. `references/build-check.py` now fails an unquoted description that starts with YAML syntax: ``[ ] { } , & * ! | > % @ ` ``, or `-` or `?` before a space. PyYAML rejects most of these, and `&anchor text` or `!!str text` silently load different words. It also fails a description that opens a quote and has text after the closing quote (`'Use this' when asked`). A `|` or `>` block scalar header is now recognised: its indented text is the value, so `: ` and `#` inside it are no longer reported, and an empty block fails. The selftest adds a leading indicator, an early closing quote and a valid `>-` block scalar, and reports `9/9`. A comment after a closing quote (`'text' # note`) loads correctly but still fails; remove the comment.

## v2.1OAI-r1 fix, 04-11-2026

Modified by EauDoon. `references/build-check.py` passed two descriptions that do not load correctly. A single-quoted value with a bare apostrophe beside a doubled one (`'it''s the owner's call'`) made the YAML parser fail, because the old test skipped any value that contained `''`. It now requires the whole value to match `(?:[^']|'')*`. With an unquoted `#` at the start or after whitespace (`Use for deal pricing #1 priority`), YAML read the rest as a comment and silently truncated the description; that now fails. The selftest adds both cases and a doubled-apostrophe control, and reports `6/6`. `Blitz/setup/frontmatter.py` was not reused: this checker ships inside the package and runs standalone, and that parser rejects keys other than `name` and `description`.

## v2.1OAI, 11-10-2026

Adapted from the corresponding method in Blitz v2OAI. The method identity is retained. Personal profiles, account observations, private-case narratives and internal operating history were removed or replaced with configurable guidance and synthetic examples. The untouched v2OAI source remains a separately preserved baseline, outside this repository.

Method availability is not installation, successful execution, or evidence of business outcomes. Use current host capabilities and task authority. Existing licenses and attribution notices remain applicable; see `../provenance.md`.
