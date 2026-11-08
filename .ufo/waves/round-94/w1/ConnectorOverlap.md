# ConnectorOverlap — Sibling Overlap Scan and Cross-Lane Pattern Finding

Round 94, wave w1. Seat `ConnectorOverlap`.
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (git branch `master`, jj-colocated).
Freeze commit: `eb3b3e5150a63507a382003fa1a70039b190396b`.
Lane axes: `operability` + `freshness` (host operability and repair; milestone C1 depth 8, C2 operability 9; judged on `adjacency`).
Receipts: `.ufo/waves/round-94/w1/ConnectorOverlap/` (`sweep-head-30.txt`, `limine-absence-proof.txt`, `probe-contract-sweep.txt`, `scan-province-frontier.txt`, `cross-lane-pattern-bounds.txt`).

---

## 1. Non-Obvious Move (UFO-FSD Connector Synthesis)

### Evidence
- **ReviewBattery Findings F1 and F2 (`w1/ReviewBattery.md:36-39`)**:
  - **F1**: `AUTO-PROBE-SHAPES` does not exercise the `12.9.6.1` (quad-component) shape. The battery rule text (line 145) and gate docstring (`check-limine-pins.py:42-50`, regex `:121` `(?![\w.-])`) specify refusal for suffixed pre-release (`-rc1`) and quad-component (`.1`) strings, but the committed fixture `before/fake-limine/suffixed-rc` (and battery line 1916) sends only `-rc1`. An adversarial mutant with a hyphen-only suffix guard `(?![\w-])` passes `AUTO-PROBE-SHAPES` while improperly accepting `12.9.6.1`.
  - **F2**: `REFUSAL-VERSIONS-10DIGIT` has no lower-bound (accepted-side) control for the 9-digit boundary. The family tests four 10-digit values against a single `12.9.4` control row (a 2-1-1 digit version). Consequently, an over-strict mutant (`len(p) <= 8`, mutant `gate-strict8.py`) scores `met 98/98` in the battery, rejecting valid 9-digit components that the published specification explicitly accepts.
- **ReviewGate Analysis (`w1/ReviewGate.md:24-37`)**:
  The probe regex `(?i)\blimine\s+v?(\d+\.\d+\.\d+)(?![\w.-])` uses `\d+` instead of `\d{1,9}`, relying entirely on downstream `parse_limine_version` to enforce the 9-digit cap.
- **Cross-Lane Boundary Standards (`tameshi-shokunin/tools/registry-check.py:104-107, 1521-1531`)**:
  Under QUALITY 139, boundary testing requires exercising both the accepted maximum ($N$) and the refused minimum ($N+1$) within the same testing unit to prevent mutant survival in either direction.

### Affected Axes
- `depth`: improves mutant kill closure by eliminating both over-strict (`<= 8`) and under-strict (`<= 10`) boundary survivals, and killing hyphen-only regex weakenings.
- `operability`: neutral/improved (clarifies error diagnosis on malformed probe outputs without altering healthy host bootloader checks).
- `freshness`: neutral (does not affect era visibility split or package version tracking).

### Proposed Move: Pairwise Boundary Certification in Battery Refusal Families
In `tools/limine-pin-battery.py`:
1. Upgrade `REFUSAL-VERSIONS-10DIGIT` to a pairwise boundary family (`BOUNDARY-VERSIONS-DIGIT-9-10`) that pairs each 10-digit refusal (`1234567890.0.0` → rc 64, empty stdout) with an explicit 9-digit accepted maximum boundary case (`999999999.0.0` → rc 0, verdict evaluated). This directly kills the over-strict mutant `gate-strict8.py` (`len(p) <= 8`) which currently passes the battery 98/98 met.
2. In `AUTO-PROBE-SHAPES`, add a quad-component fake `12.9.6.1` to the shape test suite alongside `Limine 12.9.6-rc1`. This ensures that the suffix guard `(?![\w.-])` cannot be reduced to a hyphen-only guard `(?![\w-])`.

### Risks
- Adding test cases increases battery execution time slightly (~1.5 s).
- Mitigated: Battery test cases run hermetically in memory using existing subprocess execution fixtures.

### Verification
- Run `gate-strict8.py` against the updated battery: must read `unmet` with failed family `BOUNDARY-VERSIONS-DIGIT-9-10`.
- Run a hyphen-only mutant `gate-hyphenonly.py` against the updated battery: must read `unmet` with failed family `AUTO-PROBE-SHAPES`.
- Run against the landed gate: must read `met` with 0 error rows.

---

## 2. Fleet Scan for Conflicting Ground (Item 1)

### Sweep Command Executed
```sh
grep -rl -i -e 'bwrap' -e 'unshare-all' -e 'limine' -e 'probe' --include='*.md' /home/vgpnk/Projects/shokunin/*/corpus/knowledge/*.md 2>/dev/null | grep -v tsukuroi | head -30
```

