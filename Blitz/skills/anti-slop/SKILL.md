---
name: "anti-slop"
description: 'Pattern pass on prose he publishes, sends or signs, and the scored post pass for X and LinkedIn. Use on "de-slop this", "does this sound like AI", "this feels robotic", or before a post ships. Never changes a fact.'
---

# Anti-slop

Two layers. Part 1, the floor, is this file and runs on prose the owner will publish, send or sign. Part 2, the post pass, lives in `references/post-pass.md`: read it and run it in full on any X or LinkedIn post, quote tweet or reply. The posting skills call it last. Chat replies to the owner follow the current account instructions, not this skill.

The other three writing lanes: `house-style` holds the mechanics and the one canonical banned-word list, `my-writing-style` holds the voice and the STE caps, and `write-with-pyramid` sets argument structure.

## Which part runs

| Surface | Run |
|---|---|
| X post, quote tweet, X reply, LinkedIn post, configured channel post | Part 2 (`references/post-pass.md`) in full, in its own order. Part 1's mechanisms back up the Step 2 scan |
| Document, report, memo, deck, Google Doc | Part 1 only, run on the source text before the build |
| Email, Slack or Telegram message, counterparty note | Part 1 only |

Where the two parts disagree on a post, Part 2 governs on that surface. One "not X, it is Y" per post is his move (Part 2, Steps 1 and 5). Mechanism 3's zero tolerance applies everywhere else, and to any second use on a post.

# Part 1. The floor

## Precedence, read this first

1. **`house-style` wins on words.** It holds the one canonical banned-word list and the banned phrases; `my-writing-style` holds the voice and the STE caps. This skill does not restate either. The canonical bans are flat: no density allowance, no tier below them.
2. **The channel skill wins on register.** `the configured X-post method`, `the configured X-reply method`, `the configured LinkedIn method` and `the configured channel method` own their rhythm, their closers and their warmth. Where one of them states a rhythm rule, apply that rule as written. Where one is silent, the Profiles table below supplies the default. Never overrule a channel skill on its own surface.
3. **Protected signatures survive the pass, on the surface that owns them.** The protect list is per surface, and it is held by the channel skill, not by this file. On X: deliberate fragments, an "And" opener, "leh", "liao", "sia", "bro", "haha", and the pet terms those skills list. Everywhere with his byline: first-person framing from his operating seat, and "ecosystem" in its literal domain sense. Documents, counterparty messages and contracts carry no fragment or Singlish protection at all; ASD-STE100 and `house-style` govern there. When a rule collides with a protected signature on its own surface, surface the collision and leave the text alone.
4. **This skill wins on mechanisms**: what the word lists cannot see.

## Standing adaptations

Three rules differ from the upstream skill (history in `references/history.md`). Do not re-import the upstream text over them.

- **Sentence-length uniformity is not a tell on STE surfaces.** ASD-STE100 caps produce uniform rhythm on purpose, so the uniformity rule and the dense-prose rule are off on documents and counterparty messages. They stay on for LinkedIn and original X posts, where `the configured X-post method` states "vary sentence length" in its own mechanics.
- **Em dashes and en dashes are zero on every surface**, including headings, spreadsheet notes and Read Me tabs. Catch the em dash glyph, the en dash glyph and the double-hyphen substitute. Hyphens inside compound words and identifiers are fine.
- **No verifier subagent.** `cold-read` runs isolated evaluators on shipped artifacts, and every document build runs this floor on its source before delivery. Do not spawn a second one. On surfaces cold-read never sees (a counterparty email, a Slack message), this floor is the only pass, so run the gate below properly.

## Modes

- **rewrite** (default): flag, return the clean version, show what changed and why.
- **detect**: flag only, grouped P0 / P1 / P2. No rewriting. Use on published text, on someone else's draft, or when the owner asks whether something reads like AI.
- **ingest**: the owner pastes slop, or a session catches its own. Name the mechanism that generates it, write the replacement, then record it only in the current user's explicitly authorized project log, respecting the boundary in `references/history.md`. When the surface is social, add the recurrence count and the gate that should have caught it to the corpus entry.

Never declare a text AI-written. A named pattern is checkable evidence. An authorship claim is a guess.

Never invent. No fact, name, number, date or quote enters a rewrite unless it was in the source. A rewrite that reads better and says something new is a defect, and a fabrication is always a blocker.

## The mechanisms

Structure first, words second.

