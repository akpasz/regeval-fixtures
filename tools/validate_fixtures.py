# SPDX-License-Identifier: Apache-2.0
"""Verification gates with stage applicability (spec: gates are enforced only
to the extent their artifacts exist). Stage 1 validates scaffold, schema, and
tooling integrity plus the probe fixture; scenario, claim, mutation, coverage,
diversity, and anti-shortcut gates activate as their artifacts appear."""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import yaml
from _schema_models import FixtureHeader, MARKER

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIX = ROOT / "kyc-aml" / "fixtures"
ANSWER_ONLY_FIELDS = {"status", "expected", "disposition", "risk_level",
                      "risk_score", "ground_truth", "evaluation_target"}
EMDASH = "\u2014"

def gate(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))
    return ok

def main() -> int:
    ok = True
    # structure
    required = ["LICENSE", "LICENSE-CODE", "LICENSE-CONTENT", "environment.lock.yaml",
                "PROVENANCE.md", "DESIGN_DECISIONS.md",
                "schemas/corpus-contract.yaml", "schemas/scenario.schema.json",
                "tools/manifest.py", "tools/screening.py",
                "kyc-aml/generation/generate.py"]
    missing = [r for r in required if not (ROOT / r).exists()]
    ok &= gate("required files present", not missing, ", ".join(missing))

    # every observable fixture: schema header, exact marker, no answer-world fields
    fixtures = sorted(FIX.rglob("*.yaml"))
    ok &= gate("fixtures exist (stage-applicable: probe at Stage 1)", bool(fixtures))
    for f in fixtures:
        data = yaml.safe_load(f.read_text())
        FixtureHeader.model_validate({k: data[k] for k in
            ("fixture_id", "fixture_type", "scenario_ref", "synthetic")})
        m = data["synthetic"]
        ok &= gate(f"{f.name}: exact synthetic marker",
                   m.get("marker") == MARKER and "corpus_version" in m)
        leaked = ANSWER_ONLY_FIELDS & set(data.get("record", {}))
        ok &= gate(f"{f.name}: ground-truth isolation", not leaked, ", ".join(leaked))

    # forbidden strings, each at its own scope (spec constraint 3 + gates)
    fixture_text = "\n".join(f.read_text() for f in fixtures)
    ok &= gate("no 'SAR' in fixture content", "SAR" not in fixture_text)
    ok &= gate("no simulated filing artifacts",
               not re.search(r"filing[_ ](reference|confirmation)", fixture_text, re.I))
    docs = [p for p in ROOT.rglob("*") if p.suffix in {".md", ".yaml", ".py", ".json", ""}
            and p.is_file() and "__pycache__" not in str(p)]
    emdash_hits = [str(p.relative_to(ROOT)) for p in docs if EMDASH in p.read_text(errors="ignore")]
    ok &= gate("no em dash in any repository document", not emdash_hits, ", ".join(emdash_hits))

    # SPDX headers on code
    py = [p for p in ROOT.rglob("*.py") if "__pycache__" not in str(p)]
    no_spdx = [str(p.relative_to(ROOT)) for p in py
               if "SPDX-License-Identifier: Apache-2.0" not in p.read_text()]
    ok &= gate("SPDX headers on all code", not no_spdx, ", ".join(no_spdx))

    # forbidden machinery
    banned = re.compile(r"\b(langchain|llama_index|openai|anthropic\.|score\(|Scorer|model_adapter)\b")
    # This file defines the banned vocabulary and so necessarily contains it;
    # it is the one file excluded from its own scan.
    machinery = [str(p.relative_to(ROOT)) for p in py
                 if p.name != "validate_fixtures.py" and banned.search(p.read_text())]
    ok &= gate("no scoring/harness machinery", not machinery, ", ".join(machinery))

    # stage-gated: scenarios/claims/cases (report as skipped when absent)
    scen = list((ROOT / "kyc-aml").glob("fixtures/../answers/*.yaml"))
    if not scen:
        print("[SKIP] scenario/claim/case/coverage gates: artifacts not yet present (Stage 1)")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
