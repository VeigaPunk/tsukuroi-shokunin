# ReconFalsify04 — r23 falsify group 4 independent path-oracle reconciliation slice

Seat: ReconFalsify04 (leaf reviewer/scout) · wave falsify · group 4 · pack `falsify-04.json` · execution state: none (no gate, counter, checker, or census run; no command, no fetch).

## 0. Inputs actually read (declared scope only)

| Input | Path | Use |
|---|---|---|
| Pack | `.ufo/waves/round-23/packs/falsify-04.json` (1840 lines, 8 seats) | seat bindings + raw preserved request metadata |
| Preregister | `.ufo/waves/round-23/preregister.json` | declared outside r22 counts, C3 scope, edit_decisions |
| Rough source (as data) | `.ufo/waves/round-23/sources/r22-rough-census.txt` | the exact original rough census algorithm text |
| Directive | `.ufo/waves/round-23/sources/godspeed-directive.txt`, `skill://godspeed` | posture |

Pack digest `9e31fc0b1615a8b70d177a777d1e29f59f064d1b06130e9fe0bfac482701fb19` is **supplied identity, not independently computed**: no hash, list, wc, import, or command was run to validate it. Nothing was executed from the rough source; it was read as data only.

Not readable under this seat's declared read paths, and therefore not read: `round-22/candidate/tools/check-seat-bindings.py` (the "lane" v1 checker), `round-22/*/events.json`, `round-22/*/bindings.json`, and the other falsify groups' packs. Consequences are recorded as verification gaps in §7.

## 1. Axes named (godspeed)

- **A1 selector-normalization fidelity** — does the authority's trailing-selector stripping coincide with the rough source's `strip_sel`?
- **A2 authority-list selection/order** — which declared list (read vs write) is consulted, in which order, and is a URI matched literally or resolved?
- **A3 one-per-event break / component granularity** — is a violating event counted once, and are per-component violations inside one event counted once or many times?
- **A4 tool-scope coverage** — tools outside the rough whitelist (`bash` → exec, everything else → unknown) are counted without any path check.
- **A5 event identity granularity** — one recorded event vs one recorded call: the pack contains multiple recorded entries sharing one `call_id`, and `origin: additional-recorded-start` entries.

Keep-moves must improve an axis and harm none. No production, VCS, fleet, host, or route state was touched; the only artifact written is this report.

## 2. Declared constants (frozen inputs)

From `preregister.json` → `outside_round22.path_counts_as_reported`:

| cohort | rough | lane | difference (counted units) |
|---|---|---|---|
| r22 build | 25 | 23 | 2 |
| r22 falsify | 33 | 29 | 4 |
| total | 58 | 52 | **6** |

Preregister scope note (verbatim intent): *"Given outside observations are ground truth; r23 explains classifier/unit differences rather than rerunning closure merely to confirm them."* C3 requires *"exhaustive per-event/component explanation of rough-versus-lane path counts"* and explicitly *"does not relabel old violations or retry historic checks for confirmation."*

## 3. The exact original rough source algorithm (as data, never executed)

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

Behavioural properties that matter for reconciliation (all hand-derived, all re-checkable by reading, none executed):

1. **P1 (A3)** — the `break` is inside the component loop: **at most one `path` unit per event**, and only the *first* violating component of a multi-component `;`-path is counted. A seat's `path` unit count is therefore *events*, not components.
2. **P2 (A4)** — `bash` → `exec`; any tool not in `('read','grep','glob','write')` → `unknown`. Both `continue`, so **no path check is ever performed** on such an event, even when its `path` argument is perfectly declared.
3. **P3 (A2)** — the authority list is chosen by tool family: `write` → `write_paths` only; `read`/`grep`/`glob` → `read_paths` only. There is **no** read-after-write allowance, no union, no prefix/dir containment, no realpath, no trailing-slash tolerance, no symlink resolution: membership is exact string equality in a list.
4. **P4 (A1)** — `strip_sel` is applied to `read` and `grep` paths only; **`glob` paths are never normalized**. The regex tolerates `:N`, `:N-M`, `:N-M:raw`, `:-N`, `:raw`, `:N,M`, `:N-M,P-Q`; it does **not** tolerate any other trailing colon form.
5. **P5 (A2)** — `skill://godspeed` is compared **literally**; no URI→filesystem resolution occurs, so a URI matches only because the binding declares the identical URI string.
6. **P6 (A5)** — iteration is over recorded event entries; duplicate `call_id` entries (see §5, `FxC2Unknown`) are counted separately unless the lane dedupes by call.

