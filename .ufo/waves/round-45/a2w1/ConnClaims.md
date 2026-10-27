VERDICT: draft

# ConnClaims — round 45, wave a2w1 (Item X-1: patterns across C1 and C2, lane history, and QUALITY criteria)

Scope: proposed QUALITY criterion synthesized across C1, C2, counter evolutions, and the lane's multi-round history. No claim is falsified here; this draft provides evidence, analysis, and an exact proposed criterion for the L1's integration. Evidence is read exclusively from committed repository files, frozen sources, and pre-data control batteries:
- Frozen counters: `tools/score-census-readers-r45.py` (sha256 `fe0e31e25c5b3c92cc5aace48acc56bc6dab39b4b3c09b49708a715a3250bd50`), `tools/check-scrub-grounding-r45.py` (sha256 `a1eb402dffae97fcefd9bd539529f1cacc5034419b6de06e1f8ac1c08d011331` at attempt-2 rebinding);
- Control batteries & receipts: `.ufo/waves/round-45/controls/` (`run_controls_c1.py`, `battery-summary-c1.jsonl`, `C1-K*.jsonl`), `.ufo/waves/round-45/controls-a2/` (`run_controls_c2.py`, `battery-summary-c2.jsonl`, `C2-K*.jsonl`), and baseline receipts `.ufo/waves/round-45/before/` (`adjacency-base.txt`, `c2-before.jsonl`, `self-assessment-base.txt`);
- History & lessons: `corpus/lessons/round-41.md`, `corpus/lessons/round-42.md` (`R41-CENSUS-PIPEFAIL-692`, `R42-C1-CLASS-UNSWEPT`), `corpus/lessons/round-43.md` (`R43-CENSUS-PROBE-COORDS`, `R43-CAP-HEADER-DUP`), `corpus/lessons/round-44-verifier-spotcheck.md` (§2 C2 FAIL, adjacency harm via IN-109), `.ufo/waves/round-44/w1/ConnClaims.md`, `.ufo/waves/round-44/w2/ConnFinalQuality.md`;
- Governance standards: `SCORECARD.md` section "Round 45 — declaration", and `corpus/QUALITY.md` criteria 1-92 (specifically 80-92).

As a leaf member, I did not spawn subagents, did not mutate any tracked lane file or host state, did not run git mutating commands, and did not execute the full counters. All findings and quotations cite verifiable repository bytes.

---

## 1. Cross-Claim Patterns: C1, C2, and Counter Evolution

Examining Round 45's two causally separable claims alongside the lane's historical arc from Round 41 through Round 44 reveals three interlocking structural patterns:

### Pattern 1: Defect-Class Remediation vs. Partial Site Patching (C1)
- **Origin in Round 41/42:** In Round 41, the census's `set -euo pipefail` environment turned early-reader pipelines (`printf … | grep -q`, `| grep -m1`, `| head`) into a fatal trap (`R41-CENSUS-PIPEFAIL-692`): once a captured probe buffer exceeded the 64 KiB pipe buffer, the early reader exited, the upstream producer died of SIGPIPE, and the command returned exit code 141. In Round 42, C1 claimed to fix this defect class, inserting the docstring at `tools/tsukuroi-census.sh:692-695`:
  `# Round 42 (R41-CENSUS-PIPEFAIL-692): never printf | grep -q / | grep -m1 / | head under pipefail on a probe buffer — the early reader exits, printf dies of SIGPIPE, and the pipeline reads false (a wrong verdict) or, in an assignment, kills the census with exit 141. Read here-strings or let awk consume the whole input.`
