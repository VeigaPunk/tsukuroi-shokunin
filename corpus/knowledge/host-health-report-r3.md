# Host-health report — plazir27 (round 3 e2e, TSUKUROI-R3-3)

source: live read-only probes 2026-10-14 11:39–11:58 -0300 (UTC 14:39–14:58),
host `plazir27`, user `vgpnk` (non-root); gate `tools/tsukuroi-census.sh`
census-v2 (md5 `41953ee9f2099281c91759249fe8708f`, 976 lines); the four plane
notes + the update-safety note (md5s §5); scratch `/tmp/tsukuroi-r3-3-work/`
(ephemeral — every capture below is stored there).
verified-at: 2026-10-14 (this report's own runs; every number carries its
command and capture time; counts drift live — a coredump storm is running).
recheck: Appendix A command set; `bash tools/tsukuroi-census.sh --selftest &&
bash tools/tsukuroi-census.sh`.

**What this is.** The lane's end-to-end SHONEN task, executed start-to-finish in
one sitting: the settled gate `tsukuroi-census.sh` (census-v2, four planes),
driven together with the corpus's four plane notes and the update-safety note
into one host-health snapshot. Contract per the round plan
(`plans/round-3.plan.md:3-12`): every DEGRADED finding carries its measured
evidence (command + output shape) and its exact operator unblock action;
HEALTHY planes get one-line receipts. The lane detects and reports — it never
installs, upgrades, removes, or restarts (`PROVINCE.md:16-17`); every action
below is operator-side.

## 0. Verdict board

| # | Plane | Verdict | Receipt / pointer |
|---|---|---|---|
| 1 | packages (pacman) | `DEGRADED` | sample drift=2 pair + foreign=16; full-sweep residues — detail §2.1 |
| 2 | systemd user units | **`HEALTHY`** | receipt: `running`, 0 failed units, 1/1 timer scanned `Result=success` (`ai-usage.timer`) — census line, 14:57:13Z |
| 3 | drivers (nvidia / kernel ring) | `DEGRADED` | `kerr=38` noise floor + DKMS residue; GPU present and answering — detail §2.3 |
| 4 | journal / boot | `DEGRADED` | `err=251 (coredump=211 kernel=38 other=2)`; `failedhist=0`; timers armed — detail §2.4 |
| 5 | update-safety | `DEGRADED` (arm vocabulary) | `-Syu` now `INERT`; after refresh `UNKNOWN-UPSTREAM` + `REQUIRES-PREP`; `-Suu`/`-Syyu` `DO-NOT` — detail §2.5 |

Composed rollup: `TSUKUROI_CENSUS: DEGRADED` (exit 1). No plane `BLOCKED`; one
plane `HEALTHY`. The two findings that most deserve operator eyes:
**no rollback net** (U1/J4) and the **live coredump storm** (J1).

### 0.1 Finding → action index (20 pairs)

