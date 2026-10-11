# anti-slop Part 2. The post pass

Loaded from `anti-slop` on any X or LinkedIn post, quote tweet or reply. Words come from `house-style`'s canonical list; this file adds only post-lane checks. The empty corpus boundary and a synthetic example are in `history.md`.

A subtract-only pass on a post with no stance returns a shorter post with no stance. So this pass starts with the stance and ends with a score against the owner's own writing.

Where it sits: after the draft is built and the claim ledger has closed, before the owner's edit. It replaces the closer rotation, the closer tally, the warmth scan and the question-closer cap in the posting skills, except for the counted checks in Steps 2b and 2c, which are mechanical and stay counted. It never changes a fact, a number, a date, a name, a quote or an attribution. If a sentence cannot be de-slopped without touching a fact, flag it and leave the fact alone.

## Step 0. Stance test, before anything else

Write one sentence: what does the owner believe here that a smart reader in his lane could disagree with as written. If the draft has no such sentence, stop and return the draft with the verdict NO STANCE. Do not de-slop a summary; a polished summary is still a summary. Exceptions: event and room posts (the stance is presence), and a reply whose whole job is one specific fact.

## Step 1. Voice reference

Use only voice examples supplied or authorized for this task. When none exist, state that the draft uses
the neutral style defaults in `my-writing-style`; do not claim to have matched the author's historical voice.

The following invented examples show concrete writing, not measured engagement or a real person's posts:

* "We tested the handoff with three sample orders. One had no named owner."
* "The repair is small: put the delivery date beside the promise."
* "Our next test is whether a new operator can complete the checklist without help."

Avoid repeating the same opening, contrast, or closing formula across a series. A synthetic example
is guidance for structure and is never evidence for a factual claim or audience performance.

## Step 2. Pattern scan

Mark every hit. Groups are ordered by how often they appear in the drafted illustrative posts.

**The distinction move, the shape of the retired stat single.** Source-shaped opener ("X published Y on date"), a figure, then "the interesting part is", "the real question is", "at its core", "what this actually shows", "both can be true", a rejected alternative nobody raised ("this is not about X", "one might think", "a tempting read would be"), an objection nobody made ("to be clear", "I am not saying"), then a credit closer. humanizer 27, 33, 34, 35. Rewrite from the seat: what the owner thinks, in the first sentence.

**The challenge closer (added 10-09-2026).** A final line that commands or dares the reader: "tell me where", "tell me how", "tell me where I am wrong", "make the case", "prove me wrong", "show me", "name one", "change my mind" as an order, "convince me", and the conditional dare "If you ..., <imperative>". It reads as stand-offish and it is the reply-bait shape, not an invitation. Rewrite as a statement of welcome ("Recommendations for the rooms worth the walk are welcome, and I will share the ones I find."), a specific credit, a dated forward pointer, or the first-person change-my-mind condition. Never as a question on a reply.

**The repeated formula (added 14-09-2026).** The same connective phrase doing the same job more than once in a post: "I weigh it because", "my arithmetic", "that is what I mean by", "the word I weigh", "which is why", "the point is". One use is a sentence; two is a template showing through. Also the reasons-paragraph formula "<fact>. I weigh it because <reason>." repeated per reason. Rewrite each reason so the sentence itself carries the weight ("The sample service starts with only one supported order type") and show a derived figure's operands ("62%, 412 over 668") instead of labelling it.

**Narrator from a distance and false agency.** "This happens because", "people tend to", "the market rewards", "the data tells", "supply signals", "the number says", "this tells you". stop-slop. Name the actor. When the actor is the owner, say "I" or "we". When the actor is a reader, say "you".

**Not X but Y, tailing negations, forced threes, false ranges.** "Not just X but Y", "no guessing", three parallel items where two would do, "from X to Y" where X and Y are not a range. humanizer 9, 10, 12. One contrast per post is allowed (see Step 1). A second is cut. Threes become twos or a plain list of what is actually there.

