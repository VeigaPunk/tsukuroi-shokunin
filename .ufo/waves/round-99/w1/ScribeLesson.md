# ScribeLesson — round 99, wave w1 — scoped findings

Seat: `ScribeLesson` (scribe; leaf member — no subagent dispatch). Lane:
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, pre-round tip
`f107da3afe511f7db8cdc30235a992b774903158` (git HEAD detached; **no mutating git or jj command was
run** — only read-only `git show` / `archive` / `rev-parse` / `grep` / `cat-file` / `diff` /
`status`).

Files written (this seat only):

- `.ufo/waves/round-99/w1/ScribeLesson/corpus/lessons/round-99.md` — the drafted lesson
  (`## Gate`, `## Mistakes`, `## Counter-attack scoreboard (QUALITY 115)`, `## Routed (r98 -> r99)`).
- `.ufo/waves/round-99/w1/ScribeLesson/report.md` — the commands, the raw output, the PASS/FAIL per
  expected line, the receipt paths and the final JSON line.
- `.ufo/waves/round-99/w1/ScribeLesson/receipts/` — 21 numbered text receipts plus
  `receipts/json/` (7 battery JSONs, 3 runs each).

**No `corpus/` file was created, modified or deleted** by this seat; nothing under `tools/`,
`SKILL.md`, `SCORECARD.md`, `LOG.md`, `.ufo/plans/`, `.ufo/waves/round-99/before/` or
`claims.json` was written. Scratch `/fast/scratch/hyaku/tsukuroi-r99/ScribeLesson` was deleted
before this file was written. No tool was installed or upgraded; `pacman` was not invoked (paused
host-wide); no `sudo`.

## What this seat measured (every number re-derived, not trusted)

| leg | expected | measured by this seat | verdict |
|---|---|---|---|
| instruments manifest | 16 lines `OK`, exit 0 | 16/16 `OK`, exit 0, before and after every pass | PASS |
| C1 landed gate, r99 battery, x3 | `105/105 met`, `failed_families []`, 0 error rows | exactly, 3/3 runs, 420 cases, X/Y/Z/EXPLICIT-VERSION-ERA each `[4,0]` | PASS |
| C1 N09, r99 battery, x3 | `unmet 104/105`, failed exactly `["REFUSAL-VERSIONS-9DIGIT-Y"]` | exactly, 3/3 runs, Y `[0,4]` | PASS |
| C1 N09, r98 do-nothing control, x3 | `met 105/105` (blind) | exactly, 3/3 runs | PASS |
| C1 N11, r99 battery, x3 | `unmet 103/105`, failed exactly `["EXPLICIT-VERSION-ERA","REFUSAL-VERSIONS-9DIGIT"]` | exactly, 3/3 runs, X `[0,4]`, EXPLICIT-VERSION-ERA `[3,1]` | PASS |
| C1 N11, r98 do-nothing control, x3 | `unmet 104/105`, failed exactly `["EXPLICIT-VERSION-ERA"]` — the delta | exactly, 3/3 runs | PASS |
| C1 the two new lie kinds | both read `unmet` | `93/105` and `95/105`, X and Y in the failed set, 0 error rows | PASS |
| C1 the drafted `N10-z-echo` twin bend, re-derived by this seat | a twin: the r98 control already rejects it | both batteries read identically `unmet 104/105 ["REFUSAL-VERSIONS-9DIGIT-Z"]` | PASS (twin confirmed) |
| C2 `--selftest`, r99 / r98 control | `PASS 17/17` / `PASS 14/14` | exactly, rc 0 both | PASS |
| C2 hybrid fixture, r99 / r98 control | r99 `FAIL` one `RC-CELL-MISSING`; r98 `PASS 7/7` | exactly, rc 1 / rc 0 | PASS |
| C2 restated fixture, r99 / r98 control | r99 `FAIL` one `RC-CELL-AMBIGUOUS`; r98 `PASS 7/7` | exactly, rc 1 / rc 0 | PASS |
| C2 clean and gap fixtures | both `PASS 7/7` on both checkers | exactly | PASS |
| C2 the M07 mutant, re-derived | r99 `FAIL 16/17`, exactly `ancestor` red | exactly (`ancestor FAIL rc=0 … PASS`); the same mutation on the r98 control reads `PASS 14/14`; the mutant digests are byte-identical to the frozen ones (`1ac9857f…`, `cba14ee1…`) | PASS |
| C2 coverage gate at the pre-round tip | `PASS 160/160 findings 0` | `PASS`, `registered 160 / rows_total 160 / tools_total 160`, `findings []`, rc 0 | PASS |
| census before → after | both exits, 0 E findings | exit 0 / 394 rows before, exit 0 / 395 rows after, 57 W04 + 1 W01 both times | PASS |
| Gate source S395 | byte-level anchors | `def meta_ok` 99305, echo assertion 99430, era assertion 99523, five `check_echo` sites 79015/79893/81666/83173/84390, five `check_era` sites 79039/80414/81690/83197/84414, `LIE_KINDS` members 108455, gate MAIN returns 16931/17037 (early returns 11230/11344) | PASS |
| Gate source S392 (re-open) | byte-identical to the pin | 331022 bytes, sha256 `d92580dd…`; offsets 153202 / 157767 / 159315 re-measure (the URL now 301-redirects; the bytes do not) | PASS |
| Gate rejected candidate | limine v12.9.6 `CONFIG.md` | HTTP 200, 27609 bytes, sha256 `f44f3a19…`; `grep -c` → 0 for `limine_version`, `visibility_era`, `echo` and even `version` | PASS (rejected) |

