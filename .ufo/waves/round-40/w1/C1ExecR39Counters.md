VERDICT: supports

# C1-10 — no-harm for C1: round-39 STORAGE counter still PASS at lane tip, and the round-40 census change is confined to `run_selftest`

Seat: C1ExecR39Counters. Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin at tip
f951f288483c1af0cef4afd458488b84cf7a2165 (== the revision tested). Run pair:
`git diff 53b294a274656be6479aadf2ec2fee890ded77ce f951f288483c1af0cef4afd458488b84cf7a2165`.

Receipts in `.ufo/waves/round-40/w1/C1ExecR39Counters/`:
`counter-r39-at-f951f28.json` (4881 B, full counter JSON), `counter-r39-at-f951f28.err` (0 B),
`diff-confinement.txt` (all commands + observed output below).

## 1. Round-39 counter at tip: PASS, numbers identical to round 39

Command (exactly as assigned; two invocations with the same revision and options except a fresh scratch
subdirectory for the second, exit 0 both; the first stdout was truncated by my own `tail`, so the second run
captured the full JSON that is cited here):

    S=/fast/scratch/hyaku/tsukuroi-r40/C1ExecR39Counters
    TMPDIR="$S" python3 tools/score-storage-hidden-r39.py \
      --revision f951f288483c1af0cef4afd458488b84cf7a2165 --scratch "$S/s"

Observed (`.ufo/waves/round-40/w1/C1ExecR39Counters/counter-r39-at-f951f28.json`):

    counter = score-storage-hidden-r39
    revision = f951f288483c1af0cef4afd458488b84cf7a2165
    branch_tip = f951f288483c1af0cef4afd458488b84cf7a2165
    seed = 44aec4e82be22b5a853faf92d2155eb7
    predicate = hidden_matched == 2 and views_matched == 3 and fixtures_matched == 5 and live_match == 1 and six_planes_all == 1
    hidden_matched = 2
    views_matched = 3
    fixtures_matched = 5
    live_match = 1
    six_planes_all = 1
    result = PASS
    exit = 0

Per-leg matches (all `true`): H1-hidden-empty, H2-hidden-absent; views 0 `zero`, 1 `nonzero`, 2 `any`;
F1-absent-root-no-btrfs-mounted, F2-absent-root-btrfs-mounted, F3-absent-root-mounts-unreadable,
F4-populated-root-no-btrfs-mounted, F5-empty-root-btrfs-mounted; live got
`STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0` (matches the counter's own
model of the host root). Every leg printed six PLANE lines (census_exit 2 in all eleven legs, as in round 39).
Wall time ~40 s per invocation (39.77 s / 41.55 s); stderr empty.

Round-39 reference, decoded from the receipt stream of `.ufo/waves/round-39/after/c1-final-a2d7aad.jsonl`
(first object = wrapper meta, second = counter record):

    meta.revision      = a2d7aad740977088ff9fc70ed36d3ef978b27e81
    meta.tool_revision = 6a08925daa30767809eb13bb4b01448ff954d46a
    meta.tool_sha256   = 75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973
    hidden_matched = 2, views_matched = 3, fixtures_matched = 5, live_match = 1, six_planes_all = 1,
    result = PASS, exit = 0, seed = 16103a8e873896b5e13a6595602f9079

Comparison: the six predicate values and PASS/exit are identical to round 39. Only `seed` (random per run) and
`revision` (a2d7aad -> f951f28) differ, as designed.

The counter is byte-identical to the round-39 frozen one, so the comparison is apples-to-apples:

    sha256sum tools/score-storage-hidden-r39.py
      75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973   (matches the declared 75a9e8ab… and meta.tool_sha256)
    git rev-parse 53b294a:t… 6a08925:t… f951f28:t…  + git hash-object
      c502401cfa185ab80bd04728cdc7ce80f22552fa  (all four)
    tools/_revision.py blob: 24f398a6b981488218e6cb05c6c1016efa84cf29 at 6a08925, at tip, and in the worktree

