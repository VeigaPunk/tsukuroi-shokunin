VERDICT: supports

# R50MutCounterB — C1-B6, second mutant set on `tools/check-scrub-admission-r50.py` (M5-M8)

Bytes under test: `8029cdba1049df25632c91a23c8db4eefb54be5f:tools/check-scrub-admission-r50.py`
(475 lines, sha256 `0af0e679ee82d608d6278d2575391b1a7dd53af49099e962349bddac35f333db`; extracted with
`git -C .../tsukuroi-shokunin show <REV>:tools/check-scrub-admission-r50.py`, scratch copy hash equals the
blob hash exactly). Line numbers below are lines of that blob.

## Method (same as C1-B5)

1. **Clean fixture** (scratch, `clean/`): the counter reads `--entry-file`, `--skill-file`, `--readme-file`,
   `--wave-dir`, `--results-file`, `--dispatch-file` overrides and keeps reading the pinned snapshots from the
   lane at REV (`--lane <lane> --revision 8029cdba…`, read-only `git show`). The fixture entry is the REV entry
   plus the line `## Gate status — round 50 (GR1-GR3 admitted)`; SKILL gets `## Scrub grounding — round 50
   admission`; README gets the non-negated sentence "The `knowledge/btrfs-scrub-grounding-r45.md` rows
   GR1-GR3 are admitted round 50."; 18 synthetic seat reports carry the real section hashes and ≥2 resolving
   citations per row from that row's `CITE` set; dispatch/results carry the 18 names with `reviewer`/`critic`.
2. The fixture builder's section hashes, computed by the counter's own `--section-hash` on the fixture entry,
   are `GR1 3a2ba180…43fee1`, `GR2 a2e955ce…b7f3f`, `GR3 43430a14…bbc32c` — identical to the hashes frozen in
   FROZEN.md, so the fixture sits on the same row bytes the round claims.
3. Original on the clean fixture: `rc=0 PASS`, `structural_ok 1 corr_ok 1 quotes_ok 3 verdicts_ok 3 seats_ok
   18 marks_ok 3`, per row 6/6 credited, quotes 12/29/12 all ok (`out_orig_clean.json`).
4. Each mutant is run twice: clean fixture (must PASS — no false kill) and a **defect fixture** that carries
   exactly the defect the mutant tolerates (original must FAIL, mutant must PASS).

## Mutants (exact one-line changes, all applied to the scratch copy)

| # | Site in blob | Original | Mutant | Clean fixture | Defect fixture: original | Defect fixture: mutant | Verdict |
|---|---|---|---|---|---|---|---|
| M5 | `report_citations_ok`, lines 296-299 | `if not hits: return False, 'no file:line citations'` then `if len({f for f,_ in hits} & set(CITE[row])) < 2:` | the two guards collapse to `if hits and len({f for f, _ in hits} & set(CITE[row])) < 2:` — a body with no citation now passes | PASS | **FAIL** (`verdicts_ok 2`, GR1 credited 0, notes `R50RevGR1a: no file:line citations` …) | PASS | **killed** |
| M6 | line 293 | `if len(body.encode('utf-8')) < 300:` | `if len(body.encode('utf-8')) < 0:` (floor 0) | PASS | **FAIL** (`verdicts_ok 2`, GR2 credited 0, notes `R50RevGR2a: report body under 300 bytes` …) | PASS | **killed** |
| M7 | line 393 | `quotes_ok = sum(1 for r in ROWS if quotes[r]['quotes'] > 0 and not quotes[r]['bad'])` | `quotes_ok = sum(1 for r in ROWS if quotes[r]['quotes'] > 0)` — a non-empty `bad` list no longer blocks the row | PASS | **FAIL** (`quotes_ok 2`; `per_row.GR1.quotes.bad = ["S246 cmdline.c:147: quote mismatch"]`) | PASS (`quotes_ok 3`, same bad list still reported) | **killed** |
| M8 | line 367 | `if name in sentence and phrase in sentence and not NEGATE_RE.search(sentence):` | `if name in sentence and phrase in sentence:` (negation rule dropped) | PASS | **FAIL** (`marks_ok 2`, `marks.readme false`) | PASS (`marks_ok 3`) | **killed** |

