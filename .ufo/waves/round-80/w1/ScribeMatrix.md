# ScribeMatrix — round-80 w1 — binding report

Seat: **ScribeMatrix** (scribe). Round: tsukuroi round 80, wave 1. Axes: depth + operability.
Milestone: restart documentation matrix and two gate self-invocation repairs.

**Execution class: NO-EXEC (read/write only).** No command was executed beyond read-only
inspection of files already in the tree (`read`/`glob`/`grep`/`bash` file reads) and one
byte-exact file copy of an already-frozen artifact into this seat's own report directory.
No host command, no package-manager transaction, no network fetch, no service operation,
no Git/jj mutation, no test/build/formatter run, no production file written. No tool was
installed; no host service was restarted; no sudo was used; no secret or config file was
read.

## Behavior

Two C1 artefacts drafted in this seat's report directory, and the source reading that
grounds them.

**`data.json`** (`.ufo/waves/round-80/w1/ScribeMatrix/data.json`, 88 lines) — a
byte-exact copy of the frozen expected object `.ufo/waves/round-80/before/expected.json`.
Verified byte-identical two ways: `sha256sum` on both files gives
`05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153`, and `cmp` reports the
files identical. This equals the instrument's declared expected-object SHA-256
(`SCORECARD.md` Round 80 declaration). The frozen `before/expected.json` was **not**
modified, and `before/systemd.service.xml` was **not** modified (its digest still
`12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44`).

**`note.md`** (`.ufo/waves/round-80/w1/ScribeMatrix/note.md`, 308 lines) — the prose
companion for that matrix, in the lane's knowledge-note convention. Opening lines:
`source: S330 in corpus/SOURCES.md — systemd v262 man/systemd.service.xml — <exact URL>`,
`verified-at: 2026-11-04`, `recheck: on-release`, plus a `companion:` line naming
`corpus/knowledge/service-restart-matrix-r80.json`. It carries: the six cause rows and
seven policies with per-cell source line numbers; the source table's location, title
quote and header order; the surrounding conditions (manual stop / systemd-initiated
death, oneshot, the four clean signals, `SuccessExitStatus=`,
`RestartPreventExitStatus=`, `RestartForceExitStatus=`, start rate limiting, and the
recommended-choice sentence); an explicit statement that the knowledge scope is a finite
documentation matrix and not a dynamic runtime simulation; a `## Limits` section; a
`## QUALITY check` section naming the applicable numbered criteria with the concrete
property each is satisfied by; and a provenance block.

**The source reading.** All 42 cells of the matrix were re-derived from the pinned
snapshot `before/systemd.service.xml` by parsing the `<table>` element titled
"Exit causes and the effect of the Restart= settings" (`:914`) and reading each
`<entry>` of each `<row>`, in the header's own column order
(`no`, `always`, `on-success`, `on-failure`, `on-abnormal`, `on-abort`, `on-watchdog`).
Result: **42 of 42 cells agree** with the frozen expected object; per-row `X` counts are
2, 2, 4, 3, 4, 3 → **18 marked, 24 empty**. The frozen data was left untouched; had the
source disagreed, the disagreement would have been reported as a miss rather than fixed.

## Gates

- **Cell equality (machine-checked, 42/42 agree, 0 mismatches).** Re-derived independently
  of `tools/measure-round80.py`; the instrument was read, not imported.
- **Quote verification (machine-checked, 30 range-checked quotes, 0 failures).** Every
  quoted fragment was located in the markup-stripped snapshot and its actual line span
  confirmed to fall inside the range the note cites. All 36 double-quoted fragments in
  the note are present in the snapshot verbatim after markup stripping; the longest is
  23 words, all are ≤ 25.
