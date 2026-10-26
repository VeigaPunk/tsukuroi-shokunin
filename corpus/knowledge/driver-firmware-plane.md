# Driver / firmware plane — tsukuroi knowledge note

Measured 2026-10-14 ~09:53–09:57 (-03), read-only probes, host `plazir27`.
Kernel `7.2.3-arch1-3` (uname -a; built 2026-09-06), Arch Linux rolling,
boot of 2026-10-13 11:02 (uptime 22:55 at probe). Never installed, synced,
or restarted anything; secrets shape-only (none encountered here); blob
contents never read (presence/sizes only, per assignment).

Scope note on the ring buffer: `/proc/sys/kernel/dmesg_restrict` = `1`,
so `dmesg` as uid 1000 returns nothing. All kernel-ring evidence below is
`journalctl -k -b` (journal read access confirmed: `journalctl -b -n 2`
returns lines). Counts that accumulate at runtime (UFW) carry the
measurement time.

## 1. Loaded modules of interest (this boot, `lsmod`)

nvidia stack (module | size | used):

| module | size | used |
|---|---|---|
| nvidia | 18190336 | 411 |
| nvidia_uvm | 2449408 | 4 |
| nvidia_modeset | 1921024 | 15 |
| nvidia_drm | 167936 | 43 |
| drm_ttm_helper | 20480 | 2 (amdgpu, nvidia_drm) |

(`lsmod | grep -i nvidia`; `drm_ttm_helper` listed because it references
both DRM drivers.)

sound stack (module | size | used):

| module | size | used |
|---|---|---|
| snd | 159744 | 26 |
| snd_hda_intel | 73728 | 2 |
| snd_usb_audio | 626688 | 4 |
| snd_hda_codec | 225280 | 4 |
| snd_hda_core | 151552 | 4 |
| snd_hda_codec_hdmi | 61440 | 2 |
| snd_hda_codec_nvhdmi | 16384 | 1 |
| snd_hda_codec_atihdmi | 20480 | 1 |
| snd_pcm | 221184 | 5 |
| snd_seq | 135168 | 7 |
| snd_seq_dummy | 16384 | 0 |
| snd_seq_device | 16384 | 3 |
| snd_rawmidi | 53248 | 2 |
| snd_usbmidi_lib | 53248 | 1 |
| snd_ump | 40960 | 1 |
| snd_hwdep | 24576 | 2 |
| snd_timer | 57344 | 3 |
| snd_intel_dspcfg | 49152 | 1 |
| snd_intel_sdw_acpi | 16384 | 1 |
| snd_hrtimer | 16384 | 1 |

(`lsmod | grep -E '^snd'`.) In-tree module files (7.2.3 tree):
`kernel/sound/hda/controllers/snd-hda-intel.ko.zst`,
`kernel/sound/usb/snd-usb-audio.ko.zst`,
`kernel/sound/hda/codecs/hdmi/snd-hda-codec-atihdmi.ko.zst`
(`modinfo …`).

Sound devices (`/proc/asound/cards`): card0 `USB-Audio - USB Audio`
(Generic USB Audio, usb-0000:11:00.0-12), card1 `HDA-Intel - HDA NVidia`
(0xdc080000 irq 168), card2 `HDA-Intel - HD-Audio Generic`
(0xdcf80000 irq 170) — i.e. USB + NVIDIA HDMI + AMD HDMI all present.

## 2. NVIDIA driver presence

Packages (`pacman -Qi …`, install dates):

| package | version | installed |
|---|---|---|
| nvidia-open-dkms | 610.57.04-1 | 2026-10-11 16:14:37 |
| nvidia-utils | 610.57.04-1 | 2026-10-11 16:14:19 |
| lib32-nvidia-utils | 610.57.04-1 | 2026-10-11 16:14:33 |
| libva-nvidia-driver | 0.0.18-1 | 2026-10-11 16:14:34 |
| linux-firmware-nvidia | 20260810-2 | 2026-10-11 16:14:35 |

`/var/log/pacman.log`: `[2026-10-11T16:14:37-0300] [ALPM] upgraded
nvidia-open-dkms (610.43.03-3 -> 610.57.04-1)`; DKMS scriptlets built
`nvidia/610.57.04` for `7.1.4-arch1-1` and `7.2.3-arch1-3` on the same day.

