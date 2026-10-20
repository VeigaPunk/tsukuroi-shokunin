source: S044 (docs/A row, corpus/SOURCES.md:50, ProtectSystem= value domain) — https://man.archlinux.org/man/systemd.exec.5; S045 (community/C row, corpus/SOURCES.md:51, #8047 comment authority) — https://api.github.com/repos/omacom/omarchy/issues/comments/6071740243; prior rows S041/S042/S043 at corpus/SOURCES.md:47-49; baseline r13 MD:97,171 and JSON replaced_b2_claims[0], sources[0], gate_contract; baseline corpus/lessons/round-13.md:60,68-70; corpus/lessons/round-13-verifier-spotcheck.md:143-165,175-186; corpus/QUALITY.md criteria 19-20.
verified-at: 2026-10-20 (both primary URLs reopened: systemd.exec.5 footer systemd 262.1; authenticated `gh api` returned the #8047 comment JSON with HTTP 200, canonical HTML comment anchor corroborated login, Collaborator badge, creation date and body. Unauthenticated api.github.com returned HTTP 403 rate-limit for this host earlier the same day. Source snapshots `.ufo/waves/round-14/repair/QuoteReview-source.json` and `ClaimSeparation-source.json` were read. No source-supplied command was executed, and no host probe, service start, snapper call or package transaction was made.)
recheck: on-release for S044 (re-read § ProtectSystem= on a systemd.exec(5) revision change); 90d for S045 (re-read the comment object and API fields); procedure: reopen the two URLs, re-count whitespace words in each quote, and compare `user.login`, `user.type`, `author_association`, `created_at` and the body fragments recorded here; no host mutation.

# Source-scope corrections (round 14)

All original r13 path:line citations below locate immutable baseline
`8606bad4cbc6451ac2890c9f8e2548a36c386db6`; read them with
`git show <baseline>:<path>`. Notices shift working-tree line numbers.
Active locators are the named heading, source-row ID or JSON key; the
independent verifier lesson itself is unchanged.

## Supersession and preserved history

This pair adds two named corrections while preserving historical r13 text,
source rows and lessons. Explicit notices in the old MD/JSON, r13 lesson and
SOURCES Search log route the affected propositions here; S045 supersedes
immutable S042. S044/S045 are present at `corpus/SOURCES.md:50-51`.
The named round14 LOG entries and SCORECARD record the integration; source
comparison and executable measurement remain separate evidence.

- **R14-VALUE-DOMAIN** supersedes one clause only: `corpus/knowledge/root-dac-correction-r13.md:97`, the replacement row for r12 MD:41-42, ending “the value set is not exhaustive”. It also supplies the scoped reading for the ambiguous saved phrase at `root-dac-correction-r13.json:120` (“the option set is not an exhaustive list of unit-side read-only mechanisms”). The rest of R13-DAC-EXCLUSIVITY stands.
- **R14-COMMENT-ATTRIBUTION** supersedes S042's teaching for #8047 only: `corpus/SOURCES.md:48` (S042's attribution claim, superseded here), the S042 located-quote referent at `corpus/lessons/round-13.md:60`, the collective sentence at `round-13.md:68-70`, the collective attribution at `SOURCES.md:77`, and the “model triage” clause at `root-dac-correction-r13.md:171` (QUALITY criterion 18). S042 fields are not rewritten. S043/#6629 is a different comment and is not reclassified or transferred.

The old r13 gate `tools/check-root-dac-correction.py` remains the historical,
narrow checker. The round-14 bounded checker
`tools/check-source-scope-correction.py` is present; this seat read its
predicates but did not execute it, so this pair asserts no passing gate and no
source-truth enforcement. A structural pass cannot establish source agreement.

## R14-VALUE-DOMAIN

Source object: S044, `systemd.exec(5)` § ProtectSystem= (under SANDBOXING),
rendered lines 1266-1267, page footer systemd 262.1, opened 2026-10-20.
Located quote, **11 whitespace words**, exact after joining the rendered line
break with one space:

> Takes a boolean argument or the special values "full" or "strict".

**Proposition supported:** the documented input forms for this option are a
boolean argument and the special values `full` and `strict`. The opened
revision documents no further values for `ProtectSystem=`.

**Superseded text:** `root-dac-correction-r13.md:97` says “among
`ProtectSystem=` values, `strict` is the only value that covers the hierarchy
(S041); the value set is not exhaustive” — this tail is superseded. The first
clause is a comparison of
the documented values; the tail misplaces non-exhaustiveness onto the option's
value set.

