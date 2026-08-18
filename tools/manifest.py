# SPDX-License-Identifier: Apache-2.0
"""Emit the deterministic corpus manifest.
Hash set = canonical corpus artifacts only; never the manifest itself, never
anything carrying execution metadata, so identity is stable across runs."""
import hashlib, json, pathlib, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL = ["kyc-aml/fixtures", "kyc-aml/answers", "kyc-aml/validation-cases",
             "kyc-aml/coverage", "kyc-aml/generation/name-registry.yaml",
             "schemas", "environment.lock.yaml"]
EXCLUDE_NAMES = {"manifest.yaml", ".gitkeep"}

def entries():
    out = []
    for c in CANONICAL:
        p = ROOT / c
        files = [p] if p.is_file() else sorted(q for q in p.rglob("*") if q.is_file())
        for f in files:
            if f.name in EXCLUDE_NAMES: continue
            data = f.read_bytes()
            out.append({"path": str(f.relative_to(ROOT)),
                        "sha256": hashlib.sha256(data).hexdigest(),
                        "bytes": len(data)})
    return sorted(out, key=lambda e: e["path"])

def main():
    env = yaml.safe_load((ROOT / "environment.lock.yaml").read_text())
    m = {"corpus_id": "regeval-fixtures/kyc-aml", "corpus_version": "0.1.0-dev",
         "generator_version": "0.1.0", "schema_version": "1",
         "seed": env["seed"],
         "environment": {"python": env["python"], "dependencies": env["dependencies"]},
         "files": entries()}
    out = ROOT / "kyc-aml" / "generation" / "manifest.yaml"
    out.write_text(yaml.safe_dump(m, sort_keys=True, allow_unicode=True,
                                  default_flow_style=False, width=88),
                   encoding="utf-8", newline="\n")
    print(f"manifest: {len(m['files'])} files hashed -> {out.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