| ID | Finding (verdict impact) | Exact operator unblock action |
|---|---|---|
| P1 | 1Password pair sample drift (census DEGRADED) | Root-verify the setgid group surfaces; accept as vendor convention or reinstall both packages |
| P2 | Full-sweep non-root artifacts, 36 lines | Root re-run of the full sweep — expected to clear |
| P3 | `powerprofilesctl` content mismatch | Decide deliberate omarchy patch vs drift; if drift, reinstall `power-profiles-daemon` |
| P4 | Foreign set, 16 packages | Record accepted baseline (or remove); `-Syu` never updates them |
| P5 | Cache 8.6 G / 3 alpm temp dirs [advisory] | Optional prune (`pacman-contrib`+`paccache`); root inspect of temp dirs |
| D1 | `kerr=38` (sr0 / OOM / TDX) | Conditional: media check only if sr0 recurs; memory review if OOM recurs; else accepted noise floor |
| D2 | Stale DKMS `7.1.4-arch1-1` row | `sudo dkms remove nvidia/610.57.04 -k 7.1.4-arch1-1`, then re-check `dkms status` |
| D3 | Unowned DKMS module | No repair (by design); verify via `modinfo -F version` = 610.57.04 |
| J1 | Coredump storm (211 events, live) | Cross-domain: hand to owning workstreams; re-count with the census command |
| J2 | Coredump disk footprint 3.9 G | Optional prune after crash owners have what they need (no `coredumpctl` vacuum in this build) |
| J3 | Bimodal boot dwell (12 s → 2 h 58 m) | Operator probe of the LUKS/crypttab path if dwell matters; mechanism stays [unknown] |
| J4 | `limine-snapper-sync` self-claim vs empty configs | Configure Snapper + `SNAPPER_CONFIG_NAME` (or accept snapshot-less); re-audit |
| U1 | No rollback net | Same as J4 — snapshot-less is the standing exposure for any wave |
| U2 | Upstream delta unmeasurable read-only | Operator `-Sy` or `pacman-contrib`+`checkupdates`; prep list (a–d) before any wave |
| U3 | Kernel/DKMS rebuild coupling | After any kernel wave: verify `dkms status` for the new kernel before reboot |
| U4 | Trust surfaces (`[omarchy]` TrustAll; local-file optional) | Accept or re-scope the channel |
| U5 | Downgrade trap (`1password-beta` ahead) | Use plain `-Syu` only; never `-Suu`, never `-Syyu` |
| U6 | `/boot` privilege gate | Operator root pre-verify (`sudo ls /boot`, `sudo bootctl status`) before a wave |
| U7 | `walker-restart.hook` root-exec surface | kagi / operator review of the user-owned script run as root |
| U8 | Live workload contention | Schedule waves in a quiet window (75×ffmpeg-class workloads during round time) |

Receipts (no action owed): systemd user plane HEALTHY (§2.2); journal
failed-history and timer arms HEALTHY (§2.4 receipts).

## 1. The gate run (census-v2, four planes)

```bash
bash tools/tsukuroi-census.sh --selftest    # rc=0
bash tools/tsukuroi-census.sh              # rc=1
```

Selftest, last line verbatim (26 cases = 17 legacy + 9 journal-plane; each
case asserts exit code + verdict + evidence substring + fixture byte-unchanged;
capture `selftest-v2.out`):

```
TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)
```

Live run, verbatim (capture `census-live-v2.out`; exit map 0 HEALTHY | 1
DEGRADED | 2 BLOCKED, worst plane wins):

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T14:57:13Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16; pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=38 (oom=1 io=35 gpu=0 other=2) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=251 (coredump=211 kernel=38 other=2); failedhist=0; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

Revision context: census-v2 (TSUKUROI-R3-2) adds the journal/boot plane to the
settled v1 three-plane gate; the three legacy planes read identically in the
pre-v2 snapshot taken at 14:39:26Z (`census-live.out`, v1 md5
`7a3d3b94ecd73fbe1a9a98e9dc88b92f`) and in v2 — the drift numbers are stable
across the window. v2 is authoritative here. The journal plane deliberately
does **not** probe `coredumpctl` (table parsing is a measured trap; the
`systemd-coredump` entry class is the storm signal) — the cross-count lives in
`journal-boot-plane.md` §2.2 and both agree within drift.

**Read-only check (measured).** Live mode creates no files; before/after
`git status --short` identical (only the round's own artifacts:
`tools/tsukuroi-census.sh` modified, `corpus/knowledge/journal-boot-plane.md`
and `plans/round-3.plan.md` new). The selftest writes only under its own
`/tmp/tsukuroi-r3-2-selftest.XXXXXX`. My scratch: `/tmp/tsukuroi-r3-3-work/`.

## 2. Detailed findings

### 2.1 packages — `DEGRADED`

**P1 — sample drift on the 1Password pair (census arm).** Evidence (11:39–11:41):

