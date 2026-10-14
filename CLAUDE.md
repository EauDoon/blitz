@AGENTS.md

## Claude Code

`.claude/skills/` exposes the 25 Blitz methods as project skills. Each entry repeats its method's frontmatter and points to `Blitz/skills/<name>/SKILL.md`, which stays the only copy of the method. Edit methods in `Blitz/skills/`, not in `.claude/skills/`. After a method name, description or the method list changes, run `python -B tools/sync_claude_skills.py write`; the repository tests run the check.
