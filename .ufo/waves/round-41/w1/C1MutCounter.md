VERDICT: defect-found

# C1MutCounter — round 41, item C1-16: mutation-test the C1 counter itself

The six counter mutations were all applied, run and restored in scratch; none of them is caught by
the pre-data C1 controls at the verdict level, and two of them ((a) decoy-check removal, (c) params
-check removal) are demonstrated as real false-PASS holes by paired runs on purpose-built fixtures.
The declared `controls-c1.jsonl` also does not exist. Evidence below; every run's full receipt is in
`.ufo/waves/round-41/w1/C1MutCounter/`.

## 0. Setup and bounds

- Counter under test: `tools/score-selftest-mounts-r41.py`, sha256
  `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c` — verified before the first run
  and re-verified after the last run (identical; the lane file was never written).
- All copies, fixtures and mutants under `/fast/scratch/hyaku/tsukuroi-r41/C1MutCounter/`
  (`TMPDIR` exported there; removed at the end). Receipts kept in
  `.ufo/waves/round-41/w1/C1MutCounter/` (596 KB total, no file near 2 MB).
- No tools were installed (python3 + git only; nothing to record under the 2026-10-19 tooling
  authorization).
- Cost calibration: one `bash census --selftest` in the counter's environment took 31.3 s wall
  (128 cases, `TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)`), so each counter
  run (19 selftest invocations + confirmations) took 42–261 s at `--jobs 4`. All runs serial.

## 1. The declared controls-c1.jsonl does not exist

The item and the declaration cite `.ufo/waves/round-41/controls/controls-c1.jsonl`. The directory
holds instead three per-control files (`C1-K1-declare-f-prologue-on-base.jsonl`,
`C1-K2-candidate-without-H9-case.jsonl`, `C1-K3-declare-f-prologue-on-candidate.jsonl`, each with an
empty `.err`) plus `controls-c2.jsonl` (9 C2 controls). `run_controls.py` prints one JSON line per
control on stdout (run_controls.py:194-197); the C1 aggregate was never collected into the declared
file. Bookkeeping defect, reported as found.

## 2. Fixtures — rebuilt exactly as run_controls.py built them

`run_controls.py` builds each control as a `--shared --no-checkout` clone of the lane at the freeze
revision with one variant census committed on master under the fixture identity, toplevel checked
(run_controls.py:31-45). I imported its `prologue()` and `drop_case()` verbatim
(run_controls.py:63-77) and applied them to the same census texts:

- base census = `git show 0e5805a1f149…:tools/tsukuroi-census.sh` → sha256 `032faa8f…`, byte-equal to
  the census at the counter-freeze revision e479fdc5 (both hashed) — so K1's base text is
  unambiguous;
- candidate census = `git show 568c397da11…:tools/tsukuroi-census.sh` → sha256 `646c84fc…`, equal to
  the census at HEAD 71851d63 and to the pin in `controls/candidate-sha256.txt` — the candidate text
  the controls scored is the census that landed.

| fixture | census text | commit in my clone | census sha256 |
|---|---|---|---|
| fx.K1 | `prologue(base)` | 14e6c0337eadb8de1c8300943d3416c3d5fc31a2 | acdc0414… |
| fx.K2 | `drop_case(candidate,'storage-mounts-no-subvol-opt')` | ce24eb4ee437312d1ebb7f4936f0fb6f6138ba0e | 788628cf… |
| fx.K3 | `prologue(candidate)` | cb81cd0a8e61629fd7d4c21dc7c485f6e032f55d | 2813fb45… |
| fx.demo | candidate + decoy-only self-reader (§5a) | 2c628456c75232b74e5112e2acb2b3653d1cff10 | 1d02977a… |
| fx.democ | candidate + R41_CAP self-reader (§5c) | 2ca3417e20af45fab0741a433bb1711972cdc857 | 02a7b94c… |

