# Failure Modes

Each of these costs rework. Ordered roughly by how expensive they are.

## Wrong interaction model

Building click-driven tabs when the original switches on scroll, or the reverse. This is the most expensive error in the pipeline because it needs a rewrite, not a CSS fix.

Diagnose before writing the spec: scroll slowly through the section first and watch whether anything changes on its own. Only if nothing moves do you start clicking. A sticky sidebar with scrolling content panels is a fundamentally different component from a tab bar, even though both look like "tabs with content".

## Only capturing the default state

The page loads showing "Featured", and you clone that and stop. The other three tabs are empty. Or the header is captured at scroll 0 and the floating scrolled variant never gets built.

Click every tab, capture every panel. Snapshot scroll-dependent elements twice, above and below the threshold.

## Missing layered images

A section that reads as one image is often a background gradient, a foreground product mockup, and a positioned overlay icon. Miss the overlay and the clone looks empty even with the background correct.

Enumerate every `<img>` and every non-`none` `background-image` inside the container, including absolutely positioned children.

## Approximating CSS classes

"That looks like `text-lg`" is wrong when `text-lg` carries `line-height: 28px` and the real computed value is `24px`. Small everywhere, visibly wrong in aggregate.

Every value in a spec comes from `getComputedStyle()`.

## Building mockups of video

Elaborate HTML recreations of something that is a `<video>`, a Lottie file, or a canvas animation. Check the element type before building.

## Builder scope too large

If the builder prompt is getting long because the section is complicated, that is the signal to split it, not to keep writing. Past ~150 lines of spec, break it up. Do not bundle unrelated sections: a CTA and a footer are different components and one agent handed both will do neither well.

## Pointing builders at documents

"See `DESIGN_TOKENS.md` for the colors" produces guessed colors. The builder gets everything inline and should never need to open another file.

## Dispatching without a spec file

The spec is what forces exhaustive extraction, and it is the artifact you audit when the output looks wrong. Skipping it means the builder gets whatever fits in a prompt written from memory of a browser session.

## Skipping responsive extraction

Inspecting only at 1440px means the clone breaks at tablet and mobile. Sweep 1440, 768 and 390 during extraction, not after.

Related: `srcset` often swaps in different art at mobile widths, not just a smaller file. Re-run the global audit at 390px.

## Missing the smooth scroll library

Lenis, Locomotive Scroll and similar change how the whole page feels. Native scrolling against a Lenis original is noticeable within about two seconds of use. Check for `.lenis`, `[data-scroll-container]`, or `window.Lenis` during recon.

## Skipping asset extraction

Without the real images, videos and fonts the clone looks fake no matter how exact the CSS is.

## One monolithic commit

The pipeline earns its keep through verified builds at each merge. Batching everything to the end means debugging a hundred type errors at once with no known-good state to fall back to.

## Declaring done at green build

A clean `npm run build` says it compiles, not that it matches. Phase 5 is the check that matters, and its output includes the discrepancies still outstanding, named, not rounded away.
