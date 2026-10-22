# CritClaimFraming — round 30, wave 1 (framing and sizing attack on the round-30 declaration)

Partly holds: the axis placement (C1 on depth, C2 on operability) and the separability statement mostly survive, but C1's counter can be satisfied by a trivial baseline (10 of 10, exit 0, with no btrfs knowledge at all); the "surface the lane has not covered" premise is partly false; C2's before-value 17 of 30 is not on the declared 33-pair set; and four universal clauses are not enumerated by their counting commands.

Revisions: the declaration is at `SCORECARD.md:1140-1152` (commit 8fb2cef0, tip 8976ca92); the claim base is fbfec6bd; the frozen counter sha256 is `1bf7ee14…c079`.

## Findings

1. **The 0-hit premise holds for `Global reserve`, `unallocated` and balance `usage`, but fails for the allocation sysfs directory and for DUP. Verdict: partly holds.**
   - [obs] At fbfec6bd, `git grep -c -F` over `SKILL.md corpus/ PROVINCE.md` found these counts:
     - 0 hits each for `Global reserve`, `global_rsv`, `unallocated` (also 0 case-insensitive) and `usage=`.
     - `balance`: 2 hits, both the word "unbalanced" (`corpus/lessons/round-29*.md`). Not btrfs content.
     - `ENOSPC`: 1 hit, `corpus/SOURCES.md:41`. This is the mkdir(2) errno row S035, not btrfs.
   - [obs] `allocation/`: 1 hit. `SKILL.md:2367` (row SH3) reads `ls /sys/fs/btrfs/<fsid>/allocation/{data,metadata,system}`. `corpus/knowledge/storage-health-r26.md:45` and `.json:131` cite the "sysfs allocation directories" as the host reading. So the allocation sysfs directory that D06 asks about is already in `SKILL.md`. The declaration's sentence at `SCORECARD.md:1142` ("the allocation sysfs files have 0 hits") is false for the directory and true only for its individual files.
   - [obs] D04 (metadata DUP on a single device) is already sourced:
     - S130 is registered with "lines 632-641 (DUP PROFILES ON A SINGLE DEVICE)" (`corpus/SOURCES.md:136`).
     - SH3 at `SKILL.md:2367` reads "`dup` metadata: repairable from the second copy, which an SSD may store as one physical copy."
     - This is the round-29 ruling's carry-over pattern (`round-29-verifier-spotcheck.md:82-86`: O05–O12 "copy corrections already argued").
   - [obs] The lane already holds the btrfs-progs v7.1 `ch-sysfs.rst` bytes in its committed evidence: `.ufo/waves/round-26/w1/SrcKernelSysfs/supporting-btrfs-progs-v7.1-ch-sysfs.rst`, sha256 `295b9265…3bc6`. They document:
     - `UUID/allocation/  Space allocation info` (line 10);
     - `global_rsv_reserved` and `global_rsv_size` (lines 145-153);
     - `bg_reclaim_threshold` (lines 165-169).
   - [obs] `corpus/lessons/round-26.md:52` records that fetch as "not registered … Flip: a row that needs the sysfs file list". So D02, D05 and D06 are new to `SKILL.md`/`corpus/`, but the lane has held their source bytes since round 26. The declaration's grep scope (`SKILL.md`, `corpus/knowledge/`, `corpus/SOURCES.md`) excludes that evidence, and the declaration does not mention it.
   - [inf] Of the ten rows, D01, D02, D03, D05 and D07 are new verifiable depth. D04 and D06 restate content already in `SKILL.md`. D08–D10 are point-in-time captures, which the lane's own axes table classes as "captures, not durable state" (`SCORECARD.md:1135`). So 5 to 7 of 10 are new depth: better than round 29's 4 of 12, but the counter cannot tell the classes apart (finding 2). The depth ordinal 8 → 8 is honestly declared.

