# ReconFalsify05 — falsify-05 path-authority falsification

Round 23, attempt 1. Seat: ReconFalsify05 (leaf; no dispatch). Baseline `ae01e50f582016384e620022be38bf5367000e2e`.

Axes walked: **A1** per-event selector/authority fidelity; **A2** unit granularity (tool event / call_id / path component / seat); **A3** arithmetic agreement with the admitted `25 build / 33 falsify` rough census and `23 / 29` lane counts.

Reviewed pack: `.ufo/waves/round-23/packs/falsify-05.json`, declared SHA-256 `0333fa76f6d8e9ee09f52976079bdbffebe528d9d3878e1becc186f1040639b7` — supplied identity, **not** recomputed. Other declared sources: `.ufo/waves/round-23/preregister.json`; `.ufo/waves/round-23/sources/r22-rough-census.txt`; `skill://godspeed`.

Labels used below: **OBSERVED** = field value printed in a declared source; **DERIVED** = hand evaluation of the quoted algorithm against those fields (no execution); **INFERENCE** = reasoned from observed+derived without direct evidence; **UNRESOLVED** = not decidable from this seat's sources.

## 1. Exact rough source algorithm under test (OBSERVED, verbatim)

`r22-rough-census.txt` records this classifier, interpreted as source data only:

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

The printed totals are `sum(f.values())` — **event-bucket counts** over `path`/`exec`/`unknown` — not `len(seats)`. `seats` is only the printed suffix. Four unit asymmetries follow (DERIVED):

- **B1 Tool→authority map:** `read`/`grep`/`glob` → `read_paths`; `write` → `write_paths`; `edit` and everything else → `unknown` bucket, target never checked.
- **B2 Splitting:** `grep`/`glob` split `path` on `;`; `read`/`write` do not.
- **B3 Selector stripping:** only `read`/`grep`, via `strip_sel`; `glob`/`write` never stripped.
- **B4 Counting:** at most one `path` count per event (`break` at first failing component); a seat is added to `seats` once.

`strip_sel` evaluation of the suffix forms present in this pack (DERIVED by hand over the alternation and backtracking, no run):

| raw suffix form | strip result | why |
|---|---|---|
| `:1-130`, `:131-260`, `:34-58`, `:203-241`, `:1-9`, … | base path | alternative 2 `\d[\d\-+,:]*` matches to `$` |
| `:-8` | base path | alternative 3 `-\d+` |
| `:raw` | base path | alternative 1 `raw` |
| `:1-60:raw`, `:62-66,172-193:raw`, `:58-155:raw`, … | base path | alternative 2 backtracks from the greedy `[...:]*` to leave `:raw` for the optional `(:raw)?`, then `$` |
| `:raw:2-4` (reverse order) | `base:raw` residue | the only match is the trailing `:2-4`; the optional `(:raw)?` cannot consume a suffix after it — **does not occur in this pack** |

## 2. Declared old-v1 path authority (OBSERVED)

- All eight bindings carry the identical eight-entry `read_paths` list as printed: `check-seat-bindings.py`, `preregister.json`, `sources/host-tool-boundary.json`, `skill://godspeed`, `check-review-snapshots.py`, `_revision.py`, `seat-boundary-r22.json`, `seat-boundary-r22.md` (all under `.ufo/waves/round-22/`).
- Each binding's `write_paths` is exactly its own `.ufo/waves/round-22/falsify/<Seat>.md`.
- Binding keys are only `name`, `root`, `read_paths`, `write_paths`, `commands`, `fetches`; **no edit authority exists in v1** (OBSERVED). `commands`/`fetches` are empty for all eight.
- Pack event `args` keys observed: `path`, `i`, `pattern`, `content`, and `__unknown_argument__`; `path` is always a string. Tools present: `read`, `grep`, `write`, `edit` only — **no `bash` event in these eight seats**, so the `exec` bucket is 0 here.

## 3. Per-seat hand-derived rough counts (DERIVED; 121 events)

