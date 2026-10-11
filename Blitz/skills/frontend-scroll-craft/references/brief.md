# The brief

Moved out of SKILL.md (upstream Steps 0 and 1) on 29-09-2026, text unchanged
apart from the headings. SKILL.md carries the short form; this file is the full
interview.

---

## A. The brief and creative authority

**Establish the brief before generating anything.** Reuse answers and assets
already provided. When the user explicitly delegates creative direction (for
example, "use your judgment" or "I want to get out of your way"), write a
`Self-authored under explicit creative delegation` brief and proceed. Cover the
eight topics below, distinguish evidence from assumptions, and do not invent
user quotations or force another interview/approval checkpoint.

Otherwise, interview for the missing decisions. Ask actual questions, record
the answers, and avoid inferring an entire brand from its name.

The skill is a range instrument, not a house style. The human brings intent and
whatever assets they own; the interview is where that turns into the right kind
of page: one unbroken world, distinct scenes, printed chapters, a live surface.
The skill can do any of them. The interview decides which.

Keep it short. Eight questions, asked in one pass:

1. **Vibe in three to five words**, plus up to three references from any medium.
   A film, an album cover, a shop, a magazine, a game. Not "sites you like":
   naming sites is how a page ends up looking like an existing site.
2. **The scroll journey, section by section, in their words.** What the visitor
   should hit first, what comes next, what the last thing is. Their sequence,
   not a menu you offered.
3. **The energy curve.** Where it should feel calm, where it should feel
   intense. A page that is loud the whole way is as flat as one that is quiet
   the whole way.
4. **How should someone feel while scrolling, stage by stage, and what is the
   ONE moment they should remember?** Energy is loudness. This is emotion, and
   the two do not line up: on a loud page the quiet act can be the most intense.
   The stage-by-stage answer becomes the feeling curve, the one moment becomes
   the peak. Both are required in BRIEF.md. See [feel.md](feel.md).
5. **One thing this site should do that no site they have seen does.** This is
   the seed of the signature move. Push for a real answer; "be memorable" is not
   one.
6. **How far from premium-minimal they want to go.** Offer the range in
   [uniqueness.md §5](uniqueness.md): brutalist, maximalist, playful,
   retro, dense, editorial, premium-minimal. Their answer governs the aesthetic
   family, not your taste.
7. **One unbroken world, or distinct scenes?** Should the whole page feel like
   one continuous place the scroll flies through (worldflight, see
   [worldflight.md](worldflight.md)), or like separate
   scenes, chapters, or cuts? This is the single biggest structural fork, and it
   is their call, not a device you pick later. Offer both plainly; neither is
   the default.
8. **What assets do they already have?** Footage, photos, product shots, a
   brand kit, clips of themselves. Real assets anchor the world and cut
   generation cost; the answer decides what gets graded and encoded versus
   generated. "Nothing" is a fine answer and means a fully generated world.

Write the answers into `<workspace>/builds/<name>/BRIEF.md` before any act planning, in
their words, not paraphrased into marketing prose. Everything downstream reads
from that file.

BRIEF.md must contain, at minimum:

- The eight topics, with verbatim user answers where supplied and clearly labeled authored decisions where delegated.
- **The feeling curve.** One line per act: the emotion, then what on screen
  causes it. Written before the acts exist, added to as the score fills in.
- **The peak.** The one moment, written as the sentence a visitor would say to
  a friend, plus which act it lives in.
- **The completed tell-someone sentence.** "It's the site where ___", filled
  with an experience, not a device name.
- Any authored silence, so the verification pass can tell it from dead scroll.

[feel.md](feel.md) is the spec for all four.

**If the human is genuinely unreachable** and the run is fully autonomous, write
BRIEF.md yourself: answer all eight questions in the brand's voice, mark the file
`Self-authored, not interviewed` at the top, and say so in the final report. A
self-authored brief without delegation is a fallback. Explicit delegation above
is a normal supported workflow and does not require the human to be unreachable.

---

## B. The journey

The subject is the user's to state. Ask it open, in plain prose, never as a
fabricated multiple-choice list of industries: a made-up menu biases them and
reads as you deciding their business for them.

Part A already covered vibe, sequence, energy and range. Do not ask any of it
again. Ask only what you cannot sensibly default:

1. **What is this, and who is it for?** One or two sentences in their words.
2. **What must the visitor believe by the end?** The single sentence the page
   exists to install. Not a feature list. If they give three, make them pick.
3. **What does the visitor do next?** One action. One label for it, used
   everywhere on the page.
4. **What do you already have?** Logo, palette, photography, product shots,
   footage, a brand doc. Real assets beat generated ones every time.
5. **Art direction**: offer the worlds in [worlds.md](worlds.md)
   as a real choice, and say they can go their own way.

Then write the **journey** before anything else: four to seven beats, each one a
shift in what the visitor knows or feels.

```
1  Recognition   they see their own morning
2  Tension       the cost of it, named plainly
3  Turn          the thing that changes
4  Substance     why it holds up
5  Range         what they can choose
6  Commitment    the one action
```

Beats are the spine. Sections serve beats; a section that serves no beat is cut,
however nice the shot is. Resolve the journey before generating assets. Show it
to the user when their decisions are needed; under explicit creative delegation,
record the chosen journey and proceed within the authorized scope.
