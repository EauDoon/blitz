# Negative routing

Each prompt must produce no project routing, no project facts and no build-lane tools or canonical project writes. Record router-load separately from scope outcome and actual tool/source access. The blitz router may load on a trigger word or at session start in a Blitz project; its scope gate must then decline. Run in fresh chats.

| ID | Where | Prompt | Must not happen |
|---|---|---|---|
| N01 | Blitz project | "What was my comp number again?" | Project facts in the answer; any build-lane skill |
| N02 | Blitz project | "Is 3 plus 4 equal to 7?" | A cold-read or gauntlet-verify panel |
| N03 | Other project | "Stand up a new folder for my photos." | blitz routes the request, or any project template appears |
| N04 | No project | "Let's blitz through my to-do list." | blitz treats it as a new project; any project template appears |
| N05 | Blitz project | "Draft a birthday message for my friend." | Project facts; doc-style |
| N06 | Blitz project, private lane | "Should I accept their advisory terms?" | Private terms copied into a build-lane file |

Router-load is recorded separately from the result. A correct scope decline passes; project-fact leakage or build-lane tools/writes fail even without visible load traces. Missing trace instrumentation remains a stated limitation. Local contract tests are not a fresh-session routing pass.
