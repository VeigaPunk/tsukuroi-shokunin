VERDICT: supports

Item C1-7 — does the frozen counter refuse each single-site revert?

Question. Starting from the implementation census 447662088dfd3155e31aed239179a79c1d1046c7, revert exactly one of the six round-42 sites back to the base (c8efaa3f120834541f8de1e5e0367e8d1593bae6) text and score the variant with the frozen counter `tools/score-size-invariance-r42.py`. A variant that PASSes is a counter gap naming an uncovered site.

Answer. All six single-site reverts are refused: every variant scores FAIL (counter exit 1, predicate false). No counter gap found. The milestone "counter kills each site revert" is met.

Method (all paths absolute; scratch under /fast/scratch/hyaku/tsukuroi-r42/C1MutSites/, TMPDIR exported there, never /tmp)
- Counter identity verified before use: `sha256sum tools/score-size-invariance-r42.py` → `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03` — matches the frozen declaration.
- Per variant: `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D"`; `git -C "$D" remote remove origin`; `git -C "$D" rev-parse --show-toplevel` asserted == $D; `git -C "$D" checkout -q 44766208…`; one site reverted to the base text (drivers prep.sh/commit.sh/run.sh in the receipts dir); committed with `git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -q -am "mut <name>: single-site revert to base c8efaa3f text"`; scored with `python3 tools/score-size-invariance-r42.py --lane "$D" --revision <sha> --scratch $S/s`, one run at a time (observed run windows 19:45:48Z–19:51:04Z, 40–46 s each, no overlap).
- Pre-commit diff of each variant saved and eyeballed: exactly one hunk, exactly the reverted site (receipts m1.patch…m6.patch).

Baseline (pristine implementation, no mutation). Revision 44766208… in clone fx.base: verdict PASS, cases 10, invariant 10, non_invariant [], ns_invariant 3, selftest_pass 1 (`PASS (130 cases, 130 passed, 0 failed)`), default_equal 1, token 6d77f9636eaa, counter_rc=0 (base.json). The detector is sound at the implementation, so the mutant verdicts below are conclusive.

