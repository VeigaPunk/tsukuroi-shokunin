VERDICT: supports

# C1FinalRerun — item F-1: frozen C1 counter re-run at the integration commit

Seat: L2 leaf, round 42 wave w2. Item F-1 only. Lane content read-only; nothing outside my seat dir and
`/fast/scratch/hyaku/tsukuroi-r42/C1FinalRerun/` was written; no pacman, no service, no host mutation; no
subagents (leaf). Lane HEAD when I started: `a968393c678171f8a5a2907da5015735396da4cc` (the after-receipt
commit on top of the dispatched tip `78abb8b5`); I ran against `78abb8b5` exactly as the item specifies.

## 1. Frozen counter digest — verified

`tools/score-size-invariance-r42.py` at the freeze commit `a84fc9dec860f8bea516dff7ddfdc98223cdae52`:

```
$ git -C …/tsukuroi-shokunin show a84fc9de…:tools/score-size-invariance-r42.py | sha256sum
c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03  -
```

Matches the declared digest `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03` exactly. Same
digest at `78abb8b5`, at HEAD `a968393c`, and in the worktree — the instrument did not move between the freeze,
the integration commit, and now (`…/w2/C1FinalRerun/digest-and-binding.txt`, lines under "counter digest").
The receipt header agrees: `"tool_sha256": "c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03"`.

## 2. The run

Exactly the item's command, run once from the fleet root with a scratch dir under the sanctioned path
(`…/w2/C1FinalRerun/c1-final.jsonl`; 45 s wall, `user 2m39s`):

```
python3 …/tools/run-receipt.py --revision 78abb8b5… --tool-revision a84fc9de… \
  --out …/.ufo/waves/round-42/w2/C1FinalRerun/c1-final.jsonl \
  -- tools/score-size-invariance-r42.py --revision '{rev}' --scratch /fast/scratch/hyaku/tsukuroi-r42/C1FinalRerun/s
{"out": "…/c1-final.jsonl", "revision": "78abb8b5cdc9da511b4fc523e661517a68dd33d3",
 "tool": "tools/score-size-invariance-r42.py", "exit_code": 0}
```

Footer of the receipt: `{"receipt_end": 1, "exit_code": 0, "timed_out": false, "stderr_tail": "",
"finished_utc": "2026-10-26T20:31:04Z"}` — started `2026-10-26T20:30:20Z`. The tool ran from a `--no-local`
sandbox clone of the lane checked out at the tool revision, and the census **under test** is read from
`--revision` (`tools/score-size-invariance-r42.py:308`, `rev_src = git_show(a.lane, rev, CENSUS)`), i.e. the
census at `78abb8b5`, not the base.

## 3. Every predicate field

Frozen predicate (receipt field `predicate`, identical string in the declaration):
`cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1`.

| Predicate field | This run | Holds |
|---|---|---|
| `cases` | 10 | yes |
| `invariant` | 10 | yes |
| `ns_invariant` | 3 | yes |
| `selftest_pass` | 1 (`selftest_rc` 0, `selftest_label` `PASS (132 cases, 132 passed, 0 failed)`) | yes |
| `default_equal` | 1 | yes |

Conjunction holds → counter `verdict: "PASS"`, process exit 0. Full payload, no interpretation:
`base: c8efaa3f…`, `revision: 78abb8b5…`, `non_invariant: []`, `ns_cases: {N1: true, N3: true, N6: true}`,
`token: 7600ae82f5ff`.

Per-case (all `invariant: true`, `large_lines_not_in_small` empty in every case, large/small exit codes equal):

```
case P1 P2 P3 P4 P5 P6 U1 U2 U3 U4
rc   2  2  2  1  0  2  1  1  1  0        (large_rc == small_rc for all ten)
excess lines: 0 for all ten
```

Production-path legs (real `unshare -rm` path, no `TSUKUROI_*` override), per run token `7600ae82f5ff`: N1, N3,
N6 — `large == small` byte-for-byte and the token present in **both** twins (`token in both: True/True` for each),
so no cached or replayed answer can account for the pass.

## 4. Comparison with the earlier receipts

Prior after receipt: `…/.ufo/waves/round-42/after/c1-after-78abb8b.jsonl` (present). Before receipt:
`…/.ufo/waves/round-42/before/c1-before.jsonl`. Machine copy: `…/w2/C1FinalRerun/field-compare.json`.

| Field | this run @78abb8b5 | after @78abb8b5 | before @c8efaa3f |
|---|---|---|---|
| `cases` | 10 | 10 | 10 |
| `invariant` | 10 | 10 | 3 |
| `non_invariant` | `[]` | `[]` | `[P1,P3,P6,U1,U2,U3,U4]` |
| `ns_invariant` | 3 | 3 | 0 |
| `selftest_pass` / `selftest_rc` | 1 / 0 | 1 / 0 | 1 / 0 |
| `selftest_label` | `PASS (132 cases, 132 passed, 0 failed)` | same | `PASS (128 cases, 128 passed, 0 failed)` |
| `default_equal` | 1 | 1 | 1 |
| `verdict` | PASS | PASS | FAIL |
| `token` | `7600ae82f5ff` | `7fd8303f03e6` | `fabb57cdf218` |

