# SelftestsAfterNoHarm — 31-row selftest re-run at `879daa95`

**Verdict: NO HARM.** All 31 rows of the wave-1 baseline re-run at `879daa95` with the same
arguments (the two btrfs revision-mode rows with `--revision 879daa95… --lane <this clone>` per the
item) exit 0 with empty stderr and no timeout: 28 rows are byte-identical on stdout, and the 3
remaining rows differ exactly where the item says they may — the two btrfs rows in the revision echo
and their own `counter_sha256` field, `check-revision-binding.py` in its random fixture hex only
(normalised digest equal). Zero unexplained differences; no harm found.

## Findings

1. **[obs] The row set and arguments match the baseline, and the changed tool bytes are exactly the
   nine C1 targets.** The re-run table has 31 rows, `missing=[]`, `extra=[]` against
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecSelftestBaselines/selftests-6de666c4.tsv`
   (31 data rows; sha256 `8d94874f1a56ce6db0063409baca6f24af698403cbc1f3e50cc7c774d4ee0716`).
   Re-hashing the 31 tool files in my clone against the baseline `tool_sha256` column prints exactly
   nine `CHANGED` lines and 22 silent rows:
   `check-boot-chain 91312f10→525398be`, `check-btrfs-repair-r31 4f69a109→a6f33022`,
   `check-btrfs-space-r30 4953203d→3539c41d`, `check-locator-clarification cd24d07c→7309f6db`,
   `check-recheck-commands 9dc46f46→1c6f349d`, `check-seat-scope add541d8→b2b70c43`,
   `check-section-citations 1546d804→149b9a21`, `check-source-scope-correction 93150445→99eec964`,
   `measure-update-recheck 0275af5a→e2d9f3e3` (command: inline `python3` hashing loop over the
   baseline TSV, exit 0). Every other argument string is identical to the baseline row, including
   `--selftest` for the 28 selftest targets and `tools/_revision.py`.
   Evidence: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/SelftestsAfterNoHarm/rows-comparison.tsv:1-32`.

2. **[obs] Baseline bytes were bound before comparison, so this is a comparison of measured bytes and
   not of labels.** Each of the 31 retained wave-1 stdout files under
   `/fast/scratch/hyaku/tsukuroi-r34/ExecSelftestBaselines/out/a-<tool>.out` re-hashes to the
   `stdout_sha256` recorded in the baseline TSV: `rows 31 unbound/missing 0` (exit 0), and that
   baseline clone is still at `HEAD = 6de666c427ba9aa6b4350561980bde8d0e7c261d`
   (`git -C /fast/scratch/hyaku/tsukuroi-r34/ExecSelftestBaselines/repo rev-parse HEAD`).

3. **[obs] All 31 re-run rows: exit 0, stderr empty, no timeout.** The distinct value of `exit` is
   `{0}`; every `stderr_sha256` is
   `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (the empty string) and every
   `timed_out` is `False`; wall time is ≤ 1.65 s on every row except `check-revision-binding.py`
   (finding 7). Evidence:
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/SelftestsAfterNoHarm/selftests-879daa95.tsv:1-32`
   (sha256 `b0856484c1f060ecf0bc87a028f823e22202f1cf4aea6c764588dc978bc0b240`).

4. **[obs] 28 of 31 rows are byte-identical on stdout, and they include seven of the nine C1
   targets.** Same stdout sha256 as the baseline for `_revision` `73a13dec`, `check-adjacency-anchors`
   `de03db09`, `check-appended-notices` `06ee6dda`, `check-boot-chain` `507a5ce1`,
   `check-boot-writers` `d5fa01c8`, `check-boundary-contract` `56fc04eb`, `check-edit-contract`
   `9decc518`, `check-freshness-r17` `16fc7ce3`, `check-kernel-taint` `f028f847`,
   `check-locator-clarification` `b5f4a469`, `check-memory-pressure` `dcb09f8d`,
   `check-path-reconciliation` `76378e95`, `check-pause-gate` `8bde2d30`, `check-recheck-commands`
   `5d104ee1`, `check-registry-coverage` `56e16ef3`, `check-report-receipts` `df0556ba`,
   `check-review-cohort` `cba93145`, `check-review-snapshots` `df1db114`,
   `check-root-dac-correction` `0d421c16`, `check-seat-bindings` `975897d2`, `check-seat-scope`
   `2b360f56`, `check-section-citations` `be669c86`, `check-selector-contract` `219ecee7`,
   `check-self-assessment` `35e28764` (260 lines), `check-source-scope-correction` `b1573af5`,
   `check-storage-health` `dacccd3f`, `measure-update-recheck` `e9ae5375`, `report-red-causes`
   `7226e2f0`. The seven C1 targets in this list are `check-boot-chain`,
   `check-locator-clarification`, `check-recheck-commands`, `check-section-citations`,
   `check-seat-scope`, `check-source-scope-correction`, `measure-update-recheck`.

