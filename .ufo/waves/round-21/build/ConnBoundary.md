# ConnBoundary — cross-lane selector-tooling boundary (round 21 build, connector)

Reviewed-SHA256: a296da872e83731f7f7a7737662988558ebb97e4399681a1099fab4a259b7a79
Predicate: cross-lane-selector-tooling-boundary
Lane bounds: leaf member — no subagent dispatch.

Reviewed bytes: `.ufo/waves/round-21/snapshot/PROVINCE.md` (pinned copy of baseline `PROVINCE.md`). The digest above is the one given at dispatch. I did not recompute it because this seat is NO-EXEC. Line numbers below refer to that snapshot.

## Axes

- **C1 depth:** five decision rows grounded in source.
- **C2 operability:** a new consumer target-type matrix, run only when explicitly selected.
- **C3 calibration:** preregistered receipts that bind each review to its bytes and predicate.
- **Boundary constraint (checked on every axis):** no claim takes over sibling ownership or host authority.

## Verdict

The pinned PROVINCE.md contains **no claim that absorbs ownership or host authority** for revision or selector gates. It is also **silent** about the round-21 gate family. A reader therefore has no locator saying that these gates are lane-local. The gap is one of omission, not an overclaim.

## Observations (pinned snapshot)

- **O1. Host authority is refused.** Lines 25-28: "Never installs, upgrades, or removes packages; never restarts services. Detection and report; the operator remediates." Line 20 says upgrade actions "remain operator-owned". Lines 13-14 limit update-safety to questions ("what an -Syu would touch, what pins/holds exist").
- **O2. Sibling methods are not absorbed.** Line 90 says the work proceeds "without absorbing sibling verification methods". Lines 95-96 grant "no namespace mutation, privileged inspection or sibling-method ownership". Line 117 says the section "grants no authority and is an ownership locator, not a repair mandate".
- **O3. The only revision-gate references are lane-local recheck commands.** These are `python3 tools/check-adjacency-anchors.py --revision <REV>` (line 132) and the same command with `--ownership-corrections` (line 152). The file never names `tools/_revision.py`, `check-revision-binding.py`, `check-seat-scope.py`, or the round-21 drafts (`check-selector-contract.py`, `check-review-snapshots.py`).
- **O4. The ADJ-07 trigger is narrower than the round-21 question.** Line 52 says "A census blind spot raises a reusable verification/mutation-testing question". Tsukuroi retains "Census bug, domain contract, implementation and repair in this repo", and tameshi receives "method advice, not transfer of gate ownership". The round-21 blind spot is in the revision binder, not the census (lessons R20-BIND-TARGET-TYPE and R20-HEX-REF). Under checklist item 2 (lines 59-61), "If no row fits, report to the integrator", it falls to the integrator rather than to ADJ-07 as written.
- **O5. OUT-010's proposition is phrased as an unqualified award.** Line 130: "Tameshi owns the reusable verification/mutation-testing method…". This is the same pattern that R20-OUT009 (lines 150-152) superseded for Revenger. QUALITY35 (snapshot) says a quoted "Owns" declaration "is not an integrator ownership award". The quoted words do appear in tameshi's own declaration (live `tameshi-shokunin/PROVINCE.md:7`: "**Owns:** the method, documented from the fleet's existing gates"). The issue is only that the proposition column turns an attribution into an assertion.
- **O6. The dispatch route is supported jointly, and reservation is not anchored.** OUT-006 (line 126) infers dispatch/routing semantics from kumitate's domain line "scopes OMP task/hub, ufo-fsd scripts & runtime". That quote does not itself say "dispatch"; OUT-007 (line 127, Mori's refusal "dispatch and orchestration mechanism (→ kumitate)") is what supports the recipient. No pinned anchor mentions reservation, slot or grant semantics.

## Observations (live sibling files, read-only, unpinned)

- **Tameshi.** `tameshi-shokunin/PROVINCE.md:14-17`: "every lane's gate remains its own; tameshi owns only the reusable craft (a pattern is admitted from evidence in TWO independent lanes before it is claimed general). Never edits a sibling's gate code". Its round-21 append (`:85-95`) says "sibling gate ownership is unchanged".
- **Mori.** `mori-shokunin/PROVINCE.md:135-138`: "Planning, slot acquisition, retrying and adjudicating dispatch remain **kumitate/operator**-owned; `wave-slot.sh` grant lines are recorded as evidence only". At `:145-154`, report-file settlement ("`settled` means report-file settlement only, not kumitate's lifecycle settlement or result acceptance").
- **Kumitate.** `kumitate-shokunin/PROVINCE.md:3`: "orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime". `kumitate-shokunin/SKILL.md:43` names the schema `swarm-registry.json` (`ufo-swarm-registry-v1`). The pinned `tools/check-seat-scope.py:40,104-143,300` reads exactly that schema from tsukuroi's own wave directory.
- **Round-21 reservation artifact.** `build/reservation.json` contains `"grant": "granted lane=tsukuroi wave=round-21-build seats=64 live=81 pending=64 cap=240"`. That fleet-issued grant line is evidence, not a tsukuroi contract.

## Inferences

