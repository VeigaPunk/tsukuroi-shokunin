# LB1HookQ — C3-HYPOTHESIS (labrat), round 64 wave w1

captured: 2026-11-03T18:43:21Z
verdict: **`h-refuted`** — mechanism false, outcome true, for a different reason
output: `.ufo/waves/round-64/after/labrat-hookq.md` (only file written)
host: `Linux 7.2.11-arch1-1`, `mkinitcpio 42.2-1`, boot `2026-11-02T12:07:17-03:00`
scratch: `/fast/scratch/hyaku/tsukuroi-r64/LB1HookQ/` — created, used, **removed** before yield

## Verdict in one paragraph

Hypothesis H claimed the `btrfs-overlayfs` `run_latehook` was a silent no-op **because its `/new_root` lookup found no mountpoint**. That mechanism is **false**. mkinitcpio 42.2 ships `new_root -> sysroot` as a relative symlink (`/usr/lib/initcpio/functions:1213`) next to the real mount at `/sysroot` (`init:66-67`), and `findmnt --mountpoint /new_root` **resolves through it** — my namespace test returned `A_rc=0`. The hook's line 7 and line 11 guards do not fire, and the full lines 21-56 body completes through the symlink (`mount --move` OK, overlay mount OK, target FSTYPE=`overlay`), including passing `init:77`'s device-id guard so `switch_root` still proceeds. The no-op *outcome* this boot is nonetheless real, and its actual gate is **`hook:14`** (`*) return 0 ;; # not a snapshot subvolume`), because root is `FSROOT=/@`, `subvol=/@`, `ro=false` — a normal boot, outside the hook's stated design intent ("This hook uses overlayfs to boot on a read only snapshot"). The hypothesis as written is refuted; the conclusion it aimed at is withdrawn on a different, positive basis.

## Decisive evidence

**Mechanism refuted — the single decisive line:**

```
$ unshare -rm --propagation private bash -c 'mkdir -p /tmp/root/sysroot; mount -t tmpfs -o ro tmpfs /tmp/root/sysroot; ln -s sysroot /tmp/root/new_root; findmnt --mountpoint /tmp/root/new_root -no FSTYPE; echo A_rc=$?'
/tmp/root/sysroot tmpfs tmpfs
A_rc=0
```

`findmnt --mountpoint` follows `new_root -> sysroot`. The r1 note's premise ("the missing mountpoint exits successfully before OverlayFS setup") is false.

**Outcome confirmed — the single decisive line:**

```
$ findmnt -no TARGET,SOURCE,FSROOT,OPTIONS /
/ /dev/mapper/root[/@] /@ rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@
```

`FSROOT=/@` → does not match `hook:13`'s `*/snapshot*` → `hook:14` returns 0. `ro=false` is a second independent stopper. Zero overlay mounts (`findmnt -t overlay` → header only, rc=0; `grep -c overlay /proc/mounts` → `0`, rc=1).

## Falsifier probes — all executed, none hit

| probe | result | reading |
|---|---|---|
| `journalctl -b \| grep -inE 'btrfs-overlayfs\|overlayfs'` | rc=0, 36 lines, **all ≥15:38 Nov 03** | boot was 12:07 Nov 02 — 1d3h30m earlier; **runtime, not boot-time** |
| those 36 lines' neighbours | `Starting DBus interface for snapper...`, Chromium, `ai-usage` scopes | userspace overlay mounts (container-shaped: `xattr on upper`, `userxattr`) |
| `journalctl -b \| grep -c 'OverlayFS setup'` | `0`, rc=1 | **silence, not proof** — see below |
| `findmnt -t overlay -o TARGET,SOURCE,FSTYPE,FSROOT` | header only, rc=0 | no overlay today |
| `findmnt -no FSTYPE /` | `btrfs`, rc=0 | plain btrfs |
| `cat /proc/cmdline` | contains `rootflags=subvol=@ rw rootfstype=btrfs` | normal `@` boot |
| `journalctl -b -k \| grep -inE 'overlay\|switch'` | 56 lines, all the runtime bursts; **0** switch-root lines | no boot-time overlay |
| `journalctl -b \| grep -inE 'plymouth.*(update-root\|new-root)'` | rc=1, no matches | [unk] — see silence note |
| `ls -a / \| grep -E 'cowspace\|lowdir\|ramdir'` | rc=1 | `hook:24/29/34` artifacts absent from post-`switch_root` mount table |
| `btrfs property get -t subvol / ro` | `ro=false`, rc=0 | `hook:19` would also stop |

**Silence is not proof, stated explicitly.** A zero `OverlayFS setup` count cannot settle anything here: the cmdline is `quiet splash loglevel=0 systemd.show_status=false`, and the journal has **no initramfs-stage coverage whatsoever** — `grep -icE 'initramfs|initcpio'` over the whole boot returns **1**, and that one line is the kernel's own `Trying to unpack rootfs image as initramfs...`. The hook's stdout was never in the journal to be absent from. The verdict therefore rests on the positive mechanism/structural findings, not on the missing banner.

## What `run_latehook` actually does (quoted, numbered)

`/usr/lib/initcpio/hooks/btrfs-overlayfs`, owner `limine-mkinitcpio-hook 1.40.0-2`:

