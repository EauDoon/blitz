"""Strict, dependency-free parser for the kit's two string frontmatter keys.

This intentionally supports the bundled single-line name/description schema,
not arbitrary YAML: description must be quoted; a bare name must be a safe
slug. Quotes use doubled single quotes or JSON-compatible double quotes.
Reject collections, tags, aliases, duplicate/extra keys and implicit scalars.
"""
import json
import re


def printable(value):
    return all(ord(c) in {9, 10, 13, 0x85} or 0x20 <= ord(c) <= 0x7E
               or 0xA0 <= ord(c) <= 0xD7FF or 0xE000 <= ord(c) <= 0xFFFD
               or 0x10000 <= ord(c) <= 0x10FFFF for c in value)


def scalar(raw):
    if not printable(raw):
        raise ValueError("forbidden control or non-printable character")
    if raw.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", raw):
            raise ValueError("malformed single-quoted scalar")
        return raw[1:-1].replace("''", "'")
    if raw.startswith('"'):
        try:
            value = json.loads(raw)
        except ValueError as exc:
            raise ValueError("malformed double-quoted scalar") from exc
        if not isinstance(value, str):
            raise ValueError("frontmatter values must be strings")
        if not printable(value):
            raise ValueError("forbidden decoded control or non-printable character")
        return value
    if (not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", raw)
            or raw.lower() in {"true", "false", "yes", "no", "y", "n", "on", "off", "null"}):
        raise ValueError("unsafe or non-string plain scalar; quote the value")
    return raw


def parse_skill_frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("missing frontmatter")
    if not printable(match.group(1)):
        raise ValueError("forbidden control or non-printable character in frontmatter")
    values = {}
    for line in match.group(1).splitlines():
        row = re.fullmatch(r"([a-z][a-z0-9-]*):[ \t]+(.+)", line.rstrip())
        if not row or row.group(1) not in {"name", "description"} or row.group(1) in values:
            raise ValueError("frontmatter requires exactly one name and description string")
        key, raw = row.group(1), row.group(2).strip()
        if key == "description" and not raw.startswith(("'", '"')):
            raise ValueError("description must be a quoted single-line string")
        values[key] = scalar(raw)
    if set(values) != {"name", "description"} or not all(values.values()):
        raise ValueError("frontmatter requires nonempty name and description strings")
    return values
