# [PROJECT] 12: Delta Buffer

Create on first need (Blitz kit v1.1). DELTAs from non-scribe sessions wait here until the scribe applies them. The scribe moves each applied DELTA to "Applied" with the time and the file revision it produced.

## Waiting

```text
DELTA [unique ID]
From session: [name]  Written: [DD-MM-YYYY h:mm AM/PM]
Expected revision: [file, revision or last update time]
Target: [file and section]
Change: [exact text to add or replace]
Evidence: [source ID or quote]
Affects: [artifacts to refresh or mark stale]
```

## Applied

| DELTA ID | Applied at | Resulting revision | Notes |
|---|---|---|---|
| | | | |

## Rejected

| DELTA ID | Reason (duplicate ID, stale revision, no evidence) |
|---|---|
| | |
