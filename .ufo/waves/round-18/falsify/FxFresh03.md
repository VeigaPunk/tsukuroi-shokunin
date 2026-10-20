# FxFresh03 — C3 closeout-r11

Axes: evidence linkage, correction truth, same-premise coverage.

## Findings

- **Medium — R18-FRESH-SUPPLEMENT-38 INVALID as pinned; the bounded claim survives.** `freshness-recheck-r18.json:866-872` and `closeout-r11.md:423` correctly prohibit replay/removal and grant no removal/reboot clearance, but `capture_ref:95` supports only the 7.2.3 row, not absence of a 7.1.4 row. `tools/check-appended-notices.py:280-309` accepts only one positive line and requires the quote on that line, so a `:92-96` range is not a valid fix. Narrow `now` to line 95's 7.2.3 missing-built-modules row plus “old removal action is not cleared; recheck before action”; remove the unsupported no-7.1.4/stale inference unless a one-line authenticated summary or range-capable reference is added. Quote the full line 95 for precision. Reason at JSON:869 is accurate.
- **Low — R18-FRESH-SUPPLEMENT-39 INVALID as pinned; the bounded claim survives.** `freshness-recheck-r18.json:876-882` and `closeout-r11.md:425` correctly do not infer rollback, and `capture_ref:80` exactly supports `SNAPPER_CONFIGS="root home"`. It does not support a separate claim that config files named `home` and `root` exist (those are lines 76-77); the checker only accepts a single line. Narrow `now` to the configured variable and state that files, snapshot inventory and restoration remain unverified; alternatively add single-line records for each asserted fact or extend reference syntax. Reason at JSON:879 is accurate.

## Coverage, residual risk, verification gaps

The notices cover the only current-use loci found: closeout lines 223 (DKMS) and 229 (Snapper). Line 53's `smi=610.57.04` is a dated driver-plane capture, not a DKMS registration; line 317 is a recheck command, not a current-use claim. The old `/.snapshots` observation remains historical; current inventory/restoration are explicitly unknown. No invocation-to-completion claim found (lines 409-410 report log entries only); line 183 disclaims treating the 36-day stamp as repo state; line 52 says timers-enabled/scanned, not active-count. No config-to-rollback inference or historical fact made false found. LSP is unavailable (`read xd://lsp`: no such tool); grep was used only to locate literal neighbors, not as semantic proof.

Scope: executed=none