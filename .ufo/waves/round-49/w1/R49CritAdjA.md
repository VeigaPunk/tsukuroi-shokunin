VERDICT: defect-found

# R49CritAdjA — item C2-B6: cheat the C2 counter

Axes: **adjacency** (the C2 predicate), **provenance** (does the published row prove the ownership it
claims), **freeze integrity** (does the predicate hold on the bytes it names).

Bytes under test: `55c07cd3f8bff2e12117c34d57b4c618de74d85c` (freeze). Every fixture is a
`git clone --shared` of the lane checked out at the **lane tip `d7cfc273…`**, with exactly one
fixture commit; tip was used as the harness base because at the freeze revision the anchors-checker
leg already fails for an unrelated reason (finding F1 below) and would mask cheat detection.
Each fixture asserted `git -C "$D" rev-parse --show-toplevel == "$D"`; commits were made only in the
fixture with `-c user.name=fixture -c user.email=fixture@invalid`.

Commands (per fixture `$D`, tip `$T`):

```
python3 "$D/tools/check-adjacency-table-r49.py" --lane "$D" --revision "$T"                  # full
python3 "$D/tools/check-adjacency-table-r49.py" --lane "$D" --revision "$T" --skip-anchors-check   # 5 static legs only
python3 "$D/tools/check-adjacency-anchors.py" --revision "$T"                                # checker leg alone
```

Receipts: `.ufo/waves/round-49/w1/R49CritAdjA/` (variant provinces, result JSON, fixture shas).

---

## F1 (blocking, independent of any cheat): C2's predicate is FALSE at the freeze revision

```
$ python3 tools/check-adjacency-table-r49.py --revision 55c07cd3f8bff2e12117c34d57b4c618de74d85c
{"adj_rows": 7, "linked_rows": 7, "bare_ranges": 0, "anchors_ok": 7, "registry_ok": 7,
 "anchors_checker_rc": 1, ..., "verdict": "FAIL"}   rc=1
```
(receipt `R49CritAdjA/base.json`)

The checker leg fails with exactly:

```
INBOUND-CLASSIFICATION-WRONG | corpus/knowledge/adjacency-anchors-r19.json:inbound[108]
  classification DRIFTED is inconsistent: found_line is not an occurrence of evidence_quote
```
(receipt `chk.json`; `inbound[108]` is `IN-109`, `target_path tools/tsukuroi-census.sh`)

Cause, measured against the three revisions:

| rev | line of the IN-109 quote in `tools/tsukuroi-census.sh` | registry `found_line` | checker |
|---|---|---|---|
| `6256760` (round start) | 2642 | 2642 | PASS rc=0 |
| `55c07cd` (freeze) | **2660** | **2642** | **FAIL rc=1** |
| `d7cfc27` (lane tip) | 2660 | 2660 | PASS rc=0 |

`git diff --stat 6256760 55c07cd -- tools/tsukuroi-census.sh` → `1 file changed, 56 insertions(+), 9
deletions(-)`: the C3 census edit moved the line. The registry was updated **after** the freeze:
`git diff 55c07cd d7cfc27 -- corpus/knowledge/adjacency-anchors-r19.json` → 2 lines changed,
`found_line 2642 → 2660` (receipt `freeze-to-tip-registry.diff`, hunk at lines 9-10; the A3 fixture's
own registry rewrite is a separate receipt, `a3-registry.diff`).

Consequence: the frozen C2 sentence ("Counter …; predicate `… anchors_checker_rc == 0`") cannot be
true at the revision it names. Either the freeze revision must include the registry repair, or the
claim must be restated against a revision that does. The 18-seat cohort can re-read the corrected
rows; it cannot make `anchors_checker_rc == 0` at `55c07cd`.

---

## F2 (recommended fix): the five static legs are a shape test, not an ownership test

All counter line references below are `tools/check-adjacency-table-r49.py` at the freeze revision:

- `:104-112` `adj`/`anchors` are dicts keyed by id — **a later duplicate row silently replaces an
  earlier one**; duplicates are never counted or rejected.
- `:134` `own = cs[-1]` — only the **last** cell of an ADJ row is treated as the ownership cell.
- `:137` `bare += len(row_bare)` — `BARE` is searched **only in that last cell**.
- `:145-146` `a_ok = r_ok = bool(outs)` — a row is "anchored" the moment it contains one `OUT-0NN`.
- `:160-163` `SIB.fullmatch(anc[2])` — the sibling cell is checked for **shape only**.
- `:164-166` `HEAD.fullmatch(anc[3])` — the heading cell is checked for **shape only**.
- `:167-170` `quote = anc[4]…; if not quote or len(quote.split()) > 25` — the quote is checked for
  **non-emptiness and ≤25 words only**.
- `:171-181` registry legs read the **registry file**, never the table's own cells.
- `:186-192` the checker is invoked as `[sys.executable, checker, '--revision', rev]` — the
  `--province-file` override is **not** passed to it, and no `--siblings-root` is passed (the
  checker's default fleet root applies).
- `:198-200` the predicate is the conjunction of those shape counts and the checker rc.

`tools/check-adjacency-anchors.py` (checker) is registry-driven: it never parses the anchor table.
Its only table-side requirement is `_outbound_publication` (`:402-432`, called `:638-645`): some line
in the section must contain `id+registry_quote`, `id+commit`, `id+digest`, and the heading. Live
sibling bytes are compared at `:647-652` against the **registry's** `sibling`/`sibling_path`/`commit`.

---

## The three requested cheats, measured

Static legs = `adj_rows/linked_rows/bare_ranges/anchors_ok/registry_ok`; "full" includes the checker
leg. Every row below is an observed exit status, not an inference.

| # | fixture (one commit) | change | static legs | checker alone | full |
|---|---|---|---|---|---|
| A | `5d73aee3` | whole ADJ section body **and** `### Handoff checklist` replaced by 7 two-cell rows (`| ADJ-01 | \`OUT-002\` |` …) | PASS `7/7/0/7/7` | FAIL — 17×`INBOUND-CLASSIFICATION-WRONG` | FAIL rc=1 |
| A2 | `b02f5eb9` | only the table block (header+separator+7 rows) replaced by the stub, prose/checklist kept | PASS `7/7/0/7/7` | FAIL — 17×`INBOUND-CLASSIFICATION-WRONG` | FAIL rc=1 |
| A3 | `8612944a` | A2 **plus** the 17 orphaned inbound records reclassified `UNRESOLVABLE` (`evidence_quote=""`, `found_line=0`) | PASS `7/7/0/7/7` | **PASS** | **PASS rc=0** |
| B | `d761e369` | every anchor row's quote cell → `x` | PASS `7/7/0/7/7` | FAIL — 10×`ANCHOR-UNPUBLISHED` | FAIL rc=1 |
| B2 | `2de1cada` | real anchor rows kept; 10 duplicate rows appended (quote `x`, heading `` `# x` ``) | PASS `7/7/0/7/7` | **PASS** | **PASS rc=0** |
| B2neg | `47fc00ca` | B2 with the duplicates' ADJ cell set to `ADJ-99` (negative control) | `anchors_ok=0`, problem `OUT-002 points at 'ADJ-99', not ADJ-01` | — | FAIL |
| C | `12505888` | every anchor sibling cell → `` `mori-shokunin/PROVINCE.md` @ `91940fa339e3` ``, quotes left from kama/kagi/mado/… | PASS `7/7/0/7/7` | **PASS** | **PASS rc=0** |
| C2 | `cf89b966` | C, and heading cells → `` `# x` `` | PASS `7/7/0/7/7` | FAIL — 10×`ANCHOR-UNPUBLISHED` | FAIL rc=1 |
| D | `613bee63` | ADJ-01 recipient cell `kama` → `mado` (anchor/quote still kama's) | PASS `7/7/0/7/7` | **PASS** | **PASS rc=0** |
| E | `d79248a7` | `../kama-shokunin/PROVINCE.md:3-18` inserted as a **non-final** cell of every ADJ row | PASS, `bare_ranges=0` | **PASS** | **PASS rc=0** |

Receipts: `res.A.full.json`, `res2.A2.full.json`, `res3.A3.json`, `res.B.full.json`,
`res2.B2.full.json`, `res3.B2neg.json`, `res.C.full.json`, `res2.C2.full.json`, `res2.D.full.json`,
`res3.E.json`, plus the matching `chk*`/`res*.skip.json` and `PROVINCE.*.md`.

### (a) Stub table — PASSES the counter, including the checker leg after one bookkeeping step

- Static legs pass because the stub's last cell holds an `OUT` id: `own = cs[-1]` (`:134`), a 2-cell
  row is accepted, and no header/arity/column check exists.
- With the registry untouched (A, A2) the full predicate fails, but **only incidentally**: the ADJ
  table's own cells are cited evidence for 17 inbound pointers (`IN-001, IN-002, IN-003, IN-005,
  IN-006, IN-031, IN-036, IN-041, IN-044, IN-045, IN-051, IN-058, IN-059, IN-064, IN-077, IN-079,
  IN-084`), so deleting them breaks `INBOUND-CLASSIFICATION-WRONG`. No leg looks at the ADJ table.
- Reclassifying those pointers is a normal, checker-sanctioned state: the checker's own rule is
  `quote == "" and found_line == 0` ⇒ `UNRESOLVABLE` (`check-adjacency-anchors.py:741-747`). A3 does
  exactly that and the **full predicate returns PASS, rc=0**, with the entire ADJ semantics
  (trigger / retains / recipient / minimum evidence / handoff checklist) gone.

### (b) Quote cells → `x` — the 25-word check does not bind; duplicates defeat the only content leg

- The static leg accepts `x`: non-empty, 1 word (`:167-170`). `anchors_ok` stays 7.
- Replacing every row's quote is caught by the checker (B) only because `_outbound_publication`
  demands a line carrying `id + registry_quote`; that is a **different object** from the table cell.
- Keep the real rows and append fake ones (B2): the counter's last-wins dict (`:109-112`) accepts the
  fake `x`/`` `# x` `` rows while publication is satisfied by the retained real rows → **full PASS
  rc=0**. B2neg proves the duplicates are the parsed rows: changing their ADJ cell to `ADJ-99` drops
  `anchors_ok` to 0 with `OUT-002 points at 'ADJ-99', not ADJ-01`.

### (c) Wrong sibling cell — PASSES both legs

`SIB.fullmatch` (`:160-163`) only requires the shape `` `<anything>/PROVINCE.md` @ `<12-40 hex>` ``.
Neither the counter nor the checker compares that cell with `registry[out].sibling` /
`sibling_path` / `sibling_commit`; the checker's live-bytes test uses the registry fields
(`:647-652`), and the publication test needs `id+commit` and `id+digest` on *some* line — the untouched
digest list (`PROVINCE.md:137-146`) supplies them. So C (every anchor attributed to mori while the
quote is kama's/kagi's/mado's/… ) is **PASS rc=0 on both legs**: false provenance is accepted.

Practical reading: the table's sibling and quote cells are decoration; only the registry is bound.
The keep-heading/replace-sibling split (C passes, C2 fails) shows the heading is bound solely by the
publication leg, and even that is defeated by a retained duplicate row.

> **Second-order (variant D):** the ADJ table's *recipient* column is never bound to the anchor's
> sibling either. ADJ-01 can say "mado" while its only anchor is kama's, and both legs pass — the
> central proposition C2 claims to have repaired ("ownership cell names the OUT anchor whose row
> names that recipient") is not measured.

> **Second-order (variant E):** `BARE` is searched only in `cs[-1]` (`:134-137`), so a bare
> `../kama-shokunin/PROVINCE.md:3-18` in any other cell leaves `bare_ranges == 0`.

---

## Control-surface defects found while running the item's own command line

1. **`--skip-anchors-check=false` is not accepted.** The flag is `store_true` (`:211`), so the literal
   form in the seat item exits 2 with no JSON:
   `error: argument --skip-anchors-check: ignored explicit argument 'false'`.
2. **`--province-file` never reaches the checker leg** (`:186-192`). With the lane at `d7cfc27`:
   `--province-file PROVINCE.B.quotex.md` → PASS rc=0 and `--province-file PROVINCE.C.wrongsib.md`
   → PASS rc=0 (receipts `ovr.B.json`, `ovr.C.json`), i.e. the control reports PASS while judging a
   cheated province with a checker that read the lane's clean `PROVINCE.md`. A control in this form
   cannot test what it claims to test.

---

## Smallest safe correction

Fix F1 first (re-measure C2 on a revision containing `found_line 2660`; the freeze revision cannot
satisfy its own predicate). Then four local legs in `tools/check-adjacency-table-r49.py`, none of
which needs a new file or a live sibling:

1. **Reject duplicate anchor rows** while building `anchors` (`:109-112`), e.g. track
   `dup_anchors.add(id)` when `id in anchors`, and force `a_ok = r_ok = False` for every duplicated
   id. Closes B2.
2. **Bind the table cells to the registry record** — after `rr = registry.get(out)` succeeds, add:
   ```python
   exp_sib = f'`{rr.get("sibling")}-shokunin/{rr.get("sibling_path")}` @ `{str(rr.get("sibling_commit"))[:12]}`'
   if anc[2] != exp_sib: a_ok = False; row_problems.append(f'{out} sibling cell is not the registry pin')
   if quote != str(rr.get("quote", "")).strip("`").strip(): a_ok = False; row_problems.append(f'{out} quote cell differs from the registry quote')
   if anc[3].strip("`") != str(rr.get("heading", "")): a_ok = False; row_problems.append(f'{out} heading cell differs from the registry heading')
   ```
   Closes B, B2, C, C2 (the last three at the level where the table is actually read).
3. **Require the ADJ row to be a real row**: `if len(cs) != 6 or not all(cs): row_problems.append('ADJ row is not a 6-column row')`. Closes A/A3 at the table level. Scan the whole row for
   `BARE` (`BARE.findall(" | ".join(cs))`) to close E. A recipient/sibling binding for D needs a
   ruled definition for ADJ-06's "protocol integrator — … unresolved" cell; at minimum require the
   recipient cell to be non-empty and, where it is a single token, equal to `rr["sibling"]`.
4. **Make the override honest**: when `--province-file` is given and the anchors leg is enabled,
   either run the checker on the overridden bytes or return exit 2 with
   `{"error": "--province-file is not validated by the anchors-checker leg", "verdict": "FAIL"}`.
   Also accept `--skip-anchors-check={true,false}` (or document the bare flag).

With legs 1-3 on the frozen bytes, variants A/A3, B/B2, C/C2, D and E all fail; the real table still
passes (it is a 6-column row set with unique ids, registry-matching cells, no bare range in any cell).

## Not done

- Did not run either tool's `--selftest` (cost; not needed for these fixtures) — no selftest claim is
  made here.
- Did not test whether another lane gate (`SKILL.md`, the census, a doc-consistency checker) would
  catch A3; this seat measures only the C2 counter it was assigned.
- Did not touch the lane, its index or refs; only `git show` reads and read-only clone fixtures under
  `/fast/scratch/hyaku/tsukuroi-r49/R49CritAdjA` (removed after receipts were copied).
- No tool installs.