- **The Partial-Patch Gap:** Despite naming the universal defect class in its comment and lesson, Round 42 only patched the two specific sites where failures had been concretely observed: the packages plane sample (`:692`) and update-safety `-Qu`/`-Sup`/`-Suu` name extraction (`:1621-1652`). Wave 1 seat `MistakesSweep` identified that five production probe readers retaining the first line of captured outputs with `printf '%s\n' "$CAP_OUT" | head -n1` remained in `tools/tsukuroi-census.sh` (`MistakesSweep.md:30`). The Round 42 lesson recorded this as `R42-C1-CLASS-UNSWEPT` (`corpus/lessons/round-42.md:81`) with `Captured-by: none` and routed it as debt.
- **Lingering Multi-Round Debt:** In Round 43, `R43-CENSUS-PROBE-COORDS` (`corpus/lessons/round-43.md:107`) noted that line coordinates drifted (`:931, :969, :1051, :1426, :1501` → `:934, :972, :1054, :1429, :1504`) because the defect had been cited by mutable line numbers rather than bound to a content pattern, yet the defect remained untouched. In Round 44, the debt lingered again while the census was edited for scrub records.
- **Exhaustive Sweep & Proof in Round 45:** C1 in Round 45 finally closes all five production readers:
  - `S1 probe_systemd state` (`systemctl --user is-system-running`)
  - `S2 probe_systemd r` (`systemctl --user show <timer> -p Result`)
  - `S3 probe_drivers driver` (`nvidia-smi --query-gpu=name,driver_version`)
  - `S4 probe_journal t_word` (`systemctl is-active <boot target>`)
  - `S5 probe_journal r` (`systemctl --user show <timer> -p ActiveState`)
  Replacing them with parameter expansion (`${CAP_OUT%%$'\n'*}`).
- **The Structural Verification Difference:** In Round 42, no check verified that all sites were gone. In Round 45, `tools/score-census-readers-r45.py` enforces `lexical_hits == 0` (zero lines matching `"$CAP_OUT"\s*\|\s*head\b` before `run_selftest()`). The pre-data battery includes control `C1-K1` (`| head -1` evasion, `run_controls_c1.py:11`), which tests that an un-swept or evasive early-reader fails (`lexical_hits: 5`, exit 1, `battery-summary-c1.jsonl`). Furthermore, seven masked or process-substitution readers (`:707`, `:832`, `:997`, `:1196`, `:1517`, `:1531`, `:1817`) that cannot kill the census are explicitly disclosed as recorded limits in the declaration, rather than silently ignored.

### Pattern 2: Sourced Mechanism Grounding vs. Partial Inferences (C2)
- **Round 44 Incomplete Grounding:** Round 44 added `corpus/knowledge/btrfs-scrub-record-r44.md` describing the status record file, but left three propositions marked `[inference]` because the underlying upstream mechanisms had not been mined: how `memparse` parses `scrub_speed_max` suffixes, how device replace coordinates with concurrent scrubs, and what signals `systemctl stop` issues to packaged scrub units.
- **Round 45 Depth Closure:** C2 in Round 45 replaces those inferences with definitive source groundings in `corpus/knowledge/btrfs-scrub-grounding-r45.md`:
  - `GR1`: `memparse` radix-0 and suffix multiplication in Linux v7.2.11 `lib/cmdline.c`, `lib/kstrtox.c`, and sysfs write handling in `fs/btrfs/sysfs.c` (S246, S243);
  - `GR2`: device replace running `btrfs_scrub_dev` with `is_dev_replace=true` and non-replace scrubs refusing with `EINPROGRESS` in `fs/btrfs/dev-replace.c` and `fs/btrfs/scrub.c` (S247, S242);
  - `GR3`: `systemctl stop` sending `SIGINT` to the whole cgroup, then `SIGCONT`, then `SIGKILL` after `TimeoutStopSec` (5 s on this host) in systemd v262 `man/systemd.kill.xml` and unit `btrfs-scrub@.service` (S248, S244).
- **Parallel with C1:** Just as C1 converted all five lingering early-reader sites rather than patching one, C2 resolves all three open inference gaps on the scrub mechanism rather than leaving ungrounded assertions.

