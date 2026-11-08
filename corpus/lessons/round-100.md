# Round 100 lesson — tsukuroi lane

Round 100 (attempt 1; the lane's graduation round), pre-round tip
`ce73ccaf75d0279385977f03ccb35945c1cf8e07`, freeze `743ce449`. Claims: C1 (depth 8)
`tools/make-r100-bends.py` emits two component-keyed echo bends (`N12-x-echo`, `N13-y-echo`) of the
unchanged gate, and the unchanged r99 battery must move the accepted-cap echo families, with the r98
battery as the do-nothing control; C2 (freshness 9) `tools/check-registry-content-r100.py` binds
`RC-BEND-SPAN` as a label set, closing the two round-99 named capture limits, with the r99 checker as
the do-nothing control.

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

| row | source opened 2026-11-08 | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S396 (new, own-work) | `tools/make-r100-bends.py` (sha256 `7ccfe69e…`) and `tools/check-registry-content-r100.py` (sha256 `7a23a522…`) at the freeze `743ce449` | A | `"limine_version": ("999999998.9.9" if limine_version.split(".")[0] == "999999999" else limine_version)` (BYTE 2615 of the generator, one clause); `def parse_label_set` at BYTE 12134 of the checker | **admit** — the row's anchor names both N12/N13 emission sites (BYTEs 2615/3384), the label-set parser and its `TOKEN`/`SEPARATORS` pair (BYTEs 12025/12073), all measured with `bytes.find` on the pinned bytes (QUALITY 141) |
| S397 (new, docs) | https://docs.python.org/3/library/re.html (HTTP 200, 257722 bytes, sha256 `69d64759…`, footer "Last updated on Nov 08, 2026 (14:27 UTC)") | A | `If the whole string matches the regular expression pattern, return a corresponding Match` (BYTE 112171, under `id="re.fullmatch"` at BYTE 111489) | **admit** — grounds the two primitives the tokeniser relies on: `fullmatch` (whole-token match, so a suffix cannot ride along) and `\b` (word boundary; its sentence at BYTE 69787) |
| S398 (new, docs) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md (HTTP 200, 27609 bytes, sha256 `f44f3a19…`) | C | no located quote — `grep -c` for `limine_version`, `visibility_era`, `echo` and `version` prints 0/0/0/0 | **reject** — `REJECTED: the page documents config keys and states nothing about the gate's reported fields or the battery's families; flip: a v12.9.6 page that documents the JSON report contract` |

Census (frozen command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi`): before — `.ufo/waves/round-100/before/census-before-after.txt` records the command,
output and **exit 0** with **395** rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`).
After — the landed tree, recorded in the same receipt (see the round report). Rows added by tier:
two A (S396 own-work, S397 docs) and one C rejection (S398). Rows touched in place: none in the
registry table beyond the new rows' `status mined` at write time. Frontier rows advanced: the
round-99 Frontier's two named limits (the missing X/Y echo bends; the fail-closed one-span rule).

### In-place registry changes (old → new)

None — the round adds rows; no existing row's `status`, `recheck` or `used-by` changes.

## Mistakes

- **R100-X-DELTA-COUNTED-AS-FLIP** — class: `overstatement`. The X-cap echo leg is a discrimination
  *delta*, not a closure: the r98 control on `N12-x-echo` reads `unmet 104/105` with
  `failed_families [EXPLICIT-VERSION-ECHO]` (`.ufo/waves/round-100/before/dev/c1-control-N12-x-echo.json`),
  because the r96 `EXPLICIT-VERSION-ECHO` family sends the same `999999999.9.9` spelling. Only the Y
  leg is a met→unmet flip. Captured-by: QUALITY 136 ("a family that only re-answers a case the old
  roster already covered is a twin, not a boundary") plus the r99 N11-x-era precedent (A5) — the
  rule existed and the freeze applied it before the wave, not after. Fix: the declaration's target
  names the two shapes separately, and the report repeats the delta in the same sentence as the
  closure rather than counting both as closures.
- **R100-CLONE-PATH-PREFIX** — class: `harness/path`. The first clone-layout receipts for the four bend/control legs read `0/105` with every one of the 105 families in `failed_families`, because the gate path was built as `$CLONE/$ABSOLUTE_LANE_PATH` (the absolute lane path was appended to the clone root, so the gate did not exist); the canonical twin of each leg read the frozen set. Captured-by: `none` — no criterion said a leg that fails EVERY family in one layout is a harness fault before it is a verdict; this lesson adds QUALITY 142. Fix: the four runs are quarantined under `.ufo/waves/round-100/after/c1/harness-fault/` and re-run with the clone's own path (`$CLONE/.ufo/waves/round-100/before/controls/bends/<bend>.py`), and the criterion now requires that re-run before scoring.
- **R100-REGISTRY-ROW-CELL-COUNT** — class: `self-application`. The first landing commit c450cd68 added the `check-registry-content-r100` registry row with 7 of the 8 required cells (the write-scope cell missing), so at that revision the r99 checker, the r100 checker and the coverage gate all read `CANNOT_EVALUATE` (E-TABLE / E-REGISTRY-TABLE; coverage reported `tools_total 0`). It was caught by the gates at the very next measurement and repaired at 69474c55, so the freeze tip and the final landing tip are both PASS. Captured-by: the two table parsers and the coverage gate (they caught it), but `none` caught it BEFORE the commit — the row was written without running `python3 tools/check-registry-content-r100.py --root .` on the working tree. Fix: a registry-row write now runs the content checker in `--root` mode (or the coverage gate on the committed revision) before the row is committed; this lesson names the pair sweep and the removed line below.
- **R100-TOOL-WITHOUT-ROW-AT-FREEZE** — class: `state coherence`. The freeze commit `743ce449` adds `tools/make-r100-bends.py` and `tools/check-registry-content-r100.py` but not their registry rows (those land at `c450cd68`/`69474c55`), so `tools/check-registry-coverage.py --revision 743ce449` reads FAIL `missing 2` until the landing commit; both the freeze tip and the final tip are otherwise green (`PASS 165/165/165` at `69474c55`). Captured-by: the coverage gate (it names both missing tools), but no rule says a freeze commit that introduces a tool must carry its row. Fix: a commit that adds a `tools/` file adds its registry row in the same commit; the freeze can carry a presence-only row because no binding reads those rows. Disclosed raw by ExecRegistry-4 in `.ufo/waves/round-100/w1/ExecRegistry/report.md`.
- **R99-ONE-ANCHOR-TWO-MEMBERS** — class: `corpus precision` (routed R99-D3). The S395 anchor says
  "the two new `LIE_KINDS` members at BYTE 108455"; 108455 is `limine-version`
  (`grep -abo '"limine-version"' tools/limine-pin-battery-r99.py`), and `visibility-era` starts at
  108473. Captured-by: QUALITY 141 ("a Gate row, `SOURCES.md` anchor or knowledge entry that records
  a byte offset derives it with a byte-level search") — the rule is about the *unit*, not about
  giving one offset for two facts, so the narrow criterion to add is: one anchor per named fact.
  Fix: this lesson names both offsets; the S395 row is not rewritten (append-only) and its used-by
  stays as filed.
- **R99-STALE-LOG-HEADING** — class: `bookkeeping` (routed R99-D2). The round-99 LOG headings still
  read `(pending)` / `(pending-settle)` after settle. Captured-by: `none` — the append-only rule
  forbids rewriting the heading, and no criterion said "do not put a status token in a heading
  written before the status exists". Fix: LOG.md gains an append-only correction entry naming the
  two superseded headings; future LOG entries label the round only until the status is real.
- **R99-CENSUS-EXIT-OMITTED** — class: `evidence completeness` (routed R99-D4). The r99 census
  receipt recorded the before count but only the after command's exit code. Captured-by: the round
  prompt's census clause ("paste both outputs and their exit codes") — the receipt did not follow
  it. Fix: `.ufo/waves/round-100/before/census-before-after.txt` records both commands, both
  outputs and both exit codes; the after block is appended the same way.

## Routed

| item | treatment | evidence |
|---|---|---|
| R99-D2 stale LOG headings | **landed** — an append-only LOG correction entry names both superseded headings; no heading rewritten | `LOG.md` round-100 correction entry |
| R99-D3 S395 anchor, one offset for two members | **landed as a lesson note** — both offsets named here; the row stays as filed (append-only) | this lesson; `grep -abo` receipts in the report |
| R99-D4 census before exit code | **landed** — the before/after receipt records both exit codes | `.ufo/waves/round-100/before/census-before-after.txt` |
| owed `--selftest --reference` leg (r99 A6a) | carried, unchanged — not run this round; the bends prove the family assertion, not the wrapper | `claims.json` C1 limits |
| C5 always-ok ancestor survivor's compound witness | carried, unchanged — the r99 compound M07 probe stands as filed | `corpus/README.md` Frontier |
| unbound registry rows and the three r98 C2 gaps | carried, unchanged | `corpus/README.md` Frontier (round-100 addition) |

## Frontier moved this round

- The round-99 Frontier sentence "The X/Y **echo** legs have no spelling-targeted committed bend"
  is closed on the Y side by a met→unmet flip and narrowed on the X side to a one-family delta. A
  later round that wants the X leg as a flip would need a spelling no other family sends.
- "The `unique` rule is fail-closed: a registry cell that legitimately states two spans in one cell
  must be rewritten to one span; the capture's alphabet is still `N<digits>` with no space token"
  is closed: six separator/union cells bind, and the five forged classes stay closed.
- Still open, by name: the owed `--selftest --reference` leg; the blanket echo lie's
  non-attributability; the unbound registry rows; the three r98 C2 gaps (uncovered cells,
  tool+cell co-doctoring, printed-tally parsing); the r96 launcher residuals; the r93 probe
  pre-release caveat; the r89 blank/ESP/empty-label classes.

## Correction (append-only, 2026-11-08) — the 7-cell row at `c450cd68`, repaired at `69474c55`

The repair commit `69474c55` is the one that restored the 8th cell. Pair sweep, run over the
consecutive pair:
`git diff -U0 c450cd68 69474c55 -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]'`
prints exactly **1** removed line — the original `check-registry-content-r100` row, whose
`Pinned values` cell ended `the other 161 rows stay presence-only` and which therefore had no
write-scope cell; the replacement adds
`read-only; committed reads at the bound revision; --root reads a directory and writes nothing; selftest fixtures under the caller's TMPDIR`.
The gates at `c450cd68` read `CANNOT_EVALUATE` (E-TABLE line 5951; coverage E-REGISTRY-TABLE with
`tools_total 0`) and at `69474c55` read `PASS 7/7 rows 165` and `PASS 165/165 findings 0`. This
correction is append-only; the wrong row's bytes stay in `c450cd68` and are not rewritten out of
history. Recorded as `R100-REGISTRY-ROW-CELL-COUNT` above; the round report repeats it.

## Correction (append-only, 2026-11-08, after the wave's source re-measurement)

Two defects in this lesson's own Gate block, both measured by ScoutSources and ScoutFrontier:

1. **S397's located quote was a paraphrase.** The Gate cell printed `return a corresponding match
   object`; the page at BYTE 112171 reads `return a corresponding Match.` (`bytes.find` of the
   printed phrase on the fetched 257722-byte page prints -1; `match object` occurs at BYTE 57131,
   in an unrelated table cell). The cell is corrected in place to the verbatim 13-word sentence; the
   wrong bytes remain visible in the append-only commit history (`c450cd68`) and in this note.
2. **S396's anchor pairs two different units.** `BYTE 2615` is the N12 *emission clause* start;
   `BYTE 3384` is the N13 *lie literal* start, while the N13 emission clause starts at **BYTE 3365**
   (measured with `bytes.find` of each whole quoted clause: 2615 / 3365; lie literals 2634 / 3384).
   Both are true offsets, but the pair names two different constructs. The row is not rewritten
   (append-only); the corrected anchors are these, and a later wider-scope row must take S399+.
   Relatedly, S396's `teaches` says "exactly the family" (singular) where the X bend's measured
   failed set is two families; the lesson's S396 row above is read with "the family — two families
   for the X spelling — that asserts that spelling".
3. **R99-D3 check.** ScoutFrontier re-measured the two `LIE_KINDS` offsets at
   `ce73ccaf:tools/limine-pin-battery-r99.py`: `"limine-version"` at BYTE 108455 and
   `"visibility-era"` at BYTE 108473; the lesson's mistake row `R99-ONE-ANCHOR-TWO-MEMBERS` names
   both, so the routed item's lesson-note correction is in place.
