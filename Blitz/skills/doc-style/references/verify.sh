#!/usr/bin/env bash
#
# verify.sh - pre-delivery machine checks for doc-style documents.
#
#   bash references/verify.sh "(06-08-26)Quarterly Budget Review.docx" [theme]
#
# Runs the four checks that a visual pass reliably misses:
#   check 6   bullet markers are native list items, not typed dashes
#   check 11  every colour in document.xml is in the active theme's palette
#   check 12  filename is (DD-MM-YY)Title With Proper Spaces
#   check 13  every font size in document.xml is in the theme's size set
#
# The theme is auto-detected from the accent colour in the built file. Pass it as
# a second argument (minimal | boardroom | editorial) to skip detection.
#
# Every allowlist below is copied from references/styles.js, which is the source
# of truth. Do not edit values here to make a build pass: a failure means the
# working copy of styles.js was stale. Recopy it and rebuild from source.

set -uo pipefail

FAILURES=0

pass() { printf 'PASS  %s\n' "$*"; }
fail() { printf 'FAIL  %s\n' "$*"; FAILURES=$((FAILURES + 1)); }
info() { printf '      %s\n' "$*"; }

usage() {
  cat >&2 <<'EOF'
usage: bash references/verify.sh <built-file.docx> [theme]

  <built-file.docx>  the built document, quoted (the house filename contains
                     spaces and parentheses, so an unquoted path splits)
  [theme]            minimal | boardroom | editorial
                     omitted: detected from the accent colour in the file

Runs checks 6, 11, 12 and 13 from the pre-delivery checklist.
Exits 0 if every check passes, 1 if any check fails, 2 on a usage error.
EOF
  exit 2
}

# ---------------------------------------------------------------- arguments --

[ "$#" -ge 1 ] || usage
case "${1:-}" in
  -h|--help|"") usage ;;
esac

FILE="$1"
THEME="${2:-}"

[ -f "$FILE" ] || { printf 'error: no such file: %s\n' "$FILE" >&2; exit 2; }

command -v unzip >/dev/null 2>&1 || { printf 'error: unzip not found\n' >&2; exit 2; }

DOCXML="$(unzip -p "$FILE" word/document.xml 2>/dev/null || true)"
[ -n "$DOCXML" ] || { printf 'error: could not read word/document.xml from %s\n' "$FILE" >&2; exit 2; }

# ------------------------------------------------------------------ palette --
# Per-theme colour allowlists: accent, accentLight, ruleColor, tableBorder,
# tableHeaderFill, tableHeaderText. Values from references/styles.js THEMES.

MINIMAL_COLORS="0F766E F0F7F6 DDDDDD FFFFFF E2E2E2"
BOARDROOM_COLORS="1F2A44 EEF1F6 FFFFFF C9CFDA"
EDITORIAL_COLORS="0F766E F0F7F6 DDDDDD FFFFFF E2E2E2"

# Neutrals permitted in any theme.
NEUTRAL_COLORS="111111 222222 333333 999999 DDDDDD E2E2E2 FFFFFF"

# RETIRED_COLORS in styles.js: the old editorial burgundy, plus the drifted
# green editorial replaced on 12-08-26 by the reference-pinned theme. Never valid.
RETIRED_COLORS="6B2B3D F2ECEE F7F1F3 2B6B47 F1F6F3 ECF2EE"

# --------------------------------------------------------------- font sizes --
# Half-points. Body/bullets/verdict/table cells 18; verdict label on the shaded
# themes bodySize-2 = 16; H3/H2/H1 per theme; subtitle 26 (18 editorial);
# title 44 (28 editorial, per the pinned reference doc).
# The footer's 15 lives in footer1.xml and is reported separately, not here.

MINIMAL_SIZES="18 20 23 26 30 44"
BOARDROOM_SIZES="16 18 21 24 26 32 44"
EDITORIAL_SIZES="18 20 22 26 28"

# ------------------------------------------------------------ theme detect --

