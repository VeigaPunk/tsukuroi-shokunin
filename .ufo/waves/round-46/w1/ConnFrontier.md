VERDICT: draft

# Item X-3: Round-47 Planned Row Draft (ConnFrontier)

## 1. Naming the Axes

Per `/skill:godspeed` and the lane's operative self-assessment (`SCORECARD.md:2931-2943`), the six governance axes stand as follows at the round-46 base (`2042117cfb724170772f4c128cc2ddba0b61d817`):

| Axis | Score | Current Lane State and Invariants | Lowest Axis Status |
|---|---|---|---|
| **adjacency** | **8** | Formal overlap table present (ADJ-01..07) and portable locators OUT-001..010 intact; recipient acknowledgement and independent replay of handoffs remain unverified in `PROVINCE.md:77-78` and `corpus/README.md:30-32`. | **Lowest (tied with depth)**; controls frontier advancement. |
| **depth** | **8** | 66 knowledge notes, 66 lessons; round-43 C2 verified (SR1, SR3, SR6 bound); round-44 SR7-SR9 and round-45 GR1-GR3 pending at base (`verdicts_ok 0`). If round-46 C2 admits GR1-GR3, SR7-SR9 still remain pending; if C2 fails, depth remains 8. | **Lowest (tied with adjacency)**; carries pending debt. |
| **operability** | **9** | Saturation band; census 154 selftest cases (`154 passed, 0 failed`), boot-chain 49 cases; C1 adds `--identity` (D12) in round 46; round-45 C1 review gaps on case-level reader normalization remain open. | Saturated; hardening candidate. |
| **coverage** | **9** | Saturation band; PROVINCE Core/Frontier/Adjacent, README coverage map, six census planes plus verdict-neutral `STORAGE` and `SCRUB` lines. | Saturated. |
| **freshness** | **9** | Saturation band; predecessor pins S237, S240, S242-S244, S246-S248 and host captures re-checked byte-identical. | Saturated. |
| **calibration** | **9** | Saturation band; `check-self-assessment.py` validates 27 fixed checks with 0 mismatches. | Saturated. |

**Frontier Rule:** Round 47 MUST advance at least one claim on the lowest axis after round 46. At round-46 base, **adjacency** and **depth** are tied lowest at 8. Even if round-46 C2 succeeds in admitting GR1-GR3 (raising or holding depth), adjacency remains at 8. If round-46 C2 fails, both remain at 8.

---

## 2. Evidence and Candidate Analysis

### Candidate 1: Adjacency Move with Recipient Acknowledgement (Axis: Adjacency)

#### A. Historical Problem & The Open Frontier Debt
In `tsukuroi-shokunin/PROVINCE.md:77-78`, the frontier has carried an unclosed limit since fleet round 1:
> "- Recipient acknowledgement and independently replayed handoffs are not verified. The round's author-side replay is not promotion evidence."

`corpus/README.md:30-32` mirrors this exact blocker:
> "- Recipient-side replay, acknowledgement/acceptance and closure of the memory observation packet are unverified; author-side advisory seats are not outside promotion or admit/reject spot-checks."

In `corpus/knowledge/adjacency-handoffs-fleet-r1.json:82-84`, the lifecycle state of route ADJ-04 (`TSUKUROI-F1-MEM-01`) has remained frozen at `"prepared"`:
```json
"id": "ADJ-04",
"trigger": "A host pressure observation or kill signal needs fleet/wave liveness, progress or event correlation.",
"retains": "OS memory, journal, boot and systemd diagnosis.",
"recipient": "mori",
"state": "prepared",
"state_evidence": "TSUKUROI-F1-MEM-01 is the sanitized ADJ-04 packet (corpus/knowledge/adjacency-handoffs-fleet-r1.md:74-85); the bounded sibling receipt sweep found no named-recipient receipt (corpus/knowledge/adjacency-recheck-2026-10-19.md).",
"pending_transition": "reported on integrator commit of .ufo/reports/round-1/tsukuroi.md (fleet repo)"
```

