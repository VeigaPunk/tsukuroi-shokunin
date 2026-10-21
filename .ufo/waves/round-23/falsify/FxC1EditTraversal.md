# C1 `EDIT_TRAVERSAL` → DENY — falsification

**Attacked claim:** C1 row `EDIT_TRAVERSAL` ("DENY — No dot-segment or alternate spelling expands the target list") is *validated* by `candidate/tools/check-edit-contract.py`; i.e. the tool's `PASS` / `"validated_edit_decisions": 8` establishes that the lane denies dot-segment and alternate-spelling target expansion.

**Smallest falsifier found:** two appended characters, `..`, on any S086 observation `path` (`<LANE>..`); the structured edit target then resolves one level *outside* the lane while the checker still predicts `PASS` / `"validated_edit_decisions": 8`.

**Method:** static read only (NO-EXEC). Reviewed `candidate/tools/check-edit-contract.py` (declared SHA-256 `620f3e5b…8e5081`, supplied identity, not recomputed), `candidate/corpus/knowledge/structured-edit-r23.json`, `candidate/corpus/knowledge/structured-edit-r23.md`, `candidate/corpus/SOURCES.md` line 93 (S086), `.ufo/waves/round-23/sources/structured-edit-observations.json`, and `.ufo/waves/round-23/preregister.json`. Every verdict below is *predicted by reading* `evaluate()`; no run was performed.

## 1. Landed row vs preregistered tuple — no drift

| field | preregister `edit_decisions[5]` | landed JSON `decisions[5]` | checker `EXPECTED[5]` | landed MD row |
|---|---|---|---|---|
| id | `EDIT_TRAVERSAL` | `EDIT_TRAVERSAL` | `EDIT_TRAVERSAL` | `EDIT_TRAVERSAL` |
| decision | `DENY` | `DENY` | `DENY` | `DENY` |
| reason | No dot-segment or alternate spelling expands the target list | same | same | same |
| evidence | — | `S086` | `S086` | `S086` |
| policy | — | `round23-preregister` | `round23-preregister` | `round23-preregister` |

The landed row is cell-for-cell identical (after `strip()`) to the preregistered triple plus the two fixed literal columns, so the preregister gate `declared != [list(e[:3]) for e in EXPECTED]` does not fire. The falsification therefore cannot be about transcription; it must be about what "validated" means.

## 2. Structural finding: `evaluate()` cannot validate this row semantically

`evaluate()` (from line 115) awards this row its credit only by

```
correct = set(row) == {'id','decision','reason','evidence','policy'}
          and tuple(row.get(k) for k in (...)) == expected
matches = [r for r in cells if r and r[0] == ident]
if not correct or matches != [list(expected)]: add('EDIT-DECISION-MISMATCH', ident)
```

— five string equalities plus one Markdown-row equality. The entire input domain is five documents (`main()`: `DATA`, `PROSE`, `corpus/SOURCES.md`, `EVIDENCE`, `PREREGISTER`). None is a seat binding, and the knowledge schema is closed: `set(data) != {'schema','decisions','source_path','scope'}` raises `EDIT-SCHEMA` (code 2), so the policy JSON *structurally cannot* carry `read_paths` / `write_paths` / `edit_paths`. From the preregister, `evaluate()` reads exactly one key: `pre.get('edit_decisions')`. The only path-sensitive code in the reviewed file is `evidence_ok()` lines 107–108.

Consequence: for **any** accepted corpus, the row's credit is independent of whether a dot-segment or alternate spelling is admitted anywhere. This is a real falsification of the *validated* predicate, not of enforcement (the tool disclaims enforcement in `LIMIT` and its docstring).

## 3. Falsifier A: recorded adapter step carries a dot-segment escape; checker still 8/8

Smallest literal change — in `sources/structured-edit-observations.json`, the observation with `"request_line": 33`, field `recorded_starts[0].path`:

- from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/OraclePathArtifact.md`
- to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/../../../../../../etc/passwd`

One string; no other byte changes. The fifth `..` leaves `LANE`; the sixth reaches `/home/vgpnk/Projects`, so the recorded target resolves outside the lane.

Why it passes, by line:
- line 108: `not isinstance(row.get('recorded_starts'), list) or not row['recorded_starts']` — list-ness and non-emptiness only. Element dicts are **never inspected**: no key, tool, or path of any step is read.
- line 107 (`startswith(LANE)`, `'/../' in path`) applies to `row['path']`, the frontend target, which is unchanged — and would *reject* this same string if it were the frontend target. The identical spelling is rejected in one field and unexamined in the other.

Predicted result: `evidence_ok` True; `evaluate` finds nothing; code 0; `{"status":"PASS","validated_edit_decisions":8}`.

This is by design, not a coding slip: the selftest fixture at lines 185–188 declares `recorded_starts: [{'tool': 'write'}]` and `[{'tool': 'edit'}]` — steps with **no `path` at all** — and expects code 0.

Meaning violated: S086 is registered (SOURCES line 93) as "Structured edit request metadata and adapter steps … recorded native steps", and the knowledge MD step 4 states "Audit every captured native read/write expansion against its own authority. A valid frontend target cannot clear an out-of-binding backend step." The certified evidence now records an adapter target whose spelling uses six `..` segments and leaves the lane, while the row certifies "No dot-segment or alternate spelling expands the target list" over exactly that artifact. Under the contrary reading (only declared authority lists count as "the target list"), §2 still holds: those lists are never inputs, so the certificate is vacuous either way.

