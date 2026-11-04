# C2 checker attack — R2Reviewer

Recommendation: treat the frozen checker as a text/presence gate, not semantic proof. All eight items can pass together without repairing any original artifact. These are named instrument limits to carry in the lesson, not independent C2 claim failures. Axes: freshness, C2, attack.

## Observed evidence

Checker: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-r75-routed-r76.py, SHA256 01e12e6a57211f80d2f9e042a336cf7ebe933b0560fecedef0411fe158ffe3d7 (matches frozen assignment). Actual declaration diff adds this 365-line checker. Reviewed implementation and all ten selftest cases.

- Minimal fixture CLI: ROUTED_STALE=0 ROUTED_OK=8/8, exit 0.
- Selftest CLI: SELFTEST: PASS (10 cases, 10 passed, 0 failed), exit 0.
- Distant-token copy CLI: ROUTED_STALE=1 ROUTED_OK=7/8, exit 1; R76-S314-SUPERSEDE reason=need path=corpus/lessons/round-76.md missing=S999.
- Real working-tree CLI (single current-state sample): ROUTED_STALE=5 ROUTED_OK=3/8, exit 1. This is not a committed-revision closure result.

The minimal fixture contains no original notes, genuine source, usable command/cadence, or instrument execution receipt. Exact fixture manifest, commands and captured initial outputs are preserved in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/w1/R2Reviewer/probes.json. The seven marker paths contain identical copied '{}\n' placeholder bytes, not dispatch evidence. The lesson is four token-dump lines. The fake receipt explicitly begins 'fabricated'.

## Findings by severity: named limits

All eight evasions below are exercised simultaneously by the observed passing fixture; no claim of independent removal testing is made. Line references below refer to /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-r75-routed-r76.py.

| Severity / named limit | Item and observed evasion | Evidence | Smallest targeted strengthening that refuses this fixture |
|---|---|---|---|
| High — RECEIPT-UNBOUND | R76-R75-RECEIPT-REPOINT accepts 'fabricated met=1 ROUTED_OK=4/4' plus the two revision strings in the lesson. No actual re-run occurred. | lines 162–170 accept substring pairs independently, without binding results to commands/revision. | Require separately parsed receipt records naming each exact instrument and full target revision; verify captured execution/provenance independently. Merely adding more tokens cannot authenticate a receipt. |
| Medium — SOURCE-TOKEN-DUMP | R76-S314-SUPERSEDE accepts a synthetic S999 row with every metadata cell 'x' and teaches='supersedes S314 PROPAGATE_STOP graceful'; lesson says only 'correction S999'. | lines 112–130 only check row shape, prefix, branch keywords anywhere in row, and row id within lesson window. | Validate source/anchor metadata and require the teaches cell itself to express the PROPAGATE_STOP condition and distinct graceful behavior; review against frozen source. |
| Medium — JT5-NO-SPLIT | R76-JT5-COUNT accepts 'correction eight comma-separated items ten labels split' without identifying or splitting either compound item. | lines 133–135 and 93–109 are substring checks. | Require the actual eight-item list and explicit two compound splits, then derive ten labels from the parsed list. |
| Medium — MISTAKE-PREFIX-COUNT | R76-R75-MISTAKE-COUNT accepts five repeated, unterminated '- **R75-' lines, plus 'correction five two owed'. No five identifiable mistakes or two debts exist. | lines 139–159 count prefixes; no uniqueness or content requirement. | Parse five unique nonempty mistake IDs and require two explicit named owed mistakes with evidence links in the new lesson. |
| Medium — MARKER-PRESENCE-ONLY | R76-WAVE-MARKERS accepts seven copied '{}' marker files. | lines 72–77, 173–177 inspect presence only; root mode even allows directories. | For a tracking claim, compare the exact expected regular-file blobs against the carried revision; for dispatch/authenticity claims independently inspect dispatch receipts. Presence alone supports neither. |
| Medium — QUALITY-SENTENCE-ONLY | R76-QUALITY-WORDING accepts the exact sentence plus 'correction' without tying it to any admitted knowledge inventory or checks. | lines 180–182, shared block scanner lines 80–109. | Require the narrowed statement in its identified quality context and link it to an enumerated admitted-entry recheck receipt; manual semantic review remains necessary. |
| Medium — DRIFT-NO-ERRATUM | R76-JD-CONFIG-DRIFT accepts three one-line token dumps with no old claim quoted, no supersession target, no date/host receipt. | lines 185–191 require the same three literals and generic verb only. | Require a structured erratum identifying each exact old assertion, corrected assertion, host/config receipt and check date; assess append-only preservation against prior revision. |
| Medium — CRITERION-NO-SUBSTANCE | R76-QUALITY-109 accepts '109. round-76.md recheck cadence', containing neither a command nor a cadence value nor a requirement. | lines 195–206 check only three substrings after '109.'. | Parse criterion 109 as a numbered entry and require an explicit executable recheck command and concrete trigger/interval for negative host-state claims. |

Further shared limitation: generic correction verbs match substrings, and any content within the next 80 lines can satisfy a token across section boundaries (lines 80–109). Structural block parsing would reduce accidental cross-credit; semantic review is still required. No alternative checker or runtime was introduced; no frozen files changed.

## Real-tree item-by-item sample

| Item | Result |
|---|---|
| R76-S314-SUPERSEDE | stale: absent corpus/lessons/round-76.md |
| R76-JT5-COUNT | stale: missing 'ten labels' in round-75 note token block |
| R76-R75-MISTAKE-COUNT | stale: absent corpus/lessons/round-76.md |
| R76-R75-RECEIPT-REPOINT | stale: absent corpus/lessons/round-76.md |
| R76-WAVE-MARKERS | satisfied (absence of a finding in full eight-item evaluation) |
| R76-QUALITY-WORDING | stale: absent corpus/lessons/round-76.md |
| R76-JD-CONFIG-DRIFT | satisfied (same bounded inference from evaluator output) |
| R76-QUALITY-109 | satisfied (same bounded inference from evaluator output) |

## 80-line control

Copied the complete passing fixture, then replaced only its lesson with 'R76-S314-SUPERSEDE\n' + 120 newlines + original four-line lesson. This places the first token more than 80 lines before S999 and its correction. token_block returns only the first occurrence's own line plus the next 80 lines (lines 80–85), so it refuses the first token rather than searching for the later complete occurrence. Observed missing=S999 and 7/8 confirms this required control. This does not claim a stronger semantic block boundary or an exhaustive off-by-one audit.

## Residual risk and verification gaps

No LSP device is mounted: xd://lsp returned 'No such tool'; semantic references/definition/diagnostics were unavailable. Direct implementation review and literal caller search are fallback evidence, not semantic proof. The frozen declaration at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md lines 6297–6308 names this checker and the revision CLI. The exercised root-mode working-tree sample can race sibling writes and does not establish committed closure; L1 should use the frozen --revision command after repairs land. Canonical runtime routing, saturation and resume_continuity_v1 are not affected by this scoped text checker and were not exercised. No tools installed. All scratch fixtures are removed before handoff; only assigned report/evidence files persist.

Self-evaluation: accuracy 4/5 (root sample not a frozen revision); completeness 5/5 (eight limits, real state, selftest and distant-token control recorded); clarity 4/5 (table is dense); actionability 4/5 (semantic strengthening still needs human source review); conciseness 4/5 (full reproduction evidence retained separately). Overall 4.2/5. Highest-value next verification: L1 committed-revision check plus semantic receipt/source review. Would the user agree? Expected yes: pass-without-repair demonstrated without calling these limits claim failures.
