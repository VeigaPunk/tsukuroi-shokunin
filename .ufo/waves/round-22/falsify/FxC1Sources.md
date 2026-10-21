# FxC1Sources — source-row validation attack (C1 depth)

Artifact: `.ufo/waves/round-22/candidate/tools/check-boundary-contract.py`
Digest: `1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485` (supplied by assignment; NOT recomputed — NO-EXEC).
Question: source row missing / duplicated / wrong kind / tier / status; are source IDs sufficient alone?
All findings are static source inspection. Nothing was executed (no Python, no `--selftest`, no `--revision`, no import, no hash command).
Expected fixture verdicts are stated separately from observed runtime; **observed runtime = none**.

## Verdict

Partially falsified. Exact-ID duplication, a wholly missing row, and wrong kind/tier/status **on the one row the parser counts** are rejected (lines 77–81). But the row identity is a byte-exact first-cell match on a raw `str.split('|')`, not a table parse:

- a duplicate that is a valid GFM table row omitting the optional leading pipe is never counted (C1);
- an escaped pipe (`\|`) shifts rendered columns while keeping raw index 7 = `mined`; a row whose rendered Status column reads `draft` produces no finding (C2);
- a deleted table row can be replaced by an inline prose line containing the same pipe sequence (C3);
- the path test is substring containment, so `.md.bak` or any prefixed decoy passes (C4);
- a visually identical duplicate using U+200B in the ID cell is not counted (C5);
- an absent `corpus/SOURCES.md` at the revision is classified `BOUNDARY-SCHEMA` / `CANNOT_EVALUATE`, not `BOUNDARY-SOURCE` / `FAIL` (C6).

"Source IDs alone" are not sufficient: one 11-cell metadata row per S083/S084 is required. But the row need not be a source-table row.

## Observed static facts (paths and lines)

- F1. `visible()` (38–55) drops HTML-comment and fenced lines; comment state is triggered by the literal `<!--` anywhere on a line and cleared by `-->`.
- F2. Source rows are `[[c.strip() for c in line.split('|')[1:-1]] ...]` (77). Everything before the first `|` and after the last `|` is discarded; no `line.startswith('|')` and no header/separator check.
- F3. Per-ID predicate (79–81): `len(found) == 1`, `len(found[0]) == 11`, `path in found[0][1]`, `found[0][2:4] == ['own-work','A']`, `found[0][7] == 'mined'`.
- F4. Decision rows require all five JSON fields to equal `EXPECTED` and the prose cells to equal exactly one row (84–92); prose cells require `line.startswith('|')` (82).
- F5. Columns 4,5,6,8,9,10 (scope, anchor, teaches, date, on-release, entry) are never checked.
- F6. `git_read` returns `None` for an absent path (145–146); `evaluate` only special-cases `raw is None or prose is None` (63–65), so `sources=None` reaches `visible(None)` and raises `AttributeError`, caught at 96 as `BOUNDARY-SCHEMA` code 2. Same for `host=None` via `json.loads(None)` at 74.
- F7. The 11-column layout is fixed only by the selftest fixture (106–107): `id | path | kind | tier | scope | anchor | teaches | status | date | on-release | entry`.

## Counterexamples (static trace; no execution)

For each: expected verdict if a fixed negative fixture encoded the named class, versus what lines 77–81 do with the exact literal input.

### C1 — duplicated row, GFM-valid pipe-less row (expected FAIL/BOUNDARY-SOURCE; static: no finding)

With the canonical S083 row present, append as a table body row (leading pipe omitted, which GFM accepts):

```
S083 | .ufo/waves/round-22/snapshot/corpus/lessons/round-21.md | own-work | B | scope | anchor | teaches | draft | 2026-10-21 | on-release | entry
```

`split('|')` yields 11 parts; `[1:-1]` keeps 9 and the first cell is the path, so `r[0] == 'S083'` is false and `found` stays at length 1. Readers see a second S083 row with kind `own-work`, tier `B`, status `draft`; the checker reports PASS. `len(found) != 1` never fires.

### C2 — wrong status via escaped pipe (expected FAIL/BOUNDARY-SOURCE; static: no finding)

Replace the canonical S083 row with (11 raw cells; `\|` is one scope cell in GFM):

```
| S083 | .ufo/waves/round-22/snapshot/corpus/lessons/round-21.md | own-work | A | sc\|ope | anchor | mined | draft | on-release | entry |
```

Raw split cells: `[S083, path, own-work, A, 'sc\', ope, anchor, mined, draft, on-release, entry]` → length 11, path at index 1, kind/tier at 2/3, **index 7 = `mined`**, one hit, so no `BOUNDARY-SOURCE`. GFM merges `sc\|ope` into one cell, so the rendered 11-column table places `draft` in the Status column (index 7) and leaves Entry blank. The checker's positional index and the rendered column diverge; wrong rendered status is accepted.

This is the positional counterpart of the same defect: `found[0][7]` is an offset in a raw split, not the row's Status cell under markdown escaping.

### C3 — missing table row satisfied by an inline line (expected FAIL/BOUNDARY-SOURCE; static: no finding)

