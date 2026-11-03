2026-11-03T21:16:48Z

# E3Mistake — MISTAKE-SWEEP (round 66 wave w1)

Item: mine the round-65 landing defect (a filed SCORECARD line edited in place — the round-63
"Measured outcome" sentence — instead of an appended erratum; closure defect 2 of
`corpus/lessons/round-65-verifier-spotcheck.md`), show the fix's check can fail, and write the
seat-harm tally for the considerthese proposal "Seat-harm incident log".

All reads read-only git / read-only files. No tracked file edited. No commit, no mutation.

## Status

DONE. Both drafts written; RED and PASS both observed; no blocker.

## Files written

| Path | Bytes |
|---|---|
| `.ufo/waves/round-66/drafts/mistake-sweep.md` | 10371 |
| `.ufo/waves/round-66/drafts/seat-harm-tally.md` | 7923 |
| `.ufo/waves/round-66/w1/E3Mistake.md` (this report) | — |

## Retained evidence — RED/PASS

Revisions: `1bd8e196` (r65 base) .. `7ab7c876` (r65 tip); `c68bfe97` (r66 base) .. working
copy = HEAD `aa75398e`.

| Check | Command | Output | rc |
|---|---|---|---|
| RED-1 raw removed lines | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 1bd8e196 7ab7c876 -- SCORECARD.md \| grep -c '^-[^-]'` | `1` | 0 (git diff rc 0) |
| RED-2 CR-stripped removed lines | `diff <(git -C ... show 1bd8e196:SCORECARD.md \| tr -d '\r') <(git -C ... show 7ab7c876:SCORECARD.md \| tr -d '\r') \| grep -c '^<'` | `1` | 0 (diff rc 1; 113 added lines) |
| RED-3 removed line | `... \| grep '^<' \| head -3 \| cut -c1-200` | `< view is untrusted on this host, r56/r57 lesson). Gates at the work revision: knowledge-header PASS` | 0 |
| PASS append-only | `diff <(git -C ... show c68bfe97:SCORECARD.md \| tr -d '\r') <(tr -d '\r' < /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md) \| grep -c '^<'` | `0` | 1 (grep no-match = expected 0; diff rc 1; 29 added lines) |
| Sensitivity (same PASS form on the known-bad pair) | `diff <(show 1bd8e196) <(show 7ab7c876) \| grep -c '^<'` | `1` | 0 |
| CR bytes | `git show <rev>:SCORECARD.md \| grep -c $'\r'` for 1bd8e196 / 7ab7c876 / c68bfe97 / worktree | `0 / 0 / 0 / 0` | 1 each (grep -c no-match) |

RED outcome: **FAIL-ABLE** — the sweep reports 1 removed line on the known-bad pair, the
round-63 sentence at `SCORECARD.md:4650` (base 99 bytes / 15 words → tip 227 bytes / 34 words,
rewritten in place). PASS outcome: **PASS** — 0 removed lines on the round-66 landing, and the
identical check returns 1 on the known-bad pair, so the pass is not vacuous.

Grounding of the landing: `git diff --numstat c68bfe97..HEAD -- SCORECARD.md` →
`29	0	SCORECARD.md` rc 0; HEAD `aa75398e` is the only commit in range touching SCORECARD.md;
`git show --stat` HEAD → 9 files changed, 581 insertions(+); `git status --porcelain --
SCORECARD.md` empty rc 0; `merge-base --is-ancestor c68bfe97 HEAD` rc 0.

## Retained evidence — seat-harm tally

- Item's grep, combined rc 0; per-file rc: `round-37.md` 0, `round-37-verifier-spotcheck.md`
  0, `round-39.md` 0, `round-40.md` **1**, `round-41.md` **1**.
- Calibration: the case-sensitive pattern misses `R40-TMP-MISROOT` (`round-40.md:81`) and
  `R41-TMP-MISROOT-REPEAT` (`round-41.md:80`); `grep -in 'misroot'` returns rc 0 on both,
  proving the miss is casing. Rows read by id and tabulated.
- Tally rows: R37-MISROOT-NOTE-DRAFT, R39-SEAT-PKILL, R40-TMP-MISROOT,
  R41-TMP-MISROOT-REPEAT, R41-CAPTURE-FIFO (last one from the round-45 ledger's round-41 count
  of 2; not matched by the item's pattern). Excluded matches: R37-SEAT-REPORT-COUNT
  (number-drift) and the round-37 verifier's "Fleet misroot" check row.
- Round 65: `grep -c 'R65-.*SEAT\|misroot' corpus/lessons/round-65.md` → `0`, grep rc 1
  (no match; file present, 13604 bytes).
- Cross-check: `corpus/lessons/round-45.md:140-144` gives 37:1, 38:0, 39:1, 40:1, 41:2 with
  the same ids; this seat's rows agree.

## Proposed QUALITY criterion (text in the sweep draft, §5)

Append-only corrections are checked by the CR-stripped removed-line sweep; the criterion
requires 0 removed lines, cites the round-65 closure defect 2 and the round-65 pair's 1
removed line as the red-before, and the round-66 landing's 0 as the green. `QUALITY.md` was
not edited (item forbids it).

## Risks / limits

- Other filed rounds and other files are not swept; the draft states this explicitly. The
  command generalizes but no other pair was run.
- The `tr -d '\r'` is inert on all four measured files (0 CR lines each), so on this host the
  frozen form reduces to a plain removed-line count; the stripping matters only for CRLF bytes,
  which these files do not have.
- R41-CAPTURE-FIFO is included from the round-45 ledger, not from the item's grep; if the L1
  wants strict item scope, drop that row.
- Fix texts are quoted as the lesson rows state them; no fix was re-verified.

## Scratch

`/fast/scratch/hyaku/tsukuroi-r66/E3Mistake` (raw diff, stripped diff, append-control diff) was
deleted before yielding; every command in the drafts re-derives those files. No `/tmp` path is
cited as evidence.
