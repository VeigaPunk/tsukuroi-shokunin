# Round 72 — lesson (tsukuroi, hyaku run 15, attempt 1)

author: tsukuroi L1 (round 72), integrating the wave `.ufo/waves/round-72/` (12 seats, one v1 wave).
basis: declaration `6b4267623b3d6cf88b32c2df8daaad1a5bc9f19e` (frozen before data; base `a7015d27`);
pre-data receipts in `.ufo/waves/round-72/before/`; measured revision `123e1c5767265e58bb5c9bf850bd0172bdd31c16`.

## Gate

**Trigger and sources.** Three kmod **v34** snapshots were fetched before the declaration text and
committed byte-exact under `.ufo/waves/round-72/before/src/` with `SHA256SUMS` (3/3 OK) and
`SOURCES.json`. The host runs kmod **34.2** (`modprobe --version`); S1Scout re-fetched all three by a
second route (`raw.githubusercontent.com/kmod-project/kmod/v34/…`), read `ROUTE2_OK=3/3`, byte-identical,
and measured the v34→v34.2 delta: `modprobe.d.5.scd` and `modprobe.c` unchanged, `libkmod-config.c`
differs in one weak-dependency sizing hunk at v34 line 574 (later lines shift +2); both S302 quotes
survive verbatim. Access date **2026-11-03**.

| id | snapshot | URL (tag v34) | sha256 | rows |
|---|---|---|---|---|
| **S301** | `man/modprobe.d.5.scd` | `https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git/plain/man/modprobe.d.5.scd?h=v34` | `aa1a869e…ee46e` | MD1, MD2 |
| **S302** | `libkmod/libkmod-config.c` | `…/libkmod/libkmod-config.c?h=v34` | `ae520a07…ceb11` | MD3, MD4 |
| **S303** | `tools/modprobe.c` | `…/tools/modprobe.c?h=v34` | `1e8e3526…1bf3f` | MD5, MD6 |

Gate quotes (each ≤ 25 words, located in its snapshot): S301 `modprobe.d.5.scd:43-44` "Once a file of a
given filename is loaded, any file of the same name in subsequent directories is ignored." and `:46-47`
"All configuration files are sorted in lexicographic order, regardless of the directory they reside in.";
S302 `libkmod-config.c:942` "Ignoring duplicate config file: %s/%s\n" and `:1083`
"kmod_config_parse_kcmdline(config);"; S303 `modprobe.c:128` "Do not execute operations, just print out"
and `:111` "Apply blacklist to resolved alias."

**Admitted.** Three rows, all tier A `mined`: S301 (docs), S302 (code), S303 (code), cited by
`corpus/knowledge/modprobe-config-plane-r72.md` (MD1-MD6). At the measured revision `123e1c57` the frozen
counter reads `MD_ROWS=6 MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0`, `met=1`, rc 0; the
registry reads 303 rows and all three new rows are `NF=13`.

**Rejected / refused.** No candidate was refused this round. The round-71 lead was closed rather than
rejected: the kmod man page exists at `man/modprobe.d.5.scd` (HTTP 200) and is S301; the r71 attempt's
404 was the guessed `man/modprobe.d.xml` path, not the source's absence. One read-only fetch of
`libkmod/libkmod.c` (sha256 `a3899a59…`) located the compiled `default_config_paths` array for the
lead line; it grounds no row and no rule statement, so it is a lead, not an admission.

**Non-author spot-check.** The round-71 closure's spot-check is on record
(`corpus/lessons/round-71-verifier-spotcheck.md`); the round-72 spot-check is OWED to the closure judge,
which re-opens the three URLs live and records its admit/reject agreement. No author-side `[x]` is written.

**Census.** Round start (declaration receipt): canonical validate rc 0, **300** registry rows, **89**
knowledge `.md` notes. Round end at `123e1c57`: rc 0, **303 rows, 90 notes** (W04 duplicate-URL warnings
only).

## Mistakes

- **R72-C2-FIXTURELESS** — class `declared predicate met by an in-memory imitation` · evidence: the L1's
  first `--selftest` created a temp root but wrote **0** fixture files (`write_text` count 0); the cases
  scored in-memory strings, so "builds every fixture under `$TMPDIR`" was false (`E2GateSelftest` report,
  delta item 1) · captured-by: `E2GateSelftest` · fix: adopt its patch — each case's receipt/diff is
  written to files under one `$TMPDIR` root and read back through `score_files()`; the nine-case suite
  passes and the red-before mutant fails `SELFTEST-MISMATCH` and `SELFTEST-MIXED`
  (`before/control/selftest-redbefore.txt`).
