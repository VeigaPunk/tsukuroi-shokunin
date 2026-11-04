# Round 73 — lesson (tsukuroi, hyaku run 15, attempt 1)

author: tsukuroi L1 (round 73), integrating the wave `.ufo/waves/round-73/` (12 seats, one v1 wave).
basis: declaration `749371321c00f04d98c29d2c26b57d75a92d7e37` (frozen before data; base
`eb1057575d5d8b940c4846e21611674cf5571aea`); pre-data receipts in `.ufo/waves/round-73/before/`;
measured revision `583eea87627353d6e21037216e316af8e19bdf4d`.

## Gate

**Trigger.** The systemd unit-load merge plane — the rules that decide which bytes become a unit — was
held-ground-zero at the declaration base: `git grep -nE 'unit_load_dropin|dropin_paths|
unit_need_daemon_reload|null_or_empty|unit_file_mask|config_parse_alias' -- corpus/ SKILL.md
PROVINCE.md` read **0 lines**, `unit load path`/`unit search path`/`FragmentPath`/`DropInPaths` read
**0 files**, and the twelve `corpus/knowledge/` `drop-in` mentions are host observations of named files
(`systemd-user-plane.md:29,44`, `kill-event-deep-r8.md:258,263`, `degraded-triage-r4.md:358`) or mkinitcpio
hook contexts, none of them a merge rule (`.ufo/waves/round-73/before/held-ground.txt`).

**Pins.** Three systemd **v262** snapshots, fetched before the declaration text and committed byte-exact
with `SHA256SUMS` and `SOURCES.json` under `.ufo/waves/round-73/before/src/`; the host runs
**262.1-1-arch** (`systemctl --version`), so the tag matches the build's release. Access date
**2026-11-03**. S1Scout re-fetched all three by a second route (`github.com/.../raw/v262` and the tag
tarball): `ROUTE2_OK=3/3`, byte-identical; the six planned quotes sit at the recorded lines and
`HOST_DELTAS=0` over fifteen re-measured checks (`w1/S1Scout/report.md`).

| id | snapshot | sha256 | rows |
|---|---|---|---|
| **S304** | `man/systemd.unit.xml` | `eb9479be…f82714c6` | UL1, UL2 |
| **S305** | `src/core/unit.c` | `47e98d39…42a92efcb7` | UL3, UL4 |
| **S306** | `src/shared/install.c` | `c11cd575…e6ef4d` | UL5, UL6 |

Gate quotes (each ≤25 words, located in its snapshot): S304 `systemd.unit.xml:367-370` "Unit files found
in directories listed earlier override files with the same name in directories lower in the list",
`:238-240` "Multiple drop-in files with different names are applied in lexicographic order, regardless of
which of the directories they reside in", `:236-238` "Drop-in files under any of these directories take
precedence over unit files wherever located"; S305 `unit.c:3874-3875` "For masked files check if they are
still so", `:3908` "any drop-ins that are masked are simply omitted from the list"; S306
`install.c:2387` "path = path_make_absolute(*name, config_path);", `:351` "Unit %s is an alias to a
non-existent unit, ignoring."

**Admitted.** Three rows, all tier A `mined`: S304 (docs), S305 (code), S306 (code), cited by
`corpus/knowledge/systemd-unit-load-plane-r73.md` (UL1-UL6). At the measured revision `583eea87` the frozen
counter reads `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `met=1`, rc 0
(`.ufo/waves/round-73/after/measure-583eea87.txt`); the registry reads 308 rows and every new row is
`NF=13`; the canonical census reads rc 0.

**Refused (R72-GATE-NO-REJECT exercised — one real refusal with reason and flip).**

| id | candidate | fetch | verdict |
|---|---|---|---|
| S307 | `https://man.archlinux.org/man/systemd.unit.5` (rendered Arch man page) | HTTP 200, 135978 bytes, sha256 `69dba097…` identical across two fetches | **rejected** — `REJECTED: the rendered page is the same upstream manual source already pinned as S304 and shows no divergence in any merge or precedence sentence compared, so it grounds no rule S304 does not; flip: a rendered page carrying an Arch patch that changes the merge, precedence or mask text` |
| S308 | `https://archlinux.org/packages/core/x86_64/systemd/` (core package page) | HTTP 200, 101009 bytes, body names `systemd 262.1-1`; two fetches differ only in a per-response CSP nonce | **rejected** — `REJECTED: the page is build provenance only (version, packager, build date) and states no merge, precedence or mask rule, and the host's installed version is already an own-work host reading; flip: a package note or patch list that names a change to the unit-loading code or its manual page` |

