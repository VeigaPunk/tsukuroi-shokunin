VERDICT: defect-found

# SentMisroot — X-5 scope / misroot sweep, tsukuroi r44 w1

Sweep snapshot: 2026-10-26 21:41:43 -03; observations also taken 21:22–21:43. Wave window: spec 21:04:47, `w1.ready` 21:05:00, dispatch 21:21:33. Read-only throughout: nothing deleted or signalled, no lane/fleet/PATH write except this report and `w1/SentMisroot/`.

## Findings

### F1 HIGH — the frozen C1 counter's 1200 s timeout leaves a private mount namespace holding tmpfs `r44lib`/`r44view`, plus 8 hung processes

Exploit/failure path (all observed):
- Run: `python3 .../tools/score-scrub-arm-r44.py --revision c8850f014cd3861059853755747bfc25f717dd63 --scratch .../C1CritEvasion/s --lane .../C1CritEvasion/fx.V6-gate-fixture-literal.n8tb6beq` (pid 2366199, lstart 21:13:55; gone by 21:34:17 — the `timeout=1200` at `tools/score-scrub-arm-r44.py:569` and `die('namespace leg timed out')` at `:570-571`).
- Trigger: the seat's V6 gate variant (`.../C1CritEvasion/driver/run_battery.py:57`) makes `probe_scrub_record` run `grep -ls '^scrub status:1$' "$SCRUB_DIR"/scrub.* | head -1`; the fixture has a FIFO matching `scrub.*` (`tools/tsukuroi-census.sh:3276`, fixture census `:2043`). `grep` blocks opening the FIFO (`wchan=wait_for_partner`, pid 2369037) and `head` blocks on the pipe (`wchan=anon_pipe_read`, pid 2369038); the timeout path (`run(..., 60)` at INNER `:149`, `timeout=1200` at `:569`) kills at most the direct child, and the surviving grandchildren keep the capture pipes open, so the leg never reaches EOF. The seat itself saw the per-case edge: `w1/C1CritEvasion.md:29` "note `wrong-types` also timed out".
- Survivors at 21:41:43: `2369032 bash -c . /mnt/census-lib.sh; …` (PPid **1494** = `systemd --user`, orphaned; elapsed 27:59), `2369037 grep`, `2369038 head`; and the leaked selftest chain `3823343 → 3823351 → 3827198 → 3827202 grep / 3827206 head` (all cwd in the now-deleted `C1CritEvasion/s/scrub-arm-r44.nhb477pq`, PPid 3823343 = 1494).
- Mounts: `/proc/2369032/mountinfo:548,550,551,552` — `tmpfs r44lib` on `/mnt`, `tmpfs r44view` on `/sys/fs/btrfs`, `/var/lib`, `/etc/systemd/system`; namespace `mnt:[4026533757]`, `user:[4026533746]`. Host `/proc/self/mountinfo` contains **0** r44 mounts, and `/var/lib/btrfs` does not exist on the host: no host harm, but the namespace is leaked and unreaped.
- Peer corroboration of the mechanism: `w1/C1SentScope.md:64-80` (grandchild survives parent; timeout shape).
- The seat's residue check is namespace-blind: `w1/C1CritEvasion.md:5` states "no mounts left behind (`findmnt -t tmpfs` clean)" — false at the namespace level while `/proc/2369032/mountinfo` still held the four `r44lib`/`r44view` mounts. Its V6 score was written at 21:29:59 (another attempt, `w1/C1CritEvasion/score-V6-gate-fixture-literal.json`), while the 21:13:55 run was still hung; the 1200 s stall and the eight survivors are not disclosed.

Impact: (a) `findmnt -t tmpfs` shows nothing, because the mounts are namespace-private — the sweep item's own command false-negatives (and the seat’s own no-residue claim rests on it); (b) each occurrence burns 20 min and returns an ERROR instead of a measurement; (c) 8 processes + a mount namespace leak per hang with no reaper (`sys.exit` path), and the seat deleted its scratch while its processes still run (deleted cwd). Any residue check must scan `/proc/*/mountinfo`, not only the host mount table.
Smallest remediation (not applied): in `INNER`, spawn with `stdin=subprocess.DEVNULL` and `start_new_session=True`; on `TimeoutExpired` (outer) `os.killpg(p.pid, SIGKILL)` and reap; add the same kill in a `finally`. The current 8 survivors are the owner's/L1's to kill — I did not signal them.

### F2 MEDIUM — `tools/__pycache__/` created inside the lane tree during w1

