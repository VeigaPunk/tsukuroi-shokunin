# CriticClaims — round 96 w1 — falsification of the two frozen sentences

Seat: `CriticClaims`. Scope: `.ufo/waves/round-96/claims.json` C1/C2 only. No frozen byte was edited;
every number below was produced by a command I ran from this seat, and every receipt is under
`.ufo/waves/round-96/w1/CriticClaims/receipts/`.

## 0. What was measured against what

| item | value at measurement |
|---|---|
| lane tip (moved during the seat: `b0bf1be9` → `59cbfe2f`) | `59cbfe2f4b96a73c2697cf81eb989e1d72e276fd` (branch `master`) |
| `tools/check-limine-pins.py` | `7d79ac29…` = freeze manifest, unchanged |
| `tools/limine-pin-battery-r96.py` | `f06d90ae…` = freeze manifest |
| `tools/make-r96-bends.py` | `efd1b2a1…` = freeze manifest |
| `tools/check-r96-calibration.py` | `7ff63524…` = freeze manifest at `59cbfe2f` (see §5 drift note) |
| `tools/check-registry-coverage.py` | `6fcb2d0a…` = freeze manifest |
| pre-round tree | `git archive 73c47107` → `/fast/scratch/…/tree73` (r95 battery blob `dd943287` at both `b8f878c8` and `73c47107`) |
| clone layout | `git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin clone96` at `59cbfe2f`, gate/battery hashes equal the freeze |

Scratch `/fast/scratch/hyaku/tsukuroi-r96/CriticClaims` (deleted at the end of the seat).

## 1. Findings

### F-1 — `falsifies-number` — C1 target: the N02 leg carries **4 error rows**, the target says 0

The frozen target says: "each bend: `102/103` (N04 `101/103`) unmet in each of three runs in both
layouts with exactly the frozen `failed_families` and **0 error rows**". Measured, one development
run per bend in the canonical lane and N02/N04 in the clone:

```
t-N01-echo-wrong.json            unmet 102/103 failed=EXPLICIT-VERSION-ECHO                    error_rows=0
t-N02-y-cap-8.json               unmet 102/103 failed=REFUSAL-VERSIONS-9DIGIT-Y                error_rows=4
    family=REFUSAL-VERSIONS-9DIGIT-Y error=bad-output: JSONDecodeError rc=64 stderr=usage: gate.py …
t-N03-era-label-flip.json        unmet 102/103 failed=EXPLICIT-VERSION-ERA                     error_rows=0
t-N04-extra-components.json      unmet 101/103 failed=EXTRA-COMPONENT,REFUSAL-VERSIONS         error_rows=0
clone-N02-y-cap-8.json           unmet 102/103 failed=REFUSAL-VERSIONS-9DIGIT-Y                error_rows=4
clone-N04-extra-components.json  unmet 101/103 failed=EXTRA-COMPONENT,REFUSAL-VERSIONS         error_rows=0
```

The mechanism is deterministic, not flaky: the Y family is a verdict family (not a `usage` family),
so `run_gate()` runs the gate with `--limine-version 12.999999999.4|0.999999999.0`; under N02 the
gate refuses (rc 64, empty stdout), `json.loads("")` raises and `run_gate` returns
`(None, "bad-output: JSONDecodeError rc=64 …")`, which the case log records in its `error` field —
4 cases per family per run, 4 rows every run. The same shape is what round 95's ledger recorded for
N05 ("4 rc-64 error rows per run"), so the r96 freeze repeated the r95 A1 pattern instead of
inheriting the correction.

Consequence: the frozen **kill rule** reads "unmet if any bend run … carries a non-null `error` row".
Under the instrument's actual behaviour C1 is therefore unmet by its own kill rule until an
amendment narrows the sentence. This is the QUALITY 140 defect (a target clause the instrument
cannot emit) found by exactly the "one development run" that criterion prescribes.