- census line: `drift=2[1password-beta,1password-cli]` (above).
- `pacman -Qkk 1password-beta 1password-cli` → rc=1, output shape:

```
warning: 1password-beta: /opt/1Password/1Password-BrowserSupport (GID mismatch)
warning: 1password-beta: /opt/1Password/1Password-BrowserSupport (Permissions mismatch)
warning: 1password-cli: /usr/bin/op (GID mismatch)
warning: 1password-cli: /usr/bin/op (Permissions mismatch)
1password-beta: 122 total files, 1 altered file
1password-cli: 7 total files, 1 altered file
```

- `stat -c '%a %U:%G %n' …` → `2755 root:onepassword-cli /usr/bin/op`,
  `2755 root:onepassword /opt/1Password/1Password-BrowserSupport`.

Reading: [observed] setgid helpers owned by vendor dynamic groups; [inference]
the group GID/mode delta is the 1Password packaging convention, not content
corruption (no non-backup SHA mismatch here; round-1 decomposition held the
same class). **Operator unblock:** root-verify — `sudo pacman -Qkk
1password-beta 1password-cli` (resolves the expected-value side) and `getent
group onepassword onepassword-cli`; if the delta stays inside the dynamic-group
class, record as accepted baseline; if unintended, reinstall the two packages
(operator). Note: census-v2 reports drift>0 as DEGRADED and has no
accepted-baseline mechanism — the finding stays in the verdict until repaired.

**P2 — full-sweep residues (census sample does not cover).** Evidence (11:44):

- `timeout 240 pacman -Qkk` → rc=1, wall **17.4 s**, **1332 raw lines**;
  normalized with `tr '\r' '\n'` → 1185 summaries: **18 packages with ≥1
  altered** (names below), 86 `backup file:` lines, **32 × failed-to-calculate
  SHA256**, **4 × Permission denied**.
- altered names — command: `grep -E '^[^:]+: [0-9]+ total files, [1-9][0-9]*
  altered' | sed -E 's/: [0-9]+ total files.*//' | paste -sd, -`:
  `1password-beta,1password-cli,amd-ucode,asdcontrol,audit,cups,cups-pdf,dbus,filesystem,java-runtime-common,libutempter,openssh,power-profiles-daemon,shadow,sudo,systemd,ufw,yaru-icon-theme`.
- backup diffs are benign (rc stays 0 for them; glibc/pambase prove the
  semantics — `package-state-plane.md:146-151`); the 36 non-root artifacts need
  a root run to resolve (`package-state-plane.md:184-190`: kinds, paths).

**Operator unblock:** `sudo pacman -Qkk > /tmp/qkk-root.txt 2>&1` (root view;
expected to clear the failed-calc / permission series); classify with the
decision table at `package-state-plane.md:217-226`.

**P3 — `powerprofilesctl` content mismatch.** The one true content signal in
the sweep (mtime+size+SHA all differ, package `power-profiles-daemon`).
[unknown] deliberate omarchy patch vs drift. **Operator unblock:** compare
against `pacman -Si power-profiles-daemon` (channel copy) and the omarchy
patch surface; decide patch (record) vs drift (reinstall the package).

**P4 — foreign set, 16 packages** (`pacman -Qm | wc -l` = 16, 11:41). Shape:
13 × `elephant-*` + `omarchy-walker` (meta) + `android-apktool-bin` +
`obsidian-cli-inspector`. [observed] `-Syu` covers none of them; provenance:
yay caches exist for apktool/obsidian; the elephant family is in no synced repo
(`pacman -Si elephant` → not found) and its channel is [unknown]
(`package-state-plane.md:42-71`). **Operator unblock:** record the accepted
baseline for the family (or remove). Risk note: a soname bump in their linked
libs can break them silently (`update-safety-note.md:301-306`).

