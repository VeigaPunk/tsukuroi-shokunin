VERDICT: supports

# R52ScoutReopenS242 — independent re-open of S242 and S243

Scope: re-open the live kernel sources, compare with the pins and the round-44 snapshots, and verify five-plus file:line citations per source at ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0. Receipt: `.ufo/waves/round-52/w1/R52ScoutReopenS242/reopen-S242-S243.txt`.

## Pins and access (per source)

| Source | Access (UTC) | Live size | Live sha256 | Pin (SOURCES.md row) | Match |
|---|---|---|---|---|---|
| S242 fs/btrfs/scrub.c, tag v7.2.11 | 2026-10-30T05:39:16Z (fetch; headers `last-modified` 2026-10-30 05:39:57 GMT) | 100417 B | f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8 | f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8 | yes |
| S243 fs/btrfs/sysfs.c, tag v7.2.11 | 2026-10-30T05:39:16Z (headers `last-modified` 2026-10-30 05:39:58 GMT) | 72925 B | ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43 | ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43 | yes |

- Tag: `git ls-remote` on the kernel.org stable repo gives `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea refs/tags/v7.2.11^{}`, matching the pinned peeled commit (receipt, tag section).
- Local snapshot digests: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-44/frozen/src/` prints `scrub.c: OK` and `sysfs.c: OK`. Those `SHA256SUMS` lines carry the same digests as the pins.
- Byte-identical: live `scrub.c` == local `scrub.c` (yes, `cmp`); live `sysfs.c` == local `sysfs.c` (yes, `cmp`).
- Drift check: `?h=v7.2.13` fetch of both files gives the same digests (`diff` empty). The pinned tag is one of 13 v7.2.x tags on the remote, and the two files are unchanged through v7.2.13.
- Tree-page URLs in the rows return HTTP 200 (scrub.c 234951 B, sysfs.c 181619 B).

Caveat on the "live" fetch: the sandbox resolved git.kernel.org at 2026-10-30, so "access" here is my fetch time, not a stored archive.

## Citation checks at ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0

Method: parse every `**Quote.** S24x file:line: "…"` line of GR2 and GR3 (the rows the seat names), then compare the quoted text with `live_*.c` at that line, whitespace-trimmed. Result: all S242/S243 quotes in GR2 match.

GR2 (S242/S243 quotes): 24 of 24 match.
- scrub.c (S242): 3081, 3094, 3095, 3109, 3114, 3120, 3123, 3127, 3133, 3138, 3139, 3142, 3147, 3148, 3149, 3153, 3159, 3222, 3336 — all MATCH.
- sysfs.c (S243): 78, 1288, 1302, 2015, 2019 — all MATCH.

Illustrative content checks (the complete per-citation MATCH lists above supply 19 S242 and five S243 checks from GR2):

1. S242 scrub.c:3094-3095 — `if (btrfs_fs_closing(fs_info)) return -EAGAIN;` — claim matches; the GR2 statement's `-EAGAIN` check is there.
2. S242 scrub.c:3147-3153 — `if (dev->scrub_ctx || (!is_dev_replace && btrfs_dev_replace_is_ongoing(...))) … ret = -EINPROGRESS;` — matches the GR2 claim (`-EINPROGRESS` when a scrub context is attached or a non-replace call sees an ongoing replace).
3. S242 scrub.c:3336 — `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` — matches S242 row's claim: 0 only with an attached context, ENOTCONN idle, ENODEV unknown devid.
4. S242 scrub.c:1381-1382 — `if (bwlimit == 0) return;` — matches S242 row's "limit of 0 disables throttling" (line range 1365-1385 covers it).
5. S243 sysfs.c:78 and 2015/2019 — `__INIT_KOBJ_ATTR(_name, 0444, _show, NULL)`; `val = !!test_bit(BTRFS_DEV_STATE_REPLACE_TGT, ...)`; `BTRFS_ATTR(devid, replace_target, ...)` — matches GR2's "mode 0444, read-only" and replace_target reads the target bit. (Note: the GR2 row names `BTRFS_ATTR` at line 78; that macro is the 0444 variant.)

The five individual S243 citation verdicts (GR2):
- sysfs.c:78 — MATCH: the macro initializer uses mode 0444.
- sysfs.c:1288 — MATCH: assigns `str = "device replace\n";`.
- sysfs.c:1302 — MATCH: declares `exclusive_operation` with `BTRFS_ATTR`.
- sysfs.c:2015 — MATCH: reads `BTRFS_DEV_STATE_REPLACE_TGT` as a Boolean.
- sysfs.c:2019 — MATCH: declares `replace_target` with `BTRFS_ATTR`.

Five individual S242 sample verdicts from GR2: scrub.c:3081 MATCH (readonly/is_dev_replace parameters); :3094 MATCH (filesystem-closing condition); :3095 MATCH (-EAGAIN return); :3159 MATCH (attach context); :3222 MATCH (clear context). All are literal line-content checks, not semantic proof of every caller.

Additional S243 row checks (sysfs.c lines from the S243 row):
- 72-74: `BTRFS_ATTR_RW` is 0644 — the scrub_speed_max attribute is 0644 (`BTRFS_ATTR_RW(devid, scrub_speed_max, ...)` at 2048-2049). Verified.
- 2021-2049: show emits `sysfs_emit(buf, "%llu\n", …)` (line 2028), verifying decimal-plus-newline output. Store calls `memparse` (2040), then `skip_spaces` (2042), then rejects remaining non-space text with `-EINVAL` (2043-2044). Precision caveat: SOURCES.md:252 says "anything trailing rejected"; trailing whitespace is actually accepted. Proposed wording: "a write is parsed by memparse; trailing whitespace is skipped and any remaining text is rejected as EINVAL."
- 2113: `BTRFS_ATTR_PTR(devid, scrub_speed_max)` registered — verified.

S242 row ranges: 1365-1385 (throttle function, 1380-1382 limit==0 return), 3140-3162 (dev->scrub_ctx attach at 3159, -EINPROGRESS at 3153), 3215-3226 (scrub_ctx cleared at 3222), 3321-3337 (btrfs_scrub_progress, 3336 return) — all contain the cited content.

GR1 (for completeness; S242/S243 quotes in GR1): 7 of 8 match. The one mismatch is whitespace-only: GR1 quotes `S242 scrub.c:1369` as "* second. Limit can be set…" with one space; the source line 1369 is "* second.  Limit can be set…" with two spaces (live_scrub.c:1369). The claim is unaffected. Proposed fix if the row is re-quoted: use the double-space form.

## Things checked that are NOT S242/S243 (noted to avoid confusion)

- GR3 quotes `S237 … scrub.c:421…1710` cite the btrfs-progs v7.1 `cmds/scrub.c`, not the kernel file. My first pass compared them with the kernel `scrub.c` and reported 9 mismatches; that was my error. Against `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` (sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801, fetched this session, not compared with an S237 pin) all 9 quotes match.

## Limits

- I did not re-verify GR1/GR2/GR3 prose beyond quoted lines (the claims are logic on the source, not my assessment).
- I checked only the quoted lines and the S242/S243 row ranges; full kernel behaviour outside those lines is out of scope.
- No counted verdict is given here; this is a scout report for the L1.

Commands run (absolute paths): `git show ff9470ea…:corpus/SOURCES.md | grep -E '^\| S24[23] \|'`; `curl -sfL https://git.kernel.org/…/fs/btrfs/{scrub,sysfs}.c?h=v7.2.11`; `sha256sum -c SHA256SUMS` in round-44 frozen/src; `git ls-remote --tags …linux.git 'refs/tags/v7.2.*'`; a Python pass over `**Quote.**` lines of GR1/GR2/GR3 comparing against the fetched files.
