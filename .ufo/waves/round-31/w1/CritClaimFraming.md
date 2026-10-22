# CritClaimFraming — round 31 wave 1, claim-framing falsifier

Verdict: partly holds for C1 (most of the eight questions are new to the lane, but the "topic with 0 base hits" sentence is false at the topic level, two questions are partly held already, and the novelty argument is a coverage argument filed under depth); fails on framing for C2 (the measurement "leaking 0 of 33" is honest, but 22 of the 33 pairs are already at 0 at the base, the fix extends the round-30 rule to new inputs, and SCORECARD never states the before-value of 11).

Revision read: lane tip `8cff9e7cfb034b49c645d548801ac3185a827cb4`, claim base `2077e2fa4fa70ea79aa77b6d91f4acd35bc54897`. All reads were read-only `git grep`/`git show`/`jq` in the lane. No lane tool, counter or probe was executed, and no answer key was guessed or recovered.

## C1 — depth or coverage, and is the novelty sweep honest

1. [obs] The declaration's exact sweep is literally true. Each of the 14 frozen tokens (defragment, reflink, zero-log, log tree, --repair, autodefrag, defragmentation, commit=, periodic transaction commit, nodatacow, nodatasum, btrfs replace, replace start, fstrim) gives 0 under `git grep -i -F -c -e <token> 2077e2fa -- SKILL.md PROVINCE.md corpus`. I re-ran it and every token printed 0. Evidence: `SCORECARD.md:1209`, plus my run in this seat.

2. [obs] The topic-level sentence "a topic with 0 base hits" (`SCORECARD.md:1202`) does not hold once synonyms and neighbours are swept over the same scope at the base:
   - nocow: 10 hits
   - discard: 6
   - fsck: 5
   - device delete: 2
   - btrfs check: 2
   - shared extent: 1
   - discard=async: 1
   - checksum: 32
   - scrub: 86

   Run as: `for t in ...; git grep -i -F -c -e "$t" 2077e2fa -- SKILL.md PROVINCE.md corpus`. The fsck and "btrfs check" hits are false neighbours: the fsck hits are mkinitcpio HOOKS lines and the "btrfs check" hits are hook prose (for example `corpus/knowledge/journal-boot-plane.md:245` and `corpus/knowledge/boot-chain-r17.md:60`). The others are real neighbours; finding 3 lists them per question.

   [inf] A token set picked after looking at the base will always score 0 at that base. Q06 is keyed on `nodatacow`/`nodatasum`, not the held word `NOCOW`. Q08 is keyed on `fstrim`, not the held `discard=async`. Q07 is keyed on `btrfs replace`, not the held "device remove/delete". Rule R8 therefore shows that 14 strings are absent. It does not show that the topic is absent.

3. [obs] Which of Q01–Q08 the lane already held in other words at the base:
   - **Q01 (defragmenting shared extents): source held, knowledge not held.**
     - The registered, `mined` source S152 (`corpus/SOURCES.md:158` at base, btrfs-progs v7.1 `btrfs-filesystem.rst`) has a committed snapshot whose bytes already state the answer: `.ufo/waves/round-30/w1/ScribeSrcFsUsage/S152-btrfs-filesystem.rst:98-102`, "will break up" … "the reflinks of COW data" … "This may cause considerable increase of space usage depending on the broken up". S152's scope cell limits it to `filesystem usage`, so no corpus row states the defragment consequence.
     - Neighbour fact already admitted: `corpus/knowledge/btrfs-space-r30.md:28`, "Snapshots keep shared extents allocated; deleting files in the original frees nothing they still reference".
   - **Q02 (`rescue zero-log`): not held.** zero-log has 0 hits across the whole tree at the base. "log tree" appears only in kernel-source snapshots under `.ufo/waves/round-30/` (for example `ScribeSrcBlockRsv/S156-fs.h`).
   - **Q03 (`check --repair`): not held.** `--repair` has 2 whole-tree hits at the base, none in the corpus, and the "btrfs check"/fsck corpus hits are boot-hook context (finding 2).
   - **Q04 (`autodefrag`): not held in the corpus.** It appears only in round-30 fetched bytes (S157 snapshot `.ufo/waves/round-30/w1/ScribeSrcSubvol/S157-subvolume-intro.rst`, S160/S161 HTML).
   - **Q05 (`commit=`): not held.** The only neighbour is SH2's "writes changes back at transaction commit" (`corpus/knowledge/storage-health-r26.md:29`). It gives no interval, default or warning limit.
   - **Q06 (`nodatacow`): partly held.**
     - SH3 already states the checksum half: `SKILL.md:2367` reads "NOCOW file data (systemd journals) has no checksums and is not verified". The same point appears at `corpus/knowledge/storage-health-r26.md:43` ("File data with the NOCOW attribute has no checksums and scrub does not verify it"), `:112` and `:131` ("NOCOW file data is not protected by checksums (lines 29-31)", sourced from S139).
     - The lane also fetched `ch-mount-options.rst` in round 26, with the exact sha256 now pinned for Q04/Q05/Q06: `.ufo/waves/round-26/w2/RevRowSH3.md:39` gives `sha256 aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f`.
     - The corpus already cites that file: `corpus/knowledge/storage-health-r26.md:135` ("btrfs-progs v7.1 `ch-mount-options.rst`, max_inline").
     - [unk] Whether the sealed Q06 key groups go beyond "no checksums" (for example compression). The keys are sealed and I did not try to recover them.
   - **Q07 (`btrfs replace`): neighbour only.**
     - S128 (mined, round 26) has a committed snapshot documenting `device remove` of a `missing` device in degraded mode: `.ufo/waves/round-26/sources/S128.rst:44-76`.
     - `corpus/knowledge/storage-health-r26.md:132` says removing a device deletes its counter item.
     - The replace procedure and the target-size rule are not held.
   - **Q08 (trim mode): neighbour only.**
     - `corpus/knowledge/storage-health-r26.md:11` records that the host mounts with `discard=async` (a host fact, not a decision).
     - Round 26 also read `fstrim.timer` as enabled (`.ufo/waves/round-26/capture/capture.txt:150`, `.ufo/waves/round-26/w1/ScoutHostSurfaces.md:60`), outside the sweep scope.
     - No sync/async/periodic decision is held.

   Summary: Q02, Q03, Q04 and Q05 are new. Q06 is partly held (its checksum half). Q01 is held in registered source bytes but not as knowledge. Q07 and Q08 have neighbours only.

