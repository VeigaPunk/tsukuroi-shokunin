VERDICT: draft

# S-5 — considerthese mine (round-50 w1, seat R50ScoutConsider)

Axes: freshness (newest operator file at freeze `8029cdba1049df25632c91a23c8db4eefb54be5f`), fit to C1/C2/C3, a landing the bar already uses, and no new predicate. Blobs cited below match that freeze (`git rev-parse FREEZE:path` equals `git hash-object`). No tool installed. Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ScoutConsider` was created and removed; nothing was built there. Counters were not run.

## Latest file

`considerthese/` at the freeze is seven files, `2026-10-19.md` through `2026-10-26.md`. Newest by mtime and by name: `considerthese/2026-10-26.md` (mtime 2026-10-26 14:08 -0300). Marker heading, line 15: `## Self-improvement ideas (proposed only, not acted on)`. The phrase "proposals only / not implemented" is the 2026-10-19 heading, not this file's.

| File:line | Proposal | Marker | Still open at the freeze? |
|---|---|---|---|
| `2026-10-26.md:17` | Burst-aware reading | proposed only, not acted on | No. Lesson `corpus/lessons/round-46.md:97` |
| `2026-10-26.md:18` | Counter-attack scoreboard | same heading | Partial. Tables stop at round 42 (`SKILL.md:3833`, `:3935`). `corpus/lessons/round-47.md:71` says the proposal remains open. `git grep 'Arms fielded' FREEZE -- corpus/lessons SKILL.md` prints only those two header lines. Round-48 and round-49 lessons contain no `considerthese` section. |
| `2026-10-26.md:19` | Seat-harm incident log | same | No. `corpus/lessons/round-45.md:124` |
| `2026-10-26.md:20` | Downstream patch-offset check | same | No. `corpus/lessons/round-42.md:53` |
| `2026-10-26.md:21` | Cross-note correction propagation map | same | No. `corpus/lessons/round-43.md:83` |

## One proposal

**Counter-attack scoreboard**, `considerthese/2026-10-26.md:18`. Exact words: "For each frozen counter, track how many attack arms the wave fielded, how many survived, and which class beat it (leak read, fixture literal, answer-key read)."

It is the only bullet in the latest file that is not closed, and it is the one this round's counters are about. C3 exists because the round-49 adjacency counter passed a shape-valid stub (`FROZEN.md:23`). C2 exists because the census selftest harness still used the pipe idiom the census body already bans (`FROZEN.md:22`). C1's four GR corrections are not attack arms; they are not a row of this ledger.

### What was opened

The proposal's own landing, not the reflection:

- Definition of an arm, `SKILL.md:3836-3838`: "An arm is one scored variant a wave seat built to pass a counter without the claimed work (or a counter mutant no control catches); beat means it reached the counter's PASS. Counted from the named reports, by hand, not by a script."
- Last data row, `SKILL.md:3939-3943`: round 42 only. Reading there: "the hole moved to the channels through which the code can see it is observed." No later table.
- Left open on purpose, `corpus/lessons/round-47.md:71`: "no longitudinal survivor ledger was added; the proposal remains open."

Arm that reached PASS after that table, committed in round 49:

- `tools/check-adjacency-table-r49.py:19-27` credits an anchor when the heading cell matches a shape and the quote cell is non-empty and at most 25 words. It does not compare the quote to the sibling blob.
- `.ufo/waves/round-49/w1/R49CritAdjA.md:65` calls the five static legs "a shape test, not an ownership test." Fixture A3 (`:100-102`, restated `:113-124`) replaces the ADJ table with a stub and reclassifies inbound pointers; "the full predicate returns PASS, rc=0."
- `.ufo/waves/round-49/w1/R49RevAdjB.md:112-119`: fixture M17 sets the pin to `` `kama-shokunin/PROVINCE.md` @ `deadbeef0000` `` and the counter returns PASS, `anchors_ok 7`. Fixture M19 sets the quote to `fabricated quote not from any sibling` and the counter returns PASS.
- `SCORECARD.md:3189` records the round-49 C2 adjacency claim **PASS** and the named limit: "the counter is a shape test — `R49CritAdjA` and `R49RevAdjB` show a stub table passes it."

