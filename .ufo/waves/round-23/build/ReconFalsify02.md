# ReconFalsify02 — r23 falsify group 2 path-oracle re-falsification

Seat: `TsukuroiR23-2.ReconFalsify02-7` (leaf; no subagent dispatch).
Pack reviewed: `.ufo/waves/round-23/packs/falsify-02.json` (declared SHA256 supplied by assignment, **not** independently computed — no hash/list/wc/run performed).
Frozen rough source consulted: `.ufo/waves/round-23/sources/r22-rough-census.txt` (interpreted as source data only, never executed).
Round-23 context: `.ufo/waves/round-23/preregister.json` (C1/C2/C3 claims, `outside_round22.path_counts_as_reported`).

## 0. Scope and method (bounded)

- No gate, counter, checker, or classifier was executed. `commands` and `fetches` for this seat are empty, so **NO-EXEC / NO-FETCH** was observed: no bash/eval/subprocess/import/compile/test/lint/format/hash/wc/mkdir, no delegation, no web/network, no filesystem search outside the six declared read paths.
- Every expectation below is **hand-derived** by reading the pack's preserved request metadata and the frozen rough source cell, then applying the rough algorithm's own control flow by hand to each event.
- Only these files were read: the pack, the r23 preregister, the frozen rough-census source, the godspeed directive copy, `skill://godspeed`, and this report's own path.
- The r22 **lane** tool (`check-seat-bindings.py` / `check-boundary-contract.py`) and the r22 `events.json` / `bindings.json` are **outside this seat's declared read scope**. Consequently the lane's own per-event classification is *not* observable here; this report enumerates **candidate divergence sites** where the rough algorithm's normalization/order/break behaviour can diverge from a literal application of the declared old-v1 path authority, not a resolved lane comparison. Resolving any candidate requires lane-tool evidence that this seat may not open.

## 1. Axes

1. **Fidelity** — does the hand-derived rough application of the pack's 142 events reproduce the frozen rough source's semantics exactly (tool dispatch, selector stripping, `;` splitting, membership basis, one-per-event break)?
2. **Divergence surface** — for every event, is the rough outcome normalization-invariant, normalization-dependent, order-dependent, or bucket-dependent? Only these classes can produce rough-vs-lane count differences.
3. **Arithmetic honesty** — can this pack's findings be mapped onto the outside totals (rough 25 build / 33 falsify vs lane 23 / 29) without inventing unique events or importing v2 edit authority into old v1?

## 2. Exact reconstructed rough algorithm (from the frozen source cell)

Source cell semantics, in the order the cell applies them:

1. `strip_sel(p) = re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)` — strips a **trailing** selector only.
2. Per event: `t = e['tool']`, `a = e.get('args') or {}`.
3. `t == 'bash'` → `exec += 1`, seat added, `continue`.
4. `t not in ('read','grep','glob','write')` → `unknown += 1`, seat added, `continue`. **The path is never consulted for such events.**
5. Otherwise `vals = str(a.get('path','')).split(';')` for `grep`/`glob`; for `read`/`write` `vals = [str(a.get('path',''))]` (single component, **no** `;` split).
6. `q = strip_sel(v)` for `read`/`grep` **only**; `q = v` verbatim for `write`/`glob`.
7. Membership basis: `write` → `b['write_paths']`; `read`/`grep`/`glob` → `b['read_paths']`. Exact string equality, no prefix, no directory, no dot-segment handling.
8. First non-member component → `path += 1`, seat added, **`break`** (at most one `path` per event, and only the *first* failing component in string order is ever considered).
9. Reported wave number = `sum(f.values())` — the **sum over all three buckets** `exec + unknown + path`.

Two structural facts follow and are load-bearing below:

- **Selector stripping is tool-scoped**: applied to `read`/`grep`, *not* to `write`/`glob`.
- **The `;` split is tool-scoped**: applied to `grep`/`glob`, *not* to `read`/`write`.

## 3. Per-seat hand-derived rough expectation (142 events)

