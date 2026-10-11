#!/usr/bin/env python3
"""Check the Blitz kit before setup (setup step 2).

Usage (from anywhere):
    python3 setup/verify_kit.py

Checks, each reported as PASS or FAIL:
  1. Integrity: every file in manifest.json exists and matches its SHA-256;
     no file sits in the kit without a manifest entry.
  2. Skills: each folder in skills/ has SKILL.md with strict two-string
     frontmatter (collections/tags/aliases/duplicate/extra keys rejected), a name that
     matches the folder, a description at or under 1,024 characters, a
     SKILL.md at or under 22,000 characters and 22,000 UTF-8 bytes, and
     agents/openai.yaml.
  3. House text: no em or en dash in any .md file outside skills/.
  4. Leak check: no restricted term (stored as hashes, so this file does not
     carry them) and no local user path in any text file.
Prints KIT OK and exits 0 only when every check passes.
"""
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from frontmatter import parse_skill_frontmatter
from verify_archive import (MAX_FILE, MAX_FILES, MAX_TOTAL, guard_local_path, load_json,
                            require, safe_relative, unique_paths, validate_manifest, validate_payload)

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESTRICTED = {  # first 16 hex of sha256 of the lowercase term
    "324ffbadc4c9f775", "b0442c88eea3fe5d", "040974aabfd1c691", "bc9a1a86ec98507e",
    "e999375bf16caa32", "848a37fa85f16979", "1b33caf91a913c55", "7603839d7c30c103",
    "997077f5a47a9efa", "6342a668c18d000b", "a932573e7ecf5cc3", "c213e91aeee06b20", "41c55ac752be450f",
}
PATH_RX = re.compile(r"[A-Za-z]:\\+Users\\+|/Users/[A-Za-z]")
DASH_RX = re.compile("[–—]")
TEXT_EXT = {".md", ".txt", ".json", ".py", ".js", ".sh", ".yaml", ".yml", ".html", ".css", ".mjs"}