### Matched Sibling Knowledge Files (30 files)
1. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-12-audio-checklist.md`
2. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-12-fixture-battery.md`
3. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-12-threshold-calibration.md`
4. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-13-sox-act-autodetect-predicate.md`
5. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-13-sox-ffmpeg-packet-residue.md`
6. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-13-sox-validbits-codec-map.md`
7. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-14-ffmpeg-cross-decoder-transport.md`
8. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-14-sox-autodetect-preemptor-ordering.md`
9. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-14-sox-extension-suffix.md`
10. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-14-sox-posttable-fallback.md`
11. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-14-sox-preemptor-map-complete.md`
12. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-14-sox-transport-axis.md`
13. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/2026-10-19-ebur128-dualmono-and-true-peak-on-fixtures.md`
14. `/home/vgpnk/Projects/shokunin/audio-shokunin/corpus/knowledge/seed.md`
15. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/anchor-boundaries-r4.md`
16. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/archives-verified-r9.md`
17. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/audit-r11.md`
18. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/bash-local-expansion-r35.md`
19. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/capture-bash-pin-r39.md`
20. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/capture-path-pin-r41.md`
21. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/chain-resolution-r3.md`
22. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/claim-record-fields-r33.md`
23. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/dead-zone-pcre-r34.md`
24. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/gate-baseline-r8.md`
25. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/git-revision-identity-r63.md`
26. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/hardening-r10.md`
27. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/hardlink-alias-r13.md`
28. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/json-delimiter-r24.md`
29. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/long-span-argv-r34.md`
30. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/manifest-append-lock-r32.md`

### Per-Lane Findings on Target Concepts

#### (a) The Limine Visibility Boundary
- **Tsukuroi Definition (`corpus/knowledge/limine-auto-default-r94.md`, `limine-version-probe-r93.md`, `limine-r92-oracle-isolation.md`)**:
  In Limine $\le$ 12.9.4, if line 1 is a menu entry, `c > config_addr` is false and subsequent body lines remain visible as global configuration options. In Limine $\ge$ 12.9.5 (`create_menu_tree()`), line-end NUL termination restricts global lookup to the preamble before the first entry line.
- **Fleet-Wide Search**:
  ```sh
  grep -rn -i "limine" /home/vgpnk/Projects/shokunin/*/corpus/knowledge/*.md 2>/dev/null | grep -v tsukuroi
  ```
  **Result:** Exit code 1; exactly 0 lines printed. (Recorded in `receipts/limine-absence-proof.txt`).
- **Verdict**: **Zero conflicts**. No sibling lane documents Limine bootloader configuration, parsing rules, or the 12.9.5 visibility split. `tsukuroi-shokunin` maintains exclusive fleet ownership.

#### (b) The Default-Probe Contract
- **Tsukuroi Definition (`tools/check-limine-pins.py:107-123, 503-518`)**:
  `--limine-version` defaults to `auto`. The gate executes `limine --version` read-only via PATH lookup with a 5-second timeout, matches `(?i)\blimine\s+v?(\d+\.\d+\.\d+)(?![\w.-])` on stdout, emits telemetry `limine_version_source: "probe"`, and fails closed (exit 64, empty stdout) on any failure.
- **Sibling Findings Across Fleet**:
  - `chousa-shokunin` (`corpus/knowledge/capture-bash-pin-r39.md:12-18`, `capture-path-pin-r41.md`, `grep-pin-r35.md`):
    Documents the tool provenance verification pin: default probe of `/usr/bin/bash` then `/bin/bash` via `--version` reporting `GNU bash` bounded by `timeout(1)`. If unverified, the gate refuses exit 2 (`BASH_PROVENANCE refused`) before reading records.
    *Distinction*: Chousa pins internal test-runner dependencies to prevent hostile environment hijacking; Tsukuroi probes host target binaries to determine system bootloader era.
  - `kama-shokunin` (`corpus/knowledge/endpoint-identity.md:5, 97-101`):
    Documents local inference server probe contracts: defaults to 2-second connect timeout and 5-second total request timeout on loopback.
    *Distinction*: Kama probes live HTTP model serving endpoints, not local CLI binaries.
  - `kumitate-shokunin` (`corpus/knowledge/runtime-remainder-census.md:262-266`):
    Documents `DEFAULT_PROBE_TIMEOUT_SECS` (literal 8-second default) for orchestrator interpreter probes, failing closed on non-positive or overflowing overrides.
    *Distinction*: Kumitate governs agent orchestration task execution limits.
  - `audio-shokunin` (`corpus/knowledge/2026-10-12-fixture-battery.md:11, 70`):
    Uses `--probe-failing`, `--probe-slope`, etc., as CLI test flags to execute ffprobe/sox checks on audio fixtures.
    *Distinction*: Purely local test harness modes.
- **Verdict**: **Zero conflicts**. Sibling lanes utilize analogous fail-closed probe patterns for their own domains (tool provenance, HTTP endpoint liveness, runner timeouts), but none defines or conflicts with Tsukuroi's bootloader version probe contract.

---

## 3. Province and Frontier Reconciliation (Item 2)

### Comparison of `corpus/README.md` `## Frontier` with `PROVINCE.md`

| Surface Touched This Round | `corpus/README.md` Frontier Reference | `PROVINCE.md` Boundary Definition | Ownership / Reconciliation Status |
|---|---|---|---|
| **Shipped-Artifact Reverse Engineering** | Line 34-35: "Shipped-artifact RE ownership is contested between kaidoku and revenger. Route an actual internals question to the protocol integrator before analysis." | Lines 25-28: "Refuses: ... binary RE of drivers (→ kaidoku/revenger — tsukuroi tracks *state and health*, not internals)."<br>Lines 51 (ADJ-06, OUT-008/OUT-009) & 79-81. | **Reported, Not Absorbed**. Round 94 inspects upstream open-source C files (`config.c`, `host_limine.c`) and ChangeLog texts. It performs NO binary disassembly, decompression, or ELF symbol reverse engineering of host binaries. Contested RE ownership remains external. |
| **External Binary Version Probing** | Lines 1104, 1116-1117: "`--limine-version` now defaults to `auto` ... a host upgraded without the flag is judged by the probed binary's era." | Lines 8-15: "Owns (surfaces, all read-only probes): ... Update-safety questions: what an -Syu would touch, what pins/holds exist." | **Core Owned**. Probing `limine --version` is strictly scoped to deciding `/boot/limine.conf` syntax era. Tsukuroi does not claim a general tool provenance framework (owned by `chousa`). |
| **Mutation Testing and Verification Craft** | Lines 1110-1113: "The ten-digit enumeration ... and the probe-shape family ... are the r93 survivors' closures; each is killed by a one-clause bend (N01/N03, N02)." | Lines 52 (ADJ-07, OUT-010): "A census blind spot raises a reusable verification/mutation-testing question → tameshi (owns the method)." | **Properly Scoped**. Tameshi owns generic verification craft across the fleet; Tsukuroi applies mutation-testing discipline strictly to its own gate and battery instruments. |
| **Launcher Residual Channels** | Line 1114-1115: "The r92 launcher residuals stay open; the r93 AUTO-fake literal leakage is disclosed in the battery docstring (CriticForgers f6), not closed." | Lines 8-15: Core boundary bounds read-only probes. | **Disclosed Frontier**. Residual isolation channels (such as `/proc` leakage) are acknowledged as non-claimed residual limits. |

---

## 4. Cross-Lane Pattern: Input Boundary & Digit-Cap Refusal (Item 3)

### Shared Defect Class
**Input boundary validation and numeric/string length cap refusal under QUALITY 139**:
When an instrument enforces a numeric constraint (such as a component length cap, integer value ceiling, or buffer bound) to prevent crashes or integer overflow (e.g. Python 3.11+ `sys.set_int_max_str_digits` 4300-digit limit, or C-level integer overflow), a test suite that only verifies out-of-range spellings without testing the exact boundary pair ($N$ accepted vs $N+1$ refused) allows mutant gates that widen the boundary comparison (such as `<=` instead of `<`) to survive undetected.

### Sibling Lane Exemplar: `tameshi-shokunin`
- **File**: `tameshi-shokunin/tools/registry-check.py` (`lines 104-107, 1521-1531`)
- **Shared Failure Mode**:
  In `registry-check.py`, `MAX_TIMEOUT_S = 86400` was established because a finite timeout of 2,147,484 seconds or more overflows Python `Popen.communicate()`'s internal C-level timeout structure, crashing with exit 1.
  The test harness tests the boundary failure modes explicitly:
  - `timeout-too-large` (`"2147484"`)
  - `timeout-overflow` (`"1e999"`)
  - `timeout-float-huge` (`"1e308"`)
  - `short-source-revision` (`proc.returncode == 2` for commit rev length outside 7-40 hex digits).
  If `tameshi` had only tested non-numeric strings (like `"abc"`), an off-by-one or widened numeric bound would pass silently.

### Parallel Sibling Instances
- `chousa-shokunin/tools/build-spans.py` (`lines 28, 172`) and `tools/capture-text.py` (`lines 38, 111, 396`):
  Enforces `MAX_CAPTURE` and `MAX_PART` caps and source IDs with exactly 3 digits (`S` + `\d{3}`). Any payload exceeding length or violating digit counts fails closed with exit 1 and empty stdout.
- `mado-shokunin/tools/mado-binds.py` (`lines 321, 410-421`):
  Detects numeric overflow via `std::out_of_range` / `ERANGE`, returning `"overflow"` and refusing out-of-range float/integer parameters.

### Connection to Tsukuroi Round 94
In Round 93, the battery's `REFUSAL-VERSIONS` family checked ten out-of-range values, but only tested an over-bound value far above 10 digits (`12345678901234567890.0.0`). Mutant M13 (`len(p) <= 10` instead of `<= 9`) survived because no test evaluated a component with exactly 10 digits. Round 94 added `REFUSAL-VERSIONS-10DIGIT` (`1234567890.0.0`, etc.) to close M13, demonstrating the identical boundary-refusal pattern seen in `tameshi` and `chousa`.

---

## 5. Sibling Overlap and Contract Summary Table

| Repo / File | What it Holds | Conflict / Duplicate / Silent | Recommendation |
|---|---|---|---|
| `chousa-shokunin/corpus/knowledge/capture-bash-pin-r39.md` | Pinned bash/grep tool provenance with default probe (`/usr/bin/bash`) and fail-closed exit 2. | **Silent** on Limine; **Compatible adjacent** on fail-closed version probing pattern. | Maintain boundary: Chousa owns internal tool provenance; Tsukuroi owns bootloader config diagnosis. |
| `tameshi-shokunin/tools/registry-check.py` | Selftest boundary checks for `MAX_TIMEOUT_S` (2147484s, 1e999 overflow) and hex rev bounds (7-40 digits). | **Silent** on Limine; **Exemplar pattern** for numeric boundary refusal. | Follow Tameshi's precedent for pairing accepted and refused boundary conditions under QUALITY 139. |
| `kumitate-shokunin/corpus/knowledge/runtime-remainder-census.md` | Bounded probe timeout defaults (8s) and fail-closed fallbacks. | **Silent** on Limine; **Compatible adjacent** on timeout safeguards. | Independent orchestration domain. |
| `kama-shokunin/corpus/knowledge/endpoint-identity.md` | Local loopback model endpoint identity probing with 2s/5s timeouts. | **Silent** on Limine; **Compatible adjacent** on probe timeout limits. | Independent inference domain. |
| `kaidoku-shokunin` & `revenger-shokunin` (multiple files) | Shipped artifact firmware and binary reverse engineering. | **Silent** on Limine; **Contested RE boundary**. | Maintain strict boundary: Tsukuroi tracks OS state/health, not binary internals; report, never absorb. |
| All other sibling repositories (15 lanes) | Various domain-specific fixtures and tests. | **Silent** on Limine; **Zero overlap**. | No action required. |

---

## ## Verdict

**Verdict: no contradiction**.

1. **Fleet Scan (Item 1)**: Sibling scans confirm complete absence of Limine across all 20 sibling repositories (exit code 1, 0 lines in `receipts/limine-absence-proof.txt`). Default-probe contracts in `chousa`, `kama`, and `kumitate` govern disjoint domains (tool pinning, HTTP endpoints, runner timeouts) and do not conflict with Tsukuroi's bootloader version probe contract.
2. **Province & Frontier (Item 2)**: Reconciled. Shipped-artifact reverse engineering contested between `kaidoku` and `revenger` is reported and strictly not absorbed. Tsukuroi inspects only open C sources and text metadata.
3. **Cross-Lane Pattern (Item 3)**: Identified in `tameshi-shokunin/tools/registry-check.py:104-107, 1521-1531` (`timeout-too-large` / `timeout-overflow`) and `chousa-shokunin/tools/build-spans.py:28, 172`, representing the shared class of **input boundary validation and numeric length-cap refusal under QUALITY 139**.
4. **Claims Evidence**:
   - **Claim C1 (Depth 8)**: **SUPPORTED**. The two new families (`REFUSAL-VERSIONS-10DIGIT` and `AUTO-PROBE-SHAPES`) kill bends N01, N02, N03 with single-family failures and 0 error rows, while the landed gate reads 98/98 met.
   - **Claim C2 (Operability 9)**: **SUPPORTED**. `--limine-version` defaults to `auto`, flag-free live execution probes the host `12.9.4` bootloader with source `probe` and era `pre-12.9.5`, and gate selftest passes 39/39.

**Receipts**:
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-94/w1/ConnectorOverlap/sweep-head-30.txt`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-94/w1/ConnectorOverlap/limine-absence-proof.txt`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-94/w1/ConnectorOverlap/probe-contract-sweep.txt`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-94/w1/ConnectorOverlap/scan-province-frontier.txt`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-94/w1/ConnectorOverlap/cross-lane-pattern-bounds.txt`
