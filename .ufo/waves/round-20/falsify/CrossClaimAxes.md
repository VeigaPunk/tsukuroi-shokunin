# CrossClaimAxes — Cross-Check of Round-20 Claims, SCORECARD, Preregister, and Candidate Gates for Causal Separability

**Seat:** `TsukuroiR19Recovery.CrossClaimAxes` (connector leaf; author-dispatched, not outside closure)  
**Role:** UFO-FSD connector  
**Production Lane:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`  
**Baseline:** `0cbc34dd6b20896085a8fb07943e3ea4027d8472` (`.ufo/waves/round-20/preregister.json:3`; `SCORECARD.md:616`)  
**Report Destination:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/falsify/CrossClaimAxes.md`  
**Declared Axes:** C1 **adjacency** (lowest, ordinal 8, delta 0), C2 **operability** (ordinal 9, delta 0), C3 **calibration** (ordinal 9, delta 0)  
**Contract:** NO-EXEC: `read`, `grep`, `glob`, and `write` (named report only). No bash, eval, subprocesses, tests, builds, lint, formatters, host probes, git mutations, or target execution. Boot images remain UNKNOWN; no clearance.  

---

## 1. Audit Target & Problem Statement

In `SCORECARD.md:614–625` and `.ufo/waves/round-20/preregister.json:4–29`, Round 20 attempt 1 declares three distinct claims on three separate axes:
- **C1 (Adjacency, ordinal 8 → 8, delta 0):** `ownership_corrections` (0 → 1) evaluated by `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`.
- **C2 (Operability, ordinal 9 → 9, delta 0):** `object_selector_tools` (0 → 9) evaluated by `python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors` (with supporting repair: execution-log `systemctl` mutation filtering in `tools/check-recheck-commands.py`).
- **C3 (Calibration, ordinal 9 → 9, delta 0):** `audit_live_map_errors` (1 → 0) evaluated by `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map`.

`SCORECARD.md:624` explicitly asserts causal separability:
> *"Each claim has a separate content locus and finite evaluator mode; shared revision binding is infrastructure, not C1/C3 claim content."*

This audit conducts a thorough, source-grounded cross-check across `SCORECARD.md`, `preregister.json`, and all candidate gates across the four inherited worktrees (`/tmp/tsukuroi-r20-binder-20261021`, `/tmp/tsukuroi-r20-registry-20261021`, `/tmp/tsukuroi-r20-adjacency-20261021`, `/tmp/tsukuroi-r20-execscope-20261021`) to evaluate whether the claims are truly causally separable, to identify hidden shared dependencies and metrics that induce non-independence, and to propose one bounded synthesis move that improves verification fidelity without harming any axis.

---

## 2. Systematic Cross-Check Evidence

### 2.1 Declared Independence vs. Observed Implementation Coupling

| Claim / Surface | Declared Axis & Metric | Content Locus | Candidate Evaluator Gate | Evaluator Invocations & Shared Code |
|---|---|---|---|---|
| **C1** | Adjacency (8)<br>`ownership_corrections` (0→1) | `PROVINCE.md:148–152`<br>(`## R20 ownership clarification — OUT-009`) | `/tmp/tsukuroi-r20-adjacency-20261021`<br>`tools/check-adjacency-anchors.py` | Imports `tools/_revision.py` (`bind`, `clean_env`, `RevisionError`). Probed as discovered tool by C2's judge. |
| **C2** | Operability (9)<br>`object_selector_tools` (0→9) | `tools/_revision.py:112–126`<br>(`_object_commit`), `check-recheck-commands.py` | `/tmp/tsukuroi-r20-binder-20261021`<br>`tools/check-revision-binding.py` | Evaluates `_revision.py` continuity across 9 original tools; actively executes C1 and C3 gate tools via `discover()`. |
| **C3** | Calibration (9)<br>`audit_live_map_errors` (1→0) | `SKILL.md:2096–2118`<br>(`## Gate and probe registry — round20`) | `/tmp/tsukuroi-r20-registry-20261021`<br>`tools/check-registry-coverage.py` | Imports `tools/_revision.py` (`bind`). Evaluates registry coverage over **all** tools in `tools/` (including C1 and C2 tools). |

### 2.2 Five Identified Shared Dependencies and Non-Independent Couplings

