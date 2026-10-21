# FxC3Falsify02 — falsification of ledger slice `falsify-02` (C3, path-census ledger)

Seat: FxC3Falsify02 (leaf member, no subagent dispatch).
Wave: round-23, wave `falsify`, group 2. Landed state under review: `5a25c88b77f52e940bcad87825c4ac1cd529470d`.
Target slice: `.ufo/waves/round-23/candidate/ledger-slices/falsify-02.json` (declared SHA256 `73a265762770c8ca133bd2cea861cf396a84b3bb3a2edab981e8cd1d7ece8835` — supplied identity, **not** independently computed; no hash/list/wc/command was executed).
Frozen inputs actually opened: the slice itself, `.ufo/waves/round-23/packs/falsify-02.json`, `.ufo/waves/round-23/preregister.json`, `.ufo/waves/round-23/sources/r22-rough-census.txt`, `.ufo/waves/round-23/sources/godspeed-directive.txt`, `skill://godspeed`.
Execution scope: NO-EXEC / NO-FETCH. No command, hash, import, compile, test or network action was run. All derivations below are hand derivations from the opened JSON.

## 1. Attacked claim

**C3 (calibration, `unexplained_cohorts` 2 → 0)** as carried by this slice: "Both fixed r22 cohorts have exhaustive per-event/component explanation of rough-versus-lane path counts, frozen digests and declared arithmetic."
Sub-claim under attack: for every falsify-group-2 event, the landed row's `rough_category` / `rough_first_bad` / `rough_path_count` (exact S085 regex + break rule), `canonical_bad` / `canonical_path_count` (literal v1 authority + selector grammar), `retained_path_count`, `disposition`, and `request_arguments_sha256` are correct and mutually consistent.
C1 and C2 are **not** re-derived here: this pack is r22 falsify-wave evidence only; their own seats (`FxC1*`, `FxC2*` in the falsify wave) attack those claims. This seat's verdict touches C3 and the frontier row "path-census ledger is reconcilable".

## 2. Axes (godspeed naming)