def h(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def sha256_file(p):
    d = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            d.update(chunk)
    return d.hexdigest()


def raise_walk_error(error):
    raise error


def all_files():
    for root, _, files in os.walk(KIT, onerror=raise_walk_error):
        for f in files:
            full = os.path.join(root, f)
            yield os.path.relpath(full, KIT).replace(os.sep, "/")


def check_integrity(fails):
    try:
        root = guard_local_path(KIT)
        require(root.is_dir(), "kit is not a directory")
        actual, keys, inodes, total = {}, set(), set(), 0
        # Inventory all entries before reading any manifest-listed payload.
        for current, dirs, names in os.walk(root, followlinks=False, onerror=raise_walk_error):
            for name in sorted(dirs + names):
                path = guard_local_path(Path(current) / name)
                rel = path.relative_to(root).as_posix()
                require(safe_relative(rel), "unsafe path:" + rel)
                key = rel.casefold()
                require(key not in keys, "duplicate or case collision:" + rel)
                keys.add(key)
                info = path.lstat()
                if stat.S_ISDIR(info.st_mode):
                    continue
                require(stat.S_ISREG(info.st_mode), "nonregular file:" + rel)
                inode = (info.st_dev, info.st_ino)
                require(info.st_nlink == 1 and inode not in inodes, "hardlink or duplicate identity:" + rel)
                inodes.add(inode)
                require(info.st_size <= MAX_FILE, "oversize entry:" + rel)
                total += info.st_size
                require(total <= MAX_TOTAL, "oversize kit")
                actual[rel] = path
                require(len(actual) <= MAX_FILES + 1, "invalid kit file count")
        require("manifest.json" in actual, "manifest.json missing")
        manifest = load_json(actual["manifest.json"].read_bytes())
        listed = validate_manifest(manifest)
        missing = set(listed) - set(actual)
        extra = set(actual) - {*listed, "manifest.json"}
        require(not missing, "missing " + ", ".join(sorted(missing)))
        require(not extra, "not in manifest " + ", ".join(sorted(extra)))
        unique_paths(list(actual))
        for rel, row in listed.items():
            # Reads are bounded by the already checked stable local snapshot.
            with actual[rel].open("rb") as stream:
                data = stream.read(MAX_FILE + 1)
            require(len(data) <= MAX_FILE, "oversize entry:" + rel)
            validate_payload(rel, data, row)
    except (OSError, ValueError, TypeError, KeyError, UnicodeError, RuntimeError) as exc:
        fails.append("integrity: " + str(exc))

def check_references(fails):
    """Resolve local Markdown links; host/external paths are capability dependencies."""
    for rel in all_files():
        if not rel.endswith(".md"):
            continue
        p = Path(KIT) / rel
        if p.is_symlink():
            continue
        with p.open(encoding="utf-8") as stream:
            t = stream.read()
        for raw in re.findall(r"\[[^\]]*\]\(([^)]+)\)", t):
            target = raw.split(' "')[0].split("#")[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            dest = (p.parent / target).resolve()
            if Path(KIT) not in dest.parents and dest != Path(KIT):
                fails.append("references: local link escapes kit in %s" % rel)
            elif not dest.exists():
                fails.append("references: missing %s in %s" % (target, rel))


def check_skills(fails):
    sdir = os.path.join(KIT, "skills")
    for name in sorted(os.listdir(sdir)):
        d = os.path.join(sdir, name)
        if not os.path.isdir(d):
            continue
        sm = os.path.join(d, "SKILL.md")
        if not os.path.exists(sm):
            fails.append("skills: %s has no SKILL.md" % name)
            continue
        t = open(sm, encoding="utf-8").read()
        try:
            metadata = parse_skill_frontmatter(t)
        except ValueError as exc:
            fails.append("skills: %s invalid frontmatter: %s" % (name, exc))
            continue
        if metadata["name"] != name:
            fails.append("skills: %s name does not match its folder" % name)
        desc = metadata["description"]
        if not desc or len(desc) > 1024:
            fails.append("skills: %s description length %d" % (name, len(desc)))
        if len(t) > 22000 or len(t.encode("utf-8")) > 22000:
            fails.append("skills: %s SKILL.md over 22,000 characters or bytes" % name)
        if not os.path.exists(os.path.join(d, "agents", "openai.yaml")):
            fails.append("skills: %s has no agents/openai.yaml" % name)


def check_text(fails):
    for rel in all_files():
        ext = os.path.splitext(rel)[1].lower()
        if ext not in TEXT_EXT:
            continue
        try:
            t = open(os.path.join(KIT, rel), encoding="utf-8").read()
        except UnicodeDecodeError:
            continue
        if ext == ".md" and not rel.startswith("skills/") and DASH_RX.search(t):
            fails.append("house text: em or en dash in %s" % rel)
        if PATH_RX.search(t):
            fails.append("leak: local user path in %s" % rel)
        words = re.findall(r"[a-z0-9]+", t.lower())
        grams = set(words) | {a + " " + b for a, b in zip(words, words[1:])}
        if any(h(g) in RESTRICTED for g in grams):
            fails.append("leak: restricted term in %s" % rel)


def main():
    fails = []
    check_integrity(fails)
    integrity_failed = bool(fails)
    if not integrity_failed:
        check_skills(fails)
        check_text(fails)
        check_references(fails)
    groups = ["integrity", "skills", "house text", "leak", "references"]
    for g in groups:
        bad = [f for f in fails if f.startswith(g)]
        status = "NOT RUN (integrity failure)" if integrity_failed and g != "integrity" else "PASS" if not bad else "FAIL (%d)" % len(bad)
        print("%-10s %s" % (g, status))
        for f in bad[:20]:
            print("    " + f)
    if fails:
        print("KIT FAILED")
        sys.exit(1)
    print("KIT OK")


if __name__ == "__main__":
    main()
