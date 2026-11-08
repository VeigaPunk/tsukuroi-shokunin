# ConnectorOverlap — Sibling Overlap Scan and Cross-Lane Pattern Finding

Round 93, wave w1. Seat `ConnectorOverlap`.
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
Lane axes: `operability` + `freshness` (host operability and repair)
Receipts: `.ufo/waves/round-93/w1/ConnectorOverlap/`

---

## 1. Non-Obvious Move (UFO-FSD Connector Synthesis)

### Evidence
- In Round 93 C2 (`SCORECARD.md`, `.ufo/plans/round-93.md`), `--limine-version auto` runs `limine --version` via PATH lookup (`probe_limine_version()` in `tools/check-limine-pins.py:107-119`), records `limine_version` and `limine_version_source: "probe"`, and selects the visibility era (A vs B).
- In `chousa-shokunin`'s provenance gate (`corpus/knowledge/grep-pin-r35.md`, `tools/research-gate.sh:453-471`), tool probing binds both the resolved absolute path (`path=/usr/bin/grep`) and source (`default|override`) alongside the extracted version, ensuring caller environment shadowing is visible in telemetry.
- In `revenger-shokunin`'s forensic validation contract (`corpus/knowledge/tool-validation-by-function-and-version.md`, citing SWGDE 18-Q-001-2.1 and NIST CFTT), a tool verification claim binds a specific executable binary rather than an ambient name.
- Upstream source S384 (`host/limine.c:2035` vs `2030-2033`) demonstrates that `limine` supports both `--version` (multi-line banner `Limine <X.Y.Z>`) and `--version-only` (bare `<X.Y.Z>`). The gate probe correctly parses `stdout` using regex `(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b`.

### Affected Axes
- `operability`: improves auditability and diagnostic discrimination for live host runs (`sudo check-limine-pins.py --live --limine-version auto`), preventing silent misattribution between `/usr/bin/limine` and local wrapper scripts or virtual environment binaries.
- `freshness`: neutral (does not delay package updates or change the era boundary threshold).

### Proposed Move
In corporate telemetry emission for `--limine-version auto`, bind the resolved executable's absolute path into the gate output payload (`limine_executable_path: shutil.which("limine")` alongside `limine_version` and `limine_version_source: "probe"`).
This satisfies the fleet-wide provenance standard demonstrated in `chousa` and `souji` while keeping the gate's era selection and refusal behavior strictly unchanged.

### Risks
- Adding a top-level key to the gate's JSON output must not violate closed-schema assertions in existing battery families. (Verified: `limine-pin-battery-r93.py:Case.finish()` asserts specific pin keys, `on_panic`, and `unverified_image_lines`, but does not reject additional top-level metadata keys).

### Verification
Run `python3 tools/check-limine-pins.py --live --limine-version auto` and assert `limine_version_source == "probe"`, `limine_version == "12.9.4"`, and `limine_executable_path == "/usr/bin/limine"`. Verify that `limine-pin-battery-r93.py` battery runs (96 families) pass 96/96 with 0 error rows.

---

## 2. Fleet Scan for Conflicting Ground

### Scan Commands Executed
```sh
# Scan 1a: PROVINCE.md and SKILL.md
grep -rl -i -e 'bwrap' -e 'unshare-all' -e 'limine' -e 'oracle' /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md /home/vgpnk/Projects/shokunin/*-shokunin/SKILL.md 2>/dev/null

# Scan 1b: Sibling corpus/knowledge/
grep -rl -i -e 'bwrap' -e 'unshare-all' -e 'limine' -e 'oracle' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge/ 2>/dev/null

# Verification of complete absence of Limine in sibling corpus/knowledge:
grep -rn -i 'limine' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge/ 2>/dev/null | grep -v '/tsukuroi-shokunin/'
# (exit 1, 0 output lines — proven absence)
```

### Synthesis on the Two Ground Targets

#### (a) The Judge-Oracle Isolation Rule
- **Definition in Tsukuroi (`corpus/knowledge/limine-r92-oracle-isolation.md:OI1-OI4`)**:
  A test battery launching a gate as a child process cannot certify a gate that reads the battery's own oracle. The launcher must close `sys.path[0]` and sibling import channels by copying the gate into a private, isolated directory and running `python3 -I`. Absolute-path, `/proc`, and environment channels must be closed via `bwrap --unshare-all --die-with-parent --new-session --clearenv` with read-only `/usr` and `/etc`, private `/dev`, `/proc`, and `/tmp`, restricted allowlists, and PIDs `["1","2"]`.
