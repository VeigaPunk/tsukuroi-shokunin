# SrcKernelVolumes — C1 source S132, Linux v7.2 `fs/btrfs/volumes.c`

Verdict: done — the tag `v7.2` exists and the file is at the path named by the assignment, the snapshot is saved with digest `f3400af8e924bc7743d28f43b45f02be1bc84e25de00ac99d2bfc8bab19a4fbf` (8976 lines), and it supports SH2 outright while supporting SH1 only for the ioctl half (the sysfs `error_stats` half is not in this file).

## 0. Fetch record

- Command: `curl -sS -A "Mozilla/5.0 (X11; Linux x86_64) tsukuroi-source-fetch" -o S132.c https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/volumes.c` (attempt 5 of a bounded retry loop; attempts 1-4 returned HTTP 429 rate-limit, attempt 5 returned HTTP 200).
- Snapshot written to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S132.c`.
- Digest and size: `sha256sum S132.c` → `f3400af8e924bc7743d28f43b45f02be1bc84e25de00ac99d2bfc8bab19a4fbf`; `wc -l S132.c` → `8976`; `stat -c %s` → `252468` bytes; the file ends with a newline (`tail -c 1 | od -c` → `\n`).
- Tag verification [obs]: `https://github.com/torvalds/linux/tree/v7.2/fs/btrfs` → HTTP 200, and the raw path `.../v7.2/fs/btrfs/volumes.c` returned 200 with real source bytes (first bytes `// SPDX-License-Identifier: GPL-2.0`). The file did **not** move at that tag; it is still `fs/btrfs/volumes.c`.
- Host relevance [obs]: the frozen capture records `smartctl 7.5 2025-04-30 r5714 [x86_64-linux-7.2.11-arch1-1]` at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt:177`, so the v7.2 tag is the same kernel series as the running kernel.

## 1. Proposed SOURCES row (11-column contract shape, no `|` inside any cell)

| S132 | Linux v7.2 fs/btrfs/volumes.c device error statistics — https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/volumes.c | code | A | Per-device btrfs error counters: how the five counters are printed, loaded from the device tree at mount, written back at transaction commit and zeroed only by an explicit reset, for the host kernel 7.2.11 | tag v7.2, fs/btrfs/volumes.c, lines 8186-8227 (load of the dev_stats item at mount), 8290-8348 (write back), 8351-8354 (write back at transaction commit), 8422-8436 (per-error log line), 8438-8456 (print on load), 8458-8495 (ioctl read and explicit reset); raw bytes sha256 f3400af8e924bc7743d28f43b45f02be1bc84e25de00ac99d2bfc8bab19a4fbf | The five counters are cumulative per device, survive unmount because they are reloaded from the on-disk device tree, and are cleared only by an explicit reset; the kernel prints their cumulative values both per error and at mount, so a non-zero counter is not by itself a dated incident | mined | 2026-10-22 | on-release | corpus/knowledge/storage-health-r26.md |

Note for the entry owner: the four quotes in section 2 are the exact texts that must also appear in this source's row of the lesson `## Gate` table, byte-for-byte.

## 2. Exact quotes (≤ 25 words each, byte-for-byte from the saved snapshot)

Q1 — grounds SH1 (the five counters and their names) and SH2 (the per-error log line). Source line 8429 (`fs/btrfs/volumes.c`):

    "bdev %s errs: wr %u, rd %u, flush %u, corrupt %u, gen %u",

Q2 — grounds SH2 (the counters are written back to disk, so they persist across mounts). Source line 8352:

    called from commit_transaction. Writes all changed device stats to disk.

