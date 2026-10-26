VERDICT: defect-found

# R-2 — cheap tables against the frozen C2 counter (`tools/check-hook-order-r38.py`, sha256 `60e3635b…`)

Two of twelve cheap tables PASS the frozen C2 counter, including one whose entry cites only the
own-work capture `S212` and contains **zero** rule rows (no HO1–HO7, no libalpm citation):
`rows_expected 69, rows_matched 69, mismatches 0, extra_rows 0, source_ok 1, result PASS, exit 0`
(`.ufo/waves/round-38/w1/CritControlsC2/stripC-dedup-etcfirst-srcS212.json`, revision `d476293`).
The counter therefore measures **table equality plus registry shape**, not the declared "depth
(sourced) … read from libalpm `hook.c`" (SCORECARD.md:2118). This does not by itself defeat C2 —
the pre-seat per-row HO kill rule (SCORECARD.md:2158-2161) would still require seven verdicts this
entry cannot supply — but it falsifies the amendment's stated reason for why the correct-table
control passes, and it shows the v1 counter is as fixture-gated as C1 was before QUALITY 82.

## Fixture discipline

- Scratch clone: `/fast/scratch/hyaku/tsukuroi-r38/CritControlsC2/fx.MYCAPc`, created at lane tip
  `5edb6c2` with `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D"`,
  `git -C "$D" remote remove origin`, `rev-parse --show-toplevel` == `$D`.
- Fabricated registry row `S999` (status `mined`, opened `2026-10-26`, used-by
  `corpus/knowledge/pacman-hook-order-r38.md`, evidence cells literally say "fabricated in scratch"
  / "must never appear in the lane") inserted into the clone's `corpus/SOURCES.md` only
  (commit `e109dd5`), so table scoring is isolated from the real provenance rows.
- Each control is one commit on the clone's `master`; the counter is run per revision
  `python3 tools/check-hook-order-r38.py --repo "$D" --revision <sha>` (bind accepts each sha as an
  ancestor of `master`; no origin ref). Map in `CritControlsC2/clone-control-log.txt`.
- Lane content never written; no git/jj mutation outside the scratch clone; no host change; no
  packages installed. Scratch dir removed after receipts were copied into the seat dir.

## Scores (all observed; per-control JSON in `CritControlsC2/`)

| control (table-only change) | matched | mism | extra | src_ok | result |
|---|---|---|---|---|---|
| baseline: real entry + fabricated S999 row (harness sanity) | 69/69 | 0 | 0 | 1 | **PASS** |
| `ls` order per dir, `/etc` appended (`lsdir-usr-then-etc`) | 43/69 | 26 | 27 | 1 | FAIL |
| same, dedupe keeping usr (`lsdir-dedup-usrfirst`) | 44/69 | 25 | 25 | 1 | FAIL |
| same, dedupe keeping etc (`lsdir-dedup-etcfirst`) | 41/69 | 28 | 28 | 1 | FAIL |
| global full-name byte sort, both dirs kept (`dup-bytefull-global`) | 42/69 | 27 | 28 | 1 | FAIL |
| global full-name byte sort, dedup (`dedup-bytefull-global`) | 63/69 | 6 | 6 | 1 | FAIL |
| global `LC_ALL=en_US.UTF-8` full-name sort, dedup (`dedup-enUSfull-global`) | 60/69 | 9 | 9 | 1 | FAIL |
| capture `MANIFEST.sha256` line order, dedup (`manifest-line-order`) | 17/69 | 52 | 52 | 1 | FAIL |
| `pacman.log` `running '…'` first-seen order, 49 rows (`pacmanlog-firstseen`) | 1/69 | 68 | 48 | 1 | FAIL |
| suffix-stripped C sort, dedup **keeping usr** (`stripC-dedup-usrfirst`) | 68/69 | 1 | 1 | 1 | FAIL |
| suffix-stripped `en_US` sort, dedup keeping etc (`stripC-enUS-dedup-etcfirst`) | 66/69 | 3 | 3 | 1 | FAIL |
| suffix-stripped C sort, dedup keeping etc, cite fabricated `S999` (`stripC-dedup-etcfirst`) | 69/69 | 0 | 0 | 1 | **PASS** |
| same, cite only real own-work `S212` (`stripC-dedup-etcfirst-srcS212`) | 69/69 | 0 | 0 | 1 | **PASS** |

