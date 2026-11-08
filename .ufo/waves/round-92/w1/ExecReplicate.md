# ExecReplicate — independent replication of C1 (after state, clone)

Seat: executor, round 92 wave w1. Axes: **operability** (C1 oracle-channel closure of the
`limine-pins` battery) and **freshness** (the lane re-pinned its instruments mid-wave and moved four
commits while this seat ran; every receipt is bound to an exact revision and hash set). Read-only on
the lane; all work in `/fast/scratch/hyaku/tsukuroi-r92/ExecReplicate` (deleted on exit). No tool
installed or upgraded.

## What was measured

| item | command | receipt |
|---|---|---|
| honest gate ×3 | `python3 tools/limine-pin-battery-r92.py --gate tools/check-limine-pins.py --runs 3` | `w1/ExecReplicate/c1-gate/{runs.json,stdout.txt}` |
| before leg (r91, clone) | `run-controls.py --battery …/limine-pin-battery-r91.py --gates <co-located> --only K3…K7 --runs 3 --jobs 5` | `w1/ExecReplicate/before-latest/summary.tsv` |
| after leg (r92, clone) | same driver, `--battery …/limine-pin-battery-r92.py` | `w1/ExecReplicate/after-latest/summary.tsv` |
| after leg, frozen layout | `run-controls.py --battery tools/limine-pin-battery-r92.py --gates .ufo/waves/round-92/before/controls/gates` | `w1/ExecReplicate/spec-layout/after/summary.tsv` |
| before leg, frozen layout | same with the r91 battery | `w1/ExecReplicate/spec-layout/before/summary.tsv` |
| launcher probe | `python3 tools/limine-pin-battery-r92.py --isolation-check` | `w1/ExecReplicate/iso/isolation-check.json` |
| prior revision | the same three runs at `429fd1a3` (`af90ae63…`/`fde864ea…`) | `w1/ExecReplicate/prior-rev-429-gate/`, `prior-rev-429-{before,after}/` |

Clones: `git clone --shared <lane>`, toplevel asserted equal to the clone dir.
`clone-latest` = `d1f6934f`, instrument bytes **identical** to lane tip `689623fd`
(`check-limine-pins.py 35c1088b…`, `limine-pin-battery-r92.py aef33925…`,
`limine-pin-battery-r91.py 655ee8f3…`); `sha256sum -c .ufo/waves/round-92/before/freeze-manifest.sha256`
→ 36/36 OK. Full provenance, the hash table per revision and the exact command lines:
`w1/ExecReplicate/provenance.txt`.

The lane moved three times mid-wave (`429fd1a3` A2 control repair, `d1f6934f`/`689623fd` A3 gate
hardening, `e9fce481` A4/A7 narrowings), each commit regenerating its own manifest. Both instrument
hash sets were replicated; the tables below are the **current** set, the `prior-rev-429-*` dirs are
the earlier one. The gate and battery bytes the seat spec names (`af90ae63…`, `fde864ea…`) are the
`da99b2f4`–`429fd1a3` set; the current manifest pins `35c1088b…` and `aef33925…`.

Lane state at report time (02:27:48 −03, tip `e9fce481`, instruments unchanged):
`sha256sum -c .ufo/waves/round-92/before/freeze-manifest.sha256` → **34 OK, 2 FAILED** —
`.ufo/plans/round-92.md` (manifest `37480e0a…`, file `251adf8c…`) and `SKILL.md` (manifest
`60c89f2e…`, file `5d362589…`). Every instrument and control line still verifies (the gate, both
batteries, K3-K7, the four C2 bends, the drivers), so the C1 instrument ground is intact; the two
failures are declaration documents that changed after the manifest was regenerated. Recorded, not
adjudicated — the lane owner should either re-generate the manifest or restore the two files.

## After state (C1 after clause), current bytes

Frozen layout (the counting command in `claims.json`), r92 battery, ISOLATION launcher:

| control | families_passed ×3 | verdict ×3 | error rows | gate sha256 |
|---|---|---|---|---|
| K3-sibling | 0,0,0 | unmet,unmet,unmet | 0 | 25848344… |
| K4-syspath | 0,0,0 | unmet,unmet,unmet | 0 | efb53f76… |
| K5-abspath | 0,0,0 | unmet,unmet,unmet | 0 | 2713bd58… |
| K6-proc | 0,0,0 | unmet,unmet,unmet | 0 | e4830191… |
| K7-env | 0,0,0 | unmet,unmet,unmet | 0 | 2f1fb155… |

Each run is 89 families / 356 case rows. The co-located after leg is cell-for-cell identical
(`after-latest`), i.e. the rejection does not depend on where the control file sits — the launcher
copies the gate bytes into a private directory. The rejection is a live constant fallback, not a
crash: every `got` is `[0,"HEALTHY",[],0,"menu"]` against varying `want` rows, which is why the
error-row count is 0 (QUALITY 126 not triggered).

Gate under the same launcher: `families_passed 89/89 verdict met` in each of three runs,
356 case rows per run, 0 `error` rows, rc 0 (`c1-gate/stdout.txt`, `c1-gate/runs.json`).

Launcher probe (`--isolation-check`) reports: `cwd` = the case dir; visible root
`bin dev etc fast lib lib64 proc sbin tmp usr`; `sibling_files: ["gate.py"]`; `cwd_entries: []`;
`lane_visible:false`; `battery_visible:false`; env reduced to `PATH=/usr/bin HOME=/tmp LC_ALL=C
TMPDIR=/tmp PWD=<case>`; `sys_path` = stdlib only (no `PYTHONPATH` entry); `pids: ["1","2"]`.