Delete the S083 table row and add this visible (unfenced, uncommented) prose line:

```
Retained S083 | S083 | .ufo/waves/round-22/snapshot/corpus/lessons/round-21.md | own-work | A | scope | anchor | teaches | mined | 2026-10-21 | on-release | entry |
```

The prefix `Retained S083 ` is discarded by `[1:-1]`; the remaining 11 cells satisfy F3. There is no S083 row in the source table, yet no `BOUNDARY-SOURCE` is added. This is the "source row missing" acceptance: the predicate proves a pipe-delimited line exists somewhere visible, not that a source-registry row exists.

### C4 — wrong source path via substring (expected FAIL/BOUNDARY-SOURCE; static: no finding)

```
| S083 | /tmp/decoy/.ufo/waves/round-22/snapshot/corpus/lessons/round-21.md.bak | own-work | A | scope | anchor | teaches | mined | 2026-10-21 | on-release | entry |
```

`path in found[0][1]` is true for both the absolute-path prefix and the `.bak` suffix, so an unrelated or non-existent snapshot path is accepted. The fixture's `lesson — ` prefix (106) shows substring containment is deliberate for labels, but the predicate cannot distinguish the snapshot path from a longer path containing it.

### C5 — visually identical duplicate via U+200B (expected FAIL/BOUNDARY-SOURCE; static: no finding)

```
| S083​ | .ufo/waves/round-22/snapshot/corpus/lessons/round-21.md | external | C | scope | anchor | teaches | draft | 2026-10-21 | on-release | entry |
```

(U+200B between `3` and the following space.) `str.strip()` does not remove U+200B, so the first cell is not byte-equal to `S083`, the row is not counted, and the canonical row keeps `len(found) == 1`. To a reader the two ID cells are identical; a second row with wrong kind/tier/status is visible.

### C6 — absent source file misclassified (expected FAIL/BOUNDARY-SOURCE; static: CANNOT_EVALUATE/BOUNDARY-SCHEMA)

`main` passes `git_read(... 'corpus/SOURCES.md')` (164); an absent path returns `None` (145–146). `evaluate` only handles `raw`/`prose` absence (63–65); `source_text` becomes `None`, `visible(None)` raises, and line 96 emits `BOUNDARY-SCHEMA` with code 2. This is not acceptance, but it is the wrong finding class and loses both `BOUNDARY-SOURCE` findings; deleting the host evidence file likewise loses `BOUNDARY-HOST-LIMIT` into a schema error.

## Bounded reason the rest holds

- A byte-exact duplicate of `S083`/`S084` anywhere in visible text gives `len(found) == 2` → `BOUNDARY-SOURCE`; a wholly absent ID gives 0 → `BOUNDARY-SOURCE`.
- On the single counted row, a 12th cell, a shortened row, wrong kind, wrong tier, or non-`mined` status at offset 7 all reject.
- Decision rows cannot rely on the source ID alone: all five `EXPECTED` fields and exactly one matching prose row are required (84–92). Duplicated decision IDs are caught by the six-unique-ID check (70–71).
- Duplicate JSON keys are caught by `unique` (31–36, 68).

Caveats that bound these holds: the checks are positional and file-local; they do not validate columns 4–6/8–10, do not validate a header or table membership, and do not link a decision's `source` string to a source row's subject.

## Fixture coverage gap

`selftest()` lines 109–129 contain 18 cases. The only source-row negative is `source-missing` with `''` (126), which exercises the both-rows-absent path. There is no fixture for: duplicated source row, wrong kind, wrong tier, wrong status, wrong path, or a source row that is not a table row. Therefore C1/C2/C3/C4/C5 would not be caught by the existing fixed negatives, and the checklist claim that new checks have fixed negative fixtures is unmet for exactly the named mutant classes.

Adjacent, same hidden-content class: line 93 tests `'post-hoc detection, not preventive runtime enforcement' in text` on raw prose, so the phrase inside an HTML comment or fence satisfies the limit check while invisible to a reader (the `hidden`/`fenced` selftest cases fail on rows, not on this predicate). Expected FAIL/BOUNDARY-LIMIT-MISSING; static: no limit finding.

## Remaining unknowns

- `corpus/SOURCES.md` bytes are not in this seat's read paths, so the actual column count, row syntax, and whether the file is rendered as a GFM table are unverified. C1/C2 assume the 11-column layout fixed by 106–107; C3/C4/C5 are layout-independent within the checker's own parse.
- `git_read` mixes `git show <rev>:<path>` (root-relative in git) with `git -C ROOT ls-tree ... -- path` (cwd-relative), 141 vs 144. If `ROOT` is a subdirectory rather than the repository top level, the `show` read can resolve a different `corpus/SOURCES.md` than the `ls-tree` existence check; topology not verifiable without execution.
- Digest recomputation and runtime observation are out of scope under NO-EXEC. No production or candidate files were modified except this report.

## Receipt

Reviewed-SHA256: 1b91a7c10c971b554bad144035b40d0b7054e06582093f9f851ac0fcafdd2485
Predicate: r22-fxc1sources
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