| seat | agent | events | read | grep | write | edit | rough `path` | rough `unknown` | rough `exec` | rough total | seats flagged |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FxC1Table | TsukuroiR22.FxC1Table-2 | 15 | 14 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| FxC1Sources | TsukuroiR22.FxC1Sources-2 | 15 | 11 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| FxC1HostLimit | TsukuroiR22.FxC1HostLimit-2 | 22 | 15 | 6 | 1 | 0 | **2** | 0 | 0 | **2** | 1 |
| FxC1ReadFailure | TsukuroiR22.FxC1ReadFailure-2 | 26 | 15 | 9 | 1 | 1 | **2** | **1** | 0 | **3** | 1 |
| FxC2Bash | TsukuroiR22.FxC2Bash-2 | 24 | 22 | 0 | 1 | 1 | **2** | **1** | 0 | **3** | 1 |
| FxC2Eval | TsukuroiR22.FxC2Eval-2 | 9 | 6 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| FxC2Child | TsukuroiR22.FxC2Child-2 | 16 | 12 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| FxC2Http | TsukuroiR22.FxC2Http-2 | 15 | 12 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| **group total** | — | **142** | 107 | 24 | 9 | 2 | **6** | **2** | **0** | **8** | **3 seats** |

No `bash` and no `glob` event occurs anywhere in this pack; every `exec`/`unknown` finding here comes from the `edit` tool, which the rough algorithm routes to `unknown` **without reading the path**.

Every one of the 142 events was matched against its seat's declared `read_paths`/`write_paths`; 134 events are declared-path reads/greps/writes and are clean. All 9 `write` events target the seat's own single declared `write_paths` entry with no selector → clean and normalization-invariant.

## 4. Candidate divergence sites

Field convention: *event index* is the 0-based position inside that seat's `events` array in the pack; *raw path suffix* is the verbatim trailing selector/absence as recorded (no rewriting).

### 4.1 Class N — selector-normalization-sensitive (`path` findings)

Rough strips the trailing selector, landing on the seat's own draft base path, which is declared in `write_paths` but **not** in `read_paths`; rough then fails it against `read_paths` and counts it as `path`. A lane implementation that normalizes the same suffix but resolves membership against a different basis (e.g. read-authority vs write-authority, or a distinct "read of a write-only target" category) can land on the same event with a **different category or a different count**.

| seat | event idx | call_id | tool | raw path suffix | rough outcome | bounded reason |
|---|---|---|---|---|---|---|
| FxC1HostLimit | 21 | `call_01_2yynczmqgdfvw1xgq0fvhlqe` | read | `:1-12` | `path` +1 | suffix strips to `…/round-22/falsify/FxC1HostLimit.md`; that base path is in `write_paths` only, so it fails the `read_paths` membership test the rough algorithm applies to `read` |
| FxC2Bash | 21 | `toolu_01MsCzhA8H5kDJ6a3Sd4kcBu` | read | `:74-80` | `path` +1 | same shape: strips to `…/round-22/falsify/FxC2Bash.md`, declared `write_paths` only, absent from `read_paths` |
| FxC2Bash | 23 | `toolu_014W2fHm4vLzYRxGb17mDz2U` | read | `:88-98:raw` | `path` +1 | two-part selector; rough's `(:raw)?$` tail plus greedy `\d[\d\-+,:]*` consumes `:88-98:raw` wholly, leaving the base draft path, absent from `read_paths` |

### 4.2 Class N′ — normalization-invariant (`path` findings)

These three carry **no** selector: the raw path string is byte-identical to the seat's own draft path. They are counted by rough regardless of how any classifier normalizes; the only open question is which category/bucket they land in.

| seat | event idx | call_id | tool | raw path suffix | rough outcome | bounded reason |
|---|---|---|---|---|---|---|
| FxC1HostLimit | 20 | `call_00_13jy2kj4bcch83a6v2segiuu` | grep | *(none — bare draft path)* | `path` +1 | `…/round-22/falsify/FxC1HostLimit.md` is in `write_paths` only; `grep` is tested against `read_paths` → non-member |
| FxC1ReadFailure | 23 | `call_00_vcUOc2oOA53F107WJh392123` | grep | *(none — bare draft path)* | `path` +1 | `…/round-22/falsify/FxC1ReadFailure.md` in `write_paths` only → non-member of `read_paths` |
| FxC1ReadFailure | 25 | `call_00_AerZ5CRSr0cL4zsTGTP06071` | grep | *(none — bare draft path)* | `path` +1 | same event shape as idx 23, re-emitted after the intervening `edit`; again a `write_paths`-only target read by `grep` |

