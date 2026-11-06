# ScoutHost — round 84, wave w1

Seat: ScoutHost (read-only host re-capture + missing-precondition scan for the hibernate-resume plane).
Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` →

```
f19e73f3aa9817e76044e4e43a343c6ca6d929df
```

(`master` tip at the time of this seat; the C1 re-declaration commit named in the seat brief
`69915b8603d9e443f2e1c0021d7c34509186bd9e` is its parent; `master` has since gained
`c6941adb` and `f19e73f3` — registry-row repairs only, no change to the gate, the entry or the
instruments.) The working tree is **dirty**: `git status --porcelain` lists
`corpus/QUALITY.md`, `corpus/knowledge/hibernate-resume-plane-r84.json`,
`corpus/knowledge/hibernate-resume-plane-r84.md`, `corpus/lessons/round-84.md`,
`tools/check-hibernate-resume.py` as modified (the `failed_probes` fail-closed change in the gate and
its two row-text edits). I edited nothing.

Tooling: no tool was installed or upgraded by this seat (no `pacman`, no `uv tool install`);
everything below used preinstalled `python3` (3.14.8), `git`, `btrfs-progs` 7.1, `systemd` 262.1-1,
`mkinitcpio` 42.2, `objcopy`/`lsinitcpio` (binutils), `dd`, `od`, `strings`, `curl` (upstream source
reads only, no writes).

Host guard observed: nothing was hibernated, suspended, swapped on/off, written under `/sys` or
`/proc`, no sysctl touched, no `/boot` write, no `mkinitcpio`/`limine`/`pacman` run. `sudo -n` was used
only for read-only inspection: `btrfs inspect-internal map-swapfile`, `lsattr`, `filefrag -v`,
`stat`/`ls` of root-owned paths, `objcopy`/`objdump` of the UKI (read-only extraction to scratch),
`cat` of `/etc/mkinitcpio.conf*`, `/etc/fstab`, `/etc/crypttab`, `/boot/limine.conf`, `/proc/1/mountinfo`.

---

## 1. Independent host re-capture and diff against the pinned host base

### 1a. Fresh capture (read-only)

```
$ python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/capture-resume-facts-r84.py --out $S/cap
```
exit `0`; stdout is the facts document (`captured_at: 2026-11-06T15:56:36-03:00`).
Produced `facts.json` (sha256 `1892e6d61caf6119cb930e0eb3a4924ac4cd4f89a6e8e48e5d4e36e5f7b5a738`) and
`receipt.txt` (sha256 `9a475afaf4b1662efee9b99d772b3b06498214ae9f24760027d3ce25ab2c6731`).
The receipt is copied to `.ufo/waves/round-84/w1/ScoutHost/receipt.txt` (same sha256).

### 1b. Field-by-field diff vs `.ufo/waves/round-84/before/host/facts.json`

```
$ diff -u .ufo/waves/round-84/before/host/facts.json $S/cap/facts.json
--- .../before/host/facts.json   2026-11-06 15:44:21.196454427 -0300
+++ $S/cap/facts.json            2026-11-06 15:56:36.483507058 -0300
@@ -1,5 +1,5 @@
 {
- "captured_at": "2026-11-06T15:44:21-03:00",
+ "captured_at": "2026-11-06T15:56:36-03:00",
   "cmdline": "resume=/dev/mapper/root resume_offset=3795013 quiet splash ... rootfstype=btrfs",
@@ -30,7 +30,7 @@
    "path": "/swap/swapfile",
    "size_kib": 31722876,
-   "used_kib": 11942400
+   "used_kib": 14457648
   }
  ],