## 4. Group-4 raw census, hand-derived from the pack

Totals for this pack's 8 seats / **108 recorded events**:

| rough counter | count | seats flagged |
|---|---|---|
| `exec` (bash) | 0 | — |
| `unknown` (tool outside whitelist) | 1 | `FxC2Unknown` |
| `path` (event with a violating path) | 3 | `FxC2ReadWrite`, `FxC2Unknown` |
| **sum** | **4** | **2 of 8 seats** |

Instrument census of this pack's 108 events (hand-derived): `read` = 96, `grep` = 11, `write` = 8, `edit` = 1, `bash` = 0, `glob` = 0. **No `;`-joined multi-component path occurs in this pack**, so P1's component-granularity branch is *not exercised* here; the only live P1 effect is "one unit per violating event".

Per-seat event counts: `FxC2Wildcard` 12, `FxC2Report` 16, `FxC2ReadWrite` 20, `FxC2Unknown` 8, `FxC2ParallelExec` 12, `FxC2ParallelFetch` 8, `FxC2ParallelLocal` 16, `FxC2Shape` 16.

Seat-name note (label vs recorded content): the seat named `FxC2ParallelExec` records **no** `bash` event — all 12 of its events are `read`/`grep`/`write` — so its name does not imply an exec unit in this pack; and `FxC2ParallelFetch` records no `web_search`/fetch-shaped tool either (its 8 events are `read`×7 + `write`×1). Name-implied categories must not be counted.

## 5. Exhaustive per-event table (108/108) and per-seat bindings

