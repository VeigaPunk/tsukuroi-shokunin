# MistakeScribe — round-14 repair draft

Seat: `TsukuroiR14.MistakeScribe` (leaf, depth). Baseline HEAD `8606bad` (confirmed). Report-only; no other writes. `corpus/QUALITY.md` (uncommitted, L1-owned) was read, not edited.

## Mistake rows

| # | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | R14-VALUE-DOMAIN: documented option domain conflated with the open mechanism set | E1, E2, E3 | Outside closure spotcheck:143-153; legacy gate blind | Append R14-VALUE-DOMAIN notice after provenance trio; keep r13 MD:97 bytes; replacement and ≤25-word quote per E1 |
| M2 | R14-COMMENT-ATTRIBUTION: "self-described model-generated" transferred to #8047 comment | E4, E5 | Outside closure spotcheck:155-165, 178; QUALITY #18 blanket label | Add S045 row (tier C, comment 6071740243); supersession notice for S042; quote body only |
| M3 | Stale S041 draft metadata in correction JSON | E6 | Outside closure routed defect 3 (spotcheck:243-247); not caught by census or gate | R14 JSON `erratum` block with was/now; leave r13 JSON bytes in place |
| M4 | Oversized legacy `gate_contract`: 10 headings and 13 field-scan entries, 5 headings executable | E7 | Outside closure routed defect 4 (spotcheck:248-252); no round-13 Mistakes row | Do not copy into R14; R14 `gate_scope` lists only consumed fields plus `not_enforced`; erratum records 5/10 headings and 0/13 scan entries |
| M5 | QUALITY19 red-before evidence absent: criterion is text-only, names no fixture | E8 | Not captured by any row | Require the red/green/mutant set in §Red-before before the fix counts |

## Evidence notes

E1 (M1). r13 MD:97, replacement cell of row "r12 MD:41-42": "…the value set is not exhaustive". systemd.exec(5) ProtectSystem= paragraph (reader text, opened this seat): "Takes a boolean argument or the special values "full" or "strict"." (11 words). Proposed replacement: "Among ProtectSystem= values, the documented domain is a boolean argument or the special values full and strict (S044); the non-exhaustive qualifier applies only to unit-side mechanisms (S041)." Sweep of `exhaustive` in r13 MD/JSON and lesson: MD:97 is the only defect; other hits (MD:31, :84, :102 old-claim column, JSON alternatives_scope, :120, :145, :157) are correct or quoted history.

E2 (M1 constraint). MD:97 must remain (historical bytes preserved). A red predicate that forbids the phrase anywhere in the file would violate preservation. Predicate should accept the phrase only inside a block that quotes it as superseded by R14-VALUE-DOMAIN, and reject it in any active line.

E3 (M1 legacy gate). `tools/check-root-dac-correction.py:112` and `:148` test `"non-exhaustive" in low or "not the only" in low` over the whole file; MD:31 supplies "non-exhaustive", so MD:97 passes. Measured, not re-run: `.ufo/waves/round-13/correction/verification-fixed.json` at c35d356 gives PASS, correction_count=1, findings=0; the spotcheck (lines 102-103, 129-130) records MD bytes at c35d356 equal to delivered.

E4 (M2). S042 (`corpus/SOURCES.md:48`): "the sole comment is self-described model-generated automated triage by `omarchybot`". Comment 6071740243 body, read from the rendered github.com/omacom/omarchy/issues/8047 page (api.github.com returned HTTP 403 rate-limit from this host): "I tried this on a stock Omarchy worker VM…"; "**Second opinion.** Codex Medium reviewed the same evidence…"; "It may have seen this analysis first, so its agreement is not guaranteed to be independent."; "This now waits on your answer."; maintainer deferral appears only for #6634: "waiting on the maintainer to decide whether snapshot boots should keep the overlay". Body contains no "model", "automated", "triage" or "bot". HTML shows login omarchybot and a Collaborator badge; API type and association were not re-observed.

E5 (M2 transfer risk). #6629 comment 6234472369 (S043) carries the "Nothing was run on a machine" / "Claude Opus 5.5 alone" disclaimer per spotcheck:179-180. That disclaimer must not be copied to S045. Leave S043 as is.

