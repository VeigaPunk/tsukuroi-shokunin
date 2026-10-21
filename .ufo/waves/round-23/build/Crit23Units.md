# Crit23Units — C3 unit/arithmetic critique (round23 attempt1)

Seat: TsukuroiR23-2.Crit23Units-7 (critic, leaf). Source-only: read the five declared files; no commands, fetches, installs, or delegation. The digest is the supplied declaration and was not computed here.

## Axes
- calibration (C3 `unexplained_cohorts` 2 -> 0): primary.
- operability (C2 v2 `EXPANSION` / `CHECK_EACH` unit): secondary, through counting-unit leakage.
- quality/discernment trend: false provenance if rough-side rows are reverse-engineered to hit the reported totals.

## Frozen inputs (as reported, ground truth, not rerun)
- `preregister.json` `path_counts_as_reported`: rough build 25 / falsify 33; lane build 23 / falsify 29. Per-cohort net difference: build +2, falsify +4, pooled +6.
- `r22-closure.json` rechecks: the rough census is called an "approximate own path-binding census 25/33 vs checker23/29 (selector-normalization differences, not decisive)". C2 violations are 41/46, edit 16/17 is counted as unknown-tool 16/17, and bash is 2 (build only). The notes also list two typo paths and one internal URI among the out-of-binding reads.
- `structured-edit-observations.json`: CritRuntime edit request at line 15 has two recorded starts, a read of `.../CritRuntime.md:raw` at line 12 and a write of `.../CritRuntime.md` at line 13. OraclePathArtifact has three edit requests (lines 30, 33, 36), each with exactly one recorded start at the request line + 1.

## Finding 1: matching the net total is not the same as explaining it (blocking for C3 target 0)
Assumption under attack: "rough minus lane = +2/+4 (net six), so six rough-only items explain both cohorts."

Counterexample. Let \(B\) be the items both sides count, \(R\) the rough-only items, and \(L\) the lane-only items. The reported totals only fix \(|B|+|R| = 25\) and \(|B|+|L| = 23\) for build. That forces \(|R|-|L| = 2\), not \(|R| = 2\). A reconciliation that lists three rough-only build rows (say a `:raw` selector suffix, a typo path, and the internal URI) and one lane-only row (one event the rough side counts once but the lane splits into two components) satisfies the net exactly. The gross number of differing items is then 4, not 2. A checker that asserts only `rough - lane == 2` would score this cohort "explained" while the offsetting pair goes unexplained. Pooling has the same flaw one level up: a build +3 / falsify +3 split matches "net six" but contradicts the per-cohort +2 / +4.

Evidence that lane-only items can really happen: in the CritRuntime observation, one edit event carries two path-bearing components. A rough census that counts one failure per event and a canonical checker that counts per component diverge in both directions on that one event:
- Per-component can be higher: the event splits into two components.
- Per-component can be lower: normalizing the `:raw` selector maps the read back onto the bound report path.

So the sign of each item's difference is not fixed, and net arithmetic cannot imply gross arithmetic.

Impacted axes: calibration. The cohort metric would saturate too early.

## Finding 2: edit components may be joined to the wrong request (identity / false provenance)
For CritRuntime, the recorded starts (lines 12 and 13) come before the edit request (line 15). For OraclePathArtifact, every recorded start comes right after its request (request line + 1). The observation rows carry no `call_id` on recorded starts.

Falsifier: if a per-component census links adapter steps to requests by path or nearby line rather than by `call_id`, the line-12 read and line-13 write may be separate earlier calls. They would then be counted twice: once as standalone events and again as components of the line-15 edit. Any reconciliation row of the form "rough-only because of edit expansion" built on that link has a false source. [INFERENCE] The transcript bytes were not opened, so whether lines 12 and 13 are independent calls is not established here. The ordering asymmetry alone is enough to block an unjustified join.

Impacted axes: calibration, and operability if C2's v2 `CHECK_EACH` reuses the same join.

## Finding 3: the lane total may not be per-component, so the "canonical per-component" label needs proof
From the frozen numbers: \(41 = 23 + 16 + 2\) (build) and \(46 = 29 + 17 + 0\) (falsify). That is, path violations + unknown-tool edit + bash exactly. [INFERENCE] This closes only if each edit request counts once, as unknown-tool, and is not expanded into extra out-of-binding path components. If so, the lane unit is effectively per-event for edits, and "canonical per-component" describes it wrongly. If instead the lane does expand edit components and they all happen to be in-binding, the reconciliation must show that per row. Either way the C3 record must state the lane unit from the frozen r22 v1 checker semantics. It must not import the new v2 `EXPANSION` / `CHECK_EACH` rule, which would also break the declared C3/C2 separability and create a second authority for the lane side.

## Finding 4: the rough classifier is undeclared, which invites reverse fitting
The closure calls 25/33 "approximate" and "not decisive". If the C3 executor chooses rough-side inclusion rules after looking at the targets 25 and 33, any tuple set that hits those numbers will pass. That is tautological calibration.

## Tradeoff vs defect
These are all fixable defects, not tradeoffs the Rust judge must reject outright. They become grounds for rejection if the landed checker accepts any of these:
- a net-only or pooled-only assertion,
- a component join without `call_id`,
- a lane unit borrowed from v2.

## Smallest safe in-scope correction (C3 record + `tools/check-path-reconciliation.py` only)
1. Use a per-cohort row ledger. Each row is keyed by (cohort, seat, transcript_sha256, request_line, call_id, component_index, raw_path, normalized_path). Each row has a side in {both, rough_only, lane_only} and a closed reason code, for example `selector_suffix`, `typo_path`, `internal_uri`, `component_split`, or `component_merge`. A row with no reason fails.
2. Assert the full arithmetic per cohort, never pooled:
   - `both + rough_only == rough_reported`
   - `both + lane_only == lane_reported`
   - Also report gross = `rough_only + lane_only`.
   - Expected values: build `rough_only - lane_only == 2`, falsify `== 4`.
3. Join components only on an exact `call_id`, or on an explicit adapter link in the frozen transcript. If a recorded start comes before its request line and has no such link, treat it as a standalone event, not a component.
4. Declare each side's counting unit in the record. The rough unit comes from the frozen S085 source cell, stated before any counting. The lane unit comes from r22 v1 checker semantics. Never use v2 C2 code for the lane side.
5. Add a negative selftest fixture with an offsetting +1/-1 pair whose net still matches (e.g. build 3 rough-only + 1 lane-only). The checker must exit nonzero on it. Add a second fixture with a pooled +3/+3 split that must also fail.

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23-crit23units
Scope: executed=none
