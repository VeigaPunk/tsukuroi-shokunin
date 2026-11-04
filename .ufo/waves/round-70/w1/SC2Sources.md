# SC2Sources — C1 registry rows S290–S293 and round-69 rejected rows S294–S296

scribe seat, tsukuroi lane round 70 (hyaku run 15), wave w1. Lane base for the registry:
`1710bd74aec840c71d5e4ffbdc0ca54198e953fa` (declaration; 289 rows, last id `S289`). The lane tree
`corpus/SOURCES.md` is **not** edited here — this file is the draft the L1 appends.

Sources read for this draft (all committed, read-only):

- `corpus/SOURCES.md` at `1710bd74` (registry schema and tail, rows `S288`/`S289`, `S140`)
- `CORPUS.md` § "SOURCES.md — where a shokunin learns" (contract v1: 11 cells, append-only,
  rule 1 Gate record, `REJECTED: <reason>; flip: <what would change the verdict>`)
- `corpus/QUALITY.md` rule 86 (own-work capture never verifies a rule row by itself)
- `corpus/lessons/round-69-verifier-spotcheck.md` §3 (the three refusals) and §6 D1/D5
- `.ufo/waves/round-70/before/src/{xfs.rst,xfs_stats.c,xfs_sysfs.c,health.c}` + `SHA256SUMS` +
  `SOURCES.json` (digests re-computed below, all four match)
- `.ufo/waves/round-69/before/src/{tk-v7211.rst,vm-v7211.h}` (D1 erratum locators)
- `SCORECARD.md` "Round 70 — declaration" (C1 statement list, D1–D7 routing)

Snapshot digests re-computed 2026-11-03 in `.ufo/waves/round-70/before/src`:

```
53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c  xfs.rst
4b6a9b6c239a92abb56838798a2d5657a53ba5a7fb1bee6aa9c12b89f7c9e452  xfs_stats.c
1cbcffa12346ebe3ebb29b466196786ea07450d67e4e4d1cbd675603784a5805  xfs_sysfs.c
84fdd0bec52a7f0efc592c588a6d001c2b8ba389a7e33de7daf5d13a34215950  health.c
```

Line counts: `xfs.rst` 563, `xfs_stats.c` 179, `xfs_sysfs.c` 898, `health.c` 584.

## 1. Draft registry rows (append after S289)

