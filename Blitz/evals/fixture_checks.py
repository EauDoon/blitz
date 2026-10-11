#!/usr/bin/env python3
"""Synthetic evaluation helpers only; not a live policy or connector engine."""
import math


def validate_estimates(case):
    errors = []
    kind = case.get("kind")
    rows = case.get("rows", [])
    if not isinstance(rows, list) or not rows:
        return ["missing_rows"]
    if kind == "ranking":
        if not all(case.get(k) for k in ["criteria", "evidence", "uncertainty", "sensitivity"]):
            errors.append("ranking_missing_method_or_evidence")
        if any("percent" in row for row in rows):
            errors.append("ranking_invented_probability")
        return errors
    if kind not in {"independent", "distribution"}:
        return ["unknown_estimate_kind"]
    total = 0
    valid = True
    for row in rows:
        p = row.get("percent")
        if isinstance(p, bool) or not isinstance(p, (int, float)) or not math.isfinite(p) or not 0 <= p <= 100:
            errors.append("invalid_percent")
            valid = False
        else:
            total += p
            if abs(p - round(p)) > 1e-10 and row.get("precision_justified") is not True:
                errors.append("unsupported_precision")
        if not all(row.get(k) for k in ["event", "horizon", "basis"]):
            errors.append("missing_event_definition_horizon_or_basis")
    if kind == "distribution":
        if case.get("mutually_exclusive") is not True or case.get("exhaustive") is not True:
            errors.append("distribution_not_declared_exhaustive_and_exclusive")
        if valid and not math.isclose(total, 100, rel_tol=0, abs_tol=1e-8):
            errors.append("sum_not_100")
    return sorted(set(errors))


def delta_action(delta_id, applied_ids, expected_revision, current_revision):
    if delta_id in applied_ids:
        return "reject_duplicate"
    if expected_revision != current_revision:
        return "reread_reconcile"
    return "eligible_for_authorized_scribe"


def write_recovery(result, existing_state):
    if result == "timeout" and existing_state == "unknown":
        return "read_existing_identity_before_retry"
    if result == "timeout" and existing_state == "matches_candidate":
        return "record_existing_success_no_duplicate"
    if result == "timeout" and existing_state == "newer_revision":
        return "reread_reconcile_no_overwrite"
    return "use_recorded_checkpoint_and_authorized_fallback"


def allowlisted_snapshot(sources, allowed_ids):
    return [row for row in sources if row["id"] in allowed_ids and row["scope"] == "build"]


def source_grants_authority(_source_text):
    return False


def installation_receipt_errors(receipt, expected_host, expected_runtime_hash):
    """Check supplied fixture metadata, not an actual account installation."""
    errors = []
    fields = ["host", "installed_name", "version", "observed_at", "save_install_path",
              "runtime_manifest_sha256", "installed_integrity_evidence"]
    if not all(receipt.get(k) for k in fields):
        errors.append("incomplete_receipt")
    if receipt.get("host") != expected_host:
        errors.append("wrong_host")
    if receipt.get("runtime_manifest_sha256") != expected_runtime_hash:
        errors.append("stale_or_mismatched_runtime_hash")
    return errors
