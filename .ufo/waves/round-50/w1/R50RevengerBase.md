VERDICT: falsifies

Anti-vacuity seat (non-counted). Scope: what does base `b866a1d3d26616119a089f1a69b080136becc17b`
already satisfy, per the frozen round-50 counters, and could a do-nothing control reach any claim.
Headline: **claim C3 is vacuous — the do-nothing control reaches its full target predicate.** C1
and C2 are non-vacuous. One secondary counter-label defect found.

All lanes bytes were read via `git -C .../tsukuroi-shokunin show <rev>:<path>` (the counters'
own `git show` path, `tools/check-adjacency-table-r50.py:95`); the working tree was never the bytes
under test. Scratch was `/fast/scratch/hyaku/tsukuroi-r50/R50RevengerBase/` with `TMPDIR` pinned there.

## (a) Round-50 counters at base — leg-by-leg

### C3 `check-adjacency-table-r50.py --revision b866a1d3` → **PASS (rc 0)**
Receipt `w1/R50RevengerBase/c3-base.json`. Every leg of the target predicate already holds at base:

```
adj_rows 7 · linked_rows 7 · bare_ranges 0 · anchors_ok 7 · registry_ok 7
anchors_checker_rc 0 · quote_at_pin_ok 9 · live_quote_ok 9 · stub_fails 1   → verdict PASS
```

The same counter at the freeze revision `8029cdba…` (`c3-freeze.json`) returns the identical leg
values. A key-wise diff of the two outputs minus the `revision`/`base` fields shows **no differing
leg** — all 18 compared keys identical, including `per_row` and `content_detail`. The counter has
zero discriminative power between base and freeze.

Why it cannot discriminate — the surface C3 claims to move was never touched by the round:

- `PROVINCE.md` blob: base `5f5af836c4c8cd460e0643152a031db907ecbbad` = freeze
  `5f5af836c4c8cd460e0643152a031db907ecbbad` (byte-identical). The ADJ-01..07 table and the
  anchor-quote table live in this file.
- `corpus/knowledge/adjacency-anchors-r19.json`: base `422b0d89…` → freeze `9f09d4d0…`, but a
  row-level comparison of all 124 records shows **123 identical and one changed** — only inbound
  `IN-109`'s `note`/`found_line`, the repin forced by the census edit (FROZEN.md freeze-amendment
  item 3). `sibling_blob_sha256` changes: **0**. So the digests and pins the content legs verify
  are semantically unchanged.
- `quote_at_pin_ok` and `live_quote_ok` read the **sibling repos** at `SIBLINGS`
  (`tools/check-adjacency-table-r50.py:80`, `/home/vgpnk/Projects/shokunin`), not the lane
  revision — they depend on live sibling HEAD (`content_legs`, `:112-161`). `stub_fails` is
  `stub_shape_ok == 1 and s_pin == 0 and s_live == 0` (`:344-349`) on a fully fabricated fixture
  (`stub_province`, `:170-192`) — **revision-independent**: a property of the counter's own code,
  not of any lane byte.

The FROZEN "Before at base" column (`FROZEN.md:23`) lists `quote_at_pin_ok 0, live_quote_ok 0,
stub_fails 0` with the parenthetical "(legs absent at r49)". That is a measurement of the round-49
counter's *schema*, not of the base bytes: the r49 counter's JSON keys (receipt
`c3-r49-base.json`) genuinely lack those legs. Substituting the r50 instrument for the r49 one is
the instrument-swap that makes a vacuous PASS look like a before/after movement.

The control battery has the corresponding hole. `FROZEN.md:57` / `controls/battery.py:264-278`
list C3 controls K1 (stub via `--province-file`/`--registry-file`), K2 (ADJ-02→OUT-002), K3
(mutated registry digest), K-pass (freeze province + registry) — **no control runs the counter on
base bytes**. And because `PROVINCE.md` is byte-identical at base and freeze, the K-pass control
*is* the do-nothing control; it recorded `expected PASS / got PASS` without separating base from
freeze. Contrast C1 (`battery.py:131-135`, "K0 base entry, no cohort") and C2 (`battery.py:217`,
"K0 base census") — both ran base-bytes controls, both FAILed. The anti-vacuity control was applied
to the two claims where it cannot fail and omitted from the one claim where it would.