Mismatch shapes are the expected ones: the full-name sorts miss exactly the three `-32`/base pairs
(`fontconfig`, `gio-querymodules`, `gio-remove-module-cache`, `dedup-bytefull-global.json:missing_rows_first5`);
`en_US` additionally swaps the `gtk-query-immodules-3.0`/`gtk-update-icon-cache`/`gtk4-querymodules`
block (3 more, `stripC-enUS-dedup-etcfirst.json`); per-directory `ls` order loses 26–28 rows to the
`etc` interleave; `pacman.log` gives only 49 of 69 candidates and almost nothing in the right place.

## Why the passing table is cheap (no source reading, no rule text)

1. **Order.** The ALPM order is exactly `basename .hook` + `LC_ALL=C sort` over the two capture
   directories: `ORDER_IDENTICAL`, 69 names (`CritControlsC2/order-equivalence.txt`; real entry order
   extracted from `corpus/knowledge/pacman-hook-order-r38.md`, naive order from
   `.ufo/waves/round-38/frozen/hooks-capture/`). No `strncmp`/tie-break knowledge is needed — the
   suffix strip is what `basename` does anyway, and bytewise sort then agrees with
   `_alpm_hook_cmp` on all 69 names.
2. **The one override bit.** Deduping the single same-name pair in `/etc`-first order is the only
   choice left; `stripC-dedup-usrfirst` (68/69, the one row
   `PostTransaction | 26 | 90-mkinitcpio-install.hook | usr`) shows that choosing the other file is
   the only failure mode. The `etc` file wins by listing `/etc` first and keeping the first sighting,
   or by reading the lane's own round-19 note (`corpus/knowledge/boot-writers-r19.md:36-37`, cited by
   the entry's HO2 row) — a one-grep lane read, not libalpm.
3. **Attributes.** `when/abort/needs/exec` are `grep`s of the hook files themselves; the counter parses
   the same keys (`tools/check-hook-order-r38.py:73-97`). Zero triggerless files exist, so HO3's mask
   rule is not even exercised (entry states 0 masks).
4. **Provenance.** `source_check` only demands: every cited S-id exists, status `mined`, its used-by
   names the entry, and at least one cited row is dated `2026-10-26`
   (`tools/check-hook-order-r38.py:157-181`, checks at :174/:175/:177). The evidence cells are never
   examined. Hence (a) a self-declared fabricated row passes (`stripC-dedup-etcfirst.json`,
   `source_ids ['S999']`, `source_problems []`), and (b) citing only the own-work capture `S212`
   passes (`stripC-dedup-etcfirst-srcS212.json`, `source_ids ['S212']`, PASS) — no `hook.c`,
   `trans.c`, `alpm.c` or manual row is required, although the claim is "sourced … read from libalpm
   `hook.c`" (SCORECARD.md:2118).

## Defects

D1 (counter scope, C2): the predicate at `tools/check-hook-order-r38.py:205`
(`matched == len(exp) and not mism and not extra and dups == 0 and src_ok == 1`) has no conjunct
over the entry's rule text or its source-line composition. The entry may contain no HO row at all
and PASS (passing receipt above; the passing entry is `CritControlsC2/passing-entry-srcS212.md`,
`grep -c 'HO[1-7]'` → 0). The declared "sourced depth" is not measured.

D2 (provenance shape-only): `source_check` accepts a registry row whose own evidence text disclaims
it. Smallest demonstration: `S999` with evidence "n/a — fabricated in scratch" and finding
"fabricated row, must never appear in the lane" still yields `source_ok 1` (clone commit `e109dd5`
+ control `c4f092b`).

D3 (rationale falsified): SCORECARD.md:2157-2158 says "the correct-table control PASSes because the
table is rule-derived, so the table conjunct measures the order rule, not reading." The table is
**fixture-derived**: it is reproduced exactly by `basename` + `LC_ALL=C sort` + first-sighting
dedupe over the frozen capture, with a `source:` line naming only `S212`. The conjunct measures
table equality, not the order rule.

