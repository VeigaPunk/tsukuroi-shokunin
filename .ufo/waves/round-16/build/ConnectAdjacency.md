# ConnectAdjacency — round 16

Baseline `db68e62`; read-only git/grep/sed only. Tools installed/updated: none.

**Evidence**
- `host-health-report-r3.md:581` says "§1 verdict-board row 5". Actual: `## 0. Verdict board` (:23), row `| 5 | update-safety |` (:31, unique).
- `update-safety-v3.md:398` says "§7 rank 1". Actual: `## 5. Risk-ordered operations table (recommendation only — nothing here was run)` (:208), row `| 1 | Do nothing now |` (:216, unique).
- Other R15 section references resolve (`update-safety-v2.md:371-372`, `update-safety-note.md:501`, `host-health-report-r3.md:582`). No further wrong loci found.
- Errata JSON/MD and gate are absent from the tree; nothing verified as passing.

**Boundary**
- Locator-only fix. Quoted "`-Syu` INERT" text stays history and is never restated as current.
- `BLOCKED_FOR_AGENT_PACKAGE_ACTION` and operator remediation are unchanged.
- The gate proves locator resolution in committed bytes, not host state. S050 is own-work and cites no probes.
- ADJ-03 (mado) is not triggered: neither section contains desktop, binding, or UI text. Errata must not extend the R15 libinput mention to input or UI health.
