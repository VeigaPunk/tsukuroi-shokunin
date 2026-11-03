2026-11-03T21:54:15Z
# S1Scout — C1 Source Re-verification Receipt (Round 67 w1)

- Seat: `S1Scout` (scout)
- Task: Independent re-fetch and line verification of btrfs-progs v7.3 facts for Claim C1 (S284 / S285)
- Host: Arch Linux, fleet root `/home/vgpnk/Projects/shokunin`, lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
- Scratch: `/fast/scratch/hyaku/tsukuroi-r67/S1Scout/`

---

## 1. Scratch Directory Initialization

- Command: `mkdir -p /fast/scratch/hyaku/tsukuroi-r67/S1Scout`
- Return code: 0

---

## 2. Re-fetch and SHA-256 Verification of Upstream v7.3 Sources

- Fetch `scrub.c`:
  - Command: `curl -sSf -o /fast/scratch/hyaku/tsukuroi-r67/S1Scout/scrub.c https://raw.githubusercontent.com/kdave/btrfs-progs/v7.3/cmds/scrub.c`
  - Return code: 0
- Fetch `CHANGES`:
  - Command: `curl -sSf -o /fast/scratch/hyaku/tsukuroi-r67/S1Scout/CHANGES https://raw.githubusercontent.com/kdave/btrfs-progs/v7.3/CHANGES`
  - Return code: 0
- Checksum computation:
  - Command: `sha256sum /fast/scratch/hyaku/tsukuroi-r67/S1Scout/scrub.c /fast/scratch/hyaku/tsukuroi-r67/S1Scout/CHANGES`
  - Return code: 0
  - Output:
    ```text
    b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528  /fast/scratch/hyaku/tsukuroi-r67/S1Scout/scrub.c
    5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249  /fast/scratch/hyaku/tsukuroi-r67/S1Scout/CHANGES
    ```
- Pinned reference: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-67/before/src/SHA256SUMS`
  - Command: `cat /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-67/before/src/SHA256SUMS`
  - Return code: 0
  - Output:
    ```text
    b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528  scrub.c
    5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249  CHANGES
    ```
- Result:
  - `scrub.c`: MATCH
  - `CHANGES`: MATCH

---

## 3. Remote Tag Verification (git ls-remote)

- Query remote tag:
  - Command: `git ls-remote https://github.com/kdave/btrfs-progs refs/tags/v7.3 'refs/tags/v7.3^{}'`
  - Return code: 0
  - Output:
    ```text
    b5cb02e0fdd099f44b00a41b225c1a5daf7539ef	refs/tags/v7.3
    afdc3a65e33f4d42f768ad50dca20c32e5ee1496	refs/tags/v7.3^{}
    ```
