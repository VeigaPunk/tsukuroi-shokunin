# FxC3Falsify05 — C3 path-census ledger, falsify group 5

- Slice: `.ufo/waves/round-23/candidate/ledger-slices/falsify-05.json` (declared SHA256 1616eca02ad88f73bb295fdfe25b56c959763efc3a856d0112cdd92e79511a50, supplied identity)
- Pack: `.ufo/waves/round-23/packs/falsify-05.json` (8 seats, 121 events)
- Landed: 5a25c88b77f52e940bcad87825c4ac1cd529470d; baseline ae01e50f582016384e620022be38bf5367000e2e
- Source rules: `.ufo/waves/round-23/sources/r22-rough-census.txt` (S085), `.ufo/waves/round-23/preregister.json`, pack bindings

## Attacked claim

C3 (`unexplained_cohorts`, calibration): every row of the landed path-reconciliation ledger for
this pack is an exhaustive per-event/component explanation of rough-versus-lane path counts with
frozen digests and declared arithmetic. Secondary: the r23 C1/C2 edit-authority contract must not
be retroactively applied to these historical v1 rows, and a clean row must not secretly hide a
violation.

Falsifier shape: recompute, for each of the 121 rows, the rough category / first bad component /
rough path count from the raw event under the exact S085 code, the canonical bad components under
literal v1 read/write authority plus the selector grammar, and the disposition; any disagreement
falsifies the row.

## Exact rules applied (from the supplied S085 source)

- Value extraction: `read` = one value; `grep`/`glob` = `str(path).split(';')`; `write` = one raw value.
- Selector stripping, only for `read` and `grep`: `re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$', '', path)`.
- Buckets: `bash` -> exec; any tool outside read/grep/glob/write -> unknown; otherwise compare each
  value to the seat's `read_paths` (read/grep/glob) or `write_paths` (write, no stripping), and on
  the first unauthorized value increment path once and `break` (max one path count per event).
- The census print sums all buckets (`sum(f.values())`), so unknown/exec events contribute to the
  reported total with zero path count.

Alignment check: seat row indices are contiguous and 1:1 with pack event order for all 8 seats
(19+14+16+8+17+7+20+20 = 121 rows, 121 events). No `bash` and no `glob` events occur in this pack,
so the exec bucket and the glob-no-strip branch are unexercised here.

## Result: no disputed row

All 121 recorded tuples (rough category, rough first bad, rough path count, canonical bad,
canonical path count, disposition) match hand re-derivation. There is no `disagree` disposition
in the slice (searched).

Per seat: rows / clean / path / unknown

- FxC2BindingRoot 19 / 17 / 1 / 1
- FxC2BindingDuplicate 14 / 13 / 1 / 0
- FxC2TraceMissing 16 / 16 / 0 / 0
- FxC2TraceIncomplete 8 / 6 / 1 / 1
- FxC2TraceIdentity 17 / 17 / 0 / 0
- FxC2ZeroTrace 7 / 7 / 0 / 0
- FxC2Symlink 20 / 20 / 0 / 0
- FxC2DenialWording 20 / 19 / 1 / 0
- Total 121 / 115 / 4 / 2

## Non-clean rows checked (all six agree; path spelling that drove each)

1. **FxC2BindingRoot:6** — `call_6aa3b9339f2f400da067739e`, tool read.
   Path spelling: `/home/vgvgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-review-snapshots.py`
   The second path segment is `vgvgpnk` (double `vg`), not the seat root `vgpnk`; the string is not
   a member of the eight declared read paths. Rough path / first bad 0 / count 1; canonical bad
   `[0]` / count 1. Agree. The typo occurs exactly once in the pack (searched), so no second row is
   affected. Robust to selector grammar (the base is unauthorized even unstripped).