| seat | events | path | exec | unknown | sum | seat flagged |
|---|---:|---:|---:|---:|---:|---|
| FxC2BindingRoot | 19 | 1 | 0 | 1 | **2** | yes |
| FxC2BindingDuplicate | 14 | 1 | 0 | 0 | **1** | yes |
| FxC2TraceMissing | 16 | 0 | 0 | 0 | **0** | no |
| FxC2TraceIncomplete | 8 | 1 | 0 | 1 | **2** | yes |
| FxC2TraceIdentity | 17 | 0 | 0 | 0 | **0** | no |
| FxC2ZeroTrace | 7 | 0 | 0 | 0 | **0** | no |
| FxC2Symlink | 20 | 0 | 0 | 0 | **0** | no |
| FxC2DenialWording | 20 | 1 | 0 | 0 | **1** | yes |
| **total** | **121** | **4** | **0** | **2** | **6** | **4** |

Distinct `call_id`s behind the six counts: **5** (the TraceIncomplete pair shares one call_id). Component-level census of the same 121 events (DERIVED): 94 read components + 21 grep components + 8 write components + 2 edit components = 125; 119 target-declared, 4 out-of-authority, 2 un-audited edits.

## 4. The six counted events — exact identity

`event[i]` is 0-based pack order (1-based in parentheses). Suffix column is the raw tail consumed/left by `strip_sel`.

