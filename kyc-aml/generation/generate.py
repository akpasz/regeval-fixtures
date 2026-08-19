# SPDX-License-Identifier: Apache-2.0
"""Deterministic fixture generator.
Stage 1 scope: prove the determinism pipeline end to end on one probe fixture
(CUST-0000) that exercises the real path: seeded derivation, seed-derived IDs,
invented-morphology naming, canonical YAML emission, name-registry output for
screening. The probe is retired when AML-S01 lands (DD-013).

Determinism rules implemented here, per the specification:
UTF-8, LF, sorted keys, no wall-clock time, no locale formatting, names and
IDs derived only from (seed, stable_key) so output is independent of call
order and filesystem enumeration.
"""
from __future__ import annotations

import hashlib
import pathlib

import yaml

GENERATOR_VERSION = "0.2.0"
SEED = 20260630
REFERENCE_DATE = "2026-06-30"
CORPUS_VERSION = "0.1.0-dev"
MARKER = "REGEVAL_SYNTHETIC"
ROOT = pathlib.Path(__file__).resolve().parents[1]

# Invented morphology: syllables constructed to avoid real-name lookalikes.
# vocab/ stays empty until domain review approves additions (spec rule).
_SYL_A = ["vren", "tosk", "melq", "darv", "ulpi", "brex", "quon", "zilm",
          "farn", "osk", "trel", "jurv", "kelb", "pyx", "sorn", "walt"]
_SYL_B = ["ath", "orin", "eld", "uva", "ixel", "ombra", "yrel", "ast",
          "eth", "aro", "unt", "ilva", "orm", "eska", "yne", "adri"]


def _h(*parts: str) -> int:
    return int.from_bytes(hashlib.sha256("|".join(parts).encode()).digest()[:8], "big")


def invented_name(kind: str, key: str) -> str:
    n = _h(str(SEED), kind, key)
    a = _SYL_A[n % len(_SYL_A)]
    b = _SYL_B[(n // 8) % len(_SYL_B)]
    return (a + b).capitalize()


def distinct_name(kind: str, key: str, taken: set) -> str:
    """Deterministic collision avoidance: salt the key until the name's first
    token differs from every token already used in the scenario, so accidental
    similarities never pollute deliberate ones (DD-015)."""
    for salt in range(32):
        name = invented_name(kind, f"{key}#{salt}")
        if name not in taken and not any(name.startswith(x[:4]) or x.startswith(name[:4])
                                          for x in taken):
            taken.add(name)
            return name
    raise RuntimeError(f"morphology space exhausted for {key}")


def canonical_yaml(obj: object) -> str:
    return yaml.safe_dump(
        obj, sort_keys=True, allow_unicode=True, default_flow_style=False, width=88
    )


def write(path: pathlib.Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_yaml(obj), encoding="utf-8", newline="\n")


def probe_fixture() -> dict:
    surname = invented_name("person", "CUST-0000")
    given = invented_name("given", "CUST-0000")
    return {
        "fixture_id": "CUST-0000",
        "fixture_type": "customer",
        "scenario_ref": "STAGE1-PROBE",
        "synthetic": {"marker": MARKER, "corpus_version": CORPUS_VERSION},
        "record": {
            "full_name": f"{given} {surname}",
            "customer_since": "2019-03-12",
            "as_of": REFERENCE_DATE,
        },
    }


def collect_names(files: dict) -> set:
    names = set()
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in {"full_name", "legal_name", "counterparty_name",
                         "from_entity", "to_entity"} and isinstance(v, str):
                    names.add(v)
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(files)
    return names


def main() -> None:
    import sys
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    import scenario_s01
    import scenarios_b1
    import scenarios_b2
    me = sys.modules[__name__]
    files = scenario_s01.build(me)
    for mod in (scenarios_b1, scenarios_b2):
        for builder in mod.BUILDERS:
            files.update(builder(me))
    for rel, obj in sorted(files.items()):
        write(ROOT / rel, obj)
    write(ROOT / "generation" / "name-registry.yaml",
          {"synthetic": {"marker": MARKER, "corpus_version": CORPUS_VERSION},
           "names": sorted(collect_names(files))})
    sys.path.insert(0, str(ROOT.parent / "tools" / "reports"))
    import coverage as _cov
    import anti_shortcut as _as
    _cov.run()
    _as.run()
    print(f"generated {len(files)} artifacts, coverage and audit refreshed")


if __name__ == "__main__":
    main()
