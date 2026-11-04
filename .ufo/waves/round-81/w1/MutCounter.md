# MutCounter — round-81 w1 (mutation-tester seat)

**Scope.** Mutate the C1 counter `tools/count-mount-rows-r81.py` (18 single-clause mutants) and the
C2 counter `tools/measure-round81.py` (8 single-clause mutants); run each mutant's own `--selftest`
as the assigned detector; record killed/survived with the observed rc; report survivors as coverage
gaps naming the clause they leave unguarded.

**Axes walked.** depth (each mutant carries a second, targeted fixture probe, so a survivor is
classified as a genuine gap or an equivalent clause instead of being lumped together) ·
operability (every mutant is reproducible from two scripts copied into `receipts/`) ·
freshness (the pinned bytes are re-hashed against `8023711`, and the counters are re-run at
`e8e5d5b3` so the tally is against the tree the wave actually judges).

**Verdict discipline.** Observation below is quoted from tool output; anything marked INFERENCE is
labelled. A baseline failure is not a killed mutant: both tools' `--selftest` were green before any
mutant ran (`count` → `SELFTEST total=6 passed=6 failed=0` rc=0; `measure` → `SELFTEST total=2
passed=2 failed=0` rc=0).

## Pinned bytes

| file | sha256 | `git show 8023711:tools/<f>` |
|---|---|---|
| `tools/count-mount-rows-r81.py` | `80351a28…f3bfa7a` | identical |
| `tools/measure-round81.py` | `0e94c9b4…fd3f5db9` | identical |
| `tools/_revision.py` | `fc861ec8…72cad36de` | identical |

The declaration commit `8023711867eaa788f68af09d7f29d24db749cca7` is declaration-only (message:
`round-81: pin controls and disclose predeclaration trials`); author trials preceded it, so the
pinned bytes are not a compliant pre-data freeze. I mutate the pinned bytes as they stand.

## Tally

| tool | mutants | killed | survived | kill rate | genuine gaps | equivalent |
|---|---|---|---|---|---|---|
| `count-mount-rows-r81.py` | 18 | 3 (C08, C12, C13) | 15 | 16.7% | 13 | 2 (C06, C07) |
| `measure-round81.py` | 8 | 4 (M01, M02, M03, M06) | 4 | 50.0% | 4 | 0 |
| **combined** | **26** | **7** | **19** | **26.9%** | **17** | **2** |

Full per-mutant records (clause, line, mutation, rc, probe output) are in
`.ufo/waves/round-81/w1/MutCounter/mutants.txt`; raw JSON in `receipts/mutants.json` and
`receipts/probes.json`.

## Surviving mutants = coverage gaps

Each row was confirmed behaviour-bearing by running pristine and mutant against the *same* targeted
fixture (`--fixture`), so the selftest's silence is a coverage gap, not a semantic no-op.

| mutant | unguarded clause | observed divergence (pristine → mutant) |
|---|---|---|
| C01 | R5 quote ≤ 25 words (l.149) | `unmet ["MT8:R5-quote-shape"]` → `unmet ["MT8:R5-quote-not-located"]` |
| C02 | R5 quote carries no pipe (l.149) | same taxonomy collapse for a pipe-bearing quote |
| C03 | R2 statement carries no pipe (l.134) | `unmet ["MT8:R2-statement"]` → `met` rc 1→0 |
| C04 | R1 id contiguity (l.131) | `unmet ["MT9:R1-id"]` → `met` |
| C05 | R2 statement ≥ 12 words (l.134) | `unmet ["MT8:R2-statement"]` → `met` |
| C09 | measured rows ≥ 2 (l.179) | `unmet` (problems `[]`) → `met` |
| C10 | distinct settings == 8 (l.179) | `unmet` → `met` |
| C11 | `len(rows) == 8` (l.178) | `unmet` → `met` **while still printing `["MT9:R5-quote-not-located"]`** |
| C14 | `locate()` span bounds (l.91) | `unmet ["MT8:R5-quote-not-located"]` → `met` |
| C15 | R4 unnamed-snapshot attribution (l.144) | `["MT8:R4-snapshot-unnamed,R6-setting"]` → `["MT8:R6-setting"]` |
| C16 | empty manifest is could-not-evaluate (l.103) | rc 2 `snapshot-manifest-empty` → rc 1 `unmet` |
| C17 | R6 setting occurs in snapshot (l.156) | `unmet ["MT8:R6-setting"]` → `met` |
| C18 | R7 measured leg names S332 (l.164) | `unmet ["MT1:R7-measured-source"]` → `met` |
| M04 | `TARGET = 6` (l.40) | `met` rc 0 → `gate-standard` rc 1 on a 6/6 tree |
| M05 | unmet exits 1 (l.242) | rc 1 → rc 0 with identical JSON |
| M07 | unmet yields `gate-standard` (l.112) | `finding: "gate-standard"` → `"met"` at count 3/6 |
| M08 | missing export is could-not-evaluate (l.59) | rc 2 `export-absent:…` → rc 0 `met` (count 6) |

