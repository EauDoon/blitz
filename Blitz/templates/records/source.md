# Source record

One record per input. Source quality and claim status are separate fields. For each factual claim, identify this actual evidence source and the readable passage supporting that claim, with scope and as-of time. Keep task briefing/context sources separate from claim evidence. An extraction or assistant summary is not the original evidence; preserve the original source identity in the claim record. Missing or unreadable evidence leaves the affected claim UNVERIFIED.

Source fidelity: use the actual evidence source, and only the current task/scenario sources for their stated subjects. If a source does not specify its subject, retain that uncertainty; never fill it from another batched scenario, prior output or memory. Name source IDs without assigning an unsupported subject.

| Field | Content |
|---|---|
| Source ID | S[n] |
| Title | |
| Location | Drive ID, project file, link or attachment name |
| Author or speaker | |
| Event time and precision | DD-MM-YYYY h:mm AM/PM, or "date only", or "not stated" |
| Received time | DD-MM-YYYY h:mm AM/PM SGT |
| Version or revision | |
| Audience | Who it was made for |
| Readable sections | |
| Extraction gaps | For example "page 9 absent", "audio minute 12 to 14 unclear" |
| Quality | Primary, secondary, third-party report, synthetic, private |
| Claims extracted | Claim IDs |
