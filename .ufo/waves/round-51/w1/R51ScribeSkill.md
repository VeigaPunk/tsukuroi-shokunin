VERDICT: defect-found — the SKILL.md override rule the item names (`--control`) exists only in `tools/check-adjacency-table-r51.py`; `tools/check-scrub-admission-r51.py` has no such gate and prints PASS on fixture-overridden inputs (see Finding 1).

# R51ScribeSkill — SKILL.md round-51 append (drafts A and B)

Seat: R51ScribeSkill (wave w1, uncounted). Bytes read: SKILL.md, the entry, the counters, the lint and the C2/C3 instruments at the freeze `2732ee6c06108c031c4d8043239b994e0504eb2f`, via `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <rev>:<path>`. No command was run; the section texts below are drafts, and no lane file was written.

Tail format read: SKILL.md:4562-4605 (round-49 `## Scrub grounding — round 49 (...)` and the two round-50 `## Census selftest — ...` sections; each is prose, no table, bold only for the outcome sentence). Both drafts follow that shape.

## Draft A — use only if all three rows read `holds` (counted cohort settles)

```
## Scrub grounding — round 51 admission

Round 51 re-read GR1-GR3 with the counted 18-seat cohort of wave `w2` (`.ufo/waves/round-51/w2/`, seats
`R51RevGR<n>{a,b,c}` and `R51CritGR<n>{a,b,c}`): GR1 `holds` <k>/6, GR2 `holds` <k>/6, GR3 `holds` <k>/6, no
bound `partly` or `fails`. Counter `python3 tools/check-scrub-admission-r51.py --revision <REV> --wave-dir
.ufo/waves/round-51/w2 --results-file .ufo/waves/round-51/w2-results.json --dispatch-file
.ufo/waves/round-51/w2-dispatch.json` prints `structural_ok 1, lint_ok 3, quotes_ok 3, verdicts_ok 3,
seats_ok 18, marks_ok 3`. Row hashes at admission (`--section-hash`): GR1 <hash>, GR2 <hash>, GR3 <hash>.

Lint and gap block. `python3 tools/lint-grounding-r51.py --revision <REV>` checks each row's quotes against the
whole digest-pinned source line, resolves each prose `file:line` in the pinned snapshot, and compares the lines
cited outside the SOURCES.md declared ranges with the entry's `### Range gaps (R51)` block. Regenerate the block with
`python3 tools/lint-grounding-r51.py --revision <REV> --emit-gaps`, paste its output under that heading, and re-run the
lint until `lint_ok 3`. `--worktree` reads the uncommitted lane tree and is never evidence.

Instruments (C2). `tools/check-selftest-matcher-r51.py` scans the census for printf/echo/cat piped into an
early-exit reader, checks full-read sensitivity and applies two verdict-logic mutants. `tools/score-counter-cheats-r51.py`
builds four cheat censuses and scores the matcher against each: F1 a liar that prints the expected lines, F2 a
braced `printf '%s\n' "${out}" | grep -q` respelling, F3 an `echo "$out" | grep -q` respelling, F4 a neutered
`bad()` that counts failures as passes. Named limits: an alias, an `eval`, or a producer other than printf/echo/cat is
not seen; the two mutants test only the rollup and the exit map; a census with a real rollup and harness that selects
which cases run is faithful for these legs. A passing selftest is not proof of census behaviour.

Override rule. Only `tools/check-adjacency-table-r51.py` has the gate: any input override without `--control` exits 3
with `OVERRIDE-NOT-MEASURED`, and `--control` prints `CONTROL-PASS` or `CONTROL-FAIL`, never `PASS`. Overrides are
for control batteries only. `tools/check-scrub-admission-r51.py` takes fixture overrides (`--entry-file`,
`--wave-dir`, `--results-file`, `--dispatch-file`, `--no-base-check` and others) without that gate; a PASS on
overridden inputs is not a measurement.

Named limits. The admission counter is a shape gate: it does not prove a verdict's substance or stop a fabricated
result bundle. Admission rests on the orchestrator's real dispatch and results files, never on a hand-written
report set.
```

## Draft B — use if any row reads `partly` (cohort does not settle)

```
## Scrub grounding — round 51 (pending)

