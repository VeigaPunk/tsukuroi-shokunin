VERDICT: defect-found

Seat C2DraftRevAll — item C2-15, wave-1 pre-review of the whole entry
`corpus/knowledge/btrfs-scrub-record-r44.md` @ 7e081698d4fc3c4ea944884fd093058de9909de1.
No `ROW … VERDICT` line (wave-1 pre-review). No falsifier found; findings are narrowings
(fact-vs-inference discipline and two over-broad triage phrasings), none blocking.

Entry line numbers below are the frozen bytes: `git -C <lane> diff 7e081698 --
corpus/knowledge/btrfs-scrub-record-r44.md | wc -l` printed `0` (worktree identical to the
revision; lane tip ff2c264a7f7b3fe4aec694ded959566f8f5b7d33).

## Machine checks observed (all pass)

- `python3 tools/check-knowledge-header.py --revision 7e081698…` → exit 0, `"finding_count": 0`,
  r44 entry row `"problems": []` (receipt `w1/C2DraftRevAll/header-checker.out`).
- `python3 tools/check-scrub-record-r44.py --revision 7e081698…` → exit 0; aggregates
  `rows=3 quotes_ok=3 props_ok=3 host_ok=3 sources_ok=1 pointer_ok=1 novelty_base_hits=0`;
  `verdicts_ok=0` with all three verdicts `null` — expected, verdicts bind only in wave 2
  (receipt `w1/C2DraftRevAll/c2-counter.out`).
