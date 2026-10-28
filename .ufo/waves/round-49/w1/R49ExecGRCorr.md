VERDICT: supports

# R49ExecGRCorr — C1-B1: do the seven round-48 corrections exist in the freeze bytes?

Seat R49ExecGRCorr (executor), round 49 / hyaku 11 / wave w1. Freeze revision
`55c07cd3f8bff2e12117c34d57b4c618de74d85c`. Every byte below was read with
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:<path>`;
the lane working tree was not read and nothing in the lane was written. Receipts:
`.ufo/waves/round-49/w1/R49ExecGRCorr/{freeze.md,corr-replay.txt}`.

## 0. The bytes checked are the bytes under test

The FROZEN.md row hashes reproduce from `corpus/knowledge/btrfs-scrub-grounding-r45.md` at the freeze
revision under the counter's own convention — `tools/check-scrub-admission-r49.py:178-188`: split the
entry on `\n`, take the lines from the single `## GRn` header up to (excluding) the next line starting
`## `, LF-join, sha256:

| row | computed | frozen claim | match |
|---|---|---|---|
| GR1 | `3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1` (lines 14-55) | same | yes |
| GR2 | `d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f` (lines 56-151) | same | yes |
| GR3 | `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` (lines 152-197) | same | yes |

The counter's C7 leg encodes exactly seven corrections (`CORR_REQ`,
`tools/check-scrub-admission-r49.py:97-105`) and five forbidden old strings (`CORR_FORBID`, `:107-112`).
The entry's own round-49 note names the same seven (`btrfs-scrub-grounding-r45.md:280-283`: "GR1: the
`0X` prefix and the host-reading inference mark; GR2: the `is_valid` gate, the cancel sentence's subject,
the suspend-path range and effects, the `ioctl.c:3132` citation and the `-ENODEV` devid case").

## 1. PASS/FAIL per correction (demanded wording → freeze wording)

All line numbers are freeze-revision lines of `corpus/knowledge/btrfs-scrub-grounding-r45.md`.

| # | seat / demand | demanded wording (verbatim) | freeze location and text | verdict |
|---|---|---|---|---|
| 1 | CritGR1a `.ufo/waves/round-48/w2/R48CritGR1a.md:29,36` — radix clause | "which picks hexadecimal for a leading `0x` or `0X` followed by a hex digit, octal for any other leading `0`, and decimal otherwise." | line 18: "picks hexadecimal for a leading `0x` or `0X` followed by a hex digit, octal for any other leading `0`, and decimal otherwise." | **PASS** |
| 2 | CritGR1a `R48CritGR1a.md:39-41` — host-reading inference mark | "so this caller [inference: by ordinary file-mode checks, which the capture does not exercise] cannot write one." | lines 52-54: "this caller [inference: by ordinary file-mode checks, which the capture does not exercise; ACLs and LSM rules are not captured] cannot write one." | **PASS** (superset: adds the ACL/LSM caveat) |
| 3 | CritGR2a `R48CritGR2a.md:15-16` — `is_valid` gate | "which it is when the replace data is valid (`is_valid`, dev-replace.c:1278-1279) and the state is started or suspended (dev-replace.c:1286-1287; a replace suspended by an unmount still counts, per the comment at dev-replace.c:1288-1297)" | lines 68-71, verbatim modulo wrapping | **PASS** |
| 4 | CritGR2a `R48CritGR2a.md:18-19` + RevGR2a `R48RevGR2a.md:17` — cancel sentence's subject | CritGR2a exact text: "While the copy runs, the replace's source device carries the scrub context the copy attached (scrub.c:3159); by SR7, `btrfs_dev_replace_cancel` stops it with `btrfs_scrub_cancel` for a started replace (dev-replace.c:1111) and, for a suspended replace, calls `btrfs_scrub_cancel` too (dev-replace.c:1126-1144) although the pinned code says the replace scrub is not running in that state (dev-replace.c:1127-1129)." | lines 75-79, verbatim | **PASS** |
| 5 | CritGR2a `R48CritGR2a.md:20` (second minor) + RevGR2a `R48RevGR2a.md:19` — suspend-path range | replace "(dev-replace.c:1171-1199)" with dev-replace.c:1171-1195 | line 82: "(dev-replace.c:1171-1195, state set at :1184-1188)"; old range absent | **PASS** |
| 6 | RevGR2a `R48RevGR2a.md:19` — suspend-path effects | "only moves a STARTED replace to SUSPENDED (with time_stopped and a writeback flag)" | lines 81-82: "only moves a STARTED replace to SUSPENDED, with `time_stopped` and a writeback flag (dev-replace.c:1171-1195, state set at :1184-1188), and does not call `btrfs_scrub_cancel`."; old "only sets the state to SUSPENDED" absent | **PASS** |
| 7 | RevGR2a `R48RevGR2a.md:20` — host-reading citation | cite "the CAP_SYS_ADMIN check in the scrub-progress ioctl, ioctl.c:3132 (-EPERM at ioctl.c:3133)" | lines 143-144: "the `CAP_SYS_ADMIN` check in the scrub-progress ioctl, ioctl.c:3132, `-EPERM` at :3133" | **PASS** |
| 8 | RevGR2a `R48RevGR2a.md:21` — ENOTCONN/ENODEV | add "for a devid that exists; an unknown devid gives -ENODEV (scrub.c:3336)" | lines 79-80: "returns `-ENOTCONN` for a devid that exists (`scrub.c:3222, :3336`); an unknown devid gives `-ENODEV` (`scrub.c:3336`)" | **PASS** |

