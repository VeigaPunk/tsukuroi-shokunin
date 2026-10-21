# ReconBuild02 — round23 build group 02: rough-source vs old-v1 path authority, per-event

Seat: `TsukuroiR23-2.ReconBuild02-7` (leaf member; no subagent dispatch).
Wave group: build-02 (8 historical seats, all from round 22).

## 0. Method, scope, and what was NOT done

- Sources read (declared bound paths only): `.ufo/waves/round-23/packs/build-02.json` (full file, 737 lines),
  `.ufo/waves/round-23/preregister.json`, `.ufo/waves/round-23/sources/r22-rough-census.txt`,
  `.ufo/waves/round-23/sources/godspeed-directive.txt`, `skill://godspeed`.
- Pack digest `0a7d15d62d6229b9652d5d78457638c38461a79a7e751dc726157639337dca03` is a **supplied identity**;
  it was **not** recomputed, and no hash/list/wc/import/compile/test/lint was run.
- **NO-EXEC / NO-FETCH honored**: no bash, no eval, no subprocess, no web fetch, no filesystem search beyond the
  declared bound files. Every classification below is hand-derived from the *text* of the original rough census
  cell (reproduced verbatim in §1) and the *text* of the pack. No gate, counter, or checker was executed.
- The pack supplies **no expected classifications** ("Raw preserved request metadata only"), so every "rough"
  and "lane" column below is my own derivation, labelled as such, not a recorded expectation.
- **Scope limit (declared, not improvised):** the old-v1 lane authority text (`check-seat-bindings.py` v1 policy
  of round 22) is **not** inside this seat's declared read paths, so its exact normalization/authority semantics
  are *not* observable to me. I therefore express the lane side as **bounded hypotheses H1/H2/H3** over the three
  axes that can differ, and I do not assert which one the historical lane used. I do **not** import any r23 v2
  edit permission (`DECLARED_EDIT`, `EDIT_EXTERNAL`, `READ_ONLY_EDIT`, …) into the old-v1 reading: v1 authority
  here is only "listed path" authority as recorded in the pack's per-seat `binding`.

## 1. Axes named (godspeed)

| # | Axis | What can differ between rough source and old-v1 lane |
|---|------|--------------------------------------------------------|
| A1 | Selector normalization | rough strips a trailing selector (`strip_sel`) for **read/grep only**; lane v1 may strip for all tools, for none, or with a different selector grammar |
| A2 | Order / component split | rough splits `;`-joined paths for grep/glob and checks components in order; lane may check per component and count each |
| A3 | One-per-event break | rough `break`s after the first offending component → at most one `path` hit per event |
| A4 | Tool classification | rough buckets `bash`→`exec`, and anything not in {read,grep,glob,write} → `unknown`; **edit lands in `unknown`**, not `path` |
| A5 | Authority scope | rough checks `write` against `write_paths`, and read/grep/glob against `read_paths` **only**; lane v1 may treat a declared write target as readable, or may require containment under `root` |
| A6 | Unit | rough reports a **bucket map plus a total**; the reported outside figure may be the `path` bucket or the **sum of all buckets** (exec+unknown+path) |
| A7 | Event granularity | rough evaluates **each recorded event**; a lane keyed on request/`call_id` sees one unit where rough sees several (adapter-expanded steps) |
| A8 | URI class | `skill://godspeed` is a non-filesystem URI that rough matches **literally** against `read_paths` |

## 2. Exact original rough source algorithm (verbatim from `sources/r22-rough-census.txt`)

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

Consequences that matter for every row below (derived by reading the cell, not by running it):

1. `strip_sel` is applied **only** when `t in ('read','grep')`. A `write` or `glob` path is compared **verbatim**.
2. `strip_sel` removes exactly one trailing selector of the forms `:raw`, `:<digits><[-+,:]digits…>`, `:-<digits>`,
   `:<digits>-`; the optional `(:raw)?` tail is consumed too, so `:1-40:raw` is fully removed in one match.
