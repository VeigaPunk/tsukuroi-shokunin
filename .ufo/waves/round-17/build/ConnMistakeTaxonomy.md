# ConnMistakeTaxonomy — defect classes across r1 and r12–r16

Axes: class coverage · evidence attribution · recurrence signal. Basis: `corpus/lessons/round-1.md` M1–M13/D1–D6, `round-12..16.md` § Mistakes, the five non-author spot-checks. `Q<n>` = `corpus/QUALITY.md` item.

| class | rounds | captured-by | fix shown able to fail? |
|---|---|---|---|
| locator/citation drift (section, line, pointer) | r1 M1/M12, r15, r16 | Q7→Q21→Q23 | yes from r16: red at real loci 581/398, 43/43; Q21 (r15) left section numbers uncovered → Q23 |
| claim exceeds source / attribution | r12, r13 R13-BOT, r14 | Q2/3/7→Q17/18→Q19/20 | yes r14, restored-defect fixtures; blind to novel replacement prose (r13) |
| counter green, prose false | r12–r16 | Q17, Q19 (prose rules only) | NO: red always targets the preserved old defect |
| fixture/proxy identity | r1 D3/D6, r12, r13 R13-FIXTURE | Q13/15/18 | criterion-only, never executable |
| negative claim unswept | r1 M3, r14, r15 | Q9, Q22 | partial: r15 red `NEGATIVE_DOMAIN_UNSWEPT` |
| freshness / stale current-use | r1 M7/D2, r12, r13, r14, r15, r17 | Q8; `measure-update-recheck.py` | NO: probe exits 0 ABSENT→COUNTED; no verdict gate |
| execution scope (who may run what) | r15, r16, r17 | Q24 (seats), Q26 proposed | NO: Q24 never shown red; L1 uncovered |
| landing/LOG hygiene | r1 M8/M11, r12 | Q10/11, PROTOCOL | yes, external check (r12 `f3868cd` red) |
| gate spec > executable | r13–r16 | prose demotion each time | NO |
| procedure embeds forbidden command | r1 D1, r17 | Q6 (operator advice only) | NO |

**r17 and existing classes.** [obs] `corpus/knowledge/initramfs-v42-sysroot-recovery.md:3` prescribes `pacman -Q`; the r17 captures avoided it (`l1-capture/boot-chain-capture.txt:31` uses `ls -d /var/lib/pacman/local/…`; `fresh-capture.txt:2` "no pacman invocation"). [obs] `build/LessonDraft.md:8` records the round-17 run as `[unk]`; [inf from peer] `CritMinedMistake.md:5,7-9` locates the steer (`history://TsukuroiR17:9`: "read-only — never run pacman") and one `pacman -Q` on 13 packages (`TsukuroiR17.jsonl:51-52`), cause habitual, not the recheck line.

It belongs to **two** existing classes: execution scope (row 7) and procedure-embedded command (row 10, D1/MC1 lineage). Neither criterion reaches it — Q24 names wave seats, Q6 names operator advice — so `captured-by: none` is correct, but the drafted label "steer-scope violation" hides the D1 lineage and the six-file corpus form the critic found. `corpus/QUALITY.md` ends at 24, so the row's "QUALITY26" is a proposal.

**Recurring, no demonstrated fix**, harm-ordered: counter-green/prose-false (only outside review caught r12/r13); execution scope (3 rounds; the landed `tools/check-seat-scope.py` reads registry/spec seats, so it cannot see L1); freshness (6 rounds; a 0→N notice count cannot detect an unwarned stale statement — r16's own objection to missing-file reds); gate-spec overreach; procedure-embedded commands (the proposed gate stays green on the actual event).

**Hazard:** `drafts/lesson-r17.md:48` would land a Mistakes row carrying `<L1 fills … UNVERIFIED>`. Q3 separation requires citing the transcript pointer or marking the run `[unk]` separately — not both in one cell.

Not verified: the transcript myself; whether `check-recheck-commands.py` or the `check-seat-scope.py` r16 demonstration lands.

Scope: executed=none
