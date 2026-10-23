DOES NOT MEET the C1 after-value: K06FsReaderOnly=0/24, K07NaivePac=1/24, K10LiveEtc=1/24, K11NoPairing=1/24; harness_errors=[] and exit=1 for each.

1. [obs] The axes are coverage, control:rescore and exact-byte restoration. Each requested unchanged wave-1 patch was applied to 7186722b8eba243439c6724766bdae2ef13c595c in the isolated clone, committed on its own branch, and scored exactly once with VERSION 2 and --skip-battery. No variant meets VERSION 2, so none of these four receipts supplies a control finding that ends C1. This is not an overall judgment of C1.

| Control | VERSION 1 result | VERSION 2 candidate_matches/of | VERSION 2 exit | Dominant reason |
|---|---|---|---|---|
| K06FsReaderOnly | 0/24; exit 1 | 0/24 | 1 | field mismatch (24 views) |
| K07NaivePac | 0/24; exit 1 | 1/24 | 1 | field mismatch (23 views) |
| K10LiveEtc | 0/24; exit 1 | 1/24 | 1 | field mismatch (23 views) |
| K11NoPairing | 0/24; exit 1 | 1/24 | 1 | field mismatch (23 views) |

The VERSION 1 receipt summary and footer evidence is:
- K06FsReaderOnly: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K06FsReaderOnly/fs-reader-only.jsonl:27-28.
- K07NaivePac: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K07NaivePac/naive.jsonl:27-28.
- K10LiveEtc: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K10LiveEtc/live-path.jsonl:27-28.
- K11NoPairing: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K11NoPairing/counts-without-pairing.jsonl:27-28.
The VERSION 2 receipt summary and footer evidence is:
- K06FsReaderOnly: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K06FsReaderOnly.jsonl:27-28. The footer has timed_out=false and empty stderr_tail.
- K07NaivePac: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K07NaivePac.jsonl:27-28. The footer has timed_out=false and empty stderr_tail.
- K10LiveEtc: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K10LiveEtc.jsonl:27-28. The footer has timed_out=false and empty stderr_tail.
- K11NoPairing: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K11NoPairing.jsonl:27-28. The footer has timed_out=false and empty stderr_tail.

2. [obs] Census bytes at the two candidate revisions are equal: the assigned git diff --stat 6b4561e4 7186722b8eba243439c6724766bdae2ef13c595c -- tools/tsukuroi-census.sh completed with empty output. Every reconstructed census SHA-256 equals its wave-1 receipt census_sha256, and every saved patch SHA-256 equals the source patch SHA-256. Only tools/tsukuroi-census.sh was patched. The exact commits and header hashes are:

| Control | New immutable variant commit | census_sha256 (same in VERSION 1 and VERSION 2) |
|---|---|---|
| K06FsReaderOnly | a1c11341d814029741babf0ced17f55dd8d56ae0 | 63a05423c93861a546973f128ba9da7db1e96935a402bc53cd87b3cd44480768 |
| K07NaivePac | c9a14cc3acb06465d0d3a01ae2a3f3483364d693 | 8a4fedc85ceb9c7e942c425c8cca09a1c322276e9c4a854bcd225ce3008cf4bf |
| K10LiveEtc | b62de386f9ca242a2794cddffa9935820994d222 | 57cfcbad3a5bec9f4b1bc89caf04d28908794aa2e0f463a2d52c39c29040229c |
| K11NoPairing | 266b9eff8955a62c0699e919cea70440a2f707bd | 3c3b6d275891b54b2c0198ac8cca00aba42dc1db926b7e2121fd3ee30c988e48 |

Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/setup-evidence.json:2-5; each VERSION 1 receipt above at line 2; each VERSION 2 receipt above at lines 1-2; and the corresponding /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/<Control>-lifecycle.json:48-50,103-104. Each exact diff is saved beside its receipt as <Control>.patch.

3. [obs] The expected official detector is tools/score-pacnew-arm-r35b.py VERSION 2 at 7186722b8eba243439c6724766bdae2ef13c595c. Its unchanged counter_sha256 is 7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1 in all four receipt headers, matching the runner tool_sha256. Its predicate compares all eight fields, checks fixture preservation, accepts census exits 0/1/2 within the bound, and requires claim-base parity in stub views. --skip-battery means these are control-wave results, not a battery measurement; control_matches and should_fail_accepted were not measured by this seat.
Evidence: /fast/scratch/hyaku/tsukuroi-r35/W2RescoreB/repo/tools/score-pacnew-arm-r35b.py:12-23,60-75,426-436; each VERSION 2 receipt above at lines 1-2. The exact scoring argv and actual runner output are in each <Control>-lifecycle.json:105-142 and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/commands.json.

4. [obs] The following exhaustively states each view reason. Every census invocation exited 2, which is allowed and is not the rejection reason. Null is the receipt's reason for a matching view.

