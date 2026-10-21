# C1Prefix — baseline-prefix enforcement review (round 20 attempt 1)

Axes: C1 adjacency `ownership_corrections` 0→1; specifically the baseline-prefix gate in
`_ownership_correction` (`A/tools/check-adjacency-anchors.py:135-175`) evaluated against base
`0cbc34dd6b20896085a8fb07943e3ea4027d8472` and the lane PROVINCE.md diff. C2/C3, other
candidates, host state and boot readiness are out of scope. Abbreviations: `A/` =
`/tmp/tsukuroi-r20-adjacency-20261021/`, `L/` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/`.

No `lsp` device exists in this seat's tool inventory (read/grep/glob/report-write only; mounted
`xd://` devices are `ast_edit` and `debug`), so no LSP status/references/definition/diagnostics
were available; every conclusion below is from directly read source and byte-exact greps, never
from search absence presented as semantic proof.

## Core result for the preregistered invocation

The prefix gate, given a fixed baseline blob and fixed constants, enforces exact equality
`X == B ‖ S`, where `X` is PROVINCE.md at `--revision`, `B` is PROVINCE.md at `0cbc34`
(`A/tools/check-adjacency-anchors.py:65,156-159`) and `S = ("\n" + "\n".join(OWNERSHIP_SECTION_LINES)
+ "\n").encode("utf-8")` (`:173-175`). `startswith` (`:171-172`) plus whole-remainder equality
(`:174-175`) admits no extra, missing, or displaced byte; every nonconforming input fails at
`:164-168` (no heading), `:169-170` (duplicate heading), `:171-172` (broken prefix), or
`:173-175` (broken suffix). **No bypass and no false reject exists for the preregistered
command (`L/.ufo/waves/round-20/preregister.json:10`) at the byte level.** The lane diff
conforms: byte-exact greps confirm the ASCII apostrophes (`R20-OUT009: OUT-009 is Revenger's
sibling declaration`, `proposition's unqualified`), the curly quotes (`“Revenger owns”`,
`“packages”`, `“Electron/JavaScript packages”`), the em-dash heading `## R20 ownership
clarification — OUT-009` (`L/PROVINCE.md:148`), the exact correction paragraph (`:150`,
matching `A/tools/check-adjacency-anchors.py:44-50`) and explanation paragraph incl. the
`--revision <REV> --ownership-corrections` recheck tail (`:152`, matching `:51-59`), with
single blank separators at `L/PROVINCE.md:147,149,151` — exactly the `S` layout, and consistent
with the three-way worktree agreement recorded by the C1AppendOnly seat (`A/PROVINCE.md:1-146`
== `L/PROVINCE.md:1-146`).

## Findings by severity

### P2 — Bypass (bounded to the documented `--registry-from` override): `ownership_corrections=1; exit=0` is attainable for a revision whose own registry, census and snapshot are never read, and the emitted PASS is indistinguishable from the preregistered PASS

The C1 scope requires the correction "at retained pinned scope"
(`L/.ufo/waves/round-20/preregister.json:11`). Under `--ownership-corrections`, the retention
half is enforced entirely at `registry_revision`, never at the certified `revision`:

- registry OUT-009 record must equal `OWNERSHIP_PIN` — checked against `doc`, loaded at
  `registry_binding.sha` (`A/tools/check-adjacency-anchors.py:140-147`, loaded at `:829-839`);
- census OUT-009 must equal `OWNERSHIP_CENSUS_PIN` — `census_doc` from `registry_revision`
  (`:148-154`, read at `:467-479`);
- snapshot digest re-check — `reader.read(registry_revision, OWNERSHIP_PIN["snapshot"])`
  (`:177-181`);
- only the province bytes come from the certified revision (`:481`, passed as `province_text`
  into the helper at `:761-766`).

So `python3 tools/check-adjacency-anchors.py --revision <REV> --registry-from <R2>
--ownership-corrections` accepts a `REV` whose **own** `corpus/knowledge/adjacency-anchors-r19.json`
rewrites the OUT-009 proposition into, e.g., a tsukuroi ownership grant: `REV`'s registry,
census and snapshot objects are never opened anywhere in `main`/`evaluate` (the only
registry/census/snapshot reads key on `registry_binding.sha`, `:829-839,467-479,571-590`),
while `REV`'s PROVINCE.md `== B ‖ S` satisfies the prefix gate. Result: count 1, exit 0 —
`emit` publishes `revision`, `branch`, `branch_tip`, `counts`, `findings` but **not**
`registry_revision` (`:769-776`), so this split-brain PASS JSON is byte-indistinguishable from
the preregistered PASS a consumer is told means "explicit sibling-declaration wording for
OUT-009 at retained pinned scope" at `REV`. Net semantic content of the split invocation is
only "REV's PROVINCE.md equals a fixed two-blob concatenation"; every ownership fact is
certified at the other revision.

