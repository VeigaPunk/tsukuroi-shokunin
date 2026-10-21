# CrossNoHarm — Cross-Claim No-Harm Review and Synthesis

**Seat:** `TsukuroiR19Recovery.CrossNoHarm`  
**Role:** UFO-FSD Connector  
**Round:** Tsukuroi round 20, attempt 1 (`TsukuroiR20`)  
**Baseline:** `0cbc34dd6b20896085a8fb07943e3ea4027d8472`  
**Lane:** Production lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`  
**Report Destination:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/falsify/CrossNoHarm.md`  
**Mode:** NO-EXEC (read/grep/glob and named report write only; zero subprocesses, shell/eval, host probes, tests, or code edits)  

---

## 1. Declared Axes and Contract Scope

The round's declared axes and contract metrics (per `.ufo/waves/round-20/preregister.json:4-29` and `SCORECARD.md:614-625`):

1. **C1 Adjacency** (ordinal 8, tied-lowest axis with depth; ordinal delta 0):
   - Metric: `ownership_corrections` (before: 0, after: 1).
   - Evaluator: `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`.
   - Scope: Explicit sibling-declaration wording for OUT-009 in `PROVINCE.md:148-152` at retained pinned scope (`cf02419276e5`), with zero integrator arbitration or write authority.

2. **C2 Operability** (ordinal 9; ordinal delta 0):
   - Metric: `object_selector_tools` (before: 0, after: 9).
   - Evaluator: `python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors`.
   - Scope: Original-nine consumer continuity under object-only hexadecimal selector tests; discovered tools separate. Supporting repair: execution-log `systemctl` mutation filter (`systemctl_violations` in `tools/check-recheck-commands.py`).

3. **C3 Calibration** (ordinal 9; ordinal delta 0):
   - Metric: `audit_live_map_errors` (before: 1, after: 0).
   - Evaluator: `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map`.
   - Scope: Operative `boot-chain-audit` live summary map returns `0 CONSISTENT` or `2 UNKNOWN`; `1` is selftest failure only, never live `DEGRADED`. Append named disclosures (`R20-FALSE-OPERATIVE-MAP` and `R20-SKILL-PREFIX-EXCEPTION`).

All ordinal deltas remain strictly 0; genuine within-round metric improvements within bounded claims, with no claims of host or boot safety.

---

## 2. Cross-Claim No-Harm Review

### 2.1 Default Modes and Count Schema Isolation

A critical requirement of non-regression is that candidate tools invoked without round-20 feature flags must behave identically to baseline and preserve exact backward compatibility with round-19 verification harnesses:

1. **`tools/check-registry-coverage.py`:**
   - In baseline (`tools/check-registry-coverage.py:281-292`), the evaluator takes `--revision <REV> --baseline-tools <BASE>`.
   - In candidate `/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:350-355`, `--audit-live-map` is isolated cleanly:
     ```python
     findings, covered = _coverage(rows, tools, reader, binding.sha)
     map_findings = _audit_live_map(rows) if args.audit_live_map else []
     findings.extend(map_findings)
     counts = _base_counts(len(tools), len(rows), len(covered), len(findings))
     if args.audit_live_map:
         counts["audit_live_map_errors"] = len(map_findings)
     ```
   - When run in default mode (as in `measure/run.py:81` for `registry-coverage`), `args.audit_live_map` is false; `counts` retains the exact R19 key set (`baseline_tools_missing`, `baseline_tools_total`, `discovered_tools`, `findings`, `missing`, `registered`, `rows_total`, `tools_total`; matching `.ufo/waves/round-19/measure/final/c3-after.stdout:1`). `audit_live_map_errors` is never leaked into default output.

2. **`tools/check-revision-binding.py`:**
   - In candidate `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:635-710`, `measure()` isolates `object_selectors`:
     ```python
     if object_selectors:
         selector_count = sum(1 for item in named if item.get("object_selector_ok"))
         result.update({
             "object_selectors_requested": True,
             "object_selector_tools": selector_count,
             "object_selector_total": TOTAL,
             "object_selector_status": "PASS" if selector_count == TOTAL else "FAIL",
             "object_selector_per_tool": named,
         })
     ```
   - When run in default mode (as in `measure/run.py:79` for `original-nine-continuity`), `object_selectors` is false. The returned dictionary retains the exact legacy keys without polluting the output with `object_selector_*` counters.

