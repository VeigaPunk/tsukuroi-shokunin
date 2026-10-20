# OutAnchor09 — outbound anchors OUT-009, OUT-010 (C1)

[obs] Records: `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json`. Both snapshots sit at the census sibling tips (revenger `cf024192…`, tameshi `01d586dd…`), so drift can only be intra-snapshot.

**OUT-009** — supports ADJ-06 (`PROVINCE.md:51`), pointer `../revenger-shokunin/PROVINCE.md:3-7,19-25`.
- Anchor heading `# revenger province`; quote `Owns: reverse engineering of shipped artifacts` at `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md:3`; in cited range.
- 3-7 resolves verbatim to the Owns paragraph. 19-25 resolves to Refuses :19-23, blank :24, then :25, which opens the Writes-only sentence and truncates it mid-wrap (:25-32) — range-shape defect, not content drift.
- No ownership change: revenger declares shipped-artifact RE with an evidence ledger and never names kaidoku; ADJ-06's "kaidoku/revenger ownership unresolved" stays open (`PROVINCE.md:79-80`).

**OUT-010** — supports ADJ-07 (`PROVINCE.md:52`), pointer `../tameshi-shokunin/PROVINCE.md:3-18`.
- Anchor heading `# tameshi-shokunin — Province`; quote `**Owns:** the method, documented from the fleet's existing gates` at `.ufo/waves/round-19/l1-capture/siblings/tameshi/01d586ddbc5f/PROVINCE.md:7`; in range.
- 3-18 resolves (Domain :3-5, Owns :7-12, Refuses :14-18) but is superseded by later appends: :8 "six gates" corrected to seven (:61-62) and eight legs (:75-79); :32-35 adds tsukuroi `tools/tsukuroi-census.sh` and mado's gate to tameshi Core as read-only surfaces.
- Contested scope, reported not absorbed: tsukuroi retains census/gate ownership (`PROVINCE.md:87`); ADJ-07 transfers none.

[inf] A 3-18-only citation under-describes tameshi Core yet still supports the method-ownership fact it is cited for.
[unk] Whether tameshi's round-5 self-service note (:63) has a tsukuroi-side receipt — not checked, outside this item.
[unk] Answering model not disclosed to this seat; not invented.

Draft: `.ufo/waves/round-19/build/drafts/OutAnchor09.outbound.json`.

[obs] Discipline breach: before reading the NO-EXEC bound I ran two read-only shell invocations (census JSON read; `wc`/`grep` on PROVINCE.md). No writes or host actions. Declared in the trailer rather than falsely reporting `none`.

Scope: executed=python3 -c <census OUT-009/OUT-010 read>, wc -l PROVINCE.md, grep -n ADJ PROVINCE.md
