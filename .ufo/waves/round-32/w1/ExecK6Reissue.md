# ExecK6Reissue — round-31 spot-check routed defect 5 (K6 receipt provenance)

Verdict: the re-issued K6 receipt reproduces `new_sourced` 8 of 8 with a `run-receipt.py` header and a footer `exit_code` of 0, and the re-issued control commit is byte-identical in tree to the original round-31 K6 commit.

## 1. [obs] The re-issued receipt reproduces 8 of 8 with the required header, tool digest and exit code

The receipt at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w1/ExecK6Reissue/c1-K6-reissued.jsonl:1` is a `run-receipt.py` JSON-lines receipt with a header line naming the measured revision, the tool revision, the tool and the tool digest, and a footer line carrying `exit_code`.

- header `revision`: `f05e12b13ba34eee1deaf2557c46c7caca5d57c3` (`.ufo/waves/round-32/w1/ExecK6Reissue/c1-K6-reissued.jsonl:1`)
- header `tool_revision`: `f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c` (`:1`)
- header `tool`: `tools/check-btrfs-repair-r31.py` (`:1`)
- header `tool_sha256`: `4f69a109e9b56b3fcba0df5a3555f7ff833b6b04fff28176060efe82ebde5cb8` (`:1`)
- footer `exit_code`: `0`, `timed_out`: `false`, `stderr_tail`: `""` (`:11`)
- summary line: `{"predicate": "new_sourced", "new_sourced": 8, "of": 8, "revision": "f05e12b1…", "base": "2077e2fa4fa70ea79aa77b6d91f4acd35bc54897", "counter_sha256": "4f69a109e9b56b3fcba0df5a3555f7ff833b6b04fff28176060efe82ebde5cb8"}` (`:10`)
- the eight per-question rows each read `{"id": "Qnn", "new_sourced": true, "fail": []}` (`:2`–`:9`)

The header `tool_sha256` equals the frozen counter digest named in the assignment (`4f69a109…`) and equals the digest of the counter bytes at `f4861f4d`: `git show f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c:tools/check-btrfs-repair-r31.py | sha256sum` → `4f69a109e9b56b3fcba0df5a3555f7ff833b6b04fff28176060efe82ebde5cb8` (exit 0). The counter's own self-reported `counter_sha256` on the summary line is the same value.

Command run (exit 0, output `{"out": "…/c1-K6-reissued.jsonl", "revision": "f05e12b1…", "tool": "tools/check-btrfs-repair-r31.py", "exit_code": 0}`):

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && timeout 3000 python3 tools/run-receipt.py \
  --lane /fast/scratch/hyaku/tsukuroi-r32/ExecK6Reissue/repo \
  --revision f05e12b13ba34eee1deaf2557c46c7caca5d57c3 \
  --tool-revision f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c \
  --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w1/ExecK6Reissue/c1-K6-reissued.jsonl \
  --timeout 2900 -- tools/check-btrfs-repair-r31.py --revision '{rev}' --lane '{lane}'
```

## 2. [obs] The counter's real CLI was checked before the run and is the one used

`tools/check-btrfs-repair-r31.py` at `f4861f4d` takes `--revision <REV>` (required) and `--lane <repo>` (optional, defaults to the repository two levels above the tool): `/fast/scratch/hyaku/tsukuroi-r32/ExecK6Reissue/re31-source/tools/check-btrfs-repair-r31.py:186`–`:187` (`ap.add_argument('--revision', required)`, `ap.add_argument('--lane', default=os.path.dirname(...))`). It exits 0 when `new_sourced == 8`, 1 otherwise, 2 on a harness error (`:303`). The receipt invocation uses exactly `--revision '{rev}' --lane '{lane}'`, which `run-receipt.py` substitutes with the full revision hash and the lane path (`tools/run-receipt.py:93`).

## 3. [obs] The re-issued control commit is byte-identical to the original round-31 K6 commit

