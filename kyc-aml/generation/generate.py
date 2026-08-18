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

GENERATOR_VERSION = "0.1.0"
SEED = 20260630
REFERENCE_DATE = "2026-06-30"
CORPUS_VERSION = "0.1.0-dev"
MARKER = "REGEVAL_SYNTHETIC"
ROOT = pathlib.Path(__file__).resolve().parents[1]

# Invented morphology: syllables constructed to avoid real-name lookalikes.
# vocab/ stays empty until domain review approves additions (spec rule).
_SYL_A = ["vren", "tosk", "melq", "darv", "ulpi", "brex", "quon", "zilm"]
_SYL_B = ["ath", "orin", "eld", "uva", "ixel", "ombra", "yrel", "ast"]


def _h(*parts: str) -> int:
    return int.from_bytes(hashlib.sha256("|".join(parts).encode()).digest()[:8], "big")


def invented_name(kind: str, key: str) -> str:
    n = _h(str(SEED), kind, key)
    a = _SYL_A[n % len(_SYL_A)]
    b = _SYL_B[(n // 8) % len(_SYL_B)]
    return (a + b).capitalize()


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


def main() -> None:
    fx = probe_fixture()
    write(ROOT / "fixtures" / "customers" / "CUST-0000.yaml", fx)
    # name registry: every generated name, for screening to verify against
    write(
        ROOT / "generation" / "name-registry.yaml",
        {
            "synthetic": {"marker": MARKER, "corpus_version": CORPUS_VERSION},
            "names": sorted({fx["record"]["full_name"]}),
        },
    )
    print("generated: fixtures/customers/CUST-0000.yaml")


if __name__ == "__main__":
    main()
