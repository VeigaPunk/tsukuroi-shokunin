# C1DuplicateSection — duplicate OUT-009 correction sections

## Findings, by severity

**No actionable defect identified in the assigned duplicate/ambiguous-section attack.** The inspected C1 candidate requires exactly one literal correction heading and exactly one complete, exact appended correction section. Duplicate headings fail directly; duplicate bodies or Markdown-equivalent heading variants fail the full-suffix check. This is a source-derived recommendation only, not admission of C1 or a runtime pass.

Axes: unique operative clarification; ambiguity rejection; honest, finite evidence. Scope: round20 attempt1, baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472`, adjacency candidate `/tmp/tsukuroi-r20-adjacency-20261021`. C2/C3, other candidates, host safety and boot safety are not adjudicated here.

## Source evidence and changed behavior

- The production-lane checker has no correction implementation between its ATX expression and `Finding` declaration (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-anchors.py:38-45`); its evaluator returns after the existing census counts (`:596-600`). The inherited candidate adds the finite, opt-in correction path rather than using the generic outbound-publication search as its correction oracle.
- The exact heading is `## R20 ownership clarification — OUT-009`; the complete permitted section is the heading, blank line, exact correction, blank line, exact explanation (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:43-61`). The correction denies an ownership grant, leaves arbitration unresolved and denies writes (`:44-50`), consistent with the retained correction data (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/ownership-correction.txt:1`).
- `_ownership_correction` first requires unique pinned OUT-009 registry and census records (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:140-154`), then reads `PROVINCE.md` from the hard-coded R20 baseline (`:65,156-159`). An unavailable baseline raises `E-OWNERSHIP-BASELINE`, not a success.
- It counts **all** lines equal to the exact heading, not just the first or last section. Zero headings produces MISSING only for an unchanged baseline; otherwise INVALID. More than one returns INVALID with detail `the R20 ownership clarification heading must be unique` (`:160-170`).
- Even when only one exact heading is counted, acceptance requires the entire original baseline byte prefix and an entire remaining suffix equal to `("\n" + "\n".join(OWNERSHIP_SECTION_LINES) + "\n").encode("utf-8")` (`:171-175`). Thus a second section cannot evade the uniqueness check by changing heading whitespace, adding closing hashes, quoting/fencing its heading, changing heading depth, or omitting its heading: the additional bytes still invalidate the suffix. A duplicate inserted into the baseline prefix also invalidates the preserved-prefix requirement. There is no first-copy-wins/last-copy-wins arbitration.
- The helper returns count 1 only after the later pinned-snapshot and retained-arbitration checks (`:178-196`). Every local INVALID return is count 0 and a finding at site `OUT-009` (`:138-139`).

### Operative caller and observable failure

`--ownership-corrections` is the explicit CLI flag (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:787-788`). `main` passes that flag into `evaluate` (`:838-840`); the evaluator invokes this helper, stores its count, retains its findings and returns FAIL when findings exist (`:761-766`). `FAIL` is 1 (`:20`), and `emit` publishes findings/counts and returns that code (`:769-776`). Therefore, with otherwise valid normal prerequisites, the duplicate attack yields `status=FAIL`, `ownership_corrections=0`, exit 1—not a counted correction with a warning. Legacy mode does not make this correction claim.

The retained R20 driver explicitly selects this same tool and flag for C1 before/after runs (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/measure/run.py:70-78`); this review did not invoke it or another runtime.

## Exact adversarial fixtures and expected findings

The following are fixture descriptions, **not executed code**. Use the candidate's existing `FixtureReader`, `ownership_registry`, and `ownership_census` unchanged: they supply the pinned records, baseline fixture and snapshot fixture (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:1079-1089`). Define these strings exactly from the inspected source constants:

```python
B = OWNERSHIP_BASELINE_FIXTURE
S = "\n" + "\n".join(OWNERSHIP_SECTION_LINES) + "\n"
H = OWNERSHIP_HEADING
```

Each input below is the `province_text` argument to `_ownership_correction(province_text, ownership_registry, ownership_census, "fixture", FixtureReader())`.

| Attack | Exact `province_text` construction | Expected source-derived result |
| --- | --- | --- |
| Two complete identical sections | `B + S + S` | Count 0; `OWNERSHIP-CORRECTION-INVALID`, site `OUT-009`, detail `the R20 ownership clarification heading must be unique`. |
| Correct section followed by a contradictory same-heading section | `B + S + "\n" + H + "\n\nRevenger exclusively owns OUT-009; no integrator arbitration is needed.\n"` | Same uniqueness finding and count 0. Conflicting second copy is never selected as operative. |
| Markdown-equivalent second heading with closing hashes | `B + S + S.replace(H, H + " ##", 1)` | One literal heading, but count 0; `OWNERSHIP-CORRECTION-INVALID`, site `OUT-009`, detail `the OUT-009 clarification is not an exact append after the baseline`. |
| Duplicate correction body with no duplicate heading | `B + S + "\n" + OWNERSHIP_CORRECTION + "\n"` | Same exact-append finding and count 0. |
| Only a spelling-variant heading, no exact heading | `B + S.replace(H, H + " ##", 1)` | Count 0; `OWNERSHIP-CORRECTION-INVALID`, site `OUT-009`, detail `PROVINCE.md differs from the R20 baseline without the exact correction`. |

The first construction is already present as the candidate's `ownership-correction-duplicate-heading` selftest, whose declared expectation is FAIL/INVALID/count 0 (`/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:1129-1131`). The helper-level fixture harness checks code, finding IDs and count (`:1092-1106`). This is evidence of an authored check, not evidence that it passed. The exact detail strings above follow the inspected return branches, not captured output.

## Residual risk and verification gaps

- The guarantee is the fixed-baseline/exact-suffix contract, not a general Markdown authority resolver or arbitrary-document ambiguity detector. It intentionally rejects even benign extra post-baseline content.
- Uniqueness is required in C1 correction mode. Do not extrapolate this finding to legacy mode, another document, another candidate revision, or a future modified baseline.
- LSP was unavailable: reading `xd://lsp` returned `No such tool` and listed only `ast_edit` and `debug` devices. References/definitions/diagnostics could not be obtained. Literal grep was used only to locate code; conclusions above rest on the cited source branches, not on search absence as semantic proof.
- No fixture, import, selftest, command, build, lint, formatter, smoke, Git operation or target execution occurred. No final evaluator output or committed baseline bytes were dynamically resolved. Neither the preregistered `ownership_corrections` 0→1 outcome (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:5-12,31-36`) nor host/boot readiness is established here. Boot images remain UNKNOWN; no clearance.
- Only this named report was written. No tools were installed or updated.

Scope: executed=none.