Rebuild validation — R1, the pristine counter on rebuilt fx.K1, reproduced the frozen K1 receipt
field-for-field (baseline_pass=1, capture_pass=1, neutral_pass=3, decoy_pass=0, mutants_applied=13,
survivors=13 with the same 13 names, params=0, FAIL/exit 1; receipt `R1-pristine-K1.json`), so the
frozen K2/K3 receipts are valid pristine baselines for my rebuilt fixtures.

Frozen C1 control receipts (the pristine counter's verdicts, from the three jsonl files):

| control | baseline | capture | neutral | decoy | applied | survivors | params | result |
|---|---|---|---|---|---|---|---|---|
| K1 prologue-on-base | 1 | 1 | 3 | 0 | 13 | 13 | 0 | FAIL |
| K2 candidate-without-H9-case | 1 | 1 | 3 | 1 | 13 | 1 (H9) | 3 | FAIL |
| K3 prologue-on-candidate | 1 | 1 | 3 | 0 | 13 | 13 | 4 | FAIL |

## 3. The six mutations (exact sites, before/after hashes)

All edits are single-site replacements on a scratch copy; each replacement's old text occurred
exactly once (asserted by the builder, kept as `build.py` in the seat dir).

| tag | site (tools/score-selftest-mounts-r41.py) | change | copy sha256 |
|---|---|---|---|
| a | :295-296 `ok = (… and decoy_pass == 1 and m_applied …)` | `decoy_pass == 1 and` removed from `ok` | 5fae3293… |
| b | :263-272 confirm block; :287 | confirm phase removed; `row['killed'] = killed(res[name], base)` (the `and bool(…get('confirmed'))` term dropped) | 80987d2d… |
| c | :296 | `and n_params == 4` removed from `ok` | 552b122b… |
| d | :71, :155 | `LABEL_TAIL` definition and its `.sub('')` use removed — PASS labels keep their ` (exit N[, VERDICT])` tail | f46f9ac9… |
| e | :103 | `('H10-count-exactly-one', …)` tuple removed from `MUTANTS` | 878cc41d… |
| f | :255 | `if kind != 'mutant' and not res[name]['pass']:` → `if not res[name]['pass']:` — the serial retry now also re-runs failed mutants | 9bf5fc81… |

## 4. Run table

Every run: `python3 <counter copy> --repo <fixture> --revision <fixture commit> --branch master
--scratch <seat scratch>/work.<tag> --jobs 4`, serial, TMPDIR in the seat scratch. Fields are
(baseline/capture/neutral/decoy/mutants_applied/survivors/params).

| run | counter | fixture | fields | result | wall |
|---|---|---|---|---|---|
| R1 | pristine | fx.K1 | 1/1/3/0/13/13/0 | FAIL | 63 s |
| R2 | (a) | fx.K1 | 1/1/3/0/13/13/0 | FAIL | 63 s |
| R3 | (e) | fx.K3 | 1/1/3/0/12/12/4 | FAIL | 66 s |
| R4 | (d) | fx.K3 | 1/1/3/0/13/13/0 | FAIL | 55 s |
| R5 | (c) | fx.K1 | 1/1/3/0/13/13/0 | FAIL | 57 s |
| R6 | (f) | fx.K1 | 1/1/3/0/13/13/0 | FAIL | 78 s |
| R7 | (b) | fx.K2 | 1/1/3/1/13/1/3 | FAIL | 129 s |
| R8 | pristine | fx.demo | 1/1/3/0/13/0/4 | FAIL | 261 s |
| R9 | (a) | fx.demo | 1/1/3/0/13/0/4 | **PASS, exit 0** | 227 s |
| R10 | pristine | fx.democ | 1/0/3/1/13/0/0 | FAIL | 233 s |
| R11 | (c) | fx.democ | 1/0/3/1/13/0/0 | **PASS, exit 0** | 223 s |
| R12 | (a) | fx.K3 | 1/1/3/0/13/13/4 | FAIL | 42 s |
| R13 | (d) | fx.K2 | 1/1/3/1/13/13/0 | FAIL | 112 s |

## 5. Per-mutation answers

**(a) decoy check removed from `ok` — caught by: NO control.**
R2 (K1) and R12 (K3) are field-identical to the pristine runs (FAIL; `decoy_pass` is still computed
and recorded as 0 — only the predicate term vanished). K2 is a derived no-op (its decoy_pass=1, so
the removed term was true). No control has decoy_pass=0 with survivors=0: on both decoy-failing
controls the prologue also aborts every mutant run, so `survivors=13` still fails `ok`.
Demonstrated hole — R8 vs R9 on the same census (fx.demo): a self-reader whose
`probe_storage_arm` greps its own `declare -f` text for the counter's decoy delimiter `R41DECOY`
(assembled at runtime as `local r41d=R41; r41d+=DECOY`, so the baseline arm never carries the
literal; exact inserted text in the kept `build.py`, `grep_line`; census sha256 `1d02977a…`). On it the pristine counter FAILs solely via the decoy gate
(R8: decoy_pass=0 with survivors=0, params=4 — every mutant killed, all four parameters witnessed);
with the decoy check removed the same census PASSes (R9: exit 0). This is exactly the census class
the decoy gate exists to reject (counter docstring, score-selftest-mounts-r41.py:5-13).

**(b) kill confirmation removed — caught by: NO control.**
R7 (K2) is field-identical to the frozen K2 receipt (survivors=1 H9, params=3, FAIL); it also shows
H9's survival is deterministic (`killed(first)=False`), not an unconfirmed flaky kill. K1/K3 are
derived no-ops (no mutant is ever killed there, so confirmation is structurally idle).
Reachability (analysis, not run): the confirmation is load-bearing against nondeterministic kills —
a census whose selftest fails a baseline label only on some runs (e.g. keyed on its random mktemp
suffix) produces first-run kills that the confirm run does not repeat; the pristine counter then
reports survivors (FAIL) where a confirmation-free counter records a kill and can PASS. All three
controls are deterministic, so they cannot see this.

**(c) params check removed — caught by: NO control.**
R5 (K1) is field-identical to pristine (params is still computed and recorded; only the `ok` term
vanished). K2/K3 derived identical (survivors=1 and 13 respectively still fail `ok`).
Demonstrated hole — R10 vs R11 on the same census (fx.democ): a self-reader that fails only when the
counter's capture env `R41_CAP` is set (exact inserted line in the kept `build.py`, `line`, anchored
at `run_selftest() {`; census sha256 `02a7b94c…`), so the capture run fails and no parameter is
witnessed while baseline, decoy, neutrals and all 13
mutant kills stay clean. Pristine counter: FAIL (capture_pass=0, params=0). Params check removed:
PASS, exit 0. Note the decoy does not carry `R41_CAP` (it carries only the 13 mutants' replacement
texts), so the counter's one self-reader defense misses this census class; the params gate was the
only thing rejecting it. Structural note: for this mutant set `survivors=0` implies the four
witness cases exist (each parameter's witness case is its held-out mutant's killer: P1↔H5
`storage-mounts-mp-relative`, P2↔H6 `storage-mounts-src-uuid`, P3↔H9
`storage-mounts-no-subvol-opt`, P4↔H10 `storage-mounts-two-btrfs`; census:3039-3062), so the params
term is redundant exactly when the capture succeeds — its real load is the capture-failure path,
which no control exercises (all three controls have capture_pass=1).

