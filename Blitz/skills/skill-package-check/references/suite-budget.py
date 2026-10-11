#!/usr/bin/env python3
"""suite-budget.py : listing budget gate for a Claude skill package.

Run this after build-check.py, on the same package, before delivering it.

    python3 suite-budget.py path/to/thing.skill [more.skill ...]
    python3 suite-budget.py path/to/skill-folder/
    python3 suite-budget.py                      (no package: measure the live suite)
    python3 suite-budget.py --selftest
    options: --manifest PATH, --host CHARS (host and plugin share, overrides the lookup)

Exit 0: the listing total with the package applied is at or under the ceiling.
Exit 1: over the ceiling, or a package that cannot be read. Do not deliver.
Exit 2: cannot measure here (no synced manifest, or a bad option). Measure in a
        session that has a synced manifest before delivering.

Why it exists. Claude Code gives the skill listing 1% of the model's context window
in characters, at 3 characters a token on current models and 4 on older ones:
30,000 on Opus 5.5 and Sonnet (1M context), 8,000 on Haiku (200k context), measured
on Claude Code 2.1.284, 30-09-2026. Over the budget, skills at the tail of load
order render as bare names that can only fire on a name match, and which ones
changes by session. A per-description target does not protect the total; this does.

How it counts. Every listing entry is "- <name>: <description>" on its own line, and
a when_to_use key renders after the description as " - <when_to_use>". Account
skills are listed as "anthropic-skills:<name>" and come from the synced manifest,
with each package's name and description swapped in or added. Host-bundled and
plugin skills are not in the manifest: their share is read from this session's own
listing when the session log carries a complete one, else the measured constant
below. On 30-09-2026 this reproduced the live listing exactly: 27,971 characters.
"""

import glob
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

BUDGET = 30000        # 1% of a 1M-token context at 3 characters a token
CEILING = 28500       # suite rule, 30-09-2026: a 1,500 margin under the budget
ACCOUNT_PREFIX = "anthropic-skills:"
# Host and plugin entries, measured from a live listing on 30-09-2026: 15 entries,
# each counted as len(name) + len(description) + 5.
HOST_DEFAULT = 5221
# On the account but not in the Claude Code listing (a managed setting switches
# it off in these containers; seen 25-09-2026 and 30-09-2026).
EXCLUDE_DEFAULT = ("docs",)
LISTING_HEAD = "The following skills are available for use with the Skill tool:"


class Unreadable(Exception):
    pass


def entry_cost(listed_name, description, when_to_use=""):
    """'- ' + name + ': ' + description [+ ' - ' + when_to_use] + newline."""
    extra = len(when_to_use) + 3 if when_to_use else 0
    return len(listed_name) + len(description) + extra + 5


# ---------------------------------------------------------------- inputs


def find_manifest(explicit=None):
    if explicit is not None:
        return explicit if os.path.isfile(explicit) else None
    pats = [os.path.expanduser("~/.claude/skills/synced/*/manifest.json"),
            "/root/.claude/skills/synced/*/manifest.json"]
    hits = sorted(set(h for p in pats for h in glob.glob(p)), key=os.path.getmtime)
    return hits[-1] if hits else None


def read_frontmatter(text):
    """Return {key: value} for top-level scalar keys, whitespace collapsed.

    Handles single-line values, quoted values with doubled apostrophes, values
    wrapped onto indented continuation lines, and > or | block scalars. Raises
    Unreadable on an unclosed quote or a missing frontmatter block.
    """
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        raise Unreadable("no frontmatter block")
    raw, key = {}, None
    for line in m.group(1).split("\n"):
        line = line.rstrip("\r")
        k = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*)$", line)
        if k and not line.startswith((" ", "\t")):
            key = k.group(1)
            raw[key] = [k.group(2)]
        elif key is not None:
            raw[key].append(line.strip())
    out = {}
    for key, parts in raw.items():
        head, rest = parts[0].strip(), [p for p in parts[1:] if p]
        if re.match(r"^[>|][+-]?[0-9]?$", head):
            v = " ".join(rest)
        else:
            v = " ".join([head] + rest).strip()
            if v[:1] in ("'", '"'):
                q = v[0]
                if len(v) < 2 or v[-1] != q:
                    raise Unreadable("%s has an unclosed %s quote" % (key, q))
                v = v[1:-1]
                v = v.replace("''", "'") if q == "'" else v.replace('\\"', '"')
        out[key] = " ".join(v.split())
    return out


def read_package(path):
    """Return (name, description, when_to_use) of a .skill zip or a skill folder."""
    if os.path.isdir(path):
        fn = os.path.join(path, "SKILL.md")
        if not os.path.isfile(fn):
            raise Unreadable("no SKILL.md in %s" % path)
        with open(fn, encoding="utf-8") as fh:
            text = fh.read()
    elif zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            tops = [n for n in zf.namelist() if n.count("/") == 1 and n.endswith("/SKILL.md")]
            if len(tops) != 1:
                raise Unreadable("%s: need exactly one <folder>/SKILL.md" % path)
            text = zf.read(tops[0]).decode("utf-8")
    else:
        raise Unreadable("%s is neither a folder nor a zip" % path)
    fm = read_frontmatter(text)
    if not fm.get("name") or not fm.get("description"):
        raise Unreadable("%s: name or description missing" % path)
    return fm["name"], fm["description"], fm.get("when_to_use", "")


