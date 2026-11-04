# E3Repairs — r71 w1 seat report (r70 routed-defect receipts: D1, D2, D3)

Leaf seat, read-only detection. Measured at the round-71 declaration
`0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e`; the lane advanced to `2959254a` during the seat (D3
records the shebang repair landing as `db58e7c9`). No lane-tree write, no mutating git command, no
commit, no delegation, no background work retained, no tool install, no pacman call, no secret read.
Scratch `/fast/scratch/hyaku/tsukuroi-r71/E3Repairs` (with the shared clone) was deleted before this
report.

## Files written (all inside the round-71 wave surface)

- `.ufo/waves/round-71/probes/E3Repairs/tallies.tsv` — 17-row figure ledger (8 columns, validated).
- `.ufo/waves/round-71/probes/E3Repairs/corrections.md` — exact append-only correction blocks.
- `.ufo/waves/round-71/probes/E3Repairs/shebang.txt` — D3 red-before/green-after transcript + r71 counter check.
- `.ufo/waves/round-71/w1/E3Repairs.md` — this report.

## D1 — stale final selftest tallies

Sweep: `grep -nE '21[0-9] cases|196 ->|196 →|214 cases'` over `PROVINCE.md`, `corpus/README.md`,
`SKILL.md`, `LOG.md`, `SCORECARD.md`, plus the r70-band adjacent figures (all in `tallies.tsv`).
7 regex-hit lines; 17 rows total.

**STALE — 3 files / 4 lines:**
- `PROVINCE.md:372` — `(212 cases, 16 labelled R70-C2)`.
- `corpus/README.md:613` — round-70 index row `selftest 196 -> 212`.
- `SKILL.md:5773-5774` — `196 → 212 cases, 16 of them labelled R70-C2`.

**FINAL:** `LOG.md:3047-3049` (`196 → 212 … 214 after the R2Reviewer repair … 212/214`);
`SCORECARD.md:5344/5352/5462/5472` (`214` and `18 R70-C2`); r69-scope figures at
`SCORECARD.md:5238/5246/5299/5311/5323`; `SCORECARD.md:5382` red-before `212/214`;
`SCORECARD.md:5481` is the r71 declared target, not a tally.

Final instrument, re-read (not re-run): `.ufo/waves/round-70/after/selftest-after.txt` last line
`TSUKUROI_CENSUS_SELFTEST: PASS (214 cases, 214 passed, 0 failed)`; `grep -c 'R70-C2'` → **18**;
red-before `.ufo/waves/round-70/probes/L1-redbefore-r70c2.txt` last line
`FAIL (214 cases, 212 passed, 2 failed)`. `LOG.md:3047-3048` records the intermediate
`196 → 212` patch exactly, which is what the three stale files still carry.

Corrections: three EOF appends, insert-only, anchors verbatim, at `PROVINCE.md` (after 373),
`corpus/README.md` (after 618), `SKILL.md` (after 5775) — all three files end at those lines, so
`git diff --numstat` reads 0 deletions. No in-place rewrite proposed.

## D2 — unbacked `79dac76c` re-run claims

Anchor (`.ufo/reports/round-70/tsukuroi.md:102-105`, fleet repo, read-only): claims a cited-receipts
re-run PASS at `79dac76c` (75 files, 42 cited paths) and `count-xs-rows-r70.py` 6/6 at `79dac76c`.

Committed receipts that do exist:
- Counter 6/6 at **`40c35ee7`**: `.ufo/waves/round-70/after/gates-at-40c35ee7.txt` (header
  `gates at revision 40c35ee7`; six `XS_ROW ok`, `XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4
  XS_SNAPSHOTS=4`, `XS_TARGET … met=1`, `rc=0`).
- cited-receipts PASS at **`50389560`**:
  `.ufo/waves/round-70/after/cited-receipts-r70-at-50389560c1d8c6fee7c0e348b4469727b4baddcf.txt`
  — `files_scanned` **74**, `cited_paths` 42, `finding_count` 0, verdict PASS, `rc=0`; committed by
  `79dac76c` (its message names the receipt).
- No committed receipt carries either run at `79dac76c`. The only committed 75-file cited-receipts
  run is round 69 at `10a01ca5`, `finding_count` **4**, FAIL
  (`.ufo/waves/round-70/probes/E3Repairs/cited-r69-at-repair2.txt`) — the likely origin of the
  "75 files" figure.

Corrected sentence (replaces report lines 102-105) is in `corrections.md`; it names
`after/gates-at-40c35ee7.txt` for the 6/6 and the 74-file `50389560` receipt, and states that no
`79dac76c` run is committed.

## D3 — shebang / documented invocation

- HEAD `0fcfca31` (the declaration) tracks `#!/usr/bin/env bash` over Python in
  `tools/count-xs-rows-r70.py`; at first observation the working tree already carried the same
  one-line fix (`#!/usr/bin/env python3`), uncommitted — measured, untouched (it was landed during
  this seat; see the last bullet).
- Documented invocation: `SKILL.md:5756` and `PROVINCE.md:371` both say
  `python3 tools/count-xs-rows-r70.py --revision <REV>`.
- Red-before, `git clone --shared` sandbox at `79dac76c`: `./tools/count-xs-rows-r70.py --revision
  79dac76c` → rc **2**; bash executes the Python body, resolving `import argparse` to ImageMagick's
  `import` (`import: missing an image filename 'argparse'`; `import: unable to grab mouse …`). One
  such direct-exec attempt blocked on the X display long enough to require cancellation (bg_9118),
  so this is not a harmless message. Green-after, same clone, one line changed: rc **0**,
  `XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4 XS_SNAPSHOTS=4`, `met=1` — exactly the documented reading.
- Fix: one line, `-#!/usr/bin/env bash` / `+#!/usr/bin/env python3`; clone `diff --stat` = 1 file,
  1 insertion, 1 deletion.
- Landing: at the declaration `0fcfca31` the lane tracked the bash shebang (the defect). During
  this seat the lane advanced to `2959254a`; `db58e7c9` ("round-71 C2: … + r70 counter shebang
  repair", blob `f500fe6b` → `c6ee21ce`) landed exactly the verified line. At lane HEAD `2959254a`
  the tracked and working-tree shebang both read `#!/usr/bin/env python3`.

## r71 counter check (item 6)

`tools/count-mp-rows-r71.py` sha256 `fa67d4deb5f01a5124120276a8571fa36c7367d9db711ceb39bc1ca6fded48bc`
(matches the frozen digest); shebang `#!/usr/bin/env python3`; `python3 tools/count-mp-rows-r71.py
--revision 0fcfca31` → `MP_NOTE absent path=corpus/knowledge/module-parameter-plane-r71.md`,
rc **128**; direct execution reads identically; `git cat-file -e 0fcfca31:…module-parameter-plane-r71.md`
→ rc **128**. Shebang correct, note absent at the declaration, as declared.

## Risks / blockers

- D3 is discharged: the one-line fix was verified in the clone and landed as `db58e7c9` during the
  seat (defect present at the declaration `0fcfca31`; fixed at lane HEAD `2959254a`).
- D2's correction is an erratum for a landed fleet-repo report; the lane cannot amend that file, so
  the corrected sentence must land in a lane append (lesson) or the next report.
- No blocker otherwise; nothing in the lane tree was modified.

STALE_TALLIES=3
CORRECTIONS=3
SHEBANG_FIXED=yes
MP_COUNTER_ABSENT_RC=128
