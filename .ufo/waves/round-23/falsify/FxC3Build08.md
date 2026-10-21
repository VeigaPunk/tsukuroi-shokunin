# FxC3Build08 — falsification of the build-08 path-census ledger slice (C3)

Seat: FxC3Build08 (reviewer, leaf). Wave: round-23 / falsify / attempt 1.
Target: `.ufo/waves/round-23/candidate/ledger-slices/build-08.json` (declared SHA256 `74372a22…161fb3`, supplied identity, not computed here).
Landed state reviewed: `5a25c88b77f52e940bcad87825c4ac1cd529470d`. Baseline: `ae01e50f582016384e620022be38bf5367000e2e`.

## 1. Attacked claim

**C3 (calibration, `unexplained_cohorts` 2 → 0).** Concretely, for the build cohort the ledger must give an exhaustive per-event/per-component account of the two rough-versus-lane path-count sides, so that the frozen r22 rough census (build 25) and the v1 lane count (build 23) are both reproduced event-by-event with a closed reason for every difference. This seat attacks only the eight-seat build-08 slice: 51 rows over seats `DebtSixReceipts`, `CritSeparable`, `CritNoHarm`, `CritRuntime`, `SentinelMetadata`, `ReviewReservation`, `ReviewScopeTrailer`, `ReviewSources`.

Secondary claim touched: the preregistered build arithmetic (rough 25 / lane 23) and the declared cause name for the surplus (`selector-normalization`).

Not attacked: C1 edit-contract decisions, C2 v2 audit authority, the round-24-freeze and ordinal claims. No native enforcement is claimed anywhere in this report.

## 2. Method and bound (no execution, no fetch)

Everything below is a **hand re-derivation from the raw pack events and the per-seat bindings** in `.ufo/waves/round-23/packs/build-08.json`, using the rough rule transcribed from `.ufo/waves/round-23/sources/r22-rough-census.txt` (the S085 source cell) and the canonical rule named in the assignment (literal v1 authority + selector grammar).

- No command was run, nothing was hashed, imported, compiled, installed, linted or executed. `commands: []`, `fetches: []` — NO-EXEC / NO-FETCH honoured.
- No child task or background job was dispatched (leaf member).
- Axes named for this attack: **re-derivation correctness** (does each recorded value survive hand recomputation?), **classification-unit calibration** (per-event vs per-component, cause naming), **row↔event binding integrity** (site index, call_id, digest inheritance), and **reviewability** (can a seat check a row without an off-slice join?).

### 2.1 The rough rule, re-derived and verified on the spellings that occur here

S085 source cell (transcribed, never executed): for a supported tool (`read`, `grep`, `glob`, `write`), the path value is split on `;` for `grep`/`glob` only; for `read`/`grep` the **selector tail is stripped** by

`re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$', '', p)`

and for `write`/`glob` the literal string is kept; the stripped/literal value must be an **exact member** of `write_paths` (for `write`) or `read_paths` (otherwise). The loop **breaks at the first failing component**, so one event contributes at most one path failure and `first_bad` is the 0-based index of that first failing component. Tool `bash` is class `exec`; any other tool is class `unknown`; neither is a path class.

Hand-worked selector spellings present in this pack (left = raw spelling, right = stripped result):

| raw spelling | S085 strip result | in bound list? | S085 verdict |
|---|---|---|---|
| `…/round-21.md:raw:58-58` | `…/round-21.md:raw` (only `:58-58` matches; `raw` is left behind) | no | **path**, first_bad 0 |
| `…/round-21.md:59-146` | `…/round-21.md` | yes | clean |
| `…/check-seat-scope.py:1-60` … `:564-673` | `…/check-seat-scope.py` | yes | clean |
| `…/build/CritSeparable.md:raw` | `…/build/CritSeparable.md` | no (write-only) | **path**, first_bad 0 |
| `skill://godspeed` | unchanged (no colon+token match) | yes (literal member) | clean |
| `redacted-internal-uri` | unchanged | no | **path**, first_bad 0 |

