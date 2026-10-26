VERDICT: supports

# G-5 — registry gate sweep at the lane working tree (round 39, wave 1)

Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, working tree at HEAD
`394e1ba4fab39a417abe66a7802f87cf1ff8dd61` (`git rev-parse HEAD`); the dispatch tip
`2e1c2a40c13dc52e155d89e72f3fdd560db7399a` is an ancestor of it (`git merge-base --is-ancestor
2e1c2a40 HEAD`; rc=0). Every row ran with `TMPDIR=/fast/scratch/hyaku/tsukuroi-r39/GateAllRegistry`
and no other environment change. Whole sweep: **31 rows, 31 exit 0, 1474 selftest cases, 0 failed,
0 red** — 134.6 s wall clock at `-P4`.

## 1. Enumeration — which rows this item covers

The operative table is the unique highest complete one; 25 tables in `SKILL.md` start with
`| Name | Kind | Entry command |` (header lines 1707, 1735, 1776 … 3056), and the last is operative
(`SKILL.md:3056`, the round-36-superseding table), as the section prose requires ("The unique highest
complete table is operative", `SKILL.md:3051-3053`). I parsed that table mechanically (cells split on
unescaped `|`, so the `\|` in the `--set claim\|regression` entry command does not shift columns):

- 60 rows total, table body `SKILL.md:3059-3117`
- 40 rows with `Kind = gate`
- **31** of those carry a real `--selftest` command in the Self-test column → run
- **9** read `none…` in the Self-test column → skipped, as the item directs (listed in §3)

Non-gate rows that do carry a selftest (`update-recheck` probe, `boot-chain-audit` probe,
`revision-binder` library) are outside this item's wording ("every row of kind `gate`") and were not
run. Re-parsing the table after the sweep returned the same 31 names in the same order
(`gates == mine: True`), and the table block `SKILL.md:3056-3117` hashes
`627a01868a5e9508757a1327c1e19420351923046693fc1326450f6b639cf09f`.

## 2. Result — all 31 gate selftests green

Self-test verdict map for these rows is `0 PASS / 1 FAIL` (`SKILL.md:3059-3117`, Self-test and
Verdict-map columns). Every row exited 0 and printed a PASS summary. Logs:
`.ufo/waves/round-39/w1/GateAllRegistry/logs/<name>.txt`; the machine-readable copy of this table is
`…/GateAllRegistry/sweep.tsv`.

