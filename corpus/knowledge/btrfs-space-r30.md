source: S152, S153, S154, S155, S156, S157, S158 and S159 in `corpus/SOURCES.md` (btrfs-progs v7.1 Documentation/btrfs-filesystem.rst, ch-balance-filters.rst, ch-sysfs.rst, mkfs.btrfs.rst and ch-subvolume-intro.rst; Linux v7.2 fs/btrfs/block-rsv.c, fs/btrfs/sysfs.c and fs/btrfs/space-info.c); rejected candidates S160 (archived btrfs wiki FAQ) and S161 (ArchWiki Btrfs)
verified-at: 2026-10-22 (capture 2026-10-22T21:16:37Z, kernel 7.2.11-arch1-1, btrfs-progs v7.1)
recheck: `python3 tools/check-btrfs-space-r30.py --revision <REV>` for the row evidence; re-read `/sys/fs/btrfs/<fsid>/allocation/{global_rsv_size,global_rsv_reserved,metadata/bytes_used,metadata/total_bytes,data/disk_total,metadata/disk_total,system/disk_total}` and `btrfs filesystem usage -b /` (unprivileged, read-only) for the host readings; re-open the sources on a btrfs-progs or kernel release
companion: `corpus/knowledge/btrfs-space-r30.json` (rows D01 to D10, counted by `tools/check-btrfs-space-r30.py`)

# Btrfs space allocation and ENOSPC (round 30)

## Scope

This entry adds the space-allocation side of the root btrfs filesystem to the host and rollback-net surface: why a btrfs host can return `ENOSPC` while `df` shows free space, what the global reserve is, which read-only files show the state, and which repair decisions exist. It covers mechanism and repair decisions only. Disk runway (how full the disk is, and when to warn) belongs to mori: mori's `SKILL.md:415-418` (commit `05db57ed`) already rules "Never threshold the btrfs chunk percent" and keeps the `df -P` parser. This entry does not set a runway threshold and does not replace that rule. The boundary is recorded here only; no handoff was sent to mori and no mori acknowledgement exists (wave-2 CritAdjacencyMori). Every repair named here (balance, snapshot deletion) is an operator write; the lane runs none of them.

Host at capture time: root is btrfs on LUKS (`/dev/mapper/root`, `dm-0`), one device of 998037782528 bytes, data profile `single`, metadata and system `DUP` (`btrfs filesystem usage -b /`, saved beside the capture). An earlier entry already named the allocation directory and the metadata `dup` profile for scrub repair (`SKILL.md` row SH3, `corpus/knowledge/storage-health-r26.md:45`); rows D04 and D06 restate those two facts for the space question. New depth for the lane: D01, D02, D03 and D07, and D05 (thin; its reading below rests on a supporting S159 citation). D08 to D10 are point-in-time host captures, not durable depth; D09's capture line is a derived arithmetic line, cross-checked against `Device unallocated` in `btrfs filesystem usage -b /`. Three snapshots are the same bytes the lane already held from round 26: S155 equals S130 (`mkfs.btrfs.rst`), S158 equals S133 (`fs/btrfs/sysfs.c`), and S154 equals an unregistered round-26 supporting file (`ch-sysfs.rst`); they were re-opened this round, but they are not new authorities (wave-2 CritClaimFraming2).

## How the space is split

Btrfs allocates the device in chunks (block groups) of one type: data, metadata or system. `Device allocated` is the sum of all chunks; `Device unallocated` is the rest, "the remaining unallocated space for future allocations" (S152 line 398). Free space inside a data chunk cannot hold metadata. Metadata on one device uses the `DUP` profile by default (S155 line 59), so each metadata byte costs two raw bytes; this host's `Metadata ratio` reads 2.00.

The kernel's metadata reservations may overcommit only against unallocated space; "If there is no unallocated space to be had, all reservations are kept within the free space in the allocated metadata chunks" (S159 lines 176-178). That is the classic btrfs `ENOSPC` with free space: data chunks have room, metadata chunks are full, and no unallocated space is left to allocate a new metadata chunk.

