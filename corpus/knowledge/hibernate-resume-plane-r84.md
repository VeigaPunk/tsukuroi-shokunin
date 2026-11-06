# Hibernate-resume plane (round 84)

verified-at: 2026-11-06
host capture: `.ufo/waves/round-84/before/host/receipt.txt` (2026-11-06T15:44:21-03:00, `tools/capture-resume-facts-r84.py`, read-only)
machine-readable rows: `corpus/knowledge/hibernate-resume-plane-r84.json` (counted by `tools/count-resume-rows-r84.py`)
gate: `tools/check-hibernate-resume.py --live` (HEALTHY rc 0 / DEGRADED rc 1 / CANNOT-EVALUATE rc 2)

## What this plane answers

Will this host come back from hibernation to the image it wrote? The chain has five links: the kernel
command line names the resume device and, for a swap file, the offset of its swap header; on btrfs that
offset comes from `btrfs inspect-internal map-swapfile -r`, not from `filefrag`; the swap file must be NOCOW
and active; the initramfs hands device and offset to the kernel through `/sys/power/resume` and
`/sys/power/resume_offset`; and free swap must hold an image of up to `/sys/power/image_size` bytes. A break
in any link is silent until the first resume attempt: the kernel boots fresh and the image is lost.

Line numbers below are raw lines of the pinned upstream snapshot (QUALITY 113), not host-build lines: the
host runs Arch builds of kernel 7.2.11, btrfs-progs 7.1, systemd 262.1 and mkinitcpio 42.2 (QUALITY 103).
The mkinitcpio `hooks/resume` and `install/resume` files are byte-identical to the host's
`/usr/lib/initcpio/{hooks,install}/resume` (`diff` empty, 2026-11-06).

## Rows

| Row | Rule (source, raw lines) | Host value (receipt line) | Status |
|---|---|---|---|
| HR1 | `resume_offset=` is the swap header's place inside the `resume=` partition, in PAGE_SIZE units, needed only for swap files (S336 kernel-parameters.txt v7.2 :6581-6582) | `resume_offset=3795013` on the cmdline (:4) | holds |
| HR2 | on btrfs, `map-swapfile` prints the page-adjusted resume offset (S337 ch-swapfile.rst v7.1 :127) | `map-swapfile -r` → `3795013` (:13), equal to HR1 | holds |
| HR3 | the resume offset is the device physical offset, not what `filefrag` prints (S337 :118) | `filefrag -v` first extent physical `3530821` (:24) ≠ 3795013 | trap measured: a filefrag-derived offset would be wrong here |
| HR4 | a btrfs swap file must be NODATACOW (no checksums, no compression) (S337 :13) | `lsattr` → `---------------C------` (:17) | holds |
| HR5 | the swap file must be active, present in `/proc/swaps` (S338 swsusp-and-swap-files.rst :57-58) | `/swap/swapfile file 31722876` (:9) | holds at capture |
| HR6 | a recreated swap file may move its header; `resume_offset` must be re-derived (S338 :61) | birth `1791060333` = 2026-10-03 17:45:33 -03 (:32) | recheck trigger: a different birth time |
| HR7 | `systemd-hibernate-resume` writes the device's major:minor to `/sys/power/resume` (S339 :38) | `/sys/power/resume` → `253:0` (:40) = `/dev/mapper/root` (`fd 0`, :36) | holds |
| HR8 | `/sys/power/resume_offset` overrides the cmdline offset (S340 sysfs-power :307-308) | `3795013` (:44), equal to HR1 and HR2 | holds |
| HR9 | mkinitcpio's resume install hook adds `systemd-hibernate-resume` when systemd ≥ 255 (S341 install/resume v42.2 :11-12) | `systemd 262` (:79); the booted UKI initramfs carries the binary (`.ufo/waves/round-84/after/uki-initrd-contents.txt`, UKI sha256 `12a52286…001a`) | holds for the image; this host's HOOKS are busybox-style (`base udev … encrypt … resume`, receipt :60-75), so its `resume` run hook hands off to the binary; which writer set `/sys/power/resume` this boot is not shown |
| HR10 | `image_size` is an upper limit, in bytes, on the image (S340 :97-98) | `12835467264` (:56) against (31722876 − 11942400) KiB ≈ 20.3 GB free swap | holds; headroom shrinks as swap use grows |

## Operator actions

- After recreating or resizing `/swap/swapfile`: run `sudo btrfs inspect-internal map-swapfile -r /swap/swapfile`
  and put that number, never a `filefrag` number, in `resume_offset=` (HR2, HR3, HR6); then regenerate the boot
  entries the way this host already does (limine/mkinitcpio hooks) — a state-changing action, update-safety gate first.
- Before hibernating under swap pressure: compare free swap with `/sys/power/image_size` (HR10); the gate's
  `HR-SWAP-TOO-SMALL` finding reads the same numbers.
- `HOOKS` order: `resume` must run after `encrypt` (the resume device is inside the LUKS volume). This host
  appends `resume` last via `/etc/mkinitcpio.conf.d/omarchy_resume.conf` (receipt :71/:75: `encrypt` before
  `resume`), which satisfies it; the gate flags the reverse as `HR-HOOK-BEFORE-ENCRYPT`.

- Where the offset lives (added at landing from `.ufo/waves/round-84/w1/ScoutHost.md` §3i, read-only):
  five `cmdline:` lines in `/boot/limine.conf` (two kernels, three snapshot entries), five in
  `/boot/limine.conf.old`, and the `.cmdline` section of each UKI, which holds the `resume=`/`resume_offset=`
  pair twice. Limine's line supplied the booted cmdline. A recreated swap file needs every live copy
  updated; a stale copy in a snapshot entry or a UKI fails silently. The gate reads only `/proc/cmdline`
  and takes the last occurrence, so it would not see a divergence between duplicate copies.

## Limits

- Read-only plane: nothing here hibernated the host; no resume was exercised. "Holds" means the configured
  values agree with each other and with the sources, not that a resume succeeded. The journal shows no
  hibernation entry or exit in the retained boots (`journal-boot-plane.md:251-252`).
- HR7 reads the value the kernel holds; it does not show which writer (kernel `resume=` parsing or the
  initramfs binary) set it.
- Negative-state recheck (QUALITY 109): `tools/check-hibernate-resume.py --live`, cadence 30d and on any
  swap-file, kernel-cmdline or mkinitcpio change.

## Review record

Non-author per-row review: `.ufo/waves/round-84/w1/ReviewEntry.md` and `ReviewEntry/verdict.json` (seat
ReviewEntry, 8 supports, 2 partial, 0 does-not-support, claim `unprovable-but-better`) on the text at
`c6ee78b2`. The two partials were reworded at landing: HR4 no longer asserts a mount option the receipt does
not capture; HR9 no longer asserts which writer set `/sys/power/resume`. The reviewer's further remark that
this initramfs is systemd-based is not adopted: the effective HOOKS (receipt :60-75) carry `base`, `udev` and
`encrypt` and no `systemd` hook.
