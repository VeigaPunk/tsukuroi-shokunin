# Round 77 — finite journald arithmetic, not a renamed minimum

Base `06f1bbbb803790b35358d277bb7807b82a9fab99`; frozen declaration
`eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5`. Claims: C1 depth (lowest tied,
8), six exact worked input/output vectors; C2 freshness (9), three full
correction blocks in the round-76 lesson. No new coverage or ordinal uplift
is claimed. The frozen predicates and controls live in
`.ufo/waves/round-77/before/{expected.json,controls.json}`.

## Gate

Sources opened by L1 on 2026-11-04, before freeze; source snapshots have
full SHA256SUMS in `.ufo/waves/round-77/before/src/`. Source lines are
upstream v262, not verified Arch-build line numbers. Quotes below are
located in those exact bytes; whitespace indentation is omitted.

| Row/candidate | URL and location | Located quote (at most 25 words) | Decision / reason / flip |
|---|---|---|---|
| S324 | https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro.h :325 | `UNIQ_T(A, aq) > UNIQ_T(B, bq) ? UNIQ_T(A, aq) - UNIQ_T(B, bq) : 0; \` | admit, tier A/code, mined: actual LESS_BY operation; CLAMP at :337-350 separately read |
| S325 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c :168 | `avail = LESS_BY(vfs_avail, metrics->keep_free);` | admit, tier A/code, mined; supersedes S320's still-false minimum wording; :170-171 supply limit and available |
| S326 | https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro-fundamental.h | no payload quote: HTTP 404 | reject, unreachable guessed filename, not fabrication; flip: reachable version-pinned relevant payload and located quote |
| Original minimum formula | pinned manager :168 and macro :325 | same expressions above | reject: free=1000 and keep_free=100 give 900, not minimum 100; flip: source using minimum |
| Staged corpus adoption | read-only `merge/tsukuroi/` package | not an admitted source | reject while operator hold remains; flip: explicit release plus per-entry source gates |

Spot-check result: outside round-77 admit+reject check is **pending**. Wave
seats belong to this lane and cannot provide the outside discernment check.
The previous outside check is `round-76-verifier-spotcheck.md` section 3:
agrees with substantive rejects, disagrees with the missing Gate reject row.
Round-76 Gate now has appended reject and outside-result records; the rejected
round-76 declaration remains rejected.

Registry changes: S324/S325/S326 are new, two mined and one rejected; no
existing row's status, recheck or used-by changes. S320 is retained as the
falsified historical row and explicitly superseded by S325. Tier A for S326
classifies the primary-code scope, not unavailable contents as verified.
The actual GitHub v262 tree, opened this round, identifies macro.h rather than
the failed guessed filename. No package row is appended.

## Mistakes

| Class / id | Evidence | Captured-by | Fix shown able to fail |
|---|---|---|---|
| stale-premise — R77-MINIMUM | round-76 closure :59-76 and S320 teaches | QUALITY 106 and 108 | S325 supersedes S320; six explicit examples deepen JD3. The same frozen C1 command scores the minimum-substitution control 0/6, exit 1 (`before/controls.json`); no post-data instrument change |
| number-drift — R77-COUNTS | round-76 lesson original 322 and 114 figures; closure section 6 | QUALITY 102/104/105 and outside closure | full revision-bound corrective blocks; same frozen C2 command at base scores 0/3 exit 1; the target is the three corrections, not a new counter label |
| scope — R77-GATE-SHAPE | round-76 closure :162-165 | LEARNING outside admit+reject rule | appended reject row and spot-check-result record; no invented approval and no retroactive admission |

No new QUALITY criterion is necessary: 106 already requires literal source
checks before freeze, and 108 already requires correction propagation. This
round applies them rather than creating a competing rule. Source arithmetic
was opened before declaration, with the exact operation copied next to the
claim; the six tuples deliberately avoid overflow and inverted bounds.

## Correction propagation map

Sweep: `grep` pattern `smaller of free space and|min\(free, keep_free\)`
over SCORECARD.md, LOG.md, SKILL.md, PROVINCE.md and corpus/.

- `corpus/SOURCES.md` S320 (:331 at base): standing as falsified record;
  new S325 explicitly supersedes it. No forbidden teaches edit.
- `SCORECARD.md:6307,6325-6335,6346,6372-6374` at base: historical declaration
  and errata. Round-77 appended correction adopts the outside rejection,
  not the earlier claim of verification on a lexical predicate.
- `corpus/knowledge/journald-retention-plane-r76.md:13,26`: already corrected
  arithmetic; append links to the six examples and source-row supersession.
- `SKILL.md:6066`: already correct saturated subtraction; new worked-example
  pointer deepens it without replacing the health verdict or host limits.
- `corpus/lessons/round-76-verifier-spotcheck.md:10,69`: outside historical
  evidence, never edited. LOG.md and PROVINCE.md had no matching false
  arithmetic sentence in this bounded sweep.

## Sources, frontier and assimilation

Assimilation: **none**. `before/collisions.json` records the full registry
and staged id sets at base: 323 registry ids, 147 staged ids, 124 intersections.
The parser accepts 0–3 leading spaces; the independent revision seat checks
an indented collision control. S324–S326 are this round's own source curation,
not package adoption. No id is renumbered. The open round-75 id-drift hold
and promotion hold remain unanswered; no new operator permission is inferred.

`considerthese/2026-10-26.md` was opened; the correction-propagation and
patch-offset proposals already have QUALITY 108 and 103. No still-unimplemented
proposal is claimed as newly mined. The companion examples deepen existing
JD3 rather than moving a frontier row into Core. Expansion is unchanged.

## Protocol-load note

The fleet protocol, mission, axes, corpus and learning contracts and rejection
history were read before freeze. Canonical upstream protocol deployment deltas
were read after freeze; their report/trend and source-provenance requirements
are honored here. This load-order defect is disclosed, not used to rewrite a
frozen predicate. No tool was installed by L1.

## Wave settlement and integration

WAVE-DONE received from the orchestrator; `w1-results.json` contains twelve
nonempty seat outputs, no dead seat. One v1 wave: scout 1, executors 3,
scribes 3, connector 1, reviewers 2, critic 1, mutation-tester 1. Attack
share 4/12, connector count 1; L1 holds planner, residual 0.

- ReviewArithmetic holds A1–A6 and the companion explanation; A6 is
  hypothetical, not startup reachability. The integrated explanation keeps
  those values/interpretations; provenance-first metadata and actual
  companion filename replace draft packaging.
- ExecMacro compiled the full pinned header, not a reimplementation:
  GCC 16.2.1 20260810; initial compile lacked RELATIVE_SOURCE_PATH and exited
  1, then the build-metadata define was supplied and compile/program each
  exited 0. Six actual macro output triples match.
- ExecHost executed four read-only triage commands, each exit 0. Installed
  systemd 262.1-1, aggregate usage 185.4M, configured persistent/runtime
  maxima 256M/64M. Hypothetical used=128MiB is expressly not measured
  manager usage; no service/config/package action was performed.
- ExecRevision confirms 323 rows at the historical measured commit and
  base, and matches all 147 staged ids / 124 intersections, including an
  indented-row control. The specified package is a read-only working-tree
  input with SHA256 7914d3b93cea2015c00091d7db28ca2acd289d5097cb513ad1176dc0d7148406;
  its committed shokuknow HEAD instead has 107/107. The frozen correction
  does not claim the working-tree package equals that HEAD.
- ReviewFreshness reads each correction as substantive, confirms independent
  historical facts, and observes rendered append-only reject/result records.
- ScoutSources and ScribeSources independently reopen both source bodies
  and reproduce the pinned hashes; the guessed path is HTTP 404.
- ScribeLesson's candidate agrees with the retained Gate/Mistakes and
  exact C2 repairs. ConnectorScope confirms deeper held ground, unchanged
  mori/mado boundaries and five already-implemented consideration proposals.
- MutationFinite's actual-CLI isolated battery kills 76/76 specified
  data/source defects, with clean pristine/restored controls; receipts and
  replay driver live in its seat directory.
- CriticFreeze demonstrates four semantic acceptance constructions:
  answer-copy/source-token-only and false companion prose for C1; commented
  or explicitly disowned exact correction strings for C2. These are
  in-memory evaluate observations with derived exit values, not CLI runs.
  The counter cannot prove arbitrary prose truth, registry resolution,
  understanding or rendered adoption. Actual integrated prose/source rows
  and adoption context were reviewed separately; no frozen instrument or
  predicate was changed to conceal those limitations.

No tool was installed/updated by any seat. Each seat reports scratch absent
or removed; L1 removes its remaining round root after landing. Some validator
Report trailers requested a sibling `.md` outside the narrower seat directory;
most seats honored the narrower explicit scope. Existing sibling-level
trailers are still inside this round's lane evidence, not fleet misroots.

### Additional mistake and teaching resolution

Scope — R77-STAGED-REVISION: a collision claim over the specified package's
working bytes must not be called committed-upstream evidence. Captured-by
QUALITY 102/104. ExecRevision's actual comparison can fail: committed
package 107/107 versus specified input 147/124. Fix is the digest and input
class above, not editing the frozen correction or quarantined source repo.

The pre-existing QUALITY 81 requirement for a depth counter's reviewer
binding is not implemented in this finite object counter: review is
separate committed evidence, not a seat-vote conjunct. No author-side
mechanical PASS is presented as fulfillment of that stronger criterion.
This is an instrument conformance limitation for outside closure to judge,
not an assertion of source understanding and not a predicate amendment.
