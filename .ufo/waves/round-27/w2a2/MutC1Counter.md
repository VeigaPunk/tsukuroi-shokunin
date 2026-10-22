# MutC1Counter — mutation probe of the C1 counter (round 27, attempt 2, wave 2)

Verdict: partly holds. The C1 counter `tools/check-kernel-taint.py` at revision
099c7b3f42d073203d9448807860f04c175eccd7 is well guarded: 27 of 30 single rule mutants were killed
by the bounded detector, and all three combined duplicate-refusal probes were killed. Three mutants
survived. Two of them are masked duplicate-refusal guards, and one is a genuine coverage gap: the
capture-token minimum-length rule is never exercised by the selftest, and whitespace normalisation is
exercised by the lane data but not by the selftest.

## 1. What was attacked and how

1.1 [obs] The tool under attack is `tools/check-kernel-taint.py` at revision
099c7b3f42d073203d9448807860f04c175eccd7, exported read-only to
`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/tree`. The exported file hashes to
sha256 `bd307d33bd9d4960f2dd1dcf7f0921534937e98c9d4b5769fed0097da3c6e23a`
(`sha256sum /fast/scratch/hyaku/tsuku27a2/MutC1Counter/tree/tools/check-kernel-taint.py`, exit 0).

1.2 [obs] The bounded detector is the same two commands for every probe, in this order:
`python3 tools/check-kernel-taint.py --selftest` and
`python3 tools/check-kernel-taint.py --revision 099c7b3f42d073203d9448807860f04c175eccd7 --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
The revision half reads the lane repository through `--repo` only; no write command was run against
the lane.

1.3 [obs] A mutant is called killed when the selftest exits non-zero, or when the revision run exits
non-zero, or when `verified_rows` differs from 6. A mutant that leaves the selftest at exit 0 and the
revision run at exit 0 with `verified_rows` 6 is called survived.

1.4 [obs] Each mutant was applied to its own copy of the tool under
`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/mutants/<id>/`; the pristine bytes were rewritten after
every probe and the rewritten bytes were hashed and compared with the pristine hash. The harness is
`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/harness.py`, the mutant list is
`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/mutants.json`, the machine-readable results are
`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/results.json` and
`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/results-combined.json`.

## 2. Baseline on pristine bytes

2.1 [obs] Pristine baseline: selftest exit 0, status PASS, 46 cases, 0 failed; revision exit 0,
status PASS, `verified_rows` 6, no blocking findings
(`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/baseline.json`).

2.2 [obs] The baseline is therefore a valid reference: a mutant that fails to change either detector
is a real survivor, not a broken baseline.

## 3. The thirty single rule mutants

Line numbers are the pristine file `/fast/scratch/hyaku/tsuku27a2/MutC1Counter/tree/tools/check-kernel-taint.py`.
"st failed" is the number of selftest cases that failed; "cases" lists the first failing case names.

3.1 [obs] M01, line 65, exact id set drops KT6 from `ROW_IDS`. Killed: selftest exit 1 with 35 failing
cases (including `clean-pass`), revision exit 1, `verified_rows` 0.

3.2 [obs] M02, line 793, the `seen != set(ROW_IDS)` check never fires. Killed: selftest exit 1 with 1
failing case (`duplicate-row-id`); the revision run stayed at exit 0 and 6 rows. This check is only
observable through the selftest, because the lane entry carries all six ids.

3.3 [obs] M03, line 584, `count == 1` becomes `count >= 1` so a duplicated id is no longer withdrawn
from the countable set. Survived: selftest exit 0 with 0 failed cases, revision exit 0, 6 rows.

3.4 [obs] M04, line 586, the global duplicate block never fires. Killed: selftest exit 1 with 1
failing case (`duplicate-row-id-seven-rows`); revision exit 0, 6 rows.

3.5 [obs] M05, line 607, the row-level duplicate refusal `elif counts.get(row_id, 0) > 1` never fires.
Survived: selftest exit 0 with 0 failed cases, revision exit 0, 6 rows.

3.6 [obs] M06, line 69, the verdict vocabulary is widened with lowercase `healthy`. Killed: selftest
exit 1, 1 failing case (`verdict-invalid`); revision exit 0, 6 rows.

3.7 [obs] M07, line 621, the verdict vocabulary check never fires. Killed: selftest exit 1, 1 failing
case (`verdict-invalid`); revision exit 0, 6 rows.

3.8 [obs] M08, line 648, the mined-status check never fires. Killed: selftest exit 1, 1 failing case
(`source-not-mined`); revision exit 0, 6 rows.

3.9 [obs] M09, line 650, the opened-date check never fires. Killed: selftest exit 1, 1 failing case
(`source-opened-wrong`); revision exit 0, 6 rows.

3.10 [obs] M10, line 652, the used-by check never fires. Killed: selftest exit 1, 1 failing case
(`source-used-by-missing`); revision exit 0, 6 rows.

3.11 [obs] M11, line 660, the tier-A requirement never fires. Killed: selftest exit 1, 1 failing case
(`source-no-tier-a`); revision exit 0, 6 rows.

3.12 [obs] M12, line 647, tier-A detection accepts tier B instead of tier A. Killed: selftest exit 1
with 39 failing cases, revision exit 1, `verified_rows` 0. The lane entry relies on tier A, so this
mutant is caught by both halves of the detector.

3.13 [obs] M13, line 67, `MAX_QUOTE_WORDS` raised from 25 to 1000. Killed: selftest exit 1, 1 failing
case (`quote-too-long`); revision exit 0, 6 rows.

3.14 [obs] M14, line 694, the quote length check always passes. Killed: selftest exit 1, 1 failing
case (`quote-too-long`); revision exit 0, 6 rows.

3.15 [obs] M15, line 95, whitespace normalisation removed (`norm` returns the raw text). Killed by the
revision half only: selftest exit 0 with 0 failed cases, revision exit 1 with `verified_rows` 3.
Rows KT1, KT3 and KT6 fail with `KT-QUOTE-NOT-IN-SNAPSHOT`; KT2, KT4 and KT5 still verify.

3.16 [obs] M16, line 707, the snapshot sha256 versus anchor cell check never fires. Killed: selftest
exit 1, 1 failing case (`snapshot-digest-not-in-anchor`); revision exit 0, 6 rows.

3.17 [obs] M17, line 344, the Gate quote column header match is narrowed to the exact name `quote`,
so the `Located quote` header is no longer found. Killed: selftest exit 1 with 38 failing cases,
revision exit 1, `verified_rows` 0.

3.18 [obs] M18, line 216, the Gate cell is read one column to the left of the header position, which
reintroduces the round-26 defect R26-GATE-COLUMN-OFFSET. Killed: selftest exit 1 with 38 failing
cases, revision exit 1, `verified_rows` 0.

3.19 [obs] M19, line 719, the Gate quote equality is weakened from equality to substring. Killed:
selftest exit 1, 1 failing case (`gate-two-quotes-one-cell`); revision exit 0, 6 rows.

3.20 [obs] M20, line 719, the Gate quote equality is dropped and only the presence of a Gate quote for
the source is required. Killed: selftest exit 1 with 4 failing cases (`gate-quote-with-pipe`,
`gate-two-quotes-one-cell`, `gate-cell-wrong-column`, `gate-cell-offset-date`); revision exit 0,
6 rows.

3.21 [obs] M21, line 494, the capture sha256 pin check never fires. Killed: selftest exit 1, 1 failing
case (`capture-digest-changed`); revision exit 0, 6 rows.

3.22 [obs] M22, line 570, the entry's own declared capture digest is never checked. Killed: selftest
exit 1, 1 failing case (`declared-capture-digest-mismatch`); revision exit 0, 6 rows.

3.23 [obs] M23, line 711, the quote-in-snapshot check always passes. Killed: selftest exit 1, 1
failing case (`quote-not-in-snapshot`); revision exit 0, 6 rows.

3.24 [obs] M24, line 382, any `## ` heading in SKILL.md is accepted as the kernel-taint section.
Killed: selftest exit 1, 1 failing case (`skill-section-missing`); revision exit 1,
`verified_rows` 0.

