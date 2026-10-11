# Checkpoint

Write when consequential state is needed for safe continuation, handoff or recovery, or an applicable pilot/release contract explicitly requires it. Under [Operating Loop](../skills/blitz/references/operating-loop.md), a session ending alone requires no new checkpoint when existing evidence suffices. Preserve current revisions and uncertain-write state when they matter.

| Field | Content |
|---|---|
| Time | DD-MM-YYYY h:mm AM/PM SGT |
| Completed work | Output IDs and their states |
| Current revisions | File 03 version; last file 10 entry; canonical document revisions |
| Open defects | |
| External writes in flight | Any write whose result is not yet confirmed |
| Next action | One task, with its owner |
