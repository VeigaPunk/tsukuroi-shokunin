# FxFrontier — round23 frontier classification (falsify)

Attacked object: the frontier classification of round23 (`held-ground instrument
depth` versus `frontier expansion`), not the internal correctness of the C1/C2/C3
gate code. Evidence base is the declared source set only; no command was executed.

## Verdict

**Held-ground instrument depth, not frontier expansion.** The round moves three
instrument metrics (C1 `validated_edit_decisions` 0→8, C2 `structured_edit_mode`
0→1, C3 `unexplained_cohorts` 2→0) while declaring **zero ordinal movement**
(`ordinal_delta: 0`, depth/adjacency 8, coverage/operability/freshness/calibration
9) and **no capability acquisition**. Expansion is unchanged; quality is unchanged
(no prior entry superseded or reverified); discernment has posture evidence but no
independent in-lane measurement. The round does not claim otherwise — this is a
consistent, modest self-classification, not a concealed expansion claim.

## 1. Axes named (godspeed)

- Trend axes: **expansion**, **quality**, **discernment** (r22 closure vocabulary).
- Instrument axes actually claimed: **depth** (C1), **operability** (C2),
  **calibration** (C3).
- Move filter: any move that improves an axis and harms none. Round23's only such
  moves are in-level instruments; none is an expansion move.

## 2. Observed facts (anchors are keys or observed lines)

| Fact | Anchor | Value |
|---|---|---|
| Baseline | `preregister.json` `baseline` | `ae01e50f582016384e620022be38bf5367000e2e` |
| Claim axes | `preregister.json` `claims` | C1 depth 0→8; C2 operability 0→1; C3 calibration 2→0 |
| Ordinals | `preregister.json` `ordinals`, `ordinal_delta` | depth 8, adjacency 8, coverage 9, operability 9, freshness 9, calibration 9; delta **0** |
| Capability posture | `preregister.json:107-109` | `retired: []`, `capability_acquisition: false`, `exploratory: false` |
| Declared limits | `preregister.json:110-115` | no native per-seat restrictive interface; no runtime prevention/effects/recorder completeness; no historical rewrite; no round24 |
| Outside r22 trends | `r22-closure.json:24-26` | expansion unchanged; quality unchanged; discernment improved |
| Outside capability rows | `r22-closure.json:28,32,33` | `capabilities_added: []`, `promotions: []`, `minted: []` |
| Quality rationale | `r22-closure.json` `notes` | "no prior entry superseded or re-verified" |
| Rejections | `lessons/round-23.md:12-15` | native prevention; hardening⇒quality; rough−lane⇒6 missing unsafe events; retroactive v2 |
| Quality rule | `QUALITY.md:97` (criterion 49) | instrument existence/fixture growth/in-round hardening is not `quality: improved`; name the prior entry |
| Edit rule | `QUALITY.md:98` (criterion 50) | v2 authority prospective and explicit; no native-enforcement claim |
| Ledger rule | `QUALITY.md:99` (criterion 51) | units/identities, not totals; net difference ≠ missing unsafe events |
| Admission bar status | `QUALITY.md:1` | "Admission bar (probation draft)" |
| Mutation record | `l1-mutation.json` `author`, `results`, `killed/total` | author-side, "not an outside verifier"; 27/27 killed; 10 reconciliation + 7 edit-contract + 10 seat-bindings |
| Lane independence gap | `lessons/round-23.md:42` | outside r22 verdict is inherited; "No verifier spot-check file exists inside this lane" |

Derived observation: every claimed metric delta sits **inside an unchanged
ordinal**. The v2 schema is the only candidate for lateral movement — it extends
v1 request-scope auditing to adapter edit targets — but it audited a surface the
lane already reviewed (tool calls), remains post-hoc metadata, and is filed under
operability at level 9. That is instrument coverage, not a new frontier.

## 3. Attacked claim, falsifier, bounded search

**Attacked claim (frontier):** round23 holds ground as instrument depth; it expands
no frontier and its three metric deltas are in-level instrumentation at constant
ordinals.

**Falsifier set (any one refutes):**

- F1: `ordinal_delta` > 0, or any ordinal above the prior level.
- F2: non-empty `capabilities_added`/`promotions`/`minted`, or `capability_acquisition: true`.
- F3: a new external domain — host/system probe, upstream source fetch, new artifact class.
- F4: prose claiming native enforcement, runtime prevention, or effects containment.
- F5: a new capability filed on the expansion axis.

