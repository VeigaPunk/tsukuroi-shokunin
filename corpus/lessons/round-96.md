# Round 96 lesson — tsukuroi lane

Integrated by the L1 from the `ScribeLesson` draft (`.ufo/waves/round-96/w1/ScribeLesson/`) and the
wave's attack seats. Pre-round tip `73c47107e8bda79375517ee24ec3c13688586305`; freeze `38adc4ed`.

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

Opened 2026-11-08 by the L1 and the `ScoutSources` seat (URL, access date, located quote ≤25 words).

| row | URL opened | status | tier | located quote | admit / reject |
|---|---|---|---|---|---|
| S390 (new) | https://docs.python.org/3/library/sys.html#sys.int_info.default_max_str_digits | 200, 280632 bytes, sha256 `a7e00587…` | A | "The default value for sys.get_int_max_str_digits() when it is not otherwise explicitly configured." (byte 157653) | **admit** — the configured default of CPython's decimal-conversion limit; it names the value a parser that hands a component to `int()` must bound itself against, and states no Limine behaviour. Pinned page is mutable (Sphinx "Last updated" line): re-verify by title, attribute id and byte offset, never the digest alone. |
| S389 (re-open) | https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation | 200, 815447 bytes, sha256 `6bf2ce2b…` (byte-identical to the r95 pin) | A | "The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits." (byte 785297) | **admit** (re-open; no status/used-by change) — the 4300-digit default the gate's 9-digit component cap sits under; the r95 `mined` row stands. |
| S382-S384 (re-open) | limine v12.9.5/v12.9.6 raw `common/lib/config.c`, `ChangeLog`, `host/limine.c` | 200, sha256 `a940acae…`, `ab280b45…`, `4da21c7c…` | A | unchanged from r93-r95 pins | **admit** (re-open) — the era split, the ChangeLog sentence and the `--version` line the probe parses. |

Rejected this round (opened by the L1; receipts `.ufo/waves/round-96/after/gate/`):

- `https://man.archlinux.org/man/limine.8` → **HTTP 404**, 2706 bytes, title "Page not found — Arch
  manual pages". No such man page; nothing to admit. (Same refusal as r94/r95.)
- `https://api.github.com/repos/Limine-Bootloader/Limine/releases/tags/v12.9.6` → **HTTP 200**,
  26652 bytes, `tag_name` v12.9.6, body 512 bytes pointing at the ChangeLog and the signing key.
  It states no Limine behaviour; a wave-directory locator, never a row.

Census (contract `CORPUS.md`; frozen command
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`):
before `exit 0`, 389 rows (`git show 38adc4ed:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'`);
after `exit 0`, 390 rows, 57 W04 + 1 W01, 0 E findings. Rows added by tier: one A (S390). Rows
touched old→new: none in place (S390 is new; no `status`/`recheck`/`used-by` edit). Frontier rows
advanced: the r95 "four-component shape not sent at battery level" bullet, corrected below.

## Mistakes

- **R96-FRONTIER-NOT-SENT** — class: self-assessment vs bytes. Round 95's README Frontier said the
  `12.9.6.1` extra-component shape was "not sent at battery level", but
  `tools/limine-pin-battery-r96.py` `REFUSAL_VERSIONS` contains `12.9.5.1`, so the refusal class was
  already sampled once. Evidence: `grep -n 'REFUSAL_VERSIONS = ' -A2 tools/limine-pin-battery-r96.py`
  and the r95 bend `N04` receipt (`failed_families ["EXTRA-COMPONENT", "REFUSAL-VERSIONS"]`).
  Captured-by: none (the bullet was not re-derived before the freeze). Fix: the r96 declaration
  records the class as broadened, and this row is the correction; a frontier sentence is now
  re-derived against the instrument before it is published.
- **R96-N04-TWO-FAMILIES** — class: frozen target vs instrument reading. The first draft of C1's
  kill rule said the N04 bend fails "the new family"; a development run showed
  `failed_families ["EXTRA-COMPONENT", "REFUSAL-VERSIONS"]` because the pre-existing row also covers
  a four-component value. Evidence: `.ufo/waves/round-96/before/dev/N04-extra-components.json`.
  Captured-by: QUALITY 140 (a target clause re-read against one development run before the freeze).
  Fix: the frozen target states the two-family set, and the claim records the class as broadened.
- **R96-REPORT-WORD-COUNT** (carried from r95 routed 1) — class: report prose vs committed ledger.
  Round 95's report wrote "four `falsifies-wording` rows" where the ledger held six. Captured-by:
  none in r95; r96's C2 F6 makes the sentence machine-checkable. Fix: the r96 report states the
  numeral the checker compares, and `check-r96-calibration.py --report` is run before filing.

## Counter-attack scoreboard (considerthese/2026-10-26.md, mined 2026-11-08)

The proposal "counter-attack scoreboard … track how many attack arms the wave fielded, how many
survived, and which class beat it" is implemented here for the round's counters (its first
unimplemented item that fits this round's claims): C1 fielded four one-clause bends plus the
`MutBound` mutant set; killed/failed families and survivors are recorded in the report's C1 rows, so
the next round can compare convergence instead of re-reading receipts. No code was added for this;
the table is the implementation.

## Relation to the r95 freeze manifest (r95 routed 4)

The r95 freeze manifest pins the `b8f878c8` bytes. Round 96 edits only the two r95 tools' docstrings
(wording, not code), so `sha256sum -c .ufo/waves/round-95/before/instruments.sha256` no longer holds
in the working tree; the pinned bytes are re-derivable with `git show b8f878c8:<path> | sha256sum`,
and the r96 append-only rows record the correction rather than rewriting the historic manifest.

## Routed

- r95 routed 1 (report prose count): closed by C2 F6 for r96; the r95 filed bytes stay as they are.
- r95 routed 2 (`QUALITY.md` owes M1 a criterion): closed — QUALITY 140 cites `round-95.md` M1.
- r95 routed 3 (dead void pointer): closed — the receipt + SCORECARD binding (F2).
- r95 routed 4 (superseded superlative in the frozen tool docstrings): closed — both tools corrected,
  relation to the r95 manifest stated above.
- r95 routed 5 (README over-scope): closed — the sentence is scoped to the r94 family roster (F4).
- r95 routed 6 (derived, not measured, C2 revisions): closed — a tip PASS receipt at `b8f878c8` (F5).
- r95 routed 7 (carried Frontier rows): still open, except the four-component entry corrected here;
  the r92 launcher residuals, the r93 probe pre-release caveat and r89's blanks/ESP/empty labels stay
  Frontier.
