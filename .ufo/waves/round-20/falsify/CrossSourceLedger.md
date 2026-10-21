# CrossSourceLedger — Cross-Source Ledger and Proposition Audit

**Seat:** `TsukuroiR19Recovery.CrossSourceLedger`  
**Role:** UFO-FSD Connector  
**Author Round:** Tsukuroi round 20, attempt 1 (`TsukuroiR20`)  
**Baseline:** `0cbc34dd6b20896085a8fb07943e3ea4027d8472`  
**Production Lane:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`  
**Mode:** NO-EXEC (read, grep, glob only; write only this named report; no bash, eval, subprocesses, tests, gates, host probes, or code edits)  

---

## 1. Declared Axes

Per `.ufo/waves/round-20/preregister.json:3–28` and the canonical assignment:
- **C1 Adjacency** (ordinal 8, lowest/tied-lowest, ordinal delta 0):
  - Metric: `ownership_corrections` (0 → 1).
  - Evaluator: `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`.
  - Contract: Ground OUT-009 as an attributed sibling declaration from pinned Revenger `PROVINCE.md` (Electron/JavaScript packages only), without integrator arbitration or host/sibling write authority.
- **C2 Operability** (ordinal 9, ordinal delta 0):
  - Metric: `object_selector_tools` (0 → 9).
  - Evaluator: `python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors`.
  - Contract: Ground object-only hex prefix disambiguation before commit-ish peeling (`git-rev-parse 2.56.0`), preserving original-nine consumer continuity; supporting finite read-only `systemctl` exec-log filtering without claiming general shell execution modeling.
- **C3 Calibration** (ordinal 9, ordinal delta 0):
  - Metric: `audit_live_map_errors` (1 → 0).
  - Evaluator: `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map`.
  - Contract: Align operative boot-chain-audit verdict map to schema-v2 committed summary return paths (live 0/2; selftest 1 separate; no live DEGRADED), disclosing round-19 historical row editing and false operative assertion.

All ordinal deltas remain strictly 0. No claims of host health or boot safety are made.

---

## 2. Cross-Source Ledger Evidence

This audit cross-checks corpus `SOURCES.md` rows S077–S080, round20 lesson (`round-20.md`), initial census artifact (`census-start.txt`), claim documents (`contract-corrections-r20.md`, `preregister.json`, `README.md`), and author source-opening reports (`SrcGitDisambiguate.md`, `SrcRevengerScope.md`, `SrcAuditCodes.md`, `SrcNoWriteAbsence.md`, `SrcGitRevisions.md`, `SrcHookFreshness.md`, `ScribeCensus.md`, `RevNoWriteRule.md`, `RevErratumHistory.md`, `ConnSourceLimits.md`, `MapSourceMap.md`).

### A. Registry Row Verification (S077–S080)

In `corpus/SOURCES.md:84–87` (and curation log `:142`), four rows are registered:

| ID | Source Citation | Kind | Tier | Scope | Anchor | Teaches | Status | Opened | Recheck | Used-By |
|---|---|---|---|---|---|---|---|---|---|---|
| **S077** | Git rev-parse2.56.0 — `https://git-scm.com/docs/git-rev-parse/2.56.0` | `docs` | `A` | Object-prefix enumeration and commit-ish peeling, not lane ancestry/push certification | `OPTIONS --disambiguate=<prefix> and --verify; version2.56.0, opened2026-10-21` | Object disambiguation enumerates actual object names; commit-ish verification can peel an annotated-tag object to a commit, so hex syntax alone is insufficient | `mined` | `2026-10-21` | `on-release` | `corpus/knowledge/contract-corrections-r20.md` |
| **S078** | Pinned Revenger ownership declaration — `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md` | `own-work` | `A` | Exact attributed sibling declaration only, not integrator arbitration or recipient acceptance | `title heading and lines3–7,25–29; sibling commitcf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97, blobsha25663acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f; reopened2026-10-21` | Revenger declares shipped-artifact RE and precisely Electron/JavaScript packages; the declaration neither awards contested ownership nor permits sibling or host remediation writes | `mined` | `2026-10-21` | `on-release` | `corpus/knowledge/contract-corrections-r20.md` |
| **S079** | Committed audit summary source — `tools/boot-chain-audit.sh at0cbc34dd6b20896085a8fb07943e3ea4027d8472` | `own-work` | `A` | Schema-v2 live summary return paths only, not live health or boot readiness | `header lines81–85 and summary lines795–800; opened2026-10-21` | Actual live summary emits UNKNOWN/2 or CONSISTENT/0; retained DEGRADED vocabulary does not create a live exit1, and selftest failure is a separate mode | `mined` | `2026-10-21` | `on-release` | `corpus/knowledge/contract-corrections-r20.md` |
| **S080** | Historical no-write rule — `corpus/knowledge/boot-writers-r19.md at0cbc34dd6b20896085a8fb07943e3ea4027d8472` | `own-work` | `A` | Rejection of rule4's no-write inference from absent log message, not new host evidence | `Operator decision rule item4 line93 versus Falsify qualifications line164; reopened2026-10-21` | REJECTED: missing Updated event does not establish zero writes or unchanged contents; flip: independently bound exhaustive write evidence or content comparison for the exact window | `rejected` | `2026-10-21` | `on-release` | `corpus/lessons/round-20.md` |

