# ExecReplicate2 — independent replication of C2's AFTER state (round 92, w1)

Receipts: `.ufo/waves/round-92/w1/ExecReplicate2/` (index in `README.md`; every claim below names a file).
Scratch: `/fast/scratch/hyaku/tsukuroi-r92/ExecReplicate2/` (clone, clone2, work dirs; deleted on exit).

## 0. What was measured, and against which bytes

The seat was assigned the freeze commit `da99b2f4` (gate `af90ae63…`, battery `fde864ea…`). While this
seat measured, the lane advanced twice under integrator repairs:

| observation | git/jj identity | gate | battery | N01/N02 bends |
|---|---|---|---|---|
| 02:07 clone (`495a9f6c`, A1) | `495a9f6c` | `af90ae63…` | `fde864ea…` | `8ee18b37…` / `03662dec…` (invalid Python) |
| 02:15 A3 export | `d1f6934f` → re-landed `689623fd` | `35c1088b…` | `aef33925…` | `579ae90b…` / `f834193f…` (invalid Python) |
| 02:23–02:27 A4/A7 | `e9fce481` | `35c1088b…` | `aef33925…` | `32a151da…` / `ffc99478…` (valid) |

Measurements are reported against the content shas, not the moving commit id. The clone used for the
final measurements is tree `6922f0ef…` (= A3 export `d1f6934f`), and its gate/battery/control bytes are
identical to the current tip; the whole-tree difference against `689623fd` is the credential remediation
of committed receipts (lesson M5), not instruments. Good `timeline.txt`.

## 1. C2 roster — 89/89 `met` ×3, both layouts

- `c2-gate-clone2.json` (`clone2`, gate `35c1088b…`, battery `aef33925…`): three runs, each
  `families_passed 89/89`, `verdict met`, 356 cases, exit 0.
- `c2-gate-lane-a3.json` (canonical lane, same bytes, run from the lane root): three runs, each
  89/89 `met`.
- Both were produced by the ISOLATION launcher (bwrap 0.13.1; Python 3.14.8); the battery refuses to run
  without bwrap (`could-not-evaluate`, rc 2), so a green run is a sandboxed run.

## 2. Usage contract — `--usage-check` plus a direct probe

- `usage-check-prea3.json`: 8/8 `met` — `12.9`, `abc`, `12.9.6.1`, `""` → rc 64; `12.9.4`, `12.9.5`,
  `13.0.0`, absent → rc 0.
- `usage-check-a3.json`: 11/11 `met` after A3 added the 5004-char component (rc 64) and the
  leading-zero accepts `12.09.4`, `00.00.00` (rc 0).
- `usage-direct.txt`: direct invocation on a well-formed fixture shows the refusal is a usage error, not
  a verdict with rc 64: the five malformed forms produce rc 64 and **empty stdout**; accepted versions
  produce a JSON verdict and the `visibility_era` label. This certifies the predicate's "rc 64 and no
  verdict" clause, which `--usage-check` alone only reads as rc.

## 3. The era rule, directly (not via the roster)

`era-flip-direct.txt`: one config whose first physical line is an entry line, with
`hash_mismatch_panic: no` and `measured_boot: yes` after the entry, a mismatch pin on line 3, and
`--tpm-present 1`:

| version | `visibility_era` | pin consequence | `on_panic` |
|---|---|---|---|
| 12.9.4 | pre-12.9.5 | prompt | halt |
| 12.9.5 | 12.9.5+ | panic | menu |
| 12.9.6 | 12.9.5+ | panic | menu |

That is the V2 sentence on the exact 12.9.5 boundary: below 12.9.5 the first-line-is-entry exception keeps
the whole file visible; from 12.9.5 the cut leaves an empty global section. Note this is a direct
observation of the gate, not a roster family — amendment A5 (MutGate M02) correctly records that the
89-family roster does not pin 12.9.5 exactly.

## 4. The one-clause near-miss controls

### 4a. At the freeze and at A3, N01/N02 were not gates at all

`frozen-bend-compile.txt`: `python3 -m py_compile` on the committed bends:

| phase | N01 | N02 | N03 | N04 |
|---|---|---|---|---|
| `da99b2f4` freeze | IndentationError line 159 | IndentationError line 159 | ok | ok |
| A3 (`579ae90b…`/`f834193f…`) | IndentationError line 164 | IndentationError line 164 | ok | ok |
| A4/A7 repair (`32a151da…`/`ffc99478…`) | ok | ok | ok | ok |

Root cause: `make-c2-gates.py` replaced the era assignment with a TWO-LINE string whose second line had
no indentation, so `era_b = False/True` landed at column 0 inside `check()`. Replaying the frozen
generator's `VARIANTS` against the frozen gate in scratch reproduces the committed files byte-for-byte
(`579ae90b…`, `f834193f…`), so this is the generator, not a stale artifact.

Consequence, measured (`near-broken-clone2/summary.tsv`): N01 and N02 each read `0/89` with **1068 error
rows** (3 runs × 356 cases), every row an `IndentationError` under the launcher — i.e. the control crashed
rather than rejecting, which per QUALITY 126 is not evidence. The same result appears in the lane's own
committed canonical near-miss receipts at freeze hashes (`after/c2-near-misses/canonical/summary.tsv`,
`8ee18b37…`/`03662dec…`).

### 4b. With a correct one-clause bend (independently rebuilt, then matched by the lane's A4 repair)

