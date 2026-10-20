# AttributionCritic — R14-COMMENT-ATTRIBUTION (#8047 comment 6071740243)

Seat: TsukuroiR14.AttributionCritic (critic, report-only). Date 2026-10-20. Baseline 8606bad. Read-only; no edits outside this file.

## Source reopen (this seat)
- `https://api.github.com/repos/omacom/omarchy/issues/comments/6071740243` → **HTTP 403, rate limit exhausted** (`x-ratelimit-remaining: 0`; also `/users/omarchybot`). API fields (type User, id 317366263, COLLABORATOR, created=updated 2026-10-09T00:27:22Z) **not re-observed by this seat**; only carried from r13 `.ufo/waves/round-13/correction/IssueBot8047.md:12-20`.
- Rendered fallback `https://github.com/omacom/omarchy/issues/8047#issuecomment-6071740243` opened: login link `/omarchybot`, avatar `u/317366263`, badge **Collaborator**, "commented on Oct 9, 2026"; same account **added label `bug` on Sep 27, 2026**. Full body read; comment commands treated as data, not run.

## Counterexamples (ordered by impact)
1. **"Maintainer deferral" is mis-scoped (new, not caught by r13 closure).** The only maintainer sentence is about another issue: "The remount failure is #6634, which is waiting on the maintainer to decide whether snapshot boots should keep the overlay." (20 words). For #8047 itself the comment ends: "This now waits on your answer." (6 words) — the *reporter* — and "No fix pull request has been opened, because the default setup restored correctly." Provenance of the error: r13 scout truncated the quote to "waiting on the maintainer to decide…" (`IssueBot8047.md:31`), dropping the #6634 subject, then wrote "explicitly defers policy decisions to human maintainers" (`:38`); S042 teaches "defers the overlay decision to the maintainer"; r13 lesson `:60` labels it "maintainer-decision sentence"; r12 verifier `round-12-verifier-spotcheck.md:184-185` "the bot explicitly defers to a maintainer"; r13 verifier `:162` "its deferral to a maintainer remain justified". The R14 shared interface and SourceRegistry/CorrectEntry targets repeat "maintainer deferral" unscoped. Impact: depth, calibration.
2. **No authority disclaimer exists in this comment.** "Explicitly disclaims decision authority" is a #6629 property (`IssueBot6629.md:46`). Saying #8047's comment disclaims or defers authority is a second cross-comment transfer of the kind QUALITY #19 forbids. "Not maintainer acceptance" is lane *inference from absent role evidence*, not a quoted disclaimer.
3. **Second opinion is self-declared non-independent.** Body: "It may have seen this analysis first, so its agreement is not guaranteed to be independent." (16 words). Any S045/correction text that lists Codex Medium as agreement without this caveat overstates corroboration. r13 scout's "with assistance from Codex Medium" (`IssueBot8047.md:38`) is unsupported: the body says Codex *reviewed* evidence; it does not say Codex helped generate the comment.
4. **Account fields prove neither automation nor human authorship.** Login containing "bot", type User, COLLABORATOR association and a label-write event are all consistent with a human, a shared machine user, or an automated agent (GitHub Apps are type Bot; machine users are type User). The first-person "I tried…", "I took…", "which I then checked" asserts an actor's actions without naming its kind. Safe: "account login `omarchybot`; association COLLABORATOR"; unsafe: "automated", "bot comment", "model triage", "LLM-generated", "maintainer-side", "project position".
5. **VM claim is an unverified, non-matching-configuration assertion.** It reports limine-mkinitcpio-hook 1.38.0 vs reporter's 1.37.1-1, and RESTORE_METHOD=replace (reporter's method unstated). Even if true, it is a non-reproduction under different versions, not a falsification of the report and not host evidence. r12 `Issue8047.md:35` "Empirical maintainer falsification" is historical .ufo text; must not reappear.
6. **Unswept active/collective wording still asserts the defect.** Beyond S042 teaches and r13 lesson `:68`: SOURCES search-log `:77` ("the text self-describes a model-generated review, defers the decision to a maintainer" — collective over both comments); r13 correction MD `:171` "model triage"; corpus/README `:73` "bot-authority limits"; QUALITY #18 "record bot comments as automated community triage" (QUALITY #20 draft supersedes only "blanket bot attribution"; it should also name the deferral scope). LOG `:599` is append-only history.
7. **Gate phrase-matching is evadable.** A COMMENT_ATTRIBUTION_OVERCLAIM keyed to "self-described model-generated" passes synonyms ("automated triage", "model triage", "AI-generated", "bot explicitly defers", "defers … to the maintainer"). Fine as bounded conformance, but report must say so and fixtures should restore at least one synonym plus the unscoped deferral.