- `sha256sum -c SHA256SUMS` in `.ufo/waves/round-44/frozen/src/` → all five files `OK`.
- S237/S240 carried snapshots are the same bytes the earlier rounds pinned:
  round-42 `scrub.c` sha256 `48df2e2f…0801` (= r43 entry line 1's pin), round-43 `ioctl.c`
  sha256 `7b3488f2…ba01` (= `corpus/SOURCES.md:249` S240 row).
- `capture.txt` sha256 `efb52388…4900` matches the header (entry :1-2) and SOURCES S245
  (`corpus/SOURCES.md:254`); file mtime `2026-10-26 20:53:22 -0300` = the header's
  `capture 2026-10-26T23:53:22Z` (host TZ −03). Re-ran
  `bash .ufo/waves/round-44/frozen/hostcap/capture.sh <scratch file>`: `diff` against the
  pinned capture shows only `1c1` (the timestamp line); every reading line reproduces.
- Header facts check out: `source:` names S237 S240 S242 S243 S244 S245, all present as
  SOURCES rows (`corpus/SOURCES.md:246-254`); `verified-at` peeled commits match r43's
  (r43 :2) and the FETCH.txt tags (`.ufo/waves/round-44/frozen/src/FETCH.txt`).

## Quotes and semantics verified against the pinned sources

All 20 quoted lines were read at their cited lines and match: S242 scrub.c 3081, 3147, 3153,
3159, 3222, 3321, 3331, 3333, 3336, 1380, 1381; S240 ioctl.c 3139, 3141; S243 sysfs.c 72, 74,
2028, 2040, 2042, 2044, 2048; S244 PKGBUILD 100-101, timer 5/7/8/11, service 9/10; S237
scrub.c 421, 969, 1293, 1295, 1546. Semantic checks beyond the quotes:

- `dev->scrub_ctx` has exactly two writers in S242 (attach 3159, detach 3222; grep for
  `scrub_ctx =` found only these plus the readers at 3304/3331) — supports "carries a scrub
  context exactly while btrfs_scrub_dev runs on it" (entry :17).
- `btrfs_scrub_progress` (S242:3321-3337): lookup under `device_list_mutex`, `memcpy` of
  `sctx->stat`, `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` — the success-direction
  sentence (entry :22-25) is exact.
- ioctl handler (S240:3126-3145): `CAP_SYS_ADMIN` gate, `ret = btrfs_scrub_progress(...)`,
  copy_to_user only when `ret == 0`, returns `ret` — entry :24-26 exact.
- SR8 show/store (S243:2025-2049): `%llu\n`, `memparse` at 2040, own comment at 2041
  ("There could be trailing '\n'…"), `skip_spaces` 2042, `-EINVAL` 2043-2044 — entry :58-62
  matches the pinned bytes.
- Throttle (S242:1370-1400): comment "bandwidth-limit based, the timeslice is 1 second",
  `if (bwlimit == 0) return;`, per-epoch cap `div_u64(bwlimit, div)` — supports "reads the
  value as bytes per second and returns at once when it is 0" (entry :62).
- SR9: `-B` sets `do_background=false; do_wait=true; do_print=true` (S237:1293-1295); the
  foreground path calls `scrub_handle_sigint_child(fdmnt)` (S237:1546), which installs
  `scrub_sigint_record_progress` (S237:434-441), whose body issues
  `ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL)` (S237:421); `sp->stats.canceled = !!ret`
  with `ret` from the per-device `BTRFS_IOC_SCRUB` ioctl (S237:962, 969) — entry :92-96
  matches. Unit texts and PKGBUILD install lines match; pinned unit digests equal the
  installed ones (capture.txt:7-8 vs sha256sum of the frozen files).
- Host reading reproduces (see machine checks above); `wants_btrfs_scrub_instances 0`,
  `is_enabled_btrfs-scrub@-.timer disabled`, `var_lib_btrfs absent` all re-observed.

## Contradiction sweep — none found

- vs r43 SR6: complementary, not contradictory. r43 :102-108 (unprivileged never sees
  `running`) is completed by SR7's privileged direction; SR7 :24 explicitly re-anchors the
  SR6 gate. r43 :4 (`extended-by`) names exactly these three rows in this file.
- vs r43 SR3: SR9's "the later recording failures of SR3 are printed into the service's
  output" (:93-94) matches r43 :64-65 (`do_print` gate) and S237:1295.
- vs r43 SR1: SR9's "recorded with `canceled` set … `btrfs scrub resume` later takes up"
  (:95-96) is consistent with SR1's write discipline and SR3's resumed-source rule.
- vs the census header (`tools/tsukuroi-census.sh:384-410` @7e081698): states NONE/RECORDED/
  BLOCKED, `limited=` bytes/s with 0 = no limit, `timers=` counting only
  `btrfs-scrub@<instance>.timer` links — all consistent with SR8/SR9; the header cites only
  SR1 and SR6 (:392-393), never SR7 — see F7.
- Scope line (:7) "`PROVINCE.md` Frontier" is accurate at this revision: PROVINCE.md @7e081698
  still keeps the scrub record Frontier (:212, :239, :246-247) and has no round-44 promotion
  note (the round-38 promotion pattern is at :199). The declared C1 "Frontier → Core" is a
  round-close promotion step, not an entry defect — flagging so wave 2 does not route it here.

## Findings by severity (each with exact proposed text below)

- F1 medium — SR8 states unpinned `memparse` semantics as fact (entry :60).
- F2 medium — SR8 host reading attributes the captured fsid to the root filesystem; S245
  does not pin that attribution (entry :83). Fact re-verified true live today; pin missing.
- F3 medium — SR9's SIGINT→canceled-record chain lacks the kernel-side pin that a cancel
  makes the running scrub's ioctl fail; the link is pinnable in S242 but unquoted.
- F4 low — SR7 restates its own marked replace-side inference unhedged (:27) and cites
  line numbers of a file that is not pinned anywhere in the round (:20-21).
- F5 low — triage bullet 3 over-broad: "A monthly scrub exists only if an instance of the
  packaged timer is enabled" (:134).
- F6 low — triage bullet 2 over-claims causation: "A slow scrub with `scrub_speed_max`
  nonzero is the configured limit at work" (:132).
- F7 low — intro says the census arm "relies on" SR7 (:10); the arm never reads the running
  state (unprivileged; header cites SR1/SR6 only, census.sh:392-393).
- F8 low — the systemd stop-signal inference is asserted inline in SR9 (:95) and in triage
  (:135) while its hedge lives only in Limits (:144-145); the entry's own convention (SR7
  :20) is an inline bracket.
- F9 info — `recheck` (:3) re-verifies only the round-44 frozen set; carried S237/S240 are
  re-checkable only via the round-42/43 FETCH.txt+SHA256SUMS, which r43's own recheck line
  named (r43 :3) but r44's drops.
- O1 optional — SR7 :18 names only the first `-EINPROGRESS` disjunct; S242:3147-3152 also
  refuses a non-replace scrub while a replace is ongoing.
- O2 optional — "bytes per second" (:62) is grounded only by paraphrase; the grounding
  comment is quvable at S242:1370-1372.

## Exact proposed narrowings

N1 (F1, entry :60) — replace:
  "Writing parses the text with `memparse`, so a size suffix such as `K`, `M` or `G` is
  accepted, skips trailing whitespace including the newline, and rejects anything else
  after the number with `-EINVAL`."
