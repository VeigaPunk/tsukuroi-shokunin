# FxC3Build01 — build-01 path-census ledger falsification

Seat: FxC3Build01 (leaf; NO-EXEC, NO-FETCH). Landed state 5a25c88b77f52e940bcad87825c4ac1cd529470d; baseline ae01e50f582016384e620022be38bf5367000e2e.
Target: `.ufo/waves/round-23/candidate/ledger-slices/build-01.json` — wave `build`, group 1, 8 seats, 26 rows. Reviewed digest is a supplied identity declaration, not recomputed.
Root elision: `$R` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; every path spelling below is `$R` + the shown suffix (or is shown verbatim when not rooted).

## Axes

- **A1 row fidelity** — does each recorded row equal a hand re-derivation from the raw pack event?
- **A2 authority-reading robustness** — does the recorded classification survive the strictest defensible reading of the authority (selector grammar, internal URIs, literal writes)?
- **A3 scope honesty** — what can this one slice prove about the wave-level counts, and what must stay unresolved?

## Authority applied (verbatim from bound sources, not paraphrased into a new rule)

S085 rough cell, `sources/r22-rough-census.txt`:

```python
def strip_sel(p):
  return re.sub(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$','',p)
```

Break rule as written: per event, `read`/`grep` path values are split on `;` (`grep` only), selector-stripped, then tested for literal membership in the seat's `read_paths`; the **first** offending value increments `path` once and `break` ends that event, so a single event can contribute at most 1 rough path count. `glob` is split but not stripped, tested against `read_paths`. `write` is never stripped and is tested literally against `write_paths`. `bash` counts as `exec`; any tool outside `{read,grep,glob,write}` counts as `unknown`, never as a path.

Canonical v1 (literal authority + read selector grammar), as the narrower authority: a `read` value is clean iff its selector-stripped value is literally a declared `read_path`; a `write` value is clean iff it is literally a declared `write_path`; an internal URI is clean only as the literal declared string (no URI-to-path translation); no dot-segment or alternate spelling expands the target list.

## Row re-derivation — all 26 rows

All rows record `rough_category=clean`, `rough_first_bad=null`, `rough_path_count=0`, `retained_path_count=0`, `canonical_bad=[]`, `canonical_path_count=0`, `disposition=agree`. Hand values below are what I derived; the last column is my comparison, not the ledger's own claim.

