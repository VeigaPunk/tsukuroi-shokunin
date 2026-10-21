# FxC2ParallelFetch — nested fetch-denial preservation

## Result and axes

**Bounded result: the assigned invariant holds by source inspection for the well-formed nested/mixed fixture below.** No concrete passing counterexample was found within that bound. This is a source-derived conclusion, not an observed runtime result.

Axes: retain the fetch finding through nested wrappers; do not let allowed siblings erase it; distinguish post-hoc classification from preventive enforcement; preserve source bytes and report unexecuted checks honestly.

Reviewed target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`, read at lines 1–241. The digest in the receipt is the assignment's supplied pin, not an independently computed checksum.

## Static attack fixture

These JSON objects are inert report data, not issued requests. In particular, the HTTPS URL was not fetched. The detector under discussion is the target's `evaluate` function with the following binding and recorded-event objects.

Binding:

```json
{
  "schema": "tsukuroi-seat-bindings-v1",
  "seats": [{
    "name": "FxC2ParallelFetch",
    "root": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin",
    "read_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-seat-bindings.py"],
    "write_paths": ["/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/falsify/FxC2ParallelFetch.md"],
    "commands": [],
    "fetches": []
  }]
}
```

Recorded events:

```json
{
  "schema": "tsukuroi-seat-events-v1",
  "seats": [{
    "name": "FxC2ParallelFetch",
    "agent": "fixture-FxC2ParallelFetch",
    "complete": true,
    "events": [{
      "tool": "multi_tool_use.parallel",
      "args": {
        "tool_uses": [
          {
            "recipient_name": "functions.read",
            "parameters": {
              "i": "Reading allowed fixture source",
              "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-seat-bindings.py:1-5:raw"
            }
          },
          {
            "recipient_name": "multi_tool_use.parallel",
            "parameters": {
              "tool_uses": [
                {
                  "recipient_name": "functions.read",
                  "parameters": {
                    "i": "Reading forbidden fixture URL",
                    "path": "HTTPS://EXAMPLE.INVALID/:1-5"
                  }
                },
                {
                  "recipient_name": "functions.read",
                  "parameters": {
                    "i": "Reading allowed fixture source",
                    "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-seat-bindings.py"
                  }
                }
              ]
            }
          },
          {
            "recipient_name": "functions.read",
            "parameters": {
              "i": "Reading allowed fixture source",
              "path": "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-seat-bindings.py"
            }
          }
        ]
      }
    }]
  }]
}
```

The allowed reads occur before the nested wrapper, after the denied leaf within that wrapper, and after that wrapper. Thus both recursive returns and later allowed siblings must preserve the denial.

## Expected fixture verdict — not runtime output

[INFERENCE] For the unchanged candidate, this fixture yields exit code **1**, `status=FAIL`, `request_audit_mode=1`, `seats_bound=1`, `requests_total=1`, `violations=1`, and `incomplete_seats=0`. Its sole finding is:

```json
{"id":"SCOPE-FETCH-DENIED","site":"FxC2ParallelFetch:0"}
```

The seat row has one recorded event, `complete=true`, and `violations=["SCOPE-FETCH-DENIED"]`. The wrapper's four leaf operations are not four top-level events; `requests_total` increments at the event loop, lines 134–138.

### Source-visible reason

1. Lines 105–123 accept this nonempty, exact-path binding and complete, uniquely identified trace.
2. Lines 61–72 accept both wrappers and recurse. Wrapper depths are 0 and 1; read leaves are at depths 1 or 2, safely within the depth guard.
3. Lines 73–74 normalize `functions.read` to `read`.
4. Lines 46–47 recognize the uppercase HTTPS prefix with the case-insensitive regular expression **before** read-selector stripping. The URL therefore contributes `SCOPE-FETCH-DENIED`; its trailing `:1-5` cannot disguise it as local.
5. The declared local reads contribute empty finding lists. The first read's selector is stripped at lines 50–53 before exact membership at lines 90–91.
6. Line 71 uses `findings.extend(...)` for every child. Extending by an allowed child's empty list cannot erase earlier findings. The inner wrapper returns one fetch finding; the outer wrapper retains it even after its final allowed read. More generally, for a finite well-formed tree that stays within the depth bound, each wrapper returns the concatenation of its children's findings.
7. Lines 138–144 retain that finding at the enclosing event site, increment the violation count, and select failure rather than pass.

This bound requires valid child dictionaries/tool arguments, recognized wrapper spellings, a valid binding, and complete metadata. Malformed children or excessive depth can instead produce `CANNOT_EVALUATE`/`SCOPE-SCHEMA` via lines 145–147; this report does not assert preservation of a specific fetch ID across exceptions, or universal wrapper recognition.

## One plausible mutant and detector sensitivity

**Paper mutant only; not applied:** at line 71, replace accumulation with last-child assignment, changing `findings.extend(classify(child.get('recipient_name'), child.get('parameters'), binding, depth + 1))` to `findings = classify(child.get('recipient_name'), child.get('parameters'), binding, depth + 1)`.

This is a small behavior-bearing defect: an allowed sibling would replace an earlier denial with an empty list. In the fixture above, the allowed inner sibling would erase the HTTPS finding, and the allowed final outer sibling would also erase any findings arriving from the inner wrapper.

| Bytes considered | Expected detector result [INFERENCE] | Actual observed detector output |
|---|---|---|
| Unchanged candidate | Exit 1 / FAIL / one fetch denial | None; not executed |
| Hypothetical last-child mutant | Exit 0 / PASS / zero violations | None; mutant not applied or executed |
| Original bytes after probe | Same expected result as unchanged candidate | None; no detector or restoration run |

The expected detector is the same fixed binding/event fixture for all three states. It would distinguish the candidate from this mutant if an authorized executor ran it. **Observed mutation verdict: INCONCLUSIVE / unexecuted, not a killed or surviving mutant.**

The built-in parallel fixtures at lines 180–183 cover a single exec child, a single fetch child, a single local child, and a malformed child. The uppercase fetch fixture at lines 169–170 is top-level. Those shown fixtures do not exercise nested fetch denial followed by allowed siblings. [INFERENCE] The last-child defect would leave their individual expectations unchanged. This is a source-visible coverage gap, not an observed selftest pass or a change to the contract.

## Actual activity, hashes, and restoration

Observed activity consisted only of authorized local/skill reads and this exact report write. No command, import, test, example, detector, URL fetch, mutation, checksum calculation, or additional runtime was invoked. No tool was installed or updated.

Before/after SHA-256 measurements are **unavailable** under the source-only NO-EXEC restriction; the receipt records only the supplied target pin. The target source was never written, so there were no mutated bytes to restore. No production file, build report, sibling file, Git/index state, or other report was modified. The report write is the sole filesystem change made by this seat.

This finding concerns finite post-hoc request classification only. `preregister.json` lines 9–13 and `sources/host-tool-boundary.json` lines 9–12 expressly exclude native per-seat preventive enforcement. No claim is made about actual request effects, real network blocking, trace completeness, symlinks, or proof of reading.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2parallelfetch
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
