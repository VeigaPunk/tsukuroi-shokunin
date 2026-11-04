status: complete
verdict: pass — drafts complete; the L1 appended S304-S308 verbatim; C1 target revision not yet committed

Seat SC2Sources — L2, tsukuroi lane round 73, wave w1. Leaf member.

Delivered in this directory:

- `rows.md` — registry rows S304-S306 (admitted: docs/code, tier A, mined, opened 2026-11-03, recheck
  on-release, used-by `corpus/knowledge/systemd-unit-load-plane-r73.md`) and S307-S308 (REJECTED with flip
  conditions), each with measured fetch evidence; one line per row, 11 cells, no pipes; plus the
  pre-append census and the refusal measurement log.
- `gate.md` — the `## Gate` block for `corpus/lessons/round-73.md` (one ≤25-word located quote per new
  row, supplementary located quotes, admitted/census/ordering notes, instrument probes) and the rule-5
  `## Search log` paragraph (5 identified / 5 screened / 3 included / 2 excluded).
- `report.md` — scoped findings, exact commands and outputs, and the concurrent-landing record.
- full report also at `../SC2Sources.md`.

Evidence: `python3 tools/count-ul-rows-r73.py --fixture <mirror>` over the lane registry + these five
drafted rows + the note + the committed snapshots reads
`UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `met=1`, rc 0 (declared bytes, then
re-confirmed with the replacement counter against the landed tree). Anchor binding held (removing
`unit.c` from S305's anchor flips `anchor-not-bound`, rc 1); generic-vocabulary grounding survived (a
content-free statement over the 140 KB `install.c` still verifies), recorded as a reach limit of the
frozen predicate.

Concurrent events recorded, not caused by this seat: the L1 appended S304-S308 verbatim; both instruments
were replaced (declared `542f9c29…` / `93f034e3…` -> now `84501ab8…` / `328a6bf6…`, selftest 11 -> 12
cases); HEAD is `8eeadcb9` with the note and rows uncommitted, so `--revision HEAD` reads
`UL_NOTE absent` and C1 has no measured revision yet.
