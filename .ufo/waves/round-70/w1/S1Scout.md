# S1Scout — C1 source re-open by a second route

Seat S1Scout (scout, wave w1, round 70, hyaku run 15), leaf. Declaration read at
`1710bd74aec840c71d5e4ffbdc0ca54198e953fa` (`SCORECARD.md` §"Round 70 — declaration", line 5271).
Claim under scouting: C1 depth, four committed snapshots under `.ufo/waves/round-70/before/src/`.
Precondition from declaration (a): "a second route is required from the wave's scout before any
row is admitted". **This seat answers that precondition: ROUTE2_OK=4/4, MATCHED=4/4.**

Lane tree was read-only here; every artifact of this seat lives under
`.ufo/waves/round-70/w1/S1Scout.md` and `.ufo/waves/round-70/probes/S1Scout/` plus scratch.

## 1. Second-route fetches

Route 1 (already committed, `before/src/FETCH.txt`) was git.kernel.org cgit `plain/?h=<tag>`.
Route 2 is a different host and, for `health.c`, a different artifact type:

| snapshot | route 2 | transport |
|---|---|---|
| `xfs.rst` | `https://raw.githubusercontent.com/gregkh/linux/v7.2.11/Documentation/admin-guide/xfs.rst` | GitHub raw CDN mirror of the stable tree at tag `v7.2.11` |
| `xfs_stats.c` | `https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/xfs/xfs_stats.c` | same |
| `xfs_sysfs.c` | `https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/xfs/xfs_sysfs.c` | same |
| `health.c` | `https://mirrors.edge.kernel.org/pub/linux/utils/fs/xfs/xfsprogs/xfsprogs-7.2.0.tar.xz` → member `xfsprogs-7.2.0/spaceman/health.c` | official release tarball (xz), not the cgit plain endpoint |

Commands (scratch root `/fast/scratch/hyaku/tsukuroi-r70/S1Scout`, all `curl_exit=0`):

```
curl -sS --max-time 60 -o <basename> "https://raw.githubusercontent.com/gregkh/linux/v7.2.11/<path>"
curl -sS --max-time 180 -o xfsprogs-7.2.0.tar.xz \
     "https://mirrors.edge.kernel.org/pub/linux/utils/fs/xfs/xfsprogs/xfsprogs-7.2.0.tar.xz"
tar -xJf xfsprogs-7.2.0.tar.xz -C tar --strip-components=1 xfsprogs-7.2.0/spaceman/health.c
cmp <route2-file> /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-70/before/src/<file>
```

Tarball itself: 1 599 484 bytes, sha256 `501dfa363cd8e19997a4a1a71f70ded88241b45e9db233e8875c23b80520cc83`.

## 2. Three-way digest agreement (route 2 = committed = SOURCES.json)

| snapshot | bytes (r2 / committed) | route-2 sha256 | `cmp` | `SOURCES.json` |
|---|---|---|---|---|
| `xfs.rst` | 22719 / 22719 | `53bda67b5612a3f2c02820604d05825c9d37addba9855e1d4fba330a516d051c` | rc 0 | equal |
| `xfs_stats.c` | 5319 / 5319 | `4b6a9b6c239a92abb56838798a2d5657a53ba5a7fb1bee6aa9c12b89f7c9e452` | rc 0 | equal |
| `xfs_sysfs.c` | 18203 / 18203 | `1cbcffa12346ebe3ebb29b466196786ea07450d67e4e4d1cbd675603784a5805` | rc 0 | equal |
| `health.c` | 11763 / 11763 | `84fdd0bec52a7f0efc592c588a6d001c2b8ba389a7e33de7daf5d13a34215950` | rc 0 | equal |

Observed fact: the four committed files are byte-identical to bytes served by a second host, and
each digest equals the digest recorded in `before/src/SOURCES.json` — so the registry-binding
clause of the counter (`digest == snapshot sha256 == SOURCES.json digest`) rests on bytes that two
independent routes agree on. Nothing was rewritten in `before/`.

