# SPDX-License-Identifier: Apache-2.0
"""Anti-shortcut audit runs and carries the mandated disclaimer."""
import pathlib, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "reports"))
import anti_shortcut

class TestShortcuts(unittest.TestCase):
    def test_report_disclaimer(self):
        r = anti_shortcut.run()
        self.assertIn("does not establish statistical independence", r["disclaimer"])

if __name__ == "__main__":
    unittest.main()
