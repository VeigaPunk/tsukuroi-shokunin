# Round 14 mutation design — design only

**Axes:** depth (kill each distinct source-scope regression); operability (stable finding codes and a meaningful correction count).

## Evidence and boundary

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-correction-r13.md:97` contains the defective active sentence “the value set is not exhaustive.” The round-13 spotcheck at `corpus/lessons/round-13-verifier-spotcheck.md:155-165` says that assertion exceeds the documented `ProtectSystem=` domain and that comment 6071740243 never self-describes as model-generated triage. `corpus/lessons/round-13.md:68-70` contains the historical attribution that must remain preserved but be explicitly superseded.
- The round-14 spec requires the paired `R14-VALUE-DOMAIN` and `R14-COMMENT-ATTRIBUTION` corrections, quotes of at most 25 whitespace-delimited words, and explicit supersession notices. The checker author reported planned stable IDs `R14-VALUE-DOMAIN-RESTORED`, `R14-COMMENT-ATTRIBUTION-RESTORED`, `R14-MD-NOTICE-MISSING`, `R14-LESSON-NOTICE-MISSING`, `R14-SOURCES-SUPERSESSION`, and `R14-QUOTE-WORDS`; these are reported plans, not code-inspected results.
- No round-14 checker or correction pair was found in the paths inspected for this design. No mutants, scratch copies, detector runs, or hash measurements were made, as this seat is report-only. Thus every output below is an **expected** acceptance condition, not an observed result.

## Minimal probes for the landed gate

Use one clean corrected tree as the pristine control. Apply one semantic defect per isolated scratch copy; preserve the r13 historical bytes and every unrelated field. Run the same bounded gate on clean, mutant, and restored bytes when the verifying seat is authorized. Require `FAIL` (not `CANNOT_EVALUATE`), the exact stable ID below, and a lower accepted-correction count for each mutant; require clean and byte-restored runs to return `PASS`, count 2, and no findings.

| Mutant | Single defect | Expected detector result |
|---|---|---|
| Domain regression | In only the active `R14-VALUE-DOMAIN` replacement, restore the old clause “the value set is not exhaustive” (keep mirrored MD/JSON replacement text coherent; do not edit historical r13 text). | `R14-VALUE-DOMAIN-RESTORED`; expected `FAIL`, correction count 2→1. |
| Attribution regression | In only the active `R14-COMMENT-ATTRIBUTION` replacement, restore the unsupported “self-described model-generated automated triage” characterization for comment 6071740243; keep API `User`/`COLLABORATOR`, the VM-execution assertion, Codex second opinion, and maintainer deferral otherwise unchanged. | `R14-COMMENT-ATTRIBUTION-RESTORED`; expected `FAIL`, correction count 2→1. |
| Value supersession notice removed | Delete only the new notice that marks the r13 value-domain sentence superseded; retain that historical sentence and all other notices. | `R14-MD-NOTICE-MISSING`; expected `FAIL`, correction count below 2 (1 if validity is counted per correction). |
| Attribution supersession notice removed | Delete only the new round-13 lesson notice superseding its old blanket attribution; leave historical lesson wording intact. | `R14-LESSON-NOTICE-MISSING`; expected `FAIL`, correction count below 2 (1 if validity is counted per correction). |
| Registry supersession link removed (if independently gated) | Remove only the S045→S042 supersession relation; retain both immutable source rows and all other fields. | `R14-SOURCES-SUPERSESSION`; expected `FAIL`, correction count below 2. |
| Quote over limit | Change only S045 `quote` to a 26-word contiguous excerpt from the exact comment 6071740243, preserving its source ID, URL and location. | `R14-QUOTE-WORDS`; expected `FAIL`, correction count 2→1. |

The gate should count **fully conforming corrections**, not raw array entries: otherwise a malformed replacement/overlong quote can fail while `correction_count` remains 2, defeating the requested count-drop signal. Each isolated probe should assert exactly its intended finding ID (and no unrelated IDs), not merely any nonzero failure. Keep historical matches out of “restored” scans: the old bad text remains intentionally present in preserved history and is safe only with its explicit supersession notice.

## Limitations / handoff

No actual detector output, verdict, or before/after hash exists for this report-only seat. The gate is bounded conformance, not source-truth verification; the quoted-source, attribution, and source-authority claims still require the assigned evidence review. Main/verifying seat should record real pristine→mutant→restored outputs and hashes for any authorized run; do not present the expected results here as executed.

**Tools installed or updated:** none.