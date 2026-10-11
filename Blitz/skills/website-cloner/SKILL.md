---
name: "website-cloner"
description: 'Rebuilds a live site as a Next.js, Tailwind and shadcn/ui codebase with visual QA. Use on clone, replicate or copy a site, pixel-perfect copy, his own version of a URL with the same look. Redesigns: frontend-taste.'
---

# Website Cloner

Rebuild a live site as a clean Next.js codebase by extracting what it actually is (exact computed CSS, downloaded assets, verbatim text, and observed behavior) instead of eyeballing a screenshot.

The method is not "inspect everything, then build everything." You are a foreman walking the job site: inspect one section, write its spec to a file, hand that file to a builder agent, then move to the next section while the builder works. Extraction and construction overlap.

## Boundary

Legitimate uses: rebuilds, migrations, design reference, prototypes, competitive teardowns, learning a technique. A faithful copy stays faithful: `frontend-taste`'s type and layout defaults do not apply here. When he wants the copy to look better than the original, that is a redesign and goes to `frontend-taste`.

Stop and ask what the clone is for before starting if the target is a login page, a bank, an exchange, a wallet, or a checkout flow. Do not build a lookalike that collects credentials or payments, do not deploy a clone under a name or domain that reads as the original, and do not ship someone's design as original work in a commercial deliverable. Cloning a page is not the problem; passing it off is.

## Preflight

1. **Browser tools.** This skill cannot run without them. Default to the built-in Browser pane, whose tools are named `mcp__Claude_Browser__*` in the desktop app and `mcp__remote-devices__Claude_Browser__*` when a cloud session is linked to his computer; read the `built-in-browser` skill before the first browser step. Use `mcp__claude-in-chrome__*` (with the `chrome-browser` skill) only when the target sits behind the owner's existing logged-in session.

   | Need | Call |
   |---|---|
   | Open the target | `preview_start {url}` → returns a `tabId` |
   | Second tab (clone, for QA) | `tabs_create` then `navigate` |
   | Run an extraction script | `javascript_tool {action:"javascript_exec", text, tabId}` |
   | Screenshot | `computer {action:"screenshot", tabId}` |
   | Viewport width / dark mode | `resize_window {preset\|width,height, colorScheme, tabId}` |
   | Scroll, click, hover | `computer {action:"scroll"\|"left_click"\|"hover"}` |
   | Labeled DOM tree | `read_page` |
   | Serve the clone | `preview_start {name}` from `.claude/launch.json` |

2. **Target project.** Confirm a Next.js 16 + Tailwind v4 + shadcn/ui project exists and builds. If not, scaffold it first; see `references/setup.md`. `git init` is required if builders will run in worktrees.

3. **URLs.** Normalize and validate each. Open each one and confirm it loads before promising anything.

4. **Output folders.** Create `docs/research/`, `docs/research/components/`, `docs/design-references/`, `scripts/`. For more than one target, nest per hostname: `docs/research/<hostname>/`.

## Principles

These decide the outcome. Everything else is procedure.

**Extraction is exhaustive or it is worthless.** Every builder gets a screenshot, exact CSS values, local asset paths, and verbatim text. A builder that has to guess a color, a font size, or a padding value will guess wrong. Spend the extra minute.

**Small tasks, exact results.** "Build the features section" produces something approximately right and obviously wrong. One focused sub-component with exact values gets nailed every time. If a builder prompt passes about 150 lines of spec, split the section. Treat that as mechanical, not a judgment call.

**Real content, real assets.** Pull actual text via `textContent`, download every image and video, extract inline SVGs as React components. Generate content only where it is clearly server-generated per session.

**Layered assets are the common miss.** What looks like one image is often a background gradient plus a foreground mockup plus a positioned overlay icon. Enumerate every `<img>` and every non-`none` `background-image` inside a container, including absolutely positioned children.

**Foundation is sequential and non-negotiable.** Fonts, color tokens, types, and global assets land before any section is built. Everything after that can run in parallel.

**Extract behavior, not just appearance.** A site is not a screenshot. For every element capture what it looks like (`getComputedStyle`) and what it does: the trigger, the before and after states, and the transition.

**Identify the interaction model before writing any spec.** Building click-driven tabs when the original is scroll-driven is the single most expensive error in this pipeline; it costs a rewrite, not a CSS tweak. Scroll first and watch for things changing on their own. Only if nothing moves do you start clicking. Write the verdict into the spec explicitly: `INTERACTION MODEL: scroll-driven, IntersectionObserver rootMargin -30% 0px`.

**Every state, not the default state.** Click each tab and capture its content. Capture the header at scroll 0 and again past the trigger. The diff between two captures *is* the behavior spec.

**Spec files are the contract.** No builder is dispatched without `docs/research/components/<name>.spec.md` written first. The builder gets the contents inline; the file persists as the artifact you audit when something looks wrong.

**The build always compiles.** Builders verify `npx tsc --noEmit` before finishing. You verify `npm run build` after every merge.

## Phase 1: Reconnaissance

**Screenshots.** Full-page at 1440px and 390px into `docs/design-references/`. These are the master reference.

