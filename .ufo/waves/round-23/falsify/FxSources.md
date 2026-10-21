# FxSources — round23 falsify: registry rows S085/S086

Bound identity: `candidate/corpus/SOURCES.md`, declared SHA256 `983c5114ece6bf4e4637a3eeae85240d2b2c03dd5f43a94e28e4380c83d90c32` (supplied declaration, not independently computed). Read-only, no commands, no fetches, leaf seat.

## Attacked claim

The landed round23 registry addition is authoritative for C1 and C3: S085/S086 are well-formed 11-column own-work/tier-A/mined rows with located anchors and populated used-by entries, and the Round23 curation note faithfully reflects the lesson Gate quotes. Specifically, S086 grounds C1's eight structured-edit authority decisions and S085 grounds C3's rough-versus-canonical path-cohort reconciliation.

## Observed facts (paths relative to lane root)

Checklist result:

| Property | S085 | S086 |
|---|---|---|
| 11 columns (header `SOURCES.md:5-6`) | yes, 11 cells at `:92`, no escaped pipes | yes, 11 cells at `:93` |
| kind/tier/status | own-work / A / mined | own-work / A / mined |
| opened / recheck | 2026-10-21 / on-release | 2026-10-21 / on-release |
| used-by populated | 2 paths | 2 paths |

Anchor inspection:
- S085 anchor part 1 is located: `def strip_sel(p):` at `.ufo/waves/round-23/sources/r22-rough-census.txt:4`, and the inner path loop's first-failure `break` at `:18` (`if q not in (b['write_paths'] if t=='write' else b['read_paths']): f['path']+=1; seats.add(x['name']); break`).
- S085 anchor part 2 (`MANIFEST rounds[422] at fleet4482c275f9381f219ee4d092e0324d417c3cb1e7`) is not in either named packet. `r22-closure.json` contains neither `4482c2` nor `rounds[422]`; its only `MANIFEST` occurrence is the spotcheck sentence "Recorded in this MANIFEST entry only" at `:36`. That identity is declared in `preregister.json:4-8` (`outside_round22.entry = 422`, `commit = 4482c275f9381f219ee4d092e0324d417c3cb1e7`).
- S086 anchor parts `observations`, `argument_keys`, `path`, `recorded_starts`, `transcript_sha256` are all present in `.ufo/waves/round-23/sources/structured-edit-observations.json`.
- S086 anchor part `baselineae01e50f582016384e620022be38bf5367000e2e` is absent from that packet. A whole-file grep for `baseline|ae01e50` returns no match; top-level keys are `schema`, `accessed`, `observations`, `scope`. The baseline is declared at `preregister.json:3`.

Gate-quote fidelity (`corpus/lessons/round-23.md:21-22`):
- S085 quote is an exact prefix of `r22-rough-census.txt:18`.
- S086 quote is the exact `scope` value at `structured-edit-observations.json:101` ("Observed structured path metadata and recorded adapter steps only, not universal tool semantics, native permission enforcement, effects, or reading proof.").
- Gate access dates `2026-10-21` match row `opened` and the packets' `date`/`accessed`.

Curation-note consistency (`SOURCES.md:154`):
- `Identified2/screened2/included2, excluded0` matches the two Gate rows; "two named historical seats" matches the packet's two distinct seats (`CritRuntime`, `OraclePathArtifact`) across four observations.
- Stop rationale ("no web fetch or host action") matches Gate "No remote source fetch is required or granted to seats."
- Reject set overlaps the Gate's reject rows on the net-count inference (`rough25/33` minus `23/29`) and the quality-trend inference. "Metadata proves effects or prevention" is not a literal Gate reject-table row, but it is entailed by candidate C1's disposition ("actual permission is separately declared lane policy, never inferred from body text") and S086's scope, so it is not a contradiction.
- Arithmetic corroboration: 25−23=2 and 33−29=4, total six; `r22-closure.json` rechecks call the 25/33-vs-23/29 census "approximate ... not decisive", and both the row scope and Gate reject the inference that six net differences are six unsafe events.

## Falsifier found

