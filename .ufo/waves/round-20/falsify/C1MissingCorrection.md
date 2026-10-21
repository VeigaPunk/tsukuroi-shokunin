# C1 missing-correction review — round 20 attempt 1

Axes: missing-versus-invalid diagnostic accuracy; correction-count integrity; separation from unavailable registry evidence. Read-only source review, not admission or an executed measurement.

Path abbreviations below: `candidate/` = `/tmp/tsukuroi-r20-adjacency-20261021/`; `lane/` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`. Unless another file is named, candidate line citations refer to `candidate/tools/check-adjacency-anchors.py`.

## Findings by severity

### P2 — A genuinely absent correction is called INVALID after an unrelated append

**Location:** `candidate/tools/check-adjacency-anchors.py:160–168`.

The missing case is narrower than the preregistered distinction. With no exact correction heading, the candidate emits `OWNERSHIP-CORRECTION-MISSING` only when *all* current `PROVINCE.md` bytes equal the baseline. Any other bytes emit `OWNERSHIP-CORRECTION-INVALID`, even when the correction is wholly absent and the original baseline and OUT-009 pins are untouched.

**Source-derived counterexample [INFERENCE; not executed]:** retain baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472:PROVINCE.md`, retain the original registry/census, and append only `\n<!-- unrelated registry documentation note -->\n`. This preserves the complete baseline prefix, original ADJ-06 arbitration and OUT-009 identity; it supplies no correction or altered correction. The unique-pin checks at `candidate/tools/check-adjacency-anchors.py:140–154` pass, `headings` is empty at `:162–164`, but byte equality at `:165` fails. The returned finding is therefore `OWNERSHIP-CORRECTION-INVALID`, correction count **0**; the caller produces FAIL/exit **1** (`:761–776`, with constants at `:20`).

**Expected:** the preregistered absent-correction ID is `OWNERSHIP-CORRECTION-MISSING`, distinct from the altered-correction ID (`lane/.ufo/waves/round-20/preregister.json:31–36`). The retained source oracle describes missing as omitting the correction while retaining the pinned OUT-009 identity, and its altered example changes the correction into an ownership grant (`lane/.ufo/waves/round-20/build/OracleC1.md:19–25`). Neither narrows “missing” to whole-document byte identity. This counterexample changes no correction text, ownership source or baseline prefix.

**Impact:** wrong typed finding, not a false pass: count **0** and exit **1** remain appropriate. The diagnostic conflates absence with alteration merely because unrelated documentation was appended. Preserve the baseline/pin validation, but distinguish a missing correction from an existing malformed correction rather than using whole-file equality as the absence classifier.

## Exact-baseline and unrelated-data checks

The following outcomes are control-flow deductions, not observed command output.

- **Exact preregistered baseline, intact registry/census:** the missing path itself is correct. The candidate reads baseline `PROVINCE.md` at the explicitly pinned R20 hash (`candidate/tools/check-adjacency-anchors.py:65,156–167`). The retained `candidate/PROVINCE.md:51,79–80` preserves unresolved arbitration; `candidate/PROVINCE.md:108–146` contains the R19 anchors/digests and ends without an R20 correction. Its OUT-009 row is at `candidate/PROVINCE.md:129`. Registry identity at `candidate/corpus/knowledge/adjacency-anchors-r19.json:112–124` and census identity at `candidate/.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json:2980–3004` match the candidate's required pins (`candidate/tools/check-adjacency-anchors.py:77–99`). With those prerequisites and exact baseline bytes, the helper returns `OWNERSHIP-CORRECTION-MISSING`, **0** corrections (`:164–167`), and evaluation returns FAIL/exit **1** (`:761–776`). No wrong code/count was found for that exact input.
- **Whole registry unavailable:** `main()` returns `E-REGISTRY-MISSING`, CANNOT_EVALUATE/exit **2**, before calling the correction evaluator (`candidate/tools/check-adjacency-anchors.py:819–839`). **0** is only the default correction counter, not a measured finding that a correction is absent (`:363–374,381–382,800–801`). This is correctly distinct from a genuine missing correction. The same registry refusal already exists in the production-lane baseline source at `lane/tools/check-adjacency-anchors.py:651–672`.
- **Whole pointer census unavailable:** `evaluate()` raises `E-CENSUS-MISSING` before loading/classifying the correction (`candidate/tools/check-adjacency-anchors.py:467–483`); `main()` maps that exception to CANNOT_EVALUATE/exit **2** (`:841–844,800–801`). Again, default count **0** is not evidence of correction absence. This preserves the baseline census error contract (`lane/tools/check-adjacency-anchors.py:306–321`).
- **Unrelated outbound record or snapshot absent:** a missing non-OUT-009 registry record receives `OUTBOUND-CENSUS-INCOMPLETE` (`candidate/tools/check-adjacency-anchors.py:640–644`); a missing unrelated snapshot receives `ANCHOR-SNAPSHOT-TAMPERED` (`:571–576`). Neither condition is used by `_ownership_correction`, which selects only OUT-009 from registry/census (`:140–154`). With otherwise readable input, the C1 result is still calculated separately at `:761–765`. Thus an unrelated missing anchor does not itself become `OWNERSHIP-CORRECTION-MISSING` or force the C1 correction count to zero when an exact valid correction exists; the overall registry gate can still fail independently.
- **Unrelated knowledge publication absent:** missing text becomes an empty string (`candidate/tools/check-adjacency-anchors.py:300–310`); absent inbound publication receives `INBOUND-UNPUBLISHED` (`:742–747`). C1 still reaches its independent helper. No C1 error-code/count conflation was found on this path.
- **OUT-009 registry/census identity absent or changed:** this is a related evidence failure, not missing unrelated data. The helper returns `OWNERSHIP-CORRECTION-INVALID`/count **0** before the missing-heading check (`candidate/tools/check-adjacency-anchors.py:138–154`). A zero counter alone therefore cannot distinguish missing correction, invalid source identity and cannot-evaluate outcomes; status plus finding ID must be retained.

The canonical retained measurement source selects the baseline for `c1-before` and the candidate revision for `c1-after`, without `--registry-from`; expected exits are respectively 1 and 0 (`lane/.ufo/waves/round-20/measure/run.py:70–78`). CLI binding and immutable registry selection remain in the existing `main()` → `evaluate()` path (`candidate/tools/check-adjacency-anchors.py:819–840`); this review did not invoke another runtime.

## Residual risk and verification gaps

- This review inspected the inherited adjacency candidate and the exact R20 preregistration/measurement source. No current host, boot-image, service, package or boot-readiness conclusion is supported. Boot images remain UNKNOWN; no clearance.
- LSP status/references/definition/diagnostics were unavailable under this seat's read/grep/glob/report-write-only contract. No LSP request was made. Literal grep was used for navigation only, not as semantic proof of caller completeness; the cited caller/definition bodies were read directly.
- No evaluator, test, import, shell, subprocess, build, lint, formatter or smoke command was run; no external request or host probe was made. No tool was installed or updated. Working-tree bytes were not independently authenticated against Git objects. The exact outputs above are explicitly source-derived deductions.
- The finding is a typed-diagnostic defect on a baseline-preserving unrelated append. It does not establish an incorrect positive count, a false pass, missing mandatory source pins, arbitrary Markdown equivalence or broader C1 saturation. No resume path, routing mutation or admission decision is reviewed here.

Scope: executed=none.
