VERDICT: defect-found

# C2-19 — mutation test of `tools/check-package-anatomy-r41.py` (seat C2MutCounter)

Target verified before any mutation: `sha256sum tools/check-package-anatomy-r41.py` →
`c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f` (matches the declared counter sha),
at lane tip `71851d63` ("round-41: C1 pre-data controls, before/after receipts, controls runner name filter").
Eight mutants (the six asked mutations, with mutation 1 and mutation 5 each split into their two readings),
55 sequential counter executions, no parallel counter runs.

## Method

Per run, exactly the item's recipe via the L1's own fixture code (`.ufo/waves/round-41/controls/run_controls.py:28-45`):
`git clone -q --shared --no-checkout <lane> "$D"` under `/fast/scratch/hyaku/tsukuroi-r41/C2MutCounter/`,
`git remote remove origin`, toplevel asserted equal to `$D`, variant files **plus the counter copy**
(pristine or mutated) committed on master with identity `fixture <fixture@shokunin.local>`, then
`python3 "$D/tools/check-package-anatomy-r41.py" --repo "$D" --revision <fixture sha>`.
Control variant files are built by `run_controls.py`'s own builders (`writer_r40` :113, `writer_relations`
:136, `swap` :147, `negate` :155, `verdict_files` :160; c2v dict :215-224), so variant content is bit-identical
to the frozen controls. Freeze revision `e479fdc5` ("round-41: freeze C1/C2 counters, pinned sources, host
capture, registry rows"): the entry does not exist there (`git cat-file -e e479fdc…:corpus/knowledge/alpm-package-anatomy-r41.md`
→ `fatal: path … exists on disk, but not in 'e479fdc…'`, rc=128), matching the frozen K0 do-nothing receipt
(`controls-c2.jsonl:1`: rules/verdicts/host/source all 0, FAIL). A first batch run at the tip freeze `71851d63`
showed K0's baseline depends on the freeze tree (my K0 there: rules_verified 8, host_ok 6 — entry present),
so `e479fdc5` was adopted; pristine K0 there reproduces the frozen receipt exactly (0/0/0/0, FAIL — receipt
`pristine__C2-K0-do-nothing__e479fdc.json`), and K1-K8 outcomes were identical at both freezes (untagged
first-batch receipts kept as that cross-check). Driver with the exact mutant definitions:
`.ufo/waves/round-41/w1/C2MutCounter/mut_driver.py` (every patch site asserted `count==1` before replace).

Baseline (frozen `controls-c2.jsonl:1-9`, order rules/verdicts/host/source): K0 FAIL 0/0/0/0 · K1 FAIL 0/8/6/1 ·
K2 FAIL 8/0/6/1 · K3 FAIL 6/8/6/1 · K4 FAIL 6/8/6/1 · K5 FAIL 8/7/6/1 · K6 FAIL 8/0/6/1 · K7 FAIL 8/7/6/1 ·
K8 PASS 8/8/6/1. My pristine re-scores of K0/K1/K8 reproduce all three exactly.

## Results

| # | Mutant (site in the counter) | Catcher | Before → After | Verdict |
|---|---|---|---|---|
| M1a | window containment dropped (`:372-375`), quote-at-cited-lines kept | **none** (all 9 swept) | no flip anywhere | **SURVIVES** |
| M1b | whole window block dropped (containment + quote lookup) | C2-K8 | PASS → FAIL, rules_verified 8→0 | caught (degenerate) |
| M2 | RELATIONS loop dropped (`:351-353`) | C2-K3 | FAIL → PASS, rules_verified 6→8 | caught |
| M3 | `partly` accepted as holds (`:321`) | C2-K7 | FAIL → PASS, verdicts_ok 7→8 | caught |
| M4 | `fails` ignored (`:321`) | **none** (all 9 swept) | no flip anywhere | **SURVIVES** |
| M5a | PA4 host check dropped, predicate still `host_ok == 6` (`:389`) | C2-K8 | PASS → FAIL, host_ok 6→5 | caught |
| M5b | PA4 host check dropped **and** predicate relaxed to 5 (`:389` + `:394`) | **none** (all 9 swept) | no flip anywhere | **SURVIVES** |
| M6 | a verdict file counts for any row (`:285`) | C2-K7 | FAIL → PASS, verdicts_ok 7→8 | caught |

## The three survivors — evidence

**M1a (drop the window check).** Full nine-control sweep at freeze `e479fdc5`: every control's result,
exit and metric set identical to the frozen receipts, zero flips (receipts
`M1a-window-containment__C2-K<0-8>-*__e479fdc.json`). The mutant is behavior-bearing, not a no-op: K1's PA1
reasons shrink from the frozen `["relation unmet: \bmust\b.*\broot\b", "cited range alpm-package.7.raw:1-1
outside window 95-124", "no 4-25 word quote found in alpm-package.7.raw at cited lines inside the window"]`
(`controls-c2.jsonl:2`) to exactly `["relation unmet: \bmust\b.*\broot\b"]` (receipt
`M1a…C2-K1…__e479fdc.json`, `after_row_reasons`) — the two window reasons vanish, but K1 still fails every
row on RELATIONS (`:351-353`), so no control's verdict moves. Attack probe `PROBE-out-of-window-cite`
(candidate entry with **only** PA1's citation swapped to the r40 first-line trick `alpm-package.7.raw:1-1`,
rule cell and all other rows untouched): pristine FAIL (rules_verified 7) → M1a PASS (rules_verified 8)
(receipts `pristine__PROBE-out-of-window-cite__e479fdc.json`, `M1a…__PROBE-out-of-window-cite__e479fdc.json`).
So under M1a a candidate quoting the right proposition from the wrong part of the pinned file passes, and the
control suite cannot see it. The suite only catches the self-defeating variant M1b (K8 flips PASS→FAIL,
rules_verified 8→0 — the counter then rejects everything, receipt `M1b…C2-K8…__e479fdc.json`).