Schema: 11 cells (`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck |
used-by`), no pipe inside a cell. Rows S290–S293 are `mined`, tier A, used by the C1 note; S294–S296
are the three round-69 refusals (D5) as `rejected` rows with reason and flip.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S290 | Linux v7.2.11 Documentation/admin-guide/xfs.rst — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/xfs.rst?h=v7.2.11 | docs | A | The documented XFS sysctl `fs.xfs.stats_clear` and the documented per-filesystem error-configuration sysfs hierarchy, at the host kernel release tag v7.2.11 in the stable tree | tag v7.2.11, Documentation/admin-guide/xfs.rst lines 275-282 (sysctls heading and fs.xfs.stats_clear at 280-282) and 376-496 (Error handling: the /sys/fs/xfs/<dev>/error/<class>/<error>/ hierarchy at 408-411 and 454-461, global options at 428-431 with fail_at_unmount at 433-452, max_retries at 463-476 and retry_timeout_seconds at 478-490); raw bytes sha256 53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c; snapshot .ufo/waves/round-70/before/src/xfs.rst (563 lines, 22719 bytes) | writing 1 to fs.xfs.stats_clear clears the accumulated statistics reported in /proc/fs/xfs/stat and the sysctl immediately resets to 0, and the same page locates error-handler tuning under /sys/fs/xfs/<dev>/error/<class>/<error>/ | mined | 2026-11-03 | on-release | corpus/knowledge/xfs-storage-plane-r70.md |
| S291 | Linux v7.2.11 fs/xfs/xfs_stats.c — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/xfs/xfs_stats.c?h=v7.2.11 | code | A | The text the XFS stats file emits and the clear path behind it, at the host kernel release tag v7.2.11: per-CPU counter summation, the named counter-group table, one output line per group, the four precision counters, the stateful inode counters kept across a clear, and the /proc/fs/xfs/stat symlink target | tag v7.2.11, fs/xfs/xfs_stats.c lines 10-17 (counter_val sums a counter over every possible CPU), 29-64 (the xstats group table), 66-76 (one line per named group, counters appended inside the group loop), 77-96 (the xpc, defer_relog, debug and gc precision counters), 101-119 (xfs_stats_clearall zeroes each per-CPU struct and restores xs_inodes_active and xs_inodes_meta), 151-172 (proc_symlink fs/xfs/stat to /sys/fs/xfs/stats/stats); raw bytes sha256 4b6a9b6c239a92abb56838798a2d5657a53ba5a7fb1bee6aa9c12b89f7c9e452; snapshot .ufo/waves/round-70/before/src/xfs_stats.c (179 lines, 5319 bytes) | each group name starts a line followed by its counters summed over every possible CPU, four precision counters print after the group loop, and a clear zeroes the per-CPU structures while restoring the two stateful inode counters | mined | 2026-11-03 | on-release | corpus/knowledge/xfs-storage-plane-r70.md |
| S292 | Linux v7.2.11 fs/xfs/xfs_sysfs.c — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/xfs/xfs_sysfs.c?h=v7.2.11 | code | A | The per-filesystem sysfs surface XFS creates under /sys/fs/xfs/<dev>, at the host kernel release tag v7.2.11: the stats kobject and its stats and stats_clear attributes, the log kobject's head and tail LSN and grant-head byte files, and the error tree's fail_at_unmount file plus the metadata class handlers | tag v7.2.11, fs/xfs/xfs_sysfs.c lines 33-40 (RW, RO and WO attribute macros), 349-357 (stats_show calls xfs_stats_format), 361-380 (stats_clear_store accepts only 1, EINVAL otherwise, and registers XFS_SYSFS_ATTR_WO(stats_clear)), 382-392 (stats attribute group and kobj type), 405-474 (log_head_lsn and log_tail_lsn emit cycle:block, reserve_grant_head_bytes and write_grant_head_bytes), 613-627 (error and error-cfg kobject types), 643-660 (metadata class init table: default, EIO, ENOSPC, ENODEV), 804-838 (mount init creates stats, error, error/fail_at_unmount and error/metadata); raw bytes sha256 1cbcffa12346ebe3ebb29b466196786ea07450d67e4e4d1cbd675603784a5805; snapshot .ufo/waves/round-70/before/src/xfs_sysfs.c (898 lines, 18203 bytes) | a mounted XFS exposes stats and a write-only stats_clear that accepts only 1, four read-only log files whose LSN text is cycle:block, and an error tree rooted at fail_at_unmount with a metadata class of named handlers | mined | 2026-11-03 | on-release | corpus/knowledge/xfs-storage-plane-r70.md |
| S293 | xfsprogs v7.2.0 spaceman/health.c — https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git/plain/spaceman/health.c?h=v7.2.0 | code | A | The online health reader behind xfs_spaceman -c health, at xfsprogs release tag v7.2.0: the sick-flag tables it reports from, the report_sick printer, the default filesystem, AG and rtgroup report, and the message it prints when no health state has been recorded | tag v7.2.0, spaceman/health.c lines 61-210 (the filesystem, AG, rtgroup and inode sick-flag tables), 212-235 (report_sick prints unhealthy or ok per flag and counts reported), 358-395 (bulkstat health walk), 399-548 (health_f: option pass, default report at 518-538, not-collected message at 540-545), 569-583 (command registration); raw bytes sha256 84fdd0bec52a7f0efc592c588a6d001c2b8ba389a7e33de7daf5d13a34215950; snapshot .ufo/waves/round-70/before/src/health.c (584 lines, 11763 bytes) | the reader prints only flags the filesystem marked sick or checked, and with nothing to report it states that health status has not been collected and points the operator at xfs_scrub | mined | 2026-11-03 | on-release | corpus/knowledge/xfs-storage-plane-r70.md |
| S294 | Linux v7.2 Documentation/admin-guide/tainted-kernels.rst, second registration — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/tainted-kernels.rst | docs | A | A second registration of the torvalds v7.2 tainted-kernels document already held by S140, opened only to test whether the round-69 byte comparison left any distinct authority | tag v7.2, whole file; fresh fetch 2026-11-03, 9340 bytes, raw sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841; cmp against .ufo/waves/round-27/sources/S140.rst rc 0 | REJECTED: byte-identical to S140 (cmp rc 0, same sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841) and read from the same torvalds v7.2 tag, so a second row adds no authority and no new locator; flip: the v7.2 tree bytes differ from S140's snapshot in at least one byte, or S140 is retired or its URL moves to another revision | rejected | 2026-11-03 | 90d | — |
| S295 | Round-69 host capture, tsukuroi lane — .ufo/waves/round-69/before/host.txt | own-work | A | The round-69 pre-declaration host capture read as a source row for the round-70 XFS storage-plane rule statements: uname and osrelease, package versions, mounts, sysfs presence and modes, and the xfs_spaceman health output | file captured 2026-11-03 by tsukuroi round 69, 2293 bytes, lane path .ufo/waves/round-69/before/host.txt; opened 2026-11-03 | REJECTED: an own-work capture can carry a host observation, a count or a capture digest, but QUALITY 86 says it never verifies a rule row by itself, and the rule rows state upstream behaviour; flip: the row's scope narrows to this host's observation and it is cited alongside an upstream row at the running release (S288, S289 or the S290-S293 set) that carries the rule | rejected | 2026-11-03 | 90d | — |
| S296 | Linux v7.2.11 arch/x86/include/asm/vermagic.h — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/arch/x86/include/asm/vermagic.h?h=v7.2.11 | code | A | The x86 definition site of MODULE_ARCH_VERMAGIC, which S289's include/linux/vermagic.h composes into VERMAGIC_STRING but does not define | tag v7.2.11; S289's pinned snapshot .ufo/waves/round-69/before/src/vm-v7211.h mentions the token only at line 45 inside VERMAGIC_STRING and includes asm/vermagic.h at line 10; grep -c '#define MODULE_ARCH_VERMAGIC' on that snapshot prints 0 and exits 1; the arch header fetched 2026-11-03 is 1481 bytes, sha256 c3e5c428f3f6721ba977ad9309d3034b92503eb7f6013b276de7c31c8fc0b750, and defines the token at lines 47 and 49 | REJECTED: the definition is not inside S289's pinned bytes, so S289 cannot ground it and the round-69 candidate named an arch header that was not pinned at v7.2.11; flip: arch/x86/include/asm/vermagic.h is fetched and registered as its own pinned row with its digest and the definition lines inside its snapshot | rejected | 2026-11-03 | on-release | — |

