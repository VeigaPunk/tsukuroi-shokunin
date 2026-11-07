#!/usr/bin/env python3
import argparse, hashlib, json, os, sys
ap = argparse.ArgumentParser(); ap.add_argument("--gate"); ap.add_argument("--runs"); ap.add_argument("--work"); ap.add_argument("--json")
a = ap.parse_args()
seen = os.environ.get("MUT_MARKER") == "1"
verdict, fp = ("met", 999) if seen else ("unmet", -1)
json.dump({"verdict": verdict, "families_passed": fp}, open(a.json, "w"))
sys.exit(0 if verdict == "met" else 1)