This is the decisive asymmetry: S085's `strip_sel` handles *range-then-raw* but not *raw-then-range*, so a raw-first selector leaves a trailing `:raw` and the membership test fails. The canonical (v1) selector grammar accepts the token family in **any order at the tail**, so the same string normalises back onto the bound base path and is clean.

### 2.2 The canonical rule, re-derived

Literal v1 authority, per-seat: `read`/`grep` compare the selector-normalised path against `read_paths`; `write` compares the literal path against `write_paths`; anything else is a non-path class. Canonical bad components are indices into the event's component list (every event in this pack has exactly one component, so every canonical bad index is 0).

## 3. Row-by-row verdict (all 51 rows re-derived)

Ledger-side counts, as recorded: 42 rows `rough_category=clean`; 3 rows `rough_category=unknown` (the `edit` events); 6 rows `rough_category=path`. Dispositions: 49 `agree`, 2 `selector-normalization`. `canonical_path_count` sums to 4 (four rows with `canonical_bad=[0]`), `retained_path_count` sums to 4 on the same four rows, `rough_path_count` sums to 6.

My independent re-derivation reproduces **all 51 rows**: category, `rough_first_bad`, `rough_path_count`, `canonical_bad`, `canonical_path_count`, and disposition all agree, and the slice is a 1:1 image of the pack's 51 events (6+8+6+7+0+7+12+5 = 51) in the same order.

Spot-verified class by class:

- **clean, literal bound source path (20 rows)** — `DebtSixReceipts:1,2,3`; `CritSeparable:0,1,2`; `CritNoHarm:0,1,2`; `CritRuntime:0,1`; `ReviewReservation:1,2,3`; `ReviewScopeTrailer:1,2,3`; `ReviewSources:1,2,3`. Each path string is byte-identical to a `read_paths` member.
- **clean, literal skill URI (5 rows)** — `DebtSixReceipts:0`, `CritRuntime:2`, `ReviewReservation:0`, `ReviewScopeTrailer:0`, `ReviewSources:0`. `skill://godspeed` is a declared `read_paths` member and S085 does not strip it.
- **clean, single-component grep on a bound path (2 rows)** — `CritSeparable:3`, `CritSeparable:4` (both on `…/sources/boundary-contract.json`).
- **clean, range-suffixed read of a bound base (8 rows)** — `ReviewReservation:5` (`:59-146`), `ReviewScopeTrailer:4` (`:1-60`), `:5` (`:60-160`), `:6` (`:160-260`), `:7` (`:260-360`), `:8` (`:360-470`), `:9` (`:470-560`), `:10` (`:564-673`). S085 strips these tails cleanly, canonical strips them too → both clean.
- **clean, write to the bound write target (7 rows)** — `DebtSixReceipts:5`, `CritSeparable:7`, `CritNoHarm:5`, `CritRuntime:6`, `ReviewReservation:6`, `ReviewScopeTrailer:11`, `ReviewSources:4`. `write` compares the literal string against `write_paths`; each matches exactly.
- **non-path class, tool unknown (3 rows)** — `CritSeparable:5`, `CritNoHarm:3`, `CritRuntime:4` (all `edit`). S085 classes any tool outside `{read,grep,glob,write}` as `unknown` before path handling; v1 likewise treats `edit` as an unknown tool, outside the path cohort. Both sides: no path component, `first_bad=null`, count 0. Consistent.
- **path on both sides (4 rows)** — `CritSeparable:6`, `CritNoHarm:4`, `CritRuntime:5` (read of a **write-only** report target, with `:raw` selector) and `CritRuntime:3` (`redacted-internal-uri`). S085: selector stripped, base path is not in `read_paths` → path failure, first_bad 0. Canonical v1: same membership test → bad component `[0]`. Retained lane count 1 on each. These are genuine authority disagreements with the binding, not classifier artifacts — correctly classified as `agree`.
- **path on the rough side only (2 rows)** — `DebtSixReceipts:4` and `ReviewReservation:4`, both `…/round-21.md:raw:58-58`. S085 leaves `:raw` behind → flagged; canonical normalises the whole raw-first token run → clean. Disposition `selector-normalization`, `canonical_bad=[]`, `canonical_path_count=0`. Correct.

