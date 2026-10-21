# Git rev-parse source finding

- **Source:** [git-rev-parse, version 2.56.0](https://git-scm.com/docs/git-rev-parse/2.56.0), `OPTIONS` headings `--disambiguate=<prefix>` and `--verify`; accessed 2026-10-21.
- **Located quotes (verbatim, each ≤25 words):**
  - `--disambiguate=<prefix>`: “Show every object whose name begins with the given prefix.” (10 words)
  - `--verify` example: “`"$VAR^{commit}"` will make sure `$VAR` names an existing object that is a commit-ish” (13 words); the same paragraph explains this includes a commit or an annotated tag pointing at a commit.
- **Supports:** prefix enumeration of repository objects (with the documented minimum of four hexadecimal digits); and verification of a parameter as an object of the requested type when using `^{commit}`, including peeling an annotated tag that points to a commit. This supports separating object-prefix lookup from the subsequent commit-ish type check.
- **Does not support:** a claim that `--disambiguate` itself chooses a unique match, rejects ambiguity, verifies commit type, or enforces any caller's ordering/normalization. It does not certify branch/ref selection, ancestry, push/landing status, or the correctness of a particular binder.
- **Candidate row recommendation: A — admit, narrowly.** The versioned official Git manual directly documents both propositions; keep the row limited to object-prefix enumeration and `--verify`/`^{commit}` commit-ish peeling. **Flip to reject** if the cited page/quote cannot be reproduced or the row is used to claim caller behavior (uniqueness handling, ref precedence, ancestry, or push certification) that the manual does not establish.
- **Confidence:** high for the documented option semantics; no implementation or runtime behavior was inspected.
- **Remaining unknowns:** whether the lane implementation applies these operations in the required order and handles ambiguity as intended; this source alone cannot settle those questions.

Scope: executed=none