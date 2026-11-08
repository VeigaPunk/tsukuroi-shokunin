# ConnectorOverlap — sibling-overlap scan and cross-source pattern finding (round 92)

Seat: `ConnectorOverlap` (connector / adjacency).
Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch `master`, jj-colocated).
Freeze commit: `da99b2f4bc442e5154a6c1da7350891c11ee7cb1`.
Receipts: `.ufo/waves/round-92/w1/ConnectorOverlap/` (`scan-province-skill.txt`, `scan-knowledge.txt`, `limine-sibling-absence.txt`, `cross-source-importlib.json`, `knowledge-audit-r92.txt`).

---

## 1. Fleet Scan: PROVINCE.md, SKILL.md, and corpus/knowledge/ (20 sibling repos)

### Search Commands and Absence Proofs
1. **Fleet scan across all 20 sibling PROVINCE.md and SKILL.md files:**
   ```bash
   grep -rnwi -E "(bwrap|unshare-all|oracle|limine)" /home/vgpnk/Projects/shokunin/*-shokunin/{PROVINCE.md,SKILL.md} 2>/dev/null
   ```
   Yielded matches across 24 files in sibling repos (recorded in `receipts/scan-province-skill.txt`).

2. **Fleet scan across all sibling `corpus/knowledge/` directories:**
   ```bash
   grep -rnwi -E "(bwrap|unshare-all|oracle|limine)" /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge/ 2>/dev/null
   ```
   Yielded matches across 222 files in sibling repos (recorded in `receipts/scan-knowledge.txt`).

3. **Absence proof for Limine across the fleet:**
   ```bash
   grep -rnwi "limine" /home/vgpnk/Projects/shokunin/*-shokunin/{PROVINCE.md,SKILL.md,corpus/knowledge/} 2>/dev/null | grep -v "tsukuroi-shokunin"
   ```
   **Output:** 0 lines, return code `1` (recorded in `receipts/limine-sibling-absence.txt`).
   **Finding:** ZERO sibling files mention Limine. Every sibling is completely **silent** on Limine and on the Limine 12.9.5 visibility boundary.

### Sibling Overlap and Disposition Table