| Name | Self-test command (verbatim from the row) | exit | summary line (verbatim, last/status) |
|---|---|---|---|
| host-census | `bash tools/tsukuroi-census.sh --selftest` | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)` |
| root-dac-correction | `python3 tools/check-root-dac-correction.py --selftest` | 0 | `CHECK_ROOT_DAC_CORRECTION_SELFTEST: PASS (54 cases, 54 passed, 0 failed)` |
| source-scope-correction | `python3 tools/check-source-scope-correction.py --selftest` | 0 | `CHECK_SOURCE_SCOPE_CORRECTION_SELFTEST: PASS (29 cases, 29 passed, 0 failed)` |
| locator-clarification | `python3 tools/check-locator-clarification.py --selftest` | 0 | `CHECK_LOCATOR_CLARIFICATION_SELFTEST: PASS (37 cases, 37 passed, 0 failed)` |
| section-citations | `python3 tools/check-section-citations.py --selftest` | 0 | `CHECK_SECTION_CITATIONS_SELFTEST: PASS (68 cases, 68 passed, 0 failed)` |
| boot-chain | `python3 tools/check-boot-chain.py --selftest` | 0 | `CHECK_BOOT_CHAIN_SELFTEST: PASS (83 cases, 83 passed, 0 failed)` |
| freshness-r17 | `python3 tools/check-freshness-r17.py --selftest` | 0 | `CHECK_FRESHNESS_R17_SELFTEST: PASS (59 cases, 59 passed, 0 failed)` |
| appended-notices | `python3 tools/check-appended-notices.py --selftest` | 0 | `CHECK_APPENDED_NOTICES_SELFTEST: PASS (47 cases, 47 passed, 0 failed)` |
| recheck-commands | `python3 tools/check-recheck-commands.py --selftest` | 0 | `{"selftest": {"cases": 95, "failures": [], "passed": 95, "status": "PASS"}}` |
| seat-scope | `python3 tools/check-seat-scope.py --selftest` | 0 | `CHECK_SEAT_SCOPE_SELFTEST: PASS (54 cases, 54 passed, 0 failed)` |
| revision-binding | `python3 tools/check-revision-binding.py --selftest` | 0 | `CHECK_REVISION_BINDING_SELFTEST: PASS (78 cases, 78 passed, 0 failed)` |
| adjacency-anchors | `python3 tools/check-adjacency-anchors.py --selftest` | 0 | `PASS (25 cases, 25 passed, 0 failed)` |
| boot-writers | `python3 tools/check-boot-writers.py --selftest` | 0 | `PASS (12 cases, 12 passed, 0 failed)` |
| registry-coverage | `python3 tools/check-registry-coverage.py --selftest` | 0 | `PASS (23 cases, 23 passed, 0 failed)` |
| selector-contract | `python3 tools/check-selector-contract.py --selftest` | 0 | `{"status": "PASS", "cases": 28, "passed": 28, "failures": []}` |
| review-snapshots | `python3 tools/check-review-snapshots.py --selftest` | 0 | `{"status": "PASS", "cases": 24, "passed": 24, "failures": []}` |
| boundary-contract | `python3 tools/check-boundary-contract.py --selftest` | 0 | `{"status": "PASS", "cases": 28, "failed": 0}` |
| seat-bindings | `python3 tools/check-seat-bindings.py --selftest` | 0 | `{"status": "PASS", "cases": 121, "v1_cases": 73, "v2_cases": 48, "failed": 0}` |
| review-cohort | `python3 tools/check-review-cohort.py --selftest` | 0 | `{"status": "PASS", "cases": 24, "failed": 0}` |
| edit-contract | `python3 tools/check-edit-contract.py --selftest` | 0 | `{"status": "PASS", "cases": 102, "failed": 0}` |
| path-reconciliation | `python3 tools/check-path-reconciliation.py --selftest` | 0 | `{"status": "PASS", "cases": 40, "failed": 0}` |
| red-causes | `python3 tools/report-red-causes.py --selftest` | 0 | `{"status": "PASS", "cases": 12, "failed": 0}` |
| pause-gate | `python3 tools/check-pause-gate.py --selftest` | 0 | `{"status": "PASS", "cases": 24, "failed": 0}` |
| self-assessment | `python3 tools/check-self-assessment.py --selftest` | 0 | `{"selftest": "PASS", "cases": 19, "failures": []}` |
| memory-pressure | `python3 tools/check-memory-pressure.py --selftest` | 0 | `{"status": "PASS", "cases": 41, "failed": 0}` |
| storage-health | `python3 tools/check-storage-health.py --selftest` | 0 | `{"status": "PASS", "cases": 44, "failed": 0}` |
| kernel-taint | `python3 tools/check-kernel-taint.py --selftest` | 0 | `{"status": "PASS", "cases": 56, "failed": 0}` |
| adjacency-overlap | `python3 tools/check-adjacency-overlap.py --selftest` | 0 | `{"cases": 96, "failed": 0, "observations": […96 entries…]}` — no `status` key; all 96 `"pass": true` |
| report-receipts | `python3 tools/check-report-receipts.py --selftest` | 0 | `{"cases": 2, "failures": [], "passed": 2, "selftest": "PASS"}` |
| knowledge-header | `python3 tools/check-knowledge-header.py --selftest` | 0 | `{"selftest": {"cases": 25, "failures": [], "passed": 25, "status": "PASS"}}` |
| journalctl-v262-corrections-r37 | `python3 tools/check-journalctl-v262-corrections.py --selftest` | 0 | `{"cases": 7, "failures": [], "passed": 7, "status": "PASS"}` |

No log carries a FAIL verdict and no failure count is above zero (`grep -c 'rc=0' rc.txt` → 31/31). The
only uppercase `FAIL` substrings anywhere in the logs are two finding ids inside **expected** fixture
observations — `E-GIT-FAILED` in `revision-binding.txt` (78/78 PASS) and `REVIEW-READ-FAILED` in
`review-snapshots.txt` (`"status": "PASS", "passed": 24, "failures": []`).

Cross-check that the harness is not frozen or stale: the census selftest reports **117 cases** here, the
same count the author recorded in the lane (`git log -1 2e1c2a4` subject: "selftest 117/117"), and
`check-self-assessment`'s K13 binds exactly that number to the operability row
(`tools/check-self-assessment.py:649-655`).

## 3. Skipped rows — `Self-test` = `none` (9 gate rows)

Skipped per the item. Quoted Self-test cells:

| Name | line | Self-test cell (abridged quote) |
|---|---|---|
| owed-statements-r29 | `SKILL.md:3092` | "none: no self-test mode; a counter run at the bound revision is the measurement" |
| btrfs-space-r30 | `SKILL.md:3096` | "none: no self-test mode; fixture mode `--tree … --base-sources …` is exercised by the battery `mutants-btrfs-space-r30`" |
| btrfs-repair-r31 | `SKILL.md:3102` | "none: no self-test mode; the frozen Q01-Q08 question set is measured by the counter" |
| census-handoff-r32 | `SKILL.md:3104` | "none: no self-test mode; 24 seeded fixture scenarios plus two read-only live views are the measurement" |
| storage-arm-r38 | `SKILL.md:3113` | "none: the ten built-in fixtures F01-F10 and the live leg are the measurement" |
| storage-arm-r38-q82 | `SKILL.md:3114` | "none: three per-run random views are the measurement" |
| hook-order-r38 | `SKILL.md:3115` | "none: the frozen capture is the measurement" |
| storage-hidden-r39 | `SKILL.md:3116` | "none: the hidden legs H1/H2, views V0-V2, fixtures F1-F5 and the live leg are the measurement" |
| transaction-order-r39 | `SKILL.md:3117` | "none: the frozen snapshots and capture are the measurement" |

## 4. Perturbation checks on the sweep itself

- **Concurrent sibling work in the working tree.** `git status --porcelain` before the sweep: ` M
  PROVINCE.md`, `?? .ufo/waves/round-39/w1-dispatch.err`, `?? .ufo/waves/round-39/w1/`. At report
  time the same command additionally shows ` M SKILL.md` and `?? .ufo/waves/round-39/w1.ready.dispatched`.
  The `SKILL.md` change is an EOF append only (`git diff SKILL.md` hunk `@@ -3201,3 +3201,24 @@`, the
  round-39 storage-arm section); it lands after line 3201, so the operative table (`3056-3117`) is
  untouched, and re-parsing the table after the sweep reproduced the same 31 names in the same order.
- **Hermeticity of the selftests** (so the shared dirty tree cannot have decided a verdict): the
  selftests declare fixture-only inputs — e.g. `tools/check-seat-scope.py:26` "`--selftest` is
  hermetic", `tools/check-revision-binding.py` "stub tools in mktemp fixtures, never the real lane",
  `tools/check-adjacency-anchors.py:968` and `tools/check-adjacency-overlap.py:901` `tempfile.TemporaryDirectory`,
  `tools/check-self-assessment.py:8` "the working tree is never read" with `:1032`
  `tempfile.mkdtemp(prefix="self-assessment-selftest-")`, and `tools/tsukuroi-census.sh:382` "selftest
  writes only under a mktemp dir named `${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX`" with `:389`
  "every host path read in live mode has an override below, so the selftest touches no [host]".
  Because `TMPDIR` was my scratch dir, even that census fixture tree stayed inside
  `/fast/scratch/hyaku/tsukuroi-r39/GateAllRegistry`; nothing ran from `/tmp`.
- **Parallelism.** Four rows at a time in a persistent shell; all selftests use private
  `TMPDIR`/`mktemp` trees, and no row's log shows a contention error.

## 5. Red flags

None. 0 non-zero exits, 0 failed cases, 0 missing tools (`test -f` on all 30 scripts plus
`tools/tsukuroi-census.sh`: none missing). Two rows are worth knowing about because their summary is
not the usual `PASS (N cases…)` shape and a naive scanner would miscount them:
`adjacency-overlap` prints no `status` key at all (exit code plus `"failed": 0` of 96 observations,
each `"pass": true`), and `report-receipts` prints only **2** cases — the thinnest harness in the
table, so its green is weak evidence of parser breadth.

## 6. Limits — what this sweep does not show

1. **Nine gate rows have no selftest at all** (§3). G-5 therefore says nothing about `storage-arm-r38`,
   `storage-arm-r38-q82`, `hook-order-r38`, `storage-hidden-r39`, `transaction-order-r39`,
   `owed-statements-r29`, `btrfs-space-r30`, `btrfs-repair-r31` or `census-handoff-r32`; their state
   rests on the frozen controls in `.ufo/waves/round-39/controls/` and on other seats.
2. **A green selftest is the tool's own harness verdict on fixtures**, not a live-host measurement and
   not a claim verdict. I ran no entry command in live mode (the table allows live probes "only when
   separately authorized").
3. **Case counts were not diffed against earlier rounds.** A silently shrunk fixture suite would still
   print PASS; the only size anchor I checked is the census 117 (K13 binding above).
4. The sweep reads the working-tree scripts; it does not prove the committed blobs at HEAD are what ran,
   though `git status` shows no `tools/` modification.

## 7. Evidence retained

`.ufo/waves/round-39/w1/GateAllRegistry/` — `sweep.tsv` (name, command, exit, summary),
`rows.txt` (the 31-row list), `rc.txt` (raw exit codes), `logs/<name>.txt` (31 full transcripts),
`MANIFEST.sha256` (34 digests: 31 logs + 3 index files).

## 8. No harm

Read-only toward the lane: no tracked file edited, created or deleted; `git diff --cached --stat | wc -l`
→ 0 (index untouched); no `git add/commit/stash/checkout/reset/push`, no jj command, no mutation of the
fleet repo or any sibling lane; no host mutation, no sudo, no pacman, no service action, no mount outside
a tool's own private namespace (none of these selftests needs one); no tool installed or upgraded in this
seat. Scratch `/fast/scratch/hyaku/tsukuroi-r39/GateAllRegistry` removed after the receipts were copied
into the seat directory.
