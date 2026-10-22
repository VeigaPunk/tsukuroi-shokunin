# S154 — every allocation file the chapter documents

Snapshot: `.ufo/waves/round-30/w1/ScribeSrcSysfsDoc/S154-ch-sysfs.rst`
sha256 `295b92653a70a0b896b10d5ec04bfa7f7c7221c47a00cdb08e0f4f6645803bc6`, 464 lines, 13204 bytes.

Directory naming: the chapter's top-level layout table (line 10) writes `UUID/allocation/`;
the section heading (line 140) and body (line 143, line 163) write `UUID/allocations`
(plural). Kernel 7.2.11 on this host exports `allocation` (singular), matching the table.

## /sys/fs/btrfs/UUID/allocation/ (chapter: allocations)

| File or directory | Line | Mode, since | Chapter's definition |
|---|---|---|---|
| `global_rsv_reserved` | 145 | RO, 3.14 | used bytes of the global reservation (line 148) |
| `global_rsv_size` | 150 | RO, 3.14 | total size of the global reservation (line 153) |
| `data/`, `metadata/`, `system/` directories | 155 | RO, 5.14 | space info accounting for the 3 block group types (line 158) |

## /sys/fs/btrfs/UUID/allocation/{data,metadata,system}/

| File | Line | Mode, since | Notes |
|---|---|---|---|
| `bg_reclaim_threshold` | 165 | RW, 5.19 | reclaimable percentage of block group size, excluding permanently unusable space (lines 168-170) |
| `bytes_*` | 172 | RO | complete list at lines 179-180: `bytes_may_use`, `bytes_pinned`, `bytes_readonly`, `bytes_reserved`, `bytes_used`, `bytes_zone_unusable` |
| `chunk_size` | 182 | RW, 6.0 | data and metadata only, not system, not zoned; multiple of 256MiB, upper bound 10 percent (lines 185-189) |
| `disk_total` | 191 | RO, 3.14 | bytes on devices occupied by this block group type (line 194) |
| `disk_used` | 196 | RO, 3.14 | portion of disk_total used (line 199) |
| `dynamic_reclaim` | 201 | RW, 6.11 | calculated threshold instead of bg_reclaim_threshold (lines 204-205) |
| `flags` | 207 | RO, 6.11 | raw decimal block group flags (line 210) |
| `force_chunk_alloc` | 212 | RW, 6.0, CONFIG_BTRFS_DEBUG | privileged write, can cause ENOSPC (lines 215-216) |
| `periodic_reclaim` | 218 | RW, 6.11 | periodic reclaim based on bg_reclaim_threshold (line 221) |
| `reclaim_bytes` | 223 | RO, 6.11 | monotonically increasing reclaimed bytes (line 226) |
| `reclaim_count` | 228 | RO, 6.11 | monotonically increasing reclaim attempts (line 231) |
| `reclaim_errors` | 233 | RO, 6.11 | monotonically increasing reclaim errors (line 236) |
| `size_classes` | 238 | RO, 6.3 | block groups per class, example output lines 246-249 |
| `total_bytes` | 251 | RO, 3.14 | total bytes (line 254) |

Outside the allocation directory: the top-level `UUID/bg_reclaim_threshold` is documented at
line 38 (RW, 5.19; used-space percentage of total device space, mostly zoned, line 41).

## Host reality against the chapter (kernel 7.2.11, UUID 1d02a454-c549-4a35-b567-89d60902af8e)

Observed at `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/allocation/`:

- `allocation/` holds `global_rsv_reserved`, `global_rsv_size`, `data/`, `metadata/`, `system/`.
- `allocation/data/` and `allocation/metadata/` each hold the type-level `bytes_*` files,
  `total_bytes`, `disk_total`, `disk_used`, `bg_reclaim_threshold`, `dynamic_reclaim`,
  `periodic_reclaim`, `reclaim_bytes`, `reclaim_count`, `reclaim_errors`, `size_classes`,
  `chunk_size`, `flags` — plus a profile subdirectory (`data/single/`, `metadata/dup/`).
- The profile subdirectory holds only `total_bytes` and `used_bytes`. `used_bytes` is not in
  the chapter's `bytes_*` list, and the chapter documents no profile subdirectory level at all.