- Births (`stat %w`): `score-pacnew-arm-r35b.cpython-314.pyc` 21:11:05 (47 479 B), `score-scrub-arm-r44.cpython-314.pyc` 21:11:09 (45 409 B), `check-scrub-record-r44.cpython-314.pyc` 21:22:33 (28 184 B). Headers match the lane sources' mtime+size, so the modules were imported **from the lane `tools/` tree**, not from a copy.
- Hidden from `git status` by `.gitignore:2 __pycache__/` (`git check-ignore -v` confirms), so only a path check finds it.
- Owner not attested: 21:11:05/09 is the `C1ExecOtherCounters` counter-run window (r35b and r44 counters); 21:22:33 is 9 s after `C2DraftCritSR8`'s receipt (21:22:24). Reads as module imports / `py_compile`, not seat claims.
- Remediation: importers use `python3 -B`/`PYTHONDONTWRITEBYTECODE=1` or import a copy; remove `tools/__pycache__` at integration (L1's call).

### F3 MEDIUM — fleet-root misroot by this wave at 21:08:59 (already quarantined; no recurrence)

`fx/A2-uppercase-fsid-sysfs/sysfs/<fsid>/devinfo/1/scrub_speed_max` (4 B `0\n`, sha256 `9a271f2a…`) appeared at the fleet root: `w1/C1ExecEdgeNames.md:246-249` (`dev0 "$PWD/fx/…"` with cwd = fleet root), recorded in fleet commit `685f7b36` and moved by the orchestrator into `.tower/quarantine/fleet-root-strays-20261026T2114/` (`TREE.txt`, `SHA256SUMS`, `git -C fleet status` clean at 21:41:43 except `?? .ufo/reports/round-52/mori.md`, another lane's in-flight report). No second occurrence.

### F4 LOW — `/tmp` files carrying lane content (owners removed them)

- `/tmp/_chk.sh` 3 778 B, 21:10:50, sha256 `f6775b45…`: `_scrub_real()` plus a gated `probe_scrub_record` with the `TSUKUROI_SCRUB_DIR` test duplicated — the same gated-probe shape `C1CritEvasion/driver/run_battery.py:37-57` emits, saved the same second as that driver (attribution circumstantial).
- `/tmp/cand.sha` 956 B, 21:20:22, sha256 `6224af3a…`: sha256 list of the C2 source set (`corpus/knowledge/btrfs-scrub-record-r43/r44.md`, `corpus/SOURCES.md`, `frozen/hostcap/capture.txt`, frozen `btrfs-scrub@.*`/`PKGBUILD`/`scrub.c`/`sysfs.c`). C2 owner not attested.
- `/tmp/pinerr` 0 B, 21:13:18 (`e3b0c442…`), unattributed; `/tmp/r39w.sh` 1 318 B, 21:21:39, gone by 21:23 (owner cleaned up). Both content-bearing files were gone by 21:41:43; bytes are preserved under `w1/SentMisroot/`.
- Note: `/tmp` is not evidence and not scratch under the seat rules.

### F5 NOTE — L1 integration moved HEAD and the worktree during the sweep (authorized role, w2 pinning consequence)

At 21:41:43 the lane showed ` M corpus/knowledge/btrfs-scrub-record-r44.md` and ` M tools/tsukuroi-census.sh` (index column) with `HEAD=ff2c264a`; at 21:41:54 a commit landed: `071ab0d1` author/committer `tsukuroi-shokunin <tsukuroi@shokunin.local>`, “round-44: wave-1 integration — … selftest cases; 141 -> 148 …; w1 seat reports” (`.git/HEAD` mtime 21:41:54, `.git/index` 21:42:18), with untracked `after/c1-after-071ab0d1.jsonl`; at 21:42:36 the worktree census (198 862 B) again differed from HEAD by a 3-line hunk (198 809 B) — L1 is still editing. This is L1's integrator write, not a seat breach, but the tree is no longer at the declared implementation `7e08169…` (census blob `f45d0051` vs committed `9b209ba1`, cases 141→148): w2 seats and both counters must pin the new revision.

## Sweep table (item → command → result)

| # | Item | Command (abridged) | Result at 21:41:43 |
|---|---|---|---|
| 1 | Fleet-root untracked naming tsukuroi r44/scrub | `git -C /home/vgpnk/Projects/shokunin status --porcelain`, root `find -maxdepth 1` | 0 tsukuroi/scrub entries; only `?? .ufo/reports/round-52/mori.md` (mori r52, in-flight); no `=`/`T` strays; `MANIFEST.json` 21:24 + fleet commits are protocol-shokunin kengaku r44 closure |
| 2 | Lane anything outside `w1/` | `git -C lane status --porcelain`; `find lane -newer spec -not -path '*/w1*'` | 3 entries: `w1.ready` (160 B, 21:05:00), `w1.ready.dispatched` (1 634 B, 21:21:33) — L1 dispatch markers; `w1/` expected. Two ` M` tracked files = L1 integration (F5); L1's `after/c1-after-071ab0d1.jsonl` (F5) |
| 3 | `/tmp`,`/var/tmp` newer than spec naming tsukuroi-r44/scrub | `find … \( -iname '*tsukuroi-r44*' -o -iname '*scrub*' \)`; content `grep` | 0 by name; 0 by content at 21:41 (earlier: `_chk.sh`, `cand.sha`, both removed by owners — F4) |
| 4 | New entries in `~/.local/bin` | `find ~/.local/bin /usr/local/bin -newermt spec`; count | 102 entries, newest file 18:10:45 (before wave); 0 new; no symlinks into scratch/PATH shims |
| 5 | tmpfs mounts named r44lib/r44view | `findmnt -t tmpfs`; full `/proc/*/mountinfo` scan | Host: none. Namespaces: 3 pids in `mnt:[4026533757]` with 4 such mounts (F1) |
| 6 | `tools/__pycache__` | `stat -c '%w %s'`; header check | 3 `.pyc`, born 21:11:05/21:11:09/21:22:33 (F2) |
| 7 | Leftover dirs under `/fast/scratch/hyaku/tsukuroi-r44` | `ls`; `/proc/*/cwd` map | 3 dirs: `C1MutArm` (live), `L1` (live), `SentMisroot` (mine, removed on exit). `C1CritEvasion` removed but 5 live cwds inside the deleted dir → F1 survivors. No scratch outside the seat convention |
| — | Host/mutation surfaces | mtimes of `/var/lib/pacman/local` (10-25), `/etc/systemd/system` (10-20), `timers.target.wants` (10-20), `scrub_speed_max` (16:41); lane `.jj` no op after 21:05, `.git/index` 21:42:18 (L1) | No package/service/unit/sysfs/mount mutation by the wave |

## Limits

- `/proc/2369032/fd` is unreadable (process uid 100999 in the user namespace); the mount evidence is from `mountinfo`.
- F2/F4 owner attribution is circumstantial (timing + content shape), not self-disclosed.
- No counter, census or selftest was run; nothing was signalled or deleted.
- One snapshot at 21:41:43 with L1 integrating concurrently; the lane state changed at 21:41:54 (F5).

## Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w1/SentMisroot/`: `_chk.sh` (`f6775b45…`), `cand.sha` (`6224af3a…`), `pinerr` (`e3b0c442…`), `hashes.txt`, `pycache-watch.log`. Scratch `/fast/scratch/hyaku/tsukuroi-r44/SentMisroot/` removed after copying. These five files were created 21:31–21:34 and were then swept into L1's integration commit `071ab0d1` (`git ls-tree -r 071ab0d1 -- .ufo/waves/round-44/w1/SentMisroot/` lists them); I made no git/index changes myself.

## Appendix — name collision at this path (no data lost)

A second X-5 seat under the same report name had already written this path before my run; L1 committed that file at 21:41:54 in `071ab0d1` (5 lines, 5 insertions). My mandated write replaced the working-tree copy; the committed text is preserved here verbatim so nothing is lost, and the collision is flagged for L1. Note its referenced receipt `w1/SentMisroot/sweep-snapshot.txt` does not exist in the commit or the tree — the five files in that directory are mine (above).

> VERDICT: defect-found
>
> Report: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w1/SentMisroot.md` (receipt: `.ufo/waves/round-44/w1/SentMisroot/sweep-snapshot.txt`).
>
> Late addendum (peer claim verified, read-only): ConsiderMine's `find tools -name '*.pyc'` = 3 reproduces — `score-pacnew-arm-r35b` 21:11:05, `score-scrub-arm-r44` 21:11:09, `check-scrub-record-r44` 21:22:33 — with `git status --porcelain` still blind to them (`.gitignore:2 __pycache__/`). It is a recurrence, not r43 residue: my two r43 pyc (19:08:50, 19:21:04) and the entire `/fast/scratch/hyaku/tsukuroi-r43` tree are now gone (0 dirs, all ten root strays removed). All three headers match their sources (src_mtime/size), so the loaded code is genuine — the trigger is the loader habit, and `score-pacnew-arm-r35b` stamps a pre-r44 source, widening it beyond this round's counters. Fix unchanged: `PYTHONDONTWRITEBYTECODE=1` plus a `find`/`--ignored` sweep instead of porcelain alone.

That prior text independently reproduces F2 (same three births, same header check); it does not cover F1's namespace mounts or survivors.