3. `edit` is **not** in the handled set → each `edit` event increments `unknown` (and marks the seat), never `path`.
4. `read`/`grep`/`glob` are checked against **`read_paths` only**; `write` against **`write_paths` only**.
   There is no `write_paths` fallback for a read, and no `read_paths` requirement for a write.
5. Membership is **exact string equality** against the declared absolute path lists.
6. `grep`/`glob` paths are split on `;` and each component tested; the `break` makes the hit **at most one per event**
   (A3). `read`/`write` are never split.
7. `str(a.get('path',''))` — an event with no `path` key yields `''`, which is in neither list → `path` hit.
   (No such event in this pack.)

## 3. Per-seat, per-event hand-derived table (38 events, all 8 seats)

Legend — Rough verdict (mine, from the cell above): `OK` = listed & allowed; `PATH` = increments `f['path']`;
`UNK` = increments `f['unknown']`; `EXEC` = increments `f['exec']`.
`Lane?` = whether an old-v1 lane could disagree, with the hypothesis tag from §4.

Suffix column = the **raw path suffix exactly as recorded** (empty = bare path).

### 3.1 OracleExecTask — agent `TsukuroiR22.OracleExecTask-3` (6 events)
Declared: read `[.../round-22/sources/host-tool-boundary.json, .../round-22/preregister.json, skill://godspeed]`;
write `[.../round-22/build/OracleExecTask.md]`.

| idx | tool | call_id | req/line | raw path suffix | Rough | Lane? |
|-----|------|---------|----------|-----------------|-------|-------|
| 0 | read | `call_00_ET_n0otY4cTT5jOigEGSRkS1913` | 13 / 14 | (none) | OK | A8 only (filesystem path, listed) |
| 1 | read | `call_01_ET_9ZVqKwUwoiZ1maus9y3A7549` | 13 / 15 | (none) | OK | A8 only |
| 2 | read | `call_02_ET_weJ4cYYgHLWD3rqgfGNo9473` | 13 / 16 | (none) — `skill://godspeed` | OK | **A8** — URI matched literally; a lane requiring filesystem containment would count it |
| 3 | read | `call_00_idcKr70fMxcFA2OpykWn9073` | 20 / 21 | `:1-40:raw` | OK | **A1** — rough strips → listed; H3 (no strip) counts it as a lane hit |
| 4 | read | `call_01_iYzBjSkGEMHDLzqZff607943` | 20 / 22 | `:1-40:raw` | OK | **A1** — same as idx 3 |
| 5 | write | `call_00_n8UmcKzsKIVtqutIfkuH0459` | 25 / 26 | (none) | OK | A5 — write target is in `write_paths`; no selector present, so rough's no-strip-for-write rule is inert here |

### 3.2 OracleExecAsync — `TsukuroiR22.OracleExecAsync-3` (4 events)
Same declared read list; write `[.../round-22/build/OracleExecAsync.md]`.

| idx | tool | call_id | req/line | raw path suffix | Rough | Lane? |
|-----|------|---------|----------|-----------------|-------|-------|
| 0 | read | `call_d76d1033bad6464286587c21` | 17 / 18 | (none) — `skill://godspeed` | OK | **A8** |
| 1 | read | `call_e36fd9dd0dfa4ed6b6590ce9` | 17 / 19 | (none) | OK | — |
| 2 | read | `call_9258c03ea45c438da5c5fece` | 17 / 20 | (none) | OK | — |
| 3 | write | `call_2b0d04fa04354f74b7eba8e8ac795214|fc_0fc3cea299f7c74a016ad8d0765a188191aed675a8c529ea31` | 28 / 29 | (none) | OK | A7 — compound `call_id` (`…|fc_…`); a lane keyed on the request rather than the recorded event sees one unit |