3.25 [obs] M25, line 743, the SKILL.md row check accepts any row id. Killed: selftest exit 1 with 3
failing cases (`skill-row-missing`, `skill-row-outside-section`, `skill-section-missing`); revision
exit 0, 6 rows.

3.26 [obs] M26, line 459, the capture line uniqueness check never fires. Killed: selftest exit 1 with
2 failing cases (`pointer-on-exit`, `pointer-on-duplicate-line`); revision exit 0, 6 rows.

3.27 [obs] M27, line 445, the capture token minimum length check never fires. Survived: selftest
exit 0 with 0 failed cases, revision exit 0, 6 rows.

3.28 [obs] M28, line 739, a row with no usable capture pointer still passes. Killed: selftest exit 1
with 4 failing cases (`pointer-on-header`, `pointer-on-echo`, `pointer-on-exit`,
`pointer-on-duplicate-line`); revision exit 0, 6 rows.

3.29 [obs] M29, line 730, the capture pointer presence check never fires. Killed: selftest exit 1, 1
failing case (`capture-pointer-missing`). The mutant makes the tool raise a `TypeError` while
iterating a missing pointer list, so it dies by crash rather than by a clean finding.

3.30 [obs] M30, line 342, the Gate source column header match is narrowed to `source `, so the `Source`
header is no longer found. Killed: selftest exit 1 with 38 failing cases, revision exit 1,
`verified_rows` 0.

