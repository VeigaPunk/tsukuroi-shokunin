VERDICT: defect-found

# R-10 final sweep — tsukuroi lane round 44 (hyaku run 9), w2

Seat: `SentFinalScope` (leaf; no subagents; no dispatch).
Mode: **read-only**. Nothing deleted, nothing created outside this file. All sampling done from
`/fast/scratch/hyaku/tsukuroi-r44/SentFinalScope/` (cwd for every command) with absolute paths.
Lane HEAD at sweep: `3a1c6b5c958c4f289a8b12551f96d843877b700e` (descendant of freeze
`1d2afffe…` and of declared integrated tip `8eee79db…`; `git merge-base --is-ancestor` rc=0 for
both, 22:04:47).

Claim impact: **none**. Nothing below touches the C1 census/arm bytes, the frozen counter hashes,
the SR7/SR8/SR9 corpus rows, or any seat's `ROW SR<n> VERDICT:` line. The one defect is host/wave
*process hygiene*, not evidence integrity.

## 1. Item-by-item result (the seven R-10 items)

| # | Item | State | Evidence (sampled 2026-10-26 22:02–22:07 -03) |
|---|---|---|---|
| 1 | fleet-root `git status --porcelain` strays | **clean, with one transient** | 22:02:5x: 0 lines. 22:04:2x: ` M .scratch/goal-20261026-hyaku-run9.md`, `git diff --numstat` = `1 1`. 22:05:01 and 22:06:50 (`-uall`): 0 lines, `worktree blob = index blob = HEAD blob = 3c96057ceceb8c0c7d9a0e4b7912d7ec372fbd2b`. See F-3. |
| 2 | lane `git status` | **no tracked change; untracked growth only under `.ufo/waves/round-44/`** | 22:06:50: `-uall` 172 lines (135 at 22:05:26 — live seats writing). `grep -v round-44` → rc=1: **zero** untracked paths outside the wave dir. `grep -v '^??'` → rc=1: **zero** staged/modified/deleted tracked files. |
| 3 | `/tmp` & `/var/tmp` remnants naming `tsukuroi-r44` | **none** | `find /tmp /var/tmp -maxdepth 4 -name '*tsukuroi-r44*'` → 0 (22:07:28). Broader `*r44*` scan → exactly one hit, **not ours**: `/tmp/kengaku-r44-closure-entry.json` (2403 B, mtime 21:24:31, `"lane": "kengaku"`, `"round": 44`). |
| 4 | `~/.local/bin` entries | **no lane-named entry** | 102 entries. `ls ~/.local/bin \| grep -iE 'r44\|scrub\|tsukuroi\|hyaku'` → rc=1 (no match). Newest entries are host-level (`omp` 18:10:45, `firefox` 17:48:46, `ruff` 09:46, `OpenBot…AppImage` 10:49, `sasquatch` 01:22) and none is r44-derived; no trace of a seat PATH write. |
| 5 | `findmnt -t tmpfs` for `r44lib`/`r44view` | **none** | Full `findmnt -t tmpfs`: `/dev/shm`, `/run` (+ 3 `/run/credentials/*` submounts), `/run/user/1000` only. `grep -E 'r44lib\|r44view'` → rc=1. Independent `/proc/self/mountinfo \| grep r44` → rc=1. No leaked mount namespace surface. |
| 6 | `__pycache__` under lane `tools/` | **present: 3 `.pyc`, gitignored** | `tools/__pycache__/{check-scrub-record-r44 28184 B @21:22:33, score-pacnew-arm-r35b 47479 B @21:11:05, score-scrub-arm-r44 45409 B @21:11:09}`. `git check-ignore -v` → `.gitignore:2:__pycache__/`. `git ls-files tools/__pycache__` → empty. `PYTHONDONTWRITEBYTECODE` → unset in my env. See F-2. |
| 7 | leftover scratch under `/fast/scratch/hyaku/tsukuroi-r44` | **21 dirs, 1.4 G, all in-flight seats** | 22:06:36 snapshot: `SelfAssess 680M/40969`, `C1MutFinal 346M/22097`, `RegistryFinal-2 338M/18895`, `C1ExecHandReproFinal 332K`, `SrcGateFinal 2.2M`, `SkillReview 1.1M`, `C2CritSR8 248K`, `L1 200K`, `C2CritSR7 48K`, `C2CritSR7/8/9` etc.; empty-but-present: `C1CritFinalEvasion, C2RevSR8, ConnFinalQuality, ConnFrontierFinal, CritSeparabilityFinal, RegistryFinal` (0 entries); `LessonCrit` 1, `ReadmeReview` 2, `SentFinalScope` 1. Every name ∈ w2 32-seat roster ∪ {`L1`} (`jq '.items[].name' w2-spec.json`, 32 names, `maxLanes 32`, `reportDir .ufo/waves/round-44/w2`). Host `/fast` 25 % used. |