## 2. Gate record (CORPUS rule 1) — S290–S293

Access date for every row: **2026-11-03**. Each quote is verbatim from the committed snapshot named
in the row's `anchor`, located by 1-based line number, whitespace-normalized, and at most 25 words.

- **S290** — URL `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/xfs.rst?h=v7.2.11`;
  snapshot `.ufo/waves/round-70/before/src/xfs.rst`, lines 281-282, 16 words:
  `Setting this to "1" clears accumulated XFS statistics in /proc/fs/xfs/stat. It then immediately resets to "0".`
- **S291** — URL `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/xfs/xfs_stats.c?h=v7.2.11`;
  snapshot `.ufo/waves/round-70/before/src/xfs_stats.c`, lines 73-74, 12 words:
  `len += scnprintf(buf + len, PATH_MAX - len, " %u", counter_val(stats, j));`
- **S292** — URL `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/xfs/xfs_sysfs.c?h=v7.2.11`;
  snapshot `.ufo/waves/round-70/before/src/xfs_sysfs.c`, lines 374-375, 6 words:
  `if (val != 1) return -EINVAL;`
  (the same store registers the attribute at line 380: `XFS_SYSFS_ATTR_WO(stats_clear);`)
- **S293** — URL `https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git/plain/spaceman/health.c?h=v7.2.0`;
  snapshot `.ufo/waves/round-70/before/src/health.c`, line 542, 9 words:
  `Health status has not been collected for this filesystem.`

Quote locations re-read in the committed bytes 2026-11-03; each row's URL is the exact string in
`.ufo/waves/round-70/before/src/SOURCES.json` (checked below, §5).

## 3. D1 erratum text (round-69 Gate record for S288 and S289)

Append to the round-70 lesson `## Gate`; round-69 bytes are never rewritten.

> **D1 erratum (round-69 Gate record for S288/S289; appended in round 70).** The filed
> `corpus/lessons/round-69.md` `## Gate` carried no URL, access date or located quote for the two
> rows landed that round. Recorded now from the committed round-69 snapshots
> (`.ufo/waves/round-69/before/src/`, `SHA256SUMS` rc 0; digests equal the S288/S289 pins):
>
> - **S288** — `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/tainted-kernels.rst?h=v7.2.11`,
>   opened 2026-11-03; `tk-v7211.rst` lines 72-73, 20 words: `number, as it is a bitfield, where
>   each bit indicates the absence or presence of a particular type of taint.`
> - **S289** — `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/include/linux/vermagic.h?h=v7.2.11`,
>   opened 2026-11-03; `vm-v7211.h` line 12, 8 words: `/* Simply sanity version stamp for modules. */`

## 4. D5 evidence — the three round-69 refusals, re-run 2026-11-03

**(a) second torvalds-v7.2 registration.** Fresh fetch (read-only, scratch) and byte comparison
against the S140 snapshot:

```
$ curl -sSfL --max-time 20 -o /fast/scratch/hyaku/tsukuroi-r70/SC2Sources/tk-torvalds-v72.rst \
    https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/tainted-kernels.rst
HTTP=200 bytes=9340
$ sha256sum .../tk-torvalds-v72.rst
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  .../tk-torvalds-v72.rst
$ cmp .../tk-torvalds-v72.rst .ufo/waves/round-27/sources/S140.rst
CMP_S140_RC=0
```

The registered S140 row already holds these bytes at that tag; the second registration is S294.

