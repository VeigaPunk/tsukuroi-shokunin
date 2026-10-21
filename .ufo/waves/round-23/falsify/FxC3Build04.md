# FxC3Build04 — falsification of candidate/ledger-slices/build-04.json

Seat: FxC3Build04 (reviewer). Wave: round-23, FALSIFY, group 4.
Target: `.ufo/waves/round-23/candidate/ledger-slices/build-04.json`
Declared SHA256 (supplied identity, not independently computed): `08d8ebbb0aa59f18a913dee9cf3b997130d4bc7672f72c48803a7760dbb890e8`
Landed baseline under review: `5a25c88b77f52e940bcad87825c4ac1cd529470d`; r22 baseline `ae01e50f582016384e620022be38bf5367000e2e`.

## Axes named

1. **A1 rough fidelity** — every `rough_category` / `rough_first_bad` / `rough_path_count` re-derived by hand from the pack events and bindings under the *exact* S085 regex and break rule (`.ufo/waves/round-23/sources/r22-rough-census.txt`).
2. **A2 canonical fidelity** — every `canonical_bad` / `canonical_path_count` re-derived under *literal v1 authority* (the binding's literal `read_paths` / `write_paths` grant lists, no inference, no prefix/traversal widening) and the same selector grammar.
3. **A3 disposition honesty** — `disposition` must equal the actual agreement between the rough side and the canonical side, and must not be readable as "permitted".
4. **A4 row↔pack bijection and completeness** — every ledger row must map to exactly one pack event (keyed by `call_id` + `request_arguments_sha256` + `site` index), and every pack event of every seat in the pack must have a row.
5. **A5 structural count mechanism** — whether this slice can contribute to the declared rough-vs-lane path-count gap (preregister `outside_round22.path_counts_as_reported`: rough build 25 vs lane build 23; rough falsify 33 vs lane falsify 29).

## Attack and falsifier

Attacked claim: **C3** (`unexplained_cohorts` 2 → 0; "exhaustive per-event/component explanation of rough-versus-lane path counts"), and through it the frontier claim that the landed ledger explains every captured r22 event. C1/C2 are implicated only through the *meaning* of `canonical_bad`/`disposition` on the two `edit` rows (C1's declared edit matrix vs C3's v1 path frame).

Falsifier attempted (bounded, exhaustive over the slice): for each of the 39 rows, recompute
* S085 category: `t=='bash'` → exec; `t not in ('read','grep','glob','write')` → unknown; else per path component (split on `;` for grep/glob, single component otherwise), `q = strip_sel(v)` for read/grep and `q = v` otherwise, with `strip_sel(p) = re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`; a component is *bad* iff `q ∉ (write_paths if t=='write' else read_paths)`; the rough side reports the first bad component index and, per the S085 break rule, one `path` hit per event;
* canonical side: the same component split, with the *literal* v1 grant lists and the same selector grammar; a canonical bad component is one whose stripped spelling is not literally granted;
and then require `disposition` to equal the actual agreement of the two sides.

Search space covered: 39 rows / 37 distinct `call_id`s / 7 seats carrying events (OracleWriteReport carries none) / all 44 pack events in `packs/build-04.json` (39 with events + OracleWriteReport empty). Result: **no row falsified on A1–A4**.

## Per-row re-derivation

Grant lists, all seats (identical shape): `read_paths = { .../round-22/sources/host-tool-boundary.json, .../round-22/preregister.json, skill://godspeed }`, `write_paths = { .../round-22/build/<SeatName>.md }`. Note `skill://godspeed` is a literally granted non-filesystem URI in every seat.

| site | call_id | tool | path spelling | S085/canonical outcome |
|---|---|---|---|---|
| OracleWriteOther:0 | call_00_ET_GhK9CtCtlThJVTzUM3h38234 | read | `.../sources/host-tool-boundary.json` | in read grant → clean/clean ✓ |
| OracleWriteOther:1 | call_01_ET_6GEj8FwUIw577uIZ5j4u7170 | read | `.../round-22/preregister.json` | in read grant → clean/clean ✓ |
| OracleWriteOther:2 | call_02_ET_E2IoAZ5dA228dmilpTt66676 | read | `skill://godspeed` | literal grant → clean/clean ✓ |
| OracleWriteOther:3 | call_00_lSviKjpSHMPqsvS5pbAV1873 | grep | `.../sources/host-tool-boundary.json` | in read grant → clean/clean ✓ |
| OracleWriteOther:4 | call_01_MkkgGAGtClEuheYamz6E1606 | grep | `.../round-22/preregister.json` | in read grant → clean/clean ✓ |
| OracleWriteOther:5 | call_02_7S59a04bKvLi5uIfCF4G7044 | read | `.../sources/host-tool-boundary.json:raw` | `:raw` stripped → granted → clean/clean ✓ |
| OracleWriteOther:6 | call_50b4bc28b3b44afeb1befc8f | write | `.../build/OracleWriteOther.md` | in write grant → clean/clean ✓ |
| OracleWriteOther:7 | call_c2fd3b11623d47b8a8731fc6 | read | `.../build/OracleWriteOther.md:-6` | `:-6` stripped → `.../build/OracleWriteOther.md` ∈ write grant, ∉ read grant → **path**, first bad component 0 → canonical_bad [0] ✓ |
| OracleWriteOther:8 | call_5bf42407a30d4f5e8e2f8d37 | grep | `.../build/OracleWriteOther.md` | no selector; ∉ read grant → **path**, first bad component 0 → canonical_bad [0] ✓ |
| OracleWritePrefix:0 | toolu_01S4i5ujkogyGjcULDptW8VQ | read | `.../sources/host-tool-boundary.json` | clean/clean ✓ |
| OracleWritePrefix:1 | toolu_01FF42FmjY4DPMHAYKtoH2wU | read | `.../round-22/preregister.json` | clean/clean ✓ |
| OracleWritePrefix:2 | toolu_01Q51bu1WSATPapAWZXEUhiv | edit | `.../build/OracleWritePrefix.md` (+`__unknown_argument__`) | tool not in S085 tuple → **unknown**, 0 path components; canonical (v1: no edit tool) → no path classification → canonical_bad [] ✓ |
| OracleWritePrefix:3 | toolu_01Q51bu1WSATPapAWZXEUhiv | read | `.../build/OracleWritePrefix.md:raw` | `:raw` stripped → ∉ read grant → **path**, first bad 0 → canonical_bad [0] ✓ |
| OracleWritePrefix:4 | toolu_01Q51bu1WSATPapAWZXEUhiv | write | `.../build/OracleWritePrefix.md` | in write grant → clean/clean ✓ |
| OracleWriteTraversal:0 | call_5b1fa9899233456ca2ffa9e2 | read | `skill://godspeed` | clean/clean ✓ |
| OracleWriteTraversal:1 | call_1f552220ce084c278710bb19 | read | `.../sources/host-tool-boundary.json` | clean/clean ✓ |
| OracleWriteTraversal:2 | call_45fadda7116c4ebfa560f673 | read | `.../round-22/preregister.json` | clean/clean ✓ |
| OracleWriteTraversal:3 | call_5ccd84229aca4656b9d238c9 | write | `.../build/OracleWriteTraversal.md` | in write grant → clean/clean ✓ |
| OracleEditUnknown:0 | call_00_ET_eMgHKMRQHd9cJTMqYpTM1375 | read | `.../sources/host-tool-boundary.json` | clean/clean ✓ |
| OracleEditUnknown:1 | call_01_ET_HBL8mdbBT1ld5e5TaeD63089 | read | `.../round-22/preregister.json` | clean/clean ✓ |
| OracleEditUnknown:2 | call_02_ET_mk9tzQj9eABUzu1bKoQI3927 | read | `skill://godspeed` | clean/clean ✓ |
| OracleEditUnknown:3 | call_00_wI2J5adtQgp96oGfuwZB1811 | grep | `.../sources/host-tool-boundary.json` | clean/clean ✓ |
| OracleEditUnknown:4 | call_01_IFVP9RvyYFLkL0OvjqS81442 | grep | `.../sources/host-tool-boundary.json;.../round-22/preregister.json` | two components, both granted → clean/clean ✓ |
| OracleEditUnknown:5 | call_02_8Qas8PtdyU0LTujHDzuT7967 | grep | `.../round-22/preregister.json` | clean/clean ✓ |
| OracleEditUnknown:6 | call_00_g55Vz9baWHUAurFrEleu3226 | write | `.../build/OracleEditUnknown.md` | in write grant → clean/clean ✓ |
| OracleUnknownTool:0 | call_5988cf4356014e25a307da2728a1b8cc\|fc_03a84d5b4b60e00f016ad8cf10f5788191af7f062060037640 | read | `skill://godspeed` | clean/clean ✓ |
| OracleUnknownTool:1 | call_90b37914eee242d4a0e33e7ee448bfca\|fc_03a84d5b4b60e00f016ad8cf1303c48191ba8b2d7b36d12e83 | read | `.../sources/host-tool-boundary.json:1-200` | `:1-200` stripped by the `\d[\d\-+,:]*` alternative → granted → clean/clean ✓ |
| OracleUnknownTool:2 | call_85ab1496d1b64cf5b8b33ed183f5d424\|fc_03a84d5b4b60e00f016ad8cf1303c48191a63d12d1e43b5a74 | read | `.../round-22/preregister.json:1-200` | stripped → granted → clean/clean ✓ |
| OracleUnknownTool:3 | call_9a90bb0ae9f64586a6b8d5905642d83e\|fc_03a84d5b4b60e00f016ad8cf3dc6a08191899185095e2ec36b | write | `.../build/OracleUnknownTool.md` | in write grant → clean/clean ✓ |
| OracleParallelExec:0 | call_582c072dc13e4e68bc1e94d2 | read | `skill://godspeed` | clean/clean ✓ |
| OracleParallelExec:1 | call_bf9d6ff1d3224b94aee0c7f4 | read | `.../sources/host-tool-boundary.json` | clean/clean ✓ |
| OracleParallelExec:2 | call_b802b3ceee114501a2d75b7c | read | `.../round-22/preregister.json` | clean/clean ✓ |
| OracleParallelExec:3 | call_f4f7888e21a642cd91584b4c | write | `.../build/OracleParallelExec.md` | in write grant → clean/clean ✓ |
| OracleParallelFetch:0 | call_00_ET_eNk0gSDqAffHJ6LM3DlJ3942 | read | `.../sources/host-tool-boundary.json` | clean/clean ✓ |
| OracleParallelFetch:1 | call_01_ET_p4rQYCDXqpkYLYQb3CXZ9477 | read | `.../round-22/preregister.json` | clean/clean ✓ |
| OracleParallelFetch:2 | call_02_ET_VtbJJy96aSy2WxOAMNtU5025 | read | `skill://godspeed` | clean/clean ✓ |
| OracleParallelFetch:3 | call_00_XRdzqysfNn5kTuso6T1x5101 | write | `.../build/OracleParallelFetch.md` | in write grant → clean/clean ✓ |
| OracleParallelFetch:4 | call_00_eGrf2wnOfSVOI0bOwJEp0230 | read | `.../build/OracleParallelFetch.md:-6` | `:-6` stripped → ∉ read grant → **path**, first bad 0 → canonical_bad [0] ✓ |
| OracleParallelFetch:5 | call_00_ZU8KN22IthleSncxw9x04698 | edit | `.../build/OracleParallelFetch.md` (+`__unknown_argument__`) | tool not in S085 tuple → **unknown**; canonical (v1) → canonical_bad [] ✓ |

Key identity check (A4): all 39 `request_arguments_sha256` values in the slice match the corresponding pack event's `request_arguments_sha256` string literally (no hashing performed; string equality against the supplied declarations), including the three OracleWritePrefix rows that share one `call_id` (`toolu_01Q51bu1WSATPapAWZXEUhiv`) and are distinguished only by `request_arguments_sha256` and `site` index. `site` indices are contiguous from 0 per seat and in pack event order.

## Rows whose recorded value I dispute

**None on A1–A3.** Every recorded `rough_category`, `rough_first_bad`, `rough_path_count`, `canonical_bad`, `canonical_path_count` and `disposition` is reproduced by hand from the pack.

### Non-agree (non-clean) rows checked, and the path spelling that drove them

There are **zero** rows with `disposition` ≠ `agree` in this slice. The six rows whose rough category is not `clean` — i.e. every row where the two sides had something to agree about — are:

1. `OracleWriteOther:7` / `call_c2fd3b11623d47b8a8731fc6` — spelling `.../round-22/build/OracleWriteOther.md:-6`; the `:-6` selector is stripped, exposing a path that is only in `write_paths`, so a *read* of it is out of the literal read grant. canonical_bad [0].
2. `OracleWriteOther:8` / `call_5bf42407a30d4f5e8e2f8d37` — spelling `.../round-22/build/OracleWriteOther.md` (no selector); same grant gap, reached through `grep` (whose authority set is `read_paths`).
3. `OracleWritePrefix:3` / `toolu_01Q51bu1WSATPapAWZXEUhiv` — spelling `.../round-22/build/OracleWritePrefix.md:raw`; the `:raw` selector is stripped, exposing the same read-of-a-write-only-path gap. canonical_bad [0].
4. `OracleParallelFetch:4` / `call_00_eGrf2wnOfSVOI0bOwJEp0230` — spelling `.../round-22/build/OracleParallelFetch.md:-6`; same mechanism. canonical_bad [0].
5. `OracleWritePrefix:2` / `toolu_01Q51bu1WSATPapAWZXEUhiv` — spelling `.../round-22/build/OracleWritePrefix.md`; tool `edit` is outside the S085 tuple, so the rough side records `unknown` and the v1 canonical side records no path component. canonical_bad [].
6. `OracleParallelFetch:5` / `call_00_ZU8KN22IthleSncxw9x04698` — spelling `.../round-22/build/OracleParallelFetch.md`; same `unknown` / no-canonical-component outcome.

The driving spelling pattern is exactly one: **a seat reading (or grepping) the very report file it is granted to write, with the read path spelled as `<write-path>` or `<write-path>:<selector>`**. Under literal v1 authority the seat holds *write* but not *read* on that file, so the component is bad. Both the rough and the canonical side reach that same component index (0), which is why every one of these rows is `agree` rather than a rough/lane divergence.

## Findings (severity ordered)

### F1 — Medium: "agree" on an `edit` row is ambiguous between *classified outside v1 path scope* and *authorized*. The ledger records `canonical_bad: []` + `disposition: "agree"` for the two `edit` rows, while preregister C1's own decision matrix would **DENY** both (target is predeclared for write but not for read → `WRITE_ONLY_EDIT → DENY`; and the patch body is carried as `__unknown_argument__` → `OPAQUE_PATCH → UNKNOWN`; and C1's `UNDECLARED_EDIT → DENY` covers implicit permission from generic report ownership). The slice's value is *correct for the C3 v1 frame* (v1 has no `edit` tool, so there is no path component to be bad) — but the recorded fields are literally read as "no canonical bad component ⇒ nothing wrong". Evidence: `packs/build-04.json` events for `toolu_01Q51bu1WSATPapAWZXEUhiv` (tool `edit`) and `call_00_ZU8KN22IthleSncxw9x04698` (tool `edit`), vs `preregister.json` `edit_decisions` entries `WRITE_ONLY_EDIT/DENY`, `OPAQUE_PATCH/UNKNOWN`, `UNDECLARED_EDIT/DENY`.
Remedy (smallest, in-scope): record the authority frame per row — e.g. a `canonical_authority` / `permission` field distinguishing `v1-out-of-scope-tool` from `v1-granted`, or an explicit `v2_edit_decision` field carrying the C1 outcome for `edit` rows — so `canonical_bad: []` cannot be misread as permission. No row value changes.

### F2 — Medium: per-seat coverage of the pack is not asserted, and `OracleWriteReport` is a zero-event seat with a declared write path. The pack gives `OracleWriteReport` a full binding with `write_paths = [.../round-22/build/OracleWriteReport.md]` and `events: []`, and the slice therefore has no `OracleWriteReport:*` row at all, while every one of the other seven seats records a `write` event on its own report path. The slice's `scope` string ("Exact rows of the landed ledger for this pack") makes the zero silently consistent with the pack, but the pack's own scope is "Raw preserved request metadata only" — so the C3 "exhaustive per-event explanation" claim is only *pack-relative*, and nothing in the slice shows whether OracleWriteReport's r22 requests were captured at all. I cannot check the underlying r22 transcript (outside this seat's declared read paths).
Remedy (smallest, in-scope): add one ledger row for `OracleWriteReport` with an explicit non-violation category (e.g. `rough_category: "no-events"`, `disposition: "not-exercised"`), and/or a per-seat `event_count` field, so an empty seat is declared rather than invisible.

### F3 — Low: `disposition` is not independently re-derivable from the row's own fields for the two `unknown` rows. The slice schema records only `canonical_bad` / `canonical_path_count` on the canonical side; there is no `canonical_category`. For the two `edit` rows the rough side says `unknown` while the canonical side says (implicitly) "no path component", so "agree" asserts agreement between two *categories* that the schema cannot express — it is only verifiable by re-running the classifier (out of scope for a reader of the slice). All 37 other rows are verifiable by arithmetic on the recorded fields alone.
Remedy (smallest, in-scope): add `canonical_category` to the row schema (values mirroring `clean` / `path` / `unknown` / `exec`), which makes `disposition` checkable by inspection for every row.

### F4 — Low: S085's per-event break rule versus the ledger's per-component `rough_path_count` are indistinguishable in this slice. S085 counts **one** `path` hit per event (it `break`s at the first bad component), while the slice's `rough_path_count`/`canonical_path_count` are component counts. The only multi-component event in the pack (`OracleEditUnknown:4`, a `grep` with two `;`-separated paths) has zero bad components, so the two readings coincide here. The divergence is unexercised and therefore untested in this slice.
Remedy (smallest, in-scope): none required for C3 in this slice; note the semantics of `rough_path_count` (components, not events) in the ledger's schema/prose so downstream counts against the declared rough 25 / lane 23 are not mixed.

### F5 — Informational: this slice contributes **zero** to the declared rough-vs-lane gap. Rough path events here = 4 (rows OracleWriteOther:7, OracleWriteOther:8, OracleWritePrefix:3, OracleParallelFetch:4); canonical path events here = the same 4. All 39 dispositions are `agree`. Therefore the preregister's rough build 25 vs lane build 23 gap (and falsify 33 vs 29) cannot originate in group 4; it must be explained by other groups. The only in-slice structural candidate for a count mechanism is the `call_id` collision noted below, and it is arithmetically inert here.

### F6 — Informational: `call_id` granularity is the one structural candidate for a rough/lane divergence. OracleWritePrefix rows :2, :3 and :4 all carry `call_id = toolu_01Q51bu1WSATPapAWZXEUhiv` (the last two are marked `origin: "additional-recorded-start"` in the pack and have no `digest_format` field). The slice keys rows by `call_id` **plus** `request_arguments_sha256`, so it emits 3 rows where a `call_id`-keyed auditor would emit 1. Collapsing them changes no path count (only row :3 carries a path violation), so no recorded value in this slice is falsified — but the granularity choice is undeclared in the slice and is the kind of thing that could produce a 2-event gap elsewhere.
Remedy (smallest, in-scope): declare the row key (per-request vs per-`call_id`) in the slice schema/prose so that any rough/lane arithmetic elsewhere is anchored.

## Residual risk

* R1 — **Pack-relative exhaustiveness.** Every row I confirmed is confirmed *relative to `packs/build-04.json`*. If the pack's capture dropped r22 requests, the slice would be internally perfect and externally incomplete (see F2). The preregister's `limits` already bar any recorder-completeness claim, so this is not a C3 violation — but C3's "exhaustive per-event explanation" must be read as "of the captured events".
* R2 — **Canonical side not re-derivable in isolation.** I re-derived the canonical side from *literal v1 authority + the S085 selector grammar*, which is what the assignment names. The landed lane implementation (`tools/check-path-reconciliation.py`, the canonical authority for `canonical_bad`) is outside this seat's declared read paths, so I could not read it; where my derivation and the recorded value agree, that is agreement with the *stated rule*, not a byte-level confirmation of the landed tool's rule. If the landed lane used a different selector grammar (e.g. not stripping `:raw` for `read`), rows OracleUnknownTool:1, OracleUnknownTool:2 and OracleWritePrefix:3 would flip to canonical_bad [0] and OracleUnknownTool:1/2 to a rough/lane divergence. The recorded values are consistent with the stated rule, which is the best available check here.
* R3 — **Aggregate gap unexplained by this slice.** The rough 25 / lane 23 (build) and 33 / 29 (falsify) gaps are outside group 4; this seat can neither confirm nor deny the claimed C3 target `unexplained_cohorts = 0` overall, only that group 4 contributes 0 unexplained events.
* R4 — **"agree" semantics are not defined in the slice.** I read `disposition` as *the rough side and the canonical side agree on the path-violation outcome for this row*. If the landed meaning were instead "the lane agrees with the recorded rough value", the two `edit` rows (rough `unknown`) would still be `agree`, so this seat's conclusions hold under either reading; but the ambiguity is what F1/F3 are about.

## Verification gaps

* The landed canonical classifier source and the ledger's generator were not readable within this seat's declared paths; canonical values were re-derived from the stated rule, not from the landed implementation (R2).
* The r22 transcript backing the pack (named in `sources/r22-rough-census.txt` as the CloseKaidoku22 session) is outside the declared read paths; pack-vs-transcript completeness is unverified (R1, F2).
* The falsify-side cohort (rough 33 vs lane 29) is not in this pack and was not examined.
* No execution was performed: no hashing, counting, listing, importing, compiling or testing of any artifact. Every statement above is a by-hand comparison of strings and literals present in the two declared JSON files plus the S085 source cell and the preregistration.

## Smallest in-scope remedy (consolidated)

One schema clarification plus one seat row, in `candidate/ledger-slices/*.json` and the ledger's schema/prose: (a) add `canonical_category` (and, for `edit` rows, the C1 decision outcome such as `OPAQUE_PATCH/UNKNOWN` or `WRITE_ONLY_EDIT/DENY`) so `canonical_bad: []` is never read as permission and `disposition` is checkable by inspection (F1, F3); (b) emit an explicit `no-events` row for `OracleWriteReport` and a per-seat `event_count` so an empty seat is declared rather than absent (F2); (c) state the row key (per-request vs per-`call_id`) and the component-vs-event semantics of `rough_path_count` (F4, F6). No recorded row value in this slice changes under these remedies, and no C1/C2/C3 metric target needs restating.

Reviewed-SHA256: 08d8ebbb0aa59f18a913dee9cf3b997130d4bc7672f72c48803a7760dbb890e8
Predicate: r23f-fxc3build04
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
