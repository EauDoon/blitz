"""Static module integration checks, not model execution or routing evidence."""
from pathlib import Path
import json

KIT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((KIT / 'manifest.json').read_text(encoding='utf-8'))
    module = manifest['modules']['operating-loop']
    assert module['entry'] == 'skills/blitz/references/operating-loop.md'
    assert module['optional'] is True
    assert len(manifest['skills']) == 25
    assert not (KIT / 'skills/operating-loop').exists(), 'Module must not become a separate skill'
    assert not manifest['revision_changes']['removed'], 'Keep all baseline files'
    text = (KIT / module['entry']).read_text(encoding='utf-8')
    for phrase in ['A stale row alone', 'mandated release/pilot evidence',
                   'A canceled send remains canceled', 'Before retrying an interrupted write',
                   'accepted owner requires explicit acceptance', 'unsaved proposed change']:
        assert phrase in text, phrase
    callers = ['ENTRYPOINT.md', 'PLAYBOOK.md', 'README.md', 'profiles/lean.md',
               'profiles/comprehensive.md', 'skills/blitz/SKILL.md',
               'templates/project-instructions-chatgpt.md', 'templates/project-instructions-claude.md',
               'templates/capture-protocol.md', 'templates/checkpoint.md',
               'templates/recovery-runbook.md', 'templates/daily-record.md',
               'skills/meeting-to-action/SKILL.md']
    for rel in callers:
        assert 'operating-loop.md' in (KIT / rel).read_text(encoding='utf-8'), rel
    router = (KIT / 'skills/blitz/SKILL.md').read_text(encoding='utf-8')
    assert 'Every other session ends with DELTA blocks' not in router
    assert '**Write the stage line.**' not in router
    assert 'no change needs no DELTA' in router
    cases = json.loads((KIT / 'evals/operating-loop-cases.json').read_text(encoding='utf-8'))['cases']
    assert [row['id'] for row in cases] == [f'OL{i:02}' for i in range(1, 15)]
    assert all(row['case'] and row['pass'] for row in cases)
    print('PASS: module identity, 25-skill boundary, baseline retention, safeguards, 13 callers, no-op router, 14 case definitions')
    print('LIMIT: static contracts only; actual model scenarios and native routing require separate evidence.')


if __name__ == '__main__':
    main()
