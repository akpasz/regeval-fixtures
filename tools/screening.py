# SPDX-License-Identifier: Apache-2.0
"""Name screening: a risk-reduction mechanism, never a uniqueness guarantee.
What it establishes: every person or company name in observable fixtures was
produced by the generator's invented morphology (verified against the emitted
name registry) and matches the morphology pattern, which is constructed from
syllables chosen to avoid real-name lookalikes.
What it cannot establish: global uniqueness against every real person or
entity. That residual risk is stated in SCREENING.md and LIMITATIONS.md.
Execution metadata goes to the verification report, never into fixtures."""
import pathlib, re, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
MORPH = re.compile(r"^[A-Z][a-z]{4,12}$")
# Generic corporate suffixes and descriptors: explicit synthetic design choice
# (recorded DD-014); these carry no identity and are exempt from morphology.
SUFFIX_TOKENS = {"Ltd", "S.A.", "Trust", "Holdings", "Holding", "Components",
                 "Trading"}

def screen() -> dict:
    reg_path = ROOT / "kyc-aml" / "generation" / "name-registry.yaml"
    registry = set(yaml.safe_load(reg_path.read_text())["names"]) if reg_path.exists() else set()
    findings, checked = [], 0
    NAME_KEYS = {"full_name", "legal_name", "counterparty_name"}
    def walk(obj, fname):
        nonlocal checked
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in NAME_KEYS and isinstance(v, str):
                    checked += 1
                    if v not in registry:
                        findings.append(f"{fname}: '{v}' not in generator name registry")
                    for token in v.split():
                        if token in SUFFIX_TOKENS:
                            continue
                        if not MORPH.match(token):
                            findings.append(f"{fname}: token '{token}' fails morphology")
                else:
                    walk(v, fname)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, fname)
    for f in sorted((ROOT / "kyc-aml" / "fixtures").rglob("*.yaml")):
        walk(yaml.safe_load(f.read_text()), f.name)
    return {"names_checked": checked, "collisions_found": len(findings),
            "findings": findings,
            "residual_risk": "heuristic screening; global uniqueness not established"}

if __name__ == "__main__":
    r = screen()
    print(yaml.safe_dump(r, sort_keys=True, default_flow_style=False))
    sys.exit(1 if r["findings"] else 0)