### 3.3 OracleFetchHTTPS — `TsukuroiR22.OracleFetchHTTPS-3` (5 events)
Same declared read list; write `[.../round-22/build/OracleFetchHTTPS.md]`.

| idx | tool | call_id | req/line | raw path suffix | Rough | Lane? |
|-----|------|---------|----------|-----------------|-------|-------|
| 0 | read | `toolu_01TNvsKkayUqiNVfWJBTD3ui` | 14 / 9 | (none) | OK | — |
| 1 | read | `toolu_01Mmc3jAHUxCTHPZb5cFm32h` | 14 / 10 | (none) | OK | — |
| 2 | **edit** | `toolu_018MtbybV9AAieTGyATnJU97` | 14 / 11–12 | (none) — path = own write target | **UNK** | **A4** — rough puts `edit` in `unknown`; a lane that classifies `edit` as a path event would count it as `path` (lane > rough). Args are opaque (`__unknown_argument__`: null) but `path` **is** present |
| 3 | read | `toolu_018MtbybV9AAieTGyATnJU97` (`origin: additional-recorded-start`, `request_line: null`) | – / 11 | `:raw` | **PATH** | **A1+A5** — after strip the path equals the seat's own `write_paths` entry, which is **not** in `read_paths` → rough hit. Under H1 (write target readable) lane = 0; under H2 lane = 1; under H3 the unstripped `:raw` form is also a hit → 1. Also **A7**: same `call_id` as idx 2 and idx 4 → one request, three recorded adapter steps |
| 4 | write | `toolu_018MtbybV9AAieTGyATnJU97` (`origin: additional-recorded-start`) | – / 12 | (none) | OK | A5/A7 — listed in `write_paths`; per-call lane sees one unit for idx 2–4 |

### 3.4 OracleFetchHTTP — `TsukuroiR22.OracleFetchHTTP-3` (4 events)
Same declared read list; write `[.../round-22/build/OracleFetchHTTP.md]`.

| idx | tool | call_id | req/line | raw path suffix | Rough | Lane? |
|-----|------|---------|----------|-----------------|-------|-------|
| 0 | read | `call_6b541fbad7924ed8b448da21` | 15 / 16 | (none) | OK | — |
| 1 | read | `call_38b9c514fda549aca2081460` | 15 / 17 | (none) | OK | — |
| 2 | read | `call_e75745953d2445e28a246f6b` | 15 / 18 | (none) — `skill://godspeed` | OK | **A8** |
| 3 | write | `call_8a4cd48fb17846408daa69a5` | 22 / 23 | (none) | OK | — |

### 3.5 OracleFetchSearch — `TsukuroiR22.OracleFetchSearch-3` (4 events)
Same declared read list; write `[.../round-22/build/OracleFetchSearch.md]`.

| idx | tool | call_id | req/line | raw path suffix | Rough | Lane? |
|-----|------|---------|----------|-----------------|-------|-------|
| 0 | read | `call_00_ET_o7KgT5DI3lIwKY4wvcaY3276` | 13 / 14 | (none) | OK | — |
| 1 | read | `call_01_ET_UWrnTXFgxyoxIkg3mMeg9762` | 13 / 15 | (none) | OK | — |
| 2 | read | `call_02_ET_IY2NIc6PGojoj6UIyXlE1015` | 13 / 16 | (none) — `skill://godspeed` | OK | **A8** |
| 3 | write | `call_00_j5GL4ScNbYCOkELjl48i2867` | 20 / 21 | (none) | OK | — |

### 3.6 OracleFetchBrowser — `TsukuroiR22.OracleFetchBrowser-3` (4 events)
Same declared read list; write `[.../round-22/build/OracleFetchBrowser.md]`.