**Replacement:** “The opened revision documents `ProtectSystem=` as taking a
boolean argument or the special values `full` and `strict`, and documents no
further values for this option. The other-mechanism examples
(`BindReadOnlyPaths=`, `TemporaryFileSystem=` with `ro`,
`RootDirectory=`/`RootImage=`) are illustrative, not exhaustive (they are not an
exhaustive survey); that non-exhaustiveness is lane scope **[inference]**, not a
source statement about the option's values and not a claim about undocumented
values. `full` adds `/etc/` to the mounts made read-only by true; `strict`
covers the hierarchy except `/dev/`, `/proc/` and `/sys/` with documented
exclusions.”

The illustrative other-mechanism list in § Retained alternate mechanisms is
lane scope, not a source claim that other `ProtectSystem=` values exist. The
ambiguous saved sentence at `root-dac-correction-r13.json:120` — “the option
set is not an exhaustive list of unit-side read-only mechanisms” — is read the
same way: the example list is illustrative, not exhaustive, and the phrase is
not a source statement about undocumented option values. That phrase is not
rewritten.

The r13 table's `no`/`yes`/`true` entries are mode examples for a boolean
argument, not an exhaustive lexical spelling list. This pair adds no parser or
code-level boolean facts, and value names remain option-scoped. No host
runtime state, mount namespace or cause is measured or claimed here.

## R14-COMMENT-ATTRIBUTION

Source object: S045, comment `6071740243` on omarchy issue #8047. Created
2026-10-09T00:27:22Z; API and canonical HTML read 2026-10-20. Located quote,
**16 whitespace words**, exact substring of the JSON `body`:

> I tried this on a stock Omarchy worker VM and could not reproduce the central claim

**Verified account fields (observations, not authority):**

| field | observed | basis |
|---|---|---|
| comment id | 6071740243 | REST `id`; HTML anchor |
| user.login | `omarchybot` | REST `.user.login`; HTML |
| user.type | `User` (not API type `Bot`) | REST `.user.type` |
| author_association | `COLLABORATOR` | REST; HTML badge |
| created_at / updated_at | 2026-10-09T00:27:22Z | REST |
| issue state | open, label `bug` | HTML; prior S042 |

**Body claims, kept separate from those fields:**

| label | exact fragment | words | reading |
|---|---|---|---|
| VM assertion | I tried this on a stock Omarchy worker VM and could not reproduce the central claim | 16 | unverified first-person assertion; this lane has not independently reproduced the claimed run |
| Second opinion | Codex Medium reviewed the same evidence and upstream files and reached the same conclusion. | 14 | labelled a second opinion; the comment does not establish that Codex helped write it |
| Independence caveat | It may have seen this analysis first, so its agreement is not guaranteed to be independent. | 16 | the author's own limitation |
| #6634 deferral | waiting on the maintainer to decide whether snapshot boots should keep the overlay. | 13 | the sentence's subject is the #6634 remount failure, not #8047 |
| #8047 closing | This now waits on your answer. | 6 | reporter-directed; #8047 awaits the reporter's answer, not a maintainer decision |

The maintainer-decision sentence inside the #8047 comment is about
**#6634's remount failure**; #8047's own closing waits for the reporter.

Reading the account fields as maintainer acceptance is unsupported
**[inference]**: login, API type and association are identity metadata, not a
maintainer decision. `type: User` is not API type `Bot`, but neither field is
evidence of human authorship, model generation, or who composed the text.

**Bounded negative claim:** this comment makes no generation-method claim about
itself. Performed 2026-10-20 over the exact HTTP 200 `body`; the JSON
`body_term_sweep` records the term list and the zero counts. The attribution
wording preserved in S042 and the r13 lesson does not appear in the source.
#6629's “Nothing was run on a machine.” belongs to comment `6234472369`, and
S043 remains its own row; it is not transferred to #8047.

**Replacement:** the replacement string in
`corpus/knowledge/source-scope-correction-r14.json` (`R14-COMMENT-ATTRIBUTION`)
states the verified fields, the unverified VM assertion, the second opinion and
its non-independence caveat, the #6634-scoped maintainer sentence, the #8047
reporter wait, and the rejection of host-cause and maintainer-acceptance use.
Host cause remains unknown. No new capability or host remediation is claimed.

**Referent errors covered (supporting pointers, not new claims):**

