# RedBeforeCritic — one-delta red-before for claim-exceeds-source (report only)

Seat TsukuroiR14.RedBeforeCritic, axis depth. Read-only; I ran no gate, selftest, census or test.
Evidence: committed blobs at baseline `8606bad4cbc6451ac2890c9f8e2548a36c386db6` (= HEAD), plus the in-flight,
uncommitted `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-source-scope-correction.py` and
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/source-scope-correction-r14.json` as read on
2026-10-20 (line numbers can drift). Probes P1–P5 ran my own copies of the checker's regexes on the baseline blobs.

## Counterexamples (ordered by impact)
1. **The counter is absence-only.** `count = len(by_id)` counts JSON objects with valid IDs, and `emit` prints it even on
   FAIL. The selftest oracle requires count **2** for `missing-notice`, `restored-domain` and `restored-attribution`,
   all of which FAIL. So "0→2" (`corpus/lessons/round-14.md:7`) comes from creating the file, even with both defects
   active or restored. r13 had the same shape: its red included `R13-*-MISSING`, and its gate passed with MD:97 active.
2. **Bare tokens satisfy the dead-text notice check.** P1: the baseline lesson meets every `lesson_notice_ok` conjunct
   except the IDs. The defect sentence itself (`round-13.md:68`, "…self-described model-generated triage…, not API type
   Bot…") meets the "negated self-description" requirement. So appending `R14-COMMENT-ATTRIBUTION S045` anywhere
   silences `COMMENT_ATTRIBUTION_OVERCLAIM`. `md13_notice_ok` needs three tokens anywhere (ID, `root-dac-correction-r13.md`,
   `97`) and has no position rule: a notice after `## Sources` (line 180) passes, unseen by a reader of line 97.
3. **Rewriting history in place passes.** `VALUE_DOMAIN_OVERCLAIM = value_bad and not vnotice`: delete the phrase at MD:97
   (or lesson :68), add a notice, get PASS. `R14-HISTORY-MISSING` fires only for a missing file; only S042 is pinned.
4. **The restored-defect detector misses the real historical wording.** P2: `attr_restored` is False on the real S042
   teaches and the real lesson :68 sentence, because "not" falls inside the negation window. The selftest mutant
   passes only because its fixture is a bare sentence with that context removed.
5. **The S045 row check accepts a copy of the defect.** P3: `"supersedes S042 — REJECTED: " +` S042's original teaches
   passes `R14-SOURCES-SUPERSESSION`. The check *requires* the stem `self-describ` and never scans S045 for RESTORED.
   Like r13's unscoped `nonexhaustive` pin, a positive pin rewards the defect's vocabulary.
6. **The site set is incomplete.** P4 attribution sites: SOURCES :48 (S042) and :77 (collective over both comments);
   lesson :17 ("an automated `omarchybot` comment") and :68; r13 MD :171 ("model triage", S042/S043). The checker scans
   only S042 teaches and the whole lesson, so :77 and :171 can never be red or shown repaired. Exclude SOURCES :49
   (S043): its self-description is real.
7. **The passing fixtures encode new false provenance.** `MD14`, `JSON14` and `S045_ROW` say the comment "defers to a/the
   maintainer", and `attr_rep_missing` requires that wording. The body's maintainer sentence concerns **#6634**, and #8047
   ends "This now waits on your answer." (`AttributionCritic.md:10`, `QuoteReview.md:33-34`). The landed JSON
   replacement scopes this correctly; the gate pins the wrong proposition.
8. **The line-number pointer goes stale.** `supersedes: "…r13.md:97"` + a `\b97\b` pin: a top notice (ReportConformance
   proposes one after lines 1–3) moves the phrase off line 97 at the fixed revision, yet the pointer still passes.
9. **Two inputs change between red and green.** r13 measured red with gate `44677cc` and green with `c35d356`, after
   changing the gate code. Tree mode (no `--revision`) reads the worktree, not committed input.
10. **Domain regex gaps (tradeoff).** `DOMAIN_BAD` misses paraphrases ("value domain is non-exhaustive"), and r14 MD lines
    containing "replac" are exempt. P5: unscoped `not exhaustive|non-exhaustive` also hits eight legitimate
    mechanism-scoped r13 lines (e.g. JSON :120, :157), so do not widen to that.

