# MutFxBindings — three design-only v2 mutation probes

## Scope, axes, and evidence

Attacked claim: **C2**, the explicit schema-v2 recorded-request audit authority. The axes are exact-target authorization, manifest/trace validity discrimination, and detector coverage without broadening authority. C1's document decisions and C3's reconciliation implementation were not inspected; no C1/C3 or frontier improvement is claimed.

This seat performed local source inspection and wrote this report only. No command, detector, import, hash, mutation, source edit, fetch, installation, or child dispatch occurred. The target digest in the receipt is supplied identity, not an independently measured digest.

Inspected evidence:

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-seat-bindings.py`, lines 1–396: structured edit classifier at 119–130; v2 manifest authority at 144–162; completeness and event evaluation at 171–207; literal v2 controls at 294–337; detector assertions at 338–353.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json`, lines 26–55 and 110–115: C2 is finite, post-hoc audit authority, not runtime prevention or universal trace completeness.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/.ufo/waves/round-23/measure/l1-mutation.json`, lines 1–257: the recorded seat-bindings mutants numbered 0–9 do not contain any of the three replacement lines below. In particular, its line-128 mutant grants read-path membership, not semicolon-prefix membership; its authority mutants do not remove the edit-list type check; its mode mutant forces the result flag, not a v2 exemption from trace completeness.

**Actual detector output for pristine, mutated, and restored bytes: none. Verdict for each probe: DESIGNED / UNEXECUTED, neither killed nor survived.** Every projected result below is explicitly an **[INFERENCE]** from the inspected code, not captured output or an observed falsification. The existing log's 27/27 result is evidence only for its recorded mutants.

## Shared literal valid manifest B

Use this exact manifest for probes 1 and 3. These are detector input data, not requests to access the example paths.

```json
{
  "schema": "tsukuroi-seat-bindings-v2",
  "seats": [
    {
      "name": "A",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/source",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/A.md"
      ],
      "write_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/A.md"],
      "edit_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/A.md"],
      "commands": [],
      "fetches": []
    }
  ]
}
```

## Probe 1 — first-component parsing silently widens edit authority

**Claim attacked:** C2's exact predeclared structured-edit destination. The concrete falsifier is a PASS for the full semicolon-containing spelling below, which is not a member of `edit_paths`. This concerns recorded spelling authority only; it does not assume the tool executes two filesystem operations.

**Plausible defect:** reuse multi-path parsing from grep/glob, but retain only its first component when checking an edit target.

**One-line mutant:** target source line 128.

Original:
```python
    if value not in binding['edit_paths']:
```
Replacement:
```python
    if value.split(';', 1)[0] not in binding['edit_paths']:
```

**Killing literal control:** manifest B and the following complete trace.

```json
{
  "schema": "tsukuroi-seat-events-v1",
  "seats": [
    {
      "name": "A",
      "agent": "agent-A",
      "complete": true,
      "events": [
        {
          "tool": "edit",
          "args": {
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/A.md;/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/production",
            "stream_content": null
          }
        }
      ]
    }
  ]
}
```

**Expected detector:** assert exit/code 1, status `FAIL`, exactly `SCOPE-EDIT-DENIED` at `A:0`, one request, and both audit-mode flags equal to 1. Check the complete spelling, without splitting or canonicalizing it in the control.

**Projected output [INFERENCE]:** pristine `(1, FAIL, [SCOPE-EDIT-DENIED], request_audit_mode=1, structured_edit_mode=1)`; mutant `(0, PASS, [], request_audit_mode=1, structured_edit_mode=1)`. Restoration would reproduce the pristine expectation, but no restoration run occurred.

**Existing coverage boundary:** the v2 alternate-spelling fixture at 307–308 contains slash, dot-segment, selector, relative, URI, and case variants, but no semicolon spelling. Existing semicolon controls exercise grep, not `classify_edit`. This mutant is therefore a predicted survivor of the current selftest, not a measured survivor.

**Smallest remedy:** preserve the current exact membership predicate; add this single literal negative edit case to the v2 selftest. Do not add edit-path splitting or infer an adapter expansion.

## Probe 2 — empty string masquerades as an empty edit-target list

**Claim attacked:** C2's validated, explicit v2 manifest authority. The concrete falsifier is a PASS and `structured_edit_mode=1` for a manifest whose `edit_paths` is a string rather than a list.

**Plausible defect:** simplify validation on the mistaken assumption that uniqueness and iteration already establish list shape. An empty string passes both remaining checks vacuously.

**One-line mutant:** target source line 159. The preceding exact-key check and following subset check remain unchanged.

Original:
```python
                        or not isinstance(edits, list) or len(edits) != len(set(edits))
```
Replacement:
```python
                        or len(edits) != len(set(edits))
