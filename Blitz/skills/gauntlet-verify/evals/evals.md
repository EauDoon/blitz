# gauntlet-verify evals

Moved out of SKILL.md 25-09-2026. Not loaded with the skill.

## Cases

1. Give it "build me a pricing page as good as Linear's". Passes if, before generating, it names the reference, the single matched property, how the judge will see it, the formation, and the ceiling, then decomposes by independent area (one builder per area only at full formation) and states the craft-tell stop condition. Fails if it writes a rubric, which means `cold-read` should have taken the question.
2. Give it "dig into whether Hyperliquid's fee revenue really passed Ethereum's, it goes in a public thread this week". Passes if verification mode fires unprompted at light formation (public statement, unprompted), escalates to full only if its verifier leaves a blocker open, runs `research-protocol`'s method with isolated verifiers told which primary-data tools they have (DeFi Brain when its tools are loaded; silent fallback to explorer and primary-source reads when not), and ships every claim labeled verified, reported, or unverified. Fails if the drafting context verifies its own claims, or if a "check this before I send it" prompt on a finished artifact gets taken from `cold-read`.
3. Give it a light-formation build with contained stakes that has just reached ship-ready. Passes if it seats exactly one judge at that point and none earlier, and a craft tell from that judge opens another round instead of shipping. Fails if judges ran every round at light, or if a craft tell was read as done.
4. Give it a high-stakes job with two claim clusters, say a figure going into a counterparty term sheet that rests on two sources. Passes if it runs full formation, one verifier per cluster, and names the escalation in one line. Fails if the area count drops it to light.

5. "the market report you gave me is maybe 70% there. it has to survive the board on monday. keep iterating until you can't find anything wrong with it" (trigger eval P2). Passes if gauntlet-verify takes it as an unfinished build, names the bar and a ceiling, and starts light. Fails if cold-read takes an in-progress build.
