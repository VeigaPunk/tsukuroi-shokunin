# S1Scout — round 76 w1 scoped findings

Full tables and method: `.ufo/waves/round-76/w1/S1Scout/report.md`. This file is the scoped hand-off.

**Verdict.** 4/4 snapshot digests reproduce on an independent second route and the four committed
snapshots hash to the same values; 8/8 draft quotes are FOUND verbatim with word counts 9, 19, 7, 11, 11,
21, 6, 17 (all inside 4–25); **two rows are PARTLY** (JD3, JD7); **one registry anchor is PARTLY**
(S318); host readings are internally consistent and the host package (262.1-1) is byte-identical to the
v262 pin on all four paths. Nothing is smoothed below: JD3's arithmetic is wrong in the record, JD7's
function attribution is wrong, and S318's anchor range does not cover two sections it names.

## Snapshots (second route: `curl -sSL --fail` into `$HYAKU_SCRATCH`, then `sha256sum`)

| snapshot | observed | expected | verdict |
|---|---|---|---|
| journald.conf.xml | ed71e38d…908f87f2 | ed71e38d…908f87f2 | MATCH |
| journald-config.c | 99f3e972…4bf81a9d | 99f3e972…4bf81a9d | MATCH |
| journald-manager.c | 428dc830…52a7ffa2 | 428dc830…52a7ffa2 | MATCH |
| journalctl.xml | d54bbede…6a1edbdd | d54bbede…6a1edbdd | MATCH |

Extra: `SOURCES.json` and `SHA256SUMS` agree; committed `before/src/` copies hash identically; the same
four paths at tag **v262.1** are byte-identical to v262 (so 262.1-1 on the host is not a version drift for
this pin); every draft row's `digest=` cell and every registry `sha256` token equals the snapshot digest.

## Draft rows

| JD | quote line | words | verdict | defect |
|---|---|---|---|---|
| JD1 | journald.conf.xml:86 | 9 | HOLD | — |
| JD2 | journald.conf.xml:283-284 | 19 | HOLD | cap clause is line 285, one line outside the quote |
| JD3 | journald-manager.c:170 | 7 | **PARTLY** | "the smaller of free space and keep_free" is false: line 168 is `avail = LESS_BY(vfs_avail, keep_free)` and v262 `src/fundamental/macro.h:320-326` defines `LESS_BY(a,b) = a > b ? a - b : 0`. The limit adds free space *after reserving* keep_free (`max(0, free − keep_free)`), not `min(free, keep_free)`. Clamp clause and "both limits respected" hold; the host's 256M is unaffected because max_use binds. |
| JD4 | journald-manager.c:179 | 11 | HOLD | nit: code is `MAX(min_use, vfs_used)` — a floor-raise, and the patch also runs on first journal open (386, 453, 1666, 1668), so "At startup" is a subset |
| JD5 | journald.conf.xml:304 | 11 | HOLD | quote alone carries only the seven-files clause; row drops "(enabled by default)" for compact mode |
| JD6 | journald.conf.xml:313-315 | 21 | HOLD | — ("defaults to 100" is line 318) |
| JD7 | journald-config.c:25-26 | 6 | **PARTLY** | "in journal_config_set_defaults" is over-broad: that function (line 39) sets only `.ratelimit_interval`/`.ratelimit_burst` (51-52); `DEFAULT_SYNC_INTERVAL_USEC` and `DEFAULT_MAX_FILE_USEC` are merged in `manager_merge_configs` (133, 142). All four values are correct; `USEC_PER_MONTH` = 2629800 s. Round-75 failure class. |
| JD8 | journalctl.xml:954-955 | 17 | HOLD | indirect-effect clause is 969-971 |

## Registry S318–S321

All four: 11 columns (12 pipes, no `|` inside a cell), kind docs/code, tier A, status mined, anchor names
the snapshot basename, `used-by` = `corpus/knowledge/journald-retention-plane-r76.md` (file present,
10858 bytes), and every cited row line falls inside the recorded range.

**S318 PARTLY** — its anchor names `MaxFileSec=` and `MaxRetentionSec=` but the range ends at 320; those
`<term>`s are at **322** and **344** (blocks to 341 / 364). No cited line falls outside (86, 283-284, 304,
313-315 are all in 75-93 / 243-320). One-token fix: `243-320` → `243-364`. S319 (24-27), S320 (143-186,
796-820) and S321 (941-983) HOLD; S321 nit: `--rotate`'s own definition is at 1051-1058, outside the range.

## Host readings

Consistent: `df -B1 /` and `stat -f /` agree exactly (blocks×bsize = total, bavail×4096 = available,
(blocks−bfree)×4096 = used, 4,339,007,488 B reserved); boot count 3 is correct (`--list-boots` prints a
header, 4 lines). 148.6M vs `sum_bytes` 209715200 is **sparseness, not contradiction**: `du` allocated =
155,832,320 B = 148.60 MiB (exactly `--disk-usage`), `du --apparent-size` = 209,715,200 B = 200 MiB
(exactly `sum_bytes`), and the largest file is 25,165,824 apparent vs 17,227,776 allocated. Derived figures
hold: `SystemMaxFileSize` = 256M/8 = 32M; effective limit = `CLAMP(760,100,634,624, min_use, 268,435,456)`
= **256M** with keep_free default = min(15% = 149,705,667,379 B, **4G cap**) = 4,294,967,296 B.
No draft row relies on host readings — all eight are source rows; only the note's "Effective limits on
this host" paragraph consumes `host.txt`.

## Owed before commit (not mine to do)

1. Fix JD3's middle clause (and the note prose at `corpus/knowledge/journald-retention-plane-r76.md`
   ~line 40, which repeats "the smaller of the free space and the keep-free requirement" directly after
   quoting `avail = LESS_BY(vfs_avail, metrics->keep_free)`).
2. Fix JD7's attribution to the two functions, or drop "in journal_config_set_defaults".
3. Widen S318's anchor to `243-364` (or drop MaxFileSec/MaxRetentionSec from the parenthetical).

## Residual unknowns

`min_use` actually loaded at runtime is not observable from the pin (patch is `MAX(min_use, vfs_used)`,
called at 386/453/1666/1668); the 4G cap on the percentage defaults is documented in S318 but applied by
`journal_reset_metrics`, whose definition is outside the four pinned files; v262 vs v262.1 was compared
for these four paths only.
