# diagram-design evals

1. "Draw the architecture of a fiat-backed stablecoin mint and redeem flow." Passes if
   the output is a single self-contained HTML file, `scripts/lint-diagram.py` exits 0 on
   it, C3 and C5 hold on inspection, the accent lands on two elements or fewer, and no
   container is oversized against its contents. Fails on any linter failure, on a label
   mask touching its stroke, or on asking a setup question before drawing.
2. "Chart our stablecoin supply growth over the last six months." Passes if this skill
   does not fire and `viz-dashboards` takes it. Fails if a static SVG line chart is
   produced here.
3. "Make me a sequence diagram of the settlement handshake, it is going in my talk deck"
   (a dark presented preset). Passes if the build is light, converted with `skin.py dark`, `skin.py check` exits
   clean and no text in the dark file still names the light skin. Fails if dark hex was
   written by hand.
