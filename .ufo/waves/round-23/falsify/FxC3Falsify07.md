# FxC3Falsify07 — falsify ledger slice falsify-07 (group 7, eight r22 falsify seats)

Seat: FxC3Falsify07. Wave: falsify, round 23, attempt 1. Attacked claim: **C3** (path-census
ledger, `unexplained_cohorts` before 2 target 0). C1/C2/frontier are outside this slice and were
not attacked.

## Identity and method (observed)

- Slice: `.ufo/waves/round-23/candidate/ledger-slices/falsify-07.json`, schema
  `tsukuroi-path-reconciliation-slice-v1`, group 7, landed `5a25c88b77f52e940bcad87825c4ac1cd529470d`.
  Slice declares `scope: "Exact rows of the landed ledger for this pack; not a recomputation."`
- Pack: `.ufo/waves/round-23/packs/falsify-07.json`, eight seats, 133 events:
  FxC3Manifest 16, FxC3StrictUnavailable 15, FxC3Buckets 23, FxC3ReportDigest 11,
  FxC3StrictReuse 19, FxC3ReturnModes 9, FxC3CompletedError 15, FxC3Separable 25.
- Slice has 133 rows, same seat order; the flattened `call_id` sequences of pack and slice are
  identical element-for-element, including the three ReportDigest events that share
  `toolu_vrtx_01QMz3i1tGAnSkf1mFqqh5YT` (distinguished by tool and digest).
- All eight seats share the same eight `read_paths` (r22 cohort/tool/preregister/knowledge files
  plus `skill://godspeed`); each seat's sole `write_path` is its own r22 falsify report. No
  binding declares its own report in `read_paths`.
- Rough rule exercised is the S085 census rule quoted in
  `.ufo/waves/round-23/sources/r22-rough-census.txt`: tool not in `read|grep|glob|write` →
  `unknown` (bash → `exec`); `write` compared to `write_paths`; `read`/`grep` path split on `;`
  then selector-stripped with `re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`; `glob`
  compared unsplit; first failing component increments one `path` and the per-event loop breaks
  (so at most one path count per event, first-bad index recorded).
- Canonical rule exercised: literal v1 read/write authority over the same component grammar
  (`read`/`grep`/`glob` from `read_paths`, `write` from `write_paths`), no implicit allowance from
  generic report ownership.
- Digests were compared **as declared strings** only (pack `request_arguments_sha256` vs slice
  row `request_arguments_sha256`); none was recomputed, and no command was executed.

## Disputes

**None. 0 of 133 rows disputed.** Every recorded `rough_category`, `rough_first_bad`,
`rough_path_count`, `canonical_bad`, `canonical_path_count`, `retained_path_count` and
`disposition` re-derives from the raw pack events plus the seat bindings. Distribution:
125 `clean`, 5 `path`, 3 `unknown`, 0 `exec`; all 133 dispositions are `agree`.

Per-seat re-derivation (clean/path/unknown): Manifest 16/0/0; StrictUnavailable 13/2/0;
Buckets 21/0/2; ReportDigest 9/1/1; StrictReuse 19/0/0; ReturnModes 9/0/0;
CompletedError 15/0/0; Separable 23/2/0.

Independent in-reader recomputation of the S085 rule over all 133 pack events returned exactly
this non-clean set and first-bad indices, with no `bash` or `glob` events present.

## Non-agree (non-clean) rows checked, with the spelling that drove them

The slice stores component identity as an index into the event path list, not the path text; the
spellings below come from the frozen pack event at the same `(seat, index)`, cross-bound by
`call_id` and digest. All eight match.

Path rows (`rough_category=path`, `rough_first_bad=0`, counts 1/1/1, `canonical_bad=[0]`,
`disposition=agree`):

