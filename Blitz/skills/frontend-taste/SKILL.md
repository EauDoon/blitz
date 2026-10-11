---
name: "frontend-taste"
description: 'Design gate for web surfaces: landing pages, app UI, redesigns. Use on "make this look good", "make it premium", "feel like linear.app", "review this page". Scroll sites: frontend-scroll-craft; charts: viz-dashboards.'
---

# Frontend Taste

The gate a marketing or product web surface passes through before code is written: read the brief, pick the foundation, hold the locks, ban the defaults, then verify at runtime.

Sources: impeccable.style/slop (66 tells, 61 deterministic), tasteskill.dev v2 (Leonxlnx/taste-skill, MIT), 21st.dev community registry. History and the 04-09-2026 conflict log are in `CHANGES.md`.

## 0. Boundaries

Scope: landing and marketing pages, homepages, portfolios, product and app UI, components, mockups and redesigns. It does not fire on every HTML file or Artifact; generic pages take the built-in `artifact-design` skill.

| Surface | Owner |
|---|---|
| A new website or landing page built as a scroll experience: scrubbed video, layered hero, worldflight, cinematic or immersive site | `frontend-scroll-craft` builds it; this file runs the design read before its markup and the pre-flight after, and its canvas rule (section 3) still decides light or dark |
| A faithful clone or copy of an existing site | `website-cloner`; this file applies only when he wants the copy to look better than the original |
| Charts, series, distributions, dashboards, the hex 0f0f0f data standard, the eight point QA pass | `viz-dashboards` |
| Structural figures: architecture, flow, sequence, hierarchy | `diagram-design` |
| Decks: look and build; argument and the one exact ask | `google-slides`; `pitch-architect` |
| The cinematic dark aesthetic | `references/cinematic.md`, and only when the design read selects it |
| Every visible string on the page | `house-style` |
| Everything else about how a marketing or product surface looks and behaves | this file |

When a specialist and this file disagree on a visual default, this file wins on marketing, landing, portfolio and product surfaces. The specialist wins on its own surface.

**Out of scope, say so and route:** data tables (TanStack Table, AG Grid), code editors (Monaco, CodeMirror), native mobile (Apple HIG, Material directly), realtime collaboration UI. Apply only the marketing and about page parts of this file to those projects.

## 1. Design read, before any code

Read the brief first. Signals, in priority order:

* **Page kind.** Landing (SaaS, consumer, agency, event), portfolio, product UI, editorial, redesign.
* **Vibe words he used.** Minimalist, calm, Linear style, brutalist, premium consumer, editorial, dark tech, cinematic.
* **Reference signals.** URLs, screenshots, named products, competitors.
* **Audience.** The audience picks the aesthetic, not taste. A procurement panel and a design conscious consumer want opposite things.
* **Existing brand assets.** For a redesign these are starting material, not optional input.
* **Quiet constraints.** Regulated, public sector, accessibility first, trust first. These override aesthetic preference every time.

**Anti-default discipline.** The first aesthetic that surfaces is the trained average of every site in the corpus. Name it, then pick something else unless the read actually justifies it.

If the brief is genuinely ambiguous, ask **one** question. Never two, never a questionnaire, never a silent guess.

## 2. Motion and density follow the read

Calm, editorial, Linear style and trust first pages stay near static and airy, on a mostly symmetric grid. Premium consumer, landing and portfolio pages earn moderate motion and more asymmetry. Agency and experimental briefs can go further. Dashboards and terminal tools run denser. A redesign that preserves matches the existing density and motion; an overhaul pushes both up a step.

**Motion claimed is motion shown.** If the read calls for motion, the page actually moves. If working motion cannot ship in scope, ship a clean static page. Half built motion that jumps or cuts off is worse than none.

## 3. Canvas and theme, the scoping rule

Choose the appearance from the current brief and the accessibility requirements; no personal default overrides that choice.

