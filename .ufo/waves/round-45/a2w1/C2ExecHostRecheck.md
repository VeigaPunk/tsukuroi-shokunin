VERDICT: defect-found

# C2-6 — host capture re-run, and the Host reading lines of `btrfs-scrub-grounding-r45.md`

Seat: C2ExecHostRecheck (leaf). Lane: `tsukuroi-shokunin`. Item: re-run the S249 capture read-only and diff it
against the frozen capture; then check each **Host reading** line of
`corpus/knowledge/btrfs-scrub-grounding-r45.md` at `18389f44cf6ce414d7be205998b29c79fb0b490c` against the
`capture.txt` line it cites.

Identity check before anything else: the entry at that revision and in the worktree are the same bytes —
`git show 18389f44…:corpus/knowledge/btrfs-scrub-grounding-r45.md | sha256sum` and
`sha256sum corpus/knowledge/btrfs-scrub-grounding-r45.md` both print
`129b351bdb8c954aa91850b24dbdb0ce184ce00a39997dd81fae962a9b5335f6` (lane HEAD has since moved to `3c42f556`;
no seat output was written to a tracked path — `git status --porcelain` shows only `??` under `.ufo/waves/round-45/a2w1/`).

**Result in one line:** the re-run reproduces the frozen capture byte-for-byte except the timestamp (no host drift),
GR1 and GR3's Host readings check out line-for-line, and **GR2's Host reading is false in its deciding clause**: this
unprivileged caller *can* read btrfs replace state (two world-readable sysfs attributes), which is what the row says
it cannot.

## 1. Re-run of the capture (item, part 1): reproduced, timestamp-only difference