| idx | tool | call_id | req/line | raw path suffix | Rough | Lane? |
|-----|------|---------|----------|-----------------|-------|-------|
| 0 | read | `call_388595e1b04b4fa2bcedf45c5f89e8c4|fc_013fd128b667a02e016ad8cf103690819195ed8339858c05f0` | 10 / 12 | (none) — `skill://godspeed` | OK | **A8**, plus A7 (compound `call_id`) |
| 1 | read | `call_637e5987078341d2975ae0d7090851c2|fc_013fd128b667a02e016ad8cf1426f081919240de8b00b64c2b` | 10 / 13 | `:1-220` | OK | **A1** — rough strips → listed; H3 counts a lane hit |
| 2 | read | `call_c6ef32de643d4872ad583e36e93a07b5|fc_013fd128b667a02e016ad8cf1426f48191abc5e50972f487d2` | 10 / 14 | `:1-220` | OK | **A1** — same as idx 1 |
| 3 | write | `call_c2b75f12461441b5a303bae6716fb75a|fc_013fd128b667a02e016ad8cf4febf881918b3b8bd204cfd5fa` | 18 / 19 | (none) | OK | A7 (compound `call_id`) |

### 3.7 OracleFetchInternal — `TsukuroiR22.OracleFetchInternal-3` (4 events)
Same declared read list; write `[.../round-22/build/OracleFetchInternal.md]`.

| idx | tool | call_id | req/line | raw path suffix | Rough | Lane? |
|-----|------|---------|----------|-----------------|-------|-------|
| 0 | read | `call_8d4a9f1528e647cfb069de2f` | 13 / 14 | (none) — `skill://godspeed` | OK | **A8** |
| 1 | read | `call_a4ad5672b53f4d728c20a3ee` | 13 / 15 | (none) | OK | — |
| 2 | read | `call_cee3b6140637411b953e3666` | 13 / 16 | (none) | OK | — |
| 3 | write | `call_3b2223854876415a9f12915c` | 21 / 22 | (none) | OK | — |

### 3.8 OracleFetchBare — `TsukuroiR22.OracleFetchBare-3` (7 events)
Same declared read list; write `[.../round-22/build/OracleFetchBare.md]`.

| idx | tool | call_id | req/line | raw path suffix | Rough | Lane? |
|-----|------|---------|----------|-----------------|-------|-------|
| 0 | read | `call_00_ET_U3VHAVYWD8iGKrDxpga74761` | 13 / 14 | (none) | OK | — |
| 1 | read | `call_01_ET_JzXM4NojxdPdW2PWQ84V3191` | 13 / 15 | (none) | OK | — |
| 2 | read | `call_00_iu53mPOXudJzf9qTReM49469` | 18 / 19 | (none) — `skill://godspeed` | OK | **A8** |
| 3 | write | `call_00_cHxo2le46y9o1QyQJ0Pk1188` | 21 / 22 | (none) | OK | — |
| 4 | **edit** | `call_00_m17SxefZUDWU5E91fz7t4028` | 24 / 25 | (none) — path = own write target | **UNK** | **A4** — `unknown` bucket under rough; a lane classifying `edit` as a path event would count it (lane > rough). Args opaque (`__unknown_argument__`: null) |
| 5 | read | `call_00_tZlvYBWHU0EwHlfAxZiz3192` | 27 / 28 | `:60-120` | **PATH** | **A1+A5** — after strip the path equals the seat's own `write_paths` entry, absent from `read_paths` → rough hit. H1 → lane 0; H2 → 1; H3 → 1 (unstripped `:60-120` also unmatched) |
| 6 | read | `call_01_FWnna5uFzjMkARCe6N6C0152` | 27 / 29 | `:-8` | **PATH** | **A1+A5** — same shape as idx 5 (`:‑8` is consumed by the `-\d+` branch of `strip_sel`). Same request line 27 as idx 5 → A7 (per-request vs per-event unit) |

## 4. Bounded lane hypotheses and this pack's contribution under each

