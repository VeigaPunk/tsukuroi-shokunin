VERDICT: supports

# ConnWave — Cross-Lane Pattern Scan: Verdict Binding Channels

**Seat:** ConnWave (L2 leaf, tsukuroi-shokunin lane, round 47, wave w1)  
**Item:** F-10. Cross-lane pattern scan (read-only): verdict binding channels across sibling lanes  
**Judged on:** depth, pattern  
**Milestone:** cross-lane pattern  
**Receipts:** `.ufo/waves/round-47/w1/ConnWave/receipts.txt`  

---

## 1. Executive Summary: The Fleet's Binding Channel Taxonomy

Across the 12 active shokunin lanes, the architectural problem of binding counted reviewer verdicts to seat output has evolved into two primary competing paradigms, complemented by two specialized domain-specific variants:

1. **Committed Semantic Self-Binding (Tsukuroi R46–R47, Kotodama R60):**  
   Verdicts are bound entirely within committed Git repository state (`<wave>-dispatch.json` + `<wave>-results.json` + `<wave>/<seat>.md`). The seat's report header is strictly structured (`ROW <id> VERDICT: <verdict>` on line 0, `SECTION SHA256: <hash>` on line 1). The counter cryptographically couples the verdict to the exact byte extent of the judged object at `<revision>`, verifies citations against pinned digest-checked source snapshots, and enforces pairwise distinct report bodies.
2. **Host-Execution Multi-Witness Authentication (Kumitate R63, Tsukuroi R42–R44 legacy):**  
   Verdicts are bound across three heterogeneous surfaces: committed repo state, an append-only orchestrator dispatcher log, and ephemeral host session transcripts (`~/.omp/agent/sessions/**/<Seat>.jsonl`). Structural ratchets (K63) inspect the subagent lifecycle (tool joins, row graph, timestamp spreads, template diversity) to mathematically prove physical execution.
3. **Deterministic Machine-Oracle Rerun (Kaidoku R40–R42):**  
   Bypasses human/LLM consensus entirely. Claims are proven by deterministic binaries (e.g. SquashFS superblock parsers, REA firmware extraction reruns, bitwise carrier carving) rather than counted peer verdicts. Wave ledgers use presence-only checks (`ledger-status.py`).
4. **Canonical Dispatch Payload Hashing (Mori R18–R48):**  
   Serializes and hashes `{"context": context, "tasks": tasks}` into a canonical `payload_sha256`, verifying an append-only state transition ledger against committed tree blobs.

---

## 2. Concrete Fleet Evidence: Paths, Mechanics, and Invariants

### A. Tsukuroi-Shokunin: Semantic Anchoring and Cold Hermeticity
- **Path:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r47.py`
- **Evolutionary Trajectory:**
  - In Round 42 (`check-scrub-record-r42.py:119-149`), Tsukuroi bound verdicts by requiring the verdict token in `w2-results.json`'s `output` string, matching it in the report, and verifying `transcript_has()` against uncommitted host files in `~/.omp/agent/sessions/-Projects-shokunin/`.
  - In Rounds 43–45 (`check-scrub-record-r43.py:42`, `r44.py:47`, `r45.py:62`), host transcript checking was explicitly demoted from the predicate to an uncommitted diagnostic: *"Reported outside the predicate: transcripts_bound (... host-local, uncommitted, cannot tell forged committed records from real ones)"*.
  - In Rounds 46–47 (`check-scrub-admission-r47.py:178-226`), Tsukuroi established the fleet's strictest committed semantic binding channel:
    - **Dispatch & Results Agreement (`bind()` lines 180-201):** Seat must be dispatched exactly once in the round's `*-dispatch.json` with matching role, and appear exactly once in `*-results.json`.
    - **Rigid Report Header (`lines 209-217`):** Line 0 must be `ROW (GR\d) VERDICT: (holds|partly|fails)`; Line 1 must be `SECTION SHA256: ([0-9a-f]{64})`.
    - **Extent Boundary (F1, `lines 131-164`):** Extent bounded strictly from `## GR<n>` to the expected next header (`## GR2`, `## GR3`, `## How this changes OS triage`); fails closed on any internal `## ` line or duplicate header.
    - **Anti-Contradiction Sweep (`lines 218-220`):** Body must contain no conflicting `ROW GR<n> VERDICT: <word>` lines.
    - **Citations & Snapshot Resolution (K22, `lines 241-295`):** Report body (>= 300 bytes) must cite row sources (`file:line`), and every cited line must resolve inside digest-pinned snapshot files (`SNAPSHOTS`: S237, S242, S243, S244, S246, S247, S248, S249).
    - **Anti-Plagiarism / Diversity (K23, `lines 348-356`):** `distinct = len(set(bodies)) == len(bodies) == len(on_cur)` — every bound report body must have a unique SHA256 digest.

