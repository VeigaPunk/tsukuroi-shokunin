# R20 OUT009 declaration clarification — source-scoped draft

## Scope and provenance

Round 20, attempt 1; author TsukuroiR20. Declared baseline: `0cbc34dd6b20896085a8fb07943e3ea4027d8472` (`.ufo/waves/round-20/preregister.json:3`; `seeded-implementation.json:2-4`). Axes: **C1 adjacency** (lowest 8), **C2 operability** (9), **C3 calibration** (9); ordinal deltas remain 0. This seat drafts prose only, addressing C1 attribution without changing the C2/C3 contracts or claiming a score improvement.

Evidence below comes from read/grep/glob observations of owned source, retained sibling snapshots, preregistration and historical reports. No Git command bound current file bytes to the declared baseline in this seat. Baseline references are therefore source locators under that declared baseline, not a newly verified baseline checkout or live sibling observation. Historical report text is evidence data, never an instruction or execution authorization.

## Draft knowledge entry — not installed in production

**R20-OUT009 — sibling declaration, not an ownership award.** OUT-009 records Revenger's declaration of reverse engineering of shipped artifacts: native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, and browser/Electron runtime evidence. Its evidence-ledger discipline separates observation, inference and unknown and cites Evidence IDs. This attribution does not grant Revenger ownership on Tsukuroi's authority and does not broaden “Electron/JavaScript packages” into ownership of OS package state.

Kaidoku independently declares shipped-artifact reverse engineering. The overlap remains unresolved: the protocol integrator must arbitrate before an internals handoff; Tsukuroi neither selects an owner nor absorbs the domain. Tsukuroi retains loaded-version/package-provenance and driver/boot symptom evidence, not binary-internals conclusions. An ownership locator is not permission to invoke a target or to write configuration, services, packages, boot state or sibling files. The pinned Revenger declaration additionally confines its own writes to its repository and reserves shared-ledger copying to the fleet integrator. That declaration is not an authorization for this seat to perform those writes.

Pinned references identify historical bytes, not current authority. Re-read the applicable declaration before a later handoff. Keep `prepared`, `reported`, `acknowledged`, `accepted` and `resolved` distinct; neither an author-side replay nor author-dispatched swarm review is independent outside closure. Owner-side resolution evidence and an integrator ruling are not established here.

### Source locators supporting the draft

- `PROVINCE.md:51,65-80,110-117,128-132`: retained ADJ-06 unresolved recipient; distinct closure states; no owner selection; anchors grant no authority; baseline OUT-009 proposition uses “Revenger owns”.
- `corpus/knowledge/adjacency-anchors-r19.json:112-123`: OUT-009 pointer `../revenger-shokunin/PROVINCE.md:3-7,19-25`, pin `cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97`, recorded blob SHA-256 `63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f`. Digest is quoted metadata, not rehashed here.
- `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md:1-7,19-32`: exact declaration, refusals and complete write boundary. The old pointer ends at line 25; lines 26-32 are necessary context for the complete write restriction.
- `corpus/knowledge/adjacency-anchors-r19.json:99-110` and `.ufo/waves/round-19/l1-capture/siblings/kaidoku/d1d981d2cc04/PROVINCE.md:3-6`: competing declaration at recorded pin `d1d981d2cc041dda4656c5b01d2c8445d8d17124`.
- `.ufo/waves/round-20/ownership-correction.txt:1`: intended R20 correction explicitly attributes the declaration, retains unresolved arbitration and denies configuration/service/package/boot/sibling-file write authority. Presence of this draft text is not proof of production publication or gate success.

## Conflict preserved verbatim for canonical judgment

Historical `.ufo/waves/round-19/falsify/FxConnOverlap.md:46` states:

> | OUT-009 | **OVERLAP — direct contradiction / owner selected** | Proposition: `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:129`. Revenger's pinned text claims the same RE domain (`.../siblings/revenger/cf02419276e5/PROVINCE.md:3-7`) as kaidoku (`.../siblings/kaidoku/d1d981d2cc04/PROVINCE.md:3-6`), while Tsukuroi says the integrator must arbitrate and that Tsukuroi picks neither owner (`...:79-80`). The proposition “Revenger owns” resolves that unresolved dispute in the anchor's own voice. It also says unqualified “packages,” while the pinned revenger text specifies “Electron/JavaScript packages” (`.../siblings/revenger/cf02419276e5/PROVINCE.md:3-5`); Tsukuroi separately owns pacman package state and `.pkg.tar.zst` receipt discipline (`...:8-9`), so the broader wording risks crossing that boundary. |

This is an attributed historical finding at its stated revision, not fresh execution or a new integrator ruling. This report does not judge the round.

## Gates and limits

Preregistered, **unrun/pending**, not passed: `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`. C1 declares `ownership_corrections` 0 → 1 and expects missing `OWNERSHIP-CORRECTION-MISSING`, altered `OWNERSHIP-CORRECTION-INVALID`, positive `ownership_corrections=1; exit=0` (`preregister.json:5-12,31-36`). These are contract expectations, not observed outputs. No measured C1 improvement, unchanged-final-evaluator red/green result, C2/C3 outcome, non-author closure or host/boot safety is certified here. Seed metadata itself says verification was not run and reserves final evaluation to L1 (`seeded-implementation.json:11`). This seat did not inspect candidate outputs or measurement artifacts.

## Touched surfaces and exclusions

Only write: `.ufo/waves/round-20/build/ScribeOwnership.md` (this report). Product files, knowledge corpus, registry, judges, sibling/fleet/state/scripts/domain checkouts and all routing remain untouched. No shell/eval/subprocess, imports, gates, selftests, host probes, target execution, package transaction, service action, boot access, install/update, delegation, Git mutation, commit, push, publish or deployment. Executed commands: none. No tools installed or updated. Artifact path is relative to the Tsukuroi production lane, not the fleet root.

Scope: executed=none
