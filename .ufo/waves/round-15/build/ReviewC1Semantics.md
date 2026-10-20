# Round 15 — C1 positive-definition review (ReviewC1Semantics)

Scope: read-only review of the C1 positive ProtectSystem= definition against the primary source. Verdict: the positive quote is exact and supportable as a documented-domain statement on the opened revision. Any parser-exhaustiveness or "no other values exist" reading is rejected.

## Evidence (observed 2026-10-20)

1. Primary source reopened: https://man.archlinux.org/man/systemd.exec.5 (footer `systemd 262.1`, line 4327 of the rendering). Heading `SANDBOXING > *ProtectSystem=*` at rendered line 1270; definition at 1272–1273. Rendering held as session artifact `artifact://13344` (4328 lines).
2. Exact quote (line break joined by one space), 11 words, matches the C1 interface string:
   > Takes a boolean argument or the special values "full" or "strict".
3. Text sweep of the artifact for every `ProtectSystem` token (regex `ProtectSystem`): occurrences at lines 750, 1251, 1260, 1266, 1270, 1272–1273 (definition), 1285, 1289, 1548, 2501, 2680. Value tokens attached to it anywhere in the rendering: `strict` (750, 1289, 1548), `full` (definition only), boolean. No other value token found. This is a bounded text observation of the rendered page, not a proof about the parser.
4. Locator collision: the same sentence shape appears for other options — ProtectHome= at 1297–1298 (`"read-only" or "tmpfs"`) and ProtectControlGroups= at 2104–2105 (`"private" or "strict"`). A quote search on "Takes a boolean argument or the special values" or on `"strict"` alone lands on the wrong option. Line 1266 mentions `ProtectSystem=` inside the AF_UNIX/socket sentence (not a definition).
5. r14 lesson locator claim checked: lines 1266–1267 are the AF_UNIX paragraph (1266 mentions ProtectSystem= in passing); 1270 heading and 1272–1273 definition match the lesson's statement. The reader numbering is renderer-dependent; the stable locator is the heading plus the quoted phrase.
6. Source-ID state: `corpus/SOURCES.md` has S043, S044 (line 50, systemd.exec.5, docs/A) and S045 (line 51). No S046 row exists yet. S044 already cites the same URL, so a new S046 for the same URL would add another duplicate-URL W04 (census already reports W04 for S044 with S041).
7. C1 pair files (`corpus/knowledge/source-locator-clarification-r15.{md,json}`) do not exist yet; the review was against the r14 pair (`source-scope-correction-r14.md:31-60`, JSON R14-VALUE-DOMAIN) and the C1 interface text.

## Findings

- F1 (accept): R15-POSITIVE-DOMAIN quote is exact (11 words) and locates to the ProtectSystem= definition, not to ProtectHome= or ProtectControlGroups=.
- F2 (reject): any sentence implying parser exhaustiveness ("the only accepted values", "no further values exist", "the parser accepts only…"). The page documents the argument domain; it does not enumerate parser acceptance. The spelling set of "boolean argument" is defined by systemd.syntax(7), which was NOT verified here (see Limits).
- F3 (fix wording): the r14 phrase "documents no further values for this option" is a negative claim. Restate it as a bounded observation: "In the opened rendering (systemd 262.1), the text names no other ProtectSystem= value; this is a text sweep, not a parser property." Record the sweep regex and artifact date in the evidence.
- F4 (locator): cite by heading + quote, never bare line numbers: `systemd.exec(5) > SANDBOXING > *ProtectSystem=*`, definition paragraph beginning "Takes a boolean argument or the special values" followed by `"full" or "strict"`. Reader lines 1270 and 1272–1273 may be cited only as "renderer-dependent, captured 2026-10-20, footer systemd 262.1".
- F5 (source ID): do not mint S046 for this URL unless SourceRegistry accepts a scope-separated duplicate; prefer citing S044 (existing row). If S046 is required by the wave, SourceRegistry must record the duplicate-URL W04 explicitly.

## Recommendations (for L1; not written by this review)

- R15-POSITIVE-DOMAIN proposition: "On systemd 262.1's systemd.exec(5) rendering, the documented argument form of ProtectSystem= is a boolean argument or the special values "full" or "strict"." Quote as in Evidence 2. Do not add "only", "exhaustive" or "parser".
- R15-LOCATOR: heading-based, as in F4; retain the renderer caveat; do not rewrite the r14 history.
- Keep the 0→2 depth count unchanged (depth ordinal unchanged) unless L1's own gate says otherwise.

## Limits

- systemd.syntax(7) (boolean spellings) could not be fetched: `https://man.archlinux.org/man/systemd.syntax.7` → ECONNRESET; `…/systemd.syntax.7.en` → timeout. Boolean-spelling claims remain unverified.
- No systemd source code, no parser behavior, no host systemd version checked. Host runtime not probed.
- The rendering is a session artifact (`artifact://13344`) and is not durable; a durable evidence copy must be created by the owning lane if needed.
- Text sweep scope: the rendered page only, regex `ProtectSystem` and value tokens listed above.
- S046 row absent; this review did not write SOURCES.md.
- No tests, builds, or verification runs performed; none claimed.

## Tools and installs

- Tools used: read (man.archlinux.org fetches, lane corpus files), grep (artifact 13344, SOURCES.md), glob.
- Installs/updates: none. No package, service, or sudo action taken.
