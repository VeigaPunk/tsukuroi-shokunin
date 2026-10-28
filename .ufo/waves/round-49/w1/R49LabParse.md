VERDICT: defect-found

# C1-B8 — report-parse edge probe of the frozen C1 counter

Bytes under test: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show
55c07cd3f8bff2e12117c34d57b4c618de74d85c:tools/check-scrub-admission-r49.py`, extracted to
`/fast/scratch/hyaku/tsukuroi-r49/R49LabParse/check-scrub-admission-r49.py`;
`sha256sum` of both = `3dd52ef376e233192f955208c1132f6b0d23bbebe97dd1df75e6296f55d970a4` (git blob
`240bef1e28f2…`, and the same blob at `32a85560`: `git rev-parse` equality, verified). Line numbers
below are that file.

Baseline (the control that makes every later delta attributable): the frozen counter's own K-pass
shape (`controls/battery.py:120-229`) — freeze entry/SKILL/README plus the three marks supplied
through `--entry-file/--skill-file/--readme-file`, 18 synthetic seat reports in a `--wave-dir`,
synthetic `w1-results.json` through `--results-file`, `--revision
32a855608aa3ebb19b0602a94cc33bcfda564a61` — the dispatch commit the frozen C1 controls themselves
used (`controls/battery-summary-r49-c1.jsonl`, every line `"revision": "32a85560…"`; the dispatch
file does not exist at `55c07cd3`, `git ls-tree` shows only `before/` and `frozen/` under
`.ufo/waves/round-49` there, and `dispatch_tasks()` has no fixture override) — plus
`--no-base-check`. Baseline observed: `PASS`, `structural_ok 1 corr_ok 1 quotes_ok 3 verdicts_ok 3
seats_ok 18 marks_ok 3` (receipts: `R49LabParse/summary.json` → `baseline`).

Isolation: every case directory holds exactly 18 report files and differs from the baseline
directory in exactly one report (`R49RevGR1a.md`, row GR1) — `R49LabParse/isolation.txt`. The two
quorum probes E6/E7 differ in 3 and 4 reports by design and are labelled as such.

Command shape for every receipt (one per case, full JSON in `R49LabParse/probe-out.json`):

```
python3 <extracted counter> --revision 32a85560… --lane <lane> --no-base-check \
  --entry-file r38/entry.md --skill-file r38/skill.md --readme-file r38/readme.md \
  --wave-dir r38/wave-<case> --results-file r38/results.json
```

## Result table (item cases a–i, then extras)

| case | bytes of `R49RevGR1a.md` | verdict | rc | legs `[structural, corr, quotes, verdicts, seats, marks]` | leg that fails | mode | declared? |
|---|---|---|---|---|---|---|---|
| a-crlf | all LF→CRLF | FAIL | 1 | `[1,1,3,3,17,3]` | `seats_ok` | unbound | yes |
| b-bom | `EF BB BF` before `ROW` | FAIL | 1 | `[1,1,3,3,17,3]` | `seats_ok` | unbound | yes |
| c-lead-space | one leading space | FAIL | 1 | `[1,1,3,3,17,3]` | `seats_ok` | unbound | yes |
| d-fence | ```` ``` ```` lines around the two | FAIL | 1 | `[1,1,3,3,17,3]` | `seats_ok` | unbound | yes |
| e-capital | `VERDICT: Holds` | FAIL | 1 | `[1,1,3,3,17,3]` | `seats_ok` | unbound | yes |
| f-third-line | line 3 `ROW GR2 VERDICT: fails` | FAIL | 1 | `[1,1,3,2,18,3]` | `verdicts_ok` | blocking negative | yes, but broader (F3) |
| g-second-hash | line 3 `SECTION SHA256: <GR2 hash>` | **PASS** | 0 | `[1,1,3,3,18,3]` | none | none | **no — F2** |
| h-body-299 | 299-byte body, ends LF | **PASS** | 0 | `[1,1,3,3,18,3]` | none | none | **no — F1** |
| i-body-300-bad-cite | 300-byte body, only `cmdline.c:999999` | **PASS** | 0 | `[1,1,3,3,18,3]` | none (seat not credited) | de-credited, absorbed | "earns nothing", but no leg moves (F4) |