### B. Cross-Surface Consistency Matrix

1. **Source Status Alignment:**
   - **S077:** `mined` in `SOURCES.md:84`; `admit source proposition` in `round-20.md:11`; `A — admit, narrowly` in `SrcGitDisambiguate.md:9`. **Status aligned.**
   - **S078:** `mined` in `SOURCES.md:85`; `admit source proposition` in `round-20.md:12`; `A — admit narrowly` in `SrcRevengerScope.md:20`. **Status aligned.**
   - **S079:** `mined` in `SOURCES.md:86`; `admit source proposition` in `round-20.md:13`; `A — admit narrowly` in `SrcAuditCodes.md:35`. **Status aligned.**
   - **S080:** `rejected` in `SOURCES.md:87`; `reject` in `round-20.md:14`; `README.md:184` affirms "keeps the no-write inference rejected"; `RevNoWriteRule.md:23` records S080 as rejected; `ScribeCensus.md:22,26` lists S080 among the 9 rejected rows. In `SrcNoWriteAbsence.md:18`, the scout recommended "A — admit a bounded correction/evidence row recording the event and qualification; reject the historical item-4 no-write inference." The round integration resolved this by admitting the source as a `rejected` status row because the primary proposition ("No write: a snapper-cleanup run with no Updated: line is not a write") is refuted by qualification line 164. **Status aligned as rejected.**

2. **Used-By Binding and Disk Presence:**
   - **S077, S078, S079:** All point to `corpus/knowledge/contract-corrections-r20.md` (`SOURCES.md:84–86`).
     - Disk verification: `corpus/knowledge/contract-corrections-r20.md` exists and cites `S077`, `S078`, `S079` directly in line 1: `source: S077 Git rev-parse 2.56.0 ...; S078 pinned Revenger ...; S079 tools/boot-chain-audit.sh ...`.
     - No `E11 missing used-by` or `W03 mined but unused` warning is raised. **Used-by aligned.**
   - **S080:** Points to `corpus/lessons/round-20.md` (`SOURCES.md:87`).
     - Disk verification: `corpus/lessons/round-20.md` exists and cites `S080` in the Gate table (line 14), Newly opened source rows table (line 27), and Mistakes table (R20-RULE4, line 38).
     - Structural check: `contract-corrections-r20.md:1` deliberately excludes S080 from its supporting source header (keeping it clean of rejected sources), but discusses the substantive R20-RULE4 supersession at line 31.
     - `corpus/README.md:184` synthesizes this by noting `knowledge/contract-corrections-r20.md` deepens held ground while "S080 keeps the no-write inference rejected."
     - Setting `used-by` of S080 to `corpus/lessons/round-20.md` satisfies `scripts/sources-census.sh validate` without dangling references. **Used-by aligned.**

3. **Date Verification:**
   - All four rows in `SOURCES.md` record `opened: 2026-10-21`.
   - S078 and S080 anchors specify `reopened2026-10-21` (reflecting their origin as retained round-19 artifacts).
   - `round-20.md:24–27` records access date as `2026-10-21` across all four rows.
   - `contract-corrections-r20.md:2` states `verified-at: 2026-10-21`.
   - `SrcGitDisambiguate.md:3`, `SrcRevengerScope.md:3`, `SrcAuditCodes.md:3`, `SrcNoWriteAbsence.md:3`, and `ScribeCensus.md:30` all cite `accessed 2026-10-21`.
   - Recheck cadence is uniformly `on-release` across all four rows. **Dates strictly consistent.**

