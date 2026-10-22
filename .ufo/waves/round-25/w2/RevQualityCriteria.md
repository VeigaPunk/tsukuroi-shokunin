# RevQualityCriteria: QUALITY 57, 58, 59 and the R25 correction to 54 and 55

Verdict: partly holds. Each of criteria 57, 58 and 59 cites a lesson row or section that exists, the numbering is unique (1 to 59, no gaps), and the label correction matches `corpus/lessons/round-24.md`. But criterion 57's refusal sentence is contradicted by its own base measurement, criterion 58 adds prose scope to a failure that already happened under prose scope and names no control, and criterion 59's clone clause does not reach the clone that produced its failing example.

Revision reviewed: committed `5e7c04ecb02735491456de2b8bc44550d0db4609`, with `b9046016831237cd04d38da11ba76e50d5380c53` as the comparison base. I read committed bytes from `git archive` sandboxes at `/fast/scratch/hyaku/tsukuroi-r25/w2/RevQualityCriteria/rev-5e7c04ec` and `rev-b9046016`. The lane working tree matched the sandbox byte for byte for `corpus/QUALITY.md`, `corpus/lessons/round-24.md` and `corpus/lessons/round-25.md` (`cmp`). No `lsp` device is mounted for this seat; QUALITY.md is Markdown and the checker is one Python file, so I used literal reads and git plumbing.

## Findings, by severity

### 1. [High] Criterion 57 promises a refusal for a revision without the tool, but its own base run is not a refusal. [obs]
- Criterion text, `corpus/QUALITY.md:116`: "a revision without the tool is a refusal, not a pass."
- The tool is absent at the base. `git ls-tree --name-only b9046016... tools/check-self-assessment.py` returns no entries. The file first appears in commit `5e7c04e` (one commit in `git log`).
- The base run still produced a result. `.ufo/waves/round-25/measure/c1-b9046016.json` lines 1 to 5 read `"status": "FAIL"` and `"mismatches": 13`, which is exit 1.
- The checker's documented exit-2 cases (`tools/check-self-assessment.py` lines 15 to 19) include no tool-presence test. `evaluate()` reads only SCORECARD.md, SHONEN.md, PROVINCE.md, SKILL.md, `corpus/README.md` and the census script (lines 325 to 330).
- The round-24 tool did test itself. `SCORECARD.md` line 762 at `5e7c04e` says "at `f169b3ba` it is absent and the command exits 2." Round 25 kept the sentence without the behavior.
- Repair: add a self-presence test at the named revision with a fixture that fails when the file is absent, or delete the sentence.

### 2. [High] Criterion 58's failing example happened under a written prohibition, and criterion 58 adds no control. [obs]
- The round-24 lesson says ExecSymlinkMountProbe "ran privileged scratch writes and `mkinitcpio -g` despite the context forbidding image builds" (`corpus/lessons/round-24.md:90`).
- The host journal confirms the commands. `journalctl -q _COMM=sudo --since "2026-10-22 00:00"` runs without sudo. It shows `/usr/bin/unshare -m --propagation private` at 05:51:23, `/usr/local/bin/mkinitcpio -k 7.2.11-arch1-1 -g .../fresh-initramfs.img --nopost` at 05:53:15, and four `/usr/bin/python3 -` between 05:53:29 and 05:53:36. All carry PWD `/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe`.
- Criterion 58 (`corpus/QUALITY.md:117`) adds a prose allow-list. It names no check, selftest, fixture or journal audit. Criterion 47 (`corpus/QUALITY.md:94`) already says "Prompt scope is not runtime prevention"; criterion 58 neither cites it nor adds a control.
- The journal is readable without sudo, as this seat showed. A per-wave audit by PWD is cheap. Criterion 58 should require one and name a fixture that a synthetic unlisted line must fail.