Extras (same method, beyond the item's list, each labelled):

| case | verdict | rc | legs | note |
|---|---|---|---|---|
| E1-trailing-space (`holds `) | FAIL | 1 | `[…,17,3]` | unbound, `first line 'ROW GR1 VERDICT: holds '` |
| E2-uppercase-hash | FAIL | 1 | `[…,17,3]` | unbound; `HASH_RE` accepts `[0-9a-f]` only (`:91`) |
| E3-body-300-ok-cite | PASS | 0 | `[1,1,3,3,18,3]` | seat credited; 300-byte floor is inclusive upward |
| E4-body-298 + LF | PASS | 0 | `[…,18,3]` | seat **not** credited, `seat_notes: 'report body under 300 bytes'` — joined body 299 |
| E5-body-299, no final LF | PASS | 0 | `[…,18,3]` | seat **not** credited, same note — joined body 299 |
| E6-badcite-3 | PASS | 0 | `[1,1,3,3,18,3]` | credited exactly `[R49RevGR1c, R49CritGR1b, R49CritGR1c]` |
| E7-badcite-4 | FAIL | 1 | `[1,1,3,2,18,3]` | credited 2 → `row_ok` false |
| E8-nonenum-word (`ROW GR1 VERDICT: held` in prose) | FAIL | 1 | `[…,2,18,3]` | blocking, `contradicting line ROW GR1 VERDICT: held` |

Wording of the per-seat evidence (verbatim from `probe-out.json`, `per_row.GR1.seats.R49RevGR1a`
unless stated):
(a) `{"verdict": null, "detail": "first line 'ROW GR1 VERDICT: holds\\r'"}` · (b)
`first line '\\ufeffROW GR1 VERDICT: holds'` · (c) `first line ' ROW GR1 VERDICT: holds'` · (d)
`first line '```'` · (e) `first line 'ROW GR1 VERDICT: Holds'` · (f)
`{"verdict": "partly", "detail": "contradicting line ROW GR2 VERDICT: fails"}`, `GR1.blocking =
["R49RevGR1a"]`, `row_ok false` · (g) `{"verdict": "holds", "detail": "R49RevGR1a.md"}` and
`GR1.credited` contains all six seats · (h) same as (g) with `seat_notes: []`.

## F1 — defect: the "body >= 300 bytes" floor is 299 authored bytes (case h)

Contract says `body >= 300 bytes` twice: counter docstring `:31-32` and `frozen/FROZEN.md:35`. The
check is `len(body.encode('utf-8')) < 300` (`:245`) on `body = '\n'.join(lines[2:])` (`:308`,`:309`)
where `lines = text.split('\n')` (`:297`). A report file that ends with LF yields a trailing empty
element, so the joined body always ends with one byte the author did not write as body.

Measured (`R49LabParse/isolation.txt`, byte arithmetic section):

| case | body line | file ends LF | joined body | credited? |
|---|---|---|---|---|
| h-body-299 | 299 B | yes | **300 B** | **yes (defect)** |
| E4-body-298 | 298 B | yes | 299 B | no (`under 300 bytes`) |
| E5-body-299-nonl | 299 B | no | 299 B | no (`under 300 bytes`) |
| E3-body-300-ok-cite | 300 B | yes | 301 B | yes |

So the real floor is "299 authored bytes if the report ends with a newline" — one byte looser than
declared, and the item's case (h) expectation is falsified: the counter credits a body the contract
says must fail. Impact is bounded (1 byte) but it is a declared-boundary inversion and it is exactly
the kind of off-by-one that later rounds inherit.

Proposed fix (next round's counter; nothing may change in the frozen bytes now):

```python
    lines = text.split('\n')
    ...
    body = '\n'.join(lines[2:])
    if text.endswith('\n') and body.endswith('\n'):
        body = body[:-1]          # the file's final LF is a terminator, not body
```

and return that same `body` at `:308` and `:309`.

## F2 — defect: a second `SECTION SHA256` line is silently ignored (case g)

`HASH_RE` is applied only to `lines[1]` (`:301`). A report whose line 3 is
`SECTION SHA256: d4296085…` (GR2's real hash, contradicting the GR1 hash on line 2) passes with all
legs at target, the seat credited, and no diagnostic (`seat_notes: []`). Fixture head in
`R49LabParse/fixtures/g-second-hash/R49RevGR1a.md`:

```
ROW GR1 VERDICT: holds
SECTION SHA256: 3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1
SECTION SHA256: d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f
```

The binding is still on line 2, so severity is low — but the counter is what "proves the correction
landed", and a report carrying a foreign/stale hash is accepted without a word.

Proposed fix:

```python
    if sum(1 for ln in lines if HASH_RE.fullmatch(ln)) != 1:
        return None, None, None, 'SECTION SHA256 lines != 1'
```

## F3 — the blocking trigger is broader than "a report whose first line says partly/fails" (case f)

Counter docstring `:17-19` and `FROZEN.md:36-37` describe the blocking negative as a *first-line*
property ("a report whose first line says partly/fails blocks the row whatever its citations").
Measured reality (`:306-308`): every `ROW (GR\d) VERDICT: (\w+)` occurrence in `lines[1:]` is
compared, so

* a **different row's** verdict on line 3 (`ROW GR2 VERDICT: fails`) converts this seat to `partly`
  and blocks its own row GR1 (case f: `blocking = ["R49RevGR1a"]`);
* a **word outside the enum** anywhere in prose does the same (E8: `ROW GR1 VERDICT: held` →
  `blocking`, `verdicts_ok 2`);
* there is no fenced-block or quoting exemption.

Consequence for report authors: a seat that quotes a peer's opposing verdict line (a normal thing to
do when refuting or citing an earlier negative) vetoes its own row, and a typo'd mention does
likewise. This is a real hazard, not a hypothetical: the trigger vocabulary is `\w+`, not
`holds|partly|fails`.

Not a code defect against the docstring's *behaviour* sentence ("NO bound-format negative
anywhere"), but the two contract sentences disagree with each other and the stricter reading is the
one implemented. Either the prose must say "any line", or the check must be restricted to the
verdict-shaped line or to unfenced lines.

## F4 — measured boundary: a citation failure moves no leg, and `seats_ok == 18` is not 18 credited readings (cases i, E6, E7)

Case (i): 300-byte body whose only `file:line` token is `cmdline.c:999999` → `verify_citation` fails
(`:241`), `report_citations_ok` returns `'cmdline.c:999999 outside all pinned snapshots'`, the seat
is *not* added to `credited` (`:374`) — but it *is* bound, so `seats_ok` counts it (`:383`) and the
predicate still returns **PASS, rc 0**. The de-credit is visible only in `seat_notes`; the seat's own
`per_row.seats` entry still reads `{"verdict": "holds", "detail": "R49RevGR1a.md"}`.

Quorum slack measured exactly:

| non-crediting seats in GR1 | credited | `verdicts_ok` | predicate |
|---|---|---|---|
| 1 (case i) | 5 | 3 | PASS |
| 3 (E6: RevGR1a, RevGR1b, CritGR1a) | 3 | 3 | PASS |
| 4 (E7: + CritGR1b) | 2 | 2 | FAIL |

So the frozen predicate admits up to **3 non-crediting seats per row — 9 of the 18 across the wave —
while still returning PASS**, provided at least one reviewer and one critic remain credited
(`:378`). `seats_ok == 18` therefore means "18 shape-bound reports whose line-2 hash matches", not
"18 seats that resolved a citation". `FROZEN.md:37` already says such a report "earns nothing", so
this is declared *behaviour*; what it is not is a stated boundary, and it is the one place where the
claim's prose ("a fresh 18-seat cohort re-reads the corrected rows") can be over-read. The L1 should
record `len(credited)` per row from `per_row` in the measurement narrative rather than restating
`seats_ok 18` as 18 resolving readings. The frozen predicate must not be edited post-freeze; this is
a measurement-narrative and next-round-counter item.

Secondary observability point: because the seat stays in `per_row.seats` with `verdict: holds`, a
reader of `per_row` alone cannot tell a credited seat from a de-credited one. Adding the rejection
to `seats[seat]` (or a `credited: false` flag there) would make the receipt self-explaining.

## Answer to the item's two-way question, case by case

* **unbound (shape/parse failure)** — (a) CRLF, (b) BOM, (c) leading space, (d) fence, (e)
  capitalised, E1 trailing space, E2 uppercase hash. The seat earns no verdict (`verdict: null`), so
  the leg that fails is `seats_ok` (17, `:383`); `blocking` stays empty and `verdicts_ok` stays 3
  because the row still has five credited seats. Predicate FAIL. Declared mode: yes — "A report
  binds only as a FILE … line 1 … line 2" (`FROZEN.md:33-35`).
* **blocking negative** — (f). `seats_ok` 18, `verdicts_ok` 2, `blocking` non-empty. Declared mode:
  yes for the effect, broader than the documented trigger (F3).
* **neither** — (g), (h), (i): no leg fails. (g) and (h) are defects (F2, F1); (i) is absorbed by
  quorum slack and passes the predicate (F4).

## Not done / limits

* No selftest was run (this counter has none) and no live integrated revision was measured — that is
  the L1's measurement, not this seat's.
* Only the `--wave-dir` path was exercised (as the item specifies); the committed-bytes path
  (`show(lane, rev, …)`) shares the same `bind_seat` code and was not separately probed.
* GR2/GR3 seat names were not mutated: `bind_seat` is row-agnostic apart from `CITE[row]` on the
  citation leg, and the 17 unmutated reports included all of GR2/GR3.
* No tracked lane file was created, edited or deleted — only this report and its receipts
  (`R49LabParse.md`, `R49LabParse/`). No git/jj mutation was run anywhere. Tooling: none installed
  or upgraded this seat.

## Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-49/w1/R49LabParse/`
— `probe.py` (driver; rerun with `python3 probe.py`, it recreates its own fixtures and baseline,
~1.5 s, no selftest),
`probe-out.json` (full counter JSON per case, 94 KB), `summary.json` (per-case legs / credited /
blocking / seat_notes), `isolation.txt` (18-file counts, one-file diff proof, byte arithmetic,
case-g head), `fixtures/<case>/` (the exact mutated report bytes for all 17 cases).
Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49LabParse/` removed after the receipts were copied.
