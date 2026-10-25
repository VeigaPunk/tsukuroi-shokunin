# Scribe1145 — Round 37 draft, item 1/8 (claim / assimilation / lesson surface)

seat: scribe, tsukuroi lane round 37 attempt 1, wave w1, draft item 1/8
axes: depth, quality, frontier   ·   milestone: draft evidence only
date: 2026-10-25 (all URLs below opened on this date; UTC not re-derived)
lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
lane tip at write time: `0e5f70fadba12bc9bbb9db564c2262c2c0194535` (git rev-parse HEAD, read-only)
tooling: none installed; `python3` 3.14 and `curl` already present (RULES.md channel rule not engaged). No pacman, no git/jj writes, no host changes.

This is a standalone draft for the round-37 evidence/lesson surface. It is not
an outcome claim, and it does not edit the lane. Claim boundaries from the
round-37 declaration (`SCORECARD.md`) are preserved; each item is tagged
`[obs]` (observed this round), `[inf]` (inference from observed bytes) or
`[unk]` (not established here). Source-row proposals appear only for sources
opened this round, with URL, access date and a located quote ≤ 25 words.

---

## 1. Claim surface (round-37 declaration, SCORECARD.md:1857-1974)

Preserved boundaries, as declared:

- **C1 — operability** (`SCORECARD.md:1867-1904`): the round-36 probe's
  VERSION-8 redesign (`tools/probe-child-env-allowlist-r37.py`) replaces VERSION 7
  and repairs four routed defects: S1 direct full-battery clone crash
  (`RuntimeError: cannot create local master branch`, probe line 499), S3
  livefive do-nothing vacuity, S4 `os.get_exec_path()` ambient-PATH invisibility,
  and the parameter-named-`env` source-rule false positive. Frozen predicate:
  summary `leaking` == 0, `leaking_pairs` == [], `harness_errors` == [],
  `predicate_label` == `leaking`, exit 0. Kill rule: any frozen-probe variant
  skipping any of the four fixes reading `leaking` 0 on livefive kills C1.
  Sourced-claim rows named in the declaration: S200-strace, S201-probe.
- **C2 — depth** (`SCORECARD.md:1906-1919`): the round-36 journalctl-v262 note
  becomes correction-complete per the closure's routed list: 15 not 16 predicate
  terms; `-F` truncation vs unchanged `-N` output under `-n`; action-override
  classification. Counter: `tools/check-journalctl-v262-corrections.py
  --revision <REV>` (before at base = exit 1; after = exit 0).
- **C3 — calibration** (`SCORECARD.md:1950-1974`, pre-freeze correction): the
  existing checker `tools/check-self-assessment.py` is unchanged; the claim is
  `mismatches == 0 && checked == 27 && exit == 0` at the measured round-37 tip.
  Before at base `564db0b614` = 5 mismatches, FAIL, exit 1. No-new-ledger.

### 1.1 Observed claim-state readings this round

| item | observed | tag |
|---|---|---|
| C3 base receipt | `.ufo/waves/round-37/before/c3-before.json`: revision `564db0b614b2914de5452f9ebd537a0653ae1de5`, `checked: 27`, `mismatches: 5`, `status: FAIL`, `reference_lines: 350`; `before/c3-before-exit.txt` = `exit=1` | [obs] |
| C3 at `d06cedb` (correction commit) | `.ufo/waves/round-37/after-c3-d06ced.json`: `checked: 27`, `mismatches: 2`, FAIL; mismatching checks K17 (`host-census-gate row names only repository paths that exist at the revision`; stated 3 paths, observed 2) and K18 (`root-metadata-observer`; stated 3, observed 1) | [obs] |
| C3 at `ee36f9e` | `.ufo/waves/round-37/after-c3-ee36f9.json`: `checked: 27`, `mismatches: 1`, FAIL | [obs] |
| C3 at `5124bf3` | `.ufo/waves/round-37/after-c3-5124bf.json`: `status: CANNOT_EVALUATE`, error `missing capability row` / detail `sources-registry`, `checked: 0` — the checker could not evaluate at this intermediate revision | [obs] |
| C3 at tip `0e5f70f` | `.ufo/waves/round-37/after-c3-0e5f70.json`: `checked: 27`, `mismatches: 0`, `status: PASS`, `reference_lines: 422` — the declared C3 after-state is reached at the current tip | [obs] |
| C1 catalog | `.ufo/waves/round-36/w2/W2RevCounter/W2RevCounter.md` S1-S8: S1 crash reproduced (clone already has `master`), S3 skip-work variant reads `leaking 0` with `harness_errors []`, S4 source+untraced silent on ambient-PATH copy, parameter-`env` flag at `score-census-handoff-r32.py:489` ("bound by arg") | [obs] |
| C2 findings | `.ufo/waves/round-36/w2/W2RevC2/findings.json`: B1 (blocking) "-n allowed-silent third state missing from the decision table" — evidence `ext_lines1_F argv='journalctl --no-pager -n 1 -F PRIORITY' exit=0 stdout_bytes=2 stdout_head=['5']` vs `core_plain stdout_bytes=12`, `ext_lines1_N stdout_bytes=2882 == ext_plain_N 2882`, mechanism "truncation"; M1 (minor) "predicate is 15 terms, not 16" — `field_list_has_scope_options()` has 15 OR terms (journalctl-filter.v262.c:27-41), table has 15 limiter rows; M8 (minor) "action precedence undocumented; four cited cells never execute the named action" — last `arg_action` assignment wins, `--sync` is a write request the tested ordering bypasses | [obs] |
| C2 note current state | `corpus/knowledge/journalctl-v262-field-filter-r36.md:126` still says "the 16-term limiting-option predicate"; decision table rows :40-43 show `-n` under "not a limiter → WORK" with no third state; no action-precedence row. The three C2 corrections are not yet applied at tip | [obs] |
| LOG stamp typo | `LOG.md:1379` still carries `2026-10-24T04:4043Z` (invalid time); `LOG.md:1371` carries `03:5xZ` placeholder. Matches round-36 verifier spot-check §6 item 3; the C2 declaration says the LOG stamp typo "is repaired by a LOG append" — un-repaired at tip | [obs] |
| C1/C2 base actors | round-36 verifier spot-check `corpus/lessons/round-36-verifier-spotcheck.md` §2 C1 (S1 crash reproduced by closure), §6 routed defects 1-2 (V8 items; C2 corrections) — the direct source of the round-37 C1/C2 targets | [obs] |

