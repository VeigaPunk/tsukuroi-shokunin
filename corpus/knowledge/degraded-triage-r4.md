# DEGRADED-finding triage — round 4 (TSUKUROI-S4-1)

source: triage of `corpus/knowledge/host-health-report-r3.md` — every one of its
§0.1 twenty DEGRADED findings (P1–P5, D1–D3, J1–J4, U1–U8) plus the round-4
classes its §6 errata recorded as untriaged (per that file's own instruction:
"round-4 triage material — recorded here, not triaged").
method: read-only probes, one level deeper than r3 (the mechanism, not only the
symptom); each row carries class → mechanism (command + output shape) → blast
radius → priority-ordered action. Classes per `plans/round-4.plan.md:5-6`:
package / service / driver-firmware / config.
verified-at: 2026-10-14, probes 13:19–13:33 -03 (UTC 16:19–16:33); census gate
re-run twice inside the window (16:19:56Z, 16:28:00Z); every number below is a
capture with its command and time.
recheck: Appendix A; `bash tools/tsukuroi-census.sh --selftest && bash
tools/tsukuroi-census.sh`.
read-only: no install/upgrade/remove/restart; no elevation used — see
"the elevation call" below. Scratch: `/tmp/w4-s41/` (ephemeral).

**What this is.** r3 delivered symptoms with receipts; this note delivers
mechanisms. Twelve of the twenty rows resolve to a named writer or a named
denial (P1–P5, D2, D3, J4, U2, U4, U5, U6, U7); four resolve to a mechanism
class with a routed owner (D1, J1, J3, U3); four are advisory or standing rules
(J2, U1, U8, and U5's rule arm). Six rows are honestly *mechanism blocked* —
five by elevation, one by the secrets shape-only rule — each with the exact
command that would open it. Six new classes appeared inside this round's window
(§5), three of them because the host itself changed state during triage: a user
session restart at 13:10:59 -03, a second sr0 burst, and the census's
failed-history arm flipping 0→8. Two r3 statements are superseded and recorded
as such, never laundered (§9).

**The elevation call (measured, then not used).** `sudo -n true` → rc=0: this
host *has* passwordless sudo for `vgpnk`, so the elevation-dependent rows are
blocked by lane discipline (PROVINCE.md:16-17, r3 "never escalated"), not by
capability. They stay "mechanism blocked" with the exact operator command, and
the capability itself is reported as an operator-relevant fact. No row below was
measured with raised privilege.

## 0. Anchor (census-v2 re-run inside this round, md5 `41953ee9f2099281c91759249fe8708f`, 976 lines)

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T16:28:00Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(...) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16; pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=407 (coredump=244 kernel=139 other=24); failedhist=8[...]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

Selftest in the same window: rc=0, 26/26 PASS. Drift vs r3's 14:57:13Z capture
(70 min): packages and systemd byte-identical; `kerr` 38→139 (io 35→70, other
2→68), `err` 251→407 (coredump 211→244, kernel 38→139, other 2→24), rollup
unchanged. Arithmetic closes exactly — a replay-anywhere check: kernel 139 =
40 sr0-critical + 30 sr0-buffer + 64 usb + 2 xhci + 1 tdx + 1 oom + 1 blank;
journal other 24 = 10 pipewire + 3 pipewire-pulse + 8 xdg-autostart + 2
sddm-helper + 1 limine-snapper-sync; 244 + 139 + 24 = 407.

## 0.1 Triage matrix (20 r3 findings; priority = §0.2 queue position)

| ID | class | mechanism, one line (detail §) | blast radius | blocked | pri |
|---|---|---|---|---|---|
| P1 | package | vendor `.INSTALL` script sets setgid+dynamic group; package mtree records 644 root:root → drift is by design, content sha256 intact (§1) | census packages plane DEGRADED forever; no function loss | no | P2 |
| P2 | package | verify artifacts are privilege-induced: 600/640/700 modes + `/boot` dmask mask (§1) | 36 of the full-sweep verdicts unreadable non-root; sample arm unaffected | verification: elevation | P3 |
| P3 | config | omarchy install-time shebang patch (`env python3`→`/bin/python3`) — 4-line diff vs cached package (§1) | pacman flags it forever; next upgrade of that package silently reverts the patch | no | P2 |
| P4 | package | installed from the *installer's offline repo* (`offline.db` members/versions match); channel absent from pacman.conf → foreign by construction (§1) | 14 pkgs incl. walker's backend have no update path; soname bump breaks them silently | no | P3 |
| P5 | package | cache grows only via `-Sc` (no paccache/checkupdates); 3 abandoned alpm download dirs from `DownloadUser=alpm` (§1) | 8.6 G of 930 G; abandoned temp dirs; advisory only | contents: elevation | P3 |
| D1 | driver-firmware | 3 sub-classes: sr0 = reads at the media's unrecorded tail (LBA-out-of-range sense), **recurring** at session transitions; OOM = one 27.8 G python3 kill, cross-domain; TDX informational (§2) | err-count noise; real drive read failures; OOM indicates live memory pressure | no | P1 |
| D2 | driver-firmware | dkms registered the build for the *outgoing* kernel in the Oct 11 wave; tree then removed → stale row (§2) | none functional; every kernel wave can add a row; confuses `dkms status` consumers | no | P2 |
| D3 | driver-firmware | DKMS build output is unowned by design; verification route (modinfo=/sys/module=nvidia-smi) works (§2) | none | no | P3 |
| J1 | service | 244 cores in 3 measured classes: test-induced engine probes (game-dev argv), V8 FatalOOM (memory), app SIGSEGV/SIGBUS (§3) | journal/disk; masks other signals; memory pressure is the systemic part | per-crash stacks: elevation | P1 |
| J2 | config | no retention policy configured anywhere (merged coredump/journald conf = defaults only); storm is the growth engine (§3) | 3.9 G and climbing; `/` has 847 G free (measured) | removal: elevation | P1 |
| J3 | config | pre-userspace dwell is a journal *blackout* by construction (busybox+plymouth initramfs, no journald); 12.9 s → 103 min across boots (§3) | boot-time variance only; resume path dormant (1 `PM: Image not found`/boot) | cause: elevation + shape-only | P2 |
| J4 | service | snapper auto-init **failed with EACCES** creating the `/.snapshots` subvolume (errno 13); not a self-claim (§3) | no snapshots → every wave snapshot-less (U1) | denial vector: elevation | P0 |
| U1 | config | same root cause as J4 + btrfs layout `@/@home/@log/@pkg`, no `.snapshots` anywhere (§4) | no rollback net for any wave on this host | subvolume inventory: elevation | P0 |
| U2 | config | the *single* configured mirror served 2026-09-08-era core/extra/multilib dbs on Oct 11 → "no updates" is mirror staleness, not upstream quiet (§4) | every wave-prep decision is blind; a mirror switch brings 33+ days at once | upstream delta: policy (no network) | P0 |
| U3 | config | kernel wave = mkinitcpio (nvidia modules, plymouth, encrypt, resume) + dkms + limine UKI; `/etc` hook diverges from the packaged hook of the same name (§4) | any kernel/limine/firmware wave writes the ESP, rebuilds initramfs+UKI | effective hook: not observable read-only | P2 |
| U4 | config | `[omarchy]` is the only fresh channel and carries `Optional TrustAll`; local-file sigs Optional; `DownloadUser=alpm` (§4) | the trust decision gates every other update decision | no | P0 |
| U5 | config | installed `1password-beta BETA-32` > channel `BETA-1` (repo omarchy), nothing pins it → plain `-Syu` ignores, `-Suu` downgrades (§4) | an accident-prone operator action rewrites 579 MiB and loses the beta line | no | P0 |
| U6 | config | `/boot` is the ESP mounted `fmask=0077,dmask=0077` → the 700 the gate is a *mount mask*, not on-disk perms (§4) | non-root /boot reads impossible (incl. P2 artifacts); pre-wave checks need root | no | P0 |
| U7 | service | root hook re-execs the user-owned script as its *owner* via `systemd-run --uid=` → privilege is dropped by design; 1 historical run (§4) | dormant (targets only never-updated foreign pkgs) | no | P3 |
| U8 | config | contention is not ffmpeg now (0) but the crash-looping sibling workloads (244 cores/2 h) + 30 G RAM with a 28.5 G session peak (§4) | wave timing; any heavy wave compounds thrash | no | P1 |

## 0.2 Priority-ordered action queue

- **P0 — before any `-Syu` on this host** (each is a one-command operator action
  with a measured root cause):
  1. J4+U1: `sudo snapper -c root create-config /` and set
     `SNAPPER_CONFIG_NAME="root"` in `/etc/default/limine`, then re-run the sync
     unit; re-audit `snapper list-configs`. (Without this any wave is
     snapshot-less — the standing exposure.)
  2. U2: fix/replace the single mirror, then `-Sy` and re-run `-Qu`/`-Sup`;
     only then run the prep list (rollback story, DKMS plan, schedule, trust).
  3. U6: `sudo ls /boot; sudo bootctl status` pre-verify; note the mask so it is
     not misread as corruption.
  4. U4+U5: written decision on the `[omarchy]` TrustAll channel; standing rule
     plain `-Syu` only, never `-Suu`/`-Syyu`.
- **P1 — live host, now**: D1 sr0 (eject/verify the disc; the burst recurs at
  session transitions), J1/J2 (hand crash classes to owners with the argv
  evidence; prune cores only after owners have them), U8 (schedule around the
  crash cadence, not around ffmpeg).
- **P2 — decisions/repairs owed**: P1 (record accepted baseline; no root run
  clears it), P3 (record the omarchy patch; watch its package for silent
  revert), D2 (`sudo dkms remove nvidia/610.57.04 -k 7.1.4-arch1-1`), J3
  (operator probe only if the dwell matters), U3 (post-wave checklist).
- **P3 — hygiene**: P2 root re-run, P4 baseline record, P5 prune, U7 review
  (kagi/operator), J4's upstream-vector hunt.

## 1. Package class

**P1 — mechanism: the vendor's own install script writes the drift.**
`stat -c '%a gid=%g grp=%G'` → `/usr/bin/op` `2755 gid=1002 onepassword-cli`,
`/opt/1Password/1Password-BrowserSupport` `2755 gid=1001 onepassword`;
`getent group onepassword onepassword-cli` → both exist (1001/1002). The
package's `.INSTALL` (`/var/lib/pacman/local/1password-cli-2.40.0-2/install`)
contains `groupadd onepassword-cli` (no `-g` → dynamic GID), `chgrp
onepassword-cli /usr/bin/op`, `chmod g+s /usr/bin/op`; the beta package's script
does the same for its helper. The package mtree records
`/set type=file uid=0 gid=0 mode=644` and per-file entries carry only
`time/size/sha256digest` — so pacman's expected values for these two files are
`644 root:root` and the install script deviates *by design*. Content is intact:
`sha256sum /usr/bin/op` = `8d029d2c…` and `…BrowserSupport` = `000782e7…`, each
equal to its recorded `sha256digest` (both quoted in full in scratch).
[observed] metadata-only drift; [inference] vendor convention, and a root
`pacman -Qkk` would *not* clear it (the comparison is mtree-vs-actual, not
privilege). Blast radius: the census packages arm reads DEGRADED on every run
(it has no accepted-baseline mechanism), and non-root tooling that treats
`-Qkk` rc=1 as corruption will misfire. Action: record the accepted baseline
(operator decision), or extend the census with a documented allowlist in a
later round — today no root action can remove this row.

**P2 — mechanism: tightened modes + a mount mask, nothing content-related.**
`timeout 280 pacman -Qkk` → rc=1, 1332 raw lines, 17 s class runtime,
32 × `failed to calculate SHA256 checksum`, 4 × `Permission denied`
(`/boot/amd-ucode.img`, `/etc/sudoers.d/50-asdcontrol`, `/var/cache/cups/rss`,
`/var/spool/cups/tmp`). Mode histogram over the 32 unreadable files: 9 ×
`640 root:root`, 6 × `600 root:root`, 7 × `640 root:cups`, 2 × `600 root:cups`,
1 × `4110 root:dbus`, 2 × `700 root:root`, 5 unstatable non-root (under the
`/boot` mask or root-only dirs). [observed] every artifact is a
privilege/visibility artifact: file modes 600/640/4110, directories 700, and
the `/boot` `dmask=0077` mask (U6). Blast radius: 36 rows of the full sweep are
unverifiable non-root — the *packages* arm of the census is not affected
(sample-based, `nonroot_artifacts=0`). Action (blocked → §6): operator
`sudo pacman -Qkk > /tmp/qkk-root.txt 2>&1`, classify with
`package-state-plane.md:217-226`; expected to clear the calc/permission series
entirely.

**P3 — mechanism: a deliberate omarchy shebang patch, measured byte-for-byte.**
Cached package present: `/var/cache/pacman/pkg/power-profiles-daemon-0.30-1-x86_64.pkg.tar.zst`;
`bsdtar -xOf … usr/bin/powerprofilesctl | sha256sum` = `38532d5f…` = exactly
the mtree digest; the live file = `cf0b3fa7…`, size 10733 vs recorded 10741,
mtime 2026-10-03 17:44:35 (the install window). `diff -u` is 4 lines, one hunk:
`-#!/usr/bin/env python3` / `+#!/bin/python3` (8 bytes = the size delta). The
omarchy wrapper scripts (`~/.local/share/omarchy/bin/omarchy-powerprofiles-*`)
are separate files, not the cause. [observed] deliberate install-time patch;
[unknown] who wrote it (no script in the omarchy bin dir references the path —
probe remains open). Blast radius: one permanently flagged file; the real
hazard is silent revert — the patch lives only in the file, so the next upgrade
of `power-profiles-daemon` (channel: omarchy/core) restores the packaged
`env python3` shebang without any record. Action: record as accepted/known
patch, and treat that package's future upgrade as a patch-reapplication event.

**P4 — mechanism: the installer's offline repo is the channel; it is not
configured afterwards.** `pacman -Qm` → the 16 recorded (13 × elephant-*,
omarchy-walker, android-apktool-bin, obsidian-cli-inspector). `bsdtar -tf
/var/lib/pacman/sync/offline.db` → 2550 members, **26 = the 13 elephant
packages** at `elephant-2.21.0-1` — the exact installed versions; the db was
born 2026-10-03 17:41:33, one minute before the bootstrap transaction
(`/var/log/pacman.log:484` `pacman -S --noconfirm --needed …`, ALPM `installed
elephant (2.21.0-1)` at 17:44:26). Configured repos now: core/extra/multilib
(mirror), omarchy (231 pkgs, 0 elephant) — `pacman -Si elephant` not found;
`/etc/pacman.conf` has no `[offline]` section. [observed] elephant's
provenance = the install medium's local repo; [inference] the installed system
never carried that channel → foreign by construction, no update path. Packager
field "Unknown Packager" and build dates 2026-04-15 (image era) corroborate.
`elephant` is a *dependency of* `omarchy-walker` (explicitly installed, both
Oct 3 17:44:26); walker is the desktop launcher → a silent soname break
degrades the launcher. Action: record the accepted baseline; any update means
rebuilding from source (network — out of province).

**P5 — mechanism: no pruner installed; abandoned download dirs from
`DownloadUser=alpm`.** `du -sh /var/cache/pacman/pkg` = 8.6 G (3 dirs
unreadable); 3139 cached files; `ls -ld …/download-*` → three dirs `700
alpm:alpm` (2026-10-11 10:31, 2026-10-13 13:52, 2026-10-13 16:21) left by
interrupted/failed download phases; `paccache`/`checkupdates` absent
(`pacman-contrib` not installed) → the cache only shrinks via `-Sc`. Blast
radius: 8.6 G of 930 G (`df`: 847 G free, 9 % used) — hygiene, plus 3 abandoned
temp dirs whose contents stay root-only. Action: optional prune/`pacman-contrib`
(operator install, out of province); root-inspect the 3 dirs first (blocked →
§6).

## 2. Driver-firmware class

**D1 — mechanism: three sub-classes, two of them live.**
*(a) sr0 — reads at the media's unrecorded tail.* Drive size 44989040 sectors;
the failing reads cluster at 44986976…44989024, sense `Illegal Request` /
`Add. Sense: Logical block address out of range` (`Read(10)` CDB
`0x00ab9e98` = 2048-byte LBA 11247256 × 4 = 512-byte 44989024, i.e. the last
block). Occurrence histogram: 117 lines in the 2026-10-13 11:02 boot window,
**60 + 55 lines at 2026-10-14 13:10–13:11**, i.e. the burst *recurred* at the
session transitions (13:10:59.40 = 43 ms after the user manager was SIGKILLed;
13:11:07.47 = the new session's generator run). A disc is present (sr0,
iso9660, 21.5 G, removable=1) — r3's "boot-only, no record since the boot
window" claim is superseded (§9). [inference] a session-start reader probes the
media tail (the ISO9660 backup-descriptor pattern) and the drive rejects it
because the recorded area ends ~2 MB short of the reported capacity; [unknown]
the reading process (no udev/udisks/gnome line names it in either burst;
discriminating probe: `udevadm monitor`/ftrace at the next session transition,
or an audit rule on sr0 — needs elevation or a future lane with the right
tooling). Action (cheap and testable): if the disc is not needed, eject it and
verify the burst stops at the next session change; otherwise treat as drive/
media finding.
*(b) OOM — one kill, cross-domain, with the pressure context.* The only OOM
event in the ring: 2026-10-13 23:44:30, `python3` pid 1732581, `anon-rss
27873696 kB` (27.8 G), `oom_score_adj=200`, invoked from
`app-graphical.slice/…/app-Hyprland-xdg-terminal-exec-…scope` by GpuWatchdog;
memcg `user-1000.slice/memory.events` → `oom_kill 1` lifetime (no second kill).
Context: 30 G RAM, 34 G swap (30.3 G swapfile + 4 G zram), slice peaks 28.5 G
mem / 34.2 G swap, `zswap.enabled=0` on the cmdline. Blast radius: any
memory-hungry GPU/engine workload can be killed (see J1 class B). Action: hand
to the GPU/game-dev workstream; optionally raise headroom (operator decision —
no restart, no config change from this lane).
*(c) TDX* — one informational line, host is not a TD; no action.

**D2 — mechanism: the Oct 11 kernel wave registered a build for the outgoing
kernel.** `dkms status` still lists `nvidia/610.57.04, 7.1.4-arch1-1 …
(Built modules are missing in the kernel modules folder)`; `/lib/modules/` holds
only 7.2.3-arch1-3; `/var/lib/dkms/nvidia/610.57.04/` holds `7.1.4-arch1-1/`,
`7.2.3-arch1-3/`, `source/`. `/var/log/pacman.log` (2026-10-11):
16:14:35 `linux 7.1.4.arch1-1 -> 7.2.3.arch1-3`; 16:14:37 `nvidia-open-dkms
610.43.03-3 -> 610.57.04-1`; 16:14:49 `70-dkms-install.hook`; 16:14:50
`dkms install --no-depmod nvidia/610.57.04 -k 7.1.4-arch1-1` then 16:15:12
`-k 7.2.3-arch1-3`. [observed] the hook built for both kernels while the old
tree still existed; removing the tree left the registry row. Blast radius: none
functional (loaded version 610.57.04 — `/sys/module/nvidia/version` = `modinfo
-F version` = `nvidia-smi` = 610.57.04); accumulates one stale row per kernel
wave. Action: `sudo dkms remove nvidia/610.57.04 -k 7.1.4-arch1-1`, then verify
`dkms status` lists only the running kernel; fold "verify dkms status for the
new kernel before reboot" into every wave (U3).

**D3 — mechanism: DKMS output is unowned by design; the verification route
works.** `/lib/modules/7.2.3-arch1-3/updates/dkms/` = 5 modules
(nvidia{,-drm,-modeset,-peermem,-uvm}.ko.zst); `pacman -Qo` of the main one →
rc=1 (no owner). Chain verified: `modinfo -F version` = `610.57.04` =
`/sys/module/nvidia/version` = `nvidia-smi` version. Blast radius: none (pacman
cannot verify it, by construction). Action: keep the modinfo/sysfs/smi triple as
the post-wave check; repackaging is out of province.

## 3. Journal/boot class

**J1 — mechanism: the storm has three measured classes; only one is systemic.**
Counts: 211 (14:57Z) → 228 (16:06Z) → 244 (16:28Z), live. By exe: godot 169
SIGABRT, node 47 (SIGABRT/SIGTRAP), love 7 SIGABRT, blender 7 SIGSEGV,
python3.14 4 SIGSEGV, grok-bot 3 SIGBUS, typora 2 SIGTRAP, chrome_crashpad 2
SIGBUS, electron 1, Hyprland 1 (uid 964, greeter), bash 1.
*Class A — test-induced engine probes (game-dev lanes).* Measured argv
(`coredumpctl info 1128973`): `godot --headless --path
corpus/live/r74-baseline/runs/20261014T160615371269Z/scratch --script
res://spontaneous_crash_probe.gd -- --spontaneous-crash`; cmdline census over
the boot: godot argv sets `r61-critic`, `r68-simplifier`, `r69-baseline`,
`r69-scribe`, `r83b_edges.gd`, `proj_jolt --arm=world3d_free`; love argv
`…/r74-boundary/cells`. [inference] a large share is deliberate/expected crash
probing, not host fault; [unknown] the split deliberate-vs-incidental (needs
core stack reads — blocked).
*Class B — memory exhaustion.* node cores show the V8 FatalOOM path
(`_ZN2v84base2OS5AbortEv` … `FatalProcessOutOfMemory` … `Isolate::Init`), i.e.
the process cannot allocate its startup heap — including `node -e 1` and
`node … wakaru --version` (6 and 9 occurrences). [observed] this class is a
*symptom of host memory pressure* (see D1-b), not a node defect.
*Class C — app crashes to route*: blender SIGSEGV, python3.14 SIGSEGV,
grok-bot/chrome_crashpad SIGBUS. [unknown] causes.
Blast radius: journal err mass (244/407), 3.9 G cores, and masking — the storm
drowns other err signals (that is the real cost). Action: hand classes A/C to
the owning workstreams with the argv evidence; reduce memory pressure for B;
re-count with `journalctl -b -p err -o json --no-pager | wc -l`. Blocked →
§6 for per-crash stacks.

**J2 — mechanism: no retention policy is configured; the storm is the growth
engine.** `/var/lib/systemd/coredump` = 3.9 G (215 files at 13:24);
`systemd-analyze cat-config systemd/coredump.conf` → `[Coredump]` with no
settings; no `/etc/systemd/coredump.conf.d/`; journald likewise `[Journal]`
with no settings. [observed] effective limits are compiled defaults — nothing
local expresses them (r3's unknown #10 stands); `coredumpctl --help` in this
build has no delete/vacuum → removal is a root file operation. Disk pressure
measured: `/` 80 G used of 930 G (847 G free) — no pressure. Action: prune once
owners have the cores (blocked → §6); decide an explicit retention policy
(operator). 

**J3 — mechanism: the dwell is a journal blackout by construction — 12.9 s to
103 min, unmeasurable from inside.** Per-boot first journal monotonic (the
initramfs phase ends when journald starts): 12.9 / 15.8 / 21.6 / 25.9 / 36.0 /
114.3 / 165.1 / 244.2 (boot 0) / 1616.7 / 5311.3 / 6187.6 s (two boot datasets
unparsed — the first entry lacked the monotonic bracket; shape-only note). Boot
0's first entry is `[ 244.159301]` and every kernel line from BIOS map to
device probe carries the *same* monotonic stamp — proof that journald timestamps
the ring at *read* time, i.e. the entire pre-userspace phase has zero journal
coverage. Causally consistent: `HOOKS` has no `systemd` hook (busybox
initramfs) and includes `plymouth`; `quiet splash loglevel=0` suppresses the
console. [inference] the phase is dominated by the plymouth/LUKS passphrase
wait (`cryptdevice=…:root` on the cmdline, root = `crypto_LUKS` → btrfs);
magnitude is operator/attendance dependent. [unknown] crypttab/keyfile/resume
configuration — never read (shape-only: `/etc/crypttab` 600 root:root 722 B) and
not measurable from the journal by construction. Blast radius: boot-time
variance only; `resume=` path dormant (exactly one `PM: Image not found` per
boot, all 13 boots except the oldest). Action: only if the dwell matters —
operator probes offline (rd.debug / console watch); the discriminating probes
are all outside this lane's province.

**J4 — mechanism: the self-init *failed with EACCES*; there is no contradiction
to resolve.** `/etc/default/limine` (readable, 644): `ESP_PATH=/boot`,
`ENABLE_UKI=yes`, `MAX_SNAPSHOT_ENTRIES=5`, `BOOT_ORDER="*, *fallback,
Snapshots"` — and **no `SNAPPER_CONFIG_NAME`**, which is exactly what the P3
line says to add. Journal, same second (boot 0, 11:02:05):
`limine-snapper-watcher: Directory /.snapshots does not exist … triggering
initialize`; `Creating a Snapper config named 'root' and single root snapshot`;
`Btrfs.cc(createConfig):139 create subvolume failed,
btrfs_util_create_subvolume_fd() failed, errno:13 (Permission denied)`;
`Creating config failed (creating btrfs subvolume .snapshots failed)`. State
now: `/.snapshots` absent; `snapper list-configs` header-only, rc=0;
`/etc/snapper/configs/` empty; unit enabled, `is-active` = inactive (oneshot,
last ran at boot). Unit properties (`systemctl show`): `User=root`,
`CapabilityBoundingSet=cap_sys_admin`, `ProtectSystem=no`, `ProtectHome=yes`,
`ReadWritePaths=/tmp`, `NoNewPrivileges=yes`. Denial-vector narrowing done
read-only: `btrfs property get -ts /` → `ro=false` (the root subvolume is *not*
read-only) and the tree is not remounted read-only (`ProtectSystem=no`), the
caller is root with CAP_SYS_ADMIN — none of the obvious candidates explains
errno 13. `btrfs subvolume show/list` as non-root → EPERM (elevation). Blast
radius: no snapshots ever existed on this install (boot 0 = install), so U1's
"standing exposure" is exact, and `MAX_SNAPSHOT_ENTRIES=5` is configured for a
list that can never populate. Action (P0): operator
`sudo snapper -c root create-config /` (or fix the unit's environment), set
`SNAPPER_CONFIG_NAME="root"`, restart the sync unit, re-audit; then the
vector hunt (`sudo btrfs subvolume create /.snapshots` as a discriminating
test) is blocked → §6.

## 4. Update-safety class

**U1 — same root cause as J4; exposure quantified.** btrfs layout measured
(`findmnt -t btrfs`): `@` (subvolid 256, `/`), `@home` (257), `@log` (258),
`@pkg` (259); no `.snapshots` subvolume mounted anywhere; `snapper
list-configs` header-only. Any wave on this host is snapshot-less. Action: P0
item 1; then record the acceptance or the fix in the update-safety note.

**U2 — mechanism: the mirror is the staleness; the "no updates" state is not
evidence about upstream.** `/etc/pacman.d/mirrorlist` contains exactly **one**
active server — `https://stable-mirror.omarchy.org/$repo/os/$arch` — used by
core/extra/multilib. Sync dbs: birth 2026-10-11 12:54:13.542054496 (all four),
but file mtimes core/extra/multilib = **2026-09-08 15:23**, omarchy.db =
2026-10-11 10:16 (fresh). Content checks: `pacman -Si bash` Build Date
2026-06-10, `glibc` 2026-08-10; `pacman -Qu` rc=1 empty; `-Sup` 0 lines;
`checkupdates` absent. [observed] the mirror served 33-day-old framework dbs
while the omarchy db was current; [inference] refresh-on-mirror-change is the
only thing that will move the arm vocabulary. Blast radius: every prep decision
is against a stale index; a mirror switch (or `-Syy`) can bring 33+ days of
deltas at once — precisely the wave shape the update-safety note warns about.
Action: P0 item 2; upstream delta itself stays blocked (state-changing/network →
§6).

**U3 — mechanism: a kernel wave means initramfs + UKI + DKMS in one
transaction.** Measured inputs: `MODULES=()` + drop-ins
`nvidia.conf` (`MODULES+=(nvidia nvidia_modeset nvidia_uvm nvidia_drm)`),
`omarchy_hooks.conf` (`HOOKS=(base udev plymouth keyboard autodetect microcode
modconf kms keymap consolefont block encrypt filesystems fsck btrfs-overlayfs)`,
`FILES+=(/etc/vconsole.conf)`), `omarchy_resume.conf` (`HOOKS+=(resume)`),
`thunderbolt_module.conf`; `/etc/pacman.d/hooks/` holds
`90-mkinitcpio-install.hook` (653 B, md5 `1be6095b…`) which **diverges** from
the packaged `/usr/share/libalpm/hooks/90-mkinitcpio-install.hook` (638 B,
`4d8d6497…`): Target `usr/lib/modules/*/modules.builtin` (vs `*/vmlinuz`) and
Exec `limine-mkinitcpio-install` (vs `mkinitcpio install`); plus `99-limine.hook`
(copies limine EFI binaries into the ESP) and the dkms hooks
(70/71/60/90-set). [inference] on a same-name collision the `/etc` hook wins
(pacman's documented precedence for earlier hook dirs); [unknown] the effective
hook is not observable read-only → verify item. Blast radius: a kernel wave
writes the ESP (U6 mask), rebuilds initramfs/UKI, and re-runs dkms — the exact
path that produced D2's stale row. Action: post-wave checklist — `dkms status`
shows the new kernel's nvidia build *before* reboot; confirm the UKI/ESP was
rewritten (root).

**U4 — mechanism: one fresh channel, no signature requirement, and it is the
source of the version asymmetry.** `grep -v E '^#' /etc/pacman.conf`:
`HoldPkg = pacman glibc`, `SigLevel = Required DatabaseOptional`,
`LocalFileSigLevel = Optional`, `DownloadUser = alpm`, `ParallelDownloads = 5`,
`[omarchy] SigLevel = Optional TrustAll` + `Server =
https://pkgs.omarchy.org/stable/$arch`; no `IgnorePkg/IgnoreGroup/NoUpgrade/
NoExtract/HookDir` keys at all. `/var/lib/pacman/sync/` shows only omarchy.db
fresh (Oct 11 10:16) while core/extra/multilib are Sep 8 — i.e. the
unauthenticated channel is the only channel with current content today.
Blast radius: the trust decision gates U2/U5 and any omarchy-package wave.
Action: written accept-or-rescope decision before the next wave.

**U5 — mechanism: a version asymmetry with no pin.** `pacman -Q 1password-beta`
= `8.12.42_32.BETA-32`; `pacman -Si 1password-beta` → Repository **omarchy**,
Version `8.12.42_32.BETA-1`, Build Date 2026-10-07. No pins/holds
(`pacman-conf IgnorePkg IgnoreGroup NoUpgrade NoExtract` → none; only HoldPkg).
[observed] pacman's version comparison keeps the installed BETA-32 during plain
`-Syu`; `-Suu` explicitly downgrades (r3: 579.18 MiB rewrite); `-Syy` would
re-fetch the stale dbs. Blast radius: one careless flag rewrites half a GB and
loses the beta line. Action: standing rule (P0 item 4); optionally pin by hand
if the channel later offers a "newer" build that is not the beta line.

**U6 — mechanism measured: the gate is a *mount mask*, not on-disk
permissions.** `/etc/fstab:18` mounts the ESP (`UUID=86D8-C3F6 /boot vfat
… fmask=0077,dmask=0077 …`); `findmnt -no OPTIONS /boot` reproduces it; `stat
/boot` → `700 root:root`. Consequences measured elsewhere: `ls /boot` rc=2
non-root; `/boot/amd-ucode.img` unhashable (P2's 4 permission-denied rows).
[observed] the 700 is an artifact of the mount options (omarchy/Arch ESP
default), not file corruption; a root shell is unaffected. Blast radius:
non-root pre-wave checks of the ESP are impossible (limine config, UKI, cores
of the boot chain), and P2's sweep rows persist until a root run. Action: P0
item 3 (root pre-verify before any kernel/firmware/limine wave); optionally
relax the mask if non-root reads are wanted — design decision, not a defect.

**U7 — mechanism: the root hook drops privilege by design.** Hook
(`/etc/pacman.d/hooks/walker-restart.hook`): Targets `walker`, `walker-debug`,
`elephant*`; `When = PostTransaction`; `Exec = /home/vgpnk/.local/share/omarchy/
bin/omarchy-restart-walker`. The script (mode 755 vgpnk:vgpnk, 709 B) checks
`EUID == 0` and then `systemd-run --uid="$SCRIPT_OWNER"
--setenv=XDG_RUNTIME_DIR=/run/user/$USER_UID bash -c "…"` — the root context
runs only `stat`, `id` and `systemd-run`; the restart executes as the script
owner (vgpnk). Historical use: exactly one `walker-restart.hook` run in
`/var/log/pacman.log`. [observed] no privilege escalation for a writer of the
script (any injected code runs as the writer), and the failure mode is a printed
"RESTART MANUALLY" message if the user manager is absent. Blast radius: dormant
— the 14 target packages have no update channel (P4). Action: kagi/operator
review of the trust *shape* only; measurement found nothing to repair.

**U8 — mechanism: contention now comes from crash-looping sibling workloads,
not ffmpeg.** Live snapshot 13:24: load 0.63/0.90/1.38 on 32 CPUs; `ffmpeg` 0,
`godot` 0, `node` 1 at that instant — but the window carried 244 cores in ~2 h,
30 G RAM with a 28.5 G session peak and 34.2 G swap peak, and a session
SIGKILL cascade (§5 N4). [inference] wave windows should be chosen by crash
cadence and memory headroom, not by a process-name census. Action: schedule
waves when `uptime` load is low *and* the coredump rate is quiet; keep the
census as the gate receipt.

## 5. Round-4-new classes (the r3 §6 errata, now triaged)

**N1 — driver-firmware: USB Audio endpoint-setup rejections.** 64 kernel
errors `usb 8-12: Incompatible EP setup for 0x8` (12:30:08–13:03:04 local,
63/64 inside the first five minutes; 5 boot-time enumeration lines excluded);
device `0db0:cd0e` "Generic / USB Audio", 8 interfaces `1.0–1.7`, `1.0–1.6`
bound to `snd-usb-audio`, `1.7` to `usbhid`; still enumerated; `card0` = "Audio"
present; PipeWire 1.6.8 exposes it (sinks: S/PDIF-Output (default), Front
Headphones, Speakers; sources: Microphone, Line Input) → **functional now**.
Independent second symptom measured at 13:20:36: `xhci_hcd 0000:77:00.0: PM:
suspend_common(): xhci_pci_suspend returns -110` + `can't suspend
(hcd_pci_runtime_suspend returned -110)` — a runtime-suspend timeout on the same
controller family. [observed] transient device/driver quirk; [inference] repeat
EP-setup retries by the audio stack during a 5-minute window; [unknown] trigger
and recurrence. Blast radius: transient audio-path risk + err-count mass;
watch item, no repair owed by this lane.

**N2 — service: pipewire client burst.** 10 × `pipewire` + 3 ×
`pipewire-pulse` err entries, 12:29:03–13:09:32 local: client-side failures
`can't find protocol 'PipeWire:Protocol:Native': Operation not supported`,
`could not load mandatory module "libpipewire-module-fallback-sink"`, `failed to
create context`; later `D-Bus name org.pulseaudio.Server already taken` and one
`spa.alsa: '_ucm0001.hw:Audio,3': playback open failed: Device or resource
busy`. All failing PIDs are one-shot and already gone; the daemon is healthy
(`wpctl status` shows it, 1.6.8; `pipewire.service`/`pipewire-pulse.service`
active, NRestarts=0, ActiveEnter 13:11:08 — i.e. restarted *with the new
session*, not long-lived since boot as the erratum assumed, and not flipped by
systemd). [inference] the failing instances ran with a broken pipewire *module
path* (their own protocol module could not be found) — a client-environment
problem, not a daemon fault; the launcher is not in the journal and `bwrap` is
not present now → [unknown] who launched them. Blast radius: transient
(verified functional after); err-count contribution 13.

**N3 — service: coredump growth and new entrants** — blender (7, SIGSEGV) and
love (7, SIGABRT) joined; see J1. Handoff: blender → whoever ran it; love →
game-dev-2d corpus (`r74-boundary/cells`).

**N4 — service: user session restart at 13:10:59, not an OOM kill.** Sequence
(measured, system journal): 13:10:59.345 portal interface line → .346
`sddm-helper[1567]: [PAM] Closing session` → .360 `session-1.scope: Deactivated
successfully` → .361 `sddm-helper exited with 9` + `Session 1 logged out` →
.380 `user@1000.service: Main process exited, code=killed, status=9/KILL` →
.381 `Failed with result 'signal'`; greeter line at .365, session `c1` (sddm)
at .379; the greeter's compositor then SIGSEGV'd
(`Process 1203102 (Hyprland) of user 964`, cmdline `Hyprland --watchdog-fd 4
--config /usr/share/sddm/hyprland.conf`, `SEGV_MAPERR`, session-c1.scope); new
user session 4 at 13:11:07.301 (autologin), autostart functional (1Password,
grok-bot, waybar, terminal all started). OOM ruled out by measurement: no new
`Out of memory` line in the ring, memcg `oom_kill 1` lifetime; the systemd line
`user-1000.slice: The kernel OOM killer killed some processes in this unit` at
13:10:59.400 is the cgroup-teardown annotation of the Oct 13 kill, not a new
event. [unknown] the initiator of the session end (no journal line names it;
candidates: operator logout, watchdog path, external signal). Blast radius:
8-second desktop outage, stale `/run/user/1000` generator units, and the
failedhist flip (N6).

**N6 — service: the census failed-history arm flipped 0 → 8 and its trigger is
this restart.** Reproducing the census's own match
(`grep -aE '"MESSAGE":"[^"]*(Failed to |entered failed state|Failed with
result)'`) → exactly 8 matches, all
`systemd-xdg-autostart-generator[…]: Failed to create unit file
'/run/user/1000/systemd/generator.late/app-…@autostart.service': File exists`,
timestamped 13:11:07.32 (the new session's first generator pass). Mechanism:
the user manager was SIGKILLed (N4) before it could clean `/run/user/1000`, so
the new manager's xdg-autostart generator collided with the stale generated
units; the collision is refused and the stale units stay. Blast radius:
measured *none functional* — 1Password, grok-bot, waybar, terminal all started
in session 4; the risk is stale unit content if `.desktop` files ever change.
Reading caveat for the round: the census's name extraction greps whole JSON
lines, so unit tokens come from entry *metadata* too (`init.scope`, `-.slice`,
`user@1000.service` in the census name list are cgroup/slice fields, not
failing units). Action: none for the host; worth a census note (name-extraction
should read `.MESSAGE` only).

**N5 — driver-firmware: sr0 recurrence** — folded into D1(a): the burst is no
longer boot-only; r3's claim superseded (§9).

## 6. Blocked rows — mechanism blocked, with the exact elevation needed

Five rows need elevation, one needs the shape-only rule. None of them was
opened during this lane (discipline, §"the elevation call"). `sudo -n true` =
rc=0 measured → each command below is one passwordless step for the operator.

| row | what is blocked | exact command (operator) |
|---|---|---|
| P2 | root-side verify values for 32 calc + 4 perm rows | `sudo pacman -Qkk > /tmp/qkk-root.txt 2>&1` |
| J1 | per-crash stack reason for godot/love/blender classes (core files are 640 root:systemd-coredump) | `sudo coredumpctl info <pid>` for a named core; `sudo coredumpctl list` for the set |
| J3 | crypttab/keyfile/resume vector (also shape-only by fleet rule) | none that reads content; if the dwell matters: operator adds `rd.debug` / watches the console — config change, out of province |
| J4 | the EACCES denial vector (candidates narrowed: ro=false, ProtectSystem=no, root+CAP_SYS_ADMIN) | `sudo btrfs subvolume create /.snapshots` (discriminating test), `sudo systemd-run -p CapabilityBoundingSet=CAP_SYS_ADMIN --wait …` to isolate the unit environment |
| U1 | subvolume inventory incl. any hidden `.snapshots` | `sudo btrfs subvolume list /` (non-root: EPERM, measured) |
| U2 | upstream delta behind the stale mirror | `sudo pacman -Sy` (state-changing → operator-only), then re-run `-Qu`/`-Sup` or install `pacman-contrib`+`checkupdates` |
| P5 | contents of the 3 alpm download dirs | `sudo ls -la /var/cache/pacman/pkg/download-*` |
| J2 | core removal (no vacuum in this build) | root file operation after owners have what they need |

## 7. Unknowns register (new/updated, with owners)

1. The reader process that probes sr0 at session transitions (D1a) — probe:
   `udevadm monitor`+ftrace/audit at the next transition; owner: operator or a
   later lane with the right tooling.
2. OOM victim's parent workload (D1b): the killing cgroup is
   `app-graphical.slice/…/app-Hyprland-xdg-terminal-exec-…scope`; which command
   that scope ran is not in the ring — owner: GPU/game-dev workstream.
3. The initiator of the 13:10:59 session end (N4) — owner: operator.
4. The pipewire client launcher (N2) — owner: operator/fleet-app owners.
5. The precise J4 EACCES vector (narrowed, not closed) — operator (elevated
   reproduction) or upstream limine-snapper-sync.
6. Whether `env python3`→`/bin/python3` was written by an omarchy install step
   (no script referencing it found) — owner: omarchy source (P3).
7. Effective initramfs dwell cause (J3) — owner: operator; no journal evidence
   can exist by construction (recorded, not merely missing).
8. Effective kerchunk retention limits (J2) — merged config is defaults-only;
   owner: derivation/operator (r3's unknown #10 stands).
9. Which hook wins the `90-mkinitcpio-install.hook` name collision (U3) —
   verify on the next wave's pacman output; owner: next wave executor.
10. r3's unknowns that remain open and unowned by this note (GSP selection,
    UPS existence, ai-usage env-file contents, firmware atimes) — unchanged.

## 8. Spot-checks (independent re-derivations inside this note)

1. **Arithmetic closure of the anchor**: kernel 139 = 40 + 30 + 64 + 2 + 1 + 1
   + 1 and journal 407 = 244 + 139 + 24, each term from a separate command
   (`jq`/`grep` message classes), matching the gate's composition fields at
   16:28:00Z.
2. **Content-integrity claim of P1**: `sha256sum` of both 1Password helpers
   equals the `sha256digest` recorded in
   `/var/lib/pacman/local/1password-*/mtree` (`8d029d2c…`, `000782e7…`) —
   metadata-only drift verified against the package's own recorded bytes.
3. **P3/P4 provenance cross-check**: the cached package's file digest
   (`38532d5f…`) equals power-profiles-daemon's mtree digest while the live file
   differs only in the shebang; and `offline.db` carries `elephant-2.21.0-1`,
   the exact installed version — two independent channel claims verified
   against two different db artifacts.

## 9. Errata / pending (append-only)

- 2026-10-14 — **supersedes r3's D1 claim "no record since the boot window /
  accepted noise floor" for the sr0 class**: a second burst (115 lines) fired
  at 13:10–13:11 -03 during a session restart. r3's wording stands as written;
  this note records the change, it does not rewrite the report.
- 2026-10-14 — **supersedes r3's J5 receipt "failed-service history — 0 unit
  failures"** for the current census arm: `failedhist=8` at 16:19:56Z and
  16:28:00Z, driven by the 13:11:07 generator collisions (N6). No *unit*
  failure occurred; the arm fires on generator messages (its own class regex).
- 2026-10-14 — **supersedes the r4-2 erratum's "pipewire active since boot"**:
  both pipewire units re-entered active at 13:11:08 with the new session
  (NRestarts=0). The 12:29–12:30 client burst therefore ran against the
  pre-restart daemon.
- 2026-10-14 — **J4 reframed**: r3 called it "self-claim vs empty configs";
  the measured truth is a failed auto-init (EACCES) — the claim was an attempt,
  not a false statement.
- 2026-10-14 — **LOG.md entry owed** for this note (`AGENTS.md:3`): this seat
  wrote only this file; the round scribe appends the round-4 log entry.
- Pending: the six blocked rows are operator-executable today (passwordless
  sudo measured); none was executed by this lane.

## Appendix A — executor re-run set (read-only, no elevation)

```bash
bash tools/tsukuroi-census.sh --selftest && bash tools/tsukuroi-census.sh
journalctl -b -p err -o json --no-pager | wc -l
journalctl -k -b -p err -o json --no-pager | jq -r '.MESSAGE' | sed -E 's/[0-9]+/N/g' | sort | uniq -c | sort -rn | head
coredumpctl list --since "2026-10-13 10:57:58" --json=short --no-pager | jq -r '.[]|[.exe,.signal]|@tsv' | sort | uniq -c | sort -rn
cat /etc/pacman.d/mirrorlist | grep '^Server'; stat -c '%y %n' /var/lib/pacman/sync/*.db
bsdtar -tf /var/lib/pacman/sync/offline.db | grep -c '^elephant'   # [offline] has no pacman.conf section — query the db file directly, `pacman -Sl offline` returns 0
sha256sum /usr/bin/op /opt/1Password/1Password-BrowserSupport
zcat /var/lib/pacman/local/1password-cli-*/mtree | grep 'usr/bin/op'
bsdtar -xOf /var/cache/pacman/pkg/power-profiles-daemon-0.30-1-x86_64.pkg.tar.zst usr/bin/powerprofilesctl | sha256sum; diff <(bsdtar -xOf … usr/bin/powerprofilesctl) /usr/bin/powerprofilesctl
snapper list-configs; ls -ld /.snapshots; btrfs property get -ts /
systemctl show limine-snapper-sync.service -p User -p ProtectSystem -p ProtectHome
journalctl -b --no-pager -o short-iso-precise | grep -aE 'Incompatible EP setup|xhci_pci_suspend|xhci_pci_runtime_suspend' | head
journalctl -b -o short-iso-precise --no-pager | grep sr0 | awk '{print substr($1,1,16)}' | uniq -c
systemd-analyze cat-config systemd/coredump.conf | grep -vE '^\s*#|^\s*$'
timeout 280 pacman -Qkk > /tmp/qkk.txt 2>&1; tr '\r' '\n' < /tmp/qkk.txt | grep -ciE 'failed to calculate|permission denied'
df -h /; uptime; du -sh /var/lib/systemd/coredump
```

## Erratum (2026-10-19, fleet round 1) — D1: Bare -Sy is not a safe refresh route
Superseded (`corpus/knowledge/degraded-triage-r4.md:90,524`): “fix/replace the single mirror, then `-Sy` and re-run `-Qu`/`-Sup`”; the operator-only `sudo pacman -Sy` route is repeated at :524.
Correction: use pacman-contrib's `checkupdates` for a safe installed-package update check, or a complete `pacman -Syu`; never advise bare `pacman -Sy`.
Source: S010 https://wiki.archlinux.org/title/System_maintenance § Avoid certain pacman commands: “never run `pacman -Sy`; instead, always use `pacman -Syu`.” S010 § Partial upgrades are unsupported: `checkupdates` safely checks installed-package updates without a system update.
[obs] Host `/var/log/pacman.log`, re-opened 2026-10-19: `grep -nE 'pacman -Sy ' /var/log/pacman.log` → line 1405 (`2026-10-11T12:54:13-0300`, `pacman -Sy --noconfirm fuse2`) and line 2287 (`2026-10-18T14:11:00-0300`, `pacman -Sy --noconfirm`). `grep -nE 'pacman -Syu|Running .pacman -Syu' /var/log/pacman.log` → line 1414 (`2026-10-11T16:13:19-0300`); the first gap is 3h19m06s, while no later full `-Syu` is recorded after line 2287.
S032 is own-work `/var/log/pacman.log`, lines 1405, 1414, 2287; the ArchWiki citation above is S010.

## Erratum (2026-10-19, fleet round 1) — D2: HookDir precedence and winner resolved
Superseded (`corpus/knowledge/degraded-triage-r4.md:370-371,546-547`): “pacman's documented precedence for earlier hook dirs”; “Which hook wins the `90-mkinitcpio-install.hook` name collision”.
Correction: S007 documents later HookDir entries taking precedence; S008 says a same-name file in a higher-priority hook directory overrides the prior hook. The host's `/etc/pacman.d/hooks/` entry wins over `/usr/share/libalpm/hooks/`; the collision unknown was answered by the 2026-10-11 log.
Source: S007 https://man.archlinux.org/man/pacman.conf.5 § OPTIONS, HookDir: “hooks in later directories taking precedence over hooks in earlier directories.” S008 https://man.archlinux.org/man/alpm-hooks.5 § OVERRIDING HOOKS: “Hooks may be overridden by placing a file with the same name in a higher priority hook directory.”
[obs] Re-opened 2026-10-19: `pacman-conf HookDir` → `/etc/pacman.d/hooks/`; `grep -Hn '^Exec' /usr/share/libalpm/hooks/90-mkinitcpio-install.hook /etc/pacman.d/hooks/90-mkinitcpio-install.hook` → packaged `Exec = /usr/share/libalpm/scripts/mkinitcpio install`, override `Exec = /usr/share/libalpm/scripts/limine-mkinitcpio-install`; `grep -n -A1 "running '90-mkinitcpio-install.hook'" /var/log/pacman.log` → line 1989 hook run, line 1990 `Building UKI for linux (7.2.3-arch1-3)`.

## Erratum (2026-10-19, fleet round 1) — D3: errno 13 remains an inference
Superseded (`corpus/knowledge/degraded-triage-r4.md:321-325`): “errno:13 (Permission denied)” remained without the DAC-mode/capability pair.
Correction [inf]: see `corpus/knowledge/snapper-eacces-mechanism.md` §§Current host evidence and Falsifier. The measured root mode and unit capability bound support the proposed DAC explanation, but it is not proved until the operator-only falsifier is run; that falsifier was not run in this read-only wave.
Source: S027 https://man.archlinux.org/man/capabilities.7 § CAP_DAC_OVERRIDE: “Bypass file read, write, and execute permission checks.” S028 https://man.archlinux.org/man/systemd.exec.5 § CapabilityBoundingSet=: “Capabilities listed will be included in the bounding set, all others are removed.”
[obs] Re-opened 2026-10-19: `stat -c '%a %U:%G' /` → `555 root:root`; `systemctl cat limine-snapper-sync.service | grep -n CapabilityBoundingSet` → `14:CapabilityBoundingSet=CAP_SYS_ADMIN`; `journalctl --no-pager -o short-iso -g 'create subvolume failed' | grep -c 'errno:13'` → `8`.

## Contract keys (appended 2026-10-19, fleet round 1)
source: own-work — census and one-level-deeper read-only package/service/driver/journal probes on host `plazir27`, 2026-10-14; S031 `tools/tsukuroi-census.sh`; S032 `/var/log/pacman.log` re-opened for D1/D2 on 2026-10-19.
verified-at: 2026-10-14 (the triage capture window; D1/D2/D3 host evidence and public references re-opened 2026-10-19).
recheck: 30d; procedure: Appendix A plus `bash tools/tsukuroi-census.sh --selftest && bash tools/tsukuroi-census.sh`; include the operator-only D3 falsifier only when the operator elects to run it.
supersedes the pointer-only recheck: line above.


## R18-FRESHNESS — sibling current-use restatements (2026-10-20)

Sources S060, S051 and S052. This appended correction supersedes the current-use readings listed below and every repeated current-use restatement of the same premise in this file. Historical measurements remain intact. No package, service, rebuild, boot or rollback action is authorized.

- R18-FRESH-SUPPLEMENT-34: prior locus `| U1 | config | same root cause as J4 + btrfs layout `@/@home/@log/@pkg`, no `.snapshots` anywhere (§4) | no rollback net for any wave on this host | subvolume inventory: elevation | P0 |`. Now: configuration names home/root and SNAPPER_CONFIGS="root home" are observed; do not repeat the configure-or-snapshotless instruction as an established missing-config finding. Snapshot inventory and restoration remain unverified by R18; re-audit, not create-config, is the remaining evidence task [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:75-81]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:80.

- R18-FRESH-SUPPLEMENT-35: prior locus `interrupted/failed download phases; `paccache`/`checkupdates` absent`. Now: S060 lists pacman-contrib-1.13.1-1 in local metadata and resolves /usr/bin/paccache; old package/paccache-absence guidance is not current. This capture does not query or resolve checkupdates, so its availability and any use elsewhere remain unknown; no installation is advised [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:82-86]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:83.

- R18-FRESH-SUPPLEMENT-36: prior locus `mem / 34.2 G swap, `zswap.enabled=0` on the cmdline. Blast radius: any`. Now: zswap runtime enabled isY, maximum pool percentage25 and compressorzstd; cmdline includes zswap.enabled=1. Historical pressure events are not attributed to this later state [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:8-15]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:12.

- R18-FRESH-SUPPLEMENT-37: prior locus `wave. Action: `sudo dkms remove nvidia/610.57.04 -k 7.1.4-arch1-1`, then verify`. Now: current capture lists nvidia/615.78.08 for6.18.57-2-lts and7.2.11-arch1-1, plus7.2.3-arch1-3 with missing built modules. No7.1.4 row is listed, so the old610.57.04/7.1.4 removal action is stale and must not be replayed. No removal or reboot clearance is given [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:5-7, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:92-96]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:95.
