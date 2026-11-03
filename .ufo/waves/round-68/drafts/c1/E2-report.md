# E2Battery — round-68 C1 strict counter and should-fail battery

UTC 2026-11-03T22:45Z · lane `tsukuroi-shokunin` · base `42400ec6` · wave w1
· authority: SCORECARD.md "Round 68 — declaration" row C1 and the item text.

Frozen note `corpus/knowledge/linux-v73-pinwatch-r68.md`: absent at write time
(counter rc 2, no `RW_ROWS` printed). Named battery fixtures a–f are timestamped
`2026-11-03 19:34:41 -0300`; a sibling's **draft** note first appeared
`19:38:33 -0300`, after them. The draft is read below as evidence, not as the
frozen artefact.

## Artefacts

| path | sha256 |
|---|---|
| `.ufo/waves/round-68/drafts/c1/count-rw-r68.py` | `b93f5912d91be4787c5c595e10f5a15501cd64e9af6cd87916b28cd350438458` |
| `.ufo/waves/round-68/probes/c1-battery.txt` | `5ff7a184334ee624ca074fec5483e3b427f16292192b0e295fadfff47cffc260` |

Counter: stdlib only (`sys`, `argparse`, `re`, `pathlib`), one markdown path from
argv, writes nothing, `sys.dont_write_bytecode = True`, compiles clean under
`-W error::SyntaxWarning`. stdout is `RW_ROWS=<n>`, `LAYOUT=<8|none>`, then one
`REJECT line=… id=… reason=… detail=…` per rejected row; rc 0 measured, rc 2 when
the path is not a regular file.

## The contract the note has to meet

```
| id | row-kind | fact | v7.2 anchor | v7.3 anchor | verdict | applicability | evidence |
|---|---|---|---|---|---|---|---|
| RW1 | S138 | ... | a9433bb0… | 2750c11a… | CHANGED | ... | before/src/SHA256SUMS S138 |
```

