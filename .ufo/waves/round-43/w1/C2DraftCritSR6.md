VERDICT: draft

Seat C2DraftCritSR6 — adversarial attack on SR6 of corpus/knowledge/btrfs-scrub-record-r43.md
at 717b716a8943151ace8657e0ca23d7d9b8434f26 (freeze fe35700183188f7d712e2932cabde1944efca052).
NOT a counted verdict. Pinned sources verified by sha256 before reading:
- S237 .ufo/waves/round-42/frozen/src/scrub.c = 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801
  (matches declared hash; `sha256sum` run 2026-10-26)
- S240 .ufo/waves/round-43/frozen/src/ioctl.c = 7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01
  (matches SHA256SUMS line 1; `sha256sum` run 2026-10-26)
- S241 .ufo/waves/round-43/frozen/hostcap/capture.txt = f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556
  (matches declared hash; `sha256sum` run 2026-10-26)
SR6 text read from the freeze commit itself (`git -C <lane> show 717b716a:corpus/knowledge/btrfs-scrub-record-r43.md`
| grep -n -A22 '^## SR6'`, 2026-10-26); identical to the working tree (no diff for that file between
717b716a and lane tip 7d0ed1c2).

Headline: the row's status-command claims verify line-for-line against S237/S240. One opening clause
overreaches (F1) and one implicit premise is unpinned and unmarked (F2); one capability phrase is
imprecise (F3). Two minor confirmations recorded (F4). The row does add grounded detail the lane did not
hold as verified text.

================================================================
F1 — "Whether a scrub is running comes only from the kernel" overreaches the CLI as a whole
================================================================
Row text: btrfs-scrub-record-r43.md:82 (opening clause of the SR6 Statement).

The clause is true for the STATUS command but false for the CLI as a whole. Two non-kernel authorities
are used elsewhere in the same file:
- The record file: cmd_scrub_start refuses a new start when the record shows an unfinished scrub —
  `if (!force && is_scrub_running_on_fs(&fi_args, di_args, past_scrubs))` (S237:1392); that record-based
  predicate returns 1 when a past record is neither `finished` nor `canceled` (S237:1169-1188). The kernel
  probe is consulted here only to set `force` and override the record gate (`if (!is_scrub_running_in_kernel(...))
  force = true;`, S237:1378-1379; comment "Check for stale information in the status file, ie. if it's
  canceled=0, finished=0 but no scrub is running", S237:1374-1377).
- The live progress socket: on connect success the start path errors out with "scrub already running"
  (S237:1474-1479, "/* ... yes, so scrub must be running. error out */").

Within cmd_scrub_status, the kernel-only claim holds exactly: `in_progress` is assigned once, from
`is_scrub_running_in_kernel` (S237:1946), and every print consumes that value — per-dev
`last_scrub->stats.in_progress = in_progress` (S237:1962) and fs-level `fs_stat.s.in_progress = in_progress`
(S237:1974); the only word source is `ss->in_progress ? "running" : ...` (S237:340-343). A grep for
assignments (`\.in_progress\s*=|in_progress\s*=`) finds no other assignment in scrub.c.

Exact narrower replacement (sentence 1 of the Statement):
  "In the status command, whether a scrub is running is decided only from the kernel: `btrfs scrub status`
   calls `is_scrub_running_in_kernel`, which issues `BTRFS_IOC_SCRUB_PROGRESS` once per device and answers 1
   only when a call returns 0; any failed call, whatever its errno, reads as not running. (Elsewhere the CLI
   also treats an unfinished record — `is_scrub_running_on_fs`, S237:1392 — and a live progress-socket
   connection — S237:1474-1476 — as evidence of a running scrub; this sentence covers status only.)"

================================================================
F2 — implicit premise "ioctl success ⇔ scrub running" is unpinned (missing [inference])
================================================================
The poll loop is grounded (S237:1197-1205: 1 only when `!ret`, else 0). The row's conclusion "a census
running as the user cannot learn from the kernel whether a scrub is in progress" (row line 87-88) needs only
the failure direction (EPERM -> nonzero -> not-running), which is fully grounded. But the opening authority
claim (F1) also requires the success direction — that a successful BTRFS_IOC_SCRUB_PROGRESS means a scrub is
actually running. That direction is NOT pinned: `btrfs_ioctl_scrub_progress` (S240:3126-3145) delegates to
`btrfs_scrub_progress` (S240:3139), whose body lives in fs/btrfs/scrub.c, which is absent from the frozen set
(the round-43 frozen src/ directory contains only ioctl.c, FETCH.txt, SHA256SUMS — `glob` of
.ufo/waves/round-43/frozen/**). Whether a successful call means an active scrub for that devid (vs. any
zero-value success) is unverifiable from S237/S240/S241. The row currently presents the kernel as the sole
authority without marking this chain element.

Smallest safe correction (pick one):
  (a) freeze fs/btrfs/scrub.c (`btrfs_scrub_progress`) beside ioctl.c and re-verify; or
  (b) append to sentence 1: " [inference: a successful SCRUB_PROGRESS call implies an active scrub; the
      kernel-side predicate `btrfs_scrub_progress` (ioctl.c:3139) is not in the pinned set]".

================================================================
F3 — "unless the caller has CAP_SYS_ADMIN" is imprecise about which namespace
================================================================
All three capability gates are `capable(CAP_SYS_ADMIN)` (S240:3132-3133 progress, S240:3072-3073 start,
S240:3120-3121 cancel). `capable()` resolves against the initial user namespace; a caller holding
CAP_SYS_ADMIN only inside a non-initial user namespace (e.g. an unshare'd root) still gets EPERM. `capable()`
is not defined in the frozen ioctl.c, so this is an [inference] from standard kernel semantics, not a pinned
line.

Narrower replacement: "unless the caller has CAP_SYS_ADMIN in the initial user namespace [inference:
`capable()` semantics are not in the pinned set]". The host reading (uid 1000, zero effective caps,
capture.txt:2) is unaffected.

================================================================
F4 — confirmations (no change proposed)
================================================================
- "issues BTRFS_IOC_SCRUB_PROGRESS once per device and answers 1 only when a call returns 0; any failed call,
  whatever its errno, reads as not running" — exact: S237:1197-1205 (`for (i = 0; i < max_devices; i++) …
  if (!ret) return 1; … return 0;`); call site passes `fi_args.num_devices` and `di_args` (S237:1946).
- "-EPERM before doing anything else" — the capable() check precedes `memdup_user` and any other work in all
  three handlers (S240:3132-3133, 3072-3073, 3120-3121); dispatch confirmed at S240:5582-5583.
- "the status command's in_progress is always 0" for the unprivileged caller — follows because every probe
  fails EPERM; no other assignment exists (F1's grep). No path lets a probe succeed without the capability.
- "never prints running" — S237:340-343 selects the word only from `ss->in_progress`; with a readable record
  the alternatives (aborted/finished/interrupted) print; with no record no status word prints at all
  (capture.txt:10 "no stats available"; host reading row line 110-112 matches capture.txt:2,6,8,10).

================================================================
Does SR6 add detail the lane did not already hold as verified text?
================================================================
grep of corpus/knowledge and SKILL.md (patterns EPERM|in_progress|CAP_SYS_ADMIN, 2026-10-26):
- SKILL.md: no match.
- corpus/knowledge: the only pre-existing text on this point is round-42 SC4's narrowing,
  btrfs-scrub-record-r42.md:196-198 — "the probe `BTRFS_IOC_SCRUB_PROGRESS` needs `CAP_SYS_ADMIN` (this host,
  uid 1000: `EPERM`), so a caller the ioctl refuses can read `interrupted` while a scrub runs [inference;
  reachable only with a readable record]". That row was grounded in a host errno alone (per r43 entry preamble,
  row lines 10-14).

SR6 therefore adds: (i) the progs-side control-flow ground that replaces the r42 [inference] (S237:1200-1205,
1946, 340-343); (ii) the kernel source pins for the capability gates and dispatch (S240:3072, 3120,
3132-3133, 5582); (iii) the start/cancel ioctl extension; (iv) the "never prints running" consequence.
All four are new verified text vs. the lane's prior state.

================================================================
Boundary note
================================================================
The clause "cannot learn from the kernel whether a scrub is in progress" (row lines 87-88) is scoped in the
row to this ioctl path; other unprivileged kernel-visible surfaces that might expose scrub state are not
surveyed here (out of pins). No claim about them is made.

Not done/not claimed: no scrub was started or canceled; no `btrfs device stats -z`; no privileged ioctl; no
kernel-side verification of `btrfs_scrub_progress` (not in the frozen set); no patch check of the Arch kernel
build (Limits section, row lines 126-128).
