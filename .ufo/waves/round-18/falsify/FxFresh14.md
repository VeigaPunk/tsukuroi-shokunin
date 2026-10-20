# FxFresh14 — timer-drift freshness review

## Finding — low: evidence pointers omit the observed results

`R18-FRESH-SUPPLEMENT-31` (registry `corpus/knowledge/freshness-recheck-r18.json:796-803`; notice `timer-drift-plane.md:344-346`) is semantically **valid**: the 5-timer count remains a dated 2026-10-14 observation, and the notice does not infer active count from enablement. Its evidence pointer is **incomplete**: `capture_ref ...:47` and `capture_quote "snapper-timeline.timer"` identify only the `systemctl is-enabled` invocation. The result lines are 49-50, both `enabled` (line 47 names the corresponding timers in argument order). Exact fix: change registry `capture_ref` and notice `Capture:` to `.ufo/waves/round-17/l1-capture/fresh-capture.txt:47-51`; retain the current quote.

Same defect in neighboring `R18-FRESH-SUPPLEMENT-04` (`SKILL.md:646,1940`; registry `:526-533`): its current-use “5 active timers” correction is substantively sound but points only to command line 47. Apply the same range fix. `timer-drift-plane.md:217` is covered by its notice’s “every repeated current-use restatement” scope. `journal-boot-plane.md:259-290` is a dated 2026-10-14 table (`verified-at` lines 7-8; probe at 11:41), so it preserves history and needs no freshness correction.

## Residual risk / gaps

R18 capture has package/config facts (`host-capture-r18.txt:27-37,75-80`), not a system-timer probe; current active/all timer count remains unknown. No invocation/completion, mtime/refresh, config/rollback, or historical-fact contradiction found. No LSP device was available; literal grep was fallback, not semantic proof. No execution.

Scope: executed=none