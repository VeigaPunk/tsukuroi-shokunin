# FxC1NoFetch — NO_FETCH source/reason mutation attack

Target: `.ufo/waves/round-22/candidate/tools/check-boundary-contract.py`
Claimed target SHA-256: `1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485` (supplied pin; not locally recomputed — this seat's command/fetch lists are empty, so no hashing command was run).
Method: source-only inspection of the declared read paths. No execution, import, mutation of the tree, or network access. All verdicts below are **derived from the code path**; the observed-runtime column is `none` by binding.

Read set: `check-boundary-contract.py`, `seat-boundary-r22.json`, `seat-boundary-r22.md`, `host-tool-boundary.json`, `preregister.json`, `_revision.py` (bind only), `check-review-snapshots.py` (header only), `skill://godspeed`.

## Axes attacked

1. Decision-row mutation detection (NO_FETCH `source` and `reason` in JSON and in the prose table).
2. Oracle integrity (can the expected tuple be moved with the data?).
3. Evidence-anchor integrity (is the cited S083 record content pinned?).
4. Declared policy vs native ability (does any check observe fetching?).
5. Negative-fixture coverage for the NO_FETCH row.

## Predicate map

- `EXPECTED` is an inline literal table; the NO_FETCH row is `check-boundary-contract.py:20`:
  `('NO_FETCH', 'URL read/web_search/browser', 'DENY', 'Local source reads never authorize network fetches', 'S083')`.
- JSON check: all five fields of each decision dict are compared to `EXPECTED` as an exact tuple (`:87`); one prose row whose stripped cells equal the same tuple must exist (`:82`, `:88–90`).
- Source-registry check: each S083/S084 row must have 11 cells, contain the declared path in cell 1, `own-work`/`A` in cells 2–3, and `mined` in cell 7 (`:77–81`). Cells 0 (sid), 4, 5 (anchor), 6 (teaches), 8 (date), 9, 10 are unread.
- Scope check: JSON `scope` must equal `LIMIT` and the raw prose text must contain `post-hoc detection, not preventive runtime enforcement` (`:26`, `:93`). The phrase test uses raw `text`, not `visible(text)`.
- Host check: only `native_per_seat_allowlist is False` and the exact `tools_semantics` string (`:75`). `approved_scope` in `host-tool-boundary.json:12` is never read.
- Inputs to `evaluate` are the two corpus files, `corpus/SOURCES.md`, and the host JSON only (`:164`). No seat binding, manifest, event trace, or fetch list enters the predicate.
- Selftest derives its clean data and prose from `EXPECTED` itself (`:104–105`), and its per-field negative mutants (`reason`, `surface`, `source`) target `decisions[0]` only (`:114–117`); `decision-1` mutates only the `decision` field of NO_FETCH (`:110–113`).

## Mutation matrix

All rows mutate only the NO_FETCH `source`/`reason` surface (or, where noted, the S083 record that NO_FETCH cites). "Expected" is the verdict the code would produce; nothing was run.

| # | Mutation | Expected verdict (derived) | Observed runtime |
|---|---|---|---|
| M1 | JSON `reason` only (`.json:15`) forged | exit 1, FAIL, `validated_boundary_decisions=5`, finding `BOUNDARY-DECISION-MISMATCH` site `NO_FETCH` (`:87`, `:90`) | none |
| M2 | JSON `source` only (`.json:16`) `S083`→`S084` | same as M1 — `EXPECTED:20` hardcodes `S083` | none |
| M3 | Prose table `reason` only (`.md:14`) forged | exit 1, same finding — `matches != [list(expected)]` (`:88–90`) | none |
| M4 | JSON and prose forged consistently | exit 1, same finding — the oracle is independent of both artifacts (`:20`, `:87`) | none |
| M5 | Checker `:20` `reason` forged **and** `.json:15`/`.md:14` forged in lockstep | exit 0, PASS, `validated_boundary_decisions=6`, no findings; selftest also PASS | none |
| M6 | Checker `:20` `source` `S083`→`S084` **and** both data rows changed | exit 0, PASS; selftest PASS (S084 row exists; no rule maps a decision to an allowed source) | none |
| M7 | S083 record cell 5 (`anchor`, and likewise 4/6/8–10) in `corpus/SOURCES.md` forged, path intact | exit 0, PASS — `:80` reads only 0, 1-substring, 2–3, 7 | none |
| M8 | Prose `reason`/`source` cells padded with whitespace only | exit 0, PASS — `.strip()` at `:82` | none |
| M9 | Visible prose overclaims prevention while the exact no-prevention phrase survives in an HTML comment/fence | exit 0, PASS — `:93` tests raw `text`, not `visible(text)` | none |
| M10 | Any NO_FETCH `reason`/`source` mutation as a new `--selftest` case | no such case exists; nearest coverage is `decision-1` (`decision` field only) and index-0 field mutants | none |

## Findings

**F1 — Direct mutation of the NO_FETCH decision row is fail-closed (holds).** Both carriers are compared to the inline `EXPECTED` tuple; JSON-only, prose-only, and consistent two-carrier forgeries all yield exit 1 with `BOUNDARY-DECISION-MISMATCH`/`NO_FETCH`, and the validated count drops to 5. Confidence: high (exact comparisons at `:87` and `:88–90`; no alternate NO_FETCH row can satisfy `matches` without itself equal to the expected row).

**F2 — The oracle is inline and unanchored; checker+data lockstep forgery passes (counterexample).** `EXPECTED:20` is the only authority for the NO_FETCH `reason`/`source`. Nothing in the file hashes or otherwise pins `EXPECTED` (`hashlib` is imported at `:6` and never used), so changing `:20` and both corpus rows yields PASS. The selftest cannot catch this: its clean fixtures are built from `EXPECTED` (`:104–105`), so a moved oracle moves the fixtures with it; its mutants only check a `FORGED` value against the same moved tuple. Only the externally supplied target SHA-256 pins this file. Confidence: high for `evaluate`; high for the selftest reasoning, with the single assumption that a mutated `EXPECTED` keeps the mutant values unequal to the fixed `'FORGED'` sentinel, which any substantive rewrite does.

**F3 — The cited S083 record's substantive cells are unpinned (counterexample).** `:80` verifies the row's identity shape but ignores cells 4–6 and 8–10, including the anchor cell that locates the evidence section in `round-21.md`. A change of anchor/teaches/date/package while the path stays in cell 1 passes with exit 0. This is the only way to mutate the NO_FETCH source without touching the decision row and still get PASS. I could not read `corpus/SOURCES.md` (not in this seat's read paths), so the actual cell contents are unknown; the exposure follows from the checked-index list alone. Confidence: high at predicate level; the concrete cell text is unverified.

**F4 — No fixture records a NO_FETCH reason/source verdict.** The negative bank covers all six `decision` fields (`:110–113`) but the `reason`/`surface`/`source` mutants apply to index 0 only (`:114–117`). The fixture's verdict for the assigned mutation is `absent`, not `pass`; the uniform loop at `:84–92` makes the derived verdict identical to M1, but that equality is untested by this file.

**F5 — Declared policy, not native ability (bounded reason it holds).** `evaluate` never receives seat bindings, commands, fetches, or event traces (`:164`); the host file contributes only two field checks (`:75`) and its `approved_scope` statement is unread. The NO_FETCH row is therefore a declaration that this contract says DENY; the tool cannot distinguish a conforming seat from one that fetched, and its own `LIMIT` (`:26`, `:93`, `:100`) and the prose (`seat-boundary-r22.md:22`) disclaim preventive enforcement. A source-only receipt from this tool must not be reported as runtime enforcement. Confidence: high.

**F6 — The visible no-prevention sentence is not pinned (secondary counterexample).** Because `:93` searches raw bytes, the readable sentence at `.md:22` can be replaced with a prevention claim while a commented or fenced copy of the exact phrase keeps the check satisfied; PASS. The machine-readable `scope` (`.json:47`) and the payload's `scope` field remain the honest `LIMIT`, so this is a prose-overclaim path, not an oracle move — but it is exactly the "source policy vs native ability" confusion the claim must not invite. Confidence: high.

**Non-attack observation.** `import hashlib` (`:6`) is dead in this file and coincides with the absent self-integrity anchor in F2. Not counted as a pass/fail for the predicate.

## Verdict

The shipped predicate is sound against mutation of the NO_FETCH `source` and `reason` **in the contract carriers**: every single-carrier or consistent two-carrier forgery is detected, because both are compared to the inline literal tuple. The predicate is not sound against mutation of its own oracle: a lockstep edit of `EXPECTED:20` plus the two carrier rows (M5/M6) produces a clean PASS and a passing selftest, and an S083 anchor-only edit (M7) passes without touching the decision row. Both are bounded by the externally declared SHA-256, which the file neither computes nor checks. The NO_FETCH decision remains policy-only, which the file states and does not overclaim.

## Remaining unknowns

- Actual `corpus/SOURCES.md` S083 row cells (not in read paths); M7's concrete effect is unverified, the unchecked positions are proven from code.
- Whether the S083 lesson (`round-21.md`, not in read paths) actually supports the network-fetch denial; the checker never tests semantic support, so the NO_FETCH grounding is asserted, not validated.
- Whether any sibling tool consumes `approved_scope`; `check-seat-bindings.py` is outside this seat's read paths.
- The supplied SHA-256 was not recomputed under NO-EXEC.

Reviewed-SHA256: 1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485
Predicate: r22-fxc1nofetch
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
