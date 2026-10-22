# RevShonen: SHONEN.md at 5e7c04ecb02735491456de2b8bc44550d0db4609 (round 25, wave 2)

Verdict: partly holds. The one-phrase edit keeps the content of box 2 and passes the canonical-form check, but no file in the round-25 record at 5e7c04ec says it was made, and it only clears a path rule the lane itself declared. Box 1 holds with caveats. Box 2 holds for its completed round-3 task but not for its "current" and "delivery" clauses. Boxes 3 and 4 are not supported by their evidence pointers as written.

## How I checked

- The measured tree came from `git archive 5e7c04ecb02735491456de2b8bc44550d0db4609` into `/fast/scratch/hyaku/tsukuroi-r25/w2/RevShonen/`, with a sandbox-only `git init` and commit. Every line reference below is a line of that tree, which is the lane file at 5e7c04ec.
- The base tree came from `git archive b9046016831237cd04d38da11ba76e50d5380c53` into `/fast/scratch/hyaku/tsukuroi-r25/w2/RevShonen/base-sandbox/` (sandbox commit only).
- The lane and fleet repositories were read with `git show`, `git log`, `git diff` and `git cat-file` only.

## Measured results

- The SHONEN diff is one line, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SHONEN.md:8`. The substring `/` became ` and `, so the file grew from 1309 to 1313 bytes. Line count, final newline and every other line are unchanged. [obs]
- After stripping box marks and the indented evidence lines, SHONEN.md matches the canonical seed at `/home/vgpnk/Projects/shokunin/PROTOCOL.md:441-448` at both revisions. [obs]
- I ran the measured-commit tool `tools/check-self-assessment.py` from the rev sandbox against the base tree data. Output: mismatches 13, exit 1. Check K21 (box 2) failed with "SHONEN box 2 names 1 path(s) absent at the revision: observation/request". This reproduces the lane's stated 13. [obs]
- The same tool against the rev tree gives mismatches 0, exit 0. K21 passes with "SHONEN box 2 names 3 existing path(s)". Checks K20, K22 and K23 pass at both revisions. [obs]
- Output files: `/fast/scratch/hyaku/tsukuroi-r25/w2/RevShonen/RevBase.check-base.json` and `/fast/scratch/hyaku/tsukuroi-r25/w2/RevShonen/RevShonen.check-rev2.json`.

## Findings, by severity

### 1. High: box 2 makes "current" and "delivery" claims the lane's own records do not support

- "current". The lane's copy of the round-1 report calls TSUKUROI-F1-MEM-01 "the inherited historical packet" at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/reports/round-1/tsukuroi.md:70`. The parent review says TSUKUROI-F1-MEM-01 is "inherited ... whose historical values were not recalled as current" at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/evidence/fleet-r1-interactive/parent-review.md:29`. The packet's capture is dated 2026-10-15 at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:79`, seven days before this round, and box 2 gives no date. The committed fleet copy and the adjacency note do treat the packet as the live route ADJ-04 packet, so the lane's records disagree with each other. [obs]
- "Delivery is evidenced separately by the committed fleet report". The fleet report at commit 8c1a763 (integrator commit, 2026-10-19 20:07:14 -0300) says "Ledger state: `prepared`; becomes `reported` on the integrator's commit of this file" (`git -C /home/vgpnk/Projects/shokunin show 8c1a763:.ufo/reports/round-1/tsukuroi.md`, lines 102-103). It also cites mori's committed receipt (same file, line 150). That supports the state "reported" and nothing further. The lane's machine ledger still reads ADJ-04 `prepared` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.json`, route ADJ-04). The lane's report copy says "prepared for integrator routing, not independently accepted" (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/reports/round-1/tsukuroi.md:100`). Box 2 names no file and no commit for the fleet report, so a reader cannot resolve the pointer from inside the lane. [obs]
- What does hold. Section 3 of the adjacency note contains a capture observation (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:77-105`) and a request to mori (same file, lines 107-113). The round-3 end-to-end task is real: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/host-health-report-r3.md:13-14` calls it "the lane's end-to-end SHONEN task, executed start-to-finish in one sitting", and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/LOG.md:105-106` logs it. [obs]

### 2. High: the one-phrase edit is not recorded in the round-25 record and only clears a checker rule

- The checker counts any token that contains a slash as a path and reports it absent when nothing matches. Its docstring says a slash token "names nothing in the repository is still a path and is reported as absent" (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-self-assessment.py:241-250`). The declared grammar says the same thing: "A token is a path when it contains `/`" (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:809`). [obs]
- The wave-1 specification said the token `observation/request` is prose and must not be reported (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ExecSelfAssessTool.md:113`). Wave-1 outputs still flagged it at the base commit and at the declaration commit (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ExecSelfAssessTool/c1-base-b9046016.json:233,242` and `.../c1-decl-0cd9b28.json:233,242`). So the flag comes from the grammar, and no fact in box 2 was wrong. [obs]
- Nothing in the round-25 record says the wording changed. The exact new phrase appears once in the measured tree, at SHONEN.md:8. The round-25 SCORECARD section (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:784-861`) is silent on it. The round-25 LOG entry (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/LOG.md:1207-1215`) is silent. The round-25 lesson (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-25.md`) is silent; its only SHONEN mention, line 46, is a generic description of C1. The commit 5e7c04e has a subject line and no body. [obs]
- Effect on the count. Base check K21 is one of the 13 mismatches. At the measured revision K21 passes, and the wording is the only SHONEN input that changed. So one of the 13 flips is a wording change, not a repaired fact. [obs]
- Meaning. The packet does carry both an observation and a request, so "observation and request" describes its content accurately and no fact is added or removed. [inf] The lane's category label "observation/request" is used in 9 files of the measured tree, for example `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:29` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-1.md:7`. The box is the only place that uses the new form. [obs]
- Verdict on the edit: meaning-preserving in content, but not honest by omission until the round record says the wording changed, why, and that the K21 flip is a grammar effect.

