# MutationEdit23 — write-authority-only edit mutant

## Scope and evidence

Design only. No mutant, command, detector, hash, import, runtime, or restoration operation was executed. The only output file is this report.

Axes: depth through distinct source-grounded edit decisions; operability through explicit edit/read/write authority; calibration through separating expected behavior from observed execution.

Read sources:
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/sources/edit-decision-policy.json`, lines 1–63.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/preregister.json`, lines 1–121.
- The explicitly authorized Godspeed skill.

The policy's supplied SHA-256 identity is `f6f73a1ac40a116145b38f07bf4c8c7bf147701b3e14265ae105c1559f96c805`. This is a declaration, not an independently computed digest. No implementation, manifest, event stream, or isolated source scratch copy was opened or modified.

## One proposed mutant

M1 replaces only the structured-edit authority conjunction, after unchanged structured-target validity checks:

```text
Pristine: allow_edit(P) = E(P) AND R(P) AND W(P)
Mutated:  allow_edit(P) = W(P)
Restored: allow_edit(P) = E(P) AND R(P) AND W(P)
```

Here E, R, and W mean exact membership of the structured target in `edit_paths`, `read_paths`, and `write_paths`, respectively. This is one predicate-expression substitution: a plausible defect that reuses write authorization for edit. It grants edit from `write_paths` alone and bypasses both explicit-edit and read-authority requirements. It does not change the separate authorization of an actual read or write adapter step.

This is a semantic mutation specification, not a claimed implementation diff: no checker source location is available within this seat's read binding. The normative policy and independent preregistration must remain unchanged. In particular, flipping the expected `WRITE_ONLY_EDIT` row to ALLOW would corrupt the oracle rather than faithfully test a mutated authorization gate.

## Bounded detector and controls

Use exactly the same finite corpus and unchanged oracle on pristine, mutated, and restored implementations. Every fixture below is hypothetical input data, not a modification of this seat's real binding. Let P be the exact local target `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-23/build/MutationEdit23.md`. Supply structured edit target metadata directly; do not infer a target from patch body text. An absent authority means its fixture list is empty.

| Case | E | R | W | Exact pristine/restored policy expectation | Expected M1 outcome |
| --- | --- | --- | --- | --- | --- |
| P_ALL — positive control | yes | yes | yes | `DECLARED_EDIT / ALLOW` | ALLOW; control passes |
| N_READ — read-authority-negative control | yes | no | yes | `WRITE_ONLY_EDIT / DENY` | ALLOW; detector must fail |
| N_READ_ONLY — read authority is not write authority | yes | yes | no | `READ_ONLY_EDIT / DENY` | DENY; control passes |
| N_EDIT — explicit-edit-negative control | no | yes | yes | `UNDECLARED_EDIT / DENY` | ALLOW; detector must fail |
| N_WRITE_ALONE — literal write-only authority | no | no | yes | DENY | ALLOW; detector must fail |

The isolated N_READ case deliberately retains E and W. Its rejection cannot be attributed to an absent edit declaration or absent write authority. N_EDIT isolates the other deleted conjunct. N_READ_ONLY prevents an indiscriminately permissive mutant from being confused with this specific write-authority defect. P_ALL prevents an always-deny detector from looking adequate.

Exact policy-oracle triples, including the source's reason strings:

```text
("DECLARED_EDIT", "ALLOW", "Exact target is predeclared for edit and for both read and write")
("WRITE_ONLY_EDIT", "DENY", "Edit also needs its explicit target read authority")
("READ_ONLY_EDIT", "DENY", "Read authority never grants a write")
("UNDECLARED_EDIT", "DENY", "No implicit edit permission from generic report ownership")
```

For N_WRITE_ALONE both explicit-edit and read authority are absent. The available policy does not define which denial reason has precedence when requirements overlap. Its exact decision assertion is DENY; do not invent an exact diagnostic precedence.

The proposed detector's exact mutation-failure assertions are:

```text
N_READ: expected WRITE_ONLY_EDIT/DENY; got ALLOW
N_EDIT: expected UNDECLARED_EDIT/DENY; got ALLOW
N_WRITE_ALONE: expected DENY; got ALLOW
```

These strings define proposed assertion messages; they are not observed output or a claim about existing checker stderr. P_ALL and N_READ_ONLY must have no assertion failures under M1. A read-authority leak is caught specifically by N_READ, not by merely finding a policy row that says DENY.

## Expected detector placement

The behavior-bearing detector belongs at the preregistered C2 schema-v2 structured-edit audit boundary, using the above policy expectations as its independent oracle. C1's frozen decision-row checks provide the normative expectations, but must not be claimed to kill a C2 predicate mutant merely because the row `WRITE_ONLY_EDIT` remains DENY. Preregistration explicitly separates C1's document/source contract from C2's authority audit.

Any recorded adapter reads or writes remain separately checked under `EXPANSION / CHECK_EACH`. This probe does not infer opaque patch effects, actual reading, filesystem effects, recorder completeness, or native enforcement. No native restrictive task toolset is claimed.

## Output, verdict, and restoration evidence

Actual detector output: none; no detector was run.

Expected bounded results, not observations:
- Pristine: all five case assertions pass.
- M1: exactly N_READ, N_EDIT, and N_WRITE_ALONE fail; P_ALL and N_READ_ONLY pass.
- Restored: all five case assertions pass again.

Actual verdict: **NOT EXECUTED — kill/survival is unmeasured**. This is not a killed mutant and not an observed survivor. A future executed probe can call M1 killed only after the pristine detector passes and the unchanged detector rejects M1. A baseline failure is inconclusive. If the mutant passes, that is a coverage finding, not permission to relax the contract. Exact restoration must still be demonstrated for any future non-disposable scratch mutation.

Identity/restoration record:

| State | Digest evidence | Mutation/restoration evidence |
| --- | --- | --- |
| Before | Supplied policy identity above; not independently computed | Policy read only |
| Mutated | No mutated bytes exist from this seat; no digest measured | M1 exists only as report text |
| After/restored | After digest unobserved; no restoration digest measured | No source mutation was issued, so no source restoration was required or performed |

This report does not claim byte-for-byte identity from a hash comparison. The available evidence is narrower: this seat issued no write or edit to the policy, preregistration, implementation, or any scratch source. Only this authorized report was written. No installation, update, delegation, production integration, or VCS operation occurred.
