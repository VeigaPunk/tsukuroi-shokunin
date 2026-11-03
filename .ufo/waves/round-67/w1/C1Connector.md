2026-11-03T22:08:30Z
# C1Connector — sibling overlap scan (scoped findings)

Full evidence, commands and rc: .ufo/waves/round-67/drafts/C1Connector-overlap.md (same lane). Lane HEAD 071a55c9c0fd022890d1b255c2782e4761e7a7d8. Read-only; no sibling file touched.

## Item 1 — btrfs scrub-limit material
- Sibling HEADs read 2026-11-03T22:07:35Z (table in the draft §0; kagi and kasegi moved since the first listing).
- Scoped search (`git -C <dir> grep -l -E 'scrub_speed_max|scrub limit|btrfs-progs|btrfs scrub' HEAD -- corpus tools PROVINCE.md SKILL.md`): one sibling hit, mori-shokunin 84c6cbc3.
- OV-C1 rows: 7 (OV-C1-1..7), all mori-shokunin corpus/evidence/sources-r55/btrfs_sysfs.c.v7.3 at lines 2021, 2028, 2031, 2045, 2048, 2049, 2113. All AGREES on the sysfs attribute mechanics (SR8). All are KERNEL sysfs.c at tag v7.3, not btrfs-progs cmds/scrub.c.
- C1 revert (btrfs-progs v7.3 scrub.c): NONE in any sibling.
- Siblings with no in-scope hit: audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, revenger, souji, tabi, tameshi (none).
- Out-of-scope (.ufo wave records, not counted): 13 refs. One CONFLICTS: tabi round-34 tsukuroi.diff:172, :218, :222 carries the r42 SC1/SC3 wording withdrawn in r42 wave-2 and r43.

## Item 2 — adjacency gate silent-skip pattern
- OV-C2 rows: 10 (2 MATCH: kama round46-release-recheck-audit.py:371 and round44-release-recheck-audit.py:327; 8 PARTIAL). All unexercised, from source read.
- Lane pattern is `_live_object_hash` (check-adjacency-anchors.py:447-463) feeding `if live_digest is not None: counts[...] += 1` (:648-651). No sibling reproduces it exactly; the two MATCH rows are the nearest in effect.

## Item 3 — ownership split
- ADJ-04 (mori): STANDS. Mori PROVINCE.md:25 (Kill/OOM classes) and :26 (Resource runway, SURFACE disk, df -P on $ROOT and /tmp). Lane PROVINCE.md:49 and :125.
- ADJ-06 (kaidoku/revenger): UNCHANGED, unresolved. No scrub or runway sibling hit touches RE ownership. Lane PROVINCE.md:51, :79.
- Disk-runway split (lane PROVINCE.md:165-167, :176): STANDS. Mori corpus/knowledge/disk-runway-enospc-r55.md:23-58 reads `/` btrfs free space as fleet runway (mori's question), while the lane reads it as an upgrade precondition.

## Counts
- OV-C1 rows: 7
- OV-C2 rows: 10
- Output draft: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-67/drafts/C1Connector-overlap.md
