DOES NOT MEET the C1 after-value: K15 base reference and unpaired-log-regex each candidate_matches=1/of=24; K16 chmod-restore and touch-log each candidate_matches=0/of=24; every harness_errors=[] and exit=1.

1. [obs] Exactly one committed receipt was scored for each of the four assigned variants with VERSION 2 and --skip-battery. No assigned variant reaches VERSION 2, so these re-scores produce no control-meets finding against C1. This is not a judgment of the full C1 claim. The axes exercised were coverage, control sensitivity and restoration integrity.

| Control | VERSION 1 result from w1 receipt | VERSION 2 candidate_matches/of | Exit | Dominant reason |
|---|---|---|---:|---|
| K15-base-reference | 24/24; exit 0 | 1/24 | 1 | field mismatch (23 views) |
| K15-unpaired-log-regex | 24/24; exit 0 | 1/24 | 1 | field mismatch (23 views) |
| K16-chmod-restore | 6/24; exit 1 | 0/24 | 1 | fixture mutated (23 views) |
| K16-touch-log | 0/24; exit 1 | 0/24 | 1 | fixture mutated (23 views) |

Every old and new receipt has harness_errors=[]. Evidence for each table row follows.
- [obs] K15-base-reference: VERSION 1 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/base-reference.jsonl:27-28; VERSION 2 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K15-base-reference.jsonl:27-28. The outer process, summary and receipt footer all report exit 1 for VERSION 2; the receipt footer reports timed_out=false.
- [obs] K15-unpaired-log-regex: VERSION 1 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/pacnew-log-without-backreference.jsonl:27-28; VERSION 2 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K15-unpaired-log-regex.jsonl:27-28. The outer process, summary and receipt footer all report exit 1 for VERSION 2; the receipt footer reports timed_out=false.
- [obs] K16-chmod-restore: VERSION 1 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K16ChmodRestore/chmod-restore.jsonl:27-28; VERSION 2 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K16-chmod-restore.jsonl:27-28. The outer process, summary and receipt footer all report exit 1 for VERSION 2; the receipt footer reports timed_out=false.
- [obs] K16-touch-log: VERSION 1 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K16ChmodRestore/touch-log.jsonl:27-28; VERSION 2 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K16-touch-log.jsonl:27-28. The outer process, summary and receipt footer all report exit 1 for VERSION 2; the receipt footer reports timed_out=false.

2. [obs] Each saved full .patch was applied unchanged onto 7186722b8eba243439c6724766bdae2ef13c595c in the isolated W2RescoreD clone and committed there. The required read-only command `timeout 30 git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --stat 6b4561e4 7186722b8eba243439c6724766bdae2ef13c595c -- tools/tsukuroi-census.sh` exited 0 with empty stdout: the two candidates have identical census bytes. All four resulting census SHA-256 values equal their respective VERSION 1 receipt headers. Full rebased patches sit beside their new receipts. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/preparation.json:1; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/commands.json:1.

Every VERSION 2 counter header has counter_sha256=7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1. The receipt wrapper tool_sha256 agrees, tool_revision is 7186722b8eba243439c6724766bdae2ef13c595c, and battery=false. The counter was not edited.

| Control | New committed revision | Header census_sha256 |
|---|---|---|
| K15-base-reference | c3c6756164de5b7e8aa5de3b96d09af41a95734d | 991c2c522486bf6f5cee686ff4b5bb439a8da206714c5d6e0d6595bcb628fcdd |
| K15-unpaired-log-regex | 48fed6c51ecc9b2b9f486b924bba7fe066970cd1 | 08094373ca75a93ed323070175466359cb47fe1cce4fe5df54ac538b83f46777 |
| K16-chmod-restore | 2136a1bed854ebe45f8c43eb6bbab86c61398561 | 42c8cae2148ad853041d92a839e91b7114f906ee5287786e6112229dee31ab56 |
| K16-touch-log | 33f56334b5eb9338874ac9561643f9ab66879ec6 | 2f6dbb661df6adafc80467f08fddf3c5c287dc92820705bed179b48e8145ddc4 |

