# ReviewLocatorNotices — round 15 (C1 locator and negative-wording notices)

Seat: TsukuroiR15.ReviewLocatorNotices (reviewer, read-only, leaf). Baseline 0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2.

## Status at review

- `corpus/knowledge/source-locator-clarification-r15.md` and `.json` were NOT present when checked (glob `corpus/knowledge/source-locator*` empty). This review covers the r14 loci the pair must supersede, the S044/S045 quotes, and the planned R15-LOCATOR / R15-POSITIVE-DOMAIN scope from the assignment. Re-review the landed pair against this list.

## Verdict

Scope is correct: the S044 quote stays true; only supplemental rendered-line locators and unsupported negative wording need notices. No quote needs supersession.

## Verified (observed, 2026-10-20)

- S044 quote "Takes a boolean argument or the special values "full" or "strict"." is exact. Reader text of https://man.archlinux.org/man/systemd.exec.5: heading `*ProtectSystem=*` at reader line 1270 (under `# SANDBOXING`, line 1244); definition at 1272-1273; joined = 11 words.
- Footer `systemd 262.1` at reader line 4327.
- Reader lines 1266-1267 are NOT the definition: they are the AF_UNIX sentence ("(such as *ProtectSystem=*, *ReadOnlyPaths=*, ...) do not affect ... AF_UNIX sockets"). Confirms the round-14 lesson note (lesson:234-236).
- Replacement facts match source: "full" adds /etc/ to the read-only mounts made by true; "strict" covers the hierarchy except /dev/, /proc/, /sys/.
- S045 quotes are exact substrings of the comment-6071740243 body (fetched 2026-10-20 via GitHub issue route): VM assertion 16 words; "Codex Medium reviewed ... same conclusion." 14; independence caveat 16; "waiting on the maintainer to decide whether snapshot boots should keep the overlay." 13 (#6634 referent); "This now waits on your answer." 6. Notice must not touch these.

## Locator loci to supersede (supplemental only; quote unaffected)

- L1 `corpus/knowledge/source-scope-correction-r14.md:34` "rendered lines 1266-1267" (Source object paragraph).
- L2 `corpus/knowledge/source-scope-correction-r14.json` corrections[0].location (line 13): "rendered lines 1266-1267".
- L3 same JSON sources[0].anchor (line 167): "rendered lines 1266-1267".
- SOURCES.md:50 (S044 row) has no rendered-line locator; no notice needed there.
- Lesson `corpus/lessons/round-14-verifier-spotcheck.md:234-239` is historical; do not edit. Record its request in the notice instead.
- Recommended replacement anchor: stable `SANDBOXING > ProtectSystem=` heading + footer `systemd 262.1` + quote. Any new bare line number must be labelled reader-specific (lesson says do not rely on bare reader line numbers).

## Negative wording to supersede (not the quote)

- N1 r14 MD:42 "The opened revision documents no further values for `ProtectSystem=`."
- N2 r14 MD:51-53 Replacement block, clause "and documents no further values for this option."
- N3 r14 JSON corrections[0].replacement (line 15), clause "and it documents no further values for this option."
- N4 lesson item 2 (lesson:240-245) asks for a bounded documentation sweep OR positive-only wording. Choose one and record it.
- Keep, do not supersede: mechanism-scoped "illustrative, not exhaustive" sentences (MD:55-57, JSON replacement). These are mechanism scope, not value domain.
- Positive domain alternative (supported): "The opened revision's § ProtectSystem= definition gives the argument as a boolean or the special values full and strict."

## Bounded sweep (new, this review)

Grep of all `ProtectSystem` occurrences in the reopened reader text (reader lines): 750 (implies `strict`), 1251, 1260, 1266, 1270-1289 (definition: boolean / "full" / "strict" only), 1289 (`set to "strict"`), 1548 (`strict`), 2501 and 2680 (setting lists), 4327 footer. No other value is defined. This supports a positive statement; it is one revision in one reader rendering, not proof of the parser or of other systemd versions. If the notice keeps any "documents no further values" wording it must say so is a sweep result, dated, and scoped to that rendering.

## Gate coupling (static reading only; not executed)

- `tools/check-source-scope-correction.py:161-162` requires, in the R14-VALUE-DOMAIN section, the tokens s044/97/boolean/full/strict/mechanism AND "non-exhaustive" or "not exhaustive". Deleting the mechanism-scoped non-exhaustive sentence from that section would fail this pin; keep it when rewriting.
- `DOMAIN_BAD` (line 27-28) and `MECH` (34-36) regexes do not match "documents no further values". The checker therefore cannot detect N1-N3 removal either way; if the notice is meant to be enforced, that is an L1 decision, not a reviewer edit.

## Findings by severity

1. (medium) Pair absent at review time; no notice text exists to check against the list above. Re-review on landing.
2. (low) Any R15 text that re-states the rendered line numbers as current locators repeats the defect the lesson flagged. Label them reader-specific or omit.
3. (low) S044 row teaches "the boolean and the two named modes are the documented values" (SOURCES.md:50). Positive; sweep supports it. No change needed.
4. (info) Replacement sentences in r14 are accurate to the page; no factual defect found in r14 replacement content beyond N1-N3.

## Residual risk and verification gaps

- Only the man.archlinux.org reader rendering was inspected; other renderers may place the sentences at different line numbers. Heading-based locators avoid this.
- No checker was executed; gate statements are static reading.
- S045 quotes checked by reading one fetch route; not re-verified against the authenticated API.
- No package, service, or host action; no pacman guard applicable.

## Tools

read, grep, glob (read-only). Installs/updates: none. Host changes: none. Tests/builds/checkers executed: none.
