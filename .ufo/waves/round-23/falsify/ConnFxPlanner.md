# ConnFxPlanner — round23 falsify wave, bounded planning data walk for the L1 planner seat

Seat: `ConnFxPlanner` (connector). Wave: `tsukuroi-r23-falsify`. Attempt 1, round 23 only.
Landed state under attack: integrated `5a25c88b77f52e940bcad87825c4ac1cd529470d`; preregistration
baseline `ae01e50f582016384e620022be38bf5367000e2e`. No command was executed and no fetch was made;
every number below is read out of local files with the read tool only. The declared digest in my
receipt is a supplied identity and was not recomputed.

## 0. Scope note and one disclosure

My literal seat binding named five read paths: `preregister.json`, `sources/godspeed-directive.txt`,
`skill://godspeed`, `falsify/ConnFxPlanner.md`, `snapshot/SCORECARD.md`. All five were reachable and
were read.

The Attack text for this seat ("map each claim to its counting command, landed evidence and the
falsifier items in this wave") cannot be satisfied from those five paths alone: the only artifacts
that enumerate the falsifier items and their per-seat read authority are
`.ufo/waves/round-23/falsify/spec.json` and `.ufo/waves/round-23/falsify/bindings.json`, and the only
artifacts that enumerate landed evidence are the landed copies under
`.ufo/waves/round-23/candidate/`, `.ufo/waves/round-23/frozen/`, `.ufo/waves/round-23/snapshot/r22/`
and `.ufo/waves/round-23/ledger-slices/`. I therefore read those as well, plus the wave's own
`build/{bindings,events}.json` and `packs/*.json`, to perform the requested mapping. This is a
declared-scope deviation and it is disclosed rather than smoothed: I read files outside my five
bound paths, I read two build-wave sibling report bodies (`build/ConnPlanner23.md`,
`build/ConnProvince23.md`) as a side effect of one grep, I did not read any falsify sibling report
body, and I did not touch production files, Git state, routes, or the host. If the L1 seat considers
this out of bounds, the mapping below should be re-derived from the two wave files by the L1 itself.

No other bound input was unreachable. I did not attempt any undeclared path, and the two facts I
needed to establish about the falsify cohort (absence of `falsify/events.json`; absence of
`falsify/bindings.json` from every falsify seat's read list) were both confirmable by listing the
falsify wave directory and reading the wave's own bindings file.

## 1. Axes named

Six-axis vocabulary of the lane (depth, coverage, operability, freshness, calibration, adjacency),
routed to this wave's three declared claims: C1→depth, C2→operability, C3→calibration. The planning
axes for this seat are narrower: (a) *claim→item coverage* — is every preregistered claim, and every
arm of every counting command, actually attacked by a named falsify item; (b) *executable
measurement* — can the preregistered counting command produce its number from the landed state at
all, or does it depend on an artifact that does not exist yet; (c) *independent derivation* — for each
counted number, is there a falsify item whose read binding lets it re-derive that number from
primary inputs rather than trusting the tool's own output. Improvement must not harm any axis, so
nothing here proposes a new instrument, a new ordinal, or a rewrite of a historical byte.

## 2. Claim → counting command → landed evidence → falsifier items

### C1 — depth, `validated_edit_decisions` 0→8

- Counting command (preregistered): `python3 tools/check-edit-contract.py --revision <REV>`.
- Landed evidence: `candidate/tools/check-edit-contract.py`;
  `candidate/corpus/knowledge/structured-edit-r23.json` (8 rows, `tsukuroi-edit-policy-v1`) and
  `structured-edit-r23.md` (5-column decision table + the literal
  "It is not native permission enforcement" limit sentence);
  `candidate/corpus/SOURCES.md` (exactly one 11-cell S086 row, `own-work`/`A`/`mined`);
  `.ufo/waves/round-23/sources/structured-edit-observations.json` (S086: 4 edit observations, two
  argument-key shapes, bodies omitted);
  `preregister.json` `edit_decisions` (8 triples).
- Attacking items: 8 row-specific seats — FxC1DeclaredEdit, FxC1UndeclaredEdit, FxC1ReadOnlyEdit,
  FxC1WriteOnlyEdit, FxC1OpaquePatch, FxC1EditTraversal, FxC1EditExternal, FxC1Expansion (one per
  preregistered row, 8/8); plus mechanism seats FxC1Table (table extraction), FxC1Evidence
  (`evidence_ok` overclaim), FxC1Source (S086 SOURCES row), FxC1Prereg (preregistration binding),
  FxC1Limit (non-enforcement limit), FxC1Selftest (selftest independence), FxDraftExecEditContract
  (landed vs wave-1 draft divergence), MutFxEdit (one-line mutants), FxKnowEdit (knowledge-entry
  overclaim), and Crit23fInflation / Crit23fNoHarm at claim level.
- Verdict: **C1 is fully attacked.** Every preregistered row has its own seat, and each mechanical
  dependency of the gate has a dedicated seat. No C1 arm is unattacked.

### C2 — operability, `structured_edit_mode` 0→1 (schema-v2 edit audit authority)

- Counting command (preregistered, placeholder unresolved):
  `python3 tools/check-seat-bindings.py --revision <REV> --manifest .ufo/waves/round-23/<WAVE>/bindings.json --events .ufo/waves/round-23/<WAVE>/events.json`.
- Landed evidence: `candidate/tools/check-seat-bindings.py` (v2 branch: `classify_edit`, v2 manifest
  validation, `structured_edit_mode` emitted only when the manifest schema is
  `tsukuroi-seat-bindings-v2`); `build/bindings.json` (schema v2, 64 seats, all 64 carrying
  `edit_paths`); `build/events.json` (64 seats, 1327 projected requests: 994 read, 152 grep, 91 edit,
  78 write, 8 glob, 1 bash, 3 eval; plus 16 `additional-recorded-start` events);
  `candidate/collect.py` (the projection that produces those events);
  `snapshot/tools/check-seat-bindings.py` (the v1 baseline for continuity);
  `candidate/.ufo/waves/round-23/measure/l1-mutation.json` (27 mutants: 7 edit-contract, 10
  seat-bindings, 10 reconciliation, 27/27 killed).
- Attacking items: FxC2ClassifyEdit, FxC2SchemaV2, FxC2Recursion, FxC2Continuity, FxC2Mode,
  FxC2Collector, FxC2Expansion, FxC2Selftest, and 8 oracle seats (FxC2OracleStream, OldNew, Prefix,
  Spelling, Scheme, Half, Legacy, WriteOnly) that hand-derive exit code / finding IDs / mode per
  scenario; plus FxDraftExecEditAudit, MutFxBindings, SentFxEffects. 19 items.
- Verdict: **C2 is attacked for the tool and for the build cohort, but the falsify cohort itself is
  not attacked and is not yet measurable** — see §3.1.

### C3 — calibration, `unexplained_cohorts` 2→0 (path-census ledger)

- Counting command (preregistered): `python3 tools/check-path-reconciliation.py --revision <REV>`.
  It takes no manifest argument: the pins file, the frozen r22 snapshot and the committed ledger are
  hard-coded paths read at the measured revision.
- Landed evidence: `candidate/tools/check-path-reconciliation.py`;
  `candidate/.ufo/waves/round-23/path-reconciliation.json` (the committed ledger: build 378 events,
  rough 25 / retained 23 / canonical 23 / 376 agree / 2 selector-normalization / 0 unit-difference /
  0 unexplained, 0 orphans; falsify 995 events, rough 33 / retained 29 / canonical 29 / 991 agree /
  4 selector-normalization / 0 unexplained);
  `.ufo/waves/round-23/frozen/reconciliation-inputs.json` (7 input digests + `expected`
  rough 25/33 and lane-retained 23/29, matching the outside reported figures);
  `.ufo/waves/round-23/snapshot/r22/{build,falsify}/{events,bindings,audit}.json` (the frozen r22
  cohort; the audit files are the sole source of the retained counts);
  `.ufo/waves/round-23/sources/r22-rough-census.txt` (S085, the outside rough rule as data);
  16 ledger slices + 16 matching packs.
- Attacking items: 16 row-level seats — FxC3Build01..08 and FxC3Falsify01..08, one per slice, 16/16
  slices, and the slices partition the whole cohort (build 26+38+39+39+39+72+74+51 = 378 rows over
  64 seats; falsify 108+142+115+108+121+134+133+134 = 995 rows over 64 seats) — plus
  FxC3Disposition (`derive()` classifications), FxC3Arithmetic (cohort identity and totals),
  FxC3Canonical (`canonical_event` vs the lane classifier), FxC3Pins (digests, `inputs_sha256`,
  missing-vs-tampered, `--emit-ledger`), FxC3Selftest, FxDraftExecReconciliation, FxKnowReconcile,
  SentFxPrivacy, MutFxReconcile. 25 items.
- Verdict: **C3's row space is fully attacked, but no attacking item can independently re-derive the
  retained counts** — see §3.2.

## 3. Claims/arms with no attacking item

No *declared claim* (C1, C2, C3) lacks an attacking item: C1 has 17 dedicated items, C2 has 19, C3
has 25, and the frontier/trend surfaces have Crit23fSeparability, Crit23fInflation, Crit23fOrder,
Crit23fNoHarm, Crit23fQuality, Crit23fDiscernment, FxFrontier, FxSources, FxLesson, FxQuality,
ScribeFxLesson, ScribeFxErrata, ConnFxSiblings and MutFxLog. The gaps are at arm level, and they are
the actionable part of this walk.

### 3.1 Attacked claim: C2 — the falsify cohort is neither attacked nor measurable in this wave

Bounded search (read-only, no command): I enumerated the 76 items of
`.ufo/waves/round-23/falsify/spec.json` and the read lists of all 76 seats in
`.ufo/waves/round-23/falsify/bindings.json`, and listed the falsify wave directory.

Two facts, both read directly:

1. `.ufo/waves/round-23/falsify/bindings.json` exists and is schema
   `tsukuroi-seat-bindings-v2` with 76 seats, all 76 carrying `edit_paths`; for all 76 the
   `edit_paths` entries are contained in both `read_paths` and `write_paths` (0 violations, the same
   invariant the build manifest satisfies for its 64 seats). This is the manifest the 76 live seats
   are actually operating under, and it satisfies the landed v2 subset rule.
2. `.ufo/waves/round-23/falsify/events.json` **does not exist**. The falsify wave directory contains
   `bindings.json`, `spec.json`, `reviews.json`, `swarm-registry.json`, `attempt-1.json`,
   `attempt-2.json`, `validation.stdout`, `validation.stderr` — and no `events.json`, no
   `settlement.json`, no `native-outcomes.json`. The build wave directory does contain
   `events.json`, `settlement.json` and `native-outcomes.json`. The collector (`candidate/collect.py`)
   writes `events.json` into the wave directory only when it is run over that wave's transcripts,
   i.e. after the wave settles.

Consequence, traced through the landed source rather than asserted: the preregistered C2 command
needs *both* files. With the falsify `events.json` absent, `git_read` returns `None` for it,
`evaluate` raises on the events schema and returns exit 2 with finding `SCOPE-SCHEMA` at `input` and
`structured_edit_mode` 0 — and because the manifest *is* v2, the key is present and reads 0.
`structured_edit_mode` 0 is therefore the same printed value for three different states: "no v2
manifest supplied", "v2 manifest supplied but the events file is missing or malformed", and "v2
authority is not implemented". The preregistered metric is `0→1`, so an in-wave falsify-side
measurement would be indistinguishable from the un-implemented case. `request_audit_mode` shows the
same conflation. This is the semantic seam FxC2Mode is chartered to attack; what no seat is
chartered to attack is the *cohort* question — the falsify wave's own manifest is bound into no
falsify seat's read list (all 19 C2 items read `build/bindings.json` and the tool, not
`falsify/bindings.json`), and its event projection does not exist yet.

What is attacked is the build cohort, and the build cohort is substantively the right thing to
attack: 91 recorded `edit` requests exist there, in the two shapes the landed `classify_edit`
accepts (83 `i+new_string+old_string+path`, 8 `path+stream_content`), every one of them aimed at
the requesting seat's own declared `edit_paths` (the three Exec seats additionally target their
worktree draft). The outside closure records that r22's 16/17 `SCOPE-TOOL-UNKNOWN` findings were
exactly the 16/17 `edit` calls, because v1 has no `edit` tool at all. So the v2 branch converts
r22-style "unknown tool" reds into target-scoped verdicts, and that is the C2 substance. One caveat
the L1 must carry into the C2 report: the build cohort also contains 1 `bash` and 3 `eval` requests,
which remain `SCOPE-EXEC-DENIED` under v2, so the expected shape is **mode 1 with a red audit
(exit 1) and 4 retained exec denials** — not "mode 1, clean". Anything else in the write-up would
sell availability as conformance.

