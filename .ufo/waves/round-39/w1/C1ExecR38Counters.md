VERDICT: supports

Item C1-11 — round-38 C1 counters run at the round-39 census fix `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` and at
the round-39 base `0eff65b21bb81195ee06c96a83afbd7a07e52eef` (extra supporting runs at the dispatch tip
`2e1c2a40c13dc52e155d89e72f3fdd560db7399a`). The declaration's prediction holds exactly: the v1 counter FAILs 9/10
with **F06 the only changed fixture**, and the Q82 production-path counter still PASSes 3/3. No harm is attributable
to the round-38 coverage claim; the only coverage movement is the F06 fixture that encodes the superseded
R38-ABSENT-ROOT rule.

## Commands (all read-only; receipts in `.ufo/waves/round-39/w1/C1ExecR38Counters/`)

```
TMPDIR=/fast/scratch/hyaku/tsukuroi-r39/C1ExecR38Counters/tmp \
python3 tools/score-storage-arm-r38.py     --revision <REV> --scratch /fast/scratch/hyaku/tsukuroi-r39/C1ExecR38Counters/s
TMPDIR=/fast/scratch/hyaku/tsukuroi-r39/C1ExecR38Counters/tmp \
python3 tools/score-storage-arm-r38-q82.py --revision <REV> --scratch /fast/scratch/hyaku/tsukuroi-r39/C1ExecR38Counters/q82
```
Counter bytes at the lane working tree match the frozen declarations: `tools/score-storage-arm-r38.py` sha256
`e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`, `tools/score-storage-arm-r38-q82.py` sha256
`a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3` (observed by `sha256sum`; recorded in
`summary.json`). `git cat-file -t` resolves both revisions; `git merge-base --is-ancestor` confirms
base → `49cc53c7` → tip is a linear ancestry.

## Runs

| counter | revision | result | fields | receipt |
|---|---|---|---|---|
| v1 `score-storage-arm-r38.py` | `0eff65b2` (base) | PASS exit 0 | 10/10, live 1, six 1 | `v1-base.json` |
| v1 | `49cc53c7` (fix) | FAIL exit 1 | **9/10**, live 1, six 1 | `v1-49cc.json` |
| v1 | `2e1c2a40` (tip) | FAIL exit 1 | **9/10**, live 1, six 1 | `v1-tip.json` |
| Q82 `score-storage-arm-r38-q82.py` | `0eff65b2` | PASS exit 0 | 3/3, ns_available 1 | `q82-base.json` |
| Q82 | `49cc53c7` | PASS exit 0 | 3/3, ns_available 1 | `q82-49cc.json` |
| Q82 | `2e1c2a40` | PASS exit 0 | 3/3, ns_available 1 | `q82-tip.json` |

`euid_root` is `false` in every v1 run, so F10 was credited (no root-read waiver). Q82 exits 0, so its pinned
v1-model digest check (`V1_SHA256` in `tools/score-storage-arm-r38-q82.py`, model loaded from freeze
`7cbaeb6317cb9f7323d2619eec02db4e4da29449`) passed.

Prediction vs observation:
- Predicted "v1 fixture F06 now reads BLOCKED mounts:btrfs-without-sysfs and v1 FAILs 9/10 by construction" —
  observed exactly: at `49cc53c7` and at the tip, F06 returns
  `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`
  against the frozen expectation `('HEALTHY', 0, 0, 0)` (`tools/score-storage-arm-r38.py:82`, tree absent by
  construction `:98`), giving 9/10 and exit 1.
- Predicted "Q82 still PASSes" — observed 3/3 PASS at all three revisions.

## Every fixture that changed (base `0eff65b2` → `49cc53c7`)

Exactly one of ten fixtures changed; the other nine produced byte-identical `got` tuples and `storage_lines`, and
the live leg is identical at both revisions (`HEALTHY 1/1/0`, six PLANE lines, census exit 2):

| fixture | base got (match) | at `49cc53c7` got (match) |
|---|---|---|
| `F06-no-btrfs-root` | `['HEALTHY',0,0,0]` **match** — `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` | `['BLOCKED',0,0,0]` **mismatch** — `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` |

Unchanged: F01, F02, F03, F04, F05, F07, F08, F09, F10 (`summary.json` key `fixture_changes_base_to_49cc` lists
only F06; the per-fixture diff was computed from the two receipts, not by eye).

## Cause isolation (why F06 and nothing else)

