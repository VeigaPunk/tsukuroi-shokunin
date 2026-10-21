# ReconBuild05 — r22 rough path census vs declared old-v1 authority (pack build-05)

## 1. Inputs and status

- Pack: `.ufo/waves/round-23/packs/build-05.json`, schema `tsukuroi-path-oracle-pack-v1`, wave `build`, group `5`, eight seats.
- Declared pack SHA-256, accepted as supplied identity only; not recomputed, no hash/list/wc/import/exec was run: `44039f720d5e207ff908d2fc8cea3889c889470d4e426de5997f29c3a5564e1a`.
- Rough source algorithm: `.ufo/waves/round-23/sources/r22-rough-census.txt` (19 lines, read in full). It is a recorded eval request treated as data, never executed here.
- Outside totals as declared in `.ufo/waves/round-23/preregister.json`: rough `build 25 / falsify 33`; lane `build 23 / falsify 29`; entry 422; commit `4482c275f9381f219ee4d092e0324d417c3cb1e7`; baseline `ae01e50f582016384e620022be38bf5367000e2e`.
- Pack scope line: "Raw preserved request metadata only; no expected classifications are supplied." Every classification below is therefore a hand reconstruction of the 19-line algorithm, not a recorded expectation.
- Method: source-level derivation only. No gate/counter runs, no hashing, no command, no fetch. Where a statement is inferred rather than read, it is marked `[INFERENCE]`.

## 2. Exact semantics of the rough algorithm (as written)

```python
def strip_sel(p):
  return re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)
```

Operative properties, in the order the source applies them:

1. Tool precedence: `bash` → `exec` (+seat, `continue`); any tool outside `{read, grep, glob, write}` → `unknown` (+seat, `continue`); only the remaining four reach the path test. A non-standard tool never reaches path membership.
2. Value extraction: `grep`/`glob` paths are split on `;`; every other tool is a one-element list. `write` is therefore **not** split.
3. Selector stripping: only `read` and `grep` call `strip_sel`. `glob` and `write` are compared verbatim.
4. Selector regex: anchored at end; alternation order `raw`, `\d[\d\-+,:]*`, `-\d+`, `\d+-`; optional trailing `:raw`. It strips `:raw`, `:N`, `:N-M`, `:N,M`, `:-N`, `:-N:raw`, `:N-M:raw`. It does not strip anything from URI-shaped inputs such as `skill://godspeed` (no colon suffix matches).
5. Membership set: `write` → `write_paths`; every other surviving tool → `read_paths`. A `read` of a declared write target is therefore a violation; a selector-stripped read is still tested against `read_paths` only.
6. Counting: inside a multi-value list the first undeclared value increments `path` once and `break`s. Each event yields at most one count total, and never two buckets. An event with an absent `path` coerces to `''` and counts as `path`.
7. `seats` is a set of seat names having at least one count; the printed total is `sum(f.values())` (event-bucket counts), which is distinct from `len(seats)`.

## 3. Declared old-v1 authority for these eight seats

All eight bindings are identical except the write target. Legend:

- `A` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json`
- `B` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json`
- `C` = `skill://godspeed`
- `Wn` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/<seat>.md`

| seat | agent | read_paths | write_paths | commands | fetches | edit authority |
|---|---|---|---|---|---|---|
| OracleParallelLocal | TsukuroiR22.OracleParallelLocal-3 | A, B, C | W `OracleParallelLocal.md` | `[]` | `[]` | none |
| OracleParallelMalformed | TsukuroiR22.OracleParallelMalformed-3 | A, B, C | W `OracleParallelMalformed.md` | `[]` | `[]` | none |
| OracleTraceMissing | TsukuroiR22.OracleTraceMissing-3 | A, B, C | W `OracleTraceMissing.md` | `[]` | `[]` | none |
| OracleTraceIncomplete | TsukuroiR22.OracleTraceIncomplete-3 | A, B, C | W `OracleTraceIncomplete.md` | `[]` | `[]` | none |
| OracleTraceDuplicate | TsukuroiR22.OracleTraceDuplicate-3 | A, B, C | W `OracleTraceDuplicate.md` | `[]` | `[]` | none |
| OracleTraceUnknown | TsukuroiR22.OracleTraceUnknown-3 | A, B, C | W `OracleTraceUnknown.md` | `[]` | `[]` | none |
| OracleTraceEmpty | TsukuroiR22.OracleTraceEmpty-3 | A, B, C | W `OracleTraceEmpty.md` | `[]` | `[]` | none |
| OracleTraceBadArgs | TsukuroiR22.OracleTraceBadArgs-3 | A, B, C | W `OracleTraceBadArgs.md` | `[]` | `[]` | none |

No binding in the pack contains an `edit_paths` key (grep-confirmed over the whole pack). Old v1 recognizes only read and write authority; no edit permission is imported from r23 schema-v2.

## 4. Per-seat, per-event hand result (39 records)

`ev` is 0-based within the seat's recorded `events` array; `start` is the recorded `start_line` (or `start_lines`). Bucket is the rough outcome.

### 4.1 OracleParallelLocal — 7 records — subtotal: `path 1`

| ev | tool | start | path (suffix called out) | rough bucket |
|---|---|---|---|---|
| 0 | read | 14 | `skill://godspeed` | allow (literal `C`) |
| 1 | read | 15 | `A` | allow |
| 2 | read | 19 | `B` | allow |
| 3 | read | 22 | `A` suffix `:1-20:raw` → strips to `A` | allow |
| 4 | read | 23 | `B` suffix `:1-30:raw` → strips to `B` | allow |
| 5 | write | 27 | `W OracleParallelLocal.md` | allow |
| 6 | read | 30 | `W OracleParallelLocal.md` suffix `:-6:raw` → strips to `W`, which is **not** in `read_paths` | **path 1** |

Seat flagged. The count is a genuine v1 violation (the seat read its own build report, declared only for write), not a stripping artifact: the suffix strips cleanly and the stripped value still fails `read_paths`.

### 4.2 OracleParallelMalformed — 6 records — subtotal: `path 2`

| ev | tool | start | path (suffix called out) | rough bucket |
|---|---|---|---|---|
| 0 | read | 22 | `skill://godspeed` | allow |
| 1 | read | 23 | `/home/vgpnk/Projects/shokunin/tsukuroi-shokurin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json` (root typo `tsukuroi-shokurin`) | **path 1** |
| 2 | read | 24 | `/home/vgpnk/Projects/shokuroi/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json` (root typo `shokuroi`) | **path 1** |
| 3 | read | 30 | `host-tool-boundary.json` under correct root | allow |
| 4 | read | 31 | `preregister.json` under correct root | allow |
| 5 | write | 35 | `W OracleParallelMalformed.md` | allow |

Seat flagged. Both malformed reads carry no selector, so no normalization is in play: exact string inequality against `read_paths`. The later corrected reads at records 3–4 (later `request_line` 29) show the malformed attempts were separately recorded requests, not renderings of the corrected pair.

### 4.3 OracleTraceMissing — 5 records — subtotal: `unknown 1 + path 1`

| ev | tool | start | path (suffix called out) | call_id | rough bucket |
|---|---|---|---|---|---|
| 0 | read | 9 | `A` | `toolu_01Xdhet2uzjfsVmGLj39kXDT` | allow |
| 1 | read | 10 | `B` | `toolu_016m7QbgEyoBc3N61EDxyD9o` | allow |
| 2 | edit | 11–12 | `W OracleTraceMissing.md`, plus unknown arg placeholder | `toolu_01JkHbts7HMkWNYEvbXS1NjJ` | **unknown 1** (tool not in `{read,grep,glob,write}`; path never evaluated) |
| 3 | read | 11 | `W OracleTraceMissing.md` suffix `:raw` → strips to `W`, not in `read_paths`; `request_line: null`, `origin: additional-recorded-start` | `toolu_01JkHbts7HMkWNYEvbXS1NjJ` | **path 1** |
| 4 | write | 12 | `W OracleTraceMissing.md`; `request_line: null`, `origin: additional-recorded-start` | `toolu_01JkHbts7HMkWNYEvbXS1NjJ` | allow |

Seat flagged. This is the pack's only three-record call identity: one `edit` request expanded into recorded adapter `read` and `write` records sharing its `call_id` and overlapping its `start_lines` `[11,12]`.

### 4.4 OracleTraceIncomplete — 5 records — subtotal: `0`

