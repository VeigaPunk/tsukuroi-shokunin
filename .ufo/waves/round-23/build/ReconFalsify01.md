# ReconFalsify01 — falsify-01 old-v1 path-census falsification

Wave: round-23, wave `falsify`, group 1.
Pack: `.ufo/waves/round-23/packs/falsify-01.json` (declared digest supplied as identity, not recomputed).
Baseline: `ae01e50f582016384e620022be38bf5367000e2e`.
Method: static, hand-derived application of the exact r22 rough census source cell
(`sources/r22-rough-census.txt`) to the eight preserved historical seats. No command,
counter, hasher, importer or gate was run (`executed=none`). Labels below mark
`[OBSERVED]` (declared metadata), `[DERIVED]` (hand evaluation of the stated algorithm),
`[INFERENCE]` (candidate mechanism, not observed lane code), `[GAP]` (outside declared reads).

Report: .ufo/waves/round-23/build/ReconFalsify01.md

## 1. Exact rough algorithm, as declared

The source cell, quoted as data:

```
def strip_sel(p):
  return re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)
for w in ['build','falsify']:
  ev=obj(f'{W}/{w}/events.json'); bd={s['name']:s for s in obj(f'{W}/{w}/bindings.json')['seats']}
  f=collections.Counter(); seats=set()
  for x in ev['seats']:
    b=bd[x['name']]
    for e in x['events']:
      t=e['tool']; a=e.get('args') or {}
      if t=='bash': f['exec']+=1; seats.add(x['name']); continue
      if t not in ('read','grep','glob','write'): f['unknown']+=1; seats.add(x['name']); continue
      vals=str(a.get('path','')).split(';') if t in('grep','glob') else [str(a.get('path',''))]
      for v in vals:
        q=strip_sel(v) if t in('read','grep') else v
        if q not in (b['write_paths'] if t=='write' else b['read_paths']): f['path']+=1; seats.add(x['name']); break
  print(w,dict(f),sum(f.values()),'seats',len(seats))
```

Decision order that matters for this cohort `[DERIVED]`:

1. `tool == bash` -> `exec`, skip path entirely.
2. tool outside `{read,grep,glob,write}` -> `unknown`, skip path entirely. `edit` lands here; no v1 edit class exists.
3. `read`/`write` use one value; `grep`/`glob` split the single `path` string on `;`.
4. Selector stripping applies to `read` and `grep` only; `glob` and `write` are compared raw.
5. The comparison set is `write_paths` for `write`, otherwise `read_paths`. `write_paths` is never read authority.
6. At most one counter increment per event record; the first nonconforming value breaks the loop.
7. `seats` is the set of seat names with at least one increment, so counts and unique seats are different units.

Regex consequence, evaluated by hand on the two suffix orders actually present `[DERIVED]`:

- `...py:1-175:raw`: the greedy `\d[\d\-+,:]*` backtracks one character so `(:raw)?` consumes `:raw`; the whole suffix strips -> base path. Conforms.
- `...py:raw:15-60`: `raw` cannot match because `$` fails; the numeric branch starts at the later colon and strips only `:15-60`, leaving `...py:raw`. Not in `read_paths`. One `path` increment.
- `re.sub` is a single left-to-right pass over the original string; it does not rescan its own output. A fixpoint strip would remove both suffixes.

## 2. Cohort inventory `[OBSERVED]`

Eight seats, 108 event records. All eight bindings expose exactly
`name/root/read_paths/write_paths/commands/fetches`: no `edit_paths` or edit-target key exists in
old v1. Every binding has the same eight `read_paths` and one report `write_path`, `commands: []`,
`fetches: []`. Tool mix: 81 `read`, 18 `grep`, 8 `write`, 1 `edit`; zero `bash`, zero `glob`, zero
fetch/search/task records. Every event's `start_line` is nondecreasing within its seat, so traversal
order and the `seats` set are order-independent here.

Per-seat hand derivation `[DERIVED]` (`ev#` is 0-based list index within the seat):

