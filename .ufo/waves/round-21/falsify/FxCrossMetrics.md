# FxCrossMetrics — falsify attack on C1/C2/C3 causal separation and the highest round21 registry

Seat: TsukuroiR21.FxCrossMetrics (connector, fresh attack seat, leaf). Candidate revision 0a14952b59d20179e1c813af58befaecd6992a17.
Primary reviewed file: `.ufo/waves/round-21/candidate/SKILL.md` (SHA-256 c43477cb…3b3, as named in the item and in `falsify-reviews.json` row FxCrossMetrics).
Method: read/grep/glob over immutable snapshots only. No test, selftest, mutant, Git command, import, compile or network program was run. Everything below labelled "prediction" is a source reading, not an observation of execution.

## Axes

- depth (C1): five source-grounded selector decision rows.
- operability (C2): new explicitly selected consumer target-type matrix.
- calibration (C3): preregistered reviewed-byte/predicate receipts; plus the registry and audit live-map continuity that later receipts depend on.
No ordinal, admission, native-judge or non-author closure claim is made here.

## Auxiliary snapshot dependencies (not bound by this receipt)

Candidate copies, digests from `candidate-files.json`: `corpus/knowledge/selector-contract-r21.json` 1dc94c5f…, `corpus/knowledge/selector-contract-r21.md` b4966a9b…, `corpus/SOURCES.md` ef697b7c…, `SCORECARD.md` 04403120…, `corpus/lessons/round-21.md` ab841b25…, `PROVINCE.md` a296da87…, `tools/check-selector-contract.py` 239758b4…, `tools/check-revision-binding.py` 0722537d…, `tools/check-review-snapshots.py` 736c5dc8…, `tools/check-registry-coverage.py` 1ed6d8cc…, `tools/boot-chain-audit.sh` cd398e60… (grep only), `tools/_revision.py` 06b71e8c…, and a name/flag grep over all 19 candidate tools.
Frozen round artifacts that are not candidate files: `.ufo/waves/round-21/candidate-files.json`, `preregister.json`, `falsify-reviews.json`, `reviews.json` (row count only), `snapshot/tools/check-revision-binding.py` (grep of case labels and function heads only), and the file name `falsify/death-Fx03TagTree.json` (existence observed when I read it; contents not read).

## Distinguishing the four quantities (source predictions)

