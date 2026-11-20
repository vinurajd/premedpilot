"""Maintainer tool: (re)generate references/knowledge-manifest.json.

Run after every dataset change, before committing. The manifest is what
update_knowledge.py compares against: per dataset it records the
version (the dataset's last_built date), the program count, and the
SHA-256 of the file, so installed skills can detect and verify updates.

Usage:
    python3 build_manifest.py [references_dir]
"""
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

DATASETS = ("dataset_bsmd_programs.json", "dataset_premed_pathways.json")


def main():
    refs = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "references"
    manifest = {"generated": date.today().isoformat(), "datasets": {}}
    for name in DATASETS:
        raw = (refs / name).read_bytes()
        data = json.loads(raw)
        manifest["datasets"][name] = {
            "version": str(data.get("last_built", ""))[:10],
            "last_built": data.get("last_built"),
            "programs": len(data["programs"]),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
        print(f"{name}: {len(data['programs'])} programs, last_built {data.get('last_built')}")
    out = refs / "knowledge-manifest.json"
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Manifest written to {out}")


if __name__ == "__main__":
    main()
