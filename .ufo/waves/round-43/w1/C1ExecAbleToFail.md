VERDICT: supports

# C1-3 — the 717b716 fix is able to fail

Item: build a hybrid of the 717b716a8943151ace8657e0ca23d7d9b8434f26 script whose
`inputs_newer_than` body uses the base pipeline, run its `--selftest` (expect exactly one
failure: `R43-C1-missing-start-point-deep-newer`, expected [1] got [0]) and score it with the
frozen C1 counter, reporting correct/wrong.

Everything below was run in this session; nothing was written in the lane except this report
and the receipt dir `.ufo/waves/round-43/w1/C1ExecAbleToFail/`. Lane HEAD stayed
`7d0ed1c2d62961cbde8a4d6be120b2573ebbd8f9`; `git -C <lane> status --porcelain` shows only
pre-existing untracked `.ufo/waves/round-43/w1*` paths.

## 0. Baseline identity

- Script under test is byte-identical at the declared fix and at the current lane tip:
  `git show 717b716a:tools/boot-chain-audit.sh | sha256sum` and
  `git show 7d0ed1c2:tools/boot-chain-audit.sh | sha256sum` both print
  `3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74`; working-tree file same
  hash. The tip commit only added receipts (`.ufo/waves/round-43/after/...`).
- Frozen counter hash matches the declaration:
  `sha256sum tools/score-bootinputs-r43.py` →
  `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f`.
- Shape at the fix (`tools/boot-chain-audit.sh`): `set -uo pipefail` at :139; helper
  `inputs_newer_than` :463-475 (fix body: `hit=$(find "$@" -newermt "@$epoch" -print -quit
  2>/dev/null)` at :469, decision `if [ -n "$hit" ]` at :470); `boot_inputs_newer` :477-496
  calling the helper with the same eight production start points at :494-496; gate
  `newer=$(boot_inputs_newer)` at :758 fed into
  `if [ "${kernels[i]}" = 1 ] && [ "${sels[i]}" = true ] && [ "$newer" = 0 ] && …` at :769-772;
  the three `R43-C1-*` cases at :1232, :1235, :1237.

## 1. The hybrid

Scratch clone per the seat rule: `git clone -q --shared <lane> $S/fx.W4UhxC`,
`git -C "$D" remote remove origin`, `git -C "$D" rev-parse --show-toplevel` printed `$D`
(TOPLEVEL_OK) before the first commit. Only the `inputs_newer_than` body was replaced — no
other function, no other line. Diff (`$D/tools/boot-chain-audit.sh` vs 7d0ed1c2; receipt
`C1ExecAbleToFail/hybrid.diff`):

```diff
--- i/tools/boot-chain-audit.sh
+++ w/tools/boot-chain-audit.sh
@@ -461,13 +461,9 @@ btime_epoch() {
 }
 
 inputs_newer_than() { # <epoch> <start point>... -> 1 when find lists an entry newer than epoch, else 0
-    # R43-C1: decide on find's output, never on its exit status. find exits 1 when a start
-    # point is missing or a directory is unreadable; under `set -o pipefail` that status used
-    # to mask a listed match (`find … | grep -q .`), so a newer input read as "none newer".
-    local epoch=$1 hit
+    local epoch=$1
     shift
-    hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)
-    if [ -n "$hit" ]; then
+    if find "$@" -newermt "@$epoch" -print -quit 2>/dev/null | grep -q .; then
         printf '1\n'
     else
         printf '0\n'
```

`git diff --stat`: `tools/boot-chain-audit.sh | 8 ++------` (2 insertions, 6 deletions).
Hybrid script sha256 `6711a49192d8138b438a10e0cd00fc6eebb9e4df37bb4663a138d82252906614`.
Committed in the fixture with `git -C "$D" -c user.name=fixture -c user.email=fixture@invalid
commit -m "hybrid C1: …" -- tools/boot-chain-audit.sh` → `da42f52037d8791221a55689041b605d4e39c601`.
(The change stays inside the declared kill rule's permitted function, so a counter that only
rejected text drift could not produce the result below.)

## 2. Hybrid `--selftest`: exactly one failure, the R43-C1 case

Command: `TMPDIR=$S/tmp bash "$D/tools/boot-chain-audit.sh" --selftest`.

Observed (complete output, 2 lines — receipt `hybrid-selftest.out`):

```
FAIL R43-C1-missing-start-point-deep-newer: expected [1] got [0]
TSUKUROI_BOOTCHAIN_SELFTEST: FAIL total=48 failed=1
```

Exit status 1. Total 48 matches the fix's 48 cases (`TSUKUROI_BOOTCHAIN_SELFTEST: PASS
total=48 failed=0` in `.ufo/waves/round-43/after/c1-after-717b716.jsonl`), so the hybrid adds
and removes no case; exactly the one new case that pins the masking trips, and
`R43-C1-missing-start-point-none-newer` (:1232) and `R43-C1-all-present-deep-newer` (:1237)
still pass. Nothing else fails.

## 3. Hybrid scored by the frozen counter

Command: `python3 <lane>/tools/score-bootinputs-r43.py --lane "$D" --revision
da42f52037d8791221a55689041b605d4e39c601 --scratch "$S/s"` (scratch in
`/fast/scratch/hyaku/tsukuroi-r43/C1ExecAbleToFail/`; TMPDIR exported there).

Observed JSON (receipt `hybrid-counter.out`), exit 1:

```
cases = 16
correct = 8
wrong = [{"expect":"1","got":"0","id":"miss/etc/fstab-newer","rc":0},
         {"expect":"1","got":"0","id":"miss/etc/crypttab-newer","rc":0},
         {"expect":"1","got":"0","id":"miss/etc/mkinitcpio.conf-newer","rc":0},
         {"expect":"1","got":"0","id":"miss/etc/mkinitcpio.conf.d-newer","rc":0},
         {"expect":"1","got":"0","id":"miss/etc/default/limine-newer","rc":0},
         {"expect":"1","got":"0","id":"miss/etc/limine-snapper-sync.conf-newer","rc":0},
         {"expect":"1","got":"0","id":"multi-miss-deep-modules-newer","rc":0},
         {"expect":"1","got":"0","id":"unreadable-dir-modules-newer","rc":0}]