**1. False agency.** An inanimate thing doing a human verb, used to avoid naming the actor. "The data tells us", "the market rewards", "the decision emerges", "the integration unlocks", "adoption follows". Name the actor: the issuer, the desk, the buyer, you. This is the most common tell in draft output written for him, and no banned-word list catches it.

**2. Copula avoidance.** Circling around is and has. "The stablecoin is the settlement leg", never "the stablecoin serves as the settlement leg". The specific verbs are already in `house-style`'s canonical list; this is the mechanism that keeps producing new ones.

**3. Binary contrast.** "Not X, it's Y." "The question isn't X, it's Y." "X isn't the problem, Y is." "Stops being X and starts being Y." Also "not only X but also Y", "it's not just X, it's Y", and the short tailing form: a clause that ends by naming what the thing is not. Drop the negation and assert the positive. Zero tolerance on anything with his byline, including the prose of this file. The one exception is a single use per post on X and LinkedIn, per "Which part runs" above.

**4. Mannered prose.** A metaphor or flourish standing in for a plain statement: "a dial worth turning" for "a parameter worth varying", "earns its keep" for "still matters". The phrase displays the writer instead of carrying the idea, and it imports connotations nobody chose. Use the literal phrase when one exists. Exception: a protected term, and a word with a real technical meaning in context.

**5. Dense prose.** A paragraph past about 100 words with no break, where more than half the sentences run over 30 words. Break the sentence at its second clause and the paragraph at its second idea. OFF on STE surfaces, where the caps bind harder already.

**6. Synonym cycling.** "Issuers... providers... operators... players" inside one paragraph, to avoid repeating a word. Repeat the right word. One word, one meaning is already the STE rule; this points the same rule at elegant variation.

**7. Seam monotony.** How consecutive thoughts connect. `house-style` bans "additionally", "moreover" and "furthermore", and the failure that follows a ban like that is displacement: the metronome moves to another word and the seams stay uniform. Vary the shape of the connection, not the word. A fragment, a flat statement, a callback, or nothing at all. The best transition is often none: start the next thought. Never manufacture connective tissue where the thought already connects. A rare or showy transition is its own tell; fit beats novelty.

**8. The portability test.** If a sentence could move unchanged to another company, another token or another partner and still read fine, it says nothing about this one. Cut it or make it specific. On posts, Part 2's stance test covers the same ground; on documents and decks it has no equivalent gate, which is where it earns its place.

**9. Sterile prose is also slop.** Voiceless, evenly balanced, referee-from-nowhere writing is as machine-tellable as "delve". On anything carrying his byline the draft needs a position and a stake from his operating seat. State only the author's supplied position and experience; never invent a personal stake. Exception: reference material and technical description, where neutral is the correct human voice.

**10. Significance inflation.** A routine fact dressed as history. "A watershed for the industry", "the moment the market changed". State what happened. Promotional tone where neutral description belongs is the same failure.

**11. Template slot-fill.** A sentence with a blank where any noun would fit and it still sounds the same. "A major step toward broader adoption." Name the actual capability or the actual audience, or cut.

**12. Faux-insight setups.** "What most people get wrong is", "the part everyone misses", "here's what nobody tells you". Manufactured contrarianism as a hook. If the insight is real, state it. It does not need a crowd to be wrong first.

**13. Fake-profound kicker.** A closing line that converts the point into a metaphor for gravitas: "In the end, it was never about the rails." End on the last real point. This sits in the closing position, which Part 2's final-line check gates on posts and `house-style`'s answer-first rule gates on documents, so it needs its own rule rather than falling under mannered prose.

**14. Colon reveal.** "The answer: liquidity." "The result: nothing moved." Fine once in a hook, a tell when it recurs. Write the plain sentence.

**15. Narrator from a distance.** "Nobody designed this." "People tend to." Put the reader in the room, or name who did it.

**16. Validation tails.** A clause appended to your own fact that reports your approval of what you are replying to: "so this one lands", "which is why this tracks". Delete on sight. The fact already proved the relevance. Highest-value rule on X replies.

**17. Acknowledgment loops.** "To answer your question", "the question of whether", restating the prompt before answering. Just answer.

**18. Confidence-calibration adverbs.** "Interestingly", "importantly", "surprisingly", "undoubtedly". Let the fact carry its own weight. Flag by density: one in 2,000 words is fine, three in 500 is a tell. "Notably" and "notable" get no density allowance; `house-style` bans both outright.

**19. Novelty inflation.** Treating an established idea as a discovery ("a failure mode nobody names"). Say what the person did with the idea.

