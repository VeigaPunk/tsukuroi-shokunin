# C2 valid-prefix ref-shadow fixture

**Axis:** C2 operability (`object_selector_tools`); C1 adjacency and C3 calibration are out of scope. This is a baseline-only fixture design, not a candidate verdict.

## Source and oracle

- `.ufo/waves/round-20/preregister.json:13-19,37-47` sets C2 to original-nine object-selector continuity and explicitly requires both `valid_prefix_shadow_branch` and `valid_prefix_shadow_tag` to bind the object, not the ref target.
- `tools/_revision.py:11-21,97-108,134-154` allows 7–64 hexadecimal selectors, sends the raw selector to `git rev-parse ... <selector>^{commit}`, then checks landing/push. There is no object-ID-only disambiguation before that resolution.
- The judge is deliberately independent (`tools/_revision.py:8-9`). Its own `rev_parse()` and `bind()` also pass the raw selector through `^{commit}` (`tools/check-revision-binding.py:130-176`). The current consumer matrix has ordinary `tip`/`short-tip` cases only (`:380-388`); the direct judge selftest has `bind-unknown` but no valid-prefix collision (`:790-799`). `make_fixture()` already supplies a base commit and landed tip (`:626-642`); `measure()` passes the tip's parent to `probe_tool()` (`:450-465`), with both local and origin refs initially at the tip (`:201-210`).
- Public Git `gitrevisions` documentation, “SPECIFYING REVISIONS” (`<sha1>` and `<refname>`), defines a unique leading hexadecimal substring as an object name and separately defines symbolic refnames: <https://git-scm.com/docs/gitrevisions/2.56.0. The preregistered expectation requires the object-name interpretation when those spellings collide.

## Exact synthetic fixture and expected output

Create two otherwise identical isolated repositories, one per alias type. Each has a two-commit linear history `A → C`; set `refs/heads/master` and `refs/remotes/origin/master` to `C`. Let `A` and `C` be distinct full commit IDs. After all fixture objects exist, choose `n` from 7 through the full ID length and set `P = A[:n]` where `P` matches exactly one object ID in the repository (including non-commit objects). This makes the input a valid, unique commit-object prefix, not an ambiguous abbreviation.

| Variant | Additional ref | Input | Required binder result |
|---|---|---|---|
| Branch shadow | `refs/heads/P → C` | `P` | `Binding.sha == A` (canonical full OID); branch tip and origin tip remain `C` |
| Tag shadow | `refs/tags/P → C` (lightweight tag) | `P` | `Binding.sha == A` (canonical full OID); branch tip and origin tip remain `C` |

Keep variants separate so a simultaneous branch/tag name does not add a second ref-precedence interaction. `A` is landed and pushed because it is an ancestor of both `master` and `origin/master`; the wrong target `C` is also landed and pushed. Thus a status-only assertion is insufficient: compare the returned/JSON revision with `A`, and require it not to equal `C`.

For the independent judge's own `bind()` selftest, use `make_fixture(..., return_base=True)` to obtain `(C, A)`, set `refs/remotes/origin/master → C`, install each alias in its own fixture, and assert `bind(repo, P) == A`. For the original-nine consumer probes, add separate branch/tag cases to `probe_tool()` using `A=parent`, `C=tip`, install the alias in separate sandbox variants, and call the existing acceptance path with expected SHA `A`. Required per-tool observation is accepted (`exit != 2` under `accepted()`'s contract), JSON `revision == A` (not `C`), and `ok=true`; both cases must contribute to C2's original-nine grade. This also exercises the judge's independent consumer oracle rather than importing the shared binder.

## Smallest wrong implementation killed

The smallest faulty resolver is the baseline-shaped implementation that accepts the hex regex, treats `git rev-parse "$P^{commit}"` as proof of object identity, and never disambiguates the input against object IDs first. In this collision fixture it can bind the same-named branch/tag target `C`; the test rejects that result because the required object is `A`. **[INFERENCE]** This failure mode is derived from the raw-selector source path and the colliding fixture; it was not run under this NO-EXEC assignment. The fixture's expected value comes from the frozen preregistration, not from observing Git or a candidate.

## Residual risk and verification gaps

Read-only source/oracle review only. Baseline identity is taken from the preregistration (`0cbc34dd6b20896085a8fb07943e3ea4027d8472`) and was not independently checked. No fixture, command, candidate, or test was executed. LSP status/references/definition/diagnostics were not queried because the seat permits only read/grep/glob plus report writing; no LSP result is claimed. This finite fixture makes no host, boot, or runtime-safety claim.

Scope: executed=none
