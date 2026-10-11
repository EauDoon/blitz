# Recovery runbook

Use it after a failed write, a stale input, a lost session or a tool change. Work in this order.

1. Confirm the project, the governing file 03 version and the canonical locations (file 00).
2. Read the last checkpoint and handoff when available. If absent, use sufficient accessible authoritative source and resulting-state evidence under [Operating Loop](../skills/blitz/references/operating-loop.md). Do not fabricate missing history; hold only work whose necessary basis remains unavailable.
3. Check every uncertain external write before any retry. A timeout does not prove a failure; a retry can duplicate a file, a message or a payment.
4. Reconcile newer sources. Mark only the affected artifacts stale.
5. Restore tools, or pick the fallback the capability manifest names.
6. Resume the top ready task.
7. Record consequential recovery state or explicitly required evidence: cause, observed time lost, fix and necessary next action. Do not add a rule or log solely to document an uneventful continuation. For the commissioned Delivering drill, retain the required recovery receipt and measured time from failure to resumed work.
