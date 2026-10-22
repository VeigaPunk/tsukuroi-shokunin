# RerunC1: falsification of claim C1 (round 25, wave 2)

Verdict: partly holds. The C1 numbers reproduce exactly (base b9046016 exits 1 with 13 of 23 mismatches; measured 5e7c04ec exits 0 with 0 of 23; selftest passes 7 of 7), and every content input comes from git at the named revision. But "0 of 23" is weaker than the claim: three ordinal checks compare the table with the round-25 declaration's own sentences, a forged calibration pass succeeds, stale paths outside backticks are invisible, and the census check counts cases without checking PASS or the exit code.

## Findings that fail or are weaker than claimed (most severe first)

1. [obs] Medium. Three ordinal checks take their reference from declaration sentences, not from the move log, so a forged table passes K05.
   - Rule: `tools/check-self-assessment.py` lines 391-403 keep the last line, outside the current axes table, that matches `<axis> N → M`. A later line overrides every earlier one.
   - At the measured revision, the last matches are SCORECARD.md:793 ("depth 8 → 8 (tied lowest)", round-25 C2 row), SCORECARD.md:807 (the refinement illustration "`freshness (actual 9 → 9` is."), and SCORECARD.md:792 ("calibration 9 → 9", round-25 C1 row). At the base they are SCORECARD.md:759, 772 and 771, which are also claim text, not move-log rows.
   - Forged test: commit 698a384cb1fbc18585917452e995ab2d663faf9f (sandbox `/fast/scratch/hyaku/tsukuroi-r25/w2/RerunC1/att-forged`) changes the calibration score in the table from 9 to 7 and appends the line "calibration 8 → 7 (appended line)" at the end of SCORECARD.md. Result: exit 0, 0 mismatches, K05 matches. The earlier calibration lines at the measured revision (SCORECARD.md:732, 748, 771) all say 9 → 9, and the appended line overrides them.
   - Consequence: at both revisions, K01, K04 and K05 test the table against the lane's own claim text, not against a move-log row. The declaration calls these agreement checks. The calibration claim, though, is exactly the statement that the table agrees with the evidence, so the pass proves less than the claim implies.

2. [obs] Medium-low. K13 checks the census case count only.
   - Tool lines 145-152 run the census selftest and read the case count with the regex `\((\d+) cases`. They never read the census exit code or the PASS/FAIL word. K13 (lines 522-529) compares that count with the operability row.
   - Forged census: commit 0efa5b01b4fdb52e8fd9164fc4f6c7f5cc63aeaf (sandbox att-censusfail) prints "TSUKUROI_CENSUS_SELFTEST: FAIL (97 cases, 95 passed, 2 failed)" and exits 1. Result: exit 0, 0 mismatches, K13 matches.
   - The operability row (SCORECARD.md:830) claims "PASS (97 cases, 97 passed, 0 failed) with exit 0". The PASS and exit 0 parts are not measured.

3. [obs] Low. Capability rows K16-K19 read only backticked spans.
   - Tool lines 563-566 collect tokens only from backtick spans in each capability row.
   - Commit 2853f2943a8d5fc2fa3b471888ef534995df1a9a (att-barepath) adds the unbackticked path `.ufo/evidence/round-1-kaika/gone-report.md` to the host-census-gate row. Result: exit 0, 0 mismatches. The control commit 4d8f32fe1a881afa4358857cb0cb918a6754b802 (att-tickpath) puts the same path in backticks: K17 fails, exit 1.
   - Current state: my scan of the capability rows at the measured revision found no unbackticked path token, so there is no present false pass. The behavior is declared in the round-25 refinements, so it is disclosed.

4. [obs] Low. Part of the base count of 13 is a grammar artifact, and the repair includes two wording edits that no stale fact required.
   - Eleven of the 13 are real staleness: K02, K04, K06, K07, K08, K09, K10, K11, K12, K13, K15.
   - K17 mixes a real drift (80 cases stated, 97 printed) with the prose token "HEALTHY/DEGRADED/BLOCKED" read as a path. K21 is only the prose token "observation/request" (SHONEN.md line 7 at the base).
   - The measured revision now reads "HEALTHY, DEGRADED or BLOCKED" (SCORECARD.md:853) and "observation and request" (SHONEN.md:8). No false pass results, but "13 to 0" counts two wording edits as repairs.

