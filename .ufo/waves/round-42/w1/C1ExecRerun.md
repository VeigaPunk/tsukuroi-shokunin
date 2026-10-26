VERDICT: supports

# Seat C1ExecRerun — item C1-1 (C1 after re-run at the implementation commit)

Post-receipt today 2026-10-26T19:41Z from `/home/vgpnk/Projects/shokunin`, scratch
`/fast/scratch/hyaku/tsukuroi-r42/C1ExecRerun` (removed after copying the receipt).

## 1. Frozen counter identity (freeze blob == worktree == receipt header)

```
$ git -C <lane> show a84fc9dec860f8bea516dff7ddfdc98223cdae52:tools/score-size-invariance-r42.py | sha256sum
c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03  -
$ sha256sum <lane>/tools/score-size-invariance-r42.py
c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-size-invariance-r42.py
```

Declared `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`: identical on all
three surfaces (freeze blob, working file, and `tool_sha256` in the receipt header,
`.ufo/waves/round-42/w1/C1ExecRerun/c1-after-4476620.jsonl:1`). The verdict below is therefore
produced by the frozen counter, not by a mutated copy. The base receipt carries the same
`tool_sha256` (`.ufo/waves/round-42/before/c1-before.jsonl:1`), so before/after are the same oracle.

## 2. The single run (item order, once, no re-run)

```
$ TMPDIR=/fast/scratch/hyaku/tsukuroi-r42/C1ExecRerun python3 <lane>/tools/run-receipt.py \
    --revision 447662088dfd3155e31aed239179a79c1d1046c7 \
    --tool-revision a84fc9dec860f8bea516dff7ddfdc98223cdae52 \
    --out <lane>/.ufo/waves/round-42/w1/C1ExecRerun/c1-after-4476620.jsonl \
    -- tools/score-size-invariance-r42.py --revision '{rev}' \
       --scratch /fast/scratch/hyaku/tsukuroi-r42/C1ExecRerun/s
{"out": ".../w1/C1ExecRerun/c1-after-4476620.jsonl", "revision": "447662088dfd3155e31aed239179a79c1d1046c7",
 "tool": "tools/score-size-invariance-r42.py", "exit_code": 0}
RC=0
```

Wall: started `2026-10-26T19:41:06Z`, finished `2026-10-26T19:41:50Z` (~44 s), `timed_out: false`,
`stderr_tail: ""` (`c1-after-4476620.jsonl:1` and `:3`). The lane's guidance estimated 1–3 min; the
observed cost was lower, which makes the FAIL→PASS delta no artifact of a truncated run.

## 3. Every field of the after receipt (line 2 of the JSONL)

| field | value |
|---|---|
| `counter` | `score-size-invariance-r42` |
| `revision` | `447662088dfd3155e31aed239179a79c1d1046c7` |
| `base` | `c8efaa3f120834541f8de1e5e0367e8d1593bae6` |
| `cases` | `10` |
| `invariant` | `10` |
| `non_invariant` | `[]` |
| `ns_invariant` | `3` |
| `ns_cases` | `N1: {invariant: true, stderr_tail: ""}`, `N3: {invariant: true, stderr_tail: ""}`, `N6: {invariant: true, stderr_tail: ""}`; in all three the large and small `PLANE packages:` lines are byte-identical and both carry this run's token |
| `per_case` | `P1 true (rc 2/2), P2 true (rc 2/2), P3 true (rc 2/2), P4 true (rc 1/1), P5 true (rc 0/0), P6 true (rc 2/2), U1 true (rc 1/1), U2 true (rc 1/1), U3 true (rc 1/1), U4 true (rc 0/0)` — `large_lines_not_in_small: []` in every case, and `large_rc == small_rc` in every case |
| `selftest_label` | `PASS (130 cases, 130 passed, 0 failed)` |
| `selftest_pass` | `1` |
| `selftest_rc` | `0` |
| `default_equal` | `1` |
| `token` | `ec527c084b31` |
| `predicate` | `cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1` |
| `verdict` | `PASS` |

Predicate arithmetic re-evaluated independently from the receipt's own numbers:
`10==10, 10==10, 3==3, 1==1, 1==1` → all true, so `verdict: PASS` is consistent with the declared
predicate (`c1-after-4476620.jsonl` line 2). Receipt footer: `exit_code: 0`.

Freshness: the run token `ec527c084b31` appears in both twins of each namespace leg (checked
programmatically: `tok_in_large True, tok_in_small True, large==small True` for N1/N3/N6), and it
differs from the base run's `fabb57cdf218` — the N legs cannot be a cached or replayed answer.
Observed N lines are the fixed verdict, not the round-41 wrong one:
`PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: alpha: /usr/bin/x-ec527c084b31 (Permission denied); root_status=ok …` (300 chars, identical for small and 1 MiB large twin).

## 4. Comparison with `.ufo/waves/round-42/before/c1-before.jsonl` (base c8efaa3f)

