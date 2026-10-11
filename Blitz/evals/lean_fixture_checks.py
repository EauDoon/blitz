#!/usr/bin/env python3
"""Synthetic fixture validators; not live routing, entailment or policy engines."""


def source_lineage_errors(claims, sources):
    """Check declared fixture provenance and subject scope, not semantic truth."""
    errors = []
    by_id = {row['id']: row for row in sources}
    for claim in claims:
        source = by_id.get(claim.get('source_id'))
        if source is None:
            errors.append('missing_current_scenario_source')
            continue
        if source.get('kind') == 'briefing' and claim.get('status') == 'VERIFIED':
            errors.append('briefing_not_verification_evidence')
        if claim.get('source_revision') != source.get('revision'):
            errors.append('stale_or_mismatched_source_revision')
        if claim.get('subject') != source.get('subject'):
            errors.append('unsupported_subject')
        if claim.get('status') == 'VERIFIED':
            quote = claim.get('passage')
            if source.get('readable') is not True or not quote or quote not in source.get('text', ''):
                errors.append('unreadable_or_untraced_evidence')
        if not claim.get('as_of'):
            errors.append('missing_as_of')
    return sorted(set(errors))


def delta_disposition(delta, committed, current_revision):
    """Use synthetic supplied state only; never mutate a canonical store."""
    prior = committed.get(delta['id'])
    if prior is not None:
        return 'no_duplicate_revision' if prior == delta['payload'] else 'reject_conflicting_identity'
    if delta['expected_revision'] != current_revision:
        return 'reread_reconcile_before_write'
    return 'eligible_for_authorized_scribe'


def recovery_disposition(checkpoint, writes):
    if not checkpoint or not checkpoint.get('revision') or not checkpoint.get('location'):
        return 'blocked_missing_checkpoint_or_basis'
    if any(row['state'] == 'uncertain' for row in writes):
        return 'inspect_existing_result_before_retry'
    return 'resume_next_authorized_action_without_replaying_completed_writes'