### B. Kumitate-Shokunin: Host Execution Authentication
- **Path:** `/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/inline-dispatch-evidence.mjs`
- **Mechanics (`lines 1-60, 260-440`):**
  - **Tri-Partite Binding:** Refuses to trust repo contents alone because *"The lane can write every file under its own `.ufo/waves/round-N/` itself"*.
  - **Transcript Verification:** Scans `<sessions-root>/**/<Seat>.jsonl`. Verifies user prompt contains `# Seat <name>`, context head (200 chars), and task tail (120 chars).
  - **Structural Ratchet (K63):** Enforces five structural arms on the JSONL transcript:
    1. `SESSION_HEADER`: validates `session_init` with tools, `model_change` with `subagent:<stem>`, system-prompt digest.
    2. `SESSION_TOOL_JOIN`: tool calls matched by `toolResult`, `toolName` matches, max 1 unanswered call beyond `yield`.
    3. `SESSION_ROWGRAPH`: >= 10 rows, >= 2 assistant messages, parentId graph resolving internally.
    4. `SESSION_TIMELINE`: >= 8 distinct ISO timestamps spanning >= 120s.
    5. `SESSION_TEMPLATE`: normalized transcript body must not collide with another seat (rejects cloned sessions).
  - **Dead Seat Accounting (`lines 370-377`):** Unfinished seats (transcript present but no `yield`/`session_exit`) must be explicitly named in the wave report (`DEAD_UNNAMED`).

