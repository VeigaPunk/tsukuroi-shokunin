# Round 48 (attempt 2) — frozen record

The freeze revision is the lane commit that adds this file: `git log -1 --format=%H -- .ufo/waves/round-48/frozen/FROZEN.md`.
Everything below was committed BEFORE any seat of the counted wave `w2` existed. Attempt 1's `w1` (void; see SCORECARD.md
"Round 48 — declaration") is not part of this record.

| Frozen item | Path | sha256 |
|---|---|---|
| census blob under test (C1) | `tools/tsukuroi-census.sh` | `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426` |
| C1 counter | `tools/score-selftest-tmpdir-r48.py` | `8eead161e990e9e6f5155984797396d79fe7a3e6524a1a0c3087758658625640` |
| C2 counter | `tools/check-scrub-admission-r48.py` | `eab290589fe2a8d3e900d41891bee688dd36250928aa93678b68cad5895284d4` |
| C3 counter (unchanged since the round-47 tip) | `tools/check-self-assessment.py` | `44b474fb5401559d9a4052f04f03145cd165a688a78455694d7dd25dba5838e6` |
| C2 row hashes | `.ufo/waves/round-48/frozen/gr-section-hashes.json` | GR1 `fe77ac76…9ca8`, GR2 `e0b391e1…52ce`, GR3 `43430a14…c32c` |

Base: `5fdf062f969292736e36513e39f98b1b8de43635` (lane tip at round start). Implementation commits before the freeze:
`174a2c79` (census fix, counters), `d7843b3a` (adjacency IN-109 repin 2593 -> 2642, counter PASS-line fix).

Predicates (the same sentence in the SCORECARD declaration, the counter code and the receipt label):

- C1: `pass_ok == 4 and loc_ok == 4 and clean_ok == 4 and failfast_ok == 2 and term_ok == 1 and static_ok == 1`
- C2: `structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`
- C3: `check-self-assessment.py` status PASS, checked 27, mismatches 0 at the final lane revision.

Rule discipline: no counter, predicate, kill rule or entry row is edited after the first seat scores. The L1 measures every
claim on these bytes only; a miss is an honest stop and is never narrowed after the fact.

Controls (run with the frozen counters, receipts committed): `controls/battery-summary-r48-c1.jsonl`,
`battery-summary-r48-c2.jsonl`, `battery-summary-r48-c3.jsonl`; drivers `battery-c1.py`, `battery-c2.py`, `battery-c3.py`.
Wave spec generator: `.ufo/waves/round-48/make-w2-spec.py` (output `w2-spec.json`, validated, `w2-dispatch.json`).