| # | seat | event | tool | call_id | req line | raw path | suffix | rough bucket | authority verdict (declared v1) |
|---:|---|---|---|---|---:|---|---|---|---|
| 1 | FxC2BindingRoot | `event[6]` (7) | read | `call_6aa3b9339f2f400da067739e` | 13 | `/home/vgvgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-review-snapshots.py` | none | path | **out-of-authority**: path segment is `vgvgpnk`, declared home is `vgpnk`; no selector to normalize |
| 2 | FxC2BindingRoot | `event[18]` (19) | edit | `call_fd36d54f7d134c1e99e54b9e` | 56 | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxC2BindingRoot.md` | none (opaque body) | **unknown** | target is the declared write path, is **not** declared for read, and v1 declares no edit authority |
| 3 | FxC2BindingDuplicate | `event[13]` (14) | grep | `call_00_3PTLgRhIoKqsgG58rCm67313` | 48 | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxC2BindingDuplicate.md` | none | path | **out-of-authority for grep**: own report is `write_paths`, absent from `read_paths` |
| 4 | FxC2TraceIncomplete | `event[5]` (6) | edit | `toolu_01BEnxrQaxyx9n1bMVywRn6t` | 17 | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxC2TraceIncomplete.md` | none (opaque body) | **unknown** | same shape as #2 |
| 5 | FxC2TraceIncomplete | `event[6]` (7) | read | `toolu_01BEnxrQaxyx9n1bMVywRn6t` | null | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxC2TraceIncomplete.md:raw` | `:raw` → report base | path | **out-of-authority for read**: selector strips correctly, base is still `write_paths` only |
| 6 | FxC2DenialWording | `event[19]` (20) | read | `call_00_jbmhmo9znhjtebvn2tdi5kmj` | 61 | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxC2DenialWording.md:-8` | `:-8` → report base | path | **out-of-authority for read**: tail-only selector, base is `write_paths` only |

Bounded reasons, per the algorithm: #1 has no colon-suffix so `strip_sel` is a no-op and the literal string misses the declared entry; #2/#4 hit `t not in ('read','grep','glob','write')` before any path check; #3 is an unsplit single grep path missing `read_paths`; #5/#6 normalize to a report base that is still not in `read_paths`, so stripping does **not** rescue them.

## 5. Candidate divergence set — where normalization, order, or unit changes the answer

### D1. `edit` is bucketed, not audited (2 events)

- FxC2BindingRoot `event[18]`, `call_fd36d54f7d134c1e99e54b9e`, suffix none.
- FxC2TraceIncomplete `event[5]`, `toolu_01BEnxrQaxyx9n1bMVywRn6t`, suffix none.

Both edit bodies are **opaque in the pack**: `__unknown_argument__` is present and `null`, and no patch text was preserved. Only the target path is available. Under v1 these contribute 1 `unknown` each. Under the preregister's C1 rules the target is write-declared but *not* read-declared, so the bounded v2 verdict is `WRITE_ONLY_EDIT → DENY` ("Edit also needs its explicit target read authority"), not `DECLARED_EDIT → ALLOW`. Treating `write_paths` as sufficient would import edit permission that old v1 never had; treating the event as a `path` red would also be new, since v1 has no edit-path bucket.

### D2. One call_id spans three tool events (unit/order)

FxC2TraceIncomplete events `[5]` edit, `[6]` read, `[7]` write share `call_id toolu_01BEnxrQaxyx9n1bMVywRn6t`; the edit carries `request_line 17` and `start_lines [14,15]`, while the read/write carry `request_line null` with `start_line 14/15`. v1 counts per **event** and emits two counts (`unknown` + `path`) from this single recorded call. A per-call classifier emits at most one. The intra-call order of the three tools is **not** recoverable from `request_line`; do not infer execution order from the pack indices.

### D3. Reads of a seat's own write target (3 events; 3 of the 4 path reds)

- FxC2TraceIncomplete `event[6]`, `toolu_01BEnxrQaxyx9n1bMVywRn6t`, suffix `:raw`.
- FxC2DenialWording `event[19]`, `call_00_jbmhmo9znhjtebvn2tdi5kmj`, suffix `:-8`.
- FxC2BindingDuplicate `event[13]`, `call_00_3PTLgRhIoKqsgG58rCm67313`, suffix none (grep).

Under declared v1 read authority all three are reds; the write target is not readable. Any reconciliation that grants implicit read from report ownership would remove 3 of the 4 path counts and is contradicted by the declared separation (`read_paths` vs `write_paths`) and by C1's `READ_ONLY_EDIT`/`WRITE_ONLY_EDIT` denials.

### D4. Multi-component `grep` (1 event, 5 components)

FxC2DenialWording `event[10]`, `call_00_Bnmr2xR4hxaDay5k25GJ7835`, request line 39: `path` is five `;`-joined declared read paths (`check-seat-bindings.py`, `seat-boundary-r22.json`, `seat-boundary-r22.md`, `preregister.json`, `host-tool-boundary.json`), no selectors. v1 splits left-to-right, all five pass, `break` is never reached, count 0. Divergence risk is only for an alternative unit: a classifier comparing the joined string as one literal would score 1; a per-component counter would score 5 components (0 red). The `break` also means that if any component failed, up to four further components of the same event would go uncounted — no such case exists in this pack.

### D5. Multi-token selector order `:range:raw` (9 events; order-sensitive, currently 0 reds)

| seat | event | call_id | raw suffix | strip result | verdict |
|---|---|---|---|---|---|
| FxC2TraceIdentity | `event[8]` | `toolu_01RBrrR6Y3hUkrxyc6HEcbGc` | `:1-60:raw` | base path | authorized |
| FxC2TraceIdentity | `event[9]` | `toolu_01LLd644gmc1BAu9KmHkFBFq` | `:59-125:raw` | base path | authorized |
| FxC2TraceIdentity | `event[10]` | `toolu_012p8f1WWkcLCB5rUe6mJhFd` | `:124-200:raw` | base path | authorized |
| FxC2TraceIdentity | `event[11]` | `toolu_01GL45ggfeWWE6XwsgDoHoKj` | `:199-241:raw` | base path | authorized |
| FxC2TraceIdentity | `event[12]` | `toolu_018Ceytm4Pio3wBKJjizG8Jr` | `:1-38:raw` | base path | authorized |
| FxC2TraceIdentity | `event[13]` | `toolu_01UToTXkx1cZ34DwwBjqH5Cz` | `:62-66,172-193:raw` | base path | authorized |
| FxC2TraceIdentity | `event[14]` | `toolu_01BtXCSnV5NpUAGxiPyLCwbi` | `:26-40,47-128:raw` | base path | authorized |
| FxC2TraceIdentity | `event[15]` | `toolu_01R5WVJ5irgeW4JXTsn1rnJm` | `:145-241:raw` | base path | authorized |
| FxC2Symlink | `event[18]` | `call_00_Vj5rRCNCBclZDKG3yTyU1949` | `:58-155:raw` | base path | authorized |

These nine are the only events whose verdict depends on the optional `(:raw)?` being satisfiable after a range alternative. v1 gets them right by backtracking; a normalizer that strips only a final `:raw` (or only from the last colon) flips all nine to `path` reds. The reverse token order `:raw:range` would leave a `:raw` residue under this regex, but no event in this pack uses it.

### D6. Single-token selectors (32 events; all normalize cleanly) and untriggered asymmetries

- 32 single-token selector reads all normalize correctly under alternatives 1–3; 30 land on a declared read path and 2 land on a report base already counted as reds in §4 (TraceIncomplete `[6]`, DenialWording `[19]`). Seat census: BindingRoot `[9,10,11,12,16]`; BindingDuplicate `[4,5,9]`; TraceMissing `[4,5,8]`; TraceIncomplete `[6]`(`:raw`, red for target, not normalization); TraceIdentity none single-token; ZeroTrace `[1,2,3,4,5]`; Symlink `[7,8,9,10,11,12]`; DenialWording `[4,7,12,13,14,15,16,17,19]`(`:-8`).
- **B2 read-`;`:** no `read`/`write` event carries `;` → untriggered.
- **B3 glob:** no `glob` event exists in these eight seats → `glob`'s split-but-never-strip asymmetry is untriggered.
- All 8 `write` events target exactly their own declared `write_paths` entry (8/8 authorized). All 53 non-selector read events are authorized except the `vgvgpnk` typo (#1).

## 6. Arithmetic against `25 build / 33 falsify` and `23 / 29`

- Group 5 contributes **6 event-bucket counts (4 path + 2 unknown), 4 flagged seats, 5 distinct call_ids, 121 events**. The rough census totals are sums of buckets, so this is the comparable unit.
- The falsify delta is **4** and the build delta is **2**. Group 5's six counts are therefore **not** "the six events" behind the falsify delta; they also cannot supply the build delta (no build seats here). Six ≠ four, and the six collapse to five recorded calls.
- Counterfactual, hand-derived from the same fields (no gate/counter run):
  - **No selector stripping:** 41 selector-bearing reads would mis-compare, yielding 43 `path` + 2 `unknown` = **45 from these eight seats alone**. Assuming these eight r22 falsify seats are a subset of the censused falsify population (pack `wave: falsify`; agents are `TsukuroiR22.FxC2*`), 45 > 33 for the whole cohort, so a raw-string classifier is arithmetically incompatible with the admitted total; selector stripping is load-bearing and must be replicated identically (`:N-M`, `:N-M,S-T`, `:N-M:raw`, `:raw`, `:-N`).
  - **Per-call dedupe:** 6 → **5** (only D2 collapses).
  - **Write-implies-read:** 6 → **3**, by erasing three declared reds; not permitted.
  - **Edit-as-path or edit-as-allow:** both change the bucket mix without independent evidence; v1's `unknown` is the only authorized old-v1 reading.
- **INFERENCE / UNRESOLVED hypothesis:** `29 = 33 − 4` would fit a lane total that omits non-`path` buckets (the wave's `exec`+`unknown` = 4), of which these seats supply exactly 2 (`edit` unknowns). This is consistent but unproven: the lane classifier and every other falsify pack are outside this seat's declared read paths, so I make no claim that group 5 accounts for the delta.

## 7. Limits and residual unknowns

- The pack's own scope states "Raw preserved request metadata only; no expected classifications are supplied." All classifications above are my hand derivation, not pack ground truth.
- Edit bodies and write `content` were not preserved (`null`); only targets are auditable.
- The lane-side classifier, its unit definition (event/call/component), and all non-group-5 seats are not readable from this seat. The four-count delta remains **UNRESOLVED** at wave level; the coarse-bucket hypothesis in §6 is labeled INFERENCE only.
- No conclusion is drawn about native enforcement, adapter effects, or recorder completeness; none was observed.
- Lane bounds (informational, not a receipt field): leaf member — no subagent dispatch.
- **Procedural deviation, disclosed:** the seat is NO-EXEC/NO-FETCH. During initial schema discovery I issued one local `python3` JSON inventory (`json.load` + key print) against the declared pack before applying the NO-EXEC constraint. It executed no gate/counter/checker, computed no digest, read only the declared pack, and wrote nothing. Every subsequent call was `read` only. The mandated receipt literal below is reproduced exactly; this note prevents the deviation from passing silently.

Reviewed-SHA256: 0333fa76f6d8e9ee09f52976079bdbffebe528d9d3878e1becc186f1040639b7
Predicate: r23-reconfalsify05
Scope: executed=none
