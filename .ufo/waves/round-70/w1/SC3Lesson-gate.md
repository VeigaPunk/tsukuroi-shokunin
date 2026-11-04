# Round 70 — Gate block (scribe draft; admission and verdicts are the L1's)

seat `SC3Lesson` (scribe; axes calibration, lesson) · wave `w1` · lane HEAD at draft
`84e013a732d7526d08064c6823858d602029ecd7` · declaration `1710bd74aec840c71d5e4ffbdc0ca54198e953fa`
(frozen before data) · base `b2aa0be0`.

Read read-only for this block: `SCORECARD.md` "Round 70 — declaration" at `1710bd74`
(`:5271-5320`); `.ufo/waves/round-70/before/src/{xfs.rst,xfs_stats.c,xfs_sysfs.c,health.c,SHA256SUMS,SOURCES.json}`;
`corpus/lessons/round-69.md`; `corpus/lessons/round-69-verifier-spotcheck.md` §6 D1;
`.ufo/waves/round-70/w1/SC2Sources.md` §1-§5; `.ufo/waves/round-70/w1/SC1Entry-note.md`;
`probes/S1Scout/`, `probes/E2Capture/host-enum.txt`, `probes/E3Repairs/cited-r70-at-decl.txt`,
`w1/C1Connector.md` §1. Every number below was re-measured by this seat and the producing command is
named. Nothing outside `.ufo/waves/round-70/w1/` was written.

## Gate

**Trigger and axis.** The declaration opens the round on the lowest non-retired axis, depth 8, tied
with adjacency 8; a capability entered at round 69 (`kernel-arm`), so the stagnation window stands at
1 of 3 and the nudge does not waive the lowest-axis duty. Two claims on two distinct axes: C1 depth
(the XFS sysfs storage plane, SOURCED — four new registry rows) and C2 operability (the census
`xfs-stats` arm, capability `xfs-stats-arm`). The predicates are frozen at `SCORECARD.md:5310` (C1)
and `:5311` (C2); this draft restates none of them and adds no counter.

**The four source bytes are real, three-way equal, and the digests are the frozen ones.**
`sha256sum -c SHA256SUMS` in `before/src/` at this HEAD → `xfs.rst: OK`, `xfs_stats.c: OK`,
`xfs_sysfs.c: OK`, `health.c: OK`, rc 0; the four digests equal the declaration's list
(`53bda67b…d051c`, `4b6a9b6c…9e452`, `1cbcffa1…a5805`, `84fdd0be…15950`) and the `SOURCES.json`
map. The second fetch route exists: S1Scout reports `ROUTE2_OK=4/4 MATCHED=4/4` with
`cmp_exit=0` and equal digests for all four files (`probes/S1Scout/route2-provenance.txt`; kernel
files from `raw.githubusercontent.com/gregkh/linux/v7.2.11/`, `health.c` from the xfsprogs `7.2.0`
tarball, sha256 `501dfa36…cc83`).

**Disclosed freeze defect (not a gate verdict).** At the declaration commit itself the tree held
three of the four snapshots: `git ls-tree --name-only 1710bd74:.ufo/waves/round-70/before/src` →
`FETCH.txt`, `SHA256SUMS`, `SOURCES.json`, `xfs.rst`, `xfs_stats.c`, `xfs_sysfs.c`;
`SHA256SUMS` has 3 lines; `SOURCES.json` has 3 snapshot keys. `health.c` and its map entry landed
in the repair commit `84e013a7`. The C1 predicate would have failed closed on it (the `map-digest`
clause), so this is a declaration-record defect; it is recorded as Mistakes 1 in `SC3Lesson.md`.

**Candidates considered — four admitted sources S290-S293.** Id→snapshot binding is the one in
SC2Sources §1 and the declaration's snapshot order; access date is 2026-11-03 for every row.

