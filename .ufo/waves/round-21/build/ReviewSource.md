# ReviewSource — Git type-peeling vs `tools/_revision.py` policy (round 21)

Reviewed-SHA256: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
Predicate: source-Git-policy-separation

Reviewed snapshot: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-21/snapshot/tools/_revision.py` (440 lines, read in full).
Hash line is the item-supplied pin; this seat is NO-EXEC and did not independently hash the snapshot.

## Axes

- A1 accepted input syntax (what strings can reach object resolution)
- A2 object identity and uniqueness (prefix vs ref, ambiguity)
- A3 type peeling (tag to commit; non-commit refusal)
- A4 landing policy (ancestry of `refs/heads/<branch>` and optional `refs/remotes/origin/<branch>`)

## Official Git text (git-scm.com, manuals at 2.56.0; quotes ≤25 words, exact)

- Q1 gitrevisions / git-rev-parse, `<rev>^{<type>}`: "dereference the object at <rev> recursively until an object of type <type> is found or the object cannot be dereferenced anymore (in which case, barf)."
- Q2 gitglossary, commit-ish: "A commit object or an object that can be recursively dereferenced to a commit object."
- Q3 gitglossary, peel: "The action of recursively dereferencing a tag object."
- Q4 gitrevisions, `<sha1>`: "The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository."
- Q5 git-rev-parse, `--verify`: "will make sure `$VAR` names an existing object that is a commit-ish (i.e. a commit, or an annotated tag that points at a commit)"
- Q6 git-rev-parse, `--disambiguate`: "Show every object whose name begins with the given prefix."
- Q7 gitglossary, reachable: "All of the ancestors of a given commit are said to be "reachable" from that commit."
- Q8 git-merge-base, `--is-ancestor`: "exit with status 0 if true, or with status 1 if not. Errors are signaled by a non-zero status that is not 1."

## Separation: Git commit-ish vs our policy

| Axis | Git (docs) | `_revision.py` snapshot |
| --- | --- | --- |
| A1 syntax | Extended SHA-1: refnames, `HEAD`, `@`, `^`/`~`, ranges, `:/`, `^{type}` | `REV = ^[0-9a-fA-F]{7,64}$` (L41, L175-176); everything else is E-REVISION-INVALID |
| A2 identity | `<sha1>` unique prefix (Q4) **or** `<refname>` via the dwim rules | Object IDs only: `rev-parse --disambiguate=<lower>` (L119), exactly one object of any type (L123-124); refs never consulted for the revision |
| A3 peeling | commit-ish = commit or tag chain to commit (Q2, Q3); `^{commit}` "barf"s otherwise (Q1) | `cat-file -t`: commit returns oid (L134-135); tag peels via `<oid>^{commit}` (L139-142); blob/tree/tag-to-non-commit return None, which becomes E-REVISION-INVALID |
| A4 landing | Not part of commit-ish; peeling says nothing about reachability | Extra policy: ancestor of `refs/heads/<branch>` (L184-185), and of `refs/remotes/origin/<branch>` when that ref exists (L188-190); `merge-base` rc≥2 is E-GIT-FAILED (L156-160, consistent with Q8) |

## Observations (source-grounded)

- O1 The A3 peel semantics match Git commit-ish: annotated tag → commit is accepted; nested tag → tag → commit is accepted (selftest `nested-annotated-tag-object`, L362-365); tag → blob/tree is refused (L413-419). This follows the glossary (Q2, nested), which is broader than the `--verify` parenthetical (Q5, single annotated tag). The code takes the glossary reading.
- O2 A1 and A2 are stricter than Git on purpose. Hex-named branches and tags that are not object prefixes are refused (`ghost-hex-branch`/`-tag`, `ghost-full-hex-*`, L272-312). A real object prefix wins over a same-named branch or tag (`real-prefix-shadowed-by-branch-and-tag`, L321-322). Git's own docs list `<sha1>` and `<refname>` as alternative spellings and never say which wins for a hex-looking name. The policy removes that dependence.
- O3 For ambiguity, uniqueness is counted over all object types before any type check (docstring L114-117; selftest `ambiguous-object-prefix` with a synthetic colliding blob, L378-397). This is the literal Q4 reading ("unique within the repository"). It does not use Git's commit-ish-hinted disambiguation.
- O4 A4 has no Git commit-ish counterpart. Landing and pushing are tsukuroi requirements built on Git reachability (Q7) via `merge-base --is-ancestor` (Q8), with exit codes 0 and 1 as the only boolean outcomes.
- O5 `bind()` resolves a branch only after the revision passes A1-A3 (`precedence-rev-before-missing`, L251). This matches the docstring order in steps 1-6 (L13-21).

## Inferences

- I1 [INFERENCE] With a `^{commit}` peel, Git's `rev-parse` applies a commit-ish disambiguation hint, so an ambiguous prefix whose only commit candidate collides with a blob could resolve in Git but is refused here (O3). This is stricter by design and matches the docstring. I did not fetch the official `core.disambiguate` text.
- I2 [INFERENCE] The tag path re-parses the full hex `<oid>^{commit}` (L139-140). It is correct only because Git prefers a full-length object name over a same-named ref. The official docs do not state this precedence. The selftest `full-tag-object-id-ref-shadow` (L368-377) pins the behavior empirically. The docstring "never by reparsing that full hex as a ref" (L116-117) describes this intent accurately, but it relies on Git implementation behavior rather than documented behavior.

## Gaps / limits

- G1 `REV` admits 41-64 hex digits. In a SHA-1 repository, `--disambiguate` with a prefix longer than the hash length is not covered by the official docs or by the selftest (only 65 hex is tested, L242). [INFERENCE] Git likely prints nothing and exits 0, which would give E-REVISION-INVALID. If it exits non-zero instead, the result is E-GIT-FAILED (L120-121). Unverified.
- G2 The quotes come from the git-scm.com "latest" pages (2.56.0). The installed git version was not probed (NO-EXEC).
- G3 This was review only. The selftest was not run and nothing was hashed.

Tooling: none installed or updated. Docs were read via a read-only web fetch of git-scm.com; local Git docs (`/usr/share`) are not installed.

Lane bounds: leaf member — no subagent dispatch.

Scope: executed=none
