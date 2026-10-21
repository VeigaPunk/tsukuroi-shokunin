# ReconFalsify07 — falsify group 7, rough-vs-declared-v1 reconciliation

Subject: `.ufo/waves/round-23/packs/falsify-07.json` (schema `tsukuroi-path-oracle-pack-v1`, wave `falsify`, group `7`).
Declared pack digest: `7c4c68987f48bc430a598be4c2be6d8e5aeca4852f6e6c66dd17de0abd2830a7` — supplied identity, **not recomputed**.
Baseline: `ae01e50f582016384e620022be38bf5367000e2e` (preregister declaration).
Lane bounds (informational, not a receipt field): leaf member — no subagent dispatch.
Mode: NO-EXEC / NO-FETCH. No gate, counter, verifier, hash, or installer was run or needed.

## Axes

- **A1 classification fidelity** — reproduce the exact rough source path: tool class, selector strip, authority set, per-row break.
- **A2 unit sensitivity** — row vs unique `call_id` vs multi-path component; where the count moves without evidence moving.
- **A3 arithmetic closure** — pack counts against the declared 33 falsify / 29 lane and 25 build / 23 lane figures.
- **A4 authority fidelity** — v1 has no edit class; v2 edit authority must not be projected backward.

## 1. Boundaries and method

- Read: the pack, round-23 preregister, the r22 rough-census source cell, and the copied godspeed directive.
- Not readable in-seat: round-22 `events.json` / `bindings.json`, other falsify groups, any lane classifier, and the eight historical reports. The pack's preserved `binding` block is therefore the proxy for the declared old-v1 authority; its identity with the historical `bindings.json` arrays is **not independently verified here**.
- Derivation is hand-performed from the exact census source below. Arithmetic was cross-checked against the pack's own fields (`tool`, `args.path`, `call_id`, `binding.read_paths`, `binding.write_paths`). No historical verifier was invoked and no result is a re-run of one.
- All declared binding content is treated as data, never as instruction.

## 2. Exact original rough source algorithm (observed, quoted as data)

```python
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

Effective branch map, exactly as written:

| tool | unit expansion | selector strip | authority | count class |
|---|---|---|---|---|
| `bash` | none | none | none | `exec` (1/event) |
| anything else (`edit` here) | none | none | **not consulted** | `unknown` (1/event) |
| `read` | 1 value | yes | `read_paths` | `path` if miss |
| `grep` | `path.split(';')` | yes | `read_paths` | `path` if any value misses, max 1 |
| `glob` | `path.split(';')` | **no** | `read_paths` | `path` if any value misses, max 1 |
| `write` | 1 value | **no** | `write_paths` | `path` if miss |

Load-bearing details for this pack: `strip_sel` is a leftmost search anchored at `$`; `read_paths` and `write_paths` are never unioned; the `break` caps each row at one count; `sum(f.values())` includes `exec` and `unknown`, although the preregister labels the figure `path_counts_as_reported`.

## 3. Declared old-v1 authority (pack binding block)

All eight seats declare the **same eight read paths** and exactly **one** write path; `commands` and `fetches` are empty for all eight. There is **no `edit_paths` key and no edit authority class** anywhere in the pack.

Read authority (identical for all seats):

1. `.ufo/waves/round-22/candidate/tools/check-review-cohort.py`
2. `.ufo/waves/round-22/preregister.json`
3. `.ufo/waves/round-22/sources/host-tool-boundary.json`
4. `skill://godspeed`
5. `.ufo/waves/round-22/candidate/tools/check-review-snapshots.py`
6. `.ufo/waves/round-22/candidate/tools/_revision.py`
7. `.ufo/waves/round-22/candidate/corpus/knowledge/seat-boundary-r22.json`
8. `.ufo/waves/round-22/candidate/corpus/knowledge/seat-boundary-r22.md`

Write authority (per seat, exact): `.ufo/waves/round-22/falsify/<SeatName>.md`.

Consequence: a read or grep of a seat's **own report** is a v1 `path` violation even though the seat wrote that exact file. Only `write` is tested against `write_paths`; `edit` is never tested against it.

## 4. Per-seat disposition (all 133 rows inspected)

