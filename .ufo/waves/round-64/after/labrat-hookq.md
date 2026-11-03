# C3-HYPOTHESIS — LB1HookQ labrat: btrfs-overlayfs silent no-op on the current boot

captured: 2026-11-03T18:43:21Z (read-only; no pacman transaction, no sudo, no boot action, no /boot write)
host: plazir27, `Linux 7.2.11-arch1-1`, `mkinitcpio 42.2-1`
scratch: `/fast/scratch/hyaku/tsukuroi-r64/LB1HookQ/` (removed before yield; no /tmp path is cited as evidence)

## VERDICT: `h-refuted`

The hypothesis under test was *"the `/new_root` lookup found no mountpoint, so no overlay was set up by the hook after switch-root."*

**The stated mechanism is false and the no-op outcome is nevertheless true — for a different reason.**

- **Mechanism refuted [obs]:** `/new_root` *is* resolvable in a v42 image. mkinitcpio 42.2 creates `new_root -> sysroot` as a symlink (`/usr/lib/initcpio/functions:1213`), and `findmnt --mountpoint` resolves through that symlink to the real mountpoint. The hook's line 7 predicate therefore **succeeds**, and line 11 returns a usable SOURCE. There is no lookup failure, and no `|| return 0` fires at lines 7 or 11.
- **Outcome (no overlay this boot) confirmed [obs]:** root is plain btrfs, no overlay mount exists, and no hook artifact survives.
- **Actual gate [obs]:** the hook returns 0 at **line 14** (`*) return 0 ;; # not a snapshot subvolume`), because `/` is the normal `subvol=/@` and not a `/snapshot` subvolume. The no-op is *by design for a normal boot*, not a v42 regression.

This **reverses** the r1 note's `[inf]` at `corpus/knowledge/initramfs-v42-sysroot-recovery.md:14` and its falsifier framing at `:32`, and it agrees with (and re-derives independently) the withdrawal already recorded at `## R17-SYMLINK` in the same file.

## 1. Falsifier probes — executed, with exact commands

```
$ uname -r
7.2.11-arch1-1
rc=0

$ pacman -Q mkinitcpio limine-mkinitcpio-hook plymouth util-linux
mkinitcpio 42.2-1
limine-mkinitcpio-hook 1.40.0-2
plymouth 26.134.222-3
util-linux 2.42.4-1
rc=0
```

```
$ findmnt -no TARGET,SOURCE,FSROOT,OPTIONS /
/ /dev/mapper/root[/@] /@ rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@
rc=0

$ findmnt -t overlay -o TARGET,SOURCE,FSTYPE,FSROOT
rc=0            # header only — zero overlay mounts

$ findmnt -no FSTYPE /
btrfs
rc=0

$ grep -c 'overlay' /proc/mounts
0
rc=1
```

**`FSROOT=/@` and `subvol=/@` is the decisive datum.** The hook's line 13 pattern is `*/snapshot*`; `/@` does not match.

```
$ cat /proc/cmdline
resume=/dev/mapper/root resume_offset=3795013 quiet splash loglevel=0 systemd.show_status=false rd.udev.log_level=0 vt.global_cursor_default=0 cryptdevice=PARTUUID=cf3d875f-72a4-4468-9795-015c9e953618:root:allow-discards,no-read-workqueue,no-write-workqueue root=/dev/mapper/root zswap.enabled=1 zswap.max_pool_percent=25 rootflags=subvol=@ rw rootfstype=btrfs
rc=0
```

`rootflags=subvol=@` — the kernel cmdline itself confirms a normal `@` boot, not a snapshot boot.

### Journal sweeps

```
$ journalctl -b --no-pager | grep -inE 'btrfs-overlayfs|overlayfs'
rc=0, 36 matching lines — ALL timestamped Nov 03 15:38:04, 15:39:19, 15:39:33, 15:41:07, 15:41:23, 15:41:30
```

**These are not boot-time lines and must not be read as hook evidence.** Boot was `2026-11-02 12:07:17 -03:00`; the earliest overlayfs line is `2026-11-03 15:38:04 -03:00` — **1 day 3:30:47 after boot**. Their neighbours in the journal are `Starting DBus interface for snapper...` / `Started DBus interface for snapper.` and, minutes later, Chromium and `ai-usage` scopes. These are runtime overlay mounts (container/namespace-shaped: `overlayfs: failed to set xattr on upper`, `...falling back to redirect_dir=nofollow`, `try mounting with 'userxattr' option`), not initramfs activity.

```
$ journalctl -b --no-pager | grep -c 'OverlayFS setup'
0
grep_rc=1
```

