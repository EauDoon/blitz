#!/usr/bin/env python3
"""Focused source-view checks, with synthetic bytes and no live project writes."""
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import zipfile
from types import SimpleNamespace
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / "setup/build_context.py"
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("build_context", MODULE)
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


def reject(call, contains):
    try:
        call()
    except (ValueError, OSError) as exc:
        assert contains in str(exc), str(exc)
    else:
        raise AssertionError("accepted invalid input: " + contains)


def put(root, rel, data):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def run():
    with tempfile.TemporaryDirectory(prefix="source-context-check-") as temp:
        base = Path(temp)
        kit = base / "kit"
        for method in context.METHOD_GROUP:
            put(kit, "skills/" + method + "/SKILL.md", ("---\nname: " + method + "\ndescription: 'Synthetic route for " + method + ".'\n---\n\n# " + method + "\n").encode())
        skill = put(kit, "skills/blitz/SKILL.md", b"---\r\nname: blitz\r\ndescription: 'Synthetic launch route.'\r\n---\r\n\r\n# Blitz\r\nRead [nested](references/deep.md), [asset](assets/runtime.js), [missing](missing.md).\r\n")
        nested = b"# Deep\r\nFull nested method. Read [shared](../../../templates/handoff.md).\r\n`````\ncode\n`````\n"
        put(kit, "skills/blitz/references/deep.md", nested)
        put(kit, "skills/blitz/assets/runtime.js", b"throw new Error('never execute');\n")
        put(kit, "skills/blitz/LICENSE", b"Full license statement.\n")
        put(kit, "skills/blitz/evals/answer-key.md", b"HIDDEN_FIXTURE_ANSWER")
        put(kit, "skills/blitz/answer-key.json", b'{"answer":"HIDDEN_FIXTURE_ANSWER"}')
        put(kit, "setup/build-notes.md", b"HIDDEN_FIXTURE_BUILDER_NOTES")
        put(kit, "setup/source-context-manifest.json", b'{"legacy":"HIDDEN_FIXTURE_MANIFEST"}')
        put(kit, "setup/" + context.CONTEXT_MANIFEST, b'{"current":"HIDDEN_FIXTURE_MANIFEST"}')
        put(kit, "evals/fixtures/input.md", b"HIDDEN_FIXTURE_INPUT")
        put(kit, "templates/handoff.md", b"# Handoff\nRead the adopted revision.\n")
        put(kit, "templates/receipt.json", b'{"status":"NOT TESTED"}\n')
        guide = b"# Launch\r\nRead Blitz_v2.1OAI-r1_Method_Index.md.\r\n"
        body = b"Exact instructions.\r\nRetain Work.\r\n"
        put(kit, "setup/source-use.md", guide)
        put(kit, "setup/Blitz_Project_Instructions.md", body)
        register = b"# Register\r\nNOT APPLIED. Target execution NOT TESTED.\r\n"
        put(kit, "setup/Blitz_System_Register.md", register)
        put(kit, "setup/operating-contract.md", b"# Operating contract\nKeep the commission.\n")
        put(kit, "setup/operator-guide.md", b"# Operator guide\nStart and resume.\n")
        put(kit, "setup/runtime.md", b"# Runtime\nInspect selected resources.\n")
        put(kit, "setup/export_item.py", (MODULE.parent / "export_item.py").read_bytes())
        put(kit, "setup/verify_archive.py", (MODULE.parent / "verify_archive.py").read_bytes())
        put(kit, "templates/item-export.json", b'{"schema_version":1}\n')
        before = context.inventory(kit)
        out = base / "views"
        report = context.build(kit, out)
        assert len(report["methods"]) == 25
        assert before == context.inventory(kit), "generator changed the kit"
        assert (out / context.GUIDE).read_bytes() == guide
        assert (out / context.BODY).read_bytes() == body
        assert (out / context.REGISTER).read_bytes() == register
        combined = b"".join(p.read_bytes() for p in out.iterdir() if p.suffix != ".zip")
        assert b"HIDDEN_FIXTURE" not in combined
        assert nested in combined and b"Full license statement." in combined
        assert b"Synthetic launch route." in (out / context.INDEX).read_bytes()
        assert b'{"status":"NOT TESTED"}\n' in combined
        rows = {row["path"]: row for row in report["sources"]}
        asset = rows["skills/blitz/assets/runtime.js"]
        assert asset["status"] == "packaged_resource_not_executed" and "view" not in asset
        assert b"throw new Error" not in combined
        with zipfile.ZipFile(out / context.RUNTIME) as runtime:
            assert runtime.read("Blitz/skills/blitz/assets/runtime.js") == b"throw new Error('never execute');\n"
            assert not any("evals/" in path for path in runtime.namelist())
            assert runtime.read("Blitz/skills/blitz/LICENSE") == b"Full license statement.\n"
        assert any(r["reference"] == "missing.md" and r["status"] == "unresolved_or_task_created" for r in report["references"])
        assert any(r.get("source") == "templates/handoff.md" and r["status"] == "readable" for r in report["references"])
        for row in rows.values():
            if "view" in row:
                target = out / row["view"]
                assert target.is_file()
                if row.get("section"):
                    assert ("## " + row["section"] + "\n").encode() in target.read_bytes()
        for row in report["files"]:
            data = (out / row["path"]).read_bytes()
            assert len(data) == row["bytes"] and context.digest(data) == row["sha256"]
        assert json.loads((out / context.CONTEXT_MANIFEST).read_text()) == report
        assert context.build(kit, base / "dry", dry_run=True) == report
        assert not (base / "dry").exists()
        reject(lambda: context.build(kit, out), "occupied")
        reject(lambda: context.build(kit, kit / "generated"), "overlap")
        reject(lambda: context.build(kit, base / ".codex" / "generated"), "live")
        reject(lambda: context.guard_path(str(kit) + "/../kit"), "unsafe")
        reject(lambda: context.guard_path(str(kit) + "/file.md:stream", False), "unsafe")
        reject(lambda: context.guard_path(str(kit) + "/name. ", False), "unsafe")
        reject(lambda: context.guard_path(str(kit) + "/NUL.md", False), "unsafe")
        for reserved in ["COM\u00b9.txt", "LPT\u00b2.txt", "CONIN$.md", "CONOUT$.txt"]:
            reject(lambda: context.guard_path(str(kit) + "/" + reserved, False), "unsafe")
        reject(lambda: context.guard_path(str(kit) + "//repeated", False), "alias")
        # Windows junction attributes can be exercised without symlink privileges.
        original_lstat = Path.lstat
        def reparse_lstat(path):
            if path == skill:
                return SimpleNamespace(st_mode=stat.S_IFREG, st_file_attributes=0x400)
            return original_lstat(path)
        with patch.object(Path, "lstat", reparse_lstat):
            reject(lambda: context.prepare(kit), "reparse")
        put(kit, "skills/blitz/answer.md", b"ordinary file")
        alias = kit / "skills/blitz/alias.md"
        try:
            os.link(kit / "skills/blitz/answer.md", alias)
        except OSError as exc:
            raise AssertionError("hardlink guard not exercised: " + str(exc))
        reject(lambda: context.prepare(kit), "hardlink")
        alias.unlink()
        put(kit, "setup/Blitz_Project_Instructions.md", b"x" * 8001)
        reject(lambda: context.prepare(kit), "8000")
        put(kit, "setup/Blitz_Project_Instructions.md", body)
        (kit / "skills/blitz/SKILL.md").unlink()
        reject(lambda: context.prepare(kit), "inventory differs")
    print("PASS: 25-method coverage, exact copies, nested references, licenses, resource limits, excluded fixtures, hashes, determinism, dry run, source immutability, occupied/overlap/live/alias/reparse/hardlink guards and instruction limit.")


if __name__ == "__main__":
    run()