The original K6 commit `c355dac64afa2b85a6b7ba79750a0f677c9a4e74` was scored against the base `8cff9e7cfb034b49c645d548801ac3185a827cb4` (parent), and the K6 rows were built by the round-31 seat's `build-k6.py` from that base.

- original K6 tree: `dea2220cf953e1f492e37cf0929331d685cf129e`
- re-issued K6 tree: `dea2220cf953e1f492e37cf0929331d685cf129e` (identical)
- the two `format-patch` bodies are byte-identical: `diff` of the two patch bodies exits 0, and both files have sha256 `68129fd760197e42f43ce6d87e8034d5395b502f1238b239e26f3a51e2b294c8` — `/fast/scratch/hyaku/tsukuroi-r32/ExecK6Reissue/original-k6-patch-body.diff` and `/fast/scratch/hyaku/tsukuroi-r32/ExecK6Reissue/reissued-k6-patch-body.diff`
- `git apply --check` of the kept patch against the base `8cff9e7` exits 0

The re-issued commit differs from the original only in the committer identity and timestamp (the sandbox contract requires `ctl <ctl@sandbox>`; the original used `control <control@invalid>`). The re-issue was produced by re-running the round-31 seat's own `build-k6.py` unchanged except for that one identity line (`diff` of the two builder copies shows exactly one changed line, 173).

The six committed snapshots are pinned to the counter's frozen values:

```
Defragmentation.rst   71ad07a3f200284b01d6ee18fc4cc8732fe0542b80556e2cc798247505daa60b
btrfs-rescue.rst      838504fe8b00d221e017457e7953717f3ca2a0e886a48a4c457367b8c4063a1d
btrfs-check.rst       927b67b4ab13f681866e699fcd6ea4917a42ef08e4db1731b0adf065022d955c
ch-mount-options.rst  aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f
btrfs-replace.rst     da4bf595f072a96a309535c1022b0171a8657a4f207a3d3da73250886fd8bc9e
Trim.rst              2a114d56f29d727002a981e868cc97e89d7dd77a5e1cf42ad5a9ff05bfcf0ffc
```

These are the `pin` values of `QUESTIONS` Q01–Q08 in the counter (`/fast/scratch/hyaku/tsukuroi-r32/ExecK6Reissue/r31-source/tools/check-btrfs-repair-r31.py:60`–`:88`), so the frozen pin check R3 holds at the re-issued revision.

## 4. [obs] The payload of the re-issued receipt matches the original ad-hoc JSONL row for row

The original round-31 receipt `.ufo/waves/round-31/w2/CritKeyFillerControl/c1-K6-download-not-read.jsonl` holds eight `{"id": "Qnn", "new_sourced": true, "fail": []}` rows and the summary `new_sourced 8 of 8`. Diffing the original nine payload lines against the re-issued receipt lines 2–10, with only the `revision` field normalised, exits 0. The only difference is the summary's `revision` field, which now names the re-issued commit `f05e12b1…` instead of `c355dac…`. This is the whole of routed defect 5: the ad-hoc JSONL plus `k6-result.json` is replaced by a receipt with a header and an `exit_code`.

## 5. [obs] The same receipt was also re-issued against the original K6 commit itself

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w1/ExecK6Reissue/c1-K6-original-commit.jsonl` runs the same frozen counter at the original commit `c355dac64afa2b85a6b7ba79750a0f677c9a4e74` through `run-receipt.py`. Header `tool_sha256` `4f69a109…`, `tool_revision` `f4861f4d…` (`:1`); eight `new_sourced: true` rows (`:2`–`:9`); summary `new_sourced 8 of 8` (`:10`); footer `exit_code` `0`, `timed_out` `false` (`:11`). Command exit 0. So the 8-of-8 result is a property of the frozen counter and the frozen rows, not of the re-commit.

## 6. [obs] The counter is shown able to fail on the same frozen bytes (negative control)

The same `run-receipt.py` invocation against the K6 base `8cff9e7cfb034b49c645d548801ac3185a827cb4` exits 1, with all eight questions failing (`R1 entry absent at revision`, `R1 0 rows for Qnn`) and summary `new_sourced 0 of 8`: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w1/ExecK6Reissue/c1-K6-base.jsonl:1`–`:11`. The receipt is therefore not vacuously passing, and the `exit_code` in the footer discriminates 0 from 1.

