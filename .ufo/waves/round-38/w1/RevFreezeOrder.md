VERDICT: supports

Item R-1 — freeze discipline, round 38 (lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin; master = HEAD = 5edb6c2). All evidence below is from read-only git object inspection (log/show/diff/rev-parse/diff-tree/merge-base/ls-tree/status) plus reads of tracked working files; no lane index or jj state was touched, no scratch dir or /tmp use, no tool installed or upgraded.

Committed history (command exactly as assigned):
  git -C <lane> log --format='%h %cI %s' 8bd001f58bfda29c92d90d2a7a413825c0ca9fcb..master
```
5edb6c2 2026-10-26T01:33:02-03:00 round-38: registry rows for storage-arm-r38, storage-arm-r38-q82, hook-order-r38 (QUALITY 70)
9c9bb64 2026-10-26T01:32:13-03:00 round-38: pre-seat amendment — QUALITY 82 production-path counter for C1, QUALITY 80-81 sweep and per-row kill rule for C2
1fe28e7 2026-10-26T01:21:20-03:00 round-38: C2 effective ALPM hook order entry (HO1-HO7, 69 rows) on S208-S212
52ffd65 2026-10-26T01:18:12-03:00 round-38: C1 storage-integrity census arm (verdict-neutral STORAGE line, 6 selftest cases, TMPDIR-honouring selftest)
7cbaeb6 2026-10-26T01:16:08-03:00 round-38: freeze C1/C2 counters, hook capture, before receipts and controls
```

## (a) Freeze commit contents and ordering — HOLDS

- Parentage and order: `git log -1 --format='%h %p' 7cbaeb6` → `7cbaeb6 8bd001f` (freeze sits directly on the base). `git merge-base --is-ancestor` exits 0 for base→freeze, freeze→52ffd65, freeze→1fe28e7. Committer timestamps order the freeze (04:16:08Z) before the C1 implementation (04:18:12Z) and the C2 implementation (04:21:20Z); the SCORECARD header stamps match (`SCORECARD.md:2107` "2026-10-26T04:16Z", `:2133` "04:32Z" = 9c9bb64).
- What 7cbaeb6 adds (`git diff-tree --no-commit-id --name-status -r 7cbaeb6`; all A except SCORECARD.md M):
  - both counters: `tools/score-storage-arm-r38.py`, `tools/check-hook-order-r38.py`;
  - the capture: 81 paths under `.ufo/waves/round-38/frozen/hooks-capture/` (MANIFEST.sha256, capture-meta.txt, etc-pacman.d-hooks/ ×3, usr-share-libalpm-hooks/ ×76);
  - the before receipts: `.ufo/waves/round-38/before/c1-before.json`, `c2-before.json`;
  - the (v1) controls: `.ufo/waves/round-38/controls/controls.jsonl`, `controls.err`, `run-controls.sh`;
  - the declaration: `M SCORECARD.md`, `git diff --stat 8bd001f 7cbaeb6 -- SCORECARD.md` = 26 insertions, 0 deletions.
- The implementation commits touch none of the frozen artifacts: 52ffd65 = `M tools/tsukuroi-census.sh` only; 1fe28e7 = A `.ufo/waves/round-38/sources/{SHA256SUMS,alpm-hooks.5.asciidoc,alpm.c,hook.c,trans.c}`, `M corpus/SOURCES.md`, `A corpus/knowledge/pacman-hook-order-r38.md`. This matches the declaration's causal-separability sentence (`SCORECARD.md:2129-2130`).
- By design, not a violation: the QUALITY-82 counter and its controls (`tools/score-storage-arm-r38-q82.py`, `controls-q82.*`, `before/c2-novelty-sweep.txt`) enter later, in the declared pre-seat amendment 9c9bb64 — after the implementation commits but before any wave seat scored; the freeze commit contains exactly the artifacts its message and the declaration name (v1 controls). Receipts: receipts-01-history.txt.

## (b) Counter bytes, freeze vs master — IDENTICAL

