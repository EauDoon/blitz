# Onboarding a third skin

Two skins ship and cover almost everything: light for standalone figures, dark for
the owner's hex 0f0f0f surfaces. Both are defined in [style-guide.md](style-guide.md) and
converted by `scripts/skin.py`.

Use this file only when a diagram has to wear **someone else's brand**: a partner logo
deck, a co-marketing post, a client-facing figure. That is a third skin, and it is added
as a new map in the script, never by hand-editing hex.

---

## The flow

```
Design source (URL, a local design-system folder, or pasted tokens)
      -> extract dominant colours and fonts
      -> map to the semantic roles in style-guide.md
      -> add a named map to scripts/skin.py
      -> build light as always, then convert with that map
```

Roughly ten minutes. The build path never changes: always author light, always convert.

## Step 1, get the source

**From a URL.** Fetch the page with whatever browsing or fetch tool the session has.
Sample two or three pages (landing, blog, product) and merge the signals rather than
trusting one page. Never assume a specific browser tool exists; degrade to a plain fetch
of the HTML and CSS.

**From a local folder.** Glob for `*.css`, `tokens.json`, `theme.*`, `tailwind.config.*`
and any Markdown that documents a palette.

**From pasted tokens.** Take them as given and skip to step 2.

## Step 2, extract

Pull, in priority order:

1. **Background.** The dominant large-area colour. Becomes `paper`.
2. **Body text colour.** Usually near-black or near-white. Becomes `ink`.
3. **The one brand colour** used for buttons and links, the most saturated colour with
   meaningful area. Becomes `accent`.
4. **Secondary text grey.** Becomes `muted`; a lighter step becomes `soft`.
5. **Link colour**, if distinct from the accent. Otherwise derive one in the same hue
   family as `muted` but saturated.
6. **Font families**, in the order display, body, mono.

Ignore gradients, hero imagery colours, and anything appearing only in a logo.

## Step 3, map and sanity check

Fill the token table from [style-guide.md](style-guide.md), then check the constraints
that survive any re-skin. They are listed at the bottom of that file. The two that fail
most often:

- **One accent.** A brand with eight colours still gets one. The rest become `muted`
  variants or they are dropped.
- **Contrast.** `ink` on `paper` at WCAG AA, `muted` on `paper` at AA for 11px and up.
  Check it, do not assume it.

Show the proposed mapping as a table before writing anything. A brand skin that lands
wrong is more embarrassing than a default one.

## Step 4, add the map

Copy the `HEX_MAP` and `RGB_MAP` pattern in `scripts/skin.py` into a new named map, for
example `ACME`, keyed off the same light-skin source values. Then convert:

```
python3 scripts/skin.py dark diagram.html -o diagram-acme.html   # extend the CLI for a named map
python3 scripts/skin.py check diagram-acme.html
```

If the script reports unmapped colours, add them rather than patching the output file.
An unmapped colour means a diagram carrying two skins at once.

## Step 5, prove it

Render one converted diagram and look at it. Three specific failure modes to check for,
because none of them show up in a hex diff:

- The accent no longer reads as focal against the new paper.
- A hairline that was visible on light paper has vanished into the new background.
- Mono sublabels have dropped below AA and the technical detail is now unreadable.

If any of those show up, the mapping is wrong, not the diagram.