- **Sibling Stance**:
  - `kumitate-shokunin` (`corpus/knowledge/agent-isolation-substrates.md`): Focuses on *agent seat containment* to prevent git/jj working copy collision, unshared namespaces, and `/proc/1/environ` leakage. It is **silent** on the battery-versus-gate judge-oracle isolation contract (the `sys.path[0]` copy isolation pattern).
  - `tameshi-shokunin` (`corpus/knowledge/guard-kill-closure.md`, `regression-tally-completeness.md`, `hermetic-env-differential.md`): Focuses on running untrusted mutants inside a bwrap envelope with `env -i`. It is **silent** on the gate-oracle import isolation contract.
  - `kengaku-shokunin` (`corpus/knowledge/tb2-cancel-async-tasks-grader.md`, `tb2-openssl-selfsigned-cert-grader.md`): Uses bwrap `--unshare-all` for terminal benchmark task grading sandboxes. **Silent** on the judge-oracle channel closure.
  - All other sibling lanes: **Silent** on the judge-oracle isolation rule.
  - **Verdict**: **Zero conflicts**. Sibling usage of `bwrap` is compatible and substrate-aligned, but none defines or contradicts the judge-oracle isolation rule.

#### (b) The Limine 12.9.5 Visibility Boundary
- **Definition in Tsukuroi (`limine-r92-oracle-isolation.md:EV1-EV5`, `limine-version-probe-r93.md:VP1-VP4`)**:
  In Limine $\le$ 12.9.4, when the first physical line is an entry line, the cut guard (`c > config_addr`) is false and the whole file remains visible as global options. In Limine $\ge$ 12.9.5 (`create_menu_tree()`), the cut occurs before the entry line, and line-end NUL termination prevents `config_get_value` from reading any subsequent body lines, making first-line-entry files expose no global keys.
- **Sibling Stance**:
  - Every single sibling repository in the fleet is completely **silent** on Limine configuration parsing, the `create_menu_tree()` cut, and the 12.9.5 visibility boundary.
  - `grep -rn -i 'limine' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge/` yielded exactly 0 matches outside `tsukuroi-shokunin`.
  - **Verdict**: **Zero conflicts**. `tsukuroi-shokunin` holds exclusive fleet ownership of the Limine bootloader visibility boundary.

### Sibling Overlap Table

| Repo / File | What it Holds | Conflict / Duplicate / Silent | Recommendation |
|---|---|---|---|
| `kumitate-shokunin/corpus/knowledge/agent-isolation-substrates.md` | Seat isolation substrates: bwrap `--unshare-all --clearenv` with `env -i` immediate parent; PID 1 environ leakage prevention; git/jj working tree boundaries. | **Silent** on judge-oracle isolation; **Silent** on Limine 12.9.5. Compatible on bwrap sandbox mechanisms. | Cite as peer evidence for bwrap PID-1 namespace behavior; do not absorb seat orchestration into tsukuroi. |
| `tameshi-shokunin/corpus/knowledge/guard-kill-closure.md` | Probes run under bwrap envelope with `env -i`, private `/tmp`, PID and network namespaces to evaluate mutation kill closure. | **Silent** on judge-oracle isolation; **Silent** on Limine. Compatible on hermetic sandbox execution. | Retain as reference for test runner hermetic execution. |
| `tameshi-shokunin/corpus/knowledge/regression-tally-completeness.md` | Analysis of bwrap `--unshare-all` (noting 2 of 6 flags are try-else-skip) and `--clearenv` limitations. | **Silent** on judge-oracle isolation; **Silent** on Limine. | Cite for bwrap namespace flag fidelity (supporting observation on S378). |
| `tameshi-shokunin/corpus/knowledge/oracle-anchored-survivors.md` | Classification of mutation test survivors against test oracles (citing Canedo 2026). Uses "oracle" as specification truth. | **Silent** on judge-oracle isolation; **Silent** on Limine. | Independent domain; no action required. |
| `kengaku-shokunin/corpus/knowledge/tb2-cancel-async-tasks-grader.md` | Evaluation sandbox using bwrap `--unshare-all` with `/usr` and `/etc` ro, `/app` writable. | **Silent** on judge-oracle isolation; **Silent** on Limine. | Independent domain (benchmark grading). |
| `mori-shokunin/corpus/knowledge/userns-runway-r98.md` | Analysis of `max_user_namespaces` depletion leading to ENOSPC errors on unprivileged `bwrap` invocations. | **Silent** on judge-oracle isolation; **Silent** on Limine. | Monitor when running high-concurrency isolated battery runs. |
| `chousa-shokunin/corpus/knowledge/grep-pin-r35.md` | Pinned tool provenance: runs `$cand --version` bounded by timeout, rejects unverified binaries before processing records. | **Silent** on judge-oracle isolation; **Silent** on Limine. Overlaps with version probing pattern (C2). | Cross-lane reference for version probing contracts (see Section 3). |
| `revenger-shokunin/corpus/knowledge/tool-validation-by-function-and-version.md` | Tool validation binds a specific tool function in a specific version, not broad product claims. | **Silent** on judge-oracle isolation; **Silent** on Limine. | Conceptual reference for version-scoped claims. |
| `kaidoku-shokunin` (multiple knowledge entries) | Firmware unpacking and reverse engineering using external oracles (`unsquashfs`, `backhand`). | **Silent** on judge-oracle isolation; **Silent** on Limine. | Independent domain. |
| Sibling `PROVINCE.md` / `SKILL.md` (24 files) | Generic references to reference test oracles, bwrap execution of untrusted tools/mutants. | **Silent** on judge-oracle isolation; **Silent** on Limine. | No conflict. |

