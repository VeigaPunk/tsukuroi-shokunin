# PriorCorrectionSweep — Sweep of False Exclusive Unit-Read-Only Claims

**Date:** 2026-10-20  
**Seat:** TsukuroiR13.PriorCorrectionSweep  
**Target:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md`, `corpus/README.md`, and `corpus/knowledge/`  
**Goal:** Search for false exclusive unit-read-only claims, enumerate bounded active vs historical mentions, and verify required supersession notices.

---

## 1. Executive Summary & Defect Scope

The rejected round-12 depth defect (`corpus/lessons/round-12-verifier-spotcheck.md` @m_strong) identified a substantive false universal:
> The assertion that **only** `ProtectSystem=strict` or `ReadOnlyPaths=` can make `/` read-only through a unit.

This false universal contradicted upstream `systemd.exec(5)` (S028/S041), which specifies:
1. `BindReadOnlyPaths=` creates read-only bind mounts in the unit's private filesystem namespace (independent of `ProtectSystem` and `ReadOnlyPaths`).
2. `TemporaryFileSystem=` accepts mount options including `ro` (e.g. `TemporaryFileSystem=/:ro`), masking underlying paths with a read-only tmpfs.
3. `RootDirectory=` and `RootImage=` remount/pivot the unit root view to an alternate path or image, changing the meaning of `/` within the unit.
4. Among `ProtectSystem=` values, `full` protects `/usr/`, `/boot/`, `/efi/`, and `/etc/` (not `/`), while `strict` covers the hierarchy (subject to documented exceptions such as API subtrees `/dev`, `/proc`, `/sys`, allow-listed `ReadWritePaths=`, `StateDirectory=`, and `PrivateTmp=`).

This sweep performed an exhaustive grep and structural audit across `SKILL.md`, `corpus/README.md`, and all 33+ notes in `corpus/knowledge/` to identify every occurrence of this false exclusive claim and determine whether it is active or historical, and whether the necessary supersession notice is in place.

---

## 2. Enumerated Findings Across the Corpus

### A. `tsukuroi-shokunin/SKILL.md`

- **Mentions identified:**
  1. *Round 12 section (`SKILL.md:1680–1705`):*
     - Contains: `ProtectSystem=full does not make / read-only; property text from an inactive unit is not a runtime trace. The sourced procedure and explicit unknown outcome are in corpus/knowledge/root-dac-decision-r12.md (S027/S028/S034/S035/S038–S040).`
     - Status: **Historical reference.** Does not assert the false universal directly in craft guidance, but points to the rejected round-12 note.
  2. *Round 13 section (`SKILL.md:1716–1738`):*
     - Contains: Active correction under `## Round 13 — active unit-path correction (R13-DAC-EXCLUSIVITY)`. Explicitly clarifies:
       > `"ProtectSystem=no with empty ReadOnlyPaths= excludes those settings only. It does not exclude BindReadOnlyPaths= or a TemporaryFileSystem= mounted ro; RootDirectory=/RootImage= alter the path view but are not inherently read-only. Among ProtectSystem values, full omits / and strict has documented hierarchy coverage and exceptions."`
     - Status: **Active notice present.** Properly bounds the scope to ProtectSystem comparative values.
- **Verdict for `SKILL.md`:** Clean. Active text is accurate and contains the supersession notice for the historical round-12 pointer.

---

### B. `tsukuroi-shokunin/corpus/README.md`

- **Mentions identified:**
  1. *Round 12 table entry (`corpus/README.md:57`):*
     - Pointer: `knowledge/root-dac-decision-r12.md and .json` (EACCES decision matrix).
     - Status: **Historical table row.**
  2. *Round 13 table entry (`corpus/README.md:73`):*
     - Pointer: `knowledge/root-dac-correction-r13.md and .json`.
     - Text: Explicitly labels round 13 as `Active correction R13-DAC-EXCLUSIVITY: ProtectSystem-only comparison, alternative bind/tmpfs read-only mechanisms, unmeasured private-path view, fixture-identity and bot-authority limits; supersedes the rejected round-12 B2 claims, not the historical failure evidence`.
     - Status: **Active notice present.**
