# Round 96 — declaration (frozen before any candidate is scored; controls committed with it)

Lane: tsukuroi (operability + freshness; host operability and repair). Fleet campaign: hyaku, run 15.
Round: 96 (attempt 1). Pre-round lane tip: `73c47107e8bda79375517ee24ec3c13688586305`.

## Inputs read before this freeze

- The round-95 closure (`MANIFEST.json` `rounds[]`): admitted; C1 depth (99/99 met, N05 98/99 unmet),
  C2 operability (registry PASS 151/151).
- The round-95 non-author spot-check `corpus/lessons/round-95-verifier-spotcheck.md` §6 routed 1-7
  and its conformance defects (report prose count, `QUALITY.md` owes M1 a criterion, dead void
  pointer, superseded superlative, README over-scope, derived-not-measured revisions).
- The round-95 lesson `corpus/lessons/round-95.md` (M1, Routed).
- `corpus/QUALITY.md` 124-139 (139 is the numeric-bound rule; 140 is the criterion routed 2 owes).
- `corpus/README.md` § "Round 95" and its Frontier bullets (six named limits).
- `SCORECARD.md` axes: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8.
  Lowest non-retired axes: **depth 8** and **adjacency 8** (tied). C1 works depth.
- `considerthese/2026-10-26.md` (the newest proposal batch; the assimilation item rides §2b).
- Previous rejected closures stay on the record; nothing is re-declared from them.

No adjacency move is declarable this round: the one open adjacency item (kaidoku/revenger
reverse-engineering ownership) is operator-owned and unruled; reported, not absorbed.

## Claims (2; frozen sentences; the same sentence in `claims.json`)

### C1 — depth 8 (tied lowest) — the echoed version, the era field and the per-component accepted leg