Both refusals are *opened* sources with measured fetches, not bare names; neither is a duplicate-id or
render-only rubber stamp of a row the lane already holds (`w1/SC2Sources/rows.md` carries the measurement
log, including the nonce-only diff that made a content digest unquotable).

**Non-author spot-check.** Owed to the closure judge, which re-opens the three URLs live and records its
admit/reject agreement (S307/S308 included). No author-side `[x]` is written.

**Census.** Round start: canonical validate rc **0**, **303** registry rows, **90** knowledge notes.
Round end at `583eea87`: rc **0**, **308** rows (three mined, two rejected), **91** notes.

## Admission

| claim | after state at `583eea87` | verdict |
|---|---|---|
| C1 depth (lowest tied, 8) | note present, six UL rows grounded in three pinned v262 snapshots, `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `met=1`, rc 0; registry 303 → 308, notes 90 → 91, census rc 0 | **verified** (author-side) |
| C2 freshness (9) | `ROUTED_STALE=3` rc 1 at the base → `ROUTED_STALE=0 ROUTED_OK=3/3` rc 0 at the measured revision, each item inside a line-anchored appended block with whole tokens, a digest direction and a receipt that reports ten cases | **verified** (author-side) |

The C1 predicate is form-level by construction: the counter checks id, statement length, grounding,
source kind and binding, digests, quote location and length, and snapshot reuse; it does **not** check
entailment (UL6's first draft failed a reviewer's reading). The semantic layer is R1Reviewer's per-row
verdicts — `ROWS_HOLD` rose from **2/6** on the drafted rows to **6/6 after the corrections below**, which
the L1 applied and re-scored with the frozen counter (`met=1`).

## Mistakes

- **R73-ROW-OVERCLAIM** — class `quote-attributed mechanism stated past its source` · evidence: UL6 said
  enable-time aliases to a missing unit are "ignored rather than created", while at v262 `install_info_symlink_alias`
  marks the target `broken` and creates the symlink anyway (`install.c:2013-2021`), and
  `INSTALL_CHANGE_IS_DANGLING` fires on disable/preset removal paths (`:2308-2313`, `:350-351`); UL1 omitted
  the trailing-empty-component append case (`systemd.unit.xml:376-378`); UL2 dropped the "under those
  directories" scope (`:237-238`); UL4 said "fragment path is null or empty" where the predicate tests the
  **file at** that path and fires on a stat change, not a path change (`unit.c:3866-3893`) · captured-by:
  R1Reviewer (`w1/R1Reviewer/report.md`, `ROWS_HOLD=2/6`) · fix: four statements rewritten to the reviewer's
  corrected sentences and re-scored `met=1`; the corrected text is what landed.
- **R73-INSTRUMENT-MIDWAVE** — class `instrument edited mid-wave before its record existed` · evidence:
  `tools/check-r72-routed-r73.py` moved through `93f034e3…` → `316dd51a…` → `f1c4b4d3…` → `328a6bf6…` →
  `71931c1c…` while seats were scoring, and the SCORECARD erratum that should have named the change did not
  exist yet at 23:11:43 (S1Scout §8) · captured-by: S1Scout · fix: SCORECARD "Round 73 — C2 instrument
  repair" and "final instrument digests" now name every intermediate, and the rule restated in this lesson:
  the erratum is written **before** the first repair commit, not after the edit.
- **R73-SAMPLE-ANSWER-KEY** — class `the instrument carries an admissible answer key` · evidence: K1Critic
  D2: a do-nothing writer that copies `SAMPLE_ROWS` out of `tools/count-ul-rows-r73.py` reaches `met=1`
  without opening a source; the sample rows were authored from the same L1 draft as the first note · fix:
  the note's final rows were rewritten by the reviewer's corrections and the measured overlap is
  `NOTE_ROWS=6 SAMPLE_ROWS=6 IDENTICAL=0` (`.ufo/waves/round-73/after/final-checks.txt`), with the per-row
  quotes re-opened; next round: synthetic self-test snapshots so the answer key cannot be the note.
- **R73-EMPTY-QUOTE** — class `a clause satisfied by an empty cell` · evidence: `quote=""` passed every
  frozen clause (`words("") == 0 <= MAX_QUOTE_WORDS`; `norm("") in norm(snap)` is true), `met=1` rc 0
  (`w1/E1Counter/report.md` §D1) · captured-by: E1Counter · fix: `MIN_QUOTE_WORDS=4` and a twelfth selftest
  case `EMPTYQUOTE`; the six landed quotes are 5-25 words, so the tightening removes nothing.
- **R73-CHECKER-LEXICAL** — class `required token satisfied as a substring, direction and existence unchecked`
  · evidence: `often` satisfied "ten"; `…selftest-selftest-after.txt.bak` satisfied the receipt path; the two
  digests passed in either order; a keyword list with no sentence passed (`w1/R2Reviewer/report.md`
  F1/F2/F4/F6/F7; `w1/E2Routed/receipts/`) · captured-by: R2Reviewer, E2Routed · fix: whole-token and
  path-token matching, digest direction, receipt existence with a ≥10-case line, supersession verb;
  selftest 5 → 11 cases. The denial leg (a block that keeps every token while contradicting it) **stays a
  named limit**: lexical checks cannot prove entailment.
- **R73-EXITMAP-UNREACHABLE** — class `a documented exit code the code cannot return` · evidence: the
  checker's docstring promised exit 2 for an absent input, while an absent file was a stale finding (rc 1);
  the counter's header omitted its own 128 · captured-by: SC3Index (F2, F4) · fix: both docstrings now state
  the reachable map (2 is `--selftest`-only; 128 is the counter's absent-input code) and the SKILL registry
  rows carry it.
- **R73-LISTUNITFILES-PRESET** — class `a two-column listing read as one fact` · evidence: the host line
  `systemd-networkd-wait-online.service masked enabled` was nearly read as "enablement survived a mask"; the
  header is `UNIT FILE STATE PRESET`, and `systemctl is-enabled` prints `masked` with exit 1 while
  `UnitFileState=masked` (`w1/SC3Index/deltas.md` F3; re-measured by the L1) · captured-by: SC3Index · fix:
  the SKILL table row T5 carries the corrected reading; the L1's earlier draft that read the column as
  enablement never landed.
- **R73-REGISTRY-ROWS-OUTSIDE-TABLE** — class `appended rows placed after the last section` · evidence: the
  five new rows were appended at EOF (after `## Leads (unopened)`) and the canonical census read
  `E12 ... row outside Registry section`, rc 1 · captured-by: the round's own measure (`after/measure-09dac09f.txt`)
  · fix: the rows moved into the Registry table directly after S303 (append-only landing, no filed row
  altered), census rc 0 at `583eea87`.