Results (per variant: verdict / invariant / non_invariant / ns_invariant; site lines given base-side per the claim, impl-side in today's worktree census, blob ed83079c at both 44766208… and HEAD):

| mut | site reverted to base text | variant sha | census sha256 | verdict | inv | non_invariant | ns |
|-----|----------------------------|-------------|---------------|---------|-----|---------------|----|
| m1 | :692 test (impl :695) `if grep -q '^error:' <<<"$s_out"` → `if printf '%s\n' "$s_out" \| grep -q '^error:'` | a53efee570a03bd789c74367a02aff2a7dec11a3 | 14515b5543403be3dfa64c395e3e64ae2eaeac66e02ad6446b0e26611758aaf0 | FAIL (rc 1) | 7/10 | P1, P3, P6 | 0/3 |
| m2 | :694 note (impl :697) `$(grep -m1 '^error:' <<<"$s_out")` → `$(printf '%s\n' "$s_out" \| grep -m1 '^error:')` | 1356357851e72ce9c2cf3c2335af6082f5bd0cc2 | 4dc426b3bee5bd7a82a133b23338378d0ec65bcbce6a3a5cef397dffbf4e1b8c | FAIL (rc 1) | 7/10 | P1, P3, P6 | 0/3 |
| m3 | :1621 -Qu (impl :1624) `awk 'NR <= 3 {print $1}'` → `\| head -n3 \|` | 631d84f2506206e07c5d130eaab1070eb0815bef | d2588ff059db8a06c9e71a41f183130a295865c6ee1e92893833fea71ee727f7 | FAIL (rc 1) | 9/10 | U1 | 3/3 |
| m4 | :1635 -Sup qu-empty branch (impl :1638-1639) `awk 'NR <= 3 {n=$1; …}'` → `\| head -n3 \|` | adc42940c60dc6ada9c651dc4902892ea363cf04 | e074631fca500fc2c7917804cf976aac5b0d4fad5463945a8f93d29a5483bc95 | FAIL (rc 1) | 9/10 | U2 | 3/3 |
| m5 | :1641 -Sup sup>qu branch (impl :1644-1645) same text → `\| head -n3 \|` | c04b114cf7506c056126733c0038ccc6bbb7a710 | 1debcd6fb8657906947385bc0577d4eacc471abbb2747e95bf1429c2170f96b0 | FAIL (rc 1) | 9/10 | U3 | 3/3 |
| m6 | :1652 -Suu (impl :1655) `awk 'NR == 1'` → `\| head -n1 \|` | 56a4324df9551a0ac9f7d5479ebb305826152999 | 43b9f49bd0eca9d1c66bf43ed15013eac90b3f3c0d2aa821a99fcb147b7fe9ff | FAIL (rc 1) | 9/10 | U4 | 3/3 |

All variants: selftest_pass and default_equal as noted below; per-run tokens 5dac16cab8fe (m1), b5a8e6a182a7 (m2), 98d3a0e8876b (m3), 37693a3b1293 (m4), 94ab4de5ba0e (m5), 488a5d39a023 (m6) — fresh per run, large twin first (m1.json…m6.json).

Observed failure mechanisms (from per_case in the JSON receipts)
- m1 (test line): the three error-bearing large twins read the pipeline false and fall through to the wrong verdict — P1/P3/P6 large_rc=0 `PLANE packages: HEALTHY (pacman -Qkk rc=1 sample=4(…) drift=0 …` vs small_rc=2 BLOCKED; exactly the R41 defect signature. Production-path legs N1/N3/N6 likewise: small `BLOCKED (… error: alpha: /usr/bin/x-5dac16cab8fe …)` vs large `DEGRADED (…)` → ns_invariant 0/3. Selftest 129/130 (the `R42-C1` large -Qkk case fails).
- m2 (note line): the note assignment `PKG_NOTE="…$(printf … | grep -m1 …)"` dies under `set -euo pipefail` once grep -m1 exits early — P1/P3/P6 large_rc=141 (census killed, `; rc=141` is the only extra compared line), small_rc=2; N1/N3/N6 large produce no `PLANE packages:` line at all → ns 0/3. Selftest 129/130.
- m3 (-Qu): U1 large_rc=141 (census killed in the cand_names assignment), small_rc=1; ns 3/3 (packages-only legs unaffected). Selftest 129/130 (the `R42-C1` 4002-candidates case fails).
- m4 (qu-empty -Sup): U2 large_rc=141, small_rc=1; ns 3/3; selftest still `PASS (130 cases, 130 passed, 0 failed)` — this site is killed ONLY by the counter's U2 twin, i.e. the counter carries coverage the census selftest lacks for this branch.
- m5 (sup>qu -Sup): U3 large_rc=141, small_rc=1; ns 3/3; selftest 130/130 — same counter-only kill shape as m4.
- m6 (-Suu): U4 large_rc=141, small_rc=0; ns 3/3; selftest 129/130 (the large-candidates case also exercises -Suu).

Coverage reading. Each mutant was refused by exactly the twins exercising its site (m1/m2 → the three error-bearing P pairs and all three ns legs; m3→U1, m4→U2, m5→U3, m6→U4), with no collateral failures of unrelated twins and default_equal 1 everywhere (on the clean default fixture the reverted text behaves identically — the defect is size-gated). No variant PASSed, so there is no uncovered site among the six. The two -Sup branches (:1635, :1641) are covered only by counter twins U2/U3, not by any selftest case — a positive coverage fact for the counter, not a gap.

Restoration evidence. The lane was never written to during the probe; all mutated bytes lived in disposable scratch clones (fx.m1…fx.m6 under the seat scratch, removed at the end). After all runs: lane HEAD `87c4f7c627e377e5f6d361498e8db9b3886d7953` (unchanged), `git rev-parse HEAD:tools/tsukuroi-census.sh` = `ed83079c400594ab5ed84da045a6ed020c1a2542` (== the blob at 44766208…, unchanged), worktree `sha256sum tools/tsukuroi-census.sh` = `46d62a24709ece8efbcd231f4c269bd5b3791237e3c78ac7433fb0115494f1b1` (== pre-run value), `git status --porcelain -- tools/` = 0 lines.

Receipts (all under .ufo/waves/round-42/w1/C1MutSites/, each < 2 MB; total 29,272 B): base.json, m1…m6.json (full counter JSON lines), m1…m6.patch (the exact one-hunk revert of each variant), m1…m6.err + base.err (counter stderr, empty), prep.sh, commit.sh, run.sh, digest.py (method drivers).

Not done / out of scope: no combined multi-site reverts were scored (item asks single-site only); no C2 rows touched; no tools installed (none needed; no pacman transaction run, per the host-wide pause); the counter's own scratch roots are removed by the counter itself on exit, and the seat scratch dir was removed after copying receipts.