The hook's own banners (`hook:21` "…Setting up OverlayFS…", `hook:56` "OverlayFS mounted on …") are **absent**. This is *consistent* with a no-op but is **silence, not proof** — see §5.

```
$ journalctl -b --no-pager | grep -inE 'plymouth.*(update-root|new-root|new_root)'
grep_rc=1        # no matches
```

```
$ journalctl -b -k --no-pager | grep -inE 'overlay|switch_root|switch-root'
rc=0 — 56 lines, all the same six runtime overlayfs bursts above; zero switch-root lines
```

## 2. The hook, quoted with line numbers — what `run_latehook` actually does

`/usr/lib/initcpio/hooks/btrfs-overlayfs` (owner: `limine-mkinitcpio-hook 1.40.0-2`):

```
     3	run_latehook() {
     4		root_mnt="/new_root"
     5	
     6		# Check: Is $root_mnt mounted on Btrfs?
     7		fstype=$(findmnt --mountpoint "$root_mnt" -no FSTYPE 2>/dev/null) || return 0
     8		[ "$fstype" = "btrfs" ] || return 0
     9	
    10		# Check: Does $root_mnt source path contain '/snapshot'?
    11		subvol_path=$(findmnt --mountpoint "$root_mnt" -no SOURCE 2>/dev/null) || return 0
    12		case "$subvol_path" in
    13		*/snapshot*) : ;; # ok
    14		*) return 0 ;;    # not a snapshot subvolume
    15		esac
    16	
    17		# Check: Is the subvolume read-only?
    18		ro_state=$(btrfs property get -t subvol "$root_mnt" ro 2>/dev/null) || return 0
    19		[ "$ro_state" = "ro=true" ] || return 0
```

Step by step:

1. **`hook:4`** — hardcodes `root_mnt="/new_root"`.
2. **`hook:7`** — resolves the mountpoint's FSTYPE. *Would* fail if `/new_root` did not resolve; it does resolve (§3).
3. **`hook:8`** — requires btrfs. Satisfied on this host (`fstype=btrfs`).
4. **`hook:11-15`** — requires the SOURCE to match `*/snapshot*`. **This is where the hook exits today.** `SOURCE=/dev/mapper/root[/@]` → no match → `hook:14` `return 0`.
5. **`hook:18-19`** — would require `ro=true`. Live root is `ro=false`, a second independent stopper.
6. **`hook:21`** — would echo `[OverlayFS setup] /new_root is a read-only Btrfs subvolume. Setting up OverlayFS...`. **Never emitted** (`grep -c` = 0).
7. **`hook:24-32`** — would `mktemp -d -p / lowdir_XXX` and `ramdir_XXX`.
8. **`hook:34`** — would `mount -t tmpfs cowspace "$ram_dir"`.
9. **`hook:44`** — would `mount --move "$root_mnt" "$lower_dir"`.
10. **`hook:49-51`** — would mount `overlay` on `$root_mnt`, then **`hook:56`** would echo `[OverlayFS setup] OverlayFS mounted on /new_root`.

```
$ grep -n '/new_root\|findmnt' /usr/lib/initcpio/hooks/btrfs-overlayfs
4:	root_mnt="/new_root"
7:	fstype=$(findmnt --mountpoint "$root_mnt" -no FSTYPE 2>/dev/null) || return 0
11:	subvol_path=$(findmnt --mountpoint "$root_mnt" -no SOURCE 2>/dev/null) || return 0
rc=0
```

The package's own `help()` states the design intent verbatim — **"This hook uses overlayfs to boot on a read only snapshot."** A normal `@` boot is outside that intent by construction. **This is the counter-position and it wins.**

## 3. Mechanism test — does `/new_root` resolve through the symlink?

```
$ sed -n '1208,1216p' /usr/lib/initcpio/functions | nl -ba -v1208
  1212	    install -dm755 "$buildroot/sysroot"
  1213	    ln -s "sysroot" "$buildroot/new_root"
rc=0
```

```
$ sed -n '64,72p' /usr/lib/initcpio/init | nl -ba -v64
    66	# Mount root at /sysroot
    67	"$mount_handler" /sysroot
    71	run_hookfunctions 'run_latehook' 'late hook' $LATEHOOKS
rc=0
```

So at late-hook time the real mount lives at `/sysroot`, and `/new_root` is a **relative symlink to it**. Unprivileged namespace test with the host's own `findmnt` (util-linux 2.42.4, byte-identical to the image's copy per R17 `overlay-emulation.txt:1-20`):

