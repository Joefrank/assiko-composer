import os
import sys
import importlib
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class ScoreImportTests(unittest.TestCase):
    def test_score_modules_import_without_circular_error(self):
        for module_name in ["Model.Score.Staff", "Model.Score.ScoreControl", "Model.Score.GrandStaff"]:
            module = importlib.import_module(module_name)
            self.assertIsNotNone(module)


if __name__ == "__main__":
    unittest.main()
