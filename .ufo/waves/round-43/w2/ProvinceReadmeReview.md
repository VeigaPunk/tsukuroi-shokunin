VERDICT: supports

Seat ProvinceReadmeReview, Item N-5, round 43 w2. All note texts were read at the tip under test
8acf0b022586a0f3164c77659fb96ba5f90949b6 via `git show <rev>:<path>` into scratch copies (lane HEAD
64646d6e5749e0b5b6e458aa0753d39c47404e6b has moved past the tip under test; line numbers below are the
exported copies, byte-identical to the pinned blobs). Receipts: `.ufo/waves/round-43/w2/ProvinceReadmeReview/`
(receipts-commands.txt plus PROVINCE.tip/base.md, README.tip/base.md, r43-knowledge.md, r42-knowledge.md).

Locations at 8acf0b0: round-42 note `PROVINCE.md:239-244` (its last sentence `:243-244`); round-43 note
`PROVINCE.md:246-254`; Round-43 coverage note `corpus/README.md:416-425`.

# A. The PROVINCE round-43 note's correction of the round-42 note holds on all four points

The corrected round-42 sentence (`PROVINCE.md:243-244` at 8acf0b0): "`btrfs scrub status /` reads the record
unprivileged on this host (wave-1 `C2ExecHostRecheck`), so an arm needs no privilege for the record itself."

1. **"this host has no record, so `btrfs scrub status /` showed only the no-record path" — HOLDS.**
   - Host, this seat: `ls -la /var/lib/btrfs/` → "No such file or directory"; `stat -c '%A %a %U:%G %n'
     /var/lib/btrfs` → "cannot stat ... (os error 2)". The record directory does not exist here.
   - S241 `.ufo/waves/round-43/frozen/hostcap/capture.txt:7` "var_lib_btrfs absent"; `:8` "scrub_status_exit 0";
     `:10` "no stats available". The note's citation "S241 capture line 10" is exact. Exit 0 with "no stats
     available" exercises only the no-record path: the round-42 run demonstrated nothing about reading a record.
   - Falsifier pointer resolves: `.ufo/waves/round-43/w1/ConsiderMap.md:112` "**F-6/d — `PROVINCE.md:243-244` is
     an unrepaired overreach on the SC1 0600 fact.**" — same file:lines and same subject the note corrects.

2. **"a present record is created with open mode argument 0600" — HOLDS.**
   - S237 `.ufo/waves/round-42/frozen/src/scrub.c:483` `fd = open(datafile, m, 0600);` (write path passes
     `O_WRONLY|O_CREAT`, `scrub.c:517`). "Mode argument" is exact C semantics — the third open(2) argument; the
     round-42 note had asserted the 0600 fact without this grounding (its SC1 was withdrawn, r42 entry line 4).

3. **"every open takes `flock(LOCK_EX|LOCK_NB)`" — HOLDS.**
   - `scrub.c:487` `ret = flock(fd, LOCK_EX|LOCK_NB);` sits inside `scrub_open_file` (`scrub.c:478`), the only
     function that opens the record; both wrappers route through it — read `O_RDONLY` (`:505`) and write
     `O_WRONLY|O_CREAT` (`:517`) — and the only record open call sites in the pinned file are `:917` (writer),
     `:1361` and `:1930` (status reads). No open of `SCRUB_DATA_FILE` (`:67`) bypasses the flock.

