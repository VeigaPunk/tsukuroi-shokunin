DOES NOT MEET the C1 after-value: leaking=21, pairs=21 (27 intended), harness_errors=[tools/check-locator-clarification.py, tools/check-section-citations.py], exit=2.



1. [obs] The axis is operability, control inherit. Exactly one variant commit, eefdc30cf764658305b43f66cc8d8a49e337b214, descends from declaration 6de666c427ba9aa6b4350561980bde8d0e7c261d. It removes env= from all 14 subprocess calls passing the ambient-copy builders across all nine claim targets, including the nested selftest git helpers; builders and other behavior are unchanged. The patch is /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit.patch:1 (sha256 7a666a6e62dd7d6a8d575fe4089003a5651b1a0f808bb7c1b0869b38de5008cf). The variant identity and frozen probe hash are recorded at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/variant.json:1.



2. [obs] The frozen full claim-set probe was scored exactly once, without --only or a narrowed target set. Its run lasted 2026-10-23T08:45:34Z to 08:46:09Z. The exact bounded command and return code are at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/execution.json:2-39; the receipt header is /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:1. The outer timeout was 2400 seconds, with run-receipt --timeout 2300 and an explicit seat-local --scratch. Frozen probe and predicate bytes were not edited. The actual summary line at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:25 is:

{"revision": "eefdc30cf764658305b43f66cc8d8a49e337b214", "targets": 9, "channels": ["names", "quiet", "source"], "pairs": 21, "leaking": 21, "leaking_pairs": ["tools/check-boot-chain.py:names", "tools/check-boot-chain.py:quiet", "tools/check-boot-chain.py:source", "tools/check-btrfs-repair-r31.py:names", "tools/check-btrfs-repair-r31.py:quiet", "tools/check-btrfs-repair-r31.py:source", "tools/check-btrfs-space-r30.py:names", "tools/check-btrfs-space-r30.py:quiet", "tools/check-btrfs-space-r30.py:source", "tools/check-recheck-commands.py:names", "tools/check-recheck-commands.py:quiet", "tools/check-recheck-commands.py:source", "tools/check-seat-scope.py:names", "tools/check-seat-scope.py:quiet", "tools/check-seat-scope.py:source", "tools/check-source-scope-correction.py:names", "tools/check-source-scope-correction.py:quiet", "tools/check-source-scope-correction.py:source", "tools/measure-update-recheck.py:names", "tools/measure-update-recheck.py:quiet", "tools/measure-update-recheck.py:source"], "harness_errors": ["tools/check-locator-clarification.py", "tools/check-section-citations.py"], "probe_sha256": "35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8", "probe_version": 4, "target_set": "claim", "scratch": "/fast/scratch/hyaku/tsukuroi-r34/C11InheritNoEnv/probe-scratch/sa5a360b1fa33-4j_4zv9u", "predicate_label": "leaking"}

The actual footer at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:26 is {"receipt_end": 1, "exit_code": 2, "timed_out": false, "stderr_tail": "", "finished_utc": "2026-10-23T08:46:09Z"}.