- **Verdict for `corpus/README.md`:** Clean. Contains active superseding entry row pointing to R13-DAC-EXCLUSIVITY.

---

### C. `corpus/knowledge/root-dac-decision-r12.md`

- **False exclusive claims identified in historical text:**
  1. *Line 53 (Current host evidence bullet 6):*
     - Text: `"[obs] ProtectSystem=no and empty ReadOnlyPaths=: B2 is not configured for /. For reference, ProtectSystem=full covers /usr/, /boot/, /efi/ and /etc/ but not /; only strict (or a ReadOnlyPaths= entry covering /) would make / read-only through the unit (S028). The B2 discriminator also queries BindReadOnlyPaths=, TemporaryFileSystem=, RootDirectory= and RootImage=, which can change the unit's path view; they were not part of this capture."`
     - Flaw: Asserts *"only strict (or a ReadOnlyPaths= entry covering /) would make / read-only through the unit"*.
  2. *Line 70 (Worked example SC7, step 3):*
     - Text: `"Read-only indicator: host / is rw; ProtectSystem=no; ReadOnlyPaths= empty. B2 is not configured on this host, but a host findmnt cannot exclude a unit-private namespace or another sandbox mechanism."`
     - Flaw: Deduces B2 is not configured based solely on `ProtectSystem=no` and empty `ReadOnlyPaths=`.
  3. *Line 86 (Rejected readings, R13):*
     - Text: `"- R13 — 'ProtectSystem=full makes / read-only.' Rejected: full covers /usr/, /boot/, /efi/ and /etc/; only strict mounts the entire hierarchy read-only (S028). Only strict or a ReadOnlyPaths= entry covering / could produce a B2-family EROFS for / through the unit."`
     - Flaw: Asserts *"Only strict or a ReadOnlyPaths= entry covering / could produce a B2-family EROFS for / through the unit."*
- **Supersession Notice Status:**
  - **Header Notice (Lines 4–10):**
    > `"> **Superseded after outside rejection.** Read root-dac-correction-r13.md and root-dac-correction-r13.json for active B2 unit-path reasoning. The named Round-13 correction at this file's end identifies the historical false universal, incomplete negative claims, fixture-identity and stale QUALITY text retained below."`
  - **Appended Correction Section (Lines 125–155):**
    > `"## Round-13 correction — superseded unit-read-only universal"`  
    > Formally marks R13-DAC-EXCLUSIVITY, notes that `ProtectSystem=no` and empty `ReadOnlyPaths=` exclude only those configured mechanisms (not B2), scopes `full` vs `strict` strictly among `ProtectSystem=` values, and lists `BindReadOnlyPaths=`, `TemporaryFileSystem=ro`, `RootDirectory=`, and `RootImage=`.
- **Verdict for `root-dac-decision-r12.md`:** Historical false claims are preserved under append-only rules and fully bounded by the prominent top header banner and bottom supersession notice.

---

### D. `corpus/knowledge/root-dac-decision-r12.json`

- **False exclusive claims identified in historical JSON fields:**
  1. *`branches[1].interpretation` (JSON line 77):*
     - Text: `"ProtectSystem=full covers /usr/, /boot/, /efi/ and /etc/ only; it does not cover /. ProtectSystem=strict mounts the entire hierarchy read-only except the API subtrees, and a ReadOnlyPaths= entry can cover a specific target. A read-only superblock, a covering ReadOnlyPaths= entry, or ProtectSystem=strict fails create-class writes with EROFS, independent of DAC mode and of capabilities. EROFS is a different errno from EACCES, so an observed EACCES is not explained by this branch. On this host the unit has ProtectSystem=no and empty ReadOnlyPaths=, so B2 is not configured for /."`
     - Flaw: Omits `BindReadOnlyPaths=` and `TemporaryFileSystem=ro` from the EROFS source list, and claims B2 is not configured from two properties alone.
  2. *`branches[1].limit` (JSON line 87):*
     - Text: `"ProtectSystem=full does not cover / (S028), so only strict or a ReadOnlyPaths= entry can make / read-only through the unit."`
     - Flaw: Direct assertion of the false universal.
  3. *`decision_procedure[2]` (JSON line 174):*
     - Text: `"2. Read the target mount's VFS/FS options (findmnt) and the unit's ProtectSystem/ReadOnlyPaths/ReadWritePaths: a read-only superblock, ProtectSystem=strict, or a ReadOnlyPaths= entry covering the target -> B2-family indicator (EROFS). ProtectSystem=full covers /usr,/boot,/efi,/etc, not /."`
     - Flaw: Truncated trigger list.
  4. *`scenarios[4].inputs.mount` (SC5, JSON line 242):*
     - Text: `"mount": "ro, or unit ProtectSystem=strict / ReadOnlyPaths= covering the target"`
