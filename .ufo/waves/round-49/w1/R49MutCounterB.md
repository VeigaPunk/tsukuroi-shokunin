VERDICT: defect-found

Scope of the defect: the four mutation points M5–M8 all SURVIVE the frozen C1 pre-data battery
(`.ufo/waves/round-49/controls/battery-summary-r49-c1.jsonl`, controls K0–K6 + K-pass), because that
battery contains no fixture for a citation-free report body, a sub-300-byte body, a corrupted quote
line, or a negated README sentence. The counter itself is not defective: on every defect fixture the
pristine counter FAILs and each mutant PASSes, i.e. each mutated leg is the single detector for the
defect it ignores. A surviving mutant is a coverage finding, not permission to change the contract.

# Seat R49MutCounterB — C1-B6: mutants M5–M8 on the frozen C1 counter (round 49, w1)

## What was under test

- Counter, read from the freeze (never the mutable working tree):
  `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:tools/check-scrub-admission-r49.py`,
  sha256 `3dd52ef376e233192f955208c1132f6b0d23bbebe97dd1df75e6296f55d970a4` (recomputed from the
  lane's object store and re-verified on the scratch copy: receipt `sha256-receipts.txt`).
- Every line number below is a line of that frozen file (421 lines).
- No counter selftest is involved (the C1 counter has none); each invocation is one JSON line, ~1 s.

## Method (same shape as C1-B5)

1. Pristine counter kept at `base/check.py` (byte-identical to the frozen blob, sha256 above).
2. One mutant per copy, one textual change each, assertion that the pattern occurs exactly once;
   full diffs in receipts `mutants.diff`, mutant sha256s in `sha256-receipts.txt`.
3. Fixture pairs per mutant: (a) a CLEAN fixture where original and mutant both PASS; (b) a DEFECT
   fixture carrying exactly the defect the mutant tolerates, where the original FAILs and the mutant
   PASSes. Operational definition of "surviving mutant" is the item's: original FAIL + mutant PASS on
   the defect fixture.
4. Clean fixture: the freeze's corrected entry + `## Gate status — round 49 (GR1-GR3 admitted)`,
   the freeze SKILL.md + `## Scrub grounding — round 49 admission`, the freeze README + a naming
   sentence, and 18 synthetic report files (`fx/cohort-clean/`) plus one results entry per seat. Row
   hashes recomputed from the fixture entry: GR1 `3a2ba180…fee1`, GR2 `d42960…027f`,
   GR3 `43430a14…3232c` — identical to the three hashes the round claims, so the fixture rows are the
   frozen rows.
5. The counter reads `.ufo/waves/round-49/w1-dispatch.json` and the digest-pinned snapshots from the
   lane at `--revision`, and the freeze predates w1 dispatch. So all runs name a scratch clone of the
   lane checked out at the freeze plus one added, committed dispatch fixture:
   `/fast/scratch/hyaku/tsukuroi-r49/R49MutCounterB/fixture-repo`,
   `git rev-parse --show-toplevel` = that path (asserted before the commit),
   `HEAD = b559488cc8400cc2dc7c8f96309f4a5f1a154dbc` ("fixture-dispatch"; receipt
   `fixture-commit.txt`, the 18-task dispatch itself in `fixture-dispatch.json`). Snapshot digests are
   unaffected by that one added file, and the counter verifies them itself (all 12/29/12 quotes
   resolve on the clean fixture).
6. Runner: `drive.py` (17 summary runs, `runs.jsonl`), `capture.py` (13 full-JSON runs,
   `capture-full.jsonl`), plus 4 cross-check runs (`cross.jsonl`). All 34 invocations are reproduced
   in receipts; nothing was run against the lane working tree.

## Clean fixture baseline (both must PASS, and do)

`orig/clean` — `{"verdict":"PASS","structural_ok":1,"corr_ok":1,"quotes_ok":3,"verdicts_ok":3,
"seats_ok":18,"marks_ok":3}`, rc 0. Each mutant on the same fixture: M5/M6/M7/M8 all PASS, rc 0
(`capture-full.jsonl`).

## Results: killed 0 / survived 4

| # | one-line change (frozen file line) | clean: orig / mutant | defect fixture | orig | mutant | verdict |
|---|---|---|---|---|---|---|
| M5 | insert `return True, 'M5: citation leg neutralized'` as the first body line, after `def report_citations_ok(cache, body, row):` (line 244) — the citation leg accepts any body | PASS / PASS | D5: all six GR2 bodies carry **no** `file:line` at all (674-byte report files, prose body ≈600 B) | FAIL, `verdicts_ok 2`, note `R49RevGR2a: no file:line citation of the row sources` (all six) | PASS, `verdicts_ok 3` | **SURVIVED** |
| M6 | line 245: `if len(body.encode('utf-8')) < 300:` → `< 0:` — the 300-byte floor becomes 0 | PASS / PASS | D6: all six GR3 bodies are 133-byte reports that do cite a resolving pinned line (`read RevGR3a at scrub.c:3094`, …) | FAIL, `verdicts_ok 2`, note `R49RevGR3a: report body under 300 bytes` (all six) | PASS, `verdicts_ok 3` | **SURVIVED** |
| M7 | line 345: `sum(1 for r in ROWS if quotes[r]['quotes'] > 0 and not quotes[r]['bad'])` → drop `and not quotes[r]['bad']` | PASS / PASS | D7: entry line 27 rewritten `cmdline.c:147` → `cmdline.c:90147` (quote text untouched) | FAIL, `quotes_ok 2`, per_row GR1 `bad: ["S246 cmdline.c:90147: outside snapshot (286 lines)"]`, ok 11/12 | PASS, `quotes_ok 3` (identical `bad` list, ignored) | **SURVIVED** |
| M8 | line 319: `if name in sentence and phrase in sentence and not NEGATE_RE.search(sentence):` → drop the negation conjunct | PASS / PASS | D8: the only README name+phrase sentence is `… is not admitted round 49; the counted cohort has not finished, so the rows stay pending.` | FAIL, `marks_ok 2`, `marks={"entry":true,"readme":false,"skill":true}` | PASS, `marks_ok 3`, `marks.readme = true` | **SURVIVED** |

Exact commands (one example, all others identical modulo counter/fixtures):

```
python3 mutants/M7.py --revision b559488cc8400cc2dc7c8f96309f4a5f1a154dbc \
  --lane /fast/scratch/hyaku/tsukuroi-r49/R49MutCounterB/fixture-repo --no-base-check \
  --entry-file fx/entry-d7.md --skill-file fx/skill-clean.md --readme-file fx/readme-clean.md \
  --wave-dir fx/cohort-d7 --results-file fx/res-d7.json
```

Discussion per survivor:

- **M5** is the only mutation whose one-line form also bypasses the byte floor (an early return can
  only sit above the guards), so its scope is a strict superset of M6's. Confirmed by the cross run
  `M5/D6 = PASS` (mutant M5 also accepts the short bodies) while `M6/D5 = FAIL` (M6 does not accept
  the citation-free bodies): the mutant scopes differ in the direction expected.
- **M6** widens the floor but leaves both citation guards; `M6/D5 = FAIL` shows it still rejects
  citation-free bodies.
- **M7** removes only the `bad` conjunct; the `bad` list is still computed and still reported in the
  JSON (`per_row.GR1.quotes.bad` is identical under default and mutant), it just no longer counts.
- **M8** removes only the negation test; the sentence split and the `name`/`phrase` containment are
  untouched, so a non-negated sentence still marks true (clean fixture).

## Cross-checks (fixtures are not degenerate)

Each mutant still FAILs a defect fixture belonging to a leg it did not mutate — so the fixtures
discriminate rather than blanket-pass (`cross.jsonl`):

- `M5/D6` PASS (overlap, discussed above) — the only cross run that passes, and it is explained.
- `M6/D5` FAIL `verdicts_ok 2`; `M7/D5` FAIL `verdicts_ok 2`; `M8/D7` FAIL `quotes_ok 2`.

## Coverage finding against the frozen pre-data battery

`.ufo/waves/round-49/controls/battery-summary-r49-c1.jsonl` holds exactly 8 controls: K0 (base bytes),
K1 (corrected entry + marks, no cohort), K2 (r48 defect strings restored), K3 (`partly` binds),
K4 (two identical bodies), K5 (critics absent), K6 (results entries absent), K-pass. None of them
varies a report body's citations, a report body's length, a `**Quote.**` line, or the README negation
— the four legs M5–M8 mutate. Consequence: no committed control would have detected a regression that
removed any of these four legs, although each leg is load-bearing for the C1 predicate
(`quotes_ok == 3`, `marks_ok == 3`, and `verdicts_ok == 3` via the per-seat credit rule).

Proposed controls (the exact fixtures that kill each mutant are already in the receipts and can be
lifted into `controls/battery.py` unchanged):

- `K7` = clean fixture with the six GR2 report bodies replaced by `fx/cohort-d5/*.md` → expects FAIL
  only through `verdicts_ok` (`R49CritGR2*: no file:line citation of the row sources`).
- `K8` = clean fixture with the six GR3 report bodies replaced by `fx/cohort-d6/*.md` → expects FAIL
  only through `verdicts_ok` (`report body under 300 bytes`).
- `K9` = clean fixture with `fx/entry-d7.md` (GR1 quote line 27 `cmdline.c:147` → `cmdline.c:90147`)
  and reports re-hashed to the new GR1 section → expects FAIL only through `quotes_ok 2`.
- `K10` = clean fixture with `fx/readme-d8.md` → expects FAIL only through `marks_ok 2`.

Adding K7–K10 to the battery would kill M5–M8 respectively (mutant verdict FAIL on the added control)
and leave the existing K0–K6, K-pass verdicts unchanged; I did not run that battery edit (read-only on
lane content and the battery is frozen).

## Limits and recusals

- Nothing in the lane, the fleet repo, the operator's config, `/home/vgpnk/Projects/shokuknow` or
  `~/.omp` / `~/.agents` was written. The lane was only read (`git show`, `git clone --shared`);
  no index, jj state, hook or ref was touched. All writes landed under
  `/fast/scratch/hyaku/tsukuroi-r49/R49MutCounterB` and the seat's wave directory.
- The only git commit anywhere was inside the scratch fixture clone (`git -C <clone> -c
  user.name=fixture -c user.email=fixture@invalid`), after asserting the clone's toplevel.
- Tools installed: none. No pacman transaction, no upgrade, no PATH write.
- Free space seen: `/fast` 541 G available before the run (clone 383 M, removed at the end).
- Not done: no run against the real lane revision's dispatch (the freeze has none), and no edit of the
  frozen control battery — both are proposed above instead of sampled.
- Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49MutCounterB` removed after the receipts were copied to
  `.ufo/waves/round-49/w1/R49MutCounterB/`.

## Receipts (`.ufo/waves/round-49/w1/R49MutCounterB/`)

`mutants/{M5,M6,M7,M8}.py` (80 K), `mutants.diff`, `runs.jsonl` (17 summary runs),
`capture-full.jsonl` (13 full counter JSONs incl. `per_row` and `marks`), `cross.jsonl` (4 cross runs),
`sha256-receipts.txt` (counter, mutants, fixtures), `drive.py`, `capture.py`,
`fixture-commit.txt`, `fixture-dispatch.json`, `fx/` (clean entry/skill/README, `entry-d7.md`,
`readme-d8.md`, four results files, four cohort dirs of 18 reports each).