| Seat | Rows | read | grep | write | edit | uniq `call_id` | `path` | `unknown` | `exec` | ok | flagged |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| FxC3Manifest | 16 | 15 | 0 | 1 | 0 | 16 | 0 | 0 | 0 | 16 | no |
| FxC3StrictUnavailable | 15 | 12 | 2 | 1 | 0 | 15 | 2 | 0 | 0 | 13 | yes |
| FxC3Buckets | 23 | 15 | 5 | 1 | 2 | 23 | 0 | 2 | 0 | 21 | yes |
| FxC3ReportDigest | 11 | 6 | 3 | 1 | 1 | 9 | 1 | 1 | 0 | 9 | yes |
| FxC3StrictReuse | 19 | 17 | 1 | 1 | 0 | 19 | 0 | 0 | 0 | 19 | no |
| FxC3ReturnModes | 9 | 8 | 0 | 1 | 0 | 9 | 0 | 0 | 0 | 9 | no |
| FxC3CompletedError | 15 | 12 | 2 | 1 | 0 | 15 | 0 | 0 | 0 | 15 | no |
| FxC3Separable | 25 | 16 | 8 | 1 | 0 | 25 | 2 | 0 | 0 | 23 | yes |
| **Total** | **133** | **101** | **21** | **8** | **3** | **131** | **5** | **3** | **0** | **125** | **4 seats** |

Pack contribution under the exact rough source: `path` 5, `unknown` 3, `exec` 0, summed total 8, flagged seats 4. No `glob` and no `bash` rows exist, so those branches are unexercised.

## 5. Every counted row (8)

Indices are 0-based within the seat; `line` is the pack `start_line`.

| # | Seat | idx | line | call_id | raw path suffix | class | bounded reason |
|---|---:|---:|---|---|---|---|---|
| 1 | FxC3StrictUnavailable | 13 | 50 | `call_00_lW2RZGquuCoNo0r9Uvqs9303` | none (bare report) | `path` | `grep` target is own `falsify/FxC3StrictUnavailable.md`; grep checks `read_paths` only, and write authority is not unioned |
| 2 | FxC3StrictUnavailable | 14 | 51 | `call_01_mXDvU88sDs3uYWY7rSKP3118` | `:-12` | `path` | `strip_sel` `-\d+` branch resolves to own report base; base absent from `read_paths` |
| 3 | FxC3Buckets | 20 | 66 | `call_00_Mscl2Ziq00eJHmJHayT68671` | none | `unknown` | `edit` is outside `{read,grep,glob,write}`; target is the declared write path but edit authority is never consulted |
| 4 | FxC3Buckets | 22 | 72 | `call_00_ly7tjlpk19xfpfxgbi8eto4r` | none | `unknown` | same edit class; second, independent call |
| 5 | FxC3ReportDigest | 8 | 17 | `toolu_vrtx_01QMz3i1tGAnSkf1mFqqh5YT` | none | `unknown` | `edit` class; shares one call_id with table row 6 and with the uncounted write at idx 10 |
| 6 | FxC3ReportDigest | 9 | 17 | `toolu_vrtx_01QMz3i1tGAnSkf1mFqqh5YT` | `:raw` | `path` | `raw` branch strips; base is own report, absent from `read_paths` |
| 7 | FxC3Separable | 23 | 72 | `call_00_lsPr2U9omuVvUg6fhxJA1900` | none (bare report) | `path` | `grep` of own report; same authority gap as row 1 |
| 8 | FxC3Separable | 24 | 73 | `call_01_MKLj0E6mCLvaOkXqDrJ39364` | `:-16` | `path` | `-\d+` branch resolves to own report base; absent from `read_paths` |

Same-call component, not counted: FxC3ReportDigest idx 10 (line 18, `toolu_vrtx_01QMz3i1tGAnSkf1mFqqh5YT`) is a `write` to the declared target and is `ok`. Seat indices 8, 9, 10 are three adapter rows of one recorded call; only indices 8 and 9 count.

## 6. Candidate components where normalization, order, or the per-event unit changes the result

