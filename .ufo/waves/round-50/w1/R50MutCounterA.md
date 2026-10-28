VERDICT: supports

# R50MutCounterA — C1-B5, mutation test of the frozen C1 counter

Item C1-B5. Bytes under test: `tools/check-scrub-admission-r50.py` at FREEZE
`8029cdba1049df25632c91a23c8db4eefb54be5f`, blob sha256
`0af0e679ee82d608d6278d2575391b1a7dd53af49099e962349bddac35f333db` (22170 B), read with
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <FREEZE>:tools/check-scrub-admission-r50.py`.
No lane byte was written; the only lane writes are this report and the receipts beside it.
No tool installs, no network, no pacman; `python3` (stdlib) only.

## Result

Four mutants, one per copy, each run against a clean K-pass fixture set and against the set
carrying the defect that mutant lets through. **21/21 runs scored as designed; 4/4 mutants
survived.** Every surviving mutant stayed PASS on the clean set and flipped the designed defect
from FAIL (pristine) to PASS (mutant) — so each of the four legs is the *sole* catcher of its
defect and none is redundant with another leg. The counter's predicate is therefore carried by
exactly the rules its docstring names, and no leg is decorative.

Verdict `supports` means: no leg of the C1 counter is bypassable without changing its verdict, and
no leg was found redundant. The item's convention "original FAIL, mutant PASS = surviving mutant =
defect" is read as *the defect class the removed rule guards* — the survival is what proves the
guard is load-bearing, not a bug in the counter.

## Fixtures (synthetic, built from frozen bytes)

All under `/fast/scratch/hyaku/tsukuroi-r50/R50MutCounterA/work/`, removed at the end of the seat;
the scripts that build them are receipts (`mut.py`, `probes.py`, `probes2.py`, `battery-frozen.py`,
`counters/*.py`). The cohort/results/dispatch/marks builder is
`.ufo/waves/round-50/controls/battery.py` read **at FREEZE** (`git show`, imported from scratch as
`battery-frozen.py`), so the fixtures reproduce the frozen control K-pass exactly.

Every fixture dir holds: `entry.md` = freeze entry + `## Gate status — round 50 (GR1-GR3 admitted)`,
`skill.md` with `## Scrub grounding — round 50 admission`, `readme.md` with the `admitted round 50`
sentence, `dispatch.json` (18 tasks, `reviewer`/`critic` by seat), `results.json`
(18 × `{name, agent, output:"done"}`), `wave/` = 18 reports (`ROW GR<n> VERDICT: holds` /
`SECTION SHA256: <row hash>` / ≥300 B body citing two row sources). Each fixture entry was
re-hashed with `--section-hash` and equals the three frozen row hashes
(GR1 `3a2ba18…`, GR2 `a2e955c…`, GR3 `43430a1…`) — receipt `fixture_entry_hashes` in
`mutation-r50-c1-b5.json` — so the fixtures sit on the frozen row bytes, not on look-alikes.

| Fixture | The one defect it carries |
|---|---|
| `clean` | none (K-pass) |
| `D1-partly` | `R50CritGR2b` line 1 `ROW GR2 VERDICT: partly` |
| `D2-padded` | `R50RevGR2a` and `R50CritGR2a` byte-identical bodies, second padded `'   \n\n  '` |
| `D3-noresults` | `results.json` = `{"results": []}` (18 reports still on disk) |
| `D4-stalehash` | all six GR2 reports carry `SECTION SHA256: e519cbe421a46569310d967cbfb90e905e3c101549ba1f61a7f21ab4c50a7521` — the real pre-correction GR2 hash recorded by frozen control K2 |
| `P1-allpartly` | all six GR3 seats bound `partly` |
| `P2-identical` | two GR2 bodies byte-identical, no padding |
| `P3-emptyoutput` | `R50CritGR1b` results entry `output: ""` |
| `P4-contradict` | `R50CritGR2c` body gains `… ROW GR2 VERDICT: fails …` |

## Mutants

Each mutant is the frozen text with exactly ONE anchored replacement (anchor count asserted == 1
before writing; `mutants[].anchor_count` in the receipt). Line numbers are the pristine copy's.

| # | Mutation | Anchor (pristine.py) | sha256 of mutant |
|---|---|---|---|
| M1 | drop the blocking rule | `if v in ('partly','fails'): blocking.append(seat); continue` deleted (415-417) | `891b4a7e…` |
| M2 | drop the whitespace-collapsing distinct-bodies check | `norm_body = '\n'.join(ln.rstrip() …)` + hash of it → `hashlib.sha256((body or '').encode())` (426-427) | `75483403…` |
| M3 | drop the results.json seat check | `hits = [r for r in results …]` … `'no completed output'` deleted (323-329) | `46d2abd0…` |
| M4 | accept any 64-hex report hash | `if h != hashes.get(row):` → `if not re.fullmatch(r'[0-9a-f]{64}', h or ''):` (418-420) | `734c93fc…` |

Diffs: `m1.diff` (12 lines), `m2.diff` (12), `m3.diff` (16), `m4.diff` (13) — all in this
directory. The distinctness *comparison* (`distinct = len(bodies) == len(credited)`, line 429) and
`row_ok` (430) are untouched by every mutant, so each mutation removes exactly one named rule.

Command shape for every run (identical except the counter path and fixture dir):

```
/usr/bin/python3 <counter> --revision 8029cdba1049df25632c91a23c8db4eefb54be5f \
  --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --no-base-check \
  --entry-file <fx>/entry.md --skill-file <fx>/skill.md --readme-file <fx>/readme.md \
  --dispatch-file <fx>/dispatch.json --results-file <fx>/results.json --wave-dir <fx>/wave
```

## Runs (13 in `mutation-r50-c1-b5.json`, 6 in `probes-r50-c1-b5.json`, 2 in `probes2-r50-c1-b5.json`)

Driver output: `runs 13, as expected 13, not 0` (EXIT=0), `probes 6, as expected 6, not 0`
(EXIT=0), probes2 `as_expected: true` twice (EXIT=0). Legs are
`structural/corr/quotes/verdicts/seats/marks`.

| Run | Expected | Observed | Legs | Reading |
|---|---|---|---|---|
| pristine / clean | PASS | **PASS** | 1/1/3/3/18/3 | baseline green — the fixture set is a valid K-pass |
| pristine / D1 | FAIL | **FAIL** | 1/1/3/**2**/18/3 | `blocking GR2 ['R50CritGR2b']` |
| pristine / D2 | FAIL | **FAIL** | 1/1/3/**2**/18/3 | `distinct_bodies GR2 False` |
| pristine / D3 | FAIL | **FAIL** | 1/1/3/**0**/**0**/3 | 18 report files, no results binding |
| pristine / D4 | FAIL | **FAIL** | 1/1/3/**2**/18/3 | six GR2 seats lose the hash leg |
| M1 / clean | PASS | **PASS** | 1/1/3/3/18/3 | mutant does not disturb the pass path |
| M1 / D1 | PASS | **PASS** | 1/1/3/**3**/18/3 | **M1 survived**: `partly` credited |
| M2 / clean | PASS | **PASS** | 1/1/3/3/18/3 | idem |
| M2 / D2 | PASS | **PASS** | 1/1/3/**3**/18/3 | **M2 survived**: padded copy counts distinct |
| M3 / clean | PASS | **PASS** | 1/1/3/3/18/3 | idem |
| M3 / D3 | PASS | **PASS** | 1/1/3/**3**/**18**/3 | **M3 survived**: `seats_ok 18` from files alone |
| M4 / clean | PASS | **PASS** | 1/1/3/3/18/3 | idem |
| M4 / D4 | PASS | **PASS** | 1/1/3/**3**/18/3 | **M4 survived**: stale 64-hex accepted |

