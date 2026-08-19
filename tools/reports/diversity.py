# SPDX-License-Identifier: Apache-2.0
"""Construction-diversity report (GR-12 gate).

Measures whether scenarios differ in structure rather than only in story.
Reports observations; it does not manufacture a statistical claim. A
structural signature repeated across scenarios is a finding, because the
canonical scenario is a schema contract and not a template."""
import collections
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _signature(sid: str) -> dict:
    fx = [yaml.safe_load(f.read_text())
          for f in sorted((ROOT / "kyc-aml" / "fixtures").rglob("*.yaml"))]
    fx = [d for d in fx if d.get("scenario_ref") == sid]
    ak = yaml.safe_load((ROOT / "kyc-aml" / "answers" / f"{sid}.yaml").read_text())
    sc = yaml.safe_load((ROOT / "kyc-aml" / "scenarios" / f"{sid}.yaml").read_text())
    types = collections.Counter(d["fixture_type"] for d in fx)
    statuses = collections.Counter(c["status"] for c in ak["claims"])
    etypes = collections.Counter(e["evidence_type"] for c in ak["claims"]
                                 for e in c.get("evidence", []))
    return {
        "tier": sc["difficulty_tier"],
        "has_prior_case": any("prior" in p.get("text", "").lower()
                              for d in fx for p in d.get("passages", [])),
        "has_watchlist": bool(types.get("watchlist")),
        "temporal_phases": len({d.get("record", {}).get("note_date")
                                for d in fx if d["fixture_type"] == "case_note"}),
        "disposition_shape": ak["evaluation_target"]["disposition_expected"].split(":")[0].strip(),
        "has_transactions": bool(types.get("transaction_set")),
        "has_ownership_model": "ownership" in ak,
        "document_count": types.get("document", 0),
        "case_note_count": types.get("case_note", 0),
        "fixture_types": "".join(sorted(t[0] for t in types)),
        "claim_count": len(ak["claims"]),
        "status_profile": "/".join(f"{k}{v}" for k, v in sorted(statuses.items())),
        "evidence_type_variety": len(etypes),
        "derived_claims": sum(1 for c in ak["claims"]
                              for e in c.get("evidence", [])
                              if e["evidence_type"] == "derived"),
    }


def run() -> dict:
    sids = [p.stem for p in sorted((ROOT / "kyc-aml" / "scenarios").glob("*.yaml"))]
    sigs = {s: _signature(s) for s in sids}
    findings = []
    # Coarse topology (which fixture directories are populated) is expected to
    # repeat: most KYC scenarios have a customer, an alert and documents. What
    # GR-12 forbids is a repeated CONSTRUCTION PROFILE, which combines topology
    # with evidence shape, temporal structure and claim composition. Only the
    # richer signature is treated as a finding.
    def bucket(n, edges=(0, 1, 3)):
        return sum(1 for e in edges if n > e)

    profile = collections.Counter(
        (v["fixture_types"], v["has_transactions"], v["has_ownership_model"],
         v["has_prior_case"], v["has_watchlist"], bucket(v["document_count"]),
         bucket(v["case_note_count"]), v["temporal_phases"],
         v["derived_claims"] > 0, v["evidence_type_variety"],
         v["status_profile"])
        for v in sigs.values())
    for key, n in profile.items():
        if n > 1:
            findings.append(f"construction profile repeated in {n} scenarios: {key}")
    coarse = collections.Counter(v["fixture_types"] for v in sigs.values())
    top_c, n_c = coarse.most_common(1)[0]
    observations = [f"coarse topology {top_c!r} appears in {n_c} of {len(sids)} "
                    "scenarios, which is expected and not a finding"]
    for field in ("disposition_shape", "status_profile", "tier"):
        c = collections.Counter(v[field] for v in sigs.values())
        top, n = c.most_common(1)[0]
        if n > max(2, len(sids) // 2):
            findings.append(f"{field}={top!r} dominates ({n} of {len(sids)})")
    report = {"observations": observations, "synthetic": {"marker": "REGEVAL_SYNTHETIC", "corpus_version": "0.1.0-dev"},
              "scenarios": len(sids),
              "verdict": "PASS" if not findings else "REVIEW",
              "findings": findings or ["no repeated structural signature"],
              "signatures": sigs,
              "note": ("Observational. Structural variation is reported, not "
                       "proven; at this corpus size only repetition is detectable.")}
    (ROOT / "kyc-aml" / "coverage" / "diversity_report.yaml").write_text(
        yaml.safe_dump(report, sort_keys=True, width=88), newline="\n")
    return report


if __name__ == "__main__":
    r = run()
    print(f"diversity: {r['verdict']} across {r['scenarios']} scenarios")
    for f in r["findings"]:
        print("  -", f)
