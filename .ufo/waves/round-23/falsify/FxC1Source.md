# FxC1Source — falsification of the S086 SOURCES-row check

Seat: FxC1Source (round 23, attempt 1, FALSIFY wave, C1 leg).
Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-edit-contract.py` (declared SHA256 `620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081` — supplied identity, **not** recomputed; NO-EXEC forbids hashing/running).

## 1. Attacked claim

**C1** (`preregister.json` → `claims[0]`, axis `depth`, metric `validated_edit_decisions` 0 → 8, command `python3 tools/check-edit-contract.py --revision <REV>`).

C1 is a three-legged contract: (a) the eight decisions in `corpus/knowledge/structured-edit-r23.json` + prose, (b) the policy source binding to `preregister.json`, and (c) the **S086 provenance row in `corpus/SOURCES.md`** (finding id `EDIT-SOURCE`). Leg (c) is what this seat attacks: the gate's assertion that the structured-edit source is registered in the registry with the right kind, tier, status and path.

The attacked rule, verbatim (`check-edit-contract.py`, `evaluate()`):

```python
found = [r for r in table_cells(source_text or '') if r and r[0] == 'S086']
if (len(found) != 1 or len(found[0]) != 11 or found[0][1].rsplit(' — ', 1)[-1] != EVIDENCE
        or found[0][2:4] != ['own-work', 'A'] or found[0][7] != 'mined' or any('\\' in cell for cell in found[0])):
    add('EDIT-SOURCE', 'S086')
```

`EVIDENCE = '.ufo/waves/round-23/sources/structured-edit-observations.json'`.

## 2. Axes named

| Axis | Question the rule must answer |
|---|---|
| A1 membership | Is the S086 line actually a **registry row** (inside the `## Registry` table) rather than any pipe-bearing line in the file? |
| A2 identity / uniqueness | Is there **exactly one** S086 row, counted by *identifier* rather than by raw cell text? |
| A3 path binding | Does the row's source cell name **the** evidence path (`EVIDENCE`), under the registry's own source-cell idiom? |
| A4 field binding | Are `kind`/`tier`/`status` the columns the header declares, or merely the values at positions 2/3/7? |
| A5 column model | Is the 11-cell/positional assumption the registry's shape, or one snapshot of it? |
| A6 content | Are `anchor` (evidentiary locator) and `used-by` (link to the produced artifact) verified at all? |

## 3. Findings (severity ordered)

### F1 — HIGH: registry membership is not checked; the gate certifies a non-registry line (A1)

`found` is built from `table_cells(source_text)`, which scans **every** pipe-bearing line of `corpus/SOURCES.md` — outside the `## Registry` table, outside the header/delimiter pair, in the `## Search log` prose section. The file itself draws the distinction the gate ignores: `corpus/SOURCES.md` § Leads states *"These follow-on leads are not evidence and not registry rows"* — i.e. the file separates registry rows from non-registry pipe-bearing text, and the gate does not.

**Registry text the gate wrongly ACCEPTS** (constructed; the S086 line is deleted from the `## Registry` table and re-emitted as one paragraph line in `## Search log`):

```
## Registry
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S085 | Outside round22 census method and disposition — .ufo/waves/round-23/sources/r22-rough-census.txt; .ufo/waves/round-23/sources/r22-closure.json | own-work | A | ... | ... | ... | mined | 2026-10-21 | on-release | corpus/knowledge/path-reconciliation-r23.md, corpus/lessons/round-23.md |

## Search log

S086 | Structured edit request metadata and adapter steps — .ufo/waves/round-23/sources/structured-edit-observations.json | own-work | A | Observed finite path/argument-key shapes and recorded native steps, not universal editor semantics, actual effects or runtime permission enforcement | observations argument_keys/path/recorded_starts and transcript SHA-256; baselineae01e50f582016384e620022be38bf5367000e2e; opened 2026-10-21 | Structured edit metadata exposes a target path plus opaque body-key forms and separate read/write starts; permission must be declared independently and prospectively for each exact target | mined | 2026-10-21 | on-release | corpus/knowledge/structured-edit-r23.md, corpus/lessons/round-23.md |
```