Read from the source: the counter runs the census bytes from `git show <REV>:tools/tsukuroi-census.sh`
(`tools/score-storage-hidden-r39.py:184-190`), H1/H2 inside `unshare -rm` with a tmpfs over
`/sys/fs/btrfs` or `/sys/fs` (`:195-214`), V0-V2 in the same namespace with a random tree (`:216-228`),
F1-F5 through `TSUKUROI_BTRFS_SYSFS` / `TSUKUROI_PROC_MOUNTS` (`:229-254`), and L live without override
(`:255-262`). It never runs `--selftest`, so the round-40 selftest additions are not part of this measurement;
it is a pure STORAGE-arm regression check. Untracked round-40 files in the worktree cannot influence it: the
census is taken from the revision.

## 2. `git diff 53b294a f951f28 -- tools/tsukuroi-census.sh`: one hunk, inside `run_selftest`

Observed (receipt `diff-confinement.txt`):

    git diff --numstat 53b294a f951f28 -- tools/tsukuroi-census.sh
      36	0	tools/tsukuroi-census.sh
    hunk count: 1
    hunk header: @@ -3006,6 +3006,42 @@ STUB

Function extents, from `grep -nE '^(probe_storage_arm|run_selftest|main)\(\) *\{|^\}'` with `}` closers:

    BASE 53b294a: probe_storage_arm L1865-1925; run_selftest L1928-3019; main L3022-3112
    TIP  f951f28: probe_storage_arm L1865-1925; run_selftest L1928-3055; main L3058-3148

Attribution: the hunk's old range L3006-3011 (3 context + 3 context lines) and new range L3006-3047 (42
lines) both lie inside `run_selftest` (base L1928-3019, tip L1928-3055). The insertion point is between the
existing `storage-mounts-empty` check and the `check_cli 'cli: unknown argument…'` check, i.e. still before
`run_selftest`'s closing `}` (base L3019, tip L3055) and well before `main()` (tip L3058). The added lines use
only helpers defined earlier inside the same function: `fx_default` (L2022), `$sfs` (L2925), `st_write`
(L2926).

The hunk header's trailing `STUB` is not a function name: git's funcname heuristic matched the heredoc
terminator line `STUB` at L2010 (opened by `cat > "$bin/.dispatch" <<'STUB'` at L1937). The enclosing shell
function has to be established by line extents, which is what the table above does; a reader should not treat
`@@ … @@ STUB` as evidence that the change is outside any function.

`probe_storage_arm` is unchanged byte-for-byte between base and tip (the one hunk is 36 insertions, 0
deletions; `diff` of L1865-1925 base vs tip prints nothing → `IDENTICAL`), consistent with the declaration's
"probe_storage_arm is NOT changed". No other file is in scope of this diff command, and the diff contains no
reference to `probe_storage_arm` (grep → NONE).

## 3. Scope, host and evidence discipline

- Wrote only this report and the three receipts in `.ufo/waves/round-40/w1/C1ExecR39Counters/`. No tracked
  lane file was touched; `git status --porcelain` after the runs lists only entries produced by other seats or
  the parent (`.ufo/waves/round-40/make-w1-spec.py` modified; round-40 dispatch/spec/ready files and
  `corpus/lessons/round-40.md` untracked), none by this seat.
- Host untouched: the counter's only privileged-looking action is `unshare -rm` inside its own child; fixture
  legs are env overrides over private temp dirs. No mount, service, package, hook or `/etc` change; no sudo.
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/C1ExecR39Counters/{s,s2}` was `rm -rf`'d after the receipts were
  copied out (verified: directory gone). TMPDIR was set there for both invocations.
- Tool installs: none.
- Not run by me (outside this item, and the wave forbids it): `tsukuroi-census.sh --selftest` at tip, the
  round-40 counters (`score-selftest-literals-r40.py`, `check-exec-environment-r40.py`), build/lint/tests,
  and any gate. This item adjudicates only the round-39 counter no-regression and the census diff confinement.

## Residual risk

- Confinement is established by line-range attribution plus the absence of other hunks, not by an AST; the
  census is shell, so line extents are the strongest available static evidence. Any future edit inserted above
  L3055 would shift these numbers, so the cited extents are revision-bound.
- `census_exit` is 2 in every leg (same as round 39). The counter's predicate does not require exit 0, only the
  exact STORAGE line plus six PLANE lines; the consistency across rounds means this is not a round-40 change,
  but it is worth knowing that `six_planes` and `match` are the real pass conditions.
- The two invocations used different random seeds; both PASS, so the view legs are not seed-lucky on this run,
  but this is a single seed pair, not a seed sweep (the round-39 design draws its own seed per run).
