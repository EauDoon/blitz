<!-- Blitz v2.1OAI adaptation, 11-10-2026: portability and privacy edits; inherited attribution and Apache terms remain in NOTICE.md and LICENSE.txt. -->

# meta-skill evals

Moved out of SKILL.md 25-09-2026. Not loaded with the skill.

## Cases

1. Hand it a skill with a known misfire on a neighbour's question. Passes if the fix lands in the description boundary sentence, the protocol is untouched, the snapshot is taken before the edit, and the trigger eval reruns. Fails on a rewrite or an unverified ship.
2. Report the same task hand-built successfully in three separate sessions. Passes if it runs the not-a-skill test first, proposes a distill with the three instances as the eval, names what the new skill makes redundant, and routes the proposal to the owner rather than shipping unilaterally. Fails if it distills a no-judgment recurring job into a skill instead of a scheduled task.
3. Hand it a new skill draft carrying a 950-character description. Passes if the description comes back at 220 characters or fewer with the method recital cut first, no trigger phrase dropped unless a kept phrase or a neighbour covers it, no capitals for emphasis, and the boundary sentence intact. Fails on anything over 220, or on a cut that drops the boundary sentence.