identity_ok = 1
live = {"expect": "0", "got": "0", "rc": 0}
live_agree = 1
selftest_pass = 0
selftest_line = "TSUKUROI_BOOTCHAIN_SELFTEST: FAIL total=48 failed=1"
selftest_failures = ["FAIL R43-C1-missing-start-point-deep-newer: expected [1] got [0]"]
selftest_r43 = 3
verdict = "FAIL"
```

correct = **8 / 16**, wrong = **8 / 16** — every wrong case is an expect-1-then-got-0
fail-open (a missing start point or an unreadable directory, with a newer input listed after
it in find's argument order). All eight older/no-match cases stay correct, so the hybrid is
wrong in exactly the direction the defect describes, not merely noisy.

## 4. Same-session three-state comparison

| state | revision | cases correct | wrong ids | selftest | verdict |
|---|---|---|---|---|---|
| base (declared before receipt) | `6951ead9` | 8/16 | the same 8 ids, all `…-newer` => 0 | — | FAIL |
| **hybrid (this session)** | `da42f520` (fixture) | 8/16 | **identical 8 ids, all `-newer` => 0** | FAIL total=48 failed=1 | FAIL |
| fix (re-scored this session) | `717b716a` | 16/16 | none | PASS total=48 failed=0 | PASS |

- Base row source: `.ufo/waves/round-43/before/c1-before.jsonl` (line 2: `revision
  6951ead90566…`, `cases 16 correct 8`, wrong ids `miss/etc/fstab-newer:0` …
  `unreadable-dir-modules-newer:0`, `verdict FAIL`). The hybrid's wrong set is name-for-name
  identical to the base's — the base defect reproduced by the helper body alone, with the fix's
  comment, helper signature and call sites still in place.
- Fix row re-scored in this session with the same frozen counter:
  `python3 <lane>/tools/score-bootinputs-r43.py --lane <lane> --revision
  717b716a8943151ace8657e0ca23d7d9b8434f26 --scratch "$S/s2"` → `correct 16`, `wrong []`,
  `selftest_line PASS total=48 failed=0`, `verdict PASS`, exit 0 (receipt `fix-counter.out`).
  Read-only through `git show`; nothing in the lane changed.
- Differential is therefore causal: the only variable between FAIL 8/16 and PASS 16/16 is the
  helper body, and the same counter, selftest and host round trip produce both.

## 5. Causal micro-repro (why one case fails and not others)

Fixture `$S/micro/bi`: `missing` absent, `old` @1000, `d/sub/f` @3000 (deep newer than 2000),
`d` and `d/sub` @1000. Under `set -uo pipefail`:

```
find stdout=[bi/d/sub/f] find_rc=1
grep_rc=0
pipeline=FALSE
```

find *did* list the newer entry and grep *did* match, but find's exit 1 (missing start point)
makes the pipeline false under pipefail. Sourcing a `main`-stripped lib and calling the helper
directly on the same tree:

```
hybrid inputs_newer_than -> [0] (expected 1)
fixed  inputs_newer_than -> [1] (expected 1)      # same tree, lane lib
```

Mapping to the gate: this 0 becomes `newer=0` at :758 and satisfies `[ "$newer" = 0 ]` at :770,
so `booted=1` → BOOTED-OBSERVED while an input was newer — the declared fail-open, reproduced
end to end from the helper body.

## 6. Notes, limits, risks

- `live_agree` stayed 1 in both runs (`live expect 0 got 0`): on this host today no boot-chain
  input is newer than btime, so the L leg does **not** discriminate the defect. The
  fix-able-to-fail evidence rests on the 8 namespace cases and the selftest leg; the live leg
  only certifies the fix does not regress the quiet-host answer. [INFERENCE] On a host that had
  just regenerated an initramfs before boot this leg would also diverge; not tested (it would
  need a host mutation, forbidden here).
- The hybrid is a scoring fixture, not a proposal: `da42f520` exists only in the scratch clone
  and the clone is removed at exit. Nothing was committed, staged or checked out in the lane,
  and no lane Git/jj state was touched.
- `selftest_pass = 0` independently fails the hybrid counter predicate, so the hybrid fails
  twice over (cases 8/16 and S leg). That is the expected shape: the fix's own regression test
  and the production-path cases agree on the defect.
- Not run (out of scope for this item): the round-42 C1 counter and the census selftest (no
  claim of mine depends on them), the K7 mount-table-gated channel (declared open, unchanged
  by a helper-body edit), and the C2 counter (different claim).
- Tooling: no install or upgrade was performed; nothing outside `/fast/scratch/…` and the
  report/receipt paths was written.

## 7. Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/w1/C1ExecAbleToFail/`:
`hybrid.diff`, `hybrid-selftest.out`, `hybrid-counter.out`, `fix-counter.out`,
`PROVENANCE.txt` (revisions, shas, exact commands). Scratch
`/fast/scratch/hyaku/tsukuroi-r43/C1ExecAbleToFail/` was removed after copying.
