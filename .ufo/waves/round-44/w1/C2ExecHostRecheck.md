VERDICT: supports

Seat C2ExecHostRecheck, item C2-2 (hyaku round 44, wave w1). Item: re-run the frozen own-work host capture,
diff against the frozen capture (expect only the timestamp to differ), audit each `**Host reading.**` line of
`corpus/knowledge/btrfs-scrub-record-r44.md` against the capture line it cites, and re-check
`stat -c '%a %U %G' /sys/fs/btrfs/*/devinfo/*/scrub_speed_max` and
`systemctl is-enabled btrfs-scrub@-.timer btrfs-scrub@home.timer`. All reads unprivileged (uid 1000,
CapEff=0), read-only; nothing was written outside this seat's receipt dir and scratch, no sysfs/unit/pacman
mutation, no scrub command, no privileged ioctl.

No mismatch found: the re-run reproduces the frozen capture field-for-field, and all three Host reading lines
are borne out by the capture line they cite (two citation-scope notes, no factual error — see "Notes").

## 1. Capture re-run and diff

Frozen script (read before running): `.ufo/waves/round-44/frozen/hostcap/capture.sh` — reads only
(`date`, `id`, `awk` over `/proc/self/status`, `pacman -Q`, `stat`, `cat` of the sysfs attribute, glob over
`/etc/systemd/system/timers.target.wants`, `systemctl is-enabled`, `sha256sum`, `pacman -Qo`) and writes only
`$1` (capture.sh:5-22).

Command (cwd = my scratch, TMPDIR set there):

```
/usr/bin/bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/frozen/hostcap/capture.sh \
  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-44/w1/C2ExecHostRecheck/capture-rerun.txt
exit=0
```

Re-run output (`capture-rerun.txt`, 649 bytes):

```
captured 2026-10-27T00:12:21Z uid=1000 CapEff=0000000000000000
kernel 7.2.11-arch1-1 btrfs-progs btrfs-progs 7.1-1
var_lib_btrfs absent
scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max mode=644 owner=root value=0
wants_btrfs_scrub_instances 0
is_enabled_btrfs-scrub@-.timer disabled
installed_unit 9a0b6cc23f7bd97b83b6c38dd2b4e4373fead8bd3ccfb82a47c72971e9d6f8ad  /usr/lib/systemd/system/btrfs-scrub@.timer
installed_unit eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252  /usr/lib/systemd/system/btrfs-scrub@.service
pacman_owner /usr/lib/systemd/system/btrfs-scrub@.timer is owned by btrfs-progs 7.1-1
```

Diff against the frozen capture (`diff -u`, receipt `capture-diff.txt`; footer of the hunk shown by `diff`
is why `diff` exits 1):

```
@@ -1,4 +1,4 @@
-captured 2026-10-26T23:53:22Z uid=1000 CapEff=0000000000000000
+captured 2026-10-27T00:12:21Z uid=1000 CapEff=0000000000000000
 kernel 7.2.11-arch1-1 btrfs-progs btrfs-progs 7.1-1
 var_lib_btrfs absent
 scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max mode=644 owner=root value=0
```

Only line 1's UTC timestamp differs. Normalising the timestamp field on both files and comparing byte-for-byte:

```
sed 's/^captured [^ ]*/captured TS/' <frozen> > f.norm ; sed 's/^captured [^ ]*/captured TS/' <rerun> > n.norm
cmp f.norm n.norm && echo normalised_identical=yes
normalised_identical=yes
```

Both files are 649 bytes; the re-run spans UTC midnight (frozen 2026-10-26T23:53:22Z, re-run
2026-10-27T00:12:21Z, 19 min later). Digests:

```
sha256sum .ufo/waves/round-44/frozen/hostcap/capture.txt
efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900  .../frozen/hostcap/capture.txt
sha256sum .ufo/waves/round-44/w1/C2ExecHostRecheck/capture-rerun.txt
99ffd7e4c50a2d29c884ddb04590d648da5c2e7f123bc1677c40ab48845deb5b  .../w1/C2ExecHostRecheck/capture-rerun.txt
```

The frozen digest is unchanged by this seat (it equals the `S245` digest stated in the entry's header line 1,
`efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900`; mtime still
2026-10-26 20:53:22 -0300). The re-run digest is *not* meant to equal it — the timestamp line is part of the
pinned bytes — so `capture-rerun.txt` is kept only as a receipt and does not replace the frozen file.

## 2. Host reading audit (entry line — cited capture line)

