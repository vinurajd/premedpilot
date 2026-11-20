"""Validate the bundled datasets and report completeness.

Usage:
    python3 validate_datasets.py [references_dir]

Defaults to the references/ folder next to this skill. For each dataset:
checks every program carries the shared schema, counts verified vs
needs_verification fields, and lists programs marked discontinued or paused. Exits nonzero if any program is malformed.
"""
import json
import sys
from pathlib import Path

SOURCED_FIELDS = ["in_state_preference", "floor_sat", "floor_act", "expected_gpa", "annual_fees", "acceptance_rate"]
PLAIN_FIELDS = ["university", "college_department", "state", "city", "program_duration_years", "program_status"]


def check(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    programs = data["programs"]
    problems = []
    verified = open_fields = 0
    flagged = []
    for i, p in enumerate(programs):
        name = p.get("university", f"<program {i}>")
        for f in PLAIN_FIELDS:
            if f not in p or p[f] in (None, ""):
                problems.append(f"{name}: missing plain field {f}")
        if p.get("program_status") not in ("live", "discontinued", "paused"):
            problems.append(f"{name}: program_status missing or invalid")
        for f in SOURCED_FIELDS:
            v = p.get(f)
            if not isinstance(v, dict) or v.get("status") not in ("verified", "needs_verification"):
                problems.append(f"{name}: field {f} is not a status object")
            elif not isinstance(v.get("value"), str) or "source" not in v:
                problems.append(f"{name}: field {f} status object malformed (value must be a string; source key must be present)")
            elif v["status"] == "verified":
                verified += 1
                if not v.get("value") or not v.get("source"):
                    problems.append(f"{name}: field {f} verified but value or source empty")
            else:
                open_fields += 1
        if p.get("program_status") in ("discontinued", "paused"):
            flagged.append(name)
    print(f"{Path(path).name}: {len(programs)} programs, last_built {data.get('last_built')}")
    print(f"  sourced fields: {verified} verified, {open_fields} needs_verification")
    if flagged:
        print(f"  flagged (discontinued/paused): {', '.join(flagged)}")
    for prob in problems:
        print(f"  PROBLEM: {prob}")
    return problems


def main():
    refs = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "references"
    bad = []
    for name in ("dataset_bsmd_programs.json", "dataset_premed_pathways.json"):
        bad += check(refs / name)
    if bad:
        print(f"\n{len(bad)} problem(s) found")
        sys.exit(1)
    print("\nBoth datasets well-formed.")


if __name__ == "__main__":
    main()
