source: S010 (A) https://wiki.archlinux.org/title/System_maintenance?oldid=885170 § Deal promptly with new configuration files; S011 (A) https://wiki.archlinux.org/title/Pacman/Pacnew_and_Pacsave?oldid=869214 § Locating .pac* files / Managing .pac* files; S032 (A, own-work) /var/log/pacman.log § 2026-10-11 entries 1427, 1645–1646
verified-at: 2026-10-19 (reopened S010 and S011; reran pacman.log and /etc filesystem censuses read-only)
recheck: on-release; procedure: after every -Syu, enumerate /etc .pacnew/.pacsave names and inspect pacman notices/log; compare and merge, never blindly overwrite

# Pacnew/pacsave plane — current config-drift census

## Claim

[obs] The current `/etc` sweep returned the same three `.pacnew` paths as the matching `pacman.log` install notices. The log count is **3 — `grep -cE 'installed as .*\.pacnew' /var/log/pacman.log` 2026-10-19** and **0 — `grep -cE 'saved as .*\.pacsave' /var/log/pacman.log` 2026-10-19**. The paths recorded in the log are at `pacman.log:1427,1645,1646` and dated 2026-10-11.

| Census method | Current result | Interpretation / limit |
|---|---|---|
| Current filesystem | **3 — `find /etc \( -name '*.pacnew' -o -name '*.pacsave' \) 2>/dev/null` 2026-10-19**; output: `/etc/locale.gen.pacnew`, `/etc/tpm2-tss/fapi-profiles/P_ECCP384SHA384.json.pacnew`, `/etc/tpm2-tss/fapi-profiles/P_RSA3072SHA384.json.pacnew` | [obs] These names are currently visible in the readable part of `/etc`; the command prints paths only, not file contents. No `.pacsave` name appeared. |
| Filesystem sweep access | **12 — `find /etc \( -name '*.pacnew' -o -name '*.pacsave' \) 2>&1 >/dev/null | grep -ci 'Permission denied'` 2026-10-19** | [obs] Permission-denied paths were skipped. The filesystem result is therefore not proof that no matching files exist below unreadable locations. |
| Pacman log history | **3 — `grep -cE 'installed as .*\.pacnew' /var/log/pacman.log` 2026-10-19**; **0 — `grep -cE 'saved as .*\.pacsave' /var/log/pacman.log` 2026-10-19** | [obs] The matching log lines name exactly the visible `.pacnew` files. A log is historical: absence from it does not establish current filesystem state, and its range is the available `/var/log/pacman.log`. |

[inf] The two independent methods agree on the visible `.pacnew` pathname set for this capture. Their coverage is not symmetric: `find` is current state but skipped inaccessible paths, while the log is an event history. Therefore the bounded negative is “no `.pacsave` appeared in the accessible `/etc` output or in the current pacman log,” not “no `.pacsave` exists anywhere.”

[obs] The `pacman-contrib` package query returned “not found” on this host (`pacman -Q pacman-contrib` 2026-10-19). Do not assume the `pacdiff` command is locally available; if available on an operator system, it is the ArchWiki-recommended interface for reviewing these files. No package installation or file merge was performed.

## Operator action (reported, never performed)

- After every full upgrade, read pacman’s notices and promptly compare each `.pacnew` with its live counterpart; merge deliberately rather than overwriting a live file blindly (S010, § Deal promptly with new configuration files; S011, § Managing `.pac*` files).
- Use `pacdiff` interactively when available (provided by `pacman-contrib`); otherwise use an appropriate comparison/merge tool. Decide file-by-file whether to merge, preserve, or retire a saved file. Do not run these actions as part of this read-only capture.
- To discover current paths, use the `/etc` `find` sweep below. Treat `/var/log/pacman.log` as corroborating history, not as a substitute for a filesystem search (S011, § Locating `.pac*` files).

## Falsifier

The agreement claim is falsified if a fresh readable `/etc` sweep produces a different visible `.pacnew` pathname set from the corresponding logged install events, or if any `.pacsave` is found in the accessible sweep. Changes after an operator merges/removes a file are expected state changes, so record the new census rather than rewriting this dated observation. A later scan with fewer permission errors can also change the bounded negative without contradicting this capture.

## Recheck procedure

