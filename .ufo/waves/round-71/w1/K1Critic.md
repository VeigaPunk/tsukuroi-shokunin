# K1Critic — round 71 w1 report (falsify C1 and C2 against the declaration's receipts)

Frozen declaration `0fcfca31` (base `930d5530`). Lane tree untouched; sandbox clone only; scratch removed.
Full analysis: `.ufo/waves/round-71/w1/K1Critic/critique.md`; raw command/output: `…/K1Critic/receipts.txt`.

## Verdict

- **C1 — not falsified as a target, but its predicate cannot establish its headline.** The after-state
  is one-command re-derivable over committed bytes (`python3 tools/count-mp-rows-r71.py --revision <REV>`
  → `met=1`; demonstrated at clone `51d2357`). Six channels let a note pass while stating what the
  snapshot does not say — the strongest is a row that **contradicts `params.c:709-710`
  (`if (kparam[i].perm == 0) continue;`) and still reads `MP_VERIFIED=6 … met=1`** on the real committed
  snapshots and the real registry row shape.
- **C2 — the declared target is reachable by a do-nothing control.** Three no-op `ok` calls labelled
  `R71-C2` and **zero** timeout machinery print `PASS (217 cases, 217 passed, 0 failed)` rc 0 in 46 s
  (labels 4, timeout tokens 0). The claim's kill rule (harness-removed mutation) closes it only if the
  after-state carries that mutation receipt; the frozen counting command does not.

## Receipts (a)–(f): 20 of 24 declared receipt rows reproduce

All four snapshots are byte-identical to live upstream `git.kernel.org` at `h=v7.2.11`; host capture is
byte-identical to `host.txt` (date line excepted); novelty sweep, counter pin `fa67…`, 11-case battery,
214-case baseline, live `DEGRADED` rc 1 and red-before `rc=124 0 verdicts` all reproduce.

Four items do not:

| # | Defect | Evidence |
|---|---|---|
| D1 | (b) says "4 under `/usr/lib/modprobe.d`" | committed `host.txt` and the live rerun list **5** |
| D2 | (d) "canonical census validate rc 0" | no entry point: 0 `validate` occurrences in the base census; the same unlabeled value was already flagged at round 70 (`round-70/w1/K1Critic.md:117`) |
| D3 | (e) "12 cases: 1 control + 11 mutants" | `battery.py` registers 1 + 10; `battery.txt` prints `BATTERY cases=11` |
| D4 | (e) `mutant-duplicate-id` | killed by `MP_ROWS=7` + `snapshot-reuse params.c=3`, never `duplicate-id`; the clause itself works (true MP2-twice fixture prints `duplicate-id` + `ids-not-contiguous`) |

## Predicate channels (10: C1 6, C2 4; 7 demonstrated)

| Channel | Counterexample | Clause that fails to close it |
|---|---|---|
| C1-1 lexical grounding | contradiction of params.c:709-710, 6/11 tokens, met=1 | `statement-grounding` |
| C1-2 token salad | `"return static struct const char unsigned …"`, 10/11, met=1 | same |
| C1-3 empty quote | `quote=""`, met=1 (substring of everything) | `quote-absent`/`quote-words` |
| C1-4 irrelevant quote | `quote="the"`, met=1 | none (location-only check) |
| C1-5 rejected registry row | S297 marked `rejected`, met=1; counter never reads `cells[8]`; the newest live rows S294–S296 are rejected | `source-registered`/`source-not-bound` |
| C1-6 multi-URL substring binding (named) | `url in source_cell`, `basename in anchor_cell` are substring tests | `source-not-bound`/`anchor-not-bound` |
| C2-1 do-nothing control | `PASS (217 cases, 217 passed, 0 failed)` rc 0, 0 timeout tokens | counting command never executes a bound |
| C2-2 comment label | `grep -c 'R71-C2'` counts a comment | labels |
| C2-3 self-check not wired to runner (named) | helper-only bound still prints 217/217 | "self-check proves the bound" is prose |
| C2-4 neutrality uncounted (named) | rollup/exit not compared A/B | none in the counting command |

## Sizing

- C1 one command over committed bytes: **YES** — `python3 tools/count-mp-rows-r71.py --revision <REV>`
  (caveat: the counter executes from the worktree, pinned by sha256 `fa67…`; the registry `296→300`
  half is a second command).
- C2 do-nothing control cannot reach: **NO** — see C2-1.

## Smallest safe corrections (next round; no substitution this round)

C1: non-empty quote ≥3 words; ≥4 shared non-stopword tokens between statement and **quote**; read the
registry status cell and require `mined`; bind URL/basename at word boundaries.
C2: add the harness-removed mutation arm to the counting command; count distinct case labels, not `ok`
calls; add the R70-style A/B rollup neutrality case.

KEY=VALUE
RECEIPTS_REPRODUCED=20/24
DEFECTS=4
PREDICATE_CHANNELS=10
