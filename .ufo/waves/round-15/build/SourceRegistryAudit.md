# SourceRegistryAudit — Fleet Registry Contract and Reopened Source Rules

author: TsukuroiR15.SourceRegistryAudit (scout, depth axis)
date: 2026-10-20
baseline: `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`
status: read-only research complete; leaf seat (no subagent dispatch)
judged_on: depth

## 1. Executive Summary & Audit Scope

- **Target:** Audit the source registry immutable field contract (`scripts/sources-census.sh`, `PROTOCOL.md:435`, `corpus/QUALITY.md`, `CORPUS.md`), examine the baseline 45 rows (`S001`–`S045`) through the current 49 rows (`S001`–`S049`) in `corpus/SOURCES.md`, and establish the exact allowed changes for reopened, corrected, or superseded sources.
- **Audit Findings:**
  - `corpus/SOURCES.md` conforms to the 11-column tabular layout required by `scripts/sources-census.sh` (`NF=13` under `awk -F'|'`).
  - Rows `S001` through `S045` represent immutable historical text. In-place edits to intrinsic source definitions (`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`) are strictly forbidden by protocol and validation invariants.
  - Under frozen `CORPUS.md` Rule 2 ("Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson"), mutability in place is strictly limited to `status`, `recheck`, and `used-by`. (Note that no current source fields were mutated in round 15 anyway).
  - Corrections to flawed or reopened sources MUST proceed via **append-only superseding rows** (e.g. `S038` superseding `S034`, `S042` superseding `S036`, `S045` superseding `S042`, `S046` supplementing `S041`/`S044`, `S047` adding Arch doctrine distinct from `S010`, and `S048`/`S049` adding pacman(8) command and query semantics).
  - Search log updates must be append-only dated paragraphs under `## Search log`. Historical paragraphs must remain byte-preserved.
- **Ownership & Operating Boundary:** Read-only research report. No host mutations, package manager operations, service actions, or test execution runs were performed. Tools installed or updated: none.

---

## 2. SOURCES Contract Specification & Census Rules

The authoritative registry validation logic resides in `scripts/sources-census.sh` (`SOURCES-CONTRACT-v1`), executed fleet-wide across child repositories.

### 2.1 Table Structure & Delimiters
- **Location:** Strictly under the section heading `## Registry`. Any row matching `^\|[ \t]*S[0-9]{3,}[ \t]*\|` outside this section triggers fatal error `E12`.
- **Parsing:** Line-by-line parsing with `awk -F'|'`. Markdown table lines permit 0–3 leading ASCII spaces. Lines starting with 4 or more spaces are treated as indented code blocks and ignored.
- **Header & Separator:** Row 1 is column names; row 2 is the markdown separator (`:?-+:?`). Both are skipped by `separator_row()`.
- **Field Count:** Every registry row must contain exactly 11 logical data columns, which corresponds to `NF=13` when split on `|` (accounting for leading and trailing empty fields). `NF != 13` triggers fatal error `E01`.

### 2.2 Column Schema
The 11 columns in order:
1. `id`: Source identifier. Must match regex `^S[0-9]{3,}$` (`E02`). Must be globally unique within the registry (`E03`).
2. `source`: Source title, description, and canonical URL (`https://...` or `http://...`).
3. `kind`: Category enum. Allowed values: `spec`, `docs`, `paper`, `code`, `tool`, `dataset`, `talk`, `book`, `community`, `own-work` (`E05`).
4. `tier`: Epistemic tier enum. Allowed values: `A`, `B`, `C` (`E06`).
   - Invariant: `kind == "community"` cannot be assigned `tier == "A"` (`E10`). Community sources are Tier C.
5. `scope`: Bounded topic, subsystem, or analytical boundary to which this source applies.
6. `anchor`: Section heading, page footer, commit hash, line ranges, or API field path pinning the source locus.
7. `teaches`: Concrete proposition, behavior, or doctrine taught by this source.
8. `status`: Lifecycle enum. Allowed values: `queued`, `mined`, `rejected` (`E07`). Note: `watch` or `superseded` are NOT valid statuses.
9. `opened`: ISO 8601 date (`YYYY-MM-DD`). Must be a valid calendar date and must not be in the future relative to the validation run date (`opened <= today_s`, `E08`).
10. `recheck`: Cadence or review date. Allowed formats (`E09`):
    - Exact ISO date: `YYYY-MM-DD`.
    - Relative day interval: `^[0-9]+d$` (e.g. `90d`, `180d`).
    - Symbolic cadence string: `^[A-Za-z][A-Za-z0-9 _-]*$` (e.g. `on-release`).