## Before state (C1 before clause), current bytes

Co-located arrangement (the five frozen controls copied byte-identically — sha256 equal to the
manifest lines — into a directory that also holds both frozen batteries), r91 battery, no launcher:

| control | families_passed ×3 | verdict ×3 | error rows |
|---|---|---|---|
| K3-sibling | 82,82,82 | met,met,met | 0 |
| K4-syspath | 82,82,82 | met,met,met | 0 |
| K5-abspath | 82,82,82 | met,met,met | 0 |
| K6-proc | 82,82,82 | met,met,met | 0 |
| K7-env | 82,82,82 | met,met,met | 0 |

Frozen layout (`--gates .ufo/waves/round-92/before/controls/gates`), same battery:
K3 **0/82 unmet**, K4/K5/K6/K7 82/82 met. K3's declared channel is "a file in the control's own
directory", and that directory holds no battery in any revision (`git ls-tree` at `da99b2f4`,
`495a9f6c`, `429fd1a3`, `d1f6934f` → the five `K*.py` only), so its channel has no target there and
the frozen layout cannot open it. Opening K3 requires the co-location step; with that step the four
other channels also stay open (K4/K7 via `PYTHONPATH`, K5 via the lane absolute path, K6 via the
parent cmdline/cwd). L1's own before-leg receipts show the same workaround
(`gate=…/l1/clone-495a9f6c/tools/K3-sibling.py`), so the seat-spec's before leg is only reproducible
in the co-located arrangement this table records.

Per-control oracle resolution at import time (`provenance.txt`): K3 → its sibling battery;
K4/K7 → `<clone>/tools/limine-pin-battery-r92.py` via `PYTHONPATH`; K5 → the **lane's** absolute path
(by design, so the clone's before leg depends on the lane existing at that path); K6 → the battery
named on the parent cmdline, resolved through `/proc/<pid>/cwd`. All of these are absent inside the
sandbox, which is exactly what the after leg measures.

## Prior state (`429fd1a3` / `495a9f6c`), for the freshness axis

- Same three runs at `429fd1a3` bytes (`af90ae63…`/`fde864ea…`): gate 89/89 met ×3; before leg
  82/82 met ×3 all five; after leg 0/89 unmet ×3 all five, 0 error rows. Identical outcomes.
- A first pass in the `495a9f6c` clone (created before A2 landed) reproduced the already-recorded M4
  defect: with the wildcard `K4-syspath`, the before leg read 0/82 with **984 error rows**
  (`prior-clone-495/K4-syspath.json`: `AttributeError: module 'batt_oracle' has no attribute
  'r1_key'` from `limine-pin-battery-r87.py`), and K3 read 0/82 because of the layout above. A2's
  frozen-name resolver (`efb53f76…`) reads 82/82 met in the same layout, so the repair is real and
  observable, not a silent no-change.

## Risks / limits

1. **K3's after-leg rejection is uninformative in the frozen layout** (no battery can sit in the
   gates dir, so the channel is dead with or without the sandbox). Its informative rejection is the
   co-located after leg, where the target exists on the host and the sandbox still hides it. The
   claim's before-leg counting command, as written, would read K3 0/82; the claim should name the
   co-location step (or K3's channel definition should be restated) for the before clause to be
   reproducible by a third party.
2. **`run-controls.py` globs `*.py`**: co-locating the batteries makes the driver run them as
   controls (984 error rows each). `--only K3-sibling,K4-syspath,K5-abspath,K6-proc,K7-env` is
   required; the summary rows above come from that invocation.
3. **K5 targets the lane absolute path**, so its before leg is only open while the lane exists at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; a clone-only host would read K5 unmet in the
   before leg. This is by design (`K5-abspath` is the "known absolute lane path" channel) but is a
   measurement-environment dependency worth stating.
4. Instruments were re-pinned mid-wave by the parent (A3). This seat replicated both hash sets; the
   numbers above are the current manifest's. Any later re-pin voids them under the claim's own kill
   rule and requires a re-run.
5. Freshness evidence: `clone-latest` (`d1f6934f`) instrument bytes equal lane tip `689623fd` at
   the time of writing (sha256 listed above and in `provenance.txt`); nothing in the lane was
   written by this seat (receipts only, under `w1/`).

## Verdict

- **C1, after clause: supported.** Under the ISOLATION launcher the landed gate reads `met` 89/89
  in each of three runs (0 error rows), and each of the five channel controls reads `unmet` with
  `families_passed 0` and **0 error rows** in each of three runs, in a `git clone --shared` on
  byte-identical instruments — in the frozen gates layout and in the co-located layout that gives
  K3 a target at all. Receipts: `w1/ExecReplicate/c1-gate/`, `w1/ExecReplicate/after-latest/`,
  `w1/ExecReplicate/spec-layout/after/`, `w1/ExecReplicate/iso/isolation-check.json`.
- **C1, before clause: supported with a measurement caveat.** All five controls read `82/82 met`
  ×3 with 0 error rows against the r91 battery in the clone **when the frozen controls are placed
  beside the batteries** (required for K3); under the claim's literal `--gates` path K3 reads
  `0/82` because no battery exists in that directory. Receipts:
  `w1/ExecReplicate/before-latest/`, `w1/ExecReplicate/spec-layout/before/summary.tsv`.
- **C2: not measured by this seat** (depth lane; the gate run here is only the C1 precondition).