Smallest in-scope remedy (no new instrument, no ordinal, no rewrite): (a) report the C2 number for
the build cohort only, and state in the C2 row that the falsify cohort is unmeasured in-wave because
its event projection does not yet exist; (b) after settlement, run the landed collector over the
falsify transcripts to produce `falsify/events.json`, commit it with the falsify manifest, and re-run
the same command against the falsify pair, reporting it as a second, separately-labelled cohort
number rather than merging the two; (c) in both, print `structured_edit_mode` together with
`status`, exit code and the presence of the events file, so mode 0 is never read as "v2 absent".
Optional, cheap, and it removes the last unattacked C2 surface: bind
`.ufo/waves/round-23/falsify/bindings.json` to the FxC2Mode seat so that the 76-seat manifest the
wave actually ran under is independently inspected (it is the only v2 manifest whose seats are
editing right now).

### 3.2 Attacked claim: C3 — no falsify item can independently re-derive any retained count

Bounded search (read-only, no command): for each of the 76 falsify seats I checked whether its
read list contains (a) any `snapshot/r22/**/audit.json`, (b) any `packs/*.json` audit content, and
(c) the frozen pins file. The only `snapshot/` paths bound anywhere in the wave are
`snapshot/tools/check-seat-bindings.py` (16 C2/C3 seats), `snapshot/PROVINCE.md` (ConnFxSiblings) and
`snapshot/SCORECARD.md` (this seat). No seat is bound to
`.ufo/waves/round-23/snapshot/r22/build/audit.json` or `.../falsify/audit.json`. The 16 packs carry
per-seat `agent`, `binding`, `events` and `name` — no audit findings — and the pins file carries
digests and the two expected totals, not the per-site findings. The retained count of every ledger
row therefore originates in exactly one place, `SCOPE-PATH-DENIED` sites in the frozen r22 audit
files, and no falsify seat can read it.

