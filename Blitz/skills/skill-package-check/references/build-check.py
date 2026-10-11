#!/usr/bin/env python3
"""build-check.py : generic gate for a Claude skill package.

Run this on EVERY .skill file before delivering it, not just on the skill you happen
to be editing. It is not specific to any one skill.

    python3 build-check.py path/to/thing.skill
    python3 build-check.py path/to/skill-folder/

Exit 0 means the package is safe to deliver. Exit 1 means do not deliver it.

Why it exists. Two failure modes have each cost a delivery round, and neither of them
looks like a failure at the time:

  1. description over 1024 characters. The save is rejected outright with
     "field 'description' in SKILL.md must be at most 1024 characters". The OLD
     version stays installed, so the symptom is "the change did nothing".
  2. an unquoted ": " inside the description breaks the YAML. The skill then fails
     to load with NO error at all, which is worse.

Both are covered by a negative test at the bottom of this file: run
`python3 build-check.py --selftest` to confirm the checker still catches them.
"""

import io
import os
import re
import sys
import zipfile

MAX_DESC = 1024
WARN_DESC = 220  # suite target set by meta-skill, 30-09-2026 (300 from 25-09-2026)
REQUIRED = ("name", "description")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


# ---------------------------------------------------------------- loading


def load_package(path):
    """Return (root_name, {relative_path: bytes})."""
    if os.path.isdir(path):
        files = {}
        for dirpath, _dirnames, filenames in os.walk(path):
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, path).replace(os.sep, "/")
                with open(full, "rb") as fh:
                    files[rel] = fh.read()
        return os.path.basename(os.path.normpath(path)), files

    if not zipfile.is_zipfile(path):
        err("not a zip archive and not a directory: %s" % path)
        return None, {}

    try:
        zf = zipfile.ZipFile(path)
    except Exception as exc:  # pragma: no cover
        err("cannot open zip: %s" % exc)
        return None, {}

    bad = zf.testzip()
    if bad is not None:
        err("corrupt member in zip: %s" % bad)

    names = [n for n in zf.namelist() if not n.endswith("/")]
    if not names:
        err("zip is empty")
        return None, {}

    roots = set(n.split("/")[0] for n in names)
    if len(roots) != 1:
        err("zip must contain exactly one top-level folder, found %d: %s"
            % (len(roots), ", ".join(sorted(roots))))
        return None, {}

    root = roots.pop()
    files = {}
    for n in names:
        rel = n[len(root) + 1:] if n.startswith(root + "/") else n
        if rel:
            files[rel] = zf.read(n)
    return root, files


# ---------------------------------------------------------------- frontmatter


def split_frontmatter(text):
    """Return (frontmatter_text, body) or (None, text) if absent."""
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", text, re.S)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def parse_scalar_fields(fm):
    """Minimal YAML scalar reader. Returns {key: (raw_value, quote_char_or_None)}.

    Deliberately does not use PyYAML: an unquoted colon is the exact failure being
    tested for, and a real parser either raises or silently reinterprets it.
    """
    fields = {}
    key = None
    buf = []
    for line in fm.split("\n"):
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            if key is not None:
                fields[key] = "\n".join(buf).strip()
            key = m.group(1)
            buf = [m.group(2)]
        elif key is not None:
            buf.append(line.strip())
    if key is not None:
        fields[key] = "\n".join(buf).strip()

    out = {}
    for k, v in fields.items():
        q = None
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            q = v[0]
            v = v[1:-1]
        out[k] = (v, q)
    return out


