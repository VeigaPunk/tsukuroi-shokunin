# C2 oracle: ghost hexadecimal branch

**Axis:** C2 operability only. C1 adjacency and C3 calibration are out of scope.

## Synthetic fixture and expected result

In the isolated binding fixture, keep `refs/heads/master` at the ordinary landed `tip`. Choose a lowercase 40-hex string `ghost` by scanning candidates until `git cat-file -e "${ghost}^{object}"` fails **before** creating a ref; this guarantees no object matches that full selector (or its prefix). Then create `refs/heads/${ghost}` pointing at `tip`, without creating an object named `ghost`. Call the resolver with `revision=ghost`, `branch=master`.

Expected: `E-REVISION-INVALID` (the tool-level refusal is exit 2), not a successful binding to `tip`. In the judge's existing `fx5` direct-binding selftest, the assertion is `bind_error(fx5, ghost) == ID_INVALID`. For each original-nine consumer in `probe_tool`, add a `ghost_hex_branch` refusal case using the same `ghost` ref in its sandbox; expected record is `exit=2`, `finding=E-REVISION-INVALID`, `binding_ids=[E-REVISION-INVALID]`, `finding_count=1`, `ok=true`. Keep this among the bound cases so a consumer accepting the ghost cannot count as bound. This matches preregistered C2 expectation `ghost_hex_branch: E-REVISION-INVALID; exit=2`.

The independent judge selftest fixture and each consumer sandbox must install the same-named branch only after selecting a candidate with no matching object. Pointing it at the landed `tip` makes ref fallback observable as an erroneous acceptance; leave the default binding branch as `master`.

## Source justification and defect killed

- `tools/_revision.py:40-41,97-108,134-141`: `REV` accepts 7–64 hex; `_commit` passes `ref + ^{commit}` to `git rev-parse`; `bind` accepts the returned commit before checking it against `master`. There is no check that the hex selector resolved as an object ID rather than a same-named ref. The existing `unknown` selftest at `:200-205` uses `0` repeated 40 times without creating a matching hex branch, so it does not exercise ref fallback.
- The judge deliberately has an independent resolver: `tools/check-revision-binding.py:130-136,162-176` also passes the selector to `rev-parse` and then checks ancestry. Its `probe_tool` cases at `:380-388` lack this ref-collision case; its `fx5` selftest at `:790-799` checks `bind-unknown` without a same-named ref.
- Smallest wrong implementation killed: treating “matches the hex regex and `rev-parse <selector>^{commit}` returned a commit” as sufficient proof that the selector names an object. With the ghost ref aimed at `tip`, that shortcut can bind the branch target instead of rejecting the nonexistent object. This manifestation is **[INFERENCE]** from the source path; it was not executed here.

## Scope and limitations

Read the lane source and preregistered expectation only; no candidate review, edits, or execution. The preregistered baseline is `0cbc34dd6b20896085a8fb07943e3ea4027d8472`; this read-only seat did not independently verify the checkout commit identity. Fixture proposal covers only a ghost hexadecimal branch, not the separate prefix-shadow or tag cases.

Scope: executed=none