| pointer | preserved statement (paraphrase) | corrected referent |
|---|---|---|
| `corpus/SOURCES.md:48` | S042 teaches that the sole #8047 comment carries the now-superseded attribution | no such attribution appears; account fields are not acceptance |
| `corpus/lessons/round-13.md:60` | S042 row calls the quoted sentence a “maintainer-decision sentence” | the quoted sentence refers to #6634; #8047 ends awaiting the reporter |
| `corpus/lessons/round-13.md:68-70` | collective sentence attributing automated triage to both bot comments | not true of #8047 as stated; S043/#6629 has its own text and is untouched |
| `corpus/SOURCES.md:77` | Search-log attributes a model-generated review to the text, a maintainer decision and a nothing-ran statement | those disclaimer attributes fit #6629, not #8047, which asserts VM execution |
| `corpus/knowledge/root-dac-correction-r13.md:171` | QUALITY 18 says S042/S043 supersede bot wording “without treating model triage as maintainer acceptance” | #8047 is not established as model triage; criterion 20 governs this comment |

## R14-S041-METADATA

`corpus/knowledge/root-dac-correction-r13.json:267-268` records
`sources[0].status: "reserved"` and `sources[0].registry_owner:
"SourceRegistry"` for S041. That metadata is stale. `corpus/SOURCES.md:47`
records S041 as docs, tier A, status **mined**, and
`root-dac-correction-r13.md:175` says “S041 is a mined registry row, not a
reserved future source.” There is no live owner reservation. The r13 JSON
bytes are historical and are not edited; read the field as draft metadata only.
This is a metadata repair, not a new measured correction, status change or
capability claim.

## R14-GATE-CONTRACT

`root-dac-correction-r13.json:204-240` declares a `gate_contract` object with
ten `required_md_headings`, a `corrected_field_scan`, a historical revision and
files, an active-supersession map, and a marker rule. That object is
documentation, not an executable specification. The actual checker
`tools/check-root-dac-correction.py`:

- checks **five** headings in `md13_issues` (lines 100-105): the title,
  § Corrected claim, § Retained alternate mechanisms, § Historical cause
  remains unknown and § QUALITY check;
- checks identifier/scope pins, regular expressions, S041 presence and a
  two-table minimum, but has **no** `gate_contract` reference (grep on the tool
  returned no match on 2026-10-20);
- has no predicate for the `ProtectSystem=` value domain or the S042
  attribution, so its exit 0 could not detect MD:97 or S042.

The tool predicates, not the JSON description, are the authoritative narrow
contract. No stronger enforcement is claimed. The round-14 bounded checker is
present; this seat read its predicates but did not execute it, so this pair
does not assert its red-fixture or green result.

## QUALITY check

Performed on the bytes above at authoring, 2026-10-20. It is an author-side
check, not independent verification or self-admission.

| # | Criterion | Evaluation |
|---|---|---|
| 1 | Falsifiable | Each replacement is bounded to one located quote and one proposition; host cause stays unknown. |
| 2 | Measured anchor | S044 URL, section, rendered lines and footer; S045 comment id, fields, timestamps and body fragments. |
| 3 | Observation / inference / unknown | API fields and body text are observations; VM execution is an unverified assertion; account authority is marked inference; host cause is unknown. |
| 4 | Append-only | No old file is edited; old clauses remain; supersession pointers and L1 append sites are named. |
| 5 | Rejection kept | S042/S043 and #8047 host-cause rejections remain; only the attribution basis changes. |
| 6 | Pacman advice | Not applicable; no package command appears. |
| 7 | S### citation | S044 is present at `corpus/SOURCES.md:50` (docs, tier A) and S045 at `:51` (community, tier C), with S045's teaches beginning “supersedes S042”. This seat did not write or validate those rows. |
| 8 | Unknown sweep | Both primary URLs reopened; exact body swept; frontmatter date and cadence present. |
| 9 | Negative claims bounded | Self-description absence bounded to the exact body and term list, 2026-10-20. |
| 10 | Mention sweep / tables | L1's final bounded sweep is recorded in `.ufo/waves/round-14/repair/verification.json`: original loci remain historical under named notices; active routes lead here. Tables are checked separately. |
| 11 | LOG entry | LOG.md contains named round14 entries for both corrections, the supporting metadata errata, the recurring-class criterion and source-reading evidence. |
| 12 | Absent tool | `gh`, `curl`, `jq` and the man-page fetch were available; no absent tool supports a claim. |
| 13 | EACCES triage | Unaffected; no new triage field, mode or cause claim. |
| 14 | Performed, not promised | This section evaluates the preceding content; pointers resolve to the two URLs, rows and files named above. |
| 15 | Root metadata / denial | No new mode or writability universal; DAC, namespace and credential classes remain separate. |
| 16 | Policy sources | Not applicable; no health grade, drift finding or repair advice. |
| 17 | Exhaustive claims | Scoped to the opened revision; other-mechanism examples are marked illustrative lane scope, not a documented option domain. |
| 18 | Bot attribution | Superseded in part by criterion 20 for #8047; the fixture-identity rule is unchanged. |
| 19 | Claim/source scope | Quote/proposition pairs are present. This seat read the bounded R14 checker's predicates but did not execute it, so no red-fixture or green result is claimed; this pair does not self-admit. |
| 20 | Comment ID and fields | Exact comment ID; verified fields separated from body claims; #8047 is not called model triage; host-cause rejection retained. |