| Quantity | Where it lives | Predicted baseline 82e5192 | Predicted candidate 0a14952 | Basis |
|---|---|---|---|---|
| C1 source-contract `decision_rows` (count 5) | `check-selector-contract.py` evaluate:36-83 | 0, exit1 `SELECTOR-CONTRACT-MISSING` (files absent, git_read→None :86-97) | 5, exit0 | JSON rows match EXPECTED :17-23. Prose rows `selector-contract-r21.md:19-23` contain the outcome and finding substrings. SOURCES S081/S082 rows split into 13 cells with cells[4]=A and cells[8]=mined (`SOURCES.md:88-89`) |
| C2 `target_type_mode` (new mode 1) | `check-revision-binding.py` target_type_measure:739-780 | 0, finding `TARGET-TYPE-MODE-ABSENT`, exit1 | 1, exit0 | AST census of the judge at the measured tip :750-759. The candidate has top-level `target_type_probes`:676 and `target_type_measure`:739, plus `add_argument("--object-target-types")`:924 |
| C2 `target_type_tools` (actual behavior 9) | same, :763-767 | 9 [INFERENCE: unchanged binder; `_revision.py` digest 06b71e8c… is identical in the preregistration snapshot and the candidate] | 9 | Behavior is measured by the executing judge against the consumers at the bound revision, independent of mode availability |
| C2 witness | selftest :1239-1259 | n/a | old_matrix_kills 0, new_matrix_kills 1, old_matrix_tools 9 | Stub mode `target-generic-peel` :981-989 uses `^{}` only for tag objects. Every old-matrix tag case peels to a commit (:585-632), so the mutant survives. For new `tag_to_tree`, `^{}` yields a tree, and merge-base on a tree gives a non-0/1 exit → `E-GIT-FAILED` ≠ `E-REVISION-INVALID` → killed [INFERENCE about Git's exit code] |
| C3 primary receipt declarations | `check-review-snapshots.py` evaluate:26-86 | 0 | per-manifest count of rows passing the digest, predicate and scope checks | Declarations only (:85); see F6–F8 |

Contradiction, stated rather than smoothed: `preregister.json:21-26` still declares C2 `target_type_tools` 0→9. The implemented metric predicts 9→9 for that field; the 0→1 change belongs to `target_type_mode`. SCORECARD `:646-650` and lesson `:49` disclose this as a source-only correction made before execution, and keep the preregistration as history. A final receipt that reports `target_type_tools` 0→9 would therefore be false. Only `target_type_mode` 0→1 plus behavior 9/9 is consistent with the code.

## Causal separation (C1 / C2 / C3)

- Read sets are disjoint apart from shared infrastructure. C1 reads only `selector-contract-r21.json`, `selector-contract-r21.md` and `corpus/SOURCES.md` (:154-155). C2 reads the judge and the original nine consumers (:747-748, :763-764) and never touches the C1 registry. C3 reads the manifest, its `source` paths and its `report` paths (:154-156). All three call `_revision.bind` only to bind the revision.
- The class sets differ: C1 has {commit, tree, blob, tag-to-commit, tag-to-noncommit}, while C2 has {nonempty_tree, tag_to_blob, tag_to_tree, nested_tag_to_commit, annotated_tag_to_commit} (:697-704). Direct commit and direct blob behavior are exercised only by the default and old modes (`tip`:422, `blob-revision`:449, `noncommit_blob`:633). Nested tags appear only in C2. This mismatch supports separation, and it rules out reading "five" in C1 as "five" in C2.
- In the default `--tools-revision` run, `discover`:245-256 will add the two new `"--revision"` tools (selector-contract and review-snapshots) as informational `additional_*` fields only. They are not graded (:839-842). C2's grade stays original-nine.

## Highest round21 registry and live map

- Exact headings: round18:1952, round19:2060, round20:2096, round21:2127. Round21 is the unique highest heading, and its table is the final section (rows 2133–2151 run to end of file, which is line 2151).
- Coverage: the 19 rows correspond one-to-one with the 19 candidate tool files. The new `selector-contract`:2150 and `review-snapshots`:2151 rows each name exactly one tool. Kinds are gate/probe/library, every gate verdict cell carries 0, 1 and 2, and the literal `--selftest` is present in every tool (grep). Prediction: no `REGISTRY-ROW-MISSING`, `-ORPHAN`, `-AMBIGUOUS` or `-DUPLICATE` findings. Limit: tree completeness at 0a14952 is asserted by `candidate-files.json`, not observed. A non-candidate file under `tools/` would surface as `REGISTRY-ROW-MISSING` only in L1's measured run.
- The audit live map is preserved. Row 2140 matches row 2109 byte for byte, and also matches the checker constants `AUDIT_LIVE_ENTRY`, `AUDIT_LIVE_MAP` and `AUDIT_WRITE_SCOPE` in `check-registry-coverage.py:31-37`. No other round21 row references `tools/boot-chain-audit.sh`. Prediction: `audit_live_map_errors` 0. `boot-chain-audit.sh:81-86` confirms that schema-v2 never emits exit1 in live mode, so the 0/2 live versus 1 selftest distinction holds.
- The old object-selector matrix is preserved. Case labels sit at identical line numbers 427–666 in the preregistration snapshot and in the candidate, and the new functions are inserted at 676–781. That matches SKILL:2123 "Round20 object-selector cases/count remain unchanged" [INFERENCE: line-position identity, not a byte diff].

## Findings

- **F1 calibration, medium.** None of the 64 primary receipts in `falsify-reviews.json` pins the bytes of the changed C2 judge `tools/check-revision-binding.py` (0722537d…), the new C1 evaluator `tools/check-selector-contract.py` (239758b4…), `_revision.py` or `check-registry-coverage.py` (grep: no matches). The 45 C2 seats pin the unchanged consumers, the 9 C1 seats pin the JSON, the 8 C3 seats pin `check-review-snapshots.py`, and the 2 cross seats pin PROVINCE and SKILL. Scrutiny of the C1 and C2 evaluator code is therefore auxiliary-only by construction.
- **F2 C2 metric, medium.** The hermetic selftest exercises only the mode-absent branch: its fixture lacks the judge (:1251-1254). The positive availability path that the C2 headline 0→1 relies on is untested. Prediction: a mutant whose availability check always returns false survives `--selftest`, and only the real candidate run (exit1 `TARGET-TYPE-MODE-ABSENT`) kills it. A mutant whose check always returns true is killed by `target-type-missing-mode-is-not-behavior-failure`.
- **F3 C2 input contract, low.** Target-type mode binds through `bind()` (7–64 hex characters, annotated-tag peeling; :742, :192-208). The default and object-selector modes demand a full 40-hex commit (:785-790), and the parser help says "required: full 40-hex" (:918). The receipt `revision` is still the full peeled SHA (:770).
- **F4 C2 CLI, low.** The rule "select at most one matrix" is enforced only in `main`:1391-1395. `build_parser`/`cli_finding` accept both flags, and no selftest case covers the `E-CLI` exclusion.
- **F5 C2 receipt field, low.** When the judge is absent at the measured revision, `measured_judge_sha256` is the digest of empty stdout (:778) rather than null. This does not apply at baseline, where the judge exists without the mode.
- **F6 C3 denominator, medium.** The gate has no notion of a "delivered" review. A dead seat yields `REVIEW-REPORT-MISSING` and exit1 (:63-64, :79). Success for C3 is therefore `pinned_reviews` against an externally sourced count of delivered reviews, not exit0. At my read, `falsify/death-Fx03TagTree.json` existed. Also, the preregistered command (`preregister.json:41`) names only `reviews.json`, while the claim covers "build/falsify". The falsify half needs a second run, `--manifest .ufo/waves/round-21/falsify-reviews.json`, which is not in the preregistered or SCORECARD counting command.
- **F7 C3 evasion, low (disclosed class).** The trailer scan matches only raw `startswith` prefixes (:68-76). Indented, lowercase or bold variants of a contradictory execution-declaration line are invisible to the gate. Prediction: a report carrying the canonical trailers plus an indented contradictory scope line passes.
- **F8 C3 binding target, low–medium.** The falsify `source` paths are candidate copies. That each copy equals its production blob at 0a14952 is asserted by `candidate-files.json`, not by the gate.
- **F9 C1 grading, low.** Prose agreement is a per-row substring test, not a column test (:73-76). A row's `source` is checked only for membership in {S081, S082}, not against a per-class expectation (:78). The EXPECTED copy in code is the oracle; the registry discloses this self-reference at :2150. Predicted survivors: an S081↔S082 swap on one row, and a prose row that contains both outcome strings.
- **F10 registry wording vs calibration pin, low.** The round21 host-census:2133 and boot-chain-audit:2140 rows still say "(not live-run round20)". Because `AUDIT_LIVE_ENTRY` pins that exact text (:35), an accurate round21 wording would trip `REGISTRY-AUDIT-LIVE-MAP`. Wording freshness and the exact pin conflict; this is stated rather than resolved.
- **F11 verdict-map scope, low.** The revision-binding row:2145 has one verdict map, "0 finite original-nine checks clean". In target-type mode, exit0 means the mode is available and 9/9 behavior passed; the round18 consistency probes do not run (early return :1391-1409).

## Proposed move (one, bounded)

For any future wave, and never retroactively for round21: preregister at least one primary receipt whose `source` is each claim's changed evaluator file. For round21 that means `check-revision-binding.py` for C2 and `check-selector-contract.py` for C1. The existing `distinct_source_files` field then shows coverage of the changed loci without any gate change.
- Improves calibration, and the depth of falsification on C1/C2. No metric, ordinal or frozen matrix changes, so no axis is harmed.
- For round21 itself, the gap (F1) belongs in final accounting as a disclosed limit. Adding rows now would be the retroactive reservation that lesson R21-RETRO-RESERVATION rejects.

## Risks

- Every behavioral number above is a prediction. Git exit-code semantics for merge-base on a tree, and the actual 9/9 behavior, are [INFERENCE].
- Registry tree completeness, and copy↔production identity, are unobserved.
- Selftest tally: the four added `check()` calls suggest 62→66 [INFERENCE from the round20 receipt of 62, not a stated or observed tally].

## Verification for L1 (not run by this seat)

`python3 tools/check-selector-contract.py --revision <REV>` at the baseline and at the candidate; `python3 tools/check-revision-binding.py --tools-revision <REV> --object-target-types` at both; `python3 tools/check-revision-binding.py --selftest` (read the `TARGET_TYPE_WITNESS` line); `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map`; `python3 tools/check-review-snapshots.py --revision <REV> --manifest .ufo/waves/round-21/reviews.json`, and the same with `--manifest .ufo/waves/round-21/falsify-reviews.json`.

No tool installation was needed or performed. No non-author closure or outside promotion is claimed.

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: c43477cbb012fe0b0c4170610d4fa034d2e8ae5b09005e3f48a4cccd38f843b3
Predicate: finite-metrics-and-current-registry
Scope: executed=none
