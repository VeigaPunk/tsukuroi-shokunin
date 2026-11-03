# R2RevRepair — seat report (round 65, hyaku run 15, wave w1)

Seat: R2RevRepair (reviewer, leaf). Item REV-REPAIR: attack the R64-SPOTCHECK-C1-PROOF re-expression before it lands.
Execution class: READ-ONLY (observe, compute, report). Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. HEAD 37c74e27.

## What I did

1. Re-derived the additive-only proof AT the cited revision 431f0c9 for corpus/SOURCES.md, SKILL.md, SCORECARD.md (CR-stripped 2f3061ef blob vs 431f0c9 blob, `git diff --no-index --numstat`).
2. Ran the ORIGINAL r64 wording (`git show 2f3061ef:F | tr -d '\r' | cmp - F`) three times at the current worktree (HEAD 37c74e27).
3. Reviewed E3RoutedRepair's draft (`.ufo/waves/round-65/w1-artifacts/E3/routed-repair-draft.md`): extracted its sh gate, re-ran it green and negative.

## Measured

| check | result |
|---|---|
| 431f0c9 vs stripped base, SOURCES | added **3**, removed **0** (hunk `@@ -288,0 +289,3 @@`, S279–S281 at id position) |
| 431f0c9 vs stripped base, SKILL | added **120**, removed **1** (hunk `@@ -5490 +5490,120 @@`; the `-1` is the EOF artifact: base ends `.` with no newline; `cmp` EOF after byte 859; with newline restored → `119 0`) |
| 431f0c9 vs stripped base, SCORECARD | **0/0**, byte-identical (`cmp` rc 0; sha256 `13047505…89df66` both sides) |
| original wording at worktree HEAD 37c74e27, ×3 | **rc 1 / 1 / 1** (SOURCES char 238601 line 289; SKILL EOF after byte 1351538; SCORECARD char 23030 line 166) — false for all three at HEAD |
| original wording at 431f0c9 (from the blobs) | rc 1 / 1 / 0 — matches the closure |
| E3 gate (draft's sh block) at 431f0c9 | rc **0**, prints 3/0, 120/1, 0/0 |
| E3 gate negative control REV=2f3061ef | rc **1**, prints 381/381, 5452/5452, 4723/4723 |
| E3 gate run under `sh` | rc 0, identical output |

## Verdicts

- **Re-derived counts (task step 1): PASS.** Every count matches expectation (SOURCES +3/−0, SKILL +120/−1, SCORECARD 0/0). No finding against the repair's measurement.
- **Original wording (step 2): FALSE for 3/3 at HEAD.** SOURCES/SKILL fail because of the round-64 additive work; SCORECARD fails at HEAD because of later commits (09468bda's `line-endings-guard` row at SCORECARD.md:166 and 37c74e27's declaration, `85/0`), not the r64 work. The closure's "true only of the fix-time worktree" stands.
- **E3 Block A (step 3): AGREE** on the command (exactly the one I re-derived, green rc 0 at 431f0c9, red rc 1 at 2f3061ef), on the counts (measured, not fitted), and on append-only safety (no rewrite; no axis/claim/gate change; the superseded wording is quoted verbatim from corpus/lessons/round-64-verifier-spotcheck.md §5).
  - Minor defect 1: Block A does not locate the superseded text. The `cmp - F` rc 0 ×3 wording is at SCORECARD.md:4744 (round-64 C1 row) and in LOG.md's round-64 outcome lines and corpus/lessons/round-64.md. The erratum should name SCORECARD.md:4744 so the superseded text is located, not only quoted.
  - Minor defect 2: two erratum drafts exist for one defect id: E3 Block A and `.ufo/waves/round-65/drafts/scorecard-erratum-r64-proof.md` (heading `## Round 65 — routed repair (R64-SPOTCHECK-C1-PROOF): …`). Landing both gives two erratum blocks for one routed defect. Exactly one should land; I recommend A (it carries the receipt). E3's landing note 4 says the same.

## Defects seen

- E3 Block A's untracked receipt paths (`routed-repair-receipt.txt`, `reidentity-at-431f0c9.txt`) are not committed; the L1 commit must include them, as the draft says.
- Host `diff` is pi-uu-diff 0.8.0, not GNU diff; E3's gate correctly avoids GNU flags.
- An awk extraction of the draft's sh block failed in the tool shell (parser error, rc 2); I transcribed the block with the write device instead. Not a repo defect; recorded for transparency.

## Verification gaps

- The L1 must still land exactly one erratum block and run the cited-receipts gate (`--round 65`) after landing.
- I did not run the round's census or selftests (not in my item).

## Commands and rc

Full log with rc: `.ufo/waves/round-65/drafts/rev-repair.md` (commands 1–29). Raw receipts copied to `.ufo/waves/round-65/w1-artifacts/R2RevRepair/` (step1, step2, step2b, step3, step4 run/negative/sh).

Tools: none installed. Pacman, systemctl, sudo: not used. Git: read-only only (`rev-parse`, `cat-file`, `log`, `show`, `diff`, `status --porcelain`, `rev-list`, `merge-base`).

## Files written

- `.ufo/waves/round-65/drafts/rev-repair.md` (the attack receipt; every command with rc)
- `.ufo/waves/round-65/w1/seats/R2RevRepair.md` (this report)
- `.ufo/waves/round-65/w1/R2RevRepair.md` (same content, the Report trailer path)
- `.ufo/waves/round-65/w1-artifacts/R2RevRepair/*` (receipts)

Scratch `/fast/scratch/hyaku/tsukuroi-r65/R2RevRepair/` removed at seat end (see confirmation in the final message).
