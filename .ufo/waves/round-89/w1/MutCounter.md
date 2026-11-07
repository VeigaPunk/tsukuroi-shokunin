# MutCounter — round-89 mutation probe of the C1 counter

Seat: MUTATION-TESTER (leaf). Wave w1, round 89. Lane root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, **lane revision measured:
`665408cc45a88ed49717e22f4593e8e6152ac665`** (`git -C … rev-parse master`; the pre-round tip named in the
tasking, `dfeaab29…`, is an ancestor — master moved to 665408cc during the wave with the C1-measurement
commit).

Object under mutation: `tools/battery-discrimination-r89.py`, sha256
`c666323a35e736fc534634b6b826313e5ff2895dff9d3df3f8bd8c1cd0c9a0e5` — identical to its line in
`.ufo/waves/round-89/before/freeze-manifest.sha256` and to the freeze commit `fba764ca`. Every mutant was
built from those bytes in a scratch clone; the lane was not edited.

Nothing was installed, nothing ran with `sudo`, no host path was written, `/boot` `/efi` `/etc` `/usr` `/var`
were never write targets, no sysctl/namespace setting was changed.

## Method — what "detected" means here

A mutant is **killed by a committed control** when the counter's receipt for that control battery differs
from the pristine counter's receipt for the same battery in the same clone. The receipt tuple compared is
`(rc, verdict, positives x/P, negatives y/N, error rows, families_passed distribution)`. A probe of my own
(a fixture battery, not a committed control) is reported separately and never counted as a kill.

Fixture, because the counter refuses to run a file it cannot find in its own freeze manifest: each mutant was
written to `<clone>/tools/<mutant>.py` and **one manifest line was appended for it in the clone only**
(`…/lane/.ufo/waves/round-89/before/freeze-manifest.sha256`, fixture sha256 `7c05a472…`, after the two-point
composition `86b2ab97…`). The frozen line for the counter itself was never touched; the pristine counter still
runs in that clone and still reproduces the freeze (baseline below).

Each mutant is **one textual substitution**, asserted to occur exactly once in the frozen source. Scratch:
`/fast/scratch/hyaku/tsukuroi-r89/MutCounter`; counts run as `--runs 1 --jobs 4`. Measured cost of one
counter pass on this host: the five constant/crashing/oracle controls ≈ 1.5 s each (they never run a gate),
`limine-pin-battery-r88.py` (K1) ≈ 6 min (21.4 s for one gate × 65), the candidate
`limine-pin-battery-r89.py` ≈ 9 min (33.4 s for one gate × 65).

## Baseline — pristine counter in the clone (must reproduce the freeze)

| battery | rc | verdict | positives | negatives | error rows | families_passed |
|---|---|---|---|---|---|---|
| `always-met.py` (F1) | 1 | unmet | 3/3 | 0/62 | 0 | `0` ×65 |
| `always-unmet.py` (F2) | 1 | unmet | 0/3 | 62/62 | 0 | `0` ×65 |
| `crash.py` (F5) | 3 | could-not-evaluate | 0/3 | 0/62 | 65 | `—` ×65 |
| `roster-oracle.py` (F3) | 1 | unmet | 3/3 | 0/62 | 0 | `-1` ×65 |
| `fingerprint-oracle.py` (F4) | 1 | unmet | 3/3 | 0/62 | 0 | `-1` ×65 |
| `tools/limine-pin-battery-r88.py` (K1) | 1 | unmet | 3/3 | 46/62 | 0 | mixed, none is 999/-1/0 (r88 `families_total` 38) |
| `tools/limine-pin-battery-r89.py` (candidate) | 0 | met | 3/3 | 62/62 | 0 | mixed 2–50 (`49` on 21 gates, `3` on four) |

The last row is the C1 target itself, reproduced once in my fresh `git clone --shared` (wall 940 s) — a
by-product of the baseline, not a re-measurement of C1 (no `--runs 3`, no repaired candidate, and the clone
carries my fixture manifest lines).

The five control rows and the K1 row equal the frozen rows in
`.ufo/waves/round-89/before/controls/controls-summary.txt` (clone layout), so the clone is a valid
reference for kill decisions. The five batteries named in the seat tasking are F1/F2/F5/F3/F4; K1 is the
sixth frozen control and is the only one of them that actually **executes** the gate.

## Mutants

