VERDICT: falsifies

# Seat C1ExecPriorB — item C1-6 (kill rule: the three predecessor counters B)

Kill-rule clause checked, verbatim (`SCORECARD.md:2979`, C1 row, last cell): "any of these census counters
goes PASS → FAIL base → measured revision: `score-census-readers-r45.py`, `score-scrub-arm-r44.py`,
`score-bootinputs-r43.py`, `score-size-invariance-r42.py`, `score-selftest-mounts-r41.py`,
`score-selftest-literals-r40.py`, `score-storage-hidden-r39.py`, `score-storage-arm-r38-q82.py`,
`score-pacnew-arm-r35b.py`, `score-census-handoff-r32.py` (this list is the whole kill universe …)".

**The clause fires.** Two of my three counters hold; `score-selftest-literals-r40.py` goes PASS (base
`2042117c`) → FAIL (implementation `a4477049`), reproduced twice, with exactly one predicate term moving:
`selfref` 5 → 17. The cause is the round-46 C1 feature itself: the `--identity` implementation and its
selftest add 12 net census lines that the r40 counter's own self-read regex matches. Nothing else in that
counter's predicate changed (baseline PASS, neutrals 3/3, mutants 9/9 applied, survivors 0).

## 1. Results

| counter (byte-identical at base and impl) | @ base `2042117c` | @ impl `a4477049` | changed predicate field |
|---|---|---|---|
| `tools/score-size-invariance-r42.py` | **PASS**, exit 0 | **PASS**, exit 0 | none (`cases` 10, `invariant` 10, `ns_invariant` 3, `selftest_pass` 1, `default_equal` 1) |
| `tools/score-selftest-mounts-r41.py` | **PASS**, exit 0 | **PASS**, exit 0 | none (`baseline_pass` 1, `neutral_pass` 3, `decoy_pass` 1, `mutants_applied` 13, `survivors` 0, `params` 4) |
| `tools/score-selftest-literals-r40.py` | **PASS**, exit 0 | **FAIL**, exit 1 | **`selfref` 5 → 17** (predicate: `… and selfref == 5`) |

Receipts (run through `tools/run-receipt.py`, header/body/footer JSONL, `tool_revision` = `revision` on
every leg):

| receipt | verdict line | exit | window (UTC) |
|---|---|---|---|
| `…/C1ExecPriorB/score-size-invariance-r42-2042117c.jsonl:2` | `"verdict": "PASS"` | 0 (`:3`) | 05:23:06 → 05:26:23 |
| `…/C1ExecPriorB/score-size-invariance-r42-a4477049.jsonl:2` | `"verdict": "PASS"` | 0 (`:3`) | 05:35:19 → 05:36:05 |
| `…/C1ExecPriorB/score-selftest-mounts-r41-2042117c.jsonl:345` | `"result": "PASS"` | 0 (`:348`) | 05:26:28 → 05:32:54 |
| `…/C1ExecPriorB/score-selftest-mounts-r41-a4477049.jsonl:344` | `"result": "PASS"` | 0 (`:347`) | 05:36:07 → 05:40:58 |
| `…/C1ExecPriorB/score-selftest-literals-r40-2042117c.jsonl:128` | `"result": "PASS"` | 0 (`:131`) | 05:32:56 → 05:35:17 |
| `…/C1ExecPriorB/score-selftest-literals-r40-a4477049.jsonl:128` | `"result": "FAIL"` | 1 (`:131`) | 05:41:00 → 05:43:02 |
| `…/C1ExecPriorB/score-selftest-literals-r40-a4477049-rerun.jsonl` | `"result": "FAIL"` | 1 | 05:44:5x → 05:48:23 |

(`…` = `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-46/w1`. File hashes in
`…/C1ExecPriorB/sha256sums.txt`: r40 base `8fed2c2a…`, r40 impl `41ed0cbe…`, r40 impl rerun `f1ca6f10…`,
r41 base `1e12f57a…`, r41 impl `8ffbcc13…`, r42 base `2a43d302…`, r42 impl `3fc3dcda…`.)

Commands (one counter at a time, serial, `--scratch` under my scratch; `checks.txt` §B has the loop verbatim):

```
python3 tools/run-receipt.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
  --revision <REV> --timeout 1800 --out <seat dir>/<counter>-<rev8>.jsonl \
  -- tools/<counter>.py --revision '{rev}' --scratch /fast/scratch/hyaku/tsukuroi-r46/C1ExecPriorB/s
```

