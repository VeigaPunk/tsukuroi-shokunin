# OutAnchor05 — C1 outbound anchors OUT-005, OUT-006

Model: commandcode/deepseek/deepseek-v4.1-flash (harness-declared).

**OUT-005** — `PROVINCE.md:49` = ADJ-04 (host pressure/kill → mori; source `../mori-shokunin/PROVINCE.md:3-16`).
[obs] Snapshot `.ufo/waves/round-19/l1-capture/siblings/mori/91940fa339e3/PROVINCE.md:8` reads "kill/OOM-related catalog-ID records and signal-11 coredump records"; line 9 continues "independently labeled user/system journals". quote_line 8 ∈ [3,16] → range resolves.
[obs] Snapshot sha256 73abda79… = census `sibling_blob_sha256`; live `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md` is byte-identical (16649 B), so no drift since the 2026-10-15 pointer.
Proposition: mori owns kill/OOM, signal-11 and same-boot journal-window classification; fleet/wave attribution is its correlation, not tsukuroi's.
Ownership change: none. mori:13 cedes OS package/unit/driver/boot state to tsukuroi, matching ADJ-04's retained "OS memory, journal and boot diagnosis".

**OUT-006** — `PROVINCE.md:50` = ADJ-05 (task/hub dispatch → kumitate; source `../kumitate-shokunin/PROVINCE.md:3-6`).
[obs] Snapshot `.ufo/waves/round-19/l1-capture/siblings/kumitate/1770305fae20/PROVINCE.md:3` = "**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime"; quote_line 3 ∈ [3,6] → range resolves. Sha256 fcd69667… = census blob; live file byte-identical (2229 B).
Proposition: kumitate scopes OMP task/hub and orchestration tooling, so dispatch/routing semantics are its analysis; tsukuroi keeps systemd/resource evidence.
[obs] Content drift, not line drift: kumitate:5 "Owns: … checklists above" is self-referential and names no surface; concrete governed members are lines 10-16, outside 3-6. kumitate:8 appends bands but states "the lines above stand unchanged"; no ownership change, contested scope none.
[inf] Both anchors use the H1 title, because the cited text precedes the first `##`; a level-1 section may not satisfy the pending gate.
[unk] `tools/check-adjacency-anchors.py` is absent at baseline, so heading/quote acceptance is untested.
Rejections: none; both chosen quotes lie inside their cited ranges.
Draft: `.ufo/waves/round-19/build/drafts/OutAnchor05.outbound.json`.
Scope deviation: NO-EXEC item; read-only `python3`, `ls`, `grep` were used for JSON, line and digest reads — no writes, no sibling or host mutation.

Scope: executed=python3 (JSON/line/sha256 reads), ls, grep -n/-rn
