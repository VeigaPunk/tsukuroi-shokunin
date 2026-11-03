# M1Mutation — mutation battery on the round-69 instruments

Seat M1Mutation (mutation-tester), tsukuroi lane round 69, wave w1. Report time
`date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-11-03T23:35:26Z`. Scratch
`/fast/scratch/hyaku/tsukuroi-r69/M1Mutation` (deleted after the receipts were copied out).

Axes named before acting: **depth** (C1 counter: does its clause set actually bind the five
declared evidence clauses?) and **operability** (C2 census KERNEL arm: do its selftest cases bind
the line's five contract behaviours?). Cheap parallel iteration: the counter matrix (9 instruments
× 13 fixtures) ran in one pass; the census battery (5 mutants) ran as one batch of 5 sandbox runs.
Moves kept: any mutation that the declared detector set distinguishes. No lane file was edited.

## 0. Targets and boundary

```
$ sha256sum tsukuroi-shokunin/.ufo/waves/round-69/drafts/c2/count-kr-rows-r69.py
54304628a4fe1523ae519f0a41a82d89f81ef04453c7557a50efa5143dd8bc7d  .../count-kr-rows-r69.py
$ sha256sum tsukuroi-shokunin/.ufo/waves/round-69/drafts/c2/tsukuroi-census.sh
4a6daf43ee9cc701c40625f1e2844fe73b7853973795c0a51b17dd4843b7c36d  .../tsukuroi-census.sh
$ git -C tsukuroi-shokunin rev-parse HEAD   # clone base, before any run
920a9eea3c5c5400567be0e96141014f338973df
$ git -C tsukuroi-shokunin rev-parse HEAD   # at report time (L1 landed + repaired during the wave)
68faae464b60711b0f9ba36169b87e22208ee5ae
```

Read-only on the lane; every mutation is a copy. Sandbox clone:
`$ git clone --shared .../tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r69/M1Mutation/clone`,
`$ git -C <clone> rev-parse --show-toplevel` → `<clone>`, rc 0. Fixture commits were made only in
that clone, with an explicit `-C` and a fixture identity
(`-c user.name=M1Mutation fixture -c user.email=m1mutation@fixture.invalid -c commit.gpgsign=false`).

**Drift disclosed.** The counter draft is byte-identical to the landed `tools/count-kr-rows-r69.py`
(`sha256 54304628…`, checked at report time). The census draft I mutated is the executor's
192-case draft `4a6daf43…`; the landed `tools/tsukuroi-census.sh` was repaired during the wave to
`e191688affc813018659457e0e27ea8de31ef4367bd2eb6a1c30b799c67d031b` (194 cases, pending derivation
as a candidate set). All five census mutation anchors below still exist in the landed bytes
(`grep -c` each anchor → 1), but the verdicts recorded here are measured on the 192-case draft.

## 1. Counter battery (C1 instrument)

Interface read from the draft: `--revision REV --lane REPO --snapshots DIR`, note
`corpus/knowledge/kernel-taint-plane-r69.md` and registry `corpus/SOURCES.md` read via
`git show`, output `KR_ROWS=n KR_VERIFIED=m` + one `KR_ROW <id> ok|fail:<clause>` per row, exit 0
iff rows==verified and verified>=5.

Fixtures: a fixture-only git repo in the clone (`m1-fixtures`, commits recorded in
`fixtures/revisions.json`), registry = `.ufo/waves/round-69/probes/E2Counter/outputs/fixture-SOURCES.md`
(S288, S289), snapshots = copies of the two committed snapshots (`sha256 727ddb82…`, `0556c28f…`,
verified against `before/src/SHA256SUMS`). Notes: E2Counter's control + its five malformed fixtures
(`duplicate`, `digest`, `quote`, `source`, `short`) verbatim, plus seven targeted fixtures
(`x_digest_upper`, `x_digest_prefix`, `x_source_prefix`, `x_quote_superseded`,
`x_snapshot_missing`, `x_nf_extra`, `x_fenced_only`). Commands used per cell:
`python3 <instrument> --revision <fixture sha> --lane $S/clone --snapshots $S/snapshots`.

Eight mutants, one clause each (base `54304628…`; full diffs were the exact string replacements,
re-derived with `diff -u counter.py mutants/mN.py`):