Command (read-only; `capture.sh` writes only `$1`, which was this seat's dir):

```
bash .ufo/waves/round-45/frozen/hostcap/capture.sh \
     .ufo/waves/round-45/a2w1/C2ExecHostRecheck/capture-rerun.txt     # exit 0, 2026-10-27T03:24:32Z
diff  .ufo/waves/round-45/frozen/hostcap/capture.txt \
      .ufo/waves/round-45/a2w1/C2ExecHostRecheck/capture-rerun.txt    # exit 1
1c1
< captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000
---
> captured 2026-10-27T03:24:32Z uid=1000 CapEff=0000000000000000
diff <(grep -v '^captured ' …capture.txt) <(grep -v '^captured ' …capture-rerun.txt)   # exit 0
```

- Only line 1 differs; with the `captured` line removed the two files are identical (9 lines each) — **no live drift**
  in any field the entry reads (`unit_show`, `stop_default`, `dropin_owner`, `unit_dropins`, `scrub_speed_max`,
  `devinfo`), 75 minutes after the frozen run.
- `sha256sum` frozen capture = `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`, which is exactly
  the S249 digest named in the entry's front matter (line 1) — the file the rows cite is the frozen artifact.
  Re-run digest `c015d79f66b2a65c69c2a1ace22e60562b2c02b77d89a2e6db1745d2e91b9a77` (differs only in line 1).
- Scoped note (not a C2 finding): `capture.sh` sets `set -u` only (`capture.sh:6`) and has one `| head -n1`
  (`capture.sh:10`); it does not set `pipefail`, so it does not carry the C1 exit-141 hazard.

Receipts: `a2w1/C2ExecHostRecheck/capture-rerun.txt`, `a2w1/C2ExecHostRecheck/host-recheck-probes.txt` (§1–§4).

## 2. Citation check (item, part 2) — every `capture.txt:N` in the entry

Line numbers are those of the entry at `18389f44`; capture line numbers are from the re-run, which is identical.

| entry line | row | cites | capture line says | verdict |
|---|---|---|---|---|
| 51–53 | GR1 | `capture.txt:8`, `:1` | `scrub_speed_max 1d02a454-…/devinfo/1/scrub_speed_max mode=644 owner=root value=0`; `captured … uid=1000 CapEff=0000000000000000` | **match** — independently re-read: `-rw-r--r-- root root`, `stat` mode 644 owner root, value `0` (probe §5) |
| 88–89 | GR2 | `capture.txt:9`, `:1` | `devinfo 1d02a454-…/devinfo devids=1`; caps line | **mismatch in the conclusion**, see §3: the two cited lines are quoted correctly, but the clause "no replace or scrub state is observable to this caller" does not follow from them and is false |
| 124–127 | GR3 | `capture.txt:3`, `:4`, `:5`, `:2` | `unit_show … KillMode=control-group KillSignal=2 SendSIGKILL=yes TimeoutStopUSec=5s FinalKillSignal=9 …`; `stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`; `dropin_owner …/10-faster-shutdown.conf none`; `kernel 7.2.11-arch1-1 systemd 262 (262-1-arch)` | **match** — all five unit properties, the file:line, the `none` and `262-1-arch` are present verbatim; the row omits the also-captured `FragmentPath`, which does not contradict it |
| 145–146 (Limits) | GR1 | `capture.txt:1` | caps line | **supported but incompletely cited**: "the caller cannot write the attribute" needs the owner/mode pair from `capture.txt:8` as well as `CapEff=0` from `:1`; the claim itself is true (mode 644, owner root, uid 1000 not owner) |

Extra confirmations for GR3 (the host half of that row is the strongest of the three):

- `systemctl show 'btrfs-scrub@-.service' -p DropInPaths -p TimeoutStopUSec …` → `DropInPaths=` (empty),
  `TimeoutStopUSec=5s`; `ls -d /etc/systemd/system/btrfs-scrub@*.service.d …/service.d` → exit 2 (none exist), so
  `unit_dropins` (capture line 7) is truly empty and the unit has no own `KillMode=`/`TimeoutStopSec=`.
- The host's shipped unit is byte-identical to S244: `diff .ufo/waves/round-44/frozen/src/btrfs-scrub@.service
  /usr/lib/systemd/system/btrfs-scrub@.service` → exit 0 (so `KillSignal=SIGINT`, `ExecStart=… scrub start -B`,
  no `KillMode=` are the host's real unit, not just the snapshot's).
- Attribution of the 5 s: `systemctl show -p DefaultTimeoutStopUSec` → `DefaultTimeoutStopUSec=5s`;
  `systemd-analyze cat-config systemd/system.conf` shows `#DefaultTimeoutStopSec=90s` (the shipped file's comment,
  line 53) and `DefaultTimeoutStopSec=5s` from `10-faster-shutdown.conf` (line 98); the only other drop-in,
  `99-omarchy-nofile.conf`, sets `DefaultLimitNOFILE` only. So the 5 s does come from that drop-in's line 2.
- "no package owns that drop-in", checked two ways: the capture's own method (positive controls
  `grep -lxF 'usr/lib/systemd/system/btrfs-scrub@.service'` → `btrfs-progs-7.1-1/files`;
  `grep -lxF 'etc/systemd/system.conf'` → `systemd-262-1/files`; target → no output) and a different code path,
  `pacman -Qo /etc/systemd/system.conf.d/10-faster-shutdown.conf` → `error: No package owns …` (exit 1). True.

## 3. Finding — GR2's Host reading overstates unobservability (entry lines 88–89)

Cited text: "The filesystem lists devid 1 only (capture.txt:9) and the caller has no effective capabilities
(capture.txt:1): **no replace or scrub state is observable to this caller**, and the row is read from source."

What an unprivileged caller can actually read here (uid 1000, `CapEff=0000000000000000`, no sudo — probe §6):

```
$ ls -l /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/replace_target
-r--r--r-- 1 root root 4096 … /sys/fs/btrfs/1d02a454-…/devinfo/1/replace_target      # world-readable
$ cat  /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/replace_target    # 0
$ ls -l /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/exclusive_operation
-r--r--r-- 1 root root 4096 … /sys/fs/btrfs/1d02a454-…/exclusive_operation          # world-readable
$ cat  /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/exclusive_operation         # none
```