### 3. Medium-high: box 4 ("No cross-domain bleed (PROVINCE.md still accurate)") is not supported by its pointers

- The cited "round-12 refinement" at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:85-90` is superseded. `PROVINCE.md:92-96` names the round-13 correction as the active refinement, and `PROVINCE.md:98-106` adds a round-14 erratum. Box 4 cites the superseded text as current evidence. [obs]
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-12/resumed/OverlapHostR.md` is a round-12 scan by a lane-dispatched leaf connector (its header, lines 1-9). It covers round-12 probes and does not examine PROVINCE.md at 5e7c04ec. [obs]
- The lane's own report copy says "contested ownership remains unresolved" (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/reports/round-1/tsukuroi.md:102`). Box 4 drops that clause. [obs]
- Unexamined boundary. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:125` (row OUT-005) gives mori "kill/OOM catalog-ID and signal-11 coredump classification". The lane's own table of kill-event classes at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:1078-1102` classifies kernel OOM and SIGKILL events. [inf] This may be contested ownership. Whether it is bleed is [unk]. None of box 4's pointers addresses it. [obs]

### 4. Medium: box 3 ("Instructions executable by an agent without oral context") rests on assertion, not on an executed test at 5e7c04ec

- Adjacency note sections 4 and 5 (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/adjacency-handoffs-fleet-r1.md:136-186`) contain a command block and numbered steps. The note disclaims any replay claim (same file, lines 183-185). Section 4 says "Replace the revision with the actual recorded implementation commit" (line 138) and does not say where that commit is recorded. [obs]
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-decision-r12.md:7-11` is marked "Superseded after outside rejection". Box 3 cites it as evidence for executable instructions. [obs]
- The one executability test, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/executor-test-sufficiency.md:17-19`, ran on a SKILL.md revision of 444 lines. The SKILL.md at 5e7c04ec has 2355 lines (`wc -l`). Box 3 itself says the whole-SKILL retest "remains unverified" (box text; LOG.md:153-154). So no executed evidence covers the current document. [obs]

### 5. Medium: box 1 ("SKILL.md contains real decision tables, error patterns, checklists, cited sources") holds, with two caveats

- Present in the tree: the verdict table (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:32-35`), the health-verdict decision table (`SKILL.md:38`), the update-safety checklist (`SKILL.md:90`), the error patterns E1 and E2 (`SKILL.md:2028-2031`) and the round-12 root-metadata section (`SKILL.md:1676`). [obs]
- The phrase "error classes" is not a SKILL heading. SKILL.md uses "Error patterns". This is wording drift only. [obs]
- Cited sources: SKILL.md cites 39 distinct `corpus/knowledge` notes. 37 resolve inside the lane. The other two carry explicit sibling prefixes (`SKILL.md:1504`, `tameshi-shokunin/...`; `SKILL.md:2309` and `:2313`, `mori-shokunin@4f05dd5a:...`). [obs]
- Caveat one: the round-12 DAC note that box 1 cites is superseded in part. `SKILL.md:1717-1719` and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/root-dac-correction-r13.md:38-42` supersede its B2 unit-side reading, its ProtectSystem exclusivity and its SC1/SC2 attribution. They do not touch the root-metadata observation. Box 1 does not say any of this. [obs]

### 6. Low: a LOG pointer names a SCORECARD section that does not exist at 5e7c04ec

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/LOG.md:1215` says the measured outcome is in "SCORECARD.md section 'Round 25 measured outcome'". The tree contains no such heading (`grep -n "Round 25 measured" SCORECARD.md` returns nothing, exit 1). [obs]

