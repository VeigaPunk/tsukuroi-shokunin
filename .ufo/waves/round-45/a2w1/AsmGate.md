VERDICT: defect-found

## Finding

**Assimilation: none.** The staged append is not a safe append against the present lane registry: identifier overlap is directly measured below, including the declared S242–S249 collision subset. Independently, the absent-defect register marks multiple tsukuroi rows, including S230, as having no locator, so those claims are quarantined pending source-level review rather than admitted as evidence.

## Receipts

- `MERGE-REPORT.md:5-9` reports 147 proposed rows and says the lane registry holds 199 rows with first staged id S200. `SOURCES.append.md:5-6` is the staged 11-column table.
- Quarantine extraction (register rows whose lane cell is `tsukuroi`) written to `.ufo/waves/round-45/a2w1/AsmGate/quarantine-slice`: 13 matching table rows. It contains S211 and S213 payload-absent rows, plus S225, S230, S231, S242-S244, and S249-S252 rows for which the gate named no locator. Register source: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:229-230,366-375`.
- ID collision check (`reg-ids` versus `staged-ids`; normalize markdown cell whitespace/backticks, retain S-number identifiers) written to `.ufo/waves/round-45/a2w1/AsmGate/id-collisions.txt`. Observed 183 registry ids, 147 staged ids, 30 intersections: S200, S201, S202, S205, S206, S209, S210, S211, S213, S222, S223, S224, S225, S228, S230, S231, S235, S236, S237, S238, S239, S242, S243, S244, S249, S250, S251, S252, S262, S268. In particular required S242-S249 overlap subset: **S242, S243, S244, S249**.
- Guard fixture: created indented scratch markdown rows (two leading spaces) with matching S999; the 0–3-indent extraction produced `fixture_ids=S999`, proving the leading-indent branch recognizes the fixture. Scratch fixture was under `/fast/scratch/hyaku/tsukuroi-r45/AsmGate/` only.

## Reject at least

Reject staged **S230** (own-work Snapper EACCES entry) for intake pending a properly located, re-openable citation: the register’s quarantine slice explicitly says `round3 | S230` and “the gate block named no locator, so no quote was checked” (register `:367`; slice line 5). The source target named by the staged row is the lane’s own `corpus/knowledge/snapper-eacces-mechanism.md`, not an independent external source (`SOURCES.append.md:37`). This is a source-validation defect, not a conclusion that the underlying host observation is false.

**Theme fit:** none of the examined staged rows supplies evidence for this round’s three narrow surfaces (C1 census first-line robustness; scrub speed sysfs parser / device-replace behavior; systemd stop signal sequence). The staged Btrfs ioctl entry S223 is adjacent filesystem material, not the scrub-speed parser or replace/stop mechanism; its staged knowledge text itself describes interface/flags rather than behavior (`knowledge/corpus/knowledge/btrfs-ioctl-surface-r27.md:9-14,58-63`). The v7.2 upstream UAPI header likewise defines `BTRFS_SUBVOL_*` masks/flags and ioctl argument structs (URL https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/linux/btrfs.h, accessed 2026-10-27; located declarations `BTRFS_SUBVOL_RDONLY`, `BTRFS_SUBVOL_CREATE_ARGS_MASK`, `BTRFS_SUBVOL_DELETE_ARGS_MASK`, `struct btrfs_ioctl_scrub_args`), not the current round’s sysfs parser or systemd stop semantics. The only possible foothold is broad btrfs subject overlap; it does not meet this round’s exact theme.

No campaign tools were run and no source/staged merge files were modified. No tools installed.