```
 4	root_mnt="/new_root"
 7	fstype=$(findmnt --mountpoint "$root_mnt" -no FSTYPE 2>/dev/null) || return 0
 8	[ "$fstype" = "btrfs" ] || return 0
11	subvol_path=$(findmnt --mountpoint "$root_mnt" -no SOURCE 2>/dev/null) || return 0
12	case "$subvol_path" in
13	*/snapshot*) : ;; # ok
14	*) return 0 ;;    # not a snapshot subvolume
15	esac
18	ro_state=$(btrfs property get -t subvol "$root_mnt" ro 2>/dev/null) || return 0
19	[ "$ro_state" = "ro=true" ] || return 0
21	echo "[OverlayFS setup] ${root_mnt} is a read-only Btrfs subvolume. Setting up OverlayFS..."
24	lower_dir=$(mktemp -d -p / lowdir_XXX) ...
29	ram_dir=$(mktemp -d -p / ramdir_XXX) ...
34	mount -t tmpfs cowspace "$ram_dir" ...
44	mount --move "$root_mnt" "$lower_dir" ...
49	mount -t overlay overlay -o "lowerdir=...,upperdir=...,workdir=..." "$root_mnt" ...
56	echo "[OverlayFS setup] OverlayFS mounted on ${root_mnt}"
```

Had a mountpoint existed at the target with a `*/snapshot*` source and `ro=true`, the hook would have printed **both** `hook:21` and `hook:56` banners and left `lowdir_*`, `ramdir_*` and a `cowspace` tmpfs in the post-`switch_root` mount table. None of those exist. What the journal *would* show is precisely those two echo lines — which the silenced initramfs would not have recorded anyway.

## Counter-position tested — and it wins

Overlay-on-root is **by design only during snapshot boots**. The package's own `help()` says so verbatim: *"This hook uses overlayfs to boot on a read only snapshot."* Case semantics verified directly:

```
SOURCE=/dev/mapper/root[/@]                            -> line14 return 0
SOURCE=/dev/mapper/root[/@/.snapshots/42/snapshot]     -> line13 matched -> continue to ro check
SOURCE=/dev/mapper/root[/@snapshots/42/snapshot]       -> line13 matched -> continue to ro check
```

Configured in the late-hook phase (`omarchy_hooks.conf:1` includes `btrfs-overlayfs`; `grep -oE 'run_[a-z]+hook'` → `run_latehook` only), and R17's UKI extraction records `LATEHOOKS="plymouth btrfs-overlayfs"` at `boot-chain-capture.txt:178`.

**The test is meaningful:** `mkinitcpio 41.1-1 -> 42.2-1` and `limine-mkinitcpio-hook 1.38.0-1.1 -> 1.40.0-2` both landed `2026-10-20T09:16` (pacman.log:2539, :2852), while the running kernel booted `2026-11-02T12:07:17` — so v42 `init` *was* in force for the boot under test.

## Corrected structural check (my own first attempt was wrong)

I initially tested only `hook:44`'s `mount --move` and concluded `init:77` would fire an emergency shell (`%D /` == `%D /sysroot`). **That was incomplete and I retracted it** — the hook also mounts overlay at `hook:49`, which gives the target its own device id:

```
BEFORE hook: %D /=48  %D /sysroot=5f  init:77 -> proceeds
hook:44 mount --move rc=0
hook:49 overlay mount rc=0
AFTER  hook: %D /=48  %D /sysroot=61  init:77 -> proceeds-to-switch_root
findmnt: <buildroot>/sysroot overlay overlay
write-through test: write OK (overlay upper)
```

So the full body is sound under 42.2 and there is no structural breakage to blame. Recorded because the retracted inference would otherwise have overstated the finding.

## Blockers (recorded, not worked around)

- **`/boot` unreadable to this seat:** `stat -c '%A %U:%G' /boot` → `drwx------ root:root`; `ls /boot/EFI/Linux/` → `Permission denied` (rc=2). I could **not** re-extract the currently booted UKI to confirm its `new_root` entry type first-hand, and did not use sudo. The entry type is carried by **R17's inherited extraction** (`overlay-emulation.txt:51-66` — `new_root -> sysroot` for every 42.2 image, plain directory for 41.1), labelled as inherited, not observed.
- `btrfs subvolume list /` → `Operation not permitted`; `snapper -c root list` → `No permissions.`; `ls /.snapshots` → `Permission denied`. Snapshot inventory `[unk]` — but not needed, since `FSROOT=/@` settles which subvolume this boot used.
- No pacman transaction, no sudo, no systemd/boot mutation, no `/boot` write, no git mutation.

## Impact on the frozen claims

- C3's **source** observation "the installed hook still hardcodes `/new_root` (`hook:4`)" stays **factually true**; the S021/S022 re-pins are unaffected.
- It must **not** be framed as a live v42 incompatibility: the `new_root -> sysroot` symlink preserves the lookup, and the complete body succeeds.
- The r1 note's `:14` `[inf]` should be marked **superseded**, not re-dated — its premise ("missing mountpoint") is false. Using my result plus the existing `## R17-SYMLINK` withdrawal, the defensible statement is: **no overlay this boot, by design at `hook:14`, on a normal `@` boot — not because of the `/sysroot` transition.**

## Files changed

- `.ufo/waves/round-64/after/labrat-hookq.md` (created — full receipts, verbatim commands/outputs/rc)
- `.ufo/waves/round-64/w1/LB1HookQ.md` (this report)

No other file written. Nothing committed. Scratch dir removed.