Note: all six `path` findings in this pack are the *same* shape — a seat reading back the very file it is authorised to write. Under old v1 that is a **write-only target exercised by a read**, not an access to a path outside the seat's declaration. This is the single most likely rough-vs-lane category mismatch in the group, and it is a v1 category question, **not** a question of widening any seat's authority.

### 4.3 Class O — order / one-per-event break sites (latent, zero count effect here)

Rough's `break` means a `;`-joined `grep` contributes **at most one** `path` unit no matter how many components fail, and only the first failing component in string order is ever examined. Both multi-component greps in this pack are **fully declared**, so the divergence is latent, not observable in the count:

| seat | event idx | call_id | tool | raw path suffix | rough outcome | bounded reason |
|---|---|---|---|---|---|---|
| FxC1HostLimit | 10 | `call_00_6an1ja4ufmxmuurmziud2wyy` | grep | *(none — 5 `;`-joined components)* | 0 | all five components (`check-boundary-contract.py`, `seat-boundary-r22.json`, `seat-boundary-r22.md`, `host-tool-boundary.json`, `preregister.json`) are declared in `read_paths`; under any component-wise or per-event rule the outcome is the same, so this event cannot explain a rough-vs-lane difference |
| FxC2Http | 12 | `toolu_01BpgP8DHHRMMMHUGF38Fnyt` | grep | *(none — 7 `;`-joined components)* | 0 | all seven components (the five tools, both corpus files, `preregister.json`, `host-tool-boundary.json`) are declared in `read_paths`; likewise not a divergence source |

Two further order facts, both unexercised here and therefore **not** counted as findings: (a) the `;` split does not apply to `read`/`write`, so a `;`-bearing read path would be compared as one literal string and would falsely fail membership — no read or write path in this pack contains `;`; (b) `strip_sel` is not applied to `write`/`glob`, so a selector-bearing write path would falsely fail — no write path in this pack carries a selector.

### 4.4 Class B — bucket/tool-dispatch sites (`edit`)

Rough routes `edit` to `unknown` and never consults `path`. Both `edit` events in this pack are therefore classified without reference to any path authority.

| seat | event idx | call_id | tool | raw path suffix | rough outcome | bounded reason |
|---|---|---|---|---|---|---|
| FxC1ReadFailure | 24 | `call_00_SwIeaJDd3RNwdCH6xyht3569` | edit | *(none — path present: `…/round-22/falsify/FxC1ReadFailure.md`)* | `unknown` +1 | `edit` is outside the rough algorithm's handled set, so the path is ignored. The recorded args additionally carry `__unknown_argument__` in place of the structured edit keys, so the preserved request does not establish a resolvable structured target. The path itself *is* the seat's declared `write_paths` entry, so a lane that resolves `edit` as a write against v1 write-authority would classify this event differently (authorized write vs unknown vs read-of-write-only violation). Under old v1 the seat has **no read authority** on that target, so any lane outcome that treats it as an ordinary read-authorized write would be importing a permission v1 does not grant — this must not be assumed here. |
| FxC2Bash | 22 | `toolu_01MNphx6oshJdCfbNKYFYQor` | edit | *(no `path` key at all in args)* | `unknown` +1 | the preserved args contain only `i` and `__unknown_argument__`; no target path is recoverable from the record, so no path authority can be applied. Any lane outcome must be `unknown`/unresolved too unless it infers a target from surrounding session state — an inference absent from the preserved record and not permitted as old-v1 authority. |

### 4.5 Non-findings worth recording (to bound the search)

- 134 of 142 events are declared-path operations and are clean under every variant examined (exact-match, selector-stripping, component-wise).
- All 9 `write` events hit the seat's own declared `write_paths` entry with no selector → clean and invariant (FxC2Http has two writes to the same target, both counted clean).
- No `bash`/`glob` event exists in this pack, so rough's `exec` bucket and its non-stripped `glob` handling cannot contribute here.
- No path in this pack contains a dot-segment, a trailing slash, a `..` prefix, or a URI scheme other than the declared `skill://godspeed` literal; `skill://godspeed` is present in every seat's `read_paths` and is read once per seat (FxC1Table idx 0, FxC1Sources idx 0, FxC1HostLimit idx 0, FxC1ReadFailure idx 3, FxC2Bash idx 0, FxC2Eval idx 0, FxC2Child idx 0, FxC2Http idx 1) — clean.