| site | tool | path spelling (after `$R`) | S085 normal form / membership | hand rough | hand canon | verdict |
|---|---|---|---|---|---|---|
| ConnProvince:0 | read | `/.ufo/waves/round-22/snapshot/PROVINCE.md` | literal, in read_paths | 0 | 0 | agree |
| ConnProvince:1 | read | `/.ufo/waves/round-22/preregister.json` | literal, in read_paths | 0 | 0 | agree |
| ConnProvince:2 | read | `/.ufo/waves/round-22/sources/host-tool-boundary.json` | literal, in read_paths | 0 | 0 | agree |
| ConnProvince:3 | read | `skill://godspeed` | no `:`-selector tail; literal in read_paths | 0 | 0 | agree |
| ConnProvince:4 | write | `/.ufo/waves/round-22/build/ConnProvince.md` | literal, in write_paths | 0 | 0 | agree |
| ConnPlanner:0 | read | `/.ufo/waves/round-22/snapshot/corpus/QUALITY.md` | literal, in read_paths | 0 | 0 | agree |
| ConnPlanner:1 | read | `/.ufo/waves/round-22/preregister.json` | literal, in read_paths | 0 | 0 | agree |
| ConnPlanner:2 | read | `/.ufo/waves/round-22/sources/host-tool-boundary.json` | literal, in read_paths | 0 | 0 | agree |
| ConnPlanner:3 | read | `skill://godspeed` | literal in read_paths | 0 | 0 | agree |
| ConnPlanner:4 | read | `/.ufo/waves/round-22/snapshot/corpus/QUALITY.md:1-60` | `:1-60` → `QUALITY.md`, declared | 0 | 0 | agree |
| ConnPlanner:5 | read | `...QUALITY.md:61-120` | `:61-120` → `QUALITY.md`, declared | 0 | 0 | agree |
| ConnPlanner:6 | read | `...QUALITY.md:121-180` | `:121-180` → `QUALITY.md`, declared | 0 | 0 | agree |
| ConnPlanner:7 | read | `...QUALITY.md:181-260` | `:181-260` → `QUALITY.md`, declared | 0 | 0 | agree |
| ConnPlanner:8 | read | `/.ufo/waves/round-22/preregister.json:1-40` | `:1-40` → `preregister.json`, declared | 0 | 0 | agree |
| ConnPlanner:9 | read | `/.ufo/waves/round-22/sources/host-tool-boundary.json:1-30` | `:1-30` → `host-tool-boundary.json`, declared | 0 | 0 | agree |
| ConnPlanner:10 | read | `...QUALITY.md:55-92` | `:55-92` → `QUALITY.md`, declared | 0 | 0 | agree |
| ConnPlanner:11 | read | `...QUALITY.md:40-56` | `:40-56` → `QUALITY.md`, declared | 0 | 0 | agree |
| ConnPlanner:12 | write | `/.ufo/waves/round-22/build/ConnPlanner.md` | literal, in write_paths | 0 | 0 | agree |
| OracleExecBash:0 | read | `skill://godspeed` | literal in read_paths | 0 | 0 | agree |
| OracleExecBash:1 | read | `/.ufo/waves/round-22/sources/host-tool-boundary.json` | literal, in read_paths | 0 | 0 | agree |
| OracleExecBash:2 | read | `/.ufo/waves/round-22/preregister.json` | literal, in read_paths | 0 | 0 | agree |
| OracleExecBash:3 | write | `/.ufo/waves/round-22/build/OracleExecBash.md` | literal, in write_paths | 0 | 0 | agree |
| OracleExecEval:0 | read | `/.ufo/waves/round-22/sources/host-tool-boundary.json` | literal, in read_paths | 0 | 0 | agree |
| OracleExecEval:1 | read | `/.ufo/waves/round-22/preregister.json` | literal, in read_paths | 0 | 0 | agree |
| OracleExecEval:2 | read | `skill://godspeed` | literal in read_paths | 0 | 0 | agree |
| OracleExecEval:3 | write | `/.ufo/waves/round-22/build/OracleExecEval.md` | literal, in write_paths | 0 | 0 | agree |

Totals: 22 reads (8 selector-suffixed, 4 internal-URI, 10 bare-literal) and 4 writes; 0 rough paths, 0 canonical paths. After selector normalization, all 8 selector reads hit a declared `read_path` exactly once, and no `;` appears in any path value, so the S085 cap of one path per event is never exercised.

## Disputes

**None.** Zero rows disputed; no recorded value in this slice is contradicted by a hand re-derivation from the pack.

## Non-agree candidates checked (rows where a stricter authority reading would flip the value)

All 26 rows were re-derived; the 12 rows below are the only ones where non-agreement was conceivable, and the spelling that drove them is quoted.

- **Selector hinge — 8 rows**: `ConnPlanner:4` `QUALITY.md:1-60`, `:5` `QUALITY.md:61-120`, `:6` `QUALITY.md:121-180`, `:7` `QUALITY.md:181-260`, `:8` `preregister.json:1-40`, `:9` `host-tool-boundary.json:1-30`, `:10` `QUALITY.md:55-92`, `:11` `QUALITY.md:40-56`. Under the recorded `clean`, all eight commit to the read selector grammar: a literal-only canonical reading (no `:N-M` documentation) would make each `canonical_bad` with count 1 and raise the group canonical total from 0 to 8. The selector reading is the one supported by the pack itself, which records `start_line` and `start_lines` separately from `path`, and by S085's own `strip_sel`, whose only purpose is to normalize exactly these suffixes. No dispute.
- **Internal-URI hinge — 4 rows**: `ConnProvince:3`, `ConnPlanner:3`, `OracleExecBash:0`, `OracleExecEval:2`, all `skill://godspeed`. The value carries no selector tail (`re.sub` cannot match `:godspeed` under `raw|\d…|-\d+|\d+-`), and it is literally present in each seat's `read_paths`, so both the rough and canonical passes must treat it as clean. Under a reading that restricts authority to filesystem paths these would flip to bad; the pack declares the URI as an authorized read path, so clean is the defensible value. No dispute.
- **Write hinge — 4 rows**: `ConnProvince:4` `build/ConnProvince.md`, `ConnPlanner:12` `build/ConnPlanner.md`, `OracleExecBash:3` `build/OracleExecBash.md`, `OracleExecEval:3` `build/OracleExecEval.md`. Each is byte-identical to its seat's single declared `write_path`, including the round-22 wave directory; no selector, no alternate spelling, no dot segment. No dispute.

