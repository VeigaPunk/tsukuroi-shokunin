# FxC3Build03 — C3 path-census ledger, build group 3

Seat: `FxC3Build03`. Declared review target: `.ufo/waves/round-23/candidate/ledger-slices/build-03.json`,
declared SHA256 `38dd04001aca73ddf1638d5318fce95f146cdcb6a0f4f25dcf853638807ad365` (supplied identity;
not computed here). Landed revision `5a25c88b77f52e940bcad87825c4ac1cd529470d` as stated by the slice.
Executed: nothing. No command, hash, import, compile, lint, or checker run.

## 1. Attacked claim

**C3 (calibration): `unexplained_cohorts` 2 → 0** — "Both fixed r22 cohorts have exhaustive
per-event/component explanation of rough-versus-lane path counts, frozen digests and declared
arithmetic." Seat slice: the 39 ledger rows of build group 3 across 8 seats.

Secondary, because it is the same arithmetic: the frontier's build-cohort count difference
(preregister `outside_round22.path_counts_as_reported`: rough 25, lane 23).

C3's own scope line forbids relabeling old violations or re-running historic checks for
confirmation; this seat therefore re-derives from the *pack* plus *bindings*, never from the
checker or from the slice's own claims about itself.

## 2. Method

Sources read (all declared):

- `.ufo/waves/round-23/packs/build-03.json` — 8 seat bindings, 39 raw events (fields `tool`,
  `args.path`, `call_id`, `request_arguments_sha256`, `origin`).
- `.ufo/waves/round-23/sources/r22-rough-census.txt` — the exact S085 census: tool gate, value
  list, `strip_sel`, one-point-per-event counter, first-bad `break`.
- `.ufo/waves/round-23/candidate/ledger-slices/build-03.json` — 39 rows.
- `.ufo/waves/round-23/preregister.json` — C3 metric, outside counts.

Rough side, re-implemented by hand per event: `bash` → `exec`; tool not in
`{read,grep,glob,write}` → `unknown`; else `vals = path.split(';')` for `grep`/`glob` and
`[path]` otherwise; `q = strip_sel(v)` for `read`/`grep` only; membership against
`write_paths` for `write`, else `read_paths`; first failing component increments the event once
and breaks.

`strip_sel = re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$', '', p)`.

Canonical side: literal v1 authority — exact string membership in the seat's declared
`read_paths` (selector grammar applied to `read`) or `write_paths` (no stripping), no prefix,
no normalization, no authority inferred from a write. Bad components are indices into that
event's value list.

Per-seat binding, identical for all eight seats except the seat name:

- read: `.ufo/waves/round-22/sources/host-tool-boundary.json`,
  `.ufo/waves/round-22/preregister.json`, `skill://godspeed`
- write: `.ufo/waves/round-22/build/<Seat>.md`

## 3. Re-derivation of every row

`R` = rough category / first-bad / count; `C` = canonical bad indices / count; `D` = ledger
disposition. Every row below reproduced; none disputed.