- **R72-C3-UNANCHORED-BLOCK** — class `instrument false negative after the declaration quotes its own
  target` · evidence: the checker's erratum regex had no `^` anchor, so it matched the Round-72
  declaration's inline quotation of the heading and stopped at the next line-initial `##`; an erratum
  appended at EOF was invisible (`E3Routed` tamper probe 2, `FALSE_PASSES=5`) · captured-by: `E3Routed` ·
  fix: line-anchor the heading (`^## … ` with `re.M`); the live EOF block now reads `ROUTED_SCORECARD ok`
  (`probes/L1C3/probes.txt`).
- **R72-C3-REVISION-TEXT** — class `receipt provenance unchecked` · evidence: a receipt whose summary
  lines were copied but whose revision text was fabricated read `ROUTED_STALE=0` (`E3Routed` probe (i)) ·
  captured-by: `E3Routed` · fix: the receipt must name the record revision `2b358d2d` in its own text;
  a receipt with every occurrence removed now reads `missing revision token` and rc 1.
- **R72-C3-TOKEN-LIST** — class `predicate conjunct met by a token list instead of the named set` ·
  evidence: the checker required the strings `five`, `four` and the directory, not the five filenames, so
  a note reading only `R71-NOTE-MODPROBE-COUNT five four /usr/lib/modprobe.d` read `ROUTED_STALE=0`
  (`R2Reviewer` high finding) · captured-by: `R2Reviewer` · fix: the correction section must enumerate
  `README`, `bluetooth-usb.conf`, `gsr-nvidia.conf`, `nvidia-utils.conf`, `systemd.conf`; the token-list
  note now reads `ROUTED_NOTE missing: README … systemd.conf` (`probes/L1C3/probes.txt`).
- **R72-C3-FALSE-FAIL-HEADING** — class `instrument rejects a correct repair on a cosmetic choice` ·
  evidence: `## Erratum` or a capital `Five` in an otherwise correct correction read `ROUTED_STALE=1`
  (`R2Reviewer` medium) · captured-by: `R2Reviewer` · fix: the section heading match is
  `correction|erratum` (case-insensitive) and the words `five`/`four` match case-insensitively; the pair
  now reads rc 0.
- **R72-C3-DENIAL-LIMIT** — class `semantic closure not proved` · evidence: an erratum block that names
  the receipt and revision while explicitly denying the repair still reads `ROUTED_STALE=0`
  (`R2Reviewer` medium) · captured-by: `R2Reviewer` · fix: recorded as a named limit, not repaired — the
  checker verifies naming, not entailment; the correction's substance rests on the non-author review and
  the closure judge.
- **R72-S302-LINE-ANCHORS** — class `upstream line pin read as a host-build line` (QUALITY 103) ·
  evidence: the host runs kmod 34.2 while the snapshot is v34; `libkmod-config.c` shifts +2 after its one
  changed hunk, so a host-side reading of the v34 line numbers would be wrong · captured-by: `S1Scout`
  route-2 re-open · fix: S302's anchor cell states the anchors are v34 anchors, not host-build lines, and
  names the delta hunk; the quotes were located by text, never by line.
- **R72-SKILL-ROW-OVERWRITE** — class `append-only slip` · evidence: the first landing edit replaced the
  r71 `selftest-tally` row instead of adding the round-72 continuation row; a `grep` of the count of that
  row caught it before the commit · captured-by: the L1's own pre-commit grep · fix: the r71 row was
  restored byte-exact and the continuation row carries the nine-case text; every modified prose file
  shows 0 removals against the base.
- **R72-DECL-UNRECEIPTED-TARGET** — class `pre-data receipt exists, post-data figure moves` · evidence:
  the declaration's C2 target is `N >= 7`; the adopted patch's suite is 9 cases, and the SKILL
  continuation row initially carried the seat's "seven" figure from the earlier instrument · captured-by:
  the L1's tally sweep · fix: the row now carries 9 and the sweep reads `added_figures_mismatched=0`
  against the after receipt.

Not Mistake rows: the two inherited untracked dispatcher markers
(`.ufo/waves/round-66|67/w1.ready.dispatched`) and the open L0 questions (`tsukuroi | round-64`,
`round-60`, `round-57`) are operator/closure items, routed around rather than answered.