detect_theme() {
  # minimal and editorial share the 0F766E accent since the editorial theme was
  # pinned to the reference Google Doc. Discriminate on H1 (30 minimal / 26
  # editorial), NOT on the title: a build may legitimately
  # override the title size, and keying on 44 misdetected every such build and
  # then failed it against the wrong size set.
  local found=""
  case "$DOCXML" in
    *0F766E*|*0f766e*)
      case "$DOCXML" in
        *'w:val="30"'*) found="minimal" ;;
        *'w:val="26"'*) found="editorial" ;;
        *'w:val="44"'*) found="minimal" ;;
        *)              found="" ;;
      esac ;;
  esac
  case "$DOCXML" in *1F2A44*|*1f2a44*) found="${found:+$found }boardroom" ;; esac
  printf '%s' "$found"
}

if [ -z "$THEME" ]; then
  THEME="$(detect_theme)"
  case "$THEME" in
    minimal|boardroom|editorial) info "theme detected from accent colour: $THEME" ;;
    "")  printf 'error: could not detect theme from accent plus H1 size.\n' >&2
         printf '       This is expected on a build with heading-size overrides.\n' >&2
         printf '       Pass the theme explicitly: minimal | boardroom | editorial\n' >&2
         exit 2 ;;
    *)   printf 'error: more than one theme accent present (%s). Pass the theme explicitly.\n' "$THEME" >&2
         exit 2 ;;
  esac
fi

case "$THEME" in
  minimal)   THEME_COLORS="$MINIMAL_COLORS";   THEME_SIZES="$MINIMAL_SIZES" ;;
  boardroom) THEME_COLORS="$BOARDROOM_COLORS"; THEME_SIZES="$BOARDROOM_SIZES" ;;
  editorial) THEME_COLORS="$EDITORIAL_COLORS"; THEME_SIZES="$EDITORIAL_SIZES" ;;
  *) printf 'error: unknown theme "%s". Use: minimal, boardroom, editorial\n' "$THEME" >&2; exit 2 ;;
esac

ALLOWED_COLORS="$THEME_COLORS $NEUTRAL_COLORS"

in_list() {  # in_list <needle> <space-separated list>
  local needle="$1" item
  for item in $2; do [ "$item" = "$needle" ] && return 0; done
  return 1
}

printf 'Verifying: %s\n' "$(basename "$FILE")"
printf 'Theme:     %s\n\n' "$THEME"

# ------------------------------------------------- check 6: bullet markers --
# Native cascade only: round bullet U+25CF (Noto Sans Symbols), lowercase o
# (Courier New), small square U+25AA (Noto Sans Symbols), the exact markers
# Google Docs exports. A dash marker builds and renders fine but Google Docs imports it
# as literal dash text. Scope to numbering.xml: docx-js also emits its own stock
# abstract numberings there and those are inert.

NUMXML="$(unzip -p "$FILE" word/numbering.xml 2>/dev/null || true)"
if [ -z "$NUMXML" ]; then
  fail "check 6 bullets: no word/numbering.xml in the file (no list was built)"
else
  BAD_MARKERS="$(
    printf '%s' "$NUMXML" \
      | grep -oE '<w:lvlText w:val="[^"]*"/>' \
      | grep -E 'w:val="(|[-*•·]|–|—|‒|―|−)"' | sort -u || true
  )"
  if [ -n "$BAD_MARKERS" ]; then
    fail "check 6 bullets: dash or empty bullet marker in word/numbering.xml"
    printf '%s\n' "$BAD_MARKERS" | while IFS= read -r m; do info "$m"; done
    info "styles.js was stale, or a Private Use Area codepoint was dropped in transport."
    info "Recopy styles.js from references/styles.js and rebuild from source."
    info "Never fix this by editing the output .docx."
  else
    pass "check 6 bullets: native markers, no typed dashes"
  fi
fi

# --------------------------------------------------------- check 11: colour --
# Scope to document.xml. styles.xml carries docx-js's stock heading blues
# (2E74B5, 1F4D78, 0563C1); they are overridden by explicit run colours and are
# not a defect, so grepping all of word/ would cry wolf on every run.

COLORS="$(
  printf '%s' "$DOCXML" \
    | grep -oE '="[0-9A-Fa-f]{6}"' \
    | grep -oE '[0-9A-Fa-f]{6}' | tr 'a-f' 'A-F' | sort -u || true
)"

BAD_COLORS=""
RETIRED_SEEN=""
for c in $COLORS; do
  if in_list "$c" "$RETIRED_COLORS"; then
    RETIRED_SEEN="${RETIRED_SEEN:+$RETIRED_SEEN }$c"
    BAD_COLORS="${BAD_COLORS:+$BAD_COLORS }$c"
  elif ! in_list "$c" "$ALLOWED_COLORS"; then
    BAD_COLORS="${BAD_COLORS:+$BAD_COLORS }$c"
  fi
