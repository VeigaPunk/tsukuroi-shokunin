# Round 96 lesson — tsukuroi lane

Integrated by the L1 from the `ScribeLesson` draft (`.ufo/waves/round-96/w1/ScribeLesson/`) and the
wave's attack seats. Pre-round tip `73c47107e8bda79375517ee24ec3c13688586305`; freeze `38adc4ed`;
wave `b0bf1be9`; the corrections below land at the round's settle commit. The seat's own Gate table,
rejects, census before/after and Mistakes were re-read against the receipts they cite before this
integration; numbers this L1 could not re-derive are marked with their pointer, not adopted.

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

Pins under `ScribeLesson/pins/` (and the L1's own fetch under `.ufo/waves/round-96/after/gate/`);
fetch log and digests `ScribeLesson/receipts/01-gate-sources.sha256.txt`; located quotes
`receipts/02-gate-located-quotes.txt`; refusals `receipts/05-gate-rejections.txt`.

| row | URL opened 2026-11-08 | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S391 (new; supersedes S390) | https://docs.python.org/3.15/library/sys.html#sys.int_info.default_max_str_digits | A | "The default value for sys.get_int_max_str_digits() when it is not otherwise explicitly configured." (byte 157851 of the 280632-byte pin, sha256 `a7e00587…`) | **admit** — the configured default of CPython's decimal-conversion digit limit, the value a parser that hands a component to `int()` must bound itself against; it states no Limine behaviour. |
| S389 (re-open) | https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation | A | "The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits." (byte 785297 of the 815447-byte pin, sha256 `6bf2ce2b…`) | **admit** (re-open, byte-identical to the r95 pin) — the 4300-digit default the gate's 1-9-digit per-component cap sits under. |
| S382 (re-open) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/common/lib/config.c | A | "*(p - 1) = '\0';" (byte 10046, line 329; sha256 `a940acae…`) | **admit** (re-open) — the in-place config cut that dates the era boundary to v12.9.5. |
| S383 (re-open) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/ChangeLog | A | "Parse the config in linear time. Configs with thousands of entries were slow to load." (byte 168, line 8; sha256 `d2e08cc4…`) | **admit** (re-open) — upstream's release note for the in-place parse. |
| S384 (re-open) | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/host/limine.c | A | "puts(\"Limine \" LIMINE_VERSION);" (byte 67028, line 2035; sha256 `4da21c7c…`) | **admit** (re-open) — the `--version` line the probe parses. |
| S386-S388 (re-open) | v12.9.6 `common/lib/config.c`, `ChangeLog`, `host/limine.c` | A | config.c byte-identical to v12.9.5 (`a940acae…`); "A config whose first line is an entry has had no global options since 12.9.5." (byte 476, line 14; `ab280b45…`); the same `puts("Limine " LIMINE_VERSION);` line (`4da21c7c…`) | **admit** (re-open) — the v12.9.6 bytes and the upstream sentence for the 12.9.5 visibility boundary. |

Rejected this round (opened; receipts `.ufo/waves/round-96/after/gate/` and
`ScribeLesson/receipts/05-gate-rejections.txt`):

- `https://man.archlinux.org/man/limine.8` → **HTTP 404**, 2706 bytes, title "Page not found — Arch
  manual pages"; no such page, no behaviour. (Same refusal as r94/r95.)
- `https://api.github.com/repos/Limine-Bootloader/Limine/releases/tags/v12.9.6` → **HTTP 200**,
  26652 bytes, `tag_name` v12.9.6, body 512 bytes pointing at the ChangeLog and the signing key;
  states no Limine behaviour. Kept as a wave-directory locator, never a row.
- `https://man.archlinux.org/man/limine.conf.5` → **HTTP 404**, 2725 bytes; no such page.

Census (frozen command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi`): before `git archive 73c47107` → `exit 0`, 389 rows; after the landed tree → `exit 0`,
391 rows (`git show 73c47107:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'` → 389;
`grep -cE` at the tip → 391), 0 E findings, 58 W. Rows added by tier: two A (S390, then S391 superseding it under CORPUS.md rule 2 after the locator
correction). Rows touched old→new in place: S390 `status` mined→queued and `used-by`
`corpus/knowledge/limine-bound-per-component-r96.md`→`—`; S389 re-opened and still `mined`.
Frontier rows advanced: the r95 four-component bullet (corrected; see R96-FRONTIER-COUNTED-ONCE),
plus the new Z-cap, leading-zero, era-label and F6 limits in the README.

**The locator was wrong and is corrected by supersession.** The first row (S390) cited byte 157653
for the sentence; measured on the pinned page that byte lands inside the opening tag (the sentence
starts at 157851, the `id=` attribute at 157525). CORPUS.md rule 2 makes the correction a new row,
so S391 (`teaches` opens `supersedes S390`) carries the corrected anchor and the version-pinned
`/3.15/` URL, and S390's `used-by` moved to `—` (logged above). Class: calibration; captured-by: none (the census checks row shape, not byte
resolution); fix: the byte is re-derived from the pins by
`ScribeLesson/receipts/check-s390-locator.py` (which fails on the old value and passes on the new).

