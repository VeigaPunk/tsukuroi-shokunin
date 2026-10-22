# S158 attribute inventory — /sys/fs/btrfs/<UUID>/allocation/ at Linux v7.2

Snapshot: `.ufo/waves/round-30/w1/ScribeSrcKSysfs/S158-sysfs.c` (2702 lines), sha256
`ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`.
Modes are the literal `.mode` values in the `__INIT_KOBJ_ATTR` macros at lines 68-78:
`BTRFS_ATTR_W` 0200 (line 70), `BTRFS_ATTR_RW` 0644 (line 74), `BTRFS_ATTR` 0444 (line 78).
"World-readable" below means mode 0444, i.e. readable by any user without root.

## The directory itself

Created as a kobject named `allocation` at lines 2338-2340; its files are created from
`allocation_attrs` at line 2345. The group (lines 1066-1069) has exactly two members:

| File | Declaration | Show function | Mode | World-readable |
|---|---|---|---|---|
| `global_rsv_reserved` | line 688 (`BTRFS_ATTR(allocation, global_rsv_reserved, ...)`) | lines 681-687, emits `block_rsv->reserved` | 0444 | yes |
| `global_rsv_size` | line 679 (`BTRFS_ATTR(allocation, global_rsv_size, ...)`) | lines 672-678, emits `block_rsv->size` | 0444 | yes |

## Per-type subdirectories, allocation/<bg-type>/

The kobject name comes from `alloc_name()` (lines 1902-1936), added at lines 1948-1950:
`mixed` (1908), `metadata` (1912), `metadata-treelog` (1914), `data` (1922),
`data-reloc` (1924), `system` (1931), `metadata-remap` (1933); `invalid-combination` (1936)
is the WARN fallback. Files come from `space_info_attrs` (lines 1024-1044).

| File | Declaration line | Kind | Mode | World-readable |
|---|---|---|---|---|
| `flags` | 896 | read-only (`SPACE_INFO_ATTR`) | 0444 | yes |
| `total_bytes` | 897 | read-only | 0444 | yes |
| `bytes_used` | 898 | read-only | 0444 | yes |
| `bytes_pinned` | 899 | read-only | 0444 | yes |
| `bytes_reserved` | 900 | read-only | 0444 | yes |
| `bytes_may_use` | 901 | read-only | 0444 | yes |
| `bytes_readonly` | 902 | read-only | 0444 | yes |
| `bytes_zone_unusable` | 903 | read-only | 0444 | yes |
| `disk_used` | 904 | read-only | 0444 | yes |
| `disk_total` | 905 | read-only | 0444 | yes |
| `reclaim_count` | 906 | read-only | 0444 | yes |
| `reclaim_bytes` | 907 | read-only | 0444 | yes |
| `reclaim_errors` | 908 | read-only | 0444 | yes |
| `chunk_size` | 909 | read-write (`BTRFS_ATTR_RW`) | 0644 | yes (root writes) |
| `size_classes` | 910 | read-only | 0444 | yes |
| `bg_reclaim_threshold` | 948-950 | read-write | 0644 | yes (root writes) |
| `dynamic_reclaim` | 981-983 | read-write | 0644 | yes (root writes) |
| `periodic_reclaim` | 1014-1016 | read-write | 0644 | yes (root writes) |
| `force_chunk_alloc` | 892 | write-only (`BTRFS_ATTR_W`), only when `CONFIG_BTRFS_DEBUG` (guard at 850 through 894; group at 1042-1044) | 0200 | no |

`SPACE_INFO_ATTR` (line 741) expands to `BTRFS_ATTR` at line 749, so every field declared
through it gets 0444.

## Per-profile subdirectories, allocation/<bg-type>/<bg-profile>/

Created per block-group profile by `btrfs_sysfs_add_block_group_type` (comment at 1815-1817
names the path `/sys/fs/btrfs/UUID/allocation/data/TYPE`; kobject added at 1866-1867 with the
name from `btrfs_bg_type_to_raid_name()`). Files come from `raid_attrs` (lines 724-725).

| File | Declaration line | Show | Mode | World-readable |
|---|---|---|---|---|
| `total_bytes` | 695 (`BTRFS_ATTR(raid, total_bytes, raid_bytes_show)`) | lines 698-717, sums `block_group->length` | 0444 | yes |
| `used_bytes` | 696 (`BTRFS_ATTR(raid, used_bytes, raid_bytes_show)`) | lines 698-717, sums `block_group->used` | 0444 | yes |

## Related surface outside allocation/ (not part of the directory listing)

`/sys/fs/btrfs/<UUID>/bg_reclaim_threshold` is a separate filesystem-wide attribute:
declaration at 1541-1542, show at 1508-1515, store at 1517-1539; mode 0644; outside
`CONFIG_BTRFS_DEBUG` the store rejects any non-zero value at or below 50 (lines 1529-1535).
