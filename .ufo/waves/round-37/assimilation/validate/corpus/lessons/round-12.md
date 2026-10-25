# Round 12 — root metadata without causal overclaim

Campaign date: 2026-10-19 (local -03); captures after 21:00 local carry 2026-10-20 UTC. Author: tsukuroi L1. Baseline: `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`. This is only the explicitly steered round 12; historical training round 11 and the later fleet-round-1 continuation are not renumbered.

## Declared claims

- C1, operability / capability acquisition: replace the census's silent unowned-root metadata blind spot with one explicit packages-plane finding, preserving the six-plane output contract and distinguishing owner-write/search absence from unavailable metadata.
- C2, depth: source-grounded diagnostic branches with direct read-only discriminators for DAC, mount state, service confinement and existing-target controls, independent of C1 output. These are diagnostic branches, not four simultaneously supported host causes.

Depth and adjacency are tied lowest at 8 in the post-review scorecard state; C2 works depth. Scores are ordinal, not counts. No arbitrary 9→10 operability gain or 8→9 depth gain is inferred from artifact volume.

## Gate

- Candidate C1 is pending implementation measurement and outside closure. Baseline live census emits zero root-mode findings; the presence predicate exits 1 (`.ufo/waves/round-12/CensusScribe.md` §8). Rollup is already DEGRADED for unrelated findings, so rollup alone cannot demonstrate the repair.
- Candidate C2 is pending final artifact measurement and outside closure. Parent executed direct host discriminators and isolated ordinary-directory controls; no root capability falsifier, service restart, subvolume creation, boot or upgrade ran.
- Rejected reading: `0555` means a read-only filesystem. Direct `findmnt` reports `rw`, while `stat` reports `555 0 0 directory`; `.ufo/waves/round-12/discriminator-smoke.json` preserves commands, exits and outputs. Flip: an actual relevant mount/namespace observation establishes `ro`; mode alone never does.
- Rejected reading: ordinary `mkdir` always checks parent write before target existence, so `0555` implies EACCES even for an existing name. Parent's uid-1000 fixture returned EACCES for a new name and EEXIST for an existing name under the same 0555 parent (`.ufo/waves/round-12/error-order-smoke.json`). Flip: a separately demonstrated operation/version changes that result. This control does not establish Btrfs ioctl ordering or historical target state.
- No lane-dispatched reviewer is a non-author verifier. Final admission and an admit/reject source spot-check belong to the independent hyaku closure session after landing; SHONEN remains author-asserted.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| vacuous / D6 | Prior `round-1.md` D6; baseline `CensusScribe.md` §8: root_mode_count=0, census_rc=1, predicate exit=1 | QUALITY #13 named the census obligation but no executable root observation existed | C1 must make that same presence predicate pass and retain distinct hermetic 0755/0555/unavailable outcomes; final evidence is recorded below only after execution. |
| stale-premise / kernel ordering | `.ufo/waves/round-12/MountErrors.md` original ordering claim and §6 errata; `error-order-smoke.json` | QUALITY #2–3: a source-scoped inference was presented as unconditional runtime fact | Parent ran the operation in an isolated directory; the existing-name EEXIST counterexample falsified the premise. Retract historical Btrfs attribution; keep ordinary mkdir results and unmeasured ioctl limits separate. |
| attribution / omitted admission check | Outside `round-1-verifier-spotcheck.md:12` disagreed with admission of the adjacency recheck without its promised QUALITY check; post-review repair exists | none explicitly required the section itself before admission | QUALITY #14 below requires the applicable-criteria check in every new knowledge entry before an admit is recorded; self-attestation is not outside agreement. |
| reference-drift / permission proxy | `snapper-eacces-mechanism.md:30`; `.ufo/waves/round-12/SourceReview.md` F1; `Capabilities.md` | QUALITY #2–3, partial | Supersede the claim that the old test-w comparison distinguishes permitted from effective sets. A bounded/unbounded credential comparison is not the actual failed subvolume operation. |

## Planner and scope

The L1 owns the top-level plan and canonical planner seat. The wave member named `Planner` is routed as revenger for the bounded data-walk, per L0's answer and `scripts/hyaku/lane-addendum.md:33-36`; `.ufo/waves/round-12/planner-ruling.md` records the resolution. One validated 32-seat task batch, unchanged dispatcher payload, no model parameters or routing edits. All child evidence is author-side advisory.

The round-11 verifier spotcheck does not exist in the observed lesson directory. The latest outside lesson is `round-1-verifier-spotcheck.md`; its missing-QUALITY-check disagreement motivates criterion #14. No outside record is rewritten and no prior admission is revoked by a child seat's opinion.

## Outside-disagreement learning check

Parent replayed the admission-section criterion on the exact historical knowledge path at `549ec0c1394cfa96702a457a19de672cc1754b2f` and baseline `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`: `## QUALITY check` count 0→1, criterion exits 1→0. Commands and outputs: `.ufo/waves/round-12/admission-check-red-green.json`. The old note repair belongs to round 1; this round claims only the lesson-backed admission criterion, not authorship of that repair. A section-presence check cannot verify its claims; outside source/decision review remains required.