The three counters are byte-identical at both revisions (`git rev-parse <rev>:tools/<file>`; `checks.txt`
§A: r42 `bf7c16bd…`, r41 `6351197f…`, r40 `38e955b2…` at base **and** impl), and each receipt header
carries the same `tool_sha256` on both legs (`c511104a…`, `8306d999…`, `8b06de18…`) — so each pair isolates
the census bytes. The census is *not* identical: `tools/tsukuroi-census.sh` blob `f129a18e…` at base vs
`412d0a4f…` at impl (+117/−4, hunks `@@455 @@594 @@605 @@3383+66 @@3388+38 @@3391 @@3393 @@3407+8`), and
`2042117c` is an ancestor of `a4477049`, so the comparison is non-vacuous.

## 2. Changed fields, per counter (full body deep-diff, base vs impl)

- **r42 (PASS → PASS).** Only non-predicate fields move: the per-run random `token`
  (`d5bff5cca395` → `d6533440ae84`) and the `ns_cases` N1/N3/N6 texts that embed it;
  `selftest_label` `"PASS (154 cases, 154 passed, 0 failed)"` → `"PASS (160 cases, 160 passed, 0 failed)"`
  (`:2` of both receipts). `non_invariant` is `[]` on both. Verdict-bearing fields identical.
- **r41 (PASS → PASS).** Every run label's case count moves 154 → 160 (`baseline.cases`,
  `baseline_labels`, each mutant/neutral/decoy `cases`), and one mutant row's failure *set* differs:
  `M3-VC-substring-btrfs` `fail_count` 2 → 1 with `first_fails` changing from a systemd-user-bus flake
  (`FAIL blocked: systemd user bus unreachable …`) plus the intended label, to the intended label alone
  (`FAIL healthy: btrfs in the device, mountpoint or options of an ext4 line is no btrfs mount (R40-C1) …`).
  It is killed on both legs, and the predicate terms are unchanged: `mutants_applied` 13, `survivors` 0,
  `decoy_pass` 1, `params` 4, `baseline_pass` 1, `neutral_pass` 3.
- **r40 (PASS → FAIL).** Predicate terms: `selfref` **5 → 17** (`-2042117c.jsonl:18` `"selfref": 5,` vs
  `-a4477049.jsonl:18` `"selfref": 17,`); `baseline_pass` 1, `neutral_pass` 3, `mutants_applied` 9,
  `survivors` 0 unchanged; `result` PASS → FAIL, `exit` 0 → 1. (Case-count labels also move 154 → 160, a
  field the predicate does not read.)

## 3. Why r40 fails — the round-46 C1 feature trips the round-40 self-read guard

The frozen predicate is `baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0
and selfref == 5` (`tools/score-selftest-literals-r40.py:162`), where `selfref` counts census lines matching
`SELFREF_RE = \$\{?SELF|BASH_SOURCE|\$0\b|/proc/self/(exe|fd)|/proc/\$\$` (`:53`) against the frozen base
count `SELFREF_BASE = 5` (`:54`). Re-computing that regex with my own code over the committed censuses gives
5 matches at `2042117c` and **17** at `a4477049` — the same numbers the two receipts report, so the failing
term is a pure function of the file bytes, not load. The second run
(`score-selftest-literals-r40-a4477049-rerun.jsonl`) reproduced `result FAIL`, `selfref 17`, exit 1.

The 12 net new matching lines (snapshot `…/C1ExecPriorB/census-at-a4477049.sh`, sha256 `d925839c…`; base
snapshot `census-at-2042117c.sh`, `237b21c9…`) are all in the `--identity` selftest and function, i.e. after
the `:3383` anchor the declaration pins:

```
tools/tsukuroi-census.sh:3394  planes=$(grep -E "^  printf 'TSUKUROI_CENSUS: %s \(" "$SELF" | …)
tools/tsukuroi-census.sh:3406  id_abs=$(readlink -f -- "$SELF")
tools/tsukuroi-census.sh:3409  cp -- "$SELF" "$idd/copy.sh"
tools/tsukuroi-census.sh:3412  { cat -- "$SELF"; printf '# decoy\n'; } > "$idd/dec/bash"
tools/tsukuroi-census.sh:3413  id_self_want=$(id_line "$SELF")
tools/tsukuroi-census.sh:3416  id_out=$("$BASH" "$SELF" --identity 2>&1); id_rc=$?
tools/tsukuroi-census.sh:3440  { printf 'mv -f -- "$R46_DECOY" "$R46_PATH"\n'; cat -- "$SELF"; } > "$idd/repl.sh"
tools/tsukuroi-census.sh:3441  { cat -- "$SELF"; printf '\n# decoy\n'; } > "$idd/repl.decoy"
tools/tsukuroi-census.sh:3459  # … re-opened as /proc/$$/fd/<n>,
tools/tsukuroi-census.sh:3460  # … only when that descriptor resolves to the same file as $SELF …
tools/tsukuroi-census.sh:3469  self_real=$(readlink -f -- "$SELF" 2>/dev/null || true)
tools/tsukuroi-census.sh:3471  for p in "/proc/$$/fd/255" /proc/$$/fd/*; do
```

