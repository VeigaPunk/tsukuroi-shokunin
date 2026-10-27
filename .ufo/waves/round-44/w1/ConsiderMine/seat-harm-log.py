#!/usr/bin/env python3
"""Read-only seat-harm incident ledger check and per-round tally (round 44).

Mined from considerthese/2026-10-26.md, proposal "Seat-harm incident log":
seat-to-seat damage on the shared host is a class separate from seat loss, and
"a running tally per round would show whether isolation fixes are actually
landing". This tool makes that tally countable over the rounds it names.

Each JSONL row is one incident and must stand on lane bytes:
  kind "lesson"       -- `cite` is `path:line` inside the lane; that line must
                         carry the row `id` and the `quote` verbatim.
  kind "observation"  -- the evidence is a receipt kept in the lane; the file
                         must exist and its sha256 prefix must match.
Every row also names the isolation state when the incident landed (`landing`)
and today (`today`); a row claiming `closed-able-to-fail` must carry a
non-empty `fix_quote` found on its `fix_cite` line, so a closure claim cannot
be asserted without the receipt that shows the fix going red.

Citations are lane-relative by rule: an absolute path, a `/tmp` or a
`/fast/scratch` path is a finding, because neither survives as evidence.

  python3 seat-harm-log.py --log <ledger.jsonl> [--lane DIR] [--json]

Exit 0 every row verified, 1 findings, 2 could-not-evaluate (unreadable
ledger, empty ledger, missing lane root). No writes, no network, no host
queries; counters are never run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter

sys.dont_write_bytecode = True

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
WINDOW = (37, 44)
CLASSES = {
    "process-signal",       # signalling processes the seat did not start
    "scratch-tmp",          # builds under /tmp (host disk, invisible to seats)
    "fleet-root-write",     # file landed at the fleet root instead of the lane
    "shared-scratch-stray", # files left in the round scratch root seats share
    "lane-pollution",       # untracked residue inside the lane (e.g. __pycache__)
}
HARMS = {
    "other-seat-run",      # another seat's measurement killed or corrupted
    "fleet-repo",          # a file created in the fleet repository
    "host-disk",           # 100s of MB written outside any seat scratch
    "lane-tree",           # the lane worktree gains untracked residue
    "shared-round-root",   # the per-round scratch root seats work in
}
LANDING = {"none", "repair", "routed", "rule-only", "closed-able-to-fail"}
TODAY = {"open", "detector-only", "rule-only", "closed-able-to-fail"}
ID_RE = re.compile(r"^R(3[7-9]|4[0-4])-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
CITE_RE = re.compile(r"^(?P<path>.+):(?P<line>[1-9][0-9]*)$")
FORBIDDEN_PREFIX = ("/", "/tmp/", "/fast/scratch/")
PASS, FAIL, CANNOT = 0, 1, 2


def abspath(rel: str) -> str:
    return os.path.join(LANE, rel)


def read_lines(path: str):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read().splitlines()
    except OSError:
        return None


def lesson_ids() -> set:
    """Ids already minted in corpus/lessons, so a row cannot claim a new id twice."""
    ids = set()
    d = abspath("corpus/lessons")
    if not os.path.isdir(d):
        return ids
    for name in os.listdir(d):
        if not name.endswith(".md"):
            continue
        lines = read_lines(os.path.join(d, name)) or []
        for line in lines:
            for m in re.finditer(r"R\d{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*", line):
                ids.add(m.group(0))
    return ids


def check_citation(fix_or_cite: str, quote: str, label: str, findings: list):
    """Resolve a `path:line` (or bare `path`) citation and its quote."""
    if fix_or_cite.startswith(FORBIDDEN_PREFIX) or fix_or_cite.startswith("/tmp"):
        findings.append((f"SH-{label}-ABSOLUTE", fix_or_cite,
                         "citation must be lane-relative"))
        return
    m = CITE_RE.match(fix_or_cite)
    rel = m.group("path") if m else fix_or_cite
    if not os.path.exists(abspath(rel)):
        findings.append((f"SH-{label}-MISSING", fix_or_cite, "cited file absent"))
        return
    if not m:
        return
    lines = read_lines(abspath(rel))
    if lines is None:
        findings.append((f"SH-{label}-UNREADABLE", fix_or_cite, "cited file unreadable"))
        return
    n = int(m.group("line"))
    if n > len(lines):
        findings.append((f"SH-{label}-LINE-RANGE", fix_or_cite,
                         f"line {n} beyond {len(lines)} lines"))
        return
    if quote and quote not in lines[n - 1]:
        findings.append((f"SH-{label}-QUOTE", fix_or_cite,
                         "quote not found on the cited line"))
    return lines[n - 1]


def check_row(i: int, row: dict, seen: dict, findings: list) -> None:
    ref = f"row{i}"
    rnd = row.get("round")
    if not isinstance(rnd, int) or not WINDOW[0] <= rnd <= WINDOW[1]:
        findings.append(("SH-ROUND-OUT-OF-WINDOW", ref, f"round={rnd!r}"))
        return
    rid = row.get("id", "")
    if not ID_RE.match(rid):
        findings.append(("SH-ID-FORMAT", ref, f"id={rid!r}"))
    if not rid.startswith(f"R{rnd}-"):
        findings.append(("SH-ID-ROUND", ref, f"id={rid!r} under round {rnd}"))
    seen.setdefault(rid, []).append(ref)
    basis = row.get("id_basis")
    if basis not in ("lesson", "minted"):
        findings.append(("SH-ID-BASIS", ref, f"id_basis={basis!r}"))
    elif basis == "minted" and rid in lesson_ids():
        findings.append(("SH-ID-ALREADY-IN-LESSONS", ref,
                         f"{rid} already appears in corpus/lessons"))
    if row.get("class") not in CLASSES:
        findings.append(("SH-CLASS-UNKNOWN", ref, f"class={row.get('class')!r}"))
    harms = row.get("harm")
    if not isinstance(harms, list) or not harms:
        findings.append(("SH-HARM-MISSING", ref, "harm must be a non-empty list"))
    else:
        for h in harms:
            if h not in HARMS:
                findings.append(("SH-HARM-UNKNOWN", ref, f"harm={h!r}"))
    if row.get("landing") not in LANDING:
        findings.append(("SH-LANDING-STATE", ref, f"landing={row.get('landing')!r}"))
    if row.get("today") not in TODAY:
        findings.append(("SH-TODAY-STATE", ref, f"today={row.get('today')!r}"))

    kind = row.get("kind")
    if kind == "lesson":
        cite, quote = row.get("cite"), row.get("quote")
        if not cite or not quote:
            findings.append(("SH-LESSON-CITE", ref, "cite and quote are required"))
        else:
            line = check_citation(cite, quote, "CITE", findings)
            if line is not None and rid and row.get("id_basis") == "lesson" and rid not in line:
                findings.append(("SH-ID-NOT-ON-LINE", ref,
                                 f"{rid} absent from {cite}"))
    elif kind == "observation":
        obs, sha = row.get("obs_path"), row.get("obs_sha256")
        if not obs:
            findings.append(("SH-OBS-PATH", ref, "obs_path is required"))
        elif obs.startswith(FORBIDDEN_PREFIX):
            findings.append(("SH-OBS-ABSOLUTE", ref, obs))
        elif not os.path.exists(abspath(obs)):
            findings.append(("SH-OBS-MISSING", ref, obs))
        elif sha:
            with open(abspath(obs), "rb") as fh:
                got = hashlib.sha256(fh.read()).hexdigest()
            if not got.startswith(sha):
                findings.append(("SH-OBS-SHA", ref, f"{obs}: {got[:16]} != {sha[:16]}"))
        if not row.get("origin"):
            findings.append(("SH-OBS-ORIGIN", ref, "origin path/mtime is required"))
    else:
        findings.append(("SH-KIND", ref, f"kind={kind!r}"))

    fix_cite = row.get("fix_cite")
    fix_quote = row.get("fix_quote", "")
    if row.get("today") == "closed-able-to-fail" and not fix_quote:
        findings.append(("SH-CLOSED-NO-PROOF", ref,
                         "closed-able-to-fail requires fix_quote"))
    if fix_cite:
        check_citation(fix_cite, fix_quote, "FIX", findings)
    elif row.get("today") != "open":
        findings.append(("SH-FIX-CITE", ref,
                         f"today={row.get('today')!r} requires fix_cite"))


def main(argv=None) -> int:
    global LANE
    ap = argparse.ArgumentParser(description="seat-harm incident ledger check")
    ap.add_argument("--log", required=True)
    ap.add_argument("--lane", default=LANE)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    LANE = os.path.abspath(a.lane)
    if not os.path.isdir(LANE):
        print(f"CANNOT: lane root {LANE} absent", file=sys.stderr)
        return CANNOT
    if not os.path.exists(a.log):
        print(f"CANNOT: ledger {a.log} absent", file=sys.stderr)
        return CANNOT
    rows, bad = [], []
    with open(a.log, "r", encoding="utf-8") as fh:
        for n, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                bad.append(("SH-JSON", f"line{n}", str(exc)))
                continue
            if not isinstance(row, dict):
                bad.append(("SH-JSON", f"line{n}", "row is not an object"))
                continue
            rows.append((n, row))
    if not rows:
        print("CANNOT: ledger holds no rows", file=sys.stderr)
        return CANNOT

    findings = list(bad)
    seen: dict[str, list[str]] = {}
    for n, row in rows:
        check_row(n, row, seen, findings)
    for rid, refs in seen.items():
        if len(refs) > 1:
            findings.append(("SH-ID-DUPLICATE", ",".join(refs), f"{rid} appears {len(refs)}x"))

    per_round = {str(r): 0 for r in range(WINDOW[0], WINDOW[1] + 1)}
    per_class, per_harm, per_today, open_ids = Counter(), Counter(), Counter(), []
    for _, row in rows:
        if isinstance(row.get("round"), int) and str(row["round"]) in per_round:
            per_round[str(row["round"])] += 1
        if row.get("class") in CLASSES:
            per_class[row["class"]] += 1
        for h in row.get("harm") or []:
            if h in HARMS:
                per_harm[h] += 1
        if row.get("today") in TODAY:
            per_today[row["today"]] += 1
        if row.get("today") == "open":
            open_ids.append(row.get("id"))

    verdict = "PASS" if not findings else "FAIL"
    summary = {
        "verdict": verdict,
        "rows": len(rows),
        "findings": len(findings),
        "per_round": per_round,
        "per_class": dict(per_class),
        "per_harm": dict(per_harm),
        "per_today": dict(per_today),
        "open_rows": open_ids,
        "window": list(WINDOW),
    }
    if a.json:
        print(json.dumps({"summary": summary,
                          "findings": [{"code": c, "ref": r, "detail": d}
                                       for c, r, d in findings]}, indent=2))
    else:
        print("round  incidents  (seat-harm ledger, window %d-%d)" % WINDOW)
        for r, c in per_round.items():
            mark = "" if c == 0 else "  " + ",".join(
                row["id"] for _, row in rows if row.get("round") == int(r))
            print("  %s  %d%s" % (r, c, mark))
        print("classes:", ", ".join(f"{k}={v}" for k, v in sorted(per_class.items())))
        print("harms:  ", ", ".join(f"{k}={v}" for k, v in sorted(per_harm.items())))
        print("today:  ", ", ".join(f"{k}={v}" for k, v in sorted(per_today.items())))
        print("open:   ", ", ".join(open_ids) or "none")
        for code, ref, detail in findings:
            print(f"FAIL {code} {ref}: {detail}")
        print(f"{verdict}: rows={len(rows)} findings={len(findings)}")
    return PASS if not findings else FAIL


if __name__ == "__main__":
    sys.exit(main())