4. **Located Verbatim Quotes (each ≤ 25 words):**
   - **S077:**
     - `round-20.md:24`: `OPTIONS --disambiguate=<prefix>: “Show every object whose name begins with the given prefix.”` (10 words)
     - `contract-corrections-r20.md:15`: `“Show every object whose name begins with the given prefix.”`
     - `SrcGitDisambiguate.md:5`: `“Show every object whose name begins with the given prefix.”`
     - Upstream `git-rev-parse 2.56.0` matches verbatim.
   - **S078:**
     - `round-20.md:25`: `lines3–4: “Owns: reverse engineering of shipped artifacts — native binaries, managed” / “assemblies, Electron/JavaScript packages, Android APKs, archives, firmware,”` (21 words)
     - `contract-corrections-r20.md:9`: `“Owns: reverse engineering of shipped artifacts” and specifically lists “assemblies, Electron/JavaScript packages, Android APKs, archives, firmware,”`
     - `SrcRevengerScope.md:14`: `“Electron/JavaScript packages”`
     - Retained `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md:3–5` matches verbatim.
   - **S079:**
     - `round-20.md:26`: `lines795–800: “summary=UNKNOWN” / “rc=2” / “summary=CONSISTENT” / “rc=0”` (8 words)
     - `contract-corrections-r20.md:23`: `assigns UNKNOWN/2 for unevaluable inputs and CONSISTENT/0 otherwise (S079 summary lines795–800)`
     - `SrcAuditCodes.md:8–17`: reproduces the full 6-line conditional branch.
     - Committed `tools/boot-chain-audit.sh:795–800` at baseline `0cbc34dd...` matches verbatim.
   - **S080:**
     - `round-20.md:27`: `Operator rule4 line93: “No write: a snapper-cleanup run with no Updated: line is not a write.”` (13 words)
     - `SrcNoWriteAbsence.md:7`: `“No write: a snapper-cleanup run with no Updated: line is not a write.”`
     - `boot-writers-r19.md:93` matches verbatim (`4. No write: a snapper-cleanup run with no Updated: line is not a write.`).
   - **Quotes strictly verified and bounded ≤ 25 words.**

### C. Census Start Artifact Integrity

Inspection of `.ufo/waves/round-20/census-start.txt:1–10`:
```text
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	W04	S044 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S046 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S049 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S058 duplicate url gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
exit=0
```
- Exactly eight W04 warnings are emitted; all eight correspond to historical duplicate URLs across distinct scopes (S038 through S058), identical to round 18 and round 19 baselines.
- Zero E-code errors (E01–E12) exist.
- S077–S080 introduce zero new W04 warnings and zero schema violations.
- Exit code is 0.

### D. Audit of Candidate S081 and Unadmitted Source Proposals

1. **Candidate S081 Treatment:**
   - Proposed S081 appears **only** in `ScribeCensus.md:28–48` under `## New row candidate — draft only`.
   - `ScribeCensus.md` explicitly specifies:
     - Line 32: *"Proposed S081 is available at the observed registry snapshot only; L1 must assign the actual unused ID at integration. It follows the existing docs/A/queued/on-release conventions, uses eleven cells with no embedded pipe, and keeps used-by as — because no production note currently cites this new candidate. Validator execution remains pending."*
     - Line 26: *"[INFERENCE: manual registry tally, not an executed census] Current S001–S080 gives 80 rows: A72/B1/C7; mined66/queued5/rejected9... Draft S081 below is excluded from these counts."*
     - Line 48: *"Production rows added by this seat: 0."*
   - Status in the draft table (`:36`): `queued`.
   - **Corpus check:** `corpus/SOURCES.md` ends at S080 (line 87). S081 is **not present** in `SOURCES.md`.
   - **Lesson check:** `corpus/lessons/round-20.md:29` affirms *"Registry changes: four new rows S077–S080, all scopedA; mined3/rejected1."* S081 is **not present** in `round-20.md`.
   - **Claim check:** `contract-corrections-r20.md` does not cite S081.
   - **Consumer check:** `ExecOptions.md:5,9` and `SysctlRuntimeMutation.md:17` cite `systemctl(1)` by documentation URL, not as an admitted source row S081.
   - **Finding:** Candidate S081 is **strictly draft/queued** and is **nowhere treated as admitted**.

