# MutC1Counts — mutation test of K07 to K11 and K13 in `tools/check-self-assessment.py`

Verdict: the C1 count detector holds — all nine mutants of K07, K08, K09, K10, K11 and K13 were killed at the measured revision `5e7c04ecb02735491456de2b8bc44550d0db4609`, and every mutant was restored byte-for-byte to the pristine tree.

Scope of the probe: K07, K08, K09, K10, K11 and K13 of the C1 check set of `tools/check-self-assessment.py` (the counting tool of claim C1, calibration). K12 and K14 to K23 were left untouched by this seat. The tasking named seven mutations (add one knowledge note, add one SKILL.md line, add one pipe line, add one lesson file, change a stated count by one, remove the `notes` phrase, change `97 cases` to `96 cases`); the two additions below are isolated variants that make the verdicts unambiguous, and both are reported.

## Method

1. The sandbox was built exactly as the tasking prescribes: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 5e7c04ecb02735491456de2b8bc44550d0db4609 | tar -x -C /fast/scratch/hyaku/tsukuroi-r25/w2/MutC1Counts/sandbox`, then `git init` with no remote. The lane repository was never written to and no git or jj write command was run against it.
2. The archive was committed inside the sandbox as `15d5e36530d68928d04b8d95e9639b0dfe6e15d9` (the sandbox base commit; it is a sandbox-local commit id and not a lane revision).
3. The detector is the tool at the measured revision: `python3 tools/check-self-assessment.py --revision HEAD`, run with the sandbox as the working directory. The tool reads the tree through Git at the named revision and never reads the working tree, so every mutation was committed before the detector ran.
4. Pristine run first, then one run per mutant, then the working tree was reset to the sandbox base commit and the tree digest was compared with the pristine digest. A final independent check compared the restored sandbox against a fresh archive of `5e7c04ec` with `diff -r` (exit 0, no output).

Tree digest: a sha256 over the sorted list of every tracked file path and its file sha256. Pristine digest `eb665f0853d2cfac81348b714d02539e2fa8bbf5348c1072cf7b452d4a405a88`. Every mutant produced a distinct digest, and every restored tree reproduced the pristine digest exactly.

Evidence artifacts: `.ufo/waves/round-25/w2/MutC1Counts/report.json` (full machine-readable run record), `.ufo/waves/round-25/w2/MutC1Counts/harness.py` and `.ufo/waves/round-25/w2/MutC1Counts/harness2.py` (the harnesses that produced it).

## Pristine baseline

Command `python3 tools/check-self-assessment.py --revision HEAD` in the sandbox at the pristine tree: exit 0, `"status": "PASS"`, `"mismatches": 0`, `"checked": 23`. The measured counts at the revision match the table the lane states: 47 notes, `SKILL.md` 2355 lines, 297 pipe-prefixed lines, 26 lesson files, `corpus/README.md` 231 lines, and a census selftest of 97 cases. This matches the claim C1 measurement recorded by the L1 (5e7c04ec exit 0, 0 of 23).

## Findings

### 1. K07 — add one knowledge note: killed

Mutant: add file `corpus/knowledge/mutant-k07-note.md` (a real `.md` file, so it counts under the `corpus/knowledge/*.md` grammar).

Detector output: exit 1, `"mismatches": 1`, failing check `K07` only.

Tool reason string: `depth row states 47 notes; corpus/knowledge holds 48 .md files` (stated 47, observed 48).

Mutant tree digest `a30c3c83992942d1bf9c635b0504d8e69d3ed29dfe36b1e5b0e676ae7b0f1f36`; restored digest `eb665f0853d2cfac81348b714d02539e2fa8bbf5348c1072cf7b452d4a405a88` (equal to pristine).

### 2. K07 — remove the `notes` phrase: killed

Mutant: in the depth row of the round-25 axes table, replace `47 notes (`ls corpus/knowledge/*.md` with `47 (`ls corpus/knowledge/*.md`. The number stays, the word that makes the row state a note count goes away.

Detector output: exit 1, `"mismatches": 1`, failing check `K07` only.

Tool reason string: `depth row states None notes; corpus/knowledge holds 47 .md files` (stated None, observed 47).

This is the important half of K07: the check does not fall back to the round-11 table's `24 notes` or to any other number, it reports the depth row as stating no note count at all. A row that drops the phrase is caught rather than silently passing.

Mutant tree digest `4413241c9485458f3a78bb6328c082ab9739f0e8616d5ff77b96fe5e533cc0c3`; restored digest `eb665f0853d2cfac81348b714d02539e2fa8bbf5348c1072cf7b452d4a405a88`.

### 3. K08 — add one SKILL.md line: killed

Mutant: append one plain (non-pipe) line to `SKILL.md`.

Detector output: exit 1, `"mismatches": 1`, failing check `K08` only.

Tool reason string: `depth row states 2355 SKILL.md lines; SKILL.md holds 2357 newline characters` (stated 2355, observed 2357).

[obs] The tool counts newline characters, while the lane's evidence cell names `wc -l`. The two agree only when the file ends in a newline. Here the append added a blank separator line and the text line, so the newline count rose by 2 while `wc -l` would also have risen by 2; the discrepancy in the number is not a tool error but the difference between "lines" as counted by `wc -l` and "newline characters" as counted by the tool. The check still killed the mutant, and it reported the observable it actually measured.

Mutant tree digest `d6045c9b23fdddd51e04821b736508237e418751b0ca15500c20c5eb6bfe7390`; restored digest `eb665f0853d2cfac81348b714d02539e2fa8bbf5348c1072cf7b452d4a405a88`.

### 4. K09 — add one pipe line: killed (and isolated)

Mutant A (M3): append one pipe-prefixed line to `SKILL.md`.

Detector output: exit 1, `"mismatches": 2`, failing checks `K08` and `K09`.

Tool reason strings: `depth row states 2355 SKILL.md lines; SKILL.md holds 2357 newline characters` and `depth row states 297 table lines; SKILL.md holds 298 pipe-prefixed lines` (stated 297, observed 298).

[obs] A pipe line is also a line, so this mutant necessarily moves K08 as well. To isolate K09, mutant B (M3c) appends the same pipe line and compensates the stated `` `SKILL.md` N `wc -l` `` count by the exact number of added lines (2, so 2355 becomes 2357).

Mutant B detector output: exit 1, `"mismatches": 1`, failing check `K09` only. Tool reason string: `depth row states 297 table lines; SKILL.md holds 298 pipe-prefixed lines`.

So K09 is killed in isolation and not merely as collateral damage from K08. A first compensation attempt (M3b) that set the stated count to 2356 was off by one and still tripped K08; the corrected M3c isolates it.

Mutant tree digests: M3 `8b9473982db181e6d9c26838a1eec5a8652852eab9cfcf115f176f0a62736830`, M3c `714dd3ed092e48922d730c9dcaa86f3a28f1b298` (commit id of the compensated mutant); restored digest for every case `eb665f0853d2cfac81348b714d02539e2fa8bbf5348c1072cf7b452d4a405a88`.

### 5. K10 — add one lesson file: killed

Mutant: add file `corpus/lessons/mutant-k10-lesson.md`.

Detector output: exit 1, `"mismatches": 1`, failing check `K10` only.

Tool reason string: `depth row states 26 lesson files; corpus/lessons holds 27 files` (stated 26, observed 27).

Mutant tree digest `e55f53cc2b73054a0e39aa5feb4b657f5c8f3010af075f1b766d328cd8dda402`; restored digest `eb665f0853d2cfac81348b714d02539e2fa8bbf5348c1072cf7b452d4a405a88`.

### 6. K11 — change a stated count by one: killed

Mutant A (M5, stated side): in the coverage row, change `` `corpus/README.md` 231 `wc -l` `` to `` `corpus/README.md` 232 `wc -l` ``.

Detector output: exit 1, `"mismatches": 1`, failing check `K11` only. Tool reason string: `coverage row states 232 corpus/README.md lines; the file holds 231 newline characters` (stated 232, observed 231).

Mutant B (M5b, observed side): append one line to `corpus/README.md`.

Detector output: exit 1, `"mismatches": 1`, failing check `K11` only. Tool reason string: `coverage row states 231 corpus/README.md lines; the file holds 233 newline characters` (stated 231, observed 233).

Both directions of the K11 comparison are therefore live: a wrong stated count and an unstated repository change both fail.

Mutant tree digests: M5 `1cea7b8fb1c7eda73bab87d6d40f4050e423746e152bb364d09ff6156a2bff54`, M5b `afc41955fdef9bc8aadf8c84ab078cd148fd08b6a9d0ff0959283e8008af9475`; restored digest for both `eb665f0853d2cfac81348b714d02539e2fa8bbf5348c1072cf7b452d4a405a88`.

### 7. K13 — change `97 cases` to `96 cases`: killed

Mutant: in the operability row of the axes table, change `prints PASS (97 cases, 97 passed, 0 failed) with exit 0` to `prints PASS (96 cases, 97 passed, 0 failed) with exit 0`.

Detector output: exit 1, `"mismatches": 1`, failing check `K13` only.

Tool reason string: `operability row states 96 cases; the census selftest at this revision prints 97 cases (TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed))` (stated 96, observed 97).

[obs] The observed value is not read from the scorecard. The tool archives the revision into a temporary directory and actually runs `bash tools/tsukuroi-census.sh --selftest` there, then takes the count from the printed `(97 cases` marker. The mismatch is therefore against a live re-run of the census at the mutated revision, not against a second copy of the same number. This is the strongest form of the K13 check.

Mutant tree digest `ec8eaed8189812a5db835fb62bff1ddc3e333a6cfa72d28bb02af3dabb22c82a`; restored digest `eb665f0853d2cfac81348b714d02539e2fa8bbf5348c1072cf7b452d4a405a88`.

## Summary table

| Mutant | Target check | Exit | Mismatches | Failing checks | Verdict | Restored |
|---|---|---|---|---|---|---|
| pristine | none | 0 | 0 | none | baseline pass | n/a |
| M1 add `corpus/knowledge/mutant-k07-note.md` | K07 | 1 | 1 | K07 | killed | yes |
| M6 remove the `notes` phrase from the depth row | K07 | 1 | 1 | K07 | killed | yes |
| M2 append one plain line to `SKILL.md` | K08 | 1 | 1 | K08 | killed | yes |
| M3 append one pipe line to `SKILL.md` | K09 (+K08) | 1 | 2 | K08, K09 | killed | yes |
| M3c pipe line + stated line count compensated | K09 only | 1 | 1 | K09 | killed | yes |
| M4 add `corpus/lessons/mutant-k10-lesson.md` | K10 | 1 | 1 | K10 | killed | yes |
| M5 stated README count 231 to 232 | K11 | 1 | 1 | K11 | killed | yes |
| M5b append one line to `corpus/README.md` | K11 | 1 | 1 | K11 | killed | yes |
| M7 `97 cases` to `96 cases` in the operability row | K13 | 1 | 1 | K13 | killed | yes |

Killed: 9 of 9 (ten runs counting the compensating M3c and the pristine baseline). Survived: 0. Inconclusive: 0. No baseline failure was observed, so no run is inconclusive.

## Restoration evidence

- Every mutant working tree was reset with `git reset --hard 15d5e36530d68928d04b8d95e9639b0dfe6e15d9` plus `git clean -fd` inside the scratch sandbox only, and the tree digest was recomputed. All ten post-run digests equal the pristine digest `eb665f0853d2cfac81348b714d02539e2fa8bbf5348c1072cf7b452d4a405a88`.
- Independent check after the last run: a fresh `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 5e7c04ecb02735491456de2b8bc44550d0db4609 | tar -x -C verify` compared with `diff -r verify sandbox --exclude=.git` gave exit 0 with no output.
- `git -C sandbox status --porcelain` is empty and `git -C sandbox log --oneline` shows only the sandbox base commit, so no mutant file or mutant commit remains in the scratch tree.
- The lane repository was never written to. `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain` at the end of this seat shows only wave-1 and measure files that other seats and the L1 own; this seat created exactly one path inside the lane, `.ufo/waves/round-25/w2/MutC1Counts.md` and the three files under `.ufo/waves/round-25/w2/MutC1Counts/`.

## Observations for the integrator

- [obs] K07, K08, K09, K10, K11 and K13 all fail loudly when the state they count moves away from the number the axes table states, and they fail in the direction that matters: a wrong stated count, an unstated repository change, and a dropped counting phrase are each caught.
- [obs] K13 is not self-referential. It re-runs the census selftest from a `git archive` of the revision under test, so the stated case count is compared against a live re-derivation rather than against a second reading of the same table.
- [inf] The count checks are therefore adequate for the calibration claim C1 as declared: the tool cannot pass at a revision whose stated counts do not match the repository, and it cannot pass when a counting phrase is removed from the row.
- [obs] The K08 check counts newline characters while the lane's evidence cell names `wc -l`. These agree for a newline-terminated file, which `SKILL.md` is, so the two are interchangeable in practice here; the wording in the tool's reason string is the one place where a reader could expect a difference. This is a wording observation, not a defect, and no contract change is proposed by this seat.
- [unk] Whether the census selftest is deterministic across runs and hosts was not probed beyond the single observed re-run of 97 cases per mutant. Each of the ten runs reproduced the same 97, so the count is stable within this lane and host.

Scope: read=SCORECARD.md (round-25 declaration, axes table, capabilities table), tools/check-self-assessment.py (checks K01-K23, census_case_count, main), corpus/README.md, SKILL.md, corpus/knowledge/, corpus/lessons/, wave-1 report directory listing, operator RULES.md, godspeed directive; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC1Counts.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC1Counts/report.json, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC1Counts/harness.py, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC1Counts/harness2.py, and scratch files under /fast/scratch/hyaku/tsukuroi-r25/w2/MutC1Counts/; executed=git archive and git init inside the scratch sandbox, git reset/clean/commit inside the scratch sandbox only, python3 tools/check-self-assessment.py --revision HEAD (11 runs), python3 harness.py, python3 harness2.py, diff -r verify sandbox, sha256sum, git status/log read-only in the lane and the sandbox.

Model: not exposed

Installs: none