#### Shared Dependency 1: Common-Mode Runtime Substrate in `tools/_revision.py`
- **Evidence:**  
  - Gate 1 (`tools/check-adjacency-anchors.py:18,837`):
    ```python
    from _revision import E_GIT, RevisionError, bind, clean_env
    ...
    binding = bind(ROOT, args.revision, args.branch)
    ```
  - Gate 3 (`tools/check-registry-coverage.py:17,341`):
    ```python
    from _revision import E_GIT, RevisionError, bind, clean_env
    ...
    binding = bind(ROOT, args.revision, args.branch)
    ```
  - Gate 2 (`tools/check-revision-binding.py`): Grades `tools/_revision.py`. C2's sole production implementation change is in `tools/_revision.py` (`_object_commit` disambiguation, lines 112–126).
- **Causal Non-Independence:**  
  `tools/_revision.py` is not an external runtime library; it is C2's primary deliverable. If C2's candidate implementation in `_revision.py` introduces an unexpected syntax assumption, regression in `bind()`, or failure during revision resolution, Gate 1 and Gate 3 immediately catch `RevisionError` and exit with `CANNOT_EVALUATE` (exit 2; `check-adjacency-anchors.py:841–842`, `check-registry-coverage.py:369–373`).  
  Neither C1's `ownership_corrections` nor C3's `audit_live_map_errors` can be evaluated if C2's substrate fails. A defect in C2 directly renders C1 and C3 unevaluable.

#### Shared Dependency 2: Gate 3 (`check-registry-coverage.py`) Whole-Repository Coverage Coupling
- **Evidence:**  
  - In `check-registry-coverage.py:348–361`:
    ```python
    rows = _operative_rows(skill_data.decode("utf-8", "replace"))
    tools = reader.tool_files(binding.sha)
    findings, covered = _coverage(rows, tools, reader, binding.sha)
    map_findings = _audit_live_map(rows) if args.audit_live_map else []
    findings.extend(map_findings)
    counts = _base_counts(len(tools), len(rows), len(covered), len(findings))
    if args.audit_live_map:
        counts["audit_live_map_errors"] = len(map_findings)
    code = FAIL if findings else PASS
    return _emit(code, binding.sha, binding.branch, binding.branch_tip, counts, findings)
    ```
  - In `preregister.json:51`: C3's oracle expectation for `corrected_live_map` is:
    `"audit_live_map_errors=0; exit=0"`.
- **Causal Non-Independence:**  
  The overall exit code of the C3 evaluation command (`code = FAIL if findings else PASS`) depends on `findings`, which is the union of `map_findings` and `findings` from `_coverage()`.  
  `_coverage()` validates that *every single regular tool* in `tools/` at `binding.sha` has an operative row in `SKILL.md` (no `REGISTRY-ROW-MISSING`), that no row is orphaned (`REGISTRY-ROW-ORPHAN`), that no row is ambiguous (`REGISTRY-ROW-AMBIGUOUS`), and that all selftest flags exist in the tool bodies (`REGISTRY-SELFTEST-UNRESOLVED`).  
  `tools/` contains C1's gate (`check-adjacency-anchors.py`) and C2's tools (`_revision.py`, `check-revision-binding.py`, `check-recheck-commands.py`).  
  If C1 or C2 modifies a tool in `tools/` (or alters CLI options/selftest arguments) without an exact, synchronized update to the operative `SKILL.md` table, `_coverage()` generates findings. Even if `counts["audit_live_map_errors"] == 0`, C3 fails with exit 1 (`FAIL`).  
  Therefore, C3's gate acceptance is strictly coupled to C1 and C2 integration completeness.

