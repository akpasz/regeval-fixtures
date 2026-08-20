# SPDX-License-Identifier: Apache-2.0
"""Coverage report: per-dimension scenario counts; warns when a dimension has
fewer than two independent scenarios. Stage-applicable (empty pre-Stage 3)."""
import pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
DIMS = ["citation", "absence", "ownership", "qualifier", "numerical",
        "entity_resolution", "evidence_sufficiency", "claim_decomposition",
        "temporal_update", "negative_control", "disposition"]
def run() -> dict:
    import yaml
    scen = sorted((ROOT / "kyc-aml" / "scenarios").glob("*.yaml"))
    cov = {d: [] for d in DIMS}
    for s in scen:
        d = yaml.safe_load(s.read_text())
        for label in d["coverage_labels"]:
            cov.setdefault(label, []).append(d["scenario_id"])
    warn = [d for d, v in cov.items() if 0 < len(v) < 2]
    empty = [d for d, v in cov.items() if not v]
    out = {"scenarios": len(scen), "dimensions": cov,
           "single_point_of_proof": warn, "uncovered": empty,
           "note": "single-point-of-proof dimensions are a finding, not a pass"}
    (ROOT / "kyc-aml" / "coverage" / "coverage-matrix.yaml").write_text(
        yaml.safe_dump({"synthetic": {"marker": "REGEVAL_SYNTHETIC",
                                       "corpus_version": "0.1.0"}, **out},
                       sort_keys=True, width=88), newline="\n")
    return out


if __name__ == "__main__":
    r = run()
    print(f"scenarios: {r['scenarios']}")
    for d, v in sorted(r["dimensions"].items()):
        flag = " WARN single-point" if 0 < len(v) < 2 else (" UNCOVERED" if not v else "")
        print(f"  {d:22s} {len(v)}{flag}")