| View IDs | K06FsReaderOnly reason | K07NaivePac reason | K10LiveEtc reason | K11NoPairing reason |
|---|---|---|---|---|
| stub-00, stub-01, stub-02, stub-03, stub-04, stub-05, stub-06, stub-07, stub-08, stub-09, stub-10, stub-11, stub-12, stub-13, stub-14, stub-15, stub-16, stub-17, stub-18, stub-19 | field mismatch | field mismatch | field mismatch | field mismatch |
| ns-20 | field mismatch | field mismatch | field mismatch | field mismatch |
| ns-21 | field mismatch | field mismatch | field mismatch | field mismatch |
| ns-22 | field mismatch | field mismatch | field mismatch | field mismatch |
| live | field mismatch | null (matches) | null (matches) | null (matches) |

Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K06FsReaderOnly.jsonl:3-26; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K07NaivePac.jsonl:3-26; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K10LiveEtc.jsonl:3-26; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K11NoPairing.jsonl:3-26.

[obs] K06 computes the filesystem counts but leaves the log counters and gone zero. K07 overcounts broad names and log substrings; for example stub-00 reports pacnew=9 versus 8 and log_pacnew=18 versus 11. K10 returns the live host tuple in all 20 stub views. Its namespace runs do reach the mounted fixture, but each reports log_pacnew one higher than expected; the patch counts a paired non-/etc warning that VERSION 2 excludes. K11 prints unlogged=0 and gone=0 in every view and also overcounts log_pacnew by one in each generated view. It is therefore not a pure pairing-only isolation under VERSION 2. No control was repaired or scored a second time.
Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K06FsReaderOnly.jsonl:3,26; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K07NaivePac.jsonl:3; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K10LiveEtc.jsonl:3-25; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K11NoPairing.jsonl:3-25; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K10LiveEtc/live-path.patch:52-58; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K11NoPairing/counts-without-pairing.patch:39-52. [inf] The three live-only passes show that this host draw alone does not discriminate those shortcuts; they do not meet the 24/24 target.

5. [obs] An unchanged bounded one-view auxiliary detector also ran on pristine, mutated and restored bytes for each variant. It is separate from the official 24-view counter entry point and produced no additional C1 receipt. The fixed expected tuple, in pacnew/pacsave/pacorig/unreadable/log_pacnew/log_pacsave/unlogged/gone order, is 2/2/1/1/4/1/3/1. Every pristine and restored run had census exit 2, detector exit 1, reported=null and reason drift_lines=0. Each mutated run had census exit 2, detector exit 1 and reason field mismatch:

| Mutant | Actual mutated tuple | Formal lifecycle verdict |
|---|---|---|
| K06FsReaderOnly | 2/2/1/1/0/0/5/0 | INCONCLUSIVE: pristine baseline fails |
| K07NaivePac | 4/2/1/1/6/1/4/3 | INCONCLUSIVE: pristine baseline fails |
| K10LiveEtc | 3/0/0/11/3/0/0/0 | INCONCLUSIVE: pristine baseline fails |
| K11NoPairing | 2/2/1/1/4/1/0/0 | INCONCLUSIVE: pristine baseline fails |

These auxiliary lifecycle results are not claimed as killed mutants. The official counter rejections in finding 1 remain observed control results. The fixture digest including accessible bytes, modes and inode change times stayed 73c92550072c916c81fed533cb1dcf3c8ebf553e26092de974e925438190505c before and after all twelve auxiliary runs.
Evidence: /fast/scratch/hyaku/tsukuroi-r35/W2RescoreB/detect-one.py:1-91; each /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/<Control>-lifecycle.json:13-47,51-75,78-102 retains the exact expected/reported values, output, exits and fixture digests.

6. [obs] Exact candidate census bytes were restored after each score by checking out 7186722b8eba243439c6724766bdae2ef13c595c in the scratch clone. Every pristine and restored census SHA-256 is 7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5. The VERSION 2 counter SHA-256 before and after every variant remains 7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1. The four variants remain reachable on scratch-only branches; the worktree is restored. No lane source, sibling source or counter was edited, and no background job, service, delegation or installation was started. All launched foreground commands returned.
Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K06FsReaderOnly-lifecycle.json:9-12,50,77; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K07NaivePac-lifecycle.json:9-12,50,77; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K10LiveEtc-lifecycle.json:9-12,50,77; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/K11NoPairing-lifecycle.json:9-12,50,77; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/commands.json. The prescribed receipt runner created and removed its own temporary sandbox clones and homes; counter fixtures used this seat's TMPDIR.

Scope: read=godspeed/shokunin rules, candidate declaration/redesign, lane QUALITY, VERSION 2 docstring/PREDICATE/BATTERY and runner, four wave-1 reports/patches/receipts, generated seat evidence, assigned census path views; wrote=/fast/scratch/hyaku/tsukuroi-r35/W2RescoreB/, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB/, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreB.md, plus prescribed runner-managed temporary clones/homes removed by the runner; executed=timeout-bounded df -h /fast, mkdir, read-only lane git diff --stat, isolated git clone/checkout/remote set-url/apply/add/commit/rev-parse/diff, twelve detect-one.py runs, four run-receipt.py runs of score-pacnew-arm-r35b.py --skip-battery, and Python evidence assembly
Model: openai-codex/gpt-6.1-sol
Installs: none
