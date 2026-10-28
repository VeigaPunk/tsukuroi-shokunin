VERDICT: supports

# R49MutCounterA — C1-B5: mutation test of `tools/check-scrub-admission-r49.py`

Seat: R49MutCounterA (leaf, EXEC-AUTHORIZED). Item C1-B5: four single-site mutants of the
frozen C1 counter, each run against a synthetic K-pass fixture set and against the defect set
it lets through.

Frozen counter under test (read from the lane, never written):
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:tools/check-scrub-admission-r49.py`
sha256 `3dd52ef376e233192f955208c1132f6b0d23bbebe97dd1df75e6296f55d970a4` — identical to the lane
worktree copy (same sha256, measured), so the working tree was not the variable.

Receipts: `.ufo/waves/round-49/w1/R49MutCounterA/` (matrix.txt, fieldlevel.txt, mutants.diff,
baseline.jsonl, run.M{1,2,3,4}.jsonl, run.ID.jsonl, sets.json, hashes.txt, the four mutant
files, the harness scripts).

## 1. Fixture set (synthetic, 17 sets)

One generator, `build_fx.py`, derives every set from the frozen bytes:

- entry: freeze `corpus/knowledge/btrfs-scrub-grounding-r45.md` + the C1 mark line
  `## Gate status — round 49 (GR1-GR3 admitted)`; SKILL.md + `## Scrub grounding — round 49 admission`;
  corpus/README.md + the admission sentence. Row hashes recomputed by the counter itself are
  GR1 `3a2ba180…43fee1`, GR2 `d4296085…bd027f`, GR3 `43430a14…4bbc32c` — the three values the
  frozen claim C1 names, so the fixture entry carries the same rows the claim does.
- cohort: the 18 reports `R49{Rev,Crit}GR{1,2,3}{a,b,c}.md`, each `ROW GR<n> VERDICT: holds` /
  `SECTION SHA256: <row hash>` / a body of 575-581 bytes (file 679-685 bytes) citing
  `cmdline.c:147`, `dev-replace.c:700` or `scrub.c:3094` (lines that resolve in the pinned
  snapshots), 18 distinct bodies.
- results/deps: `w1-results.json` with 18 completed entries; `w1-dispatch.json` (18 names,
  reviewer/critic) and the 11 digest-pinned snapshot files live in a synthetic fixture git repo
  `/fast/scratch/…/fx.g5UDwV` (HEAD `df24a434471fcab78c73fead236e2406321aa13d`), created with
  `git init` inside `$D` after `git rev-parse --show-toplevel` printed `$D`; all commits carry
  `-c user.name=fixture -c user.email=fixture@invalid`. The counter is run with `--lane $FXDIR
  --revision $FXHEAD` and the `--entry-file/--skill-file/--readme-file/--wave-dir/--results-file
  `--no-base-check` overrides, i.e. exactly the control-battery path
  (`controls/battery.py:133-135`), not production bytes.

Per-set deltas are scoped by content hash (measured, `build_fx.py` output):
`clean` none; `d1-*`/`d2`/`d5` one or two report files; `d3*` results.json only; `d4*` report
hash lines only. Every non-clean set differs from `clean` in nothing else.

Execution command (one run per counter per set; `run_sets.py`):

```
python3 run_sets.py <counter>.py
  -> python3 <counter>.py --revision $FXHEAD --no-base-check --lane $FXDIR \
       --entry-file sets/<set>/entry.md --skill-file sets/<set>/skill.md \
       --readme-file sets/<set>/readme.md --wave-dir sets/<set>/w1 \
       --results-file sets/<set>/results.json
