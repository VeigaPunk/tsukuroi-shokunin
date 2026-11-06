# MutBattery — round 85 w1 (mutation tester)

Question: is each QUALITY 117/119 feature of the frozen C2 battery load-bearing?

Lane `tsukuroi-shokunin`, measured at `git -C … rev-parse master` = `479d868b2fc8969a19a617cd55ced5c13edd84b6`.
Battery under test `tools/resume-gate-battery-r85.py` sha256 `b30a7c1ed8fca5fa9c30fb3f4b221ccae11137f688bffc47844b16f0a117ba21`
(= the freeze value). I ran a **byte-identical copy** (`sha256` of the copy printed in `sha256.txt`); the lane file was not
edited. Candidate gate `tools/check-hibernate-resume.py` sha256 `88041b7509fc5824b036d45dd3416bfadbaeb17f0b702e15af0edd17944483e7`.
`git status --porcelain tools/ .ufo/waves/round-85/before/` printed only `?? tools/check-nonauthor-label-r85.py` (another
seat's file); neither the battery nor the frozen inputs changed under me.

Axes walked: **calibration** (does each advertised feature carry kill weight against a forger), **provenance** (do the
committed controls reproduce byte-for-byte), **operability** (does a one-feature removal keep the instrument runnable).

## Method

Nine one-feature mutants of the battery (`mutant-batteries/B1..B9.py`; the diffs are one hunk each, `diff -u` against the
frozen bytes), run with `cwd=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` so the default `--base` resolves. For each
mutant I ran the six committed candidate-free forgers (`k2`, `k3d`, `k3e`, `k4`, `k5`, `k6` — copies of
`.ufo/waves/round-85/before/controls/*.py`, hashes in `sha256.txt`) plus one derived forger written where the frozen set
cannot exploit the removal (`forgers/S2..S9`). Every run is a real invocation of the mutant battery:
`python3 <battery> --gate <per-run copy of the gate> --out <scratch case log>`; a per-run copy isolates k5's
`.k5-counter`, and no file was left in the lane. Sanity leg: the honest candidate gate reads target on every mutant
(Table 3), so each mutant is a working battery and not a broken script.

## Table 1 — mutant matrix (one feature removed)

| Mutant | Feature removed | Mutant target (candidate) | Forger that reaches it | Frozen-forger scores | Load-bearing? |
|---|---|---|---|---|---|
| B1 | `rng.shuffle(cases)` at `:326` | 20 | **none** | k5 **18/20**, k6 14, k2/k3d/k3e 13, k4 2 | **not shown** (F-2) |
| B2 | random bases at `:321` (host base only) | 20 (23 cases) | **S2 20/20 rc0** | k6 16, k3d/k3e 14, k2 13, k4 2, k5 1 | yes |
| B3 | `MULTI-FAULT` family (`:84-85`, `:260-263`) | 19 (116 cases) | **S3 19/19 rc0** | k6 14, k2/k3d/k3e 13, k4 2, k5 0 | yes |
| B4 | `PREC-NOHIB` (`:84-85`, `:264-266`) | 19 (128 cases) | **S4 19/19 rc0** | k6 14, k2/k3d/k3e 13, k4 2, k5 0 | yes |
| B5 | `PREC-DECOYS` (`:84-85`, `:267-271`) | 19 (128 cases) | **S5 19/19 rc0** | k6 15, k2/k3d/k3e 12, k4 1, k5 0 | yes |
| B6 | `PREC-NO-RESUME-ARG` (`:84-85`, `:272-276`) | 19 (128 cases) | **S6 19/19 rc0** | k6 14, k2/k3d/k3e 13, k4 2, k5 0 | yes |
| B7 | findings comparison at `:333` (rc+verdict only) | 20 | **S7 20/20 rc0** | k6 **18**, k2/k3d/k3e 15, k5 5, k4 2 | yes |
| B8 | order/duplicate normalisation at `:333` | 20 | **S8 20/20 rc0** | k6 15, k2/k3d/k3e 13, k4 2, k5 0 | yes |
| B9 | `schema-v1` MALFORMED kind at `:226` | 20 | **S9 20/20 rc0** | k6 15, k2/k3d/k3e 13, k4 2, k5 0 | yes (and F-1) |

Derived forgers (all under `forgers/`, each a small edit of the candidate gate or of k5, so each is exactly the "one
missing property" cheat the feature is supposed to kill):

* **S2** `s2-host-base-diff.py` — reads the committed host base and maps *which field differs* to the expected finding;
  evaluates no rule base-relatively (no free-swap arithmetic, no last-token parse). 118 lines, only useful when every case
  comes from that one base.
* **S3** first chain finding only (no multi-fault aggregation). **S4** drops the `nohibernate ⇒ noresume` precedence.
  **S5** over-fires on the decoy tokens (`hibernate=nocompress`, `<mod>.noresume=1`, `<mod>.nohibernate=1`).
  **S6** round-84 rule 1 verbatim (no `resume=` ⇒ only `HR-NO-RESUME-ARG`). **S7** correct rc/verdict, one bogus finding.
  **S8** correct finding set, reversed order plus a duplicate. **S9** accepts the superseded `resume-facts/1` schema.

## Table 2 — every derived forger against the UNMUTATED frozen battery

| Forger | Pristine frozen battery | Note |
|---|---|---|
| S2 | **1/20** (only MALFORMED) | random bases defeat the base-diff memoriser |
| S3 | **19/20** (fails MULTI-FAULT) | |
| S4 | **19/20** (fails PREC-NOHIB) | |
| S5 | **19/20** (fails PREC-DECOYS) | |
| S6 | **19/20** (fails PREC-NO-RESUME-ARG) | |
| S7 | **5/20** | |
| S8 | **5/20** | |
| S9 | **20/20 in 10 of 33 runs** (incl. three consecutive) | **KILL FLAG — F-1** |

Frozen controls reproduced the freeze receipt on the pristine battery (k2 13, k3d 13, k3e 13, k4 2, k5 0, k6 15 — the
freeze receipt says K6 14–15 and 13/13/13/2/0), so the instrument is stable run to run.

## Findings

**F-1 (defect, C2 measurement gap — flagged loudly, seat's kill rule invoked).**
`MALFORMED` draws 2 kinds of 9 per base with `rng.choice` (`tools/resume-gate-battery-r85.py:226`) over 6 bases
(`:253-255`), i.e. 12 draws per run; a kind is therefore **never exercised** with probability `(8/9)^12 = 24.3%`.
A gate that validates every MALFORMED kind except the one it mishandles reads 20/20 in those runs.
S9 is exactly that gate — the candidate with `schema != SCHEMA` relaxed to `schema not in (SCHEMA, "resume-facts/1")`,
which the frozen rule set forbids (`docstring :39-40`: "schema != resume-facts/2 (**resume-facts/1 included**)" → rc2).

Measured: 33 independent runs of S9 against the unmutated frozen battery → **10 runs read 20/20 `verdict: met`, rc 0**
(x-s9-r02, x-s9-r04, x-s9-r05, x-s9-r06, x-s9-r09, x-s9-r11, x-s9-r16, x-s9-r18,
p-s9-schema-v1-r08, p-s9-schema-v1-r11), 23 read 19/20 (MALFORMED), matching the 24.3% model.
**Three consecutive runs read 20/20 (x-s9-r04, x-s9-r05, x-s9-r06)**, and in each of the 10 met runs the 12 malformed
draws contain **no `schema-v1`** — the drawn mixes differ run to run (x-s9-r04:
`cmdline-type, drop, hooks-type, lockdown-unbracketed, schema-v0`; x-s9-r06:
`cmdline-type, drop, lockdown-two-brackets, lockdown-type, lockdown-unbracketed, schema-v0, swaps-type`;
`evidence/s9-all-33-runs.json`).

Seat rule applied: a forger that does not implement the frozen rule set reached the frozen target, so **this is a KILL of
C2 as frozen and it is flagged loudly**. Scope of the claim: it is a false pass of the *measurement*, not a defect of the
candidate gate (the gate itself reads 20/20 in three separate runs, Table 3). The frozen predicate is **not** re-declared
here; the L1 decides. The battery's own deterministic parts are fine — the leak is the under-sampled MALFORMED family,
which is also visible in the frozen forgers: k3d and k3e fail MALFORMED on the pristine battery but pass it on B1 and B2
(13 → 13/14) purely because the draws differ.

Proposed patch (written, not applied): `proposed/malformed-coverage.patch` +
`proposed/FIX-malformed-kinds.py` (sha256 `3f36e84e…3096c`) — lift the nine kinds to `KINDS`, give
`plan_base(name, b, rng, idx)` and pick `KINDS[(2*idx + j) % len(KINDS)]`, so the 12 draws cover all nine kinds every
run while case *content* stays random. Verified: with the patch, S9 reads **19/20 rc1 in 3/3 runs** (MALFORMED, all nine
kinds present each run) and the candidate gate still reads **20/20 rc0 in 2/2 runs**.

**F-2 (feature not shown load-bearing: the shuffle).** With the shuffle removed (B1), the order-replay forger k5 — which
never opens `--facts` and answers from a per-parent counter — reads **18/20** (fails `MULTI-FAULT`,
`PREC-NO-RESUME-ARG`) versus 0/20 on the frozen battery. No forger reaches the mutant target. This is structural, not a
weak probe: those two families build their expected findings from OS entropy at plan time
(`:260-263` multi-fault draw, `:272-276` precedence case), so a no-read position replay **cannot exceed 18/20 even with a
fixed order**. The shuffle is therefore not what makes a replay unable to reach 20/20 — per-case randomisation is. It
costs nothing and keeps the r84 replay class at 0 instead of 18, so I recommend keeping it, but QUALITY 119's
order clause is not demonstrated load-bearing by this battery.

**F-3 (B2 load-bearing).** S2 reads 20/20 on the host-only mutant and 1/20 on the frozen battery: random bases are what
kills a committed-base diff memoriser. Cheap exploit confirmed, feature necessary.

**F-4 (B7/B8 load-bearing, and materially so).** Verdict-only comparison (B7) lifts the frozen forger k6 from 15 to 18 and
k2/k3d/k3e from 13 to 15 — the exact-findings comparison carries most of the battery's discriminative weight. B8 is
load-bearing as a class (S8 20/20 vs 5/20) though the frozen set gains little from it.

**F-5 (positive result, recorded so it is not mistaken for a gap).** B3–B6 each fall to exactly one property-less gate
(S3–S6 at 19/19) and to nothing else: the multi-fault and precedence families are each the *only* family that kills its
cheat. Removing any of the four lowers the frozen forger scores by at most three families, so their kill weight is
one-forger-specific, as designed.

**F-6 (sanity, no finding).** The candidate gate meets every mutant (Table 3) and 20/20 on the pristine battery three
times — the mutants are valid batteries, and my copy of the frozen bytes behaves identically to the freeze.

## Table 3 — candidate gate on each mutant (all `verdict: met`, rc 0)

B1 20/20 · B2 20/20 · B3 19/19 · B4 19/19 · B5 19/19 · B6 19/19 · B7 20/20 · B8 20/20 · B9 20/20 · pristine 20/20 ×3.

## Receipts

Each line is the stored per-run summary in `results/` (`matrix-summary.json`, `matrix-extra.json`,
`matrix-fixcheck.json`; flat view `results/matrix.tsv`), restricted to the fields shown; `rc` is the battery's exit code
from that run. Counting-command shape: `python3 driver.py <battery> <gate> <tag>` with `cwd` = lane root.

```
{"cases": 134, "failed_families": [], "families_passed": 20, "families_total": 20, "rc": 0, "tag": "sanity-candidate", "target": 20, "verdict": "met"}
{"cases": 23,  "failed_families": [], "families_passed": 20, "families_total": 20, "rc": 0, "tag": "b2-s2-host-base-diff", "target": 20, "verdict": "met"}
{"cases": 116, "failed_families": [], "families_passed": 19, "families_total": 19, "rc": 0, "tag": "b3-s3-first-chain-fault", "target": 19, "verdict": "met"}
{"cases": 134, "failed_families": ["MULTI-FAULT", "PREC-NO-RESUME-ARG"], "families_passed": 18, "families_total": 20, "rc": 1, "tag": "b1-k5-replay-v2", "target": 20, "verdict": "unmet"}
{"cases": 134, "failed_families": [], "families_passed": 20, "families_total": 20, "rc": 0, "tag": "b9-s9-schema-v1", "target": 20, "verdict": "met"}
{"cases": 134, "failed_families": [], "families_passed": 20, "families_total": 20, "rc": 0, "tag": "x-s9-r05", "target": 20, "verdict": "met"}
{"cases": 134, "failed_families": ["MALFORMED"], "families_passed": 19, "families_total": 20, "rc": 1, "tag": "fix-s9-r0", "target": 20, "verdict": "unmet"}
{"cases": 134, "failed_families": [], "families_passed": 20, "families_total": 20, "rc": 0, "tag": "fix-candidate-r0", "target": 20, "verdict": "met"}
```

Run totals: 88 (matrix) + 31 (extra: 20 S9 repeats, 9 mutant-vs-candidate sanity runs, 2 candidate reruns) + 5 (fix
check) = 124 runs. Runtime per pristine run ≈ 6.5 s (134 cases) on this host; mutants 1–21 s under 10-way load.

## Bounds observed

Leaf seat: no subagents, no `agent://all`, no model choice. No lane file was edited (write scope
`.ufo/waves/round-85/w1/` only); no git/jj mutation; host read-only (no swap/sysctl/`/sys`/`/boot` writes); no pacman and
no installs needed (python3 + stdlib only). Scratch `/fast/scratch/hyaku/tsukuroi-r85/MutBattery` was removed at exit;
`.k5-counter` never existed outside my scratch run dirs (verified: the lane controls dir has none).