Proposition falsified: **every anchor element of S085/S086 resolves inside the row's declared source path(s)**.
- S086's `baseline ae01e50...` clause has no textual location in `structured-edit-observations.json`; it resolves only to `preregister.json:3`, which the row does not list as a source.
- S085's `MANIFEST rounds[422]`/`fleet4482...` clause has no textual location in `r22-rough-census.txt` or `r22-closure.json`; it resolves only to `preregister.json:4-8`.

This is a provenance/traceability defect, not a substantive contradiction: both identifiers are separately declared in the round preregister, both rows' `scope` and `teaches` cells deny the stronger inferences, and the Gate quotes themselves are verbatim. Severity is low; S083's anchor also carries an "immutable baseline ..." clause, so if provenance-in-anchor is intended registry convention, the defect downgrades to attribution clarity.

Bounded search that found no other falsifier: column counts against the header/separator; kind/tier/status/opened/recheck; non-empty used-by; exact Gate quotes; note counts/dates/stop rationale; the six-count arithmetic; C3 method description (bounded suffix strip, one failing component per event via `break`); and `outside quality verdict is unchanged` against `r22-closure.json` `trends.quality: unchanged`.

Precision note, not a falsifier: S086 `teaches` says "separate read/write starts", while the packet records read+write starts for 1 of 4 observations (`CritRuntime` read `:12`, write `:13`) and edit-only starts for 3 (`OraclePathArtifact` `:31`, `:34`, `:37`). The row's scope and the Gate quote ("recorded adapter steps") remain accurate.

## Effect on C1/C2/C3

- **C1**: no source-level contradiction. The packet's observed key shapes (`path` plus `stream_content`, or `i`/`new_string`/`old_string`/`path`) and separate adapter starts match the row and the premises of the eight preregistered decisions. The anchor defect does not weaken the decisions.
- **C2**: neither row claims native enforcement, prevention, effects, or reading proof; S086's scope explicitly disclaims runtime permission enforcement. This is consistent with the seeded constraint that no native restrictive task toolset exists, and no runtime enforcement is claimed anywhere in these rows.
- **C3**: S085's method description matches `r22-rough-census.txt` exactly, and the `teaches` quality clause matches `r22-closure.json`. No C3 falsifier originates from these rows.

## Smallest in-scope remedy (L1 integration only; not applied by this seat)

1. One-cell attribution fix per row: keep the verified in-packet anchor elements and move the round-level identifiers to a provenance clause naming `preregister.json`, or add `preregister.json` to the row's `source` cell. Concretely: S086 anchor keeps `observations argument_keys/path/recorded_starts and transcript SHA-256; opened2026-10-21` and attributes `baseline ae01e50...` to the preregister; S085 anchor attributes `rounds[422]`/`4482c275...` to `preregister.json outside_round22`.
2. Optional one-phrase precision: S086 `teaches` "separate read/write starts" → "separate read/write/edit adapter starts" to match the three edit-only observations.

No change to status, recheck, used-by substance, teach claims, or the lesson Gate; the Gate quotes are exact and must not be rewritten.

## Unresolved under binding (not absence)

- Used-by referents `corpus/knowledge/path-reconciliation-r23.md` and `corpus/knowledge/structured-edit-r23.md` lie outside this seat's declared read set; their existence/citation is unverified. The other used-by referent, `corpus/lessons/round-23.md`, is bound and cites both rows and assigns S086→C1, S085→C3 (`:21-24`).
- "All old status/recheck/used-by fields unchanged" cannot be re-derived without a baseline copy; NO-EXEC forbids git/diff. The adjacent S084 row is intact in the bound copy.
- Lesson `R23-RAW-ORDER` names the selftests `mixed-raw-range-order` and `rough-misses-raw-first`; `measure/l1-mutation.json` mutant 0 records only aggregate `selftest: FAIL`, `exit: 1`, `killed: true`. General fail-capability is confirmed; exact test identity is not located in declared evidence.
- Confidence: high on cell counts and anchor presence/absence (direct reads plus whole-file greps of the exact packets); medium on whether provenance identifiers belong in `anchor` by convention (S083 precedent). No command was executed and no digest was recomputed.

Reviewed-SHA256: 983c5114ece6bf4e4637a3eeae85240d2b2c03dd5f43a94e28e4380c83d90c32
Predicate: r23f-fxsources
Scope: executed=none