- **This run == after on every named field** (`cases, invariant, non_invariant, ns_invariant, selftest_pass,
  selftest_rc, selftest_label, default_equal, verdict, predicate` → all `true`), `per_case` dictionaries equal,
  and the `ns_cases` payloads are equal after normalising each run's own token (mine vs after: `large=True,
  small=True` for N1, N3, N6). Independent run, independent token, same result.
- **This run differs from before exactly where the fix acts**: `invariant` 3 → 10, `ns_invariant` 0 → 3,
  `non_invariant` seven pairs → none, `selftest_label` 128 → 132 cases, verdict FAIL → PASS. The pre-fix failure
  signature is the declared defect, not noise: before, U1–U4 exited **141** on the large twin
  (`large_rc=141` vs `small_rc=1/1/1/0` — the SIGPIPE kill) and P1/P3/P6 answered **HEALTHY** on the large twin
  where the small twin said BLOCKED (`large_rc=0` vs `small_rc=2`, 4 excess `PLANE` lines). At `78abb8b5` all
  ten pairs have matching exit codes and zero excess lines.
- `default_equal` is 1 in all three receipts, so the counter's clean-default agreement with the base census is
  not a round-42 side effect.

## 5. Revision binding and reachability

- Receipt `revision` = `78abb8b5cdc9da511b4fc523e661517a68dd33d3`, `tool_revision` =
  `a84fc9dec860f8bea516dff7ddfdc98223cdae52`, `base` = `c8efaa3f120834541f8de1e5e0367e8d1593bae6` — the three
  revisions the claim names. Header `lane_branches` records `refs/heads/master a968393c…` at run time, i.e. the
  lane moved one commit past the measured revision during the wave, not before it.
- The C1 fix commit is in the measured history: `git merge-base --is-ancestor 44766208… 78abb8b5…` →
  `is-ancestor: yes`.
- The census the receipt measures is the integrated one: sha256 `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9`
  at `78abb8b5`, at HEAD and in the worktree; `git diff --stat 78abb8b5… a968393c… -- tools/` prints nothing,
  so no `tools/` change landed between the measured commit and lane HEAD. The measured object is what is live.
- The early reader the claim names is the awk full-read form at `tools/tsukuroi-census.sh:692-700` (rev
  `78abb8b5`; awk statement at `:698`, verdict note `:700`): `err_line=$(printf '%s\n' "$s_out" | awk
  '/^error:/ { if (!p) { print; p = 1 } } END { if (!p) exit 1 }')` and the comment stating no early-exiting
  reader and no here-string on a probe buffer; plus
  `:746` the full-read baseline lookup `awk -v n="$nm" '$1 == n && !f { print $2; f = 1 }'` (was `… {print $2;
  exit}`, which the same commit replaced because an awk `exit` under pipefail killed the census on a large
  baseline).

## 6. Notes, risks, what I did not do

- **Claim wording vs integrated mechanism (not a measurement defect).** The dispatch/claim text calls the fix
  "here-strings; awk NR", which describes commit `44766208`; wave-1 integration replaced the packages-site
  here-strings with the awk full read (`git diff 44766208… 78abb8b5… -- tools/tsukuroi-census.sh`, hunk at
  `@@ -691,10 +691,13 @@`, reason in-code: a >64 KiB here-string is a temporary file, breaking the no-write
  contract, round-42 wave-1 C1RevFix D1). The declaration row of record (`SCORECARD.md:2573`) does not name
  here-strings, so the frozen text is not contradicted; a reader of the dispatch should look for awk, not a
  here-string. Wave 1 already flagged that the declared mechanism is not a requirement
  (`.ufo/waves/round-42/w1/ConnClaims.md:114`).
- **Bounded residual, low reachability [INFERENCE]:** `check()`'s `ABSENT:` arm at `tsukuroi-census.sh:2193`
  (rev `78abb8b5`) is a here-string over `$out`, the census's own stdout — not a 1 MiB probe buffer. The largest
  census output captured in wave 1 is 13111 B
  (`.ufo/waves/round-42/w1/C1ExecSelftest/smp-tip.out`, a 400-package sample run; `live-tip.out` 8418 B), still
  about a fifth of the 64 KiB temp-file threshold, and the 1 MiB case is a *probe buffer* that the census
  summarises rather than echoes. So D1's failure mode looks unreachable for the current 132 cases. I did not
  measure the per-case `$out` size directly.
- **Not run (so not passed by me):** no independent re-derivation of the counter's fixture twins, no ENOSPC /
  full-`$TMPDIR` simulation, no second counter run (host guard: one counter at a time), no `census --selftest`
  outside the counter's own `selftest_pass` field, no gate/lint/format execution (parent owns the post-integration
  gate). I did not read the `ns` leg internals or re-implement the unshare leg; I report only what the receipt
  states.
- **Host guard:** all work read-only on the lane; no git/jj mutation anywhere; no `unshare` or `btrfs` command of
  my own (the counter's private `unshare -rm` legs are its own); only my receipt processes signalled (none
  needed). No tool installed or upgraded this wave (`pacman` guard respected; nothing needed).
- **Receipts:** `…/w2/C1FinalRerun/c1-final.jsonl` (run-receipt JSON lines, header + payload + footer),
  `…/w2/C1FinalRerun/field-compare.json` (the three-receipt field/per-case/ns comparison),
  `…/w2/C1FinalRerun/digest-and-binding.txt` (digests at every named revision, ancestry, empty `tools/` diff).
- **Scratch:** `/fast/scratch/hyaku/tsukuroi-r42/C1FinalRerun/` removed after the receipts were copied; the
  counter and `run-receipt.py` removed their own scratch/clone trees on exit.

Bottom line: at the integration commit `78abb8b5` the frozen C1 counter (digest verified against the freeze)
reproduces `PASS` with `cases 10 / invariant 10 / ns_invariant 3 / selftest_pass 1 / default_equal 1`, an
independent run token, and field-for-field agreement with the committed after receipt, against a before receipt
whose 141s and HEALTHY-instead-of-BLOCKED pairs are exactly the declared defect.