Loaded module identity (`modinfo nvidia`):
`filename: /lib/modules/7.2.3-arch1-3/updates/dkms/nvidia.ko.zst`
(12,027,573 bytes on disk), `version: 610.57.04`,
`vermagic: 7.2.3-arch1-3 SMP preempt mod_unload`. Only kernel tree present:
`ls /lib/modules/` → `7.2.3-arch1-3` (the 7.1.4 build from the pacman log is
gone).

Driver state:
- `/proc/driver/nvidia/version`: NVRM 610.57.04, open kernel module, built
  gcc 16.2.1 20260810.
- `/proc/driver/nvidia/gpus/0000:01:00.0/information:1` → `Model: NVIDIA
  GeForce RTX 5070`; `:10` → `GPU Firmware: 610.57.04`; Video BIOS
  `98.05.4a.00.5d`, PCIe.
- `nvidia-smi` (09:53:12): driver/KMD 610.57.04, CUDA UMD 13.3, RTX 5070,
  12227 MiB, persistence Off, P8 idle 13W/250W, 31C; 7 client processes
  (Hyprland, Xwayland, walker, one Electron-style name, 3× alacritty).
- Kernel log: `NVRM: loading NVIDIA UNIX Open Kernel Module for x86_64
  610.57.04`, `nvidia-modeset: … 610.57.04`, `[drm] Initialized
  nvidia-drm 0.0.0 … on minor 1` (all Oct 13 11:02:03–04).
- Taint lines this boot (1 each): `nvidia: loading out-of-tree module taints
  kernel.`, `nvidia: module verification failed: signature and/or required
  key missing - tainting kernel`; splat header shows
  `Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE`. Consistent with Secure
  Boot off: EFI var `SecureBoot-8be4df61-…` first data byte `0`
  (raw bytes 6,0,0,0,0); `mokutil` not installed (`command -v` empty).
- Runtime params (GSP firmware path active): `/proc/driver/nvidia/params:28`
  → `EnableGpuFirmware: 18`, `:29` → `EnableGpuFirmwareLogs: 2`.

## 3. GSP firmware shape (presence / sizes only; contents never read)

Driver-requested blobs (`modinfo nvidia` firmware entries, owner
`nvidia-utils 610.57.04-1`, dir mtime 2026-10-11 16:14):

| file under /lib/firmware/nvidia/610.57.04/ | bytes |
|---|---|
| gsp_ga10x.bin | 84310168 |
| gsp_tu10x.bin | 29381504 |
| ucodes_ga10x.bin | 31744 |
| ucodes_tu10x.bin | 12032 |

Per-chip tree from `linux-firmware-nvidia 20260810-2` (mtime 2026-08-14),
example GB205/RTX 5070 class (`/lib/firmware/nvidia/gb205/gsp/`):

| file | bytes |
|---|---|
| bootloader-570.144.bin.zst | 199358 |
| fmc-570.144.bin.zst | 199839 |
| gsp-570.144.bin.zst | symlink → ../../ga102/gsp/gsp-570.144.bin.zst |

Resolved target `/usr/lib/firmware/nvidia/ga102/gsp/gsp-570.144.bin.zst`
= 51,762,663 bytes (`stat -Lc`). Same-named trio exists for
`gb203/` and `gb206/` (`ls`); `/lib/firmware/nvidia/` holds 42
subdirectories (28 chip families + the version dir), presence census only.

Load-attempt forensics (atimes; contents not read):
- `610.57.04/gsp_ga10x.bin` + `gsp_tu10x.bin`: atime 2026-10-13 12:19:53.
- `gb205/gsp/bootloader-570.144.bin.zst` + `fmc-570.144.bin.zst`: atime
  2026-10-13 23:28:37.
- `gb205/gsp/gsp-570.144.bin.zst` (target ga102 blob): atime 2026-10-14
  09:53:32.
No suspend/hibernate occurred this boot (`journalctl -b` grep for
`PM: suspend|systemd-suspend|Suspending system|Freezing user space` → 0
hits), and no nvidia/gsp journal line exists near those times (23:28
window shows only UFW; 09:50–09:56 window has 0 nvidia/firmware/gsp hits).
Which blob the GB205 GPU actually maps, and what read the files at those
atimes, is not determinable from non-root read-only logs → Unknowns U1/U2.

