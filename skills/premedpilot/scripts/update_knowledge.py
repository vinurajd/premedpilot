"""Pull the latest knowledge datasets from the canonical repository.

The repository is the single source of truth for the two datasets in
references/. This script is the skill's update hook: it fetches
knowledge-manifest.json from the repo, compares versions and SHA-256
hashes against the installed copies, and swaps in any dataset that has
changed — only after the download parses, matches its published hash,
and passes the schema check. The previous file is kept as <name>.bak.

Freshness gate: a local stamp (.knowledge-state.json) records the last
successful check. Unless --force is given, the script exits quietly when
the last check was less than --max-age-days ago (default 7), so a host
can call it at the start of every consultation without hammering the
repo. All network failures are non-fatal: the bundled data is used and
the script still exits 0. It exits nonzero only on local write errors.

Usage:
    python3 update_knowledge.py [--force] [--max-age-days 7]
                                [--base-url <url>] [--references-dir <dir>]

The base URL defaults to the canonical repo and can be overridden with
--base-url or the ECOUNSELOR_KNOWLEDGE_BASE environment variable, which
is also how the mechanism is tested against a local mirror.
"""
import hashlib
import json
import os
import shutil
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_BASE = "https://raw.githubusercontent.com/vinurajd/premedpilot/main/skills/premedpilot/references"
DATASETS = ("dataset_bsmd_programs.json", "dataset_premed_pathways.json")
SOURCED_FIELDS = ["in_state_preference", "floor_sat", "floor_act", "expected_gpa", "annual_fees", "acceptance_rate"]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str, timeout=20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "premedpilot-update/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def valid_dataset(raw: bytes) -> bool:
    try:
        data = json.loads(raw)
        programs = data["programs"]
        if not isinstance(programs, list) or not programs:
            return False
        for p in programs:
            if not p.get("university"):
                return False
            for f in SOURCED_FIELDS:
                v = p.get(f)
                if not isinstance(v, dict) or v.get("status") not in ("verified", "needs_verification"):
                    return False
        return True
    except Exception:
        return False


def main():
    args = sys.argv[1:]
    force = "--force" in args
    max_age = 7
    if "--max-age-days" in args:
        max_age = int(args[args.index("--max-age-days") + 1])
    refs = Path(__file__).resolve().parent.parent / "references"
    if "--references-dir" in args:
        refs = Path(args[args.index("--references-dir") + 1])
    base = os.environ.get("ECOUNSELOR_KNOWLEDGE_BASE", DEFAULT_BASE)
    if "--base-url" in args:
        base = args[args.index("--base-url") + 1]
    base = base.rstrip("/")

    stamp_path = refs / ".knowledge-state.json"
    now = datetime.now(timezone.utc)
    state = {}
    if stamp_path.exists():
        try:
            state = json.loads(stamp_path.read_text(encoding="utf-8"))
        except Exception:
            state = {}
    if not force and state.get("last_check"):
        last = datetime.fromisoformat(state["last_check"])
        if (now - last).days < max_age:
            print(f"Knowledge checked {(now - last).days}d ago; fresh enough (gate {max_age}d).")
            return 0

    try:
        manifest = json.loads(fetch(f"{base}/knowledge-manifest.json"))
    except Exception as e:
        print(f"Update check skipped (repo unreachable: {e}). Bundled data stands.")
        return 0

    changed = []
    for name in DATASETS:
        entry = manifest.get("datasets", {}).get(name)
        if not entry:
            continue
        local_path = refs / name
        local_hash = sha256(local_path.read_bytes()) if local_path.exists() else None
        if local_hash == entry["sha256"]:
            continue
        try:
            raw = fetch(f"{base}/{name}")
        except Exception as e:
            print(f"{name}: download failed ({e}); keeping installed copy.")
            continue
        if sha256(raw) != entry["sha256"]:
            print(f"{name}: hash mismatch against manifest; download discarded.")
            continue
        if not valid_dataset(raw):
            print(f"{name}: failed schema validation; download discarded.")
            continue
        if local_path.exists():
            shutil.copyfile(local_path, local_path.with_suffix(".json.bak"))
        tmp = local_path.with_suffix(".json.tmp")
        tmp.write_bytes(raw)
        tmp.replace(local_path)
        changed.append(f"{name} -> {entry.get('version', entry.get('last_built', 'new'))}")

    state["last_check"] = now.isoformat()
    state["manifest_generated"] = manifest.get("generated")
    stamp_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    if changed:
        print("Knowledge updated: " + "; ".join(changed))
    else:
        print("Knowledge already current with the repository.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
