# AttackNegativeRestore — round 15 critic (depth, C1 R15-POSITIVE-DOMAIN)

Target: `tools/check-locator-clarification.py` (LocatorGate, mtime 04:47, read statically). Selftest/CLI **not executed**; no test pass is claimed. Probes below used regex literals copied into a standalone Python cell, run on strings, never the checker module. r15 MD/JSON pair was not yet present when this was written.

## Source boundary (reopened 2026-10-20)
`curl https://man.archlinux.org/man/systemd.exec.5` → HTTP 200, 293394 B, sha256 `26f9a182…d25043` (same as SourceRegistry SOURCES:88), footer **systemd 262.1**. SANDBOXING > ProtectSystem= opens with the positive definition “Takes a boolean argument or the special values "full" or "strict".” The page has no absence sentence (case-insensitive counts: `further values` 0, `no other values` 0, `exhaustive` 0). So the positive sentence is supported. “Documents no further values” is an unswept page-absence claim. The checker must keep these two propositions apart.

## Counterexamples (each passes a predicate it should fail)
1. **QNEG blanket exemption (high).** `absence_sites` drops every sentence that matches `supersed|withdraw|historical|does not|do not|rather than|instead of|negative|not a claim…`. Sentences restoring the claim with any of those words all slip through (flagged=False): “…documents no further values, rather than leaving the domain open.” / “Unlike the historical r14 wording, S046 documents no further values…” / “S046 documents no further values; this correction does not need a sweep.” / “R15-POSITIVE-DOMAIN supersedes the r14 locator, and the page documents no further values.” The only restore fixture (`restored-negative-md/json`) appends a sentence without any exempt word, so it passes without testing the exemption. This repeats r14 `active_restore` (paragraph exemption on `replac|supersed`), now at sentence level.
2. **ABSENCE is too narrow (high).** None of these is flagged: “the only documented values”, “complete documented value domain”, “— and only these.” (the attack hidden behind the positive quote), “documents no more values”, “accepts nothing else”, “documented values are exhaustive”, “value domain is closed”. The regex catches only `document(s) no further|other|additional value(s)`, `no further|other|additional (documented) value(s)` and `value set is closed|exhaustive`.
3. **Opposite polarity is unchecked (medium).** “…boolean, full and strict; the value set may be open.” passes all R15 pins. This brings back the r13 MD:97 defect that R14-VALUE-DOMAIN fixed. The r14 `DOMAIN_BAD` also misses `may be open`, `may not be exhaustive` and `may accept other values`.
4. **History rewrite is masked by the notice (high).** `history_issues` requires only that `documents no further values for` and `rendered lines 1266-1267` occur somewhere in r14 MD. The appended `## R15 supersession` section quotes both. I deleted both historical sites (MD:41-42 proposition, MD:52-53 replacement) and the MD:34 line locator from a copy. The plain-text occurrence count went 4→2, both survivors sit after the notice heading, and the predicate is still True. Append-only preservation is not enforced.
5. **Active-scan holes once notices exist (high).** r14 MD is scanned for absence only when `md14_notice_ok` is False. r14 JSON is never scanned for absence. In r15 JSON only `replacement` is scanned. So a restore in r14 MD after the notice, in r14 JSON `r15_supersession.notices[1].replacement_scope` or `limits`, or in r15 JSON `location`/extra keys passes. Example: `location` “…ProtectSystem= first definition; the page documents no further values” (LOC_NUM: no hit). The actual baseline JSON site `$.corrections[0].replacement` is also never reported: `BASE_JSON14` has no `replacement`, so the spec's “identify actual … negative absence phrase” holds for MD only.
6. **The wrapped line hides a site from line tools.** r14 MD:52-53 breaks “documents no / further values”. A line grep sees only MD:42. The checker's `" ".join(split())` handles this correctly; keep it. A zero-width-space split still evades (low; disclose as a limit).

## Controls that must stay green
These were checked against the proposed predicates, not the checker. Probes show no false hit on any of them:
- the exact S046 quote;
- r14 “not a claim about undocumented values”;
- the r14 notice “makes no statement about undocumented values”;
- `not_claimed` “exhaustive documentation absence”;
- mechanism non-exhaustive prose;
- the r13 comparative “strict is the only value that covers the hierarchy”, which a bare `only … value` rule would wrongly flag.

Two broad terms cause unrelated hits and must be scoped:
- `nothing else` hits r13 MD (“Nothing else is s…”) and SKILL (“oom=1 … nothing else”).
- An open-domain rule hits the legitimate negated sentence in SOURCES, “not a statement that the option's value domain is open”.

## Smallest safe correction (LocatorGate-owned file only)
- **Ledger of loci instead of word exemptions.** Allow the phrase at exactly these places and nowhere else:
  - r14 MD § R14-VALUE-DOMAIN: exactly 2 historical hits, which must remain (this is the history check);
  - r14 MD § R15 supersession: inside quotation marks only;
  - r14 JSON `$.corrections[0].replacement`: historical, must remain;
  - r14 JSON `$.r15_supersession.notices[*].superseded_text` and r15 JSON `supersedes`: pointers.

  Any other hit is `NEGATIVE_DOMAIN_UNSWEPT`, whether or not notices exist. Scan every r15 JSON string and the whole r15 MD.
- **Remove QNEG** for r15 JSON fields. In r15 MD, exempt only a sentence where the phrase is inside quotes **and** a `supersed|withdraw` verb is present.
- **Widen ABSENCE** to cover:
  - `(documents?|lists?|names?|defines?) no (further|other|additional|more) (values?|spellings?|arguments?|forms?)`;
  - `no (further|other|additional|more|undocumented) values?`;
  - `only (these|those)`, `and no others?`, `exactly (these|three)`;
  - `(the )?only (documented )?(values?|arguments?)(?! (that|which) (covers?|makes?|mounts?))`;
  - `(complete|closed|exhaustive|entire) (documented )?(value )?(domain|value set|set of values)`.

  Add `nothing else` only inside r15 correction text. Probe: all 9 restore paraphrases above are flagged; the controls are not.
- **Add an OPEN_DOMAIN predicate** on r15 replacement/MD positive section. Pattern: `value (set|domain)|values` followed by `(is|are|may|might) (not )?(be )?(exhaustive|closed|complete|open)`, or `may (accept|take|include) (other|further|additional) values`. Apply the r14 `negated()` guard.
- **Fixtures to add:** QNEG-word restore, “— and only these.”, “complete documented value domain”, “value set may be open”, restore in JSON `location`, restore in r14 MD after the notice, and both MD historical sites deleted with the notice present. Each must FAIL and set POSITIVE count to 0. The positive-only clean fixture keeps count 2.

## Impacted axes
**depth:** the R15-POSITIVE-DOMAIN count can certify a restored negative or a history rewrite (false provenance). **calibration:** the red/green restore fixture is close to vacuous. Other axes are untouched. All of these are fixable defects, not tradeoffs that require rejection. The positive-definition proposition itself is source-correct.

## Limits and tools
Static reading of the checker; regex probes on string literals; one source GET. No checker, selftest, build or lint run. No host or package action. Tools installed or updated: **none**.
