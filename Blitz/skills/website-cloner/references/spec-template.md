# Component Spec Template

One file per component at `docs/research/components/<component-name>.spec.md`. This is the contract between extraction and the builder. The builder gets these contents inline in its prompt and should never need to open another document.

Fill every heading. "N/A" is allowed but earn it.

```markdown
# <ComponentName> Specification

## Overview
- **Target file:** `src/components/<ComponentName>.tsx`
- **Screenshot:** `docs/design-references/<name>.png`
- **Interaction model:** static | click-driven | scroll-driven | time-driven | hover-driven
- **Imports:** `cn()` from `@/lib/utils`, `<IconName>` from `@/components/icons`, shadcn `<Button>`

## DOM structure
<The element hierarchy. What contains what, in order. Note which children are
absolutely positioned overlays rather than flow content.>

## Computed styles
Exact values from getComputedStyle. No estimates, no "looks like text-lg".

### Container
- display:
- padding:
- maxWidth:
- backgroundColor:

### <Child 1>
- fontSize:
- fontWeight:
- lineHeight:
- letterSpacing:
- color:

### <Child N>
...

## States and behaviors

### <Behavior name>
- **Trigger:** <scroll position 50px | IntersectionObserver rootMargin "-30% 0px" | click .tab-btn | hover>
- **State A:** maxWidth: 100vw, boxShadow: none, borderRadius: 0
- **State B:** maxWidth: 1200px, boxShadow: 0 4px 20px rgba(0,0,0,0.1), borderRadius: 16px
- **Transition:** all 0.3s cubic-bezier(0.4, 0, 0.2, 1)
- **Implementation:** <CSS transition + scroll listener | IntersectionObserver | animation-timeline | Framer Motion>

### Hover states
- **<Element>:** <property>: <before> → <after>, transition <value>

## Per-state content
Only for stateful components. One block per state.

### State: "<Tab label>"
- Title: "..."
- Cards: [{ title, description, image, href }, ...]

## Assets
- Background: `public/images/<file>.webp` (1440×720)
- Overlay: `public/images/<file>.png`, absolutely positioned, top: 40px, right: 0, z-index 2
- Icons: `<ArrowRightIcon>`, `<SearchIcon>`

## Text content
Verbatim from the live site. Copy, do not paraphrase.

## Responsive behavior
- **Desktop 1440px:** <layout>
- **Tablet 768px:** <what changes>
- **Mobile 390px:** <what changes>
- **Breakpoint:** switches at ~<N>px

## Builder notes
- Verify `npx tsc --noEmit` before finishing
- Props interface goes in `src/types/`
- Do not invent content or values not listed above; if something is missing, say so rather than guessing
```

## Sizing rule

If a filled spec runs past ~150 lines, the section is too big for one builder. Split it: one spec per sub-component, plus one for the wrapper that composes them. Build sub-components first.