E6 (M3). r13 JSON `sources[0]` lines 267-268: `"status": "reserved"`, `"registry_owner": "SourceRegistry"`. `corpus/SOURCES.md:47` status cell: `mined` (opened 2026-10-20, recheck on-release). `LOG.md:598`: "joined, not reserved". Census validate passed (spotcheck:198-204) but reads no JSON metadata.

E7 (M4). r13 JSON `gate_contract` lines 204-243: `required_md_headings` ×10 (210-221), `corrected_field_scan` ×13 (222-236), `active_supersession` (237-241), `rule` (242). Checker `md13_issues` checks five headings (lines 100-104). No checker reference to `gate_contract` or the field scan (grep: no match). Historical markers checked only as CURRENT-HOST/R13 (:167) and B2-LIMIT (:169).

E8 (M5). `corpus/QUALITY.md` (`git status`: ` M`) already has #19 (line 26) and #20 (line 27). Both cite `corpus/lessons/round-14.md` (absent; lessons dir has round-13 files only) and S044/S045 (absent from SOURCES.md). #19 requires that the check "fail the preserved prior defects and restored-defect fixtures", but no fixture is defined anywhere in `.ufo/waves/round-14/`.

## Recommendations

Red-before for QUALITY19 (draft for L1; the set must pass before R14 counts as fixed):
- R-1 (M1 red): value-domain predicate on bytes with MD:97 sentence as active prose → exit 1, finding names file:line.
- R-2 (M2 red): attribution predicate on S042 wording "self-described model-generated" used as the active attribution → exit 1.
- R-3 (M2 transfer mutant): insert "This review is by Claude Opus 5.5 alone" into S045 or the R14 attribution text → exit 1.
- R-4 (M1 restored-defect mutant): corrected r13 MD with MD:97 sentence reinserted outside the superseded block → exit 1.
- R-5 (quote bound mutant): any quote over 25 whitespace words → exit 1.
- R-6 (green): corrected R14 pair plus S045 at the committed revision → exit 0, correction_count 2.
- R-7 (legacy gate): report only as measured blind (E3); never as proof of source wording.
- R-8 (record): per run, argv, `git rev-parse` hash, bytes from `git show <rev>:<path>` (never the mutable worktree while QUALITY.md is uncommitted), exit, stdout, sha256. Retain any first failing selftest, as round 13 did (`closed-list-restored`).
- R-9 (non-claim): green proves conformance only; source wording still needs a reopened source record.

Wording for L1 (do not copy the spec phrase "maintainer deferral" unscoped):
- Scope maintainer deferral to the #6634 remount item. The #8047 comment's own status line is "This now waits on your answer" (reporter).
- S045 API fields (login, type, association) must be marked carried from S042 and unverified unless a successful API read is recorded.
- QUALITY #19/#20 and the R14 pair point at `round-14.md`, S044 and S045, none of which exist yet. Land them in the same commit or the pointers dangle.

Structural fixes:
- R14 JSON `erratum` block: `{target: corpus/knowledge/root-dac-correction-r13.json, pointer: sources[0], was: {status: reserved, registry_owner: SourceRegistry}, now: {status: mined, registry_row: corpus/SOURCES.md S041}}`. Keep the `corrections` array exactly two objects.
- R14 JSON `gate_scope`: only fields the new checker reads, plus `not_enforced` and the claim "bounded conformance, not source truth". Do not copy the r13 10-heading or 13-field lists.

## Method, limits, tooling

- Reads only: AGENTS.md, RULES.md, round-13 spotcheck, wave spec and dispatch headers, r13 MD/JSON, SOURCES rows S039-S043, checker source, QUALITY.md, round-13 lesson Mistakes, verification JSONs, LOG.md, #8047 issue page, systemd.exec(5) reader text.
- Shell: `git status`/`log`/`rev-parse` and SOURCES cell extraction, plus one curl of the comment API (HTTP 403). No checker, selftest, census, build, test or lint run.
- Limits: systemd.exec footer and API fields not re-observed; quotes come from reader rendering; the comment quotes are from the HTML page, not the API JSON.
- Tools installed or updated by this seat: none.
- No edits outside this report.