Traced outcome: `visible()` keeps the line (no fence, no 4-space indent); `table_cells()` splits it into exactly 11 cells (`r[0]=='S086'`); `found` has length 1; `r[1].rsplit(' — ',1)[-1] == EVIDENCE`; `r[2:4] == ['own-work','A']`; `r[7] == 'mined'`; no backslash → **no `EDIT-SOURCE` finding, gate PASSes** — with **no S086 row in the registry table at all**.

**Live instance of the same divergence in the landed file.** `corpus/SOURCES.md:71` is a blank line inside the registry table (between row `S064` at line 70 and row `S065` at line 72). Under the GFM table rule (header row + delimiter row + data rows; a blank line ends the block), the rows `S065`–`S086` (lines 72–93, including the S085 row at 92 and the **S086 row at 93**) are *not* rendered as table rows — the second block has no delimiter row. The gate's cell model has no header/delimiter requirement, so it counts them as rows anyway. Consequence: the C1 provenance check certifies a row that the rendered registry does not contain, and the divergence is already present in the landed artifact — it is not only a hypothetical mutation. (Rendering claim is an inference from the GFM table rule; NO-EXEC forbids rendering it.)

### F2 — HIGH: duplicate detection is raw cell-text equality; a decorated duplicate S086 row is invisible (A2)

Uniqueness is `r[0] == 'S086'` on the *raw* cell. Any Markdown decoration of the ID cell changes the string while rendering the same identifier, so the second row is never counted and `len(found) != 1` never fires.

**Registry text the gate wrongly ACCEPTS** (the landed S086 row at line 93 plus one appended row):

```
| **S086** | Duplicate of S086 — .ufo/waves/round-23/sources/structured-edit-observations.json | own-work | A | duplicate scope | duplicate anchor | duplicate teaches | mined | 2026-10-21 | on-release | corpus/knowledge/structured-edit-r23.md |
```

Traced outcome: `r[0] == '**S086**' != 'S086'` → not in `found` → `found` still has 1 element → all other conditions hold → **PASS**, while the file now renders **two** S086 rows (bold renders as S086). The same escape works for `` `S086` ``, `[S086](#s086)`, `S086<sup>`, or a leading index column (`| 87 | S086 | ... |`, where `r[0]=='87'`). The gate therefore cannot detect the duplicate-row condition it appears to police.

### F3 — HIGH: six of eleven columns are unverified, including `anchor` and `used-by` (A4, A6)

The rule inspects only the count, cell 1 (path), cells 2–3 (`kind`,`tier`) and cell 7 (`status`). Cells 4 (`scope`), 5 (`anchor`), 6 (`teaches`), 8 (`opened`), 9 (`recheck`), 10 (`used-by`) are never read. `anchor` is the evidentiary locator and `used-by` is the link from the source to the artifact the claim produces (`corpus/knowledge/structured-edit-r23.md`); neither is checked.

**Registry text the gate wrongly ACCEPTS** (gutted row):

```
| S086 | Structured edit request metadata and adapter steps — .ufo/waves/round-23/sources/structured-edit-observations.json | own-work | A |  |  |  | mined |  |  |  |
```

Traced outcome: 13 pipe-separated parts → `cells[1:]` → 12 → trailing `|` dropped → 11 cells; `r[2:4]`, `r[7]` and `r[1]` unchanged → **PASS** with an empty scope, an empty anchor, an empty teaching, no opened date, and **no `used-by` link to the produced artifact**. Equally accepted: a row whose `used-by` points at `corpus/lessons/round-99.md` — the gate still certifies the C1 provenance.

### F4 — MEDIUM: the field/column semantics are positional, so benign column shifts are falsely rejected (A4, A5)

