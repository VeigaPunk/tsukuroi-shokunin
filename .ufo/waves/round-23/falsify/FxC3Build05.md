# FxC3Build05 — falsify C3 path-census ledger (pack build-05)

Seat FxC3Build05, leaf. Root `SC = /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Landed `5a25c88b77f52e940bcad87825c4ac1cd529470d`; baseline `ae01e50f582016384e620022be38bf5367000e2e`.
Slice `.ufo/waves/round-23/candidate/ledger-slices/build-05.json`, declared SHA256
`1045164a9fbda9e3655fbe6355934c918cd750fe0df919d2d064de0d309bd360` — taken as supplied
identity, **not** recomputed (NO-EXEC). No tool installed or updated (host transactions paused).

## 1. Attacked claim

Primary: **C3** (axis calibration; `unexplained_cohorts` 2 → 0; "Both fixed r22 cohorts have
exhaustive per-event/component explanation of rough-versus-lane path counts, frozen digests and
declared arithmetic"). This seat attacks the group-5 slice of that ledger against the raw pack.

Secondary interfaces carried by the same events: **C1** (this slice contains the cohort's only
`edit` event and its opaque argument shape) and **C2** (no v2 manifest and no v2-captured events
exist in scope, so C2's structured-edit-mode increment is untested here).

Frontier result in §9: group 5 contributes **0** of the build cohort's reported 2-unit
rough→lane gap; the remaining −2 is pinned outside this pack.

## 2. Rule set used (all in scope, read only)

Rough census = S085 exactly as preserved in `sources/r22-rough-census.txt`:

- `tool == 'bash'` → `exec`; `tool ∉ {read,grep,glob,write}` → `unknown`; both consume the event
  before any path work (`continue`).
- components = `path.split(';')` only for `grep`/`glob`; otherwise `[path]`.
- `q = strip_sel(v)` for `read` and `grep` only, with
  `strip_sel(p) = re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`.
- `write` compares `v` against `write_paths`; every other accepted tool compares `q` against
  `read_paths`.
- **Break rule**: the first component not in the literal list increments the path counter by 1
  and `break`s the component loop — at most one increment per event; later components unexamined.
  Order of gates is exec → unknown → path.

Canonical / literal-v1 rule applied by hand: same component enumeration; a component is bad iff
it is **literally** unequal to every entry of the binding list for its direction
(`write`→`write_paths`; `read`/`grep`/`glob`→`read_paths`); selector suffix stripped once by the
same grammar; no case folding, no `.`/`..` or symlink resolution, no re-rooting, no trailing-slash
normalisation. `edit` has no v1 path class: every r22 binding in this pack declares only
`read_paths`, `write_paths`, `commands`, `fetches`. Only `args.path` is a component; `args.content`
(including `content: null`) and `args.i` (`null` throughout) contribute nothing.

Disposition re-derived as: row agrees iff the recorded rough category / first-bad / count, the
canonical bad set / count, and the event identity all reproduce from the pack.

## 3. Identity and inventory

**[OBS]** `packs/build-05.json` holds 8 seats / 39 events; `ledger-slices/build-05.json` holds the
same 8 seats / 39 rows in pack order (Local 7, Malformed 6, Missing 5, Incomplete 5, Duplicate 4,
Unknown 4, Empty 4, BadArgs 4). For all 39 rows the `site`, `tool`, `call_id` and
`request_arguments_sha256` equal the pack event at the same seat:index, including the triplicated
call id `toolu_01JkHbts7HMkWNYEvbXS1NjJ` (Missing :2 `edit`, :3 `read`, :4 `write`).

Tool mix: 29 `read`, 9 `write`, 1 `edit`; 0 `bash`, 0 `grep`, 0 `glob`, 0 fetch. Every seat
declares the identical read authority:

- `R1` = `SC/.ufo/waves/round-22/sources/host-tool-boundary.json`
- `R2` = `SC/.ufo/waves/round-22/preregister.json`
- `R3` = `skill://godspeed`

and exactly one write target `W1` = `SC/.ufo/waves/round-22/build/<Seat>.md`.

## 4. Re-derivation — all 39 rows