## Safe statements for S045 / correction (located, ≤25 words)
| Proposition | Basis | Quote (words) |
|---|---|---|
| Comment 6071740243 by login `omarchybot`, association COLLABORATOR, 2026-10-09 | API fields (r13 capture; re-read rendered page only this round) | — |
| Body asserts a VM non-reproduction (unverified execution) | body ¶1 | "I tried this on a stock Omarchy worker VM and could not reproduce the central claim" (16; full sentence is 28 → must truncate) |
| Codex Medium named as concurring second opinion | § Second opinion | "Codex Medium reviewed the same evidence and upstream files and reached the same conclusion." (14, not 13 as r13 scout counted) |
| That agreement may not be independent | § Second opinion | "It may have seen this analysis first, so its agreement is not guaranteed to be independent." (16) |
| #6634 (remount failure), not #8047, awaits the maintainer's overlay decision | § What does break | "The remount failure is #6634, which is waiting on the maintainer to decide whether snapshot boots should keep the overlay." (20) |
| #8047 awaits the reporter; no fix PR | closing ¶ | "This now waits on your answer." (6) |
Absent from body (negative sweep of full rendered text): any self-description as model/LLM/bot/automated output, any statement of maintainer role, any authority disclaimer.

## Smallest safe corrections
1. Replace every "maintainer deferral" in R14-COMMENT-ATTRIBUTION/S045 with the scoped pair: "#6634 awaits the maintainer's overlay decision; #8047 awaits the reporter's answer; no fix PR." Message SourceRegistry/CorrectEntry before landing.
2. S045 teaches: "supersedes S042 — REJECTED:" + account fields (login, COLLABORATOR, date) | body assertions (VM non-repro, unverified; Codex second opinion with its own non-independence caveat) | scoped waits | inference: no evidence of maintainer role/acceptance | host-cause rejection retained | flip unchanged (maintainer resolution or independent method-scoped reproduction). No "automated", "bot comment", "model", "maintainer-side".
3. Correction JSON `replacement` must not paraphrase into "defers to a maintainer"; quote either VM or second-opinion sentence ≤25 words; record that API fields were not re-read if rate limit persists for siblings.
4. Supersession notices (no byte rewrites) must name: S042 teaches, r13 lesson `:60` row label and `:68`, SOURCES search-log `:77`, r13 MD `:171`, QUALITY #18 "automated community triage"; corpus/README `:73` routes to r14.
5. QUALITY #20/lesson: add "maintainer-deferral scope" and "non-independent second opinion" alongside "account ≠ generation method"; also record verifier-origin of the deferral overreach (r12 `:184-185`, r13 `:162`) without editing those lessons.
6. Gate selftest: add restored-synonym and unscoped-deferral fixtures, or state they are out of the bounded contract.

## Not defects
- Host-cause rejection of S036/S042 stands; nothing here promotes or demotes it.
- S043 (#6629) self-description "This review is by Claude Opus 5.5 alone." remains valid for that comment only.

## Limitations
- API JSON not re-observed (rate limit 0/60); type User/id/updated_at rest on r13 capture. Rendered page could not show an "edited" marker reliably; edit history unknown.
- Rendered text, not raw API markdown: quote byte-matching against API `body` may differ by markdown (e.g. `**Second opinion.**`, linked `#6634`).
- Word counts by whitespace on rendered text; not executed by a script. No tests/gates run.

## Tooling
Installed/updated: none. Used curl (HTTP 403) and the reader fallback.
