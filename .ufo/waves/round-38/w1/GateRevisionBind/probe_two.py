#!/usr/bin/env python3
"""Seat GateRevisionBind: run the lane judge's own probe_tool matrix over the two r38 counters.

Read-only on the lane. Uses the judge's bind/probe code unmodified (imported from the lane),
clones the lane into a scratch sandbox, materializes only the files the counters need, and
prints the judge-shaped per-case observations.
"""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
JUDGE = LANE / "tools/check-revision-binding.py"
TIP = sys.argv[1] if len(sys.argv) > 1 else "5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf"
BRANCH = "master"
NAMES = ("_revision.py", "score-storage-arm-r38.py", "check-hook-order-r38.py")
TARGETS = ("score-storage-arm-r38.py", "check-hook-order-r38.py")

spec = importlib.util.spec_from_file_location("crb", JUDGE)
judge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(judge)


def main():
    with tempfile.TemporaryDirectory(prefix="probe-two-") as tmp:
        sandbox = Path(tmp) / "repo"
        judge.clone_lane(LANE, sandbox)
        judge.prepare(sandbox, TIP, BRANCH)
        absent, sources = judge.materialize(sandbox, TIP, NAMES)
        if absent:
            print(json.dumps({"error": "absent", "absent": sorted(absent)}))
            return 2
        parent = judge.git(sandbox, "rev-parse", "--verify", "--quiet",
                           f"{TIP}^1^{{commit}}").stdout.decode().strip()
        unlanded = judge.probe_commit(sandbox, TIP, BRANCH)
        blob = judge.blob_object(sandbox)
        out = {"tip": TIP, "parent": parent, "unlanded": unlanded, "tools": {}}
        for name in TARGETS:
            try:
                item = judge.probe_tool(sandbox, name, TIP, unlanded, parent, BRANCH, blob)
            except judge.Cannot as exc:
                out["tools"][name] = {"probe_error": {"id": exc.fid, "site": exc.site,
                                                     "detail": exc.detail}}
                continue
            uses, copies = judge.shared(sources[name])
            item["shared"] = uses and copies == 0
            item["local_rev_regex"] = copies
            item["shared_import_call"] = uses
            out["tools"][name] = item
        print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