4. [obs] Rule R8 cannot fail at any revision. `BASE` is a constant (`tools/check-btrfs-repair-r31.py:56`), and `base_hits` greps only `BASE` (`:176-181`). The tokens are frozen and all 14 are 0, so R8 returns the same pass at every REV. The declaration's "The counter re-runs this sweep on every invocation (rule R8)" (`SCORECARD.md:1209`) adds no falsifying power after the declaration; R8 is a one-time screen.

5. [obs] The K2 "re-scoring held knowledge" control cannot detect held-in-other-words knowledge. Its eight rows fail on structural rules alone: R3 snapshot outside round-31, R5 source row exists at base, R5 frozen URL/sha256 missing, R6 tokens and R7 keys (`.ufo/waves/round-31/measure/controls/c1-K2-restate-r30.jsonl`, rows Q01–Q03 shown by `jq`).
   - [inf] K2 relabels round-30 space rows, which share no question with Q01–Q08. Its 0 is guaranteed by R3/R5 whatever the row content.
   - The held neighbours that matter are SH3 for Q06 and S152 for Q01. K2 never restates those.
   - A writer who restates SH3's "NOCOW → no checksums" with a `nodatacow` token, a round-31 pinned quote and a fresh S row is doing real fetch and registration work. The counter would score that row on R7 keys alone [unk, keys sealed].

6. [obs] The axis argument is a coverage argument filed under depth.
   - `AXES.md:11` defines depth as "Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources". `AXES.md:12` defines coverage as the "Fraction of the domain's real surfaces the skill governs", with PROVINCE listing every surface.
   - The addendum rule (`scripts/hyaku/lane-addendum.md:221-225`) says to name the axis by the surface changed. A coverage claim "names the surface it moves … and the command that would show it unmoved".
   - C1 justifies itself by topic novelty ("a topic with 0 base hits", `SCORECARD.md:1202`). Novelty of topic is the coverage test, not the depth test.
   - C1 also writes decision lines for actions that PROVINCE puts outside the province. Base `PROVINCE.md:167-168` says "filesystem repair, running a scrub, resetting an error counter and firmware updates remain operator-owned". Q02 (rescue zero-log), Q03 (check --repair) and Q07 (replace) are filesystem repair.
   - Yet C1 changes only `corpus/` and `SKILL.md` (`SCORECARD.md:1215`), touches no PROVINCE line, and claims depth 8 → 8.

   [inf] The depth label is defensible row by row. Q05 (default and warning limit) and Q07 (target size) carry thresholds, and every row is sourced. This is not the kaidoku-r29 misfit (re-scoring a held rule), because Q02–Q05 are genuinely new. The counter, though, measures provenance plus keyword presence, not depth; the declaration concedes this at `SCORECARD.md:1211` ("row truth and usefulness are judged by wave-2 row reviewers"). So the depth evidence sits entirely with wave 2.

