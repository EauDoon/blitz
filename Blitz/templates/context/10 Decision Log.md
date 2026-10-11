# [PROJECT] 10: Decision Log

Append only. Never rewrite or delete an entry; add a superseding entry instead. One line per event, newest at the top. Day-1 file (Blitz kit v1.1).

Format: DD-MM-YYYY h:mm AM/PM | type | detail | source
Types: meeting, claim, evidence, decision, gate, terms, deadline, revision.

Rules:
* A decision entry names the decision-maker and the scope. A decision is logged only after it is made, never in advance.
* A gate entry records Proceed, Hold or Walk, the reason, and the work that may continue.
* A revision entry names the change, the reason, the decision-maker and the affected outputs, and the file 03 version it creates.
* A claim entry keeps the speaker and the evidence still needed.

## Entries

[DD-MM-YYYY h:mm AM/PM] | gate | Ingestion gate: [Proceed | Hold | Walk]. Reason: [text]. May continue: [work]. Releases it: [named evidence]. Decision owner: [name]. | [source]
