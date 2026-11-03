source: own-work probes — the 26 receipted read-only probes under `.ufo/waves/round-64/probes/` (p1–p21 plus the p4b/p6b/p7b/p8b/p10b re-derivations), the live six-plane census run `probes/p20-census.txt`, and the stored side quoted verbatim from `SKILL.md` (decision-table snapshot column, `SKILL.md:44-50`, the census live-contract block `SKILL.md:1210-1216`, the headroom item `SKILL.md:125-127`)
verified-at: 2026-11-03 (round-64 work commit; host plazir27, canonical Linux/omp host, kernel 7.2.11-arch1-1)
recheck: 30d — next pass due 2026-12-03; procedure: re-run the p1–p21 battery (each receipt carries its exact command) and re-diff against this note's live column; any new drift row supersedes in place per the contract (append a dated correction row, never rewrite)

# Host drift recheck r64 — the SKILL decision-table snapshot re-measured after the upgrade arc

The SKILL plane table's snapshot column still reads "Measured 2026-10-14 (notes:
`corpus/knowledge/`)" (`SKILL.md:44`) and says of itself "re-measure; never quote it as current
state". Between 2026-10-14 and this re-measure the host ran the pacman-pause-lifted upgrade arc:
kernel 7.2.3 → **7.2.11-arch1-1** (running), mkinitcpio 41.1-1 → **42.2-1**, systemd → **262.1-1**,
pacman → **7.1.0.r9.g54d9411-3**, nvidia-open-dkms 610.57.04-1 → **615.78.08-1**, sync dbs
re-fetched (births 2026-10-29 / 2026-11-02). This note re-measures every plane value the snapshot
column states, against the table's own HEALTHY/DEGRADED/BLOCKED definitions, with one receipt per
probe. Verdict vocabulary for rows: `match` (stored and live agree on the compared quantity),
`drift` (both sides exist and disagree). A `drift` row is the expected consequence of a host that
moved — it is a refresh of the record, not a defect allegation against the snapshot; the snapshot
column itself instructs re-measurement.

