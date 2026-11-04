# Round 70 — lesson (tsukuroi, hyaku run 15, attempt 1)

author: tsukuroi L1 (round 70), integrating the wave `.ufo/waves/round-70/` (13 seats, one v1 wave)
basis: declaration `1710bd74` (frozen before data; base `b2aa0be0`); snapshot repair `84e013a7`; the
pre-data receipts in `.ufo/waves/round-70/before/`; wave results `.ufo/waves/round-70/w1-results.json`
and the seat reports in `.ufo/waves/round-70/{w1,probes}/`.

## Gate

**Trigger and sources.** Four source documents were fetched before the declaration text, and the
snapshot set was completed in `84e013a7` after the critic found `health.c` missing at the declaring
commit. Access date **2026-11-03** for every row; the raw bytes are committed under
`.ufo/waves/round-70/before/src/` with `SHA256SUMS` (4/4 OK) and `SOURCES.json` (four map entries).

- **S290** — `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/xfs.rst?h=v7.2.11`;
  xfs.rst lines 281-282, 16 words: `Setting this to "1" clears accumulated XFS statistics in
  /proc/fs/xfs/stat. It then immediately resets to "0".` (docs, tier A).
- **S291** — `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/xfs/xfs_stats.c?h=v7.2.11`;
  xfs_stats.c lines 73-74, 12 words: `len += scnprintf(buf + len, PATH_MAX - len, " %u",
  counter_val(stats, j));` (code, tier A).
- **S292** — `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/xfs/xfs_sysfs.c?h=v7.2.11`;
  xfs_sysfs.c lines 374-375, 6 words: `if (val != 1) return -EINVAL;`; the same store registers
  `XFS_SYSFS_ATTR_WO(stats_clear);` at line 380 (code, tier A).
- **S293** — `https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git/plain/spaceman/health.c?h=v7.2.0`;
  health.c line 542, 9 words: `Health status has not been collected for this filesystem.` (code,
  tier A).

A second fetch route was required and executed by `S1Scout`: `ROUTE2_OK=4/4`, byte-identical on all
four files (`probes/S1Scout/route2-provenance.txt`).

**Candidates refused (D5, landed as rows).** (a) A second torvalds-v7.2 registration of
`tainted-kernels.rst` — byte-identical to S140, `cmp` rc 0 → **S294 rejected**. (b) An `own-work`
capture row for the round-69 host readings — QUALITY 86: an own-work row may carry a host observation
and never verifies a rule → **S295 rejected**. (c) A row for `MODULE_ARCH_VERMAGIC` from
`<asm/vermagic.h>` — the definition is not inside S289's pinned bytes (`grep -c '#define
MODULE_ARCH_VERMAGIC'` on the committed S289 snapshot prints 0) → **S296 rejected**, with the arch
header fetched only as the flip's target.

**D1 erratum (round-69 Gate record for S288/S289; appended in round 70, round-69 bytes never
rewritten).** The filed `corpus/lessons/round-69.md` `## Gate` carried no URL, access date or located
quote for the two rows landed that round. Recorded now from the committed round-69 snapshots
(`.ufo/waves/round-69/before/src/`, `SHA256SUMS` rc 0; digests equal the S288/S289 pins):

- **S288** — `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/tainted-kernels.rst?h=v7.2.11`,
  opened 2026-11-03; `tk-v7211.rst` lines 72-73, 20 words: `number, as it is a bitfield, where each
  bit indicates the absence or presence of a particular type of taint.`
- **S289** — `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/include/linux/vermagic.h?h=v7.2.11`,
  opened 2026-11-03; `vm-v7211.h` line 12, 8 words: `/* Simply sanity version stamp for modules. */`

**Non-author checks on record.** `S1Scout` re-fetched all four sources by a second route and located
every planned quote with line numbers (`probes/S1Scout/quotes.tsv`); `R1Reviewer` re-implemented the
frozen grammar independently and reproduced 6/6 rows, then built 11 counter mutants (7 refused, 4
survivor channels named below); `R2Reviewer` applied the arm patch in a sandbox and ran the full
selftest plus ten attack groups; `M1Mutation` scored counter mutants 7/7 and arm mutants 8/8 killed;
`K1Critic` re-ran all six declaration receipts and found three defects (this lesson's Mistakes 1 and 2,
and the novelty-command scope); `N1Sentinel` found 0 host writes, 0 secrets, 0 non-read-only sudo, 0
`/tmp` evidence and 0 seat-authored lane paths outside the wave dirs. These are seat checks; the
closure judge's outside spot-check is still owed (`LEARNING.md`: a seat this lane dispatched is still
the lane).

