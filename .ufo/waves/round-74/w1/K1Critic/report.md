# K1Critic — Round 74 Declaration Attack & Critique Report

- **Seat**: K1Critic (critic, L2 seat, wave w1, round 74)
- **Role**: UFO-FSD critic — attack the proposed approach, evaluate controls, examine channels, analyze sizing, and identify unfalsifiable conjuncts.
- **Basis**: Declaration commit `e51fb49d1790ef283b6aad6752a8c12fac347377` (base `d749a625f483c66f2a6f2005db3799630c776bc3`).
- **Axes**: Calibration, C1 (depth), C2 (freshness), attack.
- **Evidence artifact**: `.ufo/waves/round-74/w1/K1Critic/evidence/attacks.txt`
- **Battery script**: `.ufo/waves/round-74/w1/K1Critic/battery.py`

---

## Executive Summary & Verdict

- **Verdict**: **ATTACKED** — 3 High Severity, 2 Medium Severity, 2 Low Severity findings; Controls evaluated and held.
- **Key Findings**:
  1. **Unfalsifiable Conjunct in C1 Counter (High — D1)**: In `tools/count-uf-rows-r74.py` line 237, the conjunct `and len(snapshots_used) >= TARGET_SNAPSHOTS` in the `met` boolean expression is strictly entailed by `len(parsed_rows) == 6` combined with `findings == 0` (which enforces `MAX_SNAPSHOT_REUSE = 2`). By the pigeonhole principle ($\lceil 6/2 \rceil = 3$), it is mathematically impossible for a passing 6-row note to use fewer than 3 snapshots. Eliminating the conjunct or replacing it with `True` causes zero failures across all 13 selftest cases.
  2. **Declaration Sizing Contradiction (High — D2)**: The frozen declaration claim text in `SCORECARD.md` line 6092 explicitly claims: `"Rows UF1-UF6, sources S309-S311 (v262 unit-file.c, load-fragment.c, unit-file.h)"` — exactly 3 sources. Adding 3 sources to the base count (308) yields 311 registry rows. However, the frozen kill rule at line 6092 mandates `registry < 313` (requiring at least 5 rows), line 6095 states `"five registry rows"`, and `w1-spec.json` tasks SC2Sources with rows S309-S313. An honest implementation adhering strictly to the claim text (adding S309-S311) will fail the round's kill rule.
  3. **Verbatim Answer-Key Embedded in C2 Instrument (High — D3)**: While `count-uf-rows-r74.py` successfully eliminated the Round 73 answer-key defect (D2) by using synthetic fixtures (`syn-alpha.c`), `tools/check-r73-routed-r74.py` embeds literal strings `good_lesson` and `good_log` containing the exact solution text for `corpus/lessons/round-73.md` and `LOG.md`. An author can copy-paste these blocks directly to pass C2 without examining round 73 defects.
  4. **First-Match Block Shadowing in C2 Checker (Medium — D4)**: `check_r73_log_count` in `tools/check-r73-routed-r74.py` searches `LOG.md` blocks from the top and breaks on the first block matching either `R73-LOG-COUNT-STALE` or the fallback `("Round 73" in b and "correction" in b.lower() and "selftest" in b)`. The existing Round 73 entry in `LOG.md` matches the fallback and lacks token `14`. Consequently, an honest correction appended at EOF is never evaluated, and the checker fails with `missing token '14' in LOG.md correction block body`.
  5. **C1 Semantic Detachment / Negation Channel (Medium — D5)**: `tools/count-uf-rows-r74.py` checks only lexical token overlap (`shared >= 6`, `shared/total >= 0.5`) and verbatim quote existence. Statements asserting the exact opposite of systemd functionality pass cleanly (`rc=0 met=1 findings=[]`).
  6. **C2 Pure Lexical Channel (Low — D6)**: `tools/check-r73-routed-r74.py` checks only bare substring tokens. Blocks explicitly denying the corrections or containing ungrammatical token dumps pass with `ROUTED_STALE=0 ROUTED_OK=2/2`.
  7. **Dead Code / Unreachable Disjunct in C1 Counter (Low — D7)**: `if rinfo["kind"] not in KINDS or rinfo["kind"] == "own-work":` contains an unreachable second operand because `"own-work"` is not present in `KINDS`.

