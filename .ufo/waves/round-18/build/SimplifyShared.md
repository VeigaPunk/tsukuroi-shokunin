# Round 18 — SimplifyShared (read-only)

Model: deepseek-v4.1-flash. No `lsp` device is mounted (209 `xd://` devices), so candidates rest on literal grep call-site census [obs], not semantic references.

## Shared module
`_revision.py:40` `EXIT`, `:49` `IDS`: definition-only → delete. `branch_tip:121` has no consumer outside `:212-213` selftest; keep as worktree-tip adapter. `_exists` one call but encodes rc≥2→E-GIT; keep. Landed module SHA-256 = 51dd9ee (`8425a3c3…`).

## Adapter (no new layer)
`import _revision`; each call site `try: b=_revision.bind(repo,rev,branch)` / `except _revision.RevisionError as e: raise Cannot(e.fid,e.site,e.detail)`; payload `b.sha/.branch_tip/.origin_tip`; worktree tip `_revision.branch_tip`; worktree branch check `_revision.validate_branch`. Module-qualified call keeps boot-chain's mutation stub. No wrapper.

## Delete candidates [obs]
- boot-chain: `resolve:588`, `ref_sha:596`, `is_ancestor:601`, `bind_revision:611`, `revision_finding:628`, `branch_finding:632`, `REV:88`, `BRANCH:91`; `_git_commit:1121` re-source HEAD via `git rev-parse`.
- freshness: `resolve_in:358`, `branch_tip_in:366`, `is_ancestor:374`, `branch_finding:378`, `bind:385`, `REV:59`, `BRANCH:60`.
- locator: `BindCannot:66`, `bind_revision:482`, `revision_finding:526`, `REV:35`, `BRANCH:36`.
- recheck: `ref_sha:412`, `is_ancestor:417`, `bind:427`, `REV:38`, `BRANCH:39`.
- root-dac: `VALID_REV:32`, `resolve:258`, `ref_tip:263`, `safe_tip:266`, `is_ancestor:272`, `binding:277`.
- seat: `resolve:171`, `resolve_ref:179`, `ancestor:184`, `branch_issue:194`, `binding:202`, `revision_finding:295`, `REV:36`, `BRANCH:40`.
- section: `resolve:430`, `ref_sha:437`, `is_ancestor:443`, `bind_revision:453`, `resolve_bound:475`, `revision_finding:508`, `branch_finding:512`, `REV:61`, `BRANCH:64`.
- source: `resolve:385`, `ancestor:392`, `ref_exists:396`, `bind:400`, `REV:27`; keep `rev_parse` (sandbox `:484`).
- measure: `resolve:448`, `ref_commit:457`, `branch_ok:464`, `bind:473`, `branch_tip:495`, `REV:45`, `BRANCH:46`.
Retain `git` for `show`/`cat-file`/`show-ref`, `read_git`, emit, sandboxes.

## Contract deltas
- Branch-ref absent: NOT-LANDED→BRANCH-MISSING except seat; fixtures root-dac:435, source:517, measure:630 need that id.
- root-dac:430 unlanded expects two ids; shared emits exactly one (defect 2).
- Branch-first precedence (freshness, recheck, seat, source, measure, root-dac); locator/recheck bad branch E-CLI→E-BRANCH-INVALID.
- Locator `getattr(exc,"revision"/"branch_tip")` (:785-786) must re-source `args.revision` + `_revision.branch_tip`; section baseline site→"baseline".
- Judge needs shared import and zero `{7,64}` copies; nine local copies exist.

Tradeoff: shared `site` becomes ref names; `RevisionError` drops locator/root-dac metadata.

Scope: executed=none (read-only: git log/rev-parse/show, grep, sed, wc, sha256sum, python3 JSON read; no gate/tool run, no pacman/sudo/host probe, no external writes)