## 5. Arithmetic honesty against the outside totals

Declared outside observation (r23 preregister, `outside_round22.path_counts_as_reported`): rough = build 25 / falsify 33; lane = build 23 / falsify 29. Gaps: build **2**, falsify **4**, combined **6**.

What this pack can and cannot say:

- This pack is **falsify group 2 only** (8 seats, 142 events). It contributes rough `path` 6, rough `unknown` 2, rough `exec` 0 to the falsify wave's 33. The falsify wave's other groups are outside this seat's declared read scope, so **the falsify gap of 4 cannot be attributed from this pack**, in either direction.
- **The six `path` findings above are not six unique gap events.** They are six events of a single repeated shape (read-back of a write-only draft target) across three seats; the falsify gap is 4 and the combined gap is 6, and the arithmetic does not line up. Specifically: of the six, three are normalization-dependent (class N) and three are normalization-invariant (class N′); a lane that disagrees on the category will disagree on all six, or on none — not on a tidy 4. Therefore **no subset of size 4 or 6 of these six events may be nominated as "the" gap** without lane-side per-event evidence.
- **Basis mismatch is a live candidate and must be checked before any per-event reconciliation.** The rough source prints `sum(f.values())` — a sum over `exec + unknown + path` — whereas the lane figures are recorded under the key `path_counts_as_reported`. If the lane figure is a *path-only* count, the two numbers are not on the same basis and part of the gap can be bucket composition rather than per-event disagreement. This pack's own composition bears on that: `exec` 0, `unknown` 2 (both `edit`), `path` 6. [INFERENCE — premise not verifiable from this seat's scope] If the lane number is path-only and the falsify wave's non-path rough units total exactly the falsify gap (4), the gap could be fully accounted for by bucket composition with **zero** per-event path disagreement in this group; the two `edit` units here would be part of that composition. Establishing this requires the lane tool's own counting basis, which this seat may not open.
- **No new edit permission is imported into old v1.** The two `edit` events are reported as bucket/category divergence candidates with their recorded targets exactly as preserved — one with a path that is the seat's own declared write target, one with no path at all. Neither is treated as authorized, and neither is re-derived.

## 6. Residual risk and verification gaps

1. **Lane-side evidence is missing.** The r22 lane classifier is outside the declared read scope of this seat. Every item in §4 is a *candidate* site, not a confirmed divergence. Only the C3 reconciler (with lane access) can promote a candidate to a confirmed per-event divergence.
2. **Wave coverage is partial.** Only falsify group 2 was readable. The build gap (2) and the falsify gap (4) both require groups not in this pack.
3. **Category basis unknown.** Whether the lane figure is path-only or an all-bucket total is not determinable here; §5's basis-mismatch hypothesis stays an inference.
4. **Recorded-args fidelity.** Both `edit` events carry `__unknown_argument__` in place of structured keys, and one carries no `path`. Any lane re-derivation from the same preserved record must face the same opacity; conclusions that depend on the original structured edit target are out of reach for both sides.
5. **Selector coverage is complete but narrow.** This pack exercises only trailing numeric selectors, `…:raw` tails, and one `…:N-M:raw` composite. Selector forms not present here (e.g. `:-5`, `:N-`, bare `:raw`) remain unverified for rough-vs-lane agreement; none occur in this group.

## 7. Conclusion

Hand-derived application of the exact frozen rough algorithm to all 142 events of the eight named seats yields rough `path` 6, rough `unknown` 2, rough `exec` 0 (total 8) across three seats (FxC1HostLimit, FxC1ReadFailure, FxC2Bash). Every one of the six `path` findings is a read or grep of the seat's own write-only draft target; three are selector-normalization-sensitive and three are normalization-invariant. The two `unknown` findings are `edit` events that the rough algorithm never tests against any path authority, one with a preserved target equal to the seat's declared write path and one with no target at all. The two multi-component greps are fully declared and are latent order/break sites only. The six findings are explicitly **not** nominated as the four- or six-unit gap between the outside rough and lane totals; the falsify gap remains unreconciled from this pack, and the rough-vs-lane counting-basis question is flagged for the C3 owner rather than answered here.

Reviewed-SHA256: 98bf9cbd1ff5186879fe7d2a5f3c3c372b60ed485c7fcebf3b4bb5a5d4eda35d
Predicate: r23-reconfalsify02
Scope: executed=none