**M4 (ignore `fails`).** Full nine-control sweep: zero flips (receipts `M4-ignore-fails__C2-K<0-8>…__e479fdc.json`).
K5 — the one control carrying a `fails` verdict — stays FAIL 8/7/6 under the mutant, because its PA4 row gets
only a fails file (`run_controls.py:221`, `verdict_files({4: 'fails'})` → no holds file for PA4): the row is
disqualified by the missing `holds`, never by the `not vd[k]['fails']` conjunct (`:321`). No control in the
suite ever gives one row both a holds and a fails file, which is the only case where that conjunct is
load-bearing. Behavior-bearing probe `PROBE-holds-and-fails-PA4` (PA4 carries `C2RevPA4.md` holds **and**
`C2RevPA4b.md` fails — the real lane's second-reviewer file naming): pristine FAIL (verdicts_ok 7) → M4 PASS
(verdicts_ok 8) (receipts `pristine__PROBE-holds-and-fails-PA4__e479fdc.json`,
`M4…__PROBE-holds-and-fails-PA4__e479fdc.json`). Under M4 a committed second reviewer's `VERDICT: fails`
is silently ignored and nothing in the pre-data suite detects it.

**M5b (drop PA4's host check, predicate relaxed).** Full nine-control sweep: zero flips (receipts
`M5b…__C2-K<0-8>…__e479fdc.json`). The mutant is visibly behavior-bearing — host_ok drops 6→5 across K1-K7 —
yet no verdict moves, and K8 still PASSes (host_ok 5 == 5). No control tampers any host cell
(`run_controls.py:215-224`: every variant keeps the candidate's host cells), so the suite cannot notice PA4's
host verification disappearing. The literal minimal edit M5a (predicate left at 6) is caught by K8 only
because it makes the predicate unsatisfiable (host_ok capped at 5, K8 PASS→FAIL) — i.e. the suite catches the
sloppy version and misses the weakening a rational cheater writes.

## Caught mutants — evidence

- **M2 → C2-K3**: `FAIL → PASS`, rules_verified 6→8, exit 1→0 (receipt `M2-relations__C2-K3-x-false-swap__e479fdc.json`).
  K3's PA4/PA7 failures are pure relation-unmet reasons (`controls-c2.jsonl:4`), so dropping RELATIONS flips it.
  K1 also loses its relation reasons but stays FAIL on window/quote — K3 is the isolating catcher.
- **M3 → C2-K7**: `FAIL → PASS`, verdicts_ok 7→8 (receipt `M3-partly-as-holds__C2-K7…__e479fdc.json`): PA7's lone
  `partly` file becomes a hold.
- **M6 → C2-K7**: `FAIL → PASS`, verdicts_ok 7→8 (receipt `M6-verdict-any-row__C2-K7…__e479fdc.json`): with row
  attribution dropped (`:285` → credit every parsed file to every row), PA7 receives the seven `holds` files
  credited to it and stops being the uncredited row. The body-names-its-row gate (`:281-283`) was kept; the
  attribution loosening alone flips K7. K5 under M6 stays FAIL (every row then also carries PA4's fails file).
- **M5a → C2-K8**: `PASS → FAIL`, host_ok 6→5 (receipt `M5a-host-pa4-dropped__C2-K8…__e479fdc.json`).
- **M1b → C2-K8**: `PASS → FAIL`, rules_verified 8→0 (degenerate; see above).

## What closes the gaps (control-suite additions; the counter's own checks are sound — every mutant was behavior-bearing and the pristine counter rejects both probes)

1. Window: a control whose only defect is an out-of-window citation on an otherwise lexically valid candidate
   (= my `PROBE-out-of-window-cite` shape). Pristine expects FAIL; under M1a it PASSes.
2. Fails: a control where one row carries both a `holds` and a `fails` verdict file (the lane's real
   `C2RevPA<n>` + `C2RevPA<n>b` shape; = my `PROBE-holds-and-fails-PA4`). Pristine expects FAIL; under M4 it PASSes.
3. Host: a control with a tampered PA4 host cell. Pristine expects FAIL (host_ok 5); under M5b it PASSes
   (and under M5a it stays FAIL, so it isolates the weakening, not just the sloppy variant).

## Bounds, tooling, not done

- No tracked lane file touched; writes limited to this report and `.ufo/waves/round-41/w1/C2MutCounter/`
  (56 files, 232 KB: 39 primary receipts tagged `__e479fdc`, 16 untagged tip-freeze cross-check receipts,
  `mut_driver.py`). Scratch `/fast/scratch/hyaku/tsukuroi-r41/C2MutCounter/` removed after receipts were
  copied; `TMPDIR` pointed there; fixture commits live only in the removed clones, so their shas are
  unresolvable after cleanup (same property as the L1's frozen control receipts).
- No tools installed (python3 + git sufficed). No pacman transactions, no host mutation, no agents spawned,
  counters run strictly one at a time (55 runs, ~1.5-2 s each).
- Not done: C1 census counter mutation testing (other seats' item); scoring the counter against the live
  lane tip beyond the controls (out of item scope); dropping the `RELATIONS` dict itself rather than its
  check loop (analytic only: that is a `NameError` crash, caught degenerately by every control).
