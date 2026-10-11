#!/usr/bin/env python3
"""Run the release checks with durable results and a truthful process exit."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

SUITES = {
    'repairs': ['evals/test_oai_repairs.py'],
    'lean': ['evals/test_oai_lean.py'],
    'operating-loop': ['evals/test_operating_loop.py'],
    'context-acquisition': ['evals/test_context_acquisition.py'],
    'item-export': ['evals/test_item_export.py'],
    'thor-context': ['evals/test_thor_context.py'],
    'integrity': ['evals/test_v2_integrity.py'],
    'runtime': ['evals/test_v2_runtime.py'],
    'runner': ['evals/test_release_runner.py'],
    'company': ['evals/test_company.py'],
    'scoped-csv': ['evals/test_scope_csv.py'],
    'kit': ['setup/verify_kit.py'],
}


def run_checks(checks, kit, out, timeout=180):
    if not checks:
        raise ValueError('No checks selected')
    out = Path(out).absolute()
    kit = Path(kit).absolute()
    if out == kit or kit in out.parents:
        raise ValueError('Evidence directory must be outside the candidate')
    out.mkdir(parents=True, exist_ok=False)
    temp = out / 'temp'
    temp.mkdir()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', TEMP=str(temp), TMP=str(temp))
    rows = []
    for name, args in checks:
        command = [sys.executable, '-B', *args]
        try:
            process = subprocess.run(command, cwd=kit, env=env, capture_output=True,
                                     text=True, encoding='utf-8', errors='replace', timeout=timeout)
            output = process.stdout + process.stderr
            row = {'name': name, 'command': command, 'cwd': str(kit), 'exit': process.returncode,
                   'result': 'pass' if process.returncode == 0 else 'fail'}
        except subprocess.TimeoutExpired as exc:
            def decode(value):
                return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value or ''
            output = decode(exc.stdout) + decode(exc.stderr) + '\nTIMEOUT\n'
            row = {'name': name, 'command': command, 'cwd': str(kit), 'exit': None, 'result': 'timeout'}
        except OSError as exc:
            output = str(exc)
            row = {'name': name, 'command': command, 'cwd': str(kit), 'exit': None, 'result': 'error'}
        row.update(output=name+'.txt', python=sys.version)
        (out / row['output']).write_text(output, encoding='utf-8')
        rows.append(row)
        result = {'result': 'pass' if all(r['result']=='pass' for r in rows) else 'fail',
                  'complete': len(rows)==len(checks), 'checks': rows}
        (out/'results.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print(name, row['result'], 'exit', row['exit'], flush=True)
    return 0 if all(r['result']=='pass' for r in rows) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kit', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--suite', action='append', choices=sorted(SUITES))
    parser.add_argument('--timeout', type=float, default=180)
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error('timeout must be positive')
    names = list(dict.fromkeys(args.suite or SUITES))
    try:
        return run_checks([(n, SUITES[n]) for n in names], args.kit, args.out, args.timeout)
    except (OSError, ValueError) as exc:
        print('release checks failed: '+str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