3. [obs] Per-pair evidence follows. In every emitted names pair, all 12 injected names reached children; in every emitted quiet pair, all eight reached children. In both channels for each emitted tool, all ten exact ambient value strings reached children: HOME, TMPDIR, XDG_CONFIG_HOME, PATH, LANG, TZ, TERM, USER, LOGNAME and SHELL. All emitted run pairs retained parity: control and channel rc=0, equal stdout digests and equal successful git-exec counts, with parity_diffs=[]. Thus parity did not fire; names, values and missing required git settings did fire. The kept-settings count means git children missing GIT_CONFIG_NOSYSTEM=1 or GIT_CONFIG_GLOBAL=/dev/null. The machine-readable pair-by-pair extraction is /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/per-pair-evidence.json:1.

   [obs] check-boot-chain / names: leaking. names 12/12, values 10/10, kept settings missing 18/75, parity did not fire (rc 0→0, git execs 75→75, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:2.

   [obs] check-boot-chain / quiet: leaking. names 8/8, values 10/10, kept settings missing 18/75, parity did not fire (rc 0→0, git execs 75→75, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:3.

   [obs] check-boot-chain / source: leaking. tools/check-boot-chain.py:805 inheriting-spawn subprocess.run without env; tools/check-boot-chain.py:802 ambient-read .environ. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:4.

   [obs] check-btrfs-repair-r31 / names: leaking. names 12/12, values 10/10, kept settings missing 28/28, parity did not fire (rc 0→0, git execs 28→28, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:5.

   [obs] check-btrfs-repair-r31 / quiet: leaking. names 8/8, values 10/10, kept settings missing 28/28, parity did not fire (rc 0→0, git execs 28→28, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:6.

   [obs] check-btrfs-repair-r31 / source: leaking. tools/check-btrfs-repair-r31.py:117 inheriting-spawn subprocess.run without env; tools/check-btrfs-repair-r31.py:108 ambient-read .environ. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:7.

   [obs] check-btrfs-space-r30 / names: leaking. names 12/12, values 10/10, kept settings missing 35/35, parity did not fire (rc 0→0, git execs 35→35, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:8.

   [obs] check-btrfs-space-r30 / quiet: leaking. names 8/8, values 10/10, kept settings missing 35/35, parity did not fire (rc 0→0, git execs 35→35, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:9.

   [obs] check-btrfs-space-r30 / source: leaking. tools/check-btrfs-space-r30.py:101 inheriting-spawn subprocess.run without env; tools/check-btrfs-space-r30.py:105 inheriting-spawn subprocess.run without env; tools/check-btrfs-space-r30.py:377 inheriting-spawn subprocess.run without env; tools/check-btrfs-space-r30.py:96 ambient-read .environ. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:10.

   [obs] check-locator-clarification: names, quiet and source were not evaluated. Harness error: control run failed rc 1:  All three pairs are unknown, not passing and not counted in pairs. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:11.

   [obs] check-recheck-commands / names: leaking. names 12/12, values 10/10, kept settings missing 474/953, parity did not fire (rc 0→0, git execs 953→953, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:12.

   [obs] check-recheck-commands / quiet: leaking. names 8/8, values 10/10, kept settings missing 474/953, parity did not fire (rc 0→0, git execs 953→953, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:13.

   [obs] check-recheck-commands / source: leaking. tools/check-recheck-commands.py:803 inheriting-spawn subprocess.run without env; tools/check-recheck-commands.py:799 ambient-read .environ. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:14.

   [obs] check-section-citations: names, quiet and source were not evaluated. Harness error: control run failed rc 2:  All three pairs are unknown, not passing and not counted in pairs. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:15.

   [obs] check-seat-scope / names: leaking. names 12/12, values 10/10, kept settings missing 35/123, parity did not fire (rc 0→0, git execs 123→123, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:16.

   [obs] check-seat-scope / quiet: leaking. names 8/8, values 10/10, kept settings missing 35/123, parity did not fire (rc 0→0, git execs 123→123, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:17.

   [obs] check-seat-scope / source: leaking. tools/check-seat-scope.py:177 inheriting-spawn subprocess.run without env; tools/check-seat-scope.py:539 inheriting-spawn subprocess.run without env; tools/check-seat-scope.py:174 ambient-read .environ. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:18.

   [obs] check-source-scope-correction / names: leaking. names 12/12, values 10/10, kept settings missing 12/48, parity did not fire (rc 0→0, git execs 48→48, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:19.

   [obs] check-source-scope-correction / quiet: leaking. names 8/8, values 10/10, kept settings missing 12/48, parity did not fire (rc 0→0, git execs 48→48, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:20.

   [obs] check-source-scope-correction / source: leaking. tools/check-source-scope-correction.py:358 inheriting-spawn subprocess.run without env; tools/check-source-scope-correction.py:473 inheriting-spawn subprocess.run without env; tools/check-source-scope-correction.py:355 ambient-read .environ. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:21.

   [obs] measure-update-recheck / names: leaking. names 12/12, values 10/10, kept settings missing 22/75, parity did not fire (rc 0→0, git execs 75→75, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:22.

   [obs] measure-update-recheck / quiet: leaking. names 8/8, values 10/10, kept settings missing 22/75, parity did not fire (rc 0→0, git execs 75→75, parity_diffs=[]). Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:23.

   [obs] measure-update-recheck / source: leaking. tools/measure-update-recheck.py:488 inheriting-spawn subprocess.run without env; tools/measure-update-recheck.py:441 inheriting-spawn subprocess.run without env; tools/measure-update-recheck.py:537 inheriting-spawn subprocess.run without env; tools/measure-update-recheck.py:438 ambient-read .environ; tools/measure-update-recheck.py:485 ambient-read .environ. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/inherit-claim.jsonl:24.



4. [obs] The expected supplementary bounded detector was a read-only git-helper invocation for every target, under GIT_R34_C11_MARKER=1 and ZZ_R34_AMBIENT=1. It observes actual subprocess.Popen audit events while allowing the git reads to execute; its pass condition is that the git marker is absent from the supplied effective child environment. The same detector ran on pristine, mutated and restored bytes, yielding exits 0, 1 and 0. All nine git helper reads succeeded in all three phases. Pristine and restored calls supplied explicit environments and stripped the GIT_ marker; mutated calls omitted env and carried both markers. Mutant verdict for this GIT_ stripping invariant: killed. This is not a full allow-list claim: the pristine builder still passes the non-GIT marker. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/detect-inheritance.py:1; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/pristine-detector.json:1; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/mutated-detector.json:1; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/restored-detector.json:1. Commands were timeout 45 python3 -B /fast/scratch/hyaku/tsukuroi-r34/C11InheritNoEnv/detect-inheritance.py pristine, the same command with mutated, and the same command with restored.



5. [obs] The full frozen probe has two harness failures, so its whole-mutant kill classification is inconclusive, not a clean 27-pair kill. Seven evaluated tools nevertheless leak in every channel, and this control does not meet the after-value. [unk] The six omitted channel pairs have no frozen detector result; the receipt gives no cause beyond locator selftest rc 1 and section selftest rc 2. No rerun, repair or counter alteration was performed.



6. [obs] All nine scratch worktree source files were restored byte-for-byte to their saved pristine bytes before the committed variant was scored. Each before, mutated and restored SHA256 and exact-byte comparison is recorded at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/restoration.json:1; all_exact=true and detector_exit_codes=[0,1,0]. The variant commit remains available for reproduction, while its worktree holds the restored declaration bytes. The probe hash is 35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8. No lane code, frozen probe or sibling source was edited. All invoked commands completed; the scoring process group received a final kill attempt to remove any descendants. No background job or subagent was started. The tool rejected pty=true as unavailable on the initial clone command; that command completed without a terminal. This was reported through xd://report_issue, and the scoring command ran synchronously through a bounded Python subprocess.



Scope: read=declaration, godspeed and shokunin skill requirements, hyaku addendum, lane QUALITY, host tooling rules, nine scratch target spawn sites, frozen probe and receipt runner, own evidence; wrote=/fast/scratch/hyaku/tsukuroi-r34/C11InheritNoEnv/, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv/, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/C11InheritNoEnv.md; executed=timeout-bounded git show, df, mkdir, isolated git clone/checkout/remote/add/commit/diff, read-only git helper detector on pristine/mutated/restored bytes, one full frozen probe via run-receipt, Python evidence derivation and restoration hash comparisons

Model: openai-codex/gpt-6.1-sol

Installs: none
