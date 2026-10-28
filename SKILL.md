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
- Route shared host findings by the question, not the tool: `PROVINCE.md`
  §Adjacent gives the seven finding-to-owner handoffs and sanitized evidence
  checklist. Keep OS diagnosis here; record a reported packet separately from
  recipient acceptance. Executed example and source pins:
  `corpus/knowledge/adjacency-handoffs-fleet-r1.md`.

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

## Round-8 append — the verified OOM arm and the kill-event classes (TSUKUROI-S8-4)

Dispatch frame: `plans/round-8.plan.md` (md5 `0bef822da196368c47c56426063990fe`, 14 592 B, 216
`wc -l` / 217 as read — unterminated final line; committed in `aa136d6`). The plan's move is the
**OOM/kill-event watch joining the census** as a new plane line + new-vs-baseline rows; **that arm
had not landed at this append's write time** (block below). What this append lands in the playbook
is the **verified** OOM arm (round 7's S7-2 memory-pressure arm, non-author-verified in round 8)
and the **kill-event classes** (round 8's deep capture). Distilled sources, both re-hashed by this
seat: `corpus/knowledge/memory-arm-ver-s8.md` (VER-S8; md5 `861d83ad5a120487507b167236ee3cd0`,
251 `wc -l` / 252 as read, unterminated final line) and `corpus/knowledge/kill-event-deep-r8.md`
(S8-2; md5 `6685e1da443f5d368cd41584d2b9943e`, 340 `wc -l` / 341 as read, unterminated final
line). Supporting evidence: `corpus/knowledge/memory-arm-mutants-s8.md` (S8-1; md5
`a09e5604a9a818f38096569365d48823`, 181 `wc -l`). This seat's own read-only re-probes are named
inline. Counts are captures — re-run, never quote.

**Gate identity (unchanged this round).** The round-7 pin still stands: `md5sum
tools/tsukuroi-census.sh` = `e2c4558a3ae4ddd2eca67e8f4d64281c` · sha256
`bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55` · 1472 `wc -l` / 73 919 B
(re-hashed by this seat; = HEAD `aa136d6` blob — `memory-arm-ver-s8.md:21-26`). No round-8 census
revision landed in the round-8 window (`memory-arm-ver-s8.md:29-30,184-188`). A mismatch on a later
read means the gate has moved — stop and re-measure before trusting any rule here.

### The OOM arm as landed — `mem=` on the drivers line (S7-2, round 7)

The memory-pressure arm rides the **drivers** plane's note and verdict; there is no separate plane
line in the landed revision. `DRV_V=$(worse "$DRV_V" "$MEM_V")` — the arm can only worsen the
drivers verdict, never raise it (`tools/tsukuroi-census.sh:790-801`). Its vocabulary is the round-6
OOM note's detection contract C1–C6 (`corpus/knowledge/oom-event-plane.md` §8; the line cites it as
`r6 vocab: oom-event-plane.md §8`), as implemented at `tools/tsukuroi-census.sh:100-135,688-801`:

- **C1** kernel OOM dump entries (`journalctl -k -b -p err -o json` + the OOM regex — the same
  source and semantics as the ring's `oom=` class) · **C2** systemd OOM attribution
  (`kernel OOM killer killed some processes`, PRIORITY=5 — the only attribution for a session-wide
  SIGKILL class that leaves no kernel record) · **C3** SIGKILL/teardown
  (`status=9/KILL|Failed with result '(signal|oom-kill)'`) · **C4** cgroup `memory.events[.local]`
  `oom_kill` **presence flags, never meters** · **C5** swap-pressure anchors (`swap.events fail`,
  `swap.peak` vs meminfo `SwapTotal`, `memory.stat` pswpin/pswpout, `sock_throttled`) · **C6** live
  shape (PSI `avg300`/`total`, `MemAvailable`, `Shmem`) plus the guards shape (`memory.max/high`,
  `oom.group`).
- **pass** every signal readable and every class 0 · **degrade** any class > 0, or any required
  signal unreadable — named in `unknown=[…]`, never silent · **block** cgroup sweep empty **and**
  all three journal probes unusable (fail closed, same stance as the ring arms).
- `journalctl --grep` rc=1 means "0 entries"; any other non-zero rc means "unreadable"
  (`tools/tsukuroi-census.sh:118-125`). `memory.peak` stays out of the line — page-cache-inclusive,
  not a pressure reading (round-6 rule kept). Arm cost ≈0.3 s of a ≈1.1 s gate run.

Realized arm line at the pin (VER-S8's own run, `memory-arm-ver-s8.md:47`; the drivers line
verbatim — a capture, re-run before quoting):

```
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2[user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922849 C5_swap_peak_pct=99% C5_pswp=72315769/94058025 C5_sock_throttled=67558; C6_psi_some_avg300=0.04 C6_psi_full_avg300=0.04 C6_psi_full_total_us=69186087 C6_avail_kb=19155736 C6_shmem_kb=6935768; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
```

The round-6 two-wave state is **re-measured, not quoted** — the arm keeps no cross-run state
(new-vs-baseline is the class presence plus the note's recheck ledger).

### The verification — VER-S8 `CONFIRMED`, AUD-X7 closed

The round-7 queued gap `AUD-X7` ("S7-2's memory arm has no non-author verification", `LOG.md:170`)
is closed by VER-S8. Verdict verbatim (`memory-arm-ver-s8.md:32-40`):

> **Verdict: CONFIRMED — AUD-X7 is closed for the S7-2 memory arm as landed at `e2c4558a…`, with
> coverage debt named, not smoothed. 0 live measurement claims refuted.**

- **Independent replay of S8-1's 11-defect set**: 8 killed / 3 survived / 0 inconclusive (73 %);
  control green; restore OK; **all 11 mutant sha256s reproduce byte-for-byte**, all 11 verdicts and
  the per-case attribution reproduce (D2–D8 kill exactly their owning case; D1 kills 10)
  (`memory-arm-ver-s8.md:80-103`; S8-1's own sweep `memory-arm-mutants-s8.md:95-117`).
- **What "verified" rests on**: the 8 shipped `(S7-2)` selftest cases each kill a defect of exactly
  their own contract clause — 8/8 own-case kills, D2–D8 each uniquely the only failing case of 49
  (`memory-arm-mutants-s8.md:112-117`). The non-author pass reproduces the mutant bytes and adds
  its own 16-defect set (11 killed / 5 survived / 69 %, prediction score 15/16) and a 15-case
  fail-closed battery (`memory-arm-ver-s8.md:105-166`).
- **Coverage debt, named — 9 clause sites un-exercised by the 49-case suite** (S8-1's D9/D10/D11;
  VER-S8's M04/M06/M10/M12/M15; plus M17, the `C5-stat` sibling S8-1 left **unmeasured**). Each is
  detected by at least one case in VER-S8's battery, so the debt is suite coverage, not undetectable
  semantics (`memory-arm-ver-s8.md:177-181,149-166`). The shipped suite is **not** to be described
  as clause-complete.
- **Kept, not smoothed**: VER-S8's own prediction error on M01 (killed via a dispatcher
  routing coupling, not a semantic assertion — `:170-176`); method delta (S8-1 swept a `/tmp` byte
  copy, VER-S8 the repo file directly — identical mutant bytes, same outcome, `:189-190`); the live
  *unreadable* states stay [unknown] (hermetic fixtures only, `:192-204`).
- **Still open**: the round-8 half of the plan's measure — the new `PLANE oom` watch + ≥2 baseline
  rows re-executed by a non-author — is **not verifiable at this pin**: nothing landed
  (`memory-arm-ver-s8.md:184-188`). `AUD-X7`'s closure covers the **S7-2 memory arm**, not a round-8
  arm.

### The kill-event classes — two kill waves, two classes (S8-2)

`corpus/knowledge/kill-event-deep-r8.md` (S8-2) deepens the round-6 OOM note: `verified-at`
2026-10-14 16:11:54–16:25 -03, non-root, boot id `d7f0bc8d938e4249b4a1f250cbfacf58`, kernel
`7.2.3-arch1-3`, systemd `261.2-1-arch`. Event A = 2026-10-13 23:44:30 kernel OOM (victim
`python3`); **event B** = 2026-10-14 13:10:59 SIGKILL class. Its headline (F1–F8,
`kill-event-deep-r8.md:26-37`):

| F | finding |
|---|---|
| F1 | **No kernel OOM kill happened at event B** — `/proc/vmstat oom_kill` = 1 (event A only); exactly 1 `Out of memory: Killed process` line; **0** `Memory cgroup out of memory` prints in 13 boots; the 13:10:59 second carries no kernel OOM/kill record |
| F2 | Message #3 is **teardown-coincident, not kill-coincident** — 0.45 ms after `user@1000.service: Consumed …`, repeating a counter value event A set |
| F3 | **Counter map**: kernel `memory.events` non-zero only at `user.slice` + `user-1000.slice` (each `oom_kill 1`; `.local` 0); systemd `OOMKills=`: `user-1000.slice` 1, `user.slice` 0; no counter reads 2; no live descendant carries the slice's 1 |
| F4 | **Complete uid-1000 turnover** — zero vgpnk processes survive from before 13:10:59; earliest live start 13:11:07 |
| F5 | **Event B's pre-kill memory picture is not retained** — every surviving memory signal is a lifetime max or cumulative counter; the 34.2 GiB swap peak is undatable to 13:10:59 and consistent with event A |
| F6 | **Launch-count trap** — app scopes leave no deactivation record (0 `app-*.scope: Deactivated` in boot 0 and boot −1; 0 against 98 starts this session) |
| F7 | **The OOM-score class argues against a kernel kill** — the session ran +200/+300, the manager +100; what died was the +100 manager |
| F8 | Prevention table refined; new rows for the pre-kill capture gap and the kernel-kill ledger |

The **class table** (each row a read-only signature, measured here):

| class | signature (read-only) | measured | verdict stance |
|---|---|---|---|
| kernel OOM kill (global) | `-p err` entry `Out of memory: Killed process …`; `/proc/vmstat oom_kill` ledger | event A only: 1 print, ledger **1**; `journalctl -k -g oom` = 5 lines over all boots, all at 23:44:30 (`kill-event-deep-r8.md:333-334`; this seat re-derived both) | a named item — never bare "noise" |
| memcg-limit OOM | `Memory cgroup out of memory` print | **0** in 13 boots (`:244,333-334`) | absent; and with `memory.max/high/swap.max/zswap.max` all `max` and `oom.group` 0, the limit trigger is closed |
| systemd attribution report | `kernel OOM killer killed some processes` (PRIORITY=5) | **3** messages: A→2, B→1 (`:85-99`) | a report **about the named unit**, never evidence of *when* a kill happened; the only attribution for a class with no kernel record |
| session SIGKILL / teardown | `status=9/KILL` / `Failed with result 'signal'` | **1** line — the old user manager PID 1573 (`:198-207`) | the event-B class; **the kernel arm is blind to it by construction** |
| teardown purge | `KillMode=mixed` + `TimeoutStopSec=5s` drop-in | 0 uid-1000 survivors from before 13:10:59 (`:212-223`) | [inference] mechanism, not trigger |
| cgroup `oom_kill` counter | `memory.events[.local]` | **presence flag**: 2 slices × 1, `.local` 0 (`:120-134`) | flag, never an event count (round-6 rule re-confirmed) |
| scope-launch record | `Started app-*.scope` | 69 old / 98 new, **0** deactivations (`:225-238`) | launches, never live units |

Reading rules this capture fixes, each re-measurable:

- **The census's `oom=1` is the kernel arm and nothing else.** In the whole 13:10:55–13:11:12
  window the kernel stream carries 121 records and **zero** OOM-family lines, while same-second
  records prove capture/no-wrap/dumps-enabled (`:70-73,176-199`). A run reporting `kerr oom=1`
  while saying nothing about event B is telling the truth about the kernel arm and nothing about
  the SIGKILL class — **report the two together** (round-6 rule, re-confirmed).
- **Counters are presence flags.** The surviving `oom_kill 1` is event A's charge, propagated up
  and surviving the subtree's removal; `.local` stays 0 at ancestors; no live descendant is
  non-zero (`:120-134`; narrows round 6's Q2, does not close it).
- **Peaks are lifetime maxima, not dated snapshots.** `memory.peak`/`memory.swap.peak` span the
  whole cgroup life; the 99.907 % swap peak cannot be assigned to 13:10:59
  (`:156-189`). The discriminator is the *new* service (3.2 h): `swap.peak` 3,171,446,784 B,
  `swap.events fail` 4, vs the slice's cumulative 5,922,849 — unchanged since round 6's reading.
- **There is no non-root-readable pre-kill snapshot, and none can be backfilled** — `sar`/`atop`/
  `dool`/`dstat` absent, no `/var/log/sa`, `systemd-cgtop` live-only, PSI live-only, `dmesg`
  BLOCKED (`:190-193`). Report the missing capture capability as a standing row.
- **H1–H3 updated**: H1 (kernel path ran, print lost) is **strongly disfavoured** — the ledger
  never moved, no memcg prints, no limits on the path, so the residual needs print *and* counter
  *and* dump lost at once with no positive evidence; H2 (non-kernel SIGKILL, systemd bookkeeping)
  is supported with the **sender still [unknown]**; H3 (deferred report of the Oct-13 wave) is
  **strengthened** (`:240-246`). **No round resolves H1–H3** (read-only unmeasurable) — carry both
  readings.
- **Proposed errata E4–E8** for `oom-event-plane.md` (the round-6 §3.2/§5 dating, §4.2 counter,
  §3.5 H1, §1/§6.2 helper `9` + the 2-vs-1 `status=9` sweep discrepancy, §1/§3.4 launch counts)
  are **proposed rows in `kill-event-deep-r8.md:268-285`, not applied** to that note; the note's
  owner applies them.

### The round-8 watch — specified, not landed (carry the tag)

The plan's claim (a) (`PLANE oom` as the census's next plane line) and claim (b) (a
new-vs-baseline watch, `corpus/knowledge/oom-event-baseline.tsv`) are **not implemented** at this
append's write time: the census is unchanged (`e2c4558a…`, 1472 `wc -l`), no `PLANE oom` emitter
exists, no `*baseline*` / `*.tsv` file exists in the tree (`memory-arm-ver-s8.md:184-188`; this
seat re-checked). Quote the realized string when it lands, **never the proposal**. Two proposal
points worth carrying: the plan's C1 is a **retained-window** scan where the landed arm's C1 is
boot-scoped (`-b`); and the proposed arm words/composition
(CLEAN → HEALTHY; NEW / DECLARED-MISSING / NO-BASELINE → DEGRADED; BLOCKED → BLOCKED; composition
BLOCKED > {NEW, DECLARED-MISSING, NO-BASELINE} > CLEAN) must be adjudicated against the realized
round-7 mapping mechanism (`plans/round-8.plan.md:104-115`).

### Errata / pending — round 8 (append)

- 2026-10-14 — **census pin unchanged**: the round-7 identity pin (`e2c4558a…`, 1472 `wc -l`)
  still stands; re-hashed by this seat. Count restatements stand as history: the round-3 checklist
  step 2's "26 cases" (`:519-521`), the round-5 "35 cases" (`:600-602`, `:686-688`), and the
  round-7 "49 cases" (`:866-868`) — the **current expected line** is `PASS (49 cases, 49 passed,
  0 failed)`; a future gate revision must move them together.
- 2026-10-14 — **`AUD-X7` closed by VER-S8** (`memory-arm-ver-s8.md:32-40`), scope = the S7-2
  memory arm at `e2c4558a…`; the round-8 `PLANE oom` arm's own non-author verification is a
  separate, still-open item (`memory-arm-ver-s8.md:184-188`). No `AUD-S8` artifact exists in the
  tree at this write time (checked) — the VER-S8 note is the round-8 verdict source.
- 2026-10-14 — **S8-1's §8 open item measured**: the `C5-stat` sibling mutant it left "named as
  unmeasured" (`memory-arm-mutants-s8.md:181-182`) was swept by VER-S8 as M17 — **SURVIVED** the
  shipped suite, caught by battery case B15 (`memory-arm-ver-s8.md:163-166`). The debt is named,
  not closed by a gate edit.
- 2026-10-14 — **write scopes observed, not absorbed**: S8-1 wrote only its note (no gate edit,
  `memory-arm-mutants-s8.md:7-8,140-141`); VER-S8 wrote only its note and `/tmp` scratch; S8-2
  wrote only `kill-event-deep-r8.md` and proposed E4–E8 without applying them; this seat wrote
  only this append. Owed at write time (scribe lane): the round-8 `LOG.md` entry, the
  `SCORECARD.md` round-8 move row, and `corpus/README.md` coverage rows (rounds 4-7 collapsed
  debt).
- Carried (unchanged): root `-Qkk` delta; the 18/19 sweep-summary split; `1password-beta`
  provenance; `walker-restart.hook` (kagi/operator); dkms stale row; `snapper` empty; the "20-min
  cap" item (owner: integrator); round-4/5/6/7 `corpus/README.md` coverage debt; the round-2
  wave-1 errata merge; round-6's H1–H3 / Q1–Q7; the OOM-plane counter-lifecycle Q2 (narrowed by
  S8-2, not closed).

## Round-9 append — the fifth plane lands: `PLANE update-safety` in the 5-plane census (TSUKUROI-S9-4)

Dispatch frame: `plans/round-9.plan.md` (md5 `3a59d2edd068abf6281d7701d261ea5c`, 19 509 B,
270 `wc -l` / 271 as read — unterminated final line; committed in `72b038d`). The plan's move is
the **update-safety plane joining `tools/tsukuroi-census.sh`** as the fifth plane line — round-7
claim (a), carried *not landed* through rounds 7 and 8, is finished from its own measured model.
Landed siblings distilled here: the census revision (lane S9-1) and the AUR watch's first drift
receipt `corpus/knowledge/aur-drift-receipt-r9.md` (lane S9-3; md5
`e7d6f70b65e4846ad7001b5a66e8ec73`, 248 `wc -l`). This seat's own read-only receipts:
`/tmp/w9-tsukuroi-s94/` (`selftest.final.out`, `live.final.out`, `live.final2.out`,
`gitstatus.*`; ephemeral). Counts below are captures — re-run, never quote.

### Census revision — the fifth plane (supersedes the round-7/8 pin)

- **Identity check** (replaces the round-7 `md5sum` line `:857-865`; the round-8 block's "gate
  identity unchanged" `:1001-1006` is superseded with it): `md5sum tools/tsukuroi-census.sh` =
  `0f72f4cfaf539e3dd21ab5acbede1965` · sha256
  `301141e7258df4454a084b91b7129af18132b7627aa3d3d78945a0c2bd368fa8` · 2011 `wc -l` · 103 235 B
  (mtime 2026-10-14 17:09:39 -03). **Uncommitted at this append's write time** (`git status` =
  ` M`): the round-9 commit should pin these bytes — re-hash after the commit, and on a later
  mismatch **stop and re-measure** before trusting any rule here. The banner still reads
  `census-v2`; identity is by hash, not version string (round-5 rule kept). The header records
  why the version string did not move and that a bump is the note seat's call
  (`tools/tsukuroi-census.sh:33-38`)
- **Selftest** (own run 2026-10-14T20:10:48Z, rc=0, fixture byte-unchanged — zero mutation):
  verbatim `TSUKUROI_CENSUS_SELFTEST: PASS (63 cases, 63 passed, 0 failed)` = 49 legacy (35 base
  + 6 foreign-baseline + 8 S7-2 memory-arm) + **14 update-safety cases** (`(R9)`, block
  `tools/tsukuroi-census.sh:1861-1949`; the plan proposed ≥4).
- **Live contract** — five `PLANE` lines + the rollup; exit map unchanged (0/1/2, worst plane
  wins), and the rollup parenthetical gains its fifth term (`update-safety=<verdict>`). Own run
  2026-10-14T20:10:48Z (rc=1), verbatim:

```
tsukuroi-census census-v2 — host=plazir27 — 2026-10-14T20:10:48Z — read-only
PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=8(1password-beta,1password-cli,7zip,aalib,abseil-cpp,acl,adwaita-cursors,adwaita-fonts) drift=2[1password-beta,1password-cli] backup_diffs=0 nonroot_artifacts=0; foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16); pins=none; holds=pacman glibc; db.lck=absent)
PLANE systemd: HEALTHY (scope=user state=running failed=0 timers_enabled=1 timers_scanned=1 timer_fail=0 timer_unknown=0)
PLANE drivers: DEGRADED (ring=journalctl-k dmesg_restrict=1 kerr=139 (oom=1 io=70 gpu=0 other=68) [unknown: accepted noise floor]; nvidia=present smi=610.57.04 modules=4 nodes=6 pci_10de=2; mem=[DEGRADED] C1_kernel_oom=1 C2_sysd_oom=3 C3_sigkill=3; C4_sweep=190 C4_present=2[user.slice,user.slice/user-1000.slice] C4_local=0; C5_swap_fail=5922897 C5_swap_peak_pct=99% C5_pswp=74004334/96405737 C5_sock_throttled=73247; C6_psi_some_avg300=0.00 C6_psi_full_avg300=0.00 C6_psi_full_total_us=72403325 C6_avail_kb=18111272 C6_shmem_kb=6586876; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)
PLANE journal: DEGRADED (boots=13 current=yes target=graphical.target:active err=797 (coredump=522 kernel=139 other=136); failedhist=8[app-com.onepassword.OnePassword@autostart.service,app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service,app-walker@autostart.service,init.scope,-.slice,user@1000.service]; timers_enabled=1 timers_scanned=1 armed=1 timer_drift=0 timer_unknown=0)
PLANE update-safety: DEGRADED (status=UNKNOWN-UPSTREAM; pending=none; qu=rc=1/0; sup=0; join=equal=1171 behind=0 ahead=1 src=sl+expac; expac=agree; chan=dbs=4 fetch=3d stamp=36d; offline.db=present(stamp=85d birth=10d); log=cmd=-S@2026-10-13T16:37:58-0300; refresh=none-in-window(last 300 lines); classes=offline-exile:14,aur-local:2; trap=-Suu:1[omarchy/1password-beta 8.12.42_32.BETA-1]; traps=[-Qu blind to shadowed-newer; '%s' is not a size]; vocab: SKILL.md:358-368)
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED)
```

  Read-only verified: `git status --short` byte-identical before/after, no `db.lck` created,
  live mode writes nothing (the round-2 guarantee still holds). A second run at 20:11:46Z
  printed the plane line byte-identical; wall ≈2.3 s versus the four-plane 0.69–1.75 s band —
  a real cost move, recorded in the header (`:253-259`), not trimmed by dropping a probe.

### The plane as landed — probes, arms, mapping (`probe_update_safety`, `:1081-1352`)

Arm vocabulary and composition are the round-2 note's (`update-safety-note.md:334-339`,
restated at `SKILL.md:358-368`, which the line itself cites as `vocab: SKILL.md:358-368`):
`PASS · INERT · REQUIRES-PREP · BLOCKED · UNKNOWN-UPSTREAM · DO-NOT`, strongest fired wins,
`BLOCKED > UNKNOWN-UPSTREAM > REQUIRES-PREP > INERT > PASS`.

- **Channel reading** — every repo `*.db` under `$PACMAN_DB/sync`: **births** (`stat -c %W`, the
  local fetch instant) and **content stamps** (`stat -c %Y`, the db file's mtime — upstream's own
  file stamp preserved at download, the freshness that matters). `offline.db` is excluded by
  construction (`CHANNEL_ARCHIVE`, `:309`): it is the offline-exile preservation archive, not a
  configured channel — the 2026-07-20 stamp would drag an age it does not own; it gets its own
  `offline.db=` row. The line prints `chan=dbs=N fetch=<age>d stamp=<age>d`; an unreadable stamp
  is named (`stamp_unreadable=[…]`), never dropped.
- **Candidates, two ways + disagreement rule** — `pacman -Qu` **unpiped** (rc 1 + 0 lines =
  empty; rc 0 + n > 0 = candidates; any other shape = unreadable → `status=BLOCKED`, **never
  INERT** — the pipeline-rc trap made executable, case `(R9)` `:1882`), cross-checked against
  the allowed plan verb `pacman -Sup --print-format '%r/%n %v'`; on disagreement the **larger**
  count wins and the disagreement is printed (`disagree[qu=X sup=Y]`, fail closed).
- **Third reading — the repo-side version join** — `pacman -Sl`, **first occurrence per name =
  pacman's own repo order** (the r2 note's last-wins `expac` trap `:403-411` is why first-wins),
  `vercmp` for direction; `expac -S` cross-checks it when present. The line prints
  `join=equal=… behind=… ahead=… src=sl|sl+expac`, plus `expac=agree|partial|disagree|absent|rc=…`
  and `join=unavailable(q=rc=… sl=rc=…)` — an absent `expac` prints `expac=absent`, never a
  silent pass (cases `(R9)` `:1937`, `:1942`).
- **Class fold (exposure only)** — the **same-process** packages-arm reading
  (`PKG_FOREIGN_LIVE`, published by `probe_packages` at `:581-593`; never a second `-Qm` probe)
  joined against the register's rows (`R6_FOREIGN_CLASSES`, `:350-365`; register
  `aur-risk-plane.md:55-89`): `classes=offline-exile:14,aur-local:2`, a `new` arrival adds
  `unknown-provenance=[…]`, and an absent/unreadable/`-Qm`-unreadable baseline prints
  `classes=unavailable(<reason>)` — never HEALTHY off a missing baseline (cases `(R9)` `:1912`,
  `:1917`). The fold can only worsen (`worse`), never lift a BLOCKED probe.
- **`offline.db` + log rows** — `offline.db=present(stamp=<age>d birth=<age>d)` (presence only);
  a bounded `pacman.log` tail `TSUKUROI_LOG_TAIL_N` (default 300) prints the last command class
  (`log=cmd=-S@…`) and the last refresh-class command (`refresh=none-in-window(last 300 lines)`
  — a statement about the window, never about the host; a miss prints `cmd=unknown`, verdict
  unaffected — case `(R9)` `:1927`).
- **Trap row (verb-level, verdict-neutral)** — `pacman -Suu --print-format` prints
  `trap=-Suu:N[first-row]`; today exactly one action (`omarchy/1password-beta
  8.12.42_32.BETA-1`). `DO-NOT` stays note content (round-7 `:95-97`), never a transaction and
  never a verdict; the line also carries the two standing traps (`traps=[-Qu blind to
  shadowed-newer; '%s' is not a size]`, `SKILL.md:389-391,395-397`).
- **Arms as implemented** — `INERT` = both candidate probes empty **and** a present, fresh
  channel reading (`PASS` is vocabulary-only, never emitted — the r2 table's own row 2);
  `REQUIRES-PREP` = candidates > 0 **or** a `behind` row from the join; `UNKNOWN-UPSTREAM` = the
  oldest content stamp older than `TSUKUROI_CHANNEL_MAX_AGE_D` (default **7 d**) or a stamp whose
  age cannot be measured; `BLOCKED` = pacman missing, `db.lck` present, `-Qu`/`-Sup` unreadable,
  or **no repo db under `sync/`** — an empty candidate set over no channel cannot be told apart
  from an up-to-date one (same fail-closed stance as the memory arm; cases `(R9)` `:1887`).
  **Gate-verdict mapping, recorded not silently applied** (header `:227-236`): `BLOCKED →
  BLOCKED`; `UNKNOWN-UPSTREAM` / `REQUIRES-PREP` → `DEGRADED`; `INERT` → `HEALTHY`; the fold can
  only worsen. Realized today: 36 d of channel lag is the named unknown → `DEGRADED`, while the
  candidate set is empty and the `-Suu` trap row prints without raising the verdict.
- **Anti-claim held**: no mutating verb — `-Qu`, `-Sup`/`-Suu --print-format` (plan verbs), `-Q`,
  `-Sl`, `expac -S`, `stat`, bounded log tail; no `-Sy`, no transaction, no download, no db
  write, no AUR RPC, no external site (`PROVINCE.md:16-17`); upstream state stays [unknown]
  read-only. Never re-probes `-Qm` or pins/holds — `pins=none holds=pacman glibc` stays the
  packages plane's row.

### Fail-closed fixtures — the 14 `(R9)` cases (realized labels, executed run)

`healthy: update-safety INERT over a fresh channel` · `degraded: update candidates are
REQUIRES-PREP with names` · `blocked: an empty -Qu at rc=0 is unreadable, never INERT` ·
`blocked: empty over no channel is not an up-to-date reading` · `degraded: a stale content stamp
is UNKNOWN-UPSTREAM, never INERT` · `healthy: the channel-freshness threshold is honoured, not
decorative` · `degraded: the fold names unknown-provenance arrivals and can only worsen` ·
`degraded: the fold never reads off a missing baseline` · `healthy: the joined class split is the
register AUR-local pair` · `healthy: the -Suu trap row is printed and verdict-neutral` ·
`healthy: a log window miss prints cmd=unknown` · `degraded: a repo-side behind row joins the
candidate class` · `healthy: absent expac prints its absence, never a silent pass` ·
`healthy: an unreadable join is printed, never silent` (`tools/tsukuroi-census.sh:1861-1949`).
The plan's **named prerequisite [design] is realized, not dropped**: the channel stamp is the
fixture db file's own mtime — settable with `touch -d` — so the stale-channel case executes
against a real probe rather than being claimed vacuous (`:260-263`). New overrides, realized
names: `TSUKUROI_PACMAN_LOG` (`/var/log/pacman.log`), `TSUKUROI_OFFLINE_DB`
(`$PACMAN_DB/sync/offline.db`), `TSUKUROI_EXPAC`, `TSUKUROI_VERCMP`,
`TSUKUROI_CHANNEL_MAX_AGE_D` (7), `TSUKUROI_LOG_TAIL_N` (300) (`:303-308`). Hermeticity
unchanged: the selftest still writes only under its `mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX`
and asserts fixture byte-unchanged.

### The AUR watch's first drift receipt — an explicit no-drift (S9-3, distil)

`corpus/knowledge/aur-drift-receipt-r9.md` (md5 `e7d6f70b65e4846ad7001b5a66e8ec73`, 248 `wc -l`)
ran the same-day census and read `foreign=16(known=16 new=0 drift=0 gone=0) base=r6(16)` — the
first re-run against the r6 baseline with no drift, confirmed three ways in its window (live
`-Qm` vs the gate's embedded snapshot byte-identical incl. order; vs the register's §1 rows
identical; vs the gate's own classification consistent). It is **not** a claim that the foreign
set is current or safe — §3 of that note separates exactly that. Cite the note, re-run the
receipt.

### Count restatements — moved together (the round-7/8 rule is live, `:925-929`)

The round-3 executor-checklist step 2 ("26 cases", `:519-521`), the round-5 blocks ("35 cases",
`:600-602`, `:686-688`), the round-7 block ("49 cases", `:866-868`) and the round-8 errata
(`:1147-1151`) stand as history. The **current expected line** is
`TSUKUROI_CENSUS_SELFTEST: PASS (63 cases, 63 passed, 0 failed)` at the identity pin above, and
the live contract is the five-plane rollup. `--sample N` default 8 and the `TSUKUROI_*`
fixture-only override rule are unchanged.

### Errata / pending — round 9 (append)

- 2026-10-14 — **the fifth plane is landed and executed, but the revision is uncommitted at this
  append's write time** (`0f72f4cf…`, 2011 `wc -l`; `git status` = ` M`). The round-9 commit
  should pin these bytes; a later re-hash mismatch means the gate moved again — re-hash first,
  then re-run `--selftest` and re-quote the live plane line.
- 2026-10-14 — **write scopes observed, not absorbed**: S9-1 wrote the census revision (its own
  header states the arm's cost and the version-string decision); S9-3 wrote only its drift
  receipt; the scribe lane wrote `plans/round-9-record-draft.md` (a draft, not the record); this
  seat wrote only this append. Still owed at write time: the `LOG.md` entry and the round-9
  `SCORECARD.md` move row (scribe lane); `corpus/README.md` coverage rows (rounds 4-8 collapsed
  debt — unchanged at `98bd0066…`); the `corpus/knowledge/update-safety-v2.md` **append-only
  errata pointer** ("implemented at `<pin>`; the realized contract supersedes §10 where it
  differs") — v2 unchanged at `92803aea…` at write time; the round's own
  `corpus/lessons/round-9.md` (the lane's first; `corpus/lessons/` measured 0 files again).
- 2026-10-14 — **the plane's non-author verification is not this seat's artifact**: this append
  distils the landed revision from its own executed runs; an independent verification note (the
  same shape as VER-S7/VER-S8) is a separate active seat's product and is quoted when it lands,
  never anticipated here.
- Carried (unchanged): root `-Qkk` delta; the 18/19 sweep-summary split; `1password-beta`
  provenance; `walker-restart.hook` (kagi/operator); dkms stale row; `snapper` empty; the
  "20-min cap" item (owner: integrator); round-4/5/6/7 `corpus/README.md` coverage debt; the
  round-2 wave-1 errata merge; round-6's H1-H3 / Q1-Q7; the OOM-plane counter-lifecycle Q2
  (narrowed by S8-2, not closed). round-8's `PLANE oom` watch was **specified, not landed** at
  this block's write time (`:1132-1143`) — round 9's first landing was the update-safety
  plane; the oom watch landed later the same round, recorded in the addendum below.

### Errata addendum — round 9, post-write (append-only)

- 2026-10-14T20:19:37Z — **the census revision moved after this append's first write: lane
  S9-2's oom plane landed on top of S9-1's update-safety plane, making the gate six-plane.**
  Superseding identity pin: `md5sum tools/tsukuroi-census.sh` =
  `e32aac98c6b54f9d7fb8bc4f348cd467` · sha256
  `c396662eeb5f435d841b0c1863903dba807aa9dcbc6a67b2439fdfb13670c650` · 2349 `wc -l` · 123 410 B
  (mtime 2026-10-14 17:17:50 -03; uncommitted, `git status` = ` M`). The block above pinned
  `0f72f4cf…` (five planes); its own caveat applies — this is that mismatch, recorded, not
  smoothed. The update-safety plane's realized semantics above are **unchanged** by the move
  (same fields; the note line read byte-identical at 20:19:37Z); what moved is the plane count
  and the sixth emitter.
- 2026-10-14 — **the realized contract at the new pin, executed** (own runs, zero mutation —
  `git status` byte-identical before/after, no `db.lck`): selftest rc=0 verbatim
  `TSUKUROI_CENSUS_SELFTEST: PASS (74 cases, 74 passed, 0 failed)` (63 + 11 oom-plane cases;
  the 14 `(R9)` update-safety labels stay); live rc=1 — the rollup reads
  `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED
  journal=DEGRADED update-safety=DEGRADED oom=HEALTHY)`, the fifth emitter above is untouched
  and the sixth is `PLANE oom` (`tools/tsukuroi-census.sh:2329`; rollup `:2339`) — the watch
  round 8 specified and never landed (`plans/round-8.plan.md` claims (a)/(b); header `:38-47`).
  **The oom plane's semantics, arms and fixtures are its own lane's product** — quoted here
  only as to the emitter and rollup term; its live line in that run, verbatim:
  `PLANE oom: HEALTHY (window=boots=13 2026-10-03..2026-10-14; C1_kernel=3 killed_process=1;
  C2_events=3 C3_events=3 clusters=2[2026-10-13 23:44,2026-10-14 13:10]; base=r8(2)
  known=2[A, B] new=0 missing=0 out_of_window=0; ledger=vmstat.oom_kill=1; anchors=see
  drivers.mem; traps=presence-not-count,peak-not-datable,launch-not-live;
  rule=both-readings-carried; r8 vocab: kill-event-deep-r8.md §1)`.
- 2026-10-14 — **count restatements, re-moved**: the current expected line is now
  `PASS (74 cases, 74 passed, 0 failed)`; the 63-case line inside this append and the earlier
  round restatements stand as history. A further gate move supersedes this addendum's pin the
  same way — re-hash first.

## Round-10 append — the ten-round calibration ledger and the self-measurement result (TSUKUROI-S10-4)

Dispatch frame: `plans/round-10.plan.md` (md5 `c905a263e7a343d2c84afb21262ec465`, 321 `wc -l` /
322 as read — unterminated final line; committed in `fac745b`). Round 10 is the lane's **first
calibration move**: a ten-round claim-vs-realized ledger (§1), the standing discipline distilled from
it (§2), and the executed self-measurement of the gate at its pin (§3). Landed sibling artifacts
distilled here, each cited as landed state:

- the synthesis ledger `corpus/knowledge/calibration-synthesis.md` (S10-1; md5
  `ed8dec8938bf74647d28d630199aa7be`, sha256 `483d578ebac479999461d7165c6c7d18029c5f61651be8eeaa7e73c680eb6f00`,
  463 `wc -l` / 464 as read, 34 623 B — unterminated final line);
- the round-10 gate revision (S10-2; identity in §4 below) — the mutation sweep's four survivors
  covered by six new `(S10-2)` cases;
- the census closeout receipt `corpus/knowledge/census-closeout-receipt-r10.md` (S10-3; md5
  `c5041b5d03e38c774637f47a24304ca8`, 183 `wc -l` — **live during the window**, 179 → 183; re-hash
  before quoting);
- the scribe's `plans/round-10-record-draft.md` (SCR-S10; md5 `1262712b3c9b70fd8f6858e9c96b6ca9`,
  603 `wc -l`) — cited as a **draft**, never as landed state.

This seat's own receipts: `/tmp/w10-tsukuroi-s104/` (`selftest{,2,3}.out`, `live{,2,3}.out`, `pins.txt`,
`commit-pins.txt`, `status-{before,after}.txt`, `poll.out`; ephemeral). Every pin below is re-hashed at
dispatch from committed bytes (`git show <commit>:<path>`) or the working tree; every count is a
capture — re-run, never quote. Line anchors `:NNN` cite this revision of the file (appends below do not
shift them). The round's planned name for the synthesis (`ten-round-synthesis.md`) was superseded by the
realized `calibration-synthesis.md` — the landed name wins (`calibration-synthesis.md:453-455`).

### §1 The ten-round ledger — claim → realized → the mismeasure it caught

Every row cites landed artifacts only; a plan is never quoted as landed state. `@` marks the commit the
pin was read from. The detailed per-round ledger is `calibration-synthesis.md` §2 (rounds 1–9); this
table is the compact index, and its round-10 row is the only plan row.

| R | plan (md5, `wc -l`) | claim / axis | realized (re-hashed pin) | the mismeasure it caught |
|---|---|---|---|---|
| 1 | **none** — `git log --all -- plans/round-1.plan.md` = 0 commits (measured) | corpus from measured surfaces: verdict vocabulary + decision table + 11-step checklist | `SKILL.md` 232 `9cc6cb6b…` @`55b2186`; notes 255 `df53b0b9…`, 214 `327da5f2…`, 218 `b52f38a6…` @`55b2186` | 4 retractions: sync-db mtime→birth; journal lines→entries; unit files 136→133; rollback net inferred→measured absent; 18/19 `-Qkk` split kept open (`:213-233`) |
| 2 | `3563bd41…` 10 | operability: first executable gate | census-v1 743 `7a3d3b94…` (17 cases); `update-safety-note.md` 478 `5cc3067f…`; `SKILL.md` 444 `f80b4afd…` @`5f90645` | scope `degraded` r1-BLOCKED→census-DEGRADED recorded, not silent (`:334-336`); v1 md5-prefix transcription candidate kept (`:429`) |
| 3 | `160a0272…` 13 | freshness + depth: journal/boot plane + e2e triage | census-v2 976 `41953ee9…` (26 cases); `journal-boot-plane.md` 411 `16d4047e…`; `host-health-report-r3.md` 462 `d701cf6f…`; `executor-test-sufficiency.md` 219 `4b2c1d36…` @`9bcd162` | the no-oral-context test: doc described v1 while v2 had landed → 7 SUFFICIENT / 3 PARTIAL / 3 MISSING, landed as the r3 append (`:448-457,529-545`) |
| 4 | `63c26bb1…` 10 | depth: triage of the lane's own DEGRADED findings | `boot-plane.md` 312 `e722b7a9…`; `degraded-triage-r4.md` 607 `d57ae2d4…` @`165307f` (VER-S1: P1/D2/U6 CONFIRMED) | boot plane corrects r3's "0 unit failures"→4 records (`calibration-synthesis.md:262-291`); 755-not-644 left [unknown] (§6.1); `SCORECARD.md:16` row left malformed (unescaped `\|`) |
| 5 | `0e9e8640…` 11 | adjacency + operability: tameshi's mutation method on the own gate | hardened census 1032 `e9327046…` (26→35 cases); `timer-drift-plane.md` 332 `fc0760c8…` @`da95290` | own sweep 13/23 = 57 % killed; the cross-author sweep's replay closed only 1/4 of its survivors — a hardening gap recorded, not smoothed (`:578-609`; `LOG.md` r5 row) |
| 6 | `81a9be07…` 38 | coverage + freshness: foreign/AUR risk, provenance, OOM-event plane | `aur-risk-plane.md` 341 `1a584300…`; `foreign-provenance-r6.md` 307 `1b8f47a2…`; `oom-event-plane.md` 433 `7e99d712…` (re-cut from `48876876…` mid-append); `aur-risk-plane-ver-s6.md` 133 `b0de352d…` @`dc3436d` | r4's "single message" for event A was one of two (3-message set); the note re-cut mid-append, recorded not smoothed (`:815-828`) |
| 7 | `bb915954…` 160 | coverage + operability: AUR watch + memory arm land | census 1472 `e2c4558a…` (49 cases); `aur-risk-plane-ver-s7.md` 184 `4608743d…`; `update-safety-v2.md` 353 `92803aea…` @`aa136d6` | the plan's fifth plane and the standalone baseline file were **not landed** (carried with the tag); the S7-2 arm had no non-author verification → `AUD-X7` queued |
| 8 | `0bef822d…` 216 | operability: verify the memory arm; kill-event classes | `memory-arm-mutants-s8.md` 181 `a09e5604…`; `memory-arm-ver-s8.md` 251 `861d83ad…` (VER-S8 CONFIRMED, `AUD-X7` closed); `kill-event-deep-r8.md` 340 `6685e1da…`; `update-safety-v3.md` 387 `2ac0c21d…` @`72b038d`; `SKILL.md` 1169 `e2d058d4…` | M01 prediction miss (routing coupling); method delta (copy vs repo file); 9 un-exercised clause sites — the suite is **not** clause-complete; `PLANE oom` specified, not landed |
| 9 | `3a59d2ed…` 270 | coverage + operability: the fifth plane lands | census 2349 `e32aac98…` (74 cases) @`fac745b`; the five-plane 2011 `0f72f4cf…` **never committed** (superseded in ~12 min); `aur-drift-receipt-r9.md` 248 `e7d6f70b…` | the append's own pin was superseded 12 min later by the oom plane — recorded in its addendum, not smoothed (`:1347-1356`); `LOG.md:172` still reads "5-plane" and credits the update-safety arms with `AUD-X7` (closed in r8 by VER-S8) — carried, not repaired here (`calibration-synthesis.md:378-383`) |
| 10 | `c905a263…` 321 (**the only plan row**) | calibration: the ten-round ledger + the standing discipline + the self-measurement | `calibration-synthesis.md` 463 `ed8dec89…` (S10-1); census 2402 `945c76fc…` (S10-2; 74→80 cases, +6 covering four survivors); `census-closeout-receipt-r10.md` 183 `c5041b5d…` (S10-3); this append (S10-4) | this round's catches, in order: the dispatch premise "5-plane" against the realized six (S10-3 §0); the S10-2 revision landing **after** S10-1's note froze, leaving the note's §7 recheck set expecting `e32aac98…` / 74 cases — superseded within the wave (§3); tameshi's three round-5 survivors (B7/B8/B9: default sample cap, CLI exit map, rollup field order) matched the round-10 pre-hardening survivors H1–H3 [label correspondence — inference] and survived nine rounds of own-hardening before this round's cases closed them |

The three round-1 notes are append-only and have grown since: at this append's dispatch,
`package-state-plane.md` 323 `ef93f1b7…`, `systemd-user-plane.md` 265 `af07a829…`,
`driver-firmware-plane.md` 256 `518eda8f…` — current-revision pins, not the as-landed ones above.

### §2 The census's standing discipline (D1–D13)

Each row is a rule the ten rounds' artifacts already prove; **no row makes a new host claim**. The
pattern behind them is `calibration-synthesis.md` §1 (claim → re-measure → append the divergence →
tighten the instrument → re-verify) and its §0.2 conventions; the rows below are the executable form,
each already landed.

- **D1 fail-closed** — an unreadable probe is `BLOCKED`/`unknown=`, never a pass and never a fake
  `INERT` (`:29-31`, `:321-323`, `:1234-1238`; the r2 anti-claim `:407-408`).
- **D2 empty-proof** — an empty result passes only with the scan itself measured: an empty ring is not
  a clean bill (`:347-348`); a journal empty this boot is the same shape (`:496-498`); an empty
  candidate set over no channel cannot be told apart from an up-to-date one (`:1263-1267`).
- **D3 counts move together** — the restated case count equals the executed count; a gate revision
  moves every live restatement (13 sites found by one grep at this dispatch: `:287`, `:470`, `:521`,
  `:602`, `:688`, `:764`, `:867`, `:926-929`, `:1150`, `:1197`, `:1314`, `:1359`, `:1373` — the
  round-10 revision moved the live pair to 80, §4).
- **D4 captures, not quotes** — every count and verdict is re-run; the decision table's own right
  column says so (`:36-37`) and every snapshot block repeats it (`:441-443`). The coredump figure's
  day — 198 → 208 → 211 → 220 → 224 (`SCORECARD.md:14`), 244 → 269 (rounds 4/6, `calibration-synthesis.md:327-331`),
  279 (`:879`), 467 (`aur-drift-receipt-r9.md:57`), 523 (S10-3 §6) — is the standing proof; each
  value a capture.
- **D5 pins state their convention** — full md5, `wc -l` vs Read-count, unterminated final line named
  (`:1001-1006`, `:1347-1352`).
- **D6 no pin from a moving revision** — concurrent seats observe shape only; the r6 note's mid-append
  re-cut (`:815-828`) and the round-9 append's own supersession (`:1347-1356`) are the receipts — and
  this round added one: the S10-2 gate was read mid-write (`2373` `wc -l` at 21:03:02Z) before
  settling at `2402`; no pin is taken from the intermediate.
- **D7 sample rc never decides** — the bounded `-Qkk` sample's rc is not evidence; drift decides
  (`:311-313`).
- **D8 zero mutation** — live mode writes nothing; the suite asserts the fixture byte-unchanged;
  `git status` byte-identical before/after; no `db.lck` (`:265`, `:883`, `:1214`, `:1272-1273`).
- **D9 one probe per fact** — arms fold a same-process reading, never a re-probe; deliberate
  double-counts are distinct-value only (`:499-501`, `:1244-1246`).
- **D10 printed traps** — each plane block names its own traps (line-vs-entry, birth-vs-mtime, `-Qu`
  shadowing, `%s` not a size, pipeline rc) (`:385-401`, `:1233-1238`, `:1256-1260`).
- **D11 plane-set consistency** — the rollup names exactly the planes that emitted; verified
  mechanically at **both** pins this window (6/6 at `e32aac98…` and 6/6 at `945c76fc…`, §3) and
  independently in the S10-3 receipt §4.
- **D12 one-command re-derivation** — one machine-readable identity line. **Not landed**: the gate has
  no `--identity` mode at either pin (`usage()` lists `--selftest`/`--sample N`/`--help` only; S10-3
  §2 reads the same); the standing re-derivation is the classic three commands (`md5sum` →
  `--selftest` → live + `git status`), and this append's §4 is that line written by hand.
- **D13 attested ≠ verified** — an author's suite is author evidence; each new arm's verification is a
  non-author replay (r5 tameshi sweep; r8 VER-S8). The rule's sharpest form this round is
  `calibration-synthesis.md:356-368`: a verifier named in a log line is an **attestation**; only a
  landed note is a verification a later round can re-read.

### §3 The self-measurement result — the gate executes at both pins

Own read-only runs, 2026-10-14, non-root, no `-Sy`/`-Syu`, no transaction, no service action, no
external site. Two revisions were live in this window; receipts for each, unpiped rcs only:

- **Pre-move — the r9b revision, `e32aac98…` (2349 `wc -l`, 123 410 B):** `--selftest` rc=0, wall
  11.771 s, verbatim `TSUKUROI_CENSUS_SELFTEST: PASS (74 cases, 74 passed, 0 failed)`; live rc=1, wall
  2.745 s, 20:52:02Z, six `PLANE` lines, rollup verbatim `TSUKUROI_CENSUS: DEGRADED
  (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED
  oom=HEALTHY)`; emitted-name set == rollup-key set (6/6, this seat's own script — not a gate feature).
- **Post-move — the S10-2 revision, `945c76fc…` (2402 `wc -l`, 126 075 B):** `--selftest` rc=0, wall
  12.121 s, verbatim `TSUKUROI_CENSUS_SELFTEST: PASS (80 cases, 80 passed, 0 failed)`; live rc=1, wall
  2.770 s, 21:05:55Z, same six-plane rollup; plane-set 6/6 SET-MATCH again. The six new labels
  (executed, verbatim): `healthy: the default -Qkk sample cap bounds the sample (S10-2)` ·
  `blocked: the rollup line names every plane field in order (S10-2)` ·
  `blocked: update-safety -Sup unreadable fails closed (S10-2)` ·
  `cli: unknown argument exits 2 with usage (S10-2)` ·
  `cli: --sample 0 refuses before the parse continues (S10-2)` ·
  `cli: --help prints usage and exits 0 (S10-2)` — M = 6 ≥ the plan's ≥4, and none is vacuous: each
  covers a named survivor of the pre-hardening sweep.
- **The sweep behind the six cases, as the revision's own comment states it** (attested, not re-run
  here): target pin `c396662e…` (the r9b sha256), 10 defects, two tool revisions, **6/10 killed**;
  survivors H1 default `-Qkk` sample cap, H2 CLI exit map, H3 rollup field order, H4 update-safety
  `-Sup` fail-closed. The gate comment is the only landed receipt of that sweep in this lane at this
  append's write time [checked: no `*sweep*r10*` / `*mutant*r10*` note exists]; its independent
  replay is a non-author item (D13). The round-5 cross-author ledger leg it echoes is
  `tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md:47` (read-only substrate, cited).
- **Zero mutation at both pins:** `git status --short` showed only the seats' own expected entries
  (` M tools/tsukuroi-census.sh`, the four untracked round-10 files) — no other path moved;
  `/var/lib/pacman/db.lck` absent after every probe. One transient `/tmp/tsukuroi-r3-2-selftest.*` dir
  appeared and was cleaned by its own EXIT trap during the window — attribution **[unknown]** with 32
  lanes in flight; no lane-tagged scratch prefix exists to settle it (the same class the S10-3 receipt
  §5 records).
- **Within-window drift, recorded so no value here is read as standing:** the S10-3 receipt measured
  `C6_avail_kb` −652 732 kB in 77 s while `err`/`coredump` were quiet (§6 there) — captures with
  timestamps, re-derivable, never quotable.
- **What the ledger measures about the arc itself:** **9 commits after the mint** (`55b2186` …
  `fac745b`, one per round 1–9 — round 10 is uncommitted at this append's write time), `SKILL.md` at
  10 revisions (22 → 232 → 444 → 543 → 543 → 706 → 837 → 983 → 1169 → 1374 ln; r3/r4 share the 543
  revision), the census at **6 committed revisions plus the round-10 working-tree move** (743 → 976 →
  1032 → 1472 → 2349 → 2402 `wc -l`; 17 → 26 → 35 → 49 → 74 → 80 cases), and one uncommitted
  intermediate (`0f72f4cf…`).

### §4 Identity pin and count restatements — moved together

- **Identity check** (replaces the round-9 addendum's pin `:1349-1352`): `md5sum
  tools/tsukuroi-census.sh` = `945c76fc6cc548e47b91c23a9637df75` · sha256
  `1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11` · 2402 `wc -l` · 126 075 B ·
  mtime 2026-10-14 18:03:12 -03 · final line `main "$@"`, unterminated (Read counts 2403).
  **Uncommitted at this append's write time** (`git status` = ` M`); the round-10 commit should pin
  these bytes — re-hash after the commit and on any mismatch **stop and re-measure**. The r9b pin
  (`e32aac98…` / sha256 `c396662e…` / 2349 / 123 410 B) stands as history; the banner still reads
  `census-v2` — identity is by hash, not version string.
- **Realized contract**: six planes `packages systemd drivers journal update-safety oom`; exit map
  unchanged (0/1/2, worst plane wins).
- **Count restatement**: the current expected line is
  `TSUKUROI_CENSUS_SELFTEST: PASS (80 cases, 80 passed, 0 failed)` at the pin above — executed by this
  seat (rc=0). The 17/26/35/49/63/74-case lines above and in the earlier blocks stand as history; D3 is
  live — the next gate revision must move every live restatement with it. `--sample N` default 8 and
  the `TSUKUROI_*` fixture-only override rule are unchanged.

### §5 D13 — attested is not verified (warning, cited)

The identity pin and the executed receipts above are **author evidence**. `--identity` does not exist;
whenever it lands it will re-derive the revision's identity — it never verifies the arms, and a
self-identity is not a non-author check (`:1333-1336`; `calibration-synthesis.md:356-368`). The same
holds for this round's hardening: the sweep figures in §3 are the revision comment's attestation, and
the round-10 closeout receipt says the same of itself (its §8). Standing verification debt: (a) the two
planes round 9 added, (b) the rows of this ledger, and (c) the six `(S10-2)` cases' covering claims —
each a separate, non-author product, quoted when it lands, never anticipated here.

### Errata / pending — round 10 (append)

- 2026-10-14 — **the wave's artifacts landed while this append was being written; the order matters and
  is recorded, not smoothed.** S10-1's `calibration-synthesis.md` froze with the r9b pins (its §7
  recheck set expects `e32aac98…` and `PASS (74 cases, 74 passed, 0 failed)`, `:407-409`; its §8 pins
  re-checked at 20:58:34Z); S10-2's revision landed **after** it (gate mtime 18:03:12 -03 = 21:03Z),
  so the note's recheck expectation is superseded within its own wave. Append-only: the note's owner
  appends the pointer; nothing here edits that note. One intermediate read of the S10-2 file
  (`b7269e59…`, 2373 `wc -l`) was **mid-write**; per D6 no pin was taken from it.
- 2026-10-14 — **the synthesis note is rounds 1–9 by its own title**; this append extends the ledger to
  round 10 and is the SKILL-side carrier for the standing rows (§2) until the note's own D-table
  lands. The record draft's §4(c) contract for this append is met: standing-discipline block, count
  restatements moved together, D13 stated.
- 2026-10-14 — **`corpus/lessons/round-10.md` is still 0 files** at this append's write time
  (`corpus/lessons/` empty since round 1; `calibration-synthesis.md:390-393` names the debt) — the
  discernment loop's home is owed by the note/hygiene seat, not this one; no retro-fabrication.
- 2026-10-14 — **the S10-3 closeout receipt is a live artifact, not a frozen one**: it moved during
  this append's window (179 → 183 `wc -l`; md5 `c5041b5d03e38c774637f47a24304ca8` at this append's
  last read, 21:05Z). Re-hash it before quoting; the same rule applies to this file.
- Carried (unchanged): root `-Qkk` delta; the 18/19 sweep-summary split; `1password-beta` provenance;
  `walker-restart.hook` (kagi/operator); dkms stale row; `snapper` empty; `offline.db` coverage; the
  "20-min cap" item (integrator); `corpus/README.md` coverage debt (rounds 3–10, unchanged
  `98bd0066…` 20 `wc -l`; its stale row `:13` also carried); the `SCORECARD.md:16` malformed row and
  the row-16/round-9-row repairs (scribe + note/hygiene seat); the round-2 note errata pointer
  (`update-safety-note.md` unchanged `5cc3067f…` 478 ln); E4–E8 unapplied errata; H1–H3; the
  OOM-plane counter-lifecycle Q2; the r2 wave-1 errata merge; the LOG entry, the round-10 `SCORECARD`
  row and the closing no-oral-context re-test (scribe/executor seats).

## Round-11 append — final pointers: the handoff, the identity pin, and the closeout (TSUKUROI-S11-4)

Dispatch frame: `plans/round-11.plan.md` (md5 `2f09006e6c0d6b728c9a46067a487ea0`, sha256 `e3afb4108c748ebb55c98a0cb3f083b7420163707fc53ef3e5e4a4787c0d8e3f`, 348 `wc -l` / 349 as read — unterminated final line; committed in `af8adf1`, the round-10 commit). This is the arc's terminal append — the closeout round presumes no round 12; every item still open at its close is named with its owner, never parked. It carries, per the record contract (`plans/round-11.plan.md:166-169`): the runbook pointer (§1), the final identity pin (§2), the count restatements re-grepped and moved together (§3), the terminal-contract pointers (§4), the D13 closing warning (§5), and the closing errata. This seat's receipts: `/tmp/w11-s11-4-tsukuroi/` (`selftest.out`, `live.out`, `pins.txt`, `status-before.txt`, `status-after.txt`, `plane-names.txt`, `rollup-keys.txt`, `watch.log`; ephemeral). Write scope: **this file only**. Host probes read-only (`PROVINCE.md:16-17`): no `-Sy`/`-Syu`, no transaction, no download, no service action, no root, no external site; secrets untouched; `git status` byte-identical before/after every probe; `/var/lib/pacman/db.lck` absent after every probe. No new host claim; no pin from a moving revision; no self-promotion; nothing below quoted from this seat's draft.

Poll frame: this seat polled the tree for the wave's terminal artifacts at 40 s cadence from 21:33:10Z (57 `watch.log` samples logged by 22:10:53Z; watcher budget ≈43 min) — the lane's assignment named no cap, so the cap is this seat's own and is recorded here. The runbook did **not** land inside the window (§1); the wave was still in flight at this write — corroborated by the sibling records' own freezes (`corpus/knowledge/closeout-r11.md:27-31`; `plans/completion-evidence.md` §3/§4). This block itself lands uncommitted like the rest of the wave; the scribe's landing commit should pin it — re-hash after the commit and on any mismatch stop and re-measure (the round-10 §4 contract pattern).

Line anchors `:NNN` cite the pre-append revision of this file (md5 `19d989b32fb0b4040254a2503d503854`, sha256 `9b118f0a4fa04ed683a43f10412f3879c810c118bb5fc74a2e2ad45ff247c70c`, 1569 `wc -l` / 1570 as read — unterminated final line; committed in `af8adf1`); this block begins at `:1572` of that view, and later appends do not shift earlier anchors.

### §1 The handoff pointer — the reader's entry point

- **The runbook had not landed at this write** — the planned landing is `HANDOFF.md` at the repo root (plan `:100-128`; the realized name/placement is adjudicated at landing), **owner: the runbook seat**. Measured: `ls HANDOFF.md` rc=2; no root-level file appeared in any of the watcher's status samples; `git status --short` across the window carried only the three sibling artifacts named in §4. The absence is corroborated inside the sibling records by their own freezes — `closeout-r11.md:28-31` ("landing around and after this window … not cited as landed here") and `plans/completion-evidence.md` §3 L1 ("absent", 30 s poll 21:33:57Z–22:01:17Z). **A reader arriving after the wave closes must re-check the tree for it before relying on this paragraph**: the pointer that exists at this write is the plan, `plans/round-11.plan.md:100-128`, and the handoff's own verification contract — the executor seat's no-oral-context re-test (plan §(c), `:170-181`) — is unrun at this write.
- **The reader's landed-adjacent pointers at this write** (all three in-flight, uncommitted — §4): the arc narrative `corpus/knowledge/closeout-r11.md` (S11-1, carrying the T11-3 regression append); the round's completion ledger `plans/completion-evidence.md` (PACK-S); the independent audit `reports/r11-aud-s11.md` (AUD-S11). Each states its own window; none is completion evidence until committed (PACK-S §3's own rule).

### §2 Final identity pin — the census at `945c76fc…` (round 10's pin, now committed; re-derived, no move)

- **Identity** (re-derives the round-10 §4 pin, `:1518-1525`): `md5sum tools/tsukuroi-census.sh` = `945c76fc6cc548e47b91c23a9637df75` · sha256 `1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11` · 2402 `wc -l` / 2403 as read (final line `main "$@"`, unterminated) · 126 075 B · mtime 2026-10-14 18:03:12 -03. **Worktree == the committed blob**: `git show af8adf1:tools/tsukuroi-census.sh | md5sum` = `945c76fc…` — the round-10 append's "uncommitted, re-hash after the commit" contract is discharged by this re-hash; the gate did not move in round 11 (the watcher's md5 prefix held at every sample; AUD-S11 §1 C1.1 and its two live runs agree).
- **Executed at this pin** (own runs, receipts `selftest.out` / `live.out`): `--selftest` rc=0, wall 13.422 s, verbatim `TSUKUROI_CENSUS_SELFTEST: PASS (80 cases, 80 passed, 0 failed)`; live rc=1, wall 3.400 s at 21:31:57Z, six `PLANE` lines, rollup verbatim `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=HEALTHY)`; emitters `:2377-2382`, rollup `:2392`, exit map `:450`; emitted-name set == rollup-key set (6/6 SET-MATCH, this seat's own script — not a gate feature).
- **Zero mutation**: `git status --short` = 0 entries before and after the runs (21:31–21:32Z; the sibling artifacts landed from 21:35Z, after the check); `/var/lib/pacman/db.lck` absent after both classes of run. Every live value above is one 21:31:57Z capture — re-run, never quote (D4).
- **D12 still unlanded**: `usage()` (`:439-452`) lists `--selftest`, `--sample N`, `--help`; `grep -n identity` hits comment lines only (`:35`, `:46`). The standing re-derivation remains the classic three commands (`md5sum` → `--selftest` → live + `git status`); round 10's D12 row (`:1464-1467`) is carried, not closed.

### §3 Count restatements — re-grepped, moved together (no move required: the gate did not change)

- Executed count: **80**. The claim-bearing restatements re-checked by grep at this pin, as a supersession chain: `PASS (49…)` (`:926-928`), `PASS (49…)` (`:1147-1150`), `PASS (63…)` (`:1311-1315`), `PASS (74…)` (`:1372-1375`), and the round-10 pair that states the current count — `:1484` (the post-move execution line) and `:1529` (the **current expected line**, `PASS (80 cases, 80 passed, 0 failed)`). Each earlier block is marked history by its successors' own words (`:831`, `:928-929`, `:1149-1151`, `:1311-1313`, `:1372-1375`); the live pair reads 80 == the executed run. Because the census revision is byte-identical to round 10's, no restatement needed to move; the D3 nine-site list (`:1438-1441`) re-grepped — its line references still resolve to count statements.
- The realized contract: six planes `packages systemd drivers journal update-safety oom`; exit map unchanged (0/1/2, worst plane wins); `--sample N` default 8 and the `TSUKUROI_*` fixture-only override unchanged.

### §4 Terminal contracts — pointers (state at this append's write, re-measured, never assumed)

| artifact | state at this write | pointer |
|---|---|---|
| runbook (`HANDOFF.md` proposed) | **absent** — `ls` rc=2; no root file in any watcher sample; owner: the runbook seat | plan `:100-128` |
| `corpus/knowledge/closeout-r11.md` (S11-1 + T11-3 append) | in-flight, uncommitted — md5 `d59da63fb6c812aeea81553dfc8dc7a1` · 403 `wc -l` · 28 614 B · mtime 18:38:37 -03 | its §5 recheck; append-only surface |
| `plans/completion-evidence.md` (PACK-S) | in-flight, uncommitted — md5 `472e7f196b2c5187e96813ab2a5653b0` · 160 `wc -l` · 9 893 B · mtime 19:02:16 -03 | its §6 recipe |
| `reports/r11-aud-s11.md` (AUD-S11) | in-flight, uncommitted — md5 `7777142aaebb88b1696b05398be999ee` · 173 `wc -l` · 14 263 B · mtime 18:39:25 -03 | its §1 tables |
| `PROVINCE.md` | unchanged since round 0 — md5 `f1722b163a5c433b003de362ab93ee11` · 19 `wc -l`; no Core/Frontier/Adjacent sections | plan `:130-138` |
| `corpus/README.md` | unchanged since round 3 — md5 `98bd00668e84f18cf6781718c4d09ea0` · 20 `wc -l`; rows stop at round 3; `grep -c '## Frontier'` = 0 | plan `:153-155` |
| `corpus/lessons/` | **0 files** — rounds 1–10 never written; the round-11 lesson is a separate owed artifact | register debt |
| `SCORECARD.md` | unchanged — md5 `52218ee5fcb240fa0bd9f64602ff169d` · 22 `wc -l`; rows 16/21/22 still malformed (unescaped parens); no `planned`/`retired`/axis-score rows | plan `:156-165` |
| `SHONEN.md` | unchanged since round 3 — md5 `9cf1d450685ae0ed0d15dee1b54e8fd5` · 51 `wc -l`; mechanical diff unrun; `[x]` owed to the non-author review | `PROTOCOL.md:419-431` |
| `LOG.md` | unchanged — md5 `0c9b2f02375cca07998a6ff46a8cec6f` · 173 `wc -l`; last entry = round 10; `:172`/`:173` still read "5-plane"; closing entry absent | scribe seat |

Every row is a state reading with its hash, not a promise; where a row is still open, the owning seat is named and the plan anchor is the pointer. A reader after this wave closes re-hashes before quoting (D5); a landing that beats this append supersedes the row's state, and a landing after it is recorded by the wave's own LOG entry or a later append — never retro-inserted here.

### §5 D13 — attested is not verified (the closing warning)

Everything in this append is **author evidence**: this seat ran the gate and re-hashed the files. The arc's close has its own, separate non-author products — the executor seat's no-oral-context re-test against the runbook (plan §(c); unrun at this write), VER-S11's non-author mutant rebuilds (its scratch poll was live in this window), and the promotion review behind `SHONEN.md`'s `[x]`. None is claimed here; each lands or does not as its own artifact. The standing verification debt of round 10 §5 (`:1540-1542`) applies unchanged: (a) the two planes round 9 added, (b) the ten-round ledger rows, (c) the six `(S10-2)` covering claims.

### Errata / pending — round 11 (append)

- 2026-10-14 — **the closeout state at this append's write, recorded, not smoothed**: the runbook, PROVINCE Core/Frontier/Adjacent, the README back-rows + `## Frontier`, `corpus/lessons/round-11.md`, the SHONEN mechanical diff, the SCORECARD repairs, the LOG closing entry and the executor re-test were all still open (see §4; corroborated by `plans/completion-evidence.md` §3/§4, whose 22:01:17Z freeze found L1–L10 open). The three sibling artifacts in §4 (and §1) are in-flight and uncommitted — not completion evidence until committed; the realized names govern. Anything landing after this write is named by the wave's own LOG entry (scribe seat), never retro-inserted here.
- 2026-10-14 — **the "5-plane" wording repairs remain open**: `LOG.md:172` and `:173` still read "5-plane"; the repair call sits with the record/scribe seats, append-only (`reports/r10-aud-s10.md:190-191`; `reports/r11-aud-s11.md:119` O3; `closeout-r11.md:252-254`). A new LOG entry may correct the claim; this append edits nothing.
- Carried, unchanged (the round-10 errata's list, `:1563-1570`, each re-checked as still open at this write): root `-Qkk` delta; the 18/19 sweep-summary split; `1password-beta` provenance; `walker-restart.hook` (kagi/operator); dkms stale row; `snapper` empty (no rollback net); `offline.db` coverage; the "20-min cap" (integrator); `corpus/README.md` coverage debt (its row `:13` also carries the r4-refuted wording); the `SCORECARD.md` row-16/row-21 repairs (row 22 too — `closeout-r11.md:249-254`); the round-2 note errata pointer; E4–E8 unapplied errata; H1–H3; the OOM-counter lifecycle Q2; the r2 wave-1 errata merge. Plus: the never-written lessons register (rounds 1–10) and the deferred classes — coredump storm (523 at round 10's capture; 752–781 in the round-11 window's captures — every value a capture; owner: godot/node/LOVE app lanes + the journal workstream), V8 heap-OOM — each with the owner `closeout-r11.md` §3 names.
- [unknown] this append cannot settle (recorded here, not deferred to a round 12 that will not exist): the runbook's realized name/placement (plan proposes `HANDOFF.md`; adjudicated at landing — probe: re-read the tree; `plans/completion-evidence.md` §6 has the recipe); whether the wave's remaining artifacts land after this write; the executor re-test's outcome; VER-S11's verdicts; the promotion review's `[x]`; and the fleet-level question of whether round 11 is the last round for every lane (the plan's own frame note, `:29-38`, leaves it to the dispatcher).

### Errata addendum — round 11, post-write (append-only)

Pre-addendum revision of this file: md5 `d1cbaca225de405290b78f3d75fa1cc2` · 1622 `wc -l` / 1623 as read — unterminated final line (the convention); the anchors above cite the earlier pre-append revision (`:1569`-line view), not this one. Every pin below re-hashed at this addendum's write (22:14:4xZ); both moved files are uncommitted and may move again — re-hash before quoting (D5/D6).

- 2026-10-14 — **`LOG.md` moved after §Errata's write: the scribe's round-11 entry landed** (SCR-S11; one appended line, `:174`, unterminated final line). New pin: md5 `6f92727edeb86b60d2395578991c1b77` · 173 `wc -l` / 174 as read · 20 425 B · mtime 19:12:30 -03. It records the seats (S11-1 / S11-4 / VER-S11 / AUD-S11 / PACK-S / T11-3 / SCR-S11), the work set (a)–(d) with pins, the scribe's own re-verification (21:38–22:11Z), the SCORECARD refresh, the debt list, and the SHONEN state (all four `[~]` asserted; `[x]` owed). Two clauses of this file's §Errata are answered by it: the "5-plane wording remains open" bullet — **answered as append-only precision**: the new entry carries the committed-arc correction (3→4→5-uncommitted≈12 min→6) and the r8 VER-S8 credit fix while `:172`/`:173` keep their original text, exactly the append-only pattern; and its "Debt at this write" clause lists L7 ("SKILL terminal append") among the owed items — **superseded by timing, recorded not smoothed**: this block was in the tree at 22:12:01Z (the watcher's 22:11:50Z sample has no ` M SKILL.md`; the 22:12:30Z sample has it), so the record's read predates this file's write by ~30 s and L7 is satisfied by this file, append-only. Its L1 reading — "`HANDOFF.md` never appeared; the realized reader artifact is `closeout-r11.md`" — is the same measurement as §1 and stands as the record's adjudication of the realized reader artifact.
- 2026-10-14 — **`SCORECARD.md` moved after §Errata's write: the refresh landed** — rows 16/21/22 repaired by closing the paren only (every original word preserved in place; the unescaped-`|` reading adjudicated and rejected by the record), the round-11 move row, the six-axis score table with counting commands, and `Planned / retired` (none — no axis saturated). New pin: md5 `c9f5489843315a8bfac8a8ce4f7edea4` · 56 `wc -l` · 13 335 B · mtime 19:13:03 -03. §4's SCORECARD row ("unchanged … rows 16/21/22 still malformed") is superseded by this line.
- 2026-10-14 — **VER-S11's verdict stays scratch-only** (`/tmp/w11-ver-s11/VERDICT.md`; that lane's dispatch was do-not-edit — the record's (d) carries it): the r10 ladder re-derived from blobs (r9b `e32aac98…` 74/74 rc 0; r10 `945c76fc…` 80/80 rc 0) and the H4/S2 survivor cells re-run byte-equal (H4 SURVIVED at r9b; H4/S2 KILLED at r10). A non-author product exists; per D13 only a landed note is a verification a later round can re-read — the §5 debt stands, sharpened rather than closed.
- [unknown → narrowed] "VER-S11's verdicts" is answered as above; "whether the wave's remaining artifacts land after this write" stays open at this addendum's write (L1–L5, L9, L10 per the record's own debt line; the watcher runs to the wave's landing commit); "the runbook's realized name/placement" now has the record's reading named in the first bullet.

## Fleet round-1 append (2026-10-19) — doctrine erratum, update-gate rows, where to learn

**Erratum to `:391-393`** ("the operator's next `-Sy` is the resolving event"): superseded. Bare
`pacman -Sy` is unsupported (ArchWiki System maintenance § Avoid certain pacman commands — S010,
https://wiki.archlinux.org/title/System_maintenance?oldid=885170). The read-only upstream check is
`checkupdates` (pacman-contrib; temp DB, never the real sync DB — S009; `pacman-contrib` not
installed on this host 2026-10-19); the operator's update is a full `-Syu` after the news gate.
[obs] This host ran bare `-Sy` twice (`/var/log/pacman.log:1405`, `:2287`); after `:2287`
(2026-10-18) 7 `pacman -S`/`-Rns` transactions ran with 0 `upgraded` / 64 `installed` lines and
no `-Su` — `awk 'NR>=2287 && /\[ALPM\] upgraded/' /var/log/pacman.log | wc -l` → 0 2026-10-19.
Packages installed against a refreshed DB over un-upgraded deps is the partial-upgrade state
S010 forbids [inf: no breakage observed]. Errata in the notes: `## Erratum (2026-10-19` blocks.

Update-safety checklist rows (manual, read-only; each row's entry carries commands + falsifier):

| Check before `-Syu` | DEGRADED when | Entry |
|---|---|---|
| News gate | an applicable, unhandled item since the last `-Syu` | `corpus/knowledge/arch-news-gate-2026.md` |
| Config drift | ≥1 `.pacnew`/`.pacsave` by filesystem census (log is history, not state) | `corpus/knowledge/pacnew-plane.md` |
| Initramfs flavor vs candidate | busybox hooks hardcode `/new_root` and `mkinitcpio` ≥42 is the candidate | `corpus/knowledge/initramfs-v42-sysroot-recovery.md` |
| Rollback net | snapper/limine `errno:13` recurring, no snapper config | `corpus/knowledge/snapper-eacces-mechanism.md` |

Where to learn more: `corpus/SOURCES.md` (tiered registry, study paths, search log, leads).

If `checkupdates` is absent (`command -v checkupdates` has no path), do not install it or substitute bare `pacman -Sy`: report the upstream package delta as unknown under the current read-only probe set. Any full `pacman -Syu` remains an operator action after the news gate.

The 2026-10-18 transaction counts above are command-anchored as follows (run on `/var/log/pacman.log`):

```sh
awk 'NR>=2287 && /\[PACMAN\] Running .pacman -S / {n++} NR>=2287 && /\[PACMAN\] Running .pacman -Rns / {n++} END{print n+0}' /var/log/pacman.log
awk 'NR>=2287 && /\[ALPM\] installed / {n++} END{print n+0}' /var/log/pacman.log
awk 'NR>=2287 && /\[ALPM\] upgraded/ {n++} END{print n+0}' /var/log/pacman.log
awk 'NR>=2287 && /\[PACMAN\] Running .pacman .* -Su/ {n++} END{print n+0}' /var/log/pacman.log
```

Observed outputs in order: `7`, `64`, `0`, `0` (2026-10-19). These are separate counts; the D1 literal-text match count is not an advice count.

## Round 12 — root metadata and create-failure discrimination

The packages plane now observes `/` metadata independently of pacman's package
ownership list. `TSUKUROI_ROOT_DIR` overrides that directory for isolated fixtures;
the live default is `/`. Read `root_mode`, `root_uid` and `root_gid` on the
packages line even if the package probe itself cannot run.

| Finding | Interpretation | Next read-only discriminator |
|---|---|---|
| Missing owner write or search bit | Report-only metadata observation; no automatic degradation and no universal required mode | `getfacl -p /`; inspect tmpfiles policy/overrides and the affected unit's properties |
| Metadata unavailable or not a directory | BLOCKED: the root metadata observation cannot be evaluated | `stat -c '%a %u %g %F' /` and its exit |
| Owner write/search present | This arm has no finding; it does not certify ownership policy or process writability | Review the full census and relevant unit/mount evidence |

Never equate mode `0555` with a read-only mount. Never infer live effective
capabilities from `User=root` or a bounding-set property. For create-class
failures, inspect target existence, the relevant mount/namespace, parent
DAC/ACL and runtime credentials separately. `ProtectSystem=full` does not make
`/` read-only; property text from an inactive unit is not a runtime trace.
The sourced procedure and explicit unknown outcome are in
`corpus/knowledge/root-dac-decision-r12.md` (S027/S028/S034/S035/S038–S040).
Ordinary `mkdir` controls do not prove historical Btrfs ioctl causality.
The root-mode arm does not remove the initramfs-v42 `/sysroot` upgrade gate.

The opened `/usr/lib/tmpfiles.d/root.conf` contains `z / 555 - - -`.
Thus pacman not owning `/` does not imply no packaged policy exists. Do not
recommend changing `/` to `0755` from the inode mode alone. This round's
policy discovery supersedes the earlier "origin unknown/no baseline" premise;
it does not prove which historical operation set the inode mode.

### Gate registry

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` | 0 clean/HEALTHY; 1 failed/DEGRADED; 2 could-not-evaluate/BLOCKED or usage | `bash tools/tsukuroi-census.sh --selftest` (0 pass, 1 fail) | `tools/tsukuroi-census.sh`: embedded foreign/OOM/class baselines and selftest expected verdict/finding patterns | Live: none; selftest: disposable `/tmp/tsukuroi-r3-2-selftest.*` only | tsukuroi |

This host gate does not grade mutable fleet artifacts. Its isolated expected
finding patterns establish capability, while the dated live root-metadata
capture establishes this round's measurement; neither is outside admission.
Round evidence: `.ufo/waves/round-12/resumed/`; lesson:
`corpus/lessons/round-12.md`.

## Round 13 — active unit-path correction (R13-DAC-EXCLUSIVITY)

The round-12 matrix pointer above is a historical entry rejected at outside
closure. For current unit-read-only reasoning read
`corpus/knowledge/root-dac-correction-r13.md` and its canonical JSON first
(S028/S041). `ProtectSystem=no` with empty `ReadOnlyPaths=` excludes those
settings only. It does not exclude `BindReadOnlyPaths=` or a
`TemporaryFileSystem=` mounted `ro`; `RootDirectory=`/`RootImage=` alter
the path view but are not inherently read-only. Among ProtectSystem values,
`full` omits `/` and `strict` has documented hierarchy coverage and exceptions.
Host `findmnt` is not evidence of a unit-private namespace's mount state.
Keep the issuer, operation, path and historical capability state unknown
where they were not measured. Caller-owned mkdir controls are not executed
root-owned fixtures. No repair or upgrade clearance follows this correction.

The new checker verifies the bounded correction contract, not arbitrary
prose truth, host health, historical causality or independent admission:

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| root-dac-correction | gate | `python tools/check-root-dac-correction.py` or `--revision <commit>` | 0 clean; 1 failed; 2 could-not-evaluate | `python tools/check-root-dac-correction.py --selftest` | Committed finding IDs and correction predicates inside `tools/check-root-dac-correction.py` | None; git object reads or lane files only; selftest in memory | tsukuroi |

Measured runs, source review and limits are in `corpus/lessons/round-13.md`
and `.ufo/waves/round-13/correction/`; outside verification remains required.

**Read-only correction for this procedure:** the historical allowed-list
entry `snapper list-configs` is not a non-activating probe: the local
`/usr/share/dbus-1/system-services/org.opensuse.Snapper.service:3-6`
declares root `snapperd` D-Bus activation. Do not invoke it in the new
procedure; inspect configuration-directory names without reading secret
contents instead. This declaration does not prove which historical caller
started a daemon. Use explicit `systemctl show -p` property lists, never
raw unit text, argv, environment or credential properties. Starting a
fresh invocation is an operator-owned state change, not a read-only check.
Existing `/sysroot` update-safety conditions still bind. Evidence:
`.ufo/waves/round-13/correction/SecurityBoundary.md` F1/F2/F5 and the local
activation declaration reopened by L1 on 2026-10-20.

### Erratum (2026-10-20, round 14) — active source-scope supersession

`corpus/knowledge/source-scope-correction-r14.md` / `.json` supersede two
defective loci in the active round-13 correction, not its valid teaching:
**R14-VALUE-DOMAIN** (S044) replaces the r13 MD:97 “value set is not
exhaustive” cell — `ProtectSystem=` is documented as a boolean argument or the
special values `full` or `strict`, so the option domain is closed at those
values while non-exhaustiveness applies to unit-side mechanisms; and
**R14-COMMENT-ATTRIBUTION** (S045) replaces the #8047 “self-described
model-generated automated triage” wording in `corpus/lessons/round-13.md` and
r13 MD QUALITY item 18 — verified account fields are separate from the body's
unverified VM assertion, second opinion and maintainer deferral (the deferral
concerns #6634; #8047 waits on the reporter). S043's #6629 disclaimer stays
valid. Metadata erratum: r13 JSON `sources[0].status: reserved` /
`registry_owner: SourceRegistry` are stale draft values (S041 is mined in
`corpus/SOURCES.md`), and its `gate_contract` heading/scan object is an
authoring residual the five-heading executable check does not consume. The
round-13 section above remains usable with these two corrections applied.

### Round-14 correction-conformance gate registry

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| source-scope-correction | gate | `python tools/check-source-scope-correction.py` or `--revision <commit>` | 0 clean; 1 failed (including schema conformance); 2 could-not-evaluate (CLI/read/parse/internal errors) | `python tools/check-source-scope-correction.py --selftest` | `tools/check-source-scope-correction.py` committed correction predicates, literal fixtures and expected finding IDs | None; lane files or git objects read-only; selftest in memory without network | tsukuroi |

This command checks only its committed, explicitly bounded correction
predicates. It does not prove source truth, all prose semantics, host health,
historical causality or independent admission. The r13 JSON `gate_contract`
is not a second executable specification. Source comparison and measured
revision evidence: `corpus/lessons/round-14.md` and
`.ufo/waves/round-14/repair/`.

## Round 15 — portable locators, positive option domain, and the dated update recheck

Two named clarifications supersede only the supplemental documentation defects
routed by the round-14 outside verifier
(`corpus/lessons/round-14-verifier-spotcheck.md` § Adjudicated concerns and
routing, items 1–2): **R15-LOCATOR** withdraws the bare
`rendered lines 1266-1267` locator in the r14 pair (MD source-object,
JSON `corrections[0].location`, JSON `sources[0].anchor`) in favour of the
stable SANDBOXING > ProtectSystem= heading plus the observed footer version,
and **R15-POSITIVE-DOMAIN** replaces the unswept “documents no further values”
sentence with the quoted positive definition. Read
`corpus/knowledge/source-locator-clarification-r15.md` / `.json` (schema
`tsukuroi-locator-clarification-v1`) first. The r14 quote, technical teaching
and #8047 correction remain exact; append-only notices live in
`corpus/knowledge/source-scope-correction-r14.md` § R15 supersession and the
`r15_supersession` JSON key. QUALITY criteria 21–22 govern portable locators
and positive-versus-absence claims.

Current-use update state on 2026-10-20 is
`corpus/knowledge/partial-upgrade-recheck-r15.md` / `.json` (schema
`tsukuroi-partial-upgrade-recheck-v1`), bound to
`.ufo/waves/round-15/build/host-snapshot.json` captured 2026-10-20T07:44:39Z
(raw-byte SHA256
`b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`). It
supersedes the 2026-10-14 `INERT` / “Do nothing now” current-use reading in
`corpus/knowledge/update-safety-note.md`, `update-safety-v2.md`,
`update-safety-v3.md` and `host-health-report-r3.md`; those bytes stay
historical. The dated decision is `BLOCKED_FOR_AGENT_PACKAGE_ACTION`.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| locator-clarification | gate | `python tools/check-locator-clarification.py` or `--revision <REV>` (REV = `HEAD` or 4–64 hex) | 0 clean/PASS; 1 failed (bounded findings, `correction_count` < 2); 2 could-not-evaluate (`E-CLI`, `E-REVISION-INVALID`, read/git/parse/internal) | `python tools/check-locator-clarification.py --selftest` (21 fixture cases + 2 CLI cases = 23; exit 0 pass, 1 fail) | `tools/check-locator-clarification.py` committed constants: MD15/JSON15/MD14/JSON14 paths, `tsukuroi-locator-clarification-v1`, `R15-LOCATOR`/`R15-POSITIVE-DOMAIN`, S046 URL, 11-word quote, three required headings, seven correction fields, r14 notice tokens, pre-append r14 canonical digest pins (`MD14_SHA` = sha256 of the rstripped r14 MD prefix; `JSON14_SHA` = sha256 of sorted/compact normalized r14 JSON minus `r15_supersession`) and expected finding IDs | None; reads lane files or git objects only (`GIT_OPTIONAL_LOCKS=0`); selftest in memory | tsukuroi |
| measure-update-recheck | probe | `python tools/measure-update-recheck.py` or `--revision <REV>` (REV = `HEAD` or 4–64 hex) | No verdict map: 0 = `ABSENT` (`record_count` 0, pair absent) or `COUNTED` (`record_count` 1, internally consistent record; its internal `status: COUNTED` string is not a gate clean or health verdict); 2 = could-not-evaluate (malformed JSON, schema/digest/observation mismatch, missing record or snapshot, `E-CLI`); no 1 | None (probe; no self-test obligation) | Committed C2 schema `tsukuroi-partial-upgrade-recheck-v1`, required keys (`schema`, `source_ids` S047/S048/S049, `observed_at`, `evidence_path` `.ufo/waves/round-15/build/host-snapshot.json`, `snapshot_sha256`, `observations`, `decision`, `limits`), five snapshot probe keys with exit 0/empty stderr; digest held in the C2 JSON (`b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`), checked against raw snapshot bytes (no digest constant in the tool) | None; pure-stdlib reads, no writes, no host command execution | tsukuroi |

The locator gate checks only its committed documentation predicates: two
correction records, the S046 URL and 11-word quote, the stable heading, the
absence of an unqualified renderer line in the new location, and both r14
notices. It does **not** establish source truth, parser exhaustiveness, host
state, historical causality or independent admission. In tree mode it reports
`revision: worktree`; a comparable verdict names a commit via `--revision`.
The update measure is a read-only counting probe, not a gate: its exit 0 is a
completed observation, never a health verdict or package authorization.

Boundaries: this round installs no package, runs no service action, no
privileged probe and no repair. The pending partial-upgrade assessment is
operator-only; any full `-Syu` remains an operator action behind the news gate.
Installed `mkinitcpio 41.1-1` with 42.2-1 pending and two `/new_root`-only
hooks make mkinitcpio-42 compatibility an untested risk, not a clearance. No
host repair, ABI certification or running-process version is claimed.

## Round 16 — citation-only section/table errata

Read `corpus/knowledge/section-citation-errata-r16.md` and `.json` for
R16-BOARD-SECTION and R16-RANK-SECTION. Two R15 notice locators are
superseded: host-health's verdict-board row5 is under `## 0. Verdict board`,
not §1; update-safety-v3's rank1 “Do nothing now” row is under its exact
`## 5. Risk-ordered operations table (recommendation only — nothing here was run)`,
not §7. Explicit v2 §7 references remain correct and unchanged.

These notices correct citations only. They preserve every original byte,
R15-UPDATE-STATE's current-use supersession and operator ownership.
The quoted “now”/“Do nothing now” statements describe the 2026-10-14 capture,
not this host now. The retained r15 evidence remains dated; no fresh host,
ABI, running-version, input/UI, boot or package consistency observation is
made by correcting a citation. No agent install, upgrade, downgrade or
service action is authorized. Host recovery remains operator-owned and
all pacman transactions remain paused under the current operator ruling.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| section-citations | gate | `python tools/check-section-citations.py --revision <commit>` | 0 clean: two citation locations resolve; 1 failed: bounded conformance findings; 2 could-not-evaluate: CLI/git/read/parse errors; no health or upgrade verdict | `python tools/check-section-citations.py --selftest` | Fixed R16 IDs, paths, headings, row keys, exact quotes, notice/source bindings, baseline history and independent fixture expectations in `tools/check-section-citations.py`; independent attack vectors `.ufo/waves/round-16/build/frozen-cases.json` | Read-only committed git objects; selftest isolated, no network or host probes | tsukuroi |

This is **not the update-safety gate** and clean never authorizes an action.
It checks a bounded documentation contract, not arbitrary Markdown semantics,
all prose truth or independent admission. C1's counting command uses the
same evaluator on baseline and immutable implementation; outputs and actual
selftest tally live in `.ufo/waves/round-16/`. QUALITY23/24 cite the mined
outside defects and constrain citation resolution and seat execution scope.
## Round 17 — boot-chain next-boot verdict, freshness after the 2026-10-20 upgrade, landed revisions

Authority: read-only observation, namespace emulation and source-grounded inference. Nothing here
authorizes a package, service, initramfs, bootloader or `/boot` action. Knowledge:
`corpus/knowledge/boot-chain-r17.md` (+ `.json`), `corpus/knowledge/freshness-recheck-r17.json`;
lesson `corpus/lessons/round-17.md`; QUALITY 25–27.

### Pre-reboot procedure (read-only; operator or agent)

1. `bash tools/boot-chain-audit.sh --live` from the lane worktree. It reads `/boot/limine.conf`
   and each entry's file through `sudo -n cat`, reads each image mtime through `sudo -n stat`,
   extracts `.uname`/`.initrd` and the initramfs unprivileged in a private mktemp directory, and
   prints one TSV row per limine entry plus `TSUKUROI_BOOTCHAIN: CONSISTENT|DEGRADED|UNKNOWN`
   (exit 0/1/2). It never writes `/boot` and runs no pacman, mkinitcpio or limine-update.
2. Read the verdicts: BOOTED-OBSERVED (firmware `LoaderEntrySelected` names the entry, its image
   predates the boot, no `/etc`/`/usr` boot input is newer); UNTESTED (non-snapshot entry never
   booted); PATH-ALIASED-EMULATED (42.x `/sysroot` init, image `/new_root -> sysroot`, hooks on
   `/new_root`); CONSISTENT-PRE42 (41.x `/new_root` directory init and hooks);
   NOT-A-KERNEL-ENTRY (no non-empty `.uname`, e.g. the Limine fallback). Anything else is UNKNOWN.
3. Compare each sha256 with the decision table in `boot-chain-r17.md`; a changed default UKI
   hash voids its BOOTED-OBSERVED verdict until the next boot.
4. Before relying on rollback, note which snapshot entries exist and their cleanup algorithm;
   the 2026-10-20 snapshot #1 is the only pre-upgrade image.

Rule from the round-17 mistake: never infer a path's role from a name-only listing
(`ls -d`, `dirs:`); record the entry type (`ls -l`, `lsinitcpio -v`) — the 42.x `/new_root` is a
symlink, not an empty directory (QUALITY 25).

### Gate and probe registry (round 17)

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| boot-chain | gate | `python tools/check-boot-chain.py --revision <REV> [--branch master]` | 0 pass; 1 failed (`BOOTCHAIN-MISSING`, verdict re-derivation, hash/evidence-line findings); 2 could-not-evaluate (`E-CLI`, `E-REVISION-*`) | `--selftest` (53 cases) | schema `tsukuroi-boot-chain-v2`; output `verdicted_kernel_entries` | none; git objects only | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` | `TSUKUROI_BOOTCHAIN: CONSISTENT` 0 / `DEGRADED` 1 / `UNKNOWN` 2 | `--selftest` (44 assertions, includes a `$(touch canary)` injection fixture) | verdict rules of schema v2 | private mktemp only; privileged reads `sudo -n cat`/`sudo -n stat` | tsukuroi |
| freshness-r17 | gate | `python tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 pass; 1 failed (`R17-FRESH-MISSING`, `STALE-UNFLAGGED`, append-only/quote/notice findings); 2 could-not-evaluate | `--selftest` (53 cases) | registry `corpus/knowledge/freshness-recheck-r17.json`; output `resolved_records` | none | tsukuroi |
| recheck-commands | gate | `python tools/check-recheck-commands.py --revision <REV> [--paths ...]` | 0 pass; 1 `RECHECK-FORBIDDEN-INVOCATION`; 2 could-not-evaluate | `--selftest` (40 cases) | last `recheck:` line, backticked argv0 only; forbidden `pacman,checkupdates,yay,paru,mkinitcpio,limine-update`; resolved by `## R17-RECHECK — steer-safe procedure` | none | tsukuroi |
| seat-scope | gate | `python tools/check-seat-scope.py --wave <dir> --revision <REV>` or `--worktree` | 0 pass; 1 `SCOPE-UNDECLARED` / `SCOPE-EXEC-UNAUTHORIZED` / `SCOPE-REPORT-MISSING`; 2 could-not-evaluate | `--selftest` (42 cases) | last `Scope: executed=` line; `EXEC-AUTHORIZED` token in the seat prompt | none | tsukuroi |
| revision-binding | probe | `python tools/check-revision-binding.py --tools-revision <REV>` | 0 = all five revision tools bound; 1 = fewer; 2 could-not-evaluate | `--selftest` (23 cases) | per tool: `HEAD` → 2 `E-REVISION-INVALID`; unlanded → 2 `E-REVISION-NOT-LANDED`; tip → JSON `revision` = tip | mktemp clone only | tsukuroi |

### Revision contract (supersedes the REV cells above at the round-12–16 rows)

Every `--revision` in `tools/` now takes `REV = 7–64 hex` that is an ancestor of
`refs/heads/<branch>` (default `master`) and, when present, of `refs/remotes/origin/<branch>`;
`HEAD`, `@`, `@-` and ref names are rejected. Exit 2 with `E-REVISION-INVALID`,
`E-REVISION-NOT-LANDED` or `E-REVISION-NOT-PUSHED`; JSON carries `branch` and `branch_tip`. This
replaces “REV = `HEAD` or 4–64 hex” in the locator-clarification and update-recheck rows and the
bare `--revision <commit>` of the root-dac, source-scope and section-citations rows. Selftest
tallies after round 17: locator 28, root-dac 23, section-citations 61, source-scope 25,
update-recheck 13 (new). Under jj, git `HEAD` is the working-copy parent: measure the branch tip
named by `scripts/hyaku/jj-lane.sh state`, never `HEAD`.

Round-17 late addition: `python tools/check-recheck-commands.py --revision <REV> --exec-log <lane path>` also checks a log of executed commands (`$ cmd` lines) against `--forbid`, emitting `EXEC-STEER-VIOLATION` (exit 1) and `exec_violation_count`; selftest 43 cases. An L1 keeps `.ufo/waves/round-<N>/l1-capture/exec-log.txt` for every host probe it runs under a narrowed steer (QUALITY 26).


## R18-FRESHNESS — SKILL.md current-use re-verification (2026-10-20)

Source S060: the fresh R18 L1 capture `.ufo/waves/round-18/l1-capture/host-capture-r18.txt` (read-only, 2026-10-20 16:06 -03). Context from S051, S052 and S059 is unchanged. This notice is append-only: the baseline bytes above stay as historical snapshots and dated sections. It supersedes only the current-use reading of the statements named below. It clears no package, reboot, rollback, snapshot or update-safety decision and authorizes no pacman, mkinitcpio, limine-update, snapper or service action.

- Line 118 (kernel): running kernel 7.2.11-arch1-1 and local-db entry linux-7.2.11.arch1-1 (.ufo/waves/round-18/l1-capture/host-capture-r18.txt:6, :32). The "both 7.2.3 today" reading is superseded.
- Line 120 (dkms): dkms status lists no 7.1.4-arch1-1 entry [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:5-7, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:92-96] (.ufo/waves/round-18/l1-capture/host-capture-r18.txt:95; block 93-95 lists 6.18.57-2-lts, 7.2.11-arch1-1 and 7.2.3-arch1-3). The 7.2.3-arch1-3 registration reports built modules missing. The "stale 7.1.4 registration is already present" reading is superseded.
- Lines 129-133 (rollback net): snapper config names root and home are present [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:75-81] (.ufo/waves/round-18/l1-capture/host-capture-r18.txt:80 conf.d SNAPPER_CONFIGS="root home"; :76-77 list home and root). The "`snapper list-configs` → empty" and "no snapshot net is configured" readings are superseded for config presence; snapshot existence unmeasured in R18 and snapper list-configs was not run, so no snapshot-count claim is made.
- Line 135 (transaction state): db.lck absent (.ufo/waves/round-18/l1-capture/host-capture-r18.txt:57). The last pacman.log entry 2026-10-20T13:23:09-0300 is a "Running 'pacman -D -q --asexplicit" line for zcode (.ufo/waves/round-18/l1-capture/host-capture-r18.txt:65). The "(last: 2026-10-13 16:37 `git-filter-repo`," reading is superseded. The R18 tail shows no "transaction completed" line, so completion is unknown.
- Line 1833 (mkinitcpio): mkinitcpio 42.2-1 installed (local database entry) [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39]: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:34. No mkinitcpio 41.1 entry appears in that listing. The "Installed `mkinitcpio 41.1-1` with 42.2-1 pending" reading is superseded; R17-FRESH-01 recorded the same fact at .ufo/waves/round-17/l1-capture/fresh-capture.txt:16. The compatibility sentence after it is not changed by this notice and remains an untested risk, not a clearance.


## R18-FRESHNESS — sibling current-use restatements (2026-10-20)

Sources S060, S051 and S052. This appended correction supersedes the current-use readings listed below and every repeated current-use restatement of the same premise in this file. Historical measurements remain intact. No package, service, rebuild, boot or rollback action is authorized.

- R18-FRESH-SUPPLEMENT-01: prior locus ``checkupdates`/`paccache` absent (`pacman-contrib` not installed); `yay` present, network`. Now: S060 lists pacman-contrib-1.13.1-1 in local metadata and resolves /usr/bin/paccache; old package/paccache-absence guidance is not current. This capture does not query or resolve checkupdates, so its availability and any use elsewhere remain unknown; no installation is advised [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:82-86]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:83.

- R18-FRESH-SUPPLEMENT-02: prior locus `- `checkupdates` / `paccache` absent; **installing `pacman-contrib` is out of`. Now: S060 lists pacman-contrib-1.13.1-1 in local metadata and resolves /usr/bin/paccache; old package/paccache-absence guidance is not current. This capture does not query or resolve checkupdates, so its availability and any use elsewhere remain unknown; no installation is advised [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:82-86]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:83.

- R18-FRESH-SUPPLEMENT-03: prior locus ``systemd-oomd` inactive+disabled, `earlyoom` absent, `MemoryPressureWatch=skip` (`:277-281`) —`. Now: earlyoom is installed1.9.0-1 and active/enabled atR18; this later state cannot explain the historical OOM or certify other memory guards [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:16-23, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:17.

- R18-FRESH-SUPPLEMENT-04: prior locus `scope holds 5 active timers — a different plane (`timer-drift-plane.md:21-26,47-68,203-217`).`. Now: the five-timer statement is historical, not a new current total; snapper-timeline.timer and snapper-cleanup.timer are enabled in the R17 system-scope capture. Enabled state does not establish the active/all timer count [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:75-81, .ufo/waves/round-17/l1-capture/fresh-capture.txt:47-51]. Capture: .ufo/waves/round-17/l1-capture/fresh-capture.txt:47.


## R18-REGISTRY-SCOPE — frozen fixture authority and current-use limits

The round16 section-citations registry cell at:1857 calls `.ufo/waves/round-16/build/frozen-cases.json` independent attack vectors. That authority claim is withdrawn: the JSON is retained historical/non-normative evidence, superseded by `frozen-cases.SUPERSEDED.md`; it disagrees with the actual MD-finding count and R16-SOURCE-ROW classification. The current in-source selftest has independent fixed expectations but is not an independently authored external oracle. Read the final round18 registry below for measured commands/counts; a prior receipt's43/61 count remains historical.

The line1834 current-use 'untested risk' reading is also narrowed by round17: image `/new_root` is a symlink to`/sysroot` in the42.2 UKIs and pathname compatibility was namespace-emulated. This is not a whole snapshot boot or rollback certification. Source S059 and `corpus/knowledge/boot-chain-r17.md` distinguish BOOTED-OBSERVED, PATH-ALIASED-EMULATED and remaining unknowns. Never revive a predicted silent no-op from the historical pending-upgrade paragraph.

Revision-binding judge trust boundary: reviewed lane-owned scripts execute with caller UID in a disposable clone; the clone confines its Git mutations, not arbitrary subprocess/filesystem/network authority. It is not a sandbox for untrusted programs. Global/system Git configuration and hooks are suppressed by the judge's own Git runner. Finite probes + source review do not prove behavior on every possible input.


## Gate and probe registry — round18 superseding current rows

These rows supersede the round12–17 registry descriptions/counts for current use; earlier rows remain historical. The misleading53/44/five-tools/probe/23 and capability44 figures are not current assertions. Do not copy a selftest tally into a second registry cell: the committed execution ledger `.ufo/waves/round-18/measure/final/results.json` is the per-command observed tally/exit at its named measured revision; fixtures and fixed expectations remain in the tools. A new code change requires a new receipt, not reuse of the last tally.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (live mode not run round18) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane rules and fixed fixture assertions in tool | live probes read-only; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` (in-memory and isolated CLI Git fixtures) | R13 exact correction claims and fixed expectations in tool | committed git reads; private selftest clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 scope/comment correction fields and source bindings | committed git reads; private selftest clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 exact source/positive-definition correction fields | committed git reads; private selftest clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 observation count (not a health/upgrade clearance);1 failed;2 could-not-evaluate | `python3 tools/measure-update-recheck.py --selftest` | R15 snapshot/probe/schema inputs and fixed selftest values | committed git reads; private selftest clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | exact R16 headings/rows/quotes and source expectations; old frozen-cases.json is historical/non-normative, NOT independent oracle | committed git reads; private selftest clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV>`; C1 mode adds `--statement-corrections` | 0 clean;1 failed;2 could-not-evaluate; default emits verdicted_kernel_entries, C1 emits correction_count | `python3 tools/check-boot-chain.py --selftest` | default schema/image evidence rules; C1 fixed R18-CORR01..04, package argv, both UKI/installed hashes and live-versus-history mtime | committed git reads; private selftest clones | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not run round18) | 0 CONSISTENT;2 UNKNOWN (the live summary never emits 1; 1 is only a selftest assertion failure); not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 per-entry verdict rules | private mktemp; privileged live reads only when separately authorized | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed including STALE-UNFLAGGED;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and baseline/capture quote bindings | committed git reads; private selftest clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> --registry corpus/knowledge/freshness-recheck-r18.json [--registry-from <REV>]`; structural C1 uses statement-corrections-r18.json | 0 structurally clean;1 failed including missing/stale notice;2 could-not-evaluate; structural conformance is not semantic source agreement | `python3 tools/check-appended-notices.py --selftest` | schema tsukuroi-appended-notices-v1, baseline842a531, record/notice/capture constraints; C1 domain truth checked separately by boot-chain mode | committed git reads; private selftest fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <lane path>]` | 0 bounded clean;1 RECHECK-FORBIDDEN-INVOCATION or EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | last recheck directive, pointer/direct command scope, R17/R18-RECHECK replacement; forbidden binary set; emitted exec-log command parsing | committed git reads; private selftest fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <dir> --revision <REV>` | 0 bounded clean;1 SCOPE-UNDECLARED/EXEC-UNAUTHORIZED/REPORT-MISSING/TRAILER-MALFORMED;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | scoped item EXEC-AUTHORIZED token and reported executed line; not a complete independent execution audit | committed wave artifact reads; private selftest clones | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV>` | 0 original-nine consistency clean;1 fewer consistent;2 could-not-evaluate. consolidation_status/consolidated_tools ALSO require shared_tools9/copies0; new discovered tools reported separately | `python3 tools/check-revision-binding.py --selftest` | original nine required even if absent; D1–D6, origin-absent/blob-ref and strict refusal probes; AST import+bind-call census and literal copy count, not universal behavior proof | disposable clone/ref/probe commits only; reviewed trusted scripts execute with caller authority | tsukuroi |

### Shared revision adapter

All nine consumers and the new notice checker use `tools/_revision.py`; the measuring judge intentionally keeps independent binding. Branch syntax is checked before revision syntax, then commit resolution, local-branch presence/ancestry, then optional origin ancestry. Non-commit/unknown commit selectors are E-REVISION-INVALID; an unavailable repository, missing Git or fatal ancestry operation is E-GIT-FAILED. Every refusal is a single finding/exit2; other branch ids E-BRANCH-INVALID/E-BRANCH-MISSING and landing ids E-REVISION-NOT-LANDED/E-REVISION-NOT-PUSHED. `sys.dont_write_bytecode` precedes the import so read-only invocations do not generate tools/__pycache__. Module selftest: `python3 tools/_revision.py --selftest`; independent actual tally lives in the same execution ledger.


## R18-FRESHNESS — standing sar capture capability (2026-10-20)

Source S060. Supersedes current-use guidance in the whole historical standing capability bullet at1123–1125, not its historical lack of pre-kill samples. S060 resolves /usr/bin/sar and its /var/log/sa listing is empty, not a missing directory. This does not backfill a pre-kill snapshot; the other named tools were not independently re-audited for integrity or current use. Supporting context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:82-88

Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:84. No package, restart, boot or recovery action is authorized.


## R18-PRECISION — time bounds, refusal metadata and measured claims

R17's snapshot#1/only-pre42 image statement is a dated inventory observation, not a guarantee that the entry/image is still available at R18. S060 did not inspect boot entries or UKI hashes. Current snapshot availability, selected/default image identity and recovery feasibility must remain unknown until separately authorized fresh evidence; no current --live audit or boot action is inferred from the old pre-reboot checklist.

For a real C1 red-before comparison, use the same final evaluator and fixed correction metadata: `python3 tools/check-boot-chain.py --revision <BASELINE> --statement-corrections --registry-from <LANDED-TARGET>`, then substitute the target for BASELINE. Without --registry-from, an old tree has no new registry and reports only missing metadata. The metadata-held-fixed comparison yields the four named unresolved actual correction defects.

On a refused revision, exit2 is could-not-evaluate. Its JSON revision field is diagnostic (raw requested selector, or a target already resolved before another input failed), not a certified measured SHA; branch_tip may be null when binding failed. Only successful binding certifies the resolved commit. Root-DAC's raw-selector refusal is an intentional clean cutover, not an unchanged-error-payload claim. No caller should grade an exit2 payload as landed evidence.

Revision judge status_scope explicitly distinguishes original-nine consistency from consolidation_status/consolidated_tools. A PASS consistency result alone does not certify shared code; consolidation requires consistency, shared static bind use and zero local copies together. Both statuses are bounded probes plus source review, not universal program equivalence.

The build count88/49+39 is an intermediate snapshot. The standing sar neighbor adds one supplementary record: final candidate registry89=49primary+40supplementary across17paths. Main immutable measurements, not this declaration, determine the admitted count; the checker verifies declared records and cannot establish complete freshness of the host or the corpus.


## Operative registry resolution — round18

Current registry consumers MUST select the complete table under `## Gate and probe registry — round18 superseding current rows`, not the first table encountered. For later rounds, select the unique highest-numbered heading of that exact form; a missing/duplicate highest table is could-not-evaluate, never fallback to an older row. Earlier tables, including section-citations1857 and the round17 rows1897–1902 (53/44/five-tools/probe/23), are historical and NON-OPERATIVE. Their frozen-JSON authority and tallies are explicitly withdrawn for current use. Actual selected rows are retained in `.ufo/waves/round-18/measure/final/operative-registry.json`; exact executions/tallies in its results.json.

The revision-binding entry's exit0/status refers only to original-nine consistency. `consolidation_status` and `consolidated_tools` additionally require shared bind calls and zero local copies; do not infer consolidation from the consistency field alone. The scope gate reports declarations: SCOPE-TRAILER-MALFORMED distinguishes annotated/ambiguous none from a declared unauthorized command list. Neither canonical none nor any reported count proves actual absence of execution.

This operative selector is an append-only correction. In-place annotation of historical cells would break the explicitly measured baseline-prefix preservation; it is not used to solve a calibration defect by harming freshness/history. The earlier 'These rows supersede' paragraph is now a precise operative convention rather than an assumption that a first-table reader scans further.

## R19 — expected /boot writers (decision table)

Authority: read-only attribution of `/boot/limine.conf` writes seen in the round-19 captures (window 2026-10-19 00:00 to 2026-10-20 17:58 -03). Detection only. Nothing here authorizes running `limine-snapper-sync`, `limine-update`, `limine-install`, `snapper`, `mkinitcpio`, any pacman command, `systemctl start|stop|restart|enable`, or any `/boot` write. Every action below is record, report, or operator handoff.

Evidence and pointers:
- Capture files (lane-relative, read-only): `.ufo/waves/round-19/l1-capture/host-capture-r19.txt` (`r19`), `host-capture-r19b.txt` (`r19b`), `host-capture-r19c.txt` (`r19c`).
- Knowledge entry `corpus/knowledge/boot-writers-r19.md` (registry `corpus/knowledge/boot-writers-r19.json`; gate `python3 tools/check-boot-writers.py --revision <REV>`), sources S066-S076.
- Window total: 10 journal `Updated: /boot/limine.conf` events since 2026-10-19 (`r19c:11-20`; count `r19:562-563`, `r19b:1685-1686`) plus 3 ALPM-SCRIPTLET events in the whole pacman.log (`r19b:1695`, `1700`, `1702`; pacman.log 2021, 3015, 3047) = 13 attributed events (EV-01..EV-13 in the knowledge entry).

### Writer classes

| Signature seen | Writer | Expected when | Action |
|---|---|---|---|
| `Updated: /boot/limine.conf` with `_SYSTEMD_UNIT=snapper-cleanup.service` | W-SNAPPER-CLEANUP (W1) cleanup stop. Drop-in `ExecStopPost=limine-snapper-sync` (`r19:256-260`), timer `OnBootSec=10m` / `OnUnitActiveSec=1h` (`r19:221-231`) | Once per hourly `snapper-cleanup.timer` run. Observed 8 (`r19c:13-20`) | Record unit and PID. No action. |
| `Updated` with `_SYSTEMD_UNIT=limine-snapper-add-<id>-<pid>.service` | W-SNAPPER-PLUGIN (W2) snapper create plugin. `create-snapshot-post` runs `systemd-run --unit=limine-snapper-add-…` (`r19b:1184-1188`, dispatch `r19b:1229-1230`) | Seconds after a `snapper … create` in sudo trace (`r19c:29`→`r19c:11`; `r19c:43`→`r19c:12`). Observed 2 | Match to the sudo `COMMAND=/usr/bin/snapper` line; record. |
| `Updated` with `_SYSTEMD_UNIT=limine-snapper-delete-…` or `…-modify-…` | W-SNAPPER-PLUGIN (W3) snapper delete/modify plugin, `--debounce` (`r19b:1175-1176`, dispatch `r19b:1231-1236`) | After a snapper delete or modify. Observed 0 in window. Whether a delete ran is `[unk]` | Record. State "none observed" if absent. |
| `[EVENT] <CREATE|DELETE> -> <id>` from `limine-snapper-watcher` | W-WATCHER (W4) watcher service, `ExecStart=limine-snapper-watcher` (`r19:153-161`) | Only when `inotifywait` is installed. Not installed on this host: watcher prints fallback and exits 0 (`r19b:1365-1367`; journal `r19b:1645`, `1665`, `1675`, `1683`) | Any `[EVENT]` line in a boot that also shows the fallback line is error E3. |
| `ALPM-SCRIPTLET] Copied: /tmp/limine-mkinitcpio.*.efi -> /boot/EFI/Linux/…` then `ALPM-SCRIPTLET] Updated: /boot/limine.conf` | W-MKINITCPIO-HOOK (W5) pacman hook `90-mkinitcpio-install.hook` → `limine-mkinitcpio-install` (`r19:379-398`) | Inside the `running '90-mkinitcpio-install.hook'` span of `/var/log/pacman.log`. Observed 2026-10-11 16:16:36 and 2026-10-20 09:18:18/09:18:24 (`r19b:1695`, `1700`, `1702`; span `r19b:1688-1703`) | Confirm the span (step 2). Record. |
| `running '80-limine-efi-deploy.hook'` or `running '99-limine.hook'` span | W-LIMINE-EFI-DEPLOY / W-LIMINE-EFI-COPY (W6) deploy hooks. `80` runs `/usr/bin/limine-install` (`r19b:1399-1430`); `99` copies `BOOT*.EFI` (`r19:399-403`) | Copies EFI binaries. No `limine.conf` update observed in these spans (`pacman.log` 2977-2983, 3050, via `r19b:1697-1703`) | Not a `limine.conf` writer. An `Updated` line inside its span is error E5. |
| no line; `snapper` plugin `set-default-snapshot-pre` | (W7, not a limine.conf writer class in the registry) restore hook → `limine-snapper-restore --kernels` (`r19b:1237-1239`) | Only on set-default or rollback. Observed 0. `[inf]` that restore adds a backup entry (`README.md:38`, `r19b:51`) | Record only. |

Not a writer: `10-limine-snapper-lock.hook` (PreTransaction, `r19:347-353`; `limine-snapper-lock` takes `mutex_lock "limine-snapper-lock"`, `r19b:1389-1397`).

### Error patterns

- **E1 UNATTRIBUTED.** `Updated: /boot/limine.conf` whose `_SYSTEMD_UNIT` is none of `snapper-cleanup.service` or `limine-snapper-{add,delete,modify}-*`, and which has no ALPM line inside a `running '90-mkinitcpio-install.hook'` span. Action: ERROR. Report timestamp, PID and unit. Take no further action.
- **E2 UKI copy outside a pacman transaction.** `Copied: /tmp/limine-mkinitcpio.` or `-> /boot/EFI/Linux/` in any source outside a 90-mkinitcpio span. Journal copies to `/boot/<id>/limine_history/` are normal (`r19c:23`, `r19c:39-40`) and are not this pattern. Action: ERROR.
- **E3 watcher active.** `[EVENT]` from `limine-snapper-watcher` in a boot whose journal also shows the `inotifywait is not installed` fallback line. Action: ERROR. Identify which writer produced the event.
- **E4 stale lock.** `/run/limine-snapper-cleanup.lock` exists while `snapper-cleanup.service` is inactive. The drop-in creates it in `ExecStartPre` and removes it in `ExecStopPost` (`r19:258-259`). Action: report. Never remove it.
- **E5 deploy-hook write.** `Updated: /boot/limine.conf` inside a `80-limine-efi-deploy` or `99-limine` span. Action: ERROR.
- **E6 no-lock-skip inference.** The lock check lives in the watcher only (`r19b:1373-1374`, watcher lines 126-128). The snapper plugin skip (`r19b:1160-1169`) checks only `limine-snapper-sync.service` and `pgrep limine-snapper-watcher`. The cleanup `ExecStopPost` runs `limine-snapper-sync` directly with no lock check. Absence of a limine line during a cleanup run is **not** evidence of a lock skip. Unexplained observation: `snapper-cleanup.service` ran 09:03:03–09:08:04 with no limine line (`r19c:46-57`). Status `[unk]`.

### Read-only checklist (5 steps)

Forbidden in this checklist: `sudo`, `limine-update`, `limine-snapper-sync`, `snapper`, `mkinitcpio`, `pacman` (any form), `checkupdates`, `yay`, `paru`, `systemctl start|stop|restart|enable`, any `/boot` write.

1. Attribute journal writes by unit (verbatim form `r19c:5-10`, with the MESSAGE filter in Python):
   `journalctl --no-pager --since "2026-10-19 00:00" -t limine-snapper-sync -o json --output-fields=_SYSTEMD_UNIT,_SYSTEMD_CGROUP,_COMM,_PID,MESSAGE`
   Keep lines whose MESSAGE contains `/boot/limine.conf`. Count by `_SYSTEMD_UNIT`. Expected: `snapper-cleanup.service` plus the `limine-snapper-add-*` units only.
2. Bracket pacman writes (adapted from `r19b:1688`; not run in this exact form):
   `grep -n -E "ALPM-SCRIPTLET\] (Copied: /tmp/limine-mkinitcpio|Updated: /boot/limine.conf)|running '(80-limine-efi-deploy|90-mkinitcpio-install|99-limine)\.hook'" /var/log/pacman.log`
   Every ALPM `Updated`/`Copied` line must sit between its own `running '90-mkinitcpio-install.hook'` line and the next `[ALPM] running` line. Otherwise E1/E2/E5.
3. Snapper trigger trace (`r19c:22-37`, `sed` omitted):
   `journalctl --no-pager -o short-iso -t sudo | grep -E "COMMAND=/usr/bin/(snapper|systemctl) "`
   Match each add-unit start to a `snapper … create` line.
4. Unit, timer and watcher wiring (`r19:153-161`, `r19:220-231`, `r19:262-265`):
   `systemctl cat snapper-cleanup.service --no-pager`; `systemctl cat limine-snapper-sync.service --no-pager`; `systemctl list-timers --all --no-pager "snapper*"`; `command -v inotifywait || echo "inotifywait absent"`. If `inotifywait` is present, E3 applies to any `[EVENT]` line.
5. Lock and hook wiring (`r19:258-259`, `r19:346-409`):
   `ls -l /run/limine-snapper-cleanup.lock 2>&1`; `systemctl is-active snapper-cleanup.service`; `grep -H -E "^(Target|Exec|When|Operation)" /usr/share/libalpm/hooks/*limine* /etc/pacman.d/hooks/*limine* /etc/pacman.d/hooks/90-mkinitcpio-install.hook`.
   A lock present with an inactive cleanup unit is E4. Report it; never remove it.

Output every step, including the ones that pass. Record each signature in the table's first column with its unit, PID and timestamp.

W-KERNEL-REMOVE (60/90-limine-mkinitcpio-remove hooks) is a registry writer class with no event in the captured windows. Expected automation (round-18 closure §5 item 6): the hourly W-SNAPPER-CLEANUP rewrite is designed behaviour (S076: upstream fix for issue 4 syncs after cleanup), so a `/boot/limine.conf` mtime within the last hour of a cleanup run is not drift; `tools/boot-chain-audit.sh` already excludes limine.conf from its digest pins (`tools/boot-chain-audit.sh:60`).

## Gate and probe registry — round19 superseding current rows

These rows supersede the round18 table for current use (round-19 C3: tools/_revision.py gains its row, closure defect 2; ScoutRegistryRowsA/B corrections to update-recheck, recheck-commands, seat-scope and boot-chain cells); the round18 table and every earlier registry table are historical and non-operative. The operative table is the unique highest-numbered heading of the exact form `## Gate and probe registry — round<N> superseding current rows`; a missing or duplicate highest table is could-not-evaluate and never a fallback to an older row. Carried-forward rows keep their round18 text except where round-19 source review found it false. Do not copy a selftest tally into a registry cell: the round-19 ledger `.ufo/waves/round-19/measure/final/results.json` holds per-command tallies at its measured revision, and a new code change requires a new receipt.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (live mode not run round18 or in round-19 captures) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane rules and fixed fixture assertions in tool | live probes read-only; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` (in-memory and isolated CLI Git fixtures) | R13 exact correction claims and fixed expectations in tool | committed git reads; private selftest clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 scope/comment correction fields and source bindings | committed git reads; private selftest clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 exact source/positive-definition correction fields | committed git reads; private selftest clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 observation count COUNTED or ABSENT (not a health/upgrade clearance);2 could-not-evaluate (any other status, including revision refusal);1 emitted only by --selftest FAIL, never by the CLI | `python3 tools/measure-update-recheck.py --selftest` | R15 snapshot/probe/schema inputs and fixed selftest values | committed git reads; private selftest clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | exact R16 headings/rows/quotes and source expectations; old frozen-cases.json is historical/non-normative, NOT independent oracle | committed git reads; private selftest clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV>`; C1 mode adds `--statement-corrections` | 0 clean;1 failed;2 could-not-evaluate; default emits verdicted_kernel_entries, C1 emits correction_count | `python3 tools/check-boot-chain.py --selftest` | default schema/image evidence rules; C1 fixed R18-CORR-01..R18-CORR-04, package argv, both UKI/installed hashes and live-versus-history mtime | committed git reads; private selftest clones | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not run round18 or in round-19 captures) | 0 CONSISTENT;1 DEGRADED;2 UNKNOWN; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 per-entry verdict rules | private mktemp; privileged live reads only when separately authorized | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed including STALE-UNFLAGGED;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and baseline/capture quote bindings | committed git reads; private selftest clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> --registry corpus/knowledge/freshness-recheck-r18.json [--registry-from <REV>]`; structural C1 uses statement-corrections-r18.json | 0 structurally clean;1 failed including missing/stale notice;2 could-not-evaluate; structural conformance is not semantic source agreement | `python3 tools/check-appended-notices.py --selftest` | schema tsukuroi-appended-notices-v1, baseline 842a531; record/notice/capture constraints; C1 domain truth checked separately by boot-chain mode | committed git reads; private selftest fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <lane path>]` | 0 bounded clean;1 failed (RECHECK-FORBIDDEN-INVOCATION, RECHECK-POINTER-UNRESOLVED, RECHECK-STEER-SAFE-INVALID or EXEC-STEER-VIOLATION);2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | last recheck directive, pointer/direct command scope, R17/R18-RECHECK replacement; forbidden binary set; emitted exec-log command parsing | committed git reads; private selftest fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <dir> --revision <REV>` (or `--worktree`) | 0 bounded clean;1 SCOPE-UNDECLARED/EXEC-UNAUTHORIZED/REPORT-MISSING/TRAILER-MALFORMED;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | scoped item EXEC-AUTHORIZED token and reported executed line; not a complete independent execution audit | committed wave artifact reads; private selftest clones | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV>` | 0 original-nine consistency clean;1 fewer consistent;2 could-not-evaluate. consolidation_status/consolidated_tools ALSO require shared_tools9/copies0; new discovered tools reported separately | `python3 tools/check-revision-binding.py --selftest` | original nine required even if absent; D1–D6, origin-absent/blob-ref and strict refusal probes; AST import+bind-call census and literal copy count, not universal behavior proof | disposable clone/ref/probe commits only; reviewed trusted scripts execute with caller authority | tsukuroi |
| revision-binder | library | imported by the gates via `from _revision import bind, RevisionError` (no direct CLI) | 0 selftest PASS;1 selftest FAIL;64 usage when run without --selftest | `python3 tools/_revision.py --selftest` (tally: see measure/final/results.json) | public API bind, Binding, RevisionError, branch_tip, clean_env; E-REVISION-INVALID, E-BRANCH-INVALID, E-BRANCH-MISSING, E-REVISION-NOT-LANDED, E-REVISION-NOT-PUSHED, E-GIT-FAILED; importers check-appended-notices, check-boot-chain, check-freshness-r17, check-locator-clarification, check-recheck-commands, check-root-dac-correction, check-section-citations, check-seat-scope, check-source-scope-correction, measure-update-recheck | bind() reads Git only; --selftest writes only its mktemp git sandbox | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry corpus/knowledge/adjacency-anchors-r19.json] [--registry-from <REV>] [--siblings-root <DIR>]` | 0 clean;1 failed (ANCHOR-*, INBOUND-*, CENSUS-* findings);2 could-not-evaluate, including E-* revision refusals | `python3 tools/check-adjacency-anchors.py --selftest` (tally: see measure/final/results.json) | schema tsukuroi-adjacency-anchors-r19-v1; PROVINCE section heading `## Adjacent — portable ownership anchors (round 19)`; census .ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json; counts reported in payload, not pinned here | committed git object reads at the bound revision; --siblings-root read-only; selftest mktemp fixtures only | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry corpus/knowledge/boot-writers-r19.json] [--registry-from <REV>]` | 0 clean;1 failed (EVENT-*, WRITER-*, MECHANISM-* findings);2 could-not-evaluate, including CAPTURE-TAMPERED | `python3 tools/check-boot-writers.py --selftest` (tally: see measure/final/results.json) | schema tsukuroi-boot-writers-r19-v1; knowledge entry corpus/knowledge/boot-writers-r19.md; capture digests pinned in registry; event denominator enumerated by the gate from probe blocks; no /boot access | committed git reads; captures read from the registry revision; selftest mktemp fixtures only | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--branch master] [--baseline-tools <REV>]` | 0 clean;1 failed (REGISTRY-ROW-MISSING, REGISTRY-ROW-DUPLICATE, REGISTRY-ROW-ORPHAN, REGISTRY-KIND-INVALID, REGISTRY-SELFTEST-UNRESOLVED, REGISTRY-VERDICT-INCOMPLETE);2 could-not-evaluate, including E-REGISTRY-TABLE | `python3 tools/check-registry-coverage.py --selftest` (tally: see measure/final/results.json) | operative table = unique highest round<N> heading of the exact form above; 8-cell header exact; a row covers tools/F when its Entry or Self-test cell contains tools/F; baseline split via --baseline-tools | committed git reads (SKILL.md, tools tree); selftest mktemp fixtures only | tsukuroi |

## R20 — named corrections and read-only limits

**R20-FALSE-OPERATIVE-MAP:** the round19 fleet-report erratum C3 and LOG repair paragraph falsely said the operative boot-chain-audit row had stopped advertising live `1 DEGRADED`; the selected round19 row still did so. Only a historical round18 row was changed. The round20 table below is the actual current repair. Under schema-v2, the live audit returns `0 CONSISTENT` or `2 UNKNOWN`; `1` belongs to failed selftests, not the live summary. Neither result is package, service, hook, initramfs, bootloader or reboot clearance. See `corpus/lessons/round-19-verifier-spotcheck.md` §2 C3 and §5 items2–3, and `tools/boot-chain-audit.sh` summary code.

**R20-SKILL-PREFIX-EXCEPTION:** the round19 report's claim that all SKILL edits were append-only was false: its committed SKILL delta was+80/−1, changing a historical registry row. That exception is disclosed here and in LOG/round20 lesson, not repaired by rewriting the report or pretending the prefix was preserved. Round20 appends its current registry; earlier rows remain historical/non-operative.

**R20-OUT009:** follow PROVINCE `## R20 ownership clarification — OUT-009`. Revenger's precise declaration names Electron/JavaScript packages, not arbitrary packages; it is attributed sibling text, not an ownership grant. Kaidoku/Revenger arbitration remains unresolved. No handoff transfers remediation permission, and prepared/acknowledged is not accepted/resolved.

**R20-RULE4:** `corpus/knowledge/boot-writers-r19.md` `## R20-RULE4 — named supersession of Operator decision rule item 4` explicitly controls the older “No write” rule. No matching captured `Updated:` event does not prove no write or unchanged contents; the 09:08:04 cause remains unknown.

Object-selector and execution-log checks are bounded syntax/fixture evidence, not arbitrary program or shell proofs. A hexadecimal-looking ref must never substitute for a matching object ID. A unique annotated-tag object ID may still peel to a commit under the preserved commit-ish contract. Independently recheck current public hook bodies before any freshness statement; no fresh image/boot evidence is supplied by these documentation repairs.

## Gate and probe registry — round20 superseding current rows

The unique highest numbered complete table is operative; every earlier table is historical. No historical tally is copied into a current selftest result. The C1 ownership-correction mode, C2 object-selector mode and C3 audit-live-map mode have finite separate metrics; default modes retain their earlier scope. All actual receipts must name their measured revision.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round20) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2, finite per-entry rules | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directive/pointer rules, forbidden binaries, finite systemctl read-verb/option checks and bounded wrapper/shell recursion in exec-log lines; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | dispatch authorization and reported execution declarations, never independent execution audit | committed wave reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors]` | 0 finite original-nine checks clean;1 failed;2 could-not-evaluate; discovered tools separately reported | `python3 tools/check-revision-binding.py --selftest` | default consistency/consolidation probes; object selectors grade original nine only with exact SHA on accepted rows, exact status/ID on refusals (revision may echo the request), ghost/full-ref aliases, prefix shadows, uppercase, tag peeling, noncommit and ambiguity; not universal tag-target coverage | disposable external clone/ref/probe commits only; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py` bind/Binding/RevisionError/branch_tip/clean_env; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding contract; unique object-only hex lookup; direct and nested annotated tags to commit; blob/tree and annotated tag-to-blob/tree rejection; ghost refs and landed-prefix shadows | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | r19 finite10/114 anchor census; opt-in C1 correction is pinned to exact text/hash, exact append after baseline, and same-revision registry/census evidence; arbitration stays unresolved; metric absent in default mode | committed object reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | r19 finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads only; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | generic highest-table coverage unchanged; opt-in finite schema-v2 map reads Markdown outside fences, requires one audit-path row with live `--live`, selftest `--selftest`, exact live0/2 versus selftest1 map and no-write scope; not universal program semantics | committed reads; selftest private fixtures | tsukuroi |


## R21 — typed selectors and review evidence

Use `corpus/knowledge/selector-contract-r21.md` for the five source-grounded decisions (S081/S082). Typed commit peeling and empty-brace peeling are not equivalent. The new opt-in `--object-target-types` matrix runs original-nine consumers over non-empty trees, tags to blob/tree, nested and ordinary commit tags, with direct Git-created object identities. Its coverage metric includes finite AST availability and reports behavioral success separately: missing old coverage is not evidence that the unchanged binder was broken. Round20 object-selector cases/count remain unchanged.

Primary review snapshots and exact predicates are preregistered before dispatch; the receipt gate checks declarations only, not actual reading or independent command absence. Missing dead-seat reports remain non-clean; malformed historical trailers and retroactive reservations are never rewritten into passes. Actual final measurements and deaths live in SCORECARD/round21 lesson, not these instructions. No host or package/service/boot action follows any result.

## Gate and probe registry — round21 superseding current rows

The unique highest complete table is operative; older tables remain historical. All retained modes preserve their earlier contracts. No unrun selftest tally is stated.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round20) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2, finite per-entry rules | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directive/pointer rules, forbidden binaries, finite systemctl read-verb/option checks and bounded wrapper/shell recursion in exec-log lines; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | dispatch authorization and reported execution declarations, never independent execution audit | committed wave reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` (select at most one matrix) | default/object-selectors:0 finite original-nine checks clean; target-type:0 mode available and five behavioral classes clean;1 failed;2 could-not-evaluate; discovered tools separately reported in legacy modes | `python3 tools/check-revision-binding.py --selftest` | old object-selector cases/count unchanged; new mode counts availability once and reports actual behavior separately; non-tip commit tags, exact refusal observations and finite mutation witnesses, never universal semantics | disposable external clone/ref/probe commits only; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py` bind/Binding/RevisionError/branch_tip/clean_env; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding contract; unique object-only hex lookup; direct and nested annotated tags to commit; blob/tree and annotated tag-to-blob/tree rejection; ghost refs and landed-prefix shadows | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | r19 finite10/114 anchor census; opt-in C1 correction is pinned to exact text/hash, exact append after baseline, and same-revision registry/census evidence; arbitration stays unresolved; metric absent in default mode | committed object reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | r19 finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads only; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | generic highest-table coverage unchanged; opt-in finite schema-v2 map reads Markdown outside fences, requires one audit-path row with live `--live`, selftest `--selftest`, exact live0/2 versus selftest1 map and no-write scope; not universal program semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision or visible table/source/policy mismatch;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five class/outcome/finding/source/policy tuples; S081/S082 and corpus/knowledge/selector-contract-r21-corrected.json/.md supersede original representation; not actual consumer or host behavior | immutable Git reads; selftest isolated in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest .ufo/waves/round-21/reviews.json]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered review manifest SHA-256/predicate and committed primary snapshot bytes; declares identities, never proves reading or command nonexecution | immutable Git reads; selftest isolated in-memory fixtures | tsukuroi |

### R21 hardening supersession and execution-scope limit

The active C1 entry/data are `corpus/knowledge/selector-contract-r21-corrected.md` and `.json`; the original r21 entry/JSON remain historical and its appended R21-TYPE-PROVENANCE notice controls earlier links. Manual type propositions and QUALITY27/36 lane policy are separate. C1's visible table/source/policy checks and C2's finite non-tip/ref-shadow/typed-fixture controls are not universal prose or Git-semantic proofs.

C3 checks declared primary byte/predicate/scope receipts. Actual Bash/eval/child calls override a false `executed=none` declaration; original reports stay immutable and independent tool-call metadata must disclose contradictions. Known provider deaths remain missing/non-clean and are never replaced. A green declaration check cannot clear an observed scope violation, prove reading or grant outside admission. No package/service/boot action follows.

## R22 — prompt scopes, recorded requests and finite receipt accounting

`corpus/knowledge/seat-boundary-r22.md` and `.json` hold six explicit lane-policy decisions (S083/S084), not native permissions. Every source-only seat declares exact absolute read/write paths and empty commands/fetches before dispatch. NO-EXEC includes harmless hash/list/import/test/eval/child calls; NO-FETCH includes URL reads and search/browser/unknown remote interfaces. A local read selector is not a URL exception. Only the exact `skill://godspeed` URI is an approved skill read in this round's seats.

The host exposes native tools to every seat; `task.tools` adds extras and cannot remove them. Nothing here prevents, contains, reverts or proves absence of an out-of-scope operation. `check-seat-bindings.py` rejects scope evidence **at judgment time, not at call time**. It classifies recorded request spellings, rejects unknown/malformed/incomplete evidence, recursively inspects parallel requests, and does not resolve symlink effects or establish recorder completeness. Names ending `DENIED` are post-hoc policy finding IDs, not observed blocking.

`check-review-cohort.py` independently accounts for the fixed declared cohort using the unchanged strict receipt evaluator. Its `delivered_conformant` key means **receipt-well-formed only**, never command/fetch conformance, reading or no-harm. Report all four buckets, strict receipt exit/findings, and actual request violations separately; actual requests override false none assertions. No failed seat is replaced and no historical receipt is rewritten. Full native enforcement belongs to kumitate/operator runtime authority; lane-local detection does not absorb that province or authorize host actions.

## Gate and probe registry — round22 superseding current rows

The unique highest complete table is operative; older rows remain historical. New C1/C2/C3 have independent content inputs and modes. All outputs name the actual measured landed revision; availability metrics are not counts of repaired historical behavior.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | frozen prompt path lists, empty exec/fetch lists, exact request spelling rules; post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |

### R22 registry literal correction

The round22 audit row retains the frozen round20 command/map/no-write strings required by the finite `--audit-live-map` contract; its historical parenthetical does not mean this round live-ran the host probe. No live host probe ran round22. The first round22 draft paraphrased those API-significant cells and failed the unchanged semantic gate; its original committed bytes and red output remain evidence. This named same-round operative-row correction does not alter any earlier-round table or the checker under judgment.

## R23 — structured target authority and reconciled path census

C1 is an eight-row declared document contract, not eight repaired behaviors. S086 is a four-request/two-seat metadata sample, not observed permission outcomes. ALLOW means only that the recorded target spelling is declared under explicit v2 authority; it never proves body behavior, effects, reading or native prevention. Unknown edit shapes, including freeform patches, yield SCOPE-SCHEMA/exit2 (could-not-evaluate), never a clean result. Internal URIs denied by this audit mean “not a declared filesystem target”, not that a harness device is forbidden or refused.

For v2 edits the target is literal and selector-free. Existing v1 read/grep selector parsing remains unchanged for adapter reads, including `:raw:range`; it does not apply to edit targets. Each separately recorded frontend request and additional adapter start is audited independently; a clean frontend cannot clear another event. C3 implements the frozen old-v1 read grammar independently and never reads C1/C2 production content. Historical unknown-tool/path/exec findings stay red.

## Gate and probe registry — round23 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Existing rows retain their contracts. New selftests and actual measurements are recorded in `.ufo/waves/round-23/measure/`; selftest capability is distinct from a real measurement.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |



## Before lifting the host pacman pause — round 24

Authority: detection and report only, from `corpus/knowledge/pause-lift-gate-r24.md` (2026-10-22 capture `.ufo/waves/round-24/capture/l1-4/capture.txt`; counting command `python3 tools/check-pause-gate.py --revision <commit>`). Nothing here lets a lane run a pacman transaction, a database refresh, a cache clean, an image rebuild, a service restart or a boot. The operator alone decides package changes. Verdict words are the gate's premise verdicts (cleared, still-holds, changed, unverified), not the HEALTHY/DEGRADED/BLOCKED health words.

| Condition observed | Read-only command that observes it | Verdict on 2026-10-22 | Operator action | Entry pointer |
|---|---|---|---|---|
| P1: how far the host is from its upgrade target | `CHECKUPDATES_DB=/fast/scratch/<dir> checkupdates` (temporary database; host databases untouched), plus `pacman -Qu` for the local view | changed: 134 rows against the current snapshot (systemd 262.1, limine 12.9.4, ca-certificates-mozilla 3.131.1 security fix); 3 against the local databases; 413 is historical | Read the boot-chain rows and Arch News before deciding; a `-Qu` count alone is never the gap | gate entry P1 |
| P2: an installed package is newer than its sync entry | `pacman -Sl` joined with `vercmp` on every `[installed: ...]` row | cleared: none | Never install a single package with `-S` before a full upgrade; the host has been in the post `-Sy` state since 2026-10-21 20:32 | gate entry P2 |
| P3: a configured late hook still names `/new_root` under mkinitcpio 42 | `grep -n /new_root /usr/lib/initcpio/hooks/*`; `grep -n new_root /usr/lib/initcpio/functions`; `bash tools/boot-chain-audit.sh --live` | changed: the 42.2 symlink serves both hooks on ordinary boots; the read-only snapshot-boot overlay path is untested | Before relying on a snapshot boot for rollback, test one deliberately, or keep the 41.1 snapshot-1 entry | gate entry P3 |
| P4: the local databases are older than the mirror | `stat -c '%y %z %w %n' /var/lib/pacman/sync/*.db`; `curl -sI https://stable-mirror.omarchy.org/core/os/x86_64/core.db` | changed: mirror Last-Modified 2026-10-22 04:40 UTC, local files from 2026-10-18 | Measure the target with a temporary database; never refresh the host databases without upgrading | gate entry P4 |
| P5: a cache rollback exists | `find /var/cache/pacman/pkg -maxdepth 1 -name '*.pkg.tar*' \| wc -l`; sudo journal for `paccache -r` and `pacman -Scc` | changed: 0 package files; rollback only through the Arch Linux Archive or the 2026-10-20 Snapper snapshots | Take a Snapper pre-snapshot before any upgrade (the omarchy update does this); keep the Archive as the downgrade source | gate entry P5 |
| Error pattern: `pacman -Sy` without `-u` during a pause | `grep -F "[PACMAN] Running" /var/log/pacman.log \| grep -- " -Sy"` | observed 2026-10-21 20:32 -03 | Report the line; the repair is a full upgrade, decided by the operator | gate entry P2, P4 |

Recheck after any package transaction, database refresh, reboot or omarchy release: run `bash .ufo/waves/round-24/capture/capture.sh <new-empty-dir>`, update the gate JSON pointers and re-run the counting command.

## Gate and probe registry — round24 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every round23 row is retained verbatim, including its pinned values and its write scope; round24 adds the two round-24 claim instruments and changes no earlier row. A self-test flag is resolved against the committed tool source at the bound revision, not against this prose. Selftest capability is distinct from a real measurement.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |

## R24 current-use corrections after falsification

The historical 1password-beta downgrade-trap row at lines 386-388 is superseded: installed `8.12.42_34.BETA-1` is now behind channel `8.12.44_25.BETA-1` (capture `l1-4/capture.txt:40`). The historical empty `pacman -Qu` at line 99 and old database date at line 50 are not current readings. The candidate-upgrade framing at line 1658 and the round-15 current-use pointer at lines 1805-1814 predate the full upgrade of 2026-10-20 09:15 -03; the operative current-use entry is `corpus/knowledge/pause-lift-gate-r24.md`.

Corrections to the round-24 decision table:

- P1: 134 is the combined configured-repository set: 130 from the stable Arch snapshot and 4 from third-party repositories. `checkupdates` must not use `-d` (it would download packages); exit 2 means no updates. Use a private temporary database; never refresh the host databases for a count.
- P2: the exact read-only local-newer command is the `local-newer-than-sync` block of `.ufo/waves/round-24/capture/capture.sh`. A live re-capture requires explicit read-only authorization; a committed gate count does not grant it.
- P3: ordinary boots do not exercise btrfs-overlayfs, which exits early on the ordinary root. Only Plymouth reaching the real root is inferred from this boot; a snapshot boot remains unverified. A suggestion to retain snapshot 1 is supported by wave-1 `ExecRollbackPaths.md`, not by the P3 source table. Include `/etc/initcpio/hooks` and effective HOOKS when deciding whether a hook is configured. `boot-chain-audit.sh --live` uses privileged reads and requires separate read-only authorization.
- P5: the exact capture commands are the `cache-package-files`, `paccache-runs-since-pause` and `pacman-commands-since-pause` blocks of `capture.sh`. The host pacman pause overrides the generic package-install tooling directive.
- The error-pattern command above also matches full upgrades. Inspect only the pause window and tokenized flags: `awk '$1 >= "[2026-10-20T09:40"' /var/log/pacman.log` followed by the `[PACMAN] Running` filter, then `grep -E -- " -S[^ u']*y[^ u']*[ ']"`. It returns the single bare-sync event, not `-Syu`.

recheck: `python3 tools/check-pause-gate.py --revision <commit>` checks committed evidence links only. Host re-capture, including the read-only package queries and temporary-database refresh, needs an explicit grant; this table never grants package, service, configuration or boot writes.

Final round-24 safety correction: P3's combined hook verdict is **unverified**, not changed. Ordinary-root Plymouth evidence does not test the read-only snapshot overlay branch. The original five-premise target is retained and the checker counts four. This supersedes the P3 table verdict above; the pause is not cleared. Recheck remains committed-evidence-only unless live reads are explicitly authorized.

## Memory pressure and systemd-oomd — round 25

Authority: detection and report only, from `corpus/knowledge/memory-pressure-r25.md` (2026-10-22 capture `.ufo/waves/round-25/capture/capture.txt`, sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`; counting command `python3 tools/check-memory-pressure.py --revision <REV>`). Nothing in this section enables a service, writes a unit drop-in or changes a threshold; enabling or tuning a userspace OOM killer stays operator-owned, and this lane never writes `/etc` or a unit file. The verdict words here are the reading rules' own premise verdicts (`verified`, `scoped`, `unverified`), not the HEALTHY/DEGRADED/BLOCKED plane words.

Thresholds appear only where an opened source states them, for the installed systemd 262 (`systemd 262 (262-1-arch)`, capture line 9) and the running kernel 7.2.11-arch1-1 (capture line 6): a memory-pressure limit of 60 percent (`DefaultMemoryPressureLimit=`), a pressure duration of 30 s (`DefaultMemoryPressureDurationSec=`), a swap-use limit of 90 percent (`SwapUsedLimit=`), from systemd v262 `oomd.conf(5)`, raw bytes sha256 `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`; and a memory-pressure watch threshold of 200 ms (`MemoryPressureThresholdSec=`, defaulting through `DefaultMemoryPressureThresholdSec=`), from systemd v262 `systemd.resource-control(5)` sha256 `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8` and systemd v262 `systemd-system.conf(5)` sha256 `161359987affadc8e4a533bc9117bbbd98053cb807808b623eb24794b49b0c58`. No other numeric threshold is asserted here; a percentage that no opened source gives is not written down.

Sources opened for this round and cited by the rows below: Linux v7.2 `Documentation/accounting/psi.rst` (sha256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`), Linux v7.2 `Documentation/admin-guide/cgroup-v2.rst` (sha256 `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`), systemd v262 `man/oomd.conf.xml`, `man/systemd.resource-control.xml`, `man/systemd-oomd.service.xml` and `man/systemd-system.conf.xml`. The `SOURCES` id for each is assigned by the L1 in `corpus/SOURCES.md` (next free id S115); the rows below name the document and its sha256 so a reader can bind the id without trusting this prose. The generic PSI semantics are also held by the sibling lane mori (`mori-shokunin@4f05dd5a:corpus/knowledge/system-pressure-r24.md`); they are cited here, not absorbed, and fleet or wave attribution of a pressure reading stays with mori under `PROVINCE.md` row ADJ-04.

| id | observation | read-only command | verdict | action | entry pointer |
|---|---|---|---|---|---|
| MP1 | systemd-oomd's memory-pressure limit reads the share of time in a 10 second window in which all tasks of the control group were delayed, that is the `full` line of the memory PSI file; the `some` line is the share of time in which at least some tasks were stalled. The generic definitions of `some` and `full` are held by the sibling lane mori (`mori-shokunin@4f05dd5a:corpus/knowledge/system-pressure-r24.md`), and the `full` reading for the oomd rule is held by systemd v262 `oomd.conf(5)`. | `cat /proc/pressure/memory` | verified — capture line 15 (token `total=40856373`), the `full` line of the first read, and capture line 14 (token `total=41385384`), the `some` line of the same read; both lines are unique in the capture | Read `full` and `some` together before quoting either: a `some` value with a much lower `full` value is partial stall, not thrashing, and only the `full` share is the number the oomd rule consumes | entry row MP1 in `corpus/knowledge/memory-pressure-r25.md`; sources Linux v7.2 `Documentation/accounting/psi.rst` sha256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` and systemd v262 `man/oomd.conf.xml` sha256 `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`; sibling fact cited, not absorbed, under `PROVINCE.md` row ADJ-04 |
| MP2 | The `total` field of a memory PSI line is cumulative absolute stall time in microseconds, so one read never dates an incident and a dated reading needs two reads and a difference. systemd-oomd's own rule is not a difference of totals: it is a sustained-limit rule, so a stall that ends inside the 30 s default duration never reaches the oomd action even though a difference of totals would show it. | `cat /proc/pressure/memory`; `sleep 10`; `cat /proc/pressure/memory` (the capture's own sequence, capture lines 13 to 22) | verified — capture line 14 (token `total=41385384`) is the counted pointer, the first read; the second read is capture line 21 and its text is identical to capture line 29, so it is cited by line number only | Take two reads with a known gap and subtract: `some` 41389485 minus 41385384 is 4101 µs and `full` 40860452 minus 40856373 is 4079 µs across the 10 s sleep of capture line 17; a zero difference is not proof of no stall, because the root cgroup's `cgroup.pressure` switch can stop `psi_system` accounting while `/proc/pressure/*` stays readable (mori limit, cited not absorbed) | entry row MP2 in `corpus/knowledge/memory-pressure-r25.md`; source Linux v7.2 `Documentation/accounting/psi.rst` sha256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`; sibling fact cited, not absorbed, under `PROVINCE.md` row ADJ-04 |
| MP3 | systemd-oomd watches the `memory.pressure` file of the cgroups it monitors, not `/proc/pressure/memory`, and every cgroup exposes that file in the same format. The root cgroup's file is the system group itself, so root equals `/proc/pressure/memory` by identity and never as a sum of children; a system-scope read says nothing about a non-root cgroup, and a parent total is not the sum of its children. | `cat /sys/fs/cgroup/memory.pressure`; `cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/memory.pressure` | verified — capture line 38 (token `3158801`) is the `some` line of `user-1000.slice`, capture line 42 (token `3161820`) is the `some` line of `user@1000.service` and capture line 34 (token `3150158`) is the `some` line of `user.slice`; the root file at capture lines 29 and 30 repeats the second system read, so the root identity is cited by line number and by kernel source | Name the cgroup whose pressure is being read before quoting it; never compare a parent total with a child total taken from sequential reads, because time passes between the reads and a child can legitimately exceed its parent | entry row MP3 in `corpus/knowledge/memory-pressure-r25.md`; sources Linux v7.2 `Documentation/accounting/psi.rst` sha256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` and Linux v7.2 `Documentation/admin-guide/cgroup-v2.rst` sha256 `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`; sibling fact cited, not absorbed, under `PROVINCE.md` row ADJ-04 |
| MP4 | `ManagedOOMMemoryPressure=` and `ManagedOOMSwap=` decide whether systemd-oomd may act on a unit's cgroup: `kill` makes the unit a candidate for monitoring and adds `After=` and `Wants=` on systemd-oomd.service, while `auto` means systemd-oomd "will not actively use this cgroup's data for monitoring and detection", and an `auto` unit becomes a candidate only when an ancestor is set to `kill`. On the four captured units every value is `auto`, and the whole ancestor chain up to `-.slice` is `auto`, so nothing in that chain is monitored. | `systemctl is-active systemd-oomd.service`; `systemctl is-enabled systemd-oomd.service`; `systemctl show -p ManagedOOMMemoryPressure -p ManagedOOMSwap -- user@1000.service`; the same `show` for `user-1000.slice`, `user.slice` and `-.slice` | scoped — capture line 73 (token `inactive`) is the counted pointer; the `auto` values are capture lines 112 and 113, 121 and 122, 130 and 131 and 139 and 140, each repeated four times and therefore cited by line number only; `is-enabled` reads `disabled` at capture lines 76 and 79 | systemd-oomd monitors nothing on this host as configured, and enabling the unit would still monitor nothing while every unit stays `auto`; setting `kill` or enabling the unit is an operator action outside this lane; and a unit outside the four captured ones was not read, so no host-wide statement is made | entry row MP4 in `corpus/knowledge/memory-pressure-r25.md`; sources systemd v262 `man/systemd.resource-control.xml` sha256 `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8` and systemd v262 `man/systemd-oomd.service.xml` sha256 `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d`; the empty `OOMRules=` read on the same four units is in the supplementary capture `.ufo/waves/round-25/capture/capture-earlyoom.txt` sha256 `7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309` |
| MP5 | For the installed systemd 262 the oomd defaults are a memory-pressure limit of 60 percent, a pressure duration of 30 s and a swap-use limit of 90 percent. The swap rule fires only when the fraction of memory used and the fraction of swap used are both above the limit, and the candidate cgroup must hold more than 5 percent of total swap. A unit's `ManagedOOMMemoryPressureLimit=0` means use the default, and it is ignored unless that unit is `kill`. | `systemd-analyze cat-config systemd/oomd.conf` | verified — capture line 107 (token `DefaultMemoryPressureLimit=60%`), capture line 108 (token `DefaultMemoryPressureDurationSec=30s`) and capture line 106 (token `SwapUsedLimit=90%`) carry the three shipped commented defaults; the active-line count at capture line 83 is 1, which is the `[OOM]` section header alone, so no local key is set | Read the three commented keys as the effective defaults for this host; never read the 90 percent rule as a swap-only rule, and never read `ManagedOOMMemoryPressureLimit=0` as a zero-percent limit | entry row MP5 in `corpus/knowledge/memory-pressure-r25.md`; source systemd v262 `man/oomd.conf.xml` sha256 `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`; the installed file is the package's shipped default, unmodified (`pacman -Qkk systemd` reports no line for it) |
| MP6 | Kernel OOM-kill evidence and pressure-stall evidence are two separate readings: the kernel raises `count_vm_event(OOM_KILL)` and `memcg_memory_event_mm(mm, MEMCG_OOM_KILL)` in the kill path, while stall time is accumulated by the PSI accounting in a different file, and a userspace killer's SIGKILL moves neither counter. The kernel counter therefore reads zero even when a userspace killer has killed something. | `grep -E '^oom_kill ' /proc/vmstat`; `cat /sys/fs/cgroup/user.slice/user-1000.slice/memory.events` | scoped — capture line 52 (token `oom_group_kill`) is the counted pointer of the cgroup `memory.events`; the `/proc/vmstat` value at capture line 62 is text-identical to capture line 51, so it is cited by line number only, and it is a since-boot counter that this capture does not date | Read the kernel counter and the stall counter separately and never read one as the other; this capture never read earlyoom, so no claim is made that nothing watches memory before the kernel: the supplementary read-only capture `.ufo/waves/round-25/capture/capture-earlyoom.txt` sha256 `7adbe069326afaaa103c447b95d507e989503356c864d9726edc45381fd40309` shows `earlyoom.service` active and enabled, and an earlyoom kill would not move the kernel counters | entry row MP6 in `corpus/knowledge/memory-pressure-r25.md`; source Linux v7.2 `mm/oom_kill.c` sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` and Linux v7.2 `Documentation/admin-guide/cgroup-v2.rst` sha256 `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad`; sibling fact cited, not absorbed, under `PROVINCE.md` row ADJ-04 |

[R29-OWED-O05] verdict: qualified | original: "so nothing in that chain is monitored" | now: No ManagedOOM candidate exists in the four-unit auto chain, but units with OOMRules= are also monitored, and an active systemd-oomd.socket can accept local-account cgroup reports. | basis: corpus/knowledge/memory-pressure-r25.md:387, corpus/knowledge/memory-pressure-r25.md:390

Recheck after any kernel, systemd or memory-controller change: run `bash .ufo/waves/round-25/capture/capture.sh <new-output-file>`, point the entry's capture pointers at the new capture, and re-run `python3 tools/check-memory-pressure.py --revision <commit>`. A live re-capture needs an explicit read-only authorization; a committed gate count does not grant it.

## Gate and probe registry — round25 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every round24 row is retained verbatim, including its pinned values and its write scope; round25 adds the two round-25 claim instruments and changes no earlier row. A self-test flag is resolved against the committed tool source at the bound revision, not against this prose. Selftest capability is distinct from a real measurement.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 23 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R25 fixed check set K01 to K23 read at the bound revision; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |

## Storage integrity — round 26

Authority: detection and report only. Normative detail, quotes and sources: `corpus/knowledge/storage-health-r26.md` and `.json` (capture `.ufo/waves/round-26/capture/capture.txt`, sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd`). This lane never starts a scrub, never runs `btrfs device stats -z`, never enables `btrfs-scrub@.timer`, never changes a profile and never touches the LUKS mapping; those are operator actions. Privileged reads are the read-only set `sudo -n btrfs device stats <mountpoint>` (no `-z`), `sudo -n btrfs scrub status <mountpoint>`, `sudo -n smartctl -H -A <device>` (no `-i`, `-t`, `-s`, `-X`) and `sudo -n nvme smart-log <device>`; the sysfs counters, profiles and timer state need no privilege.

| id | signal and read-only command | how to read it | host reading at capture (verdict) | operator action |
|---|---|---|---|---|
| SH1 | `cat /sys/fs/btrfs/<fsid>/devinfo/<devid>/error_stats`; `sudo -n btrfs device stats /` | Five lifetime counters: write, read, flush (failed FLUSH writes), corruption (checksum mismatch or bad metadata header), generation (stale block). sysfs and the ioctl show the same counters under different names. | One device (devid 1, /dev/mapper/root). All five counters are 0 in sysfs (capture lines 40-44) and through the ioctl (lines 112-116). (`HEALTHY`) | None. Read the counters with `cat /sys/fs/btrfs/<fsid>/devinfo/<devid>/error_stats` (no privilege needed) or `btrfs device stats <mountpoint>`; never add -z, which zeroes them and destroys the history. |
| SH2 | `sudo -n journalctl --no-pager -o short-iso _TRANSPORT=kernel --grep 'BTRFS.*errs: wr'` over retained boots | A non-zero counter is a stored total, not an event. Date errors only from error-level `bdev ... errs:` kernel lines; the same text at info level at mount just reprints the stored total. | Counters are 0, so no mount-time line is printed; 0 `errs: wr` lines and 0 BTRFS error, critical, warning or forced-readonly lines over 6 retained boots (capture lines 154-161). Persistence across mounts cannot be observed on all-zero counters; it rests on the source. (`HEALTHY`) | When a counter is non-zero, search the kernel journal of every retained boot for error-level `errs:` lines to date the errors; treat an info-level mount-time line as the stored total, not a new incident. Resetting counters stays an operator decision. |
| SH3 | `ls /sys/fs/btrfs/<fsid>/allocation/{data,metadata,system}` (profile directory name) | Scrub repairs only by copying a verified good replica. `single` data: a checksum error is found but is uncorrectable. `dup` metadata: repairable from the second copy, which an SSD may store as one physical copy. NOCOW file data (systemd journals) has no checksums and is not verified. | Data profile single (capture line 64); metadata and system profiles dup (`btrfs filesystem df` and sysfs allocation directories); one NVMe SSD under LUKS. (`DEGRADED`) | Read this as limited self-repair, not a fault: a data checksum error on this host can be found but not fixed from a replica, so backups are the repair path for file data. Changing the data profile is an operator decision and is not proposed here. |
| SH4 | `sudo -n btrfs scrub status /`; `systemctl is-enabled btrfs-scrub@-.timer` | No `scrub.status.<UUID>` under `/var/lib/btrfs` and `no stats available` mean no scrub record, not a clean scrub; ignore the `no errors found` line printed beside it. | `no stats available` (capture line 121); `/var/lib/btrfs` absent (line 127); `btrfs-scrub@-.timer` disabled (line 131) and inactive (line 134). The `Error summary: no errors found` line printed beside `no stats available` is not a health reading. (`UNVERIFIED`) | Operator decision: run `btrfs scrub start /` once or enable `btrfs-scrub@-.timer`; the lane never starts a scrub or enables a timer. After a scrub, read `btrfs scrub status /` for csum, verify, read and super errors and the corrected versus uncorrectable split. |
| SH5 | `sudo -n smartctl -H -A /dev/nvme0n1` | smartctl prints PASSED exactly when the Critical Warning byte is 0. Spare below threshold reaches it only as bit 0x01; Percentage Used and media errors are printed but never decide it. | PASSED with Critical Warning 0x00 (capture lines 181, 184); Available Spare 100% against threshold 10%, Percentage Used 2%, Media and Data Integrity Errors 0 (lines 186-188, 197). (`HEALTHY`) | Read the Critical Warning byte and the other fields separately: a PASSED result does not mean wear or media errors were judged. Watch Percentage Used, spare against threshold and media errors as their own signals with `sudo smartctl -H -A <device>` (read-only; never -t, -s or -X). |
| SH6 | `sudo -n smartctl -H -A /dev/nvme0n1`; `sudo -n nvme smart-log /dev/nvme0` | Power Cycles, Unexpected Power Losses (labelled Unsafe Shutdowns), media errors and error-log entries are lifetime counts; compare two dated reads, and date abrupt boot ends from the journal, not from this counter. | Power Cycles 325, Unsafe Shutdowns 200, Media and Data Integrity Errors 0, Error Information Log Entries 0 (capture lines 194, 196-198; nvme-cli agrees at lines 221, 223-225). Only six boots are retained in the journal, so most of the 200 cannot be dated. (`HEALTHY`) | Compare two dated reads to see whether the count grew in a window; correlate growth with the journal's boot list before naming a cause. A high lifetime ratio alone is not a fault; report it to the operator as context. |

### Error patterns — storage integrity (round 26)

- **SE1 — kernel device error line.** An error-level kernel line `BTRFS error (device ...): bdev ... errs: wr N, rd N, flush N, corrupt N, gen N`. It dates a counted error; record the whole line and its boot, then read SH1. The same text at info level at mount is the stored total (SH2). Round-26 capture: 0 such lines over 6 retained boots.
- **SE2 — forced readonly.** A kernel line containing `forced readonly`: btrfs stopped writing after an error. Record the line and boot; never remount read-write; report to the operator.
- **SE3 — NVMe health failure.** `SMART overall-health self-assessment test result: FAILED!` or a `Critical Warning:` byte other than `0x00`. Record the byte and the reason lines smartctl prints under it, then read SH6 and SH1. Media errors are a replacement question for the operator, never something to scrub around.
- **SE4 — false clean.** `Error summary: no errors found` printed with `no stats available`: no scrub has run; this is `UNVERIFIED`, not `HEALTHY` (SH4).

## Gate and probe registry — round26 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every
round25 row is retained verbatim, including its pinned values and its write scope, except the
two cells of the `self-assessment` row named below; round26 adds the storage-health claim
instrument. A self-test flag is resolved against the committed tool source at the bound revision,
not against this prose. Selftest capability is distinct from a real measurement.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |

Round-26 wave-2 note on the storage section above (appended 2026-10-22): in SE2 "never remount read-write" and in SE3 "a replacement question for the operator" are operator guidance, not statements of an admitted source; treat them as the lane's caution, marked [inference]. The entry's `UNVERIFIED` verdict and its `DEGRADED` meaning are defined in `corpus/knowledge/storage-health-r26.json` (`verdict_vocabulary`) and do not change the census plane verdicts.
Round-26 wave-2 note on row SH6 of the storage table above: the Unexpected Power Losses trigger has a second branch and the verdict for that count is `UNVERIFIED`, not `HEALTHY`; the journal dates boot ends, not abruptness; bind a device by a stable identity, not by `nvme0`. The corrections are in `corpus/knowledge/storage-health-r26.md` section "Wave-2 corrections".

## Kernel taint — round 27

Authority: detection and report only. Normative detail, quotes and sources: `corpus/knowledge/kernel-taint-r27.md` and `.json` (capture `.ufo/waves/round-27/capture/capture.txt`, sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`; sources S140 to S145, Linux v7.2). No row authorises loading, unloading or signing a module, enrolling a key or writing a sysctl.

| id | signal and read-only command | how to read it | host reading at capture (verdict) | operator action |
|---|---|---|---|---|
| KT1 | `cat /proc/sys/kernel/tainted` | Decimal taint mask; 0 is untainted; each set bit is one reason (S140 table). 4096 = O (bit 12), 8192 = E (bit 13) | 12288 = O + E only; no W, D or L this boot (HEALTHY) | Expect 12288 while the nvidia DKMS modules are loaded; any other bit is a new event to look up, and W, D or L sends you to `journalctl -k -b 0` |
| KT2 | `journalctl -k -b 0 --grep 'out-of-tree'` | O is set at load when a module lacks the `intree` modinfo tag; the message prints once, for the first such module (S143) | nvidia at 17.5 s of boot 0 (HEALTHY) | None for the nvidia DKMS set; an O on any other module is a finding |
| KT3 | `cat /sys/module/module/parameters/sig_enforce`; `modinfo -F signer nvidia`; `journalctl -k -b 0 --grep 'verification failed'` | E means the kernel did not accept the module signature; in permissive mode a module whose key is unavailable loads and taints (S144, S145). A named signer is not a trusted key | sig_enforce N, CONFIG_MODULE_SIG_FORCE off, signer "DKMS module signing key", E set (UNVERIFIED: the kernel has not verified these modules) | Report it; E is expected every boot as configured. Never read the DKMS private key. Before enabling `module.sig_enforce=1` or a signature-enforcing lockdown, expect nvidia to be refused at load unless the kernel trusts its key |
| KT4 | `for f in /sys/module/*/taint; do t=$(cat $f); [ -n "$t" ] && echo ${f%/taint} $t; done` | Per-module taint letters, read-only (S143); names the culprit the number cannot | nvidia, nvidia_drm, nvidia_modeset, nvidia_uvm = OE; files in `updates/dkms/`, owned by no package (HEALTHY) | After a kernel or driver update compare the loaded module version with nvidia-open-dkms and nvidia-utils; pacman checks cannot see a stale DKMS build |
| KT5 | compare two readings of `/proc/sys/kernel/tainted` in one boot | Taint is never cleared while the kernel runs: unloading does not clear it and a sysctl write only adds bits (S140, S141) | O and E set since 17.5 s of boot 0 (HEALTHY) | Do not unload modules or write the sysctl to "clear" taint; a value that grows within a boot is a new event |
| KT6 | the `Tainted:` field of the `CPU:` line in an oops | Reports from tainted kernels are often ignored upstream; reproduce with an untainted kernel (S140) | every boot that loads nvidia shows O and E (HEALTHY; reporting limit only) | For an upstream kernel report, reproduce in a boot without the nvidia modules (operator decision) and report that log |

| Error pattern (kernel journal, exact text) | Meaning | Action |
|---|---|---|
| `nvidia: loading out-of-tree module taints kernel.` | KT2: first out-of-tree module of the boot set O | expected on this host; no action |
| `nvidia: module verification failed: signature and/or required key missing - tainting kernel` | KT3: the signature was not accepted (unsigned, unsupported crypto, or key not available) and enforcement is off, so the module loaded and set E | expected on this host; it is not a load failure. A `Loading of ... is rejected` line instead would mean enforcement is on and the module did not load |

## Gate and probe registry — round27 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every
round26 row is retained verbatim except the pinned-values cell of the `self-assessment` row,
which now names the round-27 QUALITY 65 change; round27 adds the two claim instruments
`kernel-taint` (C1) and `adjacency-overlap` (C2), whose rows were missing when they landed
(`check-registry-coverage.py` read FAIL, 2 missing, at `099c7b3f`; wave-2 CritAxisHarm). A
self-test flag is resolved against the committed tool source at the bound revision, not
against this prose. Selftest capability is distinct from a real measurement.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement (round-27 wave-2 CritC2Tool and MutC2Counter list the rule gaps) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |

Round-27 wave-2 notes on the kernel-taint section above (appended 2026-10-22, attempt 2; the corrections of record are in `corpus/knowledge/kernel-taint-r27.md` section "Wave-2 corrections" and the JSON `corrections_r27_a2`):

- KT1: bit 7 (D) means the kernel died recently from an oops or a BUG (S140 lines 92 and 159), not only an oops (wave-2 RevRowKT1).
- KT4: the culprit loop prints `No such file or directory` for every built-in module without a `taint` attribute and exits 1; skip absent files: `for f in /sys/module/*/taint; do [ -e "$f" ] || continue; t=$(cat "$f"); [ -n "$t" ] && echo "${f%/taint} $t"; done` (wave-2 RevSkillKernelTaint, output identical, exit 0).
- Driver and firmware row of the health-verdict table (`SKILL.md` line 49, "taint OOT + unsigned"): read E as "signature not accepted by the kernel" (KT3), not as "no signature"; the four nvidia modules carry a DKMS signature (capture, `modinfo -F signer`). The appended note in `corpus/knowledge/driver-firmware-plane.md` covers that note's lines 160 and 202; this note covers the SKILL row (wave-2 CritC1Learning).

## Gate and probe registry — round28 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every
round27 row is retained verbatim except the pinned-values cells of `kernel-taint` and
`adjacency-overlap`, which name their round-28 tightenings; round28 adds the two should-fail
batteries that measure claims C1 and C2 (QUALITY 70: a tool lands with its row). A self-test
flag is resolved against the committed tool source at the bound revision, not against this
prose. Selftest capability is distinct from a real measurement.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |

## Kernel OOM victim selection — round 29

- **Rule** (S149 `mm/oom_kill.c:228-236`): one scalar per task, `points = rss + swapents + pgtables` in pages `+ oom_score_adj × ⌊totalpages/1000⌋`; `select_bad_process` keeps the strict maximum in task-list order and an equal score replaces the earlier pick (`:339-341`, `:362-375`). One adj unit is 0.1 % of allowed memory, i.e. exactly one point on the 0-1000 badness scale (S148 `proc.rst:1761-1766`, `:1777-1783`).
- **totalpages** (S149 `:258`, `:263`): `totalram_pages() + total_swap_pages` for a global OOM, `mem_cgroup_get_max()` for a memcg OOM. Event-A host sum is 16,909,739 pages, so one adj unit is 16,909 pages (66.05 MiB); `-1000` is not a low score but removal from candidacy (`:216-222`, S148 `proc.rst:1781-1783`).
- **Decision table**:

| trigger | totalpages used | effect of the control |
|---|---|---|
| global OOM | 16,909,739 pages at event A; at event B unknown, because its swap total is unrecorded (15,861,169 today) | −1000 excluded; 0 no offset; +200 adds 3,381,800 pages (12.90 GiB) |
| memcg OOM | the memcg's `memory.max` + `swap.max`; all `max` on this host's path, so the trigger is closed | same formula at that smaller max; `memory.oom.group=1` would kill the whole cgroup (`:1040-1052`), it is 0 here |
| `oom_kill_allocating_task=1` (S150 `vm.rst:810-817`) | not consulted | kills `current` with no score at all, global path only, skipped when adj is −1000 (`:1145-1152`) |

- **Row F7 check** (`SKILL.md:1094`): the argument holds as a magnitude condition, not as a class order. A +100 manager beats a +200 app only if it holds 1,690,900 pages (6.45 GiB) more `rss+swapents+pgtables`, and 3,381,800 pages (12.9 GiB) more than each +300 Chromium; event B's per-process sizes are unmeasured (F5), so the no-kernel-kill conclusion rests on F1's `oom_kill` ledger, not on the adj class.

## Gate and probe registry — round29 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every
round28 row is retained verbatim and round29 appends the two measurement tools of claims C1
and C2 (QUALITY 70: a tool lands with its row; round-29 seat ScribeRegistryRows). The heading
keeps the exact form `## Gate and probe registry — round29 superseding current rows`: a bare
`## Gate and probe registry — round29` heading is not selected by the coverage gate, round28
stays operative and both new tools report REGISTRY-ROW-MISSING. A self-test flag is resolved
against the committed tool source at the bound revision, not against this prose; neither
round-29 tool has a self-test mode, so a real run is the only measurement.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, inherited GIT_* removed); no writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |

## Btrfs space allocation and ENOSPC — round 30

Knowledge entry: `corpus/knowledge/btrfs-space-r30.md` with companion `corpus/knowledge/btrfs-space-r30.json` (rows D01 to D10, counted by `python3 tools/check-btrfs-space-r30.py --revision <REV>`). Read-only capture: `.ufo/waves/round-30/w1/ExecHostCapture/btrfs-allocation-capture.txt` (2026-10-22T21:16:37Z). Disk runway and its thresholds stay mori's (mori `SKILL.md:415-418` at `05db57ed`: never threshold the btrfs chunk percent); this section covers the ENOSPC mechanism and repair decisions only. Every repair below is an operator write; the lane runs none of them.

| Row | Reading | Decision | Source |
|---|---|---|---|
| [R30-D01] | `Device unallocated` in `btrfs filesystem usage -b /` near 0: metadata reservations stay inside the allocated metadata chunks, so ENOSPC can come while data chunks have room | Read `Device unallocated` before `df`; near 0 with full metadata is the btrfs ENOSPC-with-free-space case | S159 line 177 |
| [R30-D02] | `Global reserve` is metadata held for emergency work such as deletion on a full filesystem; capped at 512 MiB in v7.2 | Never count it as free space; `used` above 0 means the emergency reserve is in use `[inf]`: treat the filesystem as full | S152 line 418; S156 line 394 |
| [R30-D03] | `btrfs balance start -dusage=N` relocates only block groups under N percent used and returns them to unallocated space | Operator only: start with `-dusage=0`, which needs no new work space, then raise N | S153 lines 50-54 |
| [R30-D04] | Metadata on one device defaults to `DUP`: every metadata byte costs two raw bytes (`Metadata ratio` 2.00 here) | Budget metadata chunks at twice their logical size | S155 lines 59 and 520; `btrfs-filesystem-usage.out.txt` line 11; capture lines 53 and 67 |
| [R30-D05] | `allocation/<type>/bg_reclaim_threshold` is a percentage of block-group size: the v7.2 periodic sweep reclaims a whole block group whose used bytes fall below it (the chapter calls it a reclaimable-space percentage; corrected after wave-2 RevRowD05) | Read only; metadata reads 0 on this host with `dynamic_reclaim` 0, so the periodic sweep marks no metadata block group (`[inf]`; other reclaim paths `[unk]`) | S154 lines 168-169; S159 lines 2111-2117 and 2154-2155 |
| [R30-D06] | `/sys/fs/btrfs/<fsid>/allocation/` (singular on 7.2.11; the v7.1 chapter heading spells `allocations`) holds `global_rsv_*` and the data, metadata and system directories, world-readable | Use these files for an unprivileged capture; `btrfs filesystem usage` without root lacks chunk detail | S158 lines 37, 68-78 and 1066-1068; S154 line 140; `.ufo/waves/round-30/w1/ExecHostCapture/btrfs-filesystem-usage.err.txt` line 1 |
| [R30-D07] | Snapshots share extents with their source, so deleting files in the original frees nothing a snapshot still references | Deleting the snapshots that still reference the extents is what returns the space; deleting files alone cannot. Which snapshots to delete is an operator decision (this host had no snapper configuration on 2026-10-22, wave-2 RevRowD07) | S157 lines 39-41 and 202-206 |
| [R30-D08] | Host metadata `bytes_used` 35372056576 of `total_bytes` 38654705664 (91.5 percent) | High fill alone is not ENOSPC while unallocated space remains (D01, D09) | S154 line 163; capture lines 50, 67 and 99 |
| [R30-D09] | Host unallocated 690922455040 bytes (device minus data, metadata and system `disk_total`) | New metadata chunks could still be allocated at capture time; no action | S152 line 398; capture line 98 |
| [R30-D10] | Host `global_rsv_size` 536870912, equal to `global_rsv_reserved` | The reserve sat at the 512 MiB cap, full and unused | S158 line 679; capture line 44 |

Error patterns: `No space left on device` from a btrfs path while `df -h` shows free space points at metadata chunks plus zero unallocated (D01); a balance that itself fails with ENOSPC needs `-dusage=0` first or freed snapshots (D03, D07).


## Gate and probe registry — round30 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every round29 row
is retained verbatim and round30 appends the measurement tools of claims C1 and C2, the C1 battery and
the receipt runner (QUALITY 70: a tool lands with its row). The heading keeps the exact form
`## Gate and probe registry — round30 superseding current rows`. The round-30 git-environment fixes to
eleven existing tools change no row: their entry commands and verdict maps are unchanged.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, inherited GIT_* removed); no writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |
| btrfs-space-r30 | gate | `python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]` | 0 all ten rows D01 to D10 verified;1 one or more row unverified;2 could-not-evaluate (revision or base registry unreadable) | none: no self-test mode; fixture mode `--tree <DIR> --base-sources <FILE>` is exercised by the battery `mutants-btrfs-space-r30` | R30 C1: ten frozen questions D01 to D10 with frozen tokens, base `fbfec6bd`, rules R1 to R9; declared version 1 sha256 `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (commit `8fb2cef0`), version 2 after the wave-1 attacks | committed reads only | tsukuroi |
| btrfs-space-battery | probe | `python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]` | 0 control 10, no should-fail shape accepted and no should-pass shape refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `btrfs-space-r30`; its counts are re-derived by wave seats | R30 C1 (QUALITY 73): synthetic fixture, 72 should-fail and 11 should-pass shapes in version 2 (46 and 6 at the declaration) | private temporary directory; no git | tsukuroi |
| git-env-residual | probe | `python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness error;1 a pair leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R30 C2: eleven frozen git-writing tools, channels path-wrapper, user-files and enclosing-repo (33 pairs); probe sha256 `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| run-receipt | probe | `python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE> [--lane <repo>] [--timeout <s>] -- <tool> [args...]` | 0 the tool exited 0;1 the tool exited 1 (its own verdict);2 revision or tool unreadable, or the tool's own could-not-evaluate | none: no self-test mode; the receipt header (revision, tool revision, tool sha256) is the evidence | R30 routed defect 1 (QUALITY 77): runs a tracked tool from a sandbox clone at the tool revision with a private HOME and writes header, stdout and footer | the `--out` receipt file; sandbox clone under `/fast/scratch/hyaku` | tsukuroi |
| report-receipts | gate | `python3 tools/check-report-receipts.py --report <PATH> --lane <repo> --revision <REV>` | 0 every revision-cited gate or measurement has a committed receipt;1 one or more citation unreceipted;2 could-not-evaluate (report or revision unreadable) | `python3 tools/check-report-receipts.py --selftest` | R30 mined mistake R30-UNRECEIPTED-GATES (QUALITY 77): exits 1 on the round-29 report at lane `8976ca92` (Gates at `434a7903`) | committed reads; selftest private fixtures | tsukuroi |
| owed-statements-v4shapes-battery | probe | `python3 tools/mutants-owed-statements-r29-v4shapes.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--keep]` | 0 control 12, no routed v4 shape accepted, no control refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R30 routed defect 2 of the round-29 spot-check: closed-comment, list-indented, extra-JSON-key and asterisk-id shapes; counter v5 sha256 `6fadf5fbb77579a8a49db36a560de20b20aa2bd3d3f6928218c640b1465c475b` refuses 11 of 11 (v4 `3516d579…` accepted 11 of 11) | private clone under `/fast/scratch/hyaku` | tsukuroi |

## Btrfs repair and maintenance decisions — round 31

These decision lines summarize btrfs-progs v7.1 documentation on shared extents and defragmentation, zero-log and checker repair, mount options, device replacement, and trim (`Defragmentation.rst:24-27`; `btrfs-rescue.rst:123-152`; `btrfs-check.rst:12-18,29-33`; `ch-mount-options.rst:33-43,89-101,131-159`; `btrfs-replace.rst:20-38`; `Trim.rst:12-43`). They state documented behavior, not a diagnosis of a particular host [inf] (`btrfs-check.rst:12-18,29-33`). Mori's runway row names `df -P` for the fleet root and `/tmp`, and its explicit boundary says “Never threshold the btrfs chunk percent”; this tsukuroi section records repair and maintenance decisions only and sets no runway threshold [inf] (`mori-shokunin/SKILL.md:19,415-418`).

| id | situation | decision | source |
|---|---|---|---|
| [R31-Q01] | Files made by `cp --reflink` or existing on multiple snapshots. | Account for possible increased data-space consumption: defragmentation does not preserve extent sharing. | S164 line 24-27 |
| [R31-Q02] | A filesystem mount fails during log replay; the backtrace has open_ctree and names containing replay, recover, or log_tree. | Use zero-log to clear the log tree; the filesystem may mount normally again, but changes since the last transaction commit may be lost (up to 30 seconds at the default period, or less if other filesystem activity implied a commit). | S165 lines 126-152 |
| [R31-Q03] | Considering --repair for filesystem damage | Proceed only with advice from a developer or experienced user and after accepting that no fsck can successfully repair every corruption type. | S166 line 29-33 |
| [R31-Q04] | An operator is evaluating autodefrag for a large database workload. | Treat that workload as a potentially poor fit; autodefrag queues detected small random writes for defragmentation. | S167 lines 33-43 |
| [R31-Q05] | Choosing the periodic transaction commit interval. | Do not treat the >300-second warning as a hard limit: commit= defaults to 30 seconds, and values above 300 seconds produce a warning without an enforced upper bound. | S167 lines 89-96 |
| [R31-Q06] | Frequent-overwrite workload where in-place updates are relevant. | Weigh nodatacow's loss of copy-on-write, checksums, and compression against possible partial writes after interruption by a crash or device failure. | S167 lines 131-159 |
| [R31-Q07] | Planning `btrfs replace start` for a failing or missing device | For a live filesystem, replacement duplicates source data; for a source with many read errors, consider `-r` knowing access can be very slow. If the source is unavailable or `-r` is selected, data is built from RAID redundancy, and `-r` reads the source only if no other zero-defect mirror exists. Use devid for a disconnected source and choose a target the same size as or larger than the source. | S168 lines 20-33, 54-57 |
| [R31-Q08] | Choosing a trim mode on a btrfs SSD | Avoid discard=sync, which is not recommended; fstrim needs no mount option and is suitable as a periodic service, while discard=async tracks freed ranges and throttles the number of I/O requests. | S169 line 14-32 |

## Gate and probe registry — round31 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every round30 row
is retained verbatim and round31 appends the measurement tools of claims C1 and C2 (QUALITY 70: a tool
lands with its row). The heading keeps the exact form
`## Gate and probe registry — round31 superseding current rows`. The round-31 child-environment fixes to
eleven existing tools change no row: their entry commands and verdict maps are unchanged.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, inherited GIT_* removed); no writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |
| btrfs-space-r30 | gate | `python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]` | 0 all ten rows D01 to D10 verified;1 one or more row unverified;2 could-not-evaluate (revision or base registry unreadable) | none: no self-test mode; fixture mode `--tree <DIR> --base-sources <FILE>` is exercised by the battery `mutants-btrfs-space-r30` | R30 C1: ten frozen questions D01 to D10 with frozen tokens, base `fbfec6bd`, rules R1 to R9; declared version 1 sha256 `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (commit `8fb2cef0`), version 2 after the wave-1 attacks | committed reads only | tsukuroi |
| btrfs-space-battery | probe | `python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]` | 0 control 10, no should-fail shape accepted and no should-pass shape refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `btrfs-space-r30`; its counts are re-derived by wave seats | R30 C1 (QUALITY 73): synthetic fixture, 72 should-fail and 11 should-pass shapes in version 2 (46 and 6 at the declaration) | private temporary directory; no git | tsukuroi |
| git-env-residual | probe | `python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness error;1 a pair leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R30 C2: eleven frozen git-writing tools, channels path-wrapper, user-files and enclosing-repo (33 pairs); probe sha256 `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| run-receipt | probe | `python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE> [--lane <repo>] [--timeout <s>] -- <tool> [args...]` | 0 the tool exited 0;1 the tool exited 1 (its own verdict);2 revision or tool unreadable, or the tool's own could-not-evaluate | none: no self-test mode; the receipt header (revision, tool revision, tool sha256) is the evidence | R30 routed defect 1 (QUALITY 77): runs a tracked tool from a sandbox clone at the tool revision with a private HOME and writes header, stdout and footer | the `--out` receipt file; sandbox clone under `/fast/scratch/hyaku` | tsukuroi |
| report-receipts | gate | `python3 tools/check-report-receipts.py --report <PATH> --lane <repo> --revision <REV>` | 0 every revision-cited gate or measurement has a committed receipt;1 one or more citation unreceipted;2 could-not-evaluate (report or revision unreadable) | `python3 tools/check-report-receipts.py --selftest` | R30 mined mistake R30-UNRECEIPTED-GATES (QUALITY 77): exits 1 on the round-29 report at lane `8976ca92` (Gates at `434a7903`) | committed reads; selftest private fixtures | tsukuroi |
| owed-statements-v4shapes-battery | probe | `python3 tools/mutants-owed-statements-r29-v4shapes.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--keep]` | 0 control 12, no routed v4 shape accepted, no control refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R30 routed defect 2 of the round-29 spot-check: closed-comment, list-indented, extra-JSON-key and asterisk-id shapes; counter v5 sha256 `6fadf5fbb77579a8a49db36a560de20b20aa2bd3d3f6928218c640b1465c475b` refuses 11 of 11 (v4 `3516d579…` accepted 11 of 11) | private clone under `/fast/scratch/hyaku` | tsukuroi |
| btrfs-repair-r31 | gate | `python3 tools/check-btrfs-repair-r31.py --revision <REV> [--lane <repo>]` | 0 all eight Q01-Q08 rows new_sourced;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen Q01-Q08 question set is measured by the counter | R31 C1: frozen predicate new_sourced; rules R1-R8; six pinned btrfs-progs v7.1 documentation snapshot sha256 values | committed Git reads only | tsukuroi |
| git-child-env-r31 | probe | `python3 tools/probe-git-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness errors;1 one or more (tool, channel) pairs leak;2 harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R31 C2: eleven frozen tools and channels loader-env, child-contract and dotgit-pointer; parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |


## Round 32 — sibling handoff lines and the child-environment allow-list

Appended 2026-10-23 by round 32. Evidence: `corpus/lessons/round-32.md`; claims and measurements: `SCORECARD.md` round-32 sections.

| id | situation | decision | source |
|---|---|---|---|
| [R32-H1] | The oom plane counts n ≥ 1 dated kill-event clusters in its retained window; the census prints `HANDOFF ADJ-04 mori class=kill-events value=<n> kind=dated-event state=prepared window=… source=journal-window`. | Treat the line as a prepared packet for mori's fleet correlation (mori FR1), not as a delivered, acknowledged or accepted handoff; the oom plane keeps the OS finding. A cumulative counter (`vmstat oom_kill`, a `memory.events` flag) never prints this line. | S138 lines 1507-1508; PROVINCE.md ADJ-04 |
| [R32-H2] | The census's journal arm measured boot 0's error stream (boot target active) and counted m ≥ 1 systemd-coredump entries; the census prints `HANDOFF ADJ-04 mori class=coredumps value=<m> kind=dated-event state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER`. | Each counted entry is a journal record of one coredump event, which carries a crash time when systemd knows it (COREDUMP_TIMESTAMP is saved "if known"; a core file can outlive its journal entry); an absent line can also mean the journal arm did not run (inactive boot target). `value=` is the census's count over the merged journals, not mori's MESSAGE_ID count per scope, so quote both when they differ. Coredump classification is mori's (OUT-005). | S177 lines 41-46, 431-432 |
| [R32-E1] | One of the eleven probed lane tools or `tools/check-owed-statements-r29.py` starts a child process (git, python, bash); other lane tools still copy the ambient environment (`tools/_revision.py` `clean_env`, used directly by `check-adjacency-anchors.py`; `mutants-owed-statements-r29-v4shapes.py`) and are owed. | Build the child's environment from `CHILD_ENV_BASE = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}` plus the names that builder sets itself (git config contract, private HOME and XDG_CONFIG_HOME); copy no ambient name. Ambient HOME, TZ, TMPDIR, LANGUAGE and PATH are each a demonstrated channel (round-32 SentinelAllowKeep). Check: `python3 tools/probe-child-env-allowlist-r32.py --revision <REV>`. | S174 line 1; S175 lines 392-395; S176 line 18 |

## Gate and probe registry — round32 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every round31 row
is retained verbatim and round32 appends the two measurement tools of claims C1 and C2 (QUALITY 70: a tool
lands with its row). The heading keeps the exact form
`## Gate and probe registry — round32 superseding current rows`. The round-32 allow-list change to the
eleven tools and the census HANDOFF lines change no row's entry command or verdict map.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, children get the round-32 allow-list environment); one private temporary HOME directory created at module load and removed at exit (round 32, wave-2 CritNoHarm); no other writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |
| btrfs-space-r30 | gate | `python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]` | 0 all ten rows D01 to D10 verified;1 one or more row unverified;2 could-not-evaluate (revision or base registry unreadable) | none: no self-test mode; fixture mode `--tree <DIR> --base-sources <FILE>` is exercised by the battery `mutants-btrfs-space-r30` | R30 C1: ten frozen questions D01 to D10 with frozen tokens, base `fbfec6bd`, rules R1 to R9; declared version 1 sha256 `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (commit `8fb2cef0`), version 2 after the wave-1 attacks | committed reads only | tsukuroi |
| btrfs-space-battery | probe | `python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]` | 0 control 10, no should-fail shape accepted and no should-pass shape refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `btrfs-space-r30`; its counts are re-derived by wave seats | R30 C1 (QUALITY 73): synthetic fixture, 72 should-fail and 11 should-pass shapes in version 2 (46 and 6 at the declaration) | private temporary directory; no git | tsukuroi |
| git-env-residual | probe | `python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness error;1 a pair leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R30 C2: eleven frozen git-writing tools, channels path-wrapper, user-files and enclosing-repo (33 pairs); probe sha256 `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| run-receipt | probe | `python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE> [--lane <repo>] [--timeout <s>] -- <tool> [args...]` | 0 the tool exited 0;1 the tool exited 1 (its own verdict);2 revision or tool unreadable, or the tool's own could-not-evaluate | none: no self-test mode; the receipt header (revision, tool revision, tool sha256) is the evidence | R30 routed defect 1 (QUALITY 77): runs a tracked tool from a sandbox clone at the tool revision with a private HOME and writes header, stdout and footer | the `--out` receipt file; sandbox clone under `/fast/scratch/hyaku` | tsukuroi |
| report-receipts | gate | `python3 tools/check-report-receipts.py --report <PATH> --lane <repo> --revision <REV>` | 0 every revision-cited gate or measurement has a committed receipt;1 one or more citation unreceipted;2 could-not-evaluate (report or revision unreadable) | `python3 tools/check-report-receipts.py --selftest` | R30 mined mistake R30-UNRECEIPTED-GATES (QUALITY 77): exits 1 on the round-29 report at lane `8976ca92` (Gates at `434a7903`) | committed reads; selftest private fixtures | tsukuroi |
| owed-statements-v4shapes-battery | probe | `python3 tools/mutants-owed-statements-r29-v4shapes.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--keep]` | 0 control 12, no routed v4 shape accepted, no control refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R30 routed defect 2 of the round-29 spot-check: closed-comment, list-indented, extra-JSON-key and asterisk-id shapes; counter v5 sha256 `6fadf5fbb77579a8a49db36a560de20b20aa2bd3d3f6928218c640b1465c475b` refuses 11 of 11 (v4 `3516d579…` accepted 11 of 11) | private clone under `/fast/scratch/hyaku` | tsukuroi |
| btrfs-repair-r31 | gate | `python3 tools/check-btrfs-repair-r31.py --revision <REV> [--lane <repo>]` | 0 all eight Q01-Q08 rows new_sourced;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen Q01-Q08 question set is measured by the counter | R31 C1: frozen predicate new_sourced; rules R1-R8; six pinned btrfs-progs v7.1 documentation snapshot sha256 values | committed Git reads only | tsukuroi |
| git-child-env-r31 | probe | `python3 tools/probe-git-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness errors;1 one or more (tool, channel) pairs leak;2 harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R31 C2: eleven frozen tools and channels loader-env, child-contract and dotgit-pointer; parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| census-handoff-r32 | gate | `python3 tools/score-census-handoff-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--seed <hex>] [--scenarios N]` | 0 every fixture scenario routed and both live views consistent;1 one or more scenarios unrouted or a live view inconsistent;2 harness error (planted facts not visible in the base census, a non-hermetic run, or a vacuous live check) | none: no self-test mode; 24 seeded fixture scenarios plus two read-only live views are the measurement | R32 C1 v3: base census 58cc2e0b; HANDOFF ADJ-04 mori grammar `class= value= kind= state=`; scenario types none, kill-events, coredumps, both, cumulative-only, cumulative+coredumps, tsukuroi-only | private scratch under the system temp dir; reads the live host read-only | tsukuroi |
| child-env-allowlist-r32 | probe | `python3 tools/probe-child-env-allowlist-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leaking target and no harness errors;1 one or more targets leak an injected name or break parity;2 harness error | none: no self-test mode; the eleven-target control and ambient-names runs are the measurement | R32 C2 v2: eleven frozen tools; BASH_ENV, ENV, GCONV_PATH, PERL5OPT plus eight per-run random names (four of length 2-20, four of 21-200); parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku` | tsukuroi |

## Gate and probe registry — round33 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every round32 row
is retained verbatim and round33 appends the measurement probe of claim C1 (QUALITY 70: a tool lands
with its row). The round-33 allow-list change to `tools/_revision.py` `clean_env()` and to
`tools/mutants-owed-statements-r29-v4shapes.py` changes no row's entry command or verdict map.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, children get the round-32 allow-list environment); one private temporary HOME directory created at module load and removed at exit (round 32, wave-2 CritNoHarm); no other writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |
| btrfs-space-r30 | gate | `python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]` | 0 all ten rows D01 to D10 verified;1 one or more row unverified;2 could-not-evaluate (revision or base registry unreadable) | none: no self-test mode; fixture mode `--tree <DIR> --base-sources <FILE>` is exercised by the battery `mutants-btrfs-space-r30` | R30 C1: ten frozen questions D01 to D10 with frozen tokens, base `fbfec6bd`, rules R1 to R9; declared version 1 sha256 `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (commit `8fb2cef0`), version 2 after the wave-1 attacks | committed reads only | tsukuroi |
| btrfs-space-battery | probe | `python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]` | 0 control 10, no should-fail shape accepted and no should-pass shape refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `btrfs-space-r30`; its counts are re-derived by wave seats | R30 C1 (QUALITY 73): synthetic fixture, 72 should-fail and 11 should-pass shapes in version 2 (46 and 6 at the declaration) | private temporary directory; no git | tsukuroi |
| git-env-residual | probe | `python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness error;1 a pair leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R30 C2: eleven frozen git-writing tools, channels path-wrapper, user-files and enclosing-repo (33 pairs); probe sha256 `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| run-receipt | probe | `python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE> [--lane <repo>] [--timeout <s>] -- <tool> [args...]` | 0 the tool exited 0;1 the tool exited 1 (its own verdict);2 revision or tool unreadable, or the tool's own could-not-evaluate | none: no self-test mode; the receipt header (revision, tool revision, tool sha256) is the evidence | R30 routed defect 1 (QUALITY 77): runs a tracked tool from a sandbox clone at the tool revision with a private HOME and writes header, stdout and footer | the `--out` receipt file; sandbox clone under `/fast/scratch/hyaku` | tsukuroi |
| report-receipts | gate | `python3 tools/check-report-receipts.py --report <PATH> --lane <repo> --revision <REV>` | 0 every revision-cited gate or measurement has a committed receipt;1 one or more citation unreceipted;2 could-not-evaluate (report or revision unreadable) | `python3 tools/check-report-receipts.py --selftest` | R30 mined mistake R30-UNRECEIPTED-GATES (QUALITY 77): exits 1 on the round-29 report at lane `8976ca92` (Gates at `434a7903`) | committed reads; selftest private fixtures | tsukuroi |
| owed-statements-v4shapes-battery | probe | `python3 tools/mutants-owed-statements-r29-v4shapes.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--keep]` | 0 control 12, no routed v4 shape accepted, no control refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R30 routed defect 2 of the round-29 spot-check: closed-comment, list-indented, extra-JSON-key and asterisk-id shapes; counter v5 sha256 `6fadf5fbb77579a8a49db36a560de20b20aa2bd3d3f6928218c640b1465c475b` refuses 11 of 11 (v4 `3516d579…` accepted 11 of 11) | private clone under `/fast/scratch/hyaku` | tsukuroi |
| btrfs-repair-r31 | gate | `python3 tools/check-btrfs-repair-r31.py --revision <REV> [--lane <repo>]` | 0 all eight Q01-Q08 rows new_sourced;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen Q01-Q08 question set is measured by the counter | R31 C1: frozen predicate new_sourced; rules R1-R8; six pinned btrfs-progs v7.1 documentation snapshot sha256 values | committed Git reads only | tsukuroi |
| git-child-env-r31 | probe | `python3 tools/probe-git-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness errors;1 one or more (tool, channel) pairs leak;2 harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R31 C2: eleven frozen tools and channels loader-env, child-contract and dotgit-pointer; parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| census-handoff-r32 | gate | `python3 tools/score-census-handoff-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--seed <hex>] [--scenarios N]` | 0 every fixture scenario routed and both live views consistent;1 one or more scenarios unrouted or a live view inconsistent;2 harness error (planted facts not visible in the base census, a non-hermetic run, or a vacuous live check) | none: no self-test mode; 24 seeded fixture scenarios plus two read-only live views are the measurement | R32 C1 v3: base census 58cc2e0b; HANDOFF ADJ-04 mori grammar `class= value= kind= state=`; scenario types none, kill-events, coredumps, both, cumulative-only, cumulative+coredumps, tsukuroi-only | private scratch under the system temp dir; reads the live host read-only | tsukuroi |
| child-env-allowlist-r32 | probe | `python3 tools/probe-child-env-allowlist-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leaking target and no harness errors;1 one or more targets leak an injected name or break parity;2 harness error | none: no self-test mode; the eleven-target control and ambient-names runs are the measurement | R32 C2 v2: eleven frozen tools; BASH_ENV, ENV, GCONV_PATH, PERL5OPT plus eight per-run random names (four of length 2-20, four of 21-200); parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku` | tsukuroi |
| child-env-allowlist-r33 | probe | `python3 tools/probe-child-env-allowlist-r33.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|regression] [--only <tool> ...]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the five-target claim set and channels names, quiet and source are the measurement | R33 C1 probe v3 frozen at 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0, sha256 c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd; claim set 5 targets, channels names, quiet, source, 15 pairs; label leaking; `--set regression` is repair evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |

## Round-34 reading rule — the census coredump count (C2, exploratory)

Appended 2026-10-23 by round 34; every line above is unchanged. `coredump=N` in the PLANE journal note,
and `HANDOFF ADJ-04 mori class=coredumps value=N` copied from it, count boot-0 error-or-higher journal
entries under `SYSLOG_IDENTIFIER=systemd-coredump`. That set holds both systemd crash summaries ("dumped
core." and "terminated abnormally without generating a coredump.", one `MESSAGE_ID`, priority 2) and the
coredump handler's own error records (priority 3). It is not a count of stored cores, distinct programs,
signal-11 crashes or causes. Snapshot lines above that read `coredump=N` as N coredumps are read this
way. Sources, the dated host reconciliation (1621 entries: 252 "dumped core", 1365 without a core, 4
handler errors; `Storage=none`, every `coredumpctl` record `corefile` none) and the unknowns:
`corpus/knowledge/coredump-count-unit-r34.md` (S186, S187, S188). The census code is unchanged.

## Gate and probe registry — round34 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every round33 row
is retained verbatim and round34 appends the measurement probe of claim C1 and the knowledge-header
gate (QUALITY 70: a tool lands with its row). The round-34 allow-list change to nine tools' child
environment changes no row's entry command or verdict map.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, children get the round-32 allow-list environment); one private temporary HOME directory created at module load and removed at exit (round 32, wave-2 CritNoHarm); no other writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |
| btrfs-space-r30 | gate | `python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]` | 0 all ten rows D01 to D10 verified;1 one or more row unverified;2 could-not-evaluate (revision or base registry unreadable) | none: no self-test mode; fixture mode `--tree <DIR> --base-sources <FILE>` is exercised by the battery `mutants-btrfs-space-r30` | R30 C1: ten frozen questions D01 to D10 with frozen tokens, base `fbfec6bd`, rules R1 to R9; declared version 1 sha256 `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (commit `8fb2cef0`), version 2 after the wave-1 attacks | committed reads only | tsukuroi |
| btrfs-space-battery | probe | `python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]` | 0 control 10, no should-fail shape accepted and no should-pass shape refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `btrfs-space-r30`; its counts are re-derived by wave seats | R30 C1 (QUALITY 73): synthetic fixture, 72 should-fail and 11 should-pass shapes in version 2 (46 and 6 at the declaration) | private temporary directory; no git | tsukuroi |
| git-env-residual | probe | `python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness error;1 a pair leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R30 C2: eleven frozen git-writing tools, channels path-wrapper, user-files and enclosing-repo (33 pairs); probe sha256 `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| run-receipt | probe | `python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE> [--lane <repo>] [--timeout <s>] -- <tool> [args...]` | 0 the tool exited 0;1 the tool exited 1 (its own verdict);2 revision or tool unreadable, or the tool's own could-not-evaluate | none: no self-test mode; the receipt header (revision, tool revision, tool sha256) is the evidence | R30 routed defect 1 (QUALITY 77): runs a tracked tool from a sandbox clone at the tool revision with a private HOME and writes header, stdout and footer | the `--out` receipt file; sandbox clone under `/fast/scratch/hyaku` | tsukuroi |
| report-receipts | gate | `python3 tools/check-report-receipts.py --report <PATH> --lane <repo> --revision <REV>` | 0 every revision-cited gate or measurement has a committed receipt;1 one or more citation unreceipted;2 could-not-evaluate (report or revision unreadable) | `python3 tools/check-report-receipts.py --selftest` | R30 mined mistake R30-UNRECEIPTED-GATES (QUALITY 77): exits 1 on the round-29 report at lane `8976ca92` (Gates at `434a7903`) | committed reads; selftest private fixtures | tsukuroi |
| owed-statements-v4shapes-battery | probe | `python3 tools/mutants-owed-statements-r29-v4shapes.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--keep]` | 0 control 12, no routed v4 shape accepted, no control refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R30 routed defect 2 of the round-29 spot-check: closed-comment, list-indented, extra-JSON-key and asterisk-id shapes; counter v5 sha256 `6fadf5fbb77579a8a49db36a560de20b20aa2bd3d3f6928218c640b1465c475b` refuses 11 of 11 (v4 `3516d579…` accepted 11 of 11) | private clone under `/fast/scratch/hyaku` | tsukuroi |
| btrfs-repair-r31 | gate | `python3 tools/check-btrfs-repair-r31.py --revision <REV> [--lane <repo>]` | 0 all eight Q01-Q08 rows new_sourced;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen Q01-Q08 question set is measured by the counter | R31 C1: frozen predicate new_sourced; rules R1-R8; six pinned btrfs-progs v7.1 documentation snapshot sha256 values | committed Git reads only | tsukuroi |
| git-child-env-r31 | probe | `python3 tools/probe-git-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness errors;1 one or more (tool, channel) pairs leak;2 harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R31 C2: eleven frozen tools and channels loader-env, child-contract and dotgit-pointer; parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| census-handoff-r32 | gate | `python3 tools/score-census-handoff-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--seed <hex>] [--scenarios N]` | 0 every fixture scenario routed and both live views consistent;1 one or more scenarios unrouted or a live view inconsistent;2 harness error (planted facts not visible in the base census, a non-hermetic run, or a vacuous live check) | none: no self-test mode; 24 seeded fixture scenarios plus two read-only live views are the measurement | R32 C1 v3: base census 58cc2e0b; HANDOFF ADJ-04 mori grammar `class= value= kind= state=`; scenario types none, kill-events, coredumps, both, cumulative-only, cumulative+coredumps, tsukuroi-only | private scratch under the system temp dir; reads the live host read-only | tsukuroi |
| child-env-allowlist-r32 | probe | `python3 tools/probe-child-env-allowlist-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leaking target and no harness errors;1 one or more targets leak an injected name or break parity;2 harness error | none: no self-test mode; the eleven-target control and ambient-names runs are the measurement | R32 C2 v2: eleven frozen tools; BASH_ENV, ENV, GCONV_PATH, PERL5OPT plus eight per-run random names (four of length 2-20, four of 21-200); parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku` | tsukuroi |
| child-env-allowlist-r33 | probe | `python3 tools/probe-child-env-allowlist-r33.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|regression] [--only <tool> ...]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the five-target claim set and channels names, quiet and source are the measurement | R33 C1 probe v3 frozen at 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0, sha256 c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd; claim set 5 targets, channels names, quiet, source, 15 pairs; label leaking; `--set regression` is repair evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| child-env-allowlist-r34 | probe | `python3 tools/probe-child-env-allowlist-r34.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|r33claim\|regression] [--only <tool> ...] [--base <REV>]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the nine-target claim set and channels names, quiet and source are the measurement | R34 C1 probe VERSION 5 after pre-data amendment 1 at 15c9ac0e1b02917f43c0bc016d6060f888cb603a, sha256 5231dbafc472ff42e041cbaad3f48dd8bd204d58b6ab22e497cf9372b23d6bfd; claim set 9 targets, channels names, quiet, source, 27 pairs; base parity against the claim base 2641591e303057cd0f67e190a6bdf7fa91a45c31; label leaking; `--set r33claim` and `--set regression` are no-harm evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| knowledge-header | gate | `python3 tools/check-knowledge-header.py --revision <REV> [--lane <repo>] [--branch <BRANCH>]` | 0 every corpus/knowledge/*.md carries source:, verified-at: (ISO date) and recheck: (ISO date or cadence);1 one or more KNOWLEDGE-HEADER-MISSING or KNOWLEDGE-HEADER-VALUE findings;2 could-not-evaluate | `python3 tools/check-knowledge-header.py --selftest` | QUALITY 8; red at 6de666c427ba9aa6b4350561980bde8d0e7c261d on kill-oom-boundary-r33.md (and nine recheck cadence findings) before the round-34 fix | committed reads; selftest private fixtures | tsukuroi |


## Gate and probe registry — round35 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every round34 row
is retained verbatim and round35 appends the two pacnew/pacsave drift counters (QUALITY 70). The
census row's entry command and verdict map are unchanged: the round-35 drift arm adds one
verdict-neutral `DRIFT pacnew-plane` line.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, children get the round-32 allow-list environment); one private temporary HOME directory created at module load and removed at exit (round 32, wave-2 CritNoHarm); no other writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |
| btrfs-space-r30 | gate | `python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]` | 0 all ten rows D01 to D10 verified;1 one or more row unverified;2 could-not-evaluate (revision or base registry unreadable) | none: no self-test mode; fixture mode `--tree <DIR> --base-sources <FILE>` is exercised by the battery `mutants-btrfs-space-r30` | R30 C1: ten frozen questions D01 to D10 with frozen tokens, base `fbfec6bd`, rules R1 to R9; declared version 1 sha256 `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (commit `8fb2cef0`), version 2 after the wave-1 attacks | committed reads only | tsukuroi |
| btrfs-space-battery | probe | `python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]` | 0 control 10, no should-fail shape accepted and no should-pass shape refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `btrfs-space-r30`; its counts are re-derived by wave seats | R30 C1 (QUALITY 73): synthetic fixture, 72 should-fail and 11 should-pass shapes in version 2 (46 and 6 at the declaration) | private temporary directory; no git | tsukuroi |
| git-env-residual | probe | `python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness error;1 a pair leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R30 C2: eleven frozen git-writing tools, channels path-wrapper, user-files and enclosing-repo (33 pairs); probe sha256 `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| run-receipt | probe | `python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE> [--lane <repo>] [--timeout <s>] -- <tool> [args...]` | 0 the tool exited 0;1 the tool exited 1 (its own verdict);2 revision or tool unreadable, or the tool's own could-not-evaluate | none: no self-test mode; the receipt header (revision, tool revision, tool sha256) is the evidence | R30 routed defect 1 (QUALITY 77): runs a tracked tool from a sandbox clone at the tool revision with a private HOME and writes header, stdout and footer | the `--out` receipt file; sandbox clone under `/fast/scratch/hyaku` | tsukuroi |
| report-receipts | gate | `python3 tools/check-report-receipts.py --report <PATH> --lane <repo> --revision <REV>` | 0 every revision-cited gate or measurement has a committed receipt;1 one or more citation unreceipted;2 could-not-evaluate (report or revision unreadable) | `python3 tools/check-report-receipts.py --selftest` | R30 mined mistake R30-UNRECEIPTED-GATES (QUALITY 77): exits 1 on the round-29 report at lane `8976ca92` (Gates at `434a7903`) | committed reads; selftest private fixtures | tsukuroi |
| owed-statements-v4shapes-battery | probe | `python3 tools/mutants-owed-statements-r29-v4shapes.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--keep]` | 0 control 12, no routed v4 shape accepted, no control refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R30 routed defect 2 of the round-29 spot-check: closed-comment, list-indented, extra-JSON-key and asterisk-id shapes; counter v5 sha256 `6fadf5fbb77579a8a49db36a560de20b20aa2bd3d3f6928218c640b1465c475b` refuses 11 of 11 (v4 `3516d579…` accepted 11 of 11) | private clone under `/fast/scratch/hyaku` | tsukuroi |
| btrfs-repair-r31 | gate | `python3 tools/check-btrfs-repair-r31.py --revision <REV> [--lane <repo>]` | 0 all eight Q01-Q08 rows new_sourced;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen Q01-Q08 question set is measured by the counter | R31 C1: frozen predicate new_sourced; rules R1-R8; six pinned btrfs-progs v7.1 documentation snapshot sha256 values | committed Git reads only | tsukuroi |
| git-child-env-r31 | probe | `python3 tools/probe-git-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness errors;1 one or more (tool, channel) pairs leak;2 harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R31 C2: eleven frozen tools and channels loader-env, child-contract and dotgit-pointer; parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| census-handoff-r32 | gate | `python3 tools/score-census-handoff-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--seed <hex>] [--scenarios N]` | 0 every fixture scenario routed and both live views consistent;1 one or more scenarios unrouted or a live view inconsistent;2 harness error (planted facts not visible in the base census, a non-hermetic run, or a vacuous live check) | none: no self-test mode; 24 seeded fixture scenarios plus two read-only live views are the measurement | R32 C1 v3: base census 58cc2e0b; HANDOFF ADJ-04 mori grammar `class= value= kind= state=`; scenario types none, kill-events, coredumps, both, cumulative-only, cumulative+coredumps, tsukuroi-only | private scratch under the system temp dir; reads the live host read-only | tsukuroi |
| child-env-allowlist-r32 | probe | `python3 tools/probe-child-env-allowlist-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leaking target and no harness errors;1 one or more targets leak an injected name or break parity;2 harness error | none: no self-test mode; the eleven-target control and ambient-names runs are the measurement | R32 C2 v2: eleven frozen tools; BASH_ENV, ENV, GCONV_PATH, PERL5OPT plus eight per-run random names (four of length 2-20, four of 21-200); parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku` | tsukuroi |
| child-env-allowlist-r33 | probe | `python3 tools/probe-child-env-allowlist-r33.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|regression] [--only <tool> ...]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the five-target claim set and channels names, quiet and source are the measurement | R33 C1 probe v3 frozen at 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0, sha256 c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd; claim set 5 targets, channels names, quiet, source, 15 pairs; label leaking; `--set regression` is repair evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| child-env-allowlist-r34 | probe | `python3 tools/probe-child-env-allowlist-r34.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|r33claim\|regression] [--only <tool> ...] [--base <REV>]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the nine-target claim set and channels names, quiet and source are the measurement | R34 C1 probe VERSION 5 after pre-data amendment 1 at 15c9ac0e1b02917f43c0bc016d6060f888cb603a, sha256 5231dbafc472ff42e041cbaad3f48dd8bd204d58b6ab22e497cf9372b23d6bfd; claim set 9 targets, channels names, quiet, source, 27 pairs; base parity against the claim base 2641591e303057cd0f67e190a6bdf7fa91a45c31; label leaking; `--set r33claim` and `--set regression` are no-harm evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| knowledge-header | gate | `python3 tools/check-knowledge-header.py --revision <REV> [--lane <repo>] [--branch <BRANCH>]` | 0 every corpus/knowledge/*.md carries source:, verified-at: (ISO date) and recheck: (ISO date or cadence);1 one or more KNOWLEDGE-HEADER-MISSING or KNOWLEDGE-HEADER-VALUE findings;2 could-not-evaluate | `python3 tools/check-knowledge-header.py --selftest` | QUALITY 8; red at 6de666c427ba9aa6b4350561980bde8d0e7c261d on kill-oom-boundary-r33.md (and nine recheck cadence findings) before the round-34 fix | committed reads; selftest private fixtures | tsukuroi |
| score-pacnew-arm-r35 | probe | `python3 tools/score-pacnew-arm-r35.py --lane <repo> --revision <REV>` | 0 every fixture matches;1 any fixture does not match;2 harness error | none (pre-freeze control wave receipts `.ufo/waves/round-35/w1/K*/`) | VERSION 1 sha256 19d25d14…; met by controls K08FixtureKeyed and K15FieldMutants, so not a claim counter | private temp fixtures only; reads committed census bytes | tsukuroi |
| score-pacnew-arm-r35b | probe | `python3 tools/score-pacnew-arm-r35b.py --lane <repo> --revision <REV> [--skip-battery]` | 0 candidate and control match every view and no should-fail arm is accepted;1 otherwise;2 harness error | the battery itself (control arm plus 17 should-fail arms) | VERSION 2 sha256 7517af92…; 20 stub, 3 namespace, 1 live view; claim base b40c01df | private temp fixtures; unprivileged user+mount namespace; live view reads /etc names and pacman.log read-only | tsukuroi |

## Round 35 — reading the census `DRIFT pacnew-plane` line (C1)

The census prints one `DRIFT pacnew-plane pacnew=N pacsave=N pacorig=N unreadable=N log_pacnew=N log_pacsave=N unlogged=N gone=N log=ok|unreadable` line after the HANDOFF lines (`tools/tsukuroi-census.sh` header, round-35 paragraph). Read it as names and counts, never as a verdict: it changes no PLANE text, rollup term or exit code. `unreadable` depends on the uid that ran the census (a user sees directories root can read); `unlogged` counts current files pacman's log never named, which includes every `.pacsave.N` (pacman renames older saves without a log line) and any file left from before the log's start; `gone` counts logged targets no longer present, which is the normal state after an operator merged and removed a `.pacnew`. `log=unreadable` means the pairing fields are not evidence. A nonzero `pacnew` is an operator action item under S010/S011 (compare and merge), never a census-performed action. Counter: `tools/score-pacnew-arm-r35b.py` (registry row above).
## Round 36 — `NoUpgrade` / `NoExtract` are file-extraction rules, not version pins (supersedes `SKILL.md:397-399`)

Appended in round 36 as routed repair 4 (`corpus/lessons/round-35-verifier-spotcheck.md` §6 item 4).
The historical bullet at `SKILL.md:397-399` is preserved unchanged; this block supersedes its
**classification only**.

Prior locus (`SKILL.md:397-399`), verbatim:

> - `HoldPkg = pacman glibc` is removal-protection, **not a version hold**; true
>   pins are `IgnorePkg` / `IgnoreGroup` / `NoUpgrade` / `NoExtract` — all empty
>   (`:204-222`).

Superseded as a classification by `corpus/knowledge/pacman-backup-files-r35.md`
(§ `[obs] NoUpgrade and NoExtract (S191, S195)`), whose sources are S191 pacman
`lib/libalpm/add.c` at 54d94116164b and S195 pacman `doc/pacman.conf.5.asciidoc` at
54d94116164b (`corpus/SOURCES.md:197` and `:201`):

- the version pins are `IgnorePkg` / `IgnoreGroup` — "Instructs pacman to ignore any upgrades for
  this package when performing a '--sysupgrade'." (S195 lines 102-104; group form S195 lines 106-109);
- `NoUpgrade` / `NoExtract` act on package-archive **file paths**, not on package versions:
  "All files listed with a `NoUpgrade` directive will never be touched during a package
  install/upgrade" (S195 lines 136-137) and "All files listed with a `NoExtract` directive will
  never be extracted from a package into the filesystem" (S195 lines 147-148). In the code,
  `NoExtract` skips the member outright (S191 lines 223-230), `NoUpgrade` leaves an existing
  target untouched (S191 lines 302-304) and the incoming file is written as `.pacnew` with the
  warning `warning: %s installed as %s.pacnew` (S191 lines 338-350).

Replacement sentence:

> - `HoldPkg = pacman glibc` is removal-protection, **not a version hold**; the true
>   version pins are `IgnorePkg` / `IgnoreGroup` — all empty — while `NoUpgrade` /
>   `NoExtract` are file-extraction rules, not version pins (also empty) (`:204-222`;
>   classification per `corpus/knowledge/pacman-backup-files-r35.md`, S191/S195).

Values stand unchanged: `IgnorePkg`, `IgnoreGroup`, `NoUpgrade` and `NoExtract` are all empty on
this host (re-measured 2026-10-23 by round-35 wave-1 `ExecHostPacnew`,
`.ufo/waves/round-35/w1/ExecHostPacnew/capture.txt:76-97`; re-measured read-only
2026-10-24T03:08:20Z: `/etc/pacman.conf` carries no `IgnorePkg`/`IgnoreGroup`/`NoUpgrade`/
`NoExtract` line — only `HoldPkg = pacman glibc` at line 7 — and `pacman-conf` prints nothing
for each of the four keys, rc=0).
## Gate and probe registry — round36 superseding current rows

The unique highest complete table is operative; every earlier table is historical. Every
round35 row is retained verbatim and round36 inserts one probe row after the delimiter. The
census row's entry command and verdict map are unchanged.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| child-env-allowlist-r36 | probe | `python3 tools/probe-child-env-allowlist-r36.py --revision <REV> --set livefive` | last-line `leaking` 0 clean / > 0 leaking; exit 0 clean, 1 leaking, 2 harness | none hermetic; sensitivity battery per `.ufo/waves/round-36/l1/` (claim/r33claim 0 at base) and the w2 live-mode detector receipts | VERSION 7; predicate label `leaking`; frozen bytes sha256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` at `1e926801195e304950e3eb9d2525ef8bbc245089` | committed reads; sandbox clones; no lane or host write | tsukuroi |
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, children get the round-32 allow-list environment); one private temporary HOME directory created at module load and removed at exit (round 32, wave-2 CritNoHarm); no other writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |
| btrfs-space-r30 | gate | `python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]` | 0 all ten rows D01 to D10 verified;1 one or more row unverified;2 could-not-evaluate (revision or base registry unreadable) | none: no self-test mode; fixture mode `--tree <DIR> --base-sources <FILE>` is exercised by the battery `mutants-btrfs-space-r30` | R30 C1: ten frozen questions D01 to D10 with frozen tokens, base `fbfec6bd`, rules R1 to R9; declared version 1 sha256 `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (commit `8fb2cef0`), version 2 after the wave-1 attacks | committed reads only | tsukuroi |
| btrfs-space-battery | probe | `python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]` | 0 control 10, no should-fail shape accepted and no should-pass shape refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `btrfs-space-r30`; its counts are re-derived by wave seats | R30 C1 (QUALITY 73): synthetic fixture, 72 should-fail and 11 should-pass shapes in version 2 (46 and 6 at the declaration) | private temporary directory; no git | tsukuroi |
| git-env-residual | probe | `python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness error;1 a pair leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R30 C2: eleven frozen git-writing tools, channels path-wrapper, user-files and enclosing-repo (33 pairs); probe sha256 `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| run-receipt | probe | `python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE> [--lane <repo>] [--timeout <s>] -- <tool> [args...]` | 0 the tool exited 0;1 the tool exited 1 (its own verdict);2 revision or tool unreadable, or the tool's own could-not-evaluate | none: no self-test mode; the receipt header (revision, tool revision, tool sha256) is the evidence | R30 routed defect 1 (QUALITY 77): runs a tracked tool from a sandbox clone at the tool revision with a private HOME and writes header, stdout and footer | the `--out` receipt file; sandbox clone under `/fast/scratch/hyaku` | tsukuroi |
| report-receipts | gate | `python3 tools/check-report-receipts.py --report <PATH> --lane <repo> --revision <REV>` | 0 every revision-cited gate or measurement has a committed receipt;1 one or more citation unreceipted;2 could-not-evaluate (report or revision unreadable) | `python3 tools/check-report-receipts.py --selftest` | R30 mined mistake R30-UNRECEIPTED-GATES (QUALITY 77): exits 1 on the round-29 report at lane `8976ca92` (Gates at `434a7903`) | committed reads; selftest private fixtures | tsukuroi |
| owed-statements-v4shapes-battery | probe | `python3 tools/mutants-owed-statements-r29-v4shapes.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--keep]` | 0 control 12, no routed v4 shape accepted, no control refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R30 routed defect 2 of the round-29 spot-check: closed-comment, list-indented, extra-JSON-key and asterisk-id shapes; counter v5 sha256 `6fadf5fbb77579a8a49db36a560de20b20aa2bd3d3f6928218c640b1465c475b` refuses 11 of 11 (v4 `3516d579…` accepted 11 of 11) | private clone under `/fast/scratch/hyaku` | tsukuroi |
| btrfs-repair-r31 | gate | `python3 tools/check-btrfs-repair-r31.py --revision <REV> [--lane <repo>]` | 0 all eight Q01-Q08 rows new_sourced;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen Q01-Q08 question set is measured by the counter | R31 C1: frozen predicate new_sourced; rules R1-R8; six pinned btrfs-progs v7.1 documentation snapshot sha256 values | committed Git reads only | tsukuroi |
| git-child-env-r31 | probe | `python3 tools/probe-git-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness errors;1 one or more (tool, channel) pairs leak;2 harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R31 C2: eleven frozen tools and channels loader-env, child-contract and dotgit-pointer; parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| census-handoff-r32 | gate | `python3 tools/score-census-handoff-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--seed <hex>] [--scenarios N]` | 0 every fixture scenario routed and both live views consistent;1 one or more scenarios unrouted or a live view inconsistent;2 harness error (planted facts not visible in the base census, a non-hermetic run, or a vacuous live check) | none: no self-test mode; 24 seeded fixture scenarios plus two read-only live views are the measurement | R32 C1 v3: base census 58cc2e0b; HANDOFF ADJ-04 mori grammar `class= value= kind= state=`; scenario types none, kill-events, coredumps, both, cumulative-only, cumulative+coredumps, tsukuroi-only | private scratch under the system temp dir; reads the live host read-only | tsukuroi |
| child-env-allowlist-r32 | probe | `python3 tools/probe-child-env-allowlist-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leaking target and no harness errors;1 one or more targets leak an injected name or break parity;2 harness error | none: no self-test mode; the eleven-target control and ambient-names runs are the measurement | R32 C2 v2: eleven frozen tools; BASH_ENV, ENV, GCONV_PATH, PERL5OPT plus eight per-run random names (four of length 2-20, four of 21-200); parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku` | tsukuroi |
| child-env-allowlist-r33 | probe | `python3 tools/probe-child-env-allowlist-r33.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|regression] [--only <tool> ...]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the five-target claim set and channels names, quiet and source are the measurement | R33 C1 probe v3 frozen at 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0, sha256 c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd; claim set 5 targets, channels names, quiet, source, 15 pairs; label leaking; `--set regression` is repair evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| child-env-allowlist-r34 | probe | `python3 tools/probe-child-env-allowlist-r34.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|r33claim\|regression] [--only <tool> ...] [--base <REV>]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the nine-target claim set and channels names, quiet and source are the measurement | R34 C1 probe VERSION 5 after pre-data amendment 1 at 15c9ac0e1b02917f43c0bc016d6060f888cb603a, sha256 5231dbafc472ff42e041cbaad3f48dd8bd204d58b6ab22e497cf9372b23d6bfd; claim set 9 targets, channels names, quiet, source, 27 pairs; base parity against the claim base 2641591e303057cd0f67e190a6bdf7fa91a45c31; label leaking; `--set r33claim` and `--set regression` are no-harm evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| knowledge-header | gate | `python3 tools/check-knowledge-header.py --revision <REV> [--lane <repo>] [--branch <BRANCH>]` | 0 every corpus/knowledge/*.md carries source:, verified-at: (ISO date) and recheck: (ISO date or cadence);1 one or more KNOWLEDGE-HEADER-MISSING or KNOWLEDGE-HEADER-VALUE findings;2 could-not-evaluate | `python3 tools/check-knowledge-header.py --selftest` | QUALITY 8; red at 6de666c427ba9aa6b4350561980bde8d0e7c261d on kill-oom-boundary-r33.md (and nine recheck cadence findings) before the round-34 fix | committed reads; selftest private fixtures | tsukuroi |
| score-pacnew-arm-r35 | probe | `python3 tools/score-pacnew-arm-r35.py --lane <repo> --revision <REV>` | 0 every fixture matches;1 any fixture does not match;2 harness error | none (pre-freeze control wave receipts `.ufo/waves/round-35/w1/K*/`) | VERSION 1 sha256 19d25d14…; met by controls K08FixtureKeyed and K15FieldMutants, so not a claim counter | private temp fixtures only; reads committed census bytes | tsukuroi |
| score-pacnew-arm-r35b | probe | `python3 tools/score-pacnew-arm-r35b.py --lane <repo> --revision <REV> [--skip-battery]` | 0 candidate and control match every view and no should-fail arm is accepted;1 otherwise;2 harness error | the battery itself (control arm plus 17 should-fail arms) | VERSION 2 sha256 7517af92…; 20 stub, 3 namespace, 1 live view; claim base b40c01df | private temp fixtures; unprivileged user+mount namespace; live view reads /etc names and pacman.log read-only | tsukuroi |
| journalctl-v262-corrections-r37 | gate | `python3 tools/check-journalctl-v262-corrections.py --revision <REV>` | 0 three fixed correction clusters match;1 missing/wrong correction;2 unreadable revision or CLI | `python3 tools/check-journalctl-v262-corrections.py --selftest` | Round37 correction block: exact 15 `field_list_has_scope_options()` terms; separate observed `-n -F` truncation and unchanged `-n -N` output; `--list-boots` action replacement; prior S024/round-1 teaching acknowledged | immutable Git read of the note; selftest in-memory fixtures | tsukuroi |
| child-env-allowlist-r37 | probe | `python3 tools/probe-child-env-allowlist-r37.py --revision <REV> --set livefive` | 0 `leaking` 0 and `harness_errors` empty;1 leaking pair;2 harness error | none; direct livefive receipt at `.ufo/waves/round-37/before/v8-livefive-baseline.jsonl` | VERSION 8; sha256 `9aee085b45d7566d6ce398733c10d3d87ae29bce107c4bd13fcdffcb4854b064`; 5 targets/15 predicate pairs; untraced is supplemental diagnostic only; base 564db0b | immutable target exports and disposable clones; no lane or host write | tsukuroi |
| storage-arm-r38 | gate | `python3 tools/score-storage-arm-r38.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 ten fixtures, the live leg and six PLANE lines per run match;1 any fixture, the live leg or the plane count differs;2 revision, git or bash could-not-evaluate | none: the ten built-in fixtures F01-F10 and the live leg are the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` | R38 C1 frozen at `7cbaeb63`, sha256 `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`; QUALITY 82 gap: a fixture-gated arm passes it (`controls-q82.jsonl`), so it is used only with `storage-arm-r38-q82` | private mkdtemp fixtures under `--scratch`/`TMPDIR`; reads the census at REV through git; no host write | tsukuroi |
| storage-arm-r38-q82 | gate | `python3 tools/score-storage-arm-r38-q82.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 every production-path view matches;1 a view differs;2 revision, unshare or v1-model digest could-not-evaluate | none: three per-run random views are the measurement; controls `.ufo/waves/round-38/controls/controls-q82.jsonl` (fixture-gated 0/3, cached-live 1/3, real arm 3/3) | R38 pre-seat amendment `9c9bb647`, sha256 `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3`; loads the v1 model from `7cbaeb63` by digest | `unshare -rm` child namespace with a bind mount over `/sys/fs/btrfs` that never leaves it; scratch under `--scratch`/`TMPDIR` | tsukuroi |
| hook-order-r38 | gate | `python3 tools/check-hook-order-r38.py --revision <REV> [--repo <PATH>]` | 0 all 69 rows match the frozen capture and the cited rows are mined, used-by the entry and opened 2026-10-26;1 a missing, wrong, extra or duplicate row or a source problem;2 revision, git or capture_tampered could-not-evaluate | none: the frozen capture is the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` (base, full-name sort, no override, no source FAIL; correct PASS) | R38 C2 frozen at `7cbaeb63`, sha256 `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`; capture MANIFEST sha256 `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`; libalpm order model of pacman 54d9411 | reads the entry and SOURCES at REV through git and the digest-verified capture from the work tree; no write | tsukuroi |
| storage-hidden-r39 | gate | `python3 tools/score-storage-hidden-r39.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 both hidden-root legs BLOCKED mounts:btrfs-without-sysfs, three tmpfs views, five fixtures, the live leg and six PLANE lines per run match;1 any leg differs;2 revision, git, unshare or no STORAGE line from the namespace legs | none: the hidden legs H1/H2, views V0-V2, fixtures F1-F5 and the live leg are the measurement; controls `.ufo/waves/round-39/controls/` | R39 C1 frozen at the round-39 freeze commit, sha256 `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`; views are tmpfs mounts filled from stdin inside the child (R38-Q82-LEAK) | `unshare -rm` child namespace with tmpfs mounts that never leave it; scratch under `--scratch`/`TMPDIR` | tsukuroi |
| transaction-order-r39 | gate | `python3 tools/check-transaction-order-r39.py --revision <REV> [--repo <PATH>]` | 0 TO1-TO8 each quoted from the pinned libalpm snapshot at the cited lines on a mined upstream row named on `source:`, no duplicate row or heading, two host counts present, 0 running lines inside a commit phase;1 any of these fails;2 revision, git or frozen input tampered | none: the frozen snapshots and capture are the measurement; controls `.ufo/waves/round-39/controls/` | R39 C2 frozen at the round-39 freeze commit, sha256 `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`; snapshot sha256 pins in code; capture MANIFEST sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4` | reads the entry and SOURCES at REV through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| selftest-literals-r40 | gate | `python3 tools/score-selftest-literals-r40.py --revision <REV> --scratch <DIR> [--repo <PATH>] [--jobs N]` | 0 the unmutated census selftest PASSes, three neutral rewrites of the mount-table arm PASS, all nine frozen literal/guard mutants apply once and each fails the selftest, and the census holds 5 self-reference lines;1 any of these fails;2 revision, git or scratch could-not-evaluate | none: the nine mutants and three neutral rewrites are the measurement; controls `.ufo/waves/round-40/controls/` | R40 C1 frozen at the round-40 freeze commit, sha256 `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159`; mutant texts and SELFREF_BASE 5 in code | writes only a private directory under `--scratch`, removed before exit; reads the census at REV through git | tsukuroi |
| exec-environment-r40 | gate | `python3 tools/check-exec-environment-r40.py --revision <REV> [--repo <PATH>]` | 0 EX1-EX8 each carry the source-derived value, the frozen proposition tokens and no negation word in the rule cell, a 4-25 word quote at the cited lines of the pinned snapshot on a new mined upstream row named on `source:`, no duplicate row or heading, two host values present, 0 base hits of the novelty tokens;1 any of these fails;2 revision, git, frozen input tampered or a derivation pattern unmatched | none: the frozen snapshots and capture are the measurement; controls `.ufo/waves/round-40/controls/` | R40 C2 frozen at the round-40 freeze commit, sha256 `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`; snapshot sha256 pins in code; capture MANIFEST sha256 `57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5` | reads the entry and SOURCES at REV and BASE through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| selftest-mounts-r41 | gate | `python3 tools/score-selftest-mounts-r41.py --revision <REV> --scratch <DIR> [--repo <PATH>] [--jobs N] [--timeout S]` | 0 the unmutated census selftest PASSes, three neutral rewrites and one decoy (every mutant text in a dead here-document) PASS, all thirteen frozen mutants (M1-M9, H5, H6, H9, H10) apply once and each is killed twice on a baseline case label, and the captured fixture tables cover the four declared shapes (mountpoint not absolute, source not /dev, no subvol=, two btrfs lines) on BLOCKED cases;1 any of these fails;2 revision, git or scratch could-not-evaluate | none: the mutants, neutrals, decoy and capture are the measurement; controls `.ufo/waves/round-41/controls/` | R41 C1 frozen at the round-41 freeze commit, sha256 `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`; mutant, neutral and decoy texts in code | writes only a private directory under `--scratch`, removed on exit, SIGINT and SIGTERM; the capture line is injected only into the private copy | tsukuroi |
| package-anatomy-r41 | gate | `python3 tools/check-package-anatomy-r41.py --revision <REV> [--repo <PATH>]` | 0 PA1-PA8 each carry the source-derived value, the frozen proposition relations and no negation word, a 4-25 word quote inside the row's frozen source window on a new mined upstream row named on `source:`, a committed reviewer verdict `holds` and none `fails`, six host values present, no duplicate row or heading, 0 base hits of the novelty tokens;1 any of these fails;2 revision, git, frozen input tampered or a derivation pattern unmatched | none: the frozen snapshots, capture and verdict files are the measurement; controls `.ufo/waves/round-41/controls/` | R41 C2 frozen at the round-41 freeze commit, sha256 `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`; snapshot sha256 pins in code; capture MANIFEST sha256 `632ed0443cfb26ef002ebfd2a3a99971221f9129836b63135e0ca6ea41874f89` | reads the entry, SOURCES and verdict files at REV and BASE through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| scrub-record-r42 | gate | `python3 tools/check-scrub-record-r42.py --revision <REV> [--lane <repo>]` | 0 SC1-SC5 present with quotes inside the frozen source windows, novelty verified, at least three host values, one mined source row and five wave-2 seat verdicts bound through `w2-dispatch.json` and `w2-results.json`;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen SC1-SC5 row set and the wave-2 verdict binding are the measurement | R42 C2 frozen predicate `rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1 and verdicts_ok == 5 and novelty_base_hits == 0`; pinned btrfs-progs v7.1 `cmds/scrub.c` and `CHANGES` snapshots listed in `.ufo/waves/round-42/frozen/src/SHA256SUMS` | committed Git reads only | tsukuroi |
| size-invariance-r42 | gate | `python3 tools/score-size-invariance-r42.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1` over ten P1-P6 and U1-U4 size twins and three `unshare -rm` production-path legs;1 any leg non-invariant or the census selftest not PASS;2 could-not-evaluate | none: no self-test mode; the ten fixture twins and the three namespace legs are the measurement | R42 C1 frozen counter sha256 `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`; 1 MiB verdict-neutral padding; fixtures built from the base census at `c8efaa3f` | private fixture copies under `--scratch`; `unshare -rm` namespace only for the N1/N3/N6 legs | tsukuroi |

## Storage integrity arm — round 38

Appended 2026-10-26 (round-38 C1). The census reads the five per-device btrfs error counters and prints
one **verdict-neutral** line after `DRIFT pacnew-plane` and before the rollup (`probe_storage_arm` in
`tools/tsukuroi-census.sh`; contract in the header paragraph "Round-38 addition"). It adds no `PLANE`, no
rollup term and no exit-code change, so **read the line itself; the rollup never carries it.** Normative
detail: `corpus/knowledge/storage-health-r26.md` SH1 and SH2; sources S128 and S133.

    STORAGE btrfs-device-stats state=HEALTHY|DEGRADED|BLOCKED filesystems=N devices=N nonzero=N [detail=...]

`filesystems` counts UUID-named entries under `/sys/fs/btrfs` (`features` and other names ignored),
`devices` their `devinfo/<devid>` entries, `nonzero` the (device, counter) **pairs** above zero.
`detail` lists `<fsid8>:<devid>:<key>=<value>` for nonzero pairs and one reason token per unreadable
device: `unreadable`, `malformed`, `no-devinfo`, `bad-devid` (a non-integer devid, never echoed), or
`root:unreadable`.

| `STORAGE` line | Reading | Action (read-only unless marked operator) |
|---|---|---|
| `state=HEALTHY filesystems=0 devices=0 nonzero=0` | The sysfs root is absent. Declared as "no btrfs mounted", but a namespace or container that hides `/sys/fs/btrfs` prints the same line (wave-1 C1CritAbsentRoot) | `findmnt -t btrfs`; if btrfs is mounted, record `0/0/0` as an observability finding, never as clearance |
| `state=HEALTHY filesystems=N devices=N nonzero=0`, N ≥ 1 | All five counters on every device read 0 now (SH1). Counters only: no scrub record (SH4), no NVMe SMART (SH5/SH6) | None for the counters; SH3–SH6 stay Frontier and operator-owned |
| `state=DEGRADED nonzero=N detail=...` | A stored lifetime total, not a dated event (SH2); `write/read/flush_errs` = failed IO, `corruption_errs` = checksum or metadata-header mismatch, `generation_errs` = generation mismatch | Date it from error-level kernel lines (`journalctl -k -p err --grep 'BTRFS.*errs:'`, every retained boot); never reset (`btrfs device stats -z` is operator-owned) |
| `state=BLOCKED detail=...:unreadable` / `:malformed` / `:no-devinfo` / `:bad-devid` / `root:unreadable` | The reading was impossible, not "the disk is corrupt": a file not readable, not exactly the five counters once each, a filesystem without devinfo, a non-integer devid, or an unlistable root | `ls -l` and `cat` the named file once and record the bytes; a single word `invalid` means device stats are not loaded yet (S133) — re-read after the mount settles |
| `state=BLOCKED` with `nonzero=N`, N > 0 | One device blocked beside a sibling with counted pairs | Handle the BLOCKED reason first, then date the counted pairs as for DEGRADED |

Counting: `python3 tools/score-storage-arm-r38.py --revision <REV>` (ten fixtures, the live leg, six
`PLANE` lines per run) **and** `python3 tools/score-storage-arm-r38-q82.py --revision <REV>` (no override,
`unshare -rm`, a per-run random tree bind-mounted over `/sys/fs/btrfs`). The second is required: a
fixture-gated arm passes the first (QUALITY 82, `.ufo/waves/round-38/controls/controls-q82.jsonl`).
Consumer note: the frozen round-35 probe `tools/score-pacnew-arm-r35b.py` compares every non-DRIFT line with
its claim base `b40c01df`, so at any revision after `52ffd65` it reads `base parity` failures for this new
line; it stays a round-35 instrument, valid at its round-35 revisions (wave-1 C1RevConsumers).

## Hook order — round 38

Appended 2026-10-26 (round-38 C2). One new read-only surface for the update-safety plane: which ALPM
hooks exist here, in which order they would run, and which of them can stop a transaction. Every
row below is read from the hook files and from pinned pacman `54d9411` source (snapshots
`.ufo/waves/round-38/sources/`, digests in `SHA256SUMS`); no row rests on running a hook, and nothing
here authorizes a package, hook or transaction action.

Measured 2026-10-26 (`.ufo/waves/round-38/frozen/hooks-capture/`, MANIFEST sha256
`da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`): **70 hook files → 69 effective
hooks** (one same-name override), 17 `PreTransaction` + 52 `PostTransaction`, 0 triggerless masks,
0 `AbortOnFail`, 14 effective `NeedsTargets`. Re-derived live in this seat: 67 files in
`/usr/share/libalpm/hooks` + 3 in `/etc/pacman.d/hooks`; 15 files carry `NeedsTargets`, and the
fifteenth is the `/usr` copy of `90-mkinitcpio-install.hook` that the `/etc` copy overrides — 14 is
the effective count, not a miscount. Rules HO1–HO7 and the full 69-row table:
`corpus/knowledge/pacman-hook-order-r38.md`. Gate:
`python3 tools/check-hook-order-r38.py --revision <REV> [--repo <PATH>]`.

Read-only probes used below, all permitted by the boundary rule: `pacman-conf HookDir`, `pacman -Q
linux`, `grep`/`ls`/`stat` on the two hook directories, `/boot` (gated, see limits) and
`/var/log/pacman.log`.

### Symptom → rule → read-only check → operator action

| Symptom (verbatim string or observation) | Rule | Meaning | Read-only check | Suggested operator action (tsukuroi does not run it) |
|---|---|---|---|---|
| `error: failed to commit transaction (failed to run transaction hooks)`, preceded by `[E] Missing Exec option in hook: <path>`, `[E] Missing When option in hook: <path>`, `[E] hook <path> line N: invalid section\|invalid option` | HO5 | The Pre-phase pass failed while parsing or validating candidates: a `.hook` file **that has a `[Trigger]` section** is malformed (`hook.c:129-146`), or a hook directory could not be opened/read (`hook.c:547-560`). `_alpm_hook_run` returns at `hook.c:629-631` before the run loop, so **no Pre hook ran** and the transaction never started (`trans.c:201-204`; `transaction started` at `:208` is never logged) — no target was installed | The `[E]` line is `_alpm_log(ERROR)` and reaches **stderr only**; `pacman.log` gains `alpm_logaction` lines only, so look for the absent `transaction started` rather than for the error: `grep -n 'transaction \(started\|completed\)' /var/log/pacman.log \| tail -2`, `grep -c "running '" /var/log/pacman.log`, `pacman -Q <named targets>` unchanged. Re-read the named file for `[Trigger]`, `When`, `Exec` | Fix or remove the named file; to disarm a hook without deleting it, reduce it to a `[Trigger]`-less stub (that is HO3, valid). While the file stays broken every transaction fails at Pre — including one whose `When` is `PostTransaction`, since all candidates are validated |
| A hook file you added is named in an `[E]` line although it declares `When = PostTransaction` | HO5 | Same failure: `hook.c:609-615` parses and validates every candidate file in either directory with no reference to `when`; the phase gate is only consulted later (`hook.c:629`, `:638`). Executed witness: `.ufo/waves/round-38/w1/C2CritHO5/matrix.txt:7-9` (T1, `50-bad-post.hook`) → `errnum=32` | as above; do not assume "Post hooks cannot block the transaction" | Same fix; a malformed Post hook file blocks every upgrade on this host |
| Two files share a name, or the `running '<name>'...` line shows an `Exec` you did not write | HO2 | Directories are walked **last list entry → first**, and the system directory is the list head, so `/etc/pacman.d/hooks/<name>` wins and the `/usr/share/libalpm/hooks/<name>` copy is skipped (`hook.c:540`, `:588-590`; `alpm.c:59-62`) | `pacman-conf HookDir` (prints `/etc/pacman.d/hooks/`); `ls /usr/share/libalpm/hooks/<name> /etc/pacman.d/hooks/<name>`; `grep -n '^Exec'` in both | Edit the winning file, or rename; note that deleting the `/etc` copy hands the hook back to `/usr`, so a later package update silently restores stock behaviour |
| `-32`/plain pairs (`fontconfig`, `gio-querymodules`, `gio-remove-module-cache`) run in an order that contradicts `LC_ALL=C sort` of the file names | HO1 | Order is a bytewise `strncmp` of the names **without** the `.hook` suffix over the shorter length, shorter name first on a tie (`hook.c:443-455`). `-` (0x2d) sorts before `.` (0x2e), so full-name sort reverses every such pair | Compare against the entry's `## Effective hook order` table, not `sort`: `ls /usr/share/libalpm/hooks \| LC_ALL=C sort` is a different sequence | Rename rather than renumber if a real dependency exists; report the collision — do not reorder `/usr` files |
| A hook file exists but never appears as `running '<name>'...` | HO3 | Read the mask rule first: a hook file with no `[Trigger]` section is valid and never runs (`hook.c:119-123`); 0 such files on this host. Otherwise it is the phase/trigger filter (HO7) or the phase never ran (HO6) | `grep -c '^\[Trigger\]' <file>`; `grep -n "running '<name>'" /var/log/pacman.log \| tail -3`; confirm a `transaction completed` exists for that attempt | Nothing to do if the silence is a deliberate mask; otherwise chase HO6/HO7 |
| A Pre hook exits non-zero and the upgrade continues | HO4 | A Pre hook's non-zero exit aborts only when the hook carries `AbortOnFail`; `AbortOnFail` on a Post hook is rejected with a warning at load (`hook.c:141-146`), and the run loop breaks only for Pre (`hook.c:660-669`). 0 of the 17 Pre hooks here carry it, so **no Pre hook's exit status can stop a transaction on this host**; the only other Pre blocker is HO5's scan error | `grep -l '^AbortOnFail' /usr/share/libalpm/hooks/*.hook /etc/pacman.d/hooks/*.hook` (expect nothing). Distinguish an HO5 abort from an HO4 abort: HO5 leaves a validation `[E]` line and **no** `running '…'` line for the phase; an aborting Pre run logs `running '<name>'...` first (`hook.c:653`) | Treat the failed hook as an ignored warning and check its product by hand; making it fatal needs a vendor file with `AbortOnFail` — not an `/etc` edit |
| After an upgrade the UKI/initramfs predates the installed kernel, a Post hook did not run, and the command exited 0 | HO6 | The Post phase runs only in the `else` of `state == STATE_INTERRUPTED`, after `transaction completed` (`trans.c:230-241`), so a `transaction failed` or `transaction interrupted` runs none of the 52 Post hooks. Commits are per-target (`add.c:670-687`, `sync.c:1336-1357`): a mid-transaction failure leaves already-committed targets (e.g. the new `linux` modules tree) with the **previous** UKI — version skew, not "nothing happened". An interrupt returns 0 from `alpm_trans_commit` (`trans.c:242-244` with `add.c:673-675`), so a missing Post run need not come with a non-zero exit; and a Post hook's own failure is dropped (`trans.c:238`) and reaches stderr, not `pacman.log` | Log leg: `grep -n 'transaction \(started\|completed\|failed\|interrupted\)' /var/log/pacman.log \| tail -4` and check that the Post `running '...'` lines follow the last `transaction completed`. Artifact leg: `pacman -Q linux` versus `stat -c '%y %n' /boot/…` — **BLOCKED** as a non-root user (measured 2026-10-26: `ls: cannot open directory '/boot': Permission denied`), so record `BLOCKED` and hand the probe over | Re-run the boot-artifact producers by hand (`mkinitcpio -P`, `limine-update`) and verify before reboot; the lane never runs them |
| Within one transaction the `running '...'` order disagrees with the table | HO7 | The table is the order of **candidates**; a transaction runs only the triggered subset, in that order, per phase (`hook.c:633-641`). A real sequence is therefore a subsequence of the table order for its phase, and missing hooks are normal. Witness on this host: `/var/log/pacman.log:3248-3254`, one Pre hook before `transaction started`, one Post hook after `transaction completed` | Extract the phase lines (`awk` between `transaction started` and `transaction completed`, plus the `running` lines before `started`), map each name to its `pos` in the entry table, confirm the positions increase within a phase | If positions are not increasing with an unmodified pacman, the entry or the installed pacman has moved: re-run the gate and report, never hand-edit the table |

### Limits of this table

- **No hook was executed for it.** The rows model candidates from files and pinned source; the
  order of hooks inside a real transaction is not produced here (entry `[unk]`), which is why HO7's
  check is a subsequence test on the log rather than a prediction.
- **NOHOOKS is a separate explanation.** A transaction flagged `ALPM_TRANS_FLAG_NOHOOKS` skips both
  phases (`trans.c:201`, `:237`); at pacman 54d9411 the one command-line option that sets it is `--dbonly`
  (round-38 wave seat C2ScoutNohooks, `.ufo/waves/round-38/w1/C2ScoutNohooks.md`), so "no hook ran at all" after a
  `--dbonly` run is not HO6.
- **Permission can mimic HO5.** A root-owned hook directory that the current user cannot open sets
  the same scan error (`hook.c:547-560`); the tell is `[E] error while reading hook …: Permission
  denied` (`.ufo/waves/round-38/w1/C2CritHO5/matrix.txt`, T11). Hand it to the operator; never escalate.
- **Silence in `pacman.log` is weak evidence.** Only `alpm_logaction` lines reach it
  (`hook.c:653`; `trans.c:208`, `:231`, `:235`); validation and exec failures are stderr-only, so a
  missing log line never proves a hook succeeded.
- **`/boot` is unreadable non-root** (checklist item 7): HO6's artifact leg is `BLOCKED` for an
  agent and stays an operator probe.


## Storage integrity arm — round 39 (absent or empty sysfs root)

Appended 2026-10-26 (round-39 C1, commit `49cc53c7`). Supersedes the first row of the round-38 table above
(`state=HEALTHY filesystems=0 devices=0 nonzero=0`), which stays as written. When `/sys/fs/btrfs` is absent or
holds no fsid entry, the arm now reads the mount table (`/proc/self/mounts`, override `TSUKUROI_PROC_MOUNTS`)
before it calls the disk clean. A root with fsid entries never reads the table.

| `STORAGE` line | Reading | Action (read-only) |
|---|---|---|
| `state=HEALTHY filesystems=0 devices=0 nonzero=0` (since round 39) | No fsid under the root **and** no btrfs mount in this process's mount table: no btrfs is mounted here | None |
| `state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | btrfs is mounted but its sysfs view is hidden or absent (a namespace, container or a tmpfs over `/sys` or `/sys/fs`); the counters could not be read, so nothing is known about them | Re-run the census in the host's own namespace; there, `ls /sys/fs/btrfs` and `findmnt -t btrfs` must agree. Do not read this as disk corruption |
| `state=BLOCKED … detail=mounts:unreadable` | No fsid under the root and the mount table could not be read: "no btrfs" cannot be told from "hidden" | Check that `/proc` is mounted in this namespace (`findmnt /proc`) |

Counting: `python3 tools/score-storage-hidden-r39.py --revision <REV>` — two hidden-root legs inside
`unshare -rm` (tmpfs over `/sys/fs/btrfs`, tmpfs over `/sys/fs`), three random views built on a tmpfs inside the
child namespace from stdin (no host path carries a view: the round-38 Q82 leak, R38-Q82-LEAK), five override
fixtures and the live leg. Consumer note: the round-38 v1 counter `tools/score-storage-arm-r38.py` fixture F06
(absent root under the override, the real mount table listing btrfs) encoded the superseded rule; at revisions
after `49cc53c7` it reads BLOCKED and that counter FAILs 9/10 by construction. It stays a round-38 instrument, valid
at its round-38 revisions (`b0005ae9`).

## Transaction order — round 39

Appended 2026-10-26 (round-39 C2; drafted by wave seat C2ScribeSkill, integrated by the L1). The round-38 table above orders the hooks **inside** one phase (HO1–HO7);
this one fixes, for the update-safety plane, what happens **between** the phases and what each line of a
commit proves. Rules TO1–TO8, their quotes, the host derivation and the boundaries:
`corpus/knowledge/pacman-transaction-order-r39.md`
(sources S208 `hook.c`, S213 `add.c`, S214 `sync.c`, S215 `remove.c`, S216 `util.c`, S217 `trans.c` — S217
supersedes S210's anchor — plus S218, the frozen capture `.ufo/waves/round-39/frozen/txcapture/`, MANIFEST
sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4`; libalpm snapshots
`.ufo/waves/round-39/frozen/src/`, digests in `SHA256SUMS`; pacman 54d9411). Detection and report only:
nothing here authorizes a package, hook or transaction action.

Where the lines sit in one transaction (TO1, TO2, TO3, TO6, TO7; S217, S214, S213, S215):

```
[PACMAN] Running '<command>'                 the frontend opens the window
[ALPM] running '<pre-hook>'...               PreTransaction: before the commit exists
[ALPM] transaction started
[ALPM] removed <pkg> (<ver>)                 sync commits only: conflicts/replacements go first
[ALPM] upgraded <pkg> (<old> -> <new>)       one target at a time, in transaction order
[ALPM] transaction completed                 or interrupted / failed: no Post hook then
[ALPM] running '<post-hook>'...              PostTransaction: hook files re-read from disk
```

Measured from the frozen copy (S218, captured 2026-10-26T05:42:12Z; `pacman.log` mtime 2026-10-25
13:12:06): 86 `Running` windows, 60 `transaction started`, 60 `transaction completed`, 0
`interrupted`/`failed`; 59 `running` lines before a `started` line, **0** between `started` and
`completed`, 236 after a `completed`; 441 `[ALPM-SCRIPTLET]` lines, 189 inside a commit and **252**
outside; 28 `removed` lines and 0 windows that both remove and add. That is a snapshot, not current state.

### Symptom → rule → read-only check → operator action

| Symptom (verbatim string or log shape) | Rule | Meaning | Read-only check | Suggested operator action (tsukuroi does not run it) |
|---|---|---|---|---|
| `[ALPM] running '<hook>'...` lines appear before the same window's `transaction started`, and none between `started` and `completed` | TO1 (S217 `trans.c:201-208`) | Both phases are separate calls outside the commit: Pre at `:202` with `RET_ERR(… ALPM_ERR_TRANS_HOOK_FAILED …)`, `transaction started` at `:208`, Post at `:238` after `transaction completed` at `:235`. A Pre `running` line is never part of the commit | `awk` the window between two `Running` lines and count `running` lines on each side of `started` | None — expected shape |
| A `running '<hook>'...` line falls **inside** a commit (between `started` and `completed`/`interrupted`/`failed`) | TO1 (S217 `trans.c:230-241`) | No single pacman process writes one there at 54d9411: it is a Post hook of an earlier window, a second concurrent pacman writing the same log, or a spliced log | Compare its timestamp with the window's `completed` line; `pgrep -a pacman`; baseline: 0 in 60 (S218) | None for the system; record the window as a log-anomaly finding, never as a third hook phase |
| `error: failed to commit transaction (failed to run transaction hooks)` and **no** `transaction started` for that attempt | TO1 (S217 `trans.c:201-204`) with HO5 above | The Pre pass returned at `RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1)` before `STATE_COMMITTING`, so no target was committed and the Post phase does not exist. The validating `[E] …hook…` line is stderr-only | Read forward from the last `Running '<cmd>'`; `ls /var/lib/pacman/db.lck` (absent = no frontend left holding the lock) | Fix or remove the named hook file; the operator re-runs the transaction |
| One sync window holds both `removed` and `installed`/`upgraded` lines | TO2 (S214 `sync.c:1340-1354`) | `_alpm_remove_packages(handle, 0)` at `:1345` runs before `_alpm_upgrade_packages` at `:1354`, so every `removed` line precedes the first add | Per-window `awk`; baseline: 0 of 60 windows has both, and all 28 `removed` lines sit in removal-only windows (S218) | None. An add line before a removal line inside one window is a log anomaly, not a pacman ordering |
| `[ALPM-SCRIPTLET]` lines sit between a package's own `installed`/`upgraded` line and the next package's line | TO3 (S213 `add.c:616-648`, `:669-688`) | Per target: `pre_install`/`pre_upgrade` from the package file (`:466-474`), files and db entry, the `installed`/`upgraded` line (`:618`, `:630`), then `post_install`/`post_upgrade` from the local db's `install` file (`:641`, `:644-645`). Output before the line is the pre half, after it the post half | Adjacency in the window — exemplar `.ufo/waves/round-39/frozen/txcapture/pacman.log:123-124`: `installed systemd (261.1-1)` then `Initializing machine ID from random generator.` — and `stat` the local `install` file | Name the half before proposing a fix: a post-scriptlet failure comes **after** the files and the db entry were written |
| An upgrade scriptlet takes the wrong branch on a version comparison | TO4 (S213 `add.c:470-474`) | Upgrade scriptlets get `newpkg->version` first and `oldpkg ? oldpkg->version : NULL` second (`:472-473`); install scriptlets get the new version only. `$1` is new, `$2` is old | Read `/var/lib/pacman/local/<pkg>-<ver>/install` (read-only; observed `-rw-r--r-- root root` on `/var/lib/pacman/local/systemd-262-1/install`) and how it uses `$1`/`$2`; libalpm supplies the arguments, so the log never shows them | Fix the scriptlet (package update or local rebuild); never infer the arguments from log order |
| A hook shipped by a package installed **in the same transaction** never shows `running '<name>'...` in that transaction's Pre phase | TO5 (S208 `hook.c:540,554`) | `_alpm_hook_run` re-opens each directory on every call (`opendir` at `:554` inside the `alpm_list_last` loop at `:540`), so the Pre scan ran before the package wrote the file. It can still run in the **Post** phase of the same transaction, which re-reads the directories. Host: 17 Pre hooks are owned by a package the capture shows first installed in some transaction, and none ran in that transaction's Pre — consistent, not proof | `pacman -Qo /usr/share/libalpm/hooks/<name>`; grep the window for `installed <owner>`; `grep -n "running '<name>'"` around the window; `hook-owners.tsv` and `hook-when.tsv` in the capture dir | None if its triggers did not match either; a hook that must act before install has to be installed earlier |
| `[ALPM] transaction interrupted` closes a window (no `transaction completed`) | TO6 (S213 `add.c:676-692`) with HO6 above | A target failed to commit: `trans->state = STATE_INTERRUPTED` and `skip_ldconfig = 1` (`:679-682`), so `ldconfig` is skipped (`:689-691`), later targets are not attempted (`:673-675`), `transaction interrupted` is logged (`trans.c:231`) and the Post phase is skipped (`trans.c:238` sits in the `else`). Targets committed before the failure stay installed | The window's last lines; `stat -c '%y' /etc/ld.so.cache` against the window timestamp; `pacman -Q <targets>` for what landed; Post `running` lines absent | The operator re-runs the transaction; after a kernel update, treat the boot artefacts as skewed until a Post hook really runs |
| `[ALPM] transaction failed` closes a window | TO1 (S217 `trans.c:211-228`) | The commit call itself failed (`_alpm_remove_packages` or `_alpm_sync_commit` returned -1), `transaction failed` is logged at `:216`/`:224` and the function returns before the Post phase, so Post hooks do not run. Whether `ldconfig` ran depends on how far the commit got | The line before the failure; the stderr `error: failed to commit transaction (…)`; `pacman -Q <targets>` | Read the stderr class; partial commits are possible because targets commit one at a time |
| A `removed <pkg> (<ver>)` line for the **old half of an upgrade**, or a removal with no `pre_remove`/`post_remove` output | TO7 (S215 `remove.c:699-733`) | `removed %s (%s)` is logged only in `_alpm_remove_single_package` (`:722`); the old version of an upgrade is replaced inside `commit_single_pkg` with neither scriptlet nor log line. A removal that prints nothing simply has a silent or absent scriptlet | `pacman -Q <pkg>`; if it is still installed, the line belongs to another window or another run | Count removals by `removed` lines only; never read an `upgraded` line as a removal |
| `[ALPM-SCRIPTLET]` text appears after `transaction completed`, or outside every commit window | TO8 (S216 `util.c:521-528`; hook path S208 `hook.c:525-528`) | `_alpm_chroot_process_output` logs **every** line a chroot child prints under that tag — Post hooks, Pre hooks, install scriptlets and `ldconfig` alike (`:527`); the tag does not mean "install scriptlet". Host: 252 of 441 tag lines lie outside a commit phase, so they are hook or `ldconfig` output | The nearest preceding `running '<name>'...` names the printing hook; inside a commit, tag lines after the last package's own post-scriptlet output occupy the `ldconfig` slot (`:689-691`) — content decides, the tag does not | Attribute the text to the hook above it; never quote it as the last package's install scriptlet |

### Limits of this table

- **No transaction was run or read live.** Every count above is the frozen copy S218 (captured
  2026-10-26T05:42:12Z; `pacman.log` mtime 2026-10-25 13:12:06), so no row reports current host state.
- **TO2 has no host instance** (0 of 60 windows removes and adds): its row is a shape test that may never
  fire here.
- **TO5's host column is consistency, not proof, for 16 of 17 instances**; one (`10-limine-snapper-lock.hook`,
  pacman.log:1344-1348, control :2130-2132) does discriminate and agrees with TO5 (`pacman-transaction-order-r39.md`,
  "Round-39 wave-1 correction").
- **`[ALPM-SCRIPTLET]` proves one thing only**: a chroot child printed that line — not which child, not
  success, not that anything was installed.
- **Time zones differ.** `pacman.log` stamps `+0000`; `stat` prints local time (`-0300` here). Convert
  before comparing an `/etc/ld.so.cache` mtime with a window — and note the cache mtime is no proof that a
  transaction's `ldconfig` ran: observed 2026-10-26, the cache is `2026-10-25 13:36:22 -0300`, 24 minutes
  after the frozen log's last write (`13:12:06`), because any tool may run `ldconfig`.
- **A missing log line is weak evidence** — libalpm's parent-side validation and exec errors stay on stderr;
  a hook's own stdout and stderr do reach `pacman.log` as `[ALPM-SCRIPTLET]` (TO8; `util.c:665-666`).
- **The counter checks citation, not truth**: `check-transaction-order-r39.py` verifies that each TO quote
  sits at its cited lines on a mined upstream row. A review seat that judges a TO row FALSE against the
  pinned source kills the entry (round-39 declaration, QUALITY 81).

Counting: `python3 tools/check-transaction-order-r39.py --revision <REV> [--repo <PATH>]` — 0 when every
TO1–TO8 quote is at its cited lines on a mined upstream row named on `source:`, no duplicate row or
heading, both host counts reproduce and 0 `running` lines fall inside a commit phase; 1 when any of those
fails; 2 on revision, git or tampered-input failure. Round 38's `tools/check-hook-order-r38.py` scores the
hook entry, not this section, and is not re-run here.

## Historical instrument pins — round 39

Appended 2026-10-26 (round-39 routed defect 6, seat RoutedHistorical). Append-only: every earlier row and the
two prose consumer notes (`SKILL.md:3147-3149`, `SKILL.md:3221-3224`) stay as written. Both of those notes say
"after `52ffd65`" and "after `49cc53c7`"; measured, both boundaries are **inclusive** — each instrument
already fails at the commit named. This section starts with its own heading, so it sits outside the operative
registry section and the highest-table selector is unchanged; the two rows restate the instruments as
historical readings, pinned to the census revision each must be read at. A revision outside a pin is an
out-of-window reading, not a regression.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| historical-pacnew-arm-r35b | probe | `python3 tools/score-pacnew-arm-r35b.py --lane <repo> --revision <REV> [--skip-battery]` | inside the pin only: 0 candidate and control match every view and no should-fail arm is accepted;1 otherwise;2 harness error | the battery itself (control arm plus 17 should-fail arms) | HISTORICAL. Read only where `tools/tsukuroi-census.sh` is blob `10b6d47046c9523bfeefd56c76a06ecc59ea5e01`: `e2f97e6e4beaadda8e1d5ae7bd08baa0e82d61e0` (the arm lands) through `7cbaeb6317cb9f7323d2619eec02db4e4da29449` (`52ffd65^`). Measured skip-battery 24 of 24, `harness_errors` empty, exit 0 at `e2f97e6e` and at `7cbaeb63`. Not a reading at the claim base `b40c01df38eb26f74c095c471efc6d1649b00fd4`: 0 of 24, all 24 `drift_lines=0` — the base is the parity reference and predates the arm; at `52ffd65f868431f021b8615ab281efd87195eac6` and `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` it reads 4 of 24 with `base parity` on all 20 stub views, exit 1 (battery mode at `52ffd65`: candidate 4, control 24, `should_fail_accepted` 0 of 17). Cause: the round-38 `STORAGE` line is a non-DRIFT line that `judge()` compares with the claim base (`tools/score-pacnew-arm-r35b.py:426-433`), and the census prints it after `DRIFT pacnew-plane` (`tools/tsukuroi-census.sh:3077`, line numbers at the measured tip `394e1ba4fab39a417abe66a7802f87cf1ff8dd61`) | private temp fixtures; unprivileged user+mount namespace; live view reads /etc names and pacman.log read-only | tsukuroi |
| historical-storage-arm-r38-f06 | gate | `python3 tools/score-storage-arm-r38.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | inside the pin only: 0 ten fixtures, the live leg and six PLANE lines per run match;1 any fixture, the live leg or the plane count differs;2 revision, git or bash could-not-evaluate | none: the ten built-in fixtures F01-F10 and the live leg are the measurement | HISTORICAL at fixture `F06-no-btrfs-root` only. Read only where `tools/tsukuroi-census.sh` is blob `119b645349b5eadf182aaa473d2fac38eadea45a` (`52ffd65f868431f021b8615ab281efd87195eac6`, the arm lands) or `8ef604c001ae2b2edc1598a6dd3877f30dc13de5` (`02eeed07f1c9142a037cab9cd40161feebc3ca67`, hardening; `b0005ae9f56fd5a006fc5ec026578c88e2b64b26` reads the same blob), i.e. `52ffd65 <= REV < 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82`: measured PASS 10 of 10, `live_match` 1, `six_planes_all` 1, exit 0 at `52ffd65`, `02eeed07` and `b0005ae9`. F06 is superseded by the round-39 absent-root rule in the section above (commit `49cc53c7`): it declares an absent override root clean as `('HEALTHY', 0, 0, 0)` (`tools/score-storage-arm-r38.py:82`) while its census environment sets only `TSUKUROI_BTRFS_SYSFS` and never `TSUKUROI_PROC_MOUNTS` (`:154-160`), so the default `/proc/self/mounts` is read and this host's four btrfs mounts make the post-rule arm print `BLOCKED ... detail=mounts:btrfs-without-sysfs` (`tools/tsukuroi-census.sh:1906-1914` at the measured tip). Measured at `49cc53c7` and at `394e1ba4`: 9 of 10, F06 expected `HEALTHY` got `BLOCKED`, exit 1, with `live_match` 1 and `six_planes_all` 1 still holding — the failure is F06 alone, by construction. The absent-root case is scored now by `storage-hidden-r39` (hidden legs H1/H2) | private mkdtemp fixtures under `--scratch`/`TMPDIR`; reads the census at REV through git; no host write | tsukuroi |

## Corrections from the transaction order — round 39 (append-only)

Appended 2026-10-26 (round-39 C2, wave seat C2ScoutCorrections, verified by the L1 against
`.ufo/waves/round-39/frozen/src/util.c:527`, `:665-666` and the frozen pacman.log). The rows they qualify stay as written.

- To the round-38 hook-order limits bullet "Silence in `pacman.log` is weak evidence" (section "Hook order — round 38"): Round-39 correction (TO8): the line list above is incomplete — every line a hook prints, stdout and stderr, and the child-side text of an exec or chroot failure reaches `pacman.log` as `[ALPM-SCRIPTLET]` (`util.c:527`, `:666`, `:700`) under the hook's `running '<name>'...` line; only libalpm's own parent-side errors (`command failed to execute correctly`, dependency and validation errors) stay on stderr, so a hook that fails before it prints anything still leaves no log line.
- To the round-38 HO6 row ("Meaning" cell): Round-39 correction (TO8): a failed Post hook's exit status is dropped and libalpm's failure message is stderr-only, but any text the hook printed is in `pacman.log` as `[ALPM-SCRIPTLET]` lines after its `running '<name>'...` line (`util.c:527`); look there for the cause.
- To the round-19 boot-writer rows that call the limine lines "ALPM-SCRIPTLET events" (section above at the
  `r19b:1695` window total and the writer-table `ALPM-SCRIPTLET] Copied: …` row): Round-39 clarification (TO8, TO1): `[ALPM-SCRIPTLET]` is the log tag for every line libalpm's chroot children print — hooks, install scriptlets and `ldconfig` — not a marker of an install scriptlet; the three events (pacman.log 2021, 3015, 3047) are PostTransaction-hook output: each lies after `transaction completed` and after its transaction's `running '90-mkinitcpio-install.hook'...` line (frozen capture lines 1950/1989/2021 and 2941/2983/3015, 3047). That the hook is `90-mkinitcpio-install.hook` rests on the `running` header line preceding the output, and its Exec on the hook file; the tag itself identifies neither.

## Storage arm selftest literal variation — round 40

Appended 2026-10-26 (round-40 C1, commit `c707e356c2911646f7304d706eb77d118e510610`). Append-only: the round-38
and round-39 storage-arm sections above stay as written, and the arm itself — `probe_storage_arm`,
`tools/tsukuroi-census.sh:1865-1925` — is untouched. The commit is `1 file changed, 36 insertions(+)` in
`run_selftest` only (`git diff --stat 53b294a2 c707e35 -- tools/tsukuroi-census.sh`), so no earlier label or expected
line moved and the selftest count goes 119 → 124 (`PASS (124 cases, 124 passed, 0 failed)`).

Round 39 closed R38-ABSENT-ROOT but left R39-FIXTURE-MONOCULTURE: every "btrfs mounted" fixture in that selftest was
the one string `/dev/mapper/root / btrfs rw,noatime,subvolid=256,subvol=/@ 0 0`, so any arm keyed on a literal of it
passed 117/117 (`.ufo/waves/round-39/w1/C1CritControl.md` VA, VB, VC, VG; `C1MutParse.md` (a), (b);
`C1MutCrossCheck.md` (e)). The five cases below vary the btrfs line itself — device, mountpoint, options, subvolume,
its position in the table and the case of the fstype field — and add one unlistable root with btrfs mounted. Each
fixture writes its own `$FX/mounts`; `check()` exports it as `TSUKUROI_PROC_MOUNTS="$FX/mounts"`
(`tools/tsukuroi-census.sh:2166`), so the arm's mount-table cross-check reads the fixture, never the host's table.

| Case (`tools/tsukuroi-census.sh`) | Mount table (`$FX/mounts`, one line each) | Expected `STORAGE` line | Frozen mutants it kills |
|---|---|---|---|
| `storage-mounts-varied-home` (`:3011-3016`)<br>"a btrfs /home on another device and options, not last, is BLOCKED (R40-C1)"<br>*pins: device, mountpoint, option order, `subvolid=5`/`subvol=/`, middle position* | `proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0`<br>`/dev/nvme0n1p3 /home btrfs rw,relatime,ssd,discard=async,space_cache=v2,subvolid=5,subvol=/ 0 0`<br>`tmpfs /tmp tmpfs rw,nosuid,nodev 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | M1, M2, M4, M8, M9 |
| `storage-mounts-varied-multi` (`:3018-3024`)<br>"one read-only btrfs mount among four lines, empty root, is BLOCKED (R40-C1)"<br>*pins: `ro`, `compress=zstd:3`, named subvolume `/machines`, 4-line table, not root; root holds only `features`* | `sysfs /sys sysfs rw,nosuid,nodev,noexec,relatime 0 0`<br>`UUID=0b1c /boot vfat rw,relatime 0 0`<br>`/dev/sda2 /var/lib/machines btrfs ro,noatime,compress=zstd:3,subvolid=263,subvol=/machines 0 0`<br>`/dev/sdb1 /srv ext4 rw,relatime 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | M1, M2, M4, M8, M9 |
| `storage-mounts-btrfs-in-path` (`:3026-3030`)<br>"btrfs in the device, mountpoint or options of an ext4 line is no btrfs mount (R40-C1)"<br>*pins: only the fstype field decides* | `proc /proc proc rw 0 0`<br>`/dev/disk/by-label/btrfs-old /mnt/btrfs-backup ext4 rw,relatime,comment=btrfs 0 0` | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` (no `detail`) | M3, M5 |
| `storage-mounts-fstype-case` (`:3032-3035`)<br>"the fstype match is exact, so BTRFS is not btrfs (R40-C1)"<br>*pins: case-sensitive field equality* | `proc /proc proc rw 0 0`<br>`/dev/fx0 / BTRFS rw,relatime 0 0` | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` (no `detail`) | M6 |
| `storage-root-unreadable-mounted` (`:3037-3043`)<br>"an unlistable root keeps its one reason; the mount table is never added (R40-C1)"<br>*pins: guard order — an already-BLOCKED root never consults the table, one reason only* | `proc /proc proc rw 0 0`<br>`/dev/vdb /data btrfs rw,relatime,subvolid=5,subvol=/ 0 0`<br>root `$FX/btrfs` holds one device `devinfo/1/error_stats` of five zero counters, then `chmod 000 "$FX/btrfs"` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=root:unreadable` | M7 |

Mutant ids are the counter's own frozen names (`tools/score-selftest-literals-r40.py:68-81`): M1
`M1-VA-device-literal` (`*'/dev/mapper/root'*`), M2 `M2-VB-root-mountpoint` (`*' / btrfs '*`), M3
`M3-VC-substring-btrfs` (`*btrfs*`), M4 `M4-VG-subvolid-256`, M5 `M5-a-grep-count` (`grep -c btrfs`), M6
`M6-b-fstype-casefold` (`${fst,,}`), M7 `M7-e-guard-drops-blocked` (the guard loses `&& [ "$blocked" -eq 0 ]`), M8
`M8-subvol-at-literal` (`subvol=/@`), M9 `M9-last-line-only` (`tail -n 1`). The Kills column's union is all nine; three
cases are each the only killer of something — `btrfs-in-path` kills M3 and M5, `fstype-case` kills M6,
`root-unreadable-mounted` kills M7 — while the two varied cases kill five each, because both put btrfs on a non-root
mountpoint of a device other than `/dev/mapper/root` with `subvol=/` or a named subvolume.

Counting: `python3 tools/score-selftest-literals-r40.py --revision <REV> --scratch <DIR> --jobs 2` — 0 when
`baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0 and selfref == 5`
(`tools/score-selftest-literals-r40.py:28-29`; the same sentence is in the round-40 declaration and in the receipt);
1 otherwise; 2 on revision, git or scratch failure. A mutant is applied only when its exact `old` substring occurs
once, the three neutral rewrites N1–N3 must PASS inside the same run (so a selftest keyed on the arm's own text fails
them), and `selfref` must stay 5. Measured at `c707e35`: baseline `PASS (124 cases, 124 passed, 0 failed)`, neutral
3/3, mutants applied 9/9, survivors 0, selfref 5, exit 0 (`.ufo/waves/round-40/after/c1-after-c707e35.jsonl`; per-mutant
failed-case counts 2,2,1,2,1,1,1,2,2). At the base `53b294a2`: baseline `PASS (119 cases, 119 passed, 0 failed)`,
survivors 9, exit 1 (`.ufo/waves/round-40/before/c1-before.jsonl`).

Equivalent mutant, excluded and named in the counter (`:23-25`): the guard `$fsn` → `$devn`
(`if [ "$devn" -eq 0 ] && [ "$blocked" -eq 0 ]`, round-39 `C1MutCrossCheck` (d)). `devn > 0` implies `fsn > 0`, since a
device is counted only inside an fsid directory, and `fsn > 0` with `devn == 0` sets `blocked=1` (`no-devinfo`) before
the guard — so no fixture can kill it. Applied anyway at `c707e35` it still prints `PASS (124 cases, 124 passed,
0 failed)`: the expected result for an equivalent mutant, not a survivor.

### Limits of these five cases

- **Mutant sample, not proof of immunity.** All nine mutants rewrite one thing, the mount-table cross-check of the
  round-39 rule. The sysfs walk, the five-counter parser, `bad-devid`, `no-devinfo` and the `root:unreadable` paths
  carry no mutant here, and a literal the fixtures happen to share (`ssd`, `space_cache=v2`, `rw,relatime`) is
  unprobed. `survivors == 0` means 0 of these nine, never "no literal-keyed arm can pass".
- **Fixtures and mutants were written in the same round.** A mutant the author did not imagine stays invisible; the
  sample is nine arms carried from round 39, three neutral rewrites and one excluded equivalent.
- **`BTRFS` is a forged input, not a host shape.** Linux reports this field lower-case, so `storage-mounts-fstype-case`
  pins exact-match semantics against a table the kernel will not produce; the `comment=btrfs` option and the
  `/dev/disk/by-label/btrfs-old` device name in `btrfs-in-path` are forged too. These cases prove that only the third
  field decides — not that a real host ever shows such a line, and not what the arm would do with another spelling.
- **One line shape per case.** No fixture holds two btrfs mounts, a mountpoint with an escaped space (`\040`), a field
  count other than the six `mount` prints, or a btrfs line in a table whose root already has fsid entries. Position is
  varied only within 3–4 line tables.
- **Fixtures only.** All five tables are override files; no run reads the host's table, so this section says nothing
  new about the live host (round 39's live reading stands).
- **The receipt carries counts, not labels.** The counter scans stdout for `^FAIL `
  (`tools/score-selftest-literals-r40.py:106`) while the selftest's `bad()` writes `FAIL <label>` to stderr
  (`tools/tsukuroi-census.sh:2019`), so every `first_fails` is empty. The Kills column was measured by applying the
  counter's own frozen `MUTANTS`/`NEUTRAL` tables to `git show c707e35:tools/tsukuroi-census.sh`, running each variant
  `--selftest` and capturing stderr; the per-mutant failing-case counts reproduce the receipt's. Re-derive a row the
  same way, or delete one case block on a scratch clone and watch which mutants survive.
- **bash only.** The selftest runs under GNU bash (`5.3.20` here); `[[ ]]`, `${fst,,}` and `case` globbing are bash
  semantics, so N2 and M6 are bash-specific.

### Counter sufficiency — what the round-40 wave found (appended by the L1)

The frozen C1 counter's PASS at `c707e35` is real (re-run by seats C1ExecRerun, C1RevCounter, C1CritAxis), but it is
not proof that the selftest discriminates: a one-line selftest prologue that reads the arm's parsed text with
`declare -f probe_storage_arm`, or its own file through `${0}` or `${BASH_ARGV0}`, and fails on the mutants'
replacement strings scores `survivors 0` with no new fixture — `SELFREF_RE` sees none of the three spellings
(`.ufo/waves/round-40/w1/C1CritControl.md`, variants C1-CHEAT-A/B/C, each a PASS receipt in that seat dir). Held-out
mutants keyed on an absolute mountpoint, a `/dev/` source or a `subvol=` option survive the 124-case selftest
(`C1HeldOutMutants.md` H5, H6, H9); each corresponds to a property every kernel-produced btrfs line has, so they are
near-equivalent on the real input domain, and M6 (case-folded fstype) is killed only by a forged `BTRFS` table
(`C1CritEquivalence.md`). The counter's `first_fails` is always empty because `bad()` writes to stderr. A round-41
amendment owes: a selfref guard over the executed selftest (not a regex over its text), a stderr-capturing receipt,
and the held-out mutants as frozen should-fail arms.

## Hook and scriptlet execution environment — round 40

Appended 2026-10-26 (round-40 C2; drafted by wave seat C2ScribeSkill, integrated by the L1). The
round-38 table above orders the hooks **inside** one phase (HO1–HO7) and the round-39 one fixes what
happens **between** phases (TO1–TO8); this section answers the narrower question for the update-safety
plane: what a hook `Exec` command or an install scriptlet **finds when it starts** — working directory,
streams, environment, interpreter, staged scriptlet file, stdin, `Depends`, and the paths a `Path`
trigger matches. Rules EX1–EX8 and their quotes: `corpus/knowledge/pacman-exec-environment-r40.md`
(source: S219–S225 — pacman `54d9411` `meson_options.txt`, `util.c`, `trans.c`, `hook.c`,
`alpm-hooks.5.asciidoc`, the Arch `PKGBUILD` at `7.1.0.r9.g54d9411-3`, and an own-work host capture;
snapshots `.ufo/waves/round-40/frozen/src/`, digests in `SHA256SUMS`; capture
`.ufo/waves/round-40/frozen/hostcap/`, MANIFEST sha256
`57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5`). Every row cites the EX id and the
pinned source line it rests on. Detection and report only: nothing here authorizes a package, hook or
transaction action, and no hook or scriptlet was executed for it.

Measured on this host, 2026-10-26, read-only: `pacman 7.1.0.r9.g54d9411-3`; `pacman-conf RootDir` → `/`;
`pacman-conf HookDir` → `/etc/pacman.d/hooks/`; 67 hook files in `/usr/share/libalpm/hooks` plus 3 in
`/etc/pacman.d/hooks`, 69 effective after one same-name override, 14 of them carrying `NeedsTargets`;
`strings /usr/lib/libalpm.so.16.0.1` lists `/usr/bin/bash` and not `/bin/sh`; `pacman.log` holds 295
`running '…'` lines, 0 `could not satisfy dependencies` and 0 `could not create temp directory`; `/tmp`
is a separate xfs filesystem (`/dev/nvme1n1p1`,
`rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota`), mode `1777 root:root`, 125G free,
67M free inodes (1% used), 0 leftover `alpm_*` directories; `pacman-conf NoUpgrade` prints nothing (no
`NoUpgrade` line in `/etc/pacman.conf`); `/bin/sh` is a symlink to `bash` 5.3.20. These are probes, not
a transaction: none of them observes a hook or scriptlet running.

### Symptom → EX row → check → command

| Symptom (verbatim string or observation) | Rule (EX id, pinned line) | What it means | What to check | Command (read-only, paste-ready) | Suggested operator action (tsukuroi does not run it) |
|---|---|---|---|---|---|
| `Exec = /usr/bin/ldconfig -r .` (`11-glibc-ldconfig.hook:36`), or a hook/scriptlet writes a file the operator finds at `/`, or misses one it expected beside itself | EX1 (`util.c:628`, `:683`) | Every `_alpm_run_chroot` child — hook `Exec`, install scriptlet and `ldconfig` — starts in `/` of the installation root; `.` and bare names resolve there, not in the shell that ran pacman. Here the parent's `chdir` lands on `/` and no `chroot()` call happens | Is any path in the `Exec` or the scriptlet relative? `RootDir` (here `/`), so the host's `-r .` means `-r /` | `pacman-conf RootDir; grep -n 'ldconfig -r \.' /usr/share/libalpm/hooks/*.hook` | Make the path absolute in the hook or scriptlet; do not add a `cd` and expect it to survive — the child sets `/` itself |
| A `[ALPM-SCRIPTLET]` line cannot be split into stdout and stderr; an error line has no tag of its own | EX2 (`util.c:665-666`; tag at `util.c:527`) | One socket carries both streams merged; the only attribution is the `running '<name>'...` line above the text | The nearest preceding `running` line; whether the child printed anything at all | `awk '/\[ALPM\] running /{h=$0} /\[ALPM-SCRIPTLET\]/{print h; print}' /var/log/pacman.log \| tail -6` | Attribute the text by the hook header; read the merged order as arrival order, not program order |
| A hook whose `Exec` reads stdin (`while read -r f`, `cat`) loops zero times, or a `NeedsTargets` hook gets a list shorter than its trigger matches | EX6 (`hook.c:519-526`; feed `:469-490`, newline `:476`; `alpm-hooks.5.asciidoc:91-93`) with EX2 (`util.c:667`, `:722-726`) | Without `NeedsTargets` the parent closes the child's stdin at once, so the child reads end-of-file; with it the matched targets arrive sorted (`strcmp`), de-duplicated, one per line | `NeedsTargets` present? does the `Exec` read stdin? host: 14 effective hooks carry it, e.g. `texinfo-install.hook:10-11` | `h=/usr/share/libalpm/hooks/texinfo-install.hook; grep -n '^NeedsTargets' "$h"; grep -n '^Exec' "$h"` | Add `NeedsTargets` for a stdin-reading `Exec`; otherwise remove the read — it always sees EOF |
| `running '<hook>'...` in the log, the hook's effect absent, and no `unable to run hook …` line anywhere | EX7 (`hook.c:507-517`; `running` at `:653`, call at `:660`; abort `:660-668`) | The `running` line is written before `Depends` are checked; a missing `Depends` skips the command **after** the line is written and the error goes to stderr only; only a Pre `AbortOnFail` hook turns that skip into a transaction abort (0 such hooks here) | `Depends` against the local db; `When`; `AbortOnFail`; the stderr-side error count (0 in the live log) | `h=/usr/share/libalpm/hooks/10-glibc-locale-gen.hook; grep -n -e '^Depends' -e '^When' -e '^AbortOnFail' "$h"; for p in $(sed -n 's/^Depends = //p' "$h"); do pacman -Q "$p"; done; grep -n "running '$(basename "$h")'" /var/log/pacman.log \| tail -3; grep -c 'could not satisfy dependencies' /var/log/pacman.log` | Install the dependency or drop the `Depends` line; never read a `running` line as proof of execution |
| An install scriptlet dies with `syntax error near unexpected token`, `[[: not found` or `Syntax error: "(" unexpected` | EX4 (`trans.c:357`, `:410`; `PKGBUILD:115`; upstream default `meson_options.txt:17`) | Arch's libalpm runs a scriptlet as `/usr/bin/bash -c '. <scriptlet>; <function> <new> [<old>]'`; upstream's build default is `/bin/sh`. A hook `Exec` is not a scriptlet: libalpm execs `cmd[0]` directly (`hook.c:526`, `:528`), so a hook's shell is the one its `Exec` names | The installed libalpm's compiled-in shell string; whether the failing text lives in a local-db `install` file or in a hook `Exec` | `pacman -Q pacman; strings /usr/lib/libalpm.so.16.0.1 \| grep -Fx -e /usr/bin/bash -e /bin/sh; grep -nE -e '\[\[' -e '<<<' -e '\bfunction [a-zA-Z_]' /var/lib/pacman/local/systemd-262-1/install` | Keep bash-only syntax only where bash is the runner; a hook that needs it must name `bash -c`. `/bin/sh` is bash here, so this failure is a source-level conditional on this host |
| `error: could not create temp directory` in the middle of a transaction, and every scriptlet of that transaction fails | EX5 (`trans.c:361-369`; cleanup `:412-420`) | `mkdtemp("<root>/tmp/alpm_XXXXXX")` failed: `<root>/tmp` is absent and not creatable at 01777, or not writable, out of space or inodes, or read-only. The `tmp/alpm_XXXXXX/.INSTALL` file is never staged, so no scriptlet body runs | `RootDir` to map `<root>/tmp` (here `/`); mount, mode, free space and inodes of that directory; leftover `alpm_*` directories from a failed cleanup | `pacman-conf RootDir; findmnt -T /tmp; stat -c '%a %U:%G %n' /tmp; df -h /tmp; df -i /tmp; find /tmp -maxdepth 1 -name 'alpm_*' -ls` | Restore a writable 1777 `<root>/tmp` with space and inodes, then re-run the transaction; `could not remove tmpdir` in the log means cleanup left a directory behind |
| A `Path` hook's command ran while the file pacman left is `<file>.pacnew` beside an unchanged `<file>` | EX8 (`hook.c:258-279`; `NoExtract` skip `:271`; upgrade and removal sides `:281-306`) | Matching is against the package's file-list name, independent of the extraction outcome: `NoExtract` excludes a path, `NoUpgrade` does not, so a protected file still matches under its listed name | The hook's `Target`; `NoUpgrade` entries (none on this host, so this row is source-level here); the file pair and its mtimes | `pacman-conf NoUpgrade; h=/usr/share/libalpm/hooks/texinfo-install.hook; grep -n '^Target' "$h"; ls -l /etc/pacman.conf /etc/pacman.conf.pacnew 2>&1` | Make the command act on the `.pacnew` or on both files; never assume the old file was replaced |
| A file created by a hook or scriptlet is `0644`/`0755` although the operator's umask is stricter; a variable exported in the operator's shell reaches the command while a `BASH_ENV`/rc-file setting does not | EX3 (`util.c:692-695`, `execv` `:698`) | The child sets `SHLVL=1` when unset, removes `BASH_ENV` and sets umask 0022; every other variable of pacman's environment passes through unchanged | Mode of the created file; the operator's umask (the child's is fixed at 0022); where the variable was set | `stat -c '%a %U:%G %n' /var/log/pacman.log; umask` (substitute the created file) | `chmod` explicitly in the scriptlet; export variables before starting pacman |

### Limits of this table

- **No hook or scriptlet was run** for any row. Pacman transactions are paused on this host; every host
  value above is a read-only probe on 2026-10-26 or the frozen capture S225 (captured
  2026-10-26T06:54:46Z).
- **Correction to the entry's EX5 host cell** (`corpus/knowledge/pacman-exec-environment-r40.md:25`,
  "on this host `/tmp` is a tmpfs"): measured 2026-10-26, `/tmp` is xfs on `/dev/nvme1n1p1`
  (`findmnt -T /tmp`; `/etc/fstab:26`; `systemctl cat tmp.mount` is an fstab-generated xfs mount, not
  the systemd tmpfs). The rule (EX5) is unaffected; use the measured value. With 125G free and 67M free
  inodes, a `could not create temp directory` here would come from permissions or a removed
  `<root>/tmp`, not from exhaustion.
- **EX4 is a source-level conditional on this host**: `/bin/sh` is a symlink to `bash` 5.3.20, so
  bash-only scriptlet syntax does not fail here even under `/bin/sh`. That the shell choice matters is
  visible in the stored scriptlets: 8 of 51 `install` files under `/var/lib/pacman/local/` carry
  `[[`/`function` (`systemd-262-1/install:4`, `:76`).
- **EX8 has no host instance**: `pacman-conf NoUpgrade` prints nothing and `/etc/pacman.conf` has no
  `NoUpgrade` line, so the `.pacnew` row is source-level here. A `.pacnew` written from a package's
  `backup` list was not traced in this entry.
- **A `running` line without effect has more than one cause.** Check EX6 before EX7 when the `Exec`
  reads stdin: a silent command, an EOF read and an unmet `Depends` all leave the same log shape. The
  stderr-side `unable to run hook …` error is the only discriminator for the `Depends` case.
- **`[ALPM-SCRIPTLET]` proves one thing only**: a chroot child printed that line — not which child, not
  success (TO8).
- **A missing log line is weak evidence**: libalpm's parent-side validation and exec errors stay on
  stderr.
- **The counter scores the entry, not this section.** `exec-environment-r40` (gate registry,
  `SKILL.md:3119`) verifies the EX1–EX8 quotes against the pinned snapshots and two host values from the
  frozen capture (the 14/69 `NeedsTargets` count and the `/usr/bin/bash` string); it does not read this
  table, and it does not check the `/tmp` value above.

Counting: `python3 tools/check-exec-environment-r40.py --revision <REV> [--repo <PATH>]` — 0 when
EX1–EX8 each carry the source-derived value, the frozen proposition tokens and no negation word, a
4–25 word quote at the cited lines on a new mined upstream row, no duplicate row or heading, both
capture-derived host values, and 0 base hits of the novelty tokens; 1 when any of these fails; 2 on
revision, git or frozen-input failure. Frozen sha256
`d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`.

## Counter lineage — rounds 35-40

Appended 2026-10-26 (round-40 wave 1, seat ConsiderLineage; `considerthese/2026-10-25.md` proposal "Probe lineage
table", item F-5). Append-only: no earlier section, row or prose is changed. It complements
`corpus/lessons/round-38.md:109-130`, which holds the child-env probe's VERSION 1-8 lineage and its amendment digests,
with the claim counters of rounds 35-40 and with the digest-at-freeze-commit method.

Method, one row at a time, from the lane root:
`C=$(git -C <lane> log --diff-filter=A --format=%h -- <tool>)` names the commit that first carried the tool;
`git -C <lane> show $C:<tool> | sha256sum` gives the digest. A digest below is therefore the tool's bytes at the
commit that first carried it. Where the lane later froze different bytes (an amendment or an operative revision), the
row names those revisions and their digests as well, because a digest that is not the frozen one leaves the freeze
unverifiable (the round-37 routed defect).

A `git log --all -- <tool>` read also lists commits with empty descriptions that are **not** ancestors of `master`
(`git merge-base --is-ancestor` exits 1) and carry a blob byte-identical to a master commit's version of the same file
(measured: two such commits beside the round-40 pair, five beside `tools/check-btrfs-space-r30.py`; `689eeab` and
`a447b67` both hold `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159` for the round-40 C1 counter). The
lineage below is the master ancestry, not the union of all refs; an extra hash there is a snapshot, not a divergence.

Scope: every claim counter frozen in rounds 35-40 — `tools/score-*-r3*.py`, `tools/check-*-r3*.py`,
`tools/probe-*-r3*.py`, the two round-40 counters — plus `tools/check-journalctl-v262-corrections.py`, a round-37
claim counter the globs do not match. The second table carries the eight r3\* files frozen in rounds 30-34, so a reader
who follows the globs finds them here instead of concluding they do not exist.

| # | Counter | Frozen in | First-carrying commit | sha256 at that commit | What it measured | Retired or qualified by |
|---|---|---|---|---|---|---|
| 1 | `tools/score-pacnew-arm-r35.py` | r35 | `6b4561e43e15c1cce038e390ad7d4691b0af4cc8` | `19d25d14f9ee6ad15c036c75f997f2fba7aa756779c9e3b70a0ff136297e0155` | VERSION 1: 24 fresh-seeded fixtures (`TSUKUROI_ETC_DIR` + `TSUKUROI_PACMAN_LOG`) against the census `DRIFT pacnew-plane` line — eight `name=integer` fields plus unchanged fixture bytes, modes and inode change times | Not retired by a verifier: met before any freeze by pre-freeze controls K08FixtureKeyed (keyed on name length) and K15FieldMutants (log reader without a pair check); bytes kept as the failed candidate — `SCORECARD.md:1526-1528`, `SKILL.md:3004` |
| 2 | `tools/score-pacnew-arm-r35b.py` | r35 | `7186722b8eba243439c6724766bdae2ef13c595c` | `7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1` | VERSION 2: 20 stub views, 3 namespace views and 1 live view, a correct control arm and 17 should-fail arms (fixture gate, cached live values, name-only pairing, gone by `[ -e ]`, FIFO dropped, word-split paths, date filter) | C1 not verified under the declared kill rule: W2TreeKeyed and W2LogKeyed met it before the change existed — `SCORECARD.md:1553`; unrepaired counter defects (battery misses the ctime check and the live view, arm-audit disagreements, live view compares totals only, receipt reason-string echo) — `SCORECARD.md:1556`; pinned historical, base parity FAILs after `52ffd65` — `SKILL.md:3149`, `SKILL.md:3313`, `corpus/lessons/round-39.md:91` |
| 3 | `tools/probe-child-env-allowlist-r36.py` | r36 | `1e926801195e304950e3eb9d2525ef8bbc245089` | `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` | VERSION 7: the five live tools' child environments on `livefive` — leaking (target, channel) pairs over names, quiet, source and untraced channels, 15 predicate pairs | Retired by its own gaps: S1 clone-branch crash, S3 livefive vacuity, S4 `os.get_exec_path()` silence, parameter-named-`env` source rule — `corpus/lessons/round-36-verifier-spotcheck.md:55-56`, `:102`; the crash reproduced directly — `corpus/lessons/round-37-verifier-spotcheck.md:37`; the source-channel false positive also failed C1 at `c052bb7` — `SCORECARD.md:1823-1825` |
| 4 | `tools/probe-child-env-allowlist-r37.py` | r37 | `29b22df142efb5479333af9d57ecbd069462ba05` | `9aee085b45d7566d6ce398733c10d3d87ae29bce107c4bd13fcdffcb4854b064` | VERSION 8: the same five tools and 15 pairs with the four round-36 fixes, a direct (receipt-free) livefive mode plus the receipt wrapper | Live, not retired: the sensitivity conjunct is unmet (no committed per-fix V8 mutant receipt) — `corpus/lessons/round-37-verifier-spotcheck.md:39`; the only kill ran under V7 — `:40`; a name-level source set cannot see the ambient-PATH family — `:128`; the V8-mutant-per-fix duty is carried, not paid — `corpus/lessons/round-38.md:103` |
| 5 | `tools/check-journalctl-v262-corrections.py` | r37 | `543a7cee2c5119f42023aa72597ce452d4a060d5` | `29fa51da440cb516019ce0b5a5f8fa0efb3aaa4d3d0eea6b830966402fa636d5` (operative bytes `d621b71` = `6fb5b589e2ac2678013885e7cb0bcb290d83d1547e0e3389d9360f2a858fd0cc`) | Three correction clusters in `corpus/knowledge/journalctl-v262-field-filter-r36.md`: the 15-term predicate list, `-n -F` truncation vs unchanged `-n -N` output, and action replacement; plus its own selftest | Qualified, carried: no freeze sha and no kill rule, and amended twice after the change commit (`718cc8f`, `d621b71`) — `corpus/lessons/round-37-verifier-spotcheck.md:63`, `:126`; the rejection-line-verbatim assertion is owed — `corpus/lessons/round-38.md:101` |
| 6 | `tools/score-storage-arm-r38.py` | r38 | `7cbaeb6317cb9f7323d2619eec02db4e4da29449` | `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218` | Ten built-in sysfs fixtures F01-F10, the live leg and six `PLANE` lines per run for the census STORAGE arm | Qualified by QUALITY 82: a fixture-gated arm scores v1 PASS 10 of 10 — `corpus/lessons/round-38.md:84`; usable only together with row 7 — `SKILL.md:3113`; fixture F06 encodes the superseded absent-root rule and FAILs 9 of 10 by construction after `49cc53c7` — `SKILL.md:3222-3224`, `SKILL.md:3314` |
| 7 | `tools/score-storage-arm-r38-q82.py` | r38 | `9c9bb6477951b3a52ac49ed83db4395765dfcf1a` | `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3` | Three per-run random production-path views inside `unshare -rm` with a random tree bind-mounted over `/sys/fs/btrfs`; predicate `ns_views_matched == VIEWS and ns_available == 1` | Qualified: R38-Q82-LEAK — four adversarial arms that read the view tree through leaked paths score 3 of 3 — `corpus/lessons/round-38.md:89`, `corpus/lessons/round-38-verifier-spotcheck.md:171`; repaired by round 39's stdin-filled tmpfs views — `corpus/lessons/round-39.md:86` |
| 8 | `tools/check-hook-order-r38.py` | r38 | `7cbaeb6317cb9f7323d2619eec02db4e4da29449` | `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8` | 69 effective hooks from 70 files against the frozen capture: order rule HO1-HO7 (override, suffix-ignoring sort, phase position), AbortOnFail, NeedsTargets, Exec, on mined source rows | Qualified: a stripped entry citing only S212 still passes — `corpus/lessons/round-38-verifier-spotcheck.md:82`, `:176`; an S-id dropped from `source:` survives — `:177` (R38-C2-COUNTER-GAPS, `corpus/lessons/round-39.md:76`); the HO rows are judged per row, not by the counter — `SCORECARD.md:2172` |
| 9 | `tools/score-storage-hidden-r39.py` | r39 | `6a08925daa30767809eb13bb4b01448ff954d46a` | `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973` | Two hidden-root legs (`BLOCKED … detail=mounts:btrfs-without-sysfs`), three stdin-filled tmpfs production-path views, five fixtures, the live leg and six `PLANE` lines per run | Qualified: R39-FIXTURE-MONOCULTURE — every btrfs fixture the same literal string — `corpus/lessons/round-39.md:71`, `corpus/lessons/round-39-verifier-spotcheck.md:184`; the `views_matched == 3` conjunct reads 3 in every run (R39-VIEW-CONTROL-UNREACHABLE, `corpus/lessons/round-39.md:72`); the live leg ignores `census_exit` — `corpus/lessons/round-39-verifier-spotcheck.md:187`. These falsify sufficiency, not the landed arm — `:67` |
| 10 | `tools/check-transaction-order-r39.py` | r39 | `6a08925daa30767809eb13bb4b01448ff954d46a` | `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e` | TO1-TO8: each quote at its cited line of the pinned libalpm snapshot on a mined `source:` row, no duplicate row or heading, two host counts, 0 `running` lines inside a commit phase | Retired for any re-claim, though its readings stood: R39-CONTENT-UNREAD — it reads `cells[2]` and `cells[3]` and never the rule cell, so `RULE NOT SUPPLIED` or the opposite still scores 8 of 8 — `corpus/lessons/round-39.md:70`; the closure re-derived the claim instead — `corpus/lessons/round-39-verifier-spotcheck.md:180-183` |
| 11 | `tools/score-selftest-literals-r40.py` | r40 | `a447b67b2502bae1e96fda341ae5ad32243ae524` | `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159` | Nine frozen mutants M1-M9 applied as exact substring replacements to the census `run_selftest` mount-table arms, three neutral rewrites N1-N3 and a self-reference guard; predicate `baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0 and selfref == 5` | Live in round 40; no verifier spot-check yet. Pre-data qualification: the self-reading selftest control does not isolate the selfref guard (selfref 6, its own baseline fails) — `SCORECARD.md:2312-2314` |
| 12 | `tools/check-exec-environment-r40.py` | r40 | `a447b67b2502bae1e96fda341ae5ad32243ae524` | `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d` | EX1-EX8 rule cells: source-derived value, frozen proposition tokens, no negation word, a 4-25 word quote at the cited snapshot lines on a new mined upstream row, two host values, zero base hits of the novelty tokens | Live in round 40; no verifier spot-check yet. Pre-data controls X-empty, X-false by negation and X-false by wrong values all FAIL it, 0 of 8 — `SCORECARD.md:2308-2311` |

Predecessors matched by the same globs, frozen in rounds 30-34 (the probe rows' full VERSION story is
`corpus/lessons/round-38.md:109-130`; the digests below are the first-carrying bytes, with the amendments named):

| # | Counter | Frozen in | First-carrying commit | sha256 at that commit | What it measured | Retired or qualified by |
|---|---|---|---|---|---|---|
| 13 | `tools/check-btrfs-space-r30.py` | r30 | `8fb2cef081787ccb52b38e9f74d95d2a480de18f` | `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (v2 `a3f1937` = `4953203d2b03fe5e5153441ba9fdc9193683e4b38f2613322a401616b6e55eba`) | Ten frozen btrfs space questions D01-D10, one row each: registry cells, snapshot path and digest, quote at its line, an integer in the evidence directory | v1 qualified, then replaced by v2 after a wave-1 fixture that cited a made-up S900 row and quoted the counter's own `ROWS` comments scored 10 of 10 — `corpus/lessons/round-30-verifier-spotcheck.md:58`, `:62`; the registry records "version 2 after the wave-1 attacks" — `SKILL.md:2667` |
| 14 | `tools/probe-git-env-residual-r30.py` | r30 | `8fb2cef081787ccb52b38e9f74d95d2a480de18f` | `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | Eleven git-writing tools over three channels (path wrapper, user files, enclosing repo), 33 (tool, channel) pairs | Qualified: parity is exit code plus normalized stdout digest, so a hollow fix scores 0, and `LD_PRELOAD`/`PYTHONPATH` go unmeasured — `corpus/lessons/round-30-verifier-spotcheck.md:182-184` |
| 15 | `tools/check-btrfs-repair-r31.py` | r31 | `f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c` | `4f69a109e9b56b3fcba0df5a3555f7ff833b6b04fff28176060efe82ebde5cb8` (env-fix `df66150` = `a6f330226b31c9dcae52ca297197290e958641b52ff9ef91c00c924846194a33`) | Eight frozen btrfs repair questions Q01-Q08, each one `new_sourced` row against six pinned btrfs-progs v7.1 snapshots | Not retired and C1 did not verify: the K6 scripted non-reader reaches 8 of 8 — `corpus/lessons/round-31-verifier-spotcheck.md:126` |
| 16 | `tools/probe-git-child-env-r31.py` | r31 | `f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c` | `b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0` | Eleven frozen tools over three channels (loader env, child contract, dotgit pointer); parity is exit code, normalized stdout digest and git-exec count | Qualified: the contract is a deny-list, so `BASH_ENV`, `GCONV_PATH` and 36 more names still reach children; 7 probe mutants survive the battery and `dotgit-pointer` gave 2 spurious verdicts in 121 runs — `corpus/lessons/round-31-verifier-spotcheck.md:95-97` |
| 17 | `tools/score-census-handoff-r32.py` | r32 | `fe1ae02cdf60aca141abf70400a850c59f239576` | `b2edc66924157703609f2489a1dca1c96bb00d30778f4d1b46640f5c0d6caee9` (v2 `f28442c` = `d6a8f07a53b586ffc4d710200962b8d99a796e0daf91222b9711516cdef311b3`; v3 `44c8eee` = `f45136c3ac15af820ae2c26fc1e5561101bbebe65df39e40c9549d37430c1b4a`) | 24 seeded fixture scenarios plus two live views: the census `HANDOFF ADJ-04 mori` line (`class= value= kind= state=`) routed per scenario | Qualified: under frozen v3 the post-data K11 shortcut reaches 24 of 24, so C1 is unprovable-but-better — `corpus/lessons/round-32-verifier-spotcheck.md:96`; the file later produced a source-channel false positive and was repaired at `4b2d263` — `SCORECARD.md:1823-1825` |
| 18 | `tools/probe-child-env-allowlist-r32.py` | r32 | `fe1ae02cdf60aca141abf70400a850c59f239576` | `2521711bb4e60a42ddd7a4a026961b3ae4aadbe0cf9036251c96f382630853d5` (v2 `44c8eee` = `d43f95ed8a740b71aac1ab412e769e011127eb4ae29646d12b2075a696cf0576`) | Eleven frozen tools; four fixed names plus eight per-run random names (four of length 2-20, four of 21-200); parity by exit code, normalized stdout digest and git-exec count | v1 replaced by a pre-data amendment (a filter keyed on the 2-20 length range would keep longer unknown names) — `tools/probe-child-env-allowlist-r32.py:25-26`; v2's exclusion list was never injected, so 4 mutants survive — `corpus/lessons/round-32-verifier-spotcheck.md:139` |
| 19 | `tools/probe-child-env-allowlist-r33.py` | r33 | `c2e69f3e863ff3332e99eae5c419c286435ff123` | `f34c3b8831369baee6a2f9151f1ecf8839528302e50615970ad655d45da152d2` (v2 `965bc5d` = `38a405837f7aa0dc9bb4e04c0851e44f5f0d6ba8429e0683ba21f1f3f38d8864`; operative freeze `9c89ff4` = `c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd`) | The r32 probe with a source channel hardened against indirect access; 5 targets, channels names, quiet and source, 15 pairs | Not retired by a defect: C1 verified under the operative bytes `c24f344b` — `corpus/lessons/round-33-verifier-spotcheck.md:130` — then superseded by a wider nine-target set; carried gap: `is_git` recognises only `/usr/bin/git` and `/usr/lib/git-core/` — `:182` |
| 20 | `tools/probe-child-env-allowlist-r34.py` | r34 | `6de666c427ba9aa6b4350561980bde8d0e7c261d` | `35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8` (V5 `15c9ac0` = `5231dbafc472ff42e041cbaad3f48dd8bd204d58b6ab22e497cf9372b23d6bfd`; V6 `3457f28` = `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92`) | The r33 probe widened to nine targets and 27 pairs, with a claim-base parity clause | Replaced pre-data twice (amendments 1 and 2) and the round broke its own freeze promise — `corpus/lessons/round-34-verifier-spotcheck.md:55-56`, `:69`; read-side gap owed: an untraced view and the two committed mutants (R34-COUNTER-READ-SIDE-GAPS) — `:184` |

Two defect classes recur, one per family. For the child-env probes the class is a **clean zero that is
indistinguishable from an unobserved zero** (`corpus/lessons/round-38.md:130`). For the claim counters of rounds 35-40
it is a **pass that a non-reading, single-literal or fixture-gated arm also reaches**: a rule cell never read
(R39-CONTENT-UNREAD), one mount-table literal in every fixture (R39-FIXTURE-MONOCULTURE), a citation set one row wide
(R38-C2-COUNTER-GAPS), a fixture-gated pass (R38-QUALITY-UNREAD) and a leaked view path (R38-Q82-LEAK). Both classes
end the same way: the number is evidence only for the observation key that produced it. Read a row with its key, and
before re-claiming on a counter, check that the "qualified by" condition behind it is either repaired in that counter
or declared as a named limit.

Round-40 wave note (appended by the L1 after the lineage draft): rows 11 and 12 were attacked in the same wave — row 11
is passed by a self-reading prologue (`declare -f`, `${0}`, `${BASH_ARGV0}`; `.ufo/waves/round-40/w1/C1CritControl.md`),
row 12 by a token-list writer that reads the counter's answer key and by affirmatively false rules
(`C2CritControl.md`, `C2CritXFalse.md`). Both are qualified the same way as rows 9 and 10: the readings stand for the
key that produced them.

## Storage arm selftest held-out tables — round 41

Appended 2026-10-26 (round-41 C1, commit `568c397da11339aed65181be598414f268835555`). Append-only: the round-38,
round-39 and round-40 storage-arm sections above stay as written, and the arm itself — `probe_storage_arm`,
`tools/tsukuroi-census.sh:1865-1925` — is unchanged: its text at `568c397` is byte-identical to the base `0e5805a1`
(empty `diff` of the two `sed -n '/^probe_storage_arm()/,/^}/p'` slices), the census file at `568c397` and at the
round tip `71851d63` is the same blob (`dda066f4`), and the commit is `1 file changed, 27 insertions(+)` in
`run_selftest` only, with zero removed lines (`git diff --stat 0e5805a1 568c397 -- tools/tsukuroi-census.sh`). No
earlier label or expected line moved, and the selftest count goes 124 → 128 (`PASS (128 cases, 128 passed,
0 failed)`).

Round 40 varied the btrfs line but left four shapes shared by every must-block table: mountpoints absolute, sources
`/dev/*`, a `subvol=` key on every btrfs line, exactly one btrfs line per table — the residual monoculture it named
(`.ufo/waves/round-40/w1/C1HeldOutMutants.md:194-196`). Three held-out mutants of that class survived its 124 cases
(H5, H6, H9), and a fourth, count direction, was frozen this round (H10). Each table below varies exactly **one** of
those four shapes and keeps the other three, so the case that kills H5 is not the case that kills H6. Each fixture
writes its own `$FX/mounts`; `check()` exports it as `TSUKUROI_PROC_MOUNTS="$FX/mounts"`
(`tools/tsukuroi-census.sh:2166`), so the arm reads the fixture and never the host's table.

| Case (`tools/tsukuroi-census.sh` at `568c397`) | Mount table (`$FX/mounts`, one line each) | Expected `STORAGE` line | Frozen mutants it kills |
|---|---|---|---|
| `storage-mounts-mp-relative` (`:3039-3043`)<br>"healthy rollup: a btrfs line whose mountpoint is not absolute still counts, BLOCKED (R41-C1 H5)"<br>*pins: the mountpoint field decides nothing; `/dev` source, `subvolid=5`/`subvol=/` kept* | `proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0`<br>`/dev/vdc1 relative/mnt btrfs rw,relatime,subvolid=5,subvol=/ 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | `H5-mountpoint-absolute`, `M1-VA-device-literal`, `M2-VB-root-mountpoint`, `M4-VG-subvolid-256`, `M8-subvol-at-literal` |
| `storage-mounts-src-uuid` (`:3045-3049`)<br>"healthy rollup: a btrfs line whose source is not under /dev still counts, BLOCKED (R41-C1 H6)"<br>*pins: the source field decides nothing; absolute mountpoint, `subvol=` kept* | `proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0`<br>`UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8 /data btrfs rw,relatime,subvolid=5,subvol=/ 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | `H6-source-devonly`, `M1-VA-device-literal`, `M2-VB-root-mountpoint`, `M4-VG-subvolid-256`, `M8-subvol-at-literal` |
| `storage-mounts-no-subvol-opt` (`:3051-3055`)<br>"healthy rollup: a btrfs line with no subvol= option still counts, BLOCKED (R41-C1 H9)"<br>*pins: options decide nothing, not even the `subvol=` key* | `proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0`<br>`/dev/sdc1 /mnt/plain btrfs rw,commit=60 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | `H9-subvolkey-option`, `M1-VA-device-literal`, `M2-VB-root-mountpoint`, `M4-VG-subvolid-256`, `M8-subvol-at-literal` |
| `storage-mounts-two-btrfs` (`:3057-3062`)<br>"healthy rollup: two btrfs lines are still btrfs without sysfs, BLOCKED (R41-C1 H10)"<br>*pins: any count ≥ 1, not exactly 1; both lines carry `/dev` source, absolute mountpoints and `subvol=`* | `/dev/nvme0n1p2 / btrfs rw,relatime,ssd,subvolid=256,subvol=/@ 0 0`<br>`proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0`<br>`/dev/nvme0n1p2 /home btrfs rw,relatime,ssd,subvolid=257,subvol=/@home 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | `H10-count-exactly-one`, `M1-VA-device-literal` |

Mutant ids are the counter's own frozen names (`tools/score-selftest-mounts-r41.py:85-104`): H5
`H5-mountpoint-absolute` (counts only when `[[ ${_mp:-} == /* ]]`), H6 `H6-source-devonly` (only when
`[[ ${_src:-} == /dev/* ]]`), H9 `H9-subvolkey-option` (whole-table `*'subvol='*`), H10 `H10-count-exactly-one`
(`if [ "$mt" -eq 1 ]`), beside the round-40 M1-M9. Kills are the receipt's confirmed labels — a stderr `FAIL
<label>` that names a baseline `PASS <label>` and is reproduced in a second run —
`.ufo/waves/round-41/after/c1-after-568c397.jsonl` `mutants.<id>.confirm_labels`. The union of the four Kills cells
is eight of the 13 mutants (M1, M2, M4, M8, H5, H6, H9, H10); the other five are killed by round-40 cases only. No
new case is the only killer of a round-40 M1-M9 mutant: M3 and M5 still die only on
`storage-mounts-btrfs-in-path`, M6 on `storage-mounts-fstype-case`, M7 on `storage-root-unreadable-mounted`, and M9
only on the two round-40 varied tables, so those cases stay load-bearing. What the four add is separation — each
held-out mutant's confirmed FAIL set is exactly one label, its own case — so H5, H6, H9 and H10 are killed by the
table that varies their shape and not by the others.

Counting: `python3 tools/score-selftest-mounts-r41.py --revision <REV> --scratch <DIR> --jobs 4` — 0 when
`baseline_pass == 1 and neutral_pass == 3 and decoy_pass == 1 and mutants_applied == 13 and survivors == 0 and
params == 4` (`tools/score-selftest-mounts-r41.py:295-296`, the same sentence in the round-41 declaration, in the
counter's docstring and in the receipt); 1 otherwise; 2 on revision, git or scratch failure. The counter is frozen at
sha256 `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c` (`sha256sum`; identical at the freeze commit
`e479fdc5`). Measured at `568c397`: baseline `PASS (128 cases, 128 passed, 0 failed)`, `capture_pass 1`, neutral 3/3,
decoy 1, mutants applied 13, survivors 0, params 4, exit 0 — 6 min 21 s at `--jobs 6` on a loaded host
(17:17:35Z–17:23:56Z). An independent rerun at the same revision (`.ufo/waves/round-41/w1/C1ExecRerun/`,
`field-compare.json`) reproduces every predicate field and every per-mutant confirmed label. At the base `0e5805a1`:
baseline `PASS (124 cases, 124 passed, 0 failed)`, survivors 4 (H5, H6, H9, H10), params 0, exit 1. One run is 19
selftests (baseline, capture, 13 mutants, 3 neutrals, decoy) plus one
confirmation run per attributed kill and one serial retry for any failed non-mutant run, so run it at most once per
item.

The `params` conjunct is a table-shape gate, not a behaviour test: the counter injects one `cp` into `check()` in its
private copy, captures each case's `$FX/mounts` beside its label and wanted patterns
(`tools/score-selftest-mounts-r41.py:115-117`), and requires a PASSing baseline case for each of the four declared
properties whose wanted patterns include `detail=mounts:btrfs-without-sysfs` (`:162-188`). The receipt records the
mapping (`param_cases`: P1→H5, P2→H6, P3→H9, P4→H10 labels). Dropping the H9 case from the candidate drops it to
`params 3` with `survivors 1` H9 (`.ufo/waves/round-41/controls/C1-K2-candidate-without-H9-case.jsonl`).

### What the decoy refuses, and what it does not

The one DECOY variant is the unmutated selftest with a dead here-document, `: <<'R41DECOY' … R41DECOY`, inserted in
front of the count loop **inside `probe_storage_arm`** in the counter's copy; the body carries every mutant's
replacement text verbatim (`tools/score-selftest-mounts-r41.py:114-127`). Its behaviour is the base arm's, so the
decoy must PASS (measured: 128/128). A selftest that reads its own text for any of those 13 strings — through
`declare -f probe_storage_arm`, `${0}`, `${BASH_ARGV0}` or `/proc/self/…` — fails it; that is the round-40
R40-ANSWER-KEY prologue, refused by construction (pre-data controls K1 and K3: `decoy_pass 0` on the base and on the
candidate). It does **not** refuse a self-reader that strips here-documents before matching (recorded limit; wave item
C1CritDecoy attacks it), nor one keyed on anything outside those 13 strings — the fixture tables, the four new case
labels and the expected regexes are not in the decoy body — nor a reader that keys on the census file's other text.

### What kill attribution refuses, and what it does not

A mutant counts as killed only when its run exits nonzero, prints the FAIL summary with the baseline's case count
(128), has at least one stderr `FAIL <label>` naming a label the baseline printed as `PASS <label>`, and a second run
fails at least one of the same labels (`tools/score-selftest-mounts-r41.py:190-202`, `:264-271`). Refused: a bare
nonzero exit, an early abort (no case count, or a different one — adding or losing a case invalidates every kill), a
summary-only failure, a FAIL label the baseline never passed, and a failure that does not reproduce. The receipt now
carries stderr labels, not counts (`first_fails`, the raw `FAIL …` lines, first three per run, `:159`), which closes the
round-40 "receipt carries counts, not labels" gap. It does **not** refuse an unrelated baseline label that fails
reproducibly twice: the receipt's first runs carry host-flake labels — `hostname override not honoured — possible host
read` on M2, M4, M5, M9 and H9 — which dropped out of the confirmed intersection here, but a flake confirmed twice
would be counted as a kill. Nor does it show causation: the rule proves the variant's run differs reproducibly at a
baseline case, not that the new table produced the difference.

### Limits of these four cases

- **H5's table is a shape the kernel does not print.** Measured in a private user namespace: `mount(2)` with a
  relative target stores the mountpoint absolute — `/proc/self/mounts` then reads
  `relative-source /fast/scratch/hyaku/tsukuroi-r41/C1ScribeSkill/tgt1 tmpfs rw,relatime,uid=1000,gid=1000,inode64,huge=advise 0 0`.
  So a relative mountpoint is forged input for any fstype, and H5 pins the arm's contract over an overridable file
  (`TSUKUROI_PROC_MOUNTS`, `tools/tsukuroi-census.sh:463`), not a live-host exposure.
- **H6's shape is representable but unobserved.** The same measurement shows the source field is stored verbatim
  (`UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8` prints as given), so a non-`/dev` source is not a field the format
  forbids; whether a real btrfs line ever carries one was not observed here — no btrfs mount was made (the host is
  read-only to this lane, and the measurement namespace held no block device). This host's table reads four btrfs lines, all
  `/dev/mapper/root`, all absolute mountpoints, all with `subvol=` (`awk '$3=="btrfs"' /proc/self/mounts`, 2026-10-26).
- **Live coverage is uneven.** H10's property is on this host today (four btrfs
  lines), so `mt -eq 1` answers false on this table — a live bug class whenever the sysfs root is absent or
  hidden, the only branch that reads the table; H9's — a btrfs mounted on its default subvolume, with no `subvol=`
  option — is a normal kernel shape this host does not show [inference: not mounted here].
- **Mutant sample, not proof of immunity.** The 13 mutants all rewrite the mount-table cross-check of the round-39
  rule. The sysfs walk, the five-counter parser, `bad-devid`, `no-devinfo` and the `root:unreadable` path carry no
  mutant here, and `survivors == 0` means 0 of these 13, never "no literal-keyed arm can pass".
- **`params` is a shape gate.** It checks that a passing case handed `check()` a table with the property and wanted a
  `detail=mounts:btrfs-without-sysfs` line; a selftest that hands those tables and hardcodes the answers elsewhere
  still scores 4. Removing a case is caught; faking a table is not.
- **One line shape per case.** No fixture holds a non-`/dev` source *and* two btrfs lines, a mountpoint with an
  escaped space (`\040`), a field count other than the six `mount` prints, or a btrfs line in a table whose sysfs root
  already has fsid entries (that guard is `storage-root-unreadable-mounted`).
- **Fixtures only.** All four tables are override files; no run reads the host's table, so this section says nothing
  new about the live host.
- **bash only.** `[[ ]]`, `${fst,,}` and `case` globbing are bash semantics (GNU bash `5.3.20` here).

### Counter sufficiency — what the round-41 wave found (appended by the L1)

- **The decoy limit is total, not partial** (`.ufo/waves/round-41/w1/C1CritDecoy.md`, variant `v1-shapegate`): a base
  census with no new `check` case, an inline text gate over `declare -f probe_storage_arm` with the here-document lines
  removed, and one btrfs line appended to the round-40 `storage-mounts-varied-multi` table passes the frozen predicate
  (`survivors 0, params 4`, exit 0). `params` counts a shape per key, so one table can supply all four. The counter
  therefore cannot certify "the selftest gains four cases" by itself; the landed implementation's PASS rests on its
  bytes as well — `568c397d` adds exactly four `check` cases and no self-reading construct (residual seat
  C1RevDiffRead, `.ufo/waves/round-41/residual/C1RevDiffRead.md`), and each held-out kill's confirmed label is the R41
  case that varies that shape (`after/c1-after-568c397.jsonl`).
- **Kill attribution reads labels, not causes** (`w1/C1CritLabels.md`): a selftest that prints a forged `FAIL <baseline
  label>` and a correctly-counted FAIL summary is credited; the one serial retry lets a coin-flip self-detector survive
  three times in four. **The `params` term carries no evidence of its own** (`w1/C1CritParams.md`): a suite with the four
  tables and no discriminating expectation scores `params 4` and fails only through `survivors`.
- **New held-out mutants** (`w1/C1HeldOutMutants.md`): of nine more, fstype-prefix (`btrfs*`) and exactly-six-fields
  survive the 128 cases; both key on shapes the kernel always prints, so they are coverage notes for a later round,
  not live defects.
- Read the round-41 readings for the key that produced them, as rows 9-12 of the lineage table say for rounds 35-40.

## Package anatomy and the local database — round 41

Appended 2026-10-26 (round-41 C2; drafted by wave seat C2ScribeSkill, integrated by the L1). The `-Qkk`
subsection above classifies what a sweep prints; this section answers the question underneath it: what a package
file carries, what libalpm requires of one on load, what install keeps in `/var/lib/pacman/local/`, and what the
kept copy is worth to `-Qkk` and to version comparison. Rules PA1-PA8 with their quotes:
`corpus/knowledge/alpm-package-anatomy-r41.md` (source rows S227-S236 — alpm-package(7) from alpm-docs 0.13.0-1,
pacman `54d9411` as built by `7.1.0.r9.g54d9411-3`, an own-work host capture; snapshots
`.ufo/waves/round-41/frozen/src/`, digests in its `SHA256SUMS`; capture `.ufo/waves/round-41/frozen/hostcap/`,
MANIFEST sha256 `632ed0443cfb26ef002ebfd2a3a99971221f9129836b63135e0ca6ea41874f89`, captured
2026-10-26T16:14:04Z). Entry carried by commit `9cc9aa77e30e0e23de2d4d2697b3b218ada02969`. Detection and report
only: nothing below installs, builds, removes or re-packs a package.

Measured on this host, 2026-10-26, read-only, `pacman 7.1.0.r9.g54d9411-3`, `ALPM_DB_VERSION` 9: 1409 local
entries (`pacman -Q | wc -l`) and 1409 kept `mtree` files, 51 kept `install` files, 0 `changelog`, 0 other root
dot files; all 1409 `mtree` files gzip (`1f 8b`), none listing `./.MTREE`; the kept `mtree` of `pacman` opens
with `./.BUILDINFO` and `./.PKGINFO` and holds 428 entries; kept `mtree` and `install` are mode `0644 root:root`;
`man -P cat PKGBUILD` prints 5 `This function is run inside` lines (4 `$srcdir`, 1 `$startdir`); `vercmp
1:1.0-1 2.0-1` = 1, `vercmp 0:2.0-1 2.0-1` = 0, `vercmp 1.0 1.0-5` = 0, `vercmp 1.0-1 1:0.1-1` = -1.
`/var/cache/pacman/pkg` holds 0 files (`pacman-conf CacheDir` = that directory) and a bounded `find` over
`/var/cache`, `/var/lib`, `~/Downloads` and `~/Projects` (`-maxdepth 3 -name '*.pkg.tar.*'`) found no package
file, so the `bsdtar` commands below ran only on a synthetic four-member archive built in scratch: they read
member order and `.PKGINFO` fields there, but their rule content is the pinned source, not that fixture.

### Symptom → PA row → read-only command → what the output means

| Symptom (verbatim string or observation) | Row | Command (read-only, paste-ready) | What the output means |
|---|---|---|---|
| An archive is called invalid because `.BUILDINFO` or `.MTREE` is missing | PA1 (S227 `alpm-package.7.raw:100-120`) | `bsdtar -tf <pkg-file> \| sed -n '1,4p'` | The document requires `.BUILDINFO .MTREE .PKGINFO` at the root and allows an optional `.INSTALL`; a missing `.BUILDINFO` or `.MTREE` is a format defect, **not** a load failure, because libalpm needs only `.PKGINFO` (PA2). The dot members survive where the kept `mtree` shows them: `./.BUILDINFO` and `./.PKGINFO` |
| `missing package metadata in <file>`, or `invalid package version`, on `pacman -U` or a sync install | PA2 (S228 `be_package.c:598-654`) | `bsdtar -xOf <pkg-file> .PKGINFO \| grep -e '^pkgname' -e '^pkgver'` | `.PKGINFO` present means the archive loads at all; its `pkgver` must carry the release after a dash with an optional `epoch:` prefix, and an empty name or version is refused at the same point. `.MTREE` is read only on a full load to build the file list; `.BUILDINFO` is passed over like every other unhandled dot file |
| A package built under a non-C locale starts with data files, or a partial read never saw `.MTREE` | PA3 (S229 `makepkg.sh.in:560-569`; `be_package.c:640-643`) | `bsdtar -tf <pkg-file> \| head -n 3` | makepkg lists members under `LC_COLLATE=C` with bash `dotglob`, so the dot files sort ahead of the data files and sit at the archive's start; a load that is not full stops at the end of the first entry after `.PKGINFO`, so order decides whether `.MTREE` is ever read. Data files first means the archive was not built by the pinned makepkg, or was re-packed |
| A scriptlet cannot be found after install, or `pacman -Qi` prints `Install Script : No` although the PKGBUILD has one | PA4 (S230 `add.c:168-189`) | `pacman -Qi <pkg> \| grep -E '^(Name\|Version\|Install Script)'; ls /var/lib/pacman/local/<name>-<version>/` | Install keeps `.INSTALL` as `install`, `.CHANGELOG` as `changelog` and `.MTREE` as `mtree`, each mode 0644, and skips every other root dot file — `.PKGINFO` and `.BUILDINFO` are never in the entry. `Install Script : No` is the absence of a kept `.INSTALL`, not of a scriptlet in the PKGBUILD. Measured: 51 of 1409 entries carry `install`, 0 `changelog`, 0 any other dot file |
| A kept `mtree` opens as binary, or an installed file is not listed in it | PA5 (S229 `makepkg.sh.in:615-620`) | `head -c2 /var/lib/pacman/local/<name>-<version>/mtree \| od -An -tx1; zcat /var/lib/pacman/local/<name>-<version>/mtree \| sed -n '1,3p'` | The first two bytes are `1f 8b` (gzip) on all 1409 here, and the listing opens with `#mtree` and a `/set` line; every file line carries a `sha256digest`, and `.MTREE` is excluded from its own listing (0 of 1409 list it) |
| `pacman -Qkk <pkg>` prints `<pkg>: no mtree file` and nothing else | PA6 (S231 `check.c:295-321`) with PA4 | `pacman -Qkk <pkg>; echo rc=$?` | The full check opens the kept `mtree`; with the file absent it prints the notice and returns 0, so the package adds zero errors and its clean result verified nothing. The same return covers a file that fails to open (a TODO leaves the two cases unseparated). `-Qk` (level 1) still checks file existence |
| A packaging function edits files as if in the wrong directory | PA7 (S232 `PKGBUILD.5.asciidoc:345-377`) | `man -P cat PKGBUILD \| grep -n 'This function is run inside'` | `package()`, `prepare()`, `build()` and `check()` run inside `$srcdir`, `verify()` inside `$startdir`, and `package()` also under fakeroot while the others run as the calling user. Host: 5 lines, 4 `$srcdir` and 1 `$startdir` — a `verify()` that assumes `$srcdir` is the documented exception, not a bug |
| An upgrade offers a version that looks lower than the installed one | PA8 (S233 `version.c:39-255`) | `pacman -Qi <pkg> \| grep '^Version'; vercmp <installed> <offered>` | Epoch first (an absent epoch counts as 0), then the version, then the release only when both strings carry one — any `1:` build outranks every epoch-0 build, `1.0` equals `1.0-5`, and `1.0-1` sorts below `1:0.1-1`. `vercmp` prints `1` / `0` / `-1` for greater / equal / lower and its exit status was `0` for all three on this host (measured 2026-10-26) — read the printed value, never `$?` |

### Checklist step — count local entries without mtree before trusting a clean `-Qkk`

Run this as step 4a of the update-safety checklist, before its integrity sample and full sweep, and whenever a
sweep or the census returns `0 altered` or `drift=0`:

```bash
for d in /var/lib/pacman/local/*/; do [ -f "$d/mtree" ] || echo "$d"; done | wc -l
```

- `0` (this host, 2026-10-26: 1409 entries, 1409 `mtree` files) — every local entry carries the kept `mtree`, so
  a clean `-Qkk` on it verified file contents instead of reporting a vacuous pass.
- `N > 0` — each printed entry's full check verified nothing: `-Qkk` prints `<pkg>: no mtree file` and returns 0
  (PA6), so that entry contributes zero errors to the sweep and cannot be cited as clean. `-Qk` still checks it.
- Run the loop under bash: GNU bash 5.3.20 (`/usr/bin/bash`) and `/bin/sh` print `0` here; a shell whose
  trailing-slash pattern also expands regular files printed `1`, and its one word was
  `/var/lib/pacman/local/ALPM_DB_VERSION/` — the database-version file, not a package entry. A word that is not a
  `<name>-<version>` directory is not a finding.

Reproduce the branch on a copy, never on the live database (measured 2026-10-26):

```bash
S=$(mktemp -d); mkdir -p "$S/db/local"
cp /var/lib/pacman/local/ALPM_DB_VERSION "$S/db/local/"
cp -r /var/lib/pacman/local/7zip-26.04-1 "$S/db/local/"
rm "$S/db/local/7zip-26.04-1/mtree"
pacman -Qkk --dbpath "$S/db" 7zip; echo "rc=$?"
```

Without the `mtree`: `7zip: no mtree file`, `rc=0`. With it: `7zip: 17 total files, 0 altered files`, `rc=0`.
`pacman -Qk --dbpath "$S/db" 7zip` prints `7zip: 17 total files, 0 missing files` in both states. The version
file must sit inside `local/`; beside it, `--dbpath` answers `database is incorrect version`.

The census sample inherits the blind spot: `tools/tsukuroi-census.sh:684` runs `pacman -Qkk` over a bounded
sample (8 by default, `--sample N`), and `:698-700` sums only `N total files, M altered files` summaries, so a
sampled entry without `mtree` adds 0 to `drift=` and its `no mtree file` line is counted nowhere. Read the
sample's `drift=` next to this count, never alone.

### Limits of this section

- **PA2 and PA3 are unmeasured on this host**, as the entry states: `/var/cache/pacman/pkg` holds 0 files
  (`pacman-conf CacheDir` = that directory, measured 2026-10-26) and pacman transactions are paused, so no package
  file could be opened. Those rows rest on the pinned snapshot, and their `bsdtar` commands ran only on a
  synthetic archive (member order and two `.PKGINFO` fields, not a makepkg-built package). PA1's host cell is the
  kept `mtree` of `pacman` — the members that survive install, not the archive.
- **The PA6 reproduction is a copy of one entry** (`7zip-26.04-1`) in a scratch `--dbpath`, not a live sweep. It
  shows the branch and its return code; it does not say what a mixed sweep prints, and it does not explain why an
  `mtree` would be missing on a real host — no local entry here lacks one.
- **Counts are a snapshot.** 1409 entries / 1409 `mtree` / 51 `install` / 0 `changelog` / 0 other dot files were
  true on 2026-10-26 and move with every install; the pinned form is capture S236
  (`.ufo/waves/round-41/frozen/hostcap/`, MANIFEST sha256 `632ed044…`). `ALPM_DB_VERSION` is 9.
- **Entry directories carry the epoch colon** (`blender-17:5.2.2-3`, `alsa-card-profiles-1:1.6.9-1`), so quote a
  `/var/lib/pacman/local/<name>-<version>/` path wherever it is used in a loop or a shell word.
- **A `desc`/`files`/`mtree` entry is not an incomplete install.** All 1409 entries carry `desc` and `files`
  beside `mtree`; `.PKGINFO` and `.BUILDINFO` are skipped by design (PA4), so their absence from the local entry,
  and a missing `install` or `changelog`, are the normal shape.
- **`-Qkk` is only as good as the kept `mtree`.** The kept file is opened with every decompression filter and the
  mtree format (S234), so a gzip header is not itself a failure mode; and the full check reports `N total files,
  M altered files` over the files that listing names.
- **The counter scores the entry, not this section.** `package-anatomy-r41` (gate registry, `SKILL.md:3121`)
  verifies PA1-PA8's rule cells, quotes inside frozen source windows and six host values from the frozen capture;
  it does not read this table, and its lexical half is a shape gate — a relation-literal writer passes it (control
  C2-K2), so the per-row reviewer verdicts are the read (QUALITY 81).

Counting: `python3 tools/check-package-anatomy-r41.py --revision <REV> [--repo <PATH>]` — 0 when PA1-PA8 each
carry the source-derived value, the frozen proposition relations and no negation word, a 4-25 word quote inside
the row's frozen source window on a new mined upstream row opened 2026-10-26, no duplicate row or heading, the six
capture-derived host values, 0 base hits of the novelty tokens and a committed non-author verdict per row; 1
otherwise; 2 on revision, git or frozen-input failure. Frozen sha256
`c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`.

### After the wave (appended by the L1)

- Every first-read seat returned `holds` for PA1-PA8; five second-read seats returned `partly` (PA2, PA3, PA5, PA6, PA7)
  and their conditions are appended to the entry as `## Corrections from the round-41 wave`: the exact `.PKGINFO` name
  (a `./.PKGINFO` repack is refused), the parse and post-loop metadata errors, `globstar` and the partial-load stop
  point, the `.INSTALL`/`.CHANGELOG`/directory entries in the kept `mtree` and the bare `--exclude .MTREE` pattern,
  `--quiet` and the `-Qpkk` false notice, and the split-package and `pkgver()` functions. Residual verdicts on the
  corrected rows: `.ufo/waves/round-41/residual/C2RevPA{2,3,5,6,7}c.md`.
- Read the decision table's PA2 row with the correction: `bsdtar -tf <pkg>` must list a line that is exactly
  `.PKGINFO`; and the `-Qkk` checklist step above with PA6's correction: `-Qpkk <file>` prints "no mtree file" for
  every package file, so it is no evidence about the file.
- **The verdict gate is not an authorship check** (`w1/C2CritControl.md`, `w1/C2CritXFalse.md`): eight two-line files
  committed with a writer's entry pass it, so the counter's PASS means "eight committed files say holds", and their
  provenance is the dispatch record (`.ufo/waves/round-41/w1-results.json` and the residual results: seat name, agent
  id, final output), which the counter does not read. Mutation results (`w1/C2MutCounter.md`): dropping window
  containment, ignoring `fails` and relaxing `host_ok` to 5 with the PA4 host check removed survive every frozen control.

## Counter lineage — round 41 rows (append-only continuation of "Counter lineage — rounds 35-40")

Drafted by wave seat ConnLineage (`.ufo/waves/round-41/w1/ConnLineage.md`); the round-41 bypasses are those the wave
demonstrated, not only those the docstrings name.

| # | Counter | Round | Freeze commit | sha256 | Closes / still admits |
|---|---|---|---|---|---|
| 13 | `tools/score-selftest-mounts-r41.py` | r41 | `e479fdc54d0977ccd8112a42d8d139baaebcb02e` | `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c` | Closes the round-40 `declare -f` prologue keyed on mutant text (controls K1, K3: `decoy_pass 0`) and the held-out survivors H5, H6, H9 and H10; still admits a here-document-stripping self-reader with one shared fixture line (`w1/C1CritDecoy.md`, PASS) and forged FAIL labels (`w1/C1CritLabels.md`) |
| 14 | `tools/check-package-anatomy-r41.py` | r41 | `e479fdc54d0977ccd8112a42d8d139baaebcb02e` | `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f` | Closes the round-40 token-list writer (control K1: `rules_verified 0`) and swapped or negated rules (K3, K4); still admits a relation-literal writer with planted verdict files (`w1/C2CritControl.md`, `w1/C2CritXFalse.md`, PASS) |

## Counter-attack scoreboard — rounds 40-41

Appended 2026-10-26 (round 41; `considerthese/2026-10-26.md` proposal "Counter-attack scoreboard": "For each frozen
counter, track how many attack arms the wave fielded, how many survived, and which class beat it"). An arm is one
scored variant a wave seat built to pass a counter without the claimed work (or a counter mutant no control catches);
"beat" means it reached the counter's PASS. Counted from the named reports, by hand, not by a script.

| Counter | Round | Arms fielded (reports) | Arms that reached PASS | Beating class |
|---|---|---|---|---|
| `score-selftest-literals-r40.py` | r40 | 4 self-reading variants (`.ufo/waves/round-40/w1/C1CritControl.md`) | 3 (`declare -f`, `${0}`, `${BASH_ARGV0}`) | answer-key read (the selftest reads the mutant texts) |
| `check-exec-environment-r40.py` | r40 | 2 writers + non-negated false rules (`.ufo/waves/round-40/w1/C2CritControl.md`, `C2CritXFalse.md`) | all three | answer-key read (frozen tokens, derived values) |
| `score-selftest-mounts-r41.py` | r41 | 2 decoy variants (`w1/C1CritDecoy.md`), 1 forged-label arm (`w1/C1CritLabels.md`), 1 shape-only suite (`w1/C1CritParams.md`) | 2 (here-document-stripping gate; forged labels) | answer-key read moved one level: the decoy's own mechanism is read and skipped |
| `check-package-anatomy-r41.py` | r41 | 1 cheapest writer (`w1/C2CritControl.md`), 4 affirmative false rules (`w1/C2CritXFalse.md`), 6 entry mutants (`w1/C2MutEntry.md`), 8 counter mutants (`w1/C2MutCounter.md`) | writer and false rules (with planted verdict files); 1 of 6 entry mutants (PA8 phrase order); 3 of 8 counter mutants | planted verdicts (provenance unread); relation order unchecked |

Reading: the hole moves rather than closes — each round's guard is beaten by reading that guard. What refused the
round-41 arms that failed was behaviour (C1 neutrals, kill attribution) and non-lexical inputs (C2 verdict files); the
next amendment should bind verdicts to the dispatch record and C1 kills to case-owned fixtures (planned row).

## Census early readers under pipefail — round 42

Appended 2026-10-26 (round-42 C1; wave seat ScribeSkill drafted, the L1 integrated and updated it for the wave-1
hardening). Defect R41-CENSUS-PIPEFAIL-692. Base `c8efaa3f`; first fix `44766208`; hardened at the round-42
integration commit (its hash is in `LOG.md`). Evidence: `.ufo/waves/round-42/` (`before/`, `controls/`, `impl/`,
`w1/`, `w2/`, `after/`).

The census runs under `set -euo pipefail`. A probe buffer piped into a reader that exits early (`grep -q`,
`grep -m1`, `head -n`, `awk … exit`) kills the writer with SIGPIPE, and pipefail makes that the pipeline's status:

| Where the pipeline sits | Signature | Seen at the base |
|---|---|---|
| a condition (`if printf … \| grep -q …`) | the test reads false: a wrong, cleaner verdict, census exit 0/1 | packages `:692`: an `error:` line in the merged `-Qkk` sample read `HEALTHY` (P1, P3, P6) |
| a `$( … )` assignment | `set -e` kills the census: exit 141, header line only | `-Qu`/`-Sup`/`-Suu` name extraction `:1621`, `:1635`, `:1641`, `:1652`; foreign baseline lookup `:743` |

The threshold is not a clean 64 KiB: under load the reader can exit between printf's 4 KiB chunks, so false
statuses start near 30 KB (wave-1 `C1SweepSites` §Evidence 1: 8 of 300 at 32 KB, 300 of 300 at 304 KB).

Rule (census and any lane bash under pipefail): never pipe a probe buffer into an early-exiting reader. Let awk read
the whole input and decide (`awk '/^error:/ { if (!p) { print; p = 1 } } END { if (!p) exit 1 }'`, `awk 'NR <= 3'`,
`awk 'NR == 1'`, a lookup without `exit`). Avoid here-strings for large buffers too: bash turns a here-string over the
pipe capacity into a temporary file, which breaks the census's no-write contract and, on a full `$TMPDIR` or `/tmp`,
fails the redirection so the `if` silently takes the clean branch (wave-1 `C1RevFix` D1: `HEALTHY`, exit 0, on an
error-bearing sample). The first fix used here-strings; the integration replaced them with the awk test.

Selftest: 128 → 132 cases, four `R42-C1` cases (a large error-bearing `-Qkk` sample; 4002 equal candidates on
`-Qu`/`-Sup`/`-Suu`; a large `-Sup` against an empty `-Qu`; a large `-Sup` against a two-line `-Qu`). With the base
plane bodies swapped into the first-fix census, exactly the two `R42-C1` cases that existed there fail
(`impl/c1-able-to-fail.txt`, recorded at `44766208`); the two `-Sup` cases are red on their own single-site reverts
(wave-1 `C1MutSelftest` §4.1). At the tip five of seven single-site reverts are selftest-killed; the `:743` lookup
revert survives the selftest (no case covers it; wave-2 `C1FinalSelftest` D1, corrected after wave-2 `C1RevSkill` F1).

Counter: `python3 tools/score-size-invariance-r42.py --revision <REV> --scratch <DIR>` — PASS iff `cases == 10 and
invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1`. It holds no expected verdict
(the large twin must answer what the small twin answers), and it refuses the single-site reverts (wave-1 `C1MutSites`,
six of six). Its sufficiency is falsified: a census fixed only when `TSUKUROI_FIXTURE` is set or uid is 0, or only
when `-Qq` lists the counter's four fixture names, passes it while the production path keeps the defect (wave-1
`C1CritNsView` V1-V3, `C1CritEvasion` V1i); a grammar-complete padding filter also passes (`ConnClaims` K5Z). The
namespace legs run as uid 0 with fixed fixture names, so they are override-free legs, not a view the code cannot
tell from production (QUALITY 90). The production-identity check that does separate them — the same view at uid 1000
via `setpriv` — is wave evidence (`C1CritNsView` §4), not part of the frozen predicate.

Not fixed here (routed): `tools/boot-chain-audit.sh:480-487` `find … -quit | grep -q .` reads false under pipefail
whenever `find` exits 1 on a missing start point, so `BOOTED-OBSERVED` can be awarded while an input is newer than
boot start (wave-1 `C1SweepSites`); the single-line probe readers (`:931`, `:969`, `:1051`, `:1426`, `:1501`) keep the
early reader on inputs that cannot reach 30 KB.

## Scrub status record — round 42

Appended 2026-10-26 (round-42 C2; wave seat ScribeSkill drafted, the L1 trimmed it to the integrated entry). Entry
`corpus/knowledge/btrfs-scrub-record-r42.md` SC1-SC5 on S237 (btrfs-progs v7.1 `cmds/scrub.c`), S238 (v7.1 `CHANGES`)
and S239 (host capture). The Arch build 7.1-1 applies no patch, so the source pins hold for the installed binary.
Nothing here runs a scrub, writes `/var/lib/btrfs` or sets a limit (operator actions).

| Observation | Reading | Action |
|---|---|---|
| `btrfs scrub status` prints `no stats available` | no device record carries a start time (SC4) | read "no record of a run", not "never scrubbed"; check the file and the recording state below |
| no `/var/lib/btrfs/scrub.status.<fsid>` | only the userspace `btrfs scrub start` process writes the record (SC1, SC3) | stored-data integrity stays `UNVERIFIED` (SH4); a run with recording disabled, or driven through the ioctl, leaves no file |
| open fails with an errno other than `ENOENT` | status warns and exits with an error; the file exists (SC4) | re-read with the owner's privileges before writing "no record" |
| `scrub.status.<fsid>_tmp` beside the record | the staging file; every update is written there and renamed over the record (SC1) | not a second record and not damage |
| a read fails at once instead of waiting | every open takes `flock(LOCK_EX\|LOCK_NB)` (SC1) | come back after the start process exits; do not loop |
| first line is not `scrub status:1` | not a version-1 record of this tool (SC2) | do not parse by column: fields are `\|key:value` pairs after `<fsid>:<devid>` |
| a start warning ends "status recording disabled" | `/var/lib/btrfs` could not be created or the first record not written; the scrub still runs (SC3) | expect no record for that run |
| status `running` | the kernel answered `BTRFS_IOC_SCRUB_PROGRESS` for a device (SC3) | the file's mtime says nothing about running |
| status `aborted` | any device record is canceled (SC4) | judge the devices separately |
| status `finished` | every device that has a record is finished; devices without a record are skipped (SC4) | read `btrfs scrub status -d` before calling every device scrubbed |
| status `interrupted` | an unfinished record and nothing running (SC4) | a process outcome; read the per-device error sums (`-d`, `-R`) |
| a scrub looks slow | `devinfo/<devid>/scrub_speed_max` limits it; 0 = none, and a failed read also prints 0 (SC5; btrfs-progs 6.6.3) | read the sysfs file before blaming the device |

Host, 2026-10-26: no `/var/lib/btrfs`, `btrfs-scrub@.timer` disabled, no kernel scrub line this boot, root device
limit 0 (capture.txt:6-10); `btrfs scrub status /` unprivileged prints `no stats available` (wave-1
`C2ExecHostRecheck`). Counter: `python3 tools/check-scrub-record-r42.py --revision <REV>`; its verdict conjunct binds
the ten wave-2 seats through `w2-dispatch.json` + `w2-results.json` + the committed report. Known limit: the binding
matches the verdict string anywhere in the output and the report, so a sentence that merely quotes the line counts
(wave-1 `C2CritControl` D1); forged orchestrator records pass the committed-bytes predicate (control C2-K3), which the
reported `transcripts_bound` cross-checks against omp's own seat transcripts.

## Counter lineage — round 42 rows (append-only continuation)

| # | Counter | Round | Freeze commit | sha256 | Closes / still admits |
|---|---|---|---|---|---|
| 15 | `tools/score-size-invariance-r42.py` | r42 | `a84fc9dec860f8bea516dff7ddfdc98223cdae52` | `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03` | Closes the answer-key read (no expected verdict; the small twin is the oracle) and the fixture-gated fix of the packages site (K7); still admits a fix gated on uid 0 or on the fixed fixture names, and a grammar-complete padding filter |
| 16 | `tools/check-scrub-record-r42.py` | r42 | `a84fc9dec860f8bea516dff7ddfdc98223cdae52` | `dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f` | Closes planted verdict files (K1) and results without dispatch tasks (K2); still admits forged dispatch + results (K3, reported by `transcripts_bound`) and a verdict line quoted rather than asserted (`C2CritControl` D1) |

## Counter-attack scoreboard — round 42 (continuation)

| Counter | Round | Arms fielded (reports) | Arms that reached PASS | Beating class |
|---|---|---|---|---|
| `score-size-invariance-r42.py` | r42 | 6 single-site reverts (`w1/C1MutSites.md`), 3 view-gated + 1 data-gated (`w1/C1CritNsView.md`), 2 sniffer variants (`w1/C1CritEvasion.md`), 3 padding filters (`w1/ConnClaims.md` K5X-K5Z) | 5 (V1, V2, V3, V1i, K5Z) | observation-channel read (uid 0, the fixture names, the counter's padding grammar) |
| `check-scrub-record-r42.py` | r42 | 10+ binding mutants (`w1/C2CritControl.md`), counter mutants (`w1/C2MutCounter.md`) | mention-as-assertion (D1); forged records (K3, declared) | the verdict string, not the assertion |

Reading: the metamorphic oracle removed the answer key, and the hole moved to the channels through which the code can
see it is observed. QUALITY 90 makes those channels frozen controls.

## Round-42 notes — C2 outcome and packaging offsets (appended after wave 2)

- The scrub-record section above rests on `corpus/knowledge/btrfs-scrub-record-r42.md`, whose C2 claim did **not**
  verify: counted wave-2 reads found SC1 and SC3 false in one sentence each and SC4/SC5 overreaching (entry section
  "Corrections — round-42 wave 2"). Read the `_tmp` and SC3/SC4 table rows through those corrections: a left-over
  `_tmp` can corrupt a later record (`invalid data on line …`), a resume does not write an all-zero record, a
  recording failure does not change the exit status, and `interrupted` can be read while a scrub runs by a caller the
  progress ioctl refuses.
- Packaging offset: the `add.c`, `makepkg.sh.in` and `PKGBUILD.5.asciidoc` line pins in this file's pacman sections are
  upstream 54d9411; the host's Arch build shifts `add.c` after :417 by +23, `makepkg.sh.in` by +118 and
  `PKGBUILD.5.asciidoc` by +9 (notes in `pacman-hook-order-r38.md`, `pacman-transaction-order-r39.md`,
  `alpm-package-anatomy-r41.md`; check `.ufo/waves/round-42/w1/ConsiderPatchOffset/patch-offset.py`).

## Boot-input freshness under pipefail — round 43

Appended 2026-10-26 (round-43 C1; drafted by wave-1 seat ScribeSkill, integrated by the L1). Routed defect
4 (R42-C1-COUNTER-AMEND), its boot-chain bullet (`corpus/lessons/round-42-verifier-spotcheck.md` §6), left open by the round-42 section
"Census early readers under pipefail — round 42" ("Not fixed here (routed)"): this section closes it. Base
`6951ead90566b2d74f7c45b4efca29246badad64`; fix `717b716a8943151ace8657e0ca23d7d9b8434f26`, one selftest case added at
the round-43 integration commit. Evidence: `.ufo/waves/round-43/` (`before/`, `after/`, `controls/`, `w1/`).

`tools/boot-chain-audit.sh` runs under `set -uo pipefail`. At the base `boot_inputs_newer` asked
`find <8 start points> -newermt "@$btime" -print -quit 2>/dev/null | grep -q .` and printed 1 only when the pipeline
succeeded. `find` exits 1 when a start point is missing or a directory is unreadable; under pipefail that status
outranks a matching `grep`, so the function printed 0 ("no input newer than boot start") while find had listed a newer
input, and the audit's BOOTED-OBSERVED gate (`newer = 0`) passed: a fail-open on the audit's own freshness guard.

| Input set | Signature at the base | Base receipt |
|---|---|---|
| a start point missing, a newer input listed after it in find's argument order | find exits 1, grep matched, the function prints 0 | six `miss/etc/*-newer` cases, expected 1 got 0 (`before/c1-before.jsonl`) |
| an unreadable directory (mode 0700, not the caller's) before the match | the same masking | `unreadable-dir-modules-newer`, expected 1 got 0 |
| 2-4 `/etc` start points missing, a file deep under `/usr/lib/modules` newer | the same masking | `multi-miss-deep-modules-newer`, expected 1 got 0 |

Rule (any lane bash under `set -o pipefail` whose input set may hold a missing or unreadable path): decide on the
command's output, never on its exit status — capture the text and test it (`hit=$(find … -print -quit 2>/dev/null);
[ -n "$hit" ]`), or neutralise the failing command's status before the pipe (`{ find … || true; } | grep -q .`,
control K9). `2>/dev/null` hides the error text, not the status. Pre-filtering missing start points is not enough: an
unreadable directory still masks (control K10).

Fix: helper `inputs_newer_than <epoch> <paths…>` decides on `hit=$(find "$@" -newermt "@$epoch" -print -quit
2>/dev/null)`; `boot_inputs_newer` calls it with the same eight start points in the same order. Selftest cases
`R43-C1-missing-start-point-none-newer`, `-deep-newer`, `R43-C1-all-present-deep-newer` (at `717b716`, 45 → 48) and
`R43-C1-missing-start-point-silent` (integration commit, 49; it kills the drop-`2>/dev/null` mutant that survived
the first three, wave-1 `C1MutFix` (c), `C1MutSelftest`).

Counter: `python3 tools/score-bootinputs-r43.py --revision <REV> --scratch <DIR>` (sha256 `886f92c8…e10f`) — PASS iff
`cases == 16 and correct == 16 and identity_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r43 >= 2`.
Base FAIL (`correct` 8); `717b716` PASS (`correct` 16, `selftest_r43` 3); re-runs `w1/C1ExecRerun.md`. Controls
(`battery-summary-c1.jsonl`, `should_fail_accepted 0, control_accepted 1`): K0-K6 and K10 FAIL; K8 candidate and K9
PASS; K7 (fixed only when `/proc/self/mountinfo` shows tmpfs on `/etc`) PASS — the mount table, `uid_map`, the
`/mnt/bca-lib.sh` source path and the cwd are channels the namespace legs leave open (wave-1 `C1CritChannels`).

Limits (wave-1 `C1MutFix`, `C1MutSelftest`): the counter scores `boot_inputs_newer`'s value, not the verdict line
(gate plumbing reproduced by hand, `w1/C1ExecHandRepro.md`); it does not exercise an unreadable `/proc/stat` (the
empty-btime branch), a widened comparison (`btime - 1`), or the membership of every start point in every draw (a
dropped `/etc/crypttab` is caught only when a draw makes it the newer input). These are recorded gaps, not claimed.

## Scrub record re-grounded — round 43

Appended 2026-10-26 (round-43 C2; drafted by wave-1 seat ScribeSkill, rewritten by the L1 to the integrated entry).
Entry `corpus/knowledge/btrfs-scrub-record-r43.md` rows SR1, SR3, SR6 on S237 (btrfs-progs v7.1 `cmds/scrub.c`,
round-42 snapshot), S240 (Linux v7.2.11 `fs/btrfs/ioctl.c`) and S241 (own-work host capture). Row status: judged by
the counted wave-2 reads (`tools/check-scrub-record-r43.py`); the outcome is recorded in `SCORECARD.md`
"Round 43 — measured outcome". Supersession: in "Scrub status record — round 42" above, the table rows that rest on
SC1 (the `_tmp` row) and SC3 (the recording-disabled, "no record" and `running` rows) are superseded by the
rows below; SC1 and SC3 of the round-42 entry stay withdrawn (its header line 4 and "Corrections — round-42 wave 2"),
and the `scrub_speed_max` row reads with that section's SC5 narrowing (a limit prints only for a device with a record
line, numerically only when above 1).

| Observation | Reading | Action |
|---|---|---|
| `scrub.status.<fsid>_tmp` beside the record | every record update opens it `O_WRONLY\|O_CREAT` without `O_TRUNC`, writes from the start and renames it over the record only after a successful write; nothing in `scrub.c` unlinks it (SR1) | a leftover means an update failed or its writer died before the rename; a later, shorter record can carry its tail into the record [inference, reproduced in a harness] (SR1) |
| record after `btrfs scrub resume` | for a device whose record was canceled or unfinished, every record write adds that record's thirteen counted fields to the new run's and keeps its `t_start`, durations summed (`scrub_resumed_stats`) (SR3) | the counters and start time are cumulative over the interrupted run and the resume; do not add a previous reading |
| zero counters in a record | a run's first record: zero for every device under a fresh `start`, and for devices a resume skips or that have no `resumed` source (SR3) | a start baseline, not history |
| scrub exited 0, recording doubtful | a failed progress or final record write prints only when `do_print` is set (`-B`, cleared when quiet) and assigns no `err`; the first-record and mkdir failures warn by default (`status recording disabled`) (SR3) | judge recording by the record file or a `-B` run, never by the exit status |
| `btrfs scrub status` and `running` | in the status command `running` comes only from `BTRFS_IOC_SCRUB_PROGRESS` succeeding for some device; Linux v7.2.11 returns `-EPERM` without `capable(CAP_SYS_ADMIN)` (SR6) | running state is an elevation-gated reading: an unprivileged status never prints `running` |
| no `/var/lib/btrfs`, `no stats available` (this host) | as uid 1000 with no effective capabilities the probe failed `EPERM` and status exited 0 with `no stats available` (S241) | stored-data integrity stays `UNVERIFIED` (SH4); a user-level census reads absence or a mode-0600 refusal, never the kernel's running state |

Counter: `python3 tools/check-scrub-record-r43.py --revision <REV>` (sha256 `b4602c56…9854`) — PASS iff `rows == 3 and
quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0
and pointer_ok == 1`; `verdicts_ok` counts only wave-2 seats `C2RevSR<n>`/`C2CritSR<n>` bound through the
orchestrator's records with an anchored declared verdict line. Limits found by wave 1 (recorded, not claimed): the
binding accepts a padded or blank-line-prefixed verdict line and does not read a JSON `verdict` field beside
`verdict_line` (`w1/C2MutBinding.md`); host refs on wrapped continuation lines and the proposition tokens are shape
checks only (`w1/C2RevCounter.md` D1, D3).

Wave-1 claim rejected by the integrator (QUALITY 91 check, recorded): "the device id is never emitted, so resume never
engages for self-written records" (`w1/C2DraftCritSR3.md` F1) is false — `scrub_writev` writes the formatted devid
itself (`scrub.c:782-792`, `return scrub_write_buf(fd, buf, ret);`) and the following `scrub_write_buf(fd, buf, ret)`
with `ret` 0 writes nothing; the compiled harness of `w1/C2ExecTailRepro.md` parsed `devid=7` back from its record.

## Gate and probe registry — round44 superseding current rows

Append-only continuation; every round-(<=43) row is carried verbatim below, then the two round-44 rows.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| child-env-allowlist-r36 | probe | `python3 tools/probe-child-env-allowlist-r36.py --revision <REV> --set livefive` | last-line `leaking` 0 clean / > 0 leaking; exit 0 clean, 1 leaking, 2 harness | none hermetic; sensitivity battery per `.ufo/waves/round-36/l1/` (claim/r33claim 0 at base) and the w2 live-mode detector receipts | VERSION 7; predicate label `leaking`; frozen bytes sha256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` at `1e926801195e304950e3eb9d2525ef8bbc245089` | committed reads; sandbox clones; no lane or host write | tsukuroi |
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, children get the round-32 allow-list environment); one private temporary HOME directory created at module load and removed at exit (round 32, wave-2 CritNoHarm); no other writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |
| btrfs-space-r30 | gate | `python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]` | 0 all ten rows D01 to D10 verified;1 one or more row unverified;2 could-not-evaluate (revision or base registry unreadable) | none: no self-test mode; fixture mode `--tree <DIR> --base-sources <FILE>` is exercised by the battery `mutants-btrfs-space-r30` | R30 C1: ten frozen questions D01 to D10 with frozen tokens, base `fbfec6bd`, rules R1 to R9; declared version 1 sha256 `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (commit `8fb2cef0`), version 2 after the wave-1 attacks | committed reads only | tsukuroi |
| btrfs-space-battery | probe | `python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]` | 0 control 10, no should-fail shape accepted and no should-pass shape refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `btrfs-space-r30`; its counts are re-derived by wave seats | R30 C1 (QUALITY 73): synthetic fixture, 72 should-fail and 11 should-pass shapes in version 2 (46 and 6 at the declaration) | private temporary directory; no git | tsukuroi |
| git-env-residual | probe | `python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness error;1 a pair leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R30 C2: eleven frozen git-writing tools, channels path-wrapper, user-files and enclosing-repo (33 pairs); probe sha256 `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| run-receipt | probe | `python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE> [--lane <repo>] [--timeout <s>] -- <tool> [args...]` | 0 the tool exited 0;1 the tool exited 1 (its own verdict);2 revision or tool unreadable, or the tool's own could-not-evaluate | none: no self-test mode; the receipt header (revision, tool revision, tool sha256) is the evidence | R30 routed defect 1 (QUALITY 77): runs a tracked tool from a sandbox clone at the tool revision with a private HOME and writes header, stdout and footer | the `--out` receipt file; sandbox clone under `/fast/scratch/hyaku` | tsukuroi |
| report-receipts | gate | `python3 tools/check-report-receipts.py --report <PATH> --lane <repo> --revision <REV>` | 0 every revision-cited gate or measurement has a committed receipt;1 one or more citation unreceipted;2 could-not-evaluate (report or revision unreadable) | `python3 tools/check-report-receipts.py --selftest` | R30 mined mistake R30-UNRECEIPTED-GATES (QUALITY 77): exits 1 on the round-29 report at lane `8976ca92` (Gates at `434a7903`) | committed reads; selftest private fixtures | tsukuroi |
| owed-statements-v4shapes-battery | probe | `python3 tools/mutants-owed-statements-r29-v4shapes.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--keep]` | 0 control 12, no routed v4 shape accepted, no control refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R30 routed defect 2 of the round-29 spot-check: closed-comment, list-indented, extra-JSON-key and asterisk-id shapes; counter v5 sha256 `6fadf5fbb77579a8a49db36a560de20b20aa2bd3d3f6928218c640b1465c475b` refuses 11 of 11 (v4 `3516d579…` accepted 11 of 11) | private clone under `/fast/scratch/hyaku` | tsukuroi |
| btrfs-repair-r31 | gate | `python3 tools/check-btrfs-repair-r31.py --revision <REV> [--lane <repo>]` | 0 all eight Q01-Q08 rows new_sourced;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen Q01-Q08 question set is measured by the counter | R31 C1: frozen predicate new_sourced; rules R1-R8; six pinned btrfs-progs v7.1 documentation snapshot sha256 values | committed Git reads only | tsukuroi |
| git-child-env-r31 | probe | `python3 tools/probe-git-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness errors;1 one or more (tool, channel) pairs leak;2 harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R31 C2: eleven frozen tools and channels loader-env, child-contract and dotgit-pointer; parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| census-handoff-r32 | gate | `python3 tools/score-census-handoff-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--seed <hex>] [--scenarios N]` | 0 every fixture scenario routed and both live views consistent;1 one or more scenarios unrouted or a live view inconsistent;2 harness error (planted facts not visible in the base census, a non-hermetic run, or a vacuous live check) | none: no self-test mode; 24 seeded fixture scenarios plus two read-only live views are the measurement | R32 C1 v3: base census 58cc2e0b; HANDOFF ADJ-04 mori grammar `class= value= kind= state=`; scenario types none, kill-events, coredumps, both, cumulative-only, cumulative+coredumps, tsukuroi-only | private scratch under the system temp dir; reads the live host read-only | tsukuroi |
| child-env-allowlist-r32 | probe | `python3 tools/probe-child-env-allowlist-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leaking target and no harness errors;1 one or more targets leak an injected name or break parity;2 harness error | none: no self-test mode; the eleven-target control and ambient-names runs are the measurement | R32 C2 v2: eleven frozen tools; BASH_ENV, ENV, GCONV_PATH, PERL5OPT plus eight per-run random names (four of length 2-20, four of 21-200); parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku` | tsukuroi |
| child-env-allowlist-r33 | probe | `python3 tools/probe-child-env-allowlist-r33.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|regression] [--only <tool> ...]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the five-target claim set and channels names, quiet and source are the measurement | R33 C1 probe v3 frozen at 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0, sha256 c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd; claim set 5 targets, channels names, quiet, source, 15 pairs; label leaking; `--set regression` is repair evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| child-env-allowlist-r34 | probe | `python3 tools/probe-child-env-allowlist-r34.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|r33claim\|regression] [--only <tool> ...] [--base <REV>]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the nine-target claim set and channels names, quiet and source are the measurement | R34 C1 probe VERSION 5 after pre-data amendment 1 at 15c9ac0e1b02917f43c0bc016d6060f888cb603a, sha256 5231dbafc472ff42e041cbaad3f48dd8bd204d58b6ab22e497cf9372b23d6bfd; claim set 9 targets, channels names, quiet, source, 27 pairs; base parity against the claim base 2641591e303057cd0f67e190a6bdf7fa91a45c31; label leaking; `--set r33claim` and `--set regression` are no-harm evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| knowledge-header | gate | `python3 tools/check-knowledge-header.py --revision <REV> [--lane <repo>] [--branch <BRANCH>]` | 0 every corpus/knowledge/*.md carries source:, verified-at: (ISO date) and recheck: (ISO date or cadence);1 one or more KNOWLEDGE-HEADER-MISSING or KNOWLEDGE-HEADER-VALUE findings;2 could-not-evaluate | `python3 tools/check-knowledge-header.py --selftest` | QUALITY 8; red at 6de666c427ba9aa6b4350561980bde8d0e7c261d on kill-oom-boundary-r33.md (and nine recheck cadence findings) before the round-34 fix | committed reads; selftest private fixtures | tsukuroi |
| score-pacnew-arm-r35 | probe | `python3 tools/score-pacnew-arm-r35.py --lane <repo> --revision <REV>` | 0 every fixture matches;1 any fixture does not match;2 harness error | none (pre-freeze control wave receipts `.ufo/waves/round-35/w1/K*/`) | VERSION 1 sha256 19d25d14…; met by controls K08FixtureKeyed and K15FieldMutants, so not a claim counter | private temp fixtures only; reads committed census bytes | tsukuroi |
| score-pacnew-arm-r35b | probe | `python3 tools/score-pacnew-arm-r35b.py --lane <repo> --revision <REV> [--skip-battery]` | 0 candidate and control match every view and no should-fail arm is accepted;1 otherwise;2 harness error | the battery itself (control arm plus 17 should-fail arms) | VERSION 2 sha256 7517af92…; 20 stub, 3 namespace, 1 live view; claim base b40c01df | private temp fixtures; unprivileged user+mount namespace; live view reads /etc names and pacman.log read-only | tsukuroi |
| journalctl-v262-corrections-r37 | gate | `python3 tools/check-journalctl-v262-corrections.py --revision <REV>` | 0 three fixed correction clusters match;1 missing/wrong correction;2 unreadable revision or CLI | `python3 tools/check-journalctl-v262-corrections.py --selftest` | Round37 correction block: exact 15 `field_list_has_scope_options()` terms; separate observed `-n -F` truncation and unchanged `-n -N` output; `--list-boots` action replacement; prior S024/round-1 teaching acknowledged | immutable Git read of the note; selftest in-memory fixtures | tsukuroi |
| child-env-allowlist-r37 | probe | `python3 tools/probe-child-env-allowlist-r37.py --revision <REV> --set livefive` | 0 `leaking` 0 and `harness_errors` empty;1 leaking pair;2 harness error | none; direct livefive receipt at `.ufo/waves/round-37/before/v8-livefive-baseline.jsonl` | VERSION 8; sha256 `9aee085b45d7566d6ce398733c10d3d87ae29bce107c4bd13fcdffcb4854b064`; 5 targets/15 predicate pairs; untraced is supplemental diagnostic only; base 564db0b | immutable target exports and disposable clones; no lane or host write | tsukuroi |
| storage-arm-r38 | gate | `python3 tools/score-storage-arm-r38.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 ten fixtures, the live leg and six PLANE lines per run match;1 any fixture, the live leg or the plane count differs;2 revision, git or bash could-not-evaluate | none: the ten built-in fixtures F01-F10 and the live leg are the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` | R38 C1 frozen at `7cbaeb63`, sha256 `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`; QUALITY 82 gap: a fixture-gated arm passes it (`controls-q82.jsonl`), so it is used only with `storage-arm-r38-q82` | private mkdtemp fixtures under `--scratch`/`TMPDIR`; reads the census at REV through git; no host write | tsukuroi |
| storage-arm-r38-q82 | gate | `python3 tools/score-storage-arm-r38-q82.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 every production-path view matches;1 a view differs;2 revision, unshare or v1-model digest could-not-evaluate | none: three per-run random views are the measurement; controls `.ufo/waves/round-38/controls/controls-q82.jsonl` (fixture-gated 0/3, cached-live 1/3, real arm 3/3) | R38 pre-seat amendment `9c9bb647`, sha256 `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3`; loads the v1 model from `7cbaeb63` by digest | `unshare -rm` child namespace with a bind mount over `/sys/fs/btrfs` that never leaves it; scratch under `--scratch`/`TMPDIR` | tsukuroi |
| hook-order-r38 | gate | `python3 tools/check-hook-order-r38.py --revision <REV> [--repo <PATH>]` | 0 all 69 rows match the frozen capture and the cited rows are mined, used-by the entry and opened 2026-10-26;1 a missing, wrong, extra or duplicate row or a source problem;2 revision, git or capture_tampered could-not-evaluate | none: the frozen capture is the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` (base, full-name sort, no override, no source FAIL; correct PASS) | R38 C2 frozen at `7cbaeb63`, sha256 `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`; capture MANIFEST sha256 `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`; libalpm order model of pacman 54d9411 | reads the entry and SOURCES at REV through git and the digest-verified capture from the work tree; no write | tsukuroi |
| storage-hidden-r39 | gate | `python3 tools/score-storage-hidden-r39.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 both hidden-root legs BLOCKED mounts:btrfs-without-sysfs, three tmpfs views, five fixtures, the live leg and six PLANE lines per run match;1 any leg differs;2 revision, git, unshare or no STORAGE line from the namespace legs | none: the hidden legs H1/H2, views V0-V2, fixtures F1-F5 and the live leg are the measurement; controls `.ufo/waves/round-39/controls/` | R39 C1 frozen at the round-39 freeze commit, sha256 `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`; views are tmpfs mounts filled from stdin inside the child (R38-Q82-LEAK) | `unshare -rm` child namespace with tmpfs mounts that never leave it; scratch under `--scratch`/`TMPDIR` | tsukuroi |
| transaction-order-r39 | gate | `python3 tools/check-transaction-order-r39.py --revision <REV> [--repo <PATH>]` | 0 TO1-TO8 each quoted from the pinned libalpm snapshot at the cited lines on a mined upstream row named on `source:`, no duplicate row or heading, two host counts present, 0 running lines inside a commit phase;1 any of these fails;2 revision, git or frozen input tampered | none: the frozen snapshots and capture are the measurement; controls `.ufo/waves/round-39/controls/` | R39 C2 frozen at the round-39 freeze commit, sha256 `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`; snapshot sha256 pins in code; capture MANIFEST sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4` | reads the entry and SOURCES at REV through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| selftest-literals-r40 | gate | `python3 tools/score-selftest-literals-r40.py --revision <REV> --scratch <DIR> [--repo <PATH>] [--jobs N]` | 0 the unmutated census selftest PASSes, three neutral rewrites of the mount-table arm PASS, all nine frozen literal/guard mutants apply once and each fails the selftest, and the census holds 5 self-reference lines;1 any of these fails;2 revision, git or scratch could-not-evaluate | none: the nine mutants and three neutral rewrites are the measurement; controls `.ufo/waves/round-40/controls/` | R40 C1 frozen at the round-40 freeze commit, sha256 `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159`; mutant texts and SELFREF_BASE 5 in code | writes only a private directory under `--scratch`, removed before exit; reads the census at REV through git | tsukuroi |
| exec-environment-r40 | gate | `python3 tools/check-exec-environment-r40.py --revision <REV> [--repo <PATH>]` | 0 EX1-EX8 each carry the source-derived value, the frozen proposition tokens and no negation word in the rule cell, a 4-25 word quote at the cited lines of the pinned snapshot on a new mined upstream row named on `source:`, no duplicate row or heading, two host values present, 0 base hits of the novelty tokens;1 any of these fails;2 revision, git, frozen input tampered or a derivation pattern unmatched | none: the frozen snapshots and capture are the measurement; controls `.ufo/waves/round-40/controls/` | R40 C2 frozen at the round-40 freeze commit, sha256 `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`; snapshot sha256 pins in code; capture MANIFEST sha256 `57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5` | reads the entry and SOURCES at REV and BASE through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| selftest-mounts-r41 | gate | `python3 tools/score-selftest-mounts-r41.py --revision <REV> --scratch <DIR> [--repo <PATH>] [--jobs N] [--timeout S]` | 0 the unmutated census selftest PASSes, three neutral rewrites and one decoy (every mutant text in a dead here-document) PASS, all thirteen frozen mutants (M1-M9, H5, H6, H9, H10) apply once and each is killed twice on a baseline case label, and the captured fixture tables cover the four declared shapes (mountpoint not absolute, source not /dev, no subvol=, two btrfs lines) on BLOCKED cases;1 any of these fails;2 revision, git or scratch could-not-evaluate | none: the mutants, neutrals, decoy and capture are the measurement; controls `.ufo/waves/round-41/controls/` | R41 C1 frozen at the round-41 freeze commit, sha256 `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`; mutant, neutral and decoy texts in code | writes only a private directory under `--scratch`, removed on exit, SIGINT and SIGTERM; the capture line is injected only into the private copy | tsukuroi |
| package-anatomy-r41 | gate | `python3 tools/check-package-anatomy-r41.py --revision <REV> [--repo <PATH>]` | 0 PA1-PA8 each carry the source-derived value, the frozen proposition relations and no negation word, a 4-25 word quote inside the row's frozen source window on a new mined upstream row named on `source:`, a committed reviewer verdict `holds` and none `fails`, six host values present, no duplicate row or heading, 0 base hits of the novelty tokens;1 any of these fails;2 revision, git, frozen input tampered or a derivation pattern unmatched | none: the frozen snapshots, capture and verdict files are the measurement; controls `.ufo/waves/round-41/controls/` | R41 C2 frozen at the round-41 freeze commit, sha256 `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`; snapshot sha256 pins in code; capture MANIFEST sha256 `632ed0443cfb26ef002ebfd2a3a99971221f9129836b63135e0ca6ea41874f89` | reads the entry, SOURCES and verdict files at REV and BASE through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| scrub-record-r42 | gate | `python3 tools/check-scrub-record-r42.py --revision <REV> [--lane <repo>]` | 0 SC1-SC5 present with quotes inside the frozen source windows, novelty verified, at least three host values, one mined source row and five wave-2 seat verdicts bound through `w2-dispatch.json` and `w2-results.json`;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen SC1-SC5 row set and the wave-2 verdict binding are the measurement | R42 C2 frozen predicate `rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1 and verdicts_ok == 5 and novelty_base_hits == 0`; pinned btrfs-progs v7.1 `cmds/scrub.c` and `CHANGES` snapshots listed in `.ufo/waves/round-42/frozen/src/SHA256SUMS` | committed Git reads only | tsukuroi |
| size-invariance-r42 | gate | `python3 tools/score-size-invariance-r42.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1` over ten P1-P6 and U1-U4 size twins and three `unshare -rm` production-path legs;1 any leg non-invariant or the census selftest not PASS;2 could-not-evaluate | none: no self-test mode; the ten fixture twins and the three namespace legs are the measurement | R42 C1 frozen counter sha256 `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`; 1 MiB verdict-neutral padding; fixtures built from the base census at `c8efaa3f` | private fixture copies under `--scratch`; `unshare -rm` namespace only for the N1/N3/N6 legs | tsukuroi |
| bootinputs-r43 | gate | `python3 tools/score-bootinputs-r43.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 16 and correct == 16 and identity_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r43 >= 2` over 16 production-path `boot_inputs_newer` cases in a private user+mount namespace, a live leg against an independent walk and the script's own selftest;1 any conjunct fails;2 could-not-evaluate (harness, namespace or read error) | none: no self-test mode; the 16 namespace cases, the live leg and the scored audit script's own `--selftest` are the measurement; controls `.ufo/waves/round-43/controls/run_controls_c1.py` | R43 C1 frozen counter sha256 `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f`; caller uid/gid through the `/etc/subuid` map and `setpriv`; mount-table, uid_map and script-path channels declared open | private `--scratch` only, removed on exit and on SIGINT/SIGTERM; tmpfs mounts only inside its own `unshare -m` namespace; reads the revision's script through `git show` | tsukuroi |
| scrub-record-r43 | gate | `python3 tools/check-scrub-record-r43.py --revision <REV> [--lane <repo>] [--sessions <dir>]` | 0 predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1` (SR1, SR3, SR6 of `corpus/knowledge/btrfs-scrub-record-r43.md`, wave-2 verdicts bound through `w2-dispatch.json`, `w2-results.json` and the report's first line);1 one or more conjuncts fail;2 could-not-evaluate | none: no self-test mode; the frozen SR rows and the bound wave-2 verdicts are the measurement; controls `.ufo/waves/round-43/controls/run_controls_c2.py` | R43 C2 frozen counter sha256 `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854`; snapshots scrub.c `48df2e2f…` (S237), ioctl.c `7b3488f2…` (S240), capture `f7ecbe7c…` (S241) | read-only: `git show` at the revision and session-transcript reads; writes nothing | tsukuroi |
| scrub-arm-r44 | gate | `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 16 and correct == 16 and identity_ok == 1 and wired_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r44 >= 6`;1 otherwise;2 usage/harness error | none: the 16 namespace cases, the wired leg, the live leg and the census selftest are the measurement; controls `.ufo/waves/round-44/controls/run_controls_c1.py` | R44 C1 frozen sha256 `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388`; candidate census sha256 `fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c` at freeze | private user+mount namespace under `--scratch`; live reads only; no host write | tsukuroi |
| scrub-record-r44 | gate | `python3 tools/check-scrub-record-r44.py --revision <REV> [--lane <repo>] [--sessions <dir>]` | 0 predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1`;1 otherwise;2 could-not-evaluate | none: the frozen SR7-SR9 rows and the bound wave-2 verdicts are the measurement; controls `.ufo/waves/round-44/controls/run_controls_c2.py` | R44 C2 frozen sha256 `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059`; snapshots sha256 in `.ufo/waves/round-44/frozen/src/SHA256SUMS` | committed reads | tsukuroi |
## Gate and probe registry — round43 superseding current rows
| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| child-env-allowlist-r36 | probe | `python3 tools/probe-child-env-allowlist-r36.py --revision <REV> --set livefive` | last-line `leaking` 0 clean / > 0 leaking; exit 0 clean, 1 leaking, 2 harness | none hermetic; sensitivity battery per `.ufo/waves/round-36/l1/` (claim/r33claim 0 at base) and the w2 live-mode detector receipts | VERSION 7; predicate label `leaking`; frozen bytes sha256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` at `1e926801195e304950e3eb9d2525ef8bbc245089` | committed reads; sandbox clones; no lane or host write | tsukuroi |
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, children get the round-32 allow-list environment); one private temporary HOME directory created at module load and removed at exit (round 32, wave-2 CritNoHarm); no other writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |
| btrfs-space-r30 | gate | `python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]` | 0 all ten rows D01 to D10 verified;1 one or more row unverified;2 could-not-evaluate (revision or base registry unreadable) | none: no self-test mode; fixture mode `--tree <DIR> --base-sources <FILE>` is exercised by the battery `mutants-btrfs-space-r30` | R30 C1: ten frozen questions D01 to D10 with frozen tokens, base `fbfec6bd`, rules R1 to R9; declared version 1 sha256 `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (commit `8fb2cef0`), version 2 after the wave-1 attacks | committed reads only | tsukuroi |
| btrfs-space-battery | probe | `python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]` | 0 control 10, no should-fail shape accepted and no should-pass shape refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `btrfs-space-r30`; its counts are re-derived by wave seats | R30 C1 (QUALITY 73): synthetic fixture, 72 should-fail and 11 should-pass shapes in version 2 (46 and 6 at the declaration) | private temporary directory; no git | tsukuroi |
| git-env-residual | probe | `python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness error;1 a pair leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R30 C2: eleven frozen git-writing tools, channels path-wrapper, user-files and enclosing-repo (33 pairs); probe sha256 `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| run-receipt | probe | `python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE> [--lane <repo>] [--timeout <s>] -- <tool> [args...]` | 0 the tool exited 0;1 the tool exited 1 (its own verdict);2 revision or tool unreadable, or the tool's own could-not-evaluate | none: no self-test mode; the receipt header (revision, tool revision, tool sha256) is the evidence | R30 routed defect 1 (QUALITY 77): runs a tracked tool from a sandbox clone at the tool revision with a private HOME and writes header, stdout and footer | the `--out` receipt file; sandbox clone under `/fast/scratch/hyaku` | tsukuroi |
| report-receipts | gate | `python3 tools/check-report-receipts.py --report <PATH> --lane <repo> --revision <REV>` | 0 every revision-cited gate or measurement has a committed receipt;1 one or more citation unreceipted;2 could-not-evaluate (report or revision unreadable) | `python3 tools/check-report-receipts.py --selftest` | R30 mined mistake R30-UNRECEIPTED-GATES (QUALITY 77): exits 1 on the round-29 report at lane `8976ca92` (Gates at `434a7903`) | committed reads; selftest private fixtures | tsukuroi |
| owed-statements-v4shapes-battery | probe | `python3 tools/mutants-owed-statements-r29-v4shapes.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--keep]` | 0 control 12, no routed v4 shape accepted, no control refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R30 routed defect 2 of the round-29 spot-check: closed-comment, list-indented, extra-JSON-key and asterisk-id shapes; counter v5 sha256 `6fadf5fbb77579a8a49db36a560de20b20aa2bd3d3f6928218c640b1465c475b` refuses 11 of 11 (v4 `3516d579…` accepted 11 of 11) | private clone under `/fast/scratch/hyaku` | tsukuroi |
| btrfs-repair-r31 | gate | `python3 tools/check-btrfs-repair-r31.py --revision <REV> [--lane <repo>]` | 0 all eight Q01-Q08 rows new_sourced;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen Q01-Q08 question set is measured by the counter | R31 C1: frozen predicate new_sourced; rules R1-R8; six pinned btrfs-progs v7.1 documentation snapshot sha256 values | committed Git reads only | tsukuroi |
| git-child-env-r31 | probe | `python3 tools/probe-git-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness errors;1 one or more (tool, channel) pairs leak;2 harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R31 C2: eleven frozen tools and channels loader-env, child-contract and dotgit-pointer; parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| census-handoff-r32 | gate | `python3 tools/score-census-handoff-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--seed <hex>] [--scenarios N]` | 0 every fixture scenario routed and both live views consistent;1 one or more scenarios unrouted or a live view inconsistent;2 harness error (planted facts not visible in the base census, a non-hermetic run, or a vacuous live check) | none: no self-test mode; 24 seeded fixture scenarios plus two read-only live views are the measurement | R32 C1 v3: base census 58cc2e0b; HANDOFF ADJ-04 mori grammar `class= value= kind= state=`; scenario types none, kill-events, coredumps, both, cumulative-only, cumulative+coredumps, tsukuroi-only | private scratch under the system temp dir; reads the live host read-only | tsukuroi |
| child-env-allowlist-r32 | probe | `python3 tools/probe-child-env-allowlist-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leaking target and no harness errors;1 one or more targets leak an injected name or break parity;2 harness error | none: no self-test mode; the eleven-target control and ambient-names runs are the measurement | R32 C2 v2: eleven frozen tools; BASH_ENV, ENV, GCONV_PATH, PERL5OPT plus eight per-run random names (four of length 2-20, four of 21-200); parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku` | tsukuroi |
| child-env-allowlist-r33 | probe | `python3 tools/probe-child-env-allowlist-r33.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|regression] [--only <tool> ...]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the five-target claim set and channels names, quiet and source are the measurement | R33 C1 probe v3 frozen at 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0, sha256 c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd; claim set 5 targets, channels names, quiet, source, 15 pairs; label leaking; `--set regression` is repair evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| child-env-allowlist-r34 | probe | `python3 tools/probe-child-env-allowlist-r34.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|r33claim\|regression] [--only <tool> ...] [--base <REV>]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the nine-target claim set and channels names, quiet and source are the measurement | R34 C1 probe VERSION 5 after pre-data amendment 1 at 15c9ac0e1b02917f43c0bc016d6060f888cb603a, sha256 5231dbafc472ff42e041cbaad3f48dd8bd204d58b6ab22e497cf9372b23d6bfd; claim set 9 targets, channels names, quiet, source, 27 pairs; base parity against the claim base 2641591e303057cd0f67e190a6bdf7fa91a45c31; label leaking; `--set r33claim` and `--set regression` are no-harm evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| knowledge-header | gate | `python3 tools/check-knowledge-header.py --revision <REV> [--lane <repo>] [--branch <BRANCH>]` | 0 every corpus/knowledge/*.md carries source:, verified-at: (ISO date) and recheck: (ISO date or cadence);1 one or more KNOWLEDGE-HEADER-MISSING or KNOWLEDGE-HEADER-VALUE findings;2 could-not-evaluate | `python3 tools/check-knowledge-header.py --selftest` | QUALITY 8; red at 6de666c427ba9aa6b4350561980bde8d0e7c261d on kill-oom-boundary-r33.md (and nine recheck cadence findings) before the round-34 fix | committed reads; selftest private fixtures | tsukuroi |
| score-pacnew-arm-r35 | probe | `python3 tools/score-pacnew-arm-r35.py --lane <repo> --revision <REV>` | 0 every fixture matches;1 any fixture does not match;2 harness error | none (pre-freeze control wave receipts `.ufo/waves/round-35/w1/K*/`) | VERSION 1 sha256 19d25d14…; met by controls K08FixtureKeyed and K15FieldMutants, so not a claim counter | private temp fixtures only; reads committed census bytes | tsukuroi |
| score-pacnew-arm-r35b | probe | `python3 tools/score-pacnew-arm-r35b.py --lane <repo> --revision <REV> [--skip-battery]` | 0 candidate and control match every view and no should-fail arm is accepted;1 otherwise;2 harness error | the battery itself (control arm plus 17 should-fail arms) | VERSION 2 sha256 7517af92…; 20 stub, 3 namespace, 1 live view; claim base b40c01df | private temp fixtures; unprivileged user+mount namespace; live view reads /etc names and pacman.log read-only | tsukuroi |
| journalctl-v262-corrections-r37 | gate | `python3 tools/check-journalctl-v262-corrections.py --revision <REV>` | 0 three fixed correction clusters match;1 missing/wrong correction;2 unreadable revision or CLI | `python3 tools/check-journalctl-v262-corrections.py --selftest` | Round37 correction block: exact 15 `field_list_has_scope_options()` terms; separate observed `-n -F` truncation and unchanged `-n -N` output; `--list-boots` action replacement; prior S024/round-1 teaching acknowledged | immutable Git read of the note; selftest in-memory fixtures | tsukuroi |
| child-env-allowlist-r37 | probe | `python3 tools/probe-child-env-allowlist-r37.py --revision <REV> --set livefive` | 0 `leaking` 0 and `harness_errors` empty;1 leaking pair;2 harness error | none; direct livefive receipt at `.ufo/waves/round-37/before/v8-livefive-baseline.jsonl` | VERSION 8; sha256 `9aee085b45d7566d6ce398733c10d3d87ae29bce107c4bd13fcdffcb4854b064`; 5 targets/15 predicate pairs; untraced is supplemental diagnostic only; base 564db0b | immutable target exports and disposable clones; no lane or host write | tsukuroi |
| storage-arm-r38 | gate | `python3 tools/score-storage-arm-r38.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 ten fixtures, the live leg and six PLANE lines per run match;1 any fixture, the live leg or the plane count differs;2 revision, git or bash could-not-evaluate | none: the ten built-in fixtures F01-F10 and the live leg are the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` | R38 C1 frozen at `7cbaeb63`, sha256 `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`; QUALITY 82 gap: a fixture-gated arm passes it (`controls-q82.jsonl`), so it is used only with `storage-arm-r38-q82` | private mkdtemp fixtures under `--scratch`/`TMPDIR`; reads the census at REV through git; no host write | tsukuroi |
| storage-arm-r38-q82 | gate | `python3 tools/score-storage-arm-r38-q82.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 every production-path view matches;1 a view differs;2 revision, unshare or v1-model digest could-not-evaluate | none: three per-run random views are the measurement; controls `.ufo/waves/round-38/controls/controls-q82.jsonl` (fixture-gated 0/3, cached-live 1/3, real arm 3/3) | R38 pre-seat amendment `9c9bb647`, sha256 `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3`; loads the v1 model from `7cbaeb63` by digest | `unshare -rm` child namespace with a bind mount over `/sys/fs/btrfs` that never leaves it; scratch under `--scratch`/`TMPDIR` | tsukuroi |
| hook-order-r38 | gate | `python3 tools/check-hook-order-r38.py --revision <REV> [--repo <PATH>]` | 0 all 69 rows match the frozen capture and the cited rows are mined, used-by the entry and opened 2026-10-26;1 a missing, wrong, extra or duplicate row or a source problem;2 revision, git or capture_tampered could-not-evaluate | none: the frozen capture is the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` (base, full-name sort, no override, no source FAIL; correct PASS) | R38 C2 frozen at `7cbaeb63`, sha256 `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`; capture MANIFEST sha256 `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`; libalpm order model of pacman 54d9411 | reads the entry and SOURCES at REV through git and the digest-verified capture from the work tree; no write | tsukuroi |
| storage-hidden-r39 | gate | `python3 tools/score-storage-hidden-r39.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 both hidden-root legs BLOCKED mounts:btrfs-without-sysfs, three tmpfs views, five fixtures, the live leg and six PLANE lines per run match;1 any leg differs;2 revision, git, unshare or no STORAGE line from the namespace legs | none: the hidden legs H1/H2, views V0-V2, fixtures F1-F5 and the live leg are the measurement; controls `.ufo/waves/round-39/controls/` | R39 C1 frozen at the round-39 freeze commit, sha256 `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`; views are tmpfs mounts filled from stdin inside the child (R38-Q82-LEAK) | `unshare -rm` child namespace with tmpfs mounts that never leave it; scratch under `--scratch`/`TMPDIR` | tsukuroi |
| transaction-order-r39 | gate | `python3 tools/check-transaction-order-r39.py --revision <REV> [--repo <PATH>]` | 0 TO1-TO8 each quoted from the pinned libalpm snapshot at the cited lines on a mined upstream row named on `source:`, no duplicate row or heading, two host counts present, 0 running lines inside a commit phase;1 any of these fails;2 revision, git or frozen input tampered | none: the frozen snapshots and capture are the measurement; controls `.ufo/waves/round-39/controls/` | R39 C2 frozen at the round-39 freeze commit, sha256 `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`; snapshot sha256 pins in code; capture MANIFEST sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4` | reads the entry and SOURCES at REV through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| selftest-literals-r40 | gate | `python3 tools/score-selftest-literals-r40.py --revision <REV> --scratch <DIR> [--repo <PATH>] [--jobs N]` | 0 the unmutated census selftest PASSes, three neutral rewrites of the mount-table arm PASS, all nine frozen literal/guard mutants apply once and each fails the selftest, and the census holds 5 self-reference lines;1 any of these fails;2 revision, git or scratch could-not-evaluate | none: the nine mutants and three neutral rewrites are the measurement; controls `.ufo/waves/round-40/controls/` | R40 C1 frozen at the round-40 freeze commit, sha256 `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159`; mutant texts and SELFREF_BASE 5 in code | writes only a private directory under `--scratch`, removed before exit; reads the census at REV through git | tsukuroi |
| exec-environment-r40 | gate | `python3 tools/check-exec-environment-r40.py --revision <REV> [--repo <PATH>]` | 0 EX1-EX8 each carry the source-derived value, the frozen proposition tokens and no negation word in the rule cell, a 4-25 word quote at the cited lines of the pinned snapshot on a new mined upstream row named on `source:`, no duplicate row or heading, two host values present, 0 base hits of the novelty tokens;1 any of these fails;2 revision, git, frozen input tampered or a derivation pattern unmatched | none: the frozen snapshots and capture are the measurement; controls `.ufo/waves/round-40/controls/` | R40 C2 frozen at the round-40 freeze commit, sha256 `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`; snapshot sha256 pins in code; capture MANIFEST sha256 `57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5` | reads the entry and SOURCES at REV and BASE through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| selftest-mounts-r41 | gate | `python3 tools/score-selftest-mounts-r41.py --revision <REV> --scratch <DIR> [--repo <PATH>] [--jobs N] [--timeout S]` | 0 the unmutated census selftest PASSes, three neutral rewrites and one decoy (every mutant text in a dead here-document) PASS, all thirteen frozen mutants (M1-M9, H5, H6, H9, H10) apply once and each is killed twice on a baseline case label, and the captured fixture tables cover the four declared shapes (mountpoint not absolute, source not /dev, no subvol=, two btrfs lines) on BLOCKED cases;1 any of these fails;2 revision, git or scratch could-not-evaluate | none: the mutants, neutrals, decoy and capture are the measurement; controls `.ufo/waves/round-41/controls/` | R41 C1 frozen at the round-41 freeze commit, sha256 `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`; mutant, neutral and decoy texts in code | writes only a private directory under `--scratch`, removed on exit, SIGINT and SIGTERM; the capture line is injected only into the private copy | tsukuroi |
| package-anatomy-r41 | gate | `python3 tools/check-package-anatomy-r41.py --revision <REV> [--repo <PATH>]` | 0 PA1-PA8 each carry the source-derived value, the frozen proposition relations and no negation word, a 4-25 word quote inside the row's frozen source window on a new mined upstream row named on `source:`, a committed reviewer verdict `holds` and none `fails`, six host values present, no duplicate row or heading, 0 base hits of the novelty tokens;1 any of these fails;2 revision, git, frozen input tampered or a derivation pattern unmatched | none: the frozen snapshots, capture and verdict files are the measurement; controls `.ufo/waves/round-41/controls/` | R41 C2 frozen at the round-41 freeze commit, sha256 `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`; snapshot sha256 pins in code; capture MANIFEST sha256 `632ed0443cfb26ef002ebfd2a3a99971221f9129836b63135e0ca6ea41874f89` | reads the entry, SOURCES and verdict files at REV and BASE through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| scrub-record-r42 | gate | `python3 tools/check-scrub-record-r42.py --revision <REV> [--lane <repo>]` | 0 SC1-SC5 present with quotes inside the frozen source windows, novelty verified, at least three host values, one mined source row and five wave-2 seat verdicts bound through `w2-dispatch.json` and `w2-results.json`;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen SC1-SC5 row set and the wave-2 verdict binding are the measurement | R42 C2 frozen predicate `rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1 and verdicts_ok == 5 and novelty_base_hits == 0`; pinned btrfs-progs v7.1 `cmds/scrub.c` and `CHANGES` snapshots listed in `.ufo/waves/round-42/frozen/src/SHA256SUMS` | committed Git reads only | tsukuroi |
| size-invariance-r42 | gate | `python3 tools/score-size-invariance-r42.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1` over ten P1-P6 and U1-U4 size twins and three `unshare -rm` production-path legs;1 any leg non-invariant or the census selftest not PASS;2 could-not-evaluate | none: no self-test mode; the ten fixture twins and the three namespace legs are the measurement | R42 C1 frozen counter sha256 `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`; 1 MiB verdict-neutral padding; fixtures built from the base census at `c8efaa3f` | private fixture copies under `--scratch`; `unshare -rm` namespace only for the N1/N3/N6 legs | tsukuroi |
| bootinputs-r43 | gate | `python3 tools/score-bootinputs-r43.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 16 and correct == 16 and identity_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r43 >= 2` over 16 production-path `boot_inputs_newer` cases in a private user+mount namespace, a live leg against an independent walk and the script's own selftest;1 any conjunct fails;2 could-not-evaluate (harness, namespace or read error) | none: no self-test mode; the 16 namespace cases, the live leg and the scored audit script's own `--selftest` are the measurement; controls `.ufo/waves/round-43/controls/run_controls_c1.py` | R43 C1 frozen counter sha256 `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f`; caller uid/gid through the `/etc/subuid` map and `setpriv`; mount-table, uid_map and script-path channels declared open | private `--scratch` only, removed on exit and on SIGINT/SIGTERM; tmpfs mounts only inside its own `unshare -m` namespace; reads the revision's script through `git show` | tsukuroi |
| scrub-record-r43 | gate | `python3 tools/check-scrub-record-r43.py --revision <REV> [--lane <repo>] [--sessions <dir>]` | 0 predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1` (SR1, SR3, SR6 of `corpus/knowledge/btrfs-scrub-record-r43.md`, wave-2 verdicts bound through `w2-dispatch.json`, `w2-results.json` and the report's first line);1 one or more conjuncts fail;2 could-not-evaluate | none: no self-test mode; the frozen SR rows and the bound wave-2 verdicts are the measurement; controls `.ufo/waves/round-43/controls/run_controls_c2.py` | R43 C2 frozen counter sha256 `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854`; snapshots scrub.c `48df2e2f…` (S237), ioctl.c `7b3488f2…` (S240), capture `f7ecbe7c…` (S241) | read-only: `git show` at the revision and session-transcript reads; writes nothing | tsukuroi |

## Scrub-record census arm — round 44

Appended 2026-10-26 (round-44 C1).
Surface: `probe_scrub_record` (`tools/tsukuroi-census.sh`) prints one verdict-neutral line after the STORAGE line
and before the rollup; the contract is the census header paragraph "Round-44 addition (C1)". What the arm reads:
entry names and stat under `/var/lib/btrfs`, the per-device sysfs `scrub_speed_max` value, and
`btrfs-scrub@*.timer` entry names under `timers.target.wants` — never a record's content, never an ioctl, never the
kernel's running state (round-43 SR6). Read the Frontier condition (`PROVINCE.md:212-214`, `corpus/README.md:243`)
as met for this sub-surface only: the artifact set around the record, not the record's data and not running state.

| Observation | Reading | Action |
|---|---|---|
| `state=NONE\|RECORDED\|BLOCKED` | BLOCKED if any block reason, else RECORDED when records+tmp+sockets > 0, else NONE | `BLOCKED` is an unknown, not an absence — hand to the operator |
| `dir=absent\|present\|unreadable` | absent = no record write created the directory yet; unreadable = BLOCKED `dir:unreadable` | never `mkdir` it (a host write) |
| `records=N` / `tmp=N` / `sockets=N` | regular `scrub.status.<fsid>` files; `_tmp` staging files (SR1); `scrub.progress.<fsid>` sockets (a live start process, never the running state) | names are read, content never is |
| `unreadable=N` | records/tmp the caller cannot read (a root scrub writes 0600) | re-read as root if the record matters; never chmod |
| `orphan=N` | records whose fsid has no sysfs entry (filesystem not mounted now); computed only when sysfs is listable | confirm with `btrfs filesystem show`; never mount |
| `limited=N` + `detail=<fsid8>:<devid>:speed_max=<v>` | devices whose `scrub_speed_max` reads a nonzero decimal; 0 = no limit (SR8, S243) | the value is root's to set; the census never writes it |
| `timers=N` | `btrfs-scrub@<instance>.timer` links under `timers.target.wants`; bare template and directories are not counted (SR9, S244) | `systemctl enable` is operator-owned |
| `detail=…` | block reasons in traversal order, then speed pairs; bytewise under LC_ALL=C; no name ever echoed | read the first token |

Counter: `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR> [--lane <repo>]` (sha256
`1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388`) — PASS iff `cases == 16 and correct == 16 and
identity_ok == 1 and wired_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r44 >= 6`: 16 drawn
production-path namespace cases, a wired full-census leg, the live leg against an independent walk, and the census
selftest (148 cases, sixteen `(R44-C1)` labels). Recorded limits (wave-1 findings): a sysfs root that exists but is
not a directory is now BLOCKED `sysfs:not-directory`; the live leg cannot tell a cached live answer from a real read
(C1CritEvasion F1); supplementary groups, cwd, stdin, statfs and ancestry differ between the namespace legs and
production (C1CritChannels); live mode creates no file (strace, C1ExecLiveRead).

## Scrub record — round 44 rows

Appended 2026-10-26 (round-44 C2).
Entry `corpus/knowledge/btrfs-scrub-record-r44.md` rows SR7, SR8, SR9 on S242 (Linux v7.2.11 `fs/btrfs/scrub.c`),
S243 (`fs/btrfs/sysfs.c`) and S244 (Arch btrfs-progs 7.1-1 units), with S237, S240 and S245.

| Observation | Reading | Action |
|---|---|---|
| A device carries a scrub context only inside the run's attached window: `btrfs_scrub_dev` refuses a second run with `-EINPROGRESS` while `dev->scrub_ctx` is set, attaches before any scrub work and clears it when the work ends (S242 scrub.c:3147,3153,3159,3222) | a non-NULL context means a scrub, or a device replace (dev-replace.c:701-703,1265-1268, unpinned), is running on that device now | read it only through a privileged `btrfs scrub status`; the census never calls the ioctl |
| `btrfs_scrub_progress` returns 0 only when the devid exists and carries a context, `-ENOTCONN` for an idle device, `-ENODEV` for an unknown devid (S242 scrub.c:3331,3336) | 0 = running now; `ENOTCONN` = idle, never 0; a momentary per-device answer, not history | "running" says nothing about when the last scrub ran or how it ended |
| The progress ioctl copies back only on 0, after its `CAP_SYS_ADMIN` gate (S240 ioctl.c:3132-3133,3139,3141) | an unprivileged status never prints `running` | stored-data integrity stays `UNVERIFIED` unprivileged (SH4) |
| `scrub_speed_max` is `BTRFS_ATTR_RW` mode 0644; reads one decimal plus newline; writes parse with `memparse` (K/M/G suffixes, trailing whitespace skipped, else `-EINVAL`); 0 = no limit; in-memory only (S243 sysfs.c:72,74,2028,2040,2042,2044) | any user reads it; root writes it; a nonzero value is a configured cap in bytes/s | the census reports `limited=` and never writes the attribute |
| The Arch package, not upstream, ships `btrfs-scrub@.timer`/`.service`; timer is monthly, `Persistent=true`, `WantedBy=timers.target`; the service runs `btrfs scrub start -B %f` with `KillSignal=SIGINT`, whose foreground handler issues `BTRFS_IOC_SCRUB_CANCEL`; a device whose ioctl returns nonzero is recorded `canceled`, which resume takes up (S244 units; S237 scrub.c:421,969,1293,1295,1546) | a monthly scrub exists only when an instance is enabled; a stopped scrub service cancels the scrub and leaves a resumable record | `systemctl enable`/start/stop are operator action; counters and `t_start` are cumulative across resume (SR3) |

Limits (entry Limits): kernel behaviour is pinned at v7.2.11 lines (the Arch patch touches no `fs/` file, carried
from round 43); SR7 is read from source only; SR9's systemd side is systemd.kill(5) inference; the SR7 replace side
is an unpinned caller [inference].

## Census first-line readers — round 45

Appended 2026-10-27 (round-45 C1; drafted by wave seat ScribeSkill, integrated by the L1). Base `5bbd5ff5`;
implementation `18389f44` — five site conversions plus six `(R45-C1)` selftest cases (148 → 154), census sha256
`237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc`. Evidence: `.ufo/waves/round-45/` (`before/`,
`controls/`, `a2w1/`).

Surface: five production readers in `tools/tsukuroi-census.sh` that keep only the first line of a captured output —
`probe_systemd` `state` (`:965`) and the timer `Result` `r` (`:1003`), `probe_drivers` `driver` (`:1085`),
`probe_journal` `t_word` (`:1460`) and the timer `ActiveState` `r` (`:1535`). At the base each read
`X=$(printf '%s\n' "$CAP_OUT" | head -n1 | …)`; each now takes its first line by parameter expansion
(`X=${CAP_OUT%%$'\n'*}`) and where the base form had them, does the CR removal and trailing-blank strip in further expansions — no `head` inside
an assignment.

Why it mattered: the census runs under `set -euo pipefail` (`:451`). `head -n1` exits after its one line, so a
captured output larger than the pipe buffer (65536 bytes on this host) leaves the `printf` producer writing into a
closed pipe; it dies of SIGPIPE, the pipeline reports 141, `pipefail` hands that status to the assignment and
`set -e` ends the census — exit 141, no PLANE line, no verdict (R41-CENSUS-PIPEFAIL-692, routed since round 42).
Measured on a 20000-line variable under `set -euo pipefail`: the base form exits 141 and prints nothing, the
parameter-expansion form prints the first line and exits 0. On this host the readers were latent — real probe
outputs sit far below the buffer — so the conversion changes no PLANE line here; the leg that shows the difference
uses stub commands padded to ~200 KB (`a2w1/C1ExecFullLarge.md`: base exit 141 with 0 PLANE lines, `18389f44` exit
2 with six plane lines matching an unpadded run).

| Observation | Reading | Action |
|---|---|---|
| the census exits 141 and prints no `TSUKUROI_CENSUS:` line | a first-line reader emptied its producer: `head` closed the pipe on a capture past the buffer, `printf` died of SIGPIPE, `pipefail` + `set -e` made 141 the census's own status, which is outside the gate's documented 0/1/2 arms | read the capture's size before trusting the run; the repair is parameter expansion, never `\|\| true` on the pipe — the `\| head -1` evasion (control K1) fails the counter |
| `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, …)` with six PASS lines ending `(R45-C1)` | each case puts the deciding first line in front of ~150-205 KB of padding (154000-210000 bytes; the sixth ~88 KB), so a `\| head` reader would die before the assertion; the sixth drives the foreign-baseline lookup (`probe_packages` `bn`, a full read since round 42) past the buffer with the deciding row last | `bash tools/tsukuroi-census.sh --selftest` in any copy: a FAIL on an `(R45-C1)` label means a reader, or the round-42 full read, regressed |
| `\| head` consumers of captured or file output still present at `:707`, `:832`, `:997`, `:1196`, `:1517`, `:1531`, `:1817` | each sits in a process substitution or behind `\|\| true`, so its status is not the assignment's and cannot kill the census; unclaimed by C1 and recorded as a limit | leave them; claiming one needs its own case and revert mutant, as the five claimed sites have |
| the `PLANE` lines at `18389f44` on a drawn capture | equal to the base's on eight draws per site (at least three with a 70-300 KB tail) | check a rewrite of one of these readers with the counter's equivalence leg, not a hand diff |

Counter: `python3 tools/score-census-readers-r45.py --revision <REV> --scratch <DIR> [--lane <repo>]` (sha256
`fe0e31e25c5b3c92cc5aace48acc56bc6dab39b4b3c09b49708a715a3250bd50`) — PASS iff `lexical_hits == 0 and sites_found ==
5 and equiv_ok == 5 and selftest_pass == 1 and selftest_r45 >= 6 and revert_killed == 6 and adjacency_ok == 1`.
Legs: lexical (no `"$CAP_OUT"` followed by `| head` before `run_selftest() {`); per-site equivalence for S1-S5
against the BASE statement on eight drawn captures each; the census selftest carrying at least six `(R45-C1)`
labels; six revert mutants — S1-S5 back to their base lines and the foreign-baseline `bn` back to the round-41
`awk … exit` early-read form — each killed by a non-zero selftest printing an `(R45-C1)` `FAIL`; and the adjacency kill rule
(`tools/check-adjacency-anchors.py` at REV, run from the lane copy whose bytes equal the base — the round-44 harm,
R44C-ADJ-IN109). Base FAIL (control K0: `lexical_hits` 5, `equiv_ok` 0, `selftest_r45` 0, `revert_killed` 0,
`adjacency_ok` 0); pre-data controls K0-K7 and K10 FAIL, K8 (candidate) and K9 (`sed -n 1p` full read) PASS,
`control_accepted` 1 (`.ufo/waves/round-45/controls/battery-summary-c1.jsonl`). Kill rule for the round: any
PLANE/HANDOFF/DRIFT/STORAGE/SCRUB/`TSUKUROI_CENSUS` line shape or live exit code that differs from the base (other
than live drift recurring between two runs of one revision), a predecessor census counter going PASS → FAIL, or a
live run that writes a file, fails C1.

Recorded limits (wave `a2w1`): the equivalence leg scores each site's first physical line only, so a conversion
split over two lines is scored on its first line; the seven masked or process-substitution `| head` readers listed
above are not claimed; the six cases and the draws are fixture captures, not this host's own
`systemctl`/`nvidia-smi` output, and the readers were latent here; `driver` still passes its single-line value
through `printf '%s\n' "$driver" | awk …`, which the lexical leg allows because it is not `"$CAP_OUT" | head`; the
live-mode no-write kill rule was checked by strace in `a2w1/C1ExecLiveRead.md`; the scored outcome of the counter
at `18389f44` is the receipt line under `.ufo/waves/round-45/`, not this section.

## Scrub grounding — round 45 rows

Gate status (round 45): the depth gate FAILED — `verdicts_ok` 0, no counted verdict bound (`SCORECARD.md` "Round 45 —
measured outcome"). GR1-GR3 are pending, not admitted: read the rows below as source-checked statements that no
counted seat has bound, and GR2 as corrected after two `partly` reads that no counted seat has re-read.

Appended 2026-10-27 (round-45 C2; drafted by wave seat ScribeSkill, integrated by the L1). Entry
`corpus/knowledge/btrfs-scrub-grounding-r45.md` rows GR1, GR2, GR3 on S246 (Linux v7.2.11 `lib/cmdline.c`,
`lib/vsprintf.c`, `lib/kstrtox.c`), S247 (`fs/btrfs/dev-replace.c`) and S248 (systemd v262 `man/systemd.kill.xml`),
with S242 and S243 (round-44 `fs/btrfs/scrub.c`, `sysfs.c`), S237 (round-42 btrfs-progs `scrub.c`) and the own-work
host capture S249 (`.ufo/waves/round-45/frozen/hostcap/capture.txt`). The three rows ground the three `[inference]`
marks the round-44 entry carried: SR8's `memparse` suffixes, SR7's replace caller of `btrfs_scrub_dev`, and SR9's
`KillSignal=` as the stop signal. Nothing here writes sysfs, starts, stops or enables a unit, runs a scrub or a
replace, or calls a privileged ioctl.

| Observation | Reading | Action |
|---|---|---|
| `devinfo/<devid>/scrub_speed_max` reads a value the operator did not type — `010` reads 8, `100m` reads 104857600 — or a write is refused with `EINVAL` | the write is parsed by `memparse` (S243 sysfs.c:2040) over `simple_strtoull` with base 0 (S246 cmdline.c:156), so a leading `0x` plus a hex digit is hexadecimal and any other leading `0` octal (S246 kstrtox.c:29-33, vsprintf.c:86); at most one suffix `K`/`M`/`G`/`T`/`P`/`E`, either case, each a factor of 1024, counted only when a digit precedes it (cmdline.c:189), overflow to `ULLONG_MAX` (:191-192); trailing whitespace is skipped (S243 sysfs.c:2042) and any text after that is `EINVAL` (:2043-2044); 0 = no limit, in-memory only, and a bare newline parses 0 and clears the limit | any user reads it, only root writes it; recompute 1024^n and the radix before calling the value wrong; the census reports `limited=` and never writes (SR8) |
| a scrub start answers `EINPROGRESS` on a filesystem where no scrub was started, or a privileged `scrub status` shows the source device of a replace as running | a device replace copies through the scrub code: `btrfs_scrub_dev(fs_info, src_device->devid, …, false, true)` at start (S247 dev-replace.c:701-703) and on continuation (:1265-1268); inside `btrfs_scrub_dev` three device checks answer first — unknown or missing device `-ENODEV`, non-writeable device on a writing call `-EROFS`, device outside the metadata or the replace target `-EIO` (S242 scrub.c:3120-3143) — then any call is refused `-EINPROGRESS` while the device carries a scrub context (:3147) and a non-replace call while `btrfs_dev_replace_is_ongoing`, i.e. a replace started or suspended (:3148-3153; S247 dev-replace.c:1286-1287); so while the copy runs a progress query for the source devid answers 0 (SR7), and for a suspended replace, whose scrub the suspend path cancels (S247 dev-replace.c:1143-1144), it answers `-ENOTCONN` (scrub.c:3336) [inference for the ioctl return path and the btrfs-progs printing] | read the unprivileged sysfs state first: `/sys/fs/btrfs/<fsid>/exclusive_operation` reads `device replace` while a replace holds the exclusive operation (S243 sysfs.c:1288; taken by the replace ioctl, S240 ioctl.c:3190, and the resume path, S247 dev-replace.c:1235) and `devinfo/<devid>/replace_target` reads 1 on the target (sysfs.c:2015); `btrfs replace status` and `scrub status` need privilege; starting or cancelling either operation stays operator-owned |
| `systemctl stop btrfs-scrub@<instance>.service` returns but the record shows no `canceled` mark, or counters that look frozen | the unit sets `KillSignal=SIGINT` (S244 btrfs-scrub@.service:9) and no `KillMode=`, so the default `control-group` applies (S248 systemd.kill.xml:68,101) — every remaining process, not only the main one; SIGCONT follows the signal (:114-115), and after `TimeoutStopSec=` the request repeats with SIGKILL unless `SendSIGKILL=no` (:91,96); on this host the effective timeout is 5 s from `/etc/systemd/system.conf.d/10-faster-shutdown.conf` (capture.txt:4), a drop-in no installed package owns (:5), with `systemctl show` reporting `KillSignal=2 KillMode=control-group TimeoutStopUSec=5s FinalKillSignal=9 SendSIGKILL=yes` (:3) under systemd 262-1-arch (:2); SIGINT reaches the foreground start's handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (S237 scrub.c:421) | read the record's timestamps before treating the run as finished: a start killed inside the 5 s may leave the record as last written, without `canceled` (`[inference]`); stop, start and enable stay operator-owned |

Counter: `python3 tools/check-scrub-grounding-r45.py --revision <REV> [--lane <repo>]` (sha256
`a1eb402dffae97fcefd9bd539529f1cacc5034419b6de06e1f8ac1c08d011331`; the attempt-2 rebinding `057c1804` changed only
the two wave-name literals `w1`/`r1` → `a2w1`/`a2r1`) — PASS iff `rows == 3 and quotes_ok == 3 and props_ok == 3 and
host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1`. A quote
counts only when its (id, file) is a digest-checked snapshot, its text occurs on the named line and is substantial
(at least 10 characters or the whole stripped line, and at least half of the stripped line's length), and one quote lies in the row's frozen window;
`props_ok` is the frozen proposition tokens, `host_ok` names existing non-empty `capture.txt` lines, and
`verdicts_ok` binds the counted seats `C2RevGR<n>` (reviewer) and `C2CritGR<n>` (critic) of wave `a2w1` through
`a2w1-dispatch.json`/`a2w1-results.json` and the report's first line `ROW GR<n> VERDICT: <holds|partly|fails>`; a
`partly` is answered by a residual `C2ResGR<n>` reading `holds` in wave `a2r1`, and an unbound counted seat makes
its row not ok. Controls `.ufo/waves/round-45/controls-a2/`: 30 controls, `should_fail_accepted` 0, K3 (forged
records), K19 (`partly` plus a bound residual) and K26 (JSON-string output) PASS (`battery-summary-c2.jsonl`).

Limits (entry Limits): kernel behaviour is pinned at Linux v7.2.11 lines (the Arch kernel 7.2.11-arch1-1 patch
touches no `fs/` file, carried from round 43 and not re-checked for `lib/` this round); GR1's examples follow from
the quoted code, not from a write — the capture's caller is uid 1000 with `CapEff` 0 (capture.txt:1) and this host's
devid 1 reads 0 (capture.txt:8); GR3 pins systemd's documented order and the host's effective values, not a trace of
a stop and nothing was started or stopped; GR2's ioctl return path and btrfs-progs printing and GR3's record
after SIGKILL stay `[inference]`; GR2 was corrected at the integration after its two counted seats read `partly`
(earlier device checks, the suspended state, the unprivileged sysfs view) and was read by the uncounted residual seats `ResRevGR2` and `ResCritGR2` (wave `a2r1`; the counter binds only a seat named `C2ResGR2`, which was not dispatched because no counted verdict bound); the verdicts are seat verdicts of this lane, not outside review; committed bytes cannot tell forged
orchestrator records from real ones (control K3 is the standing limit).

### Correction — the round-44 scrub rows (routed defect D2 and the round-45 mention sweep; appended 2026-10-27)

Appended; the rows above and their Limits block stay as written. `corpus/knowledge/btrfs-scrub-grounding-r45.md`
pins the three inferences those rows carried, so read them with this block:

- The first row's tag "(dev-replace.c:701-703,1265-1268, unpinned)" is stale: the replace caller is pinned at S247
  `fs/btrfs/dev-replace.c:700-703` and `:1265-1268`, each call `btrfs_scrub_dev(..., false, true)` (row GR2).
- "K/M/G suffixes" in the `scrub_speed_max` row is not the whole set: GR1 pins one suffix letter from `K M G T P E`
  in either case, a 1024 step each, on a base-0 parse (`010` is 8, `0x10` is 16), with at least one digit before the
  letter; a bare newline writes 0 and clears the limit (S246 `lib/cmdline.c:147-193`, `lib/vsprintf.c:86`,
  `lib/kstrtox.c:29-33`; S243 `sysfs.c:2040-2046`).
- The stop-signal row's outcome is conditional: on this host `systemctl stop` sends SIGINT (`KillSignal=2`), then
  SIGCONT, and SIGKILL only if a process remains once `TimeoutStopUSec=5s` has passed, so a `canceled` record exists only if the start writes it
  inside that window — a record without a `canceled` mark after a stop is possible (row GR3; S248
  `man/systemd.kill.xml:68,91,96,101,108,114-115`; S249 `capture.txt:2-5`).
- Limits block: the fragments "SR9's systemd side is systemd.kill(5) inference" and "the SR7 replace side is an
  unpinned caller [inference]" are superseded — both sides are pinned now (GR3, GR2).

## Gate and probe registry — round45 superseding current rows

Append-only continuation; every row of the round-44 table is carried verbatim below, then the two round-45 rows.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| child-env-allowlist-r36 | probe | `python3 tools/probe-child-env-allowlist-r36.py --revision <REV> --set livefive` | last-line `leaking` 0 clean / > 0 leaking; exit 0 clean, 1 leaking, 2 harness | none hermetic; sensitivity battery per `.ufo/waves/round-36/l1/` (claim/r33claim 0 at base) and the w2 live-mode detector receipts | VERSION 7; predicate label `leaking`; frozen bytes sha256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` at `1e926801195e304950e3eb9d2525ef8bbc245089` | committed reads; sandbox clones; no lane or host write | tsukuroi |
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, children get the round-32 allow-list environment); one private temporary HOME directory created at module load and removed at exit (round 32, wave-2 CritNoHarm); no other writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |
| btrfs-space-r30 | gate | `python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]` | 0 all ten rows D01 to D10 verified;1 one or more row unverified;2 could-not-evaluate (revision or base registry unreadable) | none: no self-test mode; fixture mode `--tree <DIR> --base-sources <FILE>` is exercised by the battery `mutants-btrfs-space-r30` | R30 C1: ten frozen questions D01 to D10 with frozen tokens, base `fbfec6bd`, rules R1 to R9; declared version 1 sha256 `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (commit `8fb2cef0`), version 2 after the wave-1 attacks | committed reads only | tsukuroi |
| btrfs-space-battery | probe | `python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]` | 0 control 10, no should-fail shape accepted and no should-pass shape refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `btrfs-space-r30`; its counts are re-derived by wave seats | R30 C1 (QUALITY 73): synthetic fixture, 72 should-fail and 11 should-pass shapes in version 2 (46 and 6 at the declaration) | private temporary directory; no git | tsukuroi |
| git-env-residual | probe | `python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness error;1 a pair leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R30 C2: eleven frozen git-writing tools, channels path-wrapper, user-files and enclosing-repo (33 pairs); probe sha256 `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| run-receipt | probe | `python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE> [--lane <repo>] [--timeout <s>] -- <tool> [args...]` | 0 the tool exited 0;1 the tool exited 1 (its own verdict);2 revision or tool unreadable, or the tool's own could-not-evaluate | none: no self-test mode; the receipt header (revision, tool revision, tool sha256) is the evidence | R30 routed defect 1 (QUALITY 77): runs a tracked tool from a sandbox clone at the tool revision with a private HOME and writes header, stdout and footer | the `--out` receipt file; sandbox clone under `/fast/scratch/hyaku` | tsukuroi |
| report-receipts | gate | `python3 tools/check-report-receipts.py --report <PATH> --lane <repo> --revision <REV>` | 0 every revision-cited gate or measurement has a committed receipt;1 one or more citation unreceipted;2 could-not-evaluate (report or revision unreadable) | `python3 tools/check-report-receipts.py --selftest` | R30 mined mistake R30-UNRECEIPTED-GATES (QUALITY 77): exits 1 on the round-29 report at lane `8976ca92` (Gates at `434a7903`) | committed reads; selftest private fixtures | tsukuroi |
| owed-statements-v4shapes-battery | probe | `python3 tools/mutants-owed-statements-r29-v4shapes.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--keep]` | 0 control 12, no routed v4 shape accepted, no control refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R30 routed defect 2 of the round-29 spot-check: closed-comment, list-indented, extra-JSON-key and asterisk-id shapes; counter v5 sha256 `6fadf5fbb77579a8a49db36a560de20b20aa2bd3d3f6928218c640b1465c475b` refuses 11 of 11 (v4 `3516d579…` accepted 11 of 11) | private clone under `/fast/scratch/hyaku` | tsukuroi |
| btrfs-repair-r31 | gate | `python3 tools/check-btrfs-repair-r31.py --revision <REV> [--lane <repo>]` | 0 all eight Q01-Q08 rows new_sourced;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen Q01-Q08 question set is measured by the counter | R31 C1: frozen predicate new_sourced; rules R1-R8; six pinned btrfs-progs v7.1 documentation snapshot sha256 values | committed Git reads only | tsukuroi |
| git-child-env-r31 | probe | `python3 tools/probe-git-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness errors;1 one or more (tool, channel) pairs leak;2 harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R31 C2: eleven frozen tools and channels loader-env, child-contract and dotgit-pointer; parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| census-handoff-r32 | gate | `python3 tools/score-census-handoff-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--seed <hex>] [--scenarios N]` | 0 every fixture scenario routed and both live views consistent;1 one or more scenarios unrouted or a live view inconsistent;2 harness error (planted facts not visible in the base census, a non-hermetic run, or a vacuous live check) | none: no self-test mode; 24 seeded fixture scenarios plus two read-only live views are the measurement | R32 C1 v3: base census 58cc2e0b; HANDOFF ADJ-04 mori grammar `class= value= kind= state=`; scenario types none, kill-events, coredumps, both, cumulative-only, cumulative+coredumps, tsukuroi-only | private scratch under the system temp dir; reads the live host read-only | tsukuroi |
| child-env-allowlist-r32 | probe | `python3 tools/probe-child-env-allowlist-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leaking target and no harness errors;1 one or more targets leak an injected name or break parity;2 harness error | none: no self-test mode; the eleven-target control and ambient-names runs are the measurement | R32 C2 v2: eleven frozen tools; BASH_ENV, ENV, GCONV_PATH, PERL5OPT plus eight per-run random names (four of length 2-20, four of 21-200); parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku` | tsukuroi |
| child-env-allowlist-r33 | probe | `python3 tools/probe-child-env-allowlist-r33.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|regression] [--only <tool> ...]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the five-target claim set and channels names, quiet and source are the measurement | R33 C1 probe v3 frozen at 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0, sha256 c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd; claim set 5 targets, channels names, quiet, source, 15 pairs; label leaking; `--set regression` is repair evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| child-env-allowlist-r34 | probe | `python3 tools/probe-child-env-allowlist-r34.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|r33claim\|regression] [--only <tool> ...] [--base <REV>]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the nine-target claim set and channels names, quiet and source are the measurement | R34 C1 probe VERSION 5 after pre-data amendment 1 at 15c9ac0e1b02917f43c0bc016d6060f888cb603a, sha256 5231dbafc472ff42e041cbaad3f48dd8bd204d58b6ab22e497cf9372b23d6bfd; claim set 9 targets, channels names, quiet, source, 27 pairs; base parity against the claim base 2641591e303057cd0f67e190a6bdf7fa91a45c31; label leaking; `--set r33claim` and `--set regression` are no-harm evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| knowledge-header | gate | `python3 tools/check-knowledge-header.py --revision <REV> [--lane <repo>] [--branch <BRANCH>]` | 0 every corpus/knowledge/*.md carries source:, verified-at: (ISO date) and recheck: (ISO date or cadence);1 one or more KNOWLEDGE-HEADER-MISSING or KNOWLEDGE-HEADER-VALUE findings;2 could-not-evaluate | `python3 tools/check-knowledge-header.py --selftest` | QUALITY 8; red at 6de666c427ba9aa6b4350561980bde8d0e7c261d on kill-oom-boundary-r33.md (and nine recheck cadence findings) before the round-34 fix | committed reads; selftest private fixtures | tsukuroi |
| score-pacnew-arm-r35 | probe | `python3 tools/score-pacnew-arm-r35.py --lane <repo> --revision <REV>` | 0 every fixture matches;1 any fixture does not match;2 harness error | none (pre-freeze control wave receipts `.ufo/waves/round-35/w1/K*/`) | VERSION 1 sha256 19d25d14…; met by controls K08FixtureKeyed and K15FieldMutants, so not a claim counter | private temp fixtures only; reads committed census bytes | tsukuroi |
| score-pacnew-arm-r35b | probe | `python3 tools/score-pacnew-arm-r35b.py --lane <repo> --revision <REV> [--skip-battery]` | 0 candidate and control match every view and no should-fail arm is accepted;1 otherwise;2 harness error | the battery itself (control arm plus 17 should-fail arms) | VERSION 2 sha256 7517af92…; 20 stub, 3 namespace, 1 live view; claim base b40c01df | private temp fixtures; unprivileged user+mount namespace; live view reads /etc names and pacman.log read-only | tsukuroi |
| journalctl-v262-corrections-r37 | gate | `python3 tools/check-journalctl-v262-corrections.py --revision <REV>` | 0 three fixed correction clusters match;1 missing/wrong correction;2 unreadable revision or CLI | `python3 tools/check-journalctl-v262-corrections.py --selftest` | Round37 correction block: exact 15 `field_list_has_scope_options()` terms; separate observed `-n -F` truncation and unchanged `-n -N` output; `--list-boots` action replacement; prior S024/round-1 teaching acknowledged | immutable Git read of the note; selftest in-memory fixtures | tsukuroi |
| child-env-allowlist-r37 | probe | `python3 tools/probe-child-env-allowlist-r37.py --revision <REV> --set livefive` | 0 `leaking` 0 and `harness_errors` empty;1 leaking pair;2 harness error | none; direct livefive receipt at `.ufo/waves/round-37/before/v8-livefive-baseline.jsonl` | VERSION 8; sha256 `9aee085b45d7566d6ce398733c10d3d87ae29bce107c4bd13fcdffcb4854b064`; 5 targets/15 predicate pairs; untraced is supplemental diagnostic only; base 564db0b | immutable target exports and disposable clones; no lane or host write | tsukuroi |
| storage-arm-r38 | gate | `python3 tools/score-storage-arm-r38.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 ten fixtures, the live leg and six PLANE lines per run match;1 any fixture, the live leg or the plane count differs;2 revision, git or bash could-not-evaluate | none: the ten built-in fixtures F01-F10 and the live leg are the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` | R38 C1 frozen at `7cbaeb63`, sha256 `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`; QUALITY 82 gap: a fixture-gated arm passes it (`controls-q82.jsonl`), so it is used only with `storage-arm-r38-q82` | private mkdtemp fixtures under `--scratch`/`TMPDIR`; reads the census at REV through git; no host write | tsukuroi |
| storage-arm-r38-q82 | gate | `python3 tools/score-storage-arm-r38-q82.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 every production-path view matches;1 a view differs;2 revision, unshare or v1-model digest could-not-evaluate | none: three per-run random views are the measurement; controls `.ufo/waves/round-38/controls/controls-q82.jsonl` (fixture-gated 0/3, cached-live 1/3, real arm 3/3) | R38 pre-seat amendment `9c9bb647`, sha256 `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3`; loads the v1 model from `7cbaeb63` by digest | `unshare -rm` child namespace with a bind mount over `/sys/fs/btrfs` that never leaves it; scratch under `--scratch`/`TMPDIR` | tsukuroi |
| hook-order-r38 | gate | `python3 tools/check-hook-order-r38.py --revision <REV> [--repo <PATH>]` | 0 all 69 rows match the frozen capture and the cited rows are mined, used-by the entry and opened 2026-10-26;1 a missing, wrong, extra or duplicate row or a source problem;2 revision, git or capture_tampered could-not-evaluate | none: the frozen capture is the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` (base, full-name sort, no override, no source FAIL; correct PASS) | R38 C2 frozen at `7cbaeb63`, sha256 `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`; capture MANIFEST sha256 `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`; libalpm order model of pacman 54d9411 | reads the entry and SOURCES at REV through git and the digest-verified capture from the work tree; no write | tsukuroi |
| storage-hidden-r39 | gate | `python3 tools/score-storage-hidden-r39.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 both hidden-root legs BLOCKED mounts:btrfs-without-sysfs, three tmpfs views, five fixtures, the live leg and six PLANE lines per run match;1 any leg differs;2 revision, git, unshare or no STORAGE line from the namespace legs | none: the hidden legs H1/H2, views V0-V2, fixtures F1-F5 and the live leg are the measurement; controls `.ufo/waves/round-39/controls/` | R39 C1 frozen at the round-39 freeze commit, sha256 `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`; views are tmpfs mounts filled from stdin inside the child (R38-Q82-LEAK) | `unshare -rm` child namespace with tmpfs mounts that never leave it; scratch under `--scratch`/`TMPDIR` | tsukuroi |
| transaction-order-r39 | gate | `python3 tools/check-transaction-order-r39.py --revision <REV> [--repo <PATH>]` | 0 TO1-TO8 each quoted from the pinned libalpm snapshot at the cited lines on a mined upstream row named on `source:`, no duplicate row or heading, two host counts present, 0 running lines inside a commit phase;1 any of these fails;2 revision, git or frozen input tampered | none: the frozen snapshots and capture are the measurement; controls `.ufo/waves/round-39/controls/` | R39 C2 frozen at the round-39 freeze commit, sha256 `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`; snapshot sha256 pins in code; capture MANIFEST sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4` | reads the entry and SOURCES at REV through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| selftest-literals-r40 | gate | `python3 tools/score-selftest-literals-r40.py --revision <REV> --scratch <DIR> [--repo <PATH>] [--jobs N]` | 0 the unmutated census selftest PASSes, three neutral rewrites of the mount-table arm PASS, all nine frozen literal/guard mutants apply once and each fails the selftest, and the census holds 5 self-reference lines;1 any of these fails;2 revision, git or scratch could-not-evaluate | none: the nine mutants and three neutral rewrites are the measurement; controls `.ufo/waves/round-40/controls/` | R40 C1 frozen at the round-40 freeze commit, sha256 `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159`; mutant texts and SELFREF_BASE 5 in code | writes only a private directory under `--scratch`, removed before exit; reads the census at REV through git | tsukuroi |
| exec-environment-r40 | gate | `python3 tools/check-exec-environment-r40.py --revision <REV> [--repo <PATH>]` | 0 EX1-EX8 each carry the source-derived value, the frozen proposition tokens and no negation word in the rule cell, a 4-25 word quote at the cited lines of the pinned snapshot on a new mined upstream row named on `source:`, no duplicate row or heading, two host values present, 0 base hits of the novelty tokens;1 any of these fails;2 revision, git, frozen input tampered or a derivation pattern unmatched | none: the frozen snapshots and capture are the measurement; controls `.ufo/waves/round-40/controls/` | R40 C2 frozen at the round-40 freeze commit, sha256 `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`; snapshot sha256 pins in code; capture MANIFEST sha256 `57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5` | reads the entry and SOURCES at REV and BASE through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| selftest-mounts-r41 | gate | `python3 tools/score-selftest-mounts-r41.py --revision <REV> --scratch <DIR> [--repo <PATH>] [--jobs N] [--timeout S]` | 0 the unmutated census selftest PASSes, three neutral rewrites and one decoy (every mutant text in a dead here-document) PASS, all thirteen frozen mutants (M1-M9, H5, H6, H9, H10) apply once and each is killed twice on a baseline case label, and the captured fixture tables cover the four declared shapes (mountpoint not absolute, source not /dev, no subvol=, two btrfs lines) on BLOCKED cases;1 any of these fails;2 revision, git or scratch could-not-evaluate | none: the mutants, neutrals, decoy and capture are the measurement; controls `.ufo/waves/round-41/controls/` | R41 C1 frozen at the round-41 freeze commit, sha256 `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`; mutant, neutral and decoy texts in code | writes only a private directory under `--scratch`, removed on exit, SIGINT and SIGTERM; the capture line is injected only into the private copy | tsukuroi |
| package-anatomy-r41 | gate | `python3 tools/check-package-anatomy-r41.py --revision <REV> [--repo <PATH>]` | 0 PA1-PA8 each carry the source-derived value, the frozen proposition relations and no negation word, a 4-25 word quote inside the row's frozen source window on a new mined upstream row named on `source:`, a committed reviewer verdict `holds` and none `fails`, six host values present, no duplicate row or heading, 0 base hits of the novelty tokens;1 any of these fails;2 revision, git, frozen input tampered or a derivation pattern unmatched | none: the frozen snapshots, capture and verdict files are the measurement; controls `.ufo/waves/round-41/controls/` | R41 C2 frozen at the round-41 freeze commit, sha256 `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`; snapshot sha256 pins in code; capture MANIFEST sha256 `632ed0443cfb26ef002ebfd2a3a99971221f9129836b63135e0ca6ea41874f89` | reads the entry, SOURCES and verdict files at REV and BASE through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| scrub-record-r42 | gate | `python3 tools/check-scrub-record-r42.py --revision <REV> [--lane <repo>]` | 0 SC1-SC5 present with quotes inside the frozen source windows, novelty verified, at least three host values, one mined source row and five wave-2 seat verdicts bound through `w2-dispatch.json` and `w2-results.json`;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen SC1-SC5 row set and the wave-2 verdict binding are the measurement | R42 C2 frozen predicate `rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1 and verdicts_ok == 5 and novelty_base_hits == 0`; pinned btrfs-progs v7.1 `cmds/scrub.c` and `CHANGES` snapshots listed in `.ufo/waves/round-42/frozen/src/SHA256SUMS` | committed Git reads only | tsukuroi |
| size-invariance-r42 | gate | `python3 tools/score-size-invariance-r42.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1` over ten P1-P6 and U1-U4 size twins and three `unshare -rm` production-path legs;1 any leg non-invariant or the census selftest not PASS;2 could-not-evaluate | none: no self-test mode; the ten fixture twins and the three namespace legs are the measurement | R42 C1 frozen counter sha256 `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`; 1 MiB verdict-neutral padding; fixtures built from the base census at `c8efaa3f` | private fixture copies under `--scratch`; `unshare -rm` namespace only for the N1/N3/N6 legs | tsukuroi |
| bootinputs-r43 | gate | `python3 tools/score-bootinputs-r43.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 16 and correct == 16 and identity_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r43 >= 2` over 16 production-path `boot_inputs_newer` cases in a private user+mount namespace, a live leg against an independent walk and the script's own selftest;1 any conjunct fails;2 could-not-evaluate (harness, namespace or read error) | none: no self-test mode; the 16 namespace cases, the live leg and the scored audit script's own `--selftest` are the measurement; controls `.ufo/waves/round-43/controls/run_controls_c1.py` | R43 C1 frozen counter sha256 `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f`; caller uid/gid through the `/etc/subuid` map and `setpriv`; mount-table, uid_map and script-path channels declared open | private `--scratch` only, removed on exit and on SIGINT/SIGTERM; tmpfs mounts only inside its own `unshare -m` namespace; reads the revision's script through `git show` | tsukuroi |
| scrub-record-r43 | gate | `python3 tools/check-scrub-record-r43.py --revision <REV> [--lane <repo>] [--sessions <dir>]` | 0 predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1` (SR1, SR3, SR6 of `corpus/knowledge/btrfs-scrub-record-r43.md`, wave-2 verdicts bound through `w2-dispatch.json`, `w2-results.json` and the report's first line);1 one or more conjuncts fail;2 could-not-evaluate | none: no self-test mode; the frozen SR rows and the bound wave-2 verdicts are the measurement; controls `.ufo/waves/round-43/controls/run_controls_c2.py` | R43 C2 frozen counter sha256 `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854`; snapshots scrub.c `48df2e2f…` (S237), ioctl.c `7b3488f2…` (S240), capture `f7ecbe7c…` (S241) | read-only: `git show` at the revision and session-transcript reads; writes nothing | tsukuroi |
| scrub-arm-r44 | gate | `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 16 and correct == 16 and identity_ok == 1 and wired_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r44 >= 6`;1 otherwise;2 usage/harness error | none: the 16 namespace cases, the wired leg, the live leg and the census selftest are the measurement; controls `.ufo/waves/round-44/controls/run_controls_c1.py` | R44 C1 frozen sha256 `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388`; candidate census sha256 `fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c` at freeze | private user+mount namespace under `--scratch`; live reads only; no host write | tsukuroi |
| scrub-record-r44 | gate | `python3 tools/check-scrub-record-r44.py --revision <REV> [--lane <repo>] [--sessions <dir>]` | 0 predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1`;1 otherwise;2 could-not-evaluate | none: the frozen SR7-SR9 rows and the bound wave-2 verdicts are the measurement; controls `.ufo/waves/round-44/controls/run_controls_c2.py` | R44 C2 frozen sha256 `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059`; snapshots sha256 in `.ufo/waves/round-44/frozen/src/SHA256SUMS` | committed reads | tsukuroi |
| census-readers-r45 | gate | `python3 tools/score-census-readers-r45.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `lexical_hits == 0 and sites_found == 5 and equiv_ok == 5 and selftest_pass == 1 and selftest_r45 >= 6 and revert_killed == 6 and adjacency_ok == 1`;1 otherwise;2 usage/harness error | none: the lexical leg, the per-site equivalence draws, the census selftest, six revert mutants and the adjacency gate are the measurement; controls `.ufo/waves/round-45/controls/run_controls_c1.py` | R45 C1 frozen sha256 `fe0e31e25c5b3c92cc5aace48acc56bc6dab39b4b3c09b49708a715a3250bd50`; base `5bbd5ff588120fd8e7c744695351a6978b4241c1` | scratch clone and census runs under `--scratch`; no host write | tsukuroi |
| scrub-grounding-r45 | gate | `python3 tools/check-scrub-grounding-r45.py --revision <REV> [--lane <repo>] [--sessions <dir>]` | 0 predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1`;1 otherwise;2 usage/read error | none: the frozen GR1-GR3 rows and the bound a2w1/a2r1 verdicts are the measurement; controls `.ufo/waves/round-45/controls-a2/run_controls_c2.py` | R45 C2 sha256 `a1eb402dffae97fcefd9bd539529f1cacc5034419b6de06e1f8ac1c08d011331` (attempt-2 rebinding of frozen `7e373196decd2de09124819f81008f42dbf9fe2e56a9231b3b692f841eabf70d`); snapshots sha256 in `.ufo/waves/round-45/frozen/src/SHA256SUMS` | committed reads | tsukuroi |

## Census identity — round 46

Appended 2026-10-27 (round-46 C1; drafted by wave seat ScribeSkill, integrated by the L1 against the hardened
implementation `61e06740`). Base `2042117c`; first landing `a4477049`; hardened `61e06740` after wave w1 (seat
C1LabUlimit's wrong-digest reproducer and seat C1RevImpl's `--identity --help` finding). Entry
`corpus/knowledge/census-identity-r46.md`; evidence `.ufo/waves/round-46/`.

Surface: `bash tools/tsukuroi-census.sh --identity` prints one `TSUKUROI_CENSUS_IDENTITY:` line and exits 0 before any
plane probe, so a reader names the census bytes with one command instead of three (routed debt D12,
`corpus/knowledge/closeout-r11.md:42-44`). `VERSION` stays the literal `census-v2` and names nothing: identity is the
sha256.

| Observation | Reading | Action |
|---|---|---|
| `sha256=<64 hex> md5=<32 hex> bytes=<n> lines=<n> verified=yes` | exactly one descriptor of 10 or more is a regular file, resolves to `readlink -f` of the invoked path and carries `O_CLOEXEC` (the flag bash sets on its script descriptor, S250 `shell.c:1703`), and two sha256 reads through it agree | quote the sha256 with any census verdict; `lines` counts newline bytes (the file ends without one, so an editor shows one more line) |
| the four byte fields read `unverifiable`, `verified=no` | the script came from stdin or a pipe, the path was relinked after bash opened the script, more than one descriptor qualified, a parent-held descriptor without `O_CLOEXEC` was the only match, or the descriptor limit put the script below 10 | an unknown, never a guess: re-run as `bash <path> --identity` from a plain shell |
| `tsukuroi-census: --identity takes no other argument` on stderr, exit 2 | `--identity` was given with any other argument, `--help` included | a usage error, not a reading |
| the sha256 fed to the `git log` loop in the entry's "Re-deriving the revision from the line" prints commit hashes | the first hash printed is the newest commit carrying those bytes; no output means an uncommitted local edit | re-derive the revision before quoting a census verdict |

Counter: `python3 tools/score-census-identity-r46.py --revision <REV> --scratch <DIR> [--lane <repo>]` — PASS iff
`identity_ok == 1 and tracks_ok == 1 and symlink_ok == 1 and unverifiable_ok == 1 and cli_ok == 1 and nowrite_ok == 1
and selftest_pass == 1 and selftest_r46 >= 4`. Pre-data controls: `.ufo/waves/round-46/controls/battery-summary-c1.jsonl`
(9/9 as declared; the first counter draft let the path-hasher K2 PASS, `battery-summary-c1-draft1.jsonl`, fixed before
the freeze). Selftest 154 → 162 cases, eight `(R46-C1)`.

Recorded limits: bash behaviour is pinned at tag bash-5.3, the host runs 5.3.20 (the scout seat C1ScoutBashSrc read the
patch set); `verified=yes` does not prove the bytes bash parsed equal the bytes hashed when the file is edited in place
during a run (bash reads in pieces); code that runs inside the census process before `main` (a `BASH_ENV` file) is out
of scope; the frozen counter does not exercise the parent-held-descriptor case (the selftest does) and its `nowrite_ok`
watches cwd and TMPDIR only (seat C1RevCounter).

## Scrub record — round 44 status note (routed defect D1; appended 2026-10-27)

Appended; `SKILL.md:4214` "Scrub record — round 44 rows" and its Limits block stay as written and no row above gains
or loses a word. The mark that section lacks is this: Round 44's depth gate FAILED — `verdicts_ok 0` — at
`tools/check-scrub-record-r44.py --revision fbfef071` (`FAIL`: `.ufo/waves/round-44/after/c2-final-fbfef071.jsonl`,
`corpus/lessons/round-44-verifier-spotcheck.md:84,133,185-186`), so SR7, SR8 and SR9 stay **pending**, not admitted:
read them as source-checked statements that no counted seat has bound (their grounding rows GR1-GR3 are the round-45
entry's, gated separately). Capture: `.ufo/waves/round-46/l1-capture/scribe-d1.txt:1` — the counter's own line,
`verdicts_ok 0`.

## Gate and probe registry — round46 superseding current rows

Append-only continuation; every row of the round-45 table is carried verbatim below, then the two round-46 rows.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| child-env-allowlist-r36 | probe | `python3 tools/probe-child-env-allowlist-r36.py --revision <REV> --set livefive` | last-line `leaking` 0 clean / > 0 leaking; exit 0 clean, 1 leaking, 2 harness | none hermetic; sensitivity battery per `.ufo/waves/round-36/l1/` (claim/r33claim 0 at base) and the w2 live-mode detector receipts | VERSION 7; predicate label `leaking`; frozen bytes sha256 `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` at `1e926801195e304950e3eb9d2525ef8bbc245089` | committed reads; sandbox clones; no lane or host write | tsukuroi |
| host-census | gate | `bash tools/tsukuroi-census.sh` (not live-run round22) | 0 HEALTHY/clean;1 DEGRADED/failed;2 BLOCKED/could-not-evaluate | `bash tools/tsukuroi-census.sh --selftest` | six-plane fixed fixture assertions in tool | live probes only when separately authorized; selftest private fixtures | tsukuroi |
| root-dac-correction | gate | `python3 tools/check-root-dac-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-root-dac-correction.py --selftest` | R13 fixed correction/source bindings | committed reads; selftest private clones | tsukuroi |
| source-scope-correction | gate | `python3 tools/check-source-scope-correction.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-source-scope-correction.py --selftest` | R14 exact claims/source bindings | committed reads; selftest private clones | tsukuroi |
| locator-clarification | gate | `python3 tools/check-locator-clarification.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-locator-clarification.py --selftest` | R15 source/positive-definition fields | committed reads; selftest private clones | tsukuroi |
| update-recheck | probe | `python3 tools/measure-update-recheck.py --revision <REV>` | 0 COUNTED/ABSENT observation, not health clearance;2 could-not-evaluate;1 only selftest FAIL | `python3 tools/measure-update-recheck.py --selftest` | R15 fixed snapshot/probe/schema expectations | committed reads; selftest private clones | tsukuroi |
| section-citations | gate | `python3 tools/check-section-citations.py --revision <REV>` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-section-citations.py --selftest` | R16 exact heading/table/quote; old JSON oracle non-normative | committed reads; selftest private clones | tsukuroi |
| boot-chain | gate | `python3 tools/check-boot-chain.py --revision <REV> [--statement-corrections]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-chain.py --selftest` | R17 schema/image rules; R18 four fixed corrections and source/digest/mtime bindings | committed reads; selftest private clones; no boot write | tsukuroi |
| boot-chain-audit | probe | `bash tools/boot-chain-audit.sh --live` (not live-run round20) | live: 0 CONSISTENT/observation;2 UNKNOWN/could-not-evaluate; selftest: 0 PASS;1 FAIL; usage: 2 could-not-evaluate; no live DEGRADED; not operator clearance | `bash tools/boot-chain-audit.sh --selftest` | schema-v2 summary emits0/2; finite per-entry rules; not operator clearance | private fixtures; live reads only when separately authorized; no host writes | tsukuroi |
| freshness-r17 | gate | `python3 tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-freshness-r17.py --selftest` | immutable R17 registry48 and source/notice bindings | committed reads; selftest private clones | tsukuroi |
| appended-notices | gate | `python3 tools/check-appended-notices.py --revision <REV> [--registry <PATH>] [--registry-from <REV>]` | 0 structural clean;1 failed;2 could-not-evaluate; not semantic proof | `python3 tools/check-appended-notices.py --selftest` | R18 fixed source/notice registry, baseline842a531 | committed reads; selftest private fixtures | tsukuroi |
| recheck-commands | gate | `python3 tools/check-recheck-commands.py --revision <REV> [--paths ...] [--exec-log <PATH>]` | 0 bounded clean;1 failed including EXEC-STEER-VIOLATION;2 could-not-evaluate | `python3 tools/check-recheck-commands.py --selftest` | operative directives and finite systemctl/wrapper/shell policy; not exhaustive shell analysis | committed reads; selftest private fixtures | tsukuroi |
| seat-scope | gate | `python3 tools/check-seat-scope.py --wave <DIR> --revision <REV>` | 0 bounded declarations clean;1 unauthorized/undeclared/missing/malformed declaration;2 could-not-evaluate | `python3 tools/check-seat-scope.py --selftest` | declared execution, not independent request audit | committed reads; selftest private fixtures | tsukuroi |
| revision-binding | gate | `python3 tools/check-revision-binding.py --tools-revision <REV> [--object-selectors] [--object-target-types]` | 0 finite original-nine mode clean;1 failed;2 could-not-evaluate; discovered tools separate | `python3 tools/check-revision-binding.py --selftest` | earlier matrices unchanged; target mode availability once; actual behavior separate; finite witnesses only | disposable external clone/ref/probe commits; never lane Git writes | tsukuroi |
| revision-binder | library | import `tools/_revision.py`; no direct CLI | 0 selftest PASS;1 selftest FAIL;64 usage | `python3 tools/_revision.py --selftest` | first-failure branch/object/local/origin binding; typed object-only selectors | Git reads; selftest private repository only | tsukuroi |
| adjacency-anchors | gate | `python3 tools/check-adjacency-anchors.py --revision <REV> [--registry-from <REV>] [--ownership-corrections]` | 0 clean;1 failed including OWNERSHIP-CORRECTION-MISSING/INVALID;2 could-not-evaluate | `python3 tools/check-adjacency-anchors.py --selftest` | fixed10/114 census and named ownership correction; not arbitration award | immutable reads; default siblings read-only; selftest private fixtures | tsukuroi |
| boot-writers | gate | `python3 tools/check-boot-writers.py --revision <REV> [--registry-from <REV>]` | 0 clean;1 failed;2 could-not-evaluate | `python3 tools/check-boot-writers.py --selftest` | finite captured events/classes/mechanism quotes and digests; not content-write proof | committed reads; selftest private fixtures | tsukuroi |
| registry-coverage | gate | `python3 tools/check-registry-coverage.py --revision <REV> [--baseline-tools <REV>] [--audit-live-map]` | 0 clean;1 failed including REGISTRY-AUDIT-LIVE-MAP;2 could-not-evaluate | `python3 tools/check-registry-coverage.py --selftest` | highest-table coverage; opt-in live0/2 versus selftest1 map, not universal semantics | committed reads; selftest private fixtures | tsukuroi |
| selector-contract | gate | `python3 tools/check-selector-contract.py --revision <REV>` | 0 source-contract clean;1 missing/wrong decision/table/source/policy;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-selector-contract.py --selftest` | fixed five typed decisions; corrected r21 entry; not actual consumers or host state | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-snapshots | gate | `python3 tools/check-review-snapshots.py --revision <REV> [--manifest <PATH>]` | 0 declared bytes/predicate/scope clean;1 missing/mismatched receipt;2 schema/path/revision/read/CLI could-not-evaluate | `python3 tools/check-review-snapshots.py --selftest` | preregistered primary SHA/predicate; never reading/nonexecution proof | immutable reads; selftest in-memory fixtures | tsukuroi |
| boundary-contract | gate | `python3 tools/check-boundary-contract.py --revision <REV>` | 0 six fixed policy decisions clean;1 missing/wrong decision/source/limit;2 schema/CLI/revision/read could-not-evaluate | `python3 tools/check-boundary-contract.py --selftest` | fixed six tuples and visible table, S083/S084 and explicit no-native-enforcement limit | immutable reads; selftest in-memory fixtures | tsukuroi |
| seat-bindings | gate | `python3 tools/check-seat-bindings.py --revision <REV> --manifest <PATH> --events <PATH>` | 0 available recorded requests within declarations;1 missing binding or observed violation;2 malformed/incomplete/unavailable evidence or revision/CLI/read could-not-evaluate | `python3 tools/check-seat-bindings.py --selftest` | v1 unchanged; explicit v2 edit_paths subset of read+write, two finite structured key shapes, recursive schema-only authority; body opaque, post-hoc only | immutable reads; selftest in-memory fixtures | tsukuroi |
| review-cohort | gate | `python3 tools/check-review-cohort.py --revision <REV> --manifest <PATH> --settlement <PATH>` | 0 accounted cohort, strict faults separately red;1 missing manifest or absent-unresolved;2 malformed/unavailable/schema/revision/CLI/read could-not-evaluate | `python3 tools/check-review-cohort.py --selftest` | exact cohort bijection, four receipt-only buckets, unchanged strict evaluator/findings and measured report SHA | immutable reads; selftest in-memory fixtures | tsukuroi |
| edit-contract | gate | `python3 tools/check-edit-contract.py --revision <REV>` | 0 fixed eight-row/source/policy/table clean;1 missing/wrong row/source/limit;2 schema/revision/read/CLI could-not-evaluate | `python3 tools/check-edit-contract.py --selftest` | exact eight id/decision/reason/evidence/policy tuples; S086 shapes only, separately frozen preregister policy | immutable Git reads; selftest in-memory | tsukuroi |
| path-reconciliation | gate | `python3 tools/check-path-reconciliation.py --revision <REV>` | 0 both fixed cohorts explained;1 missing/mismatched/unexplained ledger;2 tampered/missing/malformed snapshot/revision/read/CLI could-not-evaluate | `python3 tools/check-path-reconciliation.py --selftest` | frozen r22 input digests; exhaustive per-event ledger; rough25/33 vs retained23/29 with 2+4 raw-first selector disagreements | immutable Git reads; selftest in-memory | tsukuroi |
| red-causes | gate | `python3 tools/report-red-causes.py --revision <REV>` | 0 all findings attributed and preserved invariants hold;1 attribution incomplete or invariant broken;2 could-not-evaluate | `python3 tools/report-red-causes.py --selftest` | frozen round-23 falsify cohort bytes (checker, manifest, events, limit file) and their digests; input digests pinned to the f169b3ba blobs and the 266/1/1 split required; each event finding re-classified by the frozen checker and given a checker-branch subcause; the one seat-level finding has no tool operation; status CANNOT_EVALUATE, exit 2, the incomplete seat and the unrecoverable extra key stay visible; no re-grading | immutable reads; selftest in-memory fixtures | tsukuroi |
| pause-gate | gate | `python3 tools/check-pause-gate.py --revision <REV>` | 0 five premises verified;1 premise unverified or gate entry invalid;2 could-not-evaluate | `python3 tools/check-pause-gate.py --selftest` | R24 pause-lift gate entry schema tsukuroi-pause-gate-v1; fixed premise ids P1-P5; every evidence pointer resolves at the bound revision and every source id is a mined corpus/SOURCES.md row opened 2026-10-22 whose used-by names the gate; at least one unique non-boilerplate pointer per premise into the sha256-pinned capture l1-4; only cleared, still-holds or changed verdicts count; committed-bytes evidence link count only, not a host re-measurement and not pause-lift clearance | immutable reads; selftest in-memory fixtures | tsukuroi |
| self-assessment | gate | `python3 tools/check-self-assessment.py --revision <REV>` | 0 all 27 fixed checks match;1 one or more mismatch;2 could-not-evaluate | `python3 tools/check-self-assessment.py --selftest` | R26 fixed check set K01 to K27 read at the bound revision; R27 (QUALITY 65, commit 5583d75c): K01 to K06 read only the latest measured-outcome record of a round earlier than the declaring round, heading anchored; a measured self-assessment only, never a host verdict | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| memory-pressure | gate | `python3 tools/check-memory-pressure.py --revision <REV>` | 0 six rows MP1 to MP6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-memory-pressure.py --selftest` | R25 fixed row set MP1 to MP6 with the capture sha256 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| storage-health | gate | `python3 tools/check-storage-health.py --revision <REV>` | 0 six rows SH1 to SH6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-storage-health.py --selftest` | R26 fixed row set SH1 to SH6 with the capture sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd` and the per-row source, quote and pointer rules; committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| kernel-taint | gate | `python3 tools/check-kernel-taint.py --revision <REV> [--repo <PATH>] [--branch <NAME>]` | 0 six rows KT1 to KT6 verified;1 one or more row or evidence invalid;2 could-not-evaluate | `python3 tools/check-kernel-taint.py --selftest` | R27 fixed row set KT1 to KT6 with the capture sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, the per-row source, Gate located-quote equality and capture-pointer rules; counts complete evidence links, not verdict truth; R28 adds R4a (a quote of at least 2 words and 16 non-whitespace characters), R4b (a quote source the row does not cite is blocking) and R4c (Gate read only under the exact `## Gate` title, source id only from the Source column); committed evidence only, never a host re-measurement | immutable Git reads at the bound revision; selftest private temporary fixtures | tsukuroi |
| adjacency-overlap | gate | `python3 tools/check-adjacency-overlap.py --revision <REV> [--repo <PATH>] [--siblings-root <DIR>]` | 0 six rows OV1 to OV6 anchored;1 one or more row or anchor invalid;2 could-not-evaluate | `python3 tools/check-adjacency-overlap.py --selftest` | R27 fixed row set OV1 to OV6 against mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` and the pinned blob sha256 `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`; counts resolvable anchors, not the class or owner judgement; R28 adds B1 to B7 (exact six object rows, pinned sibling path and snapshot field, no heading in the quote window, quotes of at least 4 words, lane side outside `.ufo/` and the register, at most one LANE-GAP row with a null lane side, PROVINCE owner and class agree) | immutable Git reads at the bound revision and read-only sibling Git reads; selftest private temporary fixtures | tsukuroi |
| adjacency-battery | probe | `python3 tools/mutants-adjacency-overlap.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--siblings-root <DIR>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `adjacency-overlap`; its counts are re-derived by wave seats | R28 C1: the 24 should-fail register mutants of round-27 CritC2Tool (`driver.py` plus `driver2.py`), each run with the live sibling root and an empty one; accepted means exit 0 with anchored_rows 6 | private mkdtemp sandbox from `git archive`; read-only lane and sibling Git reads | tsukuroi |
| kernel-taint-battery | probe | `python3 tools/mutants-kernel-taint.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 battery ran and printed its summary (a count, not a pass);1 harness error with a traceback;2 not emitted | none: the battery is itself a should-fail check of `kernel-taint`; its counts are re-derived by wave seats | R28 C2: the round-27 CritC1Tool data mutants; declared should-fail set generic_word_quote, generic_word_quote_the, quote_from_uncited_rejected_source, gate_heading_investigate, gate_source_from_location_cell; accepted means exit 0 with verified_rows 6; other accepted mutants are listed, not counted | private mkdtemp scratch repo from `git archive`; read-only lane Git reads | tsukuroi |
| owed-statements-r29 | gate | `python3 tools/check-owed-statements-r29.py --revision <REV> [--lane <repo>]` | 0 all twelve owed statements marked;1 unmarked or invalid marker;2 could-not-evaluate | none: no self-test mode; a counter run at the bound revision is the measurement | R29 C1: twelve frozen anchors O01 to O12 (four OOM "+200 band" readings, three MP4 qualifier statements, the driver-firmware [unk], four storage-health statements) and marker rules M1 to M7 at base 16e9ab2a; counts valid source-backed markers, not the truth of a correction | committed Git reads only (`git show`, `git cat-file`, children get the round-32 allow-list environment); one private temporary HOME directory created at module load and removed at exit (round 32, wave-2 CritNoHarm); no other writes | tsukuroi |
| git-env-leak | probe | `python3 tools/probe-git-env-leak.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leak and no harness error;1 one target leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eight-target control and canary runs are the measurement | R29 C2: eight frozen write-capable lane tools at base 16e9ab2a, each run once with every GIT_* removed and once with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE at a private canary; a leak is a changed canary fingerprint (HEAD, refs, loose and packed objects, index digest) or a control/canary exit-code divergence; counts observed leaks, not general tool safety | private mkdtemp scratch (git archive export plus a bare clone); canary commits confined there; never the lane; read-only lane Git reads | tsukuroi |
| owed-statements-battery | probe | `python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no should-fail shape accepted, no crash;1 a should-fail shape accepted, a crash or a short control;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-1 CritOwedCounterShapes marker shapes (25 should-fail, 7 should-pass) over a control with all twelve markers; accepted means the shape's item is counted | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed; read-only toward the lane | tsukuroi |
| owed-statements-landed-battery | probe | `python3 tools/mutants-owed-statements-r29-landed.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>]` | 0 control 12 of 12, no mechanical should-fail shape accepted, no should-pass shape refused, no crash;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R29 C1: round-29 wave-2 CritOwedV2Shapes shapes over the landed markers (19 mechanical should-fail, 7 semantic reported but not gated, 1 should-pass) | private mkdtemp clone of the lane under scratch; every git child runs with inherited GIT_* removed and global/system config at /dev/null; read-only toward the lane | tsukuroi |
| btrfs-space-r30 | gate | `python3 tools/check-btrfs-space-r30.py --revision <REV> [--lane <repo>]` | 0 all ten rows D01 to D10 verified;1 one or more row unverified;2 could-not-evaluate (revision or base registry unreadable) | none: no self-test mode; fixture mode `--tree <DIR> --base-sources <FILE>` is exercised by the battery `mutants-btrfs-space-r30` | R30 C1: ten frozen questions D01 to D10 with frozen tokens, base `fbfec6bd`, rules R1 to R9; declared version 1 sha256 `1bf7ee14467accac5281e6ebd881db24c8ab682066e9f50ddbb0fe76a931c079` (commit `8fb2cef0`), version 2 after the wave-1 attacks | committed reads only | tsukuroi |
| btrfs-space-battery | probe | `python3 tools/mutants-btrfs-space-r30.py [--counter <path>] [--keep]` | 0 control 10, no should-fail shape accepted and no should-pass shape refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `btrfs-space-r30`; its counts are re-derived by wave seats | R30 C1 (QUALITY 73): synthetic fixture, 72 should-fail and 11 should-pass shapes in version 2 (46 and 6 at the declaration) | private temporary directory; no git | tsukuroi |
| git-env-residual | probe | `python3 tools/probe-git-env-residual-r30.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness error;1 a pair leaks;2 could-not-evaluate on a harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R30 C2: eleven frozen git-writing tools, channels path-wrapper, user-files and enclosing-repo (33 pairs); probe sha256 `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| run-receipt | probe | `python3 tools/run-receipt.py --revision <REV> [--tool-revision <REV>] --out <FILE> [--lane <repo>] [--timeout <s>] -- <tool> [args...]` | 0 the tool exited 0;1 the tool exited 1 (its own verdict);2 revision or tool unreadable, or the tool's own could-not-evaluate | none: no self-test mode; the receipt header (revision, tool revision, tool sha256) is the evidence | R30 routed defect 1 (QUALITY 77): runs a tracked tool from a sandbox clone at the tool revision with a private HOME and writes header, stdout and footer | the `--out` receipt file; sandbox clone under `/fast/scratch/hyaku` | tsukuroi |
| report-receipts | gate | `python3 tools/check-report-receipts.py --report <PATH> --lane <repo> --revision <REV>` | 0 every revision-cited gate or measurement has a committed receipt;1 one or more citation unreceipted;2 could-not-evaluate (report or revision unreadable) | `python3 tools/check-report-receipts.py --selftest` | R30 mined mistake R30-UNRECEIPTED-GATES (QUALITY 77): exits 1 on the round-29 report at lane `8976ca92` (Gates at `434a7903`) | committed reads; selftest private fixtures | tsukuroi |
| owed-statements-v4shapes-battery | probe | `python3 tools/mutants-owed-statements-r29-v4shapes.py --base <REV with markers> (--counter-rev <REV> \| --counter-file <PATH>) [--lane <PATH>] [--keep]` | 0 control 12, no routed v4 shape accepted, no control refused;1 otherwise;2 not emitted | none: the battery is itself a should-fail check of `owed-statements-r29`; its counts are re-derived by wave seats | R30 routed defect 2 of the round-29 spot-check: closed-comment, list-indented, extra-JSON-key and asterisk-id shapes; counter v5 sha256 `6fadf5fbb77579a8a49db36a560de20b20aa2bd3d3f6928218c640b1465c475b` refuses 11 of 11 (v4 `3516d579…` accepted 11 of 11) | private clone under `/fast/scratch/hyaku` | tsukuroi |
| btrfs-repair-r31 | gate | `python3 tools/check-btrfs-repair-r31.py --revision <REV> [--lane <repo>]` | 0 all eight Q01-Q08 rows new_sourced;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen Q01-Q08 question set is measured by the counter | R31 C1: frozen predicate new_sourced; rules R1-R8; six pinned btrfs-progs v7.1 documentation snapshot sha256 values | committed Git reads only | tsukuroi |
| git-child-env-r31 | probe | `python3 tools/probe-git-child-env-r31.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...] [--channels <ch> ...]` | 0 no leaking pair and no harness errors;1 one or more (tool, channel) pairs leak;2 harness error | none: no self-test mode; the eleven-target control and three-channel runs are the measurement | R31 C2: eleven frozen tools and channels loader-env, child-contract and dotgit-pointer; parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku`; canary repositories only | tsukuroi |
| census-handoff-r32 | gate | `python3 tools/score-census-handoff-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--seed <hex>] [--scenarios N]` | 0 every fixture scenario routed and both live views consistent;1 one or more scenarios unrouted or a live view inconsistent;2 harness error (planted facts not visible in the base census, a non-hermetic run, or a vacuous live check) | none: no self-test mode; 24 seeded fixture scenarios plus two read-only live views are the measurement | R32 C1 v3: base census 58cc2e0b; HANDOFF ADJ-04 mori grammar `class= value= kind= state=`; scenario types none, kill-events, coredumps, both, cumulative-only, cumulative+coredumps, tsukuroi-only | private scratch under the system temp dir; reads the live host read-only | tsukuroi |
| child-env-allowlist-r32 | probe | `python3 tools/probe-child-env-allowlist-r32.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--only <tool> ...]` | 0 no leaking target and no harness errors;1 one or more targets leak an injected name or break parity;2 harness error | none: no self-test mode; the eleven-target control and ambient-names runs are the measurement | R32 C2 v2: eleven frozen tools; BASH_ENV, ENV, GCONV_PATH, PERL5OPT plus eight per-run random names (four of length 2-20, four of 21-200); parity is exit code, normalized stdout digest and git-exec count | private scratch under `/fast/scratch/hyaku` | tsukuroi |
| child-env-allowlist-r33 | probe | `python3 tools/probe-child-env-allowlist-r33.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|regression] [--only <tool> ...]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the five-target claim set and channels names, quiet and source are the measurement | R33 C1 probe v3 frozen at 9c89ff4f093d07a6f92925518310ca6a7c8a2fa0, sha256 c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd; claim set 5 targets, channels names, quiet, source, 15 pairs; label leaking; `--set regression` is repair evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| child-env-allowlist-r34 | probe | `python3 tools/probe-child-env-allowlist-r34.py --revision <REV> [--lane <repo>] [--scratch <dir>] [--set claim\|r33claim\|regression] [--only <tool> ...] [--base <REV>]` | 0 when leaking is 0 and harness_errors is empty;1 when a pair leaks;2 on a harness error | none: no self-test mode; the nine-target claim set and channels names, quiet and source are the measurement | R34 C1 probe VERSION 5 after pre-data amendment 1 at 15c9ac0e1b02917f43c0bc016d6060f888cb603a, sha256 5231dbafc472ff42e041cbaad3f48dd8bd204d58b6ab22e497cf9372b23d6bfd; claim set 9 targets, channels names, quiet, source, 27 pairs; base parity against the claim base 2641591e303057cd0f67e190a6bdf7fa91a45c31; label leaking; `--set r33claim` and `--set regression` are no-harm evidence, not the claim | private mkdtemp (default `/fast/scratch/hyaku` when that directory exists), bare clone and strace, removed at exit; refuses a scratch inside the lane | tsukuroi |
| knowledge-header | gate | `python3 tools/check-knowledge-header.py --revision <REV> [--lane <repo>] [--branch <BRANCH>]` | 0 every corpus/knowledge/*.md carries source:, verified-at: (ISO date) and recheck: (ISO date or cadence);1 one or more KNOWLEDGE-HEADER-MISSING or KNOWLEDGE-HEADER-VALUE findings;2 could-not-evaluate | `python3 tools/check-knowledge-header.py --selftest` | QUALITY 8; red at 6de666c427ba9aa6b4350561980bde8d0e7c261d on kill-oom-boundary-r33.md (and nine recheck cadence findings) before the round-34 fix | committed reads; selftest private fixtures | tsukuroi |
| score-pacnew-arm-r35 | probe | `python3 tools/score-pacnew-arm-r35.py --lane <repo> --revision <REV>` | 0 every fixture matches;1 any fixture does not match;2 harness error | none (pre-freeze control wave receipts `.ufo/waves/round-35/w1/K*/`) | VERSION 1 sha256 19d25d14…; met by controls K08FixtureKeyed and K15FieldMutants, so not a claim counter | private temp fixtures only; reads committed census bytes | tsukuroi |
| score-pacnew-arm-r35b | probe | `python3 tools/score-pacnew-arm-r35b.py --lane <repo> --revision <REV> [--skip-battery]` | 0 candidate and control match every view and no should-fail arm is accepted;1 otherwise;2 harness error | the battery itself (control arm plus 17 should-fail arms) | VERSION 2 sha256 7517af92…; 20 stub, 3 namespace, 1 live view; claim base b40c01df | private temp fixtures; unprivileged user+mount namespace; live view reads /etc names and pacman.log read-only | tsukuroi |
| journalctl-v262-corrections-r37 | gate | `python3 tools/check-journalctl-v262-corrections.py --revision <REV>` | 0 three fixed correction clusters match;1 missing/wrong correction;2 unreadable revision or CLI | `python3 tools/check-journalctl-v262-corrections.py --selftest` | Round37 correction block: exact 15 `field_list_has_scope_options()` terms; separate observed `-n -F` truncation and unchanged `-n -N` output; `--list-boots` action replacement; prior S024/round-1 teaching acknowledged | immutable Git read of the note; selftest in-memory fixtures | tsukuroi |
| child-env-allowlist-r37 | probe | `python3 tools/probe-child-env-allowlist-r37.py --revision <REV> --set livefive` | 0 `leaking` 0 and `harness_errors` empty;1 leaking pair;2 harness error | none; direct livefive receipt at `.ufo/waves/round-37/before/v8-livefive-baseline.jsonl` | VERSION 8; sha256 `9aee085b45d7566d6ce398733c10d3d87ae29bce107c4bd13fcdffcb4854b064`; 5 targets/15 predicate pairs; untraced is supplemental diagnostic only; base 564db0b | immutable target exports and disposable clones; no lane or host write | tsukuroi |
| storage-arm-r38 | gate | `python3 tools/score-storage-arm-r38.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 ten fixtures, the live leg and six PLANE lines per run match;1 any fixture, the live leg or the plane count differs;2 revision, git or bash could-not-evaluate | none: the ten built-in fixtures F01-F10 and the live leg are the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` | R38 C1 frozen at `7cbaeb63`, sha256 `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`; QUALITY 82 gap: a fixture-gated arm passes it (`controls-q82.jsonl`), so it is used only with `storage-arm-r38-q82` | private mkdtemp fixtures under `--scratch`/`TMPDIR`; reads the census at REV through git; no host write | tsukuroi |
| storage-arm-r38-q82 | gate | `python3 tools/score-storage-arm-r38-q82.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 every production-path view matches;1 a view differs;2 revision, unshare or v1-model digest could-not-evaluate | none: three per-run random views are the measurement; controls `.ufo/waves/round-38/controls/controls-q82.jsonl` (fixture-gated 0/3, cached-live 1/3, real arm 3/3) | R38 pre-seat amendment `9c9bb647`, sha256 `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3`; loads the v1 model from `7cbaeb63` by digest | `unshare -rm` child namespace with a bind mount over `/sys/fs/btrfs` that never leaves it; scratch under `--scratch`/`TMPDIR` | tsukuroi |
| hook-order-r38 | gate | `python3 tools/check-hook-order-r38.py --revision <REV> [--repo <PATH>]` | 0 all 69 rows match the frozen capture and the cited rows are mined, used-by the entry and opened 2026-10-26;1 a missing, wrong, extra or duplicate row or a source problem;2 revision, git or capture_tampered could-not-evaluate | none: the frozen capture is the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` (base, full-name sort, no override, no source FAIL; correct PASS) | R38 C2 frozen at `7cbaeb63`, sha256 `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`; capture MANIFEST sha256 `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`; libalpm order model of pacman 54d9411 | reads the entry and SOURCES at REV through git and the digest-verified capture from the work tree; no write | tsukuroi |
| storage-hidden-r39 | gate | `python3 tools/score-storage-hidden-r39.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 both hidden-root legs BLOCKED mounts:btrfs-without-sysfs, three tmpfs views, five fixtures, the live leg and six PLANE lines per run match;1 any leg differs;2 revision, git, unshare or no STORAGE line from the namespace legs | none: the hidden legs H1/H2, views V0-V2, fixtures F1-F5 and the live leg are the measurement; controls `.ufo/waves/round-39/controls/` | R39 C1 frozen at the round-39 freeze commit, sha256 `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973`; views are tmpfs mounts filled from stdin inside the child (R38-Q82-LEAK) | `unshare -rm` child namespace with tmpfs mounts that never leave it; scratch under `--scratch`/`TMPDIR` | tsukuroi |
| transaction-order-r39 | gate | `python3 tools/check-transaction-order-r39.py --revision <REV> [--repo <PATH>]` | 0 TO1-TO8 each quoted from the pinned libalpm snapshot at the cited lines on a mined upstream row named on `source:`, no duplicate row or heading, two host counts present, 0 running lines inside a commit phase;1 any of these fails;2 revision, git or frozen input tampered | none: the frozen snapshots and capture are the measurement; controls `.ufo/waves/round-39/controls/` | R39 C2 frozen at the round-39 freeze commit, sha256 `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`; snapshot sha256 pins in code; capture MANIFEST sha256 `cb5cb4f436b93f22886ceac79b5a84c1b3b34256f671fb51d05c1b3af02c1bb4` | reads the entry and SOURCES at REV through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| selftest-literals-r40 | gate | `python3 tools/score-selftest-literals-r40.py --revision <REV> --scratch <DIR> [--repo <PATH>] [--jobs N]` | 0 the unmutated census selftest PASSes, three neutral rewrites of the mount-table arm PASS, all nine frozen literal/guard mutants apply once and each fails the selftest, and the census holds 5 self-reference lines;1 any of these fails;2 revision, git or scratch could-not-evaluate | none: the nine mutants and three neutral rewrites are the measurement; controls `.ufo/waves/round-40/controls/` | R40 C1 frozen at the round-40 freeze commit, sha256 `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159`; mutant texts and SELFREF_BASE 5 in code | writes only a private directory under `--scratch`, removed before exit; reads the census at REV through git | tsukuroi |
| exec-environment-r40 | gate | `python3 tools/check-exec-environment-r40.py --revision <REV> [--repo <PATH>]` | 0 EX1-EX8 each carry the source-derived value, the frozen proposition tokens and no negation word in the rule cell, a 4-25 word quote at the cited lines of the pinned snapshot on a new mined upstream row named on `source:`, no duplicate row or heading, two host values present, 0 base hits of the novelty tokens;1 any of these fails;2 revision, git, frozen input tampered or a derivation pattern unmatched | none: the frozen snapshots and capture are the measurement; controls `.ufo/waves/round-40/controls/` | R40 C2 frozen at the round-40 freeze commit, sha256 `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`; snapshot sha256 pins in code; capture MANIFEST sha256 `57888c10574736065bc74e48258ebff325322e95f659306642822a94e84411b5` | reads the entry and SOURCES at REV and BASE through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| selftest-mounts-r41 | gate | `python3 tools/score-selftest-mounts-r41.py --revision <REV> --scratch <DIR> [--repo <PATH>] [--jobs N] [--timeout S]` | 0 the unmutated census selftest PASSes, three neutral rewrites and one decoy (every mutant text in a dead here-document) PASS, all thirteen frozen mutants (M1-M9, H5, H6, H9, H10) apply once and each is killed twice on a baseline case label, and the captured fixture tables cover the four declared shapes (mountpoint not absolute, source not /dev, no subvol=, two btrfs lines) on BLOCKED cases;1 any of these fails;2 revision, git or scratch could-not-evaluate | none: the mutants, neutrals, decoy and capture are the measurement; controls `.ufo/waves/round-41/controls/` | R41 C1 frozen at the round-41 freeze commit, sha256 `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`; mutant, neutral and decoy texts in code | writes only a private directory under `--scratch`, removed on exit, SIGINT and SIGTERM; the capture line is injected only into the private copy | tsukuroi |
| package-anatomy-r41 | gate | `python3 tools/check-package-anatomy-r41.py --revision <REV> [--repo <PATH>]` | 0 PA1-PA8 each carry the source-derived value, the frozen proposition relations and no negation word, a 4-25 word quote inside the row's frozen source window on a new mined upstream row named on `source:`, a committed reviewer verdict `holds` and none `fails`, six host values present, no duplicate row or heading, 0 base hits of the novelty tokens;1 any of these fails;2 revision, git, frozen input tampered or a derivation pattern unmatched | none: the frozen snapshots, capture and verdict files are the measurement; controls `.ufo/waves/round-41/controls/` | R41 C2 frozen at the round-41 freeze commit, sha256 `c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f`; snapshot sha256 pins in code; capture MANIFEST sha256 `632ed0443cfb26ef002ebfd2a3a99971221f9129836b63135e0ca6ea41874f89` | reads the entry, SOURCES and verdict files at REV and BASE through git and the digest-verified frozen inputs from the tool's own tree; no write | tsukuroi |
| scrub-record-r42 | gate | `python3 tools/check-scrub-record-r42.py --revision <REV> [--lane <repo>]` | 0 SC1-SC5 present with quotes inside the frozen source windows, novelty verified, at least three host values, one mined source row and five wave-2 seat verdicts bound through `w2-dispatch.json` and `w2-results.json`;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen SC1-SC5 row set and the wave-2 verdict binding are the measurement | R42 C2 frozen predicate `rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1 and verdicts_ok == 5 and novelty_base_hits == 0`; pinned btrfs-progs v7.1 `cmds/scrub.c` and `CHANGES` snapshots listed in `.ufo/waves/round-42/frozen/src/SHA256SUMS` | committed Git reads only | tsukuroi |
| size-invariance-r42 | gate | `python3 tools/score-size-invariance-r42.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1` over ten P1-P6 and U1-U4 size twins and three `unshare -rm` production-path legs;1 any leg non-invariant or the census selftest not PASS;2 could-not-evaluate | none: no self-test mode; the ten fixture twins and the three namespace legs are the measurement | R42 C1 frozen counter sha256 `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`; 1 MiB verdict-neutral padding; fixtures built from the base census at `c8efaa3f` | private fixture copies under `--scratch`; `unshare -rm` namespace only for the N1/N3/N6 legs | tsukuroi |
| bootinputs-r43 | gate | `python3 tools/score-bootinputs-r43.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 16 and correct == 16 and identity_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r43 >= 2` over 16 production-path `boot_inputs_newer` cases in a private user+mount namespace, a live leg against an independent walk and the script's own selftest;1 any conjunct fails;2 could-not-evaluate (harness, namespace or read error) | none: no self-test mode; the 16 namespace cases, the live leg and the scored audit script's own `--selftest` are the measurement; controls `.ufo/waves/round-43/controls/run_controls_c1.py` | R43 C1 frozen counter sha256 `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f`; caller uid/gid through the `/etc/subuid` map and `setpriv`; mount-table, uid_map and script-path channels declared open | private `--scratch` only, removed on exit and on SIGINT/SIGTERM; tmpfs mounts only inside its own `unshare -m` namespace; reads the revision's script through `git show` | tsukuroi |
| scrub-record-r43 | gate | `python3 tools/check-scrub-record-r43.py --revision <REV> [--lane <repo>] [--sessions <dir>]` | 0 predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1` (SR1, SR3, SR6 of `corpus/knowledge/btrfs-scrub-record-r43.md`, wave-2 verdicts bound through `w2-dispatch.json`, `w2-results.json` and the report's first line);1 one or more conjuncts fail;2 could-not-evaluate | none: no self-test mode; the frozen SR rows and the bound wave-2 verdicts are the measurement; controls `.ufo/waves/round-43/controls/run_controls_c2.py` | R43 C2 frozen counter sha256 `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854`; snapshots scrub.c `48df2e2f…` (S237), ioctl.c `7b3488f2…` (S240), capture `f7ecbe7c…` (S241) | read-only: `git show` at the revision and session-transcript reads; writes nothing | tsukuroi |
| scrub-arm-r44 | gate | `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 16 and correct == 16 and identity_ok == 1 and wired_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r44 >= 6`;1 otherwise;2 usage/harness error | none: the 16 namespace cases, the wired leg, the live leg and the census selftest are the measurement; controls `.ufo/waves/round-44/controls/run_controls_c1.py` | R44 C1 frozen sha256 `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388`; candidate census sha256 `fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c` at freeze | private user+mount namespace under `--scratch`; live reads only; no host write | tsukuroi |
| scrub-record-r44 | gate | `python3 tools/check-scrub-record-r44.py --revision <REV> [--lane <repo>] [--sessions <dir>]` | 0 predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1`;1 otherwise;2 could-not-evaluate | none: the frozen SR7-SR9 rows and the bound wave-2 verdicts are the measurement; controls `.ufo/waves/round-44/controls/run_controls_c2.py` | R44 C2 frozen sha256 `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059`; snapshots sha256 in `.ufo/waves/round-44/frozen/src/SHA256SUMS` | committed reads | tsukuroi |
| census-readers-r45 | gate | `python3 tools/score-census-readers-r45.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `lexical_hits == 0 and sites_found == 5 and equiv_ok == 5 and selftest_pass == 1 and selftest_r45 >= 6 and revert_killed == 6 and adjacency_ok == 1`;1 otherwise;2 usage/harness error | none: the lexical leg, the per-site equivalence draws, the census selftest, six revert mutants and the adjacency gate are the measurement; controls `.ufo/waves/round-45/controls/run_controls_c1.py` | R45 C1 frozen sha256 `fe0e31e25c5b3c92cc5aace48acc56bc6dab39b4b3c09b49708a715a3250bd50`; base `5bbd5ff588120fd8e7c744695351a6978b4241c1` | scratch clone and census runs under `--scratch`; no host write | tsukuroi |
| scrub-grounding-r45 | gate | `python3 tools/check-scrub-grounding-r45.py --revision <REV> [--lane <repo>] [--sessions <dir>]` | 0 predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1`;1 otherwise;2 usage/read error | none: the frozen GR1-GR3 rows and the bound a2w1/a2r1 verdicts are the measurement; controls `.ufo/waves/round-45/controls-a2/run_controls_c2.py` | R45 C2 sha256 `a1eb402dffae97fcefd9bd539529f1cacc5034419b6de06e1f8ac1c08d011331` (attempt-2 rebinding of frozen `7e373196decd2de09124819f81008f42dbf9fe2e56a9231b3b692f841eabf70d`); snapshots sha256 in `.ufo/waves/round-45/frozen/src/SHA256SUMS` | committed reads | tsukuroi |
| census-identity-r46 | gate | `python3 tools/score-census-identity-r46.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `identity_ok == 1 and tracks_ok == 1 and symlink_ok == 1 and unverifiable_ok == 1 and cli_ok == 1 and nowrite_ok == 1 and selftest_pass == 1 and selftest_r46 >= 4`;1 any conjunct fails;2 usage/read error | none: no self-test mode of its own; the identity, tracks, symlink, three-unverifiable, cli and nowrite legs plus the scored census's own selftest and its four (R46-C1) case labels are the measurement; controls `.ufo/waves/round-46/controls/run_controls_c1.py` | R46 C1 frozen sha256 `7c406eb5f4ba1f6265649f7102e7376882483180c161a66abc68e08cad9524ba`; the one-line `TSUKUROI_CENSUS_IDENTITY:` shape, the four `unverifiable` byte fields and the `--identity` argument refusal in code; base `2042117c` | scratch fixtures and census runs under `--scratch`; identity runs leave their cwd byte-unchanged; no host write | tsukuroi |
| scrub-admission-r46 | gate | `python3 tools/check-scrub-admission-r46.py --revision <REV> [--lane <repo>] [--section-hash]` | 0 predicate `r45_legs_ok == 1 and verdicts_ok == 3 and marks_ok == 3`;1 otherwise;2 usage/read error or the base is not an ancestor | none: no self-test mode; the frozen round-45 non-verdict legs, the twelve counted seats' report-bound verdicts on the current GR section hashes and the three admission marks are the measurement; controls `.ufo/waves/round-46/controls/run_controls_c2.py` | R46 C2 frozen sha256 `28c409bef9a87338831e0cab4c194a78e7fedfefbd9c4a300a33f30b24dd11d8`; GR1-GR3, the frozen seat universe and the two-line `ROW GR<n> VERDICT:` plus `SECTION SHA256:` report shape in code; base `2042117c` | committed reads; `--section-hash` prints hashes only; no host write | tsukuroi |
| scrub-admission-r50 | gate | `python3 tools/check-scrub-admission-r50.py --revision <REV> [--lane <repo>] [--section-hash] [--wave-dir <DIR>] [--results-file <PATH>] [--dispatch-file <PATH>]` | 0 predicate `structural_ok == 1 and corr_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3`;1 otherwise;2 usage/read error or unreadable base | none: no self-test mode; frozen GR1-GR3 row bytes, cited source snapshots, 18 report-bound cohort results and three admission marks are the measurement; controls `.ufo/waves/round-50/controls/battery.py` | Round-50 C1; correction set and report-binding legs are in the frozen counter; does not prove verdict substance or prevent a fabricated result bundle | committed reads; fixture-only overrides; no host writes | tsukuroi |
| selftest-matcher-r50 | gate | `python3 tools/check-selftest-matcher-r50.py --revision <REV> --scratch <DIR> [--runs N]` | 0 frozen predicate passes;1 any predicate leg fails;2 usage/read error | invokes the existing census selftest twice by default; no separate self-test mode | Round-50 C2; base matcher probe and census selftest summary; counter can be satisfied by a shape-valid liar census, so its output is not standalone behavior proof | private scratch under `--scratch`; census fixture tree under TMPDIR | tsukuroi |
| adjacency-table-r50 | gate | `python3 tools/check-adjacency-table-r50.py --revision <REV> [--lane <repo>] [--siblings-root <DIR>]` | 0 frozen shape/content/stub predicate passes;1 any leg fails;2 usage/read error | none: no self-test mode; frozen ADJ table, sibling pin bytes, live tip quotes and synthesized stub are the measurement | Round-50 C3; verifies the default lane table and nine referenced OUT anchors; content legs are overrideable and do not prove quote semantics | read-only lane/sibling Git reads; override fixtures only | tsukuroi |

## Scrub grounding — round 49 (the cohort read; GR2 stays partly)

Round 49 applied the seven corrections the round-48 counted cohort named and re-read GR1-GR3 with a fresh
18-seat cohort (`.ufo/waves/round-49/w1/`): GR1 `holds` 6/6, GR3 `holds` 6/6, GR2 `holds` 5/6 with one bound
`partly` (`R49CritGR2b`). The frozen predicate needs all three rows, so **no row is admitted this round** and no
admission mark is written. GR2's remaining defect is named: the bracketed mark still reads "for the ioctl and
btrfs-progs side … not pinned here" although `ioctl.c` *is* pinned (S240) and the row cites it at `ioctl.c:3132`
and `ioctl.c:3190`; the mark must shrink to the btrfs-progs printing it actually leaves open, and the entry's
`source:` line must name S240. Row hashes at the round-49 freeze: GR1 `3a2ba180…`, GR2 `d4296085…`, GR3
`43430a14…`. Counter: `python3 tools/check-scrub-admission-r49.py --revision <REV>`
(legs `structural_ok`, `corr_ok`, `quotes_ok`, `verdicts_ok`, `seats_ok`, `marks_ok`). The counter is a shape
gate, not a forgery gate: a fabricated cohort that satisfies the file shapes passes it (receipt
`.ufo/waves/round-49/w1/R49CritCounter/`), so admission credit still rests on the orchestrator's real dispatch and
results file, never on a hand-written report set.

## Census selftest — descriptor-band diagnostic (round 49)

The `--selftest` alias resolver now records a failure class and the harness prints it: an exhausted alias band
prints `fd band <band> exhausted (every descriptor already open), cannot alias TMPDIR <t>; no /tmp fallback`
and a malformed band prints `… cannot host the fixture tree (fd-band-invalid; no /tmp fallback, R48-C2)`. The
band is the fixed 240-249 list, overridable only for the selftest case through `SELFTEST_FD_BAND` (a caller who
exports it changes selftest behaviour — named limit). The `(R49-C3)` case chooses two probe descriptors that are
free and not the run's own alias descriptor, so it never breaks a dirty-TMPDIR run (the round-49 regression
`R49RevFdA` D1, fixed in the same round). Counted by `python3 tools/check-fd-band-r49.py --revision <REV>`
(`tools/check-fd-band-r49.py` was rounded forward in round 50 to require at least 167 cases, preserving the
R49-C3 witness while tolerating later selftest additions); the round-49 capture had 167 cases. Round 50 adds
one full-read matcher case: current `--selftest` is 168/168 PASS at `.ufo/waves/round-50/after/c2-final.json`.
The C2 counter's name-match leg is lexical and can be fooled by an equivalent spelling or a printed stub; its
counter receipt is not standalone proof of behavior.

## Census selftest — full-read matcher (round 50)

The must-match assertions that inspect a probe's captured output use `buf_has`/`out_has`, an `awk` matcher that
consumes the complete buffer. This preserves the no-write contract: no here-string is used on a buffer larger
than 64 KiB, because bash may materialize one as a temporary file. The old `printf | grep -q` form could exit
early, SIGPIPE its writer, and make `pipefail` report a false miss on a large plane output (round-49
`R49ExecSelfAssess.md` §4; grep semantics opened this round at S256). The `(R50-C2)` case checks 20 full-read
matches and one absent match in a 200 KB buffer. Measured by
`bash tools/tsukuroi-census.sh --selftest`: `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)`
at the round-50 measured revision. This is still a selftest of the matcher, not proof against a modified census
that merely prints the expected lines; the round-50 counter-cheat report names that limit.

The round-49 `check-fd-band-r49.py` still measures the R49-C3 witness, but its total-case leg is a minimum
(167), not an exact count, so a later independently labelled selftest case does not invalidate that witness.
