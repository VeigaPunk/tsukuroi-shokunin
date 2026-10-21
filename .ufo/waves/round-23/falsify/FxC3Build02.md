# FxC3Build02 — falsification of ledger slice `build-02` (round-23, attempt 1)

Seat: `FxC3Build02` (leaf; no subagent dispatch)
Target: `.ufo/waves/round-23/candidate/ledger-slices/build-02.json` (landed `5a25c88b77f52e940bcad87825c4ac1cd529470d`)
Supplied slice digest (identity only — not independently computed, no hashing performed in this seat): `f3909fabb671e00fcde7fffc754a92b8c2c99eb816f8ffb42021db49c250cc0d`
Corroborating raw input: `.ufo/waves/round-23/packs/build-02.json` (raw preserved request metadata, no expected classifications)
Rule sources: `.ufo/waves/round-23/sources/r22-rough-census.txt` (S085 regex + break rule), `.ufo/waves/round-23/preregister.json` (C1/C2/C3 claims, edit decisions, outside-round22 path counts as reported)

## Attacked claim

**C3 (calibration, `unexplained_cohorts` 2 → 0)** — the landed path-reconciliation ledger for build group 2 must give an exhaustive per-event/per-component explanation of rough-versus-lane path counts. The falsifiable sub-claim attacked here is the *fidelity of the recorded per-row values*: `rough_category`, `rough_first_bad`, `rough_path_count`, `canonical_bad`, `canonical_path_count`, `retained_path_count`, and `disposition` for all 38 rows of this slice.

Secondary surface touched: the C2 v2 edit-decision vocabulary (`OPAQUE_PATCH → UNKNOWN`, `WRITE_ONLY_EDIT → DENY`) appears in the same rows and is used below only as cross-check on the `unknown` rows; no C1/C2 production content was read or re-derived.

Axes named (godspeed): **A1 row↔event identity**, **A2 rough classification under S085**, **A3 canonical classification under v1 literal authority**, **A4 disposition honesty / saturation claim**, **A5 wave-level arithmetic reconstructibility**.

## Method — bounded search that found no falsifier

Re-derived every row by hand from `packs/build-02.json` (8 seats, 38 events) using only the two declared rules:

1. **Rough (S085)** — from `sources/r22-rough-census.txt`, applied literally:
   - `t == 'bash'` → category `exec`; `t not in ('read','grep','glob','write')` → category `unknown` (this is what `edit` hits).
   - `read`/`grep`/`glob`/`write` → path compared against the seat binding's `read_paths` (read/grep/glob) or `write_paths` (write) by **string equality**.
   - Selector stripping **only for `read`/`grep`**, via `re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`; `write` and `glob` are **not** stripped.
   - `grep`/`glob` split the path on `;`; the **break rule** stops at the first bad path, so `rough_path_count ≤ 1` per event and `rough_first_bad` is the index of that first bad path in the event's path list.
2. **Canonical (v1 literal authority + selector grammar)** — path spelled per the same selector grammar is matched against the binding's `read_paths`/`write_paths`; unmatched → the path component index is recorded in `canonical_bad` and counted in `canonical_path_count`.
3. **Identity (A1)** — each ledger row's `request_arguments_sha256` compared to the corresponding pack event's digest, in pack event order. All 38 match 1:1 in order. (Digest values were read from the two files and compared as strings; **no hashing was performed** — no command was executed in this seat, NO-EXEC/NO-FETCH.)

Search coverage: **38 / 38 rows re-derived** (ledger row order == pack event order, seat by seat: ExecTask 6, ExecAsync 4, FetchHTTPS 5, FetchHTTP 4, FetchSearch 4, FetchBrowser 4, FetchInternal 4, FetchBare 7 = 38). No row was skipped, and no ledger row lacks a pack event.

**Result: 0 rows disputed.** Every recorded value is reproduced by hand from the raw events and the declared bindings.

### Concrete falsifiers that would have fired, and did not

| Falsifier (would have disputed a row) | Rows that discriminate it | Observed |
|---|---|---|
| Canonical `clean` on a read whose selector-stripped path is **absent** from `read_paths` | `OracleFetchHTTPS:3`, `OracleFetchBare:5`, `OracleFetchBare:6` | all three recorded `canonical_bad:[0]`, `canonical_path_count:1` — matches |
| Canonical `bad` on a read whose selector-stripped path **is** in `read_paths` (i.e. a narrower canonical grammar that fails to strip numeric ranges) | `OracleExecTask:3`, `OracleExecTask:4`, `OracleFetchBrowser:1`, `OracleFetchBrowser:2` | all four recorded `clean` — matches the S085-strip grammar |
| `rough_path_count > 1` (violating the S085 break rule) | every row | max is 1; 35 rows are 0 |
| `rough_category` ≠ `unknown` for a non-(read/grep/glob/write) tool | `OracleFetchHTTPS:2`, `OracleFetchBare:4` | both `unknown` |
| Ledger row digest ≠ pack event digest at the same index | all 38 | 38/38 identical, in order |