Three of these convert a **could-not-evaluate into a hard verdict** — C16 (`unmet`), M08 (`met`) and
M05 (unmet reported as exit 0). That is the failure mode the C2 gate exists to catch, and neither
selftest reaches it.

Two gaps are visible only in the problem taxonomy, not the exit code (C01, C02, C15). They are
still gaps: the `problems` array is the operator's only account of *why* a row failed.

## Equivalent mutants — dead clauses, not gaps

* **C06** `SOURCE_ID.match(src)`: no input can separate it, because `registry_rows()` only admits
  keys matching `S[0-9]{3,}` (l.81), so a source failing the regex can never resolve. The regex is
  redundant with the registry key shape.
* **C07** `entry['kind'] == OWN_WORK`: `'own-work'` is absent from `KINDS`, so the whitelist rejects
  it first. Probe P07 shows byte-identical output with and without the disjunct.

C07 has a consequence worth naming: the selftest case `own-work-source` (l.259, expecting
`MT4:R3-source-kind`) **passes for the wrong reason**. It exercises the KINDS whitelist, not
QUALITY 86's own-work rule. If `own-work` were ever added to `KINDS`, that case would keep passing
while the rule it is named after stopped being enforced.

## Cross-cutting observations at `e8e5d5b3` (the tree this wave judges)

Command: `python3 tools/measure-round81.py --revision e8e5d5b39b25a83f705dc3aa760df21c6a2af508`
(run in a scratch clone; lane tree untouched).

```
count=3 target=6 finding=gate-standard   rc=1
  A-selftest  ok=False rc=0 expected=0 observed=SELFTEST total=2 passed=2 failed=0
  B-met       ok=True  rc=0 expected=0
  C-mismatch  ok=True  rc=1 expected=1
  D-tampered  ok=False rc=1 expected=2
  E-absent    ok=False rc=1 expected=2
  F-noargs    ok=True  rc=2 expected=2
```

Observation: the committed round-80 counter prints `SELFTEST total=2 …`
(`git show e8e5d5b3:tools/measure-round80.py` line 78), while the frozen table
`.ufo/waves/round-81/before/gate-standard-r81.json` expects
`SELFTEST total=6 passed=6 failed=0`; and D/E exit 1 where the table expects 2, i.e. the committed
tool maps could-not-evaluate to "unmet". That is the gate-standard repair the milestone names.
The worktree carries an uncommitted 190-line rewrite of `tools/measure-round80.py`
(`git diff --stat` → `1 file changed, 190 insertions(+), 48 deletions(-)`) whose selftest line is
`total=%d` over `len(cases)`; INFERENCE: the repair exists but is not in the revision the counter
binds, so `--revision` still measures the broken shape. Not my edit; reported, not touched.

Also at `e8e5d5b3`: `count-mount-rows-r81.py --revision …` → `{"count": 0, "finding": "note-absent"}`
rc 1, because `corpus/knowledge/mount-unit-fstab-plane-r81.json` is untracked in the worktree and
absent from the revision. The C1 count at HEAD is therefore not evaluable, not zero.

## Operability

Reproduce from `receipts/` with the pinned bytes as `base/<tool>/<file>` plus a sibling
`_revision.py`:

```
python3 drive.py     # applies each single-clause mutant into mut/<tool>/<id>/, runs --selftest
python3 probe.py     # builds targeted fixtures, runs pristine vs mutant, records divergence
```

Both scripts hard-code `S = /fast/scratch/hyaku/tsukuroi-r81/MutCounter`; change that one line to
re-run elsewhere. Each mutant is exactly one textual clause, and `drive.py` refuses a mutant whose
old-string does not occur exactly once.

## Tooling

No install, no upgrade, no PATH write, no pacman transaction. Python 3.14.8 (`/usr/bin/python3`) and
`git` were already present and sufficient.

## Restoration

Mutants were written only under `mut/<tool>/<id>/`; base copies were never rewritten. Post-run hashes
of the base copies equal the pinned hashes above (`80351a28…`, `0e94c9b4…`, `fc861ec8…`). The scratch
clone's `tools/measure-round81.py` was restored to `0e94c9b4…` after the M03 real-revision probe.
`git status --porcelain` in the lane tree after the run lists the same four pre-existing modified
files and no modification attributable to this seat; the only additions are under
`.ufo/waves/round-81/w1/MutCounter/`. Scratch
`/fast/scratch/hyaku/tsukuroi-r81/MutCounter` is removed before yield — see the removal line in the
final result.

## What this seat does not claim

No verdict on C1 or C2 metness, no change to the counters, no judgement of the sibling lanes'
repairs. A survivor here is a coverage finding, not permission to alter the contract.