def parse_listing_block(block):
    """Host and plugin share from the text after LISTING_HEAD, or None.

    None when the block is not a complete listing: no account entries, no host
    entries, or any bare '- name' line (a skill shown without its description
    means the listing is already over budget and undercounts).
    """
    entries = []
    for line in block.split("\n"):
        if re.match(r"^- \S+\s*$", line):
            return None
        m = re.match(r"^- (\S+?): (.*)$", line)
        if m:
            entries.append((m.group(1), m.group(2)))
        elif entries and line.strip():
            break
    host = [(n, d) for n, d in entries if not n.startswith(ACCOUNT_PREFIX)]
    if not host or len(host) == len(entries):
        return None
    return sum(entry_cost(n, d) for n, d in host), len(host)


def live_host_share():
    """(chars, entries, log path) from the newest session log's listing, or None."""
    logs = glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl"))
    logs += glob.glob("/root/.claude/projects/*/*.jsonl")
    if not logs:
        return None
    newest = max(set(logs), key=os.path.getmtime)
    best = None
    try:
        with open(newest, encoding="utf-8") as fh:
            for line in fh:
                if LISTING_HEAD not in line:
                    continue
                try:
                    obj = json.loads(line)
                except ValueError:
                    continue
                for s in walk(obj):
                    if LISTING_HEAD in s and (best is None or len(s) > len(best)):
                        best = s
    except OSError:
        return None
    if best is None:
        return None
    got = parse_listing_block(best[best.rindex(LISTING_HEAD) + len(LISTING_HEAD):])
    return (got[0], got[1], newest) if got else None


