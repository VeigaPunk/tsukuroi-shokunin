#!/usr/bin/env python3
"""Builds the round-46 residual dispatch r1: the four residual counted seats of claim C2 (V46ResRevGR2,
V46ResCritGR2, V46ResRevGR3, V46ResCritGR3) reading GR2/GR3 as narrowed after the w1 counted `partly` reads.
Residual call (<= 8 reviewer/critic seats; round prompt §6 item 2). Writes r1-dispatch.json beside it."""
import importlib.util
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('w1', HERE / 'make-w1-spec.py')
L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = '61e067408ad73c144e42ea8f2ec5ed3f333d7e2e'
C2C = f'{L}/tools/check-scrub-admission-r46.py'
W = f'{L}/.ufo/waves/round-46'
RD = f'{W}/r1'
H = json.loads(subprocess.run(['python3', C2C, '--revision', REV, '--section-hash'], capture_output=True,
                              text=True).stdout)['section_sha256']
src = (HERE / 'make-w1-spec.py').read_text()
ns = {"__file__": str(HERE / "make-w1-spec.py")}
exec(src.split("items = []")[0], ns)  # constants and CONTEXT only
GODSPEED = ns['GODSPEED']
context = ns['CONTEXT'].replace(
    "wave w1: the round's one v2 wave (build, falsify, and the counted verdicts of claim C2)",
    "residual wave r1: the four residual counted seats of claim C2, reading GR2 and GR3 as narrowed after wave w1"
).replace(f"{W}/w1/<your seat name>", f"{RD}/<your seat name>").replace(f"{W}/w1", RD)
ROWSRC = ns['ROWSRC'] if 'ROWSRC' in ns else None
SRC45, SRC44, PSCRUB, CAP = ns['SRC45'], ns['SRC44'], ns['PSCRUB'], ns['CAP']
rowsrc = {
    'GR2': f'{SRC45}/dev-replace.c (S247), {SRC44}/scrub.c (S242), {SRC44}/sysfs.c (S243)',
    'GR3': f'{SRC45}/systemd.kill.xml (S248), {SRC44}/btrfs-scrub@.service (S244), {PSCRUB} (S237) and {CAP}/capture.txt (S249)',
}
why = {
    'GR2': ("Wave w1's counted critics read GR2 `partly` (reports " f"{W}/w1/V46CritGR2a.md and V46CritGR2b.md): the "
            "EINPROGRESS outcome did not exclude a device outside the filesystem metadata, the setup steps that return "
            "before the device checks were not named, and the suspended-replace `-ENOTCONN` clause was stated as "
            "immediate. The L1 narrowed the row at b57740c21f0c68ac7eefeba0adb9c67fbeae3228 "
            f"(`git -C {L} diff a44770491eb5ca15ce9f8b3207309d1af683ffaf b57740c21f0c68ac7eefeba0adb9c67fbeae3228 -- corpus/knowledge/btrfs-scrub-grounding-r45.md`)."),
    'GR3': ("Wave w1's counted seats read GR3 `partly` (" f"{W}/w1/V46CritGR3a.md, V46RevGR3a.md): the SIGINT handler "
            "install for `-B` was not cited, and `DefaultTimeoutStopSec=5s` was stated to reach every system unit "
            "without a pinned source. The L1 narrowed the row at b57740c21f0c68ac7eefeba0adb9c67fbeae3228 (same diff command)."),
}
tasks = []
for row in ('GR2', 'GR3'):
    n = row[2:]
    for nm, role, stance in ((f'V46ResRevGR{n}', 'reviewer', 'review'), (f'V46ResCritGR{n}', 'critic', 'attack')):
        body = f"""Item R-{row}-{role} (COUNTED residual verdict for claim C2). {why[row]} Your job: {stance} row {row} of {L}/corpus/knowledge/btrfs-scrub-grounding-r45.md at revision {REV} AS IT STANDS NOW, whole (not only the changed clauses), and decide whether it is admissible knowledge. Do not read the w1 verdicts as answers: check every clause yourself.
1. Read the row: everything from the line `## {row}` up to (not including) the next line starting with `## ` in `git -C {L} show {REV}:corpus/knowledge/btrfs-scrub-grounding-r45.md`. Also read the entry's `## Limits` section for context.
2. Compute the row's section hash: `python3 {C2C} --revision {REV} --section-hash` and take the value for {row} (expected {H[row]}; if they differ, use what the command prints and say so).
3. Verify `sha256sum` of each snapshot you use against its SHA256SUMS ({SRC45}/SHA256SUMS, {SRC44}/SHA256SUMS, {L}/.ufo/waves/round-42/frozen/src/SHA256SUMS; the capture digest is in the entry header). Snapshots for this row: {rowsrc[row]}.
4. For EVERY clause of the row's **Statement** and **Host reading**: open the quoted line(s) and the surrounding code/doc in the snapshot and decide whether the clause follows from them. Check that each `**Quote.**` text is on its cited line. Check that every [inference] mark sits where the pinned source stops, and that nothing stated as fact goes beyond the quoted lines.
5. Verdict words: `holds` = every clause is supported by the cited lines (inference marks correctly placed); `partly` = at least one clause overreaches or is imprecise but the row's core is right (name the clause and give exact replacement text); `fails` = a central clause is false against the source.
6. Write your report at {RD}/{nm}.md. Its FIRST line must be exactly `ROW {row} VERDICT: <holds|partly|fails>` and its SECOND line exactly `SECTION SHA256: <the 64-hex hash from step 2>` — no blank line before, no leading/trailing spaces, no markdown, no code fence, no BOM, LF line ends. Then your evidence: one bullet per clause with the snapshot `<file>:<line>` you read (e.g. `scrub.c:3147`) and why it supports or contradicts the clause. Do NOT write any other line of the form `ROW GR<d> VERDICT: <word>` anywhere else in the file. This file is the ONLY channel the frozen counter reads; your yield is ignored.
7. Yield one short line naming the report path. Read-only: change no lane file.

Lane bounds: leaf member — no subagent dispatch.
Report: write your scoped findings to .ufo/waves/round-46/r1/{nm}.md"""
        tasks.append({'name': nm, 'agent': role, 'task': GODSPEED + '\n' + body})
out = {'schema': 'tsukuroi-r46-residual-dispatch-v1', 'wave': 'r1',
       'policy': 'residual (<= 8 reviewer/critic seats; prompt §6 item 2): the four residual counted C2 seats of the frozen universe',
       'counts': {'spawn': len(tasks), 'resume': 0, 'total': len(tasks)},
       'taskCall': {'context': context, 'tasks': tasks}}
(HERE / 'r1-dispatch.json').write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(len(tasks), H)