**Amendment state.** The L1 has already filed this defect as **A3** in
`.ufo/waves/round-96/before/plan-amendments-A1-A2.md` (datum: `w1/ExecBend/bend-N02*`,
`w1/ExecBattery/c1-bend-N02-y-cap-8.json`). My raw measurement agrees with A3's numbers exactly
(N02 4 rows, N01/N03/N04 0, both layouts), so this seat adds the clone leg and the mechanism
(`run_gate` → `json.loads("")` → `bad-output: JSONDecodeError rc=64`) and nothing to the count.
The frozen sentence stays as filed; until A3 is applied at scoring, C1's kill rule reads unmet on
its own "0 error rows" clause.

### F-2 — `falsifies-wording` — C1 predicate: `EXTRA-COMPONENT` is a twin, and "sampled once" is false for the instrument

Measured:

```
r95 roster size 99 unique 99
r96 roster size 103 unique 103
added ['EXPLICIT-VERSION-ECHO', 'EXPLICIT-VERSION-ERA', 'REFUSAL-VERSIONS-9DIGIT-Y', 'EXTRA-COMPONENT']
removed []
r95 REFUSAL_VERSIONS contains a four-component value: ['12.9.5.1']
r95 usage_check sends 12.9.6.1: True
```

and, decisively for the twin test:

```
dn-N04-extra-components.json  unmet 98/99 failed=REFUSAL-VERSIONS  error_rows=0
```

i.e. **the r95 roster alone kills N04** — its pre-existing `REFUSAL_VERSIONS` row (`12.9.5.1`)
already answers "four-component value refused rc 64". No committed bend separates
`EXTRA-COMPONENT` from `REFUSAL-VERSIONS`: both are `run_usage` families whose expectations change
under the same one clause (`len(parts) != 3` → `len(parts) < 3`), and every EXTRA-COMPONENT value
(`12.9.6.1`, `12.9.6.1.0`, `12.9.6.99`, `12.9.6.7`) is refused by the same comparison as
`12.9.5.1`. Under QUALITY 136's second clause ("a family that only re-answers a case the old roster
already covered is a twin, not a boundary") `EXTRA-COMPONENT` is a twin; under 136's first clause
("a family whose expected answer does not change under any committed bend is not a closure") it is
not. The two clauses conflict at this family because *its bend answers through another family*. The
measured discrimination delta of the round is therefore **three** families, carried by a roster that
went 99 → 103.

Secondary: the predicate's parenthetical "the four-component class was sampled once before this
round" is true of the family roster and false of the instrument — the r95 battery's own
`--usage-check` mode already sends `12.9.6.1` expecting rc 64
(`receipts/roster-delta.txt`). That is the same over-scope that round 95's routed defect 5 (r95 A4)
corrected in `corpus/README.md` ("the before instrument has no in-bound 9-digit case" — false for
the whole instrument), reappearing at a new site.

**Amendment needed (A4 — next free letter; A1/A2/A3 are filed, and this finding is not among them;
wording of the predicate only):**
> four new roster names (99 → 103); three of them (`EXPLICIT-VERSION-ECHO`, `EXPLICIT-VERSION-ERA`,
> `REFUSAL-VERSIONS-9DIGIT-Y`) sample classes the r95 roster does not; `EXTRA-COMPONENT` re-answers
> the four-component refusal class the r95 roster already carries (`REFUSAL_VERSIONS` value
> `12.9.5.1`) and the r95 instrument's `--usage-check` mode already sends (`12.9.6.1`), and the r95
> roster alone kills its bend (98/99 unmet, `REFUSAL-VERSIONS`), so it is a twin under QUALITY 136
> and the round's measured discrimination delta is three families.

Everything else in the C1 predicate measured true (§3, lines C1-2…C1-5).

### F-3 — `falsifies-wording` — C2 predicate: the checker is a remedy checklist, not a counter of self-assessment mismatches

Enumerated from the frozen bytes (`git show 38adc4ed:tools/check-r96-calibration.py`, hash
`7ff63524…`) and confirmed by four probes on fixture trees (`receipts/cal-probes.txt`):

