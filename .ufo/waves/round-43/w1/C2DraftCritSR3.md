VERDICT: defect-found

Seat C2DraftCritSR3 — adversarial attack (NOT a counted verdict) on row SR3 of
`corpus/knowledge/btrfs-scrub-record-r43.md` at 717b716a8943151ace8657e0ca23d7d9b8434f26.
Sources read: S237 = `.ufo/waves/round-42/frozen/src/scrub.c` (sha256
48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801), all cited regions
(795-830, 843-895, 1020-1040, 1136-1247, 1245-1340, 1420-1560, 1680-1730, 1828-1836) and the
record reader (577-795); S241 = `.ufo/waves/round-43/frozen/hostcap/capture.txt`; the r43 row text;
`corpus/SOURCES.md` S237/S240/S241 rows; `corpus/knowledge/btrfs-scrub-record-r42.md` (all rows and
the wave-2 corrections); `SKILL.md` (scrub/btrfs grep). Provenance re-fetch: upstream v7.1 scr
.c at peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b matches the frozen file byte-for-byte
(sha256 identical, receipt `C2DraftCritSR3/provenance.txt`). No btrfs scrub, record write, ioctl or
host mutation was run; no tools were installed.

## The single strongest finding (F1): SR3's premise is unreachable with self-written records

SR3 sentence 2-3: "For each device whose last record is canceled or unfinished, resume makes that
record the device's `resumed` source, and every record write passes each device through
`scrub_resumed_stats` ...". The selection code exists (scrub.c:1430-1438), but a record produced by
the pinned writer can never satisfy the condition "last record is canceled or unfinished", because:

- Writer, scrub.c:867-869:
  `scrub_writev(fd, buf, sizeof(buf), "%lld", use->scrub_args.devid) || scrub_write_buf(fd, buf, ret) ||`
  `ret` is 0 at this point (initialized at 846; the header write at 856-861 left it 0; nothing in the
  loop assigns it). `scrub_writev` (782-793) formats the devid into `buf` and returns
  `scrub_write_buf(fd, buf, len)` = `write(fd,buf,len) - len` = 0 on success, so the chain proceeds and
  `scrub_write_buf(fd, buf, 0)` writes 0 bytes. The device id is never emitted: every line written is
  `<fsid>:|data_extents_scrubbed:<n>|...` (no devid digits after the colon).
- Reader, scrub.c:693-698 (state 4, "read dev id"):
  `for (j = 0; isdigit(l[i + j]) && i+j < avail; ++j); if (j == 0 || ...) _SCRUB_INVALID;`
  With `|` immediately after the colon, `j == 0` → `_SCRUB_INVALID` (569-576) — the line is skipped
  (with `warning("invalid data on line ...")` since report_errors=1, e.g. scrub.c:1366/1940), and the
  allocated record keeps `devid` 0 and `finished`/`canceled` 0.
- `last_dev_scrub` (1136-1148) matches `past_scrubs[i]->devid == devid`; parsed records all carry
  devid 0 while real device ids are >=1 (S241 capture.txt:6: root devid=1). So `last_scrub` is NULL
  for every device, the `else if (resume)` branch (1435-1438) sets `skip=1` for all, `n_start==0 &&
  n_resume==0` (1452) prints "nothing to resume" and exits 2 (1727-1728). The `resumed`-source
  mechanism SR3 describes never engages for records written by this same binary; SR3's first two
  sentences describe code that is dead for self-written records.

Upstream authenticity (not a freeze artifact): the frozen file's sha256 equals raw upstream v7.1
(peeled 4ab0e80) fetched 2026-10-26; the identical `scrub_write_buf(fd, buf, ret)` pattern is present
in v5.19, v6.0, v6.5, v6.13 and in current master (master sha256
b58942ccaff74cf2300f5d25b99624ba8e9cfcb59eda5897639f1928b277d528, fetched 2026-10-26). This is a
long-standing upstream behavior, not an artifact of the round-42 freeze.

This also narrows SR1's tail explanation: `invalid data on line` warnings occur for every self-written
record even with no trailing bytes, independent of the SR1 leftover-`_tmp` mechanism.

Narrower replacement for SR3 sentences 2-3 (keep as the operative text):
"Resume selects per device only from a readable prior record that the parser accepted (scrub.c:693-698
requires a devid digit after the fsid colon, and scrub.c:867-869 never emits one, so records written by
this same v7.1 writer parse with devid 0 and match no device; resume then reports 'nothing to resume'
(scrub.c:1452-1457, 1727-1728)). For a device whose readable last record is canceled or unfinished,
resume makes that record the device's `resumed` source and passes its `last_physical` back to the
kernel as `scrub_args.start` (scrub.c:1433)."

## F2: "only a fresh `start` (no `resumed` source) writes zero counters" is over-absolute

- Recording can be disabled entirely: `mkdir_p(datafile)` failure (1335-1339) or initial-write failure
  (1505-1509) set `do_record=false`; then no record is written at all — not "zero counters".
