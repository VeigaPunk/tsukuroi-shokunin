DOES NOT MEET the C1 after-value: K08FixtureKeyed candidate_matches=0/24, K12TypeF=1/24, K13PacdiffExact=1/24; each has harness_errors=[] and exit_code=1.

1. [obs] The assigned axes were coverage and control:rescore. Each saved wave-1 patch was replayed unchanged onto 7186722b8eba243439c6724766bdae2ef13c595c, committed separately in /fast/scratch/hyaku/tsukuroi-r35/W2RescoreC/repo, and scored exactly once with VERSION 2 and --skip-battery. No listed control meets VERSION 2; these three rescores therefore supply no surviving-control finding against C1. They do not establish the whole claim. The VERSION 1 results below come from the original receipts, not a rerun.

| Control | VERSION 1 result | VERSION 2 candidate_matches/of | VERSION 2 exit | Dominant reason |
|---|---|---|---|---|
| K08FixtureKeyed | MEETS: matches=24/24, harness_errors=[], exit=0 | 0/24 | 1 | field mismatch, all 24 views |
| K12TypeF | DOES NOT MEET: matches=8/24, harness_errors=[], exit=1 | 1/24 | 1 | field mismatch, all 23 synthetic views; live matches |
| K13PacdiffExact | DOES NOT MEET: matches=12/24, harness_errors=[], exit=1 | 1/24 | 1 | field mismatch, all 23 synthetic views; live matches |

Evidence for VERSION 1: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K08FixtureKeyed/variant.jsonl:27-28; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K12TypeF/type-f.jsonl:27-28; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K13PacdiffExact/pacdiff-exact.jsonl:27-28. Evidence for VERSION 2: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/K08FixtureKeyed.jsonl:3-28; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/K12TypeF.jsonl:3-28; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/K13PacdiffExact.jsonl:3-28.

2. [obs] The required equality command, timeout 15 git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --stat 6b4561e4 7186722b8eba243439c6724766bdae2ef13c595c -- tools/tsukuroi-census.sh, exited 0 with empty stdout. Each replayed census has exactly the wave-1 receipt's census SHA-256. The saved VERSION 2 patches sit beside their receipts and contain only the assigned census changes. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/construction.json:7-13,327-356; each listed receipt:2; each same-named .patch:1.

| Control | Replayed commit, parent 7186722b8eba243439c6724766bdae2ef13c595c | census_sha256 |
|---|---|---|
| K08FixtureKeyed | 6e72ba6a398e35a111b640aefd0aefd5f280c599 | 00fa116a7369a35ba1154f2cf40b1daea7ba8e119e028343229c1535c6a6913e |
| K12TypeF | a76a0add52cd5769c2855bc2832fe2bf07382a9f | 08f977539a92e990b0a339132dbe13543da31932c311d76e3e916f8ea6890a33 |
| K13PacdiffExact | 9818ea42843d1e7497eaccc418435628e0199ee8 | c01d472aa20bad30ad1fc952b79a43f9a006fe65e90c73d99df4fb215c423d54 |

[obs] Every VERSION 2 receipt names tool_revision=7186722b8eba243439c6724766bdae2ef13c595c, counter_sha256=7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1, and receipt tool_sha256 equal to that counter hash. VERSION 1's counter_sha256 was 19d25d14f9ee6ad15c036c75f997f2fba7aa756779c9e3b70a0ff136297e0155. The counter, predicate, battery, label and original patches were not edited. Evidence: the six original/rescore receipts:1-2; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/construction.json:13,361.

3. [obs] These are the literal per-view reasons. null is the accepted live row's actual JSON value. Each table row is at the indicated line in all three VERSION 2 receipts named in finding 1. Every census row exits 2, which the frozen predicate accepts; all three receipt footers have timed_out=false and empty stderr_tail.

