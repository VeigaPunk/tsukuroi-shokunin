# DraftAxesTable — round-25 after-state SCORECARD sections (K01–K19 text)

Seat: `TsukuroiR25.DraftAxesTable` (scribe, wave 1). Date: 2026-10-22.
Scope: draft the text of the two appended SCORECARD sections that the round-25 C1
self-assessment check set reads. No lane production file was edited; nothing was
committed, pushed or written outside this seat directory.

Verdict: the draft below is ready for the L1 to append verbatim after filling five
`<N>` placeholders; the six ordinals it states (depth 8, coverage 9, operability 9,
freshness 9, calibration 9, adjacency 8) match the lane's own last recorded ordinal
transitions, and every phrase the K07–K19 checks read is present in the wording the
C1 refinement fixed.

---

## Findings

1. **The stale table is the round-11 one, and it is the only axes table in the file.**
   [obs] `grep -n '^## Axes' SCORECARD.md` at the claim base `b9046016` returns one
   line, `39:## Axes — final self-assessment (landed round 11; ...)`; the same grep
   at HEAD `0cd9b28bee5fd5a50d991e6dee0c0d0f48b15935` returns the same single
   heading. `grep -n '^## Capabilities' SCORECARD.md` returns one line, `157`.
   [inf] The new sections must be appended at the end of the file so the new axes
   heading is the last `## Axes — ` heading and the new capabilities heading is the
   last `## Capabilities` heading; the round-11 table stays in place as the
   historical record.

2. **K01–K06: the six scores must equal the after-value of the last ordinal
   transition recorded outside the current axes table.** [obs] Applying the fixed
   regex from `SCORECARD.md:807` to HEAD, the last match per axis is:
   `depth` line 793 `depth 8 → 8` → 8; `coverage` line 224 `coverage 8→9` → 9;
   `operability` line 621 `operability9→9` → 9; `freshness` line 772
   `freshness (actual 9 → 9` → 9; `calibration` line 792 `calibration 9 → 9` → 9;
   `adjacency` line 620 `adjacency 8→8` → 8. These match the ordinals the round-25
   declaration states (`SCORECARD.md:786`) and the ordinals at `SCORECARD.md:786`.
   The `coverage rows 10 → 15` example inside the refinement text at line 807 is
   excluded by the declared 0-to-10 bound on the second number, as intended.
   [inf] Consequence for the draft: the new sections are appended after every
   existing line, so **no** `axis N → M` pattern may appear in their prose or in the
   capabilities table, or it would become the last match. The draft uses the words
   "to" instead of an arrow outside the fixed evidence quotes, and the axes table
   carries its counts only as bare numbers.

3. **K07–K13: the counts the stale rows state, and the values that replace them.**
   [obs] Measured on a `git archive b9046016` extraction
   (`/fast/scratch/hyaku/tsukuroi-r25/DraftAxesTable/base`):
   `ls corpus/knowledge/*.md | wc -l` → 46; `wc -l < SKILL.md` → 2301;
   `grep -c '^|' SKILL.md` → 259; `find corpus/lessons -type f | wc -l` → 25 (all
   25 are `.md`); `wc -l < corpus/README.md` → 231.
   The round-11 rows state 24 notes, `SKILL.md` 1631, 55 table lines, 0 lesson files
   and `corpus/README.md` 20 `wc -l` — all stale.
   [obs] `bash tools/tsukuroi-census.sh --selftest` in that extraction exits 0 and
   prints `TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)` (two
   explicit SKIP lines, not counted in the total). The round-11 operability row says
   80 cases. `ExecHermeticSelftests` measured the same 97 at `6c580b15`, at
   `0cd9b28` and at `master`; the census script bytes
   (`sha256 d17d32a35946c71c1fc195e36178aa383f4a04f7172cc579b6e9e25fa537f27e`) are
   identical across those revisions, so 97 holds unless the census script itself
   changes this round. No round-25 seat edits `tools/tsukuroi-census.sh`.
   [obs] `bash tools/boot-chain-audit.sh --selftest` in the same extraction exits 0
   and prints `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=45 failed=0`. The round-11
   Capabilities cell says `44/44`; `SCORECARD.md:554` already records that the
   historical 44/44 is superseded by the landed round-17 measurement 45/45. The new
   Capabilities row states 45.

