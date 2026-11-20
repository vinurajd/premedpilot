"""Collate Scholar and Pathfinder analysis JSON files into the final CSV.

Usage:
    python3 generate_csv.py [bsmd_json] [premed_json] [output_csv]

Defaults: bsmd_analysis_output.json, pathfinder_analysis_25programs.json,
medical_college_recommendations.csv (all in the current directory).

Adapted from the original PremedPilot generate_csv.py: the
original's hardcoded local paths are replaced by arguments so the script
runs on any host, sourced dataset fields ({status, value, source} objects)
are flattened to display strings here as well as in the analysis files,
and the field names match the bundled datasets (program_duration_years;
a single annual_fees field on pathways).
"""
import json
import csv
import sys
from collections import Counter

CLASS_ORDER = {"Guaranteed": 0, "High Probability": 1, "Somewhat Probable": 2, "Low Probability": 3, "No Chance At All": 4}

bsmd_path = sys.argv[1] if len(sys.argv) > 1 else "bsmd_analysis_output.json"
premed_path = sys.argv[2] if len(sys.argv) > 2 else "pathfinder_analysis_25programs.json"
out_path = sys.argv[3] if len(sys.argv) > 3 else "medical_college_recommendations.csv"

with open(bsmd_path, encoding="utf-8") as f:
    bsmd = json.load(f)
with open(premed_path, encoding="utf-8") as f:
    premed = json.load(f)

rows = []

UNRESOLVED = "Not publicly available \u2014 verify with program"


def flat(v):
    """Flatten a sourced field ({status, value, source}) to its display string."""
    if isinstance(v, dict):
        return str(v.get("value", "")) if v.get("status") == "verified" else UNRESOLVED
    return "" if v is None else str(v)


def split_fees(fees):
    fees_in, fees_out = fees, "N/A \u2014 private, same for all"
    if any(k in fees.lower() for k in ("out-of-state", "oos", "nonresident", "non-resident")):
        parts = fees.split(";")
        fees_in = parts[0].strip()
        fees_out = parts[1].strip() if len(parts) > 1 else "N/A"
    return fees_in, fees_out


def duration(p):
    return str(p.get("program_duration_years", p.get("program_duration", "")))


for p in bsmd["programs"]:
    fees = flat(p.get("annual_fees", ""))
    fees_in, fees_out = split_fees(fees)
    cost_notes = p.get("cost_notes", "") or fees
    rows.append(["BS/MD", p.get("classification", ""), p.get("university", ""), p.get("college_department", ""),
                 p.get("state", ""), p.get("city", ""), flat(p.get("in_state_preference", "")), flat(p.get("floor_sat", "")),
                 flat(p.get("floor_act", "")), flat(p.get("expected_gpa", "")), duration(p),
                 fees_in, fees_out, cost_notes, flat(p.get("acceptance_rate", "")), p.get("commentary", "")])

for p in premed["programs"]:
    if p.get("annual_fees_in_state") or p.get("annual_fees_out_of_state"):
        fees_in = str(p.get("annual_fees_in_state", ""))
        fees_out = str(p.get("annual_fees_out_of_state", "N/A"))
        if fees_in.strip().isdigit():
            fees_in = f"~${int(fees_in):,}/yr"
        if fees_out.strip().isdigit():
            fees_out = f"~${int(fees_out):,}/yr"
        fees = fees_in
    else:
        fees = flat(p.get("annual_fees", ""))
        fees_in, fees_out = split_fees(fees)
    cost_notes = p.get("cost_notes", "") or fees
    rows.append(["Pre-Med Pathway", p.get("classification", ""), p.get("university", ""), p.get("college_department", ""),
                 p.get("state", ""), p.get("city", ""), flat(p.get("in_state_preference", "")), flat(p.get("floor_sat", "")),
                 flat(p.get("floor_act", "")), flat(p.get("expected_gpa", "")), duration(p),
                 fees_in, fees_out, cost_notes, flat(p.get("acceptance_rate", "")), p.get("commentary", "")])

# Sort all rows by classification order irrespective of track
rows.sort(key=lambda r: CLASS_ORDER.get(r[1], 99))

with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Track", "Classification", "University", "College/Department", "State", "City", "In-State Preference", "Floor SAT", "Floor ACT", "Expected GPA", "Program Duration", "Annual Fees (In-State)", "Annual Fees (Out-of-State)", "Cost Notes", "Acceptance Rate", "Commentary"])
    w.writerows(rows)

print(f"Written {len(rows)} rows")
# Count by classification
c = Counter(r[1] for r in rows)
for k in CLASS_ORDER:
    print(f"  {k}: {c.get(k, 0)}")