## 3. Line anchors each planned row must rest on (1-based, committed snapshots)

All quotes below were checked with the frozen counter's own predicates: `words() <= 25`,
no `|`, and the whitespace-normalized presence test (`located=yes` for all 25 candidates in
`probes/S1Scout/quotes.tsv`). Word counts are that function's `len(q.split())`.

### (a) `xfs_stats.c` — stats file surface

| fact | lines | quote (words) |
|---|---|---|
| `xstats[]` group table, 30 entries | 29-32 decl, 33-63 entries, 64 close | `static const struct xstats_entry { char *desc; int endpoint; } xstats[] = {` (13) |
| group loop, one summary line per entry | 66-76 | `for (i = j = 0; i < ARRAY_SIZE(xstats); i++) { len += scnprintf(buf + len, PATH_MAX - len, "%s",` (20) |
| `counter_val` sums **32-bit** per-CPU words | 10-17, cast at 15 | `val += *(((__u32 *)per_cpu_ptr(stats, cpu) + idx));` (7) |
| `xpc` precision line (3 × `%llu`) | 86-87 | `len += scnprintf(buf + len, PATH_MAX-len, "xpc %llu %llu %llu\n", xs_xstrat_bytes, xs_write_bytes, xs_read_bytes);` (13) |
| `defer_relog` precision line | 88-89 | `len += scnprintf(buf + len, PATH_MAX-len, "defer_relog %llu\n", xs_defer_relog);` (9) |
| `debug` precision line (compile-time 0/1) | 90-95 | `len += scnprintf(buf + len, PATH_MAX-len, "debug %u\n",` (8) |
| `gc` precision line reuses the `xpc` label | 96 | `len += scnprintf(buf + len, PATH_MAX-len, "gc xpc %llu\n", xs_gc_bytes);` (10) |

Supporting: `xfs_stats_clearall` zeroes every per-CPU block but saves two stateful counters,
`xs_inodes_active` and `xs_inodes_meta` (101-119, restore at 115-116); `/proc/fs/xfs/stat` is a
symlink to `/sys/fs/xfs/stats/stats` (157-158); precision locals are `uint64_t` and summed only
when the file is read (20-27, 77-84). The group loop prints `%u` per field, i.e. the 32-bit sum.

### (b) `xfs_sysfs.c` — the stats pair and the four log attributes

| fact | lines | quote (words) |
|---|---|---|
| `stats_show` → `xfs_stats_format` | 349-357 | `STATIC ssize_t stats_show( struct kobject *kobject, char *buf)` (8) / `return xfs_stats_format(stats->xs_stats, buf);` (3) |
| `stats` registered read-only | 358 | `XFS_SYSFS_ATTR_RO(stats);` (1) |
| `stats_clear_store` signature | 361-364 | `STATIC ssize_t stats_clear_store( struct kobject *kobject, const char *buf, size_t count)` (11) |
| integer parse | 370 | `ret = kstrtoint(buf, 0, &val);` (5) |
| only 1 accepted, else `-EINVAL` | 374-375 | `if (val != 1) return -EINVAL;` (6) |
| clear then return count | 377-378 | `xfs_stats_clearall(stats->xs_stats); return count;` (3) |
| `stats_clear` registered write-only | 380 | `XFS_SYSFS_ATTR_WO(stats_clear);` (1) |
| `log_head_lsn` format `%d:%d` (cycle:block, live `l_curr_*`) | 405-421 | `return sysfs_emit(buf, "%d:%d\n", cycle, block);` (5) |
| `log_tail_lsn` format `%d:%d` via `xlog_crack_atomic_lsn` | 423-435 | `xlog_crack_atomic_lsn(&log->l_tail_lsn, &cycle, &block); return sysfs_emit(buf, "%d:%d\n", cycle, block);` (8) |
| `reserve_grant_head_bytes` format `%lld` | 437-445 | `return sysfs_emit(buf, "%lld\n", atomic64_read(&to_xlog(kobject)->l_reserve_head.grant));` (4) |
| `write_grant_head_bytes` format `%lld` | 447-455 | `return sysfs_emit(buf, "%lld\n", atomic64_read(&to_xlog(kobject)->l_write_head.grant));` (4) |
| the four form one attribute group | 457-463 | `static struct attribute *xfs_log_attrs[] = { ATTR_LIST(log_head_lsn), ATTR_LIST(log_tail_lsn), ATTR_LIST(reserve_grant_head_bytes), ATTR_LIST(write_grant_head_bytes),` (10) |