Three hypotheses span the axes that can actually differ here; the historical lane's exact text is outside my
read scope, so I do not pick one — I bound the arithmetic each would force.

- **H1 — write target implies read authority** (lane lets a seat read a path it may write), lane still strips selectors.
- **H2 — lane strips selectors and requires `read_paths` for reads** (same authority scope as rough).
- **H3 — lane does not strip selectors** (raw path compared verbatim).

Derived `path`-bucket counts for **this pack only** (build group 02, 38 events):

| Hypothesis | Lane `path` hits in pack | Rough `path` hits in pack | Rough − Lane (pack) |
|---|---|---|---|
| H1 | 0 (HTTPS idx3, Bare idx5, Bare idx6 all become allowed) | 3 | **+3** |
| H2 | 3 (same three events) | 3 | 0 |
| H3 | 7 (the three above + ExecTask idx3/idx4 + Browser idx1/idx2) | 3 | **−4** |

Rough buckets for this pack, from the cell's logic: `exec` = 0, `unknown` = 2 (the two `edit` events),
`path` = 3, **total = 5**, seats marked = 2 (`OracleFetchHTTPS`, `OracleFetchBare`).

### 4.1 The gap cannot be closed from this pack alone

Outside figures as declared in `preregister.json` (`outside_round22.path_counts_as_reported`): rough
build **25** / falsify **33**; lane build **23** / falsify **29**. Deltas: **build −2**, **falsify −4**
(rough minus lane), i.e. **6 in total — but 2 in one cohort and 4 in another, not six unique events.**
Concrete refusals of the tempting shortcuts:

1. **This pack contains no falsify seat at all.** Every one of the 8 seats here is a round-22 *build*-wave oracle
   (`.../round-22/build/…` write targets). The falsify delta of 4 has **no source in this pack** and must be
   explained from the falsify cohort's own evidence; I do not extrapolate.
2. **The build delta of 2 is smaller than this pack's H1 contribution of 3.** So either (a) the lane is not H1,
   (b) H1 holds for at most 2 of the 3 candidate events, or (c) the lane's build count is offset by other
   build groups (build-01, …) that are outside this pack. All three remain open; the pack alone cannot close them.
3. **Unit ambiguity (A6) can absorb the whole build delta.** The cell prints *both* a bucket map and
   `sum(f.values())`. If the outside 25 is the **total** (exec+unknown+path) rather than the `path` bucket,
   then the two `unknown` hits contributed by the two `edit` events in this pack (HTTPS idx2, Bare idx4) are
   counted in 25 but would be invisible to a lane that reports only path violations. This pack's `unknown`
   count of 2 equals the build delta of 2 exactly — a *coincidence-sized* fit, not a proof; it must be checked
   against the falsify cohort's unknown/exec profile before it may be stated as the explanation.
4. **H3 is ruled out as the sole explanation of the sign**: it would make lane (7) exceed rough (3) in this pack,
   i.e. the wrong direction for both cohorts (rough is *higher* than lane in both build and falsify).
5. **The `edit` events are the only A4 divergence in this pack.** Under H2/H1/H3 the two `edit` events are
   `unknown` for rough; a lane that treats `edit` as a path-classified tool (with the target listed in
   `write_paths`, so allowed under a write-target-implies-write reading) adds 0 hits; a lane that treats
   `edit` as needing `read_paths` adds 2 hits — again the wrong direction unless the lane's `edit` rule is
   permissive. Note the r23 v2 decisions (`DECLARED_EDIT`/`READ_ONLY_EDIT`/`WRITE_ONLY_EDIT`) are **new** policy
   and are deliberately **not** applied here.

### 4.2 Axes that are provably inert in this pack (bounded negative findings)

- **A2 (order) and A3 (one-per-event break)**: this pack contains **zero** `grep`, **zero** `glob`, **zero**
  `bash`, and **zero** `;`-joined or multi-component path events. Every event has exactly one path component,
  so rough's `break` can never suppress a second hit, and component order is never exercised. Any build-cohort
  difference attributed to A2/A3 must originate in **other** build groups, not here.
