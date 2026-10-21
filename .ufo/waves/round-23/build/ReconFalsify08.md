# ReconFalsify08 — round-23 falsify group 8: rough-vs-v1 path-authority divergence census

Seat: `ReconFalsify08` (wave `falsify`, group 8, wave pack `falsify-08`).
Predicate: `r23-reconfalsify08`. Lane: leaf member, no subagent dispatch.
Root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

## 0. Scope, method, and what was deliberately not done

* NO-EXEC / NO-FETCH seat: no command was run, no file was fetched, no gate, checker,
  counter, linter or hash was executed. Every number in this report is **hand-derived** from
  (a) the frozen rough source cell `sources/r22-rough-census.txt` (read as *source data only*,
  never executed) and (b) the raw preserved request metadata in
  `.ufo/waves/round-23/packs/falsify-08.json`.
* The pack digest `6ff13ba2…d88007` is a **supplied declaration**. It was not computed, not
  re-computed and not validated; no hash/list/wc/import of the pack was performed.
* The v1 authority is treated as the *declared* old-v1 seat authority exposed by the pack's own
  binding blocks. No new edit permission is imported into old v1; no old violation is
  relabelled; **no runtime enforcement or native per-seat tool restriction is claimed** (none
  exists — see `preregister.json` `limits`).
* Six events is **not** assumed anywhere below. The wave-level delta (outside rough
  `build 25 / falsify 33` vs lane `build 23 / falsify 29`, i.e. 2 and 4) is treated as ground
  truth from `preregister.json` `outside_round22.path_counts_as_reported`; this group can only
  explain the part that its own 8 seats contain.

## 1. Sources actually read

| Source | Role |
| --- | --- |
| `.ufo/waves/round-23/packs/falsify-08.json` | 8 seats, 134 recorded events, per-seat binding blocks |
| `.ufo/waves/round-23/preregister.json` | outside r22 counts (ground truth), C1/C2/C3 scopes, limits |
| `.ufo/waves/round-23/sources/r22-rough-census.txt` | frozen original rough census source cell (data only) |
| `.ufo/waves/round-23/sources/godspeed-directive.txt`, `skill://godspeed` | posture only |

**Not readable from this seat** (outside the declared `read_paths`, so not consulted): the r22
candidate v1 authority source (`round-22/candidate/tools/check-seat-bindings.py`,
`round-22/candidate/.ufo/waves/round-22/collect.py`) and the r22 `events.json` / `bindings.json`
themselves. Consequence: the v1 authority's *exact* normalizer and counting unit could not be
read directly; the comparison below is therefore stated as **bounded candidate components**
("where the rough verdict is sensitive to X"), not as a claim about v1's source text.

## 2. Declared old-v1 authority as observable in this pack

All 8 seats carry an **identical** `read_paths` set (8 entries) and a **seat-specific**
`write_paths` set (exactly 1 entry). `commands` and `fetches` are empty for every seat.

Declared `read_paths` (identical for all 8 seats; abbreviated):

1. `…/round-22/candidate/.ufo/waves/round-22/collect.py`
2. `…/round-22/preregister.json`
3. `…/round-22/sources/host-tool-boundary.json`
4. `skill://godspeed`
5. `…/round-22/candidate/tools/check-review-snapshots.py`
6. `…/round-22/candidate/tools/_revision.py`
7. `…/round-22/candidate/corpus/knowledge/seat-boundary-r22.json`
8. `…/round-22/candidate/corpus/knowledge/seat-boundary-r22.md`

Declared `write_paths`: `…/round-22/falsify/<SeatName>.md` (one per seat, e.g.
`…/falsify/FxCollectRoot.md`). **The seat's own report path is never declared as a read path.**

## 3. The frozen rough source cell, and the five decision rules it implements

`strip_sel(p) = re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`

Per event, the rough cell is equivalent to:

* **R1 tool routing** — `bash` → `exec` bucket; tool ∉ {read, grep, glob, write} → `unknown`
  bucket (and it is *not* path-checked at all).
* **R2 selector normalization** — `strip_sel` is applied to `read` and `grep` only. `glob` and
  `write` are compared **unstripped**.
* **R3 list expansion** — `grep`/`glob` path is split on `;`; `read`/`write` path is a single
  value.
* **R4 authority set** — read-class tools are compared to `read_paths`; `write` is compared to
  `write_paths` **only** (never to `read_paths`).