def walk(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


# ---------------------------------------------------------------- measure


def total(account, host_chars):
    """account: {name: (description, when_to_use)}. The last entry has no newline."""
    return sum(entry_cost(ACCOUNT_PREFIX + k, d, w) for k, (d, w) in account.items()) \
        + host_chars - 1


def run(pkgs, manifest=None, host=None, exclude=EXCLUDE_DEFAULT, out=sys.stderr):
    mpath = find_manifest(manifest)
    if not mpath:
        out.write("CANNOT MEASURE  no synced manifest on this surface. Run this in a "
                  "session that has ~/.claude/skills/synced/*/manifest.json, or pass "
                  "--manifest. Do not deliver on an unmeasured total.\n")
        return 2
    with open(mpath, encoding="utf-8") as fh:
        man = json.load(fh)
    account = {s["name"]: (" ".join(s["description"].split()), "")
               for s in man["skills"] if s["name"] not in exclude}

    if host is not None:
        host_chars, host_src = host, "given with --host"
    else:
        live = live_host_share()
        if live:
            host_chars = live[0]
            host_src = "this session's listing, %d entries, %s" % (live[1], live[2])
        else:
            host_chars = HOST_DEFAULT
            host_src = ("measured constant of 30-09-2026; no complete listing in the "
                        "session log")

    before = total(account, host_chars)
    changes = []
    for p in pkgs:
        try:
            name, desc, wtu = read_package(p)
        except (Unreadable, UnicodeDecodeError, zipfile.BadZipFile, OSError) as exc:
            out.write("FAIL  cannot read the package: %s\n" % exc)
            return 1
        old = account.get(name)
        account[name] = (desc, wtu)
        new_cost = entry_cost(ACCOUNT_PREFIX + name, desc, wtu)
        if old is None:
            changes.append("%s added, +%d" % (name, new_cost))
        else:
            delta = new_cost - entry_cost(ACCOUNT_PREFIX + name, *old)
            changes.append("%s %d to %d characters%s, %+d" % (
                name, len(old[0]), len(desc),
                " plus when_to_use %d" % len(wtu) if wtu else "", delta))
    after = total(account, host_chars)

    stamp = man.get("lastUpdated", "unknown")
    if isinstance(stamp, (int, float)):
        import datetime
        stamp = datetime.datetime.fromtimestamp(stamp / 1000, datetime.timezone.utc) \
            .strftime("%d-%m-%Y %H:%M UTC")
    out.write("Manifest  %s (synced %s)\n" % (mpath, stamp))
    out.write("Host and plugin share  %d (%s)\n" % (host_chars, host_src))
    for c in changes:
        out.write("Package  %s\n" % c)
    out.write("Listing total  %d before, %d after; ceiling %d, budget %d\n"
              % (before, after, CEILING, BUDGET))
    if after > CEILING:
        out.write("FAIL  the listing would be %d characters, %d over the %d ceiling. "
                  "Trim, retire or switch off a skill first.\n"
                  % (after, after - CEILING, CEILING))
        return 1
    out.write("OK    headroom %d to the ceiling, %d to the budget\n"
              % (CEILING - after, BUDGET - after))
    return 0


# ---------------------------------------------------------------- selftest


def selftest():
    import io
    d = tempfile.mkdtemp()
    try:
        return _selftest(d, io)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def _selftest(d, io):
    man = os.path.join(d, "manifest.json")

    def write_manifest(entries):
        with open(man, "w") as fh:
            json.dump({"skills": [{"name": n, "description": v} for n, v in entries]}, fh)

    def package(name, frontmatter):
        folder = os.path.join(d, name)
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "SKILL.md"), "w") as fh:
            fh.write("---\nname: %s\n%s\n---\n\n# X\n\nBody.\n" % (name, frontmatter))
        return folder

    def desc(n, ch):
        return "description: '%s'" % (ch * n)

    failures = []
    quiet = io.StringIO()
    base = [("alpha", "a" * 100), ("beta", "b" * 100), ("docs", "d" * 100)]
    write_manifest(base)
    listed = {"alpha": ("a" * 100, ""), "beta": ("b" * 100, "")}

    # 1. arithmetic: two listed entries (docs excluded) plus the host share.
    got = total(listed, 1000)
    if got != (17 + 5 + 100 + 5) + (17 + 4 + 100 + 5) + 1000 - 1:
        failures.append("arithmetic")
    # 2. under the ceiling passes.
    if run([], manifest=man, host=1000, out=quiet) != 0:
        failures.append("rejected a suite under the ceiling")
    # 3 and 4. the suite sits 50 under the ceiling: +80 on alpha fails, -10 passes.
    host = CEILING - 50 - (got - 1000 + 1) + 1
    if total(listed, host) != CEILING - 50:
        failures.append("selftest setup")
    if run([package("alpha", desc(180, "a"))], manifest=man, host=host, out=quiet) != 1:
        failures.append("passed a package that crosses the ceiling")
    if run([package("alpha", desc(90, "a"))], manifest=man, host=host, out=quiet) != 0:
        failures.append("rejected a package that shortens a description")
    # 5. a new skill costs name plus description plus 22.
    buf = io.StringIO()
    run([package("gamma", desc(200, "g"))], manifest=man, host=1000, out=buf)
    if "gamma added, +%d" % (17 + 5 + 200 + 5) not in buf.getvalue():
        failures.append("new skill cost")
    # 6. no manifest means cannot measure, never a pass.
    if run([], manifest=os.path.join(d, "missing.json"), host=1000, out=quiet) != 2:
        failures.append("did not refuse a missing manifest")
    # 7. frontmatter forms all measure the full text.
    forms = {
        "quoted": "description: 'It''s a test: with a colon.'",
        "folded": "description: >\n  It's a test:\n  with a colon.",
        "wrapped": "description: 'It''s a test:\n  with a colon.'",
    }
    for label, fm in forms.items():
        try:
            n = read_frontmatter("---\nname: x\n%s\n---\nbody\n" % fm)["description"]
        except Unreadable:
            n = None
        if n != "It's a test: with a colon.":
            failures.append("frontmatter %s read as %r" % (label, n))
    # 8. an unclosed quote is refused, never measured short.
    if run([package("alpha", "description: 'never closed")], manifest=man,
           host=1000, out=quiet) != 1:
        failures.append("measured a description with an unclosed quote")
    # 9. when_to_use counts: rendered as ' - ' plus its text.
    buf = io.StringIO()
    run([package("delta", desc(100, "x") + "\nwhen_to_use: '" + "w" * 900 + "'")],
        manifest=man, host=1000, out=buf)
    if "delta added, +%d" % (17 + 5 + 100 + 903 + 5) not in buf.getvalue():
        failures.append("when_to_use not counted")
    # 10. a listing block with a bare name is refused; a complete one is read.
    ok = "\n- host-a: aaa\n- anthropic-skills:alpha: bbb\n\nnext section\n"
    bare = "\n- host-a: aaa\n- plugin-b\n- anthropic-skills:alpha: bbb\n"
    if parse_listing_block(ok) != (len("host-a") + 3 + 5, 1):
        failures.append("complete listing block misread")
    if parse_listing_block(bare) is not None:
        failures.append("listing block with a bare name accepted")

    if failures:
        for f in failures:
            sys.stderr.write("SELFTEST FAIL  %s\n" % f)
        return 1
    sys.stderr.write("SELFTEST OK    10/10\n")
    return 0


def main(args):
    if args == ["--selftest"]:
        return selftest()
    manifest = host = None
    pkgs = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--manifest", "--host"):
            if i + 1 >= len(args) or args[i + 1].startswith("--"):
                sys.stderr.write("BAD OPTION  %s needs a value\n" % a)
                return 2
            v = args[i + 1]
            if a == "--manifest":
                manifest = v
            else:
                if not v.isdigit() or int(v) <= 0:
                    sys.stderr.write("BAD OPTION  --host needs a positive whole number\n")
                    return 2
                host = int(v)
            i += 2
            continue
        if a in ("-h", "--help"):
            sys.stderr.write(__doc__)
            return 2
        if a.startswith("--"):
            sys.stderr.write("BAD OPTION  %s\n" % a)
            return 2
        pkgs.append(a)
        i += 1
    return run(pkgs, manifest=manifest, host=host)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
