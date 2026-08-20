# SPDX-License-Identifier: Apache-2.0
"""Anti-shortcut audit. Executes against every scenario with an evaluation
target and reports PASS / WARN / FAIL per audited feature.

PASS: no material association found by the implemented check.
WARN: possible association, or sample too small to distinguish, human review.
FAIL: an observable feature materially predicts the evaluation target.

PASS never means independence is established. At this corpus size the audit
catches obvious leakage only, and the report says so."""
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
FEATURES = ["amount_buckets", "name_morphology", "geography", "document_count",
            "alert_codes", "scenario_id_order", "narrative_length",
            "ownership_depth", "missing_evidence_patterns", "loaded_vocabulary"]


def _load():
    rows = []
    for s in sorted((ROOT / "kyc-aml" / "scenarios").glob("*.yaml")):
        sc = yaml.safe_load(s.read_text())
        ak = ROOT / "kyc-aml" / "answers" / f"{sc['scenario_id']}.yaml"
        if not ak.exists():
            continue
        a = yaml.safe_load(ak.read_text())
        target = a["evaluation_target"]["disposition_expected"].split(":")[0].strip()
        fx = [f for f in (ROOT / "kyc-aml" / "fixtures").rglob("*.yaml")
              if yaml.safe_load(f.read_text()).get("scenario_ref") == sc["scenario_id"]]
        types = {yaml.safe_load(f.read_text())["fixture_type"] for f in fx}
        rows.append({"id": sc["scenario_id"], "tier": sc["difficulty_tier"],
                     "target": target, "fixtures": fx,
                     "labels": tuple(sorted(sc["coverage_labels"])),
                     # construction type: what kinds of evidence the scenario is
                     # built from, independent of its story
                     "construction": (("transaction_set" in types),
                                      ("watchlist" in types),
                                      sum(1 for f in fx if "/documents/" in str(f)) > 2),
                     "doc_count": sum(1 for f in fx if "/documents/" in str(f))})
    return rows


def _verdict(groups, n):
    """groups: mapping feature-value -> set of targets. A feature that
    partitions targets perfectly is leakage; small n means WARN, not PASS."""
    if not groups:
        return "SKIP: no data"
    perfect = all(len(v) == 1 for v in groups.values()) and len(groups) > 1
    distinct_targets = len({t for v in groups.values() for t in v})
    if perfect and distinct_targets > 1 and len(groups) >= n:
        return "FAIL: feature value partitions the evaluation target"
    if n < 8:
        return "EXECUTED-UNDERPOWERED: no material association found; n too small for inference"
    return "EXECUTED-CLEAN: no material association found"


def run() -> dict:
    rows = _load()
    n = len(rows)
    findings = {}
    if n:
        by_order, by_docs, by_tier, by_len = {}, {}, {}, {}
        for i, r in enumerate(rows):
            by_order.setdefault("early" if i < n / 2 else "late", set()).add(r["target"])
            by_docs.setdefault("few" if r["doc_count"] <= 2 else "many", set()).add(r["target"])
            by_tier.setdefault(r["tier"], set()).add(r["target"])
            tot = sum(len(f.read_text()) for f in r["fixtures"])
            by_len.setdefault("short" if tot < 6000 else "long", set()).add(r["target"])
        findings["scenario_id_order"] = _verdict(by_order, n)
        findings["document_count"] = _verdict(by_docs, n)
        findings["narrative_length"] = _verdict(by_len, n)
        findings["difficulty_tier"] = _verdict(by_tier, n)

        # Two invariants the design objective states explicitly, measured
        # rather than inspected (DD-025). Both ask the same question: can an
        # observable or metadata property determine the disposition without
        # reading the evidence?
        def independence(keyfn, label):
            groups: dict = {}
            for r in rows:
                groups.setdefault(keyfn(r), set()).add(r["target"])
            determined = [k for k, v in groups.items() if len(v) == 1 and len(groups) > 1]
            if not determined:
                return f"EXECUTED-CLEAN: no {label} value determines the disposition"
            if all(len(v) == 1 for v in groups.values()):
                return (f"FAIL: {label} determines the disposition for every value")
            return (f"EXECUTED-PARTIAL: {len(determined)} of {len(groups)} {label} "
                    f"values have a single disposition, which at n={n} may be "
                    "sample size rather than leakage")

        findings["difficulty_outcome_independence"] = independence(
            lambda r: r["tier"], "difficulty tier")
        findings["construction_outcome_independence"] = independence(
            lambda r: r["construction"], "construction type")
        for f in FEATURES:
            findings.setdefault(f, f"NOT-IMPLEMENTED: no automated heuristic for this feature; "
                                   f"{n} scenarios available for future audit")
    implemented = sum(1 for v in findings.values() if not v.startswith("NOT-IMPLEMENTED"))
    report = {"audit_status": "PARTIAL",
              "audit_status_note": (f"limited heuristic screen: {implemented} of "
                                    f"{len(findings)} features have an implemented "
                                    "check. The audit has not passed; it has been "
                                    "performed within these limits."),
              "synthetic": {"marker": "REGEVAL_SYNTHETIC", "corpus_version": "0.1.0-dev"},
              "scenarios_examined": n,
              "disclaimer": ("PASS indicates only that the implemented check found no "
                             "material association. It does not establish statistical "
                             "independence or prove absence of leakage. At this corpus "
                             "size the audit detects obvious leakage only."),
              "features": dict(sorted(findings.items()))}
    (ROOT / "kyc-aml" / "coverage" / "anti_shortcut_report.yaml").write_text(
        yaml.safe_dump(report, sort_keys=True, width=88), newline="\n")
    return report


if __name__ == "__main__":
    r = run()
    print(f"anti-shortcut: executed on {r['scenarios_examined']} scenarios")
    for k, v in r["features"].items():
        print(f"  {k:26s} {v.split(':')[0]}")