4. **K12, K14 and K15 are decided by the fixed tokens in the C1 refinement, not by
   free wording.** [obs] `SCORECARD.md:808` fixes them: stated absent when the
   coverage row contains `Core/Frontier/Adjacent not landed`, stated present when it
   contains `Core, Frontier and Adjacent sections present`; `--identity` stated as
   `` `--identity` not landed `` or `` `--identity` landed ``, observed present only
   when `tools/tsukuroi-census.sh` has a case arm matching `^\s*--identity\)`; the
   overlap table stated as `no formal overlap table` or `formal overlap table
   present`, observed present when PROVINCE.md has a line starting `| ID | Finding`.
   [obs] Observed state: `grep -nE '^\s*--identity\)' tools/tsukuroi-census.sh`
   → no match, and `grep -c -- '--identity' tools/tsukuroi-census.sh` → 0, so
   `--identity` is **not landed**; `grep -n '^| ID | Finding' PROVINCE.md` →
   `44:| ID | Finding / boundary trigger | ...`, so the overlap table **is present**;
   `grep -n '^## ' PROVINCE.md` → `6:## Core`, `35:## Adjacent — finding-to-owner
   handoffs`, `75:## Frontier`, `108:## Adjacent — portable ownership anchors (round
   19)`, so Core, Frontier and Adjacent are all present.
   [inf] The round-11 rows state the opposite on all three; the draft states the
   observed state with the fixed token wording and never contains a negated token.

5. **The draft removes three path-grammar hazards that the round-11 Capabilities
   rows still carry.** [obs] The declared grammar is "A token is a path when it
   contains `/` or ends in `.md`, `.json`, `.py`, `.sh` or `.txt`". The round-11
   capabilities rows contain three backticked spans that satisfy that rule but are
   not repository paths: `HEALTHY/DEGRADED/BLOCKED` and `/new_root` (both contain a
   slash) and the bare `after.md` (ends in `.md`, but no such file at the repository
   root). [obs] `git cat-file -e b9046016:after.md` exits non-zero.
   [inf] The draft writes "HEALTHY, DEGRADED or BLOCKED", "the new_root path" and
   the full path `.ufo/evidence/round-1-kaika/after.md`, so under the declared
   grammar every path-like token in the new Capabilities cells resolves to a file
   that exists. If the tool's tokenizer is stricter than that, the new rows are
   still clean.

6. **Markdown pipe escaping is mandatory inside the new table cells.** [obs] The
   round-11 depth row (`SCORECARD.md:47`) writes its counting commands with escaped
   pipes (`` `ls corpus/knowledge/*.md \| wc -l` ``, `` `grep -c '^\|' SKILL.md` ``),
   and the round-11 row must parse at `b9046016` for K07 to be a mismatch rather
   than a setup error.
   [inf] A table-row splitter must therefore treat `\|` as content and split only
   on unescaped pipes. I verified the draft with exactly that rule: every row of
   both tables splits into four cells. The draft keeps the same escaped-pipe
   convention as the round-11 rows, and puts each count immediately before the
   keyword its check reads (`notes`, `wc -l`, `table lines`, `files`, `cases`), so
   the numbers are adjacent to their keywords however the command text is
   tokenized.

