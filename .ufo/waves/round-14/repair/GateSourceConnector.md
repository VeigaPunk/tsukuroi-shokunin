# GateSourceConnector — Synthesis of Checker, Source & Contract (Round 14)

- **Seat**: `TsukuroiR14.GateSourceConnector` (leaf connector). Author-side synthesis only.
- **Axes**: depth (worked, tied lowest at 8), adjacency (8), coverage (9), operability (9), freshness (9), calibration (9).
- **Target**: Connect checker semantics, independent source reading, and stale r13 JSON contract.

## 1. Grounded Evidence & Tripartite Contradictions
1. **Checker Semantics (`check-root-dac-correction.py:98-118`)**: Gate performs narrow mechanical checks (5 headings, regex pins, string counts). It is blind to semantic truth: MD:97 passed because `non-exhaustive` was present in the file, even though it falsely applied to the closed ProtectSystem domain. Green gates do not prove source veracity.
2. **Independent Source Reading (`round-13-verifier-spotcheck.md:143-165`)**: Integrators verify source truth by reopening primary texts (`systemd.exec(5)` S044; #8047 comment S045) and reviewing git revision blobs, never by executing gate code. Source reading identified MD:97 domain error and S042 attribution fabrication.
3. **Old JSON Stale Contract (`root-dac-correction-r13.json:206-243,267`)**: `gate_contract` declared a phantom 10-heading, 13-field scan contract that the python checker never consumed. Additionally, `sources[0]` left S041 as `status: reserved` / `owner: SourceRegistry` (stale draft residue). This created a competing declarative shadow specification that diverged from executable code.

## 2. Affected Axes & Learning Trends
- **depth (8)**: Improved. Replaces illusion of automated semantic truth with verified structural boundaries.
- **calibration (9)**: Improved. Accurately demarcates mechanical conformance vs independent source proof.
- **coverage (9), operability (9), freshness (9), adjacency (8)**: Unchanged. No new planes; keeps checker <=250 lines.
- **Learning trends**: quality improved, discernment improved, expansion unchanged (repairs on existing ground).

## 3. Proposed Move: Authoritative Single-Pointer Architecture
Synthesize across round proposals (`CorrectEntry`, `CorrectionGate`, `ActiveRefs`, `StaleMetadata`) into a decoupled 4-part architecture:
1. **No Inline Second Spec in R14 JSON**: `source-scope-correction-r14.json` adheres strictly to `tsukuroi-source-scope-correction-v1` (exactly 2 correction objects). It MUST NOT declare a `gate_contract` object. Gate linkage is declared via a minimal authoritative pointer: `"verifier": {"tool": "tools/check-source-scope-correction.py", "scope": "narrow-conformance-not-semantic-proof"}`.
2. **Dual-Tier Verification Demarcation in R14 MD**: In `source-scope-correction-r14.md` provenance, explicitly partition verification responsibilities:
   - *Mechanical Conformance*: Verified by `tools/check-source-scope-correction.py` and `SKILL.md § gate`.
   - *Substantive Semantics*: Verified by independent human/integrator source reading of S044 and S045 anchors.
3. **Additive Deprecation of R13 JSON Shadow Contract**: In `root-dac-correction-r13.json`, `ActiveRefs` appends `r14_supersession` containing:
   - `R14-GATE-CONTRACT`: Declares `tools/check-root-dac-correction.py` predicates as the sole authoritative narrow contract for r13; supersedes `gate_contract` as legacy unexecuted documentation.
   - `R14-S041-METADATA`: Supersedes draft `status: reserved` with active `status: mined` in `SOURCES.md`.
4. **Mechanical Anti-Drift Guard**: `tools/check-source-scope-correction.py` includes a structural check rejecting any top-level `gate_contract` block in r14 JSON (`FINDING: SPEC_DUPLICATION`), preventing shadow-contract regression.

## 4. Risks & Second-Order Effects
- **Risk (Checker Overreach)**: Trying to encode natural-language semantic proof into Python regexes. *Mitigation*: Limit checker to structural pins, quote lengths (<=25 words), and supersession notice IDs.
- **Risk (Specification Drift)**: Modifying historical r13 bytes. *Mitigation*: Strictly additive `r14_supersession` keys.
- **Risk (Untrusted Instructions)**: External comment commands executed. *Mitigation*: Treated as data only.

## 5. Verification (Author-Side Plan for L1)
1. `tools/check-source-scope-correction.py --selftest`: Exits 0 across all fixtures.
2. `tools/check-source-scope-correction.py --revision <commit>`: Exits 0 on implementation, 1 on baseline.
3. Schema audit: `jq '.gate_contract' corpus/knowledge/source-scope-correction-r14.json` returns null.
4. Historical preservation: `git diff 8606bad4 -- corpus/knowledge/root-dac-correction-r13.md` has 0 removals/rewrites.

## 6. Findings, Limitations & Tooling Record
- **Findings**: Single-pointer architecture eliminates competing specifications while preserving gate authority.
- **Limitations**: Leaf connector; non-author verification reserved for integrator; no live commands executed.
- **Tooling record**: Tools installed or updated: none. Native git/python/jq inspected read-only.
