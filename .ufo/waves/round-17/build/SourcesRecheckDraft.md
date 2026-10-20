# SourcesRecheckDraft — round 17 (Sources seat, 2026-10-20)

Draft rows: `.ufo/waves/round-17/build/drafts/sources-rows.md`. Nothing landed in `corpus/SOURCES.md`. No source was opened by this seat; registry and L1 captures were read as files.

## 1. Registry baseline
- [obs] `corpus/SOURCES.md` lines 7–56 hold 50 rows, S001–S050 (read this seat; no `grep -c` run).
- [obs] Registry read: `corpus/SOURCES.md` lines 7–56 (table), 58–62 (Paths), 64–114 (Search log, Leads).

## 2. Old → new field changes (in-place, contract rule 2)

| row | field | old → new |
|---|---|---|
| S014 | recheck | `90d` → `2027-01-18` (= 2026-10-20 + 90d; ISO due date so the 90d clock runs from today, not from immutable `opened` 2026-10-19) [inf] |
| S014 | used-by | `…initramfs-v42-sysroot-recovery.md, …journal-boot-plane.md` → same + `corpus/knowledge/boot-chain-r17.md` |
| S014 | status | `mined` → `mined` (unchanged) |
| S015 | used-by | `…initramfs-v42-sysroot-recovery.md` → same + `corpus/knowledge/boot-chain-r17.md` |
| S015 | recheck / status | `on-release` / `mined` → unchanged |
| S016 | used-by | `…initramfs-v42-sysroot-recovery.md` → same + `corpus/knowledge/boot-chain-r17.md` |
| S016 | recheck / status | `on-release` / `mined` → unchanged |
| S021 | used-by | `…initramfs-v42-sysroot-recovery.md` → same + `corpus/knowledge/boot-chain-r17.md` |
| S021 | recheck / status | `on-release` / `mined` → unchanged |
| S022 | used-by | `…initramfs-v42-sysroot-recovery.md` → same + `corpus/knowledge/boot-chain-r17.md` |
| S022 | recheck / status | `on-release` / `mined` → unchanged |

`teaches`, `anchor`, `opened` (2026-10-19) of S014–S022 are unchanged. Their re-open today is recorded in the round lesson `## Gate`, not in `opened` (rule 2 lists only status, recheck, used-by as mutable).

## 3. New rows (append after S050; full text in draft file)
- **S051** — own-work, tier A, scope: host boot-chain state at capture time; anchor: `boot-chain-capture.txt` captured 2026-10-20T12:35:07-03:00, line ranges 4–10, 15–30, 41–53, 68–74, 86, 126–156, 159–167, 169–258; status `mined`; opened 2026-10-20; recheck `on-release`; used-by `corpus/knowledge/boot-chain-r17.md`.
- **S052** — own-work, tier A, scope: package/settings state after the 09:15 upgrade; anchor: `fresh-capture.txt` captured 2026-10-20T12:38:12-03:00, lines 4–14, 15–38, 42–58, 58–76, 77–82, 84; status `mined`; opened 2026-10-20; recheck `on-release`; used-by `corpus/knowledge/boot-chain-r17.md`.
- Tier rationale [inf]: contract tier A covers "the lane's own re-runnable gate output"; precedent S032 (pacman.log, own-work) and S040 are A. Scope is limited to the timestamped observation, so the row claims no current state.
- `recheck` `on-release`, not a day count: both captures are invalidated by package or boot actions, matching `boot-chain-r17.md` recheck line 3.

## 4. Census W04 rows (7)
The census run output was not re-run in this seat (no bash authorized). The list below is the W04 output recorded for this registry: `corpus/lessons/round-16.md` lines 37–43 and `corpus/lessons/round-16-verifier-spotcheck.md` line 112 ("seven W04 cross-scope duplicate-URL warnings"). Rule per `scripts/sources-census.sh` lines 644–645: a URL already seen under another scope. The URL-to-row duplicates in the table are from the registry, not from the census output.

| row | URL the census reports | row scope (registry) | duplicates |
|---|---|---|---|
| S038 | man.archlinux.org/man/access.2 | access(2) as a root permission-check proxy | S034 |
| S041 | man.archlinux.org/man/systemd.exec.5 | unit path-view mechanisms for read-only `/` | S028 |
| S042 | github.com/omacom/omarchy/issues/8047 | #8047 comment author role for C1/C2 | S036 |
| S043 | github.com/omacom/omarchy/issues/6629 | #6629 comment author role, 4.x claim | S037 |
| S044 | man.archlinux.org/man/systemd.exec.5 | documented `ProtectSystem=` value domain | S028, S041 |
| S046 | man.archlinux.org/man/systemd.exec.5 | `ProtectSystem=` value domain and locator | S028, S041, S044 |
| S049 | man.archlinux.org/man/pacman.8 | `-Q -u` and `--needed` semantics | S048 |

- [obs] The two new rows S051/S052 use repo paths, so they add no W04. Expected W04 count after landing: 7 (unchanged).

## 5. Flags, unknowns, and blocking gaps
1. **Unregistered citations [obs].** `corpus/knowledge/boot-chain-r17.md` line 1 and Sources (lines 165–168) cite **S053** (`https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases`, v42 notes) and **S054** (`https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init`, init:66–67,110). Neither row exists; the provenance trio requires an `S###` row. Not drafted here: not in this item and not opened by this seat. The S054 URL is v42.2 (not the S016 v42 tag).
2. **Mutable-branch pins [unk].** S021 and S022 point at `master`/`main` raw URLs; the anchors name commits 3c011dc… and df088501…. The 2026-10-20 re-open (boot-chain entry) records no upstream blob hash or HEAD commit, so the commit pin is not reconfirmed. The installed hook hashes in `boot-chain-capture.txt` lines 183–184, 215–216, 252–253 are not compared with upstream blobs.
3. **S014 used-by is thin [inf].** `boot-chain-r17.md` cites S014 only in QUALITY item 7 (line 149). The used-by link is real but the scribe may prefer naming S014 in the entry's source line.
4. **Own-work anchors have no file hash.** Neither capture records its own sha256; the anchor uses the capture timestamp. L1 may append `sha256sum` to each capture before landing.
5. **pacnew census gap [obs].** `fresh-capture.txt` lines 77–80: the `/etc` pacnew `find` was aborted; line 82 is a pacman.log sweep only (rc=1). S052 says so explicitly; the knowledge entry must not claim pacnew absence.
6. **sync DB mtimes [unk].** `fresh-capture.txt` lines 10–12 show core/extra/multilib sync DBs dated 2026-10-17 despite a 09:15 `-Syu` (line 4–8). Probably an unchanged-download; not established.

## 6. Installs or updates
None.

Scope: executed=none