- **R73-MEASURE-PIPE-EXIT** — class `a receipt records a pipeline's exit code, not the tool's` · evidence: the
  first `c2-before-final-instrument.txt` printed `rc=0` beside a `tail -2` pipeline whose checker had exited 1
  · captured-by: the L1's own read-back · fix: the receipt regenerated without a pipeline; every command in
  it now prints its own `rc=`.

## considerthese

No proposal is mined this round. The latest file (`considerthese/2026-10-26.md`) has five proposals and all
are already accounted for, each verified by grep rather than restated: "Counter-attack scoreboard" is the
standing SKILL ledger continued below; "Seat-harm incident log" is the per-round tally below; "Burst-aware
reading" is a one-round mining record (r46), not a gate; "Cross-note correction propagation map" is recorded
partial (r43/r54) and does not clear this round's bar; "Downstream patch-offset check" was adopted at round 69
as QUALITY 103 and is exercised here by the note's v262-vs-262.1-1-arch anchor sentence.

## Counter-attack scoreboard — round 73 (continuation of the r64 ledger)

| Counter | Round / arm source | Arms fielded (receipts) | Survivors | Class that beat it |
|---|---|---|---|---|
| `count-ul-rows-r73.py` (C1) | declaration battery (`--selftest`, 11 then 12 cases) | 1 control + 10 mutants, then EMPTYQUOTE | 0 after repair; 1 before (`quote=""`) | empty-cell clause (E1Counter D1) |
| `count-ul-rows-r73.py` (C1) | E1Counter clause-isolation matrix | 10 clause-isolated fixtures | 0 (each printed its own finding) | — |
| `count-ul-rows-r73.py` (C1) | R1Reviewer attacks A/B/C/E | word-salad, unrelated-region quote, copied-quote writer, anchor without a line range | 4 | form instrument; semantic layer is the reviewer |
| `check-r72-routed-r73.py` (C2) | R2Reviewer F1-F7 | 7 fixtures | 5 before repair (F1, F2, F4, F6, F7) | substring tokens, missing receipt read, no digest direction, vacuity, denial |
| `check-r72-routed-r73.py` (C2) | E2Routed A2/A3/B1-B4 | 6 tamper receipts | 0 after repair | the repairs above |
| `check-r72-routed-r73.py` (C2) | its own `--selftest` | 11 cases | 0 | — |

