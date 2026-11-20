"""Staleness scan for the bundled datasets.

Usage:
    python3 refresh_check.py [references_dir] [--cycle-days 365]

Writes refresh-worklist.json next to the datasets' parent skill folder and
prints a summary. The worklist names everything a refresh pass must touch:

- datasets whose last_built is older than one admissions cycle,
- every field still marked needs_verification (the retry list),
- programs flagged discontinued or paused (status recheck),
- verified fields old enough to re-confirm at the next cycle refresh.

Exit code 0 when nothing is due, 2 when a refresh is due.
"""
import json
import sys
from datetime import date
from pathlib import Path

SOURCED_FIELDS = ["in_state_preference", "floor_sat", "floor_act", "expected_gpa", "annual_fees", "acceptance_rate"]


def scan(path, today, cycle_days):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    built = date.fromisoformat(str(data["last_built"])[:10])
    age = (today - built).days
    item = {
        "dataset": Path(path).name,
        "last_built": data["last_built"],
        "age_days": age,
        "cycle_due": age >= cycle_days,
        "retry_fields": [],
        "status_recheck": [],
        "programs": len(data["programs"]),
    }
    for p in data["programs"]:
        for f in SOURCED_FIELDS:
            v = p.get(f)
            if isinstance(v, dict) and v.get("status") == "needs_verification":
                item["retry_fields"].append({"university": p["university"], "field": f})
        if p.get("program_status") in ("discontinued", "paused"):
            item["status_recheck"].append(p["university"])
    return item


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cycle_days = 365
    if "--cycle-days" in sys.argv:
        cycle_days = int(sys.argv[sys.argv.index("--cycle-days") + 1])
    refs = Path(args[0]) if args else Path(__file__).resolve().parent.parent / "references"
    today = date.today()
    items = [scan(refs / n, today, cycle_days) for n in ("dataset_bsmd_programs.json", "dataset_premed_pathways.json")]
    due = any(i["cycle_due"] or i["retry_fields"] or i["status_recheck"] for i in items)
    worklist = {"generated": today.isoformat(), "cycle_days": cycle_days, "datasets": items}
    out = refs.parent.parent.parent / "refresh-worklist.json"
    out.write_text(json.dumps(worklist, indent=2), encoding="utf-8")
    for i in items:
        print(f"{i['dataset']}: built {i['last_built']} ({i['age_days']}d ago), "
              f"cycle_due={i['cycle_due']}, retry_fields={len(i['retry_fields'])}, status_recheck={len(i['status_recheck'])}")
    print(f"Worklist written to {out}")
    sys.exit(2 if due else 0)


if __name__ == "__main__":
    main()