---

## Detailed Findings & Counterexamples

### D1: Unfalsifiable Conjunct in C1 Counter (`count-uf-rows-r74.py`)
- **Impacted Axes**: Calibration, C1 (depth), attack.
- **Location**: `tools/count-uf-rows-r74.py` lines 233–238:
  ```python
  met = (
      len(parsed_rows) == TARGET_ROWS
      and len(findings) == 0
      and len(sources_used) >= TARGET_SOURCES
      and len(snapshots_used) >= TARGET_SNAPSHOTS
  )
  ```
- **Analysis**:
  - Parameters: `TARGET_ROWS = 6`, `MAX_SNAPSHOT_REUSE = 2`, `TARGET_SNAPSHOTS = 3`.
  - In `evaluate()`, every row increments `reuse_count[snap]`. If `reuse_count[snap] > MAX_SNAPSHOT_REUSE` (2), a finding is appended (`findings.append(...)`).
  - Therefore, `len(findings) == 0` guarantees that no snapshot is cited more than 2 times.
  - By the Pigeonhole Principle, partitioning $N=6$ items into distinct sets of maximum capacity $M=2$ requires at least:
    $$\text{count} \ge \left\lceil \frac{N}{M} \right\rceil = \left\lceil \frac{6}{2} \right\rceil = 3$$
  - Consequently, whenever `len(parsed_rows) == 6` and `len(findings) == 0`, `len(snapshots_used)` is strictly $\ge 3$.
  - The condition `len(snapshots_used) >= TARGET_SNAPSHOTS` is **unconditionally True** whenever the preceding conjuncts hold. It can never be evaluated as False in any candidate note that reaches the predicate without findings.
- **Empirical Evidence**:
  - Mutant created: replacing `and len(snapshots_used) >= TARGET_SNAPSHOTS` with `and True`.
  - Result: `python3 mutant.py --selftest` passed all 13 cases with 0 failures (`battery.py` Attack 5).
- **Smallest Safe Correction**:
  - Acknowledge in lesson and scorecard that `len(snapshots_used) >= TARGET_SNAPSHOTS` is an invariant entailment rather than an independent falsifiable constraint under `TARGET_ROWS=6` and `MAX_SNAPSHOT_REUSE=2`.

---

### D2: Sizing Contradiction in Round 74 Declaration
- **Impacted Axes**: C1, calibration, sizing.
- **Location**:
  - `SCORECARD.md` line 6092 (Claim text vs Kill rule)
  - `SCORECARD.md` line 6095 (Causal separability description)
  - `w1-spec.json` line 75 (SC2Sources seat milestone)
- **Analysis**:
  - The frozen C1 claim text at line 6092 states:
    `Rows UF1-UF6, sources S309-S311 (v262 unit-file.c, load-fragment.c, unit-file.h)`
    This specifies exactly three sources: S309, S310, S311.
  - The base registry at `d749a625` has 308 rows (`absence-controls.txt:11`).
  - Adding the 3 declared sources produces a registry of $308 + 3 = 311$ rows.
  - However, the frozen kill rule at line 6092 specifies:
    `kill rule: any finding > 0, rows != 6, verified != 6, sources < 3, snapshots < 3, census != 0, registry < 313, notes < 92`
  - And line 6095 asserts: `"C1 touches only its note, five registry rows, and its counter receipts"`.
  - Furthermore, `w1-spec.json` tasks SC2Sources with `"registry rows S309-S313, Gate quotes, search log and one honest rejection"`.
- **Counterexample / Failure Mode**:
  - An implementer reading the frozen claim text ("sources S309-S311") who adds only those three sources will commit a tree with 311 registry rows.
  - Running the declared gate `registry < 313` will evaluate $311 < 313 \implies \text{True}$, triggering the kill rule and failing the round.
- **Smallest Safe Correction**:
  - Wave landing documentation (and wave close erratum) must explicitly clarify that the claim text "sources S309-S311" designates the 3 active note-grounding sources, while the 5 registry rows (S309-S313) account for the required survey/rejection entries per QUALITY 86/102.

---

