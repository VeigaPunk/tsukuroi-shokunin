VERDICT: defect-found

# R49RevAdjB — C2 counter review (`tools/check-adjacency-table-r49.py`)

Bytes under test: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:tools/check-adjacency-table-r49.py`
(frozen copy also at scratch `counter.py`; all line numbers below are that file). FROZEN C2 row:
`.ufo/waves/round-49/frozen/FROZEN.md` ("C2 | adjacency ..."). I did not edit the counter, the
province, the registry or any lane file. Fixture method: `git clone -q --shared <lane>` into
`/fast/scratch/hyaku/tsukuroi-r49/R49RevAdjB/fx.*`, `checkout -B master 6256760d`, one fixture
commit per mutant, `update-ref refs/remotes/origin/master`, then the frozen counter with
`--lane <fixture>`; `--province-file`/`--registry-file` overrides for the override cases. The
fixture base bytes are the round-48 base, whose registry+census make the cross-check PASS, so the
counter's own legs are isolated from the freeze-revision coupling (H4). No mutant changed line
counts except where stated, so the cross-check stayed green (`anchors_checker_rc 0`) except M1.

## Measured mutant battery (receipts in this seat's dir)

| Fixture | Mutation | Observed verdict / legs |
|---|---|---|
| M0 | frozen PROVINCE, unchanged | PASS `7/7/0/7/7 rc=0` |
| M2 | trailing space after the row's final `|` | PASS (harmless) |
| **M3** | ADJ-01 ownership cell keeps `` `../kama-shokunin/PROVINCE.md:6-16` ``; a new 8th cell carries `` `OUT-002` `` | **PASS** `bare_ranges 0`, `per_row[ADJ-01] = {bare: [], outs: ['OUT-002'], problems: []}` |
| **M4** | ADJ-01 row has no closing pipe; ownership cell holds the bare range, evidence cell holds `` `OUT-002` `` | **PASS** `bare_ranges 0` |
| **M5** | ADJ-01 ownership cell = `` `OUT-0021` `` | **PASS** `outs ['OUT-002']` |
| **M14** | anchor OUT-002 row gains a cell before Quote (`probe`); real quote moves to index 5 | **PASS** `anchors_ok 7` |
| **M17** | anchor OUT-002 pin = `` `kama-shokunin/PROVINCE.md` @ `deadbeef0000` `` | **PASS** `anchors_ok 7` |
| **M19** | anchor OUT-002 Quote = `fabricated quote not from any sibling` (+ registry quote published elsewhere in the section) | **PASS** `anchors_ok 7` |
| **M18b** | ADJ-02 row duplicated → 8 physical ADJ rows | **PASS** `adj_rows 7` |
| **M16** | ADJ-01→OUT-007 (mori) with OUT-007's ADJ cell changed to ADJ-01; ADJ-05→OUT-006 | **PASS** (recipient `kama` unchecked) |
| M1b | legal trailing empty cell on ADJ-01 | FAIL `linked_rows 6` (false FAIL) |
| M12 | anchor quote 26 whitespace tokens | FAIL `anchors_ok 6` |
| M12b | 24 words + punctuation-only token `—` (26 tokens) | FAIL `anchors_ok 6` |
| M12c | exactly 25 whitespace tokens | PASS `anchors_ok 7` |
| M8 | ADJ-01 ownership `—` (zero outs) | FAIL `linked_rows 6`, `anchors_ok 6` |
| M10 | registry `outbound` as id-keyed dict | FAIL `registry_ok 0` (false FAIL) |
| M20 | `--skip-anchors-check` | FAIL `anchors_checker_rc -1` (predicate unsatisfiable) |

Receipts: `receipt-mutants-a.json`, `receipt-mutants-b.json`, `receipt-mutants-c.json`,
`receipt-mutant-lines.json`, `receipt-probes.json`, `receipt-freeze-coupling.txt`.

## HIGH

### H1. `cs[-1]` — the ownership cell is read positionally; a trailing column hides a bare locator
`tools/check-adjacency-table-r49.py:134` `own = cs[-1] if cs else ''`. The table is never
column-resolved by header name, and the header row is never read (only `ADJ_ROW`, line 46).
Fixture input (`receipt-mutant-lines.json` key `M3`), ADJ-01 row:

```
| ADJ-01 | ... | kama | ...no endpoint diagnosis from `nvidia-smi` | `../kama-shokunin/PROVINCE.md:6-16` | `OUT-002` |
```

Command: `python3 counter.py --revision <fixture-tip> --lane <fixture>` →
`{"verdict":"PASS","adj_rows":7,"linked_rows":7,"bare_ranges":0,"anchors_ok":7,
"registry_ok":7,"anchors_checker_rc":0}`. The ownership column still carries the exact defect
class C2 removes (`QUALITY 32` bare `PROVINCE.md:N-M`), yet `bare_ranges` is 0 because the
counter looks only at the last cell. This defeats the predicate's purpose, and the same
positional read applies to the anchor table (`anc[1]`, `anc[2]`, `anc[3]`, `anc[4]` at lines
157–167).

### H2. `cells()` drops the ownership cell when the closing pipe is omitted
`cells()` (lines 81–83) is `line.split('|')[1:-1]`, which assumes a leading **and** trailing
pipe; GFM tables may omit the trailing pipe. Fixture `M4` (`receipt-mutant-lines.json` key `M4`):

```
| ADJ-01 | ... | kama | `OUT-002` | `../kama-shokunin/PROVINCE.md:6-16`
```

`cells()` returns `[..., 'kama', '`OUT-002`']` — the ownership cell is silently discarded and the
*evidence* cell becomes `own`. Observed: `PASS`, `bare_ranges 0`. This is a false PASS of the
same class as H1, reachable with ordinary Markdown. The inverse (an extra empty cell) is a false
FAIL: `M1b` appends ` |`, `own` becomes `''`, observed `FAIL linked_rows 6, anchors_ok 6`.
A trailing space after the closing pipe is harmless (`M2` PASS).

### H3. `OUT_ID` has no token boundary — a malformed id passes
`OUT_ID = re.compile(r'OUT-\d{3}')` (line 48) applied with `findall` (line 136). Fixture `M5`:
ownership cell `` `OUT-0021` `` → `outs ['OUT-002']` → `PASS`. Same for `XOUT-002` (probe
`receipt-probes.json`). A cell that names a nonexistent anchor id is counted as a correct anchor.

### H4. The frozen C2 predicate is FALSE at the freeze revision, and is coupled to C3's surface
This is the finding the L1 must decide on. The claim says the counter runs at `<REV>` with
`anchors_checker_rc == 0`, and the docstring (`check-adjacency-table-r49.py` docstring, "must
still PASS at the measured revision") treats the cross-check as a gating leg. Measured:

```
$ python3 counter.py --revision 55c07cd3... --lane <lane>
{"verdict":"FAIL", ..., "anchors_checker_rc": 1,
 "problems":["tools/check-adjacency-anchors.py rc=1: {...}"]}