Run these read-only commands after each `-Syu` and retain only paths/counts, never configuration contents:

```sh
find /etc \( -name '*.pacnew' -o -name '*.pacsave' \) 2>/dev/null
grep -nE 'installed as .*\.pacnew|saved as .*\.pacsave' /var/log/pacman.log
find /etc \( -name '*.pacnew' -o -name '*.pacsave' \) 2>&1 >/dev/null | grep -ci 'Permission denied'
```

Compare names and line numbers; record every count as `<number> — <command> 2026-10-19` (or the new run date). The log query is historical; the filesystem query is the current-state census.

## QUALITY check

1. Falsifiable: both census outputs, their agreement condition, and the permission-denied limit are explicit.
2. External guidance cites tier-A S010/S011 with canonical URLs and section anchors; local observations cite S032 and exact commands/log lines.
3. [obs], [inf], and [unk] remain separated; no inference about unreadable paths or file contents is made.
4. This entry is a new append-only note; any correction must be a dated `## Erratum` block, not a rewrite.
5. No source was rejected; retain a reason and flip condition if a future source fails to open or fails its claim.
6. The operator action is compare/merge after a full upgrade, not a partial package operation; no pacman mutation was run.
7. External support is tier A; no tier-C source is sole support.
8. Source/verified-at/recheck keys, an explicit cadence, and a falsifier are present.
9. The negative claim names both sweeps and the inaccessible-path count; it is not generalized beyond their observed coverage.

## Sources

- S010 (tier A) — ArchWiki System maintenance, https://wiki.archlinux.org/title/System_maintenance?oldid=885170 § Deal promptly with new configuration files; quote: “users must deal with these files promptly.”
- S011 (tier A) — ArchWiki pacman/Pacnew and Pacsave, https://wiki.archlinux.org/title/Pacman/Pacnew_and_Pacsave?oldid=869214 § Locating `.pac*` files; quote: “the log does not keep track of the files currently in the filesystem nor the ones that have already been removed.”
- S011 (tier A) — same URL § Managing `.pac*` files; quote: “Always compare and merge the changes manually.”
- S032 (tier A, own-work) — `/var/log/pacman.log` lines 1427, 1645, 1646, read-only; `find /etc` output includes filenames only. This entry intentionally records no configuration-file contents.


## R18-FRESHNESS — sibling current-use restatements (2026-10-20)

Sources S060, S051 and S052. This appended correction supersedes the current-use readings listed below and every repeated current-use restatement of the same premise in this file. Historical measurements remain intact. No package, service, rebuild, boot or rollback action is authorized.

- R18-FRESH-SUPPLEMENT-32: prior locus `[obs] The `pacman-contrib` package query returned “not found” on this host (`pacman -Q pacman-contrib` 2026-10-19). Do not assume the `pacdiff` command is locally available; if available on an operator system, it is the ArchWiki-recommended interface for reviewing these files. No package installation or file merge was performed.`. Now: pacman-contrib-1.13.1-1 is now present in local metadata. The old package-absent rationale cannot establish current pacdiff availability; no pacdiff execution or executable-presence observation is credited from this R18 capture [Supporting capture context: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:27-39, .ufo/waves/round-18/l1-capture/host-capture-r18.txt:82-86]. Capture: .ufo/waves/round-18/l1-capture/host-capture-r18.txt:36.


## R35-FRESHNESS — host re-measurement (2026-10-23; drafted by round-35 wave-2 W2RevHostCapture from wave-1 ExecHostPacnew)

Sources S032 (own-work) plus the dated captures cited per supplement. This appended correction
supersedes the current-use readings listed below and every repeated current-use restatement of the
same premise in this file. Historical measurements remain intact. No package, service, rebuild,
boot or rollback action is authorized. Re-measured 2026-10-23 11:47 UTC, twice in one day
(11:31 w1 capture, 11:47 this capture, identical outputs).

