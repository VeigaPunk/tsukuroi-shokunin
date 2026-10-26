VERDICT: defect-found

# C2-11 — mutation test of `tools/check-scrub-record-r42.py` against the frozen C2 battery

Seat C2MutCounter, round 42 wave w1 (hyaku run 9). Target: the frozen counter
`tools/check-scrub-record-r42.py`, sha256 `dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f`
— verified unchanged before mutation, both as lane worktree bytes and as
`git show a84fc9dec860f8bea516dff7ddfdc98223cdae52:tools/check-scrub-record-r42.py | sha256sum`
(both printed `dbe933ec…`; observed 2026-10-26). Battery:
`.ufo/waves/round-42/controls/run_controls_c2.py`, run exactly as the item prescribes, one battery at a time.

**Headline: 1 of 12 mutants killed, 11 survived.** The frozen battery's controls (K0–K5) exercise only the
verdict-binding chain and the scripted happy path; a counter weakened at 11 of the 12 probed points would
still pass the battery. Survivors are battery gaps (item C2-11's own framing), detailed per mutant below.

## Method

- Fixture: `git clone -q --shared` of the lane into
  `/fast/scratch/hyaku/tsukuroi-r42/C2MutCounter/fx.FE4OsK`, `git remote remove origin`,
  `git rev-parse --show-toplevel` asserted equal to the clone dir (realpath compare), detached at the
  freeze commit `a84fc9dec860f8bea516dff7ddfdc98223cdae52` — the tree the frozen reference battery ran on
  (`controls/C2-K3.jsonl` records `tree_rev == counter_rev == a84fc9d…`). Counter sha256 re-verified in the
  clone before any edit: `dbe933ec…`.
- Baseline commit `2ceb2d1e90ea0c9a81e7fdd8bad21c846dd7593f` (empty commit on `a84fc9d`, pristine counter).
  Each mutant: working tree reset to `2ceb2d1e`, one minimal edit to `tools/check-scrub-record-r42.py`,
  diff printed and committed with `-c user.name=fixture -c user.email=fixture@invalid`, then:
  `python3 .ufo/waves/round-42/controls/run_controls_c2.py --lane <clone> --tree-rev <mutant commit>
  --counter-rev <mutant commit> --scratch /fast/scratch/hyaku/tsukuroi-r42/C2MutCounter/s
  --out /fast/scratch/hyaku/tsukuroi-r42/C2MutCounter/out-<n>` with `TMPDIR` inside the seat scratch.
- Kill criterion: battery summary must equal the reference pattern (below). Any control verdict flip,
  or `should_fail_accepted > 0`, or `control_accepted == 0` ⇒ killed. All 13 runs completed normally
  (no battery crash; per-control exit codes unchanged: K3 exit 0, all others exit 1).
- Mutant diffs (all 12, single-hunk, single-file): receipt `mutant-diffs.patch` (225 lines). Full battery
  records per run: receipts `out-0/` … `out-12/` (`C2-K0..K5.jsonl` + `battery-summary.jsonl` each).

## Reference (baseline, pristine counter)

Command: `run_controls_c2.py --lane fx.FE4OsK --tree-rev 2ceb2d1e… --counter-rev 2ceb2d1e… --scratch …/s --out …/out-0`.
Observed: `K0 1 FAIL rows 0 …` / `K1 1 FAIL … v 0` / `K2 1 FAIL … v 0` / `K3 0 PASS … v 5` /
`K4 1 FAIL … v 4` / `K5 1 FAIL … v 4`; summary
`{"control_accepted": 1, "controls": {"K0": "FAIL", "K1": "FAIL", "K2": "FAIL", "K3": "PASS", "K4": "FAIL", "K5": "FAIL"}, "should_fail_accepted": 0, "should_fail_accepted_names": []}`.
This reproduces the frozen `controls/battery-summary-c2.jsonl` exactly. Wall time ≈ 3 s per battery.

## Results table

| # | Mutation (pristine counter line) | Commit | Battery vs reference | Verdict |
|---|---|---|---|---|
| M1 | drop window check: `q_ok = good >= 1 and in_window >= 1 and bad == 0` → drop `in_window >= 1` (`tools/check-scrub-record-r42.py:205`) | `8b54e78b68d3132a2f7792a9143c7127188a1f09` | identical (K3 PASS, sfa 0) | **SURVIVOR** |
| M2 | drop role check: dispatch `t.get('agent') == role` and results `r.get('agent') == role` removed (`:124`, `:126`) | `c4fda91b5c2e8891b31c059612a788bb60d2502c` | identical | **SURVIVOR** |
| M3 | accept any VERDICT line: `VERDICT_RE` `(holds\|partly\|fails)\b` → `(\S+)` (`:66`) | `17664b5b271344906e590a39cda6036afc68abdb` | identical | **SURVIVOR** |
| M4 | skip report-file equality: `rep = show(...)` + `line not in rep` gate removed (`:133-135`) | `0553535c0aa2e43ce9ee0771b852df27f7488994` | identical | **SURVIVOR** |
| M5 | treat None output as holds: non-str `output` returns `('holds', None)` instead of unbound (`:127-128`) | `e5809e59b46fd3b58538dfb311a80d785b1e0da0` | identical | **SURVIVOR** |
| M6 | skip base-absence of sources: `sid not in reg_base` dropped from `ok` (`:234`) | `357ce19f96edfa6a764b2557d800ef218bcd30fa` | identical | **SURVIVOR** |
| M7 | `host_ok >= 3` → `host_ok >= 0` in predicate (`:240`) | `a16590f24f95be543cd5a3f8905072800516a889` | identical | **SURVIVOR** |
| M8 | accept `partly` without residual: `(all(v == 'holds') or resid == 'holds')` conjunct dropped (`:217-218`) | `d1c7fd811aca7d7f97b1b26159f53226d02e84b0` | **K5 FAIL→PASS**, `should_fail_accepted: 1 ["K5"]` | **KILLED** |
| M9 | drop snapshot digest check: sha256 gate removed from `snaps[f]` (`:163`) | `a052b8fed8a8c00361835ffae9d6a470f34c32a3` | identical | **SURVIVOR** |
| M10 | read the residual for every row: `if 'partly' in vs:` guard removed (`:214-216`) | `5d96a1914e608086889a6ada8c462aaa4938455f` | identical | **SURVIVOR** |
| M11 | drop `base_hits == 0` from predicate (`:241`) — beyond the required ten | `83d021b92bdacf308916fb2b5ff95fae13ca624e` | identical | **SURVIVOR** |
| M12 | drop `rows == 5` from predicate (`:240`) — beyond the required ten | `f1617e7e4c4e0fd34b7e8becc4a0592a7f4457a7` | identical | **SURVIVOR** |

M8 observed battery tail: `K5 0 PASS rows 5 q 5 nov 5 host 5 src 1 v 5 base 0 tb 0` and
`{"…, "should_fail_accepted": 1, "should_fail_accepted_names": ["K5"]}` — the only flip in the whole probe.

## Why each survivor survives (battery-side evidence, `run_controls_c2.py`)

- M1 (window): `scripted_entry` picks each quote as "the first non-blank line inside the row's frozen
  window" (`:7`, picker `:44-53`), so `in_window == good` in every control; no control ever cites a
  resolving line outside the row's windows.
- M2 (role): `write_records` always writes the correct `agent` role next to the name (`:84-87`), and the
  forged dispatch lists the same ten name+role pairs (`:89-92`); no control binds a name with a wrong role.
- M3 (verdict token): controls only ever write `holds`/`fails`/`partly` (`:128`), all matched by the
  pristine regex. Note the deeper masking: `v_ok` (`counter :217-218`) independently rejects any bound
  non-`holds` verdict unless a residual reads `holds`, so loosening the token set is behaviorally visible
  only in the residual-holds path — a garbage-token control must also forge a residual seat reading
  `holds` to kill M3.
- M4 (report equality): K1/K2 fail earlier gates (no dispatch / dispatch without the seats), and K3/K4/K5
  all write matching report files (`write_reports :78-82`); no control has dispatch+results with a
  missing or diverging report line.
- M5 (None output): `write_records` always writes `output` as a str (`:86`); no control emits `output: null`.
- M6 (base-absence): `flip_rows` (`:58-66`) only flips rows already present at the tree rev (S237–S239,
  absent at BASE `c8efaa3` — `git show a84fc9d:corpus/SOURCES.md | grep -c -E '^\|\s*S23[7-9]\s*\|'` → 3,
  and the pristine K3 run reports `novelty_base_hits: 0` with `sources S237 true`), so `sid not in
  reg_base` is vacuously true in every control.
- M7 (host threshold): every control's host line is `capture.txt:1` (`:54`), which resolves; K0 already
  fails on `rows == 0`, so no control isolates `host_ok >= 3`.
- M9 (snapshot digest): control trees always carry the intact frozen `frozen/src/*` (battery never
  corrupts them), so the sha256 gate never bites.
- M10 (residual for every row): no control creates `residual-dispatch.json`, `residual-results.json` or
  `residual/*.md` at all, so reading the residual unconditionally reads `None` everywhere — no behavior
  change. Killing it needs a should-PASS control (K3 + residual seat reading `fails` for a holds row)
  **and** a battery-summary that flags a should-PASS control failing — the current summary only flags
  should-FAIL controls that PASS and K3 failing (`:149-151`), so it is direction-asymmetric.
- M11 (base hits): structural, not a missing control — `base_hits` greps the fixed BASE `c8efaa3`
  (`counter :186-189`); the battery varies the tree rev, never BASE, so no tree-level control can plant a
  base hit. This conjunct needs a one-shot out-of-band assertion instead.
- M12 (rows == 5): equivalent mutant, not a gap — `quotes_ok == 5` implies 5 present rows (each `q_ok`
  requires a present row with a good quote, `counter :205`), so `rows == 5` is logically implied and no
  control can flip it without flipping another conjunct.

## Proposed corrections for the L1 to integrate before wave 2

1. Extend the battery with controls that kill the nine genuine-gap mutants, each a small variant of the
   existing scripted machinery: K6 out-of-window quote (resolving line outside the row's windows → kills
   M1); K7 wrong-role binding, name matched / `agent` wrong (M2); K8 garbage verdict token in results +
   report + forged residual seat reading `holds` (M3); K9 dispatch+results with the report line absent or
   divergent (M4); K10 results entry with `output: null` (M5); K11 cite an old sid present at BASE and
   flip its registry row at the control tree (M6 — needs a `flip_rows` generalization); K12 host line
   naming a blank/nonexistent capture line (M7); K13 control-tree commit corrupting
   `.ufo/waves/round-42/frozen/src/scrub.c` (M9); K14 K3-variant plus residual records reading `fails`
   for a holds row (M10).
2. Make the battery summary per-control-directional: record each control's expected verdict and flag any
   deviation (currently only `should_fail_accepted` and `control_accepted`, `:149-151`), otherwise
   counter-strengthening mutants (M10 class) are undetectable by construction.
3. For `novelty_base_hits == 0` (M11): assert BASE cleanliness once out-of-band (e.g., in the L1's
   receipt step) rather than via tree-level controls; or drop the conjunct if that assertion already
   exists elsewhere.
4. `rows == 5` (M12) is implied by `quotes_ok == 5`; keeping it is harmless defense-in-depth, but it is
   not independently tested and cannot be by this battery design.

## What this does and does not falsify

This does not falsify the C2 depth claim itself (rows SC1–SC5) and does not touch the frozen counter's
bytes; it falsifies the battery's adequacy as a guard for the counter: 11/12 probed weakening/strengthening
points pass the battery unchanged. Wave-2 seats `C2RevSC<n>`/`C2CritSC<n>` are still bound through
dispatch+results+report by the pristine counter (`counter :119-136`), and M8 shows the one place the
battery does bite.

## What I did not do

- Did not run the counter or battery against real wave-2 data (no `w2-dispatch.json`/`w2-results.json`
  exist yet); all runs are control trees.
- Did not mutate the battery script itself, nor counter checks outside the twelve probes (e.g. `QUOTE_RE`
  format looseness, `bad == 0` tolerance, the novelty-token check `n_ok`, the transcript cross-check).
- Did not verify the counter's correctness on the real entry beyond what the battery controls exercise.

## Restoration / cleanliness evidence

- Lane counter bytes after all runs: `sha256sum tools/check-scrub-record-r42.py` →
  `dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f` (unchanged, = frozen).
- Lane HEAD after all runs: `87c4f7c627e377e5f6d361498e8db9b3886d7953` (unchanged from session start;
  I ran no mutating git/jj command in the lane).
- `git ls-files .ufo/waves/round-42/w1/` → 0 entries: nothing under the wave-1 dir is tracked; this
  report and the receipts are the only lane-tree writes, both seat-prescribed.
- All mutants lived in the scratch fixture clone `/fast/scratch/hyaku/tsukuroi-r42/C2MutCounter/fx.FE4OsK`
  (commits `2ceb2d1e`, `8b54e78b`, `c4fda91b`, `17664b5b`, `0553535c`, `e5809e59`, `357ce19f`, `a16590f2`,
  `d1c7fd81`, `a052b8fe`, `5d96a191`, `83d021b9`, `f1617e7e`); the whole seat scratch dir is removed after
  receipt copy, per seat rules. No tool installs were needed (python 3.14.8, git 2.56.0 present).