- Pinned reference: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-67/before/src/TAG.txt`
  - Command: `cat /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-67/before/src/TAG.txt`
  - Return code: 0
  - Output:
    ```text
    b5cb02e0fdd099f44b00a41b225c1a5daf7539ef	refs/tags/v7.3
    afdc3a65e33f4d42f768ad50dca20c32e5ee1496	refs/tags/v7.3^{}
    ```
- Result:
  - Tag object: `b5cb02e0fdd099f44b00a41b225c1a5daf7539ef` (MATCH)
  - Peeled commit: `afdc3a65e33f4d42f768ad50dca20c32e5ee1496` (MATCH)

---

## 4. Upstream v7.3 `cmds/scrub.c` Inspection

- Search for revert comment:
  - Command: `grep -n 'Revert to the older scrub limits' /fast/scratch/hyaku/tsukuroi-r67/S1Scout/scrub.c`
  - Return code: 0
  - Output:
    ```text
    1640:	/* Revert to the older scrub limits. */
    ```
- Search for limit writer calls:
  - Command: `grep -n 'write_scrub_device_limit' /fast/scratch/hyaku/tsukuroi-r67/S1Scout/scrub.c`
  - Return code: 0
  - Output:
    ```text
    1222:static u64 write_scrub_device_limit(int fd, u64 devid, u64 limit)
    1414:		ret = write_scrub_device_limit(fdmnt, devid, throughput_limit);
    1642:		ret = write_scrub_device_limit(fdmnt, di_args[i].devid, sp[i].old_limit);
    2127:		ret = write_scrub_device_limit(fd, opt_devid, opt_limit);
    2158:			ret = write_scrub_device_limit(fd, devid, opt_limit);
    ```
- Enclosing function identification:
  - Nearest preceding line starting with a type or static at column 0 above line 1640:
  - Command: `sed -n '1,1640p' /fast/scratch/hyaku/tsukuroi-r67/S1Scout/scrub.c | grep -nE '^[a-zA-Z_][a-zA-Z0-9_* ]+[ ]+[a-zA-Z0-9_*]+\(' | tail -n 1`
  - Return code: 0
  - Output:
    ```text
    1233:static int scrub_start(const struct cmd_struct *cmd, int argc, char **argv,
    ```
  - Enclosing function name: `scrub_start`
- Exact line range of post-loop revert block: `1640-1649`
  - Verbatim lines 1640-1649:
    ```c
	/* Revert to the older scrub limits. */
	for (i = 0; i < fi_args.num_devices; ++i) {
		ret = write_scrub_device_limit(fdmnt, di_args[i].devid, sp[i].old_limit);
		if (ret < 0) {
			errno = -ret;
			warning("failed to reset scrub throughput limit on devid %llu: %m",
				di_args[i].devid);
		}
	}

    ```

---

## 5. Frozen v7.1 `cmds/scrub.c` Inspection

- Path: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c`
- Checksum verification:
  - Command: `sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c`
  - Return code: 0
  - Output:
    ```text
    48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c
    ```
  - Result: MATCH (equals expected `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`)
- Search for in-loop revert comment:
  - Command: `grep -n 'Revert to the older scrub limit' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c`
  - Return code: 0
  - Output:
    ```text
    1597:		/* Revert to the older scrub limit. */
    ```
- Loop header containing the in-loop revert:
  - Line 1596: `	for (i = 0; i < fi_args.num_devices; ++i) {`
- Verbatim block lines 1596-1604:
  - Command: `sed -n '1596,1604p' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c`
  - Return code: 0
  - Output:
    ```c
	for (i = 0; i < fi_args.num_devices; ++i) {
		/* Revert to the older scrub limit. */
		ret = write_scrub_device_limit(fdmnt, di_args[i].devid, sp[i].old_limit);
		if (ret < 0) {
			errno = -ret;
			warning("failed to reset scrub throughput limit on devid %llu: %m",
				di_args[i].devid);
		}

    ```
  - True line numbers: `1596-1604` (in-loop revert at lines 1597-1603 inside loop header line 1596).

---

## 6. Hunk Analysis: `diff -u` (v7.1 vs v7.3 `scrub.c`)

- Command: `diff -u /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c /fast/scratch/hyaku/tsukuroi-r67/S1Scout/scrub.c`
- Return code: 1 (files differ)
- Hunk headers listed via `diff -u ... | grep '^@@'`:
  1. `@@ -568,7 +568,7 @@`
  2. `@@ -1372,7 +1372,7 @@`
  3. `@@ -1594,14 +1594,6 @@`
  4. `@@ -1645,6 +1637,16 @@`
- Detailed hunk assessment:
  - Hunk 1 (`@@ -568,7 +568,7 @@`):
    - Change: Changes warning message formatting in `_SCRUB_INVALID` macro from `"invalid data on line %d pos "` to `"invalid data on line %d position "`.
    - Behaviour impact: Non-behaviour-changing (diagnostic warning string wording / typo fix).
  - Hunk 2 (`@@ -1372,7 +1372,7 @@`):
    - Change: Fixes punctuation in comment from `ie.` to `i.e.`.
    - Behaviour impact: Non-behaviour-changing (comment-only typo fix).
  - Hunk 3 (`@@ -1594,14 +1594,6 @@`):
    - Change: Removes premature per-device revert block (`ret = write_scrub_device_limit(...)`) from inside the `pthread_join` loop in `scrub_start`.
    - Behaviour impact: Behaviour-changing (devices are no longer reset to previous limit prior to waiting on thread completion).
  - Hunk 4 (`@@ -1645,6 +1637,16 @@`):
    - Change: Adds dedicated post-loop revert block (`for (i = 0; i < fi_args.num_devices; ++i) { ret = write_scrub_device_limit(...); ... }`) after all device threads finish and error counts are calculated.
    - Behaviour impact: Behaviour-changing (ensures limit is restored only after all devices finish).
- Total hunks: 4
- Count of behaviour-changing hunks: 2 (Hunk 3 and Hunk 4)

---

## 7. Inspection of Upstream v7.3 `CHANGES`

- Search for scrub limit bullet:
  - Command: `grep -n 'set to the original limit only after all devices finish' /fast/scratch/hyaku/tsukuroi-r67/S1Scout/CHANGES`
  - Return code: 0
  - Output:
    ```text
    20:   * scrub limit: set to the original limit only after all devices finish
    ```
  - Matched line: line 20
- Enclosing release header:
  - Command: `sed -n '1,20p' /fast/scratch/hyaku/tsukuroi-r67/S1Scout/CHANGES | grep -n '^btrfs-progs-' | tail -n 1`
  - Return code: 0
  - Output:
    ```text
    1:btrfs-progs-7.3 (2026-10-23)
    ```
  - Nearest release header above: Line 1 (`btrfs-progs-7.3 (2026-10-23)`)

---

## 8. S237 Row Confirmation in `corpus/SOURCES.md`

- Search for S237 row:
  - Command: `grep -n '^| S237 ' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`
  - Return code: 0
  - Output:
    ```text
    246:| S237 | btrfs-progs v7.1 cmds/scrub.c — https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c | code | A | How the btrfs CLI writes, names, locks and reads the scrub status record, and when it disables recording | tag v7.1 (peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b), cmds/scrub.c lines 67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220, 1330-1340, 1498-1512, 1925-1945; raw bytes sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801 | The status record is a userspace file the scrub start process writes and the status command reads; its format, its write discipline and the cases that leave no record | mined | 2026-10-26 | on-release | corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md |
    ```
- Extract sha256 from row:
  - Command: `grep -n '^| S237 ' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md | grep -o 'sha256 [0-9a-f]*'`
  - Return code: 0
  - Output:
    ```text
    sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801
    ```
- Comparison to frozen v7.1 `scrub.c` sha256 (`48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`):
  - Result: MATCH

---

## 9. Verification Summary Table

| fact | command | observed | MATCH/MISMATCH |
|---|---|---|---|
| v7.3 `scrub.c` sha256 | `sha256sum $S/scrub.c` | `b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528` | MATCH |
| v7.3 `CHANGES` sha256 | `sha256sum $S/CHANGES` | `5046bac1def81247a02d7442807a6d495de2caafbc1a7194637ef03ea958a249` | MATCH |
| v7.3 git tag object | `git ls-remote ... refs/tags/v7.3` | `b5cb02e0fdd099f44b00a41b225c1a5daf7539ef` | MATCH |
| v7.3 git tag peeled commit | `git ls-remote ... 'refs/tags/v7.3^{}'` | `afdc3a65e33f4d42f768ad50dca20c32e5ee1496` | MATCH |
| v7.3 scrub.c revert comment line | `grep -n 'Revert to the older scrub limits' $S/scrub.c` | Line 1640 | MATCH |
| v7.3 scrub.c enclosing function | `sed -n '1,1640p' ... \| grep -nE '^[a-zA-Z_]...'` | `static int scrub_start(...)` at line 1233 | MATCH |
| v7.3 scrub.c post-loop revert range | `awk 'NR>=1640 && NR<=1649' $S/scrub.c` | Lines 1640-1649 | MATCH |
| v7.1 frozen scrub.c sha256 | `sha256sum .../frozen/.../scrub.c` | `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` | MATCH |
| v7.1 scrub.c in-loop revert range | `awk 'NR>=1596 && NR<=1604' .../frozen/.../scrub.c` | Lines 1596-1604 (header at 1596, comment at 1597) | MATCH |
| `diff -u` hunk count | `diff -u ... \| grep -c '^@@'` | 4 total hunks (2 behaviour-changing) | MATCH |
| v7.3 `CHANGES` bullet line | `grep -n 'set to the original limit...' $S/CHANGES` | Line 20 | MATCH |
| v7.3 `CHANGES` release header | `sed -n '1,20p' ... \| grep -n '^btrfs-progs-'` | Line 1: `btrfs-progs-7.3 (2026-10-23)` | MATCH |
| `corpus/SOURCES.md` S237 sha256 | `grep -n '^\| S237 ' ... \| grep -o 'sha256 [0-9a-f]*'` | `sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` | MATCH |