**Bounded search (read-only, declared paths only, 2026-10-21):** full reads of
`preregister.json`, `lessons/round-23.md`, `r22-closure.json`, `l1-mutation.json`,
`QUALITY.md`; grep for `expansion|frontier|capabilit|ordinal_delta|promotions|minted|retired|exploratory`
over the same five paths. Result: **no F1–F5 hit.** The only `expansion` values are
`"unchanged"`; the sole other occurrence is QUALITY37's shell-word "expansion"
(unrelated mechanism). No `frontier` token appears in the bound artifacts. Capability
rows are empty; enforcement is explicitly denied in `preregister.json:111-112` and
`lessons/round-23.md` § Mechanics and limits. The claim is **not falsified** within this bound.

**Second attempt (quality):** falsifier = a named prior weaker/stale entry
superseded or reverified with actual evidence. Search `supersed|reverif|prior weaker|stale entry`
over `preregister.json`, `r22-closure.json`, `lessons/round-23.md`, `QUALITY.md`.
Hits are only: r22's *trend label* superseded by the outside verifier (not a corpus
entry), criterion 49's rule text, and unrelated historical supersessions in criteria
17/18/20/26. No prior knowledge entry was reverified by r23. Under criterion 49's
own test, **quality is unchanged**; the round asserts no quality gain.

**Third attempt (discernment):** falsifier = independent non-author measurement of
r23 discrimination. `l1-mutation.json` states author-side/authorship explicitly and
`lessons/round-23.md:42` records the absence of an in-lane verifier spot-check. The
four rejections at `lessons/round-23.md:12-15` and the accepted r22 quality correction
are real posture evidence, but they are prospective policy and self-adjudication, so
discernment **improvement is unmeasured**, not established.

## 4. What the round has and lacks

**Has**

- Depth evidence: three fail-capable instruments at declared targets; 8 decision
  rows; v2 schema; reconciliation ledger; 27 author-side mutants killed (10/7/10).
- Discernment posture: explicit refusals of native prevention, hardening⇒quality,
  totals-as-missing-events, and retroactive authority; accepted outside correction
  without rewriting r22 (`lessons/round-23.md:30,42`).
- Scope discipline: separability statement, prospective v2, limits denying
  enforcement and round24.
- Corpus-shape evidence: three new admission criteria added to a bar that is itself
  labeled "probation draft".

**Lacks**

- Expansion: no capability row, no promotion/mint, no ordinal movement, no
  exploratory slice, no external source class (S085/S086 are lane-internal
  artifacts) — [INFERENCE] from the declared source descriptions, since the
  snapshots themselves are not in this binding.
- Quality: no named prior weaker/stale entry superseded or reverified; new
  instruments and new criteria are "new material" by criterion 49 and cannot count.
- Discernment measurement: no non-author adjudication of r23; the mutation suite was
  authored and selected by the same side that wrote the selftests (QUALITY28/41
  independence concern), so killed mutants show fail-capability, not independent
  discrimination.
- Realized outcomes in this seat's evidence: gate exit codes and the
  `path-reconciliation.json` contents are not verifiable here (NO-EXEC; those paths
  are outside this binding). Declared targets are not confirmed achieved.

## 5. Smallest in-scope remedy

No production repair follows from an unfalsified claim. The smallest in-scope remedy
is a **label binding**, not a code change:

1. Carry the closure verdict as expansion **unchanged**, quality **unchanged**,
   discernment **posture-only / unmeasured** unless a non-author adjudication lands.
   Do not inherit r22's `discernment: improved` (`r22-closure.json:26`) as if it were
   r23's own measurement.
2. Report the three metric deltas together with `ordinal_delta: 0` and the empty
   capability rows, so 0→8, 0→1, 2→0 read as in-level instrumentation.
3. If a later closure credits expansion or quality to r23, F1–F5 and QUALITY49 are
   the falsifiers; the credit fails on the missing named superseded/reverified entry.

This seat makes no production edit and issues no command (NO-EXEC/NO-FETCH).

## 6. Unknowns and limits

- Realized C1/C2/C3 exit codes and ledger arithmetic: **[unknown]** — the tools and
  `.ufo/waves/round-23/path-reconciliation.json` are not in this seat's declared
  read set; running them is forbidden here.
- Semantic completeness of the 27 mutants: **[unknown]** — author-side set; three
  survivors were fixed before recording (`l1-mutation.json`), which is disclosed but
  not independent.
- Whether the six `:raw:N-M` rough-only events are the complete delta: **[unknown]**
  in this binding; declared by `lessons/round-23.md` R23-RAW-ORDER and
  independently located by two wave-1 seats, but the ledger itself is unread here.
- Digest `99d70d94…` is accepted as the supplied declaration; it was not recomputed.

Reviewed-SHA256: 99d70d94f1eecebfbf06088d39df0f378c9ce79dac4f6f6d6a4f55f8ee967043
Predicate: r23f-fxfrontier
Scope: executed=none
