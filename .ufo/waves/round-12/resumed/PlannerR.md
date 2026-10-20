# PlannerR — C1/C2 data-walk and score guard

Scope: read-only reconstruction of the current census seam, inherited C1/C2 evidence, root metadata contract, and score evidence. This is not an implementation review or a gate run. No source was edited; this file is the only write. No shell/host probe, build, selftest, lint, or formatter was run. No install/update. No LSP route is exposed in the mounted tool inventory; I used `grep` only to locate passages and direct `read` results for source semantics. No command exit code applies to these reads.

## Reconstructed contract and invariant

- `PROVINCE.md:8-14,23-28` owns read-only host/pacman and Snapper/rollback diagnosis; repair remains operator-owned. `corpus/QUALITY.md:13-20` requires bounded negative evidence, exact source anchors, explicit unknowns, and root metadata findings that report owner-write/search bits rather than asserting process writability or a mount policy.
- Baseline package probe (`tools/tsukuroi-census.sh:529-685`) verifies a sample of package-owned paths with `pacman -Qkk`, classifies package drift/foreign-baseline/pins, and emits only those package facts in `PKG_NOTE`. Its early-return paths at `:534-557,563-571` also mean a new root observation must not accidentally be skipped on package-probe failures. The opened function has no `/` mode/uid/gid observation. The historical `corpus/knowledge/snapper-eacces-mechanism.md:13` reports `pacman -Qo /` as unowned and an installed filesystem mtree sweep as zero root-directory entries, explaining why `-Qkk` does not provide this baseline.
- The invariant to preserve is the existing six-plane output and six-key worst-verdict rollup: `tools/tsukuroi-census.sh:2377-2399` prints six `PLANE` lines, folds six keys, and maps HEALTHY/DEGRADED/BLOCKED to exits 0/1/2. C1 belongs as an observation in the existing packages (or update-safety) line; no seventh plane or rollup change is needed.

## C1 — baseline divergence and generalized discriminator

**Observed baseline:** the current source body has no root metadata probe; the matching prior host note records `/` as mode `555`, owner `root:root`, with no owner write and search present (`corpus/knowledge/snapper-eacces-mechanism.md:9`). That dated note is evidence of the observed case, not a fresh host measurement by this seat. Thus the unowned-root seam is present in the source, while the live `0 -> 1` finding remains unverified here.

**Required shape for generalization:** append numeric root mode/uid/gid plus an explicit owner-write/search-bit interpretation to an existing plane note. Treat the owner-write bit as the predicate, not the literal `0555`: `0755` has owner-write and should not create this finding; `0555` and another mode with owner-write clear should. Report raw inode metadata, not “read-only mount” or “process cannot write.” An unreadable metadata result must be `BLOCKED` or a visible `unknown`, never silently HEALTHY. Keep root metadata independent of `pacman -Qkk`'s sampled package ownership.

**Fixture discrimination required by the contract:** isolate `/` metadata behind a host-path/metadata-probe seam so the selftest never reads the real root; use fixed baseline fixtures and assert package-plane evidence, aggregate verdict, and exit for (a) `0755`, (b) `0555`, and (c) unreadable metadata. Include a second owner-write-absent mode (for example `0455`) or an equivalent bit-predicate assertion to reject a literal-`0555` special case. The existing hermetic harness already supplies path/command overrides and `check()` assertions for exit, verdict, evidence, and fixture immutability (`tools/tsukuroi-census.sh:286-308,326-350,1570-1809`). This is a test design requirement, not a test result; none was run here.

## C2 — current matrix and one-case-to-general rule

The inherited baseline note held one host-shaped `[inf]` candidate and listed untested causes (`corpus/knowledge/snapper-eacces-mechanism.md:9-14,19-30`). Current source state now includes `corpus/knowledge/root-dac-decision-r12.md` and its canonical JSON, so the historical Planner statement that the matrix was absent (`.ufo/waves/round-12/Planner.md:19-30`) is superseded as a *current-state* description. The new note/JSON explicitly state that C2 reads no census script, census output, census fixture, or C1 root field (`root-dac-decision-r12.md:9-17`; `.json:5-6`).

The structured matrix has four records, each with cited source evidence, a read-only discriminator, and a limit (`root-dac-decision-r12.json:8-127`):

| Record | Discriminator / class | Evidence boundary |
|---|---|---|
| B1 | Parent DAC write or path-prefix search denial; EACCES. `stat`/`getfacl` target the parent and prefix directories. | S035 EACCES semantics and S027/S034; mode/ACL must be interpreted for the caller. |
| B2 | Read-only mount or unit read-only namespace; EROFS, a control distinct from EACCES. | `findmnt` plus effective unit `ProtectSystem`/`ReadOnlyPaths`/`ReadWritePaths`; host `findmnt` is not the unit namespace. |
| B3 | Root's missing `CAP_DAC_OVERRIDE` under the unit capability bound; a conjunct explaining why B1 is not bypassed, **not an independent EACCES cause**. | `systemctl show` capability properties plus S027/S028/S034; configured properties on an inactive unit are not live process capability measurements. |
| B4 | Existing target; EEXIST-family control. | `stat`/`findmnt`/Snapper configuration, with a dated target observation; the note limits ordinary `mkdir` behavior and does not establish Btrfs ioctl ordering. |

