VERDICT: defect-found

# TMutCounter — C1-M3: mutation test of the frozen C1 counter (tools/score-selftest-tmpdir-r48.py)

Result: **5 of 6 single mutants SURVIVE the frozen control battery** (same verdict on all five
battery controls K0/K2/K3/K4/K-pass as the pristine counter), and every survivor is proven
live by a discriminator census that flips its verdict between pristine and mutant. Only
**m5 is killed** — it flips the K-pass control to FAIL. The counter itself is byte-identical
to the frozen file; the mutation surface under test is its scoring logic, so the battery's
verdict-level checks are the contract being probed.

Verdict `defect-found`: the battery has five independent leg-level holes — every leg of the
counter predicate can be weakened one leg at a time without any battery control noticing.
C1's claims are NOT falsified (the pristine counter still reaches the right verdicts); the
coverage ledger is what is defective.

## Setup (all in scratch; nothing written to the lane except this report + receipts)

- Pristine counter: `git show ae99f021:tools/score-selftest-tmpdir-r48.py` →
  `counter_pristine.py`, sha256 `8eead161e990e9e6f5155984797396d79fe7a3e6524a1a0c3087758658625640`
  (receipt: `TMutCounter/mutants/counter_pristine.py`).
- The real census was never run (would be 7 counters × 5 controls × ~5-10 min). Instead, five
  ~20-line bash stub censuses emulate each battery control's *observable* signature
  (exit code, stdout last line, mktemp call count/location, fixture cleanup, TERM behaviour,
  static text). The stubbed leg vectors were verified against the frozen pre-data receipt
  `controls/battery-summary-r48-c1.jsonl` — after one stub fix, **all five stub signatures
  match the recorded vectors exactly** (see table below; each counter run against a stub
  takes ~19 s; receipts `TMutCounter/stubs/`, `TMutCounter/results*.jsonl`,
  `TMutCounter/out/*.json`).
- Battery expectation per control (from `battery-c1.py:63-67`): K0→FAIL, K2→FAIL, K3→FAIL,
  K4→FAIL, K-pass→PASS.

Recorded leg vectors vs. stub vectors under the pristine counter:

| control | recorded (battery-summary-r48-c1.jsonl) | stub observed | match |
|---|---|---|---|
| K0 base | pass=0 loc=3 clean=4 ff=1 term=0 static=0 | same | ✓ |
| K2 fallback | 4 3 4 2 1 0 | same (after ordering fix, results2.jsonl) | ✓ |
| K3 traps | 4 4 4 2 0 1 | same | ✓ |
| K4 usage-text | 0 3 4 1 0 0 | same | ✓ |
| K-pass fix | 4 4 4 2 1 1 | same | ✓ |

(K0's pass=0 is the base census printing `PASS (149 cases, …)` — base `tsukuroi-census.sh:3484`
prints its own case count and the counter wants 166; its static=0 is the literal `st_base=/tmp`
at base line 2057. K3's term=0 reproduces bash `trap … EXIT INT TERM` semantics — trap runs,
script continues, exits 0; verified empirically: rc=0 + final line printed vs rc=143 with an
explicit `exit 143` trap.)

## The six mutants (each a single-line/single-expression change; diffs in `TMutCounter/mutants/`)

| mutant | change (counter source line) | battery verdicts (K0,K2,K3,K4,Kpass) | outcome |
|---|---|---|---|
| m1 | `pass_ok = int(rc == 0 and …)` → `int(last_line(out) == want)` | F F F F P | **SURVIVED** |
| m2 | loc leg: `… or int(tmpdir not in (None, '/tmp'))` | F F F F P | **SURVIVED** |
| m3 | `clean_ok = int(not exists(real))` → `clean_ok = 1` | F F F F P | **SURVIVED** |
| m4 | term leg: `rc == 143` → `rc in (143, 1)` | F F F F P | **SURVIVED** |
| m5 | `read_log` absent-log → `[['<absent-log>','','']]` | F F F F **F** | **KILLED** |
| m6 | `if BASE_ASSIGN.search(ln):` → `if False:` | F F F F P | **SURVIVED** |

## Live-mutant proof (discriminators; `pristine → FAIL`, `mutant → PASS`)

- **m1** vs `disc_m1.sh` (prints exact `PASS (166 cases, …)` line, exits 1): pristine FAIL
  (pass=0), m1 PASS — the counter accepts a selftest whose summary claims 166/166 while the
  process fails.
- **m2** vs `disc_m2.sh` (statically clean census that builds its fixture under /tmp for a
  scratch/spaced TMPDIR, no `base=/tmp` text): pristine FAIL (loc=2), m2 PASS — a silent
  TMPDIR-ignoring census escapes both legs.
- **m3** vs `disc_m3.sh` (leaves the fixture behind only when the base is not /tmp): pristine
  FAIL (clean=2), m3 PASS — a census that leaks every fixture under scratch/spaced scores
  fully clean.
- **m4** vs `disc_m4.sh` (TERM → remove fixture, exit 1): pristine term rc=1→ok=0 FAIL, m4
  term_ok=1 PASS.
- **m6** vs `disc_m6.sh` (compliant census + dead `idle_base=/tmp` line): pristine FAIL
  (static=0), m6 PASS.
- **m5** discriminates itself: on stub_pass, absent logs at the failfast legs become phantom
  fixture rows (`failfast_ok=0`), and the term poll loop consumes the phantom row, computes
  `real=''` and reports `fixture_removed=false` (`term_ok=0`) — receipt
  `out/m5--K-pass.json` vs `out/pristine--K-pass.json`.

## Why each survivor escapes (battery structure)

- **m1**: no control prints the PASS line with a non-zero exit; every FAIL control fails
  pass_ok via *content* (149-case line) or missing line, so `rc==0` is dead weight inside
  the battery's visible range.
- **m2**: the only loc-failing controls (K0/K2/K4) all fail ≥2 other legs simultaneously
  (K0/K4: pass+static; K2: static `st_base=/tmp`); a static-clean /tmp-under-scratch census
  is never among the controls.
- **m3**: no control leaves a fixture behind; clean_ok is never the margin anywhere.
- **m4**: K3 is the sole term-failing control and the real K3 exits **0** on TERM (verified
  bash semantics), not 1 — accepting rc∈{143,1} never sees a 1. m4's survival is contingent
  on that accident of K3's construction.
- **m6**: K0/K2/K4 all carry static=0 *and* other failures; `static_ok` is never the sole
  FAIL leg, so the entire `...base...=/tmp` regex is unguarded by the battery.
- **m5 (killed)**: the only mutant that breaks a *passing* leg of a control expected to pass —
  showing the battery's kill criterion is effectively "flips a control verdict", never
  "changes a leg".

## Note on scope

- Everything ran on stubs; no real `--selftest` was executed (cost rule honoured: zero real
  census invocations). Stub signatures were anchored to the frozen receipt, not guessed.
- Counter byte hashes: pristine `8eead161…`, m1 `7c63afd8…`, m2 `00a9326c…`, m3 `e12d44c9…`,
  m4 `6f08c371…`, m5 `62480c35…`, m6 `66bf2419…` (files under `TMutCounter/mutants/`).
- No tools installed; python3/bash/git only. Scratch `/fast/scratch/hyaku/tsukuroi-r48/TMutCounter`
  removed after receipts were copied.
