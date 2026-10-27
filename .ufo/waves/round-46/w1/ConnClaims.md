VERDICT: draft

# Item X-1: Cross-Claim Synthesis and Proposed QUALITY Criterion (ConnClaims)

## 1. Axes of Analysis
- **Axis 1 (Cross-Claim Synthesis & Discernment):** Recognizing the unified invariant across runtime self-identity (C1) and reviewer admission (C2) — the necessity of cryptographic binding between an evaluative attestation and the exact executed/read bytes.
- **Axis 2 (Corpus Consistency & Gap Precision):** Evaluating the criteria progression in `corpus/QUALITY.md` (specifically 80-93) to prove that content-digest binding is an unstated, distinct invariant not covered by existing rules.
- **Axis 3 (Empirical Grounding & Falsifiability):** Anchoring the proposed criterion in verified repository evidence: commit history (`0503400b`), round-45 lessons, and pre-data battery controls (`battery-summary-c1-draft1.jsonl:3`, `battery-summary-c1.jsonl:3`, `battery-summary-c2.jsonl:6,9`).
- **Axis 4 (Host Guard & Non-Harm):** Preserving read-only lane discipline, operating without subagents, and avoiding unnecessary abstractions or regressions.

## 2. Evidence and Cross-Claim Analysis

### A. The Core Invariant: Binding Assertions to Content Bytes
Both round-46 claims converge on eliminating **content-decoupled attestation**:
1. **C1 Runtime Execution Identity (`tools/tsukuroi-census.sh --identity`):**
   - The census emits an identity assertion (`TSUKUROI_CENSUS_IDENTITY: ... sha256=<hex> ... verified=yes`).
   - If the identity mechanism relies on the ambient file path (`$SELF` / `$0`), an adversary or race condition (a file replaced on disk after bash opens it) decouples the hash from the bytes bash executes.
   - S250 (`shell.c:1586,1700`, `general.c:690-700`) pins that bash opens the script and moves the descriptor to a high fd (typically fd 255).
   - S251 (`proc_pid_fd.5.html:75`) establishes `/proc/$$/fd/<n>` as the authoritative reference to the open inode.
   - Grounding: Draft 1 of the C1 counter passed control `K2-pathhash` (`battery-summary-c1-draft1.jsonl:3`), because it did not test the replaced-after-open case. The final counter added `mv -f $R46_DECOY $R46_PATH` in `unverifiable_ok`, properly failing `K2-pathhash` (`battery-summary-c1.jsonl:3`).
2. **C2 Reviewer Verdict Admission (`tools/check-scrub-admission-r46.py`):**
   - A counted reviewer or critic seat emits an admission verdict (`ROW GR<n> VERDICT: holds`).
   - If the verdict references only the row label (`GR2`), an author or integrator can mutate, narrow, or rewrite the row text post-review without invalidating the verdict.
   - Round-45 history: At commit `18389f44`, GR2 section hash was `23adf569...`. Wave `a2w1` counted seats read this text and returned `partly`. At integration `0503400b`, the statement and host reading were narrowed (section hash changed to `3534461d...`), and narrowed again at `cd1b3a03` (section hash `a963df81...`). No counted seat ever evaluated the narrowed text; it was only read by uncounted residual seats (`a2r1/ResRevGR2`, `ResCritGR2`). Because round-45 lacked content-digest binding, the gate evaluated verdict files nominally.
   - Round-46 C2 addresses this by enforcing `SECTION SHA256: <hash>` on line 2 of the seat report, requiring `hash == cur` in `tools/check-scrub-admission-r46.py:238-242`. Controls `C2-K5-stale-hash` (all-zeros or stale hash) and `C2-K8-fails-old-hash` verify that mismatched hashes fail admission (`row_ok: false`).