That class is not one of the three names in the 2026-10-26 bullet (leak read, fixture literal, answer-key read). It is the class QUALITY 87 already names: a counter that credits content it does not read (`corpus/QUALITY.md:171`).

Not an arm, so not a scoreboard row:

- `.ufo/waves/round-49/w1/R49ExecSelfAssess.md:84-90` and receipt `race3.out:4` measure the banned idiom: at 96 KiB, "pipe-arm false misses 11/20". The same section (`:83`, `:95`) marks the link from that probe to the observed selftest FAIL as `[INFERENCE]`, because the captured `got:` planes are 2 220 bytes, under the ~64 KiB threshold.
- The rule the harness broke is already `SKILL.md:3869`: "never pipe a probe buffer into an early-exiting reader." At freeze the harness uses `buf_has` (`tools/tsukuroi-census.sh:2236-2239`). That is C2's repair, not a variant that made a counter PASS.
- `FROZEN.md:59-60`: K-pass runs "are never reported as the claim's measurement." They are not arms under `SKILL.md:3836-3838`. This wave's attack reports are not in the freeze. No round-50 `Arms fielded` count is stated here.

### Bar

| Form | Decision | Reason | Flip |
|---|---|---|---|
| Lesson | Admit one continuation | Same landing as `corpus/lessons/round-41.md:99`: a `### considerthese` section that counts arms from named reports. One new row is grounded (the round-49 adjacency counter). | — |
| QUALITY criterion | Refuse | Items 85-90 already require the beating classes as frozen controls. Item 87 is this stub. Item 1 requires a falsifiable claim; "keep a table" is not a predicate. Round 50 C3 K1 (`FROZEN.md:57`) is the content-free control 87 already asks for. | A committed arm reaches the counter's PASS by a class items 85-93 do not name, with the report path. Then a new numbered criterion whose failing example is that arm. |
| SOURCES row | Refuse | `corpus/SOURCES.md:5` columns are source, kind, tier, scope, anchor, teaches. This bullet names no external artifact. QUALITY 7 cites an S### row for an external claim; a reflection is not one (`FROZEN.md` calls the reflection a pointer). | A retrievable document that states the tracking rule is opened, with access date, pin, and a quote of at most 25 words, and a sentence in the lane uses it as support. |

Province: the row records this lane's own counter. It does not absorb a sibling. `PROVINCE.md:82` ("Out of province → report, never absorb") is not triggered.

### Exact proposed text

```
### considerthese — counter-attack scoreboard, continuation (`considerthese/2026-10-26.md:18`)

Mined again because the round-41 and round-42 tables were not extended. `SKILL.md:3833` and `:3935` are the only `Arms fielded` tables (`git grep` at the round-50 freeze). `corpus/lessons/round-47.md:71` left the proposal open. An arm is the definition at `SKILL.md:3836-3838`: a variant built to pass a counter without the claimed work; beat means that counter's PASS.

| Counter | Round | Arms fielded (reports) | Arms that reached PASS | Beating class |
|---|---|---|---|---|
| `check-adjacency-table-r49.py` | r49 | stub table A3 (`.ufo/waves/round-49/w1/R49CritAdjA.md:100-102`); pin `deadbeef0000` M17 and fabricated quote M19 (`.ufo/waves/round-49/w1/R49RevAdjB.md:114-116`) | A3 full predicate rc=0; M17 and M19 `anchors_ok 7` | shape-only credit (quote non-empty and ≤25 words). Not leak read, fixture literal, or answer-key read. QUALITY 87 already names the class. |

Not a row: the round-49 census selftest flake (`R49ExecSelfAssess.md:90`, `race3.out:4`, 11/20 false misses at 96 KiB). The seat marked the link to the observed FAIL as inference (`:83`, `:95`). The idiom breaks `SKILL.md:3869`; it did not make a counter PASS. Pre-data K-pass runs are not arms (`FROZEN.md:59-60`).

Rule taken: extend this table only from a named report where the counter returned PASS. A sensitivity probe, a K-fail, and a K-pass do not add a row.
```

## Not done

Did not run `check-selftest-matcher-r50.py`, `check-adjacency-table-r50.py`, or `check-scrub-admission-r50.py`. Did not re-execute `race3.sh`. Did not list attack arms in rounds 43-48; the grep shows no `Arms fielded` row for them, which is not a claim that none passed.
