"""Regression: failing, missing and timed-out suites must never look green."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('release_runner', Path(__file__).with_name('run_all.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class RunnerChecks(unittest.TestCase):
    def test_failure_continues_and_returns_failure(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw); kit=root/'kit'; kit.mkdir(); out=root/'results'
            code=runner.run_checks([('bad',['-c','raise SystemExit(7)']),('good',['-c','print("done")'])],kit,out)
            receipt=json.loads((out/'results.json').read_text())
            self.assertEqual(code,1)
            self.assertTrue(receipt['complete'])
            self.assertEqual([r['exit'] for r in receipt['checks']],[7,0])
            self.assertEqual(receipt['result'],'fail')

    def test_timeout_has_receipt(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw); kit=root/'kit'; kit.mkdir(); out=root/'results'
            code=runner.run_checks([('slow',['-c','import time; time.sleep(2)'])],kit,out,timeout=.05)
            self.assertEqual(code,1)
            self.assertEqual(json.loads((out/'results.json').read_text())['checks'][0]['result'],'timeout')

    def test_missing_suite_file_fails(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw); kit=root/'kit'; kit.mkdir()
            self.assertEqual(runner.run_checks([('absent',['absent.py'])],kit,root/'results'),1)

    def test_unknown_selection_and_existing_output(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw); sentinel=root/'keep'; sentinel.write_text('unchanged')
            process=subprocess.run([sys.executable,'-B',str(Path(runner.__file__)),'--out',str(root),'--suite','typo'],capture_output=True)
            self.assertNotEqual(process.returncode,0)
            with self.assertRaises((FileExistsError, ValueError)):
                runner.run_checks([('good',['-c','pass'])],root.parent,root)
            self.assertEqual(sentinel.read_text(),'unchanged')

    def test_pass_and_empty_selection(self):
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw); kit=root/'kit'; kit.mkdir()
            self.assertEqual(runner.run_checks([('good',['-c','pass'])],kit,root/'results'),0)
            with self.assertRaises(ValueError): runner.run_checks([],kit,root/'empty')


if __name__=='__main__': unittest.main()