7. **Both new tables must be the last table under their own heading, and the tool
   resolves headings section-scoped, so the order is settled.** [obs] The tool
   builder (`TsukuroiR25.ExecSelfAssessTool`) confirmed the implementation: it
   scans forward from the last heading matching `^##\s+Axes\s+[—-]\s` to the next
   `^## ` heading and takes the last table in that range whose header first cell
   is `Axis`; for capabilities it scans from the last heading matching
   `^##\s+Capabilities\b` and takes the last table whose header first cell is
   `Capability`. [inf] Either order therefore works, and the draft keeps the
   file's existing order (Axes first, Capabilities second) as the tool builder
   requested. The draft's two headings satisfy those patterns: `## Axes — current
   self-assessment (round 25)` (em dash, `e2 80 94`, verified by hexdump) and
   `## Capabilities — current (round 25)`.
   [obs] The tool builder also fixed the reading predicates, which the draft
   matches: K07 `(\d+)\s+notes\b`, K08 the number between `SKILL.md` and `wc -l`,
   K09 `(\d+)\s+table lines\b`, K10 `(\d+)\s+files?\b` after `corpus/lessons/`,
   K11 the number between `corpus/README.md` and `wc -l`, K13 the first of
   `PASS (N cases`, `N cases`, `N-case`, `PASS N/N`, K14 the literal
   `` `--identity` not landed ``, K15 the literal `formal overlap table present`,
   K12 the literal `Core, Frontier and Adjacent sections present`.
   [inf] On the tool builder's own reading, the round-11 table mismatches K02
   (coverage), K04 (freshness) and K06 (adjacency) on score plus the seven stale
   counts and the K15 wording; the drafted table states coverage 9, freshness 9
   and adjacency 8 and carries the fixed tokens, so those become matches.
   [obs] The tool builder reports that with a corrected axes and capabilities
   table appended in this style the tool reads 0 of 23 mismatches and exits 0.
   That is the tool builder's own statement about its own tool; the round-25
   measurement of the integrated revision remains the L1's to take.

8. **K16–K19: every path named in the new Capabilities rows exists at the claim
   base.** [obs] `git cat-file -e b9046016:<path>` → exit 0 for
   `corpus/SOURCES.md`, `.ufo/evidence/round-1-kaika/after.md`,
   `.ufo/evidence/round-1-kaika/scout-live.md`, `tools/tsukuroi-census.sh`,
   `.ufo/waves/round-12/resumed/after.json`,
   `.ufo/waves/round-12/resumed/selftest-after.json`,
   `.ufo/waves/round-12/resumed/mode-policy-mutant.json`,
   `tools/boot-chain-audit.sh`, `.ufo/waves/round-17/l1-capture/audit-live.txt`;
   the commit `70fede2a7a890cb50a72db2d4230ee541183bf7b` exists and is an ancestor
   of `6c580b15`. `ExecHermeticSelftests` reports the same list at `6c580b15`.
   [inf] The draft keeps every backticked span in the Capabilities cells either a
   path that exists or a token with no slash and no `.md`, `.json`, `.py`, `.sh` or
   `.txt` ending. Each of the four rows names at least one path, as the "a row that
   names no path is a mismatch" rule requires.

9. **K20–K23 (SHONEN): no `[x]` box, but box 2 held one prose slash that the
   literal path grammar reads as a named path.** [obs] `SHONEN.md` has four
   `- [~]` boxes and `grep -c '^- \[x\]' SHONEN.md` → 0, so the "non-author
   verifier" clause cannot fire. [obs] The bare path tokens in the boxes
   (`SKILL.md`, `corpus/knowledge/root-dac-decision-r12.md`,
   `corpus/knowledge/host-health-report-r3.md`, `LOG.md`,
   `corpus/knowledge/adjacency-handoffs-fleet-r1.md`,
   `corpus/knowledge/executor-test-sufficiency.md`, `PROVINCE.md`,
   `.ufo/waves/round-12/resumed/OverlapHostR.md`) all exist at `b9046016`.
   [obs] The tool builder measured one further K21 mismatch at `0cd9b28` that my
   own scan had missed: box 2's evidence line reads "current sanitized
   observation/request TSUKUROI-F1-MEM-01 in
   `corpus/knowledge/adjacency-handoffs-fleet-r1.md` section 3", and under the
   literal grammar the token `observation/request` matches
   `[A-Za-z0-9_.{},/-]+`, holds a slash and names no tree at the revision.
   [inf] My earlier "needs no edit" reading was wrong because I only enumerated
   tokens that looked like file names, not every token the grammar admits. The
   L1 fixed it in the integration by rewording that phrase to "observation and
   request" — the only changed line in `git diff b9046016 5e7c04e -- SHONEN.md`.
   K20 to K23 now match.