```

## 2. Baseline: the pristine counter on the fixture set

Observed (`baseline.jsonl`, re-run twice — byte-identical, deterministic):

| set | verdict | rc | s/c/q/v/seats/m |
|---|---|---|---|
| clean (K-pass) | PASS | 0 | 1 1 3 3 18 3 |
| d1-partly | FAIL | 1 | 1 1 3 **2** 18 3 |
| d1b-fails | FAIL | 1 | 1 1 3 2 18 3 |
| d1c-contradict | FAIL | 1 | 1 1 3 2 18 3 |
| d2-dupbodies | FAIL | 1 | 1 1 3 2 18 3 |
| d3-noresults | FAIL | 1 | 1 1 3 3 **17** 3 |
| d3b-emptyresults | FAIL | 1 | 1 1 3 **0** **0** 3 |
| d3c-emptyoutput | FAIL | 1 | 1 1 3 3 17 3 |
| d3d-wrongrole | FAIL | 1 | 1 1 3 3 17 3 |
| d3e-dupentry | FAIL | 1 | 1 1 3 3 17 3 |
| d4-badhash (1 of 6) | PASS | 0 | 1 1 3 3 18 3 |
| d4c-badhash-3of6 | PASS | 0 | 1 1 3 3 18 3 |
| d4d-badhash-4of6 | FAIL | 1 | 1 1 3 2 18 3 |
| d4e-crossrow (4 of 6, GR2's hash) | FAIL | 1 | 1 1 3 2 18 3 |
| d4b-badhash-all (6 of 6) | FAIL | 1 | 1 1 3 2 18 3 |
| d4f-margin-3of6-allrows | PASS | 0 | 1 1 3 3 18 3 |
| d5-prose-partly | PASS | 0 | 1 1 3 3 18 3 |

The pristine counter is PASS on `clean` and FAIL on every set that carries the defect class the
mutant below removes, so the baseline failure mode of a detector is pinned to the fixture, not
to the mutant.

## 3. Mutants (single-site each; unified diffs in `mutants.diff`)

All four are one textual hunk of the frozen file, produced by `make_mutants.py` which asserts the
old text occurs exactly once; the pristine file is never modified (hashes in §5).

| id | site in the frozen counter | mutation | sha256 |
|---|---|---|---|
| M1 | `check-scrub-admission-r49.py:379` | drop `and not blocking` from `row_ok` (A2 blocking rule gone) | `db73f3f6…b52940` |
| M2 | `:379` | drop `and distinct` from `row_ok` (distinct-bodies check gone) | `2c249eff…9cc8e95a` |
| M3 | `:275-281` | delete the `hits`/`exactly one results entry`/`results agent`/`no completed output` block in `bind_seat` (results.json seat check gone) | `035e858b…e3818ded15` |
| M4 | `:367-369` | replace `if h != hashes.get(row)` with `if hashes.get(row) is None` (any 64-hex accepted; `HASH_RE` at `:91` still enforces the 64-hex shape) | `805886e5…b7368714f` |
| ID | — | identity control: frozen file + one trailing comment | `abadeec1…d7f6d3f2773` |

Result matrix (`matrix.txt`; PASS/FAIL as printed by each counter, 17 sets × 5 binaries):

```
set                        orig  M1    M2    M3    M4
clean                      PASS  PASS  PASS  PASS  PASS
d1-partly                  FAIL  PASS  FAIL  FAIL  FAIL
d1b-fails                  FAIL  PASS  FAIL  FAIL  FAIL
d1c-contradict             FAIL  PASS  FAIL  FAIL  FAIL
d2-dupbodies               FAIL  FAIL  PASS  FAIL  FAIL
d3-noresults               FAIL  FAIL  FAIL  PASS  FAIL
d4-badhash                 PASS  PASS  PASS  PASS  PASS
d4b-badhash-all            FAIL  FAIL  FAIL  FAIL  PASS
d3b-emptyresults           FAIL  FAIL  FAIL  PASS  FAIL
d4c-badhash-3of6           PASS  PASS  PASS  PASS  PASS
d4d-badhash-4of6           FAIL  FAIL  FAIL  FAIL  PASS
d5-prose-partly            PASS  PASS  PASS  PASS  PASS
d3c-emptyoutput            FAIL  FAIL  FAIL  PASS  FAIL
d3d-wrongrole              FAIL  FAIL  FAIL  PASS  FAIL
d3e-dupentry               FAIL  FAIL  FAIL  PASS  FAIL
d4e-crossrow               FAIL  FAIL  FAIL  FAIL  PASS
d4f-margin-3of6-allrows    PASS  PASS  PASS  PASS  PASS
```

Identity control: `run.ID.jsonl` equals `baseline.jsonl` on all 17 sets once the `counter` path
field is normalised (measured `identical: True`), so the harness produces no differences of its
own.

### M1 — A2 blocking rule dropped — SURVIVED on its own defect, killed elsewhere

Expected detector: a bound seat whose first line is `partly` (or `fails`, or a contradicting
`ROW GR<n> VERDICT:` line in the body) must block its row. Output:

- `d1-partly` (one seat `R49CritGR2b` = `partly`): orig **FAIL** rc 1, `verdicts_ok 2`, GR2
  `blocking ['R49CritGR2b'] row_ok False`; M1 **PASS** rc 0, `verdicts_ok 3`, GR2
  `blocking ['R49CritGR2b'] row_ok True` — the seat is still recorded as blocking but the rule
  that consumes it is gone, so the row is credited anyway.
- `d1b-fails` (`R49RevGR3a` = `fails`): orig FAIL (`verdicts_ok 2`) → M1 PASS (`3`).
- `d1c-contradict` (first line `holds`, body line `ROW GR1 VERDICT: partly`): orig FAIL (`2`) →
  M1 PASS (`3`).
- Every other defect set: M1 = orig (FAIL) — no cross-contamination.

### M2 — distinct-bodies check dropped — SURVIVED on its own defect, killed elsewhere

- `d2-dupbodies` (GR1's `R49RevGR1a` and `R49RevGR1b` carry byte-identical bodies): orig
  **FAIL** rc 1, `verdicts_ok 2`, GR1 `distinct_bodies false row_ok False`; M2 **PASS** rc 0,
  `verdicts_ok 3`, GR1 `distinct_bodies false row_ok True`. All other sets unchanged.

### M3 — results.json seat check dropped — SURVIVED on its own defect, killed elsewhere

- `d3b-emptyresults` (results.json carries no seat at all; strongest form): orig **FAIL** rc 1,
  `seats_ok 0`, `verdicts_ok 0`, every seat `unbound (not exactly one results entry)`; M3
  **PASS** rc 0, `seats_ok 18`, `verdicts_ok 3` — the report files alone bind the cohort.
- `d3-noresults` (one entry missing): orig FAIL `seats_ok 17` → M3 PASS `18`.
- `d3c-emptyoutput` (entry present, `output: ""`): orig FAIL `17` → M3 PASS `18`.
- `d3d-wrongrole` (results agent `reviewer` for a critic seat): orig FAIL `17` → M3 PASS `18`.
- `d3e-dupentry` (same seat twice): orig FAIL `17` → M3 PASS `18`.
- All other sets: M3 = orig.

### M4 — any 64-hex hash accepted — SURVIVED on its own defect, killed elsewhere

- `d4b-badhash-all` (all six GR3 reports carry `f`×64): orig **FAIL** rc 1, `verdicts_ok 2`,
  GR3 `credited 0`; M4 **PASS** rc 0, GR3 `credited 6`.
- `d4d-badhash-4of6`: orig FAIL (`credited 2` → row_ok False) → M4 PASS (`credited 6`).
- `d4e-crossrow` (four GR1 seats carry GR2's *correct* hash): orig FAIL → M4 PASS.
- All other sets: M4 = orig; in particular M4 still FAILs `d1*`, `d2`, `d3*`.

## 4. Readings the L1 should carry

1. **All four checks are load-bearing and singly detected.** Each mutant escapes exactly the
   fixture family that carries its defect and nothing else (rows above: the off-diagonal is
   always `mutant = orig`). By the item's own label each is therefore a *surviving* mutant on
   its defect fixture (original FAIL → mutant PASS), which is the property the fixture pair was
   built to show: no other rule in the counter substitutes for the one removed.
2. **Coverage observation (not a claim defect): the credit floor tolerates a partially
   mis-read cohort.** `d4f-margin-3of6-allrows` — three of the six seats in *every* row declare
   `f`×64 instead of the row hash, and the pristine counter still prints
   `PASS rc 0, s/c/q/v/seats/m = 1 1 3 3 18 3` with `credited 3` per row and 9 notes. Cause:
   `seats_ok` counts every *bound* seat (`run():383`: `sum(1 for s in seats.values() if
   s['verdict'] is not None)`) while `verdicts_ok` only needs `>= 3` credited seats per row, so
   `seats_ok == 18` does **not** imply 18 seats hashed the corrected row. Same mechanism makes
   `d4-badhash` (1 of 6) and `d4c-badhash-3of6` PASS. The frozen predicate permits this, so it is
   reported, not scored as a defect; a future claim that wants "all 18 read the corrected bytes"
   needs a different leg.
3. **The C1 predicate cannot pass at the freeze revision itself** — measured, twice:
   `--revision 55c07cd…` → `FAIL`, `seats_ok 0`, `verdicts_ok 0`, notes
   `dispatch agent None != reviewer` (no `w1-dispatch.json` in the freeze commit); at the later
   `32a8556…` → `FAIL`, `seats_ok 0`, notes `not exactly one results entry` (dispatch present,
   no `w1-results.json`). The claim's `--revision <REV>` must name a revision that carries the
   w1 reports *and* `w1-results.json`, not the freeze commit. `structural_ok 1`, `corr_ok 1`,
   `quotes_ok 3` held at both revisions, and the row hashes were the frozen three.
4. **Minor usability note:** `--section-hash` with only `--entry-file` exits 2 with
   `{"error": "entry/SKILL/README unreadable"}` — the flag still requires the SKILL/README
   overrides (or a lane whose revision has them). The control battery passes all three, which is
   why it did not surface there.
5. **A2 is first-line/`ROW GR<n> VERDICT:`-line only** (`bind_seat`, `ANY_VERDICT_RE` at `:90`):
   `d5-prose-partly` — a body that says the row is "partly correct" in prose — PASSes on the
   pristine counter. Consistent with the documented rule ("a report whose first line says
   partly/fails"), noted only.

No mutant survived on the K-pass set (all five binaries PASS `clean` rc 0), so no mutant is
detected by valid traffic; no baseline run of a detector was inconclusive.

## 5. Restoration evidence

The frozen counter and the lane were never written. The frozen bytes were extracted with
`git show … >` into scratch, mutated only into separate scratch copies, and re-hashed after all
runs:

```
3dd52ef376e233192f955208c1132f6b0d23bbebe97dd1df75e6296f55d970a4  scratch counter.orig.py
3dd52ef376e233192f955208c1132f6b0d23bbebe97dd1df75e6296f55d970a4  lane blob 55c07cd:tools/check-scrub-admission-r49.py
3dd52ef376e233192f955208c1132f6b0d23bbebe97dd1df75e6296f55d970a4  lane worktree tools/check-scrub-admission-r49.py
```
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain=v1 tools/check-scrub-admission-r49.py`
printed nothing. Mutant hashes are in §3 / `hashes.txt`; the fixture repo's HEAD and path are in
`hashes.txt`. Scratch (`/fast/scratch/hyaku/tsukuroi-r49/R49MutCounterA`, including `fx.g5UDwV`)
is removed after the receipts were copied.

## 6. What I did not do

No installs (nothing needed; no pacman transaction attempted). I did not run the C1 counter's
`--selftest` path (the counter has none) or the census. I did not build a mutant for the
quotes/structural/corr/marks legs — the item names M1-M4 only. I did not test production
(`--lane` = the real lane) success of the C1 predicate, because the w1 cohort files are not
committed at any revision I was authorised to observe; item 3 above is the observed state.
