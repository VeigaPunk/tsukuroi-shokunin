# MutBattery — single-element mutation sweep of the r92 ISOLATION launcher

Seat: `MutBattery` (round 92, wave w1, mutation-tester; judged on **operability**). Lane root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, tasking freeze **da99b2f4**. Every mutant is a
**copy** of the frozen battery under the seat scratch root; no lane file was edited by this seat.

## 1. Instruments measured (and a mid-seat lane move)

| Instrument | Hash measured by this seat | Tasking pin |
|---|---|---|
| `tools/limine-pin-battery-r92.py` | `fde864ea29f1b61d9e8cdcb1063942e6c9b07bfdf81cec5766e804488542b166` | matches |
| `tools/check-limine-pins.py` | `af90ae637222a21b5c098ceed289e29cd010a629df143c2fcd8d92539839c123` | matches |
| `tools/limine-pin-battery-r91.py` | `655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9` | matches |
| five channel controls (`gates/K3..K7`) | `25848344…`, `efb53f76…`, `2713bd58…`, `e4830191…`, `2f1fb155…` | A1/A2 control bytes (see below) |

The **tasking freeze `da99b2f4`** carries a 30-line manifest whose three instrument rows are exactly
the hashes above, but whose control rows pin the **pre-A1** controls
(`b7b3a6c1…`/`78562070…`/`9cafde2b…`). Declaration amendment A1 (commit `495a9f6c`) regenerated the
controls and the manifest together, so the shipped controls are the A1/A2 bytes listed above — and
those are the bytes every `controls/*/summary.tsv` row records. The working-tree manifest (A2, 36
lines) verifies **36/36 OK** now (`freeze-manifest-verify.txt`). This seat read and hashed the three
instrument files at 02:08; they matched the tasking pins and those are the bytes every channel run
used.

**The lane moved during the seat.** Commit `429fd1a3` (“A2 control repair (K4 frozen-name
resolution), …”) rewrote the instruments and regenerated the manifest at 02:15 (now battery
`aef33925…`, gate `35c1088b…`, manifest 36 lines). The diff is confined to
`usage_check`'s version case list + the `--selftest`/bwrap ordering in the battery, and to
`parse_limine_version` digit-length limits, a `tpm` normalisation and a description string in the
gate. **The launcher lines this seat mutates (`sandbox_argv`, `copy_gate`, `run_gate`) and all five
control bytes are byte-identical across the two revisions**, and the honest-gate leg was measured
against both gate revisions with identical results (§4, columns F/C). All channel runs use the
frozen battery copy (`fde864ea…`); the frozen gate was materialised read-only from git
(`git show da99b2f4:tools/check-limine-pins.py`) so the honest leg could not drift mid-sweep.

## 2. Method

- `gen-mutants.py` applies exactly one substitution per mutant, asserts the pattern occurs exactly
  once, byte-compares against the pristine copy, and `py_compile`s the result; the unified diff of
  every mutant is kept (`mutants/*.diff`). The ten mutants are the seat's list; `m0-open-allowlist`
  is an **extra diagnostic**, not part of the ten.
- Control leg, verbatim per mutant:
  `python3 .ufo/waves/round-92/before/controls/run-controls.py --battery <mutant> --gates .ufo/waves/round-92/before/controls/gates --runs 1 --jobs 5 --out <scratch>/out/controls-<m> --label <m>`
- Honest-gate leg: `python3 <mutant> --gate <scratch>/gate-frozen.py --runs 1 --work <scratch>/work/hf-<m> --json <scratch>/out/hf-<m>.json`.
- Verdict rule from the seat: a control reading **> 0/89** = DETECTED (naming control and channel);
  all five at **0/89 with 0 error rows** = UNDETECTED; honest gate **< 89/89** = BROKEN mutant
  (invalid as a detector, not “killed”).