11. `used-by`: Comma-separated list of repository-relative markdown paths citing this source, or `—` if none.

### 2.3 Diagnostic Error Codes (`E01`–`E12`)
- `E01`: Malformed row (`NF != 13`).
- `E02`: ID does not match `^S[0-9]{3,}$`.
- `E03`: Duplicate source ID.
- `E04`: Duplicate normalized URL within the same `scope`, unless `status == "rejected"` or `teaches` contains regex `/supersedes S[0-9]{3}/`.
- `E05`: Invalid `kind` enum value.
- `E06`: Invalid `tier` enum value.
- `E07`: Invalid `status` enum value.
- `E08`: `opened` date is invalid or in the future (`> today`).
- `E09`: `recheck` is not an ISO date, `NNd`, or valid symbolic cadence.
- `E10`: `community` kind assigned to Tier `A`.
- `E11`: Referenced `used-by` file path does not exist on disk when `status == "mined"` (evaluated against `$dir/$path`).
- `E12`: Source row (`S###`) placed outside `## Registry`.

### 2.4 Diagnostic Warning Codes (`W01`–`W04`)
Warnings do not cause a non-zero exit code (`status 0`), but must be disclosed:
- `W01`: Tier `C` source marked `mined` with `used-by != "—"` (Tier C community sources cannot be the sole grounding for mined knowledge).
- `W02`: Source marked `rejected` with thin explanation (`length(teaches) < 8`).
- `W03`: Source marked `mined` with `used-by == "—"` (mined source has no referencing document).
- `W04`: Normalized URL appears multiple times across different scopes. (This is a disclosed duplicate-URL warning, not a validation failure).

---

## 3. Immutability Contract vs. Mutable Fields

The registry enforces strict write boundaries between frozen historical records and active lifecycle transitions governed by `CORPUS.md` Rule 2.

### 3.1 Strictly Immutable Fields
For any existing historical row (`S001`–`S045`), the following fields MUST NEVER be edited in place:
1. `id`: Immutable identifier. Renumbering or reassigning an ID breaks fleet references.
2. `source`: URL, title, and initial citation text are frozen.
3. `kind` & `tier`: Historical epistemological classification is immutable.
4. `scope`: Defining scope cannot be widened, narrowed, or rewritten.
5. `anchor`: Historical section locator or citation point is frozen.
6. `teaches`: The proposition or teaching recorded when opened cannot be altered in place. Even if proven false, incomplete, or flawed, the original text is preserved as evidence of what was understood at that time.
7. `opened`: Historical date of access cannot be changed to a later date.

### 3.2 Conventionally Mutable Fields
Under frozen `CORPUS.md` Rule 2 ("Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson"), exactly three fields may transition in place under strictly defined criteria:
1. `status`:
   - `queued` → `mined`: When an active knowledge note or correction pair cites the source and lands on disk.
   - `queued` → `rejected`: When source evaluation determines that the source is disqualified, contradictory, ungrounded, or unverified.
   - *Prohibition:* A `mined` or `rejected` row is NEVER transitioned to another status in place. To change a verdict, append a superseding row.
2. `recheck`:
   - Review cadence or review date updates when a cadence expires or review occurs (each change logged old→new in the round lesson). Allowed formats (`YYYY-MM-DD`, `NNd`, or symbolic string) continue to be enforced by `E09`.
   - *Current Status:* In practice, no current source fields were mutated anyway for `S001`–`S049`.
3. `used-by`:
   - Transition from `—` to an active path when a `queued` row becomes `mined`.
   - Appending additional referencing paths (e.g. `path1.md, path2.md`) as subsequent research cites the source.
   - *Prohibition:* Never delete historical file paths from `used-by` unless correcting an unlanded draft before commit.

---

## 4. Exact Allowed Changes for Reopened or Superseded Sources

When a primary source is reopened in a subsequent wave to correct a prior defect (e.g., locator instability, negative claim overreach, or mistaken attribution), the following exact protocol governs the registry:

### 4.1 Append-Only Superseding Rows
1. **Minting a New Row ID:** Assign the next sequential ID (e.g. `S046`, `S047`, `S048`, `S049`).
2. **Explicit Supersession Link in `teaches`:**
   - If the new row shares the exact same scope and URL as a non-rejected prior row, `teaches` MUST explicitly begin with:
     `supersedes S### — <rationale and corrected teaching>`
     This satisfies the `scripts/sources-census.sh` exemption for `E04`.
   - If the new row defines a new, narrower, or refined scope (e.g. `S041` vs `S044` vs `S046` for `systemd.exec(5)`), the URL reuse across scopes emits warning `W04`. Warning `W04` is NOT an error; it must be disclosed in the authoring report and search log.
3. **Preserving the Historical Row:**
   - The superseded row (e.g., `S034`, `S036`, `S042`) remains completely intact in the table.
   - Its `status` remains as originally recorded (`mined` or `rejected`).
   - Its `teaches` and `anchor` text are NOT edited or deleted.
   - Downstream documents cite the new row, while historical documents retain their citation to the original row.

### 4.2 Handling Duplicate URLs & Scope Discipline
- URL normalization in `sources-census.sh`: lowercases host, strips scheme (`http://`, `https://`), strips trailing `/`, and strips fragment (`#...`).
- When referencing the same URL under a distinct analytical scope (e.g. `systemd.exec(5)` for unit namespaces in `S041`, for argument domain in `S044`, and for stable heading locator in `S046`):
  - Ensure the `scope` string is distinct from earlier rows to avoid triggering `E04`.
  - Disclose the resulting `W04` warning in the commit documentation.

### 4.3 Search Log Protocol
The `## Search log` section records the chronological search and screening provenance:
1. **Append-Only Paragraphs:** Each round or session appends a new dated paragraph at the end of `## Search log`.
2. **Mandatory Elements per Paragraph:**
   - Date and seat identifier.
   - Search query or primary URLs reopened.
   - Candidate counts: identified, screened, included as support, and excluded/rejected.
   - Specific findings and row ID associations.
   - Explicit **Stop Rationale**: Concrete justification for concluding the search without infinite expansion.
3. **Historical Preservation:** Never edit, reword, or reorder earlier paragraphs in `## Search log`. Any corrections to earlier search statements must be stated as an erratum or clarification in the newly appended paragraph.

### 4.4 Downstream Knowledge & Ordering Constraints (`E11`)
- Validation rule `E11` enforces that any path listed in `used-by` for a `mined` row must physically exist on disk at the moment `sources-census.sh validate` is executed.
- **Workflow Dependency:** When authoring a new mined row (such as `S046`, `S047`, `S048`), the citing markdown file (`source-locator-clarification-r15.md`, `partial-upgrade-recheck-r15.md`) must be committed or written to disk before running census validation.

---

## 5. Comprehensive Audit of Registry Rows (S001–S049)

### 5.1 Census Distribution & Histograms

| Metric | Baseline (R14 Start) | R14 Delivered | Round 15 Current |
|---|---|---|---|
| **Total Rows** | 43 | 45 | **49** |
| **Tier A** | 36 | 37 | **41** |
| **Tier B** | 1 | 1 | **1** |
| **Tier C** | 6 | 7 | **7** |
| **Status: mined** | 31 | 32 | **36** |
| **Status: queued** | 5 | 5 | **5** |
| **Status: rejected** | 7 | 8 | **8** |
| **Malformed (`NF != 13`)** | 0 | 0 | **0** |
| **Duplicate IDs (`E03`)** | 0 | 0 | **0** |
| **Same-Scope Collisions (`E04`)** | 0 | 0 | **0** |

### 5.2 Breakdown of Reopened Source Lineages

The registry contains multiple clear lineages illustrating the protocol for reopening sources:

1. **`access(2)` Lineage (`S034` → `S038`):**
   - `S034`: Opened 2026-10-19. Claimed `access(2)` checked permitted capabilities and proved actual writability.
   - `S038`: Appended 2026-10-20. Teaches begins with `supersedes S034 — `. Clarifies that `access(2)` is a proxy check using real UIDs and permitted capabilities, and explicitly does not attempt the operation. `S034` remains preserved in the registry with `used-by` intact.
2. **Omarchy Issue #8047 Lineage (`S036` → `S042` → `S045`):**
   - `S036`: Rejected row attributing comment to "maintainer-side rebuttal".
   - `S042`: Superseding rejected row correcting attribution to `omarchybot` (API type `User`, association `COLLABORATOR`), but incorrectly describing it as model triage based on conflation with #6629.
   - `S045`: Superseding rejected row based on authenticated API inspection of comment `6071740243`. Corrects that the body has no model/triage self-description, identifies "Codex Medium" second-opinion caveat, and grounds rejection on lack of host-specific proof and open issue state.