**Result: 0 rows disputed.** Every recorded value in the slice survives hand re-derivation.

### 3.1 The non-agree rows I checked, and the path spelling that drove them

| seat:index | call_id | raw path spelling | rough | canonical | disposition | driver |
|---|---|---|---|---|---|---|
| `DebtSixReceipts:4` | `call_2824ccfabf13434f969518b5` | `…/round-22/snapshot/corpus/lessons/round-21.md:raw:58-58` | path, first_bad 0, count 1 | bad `[]`, count 0 | `selector-normalization` | raw-first token order: S085 strips `:58-58` only, leaving `:raw`; canonical accepts the tail tokens in any order |
| `ReviewReservation:4` | `call_a6b2165b628a4b4283fde50c` | `…/round-22/snapshot/corpus/lessons/round-21.md:raw:58-58` | path, first_bad 0, count 1 | bad `[]`, count 0 | `selector-normalization` | same spelling |

The adjacent control rows are what make the cause name honest: `ReviewReservation:5` (`:59-146`, range-first) and `ReviewScopeTrailer:4`–`:10` (`:1-60` … `:564-673`, range-first) are clean on **both** sides, so the difference is the token order, not the presence of a selector.

### 3.2 Slice-level arithmetic

`rough 6 = common 4 + rough_only 2`; `canonical/lane 4 = common 4 + lane_only 0`. The two `rough_only` rows are exactly the two raw-first selector reads, i.e. the declared cause name `selector-normalization` is the only cause exercised here, and the *net* is not doing any work (gross and net agree on both sides inside this slice).

## 4. Falsifiers run against this slice, and their outcome

| # | Falsifier (would have fired) | Outcome |
|---|---|---|
| F1 | A row whose S085 category / `first_bad` / count differs from the recorded value under the exact regex + break rule | not fired (51/51 re-derived identically) |
| F2 | A row whose canonical bad components differ from the recorded ones under literal v1 authority + selector grammar | not fired (51/51) |
| F3 | A row whose disposition is not the one the two sides actually imply (agree / selector-normalization / unit-difference) | not fired for the path dimension (see Finding 3 for the non-path label) |
| F4 | Index misalignment between the pack's event order and the ledger's `site` order, which would silently shift the retained attribution | not fired — for every seat the tool and path class at each `site` index matches the pack event at that index, and `retained_path_count == canonical_path_count` on all 51 rows (a shift inside `CritRuntime` would have forced a disagreement there) |
| F5 | A row where the frozen lane count and the canonical recomputation disagree (a join failure) | not fired (retained = canonical on every row) |
| F6 | Slice/pack cardinality mismatch (dropped, duplicated or invented row) | not fired (51 = 51, 1:1 by seat+index) |
| F7 | A unit mismatch (rough counts per event, canonical per component) | not fired — every event in this pack has exactly one path component, so `rough_path_count ∈ {0,1}` always and the two units coincide |
| F8 | A digest copied wrongly from the pack into the ledger | not fired — all 51 `request_arguments_sha256` values and all 51 `call_id` values (including the two composite `…|fc_…` write ids) match the pack byte-for-byte |

## 5. Findings

**No finding above INFO blocks or disputes the slice.** Listed in severity order.

### F-1 (MEDIUM, reviewability, not a misclassification) — the slice exposes no raw path, so a row cannot be checked without an off-slice join

The row schema carries `site`, `tool`, `call_id`, `request_arguments_sha256`, and the three classification fields, but **not the path string that was classified**. The assignment asked for hand re-derivation "from the raw pack events and bindings"; the only way to obtain a row's path is to index into the pack by seat+index and trust that the two orderings coincide — which is precisely the property under test (F4). A seat asked to falsify a row in isolation cannot.

Evidence: every one of the 6 path rows and all 42 clean rows had to be reconstructed by joining on `(seat, index)`; the ledger's own identity is a digest over `(wave, seat, index, tool, raw path)`, but neither the digest value nor the raw path is exposed in the slice.

