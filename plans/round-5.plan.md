# WWKD plan — tsukuroi round 5 (ufo-round-plan-v1)

Axis move: calibration — the census gate's own mutation testing, via
tameshi's read-only runner `tools/mutate-and-run.sh` (r4-2).
Claim: the census gate (census-v2, 976 ln, sha256 `084951be…78c5`) gets a
measured defect-detection receipt: a pre-registered ~10-defect spec (classes
below) run as `--suite 'bash "$MUTANT" --selftest'` → per-defect
KILLED/SURVIVED/INCONCLUSIVE + kill-rate, with `MUTATE_RESTORE: OK` and the
target sha256 unchanged; every survivor becomes a named suite blind spot —
either a strengthened selftest case (green re-run, case count 26→26+k) or a
documented limitation with reason; the case note lands as
`corpus/knowledge/mutation-case-tsukuroi-census.md`, and the third-census data
is offered to tameshi's cross-case catalog (report line, not absorbed). The
lane's central instrument stops being pass/fail-tested only and gets a
kill-power number.
Anti-claim: unexpressible defect classes (not a single unique exact-string
edit, or exercisable only live) are dropped from the spec BEFORE the sweep
with the reason recorded — never reworded into an easier defect; a SETUP
refusal (runner exit 2) is the recorded outcome, not a partial table;
inconclusive runs count as inconclusive; a surviving defect is a finding,
never a failure of the round; the suite is `--selftest` only — no mutant is
ever run live (host mutation is the one forbidden class).
Measure: kill-rate % over N classed defects (table rows = spec defects); the
survivor rows with disposition; selftest case count before/after with the
green re-run line; `MUTATE_RESTORE: OK` + target sha256 identical; repo `git
status` byte-identical before/after (zero mutation).

## Why this move (candidate decision)

Post-triage context: round 4 (TSUKUROI-R4-2 receipt on the r3 report working
tree, in flight at draft time) re-ran the gate and classed new host findings;
round 5 deepens the instrument behind those findings. SCORECARD move log holds
operability ×2, freshness ×2, depth ×1 and **zero calibration rows**
[observed: SCORECARD.md move-log axes] — calibration is the axis furthest
behind, and the gate is the lane's central instrument whose only current
quality proof is "selftest 26/26 pass": behavior under correct code, not
defect-detection power [inference].

- **Chosen: mutation testing.** Tool + method exist (tameshi works the method
  only; two worked census cases: kimi-census.mjs 8/10 = 80 %, kagi
  surface-census.sh 8/10 = 80 % [observed: tameshi SKILL.md catalog + case
  notes]); tsukuroi's newer, larger census (976 ln vs 896/886) has never been
  measured. Planning probe below shows the interface drives tsukuroi's suite
  end-to-end.
- **Deferred — timer-drift history method** (freshness/depth): §6 measured
  5/5 in-window at snapshot level (journal-boot-plane.md:259-291). The
  retained series spans 2026-10-03 17:42 → now across 13 boots
  [observed: journal-boot-plane.md §1.1], ≈10 days of running time ⇒ daily
  timers ≈10 firing events, boot-based tmpfiles ≈13, weekly keyring ≈1-2
  [inference] — enough for a real trend method, so this is a strong round-6
  candidate; deferred only because one round carries one axis move and
  §6's method already exists (extension, not uncovered ground).
- **Deferred — AUR/foreign risk plane** (coverage): census is 16 foreign /
  3 explicit, provenance split partially measured (yay caches for 2; elephant
  family channel [unknown]; package-state-plane.md:42-72). Local-only signals
  are thin for a *risk* verdict without provenance/upstream comparison
  (network = out of scope per round discipline); promote as its own coverage
  round when triage names package findings.

## Pre-registered defect classes

Single-line exact-string edits, one edit per mutant copy, `count==1` asserted
(runner refuses the spec otherwise). Candidates, ~10 kept after the
expressibility screen: (1) rollup seed / dropped plane; (2) exit map
(DEGRADED/BLOCKED moved); (3) arm refinement (scope `degraded`→DEGRADED
weakened; false HEALTHY in a DEGRADED arm); (4) fail-closed path (BLOCKED arm
→ HEALTHY); (5) threshold/default (sample default; timer scan cap; boot-count
boundaries); (6) predicate weakening (drift predicate; failed-history
pattern); (7) reported-but-unasserted (printed constant/field no case
asserts); (8) selftest self-protection (check()/count arithmetic); (9)
severity ordering (rank/worse inversion); (10) journal class attribution
(coredump/kernel/other disjointness). Record a per-defect **pre-run
expectation** (killed/survived) before the sweep; divergence between expected
and measured is the calibration signal to report [method: tameshi case notes,
E1 column].