## Trend verdicts

- **expansion: improved.** Three admitted tier-A registry rows (S304-S306) on ground the held-ground sweep
  reads as unheld, one admitted entry (UL1-UL6) citing them, registry 303 → 308 and notes 90 → 91, and two
  refusals kept as taste evidence.
- **quality: improved.** The three round-72 routed defects close in committed bytes (`ROUTED_STALE=3` → 0)
  with a same-instrument before/after pair; both round-73 instruments were hardened by the wave's own attacks
  (empty quote, substring tokens, receipt existence, digest direction, exit maps) and their new selftests
  carry twelve and eleven named cases; the note's four overreaching statements were corrected before landing.
- **discernment: unchanged (author-side).** The wave found defects in every claim (R1Reviewer 2/6 rows on
  the first draft, E1Counter's empty quote, R2Reviewer/E2Routed's five checker survivors, K1Critic's D2/D6,
  SC3Index's F2/F3/F4) and all are repaired or recorded; the outside admit/reject spot-check is owed by the
  closure judge, so no author-side uplift is claimed.

## Seat-harm tally (standing per-round tally, r66 adoption continued)

Round 73: 0. One seat (`S1Scout`) reported the L1's mid-wave instrument drift as an observation with no
blame and no seat damage; no seat wrote outside its wave dir, none mutated git/jj, and the L1's misroot sweep
at report time is clean. Running tally since r66: 0, 0, 0, 0, 1, 0, 0, 0.

## Correction (round 73, late wave; append-only)

The `R73-CHECKER-LEXICAL` row above says the checker's selftest grew "5 → 11 cases" and the measured
outcome block says "eleven". The last repair (E2Routed's absolute-path/FAIL-receipt/placeholder traps)
lands **thirteen** cases (`SELFTEST: PASS (13 cases, 13 passed, 0 failed)`, final checker sha256
`73184198…`, receipt `.ufo/waves/round-73/after/c2-final-instrument.txt`); the earlier figures stand as
filed and this line is the correction of record.

## Correction 2 (round 73, wave close; append-only)

The wave's last attack seat (M1Mutation) mutated both instruments after the correction above: the counter
crashed on a non-map `snapshots` value and now prints `UL_MAP malformed` (rc 1) instead, with a thirteenth
case `MAPLIST`; the checker accepted a finding id placed only in a block heading and now requires the block's
body (the id itself may label the heading), with a fourteenth case `TITLE-TOKEN`. Final bytes: counter
`1f22c26b…` (13 cases), checker `ad853877…` (14 cases). Both still read `met=1` and `ROUTED_STALE=0` at the
measured tip. M1Mutation's matrices (`w1/M1Mutation/{counter_matrix.json,c2_matrix.json,battery.py}`) record
38 mutants, 6 survivors, all dead/entailed clauses.

## Correction 3 (round 74, C2 routed repair; append-only)

R73-GATE-QUOTE-LINE-DRIFT: S306's quote `path = path_make_absolute(*name, config_path);`
is at install.c:2383 in the pinned v262 snapshot, superseding the cited 2387.
S304's corrected quote anchors are :368-370 (superseding :367-370), :237-238 (superseding
:236-238), and :238-239 (superseding :238-240). The earlier Gate table remains visible;
these exact locations replace its over-wide or incorrect anchors.
