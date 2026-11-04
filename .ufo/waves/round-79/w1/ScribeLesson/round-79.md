# Round 79 — dependency propagation and gate-standard registry

Base `9086589a82f221d130ed6711fbe70b85f0d07aea`; frozen claim commit
`afe1f26128bde87484001cd02ebf11fa524c4059`. LOG.md Round 79 motivates C1 depth
(8, lowest non-retired, tied with adjacency) and C2 operability (9). Neither
claim pre-claims an ordinal uplift, a coverage promotion or a capability. L1
holds the planner seat; one v1 wave of 12 seats was dispatched.

C1 opened systemd v262 `man/systemd.unit.xml` (upstream tag, not the installed
Arch build) and froze eight dependency-propagation rows against the pinned
snapshot `.ufo/waves/round-79/before/src/systemd.unit.xml`, SHA-256
`eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c8`; the frozen
expected set `before/expected.json` is SHA-256
`0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21`. The
reviewer's first pass found that the frozen DP6 statement dropped the source's
precondition "and no job is queued for them" (`:785`); the landed entry carries
the corrected statement, so the **frozen C1 predicate is a declared miss** — its
expected tuple cannot be altered after data without becoming a different
instrument. C2 marks the four current continuation registry tables non-operative
and gives the two routed round-72 gates real hermetic selftests; it verifies.

## Gate

Source opened before the freeze, on 2026-11-04, and pinned byte-exact:
`https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml` →
`.ufo/waves/round-79/before/src/systemd.unit.xml`, SHA-256 `eb9479be…14c8`.
The four rows below are taken **verbatim from ScribeSources' draft**
`.ufo/waves/round-79/w1/ScribeSources/sources-gate.md` (written 16:12 local),
which is the seat that owns the `## Gate` block. Every quote was independently
re-located by this seat with the frozen instrument's own rule (tag-stripped,
whitespace-normalised, space-padded token match): the admit quote resolves at
`:659`, the three rejection quotes at `:855-857`, `:698-699` and `:785-787` —
all four as recorded, all at most 25 words (7 / 21 / 24 / 24).

| Row / candidate | URL, access date, located quote (at most 25 words) | Decision / reason / flip |
|---|---|---|
| S329 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml ; 2026-11-04, :659: `Configures (weak) requirement dependencies on other units.` | admit, tier A/docs/mined for the dependency-propagation and ordering keyword scope only: Wants= :657-679, Requires= :682-708, Requisite= :711-728, BindsTo= :731-758, PartOf= :761-778, Upholds= :781-797, Before=/After= :826-866, RequiresMountsFor= :934-947; eight finite DP rows over documented semantics, not a live-host reading and not an installed-build equivalence claim |
| `After=` pulls the unit in | same page, :855-857: `Note that those settings are independent of and orthogonal to the requirement dependencies as configured by Requires=, Wants=, Requisite=, or BindsTo=.` | reject: ordering and requirement dependencies are orthogonal — an `After=` line alone never creates a requirement dependency and never pulls a unit into the transaction. Flip: a located upstream passage stating that `After=` itself creates or implies a requirement/pull-in dependency |
| `Requires=` guarantees the listed unit stays active | same page, :698-699: `Note that this dependency type does not imply that the other unit always has to be in active state when this unit is running.` | reject: `Requires=` explicitly does not imply the other unit must remain active; the page directs `BindsTo=` with `After=` for that guarantee. Flip: a located upstream passage stating that `Requires=` guarantees continued active state of the listed unit |
| `Upholds=` is a one-time pull-in | same page, :785-787: `While a Wants= dependency on another unit has a one-time effect when this units started, a Upholds= dependency on it has a continuous effect,` | reject: the page contrasts `Wants=` (one-time effect) with `Upholds=` (continuous effect, constantly restarting the unit). Flip: a located upstream passage stating that `Upholds=` has only a one-time pull-in effect |

