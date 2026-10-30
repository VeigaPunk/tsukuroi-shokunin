VERDICT: defect-found

# R52CritForgeC1b — second C1 cheat angle, leg by leg (W-C1b)

Seat: `R52CritForgeC1b` (critic, non-counted). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
revision under test `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`. Counter under test:
`tools/check-scrub-admission-r52.py` at that revision, sha256
`bd5563af9b4a978552130e15d583614000e225fb7fb3f7c2e1c193dba7c08a80` — identical to
`.ufo/waves/round-52/frozen/FROZEN-hashes.txt` line 1 and to the lane working-tree bytes
(`sha256sum tools/check-scrub-admission-r52.py` → same digest; `git diff ff9470ea… -- tools/check-scrub-admission-r52.py`
→ empty). The counter is **frozen**: every hole below is a **reported limit, not a fix**.

## 0. Scope and method

I read the frozen counter's `bind_seat` / `report_citations_ok` / `verify_citation` / credit loop
(`tools/check-scrub-admission-r52.py:270-382` at the freeze) and then exercised each leg with
synthetic fixtures in scratch, under two paths:

* **override path** — the counter's own documented control-battery overrides (`--wave-dir`,
  `--results-file`, `--dispatch-file`, `--entry-file`, `--skill-file`, `--readme-file`);
* **production path** — a fixture git repo (`git clone --shared` of the lane at the freeze, a
  commit with the 18 seat reports, `w1-results.json`, `w1-dispatch.json` and the three admission
  marks), run as `python3 tools/check-scrub-admission-r52.py --revision <fixture-rev> --lane <fixture>`
  with **no overrides at all** — the same invocation the claim names.

Every fixture repo asserted `git rev-parse --show-toplevel` equals the fixture dir before its one
commit; all commits used `-c user.name=fixture -c user.email=fixture@invalid`. Scratch root:
`/fast/scratch/hyaku/tsukuroi-r52/R52CritForgeC1b/` (removed on exit). No lane tracked file was
edited, created or deleted; the only lane writes are this report and
`.ufo/waves/round-52/w1/R52CritForgeC1b/leg-fixture-receipts.json` (102 fixture receipts, each with
the counter's verbatim `verdict` / `rc` / six leg values / per-row credited-blocking-distinct /
seat_notes).

Fixture baselines that anchor every result below:

* `P1-production-honest-18` — 18 valid distinct reports, marks present, production path:
  `rc=0 verdict=PASS struct=1 lint=3 q=3 verd=3 seats=18 marks=3`, `section_sha256`
  `{GR1: 98fa4e07…, GR2: 9fd581a0…48b7c6e4…, GR3: 0405f38a…}`. The three hashes match the frozen
  record exactly (`--section-hash` at the freeze prints the same three).
* `P4-production-no-marks` — same cohort, marks not written: `verdict=FAIL … verd=3 seats=18 marks=0`.
  So the marks leg is real and independent.

---

## Leg (a) — can a report pass `bind_seat` with a verdict line inside a fenced block or after a preamble?

**No. The counter is sound here; the leg is closed.** `bind_seat` requires
`VERDICT_RE.fullmatch(lines[0])` (`tools/check-scrub-admission-r52.py:298`), i.e. the *literal first
line* of the file must be exactly `ROW GR<n> VERDICT: holds|partly|fails`, and
`HASH_RE.fullmatch(lines[1])` (`:299`) the literal second line. Nothing is read from anywhere else.

Observed, production path, one seat perturbed, the other 17 honest:

| fixture | perturbation on `R52RevGR1a` | counter's own detail |
|---|---|---|
| `Q5-verdict-inside-fence` | report wrapped in ```` ```markdown ```` … ```` ``` ```` | `first line '```markdown'` → seat **unbound** |
| `Q6-preamble-before-verdict` | `Report of seat R52RevGR1a on GR1.` prepended | `first line 'Report of seat R52RevGR1a on GR1.'` → **unbound** |
| `Q4-verdict-line-indented` | verdict line indented 4 spaces (markdown code block) | `first line '    ROW GR1 VERDICT: holds'` → **unbound** |
| `F1c-verdict-trailing-spaces` | `ROW GR1 VERDICT: holds␣␣␣` | unbound (`fullmatch`, not `match`) |
| `H6-crlf-line-endings` | whole report CRLF | `first line 'ROW GR1 VERDICT: holds\r'` → **unbound** |
| `P9-production-bom-first-line` | UTF-8 BOM before the verdict | `first line '﻿ROW GR1 VERDICT: holds'` → **unbound** |
| `H7-line1-names-other-row` | GR1 seat's line 1 says `ROW GR2 VERDICT: holds` | `first line 'ROW GR2 VERDICT: holds'` → **unbound** (row must match the seat's row) |

In every case the perturbed seat is *unbound*, `seats_ok` falls 18 → 17, and the overall verdict is
FAIL. **No fixture let a fenced or preamble-wrapped verdict credit.** The one seam worth naming is
that `fullmatch` is strict about invisible characters: CRLF (`:299`) and a BOM (`:298`) silently
unbind an otherwise perfect report. That is a **usability hazard for the counted cohort**, not a
cheat: an 18-seat cohort that writes its reports with CRLF endings on one seat, or with a trailing
space, loses that seat's credit and the claim fails for a formatting reason. This is the shape of
the round-49/50 failures and deserves a line in the seat instructions ("write LF, no BOM, no
trailing whitespace on lines 1–2").

## Leg (b) — does a contradicting `ROW GR<other> VERDICT:` line in a body block act as intended?

**Yes for the exact bound spelling, and it is over-broad in a way that will bite honest seats, but
it is not a cheat.** `bind_seat` scans `'\n'.join(lines[1:])` for `ANY_VERDICT_RE` =
`ROW (GR\d) VERDICT: (\w+)` (`:84`, `:304`); any hit whose row ≠ the seat's row, or whose word ≠
the seat's own verdict, returns the seat as `'partly'` — a **binding negative** (`:360`), which
blocks the whole row regardless of citations.

Observed, production path:

| fixture | body of `R52RevGR1a` | outcome |
|---|---|---|
| `R1-…quotes-GR2-verdict-line` | `… ROW GR2 VERDICT: holds was recorded earlier.` | GR1 seat → `partly`, `detail='contradicting line ROW GR2 VERDICT: holds'`, **GR1 row_ok=False**, `verdicts_ok=2` |
| `R2-…quotes-round50-partly` | `… the round-50 gate status records ROW GR1 VERDICT: partly.` | GR1 seat → `partly`, GR1 blocked, `verdicts_ok=2` |
| `T3-mention-other-row-holds` | same shape, other-row **holds** | blocked (a *positive* mention of another row also blocks) |
| `T5-mention-own-row-holds` | `ROW GR1 VERDICT: holds` in own body | **not** blocked — only *other-row* or *differing-word* lines trip it |
| `T6-prose-negative` | `In plain terms this row does not hold and I would have said partly.` | **not** blocked — free prose is invisible |
| `T7-mention-own-row-partly` | `ROW GR1 VERDICT: partly` (as a format example) | blocked |

Two properties of this leg that the L1 must know:

1. **It is spelling-exact.** The regex needs `ROW`, one space, `GR<digit>`, one space, `VERDICT:`,
   one space, then a word. `ROW GR1 VERDICT:partly` (no space after colon, `G5e`/`R3`),
   `row gr1 verdict: partly` (lowercase, `G5f`), `ROW  GR1 VERDICT: partly` (double space, `G5g`),
   `GR1 VERDICT: partly` (no `ROW` prefix, `G5h`), `ROW GR1\nVERDICT: partly` (line-split, `T1`)
   and `ROW\tGR1 VERDICT: partly` (tab, `T2`) all **PASS** with `verdicts_ok=3`. A negative that
   does not use the exact bound spelling is not detected — but it also does not need to be: the
   *first line* still has to say `holds` to credit, so this is a gap in the *negative detector*,
   not a way to smuggle a negative past a positive first line.
2. **It is over-broad for honest prose.** Any body sentence that mentions *any other row's* bound
   verdict line — even a **positive** `holds` mention, even a quoted round-50 history line, even a
   fenced code block showing the format — converts that seat into a binding negative and fails its
   row. `R1`/`T3` show a seat writing `ROW GR2 VERDICT: holds` in a GR1 report kills GR1. This is
   the single most likely way the honest round-52 cohort loses C1 by accident, and it is exactly
   the round-50 failure mode ("GR1 has one `partly`") reappearing in a new dress.

**Recommendation to the L1 (dispatch-level, not a counter change):** instruct the 18 counted seats
in the dispatch prompt that their body must not contain the literal substring `ROW GR` followed by
a digit — quote nothing in that shape, and refer to other rows as "GR2" or "the round-50 cohort"
instead. The counter is frozen; the prompt is the live surface.

## Leg (c) — does a `SECTION SHA256` mismatch slot reject cleanly?

**Yes — clean rejection, no false credit — with one asymmetry worth naming.**

`bind_seat` parses line 2 with `HASH_RE.fullmatch` (`:299`, `:85`) and the credit loop compares it
to the row's frozen section hash (`:362`). Observed, production path:

| fixture | perturbation | outcome |
|---|---|---|
| `R4-all-GR1-wrong-hash` | all six GR1 seats carry `SECTION SHA256: 8888…` | GR1 `credited=0`, **`blocking=[]`**, `row_ok=False`, `verdicts_ok=2`, verdict FAIL |
| `R5-one-GR1-garbage-hash-slot` | one GR1 seat carries `SECTION SHA256: not-a-hash` | `second line 'SECTION SHA256: not-a-hash'` → seat **unbound**, `seats_ok=17`, FAIL |
| `H14-hash-slot-trailing-space` | one GR3 seat's hash line has a trailing space | unbound (`fullmatch`), `seats_ok=17`, FAIL |
| `H6` / `P9` / `F1c` | CRLF / BOM / trailing space on line 1 or 2 | unbound, `seats_ok=17` |

A wrong hash does not credit and does not block — it simply drops that seat out of `credited`
(`:363-364`). A *malformed* hash slot unbinds the seat entirely. Both are clean; neither can
manufacture a credit.

**The asymmetry that matters:** a wrong hash is not a *binding negative* (it does not land in
`blocking`), so a row whose other five seats are fine still passes on the remaining credits — see
`F3b-wrong-hash-one-seat-GR1`: `verdicts_ok=2`, GR1 `credited=5`, `row_ok=True`, GR1 still
`row_ok`. That is correct behaviour (the hash is a binding, not a verdict), but it means a
hash-mismatched seat disappears *silently* rather than loudly. It is visible in the receipt only
in `seat_notes` (`R52RevGR2a: hash … != …`), not in `per_row[...]['blocking']`.

## Leg (d) — can 18 IDENTICAL bodies still credit (the distinct-bodies rule)?

**No — the rule bites. But the *scope* of the rule is narrower than the claim text, and that is
where the real finding is.**

The rule (`:370-375`): the body of each credited seat is whitespace-normalised
(`' '.join(body.split())`) and hashed; a row's `distinct` flag is `len(bodies) == len(credited)`,
and `row_ok` requires `distinct`. Observed, production path:

| fixture | bodies | outcome |
|---|---|---|
| `R6-18-identical-bodies` | all 18 byte-identical | every row `credited=6`, **`distinct_bodies=False`**, all three `row_ok=False`, `verdicts_ok=0`, FAIL |
| `Q1-18-truly-identical-bodies` | same | `verdicts_ok=0`, FAIL |
| `H2-GR1-whitespace-only-differences` | GR1 bodies differ only in whitespace | GR1 `distinct_bodies=False` → GR1 `row_ok=False` (normalisation is deliberate) |
| `H3-GR1-one-char-differences` | GR1 bodies differ by **one trailing character** | GR1 `distinct=True` → GR1 `row_ok=True` |
| `S3b-one-char-diff-all-18-credited` | one char on each of the 18 | `verdicts_ok=1`, FAIL only because GR2/GR3 bodies were identical to each other |
| `G4-bodies-reused-across-rows` | one body per row shared by all six seats of that row | all three rows `distinct=False`, `verdicts_ok=0`, FAIL |

So identical bodies do **not** credit. The rule is a *byte-distinctness* rule, not a
*semantic-independence* rule: one character of difference is enough (`H3`), and whitespace is
normalised away (`H2`).

### The finding that matters: `distinct` is computed **per row**, over **credited** seats only

`bodies` is a per-row `set()` reset on every row iteration (`:353`), and only *credited* seats
contribute to it (`:370-371`). Cross-row reuse is therefore invisible to the rule, and a seat that
fails to credit contributes nothing. Combining that with the `>= 3` credited threshold
(`:374`) gives the minimum real cohort:

**`R7-minimal-9-substantive-plus-9-stubs` and `R8-three-distinct-texts-for-the-whole-cohort`
both PASS** (`rc=0 verdict=PASS struct=1 lint=3 q=3 verd=3 seats=18 marks=3`), with:

* only **three** substantive report texts in the entire 18-seat cohort — the *same* three texts
  credited once in GR1, once in GR2, once in GR3 (`R8`, `Q7`: each row `credited=3`,
  `distinct=True`);
* the other nine seats carrying either a three-line stub (`R52RevGR1b` … `SECTION SHA256: <hex>`
  and nothing else — `S2`) or a well-formed report with a **wrong** hash (`R7`, `S1`, `P3`).

`seats_ok` still reads 18 because `seats_ok += sum(1 for s in seats.values() if s['verdict'] is not
None)` (`:379`) counts a seat as present when `bind_seat` *bound* it — a bound seat with a wrong
hash or a stub body still has `verdict='holds'` and counts, while contributing nothing to
`credited`. The counter's own docstring says `seats_ok` is "each of the 18 expected seats is
exactly one completed entry of `w1-results.json`", and that is literally what it measures; but the
*predicate* `seats_ok == 18 and verdicts_ok == 3` therefore admits a cohort in which **only three
distinct readings exist, one per row**.

### Is that a cheat, or a limitation to disclose?

The honest reading is that this is the **same named limit the round already carries**, one level
up: the counter proves *format and binding*, not *independent judgement*. The FROZEN record's
named-limits section already discloses "a liar that reasons semantically about arbitrary edits of
itself" and "a clause the pre-read and the cohort both misjudge". What is new and worth the L1's
attention is the **pre-data control gap**: the round-52 battery has 26 C1 controls
(`.ufo/waves/round-52/controls/battery.py:112-193`, receipt
`.ufo/waves/round-52/controls/battery-summary-r52-freeze-c1.jsonl`, all 26 `as_expected: True`), and
**none of them exercises this shape**:

* `K5 whitespace-padded identical bodies` (`battery.py:179-180`) uses the *same* body for two
  GR2 seats — it pins the whitespace-normalisation half of the rule, but **not** the
  one-character-difference escape (`H3`) nor the per-row scoping (`R8`).
* `K6 GR1 reviewers only` (`battery.py:182`) pins the role mix, but **not** the `>= 3` credited
  threshold.
* `K7 reports but no results entries` (`battery.py:183`) pins the results binding, but **not** the
  fact that a *bound-but-uncited* seat still counts toward `seats_ok == 18`.
* `K-pass` (`battery.py:192`) uses 18 valid distinct reports — the honest shape — so nothing in the
  battery demonstrates that a **9-substantive + 9-stub** cohort would PASS.

That is a **control-coverage gap in the frozen battery**, not a counter defect: the counter's
behaviour is deterministic and consistent with its own docstring, but the battery never pins the
boundary between "18 distinct readings" (K-pass) and "3 distinct readings + 15 stubs" (`R8`),
which is the boundary a future reader of the receipt would want pinned.

## Two additional cheats I found while closing the legs (not in the item's four legs, both cheap to confirm)

**(i) The `--` override surface has no `--control` gate, unlike C3.**
`check-adjacency-table-r51.py:317-319` refuses to run with any input override unless `--control`
is passed, printing `'an input override is a control, never a measurement'`;
`check-scrub-admission-r52.py:395-405` accepts `--entry-file --skill-file --readme-file
--sources-file --wave-dir --results-file --dispatch-file --lane --no-base-check` with **no** such
gate and no "mode" field in its output. Every PASS receipt I produced in this seat came from the
override path; the JSON it emits is indistinguishable from a production receipt (my `P1` production
PASS and `R8` override PASS have identical `verdict`/`legs` shape). A C1 receipt built on
overrides — including the battery's own `K-pass` — can be presented as a measurement. C3 already
solved this; C1 did not inherit the guard. **This is the highest-value transferable fix**, but the
counter is frozen this round, so it is a report, not a change.

**(ii) Report citations resolve against *any* pinned snapshot with that basename, not the row's own.**
`verify_citation` (`:221-239`) builds `cands = [lines for (sid, sf), lines in cache.items() if sf ==
fname]` — basename only, no `sid` — and accepts the line if it is in range for *any* candidate.
`scrub.c` exists as S237 (`.ufo/waves/round-42/frozen/src/scrub.c`, 2231 lines) and S242
(`.ufo/waves/round-44/frozen/src/scrub.c`, 3337 lines), and GR3's own prose source for `scrub.c` is
S237 while GR2's is S242. A GR3 report citing `scrub.c:3300` therefore **resolves** even though line
3300 does not exist in GR3's declared S237 snapshot — confirmed in `G7-GR3-cites-scrub.c-in-S242-only`
and `H15-GR3-cites-scrub.c-in-the-other-snapshot`: both `verdict=PASS verd=3`, GR3 `credited=6`.
The row-source *pair* requirement is also per-row and loose: `G8-GR1-cites-GR2-sources` shows GR1
citing only `ioctl.c` + `dev-replace.c` (GR2's sources) → GR1 `credited=0` (the `>= 2 distinct
row source files` check at `:249` uses the row's own `CITE` set, so this one *is* enforced), while
`G10-citations-outside-declared-ranges` shows a citation to `cmdline.c:280` (outside GR1's declared
ranges) still credits — the *report* citation leg has no range check, only the *entry* lint does.

By contrast the citation leg correctly **ignores** a basename that is neither a row source nor a
declared lane artifact (`verify_citation`'s last branch, `:239`) rather than disqualifying it
(`P7-production-mixed-citation` PASSes with `randomfile.txt:3` in the body), and correctly
disqualifies a row-source citation to a line that exists in no snapshot
(`F5b-citation-line-outside-snapshot` → `cmdline.c:999999 outside all pinned snapshots`).

---

## Summary table — every leg, with the counter's own numbers

| leg | fixture (production path) | verdict | verdicts_ok | seats_ok | what it proves |
|---|---|---|---|---|---|
| (a) | `P1-production-honest-18` | PASS | 3 | 18 | baseline |
| (a) | `Q5-verdict-inside-fence` | FAIL | 3 | 17 | fenced verdict unbound |
| (a) | `Q6-preamble-before-verdict` | FAIL | 3 | 17 | preamble unbound |
| (a) | `Q4-verdict-line-indented` | FAIL | 3 | 17 | indented verdict unbound |
| (a) | `H6-crlf-line-endings` | FAIL | 0 | 0 | CRLF unbound (all 18) |
| (a) | `P9-production-bom-first-line` | FAIL | 3 | 17 | BOM unbound |
| (b) | `R1-…quotes-GR2-verdict-line` | FAIL | 2 | 18 | other-row mention → binding negative |
| (b) | `T5-mention-own-row-holds` | PASS | 3 | 18 | own-row mention is not a negative |
| (b) | `T6-prose-negative` | PASS | 3 | 18 | free prose negative invisible |
| (b) | `G5e/G5f/G5g/G5h`, `T1`, `T2` | PASS | 3 | 18 | non-bound spellings not detected |
| (c) | `R4-all-GR1-wrong-hash` | FAIL | 2 | 18 | wrong hash → not credited, not blocking |
| (c) | `R5-one-GR1-garbage-hash-slot` | FAIL | 3 | 17 | malformed hash slot → unbound |
| (d) | `R6-18-identical-bodies` | FAIL | 0 | 18 | identical bodies blocked |
| (d) | `H3-GR1-one-char-differences` | FAIL | 1 | 18 | one character defeats distinctness |
| (d) | `R8-three-distinct-texts-for-the-whole-cohort` | **PASS** | 3 | 18 | **3 texts + 9 stubs PASS** |
| (d) | `R7-minimal-9-substantive-plus-9-stubs` | **PASS** | 3 | 18 | **9 substantive + 9 stubs PASS** |
| extra | `P4-production-no-marks` | FAIL | 3 | 18 | marks leg independent |
| extra | `S4-results-duplicate-top-level-key` | FAIL | 0 | 0 | duplicate JSON key → whole file unusable (`no_dups`) |
| extra | `S5-dispatch-wrong-shape` | FAIL | 0 | 0 | wrong dispatch shape → no seats bound |

## Impacted axes

* **C1 / depth** — the four legs are *closed against the cheat* in the direction that matters:
  no fixture let a fenced, preamble-wrapped, indented, BOM'd, CRLF'd, or wrong-row verdict credit,
  and no fixture let 18 identical bodies credit. The residual risk to the round's own claim is
  **two operational hazards, both dispatch-level**: (i) the over-broad bound-format negative
  detector will fire on any honest body that quotes another row's verdict line — the L1 should
  forbid the literal substring `ROW GR<digit>` in seat bodies; (ii) CRLF/BOM/trailing-space line
  endings silently unbind a seat.
* **C1 / cheat** — the counter cannot be tricked into a false `holds` on the bytes; what it *can*
  do is PASS a cohort of 9 substantive + 9 stub (or 3 text + 9 stub) reports, because `seats_ok`
  counts bound seats and `distinct` is per-row over credited seats only. The frozen battery's 26
  C1 controls pin none of that boundary.
* **C1 / instrument** — the C1 counter lacks C3's `--control` gate on its input overrides, so a
  C1 receipt built on overrides is indistinguishable from a production receipt. Worth carrying into
  the next round's counter (round 53), not fixable in the frozen round-52 bytes.

## Smallest safe correction

The counter is frozen, so nothing here is a fix to `check-scrub-admission-r52.py`. The smallest
safe corrections are all **outside** the frozen bytes:

1. **Dispatch-level (L1, now, before the counted cohort runs):** add to the 18 seat prompts —
   *"write the report with LF line endings, no BOM, no trailing whitespace on lines 1–2; line 1
   exactly `ROW GR<n> VERDICT: holds`; line 2 exactly `SECTION SHA256: <64 hex>`; and your body
   must not contain the literal string `ROW GR` followed by a digit — refer to other rows as
   `GR2` or `the round-50 cohort`."* This closes both hazards (a) and (b) at zero cost to the
   frozen counter. It also lets the L1 state in the wave record that the *bound-format negative
   detector is over-broad by design*, so a future reader of a FAIL receipt does not misread it as
   a substantive negative.
2. **Battery-level (L1, next round's control set):** add two controls to the C1 battery —
   a *K12* that runs the counter on **9 substantive + 9 stub** reports and records the observed
   PASS, and a *K13* that runs it on **3 texts reused across all three rows + 9 stubs** — so the
   boundary between K-pass (18 distinct) and the minimum is pinned by a receipt rather than left
   implicit. This is the control-coverage gap named above; it is the honest way to disclose the
   limit without touching frozen bytes.
3. **Next round's counter (round 53, out of scope here):** port C3's `--control` gate
   (`check-adjacency-table-r51.py:317-319`) into the C1 counter so an override-run is labelled a
   control, and narrow `verify_citation` (`:222`) to resolve a citation against the row's own
   snapshot id rather than any snapshot sharing the basename.

## What I did NOT do (stated, not implied)

* I did not modify `tools/check-scrub-admission-r52.py` or any other lane file; the counter is
  frozen and every finding above is a reported limit.
* I did not write the three round-52 admission marks, the dispatch, or the results file — the L1
  alone does that, and only after three clean counted rows.
* I did not run the C2 scorer or the C3 adjacency counter; this seat's item is C1-only. I did read
  `check-adjacency-table-r51.py` (read-only) for the `--control` comparison in finding (i).
* I did not measure the live integrated revision: `.ufo/waves/round-52/w1-dispatch.json` and
  `.ufo/waves/round-52/w1-results.json` are **ABSENT** at the freeze revision (verified with
  `git cat-file -e ff9470ea…:<path>` for both), so no counted cohort exists yet and no C1
  measurement is possible at this revision. Every PASS/FAIL above is a **synthetic control**, not
  a measurement.
* I did not use `--selftest`-bearing commands; each counter invocation is a single C1 run, ~0.1–1 s.
* Tooling: no package was installed or upgraded this seat; nothing to record under the operator's
  tooling directive. (I briefly wrote two files under `/tmp` while diffing the round-51 and
  round-52 counters; both were removed immediately, and no other `/tmp` write occurred.)

## Reproduction

```
S=/fast/scratch/hyaku/tsukuroi-r52/R52CritForgeC1b        # scratch, removed on exit
git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin $S/lane
git -C $S/lane checkout -q --detach ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0
sha256sum $S/lane/tools/check-scrub-admission-r52.py      # bd5563af… == FROZEN-hashes.txt
python3 $S/legs.py && python3 $S/legs2.py && python3 $S/legs3.py \
  && python3 $S/legs4.py && python3 $S/legs5.py && python3 $S/legs6.py \
  && python3 $S/legs7.py && python3 $S/legs8.py && python3 $S/legs9.py
```

Per-fixture verdicts, leg values, per-row credited/blocking/distinct and seat_notes for all 102
fixtures are in `.ufo/waves/round-52/w1/R52CritForgeC1b/leg-fixture-receipts.json`.

## Exact proposed text for the L1's wave record (advisory, not a counter change)

> **C1 counter limits (measured by `R52CritForgeC1b`, round 52, wave w1).** The frozen
> `tools/check-scrub-admission-r52.py` rejects, cleanly and without false credit: a verdict line
> inside a fenced block, after a preamble, indented, BOM-prefixed or CRLF-terminated; a
> `SECTION SHA256` that is malformed or mismatched; and 18 identical report bodies. Its bound-format
> negative detector (`ANY_VERDICT_RE`) fires on **any** body occurrence of `ROW GR<digit> VERDICT:
> <word>` for a row other than the seat's own — including a *positive* `holds` mention — and
> ignores the same content in any non-bound spelling or in free prose. Its `seats_ok == 18` counts
> seats that *bound*, not seats that were credited, and its `distinct` rule is per-row over
> credited seats only, so a cohort of **9 substantive reports plus 9 stubs** (or **3 report texts
> reused across the three rows plus 9 stubs**) satisfies the whole predicate: observed PASS,
> `verdicts_ok=3 seats_ok=18 marks=3`. Unlike the C3 counter, the C1 counter has no `--control`
> gate on its input overrides, so an override-built receipt is indistinguishable from a production
> receipt. The round-52 C1 battery (26 controls) pins none of these boundaries. The counted seats
> are instructed to write LF/no-BOM/no-trailing-whitespace reports and to avoid the literal
> `ROW GR<digit>` substring in their bodies.

**Report path:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-52/w1/R52CritForgeC1b.md`
**Receipts:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-52/w1/R52CritForgeC1b/leg-fixture-receipts.json`