#### B. Verified Sibling Evidence in Mori
The premise that "no named-recipient receipt exists" was superseded on 2026-10-19. Mori committed a dedicated recipient section in `mori-shokunin/PROVINCE.md:71-91` at commit `1f07f1dd1eed59f10c4859726e2f780199190b22` (verified active through current HEAD `c71d088a94b5992d74c2780fde1a7ac267a9b732`, see `.ufo/waves/round-46/w1/ConnFrontier/mori-recipient-receipt.txt`):
1. **Receipt acknowledgement:** `mori-shokunin/PROVINCE.md:71`:
   > `- **Received packet TSUKUROI-F1-MEM-01 (ADJ-04):** ../tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:74-112 records the 2026-10-15T04:53:46Z capture as prepared; boot identity/event window were not captured, and acknowledgement/acceptance/resolution are unobserved. Its request is to compare the timestamp with watchdog/wave evidence if retained, not to infer an OOM or cause.`
2. **Timeline placement:** `mori-shokunin/PROVINCE.md:72` places `04:53:46Z` between watchdog ticks at `01:50:57` and `01:58:27`, bookended by fleet commits `99efc52` and `f2df270`.
3. **Execution of time-bounded sweep:** `mori-shokunin/PROVINCE.md:73-86` executed bounded journal queries for kernel OOM, `fe6faa94…` unit-kill notices, and `d989611b…` oomd notices, all returning 0.
4. **Answer and Non-Absorption Boundary:** `mori-shokunin/PROVINCE.md:88`:
   > `No retained kernel OOM, fe6faa94… unit-kill notice, or d989611b… oomd notice overlaps this bounded query; [UNKNOWN] no independent pressure-series comparison is available for this packet. The single snapshot cannot establish fleet cause or wave settlement. Correlation is not causation.`

#### C. The Proposed Round-47 Move
Advancing ADJ-04 from `prepared`/`reported` to `acknowledged`:
- **Surface moved:**
  - `corpus/knowledge/adjacency-handoffs-fleet-r1.json`: Updates ADJ-04 `state` to `"acknowledged"`, pins mori's `PROVINCE.md` blob hash and commit `1f07f1d`, and records the explicit boundary that receipt acknowledgement does not constitute acceptance of causation or downstream problem resolution.
  - `corpus/knowledge/adjacency-handoffs-fleet-r1.md`: Updates table row ADJ-04 to `acknowledged` with the mori receipt citation.
  - `PROVINCE.md`: Rewrites the blanket frontier sentence (`:77-78`) to distinguish verified recipient acknowledgement (ADJ-04 acknowledged by mori) from unverified downstream acceptance/resolution and unverified independent replay.
  - `corpus/README.md`: Mirrors the updated Frontier clause (`:30-32`).
  - `SCORECARD.md`: Advances the adjacency axis, documenting verified recipient acknowledgement.
- **Counter Idea:** `tools/check-adjacency-acknowledgement-r47.py`
  - Validates JSON ledger schema and confirms ADJ-04 `state == "acknowledged"`.
  - Asserts that the cited mori commit (`1f07f1d`) and blob SHA-256 match the snapshot/sibling bytes.
  - Validates that the report asserts non-absorption (acknowledgement ≠ acceptance, correlation ≠ causation).
  - Runs `python3 tools/check-adjacency-anchors.py --revision <REV>` and requires PASS (no regression of OUT-001..OUT-010).
- **Kill Rule:**
  - Do-nothing control FAILs because at base ADJ-04 is `prepared` and `check-adjacency-acknowledgement-r47.py` expects `acknowledged`.
  - Kill rule fires if:
    - Any sibling repo file is modified (must remain strictly read-only);
    - Sibling authority or causal resolution is asserted;
    - Any existing anchor in `check-adjacency-anchors.py` goes PASS → FAIL;
    - Census behavior, lines, or exits change.