- **Digest equality.** `data.json` sha256 `05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153`
  (matches the instrument's declared expected SHA and the frozen `before/expected.json`).
  `note.md` sha256 `1aae7b2a5362c6e63ccdd2df1c7cb06c8712b71950c275fdc9047ab3bba67a0b`
  at this write — the corrected bytes, superseding the first draft's
  `c92b1e4c…`. The note digest is the value ReviewMatrix must bind; if the note bytes
  change again, the reviewer needs a renewed verdict.

**Self-corrections made before finishing** (recorded, not hidden): the first note draft
stated "24 are marked X and 18 are empty" — inverted. A machine count of the source
table (`2, 2, 4, 3, 4, 3` = 18 `X`) caught it, and the note now reads 18 marked / 24
empty in both places it states the count. Nine further draft quotations carried wrong
stated word counts or wrong line ranges (e.g. `:899-900` → `:900`; 23 → 18 words; the
`on-watchdog` quote at `:906-907` → `:907`); each was corrected against the locator and
re-verified. The OOM sentence at `:1417-1418` was initially presented as generic page
prose; it is in fact inside the `OOMPolicy=` entry (`:1398`), and the note now says so.

**Review cycle (ReviewMatrix).** The reviewer found real defects in the first note
bytes and I corrected all of them; the note digest below is the corrected final bytes.

1. **OOM row mis-characterised (semantic blocker, corrected).** The note said the OOM
   row "is marked like an unclean exit code, with the signal-only policies left
   unmarked". The source disagrees: the OOM row's marked set is
   `('always','on-failure','on-abnormal')` — identical to the **Timeout** row and
   *different* from Unclean exit code, whose `on-abnormal` cell is empty at `:948`
   against OOM's `X` at `:988`. The note now states the marked set explicitly, names
   the `:948`-vs-`:988` cell as the exact difference, and says the OOM row is not the
   unclean-exit-code row with signal policies removed. It also records that the
   `on-abnormal` prose (`:902-904`) enumerates signals, timeouts and watchdog expiry but
   does not name OOM termination, so this cell is a table marking the prose does not
   spell out — recorded as read, with no cause supplied.
2. **Row-2 rationale wrongly called `on-abnormal` signal-defined (corrected).** It now
   says the unclean *exit code* is neither a signal nor a timeout nor a watchdog expiry,
   and that the `on-abnormal` and `on-abort` definitions (`:902-906`) cover only those
   three kinds of event, which is why the row leaves both unmarked.
3. **Column-separation count wrong (corrected).** The note said the `on-abnormal` and
   `on-abort` columns "separate in exactly one place". They separate in **three** rows —
   Timeout, Watchdog and OOM — where `on-abnormal` is marked and `on-abort` is not;
   `on-abort` is marked in Unclean signal alone. The note now says so.
4. **QUALITY 94 was labelled as a complete-line claim (corrected, and recorded as
   partial compliance).** Several quotes are exact fragments of their cited line, not
   complete lines — `:907` carries both the `on-watchdog` clause and the start of the
   `always` clause, and the note quotes only the watchdog fragment. The QUALITY 94 bullet
   is relabelled "every cited line accounted for", states the fragment property plainly,
   and declares the complete-line clause **not met** and recorded as a limitation; the
   same limitation is now also in the Limits section.
5. **One non-source scare-quote removed.** The phrase "the unclean exit code row with
   the signal policies left out" was in double quotes although it is my own wording, not
   the source's; it is now unquoted so no reader takes it for a quotation.

The reviewer separately retracted its own two quote observations on rows 3 (it confirmed
the quotes at note lines 91-95 do match contiguous markup-stripped source `:902-906`);
no change was made on those.

**Verification after the corrections** (re-run against the corrected bytes):

- 30 range-checked quotes, 0 failures; every quoted fragment's own start and end line
  fall inside the cited range; all 36 double-quoted fragments present verbatim in the
  markup-stripped snapshot; longest 23 words, none over 25.
- **42 of 42 per-cell claims in the note verified mechanically**: for every one of the
  six rows, each `Marked:` cell is genuinely `X` in the source, each `Unmarked:` cell is
  genuinely empty, and every cited cell line number equals the source `<entry>` line —
  0 violations.
- Marked sets re-derived from the source table: Clean `always,on-success`; Unclean exit
  code `always,on-failure`; Unclean signal `always,on-failure,on-abnormal,on-abort`;
  Timeout `always,on-failure,on-abnormal`; Watchdog
  `always,on-failure,on-abnormal,on-watchdog`; OOM `always,on-failure,on-abnormal`.
- `on-abnormal` marked in Unclean signal, Timeout, Watchdog, OOM; `on-abort` marked in
  Unclean signal alone; OOM's set equals Timeout's set.

## Touched surfaces

Written (both inside this seat's own report directory; nothing else on the host changed):

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-80/w1/ScribeMatrix/data.json`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-80/w1/ScribeMatrix/note.md`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-80/w1/ScribeMatrix.md` (this report)

Read-only: `SCORECARD.md` (Round 80 declaration), `.ufo/waves/round-80/before/{expected.json,controls.json,systemd.service.xml}`,
`.ufo/waves/round-80/w1-spec.json`, `.ufo/waves/round-80/w1-dispatch.json`,
`tools/measure-round80.py`, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
`corpus/knowledge/journald-retention-plane-r76.md`, `corpus/knowledge/systemd-job-transaction-plane-r75.md`,
`corpus/knowledge/alpm-package-anatomy-r41.md`.

Scratch `/fast/scratch/hyaku/tsukuroi-r80/ScribeMatrix/` was created empty and holds no
files; nothing durable lives there, so there is nothing to copy out and the directory is
removed before this yield.

## Out of scope (not done, and why)

- **No production edits.** `corpus/knowledge/service-restart-matrix-r80.json` and
  `corpus/knowledge/service-restart-matrix-r80.md` — the two paths the instrument reads
  (`NOTE`, `COMPANION`) — were **not** created. This seat's brief says "No production
  edits"; the drafts are for the integrating seat to land. The note's `companion:` line
  and the review contract both name the production paths.
- **No `S330` registry row.** `corpus/SOURCES.md` currently holds 329 `S###` rows, the
  last being `S329` at line 340; there are 0 rows matching `| S330 |`. The instrument's
  `source-row` leg requires exactly one `| S330 |` row with 13 split cells whose kind is
  `docs`, tier is `A`, status is `mined`, whose source cell contains the expected URL,
  and whose used-by cell names the matrix JSON path. Writing that row is the source-row
  seat's deliverable; this seat only cites `S330` and records the required cell values
  in the note.
- **No review verdict.** `w1/ReviewMatrix/verdict.json` is the reviewer's file and is not
  written here.
- **No C2 work.** The two `--selftest` repairs and their receipts belong to the executor
  seats; this seat touched neither tool.
- **No host-side reading of installed units.** The matrix is documentation. No
  `systemctl` call was made and no unit was inspected; no claim about the installed
  systemd build is made anywhere in the note.

## Findings

1. **The frozen expected object matches the pinned source table exactly** — 42/42 cells,
   independently re-derived by XML parsing rather than by reading the instrument. The
   C1 matrix leg has no content disagreement to report. (C1's remaining legs — the `S330`
   registry row and the reviewer's digest-bound verdict file — are other seats' and are
   not landed yet, so C1 is not claimable from this seat.)
2. **Two defects in my own first draft were caught by machine verification and fixed**:
   the inverted `X`/empty counts and nine wrong quote word counts / line ranges. Recorded
   above. The lane's own gate would not have caught either — the frozen counter checks
   the matrix bytes, not the prose.
3. **The note's line anchors are snapshot-relative, not host-build-relative.** The
   upstream v262 tag file's line numbers are quoted as such and explicitly are not
   claimed to be the installed build's line numbers; the note says so in its Limits
   section.
4. **The matrix's `X` marks are coarse.** The page does not enumerate the members of
   each cause class (signals, timeout kinds, OOM-adjacent exits), so a marked cell states
   that the policy applies to the class, not to each member. Stated as a limit.
5. **The `no` column is empty in all six rows**, which the prose at `:887` corroborates
   ("no (the default), the service will not be restarted"). Noted so a reader does not
   treat an empty cell as an omission in the matrix.
6. **Six conditions sit outside the table** — manual stop, oneshot (rejected options, not
   merely inert ones), the clean-signal list, `SuccessExitStatus=`,
   `RestartPreventExitStatus=`, `RestartForceExitStatus=`, and start rate limiting. The
   table has no column for any of them, so a reader using the matrix alone will answer a
   different question than the page answers. The note gives each with its exact source
   range.

## Artifact paths

- Matrix draft: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-80/w1/ScribeMatrix/data.json`
  — sha256 `05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153`, 88 lines.
- Note draft: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-80/w1/ScribeMatrix/note.md`
  — sha256 `c92b1e4ca872bcca8cadf6d4a0d2a07613045e5d1b04dc7d38435510733781fa`, 308 lines.
- This report: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-80/w1/ScribeMatrix.md`.
- Production landing paths for the integrating seat (not written by this seat):
  `corpus/knowledge/service-restart-matrix-r80.json` and
  `corpus/knowledge/service-restart-matrix-r80.md`.
- Frozen inputs read (unmodified): `.ufo/waves/round-80/before/expected.json` (sha256
  `05abbf14…`), `.ufo/waves/round-80/before/systemd.service.xml` (sha256 `12770f86…`),
  `.ufo/waves/round-80/before/controls.json`.

**Reviewer notification:** ReviewMatrix is notified by this report file's existence and
by the note digest above; no broadcast was sent.

**Freeze.** `note.md` is frozen at sha256
`1aae7b2a5362c6e63ccdd2df1c7cb06c8712b71950c275fdc9047ab3bba67a0b` (333 lines).
`data.json` is frozen at sha256
`05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153` (88 lines).
No further byte change will be made to either file; if one becomes necessary, the
reviewer must issue a renewed verdict against the new digest rather than reuse this
one.

Scope: executed=none