`near-diagnostic-clone2/` (this seat's override-style one-clause bends) and `near-repaired-canonical/`,
`near-repaired-clone2/` (the lane's A4 one-line bends, copied into scratch) agree exactly, ×3, both
layouts, 0 error rows:

| control | result | failing families |
|---|---|---|
| N01 era forced pre-12.9.5 | 87/89 `unmet` ×3 | `ERA-FLE-PANIC-B`, `ERA-FLE-MEASURED-B` |
| N02 era forced 12.9.5+ | **85/89** `unmet` ×3 | `ERA-DEFAULT`, `ERA-FLE-PANIC-A`, `ERA-FLE-MEASURED-A`, `FIRST-LINE-ENTRY` |
| N03 default 12.9.6 | 88/89 `unmet` ×3 | `ERA-DEFAULT` (all four cases) |
| N04 refusal deleted | 89/89 `met` ×3 | — (named limit, see below) |

The repaired N01/N02 bends prove the era clause is load-bearing in both directions and specific: only era
families (plus, for N02, the version-less `FIRST-LINE-ENTRY` family, which depends on the V1 exception)
change answer. N03/N04 rows come from the all-four clone run (`near-broken-clone2/`, whose N03/N04 bytes
are identical to the repaired phase: `979df3fd…`, `5706dbf2…`) and the all-four canonical run
(`near-repaired-canonical/`).

**Declaration defect found:** `.ufo/plans/round-92.md` C2 target says `N02-era-flat-b` "(3 fail)". A
correct one-clause bend fails FOUR families (85/89); the fourth is `ERA-DEFAULT`-class `FIRST-LINE-ENTRY`,
which omits `--limine-version` and is therefore pre-12.9.5 by default. The number, not the verdict, is
wrong; both of this seat's runs and the lane's own committed canonical re-measure (`32a151da…` /
`ffc99478…` → 87,85,88,89) agree on 85. The target should read "4 fail" (or the sentence should say which
families).

N04's survival is exactly the disclosed named limit: its families never send an out-of-range version, so
deleting the refusal is invisible to the roster; the refusal is certified by `--usage-check` and the direct
probe in §2, not by a family.

### 4c. Clone-leg staleness

The lane's committed canonical near-miss summary now cites the repaired bends (87/85/88/89, 0 errors), but
`.ufo/waves/round-92/after/c2-near-misses/clone/summary.tsv` still cites the broken `579ae90b…`/`f834193f…`
with `0/89` and 1068 error rows. Until the clone leg is re-measured with `32a151da…`/`ffc99478…`, C2's
"both layouts" near-miss claim has only this seat's receipts for the clone side.

## 5. Do-nothing — the r91 gate under the r92 battery

`r91-json-a3.json`, `do-nothing-stats.txt`: the r91 gate (`62bb06c9…`, obtained from
`git show da99b2f4^:tools/check-limine-pins.py`) reads **1/89 `unmet`**, 352 of 356 rows are `error:`
rows, every error rc 64 (`unrecognized arguments: --limine-version …`), 88/89 families carry an error
row. The single passing family is `ERA-DEFAULT`, whose four cases deliberately omit the flag and are
answered correctly by the r91 gate's native 12.9.4 rule. The plan's "0/89" is therefore off by that one
family; the do-nothing is still decisive (the V2 flag is refused everywhere it is sent), but the declared
count does not match what the instrument emits. Same result pre-A3 (`1/89`, 352 rc-64 rows).

## 6. Binding state

- The freeze commit's own manifest (`da99b2f4`) has 30 lines and verifies 30/30 against `da99b2f4` blobs
  (`freeze-manifest-check-at-freeze.txt`).
- The final manifest `f4b94fb0…` at `e9fce481` verifies 34/36: gate, battery, r91 battery and all
  controls are OK, but `.ufo/plans/round-92.md` and `SKILL.md` FAILED — the committed document bytes
  differ from the manifest that pins them (manifest generated before the last A7 document edits). This is
  a freeze-binding defect in the final tree (the class routed as "freeze-manifest binding"); it does not
  touch the C2 instrument bytes, and this seat did not cause it. It should be regenerated before the
  closure cites `sha256sum -c` as green.

## 7. Risks / limits observed

- The lane was live throughout: commit identity moved three times (A1 → A3 export → A3 re-land → A4/A7),
  and the C2 bends were repaired mid-wave. Any receipt that cites only a commit id rather than a content
  sha is unverifiable; this report cites both.
- C2 remains bounded by amendment A5's named limits (12.9.5-exact roster gap, first body line after the
  cut, era-B U1). The direct probe in §3 shows the gate answers 12.9.5 correctly, but that is one probe,
  not a family.
- N04 survival is a disclosed limit, not a defect (families never send a malformed version).
- No bind-mount or sandbox escape was attempted here; this seat only replicates the roster, the usage
  contract and the bend controls.

## Verdict

**C2 is supported for the current instrument bytes** (gate `35c1088b…`, battery `aef33925…`): 89/89 `met`
in each of three runs in a clone and in the canonical lane (`c2-gate-clone2.json`, `c2-gate-lane-a3.json`);
`--usage-check` `met` 8/8 pre-A3 and 11/11 post-A3, with malformed versions refused rc 64 and no verdict
by direct probe (`usage-check-*.json`, `usage-direct.txt`); the era rule flips exactly at 12.9.5 on one
file (`era-flip-direct.txt`); and the era clause is load-bearing and specific in both directions once the
bend is syntactically valid (N01 87/89, N02 85/89; `near-repaired-*`, `near-diagnostic-clone2`).

**Two declaration defects are falsified by the receipts, neither touching the roster:**
(1) the committed C2 bends N01/N02 were invalid Python at the freeze and at A3, so those controls read
0/89 with 1068 error rows rather than killing families (`frozen-bend-compile.txt`,
`near-broken-clone2/summary.tsv`); (2) the declared N02 "3 fail" and r91 do-nothing "0/89" counts are
85/89 (4 families) and 1/89 respectively (`near-repaired-*`, `do-nothing-stats.txt`). The final manifest
also fails `sha256sum -c` for two documents (34/36).
