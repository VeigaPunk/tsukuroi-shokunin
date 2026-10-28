VERDICT: supports

Seat R49RevCorr (reviewer, non-counted) — independent review of the C1 correction pass. Bytes under test:
`55c07cd3f8bff2e12117c34d57b4c618de74d85c:corpus/knowledge/btrfs-scrub-grounding-r45.md`, read with
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show`. I did not read `R49ExecGRCorr`; the demanded
corrections come from the three r48 reports named in my item, read directly.

## Digest / hash checks I ran (all pass)

- `sha256sum -c SHA256SUMS` in `.ufo/waves/round-45/frozen/src/`: cmdline.c, dev-replace.c, systemd.kill.xml,
  kstrtox.c, vsprintf.c all OK. `dev-replace.c` = f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a,
  `kstrtox.c` = 0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4.
- `.ufo/waves/round-44/frozen/src/`: `scrub.c` = f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8,
  `sysfs.c` = ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43, `btrfs-scrub@.service` OK.
- `.ufo/waves/round-43/frozen/src/ioctl.c` = 7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01,
  equal to S240's recorded digest (`corpus/SOURCES.md:249`).
- `.ufo/waves/round-45/frozen/hostcap/capture.txt` = f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70,
  equal to the digest the entry records on doc line 1.
- Row hashes recomputed independently (Python, `git show` of the freeze, LF-joined lines `## GRn` → next heading,
  no trailing LF): GR1 `3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1`, GR2
  `d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f`, GR3
  `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` — all equal to `.ufo/waves/round-49/frozen/FROZEN.md`.
  Row extents and hashes are what the cohort reads.

## The correction pass, taken from the actual diff

`git diff ae99f021b76f8eb1c8805d32d80644464afb1ff6 55c07cd3f8bff2e12117c34d57b4c618de74d85c --
corpus/knowledge/btrfs-scrub-grounding-r45.md` touches exactly seven prose hunks (plus the round-49 gate heading);
GR3 has no hunk. Per-demand disposition:

1. **CritGR1a defect — `0X` prefix.** Frozen doc line 18: "which picks hexadecimal for a leading `0x` or `0X`
   followed by a hex digit, octal for any other leading `0`, and decimal otherwise." This is the critic's
   replacement text character for character. **Adopted verbatim.** Supported by kstrtox.c:29-33 (`s[0]=='0'`,
   `_tolower(s[1])=='x' && isxdigit(s[2])` → 16, else 8) and kstrtox.c:37 (the prefix skip also uses `_tolower`);
   both snapshot lines are quoted at doc lines 37-41.
2. **CritGR1a minor — host-reading inference mark.** Frozen doc lines 52-54: "…this caller [inference: by
   ordinary file-mode checks, which the capture does not exercise; ACLs and LSM rules are not captured] cannot
   write one." **Adopted with a change** — the critic's shorter bracket was widened with the ACL/LSM caveat.
   The bracket is accurate: capture.txt:8 `mode=644 owner=root value=0`, capture.txt:1 `uid=1000
   CapEff=0000000000000000`, and the capture records no ACL or LSM state.
3. **CritGR2a defect 1 — `is_valid` gate.** Frozen doc lines 68-71: "…which it is when the replace data is valid
   (`is_valid`, dev-replace.c:1278-1279) and the state is started or suspended (dev-replace.c:1286-1287; a replace
   suspended by an unmount still counts, per the comment at dev-replace.c:1288-1297)…". This is the critic's
   replacement text verbatim. **Adopted verbatim.**
4. **CritGR2a defect 2 / RevGR2a finding 1 — cancel sentence.** Frozen doc lines 75-79: "While the copy runs, the
   replace's source device carries the scrub context the copy attached (scrub.c:3159); by SR7,
   `btrfs_dev_replace_cancel` stops it with `btrfs_scrub_cancel` for a started replace (dev-replace.c:1111) and,
   for a suspended replace, calls `btrfs_scrub_cancel` too (dev-replace.c:1126-1144) although the pinned code says
   the replace scrub is not running in that state (dev-replace.c:1127-1129)." This is CritGR2a's replacement text
   verbatim. **Adopted verbatim**; RevGR2a's alternative wording was not used, and its aside that SR7 is
   "never defined inside the row" is not adopted (see "Not adopted" below).