with:
  "Writing parses the text with `memparse` [inference: `memparse`'s size-suffix table —
  `K`, `M`, `G` — is defined outside the pinned files], skips trailing whitespace including
  the newline (sysfs.c:2041's own comment: "There could be trailing '\n'"), and rejects
  anything else after the number with `-EINVAL`."
Ground: `memparse` appears in the frozen set only as the call S243 sysfs.c:2040; no pinned
file defines it.

N2 (F2, entry :83) — replace:
  "**Host reading.** The root filesystem's only device (devid 1) has `scrub_speed_max` mode
  644, owner root, value 0: no limit (capture.txt:4), read as uid 1000 with no effective
  capabilities (capture.txt:1)."
with:
  "**Host reading.** The only btrfs sysfs shows on this host (fsid
  `1d02a454-c549-4a35-b567-89d60902af8e`, devid 1 — `findmnt -no UUID /` names the same
  fsid for `/`; the attribution is not in the pinned capture) has `scrub_speed_max` mode
  644, owner root, value 0: no limit (capture.txt:4), read as uid 1000 with no effective
  capabilities (capture.txt:1)."
Ground: capture.sh enumerates all `/sys/fs/btrfs/*/devinfo/*/scrub_speed_max` and never
ties the fsid to `/` (`.ufo/waves/round-44/frozen/hostcap/capture.sh`, the `for f in` loop);
capture.txt:4 shows exactly that one fsid. Re-verified live 2026-10-27T00:2xZ:
`findmnt -no UUID,FSTYPE /` → `1d02a454-c549-4a35-b567-89d60902af8e btrfs`; `ls
/sys/fs/btrfs/` → that fsid plus `features` only.

N3 (F3, SR9) — add after the `S237` scrub.c:969 quote:
  "**Quote.** `S242` scrub.c:3285: "atomic_inc(&fs_info->scrub_cancel_req);""
  "**Quote.** `S242` scrub.c:2083: "return -ECANCELED;""
and in the statement (:95) replace "the foreground start installs a SIGINT handler that
issues `BTRFS_IOC_SCRUB_CANCEL`, so a SIGINT sent to it" with:
  "the foreground start installs a SIGINT handler that issues `BTRFS_IOC_SCRUB_CANCEL` —
  the kernel cancel path raises `scrub_cancel_req`, which makes the running scrub end with
  `-ECANCELED` (S242 scrub.c:3281-3293, 2077-2083), the value the start ioctl returns — so
  a SIGINT sent to it".
Ground: S242:3281 `int btrfs_scrub_cancel(struct btrfs_fs_info *fs_info)`, :3285
`atomic_inc(&fs_info->scrub_cancel_req);`, :2077-2083 `should_cancel_scrub` returning
`-ECANCELED` on cancel requests; the progs side then records `canceled = !!ret`
(S237:969). This closes the chain the entry currently leaves to reader inference between
the cancel ioctl and the nonzero scrub return.

N4 (F4, entry :20-21 and :27) — replace:
  "[inference for the replace side: its caller is in `fs/btrfs/dev-replace.c`, opened this
  round at v7.2.11 lines 701-703 and 1265-1267 but not pinned]."
with:
  "[inference for the replace side: its caller is in `fs/btrfs/dev-replace.c`, not pinned
  this round, so no line numbers are citable from the frozen set]."
and replace "answers 1 exactly when some device it asks about is being scrubbed, or is the
source of a running replace, at that moment" with:
  "answers 1 exactly when some device it asks about is being scrubbed, or — replace side as
  marked above — is the source of a running replace, at that moment".
Ground: `dev-replace.c` is not in `.ufo/waves/round-44/frozen/src/` (directory holds
scrub.c, sysfs.c, PKGBUILD, the two units, FETCH.txt, SHA256SUMS only), so the cited
701-703/1265-1267 cannot be re-verified by the entry's own recheck procedure.

N5 (F5, entry :134) — replace:
  "- A monthly scrub exists only if an instance of the packaged timer is enabled (SR9); the
  census counts the `timers.target.wants` links (`timers=`)."
with:
  "- The packaged monthly scrub fires only if an instance of `btrfs-scrub@.timer` is
  enabled (SR9); a self-arranged cron or timer is invisible to it. The census counts the
  `timers.target.wants` links (`timers=`)."
