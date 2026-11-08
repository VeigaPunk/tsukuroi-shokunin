# Round 93 lesson — tsukuroi lane

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

Candidates opened 2026-11-08 by the L1 (URL, access date, located quote; ≤25 words each):

| row | URL opened | tier | located quote (≤25 words) |
|---|---|---|---|
| S382 | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/common/lib/config.c | A | "if (p > config_addr) { *(p - 1) = '\0'; }" (raw 328-330, inside `create_menu_tree()`) |
| S383 | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/ChangeLog | A | "Parse the config in linear time. Configs with thousands of entries were slow to load." (raw 8-9) |
| S384 | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/host/limine.c | A | "puts(\"Limine \" LIMINE_VERSION);" (raw 2035; `--version` dispatch raw 2089-2091) |

Admitted: all three, `used-by corpus/knowledge/limine-version-probe-r93.md, corpus/lessons/round-93.md`.
S382 pins the v12.9.5 tag itself (the r92 evidence pinned v12.9.6; the boundary was an inference from
the ChangeLog plus the two files' equality — now measured at the tag). S383 dates the change. S384
sources the V3 probe's input format.

Rejected / refused this round:
- `https://api.github.com/repos/limine-bootloader/limine/git/trees/v12.9.5?recursive=1`: rejected as a
  support row — a directory listing locates S384, it does not state the behaviour; kept as a locator
  in the wave dir only.
- `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/common/lib/misc.c`: rejected as a
  version-print source — the print lives in `host/limine.c` (S384); the file is pinned as a negative
  locator (`grep -c 'Limine '` = 0 on the version path).

Anchor changes logged this round (old → new, no silent rewrite): (a) S377's anchor cell read
the `Python 3.14` docs line; the pinned snapshot and the live page both carry `Python 3.15.2` (the two `3.17`
mentions are inside the `-b`/`-bb` deprecation note, not a page version), so the cell now reads
`Python 3.15.2 docs`; the ≤25-word quote is unchanged. (b) S384's anchor cell said the version print
was at raw 2029 and `--version-only` at raw 2022-2026; ScoutSource re-read the pinned bytes: the print
is raw 2035 (raw 2029 is blank) and the `--version-only` print is raw 2031 — the cell now says so.
The QUALITY-127 sweep receipts are `.ufo/waves/round-93/after/q127-s377-pre.txt` (prints the old S377
cell at the freeze revision) and its landing leg at filing.

Status changes this round: none in place; the rows are new (SOURCES 381 → 385), and S385 is the
appended supersession of S377's locator (a version-pinned URL), per CORPUS rule 2.

Spot-check result: the round-92 spot-check's §6 routed defects are dispositioned in this round's
report (routed 1: the four missing commit rows appear in the r93 Landed-changes table; routed 2:
`ExecLints` runs `check-registry-coverage.py --revision <r93 tip>` and commits the receipt; routed 3:
S377's anchor is corrected by an appended row (S385) rather than a silent rewrite; routed 4:
`claims.json` C2 keeps its frozen literal and the report points at A7 §5; routed 5: the pre-A3
receipts stay labelled as such). This round's own non-author clos is the hyaku closure.

## Mistakes

- **M1 (`landing`, disclosed) — a one-run smoke of the candidate gate ran before the freeze commit.**
  Class: `landing`. The r93 battery was exercised once against the candidate gate (`96/96 met`,
  `.ufo/waves/round-93/after/` was not yet a receipt) during instrument development, before the
  freeze landed at `c633f49a`. Captured-by: the round-93 declaration's own disclosure sentence
  (`SCORECARD.md` "Round 93 — declaration", frozen at `c633f49a`: "the candidate was drafted alongside
  the battery; no score of it is a receipt. The landed gate is committed and scored only after this
  freeze"), QUALITY 114 (`R82-FROZEN-CONTROLS`) and QUALITY 73 (`R28-BATTERY-MEASURE`: a run of
  uncommitted counter bytes is development output) — the lane has no `PROTOCOL.md`; the fleet-root
  file carries no freeze rule (ScribeLesson §4, `git log --all -- PROTOCOL.md` empty). The rule fired
  only as a disclosure because the run left no receipt and every claimed number is from post-freeze
  runs. Fix: the smoke is disclosed in
  the report, the freeze manifest pins the bytes all receipts used, and the lesson records that a
  smoke must be labelled as instrument development in the plan before the freeze. Shown able to fail:
  at the freeze commit the 14-line manifest verifies 14/14 (`w1/ExecReplicate/clone-identity.txt`) and
  the 13-line instrument-only manifest (`before/instruments.sha256`) verifies clean at the landing
  tip; the 14-line file's plan line changes only by this plan's own appended amendments (the r92 A8
  precedent excluded declarations from that manifest — the over-pin is recorded in A2/A4).

- **M2 (`calibration`, self-found by the measured do-nothing leg) — a refusal-shaped control cannot
  certify a refusal family.** Class: `calibration`. The frozen C2 control sentence said the r92 gate
  (which rejects every `auto` value with rc 64) fails all three auto families. Measured
  (`.ufo/waves/round-93/after/c2-donothing-r92-gate.json`): `94/96 unmet`, failed
  `AUTO-ERA-A,AUTO-ERA-B`; `AUTO-PROBE-FAIL` PASSES, because a gate that refuses every `auto` value
  satisfies a family that expects a refusal when the probe fails. Captured-by: none for this shape —
  QUALITY 133 requires both legs for a channel control, not for a refusal control; this round adds
  QUALITY 137. Fix (shown able to fail): the plan's amendment A1 narrows the control sentence and
  names N06 as `AUTO-PROBE-FAIL`'s discriminator; N06 reads `unmet` with the family in
  `failed_families` ×3 (`after/bend-N06-auto-fallback.json`).

- **M3 (`landing`, inherited from the r92 spot-check routed 1) — the r92 report's landed-changes table
  stopped four commits short of its tip.** Class: `landing`. Evidence: `round-92-verifier-spotcheck.md`
  §6 routed 1 (`b5cb636a`, `98185b9b`, `1d1c7439`, `7793773a` unnamed). Captured-by: the report
  contract's "every change tied to … its commit hash" (an existing rule that the r92 wave overtook);
  fix: this round's report table is built from `git log --format` over the freeze range at filing time,
  and the four r92 rows are appended here (reports are never rewritten). Shown able to fail: the r93
  table's hash set equals `git log c633f49a^..<tip>` (one line per commit, checked before filing).

## Routed

- The r92 launcher's residual channels (argv via `/proc/1/cmdline`, host fingerprint via
  `uname`/`/usr`//`/etc`, writable transient gate-copy parent, `/dev` writes; r92 A6) remain
  uncertified; the r93 battery adds a PATH channel for the fake `limine` and names it in its
  docstring. A later round that claims launcher totality must close them or narrow the sentence.
- The probe reads the first `X.Y.Z` of `limine --version`; a pre-release answer (`12.9.6-rc1`) would
  read as `12.9.6` [inference]. A later release-format change is a re-pin of S384.

- **M4 (`curation`, self-found by the wave's ScoutSource) — an SOURCES anchor cited a line window's
  offset instead of the pinned file's line.** Class: `curation`. The S384 row said the version print
  was at raw 2029 and `--version-only` at raw 2022-2026; the pinned bytes put the print at raw 2035
  (raw 2029 is blank) and the `--version-only` print at raw 2031 (2022-2026 is the argv loop). The
  L1 wrote the cell from a memory of a `sed -n '2018,2040p'` window rather than from `nl -ba` on the
  pinned file. Captured-by: the round-82 anchor-coordinate rule (a cited span must be the located
  span) — it existed and could not fire because no gate compares SOURCES anchors to the pinned file;
  the fix is the `nl -ba`-receipt habit, shown able to fail: `after/s384-line-receipt.txt` prints
  `2029` (blank), `2031` (`puts(LIMINE_VERSION)`) and `2035` (`puts("Limine " LIMINE_VERSION)`) and
  the 2089-2091 dispatch, and the corrected cell is in the registry. The row was corrected by a
  logged old→new change, not a rewrite.