**Global extraction.** Run the global audit script from `references/extraction.md`. It returns fonts, favicons, images, videos, background images, and SVG counts in one pass. From it, settle:
- every font family, weight and style actually in use
- the color palette, mapped onto shadcn token names where they fit, with custom properties for the rest
- favicons, apple-touch-icons, OG images, webmanifest → `public/seo/`
- site-wide patterns: hidden scrollbars, scroll-snap containers, global keyframes, backdrop filters, and smooth-scroll libraries (check for `.lenis`, `.locomotive-scroll`, or a custom scroll wrapper; native scrolling feels different and the owner will notice immediately)

**Interaction sweep.** A dedicated pass, after screenshots, before anything else. Most of what matters here is invisible in a static capture.
- *Scroll:* move down slowly. Does the header change, and at what scroll position? Do elements animate in? Does a sidebar or tab indicator switch on its own? Any scroll-snap? Any non-native scroll feel?
- *Click:* every button, tab, pill, card and link. For tab groups, click each one and record the content per state.
- *Hover:* buttons, cards, links, nav items, images. Record the property that changes and the transition timing.
- *Responsive:* 1440, 768, 390. Note which sections reflow and roughly where the breakpoint sits.

Write it all to `docs/research/BEHAVIORS.md`. Every later spec references this file.

**Topology.** Map each section top to bottom with a working name, its interaction model, whether it is flow content or a fixed overlay, and its z-index relationships. Save as `docs/research/PAGE_TOPOLOGY.md`. This is the assembly blueprint.

## Phase 2: Foundation

Sequential, and you do it yourself rather than delegating, because it touches many files at once.

1. Fonts in `src/app/layout.tsx` via `next/font/google` or `next/font/local`
2. `src/app/globals.css`: color tokens, spacing, keyframes, utility classes, global scroll behavior
3. TypeScript interfaces in `src/types/` for the content shapes observed
4. Inline SVGs deduplicated into named components in `src/components/icons.tsx`, named by function (`SearchIcon`, `ArrowRightIcon`)
5. A `download-assets.mjs` script in the project's `scripts` folder: fetch every image and video to `public/`, four at a time, with error handling
6. Verify `npm run build`

## Phase 3: Extract, spec, dispatch

The core loop, run per section in topology order.

**Extract.** Screenshot the section in isolation. Run the per-component extraction script (`references/extraction.md`) against its container selector; do not hand-measure properties. For anything stateful, capture state A, trigger the change, capture state B, and record the diff. Pull verbatim text. List which downloaded assets and which icon components it needs. Count distinct sub-components.

**Spec.** Write `docs/research/components/<name>.spec.md` using the template in `references/spec-template.md`. Fill every section. "N/A" is allowed but earn it: even a footer usually has link hover states.

**Dispatch.** One builder for a simple section. For three or more distinct sub-components, one builder each plus one for the wrapper, sub-components first.

Each builder receives the full spec inline in its prompt, never a pointer to a file. It also gets the screenshot path, which shared components to import, its exact target file path, the breakpoint values, and the instruction to verify `npx tsc --noEmit`.

Isolation: builders that each own one new component file rarely collide, so plain parallel `Agent` calls are usually right. Use `isolation: "worktree"` when builders will touch shared files (`globals.css`, `icons.tsx`, `page.tsx`) or when running more than about four at once. Worktree agents must report their branch name so you can merge.

**Do not wait.** Dispatch, then start extracting the next section immediately.

**Merge.** As builders return, merge, then verify `npm run build`. Fix type errors on the spot rather than accumulating them.

## Phase 4: Assembly

Wire `src/app/page.tsx` from the topology doc: imports, layout structure, sticky positioning, z-index layering, real content into props, and page-level behavior (scroll snap, intersection observers, smooth scroll, theme transitions between sections). Verify `npm run build` is clean.

## Phase 5: Visual QA diff

The clone is not done when it builds. Serve it with `preview_start`, open the original in a second tab, and compare.

1. Section by section, top to bottom, at 1440px
2. Repeat at 390px
3. For each discrepancy, check the spec file first. Wrong spec means re-extract and update it. Right spec means fix the component.
4. Exercise every behavior: scroll the full page, click every tab and button, hover everything interactive, confirm the header transition and scroll feel

Report only after this pass.

## Pre-dispatch checklist

Every box, or go extract more.

- [ ] Spec file written, all sections filled
- [ ] Every CSS value came from `getComputedStyle()`, none estimated
- [ ] Interaction model identified and stated
- [ ] Stateful components: content and styles captured per state
- [ ] Scroll-driven: trigger threshold, both states, transition recorded
- [ ] Hover: before, after, and timing recorded
- [ ] Every image identified, overlays and layers included
- [ ] Responsive documented for desktop and mobile
- [ ] Text verbatim, not paraphrased
- [ ] Spec under about 150 lines, or the section gets split

## Completion report

Sections built, components created, spec files written (should equal components), assets downloaded, `npm run build` status, visual QA findings, and known gaps. Name the gaps rather than rounding up to "done".

## References

- `references/setup.md`: scaffolding the target project (bash, or PowerShell on Windows), launch.json, git init
- `references/extraction.md`: the browser scripts: global audit, per-component walk, state diff
- `references/spec-template.md`: the builder contract
- `references/pitfalls.md`: failure modes that cost rework

---

Method adapted from [ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) by JCodesMore (MIT). Reworked for this environment: scaffolding from zero, Claude Browser tool mapping, native `Agent` isolation, Windows paths where the rig is Windows. License and change notes: `NOTICE.md`.