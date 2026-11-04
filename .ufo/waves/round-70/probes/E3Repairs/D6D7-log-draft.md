# D6 / D7 — exact LOG.md text to append for round 69 (not written by this seat)

D6 (`LOG.md` carries one r69 landing entry; `68faae4`, `10a01ca`, `ea20c862` are not tied to any
entry) and D7 (the landing entry's "selftest 177 → 192" is not the final 196).

Owner: the L1 (only writer of the lane tree). This file is the text to append, byte-exact, at the end
of `LOG.md` (current last line 3025 is `Measured outcome and final counts follow the landing commit.`).
The existing "## Round 69 — landing" entry is **not** rewritten; the correction is appended, per the
lane's append-only erratum habit.

Citations used below, all re-read at lane tip `84e013a7`:

- `.ufo/reports/round-69/tsukuroi.md` (fleet repo) lines 56-65: the five-commit landed-changes list;
  line 42: "Selftest 192 → 194 → 196"; lines 69-70: the measurement header.
- `SCORECARD.md:5231` (outcome header), `:5233` (measured surface `7d7d3aee`), `:5246` (selftest
  `PASS (196 cases…`), `:5248` (cited-receipts PASS at `7d7d3aee`), `:5263` (selftest 192 → 194),
  `:5264` (selftest 194 → 196).
- `corpus/lessons/round-69.md:97` ("with 192 selftest cases (177 → 192)"), `:134` ("192 → 194").
- Gate receipts' own `rev=` lines: `after/gates-at-work.txt` `32c0b50e`, `after/gates-at-final.txt`
  `68faae46`, `after/gates-final.txt` `10a01ca`.
- Round-70 receipts in this directory (`.ufo/waves/round-70/probes/E3Repairs/`): the cited-receipts
  ladder for round 69 — FAIL 4 at `32c0b50e`/`68faae46`/`10a01ca`, PASS 0 at `7d7d3aee`/`ea20c862`.

## Text to append (verbatim)

```markdown
## Round 69 — post-landing commits and measured outcome (2026-11-03; appended erratum)

The "Round 69 — landing" entry above is one of five commits. The four later commits are tied to
entries here, and that entry's selftest figure is superseded here, not edited there (r69 spot-check
`corpus/lessons/round-69-verifier-spotcheck.md` §6 D6/D7; report `.ufo/reports/round-69/tsukuroi.md`
lines 56-65 name the same five commits).

- `68faae464b60711b0f9ba36169b87e22208ee5ae` — repair after critic K1 A5 (`pending` read `YES` on the
  installed `linux-lts` pair): the derivation became a candidate set (version, every single-dot
  rewrite, `<version>-lts`) with an LTS `pending=NO` case and a `pending=YES` case; selftest
  192 → 194; appended errata in the C1 note, `SKILL.md` and the lesson. Receipt:
  `.ufo/waves/round-69/after/gates-at-final.txt` (internal revision `68faae46`, selftest 194).
- `10a01ca519d5b385c0e47fb9d5b40307bfcf5410` — repair after reviewer R2 HIGH: the census taint input
  is normalized as a bounded decimal (leading zeros stripped, values wider than the closed 0-19 table
  refused before any arithmetic, so `08` no longer aborts and a 25-digit value no longer fabricates an
  all-bits decode); selftest 194 → 196; live line unchanged. Receipt:
  `.ufo/waves/round-69/after/gates-final.txt` (internal revision `10a01ca`, selftest 196).
- `7d7d3aeecacd8633537bf68427a24a02534884f4` — settled wave evidence (13 seat reports,
  `w1-results.json`, attack receipts) and the final gate battery. This is also the landing of the
  receipts the round's own bytes cite: `check-cited-receipts-r62.py --revision 7d7d3aee --round 69`
  reads PASS, 0 findings, 82 files, from `7d7d3aee` on (FAIL, 4 findings at each of `32c0b50e`,
  `68faae46`, `10a01ca5`; the four cited-and-unlanded paths are the wave evidence this commit lands).
  Re-run receipts, full hex and tool hash per revision:
  `.ufo/waves/round-70/probes/E3Repairs/cited-r69-at-claimed.txt` (and `…-at-landing/-repair1/-repair2`).
- `ea20c862f191c77e31c6a357ff7564b5b774acfa` — measured outcome: `SCORECARD.md` "Round 69 — measured
  outcome" (`:5231`), capability row `kernel-arm`, axes restatement, named limits (report lines 64-65).

Selftest figure, corrected (D7): the landing entry above says "selftest 177 → 192 cases"; the round's
final value is **196** (report line 42: "Selftest 192 → 194 → 196"). Ladder: 177 at base `acce353b` → 192 at `32c0b50e` → 194 at `68faae46` →
196 at `10a01ca5` (`196 cases, 196 passed, 0 failed`; `SCORECARD.md:5246`, `:5264`;
`after/gates-final.txt`). The same drift survives in `corpus/lessons/round-69.md:97` ("the census
`KERNEL` arm with 192 selftest cases (177 → 192)"), whose own errata line 134 stops at 192 → 194; a
lesson erratum for the final figure belongs to the r69 lesson's next reader, and is not written by
this entry (never rewrite round-69 bytes).
```

## Checks run against the draft

- The three commits D6 names all appear as full 40-hex in the draft: `68faae46…`, `10a01ca5…`,
  `ea20c862…`, plus `7d7d3aee…` for the receipt landing that D2 needed.
- `196` appears in the block only where the final figure is asserted: the corrected figure, the
  four-rung ladder, the report-line-42 quote and the `PASS (196 cases, 196 passed…)` pointer. The
  string `177 → 192` appears only inside the closing correction paragraph, both times as a quote of
  superseded text (the landing entry's sentence and the lesson line 97).
- No sentence in the draft asserts a figure the receipts do not show. Each rung is a committed file:
  177 at base `acce353b` — the r69 report's before-value for the C2 row (report line 75);
  192 — `.ufo/waves/round-69/after/selftest-at-work.txt` (`PASS (192 cases, 192 passed, 0 failed)`);
  194 — `after/selftest-repair.txt` (`194 cases`) and `after/gates-at-final.txt` (internal rev
  `68faae46`); 196 — `after/selftest-taint-repair.txt` (`196 cases`) and `after/gates-final.txt`
  (internal rev `10a01ca`). `gates-at-work.txt` carries no selftest line at all, which is why the
  draft points at `selftest-at-work.txt` for the 192 rung.
- The fleet-report line numbers cited are from the file as of this read; they are pointers into another
  repository and cannot be verified by the lane's own gates.
