source: S085 — .ufo/waves/round-23/sources/r22-rough-census.txt original strip_sel and per-event break; .ufo/waves/round-23/sources/r22-closure.json verification.rechecks/notes; fixed input digests in .ufo/waves/round-23/frozen/reconciliation-inputs.json
verified-at: 2026-10-21; round22 inputs pinned at ae01e50f582016384e620022be38bf5367000e2e; outside closure rounds[422], fleet4482c275f9381f219ee4d092e0324d417c3cb1e7
recheck: python3 tools/check-path-reconciliation.py --revision <landed-hex>

# Reconciling a rough path census with retained policy findings

The fresh non-author CloseKaidoku22 admitted the bounded round22 instruments and reported approximate path counts 25/33 for build/falsify against the lane's 23/29. Those are accepted outside observations. They are not silently replaced, rounded into agreement, or rerun just to confirm their existence. Before round23 the two cohorts had no event-level explanation.

## Finding

Every event in both fixed cohorts (build 378, falsify 995 recorded requests) was classified twice from the frozen bytes: once by the outside rough rule, re-authored from S085 and never executed from the source cell, and once by canonical literal v1 authority. The retained audit's `SCOPE-PATH-DENIED` sites were then compared per event.

| Cohort | Rough | Retained | Agree events | Selector-normalization events | Unit-difference events | Unexplained |
|---|---|---|---|---|---|---|
| build | 25 | 23 | 376 | 2 | 0 | 0 |
| falsify | 33 | 29 | 991 | 4 | 0 | 0 |

The retained findings are a strict subset of the rough ones; no retained site is missing from the rough set and no retained finding is orphaned. All six rough-only events are `read` requests whose selector puts `raw` before a line range (`<path>:raw:58-58`, `<path>:raw:15-60`). The rough regular expression `:(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$` strips only a trailing range or a trailing `raw`, so `:raw:N-M` leaves `<path>:raw`. That spelling is not a bound path, so the rough rule counts a violation. The canonical selector grammar accepts `raw`/`img`/`conflicts` and range tokens in any order. The bare path is literally bound for each of those seats: build DebtSixReceipts:4 and ReviewReservation:4 (snapshot round-21 lesson), and falsify FxC1Unknown:8/9/10/14 (round22 candidate tools).

The per-event versus per-component counting unit made no difference in these cohorts: no event had more than one denied component. The 2- and 4-event gaps are therefore entirely selector normalization in the rough rule. They are not missing unsafe events and not lane under-counting. The other retained reds (16/17 unknown-tool, 2 exec) are untouched by this reconciliation and stay red.

## Reconciliation contract

- Pin the original round22 event, binding and audit bytes and the rough source text by SHA-256. A changed or missing snapshot cannot be evaluated (exit 2). It is never a freshly compared pass.
- Enumerate every seat/event with its call ID and argument digest. Record the rough category and first bad component, the canonical bad component indices, the retained count, and one disposition: `agree`, `selector-normalization` (rough flags, canonical and retained clear, and the rough-stripped spelling differs from the canonical base) or `unit-difference` (rough counts one event, canonical and retained count more than one component). Anything else is `unexplained`.
- A cohort counts as explained only if the recorded ledger equals the recomputation exactly. Rough and retained totals must also equal the reported 25/33 and 23/29, canonical must equal retained, no retained site may be orphaned, and `rough − retained = selector-normalization − Σ(unit extra)`.

This is calibration of two historical counting methods. It is not native runtime enforcement, effects/read proof, retrospective authorization, an instruction to repair old receipt text, or a general shell/URL/Markdown/Git theorem. Any actual scope violation remains a violation regardless of the reconciliation disposition.

## QUALITY check

QUALITY9/19/36/41/42/46–48/51 require bounded searches, exact source/policy attribution, independent literal cases, predeclared byte identities and preservation of failures. Reported outside numbers stay labelled as reported; per-event conclusions rest on the committed ledger `.ufo/waves/round-23/path-reconciliation.json` and the gate's own run. The gate's literal selftest includes mixed `:raw:range` order, per-component units, forged dispositions, dropped/duplicate rows, tamper and orphan controls, and the recorded L1 mutants (`.ufo/waves/round-23/measure/l1-mutation.json`) are all killed. This deepens held calibration ground. Row creation itself is neither expansion nor a quality-trend improvement.