Q3 — grounds SH2 (only an explicit reset clears them). Source line 8477:

    } else if (stats->flags & BTRFS_DEV_STATS_RESET) {

Q4 — grounds SH1 (the `btrfs device stats` query reads the same in-memory counters). Source line 8490:

    stats->values[i] = btrfs_dev_stat_read(dev, i);

Byte-exactness was verified with `grep -qF -- "<quote>" S132.c` for each of the four texts: all four returned FOUND. Leading indentation of the source line is trimmed in the quote above; the text after the first non-blank character is unchanged.

## 3. Support, limits and contradictions against the declared wording

### SH1 — "what the five btrfs per-device error counters (write, read, flush, corruption, generation) count, and that the sysfs `error_stats` file and the `btrfs device stats` query report the same counters"

- **Supports (partly)** [obs]: the file names the five counters and shows them all read from the same per-device array. Lines 8431-8435 (inside the per-error print) read `BTRFS_DEV_STAT_WRITE_ERRS`, `BTRFS_DEV_STAT_READ_ERRS`, `BTRFS_DEV_STAT_FLUSH_ERRS`, `BTRFS_DEV_STAT_CORRUPTION_ERRS` and `BTRFS_DEV_STAT_GENERATION_ERRS`; lines 8442-8445 iterate `i < BTRFS_DEV_STAT_VALUES_MAX` over the same values. The `btrfs device stats` query is the ioctl path `btrfs_get_dev_stats()` at lines 8458-8495, whose non-reset arm (line 8490, Q4) fills `stats->values[i]` from `btrfs_dev_stat_read(dev, i)`, i.e. the same counters the log line prints.
- **Limits** [obs]: this file contains no sysfs `error_stats` file at all. A case-insensitive search for `error_stats` over all 8976 lines returns nothing; `sysfs` appears only as `#include "sysfs.h"` (line 22) and calls to `btrfs_sysfs_add_device` / `btrfs_sysfs_remove_device` (lines 2447, 2564, 2996). The sysfs file body lives in `fs/btrfs/sysfs.c`, which is the separately declared source S133. Therefore S132 alone can ground only the ioctl half of SH1's "same counters" claim; the sysfs half is S133's to ground, and the entry must cite both.
- **Limits** [obs]: the file names the counters through the `BTRFS_DEV_STAT_*` constants but does not define what each one counts, and it does not contain the enum definition or the mapping from ioctl index to counter name (the uapi header `include/uapi/linux/btrfs.h` holds the enum). The semantic definition of the five counters belongs to S128 (`Documentation/btrfs-device.rst`).
- **Limits** [obs]: no `btrfs_dev_stat_inc` call site other than the helper itself exists in this file (the only occurrences of `btrfs_dev_stat_inc` are line 8406 in a comment and line 8424 inside `btrfs_dev_stat_inc_and_print`). The paths that actually raise a write, read, flush, corruption or generation error live in other translation units, so this file cannot by itself prove which kernel event increments which counter.

### SH2 — "those counters persist across mounts until an explicit reset, so a non-zero value is not a dated incident; a dated incident comes from the kernel's per-error log line"

- **Supports** [obs]: the counters are persisted, reloaded and only explicitly cleared.
  - Load at mount: `btrfs_device_init_dev_stats()` at lines 8186-8227 searches the device tree for the device's item (`key.objectid = BTRFS_DEV_STATS_OBJECTID;` line 8198; the search call at line 8201 is `ret = btrfs_search_slot(NULL, device->fs_info->dev_root, &key, path, 0, 0);`) and copies the stored values into the in-memory counters (lines 8215-8221); when the item is absent it zeroes them (lines 8203-8204).
  - Write back: `update_dev_stat_item()` at lines 8290-8348 stores the current counters back into the same device-tree item, and `btrfs_run_dev_stats()` (line 8354) is documented at line 8352 as `called from commit_transaction. Writes all changed device stats to disk.` (Q2), so a committed change survives unmount.
  - Explicit reset: the only clearing path is the `BTRFS_DEV_STATS_RESET` flag in `btrfs_get_dev_stats()` (line 8477, Q3), which uses `btrfs_dev_stat_read_and_reset` (line 8481) or `btrfs_dev_stat_set(dev, i, 0)` (line 8483), and logs line 8485-8486 `btrfs_info(fs_info, "device stats zeroed by %s (%d)", ...)`. No other zeroing of the in-memory counters exists in this file.
  - Dated incident: the per-error path is `btrfs_dev_stat_inc_and_print()` at lines 8422-8436, which increments the counter and then prints the five cumulative values with `btrfs_err_rl` (line 8428) in the format of Q1 (line 8429).
- **Limits — the wording "a dated incident comes from the kernel's per-error log line" is true but incomplete** [obs]: the same `bdev %s errs: ...` text is printed on two different occasions.
  - On an error: line 8428-8429, at error severity via `btrfs_err_rl`.
  - On mount: `btrfs_dev_stat_print_on_load()` at lines 8438-8456, called from `btrfs_device_init_dev_stats()` at line 8224, prints the identical format string at line 8449 but at info severity via `btrfs_info` (line 8448). It is suppressed only when every counter is zero — line 8446 reads `return; /* all values == 0, suppress message */`.
  So the format string alone does not date an incident: the journal entry's severity and timestamp are what distinguish "counters were non-zero at mount" from "an error just happened". The entry should say the line must be read with its severity, not that the line is inherently per-error.
- **Limits — the per-error line is rate-limited** [inf]: the print goes through `btrfs_err_rl` (line 8428), whose rate-limit parameters are defined in `fs/btrfs/super.c`, not in this snapshot [unk]. Therefore not every error necessarily yields a log line, and "no `errs: wr` line in the journal" is not by itself proof that no error occurred.
- **Limits — persistence has a commit boundary** [inf]: `btrfs_run_dev_stats()` only writes changed devices when `atomic_read(&device->dev_stats_ccnt) != 0` (lines 8380-8396), and the write happens inside a transaction commit. An increment made just before a crash or power loss and never committed is lost, so "persist across mounts" is true for committed increments. [unk] The capture records 200 unsafe shutdowns on this NVMe device, so this caveat is not vacuous for this host.
- **Limits — the "device tree" here is btrfs's `dev_root` tree, not sysfs** [obs]: lines 8198 and 8302 key the item by `BTRFS_DEV_STATS_OBJECTID` under `device->fs_info->dev_root` (line 8201). This is the btrfs device tree, distinct from the sysfs device directory that carries `error_stats`.

## 4. Anything in the source that contradicts the frozen capture's host facts

- **No contradiction found** [obs]. Each capture fact checked against this snapshot:
  - Capture `capture.txt:39-44` — sysfs `error_stats` shows `write_errs 0`, `read_errs 0`, `flush_errs 0`, `corruption_errs 0`, `generation_errs 0`; capture `capture.txt:112-116` — `btrfs device stats /` shows `write_io_errs 0`, `read_io_errs 0`, `flush_io_errs 0`, `corruption_errs 0`, `generation_errs 0`. The two views carry the same five counters under different field names (sysfs drops the `io_` infix); the kernel side of that mapping is `btrfs_get_dev_stats()` (lines 8458-8495) for the query and `fs/btrfs/sysfs.c` (S133) for the file. Consistent, and it corroborates SH1's "the same counters" claim at the level of counter identity.
  - Capture `capture.txt:154-156` — the kernel journal grep for `BTRFS.*errs: wr` counted `0` over 6 retained boots; capture `capture.txt:163-165` shows the current boot's 7 `BTRFS` kernel lines are all mount-time info, none of them a `bdev ... errs:` line (`capture.txt:167-173` lists them). This is exactly what the source predicts: with every counter at zero, `btrfs_dev_stat_print_on_load()` returns at line 8446 before printing, and no error path ran. Consistent, and it is a positive prediction of the source rather than a coincidence.
  - Capture `capture.txt:157-159` — zero `BTRFS (error|critical|warning)|forced readonly` lines. Consistent with the same zero counters; the source says nothing that would predict such a line here.
  - Capture device identity `[/dev/mapper/root]` (LUKS dm device) and the boot log `BTRFS info (device dm-0): ...` (`capture.txt:168-173`) — consistent with line 8430, `btrfs_dev_name(dev)`, which prints the kernel's device name for the same device.
- **One thing the capture cannot establish** [obs]: persistence across mounts. Every counter on this host is zero and no reset or scrub was performed, so the capture provides no positive observation of a value surviving a remount. The persistence claim rests on the source (section 3), not on the capture.
- **One caveat the capture makes relevant** [obs]: the capture's zero counters are cumulative-since-inception values read at one moment. Per SH2 as supported above, that is a "no error ever recorded for this device" statement, not a statement about the last six boots only, and it is not a statement that the NVMe device never had a media error (that is the separate SMART counters of SH5 and SH6, sourced elsewhere).

## 5. Out of scope for this seat

- The sysfs `error_stats` file body (S133, `fs/btrfs/sysfs.c`).
- The semantic definitions of the five counters (S128, `Documentation/btrfs-device.rst`) and the uapi enum (`include/uapi/linux/btrfs.h`), neither of which is in this snapshot.
- The scrub behaviour and profiles (S129, S130), the scrub timer (S131), smartctl and NVMe lifetime fields (S134, S135) — none of these appear in `fs/btrfs/volumes.c`.
- The rate-limit constants for `btrfs_err_rl` (`fs/btrfs/super.c`) — not opened here.

## 6. Commands executed

- `curl` of the raw file at tag v7.2 (5 attempts; 429, 429, 429, 429, 200).
- `sha256sum`, `wc -l`, `stat -c %s`, `od -c` on the saved snapshot.
- `grep -n`/`grep -qF` over the saved snapshot for the counter constants, the quote texts, `error_stats`, `sysfs`, `btrfs_dev_stat_inc`.
- `awk` line-range reads of the snapshot at 8160-8500 and 8349-8360.
- `git`/`jj`: none. Host state: no command was run against the host filesystem beyond reading the frozen capture text; no sudo, no service, no scrub, no counter reset.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md (round-26 declaration), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md (11-column shape and mined rows), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt (lines 39-44, 104-178), and the fetched Linux v7.2 fs/btrfs/volumes.c bytes; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S132.c (252468 bytes, sha256 f3400af8e924bc7743d28f43b45f02be1bc84e25de00ac99d2bfc8bab19a4fbf, 8976 lines), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/SrcKernelVolumes.md; executed=curl of https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/volumes.c (4x HTTP 429 then HTTP 200), sha256sum, wc -l, stat, od -c, grep -n, grep -qF, awk, curl of https://github.com/torvalds/linux/tree/v7.2/fs/btrfs (HTTP 200)
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