Four log shows, two formats: LSNs as `cycle:block` `%d:%d`, grant heads as `%lld` from `atomic64_read`.

### (c) `xfs.rst` — error-configuration hierarchy and the metadata class

| fact | lines | quote (words) |
|---|---|---|
| hierarchy for each mounted filesystem | 408-411 | `The configuration files are organized into the following hierarchy for each mounted filesystem: /sys/fs/xfs/<dev>/error/<class>/<error>/` (14) |
| `<class>` = subsystem, metadata the only defined one since 4.9 | 418-422 | `The subsystem the error configuration belongs to. As of 4.9, the defined classes are: - "metadata": applies metadata buffer write IO` (21) |
| class meaning | 389-392 | `Specifies the subsystem the error configuration will apply to, such as metadata IO or memory allocation.` (16) |

Supporting: handlers act independently and the first met condition propagates (397-400); `<dev>` is
the short device name used in `XFS(<dev>):` messages (414-416); the global `error/` level holds
`fail_at_unmount` (Min 0, Default 1, Max 1) (428-433); per-class handlers are
`max_retries` (Min -1, Max INTMAX; -1 forever, 0 fail fast, N retries) and `retry_timeout_seconds`
(Max 1 day) (454-490); `metadata/ENODEV` defaults to 0 not -1 because ENODEV is fatal for
metadata IO (492-496).

### (d) `health.c` — the "not collected" state

| fact | lines | quote (words) |
|---|---|---|
| nothing reported → not-collected message | 540-542 | `if (!reported) { fprintf(stderr, _("Health status has not been collected for this filesystem.\n"));` (13) |
| remedy points at `xfs_scrub` | 543-544 | `_("Please run xfs_scrub(8) to remedy this situation.\n"));` (7) |

Short forms for the row quote field: `Health status has not been collected for this filesystem.`
(9 words) and `Please run xfs_scrub(8) to remedy this situation.` (7 words), both located verbatim.

## 4. Does the v7.2.11 admin guide mention the stats or log sysfs files? No.

`grep -c -F` over the committed `xfs.rst` (`probes/S1Scout/docs-mentions.txt`):
`/sys/fs/xfs` 4, `/sys/fs/xfs/<dev>/error` 3, `/sys/fs/xfs/<dev>/stats` **0**,
`/sys/fs/xfs/<dev>/log` **0**, `log_head_lsn` 0, `log_tail_lsn` 0, `reserve_grant_head_bytes` 0,
`write_grant_head_bytes` 0, `xfs_spaceman` 0, `xfs_scrub` 0, `stats` 1, `stats_clear` 1,
`/proc/fs/xfs/stat` 1.

The single `stats` hit is the **sysctl** `fs.xfs.stats_clear` (line 280) whose prose (281-282) names
`/proc/fs/xfs/stat`, i.e. the legacy proc interface — not `/sys/fs/xfs/<dev>/stats/stats`. The four
`/sys/fs/xfs` lines in the docs are 411, 431, 461 (error) and 545 (`zoned/`).

Code-only facts (must be attributed to the source files, never to the guide): the stats file's
group/precision line structure, the `stats_clear` write-only one-value contract, all four log
attributes and their formats, and the health reader's not-collected state. Documented facts: the
error tree, its `<class>`/`<error>` decomposition, `fail_at_unmount`, `max_retries`,
`retry_timeout_seconds`, and the metadata/ENODEV default.

