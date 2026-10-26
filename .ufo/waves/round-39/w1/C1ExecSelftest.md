VERDICT: supports

Seat C1ExecSelftest, item C1-12: run the census `--selftest` against the implementation file
(49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82) and the base file
(0eff65b21bb81195ee06c96a83afbd7a07e52eef), expect 117/117 and 113/113, snapshot `/tmp`
around each run, and diff the PASS label lists. All four expectations hold; no `/tmp` entry
from this seat's runs.

## 1. File identity (verified before and after the runs)

- `git -C <lane> diff --quiet 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82 -- tools/tsukuroi-census.sh`
  → rc 0 (checked at dispatch and again after all runs). The tested file is the declared
  implementation commit's content.
- `git show 49cc53c7...:tools/tsukuroi-census.sh` sha256 `e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d`
  = sha256 of the working-tree `tools/tsukuroi-census.sh` (same value observed on both).
- Base: `git show 0eff65b2...:tools/tsukuroi-census.sh` → sha256
  `6a675a4e06939e451bb6d1f7eb50f783b61c435e0d9d1efc983a0c7dfc81c33d`, 3054 lines
  (`w1/C1ExecSelftest/script-shas.txt`; snapshots `census-base.sh`, `census-impl.sh`).
- `git diff --stat 0eff65b2... -- tools/tsukuroi-census.sh` at the tested file:
  `45 insertions(+), 1 deletion(-)`.

## 2. Implementation selftest — 117/117 (expected 117/117)

    TMPDIR=/fast/scratch/hyaku/tsukuroi-r39/C1ExecSelftest bash tools/tsukuroi-census.sh --selftest
    rc=0
    TSUKUROI_CENSUS_SELFTEST: PASS (117 cases, 117 passed, 0 failed)

Observed twice: plain run (`w1/C1ExecSelftest/impl-selftest.out`) and under a
seccomp-filtered narrow strace (`impl-selftest-3.out`, rc 0, same 117/117). stderr was 0
bytes in both clean runs (no `FAIL` lines).

## 3. Base selftest — 113/113 (expected 113/113)

    TMPDIR=<scratch> bash <scratch>/census-base.sh --selftest     # cwd = scratch
    rc=0
    TSUKUROI_CENSUS_SELFTEST: PASS (113 cases, 113 passed, 0 failed)

Observed three times: two plain runs from the scratch cwd (`base-selftest.out`,
`base-selftest-2.out`), one from the lane cwd (`base-selftest-3.out`), all rc 0, 113/113,
0-byte stderr.

## 4. PASS label delta — every old label retained, exactly 4 added

Method: `sed -n 's/^PASS //p' <out> | LC_ALL=C sort` on both outputs, then
`LC_ALL=C comm -23` / `comm -13` (`base-labels.txt` 113 lines, `impl-labels.txt` 117 lines).

- Base labels missing from impl: **0** (`missing_from_impl=0`).
- Added in impl (4, all R39-C1):

      healthy rollup: btrfs mounted with no sysfs root is BLOCKED, never 0/0/0 (R39-C1) (exit 0, HEALTHY)
      healthy rollup: btrfs mounted with a root holding no fsid is BLOCKED (R39-C1) (exit 0, HEALTHY)
      healthy rollup: an unreadable mount table with no sysfs root is BLOCKED (R39-C1) (exit 0, HEALTHY)
      healthy: a root with an fsid entry is read and the mount table adds nothing (R39-C1) (exit 0, HEALTHY)

These are the four declared cases in the script at tools/tsukuroi-census.sh:2976, :2981, :2986,
:2991, and their `check` regexes assert exactly the declared strings:
`detail=mounts:btrfs-without-sysfs` (:2977, :2982), `detail=mounts:unreadable` (:2987), and a
detail-free HEALTHY on a populated root (:2992). 113 + 4 = 117, consistent.

## 5. /tmp snapshots

`ls -A /tmp | sort` immediately before and after each run
(`tmp-before-impl.txt`, `tmp-after-impl.txt`, `tmp-before-base.txt`, `tmp-after-base.txt`,
`tmp-final.txt`; 126 entries at baseline).