### 3. [Medium] Criterion 58's allow-list has no target scope. [obs]
- Landed text (`corpus/QUALITY.md:117`) names `sudo -n cat`, `sudo -n stat`, `sudo -n ls` and `sudo -n journalctl` with read options. It does not limit the targets of `cat` or `stat`, so `sudo -n cat` on any root-readable file falls inside the text.
- The seat proposal in `.ufo/waves/round-25/w1/SentinelCapture.md:13` required "argument and option forms, and target-path scopes" and an argv-and-target comparison before execution. The landed criterion dropped both.
- `.ufo/waves/round-25/w1/DraftRoutedRepairs.md:27` noticed that the placeholders bound the command but not the target, and proposed no change.

### 4. [Medium-Low] The wave-2 context does not name the stdin-interpreter class that criterion 58 lists. [obs]
- Criterion 58 names "interpreters on stdin". The failing example ran `python3 -` four times.
- A grep of `.ufo/waves/round-25/w2-spec.json` and `w2-dispatch.json` for "stdin" or "interpreter" returns no matches. Both say "Everything else under sudo is forbidden. No item this wave needs sudo." The host-actions clause says "never boot, mount, unshare or rebuild an image", but not as a sudo class.
- The wave-1 context names "interpreters or shells on stdin" and says "report it instead" (`w1-spec.json` line 5).
- Read literally, the wave-2 text still forbids these through the general "everything else" clause. The named class is absent, and it is the class that failed.

### 5. [Medium] Criterion 59's clone clause does not reach the clone that produced its failing example. [obs]
- Criterion 59 (`corpus/QUALITY.md:118`): "every clone the L1 hands a seat has its push URL disabled."
- DraftSkillTable made its own clone. Its Scope trailer at `5e7c04e` (`.ufo/waves/round-25/w1/DraftSkillTable.md:105`) reads "git clone, git add/commit/push in the scratch clone only." Its dispatch item in `w1-spec.json` (lines 88 to 91) gives no clone instruction, and it was a scribe, not an executor.
- So the first clause does not cover the failing path. The second clause does: "seats build other fixtures with `git init` and no lane remote." That is a prompt rule. The wave-1 context forbade git writes "in the lane repo" (`w1-spec.json` line 5), and the lesson quotes exactly that wording.
- Wave 2 now forbids "`git clone` the lane and push back" (`w2-spec.json` line 5). That closes the gap in prose for wave 2 only.

### 6. [Medium] The push-URL control is confirmed for three executor clones. The failing clone no longer exists. [obs] [unk]
- ExecCensusW04, ExecMemPressureTool and ExecSelfAssessTool each have origin set to the lane path and `remote.origin.pushurl` set to `/nonexistent/no-push-to-lane` (`git config --get` in each scratch clone).
- `/fast/scratch/hyaku/tsukuroi-r25/DraftSkillTable/clonetest/repo` returns "No such file or directory" (exit 128). The parent directory last changed at 07:34 -03. No round-25 LOG, SCORECARD, lesson or report records its removal.
- [unk] Whether that clone had a push URL when the seat pushed.

### 7. [Medium] Criterion 59's detection evidence is not in the lane. The push itself is confirmed. [obs]
- The lesson (`corpus/lessons/round-25.md:60`) says `jj-lane.sh state` printed `ahead=4` before the repair and `ahead=0` after. No file under `.ufo/waves/round-25` contains an `ahead=` value; grep finds none.
- The script is outside the lane at `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh`. Its state branch computes ahead as `refs/remotes/origin/<branch>..refs/heads/<branch>` (lines 160 to 182; the count is at line 176). Criterion 59 cites it by bare name.
- The event itself checks out. Commits d2e9a7a, 9e9a97d, d70cbd0 and d5e6481 were pushed into local master between 07:31:03 and 07:32:51 -03, and the reflog records "round-25 L1: undo seat push of 4 scratch commits (DraftSkillTable)" at 07:35:48. `git merge-base --is-ancestor d5e64812 5e7c04ec` exits 1. `git rev-list --count origin/master..master` returns 0 now.