Supplementary lane facts (for the sweep line, not defects): w2 output dir held 125 files at 22:05,
all under the declared `reportDir`; every directory/report name is in-roster; the only non-seat
file is `w2/swarm-registry.json` (swarm bookkeeping, not a seat write — I did not touch it).
`/dev/shm/tmp7qyqokw0` (700, vgpnk) holds four 0-byte `.desktop` stubs (`alacritty/foot/kitty/xterm`, 19:50)
— host xdg-helper temp, not lane. `/var/tmp` non-systemd entries (`r15/r17/r18/r21/r29-*`,
`souji-*`) and `/tmp/w5-mado-*`, `/tmp/tameshi-r14-*` belong to other lanes.

## 2. F-1 (the defect): orphaned w1 pipeline, still blocked, cwd deleted

Severity: **low** (no writes, no mounts, no evidence path). Class: process cleanup / no-harm.

Evidence, 22:07:28 -03:

```
pid      ppid  pgid     sid      etimes stat wchan             cmd
3827202  1494  3644205  3644205  3102   S    wait_for_partner  grep -ls ^scrub status:1$ …
3827206  1494  3644205  3644205  3103   S    anon_pipe_read    head -1
```

- Both started `Mon Oct 26 21:15:45 2026`; still alive at 22:07:28.
- `readlink /proc/3827202/cwd` and `/proc/3827206/cwd` →
  `/fast/scratch/hyaku/tsukuroi-r44/C1CritEvasion/s/scrub-arm-r44.nhb477pq (deleted)`;
  that directory no longer exists (`ls -ld` → ENOENT).
- `ppid 1494` = `/usr/lib/systemd/systemd --user`: the seat's parent died and both were
  reparented (orphan by definition). `pgid == sid == 3644205`; `ps -eo pid,pgid | awk '$2==3644205'`
  returns exactly these two — the session leader is gone, so **process group 3644205 is a
  two-member orphan group**.
- `grep` argv: `grep -ls '^scrub status:1$' <4 fixture paths under …/fx/scrub-wrong-types/scrub/> "TSUKUROI_CENSUS: HEALTHY (forged)"`;
  its fds are `0 -> /dev/null`, `1 -> pipe:[656635014]`, `2 -> /dev/null` — **no file descriptor
  open for write, no deleted regular file pinned**, only the deleted cwd inode. `head -1` reads
  that pipe (`0 -> pipe:[656635014]`) and writes to `pipe:[656622384]` whose reader is gone.
- `WCHAN wait_for_partner` = blocked inside `fifo_open()`: one argv path was a **fixture FIFO with
  no writer**, so `grep` blocks in `open()` forever; `head` blocks on the never-written pipe. No
  syscall file available for the pid (`/proc/3827202/syscall` → EPERM), so the FIFO diagnosis is
  from wchan + argv shape + the `scrub-wrong-types` fixture names [INFERENCE, high confidence].

Attribution: `C1CritEvasion` is a **w1** seat (`w1-spec.json` contains it; its report
`.ufo/waves/round-44/w1/C1CritEvasion.md` is 8520 B @21:32:48, `w1-results.json` @21:54:20). Its
lane scratch dir is already removed; only its orphaned children survived it. Two other lanes'
orphans of the same shape exist on the host (`/var/tmp/souji-r18-…` python, 14:06) — so this is a
*driver-habit* class, not a one-off.

Impact: two sleeping processes + 3 fds each, one pinned deleted-cwd inode (directory only —
`grep` holds no deleted data file, so this is **not** a disk leak; the 1.4 G `du` under scratch is
unaffected). No write capability, no mount, no lane/PATH/fleet-root mutation, no claim evidence
touched. Residual risk it creates: an un-reaped process group keeps a seat slot invisible and, if
the same hang hit a *measuring* pipeline, the seat would silently score an empty stream instead of
red — the r44 guard's "kill only your own processes" rule does not cover a group whose leader
already exited.

Smallest remediation (for the L1 / host, **not** this seat — I signalled nothing):
1. Reap: `kill -TERM -3644205` (group kill; verified two members, pgid==sid) → both exit; do not
   `kill -9` first. Verify `ps -o pid= -g 3644205` empty.
2. One-line habit fix for future waves' fixture drivers: run each fixture pipeline under
   `timeout -k1 60 setsid …` **or** wrap in `setsid … &` + `kill -TERM -$pgid` in a `trap EXIT`;
   a `setsid` group whose leader exits is otherwise immortal. Fixture FIFOs must be created with a
   writer attached (or used with `grep` on a *regular* file copy) so `open()` cannot block.