The decision order and residual `UNCLASSIFIED` outcome are in `.json:129-135`. The worked host is one dated case: mode `555`, rw Btrfs mount, unit bounded to `cap_sys_admin`, absent `/.snapshots`, and journal `errno:13` matches; the note explicitly leaves historical syscall/path and Btrfs ioctl ordering unproven (`root-dac-decision-r12.md:35-56,58-70`; `.json:223-236`). This is the right shape for not turning one 0555 observation into a universal cause. Generalization examples include the 0755 success, 0555 DAC denial, EEXIST despite a 0555 parent, capability-bypass semantics, EROFS control, bounded-root conjunction, and residual EACCES left unclassified (`.json:137-253`). Several scenarios are source-grounded expectations, not observed executions.

The recorded isolated ordinary-`mkdir` outputs are author-side evidence, not independent verification: `discriminator-smoke.json:2-21` records uid 1000, 0555 -> EACCES, 0755 -> child created, and existing target -> EEXIST; `error-order-smoke.json:1-17` records 0555/new -> EACCES and 0555/existing -> EEXIST. Both artifacts explicitly limit extrapolation to ordinary mkdir, not the Btrfs subvolume ioctl. No smoke or privileged probe was run by this seat.

## Divergences, risks, and corrections to inherited evidence

1. **C1 still absent from the live source.** The current `probe_packages()` and `PKG_NOTE` end at package checks; no root stat/uid/gid path is present. No C1 fixture result or current census output was observed. The next integration must show the requested 0755/0555/unreadable distinctions and preserve the six-plane rollup.
2. **Metadata failure versus absence.** An unreadable root metadata probe is not evidence of a permissive mode or of a read-only mount. Preserve an explicit unknown/BLOCKED result. For the C2 target-presence discriminator, only a proven absent result (e.g. explicit ENOENT) excludes B4; a failed/unreadable `stat` must remain unknown, not be collapsed to “absent.” The generic procedure at `.json:130` does not spell out that failure subcase.
3. **S035 registry state conflicts with the matrix source claim.** `root-dac-decision-r12.md:1,80-89` relies on S035 as opened/assigned and cites its exact errno anchors, but current `corpus/SOURCES.md:41` still lists S035 status `queued`. The exact primary citation is present, but the registry needs reconciliation before treating S035 as mined/admitted under `QUALITY.md:10-13`.
4. **Four records are not four independent EACCES causes.** The record count is four, but the matrix itself defines B3 as B1's capability conjunct; B2 and B4 discriminate EROFS/EEXIST control classes. Do not report them as four distinct causes of the historical EACCES. If acceptance means four distinct EACCES mechanisms, this matrix does not establish that stronger interpretation.
5. **API boundary.** S035 grounds `mkdir(2)` errno behavior, not the exact Btrfs subvolume ioctl used by the snapshot tool. The matrix correctly retains this uncertainty; do not promote the ordinary-mkdir fixtures or SC7 correlation into syscall proof.
6. **Source admission state.** S027/S028/S034 are listed `mined` (`corpus/SOURCES.md:33-40`); S035 is the exception above. C2's explicit no-census dependency is reusable and should remain intact.
7. **Inherited Planner/ScoreReview are historical records.** Reuse the old Planner's C1 seam, six-plane preservation, and no-count-based-score cautions (`.ufo/waves/round-12/Planner.md:11-18,32-36`), but correct its C2 “matrix absent” baseline using the present matrix files. The old ScoreReview's “no claim has landed” is also only its recorded review state (`.ufo/waves/round-12/ScoreReview.md:4-9`); it is not a current C1/C2 verification. Its count-based cautions remain relevant, not its historical after-state.

## Score evidence (no arbitrary conversion)

`SCORECARD.md:47,49` records depth **8** and operability **9**; `:175-178` declares saturation at **9** and records depth/adjacency at 8 for the lowest-axis obligation. The older axes table has stale adjacency/coverage/freshness values that later post-review claims supersede (`SCORECARD.md:45-52,207-240`), so do not copy the stale adjacency 7 from the earlier table when describing the tie.

The opened SCORECARD defines no numeric rule converting one census finding or four matrix records into a one-point change. `AXES.md`/`LEARNING.md` are not present in the project recursive file search; no scale mapping was available in this seat. Therefore neither 9→10 operability nor 8→9 depth is grounded by row counts, test counts, or prose volume alone. These artifacts provide evidence to the parent, not a score or PASS verdict. A score change requires the parent's rubric and post-integration evidence; the necessary C1 live/fixture outcomes and any independent replay remain unobserved here.

## Confidence and handoff

- **High confidence:** baseline C1 source gap; six-plane contract; current four matrix IDs and their stated independence; S035 status discrepancy; score values/saturation as recorded in SCORECARD.
- **Moderate confidence:** the proposed generalized C1 discriminator follows directly from the owner-write/search contract and existing fixture seams, but implementation and expected verdicts are not present to observe.
- **Low / unresolved:** historical `errno:13` causation. Matrix notes explicitly lack syscall/path evidence, privileged reproduction, Btrfs ioctl ordering, and contemporaneous target state.

No PASS is claimed. Parent checks after integration should verify the C1 outcomes and unchanged six-emitter/six-key rollup once, confirm S035 registry status and preserve C2 independence, then make any score judgment under the applicable rubric.
