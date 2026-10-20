# FxFresh12 — `pacnew-plane.md`

Axes: evidence fidelity; current-use scope; neighbor coverage.

**SURVIVES — `R18-FRESH-SUPPLEMENT-32` (only freshness record for this path).** Registry lines 806–813 quote the 2026-10-19 package query, give the new state, capture reference and reason. The old query/no-install statement at `corpus/knowledge/pacnew-plane.md:19` is dated history, not made false. The append at `:63–67` correctly limits its correction to current-use readings, preserves history, and does not infer that `pacdiff` is available. The reason (“correction sweep…; historical measurements remain dated”) is generic but consistent; it is not treated as evidence.

**Capture support:** `host-capture-r18.txt:27–39` shows the local-db listing command and exact output `/var/lib/pacman/local/pacman-contrib-1.13.1-1` at `:36`, rc=0 at `:39`. This supports local metadata presence. `:82–86` probes paccache, sar, atop, dool, dstat and earlyoom—not pacdiff—so the notice correctly leaves pacdiff executable presence unknown. No invocation-to-completion, mtime-to-refresh, enabled-to-count, or config-to-rollback inference appears here.

**Neighbor coverage:** Within this file, line 19 is the sole current-use absence/pacdiff premise; line 24 is conditional guidance (“when available”), not another availability claim. Same-premise cross-file records are separately noticed: `R18-FRESH-NoticePackages-08` and `R18-FRESH-SUPPLEMENT-01/02/09/12/19/21/26/35`; their notices were located in the corresponding files (package-state notice at `:396–402`; supplement IDs in each file). No target-file neighbor is omitted.

**Invalid:** none. **Fixes:** none. **Bounded unknowns:** no R18 pacdiff executable check or new `/etc` `.pacnew`/`.pacsave` census; the 2026-10-19 pathname counts are not current R18 counts. LSP unavailable (`xd://lsp`: no such tool); grep was used only as a literal locator, not semantic proof.

Scope: executed=none