```
exit `1` (differences present). **Exactly two fields differ.**

| field | pinned (15:44:21) | fresh (15:56:36) | explanation |
|---|---|---|---|
| `captured_at` | 2026-11-06T15:44:21-03:00 | 2026-11-06T15:56:36-03:00 | capture timestamp; not a fact about the host. |
| `swaps[0].used_kib` | 11 942 400 | 14 457 648 | **expected swap-use drift.** The pinned base was captured at a different minute; the host is under real memory pressure (below). Independently measured: `/proc/meminfo` `SwapFree` moved between 15 043 760 kB and 18 396 972 kB inside a ~90-minute window of ordinary host activity, and `swapon --show --bytes` reported `USED 13 751 808 000` (= 13 115 940 KiB) at one sample and 13 764 052 KiB at another. No `swapon`/`swapoff` was issued by this seat. |

**Every other field is byte-identical** and therefore still holds on the live host 12 minutes after the
pinned capture: `cmdline`, `hooks` (16 entries, `resume` last), `image_size` 12835467264,
`map_swapfile_offset` 3795013, `resume_dev_majmin` "253:0", `resume_swapfile` "/swap/swapfile",
`swapfile_attrs` "---------------C------", `sys_power_disk`
"[platform] shutdown reboot suspend test_resume", `sys_power_resume` "253:0",
`sys_power_resume_offset` 3795013, `sys_power_state` "freeze mem disk", `schema` "resume-facts/1",
`swaps[0].path` "/swap/swapfile", `swaps[0].size_kib` 31722876, `swaps[0].type` "file".

Independent check that the pinned manifest still matches the pinned inputs (read-only):
`sha256sum -c .ufo/waves/round-84/before/host/SHA256SUMS` → both `receipt.txt` and `facts.json` OK;
`sha256sum -c .ufo/waves/round-84/before/src/SHA256SUMS` → all 8 snapshots `OK`.

### 1c. Instrument digests re-verified against the frozen declaration

```
$ sha256sum tools/count-resume-rows-r84.py tools/resume-gate-battery-r84.py tools/capture-resume-facts-r84.py
cb70d4357ebe2d50f360dbbc2079f3a35756a79fc785280cf9d4312268ac8309  tools/count-resume-rows-r84.py
00310ac205f07f396bc4a7a0406f1c0d4baf74c7ab30e27245bbc89d8ce00964  tools/resume-gate-battery-r84.py
cec27b9d19e4ac85ccaa513b94e37f568b51979c546133c3d4bc5f62cd6cea23  tools/capture-resume-facts-r84.py
```
All three are **byte-equal to the frozen values** in the declaration block of the frozen
`SCORECARD.md` (`git show 69915b8603d9e443f2e1c0021d7c34509186bd9e:SCORECARD.md`), checked
programmatically:

```
count-resume-rows    frozen cb70d4357ebe2d50f360dbbc2079f3a35756a79fc785280cf9d4312268ac8309  actual cb70d4357ebe2d50f360dbbc2079f3a35756a79fc785280cf9d4312268ac8309  MATCH
resume-gate-battery  frozen 00310ac205f07f396bc4a7a0406f1c0d4baf74c7ab30e27245bbc89d8ce00964  actual 00310ac205f07f396bc4a7a0406f1c0d4baf74c7ab30e27245bbc89d8ce00964  MATCH
capture-resume-facts frozen cec27b9d19e4ac85ccaa513b94e37f568b51979c546133c3d4bc5f62cd6cea23  actual cec27b9d19e4ac85ccaa513b94e37f568b51979c546133c3d4bc5f62cd6cea23  MATCH
host manifest file   sha256 4ca3e20939eadff71c190f5e2d27a5f453479d0133321ebd118eb7eef624fde6  (declaration's manifest sha256) MATCH
src  manifest file   sha256 5d1673de7f893f035cb2808e9579bcdd292339a32dad605c6e3a53d6561f7eef  (declaration's manifest sha256) MATCH
```
No instrument or pinned input drifted.

---

## 2. Independent re-derivation (no capture script), and whether each HR1–HR10 host value still holds

All commands below were run by hand; none used `capture-resume-facts-r84.py`.

```
$ cat /proc/cmdline
resume=/dev/mapper/root resume_offset=3795013 quiet splash loglevel=0 systemd.show_status=false rd.udev.log_level=0 vt.global_cursor_default=0 cryptdevice=PARTUUID=cf3d875f-72a4-4468-9795-015c9e953618:root:allow-discards,no-read-workqueue,no-write-workqueue root=/dev/mapper/root zswap.enabled=1 zswap.max_pool_percent=25 rootflags=subvol=@ rw rootfstype=btrfs
```

```
$ sudo -n btrfs inspect-internal map-swapfile -r /swap/swapfile
3795013
(exit 0)

$ sudo -n btrfs inspect-internal map-swapfile /swap/swapfile
Physical start:  15544373248
Resume offset:       3795013
(exit 0)
```
`15544373248 / 4096 = 3795013` exactly — the `-r` value is the byte-physical start divided by
PAGE_SIZE, i.e. the kernel's `resume_offset` unit (pinned source S336, kernel-parameters.txt:6579-6583,
"in <PAGE_SIZE> units (needed only for swap files)").

```
$ cat /sys/power/resume /sys/power/resume_offset /sys/power/state /sys/power/disk /sys/power/image_size
253:0
3795013
freeze mem disk
[platform] shutdown reboot suspend test_resume
12835467264
```

```
$ stat -L -c '%t %T' /dev/mapper/root
fd 0
```
`fd`=253, `0`=0 → 253:0, equal to `/sys/power/resume`.

```
$ sudo -n lsattr /swap/swapfile
---------------C------ /swap/swapfile
```

Effective mkinitcpio HOOKS (sourced by hand from `/etc/mkinitcpio.conf` + `/etc/mkinitcpio.conf.d/*.conf`,
same order the capture script uses): `base udev plymouth keyboard autodetect microcode modconf kms keymap
consolefont block encrypt filesystems fsck btrfs-overlayfs resume` — `encrypt` at position 12, `resume`
last (position 16). `/etc/mkinitcpio.conf.d/omarchy_resume.conf` is exactly `HOOKS+=(resume)`;
`omarchy_hooks.conf` is `HOOKS=(base udev plymouth keyboard autodetect microcode modconf kms keymap
consolefont block encrypt filesystems fsck btrfs-overlayfs)`.

**New byte-level check the plane and the gate do not perform.** The resume offset was verified against
the *bytes on the resume device*, not by comparing two numbers:

```
$ sudo -n dd if=/dev/mapper/root bs=4096 skip=3795013 count=1 2>/dev/null | dd bs=1 skip=4086 count=10 | od -An -c
   S   W   A   P   S   P   A   C   E   2
$ sudo -n dd if=/swap/swapfile bs=1 skip=4086 count=10 | od -An -c
   S   W   A   P   S   P   A   C   E   2
$ cmp <(sudo -n dd if=/dev/mapper/root bs=4096 skip=3795013 count=1 2>/dev/null) \
       <(sudo -n dd if=/swap/swapfile bs=4096 count=1 2>/dev/null) && echo IDENTICAL
IDENTICAL
$ sha256sum (both 4096-byte pages)
c5130e1893438922b381eef9caac49fac38e1b29726eb070aa93dea10688a721  <physical page at resume offset>
c5130e1893438922b381eef9caac49fac38e1b29726eb070aa93dea10688a721  </swap/swapfile page 0>
```
So the device page addressed by `resume_offset=3795013` on the resume device `/dev/mapper/root` is
**byte-identical to page 0 of `/swap/swapfile`** and carries the swap-space signature
`SWAPSPACE2` at intra-page offset 4086 (= PAGE_SIZE − 10). The same UUID appears in the header
(`swaplabel /swap/swapfile` → `UUID: 6d22e065-aa2a-4e4a-bee4-1ae319e5df12`, matching the bytes at file
offset 1036), and the header's version field reads `01 00 00 00` at file offset 1024.
The `filefrag` candidate was tested the same way and does **not** hold the header:
at byte 3530821 × 4096 = 14 462 242 816 the device returns unrelated bytes
(`336 L 017 B 336 I 213 016 L 211`), no `SWAPSPACE2`.

### Verdict per row (does the pinned host value still hold?)

| row | pinned host value | re-derived now | holds? |
|---|---|---|---|
| HR1 | `resume_offset=3795013` on cmdline (receipt :4) | present exactly once in the effective `/proc/cmdline` | **holds** |
| HR2 | `map-swapfile -r` → `3795013` (receipt :13) | `3795013`; long form `Physical start: 15544373248` (= ×4096) | **holds** (now also byte-verified: the header page) |
| HR3 | `filefrag` first extent physical `3530821` ≠ resume offset (receipt :24) | unchanged; byte-check confirms the filefrag number does **not** address the header page | **holds** (trap re-confirmed at byte level) |
| HR4 | `lsattr` → `---------------C------` (receipt :17) | identical | **holds** |
| HR5 | `/proc/swaps` lists `/swap/swapfile file 31722876` (receipt :9) | listed, type `file`, size 31722876 KiB; `used_kib` now 13 764 052–14 457 648 (drift, see §1b) | **holds** (activity and identity) |
| HR6 | birth `1791060333` = 2026-10-03 17:45:33 -03 (receipt :32) | `stat` still `1791060333 257 32484229120`; `date -d @1791060333` → `Sat 03 Oct 2026 05:45:33 PM -03` | **holds** (file not recreated) |
| HR7 | `/sys/power/resume` → `253:0` = `/dev/mapper/root` (receipt :40, :36) | `253:0`; `stat -L` gives `fd 0` | **holds** |
| HR8 | `/sys/power/resume_offset` → `3795013` (receipt :44) | `3795013` | **holds** |
| HR9 | systemd 262 (receipt :79); booted UKI initrd carries `usr/lib/systemd/systemd-hibernate-resume` | re-extracted the UKI's `.initrd` myself: `objcopy --only-section=.initrd` → initrd sha256 `279d492ee9b23d38744546b14031f10a5642c4160030d5d5c8043f0639f014a2` (equal to the committed `.ufo/waves/round-84/after/uki-initrd-contents.txt` value), `lsinitcpio` lists `hooks/encrypt`, `hooks/resume`, `usr/lib/systemd/systemd-hibernate-resume`; the initrd also carries `etc/initrd-release` (the `AssertPathExists=` that `systemd-hibernate-resume.service` requires) and `etc/fstab` | **holds** |
| HR10 | `image_size` = `12835467264` (receipt :56) vs free swap | `12835467264`; free swap at capture 19 780 476 KiB ≥ 12 534 636 KiB (= image_size in KiB) → holds; **live free swap has fallen to 17 234 228–18 396 972 KiB** and is volatile | **holds**, with the headroom shrinking (see §3d) |

Instrument runs (independent of the candidate's own evidence):

```
$ python3 tools/resume-gate-battery-r84.py --gate tools/check-hibernate-resume.py     # working-tree gate
EXIT=0   verdict met, families_passed 13, families_total 13, failed_families [],
         bases [host, random0..random4]

$ python3 tools/resume-gate-battery-r84.py --gate $S/tools/check-hibernate-resume.py  # gate as committed at master
EXIT=0   verdict met, families_passed 13, families_total 13, failed_families [],
         bases [host, random0..random4]

$ python3 tools/check-hibernate-resume.py --live
{"findings": [], "verdict": "HEALTHY"}   rc=0     (committed master gate; worktree gate identical result)

$ python3 tools/count-resume-rows-r84.py --revision master
"verdict": "met", "counted": 10, "failed": 0, "distinct_snapshots": 6   EXIT=0
```
The C1 counter is a shape/provenance gate by the L1's own declaration (the frozen positive control P1
is a random-span junk entry that also reads `met`), so its `met` is not evidence that any row is
*true*. I therefore re-checked all ten rows by hand against the pinned snapshots: every `source.quote`
is present in the cited raw span (HR1 spans the line break at kernel-parameters.txt:6581-6582 and
matches after whitespace normalisation, exactly as the counter normalises it), and every `host.value` is
present in the cited receipt span (HR5's value uses single spaces where the receipt has tabs — the
counter normalises whitespace, so it passes; the raw receipt line is tab-separated). No row fails on
its own terms.

---

## 3. Missing-precondition scan: what the plane and the gate do not read

Each item below is a read-only measurement with its output. **These are frontier candidates, not
claims**; none of them is a measured defect in the round-84 instruments.

### 3a. Kernel lockdown — holds (does not block hibernation)

```
$ cat /sys/kernel/security/lockdown
[none] integrity confidentiality
```
Current mode is `none` (the two other modes are selectable). No lockdown is enforced, so nothing here
blocks `/sys/power/resume*` writes or the resume path. Not a precondition the plane or gate reads.

### 3b. Secure Boot / measured boot — not applicable to the resume chain

```
$ bootctl status | head
      Firmware: UEFI 2.110 (American Megatrends 5.41)
   Secure Boot: disabled
  TPM2 Support: no
   Measured UKI: no
```
Secure Boot is off and there is no TPM2; the UKI carries no signature section
(`objdump -h` on `/boot/EFI/Linux/omarchy_linux.efi` shows `.text .rodata .data .sbat .sdmagic .reloc
.uname .osrel` and no `.pcrsig`). This bears on module/UKI trust, not on the resume chain: nothing
about `resume=`/`resume_offset=` depends on it. There is **no EFI `HibernateLocation` variable** on this
host (`ls /sys/firmware/efi/efivars | grep -i hibernate` → empty), so systemd's hibernation path will
use the kernel-command-line `resume=` (the `HibernateLocation-…` variable the journal keeps reporting
as absent), i.e. the cmdline is the only resume-location carrier.

### 3c. NVIDIA suspend/hibernate units, `PreserveVideoMemoryAllocations`, and session freezing — **the strongest gap**

```
$ systemctl is-enabled nvidia-hibernate.service nvidia-resume.service
disabled
disabled
$ systemctl show nvidia-hibernate.service -p WantedBy -p UnitFileState
WantedBy=
UnitFileState=disabled
$ ls -la /etc/systemd/system/systemd-hibernate.service.wants/
ls: cannot access '...': No such file or directory
$ cat /proc/driver/nvidia/params | grep -i PreserveVideoMemoryAllocations
PreserveVideoMemoryAllocations: 1
$ ls /proc/driver/nvidia/suspend
ls: cannot access '/proc/driver/nvidia/suspend': No such file or directory
$ systemctl show systemd-hibernate.service -p Environment
Environment=SYSTEMD_SLEEP_FREEZE_USER_SESSIONS=false
$ cat /usr/lib/systemd/system/systemd-hibernate.service.d/10-nvidia-no-freeze-session.conf
[Service]
Environment="SYSTEMD_SLEEP_FREEZE_USER_SESSIONS=false"
```

Facts: (i) the NVIDIA hibernate/resume helper units are **disabled and not wired into
`systemd-hibernate.service`** (`WantedBy=` empty, no `.wants` directory) — on this host
`nvidia-sleep.sh` would also be inert even if invoked, because `/proc/driver/nvidia/suspend` does not
exist in this open-kernel-module build (`nvidia-sleep.sh` exits 0 early when that file is absent);
(ii) VRAM preservation therefore rests on the driver's own
`NVreg_PreserveVideoMemoryAllocations=1`, which is set; (iii) **`systemd-hibernate.service` carries a
drop-in that sets `SYSTEMD_SLEEP_FREEZE_USER_SESSIONS=false`**, i.e. user sessions are *not* frozen
before a hibernation write. A hibernation image taken with unfrozen sessions can capture
inconsistent application/filesystem state, and neither the plane nor the gate reads this. This is the
single most consequential precondition the round-84 plane misses. It is also *not* a resume-chain
break — it is an image-consistency hazard that would only manifest after a real hibernate.

### 3d. zswap ↔ hibernation, and the erosion of the free-swap headroom — candidate

```
$ cat /sys/module/zswap/parameters/enabled /sys/module/zswap/parameters/max_pool_percent /sys/module/zswap/parameters/compressor
Y
25
zstd
$ grep -E 'SwapTotal|SwapFree|Zswap|Zswapped' /proc/meminfo
SwapTotal:      31722876 kB
SwapFree:      18396972 kB
Zswap:            349984 kB
Zswapped:        1293728 kB
$ cat /proc/pressure/memory
some avg10=0.34 avg60=0.93 avg300=1.05 total=1247373126
full  avg10=0.34 avg60=0.90 avg300=1.01 total=1174786306
```
zswap is on (cmdline `zswap.enabled=1 zswap.max_pool_percent=25`), holding 1.3–2.1 GiB of swap content
compressed in RAM at capture time. The plane and the gate read neither zswap nor the pressure
counters. Two consequences worth an operator's eye, neither of which I can settle read-only:
(i) with zswap in the path, `/proc/swaps` "Used" counts pages whose bodies still live in RAM, so the
gate's free-swap arithmetic (`sum((size_kib-used_kib)*1024)`) is a *device-free-space* proxy that
includes not-yet-written-back zswap content — I measured the gate's number to agree exactly with
`/proc/meminfo SwapFree` (delta 0 kB), so today the two are the same quantity;
(ii) **the free-swap margin is eroding under live load**: `used_kib` was 11 942 400 at the pinned
capture (15:44) and 14 457 648 twelve minutes later (15:56), i.e. free swap fell from ~19.8 GiB to
~17.2 GiB in twelve minutes of ordinary host activity; the gate's `HR-SWAP-TOO-SMALL` threshold is
`used_kib > 19 188 240`, so roughly 4.7–5.4 GiB of further swap growth would make the gate report
DEGRADED, and the .md's HR10 figure ("≈ 20.3 GB free swap") is a capture-time number that no longer
describes the host. That is a freshness statement about the plane's own table, not a defect in it.

### 3e. systemd sleep configuration (`HibernateMode=`, `HibernateDelaySec=`) — defaults apply and are satisfiable

```
$ cat /etc/systemd/sleep.conf
[Sleep]                     # only the section header; every setting is commented out
$ ls -la /etc/systemd/sleep.conf.d/ 2>&1
ls: cannot access '/etc/systemd/sleep.conf.d/': No such file or directory
$ systemd-analyze cat-config systemd/sleep.conf
[Sleep]
```
No local override exists. Upstream systemd v262 defaults (`src/shared/sleep-config.c`):
`SLEEP_HIBERNATE` state = `{"disk"}`, modes = `{"platform","shutdown"}`. On this host
`/sys/power/disk` = `[platform] shutdown reboot suspend test_resume`, so `platform` **is** offered
and is the currently selected mode, and `/sys/power/state` offers `disk`. The hibernate write path is
therefore serviceable as configured; the plane does not read `/sys/power/disk` or the sleep config.
`HibernateDelaySec` (default 2 h when there is no battery) is inert here: this machine has **no
battery** (`/sys/class/power_supply/` is empty, `upower -e` lists only a DisplayDevice), so the
no-battery branch applies and AC-only hibernation is permitted (`HibernateOnACPower` default true).

### 3f. Swap priority, multiple swap areas, and zram — one area only; an older corpus row is stale

```
$ swapon --show
NAME           TYPE        SIZE        USED PRIO
/swap/swapfile file 30.3G  13.6G    0
$ ls /dev/zram*
ls: cannot access '/dev/zram*': No such file or directory
$ lsmod | grep -i zram        # (no output; zram module not loaded)
$ systemctl list-units --type=swap --all
  UNIT                   LOAD   ACTIVE SUB     DESCRIPTION
  swap-swapfile.swap loaded active active /swap/swapfile
```
Exactly one swap area (file, priority 0), activated by `systemd-fstab-generator` from
`/etc/fstab` (`/swap/swapfile none swap defaults,pri=0 0 0`). **No zram device exists on this host
now**, while `corpus/knowledge/kill-event-deep-r8.md:259` and `corpus/knowledge/oom-event-plane.md:348`
still present `/dev/zram0` 4 G (prio 100) as current-use swap capacity, and the R18 freshness notice
set (`corpus/knowledge/freshness-recheck-r18.json`, notice on oom-event-plane.md:348) refreshed the
zswap clause of that same row but left the zram clause unrefreshed. This is a **freshness observation
about adjacent corpus rows, outside the round-84 claim set**; I did not edit those files and I put a
proposed patch under my own wave directory (§4).

### 3g. `noresume` / `hibernate=` / `nohibernate` — absent, so hibernation is not disabled

```
$ tr ' ' '\n' < /proc/cmdline | grep -iE 'noresume|hibernate|nohibernate|cryptkey|resumewait|resumedelay|mem_sleep|resume'
resume=/dev/mapper/root
resume_offset=3795013
```
(the full effective cmdline is the 15 tokens printed in §2). None of `noresume`, `hibernate=no`,
`nohibernate`, `resumewait`, `resumedelay` is present, so the kernel's `__setup("noresume")` /
`hibernate_setup()` paths do not disable the resume attempt. `nohibernate` and `hibernate=no` are
documented in the pinned kernel-parameters snapshot (S336) — a reader of the plane cannot see that
these tokens exist at all.

### 3h. logind `HandleLidSwitch` and power-key policy — defaults, and no battery to act on

```
$ grep -vE '^\s*(#|$)' /etc/logind.conf
[Login]
HandlePowerKey=ignore
$ systemd-analyze cat-config systemd/logind.conf | grep -iE 'HandleLidSwitch|HandlePowerKey'
HandlePowerKey=ignore
#HandleLidSwitch=suspend
#HandleLidSwitchExternalPower=suspend
#HandleLidSwitchDocked=ignore
```
`HandleLidSwitch` is left at the default `suspend` (logind.conf(5)); `HandlePowerKey=ignore` is set
locally; `HandleLidSwitchExternalPower`/`Docked` are at defaults (`suspend`/`ignore`). With no battery
present, none of these can trigger a hibernation on this host; the only hibernate trigger is an
explicit `systemctl hibernate`. Note that `systemd-hibernate.service` in turn refuses without a usable
resume location (`systemd-sleep` carries the string `No valid 'resume=' option found, refusing to
hibernate.`) — this host does have `resume=` on the cmdline, so that refusal does not apply.

### 3i. Where the resume offset actually lives (operator-action precision) — candidate

```
$ sudo -n grep -o 'resume_offset=[0-9]*' /boot/limine.conf | sort | uniq -c
      5 resume_offset=3795013
$ sudo -n grep -c 'cmdline:' /boot/limine.conf
5
$ sudo -n grep -o 'resume_offset=[0-9]*' /boot/limine.conf.old | sort | uniq -c
      5 resume_offset=3795013
$ for u in /boot/EFI/Linux/omarchy_linux.efi /boot/EFI/Linux/omarchy_linux-lts.efi; do
    sudo -n objcopy -O binary --only-section=.cmdline "$u" - | tr ' ' '\n' | grep -cE '^resume_offset=3795013$'; done
2
2
$ sudo -n objcopy -O binary --only-section=.cmdline /boot/EFI/Linux/omarchy_linux.efi - | tr ' ' '\n' | grep -nE 'resume'
resume=/dev/mapper/root
resume_offset=3795013
… (14 more tokens) …
resume=/dev/mapper/root
resume_offset=3795013
```
Two things the plane's operator-action section does not say. First, **seven boot-config sites carry the
offset**: five `cmdline:` lines in `/boot/limine.conf` (two live kernels + three snapper-snapshot
entries), five in the retained `/boot/limine.conf.old`, and the `.cmdline` section of each of the two
UKIs. Second, **each UKI's `.cmdline` section contains `resume=`/`resume_offset=` twice** (18 tokens
against the 15 that actually reached the kernel): this host boots through Limine, whose `cmdline:`
line supplied the effective 15 tokens (`md5` of the token lists of `/proc/cmdline` and of limine.conf:31
are equal: `4a511cd62a321de5c5b0a9753d53abc1`), so the UKI's duplicated pair is inert here — but a
future loader that prefers the UKI's own `.cmdline` would see the pair twice. The gate's `arg()`
helper takes the *last* occurrence, which is harmless while both copies are equal, and would silently
mask a divergence between the two copies. Concretely: **the operator action should say "update the
five limine.conf cmdline lines and both UKI .cmdline sections (each of which holds the pair twice)",
not just "regenerate the boot entries"** — otherwise a stale offset survives in a snapshot entry or in
one of the two UKI copies and the failure is silent.

### 3j. Snapshot roots: the swap file is absent from them — candidate

```
$ sudo -n btrfs subvolume show /swap
Name: 			swap
Subvolume ID: 		262      Parent ID: 256 (@)      Creation time: 2026-10-03 17:45:33 -0300
$ sudo -n btrfs subvolume list /
… ID 262 … path swap ; ID 263 path .snapshots ; ID 264 path .snapshots/1/snapshot ; ID 266 path .snapshots/2/snapshot …
$ sudo -n ls -A /.snapshots/2/snapshot/swap/ | wc -l
0
$ sudo -n grep -E 'swap' /.snapshots/2/snapshot/etc/fstab
/swap/swapfile none swap defaults,pri=0 0 0
```
The active swap file lives in its **own btrfs subvolume** `@/swap` (id 262), not in `@`. That is
what keeps the root snapshotting legal: the pinned source states `subvolume - cannot be snapshotted if
it contains any active swapfiles` (S337 ch-swapfile.rst:11), and the snapshot roots indeed contain an
**empty** `swap/` directory while their `etc/fstab` still references `/swap/swapfile`. The three
snapshot boot entries in `/boot/limine.conf` (lines 51, 57, 65) carry the same `resume_offset=3795013`
with `rootflags=subvol=/@/.snapshots/N/snapshot`. Measured facts only: in such a root there is no
swap file at that path, so the swap area that the resume offset names is not the one that root would
activate, and no `swapon` of `/swap/swapfile` can succeed there. Whether a resume attempted from such a
root would still find the (device-level) header is a kernel-path question I did not exercise and do
not claim. Nothing in the plane or the gate mentions the `@/swap` subvolume at all.

---

## 4. Proposed patch (written under my own wave directory; not applied to lane files)

Observation (§3f): the current-use rows `corpus/knowledge/kill-event-deep-r8.md:259` and
`corpus/knowledge/oom-event-plane.md:348` name `/dev/zram0` 4 G (prio 100) as present swap capacity,
but the device does not exist on this host (`ls /dev/zram*` → no such file; module not loaded;
`swapon --show` lists only `/swap/swapfile`).

Proposed patch file (written, **not applied**):
`.ufo/waves/round-84/w1/ScoutHost/proposed-zram-freshness-notice.patch` — a unified diff that appends a
dated `## R84-FRESHNESS — … zram clause (2026-11-06)` notice to `corpus/knowledge/oom-event-plane.md`
(after its last line) and to `corpus/knowledge/kill-event-deep-r8.md`, in the same append-only shape as
the existing R18-FRESHNESS notices. It touches no round-84 file, no instrument and no manifest.
`git apply --check` on it returns clean (`PATCH_APPLIES_CLEANLY`); `git status --porcelain` on both
corpus files is empty — **the patch was not applied**: the lane's write scope forbids editing corpus
files from this seat, and the L1 decides what lands.

---

## 5. Unrun / not established

- **No hibernation or resume was exercised** — by host guard. Every "holds" above is an agreement
  between configured values, sources and the live kernel's own idea of where the swap header is; no
  image was written and no resume was attempted.
- **Which writer set `/sys/power/resume` this boot** stays unresolved (the plane says the same at
  its Limits): the kernel's `resume_setup()`/`resume_offset_setup()` (`kernel/power/hibernate.c`) and
  the initramfs `systemd-hibernate-resume` both write those two nodes, and the host values are
  consistent with either. Not separable read-only.
- **The `nohibernate` / `hibernate=no` / `noresume` kernel semantics** were read from the pinned
  kernel-parameters snapshot and from upstream `kernel/power/hibernate.c`; I did not exercise them.
- **`zswap` vs. the hibernation write path** (does the hibernation image write interact with the zswap
  pool?) is **unresolved**: no upstream zswap document mentioning hibernation was retrieved, and the
  behaviour cannot be observed without hibernating. Reported as a candidate only.
- **Snapshot-root resume behaviour** (§3j) is unexercised.
- The `systemd-sleep` binary's own strings (`No valid 'resume=' option found, refusing to hibernate.`,
  `Failed to write mode to /sys/power/disk`) were read as evidence of the upstream refusal paths; I did
  not run `systemd-sleep hibernate`.
- Scratch: `/fast/scratch/hyaku/tsukuroi-r84/ScoutHost` was used for capture output, the UKI initrd
  extraction and the byte-level pages, and was removed on exit. The copied receipt remains at
  `.ufo/waves/round-84/w1/ScoutHost/receipt.txt` (sha256
  `9a475afaf4b1662efee9b99d772b3b06498214ae9f24760027d3ce25ab2c6731`).
