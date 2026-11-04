# Round 70 — lesson sections (scribe draft; the L1 fills verdicts)

author: `SC3Lesson` (scribe; axes calibration, lesson), wave `w1` of round 70 (hyaku run 15)
basis: declaration `1710bd74aec840c71d5e4ffbdc0ca54198e953fa` (frozen before data) at base
`b2aa0be0`; lane HEAD at draft `84e013a732d7526d08064c6823858d602029ecd7`; receipts
`.ufo/waves/round-70/before/`, `probes/`, `w1/`. Nothing here asserts a claim verdict, an axis move,
a trend verdict, or a registry admission; those are the L1's.

## Gate

The paste-ready Gate block is `.ufo/waves/round-70/w1/SC3Lesson-gate.md`; its content is reproduced
here so this file can be read alone. Both copies were written in the same pass and carry the same
quotes and counts.

**Trigger and axis.** The declaration opens the round on the lowest non-retired axis, depth 8, tied
with adjacency 8; a capability entered at round 69 (`kernel-arm`), so the stagnation window stands at
1 of 3 and the nudge does not waive the lowest-axis duty. Two claims on two axes: C1 depth (the XFS
sysfs storage plane, SOURCED — four new registry rows) and C2 operability (the census `xfs-stats`
arm). The predicates are frozen at `SCORECARD.md:5310` (C1) and `:5311` (C2); this draft adds no
counter and reinterprets none.

**The four source bytes are real, three-way equal, and the digests are the frozen ones.**
`sha256sum -c SHA256SUMS` in `.ufo/waves/round-70/before/src/` at this HEAD → four `OK`, rc 0; the
digests equal the declaration's list and the `SOURCES.json` map. The second route exists: S1Scout
reports `ROUTE2_OK=4/4 MATCHED=4/4`, `cmp_exit=0` for all four files
(`probes/S1Scout/route2-provenance.txt`).

**Disclosed freeze defect (not a gate verdict).** At the declaration commit the tree held three of
the four snapshots (`git ls-tree --name-only 1710bd74:.ufo/waves/round-70/before/src` → 3 `.rst/.c`
files; `SHA256SUMS` 3 lines; `SOURCES.json` 3 keys). `health.c` and its map entry landed in the
repair `84e013a7`. Recorded as Mistakes 1.

