VERDICT: defect-found

Seat C1-R4 (C1CritBattery) — attack on the round-47 pre-data battery
(`tools/check-scrub-admission-r47.py` frozen at 77e9e2b2, sha256
e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b — verified:
`git show 77e9e2b2:tools/check-scrub-admission-r47.py | sha256sum`).
Axes attacked: (A) reproducibility of the committed 12/12 summary, (B) control identity —
is each control what its name says and does each FAIL for its intended reason, (C) declaration
↔ battery consistency, (D) missing cheap writers / admission gaps, (E) precision of stated
FAIL reasons.

# A. Reproducibility — independent re-run reproduces 12/12

Copied `controls/battery.py` to my scratch, set `HYAKU_SCRATCH` to my seat dir, ran it
unmodified. Result: 12 controls, 0 not as expected; every `detail` string matches the committed
`controls/battery-summary-r47.jsonl` at HEAD (e31070a9) exactly. Receipts:
`w1/C1CritBattery/rerun-console.txt`, `w1/C1CritBattery/battery-summary-r47.jsonl`.
The frozen-counter hash above matches the declaration byte for byte.

# B. Control identity and intended FAIL reasons — all 12 check out

Static trace against the frozen counter legs, confirmed by the re-run's per-control details:

| control | claim of name | intended reason | counter leg | re-run detail |
|---|---|---|---|---|
| C1-K0 do-nothing | counter at base bytes | no dispatches → verdicts_ok=0 | bind():0 dispatches | verdicts_ok=0 |
| C1-K1 marks-only | marks without seats grant nothing | verdicts_ok=0 despite marks_ok=3 | run() verdict loop | marks_ok=3 verdicts_ok=0 |
| C1-K22a nonexistent citation | `cmdline.c:999999` unresolvable | GR1 cite_problems → row_ok False | verify_citation():241-248, report_citations_ok():286-296 | GR1 row_ok=False citations_ok=False |
| C1-K23a byte-identical reports | reviewer=critic bodies identical | distinct_bodies False | counter:352 | distinct_bodies=False |
| C1-F1a inner `## ` line | unbound tail inside GR1 | structural_ok=0 | row_extent():154-158 | problems=['GR1: unexpected "## " line…'] |
| C1-F1b duplicated `## GR2` | header occurs twice | structural_ok=0 | row_extent():143-144 | structural_ok=0 |
| C1-F2a negating marks | WITHHELD/unadmitted earn nothing | marks_ok=1 (entry only) | marks block:368-373 | marks_ok=1 marks={entry:T,readme:F,skill:F} |
| C1-F3a deep-nested dispatch | degrade in-band, never empty stdout | parse failure → leg result, rc=1 | load_obj():119-125 | rc=1 stdout_bytes=3260 |
| C1-K-pass | forged valid candidate admits | predicate true | whole predicate | verdicts_ok=3 marks_ok=3 |
| C2-K0 base census, space TMPDIR | base harness fails under space | 13/162 pass | live selftest | FAIL (162 cases, 13 passed, 149 failed) |
| C2-K2 guard removed, cases kept | guard is what makes it pass | cases fail guard-less | live selftest | FAIL (164 cases, 14 passed, 150 failed) |
| C2-K-pass impl census, space TMPDIR | fix restores 164/164 | all cases pass | live selftest | PASS (164 cases, 164 passed, 0 failed) |

Every FAIL is for its intended reason; no control is mislabeled in the current battery.

# C. Declaration ↔ battery consistency — three defects

- C-D1 (stale docstring): `controls/battery.py:4` says "fixture git clone of the lane at IMPL
  (3629c46a)" but `battery.py:12` pins `IMPL = 77e9e2b2…`. 3629c46a is the pre-F1-freeze commit;
  the docstring was never updated when the constant moved (the constant itself moved again in
  e31070a9, which is correct at HEAD).
- C-D2 (contradiction): SCORECARD.md:3073-3074 declares "K-pass the full candidate with forged
  valid holds is proven by the live integration itself, **not by a fixture**", yet
  `battery.py:201-208` builds exactly such a fixture and summary line 9 records
  "C1-K-pass candidate … PASS". Either the sentence or the control must go.
- C-D3 (declared control missing): SCORECARD.md:3077 declares C2 "K1 live output only (no
  selftest change → still FAIL)". `battery.py` has no C2-K1 — only K0 (:212), K2 (:244), K-pass
  (:253). I built and scored it here: base census, space TMPDIR, **two** consecutive live runs,
  no selftest change — both FAIL (162 cases, 13 passed, 149 failed), rc 1, and the two
  digits-stripped stdout streams are byte-identical. As expected. Receipt:
  `w1/C1CritBattery/c2k1-summary.json`.
- C-D4 (historical, informational): the summary committed *at the impl freeze* 77e9e2b2 still
  carried first-run stale lines — C2-K0 `as_expected:false` ("observed PASS (164 cases, 164
  passed)") and an F1a line in the pre-closure shape. e31070a9 repaired both by re-running the
  finalized battery (the first run had caught the counter F1 gap, closed in 77e9e2b2, and its
  own C2-K0 writer bug where the base fixture did not land on base bytes). The receipts path in
  the declaration resolves to HEAD's 12/12 file, which is the authoritative one — but anyone
  auditing "the freeze revision counted seats read" (77e9e2b2) finds a summary whose C2-K0 line
  says the battery failed at the freeze.