### D3: Verbatim Solution Answer Key in C2 Instrument
- **Impacted Axes**: C2 (freshness), attack.
- **Location**: `tools/check-r73-routed-r74.py` lines 123–142 (`run_selftest`).
- **Analysis**:
  - `count-uf-rows-r74.py` addressed Round 73 D2 by generating synthetic fixtures (`syn-alpha.c`, `syn-beta.c`, `syn-gamma.h`) with artificial text in `run_selftest()`.
  - In contrast, `check-r73-routed-r74.py` hardcodes the literal production solution blocks:
    - `good_lesson`: contains the verbatim `## Correction (R73-GATE-QUOTE-LINE-DRIFT)` block citing `install.c:2383`, `2387`, `:368-370`, `:237-238`, `:238-239`.
    - `good_log`: contains the verbatim `## Round 73 — correction (R73-LOG-COUNT-STALE)` block citing `11`, `12`, `13`, `14`.
  - This constitutes a direct answer key leak.
- **Empirical Evidence**:
  - `battery.py` Attack 2 extracted `good_lesson` and `good_log` via AST/regex from `run_selftest()` and evaluated them against `evaluate(fixture_texts=...)`.
  - Result: `ROUTED_STALE=0 ROUTED_OK=2/2`, rc 0.
- **Smallest Safe Correction**:
  - In future checker iterations, test checker logic using synthetic heading IDs and synthetic token requirements (e.g. `R73-TEST-DEFECT`, `:100-200`) rather than the production defect names.

---

### D4: First-Match Block Shadowing Rejects Appended LOG.md Correction
- **Impacted Axes**: C2, calibration, attack.
- **Location**: `tools/check-r73-routed-r74.py` lines 68–76:
  ```python
  blocks = re.split(r'\n(?=##+ )', log_text)
  matching_block = None
  for b in blocks:
      if "R73-LOG-COUNT-STALE" in b or ("Round 73" in b and "correction" in b.lower() and "selftest" in b):
          matching_block = b
          break
  ```
- **Analysis**:
  - The loop inspects `blocks` from index 0 forward and executes `break` on the first match.
  - In `LOG.md` at base `d749a625`, the Round 73 entry block already contains:
    `"Round 73"`, `"correction"` ("carried an appended correction"), and `"selftest"` ("twelfth selftest case").
  - Therefore, the existing Round 73 entry block matches the fallback clause `("Round 73" in b and "correction" in b.lower() and "selftest" in b)`!
  - When a new correction block `## Round 73 — correction (R73-LOG-COUNT-STALE)` is appended to EOF (per the append-only convention declared in C2: "LOG.md carries an appended correction"), the loop matches the old block first and halts.
  - The checker then inspects the old block for token `"14"`, fails to find it, and returns `False, "missing token '14' in LOG.md correction block body"`.
- **Empirical Evidence**:
  - Appending `## Round 73 — correction (R73-LOG-COUNT-STALE)\nAppended correction: superseded counts 12 and 11, final committed instrument counts 13 and 14.\n` to `d749a625:LOG.md` resulted in:
    `ok=False msg=missing token '14' in LOG.md correction block body` (`battery.py` Attack 8).
- **Smallest Safe Correction**:
  - Implementers must place the correction block before the existing Round 73 entry, or append an unheaded paragraph inside the existing entry, or the checker must be amended (e.g. checking `reversed(blocks)` or prioritizing explicit ID match over fallback) under the instrument-change rule.

---

### D5: Semantic Detachment in C1 Counter (`count-uf-rows-r74.py`)
- **Impacted Axes**: C1 (depth), attack.
- **Location**: `tools/count-uf-rows-r74.py` lines 193–200.
- **Analysis**:
  - Row statements are checked only for:
    1. Word count $\ge 12$
    2. Shared non-stopword tokens $\ge 6$
    3. Token overlap ratio $\ge 0.5$
    4. Quote verbatim in snapshot
  - There is no semantic entailment check, no contradiction filter, and no requirement that the quote relates to the statement.
- **Empirical Evidence**:
  - `battery.py` Attack 4 constructed 6 rows with explicitly negated assertions directly contradicting systemd's behavior (e.g. "The unit search path priority order NEVER registers first seen unit names at all", "Unit symlinks PERMIT self aliases and IGNORE target unit types completely and unconditionally").
  - The counter evaluated `rc=0 met=1 findings=[]`.
