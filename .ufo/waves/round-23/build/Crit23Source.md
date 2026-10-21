# Crit23Source — round 23 attempt 1 critic report

Seat: Crit23Source (UFO-FSD critic, leaf). NO-EXEC, NO-FETCH. Source-only review of the declared files:
`preregister.json`, `sources/godspeed-directive.txt` (the copied directive; `skill://godspeed` was not resolvable in this runtime), `sources/r22-closure.json`, `sources/structured-edit-observations.json`. The checker sources (`tools/check-seat-bindings.py`, `tools/check-edit-contract.py`, `tools/check-path-reconciliation.py`) are **not** in my read binding. Any statement about what they currently do is marked [INFERENCE].

Axes named: depth (C1), operability (C2), calibration (C3), plus provenance and identity integrity as cross-cutting guards.

## Verdict

The observation source (S086) is honest in its own `scope` line. The risk is downstream: the C2 v2 audit authority and the C1 `EXPANSION`/`WRITE_ONLY_EDIT` decisions could read harness metadata as if it were native API semantics or proof of effects. That misreading happens if three things are treated as authority:

- the adapter tool label `edit`,
- the `argument_keys` shapes,
- the `recorded_starts` rows.

The local evidence contains a concrete counterexample to that reading. This is a fixable defect, not a tradeoff. But the Rust judge must reject any C2/C1 artifact that claims a recorded start proves that an effect happened, or that the `edit` label is a native API contract.

## Counterexample 1: recorded starts are not the edit request's effects, and attribution is underdetermined

Evidence (`structured-edit-observations.json`, the CritRuntime row):

- The request is at `request_line: 15`, `tool: "edit"`, call_id `toolu_014nToY7USd3cckcqeieNJ4o`.
- Its `recorded_starts` are at line 12 (`read`) and line 13 (`write`). Both lines come **before** the request line.
- The starts' tool names (`read`, `write`) are not the requested tool (`edit`).
- No `recorded_starts` row carries a `call_id`. The linkage between a request and its starts is not recorded anywhere in the source.

Falsifier:

- Take a v2 binding where the target is in `read_paths` and `write_paths` but **not** in `edit_paths`.
- An edit request to that target should be `UNDECLARED_EDIT → DENY`. Under the preregister's own row (`DECLARED_EDIT` needs edit plus read plus write) it is also not `ALLOW`.
- If the auditor evaluates the edit through its recorded adapter steps, each step is individually authorized: the read is in `read_paths` and the write is in `write_paths`. The decision then flips from DENY to clean. The same substitution turns `WRITE_ONLY_EDIT` into a pass whenever a read start happens to be recorded nearby.
- The CritRuntime row shows this shape is real: an edit whose only recorded steps are a read and a write.

Second falsifier (line-adjacency attribution):

- OraclePathArtifact has three edits to the same path. Each start sits at `request_line + 1` (31, 34, 37).
- CritRuntime's starts sit at `request_line − 3` and `request_line − 2`. This is consistent with streaming-time execution logged before the finalized assistant message ([INFERENCE] from the `stream_content` key).
- So no single proximity rule fits both rows. Any linkage rule that guesses from line position will either mis-assign starts between neighbouring same-path edits or detach CritRuntime's starts entirely.

Impacted axes: operability (C2 verdicts), depth (C1 rows `UNDECLARED_EDIT`, `WRITE_ONLY_EDIT`, `EXPANSION`).

## Counterexample 2: argument-key shapes are adapter-specific, and the sample is too small to generalize

Evidence:

- CritRuntime's `edit` has keys `{path, stream_content}`.
- OraclePathArtifact's `edit` has keys `{i, new_string, old_string, path}`.
- These are two incompatible shapes under the same label.
- `r22-closure.json` records `edit16/17=unknown-tool16/17`: 33 edit calls that the r22 checker did not know.
- S086 contains 4 of those 33, from 2 seats.

Falsifier:

- Suppose a classifier derives "structured edit" from these 4 rows, for example "`path` key plus body field means structured target".
- Then a third adapter shape among the 29 unobserved calls will be silently classified under a contract it was never observed to follow. An example would be a multi-target key, or a patch body without `path`.
- That third shape should land in `OPAQUE_PATCH → UNKNOWN`. Instead it is given a target that was inferred, not structured.

