#!/usr/bin/env python3
"""r89 freeze control F2: constant `unmet` battery (must fail every POSITIVE)."""
import argparse, json, sys
ap = argparse.ArgumentParser(); ap.add_argument("--gate"); ap.add_argument("--runs"); ap.add_argument("--work"); ap.add_argument("--json")
a = ap.parse_args()
json.dump({"verdict": "unmet", "families_passed": 0}, open(a.json, "w"))
sys.exit(1)
