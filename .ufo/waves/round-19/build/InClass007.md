# InClass007 — inbound census IN-007..IN-012 (kaidoku source)

Model: commandcode/deepseek/deepseek-v4.1-flash.

**Counts [obs]:** RESOLVES 6, DRIFTED 0, UNRESOLVABLE 0. Scope: operative 0, historical 6 — every sibling path lives under kaidoku `.ufo/waves/` at `d1d981d2cc04`. Consequently there are **no operative DRIFTED/UNRESOLVABLE pointers** and no owner handoff packets from this slice.

**Per id [obs]** (all against current `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md`, 106 lines; `…/round-12/PackageBlind.md`, 289 lines):
- IN-007 `luna-round-6/K1.md:9` → `8-24,35-37`: ownership at PROVINCE.md:8; refusal at :25-28 and kama routing ADJ-01 at :46 fall outside this pointer's spans (present, precision only).
- IN-008 `round-15/w1/SiblingBoundary.md:22` → `8-14,25-28,51`: owns :8, refusal :26, ADJ-06 :51.
- IN-009 `SiblingBoundary.md:255` → `25-28`: quoted block still verbatim at :25-28; evidence :26.
- IN-010 `round-17/w1/ConnSiblingOverlap.md:15` → `:26`: exact; sentence's `:51` and `:79-80` also intact.
- IN-011 `round-17/w1/ConnSiblingOverlap.md:30` → `PackageBlind.md:110`: mtree `./.BUILDINFO` line exact; sibling's second ref `:140` intact.
- IN-012 `round-18/w1/ConnSiblingOverlap.md:39` → `:79`: quote exact, continuation at :80.

**Retained rejection:** I considered IN-007 DRIFTED (paraphrase's refusal/routing clauses resolve at :25-28/:46, not its cited 35-37). Rejected: cited 8-24 holds the relied-on ownership text and 35-37 is the Adjacent section head, so the pointer is imprecise, not drifted.

**History [obs]:** `git log -L` last-touch commits: 459e3ce (8-24), aea5fa2 (25-28 creation), 9b70381 (35-37,79); no line-number shift explains any citation.

Undecided records: none. Draft: `.ufo/waves/round-19/build/drafts/InClass007.inbound.json` (schema-validated: exact keys, quotes are substrings of found_line, found_line inside target_ranges).

Scope: executed=python3 -c (census JSON extract), nl -ba PROVINCE.md | sed -n '1,90p', git -C tsukuroi-shokunin log -L8,24 / -L25,28 / -L35,37 / -L79,79:PROVINCE.md --format=%h, git -C kaidoku-shokunin show d1d981d2cc04:{.ufo/waves/luna-round-6/K1.md,.ufo/waves/round-15/w1/SiblingBoundary.md,.ufo/waves/round-17/w1/ConnSiblingOverlap.md,.ufo/waves/round-18/w1/ConnSiblingOverlap.md} | nl | sed, sed -n on PackageBlind.md, grep -n PackageBlind.md, ls sibling snapshot dir, python3 -c (draft schema/quote validation)