## 4. Boot error/warn classes (bounded, kernel ring via journal)

As measured 2026-10-14 ~09:54 (UFW counts drift upward with live traffic):

| class | count | anchor |
|---|---|---|
| kernel warning+ lines total | 8278 | `journalctl -k -b -p warning \| wc -l` |
| ├ UFW BLOCK (all warning level) | 8191 | `journalctl -k -b \| grep -c 'UFW BLOCK'` |
| kernel err lines total | 38 | `journalctl -k -b -p err \| wc -l` |
| ├ sr0 READ errors (`critical target error` + `Buffer I/O error`) | 35 (20+15) | grep -c on `-k -b` |
| ├ OOM kill event (1 event / 2 lines) | 1 | `invoked oom-killer` + `Out of memory: Killed` |
| ├ nvidia taint lines (OOT + unsigned) | 2 | see §2 |
| └ `virt/tdx: TDX not supported by the host platform` | 1 | err head |

- sr0 errors: all 2026-10-13 11:02:03–06, op `(READ)` on `dev sr0`
  (optical drive probe at boot; sectors 44986976–44989024). Boot-time
  only, none since.
- OOM (Oct 13 23:44:30): `GpuWatchdog invoked oom-killer`, killed
  `python3` PID 1732581 (`total-vm:56727648kB, anon-rss:27873696kB,
  oom_score_adj:200`); splat tainted G OE; hardware string
  `MS-7E59/MAG X870E TOMAHAWK WIFI (MS-7E59), BIOS 2.AC3 06/25/2026`.
  Same boot: 191 `dumped core` lines in journal (godot ≥142,
  MainThread ≥47) — the all-units err volume (60,941 lines) is dominated
  by coredump stack dissections, not kernel faults.
- Kernel "errors" are thus 35 boot-only optical-drive lines + 1 OOM event
  + 1 informational + 1 blank; no nvidia/driver fault class this boot.

## 5. Update candidates (read-only)

- `checkupdates` absent: not on PATH, and `pacman -Q pacman-contrib` →
  `error: package 'pacman-contrib' was not found`. `yay` exists at
  `/usr/bin/yay` but was not invoked (network, out of read-only scope).
- `pacman -Qu` (LC_ALL=C) → empty output, exit code 1 — no upgrade
  candidates known to the local sync DB.
- Local sync DB snapshot: `core.db`, `extra.db`, `multilib.db` mtimes
  2026-09-08 15:23; `omarchy.db` 2026-10-11 10:16
  (`ls -la /var/lib/pacman/sync/`).
- Cross-check against that snapshot: `pacman -Si linux` → 7.2.3.arch1-3
  (== running/installed), `pacman -Si nvidia-utils` → 610.57.04-1
  (== installed).
- Inference (clearly inference): an empty `-Qu` only proves "nothing
  newer than the 2026-09-08 snapshot", ~5 weeks before probe; it cannot
  prove "no updates exist". A truthful candidate list needs a network
  DB refresh (`-Sy`/checkupdates), which is a write action → operator.
  The lane never syncs or upgrades.

## 6. Observations / Inferences / Unknowns

Observations: everything in §1–§5 is directly measured. Key one-liner:
driver plane is healthy — open DKMS 610.57.04 loaded and active, both
firmware shapes present, no driver fault class this boot.

Inferences: (a) sync DB staleness makes `-Qu` under-informative (§5);
(b) unsigned DKMS + Secure Boot off is internally consistent (§2);
(c) coredump volume, not drivers, explains the boot's error-line total
(§4).

Unknowns:
- U1: which GSP image the running driver uses for the GB205 (no
  non-root log evidence; blob-content identification is rejected here as
  out of province — RE belongs to kaidoku/revenger; kept as rejection).
- U2: what processes read the firmware files at the three atimes above
  (no suspend, no nvidia log lines; root-only tracing would be needed).
- U3: actual current update set (needs network DB refresh; §5).
- U4: whether the 142 godot coredumps relate to GPU/driver state at all
  (process-level events; out of this plane).
- U5: long-term stability of the GSP path (single-boot snapshot only).

## Errata (append-only)

(none yet — as declared at write time 09:58; wave-1 errata appended below)

### Wave-1 errata applied (2026-10-14 10:51 -0300, re-measured; append-only)