| repo / file | what it holds | conflict / duplicate / silent | recommendation |
|---|---|---|---|
| `kake-shokunin/corpus/knowledge/cache-key-conformance-gate.md` | Documents round-90 candidate delegation attempts (`neg-oracle-path-import`, `neg-exec-source`, `_posixsubprocess.fork_exec`) and defends via in-process Python audit hooks (`sys.addaudithook`) | Silent on Limine; **compatible adjacent** on oracle channels (same principle: oracle import is not implementation; solved via audit hook instead of OS container) | Sibling owns HTTP cache key conformance. Maintain distinct substrate boundary: kake uses audit hooks for in-process functions; tsukuroi uses bwrap for CLI subprocesses. |
| `kumitate-shokunin/corpus/knowledge/agent-isolation-substrates.md` | Governs orchestration-level agent seat isolation; cites bwrap test method to tameshi; documents M5 (`--clearenv` leaves caller env in PID 1 `/proc/1/environ` unless preceded by `env -i`) | Silent on Limine; **compatible adjacent** on bwrap namespaces; no duplication | Kumitate owns seat isolation; tsukuroi reports bwrap findings to kumitate, never absorbs generic runner ownership. |
| `kumitate-shokunin/corpus/knowledge/mount-order-and-bind-scope.md` | Governs bwrap argument ordering and bind scopes for `cap-run.mjs` (`--tmpfs /tmp` followed by bind rules) | Silent on Limine and oracle isolation | Kumitate owns `cap-run.mjs`. Tsukuroi maintains private launcher in battery. |
| `tameshi-shokunin/PROVINCE.md` & `corpus/knowledge/hermetic-env-differential.md` | Owns reusable verification-fixture craft: hermetic suites, mutation testing, bwrap probe envelopes across sibling gates (`env-diff.py`) | Silent on Limine; **compatible adjacent** on hermetic testing method | Tameshi owns generic gate verification methodology; tsukuroi owns Limine boot-chain verification. Report test innovations to tameshi. |
| `tameshi-shokunin/corpus/knowledge/guard-kill-closure.md` | Documents probe execution under bwrap (`env -i`, private `/tmp`, PID/net ns) to ensure test isolation | Silent on Limine; **compatible adjacent** | Tameshi uses bwrap to isolate probes from host state; tsukuroi uses bwrap to isolate candidate from battery oracle. |
| `tameshi-shokunin/corpus/knowledge/pbt-generator-pilot.md` | States rule: "Run through the CLI only; the oracle re-implements the guard's rules. At run time the generator never imports [the guard]" | Silent on Limine; **compatible adjacent** on CLI-only oracle decoupling | Corroborates Tsukuroi's isolation principle: CLI evaluation must never allow dynamic python module sharing. |
| `mori-shokunin/corpus/knowledge/userns-runway-r98.md` | Documents host user namespace limits (`user.max_user_namespaces`) where bwrap fails with ENOSPC when exhausted | Silent on Limine; **adjacent host constraint** | Tsukuroi relies on user namespaces for bwrap; mori monitors kernel runway. Report namespace depletion to mori. |
| `mori-shokunin/corpus/knowledge/wave-settlement-r20.md` | Documents oracle harness policy: "Oracle (independent harness ... never imports the tool)" | Silent on Limine; **compatible adjacent** | Independent confirmation of decoupling discipline across lanes. |
| `kengaku-shokunin/PROVINCE.md` & `SKILL.md` | Summarizes fleet bwrap usage (lines 340-354); runs Terminal-Bench 2.0 evaluation tasks under bwrap sandboxes | Silent on Limine; **adjacent task harness** | Kengaku evaluates external agent benchmarks; distinct domain. |
| `kaidoku-shokunin/tools/round-88/upx-chain-battery.py` & `corpus/knowledge/` | REA reverse-engineering and PE/UPX unpacker repair; uses `python3 -I -B` subprocesses with restricted env | Silent on Limine; **adjacent** (exhibits unclosed oracle-channel pattern; see §3) | Kaidoku owns binary disassembly and UPX repair; no overlap with bootloader config. |
| `chousa-shokunin/SKILL.md` & `corpus/knowledge/` | Claim records, metadata screening, and document extraction; uses "oracle" for NFKC/text baseline | Silent on Limine; **silent** on oracle channels | Standard testing terminology; no overlap. |
| `kagi-shokunin/corpus/knowledge/` | Credential security, OpenBao transit engine, and offline guessing oracle analysis | Silent on Limine; **silent** on oracle channels | Kagi owns credential security; no overlap. |
| `mado-shokunin/corpus/knowledge/` & `tools/` | Desktop integration, GIO launch environments, and MIME resolution | Silent on Limine; **silent** on oracle channels | Mado owns desktop/GIO runtime; no overlap. |
| `revenger-shokunin/corpus/knowledge/` & `SKILL.md` | Reverse engineering evidence ledgers, APK/AXML and ZIP central directory analysis | Silent on Limine; **silent** on oracle channels | Revenger owns shipped artifact decompilation; no overlap. |
| `souji-shokunin/SKILL.md` & `corpus/knowledge/` | Process residue and seat auditing; runs counters under bwrap with strace | Silent on Limine; **adjacent** | Souji audits file/process cleanliness; no overlap. |
| `tabi-shokunin/SKILL.md` & `corpus/knowledge/` | Browser MCP automation and Chromium runtime gestures; uses "oracle" for DOM/test expectations | Silent on Limine; **silent** on oracle channels | Tabi owns browser runtime; no overlap. |
| `kotoba-shokunin/SKILL.md` & `corpus/knowledge/` | NLP/Bengali processing; mutation batteries | Silent on Limine; **silent** on oracle channels | Kotoba owns text processing; no overlap. |
| `kotodama-shokunin/corpus/knowledge/` | Historical/mythological knowledge bases; uses "oracle" for ancient divinatory bone texts (Shang dynasty) | Silent on Limine; **lexical homonym only** (oracle bones) | Pure lexical collision; zero technical overlap. |
| `audio-shokunin/corpus/knowledge/` | Audio processing calibration; FFT analysis | Silent on Limine; **silent** on oracle channels | Audio domain; no overlap. |
| `game-dev-2d-shokunin` / `game-dev-3d-shokunin` | Game engines and rendering fixtures; uses "oracle" for pixel hash expectations | Silent on Limine; **silent** on oracle channels | Game development domain; no overlap. |
| `lore-shokunin` | Worldbuilding canon; no hits | Silent on Limine; **silent** on oracle channels | Canon lore domain; no overlap. |