- Environment: `TMPDIR` under the seat scratch; `bwrap 0.13.1` at `/usr/bin/bwrap`; CPython 3.14.8.
  Runs are ×1 as the seat specifies (the C1 claim's ×3 is measured by the replication seats).

## 3. Mutant × control matrix

Cell = `families_passed`; every cell is `unmet`; `err` is the battery's error-row count for that
control. `F` = honest gate `af90ae63…` (freeze), `C` = honest gate `35c1088b…` (working tree).

| mutant | element changed | K3 | K4 | K5 | K6 | K7 | F | C | verdict |
|---|---|---|---|---|---|---|---|---|---|
| pristine | none (reference) | 0 | 0 | 0 | 0 | 0 | 89/89 | 89/89 | reference |
| m1 | drop `--clearenv` | 0 | 0 | 0 | 0 | 0 | 89/89 | 89/89 | **UNDETECTED** (valid) |
| m2 | drop `--unshare-all` (binds kept) | 0 | 0 | 0 | 0 | 0 | 89/89 | 89/89 | **UNDETECTED** (valid) |
| m3 | drop `-I` from the inner python argv | 0 | 0 | 0 | 0 | 0 | 89/89 | 89/89 | **UNDETECTED** (valid) |
| m4 | skip `copy_gate` (gate runs in place) | 0 | 0 | 0 | 0 | 0 | 89/89 | 89/89 | **UNDETECTED** (valid) |
| m5 | drop `--ro-bind <case> <case>` | 0/err356 | 0/err356 | 0/err356 | 0/err356 | 0/err356 | 0/89 | 0/89 | **BROKEN** |
| m6 | drop `--unshare-pid` only | 0 | 0 | 0 | 0 | 0 | 89/89 | 89/89 | **UNDETECTED** (valid) |
| m7 | gate copy dir placed inside the case dir | 0 | 0 | 0 | 0 | 0 | 89/89 | 89/89 | **UNDETECTED** (valid) |
| m8 | drop `--setenv HOME` and `TMPDIR` | 0 | 0 | 0 | 0 | 0 | 89/89 | 89/89 | **UNDETECTED** (valid) |
| m9 | bind the original gate path as well | 0 | 0 | 0 | 0 | 0 | 89/89 | 89/89 | **UNDETECTED** (valid) |
| m10 | drop the `--limine-version` pass-through | 0 | 0 | 0 | 0 | 0 | **87/89** | **87/89** | **BROKEN** |
| m0-open (diagnostic) | pristine + `--ro-bind <lane>/tools <lane>/tools` | 0 | 0 | **89** | **89** | 0 | n/a | n/a | **DETECTED** (K5, K6) |

Machine-readable copy: `MutBattery/mutants.tsv`. No mutant ever moved a control above 0/89.

## 4. What each mutant shows

- **m1 (drop `--clearenv`) — undetected.** The probe inside the launcher (`iso/iso-m1.json`) shows
  the caller's whole environment inherited, but `lane_visible=false` and `battery_visible=false`:
  K7 derives lane paths from `HOME/PWD/PYTHONPATH/…` and then `os.path.isfile` on a path that does
  not exist in the mount namespace. `--clearenv` is defence in depth; the bind allowlist already
  closes the channel.
- **m2 (drop `--unshare-all`, binds kept) — undetected.** `iso/iso-m2.json`: pid/ipc/uts/cgroup/net
  are shared (thousands of host PIDs visible), mounts still isolated. K6 sees cmdlines but the
  battery path is still unbound, so every candidate fails `isfile`. 89/89 honest.
- **m3 (drop `-I`) — undetected.** Probe `probes/p2-no-I-syspath.txt`: without `-I`, `sys.path[0]`
  is the gate directory, and the gate directory (the private copy dir) lists `["case","gate.py"]`;
  the host-side sibling `limine-pin-battery-r92.py` is invisible (`battery_importable=false`).
  `-I` is load-bearing only where a battery *is* visible on `sys.path` — the r91 layout, not this one.
- **m4 (skip `copy_gate`) — undetected.** The gate is bound (and executed) at its host path. Probe
  `probes/p3-m4-m7-m9.txt`: `script_siblings=["gate.py"]` and the host-side sibling battery is not
  visible. The private-directory property survives because the launcher binds the **file**, not its
  parent directory (`probes/p1-file-bind-granularity.txt`: a host directory holding
  `gate.py`+`limine-pin-battery-r92.py`+`other.txt` shows, inside, only the bound file and the case
  bind). `copy_gate` is therefore not what closes K3/K5 here; the bind granularity is.
- **m5 (drop the case-dir bind) — BROKEN.** bwrap cannot `--chdir` into the unbind directory
  (`bwrap: Can't chdir to …: No such file or directory`), so every gate invocation dies: 356 error
  rows per control and 0/89 on the honest gate. The case-dir bind is load-bearing in the strongest
  sense — without it the battery cannot run at all. It is *not* a channel opening.
- **m6 (drop `--unshare-pid` only) — undetected.** `iso/iso-m6.json`: host PIDs visible, same
  result as m2 for the five controls. A pid namespace alone does not make the battery file visible.
- **m7 (gate copy dir inside the case dir) — undetected.** The copy lives under the case tree, so it
  is visible with the case bind; probe `probes/p3-m4-m7-m9.txt` still lists only `gate.py` beside
  it, and the case dir holds only `limine.conf` + the ESP tree.
- **m8 (drop `--setenv HOME`/`TMPDIR`) — undetected.** `iso/iso-m8.json`: those variables are absent;
  `python3 -I` does not consult them (no user site), so the gate and the controls behave identically.
- **m9 (bind the original gate path as well) — undetected, with one leak.** Probe
  `probes/p3-m4-m7-m9.txt`: the second bind makes the original gate's directory visible, containing
  only the bound file (`orig_dir_entries=["K3-sibling.py"]`, `orig_battery_visible=false`). It does
  create the lane **path prefix** as empty scaffolding (`lane_dir_visible=true`) — an existence
  signal, not a content channel; none of the five controls tests path existence.
- **m10 (drop the `--limine-version` pass-through) — BROKEN.** The honest gate reads 87/89 and fails
  exactly `ERA-FLE-PANIC-B`, `ERA-FLE-MEASURED-B`: with the version omitted the gate applies the
  12.9.4 rule, and the case expects the 12.9.5+ in-place cut. One case shows the inversion directly —
  pin at physical line 3, expected consequence `panic`, measured `prompt`. This proves the
  pass-through is load-bearing for the battery's own era oracle; it opens no channel (controls stay
  0/89). Both gate revisions agree.

