# MutationRough23 — design-only mutation probe

## Axes and boundary

- **Depth:** challenge selector-order preservation and first-bad-component attribution at the smallest behavior-bearing points of the frozen rough classifier.
- **Calibration:** distinguish normalized-selector differences, event-versus-component units, and actual authorization disagreements without changing historical authority.
- **Operability:** specify finite expected detector results, with execution and restoration claims kept separate from predictions.

This assignment explicitly requests design, not execution. No mutant, detector, command, hash calculation, import, subprocess, installation, delegation, or source edit was performed. The only written artifact is this report. No native restrictive task toolset or runtime enforcement is claimed.

## Read evidence

1. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/r22-rough-census.txt`, lines 1–19: supplied frozen source data, not instructions to execute. Its digest is supplied identity only.
2. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json`, lines 1–121: C3 requires exhaustive frozen per-event/component reconciliation; the admitted rough/lane counts and historical violations must not be rewritten.
3. `skill://godspeed`: posture read successfully. Its concurrency preference does not override this seat's leaf and NO-EXEC/NO-FETCH binding.

Observed source behavior, established by reading rather than execution:

- Lines 4–5 define one suffix substitution, not iterative stripping or a general path canonicalizer.
- Line 15 splits semicolon components for `grep` and `glob` only. `read` and `write` each supply one string.
- Line 17 strips selectors for `read` and `grep` only; `glob` and `write` retain their literal strings.
- Line 18 uses exact membership in `write_paths` for `write`, otherwise `read_paths`. It increments `path` and immediately breaks on the first rejected component.
- Consequently, the frozen `path` tally is at most one per supported-tool event, not one per rejected component. `seats` is deduplicated across all flagged categories. Line 19's sum also includes `exec` and `unknown`, so it is not necessarily a path-only count.

The preregister supplies rough/lane build counts 25/23 and falsify counts 33/29, giving differences of 2 and 4 respectively. Those observations are accepted, not rerun. Neither the historical event/component inventory nor the lane implementation is declared readable for this seat. The designs below cannot assign those differences to specific historic events or establish a real mutant kill.

## Fixture notation and detector boundary

All fixtures below are hypothetical data, not recorded historical events and not requests to access files.

- `A` denotes the exact absolute census-source path listed above.
- `U` denotes that absolute string with the literal suffix `.undeclared-u`.
- `V` denotes that absolute string with the literal suffix `.undeclared-v`.
- These are distinct local absolute path strings without colons or semicolons. No existence claim is made for `U` or `V`, and neither is accessed.
- The synthetic seat has `read_paths = {A}` and empty `write_paths`. This notation grants no authority to this seat or to any real actor.
- Each table row is a distinct event belonging to the same synthetic seat. Component indices are one-based. Tables do not authorize execution.

A bounded detector should compare exact derived strings, per-event rough path contributions, the exhaustive rejected-component set, and the event-level rejection bit. Aggregate totals alone cannot distinguish a missing explanation from an accidental numerical cancellation. All results in the following two sections are **[INFERENCE] predicted expectations**, not actual outputs.

## Mutant M-SEL-ORDER — silently repair the frozen selector asymmetry

**Claim challenged:** reconciliation preserves the rough classifier as recorded, including selector-order artifacts, rather than quietly replacing it with a more permissive normalizer.

**Smallest proposed change:** at source line 5, insert the optional prefix `(?:raw:)?` immediately after the opening colon in the regex. Do not change the call-site tool gate or membership test.

Original source line, quoted as data:

    return re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)