Wave-1 record sources: `SKILL.md:44` (driver-row residues), `corpus/README.md:9`
(coverage claim), `CORPUS.md:17`. Scratch `/tmp/tsukuroi-r2-3-work/`.

- 2026-10-14 — **stale dkms registration landed as erratum** (body §2 carried
  the pacman-log build line, not this residue): `dkms status` →
  `nvidia/610.57.04, 7.1.4-arch1-1, x86_64: installed (Original modules exist) (Built modules are missing in the kernel modules folder)`
  beside `nvidia/610.57.04, 7.2.3-arch1-3, x86_64: installed`; `ls /lib/modules/`
  = `7.2.3-arch1-3` only. Classification judgment: residue, not a driver
  failure — the loaded module is the 7.2.3 build. [observation + judgment]
- 2026-10-14 — **unowned module landed as erratum** (pacman cannot verify the
  DKMS artifact): `pacman -Qo /lib/modules/7.2.3-arch1-3/updates/dkms/nvidia.ko.zst`
  → `error: No package owns …`, rc=1; file 12 027 573 B, mtime
  2026-10-11 16:15:34.810910954; `modinfo nvidia` → `version: 610.57.04`;
  `nvidia-smi --query-gpu=name,driver_version` → `NVIDIA GeForce RTX 5070,
  610.57.04` (rc=0). [observation]
- 2026-10-14 — **field-contract erratum**: the header carries measured-date
  prose, not the contracted literal keys (`CORPUS.md:17`). Appended values:
  `source:` lsmod / dkms / modinfo / nvidia-smi probes, host `plazir27`;
  `verified-at:` 2026-10-14 (wave-1 audits + this re-measure); `recheck:`
  `dkms status`; `ls /lib/modules`; `pacman -Qo` on the DKMS module;
  `nvidia-smi --query-*`. [observation]

## Errata (round 4)

- 2026-10-14 (TSUKUROI-ERR-S sweep) — **header pins re-verified, hold.** `uname -a` →
  `7.2.3-arch1-3` (built 2026-09-06); `modinfo nvidia` → `version: 610.57.04`; `dkms status`
  still lists the stale `nvidia/610.57.04, 7.1.4-arch1-1 … (Built modules are missing in the
  kernel modules folder)` row beside the live `7.2.3-arch1-3` row; `ls /lib/modules/` → `7.2.3-arch1-3`
  only. Every pinned anchor at `:3-6,80-86` holds. No stale pin on this note. [observed]
- 2026-10-14 — the field-contract erratum already carried above (`:239`, `CORPUS.md:17`) stands;
  not duplicated. **md5-pin consequence:** this append changes this file's md5 and line count, so
  `host-health-report-r3.md` §5's pin for this note (`a44e9c07d5b139fe65d5284674398b3a`, 242
  lines) is superseded as of this block; post-append values recorded in that report's round-4
  errata. [observation]

## Erratum (2026-10-19, fleet round 1) — D1: Bare -Sy is not a safe refresh route
Superseded (`corpus/knowledge/driver-firmware-plane.md:192`): “DB refresh (`-Sy`/checkupdates), which is a write action → operator.”
Correction: use pacman-contrib's `checkupdates` for a safe installed-package update check, or a complete `pacman -Syu`; never advise bare `pacman -Sy`.
Source: S010 https://wiki.archlinux.org/title/System_maintenance § Avoid certain pacman commands: “never run `pacman -Sy`; instead, always use `pacman -Syu`.” S010 § Partial upgrades are unsupported: `checkupdates` safely checks installed-package updates without a system update.
[obs] Host `/var/log/pacman.log`, re-opened 2026-10-19: `grep -nE 'pacman -Sy ' /var/log/pacman.log` → line 1405 (`2026-10-11T12:54:13-0300`, `pacman -Sy --noconfirm fuse2`) and line 2287 (`2026-10-18T14:11:00-0300`, `pacman -Sy --noconfirm`). `grep -nE 'pacman -Syu|Running .pacman -Syu' /var/log/pacman.log` → line 1414 (`2026-10-11T16:13:19-0300`); the first gap is 3h19m06s, while no later full `-Syu` is recorded after line 2287.
S010 https://wiki.archlinux.org/title/System_maintenance § Avoid certain pacman commands; own-work S032 `/var/log/pacman.log` lines 1405, 1414, 2287.

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — `lsmod`, DKMS, `modinfo`, `nvidia-smi`, pacman package and kernel-journal probes on host `plazir27`, 2026-10-14; S010 https://wiki.archlinux.org/title/System_maintenance § Avoid certain pacman commands; S032 `/var/log/pacman.log` lines 1405, 1414, 2287 (re-opened 2026-10-19).
verified-at: 2026-10-14 (the driver/firmware measurement window; D1 log evidence re-opened 2026-10-19).
recheck: 90d; procedure: `dkms status`; `ls /lib/modules`; `pacman -Qo` on the DKMS module; `nvidia-smi --query-*`.