**Predicate.** `tools/limine-pin-battery-r96.py --gate G --runs 3` carries, on fixtures generated
fresh per run, four families beyond the r95 roster (99): `EXPLICIT-VERSION-ECHO` (one explicit
version per case — `12.9.4`, `12.9.5`, `12.9.6`, `999999999.9.9` — on an era-sensitive fixture: the
JSON `limine_version` equals the flag value and `limine_version_source` is `flag`);
`EXPLICIT-VERSION-ERA` (the same four versions: `visibility_era` reads `pre-12.9.5` for 12.9.4 and
`12.9.5+` for the other three); `REFUSAL-VERSIONS-9DIGIT-Y` (`12.999999999.4` era B and
`0.999999999.0` era A, each accepted with its era's own answer, never rc 64);
`EXTRA-COMPONENT` (`12.9.6.1`, `12.9.6.1.0`, `12.9.6.99`, `12.9.6.7` refused rc 64 with empty
stdout, with `12.9.6` as the same-list positive control answering rc 0). The landed gate reads
`103/103` met in every run; against four one-clause bends the same battery reports exactly
`N01-echo-wrong` -> `["EXPLICIT-VERSION-ECHO"]`, `N02-y-cap-8` ->
`["REFUSAL-VERSIONS-9DIGIT-Y"]`, `N03-era-label-flip` -> `["EXPLICIT-VERSION-ERA"]`, and
`N04-extra-components` -> `["EXTRA-COMPONENT", "REFUSAL-VERSIONS"]` (the second member is the
pre-existing `12.9.5.1` row — the four-component class was sampled once before this round).

**Target.** Landed gate: `103/103` met in each of three runs, `failed_families []`, 0 error rows, in
the canonical lane and in a `git clone --shared`; each bend: `102/103` (N04 `101/103`) unmet in each
of three runs in both layouts with exactly the frozen `failed_families` and 0 error rows; the r95
do-nothing battery (`before/controls/do-nothing-battery-r95.py`, byte-identical to the r95 landed
bytes) on the landed gate and on N01/N02/N03: `met` `99/99` in each of three runs in both layouts;
the same battery on N04: `98/99` unmet with `failed_families` exactly `["REFUSAL-VERSIONS"]` and 0
error rows (blindness receipt for the three new families and the four-component correction).

**Kill rule.** Unmet if any landed-gate run reads below 103/103 or carries a non-null `error` row;
unmet if any bend run is not `unmet`, carries a non-null `error` row, or its `failed_families` is
not exactly the frozen list; unmet if any do-nothing leg differs from its frozen reading above;
void if any instrument byte differs from `.ufo/waves/round-96/before/instruments.sha256` at scoring
time.

**Counting command.**
`python3 tools/limine-pin-battery-r96.py --gate <GATE> --runs 3 --work <scratch> --json <out>`; then
`python3 .ufo/waves/round-95/before/controls/count-runs.py <out> --family EXPLICIT-VERSION-ECHO
--family EXPLICIT-VERSION-ERA --family REFUSAL-VERSIONS-9DIGIT-Y --family EXTRA-COMPONENT`.

**Do-nothing and near-miss controls (committed with this freeze).**
`before/controls/do-nothing-battery-r95.py` (sha256 `a51dca18…`, byte-identical to the r95 landed
battery), `before/controls/do-nothing-gate-r95.py` (sha256 `7d79ac29…`, the unchanged gate),
`before/controls/bends/N01-echo-wrong.py` … `N04-extra-components.py` (emitted by
`tools/make-r96-bends.py`, each exactly one clause and asserted one match). The landed gate is
unchanged this round: C1 is instrument work, so no gate byte moves.

### C2 — calibration 9 — the lane's recorded self-assessment against its bytes: six mismatch classes -> 0

**Predicate.** `python3 tools/check-r96-calibration.py --root R --report F --tsv T` reports
`status PASS` with `findings []` at the landed tree with the filed round-96 report and the committed
round-96 ledger; against a `git archive` of `73c47107` with the r95 report and the r95 ledger the
same checker reports at least one finding in each of F1-F6 and `status FAIL`; the checker's
`--selftest` reads `PASS 7/7`, and each of its six one-fault fixtures fails exactly its own finding
(clean fixture: none).

**Target.** After: 0 findings. Before: six classes present (`F1 quality-m1-criterion`, `F2
void-receipt`, `F3 docstring-superseded`, `F4 readme-scope`, `F5 tip-receipt`, `F6 report-count`).
Selftest 7/7. No work: the pre-round tree cannot reach 0 (it has no receipts, no criterion, the
superlative, the over-scope sentence, and a report whose count is a word the checker cannot bind).

**Kill rule.** Unmet if any of F1-F6 is absent before, if any finding remains after, if the selftest
is not 7/7, or if any one-fault fixture fires another id; void if `tools/check-r96-calibration.py`
differs from the freeze manifest at scoring time.

**Counting command.**
`python3 tools/check-r96-calibration.py --root <tree> --report <report> --tsv <ledger>` and
`python3 tools/check-r96-calibration.py --selftest`.

**Do-nothing control (committed with this freeze).** `before/c2-before-73c47107.json` — the
checker's own run against the pre-round archive, r95 report and r95 ledger (status FAIL, six
classes). The six one-fault fixtures are built inside `--selftest` (no lane bytes written).

## Limits declared before data

- C1 certifies metadata the *gate* emits; it does not read the upstream binary beyond the versions
  already sourced (S382-S384, S389-S390).
- `EXTRA-COMPONENT` broadens a class the r95 roster sampled once (`12.9.5.1`); its bend is also
  killed by that pre-existing row, which this declaration records instead of claiming a first.
- C2 counts the six routed r95 defects; it is not a claim that the lane's self-assessment is
  generally true, and it rewrites no frozen predicate or filed report byte.
- The r95 freeze manifest pins the *r95 landed* bytes; the r95 tool docstrings are corrected this
  round, so `sha256sum -c .ufo/waves/round-95/before/instruments.sha256` no longer holds in the
  working tree — the bytes it pinned are re-derivable at `b8f878c8`, and the round lesson says so
  (this is the routed-4 relation, not a claim that the historic manifest changed).

## Amendment slot

Amendments are appended here (A1, A2, …) with the datum that forced them, exactly as in rounds
92-95. A claim's predicate, counter, kill rule and target are never rewritten after any candidate
score; a narrowing is an amendment plus a report sentence, never an in-place edit.
