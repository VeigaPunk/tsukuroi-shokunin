2026-11-03T21:55:00Z
# S1Scout — round-67 w1 scoped findings (C1 source re-verification)

Full receipt with verbatim commands/outputs: .ufo/waves/round-67/drafts/S1Scout-verify.md

- Step 2 (re-fetch & sha256sum): `curl -sSf` from `raw.githubusercontent.com/kdave/btrfs-progs/v7.3/` yielded `scrub.c` (sha256 `b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528`) and `CHANGES` (sha256 `5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249`). Both sha256 digests MATCH `.ufo/waves/round-67/before/src/SHA256SUMS` exactly (rc 0).
- Step 3 (remote tag): `git ls-remote https://github.com/kdave/btrfs-progs refs/tags/v7.3 'refs/tags/v7.3^{}'` returned tag `b5cb02e0fdd099f44b00a41b225c1a5daf7539ef` and peeled commit `afdc3a65e33f4d42f768ad50dca20c32e5ee1496`, matching `.ufo/waves/round-67/before/src/TAG.txt` exactly (rc 0).
- Step 4 (v7.3 scrub.c locus): `Revert to the older scrub limits` is at line 1640. `write_scrub_device_limit` calls occur at lines 1222 (definition), 1414, 1642, 2127, 2158. The enclosing function is `scrub_start` (`static int scrub_start(...)` at line 1233). The post-loop revert block covers lines 1640–1649 (loop lines 1641–1648).
- Step 5 (v7.1 frozen scrub.c locus): sha256 is `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` (MATCH). The in-loop revert (`Revert to the older scrub limit.`) is at line 1597 inside loop header line 1596 (`for (i = 0; i < fi_args.num_devices; ++i)`), covering lines 1596–1604 verbatim.
- Step 6 (diff hunk analysis): `diff -u` between v7.1 and v7.3 `scrub.c` has 4 hunks total:
  1. `@@ -568,7 +568,7 @@`: Warning message formatting in `_SCRUB_INVALID` (`pos` -> `position`). Non-behaviour-changing (diagnostic string wording).
  2. `@@ -1372,7 +1372,7 @@`: Comment punctuation (`ie.` -> `i.e.`). Non-behaviour-changing (comment-only).
  3. `@@ -1594,14 +1594,6 @@`: Removal of in-loop revert inside device join loop. Behaviour-changing.
  4. `@@ -1645,6 +1637,16 @@`: Addition of dedicated post-loop revert after all device threads complete. Behaviour-changing.
  Count of behaviour-changing hunks = 2.
- Step 7 (v7.3 CHANGES locus): Bullet `* scrub limit: set to the original limit only after all devices finish` is at line 20 under release header `btrfs-progs-7.3 (2026-10-23)` at line 1.
- Step 8 (SOURCES S237 confirmation): Row S237 in `corpus/SOURCES.md` (line 246) specifies sha256 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`, matching frozen v7.1 `scrub.c` exactly (MATCH).
- VERDICT = ALL_MATCH (100% agreement between upstream v7.3 sources, frozen v7.1 sources, before-receipts, and C1 claim loci).
