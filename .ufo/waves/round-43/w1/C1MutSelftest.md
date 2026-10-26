VERDICT: defect-found

# C1-9 — which of the C1-8 helper mutants (a)–(h) do the three R43-C1 selftest cases kill?

Item: same mutants as C1-8 (a)–(h) (mutant list at `.ufo/waves/round-43/make-w1-spec.py:72`), scored by the
717b716a8943151ace8657e0ca23d7d9b8434f26 script's own `--selftest`; for each survivor propose an exact extra
`st_check` case, red on the mutant and green on 717b716, and run both.

Method: single-site mutations applied to scratch copies of
`tools/boot-chain-audit.sh` at 717b716 (`git show 717b716…:tools/boot-chain-audit.sh` → pristine, 1320 lines,
sha256 `3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74`); detector = the mutated script's own
`--selftest` (`run_selftest` :885, `st_check` :824-833, R43-C1 block :1225-1237), `TMPDIR` in scratch. The lane
was never written; every byte lived in `/fast/scratch/hyaku/tsukuroi-r43/C1MutSelftest/` (removed at end,
receipts copied to this dir). No tools installed (tooling authorization unused; no pacman/uv/npm calls).

## Baseline (pristine 717b716)

`TMPDIR=$S bash pristine-bca.sh --selftest` → `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=48 failed=0`, rc=0
(receipt `baseline-selftest.out`). 48 = 45 legacy + 3 R43-C1 cases. A baseline failure would have made every
mutant run inconclusive; it passed, so all verdicts below are valid kills/survivals.

Environment (receipt `env.txt`, `find-probes.out`): bash 5.3.20; find = GNU findutils 4.11.0-modified at
`/usr/bin/find` (child bash `command -v find` → `/usr/bin/find`; the omp session shell's `type -a find`
reporting "shell builtin" is a session-wrapper artifact, not what the script's child bash resolves).
`/proc/stat` mtime 1793052459, btime 1793027300.

## Per-mutant results

Site lines are 717b716 numbering: find line :469, decision :470, production list :494-496.
Receipts `mut-<x>-selftest.out`; sha256 of every mutated script in `mutant-sha256.txt`.

| mut | site | selftest | verdict |
|---|---|---|---|
| (a) `-n`→`-z` | :470 | FAIL total=48 failed=3, rc=1 | **killed by all three R43-C1 cases** |
| (b) drop `-quit` | :469 | PASS total=48 failed=0, rc=0 | **survives** (output-equivalent) |
| (c) drop `2>/dev/null` | :469 | PASS total=48 failed=0, rc=0 | **survives** (stderr channel) |
| (d) `\| head -n1` | :469 | PASS total=48 failed=0, rc=0 | **survives** (output-equivalent) |
| (e) drop /etc/crypttab | :494 | PASS total=48 failed=0, rc=0 | **survives** (list unexercised) |
| (f) drop /usr/lib/modules | :496 | PASS total=48 failed=0, rc=0 | **survives** (list unexercised) |
| (g) `-newermt`→`-newer /proc/stat` | :469 | FAIL total=48 failed=2, rc=1 | **killed** by `R43-C1-missing-start-point-deep-newer` + `R43-C1-all-present-deep-newer` |
| (h) decide on find's exit status | :470 | FAIL total=48 failed=1, rc=1 | **killed** by `R43-C1-missing-start-point-deep-newer` |

Attribution is clean: every FAIL line in every mutant receipt is an `R43-C1-*` case; no legacy case failed in
any run.

Kill mechanisms (probes in `find-probes.out`, GNU find 4.11.0-modified):
- (a): each case's expectation is inverted, so all three fail (`expected [0] got [1]` / `expected [1] got [0]` ×2).
- (g): the epoch argument is ignored; the anchor becomes `/proc/stat`'s mtime (1793052459), which is ≫ the
  fixture epochs 1000/2000/3000, so the @3000 file is no longer "newer" and cases 2–3 read 0. Case 1 still
  passes. The kill holds on any host booted after 1970-01-01T00:50Z; on a hypothetical host with an earlier
  `/proc/stat` mtime, case 1 would fail instead — still killed.
- (h): interpretation of "print 1 when find's exit status is 0 else output test" = decision line :470
  `if [ -n "$hit" ]` → `if [ $? -eq 0 ]` immediately after the `hit=$(find …)` assignment (`$?` is find's
  status). GNU find prints the match **and exits 1** when an earlier start point is missing (probe P1:
  match printed, `rc=1`; P2 no-match `rc=1`; P3 same without `-quit` `rc=1`), so in case 2 the status-based
  decision reads 0 where the output-based decision reads 1. Caveat: this kill depends on find preserving the
  error status through `-quit`; a find that exits 0 on `-quit` would make (h) output-equivalent.

## Survivors

- **(b) drop `-quit` (:469) — output-equivalent, not a coverage gap.** The decision reads only find's stdout
  non-emptiness; `-quit` changes how many entries find lists (first vs all), never whether one is listed;
  find's exit status is unused. Battery (`runner.sh`, 8 shapes: missing×{none,deep,top-newer}, all-present×2,
  unreadable mode-000 dir×2, match-first-then-missing): `equiv-pristine.out` vs `equiv-b.out` → diff
  IDENTICAL (all 8 lines `0/1` equal).