- **A1 for `write`/`glob`**: rough's "strip only for read/grep" rule is inert for writes here — **no** `write`
  event in this pack carries a selector suffix. It would bite only on a write/glob path ending in `:raw` or
  `:N-M`, and no such event exists in this pack.
- **Missing-path events**: every event in this pack carries a `path` key, so the `''`→`path`-hit branch is
  never taken.
- **Seat-level `seats` counter**: rough marks a seat only when it records a hit; under rough only
  `OracleFetchHTTPS` and `OracleFetchBare` are marked here. The pack's own seats are all "oracle" seats whose
  entire write target is their own report file.

## 5. Candidate divergence register (the requested enumeration)

Every candidate event/component in this pack where rough and an old-v1 lane can differ, with seat, event index,
call_id, raw path suffix, and bounded reason. **No candidate is asserted as *the* cause of the cohort delta.**

| # | seat | idx | tool | call_id | raw path suffix | axis | bounded reason |
|---|------|-----|------|---------|-----------------|------|----------------|
| C1 | OracleFetchHTTPS | 2 | edit | `toolu_018MtbybV9AAieTGyATnJU97` | (none) | A4 | rough routes `edit` to `unknown`; a lane classifying edit as a path event counts it instead — direction lane > rough |
| C2 | OracleFetchHTTPS | 3 | read | `toolu_018MtbybV9AAieTGyATnJU97` | `:raw` | A1+A5 | after `strip_sel` the path equals the seat's own `write_paths` entry, absent from `read_paths` → rough `path` hit; lane differs iff write-target-implies-read (H1) or iff it does not strip (H3) |
| C3 | OracleFetchHTTPS | 4 | write | `toolu_018MtbybV9AAieTGyATnJU97` | (none) | A7 | adapter-expanded step sharing one `call_id` with idx 2–3; per-event vs per-request unit changes how many units the seat contributes |
| C4 | OracleFetchBare | 4 | edit | `call_00_m17SxefZUDWU5E91fz7t4028` | (none) | A4 | same as C1 for the second edit event |
| C5 | OracleFetchBare | 5 | read | `call_00_tZlvYBWHU0EwHlfAxZiz3192` | `:60-120` | A1+A5 | stripped form is the seat's own write target, not in `read_paths` → rough `path` hit; H1 lane = 0, H2/H3 lane = 1 |
| C6 | OracleFetchBare | 6 | read | `call_01_FWnna5uFzjMkARCe6N6C0152` | `:-8` | A1+A5 | `-\d+` branch of `strip_sel` consumes `:-8`; same shape as C5; also same request line 27 as C5 (A7) |
| C7 | OracleExecTask | 3 | read | `call_00_idcKr70fMxcFA2OpykWn9073` | `:1-40:raw` | A1 | rough strips the selector and the file is listed → no hit; a no-strip lane (H3) counts a hit here — direction lane > rough |
| C8 | OracleExecTask | 4 | read | `call_01_iYzBjSkGEMHDLzqZff607943` | `:1-40:raw` | A1 | same as C7 |
| C9 | OracleFetchBrowser | 1 | read | `call_637e5987078341d2975ae0d7090851c2|fc_013fd128b667a02e016ad8cf1426f081919240de8b00b64c2b` | `:1-220` | A1 | same shape as C7/C8 |
| C10 | OracleFetchBrowser | 2 | read | `call_c6ef32de643d4872ad583e36e93a07b5|fc_013fd128b667a02e016ad8cf1426f48191abc5e50972f487d2` | `:1-220` | A1 | same shape as C7/C8 |
| C11 | OracleExecTask | 2 | read | `call_02_ET_weJ4cYYgHLWD3rqgfGNo9473` | (none) — `skill://godspeed` | A8 | non-filesystem URI matched literally by rough; a lane requiring root containment would count it |
| C12 | OracleExecAsync | 0 | read | `call_d76d1033bad6464286587c21` | (none) — `skill://godspeed` | A8 | same as C11 |
| C13 | OracleFetchHTTP | 2 | read | `call_e75745953d2445e28a246f6b` | (none) — `skill://godspeed` | A8 | same as C11 |
| C14 | OracleFetchSearch | 2 | read | `call_02_ET_IY2NIc6PGojoj6UIyXlE1015` | (none) — `skill://godspeed` | A8 | same as C11 |
| C15 | OracleFetchBrowser | 0 | read | `call_388595e1b04b4fa2bcedf45c5f89e8c4|fc_013fd128b667a02e016ad8cf103690819195ed8339858c05f0` | (none) — `skill://godspeed` | A8+A7 | same as C11, plus compound `call_id` |
| C16 | OracleFetchInternal | 0 | read | `call_8d4a9f1528e647cfb069de2f` | (none) — `skill://godspeed` | A8 | same as C11 |
| C17 | OracleFetchBare | 2 | read | `call_00_iu53mPOXudJzf9qTReM49469` | (none) — `skill://godspeed` | A8 | same as C11 |

