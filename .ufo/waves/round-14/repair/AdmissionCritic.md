# AdmissionCritic — round 14 repair, C1 depth (structural count gaming)

Critic seat. This is author-side advice, not admission. Axis: **depth**. Guardrails: calibration and adjacency must not move.
Reviewed 2026-10-20 against baseline `8606bad`, with the worktree holding only L1's uncommitted QUALITY #19/#20 and wave reports.
The r14 pair and `tools/check-source-scope-correction.py` were **absent** when I read them, so this report attacks the design in spec.json and the r13 loci that remain active.
Tools installed or updated: **none**.

## Core counterexample: a correction_count of 2 can pass while both defects persist
The planned gate counts named objects (0..2), checks that each quote is ≤25 words, and checks that ids and supersession notices are present.
A pair that passes all of those checks can still be false. Example: R14-VALUE-DOMAIN with replacement "the ProtectSystem value set is open/non-exhaustive", and R14-COMMENT-ATTRIBUTION with "omarchybot's automated triage", each carrying a real ≤25-word quote.
That is exactly the r13 failure mode. The r13 gate showed 0→1 while MD:97 was false (spotcheck :143-153). A count shows that the corrections are present, not that they are true.
Offline, the gate also cannot show that a quote is a substring of its source, or that the quote supports the replacement's proposition.

## Source evidence I reopened (data only; I executed no commands from the comment)
- **S044** https://man.archlinux.org/man/systemd.exec.5 (.en.txt, § ProtectSystem=, footer 262.1): “Takes a boolean argument or the special values "full" or "strict".” (11 words).
  The same paragraph also says: implied by DynamicUser=, “cannot ensure protection in all cases”, “Defaults to off.”
  The r13 JSON `replaced_statements` entry for r12 MD:41-42 (JSON:120) already reads correctly: “the option set is not an exhaustive list of unit-side read-only mechanisms”. MD:97 is a lossy paraphrase of it. **MD and JSON diverge** (two authorities).
- **S045** comment 6071740243, read through `gh api`:
  - API fields: user.type User; association COLLABORATOR; `performed_via_github_app` null; created = updated = 2026-10-09T00:27:22Z, so the comment is unedited.
  - Body: 2955 bytes, sha256 `f9d55e89e92ee6279eb0504bf14fe228ef9c6a4010036cb09cf6642353948c34`.
  - Profile: name Omarchybot, bio null, created 2026-08-15. Nothing in the profile describes the account's own nature.
  - Body term sweep (lower-cased counts): model 0, generat 0, automat 0, claude 0, llm 0, codex 1, opinion 1, “i tried” 1. The single `bot` hit is inside a word (likely “both”), so it is not a self-label.
  - Quotes for a correction:
    - “I tried this on a stock Omarchy worker VM and could not reproduce the central claim” (16 words). This shows only that the comment *asserts* execution.
    - “Codex Medium reviewed the same evidence and upstream files and reached the same conclusion.” (14 words)
    - “It may have seen this analysis first, so its agreement is not guaranteed to be independent.” (16 words)
- **#6629 contrast** (6234472369): this comment does contain “This review is by Claude Opus 5.5 alone.” and “Nothing was run on a machine.”, so S043's model-review self-description has a basis.
  “automated triage” appears in neither comment. That is a residual stretch in S043. The outside verifier agreed with S043's rejection, so do not widen r14 to cover it. Just do not cite S043 wording as precedent.

## Counterexample to the shared interface: “maintainer deferral” is mis-scoped
The only maintainer sentence in #8047 is: “The remount failure is #6634, which is waiting on the maintainer to decide whether snapshot boots should keep the overlay.”
The comment's own disposition is: “This now waits on your answer.” — that is, on the reporter.
So any R14 or S045 text saying the comment defers *the #8047 issue or its conclusion* to a maintainer is new false provenance.
**Safe wording:** “reports that #6634's overlay decision awaits the maintainer; asks the reporter for diagnostics”.

## Overcorrection risks (wrong in the other direction; reject these)
- “The comment is human-authored”, “a VM test was performed”, or “omarchybot is not automated”. Generation method and authorship are **unknown**. The body's execution claim is unverified.
- “The domain is exactly no/yes/full/strict”. A boolean argument accepts several spellings (the r13 table already shows `yes`/`true`). Write “boolean, or the special values full/strict”. Do not enumerate a closed lexical list.
- “Codex Medium independently confirmed”. The body itself disclaims independence.

