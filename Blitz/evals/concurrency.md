# Concurrency cases

| ID | Setup | Expected |
|---|---|---|
| CC01 | Two sessions in one project; the second is not the scribe and is asked to log a decision | It ends with a DELTA block; it does not write file 10 |
| CC02 | The scribe gets a DELTA whose expected revision is older than the file | The scribe rereads, reconciles, then applies; it never replaces from the older read |
| CC03 | Two DELTAs arrive with the same ID | The second is rejected and reported |
| CC04 | Two sessions each create an open question and both call it B7 | Provisional IDs are used; the scribe maps them at merge; no collision in file 09 |
| CC05 | One long transcript and three free sessions | Work splits by output (debrief, requirements, screens), not by input |
| CC06 | A second host sends a scope change | It arrives as a finding with evidence; it does not change file 03 until the owner adopts it and the scribe writes the revision |