- **Supersession Notice Status:**
  - Line 2: `"superseded_by": "corpus/knowledge/root-dac-correction-r13.json"`
  - Line 3: `"correction_notice": "Round 13: historical round-12 records below are preserved, not current advice. The superseding correction replaces B2 interpretation/limit, decision_procedure step 2, SC1/SC2 fixture attribution and the corresponding MD current-host/R13 claims. ProtectSystem=no plus empty ReadOnlyPaths does not exclude another unit-side read-only path view."`
- **Verdict for `root-dac-decision-r12.json`:** Historical records preserved with top-level supersession pointer and notice.

---

### E. `corpus/knowledge/snapper-eacces-mechanism.md`

- **Mentions identified:**
  1. *Lines 10, 58:*
     - Querying `CapabilityBoundingSet`, `ProtectSystem`, `ReadOnlyPaths`, `ProtectHome`.
     - Observes `ProtectHome=yes`, with no matching `ProtectSystem` or `ReadOnlyPaths` lines.
  2. *Line 75 (Round-12 Erratum):*
     - Cited `root-dac-decision-r12.md` and `.json`.
- **Supersession Notice Status:**
  - Appended dated erratum: `## Erratum (2026-10-20, round 13) — R13-DAC-EXCLUSIVITY` (lines 91–102).
  - Explicitly states:
    > `"The round-12 procedure pointer above now resolves to a historical entry rejected at outside closure. Use root-dac-correction-r13.md and .json (S041) for active unit-read-only discrimination. It supersedes the false claim that only strict ProtectSystem or ReadOnlyPaths can make a unit's root/path read-only. BindReadOnlyPaths and read-only TemporaryFileSystem are alternative examples; RootDirectory/RootImage change the path view, and the unit-private namespace was not observed."`
- **Verdict for `snapper-eacces-mechanism.md`:** Clean. Erratum present and accurate.

---

### F. `corpus/knowledge/degraded-triage-r4.md`

- **Mentions identified:**
  1. *Lines 320–324 (J4 analysis):*
     - Text: `"CapabilityBoundingSet=cap_sys_admin, ProtectSystem=no, ProtectHome=yes, ReadWritePaths=/tmp... ro=false (the root subvolume is *not* read-only) and the tree is not remounted read-only (ProtectSystem=no), the caller is root with CAP_SYS_ADMIN — none of the obvious candidates explains errno 13."`
  2. *Line 522 (Table finding J4):*
     - Text: `"the EACCES denial vector (candidates narrowed: ro=false, ProtectSystem=no, root+CAP_SYS_ADMIN)"`
- **Historical Analysis:**
  - Round 4 was an early exploratory triage note (2026-10-14). It observed that `ProtectSystem=no` meant systemd had not applied standard system directory protection. It did not make an affirmative universal claim about all possible namespace options.
  - Furthermore, `degraded-triage-r4.md` carries an appended fleet round 1 erratum (`line 625`):
    > `"Correction [inf]: see corpus/knowledge/snapper-eacces-mechanism.md §§Current host evidence and Falsifier. The measured root mode and unit capability bound support the proposed DAC explanation, but it is not proved until the operator-only falsifier is run..."`
  - Because `snapper-eacces-mechanism.md` is already updated with the Round 13 erratum superseding the r12 note in favor of `root-dac-correction-r13.md`, the provenance chain is intact.
