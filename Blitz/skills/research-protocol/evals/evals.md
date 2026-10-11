# research-protocol evals

Moved out of SKILL.md 25-09-2026. Not loaded with the skill.

## Cases

1. Give it a draft that quotes a live figure with its source and as-of date, where the source now shows a different number. Passes if stage 4 test 4 re-fetches, reports the difference, and relabels the claim unverified until the difference is explained. Fails if the figure ships because a source was named.
2. Give it "is this actually true" on a claim two outlets carry from one press release. Passes if the two count as one source and the claim grades reported, not verified. Fails if it grades verified on two tier B citations that are not independent.

3. "someone on x claims pyusd supply tripled since june. real or cope?" (trigger eval P2, which went to metric-pull on Opus 5.5 twice). Passes if research-protocol takes it, traces the claim to the issuer's own supply data or a contract read, and labels it verified, reported or unverified. Fails if the claim is graded on the post alone.
4. "research the state of agentic payments on stablecoin rails, who's live and what volumes" with DeFi Brain not loaded. Passes if it falls back silently to primary sources and web search and names the source of each figure. Fails if it halts or asks about the missing connector.
