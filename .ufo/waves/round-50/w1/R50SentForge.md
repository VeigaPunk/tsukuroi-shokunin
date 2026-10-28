VERDICT: defect-found

# C1-B7 — sentinel forgery probe: the counted cohort can be fabricated end to end

Seat R50SentForge, wave w1, round 50. Counter under test: `tools/check-scrub-admission-r50.py` at
the freeze, staged to scratch as `counter-at-freeze.py`, sha256
`0af0e679ee82d608d6278d2575391b1a7dd53af49099e962349bddac35f333db`. Lane
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, revision
`8029cdba1049df25632c91a23c8db4eefb54be5f`. All runs used `--lane <lane>` and, where stated,
`--revision <fixture HEAD>`; every fixture lived in
`/fast/scratch/hyaku/tsukuroi-r50/R50SentForge` and was committed only inside a `--shared` clone
(`git rev-parse --show-toplevel` asserted equal to the fixture dir before the first commit,
`-c user.name=fixture -c user.email=fixture@invalid`). Scratch removed; receipts in
`.ufo/waves/round-50/w1/R50SentForge/`.

## 0. The freeze carries none of the cohort

```
$ git -C <lane> show 8029cdb...:.ufo/waves/round-50/w1-results.json
fatal: path '.ufo/waves/round-50/w1-results.json' does not exist in '8029cdba...'
$ git -C <lane> ls-tree --name-only 8029cdb...:.ufo/waves/round-50/w1/
fatal: Not a valid object name 8029cdba...:.ufo/waves/round-50/w1/
```

Production run at the freeze (no overrides): `rc=1`, `structural_ok 1, corr_ok 1, quotes_ok 3,
verdicts_ok 0, seats_ok 0, marks_ok 0`, first note `R50RevGR1a: unbound (not exactly one results
entry)` (`receipts/prod-rev.json`). Section hashes printed by `--section-hash` are exactly the
three in the frozen claim (GR1 `3a2ba18…`, GR2 `a2e955c…`, GR3 `43430a1…`).

The three round-50 marks are also absent at the freeze: `corpus/knowledge/btrfs-scrub-grounding-r45.md:297`
is `## Gate status — round 50 (pending; the round-50 cohort has not settled)`, `SKILL.md:4548` is
the round-49 heading, `corpus/README.md:488` says the rows `stay pending`. So no run against genuine
freeze bytes can reach `marks_ok 3` — a forged cohort alone stops at 5 of 6 legs, and the sixth leg
is two appended lines that the forger writes as easily as the scribe seats do.

## 1. Variants and what each produced

`forge.py` builds the cohort; `closeout.py` adds the marks; `substitute.py` runs the substitution.
Each row is the counter's own JSON, saved verbatim under `receipts/`.

| # | fabricated set | rc | structural/corr/quotes | verdicts | seats | marks | outcome |
|---|---|---|---|---|---|---|---|
| prod | nothing (freeze) | 1 | 1/1/3 | 0 | 0 | 0 | FAIL |
| **a** | 18 reports written by **one process** into `--wave-dir` + hand-written `--results-file`; dispatch read from the **real frozen** `w1-dispatch.json`; **no dispatch ran** | 1 | 1/1/3 | **3** | **18** | 0 | FAIL only on `marks_ok` (5/6) |
| b1 | forged `--dispatch-file` with decoy names only | 1 | 1/1/3 | 0 | 0 | 0 | FAIL — `dispatch agent None != reviewer` |
| b2 | reports/results under names absent from the real dispatch | 1 | 1/1/3 | 0 | 0 | 0 | FAIL — `not exactly one results entry` |
| b3 | forged dispatch carrying the universe names with **wrong roles** | 1 | 1/1/3 | 0 | 0 | 0 | FAIL — `dispatch agent 'critic' != reviewer` |
| **c** | universe names in the real dispatch, one body copied 18× with whitespace padding | 1 | 1/1/3 | 0 | **18** | 0 | FAIL — `distinct_bodies False` on all three rows |
| **c2** | same, each copy differing by **one citation line number** | 1 | 1/1/3 | **3** | **18** | 0 | FAIL only on `marks_ok` (5/6) |
| **d1** | (a) + the three mark lines, all via overrides | **0** | 1/1/3 | 3 | 18 | **3** | **PASS** |
| **d2** | d1 bytes **committed** in a fixture clone at parent REV, counter with **no overrides** | **0** | 1/1/3 | 3 | 18 | 3 | **PASS** at fixture HEAD `5a0b00435e34402d59bb32402a6d1efdd76977a1` |
| e1 | fixture cohort committed with every report saying `fails` | 1 | 1/1/3 | 0 | 18 | 3 | FAIL — all six seats per row `blocking` |
| **e2** | **same revision as e1**, plus `--wave-dir` holding the forged `holds` set | **0** | 1/1/3 | 3 | 18 | 3 | **PASS** at `59928be7e8a5d362664528b31a693c9c495e4463` |