### Pattern 3: Refusal of Structural Projection Gaps Across Both Counters
In Round 44, both counters operated through weak normalizing projections that accepted malformed or vacuous inputs (documented in `round-44-verifier-spotcheck.md`, `w1/C2RevCounter.md`, `w1/C2MutBinding.md`, and `w2/ConnFinalQuality.md`). In Round 45, both counters were systematically hardened to refuse what Round 44 accepted:
1. **Gutted Quotes:** Round 44 evaluated quotes by simple substring presence (`q in src[n-1]`), allowing single-character quotes like `"n"` to pass (C2RevCounter F1). Round 45 C2 counter requires quotes to be at least 10 characters or the full stripped line, and at least half the stripped line length. Pre-data control `C2-K20` (gutted quote `"n"`) is refused (`quotes.bad: 1`, exit 1, `controls-a2/C2-K20.jsonl`).
2. **Duplicate Keys & Duplicate Registry Rows:** Round 44 parsed JSON with default `json.loads` (last duplicate key wins; C2MutBinding F1) and parsed `SOURCES.md` with `rows[cells[0]] = cells` (last row wins; C2RevCounter F2). Round 45 C2 counter enforces `object_pairs_hook=reject_duplicate_keys` on JSON files (`a2w1-dispatch.json`, `a2w1-results.json`) and requires that an S-id appearing on more than one row-shaped line in `SOURCES.md` makes `sources_ok: 0`. Pre-data controls `C2-K21` (duplicate S246 row appended), `C2-K22` (duplicate S246 row in code fence), and `C2-K23` (duplicate `verdict_line` keys) all fail (`controls-a2/C2-K21.jsonl`, `C2-K22.jsonl`, `C2-K23.jsonl`).
3. **Orphan Repositories:** Round 44 C2RevCounter F3 noted that an orphan git clone without base ancestry could vacuously satisfy certain gates. Round 45 C2 counter checks `base_ok` (`git merge-base --is-ancestor BASE REV`). Control `C2-K25` (orphan repository) exits 2 (`controls-a2/C2-K25.jsonl`).
4. **Unrepinned Anchors (Adjacency Gate as Kill Rule):** In Round 44, inserting `probe_scrub_record` into `tools/tsukuroi-census.sh` moved line 2468 to 2582 without updating `IN-109` in `corpus/knowledge/adjacency-anchors-r19.json`, causing the adjacency gate to fail at the tip (`status: FAIL`, `INBOUND-CLASSIFICATION-WRONG`, `adjacency-base.txt`) and resulting in `rejected-harmed` closure. In Round 45, C1 embeds `adjacency_ok == 1` as an inviolable kill rule scored against `check-adjacency-anchors.py`. Control `C1-K7` (unrepinned anchor drift) fails C1 immediately (`adjacency_ok: 0`, exit 1, `controls/C1-K7.jsonl`).

---

## 2. Comparison with QUALITY Criteria 80–92

`corpus/QUALITY.md` currently ends at criterion 92 (`R43-CAP-HEADER-DUP`). Let us evaluate criteria 80 through 92 against the defect-class sweep gap exposed by C1, C2, and counter hardening:

| Criterion | Stated Obligation | Does it govern defect-class sweeps on code/tools? |
|---|---|---|
| **80** (R31-DEPTH-UNFALSIFIABLE) | Depth claim target requires pre-data do-nothing controls; novelty swept as facts, not tokens. | No. Governs depth claim falsifiability and semantic novelty in knowledge entries. |
| **81** (R31-SCRIPTED-NONREADER) | Depth rows require committed non-author reviewer verdict; controls include scripted writer. | No. Governs non-author reading of sources vs scripted filler. |
| **82** (R32-FIXTURE-GATEABLE) | Behavioural counter must score code outside fixtures (live host, cached live variant). | No. Governs execution environment of scored code, not code defect sweeps. |
| **83** (R38-VERDICT-CONJUNCT) | Post-wave verdict changes grounded per declared conjunct; closure re-measures conjuncts. | No. Governs adjudication and closure verdict accounting. |
| **84** (R38-ECHO-UNVALIDATED) | Machine grammars echo only validated tokens. | No. Governs `key=value` serialization formats. |
| **85** (R38-Q82-LEAK) | Production-path views must be built in child mount namespaces without host path leaks. | No. Governs container/namespace isolation in test harnesses. |
| **86** (round-38 C2 counter gaps) | Rule rows verify on upstream sources, never own-work captures alone. | No. Governs source provenance of knowledge rows. |
| **87** (R39-CONTENT-UNREAD) | Content counters must read the content they credit; controls include content-free entries. | No. Governs counter inspection of statement cells. |
| **88** (R40-CLAIM-PARAMETERS) | Counter acceptance implies declaration's named content parameters; controls violate exactly one. | Partial analog, but restricted to declaration parameters. Does not mandate sweeping a defect class across the codebase. |
| **89** (R41-GUARD-BYPASS) | Adversarial guards scored against evasions of the guard's own mechanism; family closed only by non-lexical checks. | Close, but governs test harness evasions (e.g. decoys, here-docs), not completeness of code repair across call sites. |
| **90** (R42-OBSERVED-CHANNEL) | Counters without answer keys scored per observation channel; verdict binding matches asserted first line. | No. Governs metamorphic twin channels and verdict line anchoring. |
| **91** (R42-ADOPTED-UNREAD) | Integrator checks reviewer proposed text against source before adoption; counted read follows. | No. Governs text adoption workflow. |
| **92** (R43-CAP-HEADER-DUP) | Rendered machine-readable tables must carry exactly one header row. | No. Governs Markdown table formatting. |