### Probes — remove or only narrow?

| Probe | pristine | mutant | Finding |
|---|---|---|---|
| P1 all six GR3 `partly` | FAIL (`verdicts_ok 2`, GR3 credited 0, blocking 6) | **M1 PASS** (`verdicts_ok 3`, GR3 credited **6**) | M1 *removes* the rule: a row whose entire cohort said `partly` is admitted, and the `partly` seats supply the ≥3 credited reviewer+critic evidence |
| P2 byte-identical bodies | FAIL (`verdicts_ok 2`, GR2 credited 6) | **M2 FAIL** (`verdicts_ok 2`) | M2 only *narrows*: exact duplicates are still caught without the whitespace collapse; the collapse is exactly the padded-copy guard |
| P3 one results entry `output: ""` | FAIL (`seats_ok 17`, GR1 credited 5) | **M3 PASS** (`seats_ok 18`) | M3 removes the "completed output" half too; `seats_ok == 18` stops meaning "one completed results entry" |
| P4 contradicting `ROW GR2 VERDICT: fails` line in body | FAIL (`verdicts_ok 2`, blocking `['R50CritGR2c']`) | **M1 PASS** (`verdicts_ok 3`) | M1 removes both halves of the bound-format negative rule (line 1 and the in-body contradicting line) |

