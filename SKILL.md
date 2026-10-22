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

- **Rule** (S149 `mm/oom_kill.c:228-236`): one scalar per task, `points = rss + swapents + pgtables` in pages `+ oom_score_adj × totalpages/1000`; `select_bad_process` keeps the strict maximum in task-list order and an equal score replaces the earlier pick (`:339-341`, `:362-375`). One adj unit is 0.1 % of allowed memory, i.e. exactly one point on the 0-1000 badness scale (S148 `proc.rst:1761-1766`, `:1777-1783`).
- **totalpages** (S149 `:258`, `:263`): `totalram_pages() + total_swap_pages` for a global OOM, `mem_cgroup_get_max()` for a memcg OOM. Capture-epoch host sum is 16,909,739 pages, so one adj unit is 16,909 pages (66.05 MiB); `-1000` is not a low score but removal from candidacy (`:216-222`, S148 `proc.rst:1781-1783`).
- **Decision table**:

| trigger | totalpages used | effect of the control |
|---|---|---|
| global OOM | 16,909,739 pages at event A/B (15,861,169 today) | −1000 excluded; 0 no offset; +200 adds 3,381,800 pages (12.90 GiB) |
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