- [obs] K15-base-reference header: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K15-base-reference.jsonl:1-2. Saved source patch: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/base-reference.patch:1. Rebased patch: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K15-base-reference.patch:1.
- [obs] K15-unpaired-log-regex header: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K15-unpaired-log-regex.jsonl:1-2. Saved source patch: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/pacnew-log-without-backreference.patch:1. Rebased patch: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K15-unpaired-log-regex.patch:1.
- [obs] K16-chmod-restore header: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K16-chmod-restore.jsonl:1-2. Saved source patch: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K16ChmodRestore/chmod-restore.patch:1. Rebased patch: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K16-chmod-restore.patch:1.
- [obs] K16-touch-log header: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K16-touch-log.jsonl:1-2. Saved source patch: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K16ChmodRestore/touch-log.patch:1. Rebased patch: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/K16-touch-log.patch:1.

3. [obs] Below are the counter's literal per-view reasons. The two K15 controls match only live. Both K16 controls are refused for fixture mutation in all 23 synthetic views and for no drift line in live. All 23 synthetic census exits are 2. The live census exit is 2 for K15 and 1 for K16; these are subprocess exits, distinct from every score's exit 1. `null` means that view matched.

| View | K15 base reference | K15 unpaired-log-regex | K16 chmod-restore | K16 touch-log |
|---|---|---|---|---|
| stub-00 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-01 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-02 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-03 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-04 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-05 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-06 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-07 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-08 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-09 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-10 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-11 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-12 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-13 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-14 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-15 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-16 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-17 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-18 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| stub-19 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| ns-20 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| ns-21 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| ns-22 | field mismatch | field mismatch | fixture mutated | fixture mutated |
| live | null | null | drift_lines=0 | drift_lines=0 |

[obs] For each column, stub-00 through ns-22 are receipt lines 3-25, and live is line 26 in its receipt named above. The exhaustive machine-readable view ledger is /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/view-reasons.jsonl:1-96; complete expected/reported dictionaries, revisions and original/new summaries are retained in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/results.json:1.

4. [obs] The old reference itself does not satisfy the redesigned oracle: in every synthetic view it reports log_pacnew exactly one above expected. The unpaired regex reports log_pacnew two above expected and gone one above expected. Both K16 variants also report log_pacnew one above expected in those views; their reported reason is fixture mutated because the unchanged judge gives mutation precedence. Evidence: the four new receipts:3-25; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/probe-verdicts.json:1.

[obs] VERSION 2 restricts counted warning sources to /etc/ (counter docstring lines 33-34 and oracle lines 205-212), while the saved wave-1 reference regex accepts any correctly paired source (original base-reference.patch:20). [inf] The forced paired /usr/share/ event in every VERSION 2 fixture explains the reference's +1; the forced directory-mismatched pair explains the unpaired mutant's additional +1 and gone +1. Source evidence: /fast/scratch/hyaku/tsukuroi-r35/W2RescoreD/repo/tools/score-pacnew-arm-r35b.py:296-299; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/base-reference.patch:20; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/pacnew-log-without-backreference.mutation.patch:9-10. Because this reference fails the full VERSION 2 counter, its full-counter comparison alone is inconclusive as an isolated regex-mutant kill. It is still an observed rejection of both scored variants; the original patch was not repaired or replaced.

5. [obs] To satisfy the pristine/mutated/restored mutation contract without scoring any listed revision twice, a supplementary 20-second-bounded literal stub view ran VERSION 2's unchanged harness, snapshot, ctimes, run and judge functions on each defect before mutation, after mutation and after exact restoration. It contains one directory-mismatched installed-as event, paired /etc/ events, three unreadable modes (000, 300, 100), and no non-/etc event. Its independently literal expected dictionary is pacnew=1 pacsave=1 pacorig=1 unreadable=3 log_pacnew=4 log_pacsave=1 unlogged=1 gone=1. It checks other-output/exit parity with the claim-base census as VERSION 2 specifies. This probe is not a 24-view receipt, not a battery run, and not the C1 measure. Evidence: /fast/scratch/hyaku/tsukuroi-r35/W2RescoreD/restoration-probe.py:1; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/restoration-probes.jsonl:1-9.

