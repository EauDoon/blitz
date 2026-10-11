# Minimum Viable Company kit

Listen, collect, sprint.  
Reduce cycle time.

## Choose a method for the work

Start with the result you need: a customer test, cash model, document, screen, or checked decision. Use the relevant methods below. Small edits can stay small.

The kit contains 25 skill packages. Each entry links to its actual `SKILL.md`; read that file and its required references before applying it. The examples below are synthetic requests, not customer evidence, completed work, or routing test results. Expected outputs describe the method's intended result when the necessary inputs and tools are available.

Company work follows [Frame, Test, Deliver and Operate](../profiles/company.md). Frame needs a bounded offer, customer and payer, accountable owner, permitted test, and cash/time cap. Test needs observed customer behavior against criteria set before the test. Deliver needs actual delivery and acceptance evidence, with support and failure responsibilities. Operate needs reconciled exchange and obligations, cash and capacity evidence, and an owned next-cycle procedure. Commercial collection needs verified payment. A plan, prototype, package check, or single successful cycle cannot establish repeatability.

## Set up selection on your host

Packaged Markdown supplies guidance. For native skill selection, the host must first discover or register the package through its supported installation route. Where the host supports implicit selection, frontmatter descriptions and invocation metadata can help it choose a method from an ordinary request. Selection still depends on the host, configuration, available listing, and request. No package guarantees reliable automatic selection everywhere.

The [kit manifest](../manifest.json) inventories the packages and records evidence states. It does not install or register skills. All 25 source packages include `agents/openai.yaml` with `allow_implicit_invocation: true`; this permits implicit invocation on supporting hosts, but proves no native load or routing success.

| Route | How to use the package | What to verify |
|---|---|---|
| Codex or another OpenAI host with native skills | Follow the [OpenAI setup guide](chatgpt.md) and [capability adapter](host-adapters/openai.md). Inspect the current listing, preserve existing adaptations, and use the target's supported install/register route when authorized. | The actual listed name, saved version, readable dependencies, native load, and fresh positive and negative routing cases. Metadata alone establishes none of these. |
| ChatGPT project using readable sources | Use the [project instruction template](../templates/project-instructions-chatgpt.md) within the named project. Instructions can select readable method sources without installing global skills. | Applied instructions, full saved readback, source access, needed tools, and observed method use. A source read is separate from a native load. |
| Claude | Follow [Claude setup](claude.md). Project instructions support source-based use; optional native installation has its own authorized preparation, comparison, save, and verification steps. | Current Claude capabilities and actual host results. Historical listing sizes and installed counts are not current observations. |
| Thor | Follow [Thor setup](thor.md), its exact project instructions, and the generated `Thor_Blitz_v2.1OAI_Method_Index.md`. Read selected source sections and dependencies. Use the verified [task-local runtime](runtime.md) only when the work needs packaged resources. | Instruction readback, selected resource bytes, actual execution and saved state. Generating or opening the runtime installs nothing globally. |

The project router activates only for explicitly selected Blitz work, governing project instructions, or the scoped item record. Within that scope, ordinary language can select creation, continuation, review, planning, or export. Review stays review; planning stays planning. An unrelated request does not authorize project access or build actions.

