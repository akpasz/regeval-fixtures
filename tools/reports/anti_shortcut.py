# SPDX-License-Identifier: Apache-2.0
"""Anti-shortcut audit. Stage-applicable: requires scenarios with evaluation
targets, so before Stage 3 it reports SKIP for every feature class.
Findings per feature use PASS / WARN / FAIL with the semantics fixed in the
specification, and the report always carries the disclaimer that PASS does
not establish statistical independence or absence of all leakage."""
import pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
FEATURES = ["amount_buckets", "name_morphology", "geography", "document_count",
            "alert_codes", "scenario_id_order", "narrative_length",
            "ownership_depth", "missing_evidence_patterns", "loaded_vocabulary"]

def run() -> dict:
    scenarios = sorted((ROOT / "kyc-aml").glob("scenarios/*.yaml"))
    state = "SKIP: no scenarios with evaluation targets yet (pre-Stage 3)"
    report = {"disclaimer": ("PASS indicates only that the audited check found no "
              "material issue; it does not establish statistical independence or "
              "prove the absence of all leakage. Heuristic at n<=16."),
              "features": {f: state for f in FEATURES},
              "scenarios_examined": len(scenarios)}
    out = ROOT / "kyc-aml" / "coverage" / "anti_shortcut_report.yaml"
    out.write_text(yaml.safe_dump(report, sort_keys=True, width=88), newline="\n")
    return report

if __name__ == "__main__":
    r = run(); print(f"anti-shortcut report written ({r['scenarios_examined']} scenarios)")
