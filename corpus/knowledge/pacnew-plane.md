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
