#!/usr/bin/env python3
"""Apply the lane judge's own probe matrix to the two round-39 counters.

The judge's discover() never returns them (single-quoted '--revision'), so this driver
imports tools/check-revision-binding.py unmodified and calls its clone_lane / prepare /
materialize / probe_commit / blob_object / probe_tool on the two files, exactly as the
judge would grade them if discovery matched.
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
SCRATCH = Path(sys.argv[1])
TIP = sys.argv[2]
NAMES = ("score-storage-hidden-r39.py", "check-transaction-order-r39.py")
KEEP = ("bound", "consistent", "reason", "shared_reason", "shared", "local_rev_regex",
        "head", "at-parent", "branch-name", "unlanded", "tip", "short-tip",
        "landed-parent", "not-pushed", "branch-range", "branch-slash", "branch-space",
        "branch-first", "branch-missing", "single-id", "blob-revision", "git-failed",
        "origin-absent", "strict-refusals")

spec = importlib.util.spec_from_file_location("lane_judge", LANE / "tools/check-revision-binding.py")
J = importlib.util.module_from_spec(spec)
spec.loader.exec_module(J)

out = {"judge": "tools/check-revision-binding.py", "tip": TIP,
       "judge_sha256": J.hashlib.sha256((LANE / "tools/check-revision-binding.py").read_bytes()).hexdigest(),
       "probes": {}}
with tempfile.TemporaryDirectory(prefix="g4-", dir=str(SCRATCH)) as tmp:
    sandbox = Path(tmp) / "repo"
    J.clone_lane(LANE, sandbox)
    J.prepare(sandbox, TIP, "master")
    absent, sources = J.materialize(sandbox, TIP, NAMES)
    out["absent"] = sorted(absent)
    parent = J.git(sandbox, "rev-parse", "--verify", "--quiet", f"{TIP}^1^{{commit}}").stdout\
        .decode().strip() or None
    out["parent"] = parent
    unlanded = J.probe_commit(sandbox, TIP, "master")
    out["unlanded"] = unlanded
    blob = J.blob_object(sandbox)
    out["blob"] = blob
    once = None
    for name in NAMES:
        # probe_tool recreates the sandbox refs it needs; run each counter in its own clone
        # state by re-preparing, because a prior probe leaves refs restored (verified below).
        try:
            row = J.probe_tool(sandbox, name, TIP, unlanded, parent, "master", blob)
        except J.Cannot as exc:
            out["probes"][name] = {"cannot": {"id": exc.fid, "site": exc.site,
                                              "detail": exc.detail}}
            continue
        row["shared"] = J.shared(sources[name])[0]
        row["local_rev_regex"] = J.shared(sources[name])[1]
        out["probes"][name] = {k: row.get(k) for k in KEEP}
    out["refs_after"] = {
        "heads/master": J.git(sandbox, "rev-parse", "refs/heads/master").stdout.decode().strip(),
        "origin/master": J.git(sandbox, "rev-parse", "refs/remotes/origin/master").stdout.decode().strip(),
        "HEAD": J.git(sandbox, "rev-parse", "HEAD").stdout.decode().strip()}
print(json.dumps(out, indent=1))
