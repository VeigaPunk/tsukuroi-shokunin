VERDICT: defect-found

Seat R51ConnOverlap (connector, non-counted, w1). Scope: cross-claim and cross-source overlap scan of round 51 at pin 2732ee6c06108c031c4d8043239b994e0504eb2f. Bytes read with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 2732ee6c…:<path>`; sibling bytes read read-only from `/home/vgpnk/Projects/shokunin/<sib>-shokunin` (`show`, `rev-parse`). Working-tree files were only hashed (`git hash-object`, no index write). No counter, selftest or battery was executed; all findings are static reads plus two read-only scripts (receipts in `.ufo/waves/round-51/w1/R51ConnOverlap/`).

## Summary

1. No counter reads another claim's measured bytes. Data reads are separable (table A).
2. Code-loading is NOT separable from the working tree. C1 (`check-scrub-admission-r51.py` → `lint-grounding-r51.py`), C2 (`score-counter-cheats-r51.py` → both matcher counters) and C3 (`check-adjacency-table-r51.py` → `check-adjacency-table-r50.py`, and `check-adjacency-anchors.py`) execute code from the lane working tree, not from the pin. Also the round-51 `controls/battery.py` runs the working-tree paths. All 13 counter/data files I hashed are currently byte-identical to the pin (so no present effect), but the frozen-hash claim does not bind what runs. This is a real causal-separability defect.
3. C3 has a live-tip input: `live_quote_ok` reads each sibling's current HEAD. Today 9/9 quotes are present in tip (tolerance is ≥8), so this is a moving input owned by sibling lanes.
4. C3's displayed-bound leg is NOT a duplicate of `check-adjacency-anchors.py` for path, commit prefix, or heading cell. It partly duplicates it for quote-in-row, digest, and (with different bytes) quote-line / heading-section.
5. C1's quote leg (`lint-grounding-r51.py`, whitespace-normalised whole-line equality) and the older `check-scrub-grounding-r45.py` quote leg (byte-substring + half-length) match the same 63 quote lines and DISAGREE on one: GR1 `cmdline.c:147`. The R51 lint accepts a quote that is not a byte substring of its cited snapshot line. r45 is not called by any R51 counter, so this is not a double count inside a predicate; it is a conflicting instrument left at the pin.
6. Sibling PROVINCE files: no sibling now claims an owner role for an ADJ-table surface in a way that contradicts ADJ-01..ADJ-07. One pre-existing unresolved overlap (ADJ-06 kaidoku/revenger), one surface-level read-only claim on the tsukuroi census by tameshi (benign), and a mori memory-pressure wording that is already split by question.

## (a) Reads per counter at 2732ee6c

Table A — data reads (REV = pinned bytes; WT = lane working tree; SIB = sibling repo object store)

| Counter | Reads (data) | Source | Evidence |
|---|---|---|---|
| C1 `lint-grounding-r51.py` | `corpus/knowledge/btrfs-scrub-grounding-r45.md`, `corpus/SOURCES.md`, 11 snapshot files under `.ufo/waves/round-42..45/frozen/**` | REV (`read_bytes` with rev; WT fallback only if rev is None) | lint51copy.py:39-40, 43-63, 89-96, 292-299 |
| C1 `check-scrub-admission-r51.py` | entry, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, wave cohort `.ufo/waves/round-51/w2/<seat>.md`, LANE_FILES (incl. `FROZEN.md`) for citation line counts | REV (`show`) | adm51.py:57-61, 79-91, 218-230 (LANE_FILES via `show(lane, rev, path)`), 283, 324-327 |
| C1 (loads its own lint) | `lint-grounding-r51.py` module | WT (`os.path.dirname(__file__)`) | adm51.py:95-103 |
| C2 `check-selftest-matcher-r51.py` | `tools/tsukuroi-census.sh` | REV (`git show`) unless `--census-file` | match51.py:121-138; probe + selftests in scratch :109-144 |
| C2 `score-counter-cheats-r51.py` | `tools/tsukuroi-census.sh` at REV; writes 4 fixtures under scratch | REV for data, but counter and r50 counter resolved from WT | cheats51.py:86, 91-93 (`counter = os.path.join(lane, a.counter)`, `r50 = os.path.join(lane, 'tools/check-selftest-matcher-r50.py')`), 105-112 |
| C3 `check-adjacency-table-r51.py` | `PROVINCE.md`, `corpus/knowledge/adjacency-anchors-r19.json` | REV (`show_text` → `git show`) | r51adj.py:216-217 |
| C3 sibling legs | `<sib>-shokunin` PROVINCE blob at pinned commit | SIB object store (pinned) | r51adj.py:78-81, 116-117 |
| C3 r50 legs (child process) | `check-adjacency-table-r50.py` loaded from its own directory | WT | r51adj.py:69, 222-230, 265-268 |
| r50 live leg (inside C3) | sibling HEAD PROVINCE (`rev-parse HEAD` then `show`) | SIB live HEAD | r50adj.py:152-158 |
| r50 anchors leg (inside C3) | `tools/check-adjacency-anchors.py` run as `os.path.join(lane, CHECKER) --revision <REV>` | WT (code), REV (data) | r50adj.py:352-353 |

Cross-claim data reads: none. C1 reads neither the census, PROVINCE nor the registry (grep of lint51/adm51 for adjacency|selftest|census|cheat|PROVINCE|anchors: no hits). C2 reads only the census at REV. C3 reads PROVINCE, registry, sibling repos and round-19 census/snapshot bytes via the anchors checker. The FROZEN.md "causal separability" paragraph (FROZEN.md, round-51 frozen record, line 40) is consistent with this for data; it does not mention code-loading.

Code-loading (causal leaks):
- L1. C2 scorer runs the matcher and r50 counters from the working tree: cheats51.py:86, 91-92. Its census fixtures come from REV (:93), so the scored census and the scored counter may come from different revisions.
- L2. C3 loads `check-adjacency-table-r50.py` from its own directory (r51adj.py:69, :222, :265). Run in place, that is the working-tree copy, not the pin. Its own anchors leg runs `check-adjacency-anchors.py` from the lane working tree (r50adj.py:352-353).
- L3. C1 admission loads `lint-grounding-r51.py` from its own directory (adm51.py:95-103), while hashing/line-counting the same file at REV (adm51.py:218-230). The executed code and the checked bytes are not forced equal.
- L4. `controls/battery.py` lines 17-21 point C1/C2/C3 at `${L}/tools/...` (the lane root), so pre-data controls also run working-tree code.
- L5. `check-adjacency-anchors.py` reads `.ufo/waves/round-20/ownership-correction.txt` from the working tree (anchors.py:137-142), but only under `--ownership-corrections` (anchors.py:778). C3 does not pass that flag, so this read does not reach C3's predicate. Noted as not a leak for C3.

Working-tree hash check (`git hash-object` vs `git rev-parse 2732ee6c:<path>`): SAME for tools/check-selftest-matcher-r51.py, -r50.py, score-counter-cheats-r51.py, check-adjacency-table-r51.py, -r50.py, check-adjacency-anchors.py, lint-grounding-r51.py, check-scrub-admission-r51.py, check-scrub-grounding-r45.py, tools/tsukuroi-census.sh, PROVINCE.md, corpus/knowledge/adjacency-anchors-r19.json, corpus/knowledge/btrfs-scrub-grounding-r45.md. No present divergence; the defect is that the predicate does not force it.

Recommended fix for the L1 (not applied by me): run each counter from a checkout at the measured revision (or assert `hash-object` of every loaded tool equals its FROZEN-hashes entry before exec), and have C3 and C2 resolve their child counters relative to the pin.

## (b) C3 displayed-bound leg vs `tools/check-adjacency-anchors.py`

The anchors checker is already a counted leg of C3 (`anchors_checker_rc == 0`, r50adj.py:352-357). Its publication test (`_outbound_publication`) is at check-adjacency-anchors.py:402-431. Its region is every line after the heading to end of file (:420), not the displayed row alone.

| Leg | r51 counter (line) | anchors checker (line) | Verdict |
|---|---|---|---|
| Quote | display_bound quote equality, r51adj.py:111-112 (cell == registry quote) | id+quote substring on one line, check-adjacency-anchors.py:421-422 | r51 stronger (cell equality). Subsumes the anchors leg. Real overlap, benign. |
| Heading | display_bound heading equality, r51adj.py:109-110 | heading substring anywhere after the heading, :429-431 (satisfied by the table's own heading cell) | r51 NEW. Anchors cannot detect a wrong displayed heading. |
| Sibling path | display_bound path equality, r51adj.py:98, 105-106 | none | r51 NEW. |
| Commit | displayed 12-40-hex prefix of registry full commit, r51adj.py:107-108 | full 40-hex commit on an id-line after the heading, :423-425 (satisfied by the "Portable digests" list at PROVINCE.md:137-146, not by the displayed cell) | r51 NEW for the displayed cell. This is exactly the round-50 OUT-009 forgery class the anchors checker cannot see. |
| Digest | digests_bound_ok, r51adj.py:143-161 (path+commit+sha256 equal on each digests-list line) | id+digest substring on one line, :426-428 | Overlap. r51 is stricter (exact regex, path and commit too). Benign duplication. Note r51 scans the whole file, not the section (:150). |
| Quote in pinned line + heading section | quote_specific, r51adj.py:117-135 (sibling repo at pin, >=6 words, quote on registry quote_line, section ends at ANY ATX heading, `^#{1,6}\s`, :133) | `_heading_section_contains` (same-or-higher level, :357-378) and quote-on-quote_line (:620-622), but against the lane snapshot (registry `snapshot` path, digest-bound at :599-601) | REAL duplicate logic over different byte sources. Same sha256 binds both, so bytes match when both pass. Semantic divergence: r51 ends the section at a sub-heading, anchors does not. Not run; current pins not checked by me. |

Net: 3 legs of r51's display_bound_ok (path, commit prefix, heading cell) are not covered by any existing leg. Quote-row, digest and quote-section legs overlap existing legs with stricter or differently-sourced logic.

## (c) C1 quote leg vs `check-scrub-grounding-r45.py` quote leg

- Both regexes match the same 63 quote lines in the GR1-GR3 sections of `corpus/knowledge/btrfs-scrub-grounding-r45.md` (receipt `qcmp.out`).
- r45 (check-scrub-grounding-r45.py:294-301, `quote_good`): quote must be an exact byte substring of the cited line, len>=10 (or whole line), and cover >=half the stripped line.
- lint-grounding-r51 (lint51copy.py:99-100 `norm`, :233): whitespace-collapsed equality of the whole line.
- Measured on pinned snapshots (receipt `qdiff.out`): lint accepts 63/63; r45 rule accepts 62/63. Disagreement: entry line 27, GR1, `S246 cmdline.c:147`.
- Byte evidence (`git show 2732ee6c:.ufo/waves/round-45/frozen/src/cmdline.c` line 147, od -c): ` *<TAB>potentially suffixed with K, M, G, T, P, E.` The entry quote is `* potentially suffixed with K, M, G, T, P, E.` with a space. The lint's `norm()` makes the tab a space and accepts; r45's substring test rejects.
- Relevance: the C1 claim says the GR1 quote "carries its `* ` leader". The counted lint admits it only because of whitespace normalisation. Not a double count inside R51's predicate (adm51 does not call r45: grep of adm51.py/lint51.py finds no reference), but a conflicting instrument still at the pin. Routed to the C1 seat/L1 as a fact, not a verdict.

## (d) Sibling PROVINCE files at live HEAD (read-only; snapshots in receipts `live.out`)

Each sibling's registry pin is still present at its live tip quote (9/9 quotes present at pin and at tip, receipt `live.out`). Tips: kagi 69b61db, kaidoku e4f2cfa, kama 7ee8cbd, kumitate 14057f3, mado 3b55b6e, mori 325f7e6, revenger 6defe31, tameshi 8c20d5c.

| ADJ / OUT | Sibling claim (tip) | Assigned in r51 ADJ table | Verdict |
|---|---|---|---|
| ADJ-01 / OUT-002 kama | `tip-kama.md:6-9` Owns served-model-id reconciliation (`GET /v1/models` vs `--alias`) | kama (PROVINCE.md:12 ADJ-01) | Consistent. Noise. |
| ADJ-02 / OUT-003 kagi | `tip-kagi.md:5-6` Owns domain knowledge; secrets/vault ops in its Domain line | kagi | Consistent. Noise. Also kagi uses its own `corpus/adjacency.tsv` (`tip-kagi.md:51`): name collision with tsukuroi's ADJ table, different file. Noise. |
| ADJ-03 / OUT-004 mado | `tip-mado.md:6-9` Owns hypr/waybar/terminal configs and screen/idle behavior | mado | Consistent. Noise. `tip-mado.md:96` cites tsukuroi's OUT-004 by bare line range `lines 3–16` (mado's own file, not a tsukuroi claim). Noise. |
| ADJ-04 / OUT-005, OUT-007 mori | `tip-mori.md:6-10` Owns kill/OOM catalog IDs, cgroup `memory.events`, and "resource runway (…memory pressure)"; `tip-mori.md:12-15` refuses OS/boot (→ tsukuroi); `tip-mori.md:286-290` acknowledges the census reads the same `/proc/pressure/memory` | mori; OS memory stays tsukuroi (ADJ-04 "Tsukuroi retains") | Real but pre-existing and already split by question (tsukuroi PROVINCE:30-33; mori tip:286-290). Not introduced by round 51. |
| ADJ-05 / OUT-006 kumitate | `tip-kumitate.md:3-6` Domain: scopes OMP task/hub; refuses everything outside | kumitate | Consistent. Noise. |
| ADJ-05 / OUT-007 mori | `tip-mori.md:12` refuses dispatch (→ kumitate) | kumitate | Consistent. |
| ADJ-06 / OUT-008 kaidoku, OUT-009 revenger | `tip-kaidoku.md:3-4` Domain: "reverse engineering of shipped artifacts with REA"; `tip-revenger.md:3-5` Owns: "reverse engineering of shipped artifacts" | recipient "protocol integrator — kaidoku/revenger ownership unresolved" (PROVINCE.md:17) | REAL overlap between two siblings, pre-existing, explicitly unresolved in the ADJ table. Not new. Not a tsukuroi defect. |
| ADJ-07 / OUT-010 tameshi | `tip-tameshi.md:7-12` Owns the method (kumitate, kagi, kaidoku, game-lane gates; does NOT list tsukuroi); `tip-tameshi.md:28-35` Core lists `tools/tsukuroi-census.sh` as a read-only primary surface and says "the tsukuroi and mado gates entered through the round-5/6 service runs" | tameshi (method advice); census repair retained by tsukuroi (PROVINCE.md:52) | Surface-level overlap: tameshi lists the same census C2 counts. Tameshi explicitly does not own it (`tip-tameshi.md:14-17` "never edits a sibling's gate code"). Benign. Noted because C2 is a mutation-style instrument on that census. |
| tsukuroi boot/update-safety | `tip-mori.md:116`, `:141` (boot-chain stays tsukuroi); `tip-kaidoku.md:125` (update-safety gate is tsukuroi's) | tsukuroi | Consistent. Noise. |
| btrfs / scrub / SMART | no sibling PROVINCE mentions btrfs, scrub or SMART (grep over the 8 tips) | tsukuroi | No overlap. |

No sibling PROVINCE claims ownership of: the adjacency table, the portable anchor registry, `Portable digests`, the selftest matcher, or the census scrub arm.

## Noise (checked, not overlaps)

- `tip-mori.md:66`, `:71` cite tsukuroi's adjacency-handoffs file by line range; C3's bare-range leg (r51adj/r50adj BARE) is scoped to PROVINCE ownership cells only.
- `tip-kagi.md:51` `corpus/adjacency.tsv`: kagi's own file; not tsukuroi's table.
- ADJ routing keywords appearing in sibling tips are cross-references, not owner claims.

## Not done

- No counter, selftest, scorer or battery was run (EXEC-AUTHORIZED scope = the named greps/shows). Therefore I did not measure whether `quote_specific_ok == 10` or `digests_bound_ok == 10` hold at the pin; the claims above about those legs are structural only.
- I did not verify the round-45 counter's current PASS/FAIL at the pin (it needs `~/.omp/agent/sessions`).
- Receipts: `.ufo/waves/round-51/w1/R51ConnOverlap/` (qdiff.py, qcmp.py, live.py and their outputs). The scripts expect the REV-pinned copies of `lint-grounding-r51.py` and `btrfs-scrub-grounding-r45.md` they name in scratch; they were run from a scratch copy that has since been removed.

## Tool/record

No tools installed or upgraded. Scratch `/fast/scratch/hyaku/tsukuroi-r51/R51ConnOverlap/` removed after copying receipts (`/fast` 430 G free at time of copy).