- `git diff 7cbaeb6317cb9f7323d2619eec02db4e4da29449 master -- tools/score-storage-arm-r38.py tools/check-hook-order-r38.py` → empty output, exit 0.
- Blob ids equal at both revisions: C1 `df214578de1316820e3ccefbada56246c033b790`, C2 `505d3d89c7a5d91e550f4ab8e5838f4834a94567` (`git rev-parse <rev>:<path>`, four calls).
- sha256 equal at freeze and master and equal to the declaration's pins: C1 `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218` (`SCORECARD.md:2117`), C2 `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8` (`SCORECARD.md:2118`).
- Bonus pin: `git show <rev>:.ufo/waves/round-38/frozen/hooks-capture/MANIFEST.sha256 | sha256sum` = `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd` at both 7cbaeb6 and master — equals the C2 row's MANIFEST pin. Receipts: receipts-02-counter-bytes.txt.

## (c) Predicate sentence identity — HOLDS byte-for-byte

Mechanical check (python3: substring count + JSON field equality; full output in receipts-03-predicate-identity.txt):
- C1 sentence `fixtures_matched == FIXTURES_EXPECTED and live_match == 1 and six_planes_all == 1`:
  - `SCORECARD.md:2117` Target column — exactly 1 occurrence in the file;
  - `tools/score-storage-arm-r38.py:7` (docstring) and `:232` (emitted `predicate` constant) — 2 occurrences; the docstring appends only `  -> PASS, exit 0` to the otherwise identical sentence;
  - `.ufo/waves/round-38/before/c1-before.json:5` and `.ufo/waves/round-38/after/c1-after-52ffd65.json:5` — `predicate` field equals the sentence exactly (True).
- C2 sentence `rows_expected == rows_matched and mismatches == 0 and extra_rows == 0 and source_ok == 1`: same pattern — `SCORECARD.md:2118`, `tools/check-hook-order-r38.py:8` and `:207`, `before/c2-before.json:5`, `after/c2-after-1fe28e7.json:5`, all exact.
- No cross-contamination: 0 occurrences of each sentence in the other claim's artifacts.
- The pre-seat amendment could not have shifted them: `git diff 7cbaeb6 master -- SCORECARD.md` = 31 insertions, 0 deletions (amendment appended at `:2133`); declaration section byte-unchanged, matching the amendment's own "the v1 predicates above stay frozen and unchanged" (`SCORECARD.md:2139`).
- Receipt-to-declaration coherence: both before receipts carry revision = branch_tip = 8bd001f (base), result FAIL, exit 1, with field values matching the declaration's "Before at base" cells (C1: fixtures 0/10, live_match 0, six_planes_all 1 — c1-before.json; C2: rows_matched 0/69, source_ok 0 — c2-before.json). After receipts: branch_tips 52ffd65 / 1fe28e7, PASS, exit 0.

## Findings (no mismatch on the item; two durability notes)

1. The declared after receipts (`.ufo/waves/round-38/after/c1-after-52ffd65.json`, `c2-after-1fe28e7.json`) are UNTRACKED at master: `git ls-tree -r --name-only master -- .ufo/waves/round-38` lists no after/ path, and `git status --porcelain` shows `?? .ufo/waves/round-38/after/` (1 of 10 untracked entries; zero modified tracked files). The declaration's PASS evidence currently exists only in the working tree and would be destroyed by any clean/prune of untracked files. Not a freeze breach (the freeze claim never included after receipts), but they should be committed when the wave lands.
2. All quoted bytes were taken from git objects, so none of the above depends on working-tree state — except finding 1's two files, read as files.

Not performed (outside this item, for other seats): running either counter or the q82 counter; per-file verification of the capture against MANIFEST.sha256 entries (only the manifest self-hash pin checked); judging HO1–HO7; scoring the controls.

Receipts: `.ufo/waves/round-38/w1/RevFreezeOrder/receipts-01-history.txt`, `receipts-02-counter-bytes.txt`, `receipts-03-predicate-identity.txt`.
