# Crit23fSeparability — round23 falsify, causal separability of C1/C2/C3

Seat: TsukuroiR23-2.Crit23fSeparability-2 (critic, leaf). NO-EXEC, NO-FETCH. I opened only the declared files: the preregister, the godspeed directive copy (skill://godspeed is not supported in this harness), the round-23 lesson, r22-closure.json, path-reconciliation-r23.md and structured-edit-r23.md. The report path did not exist before this write. No tool was installed or updated. I did not read the gate code (tools/check-edit-contract.py, check-seat-bindings.py, check-path-reconciliation.py), the ledgers, bindings, events, frozen inputs or S086, because none of them is in my read binding. So any finding that depends on gate code is a bounded inference, labelled [INFERENCE], and comes with a concrete falsifier the canonical judge can run.

## Axes attacked

- Separability (preregister `separability`): each gate verifies at `<REV>` without reading another claim's new production content.
- Duplicate authority: one normative rule is defined in two claims, with no gate checking that the two agree.
- Provenance: each claim's source attribution covers what its gate actually consumes.

## Verdict summary

| Claim | Attack | Result | Class |
|---|---|---|---|
| C3 | Is the "canonical literal v1 authority" recomputation executed by C2's modified code? | Unresolved within my bounds; this is the strongest counterexample. | Possible separability defect; fixable |
| C1 versus C2 | The same edit-authority rule is defined twice | Confirmed in the documents. No declared gate checks that the two copies agree. | Duplicate authority; a tradeoff, not a separability break |
| C2 | Source grounding | C2 depends on S086's observed argument-key shapes, but the lesson attributes S086 to C1 only | Provenance gap; fixable |
| C2 | Event corpus is the build wave that produced C1/C3 | Metadata only, and the metric is binary mode availability | No falsifier found |
| C1 | Does the gate read C2 or C3 content? | No falsifier found in the documents; the gate code was not readable | Bounded clean |
| Frontier | Arithmetic and identity in C3 | Consistent: 376+2=378, 991+4=995, 25−23=2−0, 33−29=4−0 | No falsifier found |

## F1 — C3 may execute C2's landed v1 selector code (attacked claim: C3; also the frontier `separability` statement)

**Counterexample.** path-reconciliation-r23.md says every event "was classified twice … once by canonical literal v1 authority". It requires "canonical must equal retained" and relies on "the canonical selector grammar accepts `raw`/`img`/`conflicts` and range tokens in any order". The pinned inputs it lists are the event, binding and audit bytes and the rough source text. It does not list the canonical classifier code. C2 changes the binding auditor (check-seat-bindings.py) at `<REV>` to add schema-v2 `edit_paths`. Suppose check-path-reconciliation.py imports or shells out to that module's v1 normalizer [INFERENCE: the natural implementation, because the lane already owns one canonical normalizer]. Then C3's verdict at `<REV>` is computed by new C2 production content. That contradicts the preregister sentence "C3 … never new C1/C2 production content."

Two consequences follow:
1. If C2's v2 work regresses v1 selector handling (for example, a widened or narrowed `:raw:N-M` rule), C3 fails at `<REV>`, even though C3's own data, ledger and arithmetic are unchanged. C3 then cannot verify independently of C2.
2. Conversely, the `canonical == retained` check is silently acting as C2's "legacy schema-v1 policy unchanged" regression test. That is a real safety property, but it is credited to calibration (C3) rather than operability (C2), and it would disappear if C3 were reverted.

**Evidence.** The documents leave the provenance of the canonical classifier unstated: "canonical literal v1 authority" has no code digest. The pinned-input list in the reconciliation contract names events, bindings, audit and rough text only. The preregister claims C3 reads only "frozen r22 evidence and its reconciliation record".

**Falsifier for the judge (not run by me).** Check out `<REV>`, revert only C2's changes to check-seat-bindings.py (and any shared module C2 touched) to baseline ae01e50f, then run the C3 command. Then do the reverse: keep C2 and apply a one-token mutant to the v1 `raw`-ordering normalizer in C2's file. If C3's exit code or ledger comparison changes in either case, separability is falsified for C3.

**Impacted axes.** Calibration (C3 validity) and operability (C2 v1-preservation credit). Also the frontier separability statement.

**Smallest safe correction.** Make C3's canonical classifier self-contained: either a re-authored literal v1 normalizer inside check-path-reconciliation.py, or a frozen copy of the baseline normalizer pinned by SHA-256 in `.ufo/waves/round-23/frozen/reconciliation-inputs.json`. A changed digest then gives exit 2, like the other pinned inputs. Separately, give C2's own selftest a v1-preservation control on the six `:raw:N-M` events, so the property stays credited to C2. If the gate already does this, the judge only needs to confirm it with the falsifier above. No claim text needs to change.

## F2 — C1 and C2 each define the edit-authority rule (attacked claims: C1 and C2; duplicate authority)

**Counterexample.** The rule "edit requires exact predeclared target that is also in read and write" is defined twice:
- In C1's decision rows DECLARED_EDIT, READ_ONLY_EDIT and WRITE_ONLY_EDIT, and in step 1 of structured-edit-r23.md's "Bounded procedure" ("Freeze explicit schema-v2 `edit_paths` as canonical literal subsets of both read and write targets").
- In C2's schema-v2 authority (lesson: "Prospective exact read+write+edit targets"; preregister C2 scope).

Steps 2–4 of C1's procedure also describe C2's auditor behaviour: the key-shape check, unknown as non-clean, and per-step expansion audit. Now suppose C2 lands `edit_paths ⊆ write_paths` without the read requirement. C1's gate still passes, because the preregister says it is a "new document contract, not eight repaired runtime behaviors". C2's metric still reads `structured_edit_mode` = 1, and the knowledge doc itself says "Numeric mode availability is not compliance". Both gates are green while the two authorities contradict each other.

**Evidence.** The preregister defines C1 as a document contract and C2 as a binary mode. The lesson's R23-EDIT-AUTHORITY fix demands "target/subset/opaque/extra-key/wrapper controls must be discriminating". That control would catch the divergence only if it lives in C2's selftest. I cannot see that selftest.

**Separability judgment.** This does not break separability: each gate verifies alone. It is the cost of separability. Adding a cross-gate consistency check, where C1 reads C2's schema or C2 reads C1's table, would couple the claims, and the canonical judge should reject that as a remedy.

**Impacted axes.** Depth (C1 decisions could go unrealised) and operability (C2 could be admitted as non-conforming).

**Smallest safe correction.** Keep the claims separate. Require C2's own selftest to carry independent literal controls for write-only, read-only, undeclared, traversal, URI and opaque targets, each written from the preregister `edit_decisions` row and not by reading C1's document or gate. Also trim the "Bounded procedure" steps in C1's document to point at the preregister rows instead of restating C2's auditor. That removes the second prose authority without C1's gate needing C2's content.

## F3 — C2's grounding is attributed to C1 only (attacked claim: C2; provenance)

**Counterexample.** The lesson says "S086 grounds C1, S085 grounds C3", and the preregister `sources_opened` lists only S085 and S086. But C2's auditor accepts "one of the two observed finite argument-key shapes" (`stream_content`, or `old_string`/`new_string`), and the lesson's C2 row says v2 "accommodate[s] observed native editor shapes". Those key shapes are S086 observations. So C2's allowed-shape list has no source row of its own.

If C2's gate reads S086 or C1's knowledge document at runtime to get the key shapes [INFERENCE: unlikely; a hardcoded list is more probable], C2 would also read C1's content. A shared source row alone is shared infrastructure and does not count against separability.

**Impacted axes.** Operability provenance. Separability is affected only if the runtime read is confirmed.

**Smallest safe correction.** Attribute S086 to both C1 and C2 in the lesson's source paragraph, or have C2's knowledge or selftest cite S086 directly. The judge can confirm that check-seat-bindings.py hardcodes the two shapes rather than reading structured-edit-r23.md.

## Bounded searches that found no falsifier

- **C2's event corpus.** C2's events are the round-23 wave transcripts, including the build seats that produced C1/C3 artifacts. The C2 gate treats bodies as opaque, and its metric is mode 0→1. Removing C1 or C3 would change the counts but not the metric. Not a separability break.
- **C1 reading C3 content.** No row in C1's table or procedure references S085, the path ledger or the r22 cohorts. C1's grounding is S086 metadata from the baseline ae01e50f snapshot, not round-23 C2 events. There is one residual risk: if check-edit-contract.py validates the whole SOURCES table, a missing S085 row (C3's) could fail C1. That falls under the shared-SOURCES exemption unless the gate checks S085 content. The judge can check this by deleting S085 at `<REV>` and running C1.
- **C3 arithmetic.** The ledger table is internally consistent: build 376 agree + 2 selector-normalization = 378 requests, and falsify 991 + 4 = 995. The rough-minus-retained identity holds with zero unit extra (25−23=2, 33−29=4). The retained set is a strict subset of the rough set, matching the outside report "approximate own path-binding census 25/33 vs checker23/29 (selector-normalization differences)" in r22-closure.json. The arithmetic does not use any C1/C2 quantity.
- **Shared lesson and QUALITY rows.** R23-RAW-ORDER, QUALITY51 and the other shared references are prose; none is a gate input of another claim as far as the declared documents show.

## Recommended separability matrix for the canonical judge

For each claim X, run X's preregistered command at `<REV>`, with the other two claims' production files (tools, knowledge documents, ledgers) reverted to baseline ae01e50f. Shared SOURCES, QUALITY and lesson files stay at `<REV>`. The expected result is that X's metric and exit code are unchanged. F1 is the case most likely to fail this matrix, through C3's use of the v1 normalizer in C2's file. I did not run any of this.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23f-crit23fseparability
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
