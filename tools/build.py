# SPDX-License-Identifier: Apache-2.0
"""Canonical build and verify sequence. One entry point so a derived report
can never describe an earlier state than the corpus it accompanies (DD-023).

    generate -> coverage -> diversity -> anti-shortcut -> manifest -> validate
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
# One owner per derived artifact: generate.py writes source artifacts only,
# each report is produced by its own tool, and this list is the whole pipeline.
STEPS = [
    ("generate", ROOT / "kyc-aml" / "generation" / "generate.py"),
    ("coverage", ROOT / "tools" / "reports" / "coverage.py"),
    ("diversity", ROOT / "tools" / "reports" / "diversity.py"),
    ("anti-shortcut", ROOT / "tools" / "reports" / "anti_shortcut.py"),
    ("manifest", ROOT / "tools" / "manifest.py"),
    ("validate", ROOT / "tools" / "validate_fixtures.py"),
]

if __name__ == "__main__":
    for name, script in STEPS:
        r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
        tail = [l for l in r.stdout.strip().split("\n") if l][-1] if r.stdout.strip() else ""
        print(f"[{name}] {tail}")
        if r.returncode:
            print(r.stdout, r.stderr)
            sys.exit(r.returncode)
    print("build complete")