The gate never parses the header row `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (`corpus/SOURCES.md:5`); it hardcodes 11 cells and indices 2/3/7.

* **Registry text the gate wrongly REJECTS (a):** add a 12th registry column (e.g. `evidence-digest`) to the header and to the S086 row → `len(found[0]) == 12` → `EDIT-SOURCE` → C1 FAIL, although the row is semantically correct and the new column is unverified-but-harmless.
* **Registry text the gate wrongly REJECTS (b):** the registry's own multi-source idiom. `S085` (`corpus/SOURCES.md:92`) writes two sources in one cell — `... — .ufo/waves/round-23/sources/r22-rough-census.txt; .ufo/waves/round-23/sources/r22-closure.json` — and `S015`/`S053`/`S072` do the same with URLs. `rsplit(' — ', 1)[-1]` then returns the *whole* path list, which can never equal a single path, so the rule **would reject the registry's own S085 row** if S085 were the target. Writing the S086 cell in that same in-file idiom (`... — observations.json; transcript-index.json`) is likewise rejected although the source is correctly registered.
* **Registry text the gate wrongly REJECTS (c):** any S086 cell containing a pipe inside a code span or escaped (`\|`) is split naively into an extra cell → count ≠ 11 → rejected, while the rendered row is a well-formed 11-column row.

### F5 — MEDIUM: the source-cell binding pins only the *last* ` — ` segment, so extra/decoy sources are accepted (A3)

`rsplit(' — ', 1)[-1]` constrains only the tail after the **last** em-dash separator.

* **Wrongly accepted:** `| S086 | Decoy packet — .ufo/waves/round-23/sources/r22-rough-census.txt — .ufo/waves/round-23/sources/structured-edit-observations.json | own-work | A | ... | ... | ... | mined | ... |` → tail == `EVIDENCE` → **PASS**, although the row's own description names a *different* packet (the r22 rough census) and registers two sources of which the gate pins one.
* **Correctly rejected (negative result):** a decoy *suffix* on the path (`...observations.json.bak`), a decoy *prefix* (`/tmp/decoy/.ufo/.../structured-edit-observations.json`), or any trailing descriptor (`... — observations.json — sanitized index`) all make the tail differ from `EVIDENCE` → `EDIT-SOURCE`. So the suffix decoy the brief asked about is handled; the *additional-source* decoy is not.

### F6 — LOW: the uniqueness check is global over the file, so an unrelated table breaks the gate (A1/A2 inverse)

Because `found` spans the whole file, any other table whose **first** column contains the literal `S086` (a source-index table, a "used-by" matrix, the `## Paths` section rendered as a table) makes `len(found) == 2` → `EDIT-SOURCE` → C1 FAIL, although the registry itself is unchanged. The registry is expected to grow (rounds 18–23 added 3→22 rows and 4 sections); the check has no scoping to the registry table, so benign file growth is a latent false-reject in both directions (F1/F3 accept too much; F6 rejects too much).

### F7 — LOW: the `\`-ban is a proxy that neither prevents what it implies nor matches the registry

`any('\\' in cell for cell in found[0])` bans any backslash in any of the 11 cells. Its apparent purpose (block `\|`-smuggled columns) is already defeated by the naive split, and it independently rejects a legitimate row that quotes a path/regex containing a backslash. It also means the S086 row can never carry one, which is a content restriction the registry's own conventions do not state.

## 4. Bounded negative results (vectors searched, no defect found)

