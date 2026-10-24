# Round 36 scope and bounds review

**Lane root:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`  
**Verdict:** No out-of-surface change is observed in the checkout snapshot. All present round-36 untracked artifacts are under `.ufo/waves/round-36/`; the current change since declaration is wave metadata only. Production edits are planned for the L1 integration, not authorized for seats.

## Allowed-path table

| Planned path (lane-relative) | Round-level allowed touch | Seat write boundary / guard |
|---|---|---|
| `tools/check-revision-binding.py`; `tools/check-report-receipts.py`; `tools/score-census-handoff-r32.py`; `tools/mutants-btrfs-space-r30.py`; `tools/run-receipt.py` | C1 fixed-dictionary child-environment changes only, as declared. | Production files: seats may read and report patches/findings only; L1 applies changes. No direct seat edits. |
| `tools/probe-child-env-allowlist-r36.py` | New C1 counter/probe; freeze pins its bytes, predicate/label, set, and after-value. | Same: L1 integration only; seat outputs belong in that seat's evidence directory. |
| `corpus/knowledge/journalctl-v262-field-filter-r36.md` | New C2 note, sourced by S024 and S198. | L1 only; seats do not edit `corpus/`. |
| `corpus/SOURCES.md` | S198 addition and the declared S024 reopen/pin evidence. | Append-only; do not rewrite or delete old rows. L1 only. Preserve S024's prior queued/mutable-main record and append a dated pinned-reopen correction/provenance record. |
| `SKILL.md` | Add the declared registry entry and one of the four NoUpgrade/NoExtract correction append sites (the prior lines 397–399). | L1 only. Keep the old assertions/history; append the supersession correction rather than replacing old text. |
| `corpus/knowledge/update-safety-note.md`; `corpus/knowledge/update-safety-v2.md` | The remaining three of the four declared NoUpgrade/NoExtract correction append sites: update-safety-note at prior lines 420–424; update-safety-v2 at prior lines 52 and 198. | L1 only. Append corrections; do not rewrite history. |
| `SCORECARD.md`; `LOG.md` | Round-36 outcome/reporting additions after the declaration. | Append-only, L1 only; do not edit historical rows/claims. |
| `corpus/README.md` | One row for the new C2 note. | L1 only; add the declared row, with no unrelated edits. |
| `corpus/lessons/round-36.md` | New lesson file after the round evidence is settled. | L1 only; no seat writes in `corpus/`. |
| `.ufo/waves/round-36/w1/` | Wave-1 seat reports and evidence; wave metadata/registry is orchestrator-managed. | Each seat writes only its own `w1/<SeatName>/` directory. SentScope's sole report location is `w1/SentScope/`; never edit peer evidence or wave-root metadata. |
| `.ufo/waves/round-36/w2/` | Wave-2 falsification reports and evidence. | Future wave-2 seats write only their own `w2/<SeatName>/`; SentScope has no write authority there. |
| `.ufo/waves/round-36/l1/`; `.ufo/waves/round-36/after/` | L1 integration and after-state evidence, per the declared sequence. | L1/orchestrator-owned; no seat writes there. |
| `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz` | Already committed evidence, explicitly carried forward by the declaration. | Read-only; do not modify or relocate. The declaration tree records blob `5ef93e98461758e485a8375da246ec637e8d503e`. |
| `corpus/QUALITY.md`; `SHONEN.md` | **Not in the declared round-36 touch set.** | Leave untouched; if separately authorized later, append-only. Any edit in this round is out of the planned surface. |

**Hard exclusions:** anything outside the lane root; fleet-root files, sibling lane repositories, `.ufo/state/`, `.ufo/watchdog.log`, `MANIFEST.json`, templates, fleet scripts, another seat's directory, or any production-file write by a seat. No mutating VCS/index operation. The full-round path list does not enlarge a seat's write allowance: seats report evidence/patches; L1 lands production changes.

## Wave-2 watchlist

1. Keep wave-2 evidence under the individual seat's `.ufo/waves/round-36/w2/<SeatName>/`; keep L1's integration and after captures in their L1-owned directories. Do not write to fleet/shared state or sibling lanes.
2. Once frozen, do not change `tools/probe-child-env-allowlist-r36.py`, its `PREDICATE`/`leaking_pairs` label, `livefive` set, or declared after-value. Receipts must identify the frozen tool revision; a control or after-mutant that satisfies the declared kill condition is a C1 failure, not grounds to alter the counter.
3. Keep falsification variants and their artifacts as evidence, not direct edits to the five production tools. Do not edit wave-1 receipts/reports or another seat's files.
4. C2 integration stays within the declared note, SOURCES row(s), SKILL registry/correction appendices, README row, lesson and round outcome/log. `corpus/QUALITY.md` and `SHONEN.md` are not expected destinations.
5. Do not publish raw environment/secret values in receipts; record only the probe's declared normalized results and necessary evidence.
6. The current plan reports `resume: 0`; no `resume_continuity_v1` rejection is present in this wave plan, so no such rejection/mutation case was exercised by this scope review.

## Findings and evidence

- **No observed scope breach (informational).** `git diff --name-only 6d76fb20f6ecbc940e5c8fff36c74060c885e161..HEAD` lists only `.ufo/waves/round-36/` spec/plan/dispatch/registry metadata. At the inspected worktree snapshot, `git status --short --untracked-files=all` reported zero staged and zero unstaged paths; its 23 untracked paths were all beneath `.ufo/waves/round-36/` (mostly wave-1 seat artifacts). No fleet-root, sibling-lane, `.ufo/state/`, or production path was reported. Current HEAD is `189d8a080ba8d508d5faab12cad9e688aee91dab` (`round-36: wave-1 spec, plan, dispatch payload and registry (32 seats)`).
- **Medium — append-only source-provenance collision (prospective, no overwrite observed).** Exploit path: an integrator changes S024's status/URL in place to make its old mutable `main` URL appear to be the newly reopened pinned source. Evidence: `corpus/SOURCES.md` row S024 (line 30) currently says `queued` and points to `systemd/NEWS` on `main`; the declaration says S024 is reopened pinned this round, while its append-only rule prohibits rewriting old source history. S198 is not yet present in the inspected SOURCES file. Impact: loses the historical queued/mutable-source state and weakens reproducibility. Smallest remediation: preserve S024 as-is and append the dated pinned-reopen provenance; add S198 as a new row.
- **High if violated — seat-level production-write bypass (no such write observed).** Exploit path: a seat directly edits one of `tools/`, `corpus/`, `SKILL.md`, `SCORECARD.md`, or `LOG.md`, bypassing L1's review/integration. Evidence: the wave contract explicitly says seats must not edit production files and L1 lands production changes; the declared C1/C2 paths include production files but do not grant seat write access. Impact: unreviewed changes can enter a freeze/receipt lineage and invalidate attribution. Smallest remediation: keep all seat findings/patches inside that seat's own report directory; have L1 apply and commit only the reviewed, in-surface changes.

At inspection, `.ufo/waves/round-36/w2/` and `after/` were not yet present; this is consistent with the declared wave-1 → freeze/change → wave-2 order, not a blocker. The tarball is already present in the declaration commit and is read-only for this seat. No tests, tools, or other runtime were invoked; no production files were edited.