3. **`tools/check-recheck-commands.py`:**
   - In candidate `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:62,812`, `DEFAULT_FORBID` is defined as:
     `("pacman", "checkupdates", "yay", "paru", "mkinitcpio", "limine-update")`.
   - `systemctl` is **not** included in `DEFAULT_FORBID`.
   - When run in default mode across `corpus/knowledge/*.md` (as in `measure/run.py:93` for `recheck-corpus`), knowledge entries with valid read-only `systemctl` commands in their recheck procedures (`systemd-user-plane.md:234-239`, `journal-boot-plane.md:261-288`, `root-dac-correction-r13.md:3`, `boot-plane.md:264-281`) evaluate cleanly.

4. **Defect Identified — `tools/check-adjacency-anchors.py` Schema Leak:**
   - In baseline `tsukuroi-shokunin/tools/check-adjacency-anchors.py:208-217`, `_empty_counts()` returned 8 keys:
     `outbound_total`, `outbound_portable`, `inbound_total`, `inbound_classified`, `inbound_by_class`, `inbound_by_scope`, `live_object_checked`, `live_object_match`.
   - In candidate `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:363-374`, `_empty_counts()` unconditionally includes:
     `"ownership_corrections": 0`.
   - Consequently, running the tool in default mode without `--ownership-corrections` (as executed in `measure/run.py:83` for `adjacency-legacy`: `python3 tools/check-adjacency-anchors.py --revision <TARGET>`) emits an unrequested extra field `"ownership_corrections": 0` in `counts`.
   - This creates an asymmetrical schema mutation between baseline and target runs of the legacy check, unlike the strict key isolation maintained by C2 and C3.

---

### 2.2 R19 Behavior and Historical Captures

In round 19, the retained execution log `host-capture-r19.txt` recorded 6 `systemctl` invocations (`.ufo/waves/round-19/l1-capture/host-capture-r19.txt`):
- Line 153: `$ systemctl cat limine-snapper-sync.service --no-pager`
- Line 191: `$ systemctl list-unit-files --no-pager "limine*" "snapper*"`
- Line 208: `$ systemctl show limine-snapper-sync.service -p UnitFileState -p TriggeredBy -p WantedBy -p After -p Requires --no-pager`
- Line 215: `$ systemctl list-dependencies --reverse --no-pager limine-snapper-sync.service`
- Line 220: `$ systemctl cat snapper-cleanup.timer snapper-cleanup.service --no-pager`
- Line 262: `$ systemctl list-timers --all --no-pager "snapper*"`

In round 19 evaluation (`.ufo/waves/round-19/measure/final/recheck-exec-log-r19.stdout:1`), this log passed with:
`{"clean_count": 23, "exec_violation_count": 0, "file_count": 39, "findings": [], "flagged_count": 0, "forbidden": ["pacman", "checkupdates", "yay", "paru", "mkinitcpio", "limine-update"], ... "status": "PASS"}`.

In early round-20 candidate drafts, `list-dependencies` and `--reverse` were omitted from the allowlist (documented in build reports `ExecReadOnly.md:5` and `ExecMutating.md:9`). Had this gap remained, line 215 would have triggered `EXEC-STEER-VIOLATION`, causing `measure/run.py:95` (`exec-log-r19`) to regress from PASS to FAIL.

In candidate `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:276-282`:
- `list-dependencies` is present in `SYSTEMCTL_READ_VERBS`.
- `--reverse` is present in `SYSTEMCTL_READ_FLAGS`.
- Value-taking option parsing (`SYSTEMCTL_VALUE_FLAGS:283-285`) correctly consumes properties after `-p` without consuming following flags or tokens.
- All 6 captured commands evaluate to `_systemctl_read_only(args) == True`.
- In `host-capture-r19c.txt:32`, the mutating command `COMMAND=/usr/bin/systemctl enable --now snapper-timeline.timer snapper-cleanup.timer` is a sudo journal entry, not a line starting with `$ `. `assess_exec_log:659` checks only `line.startswith("$ ")`, correctly ignoring passive journal output.
- Thus, R19 capture compatibility is preserved with `exec_violation_count = 0`.

---

### 2.3 Generic Systemctl Forbid vs. Finite Exec-Log Policy

A critical architectural distinction exists between **generic binary forbid policy** and **semantic exec-log filtering** in `check-recheck-commands.py`:

In `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:654-668`:
```python
def assess_exec_log(path, text, forbid):
    findings, hits = [], 0
    for number, line in enumerate(text.splitlines(), 1):
        if not line.startswith("$ "):
            continue
        found = invocations(line[2:], forbid)
        if "systemctl" not in forbid:
            found.extend(systemctl_violations(line[2:]))
        if found:
            hits += len(found)
            findings.append(Finding("EXEC-STEER-VIOLATION", f"{path}:{number}",
                                    "executed command invokes " + ",".join(sorted(set(found)))))
    return findings, hits
```

