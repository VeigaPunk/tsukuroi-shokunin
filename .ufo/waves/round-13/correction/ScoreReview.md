# ScoreReview — tsukuroi round 13 correction (depth score delta)

Seat: `TsukuroiR13.ScoreReview` (reviewer, leaf, read-only). Repo: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Snapshot: 2026-10-20, working tree not pinned to a commit (other seats may be editing). Every pointer below is a dated observation.
Installs / updates: none. Checks run: none (no selftest, census, jq or build). Probes were read-only file reads and greps.

## 1. Outcome

- **Lowest non-retired axis: depth = 8**, tied with adjacency = 8. Retired: none. Not every owned axis is >= 9 (saturation line 9, SCORECARD.md:176-178), so the stagnation nudge does not apply.
- **Honest delta for the sole depth claim (C1 correction): 8 -> 8 (0 ordinal).** The correction removes a false universal that the outside closure scored as depth **harmed**. Removing a harm is not an ordinal gain above 8.
- **Depth verdict status:** remains "harmed as delivered" (round-12 C2) until (a) the correction lands and (b) a non-author verifier passes it. An author-side seat cannot clear an outside verdict (lesson `corpus/lessons/round-12-verifier-spotcheck.md:14-19`, `:214`).
- **No +1 (8 -> 9).** The round-12 review conditions for one step are still unmet (section 5). The correction does not address them.

## 2. Authoritative scores read

| Axis | Score | Source (observed) |
|---|---|---|
| depth | 8 | SCORECARD.md:45-52 table (r4 change); round-12 section SCORECARD.md:243-283: "Unworked ordinal axes stay depth 8 (worked but not rescored)"; C2 row `8 -> 8 (0)`. |
| adjacency | 8 | Post-review claim A, SCORECARD.md:207-240 (7 -> 8). |
| coverage | 9 | Post-review claim B, SCORECARD.md:207-240 (8 -> 9). |
| freshness | 9 | Post-review claim C, SCORECARD.md:207-240 (8 -> 9). |
| operability | 9 | Final row r11; round-12 C1 `9 -> 9`. |
| calibration | 9 | Final row r10. |

**Stale conflict, not reconciled:** SCORECARD.md:45-52 still reads adjacency 7, coverage 8, freshness 8. The depth row still cites 24 notes, census 2402 `wc -l`, 80 selftest cases and SKILL 1631/55. Those are size or count evidence that the round-12 reviewer rejected as depth counters (`.ufo/waves/round-12/resumed/ScoreReviewR.md` section 7). L1 should add a dated supersession append. Do not rewrite the table.

## 3. Outside rejection (what the delta must price)

- Closure status: `rejected-harmed`, `admitted: false` (lesson :14). Lesson per-axis verdict: **depth: harmed** (:214). Learning trends: expansion, quality and discernment all harmed (:222-234).
- Lesson :175 and :176 mark C2 as "disagree as delivered"; "correction is still owed" (:175).
- Routed defect 1 (:237-242): narrow the exhaustive read-only-unit sentence in the MD current-host explanation, R13 and the JSON B2 `limit`. Keep the valid ProtectSystem comparison. Keep the alternate path-view mechanisms. Then seek fresh non-author verification.
- **Conflict:** SCORECARD round-12 row says C2 `improved, author-verified` (SCORECARD.md around :255). The outside verdict is `harmed`. The scorecard row is stale against it. L1 must append a supersession notice; the row must not be edited in place.

## 4. Scope of the false universal (observed in active bytes)

Three occurrences the correction must narrow:

1. `corpus/knowledge/root-dac-decision-r12.md:53` — "only `strict` (or a `ReadOnlyPaths=` entry covering `/`) would make `/` read-only through the unit (S028)."
2. `corpus/knowledge/root-dac-decision-r12.md:86` — R13: "Only `strict` or a `ReadOnlyPaths=` entry covering `/` could produce a B2-family `EROFS` for `/` through the unit."
3. `corpus/knowledge/root-dac-decision-r12.json` B2 `limit` (line 87): "so only strict or a `ReadOnlyPaths=` entry can make `/` read-only through the unit."

