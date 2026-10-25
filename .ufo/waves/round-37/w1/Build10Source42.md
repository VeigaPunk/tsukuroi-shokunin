# Build10Source42 — design item 10/12: source rows schema validator

**Axes:** operability / build. **Milestone:** independent runnable design.

**Verdict:** the registry's per-cell schema is clean (11 cells × 199 rows, valid
enums/dates/ids, all `used-by` paths resolve), so a width/vocabulary validator is
vacuous on the unchanged baseline. The non-vacuous structural defect is Markdown
table **contiguity**: rows S198 and S199 sit outside the single contiguous table
block in `corpus/SOURCES.md`. The frozen line-based census counts them (exit 0)
and cannot see the defect; the delivered validator's new `E13` check flags
exactly those two rows on the unchanged baseline and passes after the minimal
repositioning — the measured after-state.

## Check

`tools/check-source-rows-schema.py` (this seat dir) — standalone, stdlib-only,
runnable anywhere. It mirrors the frozen fleet census contract
(`scripts/sources-census.sh` E01–E12/W01–W04: 11-column width, `S\d{3,}` id,
duplicate id, duplicate URL+scope with `supersedes S###` exemption, kind
`spec|docs|paper|code|tool|dataset|talk|book|community|own-work`, tier A/B/C,
status `queued|mined|rejected`, opened ISO date ≤ today, recheck ISO/`NNd`/symbolic,
community-never-A, `used-by` existence for mined rows, W01–W04) and adds one new
check the census does not have:

- **E13** — a row-shaped line (`^\|` after 0–3 spaces) inside the `## Registry`
  section but OUTSIDE the single contiguous table block (header + separator +
  unbroken body rows). A blank or non-table line ends the GFM block, so such rows
  are invisible to any block parser/renderer while the line-based census counts
  them.

## Baseline behavior (unchanged `corpus/SOURCES.md`)

Fixture: fresh `mktemp` git repo, `git init -C`, top-level verified equal to
fixture root (`TOPLEVEL_OK_A2`) before `git add`/commit; lane `corpus/` copied
in; baseline file byte-identical to lane (`sha256 76da7e58…` both sides);
validator run with `--root` = lane root (read-only) for `used-by` resolution,
exactly as the census validates against the lane root.

Observed (`validator_exit_A3=1`):

```
…/corpus/SOURCES.md	E13	S198 row outside contiguous table block (line 205)
…/corpus/SOURCES.md	E13	S199 row outside contiguous table block (line 208)
…/corpus/SOURCES.md	C	rows 197
…/corpus/SOURCES.md	C	section-row-lines 201
…/corpus/SOURCES.md	C	contiguous-block-rows 197
```

Details: the table block spans header (line 5), separator (6) and body rows
S001–S197 (lines 7–203). Blank line 204 ends the block; S198 (line 205) and
S199 (line 208) sit after it, with the explanatory paragraph (line 206) and blank
lines between them, still inside `## Registry` (lines 3–209, `## Paths` at 210).
A block parser sees 197 rows; the line-based census sees 199. All other schema
checks pass on baseline: no E01–E12, no W01–W03, 31 W04 duplicate-URL warnings
(also carried by `fixed`).

## After state measured

`fixtures/fixed-SOURCES.md` = exact baseline with S198/S199 moved, byte-unchanged,
to directly follow S197 (lines 204–205) and the note paragraph below the table.
Row-content set identical to baseline (sorted equality True; diff shows moves
only). Observed (`validator_exit_B3=0`): exit 0, zero E-codes, `rows 199`,
`section-row-lines 201`, `contiguous-block-rows 199` — i.e. every registry row
inside the one contiguous block, all canonical checks green. Negative control
(mutated copy: 12-cell S001, duplicated S002 id) fires `E01 S001 fields=12`
and `E03 S002 duplicate id` plus the two baseline E13s, confirming the validator
is not trivially green.

## Cited sources opened this round (read-only)

- `corpus/SOURCES.md:3-6,203-210` — `## Registry` heading, 11-column header/separator,
  S197 at 203, blank 204, S198 at 205, note 206, blank 207, S199 at 208, blank 209, `## Paths` at 210.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:24-33` — code table: `E12 row-shaped source outside the ## Registry section`; `:609-627` — `in_registry` set only by `## Registry`; any `^\|` line inside the section counts as a row; only outside-section `S###` rows emit E12; `:555-567` — E11 resolves `used-by` for `mined` rows against the lane root.
- `SCORECARD.md:1798` — "SOURCES.md 199 rows (S198/S199 added, S024 unchanged; census exit 0)" (frozen census passes the baseline; the defect is unenforced).
- `SCORECARD.md:1233` — round-31 precedent: rows appended outside `## Registry` caused E12 (`exit 1`) and were fixed by moving them unchanged inside the section; S198/S199 are inside the section, so E12 does not fire on them.
- `.ufo/waves/round-13/correction/SourceContractReview.md:7-9` — "Shape: `corpus/SOURCES.md:5-6` header, 11 columns"; E12 fires only for rows outside `## Registry`; "non-pipe lines are skipped (l.609-615)".
- `.ufo/waves/round-14/repair/SourceContract.md:6-9` — 11-column contract, enum/status/recheck rules.

## Limits / provenance

- No lane/fleet/sibling repo, git/jj state, or host state touched; only writes are
  this seat dir (report, validator, fixtures) and two `mktemp` fixture repos
  (top-level verified before commit). No tools installed: `git`, `python3`
  preinstalled (recorded per RULES.md; no pacman, no host changes).
- The frozen census was not re-executed (campaign tool); its baseline exit 0 is
  evidenced by the opened SCORECARD receipt and its source logic above.
- Scope: single-file static schema; immutability cross-revision diffing and
  per-claim quote/coverage checks are other seats' items.