1. `FxC3StrictUnavailable:13` — `call_00_lW2RZGquuCoNo0r9Uvqs9303` — grep —
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxC3StrictUnavailable.md`
   (file is the seat's `write_path` only, never a `read_path`).
2. `FxC3StrictUnavailable:14` — `call_01_mXDvU88sDs3uYWY7rSKP3118` — read — same path plus
   `:-12`; S085 strips `:-12` via the `-\d+` alternative, leaving the same undeclared read base.
3. `FxC3ReportDigest:9` — `toolu_vrtx_01QMz3i1tGAnSkf1mFqqh5YT` — read —
   `…/round-22/falsify/FxC3ReportDigest.md:raw`; `:raw` stripped, base undeclared for read.
4. `FxC3Separable:23` — `call_00_lsPr2U9omuVvUg6fhxJA1900` — grep —
   `…/round-22/falsify/FxC3Separable.md` (undeclared read).
5. `FxC3Separable:24` — `call_01_MKLj0E6mCLvaOkXqDrJ39364` — read —
   `…/round-22/falsify/FxC3Separable.md:-16`; `:-16` stripped, base undeclared for read.

Unknown rows (`rough_category=unknown`, counts 0/0/0, `canonical_bad=[]`, `disposition=agree`):

6. `FxC3Buckets:20` — `call_00_Mscl2Ziq00eJHmJHayT68671` — edit — `…/round-22/falsify/FxC3Buckets.md`.
7. `FxC3Buckets:22` — `call_00_ly7tjlpk19xfpfxgbi8eto4r` — edit — same path.
8. `FxC3ReportDigest:8` — `toolu_vrtx_01QMz3i1tGAnSkf1mFqqh5YT` — edit — `…/round-22/falsify/FxC3ReportDigest.md`.

`edit` is outside the v1 read/grep/glob/write grammar, so it yields `unknown` with no canonical
path components; the preregister's C1/C2 edit decisions do not extend v1 path authority here.

Adjacent row worth naming (recorded `clean`, and correctly so): `FxC3StrictReuse:17` —
`toolu_01VQY3W815qW1SYQJ1M2pz9d` — grep — a single `;`-joined argument of seven paths
(`preregister.json; host-tool-boundary.json; check-review-cohort.py; check-review-snapshots.py;
_revision.py; seat-boundary-r22.json; seat-boundary-r22.md`), each individually declared; the
component grammar splits before comparison, so all seven pass.

## Attack on C3 (concrete falsifiers tested)

- **F1 — own-report read-back authorized.** Claim: the five path rows are legal because each
  file is the seat's declared `write_path`. Result: not under literal v1 authority (reads compare
  to `read_paths` only; bindings never list the own report as readable), and the ledger's
  canonical values agree with rough. **F1 does not hold.** [INFERENCE] Additionally, a
  read-back allowance cannot by itself explain the reported falsify cohort delta: it would flip
  five events in this pack, more than the whole reported rough−lane difference of 4 (33−29).
- **F2 — joined grep counted as one literal argument.** Claim: `FxC3StrictReuse:17` should be a
  path violation because the joined string is not literally any declared path. Result: the S085
  and component grammar split on `;`; all components are declared. A non-splitting lane rule
  would also make the lane count larger than rough, contrary to the reported 29 < 33. **F2 does
  not hold.**
- **F3 — shared call_id collapse.** Claim: `FxC3ReportDigest:8/9/10` share one `call_id` and
  should collapse to one row. Result: three distinct tool/path tuples and three distinct declared
  digests (`71803f31…`, `b1622e04…`, `9571b9ec…`); the slice keeps three rows with correct
  per-row classifications. **F3 does not hold.**
- **F4 — selector strip over/under-reach.** Claim: a digit-bearing selector or filename is
  mis-stripped, turning a violation clean or the reverse. Result: every selector-bearing event
  (`:N`, `:N-M`, `:N-M,K-L`, `:N-M:raw`, `:-N`, `:raw`) strips to a declared base; no filename
  base terminates in `:<digits>` outside a selector. **F4 does not hold.**

Bounded search performed: hand re-derivation of all 133 events across all eight seats,
pack/slice `call_id` sequence equality, digest equality on all eight non-clean rows, and a
rule-faithful re-classification of the full pack reproducing exactly the recorded non-clean set.
Within this slice, no row-level falsifier of C3 exists.

## Residual unknown and smallest in-scope remedy

- [INFERENCE] This pack contributes 5 path and 3 unknown events and **zero** rough-vs-canonical
  disagreement. It therefore proves per-event/per-component exactness but cannot, by itself,
  account for the reported falsify cohort reduction 33 → 29: the whole difference must be carried
  by the other packs plus whatever counting unit the ledger declares (event vs distinct file vs
  seat vs call_id). That closure is outside this seat's declared read set (other slices and the
  reconciliation tool are not readable here), so it is reported as an unresolved gap, not as a
  row dispute.
- Field semantics for `retained_path_count` are not schema-documented in my readable set; every
  row is coherent with "retained violation components" (0 on clean/unknown, 1 on path), and no
  row contradicts that reading.
- Smallest in-scope remedy: **no row correction**. If L1 needs to close C3, add one explicit
  declared-arithmetic line per cohort naming the counting unit and the pack-sum closure that maps
  rough 33/25 to lane 29/23, and state that group 7 contributes 5 path + 3 unknown with all rows
  agreeing. No production file, binding, or VCS state was touched; this report is the only
  write. No tool was installed or executed (NO-EXEC/NO-FETCH honoured; no LSP/server tracing was
  applicable to this frozen-data question).

Reviewed-SHA256: f2aea12c5468b69a3e52f76478f220ba90a3ef9afdfbcc0f112e72c98900b7c9
Predicate: r23f-fxc3falsify07
Scope: executed=none