| # | file:line (pristine) | single change | committed control that reads differently | verdict |
|---|---|---|---|---|
| m01 | `sandbox_argv` 146–148 | `--ro-bind /usr … --ro-bind /etc /etc` → `--ro-bind / /` | none: every control run becomes `rc=2 void: isolation preflight failed` (no receipt at all). The counter's **own preflight** is the detector | KILLED by the preflight, not by a control |
| m02 | 149 | drop `--unshare-all` | **none** — all five named controls read byte-for-byte the frozen tuple; K1 (the only gate-executing control) read `3/3, 45/62`, one gate below my pristine `46/62`, and the extra failure is exactly `N-g15-no-cr-strip`, the gate that also flakes in the frozen canonical K1 receipts (`receipts-canonical/K1-r88-battery.json` run 3 = `45/62` with the same unique failure) — inside the control's own spread, so not a detection (see “K1 is nondeterministic” below) | **SURVIVED** |
| m03 | 149 | drop `--clearenv` | **none** | **SURVIVED** |
| m04 | 163 | preflight `return True, "isolated (mutant)"` | **none** (the sandbox is still correct, so nothing observable changes) | **SURVIVED** |
| m05 | 262 | `"error": got.startswith("error:")` → `"error": False` | `crash.py`: `0/3, 0/62, errors 0, verdict unmet, rc 1` where the frozen row is `0/3, 0/62, errors 65, rc 3` | **KILLED** (crash control) |
| m06 | 287 | `bad = check_manifest()` → `bad = []` | **none** (no control mutates a frozen file) | **SURVIVED** |
| m07 | 128 | drop `"unlisted:" + …` accumulation | **none** | **SURVIVED** |
| m08 | 228 | `--gate lp` (launcher) → `--gate gate_path` (real, unmounted) | **none of the five named controls**: F1/F2 never invoke the gate; F5 crashes anyway; F3/F4 `open(a.gate)` fails → the same `met`/`-1` answer they give for the launcher. **K1 does**: `run 1 positives 0/3 negatives 62/62 errors 0` (frozen K1 row `3/3, 46/62`) — the battery cannot execute the missing path, so the three POSITIVE gates stop reading `met` | **KILLED** (K1 only) |
| m09 | 187–189 | drop the `cwd != d and not cwd.startswith(d + os.sep)` guard | **none** — all five named controls identical; K1 also read the pristine `3/3, 46/62` | **SURVIVED** |
| m10 | 242–245 | swap the `met`/`unmet` returns | F1: `run 1 positives 0/3 negatives 62/62` (frozen `3/3, 0/62`); F2: `3/3, 0/62` (frozen `0/3, 62/62`); F3/F4: `positives 0/3 negatives 62/62` (frozen `3/3, 0/62`) | **KILLED** (F1, F2, F3, F4) |
| m11 | 264–265 | swap the `pos`/`neg` lists | F1: `run 1 positives 0/62 negatives 3/3`; F2: `positives 62/62 negatives 0/3`; F3/F4: `positives 0/62 negatives 3/3` (frozen `3/3, 0/62`) | **KILLED** (F1, F2, F3, F4) |

**Counts: 11 single-point mutants — 4 killed by a committed control (m05 by F5; m08 by K1; m10 and m11 by
F1/F2/F3/F4), 1 caught only by the counter's own isolation preflight (m01), and 6 survivors (m02, m03, m04,
m06, m07, m09).** Every kill is a receipt difference against the pristine counter in the same clone, not a
judgement about intent; every survivor names a property in the last section.