5. [obs] Low. The receipts are not committed. `git status` lists `.ufo/waves/round-25/measure/c1-b9046016.json`, `c1-5e7c04ec.json`, `c1-selftest.txt`, `exits.txt` and `registry-5e7c04ecb02735491456de2b8bc44550d0db4609.json` as untracked. My byte comparisons therefore check on-disk copies, not files inside the measured commit.

## Checks that hold

6. [obs] Reproduction holds, run from the lane.
   - `python3 tools/check-self-assessment.py --revision b9046016831237cd04d38da11ba76e50d5380c53`: exit 1, checked 23, mismatches 13, status FAIL, ids K02, K04, K06, K07, K08, K09, K10, K11, K12, K13, K15, K17, K21. Byte-identical to `measure/c1-b9046016.json` (sha256 prefix ea80e12fb54f on both).
   - `--revision 5e7c04ecb02735491456de2b8bc44550d0db4609`: exit 0, checked 23, mismatches 0, PASS. Byte-identical to `measure/c1-5e7c04ec.json` (sha256 prefix d2982e099f61 on both).
   - `--selftest`: exit 0, 7 of 7 cases PASS. Stdout byte-identical to `measure/c1-selftest.txt` (sha256 prefix dd1a760c08c6).
   - The only machine-specific field, "repo", holds the lane path in both the rerun and the receipt. No other field varies.
   - `exits.txt` agrees: c1 b9046016 exit=1, c1 5e7c04ec exit=0, c1 selftest exit=0.
   - An unknown revision exits 2 (CANNOT_EVALUATE). `--revision HEAD` exits 0; lane HEAD is 5e7c04ecb027.
   - Rerun outputs: `.ufo/waves/round-25/w2/RerunC1/c1-b9046016-rerun.json`, `c1-5e7c04ec-rerun.json`, `selftest-rerun.json`.

7. [obs] Content inputs come from git at the named revision.
   - Source: the git helpers (lines 84-130) and `census_case_count` (lines 133-154, which runs git archive into a temporary directory) are the only input paths. The tool reads no worktree file except its own source.
   - Python audit-hook trace of both runs: the only lane file read outside `.git` is `tools/check-self-assessment.py`. Writes go only under /tmp and /dev/null. Twelve subprocesses: eleven git, one bash.
   - Dirty-tree sandbox at both revisions: the working tree had a changed SCORECARD (depth score 8 to 3 and an appended table), an appended SKILL.md (137 blank lines plus one table row), a new corpus/knowledge file, a deleted corpus/README.md, a reworded SHONEN box, an untracked root file, and a staged PROVINCE change. Output matched the lane reruns except the repo field: 13 mismatches at the base, 0 at the measured revision.
   - HEAD-moved control: commit 090c1d06644b9e6c3fef1255969489193cde4299 (att-headmoved, depth 8 to 3 at HEAD only). Run at 5e7c04ec: exit 0, 0 mismatches. Run at the new HEAD: exit 1, K01. The tool follows the named revision.
   - Environment: the census selftest prints 97 cases with the inherited environment, with hostile TSUKUROI_* path overrides (cgroup root, pressure, meminfo, vmstat, hostname, PCI, dmesg), and with an empty environment. K13 observed 97 under inherited and hostile environments.
   - strace (-f) of the tool at both revisions: content reads go only through git objects and git config. Host touches that are not content: Python reads /proc/sys/vm/overcommit_memory; GNU sort reads /sys/fs/cgroup cpu.max and cgroup.controllers (attributed by execve to /usr/bin/sort; the census pipeline is the likely caller [inf]); git reads ~/.config/git/config and ~/.gitconfig. No successful open of /proc/meminfo, /proc/pressure/memory, /proc/vmstat, the hostname or PCI sysfs files, the kernel log, /var/log or pacman state. The census selftest runs fixture stubs named journalctl, pacman and systemctl from a temporary directory, not host binaries, which supports its hermetic claim. Traces: `/fast/scratch/hyaku/tsukuroi-r25/w2/RerunC1/strace-5e7c04ec.txt` and `strace-b9046016.txt`.
   - No .gitattributes at 5e7c04ec, no /etc/gitattributes, and no textconv driver in the user config, so git show output is not altered by attributes or filters.
   - Restated: "reads only git at the revision" is true for every content input. The runtime, sort and git config touch host files, but no count uses them [inf].

