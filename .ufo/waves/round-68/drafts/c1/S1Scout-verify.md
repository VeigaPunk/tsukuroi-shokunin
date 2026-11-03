2026-11-03T22:35:41Z
# S1Scout — C1 Source Re-verification Receipt (Round 68 w1)

- Seat: `S1Scout` (scout)
- Task: Independent re-fetch and fact verification of Linux v7.3 sources for Claim C1 (S138, S149, S158, S182, S185, S286, S287)
- Host: Arch Linux (`linux 7.2.11.arch1-1`), fleet root `/home/vgpnk/Projects/shokunin`, lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
- Scratch: `/fast/scratch/hyaku/tsukuroi-r68/S1Scout/`

---

## 1. Fact Verification Table

| fact | command | observed | MATCH/MISMATCH |
|---|---|---|---|
| v7.3 cgroup-v2.rst sha256 | `curl -sSf -o v73-cgroup-v2.rst https://raw.githubusercontent.com/torvalds/linux/v7.3/Documentation/admin-guide/cgroup-v2.rst && sha256sum v73-cgroup-v2.rst` | `2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68` (rc 0) | MATCH |
| v7.2 cgroup-v2.rst sha256 | `curl -sSf -o v72-cgroup-v2.rst https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst && sha256sum v72-cgroup-v2.rst` | `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` (rc 0) | MATCH |
| v7.3 fs/btrfs/sysfs.c sha256 | `curl -sSf -o v73-sysfs.c https://raw.githubusercontent.com/torvalds/linux/v7.3/fs/btrfs/sysfs.c && sha256sum v73-sysfs.c` | `098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377` (rc 0) | MATCH |
| v7.2 fs/btrfs/sysfs.c sha256 | `curl -sSf -o v72-sysfs.c https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c && sha256sum v72-sysfs.c` | `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` (rc 0) | MATCH |
| mm/oom_kill.c byte identity (v7.2 vs v7.3) | `curl -sSf -o v72-oom_kill.c https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c && curl -sSf -o v73-oom_kill.c https://raw.githubusercontent.com/torvalds/linux/v7.3/mm/oom_kill.c && cmp v72-oom_kill.c v73-oom_kill.c` | `rc 0`, identical sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` | MATCH |
| psi.rst byte identity (v7.2 vs v7.3) | `curl -sSf -o v72-psi.rst https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst && curl -sSf -o v73-psi.rst https://raw.githubusercontent.com/torvalds/linux/v7.3/Documentation/accounting/psi.rst && cmp v72-psi.rst v73-psi.rst` | `rc 0`, identical sha256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` | MATCH |
| S138 anchor quote 1: "Note that all fields in this file are hierarchical" | `grep -n -F "Note that all fields in this file are hierarchical" v72-cgroup-v2.rst v73-cgroup-v2.rst` | v7.2 line 1474; v7.3 line 1501; `grep -cF` = 1 in both files (byte-identical) | MATCH |
| S138 anchor quote 2: "killed by any kind of OOM killer" | `grep -n -F "killed by any kind of OOM killer" v72-cgroup-v2.rst v73-cgroup-v2.rst` | v7.2 line 1508; v7.3 line 1535; `grep -cF` = 1 in both files (byte-identical) | MATCH |
| S138 anchor quote 3: "Similar to memory.events but the fields in the file are local" | `grep -n -F "Similar to memory.events but the fields in the file are local" v72-cgroup-v2.rst v73-cgroup-v2.rst` | v7.2 line 1518; v7.3 line 1545; `grep -cF` = 1 in both files (byte-identical) | MATCH |
| sysfs.c diff hunk count and comment-only status | `diff -u v72-sysfs.c v73-sysfs.c` | Exactly 1 hunk at line 1336 (`@@ -1336,7 +1336,7 @@`); changed line 1339 in both v7.2 and v7.3 (`parameter` -> `parameters`); comment-only typo fix | MATCH |
| S158 sysfs.c anchor range 37,40 | `cmp <(sed -n 37,40p v72-sysfs.c) <(sed -n 37,40p v73-sysfs.c)` | `rc 0`, byte-identical (attribute doc comments) | MATCH |
| S158 sysfs.c anchor range 68,78 | `cmp <(sed -n 68,78p v72-sysfs.c) <(sed -n 68,78p v73-sysfs.c)` | `rc 0`, byte-identical (`BTRFS_ATTR_*` macros) | MATCH |
| S158 sysfs.c anchor range 672,688 | `cmp <(sed -n 672,688p v72-sysfs.c) <(sed -n 672,688p v73-sysfs.c)` | `rc 0`, byte-identical (`global_rsv_size_show` & `global_rsv_reserved_show`) | MATCH |
| cgroup-v2.rst total diff hunks | `diff -u v72-cgroup-v2.rst v73-cgroup-v2.rst \| grep -c "^@@"` | 16 hunks total | MATCH |
| cgroup-v2.rst memory-section hunks | Inspection of diff against section structure | Exactly 1 hunk (Hunk 7: `@@ -1909,7 +1936,7 @@` touching `memory.pressure`) | MATCH |

