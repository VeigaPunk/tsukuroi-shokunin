2026-11-03T22:35:41Z
# S1Scout — round-68 w1 scoped findings (C1 Linux v7.3 fact verification)

Full receipt with verbatim commands/outputs: `.ufo/waves/round-68/drafts/c1/S1Scout-verify.md`

- Step 2 (re-fetch & sha256sum): `curl -sSf` from `raw.githubusercontent.com/torvalds/linux/` yielded:
  - `v7.3 cgroup-v2.rst`: `2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68` (MATCH `.ufo/waves/round-68/before/src/SHA256SUMS`)
  - `v7.2 cgroup-v2.rst`: `a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad` (MATCH)
  - `v7.3 fs/btrfs/sysfs.c`: `098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377` (MATCH)
  - `v7.2 fs/btrfs/sysfs.c`: `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` (MATCH)
- Step 3 (cgroup-v2.rst diff & hunks): `diff -u` has 16 hunks total. Exactly 1 hunk touches memory controller sections:
  - Hunk 7 (`@@ -1909,7 +1936,7 @@`) touches `memory.pressure` under `Memory Interface Files` / `Memory`, updating it from "A read-only nested-keyed file." to "A read-write nested-keyed file."
  - The remaining 15 hunks touch CPU (hunks 1-6), IO (hunks 8-10), Cpuset (hunk 11), RDMA (hunks 12-14), DMEM (hunk 15), and Misc (hunk 16).
- Step 4 (S138 anchor quotes in cgroup-v2.rst):
  - "Note that all fields in this file are hierarchical": v7.2 line 1474, v7.3 line 1501 (`grep -cF` = 1 in both, byte-identical).
  - "killed by any kind of OOM killer": v7.2 line 1508, v7.3 line 1535 (`grep -cF` = 1 in both, byte-identical).
  - "Similar to memory.events but the fields in the file are local": v7.2 line 1518, v7.3 line 1545 (`grep -cF` = 1 in both, byte-identical).
  - Net line shift across all three anchors is uniform +27 lines, caused by net 21 lines in hunk 3 and net 2 lines each in hunks 4, 5, 6.
- Step 5 (sysfs.c v7.2 vs v7.3):
  - Single hunk (`@@ -1336,7 +1336,7 @@`) changing line 1339 from `/* Set perms to 0, disable /sys/module/btrfs/parameter/read_policy interface. */` to `.../parameters/...`. Comment-only typo fix.
  - S158 anchor ranges (`sed -n` 37,40p; 68,78p; 672,688p) are 100% byte-identical between v7.2 and v7.3 (`cmp` rc 0 on all 3 ranges, MATCH).
- Step 6 (mm/oom_kill.c and psi.rst):
  - `mm/oom_kill.c`: `cmp` rc 0 between v7.2 and v7.3, sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` (UNCHANGED).
  - `psi.rst`: `cmp` rc 0 between v7.2 and v7.3, sha256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` (UNCHANGED).
- VERDICT: SHA_ALL=MATCH, S138_HUNKS=16, S138_MEMORY_HUNKS=1, SYSFS_HUNKS=1, S138_ANCHORS_V73=1501,1535,1545.