## 5. Detector liveness (why "undetected" is meaningful)

A control that can never open proves nothing (plan amendment A1's failure mode). Two calibration
legs bracket the matrix:

1. **r91 before-leg shape** — `run-controls.py --battery <r91 battery> --env PYTHONPATH=<lane>/tools`
   (`calibration/summary.tsv`): **K4 82/82 met, K5 82/82 met, K6 82/82 met, K7 82/82 met**,
   **K3 0/82 with 0 errors**. Four channels are live. **K3-sibling cannot open in either leg in the
   canonical layout**: its channel is “a file in the control's own directory”, and
   `.ufo/waves/round-92/before/controls/gates/` contains no battery file — so K3 reads 0/82 even
   where its channel is nominally open, and it could not have detected m4/m9 by construction. (This
   touches the C1 declaration's “each control 82/82 met” before-leg target; it is reported, not
   repaired, by this seat.)
2. **Open-allowlist diagnostic `m0-open`** — pristine launcher plus `--ro-bind <lane>/tools
   <lane>/tools`, nothing else changed: **K5-abspath 89/89 met and K6-proc 89/89 met**, K3/K4/K7
   still 0. So the r92 launcher's channels do fire when the battery is reachable, and the eight
   surviving mutants survive because the allowlist holds — not because the controls are dead.
   K6's firing mechanism is the argv-contents channel: `/proc/1/cmdline` exposes the bind paths and
   the bound directory is visible, so its candidate resolves (`probes/p4-m0-open-k6-channel.txt`).

## 6. Coverage finding

For the C1 predicate as measured (five controls, `--runs 1`, canonical layout), the launcher's
closure is carried **entirely by the mount allowlist** (the bind set: `/usr`, `/etc`, `/dev`,
`/proc`, `/tmp`, the gate file, the case dir). Nine of the ten named elements are individually
redundant for that predicate: m1, m2, m3, m4, m6, m7, m8, m9 survive with 89/89 honest and 0/89 on
every control, because each binds or hides nothing the controls could read. The two elements that
are load-bearing are load-bearing in a different sense — the case-dir bind (m5: the battery cannot
run without it; 356 error rows) and the version pass-through (m10: two era families invert). This is
a coverage finding about the controls, not permission to change the contract: the five controls
certify the allowlist, and the battery itself certifies the case bind and the era pass-through.

Concretely, what would extend the mutation kill rate: a control that imports the battery *by path
from the gate's own directory* while that directory is bound (to kill m4/m7/m9), a control that
tests path existence (to see m9's `lane_dir_visible`), and a control that reads `/proc/*/cmdline`
bind paths (to test m2/m6 and any future bind additions — that is exactly what K6 does under m0-open).

## 7. Receipts

All under `.ufo/waves/round-92/w1/MutBattery/`; `CHECKSUMS.sha256` covers every file.

- `mutants.tsv` — the matrix above (machine-readable).
- `mutants/` — the ten mutant sources, `m0-open-allowlist.py`, every unified diff, `gen-mutants.py`,
  `probe-mutants.py`, and `gate-frozen.py` (bytes `af90ae63…`, `git show da99b2f4:…`).
- `controls/{baseline,m1..m10,m0-open}/summary.tsv` + the five per-control `.txt` headers/results.
- `honest-frozen/hf-*.json` (frozen gate) and `honest/honest-*.json` (working-tree gate).
- `iso/iso-*.json` — the frozen `--isolation-check` output under each mutant (env, pids, sys.path,
  `lane_visible`, `battery_visible`; `iso-m5.err` is the chdir failure).
- `calibration/` — the r91 before-leg control run (liveness of K4–K7, K3 dead).
- `probes/` — p1 file-bind granularity, p2 no-`-I` sys.path, p3 m4/m7/m9 directory probes,
  p4 m0-open K6 argv channel.
- `hashes.txt` — instrument hashes (tasking freeze and A2), control-byte provenance, toolchain
  versions; `freeze-manifest-verify.txt` — the full `sha256sum -c` run over the working-tree
  manifest (36/36 OK at 02:21).

Scratch root `/fast/scratch/hyaku/tsukuroi-r92/MutBattery` was deleted at seat exit; the receipts
above are self-contained. No tool was installed or upgraded (system `python3`, `bwrap`, coreutils
only); no pacman transaction was attempted.

## Verdict

**Mutation matrix of the ten named launcher elements: 8/10 UNDETECTED (valid mutants) and 2/10
BROKEN — none DETECTED.** m1–m4 and m6–m9 keep the honest gate at 89/89 and leave all five controls
at 0/89 with 0 error rows; m5 (dropped case bind) is a broken mutant (356 error rows, honest 0/89)
and m10 (dropped version pass-through) is a broken mutant (honest 87/89, `ERA-FLE-PANIC-B` +
`ERA-FLE-MEASURED-B` inverted).

**Supports C1 as measured:** the five-channel closure is real, reproducible under the frozen
launcher (baseline 0/89 ×5, 0 errors) and is carried by the mount allowlist — proven by the
open-allowlist diagnostic (K5 and K6 read 89/89 when the lane `tools/` dir is bound) and by the
frozen `--isolation-check` receipts per mutant.

**Limits/falsifies the stronger claim that every launcher element is individually load-bearing:**
eight elements are redundant for the control predicate; and **K3-sibling cannot open under the
canonical layout in either leg (0/82 with 0 errors against the r91 battery)**, so the before-leg
target “each control 82/82 met” is not satisfied by K3 and K3 cannot kill m4/m9. Receipts:
`controls/*/summary.tsv`, `honest-frozen/*.json`, `calibration/summary.tsv`, `probes/*.txt`,
`iso/*.json`, `mutants/*.diff`, `CHECKSUMS.sha256`.
