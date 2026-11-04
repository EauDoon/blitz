#!/usr/bin/env python3
"""Prepare corrected scoring outside the immutable v1 corpus; no model calls."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def prepare(out):
    here = Path(__file__).resolve().parent
    base = here.parent / "customer-discovery"
    patch = json.loads((here / "corrections.json").read_text(encoding="utf-8"))
    inventory = base / "SHA256SUMS"
    if hashlib.sha256(inventory.read_bytes()).hexdigest() != patch["base_inventory_sha256"]:
        raise ValueError("frozen inventory differs")
    freeze = base / "FREEZE.json"
    if hashlib.sha256(freeze.read_bytes()).hexdigest() != patch["base_freeze_sha256"]:
        raise ValueError("frozen metadata differs")
    verified = {"SHA256SUMS", "FREEZE.json"}
    for line in inventory.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        verified.add(name)
        path = base / name
        if path.is_symlink() or not path.resolve().is_relative_to(base.resolve()):
            raise ValueError("unsafe frozen payload path")
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError("frozen payload differs: " + name)
    expected_dirs = {str(parent) for name in verified for parent in Path(name).parents if str(parent) != "."}
    for entry in base.rglob("*"):
        name = entry.relative_to(base).as_posix()
        if entry.is_symlink() or (entry.is_file() and name not in verified) or (entry.is_dir() and name not in expected_dirs):
            raise ValueError("unlisted or symlink source entry: " + name)
    out = Path(out).absolute()
    if out.exists() or out.is_symlink() or not out.parent.is_dir():
        raise ValueError("output must be new with an existing parent")
    repo = here.parents[2]
    if any(out.resolve().is_relative_to(source.resolve()) for source in (base, here, repo / "Blitz")):
        raise ValueError("output must stay outside the source kit and evaluator sources")
    out.mkdir()
    for name in sorted(verified):
        destination = out / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(base / name, destination)
    refs_path = out / "evaluator/references.jsonl"
    refs = [json.loads(line) for line in refs_path.read_text(encoding="utf-8").splitlines()]
    scorer_path = out / "evaluator/scorers.json"
    scorer = json.loads(scorer_path.read_text(encoding="utf-8"))
    for change in patch["corrections"]:
        ref = next(row for row in refs if row["case_id"] == change["case_id"])
        ref["version"] = patch["version"]
        ref["provenance"]["scoring_correction"] = change["reason"]
        anchor = next(row for row in ref["expected"]["criteria"] if row["anchor_id"] == change["anchor_id"])
        anchor["requirement"] = change["requirement"]
        ref["expected"]["valid_alternatives"].append(change["valid_alternative"])
        for numeric in change.get("numeric_alternatives", []):
            key = numeric["key"]
            ref["expected"].setdefault("accepted_numeric_values", {})[key] = numeric["accepted_values"]
            criterion = next(row for row in scorer["criteria"] if row["criterion_id"] == change["case_id"] + "-" + key)
            criterion.update(operator="one_of", expected_key="/accepted_numeric_values/" + key)
    refs_path.write_text("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in refs) + "\n", encoding="utf-8", newline="\n")
    scorer["version"] = patch["version"]
    scorer_path.write_text(json.dumps(scorer, indent=2) + "\n", encoding="utf-8", newline="\n")
    contract_path = out / "contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    contract["version"] = patch["version"]
    contract["reference_revision"] = patch
    contract_path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8", newline="\n")
    # Retain parent freeze evidence under explicit lineage names, never as a
    # false identity for the corrected evaluator.
    (out / "FREEZE.json").rename(out / "PARENT_FREEZE_V1.json")
    (out / "SHA256SUMS").rename(out / "PARENT_SHA256SUMS_V1")
    receipt = {"version": patch["version"], "parent_inventory_sha256": patch["base_inventory_sha256"],
               "unchanged_cases_sha256": hashlib.sha256((out / "cases.jsonl").read_bytes()).hexdigest(),
               "corrections": patch["corrections"],
               "files": {p.relative_to(out).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(out.rglob("*")) if p.is_file()}}
    (out / "EVALUATOR_REVISION.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {"result": "prepared", "version": patch["version"], "cases_unchanged": True, "corrections": len(patch["corrections"])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.out)))
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + "\n")