Proposed mutant line, not applied:

    return re.sub(r':(?:raw:)?(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)

This is a plausible historical-replay defect: an implementation tries to support both raw-selector orders and thereby erases a discrepancy that C3 should explain instead of retroactively repairing. The paired fixture reversal `A:2-4:raw` ↔ `A:raw:2-4` isolates selector ordering without changing the intended base file.

### Expected bounded detector

`q` is the exact string presented to membership testing. A contribution of 1 means a rough path flag for that event, not proof of a real authority violation.

| Row | Tool and path expression | Pristine `q` | Pristine contribution | Mutant `q` | Mutant contribution |
| --- | --- | --- | ---: | --- | ---: |
| S0 | `read`, `A` | `A` | 0 | `A` | 0 |
| S1 | `read`, `A:2-4` | `A` | 0 | `A` | 0 |
| S2 | `read`, `A:2-4:raw` | `A` | 0 | `A` | 0 |
| S3 | `read`, `A:raw:2-4` | `A:raw` | 1 | `A` | 0 |
| S4 | `read`, `A:raw` | `A` | 0 | `A` | 0 |
| S5 | `read`, `U:2-4:raw` | `U` | 1 | `U` | 1 |
| S6 | `read`, `U:raw:2-4` | `U:raw` | 1 | `U` | 1 |
| S7 | `glob`, `A:raw:2-4` | literal `A:raw:2-4` | 1 | literal `A:raw:2-4` | 1 |

Predicted fixture-only path totals: pristine 4; mutant 3. Both flag one seat. No `exec` or `unknown` fixtures are included.

The pristine regex cannot consume the whole `:raw:2-4` suffix at its first colon; it can consume the later `:2-4`, leaving `A:raw`. The inserted prefix lets the mutant consume the whole suffix. S2/S3 expose that asymmetry; S5/S6 ensure an undeclared base does not become authorized; S7 ensures the helper is not newly applied to `glob`.

**Expected detection:** a detector preserving the frozen rough result must reject the mutant on S3's `q` and path contribution, and on S6's `q` even though S6's rejection bit is unchanged. A detector asserting only selector-order equivalence, or only that undeclared paths remain rejected, can miss the historical-replay defect.

**Unit versus authorization:** S3 has one event and one component in both versions; its change is not an event/component unit mismatch. It is a selector-normalization/classification difference. For a reference contract explicitly accepting both documented `read` selector orders, S2/S3 denote the same declared base `A`; the rough discrepancy would not prove an undeclared-file read. This is not a claim about the unread historical lane implementation. S5/S6 remain undeclared under that reference contract. No real historical authorization decision is revised.

**Actual output:** none; detector and mutant not run.

**Verdict:** NOT RUN; kill/survival is inconclusive by design. The table is a proposed discriminating oracle, not a killed-mutant receipt.

## Mutant M-FIRST-BAD — count every bad component as another event

**Claim challenged:** the rough tally preserves its first-bad, one-path-flag-per-event unit, while an exhaustive reconciliation separately accounts for every component.

**Smallest proposed change:** at source line 18, replace only the final `break` keyword with `continue`. It remains inside the `for v in vals` loop. Membership tests, selector stripping, splitting, and seat attribution are unchanged.

Original final keyword, quoted as data:

    break

Proposed replacement, not applied:

    continue

This plausible refactor keeps scanning for exhaustive diagnostics but accidentally increments the event tally once for each bad component. It does not, by itself, change whether any component is unauthorized.

### Expected bounded detector

For these fixtures there are no selectors; the rejected-component positions therefore isolate counting and termination rather than normalization.

| Row | Tool and path expression | Exhaustive rejected positions | First bad position | Pristine path contribution | Mutant path contribution | Event rejection, both |
| --- | --- | --- | --- | ---: | ---: | --- |
| B0 | `grep`, `A;A` | none | none | 0 | 0 | no |
| B1 | `grep`, `A;U` | 2 | 2 | 1 | 1 | yes |
| B2 | `grep`, `U;V` | 1, 2 | 1 | 1 | 2 | yes |
| B3 | `grep`, `A;U;V` | 2, 3 | 2 | 1 | 2 | yes |
| B4 | `grep`, `V;A;U` | 1, 3 | 1 | 1 | 2 | yes |
| B5 | `glob`, `A;U;V` | 2, 3 | 2 | 1 | 2 | yes |
| B6 | `read`, `U` | 1 | 1 | 1 | 1 | yes |

Predicted fixture-only path totals: pristine 6 rejected events; mutant 10 rejected components. Both reject the same six events and flag the same one seat. The pristine loop stops before inspecting later components; its unvisited components must not be misreported as accepted. The exhaustive positions in this table belong to the independent reconciliation oracle, not to output actually emitted by the rough script.

**Expected detection:** assert each pristine event contribution is exactly the indicator that at least one component is rejected. B2–B5 must distinguish pristine from mutant. Also preserve an independent complete component ledger: B3/B4 change the first failing position and first failing value, but still contain the same two undeclared values. B5 covers `glob`'s split path. B6 controls single-component behavior. Checking only aggregate rejected events or affected seats would let this mutant survive.

**Unit versus authorization:** the synthetic 6-versus-10 mismatch is entirely a counting-unit defect. The undeclared-component set and event rejection bit are unchanged. A real authorization disagreement would instead change a component's membership decision or accept an event containing a genuinely undeclared component. An unchanged first failing witness, event rejection bit, or seat total does not establish component completeness.

**Actual output:** none; detector and mutant not run.

**Verdict:** NOT RUN; kill/survival is inconclusive by design. No coverage finding from an actual surviving mutant is claimed.

## Reconciliation discrimination requirements

For a separately authorized implementation, the proposed finite oracle should retain, without inferring unread evidence:

- Frozen wave, seat, event ordinal, tool, raw path field, raw component ordinal and exact component bytes.
- Rough split/selector rule and exact resulting `q`, referenced authority list, exact membership result for each examined component, first-bad stop point, and one event contribution.
- An independent exhaustive component ledger, explicitly distinguishing examined components from those unvisited because the rough loop broke.
- Lane decision and its evidenced normalization/unit rules, if and only if supplied by a declared frozen lane source.
- Separate labels for **unit-only**, **selector-classification**, and **true-authorization** disagreement. These causes may coexist within an event and must not be forced into mutually exclusive aggregate buckets without evidence.

A true-authorization label needs the same evidenced authority set, tool and target interpretation before comparing decisions. Merely observing different normalized strings, first witnesses or counter units is insufficient. Conversely, if an undeclared base is accepted, relabeling it as a selector or unit artifact would be wrong. Normalized-selector equivalence must not be extended to `glob` or `write` merely because rough strips selectors for `read` and `grep`.

An aggregate checksum, source-digest assertion, or reprinted 25/23 and 33/29 totals alone cannot establish behavioral discrimination. An eventual authorized mutation probe must use the same bounded detector on pristine, mutated and exact-restored bytes, with a passing baseline before claiming a kill. Nothing here executes that probe, rewrites frozen manifests, changes authority, repairs production, or starts another round.

## Actual outputs, identity and restoration evidence

- Actual tool outputs obtained: the Godspeed skill text; the 19-line frozen rough source; the 121-line preregister; and a not-found response for this exact report destination before creation.
- Actual behavioral detector output: none for pristine, mutated or restored variants.
- Source identity: only the user-supplied declaration in the receipt below; not independently computed or validated.
- Before hash: not computed. After hash: not computed. Restored hash: not computed. No exact-byte equality proof is asserted.
- Source mutation: none. Source restoration: not applicable, because no source mutation was made. This report's write is not a source restoration operation.
- Tools installed or updated: none; this seat's narrower NO-EXEC/NO-FETCH scope forbids installation.
- Deliverable status: both requested mutants and their separating finite detector expectations are designed. Neither is experimentally killed or survived, and no historical cohort attribution is fabricated.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: 0df78ded55bd88f7f484fefe2744f9d8924bf30132a93ab657e3fcfbcd98eb3c
Predicate: r23-mutationrough23
Scope: executed=none