$ python3 tools/check-adjacency-anchors.py --revision 55c07cd3...
{"status":"FAIL","findings":[{"id":"INBOUND-CLASSIFICATION-WRONG",
  "site":"corpus/knowledge/adjacency-anchors-r19.json:inbound[108]", ...}]}
$ python3 tools/check-adjacency-anchors.py --revision 6256760d...   -> PASS, []
$ python3 tools/check-adjacency-anchors.py --revision d7cfc273...   -> PASS, []
```

`inbound[108]` is IN-109, `target_path: tools/tsukuroi-census.sh`, `found_line: 2642`,
`classification: DRIFTED`. The freeze commit `55c07cd` is exactly the commit that edits
`tools/tsukuroi-census.sh` (`git diff --stat 6256760d 55c07cd` → `tools/tsukuroi-census.sh | 65
+++...`, which is C3's claimed surface), moving that line; the repair is the post-freeze commit
`32a85560` ("IN-109 repin 2642->2660", `git log --oneline 55c07cd..master`). So:

- C2's gate is **not reproducible on the frozen bytes**: at `55c07cd` the predicate is false.
- C2's PASS depends on a registry entry (IN-109) whose target is C3's file, so the FROZEN.md
  statement "Claims (1–3, causally separable, distinct axes)" does not hold for the C2 counter.
- The pre-data control battery hides this: K0–K3 were scored at `32a85560` (not at the freeze)
  and with `--skip-anchors-check` (`anchors_checker_rc: -1` in
  `controls/battery-summary-r49-c2.jsonl`), so no control ever exercised the coupling;
  only K-pass ran the real checker, and it ran at `32a85560`.
- At master tip `d7cfc273` the predicate does pass (`counter` legs 7/7/0/7/7, rc 0), so the
  claim can pass *if* the measurement revision is the post-repin integrated revision; it cannot
  pass at the freeze revision.

### H5. The anchor row's "pinned sibling commit, heading and quote" is shape-only
`SIB` (line 50) accepts any 12–40 hex commit; the counter never compares it to the registry's
`sibling_commit`/`sibling_blob_sha256`. Fixture `M17` replaces OUT-002's pin with
`` `kama-shokunin/PROVINCE.md` @ `deadbeef0000` `` → `PASS`, `anchors_ok 7`. Fixture `M19`
replaces the Quote cell with `fabricated quote not from any sibling` → `PASS`, because
`check-adjacency-anchors.py` only checks that the *registry* quote is published somewhere in the
province section, never that the table's Quote cell equals it. So the C2 claim text ("each
anchor's pin/heading/quote … checked") is stronger than what the two tools jointly enforce.
The heading cell is likewise only shape-checked (`HEAD`, line 51: `^`#[^`]+`$`).