| ev | tool | start | path | rough bucket |
|---|---|---|---|---|
| 0 | read | 19 | `skill://godspeed` | allow |
| 1 | read | 20 | `A` | allow |
| 2 | read | 21 | `B` | allow |
| 3 | write | 30 | `W OracleTraceIncomplete.md` (`content: null` in pack) | allow |
| 4 | write | 34 | `W OracleTraceIncomplete.md` (`content: null` in pack) | allow |

Rough has no per-target uniqueness rule, so the duplicate write records both count zero.

### 4.5 OracleTraceDuplicate — 4 records — subtotal: `0`

| ev | tool | start | path | rough bucket |
|---|---|---|---|---|
| 0 | read | 14 | `A` | allow |
| 1 | read | 15 | `skill://godspeed` | allow |
| 2 | read | 19 | `B` | allow |
| 3 | write | 22 | `W OracleTraceDuplicate.md` | allow |

The seat's duplicate character is not a duplicate path inside the seat. It is cross-seat request duplication by digest: ev0 repeats `a0250763…`, ev1 repeats `2b4cad9d…` (also present in OracleParallelLocal ev1/ev0 and OracleTraceBadArgs ev0/ev2). Per-seat membership sees none of that.

### 4.6 OracleTraceUnknown — 4 records — subtotal: `0`

| ev | tool | start | path (suffix called out) | rough bucket |
|---|---|---|---|---|
| 0 | read | 12 | `skill://godspeed` | allow |
| 1 | read | 13 | `A` suffix `:1-180` → strips to `A` | allow |
| 2 | read | 14 | `B` suffix `:1-180` → strips to `B` | allow |
| 3 | write | 19 | `W OracleTraceUnknown.md` | allow |

Both counts depend on the colon-range branch of `strip_sel`; without it these four would be two path violations.

### 4.7 OracleTraceEmpty — 4 records — subtotal: `0`

| ev | tool | start | path | rough bucket |
|---|---|---|---|---|
| 0 | read | 19 | `skill://godspeed` | allow |
| 1 | read | 20 | `A` | allow |
| 2 | read | 21 | `B` | allow |
| 3 | write | 26 | `W OracleTraceEmpty.md` (`content: null`) | allow |

### 4.8 OracleTraceBadArgs — 4 records — subtotal: `0`

| ev | tool | start | path | rough bucket |
|---|---|---|---|---|
| 0 | read | 14 | `A` | allow |
| 1 | read | 15 | `B` | allow |
| 2 | read | 16 | `skill://godspeed` | allow |
| 3 | write | 21 | `W OracleTraceBadArgs.md` | allow |

Batch order differs from OracleParallelLocal ev0/ev1 and OracleTraceDuplicate ev0/ev1 (same `request_line`, reversed member order). Membership is order-insensitive, so this is order-only with zero count effect.

## 5. Candidate components where the rough result is normalization-order-break sensitive

Categories: **S** selector normalization, **O** evaluation/order, **B** one-per-event break. `Δ↓` means a plausible lane treatment makes the count disappear (lane lower); `Δ↑` means it appears (lane higher). No candidate is asserted as the actual lane behavior — the lane comparator is not declared anywhere in pack or preregister.