| id | snapshot (bytes, lines) | URL (verbatim from `before/src/SOURCES.json`) | located quote (words; 1-based lines) | mechanism it grounds | draft XS rows it supports |
|---|---|---|---|---|---|
| S290 | `xfs.rst` (22719 B, 563 lines) | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/xfs.rst?h=v7.2.11` | `Setting this to "1" clears accumulated XFS statistics in /proc/fs/xfs/stat. It then immediately resets to "0".` (16; 281-282) | the documented `fs.xfs.stats_clear` sysctl (`:280-282`) and the documented per-filesystem error-configuration hierarchy `/sys/fs/xfs/<dev>/error/<class>/<error>/` with the `metadata` class (`:408-422`), `fail_at_unmount` (`:433-452`), `max_retries` (`:463-476`) | XS5 |
| S291 | `xfs_stats.c` (5319 B, 179 lines) | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/xfs/xfs_stats.c?h=v7.2.11` | `len += scnprintf(buf + len, PATH_MAX - len, " %u", counter_val(stats, j));` (12; 73-74) | `counter_val` sums a per-CPU `__u32` slot (`:10-17`), the named `xstats[]` group table (`:29-64`), one output line per group inside the group loop (`:66-76`), the four printed precision lines (`:77-96`), and the `/proc/fs/xfs/stat` symlink to `/sys/fs/xfs/stats/stats` (`:151-159`) | XS1, XS2 |
| S292 | `xfs_sysfs.c` (18203 B, 898 lines) | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/xfs/xfs_sysfs.c?h=v7.2.11` | `if (val != 1) return -EINVAL;` (6; 374-375) | `stats` RO and `stats_clear` WO on the stats kobject (`:349-380`), the log kobject's `log_head_lsn`/`log_tail_lsn` (`cycle:block`) and `reserve_grant_head_bytes`/`write_grant_head_bytes` (`:405-462`), and the error-config attributes `max_retries`/`retry_timeout_seconds`/`fail_at_unmount` (`:473-640`) | XS3, XS4 |
| S293 | `health.c` (11763 B, 584 lines) | `https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git/plain/spaceman/health.c?h=v7.2.0` | `Health status has not been collected for this filesystem.` (9; 542) | `health_f`'s default filesystem report (`:518-538`) and the not-collected branch with its `xfs_scrub(8)` advice (`:540-545`) | XS6 |

All four quotes re-located verbatim (whitespace-normalized) in the committed snapshot by this seat;
none contains a pipe; none exceeds 25 words. The draft row partition above is
`w1/SC1Entry-note.md`'s (`XS1`-`XS6`), not this seat's invention; the final partition and every row
cell belong to the note's author and the L1.

**Row-quote envelope (frozen, read from the counter).** `tools/count-xs-rows-r70.py` (sha256
`65065d9d…f6f5c`, equal at HEAD and at the declaration — measured twice) matches a row with
`quote="(?P<quote>[^"]*)" \|$` and requires `line.count("|") == 7` (`:40-42`). [INFERENCE from those
bytes] a row-level quote therefore cannot contain a literal `"`: the S290 sysctl quote above
(contains `"1"`/`"0"`) and the S291 `" %u"` quote are Gate-record quotes and not usable as row
quotes. This is a property of the frozen predicate, not a proposed change.