Accepted iff: outside a ``` / ~~~ fence; column-0 `| RW<n> | ` in the frozen
grep's own spacing; a `|---|` separator above it in the same pipe block; exactly
8 data cells (`\|` protected, so evidence may quote a pipeline); id distinct by
numeric value (`RW7`/`RW007` collide); evidence cell (the 8th, last) non-empty
and not a placeholder (`-`, `—`, `…`, `TBD`, `n/a`, `none`).

## Battery (21 fixtures: 5 red, 1 control, 1 do-nothing, 14 extra)

```
a-header-only               0  0  red      PASS   b-duplicate-id              1  1  red   PASS
c-fenced-rows               3  3  red      PASS   d-prose                     0  0  red   PASS
e-empty-evidence            5  5  red      PASS   f-control                   6  6  control PASS
g-absent                    0  0  null     PASS   h-escaped-pipe              1  1  extra PASS
i-indented                  0  0  extra    PASS   j-lone-row                  0  0  extra PASS
k-duplicate-numeric         1  1  extra    PASS   l-first-invalid-then-valid  1  1  extra PASS
m-two-tables                6  6  extra    PASS   n-placeholder-evidence      0  0  extra PASS
o-fence-mismatch            0  0  extra    PASS   p-nine-cells                0  0  extra PASS
r-rehearsal                 6  6  extra    PASS   s-tight-cells               0  0  extra PASS
t-a4-boilerplate            0  0  extra    PASS   u-no-trailing-pipe          1  1  extra PASS
v-stray-pipe                0  0  extra    PASS   battery_should_fail_accepted=5 of 5 red/5 control=6
extra_controls=14/14 failed_fixtures=0
```

Sensitivity against the frozen predicate, same 21 fixtures: `frozen_grep >
strict` on `b-duplicate-id` (6>1), `c-fenced-rows` (6>3), `e-empty-evidence`
(6>5), `j-lone-row` (1>0), `k-duplicate-numeric` (2>1),
`l-first-invalid-then-valid` (2>1), `n-placeholder-evidence` (1>0),
`o-fence-mismatch` (2>0), `p-nine-cells` (1>0), `t-a4-boilerplate` (6>0),
`v-stray-pipe` (1>0); equal on the other ten, including `f-control`,
`m-two-tables`, `r-rehearsal` and `u-no-trailing-pipe` at 6/6/6/1. Subset
ordering over all 21 fixtures: `strict > frozen_grep` never occurs
(`violations=0`) — the strict count can only be smaller than the frozen count.

`t-a4-boilerplate` is R1Attack's own A4 falsifier (six boilerplate rows with no
located anchor, 4 data cells) that the frozen grep accepts at 6; the counter
reads 0 on it. That is the instrument answering the attack the predicate cannot.

## Live draft note (read-only, not the frozen artefact)

```
$ sha256sum .ufo/waves/round-68/drafts/c1/note.md
1d2a4d8d78a0c1d0a704d887b26df4cc4e0c5f8fc979062f1fc7602fa30bbd8b
$ grep -cE '^\| RW[0-9]+ \| ' note.md            -> 6   rc 0
$ awk -F'|' '/^\| RW[0-9]+ \| /{print NR": NF="NF}' note.md -> 30..35 all NF=10  rc 0
$ python3 count-rw-r68.py note.md                -> RW_ROWS=6, LAYOUT=8, no REJECT  rc 0
```

Both instruments agree at 6 on the 8-column draft. M1Mutation's earlier read
(`RW_ROWS=5`, `LAYOUT=mixed`) measured a superseded revision of the draft whose
cells carried unescaped pipes; the current draft has none (`grep -c '\\|'` → 0).

## Fixtures that did not behave as expected (and what changed)

1. **`m-id-mismatch` (first build): observed 1, expected 0.** The rule "the id
   cell equals the anchor token" is tautological — R2 consumes `| RW<n> |` as
   the first cell, so the two cannot disagree. The rule was dead weight and was
   deleted; the fixture was repointed to `m-two-tables` (3+3 valid rows under two
   headings, expected 6), testing that counting does not stop at one block.
2. **Anchor looser than the frozen grep.** `^\| RW([0-9]+) \|` accepted
   `| RW1 |x`, which the frozen grep (`… \| ` with a trailing space) misses, so
   the counter could report more rows than the predicate it qualifies. The anchor
   now requires the grep's spacing (`(?= |$)`); `s-tight-cells` pins it at 0 and
   the subset ordering check is a permanent block in the receipt.
3. **Ninth data cell was a false accept (found by M1Mutation's probe on this
   counter).** My first version accepted a 9-cell row with evidence taken
   "4th-from-last" (the item's parenthetical). In an 8-column table a ninth cell
   means an unescaped pipe or an extra column, and the 4th-from-last cell is then
   the verdict — so a row with a stray pipe and a **blank** evidence cell passed.
   The tolerance was removed: exactly 8 data cells, evidence last (the note's own
   header at `note.md:28` is 8 columns, evidence last). `p-nine-cells` and
   `v-stray-pipe` now pin `RW_ROWS=0` with `REJECT reason=SHAPE`, and
   `u-no-trailing-pipe` pins the item's `NF == 9` reading: the same 8-cell row
   without its trailing pipe (9 raw fields) counts, `LAYOUT=8`.
4. **`SyntaxWarning: "\|" is an invalid escape sequence`** from a docstring edit
   (the module docstring is not raw). Fixed to `\\|`; the counter compiles clean
   under `-W error::SyntaxWarning`. SC1Scribe reported this on revision
   `d14c0031…`; it is gone at `fa0d866d…`.
5. **A first receipt build lost its cwd** (an inner `cd` into the fixture dir),
   so its `VERDICT` block printed `./battery.sh: command not found`. Rebuilt with
   absolute paths and a subshell; the current receipt's final rc is 0, and that
   earlier variant is not a value to quote.

No fixture failed in the final state.

## Declared deviation from the item's literal text (shape only)

The item says "NF == 9 when split on `|`" and "the 4th-from-last data cell, which
the note's table places as the evidence column", while the layout it names has 8
cells with evidence last. Reconciliation, declared rather than guessed:

- `| a | … | h |` splits into 10 raw fields; the same row without the trailing
  pipe splits into 9 (the item's NF). Both are the same 8-column row, so the rule
  is the data-cell count, never the raw field count.
- The 9-cell reading is **rejected**, with the reason above (it can only be a
  formatting defect in an 8-column table, and it tests the verdict cell as
  evidence). The counter therefore prints `LAYOUT=8` or `LAYOUT=none`, and any
  other cell count is `REJECT reason=SHAPE` — a mismatch is loud, never a silent
  zero.

## Limits (recorded, not smoothed)

1. Evidence is checked for presence only. The counter cannot tell a sha pair from
   the word `yes`; binding evidence to bytes is the reviewer's job.
2. Any table block with a separator above counts, wherever it sits; the table is
   not required to sit under a particular heading.
3. The header row is not validated against the 8 column names — an 8-cell row
   under a differently worded header still counts.
4. A note that genuinely used nine columns (evidence 4th-from-last) would read 0
   with `REJECT reason=SHAPE` on every row. That reading was rejected on purpose;
   docstring R4 states the trade and the note's own header settles it.
5. Rows indented by any whitespace are rejected, matching the frozen grep's
   column-0 anchor, so the two instruments stay ordered.

## Reproduction

```
python3 .ufo/waves/round-68/drafts/c1/count-rw-r68.py <note.md>   # RW_ROWS, LAYOUT, REJECTs
python3 .ufo/waves/round-68/drafts/c1/count-rw-r68.py <absent.md> # rc 2, no RW_ROWS
grep -cE '^\| RW[0-9]+ \| ' <note.md>                             # frozen predicate
```

Fixture bodies are disposable (scratch); `probes/c1-battery.txt` carries their
sha256s and a one-line shape each, so the battery is reproducible from that file
alone.