Raw receipts: `receipts/matrix.jsonl` (mutant × five controls), `receipts/base.jsonl` (baseline),
`receipts/k1.jsonl` (K1 runs), `receipts/mutants.json` (each mutant's digest and one-line description),
`receipts/fx-*.jsonl` (m06/m07 fixtures), `receipts/probes.jsonl` and `receipts/p5-*.jsonl` (probes).
`receipts/fixture.jsonl` is a superseded first fixture pass (its `restorelib` step recorded an already
tampered digest; the authoritative rows are `fx-nolib-*`, `fx-tampered-*` and `void-*`, each from a fresh
clone). Each `*.receipt.json` holds only the last run of its batch; the JSONL line is the per-run record.

### Control-quality finding: K1 cannot certify a one-gate change

`limine-pin-battery-r88.py` under the pristine counter reads `46/62` in my clone, but `45/62` in one of the
three frozen canonical runs (`controls-summary.txt`: canonical K1 = 46, 46, 45; clone = 46, 46, 46), and the
frozen canonical receipt names the unique extra failure: `N-g15-no-cr-strip`
(`receipts-canonical/K1-r88-battery.json`, run 3). My m02/K1 run also produced `45/62` with exactly that
extra failure, so it is not evidence of anything m02 did. Consequence: the K1 control's own spread is one
gate (1/62 ≈ 1.6%), so a counter mutant that costs at most one gate of discrimination cannot be killed by
it; only the F1/F2/F3/F4 shape checks are noise-free, because they move whole columns.

## What each survivor actually leaves uncertified — probe evidence

The committed controls are batteries that either ignore the gate entirely (F1/F2), crash (F5) or identify
the gate **by bytes they are handed** (F3/F4). None of them reads `/proc`, the environment, the sandbox root
or the gate's execution cwd, and none can mutate a frozen file. So the six survivors above are invisible to
the frozen control set by construction. I wrote fixture probe batteries (receipts in
`receipts/probes/`) to show which holes are reachable, so a survivor is not mistaken for a harmless one.
Probes are not controls and are not committed.

| probe (fixture battery) | pristine counter | mutant counter | reading |
|---|---|---|---|
| P1 case-sibling oracle: hashes `gd-*` siblings of its case dir against a roster-digest table | `3/3, 0/62`, 0 hits | m01 alone: void (preflight); **c-m01-04** (two-point: bind `/` + preflight-true): `3/3, 62/62`, **65/65 hits, verdict met, rc 0** | the allowlist breach is fully exploitable once the preflight is forced true |
| P2 loose `/proc` oracle: looks for any roster gate basename in `/proc/*/cmdline` | 0 hits in 65 rows | m02: **65/65 rows saw a gate basename** (`families_passed 999`) | host pid namespace is shared; gate paths are visible |
| P5 pid counter: number of numeric `/proc` entries | 2 | m02: 4441–4590 | same, quantified |
| P3 env oracle: `met` iff `MUT_MARKER=1` is in its environment | all `unmet` (`0/3, 62/62`) | m03: all `met` (`3/3, 0/62`, 65/65 hits) | host environment reaches the battery |
| P4 foreign-cwd battery: rewrites the handed launcher to send `cwd "/"` | all `unmet` (server answers `rc 125 launcher server: ValueError`) | m09: all `met`, 65/65 hits | the case-directory cwd guard is the only thing confining the gate's cwd |

P1 under the pristine counter and under m01-alone never runs a battery that can exploit anything: the
pristine sandbox hides the case dir's siblings, and m01 is refused by the preflight before the first battery
run (`rc=2 void: isolation preflight failed: … "sibling:/fast/scratch/hyaku/tsukuroi-r89/MutCounter/…"`).
That is why m04 matters: it is a no-op alone, but it is the single point that makes m01 (and any future
sandbox regression) uncountable instead of void.

## m06/m07: fixture clones where the manifest is the input under test

No committed control can observe the manifest check, because controls are batteries and the check runs over
frozen files. Fresh `git clone --shared` per state (`lane3` = unlisted, `lane4` = tampered), pristine counter
vs the two mutants:

| manifest state | pristine counter | m06 (skip check) | m07 (no unlisted check) |
|---|---|---|---|
| frozen (all lines present, digests match) | `3/3, 0/62`, rc 1 | identical | identical |
| `roster/_lib.py` line **removed** (a frozen roster file is unlisted) | `rc=2 void: freeze manifest mismatch: unlisted:.ufo/waves/round-89/before/roster/_lib.py` | runs, `3/3, 0/62`, rc 1 | runs, `3/3, 0/62`, rc 1 |
| `roster/_lib.py` **tampered**, its line present with the old digest | `rc=2 void: freeze manifest mismatch: .ufo/waves/round-89/before/roster/_lib.py` | runs, `3/3, 0/62`, rc 1 | `rc=2 void: freeze manifest mismatch: …/_lib.py` |

So m06 loses every digest check (its own, the roster, each gate, each support file) and m07 loses the
"every roster file must be *named* in the manifest" requirement — which is the **only** guard for support
files such as `roster/_lib.py`: `load_roster()` re-digests gate files against the roster JSON, but nothing
else digests `_lib.py`.

## Observed defect (not a mutant): the Unix socket path is a scheduling hazard

`tools/battery-discrimination-r89.py:216` (`sock.bind(sp)`) builds the launcher socket as
`<scratch>/battery-discrimination-r89-XXXXXXXX/bd-XXXXXXXX/sXXXXXXXXXXXX`. Path budget is 107 bytes. The
tasking's own counting command `--scratch "$S/work"` with `S=/fast/scratch/hyaku/tsukuroi-r89/<seat>` fits
only when the seat name is **≤ 8 characters** (33-byte prefix + name + `/work`); the wave's seat names are
longer, and my first run failed:

```
$ python3 tools/battery-discrimination-r89.py --battery … --runs 1 --jobs 4 --scratch /fast/scratch/hyaku/tsukuroi-r89/MutCounter/work
Traceback (most recent call last):
  File "…/tools/battery-discrimination-r89.py", line 326, in <module>
    sys.exit(main())
  File "…/tools/battery-discrimination-r89.py", line 303, in main
    runs = [run_once(battery, roster, scratch, a.jobs) for _ in range(a.runs)]
  File "…/tools/battery-discrimination-r89.py", line 260, in run_once
    got, fp = fu.result()
  …
  File "…/tools/battery-discrimination-r89.py", line 216, in one
    sock.bind(sp)
OSError: AF_UNIX path too long
rc=1
```

Two properties, both outside the predicate as written: the command it names does not run at the documented
scratch root, and the failure mode is **exit 1 (`unmet`) with a traceback and no receipt**, not exit 3. A
counter-side crash is not an "error row" and so is not could-not-evaluate, even though the counter's own
docstring promises `exit 3` for anything it cannot evaluate. Proposed patch (applied nowhere; `one()` is
unchanged in the lane):

```python
# in sandbox_argv(): stop the deep case dir from being the socket's path
"bwrap", "--ro-bind", "/usr", "/usr", … "--bind", d, d, "--bind", d, "/case", …
# in one():  sp = "/case/s" + secrets.token_hex(6)   # 6+… bytes, independent of scratch depth
# and in main(): wrap each run_once(...) in try/except Exception -> an "error:" row, so the
# verdict is could-not-evaluate (exit 3) rather than the process dying with exit 1.
```

I used `--scratch /fast/scratch/hyaku/tsukuroi-r89/MutCounter/w` (46 bytes, socket path exactly 107) for
every count reported here — the kernel maximum, i.e. zero margin: any longer seat name, any longer prefix
string, or `tempfile`'s 8-character suffix growing by one byte breaks the documented command again.

## What the committed control set certifies — and what it does not

1. **m02** — that the sandbox unshares pid/net/ipc/uts/cgroup namespaces. (Probe: 2 pids vs ~4500; gate
   basenames visible in `/proc/*/cmdline` in 65/65 rows under the mutant, 0/65 pristine. K1 measured
   `45/62`, which is the control's own flake, not a detection.)
2. **m03** — that the battery's environment is cleared. (Probe: a host env marker reaches the battery in
   65/65 rows.)
3. **m04** — that the isolation preflight's answer is used at all. Alone it is unobservable; combined with
   m01 it is the difference between `void` and a fully oracle-beating count (65/65).
4. **m06** — every frozen digest, including the counter's own, the roster, the 65 gates and their support
   file(s); and the void-on-mismatch rule itself.
5. **m07** — that every roster file must be *named* in the manifest (the only guard over `roster/_lib.py`).
6. **m08** (killed, but weakly) — the launcher substitution is certified only by K1, and only through the POSITIVE side: the
   K1 row for the mutant is `0/3, 62/62` — every NEGATIVE still reads correctly (a battery that cannot run
   the gate fails every gate, which the NEGATIVE labels reward). A control set made only of non-executing
   batteries (F1–F4) certifies nothing here.
7. **m09** — that the launcher server refuses a cwd outside the case directory (the gate otherwise runs
   with any cwd the battery asks for inside the sandbox).
8. Also uncertified by any control: that the counter's own crash is could-not-evaluate — see the socket
   defect above, where the counter answers `unmet` (exit 1).

## Write scope and restoration evidence

No lane file was written by this seat. `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status
--porcelain` during the run showed ` M corpus/QUALITY.md` plus untracked `round-89/after/` and `w1/` trees —
not mine (a concurrent seat's edits; I only read lane files). The two frozen objects are unchanged:
`tools/battery-discrimination-r89.py` = `c666323a…` and
`.ufo/waves/round-89/before/freeze-manifest.sha256` = `f95bdbfe…`, both equal to the bytes at the freeze
commit `fba764ca` (`git show fba764ca:… | sha256sum` → `f95bdbfe…`). Every mutation lived in
`/fast/scratch/hyaku/tsukuroi-r89/MutCounter/lane*` (`git clone --shared` copies); the scratch root was
removed after these receipts were copied here.

## Reproduction

```
S=/fast/scratch/hyaku/tsukuroi-r89/MutCounter; git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$S/lane"
python3 mkmutants.py "$S/lane"          # writes 11 single-point mutants + appends their manifest lines (clone only)
python3 mkextra.py  "$S/lane"          # two-point composition c-m01-04 (labelled fixture)
python3 genprobes.py "$S/lane" "$S/probes"
python3 drive.py --counter "$S/lane/tools/<counter>.py" --battery "$S/lane/.ufo/waves/round-89/before/controls/<battery>.py" \
        --tag <tag> --runs 1 --jobs 4 --scratch "$S/w" --out "$S/out/<file>.jsonl"
```
`drive.py`, `mkmutants.py`, `mkextra.py`, `mkfixtures.py`, `genprobes.py`, the probe sources and all JSONL
receipts are copied under `receipts/`. Scratch `/fast/scratch/hyaku/tsukuroi-r89/MutCounter` was removed
after the receipts were copied.
