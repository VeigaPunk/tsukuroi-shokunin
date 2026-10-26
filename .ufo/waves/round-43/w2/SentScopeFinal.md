VERDICT: defect-found

# SentScopeFinal — N-13 misroot / scope sweep, tsukuroi lane round 43, wave w2

Read-only sweep. Nothing was deleted, moved, committed or signalled; no lane file, no
fleet file and no host surface was modified by this seat (one self-inflicted scratch-root
file was moved into my own seat dir, disclosed as F5). No tool was installed or upgraded.

Sweep window 2026-10-26 19:55:40–20:12:22 -0300. Baseline for "new" is
`.ufo/waves/round-43/make-w2-spec.py` (mtime 2026-10-26 19:50:34.128, 26,112 B).

Scope-only findings. I found **no defect in the frozen C1/C2 claims** (frozen digests all
reproduce, see "Clean" §D); everything below is a host-guard/scope event.

## Findings (path | size | owner seat)

| # | path | size | mtime | owner | status |
|---|---|---|---|---|---|
| F1 | `tsukuroi-shokunin/.git/{index,objects/…,objects/pack/pack-81458e…pack}` | index 2,048,776 B; 1,733 loose objects; pack 38,587,659 B | 19:53:21 / 19:56–19:58, 20:01:26 | **unattributed** (see §A) | lane git state written during w2; no ref/jj/tracked-content change |
| F2 | `shokunin/p.out`, `shokunin/p.err` (fleet root) | 62 B, 0 B | 20:10:49.589 / .656 | **chousa-shokunin round 52** seat (exact seat unknown) | fleet-root misroot, still present at 20:12 |
| F3 | `tsukuroi-shokunin/.ufo/waves/round-43/w1/CritSeparability/tree-at-impl.txt` | 1,057,348 B | 19:22:33.582 | wave-1 seat `CritSeparability` (not a w2 seat) | untracked, outside `w2/`, pre-dates w2 dispatch (19:50:34) |
| F4 | `/fast/scratch/hyaku/tsukuroi-r43/skillpins.txt` | 152,914 B | seen 19:55, gone 19:57 | unknown w2 seat | transient scratch-root file, owner removed it; **no residue** |
| F5 | `/fast/scratch/hyaku/tsukuroi-r43/SentScopeFinal.ids` | 71,108 B | 20:00:5x | **this seat** (self-disclosure) | created at the scratch root by my own first receipt dump; moved to `…/SentScopeFinal/objects-touched-1957.ids` at 20:01 and deleted with my scratch at the end |
| F6 | `.ufo/waves/round-43/w2.ready` (160 B), `w2.ready.dispatched` (1,219 B), `w2-dispatch.json` (59,030 B), `w2-spec.json` (44,810 B), `w2-dispatch.err` (0 B) | — | 19:50:41–19:55:09 | L1 / orchestrator dispatch plumbing | outside `w2/` by design; not a violation |

Nothing else in the lane was written after the spec: the complete list of lane files newer
than `make-w2-spec.py` and outside `w2/` is exactly the five F6 dispatch files
(`find . -path ./.git -prune -o -path ./.jj -prune -o -path ./.ufo/waves/round-43/w2 -prune -o
-type f -newer .ufo/waves/round-43/make-w2-spec.py -print` → 5 lines; receipt
`SentScopeFinal/sweep.txt`).

## A. Lane `.git` written during w2 (F1) — detail and attribution attempt

Measured state (receipts `SentScopeFinal/lane-git-state.txt`, `objects-touched-1957.ids`,
`objects-types.txt`):

- `HEAD` = `64646d6e5749e0b5b6e458aa0753d39c47404e6b`, `refs/heads/master` mtime
  19:50:46.879, `refs/remotes/origin/master` mtime 19:50:48.471 — **no ref moved**.
  jj newest op `24efde84…` and `op_heads/heads/24efde84…` both 19:50:48.500 — **no jj op
  after dispatch**.
- `.git/index` 2,048,776 B, mtime 19:53:21.734836501. Content is identical to `HEAD`:
  `git diff-index --cached --name-status HEAD` printed nothing, rc=0. So the index write was
  a stat-cache refresh, not staging. It pre-dates this seat's first `git` call (~19:55:40)
  and my `git status` did not rewrite it (mtime still 19:53:21 at 20:12:04).