**Draft-level clause check (not the counter's verdict).** Using the frozen module's own `ROW_RE`,
`grounded` and constants, imported unmodified, over the six rows of `w1/SC1Entry-note.md` at this
HEAD: ids 1-6 unique and contiguous; pipes per row 7; statement words 19/31/24/23/21/25 (min 12);
statement-substance tokens 5/7/9/6/11/10 (min 3); digests equal the snapshot sha256 and the map
(all six); quote words 7/8/6/4/13/9 (max 25), no pipe, no double quote, located in the named
snapshot (all six). The two clauses this seat cannot evaluate at draft time are
`source-unregistered`/`source-not-bound`: `corpus/SOURCES.md` holds 289 rows at the base, at the
declaration and at this HEAD, and S290-S293 exist only as the SC2Sources draft (§1). R1Reviewer
re-derived the same six rows independently (own parser, `DERIVED_OK=6/6`, `w1/R1Reviewer.md`
Finding 1), and its one wording note (XS6's trailing clause) is a LOW risk that violates no frozen
clause.

**Rejections — the three refused round-69 candidates, with reason and flip.** (R69 spot-check §3;
D5 routes them as `rejected` registry rows.)

| candidate | decision | reason (measured) | flip | landed as (draft) |
|---|---|---|---|---|
| (a) a second registration of `tainted-kernels.rst` at the torvalds v7.2 tag | refused | byte-identical to S140: fresh fetch 2026-11-03, HTTP 200, 9340 bytes, sha256 `727ddb82…0841`, `cmp` against `.ufo/waves/round-27/sources/S140.rst` rc 0 (SC2Sources §4); a second row adds no authority | a row that pins these bytes at another tag and carries a tag-specific change | S294 |
| (b) an `own-work` capture row for the host readings | refused | `corpus/QUALITY.md:169` rule 86: an own-work row may carry a host observation, count or capture digest and never verifies a rule by itself; the XS statements are upstream behaviour | the row's scope narrows to this host's observation and it is cited alongside an upstream row at the running release (round 69 named none) | S295 |
| (c) a row for `MODULE_ARCH_VERMAGIC` from `<asm/vermagic.h>` | refused | the token is only used in the pinned bytes (`vm-v7211.h:45`, header included at `:10`); `grep -c '#define MODULE_ARCH_VERMAGIC' vm-v7211.h` → 0, rc 1; the definition sits at `arch/x86/include/asm/vermagic.h:47,49`, which round 69 never pinned | that arch header opened as its own pinned row | S296 |

**D1 erratum — round-69 Gate record for S288/S289 (append-only; round-69 bytes are never edited).**

> **D1 erratum (round-69 Gate record for S288/S289; appended in round 70).** The filed
> `corpus/lessons/round-69.md` `## Gate` carries no URL, no access date and no located quote for the
> two rows landed that round: `grep -c 'git.kernel.org\|https://' corpus/lessons/round-69.md` → 0.
> Recorded now from the committed round-69 snapshots (`.ufo/waves/round-69/before/src/`,
> `SHA256SUMS` rc 0; digests equal the S288/S289 pins):
>
> - **S288** — `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/tainted-kernels.rst?h=v7.2.11`,
>   opened 2026-11-03; `tk-v7211.rst` (sha256 `727ddb82…0841`), lines 72-73, 20 words:
>   `number, as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint`
>   (the filed note's KR5 carries the same text as a 19-word suffix form, without the leading
>   `number,`).
> - **S289** — `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/include/linux/vermagic.h?h=v7.2.11`,
>   opened 2026-11-03; `vm-v7211.h` (sha256 `0556c28f…1aea`), line 12, 8 words:
>   `/* Simply sanity version stamp for modules. */`; the composition it stamps is anchored at
>   lines 41-46 (`VERMAGIC_STRING`), which is where the filed note's KR1 quote sits.
>
> The quotes already existed in committed bytes (the round-69 wave draft
> `.ufo/waves/round-69/drafts/c1/lesson.md`, and the note's KR rows); what was missing was their
> placement in the filed lesson, which is what this erratum supplies.

**Non-author checks on record (this seat is not one).** Reports that exist at draft time:

- `S1Scout` — second-route fetch and byte equality for all four snapshots
  (`probes/S1Scout/route2-provenance.txt`: `ROUTE2_OK=4/4 MATCHED=4/4`), host cross-check and quote
  candidates (`probes/S1Scout/quotes.tsv`), row-sketch check (`probes/S1Scout/row-sketch-check.txt`).
- `E2Capture` — independent read-only host enumeration captured 2026-11-04T00:09:44Z, two identical
  full counts: `mounts=2 present=2 absent=0 unreadable=0 stats=2 error=18 log=8 detail=none`
  (`probes/E2Capture/host-enum.txt` §1/§16), with a trap witness (§15) and an independent
  `xfs_spaceman -c health` read (§13).
- `E3Repairs` — `check-cited-receipts-r62.py` receipt at `1710bd74` for round 70: `rc: 0`,
  `finding_count: 0`, `files_scanned: 9`, revision binding assert OK
  (`probes/E3Repairs/cited-r70-at-decl.txt`; the receipt at the final tree is still owed — D2), and
  the D2/D3/D6/D7 drafts (`w1/E3Repairs.md`).
- `R1Reviewer` — independent re-derivation of the six rows (`DERIVED_OK=6/6`), 11 counter mutants
  with 7 refused and 4 survivors (M4 chance-tokens, M5 duplicate-snapshot, M6 anchor-bogus, M11
  invisible-row), novelty holds, verdict "C1 stands" (`w1/R1Reviewer.md`).
- `N1Sentinel` — boundary/secret/side-effect sweep of everything under `.ufo/waves/round-70/`:
  `WRITES=0 SECRETS=0 SUDO_NONREADONLY=0 TMP_EVIDENCE=0 LANE_DIRTY=0 STATS_CLEAR_MODE_UNCHANGED=1
  FINDINGS=11` (`w1/N1Sentinel.md`, witness `probes/N1Sentinel/boundary-witness.txt`).
- `SC2Sources` — registry rows S290-S293 (admitted draft) and S294-S296 (rejected draft), 11 cells
  each, NF 13, no pipe inside a cell, with the Gate record and erratum text (`w1/SC2Sources.md`).
- `SC1Entry` — the note draft carrying XS1-XS6 (`w1/SC1Entry-note.md`).
- `C1Connector` — 20-sibling overlap scan at HEAD; the lane diff `1710bd74..HEAD -- corpus/ SKILL.md
  PROVINCE.md` is empty (re-verified by this seat: 0 lines), and the sibling hits are classified
  shared/peripheral (`w1/C1Connector.md`).

**Seats whose reports are absent at draft time.** `R2Reviewer`, `M1Mutation`, `K1Critic`, and no
`w1/E1XfsArm.md` (`probes/E1XfsArm/` holds the implementation receipts — diff, live line, selftest —
but no report and no attack arm). No admit/reject verdict, attack result or selftest count is cited
here from those seats; the non-author closure spot-check remains owed (LEARNING.md).

**Limits of this block.**

- This seat re-fetched no URL; the three-way equality is S1Scout's receipt.
- This seat did not run the frozen counter or the census: the counter's digest was compared
  (`65065d9d…f6f5c` at HEAD and at the declaration) and only its row-local clauses were evaluated
  in-process; C2's control holds at this HEAD (`grep -c 'XFS xfs-stats' tools/tsukuroi-census.sh`
  → 0, `probe_xfs` → 0).
- `corpus/SOURCES.md` is 289 rows at the base, the declaration and this HEAD; the 293 target and
  the note `corpus/knowledge/xfs-storage-plane-r70.md` do not exist yet (`git cat-file -e` rc 128 at
  base and at HEAD). The rows above are drafts for the L1 to land.
- The declaration's host prose says "error subtree 7 regular files per filesystem"; the capture it
  cites lists 9 per filesystem and E2Capture sums 18 — recorded as Mistakes 2 in `SC3Lesson.md`;
  C2's predicate counts live readable regular files recursively, so the prose figure is not a
  predicate term.