**(d) LABEL_TAIL removed — caught by: NO control at the verdict level; visible as receipt drift.**
R4 (K3): params 4→0 (tailed baseline labels no longer match the capture's raw labels,
`params_from_capture`'s membership test). R13 (K2): survivors 1→13 and params 3→0 (the tail also
breaks `failed_base_labels`' `fl == lb or fl.startswith(lb + ':')` matching, so no mutant kill is
ever confirmed). Verdicts stay FAIL on all three controls, so the control mechanism does not flag
it; a receipt-diff against the frozen receipts does. This is the one mutation a positive control
would catch by verdict: run_controls.py defines `C1-K4-candidate` (expected PASS) but skips it —
"K0 and K4 duplicate the before and after receipts" (run_controls.py:186-188) — and on K4, (d)
flips PASS→FAIL.

**(e) H10 dropped from MUTANTS — caught by: NO control at the verdict level; visible as receipt
drift.**
R3 (K3): mutants_applied 13→12, survivors 13→12 (H10 gone from survivor_names), FAIL unchanged. K1
mirrors K3 and K2 shows mutants_applied 13→12 with survivors still 1 (derived). Structural: the
predicate tests `m_applied == len(MUTANTS)` (score-selftest-mounts-r41.py:296), so the counter
redefines its own threshold when the list shrinks — no fixture can catch (e) by verdict; the count
13 is pinned only by the declaration and the frozen receipts. (e) also cannot produce a false PASS
via survivors: params=4 forces the four held-out killers to exist, and P4's witness is H10's killer.