## 7. [obs] Containment

No git or jj write was run in the lane or the fleet repo. All commits were made inside `/fast/scratch/hyaku/tsukuroi-r32/ExecK6Reissue/` only, with `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` unset on every git invocation. The sandbox origin push URL is `DISABLED`. No commit authored by `ctl <ctl@sandbox>` exists anywhere in the lane (`git log --all --format='%an <%ae>' | grep -c 'ctl@sandbox'` → 0), and `git ls-files .ufo/waves/round-32/w1/ExecK6Reissue/` returns 0 tracked files: the seat's evidence is untracked in the lane, as the wave contract requires. The lane `HEAD` moved during this seat's run (`5dc2c9e` → `44c8eee`) from other seats' commits; neither is this seat's, and neither contains this seat's work.

## 8. [unk] What this seat does not establish

The re-issue confirms provenance of the receipt and reproducibility of the 8-of-8 count. It does not adjudicate the round-31 substantive objections that remain open elsewhere: whether the K6 control should be counted as a valid pre-data control for the depth axis (QUALITY 80/81), and the key-holder editing defect (R31-KEY-SPELLING). Those are other seats' calls.

## Evidence files (all under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w1/ExecK6Reissue/`)

| File | sha256 | What it is |
|---|---|---|
| `c1-K6-reissued.jsonl` | `6457da335d876515bf8da5801a2be7b2638002ff718c025682b71385f466a998` | the re-issued K6 receipt at the re-issued commit (8 of 8, exit 0) |
| `c1-K6-original-commit.jsonl` | `caaa3d1fd1d7178699083a3ac8b42b7e038730cf4825c72ff0d911ae4a14fb08` | the same receipt at the original K6 commit `c355dac` (8 of 8, exit 0) |
| `c1-K6-base.jsonl` | `8c749f1fcb223168d43d94f4058847cf8281448944c47d4cf2a6e1eee0af4e63` | negative control at the K6 base (0 of 8, exit 1) |
| `c1-K6-reissued.patch` | `555ef21cc42ea9556fd7488bedd06032a4cfacd750018428672bc22e9d3daa7f` | the K6 patch (`format-patch -1 --stdout` of `f05e12b1`); body byte-identical to the original K6 patch body |

Sandbox: `/fast/scratch/hyaku/tsukuroi-r32/ExecK6Reissue/` (`repo` = lane clone with the re-issued K6 commit, `r31-source` = clone of the round-31 seat's sandbox holding the original K6 commit, `k6-builder`/`k6-final`/`k6-ctl` = builder scratch outputs, `build-k6-ctl.py` = the builder copy with the sandbox commit identity).

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/CritKeyFillerControl/{build-k6.py,k6-result.json,c1-K6-download-not-read.jsonl}, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-31-verifier-spotcheck.md:160-168, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:137-159, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/run-receipt.py, tools/check-btrfs-repair-r31.py at f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w1/ExecK6Reissue.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w1/ExecK6Reissue/{c1-K6-reissued.jsonl,c1-K6-original-commit.jsonl,c1-K6-base.jsonl,c1-K6-reissued.patch}; executed=git clone/checkout/log/cat-file/show/diff/ls-tree/ls-files (read-only in the lane, read-write in /fast/scratch/hyaku/tsukuroi-r32/ExecK6Reissue), python3 build-k6.py (round-31 seat's builder, sandbox), python3 tools/run-receipt.py (3 runs: K6 re-issued, K6 original commit, K6 base negative control), curl -sL (one pin probe for Trim.rst), sha256sum, diff, format-patch, git apply --check
Model: minimax-code/MiniMax-M3.1-Flash
Installs: none
