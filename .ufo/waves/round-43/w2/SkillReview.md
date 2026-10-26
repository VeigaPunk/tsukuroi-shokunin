VERDICT: defect-found

Seat SkillReview (L2, tsukuroi round 43 / hyaku run 9, wave w2), item N-4 — review of SKILL.md sections
"Boot-input freshness under pipefail — round 43", "Scrub record re-grounded — round 43" and
"Gate and probe registry — round43 superseding current rows" at `8acf0b022586a0f3164c77659fb96ba5f90949b6`.
**All SKILL line numbers below are that revision** (blob extracted with `git show`, 4112 lines). Three low-severity
reference defects found (F1–F3); every substantive claim in the three sections checked out against the entry, the
receipts and the counters, including executed runs of both frozen counters at three revisions.

Method: blobs read via `git show 8acf0b0…:<path>` into `/fast/scratch/hyaku/tsukuroi-r43/SkillReview`; counters run
as scripts (never imported) against a `git clone --shared` fixture (remote removed; `git rev-parse --show-toplevel`
asserted equal to the fixture) with `--lane <fixture> --scratch <private dir>`; heavy C1 counter runs strictly
sequential (three runs, ~1–3 min each). No lane write outside this report and `w2/SkillReview/`; no lane git/jj
mutation; no host mutation; no tools installed (none needed). No `lsp` device in this seat's tool inventory —
recorded per reviewer rules; the subject is prose, evidence is text + execution.

## Findings