- **Smallest Safe Correction**:
  - Rely on R1Reviewer manual audit of per-row semantic entailment against pinned sources.

---

### D6: Pure Lexical Presence in C2 Checker (`check-r73-routed-r74.py`)
- **Impacted Axes**: C2 (freshness), attack.
- **Location**: `tools/check-r73-routed-r74.py` lines 52–62, 78–90.
- **Analysis**:
  - Both `check_r73_gate_quote` and `check_r73_log_count` check for raw substring inclusion.
  - No directionality or semantic assertion is verified.
- **Empirical Evidence**:
  - Blocks containing explicit rejections ("We strictly reject that install.c:2383 supersedes 2387...", "We refute that instruments had 11 or 12 or 13 or 14 cases") pass cleanly with `ROUTED_STALE=0 ROUTED_OK=2/2` (`battery.py` Attack 3a).
  - Unstructured token jumbles ("11 12 13 14", "install.c:2383 2387 :368-370 :237-238 :238-239") also pass cleanly (`battery.py` Attack 3b).
- **Smallest Safe Correction**:
  - Enforce required action verbs (`supersed*`, `replac*`) alongside token presence.

---

### D7: Dead Code in C1 Counter Kind Validation
- **Impacted Axes**: Calibration, attack.
- **Location**: `tools/count-uf-rows-r74.py` lines 49, 205:
  ```python
  KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community"}
  ...
  if rinfo["kind"] not in KINDS or rinfo["kind"] == "own-work":
  ```
- **Analysis**:
  - `"own-work"` is not a member of `KINDS`.
  - When `rinfo["kind"] == "own-work"`, `rinfo["kind"] not in KINDS` evaluates to `True`.
  - The second disjunct `or rinfo["kind"] == "own-work"` is dead and never reached on False.
- **Empirical Evidence**:
  - Eliminating the second operand left all 13 selftest cases passing with 0 failures (`battery.py` Attack 6).
- **Smallest Safe Correction**:
  - Simplify expression to `if rinfo["kind"] not in KINDS:` in future maintenance.

---

## Evaluation of Pre-Data Controls

| Control Component | File / Location | Observed State | Status |
|---|---|---|---|
| C1 Note Absence | `before/absence-controls.txt:2-3` | `git cat-file -e` returned 128 | Held |
| C1 Counter at Base | `before/absence-controls.txt:4-5` | Returns 128 (`UF_MAP absent`) | Held (benign: pre-data src uncommitted at base) |
| C2 Checker at Base | `before/absence-controls.txt:7-10`| Returns 1 (`ROUTED_STALE=2 ROUTED_OK=0/2`) | Held |
| Held-Ground Sweep | `before/held-ground.txt:1-4` | 0 grep matches across corpus, SKILL, PROVINCE | Held |
| Host Environment | `before/host.txt` | systemd 262 (262.1-1-arch) matches v262 snapshots | Held |
| Snapshot Integrity | `before/src/SHA256SUMS` | All 3 sha256 checksums match upstream v262 bytes | Held |
| Instrument Hashes | `SCORECARD.md:6079-6084` | Hashes match `count-uf-rows-r74.py` and `check-r73-routed-r74.py` | Held |
| Selftest Baselines | Instrument `--selftest` | 13 cases pass (C1), 6 cases pass (C2) | Held |

---

## Conclusion & Recommendations

1. **Unfalsifiable Conjunct**: The C1 counter's `snapshots_used >= TARGET_SNAPSHOTS` is proven to be an invariant entailed by the pigeonhole principle on 6 rows with max reuse 2. This should be recorded as a known vacuity.
2. **Declaration Sizing**: The L1 integrator must ensure that the round documentation explains that the 5 registry rows (S309-S313) fulfill the registry threshold (`registry < 313`), resolving the apparent contradiction with the 3 note-bearing sources (S309-S311) named in the frozen claim.
3. **C2 Answer Key & Shadowing**: C2 executor E2Routed must avoid appending at EOF of `LOG.md` to circumvent the first-match shadowing bug, or the team must invoke the instrument-change rule to harden `check-r73-routed-r74.py`.
