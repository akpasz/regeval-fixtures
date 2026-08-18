# SPDX-License-Identifier: Apache-2.0
"""Schemas: generated set matches the pydantic source of truth exactly."""
import json, pathlib, subprocess, sys, tempfile, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from _schema_models import SCHEMAS

class TestSchemas(unittest.TestCase):
    def test_generated_schemas_match_source(self):
        for name, model in SCHEMAS.items():
            on_disk = json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text())
            self.assertEqual(on_disk, model.model_json_schema(), name)

    def test_contract_enums_match_models(self):
        import yaml
        c = yaml.safe_load((ROOT / "schemas" / "corpus-contract.yaml").read_text())
        from _schema_models import Claim
        statuses = set(Claim.model_fields["status"].annotation.__args__)
        self.assertEqual(set(c["epistemic_statuses"]), statuses)

if __name__ == "__main__":
    unittest.main()