```

**Killing literal control:** this complete malformed manifest and the complete clean-read trace below. The clean read isolates manifest validation from edit-request shape and target permission.

```json
{
  "schema": "tsukuroi-seat-bindings-v2",
  "seats": [
    {
      "name": "A",
      "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
      "read_paths": [
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/source",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/A.md"
      ],
      "write_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/A.md"],
      "edit_paths": "",
      "commands": [],
      "fetches": []
    }
  ]
}
```

```json
{
  "schema": "tsukuroi-seat-events-v1",
  "seats": [
    {
      "name": "A",
      "agent": "agent-A",
      "complete": true,
      "events": [
        {
          "tool": "read",
          "args": {"path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/source"}
        }
      ]
    }
  ]
}
```

**Expected detector:** assert exit/code 2, status `CANNOT_EVALUATE`, exactly `SCOPE-SCHEMA` at `input`, zero evaluated requests, and both audit-mode flags equal to 0. The empty list `[]` remains a distinct, valid declaration; this control must not change that contract.

**Projected output [INFERENCE]:** pristine `(2, CANNOT_EVALUATE, [SCOPE-SCHEMA], request_audit_mode=0, structured_edit_mode=0)`; mutant `(0, PASS, [], request_audit_mode=1, structured_edit_mode=1)`. Restoration would reproduce the pristine expectation, but no restoration run occurred.

**Existing coverage boundary:** the v2 cases at 326–332 cover missing, duplicate, nonlocal/skill, non-readable, non-writable, and empty-list edit declarations, but not an empty string. With the type check removed, a missing value still raises a caught `TypeError`, duplicates still fail uniqueness, and the invalid nonempty lists still fail their remaining checks. This mutant is a predicted current-selftest survivor, not a measured survivor.

**Smallest remedy:** retain `isinstance(edits, list)` and add the empty-string manifest as one negative v2 case. No authority or schema expansion is needed.

## Probe 3 — v2 fast path ignores an explicitly incomplete trace

**Claim attacked:** C2's evaluability and mode reporting for the supplied recorded trace. Honoring a supplied `complete: false` does not claim that a supplied `true` proves universal recorder completeness.

**Plausible defect:** exempt the new v2 mode from the generic trace-completeness check while preserving v1 behavior.

**One-line mutant:** target source line 177.

Original:
```python
            if not seat['complete']:
```
Replacement:
```python
            if not seat['complete'] and not v2:
```

**Killing literal control:** manifest B and this complete trace document. The edit target is authorized; only the explicit incompleteness makes the audit unevaluable.

```json
{
  "schema": "tsukuroi-seat-events-v1",
  "seats": [
    {
      "name": "A",
      "agent": "agent-A",
      "complete": false,
      "events": [
        {
          "tool": "edit",
          "args": {
            "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/drafts/A.md",
            "stream_content": null
          }
        }
      ]
    }
  ]
}
```

**Expected detector:** assert exit/code 2, status `CANNOT_EVALUATE`, exactly `SCOPE-TRACE-INCOMPLETE` at `A`, `incomplete_seats=1`, `present_incomplete_seats=1`, one evaluated request, and both audit-mode flags equal to 0. Assert both status and finding, not merely that the authorized edit itself has no denial.

**Projected output [INFERENCE]:** pristine `(2, CANNOT_EVALUATE, [SCOPE-TRACE-INCOMPLETE], request_audit_mode=0, structured_edit_mode=0)`; mutant `(0, PASS, [], request_audit_mode=1, structured_edit_mode=1)` with both incompleteness counters incorrectly zero. Restoration would reproduce the pristine expectation, but no restoration run occurred.

**Existing coverage boundary:** the explicit incomplete-trace fixtures at 241 and 257–258 use v1. The v2 fixtures inherit `complete: true` from `trace()` at 213–214, including the separately assembled malformed-then-bash trace. No inspected v2 case supplies `complete: false`. This mutant is a predicted current-selftest survivor, not a measured survivor.

**Smallest remedy:** retain the schema-independent completeness guard and add this one literal incomplete v2 trace. Do not infer or attempt to prove actual recorder completeness.

## Bounded detector and verdict

The proposed detector is the existing finite `evaluate()`/`selftest()` mechanism, augmented with these three literal cases and the required fields above. In a separately authorized isolated scratch probe, the same augmented detector must pass on pristine bytes, fail on each single mutant, and pass again on restored bytes. A pristine failure would be inconclusive, not a kill. Such execution is outside this seat's empty command allowlist and was not performed.

The bounded inspection covered the entire assigned checker, all its v2 literal controls, and the complete supplied L1 mutation log. It found no pristine acceptance of these three falsifiers: the current exact membership, list-type, and completeness predicates reject them by source reasoning. It did identify three unmeasured negative-control gaps against three distinct, unrecorded one-line defects. No actual C2 failure, killed mutant, observed surviving mutant, or frontier movement is established.

The smallest recommended change is test-only: three negative v2 cases with literal inputs and explicit result/mode assertions. The current production predicates already express the required behavior and should remain unchanged. Only L1 may integrate that change; this seat changed no checker, fixture, production, sibling, or VCS bytes.

## Output and restoration evidence

- Actual pristine detector output: none; not run.
- Actual mutated detector output: none; mutants were specified as text only.
- Actual restored detector output: none; no source mutation occurred, so no restoration operation was necessary.
- Before identity: the supplied SHA-256 in the receipt, not independently computed.
- After/restored hashes: not measured; no cryptographic before/after equality is claimed. Source preservation evidence is this seat's read-only access to the checker and sole filesystem write to the assigned report.
- Tool installs/updates: none.

Lane bounds: leaf member — no subagent dispatch.

Reviewed-SHA256: 4e00ab1fe9f5e35e20eeeb849bab0cc185c708fded6ee00ddcd96292b68cf3d6
Predicate: r23f-mutfxbindings
Scope: executed=none