5. **[obs] The two btrfs revision-mode rows differ only in the two fields the item allows: the
   revision echo and the tool's own sha256.** Line-level diffs are one hunk each
   (`@@ -9 +9 @@` for `check-btrfs-repair-r31`, `@@ -11 +11 @@` for `check-btrfs-space-r30`); every
   Q01–Q08 / D01–D10 line is byte-identical. Parsing the last line of both sides as JSON and diffing
   key by key prints exactly two differing keys per tool and no others:
   `revision 6de666c4… → 879daa95…` and
   `counter_sha256 4f69a109e9b56b3fcba0df5a3555f7ff833b6b04fff28176060efe82ebde5cb8 →
   a6f330226b31c9dcae52ca297197290e958641b52ff9ef91c00c924846194a33` (repair),
   `counter_sha256 4953203d2b03fe5e5153441ba9fdc9193683e4b38f2613322a401616b6e55eba →
   3539c41dd71a094b336dabdaa8b70281537ee29f50236c0a5e10daf7666740d1` (space). The new
   `counter_sha256` values equal the sha256 of the tool file in my clone, and `base`
   `2077e2fa4fa70ea79aa77b6d91f4acd35bc54897`, `new_sourced 8 of 8`, `verified 10 of 10`,
   `unverified []`, `counter_version 2` are unchanged. The `revision` field differs because the item
   mandates the new `--revision` argument; it is an argument-mandated difference, not a behavioural
   one. Evidence: `…/rows-comparison.tsv:8,9`, `…/compare.txt` (hunks above), and the JSON key-diff
   command output in this seat's transcript.

6. **[obs] `check-revision-binding.py` differs only in random fixture hex; its pass line is
   byte-identical.** Both outputs are 3 lines (2184 bytes). Line 2
   (`TARGET_TYPE_TREE_PREFIX_WITNESS: …`) and line 3
   (`CHECK_REVISION_BINDING_SELFTEST: PASS (78 cases, 78 passed, 0 failed)`) are exactly equal to the
   baseline bytes. Line 1 is equal in length (1932 bytes), carries 12 hex tokens at the same positions
   with equal lengths, all 12 differing (fresh fixture ids, e.g. baseline `b05a0d2d9bcce2…` vs re-run
   `260f0116874f7a…`). Applying the baseline's own normaliser (7–64-char hex runs → `<HEX>`, `/tmp/…`
   paths → `<TMP>`) gives the same digest on both sides:
   `3cdf028877ce4a8b6837a81ff898417da81c47c17c9142ceec14155cf9adc1b0`. The baseline row itself was
   already non-deterministic in the same way (`a002261de774f44d…` vs `385f1ad2721187500b…`), so this
   is the declared exception, not a harm.

7. **[obs] Timing only: `check-revision-binding.py` took 201.69 s here versus 135.74 s (pass A) and
   144.71 s (pass B) in the baseline; every other row is within 0.65 s of its baseline wall time
   (`check-recheck-commands` 0.79→1.44 s is the largest delta) and ≤ 1.65 s absolute
   (`check-kernel-taint`).** Exit code, line count and normalised bytes are unchanged, and 201.69 s is
   4.5× inside the item's 900 s `timeout` bound. Recorded as an observation; it is not an exit-code
   or stdout-digest difference, so under this item's comparison rule it is not a harm. [unk] whether
   the extra time is host load or nested-git fixture cost; this item does not measure that.

