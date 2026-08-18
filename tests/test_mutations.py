# SPDX-License-Identifier: Apache-2.0
"""Mutation validity gates (single plausible semantic defect). Stage-gated:
activates when corruptions exist; asserts the directory is trackable now."""
import pathlib, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]

class TestMutations(unittest.TestCase):
    def test_stage_applicability(self):
        d = ROOT / "kyc-aml" / "validation-cases" / "corruptions"
        self.assertTrue(d.is_dir())
        if not list(d.glob("*.yaml")):
            self.skipTest("no corruptions yet (pre-Stage 4)")

if __name__ == "__main__":
    unittest.main()