# D. Missing cheap writers — five built and scored (receipt: w1/C1CritBattery/xcontrols-summary.jsonl)

All fixtures clone the lane at IMPL, remove origin, toplevel-checked, committed with the fixture
identity, scored with the frozen counter via `--lane`.

- D-X1 wrong-row hash — **counter FAILs closed, now controlled.** GR1 reviewer binds
  `SECTION SHA256` of GR2's section on a `ROW GR1 VERDICT: holds` first line. Observed FAIL,
  rc=1, GR1 bound_on_current=1 (only the critic lands on current). Counter leg: hash equality
  at counter:343. No battery control existed for this writer.
- D-X2 `partly` on current bytes — **counter FAILs closed, now controlled.** All six a-seats
  bind `partly` on correct hashes, distinct bodies, valid citations, marks present. Observed
  FAIL, rc=1; GR1 seats all read `partly`, row_ok False. Counter leg: the all-`holds` quorum at
  counter:355. The item's worry "a `partly` … that the quorum still admits" does not hold.
- D-X3 results status ignored — **admission gap, counter PASSes.** All six results entries
  carry status `failed`/`timeout`/`error`/`killed`; the counter admits all three rows
  (verdicts_ok=3, PASS). `bind()` counts results entries by `name`+`agent` only, never `status`
  (counter:200). The battery's `add_wave` always writes `status: completed`, which masks this.
- D-X4 whitespace-only distinct bodies — **admission gap, counter PASSes.** Reviewer and
  critic bodies differ only by one trailing space per repeated sentence; K23's
  `len(set(bodies)) == len(bodies)` is byte-level (counter:352), so `distinct_bodies=True` and
  the row is admitted. Distinctness of substance is unenforced.
- D-X5 real-but-wrong citation line — **admission gap, counter PASSes.** The GR1 reviewer cites
  `cmdline.c:1` — a real pinned-snapshot line (the SPDX header) that resolves, but the GR1 claim
  (memparse as the scrub_speed_max write parser) lives at cmdline.c:142-153. K22's seat side
  checks resolution only (verify_citation:241-248, report_citations_ok:286-296); GR1
  citations_ok=True, row_ok=True. "Cites resolves, clause false" is admitted.
- D-X6 "seat of another lane's wave directory" — analyzed, not built: the counter is
  `--lane`-scoped and `bind()` requires exactly one dispatch hit, so a report living under a
  different wave directory or round never binds; K0/K1 already exercise the unbound-seats FAIL
  path. Adding it would be redundant.

# E. Imprecise stated reason (control still correct)

- E-1 C2-K2: the declared reason "cases must fail under a space TMPDIR" is only half-true.
  Guard removal leaves the second (R47-C2) pinning case — "a space in a root override stays
  unsafe by design" (tools/tsukuroi-census.sh:3480-3482) — passing with or without the guard,
  because it tests the locator, not the fixture base. That is exactly why the count is 14/164
  (= 13 base-era passes + that one case) rather than 13/164. The control FAILs overall, as
  declared; only the parenthetical overstates. The guard being removed is at
  tools/tsukuroi-census.sh:2055-2059.

# Proposed text

1. `controls/battery.py:4` — s/IMPL (3629c46a)/IMPL (77e9e2b2)/.
2. SCORECARD.md:3073-3074 — either delete "not by a fixture" (the fixture K-pass is the
   stronger control and stays), or delete the battery's C1-K-pass control. Keep the fixture;
   amend the sentence to "K-pass the full candidate with forged valid holds is additionally
   proven by a fixture control (battery C1-K-pass)".
3. Add to the battery: C2-K1 live-output-determinism (already built/scored here — receipt
   c2k1-summary.json), C1-X1 wrong-row-hash (expect FAIL), C1-X2 partly-on-current (expect FAIL),
   and as documented gap probes (expect PASS, labeled "boundary"): C1-X3 results-status-ignored,
   C1-X4 whitespace-only-distinct, C1-X5 real-but-wrong-line.
4. Round-48 counter-hardening candidates (NOT this frozen round): check results-entry status,
   whitespace-normalize bodies before the K23 distinctness test, and — out of scope for a frozen
   mechanical counter — citation-support checking stays a seat-duty, so say so explicitly in the
   counter docstring.

# Receipts (seat dir `.ufo/waves/round-47/w1/C1CritBattery/`)

- `rerun-console.txt` — full independent battery re-run, 12/12 OK lines.
- `battery-summary-r47.jsonl` — re-run summary, matches committed file.
- `xcontrols-summary.jsonl` — D-X1..D-X5 scored results.
- `c2k1-summary.json` — C2-K1 scored result.

Not done: the C2 census identity counter and the live integration kill-rule receipts are other
seats' items; I did not re-run them. No lane, fleet, or host state was mutated; all fixtures
lived under `/fast/scratch/hyaku/tsukuroi-r47/C1CritBattery/` (removed at exit).
