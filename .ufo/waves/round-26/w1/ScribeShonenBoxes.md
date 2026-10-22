# ScribeShonenBoxes — replacement evidence lines for SHONEN boxes 1, 3 and 4 (round 26, wave 1)

Verdict: done — three replacement evidence lines are proposed for boxes 1, 3 and 4; every corpus/knowledge path they name exists at the claim base `e9f5356c` and carries no `superseded` word in its first 20 lines, box 4 no longer cites the superseded round-12 PROVINCE refinement as current, box 3 no longer cites `corpus/knowledge/root-dac-decision-r12.md`, every box stays `[~]`, and the seed block still diffs byte-identical modulo `<name>`.

## 1. Scope and what was not touched

- [obs] The lane was not edited. The only file this seat wrote is this report, at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/ScribeShonenBoxes.md`. `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain` was not run as a write; the working tree was read only through `git show`, `git ls-tree`, `git cat-file` and `git archive`.
- [obs] All candidate lines were tested in a private sandbox, `/fast/scratch/hyaku/tsuku26/ScribeShonenBoxes/sandbox/`, built with `git archive e9f5356c | tar -x -C <dir>` and a sandbox-only `git init`. No remote was added and nothing was pushed.
- [obs] Box 2 was not part of this assignment and is not proposed for change. The line for box 2 is already compliant with K24 (it names `corpus/knowledge/host-health-report-r3.md` and `corpus/knowledge/adjacency-handoffs-fleet-r1.md`, both clean of a `superseded` marker in their first 20 lines). [inf] Box 2 still has the separate round-25 RevShonen finding about the word "current" and the delivery clause; that is a different defect and out of this seat's scope.
- [obs] The canonical form allows only the box mark plus one indented evidence line per box (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:446`, seed at lines 455-462). Each proposed replacement is exactly one indented line. No box wording and no box mark is changed.

## 2. The defect being repaired, and where it lives