2. **FxC2BindingDuplicate:13** — `call_00_3PTLgRhIoKqsgG58rCm67313`, tool grep.
   Path: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxC2BindingDuplicate.md`
   Grep authority is read-only; the report markdown is only in `write_paths`, so v1 denies the read
   (write never grants read). Rough path / 0 / 1; canonical `[0]` / 1. Agree.
3. **FxC2TraceIncomplete:6** — `toolu_01BEnxrQaxyx9n1bMVywRn6t`, tool read.
   Path: `…/round-22/falsify/FxC2TraceIncomplete.md:raw`; `strip_sel` removes `:raw` to the
   write-only report path. Rough path / 0 / 1; canonical `[0]` / 1. Agree. This row and row 7 are
   pack `additional-recorded-start` entries sharing the edit call id of row 5; the ledger's declared
   unit is per event, and it does not dedupe.
4. **FxC2DenialWording:19** — `call_00_jbmhmo9znhjtebvn2tdi5kmj`, tool read.
   Path: `…/round-22/falsify/FxC2DenialWording.md:-8`; the negative selector `:-8` is stripped by
   the `-\d+` alternative, leaving the write-only report path. Rough path / 0 / 1; canonical `[0]`
   / 1. Agree.
5. **FxC2BindingRoot:18** — `call_fd36d54f7d134c1e99e54b9e`, tool edit. Edit is outside v1's
   tool set, so S085 yields unknown with no path value inspected; canonical bad `[]` / 0. Agree.
   The row carries no v2 edit verdict (correct: v1 historical event).
6. **FxC2TraceIncomplete:5** — `toolu_01BEnxrQaxyx9n1bMVywRn6t`, tool edit. Same unknown class;
   canonical `[]` / 0. Agree.

Verdicts 2–4 are grammar-robust: even if the selector were not stripped, the full string is absent
from `read_paths`, so canonical `[0]` would not change. Verdict 1 is spelling-driven and also
grammar-independent.

Clean-adjacent row specifically checked: **FxC2DenialWording:10** (`call_00_Bnmr2xR4hxaDay5k25GJ7835`,
grep) carries a five-component `;`-joined path string (check-seat-bindings.py; seat-boundary-r22.json;
seat-boundary-r22.md; preregister.json; host-tool-boundary.json). S085 iterates all five, finds each
exactly in `read_paths`, never increments, so rough path count 0 — matching the ledger. A
per-token violation counter would wrongly report 5 and a "contains a separator" heuristic would
wrongly report 1; both are falsified for this row.

## Clean-class verification (115 rows)

- Every read/grep path equals a declared read path after `strip_sel`; every write path equals the
  seat's declared write path; the only non-path tools are the two edits (unknown).
- Selector forms actually exercised and stripped: `:N`, `:N-M`, `:N-M:raw`, `:N-M,K-L:raw`, `:raw`,
  and (on row 4 above) `:-N`. All match the declared regex at the end anchor.
- All 8 write rows are clean under v1 (`write_paths` membership alone).
- All 121 `request_arguments_sha256` values in the ledger equal the corresponding pack event value
  (transcription check, not recomputation).

## Bounded search / findings

- **F1 (row values):** exhaustive re-derivation over the whole slice found no falsifier.
- **F2 (digest declaration, no row impact):** identical displayed argument objects carry different
  frozen digests. Six `skill://godspeed` reads display `{path, i:null}` (or `{i:null, path}` for
  FxC2ZeroTrace:0) yet hash to four distinct values: `a2633e1a…` (BindingRoot:0), `2b4cad9d…`
  (BindingDuplicate:6, TraceMissing:3, DenialWording:0), `21e214c6…` (TraceIdentity:1), `2842d5da…`
  (ZeroTrace:0). Within FxC2BindingRoot, the three same-path greps (rows 13/14/15) display
  `{i:null, path, pattern:null}` but hash to `13da46a3…`, `94a418b8…`, `fcbc8193…`. Therefore the
  digest input contains values the pack displays as null; the displayed `i`/`pattern` are
  redactions. [INFERENCE: the hidden values are the real intent string and grep pattern.]
  [OBSERVED: the digests differ for identical displayed args.] No count depends on this — S085
  reads only `tool` and `path`, never `pattern`, and `i` is never consulted — and the ledger copies
  the digests faithfully. But any C3 wording that treats the digest as recomputable from, or as an
  equality proof over, the displayed arguments is falsified by these four values.
- **F3 (declared arithmetic):** in this slice `sum(rough_path_count) = 4`, while the census-style
  `sum(f.values()) = 6` (4 path + 2 unknown + 0 exec). The ledger's path-count field is the path
  bucket only; the reported cohort total must sum the category buckets. The global rough/lane pair
  (falsify 33 vs 29, build 25 vs 23) is not reproducible from one pack: the other falsify packs are
  outside this seat's read set. Bounded, not refused.
- **F4 (break rule):** no event in this slice has more than one unauthorized component, so S085's
  `break` is observationally identical to per-component counting here; the first-bad index is
  always 0 and is exercised only in the trivial single-component sense.
- **F5 (C1/C2 boundary):** the 8 write rows are clean under v1 write authority even though none of
  those seats has read authority for its own report. Under r23 C1's `WRITE_ONLY_EDIT` decision they
  would be DENY if the new contract were applied retroactively; the ledger correctly does not.
  Likewise the edit rows are v1-unknown, not v2 classes; under v2 the FxC2TraceIncomplete edit
  (target displayed, read absent) would be `WRITE_ONLY_EDIT` DENY, not `OPAQUE_PATCH`. No runtime
  enforcement is claimed or evidenced.

## Remaining unknowns

- The r22 v1 checker (`check-seat-bindings.py`) is not in this seat's declared read set, so
  "literal v1 authority" is instantiated from the pack binding arrays plus the S085 comparison
  rule. If that unopened checker uniquely allowed grep on `write_paths`, rows 2–4 would flip; the
  landed v2 decision set agrees with `[0]` (edit needs read+write; read-only never grants a write),
  so the landed values survive both readings. Recorded as a declared-scope gap, not improvised.
- Whole-cohort (33 vs 29) arithmetic requires the sibling packs.

## Smallest in-scope remedy

No ledger value requires change. Retain all 121 rows as landed. If the C3 reconciliation asserts
either digest recomputability from pack arguments or a naive equality between `rough_path_count`
sums and cohort totals, replace those two statements with the exact facts above (opaque digest over
redacted arguments; totals are the sum of path+unknown+exec buckets). No production, routing, or
VCS action from this seat.

Reviewed-SHA256: 1616eca02ad88f73bb295fdfe25b56c959763efc3a856d0112cdd92e79511a50
Predicate: r23f-fxc3falsify05
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