**Inflated importance and shallow -ing analysis.** "Marks a shift", "a pivotal moment", "reflects a broader", "setting the stage", and any trailing "highlighting", "underscoring", "signaling", "reflecting" clause that restates the sentence it hangs off. humanizer 1, 3. Cut the clause; the fact stands alone.

**Avoiding is and are.** "Serves as", "stands as", "represents", "marks", "boasts", "features", "offers". humanizer 8. Write is, are, has.

**Vague sources and vague declaratives.** "Observers", "industry reports", "experts", "one widely cited read", "the implications are significant", "the stakes are high", "the reasons are structural". humanizer 5, stop-slop. Name the source or cut the sentence; name the implication or cut the sentence.

**Passive voice and missing subjects.** "Was created", "is believed", "it is expected". humanizer 13. Find the actor.

**Qualifier pile-up.** Two hedges on one claim ("could potentially", "in some cases may"). humanizer 24. Keep the one the source needs. A qualifier that is part of the fact ("up to", "including contingent", "annualized") is not a hedge and stays.

**Forced fragments and quotables.** A row of one-line fragments for drama, a line that could stand alone as a quote card anywhere in the body, a formulaic saying ("X is the language of Y", "X becomes a trap"). humanizer 31, 32; stop-slop. One short sentence for emphasis is fine. Rewrite the rest as sentences.

**Fake-candid openers and throat-clearing.** "Here is the thing", "honestly", "let me be clear", "the uncomfortable truth", "it turns out", "worth noting". humanizer 33, stop-slop. Delete and start at the point. The seat-flex opener ("X is the part of Y I get paid to worry about") is banned outright per `my-writing-style` (the plain-language rule).

**Generic positive endings and enthusiasm markers.** "Exciting times", "the future looks bright", "excited to see", "kudos", "shoutout", "big if true", "huge". humanizer 25 and the 16-08 list. End on the last useful fact, the change-my-mind condition, or a specific credit.

**Overused words.** `house-style`'s canonical list binds here unchanged. Post-lane additions from humanizer's high-frequency set: actually (when stacked), align with, key (as an adjective), quietly.

**Mechanics.** No em or en dashes on any account, and no hyphen used as a separator; hyphens appear only inside compound words and identifiers. Straight quotes. Use emoji only when the current author's channel preferences permit it.

## Step 2b. Two counted checks (added 10-09-2026; these are gates, not feel)

1. **Final line.** Take the last sentence of the post. It contains no second-person imperative verb addressed to the reader (tell, show, make, prove, name, convince, explain, try, go, change) and no "If you ..., <imperative>" construction. On replies it also contains no question mark. On standalone posts and quote-tweets a question mark is allowed at most once in any seven posts (the 16-08 cap), counted across the slate. A hit is a gate failure: rewrite before scoring.
2. **Openers across the slate.** When more than one root post is in hand for the same week, list the first three words of each side by side. No two consecutive posts share them or share a labelled scaffold ("My read:", "Hot take:", "Unpopular opinion:"); a labelled scaffold appears at most once per slate. Plain first-person claims ("I think", "I don't think") may recur but not in the same form on consecutive days. A hit is a gate failure on the later post.

Report both checks as PASS or the exact hit, with the line quoted.

## Step 2c. The repetition gate (added 14-09-2026; a script, not a feel check)

If the Socials project is reachable on this surface, run `claude/repetition-gate.py` from it: project_read it, save it locally, put every post of the slate in one JSON object keyed by day (a post from earlier in the same week that is already live goes in too, so the slate checks see it), and run `python3 repetition-gate.py drafts.json`. It is standard-library Python. Per post it prints every content phrase of two or more words used twice (quoted source words, proper nouns and handles, and one callback of line 1 in the close are exempt), any derived-figure label used more than once ("my arithmetic", "my own tally", "by my count"), the imperative-closer check, and the post's objection sentence and final line. Across the slate it prints every 4-gram shared between two posts and the opener, objection-frame and closer-frame forms side by side, and fails any form that recurs on consecutive posts or appears on more than two.