## Observations (calibration, not falsification)

1. **No redundant coverage.** All four legs are single-catcher: with any one removed, the defect it
   guards passes the full predicate while every other leg stays green. That is what the frozen
   controls K3/K4/K6 assert one defect at a time; this seat shows it per *rule*, not per fixture.
2. **The distinctness leg is a hash, not a similarity measure.** P2 shows exact duplicates are
   caught, D2/M2 shows padded copies are caught only by the whitespace collapse. A one-character
   edit in a copied body defeats it. That matches the frozen wording "pairwise distinct bodies"
   (`FROZEN.md`, cohort paragraph) — it is a lower bound on independence, not a plagiarism check.
3. **M4 is shape-only by construction, and the shape test already exists.** `HASH_RE` (line 352
   `if not h:`) rejects any non-64-hex second line at bind time, so the mutated comparison adds
   nothing; after M4 the hash leg is pure format. Consequence for the claim: `SECTION SHA256` binds
   the bytes a seat read *only* through line 418's equality, so a cohort carrying a stale-but-valid
   hash passes (D4). The frozen control K2 caught its analogue via `corr_ok`, not via this leg —
   i.e. this leg is the one that would catch a cohort reading the *corrected* rows at the wrong
   revision.
4. **Declared asymmetry (not a defect).** The blocking branch (line 415) runs before the hash
   comparison (line 418), so a seat whose hash proves it read *other* bytes still vetoes the row
   when its first line says `partly`/`fails`. `FROZEN.md` states this explicitly ("blocks the row
   whatever its citations"), so it is contract, not drift — noted because it means a stale-reading
   seat can block a row whose other five seats read the frozen bytes.
5. The mutants never touch the pass path: all four score identical legs to pristine on `clean`,
   which is what makes the survival attributable to the removed rule and nothing else.

## Restoration evidence

- `counters/pristine.py` is a byte copy of the frozen blob:
  `sha256 0af0e679ee82d608d6278d2575391b1a7dd53af49099e962349bddac35f333db`, identical before and
  after all 21 runs (`pristine_copy_sha256_before` == `pristine_copy_sha256_after` ==
  `pristine_restored: true` in `mutation-r50-c1-b5.json`).
- The frozen lane blob re-hashed after the seat:
  `git show <FREEZE>:tools/check-scrub-admission-r50.py | sha256sum` →
  `0af0e679…33db`, unchanged. Only read-only `git show` was run in the lane.
- Mutant bytes preserved as separate files (never mutated in place): `counters/m1.py 891b4a7e…`,
  `m2.py 75483403…`, `m3.py 46d2abd0…`, `m4.py 734c93fc…`.
- Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50MutCounterA` (1.3 MB) removed after the receipts were
  copied here.

## Not done

- No mutation of the `structural_ok`, `quotes_ok` or `marks_ok` legs — the item names M1–M4 only.
- No run against the live integrated revision: this seat measures the counter's rules on synthetic
  fixtures, never the claim's measurement (that is the L1's live run).
- No mutation of the C2 or C3 counters.