```
$ unshare -rm --propagation private bash -c '... mkdir -p /tmp/root/sysroot; mount -t tmpfs -o ro tmpfs /tmp/root/sysroot; ln -s sysroot /tmp/root/new_root; ...'
--- layout ---
lrwxrwxrwx 1 root root 7 Nov  3 15:40 new_root -> sysroot
drwxrwxrwt 2 root root 40 Nov  3 15:40 sysroot
--- A: findmnt --mountpoint (symlink path) ---
/tmp/root/sysroot tmpfs tmpfs
A_rc=0
--- B: findmnt --mountpoint on real path ---
/tmp/root/sysroot tmpfs tmpfs
B_rc=0
--- C: findmnt --mountpoint with trailing slash ---
/tmp/root/sysroot tmpfs tmpfs
C_rc=0
```

**`A_rc=0`.** `findmnt --mountpoint` follows the symlink. The line 7 / line 11 `|| return 0` guards **do not fire**. The r1 note's `[inf]` is wrong on this point.

Full hook body emulation (lines 21-56) through the symlink, in the same namespace:

```
=== replicate hook lines 21-56 through the symlink ===
lower_dir=/tmp/root/lowdir_5JV
ram_dir=/tmp/root/ramdir_E1H
tmpfs cowspace OK
mkdir upper/work OK
mount --move via symlink: OK
overlay mount via symlink: OK
--- result ---
TARGET            SOURCE  FSTYPE
/tmp/root/sysroot overlay overlay
OUTER_RC=0
```

Given a genuinely read-only snapshot at the target, **the hook works correctly under mkinitcpio 42.2**. The symlink is precisely the compatibility shim that was added so it would.

I additionally checked whether a correct hook run would trip `init:77` (`stat -c %D /` vs `%D /sysroot`) and dump the boot to an emergency shell. It would **not**:

```
BEFORE hook: %D /=48  %D /sysroot=5f  init:77 -> proceeds
hook:44 mount --move rc=0
hook:49 overlay mount rc=0
AFTER  hook: %D /=48  %D /sysroot=61  init:77 -> proceeds-to-switch_root
findmnt of target:
TARGET                     SOURCE  FSTYPE
<buildroot>/sysroot overlay overlay
write-through test:
write OK (overlay upper)
```