## Findings for the L1

1. **The twin bend's cited receipt does not exist in the tree.** The plan (BYTE 5640 of
   `.ufo/plans/round-99.md`), the knowledge entry (BYTE 3609 of
   `corpus/knowledge/limine-metadata-cap-families-r99.md`) and the draft lesson (BYTE 3418 of
   `corpus/lessons/round-99.md`) all cite a `before/dev/c1-N10-twin-r98*.json` that is absent
   (`find .ufo -name 'c1-N10*'` → no output). The reading they assert is **true** — this seat
   re-derived the bend and measured it — so the fix is to commit the receipt under `before/dev/` or
   re-point the citations, not to change any claim. The r98 lesson carries the same defect
   uncorrected (BYTE 12138, `MutRegistry/probe-nonancestor.txt`, also absent).
2. **The draft lesson's in-place registry table names edits that did not happen.** `git diff
   --numstat corpus/SOURCES.md` → `1  0` and zero removed lines: the S395 row was *added* already
   carrying `status mined` and its two `used-by` paths. There is no `queued` → `mined` transition.
3. **The draft's census block cites a receipt that carries only the after exit.**
   `before/census-before-after.txt` holds `after exit=0` and the two row counts, but no *before*
   exit code. This seat ran the before census itself: `EXIT_BEFORE=0`.
4. **A seat-harm disclosure belongs in the round's lesson.** At ~11:24 a sibling seat ran
   `rm -rf /fast/scratch/hyaku/tsukuroi-r99` (the shared parent), removing this seat's scratch
   tree mid-measurement. Every receipt cited here was re-derived after the wipe and written
   straight into the seat dir; the re-derived readings agree with the committed `before/dev/`
   receipts wherever the same leg exists there. The sibling disclosed it to the L1 and in
   `w1/CriticClaims.md` §7b.

The lesson's three mined mistakes are **R99-TWIN-BEND** (a near-miss control the do-nothing
instrument already rejects witnesses the predecessor, never the round — the rule that follows: a
bend is committed only when the control reads a different verdict on it), **R99-X-LIMIT-DELTA** (a
limit closes by the *marginal* discrimination over the do-nothing control — the delta in the
failed-family set, not the verdict — and a closure sentence naming a family must name the family
whose reading changed), and **R99-TWIN-RECEIPT-ABSENT** (a reading may be true and still have no
committed receipt behind it).

{"seat":"ScribeLesson","verdict":"findings","notes":"Lesson drafted at .ufo/waves/round-99/w1/ScribeLesson/corpus/lessons/round-99.md (Gate with 3 source rows + census before/after and both exits; Mistakes with 3 rows each naming red-before and fix — R99-TWIN-BEND, R99-X-LIMIT-DELTA, R99-TWIN-RECEIPT-ABSENT; scoreboard 22 rows met/owed; Routed 8 rows). All readings re-derived by this seat: landed gate met 105/105 x3; N09 r99 unmet 104/105 [Y] x3 with r98 control met 105/105 x3 (blind); N11 r99 unmet 103/105 [EXPLICIT-VERSION-ERA,X] x3 with r98 control unmet 104/105 [EXPLICIT-VERSION-ERA] x3 (the delta); N10 twin bend re-derived and measured — both batteries read identically unmet 104/105 [REFUSAL-VERSIONS-9DIGIT-Z], confirming the twin; r99 selftest PASS 17/17, r98 PASS 14/14; hybrid/restated fixtures r99 FAIL one frozen finding each where r98 reads PASS 7/7; M07 mutant FAIL 16/17 exactly ancestor red (digests byte-identical to the frozen ones) while the same mutation on r98 reads PASS 14/14; coverage PASS 160/160 findings 0 at the pre-round tip; census exit 0/394 rows before and exit 0/395 rows after, 0 E findings both; S392 byte-identical to the pin and limine v12.9.6 CONFIG.md rejected. FINDINGS: the twin's cited receipt before/dev/c1-N10-twin-r98*.json is absent although three landed files cite it (plan BYTE 5640, knowledge BYTE 3609, draft lesson BYTE 3418) — same class as r98's absent MutRegistry/probe-nonancestor.txt (BYTE 12138); the draft lesson's in-place registry table names S395 edits that did not happen (numstat 1 0, zero deletions); the draft's census receipt carries only the after exit (before exit measured here = 0); a seat-harm disclosure belongs in the lesson. Scratch deleted; no tool installed; no pacman; no mutating git/jj command."}