## r13 defects still active outside the two named loci (counterexamples to “only MD:97 and S042”)
1. `corpus/lessons/round-13.md:17`: “an **automated** `omarchybot` comment”. ActiveRefs' notice is planned “before historical self-description” (:68). A reader reaches :17 before that notice.
2. `corpus/lessons/round-13.md:68-70`: the collective “Bot comments are self-described model-generated triage”. This is the named locus.
3. `corpus/SOURCES.md:77` (old search log): “the text self-describes a model-generated review … so it is automated triage”. This covers #8047 collectively. SourceRegistry may not edit it, so S045 or the new search-log paragraph must name :77 explicitly.
4. `corpus/knowledge/root-dac-correction-r13.md:171` (QUALITY #18): “without treating **model triage** as maintainer acceptance”. This applies to S042 too. The planned r13 MD notice names only R14-VALUE-DOMAIN.
5. `corpus/QUALITY.md:24` (#18), “record bot comments as automated community triage”. This is superseded by L1's #20 in the worktree, which is fine. #19/#20 cite `lessons/round-14.md`, which does not exist yet; L1 must land it in the same commit.
6. r13 JSON `sources[0]` still has `status: reserved` and `registry_owner: SourceRegistry` (JSON:267-268), plus the oversized `gate_contract` (:204). An additive `r14_supersession` leaves these values readable as-is. The notice must name these exact JSON pointers.
7. `corpus/README.md:73` still routes to r13 as “Active … bot-authority limits”. Without an r14 row, the correction is dead text that no route reaches.

## Necessary evidence before any “semantic fix” wording (smallest safe correction)
- **Per-proposition agreement table** in the r14 MD and in the report, one row per replacement proposition. Columns: proposition; source object (URL plus comment id or § anchor); located quote; observation, assertion or inference; agree/disagree.
  Required propositions:
  - value domain = boolean/full/strict
  - non-exhaustive applies to mechanisms
  - API fields
  - VM execution asserted but unverified
  - second opinion, not independent
  - #6634 maintainer decision versus the reporter-directed wait
  - no self-description in this comment (with the bounded term sweep above)
  - host-cause rejection retained
  - no #6629 transfer
- **Pin the source identity** in the JSON so that a later reopen can detect drift:
  - S045: comment `updated_at` and body sha256.
  - S044: footer `systemd 262.1`, plus the host package version (261.2-1) marked as unmeasured for host runtime.
- **Gate content predicates, not presence alone:**
  - `VALUE_DOMAIN_OVERCLAIM`: matches `value (set|domain)…(not exhaustive|non-exhaustive|open)` in active r14 or unnoticed r13 text.
  - `DOMAIN_MISSING`: the replacement lacks boolean + full + strict.
  - `ATTRIBUTION_UNSUPPORTED`: `self-described|model-generated|automated` within the S045/6071740243/#8047 context.
  - `ATTRIBUTION_FIELDS_MISSING`: User, COLLABORATOR, unverified/asserted, second opinion.
  - `DEFERRAL_MISSCOPED`: “defers” + maintainer without #6634.
  - `NOTICE_ORDER`: the notice byte offset must precede each defect locus, including lesson :17, SOURCES :77 and MD:171.
  - `MD_JSON_DIVERGENCE`: the r14 MD and JSON replacements must carry the same proposition tokens.
  - `ROUTE_MISSING`: README, SKILL or PROVINCE has no r14 pointer.
- **Red-before must be defect-driven.** Count 0 at `8606bad` because the files are absent is trivially red. Require baseline findings to name the MD:97 and S042/:68/:77 phrases with stable IDs. Then add one-delta mutants: restore the old phrase inside an r14 replacement; delete a notice; move a notice after its locus; add “automated”. Each mutant must fail with its specific ID while the count declines.
- **Claim ceiling.** The gate is “bounded correction conformance”. Source agreement comes only from reopen evidence, and seats in the same wave are author-side. LOG, SCORECARD and the report must say “author-side source agreement; outside closure decides”. Depth ordinal stays 8.

## Impacted axes
- **depth:** at risk if the count is reported as repair.
- **calibration:** harmed if the report says “verified/fixed”, or if a reverse overclaim (human/VM-confirmed) lands.
- **adjacency:** neutral if no sibling or methodology ownership is claimed.
- **coverage/freshness/operability:** unchanged; pins do not add freshness credit.

## Limitations
- I executed no lane gate, census, test or selftest; the r14 artifacts did not yet exist.
- Network reads were the Arch man page and the GitHub API. Term counts are substring counts over the API body text.
- I did not open the local host man page. I did not read peer reports in depth.
- Only this file was written.