## 4. Survivor 1: M03, the countable-set withdrawal of a duplicated id

4.1 [obs] M03 removes the condition at line 584 that withdraws an id which appears more than once from
`counted`. Both detectors pass: the selftest exits 0 with 0 failed cases and the revision run exits 0
with 6 rows (`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/results.json`, entry `M03`).

4.2 [inf] The reason is masking, not dead code: the global duplicate block at line 586 sets
`global_blocked`, and `verified_rows` is forced to 0 whenever `global_blocked` is true, so the
countable set never influences the result while that block stands.

4.3 [obs] The masking was confirmed by probe C01, which removes M03 and M04 together. C01 is killed:
selftest exit 1 with 1 failing case (`duplicate-row-id-seven-rows`)
(`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/results-combined.json`, entry `C01`).

4.4 [obs] The selftest case that would kill M03 on its own does not exist. A new case is needed: an
entry whose seven rows repeat KT1 once, where the expectation is `verified_rows` 0 and the finding
`KT-ROW-ID-DUPLICATE`, with the global block at line 586 left in place but the guard at line 584
removed. The existing case `duplicate-row-id-seven-rows` expects exactly that outcome and passes
under M03 because the global block still fires.

## 5. Survivor 2: M05, the row-level refusal of a duplicated id

5.1 [obs] M05 removes the condition at line 607 that makes a row carrying a duplicated id fail. Both
detectors pass: selftest exit 0 with 0 failed cases, revision exit 0, 6 rows.

5.2 [inf] The row-level refusal is likewise masked by the global duplicate block at line 586.

5.3 [obs] Probe C02 removes M04 and M05 together and is killed: selftest exit 1 with 2 failing cases
(`duplicate-row-id`, `duplicate-row-id-seven-rows`). Probe C03 removes M03, M04 and M05 together and is
killed the same way with the same 2 failing cases
(`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/results-combined.json`).

5.4 [obs] The selftest case that would kill M05 on its own does not exist. A new case is needed: an
entry that repeats KT1 as a second row, where the repeated row must be reported as failed with the
finding `KT-ROW-ID-DUPLICATE` on that row, checked with the row-level refusal removed and the
global block left in place.

## 6. Survivor 3: M27, the capture token minimum length

6.1 [obs] M27 removes the condition at line 445 that rejects a capture pointer whose token is shorter
than three characters. Both detectors pass: selftest exit 0 with 0 failed cases, revision exit 0,
6 rows.

6.2 [obs] This is a real coverage gap, not masking. Every selftest fixture uses the token
`write_errs 0` (eleven characters) and no lane pointer carries a token shorter than three characters,
so the finding `KT-CAPTURE-POINTER-TOKEN-SHORT` is never produced by any current case.

6.3 [obs] The selftest case that would kill M27 was checked against the pristine tool before being
proposed, so the proposal is not vacuous. A case whose KT1 capture pointer is
`{'line': 6, 'token': 'wr'}` on the unique capture line `write_errs 0` gives, on the pristine tool,
exit 1, `verified_rows` 5 and the findings `KT-CAPTURE-POINTER-TOKEN-SHORT` and
`KT-CAPTURE-POINTER-UNUSABLE`
(`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/probe.py`, output line `PRISTINE proposed M27 case ->`,
exit 0). Under M27 the `KT-CAPTURE-POINTER-TOKEN-SHORT` finding disappears, so that case fails and
kills the mutant.

## 7. Selftest coverage gap found by the revision half of the detector

7.1 [obs] M15 removes whitespace normalisation at line 95. The selftest passes unchanged, exit 0 with
0 failed cases, while the revision run over the lane data drops to exit 1 with `verified_rows` 3, and
KT1, KT3 and KT6 fail with `KT-QUOTE-NOT-IN-SNAPSHOT`
(`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/probe.py`, second probe, exit 0).