def check_skill_md(root, text):
    fm, body = split_frontmatter(text)
    if fm is None:
        err("SKILL.md has no YAML frontmatter delimited by --- lines")
        return
    if not body.strip():
        err("SKILL.md has frontmatter but no body")

    fields = parse_scalar_fields(fm)

    for req in REQUIRED:
        if req not in fields or not fields[req][0].strip():
            err("frontmatter is missing required field '%s'" % req)

    if "name" in fields:
        name = fields["name"][0].strip()
        if not NAME_RE.match(name):
            err("name '%s' must be lowercase letters, digits and single hyphens" % name)
        if root and name != root:
            err("name '%s' does not match the package folder '%s'" % (name, root))

    if "description" in fields:
        raw, quote = fields["description"]
        desc = " ".join(raw.split())
        n = len(desc)
        if n > MAX_DESC:
            err("description is %d characters, over the %d cap. The save will be "
                "REJECTED and the old version will stay installed." % (n, MAX_DESC))
        elif n > WARN_DESC:
            warn("description is %d characters, over the %d suite target (cap %d). "
                 "Re-run the trigger eval, because trimming to fit can drop the sentence "
                 "carrying the routing." % (n, WARN_DESC, MAX_DESC))

        if quote is None and (": " in raw or raw.rstrip().endswith(":")):
            err("description contains an unquoted ': ' which breaks the YAML. The skill "
                "will fail to load with no error at all. Single-quote the description.")
        if quote == "'" and "''" not in raw and "'" in raw:
            err("description is single-quoted but contains a bare apostrophe. Escape it "
                "by doubling it, or switch to double quotes.")
        if quote == '"':
            unescaped = re.search(r'(?<!\\)"', raw)
            if unescaped:
                err("description is double-quoted but contains an unescaped double quote.")

    # Reference paths named in the body. Only concrete filenames count: a bare
    # "references/" or a glob stem like "references/type-" is prose, not a path.
    this_name = fields.get("name", ("", None))[0].strip()
    for line in body.split("\n"):
        for ref in re.findall(r"references/[A-Za-z0-9_.\-]+\.[A-Za-z0-9]{1,5}\b", line):
            # A line naming another skill is describing that skill's file, not ours.
            others = [t for t in re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`", line)
                      if t != this_name]
            MISSING_REFS.append((ref, bool(others)))


MISSING_REFS = []


# ---------------------------------------------------------------- main


def check(path):
    del errors[:]
    del warnings[:]
    del MISSING_REFS[:]

    root, files = load_package(path)
    if not files:
        return 1

    md_paths = [p for p in files if p.lower().endswith("skill.md")]
    if "SKILL.md" not in files:
        if md_paths:
            err("SKILL.md must sit at the top of the package folder, found it at: %s"
                % ", ".join(md_paths))
        else:
            err("no SKILL.md in the package")
        return finish()
    if len(md_paths) > 1:
        err("more than one SKILL.md in the package: %s" % ", ".join(sorted(md_paths)))

    try:
        text = files["SKILL.md"].decode("utf-8")
    except UnicodeDecodeError:
        err("SKILL.md is not valid UTF-8")
        return finish()

    check_skill_md(root, text)

    seen = set()
    for ref, foreign in MISSING_REFS:
        if ref in files or ref in seen:
            continue
        seen.add(ref)
        hint = " (a line naming another skill, so probably that skill's file)" if foreign else ""
        warn("SKILL.md names %s, which is not in this package%s. Check it by eye: a "
             "cross-skill reference is fine, a missing own file is not." % (ref, hint))

    for p, b in files.items():
        if p.endswith((".py", ".js", ".sh", ".md")) and b == b"":
            err("%s is empty" % p)

    return finish()


def finish():
    for w in warnings:
        sys.stderr.write("WARN  %s\n" % w)
    for e in errors:
        sys.stderr.write("FAIL  %s\n" % e)
    if errors:
        sys.stderr.write("\n%d error(s). Do not deliver this package.\n" % len(errors))
        return 1
    sys.stderr.write("OK    package passes%s\n"
                     % (" with %d warning(s)" % len(warnings) if warnings else ""))
    return 0


# ---------------------------------------------------------------- selftest


def selftest():
    """Negative tests for the two failure modes that have actually happened."""
    import tempfile

    def build(desc_line, name="demo-skill"):
        d = tempfile.mkdtemp()
        folder = os.path.join(d, name)
        os.makedirs(folder)
        with open(os.path.join(folder, "SKILL.md"), "w") as fh:
            fh.write("---\nname: %s\n%s\n---\n\n# Demo\n\nBody.\n" % (name, desc_line))
        return folder

    failures = []

    over = "description: '" + ("x" * 1100) + "'"
    if check(build(over)) == 0:
        failures.append("did not catch an over-cap description")

    colon = "description: Use this when the user says: do the thing"
    if check(build(colon)) == 0:
        failures.append("did not catch an unquoted colon")

    good = "description: 'Use this when the user says do the thing, and not otherwise.'"
    if check(build(good)) != 0:
        failures.append("rejected a valid package")

    if failures:
        for f in failures:
            sys.stderr.write("SELFTEST FAIL  %s\n" % f)
        return 1
    sys.stderr.write("SELFTEST OK    3/3\n")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        sys.exit(selftest())
    if len(sys.argv) != 2:
        sys.stderr.write(__doc__)
        sys.exit(2)
    sys.exit(check(sys.argv[1]))