* **Duplicate row without a leading pipe** (brief item 1). Traced: `table_cells` splits on `|` regardless of a leading pipe, so `S086 | ... |` yields the same 11 cells with `r[0]=='S086'`; it *is* counted, `len(found)==2` → `EDIT-SOURCE` → correctly **rejected**. The same holds for a leading-pipe-less duplicate without a trailing pipe. No defect.
* **Quoted duplicate** `> | S086 | ... |`: `table_cells` strips `>` prefixes before splitting → counted → correctly rejected.
* **Fenced / 4-space-indented duplicate**: `visible()` drops fenced content and 4-space-indented lines → ignored → correctly *not* counted (Markdown-consistent).
* **Wrong status / wrong tier**: `r[7] != 'mined'` and `r[2:4] != ['own-work','A']` → correctly rejected (the selftest's `source-wrong-tier` / `source-rejected` mutants cover this).
* **Duplicate with an identical leading pipe** (`| S086 |`): counted → correctly rejected.
* **Gate crash on short rows**: `len(found[0]) != 11` short-circuits the `or` chain, so `found[0][7]` can never raise `IndexError` — the `except` clause need not list it. No crash path found.

## 5. Smallest in-scope remedy

One localized change to the `EDIT-SOURCE` block in `evaluate()` (plus one production-file repair for L1). No change to `EXPECTED`, the eight decisions, the evidence check, or the preregister binding.

1. **Scope to the registry table and address columns by header name (fixes F1, F4a/b/c, F6).** Parse the header row whose cells are `['id','source','kind','tier','scope','anchor','teaches','status','opened','recheck','used-by']`, require the next line to be the delimiter row, and take only the following rows up to the next blank line as registry rows. Look up `kind`/`tier`/`status` by header index instead of 2/3/7, so a legitimate column insertion/removal is not a false reject and a row whose header disagrees cannot be mis-read.
2. **Normalize the ID cell before uniqueness comparison (fixes F2).** Compare on the ID cell with `*`, `_`, `` ` `` and whitespace stripped, so a decorated duplicate counts toward `len(found) != 1`.
3. **Compare the source cell as a path set (fixes F4b, F5).** Take the text after the *first* ` — ` as the description and split the remainder on `; `, then require `EVIDENCE ∈ {path tokens}` — matching the registry's existing multi-source idiom (S085, S015, S053, S072) instead of forbidding it.
4. **Minimum content check (fixes F3).** Require the `anchor` and `used-by` cells to be non-empty and require `used-by` to reference `corpus/knowledge/structured-edit-r23.md`; require `scope` and `teaches` to be non-empty.
5. **Production repair (for L1, not this seat):** remove the blank line at `corpus/SOURCES.md:71` so rows `S065`–`S086` are inside the rendered registry table; otherwise the S086 row the gate certifies is not a rendered registry row even after (1)–(4).
6. Drop the `\`-ban, or replace it with a real cell-model rule (escaped-pipe/code-span-aware splitting), so the check stops rejecting legitimate content (F7).

Items 1–3 are the smallest set that removes the actionable accepts (F1, F2, F5) and the registry-incompatibility rejects (F4b); item 4 removes the F3 accepts; item 5 is a one-line file repair that makes the landed row a rendered registry row.

## 6. Residual risk and verification gaps

* **Nothing was executed** (NO-EXEC): no command, hash, import, subprocess or test was run. Every "gate outcome" above is a line-level trace of `visible()` → `table_cells()` → `evaluate()` against the exact source text of the target file and the landed `corpus/SOURCES.md`; the declared SHA256 was treated as supplied identity and not recomputed. The traced outcomes should be re-confirmed by one `--selftest` extension of the same mutants once execution is permitted.
* **F1's rendering claim is an inference** from the GFM table rule (blank line ends the table block; a table requires a header row *and* a delimiter row), not an executed rendering of `corpus/SOURCES.md`. The *gate-side* half (no header/delimiter requirement in `table_cells`) is read directly from the source and does not depend on the renderer.
* **Scope of this seat**: only the `EDIT-SOURCE` / S086-registry-row leg of C1. The `EDIT-EVIDENCE`, `EDIT-POLICY-SOURCE`, `EDIT-DECISION-MISMATCH` and `EDIT-LIMIT-MISSING` legs, the C2 v2 authority, and the C3 path census were not attacked here.
* **No runtime claim.** The gate is a declared-audit text check; nothing in this report asserts native prevention, effect or reading proof, and the C1 metric remains a text-contract measurement only.
* **Landed-state note:** if the S086 row's registry cell were ever reworded (for example to add the transcript index as a second source), the current rule would reject it — the S085 precedent shows that this is a live, not hypothetical, wording hazard.

Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-fxc1source
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
