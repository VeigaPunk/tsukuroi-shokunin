# FxC3Canonical — falsify review of canonical_event() vs lane requested_path()

Attacked claim: C3 (calibration, `unexplained_cohorts` 2 -> 0), specifically the
per-event `canonical_path_count == retained_path_count` gate in
`candidate/tools/check-path-reconciliation.py` and its total-level companions.

Method: static read-only comparison of `canonical_event()` / `canonical_base()` /
`_local()` (candidate, declared SHA256 fd0393be…6b, supplied not computed) against
`classify()` / `requested_path()` / `local()` in `snapshot/tools/check-seat-bindings.py`,
plus disposition logic in `derive()` / `cohort_findings()` and the L1 mutation record.
Nothing executed. Frozen r22 events/bindings/audit were NOT in this seat's read set, so
no statement below asserts which envelope classes actually occur in r22 data.

## Verdict

No C3 falsifier found. The per-event check fails closed on every divergence found,
so no spelling turns an unexplained row into `agree` / `selector-normalization` /
`unit-difference`. It is a real *replay* check against recorded lane output, but
**not independent** of the lane's own path semantics, and the two total-level checks
(`RECONCILIATION-CANONICAL-MISMATCH`, `RECONCILIATION-ARITHMETIC`) can't fire on their own
(their inputs are fully determined by the other checks).

## 1. Per-component spellings (literal tool, dict args, non-empty string path): no divergence (bounded search)

I compared them branch by branch. For `tool in {read, grep, glob, write}` with dict args
and a non-empty string `path`, the two sides compute the same per-component predicate:

- Fetch skip: same two regexes (`(?i)^https?://`, `^[^/:\s]+:[0-9]+/`), applied to the
  raw component before selector stripping on both sides. Lane emits FETCH (not PATH).
  Canonical skips the component. PATH counts match.
- `skill://godspeed`: both short-circuit before selector stripping. Both treat it as
  clean only if it is in that tool's authority list, and denied otherwise (lane through
  the not-in-authority branch, canonical through `not _local`). `skill://godspeed:raw`
  is denied on both sides.
- Selector grammar: same condition (`selector and ':' in value`), same `split(':')`,
  same token set `raw|img|conflicts` and same regex `\d+(?:[-+]\d*)?|-\d+` per
  comma part. Selector is enabled only for read/grep on both sides, and glob/write are
  never stripped. Edge cases checked: trailing `:` (empty token, invalid on both sides),
  repeated tokens (`:raw:raw:img`, valid on both sides), and `:-5` / `:1+` (valid on both).
- Locality: `_local` and `local` are the same predicate for `str` input. The lane's extra
  `isinstance`/`bool` guards are implied by `startswith(LANE + '/')`.
- Authority lookup: `write_paths` for write and `read_paths` otherwise, on both sides.
  The `;` split applies to grep/glob only, on both sides. Empty components from `a;` or
  `;` are denied on both sides.

## 2. Event-envelope divergences (real), all fail closed

`canonical_event` and `rough_event` only recognise literal tool names and use
`event.get('args') or {}`. The lane normalises and unwraps more:

| Class | Lane (retained PATH) | canonical | rough | Disposition |
|---|---|---|---|---|
| `functions.read`/`functions.grep`/… with denied component(s) | N (prefix stripped) | 0 (`tool not in ROUGH_TOOLS`) | 0 (`unknown`) | unexplained |
| `multi_tool_use.parallel` / `parallel` / `functions.multi_tool_use.parallel`, nested ≤8, with denied child paths | N, all at parent site | 0 | 0 | unexplained |
| read/grep/glob/write with `args` None / `{}` / `[]` / `""` / `0` (coerced to `{}`) | 0 (raises, SCOPE-SCHEMA) | 1 (`''` denied) | 1 | unexplained |
| `path` missing, `''`, or non-string (e.g. `5`, list) | 0 (SCOPE-SCHEMA) | 1 (`str()`-coerced, denied) | 1 | unexplained |
| truthy non-dict args (e.g. `['x']`) | 0 (SCHEMA) | 0 | 1 | unexplained (selector guard compares `'' != ''`) |
| prefixed/wrapped events whose paths are all allowed | 0 | 0 | 0 | agree (correct) |

