# FxFresh10 — C3 per-surface attack: corpus/knowledge/oom-event-plane.md

Verdict: **SURVIVES** — 6/6 records valid; 2 LOW findings, no FAIL. Read-only: read/grep only.

T=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md`;
C=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/l1-capture/host-capture-r18.txt`;
R=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/freshness-recheck-r18.json:415-464`.

Per-record (baseline_quote located; capture line byte-checked):
- NoticeOom-01 VALID — T:51 ✓; C:29 dir entry ✓; "installed" rests on the local-db artifact, no transaction-time overclaim (zcode narrowing respected).
- NoticeOom-02 VALID, LOW — T:280 ✓; C:21 ActiveEnterTimestamp ✓; active C:17, enabled C:18. R reason "active and enabled since 09:57:11 -03" overstates: enabled-since is unevidenced; ActiveEnterTimestamp proves active-since only. Fix reason: "active since 2026-10-20 09:57:11 -03 and currently enabled". Operative "now"/notice body already precise.
- NoticeOom-03 VALID — T:345 ✓; C:85 `/usr/bin/earlyoom` is the literal `command -v` output (invocation C:82); no invocation→completion conversion.
- NoticeOom-04 VALID — T:85 ✓; C:12 `Y`, C:13 `25`, C:14 `zstd`; quote "Y" minimal but anchored by :8-15 context; no pressure/causality claim.
- NoticeOom-05 VALID — T:348 ✓; C:9 exact `zswap.enabled=1 zswap.max_pool_percent=25`; enable-action cell explicitly superseded; no config→rollback claim.
- NoticeOom-06 VALID — T:384 ✓; C:9.

Class sweep: zero mtime→refresh; all six bodies preserve dated meaning ("stays dated"); notice headings at T:442/446/450/454/458/462 byte-match R.

Same-premise neighbors: GAP (LOW) — T:281 "Nothing was configured to act before the kernel." is §4.5's conclusion one line under the -02 quote; stale as current use now that earlyoom is installed+active+enabled; named by no notice. Fix: extend -02 body to name line 281, or add a 7th record. Judged historical, no notice owed: §5 "nothing was watching" (dated 14:42 cell), §5 reconstruction "no userland monitor" ([inference]), T:52 kill causality, T:425 ledger row.

Unknowns (bounded): current systemd-oomd state not recaptured (no record claims it); earlyoom enable-in-time absent from C.

Scope: executed=none