- 1,733 **loose objects** (1,524 blobs + 209 trees, **0 commits**) carry ctime/mtime in the
  bursts 19:56:13–19:58:19 and again 20:01:26 (`find .git/objects -newerct 19:55:00
  -printf '%TH:%TM\n' | sort | uniq -c` → `12 19:56`, `1734 20:01`; the 1,734th file is the
  pack, below). Four sampled ids are reachable from refs (`rev-list --objects --all`), none
  is in either pack (`verify-pack` hits=0), `git count-objects -v` → `count: 2607,
  in-pack: 18650, prune-packable: 0`.
- `pack-81458e32…pack` 38,587,659 B rewritten in place (mtime 20:01:26.375502078) while its
  `.idx` stayed 14:08:48; `git verify-pack` reports both packs `ok`; the other pack
  (`pack-546089e9…`) is untouched (14:08:48).
- No further object/index/pack write after 20:01:26 through 20:12:04.

Attribution — what I could and could not establish:

- The only `git` process observed at the 19:58:17 burst was
  `git -C /fast/scratch/hyaku/tsukuroi-r43/SimplifierCounters/fx.KyOdHC -c user.name=fixture
  -c user.email=fixture@invalid commit -q -m ctl` (seat `SimplifierCounters`; its fixture is
  already removed). **This is not sufficient to explain the lane writes**: a controlled run of
  the mandated recipe — `git clone -q --shared`, then a fixture commit, then `git gc` in the
  clone — leaves the source object store byte- and mtime-identical (0 source files newer;
  loose-only source and `git gc`-packed source both; `SentScopeFinal/writer-elimination.txt`).
- My own read-only git invocations against the lane (`count-objects`, `rev-parse`,
  `ls-files`) changed nothing: touched-object count `before=1734 after=1734`, pack mtime
  unchanged.
- A 175 s watch of `/proc/*/fd` for any descriptor on a path under
  `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/` (20:04:56–20:07:50) recorded **0 hits** —
  but that window was after the last burst, so it is a negative result only.
- Consequence: the writer is **unattributed**. Two seat reports document git use that is
  read-only (`C1FinalKillRule.md:9,11` `rev-parse --verify`; `C1FinalRerun.md:22` `rev-parse`
  + `hash-object` without `-w`; `C1MutFinal.md:10-12`, `SourcesCensusFinal.md:16-18` fixture
  `clone --shared`), and the lane tools' write-capable paths (`tools/_revision.py:393-422`,
  `tools/check-registry-coverage.py:482-489`) are fixture-only and would move refs, which did
  not happen.

Impact: no tracked lane file, no ref, no jj operation and no staged content changed; the
frozen counters and the record are untouched, so the kill-rule inputs are unaffected. The
residual is metadata churn in the object DB plus one index stat-cache write — low severity,
but it is lane git state written by an unidentified process during w2, which the seat guard
forbids. **Smallest remediation:** the L1 should record the writer's identity before the next
wave (run the sweep with an `inotify`/`/proc/*/fd` watch armed *while* seats are still
executing) and state the allowed git surface explicitly for fixture-driving seats.

## B. Fleet-root misroot (F2)

`git -C /home/vgpnk/Projects/shokunin status --porcelain` was **empty** at 19:55:40 and at
20:11:45 printed `?? p.err` / `?? p.out`. `p.out` (62 B) contains exactly
`QUOTE S115 char 13246 spans/S115-1.txt` + `SPANS_ROWS=1 WRITTEN=1`, which is the print
format of `chousa-shokunin/corpus/evidence/round52/build-spans.py:261-262`; S115 is a
kotoba/chousa source id, not one of this wave's S237/S240/S241. The chousa r52 lane is live
(fleet reflog 19:51:21 `chousa-shokunin <chousa@shokunin.local>`). So a **chousa round-52
seat ran its spans builder with cwd = the fleet root and relative redirection**. Not
tsukuroi content, not mine to delete (read-only sweep); reported for the orchestrator.