**Expected finite behavior:** either refuse the combination (`--ownership-corrections` requires
`registry_revision == revision`), or emit `registry_revision` in the payload so retained-scope
certification is attributable. This sharpens, and does not duplicate, C1SnapshotBinding, which
recorded the override as an intentional boundary and deferred to "retained invocation
evidence" — this finding is that the tool's only machine-readable output provides no such
evidence, and that the acceptance semantics (count 1) are unaffected by the split.

**Limitations:** not the preregistered C1 invocation; requires the operator to pass a
documented flag; no runtime execution was performed — the outcome is source-derived
([INFERENCE] from the cited branches). `bind()`'s landed/pushed requirement
(`A/tools/_revision.py:12-19` error contracts; `preregister.json` expected map) constrains
which `REV`/`R2` pairs bind, but does not couple them to each other.

### P3 — "Baseline prefix" is byte identity without lineage binding

`reader.read(OWNERSHIP_BASELINE, "PROVINCE.md")` (`:156`) pins the baseline blob by constant
OID, but no check requires `revision` to descend from `0cbc34` (no merge-base/ancestor
anywhere in the helper, `:135-196`). "Preserves the exact R20 baseline prefix" (`:172`) is
therefore provable only as byte-identity of two independent blobs: a cherry-picked or rebased
`REV` on a diverged lineage that carries `B ‖ S` verbatim passes identically. Bounded by
`bind()`'s landed-and-pushed-on-branch contract (default `master`), so exploitation requires a
pushable diverged lineage; the claim language should not be read as history preservation.
[INFERENCE — `bind()` internals were read only at the constants/error-ID level
(`A/tools/_revision.py:1-30`); no execution.]

### P3 — Exact-append-only acceptance is a false-reject boundary for any other honest diff shape

The predicate admits only the terminal append `B ‖ S`. An equally faithful clarification
inserted before the "Portable digests" list, or any second hunk anywhere (including one extra
trailing newline at EOF), yields `OWNERSHIP-CORRECTION-INVALID` at `:171-175` — count 0, exit 1
— even with pins, arbitration and the r19 section intact. This is intentional exactness, not a
defect against the preregistered diff (which conforms, see core result); it is recorded as the
finite behavior boundary so a future red/green FAIL on a reflowed-but-equivalent diff is not
misread as tampering. The related MISSING-vs-INVALID typing asymmetry is already claimed by
the C1MissingCorrection seat and is not re-reported here.

## Residual risk and verification gaps

- The terminal byte of `L/PROVINCE.md` (whether the file ends in exactly one `\n` after line
  152, as `S` requires) could not be observed through the read-only reader; all visible bytes
  match. If that byte is absent or doubled, the committed diff would false-reject at `:174-175`
  and the claimed green measurement could not reproduce — main agent should confirm with
  `git show <REV>:PROVINCE.md | tail -c 1` or equivalent.
- `B` was never authenticated: identity of the three agreeing worktree copies with the
  `0cbc34` blob was not measured (no git execution permitted); if the candidate clone lacks
  the object, the gate raises `E-OWNERSHIP-BASELINE` → CANNOT_EVALUATE/exit 2 (`:156-159`,
  `:841-844`), unasserted by any selftest (C1SelftestCoverage gap).
- No checker, selftest, fixture, build, lint, smoke, git, or host command was executed; no code
  or routing edits; only this report was written. No tool was installed or updated.
- Findings attack the candidate source and lane artifacts only; no claim is made about the
  measured 0→1 result, runtime routing, saturation, or resume paths. Boot images remain
  UNKNOWN; no clearance. No host or boot-safety claim is made.

**Suggested checks for the main agent:** (1) run `--selftest` and the C1 before/after via
`L/.ufo/waves/round-20/measure/run.py:70-78`; (2) red fixture for P2: rewrite OUT-009's
proposition in a candidate registry commit, run `--revision <that> --registry-from 0cbc34
--ownership-corrections` — current source predicts count=1/exit=0, which would demonstrate the
bypass; (3) authenticate `git diff 0cbc34..<REV> -- PROVINCE.md` as exactly the append,
including the EOF newline.

Scope: executed=none