**P5 — hygiene [advisory, not a census arm]:** cache `8.6 G` (`du -sh
/var/cache/pacman/pkg`, 11:45; ≥ — 3 root-only `download-*` dirs excluded),
`paccache`/`checkupdates` absent (`command -v` rc=1). **Operator unblock:**
optional — `pacman-contrib` + `paccache` (operator-side), root inspect of the
3 alpm temp dirs.

### 2.2 systemd user units — `HEALTHY` (receipt)

Receipt (14:57:13Z census + 11:39 re-probe): `systemctl --user
is-system-running` → `running`; `--failed` → `0 loaded units listed.`;
`show ai-usage.timer -p Result --value` → `success`; `list-timers --all` → 1
timer, last 11:40:30, next 11:45:30. No action owed. Latent, intent-[unknown]
side-findings (not defects, from `systemd-user-plane.md:88-102`):
`omarchy-battery-monitor.timer` disabled (preset would enable it);
`omarchy-recover-internal-monitor.service` condition-skipped (toggle file
absent).

### 2.3 drivers — `DEGRADED`

**D1 — kernel error ring, 38 entries (census arm).** Evidence (11:41):

- census line: `kerr=38 (oom=1 io=35 gpu=0 other=2) [unknown: accepted noise floor]`.
- `journalctl -k -b -p err -o json --no-pager | wc -l` = 38.
- composition (same stream, `jq -r '.MESSAGE'`): 20 × `critical target error, dev
  sr0, sector …` + 15 × `Buffer I/O error on dev sr0 …` (35 sr0 lines, boot-only
  window 2026-10-13 11:02:03–06; cross-ref `driver-firmware-plane.md:163-165`),
  1 × OOM kill (Oct 13 23:44:30, `python3` PID 1732581, `anon-rss:27873696kB`,
  `GpuWatchdog invoked oom-killer` — `journal-boot-plane.md:108-111,129`),
  1 × `virt/tdx: TDX not supported by the host platform`, 1 × empty MESSAGE.

Reading: [observed] no nvidia/driver fault class this boot — the ring is 35
boot-only optical lines + 1 OOM event + 1 informational + 1 blank. **Operator
unblock (conditional):** sr0 — only if it recurs (check media/drive; no record
since the boot window); OOM — only if it recurs (review memory pressure for the
GPU workstream); TDX line — informational. Otherwise accepted noise floor;
re-check next boot: `journalctl -k -b -p err -o json | wc -l`.

**D2 — stale DKMS registration.** Evidence (11:41):

```
$ dkms status
nvidia/610.57.04, 7.1.4-arch1-1, x86_64: installed (Original modules exist) (Built modules are missing in the kernel modules folder)
nvidia/610.57.04, 7.2.3-arch1-3, x86_64: installed
$ ls /lib/modules/
7.2.3-arch1-3
```

Classification: residue, not a driver failure — the loaded module is the current
7.2.3 build (`nvidia-smi` answers 610.57.04); the 7.1.4 tree is gone. **Operator
unblock:** `sudo dkms remove nvidia/610.57.04 -k 7.1.4-arch1-1`; verify
`dkms status` then lists only the running-kernel row. Until cleared, this stays
a named residue in the plane.

**D3 — unowned DKMS module artifact.** Evidence (11:41):

```
$ pacman -Qo /lib/modules/7.2.3-arch1-3/updates/dkms/nvidia.ko.zst
error: No package owns /lib/modules/7.2.3-arch1-3/updates/dkms/nvidia.ko.zst        (rc=1)
$ modinfo -F version /lib/modules/7.2.3-arch1-3/updates/dkms/nvidia.ko.zst
610.57.04
```

file 12 027 573 B, mtime 2026-10-11 16:15. Reading: expected for DKMS build
output — pacman cannot verify it. **Operator unblock:** none required; the
verification route is `modinfo -F version` (610.57.04) + `nvidia-smi`
(610.57.04). Only repackaging the module could make pacman own it (out of
province).