| seat | events | read/grep/write/edit | path | unknown | exec | flagged |
|---|---|---|---|---|---|---|
| FxC1NoExec | 11 | 10/0/1/0 | 0 | 0 | 0 | no |
| FxC1NoFetch | 17 | 11/5/1/0 | 0 | 0 | 0 | no |
| FxC1LocalRead | 16 | 11/4/1/0 | 0 | 0 | 0 | no |
| FxC1ReportWrite | 8 | 6/0/1/1 | 1 | 1 | 0 | yes |
| FxC1Unknown | 16 | 12/3/1/0 | 4 | 0 | 0 | yes |
| FxC1Dead | 11 | 9/1/1/0 | 0 | 0 | 0 | no |
| FxC1Duplicate | 14 | 10/3/1/0 | 0 | 0 | 0 | no |
| FxC1Hidden | 15 | 12/2/1/0 | 0 | 0 | 0 | no |
| cohort | 108 | 81/18/8/1 | 5 | 1 | 0 | 2 seats |

If this pack were the whole falsify wave, the algorithm would print
`falsify {'unknown': 1, 'path': 5} 6 seats 2` (dict insertion order: unknown at ReportWrite ev#5,
then path). It is not the whole wave: the declared outside rough falsify total is 33, so 28 path
records lie outside this pack's declared scope.

## 3. Candidate components

### A. Inverted `:raw:N-M` suffix residue — four events, one mechanism `[DERIVED]`, `[INFERENCE]` for lane

All four are primary request records (non-null `request_line`, no `additional-recorded-start`
origin), the shape the census extract consumes, unlike component B's ordered-start records. Each has
an authorized base path in `read_paths`.

| # | seat | ev# | start_line | request_line | call_id | raw suffix | rough | fixpoint/order-aware strip |
|---|---|---|---|---|---|---|---|---|
| A1 | FxC1Unknown | 8 | 36 | 35 | toolu_01SCLctdiGzTL9cNPCdfjFYW | `:raw:15-60` | path +1 | conforms, -1 |
| A2 | FxC1Unknown | 9 | 37 | 35 | toolu_01ASiJwaeMcZrphAZyuTztc3 | `:raw:58-102` | path +1 | conforms, -1 |
| A3 | FxC1Unknown | 10 | 38 | 35 | toolu_01K3ih69GpJx5agmk4hChSei | `:raw:103-175` | path +1 | conforms, -1 |
| A4 | FxC1Unknown | 14 | 46 | 42 | toolu_01R72arcerJspPr3z3wvNHRL | `:raw:172-193` | path +1 | conforms, -1 |

