# Round 52 — lesson

L1: `TsukuroiR52` (hyaku run 11 continuation). Base `cc88b81d` → freeze `ff9470ea` → wave `w1`
(64 seats, policy v2, ONE wave) → WAVE-DONE received before this file was written. Claims C1/C2/C3
declared at the freeze (SCORECARD "Round 52 — declaration"; `.ufo/waves/round-52/frozen/FROZEN.md`);
the counted row bytes were the round-51 AMENDMENT-1 bytes, unchanged since `6abef5d0`.

## Gate

- Candidates: rows GR1, GR2, GR3 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` (the round-51
  amendment bytes), each to be admitted only by a clean counted cohort; plus the two
  instrument-measurement claims C2 (valid 5-cheat scorer receipt) and C3 (named-revision C3 counter
  receipt) — instruments, not corpus admissions.
- Admitted: **none**. The frozen C1 predicate fails on `seats_ok 16 ≠ 18` (two counted seats —
  `R52CritGR1b`, `R52CritGR3b` — produced full transcripts but never wrote their report files; no
  replacement seats under the orchestrator recovery boundary) and on bound negatives: GR2 blocked by
  all six bound seats (reviewers `fails`, critics `partly`), GR3 blocked `partly` by three of five
  bound seats. No admission mark was written. Receipt `.ufo/waves/round-52/after/c1-at-freeze.json`
  (`structural_ok 1, lint_ok 3, quotes_ok 3, verdicts_ok 1, seats_ok 16, marks_ok 0`).
- Rejected, with reasons:
  - **GR2** — the observability clause at entry lines 233-235 ("a replace that the resume path set
    to suspended without taking the exclusive operation … shows in neither") is contradicted for
    `replace_target`: the resume-failure branch sets SUSPENDED and returns without clearing
    REPLACE_TGT (dev-replace.c 1235-1242), which the mount-time restore re-sets whenever a target is
    present (dev-replace.c 170-174, 196-210) after the target/bdev check the resume path passes
    (dev-replace.c 1218-1235). Six independent seats converged on this clause
    (`.ufo/waves/round-52/w1/R52RevGR2{a,b,c}.md`, `R52CritGR2{a,b,c}.md`); replacement text is in
    the reports and the entry's round-52 Gate-status section. **flip:** adopt the qualified sentence
    (one clause), re-hash, and a fresh counted cohort reading `holds` admits the row.
  - **GR3** — the SIGINT handler-window sentence overstates the pinned caller: the installation
    helper returns sigaction's result (scrub.c 436-443) which the start path discards at scrub.c 1546
    (attempted, unchecked), and thread-creation failures jump to `out` (scrub.c 1575, 1592, out at
    1712) bypassing the reset at scrub.c 1710. Three seats bound `partly`
    (`R52RevGR3{a,c}.md`, `R52CritGR3c.md`); two bound `holds`. **flip:** same — qualify the two
    sentences, re-hash, fresh counted cohort.
  - **GR1** — read `holds` by all five bound seats, but the claim binds all three rows together, so
    GR1 is not admitted this round; its bytes need no change.
- Source rows touched this round, with the logged changes:
  - **S257 added** (GNU Bash Reference Manual, Pipelines — https://www.gnu.org/software/bash/manual/html_node/Pipelines.html),
    opened 2026-10-30 by the L1 (HTTP 200, 7513 bytes, sha256 `b5629f04ccf5fe711d1b30f5dd4d8cf67dc6ab836d413292cd15c870a662059a`);
    located quote (Pipelines section body, ≤25 words): "If pipefail is enabled, the pipeline's return
    status is the value of the last (rightmost) command to exit with a non-zero status". Registered
    `queued` at the freeze; **flipped `queued` → `mined`** after this lesson landed (cited by
    `used-by: corpus/lessons/round-52.md`); old→new: status `queued`→`mined`, used-by `—`→
    `corpus/lessons/round-52.md`. Independent open: `R52ScoutS257` (per-cell check).
  - No other row changed (no status/recheck/used-by edits; census exit 0 at start, freeze, end).
- Sourced claim: **C2** rests on S257 (this round) + S256; its receipt cites the pipefail semantics
  the matcher counter and the cheat classes are grounded in.
- Spot-check result: the lane's own seats re-opened and cross-checked (R52ScoutS257 per-cell on
  S257; R52ScoutReopenS242/S246 on the pinned snapshots; R52RevHashBind re-derived the section
  hashes) — all agreeing per their reports; the REQUIRED independent non-author admit/reject sample
  is the closure's to run and was **not available in-round** (lane-dispatched seats are still the
  lane, `LEARNING.md`); this Gate therefore records the sample as pending external closure, and the
  round reports discernment accordingly.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| counted seat lost its report file — a cohort seat that runs out of turn budget after deep verification never writes the binding file, so its work binds nothing and the round's seats_ok leg fails | `R52CritGR1b`, `R52CritGR3b`: rich final outputs in `w1-results.json`, no `<seat>.md` file; counter `seats_ok 16` | none — QUALITY 93 binds the channel but no rule orders a counted seat to write the file BEFORE deep verification | QUALITY 96 (this round, cites this lesson): a counted seat writes its two binding lines and a minimal body to the report path FIRST, then deepens; red state is this round's two lost seats, green state is a cohort with 18/18 files |
| two seats died with empty output (provider loss under fleet load) | `R52CritLimits`, `R52ScoutArch`: empty `output` in `w1-results.json` | run-11 routing-recovery notes (provider failures reported, never replaced) | reported as dead seats in the round report with their last error text (empty output); their items (`Limits` staleness, Arch News sweep) are named unverified in the report |
| fourth consecutive honest stop on the same claim family (49-52) | SCORECARD rounds 49-52 outcomes: C1 failed each time on a newly-counted defect class | the claim-sizing rule (§9) kept each round's target honest, but the lane never reserved cohort budget for report-writing overhead | next round sizes the cohort with the QUALITY 96 write-first rule and amends exactly the two named clauses; no target narrowing |

## considerthese — counter-attack scoreboard, rounds 38-50 (proposal landed)

Mined from `considerthese/2026-10-26.md` ("Counter-attack scoreboard" bullet; date 2026-10-30), the
last still-open proposal in that file. The table below is the seat-drafted scoreboard
(`.ufo/waves/round-51/w1/R51ScoutConsider.md`, rounds 38-50), verified by `R52RevScoreboard` (8 cells
re-opened against the cited seat reports; per-cell verdicts in `.ufo/waves/round-52/w1/R52RevScoreboard.md`).
One arm = one scored variant a wave seat built to pass a counter without the claimed work; "beat" =
that frozen counter printed PASS.

| Counter | Round | Arms fielded | Reached frozen PASS | Class that beat it |
|---|---|---|---|---|
| `score-storage-arm-r38.py` | 38 | 6 + 5 | 8 | override; answer-key; leak read; liar |
| `score-storage-arm-r38-q82.py` | 38 | 8 | 4 | leak read |
| `check-hook-order-r38.py` | 38 | unsourced | unsourced | unsourced |
| `score-storage-hidden-r39.py` | 39 | 18 | 10 | fixture literal; answer-key; spelling; liar |
| `check-transaction-order-r39.py` | 39 | 11 | 8 | liar (false/empty rule cells) |
| `score-selftest-literals-r40.py` | 40 | 4 | 3 | answer-key; spelling |
| `check-exec-environment-r40.py` | 40 | 14 | 13 | liar (pasted frozen tokens) |
| `score-selftest-mounts-r41.py` | 41 | 4 | 1 | answer-key (stripped here-document) |
| `check-package-anatomy-r41.py` | 41 | writer + 6 + 6 mutants | writer + rows 01-06 + M5 | liar; spelling |
| `score-size-invariance-r42.py` | 42 | 9 | 6 | override; answer-key |
| `check-scrub-record-r42.py` | 42 | ≥10 PASS rows tallied | ≥10 | liar (holds-line quoting); forged dispatch+results |
| `score-bootinputs-r43.py` | 43 | 2 evasion + declared K7 | 0 unexpected | K7 leak read is declared, not a beat |
| `check-scrub-record-r43.py` | 43 | 7 fixtures scored, of which 6 are further mutations (Z-k3 is the declared-limit reproduction) | 5 further-mutation PASS (Z-k3 PASS is the declared-limit reproduction) | liar (negated statements that keep the frozen tokens) |
| `score-scrub-arm-r44.py` | 44 | 10 raw variants, 9 cheating candidates (V7 is a faithful rewrite, not an arm) | 5 (V1-V5) | leak read (script path, statfs tmpfs, `BASH_SOURCE`, cwd, uid_map) |
| `check-scrub-record-r44.py` | 44 | 2 writers | 2 | liar |
| `score-census-readers-r45.py` | 45 | 30 equivalence variants + 2 full-counter runs (no full-counter run for the other mutants) | 0 observed of the 2 full-counter runs | none observed |
| `check-scrub-grounding-r45.py` | 45 | none scored | 0 unexpected | none in the scored battery |
| `score-census-identity-r46.py` | 46 | 2 | 2 | liar (unasserted labels) |
| `check-scrub-admission-r46.py` | 46 | 2 | 2 | unresolved-citation + duplicate-body (not of the six) |
| `check-scrub-admission-r47.py` | 47 | 6 | 4 | spelling; answer-key; quorum |
| `score-selftest-tmpdir-r48.py` | 48 | unsourced (w1 void) | unsourced | unsourced |
| `check-scrub-admission-r48.py` | 48 | 7 | 6 | liar (content-free bodies); forged bundles |
| `check-scrub-admission-r49.py` | 49 | 22 scenarios | 9 | liar; spelling; answer-key |
| `check-adjacency-table-r49.py` | 49 | 23 | 15 | shape credit (uncompared pins) |
| `check-fd-band-r49.py` | 49 | 3 | 2 | liar |
| `check-scrub-admission-r50.py` | 50 | 14 | 9 | liar (body contradicts first line); stub cohorts |
| `check-selftest-matcher-r50.py` | 50 | 6 | 2 distinct variants (c, e; e observed at runs 1 only) | liar; spelling (braced pipes) |
| `check-adjacency-table-r50.py` | 50 | 4 | 3 | shape credit; override |

Pattern (the proposal's question — converging or moving the hole?): the classes move, they do not
disappear. r38-r39 holes (leak read, fixture literal) were closed by r39-r40; r40-r41 lost to
answer-key reads; r42-r44 to watched-channel leaks and token-keeping liars; r45 was the quiet row
(30 equivalence variants, 0 full-counter PASS observed); r46-r50 every new admission/matcher counter
was beaten by a liar or a forged bundle — the falsifier's job is now primarily liar-and-bundle
shaped. Round 52 adds its own datapoint: `R52CritForgeC1a` printed a full-predicate PASS on the real
entry bytes using the counter's declared fixture overrides (18 forged reports + results + dispatch +
marks) — the override-injection limit the instrument family has disclosed since round 51 — while the
production path (committed revision bytes, no overrides) fails without real counted files
(`R52CritForgeC1b` P4: `verdicts_ok 3, seats_ok 18, marks_ok 0` → FAIL without the marks). The
verification seat `R52RevScoreboard` corrected four convention miscounts in the scout's table
(r43, r44, r45, r50 rows above carry its replacement cells; full corrections in
`.ufo/waves/round-52/w1/R52RevScoreboard.md`).

This table answers the proposal's question with lane data and is the delivered artifact for the
mined proposal; no SOURCES row is appended for it (own-work rows only; `considerthese/<file>` is the
pointer, not a source).