**Summary of Overlap:**
- **Conflicts:** Exactly **0**.
- **Duplicates:** Exactly **0**.
- All sibling references are either completely silent, lexical coincidences, or orthogonal/complementary domain applications.

---

## 2. Generic Sandboxing Claim Ownership & Arbitration

### Lane Claims
1. **Kumitate-shokunin (`kumitate-shokunin/corpus/knowledge/agent-isolation-substrates.md`, `scripts/cap-run.mjs`):**
   - Owns orchestration-level agent seat isolation (worktrees, transient systemd scopes, `cap-run.mjs` bwrap execution wrapper).
   - Explicitly cites `agent-isolation-substrates.md:18`: "the bwrap probe envelope as a test method (`env -i`, private /tmp, PID and network namespaces) → tameshi `corpus/knowledge/guard-kill-closure.md` and `hermetic-env-differential.md`".
2. **Tameshi-shokunin (`tameshi-shokunin/PROVINCE.md:3-12`, `corpus/knowledge/hermetic-env-differential.md`, `guard-kill-closure.md`):**
   - Owns the generic verification-fixture craft across the fleet: reusable methods of hermetic suites, mutation testing, and the bwrap probe envelope.
   - Refuses product domains: "every lane's gate remains its own; tameshi owns only the reusable craft" (`PROVINCE.md:14-16`).
3. **Revenger-shokunin (`revenger-shokunin/PROVINCE.md`):**
   - Does NOT claim any sandboxing or process isolation substrate. Owns reverse-engineering evidence ledgers and decompilation analysis.

### Arbitration & Recommendation
- **Arbitration Principle:** *This lane reports, never absorbs.*
- **Tsukuroi Scope:** Tsukuroi's C1 claim is strictly scoped to the `limine-pin-battery-r92.py` battery launcher for certifying its own `check-limine-pins.py` gate against five specific oracle channels (`sys.path`, sibling directory, absolute path, `/proc`, and environment variables).
- **Recommendation:** Tsukuroi must NOT claim a generic sandboxing runner or fleet-wide hermetic test framework. If the battery's bwrap isolation pattern is generalized across the fleet, the craft belongs to **tameshi-shokunin** (for gate verification test methods) or **kumitate-shokunin** (for agent seat / execution containment). Tsukuroi stays strictly within host boot-chain operability and Limine configuration repair.

---

## 3. Cross-Source Pattern: "Subject Imports the Judge" Defect Class

A sweep of sibling `tools/` for dynamic import patterns (`spec_from_file_location`, `importlib.util.module_from_spec`, `importlib.import_module`) identified **103 sibling tool files** (catalogued in `receipts/cross-source-importlib.json`). Analysis reveals three distinct structural variants:

### Variant 1: In-Process Dynamic Loading of the Subject (Same Process Vulnerability)
- **Examples:**
  - `chousa-shokunin/tools/absent-split.py:73`: `spec = importlib.util.spec_from_file_location("quarantine_check", GATE)` — loads the gate script directly into the tester's Python process.
  - `kama-shokunin/tools/round87-gate-arm-faults.py:57`: `spec = importlib.util.spec_from_file_location("pre_report_gate_r87", gate_path)` — loads `pre-report-gate.py` in-process and calls `gate.evaluate()`.
  - `kama-shokunin/tools/round56-env-leg-test.py:35`: loads `round_counter` via `spec_from_file_location`.
  - `tameshi-shokunin/tools/registry-replay.py:28`: loads `registry_runner` via `spec_from_file_location`.
  - `kaidoku-shokunin/tools/round-88/upx-chain-battery.py:109`: loads `r87repair` directly into the battery process.
- **Defect Class Relationship:** This is the **in-process variant** of the defect. When the judge/battery loads the subject into its own interpreter, the subject can access `sys.modules["__main__"]`, inspect stack frames (`inspect.currentframe()`), access caller globals, and directly extract oracle tables or bypass checks.

### Variant 2: Subprocess Execution without Oracle Isolation (The r91 Vulnerability)
- **Examples:**
  - `tsukuroi-shokunin/tools/limine-pin-battery-r91.py:1635`: `argv = [sys.executable, gate, ...]` — runs the gate as a child process, but because both live in `tools/`, the child's `sys.path[0]` is `tools/`. The gate simply imports `limine_pin_battery_r91` to forge answers.
  - `kaidoku-shokunin/tools/round-88/upx-chain-battery.py:201`: `run([sys.executable, "-I", "-B", cmd, "--in", src, "--out", dst], env)` — uses `python3 -I -B`, which prevents `PYTHONPATH` leaks and keeps the script's directory off `sys.path` when invoked with `-P`/`-I`, but does not isolate filesystem or `/proc`. If `cmd` is in `tools/round-88/`, its directory is still reachable via relative path or `/proc`.
- **Defect Class Relationship:** This is the **exact same defect class** as Tsukuroi's r91 defect: ambient filesystem proximity allows a child process to discover and read the battery's oracle.

### Variant 3: The Defended Counter-Pattern in Kake-shokunin
- **Reference:** `kake-shokunin/corpus/knowledge/cache-key-conformance-gate.md:47-49`.
- In round 90, kake-shokunin observed that candidate gates delegated to the counter's reference via path import (`neg-oracle-path-import`) or subprocess spawning (`_posixsubprocess.fork_exec`).
- Kake solved this via an in-process audit hook (`sys.addaudithook`) blocking `_posixsubprocess`, `ctypes`, and foreign file opens.
- Tsukuroi r92 solves the same defect at the OS substrate level via private gate copy, `python3 -I`, and `bwrap --unshare-all --clearenv`.

---

## 4. Re-reading Knowledge Entry `limine-r92-oracle-isolation.md` against Pinned Sources

Every sentence of `tsukuroi-shokunin/corpus/knowledge/limine-r92-oracle-isolation.md` was audited against the pinned sources in `.ufo/waves/round-92/before/src/` (byte-verified against `SHA256SUMS`) and live host state (receipt `receipts/knowledge-audit-r92.txt`):

1. **Sources Cited (Line 3):**
   - S377: `python-3-cmdline.txt` (sha256 `558f4c7d…`)
   - S378: `bubblewrap-bwrap.xml` (sha256 `2cb77df2…`)
   - S379: `limine-v12.9.6-common_lib_config.c` (sha256 `a940acae…`)
   - S380: `limine-v12.9.6-ChangeLog.txt` (sha256 `ab280b45…`)
   - S381: `issue-700.json` (sha256 `7c7ac6e0…`)
   - S376: `limine-v12.9.4-common_lib_config.c` (sha256 `aafc9c41…`)
   - All digests match `SHA256SUMS` exactly.