- **(d) `| head -n1` (:469) — output-equivalent, not a coverage gap.** With `-quit` retained find emits ≤1
  line and `head -n1` passes it through; the pipefail substitution status is unused. Battery:
  `equiv-d.out` diff IDENTICAL.
- **(c) drop `2>/dev/null` (:469) — real selftest blind spot: stderr.** `mut-c-selftest.out` lines 1–2 show
  two `find: '…/bootinputs/missing': No such file or directory` lines emitted during the legacy R43-C1 cases,
  which still pass because `st_check` compares stdout only (:824-833). Production effect: stderr noise during
  live audits whenever an optional start point is missing; stdout/verdicts unchanged.
- **(e) drop /etc/crypttab (:494) — real host-behaviour regression the selftest cannot see.** A newer
  /etc/crypttab would again read as "none newer" — the original fail-open scoped to that input. The selftest
  is structurally blind: in fixture mode `boot_inputs_newer` returns `$BOOTCHAIN_FIXTURE/boot_inputs_newer`
  (:478-489) and never touches the list; non-fixture mode reads the real host /etc (non-hermetic).
- **(f) drop /usr/lib/modules (:496) — same as (e)** for the modules tree (kernel package updates while up).

## Proposed extra `st_check` cases (insert after :1237, before the `if [ "$st_fail" -eq 0 ]` at :1239)

All five inserted together into a pristine copy pass (`green-all-selftest.out`: `PASS total=53 failed=0`,
rc=0); each is red on its mutant (`red-<x>-selftest.out`, each `FAIL total=49 failed=1`, rc=1, failing exactly
the new case).

1. For (c) — behavioural, stderr quiet on a missing start point:
```bash
    got=$(inputs_newer_than 2000 "$bi/missing" 2>&1)
    st_check 'R43-C1-missing-point-stderr-quiet' 0 "$got"
```
red: `FAIL R43-C1-missing-point-stderr-quiet: expected [0] got [find: '…/bootinputs/missing': No such file or directory\n0]` (find's stderr, unbuffered, precedes the function's `0`).

2. For (e) — hermetic source guard (no behavioural case exists without a mount namespace; the behavioural
kill for list mutants is the frozen counter's job):
```bash
    got=$(declare -f boot_inputs_newer | grep -c -- '/etc/crypttab')
    st_check 'R43-C1-production-list-includes-crypttab' 1 "$got"
```
red: `expected [1] got [0]`.

3. For (f) — same shape:
```bash
    got=$(declare -f boot_inputs_newer | grep -c -- '/usr/lib/modules')
    st_check 'R43-C1-production-list-includes-modules' 1 "$got"
```
red: `expected [1] got [0]`.

4. For (b) — source guard, implementation-pinning only (the mutant is output-equivalent, so no
fixture-driven case can be red on it; adopt only if pinning the `-quit` is wanted):
```bash
    got=$(declare -f inputs_newer_than | grep -c -- '-quit')
    st_check 'R43-C1-helper-early-quit-present' 1 "$got"
```
red: `expected [1] got [0]`.

5. For (d) — source guard, same caveat:
```bash
    got=$(declare -f inputs_newer_than | grep -c -- 'head -n1')
    st_check 'R43-C1-helper-no-head-truncation' 0 "$got"
```
red: `expected [0] got [1]`.

## Findings for the integrator

- The three R43-C1 cases kill exactly the decision-site mutants: (a) inversion, (g) anchor swap, (h)
  status-vs-output. They do not kill (c), (e), (f): stderr quietness and production-list membership are
  outside the selftest's hermetic reach (fixture mode bypasses the list; `st_check` compares stdout only).
  List-mutant behavioural kills remain the frozen counter's job (its namespace cases over /etc and
  /usr/lib/modules); the guards in 2–3 close the text-level gap if the selftest should pin the list.
- (b)/(d) are equivalent mutants — not coverage gaps; do not count them against the selftest.
- Not done: scoring these mutants with the frozen counter `tools/score-bootinputs-r43.py` (that is item
  C1-8's detector, sibling seat C1MutFix); no cross-check against `C1MutFix.md` (not published at write
  time). No `--live` run, no host mutation, no sudo.

## Restoration evidence

All mutations lived in scratch copies; the lane file was never opened for writing. Read-only checks:
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain -- tools/boot-chain-audit.sh` →
empty; `git -C … diff 717b716a… -- tools/boot-chain-audit.sh | wc -l` → 0 (commands and outputs in
`restoration.txt`). `pristine-bca.sh` sha256 identical before and after all experiments
(`3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74`, last line of `mutant-sha256.txt`).
Scratch dir removed after copying receipts.

## Receipts (this dir)

`baseline-selftest.out`, `mut-{a..h}-selftest.out`, `red-{b,c,d,e,f}-selftest.out`, `green-all-selftest.out`,
`equiv-{pristine,b,d}.out`, `find-probes.out`, `env.txt`, `mutant-sha256.txt`, `restoration.txt`,
`runner.sh`, `fn-{pristine,mut-b,mut-d}.sh`, and the exact scored bytes: `pristine-bca.sh`,
`mut-{a..h}.sh`, `red-{b,c,d,e,f}.sh`, `green-all.sh`.