| site | call_id | tool | path spelling (as recorded) | R | C | D |
|---|---|---|---|---|---|---|
| OraclePathSibling:0 | call_00_ET_cRObkJEcJEe7OuJZKrE63699 | read | host-tool-boundary.json | clean/-/0 | []/0 | agree |
| OraclePathSibling:1 | call_01_ET_NakLCrL0OwIgKmtH8w6O0508 | read | preregister.json | clean/-/0 | []/0 | agree |
| OraclePathSibling:2 | call_02_ET_dAONu7bozLUIb6GYaaJ28354 | read | skill://godspeed | clean/-/0 | []/0 | agree |
| OraclePathSibling:3 | call_00_X2X7TTmLmhrU8yTpGNo49858 | write | build/OraclePathSibling.md | clean/-/0 | []/0 | agree |
| OraclePathSibling:4 | call_00_OWOcC447oumeUKJrcMcl3624 | edit | build/OraclePathSibling.md | unknown/-/0 | []/0 | agree |
| OraclePathRelative:0 | call_d54fd3e9…\|fc_06b70be6… | read | skill://godspeed | clean/-/0 | []/0 | agree |
| OraclePathRelative:1 | call_aec6c640…\|fc_06b70be6… | read | host-tool-boundary.json | clean/-/0 | []/0 | agree |
| OraclePathRelative:2 | call_56a1f89c…\|fc_06b70be6… | read | preregister.json | clean/-/0 | []/0 | agree |
| OraclePathRelative:3 | call_5564d8c7…\|fc_06b70be6… | write | build/OraclePathRelative.md | clean/-/0 | []/0 | agree |
| OraclePathDotDot:0 | toolu_01Udh36jBaCCZaFq5Vwn44AE | read | host-tool-boundary.json | clean/-/0 | []/0 | agree |
| OraclePathDotDot:1 | toolu_01JbR7pHb6ZSd6mamiyqBKC6 | read | preregister.json | clean/-/0 | []/0 | agree |
| OraclePathDotDot:2 | toolu_01TrSaSXWj5uyJSiBB6P733w | edit | build/OraclePathDotDot.md | unknown/-/0 | []/0 | agree |
| OraclePathDotDot:3 | toolu_01TrSaSXWj5uyJSiBB6P733w | read | build/OraclePathDotDot.md`:raw` | path/0/1 | [0]/1 | agree |
| OraclePathDotDot:4 | toolu_01TrSaSXWj5uyJSiBB6P733w | write | build/OraclePathDotDot.md | clean/-/0 | []/0 | agree |
| OraclePathSelector:0 | call_096d22d85fc0487ba1e60b6d | read | skill://godspeed | clean/-/0 | []/0 | agree |
| OraclePathSelector:1 | call_5ff0b46f9fd54aabb02162fe | read | host-tool-boundary.json`:1-5:raw` | clean/-/0 | []/0 | agree |
| OraclePathSelector:2 | call_cfdb69301dc34d8f8244b151 | read | preregister.json | clean/-/0 | []/0 | agree |
| OraclePathSelector:3 | call_a165cc034e8d4440a9c41332 | write | build/OraclePathSelector.md | clean/-/0 | []/0 | agree |
| OraclePathSemicolon:0 | call_00_ET_Hxflp35wnpmWXLymwnQK4182 | read | host-tool-boundary.json | clean/-/0 | []/0 | agree |
| OraclePathSemicolon:1 | call_01_ET_hdygM54GzO52iBbUrugc1196 | read | preregister.json | clean/-/0 | []/0 | agree |
| OraclePathSemicolon:2 | call_02_ET_AGc8TeL7KLsL8UKwp2Mn5049 | read | skill://godspeed | clean/-/0 | []/0 | agree |
| OraclePathSemicolon:3 | call_00_CCnwiwanx2qhY2JXsEZh8394 | write | build/OraclePathSemicolon.md | clean/-/0 | []/0 | agree |
| OraclePathWildcard:0 | call_753d1074…\|fc_095be9cb… | read | skill://godspeed | clean/-/0 | []/0 | agree |
| OraclePathWildcard:1 | call_88de2a5e…\|fc_095be9cb… | read | host-tool-boundary.json`:1-240` | clean/-/0 | []/0 | agree |
| OraclePathWildcard:2 | call_9cf8ec13…\|fc_095be9cb… | read | preregister.json`:1-240` | clean/-/0 | []/0 | agree |
| OraclePathWildcard:3 | call_d2178aa3…\|fc_095be9cb… | write | build/OraclePathWildcard.md | clean/-/0 | []/0 | agree |
| OraclePathSkill:0 | call_2d9447a6dca144b68504d31e | read | skill://godspeed | clean/-/0 | []/0 | agree |
| OraclePathSkill:1 | call_1749ee999d5c44b194317232 | read | host-tool-boundary.json | clean/-/0 | []/0 | agree |
| OraclePathSkill:2 | call_9b0a5996e2a54ce6b3e327c8 | read | preregister.json | clean/-/0 | []/0 | agree |
| OraclePathSkill:3 | call_746596c932c14821a3cdc559 | write | build/OraclePathSkill.md | clean/-/0 | []/0 | agree |
| OraclePathArtifact:0 | call_00_ET_Za93TVhw7M5hC9AhTXgA2702 | read | host-tool-boundary.json | clean/-/0 | []/0 | agree |
| OraclePathArtifact:1 | call_01_ET_HJmN0AfBWFIiDEzsP7yX0614 | read | preregister.json | clean/-/0 | []/0 | agree |
| OraclePathArtifact:2 | call_02_ET_MXvIuWShAxtGxMu7BNsY8070 | read | skill://godspeed | clean/-/0 | []/0 | agree |
| OraclePathArtifact:3 | call_00_ET_9ujWNOULnpZMsB4YC3K68048 | read | `round-22/build` (directory) | path/0/1 | [0]/1 | agree |
| OraclePathArtifact:4 | call_01_ET_4Vn0gyd9JHgqcHJq8CnV9402 | glob | `tools/*.py` | path/0/1 | [0]/1 | agree |
| OraclePathArtifact:5 | call_00_c9q0Gw8mqaxhRMIkdFqL5227 | write | build/OraclePathArtifact.md | clean/-/0 | []/0 | agree |
| OraclePathArtifact:6 | call_00_hvOTrbx3xphvC7xox3rH9470 | edit | build/OraclePathArtifact.md | unknown/-/0 | []/0 | agree |
| OraclePathArtifact:7 | call_00_Q0S2EKfbY3zp9UWqAIj37496 | edit | build/OraclePathArtifact.md | unknown/-/0 | []/0 | agree |
| OraclePathArtifact:8 | call_00_49kg5c5quaga33svwodl1gci | edit | build/OraclePathArtifact.md | unknown/-/0 | []/0 | agree |

