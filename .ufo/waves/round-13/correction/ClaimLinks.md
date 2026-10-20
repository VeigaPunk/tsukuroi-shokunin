# ClaimLinks: Verifier Defects Linked to QUALITY #2, #3, #10, #14, #15 & Proposed Exclusive-Claim Criterion

**Seat:** TsukuroiR13.ClaimLinks (connector role)  
**Target:** Connect outside verifier defects (`round-12-verifier-spotcheck.md`) to `corpus/QUALITY.md` (#2, #3, #10, #14, #15) and propose a precise lesson-backed admission criterion catching exclusive claims.  
**Report Destination:** `.ufo/waves/round-13/correction/ClaimLinks.md`  

---

## 1. Inventory of Round-12 Verifier Defects

From the outside closure audit (`corpus/lessons/round-12-verifier-spotcheck.md` @m_strong) on delivery `f3868cdef07027f7ec8ecd095457d95108f75676`:

1. **Defect D1 — False Universal / Exclusivity Assertion (Primary Rejection Cause):**
   - *Locations:* `root-dac-decision-r12.md` line 53 (current-host explanation), line 86 (R13), and `root-dac-decision-r12.json` B2 `limit`.
   - *Statement:* Asserted that **only** `ProtectSystem=strict` or `ReadOnlyPaths=` can make `/` read-only through a unit.
   - *Falsification:* Independent reopening of `systemd.exec(5)` (S028/S041) confirms `BindReadOnlyPaths=` creates read-only bind mounts, `TemporaryFileSystem=` mounts filesystems with options such as `ro`, and `RootDirectory=` / `RootImage=` modify root view. The exclusive condition contradicted the entry's own B2 `discriminator` list.
2. **Defect D2 — Source Attribution & Automation Conflation:**
   - *Locations:* `corpus/SOURCES.md` S036, S037.
   - *Statement:* Labeled `omarchybot` triage comments as "maintainer-side" authority.
   - *Falsification:* Reopened GitHub API comments show automated triage disclaimers deferring to maintainers, not human maintainer acceptance.
3. **Defect D3 — Fixture Identity vs. Inferred Outcome:**
   - *Locations:* `root-dac-decision-r12.json` SC1/SC2 scenarios.
   - *Statement:* SC1/SC2 specify root-owned hypothetical inputs but cite caller-owned smoke controls (`discriminator-smoke.json`, `error-order-smoke.json` executed as `uid 1000`) as actual basis without explicitly separating inferred same-mode behavior from executed fixture identity.
4. **Defect D4 — Stale Mid-Wave Evaluation & Incomplete Landing Audit:**
   - *Locations:* `root-dac-decision-r12.md` § QUALITY check.
   - *Statement:* Contained mid-wave uncommitted self-assessments (e.g., claiming file was uncommitted mid-wave) rather than an accurate post-landing state check, failing to catch the internal contradiction between B2 discriminator and B2 limit.
5. **Defect D5 — Non-Atomic Commit Ordering (Late Seat Write):**
   - *Locations:* Commit `f3868cd` after report commit `6800f05`.
   - *Statement:* S027 reopening paragraph and LOG erratum committed after the final report.

---

## 2. Rigorous Mapping to QUALITY Criteria (#2, #3, #10, #14, #15)

### QUALITY #2 — Source Anchors & Falsifiability
> *"Every claim carries a source: a measured anchor (path:line, command, evidence id) — never oral knowledge."*

- **Connection to D1 (Exclusivity):** The statement *"only ProtectSystem=strict or ReadOnlyPaths= can make / read-only"* lacked an anchor supporting exhaustive exclusion. The cited anchor (`systemd.exec(5) § ProtectSystem=`) specifies the scope of `ProtectSystem` settings (`full` vs `strict`), but nowhere states that no other directive in `systemd.exec(5)` can create a read-only root mount. Citing a source for setting X does not anchor an exhaustive negative claim over settings Y and Z.
- **Connection to D2 (Bot Attribution):** S036/S037 lacked source-anchored evidence that the bot comment represented maintainer consensus. The anchor (`/comments` endpoint) showed `user: omarchybot` with an automated triage disclaimer.

### QUALITY #3 — Separation of Observation, Inference, and Unknown
> *"Observation, inference, and unknown stay separate."*

- **Connection to D1 (Exclusivity):** An inference (believing `strict` and `ReadOnlyPaths=` are the sole unit-side mechanisms based on common usage) was stated as an unvarnished factual observation/limit, obscuring the unknown configuration surface of systemd mount namespaces (`BindReadOnlyPaths=`, `TemporaryFileSystem=ro`).
- **Connection to D3 (Fixture Identity):** An executed observation on a caller-owned temporary directory (`uid 1000`) was conflated with a hypothetical inference on a `root:root` parent directory. While the DAC mode bits (`0555`) behave identically with respect to write denial across uids without `CAP_DAC_OVERRIDE`, the executed fixture identity is an observation, whereas the root-owned scenario outcome is an inference.
- **Connection to D2 (Bot Authority):** Bot triage output was an observation; assigning it maintainer decision authority was an unsupported inference.

### QUALITY #10 — Supersession Sweep Across Artifacts
> *"Before a correction commit, sweep every mention in README.md, SKILL.md and corpus/knowledge/ for superseded text, and verify changed Markdown tables retain their intended column count and delimiters."*

- **Connection to D1 (Multi-Site Propagation):** The false universal was not an isolated slip; it was replicated across three distinct locations:
  1. `corpus/knowledge/root-dac-decision-r12.md:53`
  2. `corpus/knowledge/root-dac-decision-r12.md:86` (R13)
  3. `corpus/knowledge/root-dac-decision-r12.json` B2 `limit`
  Even though the discriminator correctly enumerated `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=`, and `RootImage=`, the prose and JSON limit retained the superseded exclusive phrasing. QUALITY #10 requires sweeping every active and historical mention in tandem so that partial corrections do not leave conflicting assertions within the same entry.

### QUALITY #14 — Performed vs. Promised QUALITY Check
> *"Before recording an admit for a new knowledge entry, require its explicit `## QUALITY check` to evaluate the applicable numbered criteria and resolve its source/evidence pointers; a promised check is not a performed check."*

- **Connection to D4 (Stale Mid-Wave Quality Check):** The r12 matrix contained a `## QUALITY check` section, but it functioned as self-attestation rather than a rigorous verification gate. Item 14 claimed the check was performed, yet failed to verify:
  - That S028 actually proved exclusivity (it did not).
  - That B2 limit did not contradict B2 discriminator in the very same JSON object.
  - That uncommitted mid-wave drafting language was scrubbed prior to report delivery.
  Under QUALITY #14, a check is not performed if it merely recites criteria numbers without checking the semantic consistency of its assertions against cited sources.

### QUALITY #15 — Precision in Permission Denial, Namespace & Fixture Controls
> *"Root metadata findings report owner-write/search bits, not universal mode policy or process writability. Permission-denial explanations distinguish inode DAC/ACL, mount namespace and runtime credentials; ordinary `mkdir` controls never certify a historical Btrfs ioctl cause."*

- **Connection to D1 & D3 (Namespace & Fixture Separation):** QUALITY #15 mandates distinguishing inode DAC/ACL, mount namespace, and runtime credentials. 
  - For mount namespaces (B2), the explanation failed this standard by falsely narrowing the unit mount namespace options to `ProtectSystem=strict` and `ReadOnlyPaths=`, ignoring documented path-view and mount-namespace primitives.
  - For controls (B1/B4), invoking smoke controls requires precise attribution to the executing identity rather than masking the caller-owned fixture as a root-owned run.

---

## 3. Proposed Lesson-Backed Admission Criterion (QUALITY #17)

To prevent future subagents and lane authors from introducing unanchored universal or exclusive conditions, the following precise criterion is proposed for addition to `corpus/QUALITY.md`:

```markdown
17. Exhaustive exclusivity and universal negative claims ("only X can cause Y", "no other directive can configure Z", "X is the sole mechanism") require an explicit source anchor covering the complete candidate space, or must be strictly scoped to a comparative set ("among ProtectSystem settings, only strict..."). When an entry's own discriminator, diagnostic command, or upstream documentation enumerates alternative mechanisms (e.g. BindReadOnlyPaths=, TemporaryFileSystem=ro), prose limits and JSON records must not contradict that enumeration by asserting exhaustive exclusivity (lesson: corpus/lessons/round-12-verifier-spotcheck.md ## Per-axis verdicts, depth harmed).
```

### Justification & Falsifiability of Criterion #17:
- **Root Cause Caught:** Directly halts the defect where a localized comparison (`ProtectSystem=full` vs `strict`) is expanded into a universal system-wide exclusivity claim without checking other systemd directives.
- **Operational Test:** A mechanical grep/lint or review check can inspect any knowledge entry for exclusivity markers (`only`, `solely`, `exclusively`, `no other`) in explanation/limit fields and check whether:
  1. The sentence qualifies the exact domain (`"Among ProtectSystem values..."`), OR
  2. The source cited explicitly proves exhaustive completeness.
  If the entry's discriminator already lists alternative directives that achieve the effect, an unqualified exclusive statement fails criterion #17 immediately.