The whole census delta between the two revisions is one commit, `49cc53c7` "round-39: C1 storage arm cross-checks
the mount table on an absent or empty sysfs root; IN-109 repinned": `git diff 0eff65b2 49cc53c7 --
tools/tsukuroi-census.sh` is +45/−1, and the functional hunk is the `fsn == 0 && blocked == 0` mount-table branch at
`tools/tsukuroi-census.sh` (at `49cc53c7`) lines 1903–1914: `cat -- "$PROC_MOUNTS"`; any field-3 `btrfs` gives
`BLOCKED detail=mounts:btrfs-without-sysfs`, an unreadable table gives `detail=mounts:unreadable`. The rest is the
header comment, `PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}` (`:460`), the selftest fixture env wiring
(`:2161`) and three new selftest cases (`:2969`+).

Run in isolation against an absent root with four different mount tables (`isolate-mount-table.txt`):

```
census49cc mounts=nobtrfs  -> HEALTHY filesystems=0 devices=0 nonzero=0
census49cc mounts=btrfs    -> BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
census49cc mounts=absent   -> BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:unreadable
census49cc mounts=real     -> BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
censusbase mounts=nobtrfs  -> HEALTHY 0/0/0
censusbase mounts=btrfs    -> HEALTHY 0/0/0        # base ignores the table
```

So F06's flip is caused solely by the new mount-table branch reacting to the **real** `/proc/self/mounts`, which on
this host lists four btrfs rows (`summary.json` → `host.btrfs_mount_rows = 4`, e.g.
`/dev/mapper/root / btrfs rw,noatime,...`). F01–F05, F07–F10 all pass a root that holds an fsid entry, so the new
branch is not entered for them — consistent with the code (`fsn == 0`) and with the observed identical outputs.

## Harm judgment

**No harm to the round-38 coverage claim.** The claim is pinned at `b0005ae9`
(`SCORECARD.md:2232-2234`: "at post-C1 revisions it reads BLOCKED and `score-storage-arm-r38.py` FAILs 9/10 by
construction; the round-38 claim stays measured at `b0005ae9`"), and its after receipt
`.ufo/waves/round-38/after/c1-final-b0005ae.json` reads `PASS 10 10 1 1 b0005ae9f56fd5a006fc5ec026578c88e2b64b26`.
Re-measured here, the base-equivalent revision `0eff65b2` (a descendant of `b0005ae9`) still PASSes 10/10, live 1,
six 1, so the pinned claim's surface is intact at the round-39 base.

**The only changed coverage is the superseded F06 rule.** F06 encodes "an absent root means no btrfs filesystem is
mounted: HEALTHY 0/0/0" (`score-storage-arm-r38.py:82`; the old rule is quoted in the census comment that `49cc53c7`
rewrites). The day that premise is false — btrfs is mounted and only the sysfs view is absent — the new arm correctly
says BLOCKED. The old rule still holds when nothing is btrfs-mounted (isolation row `mounts=nobtrfs`), so the change
is not a blanket "empty root is blocked": it is exactly the superseded rule.

**The QUALITY 82 conjunct is not harmed.** Q82 (production-path views, no `TSUKUROI_*` override) stays green 3/3 at
`49cc53c7` and at the tip, including the all-zero and forced-nonzero views; random trees this run had 2–3
filesystems / 4–6 devices, and every view's `got` equalled the frozen v1 model's expectation.

## Risks / caveats (reported, not resolved)

1. **The 9/10 is host-conditional.** On a host whose mount table lists no btrfs, a post-C1 census still prints
   `HEALTHY 0/0/0` for an absent root (isolation row `mounts=nobtrfs`), so F06 would match and the frozen v1 counter
   would read 10/10. "FAILs 9/10 by construction" is exact only where the default table lists btrfs (this host: 4
   rows). Any later gate that re-runs the frozen v1 counter at post-C1 revisions should pin `TSUKUROI_PROC_MOUNTS`
   or expect host variance; the counter itself must not be edited (frozen).
2. **One transient external kill, not reproducible.** Of three v1 runs at `49cc53c7`, two read 9/10 (F06 only,
   `v1-49cc.json`, `v1-49cc-repeat2.json`); one read **8/10** (`v1-49cc-repeat.json`) because F03's census child
   ended `rc = -15` (SIGTERM) with no output (`got null`, `six_planes false`), which the counter counts as a
   mismatch. The live leg matched in that run. Host load was `14.14` with sibling wave harnesses on the box, and
   the journal shows concurrent harnesses ptraching `tsukuroi-census.sh` processes (`journal-excerpt.txt`,
   `2026-10-26 03:06:02`); no earlyoom/OOM-kill line appears in the window despite earlyoom being active. This is
   an environment artifact of the multi-seat wave, not a property of the census bytes or the counter's fixtures —
   F06 behaved identically in all three runs. Related counter weakness worth recording: the v1 counter discards the
   census child's stderr, so an externally killed child is indistinguishable from a rule mismatch in the receipt.
3. **F06 reads the real mount table by design** (the v1 counter sets only `TSUKUROI_BTRFS_SYSFS`; it deliberately
   leaves `TSUKUROI_PROC_MOUNTS` unset), so the frozen receipt is bound to this host's mount table. That is the
   trigger the round-39 declaration names, but it means the receipt is not portable evidence of the census rule.

## What I did not do

- Did not run the round-39 `score-storage-hidden-r39.py` (other seat) or `tsukuroi-census.sh --selftest` (parent
  gate); did not judge the new census selftest cases.
- Did not edit, stage, or commit anything in the lane; wrote only this report and receipts under
  `.ufo/waves/round-39/w1/C1ExecR38Counters/`. Scratch lived under
  `/fast/scratch/hyaku/tsukuroi-r39/C1ExecR38Counters/` and was removed after the receipts were copied.
- No tools installed or upgraded; no host mutation; no sudo.
