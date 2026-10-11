# metric-pull evals

Moved out of SKILL.md on 25-09-2026 so the skill does not read its own pass bar.

## Case 1

"What is TVL on protocol X" passes only if the answer returns two named independent sources, the exact TVL definition used including double count treatment, the chain scope, an as-of timestamp with timezone, and an explicit flag with the delta when the sources disagree beyond tolerance. Any one missing is a fail, and an unflagged single source number is the worst failure because it looks finished.