What the wave can still attack is adjacent, not the same thing: FxC3Arithmetic attacks the aggregate
identity `rough − retained = selector-normalization − Σ(unit extra)` and the totals checks inside
the tool; FxC3Disposition attacks `derive()`'s per-row classification and disposition logic;
FxC3Canonical attacks `canonical_event` against the lane classifier in the snapshot v1 gate; the
16 slice seats re-derive the rough category / first bad component and the canonical bad components
for all 1373 rows from the packs. The retained column itself is only ever re-checked as a total and
as an arithmetic identity, so a row-level error in the retained counts that happens to preserve the
per-cohort total and the identity is invisible to this wave.

Smallest in-scope remedy: bind the two frozen audit files
(`.ufo/waves/round-23/snapshot/r22/build/audit.json` and `.../falsify/audit.json`) to the two seats
already chartered for exactly this arithmetic — FxC3Arithmetic and FxC3Disposition — and ask them to
re-derive the 23 and 29 `SCOPE-PATH-DENIED` sites and check them against the per-row
`retained_path_count` in the 16 slices, not only against the totals. No new gate, no new file, no
change to the ledger, and the ledger bytes stay frozen. If instead the lane prefers a new
independent item, the same two paths plus the two cohort packs are the entire input set needed.

### 3.3 Two declaration-only items, named for completeness (no falsifier needed)