| id | what it actually reads | class |
|---|---|---|
| F1 quality-m1-criterion | three substrings (`round-95.md`, `M1`, `development run`) inside the criterion-140 block | presence of the remedy |
| F2 void-receipt | one recorded sha256 == current `tools/check-registry-coverage.py` bytes, the manifest line, and three substrings in `SCORECARD.md` §Round 96 | one claim-vs-bytes equality for the receipt this round introduces, rest substring |
| F3 docstring-superseded | substring absent/present in two r95 tools + one substring in the r96 lesson | presence of the remedy |
| F4 readme-scope | two substrings in `corpus/README.md` | presence of the remedy |
| F5 tip-receipt | parses one receipt JSON's recorded `status`/`revision`/`counts`; **no re-measurement** | lint of a receipt |
| F6 report-count | report prose count vs the rows of `.ufo/waves/round-96/claim-falsification.tsv` | the only self-assessment-vs-bytes count, and only against the round's own ledger |

Probes (measured, `receipts/cal-probes.txt`):

```
E1b tools/ reduced to 3 files, receipt still 151/151 registered: PASS (no finding)
E2  tokens-in-denial criterion 140: PASS (no finding)
E3  report binds to an all-neutral ledger: PASS (no finding)
E4  correct r96 count preceded by the r95 sentence: [('F6', 'report says 4 falsifies-wording, tsv has 3')]
```

E1b: a tree with **three** files in `tools/` still passes the finding that certifies the tip receipt
(151/151). E2: a criterion 140 that says it is *not* a criterion passes F1. E3: a report that
states `0 falsifies-wording / 0 falsifies-number` against an all-neutral ledger passes F6. E4: a
**truthful** report is rejected by F6 because `re.search(r"(\d+)\s+`?falsifies-wording", text)`
binds the first numeric occurrence in the whole document — here round 95's wrong count quoted as
history — not the round-96 statement.

So none of F1–F6 re-measures an r95 fact (no `check-registry-coverage.py --revision b8f878c8`, no
`limine-pin-battery-r95.py --gate` run, no re-derivation of the 21-row ledger), and only F6 touches
a recorded number at all. The frozen predicate's "counts the six routed r95 mismatch classes (F1-F6)"
reads as calibration and is in fact six checks that *the repair was written*. Its literal test
("at least one finding in each of F1-F6 before, 0 after, selftest 7/7") is met (§4), so this is a
wording over-statement, not a failed measurement.

**Amendment needed (A5 — next free letter after A4; wording of the predicate only):**
> the checker asserts six remedy conditions, one per routed r95 defect: F1/F3/F4 are substring
> conditions on the repair text, F2 binds one recorded sha256 to one tool's current bytes, F5 lints
> a committed receipt without re-measuring it, and F6 is the single finding that binds a recorded
> number (the report's prose count) to committed bytes (the round's own ledger) — and it binds the
> first numeric occurrence of each class, so a truthful report that quotes the r95 wrong count
> first is rejected (measured). None of the six re-measures an r95 fact; the claim is that the six
> repairs exist and that the report's own count agrees with its ledger.

F6's first-match binding should also be fixed in the checker this round (parse the sentence that
names the round-96 ledger, or anchor on a round-96 marker), otherwise "0 findings after" can be
achieved or lost by prose ordering rather than by the count.

### F-4 — `falsifies-wording` — C1: the Y family's own docstring names the wrong era channel (instrument text, not the frozen claim)

`fam_refusal_versions_9digit_y`'s docstring says "one that reads the era from `X` alone answers era B
for `0.999999999.0` and fails". Built that gate in scratch (`gate-era-x-only.py`, one line:
`era_b = version >= VISIBILITY_ERA_SPLIT` → `era_b = version[0] >= 12`) and ran the families
(`receipts/era-reader-mutant.txt`):