## Identity cross-checks (row ↔ event)

- Pack events and ledger rows are one-to-one: 26 pack events (ConnProvince 5, ConnPlanner 13, OracleExecBash 4, OracleExecEval 4) against 26 rows, sites unique.
- Every ledger `call_id` and `request_arguments_sha256` equals its pack event's, including the one non-uniform value `OracleExecBash:3` `call_0fc69cfd7a55483c8d192a862eb59e42|fc_0b455b883fc78dbf016ad8d07a00448191b4d8ff92fa21ac70`, which is identical in both files.
- Row order follows pack seat order (ConnProvince before ConnPlanner), **not** the alphabetically sorted `seats` array; site indices are pack-order indices. A consumer that reassigns indices from the sorted `seats` list would mis-key all 26 sites.
- The four seats with no rows (ExecBoundary, ExecBindings, ExecCohort, ScribeBoundary) carry `events: []` in the pack, so no row is missing relative to the pack.

## Claim attacks

### C3 — path-census ledger (the target)

The exact falsifiers I searched, each exhaustively over the finite slice, and each failed:

1. a selector-stripped read value not literally declared → 0 of 8;
2. a write value not literally declared → 0 of 4;
3. a tool outside `{read,write}` (which would become `exec`/`unknown` rather than a path) → 0 events; no `grep`, `glob`, `bash`, or `edit` appears;
4. more than one path value in one event (where the `break` rule would undercount) → 0 events; no `;` in any value;
5. ledger/pack cardinality mismatch or duplicate site → none (26↔26, 26 unique sites);
6. identity mismatch on `call_id` or digest → none, pairwise equal;
7. a recorded count that disagrees with hand computation → none (0/0 vs 0/0 on all 26);
8. a non-null `rough_first_bad` on a row labelled `clean` → none;
9. a write whose seat binding lacks the path → none.

**Result: not falsified.** The build-01 rows are exact, and their zero counts are reproducible by hand from the pack under both authorities. This is a genuine (small) positive: a slice of 26 rows that could have contained selector or URI artefacts contains none misclassified.

### C1 — eight edit-contract decisions (spec-level only; this slice contains no edit evidence)

The pack's 26 events contain zero `edit` tool calls (`read`/`write` only), so C1 is not exercised here. Attacking the decision table itself from the preregister text: the four edit-bearing cells of the `{edit, read, write}` authority lattice are

- edit+read+write → `DECLARED_EDIT` ALLOW;
- edit+read, no write → `READ_ONLY_EDIT` DENY;
- edit+write, no read → `WRITE_ONLY_EDIT` DENY;
- **edit only, neither read nor write → no named row.**

`DECLARED_EDIT` demands all three legs, and each deny row names exactly one missing leg; the allow rationale plus the two deny rationales leave the edit-only cell covered only by analogy to `UNDECLARED_EDIT`, whose rationale is about edit authorization ("no implicit edit permission from generic report ownership"), not about missing read/write legs. A checker that implements the table literally has no decision for that cell and would have to default (to `UNKNOWN` like `OPAQUE_PATCH`, or to a skip). This is a totality/precision gap, **not** a falsification of the claim "eight decisions exist" — the count and the metric are intact. It is the one place where C1's contract could produce an unaudited edit six months from now.

### C2 — v2 edit audit authority

Not reachable from this slice: no structured edit target, no edit event, and the C2 command consumes round-23 wave `bindings.json`/`events.json`, not this frozen r22 pack. I can neither confirm nor falsify C2 here. One adjacent hazard is evidenced, though: the pack's legacy `digest_format` string is `sorted ensure_ascii JSON arguments; not raw JSONL bytes`, while four events reading the same bare `preregister.json` with byte-identical visible args (`path`, `i: null`) carry four **different** digests (`7a4052…`, `7cb935…`, `3d998e…`, `bc5baa…`), and three seats reading bare `host-tool-boundary.json` share one digest (`a025…`). The only consistent explanation is that the digest covers at least one argument field redacted in the pack (most plausibly a non-null `i`). If v2 reuses this digest format and a checker recomputes it from preserved arguments, it will mis-audit exactly the cases where a seat's intent string differed. Stated as hazard, not as observed C2 failure.

