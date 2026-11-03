# E2Probes — C2-BATTERY (round 64 / w1, claim C2)

Timestamp of this report: 2026-11-03T18:40Z. Host: canonical Linux/omp host,
`uname -r` `7.2.11-arch1-1`. Lane repo: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

Every command below was **read-only**. Zero mutating operations: no pacman transaction
(`-S`/`-Sy`/`-Syu`/`-U`/`-R`), no `systemctl` start/stop/enable/disable, no journal or core-dump
write, no git/jj command at all, no writes outside `.ufo/waves/round-64/probes/` and the one
draft file named below. No privilege gate was hit — no probe needed root and none was attempted.

## Stored side (grepped myself, not transcribed)

Read directly out of `SKILL.md` (`grep -n`, then per-line raw reads). The snapshot is the
decision table's right column, header `SKILL.md:44` — "Measured 2026-10-14 (host `plazir27`)" —
rows `SKILL.md:46` (packages), `:47` (systemd), `:48` (journal), `:49` (drivers), `:50`
(update-safety), plus the census live-contract block `SKILL.md:1210-1216` and the deep-checklist
headroom item `SKILL.md:125-127`.

| stored value | SKILL.md line |
|---|---|
| census **1188** installed (`pacman -Q \| wc -l`) | 46 (also 202, 729) |
| 207 explicit | 46 (also 729) |
| **16 foreign** | 46 (also 100, 729) |
| 3 orphans (`electron39`, `mbedtls`, `webp-pixbuf-loader`) | 46 |
| `-Dk` clean | 46 |
| both scopes `running`; 0 failed units (`--failed` and `--all`) | 47 |
| only `ai-usage.timer` active (last run 09:52:56, `Result=success`) | 47 |
| 60 941 err lines but only **238 entries** (`-o json \| wc -l`) | 48 |
| coredumps this boot 198 (godot 142, node 47, typora 2, chrome_crashpad 2, electron 1, bash 1) | 48 |
| open DKMS **610.57.04** loaded and active | 49 (census mirror: 1213) |
| `dkms status` stale `7.1.4-arch1-1` (tree gone; `ls /lib/modules` = 7.2.3 only) | 49 |
| sync dbs born **2026-10-11 12:54:13.542** (core/extra/multilib/omarchy) | 50 (also 96, 202) |
| `-Qu` empty **rc=1** | 50 |
| no `IgnorePkg`/`IgnoreGroup`; `HoldPkg = pacman glibc` (`/etc/pacman.conf:7`) | 50 |
| no `db.lck` | 50 |
| `snapper list-configs` → empty / 0 configs | 50, 403, 957 |
| `851G` free on `/`, `1.8G` on `/boot` | 125 |
| cache 8.6 G (1568 archives + 1568 sigs) | 125-127 |
| `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED)` | 1216 |

## Live battery — receipt list (26 files, all under `.ufo/waves/round-64/probes/`)

Each receipt opens with `date -u +%Y-%m-%dT%H:%M:%SZ`, then `$ <command>`, full output, `rc`.