#### Shared Dependency 3: Gate 2 (`check-revision-binding.py`) Active Subprocess Execution of C1 and C3 Tools
- **Evidence:**  
  - In `check-revision-binding.py:245–256`:
    ```python
    def discover(sandbox, tip):
        proc = must(git(sandbox, "ls-tree", "--name-only", f"{tip}:tools"), "E-GIT-READ", "tools/")
        found = []
        for name in sorted(proc.stdout.decode("utf-8", "replace").split("\n")):
            if (not name.endswith(".py") or name in TOOLS or name == JUDGE or name.startswith("_")):
                continue
            body = must(git(sandbox, "show", f"{tip}:tools/{name}"), "E-GIT-READ", f"tools/{name}")
            if b'"--revision"' in body.stdout:
                found.append(name)
        return tuple(found)
    ```
  - Both Gate 1 (`check-adjacency-anchors.py`) and Gate 3 (`check-registry-coverage.py`) contain `b'"--revision"'` and are returned in `extras = discover(sandbox, tip)`.
  - In `check-revision-binding.py:644–673`, `measure()` builds `names = TOOLS + extras` and iterates over *all* `names`, calling:
    ```python
    item = probe_tool(sandbox, name, tip, unlanded_sha, parent, branch, blob)
    ```
  - Inside `probe_tool()`, `run_tool(sandbox, name, revision, ...)` spawns subprocesses:
    ```python
    try:
        proc = subprocess.run([sys.executable, str(sandbox / "tools" / name),
                               "--revision", revision, *extra, *EXTRA.get(name, ())],
                              cwd=str(sandbox), stdin=subprocess.DEVNULL,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env=clean_env(), timeout=60)
    except subprocess.TimeoutExpired:
        raise Cannot("E-TOOL-TIMEOUT", f"tools/{name}", "exceeded 60s")
    except OSError as exc:
        raise Cannot("E-TOOL-RUN", f"tools/{name}", str(exc)[:120])
    ```
- **Causal Non-Independence:**  
  `Cannot` is not caught within `measure()`. If either C1 (`check-adjacency-anchors.py`) or C3 (`check-registry-coverage.py`) hangs, times out (>60s), or raises an `OSError` during `run_tool()`, `measure()` terminates immediately. `main()` catches `Cannot` and outputs:
  `{"status": "CANNOT_EVALUATE", "object_selector_status": "CANNOT_EVALUATE", ...}` with exit 2.  
  Furthermore, C2's JSON payload explicitly includes `all_bound_tools`, `all_consistent_tools`, and `additional_consistent_tools`, which aggregate the execution outcomes of C1 and C3 tools. A fatal flaw in C1 or C3 tool scripts can abort C2's evaluation entirely.

#### Shared Dependency 4: Gate 1 (`check-adjacency-anchors.py`) Schema Pollution in Default Mode
- **Evidence:**  
  - Baseline `tsukuroi-shokunin/tools/check-adjacency-anchors.py:208–217` defined `_empty_counts()` with exactly 8 keys:
    `outbound_total`, `outbound_portable`, `inbound_total`, `inbound_classified`, `inbound_by_class`, `inbound_by_scope`, `live_object_checked`, `live_object_match`.
  - In candidate `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:373`, `_empty_counts()` unconditionally inserts:
    `"ownership_corrections": 0`.
- **Causal Non-Independence:**  
  When `tools/check-adjacency-anchors.py` is executed in default legacy mode without `--ownership-corrections` (as run in `measure/run.py:83` for `adjacency-legacy`: `python3 tools/check-adjacency-anchors.py --revision <TARGET>`), it emits an unrequested `"ownership_corrections": 0` field.  
  While C2 (`check-revision-binding.py`) and C3 (`check-registry-coverage.py`) strictly guard their new metrics behind their respective CLI flags (`object_selectors_requested`, `audit_live_map_errors`), C1 leaks its metric into legacy baseline/target runs, breaking exact schema comparability across rounds.

#### Shared Dependency 5: Single Commit SHA & Historical Prefix Lock in Runner
- **Evidence:**  
  - In `measure/run.py:70–78`, all three claim checks (`c1-before/after`, `c2-before/after`, `c3-before/after`) are driven in a single clone against one target revision `args.revision`.
  - In `measure/run.py:104–111`, `prefixes.json` verifies strict prefix preservation (`new.startswith(old)`) across seven core files, notably `PROVINCE.md` (C1) and `SKILL.md` (C3).
- **Causal Non-Independence:**  
  If C1 mutates lines 1–146 of `PROVINCE.md` in place (violating additive supersession), or if C3 mutates lines 1–2083 of `SKILL.md` in place (repeating the R19 `+80/−1` nonappend defect), the entire measurement run fails `round20-prefixes` (`run.py:111`), invalidating the evaluation of all three claims simultaneously.

---

## 3. Explicit Contradictions

1. **Separability Declaration vs. Substrate Coupling:**  
   `SCORECARD.md:624` states that shared revision binding is "infrastructure, not C1/C3 claim content." However, because C2's core work is the direct modification of `tools/_revision.py`, any failure in C2's code directly breaks the runtime execution of C1 and C3 evaluators.