This is premature saturation, and it misattributes the meaning of harness argument names to a native API.

Impacted axes: depth (the C1 `OPAQUE_PATCH` row), operability (C2).

## Counterexample 3: the `:raw` selector is one hidden normalization authority shared by C2 and C3

Evidence:

- CritRuntime's line-12 read path is `…/round-22/build/CritRuntime.md:raw`. That is a read selector, not the filesystem spelling of the target.
- `r22-closure.json` attributes the rough-versus-lane census gap (25/33 vs 23/29) to "selector-normalization differences".

Falsifier:

- If the C2 auditor strips `:raw` before matching, it uses an alternate spelling to match the target list. That conflicts with `EDIT_TRAVERSAL` ("No dot-segment or alternate spelling expands the target list") and with `EDIT_EXTERNAL`, since the selector is effectively an internal URI form.
- If the auditor does not strip it, the same read becomes out-of-binding.
- Either choice also decides part of C3's 25→23 / 33→29 explanation.
- The preregister's `separability` claims that C2 and C3 read disjoint inputs. A single unshared, undeclared selector rule would therefore be a duplicate authority. C2 and C3 could each pick a different answer for the same event and both report green ([INFERENCE]: I cannot read the checkers to see which rule each uses).

Impacted axes: calibration (C3), operability (C2), and the separability claim.

## Counterexample 4: S086 provenance is thinner than an authority needs

Evidence:

- S086 carries `transcript_sha256` per row and `accessed: 2026-10-21`.
- It has no collector identity, no revision or commit binding, and no statement that it is exhaustive.
- Its rows come from `TsukuroiR22.*` agents, not from round-23 waves.

Falsifier: if C2 tests or contract prose cite S086 as the definition of edit semantics, a round-23 event shape that does not appear in S086 is judged against a fixture rather than a declared rule. Any "observed" claim then rests on a digest the seat cannot verify. This is false provenance by elevation: a fixture gets promoted into authority.

Impacted axis: operability (C2 evidence chain).

## Smallest safe in-scope correction

All of these fit inside the v2 contract, decision prose and checker. None needs native enforcement, history rewrites or new capability.

1. **The request decides.** Compute the edit decision only from the request's own structured target: the `path` key when it is present and has exactly one value. Match it as an exact string against `edit_paths ∩ read_paths ∩ write_paths`. Recorded starts never rescue an edit request and never replace it.
2. **Check each start under its own tool.** For `EXPANSION → CHECK_EACH`, check each recorded start against the binding of its own tool: read against `read_paths`, write against `write_paths`, edit against `edit_paths`. Label these results `recorded_start`, never `effect` or `completed`.
3. **Link only by call_id.** Link a start to a request only through an explicit `call_id`. Where the id is absent, as in all 4 S086 rows, report `linkage: UNKNOWN`. Do not infer linkage from line adjacency.
4. **Fail closed on unrecognized shapes.** Any argument-key shape outside an explicitly enumerated v2 list falls to `OPAQUE_PATCH → UNKNOWN`. The tool label `edit` alone confers nothing.
5. **Declare one selector rule.** Write one frozen rule for selector suffixes such as `:raw`, recommended as "no stripping; separate spelling". Cite it identically from the C2 audit and the C3 reconciliation, so the census arithmetic and the audit cannot diverge.
6. **Mark S086 as a fixture.** Add one prose line stating that S086 is a fixture or sample (4 of 33 r22 edit calls). It is not a semantics source, not a completeness claim, and not native-API evidence. Existing preregister `limits` already allow this. It adds a constraint and claims no new authority.

## Gap

I could not confirm whether the landed checkers already implement corrections 1–5. They are outside this seat's read binding, and the seat is NO-EXEC. The main agent or integrator should check:

- `tools/check-seat-bindings.py` for start-based authorization, for line-adjacency linkage, and for `:raw` stripping;
- `tools/check-path-reconciliation.py` for the same selector rule.

No installs and no commands were run. Tooling record: none.

Reviewed-SHA256: 8f3f33eaa6e9cd1c3af369955420a13e6d5b339cc5970bec04560de2c08767e8
Predicate: r23-crit23source
Scope: executed=none