### Frontier

Build-01 moves no frontier axis: the slice is calibration-neutral at row level (0 rough, 0 canonical), so it can neither support nor refute any wave-total arithmetic. The two places a frontier move would have to be made are the residuals below, not the rows.

## Residual unknowns

1. **`retained_path_count` is undefined in every bound file.** Uniform 0 is consistent with a violation-retention meaning (the count of bad components retained for explanation) and inconsistent with an authorized-path meaning (which would be 1 per event, 26 in total). I mark the violation reading as `[INFERENCE]`; no glossary is bound and NO-FETCH forbids seeking one. This is a field-semantics gap, not a disputed row.
2. **The row digest is supplied identity, not a function of pack-visible arguments.** The signature is exactly what a hidden per-call field produces: identical visible arguments sometimes share a digest and sometimes do not. `preregister.json` read bare gives four distinct digests (`7a4052…`, `7cb935…`, `3d998e…`, `bc5baa…`); `host-tool-boundary.json` read bare gives `a025…` for ConnProvince:2, ConnPlanner:2 and OracleExecEval:0 but `02869cb7…` for OracleExecBash:1; `skill://godspeed` gives `2b4c…` for ConnProvince:3, ConnPlanner:3 and OracleExecEval:2 but `085bf6ab…` for OracleExecBash:0. Equality or inequality of digests therefore tracks a redacted argument (most plausibly a non-null `i`), not the visible path. Under NO-EXEC I did not hash anything. Consequence: the slice's `request_arguments_sha256` values cannot be independently recomputed from the pack alone, and digest equality across rows must not be read as proof of identical requests.
3. **Wave-total coverage.** The pack declares `group: 1`; the r22 outside observation for build is 25 rough / 23 lane. This slice contributes 0/0. If the build wave consisted only of these 8 seats and 26 events, 0 would contradict 25, so events outside this pack must exist. I cannot verify group coverage: directory enumeration is outside this seat's scope. I therefore make no claim about the wave totals or about other groups.
4. **Empty-seat event preservation.** ExecBoundary, ExecBindings, ExecCohort and ScribeBoundary declare write paths for checker tools that the r22 build evidently produced, yet record zero events. `[INFERENCE]` (low-medium confidence) that the pack preserved no events for those seats rather than that they made no adapter calls. If events were dropped, S085's census and the ledger both undercount by construction while remaining mutually consistent — this is the sharpest residual risk to C3's wave-level explanation, and it is invisible from inside the slice.
5. **Composite call id.** `OracleExecBash:3` carries a `|`-joined provider id, the only such value in the slice. It is identical in pack and ledger, so row identity is faithful; but if that id denotes a two-request batch, a one-event row cannot represent both, and S085's `break` caps the event at one path regardless. No effect at 0 counts.

## Smallest in-scope remedy

Documentation only; no production, test, config, or VCS edit from this seat:

- **C3:** add one sentence to the ledger definition naming the two authority hinges it already relies on — read paths are compared after documented `:selector` normalization, and internal URIs count only as the literal declared string — plus a one-clause definition of `retained_path_count`. No row changes, no reclassification.
- **C1:** extend one existing rationale instead of adding a ninth row: "edit requires declared edit and declared read and declared write; any missing leg denies." This closes the edit-only cell while preserving the claimed count of eight and the target.
- **C2:** if v2 reuses the legacy argument-digest format, state whether the digest covers preserved arguments only or the original intent field; otherwise a recomputing checker will diverge on seats whose `i` differed.
- **C3 coverage:** require any consumer to state per-pack rows and never sum a slice as a wave total (residual 3), and record the empty-event seats explicitly so their zero is a recorded fact rather than an absence (residual 4).

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: 0f84941f3f42ee4ebdad5af67769893236d0097195252bf08f913dde40d1a40a
Predicate: r23f-fxc3build01
Scope: executed=none
