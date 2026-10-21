# MutFxEdit — round23 attempt1, design-only falsification

## Scope and axes

Attacked claim: **C1**, the eight finite source-grounded structured-edit authority decisions, not runtime enforcement. Axes: exact provenance binding, observation-kind fidelity, and visible-only scope disclosure. These are C1 subproperties, not three additional claimed capabilities. C2, C3, and frontier dominance were not tested.

Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/tools/check-edit-contract.py` (lines 1–283 read). The reviewed SHA-256 is supplied identity only, not independently computed.

Also read the declared preregistration and the complete recorded L1 mutation log at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/candidate/.ufo/waves/round-23/measure/l1-mutation.json`. None of the three original-to-mutated line replacements below occurs among its seven edit-contract mutants or its recorded pre-log fixes. The existing L1 mutations cover prose-table agreement, preregistration comparison, shape-set checks, dropping the prose-limit check, row-key exactness, and source ownership/tier; the proposals below target different behavior-bearing points.

**Execution boundary:** NO-EXEC / NO-FETCH. Only authorized reads and this report write were performed. No command, import, selftest, hashing, installation, delegation, source mutation, or restoration was performed. Every predicted result below is **[INFERENCE]**, not an actual detector output. Code snippets are inert design material; relative strings inside literal cases are existing fixture values, not accessed paths.

## M1 — detach the declared source pointer from its evidence

Claim/axis: C1 / exact provenance binding. Plausible defect: validating the evidence object but forgetting that the policy must name that same evidence carrier.

Original line 131:

```python
        if data.get('source_path') != EVIDENCE or evidence is None or not evidence_ok(evidence):
```

One-line replacement:

```python
        if evidence is None or not evidence_ok(evidence):
```

Literal existing selftest case that should kill it (line 233):

```python
        ('source-path-swap', json.dumps(dict(data, source_path='.ufo/waves/round-23/sources/r22-rough-census.txt')), prose, sources, ev, pr, 1, 'EDIT-EVIDENCE'),
```

Concrete mutant falsifier: otherwise-clean fixtures retain valid S086 observations while the policy's `source_path` is changed to the r22 census carrier. This challenges the C1 source-grounding promise, not authorization of any filesystem action.

[INFERENCE] Pristine/restored evaluation of this case should return code 1, status `FAIL`, findings `['EDIT-EVIDENCE']`, and `validated_edit_decisions=0`. Under this mutant it should return code 0, status `PASS`, no findings, and `validated_edit_decisions=8`. The case's existing expected-code/expected-ID assertion should therefore fail, making the unchanged full `selftest()` return 1.

Smallest in-scope remedy: retain the exact `source_path != EVIDENCE` comparison and its existing `source-path-swap` negative control. No new exception, compatibility path, or production change is justified by an unexecuted proposal.

## M2 — accept a write observation as structured-edit evidence

Claim/axis: C1 / observation-kind fidelity. Plausible defect: treating a recorded adapter write as interchangeable with the top-level observed edit request.

Original line 105:

```python
        if (row.get('tool') != 'edit' or not isinstance(keys, list) or len(keys) != len(set(keys))
```

One-line replacement:

```python
        if (row.get('tool') not in ('edit', 'write') or not isinstance(keys, list) or len(keys) != len(set(keys))
```

Literal existing selftest case that should kill it (line 232):

```python
        ('evidence-wrong-tool', json.dumps(data), prose, sources, mut(lambda m: m['observations'][1].update(tool='write')), pr, 1, 'EDIT-EVIDENCE'),
```

Concrete mutant falsifier: the second observation still has the accepted path/old_string/new_string metadata shape but now declares its top-level tool as `write`. The mutant would accept that substitution. This is distinct from the legitimate `write` in the clean fixture's `recorded_starts`: that child adapter observation is not the top-level `tool` being validated.

