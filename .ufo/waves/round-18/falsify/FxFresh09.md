# FxFresh09 — C3 kill-event freshness review

**VALID content:** `R18-FRESH-NoticeKill-01/02/03` (registry 466–493) accurately supersede current use only; reasons match old rows at `kill-event-deep-r8.md:256,259,265`. Notice text preserves the 2026-10-14 snapshot (`:352–369`). Capture support: earlyoom package/binary/state :17–18, :21–22, :29, :85; zswap cmdline/sysfs :9, :12–14; sar/sysstat/PATH results :38, :82–86; empty `/var/log/sa` listing with `rc=0` :87–88. No historical causation, mtime→refresh, enabled→count, or config→rollback inference.

**INVALID as fully sourced (claims themselves supported):** `R18-FRESH-SUPPLEMENT-11` cites only capture :84 although its `now` also says `/var/log/sa` is empty; add :87–88. Same-premise neighbors are present: OOM notices cover earlyoom `:51,280,345` and zswap `:85,348,384`; `SKILL.md` Supplement-03 covers earlyoom; `degraded-triage-r4.md` Supplement-36 covers zswap. Their local citations under-document their multi-part `now`: `SKILL.md:1938` cites :17 but claims installed/version + active/enabled (add :18,:29); degraded `:644` cites :12 but claims Y/25/zstd + cmdline (add :9,:13–14).

**LOW traceability:** S060 `corpus/SOURCES.md:66` omits capture :9 and :87–88 from its declared line list, though notices rely on them. Add those lines and identify cmdline/sa listing in scope. `SKILL.md:1123–25` is historical pre-kill unavailability, not a current absence claim; no notice gap there.

**Bounded unknowns:** S060 does not read sysstat timers/config or establish whether sar data existed before the 2026-10-13/14 events or elsewhere. Current earlyoom/zswap state does not explain those events; attribution remains unknown. LSP unavailable (`read xd://lsp`: no such tool); grep was discovery only. No runtime/test/host checks.

Scope: executed=none