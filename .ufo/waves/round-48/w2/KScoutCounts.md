VERDICT: defect-found

# C3-Y1 — count sweep at FREEZE ae99f021b76f8eb1c8805d32d80644464afb1ff6

All bytes measured on a `--shared` clone checked out detached at ae99f021 in
`/fast/scratch/hyaku/tsukuroi-r48/KScoutCounts/lane` (removed after writing this report). The lane
working tree was never read as evidence. File hashes at FREEZE: `SCORECARD.md` sha256
`a9ebfde73e1793ccd99b7427fd5a285af9e5001772b4a4c2aac3042000c62074`,
`tools/tsukuroi-census.sh` `375aa737…e2426` (matches the frozen blob hash), `tools/boot-chain-audit.sh`
`77c80be8…9141ad`.

## Which tables the checker's "current" picks

`tools/check-self-assessment.py` `find_section` (lines 250-263) takes the LAST heading matching
`^##\s+Axes\s+[—-]\s` and `^##\s+Capabilities\b` respectively (confirmed by reading; last = round 46
since rounds 47/48 declared no new tables). At FREEZE:

- Axes table: `## Axes — current self-assessment (round 46 final measured surface)`, SCORECARD.md:3023-3034.
- Capability table: `## Capabilities — current full evidence set (round 46)`, SCORECARD.md:3036-3044.

## Stated vs observed

| Stated (cell, SCORECARD.md line) | Exact command | Observed at FREEZE | Line | Verdict |
|---|---|---|---|---|
| depth row: "67 notes" (:3029) | `find corpus/knowledge -maxdepth 1 -type f -name '*.md' \| wc -l` | 67 | :3029 | match |
| depth row: "SKILL.md 4546 `wc -l`" (:3029) | `wc -l SKILL.md` | 4546 | :3029 | match |
| depth row: "1323 table lines" (:3029) | `grep -c '^\|' SKILL.md` | 1323 | :3029 | match |
| depth row: "`corpus/lessons/` 70 files" (:3029) | `find corpus/lessons -type f \| wc -l` | **71** | :3029 | **DIVERGENCE — K10** |
| coverage row: "`corpus/README.md` 480 `wc -l`" (:3030) | `wc -l corpus/README.md` | 480 | :3030 | match |
| operability row: "PASS (164 cases, 164 passed, 0 failed)" (:3031) | `TMPDIR=<scratch> bash tools/tsukuroi-census.sh --selftest` (one run, 82 s, rc=0) | `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)` | :3031 | **DIVERGENCE — K13** |
| operability row: "boot-chain-audit --selftest prints `PASS total=49 failed=0`" (:3031) | `TMPDIR=<scratch> bash tools/boot-chain-audit.sh --selftest` (one run, rc=0) | `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=49 failed=0` | :3031 | match |
| capability host-census-gate: "selftest prints PASS (164 cases…)" (:3041) | same selftest as above | 166 cases | :3041 | **DIVERGENCE — K17** |
| capability boot-chain-audit row (:3043) | (no count stated; description only) | — | :3043 | not measurable |

Net: 3 divergences, matching the declaration's predicted "3 (K10, K13, K17) at the implementation
commit until restated" (SCORECARD.md:3106). The names fit the checker code: K10 lessons count
(check-self-assessment.py:617-625), K13 operability-row case count (:656-663), K17 host-census-gate
row case count (:709-725). The extra selftest output shows the two new cases are the declared
`(R48-C2)` TMPDIR-alias cases: `dirty TMPDIR resolves to an in-TMPDIR fd alias` and
`nonexistent dirty TMPDIR fails the base resolver`.

## Cheap spot-checks of non-counted cell statements (all consistent at FREEZE)

- coverage row "PROVINCE Core, Frontier and Adjacent sections present": `grep -n '^## Core\|^## Frontier\|^## Adjacent' PROVINCE.md` → `## Core` :6, `## Adjacent — finding-to-owner handoffs` :35, `## Frontier` :75 — present.
- adjacency row "formal overlap table present … OUT-001..010 anchors": `| ID | Finding` table at PROVINCE.md:44, ADJ-01..07 rows :46-52, OUT-001..010 rows :121-130 — present.
- operability row "round-46 `--identity` landed": `grep -n '^\s*--identity)' tools/tsukuroi-census.sh` → :3621 `      --identity) identity=1; shift ;;` — present (K14 consistent).

## corpus/lessons — what it will be after this round

Observed 71 files at FREEZE; every file matches `^round-` (37 `round-N.md` + 34
`round-N-verifier-spotcheck.md`, starting at round 1 — no round-0 file). The +1 vs the stated 70 is
`corpus/lessons/round-47.md`, committed at `3629c46a` (2026-10-27) — after the round-46 table was
written. Expected additions this round (named in `.ufo/waves/round-48/w2-spec.json` /
`w2-dispatch.json`):

- `corpus/lessons/round-48.md` — drafted by seat F-4 (`## Mistakes` section text only) and ScribeLesson; landed by the L1.
- `corpus/lessons/round-48-verifier-spotcheck.md` — not written by a w2 seat; written by the integrator at closure by house convention (`round-46-verifier-spotcheck.md` landed at `3c738a87` "integrator, hyaku"; `round-47-verifier-spotcheck.md` at `f6a46fa9`).

`find corpus/lessons -type f | wc -l` therefore reads **73** at the round's final revision if both
land (73 + N if the operator copies `considerthese/` notes or other files into lessons — no such file
is named in the w2 spec, so +2 is the expected delta). The L1 must restate the depth row's
`corpus/lessons/` count to the post-integration count, not 71 and not 70.

## What did not move

`corpus/knowledge` 67, `SKILL.md` 4546/1323, `corpus/README.md` 480 are all unchanged at FREEZE; the
L1's restatement changes only the lessons count (→73 expected) and the two census case counts
(164→166). If any w2 seat lands an additional knowledge note, knowledge becomes 68 — none is declared
in the round-48 claims (C2 admits rows of an existing file, `btrfs-scrub-grounding-r45.md`).

## Not run

- `python3 tools/check-self-assessment.py --revision ae99f021…` — not run (its inner census selftest
  would double my one allotted census run; the 3 divergences above are the exact K-checks it fires
  on, verified from the checker source and one live selftest each).
- `python3 tools/check-adjacency-anchors.py` — not run; the adjacency row cites its PASS at `a4477049`
  from round-46 wave receipts, which I did not re-execute.
- No counter files (`score-selftest-tmpdir-r48.py`, `check-scrub-admission-r48.py`) run — outside this item.