`path` below is the recorded spelling relative to `SC/.ufo/waves/round-22/`; `→` is the stripped
component. `rough` = category(first-bad). `canon` = canonical bad indices / count.

### OracleParallelLocal (`W1` = build/OracleParallelLocal.md)

| idx | tool | call_id | path → stripped | authority | rough | canon |
|---|---|---|---|---|---|---|
| 0 | read | call_00_ET_zvjKEI2fBq5409p3LmVv0571 | `skill://godspeed` | R3 | clean(null) | [] / 0 |
| 1 | read | call_01_ET_FuwjBSXISzZPrV6lJH021607 | `sources/host-tool-boundary.json` | R1 | clean(null) | [] / 0 |
| 2 | read | call_00_SjNIGzT3rKLd9CBRdIP00226 | `preregister.json` | R2 | clean(null) | [] / 0 |
| 3 | read | call_00_62N1RQ7QVIkbaF4hOZI92448 | `sources/host-tool-boundary.json:1-20:raw` → `sources/host-tool-boundary.json` | R1 | clean(null) | [] / 0 |
| 4 | read | call_01_EV6jlNlPMsroMjsnc45l5081 | `preregister.json:1-30:raw` → `preregister.json` | R2 | clean(null) | [] / 0 |
| 5 | write | call_00_V3DxNzneS6ShA7MtMqx56924 | `build/OracleParallelLocal.md` | W1 | clean(null) | [] / 0 |
| 6 | read | call_00_jzklheuqzGfyYiaMhp4N3833 | `build/OracleParallelLocal.md:-6:raw` → `build/OracleParallelLocal.md` | none (W1 is not read authority) | path(0) | [0] / 1 |

### OracleParallelMalformed (`W1` = build/OracleParallelMalformed.md)

| idx | tool | call_id | path → stripped | authority | rough | canon |
|---|---|---|---|---|---|---|
| 0 | read | call_added95fdfd740b1bd90b90279758121\|fc_02fd96881f8817c0016ad8d05e4b90819193abcf5bfe5984ee | `skill://godspeed` | R3 | clean(null) | [] / 0 |
| 1 | read | call_05a03b1ac80e494e94343112ad241dbc\|fc_02fd96881f8817c0016ad8d05e5f588191b83037b286356f3e | `/home/vgpnk/Projects/shokunin/tsukuroi-shokurin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json` | none | path(0) | [0] / 1 |
| 2 | read | call_cd8167d09a8d45ad8d188a36462a8b35\|fc_02fd96881f8817c0016ad8d05e5f588191ae8487a99b8955b1 | `/home/vgpnk/Projects/shokuroi/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json` | none | path(0) | [0] / 1 |
| 3 | read | call_6cb5dc9a49d949099209902032429db9\|fc_02fd96881f8817c0016ad8d06288dc81919b341e91d5f8cac5 | `sources/host-tool-boundary.json` | R1 | clean(null) | [] / 0 |
| 4 | read | call_eb98a3d59638422fbc9c0dfebaafd860\|fc_02fd96881f8817c0016ad8d06299d08191b01d44a4404ac929 | `preregister.json` | R2 | clean(null) | [] / 0 |
| 5 | write | call_65eaf9aec4364094933a1b00aa14a1cd\|fc_02fd96881f8817c0016ad8d08a871081919dde63500ea0dfdc | `build/OracleParallelMalformed.md` | W1 | clean(null) | [] / 0 |

### OracleTraceMissing (`W1` = build/OracleTraceMissing.md)

| idx | tool | call_id | path → stripped | authority | rough | canon |
|---|---|---|---|---|---|---|
| 0 | read | toolu_01Xdhet2uzjfsVmGLj39kXDT | `sources/host-tool-boundary.json` | R1 | clean(null) | [] / 0 |
| 1 | read | toolu_016m7QbgEyoBc3N61EDxyD9o | `preregister.json` | R2 | clean(null) | [] / 0 |
| 2 | edit | toolu_01JkHbts7HMkWNYEvbXS1NjJ | `build/OracleTraceMissing.md` + `__unknown_argument__: null` | tool gate precedes paths | unknown(null) | [] / 0 |
| 3 | read | toolu_01JkHbts7HMkWNYEvbXS1NjJ | `build/OracleTraceMissing.md:raw` → `build/OracleTraceMissing.md` | none (W1 is not read authority) | path(0) | [0] / 1 |
| 4 | write | toolu_01JkHbts7HMkWNYEvbXS1NjJ | `build/OracleTraceMissing.md` | W1 | clean(null) | [] / 0 |

