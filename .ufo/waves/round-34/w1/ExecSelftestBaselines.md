# ExecSelftestBaselines — no-harm selftest baselines at `6de666c4`

**Verdict: BASELINE ESTABLISHED (no-harm seat, not a control).** At `6de666c427ba9aa6b4350561980bde8d0e7c261d`,
all **31** targets exit **0** with **empty stderr**, **no timeout**, and **30 of 31** are byte-identical
on an independent second run; the single exception, `check-revision-binding.py`, differs only in its
own randomly generated commit hex (hex-normalised digests are equal). Table:
`.ufo/waves/round-34/w1/ExecSelftestBaselines/selftests-6de666c4.tsv`
(31 data rows + header, sha256 `8d94874f1a56ce6db0063409baca6f24af698403cbc1f3e50cc7c774d4ee0716`).
The nine C1 claim targets all pass and are deterministic.

## Findings

1. **[obs] The table covers the assigned set exactly — nothing missing, nothing extra.**
   Derivation: `grep add_argument('--selftest')` over `tools/*.py` gives 29 files; 28 of those contain
   the text `_revision`; `tools/_revision.py` carries its own argv-based `--selftest` without argparse;
   and the two btrfs claim targets have **no** `--selftest` mode at all
   (`grep -c selftest tools/check-btrfs-repair-r31.py tools/check-btrfs-space-r30.py` → `0`, `0`;
   their only flags are `--revision`/`--lane` at `tools/check-btrfs-repair-r31.py:185-187` and
   `tools/check-btrfs-space-r30.py:370-375`). So 28 selftest rows + 2 btrfs rows in the ordinary
   revision-mode form the item names = 30, plus `tools/_revision.py` = **31**; a set-difference
   check of the final table against that definition prints `missing: []`, `extra: []`.
   The only `--selftest` tool with no `_revision` mention, `tools/check-adjacency-overlap.py`, is
   outside the item's criterion; I ran it anyway for the record: exit 0, 96 cases, 0 failed,
   1 line, sha256 `0c664f8bc7ab990197a9cb4fdb529df059746df3dfef80b6f864318d8852cffa`
   (`/fast/scratch/hyaku/tsukuroi-r34/ExecSelftestBaselines/out/x-check-adjacency-overlap.out`).

2. **[obs] All 31 rows: exit 0, stderr empty, no timeout.**
   Column `stderr_sha256` is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
   (the empty string) on every row; `timed_out` is `False` on every row; the distinct values of
   `exit` are exactly `{0}`. Runner: 3 concurrent processes for pass A, 2 for pass B, each command
   `timeout 900 python3 tools/<t> --selftest` from the clone root with every `GIT_*` name removed
   from the ambient environment (the ambient shell had only `GIT_EDITOR`, `GIT_PAGER`,
   `GIT_TERMINAL_PROMPT`; no `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` were ever set).

3. **[obs] The nine C1 claim targets, exact rows** (exit, stdout sha256, second-run sha256):

   | target | args | exit | stdout sha256 | run B | wall s |
   |---|---|---|---|---|---|
   | check-boot-chain.py | `--selftest` | 0 | `507a5ce1b9c01ed2a6d1e400da5a2afd6facf72278aa470fb5590708729e2333` | same | 0.10 |
   | check-btrfs-repair-r31.py | `--revision 6de6… --lane <clone>` | 0 | `fa54b24b1118760e0be0d86ce441cb6a3b429039ebb7c1f3503968f2ceb28400` | same | 0.10 |
   | check-btrfs-space-r30.py | `--revision 6de6… --lane <clone>` | 0 | `636e472cbc50caaab4e64d38e1b29cde286118ba16142cf78daa696ddf0fb249` | same | 0.09 |
   | check-locator-clarification.py | `--selftest` | 0 | `b5f4a469a3fbaa7e7f9f1d6fc4c86e0dc1ef151e1a49ec0d821fc56f9e45392e` | same | 0.09 |
   | check-recheck-commands.py | `--selftest` | 0 | `5d104ee1c5a7899d2af26003532862eca287f08b1398003e9261f105266d62e1` | same | 0.79 |
   | check-section-citations.py | `--selftest` | 0 | `be669c8652a16df582fbc9d560ede0a05268392ff07ce1d35e4ce928ee009f84` | same | 0.11 |
   | check-seat-scope.py | `--selftest` | 0 | `2b360f56f8979c379790d22caaa0dc3354a20b69fc51575f6b6e6fd0454a25cc` | same | 0.43 |
   | check-source-scope-correction.py | `--selftest` | 0 | `b1573af505903a0c4a5e6729c25c4ac082dd2477a5a3a602b950616bbc75ca2f` | same | 0.58 |
   | measure-update-recheck.py | `--selftest` | 0 | `e9ae5375a31c2808145daa79f130528b890f64bec22a47cfa1d592e7a8f01473` | same | 0.64 |

   Content of those stdout lines (verbatim, last line of each): `CHECK_BOOT_CHAIN_SELFTEST: PASS
   (83 cases, 83 passed, 0 failed)`; `{"predicate": "new_sourced", "new_sourced": 8, "of": 8,
   "revision": "6de666c4…", "base": "2077e2fa…", "counter_sha256": "4f69a109…"}`;
   `{"revision": "6de666c4…", "verified": 10, "of": 10, "unverified": [], "counter_sha256":
   "4953203d…", "counter_version": 2}`; `CHECK_LOCATOR_CLARIFICATION_SELFTEST: PASS (37 cases, 37
   passed, 0 failed)`; `{"selftest": {"cases": 95, "failures": [], "passed": 95, "status": "PASS"}}`;
   `CHECK_SECTION_CITATIONS_SELFTEST: PASS (68 cases, 68 passed, 0 failed)`;
   `CHECK_SEAT_SCOPE_SELFTEST: PASS (54 cases, 54 passed, 0 failed)`;
   `CHECK_SOURCE_SCOPE_CORRECTION_SELFTEST: PASS (29 cases, 29 passed, 0 failed)`;
   `MEASURE_UPDATE_RECHECK_SELFTEST: PASS (20 cases, 20 passed, 0 failed)`.