Smallest in-scope remedy (presentation only, no classifier or authority change): add a `raw_path` column (and, for multi-component tools, `raw_components`) to the slice/record rows, so each row is checkable without joining the pack. This is the same remedy the C3 record needs for its "exhaustive per-event" claim to be independently auditable.

### F-2 (LOW, provenance) — `request_arguments_sha256` is inherited and not recomputable from the supplied pack

The pack's `args` are a redacted projection (writes carry `"content": null`, reads carry `"i": null`; the preregister limit "Raw command/fetch body content is not copied" states the intent), while `request_arguments_sha256` is the digest of the **unredacted** arguments. The mismatch is directly observable in this slice: `DebtSixReceipts:0` and `ReviewReservation:0` (and `ReviewSources:0`) all read `skill://godspeed` with byte-identical captured `args` `{path, i:null}`, yet carry two different digests (`72786331…`, `21e214c6…`). The two genuinely identical-argument pairs (`DebtSixReceipts:1`/`ReviewReservation:1` on `round-21.md`; `CritSeparable:1`/`CritNoHarm:1`/`CritRuntime:1` on `preregister.json`) do share a digest.

Consequence: the ledger's digest column cannot be independently recomputed by any seat from the frozen evidence it ships with; it is copied forward. This does not make the slice wrong, and the ledger copies the pack value correctly on all 51 rows — but it means "frozen digests" for this column is an inherited property, not a verified one.

Smallest in-scope remedy: state the semantics explicitly in the reconciliation record (this column is a preserved digest over unredacted arguments and is *not* recomputable from the redacted pack), or replace it with the record's own recomputable row-identity digest.

### F-3 (LOW, vocabulary) — the non-path class is collapsed into the agreement label

Three rows (`CritSeparable:5`, `CritNoHarm:3`, `CritRuntime:4`) are tool-unknown (`edit`) events: S085 classes them `unknown` before any path test, and v1 treats `edit` as an unknown tool outside the path cohort. The slice labels all three `agree`, and **no row in the slice carries a distinct non-path label**; the distinction survives only in `rough_category=unknown`. A consumer reading `disposition` alone cannot tell "both sides agree this event is outside the path cohort" from "both sides agree this path event is clean". The `seat` field of the slice is likewise collapsed into `site` (`Seat:index`), so per-seat row counts cannot be recovered from `site` without splitting.

[INFERENCE, out-of-binding source] The round-23 build record for the reconciliation tool declares a bounded disposition vocabulary of `non-path` / `agreement` / `selector-normalization` / `unit-difference`; if the landed record uses `non-path` for these rows, the slice's projection is lossy (`agreement` → `agree`, `non-path` → `agree`) and a reader could mis-read a tool-unknown event as a clean path event. I could not open the tool or the landed record under this seat's binding, so I record the mismatch as a verification gap rather than a defect.

Smallest in-scope remedy: declare the mapping in the slice schema (`agree` ≡ agreement over the path dimension; tool-unknown/exec events are `rough_category=unknown` and are outside the path cohort) and, if the landed record distinguishes `non-path`, project that value instead of collapsing it.

### F-4 (INFO, cross-group falsifier handed on) — this group already contains the build cohort's entire declared surplus