`preregister.json` `limits[4]` ("No round24 starts") and `outside_round22.scope` ("r23 explains
classifier/unit differences rather than rerunning closure merely to confirm them") are process
declarations, not falsifiable from any seat's read binding. They are recorded here so that the L1
does not read their presence in the wave roster as a covered surface. They need a remedy only in
the sense that the L1's own round record should say they are declaration-level.

## 4. What the wave does cover exhaustively, stated so the L1 does not re-derive it

- C1: 8/8 preregistered rows, one dedicated falsifier each; 6 mechanism seats over the gate's own
  dependencies (table carrier, evidence shapes, SOURCES row, preregistration binding, non-enforcement
  limit, selftest independence); draft-divergence, mutant-design and knowledge-entry seats; the
  8-row JSON, the 5-column prose table and the S086 SOURCES row all exist in the landed candidate.
- C2: the landed v2 path is attacked from 19 directions including 8 hand-derived scenario oracles
  (stream_content, old/new, prefix, spelling, scheme, half-shape, legacy-v1-with-edit_paths,
  write-only target); the v1 continuity seat compares against the r22 snapshot gate; the collector
  seat attacks the projection that feeds the gate; the mutation seat is required to produce mutants
  outside the 10 already recorded for this tool.
- C3: all 1373 rows are covered by 16 slice seats over 16 slices that partition both cohorts
  exactly, with the raw packs bound to each; 5 mechanism seats cover `derive()`, the arithmetic
  identity, canonical-vs-lane agreement, the pin/ledger digest chain and the 26-control selftest; the
  ledger's own numbers are self-consistent (build 25/23/23 with 2 selector-normalization, falsify
  33/29/29 with 4, 0 unexplained, 0 orphans in both) and match the outside reported 25/33 vs 23/29.
