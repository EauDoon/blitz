# write-with-pyramid evals

Moved out of SKILL.md on 25-09-2026. Not loaded at run time.

## Eval checklist

Run these before trusting the skill on real sends.

| Test | Pass condition |
|---|---|
| Trigger, positive | Fires on five prompts: rewrite this email, why did nobody reply, tighten this email so it lands, structure this memo, make this ask land |
| Trigger, negative | Does not fire on: price lookups, casual chat, deck requests (pitch-architect), X post drafts (the configured X-post method) |
| First-sentence test | On five real sent-folder messages, the rewrite carries the ask or recommendation in sentence one, five of five |
| Compression | Rewrite is shorter than the input on at least four of five real samples |
| MECE catch | Given a planted overlapping point set, the overlap is named and merged |
| False-answer guard | Given an open question with no clear answer, it ships a decision frame rather than fabricating a recommendation |
| Hostile reader | Given a bad-news message to a resistant reader, it selects SCQA rather than a cold open |
| Composition | Output has no dashes, ranges written as X to Y, negatives in parentheses. No conflict with house-style |
| Narrative exception | Given an explicitly exploratory thinking document, it declines to pyramid and says why |
| Person-framed brief | Given a draft whose recommendation rests on a named colleague, the rewrite restates the ground as mechanism or number and moves the name to a structured position |

Failure on the false-answer guard or the narrative exception is more serious than a structural miss. Those are the two ways this method makes writing worse rather than better.