- The "zero" is literal only for the *first* record: it is written before any ioctl thread exists
  (1501-1510 precede thread creation at 1565/1585; `sp` is `calloc`'d, 1402). Later records during a
  start carry the kernel-fetched counters.
- On a resume, the initial record for devices that are *skipped* (finished record) is also all-zero at
  the pre-fork write (resumed set, but `skip=1` makes `scrub_resumed_stats` return `data` unchanged,
  scrub.c:803-804; the old values are only copied into `sp[i]` later in the child at 1549-1554 and
  appear in the final write at 1701). "Only a fresh start writes zero counters" ignores this.
- Degenerate corner: a resumed device whose interrupted record already holds zero counters writes zeros.

Narrower replacement: "a fresh start begins its first record from a zero baseline (written before any
progress is read, scrub.c:1501-1510); a resume's first record for a resumed device is the interrupted
record's counters plus its `t_start` and the summed durations — both only while recording stays enabled
(`do_record`; scrub.c:1335-1339, 1505-1509), and the pre-fork first record of a resume writes zeros for
skipped devices until the final write (scrub.c:1549-1554, 1701-1708)."

## F3: "writes the earlier record's progress counters added to the new run's" is imprecise

`scrub_resumed_stats` (800-828) sums exactly thirteen fields (806-818: data/tree_extents_scrubbed,
data/tree_bytes_scrubbed, read_errors, csum_errors, verify_errors, no_csum, csum_discards,
super_errors, malloc_errors, uncorrectable_errors, corrected_errors). It does NOT sum:
- `last_physical` — copied from the NEW run (819, `_SCRUB_COPY`);
- `t_resumed` — set to the new run's `t_start` (822);
- `canceled`/`finished` — taken from the new run's current state (820-821);
- `unverified_errors` — neither summed nor persisted (the writer never emits it; status reads it at
  scrub.c:1644).

Narrower replacement: "which for such a device writes the thirteen counted fields summed with the new
run's (scrub.c:806-818), the earlier record's `t_start` (823), and the two durations summed
(824-825); `last_physical` (819), `t_resumed` (= new run's `t_start`, 822) and `canceled`/`finished`
(820-821) come from the new run."

## F4 (minor narrowing): "ends the progress thread with its error, printed only when `do_print` is set"

Verified: a failed `scrub_write_progress` in the cycle does `goto out` → `ERR_PTR(ret)` (1123-1126,
1133), and 1696-1699 prints "recording progress failed" only under `do_print`. Two precision points:
- the print also requires `terr != PTHREAD_CANCELED` (1696) — a cancelled thread prints nothing;
- the cycle also exits with an error from `poll`/`accept` (1043-1047) and from a peer-socket write
  (1111-1117), which are not progress-record writes; and no writes are attempted at all when
  `spc->do_record` is false (1121-1122).

## F5 (footnote): "last record" is actually the first match

`last_dev_scrub` returns the FIRST list entry matching the devid (1144-1146), not the newest. With one
record per device (the normal case) the two coincide; with multiple per-device entries (possible given
SR1 tail behavior) the oldest would win.

## Verified-true statements (no finding)

- `cmd_scrub_resume` → `scrub_start(cmd, argc, argv, true)` (1831-1834) vs `cmd_scrub_start` → false
  (1759-1762). All ten quotes in SR3 match the frozen lines exactly.
- The initial record write at 1501-1510 indeed precedes any ioctl and for a resumed device writes
  old+zero, old `t_start`, old duration (864, 823-825) — the "first record carries interrupted run" claim
  holds as written.
- `do_print` false by default (1249), set by `-B` (1295), cleared when quiet (1332-1333).
- "failed to record the result" prints under `do_print` only (1704-1707); neither branch assigns `err`
  (1690-1708) — exit status is unaffected by recording failures.

## Does the row add detail the lane does not already hold as verified text?

`grep` over `corpus/knowledge` (+`SKILL.md`):

- Already held (r42.md wave-2 corrections, `btrfs-scrub-record-r42.md:185-192`): first-after-resume
  record carries interrupted counters/original start time/accumulated duration; only a fresh start
  writes an all-zero record; mid-run failures print "recording progress failed"/"progress thread
  handling failed", final failure prints "failed to record the result"; all print only in foreground
  (`-B`; `do_print` false by default); none changes the exit status. SC2 holds the field list/order
  (r42.md:45-51).
- `SKILL.md` holds no scrub-record mechanics: the only scrub-related gates are SH4 (`no stats
  available` ≠ clean, line 2368), the storage-health-r26 rows and the round-30/31 gate registry; no
  SR3 content.
- SR3 genuinely adds: the per-device selection criterion `canceled || !finished` and the skip path
  (1430-1443); the explicit plumbing "every record write → `scrub_write_file` → `scrub_resumed_stats`"
  (843-895); the sum-vs-copy/flag/`t_resumed` details (806-826; r42 cited only :795-796 and :823-825);
  the quiet-clearing of `do_print` (1332-1333); "neither branch assigns err" as a narrower restatement
  of r42's "none changes the exit status". The additions are the sentences F1-F3 attack.

## What I did not do

No scrub start/cancel/resume, no record write, no `btrfs` ioctl, no `/var/lib/btrfs` access (host
guard); no counter runs; no git/jj mutations; no installs (no tool was needed beyond `curl`/
`sha256sum`/`grep`/`awk`, all read-only). Evidence for the upstream checks: receipt
`C2DraftCritSR3/provenance.txt` (fetched hashes, 2026-10-26).