### 8. [Medium] Criterion 57's failing-example wording is wrong in two places. [obs] [inf]
- "still current at `b9046016`": the same file says the round-11 table is superseded. `SCORECARD.md` lines 295 to 297 at `b9046016` read "the later fleet-r1 corrections supersede the historical terminal table." The table sits under the heading at line 39 (`## Axes — final self-assessment (landed round 11 ...)`), with rows at lines 45 to 52 and the freshness row at line 50. [inf] The "historical terminal table" is this table.
- "from which round 24 read freshness 8": this link is inferred. The round-24 declaration heading is at `SCORECARD.md:740` at both revisions. Its C2 row at `5e7c04e` line 749 reads "freshness 8 → 8 (tied lowest)" but cites no lines 45 to 52. The round-25 lesson cites spot-check line 98 for the link, but that line says only "Re-read SCORECARD ordinals before declaring" (`corpus/lessons/round-24-verifier-spotcheck.md:98`).
- What holds: check K04 (freshness) flags the base value. `c1-b9046016.json` lines 37 to 46 give stated 8 at line 50 and observed 9 from `SCORECARD.md:772`, which reads "freshness (actual 9 → 9)."

### 9. [Low-Medium] Criterion 57's stated test is not what the checker does for axis scores. [obs] [inf]
- Criterion 57 says an axis score "is admissible only when its counting command ... reproduces it." Checks K01 to K06 instead match each score to the after-value of the latest free-text transition written as `<axis> N → M` outside the table (`check-self-assessment.py` lines 385 to 411). Freshness and calibration have no counting command.
- The criterion should name two tests: counts reproduced by commands, and axis scores matched to the latest transition record. [inf] A transition written in another form would be invisible to that regex.

### 10. [Low] Criterion 58 paraphrases its failing command. [obs]
- `corpus/QUALITY.md:117` gives "`sudo mkinitcpio -g`." The cited line (`round-24-verifier-spotcheck.md:69`) gives `sudo /usr/local/bin/mkinitcpio -k 7.2.11-arch1-1 -g <scratch> --nopost`, and the journal records the full argv. Quote the exact command.

### 11. [Low] Criteria 58 and 59 name no fail-capable control. [obs]
- Criteria 54, 55 and 56 each name a selftest case or a synthetic fixture (`corpus/QUALITY.md:107` to `109`). Criterion 57 names a check command but not its selftest cases. The lesson says the selftest has stale-ordinal and stale-count cases, which matches `check-self-assessment.py` lines 745 to 750. I did not run that selftest.

### 12. [Low] DraftSkillTable's report cites the undone commits as measured revisions. [obs]
- `.ufo/waves/round-25/w1/DraftSkillTable.md` lines 13 to 15 cite `9e9a97daf9137127683830d570e2bcc367462e9a` and `d70cbd06d3c0f4cede3d2984ae376f45781bc167` as gate runs in a scratch clone of the lane. The reflog shows both were pushed into the lane's master and then undone. The lesson does not mention the report's revisions.

### 13. [Holds] The R25 label correction matches `corpus/lessons/round-24.md`. [obs]
- The correction's two wrong labels are on the criterion headings: `R24-SUMMARY-RECALL` at `corpus/QUALITY.md:107` (criterion 54) and `R24-PREMISE-STALE` at line 108 (criterion 55).
- The Mistake IDs exist in `corpus/lessons/round-24.md`: `R24-STALE-PREMISE` at line 45, marked "QUALITY 55", and `R24-KEY-RECOLLECTION` at line 47, marked "QUALITY 54".
- Each criterion's own pointer already uses the right ID. Line 107 says "Lesson: `corpus/lessons/round-24.md` Mistakes R24-KEY-RECOLLECTION"; line 108 says "Lesson: `corpus/lessons/round-24.md` Mistakes R24-STALE-PREMISE."
- The spot-check's item 6 (`round-24-verifier-spotcheck.md:103`) names the drift and both correct IDs. Its line 94 already uses R24-KEY-RECOLLECTION.
- The criteria text is unchanged. `git diff b9046016... 5e7c04e... -- corpus/QUALITY.md` adds seven lines at the end and changes no existing line.
- One description error: `corpus/lessons/round-25.md:51` says "Appended correction after QUALITY 56." The correction sits at `corpus/QUALITY.md:120`, after criterion 59. [obs]

### 14. [Holds] Numbering is unique. [obs]
- A Python count over the committed `corpus/QUALITY.md` at `5e7c04e` finds 59 numbered criteria, each once, in order, from 1 to 59 with no gaps. The unnumbered clarification and correction blocks do not collide with any number.

