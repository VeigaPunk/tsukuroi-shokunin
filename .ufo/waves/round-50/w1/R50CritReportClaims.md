VERDICT: defect-found

Item D-16: attack the wording of the three frozen claims — for each, name a reader who can
re-derive the after-state with one command over committed bytes, and compare the FROZEN.md
predicate sentence with the counter's `PREDICATE` constant, the `ok =` expression and the
receipt's label. Freeze rev 8029cdba1049df25632c91a23c8db4eefb54be5f ($R below). Receipts:
`.ufo/waves/round-50/w1/R50CritReportClaims/receipts.txt` (counter outputs re-run by me).

## Summary

| Claim | Declaration ≡ PREDICATE | PREDICATE ≡ `ok =` | Receipt label | One-command re-derive |
|---|---|---|---|---|
| C1 | YES (FROZEN.md:21 = c1.py:105-106) | YES (c1.py:445-446 identical) | NO — stale `r49` name | PARTIAL — marks legs unresolvable from committed text |
| C2 | YES (FROZEN.md:22 = c2.py:50-51) | **NO** — `pass_runs == a.runs` (c2.py:129-130) | NO — K-pass ran `--runs 1` | YES for the named command; receipts used a weaker rule |
| C3 | YES (FROZEN.md:23 = c3.py:77-79) | YES, via variable aliasing | YES | PARTIAL — needs working-tree checker + sibling live tips |

## Finding 1 (defect, C2) — the enforced rule is not the declared rule

- FROZEN.md:22 predicate: `... and pass_runs == 2 and case_ok == 1`.
- `tools/check-selftest-matcher-r50.py:50-51` `PREDICATE`: identical string.
- `tools/check-selftest-matcher-r50.py:129-130`: `ok = (idiom_sites == 0 and base_misses > 0
  and full_misses == 0 and cases == 168 and pass_runs == a.runs and case_ok == 1)` — the
  threshold is the CLI knob, not the literal 2; `--runs` default 2 (line 150).
- `controls/battery.py:206`: every C2 control, including K-pass, was run with `'--runs', '1'`.
- `controls/battery-summary-r50-c2.jsonl`: all four records show `"pass_runs": 1`; the K-pass
  record `{"control":"K-pass freeze census","got":"PASS","legs":{"pass_runs":1,...}}` — a PASS
  that does not satisfy the frozen predicate sentence.
- Direct reproduction: `python3 <c2.py> --revision $R --scratch <dir> --runs 1` →
  `{"verdict":"PASS","pass_runs":1,"runs":1,"predicate":"... pass_runs == 2 ..."}` (receipts.txt).
  The counter emits a self-contradicting receipt: the printed predicate is false of the same
  JSON line's legs. `--runs 0` cannot smuggle a PASS (cases stays −1 ≠ 168), but `--runs 1`
  halves the repeated-success leg.
- The claim's named command (no `--runs`) does reproduce the declared rule: my default run
  → `{"verdict":"PASS","pass_runs":2,"runs":2}` (receipts.txt). So the measurement command is
  honest; the control battery is not the claim's rule — the r42 pattern (rule changed after a
  seat scored), inverted: the *receipts* were produced under a weaker rule than the claim states.
- Smallest safe correction: hard-code the literal — `ok = (... and pass_runs == 2 and ...)` and
  refuse `a.runs != 2` unless `--fixture` is passed; or run the battery with `--runs 2`. One line.

## Finding 2 (defect, C1) — the receipt's label names the round-49 counter

- `tools/check-scrub-admission-r50.py:437`: `out = {'counter': 'check-scrub-admission-r49', ...}`
  — the r50 counter signs its receipts with the r49 name.
- Already observable in sibling receipts: `w1/R50RevCounterC1/receipts.jsonl:1`
  `{"counter_field":"check-scrub-admission-r49",...}`; every `w1/R50LabParse/*.json` has
  `"counter":"check-scrub-admission-r49"`. The round-50 receipts for C1 will be labelled
  `r49`, and they coexist with the actual round-49 file `tools/check-scrub-admission-r49.py`
  (a sibling seat, item D-12, is instructed to run it) — false provenance: the label cannot
  distinguish which binary produced the verdict.
- Smallest safe correction: `'counter': 'check-scrub-admission-r50'` at c1.py:437. One word.

## Finding 3 (defect, C1) — the counter's prose names the wrong round

The docstring is stale against the code:

- c1.py:26-27: "wave universe R49RevGR<n>a..c / R49CritGR<n>a..c"; code `universe()` at
  c1.py:307-310 builds `R50Rev/R50Crit`.
- c1.py:34-36: marks are `## Gate status — round 49 (GR1-GR3 admitted)`, `## Scrub
  grounding — round 49 admission`, README `admitted round 49`; code constants c1.py:96-98
  are all `round 50`.
- c1.py:51: `Usage: python3 tools/check-scrub-admission-r49.py ...`.

