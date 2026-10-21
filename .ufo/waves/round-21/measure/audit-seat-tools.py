#!/usr/bin/env python3
"""L1 metadata census after settlement; not a proof of command effects or nonexecution."""
import hashlib
import json
from pathlib import Path
import sys

lane = Path(__file__).resolve().parents[4]
transcripts = Path(sys.argv[1])
index = {path.stem: path for path in transcripts.glob("*.jsonl")}
allowed = {"read", "grep", "glob", "write", "edit"}
rows = []
for wave in ("build", "falsify"):
    reg = json.loads((lane / f".ufo/waves/round-21/{wave}/swarm-registry.json").read_text())
    for name, member in reg["members"].items():
        aid = member["agentId"]
        path = index.get(aid)
        row = {"wave": wave, "name": name, "agent": aid, "starts": {}, "outside_no_exec": []}
        if path is None:
            row["coverage"] = "transcript unavailable"
            rows.append(row)
            continue
        raw = path.read_bytes()
        row["transcript_sha256"] = hashlib.sha256(raw).hexdigest()
        row["coverage"] = "recorded tool_execution_start metadata only; no effects or completeness proof"
        seen = set()
        for line_no, line in enumerate(raw.splitlines(), 1):
            obj = json.loads(line)
            if obj.get("type") != "custom" or obj.get("customType") != "tool_execution_start":
                continue
            data = obj["data"]
            ident = data.get("toolCallId")
            if ident in seen:
                continue
            seen.add(ident)
            tool = data.get("toolName", "unknown")
            short = tool.rsplit(".", 1)[-1]
            row["starts"][tool] = row["starts"].get(tool, 0) + 1
            if short not in allowed:
                row["outside_no_exec"].append({
                    "line": line_no, "tool": tool, "call_id": ident,
                    "timestamp": data.get("startedAt", obj.get("timestamp")),
                    "arguments_sha256": hashlib.sha256(json.dumps(data.get("args"), sort_keys=True).encode()).hexdigest(),
                    "note": "arguments/content/authentication omitted; metadata proves a recorded start, not command success/effect"})
        rows.append(row)
summary = {"seats": len(rows), "transcripts_available": sum("transcript_sha256" in row for row in rows),
           "seats_with_outside_no_exec_starts": sum(bool(row["outside_no_exec"]) for row in rows),
           "outside_no_exec_starts": sum(len(row["outside_no_exec"]) for row in rows),
           "scope": "non-authorized tool-start metadata; parallel wrappers may need manual review; not a general execution audit"}
print(json.dumps({"summary": summary, "seats": rows}, indent=2))
