VERDICT: supports

Seat: C1ExecRerun (L2 executor, round 43 / hyaku run 9), item C1-1 — counter hash identity and after/before re-run of the frozen C1 counter, stability across draws. All commands run from scratch dir `/fast/scratch/hyaku/tsukuroi-r43/C1ExecRerun` with `TMPDIR` set there; the lane was read-only throughout (no git/jj mutation, no lane write outside this seat dir). Counters were run strictly one at a time.

## 1. Counter hash identity (frozen claim holds)

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show fe35700183188f7d712e2932cabde1944efca052:tools/score-bootinputs-r43.py | sha256sum
886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f  -
$ sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-bootinputs-r43.py
886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f  .../tools/score-bootinputs-r43.py
```

- Freeze-commit blob == working file == the declaration's `886f92c8…b3e10f`. No mismatch.
- Every receipt header also carries `"tool_sha256": "886f92c8…b3e10f"` (all 7 receipts), so each scored run used that same counter text from the freeze revision `fe357001`.
- Incidental, same identity discipline: `git show 717b716:tools/boot-chain-audit.sh | sha256sum` = `3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74` = `sha256sum tools/boot-chain-audit.sh` (working file still the fixed one).

## 2. Runs (per-run fields, verbatim from receipts)

Driver (all four/five/scored runs, e.g. rerun1):
`python3 <lane>/tools/run-receipt.py --revision 717b716a8943151ace8657e0ca23d7d9b8434f26 --tool-revision fe35700183188f7d712e2932cabde1944efca052 --out <receipt> -- tools/score-bootinputs-r43.py --revision '{rev}' --scratch /fast/scratch/hyaku/tsukuroi-r43/C1ExecRerun/s` (base run: `--revision 6951ead90566b2d74f7c45b4efca29246badad64`).

| receipt (in `.ufo/waves/round-43/w1/C1ExecRerun/`) | rev | cases | correct | wrong ids | identity (euid,uid,suid) | identity_ok | live (expect/got/rc) | live_agree | selftest_line | selftest_r43 | verdict | exit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c1-after-717b716-rerun1.jsonl | 717b716 | 16 | 16 | — (empty) | 1000,1000,1000 | 1 | 0/0/0 | 1 | `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=48 failed=0` | 3 | PASS | 0 |
| c1-after-717b716-rerun2.jsonl | 717b716 | 16 | 16 | — | 1000,1000,1000 | 1 | 0/0/0 | 1 | same, total=48 | 3 | PASS | 0 |
| c1-after-717b716-rerun3.jsonl | 717b716 | 16 | 16 | — | 1000,1000,1000 | 1 | 0/0/0 | 1 | same, total=48 | 3 | PASS | 0 |
| c1-after-717b716-rerun4.jsonl | 717b716 | 16 | 16 | — | 1000,1000,1000 | 1 | 0/0/0 | 1 | same, total=48 | 3 | PASS | 0 |
| c1-after-717b716-rerun5.jsonl | 717b716 | 16 | 16 | — | 1000,1000,1000 | 1 | 0/0/0 | 1 | same, total=48 | 3 | PASS | 0 |
| c1-before-6951ead-rerun1.jsonl | 6951ead | 16 | 8 | 8 (below) | 1000,1000,1000 | 1 | 0/0/0 | 1 | `…PASS total=45 failed=0` | 0 | FAIL | 1 |
| c1-before-6951ead-rerun2.jsonl | 6951ead | 16 | 8 | 8 (below) | 1000,1000,1000 | 1 | 0/0/0 | 1 | `…PASS total=45 failed=0` | 0 | FAIL | 1 |

Base `wrong` list, identical in both base runs (order as emitted):
```
miss/etc/fstab-newer            expect 1 got 0 rc 0
miss/etc/crypttab-newer         expect 1 got 0 rc 0
miss/etc/mkinitcpio.conf-newer  expect 1 got 0 rc 0
miss/etc/mkinitcpio.conf.d-newer expect 1 got 0 rc 0
miss/etc/default/limine-newer   expect 1 got 0 rc 0
miss/etc/limine-snapper-sync.conf-newer expect 1 got 0 rc 0
multi-miss-deep-modules-newer   expect 1 got 0 rc 0
unreadable-dir-modules-newer    expect 1 got 0 rc 0
```
That is exactly the declared fail-open: every case where a start point is missing (or a directory is unreadable) *and* a later-listed input is newer returns 0 at base; the six `miss<k>-older`, `all-present-newer`, `all-present-older` cases still pass, hence 8/16. `btime` 1793027300 in all seven receipts.

Scope note: the seat asked for three after runs and one base run; I ran five after and two base (extra names `-rerun4`, `-rerun5`, `c1-before-6951ead-rerun2`) to answer the stability question with more draws. No other counter was run (census selftest and round-42 C1 counter deliberately not run — not this item).

## 3. Comparison with the canonical receipts

Parsed JSON comparison against `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/after/c1-after-717b716.jsonl` and `.../before/c1-before.jsonl`:

- **Scored body line: byte-identical (as parsed dict) in every case.** All five after reruns print `b == canonical_after_body` → `True`; both base reruns print `b == canonical_before_body` → `True`. So cases/correct/wrong/identity/live/selftest/verdict match the declaration's before and after records exactly, not merely in verdict.
- Header differences are only `argv`, `lane_branches`, `started_utc`; footer difference is only `finished_utc`.
  - `argv`: canonical after used `--scratch /fast/scratch/hyaku/tsukuroi-r43/after-c1`, mine uses `/fast/scratch/hyaku/tsukuroi-r43/C1ExecRerun/s` (seat scratch). No scored effect.
  - `lane_branches`: canonical records `refs/heads/master 717b716a…`, mine records `refs/heads/master 7d0ed1c2d62961cbde8a4d6be120b2573ebbd8f9`. The lane simply advanced after the after-receipt was taken: `git -C <lane> log --oneline -1 master` → `7d0ed1c2 round-43: C1 after receipt at 717b716; w1 spec and validated dispatch`; `git merge-base --is-ancestor` confirms 6951ead, 717b716 and fe357001 are all ancestors of master. `revision`, `tool_revision`, `tool_sha256` are identical to the canonical receipts, so the difference is bookkeeping of branch tips, not of the scored revision.
  - Lane worktree HEAD is detached at `7d0ed1c2…` (`git -C <lane> rev-parse HEAD`); read-only observation, nothing written.

## 4. Stability across draws

- Randomness is genuinely per run: `tools/score-bootinputs-r43.py:289` `rng = random.Random(os.urandom(16))`, and `make_cases(rng, bt)` is called per run (`:289-290`). Fixture values are not recorded in the output, so to observe variability I imported the *frozen* module unmodified (`importlib.util.spec_from_file_location` on the lane path, module sha256 re-checked `886f92c8…`) and called `make_cases(random.Random(os.urandom(16)), btime())` five times:
  ```
  module sha256 886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f
  btime 1793027300
  draw1 n_cases=16 digest=350553d775a1ebb8
  draw2 … 4d817da34e136eec | draw3 … 4ad9927b917e25f7 | draw4 … 2a62a6fdbb9dffa9 | draw5 … 7d1bc9cbf74f9b66
  distinct draw digests: 5 of 5
  ids/expect draw-invariant: True
  ```
  So the draws really do differ (5/5 distinct fixture layouts: entry names, depths, modes, mtimes), while the 16 case ids and their expected values are fixed by construction.
- The scored verdict is invariant across those draws: 5/5 after runs PASS with identical bodies; 2/2 base runs FAIL at correct 8 with the identical 8-case wrong list. At base the 8 failures are precisely the structurally masked family (missing point / unreadable dir before a newer input in find's argument order), which cannot be repaired by a draw, so `correct == 8` at base and `16` at fix are draw-invariant — consistent with the canonical before/after pair taken on a different draw.
- Live leg: `expect 0 got 0 rc 0` in all seven runs. This leg reads the real host, so it is the one field that could legitimately vary; the host's boot-chain inputs stayed older than boot start (`btime` 1793027300) across the ~2-minute window 22:07:15Z–22:09Z 2026-10-26. A host write to `/etc`/`/usr/lib/{initcpio,modules}` during a run would flip it to expect/got 1 and is an environment change, not counter instability.

## 5. Supporting check on the fix (incidental, not a kill-rule verdict)

`git -C <lane> diff --unified=2 6951ead 717b716 -- tools/boot-chain-audit.sh` contains exactly three hunks: new `inputs_newer_than()` (fix revision `:463-474`), `boot_inputs_newer()` delegating with the same 8 paths (`:494-496`; the empty-btime branch and fixture branch untouched), and three `R43-C1-*` selftest cases in `run_selftest` (`:1232, :1235, :1237`). Line 139 is `set -uo pipefail` at both revisions; base `boot_inputs_newer` is `:463` with the pipe at `:481-483`; base gate is `:761` `[ "$newer" = 0 ]`. Consistent with the declaration text; the full kill-rule judgement belongs to the reviewer seats, and I did not run the round-42 C1 counter or the census selftest.

## 6. What I did not do

- Did not run the controls battery (`controls/C1-K*.jsonl`), the census selftest, or the round-42 C1 counter (other seats' items; also the guard's one-heavy-counter rule).
- Did not audit the working tree for unrelated edits (read-only seat; no `git status`, to avoid touching the lane index).
- No tools installed or upgraded; no host mutation; nothing written outside this seat's report, seat dir and `/fast/scratch/hyaku/tsukuroi-r43/C1ExecRerun` (scratch removed after the receipts were copied into the seat dir; the transient `run-receipt-*` dirs under `/fast/scratch/hyaku` are the driver's own and were gone at 22:09Z, none of them a `/tmp` path).

## 7. Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/w1/C1ExecRerun/` (28 KB total): `c1-after-717b716-rerun{1..5}.jsonl`, `c1-before-6951ead-rerun{1,2}.jsonl`.