1. **Separation and Orthogonality:**
   - When `--forbid systemctl` is explicitly passed by an operator:
     - `"systemctl" in forbid` is true.
     - `invocations(line[2:], forbid)` matches **every** `systemctl` invocation (both read and mutate).
     - Line 662 checks `if "systemctl" not in forbid:`. Since `"systemctl"` is in `forbid`, `systemctl_violations` is bypassed, preventing double-counting of the violation on the same line.
     - Selftest at `:1493-1496` confirms this behavior: under `--forbid systemctl`, all 18 commands in `systemctl_green` are flagged with `exec_violation_count = 18`.
   - When `--forbid` is left at default (`DEFAULT_FORBID`):
     - `"systemctl"` is not in `forbid`.
     - `invocations` does not flag `systemctl`.
     - Line 662 executes `systemctl_violations(line[2:])`, which queries `_systemctl_read_only(args)`. Read-only forms pass cleanly (0 hits); mutating verbs (`restart`, `enable`, `daemon-reload`) and unknown verbs emit `EXEC-STEER-VIOLATION`.

2. **No-Harm Guarantee:**
   - Keeping `systemctl` out of `DEFAULT_FORBID` prevents breaking knowledge-plane recheck procedures.
   - Guarding line 662 ensures explicit CLI flags behave predictably without double-counting.

---

### 2.4 Ordinal Deltas and the Lowest-Axis Invariant

In `preregister.json:4-29` and `SCORECARD.md:616-622`:
- **C1 Adjacency:** ordinal 8 → 8 (delta 0). Lowest axis.
- **C2 Operability:** ordinal 9 → 9 (delta 0).
- **C3 Calibration:** ordinal 9 → 9 (delta 0).

Why all ordinal deltas must remain strictly 0:
1. `SCORECARD.md:82,249,481` establishes that Tsukuroi maintains an ordinal ranking across six axes: depth (8), adjacency (8), coverage (9), operability (9), freshness (9), calibration (9).
2. Adjacency and depth are tied-lowest at 8. Under canonical UFO-FSD discipline, work must focus on or advance the lowest axis. C1 directly addresses adjacency.
3. Ordinal scores reflect broad capability and architectural tiers, not counts of passing unit tests or individual markdown errata. Converting a finite count (e.g. `ownership_corrections` 0→1, `object_selector_tools` 0→9, `audit_live_map_errors` 1→0) into an ordinal bump would constitute ungrounded score inflation.
4. Keeping ordinal deltas at 0 guarantees that no claim makes an overclaim of global capability uplift, keeping all six axes strictly comparable across rounds 19 and 20.

---

### 2.5 Cross-Claim Interactions and Potential Incomparabilities

Examining cross-claim dependencies across the four candidate worktrees reveals three key interaction surfaces:

1. **Shared Substrate: `tools/_revision.py`:**
   - C2's primary deliverable is object-ID-first resolution in `tools/_revision.py:112-147` (`_object_commit`).
   - `_revision.py` is imported by all gates: `check-adjacency-anchors.py` (C1), `check-registry-coverage.py` (C3), and the other seven original consumers.
   - *Interaction check:* Does C2's modification in `_revision.py` alter binding behavior for C1 or C3?
     - `_object_commit` calls `git rev-parse --disambiguate=<hex>`. For canonical 40-hex commit hashes (which C1 and C3 pass), `--disambiguate` returns exactly that one commit.
     - Peeling is restricted: `^{commit}` peeling is applied only if `cat-file -t` reports `"tag"`. Commit objects are returned directly by their confirmed OID.
     - In detached HEAD clones (such as `measure/run.py:58`), `bind()` verifies `_ancestor(repo, sha, f"refs/heads/{branch}")`. Line 61 updates `refs/heads/master` to the detached commit, so ancestry checks succeed.
     - Therefore, C2's enhancement strengthens object binding for C1 and C3 against decoy branch/tag shadowing without altering normal commit resolution.

2. **C1-C2 Cross-Axis Contract Lock:**
   - In `PROVINCE.md:150`, C1's clarification explicitly concludes:
     `"No configuration, service, package, boot or sibling-file write is authorized."`
   - This contract clause establishes the exact boundary enforced by C2:
     - "service write" $\rightarrow$ caught by `check-recheck-commands.py` (`systemctl_violations` catching `restart`, `enable`, etc.).
     - "package write" and "boot write" $\rightarrow$ caught by `check-recheck-commands.py` (`DEFAULT_FORBID` catching `pacman`, `yay`, `mkinitcpio`, `limine-update`).
     - "sibling-file write" $\rightarrow$ caught by seat isolation.
   - Thus, C1 and C2 mutually reinforce the host-safety boundary without conflating their verification metrics.