7.2 [inf] The lane quotes and the lane snapshot bytes differ only in whitespace for those three rows,
so the normalisation at line 95 carries real weight on the committed data while no selftest case
depends on it.

7.3 [obs] The selftest case that would kill M15 does not exist. A new case is needed: a snapshot whose
quote text carries a double space where the entry quote and the Gate cell carry one space. That case
was checked against the pristine tool before being proposed: it gives exit 0, `verified_rows` 6 and no
findings on the pristine tool, because the normalisation at line 95 collapses the double space, and it
gives exit 1, `verified_rows` 5 with the finding `KT-QUOTE-NOT-IN-SNAPSHOT` under M15
(command shown in finding 6.3 with the snapshot quote `the btrfs  device error counters are cumulative
per device` and the entry and Gate quote `the btrfs device error counters are cumulative per device`,
exit 0).

7.4 [obs] By contrast, the lane data does exercise the tier-A rule (M12), both Gate column rules
(M17, M18, M30), the SKILL.md section rule (M24) and the whitespace rule (M15): each of these mutants
also changed the revision count, so those conditions are load-bearing on the committed bytes.

## 8. Restoration evidence

8.1 [obs] The pristine bytes were restored after every probe and hashed. After all thirty single
mutants and the three combined probes, the tool under the export hashes to
`bd307d33bd9d4960f2dd1dcf7f0921534937e98c9d4b5769fed0097da3c6e23a`, identical to the hash taken
before any mutation
(`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/results.json`, keys `pristine_sha256` and
`restored_sha256`; every mutant record carries `restored_sha` equal to `sha256_pristine`).

8.2 [obs] A fresh read-only export of the same revision was taken after the whole run and compared
with the working export: `diff -r` reported no difference and the tool hash was unchanged
(`/fast/scratch/hyaku/tsuku27a2/MutC1Counter/verify-export`, exit 0).

8.3 [obs] The lane repository was never written to. `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain`
lists only the untracked report files of other seats, and the lane HEAD was
`2e519d615135ba3b3d60dcd19a5642dc0d4391f9` after the run. The revision under attack,
099c7b3f42d073203d9448807860f04c175eccd7, was bound explicitly by every revision run.

8.4 [obs] The restored bytes were exercised once more after the whole run, from the export: the
selftest returned status PASS with 46 cases and 0 failed, the revision run returned status PASS with
`verified_rows` 6, and the tool still hashes to
`bd307d33bd9d4960f2dd1dcf7f0921534937e98c9d4b5769fed0097da3c6e23a`.

## 9. Scope of this probe

9.1 [obs] This probe attacks the detection strength of one tool. It says nothing about whether the
C1 entry's claims are true, and it does not propose any change to the contract of the counter.

9.2 [obs] Whether the three survivors should be closed by adding selftest cases or by changing the
tool is a decision for the integrator. The proposed selftest cases in findings 6.3 and 7.3 were
checked against the pristine tool and are known to be non-vacuous; the two cases in findings 4.4 and
5.4 were derived from the behaviour of the combined probes C01, C02 and C03 and were not executed
against the pristine tool as separate cases.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-kernel-taint.py at revision 099c7b3f42d073203d9448807860f04c175eccd7 through a read-only export, plus the lane bytes that the counter reads; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/MutC1Counter.md, /fast/scratch/hyaku/tsuku27a2/MutC1Counter/{harness.py,mutants.json,mutants-combined.json,probe.py,results.json,results-combined.json,baseline.json,baseline-selftest.json,baseline-revision.json,golden-check-kernel-taint.py,tree/,verify-export/}; executed=git archive 099c7b3f42d073203d9448807860f04c175eccd7 into /fast/scratch/hyaku/tsuku27a2/MutC1Counter/tree, python3 tools/check-kernel-taint.py --selftest, python3 tools/check-kernel-taint.py --revision 099c7b3f42d073203d9448807860f04c175eccd7 --repo /home/vgpnk/Projects/shokunin/tsukuroi-shokunin, python3 harness.py mutants.json results.json, python3 harness.py mutants-combined.json results-combined.json, python3 probe.py, sha256sum, diff -r, git status --porcelain, git rev-parse HEAD
Model: minimax-code/MiniMax-M3.1-Flash
Installs: none