| View | Receipt line | K08FixtureKeyed reason | K12TypeF reason | K13PacdiffExact reason |
|---|---|---|---|---|
| stub-00 | 3 | field mismatch | field mismatch | field mismatch |
| stub-01 | 4 | field mismatch | field mismatch | field mismatch |
| stub-02 | 5 | field mismatch | field mismatch | field mismatch |
| stub-03 | 6 | field mismatch | field mismatch | field mismatch |
| stub-04 | 7 | field mismatch | field mismatch | field mismatch |
| stub-05 | 8 | field mismatch | field mismatch | field mismatch |
| stub-06 | 9 | field mismatch | field mismatch | field mismatch |
| stub-07 | 10 | field mismatch | field mismatch | field mismatch |
| stub-08 | 11 | field mismatch | field mismatch | field mismatch |
| stub-09 | 12 | field mismatch | field mismatch | field mismatch |
| stub-10 | 13 | field mismatch | field mismatch | field mismatch |
| stub-11 | 14 | field mismatch | field mismatch | field mismatch |
| stub-12 | 15 | field mismatch | field mismatch | field mismatch |
| stub-13 | 16 | field mismatch | field mismatch | field mismatch |
| stub-14 | 17 | field mismatch | field mismatch | field mismatch |
| stub-15 | 18 | field mismatch | field mismatch | field mismatch |
| stub-16 | 19 | field mismatch | field mismatch | field mismatch |
| stub-17 | 20 | field mismatch | field mismatch | field mismatch |
| stub-18 | 21 | field mismatch | field mismatch | field mismatch |
| stub-19 | 22 | field mismatch | field mismatch | field mismatch |
| ns-20 | 23 | field mismatch | field mismatch | field mismatch |
| ns-21 | 24 | field mismatch | field mismatch | field mismatch |
| ns-22 | 25 | field mismatch | field mismatch | field mismatch |
| live | 26 | field mismatch | null | null |

4. [obs] The preserved defects are K08's name-length substitutes for pairing/readability, K12's regular-file-only selection, and K13's directory-inclusive pacdiff find expression. The expected adversarial detector outcome was fewer than 24 matches for each; that outcome was observed. The rescores are not single-cause isolation tests: all three preserved wave-1 arms also count the valid outside-/etc warning that VERSION 2 excludes. For example, every synthetic row reports log_pacnew one above expected. K12 additionally reports pacnew two below expected, pacsave and pacorig one below, and unlogged four below. K13 additionally reports gone one below expected and counts extra pacnew entries. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/K08FixtureKeyed.patch:18-48; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/K12TypeF.patch:65-89; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/K13PacdiffExact.patch:42-48,82-100; all three rescore receipts:3-25. [inf] The new counter refuses these exact earlier controls, but the results alone cannot attribute each refusal exclusively to the defect in its seat name.

5. [obs] The same unchanged VERSION 2 --skip-battery detector was also run on pristine and exactly restored candidate bytes. Both report candidate_matches=0, of=24, harness_errors=[], exit_code=1; the inspected rows report drift_lines=0 because this candidate has no claimed arm. Formal calibrated mutation verdict: INCONCLUSIVE for each mutation, not killed, because the pristine baseline fails. Separately, the assigned control-rescore verdicts are the observed DOES NOT MEET results in finding 1. Exact restoration occurred in a finally block: before and restored census SHA-256 are both 7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5, and restored_exact_bytes=true records byte-for-byte equality with git show of the pinned candidate. The counter's restored hash remains 7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1. The three control commits remain on private scratch branches; final scratch HEAD and working census are the pristine candidate, with no restoration commit. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/pristine.jsonl:1-4,27-28; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/restored.jsonl:1-2,23-28; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/construction.json:299-325,359-361.

6. [obs] Each variant used the prescribed timeout-900 run-receipt.py form, --timeout 800, the pinned tool revision and literal {lane}/{rev} substitution, adding only seat-local TMPDIR. Full argv, actual output and exit are saved in the three *-command.json files:3-37 under /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/. Three variant scoring calls ran concurrently in one foreground ThreadPoolExecutor(max_workers=3), which joined before returning. Pristine and restored calls were foreground and returned. No full battery, additional variant score, external-source fetch, package transaction, service action, integration or shipping change was performed. No background job or persistent service was started. All launched command trees returned. The prescribed receipt runner itself creates disposable run-receipt-* and run-receipt-home-* directories directly under /fast/scratch/hyaku, outside the seat root, despite TMPDIR; its finally block removes them. This tool-managed path-scope exception is disclosed rather than claimed seat-local. Evidence: /fast/scratch/hyaku/tsukuroi-r35/W2RescoreC/repo/tools/run-receipt.py:75-83,116-118; the five receipt footers:28; the three *-command.json files:34-36. All direct git writes were confined to the assigned clone and its push URL was disabled before replay.

Scope: read=godspeed/shokunin skills and canonical protocol excerpts, candidate declaration/redesign, lane QUALITY, pinned counter predicate/battery/execution and receipt runner, three wave-1 reports/patches/receipts, own results; wrote=/fast/scratch/hyaku/tsukuroi-r35/W2RescoreC/, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC/, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreC.md, prescribed runner disposable /fast/scratch/hyaku/run-receipt-* and run-receipt-home-*; executed=timeout-bounded mkdir, read-only lane git show/diff, isolated clone/checkout/remote set-url/apply/add/commit/rev-parse/diff/show, sha256sum, foreground Python orchestration/hash/byte comparison, five run-receipt.py calls of unchanged VERSION 2 --skip-battery (pristine, three controls once each, restored)
Model: openai-codex/gpt-6.1-sol
Installs: none