`[inf]`: the C3 mismatch trajectory (5 → 2 → 1 → 0 with one cannot-evaluate)
is consistent with the append-only correction commits `d06cedb` (self-assessment
counts), `ee36f9e` (capability pointers), `5124bf3` (census case count) and
`0e5f70f` (capability table) on top of base `89bb8af`; the checker runs themselves
are observed receipts, not re-derived here.
- `merge/tsukuroi/SOURCES.append.md` carries the staged row set S200–S346
  (11-column registry schema); `MERGE-REPORT.md` records 147 proposed rows
  accepted, 0 refused, lane registry 199 rows, first staged id S200.

---

## 2. Assimilation surface (errno discrimination theme)

Declared (`SCORECARD.md:1936-1941`): ONE theme — errno discrimination — with
THREE package entries admitted from `merge/tsukuroi/`:
`errno-name-discrimination-r25.md`, `mount-errno-contract-r26.md`,
`errno-contract-variance-r37.md`; rows S204/S205/S214/S220/S279–S282/S286/S287
appended (transformed to fleet schema, census-validated, collision-guard
proven) with re-grounded Gate quotes; quarantine slice (12 data rows) hand-checked.

Observed package state:

- The three staged entries exist at
  `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/`
  (read-only; opened this round): `errno-name-discrimination-r25.md`,
  `mount-errno-contract-r26.md`, `errno-contract-variance-r37.md`.
- `merge/tsukuroi/SOURCES.append.md` carries the staged row set S200–S346
  (11-column registry schema); `MERGЕ-REPORT.md` records 147 proposed rows
  accepted, 0 refused, lane registry 199 rows, first staged id S200.
