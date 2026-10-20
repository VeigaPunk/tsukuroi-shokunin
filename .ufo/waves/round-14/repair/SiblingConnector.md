# SiblingConnector — Bounded Province Alignment & Substrate Containment

Seat: `TsukuroiR14.SiblingConnector` (leaf connector). Author-side synthesis; no closure authority.
Baseline: `8606bad4cbc6451ac2890c9f8e2548a36c386db6` (round-13 verifier spot-check, rejected-harmed).
Target: Audit mori/mado/tameshi province boundaries to keep r14 repair strictly host diagnosis.

## 1. Evidence: Bounded Sibling Province Overlap Audit
- **Tameshi (`../tameshi-shokunin/PROVINCE.md:3-18,44-48`):** Owns reusable verification/mutation craft; refuses product domains ("every lane's gate remains its own... a pattern is admitted from evidence in TWO independent lanes before it is claimed general"). R13 created an unconsumed 42-line `gate_contract` in JSON (`root-dac-correction-r13.json:204-245`), creating a competing spec against the 375-line narrow checker. R14 proposals (`PredicateReview.md`) risk repeating this by designing an over-generalized multi-file AST verification spec.
- **Mori (`../mori-shokunin/PROVINCE.md:6-16,50-54`):** Owns fleet wave liveness, journal OOM/kill correlation, resource runway; refuses OS host state (systemd units, packages, boot state → tsukuroi). S045 discusses #8047 comment 6071740243 asserting an "Omarchy worker VM" non-reproduction and snapshot overlay remount failures (#6634). R13 misattributed this as collective "automated triage"; analyzing remote VM execution or fleet wave impact trespasses into Mori.
- **Mado (`../mado-shokunin/PROVINCE.md:3-16`):** Owns compositor (`hypr`), waybar, walker, and terminal configs. S044 ProtectSystem= sandboxing applies strictly to systemd unit execution environments (`systemd.exec(5)`), distinct from desktop UI configuration.
- **Tsukuroi Core (`PROVINCE.md:8-16,48-52`):** Owns host OS operability & diagnostic mending. ADJ-03 (mado), ADJ-04 (mori), and ADJ-07 (tameshi) define exact handoff boundaries; tsukuroi retains only the OS finding.

## 2. Affected Axes
- **depth (worked, held at 8):** Improved. Reconciles gate contract with narrow code; prevents semantic overclaim.
- **calibration (held at 9):** Improved. Eliminates false spec duality and unverified remote fleet claims.
- **adjacency (held at 8):** Improved. Enforces strict non-absorption of tameshi methodology and mori fleet correlation.
- **coverage (9), operability (9), freshness (9):** Unchanged. Zero new surfaces, zero sibling writes.

## 3. Proposed Move: Substrate Diagnostic Containment (Single Bounded Synthesis)
Synthesize the round's proposals under strict province containment:
1. **Eliminate JSON Gate Contract (Tameshi Boundary):** Do not emit an unconsumed `gate_contract` or multi-file AST schema in `source-scope-correction-r14.json`. Declare `tools/check-source-scope-correction.py` as a single-purpose, lane-local structural regression checker whose CLI/docstring is the sole authoritative specification, respecting Tameshi's exclusive ownership of reusable verification methodology.
2. **Isolate External VM Telemetry as Unverified (Mori Boundary):** In S045 and R14-COMMENT-ATTRIBUTION, classify comment 6071740243's worker VM assertion as an unverified external report; reject it purely as host cause without evaluating remote execution or fleet wave liveness, which belongs to Mori.
3. **Demarcate Unit Sandboxing from Desktop Plane (Mado Boundary):** In S044 and R14-VALUE-DOMAIN, explicitly bound `ProtectSystem=` to systemd daemon process execution contexts (`systemd.exec(5)`), preventing any creep into mado compositor/user-session configuration.
4. **Additive Errata Resolution:** In `root-dac-correction-r13.json`, append additive `r14_supersession` marking `gate_contract` as legacy unconsumed draft and S041 `reserved`/`SourceRegistry` as stale draft metadata.

## 4. Risks & Contradictions
- *Risk: False Equivalence of Gate Pass with Source Truth.* A passing structural checker does not verify documentation semantics. *Mitigation:* Explicitly state in the checker header and report that the tool measures bounded correction conformance, not source truth.
- *Contradiction: Unscoped Maintainer Deferral.* #8047 ends with "This now waits on your answer" (reporter wait); only #6634 awaits maintainers. *Mitigation:* Explicitly distinguish the two referents in S045 teaches.

## 5. Verification (Non-Author Execution by L1 / Integrator)
1. `tools/check-source-scope-correction.py`: Bounded to local files; passes clean r14 pair; fails baseline r13.
2. `scripts/sources-census.sh validate tsukuroi`: Exits 0; zero cross-lane URL collisions outside disclosed W04s.
3. Sibling Invariant: `git status --porcelain` shows 0 modifications in `../mori-shokunin`, `../mado-shokunin`, or `../tameshi-shokunin`.

## 6. Limitations & Tooling Record
- **Limitations:** Leaf connector seat; analysis based on local repository evidence and round cache; no live verification commands executed.
- **Tooling record:** Tools installed or updated: none. Read-only filesystem operations only.