### The Governance Gap in Existing Sweep Rules
Existing sweep rules in `corpus/QUALITY.md` are exclusively informational or document-oriented:
- QUALITY 8: Sweep logs before retaining `[unknown]`.
- QUALITY 9: Negative claims require a bounded search sweep command.
- QUALITY 10: Sweep mentions in documentation for superseded text before a correction commit.
- QUALITY 60: Sweep non-append lines in record files via `git diff -U0`.
- QUALITY 68: Sweep knowledge corpus before declaring a frontier coverage claim.

**The Void:** There is NO criterion in `QUALITY.md` governing **code repairs and defect classes**. When a defect class (such as `R41-CENSUS-PIPEFAIL-692`) is uncovered:
1. Nothing forbids an integrator from fixing only the single line that triggered an incident while leaving identical vulnerability sites unpatched across the same file or module.
2. Nothing requires the verification counter or gate to pin an exhaustive lexical or AST sweep check asserting zero remaining unhandled occurrences (`lexical_hits == 0`).
3. Nothing requires the pre-data control battery to prove that an un-swept site or evasion variant fails the gate.
4. Nothing requires unpatched sites (such as masked or non-fatal variants) to be formally enumerated as recorded limits in the declaration.

Because this standard was missing, `R42-C1-CLASS-UNSWEPT` had `Captured-by: none` in `corpus/lessons/round-42.md:81`. The five production probe readers survived untouched through Round 42, Round 43, and Round 44—causing three rounds of lingering debt and risk until Round 45 C1 finally performed the sweep.

---

## 3. Proposed QUALITY Criterion (Exact Text)

Criterion 93 is warranted to close this standing gap. It synthesizes the lessons of Round 42 (where partial patching created debt), Round 43 (where probe coordinates drifted), Round 44 (where unrepinned anchor sweeps broke adjacency), and Round 45 (where C1 pinned `lexical_hits == 0` with pre-data controls and declared limits, and C2 pinned exhaustive grounding and counter projection checks):

