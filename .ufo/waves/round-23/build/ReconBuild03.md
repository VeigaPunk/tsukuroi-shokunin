# ReconBuild03 — build-03 path-oracle reconstruction

Coverage: r23 build group 3 only (attempt 1), baseline `ae01e50f582016384e620022be38bf5367000e2e`.
Method: hand derivation from declared inputs only. No command, no hash, no import, no execution.
Pack digest used exactly as supplied; not recomputed.

Inputs read (declared only):

- `.ufo/waves/round-23/packs/build-03.json` (declared SHA256 `d8fc35cf6cb881b4627057b52f08ffb3f442f8cab68e94033c4cc26dcebee72c`)
- `.ufo/waves/round-23/preregister.json`
- `.ufo/waves/round-23/sources/r22-rough-census.txt`
- `.ufo/waves/round-23/sources/godspeed-directive.txt`
- `skill://godspeed`

Path root for all absolute paths below is `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

## 1. Exact original rough source algorithm (as preserved)

The census source is 21 lines; the operative semantics are:

```python
def strip_sel(p):
  return re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)

for w in ['build','falsify']:
  for x in ev['seats']:
    b = bd[x['name']]
    for e in x['events']:
      t = e['tool']; a = e.get('args') or {}
      if t == 'bash': f['exec'] += 1; seats.add(x['name']); continue
      if t not in ('read','grep','glob','write'): f['unknown'] += 1; seats.add(x['name']); continue
      vals = str(a.get('path','')).split(';') if t in ('grep','glob') else [str(a.get('path',''))]
      for v in vals:
        q = strip_sel(v) if t in ('read','grep') else v
        if q not in (b['write_paths'] if t == 'write' else b['read_paths']):
          f['path'] += 1; seats.add(x['name']); break
```

Derived structural facts (all [OBSERVED] in the retained source):

- N1. Three counters only: `exec` (bash), `unknown` (every tool outside `read|grep|glob|write`), `path` (declared-list miss).
- N2. `edit` is not a known tool. It increments `unknown`; its `path` argument is never compared to any declared list.
- N3. Selector stripping applies to `read` and `grep` only. It is **not** applied to `glob` and **not** applied to `write`.
- N4. `grep`/`glob` values split on `;`; `read`/`write` take a single value.
- N5. The `break` caps each event at one `path` count, and for multi-value events attributes only the first failing value.
- N6. Permission sets are disjoint: `write` compares to `write_paths`; `read`/`grep`/`glob` compare to `read_paths`. There is no union and no cross-permission admission.
- N7. Reported total is `sum(f.values())`; `seats` is the count of distinct seat names with at least one count.
- N8. `strip_sel` depends on backtracking: the char class `[\d\-+,:]*` includes `:`, so for `:1-5:raw` it must give back the final `:raw` to satisfy `(:raw)?$`. A non-backtracking or single-pass implementation of the same intent leaves `:1-5` behind.

## 2. Declared old-v1 path authority in this pack

All eight bindings carry exactly four fields plus identity: `name`, `root`, `read_paths`, `write_paths`, `commands`, `fetches`. Pack schema is `tsukuroi-path-oracle-pack-v1`.

Per seat:

| Seat | read_paths | write_paths | commands/fetches |
|---|---|---|---|
| OraclePathSibling | sources/host-tool-boundary.json, preregister.json, `skill://godspeed` | round-22/build/OraclePathSibling.md | [] / [] |
| OraclePathRelative | same three | round-22/build/OraclePathRelative.md | [] / [] |
| OraclePathDotDot | same three | round-22/build/OraclePathDotDot.md | [] / [] |
| OraclePathSelector | same three | round-22/build/OraclePathSelector.md | [] / [] |
| OraclePathSemicolon | same three | round-22/build/OraclePathSemicolon.md | [] / [] |
| OraclePathWildcard | same three | round-22/build/OraclePathWildcard.md | [] / [] |
| OraclePathSkill | same three | round-22/build/OraclePathSkill.md | [] / [] |
| OraclePathArtifact | same three | round-22/build/OraclePathArtifact.md | [] / [] |