The fleet repo's own object churn during w2 (objects at 19:51–20:06, commits `e8c221f2`
"round-43: kengaku report", `155e33bd`, `f542d31d`) is other lanes' jj exports, not
tsukuroi w2 seats; the fleet pack is untouched since 02:13:52.

## C. Clean surfaces

- Lane tracked content: `git status --porcelain` shows only the four expected untracked
  paths (`w1/CritSeparability/tree-at-impl.txt`, `w2.ready`, `w2.ready.dispatched`, `w2/`);
  no ` M `/`A `/`D ` line. `w2/` = 204 files, 2.4 MB, no symlinks.
- `tools/__pycache__` does **not** exist (no lane tool was imported from the lane dir).
- Ignored entries are all pre-w2: `.jj/` (20:29 Oct 20), `.ruff_cache/` (15:08:28),
  `round-37/…/__pycache__` (Oct 25 16:07), `round-41/controls/__pycache__` (15:11:59),
  `round-42/controls/__pycache__` (16:42:37), `round-35/…/pacman-54d9411/build-aux`
  (2026-01-07). None is a w2 write.
- `/tmp`, `/var/tmp`: no file or dir named `*tsukuroi-r43*`, `*bootinputs*`, `r43lib`,
  `r43view` (full-name search, no depth limit). Entries newer than the spec belong to other
  lanes (`/tmp/kaidoku-r42/…` 20:06–20:07, `/tmp/mori-r38-scratch`, `/tmp/mado-term-*`,
  `/tmp/tameshi-r14-*`, `/tmp/ecc-metrics-*`). **No /tmp path is used as evidence here.**
- tmpfs: `findmnt -t tmpfs` → `/dev/shm`, `/run`, `/run/credentials/*`, `/run/user/1000`.
  No mount named `r43lib` or `r43view`. `/dev/shm` holds only `tmp7qyqokw0/` (four empty
  `*.desktop` probes, 19:50, unrelated to tsukuroi); a `c1w47/` dir seen at 19:55 was gone by
  20:08.
- `/fast/scratch/hyaku/tsukuroi-r43`: 329 MB at 20:11:59, three dirs — `L1` (own receipts,
  12 KB), `SentScopeFinal` (mine, removed at the end), `SkillReview` (live seat's clone).
  No top-level files. Earlier (19:55) there were 19 seat dirs plus the F4 file; seats are
  cleaning up as they finish.
- `~/.local/bin`: no file newer than the spec (no shim planted).
- Host: `/etc`, `/boot`, `/usr/local` have **0** entries newer than the spec; `/var/lib` has
  exactly one, `/var/lib/systemd/timesync/clock` (systemd-timesyncd's own periodic write,
  not a seat). No reboot (`uptime -s` = 2026-10-26 12:08:37; up 8 h at sweep time).

## D. Frozen evidence re-verified (read-only)

```
48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801  .ufo/waves/round-42/frozen/src/scrub.c
7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01  .ufo/waves/round-43/frozen/src/ioctl.c
f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556  .ufo/waves/round-43/frozen/hostcap/capture.txt
886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f  tools/score-bootinputs-r43.py
b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854  tools/check-scrub-record-r43.py
```

All five match the frozen claim prefixes (48df2e2f…0801, 7b3488f2…ba01, f7ecbe7c…c556,
886f92c8…e10f, b4602c56…9854).

## What I did not do

No counter, selftest or heavy run was executed (no C1/C2 counter, no census selftest); no
seat was spawned; no peer was messaged; no lane/fleet/jj/git mutation; nothing deleted; no
sudo, no package manager, no service restart, no btrfs ioctl; no fixture was created from the
lane (the only fixtures were two synthetic repos in my own scratch, removed). Scratch
`/fast/scratch/hyaku/tsukuroi-r43/SentScopeFinal` (incl. `src`, `dst`, `src2`, `dst2`) was
removed after the receipts above were copied to
`.ufo/waves/round-43/w2/SentScopeFinal/`.

Receipts: `.ufo/waves/round-43/w2/SentScopeFinal/lane-git-state.txt`,
`objects-touched-1957.ids`, `objects-types.txt`, `sweep.txt`, `writer-elimination.txt`.
