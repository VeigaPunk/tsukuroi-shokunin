# Sweep03 — C3 recon: timer-drift-plane.md

Surface `corpus/knowledge/timer-drift-plane.md`: 339 lines; baseline 842a5312 bytes = current; no R18 heading. Only S052 covers timers; S060, S051, S059 do not.

## Stale current-use quotes [obs]

- `:25` "System-scope timers are a different plane — 5 of them"
- `:217` "system scope holds 5 timers (`systemctl list-timers --all`)"

Present-tense boundary guidance; the moving-value caveat (`:17`) covers only §2.

## Evidence

S052 `.ufo/waves/round-17/l1-capture/fresh-capture.txt:47-51` (2026-10-20): `snapper-timeline.timer` and `snapper-cleanup.timer` return `enabled`. `journal-boot-plane.md:259-303` lists five timers, no snapper. S060:37 gives snapper-0.13.2-1; S060 has no timer probe.

[inf] Count 5 no longer describes the current enabled set; at least two added, exact total unmeasured. The Oct-14 fact stays true.

## Proposed notice (not written)

Heading `## R18-FRESHNESS — system-scope timer set grew after 2026-10-14 (2026-10-20)`: dated S052/S060 re-verification; snapshot preserved; current-use superseded only. Observed now: two snapper timers enabled, absent from the five-row table; re-enumerate with `systemctl list-timers --all`. Read-only; no package/service/reboot clearance.

Record: `{"id":"R18-FRESH-NoticeTimer-01","path":"corpus/knowledge/timer-drift-plane.md","baseline_quote":"System-scope timers are a different plane — 5 of them","reason":"count is the 2026-10-14 snapshot; two snapper timers enabled now","now":"snapper-timeline.timer and snapper-cleanup.timer enabled","capture_ref":".ufo/waves/round-17/l1-capture/fresh-capture.txt:47","capture_quote":"snapper-timeline.timer","notice_heading":"## R18-FRESHNESS — system-scope timer set grew after 2026-10-14 (2026-10-20)"}`

## Non-findings

- §8 census pin `:245-249`: 1032 lines/md5 `e9327046…`/`:94-97` stale; current 2679 lines/md5 `b7de3bdd…`, timer arm `1377-1404`; `:94-97` is packages root-metadata. Not notice-ready: re-pin already ordered, `ActiveState` semantics match, evidence is repo bytes not a capture line.
- Adjacent: `SKILL.md:646` repeats "5 active timers"; `SKILL.md:650` cites stale `tools/tsukuroi-census.sh:94-97,594-621` (594-621 is pacman -Qkk).

## Bounded unknowns

User-timer set (N=1), §2 live rows, P/A thresholds: no capture coverage; no change evidence. 30-day recheck due 2026-11-13.

Scope: executed=read-only git show/log, grep, sed, wc, md5sum, jq, cat.