---

### Candidate 2: Binding Round-44 SR7-SR9 Depth Rows (Axis: Depth)

#### A. Historical Problem & The Open Depth Debt
In round 44, three rows were grounded in `corpus/knowledge/btrfs-scrub-record-r44.md`:
- **SR7:** Kernel scrub context lifetime (`dev->scrub_ctx` attached at `scrub.c:3159`, cleared at `:3222`) and replace sharing; `btrfs_scrub_progress` returns 0 only while attached, `-ENOTCONN` when idle.
- **SR8:** Per-device `scrub_speed_max` sysfs attribute (0644, `%llu` read, `memparse` write, 0 = no limit, in-memory only).
- **SR9:** Arch packaging of `btrfs-scrub@.timer` and `.service` (monthly, `Persistent=true`, `btrfs scrub start -B %f`, `KillSignal=SIGINT`).

However, the round-44 depth gate FAILED on binding (`tools/check-scrub-record-r44.py` at `fbfef071`: `verdicts_ok 0`; `.ufo/waves/round-44/after/c2-final-fbfef071.jsonl`). As documented in `btrfs-scrub-record-r44.md:155-159`:
> "**Gate status:** the round-44 depth gate for SR7-SR9 FAILED (`tools/check-scrub-record-r44.py` at `fbfef071`: `verdicts_ok 0` ... Until a counted non-author read binds them, SR7-SR9 are pending, not admitted."

Furthermore, non-author closure spot-check defect D1 (`R45C-D3-R44-MARK-SWEEP`, `corpus/lessons/round-45-verifier-spotcheck.md:184-191`) noted that `corpus/README.md:434` and `SKILL.md:4214` still present SR7-SR9 without proper pending marks.

#### B. The Proven Round-46 Admission Channel
Round-46 C2 solved the verdict-binding channel failure via `tools/check-scrub-admission-r46.py`:
1. The counter reads the seat's **own report file** (`.ufo/waves/round-46/<wave>/<seat>.md`), which seats write verbatim.
2. Line 1: `ROW GR<n> VERDICT: <holds|partly|fails>`.
3. Line 2: `SECTION SHA256: <64-hex>`.
4. The counter binds across any wave name in `*-dispatch.json` and `*-results.json`.

#### C. The Proposed Round-47 Move
Admitting pending rows SR7-SR9 through the proven report-first-line channel:
- **Surface moved:**
  - `corpus/knowledge/btrfs-scrub-record-r44.md`: Gains `## Gate status — round 47 (SR7-SR9 admitted)`.
  - `SKILL.md`: Gains `## Scrub record — round 47 admission (SR7-SR9)` and closes routed defect D1 mark sweep.
  - `corpus/README.md`: Appends `admitted round 47` to the round-44 coverage row.
- **Counter Idea:** `tools/check-scrub-record-r47.py` (or `check-scrub-admission-r47.py`)
  - Evaluates non-verdict legs from round 44 (rows == 3, quotes_ok == 3, props_ok == 3, host_ok == 3, sources_ok == 1, novelty_base_hits == 0, pointer_ok == 1).
  - Binds counted reviewer (`V47RevSR<n>a/b`) and critic (`V47CritSR<n>a/b`) verdicts from seat report files.
  - Asserts that section hashes match the exact byte ranges of SR7, SR8, SR9.
  - Requires `marks_ok == 3` (entry gate status, SKILL section, README row).
- **Kill Rule:**
  - Do-nothing control FAILs because at base SR7-SR9 are pending (`verdicts_ok == 0`).
  - Kill rule fires if:
    - Any bound counted seat reads `fails`;
    - Source quotes drift against frozen snapshots S237, S240, S242-S244;
    - Existing grounding admissions (`check-scrub-admission-r46.py` for GR1-GR3) regress;
    - Any older knowledge entry or gate fails.