7. [inf] Calibration: the topic-level novelty sentence repeats the round-30 pattern R30-DECLARATION-OVERCLAIM ("The declaration's novelty sentence was false", `corpus/lessons/round-30-verifier-spotcheck.md:174`). The overclaim is narrower this time. The 14-token sentence is true, while the topic sentence is not.

Impacted axes, C1: depth (claimed; evidence rests on wave-2 row review), coverage (touched but not claimed; PROVINCE boundary at `PROVINCE.md:167-168` not reconciled), calibration (topic-level novelty sentence).

Smallest safe correction, C1 (no target, rule or predicate changes):
- Append an erratum to the declaration; do not rewrite it in place. Replace "a topic with 0 base hits" with "14 frozen tokens with 0 base hits". List the held neighbours:
  - Q01: S152 snapshot lines 98-102 and `btrfs-space-r30.md:28`
  - Q06: SH3 at `SKILL.md:2367` and `storage-health-r26.md:43/112/131/135`, plus the round-26 fetch of `ch-mount-options.rst` at the Q04–Q06 pin
  - Q07: `S128.rst:44-76`
  - Q08: `storage-health-r26.md:11`
- State that the Q02, Q03 and Q07 decision lines are operator-only knowledge and that `PROVINCE.md:167-168` is unchanged, so no coverage move is claimed.
- Route to the wave-2 row reviewers:
  - The Q06 row must be judged on what it adds beyond SH3.
  - The Q01 row and entry should name S152 as prior held bytes. That note belongs in the knowledge note or lesson, because the row schema has fixed keys.

## C2 — is "leaking 0 of 33" honest, and is it a new surface

8. [obs] The before receipt has 11 of 33 leaking, and all 11 are `loader-env`. `child-contract` and `dotgit-pointer` are `leak: false` for all 11 tools. Evidence: `.ufo/waves/round-31/measure/c2-before-f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c.jsonl`, summary line `"pairs": 33, "leaking": 11`, receipt exit_code 1.
   - So 22 of the 33 pairs are already at their target under the do-nothing control (the base tools; see `SCORECARD.md:1213`).
   - The aggregate target passes the addendum rule "a target must be one a do-nothing control cannot reach" (`scripts/hyaku/lane-addendum.md:211-216`), because 11 ≠ 0.
   - However, the claim sentence names three behaviours (`SCORECARD.md:1203`). "Give every git child the system-scope contract" and "keep parity with their control run under a dropped `.git` pointer" are both already true at the base by measurement, so the do-nothing control reaches them.

9. [obs] SCORECARD never states the before-value. The declaration table's Before cell for C2 reads "measured at the declaration commit" (`SCORECARD.md:1203`). The number 11 and the all-loader-env split appear only in the receipt and the dispatch.
   - The after-value string is identical to round 30's C2 closure on the same eleven tools: "`leaking` 0 of 33, `harness_errors` [], exit 0" (`SCORECARD.md:1162`).
   - [inf] A reader of SCORECARD alone sees "0 of 33" twice in two consecutive rounds on the same tools. They will plausibly read round 31 as 33 pair fixes, or as a re-closure of the round-30 surface. The real delta is 11 pairs on one channel.

10. [obs] The fix re-applies the round-30 rule with two more prefixes.
    - At the tip, the round-30 contract already drops every `GIT_` name and sets the config contract in the targets. Examples: `tools/check-kernel-taint.py:253` and `tools/check-memory-pressure.py:107` (`if not key.startswith('GIT_')`), `tools/mutants-adjacency-overlap.py:19` and `tools/mutants-owed-statements-r29.py:36`.
    - The genuine control H2 is a one-line change of that same filter to `key.startswith(('GIT_', 'LD_', 'PYTHON'))`, and it zeroes the pair. Evidence: `.ufo/waves/round-31/measure/controls/c2/0001-H2-genuine-drop-LD_-and-PYTHON-names-in-the-git-chil.patch`, and `c2-H2.jsonl` with `"leaking": 0`.
    - The FIX CONTRACT in the assignment is exactly this prefix extension, followed by "the existing round-30 contract unchanged".
    - The declared surface, "the child-process environment the eleven tools build" (`SCORECARD.md:1203`), is the surface round 30's C2 changed on the same eleven tools (`SCORECARD.md:1147`, `1162`).
    - [inf] This matches the addendum's "Re-scoring a rule the lane already holds on new inputs" (`scripts/hyaku/lane-addendum.md:222`). The rule is the prefix scrub plus contract; the new inputs are the LD_ and PYTHON names and a `.git` pointer. That clause says such work is "quality work, never coverage or depth". It does not name operability, so the operability label is not literally barred. By the surface rule in the same paragraph, though, no new surface is moved.

