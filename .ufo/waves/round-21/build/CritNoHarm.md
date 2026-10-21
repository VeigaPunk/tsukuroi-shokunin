# CritNoHarm — no host action, no axis trade (round 21 build, critic)

Reviewed-SHA256: a296da872e83731f7f7a7737662988558ebb97e4399681a1099fab4a259b7a79
Predicate: no-host-action-no-axis-trade
Lane bounds: leaf member — no subagent dispatch.

Reviewed bytes: `.ufo/waves/round-21/snapshot/PROVINCE.md`. The digest above is the one supplied at dispatch. I did not recompute it (NO-EXEC). To test the claims against that province, I also read, read-only: `preregister.json`, `reviews.json`, `build/{spec,spawn,reservation*,refusal-*,death-ScribeDecision}.json`, the `SCORECARD.md` Round 21 block, the snapshots of `check-revision-binding.py`, `_revision.py` and `lessons/round-20.md`, and the `--revision` paths of the nine consumers.

## Axes

The preregistered axes are C1 depth (`decision_rows` 0→5), C2 operability (`target_type_tools` 0→9) and C3 calibration (`pinned_reviews`). Every claim is also checked against two constraints: no host, package, service or boot action, and no ordinal or cross-axis trade.

## Verdict

- **Host, boot and ownership:** there is no invariant violation in the pinned province or in the C1–C3 declarations.
- **Ordinals:** they are honestly unchanged.
- **Cross-axis risks:** two real ones exist (N1 and N2), plus two duplicate-authority defects in the dispatch (N3 and N4). All four are fixable. None of them requires the canonical judge to reject the round, provided the corrections below land before measurement.

## Clean checks (counterexample sought, none found)

- **H1. Host authority.** The province refuses package install, upgrade and removal and service restarts: "Never installs, upgrades, or removes packages; never restarts services" (Refuses). It refuses rebuild and boot: "never rebuild or boot" (Initramfs row). R20-OUT009 adds "No configuration, service, package, boot or sibling-file write is authorized." No C1, C2 or C3 text grants or needs host action. SCORECARD R21 says "No capability, exploratory claim, host-recovery action".
- **H2. C2 accept cases run the nine real consumer CLIs.** I looked for the strongest counterexample: an accepted tag-to-commit lets `check-boot-chain.py` or `measure-update-recheck.py` go past binding into host probes. It does not happen.
  - `measure-update-recheck.py:13` says "--revision only reads git blobs". Its `pacman -Q`/`-Qu` strings (`:619-635`) are selftest probe stubs.
  - The `/boot/...` literals in `check-boot-chain.py` are comparisons against committed captures. Its only subprocess is `git` (`:805`).
  - In all nine consumers, `subprocess.run` invokes only `git` or `sys.executable` on lane tools.
  - Limit (judge docstring `:50-51`): the tools keep "the caller's user-level filesystem/network authority". The sandbox clone is not OS isolation.
- **H3. Ordinals.** `preregister.json` `ordinals` are depth8, adjacency8, coverage9, operability9, freshness9 and calibration9, with `ordinal_deltas: 0`. These equal the SCORECARD Round 20 baseline (`SCORECARD.md:616`). C1 works the tied-lowest axis, depth. No count is converted into an ordinal.
- **H4. Reservation chronology.** The five reservations precede their attempts. Attempts 1–4 recorded `spawned: 0` (job limit), with the policy "never split, shrink or replace". `reservation-05` (12:48:42Z) precedes `spawn.json` (12:48:50Z), and both have seats=64. `spec.json` and `reviews.json` both have 64 names. I am not making a claim from swarm size.

## Findings

### N1. C3's "after" predicate is incompatible with its own fail-closed gate (calibration, process)

**Counterexample:**
- `death-ScribeDecision.json` records `"status": "failed exit1"` (429) and `"replacement": false`.
- `reviews.json` still lists ScribeDecision.
- The ExecReview contract mandates exit1 `REVIEW-REPORT-MISSING` "never silently omit".

The measured C3 command must therefore exit 1. However, `preregister` C3 `after` is a non-numeric string ("every delivered build/falsify review…"), and the SCORECARD says "pinned_reviews0→every delivered round21 review". Only three ways to reach "pass" remain, and each breaks an invariant:
- dropping the dead row is silent omission;
- writing a substitute report is "manufacturing dead-seat reports" (SCORECARD R21);
- grading only the delivered subset makes the claim diverge from the preregistered command's exit.

**Further gap:** "falsify" reviews are not in the manifest. Adding them after falsify outputs exist would violate "review digests must precede reviewed outputs".

**Identity note:** the live roster I was given still lists `TsukuroiR21.ScribeDecision-5` as running. The death record may be premature, or it may be correct while the roster is stale. Either way the denominator is not fixed.