### 15. [Holds, with a note] Lesson pointers resolve. [obs]
- Criterion 57 points to `corpus/lessons/round-25.md` Mistakes, row R25-STALE-AXES-TABLE (line 59).
- Criterion 58 points to "Routed defects", which is the heading "Routed defects from the round-24 spot-check" (line 42). Its row 2 at line 47 says "QUALITY 58." The criterion has no Mistake ID, unlike 57 and 59.
- Criterion 59 points to row R25-SEAT-PUSH (line 60), which says "QUALITY 59."

### 16. [Holds for wave 1, with one unexplained sudo session] No round-25 seat shows sudo use in the wave window. [obs] [unk]
- The last sudo session in today's journal starts at 07:31:21 -03. It is `/usr/bin/journalctl --since '2026-10-21 00:00' _COMM=sudo` with PWD set to the fleet root. Nothing starts after it through my dump, which was taken after 08:47 -03. The wave-1 dispatch files were last written between 07:12 and 07:19 -03.
- No round-25 report mentions `_COMM=sudo` or that query; grep finds none. [unk] The invoker is not identified.
- Earlier sudo records have other origins. About 13,300 come from `/home/vgpnk/tmp`, mostly between 01:50 and 04:10 -03; 421 come from `/tmp`; round-24 paths (`tsuku24-*`) and lane-root `/boot` reads fall between 05:18 and 05:59. All of these predate round 25's declaration at 06:49 -03.

### 17. [Residual risk] Host sudo use outside the lanes is not governed by criteria 57 to 59. [obs]
- The account ran 14,092 sudo COMMAND records on 2026-10-22, most from non-lane directories. Criteria 57 to 59 constrain seats only.

## Verification gaps
- I did not run `check-self-assessment.py` or its selftest. I relied on the committed receipts and the checker source at `5e7c04e`. [unk]
- No `lsp` device was available to this seat.
- [unk] The `ahead=` values the lesson quotes, the DraftSkillTable clone's configuration and removal, and the 07:31:21 invoker.
- The round-24 C2 row at line 749 was checked at `5e7c04e` only.

## Suggested repairs (for the L1 to decide; I did not edit anything)
- Criterion 57: add a self-presence test at the named revision with a fixture, or delete "a revision without the tool is a refusal." Split the admissibility test into counts reproduced by commands and axis scores matched to the latest transition. Correct "still current" to "superseded at `b9046016` by SCORECARD.md lines 295 to 297."
- Criterion 58: state target-path scope and the argv comparison. Add the stdin-interpreter class to the wave-2 context. Add a per-wave sudo-journal audit by PWD, with a fixture.
- Criterion 59: extend the clone rule to seat-made clones (no lane remote). Receipt the `ahead` check, or move it inside the lane.

Scope: read=/fast/scratch/hyaku/tsukuroi-r25/w2/RevQualityCriteria/rev-5e7c04ec and rev-b9046016 (git archive extracts of both revisions); lane files corpus/QUALITY.md, corpus/lessons/round-24.md, round-25.md, round-24-verifier-spotcheck.md, SCORECARD.md at both revisions, tools/check-self-assessment.py at 5e7c04e, .ufo/waves/round-25 measure receipts, w1 and w2 specs, dispatch files and reports; scratch clone git config; scripts/hyaku/jj-lane.sh; git objects, refs and reflog; host sudo journal read without sudo; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RevQualityCriteria.md, /fast/scratch/hyaku/tsukuroi-r25/w2/RevQualityCriteria/ (sandboxes and a journal dump); executed=git archive piped to tar, git init in sandboxes only, git log, git ls-tree, git diff between two revisions (tree comparison), git cat-file, git merge-base --is-ancestor, git rev-list --count, git rev-parse, git reflog show, git config --get in scratch clones, cmp, ls -la, stat -c, test -f, journalctl --no-pager read-only without sudo, python3 counting and parsing over committed files and the journal dump; no sudo command, no lane write, no git write, no service or package action
Model: anthropic/claude-haiku-5-5 (from this session's workstation context; not checked against the serving endpoint)
Installs: none
