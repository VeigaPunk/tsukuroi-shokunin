# ScribeNoUpgrade — seat index (round 36, wave 1, routed repair 4)

Target repo: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
Base read: declaration `6d76fb20f6ecbc940e5c8fff36c74060c885e161`; gate baselines and digests at
lane head `189d8a080ba8d508d5faab12cad9e688aee91dab`.

| # | Site (lane-relative) | Draft file (this directory) | Append block lines (exact) | Pipe-prefixed lines added |
|---|---|---|---|---|
| 1 | `SKILL.md:397-399` | `SKILL.md.append.md` | 40 | 0 |
| 2 | `corpus/knowledge/update-safety-note.md:420-424` (bullet ends at 425) | `update-safety-note.md.append.md` | 38 | 0 |
| 3 | `corpus/knowledge/update-safety-v2.md:52` | `update-safety-v2.md.52.append.md` | 25 | 0 |
| 4 | `corpus/knowledge/update-safety-v2.md:198` | `update-safety-v2.md.198.append.md` | 24 | 0 |

Every block is **appended at EOF** of its target, never inserted at the cited line. Each draft file
carries: the landing instruction with the verified reason, the `>`-quoted verbatim original, the
exact fenced append block, and the replacement sentence.

Evidence files in this directory:

- `receipts-live.txt` — read-only re-measurement of the four directives + `HoldPkg` and of
  `/etc/pacman.conf` at 2026-10-24T03:08:20Z, plus target digests.
- `ability-to-fail-before.txt` — the sweep's before state: 0 of 3 target files name
  `corpus/knowledge/pacman-backup-files-r35.md`; the four routed loci quoted verbatim.
- `gates-baseline-189d8a08.txt` — read-only gate baselines at the lane head: `check-appended-notices`
  PASS, `check-knowledge-header` PASS, `check-recheck-commands` PASS, `check-self-assessment` FAIL
  with exactly one mismatch (K10, 46 vs 47 lesson files — pre-existing, not caused by this seat).
- `verify-drafts.txt` — the four drafted blocks run against the real gate functions
  (`check-recheck-commands.assess_file`, `check-knowledge-header.evaluate`, `header_lines`,
  `recheck_line`) and against the r18 registry prefix rule, plus the exact SKILL.md
  `wc -l` / pipe-line delta.
- `residual-mentions.md` — other corpus loci that still group `NoUpgrade`/`NoExtract` with the pins
  (outside the routed four; L1 decision).
- `round-36-mistakes-row.md` — the drafted `corpus/lessons/round-36.md` `## Mistakes` row.
- `ScribeNoUpgrade.md` — the seat report (also at `.ufo/waves/round-36/w1/ScribeNoUpgrade.md`).
