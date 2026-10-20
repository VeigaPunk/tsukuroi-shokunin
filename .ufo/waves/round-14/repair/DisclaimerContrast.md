# DisclaimerContrast: #6629 vs #8047 Comment Contrast & Transfer Invalidation

- **target**: omarchy #6629 comment 6234472369 vs #8047 comment 6071740243
- **source**: `gh api repos/omacom/omarchy/issues/comments/<cid>` (opened 2026-10-20)
- **agent**: `TsukuroiR14.DisclaimerContrast` (depth axis, scout)

## 1. Primary Source Evidence & Textual Observations

1. **#6629 (comment `6234472369`, 2026-10-17T13:31:32Z, @omarchybot / User / COLLABORATOR)**:
   - **Explicit execution disclaimer**: `"Nothing was run on a machine."` (6 words).
   - **Explicit model self-description**: `"This review is by Claude Opus 5.5 alone."` (8 words); notes budget exhaustion for second classifier model.
   - **Maintainer deferral**: Defers design change (@snapshots) and 4.x issue closure to human maintainers. Body performs static code review of `quattro` branch.

2. **#8047 (comment `6071740243`, 2026-10-09T00:27:22Z, @omarchybot / User / COLLABORATOR)**:
   - **Execution assertion**: `"I tried this on a stock Omarchy worker VM and could not reproduce the central claim"` (16 words). Details packages, commands, overlay behavior.
   - **Second opinion**: `"Codex Medium reviewed the same evidence and upstream files and reached the same conclusion."` (14 words); disclaims independence: `"It may have seen this analysis first, so its agreement is not guaranteed to be independent."` (16 words).
   - **Absence of model self-description**: Zero hits for `Claude`, `model`, `generated`, `triage`, `automated`, or `Nothing was run`. Text is first-person ("I tried", "I checked").
   - **Deferral referents**: `"This now waits on your answer."` (defers to issue reporter); maintainer deferral is strictly scoped to #6634 (`"The remount failure is #6634, which is waiting on the maintainer..."`).

## 2. Why Transferring #6629 Disclaimer to #8047 Is Invalid

1. **Direct Empirical Contradiction**: #6629 explicitly disclaims machine execution (`"Nothing was run on a machine."`), whereas #8047 explicitly asserts machine execution (`"I tried this on a stock Omarchy worker VM"`). Transferring the disclaimer asserts a false negative.
2. **Second Opinion vs. Self-Description**: In #8047, Codex Medium is cited as an external second opinion, not the author of the comment. Calling a second opinion does not make the primary comment text a self-described model generation.
3. **Conflating Account Metadata with Textual Claims**: Account login `omarchybot` and API type `User` (COLLABORATOR) do not establish body self-description. Round 13 mistakenly pooled both comments under #6629's explicit Claude Opus 5.5 self-description.
4. **Evidentiary Impact**: #8047's rejection as host cause remains sound (Tier C, unverified VM test, unresolved bug, mechanically distinct from host DAC/capabilities). However, attributing rejection to a non-existent self-description creates a factual flaw in the knowledge base.

## 3. Why No Source Row Edits (Historical Immutability)

- **Append-Only Doctrine**: Historical entries S036, S037, S042, and S043 in `corpus/SOURCES.md` and `corpus/lessons/round-13.md` are immutable committed baseline artifacts.
- **In-Place Mutation Prohibited**: In-place edits rewrite history and destroy verifiability.
- **Supersession Pattern**: Active repair requires appending a new row `S045` that explicitly supersedes `S042` (`supersedes S042 — REJECTED: ...`), preserving S042 intact while providing accurate attribution for active references.

## 4. Concrete Recommendations for Round 14 Repair

1. **Row S045 (SOURCES.md)**: Add S045 (community, Tier C, rejected), used-by `—`. Teaches must begin: `supersedes S042 — REJECTED:`. Accurately distinguish verified account fields (`omarchybot`, `User`, `COLLABORATOR`), unverified VM execution assertion, Codex Medium second opinion (non-independent), and reporter/issue #6634 deferrals.
2. **Approved Quotes (≤25 words)**:
   - VM assertion: `"I tried this on a stock Omarchy worker VM"` (9 words).
   - Second opinion: `"Codex Medium reviewed the same evidence and upstream files and reached the same conclusion."` (14 words).
   - Independence caveat: `"It may have seen this analysis first, so its agreement is not guaranteed to be independent."` (16 words).
3. **Active References & Gate**: Update `source-scope-correction-r14.md` and `.json` to reference S045 for #8047; add R14-COMMENT-ATTRIBUTION notice to round 13 lesson.

## 5. Limitations & Tooling Record

- **Limitations**: GitHub API accessed read-only via authenticated `gh api` (unauthenticated returns 403 rate-limit). No test, build, lint, or verification commands run.
- **Tooling record**: Installed/updated: none. Used: pre-existing `/home/vgpnk/.local/bin/gh` 2.102.0 and python3.