## MEDIUM

### M1. Anchor-table fixed indices break under a column shift
`anc[1]`..`anc[4]` (lines 157–167). Fixture `M14` inserts a cell before Quote: the counter then
validates `` `probe` `` as the quote and never reads the real Quote/Proposition cells → `PASS`,
`anchors_ok 7`. Same class as H1, on the other table.

### M2. `registry_ok` requires one exact JSON shape
Lines 115–123: only `dict` → `reg['outbound']` → `list` of `dict` → `id: str`. A dict keyed by
id (the shape the province anchor table itself uses, and the natural one) yields an empty
registry: fixture `M10` → `registry_ok 0`, `FAIL`. A top-level list behaves the same by code
reading (line 118 `rows = reg.get('outbound') if isinstance(reg, dict) else None`). The docstring
("the round-19 JSON registry must carry the anchor's blob sha256") does not declare the list
shape. Also: duplicate ids silently overwrite (`registry[r['id']] = r`, line 122) — the round-19
checker flags duplicate *inbound* ids; this counter has no duplicate check.

### M3. `adj_rows` counts distinct ids, not rows
Line 107 `adj[m.group(1)] = cells(ln)`. Fixture `M18b` appends a copy of the ADJ-02 row:
`physical_adj_rows 8`, `adj_rows 7`, `PASS`. `adj_rows == 7` is satisfiable by a table with a
duplicated row (the duplicate also silently wins over the original).

### M4. `--skip-anchors-check` can never satisfy the predicate
Lines 185–198: `checker_rc` starts at `-1` and the predicate requires `== 0`. The docstring
advertises the flag as a control override, but a control using it is forced to `FAIL` (fixture
`M20`). The control battery's K0–K3 (`anchors_checker_rc: -1`) therefore could not have shown
the checker leg; only a fixture lane with the real checker can.

### M5. `checker_rc` is measured from the worktree script, not from `--revision`
Lines 187–189: `checker = os.path.join(lane, CHECKER)` then `[sys.executable, checker,
'--revision', rev]`. The checker script itself is not read from `rev`; editing or replacing
`<lane>/tools/check-adjacency-anchors.py` (or its `_revision` import) changes
`anchors_checker_rc` without changing the measured revision. Likewise `--province-file` does not
reach the cross-check: the checker always re-reads `PROVINCE.md` at `rev` (override reads at lines 91 and 114; checker at 187–188), so an
override-driven PASS still depends on the live revision's province/registry.

### M6. Quote word count is a whitespace-token count
Line 167 `quote = anc[4].strip('`').strip()` then `len(quote.split())`. Consequences, measured:
exactly 25 tokens passes (`M12c`); 26 fails (`M12`); a 24-word quote plus a punctuation-only
token `—` counts as 26 and fails (`M12b`). Only backticks at the cell edges are stripped, so
embedded backticks stay inside tokens; markdown emphasis tokens (`**Domain:**`) count as words.
The docstring says "<=25 words"; the implementation counts tokens, which can reject a 25-word
quote and accept punctuation as words.

## LOW / answers to the specific audit questions

- **ADJ-row regex** (`line 46`, `^\|\s*(ADJ-0\d)\s*\|`): `ADJ-7`/`ADJ-10` are not matched; a
  row indented by spaces (`  | ADJ-01 |`) is not matched (`adj_rows` drops, false FAIL, no pass
  vector). `|ADJ-01|` with no spaces is matched. Duplicate ids collapse (M3 above).
