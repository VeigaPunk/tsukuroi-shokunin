VERDICT: defect-found

# R49CritCounter — C1 cheat battery (item C1-B4)

Seat class EXEC-AUTHORIZED. Fixtures only, in `/fast/scratch/hyaku/tsukuroi-r49/R49CritCounter/` (removed
after the receipts were copied). No lane byte was edited; every counter run used the FROZEN counter bytes
(`git show 55c07cd:tools/check-scrub-admission-r49.py`, sha256
`3dd52ef376e233192f955208c1132f6b0d23bbebe97dd1df75e6296f55d970a4`, identical to the lane working copy
`tools/check-scrub-admission-r49.py`). Receipts: `.ufo/waves/round-49/w1/R49CritCounter/`
(`cheat.py`, one JSON per scenario, `summary.json` = frozen-counter run, `patched-summary.json` =
validation run, `counter-frozen.py`, `counter-patched.py`, `patch-proposal.diff`, fixture
`entry-good.md` / `entry-o.md` / `entry-o2.md` / `readme-neg.md`).

Command shape per scenario (the item's override form):

```
python3 counter-frozen.py --lane <lane> --revision <REV> --no-base-check \
  --entry-file <fx> --skill-file <fx> --readme-file <fx> \
  --wave-dir <fx/cohort> --results-file <fx/res.json>
```

**Two form changes were forced by the counter itself** (finding D9): the dispatch leg has no
`--dispatch-file` override and `.ufo/waves/round-49/w1-dispatch.json` does not exist at the freeze revision
(first appears at `32a85560`). At `--revision 55c07cd` every seat binds `None`
(`F0-mandated-rev-freeze.json`: `seats_ok 0`, `seat_notes[0] = "R49RevGR1a: unbound (dispatch agent None !=
reviewer)"`), so scenarios were scored at `--revision 32a85560` (same entry bytes, sha256
`81ce009f…20546` at both revisions). This is also the revision the frozen controls used.

## Result: 9 of 9 cheat families that matter reach `PASS` on the frozen counter

`summary.json`: 22 scenarios, 10 PASS = the honest control `C0` + **9 fabricated cohorts**. The predicate
printed by every passing cheat is the full target:
`structural_ok 1, corr_ok 1, quotes_ok 3, verdicts_ok 3, seats_ok 18, marks_ok 3 → verdict PASS, rc 0`.
The 300-byte citation floor and the distinct-body rule do not bind:

| Scenario (item letter) | Fixture | Frozen | Patched | Defect |
|---|---|---|---|---|
| C0 honest control | distinct bodies, 2 row-source citations each | PASS | PASS | — |
| A (a) 18 identical bodies | one body copied to all seats | FAIL (`verdicts_ok 0`, `seats_ok 18`) | FAIL | — |
| A2 (a) identical + one trailing space | byte-differing padding | **FAIL but GR1 credited** (`verdicts_ok 1`) | FAIL | D8 |
| B (b) one sentence + 300 pad + one cite | `Read. ` + 300×`x` + `cmdline.c:147` | **PASS** | FAIL | D2 |
| B2 (b) citation of line 1 | same, aiming at `cmdline.c:1` = `// SPDX-License-Identifier: …` | **PASS** | FAIL | D2 |
| C1 (c) bound-format contradiction | GR2 critic body adds `ROW GR2 VERDICT: fails` | FAIL (`verdicts_ok 2`) | FAIL | — |
| C2 (c) free-text contradiction | every body: "This row is false … must not be admitted" | **PASS** | FAIL | D3 |
| C3 true cross-row token | GR1 body cites `ROW GR2 VERDICT: holds` (true) | FAIL (`verdicts_ok 2`) | PASS | D4 |
| D (d) empty `output` | `"output": ""` ×18 | FAIL (`seats_ok 0`) | FAIL | — |
| D2 (d) whitespace `output` | `"output": " "` ×18 | **PASS** | FAIL | D5 |
| E (e) duplicated seat | `R49RevGR1a` twice in `results` | FAIL (`seats_ok 17`) | FAIL | — |
| E2 (e) duplicated seat, same agent | `R49CritGR3c` twice | FAIL (`seats_ok 17`) | FAIL | — |
| F1 (f) one r48 defect string reintroduced (outside rows) | `dev-replace.c:1171-1199` appended | FAIL (`corr_ok 0`) | FAIL | — |
| F2 (f) one defect string inside GR1 | same string in the row | FAIL (`corr_ok 0`) | FAIL | — |
| O corrections parked in an appendix | base rows, defect sentences deleted, no correction fact added | **PASS** | FAIL (`corr_ok 0`) | D6 |
| O2 corrections explicitly denied | "The following corrections were NOT made:" + the 7 sentences | **PASS** | FAIL | D6 |
| H 9 of 18 seats with zero hash | 9 seats `SECTION SHA256: 000…0`, 9 correct | **PASS** (`seats_ok 18`) | FAIL (`seats_ok 9`) | D1 |
| I full mock, zero reading | H + padding bodies with irrelevant citations + `" "` output | **PASS** | FAIL | D1/D2/D5 |
| M negated README mark | `…entry is **not** admitted round 49.` | **PASS** (`marks 3/3`) | FAIL (`marks 2`) | D7 |
| G (extra) wrong row token | GR1a file says `ROW GR2` | FAIL (`seats_ok 17`) | FAIL | — |
| L (extra) CRLF report | one file written with `\r\n` | FAIL (`seats_ok 17`) | FAIL | — |

The exact item asks, answered: **(b) the citation floor does not bind** — 300 bytes of `x` plus one existing
line number is credited, and the line need not touch the row's clause; **(c) only the exact bound token
blocks** — a body asserting the row is false is credited `holds`; **(d) an empty `output` fails but a single
space passes**; **(e) duplicate seat names fail** (that seat unbinds); **(f) a reintroduced defect string
fails** both inside and outside the rows.

## Findings (frozen counter, `tools/check-scrub-admission-r49.py` at 55c07cd)

**D1 (high) — half the cohort need not verify the section hash.** `seats_ok` counts any well-formed
first/second line: `seats_ok += sum(1 for s in seats.values() if s['verdict'] is not None)` (:383) while a
hash mismatch only appends a note (:368-369). Evidence `H-loose-seats.json`: 9 seats report
`SECTION SHA256: 000…0`, the counter itself prints `R49RevGR1c: hash 000… != 3a2ba180…`-style notes, and
`seats_ok` is still 18 with `verdict PASS`. 9 unverified is the maximum: `verdicts_ok` needs ≥3 credited per
row (:378), so at least 9 seats must carry the right hash.
Smallest correction: `seats_ok += sum(1 for s in seats.values() if s['verdict'] is not None and
s['hash'] == hashes.get(row))`.

**D2 (high) — the citation floor is one citation and no relevance test.** :245 requires ≥300 bytes, :247
requires one `CITE[row]` file with `:<digits>`, and `verify_citation` (:235-241) only checks
`1 <= lineno <= len(lines)`; blank lines and `// SPDX-…` line 1 resolve. Evidence `B-padding-one-cite.json`
and `B2-irrelevant-citation.json` (both PASS; body text is `Read. ` + 300×`x` + one citation).
Smallest correction: require ≥2 distinct `CITE[row]` files cited, and reject a cited line that is blank or a
license/XML-declaration line. Safe against production: all 18 live reports in the wave now cite **4 of 4**
row-source files (bodies 6-13 KB, 18-57 citations; measured on the working tree, not a lane write).

**D3 (medium) — a contradiction outside the bound token is invisible.** `bind_seat` scans only
`ROW GR<n> VERDICT: …` (:306). Evidence: `C2-freetext-contradiction.json` PASS with bodies reading "This row
is false: the correction did not land … and it must not be admitted." Correction: add a negation lexicon on
the body (`is false`, `must not be admitted`, `did not land`, `contradicts the row`) returning `partly`.
Heuristic by nature; it closes the observed phrasing, not every phrasing.

**D4 (medium) — false positive: a true cross-row mention blocks a row.** :306-308 blocks when `r != row`
regardless of verdict, so a GR1 report that notes `ROW GR2 VERDICT: holds` makes GR1 `partly`
(`C3-cross-row-holds-mention.json`: `verdicts_ok 2`). Correction: `if r == row and w != m.group(2):` — only
the seat's own row can block. With that change C3 passes (validated) and C1 still fails (validated).

**D5 (medium) — `output` truthiness.** :280 `if not hits[0].get('output')` accepts `" "`
(`D2-space-output.json` PASS). The `output` text is never compared with the report file. Correction:
`if not str(hits[0].get('output') or '').strip():`, and ideally require `output` to start with the same
first line + `SECTION SHA256` as the report file.

**D6 (medium-high) — `corr_ok` is not bound to the row extents and cannot see denial.** :346 scans the whole
entry. Evidence `O-corrections-outside-rows.json`: PASS where GR1/GR2 keep base prose (defect sentences
deleted, no correction fact added; base carries none of the 7 required strings) with the seven sentences in
an appendix; its `section_sha256` differ from the frozen `3a2ba180…/d4296085…` (`1854ae98…/2ed86aad…`).
`O2-negated-corrections.json`: PASS with the appendix headed "The following corrections were NOT made".
Correction: evaluate `CORR_REQ` only inside the GR1-GR3 extents and reject a match whose preceding 80
characters contain `not|never|no longer|refused`; keep `CORR_FORBID` entry-wide (C8 is "gone from the
bytes"). Validated: honest entry `corr_ok 1`, O/O2 `corr_ok 0`.

**D7 (low-medium) — README mark negation guard is a four-phrase blacklist** (:88
`unadmitted|not admitted|never admitted|stay pending|stays pending`). `is **not** admitted round 49`
contains none of them: `M-negated-readme-mark.json` PASS with `marks 3/3`. Correction: exact positive line
(as already done for `MARK_ENTRY`/`MARK_SKILL`), or a negator test on the sentence.

**D8 (low) — distinctness is byte-level.** `distinct = len(bodies) == len(credited)` over a raw sha (:377).
`A2-trailing-space-distinct.json` credits all 6 GR1 seats with bodies differing only in trailing spaces
(`per_row.GR1.distinct_bodies true`, `verdicts_ok 1`). Correction: hash `' '.join(body.split())`.

**D9 (high, operability) — no dispatch override; the freeze revision cannot bind.** `dispatch_tasks` (:265)
always reads `.ufo/waves/round-49/w1-dispatch.json` from the revision; that path is absent at
`55c07cd` (`git show 55c07cd:.ufo/.../w1-dispatch.json` → "exists on disk, but not in"), first committed at
`32a85560` (`git log --all --oneline -- .ufo/waves/round-49/w1-dispatch.json`). Consequence:
`F0-mandated-rev-freeze.json` — perfect fixtures at `--revision 55c07cd` give `seats_ok 0`. The claim's
`--revision <REV>` must therefore name the integrated revision, and no seat can reproduce the cohort leg at
the freeze revision. Correction: add `--dispatch-file` (and echo the override paths in the JSON, see D10).

**D10 (low) — fixture runs are indistinguishable from measurements.** The output never echoes `entry_file`,
`wave_dir`, `results_file`; a fixture PASS at `32a85560` has exactly the same keys as a production PASS.
Correction: emit `"overrides": {"entry": …, "wave_dir": …, "results": …}` and keep the claim's receipt to
the no-override run.

**Control-battery drift (defect in `.ufo/waves/round-49/controls/battery.py`, not the counter).**
`FORBID[4]` is `which it is for a previous replace in state`, the counter's `CORR_FORBID[4]` is
`which it is for a replace in state`; the two do not match (F3 receipt:
`battery_string_matches_counter_pattern: false`), so control K2 never exercised that pattern. Correction:
import `CORR_REQ`/`CORR_FORBID` from the counter module (single authority).

## Validation of the correction set

`counter-patched.py` (scratch copy; `patch-proposal.diff`) applies D1-D7. `patched-summary.json`: 22
scenarios, PASS = `C0-honest-pass` (the honest control still passes) and `C3` (the false positive repaired);
**every one of the 9 cheats now fails**, and `C1` (bound-format negative) still blocks GR2. Not applied and
not validated: D9/D10 (`--dispatch-file`, override echo, battery import) — operational, no claim byte.

## Exact proposed text for the round report (claim C1)

> The C1 counter is forgeable: 9 fabricated cohort fixtures reach the full predicate
> (`verdicts_ok 3, seats_ok 18, marks_ok 3`, rc 0) without any seat reading a row — padding bodies with one
> irrelevant citation, bodies that call the row false, `output: " "`, 9 of 18 seats reporting
> `SECTION SHA256: 000…0`, the seven correction sentences parked in an appendix (even headed "NOT made")
> while GR1/GR2 keep base prose, and a README line reading `is **not** admitted round 49`. C1's PASS is
> therefore necessary but not sufficient: the round report must rest on the seat reports' content, and the
> counter needs the D1-D7 hardening (`patch-proposal.diff`) before it can be cited as the claim's
> measurement. Run the claim command at the integrated revision, never at the freeze: at
> `55c07cd` the dispatch file is absent and the counter binds 0 seats.

## Not done

- No run against the live integrated revision (it does not exist yet in this wave; the live `w1-results.json`
  is not final). Production state was only *read* to check the proposed citation rule (18/18 reports cite
  4/4 row-source files).
- No mutation of the frozen counter inside the lane; the patched copy lives only in the receipts.
- Tooling: none installed (python3 stdlib only); pacman untouched.
