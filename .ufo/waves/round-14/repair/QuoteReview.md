# QuoteReview — round 14 (TsukuroiR14.QuoteReview, depth)

Scope: reopen shared sources; check proposed substrings (<=25 whitespace words), location, version and account facts; flag semantics broader than the quote. Report only. Reopened 2026-10-20.

## 0. Artifact status
- `corpus/knowledge/source-scope-correction-r14.md` and `.json` do NOT exist yet (glob empty). No drafted quotation list was available, so the table below checks the candidate substrings implied by the assignment, `SOURCES.md` S041–S043 and the round-13 lesson. Re-check once the drafts land.

## 1. S044 — systemd.exec(5) ProtectSystem= (https://man.archlinux.org/man/systemd.exec.5)
Reopened native HTML; footer `systemd 262.1` confirmed. Paragraph at page lines 1271–1287 (whitespace normalized).

| # | Exact substring | Words | Result |
|---|---|---|---|
| S044-A | `Takes a boolean argument or the special values "full" or "strict".` | 11 | Verbatim (line-wrapped in source). **The brief's paraphrase "boolean argument or special values full or strict" is not a quotation**: it drops "Takes a", "the" and the quote marks. Do not quote that form. |
| S044-B | `If set to "strict" the entire file system hierarchy is mounted read-only, except for the API file system subtrees /dev/, /proc/ and /sys/` | 23 | Verbatim. |
| S044-C | `If set to "full", the /etc/ directory is mounted read-only, too.` | 11 | Verbatim. |
| S044-D | `This setting cannot ensure protection in all cases.` | 8 | Verbatim (line 1286). This is the source's own limitation sentence; it concerns protection, not the value domain. |
| S044-E | "non-exhaustive" / "not exhaustive" | — | **Absent.** Artifact grep for `exhaust` returns no hit in the ProtectSystem paragraph or anywhere in systemd.exec(5) text fetched. |

Semantics broader than the quote (flags):
- **F1 (blocking for any value-domain sentence):** the claim "non-exhaustive applies to unit-side mechanisms, not documented option domain" has no source support. The source says nothing about exhaustiveness. A closed reading of the option domain comes only from grammar ("Takes a boolean argument or the special values …"), and that same construction appears for ProtectHome= (`"read-only" or "tmpfs"`), PrivateUsers=, PrivateTmp= and others, which shows it is a documentation style, not a closure statement. Mark any "closed domain" statement as `[inference]` from the grammar.
- **F2:** "full … does not cover /" (S041 teaching) is inferred from the list `/usr/`, `/boot`, `/efi`, `/etc/`. Quote the list or tag `[inference]`.
- **F3:** the MD:97 sentence "the value set is not exhaustive" (active, r13 correction) remains unsupported by S044-A/S044-D. The R14 correction must supersede it by name; it must not be re-quoted as source.

## 2. S045 — omarchy #8047 comment 6071740243 (https://github.com/omacom/omarchy/issues/8047#issuecomment-6071740243)
Body read through the authenticated `gh api` path (see §5). Body is 425 words; the GitHub HTML page shows the same text.

| # | Exact substring | Words | Result |
|---|---|---|---|
| S045-A | `I tried this on a stock Omarchy worker VM` | 9 | Verbatim. This is the body's execution assertion; it is unverified from outside. |
| S045-B | `could not reproduce the central claim` | 6 | Verbatim. |
| S045-C | `Codex Medium reviewed the same evidence and upstream files and reached the same conclusion.` | 14 | Verbatim. |
| S045-D | `It may have seen this analysis first, so its agreement is not guaranteed to be independent.` | 16 | Verbatim. Mandatory companion to S045-C. |
| S045-E | `This now waits on your answer.` | 6 | Verbatim. The deferral is addressed to the reporter, not to a maintainer. |
| S045-F | `which is waiting on the maintainer to decide whether snapshot boots should keep the overlay.` | 15 | Verbatim, but its referent is **#6634** (sentence begins "The remount failure is #6634, …"). It is not #8047's deferral. |
| S045-G | "model", "Claude", "generated", "triage" | — | **0 hits** in the body. The body does not self-describe as model-generated automated triage. |