4. **"[inference: a record written by a root scrub under the usual umask is root-only]" — properly labeled and
   correctly calibrated.**
   - No pinned source states root-only-ness outright; it follows from the mode argument 0600 (`scrub.c:483`,
     `:517`) plus the writer needing `CAP_SYS_ADMIN` (S240 `.ufo/waves/round-43/frozen/src/ioctl.c:3132-3133`
     for `BTRFS_IOC_SCRUB_PROGRESS`; same gate on scrub start/cancel at `ioctl.c:3072-3074`, `:3120-3121`).
     Inference labeling is the honest strength. (0600 sets no group/other bits, so any umask keeps it root-only;
     the note's "usual umask" qualifier is conservative, not wrong.)
   - The note's sibling clauses also check: "see the directory" — the directory is created with
     `mkdir(path, 0777)` subject to umask (`scrub.c:1160`); "read `scrub_speed_max`" — the limit is read from
     sysfs `/sys/fs/btrfs/<fsid>/devinfo/<devid>/scrub_speed_max` (`scrub.c:1214-1216`), not from the record, so
     an unprivileged arm can read it while "cannot be assumed to parse the record" stays true; "cannot read the
     running state at all" — `ioctl.c:3126-3133` returns `-EPERM` before anything else without `CAP_SYS_ADMIN`,
     and the host agrees (`capture.txt:6` "scrub_progress_ioctl devid=1 errno=EPERM (1)", uid 1000 with empty
     effective caps, `capture.txt:2`).

# B. The README round-43 coverage note claims no ground the round did not move

Round-43 non-`.ufo` ground (`git diff --name-status 6951ead90566b2d74f7c45b4efca29246badad64
8acf0b022586a0f3164c77659fb96ba5f90949b6`): M PROVINCE.md, M SCORECARD.md, M SKILL.md, M corpus/README.md,
M corpus/SOURCES.md, M corpus/knowledge/btrfs-scrub-record-r42.md, A corpus/knowledge/btrfs-scrub-record-r43.md,
A corpus/lessons/round-43.md, M tools/boot-chain-audit.sh, A tools/check-scrub-record-r43.py,
A tools/score-bootinputs-r43.py.

- **Row claims match the delivered entry.** `corpus/README.md:417-419` (row) describes SR1/SR3/SR6; the delivered
  `corpus/knowledge/btrfs-scrub-record-r43.md` contains exactly them, source-pinned: SR1 write discipline —
  `_tmp` opened without `O_TRUNC` (`scrub.c:517`), renamed only after a successful write (`:534`, write/rename
  sequence `:917/:922/:925`), never unlinked (the file's three `unlink` calls all name the progress socket,
  `:1485/:1497/:1721`), trailing-bytes consequence explicitly marked "[inference … not observed on this host]";
  SR3 — `scrub_resumed_stats` (`:864`), `do_print` (`:1249/:1295/:1333`) set by `-B` (`case 'B'` at `:1292`);
  SR6 — `BTRFS_IOC_SCRUB_PROGRESS` needs `CAP_SYS_ADMIN` (`ioctl.c:3126-3133`, dispatch `:5582-5583`).
- **Sources/evidence column is real and pinned.** S237/S240/S241 hashes verified by this seat:
  scrub.c 48df2e2f…0801, ioctl.c 7b3488f2…ba01, capture.txt f7ecbe7c…c556 — matching the frozen claims; the
  counter `tools/check-scrub-record-r43.py` was added by the round.
- **"SC1 and SC3 stand withdrawn and SC4/SC5 are narrowed (its header line 4 and 'Corrections — round-42 wave 2')"**
  is exact: r42 entry line 4 "superseded-in-part: round 43 — SC1 and SC3 below stand withdrawn (see "Corrections —
  round-42 wave 2") …" and line 171 "## Corrections — round-42 wave 2 (appended 2026-10-26 after the counted
  reads; these carry no counted verdict)".
- **"it enters no new coverage-map ground" holds.** Both edited docs are append-only (PROVINCE.md +10/−0;
  corpus/README.md +11/−0 between base and tip); SKILL.md's 156 inserted lines contain zero additions matching
  frontier/coverage-map/core-now wording (grep count 0), i.e. round bookkeeping only; no census arm was added
  (tools/tsukuroi-census.sh is absent from the round's diff), so the scrub record stays Frontier as claimed.
- **Calibration is right.** The note claims no C1 ground (that lives in SCORECARD, as in round 42), no counter
  PASS, and no counted verdict seats — consistent with the wave state in which `verdicts_ok` is the one C2
  counter conjunct not yet true at the tip under test.

# Residual risk / not done

- I did not re-run `tools/check-scrub-record-r43.py`, re-derive SR3's 13-field resume arithmetic, or audit the
  r42 "Corrections" section's narrowed SC4/SC5 text line by line; the entry, its counter and the counted C2
  seats own those, outside item N-5.
- The root-only reading remains an inference from source (mode 0600 + capability gating); no record exists on
  this host to observe empirically — the note and the entry both mark it as such.
- F-6/d was verified to exist and to describe the same overreach at the same lines (`ConsiderMap.md:112`); the
  whole ConsiderMap seat was not re-audited.
- No tool installs were needed; nothing was installed or upgraded by this seat.
