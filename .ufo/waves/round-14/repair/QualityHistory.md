# QualityHistory Scout Report — Round 14 Repair

- Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` | Agent: `TsukuroiR14.QualityHistory`
- Axis focus: Depth (primary: resolving claim-source boundaries), Calibration, Adjacency
- Target: Audit QUALITY #17/#18 against lessons 12/13 outside rejections, identify claim-exceeds-source class, isolate Criterion 18 bot overgeneralization.

## 1. Grounded Evidence: Lessons 12/13 Rejections & QUALITY #17/#18

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-12-verifier-spotcheck.md:144-154`: C2 rejected for false exclusivity (`ProtectSystem=strict` or `ReadOnlyPaths=` claimed as the *only* unit-side read-only routes). Line 183 noted S036/S037 misattributed `omarchybot` as "maintainer-side".
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:23-24`:
  - Criterion 17 mandated scoping "only"/"not configured" claims to checked properties, comparing ProtectSystem without excluding alternate mechanisms.
  - Criterion 18 mandated: "record bot comments as automated community triage, never maintainer acceptance."
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-13-verifier-spotcheck.md:143-165`: R13 rejected-harmed on two current factual defects:
  1. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-correction-r13.md:97`: Replacement asserted "the value set is not exhaustive" for `ProtectSystem=`, contradicting `systemd.exec(5)` defining the option as boolean or `full`/`strict`. Non-exhaustiveness belonged to unit-side mechanisms, not the option's value domain.
  2. S042 in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:47` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-13.md:68`: S042 asserted #8047 was "self-described model-generated automated triage", transferring #6629's disclaimer ("Nothing was run on a machine") to #8047, whose body asserted VM execution and cited Codex Medium as a second opinion.

## 2. Recurring Claim-Exceeds-Source Class: Cross-Category Property Projection

The recurring defect across R12 and R13 is **Cross-Category Property Projection**:
When repairing an overclaim, the lane repeatedly projects a valid attribute from one category/scope onto an adjacent, distinct category or source entity:
1. *Mechanism-to-Value Projection (R13 MD:97)*: Valid property "open/non-exhaustive mechanism set" (BindReadOnlyPaths, TemporaryFileSystem=ro, RootDirectory, RootImage) was projected onto the option's parameter domain (ProtectSystem values, which are closed/exhaustive).
2. *Sibling-Source-to-Source Projection (S042 vs S043)*: Valid property "self-described model triage without execution" (strictly confined to #6629 / Claude Opus) was projected across issues onto #8047 based solely on shared author username `omarchybot`.
3. *Account-to-Content Projection*: Inferring textual claims from account handle rather than verbatim quotation.

In each round, correcting an affirmative overclaim produced an ungrounded symmetric counter-claim because the lane reasoned by category transfer rather than verbatim source boundaries.

## 3. Where Criterion 18 Overgeneralizes Bot Role

Criterion 18 (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:24`) states: *"record bot comments as automated community triage, never maintainer acceptance."*

This overgeneralizes bot role in three specific ways:
1. **Monolithic Binary Fallacy**: Forces all comments from bot-named accounts into a single bucket ("automated community triage"), erasing four distinct evidentiary layers:
   - *API Account Metadata*: `login: omarchybot`, `type: User` (not `Bot`), `author_association: COLLABORATOR`.
   - *Execution Claims*: Empirical VM execution asserted (#8047) vs machine execution disclaimed (#6629).
   - *AI Assistance Scope*: AI as consulted "second opinion" (#8047) vs sole model author (#6629).
   - *Decision Governance*: Explicit deferral to maintainer (present in both).
2. **Induced False Attribution**: Mandating "record bot comments as automated community triage" directly caused the R13 author to fabricate the "self-described" attribution in S042 to satisfy the criterion.
3. **Cross-Thread Contagion**: Licenses treating distinct threads by the same bot account as fungible, directly violating immutable source boundaries.

## 4. Concrete Recommendations for Round 14

1. **R14-VALUE-DOMAIN**: Supersede MD:97. Restrict non-exhaustiveness to unit-side sandboxing mechanisms; state ProtectSystem's documented value domain is closed (boolean, `full`, `strict`).
2. **R14-COMMENT-ATTRIBUTION**: Supersede S042 with S045. Ground rejection on absence of host-specific proof and maintainer deferral; report API User/COLLABORATOR fields; cite unverified VM assertion and Codex Medium second opinion; forbid transferring #6629 disclaimer.
3. **Refine Criterion 18 in QUALITY.md**: Replace the blanket "automated community triage" phrase with:
   *"Record bot-associated comments by verbatim claims and API role: distinguish account type/association, empirical assertions, and AI citations from maintainer acceptance; never transfer disclaimers across threads."*

## 5. Limitations

Scout review only; no live repository mutations outside assigned repair report. Source verification performed via historical inspection and outside verifier spot-checks.

## 6. Tooling Record

Tools installed/updated: none
