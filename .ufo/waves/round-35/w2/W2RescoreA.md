DOES NOT MEET the C1 after-value: K02JunkBytes=0/24, K03AllZero=0/24, K04ConstantLive=1/24, K05LogReaderOnly=0/24; every control has harness_errors=[] and exit=1.

1. [obs] The axes are coverage and control:rescore. Each listed wave-1 patch was applied without changes onto 7186722b8eba243439c6724766bdae2ef13c595c, committed independently in /fast/scratch/hyaku/tsukuroi-r35/W2RescoreA/repo, and scored exactly once with VERSION 2 and --skip-battery. The required git diff --stat 6b4561e4 7186722b8eba243439c6724766bdae2ef13c595c -- tools/tsukuroi-census.sh exited 0 with empty output. Every receipt binds counter_sha256=7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1, tool_revision=7186722b8eba243439c6724766bdae2ef13c595c and battery=false. VERSION 2 requires candidate_matches=24 of 24, empty harness_errors and exit 0 for these control runs. No counter was edited and no battery was run by this seat. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/mutants.json:3-16 and each VERSION 2 receipt below at lines 1-2 and 27-28; the fixed predicate is /fast/scratch/hyaku/tsukuroi-r35/W2RescoreA/repo/tools/score-pacnew-arm-r35b.py:62-72.

| Control | VERSION 1 result, matches/of; exit | VERSION 2 candidate_matches/of | VERSION 2 exit | Dominant VERSION 2 reason |
|---|---|---|---|---|
| K02JunkBytes | 0/24; 1 | 0/24 | 1 | drift_lines=0, all 24 views |
| K03AllZero | 0/24; 1 | 0/24 | 1 | field mismatch, all 24 views |
| K04ConstantLive | 0/24; 1 | 1/24 | 1 | field mismatch, 23 views; live matches |
| K05LogReaderOnly | 0/24; 1 | 0/24 | 1 | field mismatch, all 24 views |

[obs] harness_errors=[] in all four VERSION 1 receipts and all four VERSION 2 receipts. Each VERSION 2 footer has timed_out=false and empty stderr_tail. The VERSION 1 values above come from the original receipts, not a rerun:
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K02JunkBytes/junk-bytes.jsonl:27-28.
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K03AllZero/all-zero.jsonl:27-28.
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K04ConstantLive/constant-live.jsonl:27-28.
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K05LogReaderOnly/log-reader-only.jsonl:27-28.

[obs] The corresponding VERSION 2 summaries and footers are:
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/K02JunkBytes.jsonl:27-28.
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/K03AllZero.jsonl:27-28.
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/K04ConstantLive.jsonl:27-28.
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/K05LogReaderOnly.jsonl:27-28.

2. [obs] The replays retain exactly the wave-1 census bytes: the census_sha256 in each new receipt equals the corresponding original receipt's line 2. K02 appends comments and an unused no-op; it supplies no arm. K03 adds a literal all-zero line without reading the drift inputs. K04 prints its saved live constants and exits immediately. K05 reads only the log for its added arm, with no tree sweep or tree/log pairing. The saved patches beside the new receipts contain only their original census changes. Evidence: the original patch paths recorded at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/mutants.json:13,29,45,61, the four new patches at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/K02JunkBytes.patch:1, K03AllZero.patch:1, K04ConstantLive.patch:1 and K05LogReaderOnly.patch:1 in that same absolute directory, and each new receipt's line 2.

| Control | Replayed commit, parent 7186722b8eba243439c6724766bdae2ef13c595c | census_sha256 |
|---|---|---|
| K02JunkBytes | a61707d3f95e61102e95f8fbb5e4ebd3dfabee31 | 3a9a8e9a683d86ea155da1e1c3934e2e6a3c4ed25541e363c04b4201965e31cc |
| K03AllZero | 2d00e01a5d67acabb876766bdad94ce644cec0e0 | 75effdef0eb52a05ab06d66c5b25a529876d5082f772eb6e72050ce3191cf6a6 |
| K04ConstantLive | 7ac112df72147cff81e4009cc977ac537ce8c6a6 | 31a9b8444cde7804708e6521afa4fda97d0ca812d0ab4d4f0be6936fe6578990 |
| K05LogReaderOnly | 4907b5946645d411780b0ecc56d4e923c44a30fc | ee0e3c089193d63b10282dada9bcc7c494314e087e09c8f6b17631fc0662433c |

3. [obs] The per-view reasons below are literal receipt values; null means a matching view. The rows correspond, in order, to lines 3-26 of each of these absolute receipts:
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/K02JunkBytes.jsonl:3-26.
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/K03AllZero.jsonl:3-26.
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/K04ConstantLive.jsonl:3-26.
- /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/K05LogReaderOnly.jsonl:3-26.

