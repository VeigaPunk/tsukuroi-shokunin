# ScribeKnowledge — round 99, wave w1 (scoped findings)

Seat: scribe (leaf member, no dispatch). Scope: draft the round's knowledge entry — what the
accepted-cap families must assert, and what the two new lie kinds certify.

- **Drafted knowledge entry (the deliverable):**
  `.ufo/waves/round-99/w1/ScribeKnowledge/limine-metadata-cap-families-r99.md` — provenance trio
  first (`source:` citing `corpus/SOURCES.md` S395 **and** the gate's byte offsets, `verified-at:
  2026-11-08`, `recheck:` with a runnable procedure), six sections, a `Limits` section that names
  the uncertified X/Y echo legs, the unchanged roster, and the r92-r98 families it does not
  re-certify. Every number in it carries the command that produced it; every negative claim
  carries its sweep. It is written in the seat dir — no `corpus/` file was created or modified.
- **Review of the landed corpus draft:**
  `.ufo/waves/round-99/w1/ScribeKnowledge/corpus-draft-review.md` — six findings on the L1's landed
  `corpus/knowledge/limine-metadata-cap-families-r99.md`, each with its sweep.
- **Seat report (commands, raw output, PASS/FAIL table):**
  `.ufo/waves/round-99/w1/ScribeKnowledge/report.md`
- **Receipts:** `.ufo/waves/round-99/w1/ScribeKnowledge/receipts/` (14 numbered files, 10 battery
  JSONs with their stdout/stderr, the two lie-wrapper bytes, the fixture JSONL).
- **Scratch (deleted before this report):** `/fast/scratch/hyaku/tsukuroi-r99/ScribeKnowledge`

## What this seat measured (own runs, own receipts)

| leg | measured | verdict |
|---|---|---|
| landed gate, r99 battery x3 | `met` 105/105, `failed_families []`, 0 error rows; the six named families `[4, 0]` | PASS |
| `N09-y-era`, r99 x3 | `unmet` 104/105, failed exactly `[REFUSAL-VERSIONS-9DIGIT-Y]`, that family `[0, 4]` | PASS |
| `N09-y-era`, r98 control x3 | `met` 105/105, `[]` — the r98 roster is blind to the Y-cap era lie | PASS |
| `N11-x-era`, r99 x3 | `unmet` 103/105, failed exactly `[EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]`; `REFUSAL-VERSIONS-9DIGIT` `[0, 4]`, `EXPLICIT-VERSION-ERA` `[3, 1]` | PASS |
| `N11-x-era`, r98 control x3 | `unmet` 104/105, failed exactly `[EXPLICIT-VERSION-ERA]` — the X leg is a **delta**, not a flip | PASS |
| landed gate, r98 control x3 | `met` 105/105 | PASS |
| the r98 G6 survivor attack gate, r98 control x3 | `met` 105/105 — the r98 roster read the Y-cap era lie as met | PASS |
| the same G6 gate, r99 x3 | `unmet` 104/105, failed exactly `[REFUSAL-VERSIONS-9DIGIT-Y]` — the survivor is closed by the file that produced it | PASS |
| the r98 fixed-echo attack gate, r99 and r98 control | r99 `unmet` 98/105 naming `REFUSAL-VERSIONS-9DIGIT` and `REFUSAL-VERSIONS-9DIGIT-Y` (`[0, 4]` each); r98 control `unmet` 100/105 without them — the echo side's delta is two families | PASS |
| `--selftest` (no reference) | `selftest PASS 5/5` | PASS |
| the two new lie kinds, r99 x3 each | `limine-version` `unmet` 93/105; `visibility-era` `unmet` 95/105; 0 error rows | PASS |
| byte anchors on the pinned gate and battery | MAIN 16931/17037 (lines 316/318), EARLY 11230/11344 (lines 200/202), source field 16977/11280; `meta_ok` 99430/99523; the ten `check_echo`/`check_era` sites; `LIE_KINDS` 12 → 14 | PASS |
| the gate's own JSON per spelling | echo verbatim, source `flag`, era from the whole tuple (`12.09.4`→A, `12.000000009.000000005`→B, `12.999999999.4`→B, `0.999999999.0`→A) | PASS |
| roster | `FAMILY_ROSTER` 105 in both batteries; the r99-vs-r98 diff touches no roster literal | PASS |
| C2 context (not this seat's claim) | r99 checker `--selftest` `PASS 17/17`; hybrid fixture → `RC-CELL-MISSING`; restated → `RC-CELL-AMBIGUOUS`; the r98 control reads `PASS` on both | PASS |

## Findings (reported; the corpus is the L1's)

1. **The cited N10 twin receipt does not exist.** The landed corpus entry's §3 and
   `corpus/lessons/round-99.md` cite `.ufo/waves/round-99/before/dev/c1-N10-twin-r98-control.json`
   for the dropped bend's r98-control reading (the plan names a third spelling,
   `before/dev/c1-N10-twin-r98.json`). Sweep: `find .ufo/waves/round-99 -name "*N10*"` → no output.
   The reading is asserted in two landed files with nothing behind it; this seat did not
   re-derive it and does not cite it.
2. **A blanket lie kind's `unmet` reading is only partly the field assertion.** Of the twelve
   families the `limine-version` lie fails, **seven** fail because the falsified field was read and
   **five** (`AUTO-PROBE-FAIL`, `AUTO-PROBE-SHAPES`, `EXTRA-COMPONENT`, `REFUSAL-VERSIONS`,
   `REFUSAL-VERSIONS-10DIGIT`) fail because the wrapper does `json.loads(p.stdout)` before it can
   falsify anything and a refusal answers rc 64 with an **empty** stdout — so the wrapper exits 1
   and the refusal family sees `rc 1` where it expects `rc 64`. The landed §4 reads as if every
   failing family failed because of the field; the drafted §4 states the split.
3. **The landed `recheck:` line carries no procedure** (`recheck: 180d`), while
   `tools/check-recheck-commands.py` reads the last `recheck:` line as a procedure another agent is
   invited to follow.
4. **The landed `source:` line carries no gate byte offsets**, although the entry's first
   proposition is about the gate's two emission sites.
5. **The landed §3 heading counts three committed bends; two are committed** (the bend directory
   holds `N09-y-era.py` and `N11-x-era.py`; the third row is marked "(dropped)").
6. **The r98 battery still emits the r97 JSON schema token** (`tsukuroi-limine-pin-battery-r97-v1`
   in the control receipts; the r99 battery moved to `…-r99-v1`). This is the carried r98 Frontier
   item, noted because a reader comparing the two batteries' receipts by schema token will see
   `r97-v1` on the control leg.
7. **The L1's `--selftest --reference` leg is incomplete.** Its frozen receipt
   `.ufo/waves/round-99/before/dev/c1-selftest-r99-reference.txt` ends `rc=1` with a
   `FileNotFoundError` on a scratch path under `/fast/scratch/hyaku/tsukuroi-r99/dev/` — the shared
   scratch tree a sibling seat deleted at ~11:24. The leg certifies nothing; this seat established
   the equivalent fact directly (each new lie kind makes the battery read `unmet`).

## Limits of this seat's own work

- The X/Y **echo** legs have no spelling-targeted committed bend: the round's two bends falsify
  `visibility_era` only (`grep -c '"limine_version": limine_version'` → 2 for the gate and 2 for
  each bend; the bend directory holds exactly two files). They *are* witnessed, but only by blanket
  adversaries — the `lie-limine-version` wrapper and the r98-carried fixed-echo attack, which
  under the r99 battery reads `unmet` 98/105 and names both `REFUSAL-VERSIONS-9DIGIT` and
  `REFUSAL-VERSIONS-9DIGIT-Y` (`[0, 4]` each) where the r98 control reads `unmet` 100/105 without
  them. Those adversaries falsify the echo for every explicit flag at once, so they cannot say
  which spelling a family covers.
- A lie kind proves the battery **sees** the field, not that every family asserts it: five roster
  families set `check_echo`, five set `check_era`, and 99 of the 105 set neither.
- This seat did not re-derive the dropped N10 bend's reading (no receipt exists to re-derive
  from), did not run `tools/make-r99-bends.py` or any earlier `make-r*-bends.py` (they write into
  the frozen wave dirs), and ran no mutating git or jj command.

{"seat":"ScribeKnowledge","verdict":"findings","notes":"Entry drafted at .ufo/waves/round-99/w1/ScribeKnowledge/limine-metadata-cap-families-r99.md (trio first, S395 + gate byte offsets cited, six sections, Limits names the uncertified X/Y echo legs, every number paired with its command, every negative claim with its sweep); review of the L1's landed corpus draft at .ufo/waves/round-99/w1/ScribeKnowledge/corpus-draft-review.md; report and 14 receipts under the seat dir. RUN (own receipts): landed gate met 105/105 x3 (0 error rows); N09 unmet 104/105 x3 failed exactly [REFUSAL-VERSIONS-9DIGIT-Y]; N09 on the r98 control met 105/105 x3 (blind); N11 unmet 103/105 x3 failed exactly [EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]; N11 on the r98 control unmet 104/105 x3 failed exactly [EXPLICIT-VERSION-ERA] (the X leg is a delta); the r98 G6 attack gate met 105/105 x3 on the r98 control and unmet 104/105 x3 [REFUSAL-VERSIONS-9DIGIT-Y] on r99; selftest PASS 5/5; the two new lie kinds unmet 93/105 and 95/105 x3; AST roster 105 in both batteries; grep -abo byte anchors for both emission sites and the ten assertion sites. FINDINGS: (1) the cited before/dev/c1-N10-twin-r98-control.json does not exist (find .ufo/waves/round-99 -name '*N10*' empty) though the landed entry and the lesson cite its reading; (2) a blanket lie kind's unmet reading is only partly the field assertion - 7 of 12 failures are field-caused, 5 are the wrapper's refusal-path breakage; (3) the landed recheck: line has no procedure; (4) the landed source: line omits the gate byte offsets; (5) the landed heading counts three committed bends where two are committed; (6) the r98 control battery still emits the r97 schema token; (7) the L1's --selftest --reference leg ended rc=1 on a deleted scratch path and certifies nothing."}