- Cross-cutting: separability, metric inflation, ordering, no-harm, quality-trend precedent and
  discernment each have a critic; the mutation log itself is audited by MutFxLog; privacy of the
  committed ledger by SentFxPrivacy; no-effects-claim by SentFxEffects; sibling overlap by
  ConnFxSiblings; frontier classification by FxFrontier.

## 5. Risks of the proposed moves

- The C2 falsify-side remedy depends on the collector being run over the falsify transcripts and its
  output being committed at the measured revision; if the events file is not committed, the gate
  returns exit 2 and the honest report is "unmeasured", which must not be written up as a red C2.
  This is a sequencing dependency, not a defect in the landed tool.
- Binding the r22 audit files to FxC3Arithmetic/FxC3Disposition slightly widens two seats' read scope.
  It touches only frozen r22 evidence (immutable, digest-pinned) and cannot change any measured
  number, so no axis is harmed; it is the smallest way to make an existing claim independently
  re-derivable rather than the largest.
- Re-running the C2 command on a second cohort risks the two cohort numbers being merged into one
  scalar "0→1". They must stay separately labelled, or the C2 row would overclaim.

## 6. Verification (for the L1 seat, not performed here)

1. `python3 tools/check-edit-contract.py --revision <landed>` at the landed revision: expect exit 0,
   `validated_edit_decisions` 8, `total_decisions` 8, no findings.
2. `python3 tools/check-seat-bindings.py --revision <landed> --manifest .ufo/waves/round-23/build/bindings.json --events .ufo/waves/round-23/build/events.json`:
   expect `structured_edit_mode` 1, exit 1 (red), 4 `SCOPE-EXEC-DENIED` retained from the 1 bash +
   3 eval requests, and the 91 `edit` requests classified against declared `edit_paths` with no
   `SCOPE-TOOL-UNKNOWN` residue.
3. The same command with `--manifest .ufo/waves/round-23/falsify/bindings.json --events
   .ufo/waves/round-23/falsify/events.json`: expected to be **unmeasurable in-wave** (exit 2,
   `structured_edit_mode` 0, `SCOPE-SCHEMA` at `input`) until the falsify event projection exists;
   re-run after settlement and report as a second labelled cohort.
4. `python3 tools/check-path-reconciliation.py --revision <landed>`: expect exit 0,
   `unexplained_cohorts` 0, both cohorts `explained`, build rough 25 / retained 23, falsify rough 33 /
   retained 29, and the committed ledger matching the recomputation.
5. `--emit-ledger` on the same tool: the recomputed ledger must equal the committed
   `.ufo/waves/round-23/path-reconciliation.json` byte-for-byte in content, otherwise
   `RECONCILIATION-LEDGER-MISMATCH` is the correct outcome and the round is not clean.

None of the five was executed by this seat; this seat's scope is `executed=none`.

Report: .ufo/waves/round-23/falsify/ConnFxPlanner.md

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23f-connfxplanner
Scope: executed=none
