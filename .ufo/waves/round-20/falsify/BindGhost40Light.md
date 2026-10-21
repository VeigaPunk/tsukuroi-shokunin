# BindGhost40Light — full-width lightweight ghost tag

## Findings by severity

### Low — independent judge's direct selector path lacks the ghost-alias regression guard

This is a concrete coverage gap, **not a demonstrated acceptance bypass in the current candidate**.

The independent judge constructs `refs/tags/<ghost_full> -> tip` and records `ghost_full_hex_lightweight_tag`, but sends that selector to a consumer tool, not to its own `--tools-revision` binder: `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:527-540`; `exact_refusal()` calls `refused()` at `:473-477`; `refused()` calls `run_tool()` at `:383-390`; `run_tool()` supplies `--revision` to the selected tool at `:359-366`. The judge itself is excluded from discovery at `:245-252`, and object-selector probes run only for the original `TOOLS` members at `:664-669`.

The judge's own binding happens earlier, on the caller's real `tools_rev`, before sandbox ghost references exist (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:635-650`). Its direct-binding selftest checks a missing `"0" * 40` object but creates no same-named tag before that check (`:1043-1056`); `bind_error()` does call the independent `bind()` (`:886-891`). Thus the consumer ghost fixture does not establish direct-path alias rejection.

**[INFERENCE] Regression discriminator:** replacing only the judge's object-only resolution in `bind()` with its existing raw `rev_parse(repo, rev)` would not be challenged by this full-width consumer fixture or the unaliased `bind-unknown` case. The direct-path negative control would need an absent full-width object name `G`, `refs/tags/G ->` landed/pushed tip, and a direct independent `bind_error(repo, G)` expectation of `E-REVISION-INVALID`. No mutation or control was executed.

No higher-severity defect was established for this assigned lightweight ghost selector.

## Scoped source result

Axes reviewed: object identity, independence from same-spelled refs, exact refusal identity, and separation of consumer coverage from the independent judge's direct gate. The canonical C2 expectation is invalid revision / exit 2 for a ghost hexadecimal tag (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:37-41`). The inherited binder worktree identity is recorded at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:2-7`.

### Shared binder fixture

- `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:268-282` inventories object IDs, chooses a repeated-character 40-hex name absent from that inventory, creates a lightweight tag to `tip`, and directly expects `bind(repo, ghost_full)` to raise `E-REVISION-INVALID`. The tag is removed at `:283`. Lightweight tag creation references an existing commit; unlike annotated-tag creation, it introduces no new tag object that could invalidate the pre-creation inventory.
- `master` is established at `tip` before a detached unlanded commit is made (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:220-228`), and `origin/master` is restored to that same `tip` immediately before ghost cases (`:257-263`). Therefore accidental resolution to the tag target would satisfy landing/push checks rather than be hidden by an unrelated ancestry rejection.
- The fixture's `expect()` compares the exact `RevisionError.fid` (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:198-208`), so another binding error is not an accepted result.

### Independent consumer fixture

- `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:502-505,527-540` inventories objects, excludes both an equal object ID and pre-existing branch/tag refs for the chosen 40-hex name, then writes the tag ref directly to `tip`. Cleanup is in `finally`. The intervening 12-hex cases only create/delete refs (`:514-525`), so they do not make that object inventory stale for this lightweight case.
- Sandbox preparation sets both the landed branch and its origin-tracking ref to `tip` (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:233-241`).
- The required refusal is exit 2 with `E-REVISION-INVALID` (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:59,83,383-390`), strengthened to exactly one finding and exactly `[expected_id]` binding IDs by `:473-477`. This case participates in each original tool's `all(case["ok"])` result (`:664-669`); it is not an informational-only probe.

### Current direct resolution rejects the alias by construction

**[INFERENCE, source-only]** Under Git's object-disambiguation semantics, the absent full-width object produces no object-ID match even though the tag ref names a landed commit. The shared binder enumerates object matches and returns `None` unless exactly one exists (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:119-124`); `bind()` turns that into `E-REVISION-INVALID` before branch/ancestry checks (`:172-185`). There is no raw-selector ref-resolution fallback on this failure path.

The independent judge now has the same object-only boundary in its own implementation: `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:139-148,192-199`. Its CLI calls `measure()` and converts a binding `Cannot` into exit 2 / `CANNOT_EVALUATE` (`:1108-1113`, payload at `:733-743`). **No current direct-path alias acceptance gap was found in this source path.** The low-severity gap above is that the retained full-width fixture does not exercise it.

## Residual risk and verification gaps

- Static review only. Git's actual output for the constructed absent OID, either fixture's execution result, and the final nine-tool metric were not observed. The inspected R20 measurement directory contained `run.py` and `smoke.py`, not retained output for this fixture. Fixture declarations are not runtime evidence or saturation proof.
- LSP status/references/definitions/diagnostics were unavailable within the explicit `read`/`grep`/`glob`/named-report-write allowlist. Literal search located relevant code; the cited function bodies and callsites support the source trace, not an LSP semantic proof.
- Review was limited to the assigned full 40-hex lightweight ghost-tag case in the inherited binder candidate and exact R20 artifacts. No runtime was invoked, no code/Git/host state was changed, and no tool was installed or updated. No judgment, admission, host safety, or boot-image clearance is asserted; boot images remain UNKNOWN.

Scope: executed=none.