| probe | path | value |
|---|---|---|
| p1 | `probes/p1-installed-count.txt` | `1519` (rc=0) |
| p2 | `probes/p2-explicit-count.txt` | `334` (rc=0) |
| p3 | `probes/p3-foreign.txt` | 23 foreign, full list, `wc -l` = 23 (rc=0) |
| p4 | `probes/p4-orphans.txt` | raw first pass (echo-as-blank-line artifact, superseded by p4b) |
| p4b | `probes/p4b-orphans-clean.txt` | `pacman -Qdt` empty rc=1; `\| wc -l` = `0`; the 3 stored names individually re-queried |
| p5 | `probes/p5-dk.txt` | `No database errors have been found!` rc=0 |
| p6 | `probes/p6-user-manager-state.txt` | user `degraded` rc=1 |
| p6b | `probes/p6b-system-scope.txt` | system `running` rc=0; `systemctl --failed` → `0 loaded units listed` |
| p7 | `probes/p7-failed-units.txt` | `2 loaded units listed`; both `Result=oom-kill` |
| p7b | `probes/p7b-user-timers.txt` | `2 timers listed` (ai-usage, cursor-shim-healthcheck); both `enabled enabled` |
| p8 | `probes/p8-journal-err-entries.txt` | `5275` entries (rc=0) |
| p8b | `probes/p8b-journal-line-count.txt` | `6212` err lines; `44597` boot-0 lines |
| p9 | `probes/p9-retained-boots.txt` | `3` boots (−2 10-26, −1 10-31, 0 11-02) |
| p10 | `probes/p10-coredumps.txt` | `coredumpctl list \| wc -l` = 253 incl. header (252 rows); `/var/lib/systemd/coredump` = 10 files |
| p10b | `probes/p10b-coredump-derivation.txt` | boot-0 window coredumps = `4`; `uptime -s` = `2026-11-02 12:07:17` |
| p11 | `probes/p11-nvidia-smi.txt` | `NVIDIA GeForce RTX 5070, 615.78.08` rc=0 |
| p12 | `probes/p12-dkms.txt` | 3 registrations: `6.18.57-2-lts`, `7.2.11-arch1-1`, `7.2.3-arch1-3` (last flagged built-modules-missing); none for `7.1.4` |
| p13 | `probes/p13-syncdb-birth.txt` | core/extra/multilib `2026-10-29 03:44:19.803659836 -0300`; omarchy/openai-chatgpt `2026-11-02 09:42:35.879600953 -0300` (5 dbs) |
| p14 | `probes/p14-qu.txt` | empty, `rc=1` |
| p15 | `probes/p15-holds.txt` | `pacman-conf IgnorePkg IgnoreGroup` empty rc=0; `7:HoldPkg = pacman glibc` |
| p16 | `probes/p16-db-lck.txt` | `No such file or directory` rc=2 (absent = passing) |
| p17 | `probes/p17-snapper.txt` | **two configs**: `home │ /home`, `root │ /` rc=0 |
| p18 | `probes/p18-df.txt` | `/` 930G/717G free 23%; `/boot` 2.0G/687M free 67% |
| p19 | `probes/p19-pkg-cache.txt` | `6.9G`; rc=1 on one unreadable `download-KH5iIO` subtree |
| p20 | `probes/p20-census.txt` | full census, 8 PLANE lines + 3 HANDOFF/DRIFT/STORAGE/SCRUB lines + rollup; `rc=1` |
| p21 | `probes/p21-versions.txt` | `7.2.11-arch1-1`; `linux 7.2.11.arch1-1`, `systemd 262.1-1`, `mkinitcpio 42.2-1`, `pacman 7.1.0.r9.g54d9411-3`, `nvidia-open-dkms 615.78.08-1` |

Census rollup verbatim (`p20`): `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED
drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)`, rc=1. Census itself
reports `foreign=23(known=3 new=7 drift=13 gone=0) base=r6(16)`, `err=5275 (coredump=4
kernel=39 other=5232)`, `boots=3`, `timers_enabled=2`, `failed=2`, `holds=pacman glibc`, `db.lck=absent`,
`chan=dbs=5 fetch=1d stamp=12d` — i.e. the tool's own readings agree with my independent probes
on every quantity both measured.

