# SourceContractReview — round 13 (C1 depth), read-only audit

Scope: constraints for the proposed S041 namespace row and the superseding bot rows S042/S043. No registry, knowledge, or script writes. The census validator was read, not executed. Tools installed or updated: none. Not opened here: systemd.exec(5) text itself (owned by the ProtectSystem/BindReadonly/RootViews seats).

## 1. Contract constraints (observed)

- Shape: `corpus/SOURCES.md:5-6` header, 11 columns; validator requires NF=13 (`scripts/sources-census.sh` header l.24-38, check at l.635).
- Placement: E12 fires for any `S###` row outside `## Registry` (l.618-622). Only a `#` heading ends the section; non-pipe lines are skipped (l.609-615). A row appended after `## Paths` or the notes fails.
- Enums: kind `spec|docs|paper|code|tool|dataset|talk|book|community|own-work` (l.655); tier A/B/C; status `queued|mined|rejected` only (l.658). There is no `superseded` status: adding one is E07.
- E04 (same URL, same scope, non-rejected) is exempted only by the literal regex `supersedes S[0-9]{3}` in `teaches` (l.646-649). W04 (same URL, different scope) is a warning and is NOT exempted by `supersedes`; S038 vs S034 already yields a disclosed W04.
- E08: `opened` must be a valid ISO date `<=` today. E09: recheck = ISO, `NNd`, or symbolic.
- E11: every `used-by` path must exist on disk at validate time (l.566-567). S041's `corpus/knowledge/root-dac-correction-r13.md` does not exist yet, so validate must run after CorrectMatrix lands.
- W01: tier-C mined with `used-by` != `—`. W02: rejected row with `teaches` under 8 chars. W03: mined row with `used-by` = `—`.
- URL normalisation (l.600-605): lowercases host, strips scheme, trailing `/`, and fragment. It does NOT strip `.en`. So `.../systemd.exec.5.en` (the dispatch's URL) is a different string from S028's `.../systemd.exec.5`; dedup and W04 are silently bypassed.
- Immutability is NOT validator-enforced. It is a convention. Precedent shows the mutable fields are `status` and `used-by` (S035 queued→mined, S039/S040 queued→mined, S034 used-by extended). `teaches`, `anchor`, `opened` were never edited in place; S038 added `supersedes S034` in its own teaches instead. The Gate should state this list explicitly.
- Quote cap of 25 words is a lesson convention (`corpus/lessons/round-1.md` quote table; `round-12.md` "Located quote (at most 25 words)"), not a validator rule.

## 2. Existing rows

- **S028** (`corpus/SOURCES.md:34`): URL `https://man.archlinux.org/man/systemd.exec.5`; scope "systemd unit CapabilityBoundingSet behavior..."; anchor "CapabilityBoundingSet= under execution environment options; systemd 262.1 man-page footer"; teaches covers CapabilityBoundingSet only; status mined; used-by degraded-triage-r4, snapper-eacces-mechanism, root-dac-decision-r12.
  - **Finding A (citation accuracy, blocking for the correction):** the r12 matrix cites S028 for `§ ProtectSystem=` (three quotes) and `§ ReadWritePaths=` (`root-dac-decision-r12.json` ~l.56-75, B2 source_ids l.88; MD l.114 lists ProtectSystem under S028). S028's registry anchor and teaches do not cover ProtectSystem. QUALITY #7 requires the applicable section anchor from the registry row. Since S028's anchor cannot be rewritten in place, the correction's namespace claims must cite S041, and S028 stays limited to CapabilityBoundingSet (B3). Historical r12 citations get a superseding notice, not an edit.
  - S028 `used-by` may be extended with the correction path only if the correction still cites S028 (mutable field; record it in the Search log).
- **S036** (`:42`) and **S037** (`:43`): both rejected, tier C, kind community, used-by `—`, scope and teaches as recorded. Both teaches say "maintainer-side" comment. Leave those words unedited (immutable history); the correction is by superseding row.
- Registry now: 40 rows (A35/B1/C4; mined30/queued5/rejected5) per the Search log (l.70). Free IDs: S041, S042, S043 (verified against `^| S0`).

## 3. Proposed S041 — audit

| field | constraint | status of dispatch text |
|---|---|---|
| id | `S041`, unique, inside `## Registry`, inserted after S040 (`:46`) | ok |
| source | use the exact S028 URL `https://man.archlinux.org/man/systemd.exec.5`. If `.en` is used, dedup is silent; disclose the variant and the reason if kept | `.en` URL is a defect of dedup, not of the page |
| kind | `docs` | ok |
| tier | `A` (man page) | ok |
| scope | narrow and distinct from S028: "systemd unit path-view and read-only mount options: ProtectSystem=, ReadOnlyPaths=, BindReadOnlyPaths=, TemporaryFileSystem=, RootDirectory=, RootImage=; not CapabilityBoundingSet" | dispatch lists only three sections; see gap G1 |
| anchor | enumerate every section the correction cites, plus the version footer `systemd 262.1` | gap G1 |
| teaches | state documented semantics only; keep ProtectSystem's documented exceptions (`/dev/`, `/proc/`, `/sys/`) and the `full` vs `strict` scope. Must not say a path view is a read-only mount, nor that the host runs these semantics. Avoid `|` characters (they break NF=13) | ok, wording to be drawn from the scout reports |
| status | `mined` (W03 needs non-`—` used-by) | ok |
| opened | `2026-10-20`. Not `2026-10-19`: S038–S040 carry the same correction (`:68`) | ok if dated correctly |
| recheck | `on-release`, matching S028 | ok |
| used-by | `corpus/knowledge/root-dac-correction-r13.md`. E11 fails until CorrectMatrix lands | ordering dependency, see §6 |

- **G1 (gap):** the dispatch names ProtectSystem, BindReadOnlyPaths and TemporaryFileSystem. The correction's discriminators (`root-dac-decision-r12.json` B2 discriminator l.80-84 and limit l.87) also rely on ReadOnlyPaths=, RootDirectory= and RootImage=, and the "path view is not intrinsically read-only" claim needs their anchors. Without them those claims are unsourced. Add all six anchors to S041, or add a second row, before the correction cites them.
- **G2 (version scope):** the man page footer is systemd 262.1 (S028 anchor). The host's systemd is 261.2-1 (S040 `:46`; S029). Any host-level application of S041 must be marked `[inference]` unless the version difference is checked.
- **G3 (row count):** adding S041 gives W04 for S041 (if S028's URL is used), in addition to the existing W04 for S038. Warnings do not affect exit status.
- **G4 (table format):** keep rows as single lines with 11 pipe-separated cells; no literal `|` inside any cell.

## 4. Superseding bot rows S042 / S043 — constraints

- `teaches` must contain the literal `supersedes S036` (S042) and `supersedes S037` (S043). The regex is the only machine-visible link.
- Status `rejected` (W01 forbids tier-C mined with used-by; community is never sole support). `teaches` must be at least 8 characters (W02). Used-by `—` is consistent with S036/S037 unless the correction cites the row.
- Scope: either reuse S036's/S037's exact scope text (no W04) or accept a disclosed W04. E04 cannot fire because the rows are rejected.
- Do NOT edit S036/S037 teaches or status. Record the attribution correction in a Search-log paragraph.

### Attribution facts (GitHub API, read 2026-10-20; read-only)

- Both issues: `state=open`, label `bug`, `comments=1`. The only comment on each is by login `omarchybot`.
  - #8047: `updated_at 2026-10-09T00:27:22Z`, author_association of the comment `COLLABORATOR`, user type `User`.
  - #6629: `updated_at 2026-10-17T13:31:32Z`, author_association `COLLABORATOR`, user type `User`.
- No comment from an OWNER or MEMBER association exists on either issue. The "maintainer" label in S036/S037 is therefore not grounded in any observed maintainer comment.
- The account `omarchybot` reports API `type=User` (not `Bot`); profile `created_at 2026-08-15`.
- Self-description in the comments:
  - #8047: "Codex Medium reviewed the same evidence... It may have seen this analysis first, so its agreement is not guaranteed to be independent." And "This now waits on your answer."
  - #6629: "This review is by Claude Opus 5.5 alone." and "Nothing was run on a machine." And "that part is the maintainer's decision."
- Therefore "automated-bot" (dispatch wording) and "maintainer-bot" (`round-12.md` l.88) are not API-grounded. Use: "model-generated comment by account `omarchybot` (API association COLLABORATOR, type User) that defers the decision to the maintainer."
- Reported actions are self-reports, not observations. #8047's "I tried this on a stock Omarchy worker VM" and "restore completed" must be labelled as reported. S036's teaches currently states the restore result as a fact.
- Branch wording: #6629 reads the `quattro` branch ("current `quattro` branch (Omarchy 4.x)"). Do not write "4.x ships" as a released fact.
- Short quotes available within 25 words: "This review is by Claude Opus 5.5 alone." (8 words); "Nothing was run on a machine." (6); "This now waits on your answer." (6).

### Unacceptable wording for S042/S043 and the correction

- "maintainer-side", "maintainer-bot", "automated-bot" as authority facts.
- "restore completed" or "reproduced" without "reported by the comment".
- "4.x ships inotify-tools" as a release fact (branch-scoped).
- Any use of S036/S037/S042/S043 as host-cause evidence (rejected rows; flip conditions retained).

## 5. Expected census after integration (for L1 once)

- Current: one W04 (S038). Expected after: S041 W04 (if S028 URL), S038 W04, and S042/S043 W04 only if the scope text differs. No E-codes if S041's used-by exists.
- Totals after: 43 rows; tier A36/B1/C6; mined31/queued5/rejected7. These are computed from the Search log's 40-row figures, not from a fresh census.
- E11 failure is expected if validate runs before `root-dac-correction-r13.md` exists.

## 6. Ordering

- S041 used-by depends on CorrectMatrix; validate after integration, not before.
- The correction must cite S041 (not S028) for namespace claims; the r12 JSON/MD supersession notices name S041 as the replacement source for B2 path-view claims.
- S028 used-by extension and the Search-log paragraph are registry mutable changes; record them with the counts so L1 can check them.