| field | before (`c1-before.jsonl`, base) | after (`c1-after-4476620.jsonl`, 4476620) |
|---|---|---|
| `verdict` | `FAIL` | `PASS` |
| receipt footer `exit_code` | `1` | `0` |
| `cases` | 10 | 10 |
| `invariant` | 3 | 10 |
| `non_invariant` | `["P1","P3","P6","U1","U2","U3","U4"]` | `[]` |
| `per_case` failures | P1 F, P3 F, P6 F, U1 F, U2 F, U3 F, U4 F (P2/P4/P5 true) | all 10 true |
| `ns_invariant` | 0 | 3 |
| `ns_cases` | N1 F, N3 F, N6 F | N1 T, N3 T, N6 T |
| `selftest_label` | `PASS (128 cases, 128 passed, 0 failed)` | `PASS (130 cases, 130 passed, 0 failed)` |
| `selftest_pass` / `selftest_rc` | 1 / 0 | 1 / 0 |
| `default_equal` | 1 | 1 |
| `token` | `fabb57cdf218` | `ec527c084b31` |
| `revision` | `c8efaa3f…` | `4476620…` |
| `tool_revision` | `a84fc9de…` | `a84fc9de…` |
| `tool_sha256` | `c511104a…` | `c511104a…` |

The exact defect the declaration names is reproduced at base and removed at the implementation
commit: at base, the packages/update-safety planes give a *different verdict at 1 MiB* (P1/P3/P6,
U1–U4 non-invariant) and every production-path leg fails on the merged `-Qkk` sample
(base N1 small = `BLOCKED (sample probe error)` vs large = `DEGRADED … foreign=21(known=3 new=5
drift=13 gone=0)`, i.e. the R41 read-an-error-line-as-HEALTHY family); at 4476620 the same twins
agree byte for byte.

## 5. Corroborating checks I ran (cheap, read-only on the lane)

- Census under test: `git show 4476620:tools/tsukuroi-census.sh | sha256sum` =
  `46d62a24709ece8efbcd231f4c269bd5b3791237e3c78ac7433fb0115494f1b1` = worktree census = `HEAD`
  census, so the receipt's `--revision` names exactly the file that ships.
- Selftest case count reconciles with the claim “128 → 130 cases”: base census has
  `125` `check ` + `3` `check_cli ` invocations = 128; implementation census has `127` + `3` = 130
  (the +2 are the two `R42-C1` checks at `tools/tsukuroi-census.sh:2357` and `:2564`).
- Diff hunk placement against the C1 kill rule (supporting, not my judgement call): for
  `git diff -U0 c8efaa3f 4476620 -- tools/tsukuroi-census.sh` the hunks at 692 and 697 sit inside
  `probe_packages()` (opens at line 654), those at 1624/1638/1644/1655 inside
  `probe_update_safety()` (opens at 1552), and the two new-case hunks at 2350/2556 inside
  `run_selftest()` (opens at 1931, its closing `}` at 3107 — brace-depth 20 at both lines), so no
  hunk lands outside the three functions the kill rule permits.
- The implementation commit's own able-to-fail note
  (`git show 4476620:.ufo/waves/round-42/impl/c1-able-to-fail.txt`) records the hybrid
  (implementation selftest + base `probe_packages`/`probe_update_safety`) failing both new cases
  (one `exit 0` where 2 was wanted, one `exit 141`) and the implementation passing. I read that
  note; I did **not** re-run it — my item asked only for the single frozen-counter receipt.

## 6. Lane state observed while measuring (context, not a finding of mine)

- Receipt header records `refs/heads/master 87c4f7c627e377e5f6d361498e8db9b3886d7953` at run time;
  the base receipt recorded `refs/heads/master a84fc9de…`. The measured revision is named
  explicitly and `git merge-base --is-ancestor 4476620… 87c4f7c6…` → true, so the verdict is pinned
  to the implementation commit either way. `HEAD` is detached at `87c4f7c6…`.
- Untracked lane files (`.ufo/waves/round-42/w1/`, `w1.ready*`, `w2-context.txt`,
  `corpus/lessons/round-42.md`, `.ufo/waves/round-42/make-w2-spec.py`) exist from other seats; I
  wrote only my own seat directory and this report.

## 7. Checks I did not run (so: not passed)

- Did not run `tools/tsukuroi-census.sh --selftest` standalone; `selftest_pass: 1` is the counter's
  own invocation at the pinned revision (receipt line 2), which is the declared measurement.
- Did not run the C2 counter, the control batteries, any mutant or any `--lane <fixture>` variant —
  out of scope for C1-1 and other seats hold them.
- Did not run the `score-selftest-mounts-r41.py` kill-rule check, the hunk-scope judgement, or any
  SCORECARD/LOG edit (L1 integrates).
- No tool installed or upgraded this seat: nothing needed (python3/git/unshare were sufficient).

## 8. Proposed text (drop-in for the L1's C1 after row)

> C1 after re-run (C1ExecRerun): counter `tools/score-size-invariance-r42.py` sha256
> `c511104a…` identical at freeze `a84fc9de`, in the worktree, and in the receipt header; one run
> via `run-receipt.py --revision 4476620… --tool-revision a84fc9de…` produced
> `.ufo/waves/round-42/w1/C1ExecRerun/c1-after-4476620.jsonl` (exit 0, 19:41:06Z→19:41:50Z):
> `cases 10, invariant 10, non_invariant [], ns_invariant 3 (N1/N3/N6), selftest_label "PASS (130
> cases, 130 passed, 0 failed)", selftest_pass 1, default_equal 1, verdict PASS`, token
> `ec527c084b31` present in both twins of every N leg. Against `before/c1-before.jsonl` (base
> `c8efaa3f`): `FAIL → PASS`, `invariant 3 → 10`, `non_invariant [P1,P3,P6,U1,U2,U3,U4] → []`,
> `ns_invariant 0 → 3`, selftest 128 → 130 cases, token `fabb57cdf218 → ec527c084b31`.