Bounded reason: the base files are declared read targets; `:raw` and a line range select bytes, not
a different file. The declared authority enumerates files and is silent on selector order, so the
four counts are produced by the classifier's single-pass normalizer, not by an authority difference.
The cohort contains eight raw-suffix reads: three canonical `:N-M:raw` (NoExec ev#8, LocalRead ev#11
and ev#12), one bare `:raw` on the report (component B), and the four inverted `:raw:N-M` records
above. All three canonical records strip cleanly; no other inverted selector exists in the pack.

### B. Read of the write-only report — one event, authority-negative `[OBSERVED]`

| seat | ev# | start_line | request_line | call_id | raw suffix | rough |
|---|---|---|---|---|---|---|
| FxC1ReportWrite | 6 | 14 | null (`origin: additional-recorded-start`) | toolu_01SKTuRKNxh7ui6itpAk2oCi | `:raw` on `falsify/FxC1ReportWrite.md` | path +1 |

Bounded reason: `:raw` strips cleanly to the base report path. That base appears only in
`write_paths`, never in `read_paths`; old v1 has no read-from-write grant. This is a genuine
file-target absence, unlike A. It flips only if read authority is unioned with `write_paths`
(generic report ownership) or if the record is deduped into its sibling `write` record. Neither is
declared v1 authority; importing either would be a new edit/report permission.

### C. `edit` precedence — one event `[OBSERVED]`

| seat | ev# | start_line | request_line | call_id | tool | path |
|---|---|---|---|---|---|---|
| FxC1ReportWrite | 5 | 14, `start_lines [14,15]` | 17 | toolu_01SKTuRKNxh7ui6itpAk2oCi | `edit` | exact report path; args carry `__unknown_argument__` |

Bounded reason: old v1 bindings have no edit key and the tool taxonomy has no edit class, so the
record is `unknown` by construction and its path is never consulted. Treating it as a write would
conform it (the path is declared); treating it as a read would add a path count. Both are imports of
a class the frozen v1 schema does not contain. The withheld structured body is why no target can be
reconstructed from the record itself.

### D. One call, three recorded starts `[OBSERVED]`

`toolu_01SKTuRKNxh7ui6itpAk2oCi` yields ev#5 (`edit`, request_line 17), ev#6 (`read`, null
request_line, `origin: additional-recorded-start`, start 14) and ev#7 (`write`, null request_line,
same origin, start 15, conforming). The edit record's `start_lines` is `[14,15]`, the same two lines
as the two adapter records. Per-record evaluation gives 1 unknown + 1 path. One-per-call dedupe
could give 1 (most severe) or 0 (last record wins); per-`start_line` expansion could give more than
two components. Old v1 has no expansion or dedupe rule; the new v2 `EXPANSION/CHECK_EACH` row must
not be retro-applied. Whether the frozen `events.json` contained the two additional records is not
declared `[GAP]`; if it did not, component B is not part of the historical 33 at all, and the pack's
path count for the cohort is 4 rather than 5. The A delta is unaffected either way.

### E. Multi-value break `[DERIVED]`, no divergence

Two `;`-joined path records exist: FxC1NoFetch ev#15 (`round-22/preregister.json;round-22/sources/host-tool-boundary.json`,
start 52) and FxC1Hidden ev#11 (four paths, start 43). Every value is an authorized read target, so
per-event and per-value evaluation both yield zero. No record in the cohort has a second
nonconforming value hidden behind the break. The `break` therefore has no observed effect here, but
it remains the component that would cap a multi-value event at one count.

### F. Branches with zero cohort members `[OBSERVED]`

- `exec`: zero `bash` records; the exec counter cannot move.
- `glob`: zero records; the unstripped-glob branch is untested by this cohort.
- fetch/search/task: zero records; no fetch authority exists (`fetches: []`), and none was used.

### G. Normalization non-candidates `[DERIVED]`

- `skill://godspeed`: eight reads, one per seat, string-equal to an entry in `read_paths`; all
  conform. Rejecting non-filesystem URIs would inflate, not reduce. The v2 `EDIT_EXTERNAL` row is
  edit-scoped and cannot be imported into read authority.
- Absolute paths: all under the declared root, no `.`/`..`, duplicate separators, case variants or
  symlinked spellings; file identity is exact.
- Argument key order and `i: null` do not affect `path` extraction.
- Comma-separated ranges (`:1-60,60-120,120-200`, `:18-25,58-100,103-137,150-175`) strip as one
  suffix; splitting them as multiple files would inflate counts and has no support.
- Ordering: monotone `start_line`; the `seats` set is order-free. No ordering divergence.

## 4. Arithmetic against 25/33 versus 23/29

The declared record labels the numbers `path_counts_as_reported`; the source cell prints a path
counter, an exec/unknown counter and a unique-seat count, so the column is not restated outside the
preregister `[GAP]`. Three readings are evaluated; all keep the A mechanism, and each constrains the
other candidates differently.

Reading P — the numbers are the `path` counter (best supported by the label):

- Cohort rough path = 5: four A records plus the B report read.
- A alone flips 5 -> 1; falsify 33 -> 29 exactly if every event outside this pack keeps its class
  (`28` rough = `28` lane outside).
- B also flipping would give 28, which contradicts 29; B is therefore refuted as a lane mechanism
  under reading P, and the read authority stays `read_paths`-only.