**Census.** Round start: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi` → rc 0, 289 rows. Round end (after the note landed): rc 0, 296 rows (four admitted + three
rejected rows).

**QUALITY 98 watch (standing duty).** No new upstream release fired for the four pinned artifacts this
round: the kernel tag is the host's own v7.2.11 and xfsprogs 7.2.0 is the installed package version
(`pacman -Q xfsprogs` 7.2.0-1). The watch's next re-read is due on a kernel or xfsprogs release.

## Mistakes

- **R70-DECL-SNAPSHOT-RECEIPT-UNBACKED** — class `declaration-overclaim` (the r69 D4 freeze-ordering
  family: a receipt claimed for bytes not at the commit claiming them) · evidence: the declaration at
  `1710bd74` says the four snapshots were "committed byte-exact under `before/src/` with `SHA256SUMS`
  (`sha256sum -c` rc 0)"; at that commit `git show 1710bd74:.ufo/waves/round-70/before/src/SHA256SUMS
  | wc -l` → **3**, and `SOURCES.json` has three keys; `health.c` (the snapshot XS6 cites) and its map
  entry landed only in `84e013a7` · captured-by: none at freeze; `K1Critic` re-ran the receipt · fix:
  the durable check is one loop over `SOURCES.json` keys requiring `git cat-file -e
  <decl>:<dir>/<key>` rc 0 for every declared snapshot, and a `sha256sum -c` whose line count equals
  the named set. Red state: `sha256sum -c` rc 0 on a three-line manifest, which is why the short set
  looked green. The C1 predicate fails closed on the same gap (`map-digest`), so no data inherits it.
  QUALITY 104 records the rule.
- **R70-DECL-HOST-COUNT-CONTRADICTED-BY-ITS-CAPTURE** — class `frozen-fact-misread` · evidence: the
  declaration says "error subtree 7 regular files per filesystem"; the capture it cites,
  `before/host.txt`, lists **9** per filesystem (`fail_at_unmount` plus four handler classes ×
  `{max_retries, retry_timeout_seconds}` = 1 + 8), and the independent seat sums 18
  (`probes/E2Capture/host-enum.txt`) · captured-by: `E2Capture` in this wave · fix: a pre-freeze count
  against the same capture — `awk '/^## error subtree/,/^## geometry/'
  .ufo/waves/round-70/before/host.txt | grep -c '^ 644 '` → 18, so the prose count must be the
  capture's own enumeration. The frozen predicate's "enumerated regular-file counts" is 18, not 14;
  the note and the LOG carry the corrected figure.
- **R70-DECL-NOVELTY-COMMAND-SCOPE** — class `reference-drift` · evidence: the declaration quotes the
  novelty sweep as `git ls-tree … | grep -i xfs | wc -l` 0; run without the `-- corpus/knowledge`
  pathspec at the declaring commit it prints 3, because that same commit added `before/src/{xfs.rst,
  xfs_stats.c, xfs_sysfs.c}` · captured-by: `C1Connector` §4 · fix: quote the command with its
  pathspec (`git ls-tree -r --name-only <rev> -- corpus/knowledge | grep -i xfs | wc -l` → 0; the
  receipt `before/novelty-sweep.txt` already carries it). The substantive proposition — no held XFS
  knowledge note — is true and unaffected.
- **R70-CONSIDERTHESE-ALREADY-ADOPTED** — class `stale-premise` · evidence: the declaration named the
  `considerthese/2026-10-26.md` "Counter-attack scoreboard" proposal as this round's mining; it was
  adopted at round 64 (`SKILL.md:5603`) and continued from r41/r42 · captured-by: the L1's own read of
  `SKILL.md` before landing; `SC3Lesson` measured the hit table · fix: no proposal is mined this round;
  the scoreboard is continued as the standing ledger, and the measured implementation status per
  proposal is recorded below so a later round does not re-adopt a landed one.
- **R70-SEAT-SCRATCH-STRAY** — class `provider`/housekeeping (a seat left state behind) · evidence:
  `M1Mutation`'s FIFO mutant process (`A4-read-fifo`) outlived the seat by >5 minutes and its scratch
  tree was 484 MB at the L1's check; the L1 killed the process and the tree was reclaimed · captured-by:
  the L1's post-wave disk check · fix: the seat-self report rule stands; a wave whose mutant hangs has
  no per-case timeout in the census selftest, which is the durable finding (`M1Mutation` §2: "a hang is
  the only observable" — a timeout harness is a next-round instrument amendment).

## Considerthese

No proposal is mined this round; the measured status of the four proposals in the latest file
(`considerthese/2026-10-26.md`) is recorded rather than claimed: "Counter-attack scoreboard" is a
standing `SKILL.md` ledger since r41/r42 and resumed at r64 (7 lesson + 5 `SKILL.md` hits);
"Seat-harm incident log" is a lessons-only per-round tally since r66 (3 lesson hits, 0 `SKILL.md`);
"Burst-aware reading" has one mining record (r46) and is explicitly not a gate; the "Cross-note
correction propagation map" is recorded partial (r43/r54, and r57/r58 say "none clears this round's
bar"). The scoreboard below is a continuation of the r64 ledger, not a new adoption.

### Counter-attack scoreboard — round 70 (continuation of the r64 ledger)

| Counter | Round / arm source | Arms fielded (receipts) | Survivors (arms that reached PASS) | Class that beat it |
|---|---|---|---|---|
| `count-xs-rows-r70.py` (C1) | r70 pre-data battery (`before/control/battery.txt`) | 8 cases: 1 well-formed control + 7 mutants | 0 survived (7/7 mutants read below target, rc 1; control 6/6 rc 0) | the seven frozen clauses fired: substance, source-to-snapshot binding, digest, quote location, statement words, row count, id uniqueness |
| `count-xs-rows-r70.py` (C1) | r70 wave `w1/R1Reviewer.md` | 11 self-built mutants over the four real snapshots | 4 survived: M4 chance-tokens, M5 duplicate-snapshot, M6 anchor-bogus, M11 invisible-row; 7 refused | substance floor is lexical (three real tokens + gibberish passes); bookkeeping channels: unused registry `anchor` cell (M6), `>=4 distinct` tolerates duplicate snapshots (M5), `startswith("| XS")` skips `|XS8|` (M11) |
| `count-xs-rows-r70.py` (C1) | r70 wave `probes/M1Mutation/` | 7 source-level mutants (dedupe-binding, digest-any, stopword-free tokens, no quote location, 7-word accept, non-contiguous ids, pipe-cell accept) | 0 survived (7/7 killed); the committed pre-data battery alone kills only 2/7 of these | the battery's fixture set is thinner than the counter's clause set — coverage debt in a committed receipt, not a predicate defect |
| `xfs-stats` census arm (C2) | r70 wave `probes/M1Mutation/` | 8 arm-body mutants (no dedupe, global-dir-as-fs, unvalidated echo, FIFO read, unreadable-as-parsed, rollup term, silent absent) | 0 survived (8/8 killed); A6 (rollup) is killed by the pre-existing R39 rollup cases and the R70 shape cases, not by the neutrality A/B case | case-attribution gap: the neutrality case cannot fire where the fixture journal plane is already DEGRADED |
| `xfs-stats` census arm (C2) | r70 wave `w1/R2Reviewer.md` | 10 attack groups (a-j) | 7 required groups survived; 2 counting defects (F2 dotfile undercount, F3 symlink overcount) and 1 fixture-policy finding (h) | counting semantics: globstar skips dotfiles and `test -f` follows symlinks — repaired in-round with two new cases and a red-before receipt |

## Trend verdicts

- **expansion: improved.** Four new registry rows (S290-S293) on ground the lane never held — `sys/fs/xfs`,
  `stats_clear`, `log_head_lsn`, `reserve_grant_head_bytes`, `fail_at_unmount`, `xfs_spaceman`,
  `max_retries` all read 0 hits at base (`before/novelty-sweep.txt`) — one admitted knowledge entry
  citing them, three rejected rows (S294-S296) that keep the refusals visible, and one new capability
  (`xfs-stats-arm`, SCORECARD capabilities).
- **quality: improved.** The r68 shape-only-counter debt stays answered by a declaration-frozen
  content-sensitive counter, now with the r69-planned statement-substance and source-to-snapshot
  binding clauses (`before/control/battery.txt`); two attack-found arm defects (F2/F3) are repaired
  with red-before proof (212/214 pre-repair, 214/214 post-repair); the PROVINCE promotion removes a
  standing contradiction ("stays unread"); QUALITY 104 lands from this round's own declaration defects;
  the D1 Gate erratum closes the r69 record gap. No admitted entry failed its re-check.
- **discernment: unchanged.** The lane's own declaration carried three defects that the wave caught
  (snapshot set, host count, novelty command scope) and one stale considerthese premise — all
  learned into `## Mistakes` and QUALITY 104 rather than smoothed; `R1Reviewer`/`R2Reviewer`/`M1Mutation`/
  `K1Critic` found and named real weaknesses (M4 substance floor, M5/M6/M11 bookkeeping channels, C2
  predicate weakness C2-1, F2/F3) which are recorded as limits, not closed by relabelling. The outside
  non-author admit/reject spot-check is owed by the closure judge; no `[x]` is claimed.

## Seat-harm tally (standing per-round tally, r66 adoption continued)

Round 70: **0** seat-to-seat harms (no `pkill`, no cross-seat `/tmp` collision, no fleet-root misroot;
`N1Sentinel` measured `WRITES=0 SECRETS=0 SUDO_NONREADONLY=0 TMP_EVIDENCE=0 LANE_DIRTY=0`). One
seat-self housekeeping defect: `M1Mutation`'s hung FIFO mutant process and 484 MB scratch tree outlived
the seat and were reclaimed by the L1 (`R70-SEAT-SCRATCH-STRAY`). Running tally since r66: 0, 0, 0, 0, 1.
