# FxC3Gameability — C3 harness

Verdict: **UNPROVEN.** The count does not establish "bound 5/5". The tools look bound when read, but the harness cannot tell them apart from S1–S3.

Axes: operability, provenance, denominator.

1. [obs] All three stubs still score BOUND. `probe_tool` (`tools/check-revision-binding.py:229-248`) runs only three probes: HEAD, an unlanded commit, and the full tip.
   - S1 (tip-equality only): no landed non-tip ancestor is probed.
   - S3 (literal HEAD only): `@`, `@-` and `master` are never probed.
   - S2 (no origin check): `prepare` sets origin to the tip (`:142-145`).
   - The selftest has only the modes bound/unbound/wrong-id/absent (`:318-330`). Its NOT-PUSHED case (`:451-455`) tests the harness's own `bind()`, not the tools. So the docstring at `:19-20` is false.
2. [obs] The tip probe passes the full sha (`:238`), so a stub that echoes its input passes. Abbreviated input is never checked. The worktree equals the tip, so reading the worktree also passes.
3. [obs, effect inf] `--revision ""` falls into worktree mode in three tools: locator `:778`, root-dac `:498`, source-scope `:639`. Neither `""` nor an omitted flag is probed.
4. [obs] The denominator is fixed at 5 (`:36-43`). Nine tools define `--revision`. Uncounted: boot-chain `:611`, freshness-r17 `:435`, recheck-commands `:507`, seat-scope `:268`. C1 and C2 rely on the first two.

Correction:
- Add S1–S3 stubs to the selftest; they must score UNBOUND.
- Add probes:
  - a landed tip^ is accepted;
  - origin set to tip^ makes the tip fail with NOT-PUSHED;
  - `@`, `master` and `""` are rejected as INVALID;
  - an abbreviated tip returns the full sha.
- Denominator = tools that define `--revision`.

[unk]: nothing run.

Scope: executed=none