## Mistakes

- **R96-FRONTIER-NOT-SENT / R96-FRONTIER-COUNTED-ONCE** — class: self-assessment vs the instrument's
  bytes. Round 95's README Frontier said the four-component shape was "not sent at battery level",
  but the r95 roster's `REFUSAL_VERSIONS` carries `12.9.5.1` and the r95 `--usage-check` leg sends
  `12.9.6.1` (and reads `unmet` on the N04 bend: `{'version': '12.9.6.1', 'want_rc': 64, 'rc': 0,
  'ok': False}`). r96's first correction then said "sampled once", which is true of the roster and
  false of the instrument. Evidence: `ScribeLesson/receipts/04-mistakes-evidence.txt` §(a),
  `receipts/10-r95-usage-check-leg.txt`. Captured-by: none (a correction's own count is not
  re-derived). Fix: the README now says the class reached the r95 instrument twice and r96 broadens
  it a third time; A4 records the twin.
- **R96-N04-TWO-FAMILIES** — class: frozen target vs instrument reading. `N04-extra-components`
  fails two families (`EXTRA-COMPONENT`, `REFUSAL-VERSIONS`), not one; caught by the development run
  under `before/dev/` before dispatch. Captured-by: QUALITY 140 (the rule working). Fix: the frozen
  target states the two-family set; the report prints the raw list.
- **R96-N02-ERRORROWS** — class: frozen target vs instrument reading, one round after QUALITY 140
  entered. The N02 bend refuses the four Y-family cases (rc 64, empty stdout), so its receipt carries
  four non-null `error` rows per run; the frozen "0 error rows" clause cannot be emitted. Evidence:
  `w1/ExecBend/bend-N02-y-cap-8.json`, `w1/ExecBattery/c1-bend-N02-y-cap-8.json`. Captured-by:
  QUALITY 140 (the L1's development run printed the verdict but did not inspect the error-row field).
  Fix: A3 narrows the clause to landed-gate/do-nothing legs and the bend's own refusal rows; the
  report prints the counts.
- **R96-EXTRA-TWIN** — class: claimed discrimination vs measured. `EXTRA-COMPONENT` was declared as
  closing a class; the r95 roster alone kills the same bend (`98/99 unmet`, `REFUSAL-VERSIONS`) and
  the r95 `--usage-check` already sends `12.9.6.1`. Captured-by: QUALITY 136's twin clause (not
  applied before the freeze). Fix: A4 narrows the claim to a three-family discrimination delta; the
  family stays as coverage broadening.
- **R96-Y-DOCSTRING-ERA** — class: instrument text vs measured behaviour. The Y family's docstring
  says an X-only era reader fails it; such a reader answers `0.999999999.0` as era A (correct) and
  is caught on the other row / by the pre-existing era families (`w1/ReviewBattery` F3,
  `w1/CriticClaims` F-4). Captured-by: none (a docstring claim is not covered by a family). Fix:
  frozen bytes are not edited this round (C1's void clause); routed to r97 as a docstring
  correction with its own manifest.
- **R96-C2-REMEDY-CHECKLIST** — class: claim naming vs counter scope. C2's frozen sentence said the
  checker "counts" six mismatch classes; F1/F3/F4 are substring presence, F5 a receipt lint, only
  F6 binds a number (and the first numeric occurrence at that). Captured-by: `w1/CriticClaims` F-3
  (E1b-E4 probes), `w1/ReviewCalibration` §1.8. Fix: A5 narrows the sentence; the ledger-provenance
  and first-match limits are named in the README Frontier.
- **R96-FREEZE-DRIFT** — class: frozen bytes vs worktree. A post-freeze whitespace fix to the
  checker left the worktree (`ad894667…`) off the freeze manifest (`7ff63524…`) for ~6 minutes;
  `w1/ExecDoNothing` §4 and `w1/ExecControls` D1 read the drift, the L1 restored the pinned bytes
  (`sha256sum -c` 17 × OK at scoring), and the pinned checker passes after a wrap-only reflow of the
  r95 emitter. Captured-by: C2's own void clause + `sha256sum -c` in two seats. Fix: instruments are
  frozen by digest; a behavioural repair is an amendment plus a re-pin, never a worktree edit.
- **R96-REPORT-WORD-COUNT** (carried r95 routed 1) — class: report prose vs the committed ledger.
  r95 wrote "four `falsifies-wording` rows" where the ledger held six. Captured-by: none in r95;
  r96's C2 F6 makes the sentence machine-checkable (and binds the first numeric occurrence — a
  limit). Fix: this round's report states 3 falsifies-wording / 1 falsifies-number, matching the
  11-row ledger, and F6 reads 0 findings at filing.

