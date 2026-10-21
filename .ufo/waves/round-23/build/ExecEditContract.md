# TsukuroiR23-2.ExecEditContract-7 — C1 `check-edit-contract.py` draft (round23 attempt1)

Baseline: ae01e50f582016384e620022be38bf5367000e2e (worktree branch round23/ExecEditContract).

## Files changed

- `.ufo/waves/round-23/worktrees/ExecEditContract/draft/check-edit-contract.py` — new, complete standard-library source, intended for `tools/` placement after L1 integration. Not executed, imported, compiled, tested, linted or formatted (NO-EXEC honored; no commands run, `commands: []`).
- `.ufo/waves/round-23/build/ExecEditContract.md` — this report. No production files, VCS state, refs, or fleet files touched.

## Behavior of the draft

- CLI: `--revision HEX` / `--branch master` (default) / `--selftest`, mutually exclusive, reusing the shared `tools/_revision.py` binding (`_revision.bind(ROOT, ...)`, `RevisionError` → exit 2 CANNOT_EVALUATE with the typed binding id). `sys.dont_write_bytecode = True` is set before importing `_revision`. Read failures at the selected revision → exit 2 with `EDIT-READ`. Exit classes 0 clean / 1 failed / 2 could-not-evaluate per existing convention.
- Reads four surfaces at the selected revision via `git show REV:path` (with the sibling `ls-tree` existence probe): `corpus/knowledge/structured-edit-r23.json`, `corpus/knowledge/structured-edit-r23.md`, `corpus/SOURCES.md`, `.ufo/waves/round-23/sources/structured-edit-observations.json`.
- `evaluate(raw, prose, sources, evidence) -> (code, payload)` exactly as specified. Payload carries `validated_edit_decisions` (0→8, `total_decisions: 8`), `findings`, `scope`, and CLI adds `revision`/`branch`/`branch_tip`.
- Contract definition for the new entry: `tsukuroi-edit-contract-v1` JSON with exactly eight unique `decisions` rows keyed `id/decision/reason/evidence/policy`, plus `scope`; the prose must carry one visible five-column table row per decision matching the tuple exactly (`id | decision | reason | evidence | policy`), using the landed finite Markdown carrier rules (`visible()`/`table_cells()` reused verbatim from `check-boundary-contract.py`: fence, HTML-comment, indentation, blockquote stripping).
- Fixed eight tuples from the primary source `edit-decision-policy.json` (schema `tsukuroi-edit-policy-v1`): DECLARED_EDIT/ALLOW, UNDECLARED_EDIT/DENY, READ_ONLY_EDIT/DENY, WRITE_ONLY_EDIT/DENY, OPAQUE_PATCH/UNKNOWN, EDIT_TRAVERSAL/DENY, EDIT_EXTERNAL/DENY, EXPANSION/CHECK_EACH — every row `evidence=S086`, `policy=round23-preregister`, reasons byte-identical to the primary source and preregister `edit_decisions`.
- Nonclean conditions: any decision/table divergence (`EDIT-DECISION-MISMATCH`), hidden (comment) or fenced rows, duplicated visible rows (indented or blockquoted), missing rows; duplicate JSON members (`object_pairs_hook` → `EDIT-SCHEMA`, exit 2), duplicate ids or wrong row count or extra rows (`EDIT-SCHEMA`, exit 2); missing new entry (`EDIT-CONTRACT-MISSING`, exit 1); wrong/missing S086 SOURCES.md row (`EDIT-SOURCE`: exactly one 11-cell row, path cell ending in the evidence path after `' — '`, cells 2:4 `own-work|A`, cell 7 `mined`, no backslashes); omitted or overclaiming no-enforcement scope in JSON or hidden in prose (`EDIT-LIMIT-MISSING`; LIMIT = the primary source scope sentence).
- Evidence source is audited shape-only (`audit_evidence`): exact schema `tsukuroi-structured-edit-observations-v1`, exact scope string (the observations file's own scope — any native-enforcement/universal-semantics overclaim fails `EDIT-EVIDENCE-SCOPE`; missing file → `EDIT-EVIDENCE-MISSING`, exit 1), per-observation shape: seat/agent/call_id nonempty control-free strings, 64-hex transcript sha, positive int request_line (bool rejected), `tool == 'edit'`, distinct nonempty `argument_keys` containing the structured `path` key, nonempty `path`, `body_fields` exactly `omitted; no report text copied`, and `recorded_starts` steps as positive-int line + tool + path. Any violation → `EDIT-EVIDENCE-SHAPE` (site = seat). Lane policy is validated only in the decision rows (`policy=round23-preregister` column), never from the evidence file.
- Any non-`EDIT-DECISION-MISMATCH` finding resets `validated_edit_decisions` to 0 (sibling rule).

## Selftest (literal, independent, not run)

`--selftest` builds its own literals — never synthesized from the module `EXPECTED` map: all eight policy rows redeclared, a two-observation evidence fixture with invented but well-formed shapes, an S086+S085 SOURCES fixture, scope strings redeclared locally. 38 cases with exact expected exit + finding id, including: clean (exit 0, count 8); missing raw/prose (`EDIT-CONTRACT-MISSING`); per-row decision forgery ×8; reason/source (`S085`)/policy (`legacy-default`) swaps; duplicate id, extra ninth row, duplicate JSON member, malformed JSON (exit 2 `EDIT-SCHEMA`); hidden, fenced, wrong-table (count asserted 7), missing row, indented duplicate, quoted duplicate; hidden limit, JSON scope overclaim, scope omitted; evidence scope overclaim (count asserted 0), missing `path` argument key, body-text copy, evidence schema swapped to the policy schema, evidence missing, evidence malformed; source missing (count 0), decoy path, wrong status, wrong tier, unpiped duplicate S086 row.

## Exact retained evidence

- Primary source `.ufo/waves/round-23/sources/edit-decision-policy.json` read in full (declared SHA256 f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805, supplied identity, not recomputed); its 8 decision rows, `source_path`, and scope sentence are transcribed verbatim into `EXPECTED`/`LIMIT`.
- `preregister.json` read in full: `edit_decisions` 8×3 agrees with the primary source; C1 command is `python3 tools/check-edit-contract.py --revision <REV>`; metric `validated_edit_decisions` 0→8; sources_opened names S086.
- `.ufo/waves/round-23/sources/structured-edit-observations.json` read in full (4 edit observations, argument_keys `path,stream_content` and `i,new_string,old_string,path`, `body_fields` marker, recorded_starts, exact scope sentence) — shapes mirrored by the evidence audit and fixtures.
- Sibling conventions taken from `snapshot/tools/check-boundary-contract.py` (evaluate/table carrier/selftest/git_read/main pattern), `snapshot/tools/check-review-snapshots.py` (control-char class, duplicate-key hook, receipt-line philosophy), `snapshot/tools/_revision.py` (bind/RevisionError/clean_env/ids).
- No builds/tests/linters/formatters run; no installations performed (none needed).

## Assumptions, risks, blockers

- The corpus knowledge entry `corpus/knowledge/structured-edit-r23.json/.md` is not yet landed at the baseline; this draft defines the document contract (schema `tsukuroi-edit-contract-v1`, scope sentence, five-column table grammar) the C1 knowledge author must satisfy — mirroring the landed `seat-boundary-r22` shape. If the entry lands with a different schema string or scope wording, the audit fails visibly by design.
- The SOURCES.md S086 row is expected to follow the corpus-wide 11-cell grammar pinned for S083/S084 (`own-work`, tier `A`, `mined`, path cell after `' — '`); the label prefix before the em-dash is deliberately unpinned.
- The evidence file must be committed at the audited revision; if absent there, the tool reports `EDIT-EVIDENCE-MISSING` exit 1 (not a crash).
- Blockers: none. L1 integration remains: place draft at `tools/check-edit-contract.py`; post-integration gates (`--selftest`, `--revision <REV>`) are the parent's to run.

Reviewed-SHA256: f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805
Predicate: r23-execeditcontract
Scope: executed=none