- R35W2-FRESH-SUPPLEMENT-A: prior locus `| Filesystem sweep access | **12 — `find /etc \( -name '*.pacnew' -o -name '*.pacsave' \) 2>&1 >/dev/null | grep -ci 'Permission denied'` 2026-10-19** |`. Now: **11 — same command 2026-10-23**. The twelfth path was `/etc/cryptsetup-keys.d` (mode 700 root:root), still present in btrfs snapshots `/.snapshots/1` and `/.snapshots/2` (snapshot set is exactly {1,2}, mtimes 2026-10-20 09:03:02 and 09:29:19) and removed by the operator (`/usr/bin/rmdir /etc/cryptsetup-keys.d`) on 2026-10-20 09:33:19 per the systemd journal; it is absent from live `/etc` today. The remaining 11 denied directories (`/etc/audit/plugins.d`, `/etc/cni/net.d`, `/etc/credstore`, `/etc/credstore.encrypted`, `/etc/cups/ssl`, `/etc/pacman.d/gnupg/crls.d`, `/etc/pacman.d/gnupg/openpgp-revocs.d`, `/etc/pacman.d/gnupg/private-keys-v1.d`, `/etc/polkit-1/rules.d`, `/etc/ssl/private`, `/etc/sudoers.d`) were name-scanned read-only via `sudo -n ls -1A`: 30 entries total, none matching `*.pacnew`, `*.pacsave`, `*.pacsave.N` or `*.pacorig`. [Supporting capture context: fresh-capture-20261023T1211Z.txt:22-40, :144-156, :179-197.]
- R35W2-FRESH-SUPPLEMENT-B: prior locus `[obs] The `pacman-contrib` package query returned “not found” on this host (`pacman -Q pacman-contrib` 2026-10-19). Do not assume the `pacdiff` command is locally available; …` (and the residual caveat of R18-FRESH-SUPPLEMENT-32 that no executable-presence observation is credited). Now: `pacman-contrib 1.13.1-1` is installed (installed 2026-10-20 07:45:37, `/var/log/pacman.log:2444`) and `/usr/bin/pacdiff` is present, `pacman -Qo /usr/bin/pacdiff` → exit 0, owned by `pacman-contrib 1.13.1-1`. The “otherwise use an appropriate comparison/merge tool” branch is currently inapplicable on this host; the compare-and-merge operator action is unchanged. [Supporting capture context: fresh-capture-20261023T1211Z.txt:68-74.]
- R35W2-FRESH-SUPPLEMENT-C: prior locus `## Recheck procedure` (the three-command block and the sentence “Compare names and line numbers; record every count as `<number> — <command> <date>`”). Now: command 1 (`find /etc …`) **exits 1** on this host because find cannot read 11 `/etc` subdirectories, while still printing every reachable match; commands 2 and 3 exit 0. Record command 1 as `<number> — <command> (exit 1: N permission-denied directories, see command 3) <date>`; an exit 1 from command 1 means “sweep incomplete by permission”, not “sweep failed”. Also widen command 1's globs to `*.pacnew`, `*.pacsave`, `*.pacsave.[0-9]*`, `*.pacorig` so the sweep matches the counter plane (tools/score-pacnew-arm-r35*.py); on 2026-10-23 the two extra kinds are 0, so the narrow and wide sweeps agree today. [Supporting capture context: fresh-capture-20261023T1211Z.txt:8-9, :22-25, :28-65.]

Unchanged on 2026-10-23 and re-affirmed: the visible `.pacnew` set is still exactly `/etc/locale.gen.pacnew`, `/etc/tpm2-tss/fapi-profiles/P_ECCP384SHA384.json.pacnew`, `/etc/tpm2-tss/fapi-profiles/P_RSA3072SHA384.json.pacnew`; log targets are still lines 1427, 1645, 1646 dated 2026-10-11; 0 `.pacsave`, 0 numbered `.pacsave`, 0 `.pacorig` on disk and in the log; `/var/log/pacman.log` is still the only unrotated log (3191 lines, 246 903 bytes, mtime 2026-10-22 04:10). Counter-plane constant re-derived twice:
`DRIFT pacnew-plane pacnew=3 pacsave=0 pacorig=0 unreadable=11 log_pacnew=3 log_pacsave=0 unlogged=0 gone=0`.
The `unreadable` value is a property of the sweeping user (`vgpnk`, uid 1000); a root run would report 0.

The round-35 census arm (`DRIFT pacnew-plane`, `tools/tsukuroi-census.sh`) now prints these counts on every live run; `corpus/knowledge/pacman-backup-files-r35.md` explains which pacman events produce them.