**Which forged set passes:** (d1), (d2) and (e2) pass the full predicate `rc=0 PASS`. (a) and (c2)
pass five of six legs and fail only `marks_ok`, which the genuine freeze cannot supply either. (c)
fails as designed — the routed round-49 fix for whitespace padding holds. (b1/b2/b3) fail.

Two of these are sharper than "a forger passes":

* **d2** passes with **zero overrides**, on bytes committed at a revision whose parent is the
  freeze. `git diff --stat REV 5a0b004` is 19 added files (`w1/*.md`, `w1-results.json`) plus the
  three mark edits. "The reports are committed at REV" is therefore not evidence that any seat ran.
* **e2** prints `"revision": "59928be7e8a5d362664528b31a693c9c495e4463"` and `PASS`, while the
  committed report blob at that same revision is
  `b40ee10ef81d60304f2fadcfa0be95bc1a5f9700` = `ROW GR1 VERDICT: fails`, and e1 at that same
  revision printed `FAIL` with all 18 seats blocking. The `revision` field (`counter:437`) does not
  identify the bytes that were judged.

## 2. Which single leg stands between a forger and admission

Of the six predicate legs, five are shape checks on bytes the forger supplies or can read:

* `structural_ok`, `corr_ok`, `quotes_ok`, `marks_ok` are properties of the entry/SKILL/README, and
  the forger can read every required value out of the counter itself — `--section-hash`
  (`counter:456`) prints the three hashes the seat must echo, and the mark strings are literals in
  the source. d1 shows the marks are a two-line append.
* `seats_ok` (`counter:435`) counts any seat whose report parsed to a verdict —
  `sum(1 for s in seats.values() if s['verdict'] is not None)`. It is satisfied by 18 well-formed
  files; c and c2 both reach `seats_ok 18` with fabricated bodies.
* the dispatch leg is `tasks.get(seat) != role` (`counter:321`) against a JSON file, plus a truthy
  `output` string (`counter:328`). No run id, no transcript, no digest ties `w1-results.json` to the
  reports it claims to describe: variant (a) hand-writes it and passes.

The only leg that even attempts to detect non-independence is the **distinct-bodies** comparison
inside `verdicts_ok`:

```
426:            norm_body = '\n'.join(ln.rstrip() for ln in (body or '').split('\n') if ln.strip())
427:            bodies.add(hashlib.sha256(norm_body.encode('utf-8')).hexdigest())
429:        distinct = len(bodies) == len(credited)
```

That leg **does not stand**: it is a duplicate detector, not an independence detector. (c) shows it
catches literal copies and whitespace padding (`distinct_bodies False`, the routed round-49 fix
working). (c2) — one citation line number changed per copy — yields `distinct_bodies True` on all
three rows and `verdicts_ok 3`. A forger has to spend one character per seat to defeat it.

So the honest answer is: **no leg stands.** The nearest candidate is the distinct-bodies leg, and it
is defeated by a one-token variation; the rest are format and presence checks.

## 3. Does the real integration close it