## Smallest safe correction: one-delta red-before contract
- **R1 Same command, committed inputs.** Run `--revision <B>` and `--revision <F>` (B=8606bad, F=fixed commit) from one gate
  blob, recording its sha256 in both runs. Read inputs only via `git show`: no network, no worktree. Rerun red if the
  gate changes.
- **R2 Site table, pinned in the gate.** One row per site: (ID, path, row anchor, verbatim baseline phrase, sha256 of the
  baseline line), anchored by row, not line number. Rows: r13 MD `r12 MD:41-42` + "the value set is not exhaustive";
  S042 teaches; SOURCES :77; lesson :68 (and :17); MD :171. A site is out of scope only by an explicit JSON
  `supersession_notices` disposition with a reason, reported as declared-unrepaired.
- **R3 Per-site states.** Phrase or line absent → FAIL `R14-HISTORY-REWRITTEN`, never PASS. Present with no notice
  resolving it → FAIL `<ID>-ACTIVE@site`. Otherwise SUPERSEDED, emitted as an informational record.
- **R4 Notice predicate (anti-dead-text).** Inside the notice block only: the ID, the r14 MD path, the verbatim superseded
  phrase and, for attribution, `6071740243` + S045. The block sits in the same file before the site (byte offset < site
  offset). For registry sites, S045 is a later row with `supersedes S042` that names the :77 paragraph. The r14 pair at
  the same revision must hold the matching object; a notice with an unresolved target does not count.
- **R5 Acceptance of the red.** At B, findings include ≥1 `<ID>-ACTIVE` at a historical site per correction; `*-MISSING`
  findings never count as the red. At F: exit 0, no findings, and SUPERSEDED site keys equal B's ACTIVE keys. The single
  delta per site is ACTIVE→SUPERSEDED, with bytes unchanged.
- **R6 Count from resolution.** count = the number of IDs whose sites are all SUPERSEDED and whose object, notice and
  RESTORED checks are clean: 0 at B, 2 at F. Fix the oracle: `missing-notice` 0, one notice removed 1, `restored-*` 1.
- **R7 Fixtures from real bytes.** Each mutant is F plus exactly one edit, built from B/F blob bytes. Drop one notice →
  ACTIVE, count 2→1. Move a notice after its site → ACTIVE. Delete a historical phrase → HISTORY-REWRITTEN. Paste a
  verbatim B sentence *with its native negation context* into a replacement or S045 teaches → RESTORED. Remove the pair,
  keep the notices → ACTIVE (dead pointer). Keep the pair, drop all notices → ACTIVE. Turn "#6634 awaits the
  maintainer" into "defers to a maintainer" → `DEFERRAL_MISSCOPED`.
- **R8 RESTORED scan without the negation heuristic.** In claim-bearing fields (JSON `replacement`, S045 teaches, r14 MD
  bodies outside quoted spans), flag verbatim historical phrases or scoped-regex hits; only notice blocks and
  `supersession_notices.scope` may quote them. Drop the S045 `self-describ` requirement; pin `6071740243`, User,
  COLLABORATOR, unverified, second opinion and `#6634`.
- **R9 Word-boundary pins.** Use `\bfull\b`/`\bstrict\b`; the substring checks also match "carefully"/"restricted".

## Impacted axes and limitations
- Axes: depth direct; calibration at risk if "0→2" is reported from the current counter; nothing grades reachability.
- The checker and JSON are in flight; findings 1–8 describe the snapshot read here and may be fixed before landing.
- The real-revision gate outputs are [INFERENCE] from code reading. The API returned HTTP403 to this seat; the #6634
  scoping relies on sibling captures (`ClaimSeparation-source.json`, body sha256 `b7445025…`).
- This gate checks bounded conformance, not source truth; R2–R8 cannot catch new paraphrases outside the pinned sites.
- Coordination: one short message to CorrectionGate (findings 1–7); no other writes. **Tooling:** installed/updated
  none; read RULES.md; used existing git and python3 for read-only blob reads.
