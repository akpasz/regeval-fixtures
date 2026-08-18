# SPDX-License-Identifier: Apache-2.0
"""Manifest: correct scope, deterministic, and never self-referencing."""
import pathlib, subprocess, sys, unittest, yaml
ROOT = pathlib.Path(__file__).resolve().parents[1]

class TestManifest(unittest.TestCase):
    def setUp(self):
        subprocess.run([sys.executable, str(ROOT / "tools" / "manifest.py")],
                       check=True, capture_output=True)
        self.m = yaml.safe_load(
            (ROOT / "kyc-aml" / "generation" / "manifest.yaml").read_text())

    def test_no_self_reference(self):
        self.assertFalse(any("manifest.yaml" in e["path"] for e in self.m["files"]))

    def test_scope_includes_contract_and_lock(self):
        paths = {e["path"] for e in self.m["files"]}
        self.assertIn("schemas/corpus-contract.yaml", paths)
        self.assertIn("environment.lock.yaml", paths)

    def test_deterministic_reemission(self):
        first = (ROOT / "kyc-aml" / "generation" / "manifest.yaml").read_bytes()
        subprocess.run([sys.executable, str(ROOT / "tools" / "manifest.py")],
                       check=True, capture_output=True)
        second = (ROOT / "kyc-aml" / "generation" / "manifest.yaml").read_bytes()
        self.assertEqual(first, second)

if __name__ == "__main__":
    unittest.main()