Why no false explanation is possible: all three non-unexplained dispositions require
`len(canonical) == kept` (`agree` directly, `selector-normalization` through
`not canonical and kept == 0`, `unit-difference` through `kept == len(canonical)`). In every
envelope class the two values differ (0 vs N, or 1 vs 0). Rows are compared per event,
not summed, so one class cannot offset another. Wrapped or prefixed events with clean
children correctly agree at 0/0/0.

Consequence for C3 [INFERENCE]: if any r22 event belongs to a denied envelope class,
C3 shows FAIL rather than a false PASS. A landed PASS therefore implies none exist in the
frozen cohorts. I could not confirm that here because the snapshot events were not in my
read set.

## 3. Is canonical == retained an independent check?

Partly. It is independent in *execution*: a fresh recomputation is compared against
the recorded `audit.json` findings. That catches forged, dropped or duplicated retained
findings at a site, audit drift (also pinned by digest), and the envelope classes above.
It is **not independent in semantics**: section 1 shows `canonical_event` copies the lane's
path predicate (same regexes, token set, locality rule and authority choice). Any grammar
defect in the lane, such as a too-permissive token, would be reproduced and reported as
`agree`. So the check measures the count unit and its reproducibility, not whether the
lane's classifications are correct. That fits C3's stated scope ("explains
counting-method differences"). The labels "canonical" and "local selector grammar"
overstate independence, which hits the provenance / duplicate-authority axes.
Separately, the classifier revision that *produced* r22 `audit.json` is not pinned in
`frozen/reconciliation-inputs.json`. Only events/bindings/audit/census are pinned, so
the replica's fidelity to the r22-era producer rests on per-event agreement alone
[INFERENCE].

## 4. Total-level checks can't fire on their own

Suppose the cohort has no unexplained row and no orphan. Every explained row has
canonical == kept, so `canonical_path == retained_path`. It follows that
`RECONCILIATION-CANONICAL-MISMATCH` fires only when there are orphans, and orphans already
raise `RECONCILIATION-ORPHAN-FINDING`. Likewise the per-row contributions to
`rough − retained` are 0 for `agree`, +1 for `selector-normalization`, and −(kept−1) for
`unit-difference`. So `RECONCILIATION-ARITHMETIC` is an identity and also fires only
alongside orphans or unexplained rows. No selftest case expects either finding ID, and
`l1-mutation.json` (27/27 killed) contains no mutant on either line. The prediction is
that deleting either line would survive the selftest (an equivalent mutant)
[INFERENCE, not executed].

## Impacted axes

calibration (C3 evidence strength), provenance/labeling (false-independence wording),
duplicate authority (the selector/locality grammar now lives in two copies). No impact
on C1/C2. No frontier saturation claim is affected.

## Smallest in-scope remedy

These are fixable defects, not tradeoffs for the judge to reject:
1. Relabel `canonical_event`/`canonical_base` docstrings as "literal-tool replica of the
   r22 lane `requested_path` path predicate; not an independent classifier; envelope
   classes (`functions.` prefix, parallel wrappers, falsy/non-dict args, missing or
   non-string path) deliberately surface as unexplained."
2. Add three selftest controls that pin the fail-closed envelope behaviour:
   - `functions.read` of a denied path with retained `S:0`, expecting
     `RECONCILIATION-UNEXPLAINED`.
   - `multi_tool_use.parallel` with a denied child and retained `S:0`, expecting
     `RECONCILIATION-UNEXPLAINED`.
   - read with `args: {}` and no retained finding, expecting `RECONCILIATION-UNEXPLAINED`.
3. Delete `RECONCILIATION-CANONICAL-MISMATCH` and `RECONCILIATION-ARITHMETIC` because they
   can't fire on their own. Alternatively, keep them only with selftest cases that isolate
   them, which is impossible by the identity above, so deletion is the safer choice.

Reviewed-SHA256: fd0393be9140579424bdfc3c099b2b82fee11ccf9306d926c998235ce7ee1a6b
Predicate: r23f-fxc3canonical
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