2. **A trivial baseline reaches 10 of 10 under the frozen counter. Verdict: fails (the counter does not measure depth).**
   - [obs] Fixture "self": the only "mined source" is the counter's own source file. Each quote is taken from its `ROWS` comment (for example, "unallocated space vs chunk allocation"). D02 quotes the docstring "`Global reserve`, `unallocated` and the".
     - Every statement is the 12 filler words "alpha beta … mu".
     - The host value is `12`, captured from the docstring line "R3 `statement` has at least 12".
     - Each `SKILL.md` marker is just `| [R30-Dnn] S900 |`.
     - Command: `python3 counter.py --tree fx/self --base-sources base-SOURCES.md` gave exit 0 and `"verified": 10, "of": 10`, counter_sha256 `1bf7ee14…c079`.
     - Evidence: `.ufo/waves/round-30/w1/CritClaimFraming/out-self.txt` (sha256 `d5355be8…`), builder `build_trivial.py` (sha256 `571b9583…`), fixture JSON `fixture-self-btrfs-space-r30.json`.
   - [obs] Fixture "r26": seven rows quote the round-26 `ch-sysfs.rst` bytes, re-registered as a new `S9xx` row. The token matches are wrong:
     - D04's `dup` matches "*dedupe* ioctls";
     - D08's `metadata` matches "Show the metadata UUID";
     - D09's `data` matches "Show the reserved bytes for data."
     - Result: exit 0, 10 of 10 (`out-r26.txt`, sha256 `1dcf47f2…`).
   - [inf] Revision mode calls the same `measure()` (`tools/check-btrfs-space-r30.py`, `main` → `measure(read, base_sources)`), so the same bytes committed to a branch would also score 10. That is not run.
   - Gaps that let this through:
     - No rule binds `statement` to the quote or to the question.
     - R4 checks only the registry cells (new id, `mined`, `2026-10-22`, sha present). It does not check that the source is btrfs or external, or that the bytes were not already committed.
     - R7 is a case-insensitive substring match.
     - R8 accepts any integer on any line of any file under `.ufo/waves/round-30/`.
     - R9 needs only the id, source and value, so the "decision-table line" can carry no decision.
   - [obs] The 46 should-fail battery shapes (`tools/mutants-btrfs-space-r30.py`, F01–F46) are all format and provenance shapes. None is semantic: no unrelated source, no statement mismatch, no non-sysfs capture, no token inside another word. So "battery 0 of 46" shows format robustness, not depth.
   - Smallest safe correction (applied before any landing run):
     - R7 whole-word token match.
     - R3' the statement must contain the row's frozen token.
     - R4' the snapshot sha256 must not equal any blob reachable from fbfec6bd, and the source URL cell must be a btrfs-progs v7.1 or linux v7.2 path.
     - R8' one fixed capture path, whose sha256 is pinned by the counter, and the capture line must contain the row's frozen sysfs name (`allocation/metadata/…`, `allocation/data/…`, `allocation/global_rsv_size`).
     - A non-author per-row reviewer judgment (as round 29 had) for whether each statement answers its question.

3. **C1 has an unnamed adjacency overlap with mori. Verdict: fails as declared (no overlap row); fixable.**
   - [obs] The fleet root and the host root are the same btrfs filesystem. `findmnt -T /home/vgpnk/Projects/shokunin` gives `/home /dev/mapper/root[/@home] btrfs`, the same device as `/` (UUID 1d02a454…).
   - [obs] Mori owns disk runway on the fleet root (`../mori-shokunin/PROVINCE.md:26`, `SURFACE disk`). Mori's `SKILL.md:415` (mori HEAD `b039dd4f`) already holds a btrfs allocation rule: "**Never threshold the btrfs chunk percent.** Data-chunk fill reads **94.25%** while `df -P` Capacity … reads **10%**".
   - [obs] This lane's own split, at `PROVINCE.md:165-167` and the correction at `:176`: "free space as fleet runway is mori's, free space as an upgrade or boot precondition is this lane's". `storage-health-r26.md:9,106` excludes "disk-space runway (mori's surface)".
   - [inf] D01 (unallocated vs ENOSPC) and D09 (host data/unallocated) answer a runway question on mori's measured device. The declaration ties neither to an upgrade or boot precondition, and it names no adjacency row. Absorbing them risks harm on the adjacency axis (8, tied lowest), which blocks admission under AXES.md:34-35.
   - Smallest correction: one overlap row (PROVINCE adjacent table or the knowledge JSON) that cites mori `SKILL.md:415` and scopes D01/D09 to allocation semantics and ENOSPC triage, leaving runway thresholds to mori.