Shorthand (all under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/`): `<SSB>` = `candidate/tools/check-seat-bindings.py`; `<CRS>` = `candidate/tools/check-review-snapshots.py`; `<REV>` = `candidate/tools/_revision.py`; `<SBJ>` = `candidate/corpus/knowledge/seat-boundary-r22.json`; `<SBM>` = `candidate/corpus/knowledge/seat-boundary-r22.md`; `<PRE>` = `preregister.json`; `<HTB>` = `sources/host-tool-boundary.json`; `<GS>` = `skill://godspeed`; `<OWN>` = `falsify/<seat>.md`. "raw suffix" = the literal trailing portion of the recorded path string, selector included.

Every seat in this pack declares the **same** v1 authority:

- `read_paths` = { `<SSB>`, `<PRE>`, `<HTB>`, `<GS>`, `<CRS>`, `<REV>`, `<SBJ>`, `<SBM>` } (8 entries)
- `write_paths` = { `falsify/<own seat>.md` } (1 entry)
- `commands` = [], `fetches` = []

Consequences that hold for all 8 seats: the seat's own report path is **not** in `read_paths`; no other seat's report path is in any list; `skill://godspeed` is in `read_paths` for all 8.

### 5.1 FxC2Wildcard (12 events) — agent `TsukuroiR22.FxC2Wildcard-2`
| idx | tool | raw suffix | rough class | tags |
|---|---|---|---|---|
|0|read|`skill://godspeed`|allowed|URI|
|1|read|`<SSB>`|allowed|—|
|2|read|`<PRE>`|allowed|—|
|3|read|`<HTB>`|allowed|—|
|4|read|`<CRS>`|allowed|—|
|5|read|`<REV>`|allowed|—|
|6|read|`<SBJ>`|allowed|—|
|7|read|`<SBM>`|allowed|—|
|8|read|`<SSB>:1-100`|allowed|NORM|
|9|read|`<SSB>:101-200`|allowed|NORM|
|10|read|`<SSB>:201-330`|allowed|NORM|
|11|write|`<OWN>`|allowed|—|

Rough: 0 units.

### 5.2 FxC2Report (16 events) — agent `TsukuroiR22.FxC2Report-2`
| idx | tool | raw suffix | rough class | tags |
|---|---|---|---|---|
|0|read|`skill://godspeed`|allowed|URI|
|1|read|`<SSB>`|allowed|—|
|2|read|`<PRE>`|allowed|—|
|3|read|`<HTB>`|allowed|—|
|4|read|`<SSB>:1-120`|allowed|NORM|
|5|read|`<SSB>:121-260`|allowed|NORM|
|6|read|`<SBJ>`|allowed|—|
|7|read|`<SBM>`|allowed|—|
|8|read|`<SSB>:20-62:raw`|allowed|NORM|
|9|read|`<SSB>:62-112:raw`|allowed|NORM|
|10|read|`<REV>`|allowed|—|
|11|read|`<CRS>`|allowed|—|
|12|grep|`<SSB>`|allowed|—|
|13|grep|`<SSB>`|allowed|—|
|14|grep|`<SSB>`|allowed|—|
|15|write|`<OWN>`|allowed|—|

Rough: 0 units.

### 5.3 FxC2ReadWrite (20 events) — agent `TsukuroiR22.FxC2ReadWrite-2`
| idx | tool | raw suffix | rough class | tags |
|---|---|---|---|---|
|0|read|`<SSB>`|allowed|—|
|1|read|`skill://godspeed`|allowed|URI|
|2|read|`<SSB>:1-120`|allowed|NORM|
|3|read|`<SSB>:121-260`|allowed|NORM|
|4|read|`<SBM>`|allowed|—|
|5|read|`<SBJ>`|allowed|—|
|6|read|`<REV>`|allowed|—|
|7|read|`<CRS>`|allowed|—|
|8|read|`<PRE>`|allowed|—|
|9|read|`<HTB>`|allowed|—|
|10|read|`<SSB>:86-125:raw`|allowed|NORM|
|11|read|`<SSB>:126-165:raw`|allowed|NORM|
|12|read|`<SSB>:166-241:raw`|allowed|NORM|
|13|grep|`<SSB>`|allowed|—|
|14|grep|`<SSB>`|allowed|—|
|15|grep|`<SBM>`|allowed|—|
|16|read|`<SSB>:1-32:raw`|allowed|NORM|
|17|write|`<OWN>`|allowed|—|
|18|read|`<OWN>:-12`|**path violation**|NORM,ORDER,BRK|
|19|grep|`<OWN>`|**path violation**|ORDER,BRK|

Rough: 2 `path` units (idx 18, 19).

### 5.4 FxC2Unknown (8 events) — agent `TsukuroiR22.FxC2Unknown-2`
| idx | tool | raw suffix | rough class | tags |
|---|---|---|---|---|
|0|read|`<SSB>`|allowed|—|
|1|read|`<PRE>`|allowed|—|
|2|read|`<HTB>`|allowed|—|
|3|read|`<SBM>`|allowed|—|
|4|read|`<SBJ>`|allowed|—|
|5|edit|`<OWN>` (`__unknown_argument__`: null)|**unknown unit (no path check performed)**|SCOPE,CALLID|
|6|read|`<OWN>:raw`|**path violation**|NORM,ORDER,BRK,CALLID|
|7|write|`<OWN>`|allowed|CALLID|

Rough: 1 `unknown` + 1 `path` unit. Note idx 5, 6 and 7 all carry `call_id` `toolu_01XhhyTUnroyCin946g7BbTg`; idx 6 and 7 are `origin: additional-recorded-start` entries for that same call.

### 5.5 FxC2ParallelExec (12 events) — agent `TsukuroiR22.FxC2ParallelExec-2`
| idx | tool | raw suffix | rough class | tags |
|---|---|---|---|---|
|0|read|`skill://godspeed`|allowed|URI|
|1|read|`<SSB>`|allowed|—|
|2|read|`<SBM>`|allowed|—|
|3|read|`<SSB>:22-120`|allowed|NORM|
|4|read|`<SSB>:120-230`|allowed|NORM|
|5|read|`<HTB>`|allowed|—|
|6|read|`<SSB>:1-21`|allowed|NORM|
|7|read|`<SSB>:233-241`|allowed|NORM|
|8|read|`<PRE>`|allowed|—|
|9|read|`<REV>`|allowed|—|
|10|grep|`<SSB>`|allowed|—|
|11|write|`<OWN>`|allowed|—|

Rough: 0 units (no `bash` event recorded despite the seat name).

### 5.6 FxC2ParallelFetch (8 events) — agent `TsukuroiR22.FxC2ParallelFetch-2`
| idx | tool | raw suffix | rough class | tags |
|---|---|---|---|---|
|0|read|`skill://godspeed`|allowed|URI|
|1|read|`<SSB>:1-240`|allowed|NORM|
|2|read|`<PRE>:1-220`|allowed|NORM|
|3|read|`<HTB>:1-200`|allowed|NORM|
|4|read|`<SBJ>:1-220`|allowed|NORM|
|5|read|`<SBM>:1-200`|allowed|NORM|
|6|read|`<CRS>:1-220`|allowed|NORM|
|7|write|`<OWN>`|allowed|—|

Rough: 0 units. All 8 `call_id`s are compound (`call_<id>|fc_<id>`), one per recorded event; no shared call collapses two events here.

### 5.7 FxC2ParallelLocal (16 events) — agent `TsukuroiR22.FxC2ParallelLocal-2`
| idx | tool | raw suffix | rough class | tags |
|---|---|---|---|---|
|0|read|`<SSB>`|allowed|—|
|1|read|`<PRE>`|allowed|—|
|2|read|`<HTB>`|allowed|—|
|3|read|`skill://godspeed`|allowed|URI|
|4|read|`<CRS>`|allowed|—|
|5|read|`<REV>`|allowed|—|
|6|read|`<SBJ>`|allowed|—|
|7|read|`<SBM>`|allowed|—|
|8|read|`<SSB>:1-200:raw`|allowed|NORM|
|9|read|`<SSB>:200-400:raw`|allowed|NORM|
|10|read|`<SSB>:60-100`|allowed|NORM|
|11|read|`<SSB>:140-200`|allowed|NORM|
|12|read|`<SSB>:100-140`|allowed|NORM|
|13|grep|`<SSB>`|allowed|—|
|14|grep|`<SSB>`|allowed|—|
|15|write|`<OWN>`|allowed|—|

Rough: 0 units.

### 5.8 FxC2Shape (16 events) — agent `TsukuroiR22.FxC2Shape-2`
| idx | tool | raw suffix | rough class | tags |
|---|---|---|---|---|
|0|read|`skill://godspeed`|allowed|URI|
|1|read|`<SSB>`|allowed|—|
|2|grep|`<PRE>`|allowed|—|
|3|read|`<SSB>:1-120`|allowed|NORM|
|4|read|`<SSB>:121-240`|allowed|NORM|
|5|read|`<SSB>:241-360`|allowed|NORM|
|6|grep|`<PRE>`|allowed|—|
|7|read|`<REV>`|allowed|—|
|8|read|`<PRE>:1-60`|allowed|NORM|
|9|grep|`<PRE>`|allowed|—|
|10|read|`<SBM>`|allowed|—|
|11|read|`<HTB>`|allowed|—|
|12|read|`<SBJ>`|allowed|—|
|13|read|`<CRS>:1-90`|allowed|NORM|
|14|grep|`<SSB>`|allowed|—|
|15|write|`<OWN>`|allowed|—|

Rough: 0 units.

## 6. Candidate divergence set (the deliverable)

A candidate is an event whose rough classification changes if the authority differs on exactly one of A1–A5. Listed with seat, event index, `call_id`, raw path suffix, and bounded reason. **Direction** is stated as "rough↑" (rough records a unit that a stricter/differently-scoped authority may not) or "lane↑" (rough records none where a differently-normalizing authority may).

### 6.1 High-signal candidates — the only 4 events in this pack where rough records a unit

These are the only events in this group that can contribute to a rough-over-lane difference.

| # | Seat | idx | tool | call_id | raw path suffix | rough class | Direction | Bounded reason |
|---|---|---|---|---|---|---|---|---|
| D1 | `FxC2ReadWrite` | 18 | read | `call_00_wBa0QNy499W9OWlQpGP76609` | `falsify/FxC2ReadWrite.md:-12` | `path` | rough↑ | `strip_sel` removes `:-12` → `falsify/FxC2ReadWrite.md`, which is in `write_paths` but **not** in `read_paths`; rough's read family consults `read_paths` only (P3). Flips to allowed if the authority allows reading a path in `write_paths` (read-after-write) — a v1-policy question, not a normalization question: the `-12` form is stripped identically by any selector-stripping rule. |
| D2 | `FxC2ReadWrite` | 19 | grep | `call_01_zvNpWPGdDrQyyMcLQROG6307` | `falsify/FxC2ReadWrite.md` | `path` | rough↑ | Same authority-list question without any selector: `grep` → `read_paths` only; the single component is not in `read_paths`. One unit for this event (P1). |
| D3 | `FxC2Unknown` | 6 | read | `toolu_01XhhyTUnroyCin946g7BbTg` | `falsify/FxC2Unknown.md:raw` | `path` | rough↑ | `strip_sel` removes `:raw` → `falsify/FxC2Unknown.md` ∈ `write_paths`, ∉ `read_paths`. Same authority-list question as D1/D2. Shares its `call_id` with idx 5 and 7. |
| D4 | `FxC2Unknown` | 5 | edit | `toolu_01XhhyTUnroyCin946g7BbTg` | `falsify/FxC2Unknown.md` (args carry `__unknown_argument__`: null) | `unknown` | rough↑ | `edit` ∉ `('read','grep','glob','write')` → `unknown` unit and `continue`; **no path check is performed at all** (P2), even though the path equals the seat's declared `write_paths` entry. A v1 authority that scoped `edit` against `write_paths` would record no unit — but that would be *introducing* edit semantics into v1, which this round forbids (§6.3). |

### 6.2 Divergence-sensitive events that rough records as **allowed** (would move the other way)

These are not candidate sources of a rough-over-lane difference, but they are the events a "different normalization" story must not silently reclassify. They are listed so the C3 per-event explanation is exhaustive in both directions.

**A1 / selector-normalization sensitive — 35 events.** Each carries a trailing selector that `strip_sel` removes, yielding an exactly-declared `read_paths` entry. If an authority stripped differently (or not at all), each becomes a `path` violation. Distinct selector forms observed: `:1-100`, `:101-200`, `:201-330`, `:1-120`, `:121-240`, `:241-360`, `:22-120`, `:120-230`, `:1-21`, `:233-241`, `:1-240`, `:1-220`, `:1-200`, `:60-100`, `:140-200`, `:100-140`, `:1-60`, `:1-90`, `:1-200:raw`, `:200-400:raw`, `:20-62:raw`, `:62-112:raw`, `:86-125:raw`, `:126-165:raw`, `:166-241:raw`, `:1-32:raw`, `:-12`, `:raw` (28 distinct forms). Two shape families are worth naming explicitly because a naive stripper gets them wrong: the **double-suffix** `:N-M:raw` / `:N:raw` forms (7 events: `FxC2Report` 8, 9; `FxC2ReadWrite` 10, 11, 12, 16; `FxC2ParallelLocal` 8, 9) and the **negative-only** `:-12` form (`FxC2ReadWrite` 18). Per-seat counts: Wildcard 3 (8, 9, 10); Report 4 (4, 5, 8, 9); ReadWrite 7 (2, 3, 10, 11, 12, 16, 18); Unknown 1 (6); ParallelExec 4 (3, 4, 6, 7); ParallelFetch 6 (1–6); ParallelLocal 5 (8–12); Shape 5 (3, 4, 5, 8, 13).

**A2 / URI-literal matching sensitive — 7 events** (one per seat: `FxC2Wildcard` 0, `FxC2Report` 0, `FxC2ReadWrite` 1, `FxC2Unknown` — none, `FxC2ParallelExec` 0, `FxC2ParallelFetch` 0, `FxC2ParallelLocal` 3, `FxC2Shape` 0). Raw suffix `skill://godspeed`. Rough allows them only because the binding declares the identical URI string and the comparison is literal (P5). Any resolver-based check that maps `skill://` to a file path would classify all 7 as violations. `FxC2Unknown` is the only seat in this pack with no `skill://` read.

**A2 / write-family ordering sensitive — 8 events** (one write per seat: Wildcard 11, Report 15, ReadWrite 17, Unknown 7, ParallelExec 11, ParallelFetch 7, ParallelLocal 15, Shape 15). Raw suffix `falsify/<own seat>.md`. Rough checks these against `write_paths` only; each is an exact declared entry, so all 8 are allowed. Order sensitivity here is one-sided: no `write` event in this pack targets a path that is only in `read_paths`, so a "write checked against the union" rule would not change any of them.

**A5 / event-vs-call identity sensitive — 3 events** (`FxC2Unknown` 5, 6, 7, all `call_id` `toolu_01XhhyTUnroyCin946g7BbTg`; idx 6 and 7 are `origin: additional-recorded-start`). Rough counts recorded entries, so the one call yields up to three counted events (here: 1 `unknown` + 1 `path` + 1 allowed write). A lane that keys on `call_id` would fold these three into one unit, changing this group's falsify-side unit count by up to 2 without changing any path judgement. `FxC2ParallelFetch`'s 8 compound `call_<id>|fc_<id>` ids are each distinct, so no folding applies there.

### 6.3 The edit-authority boundary (explicitly not crossed)

- `FxC2Unknown` idx 5 is an `edit` whose recorded args carry `__unknown_argument__: null` — the **structured edit target is absent**, not merely unlisted. Under the round-23 decision table this is the `OPAQUE_PATCH → UNKNOWN` shape: *"Missing structured target is not inferred from opaque patch text."*
- Old v1 has **no edit-target rule at all** (v1 authority is `read_paths` / `write_paths` over path strings). Therefore the honest v1-era classification of idx 5 is exactly what rough produced: *tool outside the path-checked family* — not "path violation" (no v1 path rule applies to `edit`), and not "allowed" (no v1 grant).
- The r23 C2 schema-v2 edit-target authority is **new** authority for new events. Importing it backwards to legitimise this 2026-r22 event would be a retrospective authorization, which the preregister forbids (*"No historical manifest/report rewrite or retrospective authorization"*) and which this seat's brief forbids (*"do not … import new edit permissions into old v1"*). No v2 permission was imported in this analysis; the r23 C2 mechanism is cited only to characterise the *shape* of the recorded event.

## 7. Arithmetic, and why "six unique events" is not the answer

Declared difference units: build 25−23 = 2, falsify 33−29 = 4, total **6 units**. That is a difference between two *counters*, not a count of distinct historical events, and the two counters are not even guaranteed to share a unit definition (the rough counter mixes `exec`, `unknown` and `path`; the lane counter's unit is unverified — see gaps below). Consequences:

- **Do not read 6 as 6 unique events.** In this group's slice the falsify-side rough units are **4 recorded events but only 3 unique `call_id`s** (`FxC2ReadWrite` 18 and 19 are distinct calls; `FxC2Unknown` 5 and 6 share `toolu_01XhhyTUnroyCin946g7BbTg`). One call already contributes 2 units, so unit-count and event-count and call-count are three different numbers.
- **Do not assume this group's 4 falsify-side units are the wave's 4.** The declared falsify difference (4) is a wave-level number over the whole r22 falsify cohort; this seat's scope is one group of 8 seats out of that cohort (the other groups' packs and the r22 `events.json` are outside this seat's declared read paths). That the local slice also yields 4 units is a **coincidence of magnitude, not an identity claim** — it may equally be that other groups contribute units and this group's units are partly matched by the lane.
- **Do not net the two waves.** build's 2 and falsify's 4 may come from different mechanisms; a single explanation covering both is not established here.
- **Do not relabel.** D1–D4 are recorded as *rough-side units under the rough algorithm*. This report does not convert them into "not violations", does not convert `path` into `unknown`, and does not close or reopen any r22 finding. C3's requirement is an explanation of the difference, not a change of history.

## 8. Findings, by severity

**F1 (high) — The falsify-side difference must be decomposed per event *and* per unit type, not per event.** The rough counter's 4 falsify-side units in this group are not 4 comparable units: 3 are `path` units (D1–D3) and 1 is an `unknown` unit from an unscoped `edit` (D4). Any reconciliation that sums them as one homogeneous "path violation" quantity will mis-state the r22 history. Evidence: §5.3, §5.4, §6.1.

**F2 (high) — The `edit` unit (D4) is not a path violation and must not be relabelled as one.** `edit` is outside the rough whitelist, so its path is never compared to any authority; the recorded args also lack a structured target. Classifying it as a path violation would fabricate a v1 path rule; classifying it as allowed would import v2 edit permission into v1. Evidence: rough source lines `if t not in ('read','grep','glob','write'): f['unknown']+=1; … continue`; preregister `edit_decisions` `OPAQUE_PATCH → UNKNOWN`; preregister `limits` ("No historical manifest/report rewrite or retrospective authorization").

**F3 (medium) — Read-after-write is the single authority-list choice that can explain D1–D3, and it is a v1-policy question.** All three path units are the same shape: the seat reads/greps its own report, which is in `write_paths` but not `read_paths`. If the lane's v1 rule reads `write_paths` as also readable, all three vanish; if not, all three stand and the difference must come from elsewhere (A1/A5). This single question is the highest-leverage unknown in this group. Evidence: §6.1 D1–D3; §5.3 idx 18/19; §5.4 idx 6.

**F4 (medium) — The `:-12` selector form and the `:N-M:raw` double-suffix form are the normalization-sensitive shapes.** `:-12` is the only negative-only selector in the group; `:N-M:raw` occurs 8 times (Report 8, 9; ReadWrite 10, 11, 12, 16; ParallelLocal 8, 9). A naive stripper that handles `:N-M` but not the optional `(:raw)` tail, or that requires a leading digit, will mis-handle exactly these 9 events. They are all currently *allowed* under rough, so the risk is an over-count by a differently-normalizing authority, not an under-count. Evidence: §6.2 A1 list; rough source `strip_sel` regex.

**F5 (medium) — Unit granularity vs call granularity is undecided in this cohort.** `FxC2Unknown` yields 2 units from a single `call_id`; a call-keyed lane yields 1. A reconciliation that counts events where the lane counts calls would silently shift by 1–2 in this group alone. Evidence: §6.2 A5; §5.4 idx 5–7.

**F6 (low) — Seat names must not be used as classifier evidence.** `FxC2ParallelExec` records no `bash`/exec event and `FxC2ParallelFetch` records no fetch-shaped tool; both contribute 0 `exec` units. Only recorded tool names may drive classification. Evidence: §4, §5.5, §5.6.

**F7 (low) — Literal URI matching is load-bearing for 7 events.** `skill://godspeed` is allowed in all 8 seats only because the binding declares the identical URI string; no resolution occurs. Evidence: rough source literal `in` membership; §6.2 A2.

**F8 (low) — The pack's binding copy is not proven 1:1 with the r22 `bindings.json` the rough source reads.** The rough source looks up `bd[x['name']]` and would abort on a missing seat; the pack is a "path oracle pack" copy. If the pack's `read_paths`/`write_paths` were re-serialized (e.g. reordered, or with a path dropped), every membership verdict in §5 could shift. This is unverified here for lack of read scope.

## 9. Residual risk and verification gaps

1. **The lane checker's source is unreadable under this seat's binding** (`round-22/candidate/tools/check-seat-bindings.py` is not in this seat's `read_paths`). Therefore "the lane counts X" is **inference**, not observation, everywhere in this report. The lane's unit definition (event vs call vs component), its selector stripping, its read/write list selection, and its tool family are all unverified. Any final C3 reconciliation must cite the lane's actual rule text; this report can only bound the candidate set.
2. **No counter was run.** Nothing was executed — no `check-seat-bindings.py`, no `check-path-reconciliation.py`, no census, no hash, no `wc`. All counts in §4 are hand-derived from the pack text and are re-checkable by reading; they are not independently confirmed by execution, and the preregister explicitly forbids rerunning closure "merely to confirm them".
3. **Pack ↔ r22 `events.json` identity is unverified** (gap F8): the pack is preserved request metadata with `request_line`/`start_line`/`origin` fields; whether its per-seat event lists are exactly the r22 recorded entries the rough source iterates is not provable from this scope. If r22 recorded fewer/more entries per seat, this group's raw counts change.
4. **Cohort completeness is unknown**: the falsify cohort spans packs outside this seat's scope, so the wave-level 4-unit difference cannot be allocated from this slice alone. The 4 local units are a *candidate* set, not a proven partition.
5. **Build-wave side (2 units) is entirely out of scope** here; nothing in this report speaks to it.
6. **Digest unverified**: `9e31fc0b…fb19` is supplied. No hashing, listing, or import was performed to confirm it, and none may be inferred from this report.
7. **No runtime claim**: nothing here asserts runtime enforcement, effect semantics, or per-seat tool restriction; the round-23 limits ("No native per-seat restrictive tool interface exists") remain in force.

## 10. Bottom line

Within falsify group 4 (8 seats, 108 recorded events), the rough algorithm yields **4 units over 3 unique calls over 2 seats**: 3 `path` units, all of the identical "seat reads its own report, which is only in `write_paths`" shape (`FxC2ReadWrite` idx 18, 19; `FxC2Unknown` idx 6), plus 1 `unknown` unit from an unscoped `edit` with no structured target (`FxC2Unknown` idx 5). These 4 events are the only candidates in this group that can move a rough-over-lane difference, and their divergence mechanism is *authority-list selection* (read-after-write) and *tool-scope coverage* (edit), not selector normalization: all 35 selector-bearing events in this group are classified allowed and are normalization-sensitive in the opposite direction. Whether they are the wave's four falsify-side units cannot be established from this seat's scope, and the declared "six" must not be read as six unique events — in this group alone, 4 units already correspond to 3 unique calls.

Reviewed-SHA256: 9e31fc0b1615a8b70d177a777d1e29f59f064d1b06130e9fe0bfac482701fb19
Predicate: r23-reconfalsify04
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