The overlay mount gives the target its own device id (`61` vs root's `48`), so the guard passes and `switch_root` proceeds. **This structural route independently confirms the hook is viable and that today's no-op cannot be attributed to the v42 path change.**

## 4. The snapshot-boot counter-position, resolved

| condition | live value | hook decision |
|---|---|---|
| `hook:7` mountpoint resolves | yes (symlink) | continue |
| `hook:8` FSTYPE | `btrfs` | continue |
| `hook:13` SOURCE matches `*/snapshot*` | `SOURCE=/dev/mapper/root[/@]` | **`hook:14` return 0** |
| `hook:19` `ro=true` | `ro=false` | return 0 |

```
$ btrfs property get -t subvol / ro
ro=false
rc=0
```

Root is a **writable** `@`, not a read-only snapshot, and not under `/snapshot`. On a normal boot the hook is a designed no-op at line 14. Overlay-on-root is **by design only during snapshot boots**, exactly as the counter-position states.

Case logic verified as pure shell semantics — only `*/snapshot*` passes:

```
SOURCE=/dev/mapper/root[/@] -> line14 return 0
SOURCE=/dev/mapper/root[/@/.snapshots/42/snapshot] -> line13 matched -> continue to ro check
SOURCE=/dev/mapper/root[/@snapshots/42/snapshot] -> line13 matched -> continue to ro check
```

The hook is configured in the late-hook phase, and the generated image carries it in `LATEHOOKS`:

```
$ grep -Hn '^HOOKS' /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d/*.conf
/etc/mkinitcpio.conf:55:HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block encrypt filesystems fsck)
/etc/mkinitcpio.conf.d/omarchy_hooks.conf:1:HOOKS=(base udev plymouth keyboard autodetect microcode modconf kms keymap consolefont encrypt filesystems fsck btrfs-overlayfs)
/etc/mkinitcpio.conf.d/omarchy_resume.conf:1:HOOKS+=(resume)
rc=0
```

```
$ for h in btrfs-overlayfs plymouth; do echo "-- $h:"; grep -oE 'run_[a-z]+hook' /usr/lib/initcpio/hooks/$h | sort -u; done
-- btrfs-overlayfs:
run_latehook
-- plymouth:
run_emergencyhook
run_latehook
```

R17's extraction of the booted UKI records `LATEHOOKS="plymouth btrfs-overlayfs"` for the 42.2 image (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:178`).

## 5. What the journal can and cannot prove — `[unk]` where earned

`grep -c 'OverlayFS setup'` = **0** is *consistent with* no overlay, but it is **not proof**, and I do not lean on it:

- The cmdline sets `quiet splash loglevel=0 systemd.show_status=false vt.global_cursor_default=0` — a deliberately silenced console.
- The journal's first line is the **kernel** banner at `2026-11-02T12:07:17`. The single initramfs-related line in the whole boot is the kernel's own `Trying to unpack rootfs image as initramfs...`; `grep -icE 'initramfs|initcpio'` = **1**. There is **no initramfs-stage (busybox-init) journal coverage at all**, so the hook's stdout was never in the journal to begin with.
- `plymouth` `grep -ic` = 13, all from `systemd[1]` about the `Show Plymouth Boot Screen` / `Terminate Plymouth Boot Screen` units — userspace unit chatter, not the initrd hook.
- `pgrep -a plymouth` → `rc=1` (no live daemon), which is expected after boot, not evidence either way.

**A missing journal line is silence, not proof.** The `h-refuted` verdict rests on the *mechanism* (§3) and the *structural reason for the no-op* (§4), both of which are positive observations — not on the absent banner.

## 6. Evidence the outcome *did* or *did not* happen — positive probes

No hook artifact survives anywhere, and each of these would have persisted across `switch_root` had lines 24-56 run:

```
$ ls -a / | grep -E 'cowspace|lowdir|ramdir'
rc=1
$ ls -d /lowdir_* /ramdir_*
ls: cannot access '/lowdir_*': No such file or directory
ls: cannot access '/ramdir_*': No such file or directory
rc=2
$ grep -c 'cowspace\|lowdir_\|ramdir_' /proc/self/mountinfo
0
rc=1
```

`hook:24`/`29` create `lowdir_*`/`ramdir_*` **on the initramfs rootfs**, and `hook:34` mounts `cowspace` there; had the hook proceeded past line 14, those mountpoints would be visible in the post-`switch_root` mount table. They are not. Combined with `findmnt -t overlay` returning zero rows and `FSROOT=/@`, the no-op outcome is established positively.

## 7. Blockers and boundaries recorded

- **`/boot` is unreadable to this seat** — `[obs]` `stat -c '%A %U:%G' /boot` → `drwx------ root:root /boot`; `ls /boot/EFI/Linux/` → `Permission denied` (rc=2). I therefore **could not re-extract the currently booted UKI** to confirm its `new_root` entry type first-hand. I did not use sudo. The 42.2 image entry type is instead carried by R17's typed extraction (`.ufo/waves/round-17/l1-capture/overlay-emulation.txt:51-66`, `boot-chain-capture.txt:169-180`), which shows `new_root -> sysroot` for every 42.2 image and a plain directory for the 41.1 image. **That is inherited evidence, not my observation — labelled as such.**
- `btrfs subvolume list /` → `ERROR: can't perform the search: Operation not permitted`; `snapper -c root list` → `No permissions.`; `ls /.snapshots` → `Permission denied`. Snapshot inventory is therefore `[unk]`, but it is **not needed**: the live `FSROOT=/@` settles which subvolume this boot used.
- Image rebuild age is corroborated from the package log rather than the unreadable ESP: `mkinitcpio 41.1-1 -> 42.2-1` and `limine-mkinitcpio-hook 1.38.0-1.1 -> 1.40.0-2` both at `2026-10-20T09:16`, while the running kernel booted `2026-11-02T12:07:17` — so the boot **post-dates** the v42 pairing, meaning v42 `init` *was* in force for the boot under test. This is what makes the test meaningful.
- No pacman transaction, no `sudo`, no systemd mutation, no boot action, no `/boot` write, no git mutation. Scratch `/fast/scratch/hyaku/tsukuroi-r64/LB1HookQ/` removed.

## 8. What this means for the round

- **The C3 "hook still hardcodes `/new_root`" finding remains factually true** as a *source* observation (`hook:4`), and the re-pins of S021/S022 are unaffected.
- **It must not be read as a live incompatibility.** Under mkinitcpio 42.2 the symlink `new_root -> sysroot` preserves the hook's lookup, and the full move+overlay sequence completes and passes `init:77`. The v42 path change does **not** break this hook.
- The r1 note's `:14` `[inf]` ("`findmnt --mountpoint` … means the missing mountpoint exits successfully before OverlayFS setup. This predicts a silent no-op") **should be marked superseded**, not merely re-dated: the premise ("missing mountpoint") is false. The already-present `## R17-SYMLINK` withdrawal covers the conclusion; this seat's contribution is the *positive mechanism demonstration* plus the identification of **`hook:14` as the real, by-design gate** for a normal `@` boot.
- Consequently the correct framing is: **`h-stands` on the outcome only.** "No overlay was set up this boot" — true, and now explained. "The `/new_root` lookup found no mountpoint" — false. The hypothesis as written is refuted.