4. **[obs] Non-deterministic stdout: exactly one row.** `tools/check-revision-binding.py --selftest`
   printed 3 lines with sha256 `a002261de774f44d4fa1224ee8fe35f449c7b66d017e72f0c6f0ba50604f28fb`
   on pass A and `385f1ad2721187500b1dccf0ef0b96b80ba965a7712c425dc2ff03b8944576ca` on pass B
   (both exit 0, 3 lines, length identical at 2184 bytes). The varying bytes are the tool's own
   random fixture commit ids, e.g. `"shadow_ref": "refs/heads/4b4aa15"` / `"refs/heads/2115a3d"`
   inside `TARGET_TYPE_GENERIC_PEEL_WITNESS`; after replacing 7–64-char hex runs and `/tmp/…`
   paths the two outputs hash equal, so the row is recorded as `deterministic=no-hex-only`.
   **Consequence for the after-change comparison:** for this row compare line 3
   (`CHECK_REVISION_BINDING_SELFTEST: PASS (78 cases, 78 passed, 0 failed)`), the line count, the
   exit code or a hex-normalised digest — never the raw digest.

5. **[obs] Timing headroom.** Every row except `check-revision-binding.py` finished in **≤ 1.16 s**
   (`check-kernel-taint.py`), the two btrfs revision-mode rows in 0.09–0.10 s. `check-revision-binding.py`
   took **135.74 s** (pass A) and **144.71 s** (pass B) because it builds nested git fixtures. All are
   far inside the 900 s per-tool bound, but it is the only row where the after-change run could
   plausibly approach the bound if the new allow-list slows child spawns.

6. **[inf] These rows are sensitive to the builder C1 changes, so "same digest" is a real no-harm test.**
   The selftests drive the same spawn path through the code that composes the child environment:
   `tools/check-recheck-commands.py:798-803` `git()` builds
   `{key: value for … if not key.startswith("GIT_")}` and is exercised by the selftest through
   `sandbox_git()` (`:1071-1093`) and `case()` (`:1100-1135`); `tools/check-btrfs-repair-r31.py:107-110`
   `clean_env()` is the git environment for the revision-mode rows; the other targets carry the same
   ambient-copy shape at `check-boot-chain.py:802`, `check-locator-clarification.py:448,577`,
   `check-section-citations.py:406,568`, `check-seat-scope.py:174`,
   `check-source-scope-correction.py:355`, `measure-update-recheck.py:438,485`. A builder that drops a
   name git needs changes these exit codes or stdout; one that keeps git working should leave the
   digests unchanged. [unk] whether the declared allow-list will actually leave every join/spawn
   working — untested here, that is the L1's after-receipt.

7. **[obs] No harm to the sandbox clone.** After 62 tool runs the clone is clean
   (`git status --porcelain` → 0 lines) and still at `HEAD = 6de666c427ba9aa6b4350561980bde8d0e7c261d`;
   the selftests work in `mktemp` directories, and no run wrote into the lane repo, the fleet repo or
   `/home/vgpnk/Projects/shokunin`.

## Evidence retained

- Table (committed): `.ufo/waves/round-34/w1/ExecSelftestBaselines/selftests-6de666c4.tsv`,
  columns `tool, tool_sha256, args, exit, stdout_sha256, stdout_lines, stderr_sha256, stderr_lines,
  wall_s, timed_out, run_b_stdout_sha256, deterministic, note`.
- Raw stdout/stderr of both passes: `/fast/scratch/hyaku/tsukuroi-r34/ExecSelftestBaselines/out/`
  (125 files, manifest `SHA256SUMS` there, sha256 `abef824cfad051b7b6246bf5a758f2df3800a23930dd44c00398ee7ede3ea54e`).
- Drivers (scratch, not committed): `drive_selftests.py`, `merge.py` in
  `/fast/scratch/hyaku/tsukuroi-r34/ExecSelftestBaselines/`.
- Sandbox clone: `/fast/scratch/hyaku/tsukuroi-r34/ExecSelftestBaselines/repo` at `6de666c4…`,
  `origin` push URL `DISABLED`, nothing committed there (no variant was scored — this item builds
  no control).

Scope: read=`SCORECARD.md` round-34 declaration at `6de666c4`, the frozen probe docstring/target tables, `tools/*.py` (31 targets plus `check-adjacency-overlap.py`), `tools/probe-child-env-allowlist-r34.py`; wrote=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecSelftestBaselines/selftests-6de666c4.tsv`, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ExecSelftestBaselines.md`; executed=`git clone/checkout/status/rev-parse (read-only), timeout 900 python3 tools/<t> --selftest for the 28 selftest targets and timeout 900 python3 tools/check-btrfs-*.py --revision 6de6… --lane <clone> for the two btrfs targets (pass A), the same set again (pass B), plus check-self-assessment.py --selftest twice more after it was found missing from the first pass, timeout 300 python3 tools/check-adjacency-overlap.py --selftest, python3 merge.py`
Model: opencode-go/deepseek-v4.1-flash
Installs: none