3. **Incomparability Threat: C1 Baseline Prefix Verification:**
   - In `dispatch.json:436`, the canonical planner directive for `ExecAdjacency` instructed:
     *"Prefix preservation against base can be checked for PROVINCE to ensure no old rewrite. Keep baseline red named actual missing correction, not missing registry."*
   - In `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:123-178`, `_ownership_correction` checks that `OWNERSHIP_HEADING` exists, that `lines[start:end]` matches `OWNERSHIP_SECTION_LINES`, that `OWNERSHIP_ARBITRATION_LINES` exist, and that `"| OUT-008 | ADJ-06 |"` and `"| OUT-009 | ADJ-06 |"` appear in `province_text`.
   - **However, `_ownership_correction` omits checking `lines[:start]` against baseline `PROVINCE.md`.**
   - In round 19, an author mutated historical row 1965 in `SKILL.md` in place (`+80/−1`), breaking baseline prefix preservation and forcing the round-20 disclosure `R20-SKILL-PREFIX-EXCEPTION`.
   - If `check-adjacency-anchors.py` does not verify baseline prefix preservation for `PROVINCE.md`, an edit that mutates lines 1–147 in place (such as altering the historical `OUT-009` row at line 129) would slip past both default mode and `--ownership-corrections`. Default mode (`_outbound_publication`) checks only anchor IDs, quotes, and hashes, not proposition text. This would allow historical rewriting while claiming additive correction.

---

## 3. The Proposed Move: Strict Count Schema Isolation and Baseline Prefix Verification in C1

To synthesize the round's proposals and guarantee zero harm across all axes, L1 should execute a single bounded move during production integration:

### The Move:
In `tools/check-adjacency-anchors.py`:
1. **Restore strict count schema isolation in default mode:**
   - Remove `"ownership_corrections": 0` from `_empty_counts()`.
   - In `evaluate(...)` (line 761), conditionally insert `"ownership_corrections"` into `counts` **only when `ownership_corrections=True`**:
     ```python
     if ownership_corrections:
         correction_count, correction_findings = _ownership_correction(
             province_text, doc, census_doc, registry_revision, reader)
         counts["ownership_corrections"] = correction_count
         findings.extend(correction_findings)
     ```
   - This ensures that `python3 tools/check-adjacency-anchors.py --revision <TARGET>` (legacy mode) emits the exact 8-key count dictionary of R19, mirroring the clean separation practiced by `check-registry-coverage.py` and `check-revision-binding.py`.

2. **Enforce immutable baseline prefix verification in `_ownership_correction`:**
   - In `_ownership_correction(province_text, doc, census_doc, registry_revision, reader)`:
     - Use `reader.read(BASE_REVISION, "PROVINCE.md")` (where `BASE_REVISION = "0cbc34dd6b20896085a8fb07943e3ea4027d8472"`) to obtain the canonical baseline text.
     - Verify that `province_text[:heading_byte_offset] == base_province_text` (or line-wise `lines[:start] == base_lines`).
     - If the baseline prefix was altered, emit finding `OWNERSHIP-CORRECTION-INVALID`, site `PROVINCE.md:1`, detail `"baseline PROVINCE.md prefix modified; correction must be strictly append-only"`, and return `(0, findings)`.
     - If the heading is absent, emit `OWNERSHIP-CORRECTION-MISSING` (exit 1).

---

## 4. Affected Axes

- **C1 Adjacency (Primary Beneficiary):**  
  Improves C1 verification rigor by enforcing the immutable prefix invariant on `PROVINCE.md`, preventing historical tampering (the exact failure mode that compromised `SKILL.md` in R19).
- **C2 Operability & C3 Calibration (Protected):**  
  Zero regression. `check-recheck-commands.py` and `check-registry-coverage.py` remain untouched and causally independent.
- **Legacy Verification Suite (`adjacency-legacy` in `measure/run.py:83`):**  
  Protected against JSON schema pollution, ensuring byte-level count comparability between R19 baseline and R20 target.

---

## 5. Second-Order Effects Across Surfaces