10. **Placeholders the L1 must fill, with the base values as a sanity bound.**
    [obs] Base values at `b9046016` are in finding 3. [inf] All five will move this
    round: the C2 entry adds a knowledge note, the C2 SKILL section adds lines and
    decision-table rows, the round-25 lesson adds a file under `corpus/lessons/`,
    and `corpus/README.md` may gain a row. Fill with the commands in the table
    below, on the final measured revision.

    | Placeholder | Row | Fill with | Command | Base value at `b9046016` |
    |---|---|---|---|---|
    | `<N>` notes | depth | count of knowledge notes | `ls corpus/knowledge/*.md \| wc -l` | 46 |
    | `<N>` after `SKILL.md` | depth | SKILL.md line count | `wc -l < SKILL.md` | 2301 |
    | `<N>` table lines | depth | SKILL.md table lines | `grep -c '^\|' SKILL.md` | 259 |
    | `<N>` files | depth | files under `corpus/lessons/` | `find corpus/lessons -type f \| wc -l` | 25 |
    | `<N>` after `corpus/README.md` | coverage | README line count | `wc -l < corpus/README.md` | 231 |

    The census case count is **not** a placeholder: it is 97 unless the census script
    changes this round. Re-verify with
    `git archive <REV> | tar -x -C <tmp> && (cd <tmp> && bash tools/tsukuroi-census.sh --selftest)`
    on the final revision before integration.

---

## Final state: integrated and verified