---

## 3. Generic Sandbox / Probe Contract Collision Analysis (Item 2)

### Question
Does another lane own a generic sandbox/probe contract this round's C2 would collide with?

### Analysis
Searching sibling `tools/` for `subprocess.run([.*--version` and tool execution patterns reveals three lanes with formalized tool validation / probe patterns:
1. **`chousa-shokunin`**: Owns the **tool provenance verification contract** (`grep-pin-r35.md`, `tools/research-gate.sh:342-363`, `captool_verify`). It verifies external executables (`grep`, `coreutils`, `bash`, `sed`) via `<executable> --version`, bounded by timeout (10s), requiring specific banner strings (`GNU grep`, `GNU coreutils`), and refusing unverified overrides before record processing (exit 2).
2. **`kumitate-shokunin`**: Owns the **agent sandbox containment contract** (`agent-isolation-substrates.md`), specifying how agent seats and child processes are wrapped with `bwrap` and `env -i`.
3. **`souji-shokunin` / `tameshi-shokunin`**: Own environment census and differential tools (`souji-size-census.py`, `env-diff.py`), probing `git --version`, `node --version`, `bash --version`.

### Arbitration Recommendation
- **Tsukuroi reports, never absorbs**:
  `tsukuroi-shokunin`'s C2 `--limine-version auto` is a domain-specific capability for the host bootloader. It queries `limine --version` solely to select the internal parsing era (era A $\le$ 12.9.4 vs era B $\ge$ 12.9.5) when checking `/boot/limine.conf`.
- `tsukuroi-shokunin` must **not** attempt to establish or absorb a general-purpose host tool version probing contract or fleet-wide runner framework.
- The gate's implementation in `check-limine-pins.py` correctly restricts its scope:
  - 5-second timeout on `limine --version`
  - Strict refusal on probe failure (rc 64, empty stdout)
  - Explicit record of `limine_version_source: "probe"`
- If a generic tool-version probing interface is unified across the fleet in a future round, `chousa-shokunin` (as the research/provenance lane) or `souji-shokunin` should own the general contract.

---

## 4. Cross-Source Pattern: Version Probing Census (Item 3)

The pattern "resolve an installed tool's version by running it with `--version`" appears across 15 distinct sibling tool suites:

| Lane | Tool Path | What it Probes | Fails Closed on Probe Failure? | Behavior on Failure |
|---|---|---|---|---|
| `chousa-shokunin` | `tools/research-gate.sh` | GNU coreutils (`mktemp`, `sed`, `mkdir`, `cat`, `rm`, `sort`, `readlink`, `dirname`, `date`, `tr`, `wc`, `od`, `head`, `stat`), GNU `grep`, GNU `env`, GNU `bash` | **Yes** | Refuses with exit 2 (`<NAME>_PROVENANCE refused`) before any record is read; never falls back to an unverified binary. |
| `kaidoku-shokunin` | `tools/round-69/contract-probe.py:140` | `/usr/bin/upx` | **Yes** | Host version evaluates to `None`; pin comparison fails and triggers test arm failure. |
| `kaidoku-shokunin` | `tools/round-70/contract-probe.py:228` | `/usr/bin/upx` | **Yes** | Host version evaluates to `None`; pin comparison fails and triggers test arm failure. |
| `kaidoku-shokunin` | `tools/round-70/packed-elf.py:334` (also r71, r72, r73) | `upx`, `node` | **Yes** | Refuses execution unless banner matches pinned expectation. |
| `kaidoku-shokunin` | `tools/round-50/c1-counter.py:1977` | `unblob`, `node` | **Yes** | Requires `unblob --version` == `26.6.4`, else exits 2. |
| `kaidoku-shokunin` | `tools/round-39/c1-run.sh:258` (also r40, r41, r42, r50, r67) | `unblob`, `rea-agents` (via npx) | **No** | Captures output into receipt metadata; continues with empty string if probe fails. |
| `kaidoku-shokunin` | `tools/round-42/sqfs3-oracle.py:814` | `backhand` | **Yes** | Aborts oracle evaluation if binary fails. |
| `kama-shokunin` | `tools/kama-context-capacity.py:746` | `server_real` (llama.cpp server) | **Yes** | Raises `SetupError('server-version-failed:...')` or `SetupError('server-version-mismatch:...')`. |
| `kama-shokunin` | `tools/round89-router-signatures.py:50` | `a.server` (router server) | **No** | Sets build string to `'?'` and proceeds with HTTP requests. |
| `mado-shokunin` | `tools/mado-verify.sh:3383, 3586` | `walker`, `waybar` | **Yes** | Logs `FAIL` in verification ledger if version output does not match pin. |
| `mori-shokunin` | `tools/mori-round17-jj-regressions.py:1889` | `git`, `jj` | **No** | Records `'absent'` in diagnostic census; does not abort regression harness. |
| `souji-shokunin` | `tools/souji-size-census.py:205` | `git` | **Yes** | `checked()` raises exit 1 on missing git, nonzero exit, or stderr. |
| `souji-shokunin` | `tools/souji-repo-structure.sh:179` | `git` | **No** | Stores `git --version` output in script variable; continues execution. |
| `souji-shokunin` | `tools/cand-e1-regress.sh:427` | `git` | **No** | Emits fallback `'git-absent'` in report header. |
| `tameshi-shokunin` | `tools/env-diff.py:258` | `node`, `bash` | **Yes** | Catches `OSError`/`ValueError`, outputs `ENVDIFF_SETUP:`, and exits 2. |

### General Rule Ownership
- **Recommended Owner**: **`chousa-shokunin`**
- **Justification**:
  `chousa-shokunin` is the designated research and evidence provenance lane. It already formalized the `grep-pin` pattern (`grep-pin-r35.md`) requiring:
  1. Absolute path or verified PATH resolution
  2. Bounded execution timeout
  3. Format/banner string validation
  4. Immediate fail-closed refusal before operational processing
  This directly mirrors the fail-closed discipline adopted by `tsukuroi`'s C2.

---

## 5. Sources Verification: r92 Entry and r93 New Rows (Item 4)

### Verification of `corpus/knowledge/limine-r92-oracle-isolation.md`

Every claim and sentence of `limine-r92-oracle-isolation.md` was audited against the cited sources (S352, S353, S361, S362, S374, S375, S376, S377, S378, S379, S380, S381) and pinned source files in `.ufo/waves/round-92/before/src/`:

1. **OI1 (r91 Oracle Leakage)**:
   - Sourced from `tools/limine-pin-battery-r91.py:1635` (`argv = [sys.executable, gate, ...]`) and receipt `.ufo/waves/round-91/w1/ScribeLesson/receipts/channel-open.json`.
   - **Supported**: Verified line 1635 and receipt existence.
2. **OI2 (Private Copy & Isolated Mode)**:
   - Cites S377 (Python 3 docs `-P`, `-I`).
   - S377 raw documentation: `-I` implies `-E`, `-P`, and `-s`, ensuring neither script directory nor user site is added to `sys.path` and `PYTHON*` variables are ignored.
   - **Supported**: Verified verbatim in `python-3-cmdline.txt`.
3. **OI3 (Mount & PID Namespace Closure)**:
   - Cites S378 (`bwrap.xml`).
   - S378 defines `--clearenv` as unsetting all environment variables except `PWD`.
   - *Discrepancy / Nuance Flagged*: The entry states `S378: --unshare-all unshares user, ipc, pid, net, uts and cgroup`. In `bwrap.xml`, `--unshare-all` is defined as:
     `--unshare-user-try --unshare-ipc --unshare-pid --unshare-net --unshare-uts --unshare-cgroup-try`.
     The user and cgroup namespace unshares are *try-else-skip* (`-try`), not unconditional hard failures. This is technically supported as the definition of `--unshare-all`, but the try-else-skip semantic is an important qualification (previously observed in `tameshi` round 30).
4. **EV1 (12.9.4 Visibility Exception)**:
   - Cites S376 (`limine-v12.9.4-common_lib_config.c`, raw 638-650).
   - In 12.9.4, `init_config` scans `c > config_addr` before setting `c[-1] = 0`. When the first line is an entry, `c == config_addr`, the condition is false, and the cut is skipped.
   - **Supported**: Verified lines 638-651 in pinned source.