1. **Runtime Surface:**  
   `GitReader` in `tools/check-adjacency-anchors.py:101-140` already implements memoized committed blob retrieval (`reader.read(revision, path)`). Reading `PROVINCE.md` at baseline commit `0cbc34dd6b20896085a8fb07943e3ea4027d8472` requires one dictionary lookup. Zero additional subprocesses or shell calls are spawned.

2. **Contract Surface:**  
   Formally enforces that C1's clarification is strictly additive supersession, symmetrically closing the class of defects represented by `R20-SKILL-PREFIX-EXCEPTION` across both primary markdown documents (`SKILL.md` and `PROVINCE.md`).

3. **Substrate Surface:**  
   Completely read-only. Operates exclusively within committed Git blobs. Zero host mutation, package action, or boot-chain interaction.

4. **Verification Surface:**  
   Preserves exact oracle conformance with `preregister.json:31-36`:
   - Baseline commit: `OWNERSHIP_HEADING` absent $\rightarrow$ emits `OWNERSHIP-CORRECTION-MISSING; exit=1` (baseline red preserved).
   - In-place historical rewrite: `lines[:start]` modified $\rightarrow$ emits `OWNERSHIP-CORRECTION-INVALID; exit=1` (negative control enforced).
   - Valid append-only target commit: exact prefix preserved and clarification section present $\rightarrow$ emits `ownership_corrections=1; exit=0` (target green).

---

## 6. Risks and Counter-Measures

- **Risk 1: Baseline commit unavailable in shallow or isolated clones.**  
  *Counter-measure:* `measure/run.py:55-56` clones from `LANE` directly without depth limitation; `BASE` is the merge-base and parent commit. `GitReader` resolves `0cbc34d...` via `git cat-file -p`, which is guaranteed present in all lane clones.
- **Risk 2: Trailing whitespace differences across environments.**  
  *Counter-measure:* Compare exact raw bytes `province_text[:start_offset] == base_bytes` or strip newline variations (`rstrip("\r\n")`) consistently with `GitReader.read()`.
- **Risk 3: Test runner expecting `"ownership_corrections": 0` in default mode.**  
  *Counter-measure:* `preregister.json:10` explicitly binds the evaluator command for C1 to `--ownership-corrections`. The legacy suite (`measure/run.py:83`) checks `python3 tools/check-adjacency-anchors.py --revision <TARGET>` for exit 0 and clean findings, where omitting unrequested keys preserves R19 contract fidelity.

---

## 7. Verification

Verification steps for L1 integration (run under authorized final measurement):

1. **Verify default mode schema purity:**
   ```bash
   python3 tools/check-adjacency-anchors.py --revision <TARGET>
   ```
   *Expected outcome:* Exit 0; `status: "PASS"`; `counts` contains exactly the original 8 keys (`outbound_total`, `outbound_portable`, `inbound_total`, `inbound_classified`, `inbound_by_class`, `inbound_by_scope`, `live_object_checked`, `live_object_match`); `"ownership_corrections"` is absent.

2. **Verify explicit C1 evaluation:**
   ```bash
   python3 tools/check-adjacency-anchors.py --revision <TARGET> --ownership-corrections
   ```
   *Expected outcome:* Exit 0; `status: "PASS"`; `counts["ownership_corrections"] == 1`; findings empty.

3. **Verify negative control (prefix tampering):**
   In a fixture clone, mutate `PROVINCE.md:129` in place and append the clarification heading.
   ```bash
   python3 tools/check-adjacency-anchors.py --revision <TAMPERED_REV> --ownership-corrections
   ```
   *Expected outcome:* Exit 1; `status: "FAIL"`; finding `OWNERSHIP-CORRECTION-INVALID`; `counts["ownership_corrections"] == 0`.

4. **Verify baseline red control:**
   ```bash
   python3 tools/check-adjacency-anchors.py --revision 0cbc34dd6b20896085a8fb07943e3ea4027d8472 --ownership-corrections
   ```
   *Expected outcome:* Exit 1; `status: "FAIL"`; finding `OWNERSHIP-CORRECTION-MISSING`; `counts["ownership_corrections"] == 0`.

---

## 8. Limits and Boundaries

- **Static Review Only:** This connector review was conducted exclusively via read-only inspections of committed blobs, candidate worktree sources, and round-19/20 artifacts. No tests, builds, linter checks, or shell commands were executed.
- **No Clearance or Boot Readiness:** Nothing in this review certifies live host health, kernel readiness, or boot safety. Boot images remain UNKNOWN.
- **Sole Integration Authority:** L1 remains the sole integration writer and planner. This report presents evidence and a bounded proposal for integration synthesis without modifying production source code.

Scope: executed=none