done

if [ -n "$BAD_COLORS" ]; then
  fail "check 11 colour: value(s) outside the $THEME palette: $BAD_COLORS"
  if [ -n "$RETIRED_SEEN" ]; then
    info "RETIRED palette present: $RETIRED_SEEN (6B2B3D family = old burgundy; 2B6B47 family = drifted green editorial)."
    info "styles.js was stale. Recopy it from references/styles.js and rebuild from source."
    info "Do not patch the colours in the output file."
  fi
  info "permitted: $ALLOWED_COLORS"
else
  pass "check 11 colour: all values in the $THEME palette"
fi

# ------------------------------------------------------- check 12: filename --
# (DD-MM-YY)Title With Proper Spaces, extension appended. Real spaces, real
# capitals, no space after the closing parenthesis. Drive takes the document
# title from the filename, so rename before uploading, never after.

BASE="$(basename "$FILE")"
if [[ "$BASE" =~ ^\([0-9]{2}-[0-9]{2}-[0-9]{2}\)[A-Z] ]]; then
  pass "check 12 filename: $BASE"
else
  fail "check 12 filename: not in (DD-MM-YY)Title form: $BASE"
  info 'expected e.g. "(06-08-26)Quarterly Budget Review.docx"'
  info "Rename before uploading. Quote the path everywhere downstream."
fi

# ----------------------------------------------------- check 13: font sizes --
# Scope to document.xml, same reason as check 11.

SIZES="$(
  printf '%s' "$DOCXML" \
    | grep -oE '<w:sz w:val="[0-9]+"' \
    | grep -oE '[0-9]+' | sort -n | uniq -c || true
)"

BAD_SIZES=""
N18=0; N20=0; N21=0
while read -r count val; do
  [ -n "${val:-}" ] || continue
  in_list "$val" "$THEME_SIZES" || BAD_SIZES="${BAD_SIZES:+$BAD_SIZES }$val(x$count)"
  case "$val" in 18) N18=$count ;; 20) N20=$count ;; 21) N21=$count ;; esac
done <<< "$SIZES"

# 20 and 21 are legitimate H3 sizes, so the allowlist alone cannot catch a
# styles.js whose bodySize was never lowered to 18. Volume can: body paragraphs,
# bullets and table cells are all 18, so 18 dominates any real document.
STALE_BODY=""
[ "$N20" -gt "$N18" ] && STALE_BODY="20"
[ "$N21" -gt "$N18" ] && STALE_BODY="${STALE_BODY:+$STALE_BODY and }21"

if [ -n "$BAD_SIZES" ] || [ -n "$STALE_BODY" ]; then
  if [ -n "$BAD_SIZES" ]; then
    fail "check 13 font size: value(s) outside the $THEME set: $BAD_SIZES"
    info "permitted (half-points): $THEME_SIZES"
    case " $BAD_SIZES " in
      *" 17"*) info "17 means table cells are still on the old bodySize-1 derivation: styles.js is stale." ;;
    esac
    info "A single odd value means a Paragraph was hand-rolled outside the builders."
  fi
  if [ -n "$STALE_BODY" ]; then
    fail "check 13 font size: $STALE_BODY outnumbers 18 (x$N18); bodySize was never lowered to 18"
  fi
  info "Fix by recopying styles.js from references/styles.js and rebuilding, never by editing the .docx."
else
  pass "check 13 font size: all values in the $THEME set"
fi

# The footer's 15 lives in footer1.xml, not document.xml. Reported, not checked.
FOOTER_SIZES="$(unzip -p "$FILE" word/footer1.xml 2>/dev/null | grep -oE '<w:sz w:val="[0-9]+"' | grep -oE '[0-9]+' | sort -u | tr '\n' ' ' || true)"
[ -n "$FOOTER_SIZES" ] && info "footer1.xml sizes (expected 15): $FOOTER_SIZES"

# ------------------------------------------------------------------ verdict --

printf '\n'
if [ "$FAILURES" -eq 0 ]; then
  printf 'ALL CHECKS PASSED\n'
  exit 0
fi
printf '%d CHECK(S) FAILED. Fix at source and rebuild; do not edit the output .docx.\n' "$FAILURES"
exit 1
