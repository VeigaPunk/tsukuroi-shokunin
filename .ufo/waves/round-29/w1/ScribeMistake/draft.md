# Round 29 — Mistakes row (draft, seat ScribeMistake)

Verdict: one row drafted, `R29-SEAT-ATTRIBUTED-BY-TIMING`, captured by QUALITY 2, with a check that prints FAIL on the round-28 bytes at `81a061a67466c5e1be812814a895a4b5ed89b4ff` (three findings, exit 1) and exit 0 on a clean row. `corpus/lessons/round-29.md` does not exist yet (no such file under `corpus/lessons/`); this is the draft for its `## Mistakes` table.

## Why this candidate rather than the leak-census one

- The attribution mistake cost work that cannot be recovered: a named seat was cancelled and its findings were lost, while the writer was a different seat that disclosed itself. The row below records that whole chain in the round's own words.
- The leak-census candidate is real but narrower, and round 29 already absorbs it. The round-28 spot-check named two leaking files ("Scrub `GIT_*` in both batteries", `corpus/lessons/round-28-verifier-spotcheck.md:90`), while the probe at `81a061a` measures three (`check-adjacency-overlap.py --selftest` joins the two batteries: `.ufo/waves/round-29/measure/c2-before-81a061a67466c5e1be812814a895a4b5ed89b4ff.jsonl`, last line `leaking: 3`). The round-29 C2 declaration already widens the target from "the two batteries" to "every tool with a sandbox git write" (`SCORECARD.md:1104`), so a Mistakes row would restate a decision the declaration already took.
- The attribution mistake has no such absorption: round 28 appended a correction but no rule and no check, so the same L1 move (name a seat from assignment order plus timestamps) stays available in round 29 and later.

## Row (paste-ready, one table line)

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R29-SEAT-ATTRIBUTED-BY-TIMING | attribution without a trace | `corpus/lessons/round-28.md:49` at `81a061a67466c5e1be812814a895a4b5ed89b4ff` names seat RevFamilyB2 as the writer of the lane sandbox commits and adds "attribution is by assignment and timing, not by a process trace"; `:58` (Correction to R28-SEAT-COMMITTED-IN-LANE) names seat SentinelBattery instead (it ran `tools/mutants-adjacency-overlap.py` once with `GIT_DIR` at the lane `.git`) and records that RevFamilyB2 "was cancelled on a wrong suspicion; its findings are lost". Bound bytes: `.ufo/waves/round-29/w1/ScribeMistake/round-28-at-81a061a.md`, sha256 `75f28c1d7745e2b2be2aadf6eeec8f40003da0ef1fa78c66151f5fc6cad3420e` | QUALITY 2 | Before a named seat is blamed or cancelled, the record cites the seat's own artifact or a process trace (environ, argv, pid), and a later correction naming another seat fails it. Draft `check-attribution-trace.py` prints FAIL on the round-28 bytes: `python3 .ufo/waves/round-29/w1/ScribeMistake/check-attribution-trace.py --lesson .ufo/waves/round-29/w1/ScribeMistake/round-28-at-81a061a.md` gives `FINDING R28-SEAT-COMMITTED-IN-LANE UNTRACED`, `UNOWNED`, `REVERSED original=RevFamilyB2 correction=SentinelBattery`, `verdict findings=3 ... exit=1`, rc 1. Shown able to fail and to clear: deleting the correction leaves 2 findings, supplying a trace and the seat report leaves 1 (REVERSED only), the clean fixture gives `findings=0 ... exit=0`; selftest `cases=5 failed=0`. Landing under `tools/` with a registry row (QUALITY 70) is owed; this draft sits in wave evidence only |

## Evidence, bound to the revision under attack

- `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 81a061a67466c5e1be812814a895a4b5ed89b4ff:corpus/lessons/round-28.md` → 58 lines, sha256 `75f28c1d7745e2b2be2aadf6eeec8f40003da0ef1fa78c66151f5fc6cad3420e`, saved at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeMistake/round-28-at-81a061a.md`.
- `grep -cF "attribution is by assignment and timing, not by a process trace"` → 1, at line 49. `grep -cF "was cancelled on a wrong suspicion; its findings are lost"` → 1, at line 58. The seat id in the row cell is `RevFamilyB2`; the seat id the correction names is `SentinelBattery`.
- The lane tip at the time of this write was `3c94d7308e561832a0df0981cbc39dda270e32d8` (`rev-parse HEAD master origin/master`, all three equal), so the round-28 lesson bytes at `81a061a` and at the tip are the same file for this row's purpose; the check ran on the `81a061a` bytes saved above.
- Round-28 verification agrees the cancellation was wrong: `corpus/lessons/round-28-verifier-spotcheck.md:94` (routed defect 6) and `:90` (routed defect 2, the "both batteries" naming used as the rejected candidate).

## The check

`check-attribution-trace.py` (seat dir; sha256 `4280ab502a170856614ac6925b15b7eb9210b0aa20daac9ef675b2366c643aab`) reads a round lesson and parses `Mistakes` tables plus `Correction to <ID>` sections. Three rules, each one finding:

- `UNTRACED`: the evidence cell names a seat and disclaims a process trace ("not by a process trace", "attribution is by ... timing") while carrying no trace token (environ, GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE, argv, pid, strace, shell history).
- `UNOWNED`: the evidence cell names a seat as the actor but cites no `.ufo/` path carrying that seat's own name. A commit listing is not a writer trace.
- `REVERSED`: a correction section carries reversal wording ("is wrong", "wrong suspicion", "incorrect") and names a seat the row did not name.

Observed ladder (each run is `python3 check-attribution-trace.py --lesson <file>`):

| File | Findings | Exit |
|---|---|---|
| `round-28-at-81a061a.md` (real bytes) | 3: UNTRACED, UNOWNED, REVERSED | 1 |
| `mut-no-correction.md` (correction section deleted) | 2: UNTRACED, UNOWNED | 1 |
| `mut-traced-fixture.md` (synthetic: trace token plus a citation of the named seat's report) | 1: REVERSED | 1 |
| `fixture-clean.md` (compliant row) | 0 | 0 |

`--selftest` → `PASS` for `r28-live-shape`, `clean-cited`, `untraced-only`, `reversed-only`, `correction-other-id`; last line `selftest cases=5 failed=0`, exit 0. The three fixture mutations were derived from the real row text; `mut-traced-fixture.md` is synthetic and is not a claim about what happened (the historical row stays as committed).

## Limits and what is owed

- [unk] The check reads lesson prose, not process records. It refuses an attribution that carries no cited trace; it cannot show that a cited trace is correct, and a seat named in prose with a real trace token but wrong identity would pass `UNTRACED`.
- [inf] Rule text is tuned to this lane's lesson grammar (Mistakes table starting at column 3, `Correction to <ID>` headings). A different table layout needs a parser pass; the header skip is by the literal `ID`.
- Landing the check under `tools/` needs its registry row (QUALITY 70) and an L1 or operator decision; the selftest gives 5 cases, but a landing would want the decision recorded in `corpus/lessons/round-29.md` and a run from a lane export.
- No lane product file was edited; this draft and its fixtures live only under `.ufo/waves/round-29/w1/ScribeMistake/`.