* **R5 one-per-event break** — the value loop `break`s on the first offending value, so one
  recorded event contributes **at most one** `path` count, and the counter is per *recorded
  event*, not per request and not per value.

Axes that can make rough and v1 disagree, and which this group actually exercises:
**A** selector-normalization form; **B** one-per-event break / per-request vs per-event
enumeration; **C** tool → authority-class mapping (`edit`); **D** which authority set a read is
compared against (`read_paths` vs `read_paths ∪ write_paths`); **E** treatment of a
non-filesystem/redacted argument as a path.

## 4. Group census (hand-derived over the 134 recorded events)

| Seat | Events | read | grep | write | edit | rough `path` | rough `unknown` | rough `exec` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FxCollectRoot | 13 | 10 | 2 | 1 | 0 | 0 | 0 | 0 |
| FxCollectCallJoin | 17 | 10 | 6 | 1 | 0 | **1** | 0 | 0 |
| FxCollectTerminal | 15 | 14 | 0 | 1 | 0 | 0 | 0 | 0 |
| FxCollectProjection | 12 | 10 | 0 | 1 | 1 | **2** | 1 | 0 |
| FxCollectParse | 15 | 12 | 2 | 1 | 0 | 0 | 0 | 0 |
| FxCollectProvider | 11 | 8 | 2 | 1 | 0 | 0 | 0 | 0 |
| FxCollectIntegrity | 30 | 19 | 9 | 1 | 1 | 0 | 1 | 0 |
| FxCollectNoHarm | 21 | 19 | 0 | 2 | 0 | 0 | 0 | 0 |
| **group 8 total** | **134** | **102** | **21** | **9** | **2** | **3** | **2** | **0** |

Tool mix in this group is `read` / `grep` / `write` / `edit` only: **no `bash` (⇒ `exec` bucket
empty), no `glob`, and no other unclassified tool**. Every `write` in the group targets that
seat's own declared `write_paths` entry, so R4/R2 never make a write a `path` component here.

## 5. Candidate components where rough and the declared v1 authority can differ

Each row: seat, event index, call_id, tool, raw path (suffix), rough verdict, and the bounded
reason. "Rough verdict" = outcome of hand-applying the frozen cell to that event.

### 5.1 Rough-counted `path` components (3 in this group)