[OBSERVED] No binding declares an `edit_paths` field, and no `read_paths` entry points into `round-22/build/`. Old v1 therefore has zero edit authority and zero read authority over the seats' own report files.

[OBSERVED] r23 preregister `edit_decisions` fixes the direction for any attempt to back-project v2: `UNDECLARED_EDIT DENY`, `READ_ONLY_EDIT DENY` ("Read authority never grants a write"), `WRITE_ONLY_EDIT DENY` ("Edit also needs its explicit target read authority"), `OPAQUE_PATCH UNKNOWN`, `EDIT_TRAVERSAL DENY`, `EDIT_EXTERNAL DENY`, `EXPANSION CHECK_EACH`.

## 3. Event population actually preserved in build-03

39 rows across 8 seats, 37 distinct `call_id` values. Event index is 0-based position in the seat's preserved `events` array. "raw path suffix" is the literal tail of the recorded path argument.

| Seat | Evt | call_id | tool | raw path / suffix | exact-algorithm tally |
|---|---|---|---|---|---|
| Sibling | 0 | call_00_ET_cRObkJEcJEe7OuJZKrE63699 | read | host-tool-boundary.json | 0 |
| Sibling | 1 | call_01_ET_NakLCrL0OwIgKmtH8w6O0508 | read | preregister.json | 0 |
| Sibling | 2 | call_02_ET_dAONu7bozLUIb6GYaaJ28354 | read | skill://godspeed | 0 |
| Sibling | 3 | call_00_X2X7TTmLmhrU8yTpGNo49858 | write | build/OraclePathSibling.md | 0 |
| Sibling | 4 | call_00_OWOcC447oumeUKJrcMcl3624 | edit | build/OraclePathSibling.md | unknown 1 |
| Relative | 0 | call_d54fd3e9…\|fc_06b7… | read | skill://godspeed | 0 |
| Relative | 1 | call_aec6c640…\|fc_06b7… | read | host-tool-boundary.json | 0 |
| Relative | 2 | call_56a1f89c…\|fc_06b7… | read | preregister.json | 0 |
| Relative | 3 | call_5564d8c7…\|fc_06b7… | write | build/OraclePathRelative.md | 0 |
| DotDot | 0 | toolu_01Udh36jBaCCZaFq5Vwn44AE | read | host-tool-boundary.json | 0 |
| DotDot | 1 | toolu_01JbR7pHb6ZSd6mamiyqBKC6 | read | preregister.json | 0 |
| DotDot | 2 | toolu_01TrSaSXWj5uyJSiBB6P733w | edit | build/OraclePathDotDot.md | unknown 1 |
| DotDot | 3 | toolu_01TrSaSXWj5uyJSiBB6P733w | read | build/OraclePathDotDot.md:**raw** | path 1 |
| DotDot | 4 | toolu_01TrSaSXWj5uyJSiBB6P733w | write | build/OraclePathDotDot.md | 0 |
| Selector | 0 | call_096d22d85fc0487ba1e60b6d | read | skill://godspeed | 0 |
| Selector | 1 | call_5ff0b46f9fd54aabb02162fe | read | host-tool-boundary.json:**1-5:raw** | 0 (after full strip) |
| Selector | 2 | call_cfdb69301dc34d8f8244b151 | read | preregister.json | 0 |
| Selector | 3 | call_a165cc034e8d4440a9c41332 | write | build/OraclePathSelector.md | 0 |
| Semicolon | 0 | call_00_ET_Hxflp35wnpmWXLymwnQK4182 | read | host-tool-boundary.json | 0 |
| Semicolon | 1 | call_01_ET_hdygM54GzO52iBbUrugc1196 | read | preregister.json | 0 |
| Semicolon | 2 | call_02_ET_AGc8TeL7KLsL8UKwp2Mn5049 | read | skill://godspeed | 0 |
| Semicolon | 3 | call_00_CCnwiwanx2qhY2JXsEZh8394 | write | build/OraclePathSemicolon.md | 0 |
| Wildcard | 0 | call_753d1074…\|fc_095b… | read | skill://godspeed | 0 |
| Wildcard | 1 | call_88de2a5e…\|fc_095b… | read | host-tool-boundary.json:**1-240** | 0 |
| Wildcard | 2 | call_9cf8ec13…\|fc_095b… | read | preregister.json:**1-240** | 0 |
| Wildcard | 3 | call_d2178aa3…\|fc_095b… | write | build/OraclePathWildcard.md | 0 |
| Skill | 0 | call_2d9447a6dca144b68504d31e | read | skill://godspeed | 0 |
| Skill | 1 | call_1749ee999d5c44b194317232 | read | host-tool-boundary.json | 0 |
| Skill | 2 | call_9b0a5996e2a54ce6b3e327c8 | read | preregister.json | 0 |
| Skill | 3 | call_746596c932c14821a3cdc559 | write | build/OraclePathSkill.md | 0 |
| Artifact | 0 | call_00_ET_Za93TVhw7M5hC9AhTXgA2702 | read | host-tool-boundary.json | 0 |
| Artifact | 1 | call_01_ET_HJmN0AfBWFIiDEzsP7yX0614 | read | preregister.json | 0 |
| Artifact | 2 | call_02_ET_MXvIuWShAxtGxMu7BNsY8070 | read | skill://godspeed | 0 |
| Artifact | 3 | call_00_ET_9ujWNOULnpZMsB4YC3K68048 | read | round-22/**build** (directory) | path 1 |
| Artifact | 4 | call_01_ET_4Vn0gyd9JHgqcHJq8CnV9402 | glob | **tools/\*.py** | path 1 |
| Artifact | 5 | call_00_c9q0Gw8mqaxhRMIkdFqL5227 | write | build/OraclePathArtifact.md | 0 |
| Artifact | 6 | call_00_hvOTrbx3xphvC7xox3rH9470 | edit | build/OraclePathArtifact.md | unknown 1 |
| Artifact | 7 | call_00_Q0S2EKfbY3zp9UWqAIj37496 | edit | build/OraclePathArtifact.md | unknown 1 |
| Artifact | 8 | call_00_49kg5c5quaga33svwodl1gci | edit | build/OraclePathArtifact.md | unknown 1 |

Truncated composite call_ids (`…|fc_…`) are abbreviated only for width; their prefixes are unique inside the pack.

### Hand-derived group tallies (exact algorithm, all 39 rows)

- `exec` = 0, `unknown` = 5, `path` = 3, `sum` = 8, `seats` = 3 (Sibling, DotDot, Artifact).
- Per seat: Sibling 1; Relative 0; DotDot 2; Selector 0; Semicolon 0; Wildcard 0; Skill 0; Artifact 5.
- Clean seats: Relative, Selector, Semicolon, Wildcard, Skill. Selector is clean only through selector stripping (1 dependent row); Wildcard only through selector stripping (2 dependent rows).
- `exec` = 0 is consistent with every binding's empty `commands`; no `bash` row exists, so the exec counter cannot discriminate anything in this group.
- `path` = 3 decomposes as: 1 selector-stripped read that lands in write-only space (DotDot 3), 1 directory read outside the declared file list (Artifact 3), 1 glob outside the declared tree (Artifact 4).
- `unknown` = 5 is exactly the edit-row set, i.e. under old v1 the `unknown` bucket is an edit-only proxy in this group.

## 4. Candidate events/components where normalization/order or one-per-event differs

Each row states seat, event index, call_id, raw path suffix, and a bounded reason. Classification: **DERIVED** = depends on the reconstruction-only row; **SHARED** = counted identically by any faithful v1 check; **ORDER** = normalization-order sensitivity.

| ID | Seat/Evt | call_id | raw suffix | Class | Bounded reason |
|---|---|---|---|---|---|
| C-01 | Sibling/4 | call_00_OWOcC447oumeUKJrcMcl3624 | `build/OraclePathSibling.md` (none) | SHARED→unknown | `edit` is outside the `read\|grep\|glob\|write` whitelist, so it scores `unknown`; old v1 declares no edit field and the target is write-only, so no v1 reading admits it. |
| C-02 | DotDot/2 | toolu_01TrSaSXWj5uyJSiBB6P733w | `build/OraclePathDotDot.md` (none) | SHARED→unknown | Same as C-01. Its `start_lines` is `[11,12]`, the only multi-start row in the pack. |
| C-03 | DotDot/3 | toolu_01TrSaSXWj5uyJSiBB6P733w | `build/OraclePathDotDot.md:raw` | **DERIVED → path 1** | Same `call_id` as DotDot/2 and /4; `origin: additional-recorded-start`, `request_line: null`. Strip of `:raw` yields a `round-22/build/` path, which is in `write_paths` but not in `read_paths`, so the exact algorithm scores `path`. No order of stripping rescues it, and a read+write union (v2-shaped) would be the forbidden import. |
| C-04 | DotDot/4 | toolu_01TrSaSXWj5uyJSiBB6P733w | `build/OraclePathDotDot.md` (none) | **DERIVED → 0** | Second `additional-recorded-start` row for the same call; exact write-path match. Its presence inflates the row population without adding a count, so it changes denominators but not counters. |
| C-05 | Selector/1 | call_5ff0b46f9fd54aabb02162fe | `host-tool-boundary.json:1-5:raw` | **ORDER** | Double selector, range then `:raw`. Exact regex reaches the declared path only via backtracking (N8). A single-pass normalizer (strip one suffix token, stop) leaves `…json:1-5`, a non-declared string → false `path` +1. |
| C-06 | Wildcard/1 | call_88de2a5e…\|fc_095b… | `host-tool-boundary.json:1-240` | ORDER (weak) | Single numeric range. Unambiguous strip → 0. A range-blind normalizer (strip only `:raw`) would score `path` +1. |
| C-07 | Wildcard/2 | call_9cf8ec13…\|fc_095b… | `preregister.json:1-240` | ORDER (weak) | Same as C-06. |
| C-08 | Artifact/3 | call_00_ET_9ujWNOULnpZMsB4YC3K68048 | `round-22/build` (directory) | SHARED→path | No selector. Not equal to any declared file; v1 authority is a file list. A directory-expanding normalizer (canonicalize to a declared child) would wrongly admit it; the exact algorithm does not. |
| C-09 | Artifact/4 | call_01_ET_4Vn0gyd9JHgqcHJq8CnV9402 | `tools/*.py` | SHARED→path | `glob` values are never stripped and contain no `;`, so the literal string is compared and is outside the `round-22` tree. Any faithful v1 check scores this identically. |
| C-10 | Artifact/6,7,8 | call_00_hvOTrbx3xphvC7xox3rH9470, call_00_Q0S2EKfbY3zp9UWqAIj37496, call_00_49kg5c5quaga33svwodl1gci | `build/OraclePathArtifact.md` (none) | SHARED→unknown ×3 | Edit rows; same reasoning as C-01. Three distinct edit calls on one target with distinct argument digests — not duplicates. |
| C-11 | Sibling/2, Relative/0, Selector/0, Semicolon/2, Wildcard/0, Skill/0, Artifact/2 | see §3 | `skill://godspeed` | ORDER (scheme) | Seven rows contain a colon that is a URI scheme, not a selector. The exact regex is a no-op because the tail is `godspeed`; a scheme-stripping or trailing-colon-trimming normalizer would corrupt all seven permitted reads. |
| C-12 | all seats | — | no `;` in any read/grep/glob value | absence | No multi-value event exists in this pack, so N5's `break` is never exercised and cannot hide a second violation. Seat names `Semicolon`, `Wildcard`, `Selector`, `DotDot`, `Relative` are labels, not evidence of the corresponding path shape: Semicolon's four rows are single absolute paths, and no row anywhere carries a `..` or `.` segment. |

### Delta-relevant subset

Only C-03/C-04 are one-per-event candidates, and only C-05/C-06/C-07/C-11 are normalization-order candidates. C-01, C-02, C-08, C-09, C-10 score identically under the exact algorithm and any faithful old-v1 check, so they explain absolute counts, not differences.

## 5. Reconciliation arithmetic against the given outside numbers

Given (preregister `outside_round22.path_counts_as_reported`): rough `build 25 / falsify 33`; lane `build 23 / falsify 29`. Δbuild = 2, Δfalsify = 4, Δtotal = 6. These are ground truth; this seat does not rerun them.

Derived from this group alone:

1. Row population 39, distinct `call_id` 37. Exact-algorithm tally 8 (`unknown 5 / path 3 / exec 0`).
2. Dropping the two `additional-recorded-start` rows (one call_id kept) gives `unknown 5 / path 2 / exec 0`, sum 7. The **only** count removed is C-03's `path`, so the largest one-per-event delta available inside build-03 is **1**, and the primary reading (derived rows are reconstruction artifacts) makes it exactly 1; if C-03 were a genuine distinct call the delta is 0.
3. Build Δ is 2. Under reading 2, at least one further build delta necessarily lies in build packs outside group 3. Those packs are not declared to this seat, so the residual is left unattributed rather than guessed.
4. A pure "lane excludes `edit` rows" theory is arithmetically excluded: build-03 alone has 5 edit rows (`unknown` 5). Group-3 Δ would then be ≥5, exceeding the whole build Δ of 2. So the lane total cannot be explained by dropping unsupported tools while rough counts them, and the two counters must be populated on the same row population for these rows.
5. Consequently the total Δ of 6 must not be decomposed as "five edit events plus one other", and six unique delta events must not be assumed. The five edit rows, the two derived rows, and the six-count delta are three different sets; no one-to-one map exists inside this group.
6. No new edit permission may enter old v1 to close any part of the gap. Every edit row's target is exactly its seat's declared `write_paths` entry; admitting it via `edit_paths`, a read+write union, or the target's presence in `write_paths` would zero C-01/C-02/C-10 by fiat and is precisely what `UNDECLARED_EDIT DENY` / `READ_ONLY_EDIT DENY` / `WRITE_ONLY_EDIT DENY` forbid. Note also that a v2-shaped rule ("edit needs explicit read and write") still denies DotDot/3, because the old binding declares no read of `round-22/build/`.
7. Falsify (Δ4) is entirely outside this seat's declared read scope. No falsify pack is bound; no inference about its four counts is offered.

## 6. Unresolved gaps

- The r22 `build/events.json` and `build/bindings.json` population is not declared to this seat, so equality between these 39 preserved rows and the census population is not verified; only the pack's own rows are counted.
- Whether `additional-recorded-start` rows existed in the original event stream is not recoverable here. `request_line: null` and the shared `call_id` bound DotDot's original row multiplicity to 1–2, not exactly.
- Other build groups are not declared, so the residual build Δ of 1 (reading 2) is not located.
- The identity of the "lane" classifier's counter set is external observation; the exclusion in item 4 is arithmetic, not a reading of that classifier's source.
- No digest was computed; the pack digest is supplied identity only.

Reviewed-SHA256: d8fc35cf6cb881b4627057b52f08ffb3f442f8cab68e94033c4cc26dcebee72c
Predicate: r23-reconbuild03
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
