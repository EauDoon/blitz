#!/usr/bin/env python3
"""Check inline HTML JavaScript without execution. Python 3 + Node required.

Exit 0: checked inline scripts pass (data scripts reported separately).
Exit 1: syntax/parser/tool failure. Exit 2: external scripts remain unchecked.
This is not a browser behavior, HTML validity or dependency-closure check.
"""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess

JS_TYPES = {"", "module", "text/javascript", "application/javascript", "text/ecmascript",
            "application/ecmascript", "application/x-javascript", "text/jscript", "text/livescript",
            "text/x-javascript", "text/x-ecmascript"} | {"text/javascript1." + str(i) for i in range(6)}


class Scripts(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.rows, self.current = [], None

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            # HTML keeps the first duplicate attribute, as browsers do.
            attributes = {}
            for name, value in attrs:
                attributes.setdefault(name, value or "")
            kind = attributes.get("type", "").strip().lower()
            if "type" not in attributes and attributes.get("language"):
                kind = "text/" + attributes["language"].strip().lower()
            self.current = {"line": self.getpos()[0], "type": kind,
                            "external": "src" in attributes, "body": ""}

    def handle_data(self, data):
        if self.current is not None:
            self.current["body"] += data

    def handle_startendtag(self, tag, attrs):
        if tag == "script":
            # In HTML, the self-closing slash does not end a script element.
            self.handle_starttag(tag, attrs)
            self.set_cdata_mode("script")
        else:
            super().handle_startendtag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "script" and self.current is not None:
            self.rows.append(self.current)
            self.current = None


def check(path):
    node = shutil.which("node")
    if node is None:
        raise ValueError("Node is required; no syntax checks ran")
    parser = Scripts()
    parser.feed(Path(path).read_text(encoding="utf-8-sig"))
    parser.close()
    if parser.current is not None:
        raise ValueError("Unclosed script element; no complete syntax check claimed")
    rows = []
    for index, row in enumerate(parser.rows):
        result = {"script": index + 1, "line": row["line"], "type": row["type"] or "classic"}
        if row["type"] not in JS_TYPES:
            result["status"] = "skipped-data"
        elif row["external"]:
            result["status"] = "unchecked-external"
        else:
            args = (["--check", "--input-type=module"] if row["type"] == "module" else
                    ["-e", "new (require('node:vm').Script)(require('node:fs').readFileSync(0,'utf8'))"])
            process = subprocess.run([node, *args], input=row["body"], text=True, encoding="utf-8",
                                     capture_output=True, timeout=15)
            result["status"] = "pass" if process.returncode == 0 else "fail"
            if process.returncode:
                # Do not echo source lines or local file paths in diagnostics.
                result["error"] = next((line for line in process.stderr.splitlines()
                                        if line.startswith("SyntaxError:")), "Node syntax check failed")
        rows.append(result)
    status = "fail" if any(r["status"] == "fail" for r in rows) else (
        "partial" if any(r["status"] == "unchecked-external" for r in rows) else "pass")
    return {"result": status, "checked": sum(r["status"] in {"pass", "fail"} for r in rows),
            "scripts": rows, "limits": "Syntax only. External sources and browser behavior are not verified."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    args = parser.parse_args()
    try:
        report = check(args.html)
    except (OSError, UnicodeError, ValueError, subprocess.TimeoutExpired) as error:
        report = {"result": "fail", "error": type(error).__name__, "limits": "Check did not complete."}
    print(json.dumps(report, indent=2))
    return {"pass": 0, "partial": 2, "fail": 1}[report["result"]]


if __name__ == "__main__":
    raise SystemExit(main())