---

### Candidate 3: Round-45 C1 Review Gaps on Case-Level CR Pinning (Axis: Operability)

#### A. Historical Problem & Review Gaps
In round 45, C1 converted five reader sites in `tools/tsukuroi-census.sh` to parameter expansion (`${line%%[$'\r\n']*}`, etc.) to prevent SIGPIPE pipe-buffer deadlock on large inputs. However, review seats identified critical gaps:
1. **`C1CritCases.md:15-20` (Surviving mutants & normalization gaps):**
   - Only Case 4 (`t_word`) tested trailing carriage returns and whitespace (`inactive \t\r`).
   - Cases 1, 2, and 5 used clean first lines without trailing whitespace or CR.
   - A mutant that selects the first line but omits CR/trailing-space trimming survives cases 1, 2, and 5.
   - The case labels implied full normalization coverage, but normalization was not pinned per site.
2. **`C1RevKillRules.md:14-20` (Undeclared kill-rule universe & shape ambiguity):**
   - "Shape" comparison was operationalized ad-hoc by `C1ExecPlaneDiff` without a defined schema contract.
   - The predecessor counter regression universe was ambiguously phrased.
   - PASS→FAIL semantics failed to catch field-level regressions where verdicts remained the same.

In `SCORECARD.md:2958-2959`, the round-45 planned row specifically designated:
> "(2) operability — the round-45 C1 review gaps: case-level CR/blank pinning at `:1003`/`:1085`-class sites and a declared kill-rule universe (`a2w1/C1CritCases.md`, `C1RevKillRules.md`)"

Round 46 C1 deferred this to prioritize debt D12 (`--identity`). Thus, the review gaps remain open.

#### B. The Proposed Round-47 Move
Hardening reader normalization and closing the review gaps:
- **Surface moved:**
  - `tools/tsukuroi-census.sh`: Adds explicit case-level selftests with CR (`\r`), blank, and whitespace variations across all 5 reader sites (`probe_systemd`, `probe_drivers`, `probe_journal`, `probe_packages`, etc., labelled `(R47-C1)`), and asserts normalized output values.
  - `SKILL.md`: Documents the explicit input sanitization invariant (whitespace and carriage return stripping) across all census reader sites.
  - Declaration establishes a formal, bounded kill-rule universe for reader normalization.
- **Counter Idea:** `tools/score-census-readers-r47.py`
  - Injects mutants dropping `%%[$'\r\n']*` and `%%[[:space:]]*` at each reader site and verifies that the suite kills every mutant.
  - Asserts `TSUKUROI_CENSUS_SELFTEST: PASS` with 0 failures and `selftest_r47 >= 5` new cases.
  - Verifies that large inputs (past 64 KiB) continue to execute without deadlock or truncation.
- **Kill Rule:**
  - Do-nothing control FAILs because `selftest_r47` cases are absent at base.
  - Kill rule fires if:
    - Any `PLANE`, `HANDOFF`, `DRIFT`, `STORAGE`, `SCRUB`, or `TSUKUROI_CENSUS` line changes shape or exit code base → implementation;
    - Predecessor counters (`score-census-identity-r46.py`, `score-census-readers-r45.py`, `score-scrub-arm-r44.py`) go PASS → FAIL;
    - The census writes a file in live or identity mode.

---

## 3. Second-Order Effects Matrix

Per UFO-FSD connector discipline, tracing effects across all four operational surfaces:

| Candidate | Runtime Substrate Surface | Contract Surface | Sibling & Adjacent Surface | Verification Surface |
|---|---|---|---|---|
| **1. Adjacency Recipient Ack** | Zero runtime execution; no daemon, hook, or binary runs. | Updates ADJ-04 to `acknowledged`; refines Frontier from blanket unverified to verified recipient receipt. | Pins `mori-shokunin/PROVINCE.md:71-91` read-only; affirms non-absorption (correlation ≠ causation). | `check-adjacency-acknowledgement-r47.py` verifies JSON/MD consistency and OUT-001..010 anchor integrity. |
| **2. Depth SR7-SR9 Admission** | Zero runtime execution; source and unit analysis only. | Admits SR7-SR9 into Core depth; grounds kernel scrub lifetime, limit, and timer stop semantics. | No sibling impact; sources are upstream Linux v7.2.11, btrfs-progs v7.1, and systemd v262. | `check-scrub-record-r47.py` binds seat report first lines to exact section hashes; eliminates nominative review drift. |
| **3. Operability Reader Hardening** | Hardens bash parameter expansion against CRLF/whitespace inputs without pipeline forks. | Standardizes reader token trimming contract in `SKILL.md`. | Preserves sibling line pins into census (e.g. mori, tameshi) via append-only selftest cases. | `score-census-readers-r47.py` verifies mutant kill rate on whitespace/CR stripping at all 5 sites. |

---

## 4. Exact Proposed Text for SCORECARD.md

