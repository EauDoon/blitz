@AGENTS.md

## Claude Code

`.claude/skills/` exposes the Blitz methods named in `tools/claude_skills.json` as project skills. Each entry repeats its method's frontmatter and points to `Blitz/skills/<name>/SKILL.md`, which stays the only copy of the method. Edit methods in `Blitz/skills/`, not in `.claude/skills/`. After that list, a method name or a description changes, run `python -B tools/sync_claude_skills.py write` and delete any entry folder that the check reports as unexpected; the repository tests run the check.
