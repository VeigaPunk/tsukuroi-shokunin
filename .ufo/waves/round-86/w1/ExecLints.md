# ExecLints — no-harm lints at the round-86 tip

Lane revision measured: `1e1caabcdd740a6429dd31d7aba3b725ff8c677d` (`git -C … rev-parse master`), branch master.
Environment: `PYTHONDONTWRITEBYTECODE=1`; nothing written outside `.ufo/waves/round-86/w1/ExecLints/` (scratch removed).
Receipts: `.ufo/waves/round-86/w1/ExecLints/` (`rcs.txt` is the index; all raw stdout/stderr saved there).

| Check (cwd = lane root) | rc | Verdict / verbatim key output |
|---|---|---|
| `python3 tools/check-knowledge-header.py --revision 1e1caabcdd740a6429dd31d7aba3b725ff8c677d` | 0 | PASS: `"note_count":102,"clean_count":102,"complete_count":102,"finding_count":0`; new entry `hibernation-boot-parse-r86.md` clean (source 3, verified-at 5, recheck 4). Baseline `3f567898` PASS 101/101, so +1 note, no finding introduced. |
| `python3 tools/check-registry-coverage.py --help` | 0 | usage printed (`--revision REV`, `--selftest`, `--branch` default master). |
| `python3 tools/check-registry-coverage.py --revision 1e1caabc…` | **1** | **FAIL 1 finding**: `{"detail":"no operative row names this regular tools/ file","id":"REGISTRY-ROW-MISSING","site":"tools/resume-gate-battery-r86.py"}`, counts `findings 1, missing 1, registered 135, rows_total 135, tools_total 136`. |
| `bash tools/tsukuroi-census.sh --selftest` | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (218 cases, 218 passed, 0 failed)`. |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | 0 | 52 × W04 duplicate-url warnings, 1 × `ok …/corpus/SOURCES.md`, no E code; no W04 names S346–S349; SOURCES rows 349 (r85 close 345, +4) with S346–S349 at lines 357–360. |
| `python3 tools/check-scorecard-unique-sections.py --help` | 2 | `check-scorecard-unique-sections: unknown arguments ['--help']` — the tool has no `--help`; contract is its module docstring (`[--file <path>]`, `--selftest`). Not a round regression. |
| `python3 tools/check-scorecard-unique-sections.py` | 0 | `every duplicate level-2 heading pair carries a supersession marker; ok` (SCORECARD.md unmodified vs tip). |
| `python3 tools/check-scorecard-unique-sections.py --selftest` | 0 | `SCORECARD_UNIQUE_SECTIONS: PASS (5 cases, 5 passed, 0 failed)`. |

## Round-introduced finding (routed to the L1; not fixed here — lane is read-only to this seat)

**REGISTRY-ROW-MISSING `tools/resume-gate-battery-r86.py`** — the only tool added in `git log 3f567898..master`
(`git diff --name-status … -- tools/ SKILL.md`: `A tools/resume-gate-battery-r86.py`, `M tools/check-hibernate-resume.py`;
`check-hibernate-resume.py` keeps its row). Introduced by freeze commit `2f67de80` (not present at `3f567898`: PASS 135/135).

- Committed `SKILL.md` at the tip has registry rows at 5917 `hibernate-resume`, 5918 `resume-gate-battery-r84`,
  5919 `resume-gate-battery-r85`; there is **no committed `resume-gate-battery-r86` row** (the table's next committed row
  is `count-resume-rows-r84`, so the missing row's site is the table gap after `SKILL.md:5919`).
- An **uncommitted** worktree edit to `SKILL.md` (`M SKILL.md`, not authored by this seat; `git diff -- SKILL.md`,
  saved verbatim as `skill-uncommitted.diff`, 3 insertions / 2 deletions) already adds that row at worktree line 5920
  plus the `--selftest` note on the `hibernate-resume` row. Nothing else tracked is dirty (`tools/`, `corpus/`,
  `SCORECARD.md` have no tracked diff).
- Proposed patch: commit that existing hunk as-is. Evidence it is sufficient — scratch fixture (`git clone --shared`,
  origin removed, worktree `SKILL.md` committed as `2ce6c784583204b6b6879f606e34589948110adf`):
  `{"counts":{"findings":0,"missing":0,"registered":136,"rows_total":136,"tools_total":136},"status":"PASS"}`, rc 0
  (`registry-fixture-worktree-skill.out`). The gate's own selftest passes 23/23 rc 0.

## Refusals / notes

- No lane file edited, no git/jj mutation, no host action, no tool installed, no subagent used.
- W04 count 52 matches the r85 both-ends figure; no new warning on the round's rows. Nothing else in the round's
  commits produced a lint finding.