Not a defect: the failing controls confirm the counter does discriminate anything that changes a
row (wrong pair order, wrong dir tag, non-interleaved dirs, log order). The counter is a faithful
table-equality check; the defect is that the claim and the amendment read more into it.

## Impacted axes

- C2 depth (primary): the counter's PASS is reproducible without reading; depth evidence must rest
  on the per-row HO1–HO7 verdict seats, and on the composition of the `source:` line, not on this
  counter.
- Provenance/`source_ok`: any entry can satisfy it with one fabricated or single-capture row.
- Not impacted: C1 (untouched), adjacency, and the actual entry — I read the real entry: it does
  carry 7 rule rows (`grep -c '^| HO[1-7] |'` → 7) and cites S208–S212 on the `source:` line
  (`corpus/knowledge/pacman-hook-order-r38.md:1`), so *this* revision is not the cheap control; the
  counter just cannot tell.

## Smallest safe correction

1. **Text (no predicate change; amendment stays tightening-only).** Replace SCORECARD.md:2157-2158
   ("the correct-table control PASSes because the table is rule-derived, so the table conjunct
   measures the order rule, not reading.") with:

   > sort table (63/69, FAIL, `controls.jsonl`); a correct-table control PASSes because the counter
   > compares the table to the frozen capture. The table is reproducible from that capture without
   > reading libalpm — `basename .hook` + `LC_ALL=C sort` reproduces the 69-name order exactly, and
   > a `source:` line naming only the own-work `S212` satisfies `source_ok` — so the table conjunct
   > measures table equality, not rule reading. Depth rests on the per-row HO1–HO7 verdicts, which
   > must be judged **against the entry's rule rows**, and the entry must be rejected if any of the
   > seven rows is absent or its cited `file:line` does not resolve in the pinned snapshot.

2. **Optional C2 analogue of the C1 QUALITY-82 counter** (same pre-seat pattern): add
   `tools/check-hook-order-r38-q82.py` returning `rules_ok` with the conjunct
   `rows_ok == 1 and rules_ok == 1`, where `rules_ok` requires: exactly one `| HO<n> |` row for each
   n∈1..7 inside the entry's rules section; each row cites at least one `Sxxx` in {S208,S209,S210,
   S211} plus a `file:line[-line]` anchor that resolves inside `.ufo/waves/round-38/sources/` at the
   snapshot whose sha256 is recorded in `sources/SHA256SUMS`; the `source:` line cites S208–S212 with
   no unknown id. Controls I can already score against it: `stripC-dedup-etcfirst` 0/1 FAIL,
   `stripC-dedup-etcfirst-srcS212` 0/1 FAIL, real entry (7 HO rows, S208–S212) 1/1 PASS. If the wave
   will not add a counter mid-round, the existing kill rule covers the case only if the verdict seats
   are instructed to fail an entry that lacks the seven rule rows (a seat can currently emit seven
   "holds" lines from the source while judging nothing in the entry).

## Receipts

- `.ufo/waves/round-38/w1/CritControlsC2/scores-summary.txt` (14 observed counter runs),
  `baseline-real-entry.json`, each `<control>.json`, `passing-entry-srcS212.md`,
  `order-equivalence.txt`, `clone-control-log.txt` (base `5edb6c2` … pass `d476293`),
  `counter-sha256.txt` (`60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`),
  `gen2.py`, `gen3.py`.
- Frozen counter anchors: `tools/check-hook-order-r38.py:48-50` (capture/dirs), `:99-124`
  (`expected_rows`), `:141-155` (`entry_rows`), `:157-181` (`source_check`), `:205` (predicate).
- Scratch `/fast/scratch/hyaku/tsukuroi-r38/CritControlsC2/` removed after the copy above.

## Not done

- I did not test the pinned-source line anchors of the real HO rows (out of scope; C2RevHookC /
  C2RevOtherSrc / C2CritHO5 / C2CritHO6 / C2RevenConf own that).
- I did not test a live-directory (non-capture) derivation; irrelevant to this counter, which reads
  the capture only, and the host is not to be touched.
- No tools installed or upgraded; no package, service, sysfs, hook or `/etc` change; no sudo.
