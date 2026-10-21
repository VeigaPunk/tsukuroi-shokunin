# ConnPlanner23 — round23 bounded planning data walk

Seat: ConnPlanner23, leaf connector. L1 retains the planner. This is planning data only:
no production edit, no named draft, no command, fetch, hash or list. The snapshot digest
`09af22c5…` is the declared identity supplied by the assignment, not independently computed.
Citations point only at this seat's bound files. `executed=none`.

## 0. Axes named, and the tied-lowest check

| Axis | Round23 claim | Before → target | Ordinal |
|---|---|---|---|
| depth | C1 typed structured-edit decision contract | `validated_edit_decisions` 0 → 8 | 8 → 8 (0) |
| operability | C2 explicit structured-edit audit authority | `structured_edit_mode` 0 → 1 | 9 → 9 (0) |
| calibration | C3 independent outside path-census reconciliation | `unexplained_cohorts` 2 → 0 | 9 → 9 (0) |

Inherited and untouched: coverage 9, freshness 9, adjacency 8. The operative ordinals are
`preregister.json:98-105` — depth 8, adjacency 8, coverage 9, operability 9, freshness 9,
calibration 9 — with `ordinal_delta` 0, `retired` empty, `capability_acquisition:false`,
`exploratory:false` (`:106-109`). **Tied-lowest is depth 8 and adjacency 8**; C1 works depth.
`SCORECARD.md:716` labels C1 “depth8→8 (0, tied-lowest)”, and the round20 baseline line
`SCORECARD.md:616` carries the same six inherited values. Confirmed.

Two archival-versus-operative discrepancies are stated rather than smoothed:

1. `SCORECARD.md:52` (the round-11 terminal self-assessment) still shows adjacency 7, coverage 8
   and freshness 8. Those cells are historical; the later inherited ordinals (`:616`) supersede
   them. Anyone quoting `:52` as current would name the wrong tied-lowest pair.
2. Working depth discharges the tied-lowest duty this round (same pattern as the round20 and
   round22 declarations at `:616`, `:678`). Adjacency 8 remains unworked, not harmed.

## 1. Evidence ledger (verified from bound data)

| Datum | Value | Evidence |
|---|---|---|
| Baseline | `ae01e50f582016384e620022be38bf5367000e2e`, clean at start | `SCORECARD.md:710`; `preregister.json` `baseline` |
| Outside round22 closure | entry 422, admitted true, verifier CloseKaidoku22, commit `4482c275…`; trends expansion unchanged / quality unchanged / discernment improved | `preregister.json` `outside_round22`; `SCORECARD.md:710` |
| Outside path counts as reported | rough build 25 / falsify 33; lane build 23 / falsify 29 | `preregister.json` `outside_round22.path_counts_as_reported` |
| Three claims frozen before candidate outputs | C1/C2/C3 table | `SCORECARD.md:712-718` |
| C1 scope | eight finite source-grounded decisions; “new document contract, not eight repaired runtime behaviors” | `preregister.json:34` |
| C2 scope | schema-v2 audit authority; legacy v1 and historical reds unchanged; body opaque; no native enforcement/effects claim | `preregister.json:43` |
| C3 scope | 2 → 0 unexplained cohorts over fixed r22 build/falsify; provenance and arithmetic | `preregister.json:48-51` |
| Separability sentence | C1 reads only decision/prose/source contract; C2 only v2 authority and captured events; C3 only frozen r22 evidence and its reconciliation record; revision binding is infrastructure | `preregister.json:55`; `SCORECARD.md:720` |
| Limits | no native per-seat restrictive interface; no runtime prevention, effect/reading/recorder-completeness or universal tool/patch semantics | `preregister.json:110-112` |
| C1 contract rows | 8 decisions, `ALLOW` 1, `DENY` 5, `UNKNOWN` 1, `CHECK_EACH` 1 | `edit-decision-policy.json:5-59` |
| C1 evidence key | every row cites `S086`; every row's `policy` is `round23-preregister` | `:8,15,22,29,36,43,50,57` |
| C1 observation source | `source_path` = `.ufo/waves/round-23/sources/structured-edit-observations.json`; scope: metadata audit only, no prevention/opaque interpretation/effect/reading proof | `:61-62` |

## 2. Causal separability — declared disjoint, implementation discipline unverified

The declared input loci are path-disjoint:

- **C1**: the 8-row contract in `sources/edit-decision-policy.json` (`:5-59`, source `:61`),
  read by `tools/check-edit-contract.py --revision <REV>`.
- **C2**: a new schema-v2 `bindings.json` plus `events.json` under
  `.ufo/waves/round-23/<WAVE>/`, read by
  `tools/check-seat-bindings.py --revision <REV> --manifest … --events …`
  (`preregister.json:42`).
- **C3**: frozen round22 build/falsify evidence plus one reconciliation record, read by
  `tools/check-path-reconciliation.py --revision <REV>` (`preregister.json:51`).

Separability therefore holds on the declared command paths, subject to four exact-path
conditions that a falsifier must check because this seat cannot read the checker sources:

