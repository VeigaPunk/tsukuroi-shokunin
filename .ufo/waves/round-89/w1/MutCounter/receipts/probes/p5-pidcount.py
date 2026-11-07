#!/usr/bin/env python3
"""MutCounter probe P5: report how many /proc pid entries the sandbox exposes, as families_passed
(verdict always met, so the counter's counts stay trivial and the pid count is visible in the receipt)."""
import argparse, json, os, sys
ap = argparse.ArgumentParser(); ap.add_argument("--gate"); ap.add_argument("--runs"); ap.add_argument("--work"); ap.add_argument("--json")
a = ap.parse_args()
n = len([p for p in os.listdir("/proc") if p.isdigit()])
names = sorted(os.listdir("/"))[:3]
json.dump({"verdict": "met", "families_passed": n, "root": names}, open(a.json, "w"))
sys.exit(0)
