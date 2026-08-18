# SPDX-License-Identifier: Apache-2.0
"""Screening: fixture names trace to the generator registry and morphology."""
import pathlib, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import screening

class TestScreening(unittest.TestCase):
    def test_all_names_screened_clean(self):
        r = screening.screen()
        self.assertGreater(r["names_checked"], 0)
        self.assertEqual(r["findings"], [])

    def test_detects_unregistered_name(self):
        fx = ROOT / "kyc-aml" / "fixtures" / "customers" / "CUST-0000.yaml"
        original = fx.read_text()
        try:
            fx.write_text(original.replace("full_name:", "full_name: John Smith #"))
            self.assertGreater(len(screening.screen()["findings"]), 0)
        finally:
            fx.write_text(original)

if __name__ == "__main__":
    unittest.main()
