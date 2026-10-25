# C31Ledger117 — C3 falsification, item 1/8: self-assessment mismatch repair claim

Role: UFO-FSD critic (attack the approach; the canonical checker is the only ground truth).

## Claim under attack

SCORECARD.md at tip `d06cedb`, lines 1958-1968 (accessed 2026-10-25 via `git show d06cedb:SCORECARD.md`):

> "**C3 — calibration: the self-assessment checker reports zero mismatches (all 27 fixed checks match) at the measured round-37 tip.** … After: append-only correction of the five current self-assessment count cells to the measured tip values, then the same command at the measured round-37 branch-tip revision reports `checked: 27`, `mismatches: 0`, `status: PASS`, exit 0. The frozen predicate is `mismatches == 0 && checked == 27 && exit == 0` … The checker bytes and fixed 27-check population are unchanged; only the self-assessment values may change."

## Method

Ran the unchanged checker `tools/check-self-assessment.py` (fixed checks K01-K27; docstring lines 4-6) with `--revision <REV> --repo <lane>` at four round-37 revisions. The checker reads everything through Git (`git show`/`ls-tree`/`archive`); read-only on the lane. Validation of corrections used fresh fixture repos (mktemp + `git init`, seeded from `git archive` of the lane revision; top-level verified equal to fixture root before each commit) — no lane/Git/jj write.

## Observations (all measured 2026-10-25)

| Revision | axes heading | declaring_round | checked | mismatches | status | mismatch IDs |
|---|---|---|---|---|---|---|
| `083cd0c` (round-37 declaration base) | round 35 | 35 | 27 | 5 | FAIL | K07, K08, K09, K10, K11 |
| `b8ededd` (pre-freeze C3 correction commit) | round 35 | 35 | 27 | 5 | FAIL | K07-K11 (same) |
| `89bb8af` (wave spec / pre-data control receipt) | round 35 | 35 | 27 | 5 | FAIL | K07-K11 (same) |
| `d06cedb` (HEAD, "self-assessment counts corrected to measured tree") | round 37 | 37 | 27 | 2 | FAIL | K17, K18 |

At the base, the stale self-assessment cells are in the operative axes table, SCORECARD.md:1570-1571:
- K07 depth notes: stated 55 vs observed 56 `corpus/knowledge/*.md`
- K08 `SKILL.md` lines: stated 3009 vs observed 3110 newline chars
- K09 table lines: stated 784 vs observed 839 pipe-prefixed lines
- K10 `corpus/lessons/` files: stated 46 vs observed 49
- K11 `corpus/README.md` lines: stated 256 vs observed 269

At the tip, the new round-37 capabilities table (d06cedb:1996-1997) names bare relative receipt paths:
- K17 host-census-gate row: "`scout-live.md` and `after.md`" — `after.md` resolves to nothing (the blob `.ufo/evidence/round-1-kaika/after.md` exists at the tip)
- K18 root-metadata-observer row: "`selftest-after.json`, `mode-policy-mutant.json`" — both resolve to nothing (both exist as `.ufo/waves/round-12/resumed/…` at the tip)

Conclusion: the claim's "after" state (0 mismatches at the measured round-37 tip) exists at **no** round-37 commit — the checker reports 5 at base, 5 at the correction commit, 2 at the tip. The repair is incomplete: it fixed the five stale count cells but introduced two fresh missing-path mismatches in the replacement capabilities table (the superseded round-35 rows used full paths and passed).

## Concrete fixed check with stale value at the declaration base

K07 (depth-row note count): at base `083cd0c`, SCORECARD.md:1570 states "55 notes"; observed count at that revision is 56 → mismatch, reason "depth row states 55 notes; corpus/knowledge holds 56 .md files". Same stale-value class: K08-K11.

## Correction proposals (unchanged checker, verified on fixtures)

- Base `083cd0c`: correct the five count cells in the operative axes table to measured values (56 / 3110 / 839 / 49 / 269). Fixture A (`git archive 083cd0c` → fresh repo): before 5 mismatches; after line-targeted edit → checked 27, mismatches 0, PASS, exit 0 (declaring_round 35).
- Tip `d06cedb`: additionally expand the three shorthand receipt names to full repo paths in the round-37 capabilities rows (host-census-gate: `` `after.md` `` → `` `.ufo/evidence/round-1-kaika/after.md` ``; root-metadata-observer: `` `selftest-after.json` `` → `` `.ufo/waves/round-12/resumed/selftest-after.json` ``, `` `mode-policy-mutant.json` `` → `` `.ufo/waves/round-12/resumed/mode-policy-mutant.json` ``). Fixture B (`git archive d06cedb` → fresh repo): before 2 mismatches; after edit → checked 27, mismatches 0, PASS, exit 0 (declaring_round 37) — satisfies the frozen predicate exactly.

Smallest safe correction: the two-row path expansion at the tip alone turns the measured tip into a zero-mismatch revision; no checker change (the claim itself requires unchanged checker bytes).

## Impacted axes

Calibration (C3) — the claim's counter is the checker output; falsified at all four round-37 revisions. Depth/coverage rows are the stale evidence pointers, but the failing claim is C3. No other axis impacted.

## Sources opened (access date 2026-10-25)

- `tools/check-self-assessment.py` (read; K01-K27 fixed set, exit codes, path grammar).
- `git show {083cd0c,b8ededd,89bb8af,d06cedb}:SCORECARD.md` (located quotes above).
- Lane `git log`.
- `~/.omp/agent/RULES.md` (tooling channels; no installs performed — python3/git preinstalled, no updates).

## Tooling record

No tool installed or updated (RULES.md channel order not exercised; nothing needed).

---

## Final answer

The C3 repair claim is falsified: the unchanged checker reports 5 mismatches at round-37 base `083cd0c` (K07-K11, stale counts at SCORECARD.md:1570-1571) and still 2 at tip `d06cedb` (K17/K18 from bare relative receipt paths in the new capabilities rows at :1996-1997); its "after: mismatches 0 at the measured tip" state exists at no round-37 commit. Minimal corrections: the five count cells (56/3110/839/49/269) for the base, plus expanding `after.md`/`selftest-after.json`/`mode-policy-mutant.json` to the full `.ufo/…` paths for the tip. Both verified with the unchanged checker on fresh fixtures: checked 27, mismatches 0, PASS, exit 0. The claim holds only after both edits land.