## Mistakes — resumed policy discovery

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| package-baseline versus policy-baseline | `.ufo/waves/round-12/resumed/ClaimCriticR.md`; `/usr/lib/tmpfiles.d/root.conf` contains `z / 555 - - -` | QUALITY #2–3 partially; #13 only required observation | Reject automatic DEGRADED for absent owner-write/search. C1 reports these bits without policy judgment; unavailable/non-directory metadata remains BLOCKED. QUALITY #16 now requires policy and override inspection. |
| stale fixture identity / credential proxy | inherited matrix SC3 described a uid-1000-owned temporary directory as root-owned; resumed `C2ReviewR.md` F3–F4 | QUALITY #2–3 and #15 | Correct fixture ownership and require effective capabilities for actual-operation discussion; a bounding set permits neither runtime-set measurement nor success prediction. |
| write-root / seat evidence misroot | Orchestrator found C1ReviewR.md and SourceReviewR.md under fleet `.ufo/waves/round-12/resumed/`; copied byte-exact into this lane, hashes `5093cc57…` and `7acaf6dd…` | Wave scope stated lane-relative paths but did not enforce absolute write targets | L1 recovered only its two evidence files, never removed fleet originals; Main owns their removal. Re-briefed live seats with absolute lane paths. A fleet-root relative write was the observed failing case; lane absolute copy is the correction. |
| source-access date copied from campaign date | `.ufo/waves/round-12/resumed/SourcesR.md` section 10; clock `2026-10-20T03:50:17Z` | QUALITY #2 source provenance | New unlanded source drafts S038–S040 incorrectly used campaign date 2026-10-19; their author corrected to actual 2026-10-20 before landing and logged the draft correction. Inherited opened dates were not rewritten. |

## Resumed contract and inherited evidence

The earlier headless launch ended mid-wave, as the committed digest in
`.ufo/waves/round-12/resumed/dispatch-history.json` records. The new L1
dispatched one additional validated batch of 32, not a substitute unvalidated
planner seat. Both batches remain round-12 evidence; all seats are
author-side. The L1 owns the planner function; `Planner`/`PlannerR` are
revenger-routed bounded data-walks.

Inherited QUALITY/SOURCES, matrix drafts, this lesson and first-wave evidence
were reused only after targeted re-reading. Discarded premises: automatic
mode-0555 degradation, unknown configured mode origin, root-owned temporary
fixtures, bounding-set-as-effective-set proof, universal syscall ordering
and permission-proxy-as-historical-cause. Old evidence remains historical,
not newly executed. No outside/aggregator-authored file was edited.

The refined C1 claims an observable metadata arm, not a new policy requiring
owner-write. C2 claims sourced distinctions/controls on an existing surface,
not four independent causes, new coverage or a demonstrated Btrfs repair.
Advisory seat prose asserting host causal certainty or automatic score gains
is rejected; the landed matrix's explicit limits govern the claim.

Parent JSON evidence under `resumed/` is authored by this round's L1.
Inherited smoke/admission JSON was predecessor-L1 evidence; its recorded
isolated controls are not independent review. The re-executed historical
QUALITY-heading presence predicate in
`resumed/admission-criterion-red-green.json` exits 1 at `549ec0c` and 0 at
`b76b5c3`; it demonstrates only the necessary heading-presence condition,
not full admission or all pointer resolution.

## Gate — resumed source openings and decisions

All access dates below are 2026-10-20 for the resumed opening; inherited
S035–S037 retain their predecessor-author opened date. Quotes are located
excerpts, not evidence of host causal truth. Source-seat reopens:
`.ufo/waves/round-12/resumed/SourcesR.md` sections 2, 8–10.

| New row | Source opened | Location | Located quote (at most 25 words) | Decision |
|---|---|---|---|---|
| S035 | https://man.archlinux.org/man/mkdir.2 | ERRORS / EROFS; man-pages 6.19, 2026-02-11 | “path refers to a file on a read-only filesystem.” | Admit API-level errno distinctions only; not Btrfs ioctl ordering. |
| S036 | https://github.com/omacom/omarchy/issues/8047 | Issue body; maintainer-bot comment 2026-10-09 | “snapshot rollback cannot work on a stock Omarchy install” | Reject as host cause/support: disputed community assertion; flip requires primary method-scoped evidence or independent reproduction. |
| S037 | https://github.com/omacom/omarchy/issues/6629 | Issue body / symptom description | “defaults to an inactive (dead) state because limine-snapper-watcher fails with inotifywait is not installed” | Reject as host cause/support: version-scoped packaging report is not proof of this host's permission mechanism. |
| S038 | https://man.archlinux.org/man/access.2 | DESCRIPTION / permission-check question; man-pages 6.19, 2026-02-08 | “access() does not answer the "can I read/write/execute this file?" question” | Admit narrower permission-proxy scope; supersedes S034's overbroad teaching. |
| S039 | https://man.archlinux.org/man/tmpfiles.d.5 | z line type; systemd 262.1 | “Adjust the access mode, user and group ownership, and restore the SELinux security context of a file or directory, if it exists.” | Admit policy interpretation when cited by the matrix, not historical attribution. |
| S040 | `/usr/lib/tmpfiles.d/root.conf`; https://api.github.com/repos/systemd/systemd/commits/7b2a10b594d7 | Local line 10; upstream commit `7b2a10b594d7ed0f463b78f29f1b30f8c1c6e64e` | “z / 555 - - -” | Admit current declarative policy; present policy does not prove an incident-time causal history. |