- **A — Identity/bijection**: every ledger row ↔ exactly one pack event; `site`, `call_id`, digest agree; no row omitted, no row invented.
- **B — Rough fidelity**: per-event category and first-bad component re-derived by hand under the exact S085 regex `':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$'` and the S085 `break` rule (one `path` hit per event, first bad component only).
- **C — Canonical fidelity**: `canonical_bad` / `canonical_path_count` / `retained_path_count` re-derived under literal per-seat v1 authority (exact membership in the seat's own `read_paths` / `write_paths`) plus the selector grammar.
- **D — Disposition arithmetic**: `disposition` consistent with rough vs canonical counts; per-seat and slice-level sums consistent with the declared cohort totals.
- **E — Digest provenance**: whether `request_arguments_sha256` is re-derivable from the frozen evidence, and whether it matches the frozen source value.

## 3. Method (bounded, hand-derived)

1. Row↔event bijection: slice has 142 rows; pack `falsify-02` has 142 events over the same 8 seats (15+15+22+26+24+9+16+15). Every `site` index equals the pack event index; every `call_id` string is byte-identical between slice and pack for all 142 rows (including the compound `call_…|fc_…` form of `FxC2Eval`).
2. Digest equality: for all 142 rows the slice's `request_arguments_sha256` equals the pack event's own `request_arguments_sha256` (compared field-by-field over the full list, not sampled) — **142/142 match**.
3. Rough re-derivation: for each event I applied S085 literally — `bash` → exec; tool ∉ {read,grep,glob,write} → unknown; otherwise split `path` on `;` for grep/glob, strip the selector with the S085 regex for read/grep only (not for write), and test exact string membership in the seat's own `read_paths` (read/grep/glob) or `write_paths` (write), counting at most one hit per event and recording the first bad component index.
4. Canonical re-derivation: same component decomposition under the literal per-seat v1 authority and selector grammar, then `canonical_bad` = list of bad component indices, `canonical_path_count` = |canonical_bad|, `retained_path_count` = retained violations, `disposition` = agreement of rough vs canonical.

## 4. Per-seat result (all 142 rows re-derived)

| seat | rows | clean | path (rough=canonical) | unknown | rough_path_count Σ | canonical_path_count Σ | retained Σ | dispositions |
|---|---|---|---|---|---|---|---|---|
| FxC1Table | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 15 agree |
| FxC1Sources | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 15 agree |
| FxC1HostLimit | 22 | 20 | 2 | 0 | 2 | 2 | 2 | 22 agree |
| FxC1ReadFailure | 26 | 22 | 2 | 1 | 2 | 2 | 2 | 26 agree |
| FxC2Bash | 24 | 20 | 2 | 1 | 2 | 2 | 2 | 24 agree |
| FxC2Eval | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 9 agree |
| FxC2Child | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 16 agree |
| FxC2Http | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 15 agree |
| **total** | **142** | **134** | **6** | **2** | **6** | **6** | **6** | **142 agree** |

Category totals reproduce exactly: 134 clean + 6 path + 2 unknown = 142; every `canonical_bad` is `[]` or exactly `[0]`; `canonical_path_count` == `rough_path_count` == `retained_path_count` on every row; `disposition` is `agree` on every row (the slice's only disposition value — `unique` over the column = `["agree"]`).

## 5. Rows whose recorded value I dispute

**None.** Zero of 142 rows are disputed on `rough_category`, `rough_first_bad`, `rough_path_count`, `canonical_bad`, `canonical_path_count`, `retained_path_count`, `disposition`, `call_id` or `request_arguments_sha256`.

## 6. Non-agree rows checked, and the path spellings that drove them

There are **no** non-agree rows in this slice (every disposition is `agree`). For completeness, the rows whose classification is *not* the trivial "clean" verdict — i.e. the rows where a spelling decided the outcome — were checked individually as follows. Path spellings are reproduced verbatim from the pack (the `;`-joined multi-path strings are shown with their real separator).

**Path rows (6) — every one is a read/grep of the seat's own round-22 report file, which is in that seat's `write_paths` but absent from its `read_paths`; under literal v1 authority that is a read outside read authority, so component 0 is bad and the S085 break fires there:**

| site | index | tool | call_id | path spelling | rough | canonical |
|---|---|---|---|---|---|---|
| FxC1HostLimit | 20 | grep | `call_00_13jy2kj4bcch83a6v2segiuu` | `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxC1HostLimit.md` | path / first_bad 0 / count 1 | `[0]` / 1 / retained 1 |
| FxC1HostLimit | 21 | read | `call_01_2yynczmqgdfvw1xgq0fvhlqe` | `…/round-22/falsify/FxC1HostLimit.md:1-12` → S085-stripped to `…/FxC1HostLimit.md` | path / 0 / 1 | `[0]` / 1 / retained 1 |
| FxC1ReadFailure | 23 | grep | `call_00_vcUOc2oOA53F107WJh392123` | `…/round-22/falsify/FxC1ReadFailure.md` | path / 0 / 1 | `[0]` / 1 / retained 1 |
| FxC1ReadFailure | 25 | grep | `call_00_AerZ5CRSr0cL4zsTGTP06071` | `…/round-22/falsify/FxC1ReadFailure.md` | path / 0 / 1 | `[0]` / 1 / retained 1 |
| FxC2Bash | 21 | read | `toolu_01MsCzhA8H5kDJ6a3Sd4kcBu` | `…/round-22/falsify/FxC2Bash.md:74-80` → stripped to `…/FxC2Bash.md` | path / 0 / 1 | `[0]` / 1 / retained 1 |
| FxC2Bash | 23 | read | `toolu_014W2fHm4vLzYRxGb17mDz2U` | `…/round-22/falsify/FxC2Bash.md:88-98:raw` → S085 strips both `:88-98` and the trailing `:raw` → `…/FxC2Bash.md` | path / 0 / 1 | `[0]` / 1 / retained 1 |

**Unknown rows (2) — `edit` is not in the S085 tool set {read,grep,glob,write}, so the rule classifies by tool before it ever looks at a path; both rows are `unknown` with no path component, and the ledger did not invent one:**

| site | index | tool | call_id | path spelling | rough | canonical |
|---|---|---|---|---|---|---|
| FxC1ReadFailure | 24 | edit | `call_00_SwIeaJDd3RNwdCH6xyht3569` | `…/round-22/falsify/FxC1ReadFailure.md` (present in pack args) | unknown / null / 0 | `[]` / 0 / retained 0 |
| FxC2Bash | 22 | edit | `toolu_01MNphx6oshJdCfbNKYFYQor` | **no `path` key at all** in the pack args (`args` = `{i: null, __unknown_argument__: null}`) | unknown / null / 0 | `[]` / 0 / retained 0 |

**Multi-path grep rows (2) — the only rows whose canonical verdict depends on the selector/path-list grammar; both are clean because every component is in the seat's `read_paths`:**

| site | index | tool | call_id | path spelling | verdict |
|---|---|---|---|---|---|
| FxC1HostLimit | 10 | grep | `call_00_6an1ja4ufmxmuurmziud2wyy` | `…/tools/check-boundary-contract.py;…/corpus/knowledge/seat-boundary-r22.json;…/corpus/knowledge/seat-boundary-r22.md;…/sources/host-tool-boundary.json;…/round-22/preregister.json` | clean (5/5 components declared) |
| FxC2Http | 12 | grep | `toolu_01BpgP8DHHRMMMHUGF38Fnyt` | `…/tools/check-seat-bindings.py;…/tools/check-review-snapshots.py;…/tools/_revision.py;…/corpus/knowledge/seat-boundary-r22.json;…/corpus/knowledge/seat-boundary-r22.md;…/sources/host-tool-boundary.json;…/round-22/preregister.json` | clean (7/7 components declared) |

**Selector-stripping rows (hand-checked, all clean).** Every `read` carrying a selector was tested against the S085 regex by hand, including the two-alternative forms: `:1-240:raw`, `:16-30:raw`, `:55-100:raw`, `:88-98:raw`, `:100-175:raw`, `:98-192:raw`, `:121-300:raw`, `:181-241:raw`, `:154-241:raw`, `:95-156:raw`, `:59-100:raw`, `:1-130:raw`, `:1-120:raw`, `:1-60:raw`, `:1-40:raw`, `:60-100:raw`, `:1-240:raw`, `:36-56`, `:18-24`, `:44-104`, `:60-76`, `:84-100`, `:84-112`, `:86-101`, `:108-144`, `:116-124`, `:132-149`, `:134-150`, `:145-190`, `:150-175`, `:219-223`, `:74-80`, `:1-80`, `:16-34`, `:36-110`, `:110-160`, `:81-200`, `:39-140`, `:140-260`, `:1-160`, `:160-260`, `:80-160`, `:1-220`, `:1-180`, `:1-210`. In each case the greedy `\d[\d\-+,:]*` branch absorbs the numeric range and the optional `(:raw)?` absorbs a trailing `:raw` (backtracked one character at a time), leaving a path that is exactly a declared `read_paths` entry → clean. The `write` rows (`FxC1Table:14`, `FxC1Sources:14`, `FxC1HostLimit:19`, `FxC1ReadFailure:22`, `FxC2Bash:20`, `FxC2Eval:8`, `FxC2Child:15`, `FxC2Http:13`, `FxC2Http:14`) all target their seat's own `write_paths` entry verbatim with no selector (S085 does not strip selectors for `write`, so no strip case arises) → clean.

## 7. Cohort arithmetic check against the declared totals

`preregister.json → outside_round22.path_counts_as_reported` gives, for the r22 falsify wave, **rough 33 / lane 29**. This slice (group 2) contributes **rough 6 / canonical 6 / retained 6** — i.e. this slice contributes **zero** to the 4-row rough-vs-lane gap. The entire gap (group-1 rough 27 → group-1 lane 23) therefore lies outside this slice, and no cohort explanation is owed by group 2 beyond "all rows agree". The landed per-row dispositions are consistent with that arithmetic: if the canonical column had been *cleaner* than rough on this slice's six own-report reads (i.e. if write authority conferred read authority), group 2 would contribute canonical 0 and group 1 would have to supply lane 29 against rough 27 — lane exceeding rough — which contradicts the declared direction (lane 29 < rough 33) and the landed "agree" dispositions. The landed treatment of own-report reads as violations is therefore the only self-consistent reading of the declared totals, and it matches this corpus's own rule that read authority comes only from `read_paths` (cf. preregister `edit_decisions`: "READ_ONLY_EDIT DENY — Read authority never grants a write"; "WRITE_ONLY_EDIT DENY — Edit also needs its explicit target read authority").

## 8. Findings by severity (none is a wrong recorded value)

**F1 — Medium (verification gap, C3 wording "frozen digests"): `request_arguments_sha256` is not re-derivable from the frozen evidence.**
The pack's per-event `args` preserve the *key set* of the original request but set every non-`path` value to `null` (`i`, `pattern`, `content`, `old_string`/`new_string`, `__unknown_argument__`), while each event declares `digest_format: "sorted ensure_ascii JSON arguments; not raw JSONL bytes"`. The digest is therefore taken over argument values the pack no longer carries, and no independent party can recompute it from the slice's declared inputs — only copy it. Evidence: `.ufo/waves/round-23/packs/falsify-02.json` event objects (`args` shown with `i: null`, `pattern: null`, `content: null`, `__unknown_argument__: null`) and the ledger's own `request_arguments_sha256` column, which matches the pack value on **142/142** rows. Impact: the landed ledger is *faithful* to the frozen source (no wrong value), but C3's claim of "frozen digests" is not independently checkable from the pack for any row whose arguments carried a redacted value — which is 142 of 142. Smallest remedy: state in the reconciliation record that the digest column is *carried from* the pack event field and is copy-verifiable (equality) but not recomputable, and cite the pack's `digest_format` + redaction rule as the reason.

**F2 — Medium (verification gap, canonical grammar): the `canonical_*` columns of this slice depend on two v1 lane-grammar facts that are not reachable from this seat's declared read paths.**
The canonical authority source (`.ufo/waves/round-22/candidate/tools/check-seat-bindings.py` for the four C2 seats, `.ufo/waves/round-22/candidate/tools/check-boundary-contract.py` for the four C1 seats) is **not** in this seat's `read_paths`, and the wave contract forbids extra filesystem search, so I could not read the lane grammar directly. Two concrete, one-line falsifiers remain open and are decidable by L1 in seconds:
 (a) *Does the v1 lane split `;`-joined grep path lists?* If **no**, then rows `FxC1HostLimit:10` (call `call_00_6an1ja4ufmxmuurmziud2wyy`) and `FxC2Http:12` (call `toolu_01BpgP8DHHRMMMHUGF38Fnyt`) must carry `canonical_bad [0]`, `canonical_path_count 1` and a non-`agree` disposition; the slice records them as clean/`agree`. Evidence for the split semantics: the S085 rough cell itself splits on `;` (`vals=str(a.get('path','')).split(';') if t in('grep','glob') else [...]`), and the split is the only reading under which these two rows are clean. Evidence that the split is *not* merely assumed: the totals in §7 are consistent with either reading, so the counts do not settle it — only the lane source does.
 (b) *Does write authority confer read authority in v1?* If **yes**, then all six path rows in §6 must have `canonical_bad []`, `canonical_path_count 0`, `retained_path_count 0` and a non-`agree` disposition. The §7 arithmetic and the corpus's own read-authority rule both argue **no**; the lane source is the authority.
Both (a) and (b) are the *only* rows in this slice whose canonical verdict is grammar-sensitive; the other 134 rows are clean under any reading of (a)/(b) because their component paths are literally declared.

**F3 — Low (observation, C3 "exhaustive explanation" wording): the `unknown` bucket is rule-faithful but semantically empty.**
`FxC1ReadFailure:24` and `FxC2Bash:22` are `edit` events. Under S085 the tool test precedes the path test, so `edit` → `unknown` and the events contribute 0 to *both* the rough and the canonical path counts. The ledger records them faithfully (`unknown`, `rough_first_bad null`, `canonical_bad []`, counts 0, `retained 0`, `agree`). But the underlying r22 divergences are real: `FxC1ReadFailure:24` edits a file that is in that seat's `write_paths` and *not* in its `read_paths` (a write-only target), and `FxC2Bash:22` has no recoverable target path at all in the pack (its `path` key is absent; only `__unknown_argument__: null` survives). For C3's "exhaustive per-event/component explanation" to be literally exhaustive, the reconciliation record must explain the two `unknown` rows as *"tool class `edit` has no v1 authority class, so no component is scored"* and not as "no violation". Cross-link to this round's own contract: the r23 `edit_decisions` name the same two shapes — `OPAQUE_PATCH → UNKNOWN` ("Missing structured target is not inferred from opaque patch text", matching `FxC2Bash:22`) and `WRITE_ONLY_EDIT → DENY` ("Edit also needs its explicit target read authority", matching `FxC1ReadFailure:24`'s shape). No r23 v2 conclusion is transferred onto r22 rows; this is a wording-alignment observation only.

**F4 — Low (cosmetic):** the slice's `seats` array is alphabetically sorted (`FxC1HostLimit, FxC1ReadFailure, FxC1Sources, FxC1Table, FxC2Bash, FxC2Child, FxC2Eval, FxC2Http`) while `rows` follow pack order (`FxC1Table, FxC1Sources, FxC1HostLimit, FxC1ReadFailure, FxC2Bash, FxC2Eval, FxC2Child, FxC2Http`). Both orders are internally complete and self-consistent; no row is mis-attributed because every row carries an explicit `site` string and a `call_id` that matches the pack. No change needed.

## 9. Attacked claim, falsifier, bounded search, smallest remedy

- **Attacked claim**: C3 — "Both fixed r22 cohorts have exhaustive per-event/component explanation of rough-versus-lane path counts, frozen digests and declared arithmetic", as instantiated by the 142 rows of `falsify-02`.
- **Falsifier attempted**: for each row, reconstruct the rough category/first-bad component from the raw pack event and the seat's own binding under the exact S085 regex and break rule, then reconstruct the canonical component set under literal v1 authority and the selector grammar, and check the disposition arithmetic and digest equality. A falsifier would be any row where the re-derived value differs from the landed value, or any pack event without a row, or any row without a pack event, or any digest mismatch.
- **Bounded search result**: 142/142 rows re-derived, 142/142 pack events consumed, 142/142 call_ids and 142/142 digests matched, 0 rows disputed. The search covered the entire slice (the slice *is* the bounded search space — no sampling). The two remaining falsifiers (F2a, F2b) are one-line reads of the r22 lane tools, which this seat is not permitted to read.
- **Smallest in-scope remedy** (no production change, no new claim, no VCS/index/ref action): L1 adds two lines to the C3 reconciliation record, citing the r22 lane-tool lines: (i) the v1 lane splits `;`-joined grep path lists (or does not) — resolving `FxC1HostLimit:10` and `FxC2Http:12`; (ii) v1 write authority does not confer read authority (or does) — resolving the six own-report path rows. Plus one provenance line stating that `request_arguments_sha256` is carried from the pack event field and is equality-verifiable but not recomputable because the pack redacts non-`path` argument values (F1), and one wording line stating that the two `unknown` rows are explained by tool-class absence, not by absence of divergence (F3). If (i) or (ii) resolves against the landed values, the affected rows' `canonical_bad`/`canonical_path_count`/`disposition` in this slice are the only cells that change; no other row in the slice is sensitive to either fact.

## 10. Residual risk and verification gaps

1. **F2 is unresolved by design of this seat's scope.** My canonical verification is by internal consistency (canonical mirrors the rough component decomposition under the literal per-seat binding, which the landed totals and the corpus's read-authority rule both support) and not by direct reading of the v1 lane grammar. The 8 grammar-sensitive rows are enumerated above so L1 can settle them in one read each.
2. **Group-1 falsify slice not inspected** (not in my `read_paths`). The whole rough 33 → lane 29 falsify gap lives there (group-1 rough 27 → lane 23). This seat's verdict does not cover it; a `FxC3Falsify01` sibling (or equivalent) must carry it. No claim is made here about group 1.
3. **Digest recomputation impossible for every row** (F1), including rows whose only redacted field is `i` — the pack discards the intent string, which is demonstrably part of the digest (identical `tool`+`path` pairs carry three different digests within this slice, e.g. `read …/check-boundary-contract.py` → `e04cbd3d…` / `df01a003…` / `5dff2e00…`; `grep …/check-boundary-contract.py` → `659075d2…` / `d76f6439…` / `516b6e6c…`). The digests are internally consistent with an argument-level hash (every equal-digest group is exactly an identical `tool`+`path`+argument group), so no digest looks fabricated, but equality is the strongest available check.
4. **`edit` targets are partly unrecoverable** (F3): `FxC2Bash:22` has no `path` in the pack, so no component can be scored for it by anyone, in this wave or later, without the original transcript.
5. **No runtime enforcement is claimed or tested here.** This seat verified recorded metadata only; no tool call was executed, no checker was run, and no claim is made that any checker enforces these values at runtime.

Reviewed-SHA256: 73a265762770c8ca133bd2cea861cf396a84b3bb3a2edab981e8cd1d7ece8835
Predicate: r23f-fxc3falsify02
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