### OracleTraceIncomplete (`W1` = build/OracleTraceIncomplete.md)

| idx | tool | call_id | path → stripped | authority | rough | canon |
|---|---|---|---|---|---|---|
| 0 | read | call_b408e4f2f15a42ec9ccf9505 | `skill://godspeed` | R3 | clean(null) | [] / 0 |
| 1 | read | call_a89f465a11684823b1e528a9 | `sources/host-tool-boundary.json` | R1 | clean(null) | [] / 0 |
| 2 | read | call_58228fb65e644fb7b4a3de4a | `preregister.json` | R2 | clean(null) | [] / 0 |
| 3 | write | call_32a3dc42eebf47668b72b9c6e82c51b2\|fc_0d57c26e3adfebaf016ad8d0a0f2008191af8031b6619b9f78 | `build/OracleTraceIncomplete.md` | W1 | clean(null) | [] / 0 |
| 4 | write | call_f391194735914b7d9ee04b7fadc3217b\|fc_0d57c26e3adfebaf016ad8d0af427081918e3c14f1d2693d86 | `build/OracleTraceIncomplete.md` | W1 | clean(null) | [] / 0 |

### OracleTraceDuplicate (`W1` = build/OracleTraceDuplicate.md)

| idx | tool | call_id | path → stripped | authority | rough | canon |
|---|---|---|---|---|---|---|
| 0 | read | call_00_ET_ynROKxkTGVQwXdSVOciJ6743 | `sources/host-tool-boundary.json` | R1 | clean(null) | [] / 0 |
| 1 | read | call_01_ET_nNudDNMRmy2w90asAPv63374 | `skill://godspeed` | R3 | clean(null) | [] / 0 |
| 2 | read | call_00_6ZBsRQPVOyRemGmFahwO5526 | `preregister.json` | R2 | clean(null) | [] / 0 |
| 3 | write | call_00_Tg1ESIhGXYWzDowt6G2y6724 | `build/OracleTraceDuplicate.md` | W1 | clean(null) | [] / 0 |

### OracleTraceUnknown (`W1` = build/OracleTraceUnknown.md)

| idx | tool | call_id | path → stripped | authority | rough | canon |
|---|---|---|---|---|---|---|
| 0 | read | call_9764f509b4944526ab8c0c37579a7762\|fc_0b9e0659220c8cb8016ad8cf0fe7688191a727aade85e872bc | `skill://godspeed` | R3 | clean(null) | [] / 0 |
| 1 | read | call_06dc41992b2d40728dca132ad9297984\|fc_0b9e0659220c8cb8016ad8cf118388819189ec899a1926e62d | `sources/host-tool-boundary.json:1-180` → `sources/host-tool-boundary.json` | R1 | clean(null) | [] / 0 |
| 2 | read | call_25d0f9f9c3b24ca09ef95796f8ec8637\|fc_0b9e0659220c8cb8016ad8cf11838881919c0a58b3dc92bf15 | `preregister.json:1-180` → `preregister.json` | R2 | clean(null) | [] / 0 |
| 3 | write | call_22a71dcccb17407c80cf32cd058fb679\|fc_0b9e0659220c8cb8016ad8cf331bb4819197f1bc30490fe1bf | `build/OracleTraceUnknown.md` | W1 | clean(null) | [] / 0 |

### OracleTraceEmpty (`W1` = build/OracleTraceEmpty.md)

| idx | tool | call_id | path → stripped | authority | rough | canon |
|---|---|---|---|---|---|---|
| 0 | read | call_a6e6e2d281b64ca49bad8499 | `skill://godspeed` | R3 | clean(null) | [] / 0 |
| 1 | read | call_e63a6ce3e5414ffa9ff23c3a | `sources/host-tool-boundary.json` | R1 | clean(null) | [] / 0 |
| 2 | read | call_dd0db2fabd6449f7b82868bd | `preregister.json` | R2 | clean(null) | [] / 0 |
| 3 | write | call_99b5d4fa12604985a647c623 | `build/OracleTraceEmpty.md` | W1 | clean(null) | [] / 0 |