**F1 (low, mislabel) — SKILL.md:4009: the superseded `running` row is called "SC4's", but the round-42 table marks
it (SC3).** The supersession note reads "SC1 (the `_tmp` row), SC3 (the recording-disabled and "no record" rows) and
SC4's `running` row are superseded by the rows below". The row being superseded is `SKILL.md:3914`:
`| status `running` | the kernel answered `BTRFS_IOC_SCRUB_PROGRESS` for a device (SC3) | …` — it carries **(SC3)**,
and the r42 entry grounds the running mechanism in SC3 (`corpus/knowledge/btrfs-scrub-record-r42.md:70-71`
"Whether a scrub is running is asked from the kernel…", quote at :85 `scrub.c:1200`); SC4 (:100-101) mentions the
status word but its counted narrowing (:195-200 of the entry's Corrections) is about `interrupted`. The row is
rightly superseded (SC3 stands withdrawn), so only the SC attribution in the note is wrong. Severity low: the row is
identified unambiguously by its content; no counter conjunct depends on the label.

**F2 (low, dangling forward reference at the pinned revision) — SKILL.md:4007-4008: "the outcome is recorded in
`SCORECARD.md` 'Round 43 — measured outcome'" — no such section exists at 8acf0b0.** The SCORECARD blob at
8acf0b0 has exactly one round-43 heading, `## Round 43 — declaration` (SCORECARD.md:2648); a search for
"Round 43"/"measured outcome" finds no outcome section, and the worktree SCORECARD (read-only check,
2026-10-26 ~20:0xZ) does not have one yet either. The sentence is therefore presently false at the tip under test;
it can only become true at the w2 integration commit. If the outcome section is planned to land with that commit,
the reference should have been written as prospective (as the C2 section itself does for the verdicts: "judged by
the counted wave-2 reads"). Severity low: pointer, not substance.

**F3 (low, ambiguous/mis-numbered reference) — SKILL.md:3960-3961: "Routed defect R42-C1-COUNTER-AMEND item 5
(`corpus/lessons/round-42-verifier-spotcheck.md` §6)".** In that lesson's §6, R42-C1-COUNTER-AMEND is **item 4**
(:200-207); item 5 (:208-210) is R42-VERDICT-FORM, a C2 item. The boot-chain fail-open fix is the **5th bullet of
item 4** (:206). Under the natural reading ("§6 item 5") the citation names the wrong routed defect; under the
bullet reading it is correct. The defect name itself pinpoints the right item, so severity is low, but the number
contradicts the cited file's own numbering.

## Checked and accurate

### C1 section ("Boot-input freshness under pipefail — round 43", SKILL.md:3958-4000)

- Base code quote (:3966-3967): base blob `boot_inputs_newer` at `:463`, pipeline exactly
  `find <8 points> -newermt "@$btime" -print -quit 2>/dev/null | grep -q .` at base `:480-483`; the audit's
  freshness gate is base `:761` `[ "$newer" = 0 ]` inside the `booted=1` condition feeding BOOTED-OBSERVED. Fix
  helper `inputs_newer_than` at `:463-474` decides on `hit=$(find "$@" -newermt "@$epoch" -print -quit
  2>/dev/null)`; `boot_inputs_newer` calls it (`:494-496`) with the **same eight start points in the same order**
  as base `:480-482` (verified pairwise). The empty-btime branch is retained (`:486-489`) and, as the Limits
  paragraph (:3994-3999) says, is not exercised by the counter (counter `btime()` reads the real `/proc/stat`).
- Selftest cases: four `st_check 'R43-C1-…'` at `:1232-1239` with exactly the four names the section gives
  (:3983-3986). `git diff 717b716a 8acf0b02 -- tools/boot-chain-audit.sh` = 2 insertions, exactly the fourth case
  (`R43-C1-missing-start-point-silent`) — "one selftest case added at the round-43 integration commit" verified.
- Selftest totals — executed:
  - base 6951ead: counter receipt `selftest_line` = `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=45 failed=0`,
    `selftest_r43` 0;
  - 717b716: `PASS total=48 failed=0`, `selftest_r43` 3;
  - 8acf0b0: `PASS total=49 failed=0`, `selftest_r43` 4 (my run) — "45 → 48" at 717b716 and "49" at the
    integration commit (:3986-3988) confirmed by execution, not just receipts.
- The claimed kill (:3988-3990): applying the wave-1 mutant (c) (drop `2>/dev/null` from the find line at `:469`)
  to the 8acf0b0 script makes the selftest FAIL with exactly `FAIL R43-C1-missing-start-point-silent: expected [0]
  got [find: '…missing': No such file or directory …]` (rc=1); pristine rc=0 total=49. Receipts:
  `w2/SkillReview/selftest-{pristine-8acf0b0,mutant-drop-devnull}.out`; wave-1 corroboration
  `w1/C1MutSelftest.md:36` ("(c) drop `2>/dev/null` … **survives**" at 48 cases).
- Counter (:3991-3994): source predicate `tools/score-bootinputs-r43.py` PREDICATE (lines 64-66) is verbatim the
  section's "PASS iff `cases == 16 and correct == 16 and identity_ok == 1 and live_agree == 1 and selftest_pass == 1
  and selftest_r43 >= 2`"; exit 0 iff ok (:347-348); sha256 of the blob at 8acf0b0 =
  `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f` (matches :3991 and the registry cell).
  Executed runs (fixture, receipts in `w2/SkillReview/counter-c1-*.json`):
  - base 6951ead: exit 1, `correct` 8, wrong = the six `miss/etc/*-newer` + `multi-miss-deep-modules-newer` +
    `unreadable-dir-modules-newer` — the same eight ids as the section's base-receipt table (:3970-3979) and
    `before/c1-before.jsonl`;
  - 717b716: exit 0, correct 16, `selftest_r43` 3 — matches ":3994 `717b716` PASS (`correct` 16, `selftest_r43` 3)";
  - 8acf0b0: exit 0, correct 16, cases 16, identity_ok 1, live_agree 1, selftest total 49 — PASS.
- Controls (:3995-3998): `controls/battery-summary-c1.jsonl` reads `should_fail_accepted 0, control_accepted 1`;
  K0–K6 and K10 FAIL, K7 PASS (expect "recorded"), K8 (candidate) and K9 PASS — exactly the section's sentence.
  The mount-table/uid_map/`/mnt/bca-lib.sh` channel disclosure matches the counter source (`channels_open`,
  INNER setpriv/mount) and `w1/C1CritChannels.md` (:15-17).
- Limits (:3994-3999) verified against counter source: no unreadable-`/proc/stat` leg (counter dies on missing
  btime instead); a widened `btime - 1` survives by construction (case mtimes are `bt−[1h,30d]` / `bt+[60s,1d]`,
  never within 1 s of bt); the crypttab-membership gap is draw-dependent (`w1/C1MutFix.md:32` row (e): caught in
  4 of 8 draws, only when a draw makes it the newer input). "Gate plumbing reproduced by hand" —
  `w1/C1ExecHandRepro.md` exists with ns-leg/run-leg receipts.

### C2 section ("Scrub record re-grounded — round 43", SKILL.md:4002-4034)

- Entry identity (:4004-4006): `corpus/knowledge/btrfs-scrub-record-r43.md` has exactly sections `## SR1`, `## SR3`,
  `## SR6`, each with Statement/Quotes/Host reading; its `source:` line names S237/S240/S241 with the frozen
  digests; the pinned files on disk hash to the frozen values — scrub.c `48df2e2f…0801`, ioctl.c `7b3488f2…ba01`,
  capture `f7ecbe7c…c556` (all three blob==disk at 8acf0b0).
- **All 33 `**Quote.**` lines verified byte-exact at their cited lines** of the frozen snapshots (0 mismatches; all
  in-window per the counter: SR1 9/9, SR3 13/14 in-window, SR6 10/10, bad 0), and all `capture.txt:N` host refs
  resolve to non-empty lines. Spot content checks: `scrub_resumed_stats` sums exactly **13** `_SCRUB_SUM` fields,
  keeps `t_start`, sums durations, takes `last_physical`/`canceled`/`finished`/`t_resumed` from the new run
  (scrub.c:800-828) — the thirteen-counted-fields claim (entry SR3; SKILL:4014) is exact; the three `unlink` calls
  (scrub.c:1485, 1497, 1721) all name `sock_path`; the unconditional `warning(… "status recording disabled")`
  first-record/mkdir failures are at scrub.c:1335-1338 and 1506-1509; `-EPERM` without `capable(CAP_SYS_ADMIN)` at
  ioctl.c:3126-3133 (plus 3072, 3120). Capture S241 lines 2/6/7/8/10 carry uid 1000 + zero caps, `errno=EPERM`,
  `var_lib_btrfs absent`, `scrub_status_exit 0`, `no stats available` — the SKILL decision-table rows 1-6 and the
  SR6 host reading are grounded.
- Counter (:4022-4026): `tools/check-scrub-record-r43.py` PREDICATE (lines 47-49) verbatim matches the section's
  PASS-iff sentence; sha256 `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854` (blob at 8acf0b0).
  **Executed at 8acf0b0** (fixture; `w2/SkillReview/counter-c2-8acf0b0.json`): rows 3, quotes_ok 3, props_ok 3,
  host_ok 3, sources_ok 1, novelty_base_hits 0, pointer_ok 1, **verdicts_ok 0** (w2 verdicts not yet bound at this
  commit), verdict FAIL exit 1 — i.e. **every conjunct but `verdicts_ok` holds**, exactly as the frozen claims
  state for this tip. Binding mechanics (:4025-4027) match `bound()`/`declared_line()`: dispatch task + single
  results entry + anchored `ROW SR<n> VERDICT: <holds|partly|fails>` + committed report first line; residual
  `C2ResSR<n>` path and the unbound-counted-seat refusal are in the code as the kill rule describes.
- Recorded limits (:4028-4030): `w1/C2MutBinding.md` variants H/I/A show the padded/blank-line-prefixed acceptance
  and the unread `verdict` sibling field — confirmed in source (`declared_line` strips the first non-empty line;
  JSON path reads `verdict_line` only); `w1/C2RevCounter.md` D1 (wrapped host-ref lines unchecked) and D3
  (substring props) match the code at :277-282.
- Rejected wave-1 claim (:4031-4034): verified against the pinned source — `scrub_writev` (scrub.c:780-793,
  `return scrub_write_buf(fd, buf, ret);` at :792) formats and writes the devid itself, and the writer loop at
  scrub.c:866-869 calls it with `ret` 0; `w1/C2ExecTailRepro/run.log` parses `devid=7` back. The integrator's
  rejection of `w1/C2DraftCritSR3.md` F1 is correct.
- Supersession anchors (:4008-4012): r42 entry header **line 4** is the `superseded-in-part: round 43` line naming
  SC1/SC3 withdrawn and SR6; `## Corrections — round-42 wave 2` exists (:171); the SC5 narrowing wording
  ("only for a device that has a record line, and numerically only when the limit is above 1", entry :201-202)
  matches the SKILL's rendering (:4011-4012). (The "SC4's `running` row" label is F1 above.)

### Registry ("Gate and probe registry — round43 superseding current rows", SKILL.md:4036-4112)

- **Row-verbatim check (the item's `diff`)**: the round-36 section's table is byte-identical at base 6951ead and at
  8acf0b0 (74 section lines, 68 table lines). Diff of the two tables' rows at 8acf0b0 (receipt
  `w2/SkillReview/registry-table-diff.txt`, unified diff): **exactly 2 added rows, 0 removed, 0 changed**, retained
  rows in the same positions. The round-43 table is 66 round36 rows (names `child-env-allowlist-r36` …
  `size-invariance-r42` — the last row is `size-invariance-r42`, matching "rows through `size-invariance-r42`" at
  :4038-4039) plus the two new gate rows `bootinputs-r43` and `scrub-record-r43` (:4111-4112).
- New-row cells vs the tools: entry commands match the argparsers (`score-bootinputs-r43.py` requires
  `--revision --scratch`, optional `--lane`; `check-scrub-record-r43.py` requires `--revision`, optional
  `--lane/--sessions`); both verdict maps quote the predicates verbatim (0/1/2 exit map matches `return 0 if ok
  else 1` + `die(code=2)`); self-test cells ("none; … own `--selftest` is the measurement" / "no self-test mode")
  match; pinned sha256s match the blobs; write-scope cells match the code (private `--scratch` dir, rmtree in
  `finally` + SIGINT/SIGTERM handlers, `git show` reads, C2 writes nothing).
- Prose (:4037-4041): "wave-1 `C1ExecBootTools` F1: without them `check-registry-coverage.py` reads 66 of 68 tools
  registered" matches that receipt (exit 0/66-66-66 at base → exit 1/68 tools/66 rows/66 registered, two
  REGISTRY-ROW-MISSING at 717b716). The heading is the unique highest table of the required exact form
  (`…— round43 superseding current rows`); no round37–42 registry heading exists, so "every earlier table is
  historical" resolves to the round36 table, which is retained.

### Decision-table scope (item: "rows say no more than SR1/SR3/SR6")

The section's `| Observation | Reading | Action |` table (:4013-4021) has six rows citing exactly (SR1), (SR3),
(SR3), (SR3), (SR6), (S241) — no SC-row restatements, no other SR rows (none exist). Row 6 additionally leans on
the standing round-26 rule SH4 (SKILL.md:2368, "no scrub record … not a clean scrub … UNVERIFIED"), which is the
same attribution the superseded r42 row carried; within scope as the host-reading row.

## Not done

- Did not run the census selftest or the round-42 C1 counter (kill-rule regression checks belong to the kill-rule
  seats; one-heavy-counter discipline). `w1/C1ExecPriorCounters/` holds those receipts; I did not audit them.
- Did not re-derive the `corpus/SOURCES.md` rows for S237/S240/S241 by hand (the counter's `sources_ok 1` covers
  them; I verified the three files' sha256s directly).
- `verdicts_ok` is 0 at 8acf0b0 because wave-2 verdicts are not bound yet; I did not (and cannot) pre-judge the
  wave-2 seats' verdicts.

## Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/w2/SkillReview/`:
`counter-c1-8acf0b0.json`, `counter-c1-717b716.json`, `counter-c1-base-6951ead.json`, `counter-c2-8acf0b0.json`,
`registry-round36-table-at-8acf0b0.rows`, `registry-round43-table-at-8acf0b0.rows`,
`registry-table-diff.txt`, `selftest-pristine-8acf0b0.out`, `selftest-mutant-drop-devnull.out`.
Scratch `/fast/scratch/hyaku/tsukuroi-r43/SkillReview` removed after this write.