4. **C2 is mostly containment hardening rather than operability as AXES defines it. Verdict: partly holds.**
   - [obs] The before receipt (`.ufo/waves/round-30/measure/c2-before-8fb2cef0….jsonl`) has 17 leaking pairs:
     - path-wrapper, 10 pairs: all `control_rc 0 = channel_rc 0`. The only evidence is "canary log lines: N", meaning the tool found git through `PATH`.
     - user-files, 7 pairs: six are `exit code 1 differs from control 0` (adjacency-overlap, kernel-taint, memory-pressure, registry-coverage, storage-health, mutants-kernel-taint). The seventh is hooks firing at rc 0 (mutants-owed-statements-r29).
     - enclosing-repo: 0 of 10.
   - [inf] Only the six exit divergences are operability failures under AXES.md:12 ("a checklist item can be run and produces the stated outcome"). The ten path-wrapper pairs show no behaviour change: they measure hermeticity, which is the seat-containment concern of round 28.
   - [inf] Forcing `PATH=/usr/bin:/bin` overrides an operator's deliberate git choice. On this host it costs nothing today: `which -a git` gives only `/usr/bin/git` [obs]. It is still a tradeoff, not a pure gain.
   - [obs] The operator's real `~/.config/git/config` has no `hooksPath`, `gpgsign` or `excludesfile`, and `~/.gitconfig` is absent. So no before-leak is a present failure on this host; all are adversarial-environment failures.
   - [obs] The enclosing-repo channel 0 of 10 adds 11 pairs to the declared denominator of 33 that cannot move.

5. **17 of 30 is not an honest before-value for the declared 0 of 33. Verdict: fails (fixable by restating).**
   - [obs] The before run itself exited 2 (`"exit_code": 2` in the receipt end line). That is the probe's own could-not-evaluate state. Its set is 30 pairs, not 33. `check-self-assessment.py`'s three pairs were never measured (`"control_rc": 2, "harness_error": "control run failed: "`).
   - [obs] I ran `check-self-assessment --selftest` from a sandbox clone at 8976ca92 (target blob `3a626aa0…`, identical at 8fb2cef0) under the probe's channel construction (`sa_channels.sh`, sha256 `ecfcf41f…`):
     - control rc 0;
     - path-wrapper rc 0 with 312 wrapper log lines;
     - user-files rc 1 with 1 hook line.
   - [obs] So the honest before on the declared set is at least 19 of 33, with one pair (enclosing-repo) unmeasured. This was run outside the frozen probe, so it is not a receipt.
   - Was the harness error foreseeable? Yes [obs]:
     - `tools/check-self-assessment.py:1075-1078` at 8fb2cef0 returns `CANNOT_EVALUATE "not a git repository"` before the `--selftest` branch at `:1080`.
     - The probe runs every target from a `git archive` export (`export_tree`, `cmd = [sys.executable, os.path.join(tree, tool), …]`), which has no `.git`.
     - Round 29's declaration screened every target by an export control run (`SCORECARD.md:1107`). Round 30's sizing paragraph (`:1149`) has no such screen.
     - The empty control `HOME` is not the cause: the exit happens before any git call.
   - [inf] The after-value "`harness_errors` empty" therefore needs a fix that is not about any residual channel: reordering the `--selftest` dispatch in the calibration gate tool. This changes that tool's output from an export, which conflicts with the contract's "byte-identical otherwise" and is not named in the C2 claim text.
   - Smallest correction: restate the before as "17 of 30 measured (probe exit 2) plus 3 unmeasured pairs; out of the probe, 2 of those 3 leak". Name the dispatch reorder as a routed repair, not as part of C2. Alternatively, run that one target from a clone instead of an export.

