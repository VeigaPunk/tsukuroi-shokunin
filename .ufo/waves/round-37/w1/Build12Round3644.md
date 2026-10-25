# Build12Round3644 — round-36 LOG typo reproduction (design item 12/12)

Seat: `Build12Round3644` · role executor · round 37 w1 · axes: operability,
`build:round-36 LOG typo reproduction` · milestone: Independent runnable design.
Lane bounds honoured: lane files read-only; seat output only under
`.ufo/waves/round-37/w1/Build12Round3644/`; no git/jj writes anywhere
(no commits needed; no mktemp repo required). No tools installed or updated
(RULES.md record: zero installs; python3 stdlib only; pacman untouched).

## 1. Located defect (evidence opened this round)

- `LOG.md:1379` (read raw): the round-36 wave-2 LOG heading reads
  `## Round 36 — wave 2, measured outcome, budget-forced landing (2026-10-24T04:4043Z stamped via date -u)`.
  The stamp `2026-10-24T04:4043Z` has a four-digit minute field `4043` — not a
  valid time.
- `corpus/lessons/round-36-verifier-spotcheck.md` § item 3: "**LOG stamp typo**
  (new instance of the bad-stamp class): `LOG.md` round-36 wave-2 heading reads
  `2026-10-24T04:4043Z` — not a valid time; omit or restamp honestly per
  R36-PLACEHOLDER-TIME's fix."
- `corpus/lessons/round-36.md` R36-PLACEHOLDER-TIME row: "Omit a time stamp
  rather than placeholder it; the real ExecProbeR36 settle time is stat-able
  from its report mtime." (`SCORECARD.md` lines ~1809-1811 record the same
  fix.) The round-36 declaration erratum (`LOG.md:1373`) fixes the convention:
  round-36+ LOG/SCORECARD heading stamps are UTC (`date -u`).

## 2. Deliverable — isolated runnable check

`check-round36-log-stamps.py` (executable; stdlib only; runs anywhere):

- Scans only `## Round N …` headings with N ≥ 36 (UTC-convention scope) of the
  LOG file; extracts ISO-like stamp tokens
  (`YYYY-MM-DD[T ]HH:MM[:SS]Z` family, including malformed shapes `04:4043Z`
  and `03:5xZ`); validates timezone suffix, two-digit 00–59 minutes, and
  calendar-validity.
- Exit 0 = no malformed stamps; exit 1 = ≥1 invalid stamp; exit 2 = input error.
- Usage: `python3 check-round36-log-stamps.py [--log PATH]` (default: lane root
  `LOG.md`); `--selftest` runs 7 embedded cases (baseline typo, corrected,
  omitted, valid freeze, legacy pre-36 ignored, placeholder minutes, no r36
  headings) — all 7 passed, selftest exit 0.

## 3. How the check fails on unchanged baseline

Run on the untouched lane `LOG.md` (read-only) and on `fixture/log-baseline.md`
(byte copy of the lane file); both fail identically:

```
LOG-STAMP-INVALID line 1379: '2026-10-24T04:4043Z' (minute field '4043' is not a two-digit 00-59 value)
LOG-STAMP-CHECK headings_checked=4 findings=1
# exit 1
```

The other three round-36 headings (declaration, pre-freeze, freeze) validate
clean; only the wave-2 stamp is malformed.

## 4. After state the check measures

`fixture/log-corrected.md` = baseline copy with the single patch applied
(restamp `04:4043Z` → `04:40Z`); the check passes:

```
LOG-STAMP-CHECK headings_checked=4 findings=0
# exit 0
```

So the after state is: every round ≥36 LOG heading carries either no stamp or a
calendar/clock-valid UTC stamp. Omitted-stamp and legacy forms are also covered
by the selftest. The precise one-line patch proposal is
`fixture/patch.diff` (only hunk: `LOG.md:1379`, `-2026-10-24T04:4043Z` →
`+2026-10-24T04:40Z`). Note: `04:40Z` is a demonstrative valid restamp; the
honest value per R36-PLACEHOLDER-TIME is the real recorded time (derivable from
the wave-2 evidence/commit stamps), or the stamp may be omitted — both after
states pass this check.

## 5. Risks

- Scope is round ≥ 36 only; pre-convention legacy stamp formats are deliberately
  not flagged (selftest-pinned).
- The check validates shape and calendar validity, not that a stamp equals the
  commit time (clock-honesty is a separate erratum class, round-35 §5).