2. **Other Build Scout Proposals:**
   - `SrcGitRevisions.md` reviewed `gitrevisions 2.56.0` and recommended Tier A admission.
   - `SrcHookFreshness.md` reviewed `/usr/lib/initcpio/hooks/{plymouth,btrfs-overlayfs}` and recommended Tier A admission.
   - Per `SOURCES.md:142` (Round 20 bounded curation stop rationale), exactly four source objects were screened (Git rev-parse, Revenger declaration, audit summary, rule 4) and exactly four rows added (S077–S080). Git revisions, hook files, and systemctl were excluded from the production registry, preserving the hermetic 80-row boundary.

---

## 3. Explicit Contradictions and Nuances

1. **Scout Recommendation vs Final Row Status on S080:**
   - `SrcNoWriteAbsence.md:18` recommended admitting a bounded row recording the journal event while rejecting the inference.
   - `SOURCES.md:87` and `round-20.md:14,29` registered S080 with `status: rejected`.
   - *Resolution:* This is a valid and conservative curation choice: the row proposition itself ("Historical no-write rule") represents the erroneous rule 4 deduction; registering it as `rejected` ensures that an invalid negative inference is never counted among `mined` evidence, adhering to `QUALITY #9` (bounded negatives).

2. **README Narrative vs Contract Corrections Source Header on S080:**
   - `corpus/README.md:184` groups S080 alongside S077–S079 in describing ground deepened by `contract-corrections-r20.md`.
   - In contrast, `contract-corrections-r20.md:1` lists only `source: S077 ...; S078 ...; S079 ...`, omitting S080 from the header while discussing the R20-RULE4 supersession at line 31.
   - *Resolution:* A knowledge entry's `source:` header must cite only valid supporting sources. Because S080 is a rejected source proposition, `SOURCES.md:87` correctly sets `used-by: corpus/lessons/round-20.md` where the rejection is adjudicated. `README.md:184` provides high-level narrative context, not a formal ledger locator.

---

## 4. Proposed Move: UFO-FSD Connector Synthesis

### The Core Move
**Preserve the Hermetic 80-Row Ledger Freeze (S001–S080) and Maintain Candidate Proposals (`systemctl(1)`, `gitrevisions`, hook paths) Strictly as Inert Tool Data, Never Admitting Draft S081 or Mutating SOURCES.md Mid-Flight.**

### Second-Order Effects Across Surfaces
1. **Verification Surface:**
   - `scripts/sources-census.sh validate` exits 0 with exactly 80 rows and the 8 historical W04 warnings (`census-start.txt`).
   - If S081 were admitted into `SOURCES.md` without an integrated production knowledge note citing it, `validate` would flag `W03 mined but unused` (if mined) or require an explicit recheck/queued cadence. If admitted with malformed fields, it would trip `E01–E12`.
   - Keeping S081 draft-only guarantees census stability across round closeout.
2. **Contract Surface:**
   - C2 Operability requires finite classification of `systemctl` read-only verbs (e.g. `cat`, `show`, `list-timers`) versus mutating verbs (e.g. `restart`, `enable`, `daemon-reload`).
   - Grounding this classifier in `tools/check-recheck-commands.py` requires only static string matching of documented command verbs; it does *not* require an active `SOURCES.md` admission to function as a verification tool.
   - C1 Adjacency and C3 Calibration contracts are fully satisfied by S078 and S079, respectively.
3. **Runtime & Substrate Surfaces:**
   - Neither the 80-row registry nor the candidate draft proposals trigger any runtime command execution, host package action, or boot image regeneration.
   - Host safety and boot clearance remain disclaimed.

---

## 5. Risks and Falsification

- **Risk of Registry Count Inconsistency:** If an uncoordinated seat or evaluator assumes 81 rows based on `ScribeCensus.md:36`, downstream census checks will fail.
  - *Falsifier:* `grep -c '^| S[0-9]' corpus/SOURCES.md` returns exactly 80. Any script expecting 81 must be flagged.
- **Risk of S080 Header Contamination:** If an edit adds `S080` to `contract-corrections-r20.md:1`, it would conflate a rejected negative overclaim with valid positive contract foundations.
  - *Falsifier:* `contract-corrections-r20.md:1` must contain only S077, S078, and S079.

---

## 6. Verification and Limits

- All observations were established via static text inspection using `read`, `grep`, and `glob`.
- No subprocess, shell command, test harness, gate runner, or host probe was executed.
- No code, registry, or documentation edits were made.
- Candidate worktree directories (`/tmp/tsukuroi-r20-*`) confirm baseline status (retaining S076 at baseline).
- Boot image contents, kernel compatibility, and host state remain UNKNOWN.

Scope: executed=none