| Surface | Canvas |
|---|---|
| Dashboard, chart, data story, quant or terminal style tool | hex `0f0f0f`, no design read needed. `viz-dashboards` owns it. |
| Slide deck | The deck theme. `google-slides` owns it. |
| Landing, marketing, portfolio, product UI, anything consumer facing | The design read picks. Ship light and dark tokens from the start. |

**Theme lock.** One theme per page. A dark page has no warm paper section in the middle of it. Section level tints inside the same family are fine (`zinc-950` beside `zinc-900`); flipping to `amber-50` mid page is broken. The single exception is a deliberate one time theme switch as a composition device, used once.

**Dark is not automatically premium.** Glowing box shadows on a dark canvas is a named tell. When dark is chosen for a marketing surface, build contrast from light and spacing, not from glow.

## 4. Foundation

Do not hand write CSS for something that has an official package. Do not import a system's tokens and then override ninety percent of them.

| Brief reads as | Reach for |
|---|---|
| Microsoft or enterprise SaaS | `@fluentui/react-components` |
| Google flavored product | `@material/web` |
| IBM style B2B analytics | `@carbon/react` |
| Atlassian style product | `@atlaskit/*` |
| GitHub style devtool or community | `@primer/css`, `@primer/react-brand` |
| UK or US public sector | `govuk-frontend`, `uswds` |
| Modern accessible React foundation | `@radix-ui/themes` |
| Modern SaaS where the components are owned | shadcn/ui, never in default state |
| Tailwind based indie or small team build | Tailwind v4 utilities plus `dark:` |

For an aesthetic rather than a system (glassmorphism, bento, brutalism, editorial, mesh gradient, kinetic type, the cinematic dark look), there is no official package. Build with native CSS plus Tailwind and label the borrowed inspiration honestly in a comment. There is no official `liquid-glass.css`; web versions are approximations.

**One system per project.** No Fluent beside Carbon. No shadcn inside Material.

**Verify the dependency exists before importing it.** Check `package.json`. Output the install command if it is missing.

## 5. Hard layout rules

Failing any of these is shipping broken work.

**Hero**

* Fits the initial viewport. Headline max 2 lines desktop. Subtext max 20 words and max 4 lines. CTA visible without scrolling.
* A 4 line hero headline is a font size error, not a copy length error. Default `text-4xl md:text-5xl lg:text-6xl`. Reach for `text-7xl` only at 3 to 5 words.
* Top padding max `pt-24` desktop. More reads as a layout bug.
* Max 4 text elements: eyebrow or brand strip (pick zero or one), headline, subtext, CTAs (1 primary plus at most 1 secondary). Banned inside the hero: tagline under the CTAs, trust micro strip, pricing teaser, feature bullets, avatar row. All of those become their own section below.
* The "used by" logo wall lives under the hero, never inside it.
* Needs a real visual. Text plus a gradient blob is a placeholder, not a hero.

**Navigation**

* One line at desktop. Two lines is broken. Condense labels, drop secondary items, or go to a hamburger.
* Height cap 80px, default 64 to 72px.

**Sections**

* **Eyebrow ration.** Max 1 eyebrow per 3 sections, hero counts as 1. The check is mechanical: count `uppercase tracking` micro labels above headlines; fail if the count exceeds `ceil(sections / 3)`. The alternative to an eyebrow is no eyebrow.
* **Split header ban.** Big left headline with a small explainer paragraph floating in the right column is banned as a default. Stack them, capped at 65ch.
* **Zigzag cap.** Max 2 consecutive image plus text split sections. The third is a fail.
* **Layout repetition ban.** A layout family appears at most once. Eight sections need at least four families.
* **Bento.** Exactly as many cells as there is content for. An empty cell means the grid was planned wrong. At least 2 to 3 cells carry real visual variation, not white on white text.
* **Long lists.** More than 5 items does not get a `<ul>` with `divide-y`. Use grouped columns, a card grid, tabs, scroll snap pills, or a carousel. A 10 row spec table with a hairline under every row is the laziest available layout.
* **Mobile collapse declared per section.** No assuming Tailwind handles it.
* `min-h-[100dvh]`, never `h-screen`. CSS Grid, never flexbox percentage math.