- [obs] The base SHONEN.md at `e9f5356c` cites `corpus/knowledge/root-dac-decision-r12.md` in box 1 and again in box 3. That note carries a whole-note supersession notice at its line 7: `> **Superseded after outside rejection.** Read` (`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show e9f5356c:corpus/knowledge/root-dac-decision-r12.md`, line 7). This is exactly the pattern the round-26 declaration says K24 to K27 detect: "none of its first 20 lines matches the case-insensitive word `superseded`" (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:904`).
- [obs] A simulation of the declared K24 to K27 rule over the base file confirms the base fails on exactly two boxes: box 1 (K24, cites the r12 note) and box 3 (K26, cites the r12 note). Box 2 (K25) and box 4 (K27) already pass, because box 4 names no `corpus/knowledge/*.md` path at all.
- [obs] The round-26 declaration already states that K24 to K27 "detect a supersession notice in a cited note's first 20 lines ... appended statement-level errata, `.json` companions and box 4's citation of a superseded PROVINCE paragraph are not counted. Box 4's evidence line is still repaired in text" (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:924`). [inf] This seat therefore treats the box 4 repair as required text work that the mechanical check does not count, exactly as the declaration says.
- [obs] The superseded round-12 PROVINCE refinement is at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:85-90`. The active refinement is named at `PROVINCE.md:92-106`: line 92 reads "Round-13 correction R13-DAC-EXCLUSIVITY: the active refinement is now" and line 98 reads "Round-14 source-scope erratum: R14-VALUE-DOMAIN and R14-COMMENT-ATTRIBUTION". The base box 4 cited "PROVINCE.md round-12 refinement" as current evidence, which is the round-25 RevShonen finding 3.

## 3. Proposed replacement evidence lines

The three lines below are the deliverable. Each replaces exactly the one indented evidence line of its box; the box mark `[~]` and the box wording are untouched.

### Box 1 — SKILL.md contains real decision tables, error patterns, checklists, cited sources

```
  Author-side evidence: SKILL.md carries the health-verdict decision table (SKILL.md:38-50), the update-safety checklist (SKILL.md:90-141), the error-pattern list (SKILL.md:2028-2036) and the Sources section (SKILL.md:179-209); the decision table's per-plane notes are corpus/knowledge/package-state-plane.md, corpus/knowledge/systemd-user-plane.md, corpus/knowledge/driver-firmware-plane.md and corpus/knowledge/aur-risk-plane.md, and the root-metadata procedure is SKILL.md:1676-1753. The round-12 matrix pointer inside that procedure is marked historical by SKILL.md:1717-1721, so no superseded note is cited here. Non-author verification of the SKILL.md content remains owed.
```

- [obs] Every cited anchor resolves at `e9f5356c`: `SKILL.md:38` is `## Health-verdict decision table (per plane)`, `:90` is `## Update-safety checklist (read-only until the stop line)`, `:179` is `## Sources`, `:2028` is `### Error patterns`, `:1676` is `## Round 12 — root metadata and create-failure discrimination`, `:1717` is `## Round 13 — active unit-path correction (R13-DAC-EXCLUSIVITY)` whose line 1719 reads "The round-12 matrix pointer above is a historical entry rejected at outside closure".
- [obs] The four per-plane notes are the notes the decision table's own "Measured" column cites: rows 46, 47, 48, 49 and 50 of `SKILL.md` at `e9f5356c` name `package-state-plane.md`, `systemd-user-plane.md`, `driver-firmware-plane.md` and `aur-risk-plane.md`.
- [obs] The line does not name `corpus/knowledge/root-dac-decision-r12.md` at all, so K24 has nothing superseded to flag. [inf] The wording "marked historical by SKILL.md:1717-1721" is accurate: `SKILL.md:1719-1721` retires that pointer and redirects to the r13 note. It says so without naming the note, which is what keeps the path grammar from naming a superseded note.
- [obs] The line states what is unverified: "Non-author verification of the SKILL.md content remains owed."

### Box 3 — Instructions executable by an agent without oral context

```
  Author-side evidence: corpus/knowledge/adjacency-handoffs-fleet-r1.md:136-186 holds the counting contract and the read-only replay steps, SKILL.md:522-532 holds the no-oral-context executor checklist and SKILL.md:453-551 the round-3 append, and corpus/knowledge/executor-test-sufficiency.md:15-20 and :106-136 records the one executed no-oral-context run, against a 444-line SKILL.md rather than the SKILL.md at this revision. The unit-path procedure in force is named at SKILL.md:1717-1721, and no superseded note is cited here. The whole-SKILL post-append no-oral-context retest remains unexecuted and no non-author has replayed it.
```

- [obs] The anchors resolve at `e9f5356c`: `corpus/knowledge/adjacency-handoffs-fleet-r1.md:136` is `## 4. Counting contract records` and `:161` is `## 5. Read-only replay and stop line`, so the cited range covers both; `SKILL.md:522` is `### Executor checklist (no-oral-context, self-contained)` and `:453` is `## Round-3 append — census-v2 in the gate + the no-oral-context executor test (TSUKUROI-R3-4)`; `corpus/knowledge/executor-test-sufficiency.md:15` is `## 1. Revisions under test and polling history [observed]` whose line 19 records the document under test as 444 lines, and `:106` is `## 3. Per-step sufficiency (the core measure)`.
- [obs] The line does not cite `corpus/knowledge/root-dac-decision-r12.md`, satisfying the assignment constraint directly and clearing K26.
- [obs] The line states honestly what is unverified: the executed test ran against a 444-line `SKILL.md`, not the 2355-line file at `e9f5356c`; the whole-SKILL post-append retest is unexecuted; no non-author has replayed it. [obs] The base box 3 said the same thing about the retest but attached it to a superseded note, which is what made K26 fail.
- [inf] Citing the executor checklist at `SKILL.md:522-532` is the more direct evidence of "executable without oral context" than the adjacency note alone, because the checklist is the document an executor reads; the adjacency note supplies the replay contract and the stop line.

### Box 4 — No cross-domain bleed (PROVINCE.md still accurate)

```
  Author-side evidence: PROVINCE.md:44-52 is the ADJ-01 to ADJ-07 finding-to-owner table, PROVINCE.md:121-146 the round-19 ownership anchors with their pinned digests, PROVINCE.md:148-152 the R20 OUT-009 clarification and PROVINCE.md:75-83 the frontier limits, with the sibling pin re-check in corpus/knowledge/adjacency-recheck-2026-10-19.md and the pointer census in corpus/knowledge/adjacency-anchors-r19.md. The active refinement is the round-13 correction and the round-14 erratum named at PROVINCE.md:92-106, while the round-12 refinement paragraph at PROVINCE.md:85-90 is historical, not current. Contested kaidoku and revenger reverse-engineering ownership is unruled, the kill and OOM classification boundary against SKILL.md:1078-1102 is unexamined, and recipient acknowledgement and acceptance are unobserved, so no cross-domain bleed is verified here.
```

- [obs] The anchors resolve at `e9f5356c`: `PROVINCE.md:44` is the `| ID | Finding / boundary trigger |` header and rows 46-52 are ADJ-01 to ADJ-07; `:121` to `:130` are the OUT-001 to OUT-010 anchor rows and `:137` to `:146` their portable digests; `:148` is `## R20 ownership clarification — OUT-009`; `:75` is `## Frontier` and its two bullets plus the "Out of province" rule run to `:83`.
- [obs] The line names the superseded round-12 PROVINCE refinement only to mark it historical, and names the round-13 and round-14 pair at `PROVINCE.md:92-106` as the active refinement. This is the assignment constraint on box 4.
- [obs] The line states what is unverified: contested kaidoku and revenger reverse-engineering ownership is unruled, the kill and OOM classification boundary against `SKILL.md:1078-1102` is unexamined, and recipient acknowledgement and acceptance are unobserved. [obs] The `SKILL.md:1078-1102` range is the lane's own kill-event class table (`### The kill-event classes — two kill waves, two classes (S8-2)` at 1078, class table at 1099-1105), which the round-25 RevShonen finding 3 named as an unexamined boundary against `PROVINCE.md:125` OUT-005. [inf] The base box 4 dropped that clause entirely; this line restores it.
- [obs] The base box 4 also cited `.ufo/waves/round-12/resumed/OverlapHostR.md`. That path exists at `e9f5356c`, but per round-25 RevShonen finding 3 it is a round-12 scan that does not examine PROVINCE.md at the measured revision, so it is dropped from the replacement.

## 4. Verification of every cited corpus/knowledge path

Requirement: for each cited `corpus/knowledge` path, show that it exists at `e9f5356c` and that its first 20 lines contain no word `superseded` (case-insensitive). All eight distinct cited paths, checked with `git cat-file -e e9f5356c:<path>` and `git show e9f5356c:<path> | head -20`:

| Cited path | Exists at `e9f5356c` | `superseded` (word, case-insensitive) in first 20 lines | Any `supersed*` form in first 20 lines |
|---|---|---|---|
| `corpus/knowledge/package-state-plane.md` | yes | 0 | 0 |
| `corpus/knowledge/systemd-user-plane.md` | yes | 0 | 0 |
| `corpus/knowledge/driver-firmware-plane.md` | yes | 0 | 0 |
| `corpus/knowledge/aur-risk-plane.md` | yes | 0 | 0 |
| `corpus/knowledge/adjacency-handoffs-fleet-r1.md` | yes | 0 | 0 |
| `corpus/knowledge/executor-test-sufficiency.md` | yes | 0 | 0 |
| `corpus/knowledge/adjacency-recheck-2026-10-19.md` | yes | 0 | 0 |
| `corpus/knowledge/adjacency-anchors-r19.md` | yes | 0 | 0 |

- [obs] The last column is a stricter test than the declared rule and is reported because it removes any argument about the marker. Every cited note is free of even the stem `supersed` in its first 20 lines, so the proposed lines survive a stricter implementation of K24 to K27 than the one declared.
- [obs] The same table over the base file, for contrast: `corpus/knowledge/root-dac-decision-r12.md` exists at `e9f5356c` and has 1 occurrence of the word `superseded` in its first 20 lines (line 7), which is the sole cause of the base K24 and K26 mismatches.

## 5. Mechanical check run on the proposal

- [obs] In the sandbox, with the three lines written into `SHONEN.md` over the base tree, `python3 tools/check-self-assessment.py --revision HEAD` (the base tool, 23 checks) reported `mismatches 1`, exit 1, and the single mismatch was K10: "depth row states 26 lesson files; corpus/lessons holds 27 files". K20, K21, K22 and K23 all reported `match`, with box 1 naming 5 existing paths, box 2 naming 3, box 3 naming 3 and box 4 naming 4.
- [obs] The K10 mismatch is a pre-existing axes-table staleness at the base revision, present with or without this change; it is the L1's item under the round-26 axes-table refresh, not a consequence of the proposed lines.
- [obs] A simulation of the declared K24 to K27 rule over the proposed file returned `match` for all four boxes: box 1 names four corpus notes, box 2 names two, box 3 names two, box 4 names two, and every one of the ten corpus-note instances has zero `superseded` occurrences in its first 20 lines and exists at `e9f5356c`.
- [obs] Canonical form over the proposed file: stripping the box marks and the indented evidence lines reproduces the canonical seed byte-identically modulo `<name>` (compared against `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:455-462`); four boxes; four indented evidence lines; marks `['[~]', '[~]', '[~]', '[~]']`; neither `root-dac-decision-r12` nor `corpus/knowledge/root-dac-decision-r12.md` appears anywhere in the proposed file.
- [obs] One draft of box 4 failed K23 with "SHONEN box 4 names 1 path(s) absent at the revision: kill/OOM". The cause is the declared path grammar in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-self-assessment.py`: a token holding a `/` is a path, so `kill/OOM` was read as a path that names nothing. The final wording says "kill and OOM" and the check then passes. [inf] The L1 should know this grammar behaviour when it writes the K24 to K27 implementation: any slash inside prose in a box evidence line will be read as a path.

## 6. Residual limits and out-of-scope items

- [unk] The proposed lines are not verified by a non-author. They are author-side proposals; a fresh non-author seat must confirm them before any box could be considered for `[x]`, and every box stays `[~]` here.
- [unk] Whether the whole-SKILL no-oral-context retest ever runs is unresolved. The line says so rather than implying the box is satisfied.
- [unk] The kill and OOM classification boundary against `SKILL.md:1078-1102` remains unexamined, and the kaidoku and revenger reverse-engineering ownership question remains unruled by the protocol integrator. The line says so; it does not resolve either.
- [obs] Out of scope and unchanged: box 2's evidence line; the base K10 axes-table staleness; the r13 and r14 notes themselves, which are the active refinement and were not modified; and every file outside this seat's own paths.
- [obs] `tools/check-self-assessment.py` at `e9f5356c` implements only K01 to K23. K24 to K27 are declared at `SCORECARD.md:904` and were simulated here from that declared text, not from a shipped implementation. [unk] Whether the shipped v2 implementation matches the declared wording exactly is unverified by this seat.

## 7. Commands run

- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree -r --name-only e9f5356cd68c9281d07a22e54d1bfd72b12306ac` (corpus/knowledge and corpus/lessons listings)
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show e9f5356c:<path>` for `SHONEN.md`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `corpus/knowledge/root-dac-decision-r12.md`, `corpus/knowledge/root-dac-correction-r13.md`, `corpus/knowledge/source-scope-correction-r14.md`, `corpus/knowledge/executor-test-sufficiency.md`, `corpus/knowledge/adjacency-handoffs-fleet-r1.md`, `corpus/knowledge/adjacency-anchors-r19.md`, `corpus/knowledge/adjacency-recheck-2026-10-19.md`, `corpus/knowledge/contract-corrections-r20.md`, `corpus/knowledge/host-health-report-r3.md`, `corpus/knowledge/package-state-plane.md`, `corpus/knowledge/systemd-user-plane.md`, `corpus/knowledge/driver-firmware-plane.md`, `corpus/knowledge/aur-risk-plane.md`
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -e e9f5356c:<path>` (existence check for every cited path)
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive e9f5356cd68c9281d07a22e54d1bfd72b12306ac | tar -x -C /fast/scratch/hyaku/tsuku26/ScribeShonenBoxes/sandbox` then `git init` in the sandbox (sandbox-only, no remote)
- `python3 tools/check-self-assessment.py --revision HEAD` inside the sandbox, on the base tree and on the tree carrying the three proposed lines
- Python simulations of the declared path grammar (`path_candidates`, `expand_braces`, `resolve_paths` copied from `tools/check-self-assessment.py`) and of the declared K24 to K27 rule, over the base file and over the proposed file

Scope: read=the lane SHONEN.md, PROVINCE.md, SKILL.md and SCORECARD.md at e9f5356c, the round-25 RevShonen review, the round-25 verifier spot-check, the round-26 SCORECARD declaration (base file and working tree), the canonical PROTOCOL.md seed and the SHONEN file-contract row, tools/check-self-assessment.py, and the corpus/knowledge notes cited above; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/ScribeShonenBoxes.md, /fast/scratch/hyaku/tsuku26/ScribeShonenBoxes/sandbox/ (sandbox-only clone, commits and check outputs); executed=git ls-tree, git show, git cat-file, git archive, git init and sandbox git commit (sandbox only), python3 tools/check-self-assessment.py --revision HEAD in the sandbox, plus read-only Python simulations of the path grammar and the K24 to K27 rule.

Model: opencode-go/minimax-m3.1-flash-free
Installs: none