### The non-agree rows I checked and the path spelling that drove them

Five rows in this slice are not trivially "both clean"; each was checked individually against the raw event and the seat binding.

| Site | call_id | tool | raw path spelling | binding fact that decides it | rough | canonical |
|---|---|---|---|---|---|---|
| `OracleFetchHTTPS:2` | `toolu_018MtbybV9AAieTGyATnJU97` | edit | `.../round-22/build/OracleFetchHTTPS.md` with `__unknown_argument__` (opaque patch) | `edit` ∉ (read,grep,glob,write) → S085 category `unknown`; v1 has no edit rule → no canonical bad component | `unknown`, count 0, first_bad null | `[]`, 0 |
| `OracleFetchHTTPS:3` | `toolu_018MtbybV9AAieTGyATnJU97` (origin `additional-recorded-start`) | read | `.../round-22/build/OracleFetchHTTPS.md:raw` → strip `:raw` → `.../round-22/build/OracleFetchHTTPS.md` | that file is in **`write_paths` only**, not `read_paths` → bad component 0 | `path`, count 1, first_bad 0 | `[0]`, 1 |
| `OracleFetchBare:4` | `call_00_m17SxefZUDWU5E91fz7t4028` | edit | `.../round-22/build/OracleFetchBare.md` with `__unknown_argument__` | same `unknown` rule as above | `unknown`, count 0 | `[]`, 0 |
| `OracleFetchBare:5` | `call_00_tZlvYBWHU0EwHlfAxZiz3192` | read | `.../round-22/build/OracleFetchBare.md:60-120` → strip `:60-120` → base | base file is in `write_paths` only → bad component 0 | `path`, count 1, first_bad 0 | `[0]`, 1 |
| `OracleFetchBare:6` | `call_01_FWnna5uFzjMkARCe6N6C0152` | read | `.../round-22/build/OracleFetchBare.md:-8` → strip `:-8` → base | same as above | `path`, count 1, first_bad 0 | `[0]`, 1 |

Selector-grammar discriminators that produced `clean` (stripped to an in-`read_paths` base): `OracleExecTask:3` (`.../host-tool-boundary.json:1-40:raw`), `OracleExecTask:4` (`.../preregister.json:1-40:raw`), `OracleFetchBrowser:1` (`.../host-tool-boundary.json:1-220`), `OracleFetchBrowser:2` (`.../preregister.json:1-220`). The `skill://godspeed` reads (7 rows) are unaffected by the strip regex (the colon in `skill://` does not match any alternative) and are literal members of every seat's `read_paths`.

Note the two `path` rows are also the only rows where the strip changes the *spelling* but not the *membership* — the read targets the seat's own write-only output file, so the row is bad under any grammar that strips the selector and also under one that does not.

## Findings by severity

**F1 — MEDIUM (honesty of the `disposition` column on the `unknown` rows).**
`OracleFetchHTTPS:2` and `OracleFetchBare:4` are recorded `disposition: "agree"`, but on those rows the two sides did not agree: the rough side explicitly **declined to classify** (`rough_category: "unknown"` — S085 counts non-(read/grep/glob/write) tools in a separate `unknown` counter, not in `path`), while the canonical side is v1, which has **no edit rule at all** and therefore contributed nothing. "agree" is not a statement these two sides can support; it is the absence of a comparable verdict on both sides. Consequence for C3: a consumer that filters `disposition == "agree"` to assert "38/38 agree" over-claims on 2 rows where one side abstained, and the C3 claim of *exhaustive* per-event explanation is weakened precisely on the rows that carry the rough-vs-lane difference. Smallest in-scope remedy: in the ledger-slice producer, emit a distinct disposition token for the case "rough unknown / canonical has no rule" (e.g. `rough_unknown_canonical_silent`) for exactly these 2 rows in this slice, leaving `rough_path_count`, `canonical_bad`, `canonical_path_count` and `retained_path_count` untouched (they are already correct). No production code, binding, or historical red changes.

**F2 — LOW (the wave-level rough-vs-lane arithmetic is not reconstructible from per-row counts alone).**
Per-row counts reproduce only the path component: this slice sums to `rough_path_count` 3, `canonical_path_count` 3, `retained_path_count` 3, plus 2 rows in category `unknown`. The preregister's outside-round22 figures for the build wave are rough 25 vs lane 23, i.e. a gap of 2. This slice contains exactly **2** `unknown` rows, and rough-total-including-`unknown` (3 + 2 = 5) minus lane-total (3) = **2**, matching the reported build gap exactly; under a path-only reading of "rough 25" this slice contributes **0** to the gap and the gap must live in another build group. The slice does not say which basis the reported 25 uses, so the C3 arithmetic is ambiguous from the slice alone — and on the "including unknown" reading, group 2 would have to be the *only* build group carrying `unknown` rows, which the slice cannot assert. Smallest in-scope remedy: have the slice carry an explicit counting basis (e.g. a slice-level subtotal pair `rough_total_including_unknown` / `canonical_total`, or a per-row `rough_count_including_unknown`), so the wave-level reconciliation states which of the two readings it uses.