## Sources

- **S044 — docs, tier A, mined (assigned row).** `systemd.exec(5)` § ProtectSystem=, https://man.archlinux.org/man/systemd.exec.5, footer systemd 262.1, opened 2026-10-20. Quote: “Takes a boolean argument or the special values "full" or "strict".” Scope: documented value domain only; not host runtime.
- **S045 — community, tier C, rejected (assigned row).** Comment `6071740243`, https://api.github.com/repos/omacom/omarchy/issues/comments/6071740243, created 2026-10-09T00:27:22Z, read 2026-10-20. Quote: “I tried this on a stock Omarchy worker VM and could not reproduce the central claim”. Scope: correction of S042's teaching; host cause remains unestablished.
- **S041/S042/S043 — prior rows.** `corpus/SOURCES.md:47-49`; S041 is mined and unchanged; S042's fields and rejection are preserved with this teaching superseded; S043/#6629 is separate and not transferred.
- **Historical pair and lessons.** `corpus/knowledge/root-dac-correction-r13.md:97,171`, `.json:204-240,267-268`; `corpus/lessons/round-13.md:60,68-70`; `corpus/lessons/round-13-verifier-spotcheck.md:143-165,175-186`.
- **Retained snapshots.** `.ufo/waves/round-14/repair/QuoteReview-source.json` and `ClaimSeparation-source.json` (body text, account fields, 403 observation; data only, no commands executed).
- **QUALITY.** `corpus/QUALITY.md` criteria 19-20, alongside the applicable numbered criteria evaluated above.

## R15 supersession (2026-10-20) — locator and positive-domain notices

Appended in round 15, after the independent verifier routed two
documentation debts in
`corpus/lessons/round-14-verifier-spotcheck.md` § Adjudicated concerns items
1–2. These notices supersede only those supplemental documentation defects.
The R14 quote, proposition, attribution correction and every historical byte
above stand unchanged; this section is additive. Canonical pair:
`corpus/knowledge/source-locator-clarification-r15.md` / `.json`, schema
`tsukuroi-locator-clarification-v1`, corrections `R15-LOCATOR` and
`R15-POSITIVE-DOMAIN`. The round-14 bounded checker
`tools/check-source-scope-correction.py` keeps its own predicates and is not
widened by this section.

- **R15-LOCATOR** supersedes one supplemental locator only: the bare,
  renderer-unqualified string “rendered lines 1266-1267” in § R14-VALUE-DOMAIN
  above (source-object sentence), at
  `source-scope-correction-r14.json` `corrections[0].location`, and in
  `sources[0].anchor` (S044: “§ ProtectSystem= (SANDBOXING), rendered lines
  1266-1267; footer systemd 262.1”). It is
  withdrawn as an active locator because rendered line numbers depend on the
  reader: the round-14 closure's reader shows AF_UNIX at those lines and
  `ProtectSystem=` at 1270, with the definition at 1272–1273 (verifier lesson
  § Adjudicated concerns and routing, item 1, `:233-239`). The active locator is the stable section path **SANDBOXING >
  ProtectSystem=** plus the observed page footer version (**systemd 262.1** at
  the 2026-10-20 reopen). The 11-word quote and every other field remain exact
  and are not superseded. A future line number is only usable when the
  renderer or reader is named alongside it; bare lines are not a locator.
- **R15-POSITIVE-DOMAIN** supersedes one negative documentation sentence
  only: the unswept absence claim “documents no further values for this
  option” / “The opened revision documents no further values for
  `ProtectSystem=`” in § R14-VALUE-DOMAIN (proposition and replacement) and in
  `corrections[0].replacement`. No command-and-date documentation sweep backs
  an exhaustive-absence claim, and this lane does not claim parser proof. The
  positive definition — “Takes a boolean argument or the special values
  "full" or "strict".” — stands unchanged, as do `full`/`strict` coverage and
  the illustrative other-mechanism list's lane-scope status. R15 records only
  that documented input form; it makes no statement about undocumented values.

Both notices are documentation corrections on the existing rollback-net
surface. They add no capability, repair no host, and license no package or
service action.