Full prefixes elided above with `…` are for display only; the pair of full call_ids and the
`request_arguments_sha256` for every one of the 39 rows were compared literally against the pack
and matched (see §5, F5). Totals: 31 clean rows, 3 `path` rows, 5 `unknown` rows = 39; rough
path sum 3, canonical path sum 3.

## 4. Disputed rows

**None.** 0 of 39 recorded values are disputed; there is no seat/index/call_id to report.

The eight non-agree rows checked, with the path spelling that drove them:

1. **OraclePathSibling:4** `call_00_OWOcC447oumeUKJrcMcl3624`, tool `edit`, target
   `…/round-22/build/OraclePathSibling.md`. Rough `unknown`: the census tool gate excludes
   `edit` before any path read. Canonical `[]`/0: v1 has no edit authority at all, and the
   target is simultaneously a declared write path, so no reading of v1 makes it a violation.
   `agree` confirmed.
2. **OraclePathDotDot:2** `toolu_01TrSaSXWj5uyJSiBB6P733w`, tool `edit`, target
   `…/build/OraclePathDotDot.md`. Same gate → `unknown`/0; target is the declared write path.
   `agree` confirmed.
3. **OraclePathDotDot:3** `toolu_01TrSaSXWj5uyJSiBB6P733w` (additional-recorded-start),
   tool `read`, spelling `…/round-22/build/OraclePathDotDot.md:raw`. `strip_sel` removes the
   trailing `:raw`, yielding `…/round-22/build/OraclePathDotDot.md`, which is **not** in
   `read_paths` (only the sources file, the preregister, and `skill://godspeed`). Rough
   `path`/0/1. Canonical literal membership: same conclusion, `[0]`/1. This is the decisive
   row: write authority over the seat's own report does **not** confer read authority, so the
   same path is legal as `write` (row :4) and illegal as `read`. `agree` confirmed.
4. **OraclePathArtifact:3** `call_00_ET_9ujWNOULnpZMsB4YC3K68048`, tool `read`, spelling
   `…/round-22/build` with no selector, so `strip_sel` is a no-op. It is a strict prefix of the
   seat's write path `…/build/OraclePathArtifact.md` but not a member of `read_paths`. Literal
   authority → `path`/0/1; canonical `[0]`/1. `agree` confirmed.
5. **OraclePathArtifact:4** `call_01_ET_4Vn0gyd9JHgqcHJq8CnV9402`, tool `glob`, spelling
   `…/tsukuroi-shokunin/tools/*.py`. The glob branch takes `path.split(';')` (one element) and
   applies **no** `strip_sel`, then compares to `read_paths`; `tools/*.py` is not declared.
   `path`/0/1; canonical `[0]`/1. `agree` confirmed.
6. **OraclePathArtifact:6** `call_00_hvOTrbx3xphvC7xox3rH9470`, tool `edit`, declared write
   path → `unknown`/0, canonical `[]`/0, `agree`.
7. **OraclePathArtifact:7** `call_00_Q0S2EKfbY3zp9UWqAIj37496`, tool `edit`, same → `agree`.
8. **OraclePathArtifact:8** `call_00_49kg5c5quaga33svwodl1gci`, tool `edit`, same → `agree`.

## 5. Bounded falsifiers tried (and what each returned)

- **F1 count divergence.** Looked for any row with `canonical_path_count != rough_path_count`
  or a non-empty canonical set beside `rough_category: clean`. Result: none; all rows are
  0/0 or 1/1, and the two `path`-category rows in Artifact plus the one in DotDot carry
  matching `[0]`/1.
- **F2 classification flip.** Looked for a row where one side calls `path` and the other has
  no bad component, or the reverse. Result: none.
- **F3 retained-vs-canonical.** Looked for `retained_path_count != canonical_path_count`.
  Result: none (pairwise equal on all 39 rows).