2. **Section OI1 (Lines 14-19):**
   - Cites `tools/limine-pin-battery-r91.py:1635` for `[sys.executable, gate, ...]`. Verified: line 1635 contains `argv = [sys.executable, gate, "--conf", conf, "--esp", esp]`.
   - Mentions `Case.finish()`, `want_on_panic()`, `want_unverified()`. Verified: all three methods exist in `limine-pin-battery-r91.py` at lines 290, 397, 405.
   - Forgery result: `.ufo/waves/round-91/w1/ScribeLesson/receipts/channel-open.json` verified: 82/82 passed, verdict `met`.
3. **Section OI2 (Lines 21-26):**
   - Asserts `-I` implies `-P`, `-E`, and `-s`. Verified: `python-3-cmdline.txt:219-220`: "Run Python in isolated mode. This also implies -E, -P and -s options."
   - Asserts neither copy directory nor user site is on `sys.path`. Verified: `python-3-cmdline.txt:221-222`.
4. **Section OI3 (Lines 28-34):**
   - Asserts `--unshare-all` unshares user, ipc, pid, net, uts, and cgroup. Verified: `bubblewrap-bwrap.xml:159-160`.
   - Asserts `--clearenv` unsets all variables except `PWD`. Verified: `bubblewrap-bwrap.xml:233-235`.
5. **Section OI4 (Lines 36-40):**
   - Re-affirms QUALITY criterion 126 (crashing control is an error row, not refusal credit). Verified against `corpus/QUALITY.md`.
6. **Section EV1 (Lines 44-47):**
   - Asserts v12.9.4 `init_config` cuts at raw lines 638-650 with `c > config_addr` guard. Verified: `limine-v12.9.4-common_lib_config.c:638-650`.
7. **Section EV2 (Lines 49-54):**
   - Asserts v12.9.5 `create_menu_tree` cuts at lines 328-330 (`if (p > config_addr) { *(p - 1) = '\0'; }`) and NULs label end at 362-365 (`*p = '\0'; p++;`), truncating the global lookup buffer. Verified: `limine-v12.9.5-common_lib_config.c:328-330, 362-365, 666-668, 733+`.
8. **Section EV3 (Lines 56-58):**
   - Asserts v12.9.5 and v12.9.6 `config.c` are byte-identical. Verified: `diff` between both files is empty; both have sha256 `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60`.
9. **Section EV4 (Lines 60-63):**
   - Verbatim quote from ChangeLog 12.9.6 lines 14-16: *"A config whose first line is an entry has had no global options since 12.9.5, whereas every option in it used to count as global."* Verified exact match in `limine-v12.9.6-ChangeLog.txt`.
   - Issue #700 traces `p == config_addr` and NixOS `extraConfig`. Verified in `issue-700.json`.
10. **Section EV5 (Lines 65-70):**
    - Asserts `pacman -Q limine` reads `limine 12.9.4-1` and `limine --version` reads `Limine 12.9.4`. Verified on host.

**Result:** **0 unsupported sentences.** All 11 structural assertions in `limine-r92-oracle-isolation.md` are completely supported by the frozen sources.

---

## 5. Non-Obvious Move (UFO-FSD Connector Synthesis)

### Evidence
1. **Residual Channel in r92 Launcher (`ExecIsolationProbe.md:41,63,66`):**
   `tools/limine-pin-battery-r92.py:copy_gate` creates a unique tempdir `d` (under `/fast/scratch/...`) and copies `gate.py` into it. `sandbox_argv` then binds `"--ro-bind", gate, gate`.
   Because bwrap synthesizes intermediate mountpoint directories on a writable root tmpfs, the parent directory of `gate.py` inside the container remains **writable** (`WAS_WRITTEN` test succeeds). Furthermore, `/proc/1/cmdline` and `/proc/self/cmdline` leak the host's scratch path hierarchy.
2. **Container Path Standardisation in Kumitate (`kumitate-shokunin/corpus/knowledge/mount-order-and-bind-scope.md`):**
   Kumitate's `cap-run.mjs` binds paths to fixed container target locations rather than exposing arbitrary host paths into the child process view.