```
REFUSAL-VERSIONS-9DIGIT-Y  all 4 cases case_ok=true (era "12.9.5+" for 12.999999999.4, "pre-12.9.5" for 0.999999999.0)
EXPLICIT-VERSION-ERA       12.9.4 case_ok=false (got era "12.9.5+", pins panic, want prompt)
EXPLICIT-VERSION-ECHO      12.9.4 case_ok=false (same era-driven flip)
```

An X-only era reader **passes the Y family** and is caught by the ERA family. The Y family does
discriminate a Y-only bound (F-5/C1-4), but not an era bug, and the docstring attributes to it a
discrimination it does not have. No frozen text needs changing (the predicate for Y only says
"accepted with its era's own answer, never rc 64"); the tool docstring does. This is the r95 routed-4
pattern (superseded/false claim left standing in a frozen tool's docstring) recurring in a new tool.

## 2. What did **not** falsify

- C1's roster arithmetic: 99 → 103 with exactly the four names, none removed (`roster-delta.txt`).
- `EXPLICIT-VERSION-ECHO`: landed gate echoes `12.9.4`/`12.9.5` with source `flag`
  (`family-probe.json`; the landed run's case log carries all four versions per family per run, `t-landed-3run.json`).
- `EXPLICIT-VERSION-ERA`: `pre-12.9.5` for 12.9.4 and `12.9.5+` for 12.9.5/12.9.6/999999999.9.9
  (`family-probe.json`, case log versions `['12.9.4','12.9.5','12.9.6','999999999.9.9']` ×3 runs).
- `REFUSAL-VERSIONS-9DIGIT-Y`: `12.999999999.4` era B, `0.999999999.0` era A, both rc 1 (never 64),
  with era-specific answers (`panic` vs `prompt`). A **Y-only** bound is discriminated: N02 fails
  exactly this family, and the r95 do-nothing battery is blind to N02 (`met 99/99`).
- `EXTRA-COMPONENT`: four refusals rc 64 with 0-byte stdout plus the same-list control `12.9.6`
  answering rc 0 (`family-probe.json` rows `usage_ok=true`, 5 rows each).
- Landed gate: `103/103 met` ×3 canonical (`t-landed-3run.json`, 412 cases each, 0 error rows) and
  `103/103 met` ×1 in the `--shared` clone (`t-clone-1run.json`).
- Do-nothing legs: `99/99 met` on the landed gate and N01/N02/N03; `98/99 unmet
  ["REFUSAL-VERSIONS"]` on N04 — exactly the frozen reading (`dn-*.json`).
- C2 before-leg: `git archive 73c47107` + the r95 report + the r95 ledger ⇒ `status FAIL` with
  F1,F2,F3,F4,F5,F6 all present (`cal-before.json`).
- C2 selftest: `selftest PASS 7/7`, each one-fault fixture firing exactly its own id and the clean
  fixture none (`cal-selftest.txt`).
- C2 after-leg at `59cbfe2f`: F1–F5 green; only F6 fires because
  `.ufo/waves/round-96/claim-falsification.tsv` is not committed yet (`cal-current.json`, run with a
  throwaway report). Not evaluable until the round files its report and ledger — reported as
  pending, not as a pass.

## 3. PASS/FAIL per expected line

| expected line (frozen claim) | verdict | receipt |
|---|---|---|
| C1-1 roster "beyond the r95 roster (99)" = +4 names | **PASS** (99→103, exact delta) | `roster-delta.txt` |
| C1-2 ECHO: echo equals flag, source `flag` | **PASS** | `family-probe.json` |
| C1-3 ERA: `pre-12.9.5` for 12.9.4, `12.9.5+` for other three | **PASS** | `family-probe.json`, `t-landed-3run.json` |
| C1-4 Y: accepted with era's own answer, never rc 64 | **PASS** | `family-probe.json`, `t-N02-*.json` |
| C1-5 EXTRA-COMPONENT: 4 refusals rc 64 + `12.9.6` rc 0 | **PASS** | `family-probe.json` |
| C1-6 landed `103/103 met` ×3, `failed_families []`, 0 error rows | **PASS** | `t-landed-3run.json` |
| C1-7 landed gate in `git clone --shared` | **PASS (1 run measured, not 3)** | `t-clone-1run.json` |
| C1-8 bends `102/103` (N04 `101/103`), exact `failed_families` | **PASS** (N01/N03 canonical; N02/N04 canonical+clone) | `bend-summary.txt` |
| C1-9 bends "0 error rows" | **FAIL** — N02 carries 4 in both layouts | `t-N02-y-cap-8.json`, `clone-N02-y-cap-8.json` |
| C1-10 do-nothing `99/99 met` on landed/N01/N02/N03 | **PASS** | `dn-*.json` |
| C1-11 do-nothing on N04 `98/99` `["REFUSAL-VERSIONS"]` | **PASS** | `dn-N04-extra-components.json` |
| C1-12 instrument bytes == freeze manifest | **PASS** at `59cbfe2f` | §0 hashes |
| C2-1 before: ≥1 finding in each of F1–F6, `status FAIL` | **PASS** | `cal-before.json` |
| C2-2 `--selftest` reads `PASS 7/7` | **PASS** | `cal-selftest.txt` |
| C2-3 one-fault fixtures fire exactly their own id; clean none | **PASS** | `cal-selftest.txt` |
| C2-4 after: `status PASS`, `findings []` | **NOT EVALUATED** (report/ledger not filed; F1–F5 green) | `cal-current.json` |
| C2-5 "counts the six routed r95 mismatch classes" | **FAIL as worded** — remedy checklist; only F6 counts a recorded number | `cal-probes.txt` |

## 4. Commands (exact, from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`)

```
sha256sum tools/check-limine-pins.py tools/limine-pin-battery-r96.py tools/make-r96-bends.py \
          tools/check-r96-calibration.py tools/check-registry-coverage.py
python3 -c "…importlib load limine-pin-battery-r96 / r95 blob…; print roster sizes, delta"
python3 tools/limine-pin-battery-r96.py --gate tools/check-limine-pins.py --runs 3 \
        --work /fast/scratch/hyaku/tsukuroi-r96/CriticClaims/w1 \
        --json /fast/scratch/hyaku/tsukuroi-r96/CriticClaims/t-landed-3run.json
for b in N01-echo-wrong N02-y-cap-8 N03-era-label-flip N04-extra-components; do
  python3 tools/limine-pin-battery-r96.py --gate .ufo/waves/round-96/before/controls/bends/$b.py \
          --runs 1 --work …/w2 --json …/t-$b.json; done
for g in tools/check-limine-pins.py …/bends/N0*.py; do
  python3 .ufo/waves/round-96/before/controls/do-nothing-battery-r95.py --gate $g --runs 1 \
          --work …/w3 --json …/dn-$(basename $g .py).json; done
git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin clone96   # then, inside it:
python3 tools/limine-pin-battery-r96.py --gate tools/check-limine-pins.py --runs 1 --work …/wc --json …/t-clone-1run.json
python3 tools/limine-pin-battery-r96.py --gate .ufo/…/bends/N02-y-cap-8.py --runs 1 …  (same for N04)
git archive 73c47107 | tar -x -C …/tree73
python3 …/cal-frozen.py --root …/tree73 --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-95/tsukuroi.md \
        --tsv .ufo/waves/round-95/claim-falsification.tsv --json …/cal-before.json
python3 …/cal-frozen.py --selftest
python3 …/cal-frozen.py --root . --report …/dummy-report.md --tsv .ufo/waves/round-96/claim-falsification.tsv --json …/cal-current.json
python3 …/cal-probe.py ; python3 …/cal-probe-e1b.py ; python3 …/cal-probe-e4.py
python3 <inline driver>  → build each of the four families twice and call run_gate/run_usage (family-probe.json)
python3 <inline driver>  → same, with scratch gate-era-x-only.py (era-reader-mutant.txt)
python3 .ufo/waves/round-95/before/controls/count-runs.py …/t-landed-3run.json \
        --family EXPLICIT-VERSION-ECHO --family EXPLICIT-VERSION-ERA \
        --family REFUSAL-VERSIONS-9DIGIT-Y --family EXTRA-COMPONENT
python3 tools/check-registry-coverage.py --revision 59cbfe2f
```

`cal-frozen.py` is `git show 38adc4ed:tools/check-r96-calibration.py` (sha256 `7ff63524…`). The
probes import that frozen module and build their own fixture trees; no lane byte is written by any
of them.

## 5. Side observations (not findings against the two sentences)

- **Instrument drift observed and resolved mid-seat.** At ~08:04 the working tree carried
  `tools/check-r96-calibration.py` sha256 `ad894667f951d2cc…` (whitespace-flattening edit from a
  sibling seat), i.e. ≠ the freeze's `7ff63524…`, which under C2's own void clause would have made
  the claim void had scoring happened in that window. At `59cbfe2f` the file is back to
  `7ff63524…`; the claim is intact at the tip I measured. This independently reproduces the L1's
  filed **A2** disclosure (`before/plan-amendments-A1-A2.md`), including its window.
- **Registry state at `59cbfe2f`**: `check-registry-coverage.py --revision 59cbfe2f` → `status FAIL`,
  151 registered / 154 tools, three `REGISTRY-ROW-MISSING` (the three r96 instruments). Expected
  before the registry seat lands; recorded so the scorer does not read it as a C1/C2 defect.
- I installed and upgraded nothing; no pacman transaction was attempted.

## 6. Receipts

`.ufo/waves/round-96/w1/CriticClaims/receipts/`: `t-landed-3run.json`, `t-clone-1run.json`,
`t-N01-echo-wrong.json`, `t-N02-y-cap-8.json`, `t-N03-era-label-flip.json`,
`t-N04-extra-components.json`, `clone-N02-y-cap-8.json`, `clone-N04-extra-components.json`,
`dn-check-limine-pins.json`, `dn-N01-echo-wrong.json`, `dn-N02-y-cap-8.json`,
`dn-N03-era-label-flip.json`, `dn-N04-extra-components.json`, `bend-summary.txt`,
`roster-delta.txt`, `family-probe.json`, `era-reader-mutant.txt`, `cal-before.json`,
`cal-current.json`, `cal-selftest.txt`, `cal-probes.txt`, `count-runs-new-families.json`,
`registry-59cbfe2f.txt`.

{"seat":"CriticClaims","verdict":"findings","notes":"C1 falsified on two lines: (a) falsifies-number — the N02 bend leg carries 4 error rows (bad-output JSONDecodeError rc=64) in canonical and clone (measured independently; the L1 already files this as A3, and my numbers match A3 exactly), so the frozen '0 error rows' target cannot be emitted and C1's own kill rule reads unmet until A3; (b) falsifies-wording — EXTRA-COMPONENT is a twin under QUALITY 136 (the r95 roster alone kills N04, 98/99 [REFUSAL-VERSIONS]; no bend separates it from REFUSAL-VERSIONS; the r95 --usage-check already sent 12.9.6.1), so the measured discrimination delta is three families, not four (proposed A4). Roster 99->103, echo/era/Y/extra-component content, landed 103/103 x3 + clone, all four bends' failed_families, and all five do-nothing legs measured exactly as frozen; the Y family does discriminate a Y-only bound (N02 kills only it; r95 blind) but its docstring wrongly credits it with catching an X-only era reader (measured: that reader passes all 4 Y cases). C2: six ids fire before (FAIL) and selftest is 7/7, but the checker is a remedy checklist — only F6 binds a recorded number to bytes, against the round's own ledger, and it binds the first numeric occurrence in the report (a truthful report is rejected, E4); F5 passes a tree with 3 tools; F1 passes a criterion that denies being one (proposed A5). C2 after-leg not evaluable yet (report/ledger unfiled; F1-F5 green at 59cbfe2f)."}