The rules it encodes (the repetition rules): no phrase twice in one post; a derived-figure label at most once per post, operands preferred ("62%, 412 over 668"); no sentence frame on consecutive posts or on more than two posts in a week, which covers the objection frame ("The strongest case against me is"), the hold line ("I still hold my view") and the close ("What would change my mind:" at most twice a week, never in the same form on consecutive days). Bring the objection in differently each day: name the person and let their line stand, "X argues the opposite", "X sees it differently", a plain concession and the reason it does not move the claim.

A FAIL line is a rewrite of that paragraph around its point, never a synonym swap, and the gate is rerun until its last line reads GATE: PASS. Paste the gate output under the draft. A draft shown without a GATE: PASS line has not been through this pass. If the script cannot be fetched, run the same counts by hand and say so in one line; the checks do not lapse because the tool did.

## Step 3. Score

Rate the draft 1 to 10 on each dimension. Below 35 of 50, rewrite. At or above 35 with any Step 0, Step 2b or Step 2c failure, still rewrite.

| Dimension | Question |
|---|---|
| Stance | Could a reader say what the owner believes after reading it, and could a peer dispute it? |
| Directness | Statements, or announcements of statements? |
| Rhythm | Uneven like speech, or metronomic? |
| Seat | Is the owner in the room, or floating above it? |
| Density | Is there a word that can go without changing the meaning? |

Report the five numbers with the draft. The score is the gate; a feel is not. The score alone is still not enough: Step 2c is the check the score cannot make.

## Step 4. Rewrite

Rewrite the paragraph around its main point, not phrase by phrase. Patching one flagged phrase at a time produces a second layer of tells. Read the result aloud. Then ask two questions and treat a yes to either as a failure: what still sounds machine-made, and did the rewrite add or lose any fact, number, date, name, quote, qualifier or attribution. Cap at two rewrite rounds; on the third, return the best version with the remaining hits listed and let the owner edit.

## Step 5. What not to flag

The false-positive list matters because the pass also runs on posts the owner typed himself, and those must come back untouched.

* One "not X, it is Y" per post. His signature move.
* "Just", "actually", "really" in his own copy. stop-slop bans every adverb; that ban is rejected here. Cut adverbs only when stacked or doing hedge work.
* Questions in the body. Curiosity mid-post pulls the reader down. stop-slop's ban on Wh- openers is rejected.
* An exclamation when he means it ("Massive cards week!").
* Singlish particles leh, liao, sia, bro, haha. Not "la".
* One short sentence for emphasis.
* Repeated openings used on purpose for rhythm inside one post, and one callback of line 1 in the close. (Across consecutive posts they are a Step 2b hit; a third use inside one post is a Step 2c hit.)
* Asides, self-corrections, mixed feelings, an odd specific detail. These are the human details humanizer says to keep; they carry the voice.
* Real alternatives a reader would actually weigh, and a named objection answered in full.
* The first-person change-my-mind close ("What would change my mind: <dated condition>"), once in a slate. It is a statement about the owner's view, not an instruction to the reader.
* Bold, title case, mini-heading lists, curly quotes and heading rules from humanizer 15 to 19 and 29 to 30. No surface on X; ignore them here.

## Output

Return, in this order: the Step 0 stance sentence or NO STANCE; the two Step 2b results (final line, slate openers); the Step 2c gate output verbatim, ending in GATE: PASS; the five scores; the rewrite; a one-line list of what changed by pattern group; any line left flagged because fixing it would touch a fact. Under 120 words of commentary. The posting skill owns presentation to the owner and the go-ahead gate.

## Boundaries

The claim ledger owns every number and attribution; this skill never adds or removes one. Confidentiality lives in the posting skills. Use the currently configured channel register. Standing signatures or calendar conventions apply only when the author supplied them. house-style and reasoning-core apply as always. These general warmth guidelines are not counted gates: no snark, no dunking, credit by name.

## License and attribution

This adapted file is distributed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), with the exact scope in [../LICENSE.txt](../LICENSE.txt). Creator/source attribution, unchanged MIT notices and the modification record are retained in [../NOTICE.md](../NOTICE.md). This attribution section was added on 11-10-2026; the post-review procedure was unchanged.