### B. Gap Analysis Against QUALITY 80-93
Review of `corpus/QUALITY.md` confirms that no existing criterion mandates cryptographic content binding for verdicts:
- **QUALITY 80 (R31-DEPTH-UNFALSIFIABLE):** Requires do-nothing controls and novelty swept as facts before data; does not govern reviewer verdict bindings.
- **QUALITY 81 (R31-SCRIPTED-NONREADER):** Requires non-author reviewer verdict files, but only regulates verdict format (`holds|partly|fails` with checked source lines). It does not bind verdicts to content digests.
- **QUALITY 82-86:** Govern behavioural fixture isolation, conjunct grounding, token validation, mount namespace leak prevention, and upstream source provenance.
- **QUALITY 87 (R39-CONTENT-UNREAD):** Mandates that content counters inspect rule cells directly; governs the counter's own parser, not reviewer or script attestations.
- **QUALITY 88-90:** Govern declaration parameters, adversarial guard evasion, observation channels, and asserted lines versus mentions.
- **QUALITY 91 (R42-ADOPTED-UNREAD):** Requires an integrator to verify proposed text against source lines and notes that "a counted read follows every adopted change." However, this is an operational process instruction; it establishes no mechanical binding contract, no hash header requirement, and no programmatic counter enforcement.
- **QUALITY 92 (R43-CAP-HEADER-DUP):** Governs table header row counts.
- **QUALITY 93 (R45-C2-BINDING-CHANNEL):** Requires that counted verdicts bind through a channel the seat writes verbatim (seat report vs orchestrator results file) and scores actual yield shapes. This secures the *channel of transmission*, but remains silent on the *semantic content* being judged. Under QUALITY 93 alone, a verbatim report stating `ROW GR2 VERDICT: holds` binds successfully even if row GR2 was altered after the seat read it.

Conclusion: A new criterion is warranted to close the gap between transmission-channel fidelity (QUALITY 93) and semantic content verification.

## 3. Proposed Move: QUALITY 94 Draft Text

```markdown
94. **A verdict or identity statement names the exact content digest it evaluated, and an admission gate credits it only when that digest matches the scored revision (R46-VERDICT-CONTENT-DIGEST):** when a claim's predicate admits an artifact based on a reviewer verdict or a runtime self-identity assertion, the statement names the cryptographic digest (SHA-256) of the exact content evaluated or executed — a seat report declares on its second line the digest of the text section it read, and an executing script hashes the bytes delivered through its open file descriptor rather than trusting an external path. A counter credits a verdict only when its declared digest matches the digest of that section or file at the measured revision, and pre-data controls include both a stale-digest control and a path-decoupled control that fail. Failing examples: in round 45, row GR2 was narrowed at integration (`0503400b`) after counted seats had read the initial text and returned `partly`; no counted seat read the narrowed text, but the unhashed verdict structure could not mechanically detect the divergence (corpus/lessons/round-45.md ## Mistakes R45-C2-GR2-HOST-READING). In round 46 C1 pre-freeze controls, draft 1 of `score-census-identity-r46.py` passed `C1-K2-pathhash` (`battery-summary-c1-draft1.jsonl:3`) because it lacked a test for a script replaced on disk after bash opened it.
```

## 4. Second-Order Effects
- **Runtime Surface:** Scripts asserting self-identity must access their execution descriptor (`/proc/$$/fd/<n>`) and verify matching inodes rather than relying on path resolution (`$0` or `$SELF`).
- **Contract Surface:** Reviewer and critic report formats require an explicit content-digest field (`SECTION SHA256: <64 hex>`) immediately following the verdict line.
- **Substrate Surface:** File replacements, asynchronous disk mutations, or post-review commit amendments cannot cause a verdict to be credited to unreviewed bytes.
- **Verification Surface:** Admission counters must compute revision section hashes independently and match them against reported hashes (`s['hash'] == cur`). Pre-data control batteries must incorporate stale-hash mutants (`C2-K5`) and path-decoupling mutants (`C1-K2`).

## 5. Risks and Verification
- **Risks:** Fragility to non-semantic formatting edits (e.g., whitespace adjustments or comment fixes altering the section SHA256 and invalidating valid reviews). Mitigated by defining clear section boundaries (e.g. from `## <ID>` up to the next `## `).
- **Verification:** Verified against round-46 control batteries:
  - `python3 tools/check-scrub-admission-r46.py --revision 2042117cfb724170772f4c128cc2ddba0b61d817 --section-hash` correctly extracts section hashes across GR1, GR2, and GR3.
  - `battery-summary-c2.jsonl` confirms that `C2-K5-stale-hash` and `C2-K8-fails-old-hash` fail as expected.
  - `battery-summary-c1.jsonl` confirms that `C1-K2-pathhash` fails as expected under `unverifiable_ok`.
- Receipts stored in `.ufo/waves/round-46/w1/ConnClaims/`:
  - `c1-c2-digest-binding-comparison.txt`
  - `quality-gap-audit.txt`