### C. Kaidoku-Shokunin: Deterministic Oracles and Presence Checks
- **Paths:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-42/prefile-gate.py`, `tools/round-40/ledger-status.py`, `tools/round-42/c1-counter.py`
- **Mechanics:**
  - `prefile-gate.py:154-185`: Validates `.ready` and `.ready.dispatched` markers; raises advisory warnings if `results.json` entries < declared dispatch seats.
  - `ledger-status.py:1-41`: Designed for orchestrator defect R39-CL6 (`status: null` in `results.json`). Discovers reports via JSON keys, `Report:` trailers, or `<wave-dir>/<name>.md`. Classifies status (`ok`, `no-report`, `empty-report`) purely on **file presence and non-whitespace**. Explicitly notes: *"It never reads the report's content beyond the whitespace test and never judges a seat's work"*.
  - Claim evaluation (`c1-counter.py:1-50`): Uses independent binary extractors (`sasquatch`, `unblob`), superblock bit parsing, and sha256 carrier pins. Does not rely on peer reviewer consensus.

### D. Kotodama-Shokunin: Judged-Object Identity via External Keys
- **Path:** `/home/vgpnk/Projects/shokunin/kotodama-shokunin/tools/check-judged-object.py`
- **Mechanics (`lines 1-45`):**
  - Solves the Round-59 failure (post-verdict narrowing: entry edited after reviewers judged it).
  - Reads `planted-key.json` containing `entry_sha256` and `cited_ids`. Uses `git show <rev>:<entry>` to ensure the committed entry byte hash matches what the reviewers evaluated.

### E. Mori-Shokunin: Dispatch Payload Hashing and Unlanded Worktree Guards
- **Paths:** `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-dispatch-ledger.py`, `tools/mori-unlanded-check.py`
- **Mechanics:**
  - `mori-dispatch-ledger.py:120-165`: Normalizes dispatch JSON `taskCall` (`context` + `tasks`) and computes `payload_sha256`. Verifies ledger state transitions (`refused` | `started` | `partial`) with strictly increasing timestamps.
  - `mori-unlanded-check.py:1-40`: Solves mistake M1 of Round 48 (late seat reports and `w2-results.json` left untracked on disk while the round closed). Fails if any wave artifact is dirty or untracked in the git working tree.

---

## 3. Comparative Channel Analysis: Trade-offs Across Surfaces

| Criterion | Channel A: Committed `results.json` + Report Headers (Tsukuroi R47) | Channel B: Host Transcripts + Dispatcher Logs (Kumitate R63) | Channel C: External Keys / Ledgers (Kotodama / Mori) | Channel D: Presence-Only Ledgers (Kaidoku R40) |
| :--- | :--- | :--- | :--- | :--- |
| **Cold Reproducibility** | **Total (Hermetic).** Evaluates on any machine, fresh clone, or CI at any historical git revision. | **Zero.** Fails immediately if `~/.omp/agent/sessions/` is cleaned, compacted, moved, or run off-host. | **Total (Hermetic).** Fully committed inside repository tree. | **Total (Hermetic).** Relies only on committed files. |
| **Semantic Integrity** | **Extreme.** Line 1 `SECTION SHA256` binds the verdict directly to the exact byte slice reviewed. Post-verdict edits fail closed. | **None.** Verifies session prompt contained task text, but cannot verify whether the seat reviewed current or stale bytes. | **High.** Key file binds entry SHA256, but requires maintaining separate JSON key. | **Zero.** Accepts any non-whitespace text regardless of content or meaning. |
| **Anti-Forgery (Subagent Authenticity)** | **Strong (via K22 + K23).** While repo files could theoretically be written by L1, K23 distinct bodies and K22 snapshot citation proofs make fabrication expensive. | **Extreme.** Mathematically proves physical execution via session headers, tool joins, row graphs, and timing spreads. | **Moderate.** Proof of dispatch payload identity, but not of execution validity. | **Zero.** Highly vulnerable to placeholder files and synthetic reports. |
| **Operational Fragility** | **Minimal.** Plain git objects. No reliance on daemon logs or local socket paths. | **High.** Breaks when subagents run with different prompt formatting, compact transcripts, or prune session directories. | **Moderate.** Risk of desynchronization between key files and entry files. | **Minimal.** Trivial regex and stat calls. |

---

## 4. Which Pattern is Stronger?

Neither pattern is universally stronger across all axes; their strength depends strictly on the **threat model** being addressed:

- **When the threat is post-verdict semantic drift or ungrounded claims:**  
  **Tsukuroi's Pattern is Vastly Superior.** Kumitate's transcript verification is blind to semantic validity: an agent can execute 100 tool calls over 10 minutes (passing Kumitate K63) while evaluating an obsolete draft or reaching an invalid conclusion. Tsukuroi's `SECTION SHA256` in line 1 guarantees that every counted vote is cryptographically bound to the exact row bytes that land in the repository.
- **When the threat is L1 synthesizer forgery (simulating a wave without dispatching subagents):**  
  **Kumitate's Pattern is Stronger.** Kumitate binds the wave to host-level artifacts that cannot be generated from within the repository git index alone.
- **Resolution for Tsukuroi:**  
  Tsukuroi's historical move (R43–R45 demoting `transcript_has`, R46–R47 elevating `SECTION SHA256` + K22 + K23) was **the correct architectural evolution**. In a decentralized multi-agent system, **hermetic reproducibility of the git object store is paramount**. By introducing K22 (snapshot citation resolution) and K23 (pairwise body distinctness), Tsukuroi effectively blocked L1 template-forgery while preserving 100% cold git reproducibility.

---

## 5. What Tsukuroi Lane Should Take and Avoid

### What Tsukuroi Should Take:
1. **Kumitate's Dead-Seat Accounting (`DEAD_UNNAMED`):**  
   In `kumitate-shokunin/scripts/inline-dispatch-evidence.mjs:370-377`, if a seat is dispatched but does not cleanly yield a report, the gate requires the wave closeout report to explicitly enumerate it as dead. In Tsukuroi's `check-scrub-admission-r47.py:180-201`, non-voting or unbindable seats simply fail to increment `bound_on_current`. Tsukuroi should take Kumitate's invariant: require the L1's wave summary or scorecard to explicitly account for every dispatched seat that dropped out or timed out.
2. **Mori's Unlanded Worktree Guard (`mori-unlanded-check.py`):**  
   Mori prevents the fatal mistake where wave artifacts sit untracked on disk while the round closes. Tsukuroi's counter checks committed git blobs via `git show <rev>:...`, but a pre-filing gate (`tools/check-unlanded-r47.sh`) running `git status --porcelain=v1` before commit would guarantee no residual seat report or results JSON is accidentally abandoned in the worktree.
3. **Mori's Canonical Dispatch Payload Normalization:**  
   In `mori-shokunin/tools/mori-dispatch-ledger.py:152-164`, normalizing `taskCall` JSON into a canonical `payload_sha256` provides an immutable anchor for the dispatch phase, preventing subtle drift in prompt text across wave generations.

### What Tsukuroi Should Avoid:
1. **AVOID Gating the Frozen Counter on Host Transcripts (`~/.omp/agent/sessions`):**  
   Kumitate's hard requirement for local JSONL session files breaks cold reproduction, prohibits running counters on remote or secondary clones, and fails once the host session store is pruned. Tsukuroi was right to remove `transcript_has` from its admission predicate in R45. It should remain strictly an informational advisory, never a gate condition.
2. **AVOID Kaidoku's Presence-Only Classification (`ledger-status.py`):**  
   Checking that a report exists and is non-empty is completely inadequate for grounding and admission claims. It invites empty compliance and vacuous holds. Tsukuroi must retain its strict line 0 / line 1 regex requirements.
3. **AVOID Kotodama's Centralized Key Files (`planted-key.json`):**  
   Kotodama centralizes the judged object hash into an auxiliary JSON packet key. Tsukuroi's approach—embedding `SECTION SHA256: <hash>` directly into line 1 of each reviewer's report—is far cleaner, completely decentralized, and makes every seat's report a self-authenticating cryptographic receipt.
