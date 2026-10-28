VERDICT: supports

# C1-X12 — independent do-nothing control (base blob at 5fdf062f) and the cosmetic-count falsifier

Seat: TExecBaseControl. Counters used verbatim from the working tree, which I verified is byte-identical to the
freeze: `sha256sum tools/score-selftest-tmpdir-r48.py` = `8eead161e990e9e6f5155984797396d79fe7a3e6524a1a0c3087758658625640`,
equal to FROZEN.md's C1-counter row and to `git show ae99f021…:tools/score-selftest-tmpdir-r48.py` (receipt
`TExecBaseControl/counter-bytes.txt`, which also re-hashes the frozen census blob at 375aa737…f3a76e2426;
`git status --porcelain` on the two C1 files printed nothing).
Base blob read via `git -C <lane> show 5fdf062f969292736e36513e39f98b1b8de43635:tools/tsukuroi-census.sh` →
sha256 `adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41`, which is the `census_sha256` recorded in the
committed K0 receipt line, so the control and my replay measured the same bytes. Frozen blob also extracted:
`375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426` (matches FROZEN.md).

## 1. Replay of the do-nothing control (one counter run)

Command (run once, 277 s wall):

```
mkdir -p /fast/scratch/hyaku/tsukuroi-r48/TExecBaseControl/{w,generic-tmp}
TMPDIR=/fast/scratch/hyaku/tsukuroi-r48/TExecBaseControl/generic-tmp \
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-selftest-tmpdir-r48.py \
  --revision 5fdf062f969292736e36513e39f98b1b8de43635 \
  --work /fast/scratch/hyaku/tsukuroi-r48/TExecBaseControl/w
```

Observed legs (`TExecBaseControl/base-k0.json`):

| leg | replay | committed K0 (`controls/battery-summary-r48-c1.jsonl` line 1) |
|---|---|---|
| pass_ok | 0 | 0 |
| loc_ok | 3 | 3 |
| clean_ok | 4 | 4 |
| failfast_ok | 1 | 1 |
| term_ok | 0 | 0 |
| static_ok | 0 | 0 |
| verdict | FAIL | FAIL |
| census_sha256 | adb1b4ce…32ce41 | adb1b4ce…32ce41 |

All six legs and the verdict match the committed receipt exactly; `as_expected: true` in the receipt is reproduced.
Per-scenario detail from my run (same file):

- unset / tmp / scratch: rc 0, one fixture creation each, real parent `/tmp`, `/tmp`, `<work>/tmp-plain`; last line
  `TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`.
- spaced: rc 0, one creation, real parent **`/tmp`** (not the spaced TMPDIR) → `loc_ok` 0 for that scenario.
  Cause: `census-base.sh:2055` `local st_base=${TMPDIR:-/tmp}` and `:2057` `*[!A-Za-z0-9._/+-]*) st_base=/tmp ;;`
  — a TMPDIR with a space is refused and replaced by `/tmp`, then `:2059` builds there.
- failfast `missing-spaced`: rc **0**, one fixture creation, PASS line printed → leg red; `missing-plain`: rc 1,
  no creation, no PASS → leg green (hence 1/2).
- term: rc **1** (not 143), no PASS line, `fixture_removed: true` → leg red. `census-base.sh:2062` installs one
  cleanup handler on `EXIT INT TERM`; it removes the tree but never exits, so a SIGTERM run continues until later
  steps fail (rc 1). Only the 143 status contract is missing; cleanup itself survives.
- static: red for two independent reasons — `2057: *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;` (matched by the counter's
  `BASE_ASSIGN` `\w*base\w*=/tmp`) and the literal usage/comment promise at `census-base.sh:412` and `:602`
  ("…, or /tmp itself when TMPDIR …"). Re-derived with the counter's own `static_leg()` in-process
  (`TExecBaseControl/static-leg-recompute.json`): base `ok 0`, problems as above; the frozen blob scores
  `ok 1` with `problems []`.

So the item's stated expectation is confirmed and completed: base = `pass_ok 0` (164 vs the counter's 166),
`loc_ok 3`, `term_ok 0`, `static_ok 0`, plus `clean_ok 4` and `failfast_ok 1`.

## 2. Is the target reachable by a cosmetic count edit? — No.

One-edit mutant: copy of the base blob with only the summary counters raised by 2, so the printed line claims 166
(`TExecBaseControl/mutant-m166.diff`, exactly one changed line):