## Considerthese

No proposal is mined this round; the measured status of the five proposals in the latest file
(`considerthese/2026-10-26.md`) is unchanged from the r71 record, each verified by grep rather than
restated: "Counter-attack scoreboard" is the standing SKILL ledger continued below; "Seat-harm incident
log" is the per-round tally below; "Burst-aware reading" stays a one-round mining record (r46), not a
gate; "Cross-note correction propagation map" is recorded partial (r43/r54) and does not clear this
round's bar; "Downstream patch-offset check" was adopted at round 69 as QUALITY 103 and is exercised this
round by the S302 anchor note (R72-S302-LINE-ANCHORS).

### Counter-attack scoreboard — round 72 (continuation of the r64 ledger)

| Counter | Round / arm source | Arms fielded (receipts) | Survivors | Class that beat it |
|---|---|---|---|---|
| `count-md-rows-r72.py` (C1) | r72 pre-data battery (`before/control/battery.txt`) | 11 cases: 1 control + 10 mutants | 0 (control met=1, ten mutants met=0) | the frozen clauses fired; the own-work-kind clause is new this round |
| `count-md-rows-r72.py` (C1) | r72 wave `w1/E1Mirror/` | independent reader + case matrix | OWED | E1Mirror's report is the seat's own matrix; the L1 did not re-run it |
| `check-r71-routed-r72.py` (C3) | r72 pre-data battery (`before/control/routed-battery.txt`) | 5 cases (1 green + 4 mutants) | 0 | control rc 0, four mutants rc 1 |
| `check-r71-routed-r72.py` (C3) | r72 wave `w1/E3Routed/tamper-probes.txt` | receipt tamper, fabricated revision, missing/duplicate erratum, correction variants | 2 (unanchored block, fabricated revision) | declaration self-quote; unchecked receipt provenance; both repaired in-round (`probes/L1C3/`) |
| `check-r71-routed-r72.py` (C3) | r72 wave `w1/R2Reviewer/findings.md` + `probes/L1C3/probes.txt` | token-list correction, cosmetic heading/case, denial block, `Five` | 1 (a denying block passes) | semantic closure is not a lexical check; recorded as a limit |
| `check-selftest-tally.py --selftest` (C2) | r72 wave `w1/E2GateSelftest/redbefore.txt` | 9-mutant matrix over the selftest | 0 after adoption | the suite notices each removed arm; the first L1 version was fixtureless (R72-C2-FIXTURELESS) |
| `check-selftest-tally.py` (C2) | r72 wave `w1/E2GateSelftest/selftest-after.txt` | `/tmp` audit + r70 self-demo | 0 | `tmp_leak_under_slash_tmp=0`; self-demo verdict unchanged |

## Trend verdicts

- **expansion: improved.** Three admitted registry rows (S301-S303, tier A `mined`) on ground the lane
  never held — the declaration's held-ground sweep read 0 file hits for `softdep`, `MODPROBE_OPTIONS`,
  `showconfig`, `APPLY_BLACKLIST`, `conf_files_insert_sorted` and `lexicographic` under
  `corpus/knowledge`, and no note named the configuration surface; one admitted entry (MD1-MD6) cites
  them; registry 300 → 303 and notes 89 → 90. No capability row enters this round: C2 is scored as an
  operability repair to an existing gate, not a new repertoire row.
- **quality: improved.** The r71 closure's routed statement/receipt defects close in committed bytes
  (`ROUTED_STALE=3` → `0`); the S302 anchor now states the upstream/host-build line split
  (QUALITY 103); the `selftest-tally` gate gains nine hermetic cases with a suite shown able to fail; the
  C3 checker's two attack-found defects are repaired with before/after probes.
- **discernment: unchanged (author-side).** The wave caught two of the lane's own instrument defects
  (fixtureless selftest, unanchored block) plus the unchecked receipt revision, and the SKILL row slip
  was caught before landing; the outside non-author admit/reject spot-check is owed by the closure judge
  and no author-side `[x]` is claimed.

## Seat-harm tally (standing per-round tally, r66 adoption continued)

Round 72: OWED — the sentinel seat did not land; the L1's own boundary check is the misroot sweep at
report time. Running tally since r66: 0, 0, 0, 0, 1, 0, (r72 pending).