Below is the exact Markdown text drafted for the round-47 planned row at the conclusion of the round-46 measured outcome section in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md`:

```markdown
- **planned (next round):** (1) adjacency — advance route ADJ-04 (`TSUKUROI-F1-MEM-01`) from `reported` to `acknowledged` based on mori's committed receipt in `mori-shokunin/PROVINCE.md:71-91`, updating `corpus/knowledge/adjacency-handoffs-fleet-r1.json` and `.md` with explicit non-absorption boundaries (receipt acknowledgement ≠ causal acceptance or closure), updating `PROVINCE.md` and `corpus/README.md` Frontier clauses, and scored by frozen counter `tools/check-adjacency-acknowledgement-r47.py`; (2) depth — admit the pending round-44 scrub-record rows SR7-SR9 (`corpus/knowledge/btrfs-scrub-record-r44.md`) through the round-46 report-first-line verdict binding channel (`tools/check-scrub-record-r47.py`), closing routed defect D1 (`R45C-D3-R44-MARK-SWEEP`) with matching `SKILL.md` and `corpus/README.md` admission marks; (3) operability — close the round-45 C1 review gaps (`a2w1/C1CritCases.md`, `C1RevKillRules.md`) by adding case-level CR (`\r`), blank, and trailing-whitespace selftest pinning across all five converted reader sites in `tools/tsukuroi-census.sh` (`:1003`/`:1085`-class sites) with a declared kill-rule universe, scored by `tools/score-census-readers-r47.py`. Routed: R45-D7-CITATION-HALF-CLOSED.
- **retired:** none.
```

### Full Declaration Table Specification (for Round-47 Declaration)

For the convenience of the L1 integrator (`TsukuroiR46`) when drafting the round-47 declaration table:

```markdown
| Claim | Axis | Surface moved | Counter (frozen) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | adjacency (capability `recipient-acknowledgement`; sourced: mori `PROVINCE.md:71-91`) | `corpus/knowledge/adjacency-handoffs-fleet-r1.json` and `.md` advance route ADJ-04 (`TSUKUROI-F1-MEM-01`) to `state: "acknowledged"` based on mori's committed receipt (`mori-shokunin/PROVINCE.md:71-91` @ `1f07f1dd1eed59f10c4859726e2f780199190b22`), retaining explicit non-absorption boundaries (receipt acknowledgement ≠ causal acceptance); `PROVINCE.md` and `corpus/README.md` `## Frontier` bullets updated to record verified recipient acknowledgement. | `python3 tools/check-adjacency-acknowledgement-r47.py --revision <REV>` | FAIL: adj04_state == "prepared" (or "reported"), mori_receipt_verified == 0, frontier_ack_qualified == 0 | PASS: adj04_state_ok == 1 and mori_receipt_verified == 1 and frontier_ack_qualified == 1 and anchors_ok == 1 | Any sibling repository file is modified; sibling authority or causal resolution is asserted; any anchor OUT-001..OUT-010 in `check-adjacency-anchors.py` goes PASS → FAIL; the census writes a file or alters live exit/line shapes. |
| C2 | depth (sourced: S237, S240, S242-S244) | `corpus/knowledge/btrfs-scrub-record-r44.md` rows SR7-SR9 (pending since round 44) are admitted: counted reviewer (`V47RevSR<n>a/b`) and critic (`V47CritSR<n>a/b`) seats evaluate each row against digest-checked snapshots and bind verdicts via the first two lines of their report files (`ROW SR<n> VERDICT: <holds|partly|fails>` and `SECTION SHA256: <hash>`); on PASS the entry gains `## Gate status — round 47 (SR7-SR9 admitted)`, `SKILL.md` gains `## Scrub record — round 47 admission (SR7-SR9)`, and `corpus/README.md` gains `admitted round 47`. | `python3 tools/check-scrub-record-r47.py --revision <REV>` | FAIL: r44_legs_ok == 1, verdicts_ok == 0, marks_ok == 0 | PASS: r44_legs_ok == 1 and verdicts_ok == 3 and marks_ok == 3 | Any bound counted seat reads `fails`; source quotes drift against S237, S240, S242-S244; `check-scrub-admission-r46.py` (GR1-GR3) regresses; any older knowledge entry or gate fails. |
| C3 | operability (capability `reader-normalization-resilience`) | `tools/tsukuroi-census.sh` gains case-level selftests with CR (`\r`), blank, and trailing-whitespace inputs across all five converted reader sites (`probe_systemd`, `probe_drivers`, `probe_journal`, `probe_packages`, etc., labelled `(R47-C1)`); `SKILL.md` documents the reader token trimming and CRLF sanitization contract across all census arms. | `python3 tools/score-census-readers-r47.py --revision <REV> --scratch <DIR>` | FAIL: selftest_r47 == 0, cr_pinning_ok == 0, mutants_killed < 5 | PASS: selftest_pass == 1 and selftest_r47 >= 5 and cr_pinning_ok == 1 and mutants_killed == 5 and nowrite_ok == 1 | Any `PLANE`, `HANDOFF`, `DRIFT`, `STORAGE`, `SCRUB`, or `TSUKUROI_CENSUS` line changes shape or live exit code base → implementation; any predecessor counter (`score-census-identity-r46.py`, `score-census-readers-r45.py`, `score-scrub-arm-r44.py`) goes PASS → FAIL; the census writes a file in live or identity mode. |
```

---

## 5. Verification and Non-Harm Receipts

Receipts generated in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-46/w1/ConnFrontier/`:
1. `mori-recipient-receipt.txt`: Transcribes `mori-shokunin/PROVINCE.md:71-91` and git commit history confirming that mori received and answered packet `TSUKUROI-F1-MEM-01 (ADJ-04)` at commit `1f07f1d` (active through HEAD `c71d088`).
2. `round44-sr7-sr9-status.txt`: Transcribes `btrfs-scrub-record-r44.md:153-162` confirming SR7-SR9 pending status, and spot-check defect D1 (`R45C-D3-R44-MARK-SWEEP`).
3. `round45-c1-review-gaps.txt`: Transcribes `C1CritCases.md:15-20` and `C1RevKillRules.md:14-20` detailing reader normalization gaps and undeclared kill-rule universes.
4. `axes-frontier-audit.txt`: Verifies `PROVINCE.md:75-84`, `corpus/README.md:28-33`, and `SCORECARD.md:2931-2962` showing current axes, saturation, and lowest-axis status (adjacency at 8, depth at 8).

Scratch directory `/fast/scratch/hyaku/tsukuroi-r46/ConnFrontier` was cleaned up on completion. No tracked lane files or fleet files were modified. Read-only host guard preserved throughout.