| id | clause removed/loosened |
|---|---|
| m1-unique-id-dropped | deleted the `counts[ident] != 1` branch |
| m2-digest-loose | `[0-9a-f]{64}` → `[0-9a-fA-F]{4,64}` and equality → case-folded prefix match |
| m3-fenced-rows-counted | `unfenced(note)` → `note.splitlines()` in `evaluate` |
| m4-source-prefix | source membership → `any(id.startswith(source))`, digits `{3,}` → `+` |
| m5-quote-any-snapshot | quote looked up in every file of the snapshot dir, not the named one |
| m6-statement-seven | threshold `< 12` → `< 7` |
| m7-snapshot-existence-skipped | `except OSError: clause = "snapshot"` → `pass` (row verifies) |
| m8-cells-not-six | `len(cells) != 6` → `len(cells) < 6` |

Baseline (pristine, same fixtures):

```
$ python3 $S/counter.py --revision b465002b… --lane $S/clone --snapshots $S/snapshots
KR_ROWS=5 KR_VERIFIED=5
KR_ROW KR1 ok … KR_ROW KR5 ok
rc=0
$ (same on the twelve malformed fixtures)  # all rejected
duplicate KR_ROWS=5 KR_VERIFIED=3 fail:unique-id | digest fail:digest | quote fail:quote |
source fail:source | short fail:statement | x_digest_upper fail:digest | x_digest_prefix fail:digest |
x_source_prefix fail:source | x_quote_superseded fail:quote | x_snapshot_missing fail:snapshot |
x_nf_extra fail:cells | x_fenced_only KR_ROWS=0 KR_VERIFIED=0 ; every rc=1
```

Matrix result (`out/matrix.tsv`, 9 instruments × 13 fixtures, 117 runs; acceptance = control
`KR_VERIFIED=5 rc=0` and a malformed fixture `KR_VERIFIED>=5 rc=0`):

| mutant | control | accepted malformed fixtures (declared five) | accepted (added seven) | item verdict |
|---|---|---|---|---|
| m1 | 5/5 rc0 | `duplicate` 5/5 rc0 | none | **survived** |
| m2 | 5/5 rc0 | none | `x_digest_upper`, `x_digest_prefix` 5/5 rc0 | killed |
| m3 | 5/5 rc0 | none | `x_fenced_only` 5/5 rc0 | killed |
| m4 | 5/5 rc0 | none | `x_source_prefix` 5/5 rc0 | killed |
| m5 | 5/5 rc0 | none | `x_quote_superseded` 5/5 rc0 | killed |
| m6 | 5/5 rc0 | `short` 5/5 rc0 | none | **survived** |
| m7 | 5/5 rc0 | none | `x_snapshot_missing` 5/5 rc0 | killed |
| m8 | 5/5 rc0 | none | `x_nf_extra` 5/5 rc0 | killed |

Verdict by the item's rule (survived = control 5 and a declared malformed fixture ≥5):
**8 mutants, 6 killed, 2 survived** (`m1-unique-id-dropped`, `m6-statement-seven`).

Both survivors are **coverage debt of the declared battery, not a hole in the frozen instrument**:

- The instrument prints `fail:unique-id` and `fail:statement` on exactly those fixtures
  (`duplicate` → `KR_ROW KR1 fail:unique-id` twice; `short` → `KR_ROW KR5 fail:statement`), so the
  clauses are bound. The battery records only `KR_ROWS`/`KR_VERIFIED`/rc, and both fixtures use the
  clause's own boundary (a duplicate whose copies are otherwise valid; a statement of exactly 7
  words). A count-only acceptance test cannot distinguish a **widening** mutant: any note the
  pristine counter accepts, the loosened counter also accepts, so no should-fail fixture can make
  it fail. The fix is a fixture-side assertion on the per-row clause word, not a counter change.
- With the seven added targeted fixtures every mutant is distinguished (each added fixture is
  rejected by pristine and accepted by exactly its mutant), i.e. the frozen counter's eight clauses
  are all behaviourally reachable; the two declared-battery gaps are the duplicate-id and
  statement-threshold fixtures.

Restoration: the instrument was never edited in place; the mutated copies live only under
`$S/mutants`. A post-matrix pristine rerun over all 13 fixtures produced byte-identical output to
the pre-matrix baseline (`restored-run mismatches: none`), and
`$ sha256sum counter.py .../drafts/c2/count-kr-rows-r69.py` → both
`54304628a4fe1523ae519f0a41a82d89f81ef04453c7557a50efa5143dd8bc7d`.

## 2. Census arm battery (C2 instrument)

Target: `drafts/c2/tsukuroi-census.sh` `4a6daf43…` (192 selftest cases). Harness:
`$ cp <draft> <clone>/tools/tsukuroi-census.sh && cd <clone> && TMPDIR=$S/tmp bash
tools/tsukuroi-census.sh --selftest`.

