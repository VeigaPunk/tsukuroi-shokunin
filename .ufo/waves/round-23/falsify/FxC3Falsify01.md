# FxC3Falsify01 — C3 path-census ledger, slice falsify-01 (group 1)

Seat: FxC3Falsify01 (leaf). Wave falsify. Landed revision 5a25c88b77f52e940bcad87825c4ac1cd529470d.
Slice: `.ufo/waves/round-23/candidate/ledger-slices/falsify-01.json` (8 seats, 108 rows).
Reviewed-SHA256 identity is the seat-supplied declaration; it was not recomputed.

Axes walked: (A1) rough row faithfulness to the S085 source; (A2) canonical component
faithfulness under literal v1 authority plus the selector grammar; (A3) disposition
coherence with A1/A2; (A4) claim impact (C3, then C1/C2 only where the slice touches them).
Every move was read-only inside the declared read set; no row was rewritten.

## Verdict

**0 of 108 rows disputed.** Every row's seat, index, tool, call_id and
`request_arguments_sha256` matches the corresponding raw pack event in
`.ufo/waves/round-23/packs/falsify-01.json`, and every rough/canonical/disposition value
re-derives exactly from the event spelling and the seat binding.

Rows not both clean and `agree` (all re-derived, none disputed): 6 — four disposition
`selector-normalization`, one canonical path component, one tool-class `unknown`. Listed
below with the driving path spelling.

## Rules used (re-derived from the bound sources, not assumed)

S085 rough census (`sources/r22-rough-census.txt`, source data only):

    strip_sel(p) = re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$', '', p)
    bash                        -> bucket "exec", seat flagged, path skipped
    tool not in {read,grep,glob,write} -> bucket "unknown", seat flagged, path skipped
    grep/glob path              -> split on ';'
    read/grep component         -> strip_sel, then literal membership in read_paths
    write component             -> literal membership in write_paths (no strip_sel)
    first non-member component  -> bucket "path" += 1, first bad index recorded, break

So at most one path component is recorded per event; `rough_path_count` is 0 or 1,
`rough_first_bad` is that component index or null. `exec` and `unknown` leave both path
fields null and zero.

Literal v1 authority + selector grammar (canonical side): compare each path component
literally against `read_paths` (read/grep/glob) or `write_paths` (write) after removing one
complete trailing selector. The read/grep selector grammar admits both orders, `:N-M:raw`
and `:raw:N-M` (system `read` selector: `:2-4:raw` or `:raw:2-4`); `strip_sel` recognizes
only the first order, plus a bare trailing `:raw` or numeric range/list. That asymmetry is
the only unit difference in this pack. `canonical_bad` is the ordered list of non-member
component indices; `canonical_path_count` its length.

Disposition [INFERENCE — the slice schema binds no definition]: `agree` exactly when the
rough path set and canonical path set coincide (both empty, or same single index);
`selector-normalization` when rough records one bad component and canonical records none
because the full selector grammar resolves the same spelling to a declared base. This rule
reproduces all 108 rows without exception, including the `unknown` row, whose path sets are
both empty.

## Per-seat re-derivation (events / rows / rough flags / canonical flags)

| seat | events=rows | rough path | rough unknown/exec | canonical path | dispositions |
|---|---|---|---|---|---|
| FxC1NoExec | 11 | 0 | 0 | 0 | all agree |
| FxC1NoFetch | 17 | 0 | 0 | 0 | all agree |
| FxC1LocalRead | 16 | 0 | 0 | 0 | all agree |
| FxC1ReportWrite | 8 | 1 | 1 | 1 | agree x8 |
| FxC1Unknown | 16 | 4 | 0 | 0 | agree x12, selector-normalization x4 |
| FxC1Dead | 11 | 0 | 0 | 0 | all agree |
| FxC1Duplicate | 14 | 0 | 0 | 0 | all agree |
| FxC1Hidden | 15 | 0 | 0 | 0 | all agree |

All eight bindings declare the same eight read paths and one seat-specific write path;
`commands` and `fetches` are empty for all. There is no bash event and no glob event in the
pack, so the `exec` bucket is empty and no glob path (which S085 does not selector-strip)
exists. Multi-path grep rows split cleanly: `FxC1NoFetch:15`
(`preregister.json;host-tool-boundary.json`) and `FxC1Hidden:11` (four `;`-joined declared
paths) are clean; the break rule never fires on them. Every write row targets the seat's own
declared report path. Every read/grep row other than the four listed below is a declared
base path optionally followed by `:N-M`, `:N-M:raw`, `:raw`, or a numeric comma list, all
fully stripped by `strip_sel`.

## Rows that are not both clean and agree (checked, none disputed)

1. **FxC1ReportWrite:5** — call_id `toolu_01SKTuRKNxh7ui6itpAk2oCi` — tool `edit`.
   Pack args: path `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxC1ReportWrite.md`
   plus `__unknown_argument__: null`. S085: `edit` is outside {read,grep,glob,write}, so it
   is bucket `unknown`, path skipped -> `rough_category=unknown`, `rough_first_bad=null`,
   `rough_path_count=0`. Canonical v1 path authority has no edit class, so no path component
   exists -> `canonical_bad=[]`, count 0; the empty/empty path-set equality yields `agree`.
   Recorded row is faithful. This row is **not** an authorization or cleanliness verdict:
   the target is declared only in `write_paths` and the captured request carries no
   structured body, so under C1's decision table the same event is WRITE_ONLY_EDIT (DENY)
   and OPAQUE_PATCH (UNKNOWN). The path ledger records the tool class in `rough_category`
   and has no component to add, which matches C2's disclosed "body data opaque" limit.