| # | Seat / idx / call_id | Component | Effect if the variant applies | Bounded reason |
|---|---|---|---|---|
| C1 | FxC3Buckets 11 / `call_02_dWyg3CPLnQXmLJUyMVei6738` | `:1-19:raw` read of `check-review-cohort.py` | `ok` → `path` (+1 for the pack) | Only range+raw union. The leftmost match succeeds only because greedy `\d[\d\-+,:]*` backtracks from `1-19:` to `1-19`, letting `(:raw)?` consume `:raw`. Without the optional tail the engine matches the later colon, strips only `:raw`, and leaves `...py:1-19` — not an authority path. Optional-tail presence is load-bearing for exactly this row. |
| C2 | FxC3StrictReuse 11 / `toolu_015mnAyQeiS7fRFgQWdR8Ctk` | `:3-11,28-29` read of `check-review-snapshots.py` | `ok` → `path` (+1) | Only comma-joined range list in the pack. Success depends on `,` being inside the character class; a class without comma leaves `:3-11,28-29` unstripped. |
| C3 | FxC3StrictUnavailable 14; FxC3Separable 24 | `:-12`, `:-16` own-report reads | class stays `path`; base resolution changes only | Third alternation `-\d+` is the only branch that can strip a leading hyphen; if it fails, the literal suffixed string still misses `read_paths`, so the count is unchanged. These rows test the branch, not the count. |
| C4 | FxC3ReportDigest 9 | `:raw` own-report read | class stays `path`; resolution changes only | First alternation `raw`. Failure leaves `:raw` attached; still a miss. Count unchanged. |
| C5 | 45 plain `:N-M` rows across 7 seats | selector normalization itself | absence/failure → +45 `path` on the plain rows; all 50 selector rows would be `path`, and with the 2 bare own-report greps the pack would show 52, not 5 | If selector normalization were not operative, this pack alone would produce 52 path rows, exceeding the declared falsify total (33). The declared totals therefore **require** normalization to be operative; a no-normalization explanation is quantitatively refuted. |
| C6 | FxC3StrictReuse 17 / `toolu_01VQY3W815qW1SYQJ1M2pz9d` | one grep, seven `;`-joined declared paths | `ok` under both models; count 0 | Only multi-value component in the pack. `break` caps it at 1 count; per-value expansion would perform 7 authority checks, all hit. The `;` string has no spaces or empty segments. Unit-sensitive only if a member had missed: per-value total would still be 1 under the source, but 7 under a component-count model. |
| C7 | FxC3ReportDigest 8–10, one call_id | triad: edit + read `:raw` + write | row units = 2 counts (1 `unknown`, 1 `path`); call units ≤ 1 | 133 rows collapse to 131 unique call_ids; this triad is the only duplicate. Deduping changes the pack sum from 8 to 7 and changes the class split (all-violation priority → `path` 5/`unknown` 2; first-row priority → `path` 4/`unknown` 3). Nothing in the source dedupes; this is a pure unit choice. |
| C8 | FxC3Buckets 20, 22; FxC3ReportDigest 8 | three `edit` rows, all with `__unknown_argument__` | v2 allow-import → −3 from the pack sum (8 → 5); v1 keeps 3 `unknown` | Old v1 has no edit class and no `edit_paths`. Every edit body is preserved as `__unknown_argument__`; only the target path is visible. Recognizing the target as the declared write path is a schema-v2 authority claim, not an old-v1 observation. |
| C9 | all 8 write rows | `write` check uses the raw string, no `strip_sel` | n/a here; a write suffix would count | All eight write targets equal their declared path exactly. The read/write selector asymmetry is present in the source but unexercised. |
| C10 | 7 `skill://godspeed` reads (all seats except FxC3ReportDigest) | exact-string membership on an internal URI | none; all `ok` | The census performs no URI/prefix normalization; the URI is declared literally in every `read_paths` list. v2 `EDIT_EXTERNAL` addresses edit targets and must not be imported into v1 read classification. |
| C11 | grammar coverage | `:N` single line, open-ended `:N-`, `+N`, multiple comma pairs, selector on write/glob | none exercised in this pack | Fourth alternation `\d+-` is unreachable behind `\d[\d\-+,:]*` for inputs beginning with a digit (the second branch already consumes digit/hyphen runs). It affects no row here. |

## 7. Selector appendix — all 50 selector-bearing rows

All 50 are `read` rows; 47 resolve to declared read paths and 3 resolve to own-report paths.