Control (draft, before and after):

```
PASS kernel: the emitted line carries every field, in contract order, once (R69-C2)
TSUKUROI_CENSUS_SELFTEST: PASS (192 cases, 192 passed, 0 failed)
rc=0
```

Five mutants, one clause each (each file syntax-checked with `bash -n` first):

| id | mutation | selftest | failing cases |
|---|---|---|---|
| a1-kernel-line-feeds-rollup | after the line: `case $KERNEL_LINE in *' release=UNKNOWN'*) roll=$(worse "$roll" BLOCKED)` | FAIL 192 (188 pass / 4 fail) | 3 healthy KERNEL cases now `exit 2 wanted 0`; neutrality `exit code (1 vs 2)` |
| a2-unreadable-counter-dropped | removed `unr=$((unr + 1))` from the osrelease-unreadable branch | FAIL 192 (191/1) | `kernel-osrelease-unreadable`: expects `unreadable=1` |
| a3-taint-bits-unbounded | deleted the `-gt 1048575` guard (no 0–19 bound) | FAIL 192 (191/1) | `kernel-taint-over`: expects `taint_bits=UNKNOWN detail=tainted:bits-outside-closed-table` |
| a4-pending-default-no | `local pend=UNKNOWN` → `local pend=NO` | FAIL 192 (185/7) | every case with pkg or release UNKNOWN now reads `pending=NO` |
| a5-kernel-line-twice | duplicated the `printf '%s\n' "$KERNEL_LINE"` | FAIL 192 (190/2) | neutrality `exactly one KERNEL line … got 2/2`; line-shape |

Verdict: **5 mutants, 5 killed, 0 survived.** Every mutation is bound by a named `R69-C2` case.
Notably a1 is not caught by the count-only neutrality comparison alone (the neutral fixture is
already DEGRADED) but by the healthy-case exit map and the A/B exit-code comparison; a2, a3, a4, a5
are caught by their specific cases.

Restoration: `$ cp census-draft.sh clone/tools/tsukuroi-census.sh` →
`sha256sum clone/tools/tsukuroi-census.sh census-draft.sh` both
`4a6daf43ee9cc701c40625f1e2844fe73b7853973795c0a51b17dd4843b7c36d`; rerun
`TSUKUROI_CENSUS_SELFTEST: PASS (192 cases, 192 passed, 0 failed)` rc 0.

Anchor transfer check on the landed repair (`e191688a…`, 194 cases): each of the five mutation
anchors is still present once (`grep -c` → 1 for the pend initialiser, the osrelease unreadable
increment, the `-gt 1048575` guard, and the single KERNEL printf; `probe_kernel_arm` → 2
definition+call). The battery was not re-run on those bytes; that is a scope limit, not a pass.

## 3. Findings

1. Both instruments bind their declared behaviours on the bytes they shipped: all eight counter
   clauses are reachable and reject a malformed note when intact; all five arm behaviours are
   covered by selftest cases.
2. Coverage debt (C1 fixture battery): the duplicate-id and 7-word-statement fixtures cannot kill a
   widening mutant under a count-only acceptance check. Either assert the `KR_ROW … fail:<clause>`
   words for those two fixtures, or use an 11-word statement and a duplicate that differs in an
   already-failing cell. Declared predicate unchanged; this is fixture strength, not a claim change.
3. No inconclusive cell: the pristine baseline passed and every mutant produced a decided verdict.
4. The census draft I mutated was superseded in the lane by the 192→194 repair while the wave ran;
   the landed bytes retain every mutation anchor, so the battery is reproducible there, but the
   recorded verdicts belong to `4a6daf43…`.

Post-report drift (observed `2026-11-03T23:37:11Z`): the lane's `tools/tsukuroi-census.sh` is now
`21b0eba3d8ccad1c351720b9b18f63655a231e550a0ad3f566dd9bd6ef37ff46` with an uncommitted
`M tools/tsukuroi-census.sh` (`git diff --stat` 17 insertions, 4 deletions) on HEAD `68faae46`.
That is not my edit and not a byte this battery mutated; the five census verdicts above stay
measured on the executor draft `4a6daf43…`, and the anchor check stays attributed to the
`e191688a…` snapshot taken at `2026-11-03T23:33:03Z`.

FINAL: `M1_COUNTER_MUTANTS=8 M1_COUNTER_KILLED=6 M1_ARM_MUTANTS=5 M1_ARM_KILLED=5 M1_SURVIVORS=m1-unique-id-dropped,m6-statement-seven`