## Counter-attack scoreboard (considerthese/2026-10-26.md, mined 2026-11-08)

The proposal "track how many attack arms the wave fielded, how many survived, and which class beat
it" was already adopted as QUALITY 115 at round 82 (`corpus/QUALITY.md:226`) but has not been
practised since r85; this round revives it (the honest residual is "not practised", not
"unimplemented" — `w1/ScoutDrift` D1). Implemented here for the round's counters. C1 fielded 4 one-clause bends + 8 mutants + 7
forgers: bends 4/4 killed at their named families; mutants 5/8 killed (M06 Z-cap and M08
leading-zero survive — Frontier; M07 `lower()` is equivalent); forgers 5/7 killed, F-E
(label-boundary-only) and F-G (trailing-zero) survive — Frontier. C2 fielded 6 one-fault fixtures
(all id-exact) plus 11 green-without-work probes (U1-U5, E1b-E4, atk-*), of which the first-match
and provenance passes are named limits (A5). The next round compares this table instead of
re-reading receipts.

## Amendment file and the frozen slot (ScoutDrift D2)

The five amendments A1-A5 live in
`.ufo/waves/round-96/before/plan-amendments-A1-A2.md` (the name was fixed when A1/A2 were written;
it holds A1-A5). The frozen plan's `## Amendment slot` is empty on purpose: the plan bytes are
pinned in `before/instruments.sha256` (`5d389241…`), so amendments are a sidecar file the ledger's
narrowing pointers name, never an in-place edit of the frozen declaration.

## Relation to the r95 freeze manifest (r95 routed 4)

The r95 freeze manifest pins the `b8f878c8` bytes. Round 96 edits only the two r95 tools' docstrings
(wording, not code), so `sha256sum -c .ufo/waves/round-95/before/instruments.sha256` no longer holds
in the working tree; the pinned bytes are re-derivable with `git show b8f878c8:<path> | sha256sum`,
and the r96 append-only rows record the correction rather than rewriting the historic manifest.

## Routed

| r95 routed item | r96 treatment | evidence |
|---|---|---|
| 1 report prose count | closed for r96 by C2 F6 (r95 bytes untouched) | `w1/ScribeLesson/receipts/04-mistakes-evidence.txt` §(c); `after/c2-after-landed.json` |
| 2 QUALITY owes M1 a criterion | closed — QUALITY 140 cites `round-95.md` M1 and a development run | `corpus/QUALITY.md` 140 |
| 3 dead void pointer | closed — receipt `6fcb2d0a…` + SCORECARD binding + empty `git diff` | `before/r95-registry-gate.sha256`; `SCORECARD.md` §Round 96 |
| 4 superseded superlative | closed — both r95 tools corrected; ASTs equal modulo docstrings; manifest relation above | `w1/ReviewCalibration/` §1.5 |
| 5 README over-scope | closed — sentence scoped to the r94 family roster | `after/c2-after-landed.json` (F4) |
| 6 derived C2 revisions | closed — `b8f878c8` PASS receipt committed | `before/c2-tip-b8f878c8.json` |
| 7 carried Frontier | still open except the four-component correction; r92 launcher residuals, r93 probe pre-release, r89 blanks/ESP/empty labels, registry content binding stay Frontier; new rows: Z cap, leading zeros, era label, F6 limits | `corpus/README.md` §Frontier (round-96) |