- **BARE** (`line 49`, `[A-Za-z0-9_.-]+\.md:\d+(?:-\d+)?`), probes in `receipt-probes.json`:
  - `PROVINCE.md:3-6,10-17` → `['PROVINCE.md:3-6']`: caught, but 1 instead of 2 (`bare_ranges`
    undercounts; the base-province K0's 9 is 11 ranges on inspection).
  - `` `../mori-shokunin/PROVINCE.md:6-16` `` → caught (matches after the last `/`).
  - `PROVINCE.md#L6-L16` → **not caught** (fragment locator, no colon).
  - `PROVINCE.md lines 6-16` → not caught.
  - `PROVINCE.md:6–16` (U+2013) → caught only as the single-line prefix `:6`.
  - `see .ufo/waves/x.json:3-6` → not caught (`.md`-only by design; a bare `.json:N-M` slips).
  - `KPROVINCE.md:6` → matched (substring, no token boundary) — false positive only.
- **Ownership cell index** `cs[-1]`: H1.
- **Anchor quote word count / 25-word rule**: M6.
- **Registry lookup shape**: M2.
- **`anchors_ok` with zero outs**: no defect — `a_ok = bool(outs)` (line 145) starts False;
  fixture `M8` → `linked_rows 6`, `anchors_ok 6`, with `problems: ['no OUT anchor named']`.
  Multiple OUT ids are all required (`a_ok = r_ok = False` on each failure, lines 153–181).
- **Lowercase-only digests**: `HEX64`/`HEX12` (lines 52–53) reject uppercase hex; the round-19
  checker accepts `[0-9a-fA-F]` (`tools/check-adjacency-anchors.py:40-41`), so the two tools
  disagree on a valid registry.

## Proposed counter amendments (not applied — reviewer seat)

1. Resolve columns by header name, once per table (`Ownership source` in the ADJ table;
   `Anchor/ADJ row/Sibling file @ commit/Heading/Quote` in the anchor table) and fail closed on a
   header mismatch; reject a row whose cell count differs from the header's.
2. Make `cells()` require both edge pipes (`if not line.startswith('|') or not line.endswith('|'):
   problem`) instead of silently slicing.
3. Token-bound the id regex: `(?<![A-Za-z0-9-])OUT-\d{3}(?![0-9])`.
4. Compare the anchor's pin to `registry[out]['sibling_commit']` (prefix match ≥12 hex) and the
   Quote cell to `registry[out]['quote']`, rather than shape/word-count alone.
5. Count rows, not ids (`adj_rows = number of matched lines`), and flag duplicate ids.
6. Accept `outbound` as a list *or* an id-keyed dict for `registry_ok` (and flag duplicates).
7. Either drop the `anchors_checker_rc == 0` leg from the predicate or bind the checker's
   inbound/every-leg inputs to the pre-data revision (e.g. `--registry-from <pre-data REV>`), and
   record the C2→C3 coupling in FROZEN.md instead of "causally separable".
8. Read the checker from `rev` (`git show rev:tools/check-adjacency-anchors.py` into a temp file)
   or bind its version by digest; make `--skip-anchors-check` acceptable only outside the
   predicate (e.g. `anchors_checker_rc: "skipped"` and a separate predicate), or remove the flag
   from the docstring.

## Residual risk / verification gaps

- I did not measure at a revision later than master tip `d7cfc273`; if the L1's measurement
  revision is `>= 32a85560`, H4's gate leg passes (observed at the tip) but the frozen bytes still
  fail it.
- I did not run the counter's own `--selftest` (it has none) nor the round-19 checker's
  `--selftest`; I ran the checker only in `--revision` mode (base PASS, freeze FAIL, tip PASS).
- The M19 fabricated-quote fixture publishes the registry quote in an extra line inside the
  anchor section; without that line the round-19 checker's `ANCHOR-UNPUBLISHED` would fire, so
  M19 demonstrates the table-cell gap, not a path that passes with no other change.
- The M18b duplicate-row fixture used `--province-file` to avoid a line-count shift in
  `PROVINCE.md` (which perturbs round-19 inbound records); the leg measured (`adj_rows 7` with 8
  physical rows) is independent of that.
- I did not test `--no-base-check`, the `--lane` default, or non-UTF-8 province bytes.

## Receipts

`.ufo/waves/round-49/w1/R49RevAdjB/`: `receipt-mutants-a.json`, `receipt-mutants-b.json`,
`receipt-mutants-c.json`, `receipt-mutant-lines.json`, `receipt-probes.json`,
`receipt-freeze-coupling.txt`. Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49RevAdjB/` removed on
exit; fixture repo was a `--shared` clone with commit identity `fixture <fixture@invalid>`.
