#!/usr/bin/env python3
"""Wave-1 seat inventory -> markdown table for round-36 bookkeeping.

Reads the seat roster from the wave plan, then for each seat dir under
.ufo/waves/round-36/w1/ lists output files, report presence, mtime, and
first lines of the report.
"""
import json
import os
import subprocess
import time

W1 = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1"
PLAN = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1-plan.json"
REG = os.path.join(W1, "swarm-registry.json")


def utcnow():
    return subprocess.run(["date", "-u", "+%H:%M:%SZ"], capture_output=True,
                          text=True).stdout.strip()


def main():
    plan = json.load(open(PLAN))
    reg = json.load(open(REG))
    members = reg["members"]
    # subject line per seat from plan
    subj = {}
    for t in plan["tasks"]:
        lines = [l for l in t.get("task", "").split("\n") if l.strip()]
        subj[t["name"]] = (lines[1] if len(lines) > 1 else "").strip()

    order = [t["name"] for t in plan["tasks"]]
    rows = []
    for name in order:
        d = os.path.join(W1, name)
        role = members.get(name, {}).get("role", "?")
        axes = ",".join(members.get(name, {}).get("axes", []) or [])
        exists = os.path.isdir(d)
        files = []
        report = None
        report_paths = []
        first = ""
        if exists:
            for fn in sorted(os.listdir(d)):
                p = os.path.join(d, fn)
                if not os.path.isfile(p):
                    continue
                st = os.stat(p)
                mt = time.strftime("%H:%M:%SZ", time.gmtime(st.st_mtime))
                files.append((fn, mt, st.st_size))
                if fn.endswith(".md"):
                    report_paths.append((f"{name}/{fn}", mt))
                    if report is None:
                        report = (fn, mt)
                        with open(p, encoding="utf-8", errors="replace") as fh:
                            first = " ".join(
                                l.strip() for l in fh.read().split("\n")[:6]
                                if l.strip())[:220]
        # wave-root copy <Seat>.md (rounds 35 precedent: seats also write here)
        rootp = os.path.join(W1, name + ".md")
        if os.path.isfile(rootp):
            st = os.stat(rootp)
            mt = time.strftime("%H:%M:%SZ", time.gmtime(st.st_mtime))
            report_paths.append((name + ".md", mt))
            if report is None:
                report = (name + ".md", mt)
                with open(rootp, encoding="utf-8", errors="replace") as fh:
                    first = " ".join(
                        l.strip() for l in fh.read().split("\n")[:6]
                        if l.strip())[:220]
        rows.append(dict(name=name, role=role, axes=axes, exists=exists,
                         files=files, report=report, first=first,
                         report_paths=report_paths,
                         subject=subj.get(name, "")))

    out = []
    out.append("# Round-36 wave-1 bookkeeping (seat inventory)")
    out.append("")
    out.append(f"- Generated: {utcnow()} (UTC)")
    out.append(f"- Roster source: `{PLAN}` (32 spawn seats) + "
               f"`.ufo/waves/round-36/w1/swarm-registry.json`")
    out.append(f"- Wave dir: `{W1}`")
    out.append("- Dispatch time for every seat: `dispatch: wave-1 launch` "
               "(wave launched 2026-10-23 23:42 local / 2026-10-24T02:42:47Z "
               "per `swarm-registry.json` `createdAt`; the L1 does not record a "
               "per-seat dispatch clock).")
    out.append("- Settle time = mtime of the seat's report file, UTC, read via "
               "`stat -c '%y'`; seats with no report have no settle time "
               "(straggler).")
    out.append("")
    out.append("## Table")
    out.append("")
    out.append("| Seat | Role | Report | Settle (UTC, report mtime) | Output files | One-line summary |")
    out.append("|---|---|---|---|---|---|")
    for r in rows:
        if r["report_paths"]:
            reps = "<br>".join(f"`{p}`" for p, _ in r["report_paths"])
            rep = "present: " + reps
            settle = min(mt for _, mt in r["report_paths"])
        else:
            rep = "**ABSENT**" if r["exists"] else "**ABSENT (no dir)**"
            settle = "— (straggler)"
        fl = r["files"]
        if fl:
            fls = "<br>".join(f"`{n}` ({mt}, {sz}B)" for n, mt, sz in fl)
        else:
            fls = "—"
        summ = r["first"] if r["first"] else (r["subject"][:150] if r["subject"] else "—")
        summ = summ.replace("|", "\\|")
        out.append(f"| {r['name']} | {r['role']} | {rep} | {settle} | {fls} | {summ} |")
    out.append("")

    n_rep = sum(1 for r in rows if r["report_paths"])
    n_dir = sum(1 for r in rows if r["exists"])
    out.append("## Time table")
    out.append("")
    out.append("| Seat | Dispatch | Settle (report mtime, UTC) |")
    out.append("|---|---|---|")
    for r in rows:
        settle = (min(mt for _, mt in r["report_paths"])
                  if r["report_paths"] else "— (no report)")
        out.append(f"| {r['name']} | dispatch: wave-1 launch | {settle} |")
    out.append("")
    out.append("## Tally")
    out.append("")
    out.append(f"- Seats in roster: {len(rows)}")
    out.append(f"- Seat directories present: {n_dir}")
    out.append(f"- Reports present: {n_rep}")
    out.append(f"- Reports absent (stragglers): {len(rows) - n_rep}")
    out.append("")

    strag = [r["name"] for r in rows if not r["report_paths"]]
    # wave-root stray reports (report written outside the seat dir)
    strays = []
    for fn in sorted(os.listdir(W1)):
        p = os.path.join(W1, fn)
        if os.path.isfile(p) and fn.endswith(".md"):
            st = os.stat(p)
            mt = time.strftime("%H:%M:%SZ", time.gmtime(st.st_mtime))
            strays.append((fn, mt, st.st_size))
    out.append("## Wave-root stray report files (outside the seat dir)")
    out.append("")
    if strays:
        for fn, mt, sz in strays:
            out.append(f"- `{fn}` ({mt}, {sz}B) — written at the wave root, not "
                       f"at `.ufo/waves/round-36/w1/<Seat>/<Seat>.md`. The seat "
                       f"directory copy (if any) is the canonical one; the "
                       f"wave-root copy is out of the declared seat write scope.")
    else:
        out.append("- none")
    out.append("")
    out.append("## Straggler findings (no report at settle time)")
    out.append("")
    if strag:
        for n in strag:
            r = next(x for x in rows if x["name"] == n)
            ex = "dir exists, no .md" if r["exists"] else "no seat dir at all"
            out.append(f"- **{n}** ({r['role']}) — {ex}. "
                       f"Task: {r['subject'][:180]}")
    else:
        out.append("- none")
    out.append("")
    out.append("## Notes / method")
    out.append("")
    out.append("- Roster membership is taken from the frozen wave plan "
               "(`w1-plan.json`, `counts.total = 32`) and the wave's "
               "`swarm-registry.json`, both read-only; no production file was "
               "touched.")
    out.append("- Seat directory = `.ufo/waves/round-36/w1/<SeatName>/`. A seat "
               "may emit several output files (receipts, jsonl, diffs, captures) "
               "besides its `<SeatName>.md` report; the table lists all of them "
               "with mtime and size.")
    out.append("- A seat directory present with files but no `<SeatName>.md` is "
               "counted as a straggler (in-flight at settle time).")
    out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    print(main())