5. **CritGR2a minor 3 (second part) / RevGR2a finding 2 — suspend-path range and effects.** Frozen doc lines
   81-82: "The unmount suspend path itself only moves a STARTED replace to SUSPENDED, with `time_stopped` and a
   writeback flag (dev-replace.c:1171-1195, state set at :1184-1188), and does not call `btrfs_scrub_cancel`."
   **Adopted with a change** — range 1171-1199 → 1171-1195 as demanded, the STARTED precondition and the
   two effects added as demanded, plus an explicit "state set at :1184-1188" citation the reports did not ask for.
6. **RevGR2a finding 3 — `ioctl.c:3132` citation.** Frozen doc lines 143-144: "(the `CAP_SYS_ADMIN` check in the
   scrub-progress ioctl, ioctl.c:3132, `-EPERM` at :3133)". **Adopted verbatim.**
7. **RevGR2a finding 4 — `-ENODEV` devid case.** Frozen doc lines 79-80: "When the replace context is absent, the
   progress query returns `-ENOTCONN` for a devid that exists (`scrub.c:3222, :3336`); an unknown devid gives
   `-ENODEV` (`scrub.c:3336`)." **Adopted with a change** — the demanded qualification and `-ENODEV` clause are
   present; the pre-existing `:3222` citation was kept and the clause split in two.

## Targeted re-reads: did a correction introduce a NEW error?