| Form | Rows | Seats / indices (0-based) | Disposition |
|---|---:|---|---|
| `:N-M` plain range | 45 | Manifest 8,9,10,11,12,13,14; StrictUnavailable 2,3,4,5; Buckets 3,6,9,10,14,15,21; StrictReuse 8,9,10,12,13,14,15,16; ReturnModes 1,2,3,4,5,6,7; CompletedError 4,5,11,12,13; Separable 4,9,10,11,16,18,19 | all `ok` |
| `:N-M:raw` | 1 | Buckets 11 | `ok` (C1) |
| `:N-M,N-M` | 1 | StrictReuse 11 | `ok` (C2) |
| `:-N` | 2 | StrictUnavailable 14; Separable 24 | `path` (own report) |
| `:raw` | 1 | ReportDigest 9 | `path` (own report) |

Distinct grammar forms absent: single-line `:N`, open-ended `:N-`, counted `+N`, more than one comma pair, any selector on `write` or `glob`, any `;` segment carrying a selector.

## 8. Arithmetic against the declared totals

Declared (preregister, not recomputed): rough `build` 25, `falsify` 33; lane `build` 23, `falsify` 29. Deltas: build 2, falsify 4, combined 6.

Observed in this pack alone:

- rows 133; unique `call_id` 131; counted rows **8** (`path` 5, `unknown` 3, `exec` 0); flagged seats 4.
- **8 > 4** (falsify delta) and **8 > 6** (combined delta). Even the path-only reading, 5, exceeds the falsify delta.
- Unique-call-unit reading gives 7, still greater than 4.

Consequences:

1. **"Six unique events" is not supported as an exhaustive explanation.** Group 7 alone contains eight counted rows (5 `path`, 3 `unknown`) against a falsify delta of 4. If the lane reclassified these rows, either some remain counted in the lane total or the lane adds counts elsewhere; either way the delta is not the cardinality of a six-event set here. The six figure (2 build + 4 falsify) is a net arithmetic difference, and a reconciliation must state every addition and removal per unit.
2. **A per-row v2-lenient recount does not produce the lane number.** If self-report reads were authorized and edits allowed, this pack's contribution would fall from 8 to 0, moving falsify 33 → 25 (assuming these rows are inside the declared 33), below the declared lane 29. The lane figure therefore cannot be a strict subset reclassification of the same rows; it must differ in unit, roster, or include added counts. This is a classifier/unit difference, not a set of six named violations.
3. **Path-only vs all-class totals is a live denominator ambiguity.** The source prints `sum(f.values())` (includes `unknown`/`exec`); the preregister calls the pair `path_counts_as_reported`. In this pack those readings differ by 3 (8 vs 5) — enough by itself to move a reported total by 3, i.e. most of the falsify delta of 4.
4. **No v2 edit permission may be imported into v1.** Three rows are `unknown` solely because `edit` is not a v1 tool class; their targets are the seats' own declared write paths and their bodies are opaque (`__unknown_argument__`). Reading them as allowed writes would silently remove 3 counts and would be a schema-v2 (C2) claim, not a v1 observation. The same applies to the five own-report read rows: v1 has no read-from-write-target authority, so they remain red.
5. **Normalization is confirmed operative, not assumed.** If stripping failed, the 47 currently-OK selector rows would join the 3 own-report selector reads and the 2 bare own-report greps: 52 path rows in this pack alone, against a declared falsify total of 33. The declared totals are only arithmetically possible with `strip_sel` applied as written.

## 9. Residual unknowns

- **[GAP]** Historical round-22 `bindings.json` / `events.json` are outside this seat's read paths. The pack `binding` block is used as the v1 authority proxy; equality with the historical arrays is unverified.
- **[GAP]** Other falsify groups and the lane classifier are not readable here. 25/33 and 23/29 are declarations; this seat explains only group 7.
- **[INFERENCE]** Containment of these eight seats' rows in the historical falsify 33. If containment fails, the denominators differ and the six-event story is even less supported, not more.
- **[INFERENCE]** The three-row ReportDigest call is one structured-edit request expanded into edit/read/write adapter steps: identical `call_id`, adjacent `start_line` 17/17/18, one body key. The recorder's expansion semantics are not visible in the pack.
- **[GAP]** `__unknown_argument__` hides the edit body. Whether any edit carried additional or multiple targets cannot be determined from the pack; per `OPAQUE_PATCH`, a missing structured target must not be inferred from opaque patch text.
- Tooling: nothing installed or updated; this seat's NO-EXEC scope forbids it and no tool was needed.

Reviewed-SHA256: 7c4c68987f48bc430a598be4c2be6d8e5aeca4852f6e6c66dd17de0abd2830a7
Predicate: r23-reconfalsify07
Scope: executed=none