Not inside the counter. The production path differs from the control path only in **where the bytes
are read from**: `read_text` (`counter:177`) and `load_json` (`counter:188`) consult the override
first and `git show REV:<path>` otherwise, and `bind_seat` takes the same branch for reports
(`counter:330`). There is no check that the revision is the dispatcher's revision, that a report
blob was written by the seat it is named after, or that `w1-results.json` was written by a
dispatcher. d2 is the direct falsification: no overrides, committed bytes, `PASS`.

What actually stands between a forger and admission is **out of band**: the lane's single-committer
rule (the L1 is the only committer, so a seat cannot land 18 report blobs) and the host guard that
forbids seats from writing tracked lane files. The counter contributes nothing to that boundary; its
verdict is a shape certificate about a set of files, not a record of dispatch.

## 4. Standing limit, stated plainly

The counter certifies: for each of GR1/GR2/GR3 there exist ≥3 credited reports, under the 18
hard-coded universe names, whose names appear in a JSON dispatch file with the declared roles, each
exactly one entry in a JSON results file with a truthy `output`, first two lines in the exact format,
`SECTION SHA256` equal to the value the counter itself prints, body ≥300 bytes with ≥2 distinct row
sources whose every `file:line` resolves, pairwise non-identical after whitespace collapse. One
process produces all of that in **under two seconds** (observed wall time: 1.73 s for the seven
variants, 1.54 s for d1+d2, 1.60 s for e1+e2). It does not certify that 18 seats ran, that any
report was written by the seat whose name it carries, or that `results.json` came from the
dispatcher. Two consequences the L1 must not paper over:

1. A `PASS` printed by a run that used `--wave-dir`, `--results-file`, `--dispatch-file`,
   `--entry-file`, `--skill-file` or `--readme-file` is evidence about scratch files, not about the
   revision named in its `"revision"` field (e2).
2. A `PASS` printed on committed bytes is evidence about the committer's diligence, not about
   dispatch (d2).

## 5. Smallest remediation

(1) Separate admission from control, so an override run cannot wear the admission verdict. After
`rev = a.revision` in `run()`:

```python
    overrides = (a.entry_file, a.skill_file, a.readme_file, a.wave_dir, a.results_file,
                 a.dispatch_file)
    if any(overrides) and not a.control:
        print(json.dumps({'error': 'fixture override without --control', 'verdict': 'FAIL'}))
        return 2
```

with `ap.add_argument('--control', action='store_true')` beside the other flags and
`'mode': 'control' if a.control else 'admission'` added to the `out` dict at `counter:437`. This
kills e2's contradiction and makes every control battery self-identifying.

(2) Bind `results.json` to the report bytes — in `bind_seat`, after `raw` is loaded and before
`text = raw.decode('utf-8')`:

```python
    raw_sha = hashlib.sha256(raw).hexdigest()
    if raw_sha not in (hits[0].get('output') or ''):
        return None, None, None, 'results output does not name the report sha256'
```

This removes the "hand-written results file with no relation to the reports" case (a, c2, d1, d2 as
built) and makes the dispatcher's record the anchor. It does **not** stop a single process that
writes both, and it does not stop d2 — no static check can. Closing d2 needs the dispatcher to
record `report_sha256` per seat at dispatch time, i.e. a provenance record produced **before** the
reports exist; that is an L1 design item, not a patch.

## 6. Observations, non-blocking

* `counter:437` emits `'counter': 'check-scrub-admission-r49'` and `counter:51` documents the r49
  usage line, while the file is `-r50`. Harmless to the predicate, but the artifact's self-label
  disagrees with its path — worth a one-line fix so a receipt cannot be mistaken for a round-49 one.
* `bind_seat` takes `hashes` and `cache` and never uses them; the hash and citation checks live in
  the caller. Dead parameters invite the reader to believe the binding is stronger than it is.

## 7. What I did not do

No build, no lane mutation, no `git add/commit` outside fixtures, no pacman (host-wide pause
respected), no installs, no subagents. I did not probe the C2 or C3 counters; this seat is scoped to
C1's cohort legs. Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50SentForge` removed after receipts
were copied (546 G free observed on `/fast`).
