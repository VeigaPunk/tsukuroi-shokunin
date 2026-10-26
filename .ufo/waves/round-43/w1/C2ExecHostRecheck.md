VERDICT: supports

# C2ExecHostRecheck (item C2-2) — host capture re-run, byte-by-byte

Seat: leaf executor, wave w1 of round 43. Scope: re-run the frozen S241 capture unprivileged and read-only, diff it against
`.ufo/waves/round-43/frozen/hostcap/capture.txt` line by line, and record capability/permission, `btrfs scrub status -d` / `-R`
and `/var/lib/btrfs` state. Question asked of the item: does SR6's host reading still hold? **Yes — every reading in S241
reproduces, the only differing line is the live size, and SR6's mechanism (kernel-only, `CAP_SYS_ADMIN`-gated running state) is
independently confirmed by `strace` of the real `btrfs` binary and by a user-namespace probe.** SR1's and SR3's host readings
("not observable on this host") are also unchanged.

All receipts are in `.ufo/waves/round-43/w1/C2ExecHostRecheck/`; all paths below are relative to
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` unless absolute.

## 1. Re-run reproduced the frozen capture

```
bash .ufo/waves/round-43/frozen/hostcap/capture.sh .ufo/waves/round-43/w1/C2ExecHostRecheck/capture-rerun.txt
```
exit 0 (`capture_rc=0`). Frozen `capture.txt` sha256 `f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556`
(unchanged, matches `corpus/SOURCES.md:250` and the S241 sha in `btrfs-scrub-record-r43.md` front matter); re-run
`capture-rerun.txt` sha256 `e26abbdd34cf6da85ab7cd829c2f13294586544b62cd036df2f5b0c209785bd5`. Digests differ only because of
lines 1 and 11 (below). `capture.sh` itself is unmodified: sha256 `77ffeecb4955a36324efa45d8c07b03d7879ed232cf3cd4d20aea9cb36d2a1a9`.

Line-by-line (both files are exactly 13 lines; `wc -l` = 13/13; receipts `capture-linecmp.txt`, `capture-diff-raw.txt`,
empty `capture-diff.txt` = normalized diff clean, `diff_rc=0`):

| line | frozen | re-run | state |
|---|---|---|---|
| 1 | `captured_utc 2026-10-26T21:51:26Z` | `captured_utc 2026-10-26T22:16:35Z` | expected timestamp delta (25m09s later) |
| 2 | `uid 1000 euid_caps 0000000000000000` | same | identical |
| 3 | `kernel 7.2.11-arch1-1` | same | identical |
| 4 | `btrfs_progs btrfs-progs 7.1-1` | same | identical |
| 5 | `root_fs btrfs 1d02a454-c549-4a35-b567-89d60902af8e` | same | identical (same fs UUID, same fstype) |
| 6 | `scrub_progress_ioctl devid=1 errno=EPERM (1)` | same | identical — the load-bearing line for SR6 |
| 7 | `var_lib_btrfs absent` | same | identical — the load-bearing line for SR1/SR3 |
| 8 | `scrub_status_exit 0` | same | identical |
| 9 | `scrub_status\| UUID:             1d02…af8e` | same | identical |
| 10 | `scrub_status\| \tno stats available` | same | identical (byte `^I` tab, `cat -A` verified) |
| 11 | `scrub_status\| Total to scrub:   309.39GiB` | `…309.54GiB` | **only value difference** — a live filesystem-usage figure |
| 12 | `scrub_status\| Rate:             0.00B/s` | same | identical |
| 13 | `scrub_status\| Error summary:    no errors found` | same | identical |

Line 11 is not stale state: it tracks `bytes_used` (`BTRFS_IOC_DEV_INFO … bytes_used=399507456000` per `strace-raw-codes.txt:2`),
and a third capture 56 s after the re-run still reads `309.54GiB` (`capture-third.txt:11`, sha256
`bd0ba7f2508b71cd9ef7dcbbf0d0286b7a587e40e65bb65cef012110b7640a0c`). No other line drifted across three runs.

Conclusion for the capture as a source: S241 is reproducible on this host at 2026-10-26T22:16:35Z and 22:17:31Z, i.e. the
timestamps in S241 are not a one-off and nothing in it has silently aged except the byte count.

## 2. Capability state: no effective capabilities

- `id`: `uid=1000(vgpnk) gid=1000(vgpnk) groups=1000(vgpnk),967(docker),992(input),998(wheel)` (`caps.txt:2`).
- `getpcaps $$` → `3438: cap_wake_alarm=i` (`caps.txt:4`), exit 0.
- `/proc/self/status` (`caps.txt:6-10`): `CapInh: 0000000800000000`, `CapPrm: 0000000000000000`,
  `CapEff: 0000000000000000`, `CapBnd: 000001ffffffffff`, `CapAmb: 0000000000000000`.
- `capsh --print` (`caps.txt:12-14`): `Current: cap_wake_alarm=i`, full bounding set present (`cap_sys_admin` included),
  `Ambient set =`, `Securebits: 00/0x0/1'b0 (no-new-privs=0)`.