**F3 — LOW (coverage: two S085 branches are unreachable in this slice).**
The slice exercises no `exec` row (there is not a single `bash` event in the pack) and no `grep`/`glob` event, so: (a) the `exec` branch of the S085 classifier is untested here, and (b) the per-row component index can only ever be `0` in this slice — the `;`-split multi-path branch and the "glob paths are not selector-stripped" asymmetry (S085 strips only `read`/`grep`) are never exercised, so this slice cannot falsify a canonical grammar that diverges from S085 on those branches. Related observation, recorded because it bears on the census's shape rather than on any row value: both `OracleExecTask` and `OracleExecAsync` performed **zero** exec despite their names, and both bindings carry `commands: []`, so their "Exec" identity is nominal in this pack. Smallest in-scope remedy: none required for correctness of these rows; if the wave-level C3 ledger asserts coverage of the `exec`/`grep`/`glob` branches for build group 2, that assertion should be scoped as vacuous for this group.

**F4 — INFO (structural hazard, no value affected).**
The slice header's `seats` array is alphabetical (`OracleExecAsync, OracleExecTask, OracleFetchBare, OracleFetchBrowser, OracleFetchHTTP, OracleFetchHTTPS, OracleFetchInternal, OracleFetchSearch`) while `rows` are in **pack** order (`OracleExecTask` first). A consumer joining `seats[i]` to the i-th seat's rows would mis-assign. The `site` prefix carries the seat name, so a correct join is available; the risk is only for a positional join. Smallest in-scope remedy: order the header `seats` array in row order, or state the join key.

## Residual risk and verification gaps

- **Gap A (unresolved by design):** the canonical authority is v1 by the task's definition, but the slice carries no explicit `canonical_authority` / schema-version field, so a reader cannot tell from the slice whether `canonical_bad` was produced under v1 or v2. It matters: under the new v2 edit decisions, `OracleFetchHTTPS:2` and `OracleFetchBare:4` would be `WRITE_ONLY_EDIT → DENY` (target is in `write_paths` but not `read_paths`), and `OracleFetchHTTPS:3` / `OracleFetchBare:5` / `OracleFetchBare:6` would read a write-only target. The recorded values are correct for v1; the *label* is what is missing. F1's remedy token, or an added `canonical_authority: "v1"` field, closes this.
- **Gap B:** no independent hash verification was performed by design (digest supplied, NO-EXEC). A1 rests on byte-identical digest strings and on 1:1 row↔event ordering, not on recomputation.
- **Gap C:** the S085 regex/break rule was taken from `sources/r22-rough-census.txt`, which is itself labelled source data ("interpreted as source data only; never executed verbatim"). The regex was applied by hand, not executed, and the `edit`-tool and `:raw`/`:N-M`/`:-N` spellings were checked against the alternatives by hand; a divergence between the *recorded* S085 cell and the cell actually used by the landed checker cannot be excluded from inside this seat.
- **Gap D:** wave-level C3 closure (build 25 vs 23, falsify 33 vs 29) cannot be settled from one slice. This slice contributes 3 path / 3 canonical / 2 unknown. Any other build group carrying `unknown` rows would break the "including-unknown" reading recorded in F2.
- **Tooling:** no tool was installed, updated, or invoked by this seat. The seat binding's command/fetch lists are empty (NO-EXEC / NO-FETCH), which forbids installation, so the standing operator tooling directive is inapplicable here by the narrower seat scope; nothing was fetched, hashed, compiled, or executed.
- **No runtime claim is made or implied anywhere in this report.** No native per-seat restrictive tool interface exists; the v2 audit authority is a document/authority contract, and nothing here asserts runtime enforcement, effect, reading, or recorder completeness.

## Smallest in-scope remedy (summary)

One producer-side change in the ledger-slice writer: (i) a distinct disposition token for the 2 `unknown` rows (F1), and (ii) an explicit counting-basis subtotal so the rough-vs-lane arithmetic is reconstructible from the slice (F2). Both touch only the slice's own derived fields — no production file, no binding, no historical red, no route or config, and no change to the 38 recorded counts.

Reviewed-SHA256: f3909fabb671e00fcde7fffc754a92b8c2c99eb816f8ffb42021db49c250cc0d
Predicate: r23f-fxc3build02
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