## 5. Code-to-host structural check (read-only, `before/host.txt`)

- `xstats[]` holds 30 entries; the live stats file's first label line (host.txt 54, identical on 57
  and 60) lists those 30 labels **in code order** followed by `xpc defer_relog debug gc`.
- Live line count 34 = 30 group lines + 4 precision lines; `debug 0` on both filesystems matches the
  `!defined(DEBUG)` branch, and `gc xpc 0` matches the literal `gc xpc` label of line 96.
- Log attributes: 8 path lines = 4 per filesystem (host.txt 35-38, 40-43); values are
  `cycle:block` for the LSNs and plain integers for the grant heads (88-91, 97-100).
- `error/metadata` class directories: exactly 2, one per filesystem (host.txt 26, 31); handler values
  `metadata/ENODEV` 0 vs `metadata/EIO` -1 (host.txt 104-109), i.e. the documented rule at 492-496.
- `xfs_spaceman -c health` output for both mounts (host.txt 153-158) is byte-identical to the two
  message strings at `health.c` 542 and 544.

## 6. Admissible row sketches (candidates for the note writer, not landed rows)

Checked with `words()` and `grounded()` loaded from the frozen counter itself
(`probes/S1Scout/row-sketch-check.txt`: 6/6 pass, `failing=0`):

| row | snapshot | statement words | shared tokens | quote words |
|---|---|---|---|---|
| XS1 | `xfs_stats.c` | 27 | 7 | 13 |
| XS2 | `xfs_stats.c` | 24 | 7 | 13 |
| XS3 | `xfs_sysfs.c` | 24 | 7 | 6 |
| XS4 | `xfs_sysfs.c` | 21 | 8 | 8 |
| XS5 | `xfs.rst` | 26 | 10 | 21 |
| XS6 | `health.c` | 26 | 7 | 9 |

That allocation reaches the frozen target's shape (6 rows over 4 distinct snapshots and 4 registry
ids) without touching any clause; the registry ids, digests and the note file remain the note
writer's to supply. Sketch XS1 folds the file surface and the 32-bit group sum into one statement,
XS2 carries the four precision lines, XS3 the read-only/write-only pair, XS4 the four log
attributes, XS5 the documented error tree plus metadata class, XS6 the health reader.

## 7. Confidence, inference and remaining unknowns

- Observed: 4/4 second-route byte equality, 4/4 digest agreement with `SOURCES.json`, 25/25 quotes
  located and under 25 words, 6/6 sketches inside the counter's thresholds, doc grep counts above.
- [INFERENCE] `raw.githubusercontent.com/gregkh/linux` at tag `v7.2.11` is the stable-tree mirror;
  the byte equality with git.kernel.org cgit shows the two hosts serve identical tag content, which
  is the property the declaration asks for (same revision, second route) and not a stronger claim.
- Unknown / out of this seat: the host's installed packages are `linux 7.2.11.arch1-1` and
  `xfsprogs 7.2.0-1`; this seat proves equality at the upstream tags only and cannot exclude Arch
  patching between tag and package. Statements should therefore say "the v7.2.11 source", not "the
  host binary" (the host capture in §5 is the only host-side evidence used here).
- Route 1 was not re-fetched; its bytes are irrelevant once the committed bytes equal route 2.
- No tool install or upgrade was needed (nothing installed, nothing changed on the host).

## Receipts

`.ufo/waves/round-70/probes/S1Scout/`: `route2-provenance.txt` (commands, bytes, digests, `cmp`),
`quotes.tsv` (25 candidates: file, lines, words, pipe, located), `docs-mentions.txt` (grep census),
`host-crosscheck.txt` (code-to-host structural check), `row-sketch-check.txt` (counter-admissibility),
`INDEX.txt` (digest of each receipt).

ROUTE2_OK=4/4 MATCHED=4/4 DOCS_MENTION_STATS=0 DOCS_MENTION_LOG=0