Internal contradiction in the same record: B2 `expected_signal` (json line 82) and B2 `commands` (json :79) already name `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=` and `RootImage=`. The S028 sentence supports only the narrower claim: among `ProtectSystem=` values, `full` does not cover `/` and `strict` covers the hierarchy (S028 § ProtectSystem=).

**Keep, not part of the defect:** `root-dac-decision-r12.md:42` ("while only `strict` mounts the entire hierarchy read-only") is scoped to ProtectSystem values. `json` B2 `interpretation` (line 75) is correct.

Bounded sweep for other mentions (read-only grep, this review): pattern `root-dac-decision-r12|read-only unit|through the unit` over `SKILL.md`, `SCORECARD.md`, `LOG.md` returns only `SKILL.md:1695` (source-list pointer, no exclusive wording) and `LOG.md:437-440` (no exclusive wording). Pattern `only (strict|ProtectSystem=strict)|ReadOnlyPaths= entry covering` over the matrix MD/JSON, `SKILL.md` and `snapper-eacces-mechanism.md` returns only the three hits above and the `:42` scoped hit.

## 5. Score-delta derivation

Scale: no count-to-ordinal-score rubric exists (SCORECARD round-12 header; AXES.md is not present at the repo root, so its clauses are not re-read here). A round can only add one step when the claim's specific gaps close.

Gaps that a +1 would need, all still open:

- **Falsifiers 0/4.** `grep -c falsifier corpus/knowledge/root-dac-decision-r12.json` → no matches. Each branch has keys `discriminator, evidence, id, interpretation, limit, source_ids` only.
- **Procedure step 1 unguarded.** `decision_procedure[1]` (json line 171) reads "present -> B4-family indicator" with no errno precondition. Target-present with EACCES is covered by no scenario. Ordinary-mkdir EEXIST-before-EACCES ordering (`error-order-smoke.json`) must not be extrapolated to the Btrfs ioctl (matrix R10).
- **SKILL parity.** `SKILL.md:1683-1687` carries root-arm rows, not the four B1-B4 branches (prior observation, `ScoreReviewR.md` section 5c; not re-counted here).
- **Non-author replay** not performed.

The correction alone closes none of these. Therefore:

| Outcome | Depth score | Verdict effect |
|---|---|---|
| Correction lands, non-author verification passes | 8 -> 8 | Harm removed; outside depth verdict may move `harmed -> restored` at L1's discretion. No ordinal gain. |
| Correction lands, no verification | 8 | Stays `harmed as delivered`; C2 not admissible. |
| Correction incomplete (any of the 3 sites in section 4 remains) | 8 | Stays `harmed`. |
| +1 to 9 | Not supported by this round | Requires falsifier 4/4, step-1 errno guard, SKILL parity and non-author replay. |

## 6. Recommended SCORECARD wording (for L1, not written here)

> depth 8 (unchanged). Round-13 correction narrows the round-12 exclusive read-only-unit statement in `root-dac-decision-r12.{md,json}`; it removes the defect the outside closure scored as harmed and adds no ordinal point. Outside verdict stands until non-author re-verification. Falsifier coverage (0/4) and procedure step-1 guard remain open.

Pin a commit before any SCORECARD row is written.

## 7. Checks owed to L1 after integration (not run here)

- Narrow check: the pattern in section 4 returns 0 hits on the active MD/JSON after the correction, and at least 1 hit on the historical bytes (`git show b76b5c3:corpus/knowledge/root-dac-decision-r12.json`). The correction must preserve the historical file; the active file gets a superseding entry or a dated erratum block.
- `jq '[.branches[]|select(has("falsifier"))]|length'` → must be 4 before any depth +1.
- Re-check that freshness and coverage rows are untouched.

## 8. Residual risk and gaps

- The working tree is mutating; this snapshot is not a pinned score basis.
- Counts and line numbers come from reads and greps, not from jq or census runs.
- The `discernment` conflict between `corpus/lessons/round-1-verifier-spotcheck.md:17` and `SCORECARD.md` remains outside this seat's axis; not scored here.
- The outside verifier's remark that `omarchybot` comments were called "maintainer-side" (lesson :183-186) is a source-attribution item, not a depth input.
