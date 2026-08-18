# SPDX-License-Identifier: Apache-2.0
"""Reproducibility proof: two independent generation runs into separate
directories must be byte-identical, and CI of this repository shows the
hashes from both runs rather than a bare claim."""
import hashlib, pathlib, shutil, subprocess, sys, tempfile, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]

def run_into(dst: pathlib.Path) -> dict:
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("__pycache__", ".git"))
    subprocess.run([sys.executable, str(dst / "kyc-aml/generation/generate.py")],
                   check=True, capture_output=True)
    out = {}
    for f in sorted((dst / "kyc-aml").rglob("*.yaml")):
        if f.name == "manifest.yaml": continue
        out[str(f.relative_to(dst))] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out

class TestDeterminism(unittest.TestCase):
    def test_two_runs_byte_identical(self):
        with tempfile.TemporaryDirectory() as td:
            a = run_into(pathlib.Path(td) / "run_a")
            b = run_into(pathlib.Path(td) / "run_b")
            self.assertEqual(a, b)
            for path, digest in sorted(a.items()):
                print(f"  {digest[:16]}  {path}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