```
-    "$([ "$FAIL" -eq 0 ] && printf PASS || printf FAIL)" "$((PASS + FAIL))" "$PASS" "$FAIL"
+    "$([ "$FAIL" -eq 0 ] && printf PASS || printf FAIL)" "$((PASS + FAIL + 2))" "$((PASS + 2))" "$FAIL"
```

Mutant sha256 `3eb8727dbc02f72fe6fd9a0e8da34f3287d488a1eaa8bee01d0244525ff6b103`. Counter run (one, 397 s wall):

```
python3 …/tools/score-selftest-tmpdir-r48.py --census /fast/scratch/hyaku/tsukuroi-r48/TExecBaseControl/mutant/census-m166.sh \
  --work /fast/scratch/hyaku/tsukuroi-r48/TExecBaseControl/w2
```

Observed (`TExecBaseControl/mutant-k166.json`): `pass_ok 4, loc_ok 3, clean_ok 4, failfast_ok 1, term_ok 0,
static_ok 0` → **verdict FAIL**. Delta against the base replay is exactly `{"pass_ok": [0, 4]}`; every other leg is
unchanged. All four scenarios now print `PASS (166 cases, 166 passed, 0 failed)` with rc 0 (so the count edit buys
`pass_ok`, nothing else), while the spaced scenario still creates its fixture with real parent `/tmp`, `missing-spaced`
still exits 0 with a PASS line and a `/tmp` fixture, the SIGTERM leg still ends rc 1 (not 143; fixture removed), and
`static_leg` still reports the same two problems.

Leg-by-leg reason a count edit cannot carry them (frozen contrast, `census-frozen.sh`):

- `loc_ok` needs the spaced-TMPDIR fixture in the *real* TMPDIR: requires `selftest_base_dir()` (`:2058`) and its
  `/proc/self/fd/24x` alias over `base=${TMPDIR:-/tmp}` (`:2074`). Base has only the `/tmp` substitution at `:2057`.
- `failfast_ok` needs a nonexistent TMPDIR to refuse: requires the `[ -d "$base" ] || return 1` arm inside
  `selftest_base_dir` and the `run_selftest` guard that returns 1 without invoking mktemp (`:2100-2106`). Base has
  no such guard, so a nonexistent *spaced* TMPDIR becomes `/tmp` and builds.
- `term_ok` needs status 143: requires the split traps `trap 'exit 130' INT` / `trap 'exit 143' TERM` (`:2110-2111`)
  beside the EXIT-only cleanup (`:2109`). Base's single EXIT/INT/TERM handler cannot produce 143.
- `static_ok` is a pure text property of the blob (assignment pattern and usage wording); a count edit by
  construction leaves both hits in place (`census-base.sh:2057`, `:412`, `:602`).

Conclusion: the case count is necessary but not sufficient. A base blob with only the count raised to 166 still
fails **loc_ok, failfast_ok, term_ok and static_ok** (the item's three plus `failfast_ok`), i.e. 4 of 6 legs and the
predicate; the C1 target needs the mechanism change (alias-based base resolution, fail-fast guard, 130/143 traps,
fallback text removal), not a cosmetic edit. The K0 control therefore discriminates: it is red for substantive
reasons, and the frozen fix revision is the only row of the committed battery that reaches PASS
(`battery-summary-r48-c1.jsonl` line 5).

## 3. Hygiene

- Two counter invocations total (one base replay, one mutant), run sequentially, never concurrently; each with its
  own `--work` under `/fast/scratch`; no selftest run outside the counter.
- Receipts: `.ufo/waves/round-48/w2/TExecBaseControl/{base-k0.json,mutant-k166.json,mutant-m166.diff,
  static-leg-recompute.json,blob-sha256.txt}`.
- Scratch `/fast/scratch/hyaku/tsukuroi-r48/TExecBaseControl/` removed after the receipts were copied
  (free space seen before the runs: 546 G on /fast; no ENOSPC).
- No lane/fleet file written, no git or jj mutation anywhere (only `git show`/`status` reads), no tool installed or
  upgraded, no subagent spawned, nothing written under /tmp by me (the census's own /tmp fixtures are the observed
  object, cleaned by the harness — `clean_ok 4`, `fixture_removed: true`).
- Not done: no attempt to run the frozen fix revision through the counter (out of scope; K-pass already covers it),
  no review of C2/C3, no third mutant variant.
