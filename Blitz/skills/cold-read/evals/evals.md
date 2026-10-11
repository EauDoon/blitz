# cold-read evals

Built at birth per meta-skill; moved out of SKILL.md 25-09-2026. Not loaded with the skill.

## Cases

1. Trigger accuracy. Fires on "check this deck before Thursday". Does not fire on
   "what is the current MAS stablecoin framework".
2. Auto-fire held. A finished term sheet with no check request fires FULL without
   asking. "Rough pass" on the same artifact runs LITE, never off. "Draft the
   term sheet" runs FULL. An internal memo whose only trigger is a forecast
   table does not fire.
3. Rubric quality. Every criterion produced can be failed with a quote. Any
   criterion phrased as improve, strengthen, or make sure is a defect.
4. Isolation held. The evaluator prompt contains no trace of how the artifact was
   made and no framing of it as good.
5. Deterministic close. A numeric FAIL is closed only by a script the main thread
   ran; an evaluator's claimed recompute with no script voids the criterion.
6. It actually fails things. A run where all evaluators pass everything on a first
   draft means the rubric is too loose, not that the draft is clean.
7. Stop rule held. Never more than two revision rounds, and the run line reaches
   the connected project folder or is skipped and reported; never Claude's
   built-in memory and never only the session directory.
8. Portability. The protocol reads correctly with subagent replaced by second
   session or different model throughout.