| View | K02JunkBytes | K03AllZero | K04ConstantLive | K05LogReaderOnly |
|---|---|---|---|---|
| stub-00 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-01 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-02 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-03 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-04 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-05 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-06 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-07 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-08 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-09 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-10 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-11 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-12 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-13 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-14 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-15 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-16 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-17 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-18 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| stub-19 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| ns-20 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| ns-21 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| ns-22 | drift_lines=0 | field mismatch | field mismatch | field mismatch |
| live | drift_lines=0 | field mismatch | null | field mismatch |

[obs] The child census exit is 2 on every K02, K03 and K05 view and 0 on every K04 view; these are allowed exits, not the reasons for refusal. K04's content-free constants match the live view exactly, but miss all 20 stub and all 3 namespace views. K05 also reports log_pacnew=11 instead of 10 on stub-00 because its global log reader includes the non-/etc event; its reported filesystem fields are zero. Evidence: K04ConstantLive.jsonl:3-26 and K05LogReaderOnly.jsonl:3 in the absolute VERSION 2 receipt directory above. [inf] None of these four controls meets VERSION 2, so this seat supplies no finding that kills C1. A passing live view alone is not the declared after-value and is not evidence that the full C1 target is met.

4. [obs] The same additional bounded behavioral detector ran on pristine, mutated and restored worktree bytes for each control. This is not an extra score invocation: it calls VERSION 2's unchanged oracle, harness, snapshot, ctimes and judge helpers on one fixed readable fixture, running timeout 30 bash /fast/scratch/hyaku/tsukuroi-r35/W2RescoreA/repo/tools/tsukuroi-census.sh each time. The oracle tuple, in order pacnew, pacsave, pacorig, unreadable, log_pacnew, log_pacsave, unlogged, gone, is (1,1,1,0,1,1,2,1). The driver and exact commands are retained at /fast/scratch/hyaku/tsukuroi-r35/W2RescoreA/rescore.py:1 and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/commands.json:1.

| Control | Pristine output; exit | Mutated output; exit | Restored output; exit | Mutation verdict |
|---|---|---|---|---|
| K02JunkBytes | no drift line; 2 | no drift line; 2 | no drift line; 2 | INCONCLUSIVE |
| K03AllZero | no drift line; 2 | tuple (0,0,0,0,0,0,0,0); 2 | no drift line; 2 | INCONCLUSIVE |
| K04ConstantLive | no drift line; 2 | tuple (3,0,0,11,3,0,0,0); 0 | no drift line; 2 | INCONCLUSIVE |
| K05LogReaderOnly | no drift line; 2 | tuple (0,0,0,0,2,1,0,2); 2 | no drift line; 2 | INCONCLUSIVE |

[obs] Every pristine/restored reason is drift_lines=0; mutated reasons are drift_lines=0 for K02 and field mismatch for the other three. Every fixed-fixture run has matches=false and fixture_unchanged=true, with identical before/after fixture hash b5a3ba05da28208de7fe28ce957d19fdf92ac00750894c2ab80b8de64eb5ea0a. Full stdout and stderr are retained rather than invented output excerpts. Evidence: the twelve <Control>-pristine.json, <Control>-mutated.json and <Control>-restored.json files under /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/; in every file lines 5-20 hold exit, oracle, unchanged status and reason; stdout is line 24 for pristine/restored/K02-mutated and line 33 for the other mutants. [inf] These are rejected controls, not killed mutants: the pristine baseline already fails, making the mutation-test classification inconclusive for all four.

5. [obs] Exact source restoration completed after each score, before the next independent replay. All four before/restored census SHA-256 values are 7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5; restored_exact_bytes is true for each, and the counter hash remains 7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1. The mutated hashes are the four receipt-bound hashes in finding 2. The clone ends at the pristine candidate; the four variant objects and saved patches remain available. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/mutants.json:5-16,21-32,37-48,53-64 and the restored detector files cited in finding 4. All commands were finite and timeout-wrapped; the outer driver returned exit 0. No subagent, background job, other mission runtime, privileged command, external source fetch or package transaction was started by this seat. No lane source or sibling file was edited.

Scope: read=Godspeed/shokunin guidance, operator RULES, lane QUALITY, candidate declaration/redesign, pinned VERSION 2 counter and receipt runner, four wave-1 reports/patches/receipts and generated evidence; wrote=/fast/scratch/hyaku/tsukuroi-r35/W2RescoreA/, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA/, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreA.md; executed=timeout-wrapped mkdir, isolated git clone/checkout/remote/apply/add/commit/rev-parse/diff, sha256sum, df, Python rescore.py with four run-receipt.py --skip-battery calls and twelve fixed-fixture detector calls, including their bounded counter/census children
Model: openai-codex/gpt-6.1-sol
Installs: none