plus the in-place modification at `:455` (`SELF=${BASH_SOURCE[0]}` → `SELF=${BASH_SOURCE[0]:-}`), which
replaces one already-matching base line (hence +12 on a base of 5, from 13 new matching texts).

This is a collision between two frozen artifacts, not a slip in the mutants: the r40 guard exists to refuse
a selftest that reads its own file, while the declared C1 target *requires* the same script to locate and
re-hash its own executing bytes (`/proc/$$/fd/<n>`) and its selftest to exercise that path. It is not
strictly unsatisfiable — `${0}` and `"/proc/""$$""/fd"` would not match `SELFREF_RE` — but a count-preserving
form would have to obfuscate the very self-path it must read, i.e. evade the guard instead of satisfying its
intent, and would not have produced the behaviour the C1 counter scores. As frozen, the clause is triggered
by the natural implementation.

## 4. Not run / limits

- I ran exactly these three counters (plus the r40 rerun). I did **not** run the other kill-universe
  counters (`score-census-readers-r45`, `score-scrub-arm-r44`, `score-bootinputs-r43`,
  `score-storage-hidden-r39`, `score-storage-arm-r38-q82`, `score-pacnew-arm-r35b`,
  `score-census-handoff-r32`), the C1 claim counter, the live-census line-shape/exit comparison, or
  `check-adjacency-anchors`; those are other seats' items. Nothing here says whether the rest of the kill
  universe holds.
- I did not rerun r42/r41 at impl a second time; their verdict fields are identical on both legs and no
  predicate term moved, so no flake hypothesis is under test there.
- **Recorded, not acted on:** the lane worktree at seat time held an uncommitted
  `tools/tsukuroi-census.sh` (blob `fedfd73a…`, differing from `a4477049`'s `412d0a4f…`: `|| true` on the
  `planes=` grep, a new `O_CLOEXEC` held-descriptor selftest case, comment names seat `C1LabUlimit`). Its
  `SELFREF` count is 20. All measurements above are pinned to the revisions through `run-receipt`'s
  sandbox clone and `git show <rev>:…`, never to the worktree, so they are unaffected — but if that edit
  lands, the census selftest case count moves again (my receipts read 160) and r40 stays FAIL.
- Host guard: no PACMAN, no service/unit/sysfs/boot action, no `btrfs` or `systemctl` mutation, no sudo; the
  lane's worktree, index and jj state untouched; no git commit/stash/checkout anywhere; scratch
  `/fast/scratch/hyaku/tsukuroi-r46/C1ExecPriorB` removed after the receipts were copied here.

## 5. Proposed text (SCORECARD kill-rule row / LOG)

> Kill rule, seat C1ExecPriorB (item C1-6), base `2042117c` → implementation `a4477049`: **fired.**
> `score-selftest-literals-r40.py` PASS at base (`selfref` 5, exit 0,
> `.ufo/waves/round-46/w1/C1ExecPriorB/score-selftest-literals-r40-2042117c.jsonl:128`) → FAIL at the
> implementation (`selfref` 17, exit 1, `…-score-selftest-literals-r40-a4477049.jsonl:128`; reproduced by
> `…-a4477049-rerun.jsonl`); every other predicate term unchanged (baseline_pass 1, neutral_pass 3,
> mutants 9/9 applied, survivors 0). Cause: the `--identity` selftest/function add 12 net census lines
> matching the round-40 `SELFREF_RE` (`tools/score-selftest-literals-r40.py:53`, pinned at 5 by `:54`/`:162`),
> all after `tools/tsukuroi-census.sh:3383` (`:3394,:3406,:3409,:3412,:3413,:3416,:3440,:3441,:3459,:3460,
> :3469,:3471`). The other two: `score-size-invariance-r42.py` PASS → PASS (cases 10, invariant 10,
> ns_invariant 3, default_equal 1) and `score-selftest-mounts-r41.py` PASS → PASS (13/13 applied, survivors 0,
> decoy 1, params 4).

Report path: `.ufo/waves/round-46/w1/C1ExecPriorB.md`
Receipts: `.ufo/waves/round-46/w1/C1ExecPriorB/` (`checks.txt`, `sha256sums.txt`, seven `.jsonl` receipts,
`census-at-2042117c.sh`, `census-at-a4477049.sh`).