- Implementation run: before == after, **identical, 126 → 126, no delta**.
- Base run: before 126 → after 127, delta `> tsukuroi-r3-2-selftest.cwR12b`. That name is
  absent from the next full snapshot (`tmp-final.txt`); immediately after the base run
  `ls -Ad /tmp/tsukuroi-r3-2-selftest.*` instead listed a *different* transient peer dir,
  `/tmp/tsukuroi-r3-2-selftest.BVaOO2`, which also disappeared later. It is **not from this
  seat**:
  - the script has exactly one `mktemp` (`tools/tsukuroi-census.sh:1925`,
    `work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")`); the base copy's is
    the same construct (base line 1906). Both runs exported `TMPDIR` to this seat's scratch,
    and the scratch tree holds no leftover work dir after either run (trap removed it).
  - narrow strace of the *same* commands (mine, `--seccomp-bpf -f -e trace=mkdir,mkdirat,
    creat[,rename,renameat]`) shows `tmp_refs=0` — zero references to any `/tmp` path across
    107003 traced lines (impl) and 102735 (base); `strace-summary.txt`. Every absolute path
    outside my scratch in those traces is a single `/fast` from `mkdir -p` on my own TMPDIR
    chain, returning `EEXIST`.
  - all concurrently running census processes visible during the runs carry `TMPDIR` under
    `/fast/scratch/hyaku/tsukuroi-r39/...` (`ps -eo pid,args` + `/proc/<pid>/environ`), i.e.
    the transient `/tmp` dir comes from a peer seat's run outside this seat's process tree,
    not from mine.
- Final snapshot vs the pre-impl snapshot differs by peer activity only (`r39idmap`,
  `stormchart-audio-qSJfA5` added); no `tsukuroi-r3-2-selftest.*` entry remains after
  `tsukuroi-r3-2-selftest.cwR12b` disappeared.
- **No-harm deviation, disclosed exactly.** `/tmp/x` was already present in my very first
  snapshot (`tmp-before-impl.txt` line 115) — it pre-existed this seat. While collecting the
  label-diff evidence I ran `sed … | sort > /tmp/x`, which overwrote it, and then moved it to
  scratch and deleted it in the same command; `tmp-final.txt` shows `x` gone. So this seat
  destroyed a pre-existing `/tmp` entry that it did not create (its original content was
  already lost to the redirect, so nothing is recoverable). A second redirect target,
  `/tmp/.c1es-final`, was created and deleted by me inside the post-run verification command
  (it appears in no snapshot interval). Both are evidence-collection artifacts of my own
  shell pipelines; neither came from the census selftest, which wrote no `/tmp` path.

## 6. Observations (not defects against the claim)

- **Case count is PASS+FAIL.** Under a heavyweight `-e trace=%file` strace the run degraded to
  `118 cases, 105 passed, 13 failed`, with `exit 143 wanted 0` on one case and one fail-only
  guard `fixture mutated by census run` (`bad` at :2121 has no `ok` counterpart), i.e. the
  extra "case" is an error counter, not a new test. Two cases also fail inside
  `unshare -rm` (`impl-ns.err`): `unreadable directory` and `unlistable btrfs sysfs root`
  rely on mode-000 fixtures, which root-in-userns bypasses via CAP_DAC_OVERRIDE. So the suite
  is stable at 117/117 only for a plain unprivileged run; isolation that grants namespace
  caps or ptrace slowdown is not a valid harness for it. Both my clean runs were plain
  unprivileged invocations.
- **Coverage note on the fourth R39 case** (:2991): it asserts a populated root yields
  `state=HEALTHY filesystems=1 devices=1 nonzero=0` with no `detail`, but its `mounts` fixture
  is benign, so it cannot distinguish "never reads the table" (the claim's wording) from
  "reads and ignores it". The implementation is guarded by
  `if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]` (tools/tsukuroi-census.sh:1903), so the
  behavior matches the claim; a leg that would pin it without the code being read is a
  populated root plus an absent/unreadable `TSUKUROI_PROC_MOUNTS`, expecting the same
  detail-free HEALTHY. Flagging for the mutation seats, not asserting a failure.
- "Unreadable table" is exercised as a **missing** table (`rm -f "$FX/mounts"` at :2985, before
  the :2986 case), which the implementation reports as `mounts:unreadable`; permission-based
  unreadability cannot be built unprivileged (same CAP_DAC_OVERRIDE issue).

## 7. Bounds, no-harm, tooling

- Wrote only this report and `w1/C1ExecSelftest/` receipts. No lane file edited, no git/jj
  mutation, no host mutation, no pacman. `git status --porcelain` in the lane shows only
  pre-existing/concurrent peer entries (`PROVINCE.md`, `SKILL.md`, the untracked
  `.ufo/waves/round-39/w1*` dispatch files) — none authored by this seat.
- All clones/fixtures/artifacts lived under
  `/fast/scratch/hyaku/tsukuroi-r39/C1ExecSelftest/`; scratch removed after receipts were
  copied (`trap`-free explicit `rm -rf` on my own dir, after the copy).
- Tools installed or upgraded: none.
- Not done (out of scope for C1-12): no live census run, no counter run
  (score-storage-hidden-r39.py / check-transaction-order-r39.py), no TO-row judgement, no
  mutation testing of the four new cases.