Line numbers are `nl -ba` of the frozen capture (9 lines, receipt `host-checks.txt` section "frozen capture
numbered" evidence: lines 1-9 listed in §1 above).

| Row | Host reading claim | Cited line | Does the cited line say it? |
|---|---|---|---|
| SR7 | "Not observable unprivileged: the caller has no effective capabilities (capture.txt:1), so the ioctl stops at the SR6 gate before this code runs (round-43 S241)." | 1 | Yes. Line 1 = `captured … uid=1000 CapEff=0000000000000000` — `CapEff` is all-zero, i.e. no effective capabilities in the capturing process, and uid 1000. The SR6-gate consequence is attributed to round-43 S241, not to the capture; that attribution is consistent with `corpus/knowledge/btrfs-scrub-record-r43.md:105` and `:123` (`"if (!capable(CAP_SYS_ADMIN))"`). |
| SR8 | "The root filesystem's only device (devid 1) has `scrub_speed_max` mode 644, owner root, value 0: no limit (capture.txt:4), read as uid 1000 with no effective capabilities (capture.txt:1)." | 4, 1 | Yes for mode/owner/value/devid: line 4 = `scrub_speed_max 1d02a454-…/devinfo/1/scrub_speed_max mode=644 owner=root value=0`. "only device": the script's loop enumerates *every* `/sys/fs/btrfs/*/devinfo/*/scrub_speed_max` and printed one line, and live enumeration confirms one fsid and one devinfo (`ls -1 /sys/fs/btrfs/` → `1d02a454-c549-4a35-b567-89d60902af8e`, `features`; `ls -1 …/devinfo/` → `1`). "root filesystem's" is not literally in line 4 (see Note A); on the live host the binding holds: `findmnt -t btrfs` → `/dev/mapper/root[/@] / btrfs`, `/dev/mapper/root[/@home] ├─/home`, `/dev/mapper/root[/@pkg]`, `/dev/mapper/root[/@log]`, and `btrfs filesystem show` → `uuid: 1d02a454-c549-4a35-b567-89d60902af8e … Total devices 1 … devid 1 … path /dev/mapper/root`. `value=0` ↔ "no limit" is the SR8 statement's kernel code, not a capture claim. |
| SR9 | "No instance is enabled: no `btrfs-scrub@*.timer` link under `timers.target.wants` (capture.txt:5), `btrfs-scrub@-.timer` is `disabled` (capture.txt:6); the installed unit files are byte-identical to the pinned ones (capture.txt:7, capture.txt:8) and belong to btrfs-progs 7.1-1 (capture.txt:9)." | 5, 6, 7, 8, 9 | Yes. Line 5 = `wants_btrfs_scrub_instances 0`; line 6 = `is_enabled_btrfs-scrub@-.timer disabled`; line 7/8 = timer `9a0b6cc2…d6f8ad`, service `eaa7af92…ba240252`, which equal the frozen `SHA256SUMS` entries for `btrfs-scrub@.timer` / `btrfs-scrub@.service` and `cmp` byte-identical against `.ufo/waves/round-44/frozen/src/`; line 9 = `… btrfs-scrub@.timer is owned by btrfs-progs 7.1-1` (timer only — Note B). |

Line 2 (`kernel 7.2.11-arch1-1 btrfs-progs btrfs-progs 7.1-1`) and line 3 (`var_lib_btrfs absent`) are not cited
by a Host reading, but the entry's `verified-at:` header does assert `kernel 7.2.11-arch1-1`,
`host btrfs-progs 7.1-1` and `capture 2026-10-26T23:53:22Z` — all three match lines 2 and 1 respectively. The
doubled package name on line 2 is a script artefact (`pacman -Q btrfs-progs` prints `btrfs-progs 7.1-1` and the
`printf` already says `btrfs-progs`), reproduced exactly:
`printf 'kernel %s btrfs-progs %s\n' "$(uname -r)" "$(pacman -Q btrfs-progs 2>/dev/null)"` →
`kernel 7.2.11-arch1-1 btrfs-progs btrfs-progs 7.1-1`. The entry does not quote that line, so nothing to fix.

## 3. Additional read-only checks the item names

`stat -c '%a %U %G' /sys/fs/btrfs/*/devinfo/*/scrub_speed_max` (exit 0):

```
644 root root /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max
```

Mode 644 and owner root match SR8's statement (`BTRFS_ATTR_RW` → 0644, S243 sysfs.c:72,74) and its Host
reading; group is also root (not claimed by the row). Value still `0`
(`cat …/scrub_speed_max` → `0`).

`systemctl is-enabled` (read-only; per-unit exit codes recorded because multi-arg `is-enabled` collapses them):

```
btrfs-scrub@-.timer   rc=1 out=disabled
btrfs-scrub@home.timer rc=1 out=disabled
systemctl list-unit-files 'btrfs-scrub@*'
btrfs-scrub@.service static   -
btrfs-scrub@.timer   disabled disabled
systemctl is-enabled 'btrfs-scrub@-.service' -> rc=0 out=static
```

Independent confirmation of the `timers=` count (the capture's `0` is only meaningful if the glob directory
exists — it does):

```
ls -la /etc/systemd/system/timers.target.wants/
… fstrim.timer, paccache.timer, snapper-cleanup.timer, snapper-timeline.timer   (4 links, no scrub link)
find /etc/systemd -name 'btrfs-scrub*'   → no output, rc=0
```

So SR9's "No instance is enabled" holds for both the root instance `-` and `home`, and the `timers=` counter
inputs saw a populated wants directory, not a missing one.

## 4. Notes (citation scope, not factual error)

- **Note A (SR8, capture.txt:4).** Line 4 shows the fsid, `devinfo/1`, mode 644, owner root, value 0, and the
  script's full glob printed only that one device, so "only device (devid 1)" is evidenced. The words "root
  filesystem's" are not evidenced by line 4 alone: nothing in the capture binds the fsid to `/`. The binding is
  true on this host (`findmnt -t btrfs` plus `btrfs filesystem show`, §2) but comes from checks outside the
  capture. Optional tightening, if the L1 wants the citation exact: "The host's only btrfs device (fsid
  1d02a454-…, devid 1; `/dev/mapper/root`, the root filesystem) has `scrub_speed_max` mode 644, owner root,
  value 0". Not required for the row to stand.