| id | seat | ev | call_id | raw path suffix | rough | category | bounded reason / sensitivity | if lane differs |
|---|---|---|---|---|---|---|---|---|
| S1 | OracleParallelLocal | 6 | `call_00_jzklheuqzGfyYiaMhp4N3833` | `OracleParallelLocal.md:-6:raw` | path 1 | S (and authority-order) | Stripping succeeds via `-\d+` + optional `:raw`; the stripped value is a declared **write** target and step 5 tests reads against `read_paths` only. A lane that tests stripped reads against `read_paths ∪ write_paths` allows it. | Δ↓1 |
| S2 | OracleParallelLocal | 3,4 | `call_00_62N1RQ7QVIkbaF4hOZI92448`, `call_01_EV6jlNlPMsroMjsnc45l5081` | `host-tool-boundary.json:1-20:raw`, `preregister.json:1-30:raw` | allow | S | Allow depends entirely on the `\d[\d\-+,:]*` + `(:raw)?` branch. A lane stripping only bare `:N`/`:N-M` without `:raw`, or not stripping at all, flips both to path. | Δ↑2 |
| S3 | OracleTraceMissing | 3 | `toolu_01JkHbts7HMkWNYEvbXS1NjJ` | `OracleTraceMissing.md:raw` | path 1 | S (and authority-order) | `:raw` strips via the first alternative, but the stripped value is write-only. Same `read_paths`-only test as S1; the count survives any stripping rule. Divergence only via read-authority-set widening. | Δ↓1 |
| S4 | OracleTraceUnknown | 1,2 | `call_06dc41992b2d40728dca132ad9297984|fc_0b9e…`, `call_25d0f9f9c3b24ca09ef95796f8ec8637|fc_0b9e…` | `host-tool-boundary.json:1-180`, `preregister.json:1-180` | allow | S | Allow depends on the colon-range branch alone (no `:raw`). A lane that strips only `:raw` yields two path counts. | Δ↑2 |
| S5 | OracleParallelLocal / Malformed / Incomplete / Duplicate / Unknown / Empty / BadArgs | 0,0,0,1,0,0,2 | as recorded | `skill://godspeed` (7 reads) | allow | S (URI shape) | `strip_sel` is a no-op on this string, and `C` is a literal `read_paths` entry. A lane that refuses URI-shaped read authority would count all 7. This direction contradicts lane < rough globally, so it is disfavored as an explanation, not impossible. | Δ↑7 |
| S6 | any write | — | — | none | — | S (untested asymmetry) | No write record in the pack carries a selector; `write` is never stripped by the source. The asymmetry is real but unexercised here. | 0 |
| O1 | OracleTraceMissing | 2 | `toolu_01JkHbts7HMkWNYEvbXS1NjJ` | `OracleTraceMissing.md` (no suffix) | unknown 1 | O (bucket precedence) | The tool test precedes the path test, so the declared **write** target is never compared. A lane that maps `edit` into the write bucket, or evaluates path first, records zero. No old-v1 edit authority exists to justify the mapping. | Δ↓1 |
| O2 | OracleTraceMissing | 3,4 | `toolu_01JkHbts7HMkWNYEvbXS1NjJ` | `…md:raw` / `…md` | path 1, allow | O (record ordering) | Both adapter records carry `request_line: null` and `start_line` 11/12, exactly overlapping the edit's `start_lines [11,12]`. Any lane ordering by `(request_line, start_line)` or placing nulls first reorders the trio. A pure reorder changes no total here; it only matters combined with O3. | 0 alone |
| O3 | OracleTraceMissing | 2,3,4 | `toolu_01JkHbts7HMkWNYEvbXS1NjJ` | `…md`, `…md:raw`, `…md` | 2 counts | O (identity/one-per-call) | The only `call_id` in the pack spanning three records. Rough counts per record (unknown + path). A lane keyed by `call_id` counts the call once, at most 1. This is the pack's only event-vs-component unit break. | Δ↓1 |
| O4 | OracleTraceMissing | 2 | `toolu_01JkHbts7HMkWNYEvbXS1NjJ` | `OracleTraceMissing.md` | unknown 1 | O (bucket exclusivity) | `continue` prevents any event from scoring both `unknown` and `path`; only this event could. A lane scoring both would add one. | Δ↑1 |
| B1 | all seats | — | — | — | — | B (multi-value break) | Zero `grep`/`glob` events exist in the pack, so the `;` split and `break` never truncate a value scan. No candidate from the one-per-event break with multiple values. | 0 |
| B2 | OracleTraceIncomplete | 3,4 | `call_32a3dc42…|fc_0d57…`, `call_f3911947…|fc_0d57…` | `OracleTraceIncomplete.md` twice | allow, allow | B (duplicate target) | Rough has no per-target uniqueness rule; a lane deduplicating write targets cannot lower a zero. The two writes are distinct `call_id`s, so per-call dedupe does not collapse them either. | 0 |
| B3 | OracleTraceDuplicate | 0,1 | cross-seat digests `a0250763…`, `2b4cad9d…` | `A`, `C` | allow | B (global digest dedupe) | Global dedupe by `request_arguments_sha256` would not change any count in this pack, because none of the duplicated requests is a violation. | 0 |

## 6. Calibration arithmetic against 25/33 vs 23/29

Hand totals for this pack only:

- records 39; unique `call_id` values 37 (the three-record collision at O3 accounts for the difference); `additional-recorded-start` records 2.
- rough buckets: `exec 0`, `unknown 1`, `path 4`, **total 5**; flagged seats 3 (OracleParallelLocal, OracleParallelMalformed, OracleTraceMissing).
- records bearing a count: 5, over 4 unique `call_id`s. Event records and request identities are therefore not interchangeable in this pack.

Constraints that follow from the source, not from re-running anything:

1. Net wave deltas are not per-event attributions. `25→23` and `33→29` are net sums over corpora that include seven other build groups and the whole falsify wave. A group can contribute both signs; nothing here licenses mapping the `-2` to two named events.
2. This pack alone can support at most `Δ -3` (S1/O1-style read-authority widening or edit mapping, S3, plus O3 collapse). It cannot reach zero: the two malformed-root reads (OracleParallelMalformed ev1, ev2) survive every selector, ordering, and break rule in the source, because they are plain exact-string misses with no suffix. If this pack's 5 are part of the 25, at least 2 of them remain inside the 23.
3. Two independent single mechanisms each produce exactly `-2` inside this pack and therefore both remain live explanations for the build delta:
   - `M2` read authority widened to `read_paths ∪ write_paths`: drops S1 and S3, total 3.
   - `M5` comparison collapsed to basename (dropping the directory identity that carries the typos): drops the two malformed-root reads, total 3. It does not rescue S1 or S3, whose basenames are also absent from `read_paths`.
   The pack does not declare which comparator was used, so the build `-2` is underdetermined from this pack.
4. `M3` (`edit` → write bucket) and `O3` (`call_id` collapse) each give `-1`; neither alone reaches `-2`, and each requires an assumption old v1 does not contain: v1 bindings expose no edit authority at all, and no unit rule beyond one event record. Not importing r23's schema-v2 edit targets here, and not importing EXPANSION/OPAQUE decisions as authority over old records.
5. Do not read the six-unit net delta (`2 + 4`) as six unique events. Within this pack the ratio of records to identities is already 39:37, one identity spans three records, and two records are `additional-recorded-start` renderings. Across both waves the count unit is undeclared: the rough source prints both `sum(f.values())` and `len(seats)`, and the lane figure's unit is not specified in pack or preregister.
6. Falsify is unobservable from this seat: the pack contains no falsify records and my read authority covers no falsify corpus. The `33→29` delta remains wholly unattributed here; no arithmetic is offered for it.

## 7. Checked and found absent (no candidate)

- `bash` events: none (zero `exec`); `glob`/`grep` events: none, so `;` splitting, the per-event `break`, and the glob-without-strip branch are all unexercised.
- writes carrying a selector suffix: none, so the write/read stripping asymmetry produces no candidate here.
- events with a missing `path`: none, so the `''`-coercion rule is unexercised.
- declared paths whose own tail matches the selector regex (false-strip risk): none. `A`, `B`, `C`, and all eight `Wn` end in `.json`, `//godspeed`, or `.md`.
- selector-stripped read equal to a declared write target after stripping: S1 and S3 only; both counted above.
- non-string `path` values: none; every `path` is a string.
- reclassification of `edit` as an allowed edit: impossible under v1; no `edit_paths` key exists in any of the eight bindings.

## 8. Remaining unknowns

1. The lane comparator is undeclared: exact-string, normalized, or basename; and whether reads may use write authority. This is the pivot for the build `-2` and is not answered by the pack.
2. The lane's counting unit (event record, `call_id`, seat, or component) is undeclared; rough prints two different totals from one pass.
3. The other seven build groups and the entire falsify wave are outside my read authority, so `25` and `33` cannot be reconstructed here; `33→29` is unattributed.
4. The census's `W` prefix is not recorded in the source excerpt, so pack records cannot be proven byte-identical to the `events.json`/`bindings.json` inputs the rough pass consumed. Pack-only fields (`origin`, `request_line: null`, `__unknown_argument__`, `content: null`) are not read by the rough source but may be read by the lane.
5. No historical manifest/report rewrite is performed or implied; classifications above are read-only reconstructions.

Reviewed-SHA256: 44039f720d5e207ff908d2fc8cea3889c889470d4e426de5997f29c3a5564e1a
Predicate: r23-reconbuild05
Scope: executed=none