2. **FxC1ReportWrite:6** — same call_id (pack origin `additional-recorded-start`) — tool
   `read`. Path spelling `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxC1ReportWrite.md:raw`.
   `strip_sel` removes `:raw`, leaving the seat's **write-only** report path; it is not in
   `read_paths`, so rough flags component 0. Canonical literal v1 says the same, `canonical_bad=[0]`,
   retained 1. Both sides flag the same component -> `agree`. Correct.

3. **FxC1Unknown:8** — call_id `toolu_01SCLctdiGzTL9cNPCdfjFYW` — tool `read`. Path spelling
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-boundary-contract.py:raw:15-60`.
   `strip_sel` can match only the trailing `:15-60` (its alternation cannot consume `raw`
   followed by `:15-60`), leaving `...check-boundary-contract.py:raw`, which is not declared
   -> rough component 0. The selector grammar accepts `:raw:15-60`, base is declared ->
   `canonical_bad=[]`. Disposition `selector-normalization`. Correct.

4. **FxC1Unknown:9** — call_id `toolu_01ASiJwaeMcZrphAZyuTztc3` — same base,
   `...check-boundary-contract.py:raw:58-102`. Identical asymmetry, same disposition.

5. **FxC1Unknown:10** — call_id `toolu_01K3ih69GpJx5agmk4hChSei` — same base,
   `...check-boundary-contract.py:raw:103-175`. Identical asymmetry, same disposition.

6. **FxC1Unknown:14** — call_id `toolu_01R72arcerJspPr3z3wvNHRL` — path
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/_revision.py:raw:172-193`.
   Identical asymmetry, same disposition.

Contrast that isolates the unit difference: **FxC1LocalRead:11**
(`...check-boundary-contract.py:54-95:raw`, call_id `toolu_00_b7bn...` = `toolu_00_b7bn5z4jsr80nkfd4cwcvtpi`)
and **FxC1LocalRead:12** (`...:104-145:raw`, call_id `toolu_01_niae036lblvxmm830w2deoor`) use
the range-then-raw order. `strip_sel` consumes the whole selector there, both classifiers
see the declared base, and both rows are clean/`agree`. The four `selector-normalization`
rows are the mirror spelling; no other divergence class exists in this pack.

## Attacked claim, falsifier, bounded search, remedy

**Claim attacked: C3** (`unexplained_cohorts` 2 -> 0; both frozen r22 cohorts exhaustively
explained per event and component, with the declared rough/lane arithmetic), scoped to this
slice's group-1 pack. C1 and C2 are touched only by the single `edit` event, which exercises
neither the eight-decision contract nor the v2 audit in this historical capture.

**Falsifier sought:** any row whose rough category/first-bad/count, canonical components, or
disposition cannot be reproduced from the raw event spelling and binding, or any row keyed
to the wrong event.

**Bounded search (found none):** all 8 seats, 108 events and 108 rows. For each row I
matched seat, index, tool, call_id and the supplied `request_arguments_sha256` against the
pack event (all 108 match; repeated argument sets reuse the same digest as expected), then
replayed the S085 loop by hand on each path spelling (tool class, `;` split, `strip_sel`,
read/write table, break), then applied literal v1 membership with full selector
normalization, then the disposition rule above. The census's `exec` and `unknown` buckets
were checked explicitly: empty and one event respectively. No row diverges.

**Smallest in-scope remedy: none.** No ledger row or count needs changing. The
`FxC1ReportWrite:5` row is the only place where a reader could over-read `agree` as
"authorized": the row records a tool-class `unknown` with no path component, and the
WRITE_ONLY_EDIT/OPAQUE_PATCH verdict belongs to C1/C2, not to this v1 path ledger. If the
wave later wants tool-axis disposition in the ledger, that is a new C2-owned field, not a
C3 row repair, and it is out of this slice's declared scope.

## Residual unknowns

- `disposition` and `retained_path_count` have no schema definition inside the declared read
  set; their semantics here are inferred from perfect co-variation across all 108 rows
  (`retained_path_count == canonical_path_count` in every row). Confidence: high for the
  values, medium for the names.
- The outside cohort arithmetic (rough falsify 33, lane falsify 29) is supplied ground truth
  and cannot be recomputed from this slice, whose declared scope is "exact rows ... not a
  recomputation". Group 1 contributes 5 rough path flags, 1 rough tool-unknown and 1
  canonical path flag; how the remaining packs close the 4-count difference is not visible
  in this file.
- C1/C2 remain unexercised here beyond the one opaque, write-only-target edit event; this
  slice supplies no falsifier for either.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: 956548eda9256794e2d8dc6b47ee6f8ac592f7dd01fb9f60e294662068b586de
Predicate: r23f-fxc3falsify01
Scope: executed=none