---

## 2. cgroup-v2.rst Hunk List and Controller Section Attribution

Total diff hunks: 16.
Memory-section hunks: 1 (Hunk 7).

### Hunk 1
- Hunk header: `@@ -1130,9 +1130,9 @@`
- Nearest preceding section heading: `CPU Interface Files` (line 1125, level `~~~`), under `CPU` (line 1094, level `---`)
- Nearest preceding entry: Overview bullet list of scheduling policies under `CPU Interface Files`
- Controller: CPU
- Touches memory controller: NO
- Change description: Updates bullet items for processes under BPF scheduler with corresponding `cgroup_set_*` callback (replacing `cgroup_set_weight`).

### Hunk 2
- Hunk header: `@@ -1145,7 +1145,7 @@`
- Nearest preceding section heading: `CPU Interface Files` (line 1125, level `~~~`), under `CPU` (line 1094, level `---`)
- Nearest preceding entry: `  cpu.stat` (line 1143)
- Controller: CPU
- Touches memory controller: NO
- Change description: Clarifies that the three stats account for all processes in the cgroup "(including those in descendant cgroups)".

### Hunk 3
- Hunk header: `@@ -1160,6 +1160,27 @@`
- Nearest preceding section heading: `CPU Interface Files` (line 1125, level `~~~`), under `CPU` (line 1094, level `---`)
- Nearest preceding entry: `  cpu.stat` (line 1143)
- Controller: CPU
- Touches memory controller: NO
- Change description: Documents that the five CFS bandwidth stats are non-hierarchical, and documents new interface file `  cpu.stat.local` reporting `throttled_usec`.

### Hunk 4
- Hunk header: `@@ -1202,7 +1223,9 @@`
- Nearest preceding section heading: `CPU Interface Files` (line 1125, level `~~~`), under `CPU` (line 1094, level `---`)
- Nearest preceding entry: `  cpu.max` (line 1193)
- Controller: CPU
- Touches memory controller: NO
- Change description: Notes that file affects processes under fair-class scheduler and BPF scheduler with `cgroup_set_bandwidth` callback.

### Hunk 5
- Hunk header: `@@ -1210,7 +1233,9 @@`
- Nearest preceding section heading: `CPU Interface Files` (line 1125, level `~~~`), under `CPU` (line 1094, level `---`)
- Nearest preceding entry: `  cpu.max.burst` (line 1207)
- Controller: CPU
- Touches memory controller: NO
- Change description: Notes that file affects processes under fair-class scheduler and BPF scheduler with `cgroup_set_bandwidth` callback.

### Hunk 6
- Hunk header: `@@ -1262,7 +1287,9 @@`
- Nearest preceding section heading: `CPU Interface Files` (line 1125, level `~~~`), under `CPU` (line 1094, level `---`)
- Nearest preceding entry: `  cpu.idle` (line 1255)
- Controller: CPU
- Touches memory controller: NO
- Change description: Notes that file affects processes under fair-class scheduler and BPF scheduler with `cgroup_set_idle` callback.