S329 is a new row; no existing row's status, recheck or used-by changed. The
census at round start and round end exits 0 with W04 duplicate-URL warnings
only: the same URL is already S304's for the unit-load merge plane, a different
scope, so W04 and not E04. Id-collision caveat, recorded and not smoothed: the
read-only staged package `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`
already uses the bare id `S329` for a different document (an own-work
mirror/locale capture; package ids run S200–S346, intersection with this
registry S200–S328). The package is not adopted and the frozen claim required
`S329` here; the resolution is namespace/document context, never arithmetic
renumbering. The package stays unadopted.

**Gate provenance note.** ScoutSources drafted an independent Gate block
(`w1/ScoutSources.md`) with a different admit anchor (`:666-667`, the DP1 quote)
and richer flip conditions. Its three rejections agree with ScribeSources' on
substance. The admit quote differs only in which located sentence is offered as
the scope witness; both are ≤25 words and both locate exactly. The L1's landed
lesson and the landed `corpus/SOURCES.md` S329 row use ScribeSources' `:659`
witness, and this draft follows the same choice, so the two Gate blocks differ
only in the optional corroborating locations ScoutSources added.

## Mistakes

| Class / id | Evidence | Captured-by | Fix shown able to fail |
|---|---|---|---|
| reference-drift — R79-DUPLICATE-SEVEN-VS-SIX | `corpus/lessons/round-78-verifier-spotcheck.md:170-173` (r78 closure routed item 4: "Seven re-registered tools now appear both in the operative round-71 table and in the round-76/77 continuation tables"); `SCORECARD.md:6625-6632` (r79 measured before-value `duplicates=6 shape_ok=0/2 met=0` rc 1); `tools/check-gate-standard-r79.py:145-158` (the duplicate leg) | QUALITY 104 (counts bind to receipts) | A line-keyed sweep of `SKILL.md` at the base counts a prose mention as a duplicate: the r78 eight carry a second *line* mention for six of them (`:5897/6023`, `:5898/6039`, `:5899/6092`, `:5900/6091`, `:5902/6038`, `:5903/6019`), and two of those six second mentions (`:6038` `count-uf-rows-r74`, `:6039` `check-r73-routed-r74`) are prose inside the "Round-74 counters:" paragraph, not table rows. The counter counts 8-column rows in the *current* operative set only, so prose never enters. Base receipt: `duplicates=6`. |
| correction-not-reproducible — R79-SEVEN-NOT-RECONSTRUCTIBLE | This seat's independent re-derivation at the r78 closure's own revision `a15aff6ea38961cae5e6748b1e8f924a1b454c34` and at the base `9086589a…` (read-only `git show` + the frozen checker's own `current_rows`, which the closure did not have): of the eight paths r78 re-registered (`corpus/lessons/round-78.md:78-80`), **four** also appear as a row of a later registry table (`check-r72-routed-r73` `:5897`/`:6023`, `check-r75-routed-r76` `:5899`/`:6092`, `count-jd-rows-r76` `:5900`/`:6091`, `count-ul-rows-r73` `:5903`/`:6019`), two are single-row (`check-r71-routed-r72` `:5896`, `count-md-rows-r72` `:5901`), and two are row-plus-prose (`check-r73-routed-r74` `:5898`/`:6039`, `count-uf-rows-r74` `:5902`/`:6038`). The checker's measured six is a *different* set — it adds two tools r78 never re-registered (`check-selftest-tally`, `measure-journal-arithmetic-r77`) and excludes both prose-only cases. | QUALITY 104; QUALITY 105 (`git diff -U0 <base> <REV> -- <files>` sweep whose output must equal the disclosed list) | The r78 closure names no seven — it asserts a count, so the r79 correction cannot be checked against it. The correction as written in `SCORECARD.md:6629-6632` ("the seventh candidate it names, `count-uf-rows-r74`") names a candidate the closure text does not name, and places its prose second mention in "the round-73 continuation block" when it is in the **Round-74** counters paragraph at `:6038` (and `:6039` is a second prose case of the same shape the correction does not mention). Fix: restate the correction as "no set of seven is reproducible from the committed bytes under either line- or row-keyed counting; the row-keyed current-set count is six" and name the two prose cases by line. |
| vacuous — R79-QUOTE-TOKEN-BOUNDARY | L1 session transcript `.omp/agent/sessions/-Projects-shokunin/2026-11-03T17-37-19-922Z_01a1a27c-a432-71e1-944b-0900e4e7a66b/TsukuroiR79.jsonl` line 142 (first `before/expected.json`, SHA-256 `17851611e46e9430969603536ad171c0be852672c85ce29ee08042d0a968c9c8`), line 185 (the C1 selftest control arm reads `expected=1 observed=0 count=0 reason=quote-location … FAIL`), line 188 (`DP1 want 666-667 got None` … `DP8 want 857-858 got None`), line 195 (the diagnosis: the generator's bare substring find matched "started" *inside* the token "started.", so the quote was a substring fragment ending inside a token) | QUALITY 80 (do-nothing controls score under the frozen predicate before any seat); QUALITY 81 | The instrument's own control arm refused every row before a seat existed. The fix was two-part and both parts are visible in the frozen bytes: the quotes were re-authored as whole-token spans (`expected.json` digest `0c09c7a4…`, frozen at `afe1f261`) and the locator's off-by-one index was corrected (`tools/measure-unit-deps-r79.py:79-80`, `first = linenos[start]`). This seat re-derived the failure mode against the frozen snapshot: dropping the trailing punctuation from **any** of the eight frozen quotes makes `locate()` return `None` for that row, and with the pre-fix `linenos[start-1]` index DP3, DP4 and DP6 would compute wrong ranges. The frozen `selftest-depth` arm (`before/controls.json`, 32/32 rc 0) is the receipt that the corrected pair now holds. |
| scope — R79-C2-SHAPE-SCOPE | `tools/check-gate-standard-r79.py:41` (`FROZEN_ROWS = ('check-r71-routed-r72', 'count-md-rows-r72')`), `:159-171` (the shape leg applies to those two rows only); `w1/CriticFreeze/attacks.json` A13/A14; `w1/ReviewRegistry/findings.md` F1/F1b | QUALITY 87 (a counter reads the content it credits) | The shape leg names two rows. Re-derived by this seat with the frozen checker's own `current_rows` semantics: at the base, **48 of 97** current `gate` rows fail the leg's self-test-cell clause (43 carry no `--selftest` token at all, 45 name no tool of their own in that cell; 38 of the 48 read `none: …`), and at the integrated head `c7dcd241…` **46 of 93** still fail (36 read `none:`). Two of 48 are repaired by this round; the other 46 are inherited debt, disclosed here as a limit and not claimed closed. |
| counter-defect — R79-C2-DUPLICATE-LEG-EVASIONS | `w1/CriticFreeze/report.md` A12/A17/A17b/A18; `w1/ReviewRegistry/findings.md` F1c; `tools/check-gate-standard-r79.py:127` (`heading_line = lines.index(heading)`) | QUALITY 100 (a gate's PASS counts each record it claims to check) | `duplicates=0` is weaker than it reads. The leg counts the *current* operative set, so a self-declared `NON-OPERATIVE` marker removes a table from the count (A12), a new highest-numbered `## Gate and probe registry — roundN …` heading drops every earlier table from the count (A18), and `lines.index(heading)` resolves a table's heading to the **first** occurrence of that heading string, so a duplicated heading text silently removes a later current table (A17; A17b isolates the cause by renaming the later heading and the duplicate reappears). A17b shows the counter reading `duplicates=1` rc 1 with byte-identical rows. Fix (two lines, not applied — the checker is frozen): have `tables()` yield the heading's own line index instead of `lines.index(heading)`. |
| vacuous — R79-C1-EQUALITY-SHADOWS-DEEP-LEGS | `w1/MutationCounter/matrix.json` (survivors `c1-seven-rows-rowcount`, `c1-no-line-check`); `tools/measure-unit-deps-r79.py:97-98` (`data != expected` → `finite-content-mismatch`) and `:110-113` (`quote-location`, `row-shape`); `w1/CriticFreeze/report.md` residual note | QUALITY 81 (a scripted non-reader must read below the target) | With `expected.json` digest-frozen and compared by strict equality at `:97`, every DATA-side perturbation dies at `finite-content-mismatch` before `quote-location` (`:110`) or `row-shape` (`:112`) can fire, and the per-row `quote-DP*` / `line-DP*` selftest cases are answered by the equality leg, not by the clause they name. Mutants that delete `row-set` or `line`-checking survive. The declaration's "eight pinned dependency-propagation rows match with review binding" is therefore a statement about equality with a frozen tuple plus digest arithmetic over a review bundle, not a semantic oracle — a limit the declaration states, and one the attack seats quantified. |
| process — R79-SCRIBE-LESSON-LATE-BINDING | This seat's own binding file `.ufo/waves/round-79/w1/ScribeLesson.md` (mtime 16:36:27) against the L1's `corpus/lessons/round-79.md` (mtime 16:30:24, written by the L1 at transcript 19:30:12Z) and its row `R79-SCRIBELESSON-UNSETTLED`; the L1's transcript reads of `agent://ScribeLesson-33` at 19:25:01Z and 19:34:44Z both returned nothing | QUALITY 96 (a counted seat's FIRST write is its two binding lines plus a minimal honest body) | This seat wrote its binding file ~6 minutes *after* the L1 had already landed the lesson asserting that "The ScribeLesson seat produced no binding file and no report; the L1 wrote this lesson instead." That statement was true when written and is now false — the seat produced both artifacts — so the landed lesson carries a row that mis-describes the wave and needs an append-only correction (QUALITY 4, 99) pointing at `w1/ScribeLesson.md` and `w1/ScribeLesson/round-79.md`. The cause was this seat's own ordering violation: deep verification ran for ~28 minutes before the first write. The fix is the rule, not the wording — the first write to the wave directory is `claim=` / `verdict=` plus a minimal body, deepened afterwards. |
| stale-premise — R79-FROZEN-ROW-DP6 | `w1/ReviewDeps/review-first.md` (first review, DP6 `partly-holds`) and `w1/ReviewDeps.md` (second review, all eight `holds`, `review_sha256=0c2dd4ad601e179110df546ec4933f2b3e8249e462a548db8263cbf5da1c8168`); snapshot `:783-785`; the frozen statement in `before/expected.json` vs the landed `corpus/knowledge/systemd-dependency-propagation-r79.json` (this seat's comparison: the two objects differ in exactly one field, DP6's `statement`) | QUALITY 66 (keep every branch the quoted source states); QUALITY 94 (every cited line accounted for) | The frozen DP6 statement stopped at "failed," and dropped the sentence's continuation "and no job is queued for them" (`:785`), asserting a broader trigger than the source states. The landed entry carries the precondition; the frozen tuple is **not** edited, so the frozen instrument reads `count=0 … reason=finite-content-mismatch` for the corrected data at any revision. That is the recorded miss, not a repair. |

## Seat harm

| Round | Harmed seat | Causing seat | Evidence class | Observed effect | Isolation fix |
|---|---|---|---|---|---|
| 79 | ReviewRegistry | ExecInstrument | seat disclosure — `w1/ReviewRegistry/findings.md` F4 (its own run, 16:13:5x–16:14:00 local) plus the mtime of `tools/count-md-rows-r72.py` (16:14:00), the file ExecInstrument owns and rewrote | One run of `count-md-rows-r72.py --selftest` returned rc 3 with `SELFTEST map-digest rc=1 FAIL / expected-but-absent: ['map-digest']` while that file was being rewritten underneath it. ReviewRegistry states the digest of the bytes it executed was not captured, so the run cannot be attributed to the final artifact; it re-ran at the final digest (5 consecutive runs pass 23/23 rc 0). A shared-file collision, not a defect in the delivered tool. | The writer owns the file; the reader measured a file that was mid-write. Fix: readers bind to a committed digest (or copy the file into their own scratch) rather than executing the live tree while a writer may be rewriting it. ReviewRegistry already does the re-run-at-final-digest repair; the durable fix is a review-time snapshot. |
| 79 | ReviewDeps | ScribeNote | seat disclosure — the L1's re-dispatch message to ReviewDeps (transcript line 465, 19:21:46Z) and `w1/ReviewDeps/review-first.md`, which preserves the first binding (`artifact_sha256=85ac6da9…`, `companion_sha256=c1149b5f…`) beside the second (`w1/ReviewDeps/verdict.json`, `artifact_sha256=1b8f833d…`, `companion_sha256=8c6b3809…`) | The reviewer bound its digests to the note bytes as they stood at 16:16–16:19; ScribeNote then re-edited `w1/ScribeNote/data.json` (16:21:23) and `note.md` (16:21:37) to carry the corrected DP6 statement, voiding the first binding. The reviewer had to re-read both files and re-issue the verdict, and the first pass was preserved separately so the DP6 finding is not lost. | The second edit was L1-requested and correct; the cost was a re-review cycle. Fix (adopted here): the reviewer copies the bytes it binds next to its verdict (done — `review-first.md`), so a later edit is a re-bind rather than a lost finding. |
| 79 | — | — | — | entries: none observed in w1 settlement for kill signals, `pkill`/`killall`, lane writes outside a seat's tree, or scratch under `/tmp`. No round-79 seat reports a `/tmp` write, and every seat that created a scratch tree used `/fast/scratch/hyaku/tsukuroi-r79/<seat>` (ExecRegistry, ExecInstrument, MutationCounter, ReviewRegistry, ScoutSources each record this in their own report). The fleet root `git status --porcelain` shows no tsukuroi round-79 artifact. Two files dated inside the wave window in `/tmp` (`x`, 0 bytes, 16:10; `o.1978295`, 16:11, another lane's `COUNTER_RECEIPT` output) carry no round-79 or tsukuroi marker; under QUALITY 75 they stay `[unk]` and are **not** attributed to a round-79 seat. The two rows above are the whole of the round's cross-seat interference. | none required beyond the two fixes recorded |

## Wave settlement and recovery

PENDING-SETTLEMENT — the orchestrator's `w1-results.json` does not exist yet
(`.ufo/waves/round-79/w1-results.json` is absent at the time of this draft, while
round 78's is present), so the seat roster, the `review_sha256=` result line
that C1's review binding requires (`tools/measure-unit-deps-r79.py:117-128`
reads `RESULTS = .ufo/waves/round-79/w1-results.json`), and the WAVE-DONE
message are all still to be filed by the L1. What is observable from the wave
directory at this draft: 12 seat report files are present
(`w1/*.md`, one per dispatched seat, this seat's among them), so no seat is
missing a report; dead-seat count is not asserted here because the L1's own
settlement is the authority.

Two wave-settlement facts belong in the record rather than in a PENDING marker,
because they are already decided by the bytes:

- **A transient red is not a defect.** ReviewRegistry's F4 red (above) and
  ExecInstrument's red-before selftest evidence (`w1/ExecInstrument.md`, mutated
  scratch copies, 9 cases / 4 failed and 23 cases / 19 failed) are the same
  class of event in opposite directions: a red run that a later, byte-pinned run
  does not reproduce is evidence about the bytes that ran, not about the tool.
- **The C1 numeric gate cannot be met this round.** `corpus/knowledge/systemd-dependency-propagation-r79.json`
  (SHA-256 `1b8f833d…`) differs from `before/expected.json` in exactly one
  field, DP6's `statement`, because the reviewer required the source's
  precondition. The counter's equality leg therefore reads `count=0 … reason=finite-content-mismatch`
  for the landed bytes at any revision. C1 is a declared miss; C2 verifies.

## QUALITY check

This is the scribe's explicit check against the applicable numbered criteria,
not an admission.

- **1 (every claim falsifiable or marked opinion).** Every factual sentence
  above carries a file, a line, a digest or a receipt. The three counts this
  seat measured independently (48 → 46 of 97/93 gate rows failing the
  self-test-cell clause; the two prose-only second mentions at `:6038`/`:6039`;
  the two-of-eight row-keyed reconstruction of the closure's claim) are stated
  with the method that produced them and are reproducible by re-running the
  frozen checker's own `current_rows` against `git show <rev>:SKILL.md`. No
  opinion is asserted as measurement; the survivals in the attack reports are
  reported as survivals, not as passes.
- **2 (every claim carries a source anchor).** Anchors are `path:line` or a
  named receipt: `SCORECARD.md:6625-6632`, `corpus/lessons/round-78-verifier-spotcheck.md:170-173`,
  `corpus/lessons/round-78.md:78-80`, `tools/check-gate-standard-r79.py:41`,
  `:127`, `:145-158`, `:159-171`, `tools/measure-unit-deps-r79.py:79-80`,
  `:97-98`, `:110-113`, `:117-128`, `before/controls.json`,
  `before/expected.json` (digest `0c09c7a4…`), the snapshot (digest
  `eb9479be…14c8`), `w1/ReviewDeps/{review-first.md,review.md,verdict.json}`,
  `w1/ReviewRegistry/findings.md` F1/F1b/F1c/F4, `w1/CriticFreeze/report.md`
  A12/A13/A14/A17/A17b/A18, `w1/MutationCounter/matrix.json`,
  `w1/ScribeSources/sources-gate.md`, and the L1 session transcript
  (path and line numbers given). No claim rests on oral knowledge, and no
  claim rests on this seat's own memory of the wave: the two wave facts quoted
  from the L1's transcript are quoted with the transcript's own timestamps.
- **5 (a rejection is kept, not silently dropped).** The three Gate rejections
  are carried with their flip conditions, and the rejection that this round's
  own review found against the lane's own instrument (the C1 equality leg
  shadowing `quote-location` and `row-shape`) is kept in the Mistakes table
  rather than folded into the claim's wording. The r78 closure's "seven" is not
  dropped either: it is restated as a claim that cannot be reconstructed, with
  the measurement that shows why.
- **14 (an admit requires an explicit, performed `## QUALITY check`).** The S329
  admit's own check is performed in `corpus/knowledge/systemd-dependency-propagation-r79.md`
  §f, where criteria 1, 2, 3, 7, 9, 66, 86, 94 and 103 are each evaluated
  against the rows. This lesson's check above is likewise performed, not
  promised: it names the criteria, the evidence and the limits.
- **96 (a counted seat writes its binding file before deep verification).**
  **This seat failed this criterion and the record must say so.** Its first
  write to the wave directory came after ~28 minutes of deep verification
  rather than first, and the consequence is visible in the lane: the L1's
  landed `corpus/lessons/round-79.md` carries the row
  `R79-SCRIBELESSON-UNSETTLED` ("The ScribeLesson seat produced no binding file
  and no report; the L1 wrote this lesson instead"), which was true when
  written at 16:30 and is false now that `w1/ScribeLesson.md` and
  `w1/ScribeLesson/round-79.md` exist. The row needs an append-only correction
  (QUALITY 4, 99) pointing at those two paths; this draft does not make that
  edit, because `corpus/lessons/round-79.md` is not this seat's file. This is
  also the one round-79 instance of the "seat assumed dead" failure mode the
  criterion exists to prevent, and it is recorded here rather than smoothed.
- **97 (host-transition gates re-verified; line-ending state is part of the
  gate's input contract).** The lane's corpus text files are CRLF-clean —
  `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SKILL.md`, `SCORECARD.md` and
  `LOG.md` each carry 0 CR lines — and the standing guard
  `python3 tools/check-line-endings-r64.py --check` reads
  `PASS (395 file(s) checked, 0 violation(s))`. The gate-standard
  instrument's own revision binding is the shared `tools/_revision.py`
  contract (QUALITY 28), imported by both new tools; no private copy of the
  validator was written.
- **110 (the per-round seat-harm tally).** Present above with the round, the
  harmed seat, the causing seat, the evidence class, the observed effect and
  the isolation fix for each entry, and an explicit empty verdict for the
  classes no seat triggered. Both entries are shared-file collisions with a
  named disclosure and a retained path; neither is attributed by timing alone,
  and neither is a kill signal or a lane-tree write outside a seat's tree.
  The two `/tmp` files dated inside the wave window that carry no round-79
  content are named in the table as checked and not attributable, rather than
  being listed as incidents.

Not claimed: no ordinal uplift, no coverage or frontier promotion, no
capability, no admission of either claim, and no outside-closure verdict.
Round-78's outside closure admitted round 78; round 79's outside closure is
pending.
