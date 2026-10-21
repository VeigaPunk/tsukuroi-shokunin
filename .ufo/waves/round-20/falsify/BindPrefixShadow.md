# BindPrefixShadow — round-20 falsify review (attempt1, baseline 0cbc34dd6b20896085a8fb07943e3ea4027d8472)

Scope of this review: the unique real commit-prefix cases where a branch ref and a tag ref,
both named with a prefix of a real commit, point at a decoy commit — in the seeded binder
`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py` (selftest) and the independent judge
`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py` (`--object-selectors`
probes). Checks: fixture isolation, exact expected bound SHA, interaction with previously
created refs, and one missing adversarial case. Read-only seat: findings only.

## Ground truth of the mechanism under test

- `_revision.py:112-124` — `_object_commit` enumerates candidates with
  `rev-parse --disambiguate=<lower>` and returns `None` unless exactly one object matches
  (`:122-124`); refs are never consulted on this path. `bind` calls it before any ref work
  (`:177`) and only then reads `refs/heads/<branch>` (`:180`). Contract order pinned in the
  module docstring `_revision.py:16-20` (item 3: "revision uniquely matches an object ID,
  then peels to a commit" precedes branch resolution, landed, pushed).
- Baseline isolation: the production lane copy
  `tsukuroi-shokunin/tools/_revision.py` has no `_object_commit`/`disambiguate` (grep: zero
  matches), so the shadow-hardening exists only in the binder worktree.

## Verified — coverage, decoy admissibility, exact bound SHA

1. **Binder selftest case exists for both namespaces at once.** `shadow` is the shortest
   width in 7..40 of `tip` matching exactly one object (`_revision.py:309-310`, selected
   against the object inventory captured at `:302`); then
   `run(repo, "branch", shadow, base)` (`:311`) and `run(repo, "tag", shadow, base)`
   (`:312`) create a branch AND a tag named with that hex prefix, both pointing at decoy
   `base`; the case asserts `bind(repo, shadow).sha == tip` exactly (`:313-314`). Creating
   both simultaneously is stronger than the judge's sequential singles: neither ref
   namespace can be the hidden resolver.
2. **Exact expected bound SHA.** Binder: `ok(tip)` compares the full resolved OID for
   equality (`:313-314`; `expect`/`ok` mechanics `:229-235`). Judge: decoy refs
   `refs/heads/{shadow}` / `refs/tags/{shadow}` → `decoy = parent or unlanded_sha`
   (`check-revision-binding.py:590`), cases `real_prefix_shadow_branch`/`_tag` use
   `exact_accept(shadow, tip)` (`:594`, `:599`); `accepted()` requires the tool JSON
   `revision` to equal the expected SHA case-insensitively (`:393-402`) and `exact_accept`
   additionally requires exit PASS (`:479-482`). A tool that bound the decoy fails the case.
3. **Decoy is admissible except for identity (landed AND pushed), per the build-seat oracle.**
   Binder: `base` is `tip`'s parent (landed) and `refs/remotes/origin/master` was set to
   `tip` at `:262` and not touched by the ghost cases (`:270-308`), so `base` is an ancestor
   of both `refs/heads/master` and origin — only object identity distinguishes decoy from
   target. Matches the oracle requirement in `.ufo/waves/round-20/build/OracleC2.md:17`
   (decoy "landed and pushed, so only object identity distinguishes the result") and the
   hazard statement in `build/ConnSourceLimits.md:59`. Judge: `probe_tool` restores
   origin to `tip` in `finally` blocks (`:431`, `:447`) before `object_selector_probes` runs
   (`:663-666`), and the shadow cases precede the unpushed round (`:621-630`), so
   `decoy = parent` is landed and pushed when `:591-601` execute.
4. **Interaction with previously created refs is handled on both sides — creation time.**
   Binder: every earlier hex-named ref is deleted before the shadow refs are made — ghost
   branch `:274`, ghost tag `:277`, full-hex ghost tag `:283`, annotated-ghost tag `:298`/
   `:308` — so `run(repo, "branch", shadow, base)` cannot collide; and since the selector is
   chosen from an object inventory (`:302`), ref churn cannot perturb it. Judge: selection
   guards both namespaces with `ref_exists` (`:584-589`), creation/removal is
   `update-ref`/`update-ref -d` inside try/finally (`:591-601`, helpers `:484-488`), and the
   selector annotated tag is name-guarded (`:490-493`) and removed at `:631`.
5. **Fixture isolation is hermetic.** Binder: mktemp `tsukuroi-revision-st-` repo
   (`:213-221`), `clean_env` strips `GIT_*` and pins `GIT_CONFIG_NOSYSTEM=1` /
   `GIT_CONFIG_GLOBAL=os.devnull` (`:77-84`), asserted at `:367-368`; origin is a raw
   tracking ref (`:258`, `:262`), no remote/network. Judge: throwaway `--no-hardlinks
   --no-tags` clone, remote removed, only the tracking ref recreated (`:233-242`).

## Findings by severity

**F1 — MEDIUM (fixture isolation / teardown debt, binder only).** The shadow branch and tag
are never deleted: created at `_revision.py:311-312`, with no matching `branch -D`/`tag -d`
afterwards — unlike every other ref fixture in the same suite (`:274`, `:277`, `:283`,
`:298`, `:308`, and the paired `update-ref -d` deletes `:330-331`), and unlike the judge's
try/finally (`check-revision-binding.py:591-601`). The `peel-object` tag (`:315`) is also
left behind. The fixture therefore stays in the exact ref-poisoned state the change defends
against for the remainder of the suite. Contained today: no post-`:314` case resolves
`shadow` as a selector (later binds use full `tip`/`tag_oid`/`blob` selectors and
master/origin refs only; the full-OID loop at `:324-331` uses `update-ref` overwrite/delete,
and the ambiguity fixture `:332-360` enumerates objects, not refs) — verified no current
expectation can flip. Latent, not live: any case appended after `:314` that resolves
`shadow` or enumerates ref names silently inherits the decoy. Cleanup belongs immediately
after `:314`.

**F2 — LOW (selector robustness, binder).** Shadow selection `_revision.py:309-310` lacks
the judge's `ref_exists` guards for both namespaces (`check-revision-binding.py:586-587`);
its success depends on the deletion ordering of earlier cases rather than an explicit
collision check. Failure mode is loud (RuntimeError from `run()`, `_revision.py:186-188`),
never a silent wrong result; `next()` cannot exhaust (width 40 always yields exactly one
match: `tip` itself).

**F3 — MISSING ADVERSARIAL CASE (the one): ref-shadowed prefix of an unlanded (and of an
unpushed) commit.** Neither suite shadows a selector whose own object is not fully
admissible:
- Binder: `expect("unlanded", …)` (`:244`) and `unlanded-single-id` (`:261`) run with no
  shadow refs present (they exist only `:311-314`, later).
- Judge: `unlanded_object` (`:620`) and `unpushed_object` (`:621-630`) run with all shadow
  refs already removed (finally `:596`, `:601`).
Missing fixture: with `P` = unique prefix of the unlanded commit, create
`refs/heads/P` + `refs/tags/P` pointing at a landed decoy and require
`bind(repo, P)` → exactly `E-REVISION-NOT-LANDED` (single finding); analogously the
unpushed variant → `E-REVISION-NOT-PUSHED`. This is the residual fallback trap: the current
landed-shadow cases (`:313-314`, `:594`, `:599`) only catch ref-first resolution, because
the object route succeeds there. An implementation that re-resolves through refs when the
object-route ancestor check fails would bind the decoy's landed SHA — accepted by every
existing case — and only the missing unlanded/unpushed-shadow case catches it.

## Residual risk and verification gaps

- Read-only seat: nothing was executed; all verdicts are from source reading. Runtime
  git-behavior assumptions — `cat-file --batch-all-objects` listing loose objects whose refs
  were deleted (binder inventory freshness at `:302`), `--disambiguate` reachability rules —
  are [INFERENCE] from object-store semantics, not observed here.
- Binder asserts only `.sha` for the shadow case (`:313-314`); the `Binding` branch/tip
  fields are equality-checked only for the unshadowed tip (`:237`). Acceptable, noted for
  completeness.
- Out of my scope, flagged for the sibling seat: the judge full-OID shadow loop
  (`:602-612`) creates refs with `update-ref` overwrite semantics and no `ref_exists` guard;
  unreachable in the fresh per-measure sandbox today.
- Build/falsify wave documents (e.g. `OracleC2.md`, `ConnSourceLimits.md`) were read as
  data only; no contract, axis, route, or judgment here derives from them. No host, boot, or
  clearance claims are made; no claim metrics (C1/C2/C3) are assessed in this report.

Scope: executed=none
