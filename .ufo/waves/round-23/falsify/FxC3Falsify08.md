# FxC3Falsify08 — falsification of landed path-census ledger slice falsify-08

Seat: `FxC3Falsify08` (TsukuroiR23-2.FxC3Falsify08-2). Round 23, wave `falsify`, group 8.
Landed revision under attack: `5a25c88b77f52e940bcad87825c4ac1cd529470d`. Baseline: `ae01e50f582016384e620022be38bf5367000e2e`.

## 1. Attacked claim and scope

Attacked claim: **C3** (`unexplained_cohorts` 2 → 0; "exhaustive per-event/component explanation of rough-versus-lane path counts"), specifically the *row-level* landed ledger slice for this pack
(`.ufo/waves/round-23/candidate/ledger-slices/falsify-08.json`, declared SHA256 `ce27c53445f434ee30d8ea077e0ad0268b3a50d12388b4959a38977e17f06a69`).

Secondary (read-only, cross-claim) attack surface: **C1**'s eight edit-contract decisions and **C2**'s v2 edit-audit authority, insofar as the two `edit`-tool rows in this slice are re-judged under the new table.

Nothing in C1's eight decision rows is *written* by this slice, so C1/C2 are attacked here only where a ledger row's classification is a direct consequence of a C1/C2 rule (see F2).

## 2. Method (bounded; NO-EXEC / NO-FETCH honoured)

