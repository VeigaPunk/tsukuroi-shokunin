# ExecCalibration — round 96 w1 (C2 counter: six routed r95 mismatch classes)

Seat: `ExecCalibration` (executor, axis calibration). Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Final measurement HEAD: `59cbfe2f4b96a73c2697cf81eb989e1d72e276fd` (landed commit "round-96: C2 repairs …",
07:54:23). In-flight measurements were at `b0bf1be9` (dirty tree).
Tools: `Python 3.14.8`, `git 2.56.0`; no installs; pacman untouched; read-only git only.
Receipts: `.ufo/waves/round-96/w1/ExecCalibration/`; full report duplicated at
`.ufo/waves/round-96/w1/ExecCalibration/report.md`.

## Final readings at the landed tree

1. **Freeze holds.** `sha256sum -c .ufo/waves/round-96/before/instruments.sha256` → every line OK, 0 FAILED
   (`state-at-measurement-final.txt`). `sha256sum tools/check-r96-calibration.py` =
   `7ff63524fa971b50a4af108e66458918a88e2fedc7140d57c1ddbe428c81dbc4` = manifest line =
   `git show 59cbfe2f:tools/check-r96-calibration.py`. C2's void condition does not hold.
2. **Selftest.** `python3 tools/check-r96-calibration.py --selftest` → `clean PASS, F1 PASS … F6 PASS,
   selftest PASS 7/7`, exit 0 (`c2-selftest-final.stdout`); same 7/7 from the freeze-manifest copy
   (`c2-selftest-frozenchecker.stdout`).
3. **Pre-round tree.** `git archive 73c47107…` + `--tsv .ufo/waves/round-95/claim-falsification.tsv`
   + `--report /home/vgpnk/Projects/shokunin/.ufo/reports/round-95/tsukuroi.md` →
   `status FAIL`, 10 findings, ids `F1 F2 F3 F4 F5 F6`, 4 unreadable (`c2-before-final.json`); the
   freeze-manifest copy reproduces `before/c2-before-73c47107.json` exactly (findings/unreadable/status
   equal; only `root` differs) (`c2-before-frozenchecker.json`).
4. **Current tree.** `python3 tools/check-r96-calibration.py --root . --json …/c2-after-landed.json` →
   `{"findings":[],"unreadable":[],"status":"PASS"}`, exit 0, with HEAD and the checker hash written into
   `c2-after-landed.stdout`.
5. **Bindings.** `git diff 73c47107..59cbfe2f -- tools/check-registry-coverage.py` → empty (0 lines);
   `git show 59cbfe2f:tools/make-r95-bends.py | grep -c 'boundary member'` → 1 (contiguous);
   `… limine-pin-battery-r95.py | grep -c 'largest in-bound'` → 0.

## PASS/FAIL per expected line

| # | Expected | Final measured | Verdict |
|---|---|---|---|
| 1 | Before: `status FAIL`, ≥1 finding in each F1–F6 | FAIL, 10 findings, every id present; equals the committed reference | **PASS** |
| 2 | After (`--root .`, no `--report`): PASS, `findings []`, `unreadable []` | PASS / [] / [] at `59cbfe2f` with the pinned checker | **PASS** |
| 3 | `--selftest` PASS 7/7 | PASS 7/7 | **PASS** |
| 4a | Criterion 140 cites round-95.md/M1/development run | block present; all three tokens True | **PASS** |
| 4b | Receipt hash = `sha256sum tools/check-registry-coverage.py` | `6fcb2d0a…` both, also in the manifest | **PASS** |
| 4c | Two r95 docstrings corrected | both carry raw `boundary member`; raw `largest in-bound` = 0 | **PASS** |
| 4d | README scoped to the r94 family roster, over-scope gone | scoped at README:1127-1129; over-scope phrase count 0 | **PASS** |
| 4e | Tip receipt r95-tip PASS 151/151 | PASS, `b8f878c8…`, 151/151, findings 0 | **PASS** |
| 4f | F6 fires exactly its own id on a wrong count | wrong count → exactly 1×F6; word count → 2×F6 ("states no … count"); matching → 0 | **PASS** |

## In-flight deviation (repaired by the L1 at `59cbfe2f`, kept as history)

At HEAD `b0bf1be9`: `instruments.sha256` FAILED on `tools/check-r96-calibration.py` (manifest `7ff63524…`,
working tree `ad894667…`, uncommitted 10-line whitespace-flattening); the pinned bytes read the tree as FAIL
with exactly one `F3 "tools/make-r95-bends.py does not say boundary member"` because the new wording was
line-wrapped (`a boundary` / `member`). Scratch simulation of the freeze-preserving repair (reflow that
docstring + restore the pinned checker bytes) read PASS 0 findings under both versions
(`sim-reflow-frozenchecker.json`, `sim-reflow-currentchecker.json`); the L1 then landed exactly that repair.
Historical receipts kept under `.ufo/waves/round-96/w1/ExecCalibration/` (`c2-before.json`,
`c2-before-frozenchecker.json`, `c2-after-noreport.json`, `c2-after-noreport-frozenchecker.json`, …).

## Open dependency

`.ufo/waves/round-96/claim-falsification.tsv` is absent; the committed-ledger F6 leg is the L1's filing
(the seat item's after-run deliberately omits `--report`). The scratch-ledger F6 tests prove the check's
discrimination.

## Receipts

`state-at-measurement-final.txt`, `c2-after-landed.json|.stdout`, `c2-selftest-final.stdout`,
`c2-before-final.json|.stdout`, `c2-f6-wrongcount-final.json|.stdout`,
`c2-f6-wordcount-final.json|.stdout`, `c2-f6-matching-final.json|.stdout`,
`frozen-checker-7ff63524.py|.sha256`, `f6-ledger.tsv`, `f6-report-{wrong,word,ok}.md`, plus the in-flight
receipts named above. Scratch `/fast/scratch/hyaku/tsukuroi-r96/ExecCalibration` deleted after writing.

{"seat":"ExecCalibration","verdict":"met","notes":"Landed tree 59cbfe2f with the manifest-pinned checker 7ff63524 (working = committed = manifest): instruments all OK, selftest 7/7, current tree PASS findings [] unreadable [], pre-round 73c47107 FAIL with F1-F6 all present (10 findings, equal to the L1's c2-before receipt); six fixes verified (criterion 140 cites r95/M1/development run; registry gate receipt 6fcb2d0a matches bytes+manifest and the 73c47107..59cbfe2f diff over it is empty; both r95 docstrings raw boundary member and no largest in-bound; README scoped, over-scope gone; tip receipt b8f878c8 PASS 151/151; F6 fires exactly its own id on a wrong count and is clean on a matching one); the in-flight checker/tree deviation was repaired by the L1 exactly as simulated; only open dependency is the round-96 ledger (L1 filing)."}
