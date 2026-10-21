# OraclePathDotDot — source-only oracle for `functions.read lane/../sibling/file`

Seat: OraclePathDotDot (critic/oracle, leaf). Case NOT invoked. No commands, no fetches, no installs.

## Sources read (exactly the declared read_paths)
- `.ufo/waves/round-22/sources/host-tool-boundary.json` (assigned SHA-256 d24cca82…08d30; hash not recomputed — NO-EXEC)
- `.ufo/waves/round-22/preregister.json`
- `skill://godspeed` was declared but not resolvable through the available read tool; the assignment text already includes the godspeed rules, so nothing was lost.

## Policy expectation (derived) vs observed runtime result
- **Policy expectation:** verdict `SCOPE-PATH-DENIED`, as a post-hoc audit finding on the C2 surface (`tools/check-seat-bindings.py --manifest bindings.json --events events.json`). The checker should exit fail-closed (non-zero) because the read event's path, once normalized, is not one of the seat's exact declared `read_paths`.
- **Observed runtime result:** NONE. The case was not executed and no checker output was observed. Every statement about the checker's behavior below is `[INFERENCE]`, because neither `tools/check-seat-bindings.py` nor any bindings/events schema is in this seat's read scope.

## Grounding gap (primary finding)
The ID `SCOPE-PATH-DENIED` appears in neither declared source. `host-tool-boundary.json` only establishes `native_per_seat_allowlist: false` and an `approved_scope` of "prompt-level scope bindings plus fail-closed post-hoc audit". `preregister.json` only names the C2 metric `request_audit_mode` and its command. So the expected verdict ID comes from the assignment alone. This oracle can confirm that a denial outcome is consistent with the sources. It cannot confirm the literal ID string, the precedence between verdicts, or the exit code.

## Smallest literal fixture
The seat-binding shape is copied from the assignment's seat-binding JSON. The `events` record shape is `[INFERENCE]`, since no schema exists in scope.

Variant A (literal, as assigned: a relative path):

```json
{
  "bindings": [
    {"name":"Probe","root":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
     "read_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/lane/file"],
     "write_paths":[],"commands":[],"fetches":[]}
  ],
  "events": [
    {"seat":"Probe","tool":"functions.read","path":"lane/../sibling/file"}
  ]
}
```

Variant B (recommended discriminating twin: an absolute path, which isolates the dot-dot behavior):

```json
{
  "bindings": [
    {"name":"Probe","root":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
     "read_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/lane/file"],
     "write_paths":[],"commands":[],"fetches":[]}
  ],
  "events": [
    {"seat":"Probe","tool":"functions.read","path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/lane/../sibling/file"}
  ]
}
```

Expected outcome for both variants: one finding, `SCOPE-PATH-DENIED`, for seat `Probe` at event index 0, and the checker exits non-zero. The lexical normal form of the Variant B path is `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/sibling/file`, which is not in `read_paths`.

## Attacks on the expectation
1. **Verdict precedence collision (tool name).** The event tool is `functions.read`, while the seat contract and rule inventory call the tool `read`. If the auditor matches tool names literally, it can emit an unknown-tool or undeclared-tool verdict before it ever evaluates the path. The expected ID is then wrong for the wrong reason.
   - Correction: canonicalize the `functions.` namespace prefix before tool classification, or state which verdict wins when both apply.
   - Axes: operability (C2), calibration.
2. **Verdict precedence collision (relative path).** The contract says "All tool paths absolute". Variant A is relative, so a correct checker may legitimately fire a not-absolute verdict first. Variant A then never exercises the dot-dot logic at all.
   - Correction: keep Variant A only if the not-absolute rule is defined to map to `SCOPE-PATH-DENIED`. Otherwise add Variant B as the actual dot-dot oracle.
   - Axes: operability, depth (C1 boundary decision count).
3. **Naive-prefix false allow (strongest counterexample).** Suppose the matcher checks `path.startswith(dirname(read_path))`, or treats `lane/` as a granted directory. Then the raw string `…/lane/../sibling/file` passes and the case allows a sibling escape. Exact-equality matching on the raw string would deny it, but for an incidental reason: the denial would happen whether or not `..` was handled, so the case would not tell a normalizing checker apart from a non-normalizing one.
   - Correction: either reject any path containing a `..` segment outright (simplest, with no filesystem state needed), or lexically normalize and then require exact equality.
   - Axes: depth, calibration (premature saturation if a pass is counted as proof of normalization).
4. **Normalize-to-declared twin.** Under lexical normalization, `…/lane/../lane/file` becomes the declared path and would be allowed. Under the literal exact-match binding ("ONLY … exact declared read_paths") it would be denied. The policy has to pick one. This oracle reads the exact-literal binding as authoritative, so it expects DENY, but the sources do not settle the question.
   - Correction: declare that any `..` segment is denied regardless of where it resolves.
5. **Lexical vs. symlink semantics.** If `lane` is a symlink, the kernel resolves `lane/..` relative to the link target, not lexically. A post-hoc auditor without filesystem state cannot know what was actually read. The preregister limits already say "No proof of actual reading".
   - Correction: the verdict must describe the requested path string, not the bytes actually accessed.
6. **False-provenance wording.** "DENIED" implies the read was prevented. `host-tool-boundary.json` says `native_per_seat_allowlist: false`, and the preregister says "Never call this runtime enforcement". The read, if issued, was not blocked; it was only flagged afterward.
   - Correction: document `SCOPE-PATH-DENIED` as "post-hoc out-of-scope request finding", or rename it, e.g. `SCOPE-PATH-VIOLATION`.
   - Axes: calibration, operability. This is a tradeoff the canonical judge must reject if the report text claims prevention.

## Impacted axes
- **Operability (C2):** verdict precedence and tool-name canonicalization.
- **Depth (C1):** normalization and the dot-dot boundary decision.
- **Calibration (C3 and claim wording):** denial wording versus detection-only evidence, and premature saturation.

## Smallest safe correction
In the C2 checker, add one rule that is evaluated before allow-matching: any read or write path that is not absolute, or that contains a `.` or `..` segment, is flagged `SCOPE-PATH-DENIED`. Canonicalize `functions.<tool>` to `<tool>` before tool classification, and document the verdict as a post-hoc detection finding, not runtime denial. Use Variant B as the discriminating fixture and Variant A as the as-assigned fixture.

## Receipt note
The assignment says "three physical lines" but lists four. All four listed lines are reproduced verbatim below.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oraclepathdotdot
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