### OracleTraceBadArgs (`W1` = build/OracleTraceBadArgs.md)

| idx | tool | call_id | path → stripped | authority | rough | canon |
|---|---|---|---|---|---|---|
| 0 | read | call_00_ET_Ey9JjpBEvMEWtiPAneUC7511 | `sources/host-tool-boundary.json` | R1 | clean(null) | [] / 0 |
| 1 | read | call_01_ET_N8B3CzzXWSGv0p1Mcztg5765 | `preregister.json` | R2 | clean(null) | [] / 0 |
| 2 | read | call_02_ET_WZ8AP2iFSKDFZvfq4ipI4653 | `skill://godspeed` | R3 | clean(null) | [] / 0 |
| 3 | write | call_00_QCnQbgQqUdKMaCyyOq0O1011 | `build/OracleTraceBadArgs.md` | W1 | clean(null) | [] / 0 |

## 5. The five non-clean rows (full call_id + exact driving spelling)

**[OBS]** All four path rows are `read`s. Two are self-readbacks of a write-only target, two are
misspelled-parent reads. One row is the tool-gate residual (the sole `edit`).

1. **OracleParallelLocal index 6**, `call_00_jzklheuqzGfyYiaMhp4N3833` —
   `SC/.ufo/waves/round-22/build/OracleParallelLocal.md:-6:raw`. `strip_sel` removes `:-6:raw`
   (third + optional second alternative), leaving the write-only report path; the read list has
   only `R1,R2,R3` → rough `path`, first bad 0; canonical `[0]`/1. Recorded values reproduce.
2. **OracleParallelMalformed index 1**, `call_05a03b1ac80e494e94343112ad241dbc|fc_02fd96881f8817c0016ad8d05e5f588191b83037b286356f3e` —
   `SC` with a fabricated extra segment: `/home/vgpnk/Projects/shokunin/tsukuroi-shokurin/tsukuroi-shokunin/.ufo/waves/round-22/sources/host-tool-boundary.json`
   (`tsukuroi-shokurin/` inserted). No selector, no `;`; literal inequality → `path(0)`, `[0]`/1.
3. **OracleParallelMalformed index 2**, `call_cd8167d09a8d45ad8d188a36462a8b35|fc_02fd96881f8817c0016ad8d05e5f588191ae8487a99b8955b1` —
   `/home/vgpnk/Projects/shokuroi/tsukuroi-shokunin/.ufo/waves/round-22/preregister.json`
   (`shokuroi` transposition in the parent). Literal inequality → `path(0)`, `[0]`/1.
4. **OracleTraceMissing index 2**, `toolu_01JkHbts7HMkWNYEvbXS1NjJ` — `edit` of
   `SC/.ufo/waves/round-22/build/OracleTraceMissing.md` with args
   `{path, __unknown_argument__: null}`. `edit` is outside the four accepted tools, so the S085
   gate yields `unknown` before any component exists: first-bad `null`, rough count 0; canonical
   has no v1 edit class → `[]`/0. The recorded `unknown` is the **tool-gate** sense, not C1's
   `OPAQUE_PATCH`.
5. **OracleTraceMissing index 3**, same `call_id` — `SC/.ufo/waves/round-22/build/OracleTraceMissing.md:raw`;
   `strip_sel` removes `:raw`, leaving a write-only target → `path(0)`, `[0]`/1.

## 6. Disputes

**None.** 0 of 39 rows disputed. My hand re-derivation reproduces, for every row: `tool`,
`call_id`, `request_arguments_sha256`, `rough_category`, `rough_first_bad`, `rough_path_count`,
`canonical_bad`, `canonical_path_count`, `disposition`.

No row carries a disposition other than `agree`, so there is no non-agree row to list; the five
rows in §5 are the only rows where a spelling or the tool gate drives a non-clean classification,
and their exact spellings are given there.