[INFERENCE] Pristine/restored evaluation should return code 1, status `FAIL`, findings `['EDIT-EVIDENCE']`, and `validated_edit_decisions=0`. Mutated evaluation should return code 0, status `PASS`, no findings, and `validated_edit_decisions=8`. The literal case should fail its existing assertion and make the unchanged full `selftest()` return 1.

Smallest in-scope remedy: keep top-level `row['tool']` restricted to `edit`; keep adapter `recorded_starts` conceptually separate. The existing wrong-tool case already expresses the needed negative control; no broader tool-semantics claim is warranted.

## M3 — leak an HTML-commented limitation into visible prose

Claim/axis: C1 / visible-only scope disclosure. Plausible defect: accidentally removing the slice bound while stripping an HTML comment.

Original line 66:

```python
                pieces.append(line[cursor:start])
```

One-line replacement:

```python
                pieces.append(line[cursor:])
```

Literal existing selftest case that should kill it (line 221):

```python
        ('hidden-limit', json.dumps(data), prose.replace('It is not native permission enforcement', '<!-- It is not native permission enforcement -->'), sources, ev, pr, 1, 'EDIT-LIMIT-MISSING'),
```

Concrete mutant falsifier: all eight visible decision rows remain correct, but the prose's required non-enforcement phrase is hidden in an HTML comment. The erroneous slice retains that same-line comment text in `visible(text)`, allowing the substring check to find an invisible limitation. Unlike L1 edit-contract mutant 4, this does not remove the prose-limit condition; it corrupts the shared visibility carrier used by that condition.

[INFERENCE] Pristine/restored evaluation should return code 1, status `FAIL`, findings `['EDIT-LIMIT-MISSING']`, and `validated_edit_decisions=0`. Mutated evaluation should return code 0, status `PASS`, no findings, and `validated_edit_decisions=8`. The literal case should fail its existing assertion and make the unchanged full `selftest()` return 1.

Smallest in-scope remedy: preserve the `cursor:start` bound and the existing hidden-limit negative control. Do not weaken the visible-prose requirement or replace it with a search of raw Markdown.

## Detector, verdict, and restoration evidence

Expected detector for all three designs: the target's unchanged bounded `selftest()` (lines 165–245), using its independent literal fixture. Lines 238–242 compare the returned code and required finding; a mutated `PASS` cannot satisfy any of the three negative cases above. Lines 243–245 convert a failed observation into detector exit 1. For an actual mutation verdict, the same detector must pass on pristine bytes, fail on the isolated one-line mutant, and pass again on exact restored bytes. A baseline failure would be inconclusive, not a killed mutant.

| Design | Actual pristine output | Actual mutant output | Actual restored output | Empirical verdict |
|---|---|---|---|---|
| M1 | Not run | Not run | Not run | UNEXECUTED; kill predicted only |
| M2 | Not run | Not run | Not run | UNEXECUTED; kill predicted only |
| M3 | Not run | Not run | Not run | UNEXECUTED; kill predicted only |

Before/after hash evidence: before identity is solely the supplied SHA-256 in the receipt below. No independently measured before, mutant, or after hash exists; hashing was forbidden. No target or scratch bytes were written, so there are no mutated bytes to restore. The only write was to this exact report path. This is tool-action evidence of non-mutation, not a hash-verified restoration claim.

Bounded-search conclusion: the complete allowed target and L1 log were inspected, and the three distinct one-line changes above were matched to concrete existing negative cases. No current C1 counterexample was established by that design-only review, and no claim is made that other defects are absent. No actual kill, survivor, newly improved axis, or Pareto/frontier movement is established. The smallest present remedy is therefore no source change: preserve the existing guards and tests rather than treating predicted kills as additional execution evidence.

Lane bounds: leaf member — no subagent dispatch.
Reviewed-SHA256: 620f3e5bad34c4ba77a0f0e458bedd79cb05b04a5b1d90200c0baf60038e5081
Predicate: r23f-mutfxedit
Scope: executed=none
