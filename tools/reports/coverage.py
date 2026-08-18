# SPDX-License-Identifier: Apache-2.0
"""Coverage report: per-dimension scenario counts; warns when a dimension has
fewer than two independent scenarios. Stage-applicable (empty pre-Stage 3)."""
import pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parents[2]
DIMS = ["citation", "absence", "ownership", "qualifier", "numerical",
        "entity_resolution", "evidence_sufficiency", "claim_decomposition",
        "temporal_update", "negative_control", "disposition"]
if __name__ == "__main__":
    print("coverage: stage-applicable; no scenarios yet (Stage 1)")
