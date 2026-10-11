"""Static wiring and fixture checks only, not model behavior or native routing."""
from pathlib import Path
import json
import re

KIT = Path(__file__).resolve().parents[1]

def main():
    reference = KIT / 'skills/blitz/references/context-acquisition.md'
    assert reference.is_file()
    assert 'Approval of a number does not reconcile conflicting factual evidence' in reference.read_text(encoding='utf-8')
    callers = ['ENTRYPOINT.md', 'PLAYBOOK.md', 'profiles/lean.md',
               'skills/blitz/SKILL.md', 'skills/doc-style/SKILL.md',
               'skills/blitz/references/operating-loop.md',
               'templates/commission-brief.md', 'templates/acceptance-template.md',
               'templates/project-instructions-chatgpt.md',
               'templates/project-instructions-claude.md']
    for rel in callers:
        text = (KIT/rel).read_text(encoding='utf-8')
        assert 'context-acquisition.md' in text, rel
        for link in re.findall(r'\]\(([^)]+context-acquisition\.md(?:#[^)]*)?)\)', text):
            target = (KIT/rel).parent / link.split('#')[0]
            assert target.resolve() == reference.resolve(), (rel, link)
    for host in ['chatgpt', 'claude']:
        text = (KIT/f'templates/project-instructions-{host}.md').read_text(encoding='utf-8')
        body = re.search(r'```text\n(.*?)\n```', text, re.S).group(1)
        scope = body.split('Scope gate\n', 1)[1].split('\n\n', 1)[0]
        assert 'private-lane request' in scope and 'no project facts' in scope
        assert 'explicit' in scope and 'source' in scope.lower()
        assert len(body) < 8000, (host, len(body))
        # A representative filled body adds longer identities/locations. Actual projects still remeasure.
        filled = re.sub(r'\[[^\]\n]+\]', lambda m: 'Example project ' + ('x' * 40), body)
        assert len(filled) < 8000, ('filled example', host, len(filled))
    manifest = json.loads((KIT/'manifest.json').read_text(encoding='utf-8'))
    assert len(manifest['skills']) == 25
    assert not manifest['revision_changes']['removed']
    cases = json.loads((KIT/'evals/context-acquisition-cases.json').read_text(encoding='utf-8'))['cases']
    keys = json.loads((KIT/'evals/context-acquisition/answer-key/expected-results.json').read_text(encoding='utf-8'))['cases']
    assert [c['id'] for c in cases] == [f'CA{i:02}' for i in range(1, 7)]
    assert [c['id'] for c in keys] == [c['id'] for c in cases]
    for case in cases:
        path = KIT/'evals'/case['input']
        assert path.is_file() and case['pass']
    # Independent expected arithmetic for synthetic fixtures, not a production parser.
    assert keys[0]['expected']['first_quarter_usd'] == 12*1250 + 1800 + 12*20*3 + 600
    assert keys[2]['expected']['Aster']['first_quarter_total'] == 1000+300-200+200*3
    assert keys[2]['expected']['Birch']['first_quarter_total'] == 600+400-100+250*3
    assert keys[3]['expected']['count_a']['cost_usd'] == (24-17)*250
    assert keys[3]['expected']['count_b']['cost_usd'] == (24-19)*250
    print('PASS: 10 caller links, template and representative filled sizes, 25 skills, baseline retention, six case definitions and synthetic arithmetic')
    print('LIMIT: structural/fixture checks only; executed model behavior, read boundaries and native routing need separate evidence.')

if __name__ == '__main__':
    main()
