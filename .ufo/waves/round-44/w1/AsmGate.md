VERDICT: no-finding

Seat AsmGate, round 44 w1, item F-8. Read-only evaluation of `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/` (MERGE-REPORT.md/.json, `knowledge/` 70 files, `SOURCES.append.md` 147 rows S200-S346). Receipts: `.ufo/waves/round-44/w1/AsmGate/` (`receipts.txt`, `quarantine-slice`, `reg-ids`, `staged-ids`, `collisions`). Access date for every URL: 2026-10-26. No campaign tool run; nothing written outside my report and receipts; scratch `/fast/scratch/hyaku/tsukuroi-r44/AsmGate` removed.

## Recommendation (one line)

**`Assimilation: none`.** No staged entry matches this round's surfaces (scrub record, sysfs `scrub_speed_max`, systemd timers, census arms), and none is adoptable as staged. **Reject: `ext4-journal-guarantee-r32.md`** and **`btrfs-ioctl-surface-r27.md`** (sections 4-5). Round 43's two named entries (`initramfs-hook-api-r25.md` refused-conditional, `ext4-journal-guarantee-r32.md` rejected) have **no flip condition cleared** (section 6).

## 1. Theme sweep (btrfs scrub / sysfs / systemd timers / census arms)

- `grep -ciE scrub MERGE-REPORT.md MERGE-REPORT.json SOURCES.append.md` -> 0, 0, 1 (the 1 is S269, the ext4 row, `SOURCES.append.md:76`).
- Over `knowledge/`: `scrub` appears only in `ext4-journal-guarantee-r32.md:6,37,48`. Regex `btrfs_scrub|scrub_speed|devinfo|btrfs-scrub|timers.target|OnCalendar|Persistent=|KillSignal|/var/lib/btrfs` over `knowledge/` + `SOURCES.append.md` -> 0 hits; `sysfs` and `\.timer` -> 0 hits. Nothing staged bears on SR7 (`btrfs_scrub_progress` returns), SR8 (`scrub_speed_max`), SR9 (Arch `btrfs-scrub@.timer`/`.service`) or the census `SCRUB` line.
- Nearest btrfs entries: `btrfs-ioctl-surface-r27.md` (ioctl numbers), `btrfs-filesystem-troubleshooting-bilingual-r26.md` (SUSE ENOSPC procedure), `btrfs-space-repair-amend-2026-10-23.md` (restates the lane's own `btrfs-space-r30.md`/`btrfs-repair-r31.md`). Nearest systemd: `mkinitcpio-42-upgrade-gate-cjk-r26.md` (the `systemd` hook, `systemd-pcrosseparator.service`), `snapshot-boot-preconditions-amend-2026-10-23.md`. None touches the scrub status record, a timer unit, or a sysfs attribute.
- Why no adopt: the instruction asks for an entry that matches the round's surface or `Assimilation: none`. Adopting an off-theme entry would add corpus without a counter and without any C1/C2 claim resting on it.

## 2. Quarantine slice (derived)

Command (receipts.txt): `awk -F'|' -v l='tsukuroi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' <register>` -> **12 rows** in `w1/AsmGate/quarantine-slice`. Register sha256 `5afe1810...d833`, unchanged from round 43; `cmp` equal to `.ufo/waves/round-43/w1/AsmGate/quarantine-slice`. Rows: S211, S213 (`payload-absent`); S225 (source not fetched); S230, S231, S242, S243, S244, S249, S250, S251, S252 (gate block named no locator).

**New hazard (not present in round 43): the slice ids S242, S243, S244 are STAGED ids and now collide with the lane's own round-44 rows.** `corpus/SOURCES.md:251-253` at HEAD ff2c264a: lane S242 = Linux v7.2.11 `fs/btrfs/scrub.c`, S243 = `fs/btrfs/sysfs.c`, S244 = Arch btrfs-progs packaging 7.1-1 — exactly the three C2 sources. Staged S242/S243/S244 (`SOURCES.append.md:49-51`) are the lane's own `boot-writers-r19.md`, `btrfs-space-r30.md`, `btrfs-repair-r31.md` (tier A own-work, hence "no locator"). A reader who matches the quarantine slice to the landed registry by id would wrongly flag C2's S242-S244 as quarantined. Quarantine entries must be read as (lane, round, staged id), never as lane ids >= S200. None of the 12 slice rows is a row C2 cites under its own meaning.

## 3. Id collision check (reg-ids vs staged-ids)

Extractor `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort`. Lane `git show HEAD:corpus/SOURCES.md` (HEAD ff2c264a) -> **245 ids** (S001-S245); `SOURCES.append.md` (sha256 `7914d3b9...8406`) -> 147 ids (S200-S346). `comm -12` -> **46 collisions, S200-S245** (`w1/AsmGate/collisions`); round 43 recorded 42 (S200-S241). The four new ones are S242-S245, added by round 44 itself (S245 staged = Chinese mkinitcpio wiki row, lane S245 = host scrub capture). Any landing of staged rows or entries needs renumbering against the lane (next free id S246 and above; staged S246-S346 do not collide yet but will after the next lane round).

## 4. Reject: `btrfs-ioctl-surface-r27.md` (staged S223)

Source-checked reasons (S240, Linux v7.2.11 `ioctl.c`, `.ufo/waves/round-43/frozen/src/ioctl.c`, sha256 `7b3488f2...ba01`):
1. Line 14 "Together they close the btrfs ioctl surface" and lines 31-32 "the command surface is stable and enumerable - a caller can be identified from its ioctl number alone" rest on a **nine-row table**. `grep -c "case BTRFS_IOC_" ioctl.c` -> **64** dispatch labels in `btrfs_ioctl`; the table has 9. Eight-fold undercount, stated as closure (QUALITY 22 exhaustive-claim, 66 overstatement).
2. The scrub trio is in the dispatch and not in the table: `ioctl.c:5578-5583` "case BTRFS_IOC_SCRUB: return btrfs_ioctl_scrub(file, argp); case BTRFS_IOC_SCRUB_CANCEL: ... case BTRFS_IOC_SCRUB_PROGRESS:". These are the very ioctls this round's C2 rows SR7/SR9 reason about (progress success direction, SIGINT cancel), so the staged "closed surface" claim is directly contradicted by the round's own pinned source.
3. Entry source S223 is `.../torvalds/linux/v7.2/...btrfs.h`, a different tag from the lane's pinned v7.2.11; no QUALITY check (14). Same defect as round-42/43 rejection; unchanged.

## 5. Reject: `ext4-journal-guarantee-r32.md` (staged S269/S270)

Re-checked this round against live bytes (journal.html sha256 `2e6693a2...5649`, identical to round 43):
1. **Out of province**: `findmnt -rno TARGET,FSTYPE` -> `/ btrfs`, `/home btrfs`, `/boot vfat`, `/fast xfs`; no ext4. `grep -n -iE "ext4|jbd" PROVINCE.md` -> 0.
2. **First quote is a splice.** Staged `ext4-journal-guarantee-r32.md:15-16`: "For performance reasons, ext4 by default only writes filesystem metadata" / "file data blocks are /not/ guaranteed to be in any consistent state after a crash." Live page text (extracted, whitespace-collapsed): "ext4 by default only writes filesystem metadata through the journal. This means that file data blocks are /not/ guaranteed to be in any consistent state after a crash." The words "through the journal. This means that" are dropped with no ellipsis (QUALITY 19/21).
3. **Btrfs comparison row unscoped for this host**: "repairs corruption? btrfs: yes, from a replica" vs `storage-health-r26.md:11` (data profile `single`) and this host's `btrfs filesystem df /` -> "Data, single: total=258.01GiB"; one copy means a bad data block is not repairable by scrub (`storage-health-r26.md:43`).
4. No `## QUALITY check` (QUALITY 14).

## 6. Round-43 flip conditions re-checked

- `initramfs-hook-api-r25.md` (refused-conditional). Conditions were: renumber S200/S210; add `## QUALITY check`; replace README line-range `ground:`; add post-hook/`/etc/mkinitcpio.d` rows; re-quote at landing. **None cleared**: S200 and S210 still collide (section 3); `grep -rl "## QUALITY check"` over staged `knowledge/` -> 0 of 70; the entry file is unchanged (package dated Oct 24, MERGE-REPORT sha256 `3b14f7b3...5fa`); mkinitcpio unchanged (`pacman -Q mkinitcpio` -> 42.2-1; man page raw sha256 `3f274415...d90f`, "Date: 2026-10-01", identical to round 43). `corpus/SOURCES.md:343` still holds mkinitcpio(8) as an unopened lead only. Stays refused; and it is off-theme this round regardless.
- `ext4-journal-guarantee-r32.md` (rejected): points 1-4 above all still hold; nothing cleared.
- Side note: `/etc/initcpio/{hooks,install,post}` still empty on the host (`ls` shows no entries). The round-43 side finding about `boot_inputs_newer` is unchanged and not re-opened here.

## Not done

- Did not read all 70 entries line by line; sweeps cover them by regex only. Did not re-open staged S269/S270 `quote` cells beyond the one entry quote.
- Did not run a census, counter or lane gate. Did not fetch the S223 header at v7.2.11 (only counted dispatch labels in the lane-pinned `ioctl.c`; the table-vs-header diff was not done).
- Tool installs: none. Lane, fleet, register and staged package untouched. (`pacman -Q` printed a stray `openai-chatgpt: missing required signature` line on stderr-style output; unrelated, host not modified.)

Report: .ufo/waves/round-44/w1/AsmGate.md