No survivor. Every mutant still PASSes the clean fixture, so the defect fixtures — not fixture noise — are what
kill them; the original's failure reason in each case is the mutated leg's own message.

### Defect fixtures (what each carries)

- M5 (`defect_M5/`): all six GR1 seat reports rewritten with a ≥300-byte body that names **no** `file:line`
  (`w1/R50RevGR1{a,b,c}.md`, `w1/R50CritGR1{a,b,c}.md`).
- M6 (`defect_M6/`): all six GR2 seat reports rewritten with a <300-byte body that still cites
  `dev-replace.c:700` and `scrub.c:3081` (both resolve in S247/S242).
- M7 (`defect_M7/`): fixture entry quote line changed from `cmdline.c:147: "potentially suffixed with K, M, G,
  T, P, E."` to `… T, P, F."`, then GR1 section hash recomputed and all GR1 seat hash lines rewritten, so the
  row fails on the quote leg and not on the hash binding. `corr_ok` and `structural_ok` stay 1.
- M8 (`defect_M8/`): fixture README's only qualifying sentence is "The `knowledge/btrfs-scrub-grounding-r45.md`
  rows are never admitted round 50." (`NEGATE_RE` matches `never admitted`); the REV README contains no
  round-50 admission sentence (`grep -c 'admitted round 50' corpus/README.md` at REV = 0), so no unnegated
  sentence shadows it.

## Coverage observation (not a contract change)

The verdicts leg needs only ≥3 credited seats of a row's 6, so **one** defective seat per row does not move
`verdicts_ok`: a single no-citation GR1 body (`out_orig_M5_singleseat.json`) and a single sub-300-byte GR2 body
(`out_orig_M6_singleseat.json`) both leave the original at `rc=0 PASS` with the failure visible only in
`seat_notes`. A row-level defect must cover ≥4 of its 6 seats (or all of one role) to flip the predicate; the
defect fixtures above therefore cover all six seats of the row. This is slack by design (6 seats, 3 credited),
recorded as a finding about the counter's discrimination, not as permission to change it.

## Restoration and hygiene

- The lane blob was never written; the counter was only read via `git show` and copied to scratch. After the
  runs, `sha256sum counter_orig.py` = `0af0e679ee82d608d6278d2575391b1a7dd53af49099e962349bddac35f333db` =
  the REV blob hash (recomputed at the end of the session), i.e. bytes restored/unchanged.
- All work in `/fast/scratch/hyaku/tsukuroi-r50/R50MutCounterB/` (546 GiB free on /fast); `TMPDIR` pointed at
  the scratch dir; the scratch tree was removed after the receipts were copied; no git/jj mutation anywhere;
  no writes outside this wave dir and scratch; no packages installed.

## Not done

- No run against the real `w1-results.json`/seat reports: at REV `.ufo/waves/round-50/` has no `w1-results.json`
  and no `w1/*.md`, and the counter at REV gives `verdicts_ok 0 seats_ok 0 marks_ok 0` (baseline `base_run.json`, in receipts).
  The clean fixture is synthetic and proves leg
  behaviour, not the round's admission.
- No census/`--selftest` run (not part of this item).

## Receipts (`…/w1/R50MutCounterB/`)

`counter_orig.py`, `counter_M5.py`…`counter_M8.py`, `diff_M5.txt`…`diff_M8.txt`, `build.py`, `mutants.py`,
`out_orig_clean.json`, `out_M{5,6,7,8}_clean.json`, `out_orig_M{5,6,7,8}_defect.json`,
`out_M{5,6,7,8}_defect.json`, `out_orig_M{5,6}_singleseat.json`, `MANIFEST.sha256` (197 KB total).