| id | plane | stored (verbatim SKILL.md text + path:line) | live (value + receipt) | verdict |
|---|---|---|---|---|
| DR1 | packages | `census **1188** installed (`pacman -Q \| wc -l`)` — `SKILL.md:46` | `1519` — `probes/p1-installed-count.txt` (`$ pacman -Q \| wc -l`, rc=0) | `drift` |
| DR2 | packages | `207 explicit` — `SKILL.md:46` (also `SKILL.md:729` "1188 installed, 207 explicit") | `334` — `probes/p2-explicit-count.txt` (`$ pacman -Qe \| wc -l`, rc=0) | `drift` |
| DR3 | packages | `**16 foreign**` — `SKILL.md:46`; `pacman -Qm` = 16 foreign (3 explicit: `android-apktool-bin`, `obsidian-cli-inspector`, `omarchy-walker`; the 13 `elephant-*` are its deps) — `SKILL.md:100` | `23` — `probes/p3-foreign.txt` (`$ pacman -Qm \| wc -l`, rc=0). Cross-check: census `foreign=23(known=3 new=7 drift=13 gone=0) base=r6(16)` — `probes/p20-census.txt` | `drift` |
| DR4 | packages | the 3 named explicit foreign `android-apktool-bin`, `obsidian-cli-inspector`, `omarchy-walker` + 13 `elephant-*` — `SKILL.md:100` | same 3 known names survive, the 13 `elephant-*` moved `2.21.0-1 → 2.22.1-1`, and 7 names are new to the baseline: `detect-it-easy`, `imhex-bin`, `opencode-beta`, `openssl-1.0`, `postgres-language-server-bin`, `tizen-sdb`, `zcode` — `probes/p3-foreign.txt` (full 23-name list) + `probes/p20-census.txt` (`new=[…]`, `drift=[elephant(2.21.0-1->2.22.1-1) …]`) | `drift` |
| DR5 | packages | `3 orphans (`electron39`, `mbedtls`, `webp-pixbuf-loader`)` — `SKILL.md:46` | `0` orphans — `probes/p4b-orphans-clean.txt` (`$ pacman -Qdt` empty, rc=1; `$ pacman -Qdt \| wc -l` = `0`). None of the three stored names is an orphan today: `electron39` and `webp-pixbuf-loader` are **not installed** (`error: package … was not found`), `mbedtls 4.2.0-1` **is** installed but is now `Required By: imhex-bin` (new foreign package, DR4), so `-Qdt` no longer lists it. First pass kept at `probes/p4-orphans.txt` | `drift` |
| DR6 | packages | `-Dk` clean — `SKILL.md:46` ("No database errors have been found!") | `No database errors have been found!`, rc=0 — `probes/p5-dk.txt` | `match` |
| DR7 | packages | `du -sh /var/cache/pacman/pkg` (8.6 G; 1568 archives + 1568 sigs 1:1, never pruned … — `SKILL.md:125-127` | `6.9G /var/cache/pacman/pkg`, with `du: cannot read directory '/var/cache/pacman/pkg/download-KH5iIO': Permission denied`, rc=1 — `probes/p19-pkg-cache.txt` (a lower bound; same privilege class as the stored `700 alpm unreadable → cache size ≥ 8.6 G` caveat, so size alone is a weak comparator — the archive/sig counts the stored text also gives were not re-probed this wave) | `drift` |
| DR8 | systemd (system scope) | `both scopes `running`` — `SKILL.md:47` | system scope `running`, rc=0 — `probes/p6b-system-scope.txt` (`$ systemctl is-system-running`; named as a probe at `SKILL.md:152`) | `match` |
| DR9 | systemd (user scope) | `both scopes `running`` — `SKILL.md:47`; census snapshot `PLANE systemd: HEALTHY (scope=user state=running …)` — `SKILL.md:1212` | user scope `degraded`, rc=1 — `probes/p6-user-manager-state.txt` (`$ systemctl --user is-system-running`) | `drift` |
| DR10 | systemd (failed units) | `0 failed units (`--failed` and `--all`)` — `SKILL.md:47`; census `failed=0` — `SKILL.md:1212` | system scope: `0 loaded units listed` — `probes/p6b-system-scope.txt`. user scope: `2 loaded units listed` — `probes/p7-failed-units.txt`: `run-p1157862-i1164315.scope`, `run-p1159104-i1145275.scope`, both `Result=oom-kill` (`systemctl --user show <u> -p Result -p ExecMainStatus`; `ExecMainStatus` is empty for a `.scope`, rc=0). Census `failed=2` — `probes/p20-census.txt`. The compound claim is false on the user half | `drift` |
| DR11 | systemd (timers) | `only `ai-usage.timer` active (≈5-min cadence; last run 09:52:56, `Result=success`)` — `SKILL.md:47` | `2 timers listed` — `probes/p7b-user-timers.txt`: `ai-usage.timer` (last `Tue 2026-11-03 15:38:40 -03`, 20s ago) **and** `cursor-shim-healthcheck.timer` (last `Mon 2026-10-19 00:33:15 -03`, `NEXT`/`LEFT` both `-`, i.e. disarmed); both read `enabled enabled` in `list-unit-files --type=timer`. Census `timers_enabled=2 timers_scanned=2 timer_fail=0 timer_unknown=0` — `probes/p20-census.txt` | `drift` |
| DR12 | journal | `**60 941 err lines but only 238 entries** (`-o json \| wc -l`)` — `SKILL.md:48` | `5275` entries — `probes/p8-journal-err-entries.txt` (`$ journalctl -b -p err -o json --no-pager \| wc -l`); `6212` err **lines** and `44597` total boot-0 lines — `probes/p8b-journal-line-count.txt`. Cross-check census `err=5275 (coredump=4 kernel=39 other=5232)` — `probes/p20-census.txt`. Both halves of the stored claim moved; the line/entry ratio trap itself still holds (6212 lines vs 5275 entries this boot) | `drift` |
| DR13 | journal (retained boots) | `boots=13` — `SKILL.md:1214` (2026-10-14 snapshot; an older capture at `SKILL.md:2366` says "6 retained boots") | `3` retained boots (`-2` 2026-10-26, `-1` 2026-10-31, `0` 2026-11-02) — `probes/p9-retained-boots.txt` (`$ journalctl --list-boots --no-pager \| tail -n +2 \| wc -l`) | `drift` |
| DR14 | journal (coredumps this boot) | `Coredumps this boot 198: godot 142 SIGABRT, node 47 …, typora 2, `chrome_crashpad` 2, electron 1, bash 1 SIGSEGV` — `SKILL.md:48` | `4` rows in the boot-0 window (`$ coredumpctl list --no-pager --since "2026-11-02 12:07:17" \| tail -n +2 \| wc -l`) — `probes/p10b-coredump-derivation.txt`; cross-check census `HANDOFF ADJ-04 mori class=coredumps value=4 kind=dated-event` — `probes/p20-census.txt`. Whole journal history `253` lines incl. header (252 rows) — `probes/p10-coredumps.txt`; `/var/lib/systemd/coredump` holds `10` files (most entries are `COREFILE missing`) | `drift` |
| DR15 | drivers | `open DKMS 610.57.04 loaded and active` — `SKILL.md:49`; census `smi=610.57.04` — `SKILL.md:1213` | `NVIDIA GeForce RTX 5070, 615.78.08` — `probes/p11-nvidia-smi.txt` (`$ nvidia-smi --query-gpu=name,driver_version --format=csv,noheader`, rc=0); census `smi=615.78.08` — `probes/p20-census.txt` | `drift` |
| DR16 | drivers | `dkms status` stale `7.1.4-arch1-1` registration (tree gone; `ls /lib/modules` = 7.2.3 only) — `SKILL.md:49` | three registrations, **none** for `7.1.4`: `nvidia/615.78.08, 6.18.57-2-lts: installed` / `…, 7.2.11-arch1-1: installed` / `…, 7.2.3-arch1-3: installed (Original modules exist) (Built modules are missing in the kernel modules folder)` — `probes/p12-dkms.txt` (rc=0). The stale-registration class survives but moved to `7.2.3-arch1-3` | `drift` |
| DR17 | drivers | `pacman -Qo` = `error: No package owns …/updates/dkms/nvidia.ko.zst` … packages `nvidia-open-dkms`/`nvidia-utils`/`lib32-nvidia-utils`/`libva-nvidia-driver`/`linux-firmware-nvidia` installed 2026-10-11 16:14 (upgrade 610.43.03-3 → 610.57.04-1) — `SKILL.md:49` | `nvidia-open-dkms 615.78.08-1` — `probes/p21-versions.txt` (`$ pacman -Q linux systemd mkinitcpio pacman nvidia-open-dkms`, rc=0) | `drift` |
| DR18 | drivers | stale `7.1.4-arch1-1` registration (tree gone; `ls /lib/modules` = 7.2.3 only) — `SKILL.md:49` | running kernel `7.2.11-arch1-1` with `linux 7.2.11.arch1-1` — `probes/p21-versions.txt`; dkms has a built `7.2.11-arch1-1` entry — `probes/p12-dkms.txt` | `drift` |
| DR19 | update-safety | sync dbs born **2026-10-11 12:54:13.542** (`%w`; core/extra/multilib/omarchy; TSUKUROI-4 re-derived) — `SKILL.md:50` | `core.db`/`extra.db`/`multilib.db` = `2026-10-29 03:44:19.803659836 -0300`; `omarchy.db`/`openai-chatgpt.db` = `2026-11-02 09:42:35.879600953 -0300` — `probes/p13-syncdb-birth.txt` (`$ stat -c '%w %n' /var/lib/pacman/sync/*.db`, rc=0). Two drifts in one row: the birth dates, and the db set (5 dbs now, `openai-chatgpt` is a repo the snapshot did not have). Census agrees on freshness only: `chan=dbs=5 fetch=1d stamp=12d` — `probes/p20-census.txt` | `drift` |
| DR20 | update-safety | `-Qu` empty **rc=1** — `SKILL.md:50` | empty output, `rc=1` — `probes/p14-qu.txt` (`$ pacman -Qu; echo rc=$?`) | `match` |
| DR21 | update-safety | no `IgnorePkg`/`IgnoreGroup`, `HoldPkg = pacman glibc` (`/etc/pacman.conf:7`) — `SKILL.md:50` | `pacman-conf IgnorePkg IgnoreGroup` prints nothing, rc=0; `7:HoldPkg = pacman glibc` — `probes/p15-holds.txt`; census `holds=pacman glibc; pins=none` — `probes/p20-census.txt` | `match` |
| DR22 | update-safety | no `db.lck` — `SKILL.md:50` | `ls: cannot access '/var/lib/pacman/db.lck': No such file or directory`, rc=2 — `probes/p16-db-lck.txt`; census `db.lck=absent` — `probes/p20-census.txt` | `match` |
| DR23 | update-safety (rollback net) | `snapper list-configs` → empty / `= 0 configs` — `SKILL.md:50`, `SKILL.md:403`, `SKILL.md:957` | two configs present: `home │ /home` and `root │ /` — `probes/p17-snapper.txt` (rc=0) | `drift` |
| DR24 | update-safety (headroom) | `df -h / /boot` (`851G` free on `/`, `1.8G` on `/boot`) — `SKILL.md:125` | `/dev/mapper/root 930G 213G 717G 23% /`; `/dev/nvme0n1p1 2.0G 1.4G 687M 67% /boot` — `probes/p18-df.txt` (rc=0) → `717G` free on `/`, `687M` free on `/boot` | `drift` |
| DR25 | census rollup | `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED)` — `SKILL.md:1216` | `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)` with `rc=1` — `probes/p20-census.txt` (six planes; `systemd` degraded; `oom` plane added since the snapshot) | `drift` |

## Per-plane tally

| plane | rows | match | drift |
|---|---|---|---|
| packages | DR1–DR7 (7) | DR6 | DR1, DR2, DR3, DR4, DR5, DR7 |
| systemd | DR8–DR11 (4) | DR8 | DR9, DR10, DR11 |
| journal / boot | DR12–DR14 (3) | — | DR12, DR13, DR14 |
| drivers | DR15–DR18 (4) | — | DR15, DR16, DR17, DR18 |
| update-safety | DR19–DR24 (6) | DR20, DR21, DR22 | DR19, DR23, DR24 |
| census rollup | DR25 (1) | — | DR25 |

**25 rows: 5 `match`, 20 `drift`, 0 unknown.** No probe left a compared value unknown. The
nonzero-exit receipts are all value-bearing: `-Qdt` rc=1 and `-Qu` rc=1 (empty-result semantics),
`db.lck` rc=2 (absent, which is the passing state), `du` rc=1 (one unreadable `download-*`
subtree).

Per-plane drift summary: **packages 6/7** · **systemd 3/4** · **journal 3/3** · **drivers 4/4** ·
**update-safety 3/6** · **census rollup 1/1** drifted.

## Findings an operator should see (detection only)

1. **The user manager is `degraded` (DR9/DR10):** two failed transient `systemd-run` scopes
   (`run-p1157862-i1164315.scope`, `run-p1159104-i1145275.scope`), both `Result=oom-kill` —
   `rembg birefnet-general` runs killed by cgroup OOM at `memory_max` 3 GiB (identity and window in
   `probes/p7-failed-units.txt` and `.ufo/waves/round-64/after/scout-host-recon.md`). App-level
   failures, not unit-definition defects; they are what flipped `is-system-running` to `degraded`.
   Fleet/wave attribution of the pressure stays with mori (ADJ-04).
2. **A rollback net now exists (DR23):** snapper configs `root` and `home` are configured — the
   stored "no snapshot net is configured" residue is closed. The upgrade-safety picture improves:
   pending empty (DR20), dbs fresh (DR19), no holds (DR21), no lock (DR22).
3. **/boot headroom tightened (DR24):** 687M free of 2.0G (67% used) — the UKI set grew with the
   kernel series; still workable, watch it before the next kernel upgrade.
4. **The stale dkms registration class survives (DR16):** now `7.2.3-arch1-3` (built modules
   missing) next to the installed `7.2.11` — same class the r1 snapshot flagged for `7.1.4`.

## Notes

- The stored column is the **2026-10-14** snapshot (`SKILL.md:44`); every `drift` row here is the
  expected consequence of a host that moved between 10-14 and 11-03 — **not** a defect allegation
  against the snapshot.
- Invariant-by-design checks survive untouched: DR20 (`-Qu` empty rc=1), DR21 (holds), DR22 (no
  lock). These are the rows that would matter if they ever drifted.
- `p21` fixes the version set: `linux 7.2.11.arch1-1`, `systemd 262.1-1`, `mkinitcpio 42.2-1`,
  `pacman 7.1.0.r9.g54d9411-3`, `nvidia-open-dkms 615.78.08-1` — the same receipt C3's
  "mkinitcpio 42.2-1 is installed" premise rests on (`corpus/knowledge/mkinitcpio42-onrelease-r64.md`).
- Boot-0 window start `2026-11-02 12:07:17` is `uptime -s` (`p10b-coredump-derivation.txt`), used
  to scope DR14.
- Not compared, deliberately: the census `packages` line now carries `root_status …
  root_owner_write` fields that the stored line (`SKILL.md:1211`) lacks — a tool-shape change, not
  a plane value.
- The extra receipts beyond the p1–p21 naming (`p4b`, `p6b`, `p7b`, `p8b`, `p10b`) are read-only
  re-derivations of named probes, added because the first pass of the naive pipeline could not
  distinguish "0" from "1 blank line".
