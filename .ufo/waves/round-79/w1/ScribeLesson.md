claim=frontier
verdict=drafted

# ScribeLesson — round 79 wave w1 — binding report

## What this seat serves

The **frontier step** of round 79: the round lesson (mined mistakes, the Gate
pointer, the new per-round seat-harm tally) that the L1 integrates into
`corpus/lessons/round-79.md`. This seat writes no registry row, no corpus file
and no tool; it writes only its own report and its own `ScribeLesson/` directory.

## Artifacts

- `.ufo/waves/round-79/w1/ScribeLesson/round-79.md` — the drafted lesson.
- `.ufo/waves/round-79/w1/ScribeLesson.md` — this binding report.

## Status at this write (first write of this seat)

Lesson drafted; depth to be deepened below. Read so far: the round-79
declaration (`SCORECORDER.md` → `SCORECARD.md` `## Round 79 — declaration`),
`before/expected.json` and `before/controls.json`, the round-78 lesson and the
round-78 non-author spot-check, `corpus/QUALITY.md` criteria 1/2/5/14/96/97 and
the landed criterion 110, `considerthese/2026-10-26.md`, the pinned snapshot
`.ufo/waves/round-79/before/src/systemd.unit.xml`, and the w1 seat reports of
ScoutSources, ScribeSources, ScribeNote, ReviewDeps, ReviewRegistry, ExecRegistry,
ExecInstrument, ExecHost, CriticFreeze, MutationCounter and ConnectorScope.

## What the lesson draft contains, and what this seat measured itself

The lesson is at `w1/ScribeLesson/round-79.md`. Its Gate block is taken verbatim
from ScribeSources' draft (`w1/ScribeSources/sources-gate.md`, written 16:12),
because that seat owns the block; this seat independently re-located all four
quotes with the frozen instrument's own rule and confirmed every claimed line
range and the ≤25-word cap (7 / 21 / 24 / 24 words at `:659`, `:855-857`,
`:698-699`, `:785-787`). ScoutSources drafted a parallel Gate block with a
different admit anchor (`:666-667`); the draft records the divergence and which
choice the landed `corpus/SOURCES.md` S329 row follows.

Eight mistake rows are mined, each with an evidence anchor a reader can re-run:

1. **R79-DUPLICATE-SEVEN-VS-SIX** — the r78 closure's "seven" against the
   measured six, with the prose-vs-row cause named line by line.
2. **R79-SEVEN-NOT-RECONSTRUCTIBLE** — this seat's own finding, beyond the
   assigned three: the r79 correction cannot be checked against the closure,
   because the closure asserts a count and names no candidates, and the
   correction itself names a candidate (`count-uf-rows-r74`) the closure never
   named and places its prose mention in the wrong block (Round-74 counters
   paragraph at `:6038`, not the round-73 continuation block). Measured at both
   the closure's revision `a15aff6e…` and the base: of the eight r78-registered
   paths, four are also rows of a later table, two are single-row, two are
   row-plus-prose; the checker's six is a *different* set that adds two tools r78
   never re-registered.
3. **R79-QUOTE-TOKEN-BOUNDARY** — the first `expected.json` (digest
   `17851611…`) whose quotes were substring fragments ending inside a token,
   caught by the C1 selftest control arm before any seat existed (`reason=quote-location`
   on all eight rows), fixed by re-authoring the quotes as whole-token spans
   (`0c09c7a4…`) **and** correcting the locator's off-by-one index
   (`linenos[start-1]` → `linenos[start]`). This seat re-derived the failure
   mode: dropping the trailing punctuation from any of the eight frozen quotes
   makes `locate()` return `None`, and with the pre-fix index DP3, DP4 and DP6
   would compute wrong ranges.
4. **R79-C2-SHAPE-SCOPE** — the shape leg names two rows; measured with the
   frozen checker's own parser, 48 of 97 current `gate` rows fail its
   self-test-cell clause at the base and 46 of 93 still fail at the head. The
   other 46 are inherited debt, disclosed as a limit, not claimed closed.
5. **R79-C2-DUPLICATE-LEG-EVASIONS** — the three ways `duplicates=0` can be
   reached without repairing the six (self-declared marker, moved operative
   boundary, duplicated heading text), with the two-line fix that is *not*
   applied because the checker is frozen.
6. **R79-C1-EQUALITY-SHADOWS-DEEP-LEGS** — the strict equality leg makes
   `quote-location` and `row-shape` unreachable for DATA-side perturbations.
