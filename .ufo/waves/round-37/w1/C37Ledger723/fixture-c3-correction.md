# Fixture: C3 correction proposal (validated against observed tip 0e5f70f)

Claim: with the SCORECARD.md operative tables below (exactly as at tip 0e5f70f), the unchanged
`tools/check-self-assessment.py --revision <tip>` reports checked 27, mismatches 0, PASS, exit 0.
This was OBSERVED directly at 0e5f70f (my run), so a fresh fixture repo is not required to
re-verify the end state; the intermediate failure states were each observed directly too.

## Operative axes table (last `## Axes` section) — rows as at tip
| depth | 8 | 56 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3110 `wc -l` / 839 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 49 files (`find corpus/lessons -type f | wc -l`); four standing rules near the top of SKILL cite no knowledge note; no ordinal move claimed. |
| coverage | 9 | `corpus/README.md` 269 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes; four declared round-1 read-only surfaces link knowledge; pacnew census arm C1 was not verified in round 35, no coverage ordinal move. |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (105 cases, 105 passed, 0 failed); live run exits 1 with six-plane rollup; `--identity` not landed. |
| freshness | 9 | Each round record re-ran predecessor pins; dated round-1 D1-D5 rechecks and current recheck procedures remain recorded; captures are dated, not durable host state. |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; C3 requires mismatches 0 at the measured round-37 tip; no ordinal uplift. |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; recipient acknowledgement and independent replay are unverified. |

## Operative capabilities table (ONE table, the last `## Capabilities` section, all four rows)
| sources-registry | Curates where the lane learns: opened tier-scoped rows with anchors, rejections with flips, study paths, search log and unopened leads; checked by frozen census commands | `corpus/SOURCES.md` |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT line; hermetic selftest prints PASS (105 cases, 105 passed, 0 failed) | `tools/tsukuroi-census.sh` and `.ufo/evidence/round-1-kaika/scout-live.md` |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations even on package-probe failure; isolates fixtures and blocks unavailable/non-directory metadata without grading intentional 0555 policy | `.ufo/waves/round-12/resumed/after.json` |
| boot-chain-audit | Audits limine entries read-only: extracts initramfs, types new_root, binds firmware-selected entry and emits per-entry next-boot verdict | `tools/boot-chain-audit.sh` and `.ufo/waves/round-17/l1-capture/audit-live.txt` |

## Rules extracted from the failure sequence (observed)
1. Every count must use the checker's literal patterns ("N notes", "`SKILL.md` N `wc -l`",
   "N table lines", "`corpus/lessons/` N files", "`corpus/README.md` N `wc -l`",
   "PASS (N cases, ...)").
2. All capability-row evidence paths must be full repository paths, individually backticked, and
   present at the measured revision. Bare relative tokens (`after.md`, `selftest-after.json`,
   `mode-policy-mutant.json`) break K17/K18.
3. The last `## Capabilities` section must contain exactly one complete table of all four rows;
   a trailing partial table becomes the selected table and drops rows (observed cannot-evaluate at
   5124bf3: "missing capability row: sources-registry").
4. Appending a superseding table must come as the new LAST table and contain ALL rows.