So the re-run reproduced capture.txt:2 exactly: uid 1000, `CapEff` all zero — and note the interesting asymmetry that the
*inheritable* set carries bit 35 (`cap_wake_alarm`) while effective is empty; that is not a path to `CAP_SYS_ADMIN`.

## 3. `btrfs scrub status` variants — exit codes and output

Receipt `scrub-status-variants.txt`:

- `btrfs scrub status -d /` → **exit 0**; prints `UUID: 1d02…af8e`, blank line, `Scrub device /dev/mapper/root (id 1) `,
  `\tno stats available`.
- `btrfs scrub status -R /` → **exit 0**; prints `UUID: …`, `\tno stats available`, then raw counters all zero:
  `data_extents_scrubbed: 0`, `tree_extents_scrubbed: 0`, `data_bytes_scrubbed: 0`, `tree_bytes_scrubbed: 0`,
  `read_errors: 0`, `csum_errors: 0`, `verify_errors: 0`, `no_csum: 0`, `csum_discards: 0`,
  `super_errors: 0`, `malloc_errors: 0`, `uncorrectable_errors: 0`, `unverified_errors: 0`, `corrected_errors: 0`,
  `last_physical: 0`.
- `btrfs scrub status -dR /` → exit 0, device form only (the plain summary block is not printed with `-d`).
- `btrfs scrub status /` → exit 0, the 5-line summary block of capture.txt:9-13.

Exit-code semantics (`exit-semantics.txt`): exit is **1 only for a path error** — `path=/proc exit=1 out=ERROR: not a btrfs
filesystem: /proc`, `path=/nonexistent-path-xyz exit=1 out=ERROR: cannot check … / No such file or directory`. For a valid
btrfs mount with **no record and no permission the exit code is 0 and stderr is empty** (`rc=0 stderr_bytes=0`). Absence of a
record is silent.

Triage caution for the record line (not a claim change): `-R` with no record still emits a *complete, all-zero* counter block
next to `no stats available`. A census or operator reading only the `key: value` lines of `-R` sees a plausible
"everything zero" block with exit 0; the discriminator is the `no stats available` line and `last_physical: 0`, not the exit
code. `scrub.c:321` prints that line when `!ss || !ss->t_start`.

## 4. `/var/lib/btrfs` — still absent

`var-lib-btrfs.txt`:
- `ls -la /var/lib/btrfs` → `ls: cannot access '/var/lib/btrfs': No such file or directory`, **`ls_rc=2`**.
- `test -e /var/lib/btrfs` → `test_e_rc=1`.
- `stat /var/lib` → `/var/lib root:root 755`.
- `find /var/lib/btrfs -maxdepth 1` → `Error: /var/lib/btrfs: No such file or directory (os error 2)`, `find_rc=1`.