Receipt: nvidia present and answering — PCI `0x10de` ×2, `nvidia-smi` → `NVIDIA
GeForce RTX 5070, 610.57.04`, `lsmod` nvidia rows = 4, `/dev/nvidia*` nodes = 6.

### 2.4 journal / boot — `DEGRADED`

**J1 — coredump storm (the plane's DEGRADED driver).** Evidence (11:41–11:45):

- census line: `err=251 (coredump=211 kernel=38 other=2)` (14:57:13Z).
- `journalctl -b -p err -o json --no-pager | wc -l` = 248 (11:41) → 251
  (11:45); same stream by identifier: `systemd-coredump` 208 → 211,
  `kernel` 38, `sddm-helper` 1 (`gkr-pam: couldn't unlock the login keyring`,
  Oct 13 11:02:06), `limine-snapper-sync` 1 (J4).
- raw lines for the same selection: 63 647 — ≈256 lines per entry (line counts
  are traps; entries only).
- `coredumpctl list --since "2026-10-13 10:57:58" --json=short | jq length` =
  208 (11:41) → 211 (11:45); breakdown (11:41): godot 148 SIGABRT, node 47
  (25 SIGABRT + 22 SIGTRAP), **python3.14 4 SIGSEGV (new since round 2)**,
  grok-bot 3 SIGBUS, chrome_crashpad 2 SIGBUS, typora 2 SIGTRAP, electron 1,
  bash 1 SIGSEGV. Latest core 2026-10-14 11:44:50 (godot SIGABRT) — the storm
  is live during this report.

**Operator unblock (cross-domain, reported not absorbed):** hand the storm to
the owning workstreams (godot → game-dev lane; grok-bot / chrome_crashpad →
fleet-app owners); tsukuroi tracks state only. Re-count:
`journalctl -b -p err -o json --no-pager | wc -l`. Context (R3-1 §1.1): this
boot's 247+ err entries stand far above every prior retained boot (prior range
1–168 entries, typical 39–92) — the storm is the dominant error source, not a
boot regression.

**J2 — coredump disk footprint [advisory].** `/var/lib/systemd/coredump` =
3.9 G (`du -sh`, 11:45), 185 files (`ls | wc -l`); journal disk 181.3 M
(`journalctl --disk-usage`, 11:45). `/` has 849 G free — hygiene, not pressure.
**Operator unblock:** prune only after crash owners have the cores; this build's
`coredumpctl --help` lists only list/info/dump/debug (no delete/vacuum) — removal
is a root file operation (operator).

**J3 — boot dwell, bimodal [unknown].** Evidence (R3-1 §5, cross-checked with my
`systemd-analyze` 11:45): userspace 3.1–4.7 s stable across 13 boots; the
pre-userspace "kernel" phase is bimodal, 12 s → 2 h 58 m (boot 0 = 4 m 3.328 s).
Candidate mechanism: initramfs dwell at the LUKS prompt (`resume=` on the
cmdline; every boot logs `PM: Image not found` once) — [inference, unproven];
`/etc/crypttab` is mode 600 root (not read — shape-only, BLOCKED).
**Operator unblock:** if the dwell matters, operator probes the crypttab/keyfile
and resume configuration (root); mechanism stays [unknown] here.

