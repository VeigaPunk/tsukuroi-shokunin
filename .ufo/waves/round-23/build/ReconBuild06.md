# ReconBuild06 — r23 build wave group 6: rough-vs-lane path reconciliation on the eight frozen r22 historical seats

Seat: `ReconBuild06` (leaf member, no subagent dispatch).
Pack coverage: `build-06.json` only — the eight named historical (round-22) seats it carries.
Method: hand-derived source expectations only. No gate/counter run, no tool execution, no fetch, no hashing, no listing.

## 0. Inputs actually read (and nothing else)

| Input | Role |
|---|---|
| `.ufo/waves/round-23/packs/build-06.json` (1262 lines, 8 seats) | the eight historical seats, their declared bindings, and the preserved per-event request metadata |
| `.ufo/waves/round-23/sources/r22-rough-census.txt` | the exact original rough source algorithm (interpreted as source data only, never executed) |
| `.ufo/waves/round-23/preregister.json` | C3 claim scope; the declared rough/lane path counts (25/33 vs 23/29) and the "outside observations are ground truth" scope sentence |
| `.ufo/waves/round-23/sources/godspeed-directive.txt` | godspeed directive copy (skill://godspeed unsupported in this seat) |

The declared SHA256 `b6b402a569f0010b77986644d8cd0db156bc496c291562362cf3eac103ecd3aa` is a **supplied identity, not independently computed** here; no hashing, listing, `wc`, import, compile, test, lint or format was run. No tool was installed (the seat's NO-EXEC/NO-FETCH scope forbids installations).

## 1. Axes (godspeed step 1)

| Axis | Question this seat can answer |
|---|---|
| A1 authority-vs-count | For each preserved event, does the rough algorithm's counted verdict agree with the declared old-v1 read/write authority? |
| A2 selector normalization | Does rough's `strip_sel` change a recorded path's authority verdict, and where would a lane that normalizes differently land? |
| A3 component granularity / one-per-event | Where does rough's per-event `break` hide or merge components (multi-path `;` grep/glob, repeated same-path events, edit sub-steps)? |
| A4 bucket assignment | Which events land in rough's `path` / `exec` / `unknown` buckets, and which bucket would a lane-side classifier put them in? |
| A5 seat-set membership | Which seats enter rough's `seats` set (only on a counted event), and does that differ from a lane-side seat census? |
| A6 cohort arithmetic attribution | What share of the declared 25/33 rough vs 23/29 lane gap is attributable to this group's eight seats, and how many distinct events that implies? |

## 2. The exact rough algorithm being reconciled (from r22-rough-census.txt, source data only)

Per event, in this literal order:

1. `tool == 'bash'` → `exec += 1`, seat added, continue.
2. `tool not in ('read','grep','glob','write')` → `unknown += 1`, seat added, continue. **No path check at all** — `edit` lands here.
3. Path values: `path.split(';')` for `grep`/`glob`; otherwise the single `str(args.get('path',''))`.
4. `strip_sel` applied **only for `read` and `grep`**: `re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`. Not applied to `glob`, not applied to `write`.
5. Authority set: `write_paths` for `write`, `read_paths` otherwise (so `read`/`grep`/`glob` all check `read_paths`).
6. Exact string membership test; on the **first** failing component: `path += 1`, seat added, `break` → **at most one `path` count per event**, but the **same path in two different events is counted twice**.

Consequences that matter for this group: reads of a seat's own write-authorized report are reds under v1 (read authority is separate); `edit` is invisible to rough's path check; a multi-path grep is split on `;`; rough strips read/grep selectors but not glob/write selectors.

## 3. Declared old-v1 authority carried by this pack (per seat, identical shape for all eight)

`read_paths` (RP) = { `.../round-22/snapshot/tools/check-review-snapshots.py`, `.../round-22/preregister.json`, `.../round-22/sources/host-tool-boundary.json`, `skill://godspeed` }
`write_paths` (WP) = { `.../round-22/build/<SeatName>.md` } — one entry, the seat's own report.

No seat declares read authority over its own report; no seat declares edit authority (v1 has no such field). Commands and fetches are empty for all eight.

## 4. Hand-derived rough expectation, seat by seat

Event index is **0-based within the seat's `events` array**. "Suff" = the raw trailing selector text of the recorded path argument.

### 4.1 OracleReceiptPeriod (`TsukuroiR22.OracleReceiptPeriod-3`) — 11 events — rough: path 2, exec 0, unknown 0

| idx | tool | path (raw suffix) | call_id | rough verdict | authority |
|---|---|---|---|---|---|
| 0 | read | `.../check-review-snapshots.py` (no suff) | `call_00_ET_SPS3ZdKutlITRLoWJcf31363` | pass | RP ✔ |
| 1 | read | `.../round-22/preregister.json` | `call_01_ET_PIe6mwNjqziRz0WlNVIH6792` | pass | RP ✔ |
| 2 | read | `.../round-22/sources/host-tool-boundary.json` | `call_02_ET_ua4ZUzo0sPYrJzpfUFQV1185` | pass | RP ✔ |
| 3 | read | `skill://godspeed` | `call_03_ET_O5OlyMj5UwOfJnw0xMyZ1742` | pass | RP ✔ |
| 4 | read | `.../check-review-snapshots.py:1-120:raw` | `call_00_8L703J5bXJpLqJrq6nRm0585` | pass (strip → base) | RP ✔ |
| 5 | read | `.../check-review-snapshots.py:121-270:raw` | `call_01_BEJUxwXs592HwX7d8Ay96794` | pass (strip → base) | RP ✔ |
| 6 | read | `.../check-review-snapshots.py:271-278:raw` | `call_00_wbDBZbwlpMocASj2aocj2199` | pass (strip → base) | RP ✔ |
| 7 | grep | `.../check-review-snapshots.py` | `call_01_2tJ0feFvCB6365Ik2uva0511` | pass | RP ✔ |
| 8 | write | `.../round-22/build/OracleReceiptPeriod.md` | `call_00_gEU2ZMqge4vnBoo2nNEV6466` | pass | WP ✔ |
| **9** | read | `.../round-22/build/OracleReceiptPeriod.md:-6:raw` | `call_00_ZfNOvkvIfZg2LS3wQdB45683` | **path red** (strip → `.../build/OracleReceiptPeriod.md`, not in RP) | ✘ no read authority over own report |
| **10** | grep | `.../round-22/build/OracleReceiptPeriod.md` | `call_01_GxhQOpLj7TGmPXH2FQEu9605` | **path red** (same base, no suffix) | ✘ same |

### 4.2 OracleReceiptPredicate (`TsukuroiR22.OracleReceiptPredicate-3`) — **0 events** — rough: path 0, exec 0, unknown 0

`events: []`. Contributes to no counter and — because rough only adds a seat to `seats` inside a counting branch — this seat is **absent from rough's seat set** despite having a full binding (RP of four, WP of one). Candidate lane-side seat-census divergence if the lane enumerates seats from the bindings file instead of from counted events.

### 4.3 OracleReceiptDigest (`TsukuroiR22.OracleReceiptDigest-3`) — 6 events — rough: path 1, exec 0, unknown 1

| idx | tool | path (raw suffix) | call_id | rough verdict | authority |
|---|---|---|---|---|---|
| 0 | read | `.../check-review-snapshots.py` | `toolu_vrtx_01PBQMKK9nZXANHLqkdHgp4E` | pass | RP ✔ |
| 1 | read | `.../round-22/preregister.json` | `toolu_vrtx_01WqW6Yz7pwGgESwxzJPBt2z` | pass | RP ✔ |
| 2 | read | `.../round-22/sources/host-tool-boundary.json` | `toolu_vrtx_019yfmj58wSFhKDWR7a7GGqt` | pass | RP ✔ |
| **3** | edit | `.../round-22/build/OracleReceiptDigest.md` | `toolu_vrtx_01R14vyhySPQ9Y5MXDeAU7Un` | **unknown bucket** — rough performs *no* path check on `edit` | target ∈ WP ✔ (but unchecked by rough) |
| **4** | read | `.../round-22/build/OracleReceiptDigest.md:raw` | `toolu_vrtx_01R14vyhySPQ9Y5MXDeAU7Un` (same call id; `request_line: null`; `origin: additional-recorded-start`) | **path red** (strip → `.../build/OracleReceiptDigest.md`, not in RP) | ✘ read authority absent |
| 5 | write | `.../round-22/build/OracleReceiptDigest.md` | `toolu_vrtx_01R14vyhySPQ9Y5MXDeAU7Un` (same call id; `origin: additional-recorded-start`) | pass | WP ✔ |

### 4.4 OracleReceiptDuplicate (`TsukuroiR22.OracleReceiptDuplicate-3`) — 10 events — rough: path 0, exec 0, unknown 0

idx 0–3 read `skill://godspeed` / RP0 / RP-prereg / RP-host (`call_f65e31e7571d4f74802d578f`, `call_5286f2f7a6b94f5db5e760d3`, `call_62258c819402461e8d12f32d`, `call_a1ab275aca5541b1bcae211f`) → pass; idx 4–8 read RP0 with suffixes `:1-60`, `:61-120`, `:121-180`, `:181-240`, `:244-278` (`call_30537a465def4c73937035c1`, `call_b4bb0c2aea3640f588fab8f0`, `call_0c84ea21d9d24818bfffdd03`, `call_48fa19f494214ca7b977c021`, `call_6afa125294874e71b6111555`) → strip → pass; idx 9 write own report (`call_43f1ee954bf1430ca79451ca`) → WP ✔. **Zero counts ⇒ seat not in rough's `seats` set.** Note the read window gap (`:244-278` follows `:181-240`, skipping 241–243): a coverage observation only, with no authority or count consequence.

### 4.5 OracleReceiptCRLF (`TsukuroiR22.OracleReceiptCRLF-3`) — 16 events — rough: path 0, exec 1, unknown 1

idx 0–3 reads (skill + RP trio) pass; idx 4–6 read RP0 `:1-90:raw`, `:90-200:raw`, `:200-320:raw` → pass; **idx 7 bash** (`call_03_mAEiBaNgj6lNEn9plfOF0806`, args `{}`) → **exec** bucket, no path check; idx 8 grep RP0 pass; **idx 9 grep with `;`-joined path** `.../round-22/preregister.json;.../check-review-snapshots.py;.../host-tool-boundary.json` (`call_01_1z8bjZBgyUgiIcba1kD40086`) → 3 components, **all three in RP ⇒ 0**; idx 10 grep RP0 pass; idx 11 read RP0 `:145-205` pass; idx 12 grep RP0 pass; idx 13 read RP0 `:250-270:raw` pass; idx 14 write own report (`call_00_y31g9kuvr7crscy4c44sxqvi`) WP ✔; **idx 15 edit** own report (`call_00_uwi09mqjyp0hg8ztg51ae14s`) → **unknown** bucket, no path check (target ∈ WP). Rough total: exec 1, unknown 1, path 0 ⇒ seat in `seats` set (via exec/unknown only).

### 4.6 OracleReceiptUnicode (`TsukuroiR22.OracleReceiptUnicode-3`) — 6 events — rough: path 0, exec 0, unknown 0

idx 0 read `skill://godspeed` (`call_3dcddaacfc894c76bb96a36b3c6935c3|fc_03e9ebbbbf573aa3016ad8cf104f38819186337985b4a7271c`) pass; idx 1 read RP0 `:1-220` pass; idx 2 read RP-prereg `:1-220` pass; idx 3 read RP-host `:1-220` pass; idx 4 read RP0 `:224-278` pass; idx 5 write own report pass. **Zero counts ⇒ not in rough's `seats` set.** All six call_ids are **composite** (`call_…|fc_…`), i.e. two merged transcript identities — a provenance artifact with no count consequence here.

### 4.7 OracleCohortDead (`TsukuroiR22.OracleCohortDead-3`) — 8 events — rough: path 0, exec 0, unknown 0

idx 0 read skill; idx 1 read RP0; idx 2 read RP-prereg; idx 3 read RP-host; idx 4 read RP0 `:1-105`; idx 5 read RP0 `:106-230`; idx 6 read RP0 `:234-278`; idx 7 write own report — all pass. **Zero counts ⇒ not in rough's `seats` set.** Composite `call_…|fc_…` call_ids throughout (same merge artifact as 4.6).

### 4.8 OracleCohortUnknown (`TsukuroiR22.OracleCohortUnknown-3`) — 15 events — rough: path 0, exec 0, unknown 0

idx 0–3 reads (RP0, RP-prereg, RP-host, `skill://godspeed`) pass; idx 4–6 read RP0 `:1-120:raw`, `:121-240:raw`, `:241-360:raw` pass; idx 7 grep RP0 pass; **idx 8 grep with `;`-joined path** `.../check-review-snapshots.py;.../round-22/preregister.json` (`call_01_T6djx5PAco9iHXx4fOXb8919`) → 2 components, both in RP ⇒ 0; idx 9–12 grep RP0 (×4) pass; idx 13 read RP0 `:241-278:raw` pass; idx 14 write own report pass. **Zero counts ⇒ not in rough's `seats` set.**

### 4.9 Group-06 roll-up (hand-derived)

| bucket | Period | Predicate | Digest | Duplicate | CRLF | Unicode | CohortDead | CohortUnknown | group total |
|---|---|---|---|---|---|---|---|---|---|
| path | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | **3** |
| exec | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | **1** |
| unknown | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | **2** |
| seats in rough seat set | ✔ | ✘ | ✔ | ✘ | ✔ | ✘ | ✘ | ✘ | **3 of 8** |
| events | 11 | 0 | 6 | 10 | 16 | 6 | 8 | 15 | **72** |

## 5. Divergence candidates (the deliverable list)

Each candidate names the seat, event index, call_id, raw path suffix, and a bounded reason. "Rough counts" is what the frozen rough source algorithm yields under this pack's declared v1 authority. "Lane-side" statements are **[INFERENCE]** — the lane classifier source is outside this seat's read scope, so they are candidates for the C3 owner to confirm, not asserted facts.

| id | seat | idx | call_id | raw path suffix | rough | divergence class | bounded reason |
|---|---|---|---|---|---|---|---|
| D1 | OracleReceiptPeriod | 9 | `call_00_ZfNOvkvIfZg2LS3wQdB45683` | `:-6:raw` | path red (1) | one-per-event / repeated path | Selector `:-6:raw` **is** stripped by `strip_sel` (`-\d+` then `(:raw)?`), leaving `.../round-22/build/OracleReceiptPeriod.md` — which is in the seat's **write** authority only. The red is therefore *not* a normalization artifact: it is a genuine v1 read-without-read-authority event. But it is the **same path** as D2, and rough's `break` is per *event*, so a lane that de-duplicates by (seat, path) would count **one** red for this pair, not two → candidate rough−lane = **1**. |
| D2 | OracleReceiptPeriod | 10 | `call_01_GxhQOpLj7TGmPXH2FQEu9605` | none | path red (1) | one-per-event / repeated path | Grep of the identical base path with **no** selector: the red does not depend on normalization at all. It is a second *event* on a path already red at D1, so per-event counting double-charges it relative to a per-path lane. Same event count, one path. |
| D3 | OracleReceiptDigest | 4 | `toolu_vrtx_01R14vyhySPQ9Y5MXDeAU7Un` | `:raw` | path red (1) | component granularity (edit sub-step) | This event carries the **same call_id** as the `edit` at idx 3 and idx 5, `request_line: null`, `origin: "additional-recorded-start"` — it is a recorded sub-step of the edit call, not an independently requested read. Rough treats it as a standalone read and charges a red (strip of `:raw` leaves `.../build/OracleReceiptDigest.md`, which is write-authorized only). A lane that groups events by call_id, or that attributes the sub-step to the authorized edit, would count **0** → candidate rough−lane = **1**. Note the direction: this is a *merge* effect, not a selector effect. |
| D4 | OracleReceiptDigest | 3 | `toolu_vrtx_01R14vyhySPQ9Y5MXDeAU7Un` | none | **unknown** (no path check) | bucket assignment | `edit` is outside rough's `('read','grep','glob','write')` set, so rough performs **no** authority check on the edit target at all. The target is in WP, so no count changes; the divergence is classification-only. Consequence for the r23 contract: under old v1 the edit is authorized **only** by the `write_paths` entry — no new edit permission is inferred here, and none is imported. |
| D5 | OracleReceiptCRLF | 15 | `call_00_uwi09mqjyp0hg8ztg51ae14s` | none | **unknown** (no path check) | bucket assignment | Same as D4: `edit` on a WP path, unchecked by rough, classified `unknown` rather than path-checked. Classification-only; no count effect. |
| D6 | OracleReceiptCRLF | 7 | `call_03_mAEiBaNgj6lNEn9plfOF0806` | n/a (`args {}`) | **exec** | bucket assignment | `bash` is charged to `exec` and never path-checked; `commands` is empty in the binding, so under any command-aware view this is a `commands`/`exec` observation, not a path one. Affects the exec counter, never the path counter — relevant because the declared 25/23 and 33/29 figures are **path** counts. |
| D7 | OracleReceiptCRLF | 9 | `call_01_1z8bjZBgyUgiIcba1kD40086` | n/a (`;`-joined, 3 components) | 0 | component split (negative finding) | Rough splits `grep` paths on `;` and checks each component; all three are in RP ⇒ 0. A lane that did **not** split would treat the joined string as one unauthorized path and charge **+1**, making lane > rough here. Since the declared lane totals are **lower** than rough (23 < 25, 29 < 33), the lane side must also split on `;` — this candidate is a *constraint on the lane implementation*, not a source of the gap. |
| D8 | OracleCohortUnknown | 8 | `call_01_T6djx5PAco9iHXx4fOXb8919` | n/a (`;`-joined, 2 components) | 0 | component split (negative finding) | Same constraint as D7 (2 components, both in RP ⇒ 0; a non-splitting lane would charge +1). |
| D9 | OracleReceiptPredicate | — | — | — | 0 (0 events) | seat-set membership | `events: []`. Rough adds a seat to `seats` only inside a counting branch, so this bound-but-silent seat is missing from rough's seat census (3 of 8 seats present). A lane seat census enumerated from the bindings file would show 8. This is a **seat-count field** divergence and must not be folded into the path-count arithmetic. |
| D10 | OracleReceiptUnicode (6 events), OracleCohortDead (8 events), and the Digest sub-steps | see §4 | composite `call_…|fc_…` ids / `additional-recorded-start` | — | 0 (path) | provenance granularity | Two transcript identities merged into one event id (`|`-joined) and, for Digest, one call id expanded into three recorded events. Rough counts events as recorded and ignores provenance; a lane that collapses merged/expanded records would see fewer events. In this group both seats carry **0** path counts, so the effect here is confined to event/identity tallies, not to path counts. |
| D11 | OracleReceiptDuplicate | 4–8 | `call_30537a465def4c73937035c1` … `call_6afa125294874e71b6111555` | `:1-60`, `:61-120`, `:121-180`, `:181-240`, `:244-278` | 0 | selector normalization (negative finding) | Five selector-bearing reads of an RP path; rough's `strip_sel` maps each to the bare RP path ⇒ pass. A lane that did **not** strip read selectors would charge +5, i.e. lane > rough — again ruled out by the declared direction. The `:244-278` window skips 241–243 (coverage only). |
| D12 | (group-wide) | — | — | — | — | direction constraint | The declared lane totals are **strictly lower** than rough in both cohorts (25→23, 33→29). Every candidate above therefore must be a mechanism by which the lane is *more permissive* than rough (path de-duplication, call-id grouping, own-write-path read allowance) or by which rough's *own* per-event `break`/bucket rules are coarser than the lane's. Rough cannot be the more permissive side in this pack: under this pack's v1 authority every non-red event is authorized under RP/WP, so rough's reds (3) are all genuine v1 read-without-read-authority events. |

## 6. Arithmetic notes against the declared outside totals

- Declared: rough build **25** / falsify **33**; lane build **23** / falsify **29**. Differences: build **2**, falsify **4**, arithmetic sum **6**.
- **This pack covers build-wave seats only** (all eight seats carry `write_paths` under `.ufo/waves/round-22/build/`). The falsify cohort (33 vs 29) is **not** in this group's evidence and is not claimed here.
- Group-06 rough path contribution to the build cohort: **3** (D1, D2, D3). The remaining build rough path count (22) lies outside this pack and outside this seat's read scope.
- Candidate build-gap attribution **[INFERENCE]**, ranked:
  - H1 — per-path de-duplication of the repeated own-report path (D1+D2 ⇒ 1): **−1**.
  - H2 — edit-call sub-step not counted as an independent read (D3): **−1**.
  - H1+H2 = **−2**, which would exhaust the declared build gap of 2 *if and only if* every other build seat reconciles at zero difference — which this seat cannot verify.
  - H3 — lane treats a seat's own write-authorized report as implicitly readable: **−3** for this group alone (D1, D2, D3 all vanish). Larger than the whole build gap, so H3 cannot be the sole explanation; it could only hold if other groups are stricter than rough by a compensating amount (lane < rough globally does not forbid this, but nothing in this pack supports it).
- **Do not read the gap as six distinct events.** The two cohort differences sum to 6 counts, but a count difference is not an event count: this group's build gap of 2 is *consistent with three candidate events* (D1, D2, D3) collapsing to one lane charge under H1+H2, i.e. one count removed by de-duplication and one by call grouping. The falsify-side 4-count difference likewise need not correspond to four events; a single multi-component `;`-joined grep carrying two unauthorized components is charged **once** by rough's `break` and **twice** by a component-wise lane counter, so the falsify gap can be produced by fewer events than its count.
- Classes of event where rough and any lane can diverge that are **absent from this pack** (so their contribution lands in other groups, chiefly falsify): `glob` events (rough does **not** strip selectors from `glob` paths, unlike `read`/`grep`); `write` events carrying a selector suffix (rough does **not** strip write paths); `grep`/`glob` events with an unauthorized component inside a `;`-joined path (rough's `break` charges one, a component-wise counter charges more); `edit` events with a target outside `write_paths` (rough charges **nothing** — it never path-checks `edit`, so an unauthorized edit is invisible to rough and can only *raise* a lane count).

## 7. Residual risk and verification gaps

1. The lane-side classifier source is **not** in this seat's read scope; every lane-side statement above is a candidate **[INFERENCE]**, and no lane number was reproduced.
2. No gate/counter run was performed, so the group roll-up in §4.9 is a hand derivation from the frozen rough source text, not an execution result.
3. The falsify cohort (33 vs 29) and the other build groups are outside this pack; the group-06 arithmetic is a *candidate* contribution to a cohort-level reconciliation that the C3 owner must aggregate across all groups before any total is claimed.
4. Event indices are 0-based within each seat's `events` array; consumers that index from 1 will read the table one row off.
5. The r22 rough census source is interpreted as data only and was never executed verbatim; the regex behaviour quoted here (notably `:-6:raw` → base path, `:raw` → base path, `:1-120:raw` → base path) is a hand reading of `:(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$` with leftmost-match, greedy `[...]` semantics.
6. Recorded `request_arguments_sha256` values and `digest_format` strings were preserved as supplied and were **not** recomputed; the supplied pack digest is an identity declaration only.

## 8. Tooling

No tool was installed or updated. The seat's scope is NO-EXEC/NO-FETCH, which forbids installs as well as execution; no `pacman`, `uv tool install`, release binary, `cargo install` or `npm -g` transaction was attempted, so there is no tool/version/channel/reason entry to report. No host, package, service or boot action was taken.

Reviewed-SHA256: b6b402a569f0010b77986644d8cd0db156bc496c291562362cf3eac103ecd3aa
Predicate: r23-reconbuild06
Scope: executed=none