| Defect | Pristine | Mutated output | Restored | Literal-detector verdict |
|---|---|---|---|---|
| K15 unpaired-log-regex | matches=true | matches=false; field mismatch; log_pacnew=5, gone=2 | matches=true | killed |
| K16 chmod-restore | matches=true | matches=false; fixture mutated; three directory ctimes changed | matches=true | killed |
| K16 touch-log | matches=true | matches=false; fixture mutated; only log ctime changed | matches=true | killed |

[obs] All nine literal-probe census exits are 2, all timed_out=false, and all claim-base exits are 2. In the chmod and touch probes, expected and reported fields agree, snapshot bytes/modes are unchanged, and the ctime changes alone cause refusal. The K16 pristine arm was the original touch-log arm with only its touch command removed; its SHA-256 is the same correct-pristine digest recorded in the wave-1 K16 report. Three-phase hash evidence follows.

| Defect | Pristine SHA-256 | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|---|
| K15-unpaired-log-regex | 991c2c522486bf6f5cee686ff4b5bb439a8da206714c5d6e0d6595bcb628fcdd | 08094373ca75a93ed323070175466359cb47fe1cce4fe5df54ac538b83f46777 | 991c2c522486bf6f5cee686ff4b5bb439a8da206714c5d6e0d6595bcb628fcdd |
| K16-chmod-restore | 16a7c5b36ea0eafdeeda3871ac4d0c95937acb90ee8364b90af3bbf91df42836 | 42c8cae2148ad853041d92a839e91b7114f906ee5287786e6112229dee31ab56 | 16a7c5b36ea0eafdeeda3871ac4d0c95937acb90ee8364b90af3bbf91df42836 |
| K16-touch-log | 16a7c5b36ea0eafdeeda3871ac4d0c95937acb90ee8364b90af3bbf91df42836 | 2f6dbb661df6adafc80467f08fddf3c5c287dc92820705bed179b48e8145ddc4 | 16a7c5b36ea0eafdeeda3871ac4d0c95937acb90ee8364b90af3bbf91df42836 |

[obs] Each mutated file also retained its same SHA-256 across detector execution. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/restoration-probes.jsonl:1-9; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/probe-restorations.json:1; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/probe-verdicts.json:1. No mutant survived the supplementary literal detector, and no literal baseline/restoration failed. Those limited kills do not promote the failing old reference into a passing full VERSION 2 positive control.

6. [obs] Restoration is exact. The isolated clone census SHA-256 was 7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5 on entry, after each saved patch was committed and removed from the worktree, and at the final restoration. The scratch probe is restored to its K16 pristine digest 16a7c5b36ea0eafdeeda3871ac4d0c95937acb90ee8364b90af3bbf91df42836. The final unchanged counter digest is 7517af92e0c9308c10f04b90d05a699cfa56278a736ef975d97ba08fbd957dc1. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/preparation.json:1; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/probe-restorations.json:1. Push URL was disabled before sandbox writes. No lane source, counter, corpus, fleet state or sibling clone was changed.

7. [obs] Exactly four official --skip-battery scores and nine supplementary literal detector executions ran; no full battery, build, lint, selftest, external source fetch or package transaction ran. Every directly launched subprocess was synchronous and timeout-wrapped, and completed. No background job, service or persistent process was started. The scoring runner's own disposable clones and fixtures were managed by its existing finally cleanup. Actual argv and captured command exits/stdout/stderr are in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/commands.json:1; official invocation outcomes are in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/invocations.json:1. These findings do not alter the contract or integrate/ship any code.

Report: .ufo/waves/round-35/w2/W2RescoreD.md
Scope: read=godspeed and shokunin instructions, operator tool rules, candidate declaration/redesign, lane QUALITY, unchanged counter and receipt runner, assigned w1 reports/patches/receipts and resulting w2 receipts; wrote=/fast/scratch/hyaku/tsukuroi-r35/W2RescoreD/**, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/**, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD.md; executed=timeout-wrapped df/mkdir, read-only lane git show/diff, isolated clone git checkout/remote/apply/add/commit/rev-parse/show/diff, sha256sum, four run-receipt.py --skip-battery commands and nine literal restoration-probe.py commands; exact scoring and probe argv in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w2/W2RescoreD/commands.json
Model: openai-codex/gpt-6.1-sol
Installs: none
