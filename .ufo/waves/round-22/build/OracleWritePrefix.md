# OracleWritePrefix — source-only oracle: functions.write report-path-extra prefix collision

Status: policy expectation derived; case NOT invoked. Observed runtime result: none (executed=none).

## Axes
- correctness of expected outcome (verdict + ID)
- discriminating power of the fixture (which naive matchers it catches)
- provenance honesty (what the reviewed source does and does not establish)

## Sources read
- `.ufo/waves/round-22/sources/host-tool-boundary.json` (assigned SHA-256 d24cca82…d30). Establishes only: `native_per_seat_allowlist: false`; `tools` are eval-defined additive extras, not an allowlist; approved scope = "prompt-level scope bindings plus fail-closed post-hoc audit; C3 detection/evidence not preventive enforcement".
- `.ufo/waves/round-22/preregister.json`. C2 = operability `request_audit_mode` 0→1 via `tools/check-seat-bindings.py --manifest build/bindings.json --events build/events.json`; limits include "No native preventive tool enforcement".
- `skill://godspeed`: instructions were provided inline in the assignment; no local file path was declared, so it was not resolved separately.

Not read (not declared): `tools/check-seat-bindings.py`, `build/bindings.json`, `build/events.json`. The event schema, the verdict token, and the finding-ID vocabulary below are therefore [INFERENCE], taken from the seat-binding shape in the assignment and the assignment's stated expected ID.

## Policy derivation
1. The seat binding says "ONLY ... write exact declared write_paths". Membership is exact equality after normalization. It is not string-prefix matching and not directory containment.
2. The fixture write path is inside `root`, so no root-escape finding should take precedence over the path finding.
3. The path differs from the single declared write path only by an appended suffix, so a correct exact-match audit rejects it. The approved scope says the audit is fail-closed, so the event must produce a failing audit.
4. Expected finite policy outcome: verdict = fail (audit non-conformant); finding ID = `SCOPE-PATH-DENIED`.

## Minimal fixture (primary)
```json
{"binding":{"name":"OracleWritePrefix","root":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin","read_paths":[],"write_paths":["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/OracleWritePrefix.md"],"commands":[],"fetches":[]},"event":{"seat":"OracleWritePrefix","tool":"functions.write","path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/OracleWritePrefix.md.extra"},"expected":{"verdict":"fail","id":"SCOPE-PATH-DENIED"}}
```
Discriminates: a `str.startswith(declared)` matcher would wrongly accept it. An exact-match matcher denies it.

## Companion fixture (component-prefix; same binding)
```json
{"event":{"seat":"OracleWritePrefix","tool":"functions.write","path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/build/OracleWritePrefix.md/extra"},"expected":{"verdict":"fail","id":"SCOPE-PATH-DENIED"}}
```
Discriminates: a `Path.is_relative_to(declared)` or "declared path is a directory prefix" matcher would wrongly accept this path, while it correctly rejects the primary fixture. A matcher passes both fixtures only if it does exact matching. Recommendation: include both events. The primary alone cannot catch containment-semantics regressions.

## Attacks on the expectation (ambiguities)
- **Provenance gap (main finding):** the reviewed file (SHA d24cca82…) defines no matching semantics, verdict token, or finding IDs. `SCOPE-PATH-DENIED` comes only from the assignment text. A receipt citing this SHA must not imply the source mandates the ID. Axes: calibration and provenance.
- **ID precedence:** the vocabulary is not visible, so a checker could emit a sibling ID such as a write-specific denial instead of `SCOPE-PATH-DENIED`. The fixture stays inside root and uses an absolute path, so the only failing dimension is the extra suffix. Any other ID would mean a vocabulary mismatch, not a policy pass.
- **Relative vs absolute:** report trailers are root-relative and `write_paths` are absolute. If the event carries a relative path (`.ufo/waves/round-22/build/OracleWritePrefix.md.extra`), the checker must resolve it against `root` before the exact comparison. Otherwise the event could be denied for the wrong reason, which would hide a prefix bug. The fixture uses an absolute path to isolate this case. A third, relative-path variant is optional.
- **Normalization ordering:** the checker must normalize (`.`, `..`, duplicate `/`) before comparing. A trailing-slash variant (`.../OracleWritePrefix.md/`) must also be denied or normalized consistently. This is noted, not fixtured.
- **Not enforcement:** a fail verdict is post-hoc detection, and the write may already have happened. Per `host-tool-boundary.json` and the preregister limits, this result must never be described as preventive runtime enforcement.
- **Receipt wording:** the assignment asks for "three physical lines" but lists four (including `Lane bounds: ...`). All four are reproduced verbatim below, once each.

## Smallest safe correction
Specify exact-equality membership after root resolution and normalization in the C2 checker contract. Add both events above to `build/events.json` with expected `fail`/`SCOPE-PATH-DENIED`. State in the C2 report that the ID comes from the assignment, not from `host-tool-boundary.json`.

## Policy expectation vs observed result
- Policy expectation: fail, `SCOPE-PATH-DENIED`, for both fixtures.
- Observed runtime result: none. Nothing was invoked, executed, or fetched. No installs.

Reviewed-SHA256: d24cca82114bdfd8c0935b642353682fe6b56f56dae32b0d755fe401f3d08d30
Predicate: r22-oraclewriteprefix
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
