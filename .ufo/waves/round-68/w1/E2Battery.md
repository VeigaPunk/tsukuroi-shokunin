# E2Battery — C1 strict counter and battery (r68 w1)

Lane `tsukuroi-shokunin`, base `42400ec6`, round 68 wave w1. The frozen note
`corpus/knowledge/linux-v73-pinwatch-r68.md` is absent, so the instrument
precedes the data it measures; a sibling's draft note (`drafts/c1/note.md`)
appeared after the fixtures and is read below as evidence only.

## Files written (only these)

- `.ufo/waves/round-68/drafts/c1/count-rw-r68.py` — sha256
  `b93f5912d91be4787c5c595e10f5a15501cd64e9af6cd87916b28cd350438458`.
- `.ufo/waves/round-68/drafts/c1/E2-report.md` — contract, battery, the five
  defects found while building it, declared deviation, limits.
- `.ufo/waves/round-68/probes/c1-battery.txt` — receipt (264 lines), sha256
  `5ff7a184334ee624ca074fec5483e3b427f16292192b0e295fadfff47cffc260`.

## Behaviour

`python3 count-rw-r68.py <note.md>` prints `RW_ROWS=<n>`, `LAYOUT=<8|none>` and
one `REJECT line=… id=… reason=… detail=…` per rejected row; rc 0 measured,
rc 2 when the path is not a regular file (no `RW_ROWS`, so an absent note cannot
read as 0). Read-only over the single argv path, stdlib only,
`sys.dont_write_bytecode = True`, compiles clean under `-W error::SyntaxWarning`.

Strict clauses: outside a ``` / ~~~ fence; column-0 `| RW<n> | ` in the frozen
grep's own spacing (the strict count is therefore a subset of the frozen count);
belongs to a table (a `|---|` separator above it in the pipe block, so a
row-shaped prose line is not a row); exactly 8 data cells with `\|` protected;
ids distinct by numeric value (`RW7`/`RW007` collide); evidence cell (8th, last)
non-empty and not a placeholder.

## Evidence

- 21 fixtures: 5 red, 1 control, 1 do-nothing empty note, 14 extra controls.
- `battery_should_fail_accepted=5 of 5 red/5 control=6` (reds observe
  0/1/3/0/5 against the control's 6); `extra_controls=14/14`,
  `failed_fixtures=0`.
- Frozen grep over the same fixtures: `frozen_grep > strict` on 11 of them — the
  duplicate, fenced, empty-evidence, lone-row, numeric-duplicate,
  invalid-then-valid, placeholder, fence-mismatch, nine-cell, A4-boilerplate and
  stray-pipe fixtures — and equal on the rest, including the control, the
  two-table and the RW1–RW6 rehearsal at 6. `strict > frozen_grep` never occurs
  (`violations=0`).
- `t-a4-boilerplate` is R1Attack's A4 falsifier (six boilerplate rows the frozen
  grep accepts at 6); the counter reads 0 on it.
- Live draft note (`note.md`, sha `1d2a4d8d…`): `awk -F'|'` gives NF=10 on all
  six RW rows, grep gives 6, the counter gives `RW_ROWS=6`, `LAYOUT=8`, no
  REJECT — both instruments agree on the real shape.
- Edge probes: absent note rc 2, no argv rc 2, directory rc 2, two runs
  byte-identical, a run writes no file and no `__pycache__`.

## Defects found and closed while building (all in `E2-report.md` §defects)

1. A tautological id-cell rule (deleted; `m-id-mismatch` repointed to
   `m-two-tables`).
2. An anchor looser than the frozen grep (tightened; `s-tight-cells` added).
3. A ninth-cell false accept that let a stray-pipe row with a blank evidence cell
   pass by testing the verdict cell instead (tolerance removed — M1Mutation's
   probe on this counter found it; `p-nine-cells` / `v-stray-pipe` now pin 0,
   `u-no-trailing-pipe` pins the item's `NF == 9` reading at 1).
4. A `SyntaxWarning` from the docstring (fixed; SC1Scribe saw it on
   `d14c0031…`, gone at `fa0d866d…`).
5. A receipt build that lost its cwd (rebuilt; final rc 0).

## Risks / blockers

None blocking. Three things the integrator should know:

1. The note must keep the shape it already has in the draft: 8 data cells,
   `evidence` last, `| RW<n> |` at column 0, a `|---|` separator above the rows,
   ids RW1…RW6 distinct, every evidence cell filled (a `—` or `-` is a blank),
   no unescaped pipe inside a cell. A row of any other shape prints
   `REJECT reason=SHAPE`, never a silent pass.
2. The counter is stricter than the claim's frozen grep by design. On a landed
   note that meets the contract both read 6; if they disagree, read the `REJECT`
   lines before trusting either.
3. The header row's cell names are not validated, so the note should keep
   `id | row-kind | fact | v7.2 anchor | v7.3 anchor | verdict | applicability |
   evidence`.

Verification for the main agent: run the counter on the landed note and compare
with `grep -cE '^\| RW[0-9]+ \| '` on the same bytes; run the counter on an
absent path and confirm rc 2 with no `RW_ROWS` line.