### Hunk 7
- Hunk header: `@@ -1909,7 +1936,7 @@`
- Nearest preceding section heading: `Memory Interface Files` (line 1290, level `~~~`), under `Memory` (line 1267, level `---`)
- Nearest preceding entry: `  memory.pressure` (line 1911)
- Controller: Memory
- Touches memory controller: YES
- Change description: Updates file type description of `memory.pressure` from "A read-only nested-keyed file." to "A read-write nested-keyed file." (supporting write triggers).

### Hunk 8
- Hunk header: `@@ -1984,9 +2011,13 @@`
- Nearest preceding section heading: `IO` (line 1982, level `---`)
- Nearest preceding entry: Overview paragraph under `IO`
- Controller: IO
- Touches memory controller: NO
- Change description: Replaces legacy cfq-iosched distribution description with modern blk-throttle, iocost (`CONFIG_BLK_CGROUP_IOCOST`), BFQ, iolatency, and ioprio descriptions.

### Hunk 9
- Hunk header: `@@ -2169,7 +2200,7 @@`
- Nearest preceding section heading: `IO Interface Files` (line 1992, level `~~~`), under `IO` (line 1982, level `---`)
- Nearest preceding entry: `  io.pressure` (line 2171)
- Controller: IO
- Touches memory controller: NO
- Change description: Updates file type description of `io.pressure` from "A read-only nested-keyed file." to "A read-write nested-keyed file."

### Hunk 10
- Hunk header: `@@ -2284,9 +2315,9 @@`
- Nearest preceding section heading: `How IO Latency Throttling Works` (line 2271, level `~~~`), under `IO Latency` (line 2238, level `~~~`), under `IO` (line 1982, level `---`)
- Nearest preceding entry: Throttling explanation paragraph under `How IO Latency Throttling Works`
- Controller: IO
- Touches memory controller: NO
- Change description: Updates field name in description from `delay` (microseconds) to `delay_nsec` (nanoseconds).

### Hunk 11
- Hunk header: `@@ -2552,6 +2583,13 @@`
- Nearest preceding section heading: `Cpuset Interface Files` (line 2479, level `~~~`), under `Cpuset` (line 2464, level `---`)
- Nearest preceding entry: `  cpuset.mems` (line 2521)
- Controller: Cpuset
- Touches memory controller: NO
- Change description: Adds paragraph specifying multithreaded threadgroup leader memory ownership rules for `cpuset.mems`.

### Hunk 12
- Hunk header: `@@ -2777,6 +2815,11 @@`
- Nearest preceding section heading: `RDMA` (line 2774, level `---`)
- Nearest preceding entry: Overview paragraph under `RDMA`
- Controller: RDMA
- Touches memory controller: NO
- Change description: Adds documentation of RDMA device naming and system-wide device index `index=N` for duplicate names across network namespaces.

### Hunk 13
- Hunk header: `@@ -2785,7 +2828,11 @@`
- Nearest preceding section heading: `RDMA Interface Files` (line 2780, level `~~~`), under `RDMA` (line 2774, level `---`)
- Nearest preceding entry: `  rdma.max` (line 2783)
- Controller: RDMA
- Touches memory controller: NO
- Change description: Clarifies write syntax for `rdma.max` including optional/required `index=N` parameter and `-ENOTUNIQ` failure mode.

### Hunk 14
- Hunk header: `@@ -2801,6 +2848,10 @@`
- Nearest preceding section heading: `RDMA Interface Files` (line 2780, level `~~~`), under `RDMA` (line 2774, level `---`)
- Nearest preceding entry: `  rdma.max` (line 2783)
- Controller: RDMA
- Touches memory controller: NO
- Change description: Adds example command for selecting device by index: `echo "rxe0 index=5 hca_handle=2" > rdma.max`.

