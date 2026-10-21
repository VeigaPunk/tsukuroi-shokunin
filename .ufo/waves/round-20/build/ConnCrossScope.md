# ConnCrossScope — Proposal connector item: explicit ownership attribution and forbidden writes

Seat: `TsukuroiR19Recovery.ConnCrossScope-2` (author-dispatched connector leaf; not outside closure).
Role: UFO-FSD connector.
Lane: `tsukuroi-shokunin` (production lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`).
Baseline: `0cbc34dd6b20896085a8fb07943e3ea4027d8472` (`.ufo/waves/round-20/preregister.json:3`; `seeded-implementation.json:4`).
Preregistered claims: C1 adjacency (lowest, ordinal 8), C2 operability (ordinal 9), C3 calibration (ordinal 9); all ordinal deltas 0.
NO-EXEC: read/grep/glob only; no shell/eval, imports, gates, selftests, host probes or target execution.
Scope: executed=none.

---

## 1. Declared axes

1. **C1 Adjacency** (ordinal 8, lowest axis, delta 0):
   - Metric: `ownership_corrections` (before: 0, after: 1).
   - Evaluator: `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`.
   - Scope: Explicit sibling-declaration wording for OUT-009 at retained pinned scope; no integrator arbitration or write authority.

2. **C2 Operability** (ordinal 9, delta 0):
   - Metric: `object_selector_tools` (before: 0, after: 9).
   - Evaluator: `python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors`.
   - Supporting repair: Exec-log `systemctl` mutation filter (`systemctl_violations`) in `tools/check-recheck-commands.py` (`assess_exec_log`), distinguishing mutating verbs (`restart`, `daemon-reload`, `enable`, etc.) from read-only query verbs (`cat`, `show`, `status`, `list-units`, `list-timers`, `is-active`, etc.).

3. **C3 Calibration** (ordinal 9, delta 0):
   - Metric: `audit_live_map_errors` (before: 1, after: 0).
   - Evaluator: `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map`.
   - Scope: Operative `boot-chain-audit` live summary map returns `0 CONSISTENT` or `2 UNKNOWN`; `1` is selftest failure only, never live DEGRADED. Append named R19 false-erratum and non-prefix disclosure.

---

## 2. Evidence and local repository provenance

1. **Province and handoff boundary:**
   - `PROVINCE.md:25-28`: Tsukuroi tracks *state and health*, not internals; refuses binary reverse engineering of drivers (`→ kaidoku/revenger`); never installs, upgrades, or removes packages; never restarts services.
   - `PROVINCE.md:51` (ADJ-06): Driver/firmware/package mechanism requiring shipped-artifact reverse engineering beyond health inventory routes to `protocol integrator — kaidoku/revenger ownership unresolved`. Minimum evidence: exact question, authorized artifact path/digest, capture time, OS probe/exit; "Request an ownership ruling before any RE work; do not invoke a target or forward raw cores."
   - `PROVINCE.md:79-80` (Frontier): "Kaidoku and revenger both declare shipped-artifact RE. The integrator must arbitrate this shared scope; tsukuroi neither picks an owner nor absorbs it."
   - `PROVINCE.md:129` (Round 19 OUT-009 table row): Proposition asserted: "Revenger owns shipped-artifact reverse engineering (binaries, packages, APKs) with an observation/inference/unknown evidence ledger; tsukuroi tracks state only."

2. **Historical falsifier and outside closure findings:**
   - `.ufo/waves/round-19/falsify/FxConnOverlap.md:46`: Direct contradiction identified in round 19. Revenger's pinned text claims the same RE domain as Kaidoku, while Tsukuroi states the integrator must arbitrate. The proposition "Revenger owns" resolved an unresolved dispute in Tsukuroi's voice. Furthermore, the proposition said unqualified "packages", whereas Revenger specifies "Electron/JavaScript packages" (`.../siblings/revenger/cf02419276e5/PROVINCE.md:3-5`); Tsukuroi separately owns pacman package state and `.pkg.tar.zst` discipline (`PROVINCE.md:8-9`).
   - `corpus/lessons/round-19-verifier-spotcheck.md:149`: Defect 4 records the scope broadening of OUT-009 and the need to preserve attribution and arbitration.

3. **Pinned sibling declaration:**
   - Snapshot `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md:3-7`: "Owns: reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, browser/Electron runtime evidence — using the REA skill and its toolset..."
   - Snapshot `:25-29`: "Writes only this `revenger-shokunin/` repository under the current interactive dispatch... Domain source checkouts, shared fleet state and sibling repositories remain read-only. No push, global routing changes or substrate/package remediation."
   - Recorded blob SHA-256: `63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f` (`corpus/knowledge/adjacency-anchors-r19.json:118`).

4. **Operative C1 clarification text in production lane:**
   - `PROVINCE.md:148-152` appends:
     ```markdown
     ## R20 ownership clarification — OUT-009

     R20-OUT009: OUT-009 is Revenger's sibling declaration of reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, browser/Electron runtime evidence. It is not a tsukuroi grant of ownership. Kaidoku/Revenger arbitration remains unresolved; ask the protocol integrator before an internals handoff. No configuration, service, package, boot or sibling-file write is authorized.

     This explicitly supersedes only the OUT-009 proposition's unqualified “Revenger owns” wording and its broad “packages” paraphrase. The original quoted declaration and pinned bytes remain historical evidence; “Electron/JavaScript packages” is the precise package scope, not arbitrary packages. ADJ-06's unresolved recipient and Frontier arbitration remain controlling. The other nine locators and all prepared/acknowledged handoff states are unchanged. Source: the pinned Revenger snapshot in `corpus/knowledge/adjacency-anchors-r19.json`; recheck: `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`.
     ```

5. **Tool implementations in external worktrees:**
   - `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py:123-178`: `_ownership_correction` enforces that `PROVINCE.md` contains the unique heading `## R20 ownership clarification — OUT-009` and exact `OWNERSHIP_SECTION_LINES`, retains `OWNERSHIP_ARBITRATION_LINES`, preserves `| OUT-008 | ADJ-06 |` and `| OUT-009 | ADJ-06 |`, verifies the pinned snapshot hash and quote, and leaves the historical `adjacency-anchors-r19.json` registry record untouched.
   - `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py:284-350,657-658`: `systemctl_violations` inspects `--exec-log` lines; mutating verbs (`restart`, `daemon-reload`, `enable`, etc.) and unknown verbs trigger `EXEC-STEER-VIOLATION`, while read-only probes (`cat`, `show`, `status`, `list-units`, `list-timers`, `is-active`, etc.) pass.
   - `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:112-126`: `_object_commit` disambiguates hexadecimal object prefixes before commit-ish peeling, preventing hex-looking ref names from shadowing object selectors.

---

## 3. Cross-axis analysis and explicit contradictions

### Contradiction 1: Ownership attribution vs. Integrator arbitration
- *Contradiction:* In round 19, OUT-009 declared "Revenger owns shipped-artifact reverse engineering..." in Tsukuroi's voice, while `PROVINCE.md:79-80` explicitly stated: "Kaidoku and revenger both declare shipped-artifact RE. The integrator must arbitrate this shared scope; tsukuroi neither picks an owner nor absorbs it."
- *Resolution:* R20-OUT009 reframes OUT-009 from a Tsukuroi grant of ownership into an *attributed sibling declaration*. Tsukuroi records what Revenger claims without adjudicating between Kaidoku and Revenger, keeping arbitration strictly with the protocol integrator.

### Contradiction 2: Package scope ambiguity vs. Host package sovereignty
- *Contradiction:* Truncating Revenger's declaration to "packages" suggested Revenger had authority over packages generally, creating confusion with Tsukuroi's core province: host package state (`pacman -Qkk`, foreign/AUR census, `.pkg.tar.zst` discipline; `PROVINCE.md:8-9`).
- *Resolution:* Restricting the proposition to Revenger's exact wording — "Electron/JavaScript packages" — isolates application artifact reverse engineering from host OS package management.

### Contradiction 3: Finding handoff vs. Substrate remediation authority (The C1-C2 Cross-Axis Lock)
- *Contradiction:* In multi-agent systems, an adjacent finding handoff (ADJ-06) is readily misconstrued by downstream agents as permission to repair. For driver/firmware mechanisms, agents might attempt package reinstallations (`pacman -Syu`), unit restarts (`systemctl restart`), or boot file edits (`limine-update`).
- *Cross-axis relation:* C1's OUT-009 clarification explicitly terminates this inference chain by declaring:
  `No configuration, service, package, boot or sibling-file write is authorized.`
  This directly anchors C2's execution enforcement:
  - `service` writes are forbidden and caught by `check-recheck-commands.py` (`systemctl_violations` flagging `EXEC-STEER-VIOLATION`).
  - `package` and `boot` writes are forbidden and caught by `check-recheck-commands.py` (`DEFAULT_FORBID` including `pacman`, `yay`, `paru`, `mkinitcpio`, `limine-update`).
  - `sibling-file` writes are forbidden by leaf seat isolation and Revenger's own declaration ("Writes only this `revenger-shokunin/` repository... sibling repositories remain read-only").

---

## 4. Second-order effects across surfaces

1. **Runtime surface:**
   - `tools/_revision.py` object disambiguation (`_object_commit`) is imported by all revision-aware tools. When integrated, `check-adjacency-anchors.py` and `check-recheck-commands.py` inherit object-prefix resolution identically to the original nine tools.
   - `check-recheck-commands.py` parses shell text in `--exec-log` lines (`$ <command>`) without executing subprocesses or shell builtins.

2. **Contract surface:**
   - Tsukuroi disclaims RE authority and maintains strict separation between *health/state monitoring* and *internals reverse engineering*.
   - The five forbidden write classes in `PROVINCE.md:150` (`configuration`, `service`, `package`, `boot`, `sibling-file`) establish an invariant across all finding handoffs.

3. **Substrate surface:**
   - Host package state, systemd manager configuration, running services, and the `/boot` filesystem remain completely unmutated.
   - The host OS substrate is protected from unauthenticated package transactions or unit state changes.

4. **Verification surface:**
   - C1 is verified by checking exact structural presence of the clarification block in `PROVINCE.md` while confirming bit-level immutability of the historical capture snapshot and registry.
   - C2 is verified by testing `--exec-log` against mutating systemctl verbs and validating tool continuity across object-only hexadecimal selectors.
   - C3 is verified by ensuring the operative registry row does not emit live `DEGRADED`.

---

## 5. Proposed move: Source-grounded integration synthesis

**One Bounded Move:**
Integrate the external worktrees by binding the C1 ownership clarification directly to the C2 steer-safety boundary through the following atomic coordination:

1. **Commit `PROVINCE.md:148-152` alongside `tools/check-adjacency-anchors.py`:**
   Incorporate `_ownership_correction` from `/tmp/tsukuroi-r20-adjacency-20261021/tools/check-adjacency-anchors.py` into production `tools/check-adjacency-anchors.py`.
   *Critical requirement:* Do not edit `corpus/knowledge/adjacency-anchors-r19.json` in place. The gate requires that `registry_doc["outbound"]` OUT-009 matches `OWNERSHIP_PIN` exactly (retaining the historical proposition), while the supersede notice resides exclusively in `PROVINCE.md`.

2. **Incorporate C2's `_revision.py` and `check-recheck-commands.py`:**
   Integrate `tools/_revision.py` and `tools/check-revision-binding.py` from `/tmp/tsukuroi-r20-binder-20261021/`, and `tools/check-recheck-commands.py` from `/tmp/tsukuroi-r20-execscope-20261021/`.
   *Synthesis effect:* C1's explicit statement — "No configuration, service, package, boot or sibling-file write is authorized" — is operationalized by C2's `systemctl_violations` and `invocations(line[2:], forbid)` checks in `check-recheck-commands.py`.

3. **Align `SKILL.md` Round 20 table:**
   Ensure the operative round 20 table in `SKILL.md:2096-2118` advertises `--ownership-corrections` for `adjacency-anchors` (row 2116), `--object-selectors` for `revision-binding` (row 2114), `EXEC-STEER-VIOLATION` for `recheck-commands` (row 2112), and `audit-live-map` for `registry-coverage` (row 2118).

---

## 6. Risks and falsifiers

1. **In-place registry tampering risk:**
   If an integrator attempts to "fix" OUT-009 by editing `corpus/knowledge/adjacency-anchors-r19.json` directly, `check-adjacency-anchors.py` line 134 will fail with `OWNERSHIP-CORRECTION-INVALID` ("OUT-009 no longer matches its original pinned Revenger declaration"). The fix MUST remain append-only in `PROVINCE.md`.

2. **Heading uniqueness collision:**
   If `## R20 ownership clarification — OUT-009` appears more than once in `PROVINCE.md`, `check-adjacency-anchors.py` line 164 flags `OWNERSHIP-CORRECTION-INVALID` ("the R20 ownership clarification heading must be unique").

3. **Context removal risk:**
   If the original ADJ-06 table rows (`| OUT-008 | ADJ-06 |` or `| OUT-009 | ADJ-06 |`) or the arbitration lines (`OWNERSHIP_ARBITRATION_LINES`) are removed from `PROVINCE.md`, `check-adjacency-anchors.py` line 177 flags `OWNERSHIP-CORRECTION-INVALID`.

4. **Exec-log false negatives/positives:**
   In `check-recheck-commands.py`, `_systemctl_read_only` allows read verbs (`cat`, `show`, `status`, `list-units`, `list-timers`, `is-active`, `is-enabled`, `is-system-running`). Any unexpected flag or verb fails closed to `EXEC-STEER-VIOLATION`. Executors must avoid chaining unlisted utility flags on status calls.

---

## 7. Verification plan (for L1 integrator post-wave)

*Note: Per seat contract, NO verification commands were executed by this leaf seat. The commands below are specified exclusively for L1 evaluation after wave integration.*

1. **C1 Adjacency measurement:**
   `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`
   - *Expected output:* `ownership_corrections=1; exit=0`.
   - *Failure controls:* `OWNERSHIP-CORRECTION-MISSING` on baseline; `OWNERSHIP-CORRECTION-INVALID` on altered heading/text.

2. **C2 Operability measurement:**
   `python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors`
   - *Expected output:* `object_selector_tools=9; exit=0`.
   - *Exec-log steer safety:* `python3 tools/check-recheck-commands.py --revision <REV> --exec-log <lane path>` rejects `systemctl restart/daemon-reload/enable` with `EXEC-STEER-VIOLATION`.

3. **C3 Calibration measurement:**
   `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map`
   - *Expected output:* `audit_live_map_errors=0; exit=0`.

---

## 8. Limitations and scope

- Seat role: Leaf connector (`ConnCrossScope`). No subagent dispatch, no task delegation.
- Tool usage: `read`, `grep`, `glob`, `write` (sole write to `.ufo/waves/round-20/build/ConnCrossScope.md`).
- NO-EXEC: No shell/eval/subprocess, imports, gates, selftests, or host probes executed.
- No production files edited (`PROVINCE.md`, `SKILL.md`, `corpus/`, `tools/` untouched by this seat).
- Host/boot state remains UNKNOWN. No packages installed, upgraded, or removed; no services restarted.

Scope: executed=none
