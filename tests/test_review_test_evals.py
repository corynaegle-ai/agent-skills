"""Validate review-tests evaluation inputs and run their original baselines.

The fixtures deliberately contain poor tests and a product defect. Passing
their baselines establishes that the exercises run, not that the skill works.
"""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


EVALS = Path(__file__).resolve().parents[1] / "skills/engineering/review-tests/evals"


class ReviewTestsEvalTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((EVALS / "evals.json").read_text())

    def test_manifest_supplies_complete_isolated_projects(self):
        self.assertEqual(self.manifest["skill_name"], "review-tests")
        cases = self.manifest["evals"]
        self.assertTrue(cases)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        for case in cases:
            with self.subTest(case=case["name"]):
                self.assertTrue(case["prompt"].strip())
                self.assertTrue(case["expectations"])
                paths = [EVALS / name for name in case["files"]]
                self.assertTrue(paths)
                self.assertEqual(len(set(paths)), len(paths))
                for path in paths:
                    self.assertTrue(path.is_file(), str(path))
                    self.assertIn(EVALS.resolve(), path.resolve().parents)
                project = paths[0].parent
                self.assertTrue(all(path.parent == project for path in paths))
                self.assertEqual(set(paths), {
                    path for path in project.iterdir() if path.is_file()
                })
                self.assertIn(project / "CONTRACT.md", paths)
                self.assertIn(project / "suite.py", paths)

    def test_fixture_baselines_run_from_disposable_copies(self):
        runner = """
import json
import unittest
suite = unittest.defaultTestLoader.loadTestsFromName('suite')
result = unittest.TextTestRunner(verbosity=0).run(suite)
print(json.dumps({'tests': result.testsRun, 'skipped': len(result.skipped),
                  'successful': result.wasSuccessful()}))
"""
        for case in self.manifest["evals"]:
            with self.subTest(case=case["name"]), tempfile.TemporaryDirectory(
                prefix="review-tests-eval-"
            ) as directory:
                originals = {}
                for name in case["files"]:
                    source = EVALS / name
                    originals[source] = source.read_bytes()
                    shutil.copyfile(source, Path(directory) / source.name)
                result = subprocess.run(
                    [sys.executable, "-B", "-c", runner], cwd=directory,
                    capture_output=True, text=True, timeout=15,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                outcome = json.loads(result.stdout)
                self.assertTrue(outcome.pop("successful"), result.stderr)
                self.assertEqual(outcome, case["baseline"])
                self.assertGreater(outcome["tests"], outcome["skipped"])
                for source, content in originals.items():
                    self.assertEqual(source.read_bytes(), content)
                    self.assertEqual((Path(directory) / source.name).read_bytes(), content)


if __name__ == "__main__":
    unittest.main()