6. **C1 and C2 are causally separable in their counting commands. Verdict: holds, with one coupling.**
   - [obs] The C1 counter reads only `corpus/knowledge/btrfs-space-r30.json`, `corpus/SOURCES.md`, `SKILL.md` and evidence files through `git show`. The probe reads no corpus file and runs only the eleven targets' `--selftest` or battery modes, which use private fixtures.
   - [inf] The coupling is that C2 edits `check-self-assessment.py`, the gate that later checks the round's axes table against the `SKILL.md` counts that C1 changes (table lines, notes). A C2 regression in that tool would show up as a no-harm gate result, not as a C1 or C2 count. This is a gate dependency, not a counting dependency, so separability under AXES.md:31 holds.

7. **Universal clauses the counting commands do not enumerate. Verdict: fails (4 clauses), against the round prompt §6 item 9 ("no universal clauses … unless the counting command enumerates the full set").**
   - (a) "a surface the lane has not covered" (`SCORECARD.md:1142`): no command enumerates it, and finding 1 falsifies it for the allocation directory and DUP.
   - (b) "quotes a `mined` source opened this round" (`:1146`): R4 checks registry cells only, so re-registered round-26 bytes and the counter's own source both pass (finding 2).
   - (c) "host … values from a read-only sysfs capture" (`:1146`): R8 does not check that the capture is sysfs or that the value is the named quantity (fixture value `12` from the docstring).
   - (d) "stop following the three residual git channels … per-user git files (config, hooks path, ignore, attributes) … an enclosing repository" (`:1147`):
     - The probe compares only exit codes and canary logs or fingerprints, never stdout. Following `ignore` or `attributes` with an unchanged exit is not counted.
     - The enclosing channel detects only writes into the canary.
     - It is blind for `mutants-owed-statements-r29*.py`, whose sandboxes sit under a hardcoded `/fast/scratch/hyaku/mut-owed-*` outside the canary (receipt `log_head`).
   - Lesser: "C1 changes only … C2 changes only the eleven target tools" (`:1151`) and the trailing "no package transaction, … balance or configuration action" (`:1153`) are attestations no command checks. They are acceptable as disclosures, but they are not counts.

## Impacted axes

- depth: the C1 count is gameable, and 5 to 7 of 10 rows are new.
- adjacency: an unnamed mori overlap.
- operability: 6 of 17 before-leaks are behavioural, and the path-wrapper fix carries a PATH tradeoff.
- calibration: the before-value is not on the declared set, and the premise is false.

The counter defects and the before restatement are fixable. The adjacency overlap and the path-wrapper-as-operability framing are tradeoffs for the judge or operator to rule on.

Scope: read=SCORECARD.md:1084-1153 at 8976ca92, AXES.md, .ufo/prompts/tsukuroi-round-30.md:335-351, corpus/lessons/round-29-verifier-spotcheck.md:60-109, tools/check-btrfs-space-r30.py, tools/mutants-btrfs-space-r30.py (shape list), tools/probe-git-env-residual-r30.py, measure/c2-before and c1-battery receipts, check-self-assessment.py:30-45,1066-1085, git grep at fbfec6bd over SKILL.md corpus/ PROVINCE.md, round-26 ch-sysfs.rst and lesson line 52, PROVINCE.md:160-176, mori-shokunin PROVINCE.md and SKILL.md:405-425, ~/.config/git/config (grep); wrote=.ufo/waves/round-30/w1/CritClaimFraming.md, .ufo/waves/round-30/w1/CritClaimFraming/{build_trivial.py,sa_channels.sh,out-self.txt,out-r26.txt,fixture-self-btrfs-space-r30.json,fixture-r26-btrfs-space-r30.json}, /fast/scratch/hyaku/tsukuroi-r30/CritClaimFraming/ (clone at 8976ca92, fixtures, sa/); executed=read-only git show/grep/ls-tree/rev-parse on the lane, git clone --no-local into scratch, python3 counter.py --tree fx/self and fx/r26 (exit 0, 10 of 10 each), sh sa_channels.sh (control 0, path-wrapper 0 with 312 log lines, user-files 1), findmnt -T, which -a git
Model: not exposed
Installs: none