7. **R79-SCRIBE-LESSON-LATE-BINDING** — this seat's own QUALITY 96 failure,
   with the consequence named (the landed lesson carries a now-false row).
8. **R79-FROZEN-ROW-DP6** — the frozen DP6 statement dropped the source's
   precondition; the landed entry corrects it, so the frozen C1 tuple reads
   `count=0 … finite-content-mismatch` and C1 is a declared miss.

The `## Seat harm` table has two entries, both shared-file collisions with a
named disclosure and a retained path: ReviewRegistry reading
`tools/count-md-rows-r72.py` while ExecInstrument rewrote it (a transient rc-3
`map-digest` failure the reviewer could not attribute to the final digest), and
ReviewDeps' first digest binding being voided by ScribeNote's later edit (a
re-review cycle, with the first pass preserved in `review-first.md`). No kill
signal, no `pkill`, no lane write outside a seat's tree and no `/tmp` scratch
by a round-79 seat was found; two `/tmp` files dated inside the wave window
carry no round-79 marker and stay `[unk]` rather than attributed.

## Unchecked at this write

- No tool was executed by this seat (NO-EXEC seat: read/grep only). Every
  number above comes from read-only parsing of committed bytes (`git show`,
  `grep`, `awk`) or from another seat's own recorded receipt.
- Wave-settlement numbers (seat counts, dead seats, `w1-results.json`) are not
  yet known and are left as `PENDING` markers for the L1. The results file
  `.ufo/waves/round-79/w1-results.json` does not exist yet, and C1's review
  binding reads it (`tools/measure-unit-deps-r79.py:117-128`), so the after
  value cannot be complete without it.
- The two shared-file collisions this seat found in the w1 evidence are
  reported in the lesson's `## Seat harm` table; whether the L1's already-written
  `corpus/lessons/round-79.md` seat-harm row is amended is the L1's call.
- This seat does not edit `corpus/lessons/round-79.md` (not its file), so the
  append-only correction that rows 2 and 7 above call for is left to the L1.

## Honesty note on this seat's own conduct (QUALITY 96)

This seat's first write to the wave dir is this file, but it is **late**: it ran
several minutes of deep verification (git history, snapshot re-derivation,
transcript reads) before writing its two binding lines. QUALITY 96 requires a
counted seat's *first* write to be the binding lines plus a minimal honest body,
deepened afterwards. The L1 observed the absence of a binding file and wrote
its own lesson recording this seat as unsettled
(`corpus/lessons/round-79.md`, row `R79-SCRIBELESSON-UNSETTLED`). This report
and the lesson draft below are the seat's actual output; the L1 should replace
the "produced no binding file and no report" wording with the pointer to these
two paths. Recorded rather than smoothed.

## Deviations and hygiene

- Execution class: NO-EXEC (read/grep only). Commands actually run:
  read-only `git show` / `git log` / `git rev-list` / `git status` / `git
  rev-parse`, `grep`, `awk`, `sed -n`, `sha256sum`, `stat`, `ls`, `find`, and
  read-only `python3` heredocs that parse committed bytes (the frozen
  checker's `current_rows`, the snapshot's token stream) and print results.
  Those heredocs imported `tools/check-gate-standard-r79.py` by path, which is a
  read of committed bytes; Python reuses a valid cached bytecode file rather
  than rewriting one, and `tools/__pycache__/check-gate-standard-r79.cpython-314.pyc`
  (mtime 16:10:36) and `tools/__pycache__/measure-unit-deps-r79.cpython-314.pyc`
  (mtime 16:12:09) both carry a source mtime/size that still matches the
  unmodified sources, so neither was rewritten by this seat. Both paths are
  covered by the lane's `.gitignore` (`__pycache__/`) and `git status --porcelain`
  shows them ignored; no tracked byte changed. Disclosed rather than smoothed.
- No git or jj mutation of any kind was performed: no commit, push, stage,
  stash, checkout or reset, in the lane, the fleet root or any sibling. No
  fixture repository was created. No lane file outside my own wave directory
  and my own `ScribeLesson/` was written.
- Scratch: one temporary file under `/fast/scratch/hyaku/tsukuroi-r79/` (a
  `git show` dump of `SKILL.md` used for line-anchored counting), deleted before
  yield; the directory now holds only the L1's and ReviewRegistry's trees, not
  this seat's.
- Tooling: nothing installed or updated; no pacman transaction attempted; no
  write to `~/.local/bin` or any PATH directory.
- Model: no model parameter was passed.
