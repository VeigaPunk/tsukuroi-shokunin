## Round 93 — the 12.9.5 tag's own cut and the installed-version probe (C1 depth, C2 operability)

- Freeze `c633f49a`: declaration `.ufo/plans/round-93.md`, instruments
  `tools/limine-pin-battery-r93.py` (`ddd7e955…`, 96 families: the r92 ISOLATION launcher plus a V3
  PATH exception for a case's fake `limine`), `tools/check-limine-pins.py` (`6b4c53d1…`, V3
  `--limine-version auto` = read-only `limine --version` probe, `limine_version_source`, probe failure
  = rc 64/empty stdout, selftest 37 → 39 rows), `tools/make-r93-bends.py` (`d0c3d3e7…`, six one-clause
  bends), do-nothing controls (r92 gate `35c1088b…`, r92 battery `aef33925…`), a 14-line freeze
  manifest and a 13-line instrument-only manifest.
- C1: the battery gains `ERA-EXACT-125` (the exact 12.9.5 boundary), `ERA-B-FIRST-BODY` (a key on the
  first body line), `ERA-B-U1` (whole-file U1 in era B) and `REFUSAL-VERSIONS` (ten out-of-range values,
  one case). Landed gate `96/96 met` x3 canonical and x3 in a `git clone --shared`; N01→`ERA-EXACT-125`,
  N02→`ERA-B-FIRST-BODY`, N03→`ERA-B-U1`, N04→`REFUSAL-VERSIONS`, `unmet` x3 both layouts with 0 error
  rows; the r92 battery still reads `89/89` on the new gate (no regression).
- C2: `--limine-version auto` resolves the installed bootloader read-only (5 s, first `X.Y.Z` after
  `limine`), records `limine_version`/`limine_version_source: probe`, selects the era from it, and
  refuses on the certified failure shapes; `AUTO-ERA-A/B` and `AUTO-PROBE-FAIL` `met` x3 canonical and
  clone; N05/N06 `unmet` x3 both; the root live run reads 12.9.4/`probe`/era A with the two
  operator-owned pin mismatches (lines 30/38), the unprivileged run reads the same fields with rc 2.
- Corpus: `corpus/SOURCES.md` 381 → 385 rows (S382 v12.9.5 `config.c`, S383 v12.9.5 ChangeLog, S384
  v12.9.5 `host/limine.c`, S385 version-pinned Python 3.15 docs); S377's anchor and S384's raw-line
  anchor corrected by logged old→new changes; `corpus/knowledge/limine-version-probe-r93.md`
  (VP1-VP4); SKILL.md gains the `limine-pin-battery-r93` and `make-r93-bends` rows plus R93-REG-1.
- Wave w1: 14 seats (5 executor, 2 reviewer, 2 critic, 2 mutation-tester, 1 scout, 1 scribe,
  1 connector; 7 attack = 50%), 0 dead; the attack receipts falsified five predicate wordings (N02's
  label, the tenth refusal member, whitespace-only stdout, the live parenthetical, the parse clause),
  each narrowed by amendments A2/A3; the route list is in `corpus/lessons/round-93.md` §Routed.
- Lesson `corpus/lessons/round-93.md` (Gate S382-S385, M1 landing smoke, M2 calibration, M3 inherited
  landing); SCORECARD round-93 declaration/outcome and the capability `installed-version-probe`; QA