Round 51 re-read GR1-GR3 with the counted 18-seat cohort of wave `w2` (`.ufo/waves/round-51/w2/`): <row
counts>. Bound `partly` on <row>: <seat ids>, naming <the defect, quoted from the seat report, with its file:line>.
The counter `python3 tools/check-scrub-admission-r51.py --revision <REV> --wave-dir .ufo/waves/round-51/w2
--results-file .ufo/waves/round-51/w2-results.json --dispatch-file .ufo/waves/round-51/w2-dispatch.json` prints
<legs>, so the frozen predicate fails and **no row is admitted**. No admission mark is written; the heading and
README sentence stay unchanged.

Still open: <row>, <the exact clause or range that stays open>. The next amendment changes <row bytes only> and
re-reads with a fresh cohort; it does not narrow the counted predicate.

Lint and gap block. `python3 tools/lint-grounding-r51.py --revision <REV>` checks each row's quotes against the
whole digest-pinned source line, resolves each prose `file:line` in the pinned snapshot, and compares the lines
cited outside the SOURCES.md declared ranges with the entry's `### Range gaps (R51)` block. Regenerate the block with
`python3 tools/lint-grounding-r51.py --revision <REV> --emit-gaps`, paste its output under that heading, and re-run the
lint until `lint_ok 3`.

Instruments (C2). `tools/check-selftest-matcher-r51.py` and `tools/score-counter-cheats-r51.py`: four cheat censuses
(F1 liar, F2 braced-pipe respelling, F3 echo-pipe respelling, F4 neutered harness) against the matcher. Named limits:
aliases, `eval` and producers other than printf/echo/cat are not seen; two mutants test only the rollup and exit map;
a faithful-rollup census that selects its cases passes these legs.

Override rule. `tools/check-adjacency-table-r51.py` prints `OVERRIDE-NOT-MEASURED` (exit 3) for an input override
unless `--control` is passed, and `--control` never prints `PASS`. `tools/check-scrub-admission-r51.py` has no such
gate; its fixture overrides are for control batteries only.

Named limits. The admission counter is a shape gate, not a forgery gate, and does not prove verdict substance.
```

## Finding 1 (defect in the item's override rule)

The item asks the section to state "the override rule (`--control`)". In the frozen bytes that rule exists only in the C3
counter:

- `tools/check-adjacency-table-r51.py:208-210`: an override without `--control` prints `OVERRIDE-NOT-MEASURED` and exits 3
  ("an input override is a control, never a measurement; pass --control").
- `tools/check-scrub-admission-r51.py:40-41` documents "Fixture overrides (control batteries only ...)" but its `main()`
  (argparse block, read at the frozen rev) accepts `--entry-file`, `--skill-file`, `--readme-file`, `--sources-file`,
  `--wave-dir`, `--results-file`, `--dispatch-file`, `--no-base-check` with no `--control` argument, and `run()` prints
  `verdict: PASS` from `ok` (line 383) whatever the inputs. `grep -nE 'control|OVERRIDE'` on that file finds only the
  docstring line 40.

So the C1 counter, the counted instrument for this round, can print PASS on overridden bytes with no label. Draft A and B
word this honestly (the admission override is "not a measurement"). The L1 should decide before w2 whether to add a
`--control` gate to `check-scrub-admission-r51.py` (an amendment to a frozen counter, which the FROZEN record would have
to name) or leave the sentence as drafted. I did not change any counter.

## Finding 2 (named-limit wording check)

- The C2 scorer's own docstring (`tools/score-counter-cheats-r51.py`) names four cheats and "its named scope" as the
  four classes only; the drafts use exactly those four.
- The matcher's docstring names the same limits (alias/eval spelling, two mutants on rollup and exit map, faithful census
  that selects cases); the drafts repeat them, not more.
- The C3 counter's named limits (byte-substring quotes are not semantic entailment; sibling pins read from working checkouts;
  coordinated rewrite out of scope) are not in either draft because the item asked for the C2 instruments and the
  `--control` rule only. The L1 may add one line if wanted.

## Line counts

Draft A section body: 32 lines (fenced block, excluding the fences; measured). Draft B: 28 lines. Both under 40.

## Not done

- No counter, lint or selftest was run (the item names no command to run). The `<REV>`, row hash, count and `partly` fields are placeholders for the integrator.
- The gap block was not regenerated; the entry's current block at the freeze is what the draft points to, and the amendment may change it.
- Nothing was written to the lane, to SKILL.md, or to the fleet root.
