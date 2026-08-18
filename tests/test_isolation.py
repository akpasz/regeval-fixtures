# SPDX-License-Identifier: Apache-2.0
"""Ground-truth isolation: observable fixtures carry no evaluation-world
fields, no answer-key references, and no resolution-state filenames."""
import pathlib, re, unittest, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]
FORBIDDEN_FIELDS = {"status", "expected", "disposition", "risk_level",
                    "risk_score", "ground_truth", "evaluation_target"}

class TestIsolation(unittest.TestCase):
    def fixtures(self):
        return sorted((ROOT / "kyc-aml" / "fixtures").rglob("*.yaml"))

    def test_no_answer_world_fields(self):
        for f in self.fixtures():
            rec = yaml.safe_load(f.read_text()).get("record", {})
            self.assertFalse(FORBIDDEN_FIELDS & set(rec), f.name)

    def test_no_answer_key_references(self):
        for f in self.fixtures():
            self.assertNotIn("answers/", f.read_text(), f.name)

    def test_no_resolution_state_filenames(self):
        for f in self.fixtures():
            self.assertIsNone(re.search(r"final|resolved|closed", f.name), f.name)

if __name__ == "__main__":
    unittest.main()
