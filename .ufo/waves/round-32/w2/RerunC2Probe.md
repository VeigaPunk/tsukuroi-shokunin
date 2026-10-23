Verdict: [obs] The requested C2 re-run reproduces leaking 0 of 11, harness_errors [], exit 0; no actionable failure was observed in these exercised cases.

The measured axis is operability, channel ambient-names. Adjacency was not measured by this seat, and no ordinal or round-admission judgment is made.

1. [obs] The run-receipt header binds both revision and tool_revision to b8bf150722a2261c80ab2ce012de3690ba732eeb and the probe to sha256 d43f95ed8a740b71aac1ab412e769e011127eb4ae29646d12b2075a696cf0576. The summary reports targets 11, pairs 11, leaking 0, leaking_pairs [], harness_errors [], and predicate_label leaking. The footer reports exit_code 0, timed_out false, and empty stderr_tail. The run began at 2026-10-23T02:39:02Z and ended at 02:42:35Z. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:1,13-14.

The executed command was `timeout 3000 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/run-receipt.py --lane /fast/scratch/hyaku/tsukuroi-r32/RerunC2Probe/repo --revision b8bf150722a2261c80ab2ce012de3690ba732eeb --tool-revision b8bf150722a2261c80ab2ce012de3690ba732eeb --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl --timeout 2900 -- tools/probe-child-env-allowlist-r32.py --revision '{rev}' --lane '{lane}' --scratch /fast/scratch/hyaku/tsukuroi-r32/RerunC2Probe/probe`, from the lane directory. It exited 0. The sandbox was cloned without local object sharing, checked out at the assigned revision, and had its push URL disabled.

For each target below, the twelve injected names were BASH_ENV, ENV, GCONV_PATH, PERL5OPT, and that target's eight freshly generated names recorded in its receipt line. Every reached map was empty: none of those names reached any recorded successful child exec after the target's own first exec, so there is no name-to-child carrier to list. Every parity_diffs list was empty, meaning the probe reported matching exit code, normalised stdout digest, and successful git-exec count. Every bashenv_log_exists was false, bashenv_log_lines was 0, and leak was false.

2. [obs] check-adjacency-overlap.py had no injected-name carrier. Control/channel exit codes were 0/0 and successful git-exec counts were 1263/1263; normalised stdout parity held. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:2.

3. [obs] check-freshness-r17.py had no injected-name carrier. Control/channel exit codes were 0/0 and successful git-exec counts were 116/116; normalised stdout parity held. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:3.

4. [obs] check-kernel-taint.py had no injected-name carrier. Control/channel exit codes were 0/0 and successful git-exec counts were 933/933; normalised stdout parity held. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:4.

5. [obs] check-memory-pressure.py had no injected-name carrier. Control/channel exit codes were 0/0 and successful git-exec counts were 390/390; normalised stdout parity held. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:5.

6. [obs] check-registry-coverage.py had no injected-name carrier. Control/channel exit codes were 0/0 and successful git-exec counts were 324/324; normalised stdout parity held. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:6.

7. [obs] check-storage-health.py had no injected-name carrier. Control/channel exit codes were 0/0 and successful git-exec counts were 717/717; normalised stdout parity held. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:7.

8. [obs] mutants-adjacency-overlap.py had no injected-name carrier. Control/channel exit codes were 0/0 and successful git-exec counts were 991/991; normalised stdout parity held. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:8.

9. [obs] mutants-kernel-taint.py had no injected-name carrier. Control/channel exit codes were 0/0 and successful git-exec counts were 635/635; normalised stdout parity held. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:9.

10. [obs] check-self-assessment.py had no injected-name carrier. Control/channel exit codes were 0/0 and successful git-exec counts were 331/331; normalised stdout parity held. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:10.

11. [obs] mutants-owed-statements-r29.py had no injected-name carrier. Control/channel exit codes were 0/0 and successful git-exec counts were 900/900; normalised stdout parity held. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:11.

12. [obs] mutants-owed-statements-r29-landed.py had no injected-name carrier. Control/channel exit codes were 0/0 and successful git-exec counts were 1044/1044; normalised stdout parity held. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl:12.

13. [obs] Residual risk and verification gaps: this was one full fresh-name invocation of the canonical committed probe, not an independent trace-parser audit or an exhaustive proof over arbitrary names and target modes. The canonical implementation retains successful execve records, excludes the target's first exec, compares only rc, normalised stdout and git-exec count for parity, and removes its scratch tree on completion. Evidence: /fast/scratch/hyaku/tsukuroi-r32/RerunC2Probe/repo/tools/probe-child-env-allowlist-r32.py:156-185,232-237,312-327,373-425. [unk] Behaviour outside those exercised paths and stderr parity are not established. Rerouting, resume continuity and saturation were not exercised or certified.

14. [obs] The lsp device was unavailable: reading xd://lsp returned “No such tool” and listed only ast_edit and debug as mounted devices. Source inspection therefore used textual reads and read-only git diff, not semantic references, definitions or diagnostics. No semantic-callsite proof is claimed. The foreground receipt command completed; `timeout 10 pgrep -af '/fast/scratch/hyaku/tsukuroi-r32/RerunC2Probe/(repo|probe)'` subsequently exited 1 with no matches. No background job was started. The PTY request was unavailable and fell back to foreground non-terminal execution; this was reported through xd://report_issue and did not change the successful receipt result.

15. [obs] This seat did not modify target code, predicates or counters, and did not commit the new report or receipt. They remain seat evidence, not a claim of committed-receipt admission under QUALITY 77. Evidence: the applicable commitment requirement is /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:147.

Scope: read=Godspeed skill, declaration at fe1ae02c, Hyaku addendum, prior rejection background, QUALITY 70-81, receipt runner, committed C2 probe/diff, generated receipt; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w2/RerunC2Probe/c2-b8bf1507.jsonl, /fast/scratch/hyaku/tsukuroi-r32/RerunC2Probe/, xd://report_issue; executed=timeout-bounded mkdir and sandbox git clone/checkout/remote push-disable, read-only git show/diff, requested run-receipt C2 probe, owned-process pgrep
Model: openai-codex/gpt-6.1-sol
Installs: none