Rows 1-8 are the seven seat demands folded onto the counter's seven patterns: row 4 = pattern
`the copy attached\s*\n?\(scrub\.c:3159\)`; rows 5+6 = pattern `dev-replace\.c:1171-1195` plus forbid
`only sets the state to SUSPENDED`; row 8 = pattern `an unknown devid gives `-ENODEV``.

Exact `corr_ok` replay against the freeze bytes (the counter's own regexes, `corr-replay.txt`):
`CORR_REQ matched 7/7; missing=[]`, `CORR_FORBID absent 5/5; present=[]`, `corr_ok=1`.

## 2. The five demanded citations resolve in the pinned snapshots

Observed with the grep tool (line/column prefixes are the tool's):

- `dev-replace.c:1111` — `1110| up_write(&dev_replace->rwsem);` / `*1111| ret = btrfs_scrub_cancel(fs_info);`
  inside `*1107| case BTRFS_IOCTL_DEV_REPLACE_STATE_STARTED:` (round-45 snapshot). Correct branch, correct line.
- `dev-replace.c:1171-1195` — `*1171|void btrfs_dev_replace_suspend_for_unmount(...)`, close at
  `*1195|}`, next function comment at `*1197|/* resume dev_replace procedure that was interrupted by unmount */`
  (`1196` blank). The range is exactly the whole function and stops before the next header, as demanded.
- `dev-replace.c:1278-1279` — `*1278| if (!dev_replace->is_valid)` / `1279| return false;`; state switch at
  `*1286| case ...STARTED:` / `*1287| case ...SUSPENDED:`; the cited comment opens `1288| /*` and closes
  `*1297| */`, matching the row's "comment at dev-replace.c:1288-1297".
- `scrub.c:3159` — `3158| sctx->readonly = readonly;` / `*3159| dev->scrub_ctx = sctx;` (round-44 snapshot);
  cleared at `*3222| dev->scrub_ctx = NULL;`, and the ENOTCONN/ENODEV return is
  `*3336| return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`.
- `ioctl.c:3132` — inside `*3126|static long btrfs_ioctl_scrub_progress(...)`, `*3132| if (!capable(CAP_SYS_ADMIN))`
  / `*3133| return -EPERM;` (round-43 snapshot). The sibling `btrfs_ioctl_scrub_cancel` check is at `:3120-3121`,
  so the row's line is the scrub-**progress** one, as written.

The radix correction's deciding line also resolves: `kstrtox.c:30` `if (_tolower(s[1]) == 'x' && isxdigit(s[2]))`,
`:31 *base = 16;`, `:33 *base = 8;`, `:35 *base = 10;`, `:37` skips the `0x`/`0X` prefix — uppercase `0X10` is hex.
The suspend-path correction's effects resolve: `dev-replace.c:1184` `case ...STARTED:`, `:1185-1186` state →
SUSPENDED, `*1187| dev_replace->time_stopped = ktime_get_real_seconds();`,
`*1188| dev_replace->item_needs_writeback = 1;`, and `:1193-1195` contain no `btrfs_scrub_cancel`.

## 3. Corrections the r48 seats demanded that are still absent

1. **CritGR2a item 3, first half (`R48CritGR2a.md:20`), still absent.** Demanded: replace "writeable" because
   "a readonly start passes the -EROFS check (scrub.c:3127-3128), so the true set is wider". Freeze line 73 still
   reads "for a present, writeable device that is in the filesystem metadata and is not the replace target is".
   The demanding seat graded this "Minor (not blocking) ... the conclusion stays true", and no `CORR_REQ` pattern
   tests it, so it does not move `corr_ok`; it is a residual wording nit, not a predicate defect.
2. **CritGR1a completeness note (`R48CritGR1a.md:42`), still absent.** The seat noted the quotes do not cover the
   `shl += 10` lines or `sysfs.c:2042`. The freeze quote list cites cmdline.c:147/156/159/189/191/192 and
   sysfs.c:2040/2043 only; `grep -c "cmdline.c:163"` and `grep -c "sysfs.c:2042"` both return 0. The seat labeled
   this "completeness note only", so it is not a defect for `corr_ok` either.
3. **Counter comment precision (not a predicate failure).** `tools/check-scrub-admission-r49.py:96-97` says the
   seven patterns cover "CritGR2a item 1, item 2, item 3, item 4", but item 3's "writeable" half has no pattern;
   only its range half is covered (`dev-replace.c:1171-1195`). Consequence: `corr_ok` would read 1 even with the
   "writeable" wording in place — which is what happens. Worth a comment fix only.
4. **RevGR2a's "bare token SR7" sub-point (`R48RevGR2a.md:17`).** The adopted sentence is CritGR2a's exact
   replacement, which keeps "by SR7,"; RevGR2a's own replacement removed it. The entry does gloss SR7 in its
   scope paragraph ("whether a device replace runs through the same scrub context (SR7)", line 10) and defines it
   in `corpus/knowledge/btrfs-scrub-record-r44.md:15` (`## SR7`). Not a defect; the two seats' exact texts conflict
   and the counted critic's text was used.

## 4. Snapshot integrity (all reads are against the pinned copies)

- round-45 `frozen/src`: `cmdline.c: OK`, `dev-replace.c: OK`, `kstrtox.c: OK`, `vsprintf.c: OK` from `sha256sum -c SHA256SUMS`.
- round-44 `frozen/src`: `scrub.c: OK`, `sysfs.c: OK`; round-43 `frozen/src`: `ioctl.c: OK`.
- round-45 `frozen/hostcap/capture.txt` = `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`,
  equal to the digest in the entry header (line 1) and in FROZEN.md.

## 5. Not done

- I did not run `tools/check-scrub-admission-r49.py` itself (it is selftest-bearing, 1-6 selftests, 5-10 min);
  this item authorized only the named `git show` read and the snapshot checks. So `structural_ok`, `quotes_ok`,
  `verdicts_ok`, `seats_ok` and `marks_ok` were not exercised by me — only the `corr_ok` legs, replayed in Python
  with the counter's own regex tuples.
- No kernel, sysfs, scrub, replace or systemd action was run; no lane file, index, jj state or fleet file was
  touched. No tool was installed or upgraded (record: none).

## 6. Bottom line

The seven corrections the round-48 counted seats demanded are present in the freeze bytes, at the cited lines,
with the old strings gone; the five asked-for citations resolve in the pinned snapshots; `corr_ok = 1` on a
faithful replay of the counter's own patterns. Two non-blocking seat notes (the "writeable" wording and the
`shl`/`sysfs.c:2042` quote completeness) remain unapplied exactly as the demanding seats graded them.