Ground: SR9 pins only the packaged timer's calendar and WantedBy (S244 timer:5,11);
nothing in the entry excludes other schedulers, so the unhedged "only if" is broader than
its evidence.

N6 (F6, entry :132) — replace:
  "- A slow scrub with `scrub_speed_max` nonzero is the configured limit at work (SR8); 0
  means none. The limit is root's to set; the census only reports it (`limited=`)."
with:
  "- Any nonzero `scrub_speed_max` throttles a scrub to at most that many bytes per second
  (SR8); 0 means no throttle, so a slow scrub with limit 0 is slow for another reason. The
  limit is root's to set; the census only reports it (`limited=`)."
Ground: S242:1370-1372 (comment "bandwidth-limit based, the timeslice is 1 second"),
:1381-1382 (`if (bwlimit == 0) return;`), :1388-1390 (per-epoch cap). A nonzero limit does
not by itself explain an observed slowness; the grounded claim is the throttling bound.

N7 (F7, entry :10) — replace:
  "This entry adds three rows the round-44 census arm (`SCRUB btrfs-scrub-record …`,
  `tools/tsukuroi-census.sh`) relies on: SR7, the success direction of the scrub-progress
  ioctl; SR8, …"
with:
  "This entry adds three rows that ground what the round-44 census arm
  (`SCRUB btrfs-scrub-record …`, `tools/tsukuroi-census.sh`) reads and refuses to read:
  SR7, the success direction of the scrub-progress ioctl — the running state the
  unprivileged arm never reads (SR6); SR8, …"
Ground: the census header states "No privilege, no ioctl" (census.sh:409) and cites only
SR1/SR6 (census.sh:392-393); nothing in the arm consumes SR7.

N8 (F8, entry :95 and :135) — inline-mark the systemd inference, matching the Limits hedge
(:144-145):
  :95 — "so a SIGINT sent to it (the service's stop signal [inference: systemd.kill(5), see
  Limits]) cancels the running scrub, …"
  :135 — "Stopping a running scrub service sends SIGINT (see Limits) and so cancels the
  scrub and leaves a canceled, resumable record (SR9, SR3)."

N9 (F9, entry :3) — after "compare `sha256sum` with its `SHA256SUMS`" insert:
  "; re-verify the carried S237/S240 snapshots the same way against
  `.ufo/waves/round-42/frozen/src/` and `.ufo/waves/round-43/frozen/src/` (each has
  `FETCH.txt` and `SHA256SUMS`)".
Ground: r44's FETCH.txt lists only the five round-44 files; S237/S240 are in the entry's
source list (:1) and are pinned by the older rounds' SUMS, exactly as r43's recheck line
did for its carried sources (r43 :3).

O1/O2 — optional, take or leave:
  O1: extend entry :18 to "…refuses with `-EINPROGRESS` when `dev->scrub_ctx` is already
  set (or, for a non-replace scrub, while a device replace is ongoing), attaches …"
  (S242:3147-3152).
  O2: add "**Quote.** `S242` scrub.c:1371: "bandwidth-limit based, the timeslice is 1"
  (comment at S242:1370-1372) so the bytes-per-second claim is quoted, not paraphrased."

## Residual risk and verification gaps

- No privileged probe was run (forbidden for this seat): SR7's privileged direction remains
  source-only, exactly as the entry declares (:40-41, :108-109).
- `memparse` suffix behavior (N1) and systemd's stop-signal behavior (N8) were not tested
  live (sysfs writes and unit changes are forbidden); both stay inference unless pinned.
- I did not re-fetch the upstream URLs (recheck is an on-release step); I verified internal
  digest stability (round-42/43 pins identical to today's bytes) instead.
- dev-replace.c lines 701-703/1265-1267 remain unverifiable from the frozen set (N4).
- The C2 counter's counted verdicts are wave-2 bindings (`verdicts_ok=0`, all null here) —
  out of scope for this seat by instruction.
- C1 counter, selftest and control batteries were not run by this seat (C1's receipts at
  `.ufo/waves/round-44/before/` and `after/c1-after-ab8aae1.jsonl` cover them).

Receipts: `w1/C2DraftRevAll/header-checker.out`, `w1/C2DraftRevAll/c2-counter.out`,
`w1/C2DraftRevAll/recapture.txt` (re-run capture; differs from the pinned file in the
timestamp line only). Scratch `/fast/scratch/hyaku/tsukuroi-r44/C2DraftRevAll/` removed
after writing.
