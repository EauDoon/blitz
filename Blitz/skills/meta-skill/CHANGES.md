# meta-skill adaptation record

## v2.1OAI, 11-10-2026

Adapted from the corresponding method in Blitz v2OAI. The method identity is retained. Personal profiles, account observations, private-case narratives and internal operating history were removed or replaced with configurable guidance and synthetic examples. The untouched v2OAI source remains a separately preserved baseline, outside this repository.

Method availability is not installation, successful execution, or evidence of business outcomes. Use current host capabilities and task authority. Existing licenses and attribution notices remain applicable; see `../provenance.md`.

## Unreleased, 04-11-2026

`scripts/package_skill.py` skips symbolic links, and files under a linked directory, instead of following them into the `.skill` archive. A link inside a skill folder could otherwise pack a target outside it, such as a credentials file. Existing licenses and attribution notices are unchanged.
