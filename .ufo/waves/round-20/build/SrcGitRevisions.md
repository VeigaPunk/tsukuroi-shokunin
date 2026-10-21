# SrcGitRevisions — round20 attempt1

Axes: source fidelity; scope calibration; curation usefulness.

## Source and located evidence

- Source URL/path: https://git-scm.com/docs/gitrevisions/2.56.0 — `SPECIFYING REVISIONS`, `<sha1>` and `<refname>` entries.
- Accessed: 2026-10-21. The document identifies itself as gitrevisions updated in 2.56.0.
- Exact quotes (each under 25 words):
  - “The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository.” (18 words)
  - “When ambiguous, a <refname> is disambiguated by taking the first match in the following rules:” (15 words)

## Evidentiary scope

The page supports that a full SHA-1 name or repository-unique leading substring can name an object, and that a symbolic `<refname>` has an ordered lookup rule when ambiguous as a refname. The listed lookup order starts with `$GIT_DIR/<refname>`, then `refs/<refname>`, tags, heads, remotes, and remotes' `HEAD`.

It does **not** establish precedence when the same token could denote both an object name and a ref; the quoted ambiguity rule is explicitly about `<refname>` lookup. It also does not establish object-prefix enumeration, commit-ish peeling, behavior of a particular command or repository, or lane ancestry/push status.

## Candidate row recommendation

**Tier A; admit narrowly** for the claim that Git documents full/unique SHA-1 object-name syntax separately from symbolic refnames and defines ordered lookup among ambiguous refnames. **Reject** any teaching that this source settles cross-kind object-name-versus-ref precedence. Reason: the source's disambiguation sentence covers refname matches only. **Flip:** admit the broader claim only if the row is narrowed to the supported refname lookup distinction or a direct primary-source passage explicitly supplies the cross-kind precedence.

Scope: executed=none