The global reserve is "portion of metadata currently used for global block reserve, used for emergency purposes (like deletion on a full filesystem)" (S152 lines 418-420). Its size comes from the used bytes of the root, extent, checksum and free-space trees and is capped at 512 MiB (S156 line 394: `block_rsv->size = min_t(u64, num_bytes, SZ_512M);`). It is reserved space, not free space.

## Decision table

| Reading | What it means | Decision |
|---|---|---|
| `Device unallocated` well above one metadata chunk (`metadata/chunk_size`, 1 GiB here, capture line 52) | New metadata chunks can still be allocated; a high metadata fill is not yet an ENOSPC risk (S152 line 398, S159 line 177) | No action; record the reading |
| `Device unallocated` near 0 and metadata `bytes_used / total_bytes` near 100 percent | Metadata reservations are confined to the existing metadata chunks (S159 177) | Operator: free data chunks with a usage-filtered balance (`btrfs balance start -dusage=N`, S153 line 51), starting with `-dusage=0`, which needs no new work space (S153 lines 52-54) |
| `ENOSPC` while `df` shows free space, snapshots present | Snapshots keep shared extents allocated; deleting files in the original frees nothing they still reference (S157 lines 39-41, 202-206) | Operator: deleting the snapshots that reference the extents is what returns the space; choosing which is the operator's decision |
| `global_rsv_reserved` below `global_rsv_size` | The reserve is under-funded: `global_rsv_reserved` reports `block_rsv->reserved` (S158 lines 681-688), which the kernel tops up toward `size` (S156 lines 395-397) `[inf]` | Re-read; a persistent shortfall with no unallocated space is the D01 case (corrected after wave-2 RevKnowledgeNote) |
| `bg_reclaim_threshold` per type | A percentage of block-group size: the v7.2 periodic sweep reclaims a block group whose used bytes fall below it (S154 lines 168-169; S159 lines 2154-2155) | Read only; the lane never writes it (RW since 5.19) |

## Host readings (capture `.ufo/waves/round-30/w1/ExecHostCapture/btrfs-allocation-capture.txt`)

- Metadata `bytes_used` 35372056576 of `total_bytes` 38654705664 (91.5 percent), line 50 and line 67.
- Unallocated 690922455040 bytes, line 98: device 998037782528 minus data `disk_total` 229789138944, metadata `disk_total` 77309411328 and system `disk_total` 16777216; `btrfs filesystem usage -b /` reports the same `Device unallocated`.
- `global_rsv_size` 536870912 and `global_rsv_reserved` 536870912 (lines 44 and 43): the reserve is at the 512 MiB cap and full.
- Metadata `bg_reclaim_threshold` 0 (line 45) and `dynamic_reclaim` 0 (line 57). The sysfs chapter does not say what 0 means. In the v7.2 periodic sweep, `btrfs_calc_reclaim_threshold` returns `bg_reclaim_threshold` when `dynamic_reclaim` is 0 (S159 lines 2111-2117), and a block group is reclaimed only when `bg->used < thresh` with `thresh = mult_perc(bg->length, thresh_pct)` (S159 lines 2154-2155), so a threshold of 0 marks no metadata block group in that sweep `[inf]`. The other reclaim paths in `fs/btrfs/block-group.c` were not opened; `[unk]`.

Reading: metadata is 91.5 percent full, but 643 GiB is unallocated, so the kernel can still allocate new metadata chunks. This host is not near metadata `ENOSPC` at capture time. The readings are a point-in-time capture; re-read them before acting.

## Sources not admitted

- S160, the archived btrfs wiki FAQ: self-declared obsolete, last modified 2022, version-unpinned, and its recipe selects block groups by count (`-dlimit=3`), a filter v7.1 still documents (`ch-balance-filters.rst` line 114) but does not offer for ENOSPC, where it points to `usage=0` (S153 lines 52-54). Corrected after wave-2 RevSourceS160: an earlier wording said v7.1 does not document `limit`.
- S161, the ArchWiki Btrfs page: opened and readable, but it adds nothing the tier-A sources do not; rejected with a flip condition.

## Limits

- `[unk]` Reclaim paths other than the periodic sweep (`fs/btrfs/block-group.c`, not opened).
- `Free (estimated)` has no formula in S152; this entry does not compute it.
- No balance, snapshot deletion or sysfs write was run; every decision above is for the operator.
