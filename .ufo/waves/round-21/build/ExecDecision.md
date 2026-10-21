# Round 21 — selector decision contract (C1)

Axes: source grounding; fixed decision coverage; gate operability; scope/safety.

## Findings

- Added the standalone gate draft at `.ufo/waves/round-21/drafts/ExecDecision/check-selector-contract.py` and companion JSON decision-row draft at `.ufo/waves/round-21/drafts/ExecDecision/selector-contract-r21.json`; no production path was changed.
- The gate uses the pinned shared `_revision.bind` interface for revision binding, reads the two fixed contract paths from `binding.sha` with `git show`, and refuses acceptance when no `origin/<branch>` tracking ref exists to establish pushed ancestry.
- The companion data contains exactly five unique rows: `commit` and `tag-to-commit` accept only if landed and pushed; `tree`, `blob`, and `tag-to-noncommit` refuse with `E-REVISION-INVALID`. Each has class, outcome, finding, rationale, source (`S081`/`S082`), and a fixed proposition.
- Gate exit map: 0 pass; 1 missing committed contract (`SELECTOR-CONTRACT-MISSING`, `decision_rows=0`) or supported-predicate mismatch (`SELECTOR-CONTRACT-MISMATCH`); 2 malformed schema (`SELECTOR-CONTRACT-SCHEMA`) or binding/read failure. `--selftest` is an in-memory seven-case fixture suite covering clean, missing row, wrong tree action, duplicate, missing source, wrong tag action, and missing Markdown; it was not run.
- Schema note: version 1 has exactly `schema_version`, `sources`, and `rows`; `sources` must pin both S081/S082 URL-section pairs; each row has exactly `id`, `class`, `outcome`, `finding`, `rationale`, `source`, and `proposition`. Markdown may use a table with the row ID in its first cell or a named paragraph, but the required exact proposition must occur in the same row/block.

## Evidence and limits

- Read-only pinned evidence: `.ufo/waves/round-21/snapshot/tools/_revision.py:41-49` defines the hexadecimal revision rule and binding finding IDs; `:51` defines `Binding(sha, branch, branch_tip, origin_tip)`; `:172-192` shows object-ID binding, local ancestry, and optional origin ancestry. In particular, the helper does not require an origin ref, so the draft adds a missing-origin refusal to meet the stricter pushed predicate.
- The pinned snapshot inventory does not contain `corpus/knowledge/selector-contract-r21.json` or `.md`; moving candidate files were not read. S081/S082 names and official Git documentation URLs/sections were supplied by the assignment and were not fetched. The gate itself performs no source-document network request and uses immutable commit paths at runtime.
- Observation: the implementation statically checks source JSON rows and matching Markdown row IDs/propositions. Limit: this is not execution of Git selector cases, proof of host health, or a claim of universal Git semantic correctness. No build, test, lint, formatter, import, or runtime check was performed under the NO-EXEC lane.
- [INFERENCE] Because the gate reads both files from the bound commit, the decision is specific to that immutable source revision; it does not establish that a later candidate revision retains the same contract. No tool install/update was needed or performed.

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: C1-fixed-five-type-decisions
Scope: executed=none