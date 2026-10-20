# FrontierLinks — round 13 correction, seat TsukuroiR13.FrontierLinks

Seat: connector (UFO-FSD connector; author-side proposal synthesis, not non-author verification).
Scope: Map round-13 C1 depth correction to the existing rollback-net surface; prevent false new coverage and false host repair claims.

## Evidence

1. **Frontier & Surface Contract:**
   - `corpus/README.md:20,59-67`: "Snapper/rollback net" is an existing core surface. Round 12 noted: "This deepens the existing rollback-net surface; it is not uncovered coverage or a resolved host repair... Exact historical failing syscall/path, runtime credentials and incident-time target state remain frontier."
   - `PROVINCE.md:24,88-91`: Round-12 refinement of root metadata and create-failure DAC/ACL, mount/namespace, and credential discrimination remains within the existing host/rollback-net surface. Tsukuroi owns detection only; no mode repair, service restart, or package transactions.
   - `SCORECARD.md:272-276`: Live host census remains `DEGRADED` (exit 1). No scope transfer or repair claimed.
2. **Verifier Disagreement & Defect Pointers:**
   - `corpus/lessons/round-12-verifier-spotcheck.md:14-19,140-161,210-218,237-243`: Verifier verdict `rejected-harmed`. C2 depth harmed by false exclusive statement in `root-dac-decision-r12.md:53,86` and `root-dac-decision-r12.json:85` asserting that only `ProtectSystem=strict` or `ReadOnlyPaths=` can make `/` read-only through a unit. Coverage was graded `unchanged` ("Existing rollback-net surface refined; no evidence of lost coverage or a new ownership surface").
3. **Source Grounding:**
   - `systemd.exec(5)` (S028, and incoming S041): `ProtectSystem=full` protects `/usr/`, `/boot/`, `/efi/`, `/etc/`; `strict` covers the hierarchy (except `/dev`, `/proc`, `/sys`). `BindReadOnlyPaths=`, `TemporaryFileSystem=ro`, `RootDirectory=`, `RootImage=` provide alternative read-only bind mounts or altered root path views.
   - `mkdir(2)` (S035) & `tmpfiles.d(5)` / `root.conf` (S039/S040): Mode 0555 on `/` is packaged policy line `z / 555 - - -`, not proof of historical Btrfs subvolume causality (QUALITY #15, #16).

## Affected Axes

- **depth:** Improved / restored. Replaces the false universal with an exact `ProtectSystem` comparison plus an open set of alternative unit mount mechanisms, while retaining unobserved runtime namespace state as an explicit unknown. Score remains 8 (honest, no ungrounded ordinal jump).
- **coverage:** Unchanged (held at 9). Bounded strictly to the existing "Snapper/rollback net" surface. Refusing to claim a new "systemd sandbox" or "namespace inspection" surface prevents false coverage inflation.
- **operability:** Unchanged (held at 9). The new `tools/check-root-dac-correction.py` is a narrow conformance gate, not an operational census plane. Six-plane census contract is preserved.
- **calibration:** Unchanged (held at 9). Fully acknowledges the R12 verifier rejection, records runtime namespace state as `[unknown]`, and avoids converting static configuration into historical cause.
- **freshness:** Unchanged (held at 9). Anchors fresh S041 `systemd.exec(5)` read without claiming an unverified corpus-wide refresh.
- **adjacency:** Unchanged (held at 8). Sibling provinces (`mori`, `mado`, `kama`, `kumitate`) remain untouched; no scope absorption.

## Proposed Move (One Bounded Synthesis)

Synthesize the round-13 correction as an **open diagnostic indicator refinement with an explicit runtime-namespace unknown**, anchored strictly within the existing `Snapper/rollback net` surface:
1. **Restrict Exclusivity to ProtectSystem:** In `root-dac-correction-r13.md` and `.json`, narrow the comparison strictly to `ProtectSystem=` settings (`full` vs `strict`). Enumerate `BindReadOnlyPaths=`, `TemporaryFileSystem=ro`, `RootDirectory=`, and `RootImage=` as non-exhaustive examples of alternative unit path views.
2. **Explicit Runtime Unknown Boundary:** Explicitly state that inactive unit configuration (`ProtectSystem=no`, empty `ReadOnlyPaths=`) does *not* prove that the failing process had a global `rw` root view during execution; unit-private mount namespaces and runtime isolation remain unobserved `[unknown]`.
3. **No New Coverage Surface:** Document this entry as an erratum/refinement of the existing rollback-net surface in `corpus/README.md` and `PROVINCE.md`. Do not add new coverage rows or declare a new sandboxing plane.
4. **No Repaired Host Claim:** Reaffirm that `/` mode 0555 is a package-shipped policy observation (S040), not a repaired state; host census remains `DEGRADED` (exit 1), and historical `errno:13` incidents remain unproven.

## Risks & Second-Order Effects

1. **Second Universal Trap:** Listing specific alternative directives (`BindReadOnlyPaths`, `TemporaryFileSystem`, etc.) could be mistaken as a new closed set.
   *Mitigation:* Explicitly label the alternatives as non-exhaustive and declare failure-time namespace isolation as fundamentally unobserved.
2. **False Coverage Creep:** Reviewers might treat namespace analysis as a new capability or coverage plane.
   *Mitigation:* Keep ownership in PROVINCE under "Snapper/rollback net" create-failure diagnostics; do not alter the 6-plane census rollup.
3. **Causal Conflation:** Conflating current unit properties with historical execution.
   *Mitigation:* Strict observation/inference separation under QUALITY #2, #3, #15. Current inactive unit properties are configuration evidence, not historical trace evidence.
4. **Historical Mutation:** Modifying round-12 files directly would destroy historical audit trail.
   *Mitigation:* Keep round-12 files intact; publish r13 files as new standalone additions and append dated supersession notices.

## Verification

1. `tools/check-root-dac-correction.py`: Fails baseline r12 files (detecting false universal in R13, current-host prose, and JSON B2 limit) and passes r13 correction files.
2. `sources-census.sh validate`: Validates S041 addition and superseding bot rows without schema failure.
3. Surface Invariant: `git diff PROVINCE.md corpus/README.md` shows 0 new surfaces or planes added.
4. Host Invariant: `bash tools/tsukuroi-census.sh` maintains six planes and exits 1 (DEGRADED), confirming no false host-repair claim.

Tools installed/updated: none.