**[OBS]** `canonical_path_count == len(canonical_bad)` in all 39 rows, and
`disposition == "agree"` in exactly those rows where `rough_path_count == canonical_path_count`
(all 39). The disposition column therefore adds no adjudication independent of the counts in this
slice; the `edit` row's `agree` means "0 rough path units = 0 canonical units", not an edit-authority
verdict.

**[GAP]** `retained_path_count` has no definition in any file in this seat's scope. Its values are
1 only at Local:6 and Missing:3 and 0 elsewhere — i.e. it equals `canonical_path_count` on every
row. If it instead meant "path components retained in the recorded adapter trace", all 39 events
carry an `args.path` and the value would be 1 everywhere, differing on 37 rows. I do not record
those 37 as disputes because the ledger is self-consistent under the narrower reading and no
declared source fixes the field's meaning; §11 recommends the one-sentence fix.

## 7. Conditional dependencies — where a different rule would have flipped a row

These are the only places in this slice where the recorded ledger depends on a rule choice; all
were checked and the ledger's choice is the S085-preserved grammar.

- **Numeric-range selector stripping (4 rows).** Local:3 `:1-20:raw`, Local:4 `:1-30:raw`,
  Unknown:1 `:1-180`, Unknown:2 `:1-180`. A grammar stripping only `:raw` would leave
  `…json:1-180` and flip these to canonical-bad (4 phantom disagreements). The S085 regex
  (`\d[\d\-+,:]*` includes `:` and `-`) strips them in one substitution; ledger canonical 0 is
  correct under it. `:-6:raw` and `:raw` are robust: either stripping path leaves the bare report
  path, still outside read authority.
- **Self-readback authorisation (2 rows).** Local:6 and Missing:3 are clean only if write
  authority implies read authority; literal v1 says it does not (read list is separate), so both
  are bad, matching the ledger. *(C1's `WRITE_ONLY_EDIT` — "Edit also needs its explicit target
  read authority" — points the same way, but it is r23 content and is **not** used as v1
  authority here.)*
- **Call-id dedup (1 row).** Collapsing `toolu_01JkHbts7HMkWNYEvbXS1NjJ` to one row would delete
  the `read` at Missing:3 and move the pack total from 4 to 3. The ledger keeps all three rows,
  which is `EXPANSION`/`CHECK_EACH` behaviour, not per-call aggregation.
- **`retained_path_count` meaning (§6).** Would affect values on 37 rows, no arithmetic.

## 8. C1 / C2 interface from this slice

**[OBS]** The cohort's only `edit` (Missing:2) has a *present* structured target **and** an
unrecognised sibling key `__unknown_argument__`. Under the literal r22 authority lists there is no
`edit_paths` at all, and the target is write-declared only.