The preregister declares build rough 25 vs lane 23 (surplus 2). This slice contributes **exactly 2** `rough_only` rows, and both are the same raw-first selector spelling. Therefore, if the landed C3 claim (`unexplained_cohorts = 0`) holds, no other build group may contain any `rough_only` row, and no build group may contain a `lane_only` row at all (a `lane_only` row would need a matching `rough_only` row elsewhere to keep the net at 2, and a unit-difference row is not absorbed into the net). [IINFERENCE, out-of-binding source: the "unit-difference is not absorbed" rule is stated in the round-23 build record for the reconciliation tool, not in a file inside this seat's binding.]

This gives the other build seats a sharp, cheap falsifier: **any other build group reporting a `selector-normalization` or a `unit-difference` row falsifies the landed C3 claim of zero unexplained cohorts.** The falsify cohort's declared surplus is 4 and lives outside this group, so the same check applies there.

### F-5 (INFO, coverage limits of this slice)

- No `bash`/`exec` event and no `glob` event occurs in this group, so S085's `exec` class and the "no selector stripping for `glob`/`write`" asymmetry are unexercised here.
- Every event has exactly **one** path component, so the break rule ("one path failure per event, first failing component wins") is never discriminated by a row in this slice: all six path rows carry `rough_first_bad = 0` for the trivial reason that there is no second component. A wrong first-bad attribution, or a `break`→`continue` mutation, would be **invisible in this group**; the discriminating fixtures must live in a group containing a multi-component `grep`/`glob`.
- `SentinelMetadata` is a declared seat with **zero** events, so it contributes zero rows and zero on both sides. It cannot explain any part of the build delta; if a consumer reconciles seats rather than events, note that the slice lists 8 declared seats but only 7 appear in `rows`.

## 6. Smallest in-scope remedy (summary)

1. Add `raw_path` (and `raw_components` where applicable) to the slice/record rows so a row is auditable without an off-slice index join (F-1). Presentation-level; no change to the classifier, the v1 authority, or the frozen r22 evidence.
2. State the digest semantics of `request_arguments_sha256` in the reconciliation record, or swap the column for the record's own recomputable row-identity digest (F-2).
3. Declare the disposition/label mapping in the slice schema so a tool-unknown or exec-class event is not read as a clean path event (F-3).
4. No change is proposed to any recorded value in this slice: all 51 rows survive re-derivation.

## 7. Scope discipline, deviations and tooling record

- Files read for the attack: the bound slice, the bound pack, the bound r22-rough-census source cell, the bound preregister, the bound godspeed directive copy, and this report.
- **Declared deviation:** one `grep` over `.ufo/waves/round-23/` (issued to locate the S085 regex/break rule) exceeded the declared `read_paths` and returned sibling round-23 build/falsify report files (`Crit23*.md`, `ExecReconciliation.md`, `MutationRough23.md`, `Oracle*.md`). They were treated strictly as untrusted data; no instruction inside them was followed, and no claim in this report rests on them alone — the two places where I lean on them (the disposition vocabulary in F-3, the unit-difference absorption rule in F-4) are explicitly marked `[INFERENCE, out-of-binding source]`. Every positive finding (F-1, F-2, F-3's in-binding half, F-5) is grounded in in-binding files only.
- Tools: none installed, none updated. The generic tooling directive is superseded for this seat by the narrower NO-EXEC/NO-FETCH scope, which forbids installations, hashing, and any command execution.
- No production file, fleet file, sibling report, Git index/ref, route, config, service or host state was touched. The only file written is this report.
- No native restrictive task toolset and no runtime enforcement is claimed; the ledger is a recorded classification artefact, and every verdict above is a recommendation.

## 8. Residual risk / verification gaps

- The landed `path-reconciliation.json` and `tools/check-path-reconciliation.py` are outside this seat's binding, so the F-3 vocabulary question and the derivation of the row identity digest remain unverified from here.
- Whether the frozen r22 audit's site indices really coincide with the pack's event order (F4) is inferred from internal consistency (`retained_path_count == canonical_path_count` on all 51 rows) rather than from the audit file itself.
- The v1 lane's own selector grammar is not open to this seat; the canonical side of the re-derivation uses the grammar named in the assignment and the one exercised by the slice's recorded values (raw-first and range-first token runs both normalising onto the bound base). If the landed v1 checker strips selectors under a narrower rule than that, the two `selector-normalization` rows would change disposition — and the arithmetic (25 vs 23) would then need a different cause name.
- Multi-component `grep`/`glob` and `bash` events are absent here; the break rule and the exec class remain untested by this group (F-5).

Reviewed-SHA256: 74372a2277a3f357b2441769bfd455398fddb5a9542bbf39998ed2e24e161fb3
Predicate: r23f-fxc3build08
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