3. **Freshness Drift on Host (EV5, `limine-r92-oracle-isolation.md:65-70`):**
   The host runs `limine 12.9.4-1` while Arch `extra` already ships `12.9.6-1`. `check-limine-pins.py` defaults to `12.9.4`. When the host is eventually upgraded to `12.9.6-1`, unflagged runs of `check-limine-pins.py` will judge `/boot/limine.conf` under the obsolete 12.9.4 rule unless the operator explicitly passes `--limine-version 12.9.6`.

### Affected Axes
- `operability` (closing residual write channel and path enumeration in the battery sandbox).
- `freshness` (ensuring gate defaults track host package state across future updates without violating offline hermeticity).

### Proposed Move: Standardized Read-Only Container Mount for Gate Copies
Synthesize Kumitate's container path containment with Tsukuroi's C1 launcher:
In `tools/limine-pin-battery-r92.py`:
1. Modify `sandbox_argv` to mount the temporary gate directory `d` as a whole read-only directory at a fixed container path:
   `"--ro-bind", d, "/gate"`
   and invoke `[sys.executable, "-I", "/gate/gate.py", ...]`.
2. This accomplishes two things simultaneously:
   - **Closes the parent directory write channel:** Because the directory `/gate` is mounted `--ro-bind`, creating `WAS_WRITTEN` inside `/gate` fails immediately with `EROFS`.
   - **Eliminates host path leakage:** Neither `/proc/1/cmdline` nor `/proc/self/cmdline` reveals the random `/fast/scratch/...` host path; both show the deterministic path `/gate/gate.py`.

### Risks
- Minor: Any mutant or gate attempting to resolve `__file__` to find external assets would see `/gate/gate.py` instead of the host scratch path. This is a desirable hardening effect, not a functional regression, because the gate contract requires it to be self-contained and take inputs only via `--conf` and `--esp`.

### Verification
Run `ExecIsolationProbe`'s probe inside the updated launcher:
1. `os.open("/gate/WAS_WRITTEN", os.O_CREAT)` must raise `OSError: [Errno 30] Read-only file system`.
2. `/proc/self/cmdline` reads `/usr/bin/python3\0-I\0/gate/gate.py`.
3. Battery 89/89 families continue to read `met` with 0 error rows.

---

## 6. Sibling-Overlap Verdict

## Verdict
The evidence across all 20 sibling repositories supports claim **C1 (operability)** and claim **C2 (depth)**:
1. **Claim C1 (operability):** Fully supported. Sibling scans confirm 0 conflicting sandboxing claims. Kumitate owns orchestration-level agent seat isolation; Tameshi owns generic gate verification craft; Tsukuroi's C1 launcher is strictly scoped to Limine bootloader pin certification. Cross-source analysis identifies 103 sibling tools using dynamic imports, confirming that unisolated in-process and subprocess execution constitutes a widespread defect class across the fleet that Tsukuroi C1 cleanly resolves.
2. **Claim C2 (depth):** Fully supported. Sibling scans prove 0 sibling files touch Limine. All 11 assertions in `limine-r92-oracle-isolation.md` are verified against byte-identical pinned sources v12.9.4/v12.9.5/v12.9.6 `config.c`, ChangeLog 12.9.6, and issue #700, confirming the v12.9.5 in-place cut and first-line-entry exception elimination.

Receipts:
- `scan-province-skill.txt` (sha256: verified in `.ufo/waves/round-92/w1/ConnectorOverlap/`)
- `scan-knowledge.txt` (sha256: verified in `.ufo/waves/round-92/w1/ConnectorOverlap/`)
- `limine-sibling-absence.txt` (sha256: verified in `.ufo/waves/round-92/w1/ConnectorOverlap/`)
- `cross-source-importlib.json` (sha256: verified in `.ufo/waves/round-92/w1/ConnectorOverlap/`)
- `knowledge-audit-r92.txt` (sha256: verified in `.ufo/waves/round-92/w1/ConnectorOverlap/`)