- **F4 ordering/site integrity.** Compared the 39 sites against the 39 pack events in pack
  order, per seat. Result: exact 8/8 seat sequences, including the three rows that share
  `call_id toolu_01TrSaSXWj5uyJSiBB6P733w` and are separated by distinct digests
  `42956926…`, `7f309c76…`, `defb6bca…` in pack order (edit, additional read, additional write).
- **F5 digest binding.** Compared `call_id` + `request_arguments_sha256` of every ledger row to
  the pack event with the same `call_id` (three pairs share a call_id but not a digest).
  Result: 39/39 literal equality. The `:1-5:raw`, `:1-240`, `:raw` spellings are exactly the
  recorded `args.path` values, not reconstructed ones.
- **F6 build-cohort arithmetic.** Group 3 contributes rough 3 and canonical 3 path events, i.e.
  **delta 0** toward the outside 25 vs 23. It also contains 5 `edit`/`unknown` events. Because
  5 > 2, the build delta cannot be a rough-counts-edit-unknowns artifact: if rough added
  unknown edits while lane counted only path rows, group 3 alone would overshoot the reported
  gap. So the two published counts must be path-only on both sides, and the 2-row difference
  is located entirely outside group 3. This neither confirms nor falsifies C3 (C3 explains a
  difference; it does not require zero), but it fences where the explanation must live.
- **F7 break rule / component index.** No `grep`/`glob` event in this slice carries `;`, so the
  split-and-break-at-first-bad rule has no discriminating instance here; every `rough_first_bad`
  of 0 indexes a single-component list. The only multi-component machinery reachable in this
  pack is the glob's one-element split. Coverage note, not a dispute.

## 6. Residual hinges and gaps

These are the places where a recorded value is right only under a stated reading; they are not
disputes because the attack's own grammar selects the reading used.

- **H1 composed selector strip.** `OraclePathSelector:1` (`:1-5:raw`) and
  `OraclePathWildcard:1/:2` (`:1-240`) are clean only because the declared `strip_sel`
  alternation `(\d[\d\-+,:]*)(:raw)?$` strips the range and the trailing `:raw` in one pass.
  If the canonical step stripped only one token, those three rows would become canonical-bad
  and their `agree` dispositions would be wrong. The ledger records them clean, so it
  implicitly asserts the composed strip. [INFERENCE] the canonical side uses the same
  selector grammar; I could not read `tools/check-path-reconciliation.py` (not a declared path)
  and executed nothing.
- **H2 literal versus prefix.** `OraclePathArtifact:3` is bad only under exact membership;
  prefix containment under `…/round-22/build` would make it clean. The attack text specifies
  literal v1 authority, so the recorded `path` is right. Same hinge on the directory read's
  no-selector spelling.
- **H3 edit neutrality.** All five edits target declared write paths, so `agree` survives
  either canonical reading (edit unaudited, or edit checked against write authority). The
  slice therefore cannot discriminate C2's edit semantics; that is C2's question, not C3's.
- **G1 unseen record.** The r22 reconciliation record itself and the sibling build groups are
  outside my read paths, so I assert only per-row reproduction for group 3, not the global
  "exhaustive" quantifier of C3.
- **G2 vacuous seats.** In this pack, `OraclePathSemicolon` issues only `read`/`write` events
  (no `grep`/`glob`), so it never exercises `;` splitting; `OraclePathWildcard` issues only
  line-range selectors, never a wildcard pattern — the sole wildcard spelling is Artifact's
  `tools/*.py` glob. Neither seat can evidence the split/break rule or wildcard handling from
  group 3 alone.

## 7. Verdict and smallest in-scope remedy

**C3 is not falsified by this slice.** 39/39 rows reproduce exactly on rough category,
first-bad component, canonical bad components, counts, and disposition; no row is disputed;
group 3 contributes zero to the build-cohort delta.

Smallest in-scope remedy: **none to any ledger row**. If C3's record needs to be
non-overclaiming, the minimal addition is one prose line in the r23 reconciliation record —
"build group 3: 39 events, 3 rough path = 3 canonical path, delta 0; the build 25→23 delta lies
outside group 3; `;`-split/break and wildcard spellings are not exercised in group 3" — with no
reclassification, no re-run, and no change to historical reds. Anything larger (relabeling rows,
recomputing counts, or extending the slice) would exceed C3's declared scope.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: 38dd04001aca73ddf1638d5318fce95f146cdcb6a0f4f25dcf853638807ad365
Predicate: r23f-fxc3build03
Scope: executed=none
