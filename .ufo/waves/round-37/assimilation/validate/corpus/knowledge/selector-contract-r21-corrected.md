source: S081 https://git-scm.com/docs/gitrevisions/2.56.0 SPECIFYING REVISIONS <rev>^{<type>}; S082 https://git-scm.com/docs/git-rev-parse/2.56.0 OPTIONS, Options for Output, --verify; lane policy QUALITY27/36 and tools/_revision.py
verified-at: 2026-10-21 (sources opened; immutable execution receipts recorded separately)
recheck: on-release

# R21-TYPE-PROVENANCE — corrected decision contract

This entry supersedes `selector-contract-r21.md` and `.json` only for their provenance representation, type quotations and gate/table binding. The five intended outcomes do not change. The earlier committed files remain historical; a structural gate pass is not a universal source-agreement theorem. Falsifier evidence: `.ufo/waves/round-21/falsify/FxC1{Blob,Tree,Policy,CommitTag,Source}.md` (the brace form names five real report files, not a literal filename).

## Located Git propositions versus lane policy

S081, SPECIFYING REVISIONS `<rev>^{<type>}`, version2.56.0, opened2026-10-21:

- “dereference the object at <rev> recursively until an object of type <type> is found”
- “or the object cannot be dereferenced anymore (in which case, barf).”

S082, OPTIONS › Options for Output › `--verify`, same version/access date:

- “a commit-ish (i.e. a commit, or an annotated tag that points at a commit)”

Each quote is an exact contiguous located excerpt of fewer than26 words. Typed peeling recursively follows tag targets until the requested type is obtained or cannot be obtained. A tree or blob cannot become a commit by stripping tag indirection. Empty-brace peeling is also recursive, but stops at any non-tag object; it is not a one-level peel and is not interchangeable with commit-type peeling.

The `source` field in each JSON row supports only its Git type proposition. Its separate `policy` field cites QUALITY27/36 and the shared binder for hexadecimal object-only selection, first-failure diagnostics, lane-branch ancestry and conditional origin-ref ancestry. Those object-prefix/ancestry/push restrictions come from the lane's evidence contract, not these manuals.

Here `accept-if-landed-and-pushed` is the existing short policy label: “pushed” means ancestor of the locally recorded `refs/remotes/origin/<branch>` only when that ref exists. An absent origin tracking ref does not itself cause refusal. Neither this condition nor the resulting error IDs is specified by the Git quotations. Local tracking state does not certify the live remote service.

## Five fixed decisions

| Class / row ID | Git type proposition | Lane outcome | Refusal finding | Git source and separate policy |
|---|---|---|---|---|
| commit | Existing commit is commit-ish; origin check applies only when the tracking ref exists | accept-if-landed-and-pushed | none on acceptance; other binding failures remain possible | S082; QUALITY27/36 |
| tree | Any tree is not commit-ish; non-empty tree is the measured control | refuse | E-REVISION-INVALID | S081; QUALITY27/36 |
| blob | A blob is not commit-ish | refuse | E-REVISION-INVALID | S081; QUALITY27/36 |
| tag-to-commit | Annotated tags, including nested annotated tags, peel recursively to the terminal commit | accept-if-landed-and-pushed | none on acceptance; other binding failures remain possible | S081; QUALITY27/36 |
| tag-to-noncommit | Annotated tag ending at tree or blob cannot peel to a commit | refuse | E-REVISION-INVALID | S081; QUALITY27/36 |

The table is a type/outcome decision contract, not an exhaustive refusal table. Branch syntax/missing branch, missing or ambiguous object IDs, not-landed, not-pushed and Git-operation failures retain the shared binder's existing precedence and IDs. Refusal payloads may echo a requested selector or the consumer's documented unbound sentinel; a diagnostic echo is not an accepted binding. The new matrix grades the expected accepted commit independently of the branch tip.

## Bounded measurements and remaining unknowns

C1 validates these five source-grounded decisions and their fixed table cells/policy/source mappings. It does not execute Git type behavior or prove arbitrary free-text semantics. C2 independently exercises the real original-nine CLIs with one non-empty tree, single-level tags to blob/tree, and ordinary/nested tags to a landed commit. Single-level noncommit controls are not universal nested-noncommit, tag-to-unlanded/unpushed, replace-ref, configuration-isolation or arbitrary-shell coverage. Those limits remain explicit; no new class is silently added to the frozen metric. The old round20 object-selector matrix remains unchanged.

The scope is lane-owned evidence tooling only. No host health, next-boot readiness, package transaction, service restart, sibling authority or native-judge admission follows any result. Primary review receipts bind declared source bytes/predicates, not proof of actual reading or command nonexecution.

## QUALITY check

QUALITY19/21: the located recursion/failure/commit-ish quotations support the Git propositions; explicit policy fields prevent attribution of lane diagnostics or ancestry rules to the manuals. QUALITY14: this source check is performed; runtime gate/selftest results are separate immutable receipts. QUALITY27/36/40/41: fixed class outcomes remain five, origin absence is allowed, new control availability is not nine-tool behavioral repair, and expected targets come from independent fixture construction. QUALITY42–44: historical reports/digests remain intact; known provider deaths remain missing/red and are never replaced. Applicable source and schema mutations must fail before a fix is credited. Independent non-author closure remains pending.