1. The C1 checker must not open any round23 `bindings.json`/`events.json` and must not read the
   C1 checker's own output as an input.
2. The C2 checker must not open `sources/edit-decision-policy.json`, the C1 registry or the C1
   measurement output. Note C2's command has no explicit policy path, so any cross-read would be
   hardcoded and invisible from the CLI.
3. The C3 checker has **no explicit record argument** — its reconciliation record path is implicit
   in the tool. It must resolve exactly one record path outside C1/C2 artifacts and must not
   enumerate `.ufo/waves/round-23/build/`; a directory scan would silently absorb the C2
   manifest and falsify `preregister.json:55`.
4. Shared `--revision` binding is infrastructure only, per `:55` and `SCORECARD.md:720`.

Shared provenance is not, by itself, a production dependency. Both C1 and C2 descend from the
prospective `S086` source (`preregister.json` `sources_opened[1]`; policy evidence keys above).
The round21 precedent states the rule: “shared semantic expectations do not create a production
dependency” (`SCORECARD.md:650`). It becomes a violation only if C2's evaluator reads the C1
policy file or the C1 checker reads the v2 manifest.

Residual separability risks:

- **Uniform evidence key.** All eight C1 rows cite one key, `S086` (“observed structured edit
  request keys and recorded adapter steps”). Rows `EDIT_TRAVERSAL` (`:40-41`), `EDIT_EXTERNAL`
  (`:47-48`) and `EXPANSION` (`:54-55`) are normative rules, not obviously observed request keys.
  If `structured-edit-observations.json` contains only read/write/edit key observations, three of
  eight rows are declared policy with a nominal citation. The count of eight decisions can still
  validate; “source-grounded” would be weak for those rows. This is a verifier duty, not a defect
  asserted here — the observations file is outside this seat's read binding.
- **Producer ambiguity on the counts.** `preregister.json` nests both `rough` and `lane` under
  `outside_round22.path_counts_as_reported`, while `SCORECARD.md:720` reads “Outside approximate
  25/33 versus lane 23/29”. That sentence can be read as outside = 25/33 and lane = 23/29, but
  both numbers are recorded under the outside block, where “rough” and “lane” more plausibly name
  two counting policies. C3 must name the producer **and** the policy for each number, not only
  reconcile the arithmetic; otherwise a correct component sum can still misattribute the count.
- **Circular-looking provenance label.** Each row's `policy` field names `round23-preregister`,
  the artifact that declares the same rows. That field is a governing-policy label, not evidence;
  the independent comparison is metadata versus lane authority (`preregister.json:34`), with
  `S086` the only external anchor.

## 3. Availability versus repaired behavior — confirmed for C1/C3, gap in C2

- **C1** is explicitly a document contract, not repaired runtime behavior (`preregister.json:34`).
  The 0 → 8 count is eight policy decisions; depth remains 8 → 8 (0). No behavioral repair is
  claimed or implied.
- **C2** is availability of a new v2 audit mode. Old schema-v1 policy and historical reds stay
  unchanged (`preregister.json:43`; `SCORECARD.md:717`), and the scope disclaims native
  enforcement and effect proof. The mode is detection evidence, not prevention and not a repair.
- **C3** is explanatory accounting over frozen r22 evidence. It “does not retrospectively
  authorize an event or alter the original audit” (`SCORECARD.md:720`). 2 → 0 unexplained cohorts
  is reconciliation completion, not a repaired old audit.

The lane's own precedents bind how the C2 availability may be credited:

- Round21 C2 separated `target_type_mode` (availability) from `target_type_tools` (behavior,
  9 → 9) and demanded a **discriminating witness**: the same weakening mutant had to survive the
  old frozen matrix and fail the new one; “No 9-fold credit for one availability fact”
  (`SCORECARD.md:648`).
- Round22's refinement: “A mode flag alone is never an acceptance criterion”; the mode required an
  evaluable complete inventory, and malformed/incomplete evidence could not satisfy it
  (`SCORECARD.md:688`). The measured credit was “improved instrumentation verified, **not
  conformance**”, with a fully evaluated red and no incomplete seats (`SCORECARD.md:699`).

**Gap.** The round23 C2 declaration (`preregister.json:42-43`; `SCORECARD.md:717`) restates
neither the fully-evaluated/no-incomplete precondition nor a discriminating witness. A bare
`structured_edit_mode=1` could be satisfied by schema acceptance while the read+write+edit rule is
untested — exactly the availability-as-achievement credit that `:648` and `:688` corrected.
C1's eight rows cannot serve as C2's witness: importing them would couple the claims and falsify
`preregister.json:55`.

Secondary second-order risk: `OPAQUE_PATCH` resolves to `UNKNOWN`, not `DENY`
(`edit-decision-policy.json:33-34`). If the real v2 audit treats an edit event with no structured
target as clean because no rule fired, the opaque decision is inert and “exact predeclared targets
require read+write+edit authority” leaves the no-target case permissive. No bound file states the
fail-closed mapping; the audit must be observed to be not-clean on no-target events.

