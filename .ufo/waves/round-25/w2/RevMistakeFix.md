# Round 25, wave 2: RevMistakeFix report

Verdict: partly holds. The fix for R25-STALE-AXES-TABLE can fail as claimed: the checker at 5e7c04ec exits 1 against b9046016 and exits 0 against 5e7c04ec. The four scratch commits of R25-SEAT-PUSH are not ancestors of master or origin/master, and no commit in the lane carries them. Two things do not hold as written: the row's cited section "SCORECARD.md Round 25 measured outcome" does not exist at 5e7c04ec, and two of the 13 mismatches at b9046016 are path-grammar artifacts rather than stale axes content.

Measured revision: 5e7c04ecb02735491456de2b8bc44550d0db4609 (master and origin/master both point at it). Base: b9046016831237cd04d38da11ba76e50d5380c53. Lesson rows: `corpus/lessons/round-25.md:59` (R25-STALE-AXES-TABLE) and `:60` (R25-SEAT-PUSH). The checker ran from a git-archive sandbox of 5e7c04ec with `--repo` pointing at the lane. Everything in the lane was read-only.

Checks use these labels: [obs] is an observation, [inf] is an inference, [unk] is an unknown.

## Part A: R25-STALE-AXES-TABLE

1. The row's evidence pointer does not resolve. [obs] (medium)
   The row says the mismatches at b9046016 are "listed in `SCORECARD.md` Round 25 measured outcome" (`corpus/lessons/round-25.md:59`). At 5e7c04ec, SCORECARD.md has "measured outcome" headings for Rounds 13 to 18 and 21 to 24 only (ten headings, at lines 320, 384, 442, 488, 511, 566, 652, 692, 724 and 765). It has none for Round 25. The Round 25 region (lines 784 to 862) holds the declaration, the refinements and the two new tables. `git grep -i "measured outcome" 5e7c04ec -- LOG.md SCORECARD.md corpus SHONEN.md SKILL.md PROVINCE.md` finds no Round 25 match. The 13-name list exists only in receipts. One is tracked: `.ufo/waves/round-25/w1/ExecSelfAssessTool/c1-base-b9046016.json` (status FAIL, mismatches 13, ids K02 K04 K06 K07 K08 K09 K10 K11 K12 K13 K15 K17 K21). The other is untracked in the lane working tree: `.ufo/waves/round-25/measure/c1-b9046016.json` (the same 13). Fix: repoint the row to the tracked receipt, or add the section to SCORECARD.md.

2. Two of the 13 mismatches come from the path grammar, not from stale content. [obs] + [inf] (medium-low, calibration)
   The checker's K21 (SHONEN box 2) reads the slash token `observation/request` as a missing path. Evidence: `SHONEN.md:8` at b9046016 contains "current sanitized observation/request TSUKUROI-F1-MEM-01". The checker says "SHONEN box 2 names 1 path(s) absent at the revision: observation/request".
   The checker's K17 (host-census-gate row) reads the verdict enum `HEALTHY/DEGRADED/BLOCKED` and the bare backticked name `after.md` as missing paths. Evidence: `SCORECARD.md:162` at b9046016. The checker says "host-census-gate row names 2 path(s) absent at the revision: HEALTHY/DEGRADED/BLOCKED, after.md".
   The fix rewrote both strings. `SCORECARD.md:853` at 5e7c04ec reads "HEALTHY, DEGRADED or BLOCKED", and `SHONEN.md:8` reads "observation and request".
   The other 11 mismatches are about the stale table. They are K02, K04 and K06 (axis scores), and K07 to K13 and K15 (depth, coverage and adjacency evidence). Mutant m3b (below) shows this split. When only the axes heading is broken, the checker reports exactly those 11, and neither K17 nor K21 appears. So the stale-table demonstration rests on 11 real mismatches. The headline "13 of 23" overstates the stale-table part by two.

