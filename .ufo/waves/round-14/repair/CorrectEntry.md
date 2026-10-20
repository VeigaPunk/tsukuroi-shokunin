# CorrectEntry — round-14 source-scope pair

## Files written (only these)
- `corpus/knowledge/source-scope-correction-r14.md`
- `corpus/knowledge/source-scope-correction-r14.json`
- `.ufo/waves/round-14/repair/CorrectEntry.md` (this report; relative to repo root)
No old file, LOG, SCORECARD, QUALITY, lesson, SOURCES row, MANIFEST or routing was edited.

## Behavior
New active pair with schema `tsukuroi-source-scope-correction-v1`; `corrections`
has exactly two objects (id, supersedes, source_id, url, location, quote,
replacement). MD opens `source:`/`verified-at:`/`recheck:` and has named
`## R14-VALUE-DOMAIN`, `## R14-COMMENT-ATTRIBUTION`, `## R14-S041-METADATA`,
`## R14-GATE-CONTRACT` and `## QUALITY check`.

- **R14-VALUE-DOMAIN** supersedes `corpus/knowledge/root-dac-correction-r13.md:97`
  (“the value set is not exhaustive”). Quote: `Takes a boolean argument or the
  special values "full" or "strict".` (11 whitespace words; § ProtectSystem=,
  rendered 1266-1267, footer systemd 262.1, opened 2026-10-20). Replacement
  marks the other-mechanism examples as illustrative lane scope [inference],
  not a source statement about the option's values and not a claim about
  undocumented values. It also supplies the scoped reading for the ambiguous
  saved phrase at `root-dac-correction-r13.json:120`; old bytes are not
  rewritten. Short clarification: the r13 table's no/yes/true rows are mode
  examples, not an exhaustive lexical boolean spelling list; no parser/code
  facts added.
- **R14-COMMENT-ATTRIBUTION** supersedes S042 teaching for #8047 only. Quote:
  `I tried this on a stock Omarchy worker VM and could not reproduce the central
  claim` (16 words; comment 6071740243, created 2026-10-09T00:27:22Z). Verified
  fields are separated from body claims: login omarchybot, type User,
  association COLLABORATOR. The VM execution is an unverified assertion; Codex
  Medium is a second opinion that may not be independent and is not shown to
  have helped write the comment. The maintainer sentence is scoped to #6634;
  #8047 ends “This now waits on your answer.” Host-cause and
  maintainer-acceptance use rejected; host cause unknown. No generation-method
  self-description appears (bounded body sweep, 0 hits for model-generated /
  automated triage / self-described / generated / triage / model / LLM /
  agent). #6629's disclaimer is not transferred.
- Covered preserved referents: `SOURCES.md:48` (S042 teaches),
  `lessons/round-13.md:60` (S042 “maintainer-decision sentence”),
  `lessons/round-13.md:68-70` (collective bot sentence),
  `SOURCES.md:77` (Search-log collective attribution), and
  `root-dac-correction-r13.md:171` (QUALITY 18 “model triage” clause).
- **R14-S041-METADATA** erratum: r13 JSON `sources[0]` says status reserved and
  registry_owner SourceRegistry, while `SOURCES.md:47` says mined and
  `root-dac-correction-r13.md:175` says “a mined registry row, not a reserved
  future source”. Stale draft metadata; no live reservation.
- **R14-GATE-CONTRACT** erratum: r13 JSON `gate_contract` (204-240) documents
  ten headings, but `tools/check-root-dac-correction.py:100-105` checks five and
  has no `gate_contract` reference (grep: no match). Tool predicates are the
  authoritative narrow contract; no stronger enforcement claimed.

## Exact retained evidence
- systemd.exec(5) reopened; quote exact after joining the rendered line break
  with one space. Unauthenticated api.github.com returned HTTP 403 rate-limit
  earlier the same day; authenticated `gh api` returned HTTP 200 for the comment.
  Canonical HTML corroborated login, Collaborator badge, creation date and body.
- Retained wave snapshots read: `.ufo/waves/round-14/repair/QuoteReview-source.json`,
  `ClaimSeparation-source.json`. JSON `body_term_sweep` records the zero-count
  term list for the bounded attribution sweep.
- Both quote word counts are within the ≤25-word bound; replacement strings are
  in the JSON. No host property, namespace or cause was measured.

## Risks / integration status
- S044/S045 rows are present at `corpus/SOURCES.md:50-51`; S045's teaches
  begins “supersedes S042”. This seat did not write or validate those rows.
- The append-only routing (r13 MD/JSON, round-13 lesson, SKILL, PROVINCE,
  corpus README, snapper note) is present; notices were read at r13 MD:5-27,
  lesson:17,66 and SOURCES:83. This seat did not author them and makes no claim
  about their final content.
- `tools/check-source-scope-correction.py` is present; this seat read its
  predicates but did not execute it. No gate, red-fixture or green result is
  asserted; criterion 19 remains unverified here. The old r13 checker was read
  statically, not executed; it has no predicate for either defect and cannot
  establish source agreement.
## Tooling record
None installed or updated. Used pre-existing `gh`, `curl`, `jq`, `python3`;
no package transaction, privileged probe, service start, snapper call or
external command execution. No build/test/lint/formatter/verification command
was run, per contract; L1 verifies after all seats land.