3. **`systemd.exec(5)` Lineage (`S028` → `S041` → `S044` → `S046`):**
   - `S028`: Scoped to `CapabilityBoundingSet=` behavior.
   - `S041`: Scoped to unit namespace path-view mechanisms (`ProtectSystem=`, `ReadOnlyPaths=`, `TemporaryFileSystem=`).
   - `S044`: Scoped to `ProtectSystem=` documented value domain (11-word quote).
   - `S046`: Appended in Round 15. Scoped to stable structural locator (`SANDBOXING > ProtectSystem=`) and positive option definition without bare renderer line numbers or negative absence assertions.
4. **ArchWiki `System maintenance` Lineage (`S010` → `S047`):**
   - `S010`: Broad package-manager doctrine (news, full upgrades, pacnew handling, rollback).
   - `S047`: Narrowly scoped to § Partial upgrades are unsupported doctrine (8-word quote: "That is why partial upgrades are not supported.") and prohibited command sequences (`pacman -Sy <pkg>`).
5. **`pacman(8)` Lineage (`S048` → `S049`):**
   - `S048`: Install transaction `-p, --print` and `--print-format` preview semantics (14-word quote).
   - `S049`: Query operations (`-Q`), out-of-date filters (`-u`), and `--needed` transaction semantics.

### 5.3 Audit of Current Warning Set (`W04`)
The current 49-row registry exhibits 8 disclosed `W04` duplicate-URL warnings:
1. `S038` vs `S034`: `man.archlinux.org/man/access.2`
2. `S041` vs `S028`: `man.archlinux.org/man/systemd.exec.5`
3. `S042` vs `S036`: `github.com/omacom/omarchy/issues/8047`
4. `S043` vs `S037`: `github.com/omacom/omarchy/issues/6629`
5. `S044` vs `S028`/`S041`: `man.archlinux.org/man/systemd.exec.5`
6. `S046` vs `S028`/`S041`/`S044`: `man.archlinux.org/man/systemd.exec.5`
7. `S047` vs `S010`: `wiki.archlinux.org/title/System_maintenance`
8. `S049` vs `S048`: `man.archlinux.org/man/pacman.8`

All 8 occurrences are intentional, scope-separated reuses compliant with `SOURCES-CONTRACT-v1`.

---

## 6. Recommendations & Integration Guidance for Round 15

1. **Guidance for `LocatorEntry` (C1 Pair):**
   - Cite `S046` (or `S044`/`S046` lineage) using the stable heading: `systemd.exec(5) § SANDBOXING > ProtectSystem=` and footer `systemd 262.1`.
   - Never use bare reader line numbers (such as `rendered lines 1266-1267`) as primary locators. Document that reader lines fluctuate across tools and viewports.
   - For `R15-POSITIVE-DOMAIN`, assert only the positive 11-word quote: `"Takes a boolean argument or the special values \"full\" or \"strict\"."`. Do not assert parser exhaustiveness or negative absence.
2. **Guidance for `IncidentEntry` (C2 Pair):**
   - Cite `S047` for Arch partial-upgrade doctrine and `S048`/`S049` for pacman preview and query semantics.
   - Ensure `corpus/knowledge/partial-upgrade-recheck-r15.md` exists before running census validation to prevent `E11` failures on `S047`, `S048`, and `S049`.
3. **Guidance for Historical Preservation (`ActiveRefs` & L1):**
   - Do NOT edit historical rows `S001`–`S045` in `corpus/SOURCES.md`.
   - In `source-scope-correction-r14.json`, append the top-level `r15_supersession` key without altering existing keys.
   - In `source-scope-correction-r14.md`, append the R15 clarification section without modifying existing text.

---

## 7. Limitations & Tooling Record

### 7.1 Limitations
- **Read-Only Inspection:** Research was strictly static and read-only. No live host state was altered.
- **No Tests or Verifications Claimed:** No verification test suites (`sources-census.sh validate`, pytest, or test runners) were executed in accordance with leaf scout bounds.
- **Scope Scrutiny:** All row counts and field invariants were verified via direct file reads.

### 7.2 Tooling Directive Conformance
- Tools used: `read`, `grep`, `glob` (Cursor built-in filesystem inspection tools).
- System package modifications: **Zero (0)** packages installed, updated, or removed via pacman, cargo, uv, npm, or any other channel. Full compliance with the operator tooling directive and the round 15 strict host instruction.