[obs] While this seat was still reporting, the L1 integrated the round at
`5e7c04ecb02735491456de2b8bc44550d0db4609` ("round-25: C1 self-assessment checker
and current axes table; C2 memory-pressure entry, sources S115-S125, checker,
SKILL table and registry; lesson, QUALITY 57-59, LOG; wave-1 evidence"). I
verified the integrated revision myself, read-only, against the lane repo:

`python3 tools/check-self-assessment.py --revision 5e7c04ecb02735491456de2b8bc44550d0db4609`
exits 0 and prints `status: PASS`, `mismatches: 0`, `checked: 23`, with every one
of K01 to K23 reported `match`. The tool's own reasons for the checks that read
my table: K01 depth 8 against the transition at `SCORECARD.md:793`; K02 coverage 9
against `:224`; K03 operability 9 against `:731`; K04 freshness 9 against `:807`;
K05 calibration 9 against `:792`; K06 adjacency 8 against `:620`; K07 47 notes
against 47 `.md` files in `corpus/knowledge/`; K08 2355 `SKILL.md` lines; K09 297
table lines; K10 26 lesson files; K11 231 `corpus/README.md` lines; K12 the
sections present with Core, Frontier and Adjacent all true; K13 97 cases equal to
the census selftest at that revision; K14 the mode absent with the census holding
no `--identity` case arm; K15 the table present with a `| ID | Finding` table in
PROVINCE.md.

[obs] The integrated text is my draft with the five `<N>` placeholders filled by
the L1 at the measured revision: 47 notes, `SKILL.md` 2355 `wc -l`, 297 table
lines, 26 lesson files, `corpus/README.md` 231 `wc -l`. A cell-by-cell diff of
the integrated rows against my draft shows no other change to the axes rows; the
one intentional addition is in the `sources-registry` capability cell, where the
L1 added "125 rows at round 25" to the `corpus/SOURCES.md` description, which
keeps the row current after the round's S115-S125 source rows landed.

[obs] The SHONEN defect the tool builder raised was fixed in the same
integration. [obs] `git diff b9046016 5e7c04e -- SHONEN.md` shows exactly one
changed line: the box-2 evidence phrase "current sanitized observation/request
TSUKUROI-F1-MEM-01" became "current sanitized observation and request
TSUKUROI-F1-MEM-01", removing the slash that the literal path grammar read as a
named path. [obs] Under that grammar every path token in the four SHONEN boxes at
`5e7c04e` now resolves: box 1 names 2, box 2 names 3, box 3 names 3, box 4 names
2, and the tool reports K20 to K23 as matches.

[inf] The C1 target as declared — 0 of the 23 fixed checks mismatching, exit 0 —
is met at the integrated revision, measured by the round's own tool on committed
bytes. No ordinal moved, no capability row was added or removed, and the two
sections I drafted are the current axes table and the current capabilities table
of the lane.

[obs] The tool that produced the after-value is the tool as written: `git show
5e7c04e:tools/check-self-assessment.py | sha256sum` gives
`343367fb309e43449ee1be50f97c86b917240de7bb6b34b942fd67a163c6242f`, byte-identical
to the working-tree copy, and `git status --porcelain tools/check-self-assessment.py`
is empty. The after-value of 0 was therefore not measured with a modified
checker.

[obs] The before-value is 13 of 23, not the 12 the L1 predicted by hand count at
the declaration (`SCORECARD.md:792`). I measured it myself with the same tool at
the claim base: `python3 tools/check-self-assessment.py --revision b9046016` exits
1 with `status: FAIL`, `mismatches: 13`, `checked: 23`, mismatching K02, K04,
K06, K07, K08, K09, K10, K11, K12, K13, K15, K17 and K21. The extra one is
exactly K21, the SHONEN box-2 prose slash that the hand count did not catch for
the same reason my own enumeration missed it. The tool builder's before-table at
`.ufo/waves/round-25/w1/ExecSelfAssessTool/` records the same 13 ids, and its
receipts name the three revisions measured: `c1-base-b9046016.json`,
`c1-decl-0cd9b28.json` and `c1-after-5e7c04e.json`.
[inf] So the declaration's hand-count prediction of 12 was one short, and the
route to the true count was the tool, not a re-reading of the prose. That is the
same lesson the round's own C1 claim makes: the lane's self-assessment is now
measured rather than asserted.

[obs] Operational note, confirmed by both of us: the checker needs the Git
repository, so it must be run from the lane repo or with `--repo` pointing at
one. A `git archive` extraction has no `.git` and the tool answers
`CANNOT_EVALUATE` with "not a git repository", exit 2 — the intended refusal,
not a pass.

---

## Local re-simulation of the K01–K19 rules over base plus these two blocks

[obs] I concatenated the `git archive b9046016` extraction of `SCORECARD.md` with
the two draft blocks below and ran the declared rules against the result with a
section-scoped table finder and a backslash-aware cell splitter. Results:

| Check | Result on the draft |
|---|---|
| K01 to K06 | last ordinal match outside the axes table gives depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8 — all six equal the drafted scores |
| K07 to K11 | the five `<N>` placeholders sit immediately before `notes`, `wc -l`, `table lines`, `files` and `wc -l`; they read empty until the L1 fills them, as expected |
| K12 | `Core, Frontier and Adjacent sections present` present, `Core/Frontier/Adjacent not landed` absent |
| K13 | `97 cases` present in the operability row |
| K14 | `` `--identity` not landed `` present, `` `--identity` landed `` absent |
| K15 | `formal overlap table present` present, `no formal overlap table` absent |
| K16 to K19 | four named capability rows; every path-like token in them resolves at `b9046016` (2, 3, 3 and 2 path tokens per row, none missing); the host-census-gate row states 97 cases, equal to the K13 observed count |
| table shape | every row of both tables splits into exactly four cells under the backslash-aware splitter |
| arrow audit | no `→` or `->` in either draft block, so no drafted line can become the last ordinal transition |

[inf] This is a local re-implementation of the declared rules, not the round-25
tool; it shows the drafted wording is readable by the fixed tokens, not that
`tools/check-self-assessment.py` returns 0 mismatches.

[obs] Second run, after the tool builder published its exact predicates: I
substituted the base-measured values into the five placeholders (46, 2301, 259,
25, 231 in document order) and re-ran the tool builder's own readings over the
result. K07 `(\d+)\s+notes\b` → 46; K08 the number between `SKILL.md` and
`wc -l` → 2301; K09 `(\d+)\s+table lines\b` → 259; K10 `corpus/lessons/` then
`(\d+)\s+files?\b` → 25; K11 the number between `corpus/README.md` and `wc -l`
→ 231; K13 `PASS (N cases` → 97; K12, K14 and K15 literals present; K01–K06
last-match values depth 8, coverage 9, operability 9, freshness 9, calibration 9,
adjacency 8. All four capability rows name at least one path and none of their
path tokens is missing at `b9046016`; the host-census-gate row reads 97 in both
the `97-case` and `PASS 97/97` forms, agreeing with K13's observed 97. Every row
of both tables splits into four cells. No arrow appears in either block.

## Draft text — append to `SCORECARD.md` (verbatim, after filling the `<N>` placeholders)

```markdown
## Axes — current self-assessment (round 25)

Appended 2026-10-22 by the round-25 C1 repair (routed defect 1 in
`corpus/lessons/round-24-verifier-spotcheck.md`). This table supersedes the
round-11 table above as the lane's current self-assessment; the round-11 table
stays in the file as the historical record of that round. Each score is the
lane's current ordinal and each evidence pointer carries the command that
re-derives the number it quotes. C1 repairs the measurement, it does not move an
ordinal: the six scores below are the same ordinals the lane's later move
records carry. The counts marked `<N>` are filled by the integrator at the final
measured revision with the command named in the same cell.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | <N> notes (`ls corpus/knowledge/*.md \| wc -l`); `SKILL.md` <N> `wc -l`; <N> table lines (`grep -c '^\|' SKILL.md`); `corpus/lessons/` <N> files (counted with `find corpus/lessons -type f` and `wc -l`); every rule in `SKILL.md` cites a `corpus/knowledge/*.md` note. Ceiling: the depth ordinal was last moved at round 4, and rounds 12 to 24 each record depth 8 to 8 with no change, so this row restates a score the round did not move. | round 4 (move-log row at `SCORECARD.md:30`); unchanged since |
| coverage | 9 | `corpus/README.md` <N> `wc -l`; `PROVINCE.md` Core, Frontier and Adjacent sections present (`## Core` at `PROVINCE.md:6`, `## Frontier` at `PROVINCE.md:75`, `## Adjacent` at `PROVINCE.md:35`); six gate planes equal the surfaces `PROVINCE.md` owns, each with a landed note; the four declared read-only surfaces of fleet round 1 (Arch News upgrade gate, `.pacnew` drift, initramfs v42, snapper net) each link one knowledge entry. Ceiling: the coverage ordinal was last moved by the fleet round-1 post-review correction; the K3 upstream delta (network read) still awaits an operator boundary ruling. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:224`; unchanged since |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (97 cases, 97 passed, 0 failed) with exit 0; the live run exits 1 with a six-plane rollup; the zero-mutation contract holds (no fixture byte changes, no `db.lck`); D12 `--identity` not landed, so the three-command re-derivation still stands. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged since |
| freshness | 9 | each round's record re-ran its predecessor's pins; the receipts `aur-drift-receipt-r9.md`, `census-closeout-receipt-r10.md` and `closeout-r11.md` recheck block hold the re-run evidence; the fleet round-1 dated D1 to D5 erratum rechecks (7 notes, 25 of 25 per-note rechecks) are the current floor; live counts such as the coredump directory size are captures, not durable state. Ceiling: a count captured now is superseded by the next capture; the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:240`; unchanged since |
| calibration | 9 | `corpus/knowledge/calibration-synthesis.md` holds the claim, re-measure, append, supersede, rule loop with its mismeasure rows; errata stay visible instead of being rewritten (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction); the register is the `closeout-r11.md` section 3 block; this round's C1 makes the lane's own table measurable against repository state, which is what the r10 ceiling asked for. Ceiling: the D13 verification debts stay open. | round 10 (`SCORECARD.md:36`); unchanged since |
| adjacency | 8 | reported-not-absorbed rows across the arc (coredump storm to the journal workstream and the app lanes, `walker-restart.hook` root-exec to kagi, GSP selection to kaidoku and revenger); `PROVINCE.md` carries the formal overlap table present (the ADJ-01 to ADJ-07 finding-to-owner handoff table at `PROVINCE.md:44`, with the round-19 portable ownership anchors OUT-001 to OUT-010); contested scope is reported, never absorbed. Ceiling: recipient acknowledgement and independently replayed handoffs are not verified. | fleet round 1 (2026-10-19), post-review correction at `SCORECARD.md:213`; unchanged since |

Scores are ordinals carried by the lane's own records, not a fresh measurement of
this round. The counting commands above are the only source of the quoted counts;
re-run them at the revision being claimed before treating any number here as
current.
```

```markdown
## Capabilities — current (round 25)

Appended 2026-10-22 with the round-25 C1 repair. This table restates the four
capability rows of the round-11 section at `SCORECARD.md:157` against the
repository state at the final measured revision. No capability row is added or
removed this round and no row claims a new capability: the round-25 tools are
gates, not capabilities. Each path pointer was re-checked against the round-25
claim base with git cat-file, and the host-census-gate case count was re-measured
by running the census selftest against a git archive of the revision.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates where the lane learns: `corpus/SOURCES.md` holds opened, tier-scoped rows with anchors, rejections with flips, study paths, a search log and unopened leads, and the row set is checked by the frozen contract's census commands | `corpus/SOURCES.md`; the census commands and their outputs in `.ufo/evidence/round-1-kaika/after.md` (34 rows in that snapshot, malformed 0, no duplicate, enum or missing output) | fleet r1 (2026-10-19) |
| host-census-gate | Emits a read-only six-plane host verdict (TSUKUROI_CENSUS: HEALTHY, DEGRADED or BLOCKED; exit 0, 1 or 2) with a hermetic 97-case selftest that touches no live host surface | `tools/tsukuroi-census.sh` selftest prints PASS 97/97 rc=0 (97 cases, 97 passed, 0 failed); the live run exits 1 with a six-plane rollup; receipts `.ufo/evidence/round-1-kaika/scout-live.md` and `.ufo/evidence/round-1-kaika/after.md` | lane r2 (census-v1); demonstrated running fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations even on package-probe failure; isolates fixtures and blocks unavailable or non-directory metadata without grading intentional 0555 policy | `.ufo/waves/round-12/resumed/after.json`, `.ufo/waves/round-12/resumed/selftest-after.json`, `.ufo/waves/round-12/resumed/mode-policy-mutant.json`; measured commit `70fede2a7a890cb50a72db2d4230ee541183bf7b` | round 12 |
| boot-chain-audit | Audits every limine entry live and read-only: copies each UKI with a read-only `sudo -n cat`, extracts its initramfs in a private mktemp directory, types the new_root path, binds the firmware-selected entry, and emits a per-entry next-boot verdict plus TSUKUROI_BOOTCHAIN | `tools/boot-chain-audit.sh` live run wrote `.ufo/waves/round-17/l1-capture/audit-live.txt` (6 entries, CONSISTENT, exit 0); its selftest prints PASS total=45 failed=0 | round 17 |

Rows enter only through a round that demonstrates the capability running; none
enter through this rollout. The boot-chain-audit selftest count in the round-11
table (44 of 44) is superseded here by the landed round-17 measurement of 45
cases with 45 passed and 0 failed, and the host-census-gate count is the current
97 cases, not the 80 of the round-11 table.
```

---

## Integration notes for the L1 (as given; the integration has since landed)

These notes were written before integration and are kept as the record of what
the L1 was told. The L1 integrated the draft at `5e7c04e` and the checker passes
23 of 23 there — see "Final state" above.

- Append both sections at the end of `SCORECARD.md`, in the order given above
  (Axes first, Capabilities second), with no further `## Axes — ` or
  `## Capabilities` heading after them. The tool resolves headings
  section-scoped, so this order is the confirmed one (finding 7).
- Fill the five `<N>` placeholders with the commands in finding 10, at the final
  measured revision. Keep each count immediately before the keyword the check
  reads: `N notes` (K07), `SKILL.md` N `wc -l` (K08), `N table lines` (K09),
  `corpus/lessons/` N files (K10), `corpus/README.md` N `wc -l` (K11).
- Do not introduce an `axis N → M` pattern in any prose of the new sections, and
  keep the round-25 outcome rows at 0-delta ordinals, so the last ordinal
  transition for each axis still yields depth 8, coverage 9, operability 9,
  freshness 9, calibration 9, adjacency 8.
- Re-measure the census case count at the final revision; it is 97 at
  `b9046016`, `6c580b15`, `0cd9b28` and `master` with identical census bytes.
- A `SHONEN.md` edit was needed after all: box 2's phrase "observation/request"
  names a path under the literal grammar. The L1 reworded it to "observation and
  request" in the integration (finding 9).
- Verify with `python3 tools/check-self-assessment.py --revision <REV>`; the
  expected result is 0 mismatches of 23 with exit 0.

Scope: read=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md` (lines 39-53, 157-169, 182-243, 244-813 and the integrated sections at 815-866), `PROVINCE.md`, `SHONEN.md`, `tools/tsukuroi-census.sh`, `tools/boot-chain-audit.sh`, `tools/check-self-assessment.py`, `corpus/knowledge/`, `corpus/lessons/`, `.ufo/waves/round-25/w1-spec.json`, `.ufo/waves/round-25/w1/ExecHermeticSelftests/summary.json`, `.ufo/waves/round-25/w1/ScoutPlanWalk.md`; wrote=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/DraftAxesTable.md`; executed=`git archive b9046016 | tar -x -C /fast/scratch/hyaku/tsukuroi-r25/DraftAxesTable/base`, `git archive 5e7c04e | tar -x -C /fast/scratch/hyaku/tsukuroi-r25/DraftAxesTable/head`, `ls corpus/knowledge/*.md | wc -l`, `wc -l < SKILL.md`, `grep -c '^|' SKILL.md`, `find corpus/lessons -type f | wc -l`, `wc -l < corpus/README.md`, `grep -c '^\x7c' SKILL.md`, `bash tools/tsukuroi-census.sh --selftest` (exit 0, 97 cases), `bash tools/boot-chain-audit.sh --selftest` (exit 0, total=45), `python3 tools/check-self-assessment.py --revision 5e7c04e` (exit 0, PASS, 0 mismatches of 23), `python3 tools/check-self-assessment.py --revision b9046016` (exit 1, FAIL, 13 mismatches of 23, ids K02 K04 K06 K07 K08 K09 K10 K11 K12 K13 K15 K17 K21), `sha256sum tools/check-self-assessment.py` and `git show 5e7c04e:tools/check-self-assessment.py | sha256sum` (both `343367fb309e43449ee1be50f97c86b917240de7bb6b34b942fd67a163c6242f`), `grep -n '^## ' PROVINCE.md`, `grep -n '^| ID | Finding' PROVINCE.md`, `grep -nE '^\s*--identity\)' tools/tsukuroi-census.sh` (no match), `grep -c -- '--identity' tools/tsukuroi-census.sh` (0), `grep -c '^- \[x\]' SHONEN.md` (0), `git cat-file -e <rev>:<path>` for each cited path, `git ls-tree -r --name-only <rev> corpus/...`, `git diff b9046016 5e7c04e -- SHONEN.md`, read-only `git show`, `git log`, `git status`, `git diff --stat`, plus three local python re-simulations of the K01–K19 rules over base plus these two draft blocks; no lane production file written, no push, no fetch, no package transaction, no service change.
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