- **Note B (SR9, capture.txt:9).** Line 9 records `pacman -Qo` for the *timer* file only; the service file's
  package ownership is not in the capture. It follows from line 8 plus the byte-identical package content
  (`cmp` identical to `frozen/src/btrfs-scrub@.service`, whose digest is in the same `SHA256SUMS`), and I
  confirmed live: `pacman -Qo /usr/lib/systemd/system/btrfs-scrub@.service` →
  `… is owned by btrfs-progs 7.1-1`. Non-blocking.

## 5. Incidental host observation (outside this item; no effect on any capture line)

Every read-only `pacman` invocation on this host prints to stderr:

```
error: openai-chatgpt: missing required signature
pacman -Q openai-chatgpt        → error: openai-chatgpt: missing required signature
                                  error: package 'openai-chatgpt' was not found (rc=1)
```

`/etc/pacman.conf` declares only `[core] [extra] [multilib] [omarchy]` (`grep -n '^\[' /etc/pacman.conf`,
lines 19/22/25/28), while `/var/lib/pacman/sync/` additionally holds an orphan pair
`openai-chatgpt.db` (1393 bytes) and `openai-chatgpt.db.sig` (566 bytes), both mtime 2026-10-20 23:22. The
message is stderr-only and `capture.sh` drops pacman stderr (`2>/dev/null`), so capture lines 2 and 9 are
unaffected and the frozen capture is not wrong; the reproduction in §1 is identical. Reporting it because the
lane owns host operability: it is an untrusted/orphan repo database, not a package (no local package of that
name). I did not attempt to remove it (no pacman transactions; the pacman guard pauses all of them).

## 6. What I did not do

- No privileged ioctl, no `btrfs scrub start/cancel/resume/limit`, no `btrfs device stats -z`, no sysfs write
  (did not touch `scrub_speed_max`), no `systemctl enable/start/stop`, no mount, no package transaction, no sudo.
- Did not run the C1 counter (`tools/score-scrub-arm-r44.py`), the census selftest, or the C2 counter
  (`tools/check-scrub-record-r44.py`) — those are other seats' items; this seat's evidence is host reads only.
- Did not edit, create or delete any tracked lane file; wrote only this report and §7's receipts.
- No tool installs (nothing needed).

## 7. Receipts and scratch

- `.ufo/waves/round-44/w1/C2ExecHostRecheck/capture-rerun.txt` (649 B) — the re-run output.
- `.ufo/waves/round-44/w1/C2ExecHostRecheck/capture-diff.txt` (609 B) — `diff -u` frozen vs re-run.
- `.ufo/waves/round-44/w1/C2ExecHostRecheck/host-checks.txt` (3729 B) — stat, is-enabled, unit digests,
  `cmp` vs frozen, SHA256SUMS, findmnt, `btrfs filesystem show`, `pacman -Qo`, pacman stderr observation.
- Scratch `/fast/scratch/hyaku/tsukuroi-r44/C2ExecHostRecheck/` held only `f.norm`/`n.norm` normalised
  captures and was removed after the receipts were copied (`rm -rf`); nothing was built or cloned.

Summary: the frozen capture re-runs clean (only the timestamp differs, byte-identical after normalising), the
three Host readings (SR7, SR8, SR9) cite lines that say what they claim, `scrub_speed_max` is `644 root root`
live, and both `btrfs-scrub@-.timer` and `btrfs-scrub@home.timer` are `disabled` — supports the C2 row set.