## 4. Concrete falsifier B (smallest): the validated field accepts a trailing `..` and escapes the lane

Line 107 rejects only the four-character substring `/../`; a trailing `..` has nothing after it, so the test misses. Smallest literal input — two appended characters in any S086 observation's `path`:

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/..`

- `startswith(LANE)` is True: the string is exactly `LANE` + `..`.
- `'/../' in path` is False: no slash follows the two dots.
- The string resolves to `/home/vgpnk/Projects/shokunin` — one level **outside** the lane.

`evidence_ok` therefore returns True and `evaluate` returns PASS with `"validated_edit_decisions": 8`, while the row "No dot-segment or alternate spelling expands the target list" is certified over evidence whose structured edit target is a dot-segment that expands beyond the lane. This is the smallest falsifier found: 2 bytes, in the field the checker *does* validate (strictly smaller than §3's unvalidated-step edit and §5's prose deletion).

Related accepted spellings (`x/..`, `x/./y`, `x/%2e%2e/y`) confirm the predicate is a substring test rather than segment canonicalization; multi-`..` forms such as `x/../..` do contain `/../` and are rejected. The single trailing `..` is the exact miss.

## 5. Concrete falsifier C: the prose that operates the row can be inverted; still 8/8

Smallest literal change — in `structured-edit-r23.md` step 3, delete `never ` from `alternate path spellings never gain authority by inference`. Nothing else changes; the table still says DENY.

`table_cells(text)` is unchanged (no `|` introduced), `matches` is unchanged, `PROSE_LIMIT` is still present elsewhere, and the other four documents are untouched. `evaluate()` has exactly one prose predicate (`PROSE_LIMIT in '\n'.join(visible(text))`) and never cross-checks prose against the table. Predicted: PASS, 8/8, no findings, while the operative procedure now grants exactly the authority the row denies.

## 6. Residual: quoted-table carrier (low severity)

`table_cells` strips leading `>` (lines 83–84). Prefixing all eight table rows with `> ` still yields `matches == [list(expected)]` for every row → PASS 8/8, although CommonMark treats them as quoted, not asserted. **[INFERENCE]** on renderer semantics; the cell-level effect is code-observed. The `quoted-duplicate` selftest case shows quoted rows are meant to be *seen* (a wrong quoted duplicate must fail), so this corner follows the current design rather than a separate defect.

## 7. Bounded search

- `row['path']`: exactly one escaping spelling survives the substring test (`<LANE>..`); non-escaping alternates (`x/..`, `x/./y`) also survive; every multi-`..` spelling contains `/../` and is rejected. No smaller or more general bypass exists in this predicate.
- `recorded_starts`: element contents are not searched at all (line 108), so §3's space is unbounded rather than bounded.
- `argument_keys`: shape equality is exact (line 112 `shapes == {frozenset(s) for s in SHAPES}`); an extra key, missing shape, or duplicate key fails. No freedom.
- Policy JSON / SOURCES: key sets and cell sets are exact; extra keys are `EDIT-SCHEMA`. No freedom.
- `_revision.py` is outside this seat's declared read set; its `bind` / `clean_env` are unexamined. It governs revision resolution, not `evaluate()`'s row logic, which is fully visible in the reviewed file.

## 8. Smallest in-scope remedy

Checker patch (keeps `EXPECTED`, the eight-row table, the JSON schema, and `LIMIT` unchanged; ~8 lines):

1. In `evidence_ok`, replace `'/../' in row['path']` with a segment test, e.g. `not any(seg in ('.', '..') for seg in row['path'].split('/'))`; this rejects `<LANE>..`, `x/..`, and `x/./y`, and still admits the existing `:raw` selector suffix.
2. Validate every step: `all(isinstance(s, dict) and s.get('tool') in {'read','write','edit'} and isinstance(s.get('path'), str) and s['path'].startswith(LANE) and not any(seg in ('.','..') for seg in s['path'].split('/')) for s in row['recorded_starts'])`.
3. Add three selftest negatives expecting `EDIT-EVIDENCE`: `evidence-lane-parent` (`row['path'] = LANE + '..'`), `evidence-dot-segment` (`row['path'] = LANE + 'x/..'`), and `evidence-recorded-escape` (a `recorded_starts[0].path` of `LANE + '…/../../../../../../etc/passwd'`).

Claim narrowing (no checker change): falsifier C cannot be cheaply fixed by pinning more prose literals; narrow the claim instead — `PASS` certifies transcription of the eight decisions, not operation of the rules. The existing `LIMIT` ("no native prevention…") should be extended to say so; do not add a second prose-string gate.

## 9. Confidence and unknowns

- High: §1–§4, §6 cell behavior, §7 — all read directly from literal code; §5/§6 PASS follows because only `visible`, `table_cells`, and the `PROSE_LIMIT` substring can see prose.
- Medium: §6's renderer-level reading (marked INFERENCE).
- Unknown: `_revision.py` contents (out of read set); whether any downstream consumer treats `recorded_starts[*].path` as authority (this checker does not); no runtime observation of the predicted PASS outputs (NO-EXEC).

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxc1edittraversal
Scope: executed=none