- **Verdict for `degraded-triage-r4.md`:** Historical artifact; correctly superseded downstream.

---

### G. Active Correction Documents (`root-dac-correction-r13.md` and `.json`)

- **Content & Boundary:**
  - Full canonical correction `corpus/knowledge/root-dac-correction-r13.json` and `.md`.
  - Replaces the false universal with:
    > `"Among ProtectSystem= values, ProtectSystem=full does not cover /, while ProtectSystem=strict mounts the entire hierarchy read-only except /dev/, /proc/ and /sys/... BindReadOnlyPaths=, TemporaryFileSystem= with the ro mount option, RootDirectory= and RootImage= can change or restrict the unit's path view and are not excluded by ProtectSystem=no and empty ReadOnlyPaths=."`
  - Explicitly documents all four alternate mechanisms, their discriminators, whether they are intrinsically read-only, and the fact that host `findmnt` cannot observe the unit's private mount namespace.
- **Verdict:** Active target is fully compliant with QUALITY criteria #2, #3, #10, #14, #15, #17, and #18.

---

## 3. Inventory of Bounded Active vs. Historical Mentions

| File | Target Location | Mention Type | Claim Status | Notice Status |
|---|---|---|---|---|
| `SKILL.md` | Line 1695 | Round 12 matrix pointer | Historical pointer | Superseded by Round 13 append (lines 1716–1738) |
| `SKILL.md` | Lines 1720–1730 | Active unit-path guidance | **Active Sourced Rule** | Fully compliant (cites S028/S041, alternatives listed) |
| `corpus/README.md` | Line 57 | Round 12 table row | Historical index | Bounded by Round 13 entry below it (line 73) |
| `corpus/README.md` | Line 73 | Round 13 table row | **Active Sourced Rule** | Explicitly documents R13-DAC-EXCLUSIVITY |
| `corpus/knowledge/root-dac-decision-r12.md` | Lines 53, 70, 86 | False universal prose | Historical defect | Top banner notice & bottom supersession section present |
| `corpus/knowledge/root-dac-decision-r12.json` | Lines 77, 87, 174, 242 | False universal fields | Historical defect | `superseded_by` and `correction_notice` top-level keys present |
| `corpus/knowledge/snapper-eacces-mechanism.md` | Lines 10, 58, 75 | Property sweep & r12 pointer | Historical inference | Appended Round 13 erratum (lines 91–102) present |
| `corpus/knowledge/degraded-triage-r4.md` | Lines 320–324, 522 | Candidate narrowing | Historical triage | Handled via downstream errata chain |
| `corpus/knowledge/root-dac-correction-r13.md` | Entire note | Active correction | **Active Sourced Rule** | Canonical superseding procedure |
| `corpus/knowledge/root-dac-correction-r13.json` | Entire document | Active canonical JSON | **Active Sourced Rule** | Canonical superseding machine-readable record |

---

## 4. Verification Check and Conclusion

All mentions of false exclusive unit-read-only claims across `SKILL.md`, `corpus/README.md`, and `corpus/knowledge/` have been surveyed:
1. **Active surfaces** (`SKILL.md`, `corpus/README.md`, `root-dac-correction-r13.md`, `root-dac-correction-r13.json`) contain strictly scoped, source-grounded statements honoring QUALITY #17 (`"Among ProtectSystem= values..."` without excluding `BindReadOnlyPaths=`, `TemporaryFileSystem=ro`, `RootDirectory=`, `RootImage=`).
2. **Historical surfaces** (`root-dac-decision-r12.md`, `root-dac-decision-r12.json`, `snapper-eacces-mechanism.md`) retain historical bytes under append-only rules, but carry explicit dated supersession notices pointing directly to `root-dac-correction-r13.{md,json}`.
3. No unflagged active false exclusive claims remain anywhere in the workspace.
