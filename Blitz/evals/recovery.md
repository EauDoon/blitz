# Recovery cases

Run one of these as the Delivering drill. Record the time from failure to resumed work.

| ID | Failure | Expected |
|---|---|---|
| RC01 | A Drive upload times out | The session checks whether the file exists before any retry; no duplicate file |
| RC02 | The session ends mid-task | A new session reads the last checkpoint and handoff, then resumes the top ready task |
| RC03 | A source used by three outputs is replaced by a newer version | Only the three affected outputs are marked stale and listed in the change-impact register |
| RC04 | A tool the manifest listed stops working | The session uses the fallback the capability manifest names and says so |
| RC05 | A zip build fails halfway | The last good release is still in place; the build ran into a temporary sibling |
| RC06 | The project instructions were saved cut off | The read back catches it; the text is shortened and pasted again; a rule near the end is tested |