For registered skills, [OpenAI documents](https://learn.chatgpt.com/docs/build-skills) `@` selection in ChatGPT and `/skills` or `$` mentions in Codex CLI and the IDE extension. [Claude Code documents](https://code.claude.com/docs/en/skills) `/skill-name` for user-invocable skills, including a plugin namespace when applicable. These routes were checked on 11-10-2026 UTC. Use the name actually listed on your surface; this kit includes no Codex native installer.

For an explicit fallback, name the method shown by the host. If it is not registered, ask the assistant to read the linked `SKILL.md` and its required resources for the task. For example: "Read `Blitz/skills/meeting-to-action/SKILL.md` and extract the commitments from these synthetic notes." A path must be accessible on that host. Naming an unavailable skill does not install it.

### Names after OpenAI reference staging

[The staging helper](chatgpt_stage.py) prepares reference candidates, with these mappings from [name-map.json](name-map.json):

| Source identity | Staging behavior |
|---|---|
| `calc-workbook` | Candidate name becomes `calculation-workbook`. |
| `frontend-taste` | Candidate name becomes `web-design-taste`. |
| `google-slides` | Skipped as a native-tool role; actual presentation capability still needs checking. The source method remains in the kit and Thor index. |
| Other 22 identities | Candidate names remain unchanged. This says nothing about current installation. |

The helper rewrites relevant Markdown names, adds the OpenAI adapter, and validates transformed copies. It prepares 24 candidates from 25 source packages. A dry-run writes nothing; a stage writes only a new reference directory. The historical map's `same`, `renamed`, and `unknown` labels require current role comparison before any installation. Preserve an existing host adaptation's tools and save route.

Package validation, source-based execution, native loading, automatic routing, installation, and adoption are separate claims. This guide supplies no native installation receipt or routing benchmark.

<a id="all-25-packaged-skills"></a>

## Coordinate work and check evidence

### [blitz](../skills/blitz/SKILL.md)

Selects methods and recovers the right item, activity, and governing revision within an identified project.

- **Example:** "Continue the synthetic repair-service offer from its saved customer test and prepare the next permitted experiment."
- **Expected output:** The requested result using the relevant methods, with evidence gaps and necessary continuation state. A stage card is reserved for a stage-routing request.
- **Prerequisites:** Authorized project scope and accessible current sources. Native router installation is optional for the project-instruction route.

### [meeting-to-action](../skills/meeting-to-action/SKILL.md)

Extracts commitments, decisions, and unresolved questions from one meeting's notes or transcript.

- **Example:** "Extract who owes what from this synthetic supplier call, preserving each quoted commitment and stated date."
- **Expected output:** For a full extraction, five blocks covering the owner's commitments, others' commitments, decisions, open questions, and discussion without a decision. Inferences stay labeled.
- **Prerequisites:** Actual notes or transcript. Calendar, email, and transcript connectors are optional; a title alone cannot establish a commitment. A follow-up draft is separate from sending it.

### [research-protocol](../skills/research-protocol/SKILL.md)

Scopes research, grades sources, tests competing claims, and writes a cited answer with explicit uncertainty.

- **Example:** "Check the claims in this synthetic vendor comparison against the supplied documentation; identify unsupported claims and conflicting definitions."
- **Expected output:** An answer tied to sources, verification status, contradictions, and the evidence needed to close remaining gaps.
- **Prerequisites:** Readable primary sources and authorized retrieval tools when fresh external evidence is needed. Optional data services do not replace source provenance.

### [reasoning-core](../skills/reasoning-core/SKILL.md)

Checks analytical conclusions, rankings, forecasts, and valuations against evidence, assumptions, and independent calculations.

- **Example:** "Rank three synthetic fulfillment options using this cost and capacity table; show which assumptions would change the ranking."
- **Expected output:** A supported conclusion, criteria, uncertainty, cross-checks, and the condition most likely to change the view. Rankings do not need invented probabilities.
- **Prerequisites:** Relevant evidence and a computation tool for material arithmetic. Independent events must not be normalized into a probability distribution.

### [gauntlet-verify](../skills/gauntlet-verify/SKILL.md)

Checks work in progress through either comparison with a named reference or isolated verification of consequential research claims.

- **Example:** "Verify the load-bearing claims in this unfinished synthetic pricing memo, using its supplied source pack and a bounded review budget."
- **Expected output:** Quoted or source-backed findings, fixes or corrected claim labels, and the review trajectory with remaining gaps.
- **Prerequisites:** Inspectable evidence or reference artifact and independent review contexts for an independence claim. Optional orchestration and logging use available authorized routes.

### [cold-read](../skills/cold-read/SKILL.md)

Checks a finished outgoing artifact against a stated rubric with readers who did not see it being built.

- **Example:** "Check this finished synthetic customer proposal before delivery against the brief, sources, and acceptance criteria."
- **Expected output:** A review verdict, exact findings and changes, unresolved decisions, and checks that could not run. Numeric criteria require executed independent recomputation.
- **Prerequisites:** The artifact, rubric, evidence, and an isolated reviewer context. External factual claims need source access. Self-review does not establish independence.

## Write and edit

### [write-with-pyramid](../skills/write-with-pyramid/SKILL.md)

Puts the recommendation or ask first, groups its reasons, and attaches proof for the intended reader.

- **Example:** "Restructure this synthetic equipment-purchase memo around approval of Option B by 20-10-2026, using only the attached evidence."
- **Expected output:** An argument skeleton followed by concise prose, with one ask, one date, and visible unsupported points.
- **Prerequisites:** A real stated ask, audience, and supporting material. No special connector is required.

### [house-style](../skills/house-style/SKILL.md)

Applies mechanics for text the author sends, signs, or publishes: answer first, clear names, numbers, dates, and file naming.

- **Example:** "Apply the kit's formatting rules to this synthetic service proposal without changing its terms or figures."
- **Expected output:** Edited prose with consistent mechanics, attribution, and supported numerical claims.
- **Prerequisites:** The source text and its evidence. The current conversation's instructions govern ordinary chat replies.

### [my-writing-style](../skills/my-writing-style/SKILL.md)

Adapts prose to the current author's supplied voice samples and preferences.

- **Example:** "Use these two synthetic voice samples to draft a reply declining the proposed delivery date and offering 23-10-2026."
- **Expected output:** A concise draft in the supplied register. Without samples, a neutral business draft identified as such.
- **Prerequisites:** Supplied preferences or samples when voice matching is wanted. The package contains no personal writing corpus or authority to infer a biography.

### [anti-slop](../skills/anti-slop/SKILL.md)

Finds and removes repetitive, inflated, or formulaic prose while preserving facts and the author's voice.

- **Example:** "De-slop this synthetic landing-page copy; keep every price, claim, and qualification unchanged."
- **Expected output:** A restrained rewrite and explanation of changes, or flagged patterns only in detect mode. Clean text can remain unchanged.
- **Prerequisites:** Source text and applicable writing rules. Social posts use the packaged post-pass reference and any available channel rules; no publishing action follows.

### [doc-style](../skills/doc-style/SKILL.md)

Builds business documents with a clear opening conclusion, consistent themes, and checks on the final artifact.

- **Example:** "Turn this synthetic operating review into a two-page Word memo with the recommendation first and the cash table intact."
- **Expected output:** The commissioned document, with source-supported content and applicable structural, arithmetic, and rendered-page checks.
- **Prerequisites:** A supported document builder and renderer for Word output; an authorized native save/conversion route for Google Docs. Preserve the host-adapted route and verify the converted artifact.

### [legal-contract](../skills/legal-contract/SKILL.md)

Reviews or amends an existing agreement while preserving its wording conventions, layout, and version history.

- **Example:** "Apply the two agreed changes in this synthetic equipment-hire ledger to the supplied original DOCX, preserving its format."
- **Expected output:** For an amendment, a clean DOCX, tracked version, checked signing PDF, and delivery stamp linking changes to the ledger. A review returns ranked issues and replacement wording.
- **Prerequisites:** Original document bytes, agreement evidence, bundled amendment scripts, validation and rendering tools, and suitable fonts. Jurisdiction questions need current scoped evidence; missing original bytes prevent a faithful edit.

## Model numbers

### [calc-workbook](../skills/calc-workbook/SKILL.md)

Builds money spreadsheets with live formulas, explicit assumptions, and stable references to the governing document.

- **Example:** "Build a synthetic monthly service-fee workbook from this schedule, including a capped fee and an independent numeric check."
- **Expected output:** A canonical XLSX with a Read Me tab, labeled inputs, formulas, and evidence from recalculation, reference checks, and numeric tests.
- **Prerequisites:** The governing schedule, packaged calculation module, `openpyxl`, and a supported spreadsheet recalculation/render route. A Google Sheet copy needs its own authorized route and readback; paid-against work also needs the required blind check.

### [metric-pull](../skills/metric-pull/SKILL.md)

Acquires and reconciles protocol or on-chain metrics across independent sources, preserving definitions, scope, and timestamps.

- **Example:** "Reconcile the two supplied synthetic chain-supply snapshots at the same block and explain any mismatch without averaging it away."
- **Expected output:** A dated figure or long-format series with source, definition, chain scope, comparison delta, and verification status. Missing observations remain null.
- **Prerequisites:** Suitable independent sources; current API, RPC, explorer, or dataset access for a live pull. A proxy and its upstream provider count as one source.

## Build presentations and visuals

### [pitch-architect](../skills/pitch-architect/SKILL.md)

Structures a persuasive pitch, proposal, or approval memo around the audience's decision, evidence, risks, and one exact ask.

- **Example:** "Outline a synthetic approval pitch for a capped service pilot, using these costs and test criteria, with a decision by 20-10-2026."
- **Expected output:** Conclusion-led titles or memo structure, supported numbers, a risk ledger, and an exact ask with next steps.
- **Prerequisites:** Audience, decision, evidence, and constraints. A document or presentation builder is needed only for the final requested format.

### [google-slides](../skills/google-slides/SKILL.md)

Builds new presentation decks, owning the canvas, visual system, rendering checks, and delivery format.

- **Example:** "Build a six-slide PowerPoint from this synthetic pilot outline and source table for an internal reading deck."
- **Expected output:** A checked PPTX or verified Google Slides delivery, with conclusion-led titles, source detail, and explicit unresolved figures.
- **Prerequisites:** Supported presentation tools, fonts, and slide rendering. Google delivery needs an authorized working conversion/save route; otherwise the method provides a PPTX and names the remaining import step.

### [slide-design](../skills/slide-design/SKILL.md)

Reviews existing slides or amends a named subset, focusing on sequence, layout, audience fit, and rehearsal.

- **Example:** "Review this synthetic eight-slide deck for a ten-minute talk and give exact fixes for slides 3 and 4."
- **Expected output:** Findings by slide with concrete edits, plus speaker notes or rehearsal prompts when requested.
- **Prerequisites:** Visible slides through a browser or rendered file. Text-only access supports a sequence review, not a visual review. Editing needs a supported route and authority for the target deck.

### [diagram-design](../skills/diagram-design/SKILL.md)

Draws structural relationships such as architecture, process, sequence, and ownership in HTML with inline SVG.

- **Example:** "Diagram the synthetic repair-service handoff from booking through inspection, repair, acceptance, and refund handling."
- **Expected output:** A self-contained HTML figure with an appropriate layout, checked connectors, and a rendered visual review. Image exports are produced when requested.
- **Prerequisites:** The selected type reference, bundled Python lint/skin tools, and a browser renderer. Exact offline fonts need embedding; declared fallback fonts remain usable.

### [viz-dashboards](../skills/viz-dashboards/SKILL.md)

Builds charts and dashboards from supplied or separately verified numbers, with consistent units and self-contained rendering.

- **Example:** "Chart the synthetic pilot's weekly orders, cash receipts, and delivery hours from this CSV; keep assumptions visible."
- **Expected output:** A checked chart or HTML dashboard whose titles, tables, and plots agree, with working interactions and source/date labels.
- **Prerequisites:** Usable data, computation and chart libraries or precomputed inline SVG, and a renderer. Inline script dependencies where the viewer blocks external loads.

## Build websites and reusable methods

### [frontend-mockup](../skills/frontend-mockup/SKILL.md)

Creates concept screens for an unbuilt product, using computed synthetic data and explicit mockup labels.

- **Example:** "Mock up a fictional repair-booking dashboard with twelve sample jobs and a clearly marked cancellation state."
- **Expected output:** Self-contained HTML and rendered PNG screens or detail crops, labeled as concept mockups with sample data.
- **Prerequisites:** A browser renderer, typically Node and Playwright, for PNGs. Without rendering, deliver the usable HTML and state that PNG verification did not run.

### [frontend-taste](../skills/frontend-taste/SKILL.md)

Chooses and checks the visual foundation of a web surface against its audience, brief, accessibility needs, and interaction states.

- **Example:** "Review this fictional booking site's desktop and mobile pages for hierarchy, readable controls, and a clear primary action."
- **Expected output:** A design direction or targeted findings, with runtime screenshots, relevant checks, and remaining choices. This method gates a build or redesign.
- **Prerequisites:** The actual page or design, browser access, and applicable frontend dependencies. Detector availability and current host behavior must be observed.

### [frontend-scroll-craft](../skills/frontend-scroll-craft/SKILL.md)

Builds new websites whose sections and motion tell a story as the reader scrolls.

- **Example:** "Build a scroll-based site for a fictional tool-restoration studio using these supplied photos; show the process and one booking action."
- **Expected output:** A brief, page plan, assets, HTML build, and screenshots across scroll positions, mobile widths, and reduced-motion behavior.
- **Prerequisites:** Bundled engine and scripts, Node, browser automation, and media/codec tools when used. Supplied assets are a supported route. Optional asset generation needs its own cost and upload authority.

### [website-cloner](../skills/website-cloner/SKILL.md)

Rebuilds an existing site from observed styles, assets, text, and interactions, with comparison against the source.

- **Example:** "Rebuild the supplied local site for a fictional community workshop in Next.js, matching its responsive layout and tab behavior."
- **Expected output:** A working codebase, extracted specifications and assets, build results, and desktop/mobile comparison findings.
- **Prerequisites:** A working browser inspection route, a reachable reference, and the target's frontend toolchain. Use permitted assets and scope; cloning does not authorize deployment or impersonation.

### [meta-skill](../skills/meta-skill/SKILL.md)

Creates or improves reusable methods, checking whether the need deserves a skill and how its trigger differs from neighboring roles.

- **Example:** "Turn this repeated synthetic equipment-inspection workflow into a candidate skill with clear triggers, boundaries, and two acceptance cases."
- **Expected output:** A candidate method with required resources, evaluation cases, actual evaluation evidence or named gaps, and package handoff.
- **Prerequisites:** The target host's observed package and evaluation routes. Independent review needs an isolated context. Paid evaluations and installation require their own authority; neither is implied by authoring.

### [skill-package-check](../skills/skill-package-check/SKILL.md)

Checks skill packaging: frontmatter, names, description limits, referenced files, and archive structure.

- **Example:** "Check this synthetic inspection-skill folder before handoff and report malformed metadata or missing required files."
- **Expected output:** Executed package-check results, actionable warnings, and any untested host-listing budget. A lint pass does not establish routing quality or correct behavior.
- **Prerequisites:** Python and the bundled checker. The suite-budget check needs a suitable current host inventory; its historical Claude assumptions cannot verify a different host.

## Keep the required resources with the method

The [source inventory](../skills/README.md) and generated Thor index preserve all 25 identities. Supporting references, scripts, assets, and notices travel with selected methods. External renderers, libraries, browsers, connectors, credentials, native agents, and other named skills are not supplied merely because a method mentions them. Check the [capability contract](host-adapters/openai.md) and current tools before dependent work.

Use the smallest sufficient method set and retain the original acceptance gates. A missing dependency needs a verified fallback or a precise limit on the affected output. Consult [provenance and notices](../skills/provenance.md) before redistributing method packages.
