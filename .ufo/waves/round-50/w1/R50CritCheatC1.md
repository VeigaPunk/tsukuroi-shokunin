VERDICT: defect-found

# R50CritCheatC1 — C1-B4: cheat the round-50 C1 admission counter

Seat: critic (L2, w1), item C1-B4, class EXEC-AUTHORIZED (the counter with fixture overrides only).
Counter under test: `tools/check-scrub-admission-r50.py` at REV `8029cdba1049df25632c91a23c8db4eefb54be5f`,
blob sha256 `0af0e679ee82d608d6278d2575391b1a7dd53af49099e962349bddac35f333db` (identical to
`.ufo/waves/round-50/w1/R50CritCheatC1/counter.py`, `sha256sum` observed).
All runs used the item's flag set: `--entry-file --skill-file --readme-file --wave-dir
--results-file --dispatch-file --revision 8029cdba1049df25632c91a23c8db4eefb54be5f --no-base-check`.
Driver: `.ufo/waves/round-50/w1/R50CritCheatC1/cheat.py` + `cheat2.py`; per-scenario JSON receipts in
`.ufo/waves/round-50/w1/R50CritCheatC1/receipts/`; fixture seat reports in `.../waves/<scenario>/`.
Python 3.14.8, no tool installs (nothing was installed; no pacman, no uv).

## 0. Control — the legs at REV, before any cheat

`python3 counter.py --lane <lane> --revision 8029cdba… --no-base-check`
→ `verdict FAIL`, `structural_ok 1`, `corr_ok 1`, `quotes_ok 3`, `verdicts_ok 0`, `seats_ok 0`,
`marks_ok 0`, `marks {entry:false, skill:false, readme:false}`, quotes `GR1 12/12, GR2 29/29, GR3 12/12`
(`receipts/control-rev.json`). So at the freeze the only unsatisfied legs are **marks (0/3), seats (0/18),
verdicts (0/3)**; corr and quotes already bind the frozen bytes. `--section-hash` at REV reproduces the
claimed row digests exactly (GR1 `3a2ba180…`, GR2 `a2e955ce…`, GR3 `43430a14…`).

Two facts that make the cheat cheap:
- the entry at REV still carries `## Gate status — round 50 (pending; the round-50 cohort has not settled)`
  (`corpus/knowledge/btrfs-scrub-grounding-r45.md:297`) and SKILL.md has no round-50 admission line, so the
  marks leg is **self-certifying**: whoever writes the mark text satisfies it, with no ordering evidence
  against the cohort;
- `w1-results.json` is absent at REV (`git ls-tree -r … -- .ufo/waves/round-50` lists `w1-dispatch.json`,
  `w1-spec.json`, `w1-validate.log` and no results file), so `seats_ok` is entirely a function of the
  file the wave writes afterwards.

## 1. Per-scenario results

| # | Scenario | Verdict | Failing leg | Declared mode? |
|---|---|---|---|---|
| S0 | 18 reports = one sentence + 300 B per-seat filler + 2 row citations | **PASS** | none — cheat succeeds | **no** |
| S0b | same, citations at line 1 of two row sources | **PASS** | none — cheat succeeds | **no** |
| Sa | 18 reports, one body modulo trailing spaces/blank lines | FAIL | `verdicts_ok 0`, `distinct_bodies false` on all 3 rows | yes |
| Sc | first line `holds`, body says the row fails and the quote does not appear | **PASS** | none — cheat succeeds | **no** (A2 is bound-format only) |
| Sc2 | same + one bound line `ROW GR1 VERDICT: fails` | FAIL | `verdicts_ok 2`; GR1 `credited 5`, `row_ok false` | yes |
| Sd | `results.json` lists the 18 seats with empty `output` | FAIL | `seats_ok 0`; notes `unbound (no completed output)` ×18 | yes |
| Se1 | one GR1 report cites `cmdline.c:147` + `entry.md:999999` | **PASS** | seat not credited (`fewer than 2 distinct row source files cited`); row still ok at 5 | partial |
| Se1b | `cmdline.c:147` + `vsprintf.c:86` + `entry.md:999999` | **PASS** | seat note `entry.md:999999 outside corpus/knowledge/btrfs-scrub-grounding-r45.md (308 lines)`; row still ok at 5 | partial |
| Se1c | same with in-range `entry.md:297` | PASS | none (credited 6) | yes |
| Se2 | `SHA256SUMS:1` + `cmdline.c:147` | **PASS** | seat not credited (`fewer than 2 distinct row source files cited`); row ok at 5 | yes (per seat) |
| Smin2 | 9 credited seats (2 reviewer + 1 critic per row) + 9 stub seats (all-zero hash, 109 B) | **PASS** | none — cheat succeeds | **no** |
| Smin3 | 12 credited + 6 stub | PASS | none | **no** |
| Sf2 | marked entry, four round-49 corrections kept, `dev-replace.c:1171-1199` reintroduced | FAIL | `corr_ok 0`, `corr_forbidden_present ["dev-replace\\.c:1171-1199"]`; every other leg 1/3/3/18 | yes |
| Sg | entry mark removed, skill+readme marks kept | FAIL | `marks_ok 2` | yes |