2. **Dedicated Map Metric vs. Whole-Table Gate Gating:**  
   `preregister.json:23–27` states that C3's metric is `audit_live_map_errors` (1 → 0). However, the gate's exit code (`exit 0`) requires zero findings across all 17 tools in `tools/` and `SKILL.md`. Thus, C3's pass/fail status is not an isolated measure of live-map calibration, but an aggregate test of total repository tool-registry synchronization.
3. **Isolated Original-Nine Continuity vs. Dynamic Discovery Probing:**  
   `check-revision-binding.py:12–15` asserts causal separability: "Other top-level public tools/*.py with the exact literal '--revision' are discovered and fully probed, but are informational additional_* / all_* fields, not C2's grade (causal separability from C1/C3)." However, `run_tool()` executes those discovered tools in subprocesses without catching timeouts or OS errors, allowing a discovered C1 or C3 tool failure to raise `Cannot` and abort C2 with `CANNOT_EVALUATE`.

---

## 4. Second-Order Effects Across Surfaces

1. **Runtime Surface:**  
   - `check-revision-binding.py` spawns subprocesses for both original nine tools and discovered tools. In a shared execution environment, any hanging tool can consume 60s of timeout before terminating the test harness.
   - `_revision.bind()` is called synchronously at startup by every CLI gate. Object lookup must remain fast plumbing (`git rev-parse --disambiguate`).
2. **Contract Surface:**  
   - C1 establishes the five forbidden write classes in `PROVINCE.md:150` (`configuration`, `service`, `package`, `boot`, `sibling-file`).
   - C2 operationalizes this boundary through `DEFAULT_FORBID` and `systemctl_violations` in `check-recheck-commands.py`.
   - C3 formalizes that `boot-chain-audit` live schema v2 emits only `0 CONSISTENT` or `2 UNKNOWN`, forbidding false live `DEGRADED` claims.
3. **Substrate Surface:**  
   - Zero modification of host OS packages, systemd unit states, bootloader configurations, or mount points.
   - Evaluators operate read-only against Git commits or within private throwaway sandbox clones.
4. **Verification Surface:**  
   - Schema purity must be maintained: legacy counting commands without R20 flags must emit exact R19 JSON schemas.
   - Oracle controls from `preregister.json:31–64` must hold without cross-tool contamination.

---

## 5. Proposed Move: Decoupled Verification Invariance Synthesis

To eliminate cross-claim fragility and guarantee genuine causal independence during L1 final integration, L1 should implement the following **Decoupled Verification Invariance Synthesis**:

### Component 1: Schema Isolation and Prefix Invariance in Gate 1 (`check-adjacency-anchors.py`)
1. **Conditional Count Schema:** In `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py`, remove `"ownership_corrections": 0` from `_empty_counts()`. In `evaluate()` (line 761), insert `"ownership_corrections"` into `counts` **only when `ownership_corrections=True`**. This guarantees that default legacy invocations emit the exact 8-key schema of R19.
2. **Prefix Invariance Verification:** In `_ownership_correction()`, verify that lines of `PROVINCE.md` prior to `## R20 ownership clarification — OUT-009` are byte-identical to `PROVINCE.md` at baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472`. This prevents silent in-place modification of historical rows (enforcing the additive supersession contract).

### Component 2: Discovered-Tool Subprocess Confinement in Gate 2 (`check-revision-binding.py`)
In `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:359–371`, confine `Cannot` exceptions originating from discovered tools:
- In `run_tool(sandbox, name, revision, branch=None)`:
  If `name not in TOOLS` (it is an extra discovered tool such as C1 or C3) and `subprocess.TimeoutExpired` or `OSError` occurs, do not raise an unhandled `Cannot`.
  Instead, return `(CANNOT, json.dumps({"findings": [{"id": "E-DISCOVERED-TOOL", "site": name, "detail": "discovered tool failed or timed out"}]}))`.
- This ensures that a bug, timeout, or environment issue in a newly discovered C1 or C3 tool marks only that informational tool un-bound, while strictly preserving C2's original-nine evaluation and preventing a catastrophic `CANNOT_EVALUATE` cascade.

### Component 3: Explicit Error Partitioning in Gate 3 (`check-registry-coverage.py`)
In `/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py`:
- Retain `counts["audit_live_map_errors"] = len(map_findings)` as the specific C3 calibration metric.
- In `SCORECARD.md` and integration notes, explicitly document that C3's `exit 0` requires total registry coverage across all tools in `tools/`, ensuring that L1 verifies full synchronization of `SKILL.md:2096–2118` across all 17 tools before committing.

---

## 6. Affected Axes

- **C1 Adjacency (Lowest Axis, Ordinal 8 → 8, delta 0):**  
  **Directly Improved.** Restores legacy schema purity and enforces historical prefix immutability on `PROVINCE.md`, preventing unflagged historical mutations.
- **C2 Operability (Ordinal 9 → 9, delta 0):**  
  **Directly Improved.** Hardens C2 against discovered-tool subprocess cascades, ensuring that the original-nine continuity evaluation is genuinely independent of external tools.
- **C3 Calibration (Ordinal 9 → 9, delta 0):**  
  **Unharmed & Clarified.** Live-map calibration remains strictly evaluated against `AUDIT_LIVE_MAP`, while integration documentation explicitly accounts for whole-table coverage prerequisites.
- **Substrate / Execution Surfaces:**  
  Unharmed. Operations remain strictly read-only and confined to committed Git blobs.

---

## 7. Risks and Counter-Measures

| Risk | Severity | Mechanism | Counter-Measure |
|---|---|---|---|
| **Discovered Tool Exception Leak** | High | A syntax error or timeout in `check-adjacency-anchors.py` crashes `check-revision-binding.py` during `measure()`. | Confine discovered-tool errors inside `run_tool()`; allow `Cannot` to propagate only for tools in `TOOLS` (the original nine). |
| **Legacy Schema Incompatibility** | Medium | Verification script in `run.py:83` expects 8 keys; candidate emits 9 keys including `"ownership_corrections": 0`. | Make `"ownership_corrections"` strictly conditional on `ownership_corrections=True`. |
| **Out-of-Sync Tool Row in SKILL.md** | High | L1 integrates tool changes but forgets to update `SKILL.md` round 20 table, causing C3 to fail with `REGISTRY-ROW-MISSING` or `REGISTRY-SELFTEST-UNRESOLVED`. | Verify all 17 tool rows in `SKILL.md:2100–2118` carry updated CLI flags (`--ownership-corrections`, `--object-selectors`, `--audit-live-map`) and match committed tool paths. |
| **Baseline Revision Resolution Failure** | Low | Sandboxed clone does not contain baseline commit `0cbc34dd6b20896085a8fb07943e3ea4027d8472`. | Clones are created from `LANE` with full history; baseline commit is guaranteed reachable. |

---

## 8. Verification Plan (for L1 Post-Wave Final Evaluation)

*Note: Per seat contract, NO verification commands were executed by this seat. The commands below are specified for L1 execution during the canonical measurement wave.*

1. **C1 Adjacency Measurement:**
   ```bash
   python3 tools/check-adjacency-anchors.py --revision <TARGET> --ownership-corrections
   ```
   - *Expected:* `ownership_corrections=1; exit=0`.
   - *Legacy Schema Check:* `python3 tools/check-adjacency-anchors.py --revision <TARGET>` emits exit 0 and `counts` contains exactly 8 keys (`ownership_corrections` absent).

2. **C2 Revision Binding Measurement:**
   ```bash
   python3 tools/check-revision-binding.py --tools-revision <TARGET> --object-selectors
   ```
   - *Expected:* `object_selector_tools=9; exit=0; object_selector_status=PASS`.
   - *Discovered Isolation Check:* Extra tools in `additional` cannot trigger `status: CANNOT_EVALUATE`.

3. **C3 Registry Coverage & Live Map Measurement:**
   ```bash
   python3 tools/check-registry-coverage.py --revision <TARGET> --audit-live-map
   ```
   - *Expected:* `audit_live_map_errors=0; findings=[]; exit=0`.

4. **Multi-File Prefix Preservation Check:**
   ```bash
   python3 -c "import hashlib, json; prefixes = json.load(open('.ufo/waves/round-20/measure/final/prefixes.json')); assert all(v['preserved'] for v in prefixes.values())"
   ```
   - *Expected:* All core files preserve baseline prefixes byte-for-byte.

---

Scope: executed=none
