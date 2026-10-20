# SourceContract — Round 14 Repair S044/S045 Specification & Quote Requirements

Seat: `TsukuroiR14.SourceContract` (scout, report-only). Baseline: `8606bad4cbc6451ac2890c9f8e2548a36c386db6`.
Target: Audit SOURCES contract, S041/S042 immutability, specify append-only S044/S045 and quotes (<=25 words).

## 1. SOURCES Contract & Immutability Rules (`scripts/sources-census.sh`)
- **Table format**: 11 pipe-separated columns (`NF=13` in awk), placed under `## Registry` before `## Paths` (E12).
- **Immutability rule**: Existing S001–S043 rows are historical records. `id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`, `recheck` are immutable and MUST NOT be rewritten in place. Only `status` and `used-by` are mutable by convention. S041 and S042 immutable text remain byte-preserved; corrections proceed strictly via superseding appended rows.
- **Validation rules**: Kind `spec|docs|paper|code|tool|dataset|talk|book|community|own-work` (E05); Tier `A|B|C` (E06; E10 forbids community-at-A); Status `queued|mined|rejected` (E07); Opened ISO date `<= today` (E08); Recheck ISO/`NNd`/symbolic (E09); `used-by` paths must exist on disk at validate time for mined rows (E11); W01 forbids tier C mined with `used-by!=—`; W02 requires rejected `teaches` >= 8 chars; W03 forbids mined with `used-by=—`; W04 warns on duplicate URLs across scopes; E04 triggers on duplicate URL within same scope unless `teaches ~ /supersedes S[0-9]{3}/`.

## 2. Specification for S044 (Value Domain Correction — R14-VALUE-DOMAIN)
- **id**: `S044` | **kind**: `docs` | **tier**: `A` | **status**: `mined` | **opened**: `2026-10-20` | **recheck**: `on-release`
- **source**: `systemd.exec(5) — https://man.archlinux.org/man/systemd.exec.5`
- **scope**: `systemd unit ProtectSystem= documented option value domain (boolean, full, strict) versus unit-side namespace mechanisms` (Distinct from S028 capabilities and S041 namespace path-views to prevent E04; triggers disclosed W04).
- **anchor**: `§ ProtectSystem=; systemd 262.1 man-page footer; page opened 2026-10-20`
- **teaches**: `ProtectSystem takes a boolean argument or the special values "full" or "strict"; the documented option value domain is closed to those values [inference from syntax]; non-exhaustiveness applies to unit-side filesystem isolation mechanisms (such as BindReadOnlyPaths or TemporaryFileSystem), not the ProtectSystem option domain itself; does not prove host runtime configuration.` (Contains no pipe characters).
- **used-by**: `corpus/knowledge/source-scope-correction-r14.md` (E11 requires r14 MD to exist before validate runs).

## 3. Specification for S045 (Comment Attribution Correction — R14-COMMENT-ATTRIBUTION)
- **id**: `S045` | **kind**: `community` | **tier**: `C` | **status**: `rejected` | **opened**: `2026-10-20` | **recheck**: `90d` | **used-by**: `—`
- **source**: `omarchy issue #8047 comment 6071740243 — https://api.github.com/repos/omacom/omarchy/issues/comments/6071740243`
- **scope**: `omarchy issue #8047 comment 6071740243 author account fields, unverified VM non-reproduction claim and maintainer deferral scope` (Distinct scope prevents E04).
- **anchor**: `comment id 6071740243; login omarchybot; user type User; author_association COLLABORATOR; created 2026-10-09T00:27:22Z; read 2026-10-20`
- **teaches**: MUST begin with `supersedes S042 — REJECTED: ` (enables validator regex match). Teaches text:
  `supersedes S042 — REJECTED: author account omarchybot has GitHub API type User (not Bot) and COLLABORATOR association; comment asserts an unverified worker VM non-reproduction run and cites Codex Medium as a non-independent second opinion; body defers #6634 overlay remount policy to maintainers while #8047 awaits the reporter; contains no model-generation or automated triage self-description (transfer of #6629 disclaimer was invalid); retained rejection as host cause; flip requires maintainer resolution or independent reproduction.`

## 4. Quote Requirements & Verified Candidates (<=25 whitespace words)
All quotes must be exact verbatim substrings with verified location, footer/commit, and access date:
- **S044 (systemd.exec(5) § ProtectSystem=, systemd 262.1 footer, line 1271)**:
  - Primary Definition: `“Takes a boolean argument or the special values "full" or "strict".”` (11 words).
  - Note: Source contains zero occurrences of "non-exhaustive" / "not exhaustive"; closure of the option domain is `[inference]` from grammar. MD:97 phrase "the value set is not exhaustive" is superseded by name, not re-quoted as source truth.
- **S045 (omarchy #8047 comment 6071740243, created 2026-10-09T00:27:22Z)**:
  - Unverified VM assertion: `“I tried this on a stock Omarchy worker VM and could not reproduce the central claim”` (16 words).
  - Second opinion: `“Codex Medium reviewed the same evidence and upstream files and reached the same conclusion.”` (14 words).
  - Non-independence caveat: `“It may have seen this analysis first, so its agreement is not guaranteed to be independent.”` (16 words).
  - Deferral scope: `“The remount failure is #6634, which is waiting on the maintainer to decide whether snapshot boots should keep the overlay.”` (20 words). #8047 itself awaits the reporter: `“This now waits on your answer.”` (6 words).
  - Negative sweep: Full comment body has 0 occurrences of "model", "automated", "triage", or "LLM". The #6629 disclaimer (`“Nothing was run on a machine.”` / `“This review is by Claude Opus 5.5 alone.”`) is strictly absent.

## 5. Search Log, Mutable Tracking & Census Predictions
- **Search Log Append**: Append-only entry dated `2026-10-20` recording 2 sources identified/screened (systemd.exec(5), #8047 comment 6071740243), 1 included as support (S044), 1 rejected for cause (S045). Historical search log paragraphs must remain unchanged.
- **Mutable Fields**: S041 status `mined` and used-by `corpus/knowledge/root-dac-correction-r13.md` remain valid; S042 status `rejected` and used-by `—` remain valid. Do not touch historical rows.
- **Predicted Census**: Baseline 43 rows (A36/B1/C6; mined31/queued5/rejected7) → Delivered 45 rows (A37/B1/C7; mined32/queued5/rejected8). Disclosed warning: W04 on S044 URL reuse across scopes.

## 6. Limitations & Tooling Record
- **Limitations**: Read-only specification and contract analysis. No verification commands, builds, or tests executed. Unauthenticated GitHub API returned HTTP 403; account fields cross-checked via rendered page and authenticated sibling read (`gh api`).
- **Tooling Record**: Tools installed or updated: none.