Both attributes are defined in the entry's own S243 snapshot (`.ufo/waves/round-44/frozen/src/sysfs.c`, v7.2.11 per
its `FETCH.txt`, digest `ce146120…` matching `SHA256SUMS`):

- `sysfs.c:1265` `btrfs_exclusive_operation_show`, registered at `sysfs.c:1302`
  `BTRFS_ATTR(, exclusive_operation, …)`; `sysfs.c:1287-1288`
  `case BTRFS_EXCLOP_DEV_REPLACE: str = "device replace\n";` — so a running replace is *named* to any reader.
- `sysfs.c:2007` `btrfs_devinfo_replace_target_show` (`val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, …)`),
  registered at `sysfs.c:2019`; it is one of `devid_attrs[]` (`sysfs.c:2107-2116`), the same attribute group as
  `scrub_speed_max` (`sysfs.c:2021-2029`) that the entry reads from `capture.txt:8`.

Scope of the refutation, stated exactly:

- **Refuted:** "no replace … state is observable". Replace state is observable read-only (fs-level
  `exclusive_operation`; per-device `replace_target`), on this host and by this caller.
- **Not refuted:** "no … scrub state is observable". Scrub progress and the scrub record still need the privileged
  `BTRFS_IOC_SCRUB_PROGRESS` ioctl / root-only record files; in this snapshot's switch `exclusive_operation` has no
  scrub case at all (`sysfs.c:1271-1298`).
- **True on the host, but for a different reason:** nothing replace-shaped is running now — `exclusive_operation`
  reads `none` (i.e. none of none/balance/balance paused/device add/device remove/device replace/resize/swap
  activate) and `devinfo/1/replace_target` reads `0` (devid 1 is not a replace target). "the row is read from source"
  still holds, since the arithmetic and refusal paths are kernel code, not host state.

Why it matters beyond wording: the same entry's triage bullet (lines 134–136) tells the operator to "check the
replace first (GR2)" before reading an `EINPROGRESS`. As written, the Host reading says the operator *cannot* check it
unprivileged; in fact `cat /sys/fs/btrfs/<uuid>/exclusive_operation` is exactly the unprivileged check for it. The
capture itself does not record either attribute, so `capture.txt:1` carries none of this claim.