## R17-FRESHNESS — dated host re-verification (2026-10-20)

Historical captures stay historical: every dated measurement above (the 2026-10-13 boot, the 2026-10-14 probes, the dated errata) keeps its original meaning. The bullets below re-verify only current-use pins invalidated by the 2026-10-20 09:15 `pacman -Syu` (log line 2462; `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:59`). Sources: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt` and `.ufo/waves/round-17/l1-capture/fresh-capture.txt`, read-only, captured 2026-10-20. Not re-captured, therefore not re-verified [unk]: `/proc/driver/nvidia/params`, GPU firmware `:10`, the `/lib/firmware/nvidia/610.57.04/` blob tree, `lsmod`. Nothing here authorizes package, service, or boot action.

- Stale: "Kernel `7.2.3-arch1-3` (uname -a; built 2026-09-06)" — [obs] running kernel 7.2.11-arch1-1 (uname -r). Capture `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:5`.
- Stale: "boot of 2026-10-13 11:02 (uptime 22:55 at probe)" — [obs] current boot started 2026-10-20 09:57:08 (uptime -s). Capture `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:6`.
- Stale: "filename: /lib/modules/7.2.3-arch1-3/updates/dkms/nvidia.ko.zst" — [obs] 7.2.3-arch1-3 dkms row: built modules missing (615.78.08); the loaded module is not re-identified by modinfo [unk]. Capture `.ufo/waves/round-17/l1-capture/fresh-capture.txt:38`.
- Stale: "NVRM 610.57.04, open kernel module, built" — [obs] NVRM 615.78.08, open kernel module, Release Build (`/proc/driver/nvidia/version`). Capture `.ufo/waves/round-17/l1-capture/fresh-capture.txt:33`.
- Stale: "Only kernel tree present:" — [obs] /usr/lib/modules holds 6.18.57-2-lts and 7.2.11-arch1-1; no 7.2.3-arch1-3 tree is listed. Capture `.ufo/waves/round-17/l1-capture/fresh-capture.txt:41` (listing lines 40-41).
- Stale: "2026-09-08 15:23; `omarchy.db` 2026-10-11 10:16" — [obs] core/extra/multilib.db 2026-10-17 22:37; omarchy.db 2026-10-20 09:09:26. Capture `.ufo/waves/round-17/l1-capture/fresh-capture.txt:13` (core/extra/multilib at lines 10-12).
- Stale: "`pacman -Si linux` → 7.2.3.arch1-3" — [obs] installed dir linux-7.2.11.arch1-1 present; `pacman -Si` was not re-run (pacman out of scope this round). Capture `.ufo/waves/round-17/l1-capture/fresh-capture.txt:21`.
- Stale: "driver plane is healthy — open DKMS 610.57.04 loaded and active, both" — [obs] running NVRM 615.78.08; the 610.57.04 headline no longer holds. Capture `.ufo/waves/round-17/l1-capture/fresh-capture.txt:33`.
- Stale: "`nvidia/610.57.04` for `7.1.4-arch1-1` and `7.2.3-arch1-3` on the same day." — [obs] dkms status: nvidia/615.78.08 for 6.18.57-2-lts, 7.2.11-arch1-1, 7.2.3-arch1-3 (built modules missing); no 7.1.4-arch1-1 row. Capture `.ufo/waves/round-17/l1-capture/fresh-capture.txt:37` (rows at lines 36-38).
- Stale: "| nvidia-open-dkms | 610.57.04-1 | 2026-10-11 16:14:37 |" — [obs] installed nvidia-open-dkms-615.78.08-1; ALPM upgrade 2026-10-20 09:16:44 (610.57.04-1 -> 615.78.08-1). Capture `.ufo/waves/round-17/l1-capture/fresh-capture.txt:24` and `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:52`.
- Stale: "`nvidia-utils 610.57.04-1`, dir mtime 2026-10-11 16:14):" — [obs] installed nvidia-utils-615.78.08-1 (blob-dir owner not re-captured [unk]). Capture `.ufo/waves/round-17/l1-capture/fresh-capture.txt:25`.


## R17-RECHECK — steer-safe procedure

Appended 2026-10-20 by the tsukuroi round-17 L1; earlier bytes unchanged. Supersedes the package-manager invocations in this file's `recheck:` line for any round whose steer forbids running pacman (QUALITY 26); file reads replace them and the substitution is recorded in that round's report. Read-only.

- `dkms status`
- `ls /usr/lib/modules`
- owner of the DKMS module without a package query: `grep -l "^usr/lib/modules/$(uname -r)/updates/dkms/" /var/lib/pacman/local/*/files` (an empty result means no package owns it, as DKMS builds are unowned)
- `cat /proc/driver/nvidia/version`
- `nvidia-smi --query-gpu=name,driver_version --format=csv,noheader`


## R18-FRESHNESS — sibling current-use restatements (2026-10-20)

Sources S060, S051 and S052. This appended correction supersedes the current-use readings listed below and every repeated current-use restatement of the same premise in this file. Historical measurements remain intact. No package, service, rebuild, boot or rollback action is authorized.

- R18-FRESH-SUPPLEMENT-12: prior locus `- `checkupdates` absent: not on PATH, and `pacman -Q pacman-contrib` →`. Now: S060 lists pacman-contrib-1.13.1-1 in local metadata and resolves /usr/bin/paccache; old package/paccache-absence guidance is not current. This capture does not query or resolve checkupdates, so its availability and any use elsewhere remain unknown; no installation is advised [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:82-86]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:36.


## R18-PRECISION — repository timestamp

The R17 notice's 'omarchy DB refreshed' wording is withdrawn as a claim about local refresh timing: the cited value is a filesystem mtime only. S060:42–46 likewise captures filesystem mtimes; neither timestamp read proves local acquisition, synchronization or content freshness. Current pending updates remain unmeasured. The earlier dated timestamp stays visible, but is not a refresh receipt.

### Round-27 note on the taint wording (appended 2026-10-22)

Lines 160 and 202 above call the nvidia modules "unsigned". At the round-27 capture (`.ufo/waves/round-27/capture/capture.txt`, driver 615.78.08) each nvidia module carries a signature (`modinfo -F signer` prints "DKMS module signing key"); the kernel sets E because it does not accept that signature, not because none is attached. Read "unsigned" above as "signature not verified by the kernel". The mechanism, the decoding of the taint number and the operator actions are in `corpus/knowledge/kernel-taint-r27.md` (sources S140 to S145). The Secure Boot reading in section 2 is from 2026-10-13 and was not re-checked in round 27.

### Round-29 owed-statement marker (appended 2026-10-22)

[R29-OWED-O08] verdict: corrected | original: "the loaded module is not re-identified by modinfo [unk]" | now: The round-27 capture re-identifies the loaded module: modinfo -F filename nvidia reports /lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst, version 615.78.08 and signer DKMS module signing key, so the loaded DKMS build for the running 7.2.11 kernel is named and the round-17 unknown is closed. | basis: .ufo/waves/round-27/capture/capture.txt:45 (the command `modinfo -F filename nvidia`), .ufo/waves/round-27/capture/capture.txt:49 (615.78.08), .ufo/waves/round-27/capture/capture.txt:55 (DKMS module signing key), the round-27 kernel-taint capture whose sha256 88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841 matches `corpus/knowledge/kernel-taint-r27.json` `capture.sha256`

## Round-39 correction (TO1, TO8; append-only)

Round-39 correction (TO8, TO1): the `dkms install` builds of 2026-10-11 were run by the PostTransaction hook `70-dkms-install.hook` after `transaction completed` (`pacman.log` 1950, 1977-1979 of the frozen copy), not by DKMS install scriptlets; the `[ALPM-SCRIPTLET]` tag on their output marks chroot-child output, not a package scriptlet. Source: `corpus/knowledge/pacman-transaction-order-r39.md` TO1, TO8 (S216, S217).
