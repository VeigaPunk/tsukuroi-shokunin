# r70 routed-defect corrections — D1 / D2 / D3 (round 71, seat E3Repairs)

Read-only detection. No lane-tree byte was written by this seat; every block below is a proposed
append-only correction the L1 lands in the lane's next amendment. Anchors are verbatim at lane
HEAD `0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e` (round-71 declaration), line numbers as of that
revision.

## Final selftest evidence (the figure every D1 correction binds to)

- Final line: `TSUKUROI_CENSUS_SELFTEST: PASS (214 cases, 214 passed, 0 failed)` —
  `.ufo/waves/round-70/after/selftest-after.txt` (last line).
- Label count: `grep -c 'R70-C2' .ufo/waves/round-70/after/selftest-after.txt` → **18**.
- Red-before: `TSUKUROI_CENSUS_SELFTEST: FAIL (214 cases, 212 passed, 2 failed)` —
  `.ufo/waves/round-70/probes/L1-redbefore-r70c2.txt` (last line, twice); `grep -c 'R70-C2'` → 2,
  the two repaired cases.
- Intermediate patch tally (why 212 and 16 appear): `Selftest 196 → 212 cases with E1XfsArm's
  patch, 214 after the R2Reviewer repair` — `LOG.md:3047-3048`. The two repair cases are the
  dotfile-counts and symlink-not-counted cases (`LOG.md:3048-3049`), which take the label count
  from 16 to 18.

## D1 — stale final selftest tallies: 3 sites / 4 lines

Sweep: `grep -nE '21[0-9] cases|196 ->|196 →|214 cases'` over the five named files, plus adjacent
r70-band figures (full ledger: `tallies.tsv`, 17 rows).

| Site | Anchor | Class |
|---|---|---|
| `PROVINCE.md:372` | `(212 cases, 16 labelled R70-C2)` | **STALE** |
| `corpus/README.md:613` | `selftest 196 -> 212` | **STALE** |
| `SKILL.md:5773-5774` | `196 → 212 cases, 16 of them labelled R70-C2` | **STALE** |
| `LOG.md:3047-3049` | `196 → 212 … 214 after the R2Reviewer repair … 212/214` | final |
| `SCORECARD.md:5344,5352,5472,5462` | `214 cases … 18 R70-C2` / `selftest 214` | final |

`SCORECARD.md:5246`, `:5238`, `:5299`, `:5311`, `:5323` carry the r69 figure **196** in r69 scope
and are final for that round; `:5382` is the r70 red-before `212/214`; `:5481` is the r71 declared
target (`214 → N >= 217`), not a tally.

### D1-a — PROVINCE.md (append after line 373 = EOF; insert-only)

Anchor, verbatim (`PROVINCE.md:372`):

```
`bash tools/tsukuroi-census.sh --selftest` (212 cases, 16 labelled `R70-C2`) plus the live line for the arm, at
```

Append, verbatim:

```
Correction appended 2026-11-04 (round 71, routed r70 D1; append-only, the paragraph above is not
rewritten): its `(212 cases, 16 labelled R70-C2)` is the intermediate E1XfsArm patch tally that
`LOG.md:3047-3048` records (196 → 212, then 214 after the R2Reviewer repair), not the final
instrument. Final: `TSUKUROI_CENSUS_SELFTEST: PASS (214 cases, 214 passed, 0 failed)` with **18**
`R70-C2` receipt lines (`.ufo/waves/round-70/after/selftest-after.txt`; `SCORECARD.md` "Round 70 —
measured outcome"); pre-repair state `FAIL (214 cases, 212 passed, 2 failed)`
(`.ufo/waves/round-70/probes/L1-redbefore-r70c2.txt`).
```

### D1-b — corpus/README.md (append after line 618 = EOF; insert-only)

Anchor, verbatim (`corpus/README.md:613`):

```
| `../tools/tsukuroi-census.sh` | The verdict-neutral `XFS xfs-stats` arm (mount-table sources, sysfs presence, stats parse, error/log counts, partition invariant); selftest 196 -> 212 |
```

Append, verbatim:

```
Correction appended 2026-11-04 (round 71, routed r70 D1; append-only, the round-70 index above is
not rewritten): the `selftest 196 -> 212` cell is the intermediate E1XfsArm patch tally that
`LOG.md:3047-3048` records, not the final instrument. Final:
`TSUKUROI_CENSUS_SELFTEST: PASS (214 cases, 214 passed, 0 failed)` with **18** `R70-C2` lines
(`.ufo/waves/round-70/after/selftest-after.txt`).
```

### D1-c — SKILL.md (append after line 5775 = EOF; insert-only)

Anchor, verbatim (`SKILL.md:5773-5774`):

```
privilege, no xfsprogs call, never a rollup or exit-code term). The census selftest grows 196 → 212 cases,
16 of them labelled `R70-C2`. The registry gains one row for `tools/count-xs-rows-r70.py`; the arm lives
```

Append, verbatim:

```
Round-71 correction (append-only, routed r70 D1; the round-70 paragraph above is not rewritten):
its "census selftest grows 196 → 212 cases, 16 of them labelled `R70-C2`" is the intermediate
E1XfsArm patch tally that `LOG.md:3047-3048` records, not the final instrument. Final:
`TSUKUROI_CENSUS_SELFTEST: PASS (214 cases, 214 passed, 0 failed)` with **18** `R70-C2` case lines
(`.ufo/waves/round-70/after/selftest-after.txt`; `SCORECARD.md` "Round 70 — measured outcome").
```

No in-place rewrite is proposed anywhere: all three blocks insert new lines at EOF (PROVINCE 373
lines, README 618, SKILL 5775 at HEAD), so `git diff --numstat` reads 0 deletions.

## D2 — the report's unbacked `79dac76c` re-run claims

Anchor, verbatim (`.ufo/reports/round-70/tsukuroi.md:102-105`, fleet repo; read-only):

```
Receipt chain, so every receipt names the revision it measured: gate battery at the measured revision `40c35ee7`
(`after/gates-at-40c35ee7.txt`), results revision `50389560` (`w1-results.json`), cited-receipts PASS at
`50389560` (receipt committed in `79dac76c`) and re-run PASS at `79dac76c` (75 files, 42 cited paths, 0
findings); `count-xs-rows-r70.py` re-ran 6/6 at `79dac76c`.
```

What actually exists (all committed):

| Claim | Committed receipt | Reading |
|---|---|---|
| `count-xs-rows-r70.py` 6/6 | `.ufo/waves/round-70/after/gates-at-40c35ee7.txt` (header `gates at revision 40c35ee7`; lines 4-11) | six `XS_ROW ok`; `XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4 XS_SNAPSHOTS=4`; `XS_TARGET … met=1`; `rc=0` — measured revision **40c35ee7**, not 79dac76c |
| cited-receipts PASS at the results revision | `.ufo/waves/round-70/after/cited-receipts-r70-at-50389560c1d8c6fee7c0e348b4469727b4baddcf.txt` (committed by `79dac76c`, whose message names it) | revision `50389560…`, `files_scanned` **74**, `cited_paths` 42, `finding_count` 0, verdict PASS, `rc=0` |
| re-run at `79dac76c` (75 files) | none | no receipt in `.ufo/waves/round-70` records revision `79dac76c` for either tool; the only committed 75-file cited-receipts run is round 69 at `10a01ca5`, `finding_count` 4, FAIL (`.ufo/waves/round-70/probes/E3Repairs/cited-r69-at-repair2.txt`) |

Corrected sentence, verbatim (replaces lines 102-105; the 74-file figure is the receipt's own):

```
Receipt chain, so every receipt names the revision it measured: gate battery at the measured revision `40c35ee7`
(`after/gates-at-40c35ee7.txt`: `python3 tools/count-xs-rows-r70.py --revision 40c35ee7` -> 6/6,
`XS_SOURCES=4 XS_SNAPSHOTS=4`, `met=1`, rc 0), results revision `50389560` (`w1-results.json`), and the
cited-receipts PASS at `50389560` — receipt committed in `79dac76c`: `files_scanned` 74, `cited_paths` 42,
`finding_count` 0, rc 0 (`after/cited-receipts-r70-at-50389560c1d8c6fee7c0e348b4469727b4baddcf.txt`). No
counter or cited-receipts run at `79dac76c` is committed; the only committed 75-file cited-receipts run is
round 69 at `10a01ca5` (`finding_count` 4, FAIL, `probes/E3Repairs/cited-r69-at-repair2.txt`).
```

## D3 — shebang / documented-invocation mismatch

One-line fix (full transcript in `shebang.txt`):

```
tools/count-xs-rows-r70.py:1
-#!/usr/bin/env bash
+#!/usr/bin/env python3
```

Red-before at `79dac76c` in a `git clone --shared` sandbox: direct execution → rc **2**, bash
resolves the Python body's `import` to ImageMagick's `import` (`import: missing an image filename
'argparse'`; `import: unable to grab mouse …`) — one such attempt blocked on the X display and had
to be cancelled. Green-after, same clone, one line changed: rc **0**,
`XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4 XS_SNAPSHOTS=4`, `met=1` — exactly the documented
`python3 tools/count-xs-rows-r70.py --revision <REV>` reading. At the declaration `0fcfca31` the
lane still tracked the bash shebang; the working tree already carried the one-line fix, and during
this seat the lane advanced to `2959254a` with `db58e7c9` ("round-71 C2: … + r70 counter shebang
repair", blob `f500fe6b` → `c6ee21ce`, 1 insertion / 1 deletion) landing it. The fix is therefore
verified and landed; this seat wrote no lane bytes.

## Verification after landing

```
git -C <lane> show <landing>:tools/count-xs-rows-r70.py | head -1   # #!/usr/bin/env python3
<lane>/tools/count-xs-rows-r70.py --revision 79dac76c               # rc 0, XS_ROWS=6 … met=1
git -C <lane> diff --numstat <base> <landing> -- PROVINCE.md corpus/README.md SKILL.md  # 0 deletions
```