8. **[inf] The identical output on the seven non-btrfs C1 targets is a real no-harm signal for the
   allow-list change, not a tautology.** Those tools' bytes changed (nine new sha256 values,
   finding 1) while their selftest stdout did not move by one byte. The wave-1 report already
   established that these selftests drive the same child-environment builders C1 rewrote
   (`.ufo/waves/round-34/w1/ExecSelftestBaselines.md:79-86`: `check-recheck-commands.py:798-803`
   `git()`, `check-btrfs-repair-r31.py:107-110` `clean_env()`, `check-boot-chain.py:802`,
   `check-locator-clarification.py:448,577`, `check-section-citations.py:406,568`,
   `check-seat-scope.py:174`, `check-source-scope-correction.py:355`,
   `measure-update-recheck.py:438,485`). So the fixed allow-list dropped nothing that these
   ordinary and selftest spawn paths need. [unk] the reaction of paths these selftests do not drive
   (for example an ambient name a target would have forwarded to a non-git child); this item does not
   test that, and no inference about the C1 counter `leaking` count is made here.

9. **[obs] No harm to the sandbox clone.** After 31 runs the clone prints an empty
   `git status --porcelain` (0 lines) and still `HEAD = 879daa95b898b5c624c609eced31f7d0d5b933e8`;
   its push URL is `DISABLED`. The selftests work in their own temporary directories, and I wrote
   nothing into the lane repo, the fleet repo or a sibling repo; all seat writes are under the seat
   directory named below.

## Evidence retained

- Re-run table (31 rows, columns `tool,args,exit,stdout_sha256,stdout_lines,stderr_sha256,
  stderr_lines,wall_s,timed_out`):
  `.ufo/waves/round-34/w2/SelftestsAfterNoHarm/selftests-879daa95.tsv`, sha256
  `b0856484c1f060ecf0bc87a028f823e22202f1cf4aea6c764588dc978bc0b240`.
- Row-by-row comparison against the baseline, including the unnormalised/`normalised_equal` verdict
  columns: `.ufo/waves/round-34/w2/SelftestsAfterNoHarm/rows-comparison.tsv`, sha256
  `07e6702bdfb35c16143aea7cece14239d10f5d2aae17c44dc6af5a3a2f3b201f`.
- Full comparison transcript (binding lines, per-row verdicts, unified diffs of the three differing
  rows): `.ufo/waves/round-34/w2/SelftestsAfterNoHarm/compare.txt`, sha256
  `572147e03de52e7ce1ea62cf4af9613de719896e3fe7580d6ca9dcb34c34f50e`.
- Raw stdout/stderr of the re-run (62 files) under
  `/fast/scratch/hyaku/tsukuroi-r34/SelftestsAfterNoHarm/out/`, manifest copied beside the tables as
  `raw-stdout-SHA256SUMS.txt`, sha256
  `2eff5808421c00f4b01ee6458fea10565eff8c98850462c01f2ba64aeada0b09`.
- Drivers (scratch, not committed): `/fast/scratch/hyaku/tsukuroi-r34/SelftestsAfterNoHarm/drive.py`
  (3 workers, `timeout 900` per tool, `GIT_*` removed from the child environment, exactly the
  baseline's invocation shape) and `compare.py`; seat clone at
  `/fast/scratch/hyaku/tsukuroi-r34/SelftestsAfterNoHarm/repo` (at `879daa95`, push URL `DISABLED`).
- No external source was opened for this item; nothing here needs a `corpus/SOURCES.md` row.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecSelftestBaselines/selftests-6de666c4.tsv, .ufo/waves/round-34/w1/ExecSelftestBaselines.md, /fast/scratch/hyaku/tsukuroi-r34/ExecSelftestBaselines/{out/a-*.out,drive_selftests.py,merge.py}, SCORECARD.md round-34 declaration at 6de666c4, tools/check-seat-scope.py:40-100, the nine changed tool files and their git diffs 6de666c4..879daa95, wave-2 sibling report trailers; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/SelftestsAfterNoHarm.md and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/SelftestsAfterNoHarm/{selftests-879daa95.tsv,rows-comparison.tsv,compare.txt,raw-stdout-SHA256SUMS.txt} plus /fast/scratch/hyaku/tsukuroi-r34/SelftestsAfterNoHarm/{drive.py,compare.py,out/}; executed=git clone --no-local + checkout + remote-set-url--push DISABLED + read-only rev-parse/status/diff/show in /fast/scratch/hyaku/tsukuroi-r34/SelftestsAfterNoHarm/repo, sha256sum/python3 hashing loops over the two TSVs (exit 0), timeout 1200 python3 drive.py (31 rows, wall 204.15 s, exit 0), timeout 300 python3 compare.py (twice, exit 0), timeout 300 python3 JSON key-diff and hex-token check on the three differing rows (exit 0)
Model: opencode-go/deepseek-v4.1-flash
Installs: none