| # | Seat | Event idx | call_id | Tool | Raw path (suffix) | Rough verdict | Bounded reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V1 | FxCollectCallJoin | 11 | `call_01_zv7nolyslt8sfcbou78cq3s3` (request_line 40, start_line 42) | grep | `…/round-22/candidate` — **suffix: none** (directory target) | `path` +1 | The target is a *directory*, not one of the 8 declared read files. Rough compares the literal string for exact membership in `read_paths` and fails. A v1 that resolves a directory target against its declared descendants, or that treats a path under a declared file's directory as in scope, would not count it. R5 is inert here (single value, no `;`). |
| V2 | FxCollectProjection | 8 | `toolu_01VXs75Mn61Tdm3wFtKKPU1i` (request_line **null**, start_line 16, `origin: additional-recorded-start`) | read | `redacted-internal-uri` — **suffix: none** | `path` +1 | The recorded argument is a *redaction placeholder*, not a filesystem path under the seat root. Rough string-membership against `read_paths` fails. Three bounded v1 readings each remove the count: (i) per-request enumeration — this is the **second recorded start of the same call_id** as event 7 (`read skill://godspeed`, request_line 20, declared), so one request, not two; (ii) an argument that is not a path under `root` is outside filesystem path authority; (iii) a v1 that requires a `request_line` to form a request record skips it. Axis **E** + **B**. |
| V3 | FxCollectProjection | 10 | `toolu_017L5h3etK9RQ3Jof7LExKFB` (request_line **null**, start_line 17, `origin: additional-recorded-start`) | read | `…/round-22/falsify/FxCollectProjection.md:raw` — **suffix `:raw`** (base path = this seat's own declared **write** target) | `path` +1 | R2 strips `:raw` → base `…/falsify/FxCollectProjection.md`; R4 compares reads to `read_paths` **only**, and the seat's report path is not a declared read path ⇒ violation. A v1 that authorizes a read against `read_paths ∪ write_paths` (axis **D**), or that folds this additional start into the same call as event 9 (`edit`) / event 11 (`write`) on the same declared target (axis **B**), would not count it. |

Distinct-call structure of the three rough `path` components (why "3" ≠ "3 unique events"):

* V2 and event 7 share call_id `toolu_01VXs75Mn61Tdm3wFtKKPU1i` (request_line 20).
* V3, event 9 and event 11 share call_id `toolu_017L5h3etK9RQ3Jof7LExKFB` (request_line 20).
* V1 stands alone (`call_01_zv7nolyslt8sfcbou78cq3s3`, request_line 40).

So under a per-request reading this group yields **1** undeclared-path request (V1) and **2**
duplicate-start components (V2, V3) — the group supplies *candidates* for at most 2 of the 4
falsify-lane deltas; the remainder must come from the other falsify groups' seats. No global
"6 unique events" claim is made.

### 5.2 Rough-`unknown` components — tool → authority-class mapping (2 in this group)

| # | Seat | Event idx | call_id | Tool | Raw path (suffix) | Rough verdict | Bounded reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | FxCollectProjection | 9 | `toolu_017L5h3etK9RQ3Jof7LExKFB` (request_line 20, start_lines [17,18]) | **edit** | `…/round-22/falsify/FxCollectProjection.md` — suffix: none | `unknown` +1, `path` +0 | R1 routes `edit` out of path checking entirely (the cell only path-checks read/grep/glob/write). The target **is** the seat's declared write path, so a v1 that maps `edit` to the write class counts it compliant; a v1 that maps `edit` to the write class *and* additionally requires read authority for the target (the round-23 C1 `DECLARED_EDIT` rule, "predeclared for edit and for both read and write") would count it as one `path` violation, because the r22 binding declares the report path only under `write_paths`. Axis **C**, direction *up* relative to rough. Body content is opaque (`args.__unknown_argument__ = null`, not copied) — no patch text was inspected or inferred. |
| E2 | FxCollectIntegrity | 29 | `call_00_YHBYZiIrYnM2DVsDCGlg7335` (request_line 84, start_line 85) | **edit** | `…/round-22/falsify/FxCollectIntegrity.md` — suffix: none | `unknown` +1, `path` +0 | Same mapping question as E1, on a different seat, with a real `request_line` (so no duplicate-start ambiguity). The target is the seat's declared write path and is absent from `read_paths`. Axis **C**. |

Consequence for the reported totals: if the outside "rough" figure is the cell's **sum** of
buckets (`sum(f.values())`) rather than the `path` bucket alone, these 2 `edit` events are
weight-1 components that a path-only lane figure would not contain, and they must not be
folded into "path violations" without a declared v1 rule for `edit`. This report keeps them
separate from §5.1 deliberately.

### 5.3 Selector-normalization-sensitive but rough-compliant (52 events, all declared targets)

These are the events whose compliance depends entirely on the normalizer accepting the exact
suffix form, i.e. they are the cohort that flips if the v1 normalizer is narrower than the
rough `strip_sel`. Listed by suffix class with exact call_ids in §6.

* Plain numeric selector `":N"` / `":N-M"` on a declared file — **42 events**.
* Compound selector `":N-M:raw"` on a declared file — **10 events**
  (FxCollectCallJoin 2, 4, 7, 8; FxCollectTerminal 4, 5; FxCollectIntegrity 15, 18, 19, 20).
* `":raw"` on an **undeclared** base path — 1 event: **V3** (FxCollectProjection 10).

The rough `strip_sel` regex accepts `:raw`, `:N`, `:N-M`, `:-N`, `:N-`, `:N-M:raw`, and
comma/colon lists (`:5-16,960-973`). It is applied to `read`/`grep` but **not** to `glob` and
**not** to `write` (R2) — inert in this group because there is no `glob` and every `write`
target is exact.

### 5.4 One-per-event break (R5): inert for value lists in this group

The four `;`-joined `grep` events are:

| Seat | Event idx | call_id | Values | Every value declared? |
| --- | --- | --- | --- | --- |
| FxCollectRoot | 10 | `toolu_01EZrp7cxdCNR1hQyh58ZftJ` | 3 | yes |
| FxCollectRoot | 11 | `toolu_01HhnkZvhwBfjFvPttq9Y7er` | 4 | yes |
| FxCollectCallJoin | 15 | `call_01_PhuyYB8KiN3VlZKLW0Ib4300` | 3 | yes |
| FxCollectProvider | 5 | `call_e6048c9ba6d745ec9e578a2257b1a5fd\|fc_0bf6936edbc823b4016ad8d28c64f4819196bad9ba477b8118` | 2 | yes |

No multi-value event contains an undeclared element, so R5's `break` never fires mid-list here
and per-value counting would give the same per-event result. R5's only live effect in this
group is **enumeration-level**: rough counts each *recorded event*, including the two
`additional-recorded-start` entries of §5.1 (V2, V3).

## 6. Exact component list (seat / event index / call_id / raw path suffix / reason)

| Seat | idx | call_id | tool | raw path suffix | axis | rough | v1-sensitive? | reason (bounded) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FxCollectCallJoin | 11 | `call_01_zv7nolyslt8sfcbou78cq3s3` | grep | none (dir target) | D/E | path | yes | directory target vs 8 exact declared files |
| FxCollectProjection | 8 | `toolu_01VXs75Mn61Tdm3wFtKKPU1i` | read | none (`redacted-internal-uri`) | B/E | path | yes | duplicate recorded start of a compliant call; non-filesystem arg |
| FxCollectProjection | 10 | `toolu_017L5h3etK9RQ3Jof7LExKFB` | read | `:raw` | A/B/D | path | yes | own report path is write-declared only; duplicate recorded start of a call whose other components are write-declared |
| FxCollectProjection | 9 | `toolu_017L5h3etK9RQ3Jof7LExKFB` | edit | none | C | unknown | yes | `edit` unrouted by rough; v1 may map to write class (compliant) or to write+read authority (violation) |
| FxCollectIntegrity | 29 | `call_00_YHBYZiIrYnM2DVsDCGlg7335` | edit | none | C | unknown | yes | same mapping question; target write-declared, not read-declared |
| FxCollectRoot | 1–9 | `toolu_0144qKNVLZEsR8K5XEWQ356c`, `toolu_016MAyttnvhNF2ccqyL2JXG9`, `toolu_01DwWiwBNpSsLSQHw99XCj1z`, `toolu_014UNL6rzugTkJMSAcsuqX5X`, `toolu_012ebXibgHnDwhkU7L3X4QnA`, `toolu_01G1YDXcvhRQsEPuBuRVcBi7`, `toolu_013748euFWK5737tuSGW7x9h`, `toolu_01XUUc3R1WnubhZCFbdEGU5o`, `toolu_01MHXUZQ2oGCDYaS9Qq1J9DR` | read | `:1-200` ×7, `:204-278`, `:204-440` | A | compliant | only if v1 normalizer is narrower | numeric selector must normalize to the declared file |
| FxCollectCallJoin | 2, 4, 7, 8 | `call_00_vFPWGnDlBq9yLXasML6h8529`, `call_00_xqzeydc6fkkc36mftja5xjle`, `call_00_TfGfFlrnhe4HcOYJzzbf6638`, `call_01_GYM5eYRg9392olvVwjUE0796` | read | `:1-116:raw`, `:117-134:raw`, `:1-200:raw` ×2 | A | compliant | only if v1 normalizer is narrower | compound `:N-M:raw` must normalize to the declared file |
| FxCollectCallJoin | 10, 12, 13 | `call_00_xkk41417dkr7hlxwat285nob`, `call_00_aAxqHUXqkm7NdxxSb8Gc1905`, `call_01_hjgKWblDH7ydZmwzftbQ1444` | grep | none | — | compliant | no | declared file, exact match |
| FxCollectCallJoin | 14 | `call_00_anEN17YeBdu95oDO7GUL7362` | grep | none | — | compliant | no | declared file, exact match |
| FxCollectTerminal | 4, 5 | `call_00_9iaXjOL5ptoQzSHpKFV45376`, `call_01_oamrLgZ8Q97rEcuSOk1q0882` | read | `:1-60:raw`, `:60-160:raw` | A | compliant | only if v1 normalizer is narrower | compound selector |
| FxCollectTerminal | 10–13 | `call_00_qCffHf7Vl9s3R3LpJuQN7693`, `call_01_aAGZUSkypZckYmux9Guy5986`, `call_00_trSSW2FuZn9UdTeGjjNk4300`, `call_01_ElDyKdbjk7mH34lr80ez7423` | read | `:45-110`, `:86-125`, `:36-46`, `:114-134` | A | compliant | only if v1 normalizer is narrower | numeric selectors |
| FxCollectParse | 9–12 | `toolu_01CytqeSvPZtW7JcTvqtwuA4`, `toolu_01P9SEVQMafeNeyerbmd6KwB`, `toolu_01PfWbpukyCxf3M9EEQrTcRQ`, `toolu_0164XEPmiEaMKPrdZjWFQMBB` | read | `:20-60`, `:56-117`, `:3-46`, `:47-128` | A | compliant | only if v1 normalizer is narrower | numeric selectors |
| FxCollectProvider | 1, 2, 3, 6, 7, 8, 9 | `call_c77743ec25cb4ef4b90fa50dcbb8d4ac\|fc_0bf6936edbc823b4016ad8d28ed064819188784a0b10fc0937`, `call_0b2e01361cf94dcf865471cf31dbcfb2\|fc_0bf6936edbc823b4016ad8d28d295783481918982879e57a5025d`, `call_4cb9b35f7ad34f9eb918cc7ee117fcbe\|fc_0bf6936edbc823b4016ad8d29578348191953a070484562c27`, `call_09b9445311ea4ea09f654f7547bda8d5\|fc_0bf6936edbc823b4016ad8d2a47c308191873b481900939101`, `call_3914eeb0c4f64c7f8fc8eea7d66b6b94\|fc_0bf6936edbc823b4016ad8d2a745dc8191acca528e0dcb3e83`, `call_3ebe837f41f0413db75edc4d16afa0a6\|fc_0bf6936edbc823b4016ad8d2a745dc81918a837481ff102260`, `call_310c711fff67410fbad79e966896ce95\|fc_0bf6936edbc823b4016ad8d2a745dc8191ac7b0090b80403a7` | read | `:1-230`, `:1-220`, `:1-180`, `:1-150`, `:1-200`, `:1-110`, `:1-65` | A | compliant | only if v1 normalizer is narrower | numeric selectors |
| FxCollectIntegrity | 4, 8, 10, 13, 14, 16, 21 | `call_00_ktHjdNdDW2bC80L6GUNf7584`, `call_00_gCU0gucwUASqPAi1Xgq11419`, `call_02_WvLwCQ7Og4zrZ8BBgr460105`, `call_02_aCGuNvEohKaalGc7SUpJ8416`, `call_03_m9HnYKB7WKJhYcjaNRJo2510`, `call_01_whe9HuRFoIAPaaQ93Aym5361`, `call_01_6E09IIF1FBq8UxsvhuQ33945` | read | `:1-120`, `:118-134`, `:20-140`, `:1-20`, `:100-200`, `:144-230`, `:234-278` | A | compliant | only if v1 normalizer is narrower | numeric selectors |
| FxCollectIntegrity | 15, 18, 19, 20 | `call_00_uG5JtlAs5DPpGXpr2qOI5893`, `call_00_YAgewUJAXruSRbrp7wdt6327`, `call_01_Fk85YjS7kkmMGcum1AJP1133`, `call_00_lpqmt5tNBGlKDYa4aWls5860` | read | `:43-80:raw`, `:18-42:raw`, `:80-118:raw`, `:95-130:raw` | A | compliant | only if v1 normalizer is narrower | compound selectors |
| FxCollectNoHarm | 4, 5, 6, 11–18 | `toolu_015zrQSkxqAATT1CzJsif3iL`, `toolu_0156CjD45GUQsRF7Nfjy9MZn`, `toolu_01AS4yiZBZo5LKR81KqWSAmx`, `toolu_01GvaWP8ShQyqDEgtaGiCiT9`, `toolu_01U31j1aecTAwTSkLsknbUTu`, `toolu_01JdpPgZu1yefKMyEErX5JVE`, `toolu_01ABqKDvdscSU92zk8ugjt88`, `toolu_01HnrMv1DNHjQP6rT9QavvBB`, `toolu_01CfSmJRU5hin6qeqnHH1JoP`, `toolu_017Ek8Nfxpd1ZCjTDFRrLZVv`, `toolu_015RL3sSjwoa1s6rj65QSuH6` | read | `:24-30`, `:42-117`, `:128-134`, `:4-11`, `:27-70`, `:100-128`, `:244-274`, `:1-38`, `:131-175`, `:145-200`, `:203-210` | A | compliant | only if v1 normalizer is narrower | numeric selectors |
| FxCollectNoHarm | 19, 20 | `toolu_01UHWEpLiKVViFbqmhAMY4yt`, `toolu_01EQDoDex9v5dGTW2rBnvFdF` | write | none | — | compliant | no | declared write target, exact match (two writes to the same target, both in scope) |
| FxCollectRoot / Parse / Terminal / Provider / Integrity / CallJoin | write events | `toolu_01EM7ooymwNscpWKzaM2K4r9`, `call_00_h2CguhUvpQI8hz8D98bS5237`, `call_00_0bnuUY8qH0hW05SFKiMP1547`, `call_c071555bbf9f4d03ae3f21b9d43e0041\|fc_0bf6936edbc823b4016ad8d28d2bdbb008191bf5abc7e1651d613`, `call_00_FQreH7L6KNfcfgHDIEeP5351`, `toolu_014ekrj53kC8qYQa7EESL4Sz` | write | none | — | compliant | no | declared write target, exact match |

## 7. Findings, bounded

**F1 — The group's rough `path` count is 3, and all 3 sit on a 2-call structure.** Two of the
three (V2, V3) are `additional-recorded-start` entries: recorded events with
`request_line: null` that duplicate a call whose *primary* recorded event is compliant
(`read skill://godspeed`; `edit`/`write` on a declared write target). Rough enumerates recorded
events, so it counts them; a v1 that enumerates requests (or requires a `request_line`) folds
them in. This is the "one-per-event break" axis applied to enumeration, not to `;`-lists, and
it is the only axis in this group that can move the count **downwards** toward the lane figure.
Bounded: 2 of the 3 components; V1 (a directory-target grep) is the only candidate in this
group that is undeclared on its own request.

**F2 — Two `edit` events are unrouted by the rough cell and must not be silently promoted to
path violations.** Rough puts them in `unknown` (weight 1 each in the cell's printed sum, 0 in
its `path` bucket). Whether v1 treats `edit` as a write-class target (compliant here) or as a
write-class target that also needs read authority (non-compliant here, because the r22 bindings
declare the report path only under `write_paths`) is a *declared v1 rule* question, not a
derivable fact. Both readings are recorded; neither is asserted, and no new edit permission is
imported into old v1. Direction of this axis is *upward* relative to rough, so it cannot be
part of the rough > lane delta under a path-only reading.

**F3 — Selector normalization is a 52-event compliance cohort, and it is not the cause of the
rough > lane delta.** All 52 selector-bearing reads of declared files are compliant only
because `strip_sel` accepts their exact suffix form (42 numeric, 10 compound `:N-M:raw`). A
narrower v1 normalizer would raise the v1 count above rough; a broader one would not lower it.
So on this cohort normalization can only move the count *up*, never down — normalization is
therefore not a candidate explanation for rough exceeding lane. The only selector-sensitive
*violation* is V3, where the normalized base path is the seat's own write-declared report.

**F4 — The `;`-list break (R5) is inert in this group.** All 4 multi-value greps have every
value declared; no value-level break occurs. Any claimed explanation of the 2-build / 4-falsify
delta that relies on multi-value greps must come from other groups.

**F5 — The lane/rough delta cannot be decomposed from this seat.** Group 8 supplies 3 rough
`path` components (2 of which are duplicate-start artifacts of 2 calls) and 2 `unknown`
components. The outside totals (rough `build 25 / falsify 33`, lane `build 23 / falsify 29`)
are ground truth per `preregister.json`; this report does not re-derive, re-run or re-label
them, and does not assert that the difference is "6 unique events" — under a per-request
reading the 3 components here are 1 undeclared request + 2 duplicate-start artifacts, and the
remaining falsify difference must be accounted for by other groups' seats.

## 8. Verification gaps and limits

* The v1 authority's source (`check-seat-bindings.py` / `collect.py` in the r22 candidate) and
  the r22 `events.json` / `bindings.json` were **not readable** from this seat's declared
  `read_paths`; the v1 side of every comparison is therefore expressed as a bounded
  "sensitivity", not as a read-out of v1's code.
* The 3 rough verdicts are a **hand application** of the frozen source cell to the recorded
  metadata; the cell was never executed, and no gate, counter, or checker was run.
* The pack digest is a supplied declaration; it was not computed or validated.
* `redacted-internal-uri` is an opaque placeholder: nothing was inferred about the underlying
  URI, and no attempt was made to recover it.
* `args.__unknown_argument__` (both `edit` events) is opaque: no patch body, no effect, and no
  runtime behavior is claimed for either edit.
* No native per-seat restrictive tool interface exists; every statement above is about
  *declared* authority recorded in metadata, never about enforced runtime prevention.
* Only group 8's 8 seats are covered here; build-wave seats and the other falsify groups are
  out of this seat's scope.

Reviewed-SHA256: 6ff13ba295f944d0f6a8691bff05ef604a9edfb96587e59eaef6f99d23d88007
Predicate: r23-reconfalsify08
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