* Read-only tools used: `read`, `grep`. No `bash`/`eval`, no command, no fetch, no delegate, no hash, no `wc`.
* Inputs read (all inside the seat's declared read set): the slice, the r23 preregister, `packs/falsify-08.json`, `sources/r22-rough-census.txt`, `sources/godspeed-directive.txt`.
* Digest is **supplied identity, not independently computed** — never hashed, listed, or verified by execution.
* Re-derivation was performed by hand from the raw pack events + the seat bindings in the pack, applying:
  * **S085 rough rule** (verbatim from `sources/r22-rough-census.txt`): `strip_sel(p) = re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)`; `bash` → `exec`; any tool outside `('read','grep','glob','write')` → `unknown`; `grep`/`glob` path split on `';'`; `read`/`grep` selector-stripped; `write` compared against `write_paths`, everything else against `read_paths`; **break after the first offending component** (so at most one `path` count per event).
  * **Canonical rule**: literal v1 authority (exact membership in the seat's `read_paths` / `write_paths`; no prefix, glob, dot-segment or alternate-spelling expansion) plus the read-tool selector grammar (`:N`, `:N-M`, `:N+len`, `:-N`, `:N,M`, `:N-M,N-M`, `:raw`, `:N-M:raw`, `:raw:N-M`).

## 3. Row inventory and event↔row alignment

The slice has **134 rows** over the 8 declared seats. The pack has **134 events**. Both are in identical order, and the `call_id` sequence and the `request_arguments_sha256` sequence match one-for-one (verified end to end; three spot checks at `FxCollectIntegrity:0`, `FxCollectNoHarm:0`, `FxCollectNoHarm:20` confirm the digest field binds the same event as the `call_id`).

| seat | rows | reads | greps | writes | edits | rows w/ non-`clean` rough category |
|---|---|---|---|---|---|---|
| FxCollectRoot | 0–12 (13) | 10 | 2 | 1 | 0 | 0 |
| FxCollectCallJoin | 0–16 (17) | 10 | 6 | 1 | 0 | 1 |
| FxCollectTerminal | 0–14 (15) | 14 | 0 | 1 | 0 | 0 |
| FxCollectProjection | 0–11 (12) | 10 | 0 | 1 | 1 | 3 |
| FxCollectParse | 0–14 (15) | 13 | 2 | 1 | 0 | 0 |
| FxCollectProvider | 0–10 (11) | 8 | 2 | 1 | 0 | 0 |
| FxCollectIntegrity | 0–29 (30) | 19 | 9 | 1 | 1 | 1 |
| FxCollectNoHarm | 0–20 (21) | 19 | 0 | 2 | 0 | 0 |
| **total** | **134** | **103** | **21** | **8** | **2** | **5** |

Tool-per-site strings in the ledger reproduce the pack exactly for every seat (spot-verified for all 8 seats, all 134 sites). No row is dropped, duplicated, or added. The four `grep` events with multiple `;`-separated components are `FxCollectRoot:10` (3 paths), `FxCollectRoot:11` (4), `FxCollectCallJoin:15` (3), `FxCollectProvider:5` (2); **every component of all four is a declared read target**, so no component index other than the three single-component rows below can ever be non-zero.

## 4. Disputed rows

**None.** I could not reproduce a single wrong recorded value in this slice. Every one of the 134 rows reproduces exactly on: rough category, rough first-bad component index, rough path count, canonical bad-component set, canonical path count, retained path count, tool, site index, `call_id` and argument digest. All 134 dispositions recorded as `agree` are, in my re-derivation, genuinely `agree`.

Re-derivation totals for the slice: `clean` 129 rows, `path` 3 rows, `unknown` 2 rows; rough path count 3, canonical path count 3, retained path count 3; canonical non-empty `canonical_bad` sets only on the 3 `path` rows, each exactly `[0]`.

## 5. Non-`agree`-signal rows I checked (the only rows that carry any signal) and the path spellings that drove them

These are the five rows whose rough category is not `clean`; each is a place where rough and canonical *could* have diverged and did not.

1. **`FxCollectCallJoin:11`** — `call_01_zv7nolyslt8sfcbou78cq3s3`, tool `grep`, path spelling `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate` (single component; a *directory* that is a strict prefix of five declared read targets, but is not itself a declared target).
   * Rough: `strip_sel` is a no-op (no selector) → not in `read_paths` → `path`, first bad component `0`, count 1.
   * Canonical (literal v1): the directory string is not an exact member of `read_paths` → bad component `[0]`, count 1.
   * **Agree.** This is the single row in the slice where the verdict flips on the *only* debatable rule: a prefix/glob reading of v1 authority would call it clean. The landed ledger's literal-exact reading is the one C1's `DECLARED_EDIT` / `EDIT_TRAVERSAL` rows also state ("exact target", "no dot-segment or alternate spelling expands the target list"), so the landed value is right and the prefix reading is the falsifier I tried and rejected.
2. **`FxCollectProjection:8`** — `toolu_01VXs75Mn61Tdm3wFtKKPU1i`, tool `read`, path spelling `redacted-internal-uri` (pack `origin: "additional-recorded-start"`; the placeholder is present *unredacted* in the pack).
   * Rough: no selector to strip → not in `read_paths` → `path`, first bad `0`, count 1.
   * Canonical: not a declared target, not under the seat root, not a filesystem path at all → bad component `[0]`, count 1.
   * **Agree.** Identity of the real target is unrecoverable from the pack, so the row can only ever be justified as "target not declared" (see F3/§8).
3. **`FxCollectProjection:9`** — `toolu_017L5h3etK9RQ3Jof7LExKFB`, tool `edit`, path spelling `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxCollectProjection.md` (declared in `write_paths` only; absent from `read_paths`).
   * Rough: `edit` is outside the S085 enumerated set `('read','grep','glob','write')` → category `unknown`, path counts 0.
   * Canonical (literal v1 authority for the *target*): the target string is a declared write target → no bad component, count 0.
   * **Agree** on the v1 reading, but see **F2**: the new C1 table (`DECLARED_EDIT` requires the exact target predeclared for edit *and* for both read and write; `WRITE_ONLY_EDIT` → DENY) judges this row **DENY**. The row is therefore simultaneously "no bad path component under v1" and "denied under the r23 edit contract" — a tension the C3 record must state rather than leave implicit.
4. **`FxCollectProjection:10`** — `toolu_017L5h3etK9RQ3Jof7LExKFB`, tool `read`, path spelling `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxCollectProjection.md:raw` (write-only target read back; `origin: "additional-recorded-start"`).
   * Rough: S085's `raw` alternative strips the trailing `:raw` → bare `…/FxCollectProjection.md` → not in `read_paths` → `path`, first bad `0`, count 1.
   * Canonical: `:raw` is a selector under the read-tool grammar, so the target is the same bare path → read of a write-only target → bad component `[0]`, count 1.
   * **Agree.** Both classifiers strip `:raw` here, which is why this row is *not* an instance of the selector-grammar divergence class (see F1/falsifier 1).
5. **`FxCollectIntegrity:29`** — `call_00_YHBYZiIrYnM2DVsDCGlg7335`, tool `edit`, path spelling `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxCollectIntegrity.md` (write-only target).
   * Rough: `unknown` category, path counts 0. Canonical: declared write target → 0 bad components.
   * **Agree**, with the same C1-contract caveat as row 3.

## 6. Falsifiers run (bounded searches; all negative)

| # | Falsifier | Bounded search | Result |
|---|---|---|---|
| 1 | Selector-grammar divergence: a canonical-valid selector that S085's regex fails to strip, making rough a false positive and canonical clean (e.g. `X:raw:2-4` → S085 leaves `X:raw`). | Enumerated all 134 path strings in the pack; classified each suffix against the S085 regex and against the read-tool selector grammar. All 134 are `path` / `:N` / `:N-M` / `:N-M:raw` / `:raw` forms that S085 strips to the correct base path; **zero** strings of the `:raw:N-M` (or `:raw`+range) shape occur. | **0 hits.** This slice contributes **0** to the 33→29 rough-minus-lane gap via selector grammar. |
| 2 | Break-rule vs per-component divergence: a multi-component `grep`/`glob` where rough (break at first bad, one count per event) and canonical (per bad component) differ. | Enumerated all 21 grep events; the 4 multi-component ones were component-by-component checked against `read_paths`. All components declared → 0 bad components in every one. | **0 hits.** In this slice event-unit and component-unit counting are numerically identical (3 = 3). |
| 3 | Write-family authority flip: a `write` event whose target is in `read_paths` but not `write_paths` (or vice versa) that the landed ledger scored on the wrong list. | Checked all 8 `write` events against each seat's `write_paths`. All 8 targets are the seat's own `round-22/falsify/<Seat>.md`; none is in `read_paths`. | **0 hits.** |
| 4 | Row↔event misalignment: a row whose `call_id`/digest belongs to a different pack event (which would silently corrupt a per-row count). | Compared the 134-length `call_id` sequence and the 134-length `request_arguments_sha256` sequence of ledger vs pack, element by element, plus 3 targeted digest spot checks. | **0 hits.** Sequences identical in order. |
| 5 | Coverage hole: a pack event with no ledger row, or a ledger row with no pack event (per seat and overall). | Per-seat event counts from the pack vs per-seat row counts from the slice: 13/17/15/12/15/11/30/21 = 134 = 134. | **0 hits.** |

## 7. Arithmetic contribution of this slice to the C3 claim

The preregister records the outside ground truth as rough `falsify: 33` vs lane `falsify: 29` (and `build: 25` vs `build: 23`), under the key `path_counts_as_reported`. The rough side comes from the S085 cell, whose printed total is `sum(f.values())` over **all** buckets (`path`, `exec`, `unknown`) — see `sources/r22-rough-census.txt`.

This slice's falsify-group-8 contribution under the three candidate units:

* **path events (S085 unit): 3** — `FxCollectCallJoin:11`, `FxCollectProjection:8`, `FxCollectProjection:10`.
* **distinct violating tool calls (call_id unit): 2** — the three path rows sit on two call_ids: `toolu_01VXs75Mn61Tdm3wFtKKPU1i` (rows `FxCollectProjection:7` clean + `:8` bad) and `toolu_017L5h3etK9RQ3Jof7LExKFB` (rows `:9` edit, `:10` bad, `:11` write-clean). Three of this seat's events carry `origin: "additional-recorded-start"` (`:8`, `:10`, `:11`).
* **non-path-bucket rows (`unknown`, i.e. tool `edit`): 2** — `FxCollectProjection:9`, `FxCollectIntegrity:29`.
* **canonical path count: 3**, **retained path count: 3** (identical to rough in this slice).

So this slice is *unit-neutral* for the path bucket and can only explain part of the 4-unit rough-minus-lane gap through the two non-path-bucket rows and/or the event-vs-call unit. The full-cohort decomposition is L1's to run; §8 F1 gives the falsifiable prediction that follows from this slice.

## 8. Findings for L1 (findings, not edits — this seat may write only its own report)

**F1 — medium — unit/label risk in the C3 arithmetic: the rough number is an all-bucket total, not a path count.**
`preregister.json` stores the pair under `outside_round22.path_counts_as_reported` (`rough.falsify = 33`, `lane.falsify = 29`), but the rough side is the S085 cell's `sum(f.values())`, i.e. `path + exec + unknown` (`sources/r22-rough-census.txt`). If the lane side is a path-only count, then 33 vs 29 is a unit mismatch, not a discrepancy of 4 path events. **Falsifiable prediction:** the falsify cohort contains exactly **4** non-path-bucket rows (of which this slice supplies **2**: `FxCollectProjection:9`, `FxCollectIntegrity:29`, both tool `edit` → `unknown`), and the build cohort exactly **2**; then `rough_path(falsify) = 33 − 4 = 29 = lane` and `rough_path(build) = 25 − 2 = 23 = lane`, and the "unexplained cohort" is fully explained by *category*, not by path spelling. **If the landed full-ledger non-path row count is not 4 (falsify) / 2 (build), the C3 decomposition is unsupported** — that is the single cheapest check L1 can run to falsify or confirm C3 from the landed data.
**Smallest remedy:** one line in the C3 reconciliation record stating the unit of each side (`33 = path + exec + unknown`, with the 4/2 breakdown) — no relabelling of historical counts.

**F2 — medium — cross-claim: the two `edit` rows are "clean" under v1 but DENY under the r23 edit contract.**
`FxCollectProjection:9` and `FxCollectIntegrity:29` edit a target that is in the seat's `write_paths` and **not** in `read_paths`. The C3 canonical gives them 0 bad components (v1 authority: the target string is declared), while C1's `DECLARED_EDIT` ("exact target is predeclared for edit and for both read and write") and `WRITE_ONLY_EDIT` ("edit also needs its explicit target read authority") judge both **DENY**. The rows are individually correct under each authority model, but a reader of the C3 record could read `canonical_bad: []` as "the edits were authorized". **Falsifier:** apply C1's table to the two rows — if any landing text asserts these edits are authorized under v2, it is false.
**Smallest remedy:** one sentence in the C3 record naming the two `unknown` rows as *non-path-bucket, excluded from the path arithmetic, and re-judged DENY by the v2 edit authority*; do not change the v1 counts. (C2's v2 audit authority, if pointed at these two r22 events, must not be reported as agreeing with the C3 canonical — they disagree by construction.)

**F3 — low — traceability: the ledger slice records component *indices* only, and one offending target is a placeholder.**
`canonical_bad: [0]` identifies *which component* of a `;`-split path list is bad, but the offending **spelling** lives only in the pack; and for `FxCollectProjection:8` the pack's own value is the literal placeholder `redacted-internal-uri`, so the real target is unrecoverable. **Consequence:** any C3 sentence of the form "component *X* of *site Y* explains the difference" is only reproducible if the C3 checker binds the pack digest to the ledger rows. **Smallest remedy:** have the C3 record cite the pack event (seat, event index, `call_id`, argument digest) alongside the ledger row; no ledger schema change required.

**F4 — low — unit pinning for the "additional-recorded-start" steps.**
Three events in this seat carry `origin: "additional-recorded-start"` (`FxCollectProjection:8`, `:10`, `:11`). If the lane's 29 counts *tool calls* while the rough 33 counts *recorded adapter steps*, part of the gap is a unit difference, not a spelling difference. In this slice the two numbers are 3 (steps) vs 2 (calls) for the path bucket, and 2 non-path rows — so this slice can account for at most 3 of the 4 units, and only if the other groups show the same shape. **Smallest remedy:** state in the C3 record which unit each reported number uses (event/step vs call vs component), since the same label `path_counts` currently covers both.

**F5 — informational — the prefix-authority reading is the only live alternative in this slice.**
`FxCollectCallJoin:11` (grep over the *directory* `…/round-22/candidate`) is clean under a prefix/glob authority and bad under literal v1. The landed ledger takes the literal reading; that is consistent with C1's `DECLARED_EDIT`/`EDIT_TRAVERSAL` rows and I recommend keeping it, but the C3 record should say so explicitly, because it is the single row in the slice where a reviewer could reasonably expect the opposite verdict.

## 9. Residual risk and verification gaps

* **Not readable within this seat's read set** (and therefore not verified here): the landed full ledger and the C3 checker `tools/check-path-reconciliation.py`, the v1/v2 policy implementations, and the r22 `events.json`/`bindings.json` that the S085 cell actually read. Consequently F1/F4 are stated as falsifiable predictions with exact acceptance conditions, not as confirmed defects of the landed text.
* **The lane side of the 33/29 pair is not in evidence here.** I can reproduce the *rough* side exactly for this slice (3 path events, 2 non-path rows) but cannot confirm the lane tool's counting unit, its selector grammar, or its treatment of `edit`/`bash` from within the allowed inputs.
* **`redacted-internal-uri` is unrecoverable.** Row `FxCollectProjection:8` can only be justified as "target not declared"; any cohort-level claim that this row explains a *specific* path spelling would exceed the evidence.
* **Digest not independently verified** — `ce27c53445f434ee30d8ea077e0ad0268b3a50d12388b4959a38977e17f06a69` is taken as supplied identity; hashing was not performed (NO-EXEC).
* **Single-slice scope.** This slice closes the falsify group-8 question only; the cohort-level 33/29 and 25/23 arithmetic is cross-group and remains open to F1's check.
* **No runtime/enforcement claim.** Nothing here asserts that any tool enforces the bindings; the C2/v2 authority is documentary only, consistent with the r23 preregister's `limits`.

## 10. Tooling record

No tool was installed, updated, or removed by this seat. The seat's narrower NO-EXEC/NO-FETCH scope forbids installation, and host-wide `pacman` transactions are paused; no package channel was touched, no version was changed, and no service/boot action was taken. All work used only the read-only `read`/`grep` tools on declared paths plus the single write of this report.

Reviewed-SHA256: ce27c53445f434ee30d8ea077e0ad0268b3a50d12388b4959a38977e17f06a69
Predicate: r23f-fxc3falsify08
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