**(f) retry applied to mutants too — caught by: NO control.**
R6 (K1): verdict and every projected field identical to pristine; the only trace is `retried` on all
13 mutant rows (first_last = the prologue's `FAIL (1 cases, 0 passed, 1 failed)` summary) — a field
the controls' projection (run_controls.py:194-196 keep-list) does not record. K2/K3 derived same
verdict (K2's 12 killed mutants would each gain a serial retry; deterministic failures keep the
kill). Reachability (analysis, not run): the retry keeps the second verdict, so a flaky kill is
undone (false-FAIL direction); and because a kill then requires the retry and confirm runs to share
labels, a census whose failing label drifts between runs can be killed under (f) where the pristine
counter spares it (first∩confirm = ∅ but retry∩confirm ≠ ∅) — a false-PASS direction. Both need
nondeterministic fixtures; deterministic controls cannot see either.

## 6. Which mutant of the counter no control catches

All six, at the verdict level. At the recorded-field level: (d) and (e) drift visibly on the
controls (K3/K2 params and survivors; applied-count), (f) drifts only in per-mutant `retried`
fields the control projection drops, and (a), (b), (c) are invisible even in the full receipt.
(a) and (c) are demonstrated as real false-PASS holes by runs (R8/R9, R10/R11); (b), (e), (f) are
argued with the field evidence above.

Root cause: the C1 control set is all-negative — every fixture must FAIL — so any counter mutation
that keeps failing those fixtures for any reason is invisible to the control mechanism; the
predicate's thresholds are self-referential (`len(NEUTRAL)`, `len(MUTANTS)`); and the three gates
whose removal was tested (decoy, confirmation, params) are never the deciding term on K1-K3. The
positive control C1-K4-candidate exists in run_controls.py but was skipped as duplicating the after
receipt; even K4 would catch only (d) by verdict (and (e) by receipt-diff). Controls that would
close the gaps: a decoy-isolating negative control (fx.demo shape), a capture-isolating negative
control (fx.democ shape), a positive control (K4), and — for (b)/(f) — a nondeterministic control.

## 7. Not done

- No full frozen-counter run on the lane itself (not this item's surface; before/after receipts are
  other seats' items).
- No adversarial-census demonstrations for (b) and (f): they need nondeterministic fixtures; the
  reachability arguments above are analysis, not runs, and are marked as such.
- Control cells not re-scored (derived from the code plus frozen receipts, each a structural no-op
  or a mirror of an executed cell): a×K2, b×K1, b×K3, c×K2, c×K3, d×K1, e×K1, e×K2, f×K2, f×K3.

## 8. Restoration evidence

- Lane counter re-hashed after all runs:
  `sha256sum tools/score-selftest-mounts-r41.py` →
  `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c` — identical to the frozen
  declaration; the lane file was never written.
- The mutated copies live only in scratch and as seat-dir receipts
  (`.ufo/waves/round-41/w1/C1MutCounter/counter-{pristine,a,b,c,d,e,f}.py`, plus `build.py` and
  `fixtures.sh` for reproduction). The variant censuses are not copied into the seat dir (census
  rule); their sha256s and the builder script reproduce them from the pinned revisions.
- Scratch `/fast/scratch/hyaku/tsukuroi-r41/C1MutCounter/` removed after the receipts were copied.