Grouping by axis (for the C3 reconciliation record): A1 → C2, C5, C6, C7, C8, C9, C10 (7 events);
A4 → C1, C4 (2 events); A5 → C2, C5, C6 (3 events); A7 → C3, C6, C15 (3 events);
A8 → C11–C17 (7 events). A2/A3: no candidates in this pack.

**Coarse reading of the register:** A1 and A8 dominate the *candidate* population (7 events each), but A1's
per-event effect on the `path` bucket is **+1 for rough under H1/H2 and −1 under H3** for the listed-read rows
(C7–C10), whereas the three read-of-own-write-target rows (C2, C5, C6) are the only rows that can push rough
**above** lane under H1. The only A4 rows (C1, C4) push lane **above** rough if a lane treats edit as a path
event, and push rough's *total* above lane's *path* figure if the outside number is the bucket total.
Therefore, in this pack, the directionally-correct (rough > lane) candidates are exactly
{C2, C5, C6} under H1, plus {C1, C4} under the A6 total-vs-bucket reading — and the pack supports at most
**2** build-delta units under any single reading, which is why the build delta of 2 must not be attributed to
"three unique events" here.

## 6. Residual risk and verification gaps

1. **Lane policy text unobserved.** The old-v1 lane authority (round-22 `check-seat-bindings.py` v1 semantics) is
   not in this seat's declared read paths. H1/H2/H3 therefore remain hypotheses; only the *rough* side of every
   table above is source-derived. This is a declared gap, not improvised around.
2. **Falsify cohort unrepresented.** The falsify delta (rough 33 vs lane 29) cannot be touched from a build-only
   pack; no falsify seat, no falsify binding, no falsify event appears in `build-02.json`.
3. **Unit of the outside figure unresolved.** `path_counts_as_reported` does not say whether 25/33 are the `path`
   bucket or `sum(f.values())`; the cell prints both. Until that is pinned from the recorded r22 evidence, the
   build delta of 2 can be explained by at least three mutually exclusive mechanisms (§4.1 items 2–4).
4. **Other build groups unexamined.** This pack is group 02; the A2/A3 candidates and any additional
   selector/unknown rows live in the remaining groups, which are outside this seat's bound.
5. **Recorded adapter steps are not per-request.** `origin: additional-recorded-start` rows carry
   `request_line: null`; their relationship to the parent request is asserted only by shared `call_id`.
6. **No re-execution.** Nothing here was run; every number in §4 is hand-derived from the cell's text. If a later
   lane decides to execute the census cell for confirmation, that is a separate, explicitly authorised step —
   this seat did not and could not perform it under NO-EXEC.