Optional hardening (not applied — the capture is frozen, and editing it would move S249's digest): add
`printf 'exclusive_operation %s\n' "$(cat /sys/fs/btrfs/*/exclusive_operation 2>/dev/null | paste -sd, -)"` and the
`replace_target` value to the devinfo loop, so the capture can evidence this row directly.

## 4. Caveat — `capture.txt:5`'s `none` conflates "unowned" with "grep failed" (value is right anyway)

`capture.sh:19` derives the owner with `grep -lxF -- "$rel" /var/lib/pacman/local/*/files 2>/dev/null`. That glob
matches the regular file `local/ALPM_DB_VERSION/files`, which is not a directory, so grep exits **2** with
`grep: /var/lib/pacman/local/ALPM_DB_VERSION/files: Not a directory (os error 20)` (discarded by `2>/dev/null`);
over the 1409 real `files` entries alone the exit is **1** (clean no-match) — probe §13. Both paths print
`none`, so a future unreadable/renamed db would be indistinguishable from a true negative.

For this round the conclusion is still correct, established independently: positive controls match (btrfs-progs owns
the unit, systemd owns `etc/systemd/system.conf`), no package lists any path under `etc/systemd/system.conf.d/`, and
`pacman -Qo` (different code path) says `No package owns` for both drop-ins. Recommendation for a later round: have
`dropin_owner` print `none` and `err` distinctly (e.g. capture grep's status), or use `pacman -Qo`.

## 5. Incidental host observation (outside the C2 rows, no claim affected)

Every `pacman` invocation on this host prints `error: openai-chatgpt: missing required signature` before its answer
(`pacman -Qo /etc/hostname` → that error then `error: No package owns /etc/hostname`). Cause visible read-only:
`/etc/pacman.conf:32` includes `/etc/pacman.d/openai-chatgpt.conf`, whose section sets
`SigLevel = Required DatabaseRequired TrustedOnly`, while the repo's db and sig exist
(`/var/lib/pacman/sync/openai-chatgpt.db`, `openai-chatgpt.db.sig`, 566 bytes, `file` says "data"). Queries still
answer; any pacman transaction would trip on this repo. Not investigated further (out of item scope, and all pacman
transactions are paused host-wide). It does not affect the capture, which reads the pacman db as files and calls no
package-manager binary (`capture.sh:4-5`).

## 6. Draft — corrected GR2 Host reading (replaces entry lines 88–89)

> **Host reading.** The filesystem lists devid 1 only (capture.txt:9) and the caller has no effective capabilities
> (capture.txt:1). Replace state is nevertheless readable by that caller: `/sys/fs/btrfs/<uuid>/exclusive_operation`
> and `devinfo/<devid>/replace_target` are world-readable attributes (S243 sysfs.c:1302, 2019) and here read `none`
> and `0` (uid 1000, CapEff 0), so no replace or other exclusive operation is in progress and devid 1 is not a
> replace target; during a replace the first reads `device replace` (sysfs.c:1287-1288). Scrub progress and the scrub
> record stay unreadable to this caller (privileged ioctl), so the row itself is read from source.

Numbers in the draft are the readings of 2026-10-27T03:24:32Z and are re-runnable with `capture.sh` plus the two
`cat`s; if the draft is adopted, the front-matter `recheck` line should mention them.

## 7. What I did not do

- Did not write to any sysfs attribute, start/stop/enable/kill any unit, run a scrub or replace, or call a privileged
  ioctl — the parse examples and the stop ordering remain untested by execution, as the entry itself says.
- Did not re-fetch S246/S247/S248 from their URLs; I only re-verified the local digests of the S243/S244 snapshots
  (`sha256sum` in `.ufo/waves/round-44/frozen/src` matches its `SHA256SUMS`) and the shipped unit against S244.
- Did not run the C2 counter (`tools/check-scrub-grounding-r45.py`) — that is the counted seats' instrument, not this
  item's; did not run any C1 counter.
- Did not edit anything: no lane file changed (`git status --porcelain` shows only untracked files under
  `.ufo/waves/round-45/a2w1/`), no package installed, no tool upgraded (nothing was needed).

## Evidence index

- `a2w1/C2ExecHostRecheck/capture-rerun.txt` — the re-run, 9 lines, `2026-10-27T03:24:32Z`.
- `a2w1/C2ExecHostRecheck/host-recheck-probes.txt` — §1–§15: both sha256s, both diffs, sysfs modes/values as uid
  1000, `systemctl show` (unit + manager default), `systemd-analyze cat-config`, unit diff vs S244, pacman-db
  ownership with positive controls and the `pacman -Qo` cross-check, the grep-exit analysis, the `openai-chatgpt`
  error.
- Grounding entry: `corpus/knowledge/btrfs-scrub-grounding-r45.md` @ `18389f44` (sha `129b351b…`), lines 51–53,
  88–89, 124–127, 134–136, 145–146.
- Snapshots: `.ufo/waves/round-45/frozen/hostcap/capture.txt` (sha `f5958a83…`), `…/capture.sh` (sha `c6d2c448…`),
  `.ufo/waves/round-44/frozen/src/{sysfs.c,scrub.c,btrfs-scrub@.service}` (digests match that dir's `SHA256SUMS`).
- Scratch `/fast/scratch/hyaku/tsukuroi-r45/C2ExecHostRecheck/` removed at end of run.