## 4. Proposed move (one, bounded, supporting only)

**C2 v2 authority witness pair + fully-evaluated precondition, local to C2.**

This is a compatible synthesis between the round's C2 proposal and the round21 C2 *verification
pattern* (`SCORECARD.md:648`) — deliberately **not** a synthesis between C1 and C2 content, which
would break `preregister.json:55`. It changes no metric, target, claim text or ordinal: `before`,
`target` and `ordinal_delta` stay frozen; `structured_edit_mode` remains 0 → 1.

Steps for L1 (planner retains these; this seat executes none):

1. Before the final measurement, freeze a minimal synthetic fixture set:
   - **A**: one structured target declared in `read_paths` + `write_paths` + `edit_paths` → v2
     clean.
   - **B**: identical except the target is in `edit_paths` but missing from exactly one of
     `read_paths`/`write_paths` → v2 `DENY`-class finding.
   - **C**: an edit event with only opaque body and no structured target → `UNKNOWN`/not-clean,
     never clean; this makes the `OPAQUE_PATCH` row operative.
2. Replay A/B/C through the legacy schema-v1 default path and pin byte/verdict identity to the
   baseline. Use an opt-in v2 mode or the selftest path; do not edit the legacy path. This is the
   `old schema-v1 results unchanged` obligation (`SCORECARD.md:717`).
3. Record the fixture digests, expected/observed verdict pairs and the final evaluator digest in
   one frozen witness JSON *before* claim results are known. No witness added after seeing them.
   If the final measurement is already frozen, record it as a separately frozen supporting
   artifact and do not let it alter the claim verdict.
4. Credit the mode only if the real round23 v2 audit is fully evaluated: finite findings, zero
   incomplete/unknown seats, exit 0 or explicit evaluated-violation exit 1 (the `:688`/`:699`
   standard). Schema acceptance or a flag alone does not earn the mode.
5. Mutation control: weaken the v2 check to “`edit_paths` membership alone is sufficient” → the
   witness B must fail (kill) under v2 while the legacy replay stays byte-identical. Mirror the
   `TARGET_TYPE_WITNESS` form at `SCORECARD.md:648`.
6. Reproduce the tuple expectation locally in C2's fixtures; never read C1's policy JSON or rows.
   Shared expectation is allowed (`SCORECARD.md:650`); a shared file is not (`preregister.json:55`).

## 5. Affected axes, risks, verification

**Affected axes.** Operability (C2, declared) improves: the availability fact becomes a
demonstrated discriminator rather than a nominal mode. Ordinal stays 9 → 9 (0). Calibration is not
harmed — the witness keeps availability, behavior and conformance separate, consistent with
`:648`/`:688`/`:699` — but no calibration improvement is claimed. Depth, adjacency, coverage and
freshness are untouched: no C1 contract edit, no new source row, no host action.

**Risks.**
1. Post-hoc target creep → witness only; no metric/target/claim change; report as supporting
   control, not a fourth claim.
2. Evaluator-freeze violation → fixtures and expected verdicts frozen before measurement; late
   additions labelled separately and barred from changing the verdict.
3. Separability breach → synthetic fixtures only; C2 must not open `edit-decision-policy.json`.
4. False conformance reading → the witness proves detection on synthetic metadata, not compliance;
   the real audit may remain red (round22 precedent).
5. Legacy regression → no shared-path edit; pinned byte-identical v1 replay.
6. `UNKNOWN` inertness → the witness alone does not fix the real audit; mode credit should require
   the real no-target events to be not-clean, else the opaque case stays permissive.

**Verification duties (L1/main; none executed here).**
- Run the C2 command and record exit, findings and incomplete-seat count.
- Witness: A clean, B `DENY`, C not-clean; legacy v1 replay identical to baseline.
- Mutation: weakened v2 fails B; v1 replay unchanged.
- Read-discipline audit: C1 checker never opens the v2 manifest/events; C2 checker never opens the
  policy JSON; C3 checker exact-paths its reconciliation record and does not enumerate the round23
  build directory.
- Confirm no ordinal, target, claim-text or capability-row change; confirm the receipt still reads
  `executed=none` for seats this scope binds.

## 6. Contradictions stated explicitly

1. Archival axis table (`SCORECARD.md:52`: adjacency 7) versus operative ordinals
   (`preregister.json:100`: adjacency 8). Use the preregister; do not quote `:52` as current.
2. “rough 25/33 vs lane 23/29”: producer and policy are not unambiguously labelled; both are
   recorded under the outside block. C3 must name producer + policy per count.
3. Uniform `S086` evidence across eight heterogeneous decisions; grounding of the three normative
   rows is unverified from this seat's binding.
4. `OPAQUE_PATCH: UNKNOWN` has no stated fail-closed mapping in C2; without an observed not-clean
   outcome the decision is inert.

Reviewed-SHA256: 09af22c52bfbd57f591fe75ab3050ab8ab96d52b2d23060186dcdc8ef7283c70
Predicate: r23-connplanner23
Scope: executed=none