## 6. The three locks

* **Color lock.** One accent, chosen once, used on the whole page. Saturation under 80 percent by default. A warm grey site does not get a blue CTA in section 7.
* **Shape lock.** One corner radius system: all sharp, all soft (12 to 16px), or all pill for interactive. A documented mixed rule is allowed if it is followed everywhere.
* **Theme lock.** See section 3.

**Banned default palettes.** The AI purple to blue glow, and cyan on dark. For premium consumer briefs (cookware, wellness, artisan, luxury, heritage, DTC home goods) the beige plus brass plus oxblood plus espresso family is banned as the reach: backgrounds `#f5f1ea` `#f7f5f1` `#fbf8f1` `#efeae0` `#ece6db`, accents `#b08947` `#b6553a` `#9a2436` `#9c6e2a`, text `#1a1714` `#1a1814`. Rotate instead: cold luxury silver and chrome, forest green with bone and amber, black and tan, cobalt and cream, terracotta and slate, olive and brick, or monochrome with one saturated pop. Do not ship the same family twice in a row.

Override on any of the above only when the brand brief literally names the color.

## 7. Typography

* Display default `tracking-tighter leading-none`. Body `text-base leading-relaxed max-w-[65ch]`.
* **Inter, Geist and Space Grotesk are discouraged as the reflex default.** They are the three most common AI tells in the corpus. Acceptable when the brief asks for a neutral or Linear style feel, or the site is accessibility first. Otherwise reach for Outfit, Cabinet Grotesk, Satoshi, PP Neue Montreal, GT Walsheim, ABC Diatype.
* **Serif discipline.** Serif is very discouraged as a default. "It feels premium" is not a reason. Justified only when the brief names a serif, or the family is genuinely editorial, luxury, publication or heritage and the fit can be articulated. `Fraunces` and `Instrument Serif` are banned outright as defaults, both are LLM favorites.
* **Emphasis inside a headline uses italic or bold of the same family.** Injecting one serif word into a sans headline is amateur.
* **Italic descender clearance.** Any italic display word containing `y g j p q` needs `leading-[1.1]` minimum plus `pb-1` reserve, or the descender clips.
* Hierarchy ratio at least 1.25 between levels. Flat hierarchy is a tell.
* Floors: body text 14 to 16px, never under 12px. Functional text (links, labels, table cells) never under 11px. Line height at least 1.3. Letter spacing on body under 0.05em. No all caps body text.
* Contrast WCAG AA minimum: 4.5:1 body, 3:1 large text at 18px and above.

## 8. Motion

* **Motivated only.** Every animation answers one of: hierarchy, storytelling, feedback, state transition. "It looked cool" is not an answer. If the reason does not fit in one sentence, drop the animation.
* Animate `transform` and `opacity` only. Never `width`, `height`, `top`, `left`.
* Banned: `window.addEventListener("scroll")`, scroll progress from `window.scrollY` in React state, `requestAnimationFrame` loops touching React state. Use `useScroll`, ScrollTrigger, IntersectionObserver, or CSS `animation-timeline: view()`.
* Continuous values (mouse position, scroll progress, magnetic hover) use `useMotionValue` and `useTransform`, never `useState`.
* Spring physics, not linear easing. Bounce and elastic on interface elements reads dated.
* **Max one marquee per page.** Two is filler.
* `prefers-reduced-motion` is required whenever the page animates beyond hover and focus states. Infinite loops, parallax, scroll hijack and magnetic physics all collapse to static.
* Grain and noise filters live on a fixed `pointer-events-none` pseudo element, never on a scrolling container.
* Never mix GSAP or Three.js with Motion in the same component tree. `useEffect` animations get strict cleanup.

## 9. Assets and components