- **I1.** The round-21 gates are tsukuroi lane-local infrastructure. They read tsukuroi Git objects and tsukuroi wave files, and they measure only tsukuroi source contracts. They imply no host state, Git-wide semantics, or fleet method. The C1 draft prompt already says it "measures source contract not actual Git execution, host health or universal semantic correctness".
- **I2.** [INFERENCE] The owner of reservation, grant and cap semantics is kumitate/operator. This rests on mori's live `:135-138` and kumitate's runtime scope, not on a pinned tsukuroi anchor.
- **I3.** The C3 receipt lines (`Reviewed-SHA256`/`Predicate`/`Scope`) and the C2 independent-judge and mutant fixtures are instances of verification method. Calling them general would require tameshi's two-lane admission. Tsukuroi may own the gate code and its contract, but not the pattern.

## Contradictions (stated, not smoothed)

- **K1. Operator directive versus Core.** The operator directive says "Full-system upgrades (`pacman -Syu`) go through tsukuroi-shokunin's update-safety gate first". PROVINCE lines 13-14, 20 and 25-28 make that gate a pre-upgrade **report** that cannot approve or run anything. Read carelessly, the directive could seem to make tsukuroi a host-upgrade authority. It does not.
- **K2. Agent tool installs versus "Never installs".** The directive authorizes agents to install tools. Line 27's "Never installs" refuses package installs as a remediation in tsukuroi's domain. These are different scopes. Neither applies this round, because pacman is paused host-wide and this seat is NO-EXEC.
- **K3. QUALITY28 wording.** QUALITY28 (snapshot) says "every lane gate imports `tools/_revision.py`". Inside tsukuroi this means tsukuroi's gates, but read on its own it could be taken as fleet-wide. This is adjacent bytes, not the reviewed predicate.

## Proposed move (one, bounded; for L1 to integrate, not applied)

Append one named paragraph to PROVINCE.md, for example R21-GATE-BOUNDARY, after the R20 section. It would leave lines 1-152 unchanged, and it is a synthesis of O3, O4 and I1-I3:

> R21-GATE-BOUNDARY: `tools/_revision.py` and its revision, selector, review-snapshot and seat-scope gates are tsukuroi lane-local instruments over this repository's Git objects and its own `.ufo/waves/` files. They measure tsukuroi source contracts only: not host, package, service or boot state, and not Git-wide semantics. They grant no configuration, package, service or sibling write. Generalizing their independent-judge, mutant-fixture or pinned-receipt method is a tameshi method question routed through ADJ-07. That route also covers lane-gate blind spots beyond the census, and asks for advice only, under tameshi's two-lane admission. Wave registry, dispatch, slot or grant and reservation semantics, and result acceptance, are kumitate/operator-owned; report-file settlement is mori's. Tsukuroi reads those artifacts as declared evidence only. OUT-010 is read as tameshi's attributed declaration, not a tsukuroi award (QUALITY35).

What this move changes on each axis:

- **C2 operability improves.** Revision-gate blind spots get an explicit route, so they no longer fall through the fact that ADJ-07 only names the census.
- **C3 calibration improves.** The receipts are scoped as a lane contract, not a fleet method.
- **C1 depth is unchanged.** The five decision rows and their sources are untouched.
- **No new capability, surface or authority.**

## Risks

- Widening the ADJ-07 trigger by an appended clarification could be misread as moving ownership of a tsukuroi gate to tameshi. The text keeps "advice only" and says each lane keeps its own gate, which mitigates this.
- The kumitate and mori citations are to live, unpinned sibling bytes, which can drift (lines 70-73). Before integration, L1 should pin the commit and blob SHA-256 per R19-ADJ-POINTERS, or cite them as attributed declarations only.
- OUT-010 wording: any correction must be appended as a named supersession, as R20-OUT009 was. Rewriting line 130 in place would break the pinned historical bytes and the anchor checker.

## Verification L1 should run after integration (not run here)

- `python3 tools/check-adjacency-anchors.py --revision <REV>` and the same command with `--ownership-corrections`. These confirm that OUT-001..OUT-010 and R20-OUT009 still resolve and that the appended paragraph does not disturb the anchors.
- If the OUT-010 attribution is adopted, add a finite correction fixture modelled on R20-OUT009. It must fail missing, altered and ownership-award rewrites.
- A read-only grep of the integrated PROVINCE.md, SKILL.md and QUALITY.md. Ownership verbs ("owns", "authorizes", "approves") next to tameshi, kumitate, mori, reservation, grant or dispatch must be either attributed or refused.
- `tools/check-seat-scope.py --revision <REV> --wave .ufo/waves/round-21/build` to confirm that this report's trailer is well-formed.

## Limits

- I reviewed the pinned PROVINCE.md snapshot and read adjacent snapshot files plus live sibling PROVINCE and SKILL files, all read-only. I did not hash the sibling bytes.
- I did not confirm that the dispatch digest equals the snapshot bytes.
- No execution, no installs, no edits to production or sibling files.
- Tooling: none installed or updated; none needed.
- This is author-side connector advice, not non-author closure or outside promotion.

Scope: executed=none