For C1 no committed text carries the three mark strings that satisfy `marks_ok`: FROZEN.md:21
says only "the SKILL/README marks" may be edited post-wave, and the freeze prose names
`## Gate status — round 50` (FROZEN.md, "row bytes are frozen" §) — consistent with the
constants — but a reader following the docstring would write `round 49` marks and score
`marks_ok 0`. My run of the C1 counter at the freeze (receipts.txt): `{verdict:"FAIL",
corr_ok:1, quotes_ok:3, verdicts_ok:0, seats_ok:0, marks_ok:0}` — the marks are unwritten at
freeze, so the one-command reader learns *that* marks fail, not *what* bytes would satisfy
them; the only committed description of those bytes is the docstring, which is wrong.

## Finding 4 (defect, C3) — two legs are not over committed bytes

- `anchors_checker_rc`: c3.py:352 runs `sys.executable <lane>/tools/check-adjacency-anchors.py
  --revision <REV>` — the **working-tree** script, not `<REV>` bytes. Today the tree copy is
  byte-identical (sha256 `a4f500ef…` = `git show $R:` blob, `git status` clean), so this is a
  latent hole: any post-freeze edit to the anchors checker changes C3's verdict without any
  committed-byte change. Compare the C2 counter, which faithfully re-executes `<REV>` bytes
  (c2.py:91-97 `git show {rev}:{CENSUS}` → scratch). The C3 command cannot run on a bare
  `git archive` checkout for the same reason.
- `live_quote_ok`: c3.py:152-158 does `git rev-parse HEAD` + `git show <tip>:PROVINCE.md` in
  each sibling checkout under `SIBLINGS` (c3.py:80 = `/home/vgpnk/Projects/shokunin`). These
  are mutable, non-committed (to the lane) state; `>= 8` gives one missing-quote tolerance,
  but the leg is not reproducible from lane bytes — a reader needs the sibling repos on disk
  at whatever tips they carry. The claim's prose ("the quote again at the sibling's live tip",
  FROZEN.md:23) is honest about this; the deficit is re-derivability, not wording.
- Predicate-vs-`ok` here is clean: `ok =` (c3.py:366-368) tests the same nine conditions under
  aliases (`len(adj)`↔`adj_rows`, `linked`↔`linked_rows`, `bare`↔`bare_ranges`,
  `checker_rc`↔`anchors_checker_rc`, `pin_ok`↔`quote_at_pin_ok`, `live_ok`↔`live_quote_ok`),
  and the emitted JSON keys map 1:1 (c3.py:358-365). Verified live: counter at $R → PASS,
  all legs at the declared thresholds (receipts.txt).
- Smallest safe correction: extract the checker via `git show {rev}:{CHECKER}` into the
  counter's own temp dir and run that; and record each sibling's tip SHA in the output so a
  reader knows which live state was measured.

## Finding 5 (shared) — the frozen command runs mutable counter bytes

All three claim cells read `python3 tools/<counter>.py --revision <REV>` (FROZEN.md:21-23).
That command runs whatever counter bytes sit in the working tree — the lane's mutable surface —
against `<REV>` bytes. None of the counters binds its own bytes: C2 emits `census_sha256`
(informational, not in the predicate; c2.py:132) and no counter emits a self-digest. A reader
re-deriving the after-state by the printed command verifies `<REV>`'s *data* but the *rule*
is the tree's current file. The honest one-command reader (which my runs used) is
`git -C <lane> show <REV>:tools/<counter>.py > x.py && python3 x.py --revision <REV>`; the
claims should name that form, or add a `counter_sha256` leg.

## Per-claim reader answer

- **C1**: yes, one command over committed bytes (`git show $REV:tools/check-scrub-admission-r50.py |
  python3 - --revision $REV` against the post-wave integration commit) — entry, SKILL, README,
  snapshots, reports, dispatch and w1-results all resolve via `git show REV:` (c1.py:172-174,
  184, 195, 338). But the *wording* must carry the r49→r50 label repair (Finding 2) and the
  mark strings exist nowhere in committed prose (Finding 3).
- **C2**: yes for the named command — verified, PASS with `pass_runs:2` at $R (56 s wall time)
  — but the frozen predicate is not the `ok =` rule (Finding 1) and every pre-data receipt was
  produced under `--runs 1`.
- **C3**: no — needs `<lane>` working tree (the anchors checker) and the sibling checkouts at
  `/home/vgpnk/Projects/shokunin/<sib>-shokunin` HEAD (today: kagi 69b61db…, kaidoku b6f7ca2…,
  kama 7ee8cbd…, kumitate 14057f3…, mado 3b55b6e…, mori 325f7e6…, revenger 6defe31…, tameshi
  21eb3c6… — observed via `git -C <sib> rev-parse HEAD`).

## What I did not do

- Did not run the C1 measurement at the post-wave integration commit: `w1-results.json` does
  not exist at lane tip 39e69493 (`git cat-file -e` → path absent); the cohort is in flight.
- Did not fuzz `--runs` beyond {default,1} or mutate sibling checkouts (read-only).
