---
name: tsukuroi-shokunin
description: Domain specialist — host operability & system repair. Rank: shonen (probation).
---

# tsukuroi-shokunin

host operability & system repair playbook. Probation seed — rounds 1-3 build the corpus from
measured surfaces; every rule below must earn a cited source before it counts. Nothing here is oral knowledge.

## Standing rules

- Read-only substrates unless PROVINCE.md declares a write surface;
  detection-and-report for operator-owned remediation.
- Secrets shape-only, never content-read.
- Every claim: measured anchor (path:line, command output, evidence id).
  Observation / inference / unknown stay separate.
- Errata append-only; rejections kept.

## Verdict vocabulary (fixed 2026-10-14, round 1)

`HEALTHY` | `DEGRADED` | `BLOCKED` — three states, never a scalar score. Every verdict
carries the probe and the observed value that produced it, so a non-author can re-derive it
(`corpus/QUALITY.md:1-2`). The third state is not "corrupt"; it is "cannot be assessed
read-only" or "core function offline".

| Verdict | Means | Never means |
|---|---|---|
| `HEALTHY` | every probe in the plane returned the pass value listed below | "no problems were found" without a run probe |
| `DEGRADED` | plane answers, but carries a named defect or an unresolved unknown | outage |
| `BLOCKED` | the probe itself cannot run (privilege gate), or the plane's core function is offline | "the hardware/package is corrupt" |

## Health-verdict decision table (per plane)

Planes are the owned surfaces of `PROVINCE.md:5-12`. The right column is a **timestamped
snapshot (2026-10-14, host `plazir27`)** — re-measure; never quote it as current state.
"Altered classes" for `-Qkk` are defined in the subsection below.

