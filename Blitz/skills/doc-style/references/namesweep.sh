#!/usr/bin/env bash
# namesweep.sh <document.md> <roster.txt>
# Roster: one individual's name per line, longest form first, built per document.
# Word boundaries matter: a bare grep for "Mark" matches "Market reference"
# in a live assumptions table. The \b anchors are not optional.
DOC="$1"; ROSTER="${2:-roster.txt}"
NAMES=$(paste -sd'|' "$ROSTER")
# Zone 1 runs from the top through section 1, so it ends at the SECOND H1.
# Do not key this on manually numbered headings ("## 2."): the house style
# forbids writing numbers into heading text (numbering is applied by the
# builder), so that pattern never matches a correctly written source and the
# whole file collapses into Zone 1, which false-BLOCKERs every Owner-column name.
ZONE1_END=$(grep -nE '^# ' "$DOC" | sed -n 2p | cut -d: -f1)
# Fallbacks, in order: the second H2, then a manually numbered section 2, then EOF.
[ -z "$ZONE1_END" ] && ZONE1_END=$(grep -nE '^## ' "$DOC" | sed -n 2p | cut -d: -f1)
[ -z "$ZONE1_END" ] && ZONE1_END=$(grep -nE '^#+ \**2\.' "$DOC" | head -1 | cut -d: -f1)
[ -z "$ZONE1_END" ] && ZONE1_END=$(wc -l < "$DOC")

echo "== ZONE 1 (title block, verdict, section 1): any hit is a violation =="
head -n $((ZONE1_END - 1)) "$DOC" | grep -nEo "\b(${NAMES})('s|’s)?\b" || echo "clean"

echo "== BODY, outside a table row: violation =="
grep -nE "\b(${NAMES})('s|’s)?\b" "$DOC" | awk -F: -v z="$ZONE1_END" '$1>=z' \
  | grep -vE '^[0-9]+:\s*\|' || echo "clean"

echo "== BODY, inside a table row: read each one =="
grep -nE "\b(${NAMES})('s|’s)?\b" "$DOC" | awk -F: -v z="$ZONE1_END" '$1>=z' \
  | grep -E '^[0-9]+:\s*\|' | cut -c1-140 || echo "none"