5. **EV2 (12.9.5 In-Place Parse)**:
   - Cites S379 (`limine-v12.9.6-common_lib_config.c`, raw 328-330, 362-365, 666, 668, 733+).
   - *Technical Nuance Flagged*: EV2 states `cuts before it (if (p > config_addr) { *(p - 1) = '\0'; }, raw 328-330), then NULs the end of the label line (raw 362-365)`.
     When line 1 is an entry (`p == config_addr`), `p > config_addr` is false, so the cut before it does *not* execute. Instead, line 363 (`*p = '\0'`) terminates the label line, confining `config_addr` to the label line alone and preventing `config_get_value` from reading any subsequent lines. The substantive conclusion (no global keys exposed) is fully supported.
6. **EV3 (12.9.5 and 12.9.6 Identity)**:
   - `config.c` in 12.9.5 and 12.9.6 both have SHA256 `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60`.
   - **Supported**: Verified byte identity.
7. **EV4 (ChangeLog Statement)**:
   - Cites S380 (ChangeLog) and S381 (Issue #700).
   - Quote: *"A config whose first line is an entry has had no global options since 12.9.5, whereas every option in it used to count as global"*.
   - **Supported**: Verified verbatim in `limine-v12.9.6-ChangeLog.txt` under `Miscellaneous:`. Issue #700 verifies reporter's trace of `p == config_addr` and NixOS `extraConfig`.
8. **EV5 (Host Version Stance)**:
   - *Flagged Statement*: `the gate never guesses the host version by shelling out, so its answer is a function of the conf and the declared version only.`
     This was the r92 architectural design statement for `check-limine-pins.py` V2. It is not supported by any external cited source (S352-S381) and is explicitly superseded in Round 93 by C2's `--limine-version auto` probe.

### Verification of Round 93 New Sources (S382, S383, S384)

The L1 landed rows S382, S383, and S384 in `corpus/SOURCES.md` and `corpus/knowledge/limine-version-probe-r93.md`. Verified against files in `.ufo/waves/round-93/before/src/`:
- **S382** (`v12.9.5 common/lib/config.c`):
  SHA256: `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60`.
  Carries `if (p > config_addr) { *(p - 1) = '\0'; }` at raw lines 328-330 and label-end NUL at lines 362-365. Byte-identical to 12.9.6. **Fully supported**.
- **S383** (`v12.9.5 ChangeLog`):
  SHA256: `d2e08cc4a4bffc4b598b9baf43435cbf05f2c76edcaf89f9ba18f35c42b51779`.
  Raw lines 8-9: *"Parse the config in linear time. Configs with thousands of entries were slow to load."* **Fully supported**.
- **S384** (`v12.9.5 host/limine.c`):
  SHA256: `4da21c7cceae238075612643b845cb63e06cc184977e950d5e6374329bc31ec0`.
  Raw lines 2089-2091 dispatch `--version` to `version()`.
  *Minor Line-Number Erratum Flagged*: In S384 citation text, the print is cited at raw 2029. In `limine-v12.9.5-host_limine.c`, line 2029 is blank; `puts("Limine " LIMINE_VERSION);` is at line 2035, while `--version-only` prints at line 2031 (`puts(LIMINE_VERSION)`). The text content is completely accurate.

---

## ## Verdict

Evidence supports claims **C1** and **C2**:
1. **C1 (Depth 8)**: Supported by the four new families (`ERA-EXACT-125`, `ERA-B-FIRST-BODY`, `ERA-B-U1`, `REFUSAL-VERSIONS`) resolving unexercised boundary conditions in Limine 12.9.5/12.9.6 config parsing, verified by code and source byte analysis.
2. **C2 (Operability 9)**: Supported by `check-limine-pins.py` V3 `--limine-version auto` implementation, which executes `limine --version` read-only with a 5s timeout, records `limine_version` and `limine_version_source: "probe"`, and fails closed with rc 64 on probe failure, matching the cross-lane fail-closed standard demonstrated in `chousa` (`grep-pin-r35.md`).
3. **Absence of Sibling Contradictions**: Sibling scans establish zero ground contradictions on the judge-oracle isolation contract and zero presence of Limine visibility rules outside `tsukuroi-shokunin`.

**Receipts**:
- `.ufo/waves/round-93/w1/ConnectorOverlap/scan1-ground-census.txt`
- `.ufo/waves/round-93/w1/ConnectorOverlap/scan2-version-probing.json`
- `.ufo/waves/round-93/w1/ConnectorOverlap/sources-r92-r93-verification.txt`
