# DraftAdmitReject — round 16 draft

Baseline db68e62065885b3f7463eb0a436c41f0dc3bcde5, read via `git show`. No commands executed, no host probes, no installs.

## Admit (citation-only)

- **R16-BOARD-SECTION** — `host-health-report-r3.md`: old "§1 verdict-board row 5" → heading `## 0. Verdict board` (L23); row_key `| 5 | update-safety |` (L31, unique); quote `detail §2.5`.
- **R16-RANK-SECTION** — `update-safety-v3.md`: old "§7 rank 1" → heading `## 5. Risk-ordered operations table (recommendation only — nothing here was run)` (L208); row_key `| 1 | Do nothing now |` (L216, unique); quote `the gate is the **next refresh**, not a run`.

Each notice must state: citation-only; R15 supersession and `BLOCKED_FOR_AGENT_PACKAGE_ACTION` unchanged; no health or repair claim.

## Reject

- Any text presenting 2026-10-14 captures as current: §0 row 2 `HEALTHY`, row 5 `DEGRADED`, `-Syu` "would be INERT".
- Treating `partial-upgrade-recheck-r15` as clearance; its health is `not_assessed`, with no health verdict possible.
- "No update action owed", "safe to run `-Syu`", or "repaired" wording.
- Bare `§7` matching: `update-safety-v3.md` L210 and L366 legitimately cite v2 §7.
- S031/S032 as health evidence (S032 says "not current filesystem state").

## Limits

Gate, errata JSON, and notices are absent at HEAD; `git status` shows only `.ufo/waves/round-16/` untracked. Decisions apply to proposed text. Gate and selftests not run. Tools installed: none.