## Drift register draft

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-64/after/drift-table-draft.md`

25 rows `DR1`–`DR25`: columns `id | plane | stored (verbatim + path:line) | live (value +
receipt) | verdict`. **5 `match`, 20 `drift`, 0 `drift?`.** A row is emitted only where both
sides exist; no probe errored in a way that left a compared quantity unknown.

Per-plane drift summary:

- **packages 6/7 drifted** — installed 1188→1519, explicit 207→334, foreign 16→23, orphans 3→0,
  cache 8.6G→6.9G; `-Dk` still clean (`match`).
- **systemd 3/4 drifted** — system scope still `running` (`match`), but user scope
  `running`→`degraded`, failed units 0→2 (both `Result=oom-kill`), timers 1→2.
- **journal 3/3 drifted** — 238→5275 err entries, boots 13→3, coredumps this boot 198→4.
- **drivers 4/4 drifted** — driver 610.57.04→615.78.08, stale dkms row `7.1.4`→`7.2.3-arch1-3`,
  package 615.78.08-1, kernel 7.2.3→7.2.11.
- **update-safety 3/6 drifted** — sync-db births 2026-10-11→10-29 / 11-02 (and 4 dbs→5),
  snapper configs 0→2, `/` free 851G→717G and `/boot` 1.8G→687M; `-Qu` rc=1 (`match`), holds
  (`match`), no `db.lck` (`match`).
- **census rollup 1/1 drifted** — stored 5-term rollup with `systemd=HEALTHY` → live 6-term
  rollup with `systemd=DEGRADED` and a new `oom` plane.

## Findings worth the integrator's attention

1. **DR23 is the only rollback-net change that is not mere staleness**: `snapper list-configs`
   now answers two configs (`home /home`, `root /`), where three separate stored lines (`:50`,
   `:403`, `:957`) assert "empty / 0 configs". Anything downstream that reasons "no rollback
   net → snapshot-less wave" is now wrong.
2. **DR10 (failed units) changes a `HEALTHY` verdict**: the snapshot's systemd row is `HEALTHY`
   on "0 failed units"; live user scope is `degraded` with two `oom-kill` scopes
   (`rembg` invocations). The census independently says `systemd: DEGRADED … failed=2`.
3. **DR5's stored orphan names are gone, not merely re-parented**: `electron39` and
   `webp-pixbuf-loader` are uninstalled; `mbedtls 4.2.0-1` is now required by `imhex-bin`, one of
   the 7 new foreign packages. Orphan count 3→0 is therefore a *consequence* of the foreign-set
   change, not a cleanup.
4. **p21 is the shared C2/C3 anchor**: `mkinitcpio 42.2-1` installed on kernel `7.2.11-arch1-1`
   is exactly C3's premise; this receipt is available for the C3 seat to cite rather than re-run.
5. **Naive-pipeline trap avoided**: `pacman -Qdt | wc -l` alone reads `1` for an empty result
   because the empty string echoes as one blank line — `p4b` uses the bare pipe (`wc -l` = `0`)
   and re-queries each stored name. Same class as the stored `-Qu` "empty but rc=1" trap.

## Artifacts / cleanliness

- Wrote only `.ufo/waves/round-64/probes/p*-*.txt` (26 files) and
  `.ufo/waves/round-64/after/drift-table-draft.md`. Nothing else touched.
- No tool install or upgrade was needed or performed this wave.
- Scratch `/fast/scratch/hyaku/tsukuroi-r64/E2Probes/` used for the battery driver and the
  `list-boots` intermediate; deleted before yield. No `/tmp` path is cited anywhere above.

## Risks / blockers

- DR7 (cache size) is a **lower bound**: `du` could not read one `download-*` subtree as an
  unprivileged user. The stored text carries the same caveat (700 `alpm` unreadable → "≥ 8.6 G"),
  so this row is a weak comparator; a root re-run resolves it, and root is not available to this
  seat (privilege gate ⇒ not attempted).
- The stored snapshot's `-Qkk` sweep figures (18/19 pkg summaries, 1332 raw lines) are not in
  this battery's authorized command list, so no row covers them; `p20` carries the census's
  bounded `sample=8` reading (`drift=2[1password-beta,1password-cli]`) instead.
- Coredump attribution by executable (the snapshot's "godot 142, node 47" breakdown) was not
  re-derived — the boot-0 window has only 4 rows, so a per-executable split would be
  uninformative at this sample size; the count is receipted, the breakdown is deliberately absent.