Matches `capture.txt:7` and therefore leaves SR1's and SR3's host readings ("Not observable on this host: there is no record
directory") exactly as written. There is no `scrub.status.<fsid>` to attempt a mode-0600 refusal against, so the SR6 "Limits"
sentence about reading "the record's absence or its mode-0600 refusal" is, on this host today, exercised only in its
*absence* arm.

## 5. Independent confirmation of SR6's mechanism (beyond the capture script)

The capture script hand-computes its ioctl number instead of using the kernel header. To check the probe is the same call
`btrfs` makes, I traced the real binary (`strace-scrub-status.txt`, `strace-raw-codes.txt`):

```
2691203 ioctl(3, BTRFS_IOC_SCRUB_PROGRESS, {devid=makedev(0, 0x1)}) = -1 EPERM (Operation not permitted)
2754124 ioctl(3, 0xc400941d, {devid=0x1}) = -1 EPERM (Operation not permitted)
```

`strace`'s symbol decoder names `0xc400941d` as `BTRFS_IOC_SCRUB_PROGRESS`, and Python `_IOWR(0x94,29,1024)` computes
`0xc400941d` (`strace-raw-codes.txt`, last section). So the capture's `REQ = 0xC400941D` is the correct request code and its
`EPERM` is the same error the tool gets — not a mis-encoded argument producing a different errno.

Source-side chain, all read at the frozen pins:
- `scrub.c:986` and `scrub.c:1200`: `ret = ioctl(fd, BTRFS_IOC_SCRUB_PROGRESS, &sp.scrub_args);` inside
  `is_scrub_running_in_kernel` (`scrub.c:1190`) — followed by `scrub.c:1201: if (!ret)` → return 1. Any failure, whatever the
  errno, is "not running"; there is no errno branch.
- `scrub.c:1946: in_progress = is_scrub_running_in_kernel(fdmnt, di_args, fi_args.num_devices);` is the only assignment
  feeding the print path (`grep -n in_progress` → `:78`, `:186`, `:341`, `:1859`, `:1946`, `:1962`, `:1974`; `:1962`
  `last_scrub->stats.in_progress = in_progress;`, `:1974` `fs_stat.s.in_progress = in_progress;`).
- `scrub.c:341: (ss->in_progress ? "running" :` is the only place the word `running` can come from in the summary.
- Kernel gate, first statement of the function: `ioctl.c:3126` `static long btrfs_ioctl_scrub_progress(…)`,
  `ioctl.c:3132` `if (!capable(CAP_SYS_ADMIN))`, `ioctl.c:3133` `return -EPERM;` — ahead of `memdup_user`, so the gate precedes
  any argument validation. Same shape at `ioctl.c:3066`/`:3072` (`btrfs_ioctl_scrub`) and `ioctl.c:3118`/`:3120`
  (`btrfs_ioctl_scrub_cancel`), which bears out SR6's "as do the scrub start and cancel ioctls".
- Dispatch: `ioctl.c:5582: case BTRFS_IOC_SCRUB_PROGRESS:` → `btrfs_ioctl_scrub_progress`.

Two extra read-only discriminations (receipts `devid-and-third.txt`, `userns-probe.txt`):

1. **The EPERM is the permission gate, not a bad devid.** devid 1 → `errno=EPERM (1)`; devid 999 (nonexistent) →
   `errno=EPERM (1)`. The gate fires before the devid is ever looked at.
2. **User-namespace root does not lift it.** Inside `unshare -r -m`: `id -u` = 0, `CapEff: 000001ffffffffff`
   (all capabilities in that namespace), `capsh --print` shows `Current: =ep` — and the ioctl still returns `errno=EPERM (1)`
   for devid 1. `capable()` checks `init_user_ns`, so SR6's "elevation-gated" means real host root; a container/userns root
   proves nothing. Observed output for that user namespace also contains no `running` line.

## 6. Does SR6's host reading still hold?

Yes, line for line. SR6 states: as uid 1000 with no effective capabilities the ioctl fails `EPERM`; `btrfs scrub status`
therefore has `in_progress = 0` and never prints `running`; with no record the summary prints no status word. Observed:
`capture-rerun.txt:2` (uid 1000, `euid_caps 0000000000000000`), `:6` (`errno=EPERM (1)`), `:8-13` (exit 0, `no stats available`,
no `Status:`/`Scrub started`/`running` anywhere in any of the four output variants), plus `caps.txt:9` `CapEff:
0000000000000000` and the strace line above. The one caveat, unchanged from the doc's own "Limits": this host shows the EPERM
coming from the Arch 7.2.11-arch1-1 kernel; I did not confirm the Arch kernel applies no patch to `fs/btrfs/ioctl.c` — the
observed errno is consistent with the upstream line, not proof of an unpatched build.

No proposed text change to SR6, SR1 or SR3. Every assertion in them that touches the host reproduces.

Optional strengthening (a **candidate**, per round-42 lesson QUALITY 91 — not evidence, not a counted verdict): append to
SR6's **Host reading** —

> A private user namespace does not change this: inside `unshare -r -m` the caller has `id -u` 0 and
> `CapEff 000001ffffffffff`, and `BTRFS_IOC_SCRUB_PROGRESS` on `/` for devid 1 still returns `EPERM` (wave-1 receipt
> `.ufo/waves/round-43/w1/C2ExecHostRecheck/userns-probe.txt`), because `capable()` tests the initial user namespace. The same
> errno is returned for devid 999, so the failure is the permission gate (`ioctl.c:3132-3133`), not device validation; and
> `strace` names the traced request `0xc400941d` as `BTRFS_IOC_SCRUB_PROGRESS`, matching the capture probe's hand-computed
> constant.

## Limits / what I did not do

- No scrub was started, resumed, canceled or limited; no btrfs ioctl other than the read-only `BTRFS_IOC_SCRUB_PROGRESS`
  probe (and the ones `btrfs scrub status` itself issues: `FS_INFO`, `DEV_INFO`, `SPACE_INFO`); no `btrfs device stats -z`.
  The only namespaced operation was `unshare -r -m` (private, no mount performed).
- No package, service, sysfs, mount or `/etc`, `/var/lib` change; no sudo; no PATH write; **no tool installs or upgrades**
  (`strace`, `capsh`, `python3` were already present; nothing to record).
- Not checked: whether the Arch kernel patches `fs/btrfs/ioctl.c`; the mode-0600 refusal arm of SR6's Limits (no record
  exists); SR1/SR3 behaviour that needs a real scrub. I did not run `tools/check-scrub-record-r43.py` or any census counter —
  out of scope for C2-2.
- Lane was read-only throughout: no git/jj command at all, no lane file written outside
  `.ufo/waves/round-43/w1/C2ExecHostRecheck{,.md}`.

## Receipts

`.ufo/waves/round-43/w1/C2ExecHostRecheck/`: `capture-rerun.txt` (re-run, 13 lines), `capture-third.txt` (third run),
`capture-linecmp.txt` (per-line SAME/DIFF), `capture-diff.txt` (normalized diff, empty = clean), `capture-diff-raw.txt`
(raw diff, 2 hunks), `caps.txt` (id/getpcaps/CapEff/capsh), `scrub-status-variants.txt` (`-d`, `-R`, `-dR`, plain),
`var-lib-btrfs.txt`, `strace-scrub-status.txt`, `strace-raw-codes.txt`, `userns-probe.txt`, `devid-and-third.txt`,
`exit-semantics.txt`, `probe.py`, `probe_devid.py`.
