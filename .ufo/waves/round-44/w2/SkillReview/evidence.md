# SkillReview-2 evidence receipt (R-2, SKILL review) — 2026-10-26

Method: anchors read via `git show 8eee79db608b5815c325a5af7cbfdeac50eda9f4:<path>` (lane HEAD was
3a1c6b5c958c4f289a8b12551f96d843877b700e with 11 untracked `.ufo/` entries; `git diff --stat
8eee79db..HEAD` over the four anchor files and `.ufo/` frozen paths empty → tip == HEAD for all
reviewed artifacts). SKILL.md sections read at HEAD (clean for SKILL.md). Read-only git only; no
writes outside this seat's report/receipt paths; no counters executed.

## Identities

- score-scrub-arm-r44.py @8eee79db sha256
  1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388 (= declaration, = SKILL:4205-4206)
- check-scrub-record-r44.py @8eee79db sha256
  c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059 (= declaration)
- Snapshot digests (sha256sum, working tree = tip): r42 scrub.c 48df2e2f…; r43 ioctl.c 7b3488f2…;
  r44 scrub.c f347931b…; r44 sysfs.c ce146120…; r44 btrfs-scrub@.timer 9a0b6cc2…; r44
  btrfs-scrub@.service eaa7af92…; r44 PKGBUILD 3b803e8b…; r44 hostcap capture.txt efb52388… —
  all equal the constants in check-scrub-record-r44.py SNAP/CAPTURE and the entry `source:` line.

## Census arm section (SKILL.md:4184-4213) vs census @tip

- Heading at SKILL.md:4184; surface sentence: probe_scrub_record census:1965; print order in `main`:
  probe_pacnew_arm → probe_storage_arm (`:3417`) → probe_scrub_record (`:3420`) → rollup (`:3423ff`);
  SCRUB_LINE format at `:2040` matches header line template at `:385-387`.
- Header contract paragraph "Round-44 addition (C1)" at census:384-408.
- Table rows → probe evidence: state `:2038-2039`; dir `:1994-2001`; records/tmp/sockets `:2002-2018`;
  unreadable (records+tmp only) `:2005,2012`; orphan under sysok `:2007,2013-2014`; limited nonzero
  single-decimal + detail pair `:1985-1990`; timers skip bare template + dirs `:2027-2034`; detail
  order (blocks then `detail+=$info`) `:2041-2042`; `local LC_ALL=C` `:1967`; no name echoed (detail
  tokens only) `:1987-1989,2004-2017`.
- `sysfs:not-directory` recorded-limit: probe `:2021`; selftest label census:3325.
- Frontier cites: PROVINCE.md:212-214 = "Still Frontier: the scrub record …" (sed 210-216);
  corpus/README.md:243 = Frontier bullet (sed 241-245). Exact.
- Counter command/predicate: docstring Usage + PREDICATE constant verbatim equal SKILL text; receipt
  `.ufo/waves/round-44/after/c1-after-8eee79db.jsonl` = receipt 1, revision 8eee79db, tool_revision
  1d2afffe, exit_code 0, cases 16, correct 16, identity_ok 1, live_agree 1, wired 1, same predicate
  string, channels_open [mount table, uid_map, script path /mnt/census-lib.sh].
- Selftest counts: `grep -cE "^[[:space:]]*check '"` = 145; `check_cli` = 3 (census:3333,3335,3337);
  total 148; labels ending `(R44-C1)` = 16 (census:3232,3239,3247,3254,3260,3266,3274,3281,3288,3297,
  3302,3307,3313,3319,3325,3330); `grep -c R44-C1` = 16 (no comment mentions).
- Wave-1 limit citations: C1CritEvasion.md:26 "**F1 — counter defect (live leg accepts a cached
  answer)…**"; C1CritChannels.md:13-20 rows supplementary groups / cwd+$PWD / stdin / statfs / ancestry
  (all "open, not declared"); w1/C1ExecLiveRead/strace-rev-live1.log exists.

## Rows section (SKILL.md:4214-4230) vs entry + snapshots @tip

- Entry `corpus/knowledge/btrfs-scrub-record-r44.md` (149 lines): source line 1 lists S237 S240 S242
  S243 S244 S245 with snapshot paths; verified-at line 2; Limits section items = the four SKILL
  Limits paraphrases.
- S242 scrub.c @r44: 3081 "bool readonly, bool is_dev_replace)"; 3147 "if (dev->scrub_ctx ||"; 3153
  "ret = -EINPROGRESS;"; 3159 "dev->scrub_ctx = sctx;" (attach precedes scrub_supers/
  scrub_enumerate_chunks in 3159-3222 body); 3222 "dev->scrub_ctx = NULL;" (after progress copy-back
  and before scrub_workers_put); 3321/3331/3333/3336 progress fn; 1380/1381 bwlimit read + zero
  return. All equal entry quotes; SKILL row cites 3147,3153,3159,3222 and 3331,3336 exact.
- S243 sysfs.c @r44: 72/74 BTRFS_ATTR_RW → __INIT_KOBJ_ATTR(…, 0644, …); 2028 sysfs_emit "%llu\n";
  2040 memparse; 2042 skip_spaces; 2044 -EINVAL; 2048 attribute declaration. SKILL row cites
  72,74,2028,2040,2042,2044 exact (entry adds 2048; SKILL omits it, no conflict).
- S240 ioctl.c @r43: 3132 "if (!capable(CAP_SYS_ADMIN))", 3133 "return -EPERM;", 3139 progress call,
  3141 "if (ret == 0 && copy_to_user(arg, sa, sizeof(*sa)))". SKILL cites 3132-3133,3139,3141 exact.
- S237 scrub.c @r42: 67-68 SCRUB_DATA_FILE/SCRUB_PROGRESS_SOCKET_PATH "/var/lib/btrfs/…" (cited by
  census header for the dir default); 421 ioctl(… BTRFS_IOC_SCRUB_CANCEL …); 969 "sp->stats.canceled =
  !!ret;"; 1293 "do_background = false;", 1295 "do_print = true;"; 1546 scrub_handle_sigint_child.
  SKILL row cites 421,969,1293,1295,1546 exact.
- S244 units @r44: timer:5 OnCalendar=monthly, :7 RandomizedDelaySec=1w, :8 Persistent=true,
  :11 WantedBy=timers.target; service:9 KillSignal=SIGINT, :10 ExecStart=/usr/bin/btrfs scrub start
  -B %f; PKGBUILD:100-101 install -Dm644 both units into /usr/lib/systemd/system. All equal entry
  quotes.
- dev-replace cite 701-703,1265-1268: unpinned by declaration in both SKILL row 1 and entry SR7 —
  consistent, unverifiable (no snapshot).
- F1 finding basis: SKILL:4217 "S244 (Arch btrfs-progs 7.1-1 units)" vs entry source line + counter
  SNAP keys `(S244, … | PKGBUILD)` + entry SR9 quotes S244 PKGBUILD:100-101.

## Adjacent checks (out of named scope, reported for the L1)

- Registry SKILL.md:4110 (scrub-arm-r44): CLI/predicate match score counter docstring; frozen sha
  matches; "candidate census sha256 fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c"
  = `git show ab8aae16:tools/tsukuroi-census.sh | sha256sum` (ab8aae16 = "round-44: C1 scrub-record
  census arm + 9 selftest cases…"). Correct.
- Registry SKILL.md:4111 (scrub-record-r44): CLI/predicate match check counter docstring verbatim;
  frozen sha matches.

Scratch /fast/scratch/hyaku/tsukuroi-r44/SkillReview removed after writing this receipt.
