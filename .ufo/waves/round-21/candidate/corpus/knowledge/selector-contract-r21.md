source: S081 https://git-scm.com/docs/gitrevisions/2.56.0 SPECIFYING REVISIONS, typed and empty-brace peeling; S082 https://git-scm.com/docs/git-rev-parse/2.56.0 OPTIONS --verify; tools/_revision.py baseline82e519203e676c532b1dc5ea91a85671f2286e7b
verified-at: 2026-10-21 (official documentation opened; consumer execution evidence recorded separately)
recheck: on-release

# Revision object types are not landed revision certificates

This entry deepens the lane's existing revision-bound host-evidence tooling. It does not change host state, certify a boot image, award disputed sibling ownership, or establish a general verification method. C1 counts the five explicit sourced decisions, not Git execution or consumer behavior; C2 independently exercises consumers.

## Source proposition and lane policy

S081, SPECIFYING REVISIONS `<rev>^{<type>}`, says: “For example, if <rev> is a commit-ish, <rev>^{commit} describes the corresponding commit object.” The same heading's empty-brace form stops at a non-tag object, which need not be a commit. S082, OPTIONS `--verify`, says: “you can add the `^{type}` peeling operator to the parameter.” Both quotations are located in version2.56.0, accessed2026-10-21; no renderer-specific line number is an authoritative locator.

Git supports many revision expressions. This lane deliberately accepts only7–64 hexadecimal selectors naming a unique actual object, then requires commit peeling. Its chosen commit must be an ancestor of the named lane branch, and of origin's corresponding branch when that ref exists. Those object-prefix/ancestry/push restrictions come from the lane's evidence contract, not these manuals. A tag object itself need not be on the commit ancestry graph; the peeled commit is what is checked.

## Five fixed decisions

| Class / row ID | Git distinction | Lane outcome | Refusal finding | Sources |
|---|---|---|---|---|
| commit | Existing commit object already has requested type | accept-if-landed-and-pushed | ancestry failures retain E-REVISION-NOT-LANDED / E-REVISION-NOT-PUSHED | S081, S082 |
| tree | Existing tree, even a non-empty one, is not commit-ish | refuse | E-REVISION-INVALID | S081, S082 |
| blob | Existing file-content object is not commit-ish | refuse | E-REVISION-INVALID | S081, S082 |
| tag-to-commit | Annotated tag, including nested annotated tags, peels recursively to the commit | accept-if-landed-and-pushed | ancestry failures retain E-REVISION-NOT-LANDED / E-REVISION-NOT-PUSHED | S081, S082 |
| tag-to-noncommit | Tag peels to tree or blob, not to the requested commit type | refuse | E-REVISION-INVALID | S081, S082 |

“Pushed” means only the local origin tracking ref when present, as defined by the binder. It does not prove current remote reachability or hosting-service state. Refusals exit2/could-not-evaluate, with exactly one binding finding. Their diagnostic `revision` field may echo the selector; an echo is not an accepted binding. Accepted controls must match the independently expected full peeled commit SHA.

## Error patterns and actionable review checklist

- `^{}` substituted for `^{commit}`: rejects neither every direct tree nor every tag-to-tree/blob; require real non-empty-tree and both noncommit tag-target controls.
- Testing binder helpers alone: leaves argument propagation and actual consumer CLI boundaries unchecked; run each frozen original-nine consumer separately in an isolated clone.
- Counting a new mode as a repaired binder: incorrect if the binder already behaves correctly. Report matrix implementation coverage and executed behavioral cases separately; before0 describes missing coverage, not nine broken consumers.
- Rewriting the old frozen metric after seeing its outputs: invalidates the preregistration. Preserve round20 `--object-selectors`; use a separately named opt-in target-type matrix.
- A scope/hash declaration is not proof of actual nonexecution/reading. Preserve missing or malformed reports, and bind each review's primary bytes and exact predicate before dispatch.

The original-nine denominator, case expectations and immutable baseline are in `.ufo/waves/round-21/preregister.json`. The new gate commands and actual results belong in SCORECARD Round21 and the committed measurement ledger. No unrun gate is declared passed here.

## QUALITY check

Criteria1–3: five finite decisions distinguish documented semantics, lane policy and unknown remote state. Criteria7/19/21: opened scopedA S081/S082 support the exact typed-peeling proposition at versioned headings; they do not support host or ancestry assertions. Criteria14: this performed check evaluates sources and scope, not pending implementation tests. Criteria24/31/38/40/41: execution classes, review identities and old matrix limits remain explicit; wrong-peeling and mismatched-receipt controls must show the corresponding fixes able to fail. Decision/source agreement is author-side; independent non-author admission remains pending.