## Planning probe (PREP-S5, 2026-10-14 — not the round-5 sweep)

- O: census identity — `wc -l` 976; md5 `41953ee9f2099281c91759249fe8708f`;
  sha256 `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5`;
  `--selftest` rc=0 `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0
  failed)` in 1.76 s.
- O: runner probe — 3 defects, `--suite 'bash "$MUTANT" --selftest'`:
  CONTROL GREEN (26/26); P1 exit-map (`DEGRADED) exit 1`→`exit 0`) KILLED,
  9 failing cases; P2 rollup seed (`local roll=HEALTHY`→`DEGRADED`) KILLED,
  5 failing cases; P3 sample default (`TSUKUROI_SAMPLE_N:-8`→`:-4`)
  **SURVIVED** (26/26 pass); kill-rate 67 %; `MUTATE_RESTORE: OK`; target
  sha256 identical; tsukuroi `git status` identical before/after; runner rc=0
  in 7.2 s wall. Scratch: `/tmp/w4-prep-s5-scratch/` (`probe.defects`,
  `mut.out`, `mut/`).
- I: the P3 survivor is the first measured blind spot: the default sample
  size is a live-only parameter no selftest case reaches
  (`tsukuroi-census.sh:160` default, `:270` `head -n "$SAMPLE_N"`). Suggested
  first strengthening: a fixture with ≥5 candidate packages and the altered
  one beyond position 4, run at the default, asserting drift is detected —
  executor verifies by measurement.
- I: a 10-defect sweep ≈ 11 suite runs ≈ 25 s wall (measured 1.78 s/run).
- Runner pin for the round: `mutate-and-run.sh` sha256
  `597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b`,
  42291 B, r4-2.

## Executor receipt (minimal command, run from the fleet root)

    bash tameshi-shokunin/tools/mutate-and-run.sh \
      --target tsukuroi-shokunin/tools/tsukuroi-census.sh \
      --defects /tmp/tsukuroi-r5-1/spec.defects \
      --suite 'bash "$MUTANT" --selftest' \
      --workdir /tmp/tsukuroi-r5-1/sweep \
      --label tsukuroi-census-r5 --timeout 60

tameshi's tree is read-only; the target is never written (fresh copies only);
all scratch under the round's own `/tmp/tsukuroi-r5-*`. Gate revision is
pinned at sweep time: if the gate is edited before the sweep, re-pin and note
it — the table is revision-tied. If the selftest is strengthened after the
sweep, the survivor-class re-run on the strengthened revision is the proof of
the fix; the case note keeps both revisions.

## Deliverables (round-5 seats)

- `corpus/knowledge/mutation-case-tsukuroi-census.md` — case note in
  tameshi's case-note shape (artifact pin, method provenance cited, kill table
  by class, survivor analysis with dispositions, reproduce block, restore
  proof); the method is cited, never reimplemented.
- `SCORECARD.md` calibration move-log row (before → after); `corpus/README.md`
  row; `LOG.md` round entry; `SKILL.md` append: defect-class table, kill-rate
  interpretation, survivor rules.
- Offer to tameshi (report line only): the third census gate case for its
  cross-case matrix; tsukuroi's gate stays tsukuroi-owned.

## Bounds & unknowns

- Spec v1 expressiveness is line-exact single edits only; multi-line or
  structural defects are unexpressible → recorded drop (anti-claim), never
  approximated.
- Fixture reach: mutant runs pass through the selftest's fixture dispatcher,
  so any host-path arm the fixtures do not reach is protected only by
  inspection; P3 is the first measured instance, not the last [inference].
- The planning probe's 3 defects are illustrative, not the round spec; the
  round re-derives its own spec (may reuse P1-P3) and re-verifies the runner
  pin.
- [unknown] Whether surviving mutants cluster by class (tameshi's two cases
  both survived "reported-but-unasserted" families) — the tsukuroi table is
  the third data point; no prediction claimed.