**Images.** Priority order: an image generation tool if one is available in the environment, then provided brand assets or real photography, then a clearly labeled placeholder slot plus a line telling the owner exactly which images the page needs. Inside an Artifact or any sandboxed file, every image is inline (a data URI) or an uploaded asset, because external image hosts do not load there. `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` is a development placeholder for a codebase served on the open web only, and never ships.

Even a minimalist page needs 2 to 3 real images. A pure text page is incomplete work, not restraint.

**Banned:** div based fake screenshots (fake dashboards, terminals, task lists built from styled divs, the single most recognizable tell), hand rolled decorative SVG illustrations and mascots, generic SVG shapes assembled as hero art, photos buried under an opacity wash, broken or empty `src`.

**Logos.** A trust wall uses real SVG marks from Simple Icons or devicon, not text wordmarks. Paste the mark inline as `<svg>` (from the `simple-icons` npm package or the site's SVG download); never hotlink `cdn.simpleicons.org`. Invented brands get an invented inline SVG monogram. Logos only, no category label printed underneath. Both modes must render.

**Icons.** Phosphor, HugeIcons, Radix or Tabler. Lucide only on explicit request or existing dependency. One family per project, one global `strokeWidth`. Never hand roll icon paths.

**Components and templates.** Before building a pattern from scratch, check 21st.dev (`21st.dev/community/templates`) for a hand built version of it: React and Next.js, mostly shadcn and Tailwind, free tier plus paid templates (read current pricing before quoting it). Use it as reference or as the base, then apply the locks in section 6 so it does not ship in default state. Never leave shadcn defaults untouched.

**Emoji.** Off by default in code, markup and visible text. Icon glyphs instead.

## 10. Interactive states

The static success state is not the whole component.

* Loading: skeletons shaped like the final layout, not a spinner.
* Empty: composed, and it says how to fill it.
* Error: inline for forms, contextual for transient.
* Active: `scale-[0.98]` or `-translate-y-[1px]` for physical feedback.
* **Button contrast check.** Every CTA label readable against its own background. White on white, transparent over a photo with no scrim, ghost buttons on imagery: all banned.
* **CTA wrap ban.** Button labels fit one line at desktop. 3 words max for a primary CTA, ideally 1 to 2.
* **No duplicate CTA intent.** "Get in touch" plus "Let's talk" plus "Start a project" on the same page is a fail. One label per intent, used in nav, hero and footer alike.
* **Form contrast check.** Inputs, placeholders, focus rings, helper and error text all pass AA against their section background. Label above input, error below, never placeholder as label.

## 11. Copy on the page

`house-style` owns the prose contract. These are the page specific additions.

* **Zero em dashes and zero en dashes anywhere visible.** Headlines, eyebrows, pills, buttons, body, quotes, attribution, captions, alt text. Ranges use "to", never a hyphen. This is the single most violated rule in the corpus and it is binary, not a budget.
* **Banned words.** `house-style`'s canonical list, plus these web marketing words: supercharge, unleash, next-gen, revolutionize, world class, enterprise grade.
* **Copy self audit before ship.** Re-read every visible string. Flag anything grammatically broken, with an unclear referent, or that reads as an LLM trying to sound thoughtful (forced metaphors, fake craftsman labels, mock poetic micro meta). Plain and functional beats cute and wrong.
* **No fake precise numbers.** `92%`, `4.1x`, `5.8mm` either come from real data, are labeled mock in a comment, or are cut. Do not fake engineering precision the brand does not claim.
* **No generic placeholder identities.** Not "John Doe", not "Acme", not "Nexus", not "SmartFlow". Realistic locale appropriate names and brand names.
* Testimonials max 3 lines. Attribution is name plus role, never a bare first name. Real typographic quote marks or none.
* One copy register per page.

## 12. The tells, banned outright

Forty-one named tells (surface and decoration, structure and labels, motion, production defects), merged from impeccable.style/slop and taste-skill section 9, are in `references/tells.md`. Read it before writing markup. None ship unless the brief explicitly asks for one.

## 13. Pre-flight

Before the code is shown, confirm the countable rules above hold: zero em and en dashes in any visible string, alt text included; eyebrows at or under `ceil(sections / 3)`; no three consecutive image plus text splits; at least four layout families across eight sections; bento cells equal to items; one marquee at most; no duplicate CTA intent; nav on one line at 80px or less; no scroll listeners; no hand rolled icon paths or div screenshots; every CTA and form control at AA; the three locks hold; reduced motion honored; empty, loading and error states exist; no tell from `references/tells.md`.

**Verification, run it, do not assert it**

```bash
python3 -c "t=open('page.html',encoding='utf-8').read();print([l for l in t.split(chr(10)) if chr(8212) in l or chr(8211) in l])"
grep -c 'uppercase tracking' page.html            # eyebrow count
grep -n 'addEventListener("scroll"' page.html      # must return nothing
grep -n 'src="http' page.html                      # external scripts and images, see the sandbox rule
node --check <(sed -n '/<script>/,/<\/script>/p' page.html)
```

Then open it. A dead script tag passes a syntax check and still ships a blank page.

**Sandbox rule, shared with `viz-dashboards`.** Artifacts and sandboxed viewers block CDN script loads and external images, and fail silently, which delivers a blank page or empty frames. Inline every library and image, or precompute coordinates and emit inline SVG. In a published Artifact, stylesheets may come from Google Fonts only. Verify with a grep for `<script src=` and `src="http`, do not assume.

## 13a. Runtime verification, then stop

The pre-flight above is the checklist; this is the run that proves it. Bounded, not a loop: build fully, inspect once in one batched round, fix everything it shows in one batch, confirm with at most one more round, stop. If the confirming round shows a regression your own fix introduced, that repair is the last edit; report anything else it surfaces as an open choice.

1. **Detector.** `npx -y impeccable@latest detect <file-or-folder>` (exit 0 clean, 2 findings, 1 scan failure; `--json` for a list). Target exit 0. A finding may stay only when the brief's own words earned it; list each kept finding with the line that earned it. It parses in jsdom and reads only physical padding: a coloured or bordered wrapper needs `padding` or the physical longhands on the wrapper itself, because `padding-inline`, `padding-block` and an inner container's calc width are invisible to it and raise `cramped-padding`. `detect <url>` cannot find Chrome in this sandbox and exits 0 with nothing scanned, so for a live site render it with Playwright, write `document.documentElement.outerHTML` to a file, and detect the file.
2. **Screenshots.** Chromium and Playwright are preinstalled in the cloud workspace. Capture 1440x900 and 390x844, first viewport then full page, open the PNGs with Read and look: first viewport holds, primary action visible, nothing overflows, hierarchy survives the squint, both palettes where dual mode applies. Never judge from one full-page thumbnail. The container shell may not reach Google Fonts (a published Artifact loads them fine), so a linked face can render in fallback here and the headline line count lies: `npm pack @fontsource/<face>`, build an `@font-face` block with the woff2 files as data URIs, inject it with `add_style_tag`, and confirm through `document.fonts` before reading the image.
3. **Report in four lines:** detector result (count kept and why), viewports inspected and what changed, tells removed, open choices for the owner (at most three).

**Review mode, for an existing page, URL or screenshot.** Render and detect per step 1, capture both viewports, then lead with the specificity verdict: authored for this product, or category interchangeable. Then 2 to 3 strengths, 3 to 5 issues with severity (P0 blocks a task, P1 fix before release, P2 has a workaround, P3 polish; tiebreak: would a user contact support about it, then at least P1), and 2 to 4 targeted questions. Score Nielsen's ten heuristics 0 to 4 each unless he asks for issues only (36 to 40 excellent, 28 to 35 good, 20 to 27 acceptable, 12 to 19 poor, under 12 critical; most real interfaces land at 20 to 32).

**Handoff.** `cold-read` before anything external facing ships. A published artifact that reads connector data or calls a model gets a security read for DOM XSS, egress and prompt injection before it goes out.

Optional tooling (impeccable, taste-skill) and its install commands: `references/tooling.md`.