**20. Emotional flatline.** Claiming the feeling instead of earning it: "what surprised me most", "I was fascinated to find". If it is surprising, the content shows it.

**21. False ranges.** "From retail wallets to sovereign reserves." "Everything from settlement to compliance." List the real items, or pick the one that matters.

**22. Chatbot residue.** The phrases in `house-style`'s chatbot residue list, plus "as of my last update" and "you're absolutely right". Strip entirely. P0.

**23. Vague attribution.** "The market expects", "industry leaders agree" with nobody named. Name the source with a date, or drop the attribution and own the claim.

**24. Signposting openers.** "Let's dive in", "here's what you need to know", "let me break this down", "step 1". Announcing the move instead of making it. Start with the point.

**25. Document formatting tells.** On documents, decks and long-form: a heading followed by a one-line restatement of itself before the real content, bullets that open with a bold header repeating the bullet, title case in subheadings, every section forced to the same length and shape, and curly quotes. Cut the warm-up line, strip the repeated header, use sentence case, let sections take their natural length, use straight quotes.

**26. Rule of three.** Stacked adjectives or phrases in threes, or three parallel clauses doing one job. Pick the one that matters. Three items with distinct referents (three parties, three dates) are an enumeration, not a tell.

**27. Participle tail.** A sentence that ends in a vague "-ing" clause to fake insight ("..., highlighting its importance", "..., reflecting broader trends"). Cut the clause; the fact stands alone.

**28. Conclusion scaffolding and padding.** "In summary", "In conclusion", "Overall", "Ultimately" as a wrap-up crutch, or "One of the most important things to consider is..." before the point. Make the point and stop.

## Severity

- **P0, credibility killers.** Chatbot residue, cutoff disclaimers, vague attribution, significance inflation on a routine event.
- **P1, obvious AI smell.** Binary contrast, false agency, copula avoidance, mannered prose, template slot-fill, validation tails, faux-insight setups, fake-profound kicker, synonym cycling, seam monotony, rule of three, participle tail, conclusion scaffolding, and any word or phrase on `house-style`'s canonical list.
- **P2, polish.** Colon reveal, narrator from a distance, confidence adverbs, emotional flatline, false ranges, formatting tells.

A quick pass clears P0 and P1. A full audit clears all three.

## Profiles

| Surface | Rhythm and dense prose | Portability | Stance required | Em and en dash |
|---|---|---|---|---|
| X post | vary rhythm, per `the configured X-post method` | strict, covered by Part 2's stance test | yes, first person from the seat | zero |
| X reply | off, the unit is too short to score | strict | yes | zero |
| LinkedIn | vary rhythm, this skill's default | strict | yes | zero |
| Google Doc, report, memo, deck | off, STE governs | strict | no, the verdict carries it | zero |
| Contract, term sheet | off | skip | no | zero |
| Internal reply | off | relaxed | no | zero |
| Counterparty email or Slack | off, STE governs | strict | no | zero |

## The gate, before anything is delivered

Two questions, answered honestly:

1. **What still makes this read as AI-generated?** Whatever you name, fix. "Nothing" is a valid answer on an already-clean draft, and naming a tell you cannot point at in the text fails this gate the same way missing a real one does.
2. **Does the rewrite state any fact, name, number, date or quote that was not in the source?** A fabrication is a defect even when it reads more human.

If question 1 keeps returning the same class of tell across passes, stop patching and rewrite from a tighter brief.

## Minimum effective edit

Fix the tell, leave strong sentences alone, cut in proportion to the actual slop. "This text is fine" is a valid verdict. Over-editing human prose sands it back toward the same uniform profile that reads as machine output, which is the failure this skill exists to prevent, pointed the other way. When in doubt on his byline, defer to the protected signatures in precedence rule 3.

When cleaning someone else's draft with no voice spec, note the core point and three to five voice signals before editing, then preserve them. De-slopped text that lost its author has failed.

## Self-reference

When the text is ABOUT slop (this file, an example, a quoted bad draft), do not flag the quoted patterns. Flag only the author's own prose.

## Credits

This adapted file is distributed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), with the exact scope in [LICENSE.txt](LICENSE.txt). It incorporates Kevin Magnan's anti-slop and the credited humanizer/Wikipedia and MIT lineages. [NOTICE.md](NOTICE.md) retains creator/source attribution, unchanged MIT notices and the modification record. The license repair on 11-10-2026 changed attribution only.
