# Crit23Quality — round 23 attempt 1 quality-trend critic

Seat: Crit23Quality (UFO-FSD critic, leaf). NO-EXEC, NO-FETCH. Source-only review of the bound files:
`preregister.json`, `sources/godspeed-directive.txt` (read in place of `skill://godspeed`, which could not be resolved by this seat's tools), `sources/r22-closure.json`, `sources/structured-edit-observations.json`. The build report path did not exist before this write. The preregister digest is taken as the supplied identity and was not computed.

## Verdict on the quality trend

**Quality: unchanged.** The outside round-22 verdict carries forward, and nothing in the round-23 preregistration earns a `quality: improved` trend.

The outside rule, from `r22-closure.json` `notes`: "Quality trend unchanged: in-round gate hardening and registry repair concern new material; no prior entry superseded or re-verified." So a quality improvement needs a genuine recheck or supersession of a prior entry. New instruments do not count.

Every round-23 claim is new material by its own declared scope:

| Claim | Declared scope (preregister) | Prior entry rechecked or superseded? |
|---|---|---|
| C1 depth | "new document contract, not eight repaired runtime behaviors" | No |
| C2 operability | "New explicit schema-v2 audit authority … legacy schema-v1 policy and historical reds unchanged" | No, explicitly excluded |
| C3 calibration | "does not relabel old violations or retry historic checks for confirmation" | No, explicitly excluded |

Corroborating fields: `"retired": []`, `"ordinal_delta": 0`, `limits` includes "No historical manifest/report rewrite or retrospective authorization", and `outside_round22.scope` treats the outside observations as ground truth that round 23 "explains … rather than rerunning closure merely to confirm them". `sources_opened` S085 and S086 are both marked prospective additions, not replacements.

## Counterexample 1: C3 claimed as a "recheck" of round 22

- **Falsifier.** The round-23 report or closure argues that `quality: improved` because C3 "re-verifies" or "makes decisive" the round-22 path census. The closure text describes that census as "approximate own path-binding census 25/33 vs checker23/29 (selector-normalization differences, not decisive)".
- **Why it fails.**
  - That census belongs to the outside verifier, CloseKaidoku22, inside the MANIFEST entry. It is not a lane entry that the lane can supersede.
  - The preregister freezes it as `path_counts_as_reported` ground truth.
  - C3 forbids its own relabel or retry.
  - Explaining a unit difference adds a reconciliation record. It is not a re-verification of a prior lane entry. Counting it as improved would be false provenance: a new artifact presented as a recheck.
- **Impacted axes and trend.** Quality trend; calibration (C3) if the claim is inflated.
- **Smallest correction.** In the round-23 report and lesson, state `quality: unchanged`. Describe C3 as "new reconciliation of frozen r22 counts; no prior entry superseded".

## Counterexample 2: C2 v2 authority used retroactively on round-22 edit findings

- **Falsifier.** Round 22 recorded edit-tool use as violations: "edit16/17=unknown-tool16/17", plus "other findings are edit-tool use". The four observations in `structured-edit-observations.json` are all round-22 `edit` calls on report paths: one from CritRuntime and three from OraclePathArtifact. Suppose the round-23 report re-scores them under the `DECLARED_EDIT → ALLOW` row, or presents them as "now explained or allowed". That is a quality-improved claim built on retrospective authorization.
- **Why it fails.**
  - Round-22 bindings predate schema v2, so no target was "predeclared for edit and for both read and write".
  - The `limits` field forbids retrospective authorization, and C2's scope keeps the historical reds unchanged.
- **Impacted axes and trend.** Quality trend (identity change of old findings); operability (C2) if detections shrink.
- **Smallest correction.**
  - Use the observations only as sources for the C1 rows: S086, "observed structured edit request keys".
  - Keep the round-22 `unknown-tool` counts byte-identical in every round-23 artifact. Any round-23 table that touches them labels them historical and unchanged.

## Counterexample 3: two selector-normalization authorities (quality hazard for later rounds)

- **Falsifier.** In S086, CritRuntime's recorded adapter steps read `…/CritRuntime.md:raw` and then write `…/CritRuntime.md`. Two preregistered rows make the outcome depend on normalization:
  - `EDIT_TRAVERSAL` ("No dot-segment or alternate spelling expands the target list").
  - `EXPANSION` (`CHECK_EACH`).

  Under exact matching, the `:raw` read falls outside the binding, and `WRITE_ONLY_EDIT` ("Edit also needs its explicit target read authority") could fire. Under normalization, it is in scope. Round 22 already blamed its 25/33 versus 23/29 gap on "selector-normalization differences". C3 is barred from reading C1/C2 production content (`separability`). So C2 and C3 can each define their own normalization of the same selector and disagree. That gives two authorities for one identity question.
- **Impacted axes.** Operability (C2), calibration (C3), and later quality, because a future round "reconciling" the two would look like a supersession.
- **Smallest correction.** C2's documentation must state the `:raw` treatment explicitly: either the exact string or a named suffix rule. C3's reconciliation record must state its own rule independently, citing only frozen round-22 evidence. Neither may import the other, because separability holds. The round-23 report notes that the two rules are separately owned and not yet unified. No unification is claimed this round, and no round 24 is started.

## Strongest counterexample to my own verdict (tested)

Could anything in round 23 qualify as a genuine prior-entry recheck? Possible candidates:
- `retired`: empty.
- `capability_acquisition`: false.
- `exploratory`: false.
- A superseded SOURCES or LESSON row: the only sources are prospective S085 and S086.
- The re-execution of a historic check: forbidden by C3 and by `outside_round22.scope`.

None qualifies. The verdict holds under local evidence.

## Fixable defect versus tradeoff for the judge

- Counterexamples 1 and 2 are **fixable wording and labelling defects**. They only bite if the report overclaims. The canonical judge should reject any round-23 `quality: improved` that lacks all three of the following:
  1. A named prior entry, with its round, file and row.
  2. A recheck executed against current bytes.
  3. An explicit supersedes pointer.

  None of these is preregistered, so the judge must reject the claim.
- Counterexample 3 is a **tradeoff**. Separability buys independence between C2 and C3 at the cost of duplicate normalization ownership. It is acceptable for round 23 if it is disclosed, and it is not a trend gain.

## Limits

This is a source-only review. I executed no commands and fetched nothing. I did not validate the digest, read any production or lane file, or check whether the planned report wording exists yet. This seat performed no installs.

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23-crit23quality
Scope: executed=none