3. A tracked receipt for the same b9046016 run disagrees with the current count. [obs] (low)
   `.ufo/waves/round-25/w1/DraftLessonMistakes/checker-red-before-b9046016.json` (tracked at 5e7c04ec) and `.ufo/waves/round-25/w1/DraftLessonMistakes.md:46` both record 12 mismatches, with K21 absent. The current checker records 13. The likely cause is the path-grammar refinement at `SCORECARD.md:809` (K21 is consistent with that refinement) [inf]. Nothing in the tracked tree marks the 12-count receipt as superseded.

4. The C1 receipts are not committed at the measured revision. [obs] (low)
   At 5e7c04ec the only tracked file under `.ufo/waves/round-25/measure/` is `census-before.txt`. The files `c1-b9046016.json`, `c1-5e7c04ec.json`, `c1-selftest.txt`, `exits.txt` and `registry-5e7c04ec...json` exist only in the lane working tree. The checker itself is in the revision, and my independent runs reproduce every C1 result (below). So the claim can be reproduced from git, but the cited receipts are not durable.

5. The old round-11 tables are still in the file under "final" headings. [obs] (low)
   `SCORECARD.md:39` is "## Axes — final self-assessment (landed round 11 ...)", with its table at lines 45 to 52. `SCORECARD.md:157` is "## Capabilities". The new section at lines 815 to 822 says it supersedes the round-11 table and that the old table stays as history. The checker reads only the last "## Axes — " heading, so the old table is never checked. A reader who opens the first table sees "final" and stale counts (24 notes, 1631 lines, coverage 8, freshness 8, adjacency 7).

What holds:

6. The checker can fail on the pre-fix revision. [obs] (holds)
   - `tools/check-self-assessment.py` at 5e7c04ec, run with `--revision b9046016... --repo <lane>`: exit 1, status FAIL, mismatches 13, checked 23. The 13 IDs match the list in item 1. Receipt: `.ufo/waves/round-25/w2/RevMistakeFix/c1-tool5e7c04e-on-b9046016.json`.
   - The same tool with `--revision 5e7c04ec... --repo <lane>`: exit 0, status PASS, mismatches 0, checked 23. Receipt: `.../w2/RevMistakeFix/c1-tool5e7c04e-on-5e7c04e.json`.
   - The tool blob is byte-identical at 5e7c04ec and in the lane working tree (`eb2778660fc8f295e768f7098048afbe2bfff57b`).
   - The selftest at 5e7c04ec (`--selftest`): exit 0, 7 of 7 cases PASS. The stale-ordinal case expects and gets exit 1 with K02. The stale-count case expects and gets exit 1 with K07. The missing-axes-table case gets exit 2. Receipt: `.../w2/RevMistakeFix/c1-tool5e7c04e-selftest.json`.
   - The row's b9046016 numbers match the checker's observed values: 46 notes; 2301 newline characters in SKILL.md; 259 pipe lines; 25 lesson files; 231 README lines; 97 census cases; ordinals 9, 9 and 8; PROVINCE Core, Frontier and Adjacent sections present; overlap table present. The old table's stated values also match the checker's stated values: 24 notes, 1631, 55, 0, 20, 80, coverage 8, freshness 8, adjacency 7, and the PROVINCE sections and overlap table absent.
   - I ran the census selftest in a b9046016 sandbox (the same step the checker's K13 runs). It printed "PASS (97 cases, 97 passed, 0 failed)", exit 0.

7. The new table can fail too (mutants at 5e7c04ec, scratch copies, each committed only inside the sandbox). [obs] (holds)
   - m1: depth score 8 changed to 7. Exit 1, mismatches [K01].
   - m5: depth note count 47 changed to 46. Exit 1, mismatches [K07].
   - m2: README line count 231 changed to 230. Exit 1, mismatches [K11].
   - m3: heading renamed to "current self-assessment (round 26)". Exit 0. This is expected, not a defect: the selector matches the "## Axes — " prefix and ignores the suffix.
   - m3b: heading dash changed to a colon. The checker falls back to the round-11 table. Exit 1, 11 mismatches [K02 K04 K06 K07 K08 K09 K10 K11 K12 K13 K15]. A lost heading fails loudly and does not pass silently.
   Receipt: `.../w2/RevMistakeFix/mutants-5e7c04e-axes.json`.

## Part B: R25-SEAT-PUSH

8. The four scratch commits are unreachable from master and origin/master, and no helper commit carries them. [obs] (holds)
   - `git merge-base --is-ancestor` exit codes (0 means ancestor, 1 means not): d2e9a7a1, 9e9a97da, d70cbd06 and d5e64812 each give 1 against master and against origin/master.
   - `git for-each-ref --contains` for each of the four: no ref tip contains any of them, including `refs/jj/keep/*` and `refs/remotes/*`.
   - Reflog of master (`git reflog show --date=iso master`): 07:31:03 push d2e9a7a; 07:32:42 push 9e9a97d; 07:32:51 push d70cbd0; 07:32:51 push d5e6481; 07:35:48 "round-25 L1: undo seat push of 4 scratch commits (DraftSkillTable)", which moves master to 0cd9b28. The next master entry is 08:34:41 "export from jj" to 5e7c04ec. The four full hashes appear in no reflog file except `logs/refs/heads/master`.
   - Descendant scan: I read all 337 commit objects in the lane's object store, including unreachable ones. Apart from the four themselves, no commit descends from any of them. Their only children are each other.
   - jj operation log (jj 0.45.1, `--ignore-working-copy`, read-only): zero operations between 07:27:19 and 08:34:41. So jj never imported the scratch commits. Receipt: `.../w2/RevMistakeFix/jj-op-window-0720-0834.txt`. The six operations at 07:27:19 are all before the scratch pushes; they include the push of master to origin and the move of the master bookmark to 0cd9b28.
   - origin/master reflog: updates only at 07:27:21 (0cd9b28) and 08:34:44 (5e7c04ec), both "update by push". No scratch commit appears.
   - `git ls-remote origin`: 12 refs. `refs/heads/master` is 5e7c04ecb02735491456de2b8bc44550d0db4609, and no advertised ref equals a scratch commit. So the remote was not touched by the scratch commits.
   - The row's details match the history. Commit times run from 07:30:58 to 07:32:51. Authors are `t <t@x>` on three commits and `r20 <r20@example.invalid>` on d5e64812. The tip is d5e64812.
   - [inf] The row's "ahead=4" matches the commit graph. origin/master sat at 0cd9b28 from 07:27:21, and four commits sat above it until 07:35:48. I did not run `jj-lane.sh`, so its actual output is [unk].
   Receipt: `.../w2/RevMistakeFix/seat-push-ancestry.txt`.

9. The lane still accepts pushes into master, so the row's fix is procedural only. [obs] + [inf] (medium, residual risk)
   - The lane's HEAD is detached: `git symbolic-ref -q HEAD` exits 1. `.git/config` has no `receive.*` keys, only `core.bare false` and the origin remote.
   - I reproduced the mechanism in a scratch sandbox. A non-bare repo with a detached HEAD accepted `git push origin HEAD:refs/heads/master` (exit 0). The same push into a repo whose HEAD is on master was refused with "refusing to update checked out branch" (exit 1). So the detached HEAD is why the pushes landed. [inf] Detached HEAD is typical of jj colocated repos.
   - The row's mitigation is a push URL of `/nonexistent/no-push-to-lane` in executor clones. In a depth-6 scan of `/fast/scratch/hyaku/tsukuroi-r25`, three clones have an origin remote: `ExecSelfAssessTool/repo`, `ExecMemPressureTool/repo` and `ExecCensusW04/repo`. Each shows that push URL. The other clones there have no origin remote. The directory `/fast/scratch/hyaku/tsukuroi-r25/DraftSkillTable` holds only `p_DraftSkillTable.txt` and no `.git`, so the push URL of the clone that pushed is [unk].
   - Nothing in the lane itself guards against a future push from any clone whose origin is the lane path. A pre-receive hook, or a rule that refuses updates to master, would be structural. The row does not mention one. I changed nothing; this is a recommendation for the L1.

10. Wording of the row. [obs] (info)
   The row's "07:30-07:32" matches the reflog (07:31:03 to 07:32:51) and the commit times (07:30:58 to 07:32:51). Its "compare-and-swap" wording cannot be checked from the reflog. The reflog shows one update to 0cd9b28 with the L1's message [inf].

## Residual risk and verification gaps

- The claim that every executor clone now has the no-push URL is checked only for the three clones with an origin under `/fast/scratch/hyaku/tsukuroi-r25`. Other clones are [unk].
- `refs/pull/1/merge` (df1dc3a...) is not in the local object store, so its ancestry is [unk]. [inf] It is very unlikely to contain the scratch commits: the reflog shows no push of a scratch commit to GitHub, and `ls-remote` lists no ref equal to one.
- The checker runs the census selftest for K13. I ran that selftest in a sandbox and read its output, but I did not audit the census script for host-touching commands.
- I did not run `jj-lane.sh`. The "ahead=4" statement is inferred from the commit graph.

## Receipts

Lane (this wave's seat directory):
- `.ufo/waves/round-25/w2/RevMistakeFix/c1-tool5e7c04e-on-b9046016.json`
- `.ufo/waves/round-25/w2/RevMistakeFix/c1-tool5e7c04e-on-5e7c04e.json`
- `.ufo/waves/round-25/w2/RevMistakeFix/c1-tool5e7c04e-selftest.json`
- `.ufo/waves/round-25/w2/RevMistakeFix/mutants-5e7c04e-axes.json`
- `.ufo/waves/round-25/w2/RevMistakeFix/jj-op-window-0720-0834.txt`
- `.ufo/waves/round-25/w2/RevMistakeFix/seat-push-ancestry.txt`

Scratch (sandboxes, not in the lane): `/fast/scratch/hyaku/tsukuroi-r25/w2/RevMistakeFix/` holds `tool-5e7c04e`, `tree-b9046016`, the mutant copies `m1-depth-score-7`, `m2-readme-230`, `m5-depth-notes-46`, `m3-new-heading-renamed`, `m3b-new-heading-colon`, and `push-mech/`.

Scope: read=lesson rows corpus/lessons/round-25.md:59-60; SCORECARD.md at 5e7c04ec and in the b9046016 tree; tools/check-self-assessment.py at 5e7c04ec; SHONEN.md; tracked wave-1 receipts under .ufo/waves/round-25/w1; .ufo/waves/round-25/measure/ in the lane working tree; lane git metadata (reflogs, refs, object store, .git/config, HEAD); jj operation log (read-only); GitHub refs through ls-remote; remote URLs of scratch clones; scratch sandboxes; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RevMistakeFix.md; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RevMistakeFix/ (six receipt files listed above); /fast/scratch/hyaku/tsukuroi-r25/w2/RevMistakeFix/ (sandboxes and mutant copies); executed=git archive, tar -x and git init in scratch; python3 tools/check-self-assessment.py (5e7c04ec tool; --revision b9046016 and 5e7c04ec; --selftest; six mutant runs); bash tools/tsukuroi-census.sh --selftest in a b9046016 sandbox; git show, git grep, git ls-tree, git hash-object (no -w), git rev-parse, git merge-base --is-ancestor, git for-each-ref --contains, git reflog show, git cat-file --batch-all-objects and --batch, git log, git symbolic-ref -q HEAD, git config --show-origin --get-regexp, git ls-remote origin; jj --version and jj --ignore-working-copy op log (read-only); find and git remote get-url --push origin in scratch clones; scratch push test (git init, clone, push).
Model: anthropic/claude-haiku-5-5
Installs: none