**J4 — `limine-snapper-sync` self-claim vs empty configs.** Evidence: my fresh
`snapper list-configs` → header-only table, rc=0 (11:45); boot 0 carries both a
P4 line ("Creating a Snapper config named 'root' …") and a P3 line ("No Snapper
config found … Please configure Snapper and set SNAPPER_CONFIG_NAME in
/etc/default/limine") — `journal-boot-plane.md:139-149`. Reading: contradictory;
snapper shows no config despite the tool's claim. **Operator unblock:** configure
Snapper + `SNAPPER_CONFIG_NAME` (P3's exact instruction) or explicitly accept
snapshot-less; re-audit the claim (cross-ref U1).

**J5 receipts (no action):** failed-service history — 0 unit failures across 13
retained boots (R3-1 §4: strict pattern 0; 36 broad matches are portal
RealtimeKit warnings); system scope `running`, `--failed` → 0 loaded units;
system timers 5/5 `Result=success`, each trigger inside its declared
randomization/accuracy window (R3-1 §6); boot target `graphical.target:active`
(census).

### 2.5 update-safety — `DEGRADED` (arm vocabulary)

**U1 — no rollback net (leading exposure).** Evidence: `snapper list-configs` →
header-only, rc=0 (11:45); `limine-snapper-sync` installed/enabled but inactive;
boot message (J4). Any wave on this host is snapshot-less
(`update-safety-note.md:289-292`; `SKILL.md:124-128`). **Operator unblock:**
configure snapper + `SNAPPER_CONFIG_NAME` (or record explicit acceptance of
snapshot-less in writing) before any `-Syu`.

**U2 — upstream delta unmeasurable read-only (the real gate).** Evidence (11:44):
`pacman -Qu` → rc=1, 0 lines; `pacman -Sup --print-format '%r/%n %v'` → rc=0,
0 lines; sync dbs born `2026-10-11 12:54:13.542054496` (`stat -c '%w'`) but
core/extra/multilib carry **2026-09-08** content stamps (36 days at measurement)
— "empty" is against a 36-day-old snapshot, not against upstream. `checkupdates`
absent (`command -v` rc=1). **Operator unblock:** the resolving event is
operator-side — `sudo pacman -Sy` then re-run the probes, or install
`pacman-contrib` + `checkupdates`; before any resulting wave, prep: (a) rollback
story (U1), (b) DKMS rebuild plan (U3), (c) schedule (U8), (d) trust-channel
decision (U4) (`update-safety-note.md:364-373`).

**U3 — kernel/DKMS rebuild coupling.** Evidence: D2's stale row shows a rebuild
already failed once; `uname -r` = `pacman -Q linux` = `7.2.3` → no reboot
pending today; a kernel-raising wave triggers the DKMS rebuild + initramfs
hooks in the same transaction (`update-safety-note.md:224-231,294-300`).
**Operator unblock:** after any kernel wave, verify `dkms status` shows the new
kernel's `nvidia/610.57.04` build **before reboot**.

**U4 — trust surfaces.** Evidence: `[omarchy]` `SigLevel = Optional TrustAll`
(`/etc/pacman.conf:29`); `LocalFileSigLevel = Optional` (`:16`); no `.db.sig`
stored (R2 note §2); global `SigLevel = Required DatabaseOptional` (`:15`).
**Operator unblock:** accept the channel explicitly or re-scope it (raise the
omarchy SigLevel / stop relying on local-file installs) — a written decision
before the next wave.

**U5 — downgrade trap.** Evidence: installed `1password-beta
8.12.42_32.BETA-32` > channel `8.12.42_32.BETA-1` (R2 version join: 1 ahead);
plain `-Syu` ignores it, `-Suu` would downgrade it (579.18 MiB rewrite).
**Operator unblock:** use plain `-Syu` only; never `-Suu`; never `-Syyu`
(re-downloads 36-day-stamped dbs).

**U6 — `/boot` privilege gate (BLOCKED arm, recorded).** Evidence: `ls /boot` →
rc=2 `Permission denied` (11:45); `bootctl status` answers partially then fails
to read `/boot/EFI/systemd`. **Operator unblock:** root pre-verify
`sudo ls /boot` + `sudo bootctl status` before a kernel/firmware/limine wave.

**U7 — `walker-restart.hook` root-exec [cross-domain].** Evidence (R2 note §4):
the hook's PostTransaction execs user-owned
`~/.local/share/omarchy/bin/omarchy-restart-walker` as root. **Operator
unblock:** kagi / operator review of that trust shape (reported, not absorbed).

**U8 — schedule around live workloads.** Evidence: round-2 census saw 75 ×
`ffmpeg` (10:51); this round runs with sibling lanes writing concurrently.
**Operator unblock:** run waves in a quiet window.

Arm composition (cited, `update-safety-note.md:334-381`): right now `INERT`
(0 candidates, 3 probes agree); right after a refresh `UNKNOWN-UPSTREAM` +
`REQUIRES-PREP`; `-Suu` / `-Syyu` `DO-NOT`.

## 3. Unknowns register (open probes; resolution owner)

1. Root `-Qkk` deltas for the 32 failed-calc + 4 permission-denied lines — operator root run (`package-state-plane.md:291-292`).
2. `powerprofilesctl` drift intent — operator question (P3).
3. Elephant-family channel provenance — operator / omarchy source (P4).
4. Upstream Arch delta since 2026-09-08 — operator `-Sy` or network probe (U2).
5. GSP image selection for the GB205 GPU (U1) — out of province (kaidoku/revenger); rejection kept.
6. What read the firmware files at their atimes (U2) — root tracing; contents never read.
7. Boot dwell mechanism incl. the crypttab/keyfile question — operator (J3).
8. `PM: Image not found` writer/phase and resume semantics — `journal-boot-plane.md:353-367`.
9. `limine-snapper-sync` claim vs empty configs — update-safety re-audit / operator (J4).
10. Journald effective retention (shipped config is defaults-only) — derivation/operator.
11. Contents of the 3 alpm temp dirs (mode 700 alpm) — root.
12. UPS existence — not exposed read-only.
13. Coredump root cause (godot storm) — owning workstream (J1).
14. Unit failures outside the failed-pattern sweep — bounded negative, `journal-boot-plane.md:361-363`.
15. `ai-usage` env-file contents — secrets shape-only, deliberately not read.

## 4. Method and read-only contract

- **Gate:** census-v2 settled at 11:52 (md5 `41953ee9…`), consumed at
  14:57:13Z; selftest 26/26 rc=0; live rc=1 `DEGRADED`. A pre-v2 v1 snapshot
  (14:39:26Z) confirms the three legacy planes read identically across the
  window.
- **Notes driven:** four plane notes + update-safety note (md5s §5); note
  claims are cited as note claims — this report re-measured the headline probes
  itself and marked the rest by source.
- **Read-only:** every probe is a query; live mode creates no files; no
  install/upgrade/remove/restart verb was run; privilege gates (`/boot`,
  `crypttab`, alpm temp dirs) are recorded as BLOCKED, never escalated.
  Before/after `git status` unchanged apart from the round's own artifacts.
- **Drift caveat (measured):** counts move while the crash storm runs —
  coredumps 208 → 211 within ~4 minutes, err entries 248 → 251. Every number
  here is a capture with its command and time; re-run for current values.

## 5. Provenance (artifacts consumed, with md5 + line counts)

| artifact | md5 | lines | role |
|---|---|---|---|
| `tools/tsukuroi-census.sh` (census-v2) | `41953ee9f2099281c91759249fe8708f` | 976 | gate, consumed 14:57:13Z |
| `tools/tsukuroi-census.sh` (v1 baseline) | `7a3d3b94ecd73fbe1a9a98e9dc88b92f` | 744 | superseded snapshot 14:39:26Z |
| `corpus/knowledge/journal-boot-plane.md` | `16d4047e8b03deec69773d2cc0b1b75c` | 411 | journal/boot plane note (R3-1) |
| `corpus/knowledge/package-state-plane.md` | `24eafc4067f6ca7bf3608dfff5ff63d6` | 303 | package plane note |
| `corpus/knowledge/systemd-user-plane.md` | `26dca9cf12b322926babfef49e257f07` | 247 | systemd user plane note |
| `corpus/knowledge/driver-firmware-plane.md` | `a44e9c07d5b139fe65d5284674398b3a` | 242 | driver/firmware plane note |
| `corpus/knowledge/update-safety-note.md` | `5cc3067fec33d261d8bff6a5c7e8ac48` | 478 | update-safety note |

Line counts via `wc -l`; hashes via `md5sum` at 11:46–11:58.

## 6. Errata / pending (append-only)

- 2026-10-14 — **mid-flight revision change, recorded not laundered:** the
  gate was being rewritten by the sibling lane during this report's window
  (v1 `7a3d3b94…` → settled v2 `41953ee9…`, +259/−26 lines). This report
  consumes the settled v2; the v1 three-plane snapshot (14:39:26Z) is kept in
  scratch, not quoted as current.
- 2026-10-14 — **LOG.md entry owed** for this report (`AGENTS.md:3`): this
  seat's write scope was this file only; the round scribe must append the
  round-3 log entry.
- 2026-10-14 — **SKILL.md round-3 distill owed:** SKILL still describes the
  three-plane gate (round-2 block) and predates `journal-boot-plane.md`; the
  round's distill seat should point it at census-v2 + the journal note.
- Count drift note (J1/J2): `journal-boot-plane.md` §2.1 captured 247 err
  entries at 11:40; this report captured 248 (11:41) and 251 (11:45) — drift in
  a live storm, not a disagreement; both are entry-level counts.

## Appendix A — executor re-run set

```bash
# gate (from the repo root)
bash tools/tsukuroi-census.sh --selftest        # expect rc=0, 26/26 PASS
bash tools/tsukuroi-census.sh                   # expect rc=1, DEGRADED rollup

# package plane
pacman -Qkk 1password-beta 1password-cli        # rc=1, GID+Permissions on the two setgid helpers
pacman -Qm | wc -l                              # 16
pacman -Qq | wc -l                              # 1188
timeout 240 pacman -Qkk > /tmp/qkk.txt 2>&1     # rc=1, ~17 s; normalize tr '\r' '\n'
pacman -Qu; echo rc=$?                          # rc=1, empty
pacman -Sup --print-format '%r/%n %v' | wc -l   # 0

# systemd / journal / boot
systemctl --user is-system-running              # running
systemctl --user --failed --no-pager            # 0 loaded units
journalctl -b -p err -o json --no-pager | wc -l # entry count (line counts are traps)
journalctl -b -p err -o json --no-pager | jq -r '[.SYSLOG_IDENTIFIER]|@tsv' | sort | uniq -c | sort -rn
journalctl -k -b -p err -o json --no-pager | wc -l   # 38
coredumpctl list --since "2026-10-13 10:57:58" --json=short --no-pager | jq length
dkms status; ls /lib/modules/                   # stale 7.1.4 row vs only 7.2.3 tree
pacman -Qo /lib/modules/7.2.3-arch1-3/updates/dkms/nvidia.ko.zst   # error, rc=1
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader

# update-safety
stat -c '%w %n' /var/lib/pacman/sync/*.db       # births vs 2026-09-08 content stamps
snapper list-configs                            # header-only
pacman-conf IgnorePkg IgnoreGroup NoUpgrade NoExtract; pacman-conf HoldPkg
ls /var/lib/pacman/db.lck                       # absent
ls /boot                                        # rc=2 non-root (privilege gate)
df -h / /boot; du -sh /var/cache/pacman/pkg
```

## Appendix B — scratch inventory (`/tmp/tsukuroi-r3-3-work/`, ephemeral)

`census-live.out` (v1, 14:39:26Z), `census-live-v2.out` (v2, 14:57:13Z),
`selftest.out` (v1 17/17), `selftest-v2.out` (26/26), `qkk-drift-pair.out`,
`qkk-full.txt` + `qkk-full.norm.txt`, `kerr-msgs.txt`, `qu.out`/`qu.err`,
`sup-print.out`, `boot-ls.err`, `run-started.txt`.