### 7. Low: the capabilities row (check K17) shows the same rewording pattern, with one genuine fix

- At the base commit, the host-census-gate row flagged "HEALTHY/DEGRADED/BLOCKED" and a bare "after.md" as absent paths, and it stated 80 cases against the selftest's 97. At 5e7c04ec the tokens are reworded ("HEALTHY, DEGRADED or BLOCKED") and the count is 97. The count correction is a real repair. The token rewording is the same kind of change as finding 2. [obs]

## Residual risk

- A reader who takes "0 of 23" as a calibration result would overstate it, because one flip is a wording change. [inf]
- Box 2 will mislead until "current" carries a date and the fleet report is named by path and commit. [inf]

## Verification gaps

- I did not open the mori receipt commit 1f07f1d or the live host. The delivery reading rests on the fleet copy at 8c1a763 as quoted above. [unk]
- I did not run the section 4 counting command in the adjacency note. [unk]
- I searched the exact new phrase across the tree and searched the round-25 SCORECARD, LOG and lesson. I did not search every wave-1 file for a paraphrase of the wording change. [unk]
- The checker runs used sandbox commits with trees identical to the measured and base revisions, so their commit identifiers differ from the lane's. The checker reads tree content, so the results apply to the lane's trees. [inf]

Scope: read=the lane SHONEN.md, PROTOCOL.md seed (lines 424-453), SCORECARD.md round-25 sections and the tool's grammar, LOG.md round-25 entry, round-25 lesson, adjacency handoffs note and JSON, round-1 report copies (lane and fleet commit 8c1a763), parent review, round-12 and round-13 DAC notes, PROVINCE.md, SKILL.md citations and sections, executor-test note, host-health report, OverlapHostR.md, wave-1 spec and outputs; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RevShonen.md, /fast/scratch/hyaku/tsukuroi-r25/w2/RevShonen/ (measured-tree sandbox, base-sandbox sandbox, check outputs and cite list); executed=git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff b9046016..5e7c04ec -- SHONEN.md, git show of SHONEN.md at both revisions, git archive of 5e7c04ec and b9046016 piped to tar into sandboxes, git init/add/commit inside sandboxes only, python3 tools/check-self-assessment.py --revision HEAD --repo <sandbox> (measured-commit tool, run against the rev tree and the base tree), read-only git log/show/cat-file at /home/vgpnk/Projects/shokunin for commit 8c1a763, read-only python checks of SHONEN.md, PROTOCOL.md and the adjacency JSON, grep and wc counts over the sandbox, mv of my own scratch files within /fast/scratch/hyaku/tsukuroi-r25/w2/RevShonen/
Model: anthropic/claude-haiku-5-5
Installs: none