8. [obs] An independent recount matches the tool for K07 to K11. Plain git and wc at 5e7c04ec: 47 .md files directly in corpus/knowledge, 2355 newline characters in SKILL.md, 297 SKILL.md lines starting with a pipe, 26 files under corpus/lessons, 231 lines in corpus/README.md. At b9046016: 46, 2301, 259, 25, 231. The "| ID | Finding" overlap table is present in PROVINCE.md at both revisions.

## Lane state and disclosures

9. [obs] The lane working tree held sibling-seat changes during my run: 30 entries at my first status check, 41 at my last. The C1 measurement reads only git, so these do not affect it.
10. [obs] Two of my `git status --porcelain` calls in the lane ran without `--no-optional-locks`. Git can refresh stat data in `.git/index` when it runs status; I wrote no content into the lane's git state. The last status check used `--no-optional-locks`.
11. [obs] Sandboxes were built with git archive and git init, plus an alternates file that points read-only at the lane's object store, with no remote. The alternates file is needed so the measured revision SHAs resolve inside a sandbox.
12. [unk] I did not establish which tool file produced the base receipt. The tool blob at 5e7c04ec (sha256 343367fb309e43449ee1be50f97c86b917240de7bb6b34b942fd67a163c6242f) is the file I ran, and the base receipt reproduces byte for byte with it.

## Residual risk and verification gaps

- The census count was checked at the two requested revisions and in the sandbox variants only.
- The controlled attacks are commits in sandboxes under `/fast/scratch/hyaku/tsukuroi-r25/w2/RerunC1/` (att-headmoved, att-forged, att-barepath, att-tickpath, att-censusfail). Each can be rerun with `python3 tools/check-self-assessment.py --revision <sha>` inside that sandbox, using the commit IDs in findings 1 to 3 and the HEAD-moved control.

## Advisory fixes (for the L1 to decide)

- Pin K01, K04 and K05 to move-log rows only, and skip the declaration and refinement sections. Or state in the claim that these three are agreement checks, not evidence checks.
- Make K13 require the census PASS word and exit 0.
- Read unbackticked path tokens in capability rows as well.
- Commit the receipts together with the measured commit.

Scope: read=SCORECARD.md and SHONEN.md in the lane and at git revisions b9046016 and 5e7c04ec, tools/check-self-assessment.py and tools/tsukuroi-census.sh as git blobs at 5e7c04ec, the C1 receipts and exits.txt under .ufo/waves/round-25/measure/, git config files, and the absence of /etc/gitattributes; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RerunC1.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RerunC1/ (c1-b9046016-rerun.json, c1-5e7c04ec-rerun.json, selftest-rerun.json, sb-b9046016-dirty-run.json, sb-5e7c04ec-dirty-run.json), /fast/scratch/hyaku/tsukuroi-r25/w2/RerunC1/ (sandboxes att-*, sb-*, sb2-*, strace-*.txt, census-5e7c04ec.sh); executed=python3 tools/check-self-assessment.py for b9046016, 5e7c04ec, HEAD and an unknown revision, and --selftest, in the lane; the same tool in sandboxes; strace -f on the tool at both revisions; a Python audit-hook child run of the tool; bash tools/tsukuroi-census.sh --selftest in sandboxes with inherited, hostile and empty environments; git show, ls-tree, rev-parse, archive, hash-object and config --list; git status --porcelain (twice, without the flag) and git --no-optional-locks status --porcelain; wc and grep counts.

Model: anthropic/claude-haiku-5-5 (from the host project-context block)
Installs: none