### Hunk 15
- Hunk header: `@@ -2886,6 +2937,12 @@`
- Nearest preceding section heading: `DMEM Interface Files` (line 2873, level `~~~`), under `DMEM` (line 2866, level `---`)
- Nearest preceding entry: Description under `DMEM Interface Files` right before `  dmem.capacity` (line 2894)
- Controller: DMEM
- Touches memory controller: NO
- Change description: Adds documentation for new interface file `  dmem.peak`.

### Hunk 16
- Hunk header: `@@ -3013,7 +3070,7 @@`
- Nearest preceding section heading: `Misc Interface Files` (line 2959, level `~~~`), under `Misc` (line 2942, level `---`)
- Nearest preceding entry: `  misc.events` (line 3010)
- Controller: Misc
- Touches memory controller: NO
- Change description: Replaces generic field name `max` with `<res>.max`.

---

## 3. S138 Anchor Quotes Verification

Verbatim search results for both tags:
1. `"Note that all fields in this file are hierarchical"`:
   - v7.2 line: 1474 (`\tNote that all fields in this file are hierarchical and the`)
   - v7.3 line: 1501 (`\tNote that all fields in this file are hierarchical and the`)
   - `grep -cF`: 1 in v7.2, 1 in v7.3
   - Byte-identical: YES
2. `"killed by any kind of OOM killer"`:
   - v7.2 line: 1508 (`\t\tkilled by any kind of OOM killer.`)
   - v7.3 line: 1535 (`\t\tkilled by any kind of OOM killer.`)
   - `grep -cF`: 1 in v7.2, 1 in v7.3
   - Byte-identical: YES
3. `"Similar to memory.events but the fields in the file are local"`:
   - v7.2 line: 1518 (`\tSimilar to memory.events but the fields in the file are local`)
   - v7.3 line: 1545 (`\tSimilar to memory.events but the fields in the file are local`)
   - `grep -cF`: 1 in v7.2, 1 in v7.3
   - Byte-identical: YES

Net line shift from v7.2 to v7.3 across all three anchors is exactly +27 lines:
- Hunk 3 added net 21 lines (`-1160,6 +1160,27`)
- Hunk 4 added net 2 lines (`-1202,7 +1223,9`)
- Hunk 5 added net 2 lines (`-1210,7 +1233,9`)
- Hunk 6 added net 2 lines (`-1262,7 +1287,9`)
- Total net shift before line 1474: 21 + 2 + 2 + 2 = +27 lines.
- 1474 + 27 = 1501; 1508 + 27 = 1535; 1518 + 27 = 1545.

---

## 4. fs/btrfs/sysfs.c Verification

`diff -u v72-sysfs.c v73-sysfs.c`:
- Hunk count: 1 (`@@ -1336,7 +1336,7 @@`)
- Changed line: 1339 in both v7.2 and v7.3
- Changed content:
  ```diff
  -/* Set perms to 0, disable /sys/module/btrfs/parameter/read_policy interface. */
  +/* Set perms to 0, disable /sys/module/btrfs/parameters/read_policy interface. */
  ```
- Comment-only: YES (fixes typo in comment, zero code change, zero line count delta).

S158 registered anchor ranges comparison (`cmp` between extracted ranges):
- `sed -n 37,40p`: rc 0 (MATCH)
- `sed -n 68,78p`: rc 0 (MATCH)
- `sed -n 672,688p`: rc 0 (MATCH)

---

## 5. mm/oom_kill.c and psi.rst Byte Identity

- `mm/oom_kill.c`: `cmp` between v7.2 and v7.3 returns rc 0. SHA-256 for both: `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e`. Byte-identical (UNCHANGED).
- `Documentation/accounting/psi.rst`: `cmp` between v7.2 and v7.3 returns rc 0. SHA-256 for both: `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`. Byte-identical (UNCHANGED).

---

## 6. Verdict

- Upstream SHA-256 digests: ALL MATCH
- Registered anchor quotes and ranges: ALL MATCH
- Overall verdict: MATCH
