# R2RevC2 — C2-ATTACK scoped findings (round 66 w1)

UTC: 2026-11-03T21:02:58Z. Lane base c68bfe97. Item: C2-ATTACK (reviewer attack on claim C2).
Full receipt with verbatim commands/outputs/rc: `.ufo/waves/round-66/drafts/rev-c2.md`.

Axes (godspeed): locator fidelity at live HEAD · method independence vs E2SibHeads · row-shape soundness against fabrication · evidence discipline (command/output/rc per number) · scratch hygiene.

## Findings

1. **AGREE — OUT-004 (mado)**: independent re-derivation by `git grep -n -F` at the sibling's live HEAD (method ≠ E2's `git show | grep`). Live HEAD `git rev-parse` = 524fa1f90b1f2de44b3019bacf833d54e0af13a0 (rc=0), identical to `drafts/c2-anchors-live.tsv` AR4 `live_head`; the 6-word register quote fragment located at `HEAD:PROVINCE.md:6` (rc=0), == TSV line 6 == register quote_line 6.
2. **AGREE — OUT-006 (kumitate)**: live HEAD 3c369336218329e30248b5d69c41348c02658169 (rc=0) == TSV AR6; quote located at `HEAD:PROVINCE.md:3` (rc=0), == TSV line 3 == register quote_line 3.
3. **AGREE — OUT-008 (kaidoku)**: live HEAD c7fe6898e9a8b3ff04486b4a1d672e9db37610c9 (rc=0) == TSV AR8; quote located at `HEAD:PROVINCE.md:3` (rc=0), == TSV line 3 == register quote_line 3.
4. **Finding (expressiveness limit)**: the frozen C2 row regex `^\| AR[0-9]+ \| OUT-0[0-9]{2} \| [a-z]+ \| [0-9a-f]{40} \| [0-9a-f]{64} \| located \|` matched all 3 fabricated fixture rows (grep -E rc=0, count 3), including rows whose 40-hex HEAD is not a real commit. The regex alone cannot catch a fabricated HEAD.
5. **Finding (discriminator works)**: `git -C <sibling> cat-file -e <HEAD>` rc=0 for all 8 distinct heads across the 10 TSV rows (AR1/AR5/AR7 share mori's head); the fabricated head 1111…1 fails with rc=1 in mado-shokunin. The L1's printed rows should carry this check behind the shape check.
6. Register r19 commits differ from live heads for all three anchors (expected r19→r66 drift); TSV correctly pins live heads per the C2 predicate "40-hex live HEAD".

No DISAGREE found. Verdict: **C2-LOCATORS-AGREE**.

## Residual risk / verification gaps

- Only the 3 item-named anchors were re-derived by the second method; the other 7 rows' line numbers rest on E2SibHeads' own receipt, not independently re-derived here (out of item scope).
- Head liveness of the 7 non-re-derived rows was checked only for object existence (`cat-file -e`), not for `rev-parse` equality; drift between E2's run and integration would not be caught by existence alone.
- The 64-hex blob sha256 column was not recomputed (not named by this item); the C2 erratum portion (2277 → found_line 2822 re-pin) is not attacked here (separate seat).
- Scratch /fast/scratch/hyaku/tsukuroi-r66/R2RevC2 deleted; fixture and outputs preserved verbatim in drafts/rev-c2.md.