```markdown
93. **A fix to a defect class sweeps every site across the scored surface and pins the sweep command (R42-C1-CLASS-UNSWEPT):** when an operability claim, repair, or lesson addresses a named defect class on a code or tool surface (an early-reader pipeline under `pipefail`, an unhandled exit code, an unescaped variable, or an unrepinned anchor), the implementation sweeps every site of that class across the entire affected surface, rather than patching only the sites where failures were observed; the counter or gate pins an automated sweep check (such as a lexical search, AST check, or static rule) asserting zero remaining unhandled occurrences in production code; any site intentionally excluded from the sweep is explicitly enumerated by name and coordinate in the declaration with its technical rationale as a recorded limit; and the frozen pre-data controls include a variant that leaves at least one unhandled site of the class intact or evades the sweep pattern, which must read below the target. Failing example: in round 42, C1 claimed the `R41-CENSUS-PIPEFAIL-692` early-reader defect class ("never `printf | grep -q` / `| grep -m1` / `| head` under pipefail on a probe buffer") but patched only the packages plane (`:692`) and update-safety plane (`:1621-1652`), leaving five single-line production readers (`$CAP_OUT | head -n1`) in `tools/tsukuroi-census.sh` un-swept (`corpus/lessons/round-42.md` Mistakes `R42-C1-CLASS-UNSWEPT`, `Captured-by: none`), where they survived as latent exit-141 failure sites through rounds 43 and 44. Shown able to fail: round 45 C1 counter `tools/score-census-readers-r45.py` pins `lexical_hits == 0` (zero lines matching `"$CAP_OUT" | head` outside `run_selftest`), requires all five sites converted (`sites_found == 5`), and refuses pre-data control K1 (`| head -1` evasion) with `lexical_hits: 5` (`battery-summary-c1.jsonl`); the seven masked readers are declared as recorded limits; and C1's `adjacency_ok` kill rule refuses unrepinned anchor drift (control K7). Cross-claim analog: round 45 C2 sweeps and grounds all three round-44 `[inference]` marks (GR1, GR2, GR3) on pinned upstream sources, and enforces exhaustive checks against duplicate keys (C2-K23), duplicate registry rows (C2-K21), gutted quotes (C2-K20), and orphan repos (C2-K25). Lesson: `corpus/lessons/round-42.md` Mistakes `R42-C1-CLASS-UNSWEPT` (captured-by: none; routed to round 43/45); `corpus/lessons/round-45.md`.
```

---

## 4. Second-Order Effects Across Surfaces

Adopting proposed criterion 93 enforces rigor across four operational surfaces:
1. **Runtime Surface:** Directly eliminates latent production crashes. In `tools/tsukuroi-census.sh`, having five production readers taking `$CAP_OUT | head -n1` meant that any host with large systemd status lines, large timer results, or verbose nvidia-smi outputs could suddenly crash the census with exit 141 under `set -euo pipefail`. Sweeping all sites guarantees host-wide operability invariance.
2. **Contract & Declaration Surface:** Eliminates "silent debt." If an integrator cannot sweep all sites (for example, the seven masked readers in `tsukuroi-census.sh`), they cannot quietly ignore them; the criterion forces them into the declaration's "Recorded limits" table. This keeps the claim honest and verifiable.
3. **Substrate & Tooling Surface:** Standardizes counter construction. A counter evaluating an operability or refactoring claim cannot rely solely on positive cases or metamorphic twins; it must implement a static/lexical sweep gate (such as `check_lexical()` in `score-census-readers-r45.py`) that audits the full source tree.
4. **Verification & Control Surface:** Pre-data control batteries must demonstrate sensitivity to partial sweeps. Controls like `C1-K1` (evasion / partial sweep) and `C1-K4` (cases without conversion) prevent vacuous passes where a counter tests only the converted sites while ignoring untouched sister sites.

---

## 5. Risks, Tradeoffs, and Boundaries

- **Risk of Over-generalization:** A naive objection might argue that requiring an "exhaustive sweep" prevents small, focused bug fixes. Proposed criterion 93 avoids this by scoping strictly to a **named defect class**—a recurring syntactic or semantic pattern identified in a claim, lesson, or audit. A unique, one-off logic bug at a single site does not constitute a defect class.
- **Safety Valve for Legitimate Exclusions:** The criterion does not demand that every conceivable variant be rewritten immediately if there are technical reasons not to (e.g. masked readers where SIGPIPE is ignored via `|| true` or where stdout is piped to a process substitution). It requires that any such un-swept sites be explicitly disclosed as recorded limits in the declaration, preventing them from being swept under the rug.
- **Independence from Execution Channels:** Static sweep checks and pre-data evasion controls are deterministic, fast, and hermetic. They do not depend on fragile live host states or long timeouts.

---

## 6. Execution Disclosure

This seat performed read-only evidence verification and analytical synthesis:
- No lane files, tracked files, or git refs were modified or staged.
- No subagents were spawned.
- No counters or batteries were executed (all results cited from committed pre-data receipts and frozen artifacts).
- Report written directly to `.ufo/waves/round-45/a2w1/ConnClaims.md`. Small receipts were unnecessary as all cited outputs already exist in `.ufo/waves/round-45/controls/`, `.ufo/waves/round-45/controls-a2/`, and `.ufo/waves/round-45/before/`.