**Candidates considered — four admitted sources S290-S293** (id→snapshot per SC2Sources §1 and the
declaration's snapshot order; access date 2026-11-03 for all four):

| id | snapshot | URL (verbatim from `before/src/SOURCES.json`) | located quote (words; lines) | draft XS rows |
|---|---|---|---|---|
| S290 | `xfs.rst` | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/xfs.rst?h=v7.2.11` | `Setting this to "1" clears accumulated XFS statistics in /proc/fs/xfs/stat. It then immediately resets to "0".` (16; 281-282) | XS5 |
| S291 | `xfs_stats.c` | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/xfs/xfs_stats.c?h=v7.2.11` | `len += scnprintf(buf + len, PATH_MAX - len, " %u", counter_val(stats, j));` (12; 73-74) | XS1, XS2 |
| S292 | `xfs_sysfs.c` | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/xfs/xfs_sysfs.c?h=v7.2.11` | `if (val != 1) return -EINVAL;` (6; 374-375) | XS3, XS4 |
| S293 | `health.c` | `https://git.kernel.org/pub/scm/fs/xfs/xfsprogs-dev.git/plain/spaceman/health.c?h=v7.2.0` | `Health status has not been collected for this filesystem.` (9; 542) | XS6 |

Each quote was re-located verbatim (whitespace-normalized) in the committed snapshot by this seat;
none carries a pipe; none exceeds 25 words. The row partition is `w1/SC1Entry-note.md`'s, not this
seat's.

**Row-quote envelope.** `tools/count-xs-rows-r70.py` (sha256 `65065d9d…f6f5c`, equal at HEAD and at
the declaration — measured twice) matches `quote="(?P<quote>[^"]*)" \|$` and requires
`line.count("|") == 7` (`:40-42`). [INFERENCE from those bytes] a row-level quote therefore cannot
contain a literal `"`, so the S290 sysctl quote and the S291 `" %u"` quote above are Gate-record
quotes, not usable as row quotes. A property of the frozen predicate, not a proposed change.

**Draft-level clause check (not the counter's verdict).** Using the frozen module's own `ROW_RE`,
`grounded` and constants, imported unmodified, over the six rows of `w1/SC1Entry-note.md` at this
HEAD: ids 1-6 unique and contiguous; pipes per row 7; statement words 19/31/24/23/21/25 (min 12);
statement-substance tokens 5/7/9/6/11/10 (min 3); digests equal the snapshot sha256 and the map;
quote words 7/8/6/4/13/9 (max 25), no pipe, no double quote, located — all six pass every row-local
clause. Not evaluable at draft time: `source-unregistered`/`source-not-bound` (registry 289 rows at
base, declaration and this HEAD; S290-S293 exist only as the SC2Sources draft).

**Rejections (the three refused round-69 candidates), with reason and flip.**

| candidate | decision | reason (measured) | flip | landed as (draft) |
|---|---|---|---|---|
| (a) second `tainted-kernels.rst` registration at torvalds v7.2 | refused | byte-identical to S140: 9340 bytes, sha256 `727ddb82…0841`, `cmp` vs `.ufo/waves/round-27/sources/S140.rst` rc 0 (SC2Sources §4) | a row pinning these bytes at another tag with a tag-specific change | S294 |
| (b) `own-work` capture row for the host readings | refused | QUALITY 86 (`corpus/QUALITY.md:169`): an own-work row carries a host observation/count/digest and never verifies a rule; the XS statements are upstream behaviour | the row's scope narrows to this host's observation beside an upstream row at the running release (r69 named none) | S295 |
| (c) `MODULE_ARCH_VERMAGIC` row from `<asm/vermagic.h>` | refused | used only at `vm-v7211.h:45` (header included `:10`); `grep -c '#define MODULE_ARCH_VERMAGIC' vm-v7211.h` → 0, rc 1; the definition is at `arch/x86/include/asm/vermagic.h:47,49`, never pinned in r69 | that arch header opened as its own pinned row | S296 |

**D1 erratum — round-69 Gate record for S288/S289 (append-only; round-69 bytes never edited).**

> **D1 erratum (round-69 Gate record for S288/S289; appended in round 70).** The filed
> `corpus/lessons/round-69.md` `## Gate` carries no URL, access date or located quote for the two
> rows landed that round (`grep -c 'git.kernel.org\|https://' corpus/lessons/round-69.md` → 0).
> Recorded now from the committed round-69 snapshots (`.ufo/waves/round-69/before/src/`,
> `SHA256SUMS` rc 0):
>
> - **S288** — `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/tainted-kernels.rst?h=v7.2.11`,
>   opened 2026-11-03; `tk-v7211.rst` (sha256 `727ddb82…0841`), lines 72-73, 20 words:
>   `number, as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint`
>   (the note's KR5 carries the 19-word suffix form without `number,`).
> - **S289** — `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/include/linux/vermagic.h?h=v7.2.11`,
>   opened 2026-11-03; `vm-v7211.h` (sha256 `0556c28f…1aea`), line 12, 8 words:
>   `/* Simply sanity version stamp for modules. */`; the composition it stamps is anchored at
>   lines 41-46 (`VERMAGIC_STRING`), where the note's KR1 quote sits.
>
> The quotes existed in committed bytes (round-69 wave draft `.ufo/waves/round-69/drafts/c1/lesson.md`,
> the note's KR rows); what was missing was their placement in the filed lesson.

**Non-author checks on record (this seat is not one).** `S1Scout` (route-2 4/4 matched,
`probes/S1Scout/`); `E2Capture` (independent enumeration 2026-11-04T00:09:44Z, two identical counts:
`mounts=2 present=2 absent=0 unreadable=0 stats=2 error=18 log=8 detail=none`,
`probes/E2Capture/host-enum.txt` §1/§16, trap witness §15, `xfs_spaceman` read §13); `E3Repairs`
(cited-receipts `rc: 0`, `finding_count: 0`, `files_scanned: 9` at `1710bd74`, plus the D2/D3/D6/D7
drafts; `probes/E3Repairs/cited-r70-at-decl.txt`, `w1/E3Repairs.md`); `R1Reviewer` (independent
re-derivation `DERIVED_OK=6/6`; 11 counter mutants, 7 refused, 4 survivors M4/M5/M6/M11; novelty
holds; verdict "C1 stands" — `w1/R1Reviewer.md`); `N1Sentinel` (boundary sweep
`WRITES=0 SECRETS=0 SUDO_NONREADONLY=0 TMP_EVIDENCE=0 LANE_DIRTY=0 STATS_CLEAR_MODE_UNCHANGED=1
FINDINGS=11` — `w1/N1Sentinel.md`); `SC2Sources` (registry drafts S290-S296, NF 13, no in-cell
pipe); `SC1Entry` (note draft XS1-XS6); `C1Connector` (20-sibling scan;
`git diff 1710bd74..HEAD -- corpus/ SKILL.md PROVINCE.md` is empty — verified by this seat, 0 lines).
**Absent at draft time**: `R2Reviewer`, `M1Mutation`, `K1Critic`, and no `w1/E1XfsArm.md` (its
`probes/E1XfsArm/` receipts exist, but no report and no attack arm) — no verdict from them is
cited; the non-author closure spot-check is owed.

## Mistakes

- **R70-DECL-SNAPSHOT-RECEIPT-UNBACKED** — class `declaration-overclaim` (the r69 D4 freeze-ordering
  family: a receipt claimed for bytes that are not at the commit claiming them) · evidence:
  `SCORECARD.md:5285-5291` at `1710bd74` says the four snapshots were "committed byte-exact under
  `before/src/` with `SHA256SUMS` (`sha256sum -c` rc 0)" and that `SOURCES.json` maps them; at that
  commit `git ls-tree --name-only 1710bd74:.ufo/waves/round-70/before/src` lists three `.rst/.c`
  files, `git show 1710bd74:.ufo/waves/round-70/before/src/SHA256SUMS | wc -l` → 3, and
  `SOURCES.json` has 3 snapshot keys; `health.c` (digest `84fdd0be…15950`, the snapshot XS6 cites)
  and its map entry landed only in repair `84e013a7` · captured-by: none at freeze — the
  declaration's own receipt claim was not re-run against the declaring tree; the repair commit names
  the defect · fix: a command that can fail, run at the declaring revision before the text is frozen:
  `git -C <lane> cat-file -e 1710bd74:.ufo/waves/round-70/before/src/health.c` → prints "Not a valid
  object name" and exits 128 (observed); the durable form is one loop over the `SOURCES.json` keys
  requiring `git cat-file -e <decl>:<dir>/<key>` rc 0 for every declared snapshot. The C1 predicate
  fails closed on the same gap (`map-digest` when the map lacks the snapshot), so the data does not
  inherit the error.
- **R70-DECL-HOST-COUNT-CONTRADICTED-BY-ITS-CAPTURE** — class `frozen-fact-misread` · evidence:
  `SCORECARD.md:5289` says "error subtree 7 regular files per filesystem"; the capture it cites,
  `before/host.txt:101-121`, lists nine per filesystem (`fail_at_unmount` plus four classes ×
  `{max_retries,retry_timeout_seconds}`), and the independent seat sums 18
  (`probes/E2Capture/host-enum.txt` §10 `sum_recursive=18`, §14 `error -> 18`) · captured-by:
  `E2Capture` in this wave — nothing at freeze · fix: a pre-freeze count against the same capture:
  `awk '/^## error subtree/,/^## geometry/' .ufo/waves/round-70/before/host.txt | grep -c '^ 644 '`
  → 18, so the sentence may state 7 only if that output is 7 per mount; the count must be the
  capture's own enumeration, never a recollection. C2's predicate is unaffected: it counts live
  readable regular files under `error/` recursively (a maxdepth-1 read would give 2, E2Capture §15),
  so the arm — not the prose — is what the counter measures.

## Considerthese

**Counter-attack scoreboard — continuation of the round-64 ledger, not a new adoption.** The
proposal first landed at round 41 (`SKILL.md:3833` "Counter-attack scoreboard — rounds 40-41"), was
continued at round 42 (`SKILL.md:3935`) and resumed at round 64 (`SKILL.md:5603` "Counter-attack
scoreboard — round 64 (resumed; considerthese assimilation)"). This round appends to that ledger in
the round-64 column shape; it claims no adoption.

| Counter | Round / arm source | Arms fielded (receipts) | Survivors (arms that reached PASS) | Class that beat it |
|---|---|---|---|---|
| `count-xs-rows-r70.py` (C1) | r70 pre-data battery (`before/control/battery.txt`) | 8 cases: 1 well-formed control + 7 mutants (content-free, any-registered-id, digest-swap, quote-absent, short-statement, five-row, duplicate-id) | 0 survived (7/7 mutants killed; `rc=1 want=1` in every mutant line, control `rc=0`) | none — the seven frozen clauses fired: substance, source-to-snapshot binding, digest, quote location, statement words, row count, id uniqueness |
| `count-xs-rows-r70.py` (C1) | r70 wave `w1/R1Reviewer.md` | 11 self-built mutants (M1-M11; distinct from the frozen battery's 8 cases), own six-row fixture over the four snapshots | 4 survived: M4 chance-tokens, M5 duplicate-snapshot, M6 anchor-bogus, M11 invisible-row; 7 refused (binding, quote order, stopwords-only, row count, id contiguity, 26-word quote, pipe, uppercase hex) | substance floor: three real domain tokens plus nine gibberish words reach `grounded()==3` (M4); bookkeeping-only channels: `registry_rows()` stores the anchor cell that `evaluate()` never reads (M6), `>=4 distinct` snapshots tolerates duplicates (M5), `line.startswith("| XS")` skips `|XS8|…` (M11) |
| `count-xs-rows-r70.py` (C1) | r70 wave `probes/M1Mutation/` | unfilled | unfilled | unfilled |
| `count-xs-rows-r70.py` (C1) | r70 wave `probes/R2Reviewer/` | unfilled | unfilled | unfilled |
| `xfs-stats` census arm (C2) | r70 wave `probes/M1Mutation/` (attack arm); `probes/E1XfsArm/` holds the implementation receipts (diff, live line, selftest) but no attack report | unfilled | unfilled | unfilled |

`unfilled` = the arm's receipt does not exist at draft time (or, as the C2 row states, exists only as
implementation receipts without an attack report); no number is invented. The pre-data
battery is not a wave attack arm and is labelled as such: it is the counter's own frozen fixture set,
and a PASS there states that the clauses fire, never that a hostile writer cannot pass.

**Proposal-implementation claim, recorded and measured.** The orchestrator's correction states that
"every proposal in the latest file `considerthese/2026-10-26.md` is already implemented this lane
(Burst-aware reading r46, Seat-harm incident log r45/r66, Counter-attack scoreboard r64, Cross-note
correction propagation map r43/r54)" and asks that the claim be verified by grepping
`corpus/lessons/` and `SKILL.md` for each proposal name, "citing the three hits per proposal".
Measured with `grep -rF -c` summed over `corpus/lessons/` and `grep -F -c` over `SKILL.md`, exact
proposal names:

| proposal (`considerthese/2026-10-26.md`) | lesson hits | `SKILL.md` hits | status measured |
|---|---|---|---|
| "Burst-aware reading" | 1 (`round-46.md:97`, rule taken `:99-109`) | 0 | mined r46; the checker is called "wave evidence, not a lane gate" (`:109`) — one record, no standing instrument |
| "Seat-harm incident log" | 3 (`round-45.md:124`, `round-66.md:59`, `round-67.md:93`) | 0 | r45:134 records a prior non-adoption; r66 lands a per-round tally (`round-66.md:81`), r67 continues it (`:93`) — lessons-only tally |
| "Counter-attack scoreboard" | 7 (`round-41.md:99,103`; `round-47.md:71`; `round-52.md:64,66`; `round-64.md:133,134`; `round-68.md:103`) | 5 (`:3833`, `:3835`, `:3935`, `:5603`, `:5605`) | standing `SKILL.md` ledger, r41 → r42 → r64 — the one proposal with three-or-more hits in both places |
| "correction propagation map" | 2 (`round-43.md:83`, `round-54-verifier-spotcheck.md:222`; broader `propagation` 6, `round-57.md:115`, `round-58.md:82`) | 0 | r57:115 and r58:82 both read "partially applied in r54 — none clears this round's bar" — partial, not a standing instrument |
| "Downstream patch-offset check" | 1 (`round-69.md:109`; adoption at `round-42.md:53,56`) | 0 (the r42 script is named at `:3956`) | adopted r42 as a script and landed again r69 as QUALITY 103 — one-shot instrument, no standing ledger |

Conflict recorded verbatim, not resolved here: the claim "every proposal … is already implemented"
holds for one of five by the standing-instrument test (`Counter-attack scoreboard`), partly for two
(`Seat-harm incident log` as a lessons-only tally; `Downstream patch-offset check` as an adopted
check), and does not hold for `Burst-aware reading` (single mining record, explicitly not a gate) or
`correction propagation map` (recorded partial). The "three hits per proposal" form is met only by
`Seat-harm incident log` (3 lessons hits) and `Counter-attack scoreboard` (7 lessons / 5 `SKILL.md`).
No new proposal is mined this round, and the scoreboard above is a continuation, as instructed.

## Trend verdicts

Skeleton only — the L1 fills each verdict; this seat asserts none.

- **expansion: `(L1 fills)`** — evidence pointers to read: `grep -cE '^\| S[0-9]{3,}' corpus/SOURCES.md`
  at the final tree (289 at base, declaration and this HEAD; target 293);
  `corpus/knowledge/xfs-storage-plane-r70.md` (absent at this HEAD, `git cat-file -e` rc 128); the
  C1 counter's `XS_ROWS/XS_VERIFIED/XS_SOURCES/XS_SNAPSHOTS` receipt at the final tree (path
  `(L1 fills)`); the two capability/registry rows the round declares.
- **quality: `(L1 fills)`** — evidence pointers: `before/control/battery.txt` (8/8, 7 mutants
  killed); the two Mistakes rows above and whether their fixes landed; the D1 erratum in this
  lesson; the D2 receipt at the final tree (`probes/E3Repairs/cited-r70-at-decl.txt` is the
  declaration-revision PASS; the final-tree receipt is still owed); `w1/R1Reviewer.md` Finding 2
  (11 mutants, 7 refused, 4 survivor channels — M4 substance floor, M5 duplicate-snapshot, M6
  unread anchor, M11 invisible row) and whether any was closed in-round; `probes/R2Reviewer/` and
  `probes/M1Mutation/` (absent at draft time).
- **discernment: `(L1 fills)`** — evidence pointers: S1Scout's second-route equality
  (`ROUTE2_OK=4/4`); E2Capture's independent counts and its divergence from the declaration's
  "7 regular files" prose (Mistakes 2); R1Reviewer's independent re-derivation (`DERIVED_OK=6/6`)
  and its one LOW wording note on XS6; the non-author closure spot-check for this round (fleet
  report, path `(L1 fills)`); the seats still silent at draft time (`R2Reviewer`, `M1Mutation`,
  `K1Critic`, no `w1/E1XfsArm.md`).

## Seat notes

- Scratch `/fast/scratch/hyaku/tsukuroi-r70/SC3Lesson` was created and removed before yield.
- One inadvertent write outside this seat's scope, disclosed and reverted: importing the frozen
  counter (`importlib`) for the row-local clause check produced
  `tools/__pycache__/count-xs-rows-r70.cpython-314.pyc` in the lane tree at 21:14; it was removed at
  21:16, `tools/` holds no `__pycache__`, and `git status --porcelain -- tools/` prints 0 lines (no
  tracked change). Nothing else was written outside `.ufo/waves/round-70/w1/`.
- No tool install or upgrade was needed or performed (no pacman transaction; PACMAN GUARD untouched).

Key definitions for the line below: `GATE_QUOTES` counts the four admitted-row located quotes in
`## Gate` (the two D1-erratum quotes are recorded there and not counted); `D1_ERRATUM` is 1 because
the erratum block above exists; `MISTAKE_ROWS` counts `## Mistakes` rows; `SCOREBOARD_ROWS` counts
data rows of the continuation table; `UNFILLED` counts table cells literally reading `unfilled`
(the one prose use in the legend is not counted).

GATE_QUOTES=4 D1_ERRATUM=1 MISTAKE_ROWS=2 SCOREBOARD_ROWS=5 UNFILLED=9