- used-by pointer correction observed in `MERGE-REPORT.md:104-112`: S279–S282
  and S286/S287 moved from `errno-contract-variance-r33.md` to
  `errno-contract-variance-r37.md` at packaging time (the "re-grounded Gate
  quotes" item).
- `.ufo/waves/round-37/assimilation/reg-ids` = S001–S199 (199 rows);
  `staged-ids` = S200–S346 (147 rows); `collisions` empty (0 bytes).

### 2.1 Source rows proposed by this draft (opened this round)

Each row below is proposed only because its source was opened this round
(2026-10-25); quotes located below are verbatim from the opened bytes.

| id | source (URL, opened) | located quote (≤25 words) | decision |
|---|---|---|---|
| S279 | https://man7.org/linux/man-pages/man3/errno.3.html (2026-10-25) | "errno is significant only when the return value of the call indicated an error" (§DESCRIPTION > errno; footer "Linux man-pages 6.19 2026-05-28") | confirm staged row; tier A; recheck on-release |
| S280 | same as S279 | "The error numbers that correspond to each symbolic name vary across UNIX systems, and even across different architectures on Linux." (§DESCRIPTION > Error numbers and names) | confirm staged row; tier A |
| S281 | same as S279 | "$ errno -s permission; EACCES 13 Permission denied" (§DESCRIPTION > worked example output) | confirm staged row; tier A — the pairing is example output, not a portable table |
| S282 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno-base.h (2026-10-25) | "#define EACCES 13 /* Permission denied */" (also `#define EROFS 30 /* Read-only file system */`, EPERM 1, ENOENT 2, EEXIST 17, ENOSPC 28) | confirm staged row; tier A, kernel ABI scope |
| S205 | https://man.archlinux.org/man/errno.3 (2026-10-25; HTTP 200, 30819 B) | "The error numbers that correspond to each symbolic name vary" (HTML line 106; footer "Linux man-pages 6.19"; `errno -s permission` example lines 134-135) | confirm staged row; tier A |
| S214 | https://man.archlinux.org/man/mount.2 (2026-10-25; HTTP 200, 41032 B) | "Some filesystems instead return the error EROFS on an attempt to mount a read-only filesystem" (§ERRORS line 438-439; CAP_SYS_ADMIN lines 85/174; footer 6.19) | confirm staged row; tier A |
| S220 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c (2026-10-25; HTTP 200, 145601 B) | "Snapshot src from another FS" then `ret = -EXDEV;` (lines 1179-1180); "Subvolume creation is not restricted, but snapshots are limited to own subvolumes only" then `ret = -EPERM;` (lines 1183-1186) | confirm staged row; tier A |
| S204 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-subvolume.rst (2026-10-25; HTTP 200, 11914 B) | "returns error (EPERM) and this is logged to the system log." (line 99); "This requires either CAP_SYS_ADMIN or the filesystem must be mounted with user_subvol_rm_allowed mount option." (lines 119-120); "would return 1 to indicate the failure (similar to what mkdir would do)" (lines 62-63) | confirm staged row; tier A |
| S286 | `/home/vgpnk/Projects/shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt` (2026-10-25) | "define EACCES 13 /* Permission denied */" (header: captured 2026-10-24T07:21:36-03:00 from `/usr/include/asm-generic/errno-base.h`, Arch x86_64) | confirm staged row; own-work tier A |
| S287 | `/home/vgpnk/Projects/shokuknow/lanes/tsukuroi/round9/lane-errno13-probe.txt` (2026-10-25) | "probe journal matches for errno:13 -> 0" (recheck run 2026-10-24T07:21:36-03:00; 6 retained boots; mechanism lines `/ mode 555 root:root`, `User=root`, `CapabilityBoundingSet=CAP_SYS_ADMIN`) | confirm staged row; own-work tier A |

`[unk]`: the quarantine slice (12 data rows) verdicts were not re-derived by
this seat — no quarantine artifact was located under `merge/tsukuroi/`; the
claim's hand-check statement is recorded as declared, not as observed here.

---

## 3. Lesson surface

- `corpus/lessons/round-36-verifier-spotcheck.md` (opened; §1-§7): C1 NOT
  VERIFIED (honest stop), C2 unprovable-but-better, six routed defects/next-round
  debts (§6): V8 probe items; C2 note corrections; LOG stamp typo; reject-sample
  note. This is the direct routing source for round-37 C1/C2.
- `corpus/lessons/round-36.md` (opened, head): wave-2 filled lesson; its Gate
  rows re-open wave-1 bytes; mistake rows R36-* mined by W2ScribeMistakes.
- `.ufo/waves/round-36/w2/W2ScribeMistakes/candidate-rows.tsv` (opened): 13
  R36-* candidate rows (e.g. R36-LOG-STAMP-PLACEHOLDER: "grep -nE
  '[0-9]{2}:[0-9]{2}[xX]Z' LOG.md SCORECARD.md; matches LOG.md:1371 today").
- `.ufo/waves/round-36/w2/W2ScribeLesson/round-36.md` (opened): lesson shape
  (Claims / Gate / Gates / Mistakes / Holds / In-place edits) — the format a
  round-37 lesson would follow; also recorded the K07-K11 self-assessment
  mismatches at `c052bb7d` (the C3 repair's antecedent).

Draft-usable lesson observations:

1. The C3 pre-freeze correction is the round's calibration claim; its counter
   gate at tip is now green (`after-c3-0e5f70.json`, mismatches 0). The
   intermediate `CANNOT_EVALUATE` at 5124bf (`missing capability row` /
   `sources-registry`) shows the checker has a hard dependency on the registry
   row population; a lesson/verifier note should record that the self-assessment
   checker exit 2 class exists and was hit mid-chain.
2. C2's three routed corrections are still unapplied at tip (note line 126
   "16-term"; table lacks the `-n` third state; no action-precedence row).
3. The LOG stamp typo (`2026-10-24T04:4043Z`, LOG.md:1379) is still present;
   C2's declared repair ("LOG append") is pending.
4. Assimilation: staged rows S204/S205/S214/S220/S279-S282/S286/S287 were
   re-validated this round against their sources; the errno theme's core
   distinction (number vs name; host-scoped binding) is supported by the opened
   sources, and the portability caveat is discharged only for this host (S286).

---

## 4. Boundaries / unknown

- No outcome is claimed; milestone is draft evidence only.
- `[unk]`: whether the C1 V8 probe design or the C2 correction checker exists
  at tip (they land at the freeze/change commits, post-wave); the wave-1
  build seats (Build1-12) hold the design drafts.
- `[unk]`: quarantine slice verdicts (see §2).
- The C3 tip PASS reading is an observed receipt from `.ufo/waves/round-37/`;
  it was not re-derived by this seat.
