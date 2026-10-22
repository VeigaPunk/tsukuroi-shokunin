# Wave 2 — RevRegistrySelftests: registry coverage runs and tool selftests at R

survives — every commanded run at the landed commit 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0 (branch master) exited 0 with PASS and the printed counts, and no run or selftest mutated the lane's git state.

## Method

- Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` was already at HEAD `22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0`; `git status --porcelain` showed only 8 untracked `.ufo/` evidence entries, so every tracked `tools/` file in the working tree is byte-identical to the committed blob at R. [obs]
- Before running, I audited each selftest body for writes: `check-registry-coverage.py` (`tools/check-registry-coverage.py:431-470`) and `tools/_revision.py` (`tools/_revision.py:213-216`) do their `git init`/`add`/`commit`/`update-ref` only inside a `tempfile.TemporaryDirectory` fixture repository, never in the lane; `check-seat-bindings.py`, `check-pause-gate.py` and `report-red-causes.py` selftests are pure in-memory fixture calls. No git-writing selftest touches the lane, so no clone was required; I additionally proved this empirically (finding 8). [obs]

## Findings

1. **Registry coverage at R: exit 0, PASS.** Command `python3 tools/check-registry-coverage.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0` run from the lane root. Output JSON: `status PASS`, `branch master`, `branch_tip 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0`, `counts {"findings":0,"missing":0,"registered":26,"rows_total":26,"tools_total":26}`, `findings []`. Exit code 0. [obs]
2. **Registry coverage with the live-map audit: exit 0, PASS.** Same command plus `--audit-live-map`. Identical base counts plus `"audit_live_map_errors":0`, no findings, exit 0. The round24 `boot-chain-audit` row in SKILL.md therefore matches the required schema-v2 mode map, entry spellings, and no-write scope. [obs]
3. **`report-red-causes.py --selftest`: exit 0, PASS, 11 cases, 0 failed.** JSON `{"status":"PASS","cases":11,"failed":0}`, no failing case names. The 11 cases are the 9 `attribute()` table cases plus 2 stub-checker cases (`stub-pristine`, `stub-shifted-sites`) at `tools/report-red-causes.py:214-263`. [obs]
4. **`check-pause-gate.py --selftest`: exit 0, PASS, 24 cases, 0 failed.** JSON `{"status":"PASS","cases":24,"failed":0}`; the case table at `tools/check-pause-gate.py:198-223` lists exactly 24 named cases (pristine plus 23 mutants), and the pristine case expects exit 0 with `premises_verified 5`, matching the C2 claim shape. [obs]
5. **`check-seat-bindings.py --selftest`: exit 0, PASS, 121 cases (73 v1 + 48 v2), 0 failed.** JSON `{"status":"PASS","cases":121,"v1_cases":73,"v2_cases":48,"failed":0}`; the printed partition sums to the total. [obs]
6. **`_revision.py --selftest`: exit 0, PASS, 57 cases, 0 failed.** Output line `REVISION_SELFTEST: PASS (57 cases, 57 passed, 0 failed)` (`tools/_revision.py:27` documents this contract). The count is internally plausible: static `expect()` calls plus loops of 11 revision spellings and 9 branch spellings in `tools/_revision.py:223-260`. [obs]
7. **`check-registry-coverage.py --selftest`: exit 0, PASS.** Its declared `total = 23` (`tools/check-registry-coverage.py:441`) matches the 23 `check(...)` invocations I counted in the selftest body; PASS line `PASS (23 cases, 23 passed, 0 failed)` semantics, exit 0. [obs]
8. **Lane proven unmutated.** `git count-objects -v` before and after all runs: identical `count: 4659`, `in-pack: 0`, `garbage: 0`; dirty entries stayed at 8; no leftover `/tmp/tsukuroi-registry-selftest-*` or `tsukuroi-revision-st-*` directories after the runs. All selftest git writes stayed inside their per-run temp fixture repos. [obs]
9. **Count honesty cross-checks.** (a) `git ls-tree --name-only 22fd1642... tools/ | wc -l` = 26, equal to `tools_total` 26, so the checker's tool discovery over the committed tree is neither inflated nor truncated. (b) The round24 registry heading sits at line 2254 of SKILL.md at R and its table holds exactly 26 data rows, equal to `rows_total` 26. (c) The registry headings at R are round22 (line 2167), round23 (line 2206), round24 (line 2254); the checker selects the unique highest-round table, consistent with the `unique-highest-table` selftest case. [obs]
10. **One methodology note, not a defect.** A naive row count across all `## Gate and probe registry — round*` headings sums to 138 rows (round22+round23+round24 combined); the operative-round discrimination is done by the checker, not by naive heading matching. No correction needed to the tool. [inf]

## Defects

None in scope. No run failed, no count mismatched an independent count, and no selftest escaped its fixture sandbox. Smallest corrections: not applicable.

## Residual risk and verification gaps

- I exercised the selftests as shipped; I did not mutation-test the checkers themselves (other seats own mutation lanes, e.g. MutC1* and MutGate*). [unk]
- `check-registry-coverage.py --baseline-tools` was not in the assignment and was not run. [unk]
- The PASS verdicts depend on the working tree matching R for tracked files; verified true at run time via `git status --porcelain` (only untracked `.ufo/` entries), but later seats editing `tools/` in the working tree would invalidate that premise. [inf]

Scope: read=lane HEAD/status/count-objects; tools/check-registry-coverage.py, tools/_revision.py, tools/report-red-causes.py, tools/check-pause-gate.py, tools/check-seat-bindings.py (selftest bodies and entry points); SKILL.md registry tables and tools/ tree at R via git show/ls-tree; wrote=.ufo/waves/round-24/w2/RevRegistrySelftests.md; executed=check-registry-coverage --revision R (exit 0), check-registry-coverage --revision R --audit-live-map (exit 0), check-registry-coverage --selftest (exit 0), report-red-causes --selftest (exit 0), check-pause-gate --selftest (exit 0), check-seat-bindings --selftest (exit 0), _revision.py --selftest (exit 0), plus read-only git count-objects/status/ls-tree/show
Installs: none