- Against C1's eight decisions, three rows are plausibly triggered: `UNDECLARED_EDIT` (nothing is
  predeclared for edit), `WRITE_ONLY_EDIT` (target is in `write_paths`, not `read_paths`), and
  `OPAQUE_PATCH` (whose rationale is worded for a **missing** structured target / opaque patch
  text — this request's target is present, so the wording does not match). Two of the three yield
  `DENY`, one yields `UNKNOWN`. The preregister states no precedence between decision rows and no
  fallback for shapes outside the eight. A request-first evaluator returns `UNKNOWN`; an
  authority-first evaluator returns `DENY`.
  **[INF]** This is a wording/exhaustiveness gap in C1's *finite* contract over the very observed
  structured-edit keys C1 cites as source S086 — not a numeric conflict, and not a C3 falsifier,
  because the ledger deliberately does not adjudicate the edit (`[]`/0, consistent with C3's
  declared separability from C1/C2 content).
- **C2:** no v2 manifest and no captured v2 events are in scope, so the schema-v2 authority is
  untested here (bounded search: all 39 events are `read`/`write`/`edit`; zero `bash`, zero
  command, zero fetch). The one relevant constraint the slice confirms is negative: an edit
  request bearing an unmapped key produced no inferred path credit (0/0), matching the
  `OPAQUE_PATCH` rationale's refusal to infer a target from opaque content. No enforcement claim
  is made or supported by this slice.

## 9. Arithmetic and aggregate boundary

| seat | rough path | canonical bad | rough unknown | events |
|---|---|---|---|---|
| OracleParallelLocal | 1 | 1 | 0 | 7 |
| OracleParallelMalformed | 2 | 2 | 0 | 6 |
| OracleTraceMissing | 1 | 1 | 1 | 5 |
| OracleTraceIncomplete | 0 | 0 | 0 | 5 |
| OracleTraceDuplicate | 0 | 0 | 0 | 4 |
| OracleTraceUnknown | 0 | 0 | 0 | 4 |
| OracleTraceEmpty | 0 | 0 | 0 | 4 |
| OracleTraceBadArgs | 0 | 0 | 0 | 4 |
| **pack** | **4** | **4** | **1** | **39** |

Categories: clean 34, path 4, unknown 1, exec 0 — sums to 39.

**[OBS/INF]** Pack delta rough−canonical = **0**. The build cohort's reported rough 25 vs lane 23
(−2) therefore cannot be produced or excluded by group 5; it must live in rows of other packs,
in shapes absent here (no `grep`/`glob` `;` lists, no `bash`, no foreign write targets, no
selector the rough grammar fails to strip). The slice's own `scope` ("not a recomputation") is
consistent with this: the slice supplies the per-row material, not the aggregate. Group 5 is
cleared of suspicion; the remaining −2 is pinned elsewhere. This is the **bounded search that
found no C3 falsifier** in this pack.

## 10. Unresolved gaps

1. `retained_path_count` semantics (§6) — not defined in scope.
2. **Additional-recorded-start attribution.** Missing:3 (`read`) and :4 (`write`) both carry
   `request_line: null`, `origin: "additional-recorded-start"`, sharing a `call_id` with the
   `edit`. The ledger treats :3 as a distinct canonical-bad adapter step. **[INF]** Event-set
   asymmetry is unlikely because the S085 cell itself reads `{W}/{w}/events.json`, the same frozen
   event list, so the lane counter most likely sees the same events; the ledger's `[0]` is then
   right. If the lane counter instead excludes reconstructed starts, Missing:3 would be a
   misattribution worth −1 of the build −2. Not resolvable inside this seat's read scope.
3. C1 precedence/default for a request matching multiple decision rows (§8).
4. The `break` rule is observable only in its single-component form here: every event carries one
   component, so the per-event cap is confirmed as ≤1 but multi-component `;` truncation is
   unexercised.
5. Whether `disposition` is defined independently or derived from count equality — it correlates
   perfectly on all 39 rows (§6).

## 11. Smallest in-scope remedy

My only writable artifact is this report, so these are recommendations to L1; no row is rewritten
and no production change is implied.

1. Add one scope sentence to the slice (or schema) defining `retained_path_count` and citing
   `strip_sel` as the selector grammar. This makes the four numeric-range reads and the 1-vs-0
   retained values auditable without recovering S085. No recorded value changes.
2. Add one sentence to C1's scope fixing precedence, or a deny-by-default fallback, for an edit
   request that satisfies more than one decision row (here `OPAQUE_PATCH` vs `WRITE_ONLY_EDIT` vs
   `UNDECLARED_EDIT`). The eight decisions and C3 arithmetic are unchanged.
3. Keep Missing:3's canonical `[0]` on current evidence: it follows from literal v1 read authority
   and does not depend on the pack's transcription quirk.

## 12. Conclusion

C3 is **not falsified** by pack build-05. All 39 rows reproduce from the raw events and bindings
under the S085 regex, gate order and break rule, and under literal v1 authority with the preserved
selector grammar: 4 rough path units = 4 canonical bad components, 1 tool-gate `unknown`, 34 clean,
delta 0, zero disputes, zero identity drift against the pack. The only concrete falsifier
candidates found are conditional and outside this slice's arithmetic: the pack-level
`additional-recorded-start` attribution (shared `events.json` makes the ledger's choice the
better-grounded one) and an unstated `retained_path_count` definition that changes labels, not
counts.

Reviewed-SHA256: 1045164a9fbda9e3655fbe6355934c918cd750fe0df919d2d064de0d309bd360
Predicate: r23f-fxc3build05
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