**Smallest safe correction:** before any C3 measurement, append a dated, named calibration note to the preregistration. It does not rewrite the frozen file. It states:
- `total_reviews=64` fixed;
- the expected `pinned_reviews` equals the delivered count;
- the expected exit is 1, with `REVIEW-REPORT-MISSING` exactly for the disclosed dead names;
- falsify reviews require a separate manifest committed before falsify dispatch.

This keeps the red disclosed and makes C3 falsifiable.

### N2. New C1/C3 gates enter the frozen round-20 C2 modes (operability versus depth/calibration)

`discover()` (`check-revision-binding.py:245-256`) probes every `tools/*.py` containing the literal `"--revision"`. The drafted `check-selector-contract.py` and `check-review-snapshots.py` both define it, and `--manifest` is optional, so they will run in the default and `--object-selectors` modes.

In default mode, `measure()` re-raises any `Cannot` raised while probing an extra (`:711-712`, `if not object_selectors or name in TOOLS: raise`). An `E-TOOL-TIMEOUT` (>60s) or `E-TOOL-RUN` from either new gate would turn the round-20 original-nine consistency run into exit 2. C1/C3 would then degrade C2's continuity metric, which the preregistration says to "preserve unchanged".

[INFERENCE] The likelihood is low, because the probes are git-only and fast. Nothing has measured it, though. Changing `:712` would itself alter the frozen mode, so the correction is to measure, not to edit.

**Correction:** at the integrated REV, L1 must run the default mode and `--object-selectors`. Both must still exit 0 with 9/9. The two new gates must appear in `additional_*` without a `probe_error`.

### N3. Executor lane bounds contradict the leaf/NO-EXEC contract (host-action, calibration)

`spawn.json` gives the three executors (6 occurrences, in task and assignment) "Lane bounds: leaf member — no subagent dispatch except your single labrat." The wave contract says "You are a leaf. Do not delegate… NO-EXEC", and `spec.json` contains no labrat clause. The dispatcher therefore injected a second, looser authority.

A labrat that executes would make an executor's `Scope: executed=none` false. C3 checks only the declared line ("not proof of… command nonexecution"), so it cannot catch this.

**Correction:** for ExecMatrix, ExecDecision and ExecReview, L1 records whether any labrat child exists (agent registry or history), and treats any such child as a scope finding. Remove the labrat clause from the round-21 falsify template.

### N4. The operator tooling directive appended to every seat conflicts with the pause (host-action)

Every spawned prompt carries "installs or updates any tool… with full privilege, without asking first… `sudo pacman -S --needed --noconfirm`". The contract says "All pacman transactions PAUSED host-wide… This seat's narrower NO-EXEC contract forbids installs".

No delivered round-21 build report records an install: every hit for install/sudo/pacman -S says "none installed". So there is no violation. This is a residual risk, and `Scope: executed=none` cannot detect an install. ConnBoundary's K1/K2 already establish that the update-safety gate is report-only.

**Correction:** L1's final ledger states, per seat, that the narrower seat contract governed and that no install records exist.

### N5. ConnBoundary's proposed R21-GATE-BOUNDARY paragraph would itself add duplicate authority (adjacency, not reviewed predicate)

The draft asserts "Wave registry, dispatch, slot or grant and reservation semantics, and result acceptance, are kumitate/operator-owned; report-file settlement is mori's". It cites live, unpinned sibling bytes. Written as a tsukuroi statement, this repeats the unqualified-award pattern that R20-OUT009 and ConnBoundary's own O5 reject.

No C1–C3 claim requires a PROVINCE change, and `preregister.json` lists none. Appending one widens round-21 scope.

**Correction:** make no PROVINCE edit this round. If L1 adopts the paragraph anyway, it must use attributed quotes with a pinned commit and blob SHA-256 per anchor, plus a finite correction fixture, and stay outside the C1–C3 accounting.

## Not a violation (tradeoff noted)

C2's 0→9 is driven by the judge gaining a mode. The nine consumers are not edited this round, and their binder already passed tree and tag cases in the supplementary R20 `_revision` selftests (57/57). That is honest coverage growth only if it is reported as matrix coverage, not as a change in consumer operability. Since the ordinal delta is 0, nothing is traded. CritBaseline owns the detail.

## Limits

- This is source review only. I did not compute the snapshot digest or verify bytes against Git.
- I did not read the transcripts of the agent registry or history, so N3's labrat existence is unknown.
- Consumer host-probe absence is source-derived for the `--revision` path, not observed at runtime.
- No tools were installed or updated, and none were needed.
- This is author-side critique: not non-author closure or outside promotion.

Scope: executed=none