Semantics broader than the quote (flags):
- **F4:** "maintainer deferral" for #8047 is not in the body. Only S045-F exists, and it is about #6634. The #8047 deferral is S045-E, to the reporter.
- **F5:** "second opinion" must not become "independent second opinion" — the body disclaims independence (S045-D).
- **F6:** "unverified VM-execution assertion" is the analyst's characterization; quote S045-A and tag the characterization `[inference]`.
- **F7:** round-13 `S042` quoting S045-F as "the maintainer-decision sentence" for #8047 is a referent error in the superseded row and lesson. A superseding row must name #6634.

## 3. Account and location facts (verified 2026-10-20)
- Comment id `6071740243`, issue `#8047` (`issue_url .../issues/8047`), `created_at 2026-10-09T00:27:22Z`: **verified** via `gh api`; HTML shows "commented on Oct 9, 2026" (day matches).
- Issue #8047: `state open`, `labels [bug]`, `updated_at 2026-10-09T00:27:22Z`, `comments 1`; the comment list has exactly one entry (the sole-comment claim in S042 holds).
- `user.login omarchybot`, `user.type User`, `author_association COLLABORATOR`: **verified** via `gh api`. Unauthenticated `api.github.com` returned **HTTP 403** from this seat, so the earlier "GitHub API read" cannot be reproduced without auth.
- HTML badge text "Collaborator" corroborates the association label [inference from GitHub display]. HTML shows no bot label; the API type `User` is the authoritative field.
- The `User` type establishes account type only. It does not establish generation method, maintainer status or acceptance (S042 wording already says so; keep it).
- Comment id `6234472369` (#6629, for S043): login `omarchybot`, type `User`, COLLABORATOR, created `2026-10-17T13:31:32Z` — matches S043 row. Sample quotes verbatim: `Nothing was run on a machine.` (6 words) and `This review is by Claude Opus 5.5 alone.` (8 words). Unlike #8047, the #6629 body **does** self-describe as a model review, so S043's attribution is supported and S042's copy of the same wording is not.
- Version facts: `systemd 262.1` footer (page line 4327) confirmed. The #8047 body cites limine-snapper-sync 1.31.0-1 and limine-mkinitcpio-hook 1.37.1-1; the comment cites limine-mkinitcpio-hook 1.38.0. Do not cite either as a single version without naming its source.

## 4. Recommendations (concrete)
1. S044 replacement: quote S044-A exactly (with quote marks, with "the"). If the point is limitation, quote S044-D. State any closed-domain reading as `[inference]` from the grammar. Remove "non-exhaustive" from the S044 proposition entirely.
2. S044 teaching: quote S044-C for `full`; do not write "does not cover /" without `[inference]`.
3. S045: quote S045-A, S045-B and S045-C together with S045-D. Do not write "independent".
4. S045 deferral: quote S045-E for the reporter-addressed wait. If a maintainer deferral is kept, quote S045-F and name #6634 as its referent.
5. S042 supersession: name the account fields (login, type `User`, COLLABORATOR, comment id, created time) as verified 2026-10-20 via authenticated `gh api`. State that the body has no model self-description (S045-G). Do not copy the #6629 disclaimer.
6. Record the read method for every GitHub fact: unauthenticated API returns 403; use `gh api` (authenticated).
7. Retain the host-cause rejection as written in S042; this review does not change it.

## 5. Limitations
- The R14 draft files are absent; checks cover candidate substrings only.
- `api.github.com` unauthenticated: HTTP 403. The account facts come from `gh api` (authenticated read, token account VeigaPunk); no write made.
- The systemd man page was read as native HTML; word counts are whitespace-normalized (line wraps joined; markdown asterisks ignored).
- Did not run any verification command, build, test or lint.

## 6. Tooling record
- Installed: none. Updated: none.
- Used: `gh` 2.102.0 at `/home/vgpnk/.local/bin/gh` (pre-existing), read-only `gh api` calls only. No GitHub mutations.
- Scratch files created during the check in `/tmp` were removed.