### C1 `check-scrub-admission-r50.py --revision b866a1d3` → **FAIL (rc 1)**
Receipt `c1-base.json`:

```
structural_ok 1 · corr_ok 0 · quotes_ok 3 · verdicts_ok 0 · seats_ok 0 · marks_ok 0 → FAIL
```

Non-vacuous: `corr_ok` is the byte leg and base fails it — `corr49_missing` lists all four
round-49 corrections absent from the base entry (`source:` S240, narrowed `[inference]`,
`dev-replace.c:1128 "* ` quote, S247/S240 range-gap declaration); `corr49_forbidden_present`
lists the three base strings the corrections remove. A do-nothing control cannot reach C1.

Two calibration notes, not vacuity but worth the L1's attention:

- `structural_ok` and `quotes_ok` already pass at base (2 of 6 legs).
- The byte movement C1 earns is confined to `## GR2`. Section hashes recomputed from the pinned
  extents (LF-joined, heading-to-next-`## `): GR1 `3a2ba180…` and GR3 `43430a14…` are **identical
  at base and freeze**; only GR2 moves (`d4296085…` → `a2e955ce…`). The 18-seat cohort's
  `holds` verdicts on GR1 and GR3 therefore certify bytes that already existed at base; only the
  GR2 re-read exercises new content. Consistent with the correction sites: two land inside GR2's
  extent (lines 83, 127), and two land outside every row (the `source:` header line and the
  Limits/QUALITY additions).
- Minor defect (does not change the verdict): `tools/check-scrub-admission-r50.py:437` emits
  `'counter': 'check-scrub-admission-r49'` — a copy-paste mislabel. The r50 legs
  (`corr49_missing`, `corr49_forbidden_present`, `LANE_FILES` citation repair at `:121`, `:273`)
  are present in the output, so the run was the r50 counter; only the self-label is wrong. A seat
  reading the JSON could mistake which counter ran.

### C2 `check-selftest-matcher-r50.py --revision b866a1d3 --scratch <dir> --runs 1` → **FAIL (rc 1)**
Receipt `c2-base.json`:

```
idiom_sites 7 · base_misses 20 · full_misses 0 · cases 167 · pass_runs 1 (of 1) · case_ok 0 → FAIL
```

Non-vacuous: the three byte legs all fail at base — `idiom_sites 7` (the `printf '%s\n' "$out" |
grep -q` family survives 7 executable sites), `cases 167`, `case_ok 0`. My independent run
reproduces the round's own `before/c2-at-base.json` leg-for-leg on every measured field
(`census_sha256 4e032bcb…`, `base_misses 20`, `full_misses 0`, `cases 167`, `idiom_sites 7`),
differing only in `pass_runs` (1 of 1 at `--runs 1` vs 2 of 2 at `--runs 2`).

Three of six legs are revision-independent or trivially satisfied at base, and the predicate
should not read them as movement:

- `base_misses > 0` and `full_misses == 0` measure the two matcher idioms on a buffer the counter
  itself builds (the counter's own docstring "Named limit"), not the census output — they pass at
  every revision.
- `pass_runs` under `--runs 1` compares `pass_runs == a.runs`, so `1 of 1` satisfies it at base;
  it is a no-regression leg, not a new-capability leg. The frozen predicate's `pass_runs == 2`
  requires `--runs 2`.

## (b) Round-49 counters at base

- `check-adjacency-table-r49.py --revision b866a1d3` → **PASS (rc 0)**
  (`c3-r49-base.json`): `adj_rows 7 · linked_rows 7 · bare_ranges 0 · anchors_ok 7 ·
  registry_ok 7 · anchors_checker_rc 0`. The r49 counter's keys contain no `quote_at_pin_ok`,
  `live_quote_ok` or `stub_fails` — confirming the FROZEN "(legs absent at r49)" is a schema fact,
  not a bytes fact.
- `check-scrub-admission-r49.py --revision b866a1d3` → **FAIL (rc 1)**
  (`c1-r49-base.json`): `structural_ok 1 · corr_ok 1 · quotes_ok 3 · seats_ok 18 ·
  verdicts_ok 0 · marks_ok 0`. `corr_ok 1` under r49 = the round-48 corrections present at base;
  `verdicts_ok 0` because the r49 cohort's citations fail the strict pinned-snapshot-only leg
  (`seat_notes`: "not a pinned snapshot file" — the defect the round-50 `LANE_FILES` leg repairs).
  Note `seats_ok 18` at base: the r49 wave's binding machinery was already satisfied; the blocker
  was the one GR2 `partly` and the citation leg.

(Reference baselines also captured: `c1-freeze.json` C1-r50@freeze FAIL, `c1-r49-freeze.json`,
`c3-r49-freeze.json` PASS.)

## (c) Do-nothing control, leg by leg — could base bytes reach each predicate?

- **C1 — No.** `corr_ok` fails at base (the four corrections are absent); `seats_ok`,
  `verdicts_ok`, `marks_ok` all 0 without the cohort and marks edits. Predicate unreachable. PASS.
- **C2 — No.** `idiom_sites 7 ≠ 0`, `cases 167 ≠ 168`, `case_ok 0` on base bytes. Predicate
  unreachable, even though `base_misses`, `full_misses` and `pass_runs` pass at base (they are
  probe/no-regression legs). PASS.
- **C3 — YES, plainly.** Every one of the nine legs — `adj_rows`, `linked_rows`, `bare_ranges`,
  `anchors_ok`, `registry_ok`, `anchors_checker_rc`, `quote_at_pin_ok`, `live_quote_ok`,
  `stub_fails` — is already satisfied by the base bytes plus the (unchanged) sibling pins and the
  counter's own synthetic-stub self-test. `check-adjacency-table-r50.py --revision b866a1d3`
  returns `verdict: PASS`, output identical to the freeze run on all 18 compared legs. A
  do-nothing control — base bytes, no cohort, no fix — reaches the full target predicate.

## Bottom line for the L1

C3's measurement cannot distinguish "the round verified the anchors by content" from "the anchors
were already real before the round". The counter *is* a real instrument improvement (`stub_fails`
proves it rejects the shape-valid stub the r49 shape legs accept — `stub_shape_ok 1`), but the
round's claim that this moved the adjacency axis is unsupported by the counter's own base-vs-freeze
readings: `PROVINCE.md` never changed and the registry's only delta is the census-forced IN-109
repin. If the round wants an adjacency claim it can defend, the predicate needs a leg that is false
at base — e.g., a leg gated on `PROVINCE.md`'s blob sha differing from base, or a leg that names the
specific anchors the round itself verified. As frozen, C3 is the round's vacuous claim.

## What I did not run (declared)

- I did not re-run the r49 counter against the synthesized stub to prove the r49 counter passes it;
  that is inferred from the r50 counter's own `stub_shape_ok == 1` (the stub satisfies the shape
  legs, which are the r49 counter's entire predicate) — `[INFERENCE]`, not an observed run.
- C2 was run with `--runs 1` per the seat spec, so `pass_runs` was 1-of-1; the frozen predicate's
  `pass_runs == 2` was not re-tested at base.
- I ran only the named counters; no census `--selftest` beyond the two runs the C2 counter itself
  performs (it ran one, per `--runs 1`).

## Receipts
`w1/R50RevengerBase/`:
`c1-base.json` `c1-freeze.json` `c1-r49-base.json` `c1-r49-freeze.json`
`c2-base.json` `c2-base.err` `c3-base.json` `c3-freeze.json`
`c3-r49-base.json` `c3-r49-freeze.json`