| Plane | Probe (verbatim, all read-only) | `HEALTHY` when | `DEGRADED` when | `BLOCKED` when | Measured 2026-10-14 (notes: `corpus/knowledge/`) |
|---|---|---|---|---|---|
| Package state (pacman) | `pacman -Dk; echo $?` and `pacman -Qkk <pkg> …` (targeted) and `pacman -Qdt` and `pacman -Qm \| wc -l` | `No database errors have been found!` and `0 altered` on the queried set | nonzero altered outside the benign classes, or orphan/foreign drift beyond accepted set | pacman itself errors: `db.lck` present, `database is locked`, unreadable local db | `DEGRADED` — census **1188** installed (`pacman -Q \| wc -l`), 207 explicit, **16 foreign**, 3 orphans (`electron39`, `mbedtls`, `webp-pixbuf-loader`); `-Dk` clean; full sweep rc=1, ~17 s, 1332 raw lines → `tr '\r' '\n'`-normalized: **18 pkg summaries with ≥1 altered** (`package-state-plane.md:167-214`); decomposition: 86 backup-diff lines (rc stays 0 — glibc/pambase prove), 36 non-root artifacts (32 failed-calc + 4 Permission denied), 17 metadata-drift lines; strongest content signal `/usr/bin/powerprofilesctl` (mtime+size+sha — operator question, `package-state-plane.md:205`). rc semantics: 0 = none, 1 = ≥1 altered (`package-state-plane.md:146-151`). TSUKUROI-4 re-derivation counted 19 nonzero summary lines (adds `cups-browsed`, a failed-calc artifact) — kept in errata. **Round-6 foreign-risk rule**: the 16 split by measured channel into 14 `offline-exile` (installer's unconfigured `offline.db`; no update **or repair** path) + 2 `AUR-local` (`pacman -U` of the yay cache, `Validated By: None`); risk is a class fold (R1–R12), never the bare count — round-6 append |
| systemd user units & timers | `systemctl --user is-system-running` and `systemctl --user list-units --state=failed` and `systemctl --user list-timers --all` | `running` and 0 failed units (loaded and `--all`) | any failed unit, or a timer whose last run failed (`systemctl --user show <u> -p Result`) | scope state ≠ `running` (`degraded`/`maintenance`/`offline`) | `HEALTHY` — both scopes `running`; 0 failed units (`--failed` and `--all`); 133 unit files listed; `~/.config/systemd/user/` = 7 unit files + 1 drop-in + 5 symlinks, `/usr/lib/systemd/user/` ships 109, 17 unit-paths (`systemd-user-plane.md:27-78`); only `ai-usage.timer` active (≈5-min cadence; last run 09:52:56, `Result=success`); latent/condition side-findings: `omarchy-battery-monitor.timer` disabled (preset would enable — intent [unk]), `omarchy-recover-internal-monitor.service` condition-skipped (toggle file ABSENT) (`systemd-user-plane.md:80-102`) |
| Journal & boot triage | `journalctl -b -p err -o json --no-pager \| wc -l` (entries) and `journalctl -b -p err \| wc -l` (lines, trap) and `journalctl --list-boots` and `coredumpctl list` and `systemd-analyze` | entry count at the plane's noise floor, hits inside the accept-list | recurring crash-loop or resource-exhaustion signatures | no boot reaches `graphical.target`, or boot record missing | `DEGRADED` — **60 941 err lines but only 238 entries** (`-o json \| wc -l`); line-classification is a trap (coredump stack traces, retracted `AMD`/`+` classes — `systemd-user-plane.md:104-116,188-193`). Entry classes: `systemd-coredump` 198, kernel 38 (20 `sr0` critical + 15 Buffer I/O, boot-only 11:02:03–06; 1 OOM; 1 TDX info), `sddm-helper` 1 (`gkr-pam: couldn't unlock the login keyring`), `limine-snapper-sync` 1 (no Snapper config — update-safety residue). Coredumps this boot 198: godot 142 SIGABRT, node 47 (25+22), `grok-bot` 3 SIGBUS, typora 2, `chrome_crashpad` 2, electron 1, bash 1 SIGSEGV; still live 09:42:10; today 92 rows / 90 godot (TSUKUROI-4). OOM: `python3` anon-rss 27 873 696 kB (Oct 13 23:44:30). Boot 0: `uptime -s` 10:57:58 vs first journal record 11:02:03 — kernel 4 min 3 s in `systemd-analyze` [INFERENCE: resume artifact (`resume=` cmdline, first message at monotonic `[244.159301]`); competing hypothesis journal flush/mount delay, `systemd-user-plane.md:184-185` — [unk]] |
| Driver & firmware plane | `nvidia-smi --query-gpu=name,driver_version --format=csv` and `lsmod \| grep -E '^nvidia'` and `dkms status` and `modinfo nvidia` and `ls /usr/lib/firmware/nvidia/*/` | nvidia-smi answers; modules loaded; dkms `installed` for `uname -r`; GSP blobs present | dkms entry stale/non-clean for another kernel, or module tree unowned by a package | `nvidia-smi` fails (`NVIDIA-SMI has failed…`), or `/dev/nvidia*` nodes missing | `DEGRADED` (table residue) — note's function verdict: "driver plane is healthy — open DKMS 610.57.04 loaded and active, both firmware shapes present, no driver fault class this boot" (`driver-firmware-plane.md:198-199`); the DEGRADED is for residue only: `dkms status` stale `7.1.4-arch1-1` registration (tree gone; `ls /lib/modules` = 7.2.3 only) + `pacman -Qo` = `error: No package owns …/updates/dkms/nvidia.ko.zst` (12,027,573 B, vermagic 7.2.3-arch1-3) → pacman cannot verify the module. Extras: packages `nvidia-open-dkms`/`nvidia-utils`/`lib32-nvidia-utils`/`libva-nvidia-driver`/`linux-firmware-nvidia` installed 2026-10-11 16:14 (upgrade 610.43.03-3 → 610.57.04-1); taint OOT + unsigned (Secure Boot off, EFI var first byte 0); GSP active `EnableGpuFirmware: 18` (`/proc/driver/nvidia/params:28`); blobs `gsp_ga10x.bin` 84,310,168 B + `gsp_tu10x.bin` 29,381,504 B; gb205-class `gsp-570.144.bin.zst` → ga102 target 51,762,663 B; atimes 10-13 12:19:53 / 23:28:37 / 10-14 09:53:32; `dmesg_restrict=1` → ring via `journalctl -k` (`driver-firmware-plane.md:9-147,206-215`) |
| Update-safety | `stat -c '%w' /var/lib/pacman/sync/*.db` (birth) and `pacman -Qu` and `pacman-conf IgnorePkg IgnoreGroup` and `ls /var/lib/pacman/db.lck` and `snapper list-configs` | snapshot recent (≤7 days by `%w`), `-Qu` empty, no holds | snapshot stale, pending nonempty, holds declared, or rollback net absent | `/var/lib/pacman/db.lck` exists (interrupted transaction) | `DEGRADED` — **mtime trap corrected**: sync dbs born **2026-10-11 12:54:13.542** (`%w`; core/extra/multilib/omarchy; TSUKUROI-4 re-derived) — the Sep 8 mtimes are upstream server stamps, not arrival (`package-state-plane.md:73-81`). `-Qu` empty **rc=1**; no `IgnorePkg`/`IgnoreGroup` (`pacman-conf`), `HoldPkg = pacman glibc` (`/etc/pacman.conf:7`); single omarchy mirror (`/etc/pacman.d/mirrorlist`, 58 B) and `[omarchy] SigLevel = Optional TrustAll` — soft-trust channel (`package-state-plane.md:9-41`); keyring 184 pub / 230 sub, master key 2026-10-03, last populate ≈10-11 (`package-state-plane.md:93-112`); no `db.lck`. Residues: **no rollback net** (`snapper list-configs` empty; boot log `limine-snapper-sync: No Snapper config found for '/'` — `systemd-user-plane.md:116`), no `checkupdates`/`paccache` (`pacman-contrib` absent), cache 8.6 G unpruned (1568+1568 archives+sigs), dkms rebuild coupling (driver row). **Round-6 foreign-risk rule**: the 16 foreign packages are unreachable by any `-Syu` and unrepairable from a repo (`pacman -Si` rc=1 ×16) — the `offline.db` snapshot + channel-A archives are the only copy; preserve before pruning (`aur-risk-plane.md:108-115`, round-6 append) |

### `pacman -Qkk` as a non-root user — benign-altered classes

A full sweep **rc=1 is not corruption evidence**. Measured shape (`package-state-plane.md:146-214`;
rc/package-count re-derived by TSUKUROI-4): rc=1, ~17 s warm cache, 1332 raw lines for 1188
packages; output interleaves `\r` progress — `tr '\r' '\n'` before parsing (3 summaries otherwise
mangle: groff/libplacebo/xxhash). rc semantics: **0 = no altered files, 1 = ≥1 altered**;
backup-file diffs alone do not set rc (glibc/pambase prove rc=0 with diffs). Classify before
reporting (decision table: `package-state-plane.md:216-225`):

1. **Backup-file diffs (benign, 86 lines)** — `backup file: … (Modification time/Size/SHA256
   mismatch)` for `/etc/pacman.conf`, `/etc/locale.gen`, `/etc/systemd/logind.conf`,
   `/etc/pam.d/system-auth` — expected operator edits; rc stays 0.
2. **Non-root artifacts, 36 lines — need a root re-run to resolve** — 32 × `(failed to calculate
   SHA256 checksum)` across 10 packages (cups 10, ufw 8, filesystem 6, audit 2, cups-browsed 1,
   cups-pdf 1, dbus 1, openssh 1, shadow 1, sudo 1) + 4 × `(Permission denied)`
   (`/boot/amd-ucode.img`, `/etc/sudoers.d/50-asdcontrol`, `/var/cache/cups/rss`,
   `/var/spool/cups/tmp`). Not integrity failures.
3. **Metadata drift, 17 lines — the visible triage list** — Permissions/GID on setgid or
   dynamic-group surfaces (`/usr/bin/op` 2755 root:onepassword-cli,
   `/opt/1Password/1Password-BrowserSupport` 2755 root:onepassword,
   `/usr/lib/utempter/utempter` 2755 root:utmp, `/var/log/journal` GID 981 systemd-journal),
   file-type swaps (`/etc/resolv.conf` → systemd-resolved stub symlink; Yaru icon symlinks),
   retargeted symlinks (`/usr/lib/jvm/default*` → java-21-openjdk, retargeted Oct 12),
   user-file size drift (`/etc/passwd` accounts, `/etc/ufw/user.rules`), and the one **content**
   signal: `/usr/bin/powerprofilesctl` (mtime+size+SHA mismatch) — [UNKNOWN] deliberate omarchy
   patch? operator question (`package-state-plane.md:190-214`).

18 pkg summaries with ≥1 altered; 1166 report 0. No broad corruption observed — [inference]
≈20 real metadata drifts + ≈36 privilege artifacts (`package-state-plane.md:207-214`).
TSUKUROI-4's summary grep shows 19 nonzero lines (adds `cups-browsed` 1, a failed-calc
artifact); resolve by root re-run, not by hand (Errata).

Sibling scratch (ephemeral; key excerpts are embedded in the notes above):
`/tmp/tsukuroi-qkk-full-summary.txt:1-3` (`rc=1 wall_s=17 lines=1332`),
`/tmp/tsukuroi-qkk-full.txt:1-26` (warning classes),
`/tmp/tsukuroi-qkk2-{sudo,shadow}.txt:1` and `-pambase.txt:1-3`,
`/tmp/tsukuroi-foreign.txt:1-16`, `/tmp/tsukuroi-keyring.txt` + `-keyring-err.txt:1`.

## Update-safety checklist (read-only until the stop line)

Run from anywhere; every step is non-mutating. Output every step, even when it passes.

1. **Freshness gate first.** `stat -c '%w %z %n' /var/lib/pacman/sync/*.db` — use `%w`/`%z`
   (birth/ctime), **never `%y`**: pacman preserves upstream mtimes (proof: dbs born
   2026-10-11 12:54:13.542 while mtimes read Sep 8 — `package-state-plane.md:73-81`).
   Empty `-Qu` proves "nothing newer than the last sync snapshot", not "fully up to date";
   refresh (`-Sy*`) is operator action.
2. **Pending picture.** `pacman -Qu` → empty here, **rc=1** (no candidates vs sync db); TSUKUROI-4
   re-derived rc=1. `pacman -Qm` = 16 foreign (3 explicit: `android-apktool-bin`,
   `obsidian-cli-inspector`, `omarchy-walker`; the 13 `elephant-*` are its deps) — not covered by
   a repo `-Syu`; provenance split in `package-state-plane.md:42-71` (`elephant` channel [unknown]).
   `checkupdates`/`paccache` absent (`pacman-contrib` not installed); `yay` present, network
   queries out of scope.
3. **Holds/pins + trust surface.** `pacman-conf IgnorePkg IgnoreGroup` (both empty) and
   `HoldPkg = pacman glibc` (`/etc/pacman.conf:7`); `pacman -Dk` →
   `No database errors have been found!`. Read the channel: mirrorlist = 1 line/58 B (single
   omarchy mirror serving core/extra/multilib) and `[omarchy] SigLevel = Optional TrustAll`
   (packages signed but signature not required — `package-state-plane.md:9-41`).
4. **Integrity sample, then full sweep.** `pacman -Qkk linux pacman systemd nvidia-utils`
   (targeted; rc semantics in the subsection). Full sweep costs ~17 s warm — normalize
   `tr '\r' '\n'`, classify per the subsection; today decomposes to ≈20 metadata drifts
   (one content signal: `powerprofilesctl`) + 36 privilege artifacts.
5. **Keyring freshness.** `pacman-key --list-keys` (rc=0, read-only; `gpg: Note: trustdb not
   writable` is normal non-root) — 184 pub / 230 sub, master key 2026-10-03, last populate
   ≈2026-10-11; expired/revoked tags are historical shape, not defects
   (`package-state-plane.md:93-112`).
6. **Kernel/driver coupling.** `uname -r` vs `pacman -Q linux` (both `7.2.3` today) and
   `dkms status` — a kernel upgrade requires a **successful dkms rebuild of
   `nvidia-open-dkms`** before reboot; a stale `7.1.4-arch1-1` registration is already present,
   so a failed rebuild would degrade the driver plane at next boot.
7. **Boot surface (privilege gate).** `bootctl status` partially answers as user but
   `/boot` reads are denied (`Failed to read "/boot/EFI/systemd": Permission denied`);
   initramfs/limine verification is **BLOCKED read-only** — hand to the operator.
8. **Headroom + cache shape.** `df -h / /boot` (`851G` free on `/`, `1.8G` on `/boot`);
   `du -sh /var/cache/pacman/pkg` (8.6 G; 1568 archives + 1568 sigs 1:1, never pruned —
   superseded copies coexist, e.g. nvidia 610.43.03 next to 610.57.04; 3 `download-*` dirs
   700 `alpm` unreadable → cache size ≥ 8.6 G — `package-state-plane.md:114-144`).
9. **Rollback net — measure, do not assume.** `pacman -Q snapper limine-snapper-sync`
   (installed) **but** `snapper list-configs` → empty and boot log carries
   `limine-snapper-sync: No Snapper config found for '/'` (`systemd-user-plane.md:116`):
   no snapshot net is configured; report any upgrade exposure as snapshot-less until the
   operator configures it.
10. **Transaction state.** `ls /var/lib/pacman/db.lck` (absent = no interrupted transaction);
    `tail /var/log/pacman.log` (last: 2026-10-13 16:37 `git-filter-repo`,
    `transaction completed`).
11. **STOP LINE.** Produce the report (plane, verdict, probe, verbatim output, unknowns,
    suggested operator action). The sweep ends here; `-Syu`/`-Sy`/`-R…` never run
    (see boundary rule). If an operator decision is needed, append to
    `.ufo/l0-questions.md` per the fleet convention.

## Boundary rule — detection, never remediation

- tsukuroi **never installs, upgrades, removes, or restarts** (`PROVINCE.md:16-17`,
  `MINT.md:18-19`); its whole product is verdict + evidence + suggested operator action.
  Observed surfaces are read-only probes (`PROVINCE.md:5-12`). All three probe notes
  record that nothing on the box was modified (`systemd-user-plane.md:7`,
  `driver-firmware-plane.md:5-7`, `package-state-plane.md:5`).
- **Allowed (read-only) verbs, all exercised this round:** `pacman -Q…`, `-Qu`, `-Dk`,
  `-Qkk`, `-Qo`, `-Qdt`, `-Qm`; `pacman-conf` (merged-config read); `pacman-key --list-keys`;
  `systemctl --user status/list-units/list-units --all/list-timers/list-unit-files/is-enabled/show`;
  `systemctl is-system-running`; `journalctl -b/-k/--list-boots/--disk-usage/-o json`;
  `coredumpctl list` / `--json=short`; `snapper list-configs`; `nvidia-smi --query-*`;
  `lsmod`, `modinfo`, `dkms status`; `find`/`ls`/`test -e` on unit dirs and firmware dirs;
  `stat`, `lsblk`, `df`, `du`, `free`, `uptime`, `uname`.
- **Forbidden (mutating) — including reads that mutate:** `pacman -Sy` (`-Syu` too) writes
  the sync db; `pacman -S/-R/-U`, `yay`-install paths; `dmesg -c/-C` clears the kernel
  ring; `journalctl --rotate/--vacuum-*`; `coredumpctl dump/delete`; `systemctl
  start/stop/restart/enable/disable/preset`; `nvidia-smi -r` (GPU reset); `pacman-key
  --refresh-keys/--populate/--init` (keyring writes); `bootctl install/update`; mirrorlist
  rewrites (`reflector`); `snapper create/rollback/set-config`; edits to `/etc`, `/boot`,
  units; `pacman -Fy` (syncs the file db).
- **Privilege gates are verdicts, not invitations.** `dmesg` reads fail non-root
  (`dmesg: read kernel buffer failed: Operation not permitted`; `/proc/sys/kernel/dmesg_restrict`
  = `1` — `driver-firmware-plane.md:9-11`); use `journalctl -k`. `/boot` and root-only `/etc`
  files are unreadable (checklist item 7) — record `BLOCKED` and hand the probe to the
  operator; never reach for `sudo` to "finish the check" (detection does not require
  privilege escalation; if it truly does, the operator runs it).
- **Secrets shape-only** (`AGENTS.md:4-5`): keyring queries read public keys only
  (184 pub / 230 sub listed; private dirs mode 700 root, not read —
  `package-state-plane.md:100-111`); env files are noted, never read
  (`systemd-user-plane.md:36`) — never read or echo private material. Cross-domain findings
  are **reported, never absorbed** (`PROVINCE.md:18`): driver internals → kaidoku/revenger;
  endpoint health → kama; secrets → kagi; fleet-app crashes (`grok-bot`, `chrome_crashpad`
  coredumps above) → the owning lane, cited in the round report.
- **Errata append-only** (`corpus/QUALITY.md:4`): corrections to this file land as new
  dated blocks; rejections stay visible.

## Sources

- Lane seeds: `PROVINCE.md:5-17` (owned surfaces, refuses, no-install boundary),
  `MINT.md:18-19` (domain boundary), `AGENTS.md:3-5` (evidence, read-only, secrets),
  `corpus/QUALITY.md:1-5` (admission bar), `SHONEN.md:6-7` (SKILL craft gate).
- **Sibling notes (this round's three; arrived 2026-10-14 09:58:13 / 09:58:41 /
  10:01:35 — package note last edited 10:02:57):**
  - `corpus/knowledge/package-state-plane.md` (TSUKUROI-1, 256 lines) — trust surface
    `:9-41`, census `:42-71`, sync-db mtime trap `:73-91`, keyring `:93-112`, cache
    `:114-144`, Qkk targeted + full + decision table `:146-226`, errata `:228-239`,
    unknowns `:241-256`.
  - `corpus/knowledge/systemd-user-plane.md` (215 lines) — manager state `:12-25`,
    unit inventory `:27-78`, timer plane `:80-95`, condition-gated units `:97-102`,
    boot error classes `:104-124`, coredump census `:126-147`, user journal view
    `:149-156`, method lessons `:158-173`, unknowns `:175-186`, errata `:188-193`.
  - `corpus/knowledge/driver-firmware-plane.md` (219 lines) — module census `:15-64`,
    driver presence `:66-108`, GSP shape `:110-147`, boot err/warn classes `:149-174`,
    update candidates `:176-193`, obs/inf/unk `:195-215`, errata `:217-219`.
- Sibling probe scratch (ephemeral; key excerpts are embedded in the notes above):
  `/tmp/tsukuroi-*.txt` (14 files, 2026-10-14 09:54:03–09:56:50) — foreign list,
  per-package and full Qkk, `qkk2` sudo/shadow/pambase, keyring + err.
- Re-derived in-lane (TSUKUROI-4, 2026-10-14): full `-Qkk` (`rc=1`, 1188 pkgs, 19 nonzero
  summary lines); targeted `-Qkk`; `pacman -Qu` (empty, **rc=1**); `-Qm`=16, `-Qdt`=3,
  `-Q`=1188; `-Dk`; `stat '%w'` sync dbs (birth 2026-10-11 12:54:13.542);
  `snapper list-configs` (empty); `pacman -Q pacman-contrib` (not found);
  `systemctl`/`journalctl -o json`/`coredumpctl list`/`nvidia-smi`/`lsmod`/`modinfo -n`/
  `dkms status`/`pacman -Qo`; `bootctl status` (partial); `systemd-analyze`;
  `df`/`du`/`free`/`uptime`.
- Shape model: `kama-shokunin/SKILL.md` (sibling lane, distilled form: decision table +
  checklist + cited sources). Fleet conventions: PROTOCOL.md file contract (`SKILL.md` =
  craft + cited sources; `.ufo/reports/round-<N>/<id>.md` = lane report).

## Errata / pending

- 2026-10-14 — **the three sibling notes landed mid-write** (09:58:13 `systemd-user-plane.md`,
  09:58:41 `driver-firmware-plane.md`, 10:01:35 `package-state-plane.md` (last edit 10:02:57),
  all under `corpus/knowledge/`); the table, Qkk subsection, and checklist above were
  re-anchored to them in the same sitting. Draft cells that rested only on scratch + in-lane
  re-derivation are superseded; the corrections that changed a verdict are kept below.
- 2026-10-14 — **correction: sync-db freshness.** First-pass read used mtime
  (`%y` → Sep 8, "36 days stale"); wrong — pacman preserves upstream mtimes; birth (`%w`)
  = 2026-10-11 12:54:13 (3 days). Update-safety verdict stays `DEGRADED`, now for the
  rollback-net/trust residues, not staleness (`package-state-plane.md:73-81,235-237`).
- 2026-10-14 — **correction: journal counting.** First-pass classified `journalctl -b -p err`
  by lines (60,941; godot 21,004) and awk columns; entry-level count is 238
  (`-o json | wc -l`) — the note retracted its own line-level classes
  (`systemd-user-plane.md:104-116,160-163,188-193`). Line counts are traps; use entries.
- 2026-10-14 — **correction: unit-file count.** "136 user unit files" was a raw `wc -l`;
  `systemctl --user list-unit-files` reports 133; per-note inventory in
  `systemd-user-plane.md:27-40`.
- 2026-10-14 — **correction: rollback net.** First-pass inferred snapshot coverage from the
  `snapper`/`limine-snapper-sync` packages + pacman hook; `snapper list-configs` → empty and
  the boot log shows `limine-snapper-sync: No Snapper config found for '/'`
  (`systemd-user-plane.md:116`; TSUKUROI-4 re-derived). No snapshot net is configured.
- 2026-10-14 — full-sweep nonzero count: 19 summary lines (TSUKUROI-4 grep, incl.
  `cups-browsed`) vs 18 pkg summaries in `package-state-plane.md:207-210`. Resolve by root
  re-run; do not reconcile by hand.
- Open unknowns carried forward (per notes): root `-Qkk` deltas, GSP image selection (U1),
  firmware atime readers (U2), `powerprofilesctl` drift intent, omarchy channel provenance
  for the elephant set, mirror/upstream freshness, `omarchy-battery-monitor.timer` intent.

## Round-2 census gate — executable verdict semantics (`tools/tsukuroi-census.sh`)

Distilled 2026-10-14 (TSUKUROI-R2-4) from the settled revision of the gate
(744 lines, md5 `7a3d3b94ecd73fbe1a9a98e9dc88b92f`) and its own runs. The gate is
the executable form of the decision table above: three planes — packages,
systemd user scope, drivers — one verdict line, firmware-style exit map
(`tools/tsukuroi-census.sh:25-74,733-741`). Plan anchor: `plans/round-2.plan.md:3-9`;
anti-claim: **any plane unreadable live → `BLOCKED` arm fires, never a fake
pass** (`plans/round-2.plan.md:8`; `tools/tsukuroi-census.sh:13-14`). Read-only
guarantee: live mode creates no files at all; the only writes anywhere are the
selftest's own `mktemp -d /tmp/tsukuroi-r2-1-selftest.XXXXXX`
(`tools/tsukuroi-census.sh:76-78,461-464`). Secrets never read — only public
package / unit / driver state (`:78`).

### Gate usage and output contract

```bash
bash tools/tsukuroi-census.sh              # live read-only census → verdict line + exit map
bash tools/tsukuroi-census.sh --selftest   # hermetic fixture-tree test; exit 0 pass / 1 fail
bash tools/tsukuroi-census.sh --sample N   # packages -Qkk sample size (default 8)
```

```
TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED (packages=.. systemd=.. drivers=..)
exit map: 0 HEALTHY | 1 DEGRADED | 2 BLOCKED   (worst plane wins; usage errors also 2)
```
(`tools/tsukuroi-census.sh:22-23,126-138`)

The gate's own selftest — run 2026-10-14T13:59:03Z against this revision, output
captured verbatim (17 cases: 4 HEALTHY / 6 DEGRADED / 7 BLOCKED; each case
asserts exit code + verdict + plane substring + fixture byte-unchanged, plus a
`host=fixture-host` check proving no host path was read —
`tools/tsukuroi-census.sh:80-88,563-599`):

```
PASS healthy: all planes pass (exit 0, HEALTHY)
PASS healthy: nvidia present and answering (exit 0, HEALTHY)
PASS healthy: unrestricted dmesg ring preferred (exit 0, HEALTHY)
PASS healthy: rc=1 backup-only sample is not a defect (exit 0, HEALTHY)
PASS degraded: Qkk sample drift (exit 1, DEGRADED)
PASS degraded: foreign packages (exit 1, DEGRADED)
PASS degraded: declared hold (IgnorePkg) (exit 1, DEGRADED)
PASS degraded: failed unit (exit 1, DEGRADED)
PASS degraded: timer last run failed (exit 1, DEGRADED)
PASS degraded: kernel error ring (exit 1, DEGRADED)
PASS blocked: pacman db.lck (exit 2, BLOCKED)
PASS blocked: pacman binary missing (exit 2, BLOCKED)
PASS blocked: sample probe error (exit 2, BLOCKED)
PASS blocked: systemd user bus unreachable (exit 2, BLOCKED)
PASS blocked: nvidia hardware, driver offline (exit 2, BLOCKED)
PASS blocked: both kernel rings unusable (exit 2, BLOCKED)
PASS blocked: empty ring is not a clean bill (exit 2, BLOCKED)
TSUKUROI_CENSUS_SELFTEST: PASS (17 cases, 17 passed, 0 failed)
```

selftest rc=0; no `/tmp/tsukuroi-r2-1-selftest.*` dir left behind (trap cleans —
`tools/tsukuroi-census.sh:461-464`). Live run, same revision (verdict lines
verbatim; zero host mutation verified — `git status` identical before/after):

```
tsukuroi-census census-v1 — host=plazir27 — 2026-10-14T13:59:03Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16; pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=38 (oom=1 io=35 gpu=0 other=2) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED)
```

(exit 1; scratch: `/tmp/tsukuroi-r2-4-scratch/selftest.txt`, `live-census.txt` —
ephemeral.) The `TSUKUROI_*` env overrides exist to make the selftest hermetic
(`tools/tsukuroi-census.sh:85-88`); a live verdict produced with overrides would
not be a measurement of the host — fixture runs only.

### What each plane's findings mean (as implemented, `tools/tsukuroi-census.sh:25-74`)

**packages** — probe: bounded `pacman -Qkk` sample over `pacman -Qq` (default 8)
+ `pacman -Qm` count + `pacman-conf IgnorePkg IgnoreGroup` + `HoldPkg` read
(printed; never gates) (`:27-42,199-279`).
- `HEALTHY` — sample drift 0, foreign 0, pins empty. Sample rc may still be 1:
  `backup file:` diffs alone do not set rc; **the drift count decides, not the
  rc** (`:30-31,42`; selftest case `healthy: rc=1 backup-only sample is not a
  defect`).
- `DEGRADED` — drift > 0 (pacman's own altered-file counts, which already
  exclude backup diffs; drifted package names listed — `drift=2[1password-beta,
  1password-cli]`), foreign > 0 (accepted baseline is an operator question, not
  a script constant; the round-6 register gives that baseline a contract —
  specified, not yet landed, see the round-6 append), or pins declared.
- `BLOCKED` — pacman missing; `-Qq` rc ≠ 0 (local db unreadable); `db.lck`
  present (interrupted transaction — never a fake pass); sample `error:` or rc
  outside {0,1}.
- The sample is bounded on purpose: the full sweep (~17 s warm) belongs to the
  operator checklist, not a gate latency budget (`:40-42`).

**systemd (user scope only)** — probe: `is-system-running` + failed units +
`show <timer> -p Result` for each enabled timer (bounded 12) (`:44-57,282-345`).
- `HEALTHY` — state `running`, failed 0, every scanned timer `Result=success`.
- `DEGRADED` — any failed unit; timer Result ≠ success or unreadable
  (unresolved unknown); state in {degraded, starting, stopping}.
- `BLOCKED` — systemctl missing; bus unreachable (output is not a state word);
  a list probe fails; state in {offline, maintenance}.
- **Deliberate refinement, recorded not silent**: round 1 lists scope `degraded`
  under BLOCKED (`SKILL.md:42`); census-v1 reports it DEGRADED because the
  failed-units probe still assesses it fully (`tools/tsukuroi-census.sh:54-57`).

**drivers** — probe: kernel err ring (`dmesg --level=err,crit,alert,emerg`
preferred, else `journalctl -k -b -p err -o json`; entry counts — line counts
are traps, `SKILL.md:217-220`) + nvidia presence (PCI `0x10de` vendor,
`nvidia-smi`, `lsmod`, `/dev/nvidia*`) (`:59-74,348-458`).
- `HEALTHY` — kerr 0 with a non-empty ring, and nvidia either
  present-and-answering (smi ok + module loaded + nodes exist) or absent from
  PCI inventory.
- `DEGRADED` — kerr > 0, class-counted `oom / io / gpu / other`; the noise floor
  is [unknown], so every kernel error entry is a named unresolved item.
- `BLOCKED` — both rings unusable; ring empty (**clean vs no-data cannot be
  told apart** — selftest case `blocked: empty ring is not a clean bill`);
  nvidia hardware in PCI but core function offline (smi not answering / no
  module / no `/dev/nvidia*` node); PCI inventory unreadable with no other
  positive evidence.
- `ring=` in the plane line names the source actually used (measured host:
  `dmesg_restrict=1` → `ring=journalctl-k`; `:73-74`).

Scope note: the gate covers 3 of the 5 adjudicated surfaces (system-scope
systemd and pure journal/boot triage stay checklist-driven — `:44-45`); journal
& boot findings still come from `SKILL.md:43` + `systemd-user-plane.md`.

### Round-2 update-safety note — verdict arms and boundaries

`corpus/knowledge/update-safety-note.md` (TSUKUROI-R2-2; settled 478 lines, md5
`5cc3067fec33d261d8bff6a5c7e8ac48`) extends the 11-step checklist with a measured
`-Syu` decision table. For the update-safety question the fixed arm vocabulary
is not HEALTHY/DEGRADED/BLOCKED but `PASS` · `INERT` (transaction would do
nothing) · `REQUIRES-PREP` · `BLOCKED` (probe cannot answer read-only) ·
`UNKNOWN-UPSTREAM` · `DO-NOT`; composition: strongest arm fired, ordered
`BLOCKED > UNKNOWN-UPSTREAM > REQUIRES-PREP > INERT > PASS`; every verdict
carries its firing row and measured value
(`corpus/knowledge/update-safety-note.md:334-339`).

Composed verdicts (measured 2026-10-14, `:358-381`):
- **`-Syu` right now: `INERT`** — 0 candidates; three probes agree (`-Qu` empty
  ×3, `-Sup --print-format` 0 lines, version join 1171 equal / 0 behind /
  1 ahead) (`:19-40`).
- **`-Syu` right after the refresh: `UNKNOWN-UPSTREAM` + `REQUIRES-PREP`** —
  candidate set decided by the mirror snapshot at that moment; 36-day content
  stamp means kernel / libc / driver classes are in scope; read-only cannot
  call it safe. Prep list a–d: rollback story, dkms rebuild plan, schedule
  around the ffmpeg workstream, accept or re-scope the `[omarchy]` TrustAll
  channel (`:364-373`).
- **`-Suu` / `-Syyu`: `DO-NOT`** — `-Suu` would downgrade `1password-beta`
  (installed BETA-32 ahead of channel BETA-1); `-Syyu` re-downloads
  36-day-stamped dbs for no benefit (`:280-284,374-375`).

Boundaries and traps the note fixes (each re-measurable):
- `-Qu` empty proves "nothing newer than a 36-day-old snapshot", not "fully
  current" — upstream delta is [unknown] read-only; the operator's next `-Sy`
  is the resolving event (`:63-66`).
- `--print-format '%s'` is **not** a size (printed `0` for nvidia-utils whose
  real sync download is 300.73 MiB); take sizes from `pacman -Si` only
  (`:199-202`).
- `HoldPkg = pacman glibc` is removal-protection, **not a version hold**; true
  pins are `IgnorePkg` / `IgnoreGroup` / `NoUpgrade` / `NoExtract` — all empty
  (`:204-222`).
- Shadowing: repo order `core→extra→multilib→omarchy` means `-Qu` never shows a
  newer shadowed omarchy copy — `linux-firmware-cirrus` is why `-Qu` reads
  empty (`:256-278`).
- `snapper list-configs` = 0 configs → any wave is snapshot-less; `dkms status`
  stale `7.1.4-arch1-1` row → a rebuild already failed once; `walker-restart.hook`
  execs a user-owned script as root → reported, not absorbed
  (`:286-330,471-473`).

### Detection, never remediation — round-2 additions

- The gate is detection by construction: no mutating verb in its probe surface;
  live mode creates no files (`tools/tsukuroi-census.sh:76-78`); an unreadable
  plane → `BLOCKED` arm, never a fake pass (`:13-14`; plan anti-claim
  `plans/round-2.plan.md:8`).
- **One non-obvious allowed verb, now exercised**: `pacman -Su* --print*`
  (e.g. `-Sup --print-format '%r/%n %v'`) builds a plan and prints it — no
  transaction, no download, no db write (observed: rc=0 with 0 lines, no
  `db.lck` created) (`corpus/knowledge/update-safety-note.md:12-14,196`). It
  joins the allowed read-only verbs; `-Sy` stays forbidden even though it, too,
  installs nothing.
- `checkupdates` / `paccache` absent; **installing `pacman-contrib` is out of
  province** — the upstream-comparison route is handed to the operator
  (`:14-17,376-381`).
- Privilege gates stay verdicts, not invitations: `/boot` reads rc=2 non-root →
  row `BLOCKED` (operator probe) (`:350`); `dmesg_restrict=1` is handled by the
  ring fallback (`journalctl -k`), never by sudo
  (`tools/tsukuroi-census.sh:73-74`).
- Cross-domain: `walker-restart.hook` root-exec of a user-owned script →
  kagi / operator; `1password-beta` provenance question and the 3 alpm temp
  dirs → operator / privilege gate — reported, never absorbed
  (`corpus/knowledge/update-safety-note.md:471-473`).

### Errata / pending — round 2 (append)

- 2026-10-14 — **round-2 arrivals + this distill.** `tools/tsukuroi-census.sh`
  (TSUKUROI-R2-1; settled 744 lines, md5 `7a3d3b94ed…`, selftest 17/17 PASS)
  and `corpus/knowledge/update-safety-note.md` (TSUKUROI-R2-2; settled 478
  lines, md5 `5cc3067fec…`) landed 10:54:42 and settled 10:58:45; the blocks
  above were distilled from those revisions and the gate's own runs. The one
  semantic refinement (systemd scope `degraded`: round-1 BLOCKED → census
  DEGRADED) is recorded above, not silently applied
  (`tools/tsukuroi-census.sh:54-57`).
- 2026-10-14 — **live snapshot from this distill's own run** (13:59:03Z, zero
  mutation): `TSUKUROI_CENSUS: DEGRADED`, rc=1; packages DEGRADED (sample
  drift 2 = `1password-beta` + `1password-cli`; foreign 16; pins none);
  systemd HEALTHY; drivers DEGRADED (`kerr=38`: oom=1 io=35 other=2; nvidia
  present, smi 610.57.04, modules=4, nodes=6). Snapshot only — re-run, never
  quote as current. The sample drift is a bounded-sample observation; the root
  `-Qkk` re-run remains the named resolution for the 18/19 drift split.
- Pending (round 2): `LOG.md` entry for this append owed per `AGENTS.md:3`
  (this seat's write scope was `SKILL.md` only); round-2 wave-1 errata not yet
  merged here.

## Round-3 append — census-v2 in the gate + the no-oral-context executor test (TSUKUROI-R3-4)

The round-3 test (record: `corpus/knowledge/executor-test-sufficiency.md`) ran the census
with this file as its **only** reference and exposed that the block above describes the
v1 three-plane gate while the settled tool is **census-v2** (four planes) — the same
distill `host-health-report-r3.md:416-418` records as owed. The test's findings stay in
the record; this append lands the fixes. Per-step sufficiency tally from the run:
**7 `SUFFICIENT` / 3 `PARTIAL` / 3 `MISSING`** — the MISSING steps were exactly the v2
coverage landed below (journal field rules, post-verdict contract, the cap item).

### Census-v2 sync (supersedes the v1 revision pins above)

- Revision: `tools/tsukuroi-census.sh` **census-v2** (TSUKUROI-R3-2, mtime 2026-10-14
  11:52:22 -03) — **976 lines** (`wc -l`), md5 **`41953ee9f2099281c91759249fe8708f`** —
  supersedes v1 (744 lines as pinned above / 743 `wc -l`,
  `7a3d3b94ecd73fbe1a9a98e9dc88b92f`). Identity check first:
  `md5sum tools/tsukuroi-census.sh` — a mismatch means the gate has drifted from this
  distill; stop and re-measure before trusting any rule here.
- Usage: the three forms above still hold, plus `--help`; `--sample N` still default 8;
  the `TSUKUROI_*` overrides remain **fixture-only** — a live verdict produced with
  overrides is not a measurement of the host (`:302-305` still holds).
- Selftest: **26 cases (17 legacy + 9 journal-plane)**; final line
  `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)`; rc=0 pass / 1 fail.
  Test-run re-verification 2026-10-14T15:25:54Z: rc=0, wall 1.75 s.
- Live contract v2: `TSUKUROI_CENSUS: HEALTHY|DEGRADED|BLOCKED (packages=.. systemd=..
  drivers=.. journal=..)`; exit map unchanged — **0/1/2, worst plane wins** (the v1
  contract at `:257-261` still holds for the legacy three). Live wall 0.69 s at
  15:25:56Z. Run from the repo root.
- Read-only addendum: live mode creates no files; the selftest now writes only
  `/tmp/tsukuroi-r3-2-selftest.XXXXXX` (`tools/tsukuroi-census.sh:118-120`). Verified in
  the test: before/after `git status` identical, no /tmp residue.
- Plan anchor v2: `plans/round-3.plan.md:3-11`; anti-claim v2: journal unreadable
  without elevated perms → the journal arm **fails closed `BLOCKED`**; the remaining
  planes still report (`tools/tsukuroi-census.sh:21-22`).

### Journal plane — field map and verdict arms (new; absent from the v1 block)

Line shape: `PLANE journal: …. (boots=N current=yes target=T:active err=N (coredump=N
kernel=N other=N); failedhist=N[names]; timers_enabled=N timers_scanned=N armed=N
timer_drift=N timer_unknown=N)`.

- `HEALTHY` — index-0 boot line present; target `active`; `err=0` with a non-empty
  journal this boot; `failedhist=0`; every enabled user timer `ActiveState=active`.
- `DEGRADED` — `err>0` (noise floor `[unknown]`; classes disjoint coredump > kernel >
  other; same stance as the drivers ring); `failedhist>0` (units that failed **earlier
  this boot and were reset since** — history the systemd plane can no longer see);
  `timer_drift>0` or unreadable timer `ActiveState` (`timer_unknown`).
- `BLOCKED` — `journalctl` missing; `--list-boots` unreadable; no index-0 line; boot
  target not `active`; err stream unreadable; journal empty this boot (clean vs no-data
  cannot be told apart).
- `err=` counts **entries** (`journalctl -b -p err -o json` lines) — line counts are the
  recorded trap (`:217-220`). Kernel entries are also counted by the drivers ring; the
  journal plane's distinct value is the non-kernel classes, the boot record/target,
  failed-history and the timer armed-state (`tools/tsukuroi-census.sh:107-109`).
- Semantics mirror `corpus/knowledge/journal-boot-plane.md:304-316`; the tool is the
  executable form.
- **Scope fix**: the gate now covers **4 of the 5** adjudicated surfaces — only
  system-scope systemd stays checklist-driven. This supersedes the "3 of the 5" scope
  note above (`:354-356`), falsified by v2.

### Post-verdict contract (new)

The gate's product is verdict + evidence + suggested operator action; DEGRADED is never
left as "noise" without its named item. For every fired finding (any plane), report the
measured evidence and the **exact operator unblock action** — the round-3 e2e report is
the model format (`host-health-report-r3.md:37-63`, 20 finding→action pairs). Privilege
gates stay verdicts, not invitations; cross-domain findings are reported, never absorbed
(`:137-172`).

### Executor checklist (no-oral-context, self-contained)

1. Confirm gate identity (md5 above). Mismatch → stop; re-distill owed.
2. From the repo root: `bash tools/tsukuroi-census.sh --selftest` → expect rc=0 and
   `PASS (26 cases, 26 passed, 0 failed)`.
3. `bash tools/tsukuroi-census.sh` → verdict line + exit code (0/1/2).
4. Interpret each plane from the tables above; journal fields from the block above.
5. For each DEGRADED/BLOCKED finding: measured evidence + exact operator action
   (pattern `host-health-report-r3.md:37-63`).
6. Read-only check: `git status` identical, no /tmp residue; **re-run before quoting** —
   counts drift live (journal `err` 251 → 260 within ~28 min, 2026-10-14).

### Errata / pending — round 3 (append)

- 2026-10-14 — **no-oral-context test (TSUKUROI-R3-4)** ran 15:25:54–15:25:57Z against
  this file at `f80b4afd…` with the v2 gate; per-step tally 7 `SUFFICIENT` / 3 `PARTIAL`
  / 3 `MISSING`; full record `corpus/knowledge/executor-test-sufficiency.md` (findings
  kept intact there). Snapshot from that run: `TSUKUROI_CENSUS: DEGRADED
  (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)`; journal
  `err=260 (coredump=220 kernel=38 other=2) failedhist=0 timer_drift=0` — snapshot
  only, re-run, never quote as current.
- 2026-10-14 — **expected "20-min cap" item: unresolved, not invented.** The round's
  dispatch expected this file to cover a 20-min cap; no artifact in this lane defines
  one, fleet-wide hits for the phrase sit only in unrelated lanes' logs, the v2 gate
  has no time-cap mechanism, and measured runs are sub-2-second. If a cap is intended,
  it must be specified; see the record §7 U1.
- Pre-existing pendings above remain (LOG entry owed; round-2 wave-1 errata merge; the
  v1 md5-prefix transcription candidate `:429` — v2 supersedes the pin, the candidate
  stays visible).

## Round-5 append — own-gate mutation kill-rate + hardening + drift semantics (TSUKUROI-S5-3)

Dispatch frame: `plans/round-5.plan.md:3-11` — axis adjacency (a sibling's craft: tameshi's
mutation method, applied to this lane's own gate) + freshness (the timer-drift plane). This
append lands the round's two measured products in the playbook — the own-gate kill-rate +
hardening (TSUKUROI-S5-1; hardened gate landed in-tree 2026-10-14 14:06:30 -03) and the
drift-class semantics (TSUKUROI-S5-2; note landed 14:09:15 -03) — and **supersedes the census
revision pins above** with an identity-checked new revision. Arrival receipts: this seat's
watchers `/tmp/w5-tsukuroi-s53-{poll,watch}.log` (tsukuroi tree, window 14:01:47–14:11 -03:
exactly one tool change + one new corpus note); no other lane artifact moved in the window.

### Own-gate mutation — two revisions, never conflated (TSUKUROI-S5-1)

Method: tameshi's runner on fresh `/tmp` copies of the gate, suite `bash "$MUTANT" --selftest`;
per-defect verdicts KILLED (suite exit ≠ 0) / SURVIVED (exit 0) / INCONCLUSIVE (124/126/127);
the target is never written — sha256 before/after is the restore proof
(`tameshi-shokunin/tools/mutate-and-run.sh:16-21,60`). Tool pin: r4-2, md5
`26a27d352690e64b2396a4aabaf4ddf6` (1001 lines), sha256 `597e141989065e03…331b`. Anti-claim
(fit) resolved as **fit, not gap**: the gate's `--selftest` satisfies the suite contract
(rc 0/1 + printed case count), so the manual fallback was not needed
(`plans/round-5-record-draft.md` §1, fit-check bullet — the draft is a moving artifact, so
section refs replace line anchors; at this append's last look `:61-69`).

**Swept revision — the table's pin.** census-v2 (`VERSION='census-v2'`,
`tools/tsukuroi-census.sh:142`) at sha256 `084951be50bcbfee…09c78c5` / md5
`41953ee9f2099281c91759249fe8708f`, 976 lines / 44 947 B — the revision pinned by the
round-3 block above. Suite 26 cases, control GREEN (exit 0). 23 pre-registered single-edit
defects; expectations written before the run (`/tmp/w5-S5-1-work/{spec-census-v2.spec,
manifest.md}`, ephemeral scratch). Executed headline (`/tmp/w5-S5-1-work/sweep1.log:319`):

```
MUTATE: DONE (target=tsukuroi-census-census-v2 defects=23 killed=13 survived=10 inconclusive=0 kill-rate=57%)
```

`MUTATE_RESTORE: OK` (sha256 before = after = pristine `084951be…`) — the sweep ran read-only
on the pinned bytes. 13 killed / 10 survived → 13/23 = 56.5 % (tool prints integer 57 %).

The 10 survivors sit in three miss classes [observed from the manifest's `because` column;
class membership is a reading — inference]:
- **fail-closed arms with no fixture** — D02 empty local db (`-Qq` lists nothing), D19
  unreadable PCI inventory, D20 journal timer plane unreadable;
- **counts never asserted nonzero / exact** — D05 privilege-artifact count, D14/D15 kernel-ring
  class counts (`other` absorbing io/gpu; narrowed OOM regex);
- **boundary / unknown semantics** — D06 bounded `-Qkk` sample size, D09 empty timer `Result`
  (rc=0) read as non-unknown, D10 scope state `degraded`, D12 module loaded but no
  `/dev/nvidia*` node.

**Hardening ledger (same round, landed in-tree).** One new selftest case per survivor class —
D14+D15 die to one class-counts case — 9 new cases, block `tools/tsukuroi-census.sh:915-970`;
each label carries the defect it kills (`:923,929,934,939,945,952,958,963,968`; block comment
`:915-920` names the sweep). Case count 26 → **35** (`grep -c "check '"` = 35).

**Hardened revision — what lands.** md5 `e9327046b05b5c71e07fe511ad7e82dd`, sha256
`aae45531fc393579…207df6`, 1032 lines (`wc -l`) / 48 410 B (banner still `census-v2` — identity
is by hash, not by version string). Executed receipts: selftest rc=0,
`TSUKUROI_CENSUS_SELFTEST: PASS (35 cases, 35 passed, 0 failed)`; the same 23 defects re-swept
(`/tmp/w5-S5-1-work/sweep2.log:175`):

```
MUTATE: DONE (target=tsukuroi-census-hardened defects=23 killed=23 survived=0 inconclusive=0 kill-rate=100%)
```

`MUTATE_RESTORE: OK` (sha `aae45531…` before = after = pristine).

Adjudication rules kept for re-use: killed = suite red **and** the full case count still
enumerated (exit-only is insufficient); survived = green at the same count — a finding, never a
footnote; inconclusive excluded from the rate and named beside it; kill-rate =
killed/(killed+survived); bands are a report convention, not a gate
(`plans/round-5-record-draft.md` §4, adjudication — `:278-280` in the draft revision seen;
moving artifact). A survivor judged equivalent code is a calibration
item, not a gap.

**Identity check (replaces the round-3 pin's `md5sum` line).** `md5sum tools/tsukuroi-census.sh`
= `e9327046b05b5c71e07fe511ad7e82dd` (sha256 `aae45531…`, 1032 lines, 48 410 B) is the current
pinned revision; a mismatch means the gate has drifted from this append — **stop and re-measure**
before trusting any census rule here. This supersedes the 976-line / `41953ee9…` / 26-case pins
above (rounds 2-3), as the round-3 block superseded v1.

Own receipts (this seat, read-only, 2026-10-14T17:08Z): selftest rc=0 (line above) and live
`TSUKUROI_CENSUS: DEGRADED` rc=1 — plane lines byte-identical to the 17:02:02Z scribe capture
(`/tmp/w5-tsukuroi-s53-evidence/{selftest,live}.out`; ephemeral). Zero host mutation.

### Drift semantics — the timer plane (TSUKUROI-S5-2, `corpus/knowledge/timer-drift-plane.md`)

Note identity (at append time): 332 lines (`wc -l`), 25 990 B, md5
`fc0760c8070c9387ff5334f0f8c645cc` (mtime 14:11:57 -03; the note moved twice during this
append — 14:09:15 / `d26babc6…` and 14:11:23 / `e0eb297a…` revisions, see Errata). Scope:
**user-scope enabled timers**
(the set the gate's arm reads); system scope stays `journal-boot-plane.md:259-303`.

**Selector realization — "enabled timers" is ambiguous; state the selector.** Literal
`systemctl --user list-unit-files --type=timer --state=enabled` = **1** row (`ai-usage.timer`);
the user-scope inventory closes at 3 unit files (the other two disabled, no
`timers.target.wants` symlink — that, not the `PRESET` column, is why they never run). System
scope holds 5 active timers — a different plane (`timer-drift-plane.md:21-26,47-68,203-217`).

**The gate's `timer_drift` means UNARMED, not schedule drift.** Arm 5 scans each enabled user
timer's `ActiveState` and counts "not `active`"; an unreadable probe →
`timer_unknown` → DEGRADED (`tools/tsukuroi-census.sh:94-97,594-621`). A live `timer_drift=0`
says "every scanned enabled timer is armed" — nothing about its schedule
(`timer-drift-plane.md:243-252`).

**Drift = interval vs the unit's declared window, never a wall-clock grid.** For the one
enabled timer: P = `OnUnitActiveSec` = 300 s, A = `AccuracySec` = 10 s, `RandomizedDelayUSec=0`,
no `OnCalendar` ⇒ the promise is an interval `[P, P+A]`; the timer is monotonic-only
(`NextElapseUSecRealtime` empty, `NEXT` prints `-`). Rules, each from a measurement:
- Compare Δ against **P + A** (+50 ms tolerance), never P: the mode is the window's upper edge
  (1 847 / 2 095 = 88.2 % in `[309.98, 310.02]`); exact `Δ == 310.0` matched 6 / 2 100 — use a
  band, never float equality.
- `NextElapseUSecMonotonic` is the window's **lower bound** (`LastTrigger + P`, measured to
  1 ms over three cycles); fires land up to +A later (+2.55 s, +7.44 s, modal +10.000 s) ⇒ a
  NEXT-vs-wall gap ≤ A is **not drift** — do not "fix" it.
- Pair starts **inside one `_BOOT_ID`**; the 8 boot-boundary gaps (302.6 s … 10 939.0 s) are
  downtime, not drift; `Persistent=true` is inert without `OnCalendar` (no catch-up).
- `NextElapseUSecMonotonic=infinity` alone is **not dead** — transient while the target runs
  mid-cycle (measured; restored within 30 s). Dead = infinity **and** empty `LastTriggerUSec`
  **and** `ActiveState≠active` (the shape the two disabled timers show).
- Trigger→activation latency (~0.6–0.7 ms here) is a **fault** channel (seconds = queued job),
  not a drift channel; run time does not stretch the interval (runtime matters only against
  `TimeoutStartSec`).

Interval history (9 boots, cut at the 14:07:18 fire): 2 109 starts → 2 100 within-boot
intervals; **on-schedule 2 095** (300.0035–310.0093 s), **early/re-arm 5** (each with a named
cause: first-activation + manager-start re-arms, two 10-11 upgrade-phase fires, the 13:06→13:11
manager replacement / round-4 E1 session restart), **late 0** (class defined, unobserved on
this host).

The full class table — `on-schedule` · `not drift` · `early — re-arm (by design)` · `early —
environmental re-arm` · `early — external [unk]` · `late (unobserved)` · `dead (unarmed)` ·
`transient` · `fires into a failing target` · `downtime` · `suspend (counterfactual)` — each
with its read-only verify command and operator action: `corpus/knowledge/timer-drift-plane.md:170-191`;
the non-window intervals' cause table `:193-201`; recheck command set `:270-306`. Census-hook
status: the gate detects the dead class only; adding `LastTriggerUSec` / `AccuracyUSec` /
`NextElapseUSecMonotonic` + the two-clock comparison is a **proposal, not applied**
(`timer-drift-plane.md:243-252`) — nothing in this append changes the gate.

### Errata / pending — round 5 (append)

- 2026-10-14 — **census revision supersession** recorded above: the 26-case / md5 `41953ee9…` /
  976-line pins in the round-2/3 blocks are superseded by the 35-case / md5 `e9327046…` /
  1 032-line hardened revision; both stay visible. Executor checklist step 2 ("26 cases") is
  superseded to `PASS (35 cases, 35 passed, 0 failed)`; its other steps still hold.
- 2026-10-14 — **S5-1's sweep note had not landed** in `corpus/knowledge/` at this append's
  write time (14:11 -03): the ledger above cites the landed tool plus the sweep's own scratch
  (`/tmp/w5-S5-1-work/…`, ephemeral) and the record-draft skeleton
  (`plans/round-5-record-draft.md` §4). When the note lands, the round record productizes
  the citation; the sweep is not to be re-measured from memory.
- 2026-10-14 — **dependencies moved while this append was written** (recorded, not smoothed):
  S5-2's note was re-cut twice (14:09:15 / `d26babc6…` → 14:11:23 / `e0eb297a…` → 14:11:57 /
  `fc0760c8…`; the cut move took the history to 2 100 intervals / on-schedule 2 095 / band
  88.2 %, and corrected two fire wall-instants so the offset reads +2.55 s, not +2.56 s), and
  the record draft grew past this append's first line anchors (hence § refs above). The
  superseded figures stay visible here; the drift section carries the latest revision — re-hash
  and re-read the note before quoting.
- 2026-10-14 — **two-author sweeps of one artifact**: tameshi's round-5 plan sweeps this same
  gate as its third cross-author case (`tameshi-shokunin/plans/round-5.plan.md`). Two
  independent sweeps of one file = two pins, cited separately, never merged (record draft §1
  cross-lane note — `:70-78` in the revision seen); both pins must cite committed bytes.
- Carried (unchanged): root `-Qkk` delta; `offline.db` coverage; round-2 wave-1 errata merge
  into the round-1 blocks; v1 census md5-prefix transcription candidate `:429`; literal
  `source:`/`verified-at:`/`recheck:` keys; `corpus/lessons/round-1.md`; the "20-min cap" item
  (owner: integrator; `executor-test-sufficiency.md` §7 U1).

## Round-6 append — the foreign/AUR risk plane, the baseline turn, and the OOM-event plane (TSUKUROI-S6-4)

Dispatch frame: `plans/round-6.plan.md:3-27` — the owned "foreign/AUR census" surface
(`PROVINCE.md:5-7`) becomes a risk plane; the package and update-safety rows above gain the
foreign-risk rule. Landed siblings distilled here: the register `corpus/knowledge/aur-risk-plane.md`
(S6-1; md5 `1a584300f6b07da78bc8332f04b4fd30`, 341 lines), the freshness receipt
`corpus/knowledge/foreign-provenance-r6.md` (S6-2; md5 `1b8f47a2a807fc8bd2fc7302f15577c8`, 307
lines), and the OOM-event plane `corpus/knowledge/oom-event-plane.md` (S6-3; md5
`7e99d712ead088727c0980e52a121199`, 433 lines — re-cut mid-append, see Errata). This seat's own
read-only re-measurements:
`/tmp/w6-tsukuroi-s64/` (spot-checks named inline). Live counts are captures — re-run, never quote.

### Foreign/AUR risk semantics — `foreign=` is not an AUR claim

Re-measured 2026-10-14: 1188 installed, 207 explicit, **16 foreign** (`pacman -Qm`); all 16
`pacman -Si` **rc=1**, in no configured repo; `pacman -T <all 16>` → empty, rc=0. "Foreign" means
only "unowned by any configured sync db"; the register closes the channel question per package
(`aur-risk-plane.md:28-53`). Two measured classes:

- **`offline-exile` (14: 13 `elephant-*` 2.21.0-1 + `omarchy-walker` 1.0.0-2)** — installed
  2026-10-03 17:44:26 in the installer's one `pacman -S` transaction (`:95-100`); channel =
  `/var/lib/pacman/sync/offline.db` (birth 17:41:33.994, 1275 pkgs, **present but not
  configured** — `pacman -Sl offline` rc=1; `:101-115`); its signatures verify (`Good signature
  from "Omarchy <pkgs@omarchy.org>"`) but `[omarchy] SigLevel = PackageOptional PackageTrustAll`
  never required them (`:117-129`). **No update path and no repair path**: `-Syu` can neither
  upgrade nor reinstall these; a damaged file has no repo source — preserve `offline.db` + the
  channel-A archives before any cache prune (`:214`).
- **`AUR-local` (2: `android-apktool-bin` 3.0.3-1, `obsidian-cli-inspector` 1.0.3-1)** —
  `pacman -U` of `~/.cache/yay/<pkg>/*.pkg.tar.zst` (`:140-150`), `%VALIDATION% = none`,
  signature optional by policy (`LocalFileSigLevel = PackageOptional`, `:166-183`). Residual trust
  is the PKGBUILD text itself (both pin upstream sha256); update path = yay 13.0.1-1 ⇒
  **review-on-update discipline** (diff against the clone before building; do not "fix" the
  missing signature by relaxing policy).

**Risk is a class fold over measured invariants, not a count** (`:195-208`): R1 no-update-path
16/16 · R2 unreviewable artifact 2/16 (channel B only) · R3 unknown packager 16/16 **but no
discriminating power** (36/1188 carry it = the 16 foreign + the 20 omarchy-repo packages;
re-derived by this seat) · R4 dead-channel exile 14/16 · R5 runtime code 14/16 · R6
install-scriptlets 0/16 · R7 outside-`/usr` writes 0/16 · R8 blast radius (13 rows depend only on
the meta package) · R9 staleness (327 d / 182 d / 1 d) · R10 **version crossing** 14/16
(`omarchy-walker → walker` unversioned; walker moved 2.16.2-1 → 2.17.0-1 on 2026-10-11, and
`walker` is in `[omarchy]` while the meta package's own channel is dead) · R11 deps satisfied
today rc=0 · R12 wiring outside the db 16/16. Use `%VALIDATION%` to split the channels, **never**
the packager field (`:218-221`). A channel a read-only probe cannot settle gets an
`unknown-provenance` row plus the exact operator probe — never a guessed channel (`:287-312`);
linkage/ABI questions read `out of reach` and route to kaidoku/revenger (`PROVINCE.md:15-16`).
Live state, re-derived: `elephant.service` active running; `journalctl --user -b | grep -ic
elephant` = 132, error/fail/panic/warn = 0 (`aur-risk-plane.md:227-237`) — a break would surface
as a dead launcher, not a pacman error.

### The baseline turn — specified, not landed (carry the tag)

The gate still reports the bare count: `tools/tsukuroi-census.sh` md5
`e9327046b05b5c71e07fe511ad7e82dd` (1032 lines, round-5 revision), selftest rc=0
`PASS (35 cases, 35 passed, 0 failed)` (this seat, 2026-10-14). The register's §8 (`:314-329`) is
the round-6 baseline contract: a machine-readable baseline (name/version/class/validation/
first_seen) the census reads, `foreign=` reported as known-vs-new, **fail-closed (a new foreign
package or a version change keeps DEGRADED; the baseline may split the report, never lower a
verdict)**, ≥3 fixtures (hit / new / version-drift). It is **not implemented** at this append's
write time — no baseline file exists and the gate is unchanged; verify at round-7 Step 0
(`plans/round-7.plan.md:95-99`), never quote it as landed. The gate-semantics `DEGRADED` bullet
above reads literally until then.

### The OOM-event plane — two classes, entry counts, presence-flag counters

Retained journal (13 boots) holds **two kill waves**, one per class: **event A** a kernel OOM
(2026-10-13 23:44:30, victim `python3` 26.6 GiB anon) and **event B** a SIGKILL class
(2026-10-14 13:10:59, the old session's user manager + helper; round-4 E1)
(`oom-event-plane.md:21-52`).

- **Count rules (entry level).** Event A is 3 kernel lines but **1** err-level entry —
  `-p err` leaves only `Out of memory: Killed process 1732581 (python3) total-vm:56727648kB,
  anon-rss:27873696kB, …, oom_score_adj:200` (PRIORITY=3; `GpuWatchdog invoked oom-killer` and
  `oom-kill:constraint=…` are warn/info) — which is the census's `oom=1` (`:56-72,193-198`).
  Systemd attribution messages count **A → 2, B → 1**
  (`journalctl -b | grep -c "kernel OOM killer killed some processes"` = 3 in total; re-derived)
  — round 4's "single message" for A was one of two (`:389-397`).
- **The census's OOM arm is blind to event B by construction**: in the whole 13:10:55–13:11:12
  window the kernel stream carries 121 records and **zero** OOM-family lines, while same-second
  kernel records prove capture, no ring wrap, and dumps enabled (`:176-199`; re-derived: 121
  records, 0 matches, `oom_dump_tasks=1`, `panic_on_oom=0`). **A round that reports `kerr oom=1`
  while saying nothing about event B is telling the truth about the kernel arm and nothing about
  this class — report the two together** (`:372-375`).
- **The cgroup counter is a presence flag, not a meter.** Two documented waves, yet `user.slice`
  and `user-1000.slice` each read `oom_kill 1` and no live descendant is non-zero (95-file
  sweep) — the subtree that generated event B was destroyed and replaced; the counter lifecycle
  is Q2 [unknown] (`:245-257`). Read it as "an oom_kill has been accounted since this cgroup was
  created"; the event list comes from the journal messages.
- **Pressure anchors that survive a session restart**: `user-1000.slice/memory.swap.peak`
  36 744 949 760 B = 34.22 GiB vs 34.25 GiB total swap (≈99.9 %) and `memory.swap.events.fail`
  5 922 849 (swap-slot allocation failures) — while `memory.peak`/`current` include page cache
  and are **not** pressure readings (`:259-275`; re-derived: swap.peak and fail match). Event A's
  dump: free below the min watermark, `Free swap 44kB` of 35.9 GB, `all_unreclaimable? yes`,
  164-row task table (`:74-119`).
- **No guard was configured on the path**: `MemoryHigh`/`Max`/`SwapMax` = `max`/`infinity`,
  `systemd-oomd` inactive+disabled, `earlyoom` absent, `MemoryPressureWatch=skip` (`:277-281`) —
  nothing acted before the kernel. Prevention levers are operator-owned (detection-only here,
  `:337-353`); the plane's detection contract C1–C6 and reading rules are `:355-375`.
- **Verdict stance**: a measured OOM is a named item (the drivers ring's `[unknown: accepted
  noise floor]`), never bare "noise"; recurrence escalates. Both waves' root causes are
  cross-domain (event B's kill source H1–H3 [unknown], `:215-224`; Q1–Q7 owners in `:377-387`) —
  reported, never absorbed.

### Errata / pending — round 6 (append)

- 2026-10-14 — round-6 arrivals at this append's write time (all untracked in the tree; hashes
  above): `aur-risk-plane.md` (14:44 -03), `foreign-provenance-r6.md` (14:43), `oom-event-plane.md`
  (14:47). The plan's draft name `foreign-aur-risk-plane.md` was superseded by the landed
  `aur-risk-plane.md` (`aur-risk-plane.md:23-24`). The **baseline + census extension is the
  round's one named debt**: specified (`aur-risk-plane.md:314-329`), not landed; the census pin
  above stays current until it is. Scribe prep: `plans/round-6-record-draft.md`.
- 2026-10-14 — **a dependency moved mid-append (recorded, not smoothed).** `oom-event-plane.md`
  was first read at 14:47:49 (md5 `48876876246cc0c961c4145e152f4639`, 432 `wc -l`, 36 122 B) and
  re-cut at 14:48:56 (`7e99d712…`, 433, 36 179 B) before this append's pin was fixed. The delta
  was not localized by this seat (no retained prior copy to diff); every citation in the OOM
  section was re-verified line-aligned against the re-cut revision (victim `:67`, swap `:82`,
  164-row table `:90-92`, 121-record window + `oom_dump_tasks` `:180-187`, 95-file sweep `:249`,
  `swap.peak` `:264`, guards `:351`, the `kerr oom=1`/event-B rule `:374`), and the pin above is
  the re-cut. A later reader must re-hash: a mismatch means the note moved again.
- 2026-10-14 — count restatements elsewhere in this file are left untouched this round because
  the gate did not change: the round-3 checklist step 2 (`:519-520`, "26 cases") and the round-5
  supersession notes (`:600-601`, `:686-687`, "35 cases") remain as history; a future gate
  revision must move them together.
- 2026-10-14 — the OOM plane's own erratum: round-4's single slice-level message is extended to
  the measured 3-message set and the two-wave structure (`oom-event-plane.md:389-403`); the
  counter rule there supersedes any use of `memory.events` as an event count.
- Carried (unchanged): root `-Qkk` delta; the 18/19 sweep-summary split; `1password-beta`
  provenance; `walker-restart.hook` (kagi/operator); dkms stale row; `snapper` empty; the
  "20-min cap" item (owner: integrator); round-4/5 `corpus/README.md` coverage debt (scribe).

## Round-7 append — the watch arms land: `foreign=` known-vs-new, the memory-pressure arm, and the update-safety v2 note (TSUKUROI-S7-4)

Dispatch frame: `plans/round-7.plan.md` (md5 `bb9159549bfdad7516af381f6f12965d`, 10 557 B,
160 `wc -l`) — drafted by PREP-S7 during the round-6 wave, so every round-6 artifact it names is
a **plan**, never landed state. **The plan's claim (a) fifth plane (`PLANE update-safety`) and
claim (b)'s round-2 errata pointer were not in the tree at this append's write time
(2026-10-14T18:52Z)** — both carried, with the tag, in the errata block below. What landed and is
distilled here: the census revision (`tools/tsukuroi-census.sh` — TSUKUROI-S7-1's foreign-baseline
watch, round-6's named debt finished, plus TSUKUROI-S7-2's memory-pressure arm), the independent
verification of the baseline arm (`corpus/knowledge/aur-risk-plane-ver-s7.md`, VER-S7), and the v2
decision note (`corpus/knowledge/update-safety-v2.md`, TSUKUROI-S7-3). **Landed names win over
draft names:** the plan's `update-safety-plane.md` landed as `update-safety-v2.md`. This seat's
own read-only receipts: `/tmp/w7-tsukuroi-s74/` (`probes.out`, `census-receipts.out`,
`census-r2-receipts.out`, `poll.log`; ephemeral). Counts below are captures — re-run, never quote.

### Census revision — the two new arms on the four planes (supersedes the round-5 pin)

- **Identity check** (replaces the round-5 `md5sum` line `:619-623`): `md5sum
  tools/tsukuroi-census.sh` = `e2c4558a3ae4ddd2eca67e8f4d64281c` · sha256
  `bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55` · 1472 `wc -l` · 73 919 B
  (mtime 2026-10-14 15:33:21 -03). **Uncommitted at this append's write time** (`git status` =
  ` M`; HEAD still `dc3436d`): the round-7 commit should pin these bytes — re-hash after the
  commit, and on mismatch **stop and re-measure** before trusting any rule here. The banner still
  reads `census-v2`; identity is by hash, not version string (round-5 rule, kept). This supersedes
  the round-5 35-case / `e9327046…` / 1032-ln pin and the round-3 26-case / `41953ee9…` / 976-ln
  pin.
- **Selftest** (own run 2026-10-14T18:39:37Z, rc=0, fixture byte-unchanged — zero mutation):
  verbatim `TSUKUROI_CENSUS_SELFTEST: PASS (49 cases, 49 passed, 0 failed)` = 35 legacy + **6
  foreign-baseline** (round-6 debt: hit / embedded-default / new / version-drift / gone / absent)
  + **8 memory-arm** (labels carry `(S7-2)`).
- **Live contract unchanged in shape** — four `PLANE` lines + rollup, exit map 0/1/2; the new arms
  ride existing lines (`mem=` on the drivers line, `foreign=` inside the packages note). Own run
  2026-10-14T18:39:42Z (rc=1), verbatim:

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T18:39:42Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2[user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922849 C5_swap_peak_pct=99% C5_pswp=72118991/93920636 C5_sock_throttled=67558; C6_psi_some_avg300=0.00 C6_psi_full_avg300=0.00 C6_psi_full_total_us=68625258 C6_avail_kb=19678812 C6_shmem_kb=6517900; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=442 (coredump=279 kernel=139 other=24); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED)
```

  (Read-only verified: `git status` byte-identical before/after, no `db.lck` created, live mode
  writes nothing — the round-2 guarantee still holds.)
- **New arm 1 — the foreign watch** (lane S7-1; finishes round 6's *specified, not landed* baseline
  contract, `plans/round-6-record-draft.md §4`):
  - realized note string: `foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16)` — `known` = a
    live `pacman -Qm` row matching the baseline at the same version; `new` = live row absent from
    the baseline; `drift` = version differs (printed `name(old->new)`); `gone` = baseline row no
    longer installed (never silently dropped). Each non-empty class is named in the note.
  - baseline source: the gate's **embedded** r6 snapshot (`R6_FOREIGN_BASELINE`, 16 rows = the
    register's §1 rows, `aur-risk-plane.md:55-89`), unless `TSUKUROI_FOREIGN_BASELINE` points at an
    external `name<TAB>version` file — the register's proposed standalone `.tsv` **stayed a
    proposal** (no `*baseline*` / `*.tsv` file in the tree at write time). `base=` reads
    `r6(16)` | `file(n)` | `absent` | `unreadable`.
  - **fail-closed both ways**: any `new`/`drift`/`gone` → DEGRADED with names; an absent/unreadable
    baseline prints `foreign=<n>(base=absent [known/new/drift/gone unknown])` and stays DEGRADED —
    never HEALTHY off a missing baseline; an unreadable `-Qm` prints `foreign=? [pacman -Qm
    unreadable]`.
  - independent verification: `aur-risk-plane-ver-s7.md` (VER-S7; md5 `4608743d…`, 184 ln):
    **CONFIRMED** — the count and the fold reproduce from the verifier's own probes, the embedded
    baseline is identical to the register's 16 rows, and all four fail-closed branches fire and
    name their class.
- **New arm 2 — the memory-pressure arm** (lane S7-2; `mem=[HEALTHY|DEGRADED|BLOCKED]` appended to
  the drivers note; `DRV_V=$(worse "$DRV_V" "$MEM_V")` — the arm can only worsen the drivers
  verdict, never raise it):
  - vocabulary: the round-6 OOM note's detection contract C1–C6 (`oom-event-plane.md` §8; cited in
    the line as `r6 vocab: oom-event-plane.md §8`) — C1 kernel OOM entries (the ring's `oom=`
    source), C2 systemd attribution (`kernel OOM killer killed some processes` — the only
    attribution for a session-wide SIGKILL class that leaves no kernel record), C3 SIGKILL/teardown,
    C4 cgroup `memory.events[.local]` oom_kill **presence flags, never meters** (round-6 rule),
    C5 swap-pressure anchors (`swap.events fail`, `swap.peak` vs meminfo `SwapTotal`,
    pswpin/pswpout, `sock_throttled`), C6 live shape (PSI avg300/total, `MemAvailable`, `Shmem`)
    plus the guards shape (`memory.max/high`, `oom.group`).
  - pass = every signal readable and every class 0; degrade = any class > 0 **or** any required
    signal unreadable (named in `unknown=[…]`, never silent); block = cgroup sweep empty **and**
    all three journal probes unusable. `journalctl --grep` rc=1 means "0 entries"; any other
    non-zero rc means "unreadable".
  - measured this run (above): `mem=[DEGRADED]` with `C1=1 C2=3 C3=3`, `C4_present=2`, `C5_swap_fail=5922849`,
    `C5_swap_peak_pct=99%`, `guards=max/max` — the round-6 two-wave state **re-measured, not
    quoted** (the arm keeps no cross-run state; new-vs-baseline is the class presence plus the
    note's recheck ledger). `memory.peak` stays out of the line — page-cache-inclusive, not a
    pressure reading (round-6 rule kept). Cost of the arm, from its own header note: ≈0.3 s of a
    ≈1.1 s gate run.
- **Count restatements — now moved together** (the round-6 deferral at `:829-832` is void, a gate
  revision having landed): the round-3 executor-checklist step 2's "`PASS (26 cases, 26 passed,
  0 failed)`" (`:519-521`) and the round-5 blocks' "35 cases" (`:600-602`, `:686-688`) stand as
  history; the current expected line is `PASS (49 cases, 49 passed, 0 failed)` at the identity pin
  above. `--sample N` default 8 and the `TSUKUROI_*` fixture-only override rule are unchanged.

### The v2 decision note — class × update-path (`corpus/knowledge/update-safety-v2.md`)

- Identity at write time: md5 `92803aea74ebeb1598fa4f450489e5d2`, 353 `wc -l` / 28 825 B (mtime
  15:25:40 -03). Scope: the round-2 note **re-run** (all 16 pins re-measured) with the round-6 AUR
  classes **joined** — the follow-up the round-2 model could not answer: "and what would that
  `-Syu` never touch?" The census plane (claim (a)) is explicitly not this file.
- The join (note §4; rows verbatim there): `official-sync` (everything repo-resolved, incl. the 26
  `[omarchy]` rows) — `-Syu` upgrades/reinstalls; `aur-local` (2: `android-apktool-bin` 3.0.3-1,
  `obsidian-cli-inspector` 1.0.3-1) — `-Syu` reach **none** (`pacman -Si` rc=1), helper-only (yay;
  review-on-update; upstream state [unknown]); `offline-exile` (14: 13 × `elephant*` 2.21.0-1 +
  `omarchy-walker` 1.0.0-2) — **no update or repair path from any repo**; the only safe operations
  are preserve (`offline.db` + the cached archives/sigs, before any prune) and observe
  (journal-watch the launcher after any `walker` upgrade); `unknown-provenance` (rule, 0 rows
  today) — the register's probe order, in order: pacman.log `-U` grep → `~/.cache/yay/<pkg>/` →
  `pacman -Qi` *Validated By* → `offline.db` listing; **a class is never guessed**; `out-of-reach`
  — the `walker` 2.17.0 vs elephant 2.21.0 linkage question routes to kaidoku/revenger, never
  absorbed.
- The reading it adds: round 2's "empty ≠ up to date" gains its second half — **"resolvable ≠
  maintainable"**: an `-Syu` reporting 0 actions says nothing about the ~357 MiB of installed code
  no configured repo can reach.
- Receipts worth keeping: the 16 r2 pins re-run all "**same**" (incl. `-Qu` rc=1 empty, db births
  2026-10-11 12:54:13.542, foreign 16, `snapper list-configs` 0 configs, dkms stale row) —
  same-value, *not* independent confirmation (no pacman activity since 2026-10-13 16:37); the
  `-Suu` downgrade trap upgraded from [inference] to **measured** (`pacman -Suu --print-format` →
  exactly one action, `omarchy/1password-beta 8.12.42_32.BETA-1` — the r2 note's `:374-375` "do not
  run" is now a printed plan); `/boot` rc=2 BLOCKED stands; hazards U1–U8 refreshed (rollback net
  0 configs; dkms stale `7.1.4-arch1-1`; cache 8.6 G unpruned; trust surfaces unchanged).
- Boundary kept: the note wrote only itself and named its owed items (the round-2 errata pointer,
  LOG entry, README rows, the census plane) — recorded here, not absorbed.

### Errata / pending — round 7 (append)

- 2026-10-14 — **plan claim (a), the fifth plane, is not in the landed gate at this append's write
  time.** The pinned revision carries four planes + the two new arms above; there is no `PLANE
  update-safety` emitter and no fifth rollup term (checked 18:52Z against `e2c4558a…`). If a later
  revision lands it, re-hash first, run `--selftest`, and quote the **realized** note line and the
  realized gate-verdict mapping (the plan proposes INERT/PASS→HEALTHY,
  REQUIRES-PREP/UNKNOWN-UPSTREAM→DEGRADED, BLOCKED→BLOCKED, DO-NOT as note content —
  `plans/round-7.plan.md:52-79`); the arm vocabulary and composition already have a measured model
  in the round-2 block above (`:359-381`) and in the v2 note.
- 2026-10-14 — **round-2 note errata pointer still owed**: `update-safety-note.md` unchanged at md5
  `5cc3067fec33d261d8bff6a5c7e8ac48` / 478 ln at write time.
- 2026-10-14 — **the standalone baseline file stayed a proposal**: the realized baseline is the
  gate's embedded r6 snapshot (register `:314-329` and round-6 draft `:252-293` both remain
  proposals). Quote the realized shape (`base=r6(16)`), not the proposal.
- 2026-10-14 — **round-7 write scopes observed, not absorbed**: S7-3 wrote only its note; SCR-S7
  only the record draft; VER-S7 only its verification note; this seat only this append. Still owed
  at write time: the `SCORECARD.md` round-7 move row, the `LOG.md` entry, and `corpus/README.md`
  coverage rows (rounds 4-6 collapsed debt) — scribe lane.
- Carried (unchanged): root `-Qkk` delta; the 18/19 sweep-summary split; `1password-beta`
  provenance; `walker-restart.hook` (kagi/operator); dkms stale row; `snapper` empty; the "20-min
  cap" item (owner: integrator); round-4/5/6 `corpus/README.md` coverage debt; the round-2 wave-1
  errata merge. `plans/round-8.plan.md` (PREP-S8 draft) proposes the OOM plane as its own census
  plane — a plan, not landed state.