**(b) own-work capture row for the round-69 host readings.** The candidate would register
`.ufo/waves/round-69/before/host.txt` (2293 bytes, captured 2026-11-03) as an `own-work` row whose
scope is the XFS storage-plane rule statements. QUALITY 86: a row whose locator is a lane path "may
carry a host observation, a count or a capture digest for that row and never makes the rule verified
by itself". The rule statements describe upstream behaviour, so the capture alone cannot verify them;
the upstream carriers are S288/S289 and the S290–S293 set. Refusal recorded as S295.

**(c) MODULE_ARCH_VERMAGIC row.** Proof from the committed snapshot, plus the arch header the flip
would need:

```
$ grep -c '#define MODULE_ARCH_VERMAGIC' .ufo/waves/round-69/before/src/vm-v7211.h
0
DEFINE_GREP_RC=1
$ grep -n 'MODULE_ARCH_VERMAGIC' .ufo/waves/round-69/before/src/vm-v7211.h
45:	MODULE_ARCH_VERMAGIC						\
$ grep -n 'MODULE_ARCH_VERMAGIC' /fast/scratch/hyaku/tsukuroi-r70/SC2Sources/asm-vermagic-v7211.h
47:# define MODULE_ARCH_VERMAGIC MODULE_PROC_FAMILY
49:# define MODULE_ARCH_VERMAGIC ""
```

`include/linux/vermagic.h` at v7.2.11 only uses the token (line 45) after including
`<asm/vermagic.h>` (line 10); the definition sits in the arch header, which was not pinned in round
69. Refusal recorded as S296; the flip is that arch header registered as its own pinned row.

## 5. Checks

Baseline registry count at the declaration commit (the item's `__BASE__` = `1710bd74`):

```
$ git show 1710bd74:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'
289
```

Cell counts and pipe absence for every draft row written above (`awk -F'|'` prints NF; contract v1
says 11 cells = NF 13). All commands run from the lane root against this file (`F`), 2026-11-03:

```
$ grep -cE '^\| S29[0-6] \|' "$F"
7
$ awk -F'|' '/^\| S29[0-6] \|/ {gsub(/^[[:space:]]+|[[:space:]]+$/,"",$2); print $2, NF}' "$F"
S290 13
S291 13
S292 13
S293 13
S294 13
S295 13
S296 13
$ awk '/^\| S29[0-6] \|/ {n=gsub(/\|/,"|"); split($0,a,"|"); print a[2], n}' "$F"
 S290  12
 S291  12
 S292  12
 S293  12
 S294  12
 S295  12
 S296  12
$ awk -F'|' '/^\| S29[0-6] \|/ && NF!=13 {n++} END{print n+0}' "$F"
0
$ grep -E '^\| S29[4-6] ' "$F" | grep -c 'REJECTED: .*; flip: '
3
$ grep -E '^\| S29[0-3] ' "$F" | grep -c 'corpus/knowledge/xfs-storage-plane-r70.md'
4
```

Each draft row carries exactly 12 pipe delimiters, so no cell contains a pipe: **0**. The `|`
count includes the two row-edge delimiters and the ten inter-cell ones.

URL binding against `.ufo/waves/round-70/before/src/SOURCES.json` (the `source` cell contains the
map URL verbatim): S290 → `xfs.rst`, S291 → `xfs_stats.c`, S292 → `xfs_sysfs.c`, S293 → `health.c`
(one map entry each, exact string match).

Quote location: each of the four Gate quotes is found verbatim in its named snapshot after
whitespace normalization at the stated 1-based lines (S290 281-282, S291 73-74, S292 374-375,
S293 542), and the two D1 quotes at `tk-v7211.rst` 72-73 and `vm-v7211.h` line 12.

Baseline rows: **289**; draft added here: 7 (4 admitted + 3 rejected); NF all 13; pipes in cells 0.

## 6. Limits

- `corpus/SOURCES.md` was not edited; the rows above are a draft for the L1 to append after S289.
- The numeric sysfs modes (stats 0444, stats_clear 0200) are **host-observed** (`before/host.txt`).
  The kernel `__ATTR_RO`/`__ATTR_WO` mode numbers live in `include/linux/sysfs.h`, which is not among
  the pinned snapshots, so no draft row claims a numeric mode from these bytes. S292 grounds only
  the attribute kinds and the attribute names.
- The C1 note `corpus/knowledge/xfs-storage-plane-r70.md` does not exist at base `1710bd74`
  (`git cat-file -e` rc 128); `used-by` names the declared path and becomes valid when that note
  lands. The declared line anchors are the ranges above; if the note's own anchors pick narrower
  spans inside them, no row content changes.
- Row S293 is pinned at xfsprogs `v7.2.0` (the URL in `SOURCES.json`), not at the kernel tag.
- No install or upgrade was performed (nothing needed; no pacman transaction attempted).