11. [obs] No base leak changes an outcome. For every one of the 11 loader-env pairs, `control_rc` equals `channel_rc` (0 = 0) and `control_git_execs` equals `git_execs` (for example 933 = 933 for check-kernel-taint, 1263 = 1263 for check-adjacency-overlap). The evidence lists only "N descendant execs carry the injection path", with no stdout-digest mismatch. Command: `jq -c 'select(.channel=="loader-env") | {rc:[.control_rc,.channel_rc], ge:[.control_git_execs,.git_execs], ev:.evidence}'` over the before receipt.
    - `AXES.md:13` defines operability as runnable artifacts where "A checklist item can be run and produces the stated outcome". Under loader injection the base tools already produce their stated outcome.
    - What the 11 leaks measure is hermeticity: the injected path string reaches child processes. The round-30 spot-check already made this distinction ("hermeticity rather than outcome", `corpus/lessons/round-30-verifier-spotcheck.md:115`).
    - [inf] A hostile `PYTHONPATH` (a shadowing module) could change outcomes in `sys.executable` children. The probe's payload is harmless by design (an LD_PRELOAD symlink to libm, `tools/probe-git-child-env-r31.py:20-24`), so the probe measures whether the path is present, not what it does.

12. [obs] The probe docstring names "the two owed-statement batteries start git children that lack the contract and so read the system config scope (SentinelProbeHollow finding 6)" as an origin (`tools/probe-git-child-env-r31.py:9-11`). The separability line adds `tools/check-owed-statements-r29.py` to the C2 change set (`SCORECARD.md:1215`). Yet `child-contract` reads `leak: false` for both batteries at the base, and `tools/check-owed-statements-r29.py:154` already drops `GIT_` names.
    - [inf] That routed defect was either closed by the round-30 contract or is invisible to this channel. Either way, it contributes 0 to C2's measured delta.

Impacted axes, C2: operability (claimed; no outcome change at the base, so the probe cannot show operability movement), quality (where the work actually lands: a rule extension plus two regression guards), calibration (SCORECARD omits the before-value of 11 and the channel split, and reuses round 30's after-string on the same tools).

Smallest safe correction, C2 (no target, rule or predicate changes; "leaking 0 of 33" stays frozen):
- Append an erratum to the declaration stating the measured before-value: 11 of 33, all `loader-env`, with `child-contract` and `dotgit-pointer` at 0 of 22.
- In the closure, report "loader-env 11 → 0; child-contract and dotgit-pointer 0 → 0, held as regression guards, not fixes". Count 11 fixed pairs across the 12 changed files, never 33 fixes.
- Name the surface "the round-30 child-environment rule extended to the LD_ and PYTHON prefixes". Whether that counts as operability or quality is for the canonical judge. The tradeoff the judge must weigh is finding 11: no outcome change at the base.

## Distinguishing fixable defects from judge tradeoffs

- Fixable, by appending text: the C1 topic-novelty sentence (findings 2, 3, 7), the C2 missing before-value (finding 9), and C2's three-behaviour claim wording (finding 8).
- For the canonical judge: whether C1's new ground under a depth label, with no PROVINCE change, is a depth move or an undeclared coverage move (finding 6). Whether C2's outcome-neutral prefix extension of a held rule counts as operability or quality (findings 10, 11).
- Not a defect: the 14-token sweep is true as stated (finding 1). Q02–Q05 are genuinely new to the lane (finding 3), so C1 is not a re-score of held knowledge.

Scope: read=SCORECARD.md:1147-1217, tools/check-btrfs-repair-r31.py (full), tools/probe-git-child-env-r31.py:1-120, .ufo/waves/round-31/measure/{c1-*,c2-before-*,controls/c2/*,controls/c1-K2/K5}, corpus/lessons/round-30-verifier-spotcheck.md:85-117,174-191, base PROVINCE.md:75-100,154-177, base SKILL.md:2367, base corpus/knowledge/{storage-health-r26.md,btrfs-space-r30.md:28}, base corpus/SOURCES.md S120-S163, base .ufo/waves/round-26/{w2/RevRowSH3.md,sources/S128.rst,w1/*fstrim*}, base .ufo/waves/round-30/w1/ScribeSrcFsUsage/S152-btrfs-filesystem.rst:90-103, /home/vgpnk/Projects/shokunin/AXES.md:11-13, /home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:195-225; wrote=.ufo/waves/round-31/w1/CritClaimFraming.md; executed=read-only `git grep -i -F -c` synonym sweeps at 2077e2fa and 8cff9e7 (exit 0), `git show`/`git ls-tree` at 2077e2fa, `jq` over the round-31 receipts, `sha256sum` of the S152 snapshot (a0ce33f5…)
Model: not exposed
Installs: none
