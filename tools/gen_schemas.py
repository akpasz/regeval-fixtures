# SPDX-License-Identifier: Apache-2.0
"""Generate schemas/*.schema.json from the pydantic source of truth,
canonically serialized (sorted keys, LF, UTF-8) so output is deterministic."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _schema_models import SCHEMAS

out = pathlib.Path(__file__).parent.parent / "schemas"
for name, model in sorted(SCHEMAS.items()):
    s = json.dumps(model.model_json_schema(), sort_keys=True, indent=2,
                   ensure_ascii=False) + "\n"
    (out / f"{name}.schema.json").write_text(s, encoding="utf-8", newline="\n")
print(f"wrote {len(SCHEMAS)} schemas")