## 2. The three cheats that succeed (with the exact observed output)

### S0 — a machine-generated cohort satisfies the whole predicate
`receipts/S0-cheap.json`: `{"verdict":"PASS","structural_ok":1,"corr_ok":1,"quotes_ok":3,
"verdicts_ok":3,"seats_ok":18,"marks_ok":3}`, `rc=0`, `per_row` credited 6/6/6, `distinct true`.
Each of the 18 reports is 4 lines and 543 B, e.g. `waves/S0-cheap/R50RevGR1a.md`:

```
ROW GR1 VERDICT: holds
SECTION SHA256: 3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1
Row GR1 was read in full; nothing in it contradicts the row text.
padding-R50RevGR1a-zzzz…(300 z)
The two anchors are cmdline.c:147 and vsprintf.c:86.
```

Nothing in the body was read from GR1-GR3; the only row-specific content is two line numbers copied out of
the row's own `**Quote.**` lines. The citation floor is `body ≥ 300 bytes` (counter.py:294), `≥2 distinct
row-source basenames` (counter.py:299) and "every cited `file:line` resolves" (counter.py:292-306). It never
checks that a cited line supports the sentence, or that the sentence asserts anything. **S0b** shows the
same with `cmdline.c:1`/`vsprintf.c:1` (`receipts/S0b-line1-citations.json`, PASS, credited 6/6/6) — the
floor binds file existence and line range only, so even the anchor choice is free.

### Sc — prose contradiction is invisible; only the bound line blocks
`receipts/Sc-prose-contradiction.json`: PASS, credited 6/6/6, `distinct true`. Every credited body reads
"Row GR1 fails: the quoted text does not appear at cmdline.c:147 and the second anchor vsprintf.c:86 says
nothing of the kind." and is still credited `holds`. The blocking scan is
`ANY_VERDICT_RE = ROW (GR\d) VERDICT: (\w+)` (counter.py:101, used at counter.py:354-356), i.e. the
declared A2 scope ("bound-format negative"). `Sc2` proves the bound-format half does bind: one `ROW GR1
VERDICT: fails` line drops GR1 to `credited 5, row_ok false`, `verdicts_ok 2`, FAIL
(`receipts/Sc2-bound-negative.json`). So A2 behaves as declared but its docstring sentence — "a report
whose first line says partly/fails blocks the row whatever its citations" — reads as a guarantee about
report *content* that the code does not provide.

### Smin2 — 9 of 18 seats can be stubs; `seats_ok` counts bound, not credited, seats
`receipts/Smin2-9credited-9stub.json`: PASS with `seats_ok 18` while 9 seats carry
`hash 0000… != 3a2ba180…` notes. `seats_ok += sum(1 for s in seats.values() if s['verdict'] is not None)`
(counter.py:435) counts seats whose *first line parsed*, and `row_ok` needs only
`len(credited) >= 3` (counter.py:430). The cheapest PASS I could build is therefore **9 credited reports
(2 reviewers + 1 critic per row, each 543 B of template) + 9 three-line stubs of 109 B**, total 5 835 B of
report bytes for the 18 seats (`waves/Smin2-9credited-9stub/`). Every non-resolving citation, wrong section
hash, or 1-line report in the other 9 seats costs nothing but a `seat_notes` string.

## 3. Where the declared failure modes DO bind (no cheat found)

- whitespace padding does not buy distinctness: `norm_body` strips trailing whitespace and drops blank
  lines (counter.py:426-427) → Sa FAILs `distinct_bodies` on all rows. The leg constrains byte-identity
  only; S0 defeats it with *arbitrary* per-seat filler, which is all a script needs.
- empty `output` → `no completed output` (counter.py:328) → `seats_ok 0`, FAIL (Sd).
- `entry.md:999999` → `outside … (308 lines)` (counter.py:278-287) — the out-of-range leg is real, it just
  only costs the seat's credit, never the row (Se1b PASS at `credited 5`).
- `SHA256SUMS:1` + one row source → blocked by the ≥2-distinct-row-source leg (counter.py:299), i.e. a
  declared-lane-artifact citation does not count toward the row-source floor (Se2). Note the masking: in
  Se1 the out-of-range `entry.md:999999` never reaches `verify_citation` because the distinctness check
  fires first.
- the four round-49 corrections plus one reintroduced round-48 defect string → `corr_ok 0`, FAIL, all other
  legs clean (Sf2). This is the one leg a stub cohort cannot cheat: it reads the entry bytes.
- each mark leg is separable: entry mark absent → `marks_ok 2`, FAIL (Sg); all three present → 3 (S0).

## 4. Impacted axes

1. **cheat** — C1's admission standard is satisfiable by an artifact set that never read GR1-GR3: 3 mark
   lines + 9 template reports + 9 stubs, generated in one script. The claim text "a fresh 18-seat cohort
   re-reads GR1-GR3" is not what the counter measures; the counter measures *format conformance + citation
   resolution + distinctness*, which a generator meets.
2. **C1** — the four routed round-49 repairs do what they say (citation leg resolves, whitespace padding is
   not distinct, `--dispatch-file` override works, S240/inference/1128/range-gap text is bound by
   `corr_ok`), but the counter still cannot distinguish a reading cohort from a conforming one, so the
   predicate `seats_ok == 18 and verdicts_ok == 3` does not certify the depth it is cited for.
3. **depth** — the 18-seat leg is now the weakest link in the claim, weaker than `corr_ok` (which reads the
   bytes) and `quotes_ok` (which re-resolves 53 quotes against digest-pinned snapshots).

## 5. Smallest safe corrections

Ordered by value per line changed; each is local to the counter and does not touch the entry, the cohort
contract or any seat's format.

- **M1 (kills Smin2/Smin3/Se1/Se1b/Se2 in one line of predicate).** Close the tolerance: require every
  expected seat to be credited, not just 3 of 6. In `run()`, keep the per-row count but add
  `full_ok` = number of rows with `len(credited) == len(exp) and not blocking`, and add `full_ok == 3` to
  the predicate (counter.py:430-437 plus `PREDICATE` at counter.py:105-106). Effect: a wrong section hash,
  a non-resolving citation, or a stub body anywhere in the 18 fails the row. No legitimate report is
  affected — a real seat already cites resolving lines and the frozen hash. This is the correction I would
  ship: it converts "at least 3 read it" into "all 18 read it", which is what C1 asserts.
- **M2 (kills S0b, raises S0's cost).** Bind each credited body to the row's evidence: build
  `anchors[row] = {(file, line)}` from the `QUOTE_RE` matches already parsed in `quote_legs`
  (counter.py:240-271) and require `set(hits) & anchors[row]` non-empty in `report_citations_ok`
  (counter.py:292-306). A body then has to cite a line the row actually rests on, not line 1.
- **M3 (kills S0's template reuse, costliest).** Require the credited seats of a row to partition distinct
  anchors — no anchor cited by two credited bodies of the same row. GR2 has 29 anchors, GR1/GR3 have 12
  each, so 6 distinct anchors per row is feasible. This is the only structural way to force six separate
  evidence points per row; it still cannot prove comprehension, so it must be sold as "distinct evidence
  coverage", not as "read".
- **M4 (no code — honesty of the docstring).** The citation/size/distinctness legs cannot distinguish a
  reading cohort from a conforming generator, and A2 is bound-format only. Either add M1-M3 and say so, or
  narrow the counter docstring's claims: replace "a fresh counted cohort … reads GR1-GR3 `holds`" with
  "the 18 seats are format-conforming, hash-bound, citation-resolving and pairwise distinct"; and replace
  the A2 sentence "a report whose first line says partly/fails blocks the row whatever its citations" with
  "a report carrying a bound `ROW GRn VERDICT: partly|fails` line blocks the row; prose contradiction is
  not scanned". Do **not** add a prose regex for `fails` — it would false-positive on the real reports,
  which quote "FAILED" gate headings (`corpus/knowledge/btrfs-scrub-grounding-r45.md:241,273`).
- **M5 (marks leg, optional).** The three marks are self-certifying: my fixture wrote
  `## Gate status — round 50 (GR1-GR3 admitted)` into an entry whose cohort never read it and `marks_ok`
  was 3 (S0). If the mark is meant to record a *post-cohort* state, bind it to evidence the cohort
  produced (e.g. require `w1-results.json` to be committed at the same revision as the mark, or require the
  mark line to carry the three row digests). Otherwise say in the docstring that the mark is a
  declaration, not a receipt.

No correction is proposed for `corr_ok`, `quotes_ok` or `structural_ok`: Sf2 and the control show they
bind the frozen bytes, and Sa/Sd/Sc2/Sg show the declared failure modes fire.

## 6. What I did not do

- Did not run the real cohort or the production predicate against a committed `w1-results.json` (it does not
  exist at REV); every run used fixture overrides as the item specifies.
- Did not test `--section-hash` against a rewritten entry beyond Sf2's single mutation.
- Did not attempt a cheat against `quotes_ok` (it needs a real digest-pinned snapshot match) or against
  `corr_ok` (Sf2 shows the defect strings bind).
- Did not touch the lane index, the fleet repo, any sibling lane, or `/home/vgpnk/Projects/shokuknow`.