**(a) `is_valid` parenthetical vs dev-replace.c:1288-1297 — accurate.**
`sed -n '1276,1300p'` of the r45 snapshot: 1276 `bool __pure btrfs_dev_replace_is_ongoing(...)`, 1278
`if (!dev_replace->is_valid)`, 1279 `return false;`, 1286 `case …STARTED:`, 1287 `case …SUSPENDED:`, 1288 `/*`,
1289-1296 the comment ("return true even if tgtdev is missing … if the dev_replace procedure is suspended by an
umount … This does not stop the dev_replace procedure. It needs to be canceled manually…"), 1297 `*/`, 1300
`return true;`. So the cited gate lines are exact, and "a replace suspended by an unmount still counts" is stated
by that comment block and independently true from the code (SUSPENDED → break → `return true`). No new error.

**(b) Suspend-path sentence vs dev-replace.c:1171-1195 and :1184-1188 — correct.**
`grep -n` and `sed -n '1178,1196p'`: 1171 `void btrfs_dev_replace_suspend_for_unmount(...)`, 1178 `switch`, 1184
`case …STARTED:`, 1185-1186 `replace_state = …SUSPENDED`, 1187 `time_stopped = ktime_get_real_seconds()`, 1188
`item_needs_writeback = 1`, 1195 `}`. The function body contains no `btrfs_scrub_cancel`. The STARTED precondition,
`time_stopped`, the writeback flag, the range end at 1195 and the "does not call `btrfs_scrub_cancel`" claim all
hold. No new error.

**(c) `-ENODEV` devid case vs scrub.c:3336 — supported.**
`sed -n '3321,3336p'` of the r44 snapshot: `btrfs_scrub_progress` looks the devid up with `btrfs_find_device`;
line 3336 is `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`. dev NULL (unknown devid) → `-ENODEV`; dev found with
no context → `-ENOTCONN`. The userspace devid reaches this function through `btrfs_ioctl_scrub_progress`
(ioctl.c:3126-3138: `sa->devid` → `btrfs_scrub_progress(fs_info, sa->devid, …)`), so the qualification "for a
devid that exists" is the right one. No new error.

**Extra checks on the other corrections.**
- `scrub.c:3159` is `dev->scrub_ctx = sctx;` (r44 snapshot; function opens at 3079), i.e. the device named by the
  replace's `src_device->devid` (dev-replace.c:701, :1265) carries the context — the attach citation is right.
- dev-replace.c:1111 is `ret = btrfs_scrub_cancel(fs_info);` inside the `case …STARTED:` arm of
  `btrfs_dev_replace_cancel` (function at 1085, switch at 1099); 1126 is `case …SUSPENDED:`, 1127-1129 the comment
  "Scrub doing the replace isn't running…", 1144 the call. "stops it … for a started replace" is accurate inside
  the sentence's "While the copy runs" frame; `btrfs_scrub_cancel` (scrub.c:3277-3296) returns 0 while
  `scrubs_running` is nonzero and -ENOTCONN otherwise, and the STARTED arm maps a negative return to NOT_STARTED
  (1112-1113), so the sentence is not overreaching.
- ioctl.c:3126 `static long btrfs_ioctl_scrub_progress(...)`, 3132 `if (!capable(CAP_SYS_ADMIN))`, 3133
  `return -EPERM;` — the added citation names the progress ioctl, not the cancel one (cancel is 3118-3124).

No correction introduces a new factual error. The five r48 defect strings the claim names are gone from the row
(`0x`-only prefix, the bare "in state started or suspended" without `is_valid`, the "which by SR7" relative clause,
`1171-1199`, and the unqualified `-ENOTCONN` sentence). I checked this by reading the frozen row, not by running
the counter.

## Not adopted (and why that is harmless)

- **CritGR2a minor 3 (first part): "writeable" is stricter than needed.** Not adopted: frozen doc line 73 still
  reads "a present, writeable device that is in the filesystem metadata and is not the replace target is refused
  with `EINPROGRESS`". The critic itself said the conclusion stays true, and it does: the sentence states a
  sufficient condition (`scrub.c:3127-3133` only applies `-EROFS` to `!is_dev_replace && !readonly`, so a readonly
  start on a non-writeable device still reaches the 3147-3153 refusal). No change required; if the row owner wants
  the wider set, the minimal edit is "a present device that is in the filesystem metadata and is not the replace
  target — writeable unless the start is readonly — is refused with `EINPROGRESS`".
- **CritGR1a completeness note (quotes do not cover `shl += 10` or sysfs.c:2042).** Not adopted; the lines exist in
  the snapshot and the critic marked it as non-blocking.
- **RevGR2a aside that SR7 is undefined inside the row.** Not adopted, and not a defect: SR7 is defined in the
  entry scope (doc line 9-10, "whether a device replace runs through the same scrub context (SR7)") and in
  `corpus/knowledge/btrfs-scrub-record-r44.md:15` (`## SR7`).

## Residual notes (non-blocking; no row edit needed for `holds`)

1. `btrfs_dev_replace_is_ongoing` has no `default:` arm; an out-of-enum `replace_state` with `is_valid == 1` also
   returns true. The corrected clause "which it is when … the state is started or suspended" is a sufficient
   condition, so it is not false; only an unattainable corrupt-state case is uncovered. No change.
2. Provenance: the S247 registry row (`corpus/SOURCES.md:256`) declares `fs/btrfs/dev-replace.c lines 700-703,
   1143-1144, 1235, 1256-1268, 1276-1300`. The new citation 1111 (from correction 4) and the cited ranges
   1126-1129 and 1171-1195 fall outside that list, as did the pre-correction citations. The whole-file digest
   f07ef0a0… covers them, so citations remain digest-backed; only the declared-range note is short. Optional
   registry edit (outside the frozen rows): lines `700-703, 1111, 1126-1129, 1143-1144, 1171-1195, 1235,
   1256-1268, 1276-1300`.
3. The entry header's source list (doc line 1) still omits S240 although GR2 cites `ioctl.c` at :3132 and :3190.
   This is pre-existing at the r48 revision as well (same header text), so it was not introduced by the
   correction pass.

## What I did not do

I did not run `tools/check-scrub-admission-r49.py` or any selftest/counter (not named in this item; the counter is
the L1's measurement, and one selftest is minutes of CPU). I did not run a scrub, a replace, a sysfs write or a
privileged ioctl; every kernel claim above is a source read of the pinned snapshots, verified against each wave's
`SHA256SUMS` rather than by re-fetching the upstream URLs. I did not read `R49ExecGRCorr`'s report.