- C is invisible to this column; D changes the column only through B (same refutation).

Reading S — the numbers are `sum(f.values())` over path+exec+unknown:

- Cohort rough sum = 6 (5 path + 1 unknown).
- A alone flips 6 -> 2; 33 -> 29 exactly under unchanged outside (27 = 27).
- B would give 28 -> refuted. C alone would give 32; A+C would give 28. Neither is 29, so under
  this reading the lane must retain the edit's old-v1 `unknown` disposition and must not convert it
  to write/path. That is the "no imported edit permission" result derived from the reported
  arithmetic itself.

Reading C — the numbers are unique flagged seats:

- This pack flags at most 2 seats (ReportWrite, Unknown); A unflags Unknown, while ReportWrite stays
  flagged by the `edit` unknown even if B flips. A 33 -> 29 seat delta needs four unflagged seats, so
  three must be outside this pack; A in one seat cannot supply it. This reading is disfavored by the
  `path_counts` label but is not closed by this pack. No unique-seat conclusion is drawn.

Build cohort: 25 -> 23 is a delta of 2 with no build pack in this seat's declared reads `[GAP]`.
Nothing in falsify-01 observes build records. If A is the global mechanism, build would need exactly
two inverted-order selector records and no other class change; that is a test expectation only, not
an observation. The 2 and the 4 must not be pooled into "six unique events": they are separate wave
counters, and even the falsify 4 is four event instances of one mechanism in one seat.

## 5. What the cohort's six counts are, and are not

The cohort contributes 6 increments: 5 `path` records and 1 `unknown` record. They span 2 seats,
not 6; the path increments come from 2 mechanisms (A on four records, B on one); the unknown is the
single `edit` record. There are not six unique events, six seats, or six independent causes, and the
outside 33 cannot be decomposed into unique seats from this pack. Any reconciliation record that
presents 2+4 as six unique events, or that treats the four A records as four independent causes
rather than one normalizer order defect, overstates the evidence.

## 6. Old-v1 non-imports enforced

- No `edit_paths` key exists in any of the eight frozen bindings; the `edit` record has no v1
  authority row and remains `unknown`. The C1 decision vocabulary (`DECLARED_EDIT`,
  `UNDECLARED_EDIT`, `READ_ONLY_EDIT`, `WRITE_ONLY_EDIT`, `OPAQUE_PATCH`, `EDIT_TRAVERSAL`,
  `EDIT_EXTERNAL`, `EXPANSION`) is v2 contract text and is not used here to reclassify old records.
- `write_paths` is not read authority. The B report read stays a path count under literal v1; it is
  not excused by report ownership, by the later write to the same file, or by `CHECK_EACH`.
- The two additional-recorded starts are not merged into one permission and not expanded into a new
  rule; the frozen census input's membership for them is declared unknown.
- No new edit permission is inferred from `start_lines [14,15]`, from `__unknown_argument__`, or
  from the presence of both read and write targets for the same call.

## 7. Remaining unknowns

1. The lane classifier source is not in this seat's declared reads; the normalizer mechanism is
   inferred from the 4-count arithmetic only.
2. 28 of the 33 rough falsify path records and all 25/23 build records are outside this pack.
   C3 must enumerate them with zero class changes for the A-only reconciliation to hold; any second
   normalization-sensitive record outside this pack falsifies "A alone".
3. Whether the frozen r22 `events.json` included the two `additional-recorded-start` records is
   undeclared. It changes the cohort path count (5 vs 4) but not the A delta.
4. Whether the reported numbers are a path column, a counter sum, or unique seats. Reading P/S agree
   on A-only and on refuting B/C flips; reading C cannot be closed from this pack.
5. The pack's `request_arguments_sha256` values are supplied declarations; none was recomputed, and
   no conclusion depends on recomputing them.

Reviewed-SHA256: 27538ccd5c1406e9c92bcfe371ea098bf9c75d2469e7a07ddf61a5332ff66662
Predicate: r23-reconfalsify01
Scope: executed=none