3. Add to the wave sweep: `pgrep -af 'tsukuroi-r44'` plus `ls -l /proc/*/cwd 2>/dev/null | grep '(deleted)'`.

## 3. F-2 (recurrence confirmed independently, already open): lane bytecode pollution

`tools/__pycache__/` holds three `.pyc` for this round's counters (`score-scrub-arm-r44` @21:11:09,
`check-scrub-record-r44` @21:22:33, plus the older `score-pacnew-arm-r35b` @21:11:05), all covered
by `.gitignore:2 __pycache__/`, none tracked — hence invisible to the `git status` sweep item,
which is exactly the trap w1's `ConsiderMine` recorded as open item `R44-PYCACHE-RECUR`
(`.ufo/waves/round-44/w1/ConsiderMine.md:100,112`, with `lane-pycache-red.txt` and the r43 fix
`PYTHONDONTWRITEBYTECODE=1` written but **not adopted** by the r44 guard). My sweep reproduces it
from the other direction: `find tools -name '*.pyc' | wc -l` = 3 while `git status` shows 0.
No verdict is affected (bytecode mtime/size match their sources; the counters run from source).
W1 also preserved copies in `.ufo/waves/round-44/w1/ConsiderMine/pycache/` (3 files, same sizes);
those are deliberate receipts, not strays.
Remediation (L1): delete `tsukuroi-shokunin/tools/__pycache__/` once the round closes and carry
`export PYTHONDONTWRITEBYTECODE=1` in the seat guard so the next wave cannot re-grow it; widen the
sweep item to `git status --ignored` + `find -name '*.pyc'`.

## 4. F-3 (observation, not a defect): fleet-root transient ` M`

One sample (22:04:2x) showed ` M .scratch/goal-20261026-hyaku-run9.md` with `numstat 1 1`; the
next samples are clean and the worktree blob is byte-identical to HEAD
(`3c96057cec…`, `sha256 e8dccfd14452207cb07e938a3e37035db7e15d7652abc459be88362d2cce14a1`,
25319 B). `stat` ctime == mtime == `22:03:50.339402670` and `git ls-files --debug` records that
same stat with `size 25319`, i.e. the **worktree file has not been written since 22:03:50** — so
the skew was index-side, not content-side. Fleet-root reflog is `export from jj` (HEAD@{0..2}) and
`.git` mtime moved 22:06; the fleet root is a jj-managed repo where exports rewrite the index.
Conclusion: transient index churn from jj export, self-cleared, **no worktree stray and no lane
seat involvement**; final answer for item 1 is "clean". [INFERENCE on cause, from reflog + ctime
invariance; the observable facts are the four samples.]

## 5. Proposed sweep text (for the L1 report / SCORECARD round-44 hygiene line)

> R-10 final sweep (SentFinalScope, 22:02–22:07 -03, read-only, nothing deleted):
> fleet-root worktree clean (0 lines, `-uall`; one transient index skew during a `jj` export,
> self-cleared, worktree ctime-invariant since 22:03:50); lane 0 tracked changes, 172 untracked
> paths all under `.ufo/waves/round-44/`; `/tmp`+`/var/tmp` 0 paths naming `tsukuroi-r44`; `~/.local/bin`
> 0 lane-named entries (102 total, host-level only); `findmnt -t tmpfs` 0 `r44lib`/`r44view`
> mounts and `/proc/self/mountinfo` 0 `r44` lines; `tools/__pycache__` 3 `.pyc` present and
> gitignored (**R44-PYCACHE-RECUR confirmed, open**); scratch 21 dirs / 1.4 G, all in-flight w2
> seats + L1. **One defect:** orphaned blocked pipeline from w1 seat `C1CritEvasion`
> — pids 3827202 (`grep`, wchan `wait_for_partner`) and 3827206 (`head`, `anon_pipe_read`),
> started 21:15:45, ppid 1494 (`systemd --user`), pgid==sid 3644205, cwd a deleted scratch path;
> no writes, no fds to deleted data, disk untouched. Reap with `kill -TERM -3644205`; habit fix:
> fixture pipelines under `timeout`+`setsid` with a group `trap EXIT` kill.

## 6. Bounds observed

No writes outside this file; no git/jj mutation in the lane or fleet root (read-only
`status`/`log`/`diff`/`ls-files`/`check-ignore` only); no signal to any process I do not own; no
pacman/sudo/service/timer/sysfs/mount; no btrfs scrub; `/home/vgpnk/Projects/shokuknow` untouched;
no `~/.local/bin` or PATH write; lane tracked files untouched; scratch removed at exit.