S040 corroboration also opened: https://raw.githubusercontent.com/systemd/systemd/main/NEWS,
CHANGES WITH 261: “A new tmpfiles.d/root.conf has been added that sets permissions
on the root directory (/) to 0555.” Source count is not a quality measure.

Mutable-field changes, from the inherited working state:

- S027 used-by `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/snapper-eacces-mechanism.md`
  → same two paths plus `corpus/knowledge/root-dac-decision-r12.md`.
- S028 used-by: the same old two paths → the same two plus the matrix path.
- S034 used-by `corpus/knowledge/snapper-eacces-mechanism.md`
  → that path plus the matrix path; the old immutable teaching is superseded by S038.
- S035 status `queued` → `mined`; used-by `—` → the matrix path.
- S036/S037 status/recheck/used-by unchanged (`rejected` / `90d` / `—`).
- S038 added mined with matrix used-by; S039/S040 initially queued with `—`.
  Their eventual usage transition, if made, is logged in the final integration below.
- No existing recheck field changed. New-draft date correction is logged under Mistakes.

The gate admits the corrected C2 entry on the lane's own evidence only,
subject to the final integration measurements and independent closure.
It rejects universal mode policy, permission-proxy causality, universal
errno priority and issue-symptom equivalence. At least one admit and reject
still require the independent non-author spot-check; no dispatched seat
supplies that authority.

### Final source usage and evidence handling

After the matrix cited the policy rows, S039 and S040 each changed status
`queued` → `mined`, used-by `—` →
`corpus/knowledge/root-dac-decision-r12.md` (source-seat final confirmation).
S038–S040 are newly drafted this resumed attempt; their author corrected
draft access dates from copied campaign date to the measured 2026-10-20
before landing. No prior committed registry row was rewritten.

L1 retained each canonical resumed `<Seat>R.md` and removed duplicate
unlanded alias copies. The sentinel's scan found no credentials but identified
raw journal bodies outside the sanitized-metadata contract; L1 replaced those
excerpts in inherited Issue6629/RootLive/MatrixCritic/C2Review and resumed
Issue6629R/RootLiveR/OverlapHostR with dated aggregate findings. These edits
sanitize unlanded evidence, not a rewrite of filed round history.

## Gate — measured integration

Path shorthand `resumed/` in this section denotes repo-relative
`.ufo/waves/round-12/resumed/`.

The final measured implementation is
`70fede2a7a890cb50a72db2d4230ee541183bf7b`, not the earlier moving-review
snapshots. L1's single shipping selftest: 97/97, exit 0, two named skips;
live census exit 1, six-plane DEGRADED, one root-metadata record. Baseline
`b76b5c3` had zero records and the presence predicate exited 1.
Evidence: `resumed/{selftest-after,live-after,after}.json`.

The policy correction is shown able to fail: the sole inserted automatic
DEGRADED assignment in an isolated mutant produced exit 1 and four named
failures, including the 0555 report-only finding; shipping code was not
changed (`resumed/mode-policy-mutant.json`). A capture-script assertion
initially looked on stdout instead of stderr; it was fixed from the retained
output with no mutant rerun.

The source-resolving branch counter gives 0→4, exits 0→0, and all criteria
1–16 are explicitly evaluated. Fresh ordinary-mkdir controls returned errno
13 for new-name 0555, errno 17 for existing-name 0555, and success for
caller-owned 0755. These prove only those controls, not Btrfs causality:
`resumed/count-commands.json`, `resumed/mkdir-controls.json`.

Start source validation (both inherited first-wave and resumed captures):
`tsukuroi ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`,
exit 0. End: same ok line, exit 0, plus W04 for S038's deliberate duplicate
access(2) URL with corrected scope. Source rows: baseline 34 → inherited 37
→ final 40; final tiers A35/B1/C4, statuses mined30/queued5/rejected5.
The exact validator command and uncollapsed outputs are in
`resumed/{before,sources-after,inheritance}.json`.

Author-side admission supports C1/C2 with no measured code regression;
non-author source/decision sampling and final hyaku adjudication remain
required. SHONEN's four marks stay `[~]`. No service or filesystem repair,
upgrade clearance, independent promotion or next-round execution is claimed.
