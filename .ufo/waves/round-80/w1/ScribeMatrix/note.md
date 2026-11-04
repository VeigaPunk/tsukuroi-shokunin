# Service restart matrix — Restart= policies against six exit causes (round 80)

source: S330 in `corpus/SOURCES.md` — systemd v262 `man/systemd.service.xml` — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml (raw snapshot `.ufo/waves/round-80/before/systemd.service.xml`, sha256 `12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44`)
verified-at: 2026-11-04
recheck: on-release — re-open the same upstream URL at the next systemd tag, compare the raw sha256 against the pinned snapshot digest above, and re-read the `Restart=` table and its surrounding paragraphs; a changed table or changed surrounding condition is an appended erratum, not a rewrite.
companion: `corpus/knowledge/service-restart-matrix-r80.json` (the six-row × seven-policy cell matrix, counted by `tools/measure-round80.py --claim C1`); this note is the prose companion for that matrix.

## What this note is, and what it is not

This is a **finite documentation matrix**: 42 cells read out of one upstream manual page
at one tag. It says which `Restart=` policy the page marks for each of six exit causes.
It is **not** a runtime simulation, not an observation of any host unit, and not a
statement about what any installed systemd build will do.

Three limits are load-bearing and are repeated in the Limits section below:

- **No universality.** Each cell is a reading of what this page states about one cause
  class under one policy. The page's own exceptions (manual stop, oneshot,
  `SuccessExitStatus=`, `RestartPreventExitStatus=`, `RestartForceExitStatus=`, start
  rate limiting) change the answer, and the table does not carry those columns.
- **No installed-build equivalence.** The pinned bytes are the upstream v262 tag file.
  The host runs a distribution build of a systemd version, which may carry patches that
  shift lines and change behaviour. Upstream line anchors here are not host-build line
  numbers, and nothing here is a claim about the installed build.
- **Documentation scope only.** No service was started, stopped, restarted, killed or
  inspected for this note. The unit-level reading of the matrix against a live unit is a
  separate, separately-authored step.

## The source table

The page's `Restart=` entry opens at `systemd.service.xml:876`. The policy options are
listed at `:885-887`; the per-policy prose that defines them runs `:887-911`. The
machine-readable table is titled

> Exit causes and the effect of the Restart= settings

(`systemd.service.xml:914`, 9 words), inside `<table>` at `:913` and closed at `:994`.

Its header row (`:920-929`) names the exit-cause column and then seven policy columns in
this order: `no`, `always`, `on-success`, `on-failure`, `on-abnormal`, `on-abort`,
`on-watchdog`. The `<tbody>` (`:931-992`) holds six cause rows, each with seven cells;
a cell carries the literal text `X` when the page marks that policy for that cause, and
is empty when it does not. The matrix JSON stores `true` for an `X` cell and `false` for
an empty cell, in the header's own column order — so `42` cells = 6 rows × 7 columns,
of which `18` are marked `X` and `24` are empty.

The page's `tgroup` declares `cols='2'` (`:916`) while the header row carries eight
entries; the columns are read from the header row, which is what a reader and a parser
both do.

## The six cause rows, read cell by cell

Each row below gives the cause label with its source line, the marked cells with their
own source lines, and the policy the page attaches to the cause in prose. Cell lines are
the individual `<entry>` elements inside that row's `<row>`. Quotes are the source text
with the XML markup stripped, as the lane's other notes quote XML man pages; each is
located in the pinned snapshot by the cited line range and is 25 words or fewer.

### 1. Clean exit code or signal — `:932-941`

Label at `:933`. Marked: `always` (`:935`), `on-success` (`:936`). Unmarked: `no`
(`:934`), `on-failure` (`:937`), `on-abnormal` (`:938`), `on-abort` (`:939`),
`on-watchdog` (`:940`).

The page defines the class before the table: "In this context, a clean exit means any
of the following:" (`:889`, 11 words), then lists "exit code of 0;" (`:891`), "for types
other than Type=oneshot, one of the signals SIGHUP, SIGINT, SIGTERM, or SIGPIPE;"
(`:892-894`, 14 words), and "exit statuses and signals specified in
SuccessExitStatus=." (`:896-897`, 7 words). So the row marked `on-success` is a row
about a *configured* class, and the class itself is configurable — see the
`SuccessExitStatus=` section below.

### 2. Unclean exit code — `:942-951`

Label at `:943`. Marked: `always` (`:945`), `on-failure` (`:947`). Unmarked: `no`
(`:944`), `on-success` (`:946`), `on-abnormal` (`:948`), `on-abort` (`:949`),
`on-watchdog` (`:950`).

Prose: `on-failure` restarts when the process exits with "a non-zero exit code, is
terminated by a signal" (`:900`, 9 words), the same sentence continuing "(including
on core dump, but excluding the aforementioned" four clean signals (`:900-901`). An
unclean *exit code* is neither a signal nor a timeout nor a watchdog expiry, and the
page's `on-abnormal` and `on-abort` definitions (`:902-906`) cover only those three
kinds of event, so this row leaves both unmarked.

### 3. Unclean signal — `:952-961`

Label at `:953`. Marked: `always` (`:955`), `on-failure` (`:957`), `on-abnormal`
(`:958`), `on-abort` (`:959`). Unmarked: `no` (`:954`), `on-success` (`:956`),
`on-watchdog` (`:960`).

Prose: `on-abnormal` restarts when "the service will be restarted when the process is
terminated by a signal" (`:902-903`, 13 words), continuing "(including on core dump,
excluding the aforementioned four signals)" (`:903-904`). `on-abort` restarts "only if
the service process exits due to an uncaught signal not specified as a clean exit
status" (`:905-906`, 18 words). The two differ because `on-abort` is the narrower
signal-only policy and `on-abnormal` additionally covers timeouts and watchdog expiry.
In the table `on-abort` is marked in this row alone, while `on-abnormal` is marked in
this row and in the Timeout, Watchdog and OOM rows. The two columns therefore differ in
three rows — Timeout, Watchdog and OOM — where `on-abnormal` is marked and `on-abort` is
not.

### 4. Timeout — `:962-971`

Label at `:963`. Marked: `always` (`:965`), `on-failure` (`:967`), `on-abnormal`
(`:968`). Unmarked: `no` (`:964`), `on-success` (`:966`), `on-abort` (`:969`),
`on-watchdog` (`:970`).

Prose: `on-failure` restarts "when an operation (such as service reload) times out, and
when the configured watchdog" timeout is triggered (`:901-902`, 14 words). `on-abort` is
signal-only, so it is unmarked here. Note the scope of the word *timeout* in the page:
it covers a service start, reload and stop operation timeout and the missing watchdog
keep-alive deadline (`:882-883`), which is broader than one cause class.

### 5. Watchdog — `:972-981`

Label at `:973`. Marked: `always` (`:975`), `on-failure` (`:977`), `on-abnormal`
(`:978`), `on-watchdog` (`:980`). Unmarked: `no` (`:974`), `on-success` (`:976`),
`on-abort` (`:979`).

Prose: `on-watchdog` restarts "only if the watchdog timeout for the service expires"
(`:907`, 9 words) — the single-purpose policy, marked in exactly one row.

### 6. Termination due to OOM — `:982-991`

Label at `:983`. Marked: `always` (`:985`), `on-failure` (`:987`), `on-abnormal`
(`:988`). Unmarked: `no` (`:984`), `on-success` (`:986`), `on-abort` (`:989`),
`on-watchdog` (`:990`).

The page gives the OOM row no separate prose of its own. Its marked set is exactly the
Timeout row's set — `always`, `on-failure`, `on-abnormal` — and it differs from the
Unclean exit code row precisely in the `on-abnormal` cell, which is empty at `:948` and
marked `X` at `:988`. The signal-only policy `on-abort` is unmarked here (`:989`), but
`on-abnormal` is marked, so the OOM row is not the unclean-exit-code row with the
signal policies left out. Note also that the `on-abnormal` prose (`:902-904`) enumerates
signals, operation timeouts and watchdog expiry and does not name OOM termination, so
the `X` in this row's `on-abnormal` cell is a table marking that the prose does not
spell out; this note records the marking as read, and does not supply a cause for it.
The only prose in the page that names OOM termination
together with `Restart=` is in the separate `OOMPolicy=` entry (`:1398`), which says
that when the policy is `stop` or `kill` the service ends up in the "failed state after
which Restart= may apply" (`:1417-1418`, 7 words) — a conditional statement about the
unit state under that policy, not a claim that OOM termination always restarts a unit.

### The `no` column

The `no` column is empty in all six rows (`:934`, `:944`, `:954`, `:964`, `:974`,
`:984`). The prose agrees: "no (the default), the service will not be restarted" (`:887`,
9 words).

## The conditions around the table

These are stated in the page next to the table and are not columns in it. A reader who
uses the matrix without them will answer the wrong question.

**Manual stop and systemd-initiated death.** The `Restart=` entry opens with
"Configures whether the service shall be restarted when the service process exits, is
killed, or a timeout is reached." (`:877-878`, 19 words) and adds "When the death of the
process is a result of systemd operation (e.g. service stop or restart), the service
will not be restarted." (`:881-882`, 23 words). The exceptions paragraph states it
again: "As exceptions to the setting above, the service will not be restarted if the
exit code or signal is specified in RestartPreventExitStatus=" (`:996-998`, 22 words)
and "the service is stopped with systemctl stop or an equivalent operation"
(`:999-1000`, 11 words). So a table cell of `true` describes the policy's effect on
that cause, not a promise that a stop-triggered exit restarts the unit.

**Oneshot services.** Two places. The `Restart=` prose: "Type=oneshot services will
never be restarted on a clean exit status" (`:909-910`, 11 words) and "always and
on-success are rejected for them" (`:910-911`, 7 words). And the `Type=` section's example: "For
Type=oneshot, Restart=always and Restart=on-success are not allowed." (`:1779-1780`,
8 words). For a oneshot unit the rows that mark `always` and `on-success` do not apply
as written; the options are rejected, not merely inert.

**Clean signals.** The four clean signals are listed only "for types other than
Type=oneshot" (`:892`), so the clean-signal part of row 1 does not reach oneshot units.

**`SuccessExitStatus=`.** The entry is at `:1064`. It takes "a list of exit status
definitions that, when returned by the main service process, will be considered
successful termination" (`:1066-1067`, 19 words), "in addition to the normal successful
exit status" 0 and the four signals (`:1067-1069`). The page also states that "this
setting does not change the mapping between numeric exit statuses and their names"
(`:1078-1079`, 14 words), and that "This option may appear more than once, in which case
the list of successful exit statuses is merged" (`:1085-1086`, 18 words), with the empty
string resetting the list. Effect on the matrix: a status added to `SuccessExitStatus=`
moves that status into row 1's cause class, so the row-1 `on-success` cell applies to
it.

**`RestartPreventExitStatus=`.** The entry is at `:1105`. It takes a list that will
"prevent automatic service restarts, regardless of the restart setting configured with
Restart=" (`:1108-1109`, 12 words). "Defaults to the empty list, so that, by default, no
exit status is excluded from the configured restart logic" (`:1110-1111`, 19 words). It
also "has no effect on processes configured via ExecStartPre=, ExecStartPost=,
ExecStop=, ExecStopPost= or ExecReload=" (`:1126-1128`, 13 words), "but only on the main
service process" (`:1128-1129`, 7 words). Effect on the matrix: a listed status
suppresses every marked cell for that cause.

**`RestartForceExitStatus=`.** The entry is at `:1137`. It takes a list that will
"force automatic service restarts, regardless of the restart setting configured with
Restart=" (`:1140-1141`, 12 words). Its oneshot note is the counterpart of the oneshot
rule above: "for Type=oneshot services, a success exit status will prevent them from
auto-restarting" (`:1144-1145`, 12 words), "no matter whether the corresponding exit
statuses are listed in this option" (`:1145-1146`, 12 words) — a success exit status
prevents a oneshot unit from auto-restarting even when the status is force-listed.

**Start rate limiting.** "service restart is subject to unit start rate limiting
configured with StartLimitIntervalSec= and StartLimitBurst=" (`:1004-1006`, 14 words),
with details in `systemd.unit(5)` (`:1007`). A marked cell says the policy applies to
that cause; it does not say the restart will happen, because the manager's start rate
limit is a separate gate.

**Recommended choice.** "Setting this to on-failure is the recommended choice for
long-running services" (`:1010-1011`, 11 words), with "on-abnormal is an alternative
choice." (`:1015`, 5 words) "For services that shall be able to terminate on their own
choice (and avoid immediate restarting)," (`:1013-1014`, 16 words). That is a
recommendation sentence, not a table cell.

## Verification of the matrix against the source

The 42 cells in `corpus/knowledge/service-restart-matrix-r80.json` were read out of the
pinned snapshot cell by cell, in the header's column order, and each was checked against
the corresponding `<entry>` line in the source table. Result: **42 of 42 cells agree**
with the source — no cell disagrees, and no cell was adjusted to make the data fit.
18 cells are marked `X` and 24 are empty (per row: 2, 2, 4, 3, 4, 3).

The frozen expected object at `.ufo/waves/round-80/before/expected.json` (sha256
`05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153`) equals this
reading; the draft matrix in this seat's directory is a byte-exact copy of it
(`cmp` identical, same sha256). Had the source table disagreed with the frozen object,
the disagreement would have been reported as a miss and the frozen object left untouched;
that did not happen here.

The registry row `S330` that carries this source does not yet exist in
`corpus/SOURCES.md` at read time (0 rows matching `| S330 |`; the file's last row is
`S329`). This note cites `S330` as the row that must carry it, and its cells are the
upstream URL, kind `docs`, tier `A`, status `mined`, with this note and the matrix JSON
in `used-by`.

## Limits

- Upstream tag v262 file lines are not the installed build's lines. This note makes no
  claim about the systemd build the host runs, and no host unit was inspected for it.
- The matrix is documentation. It does not predict whether a specific unit restarts;
  overrides, `SuccessExitStatus=`, prevent/force lists, oneshot typing and start rate
  limiting all intervene, and the page's own exception paragraphs say so.
- The `no` column being empty in every row is the page's claim about the policy `no`,
  not a measurement of any unit.
- Row 6 (OOM) has no dedicated prose in the `Restart=` entry; its reading is the table
  marks plus the conditional OOM sentence in the `OOMPolicy=` entry at `:1417-1418`.
- `X` marks are the page's coarse classification. The page does not enumerate every
  signal, timeout kind or OOM-adjacent exit path, so a cell marked for a cause class
  does not enumerate the members of that class.
- The quoted fragments are exact fragments of their cited source lines, not complete
  lines: `:907` holds both the `on-watchdog` clause and the start of the `always`
  clause, and the note quotes only the watchdog fragment. A reader who needs the whole
  line must open the cited range.
- Equality between this matrix and the frozen expected object is a finite answer-key
  comparison. It is not proof that the source entails the object, and it is not proof
  that any reviewed artefact was actually read.

## QUALITY check

- **QUALITY 1 (claims falsifiable) and 2 (source anchor).** Every cell claim names the
  snapshot digest and the exact source line of the `<entry>` it was read from; each
  cause row names its `<row>` line range.
- **QUALITY 3 (observation, inference, unknown separate).** The matrix is labelled a
  documentation reading; the surrounding-condition paragraphs are labelled as page
  prose; no host observation is asserted anywhere in this note, so there is no host
  observation to separate from inference.
- **QUALITY 7 (external claim cites an exact registry row).** The single external
  source is cited as `S330` in `corpus/SOURCES.md` with tier `A` and kind `docs`, and
  the exact upstream URL and raw digest are given. No tier-C source is used.
- **QUALITY 8 (`source:`, `verified-at:`, `recheck:` present).** All three header lines
  are present; `verified-at: 2026-11-04` is an ISO date and `recheck: on-release` is a
  cadence keyed to the upstream release trigger.
- **QUALITY 14 (the QUALITY check is performed, not promised).** This section is the
  performed check and names the applicable criteria with the concrete property each
  one is satisfied by.
- **QUALITY 19 (claim/source scope per row).** Each cause row names the source object
  (the pinned `systemd.service.xml` snapshot), the located quote of at most 25 words,
  and the exact proposition it supports. The longest quote used is 23 words, and each
  was located in the pinned snapshot before being written down.
- **QUALITY 21 (portable locators).** Each row is located by the file path plus the
  line range and a quoted fragment, so the row resolves without depending on a
  renderer. Line ranges are reader-line numbers against the pinned snapshot file.
- **QUALITY 23 (section/table citation resolution).** The table is resolved by its
  title quote at `:914` and its header row at `:920-929`; the six body rows are
  resolved individually at `:932-941`, `:942-951`, `:952-961`, `:962-971`, `:972-981`
  and `:982-991`, and each row's quoted label was located in the snapshot before being
  written down.
- **QUALITY 66 (a taught cell keeps every branch its source states).** The
  `on-abort`/`on-abnormal` distinction is stated with both branches (`on-abort` is
  signal-only; `on-abnormal` additionally covers timeouts and watchdog expiry), and
  the `on-failure` prose quote retains its parenthetical about core dump and the
  excluded clean signals.
- **QUALITY 79 (row bound to a digest-checked snapshot at a cited line).** Every row
  is bound to the snapshot whose sha256 is `12770f86…` and to a cited line; the
  snapshot digest is repeated in the header and in the verification section.
- **QUALITY 94 (every cited line accounted for).** The cited ranges cover the
  `Restart=` entry (`:876-911`), the table (`:913-994`), the exception paragraph
  (`:996-1002`), the rate-limiting paragraph (`:1004-1008`), the recommendation paragraph
  (`:1010-1015`), the three exit-status entries (`:1064-1101`, `:1105-1133`,
  `:1137-1148`), the oneshot example (`:1779-1780`) and the OOM sentence in the
  `OOMPolicy=` entry (`:1398`, `:1417-1418`). Each quoted fragment was located verbatim
  inside its cited range after XML markup stripping, and each fragment's own start and
  end lines fall within the range the note cites.
  **Partial compliance, stated honestly:** the criterion also asks that a quote preserve
  the *complete* cited line. Several quotes here are shorter than their source line —
  `:907` carries both the `on-watchdog` clause and the start of the `always` clause, and
  the note quotes only the watchdog fragment; `:900-901` carries the `on-failure` clause
  and the note quotes a fragment of it. The quotes are exact fragments of the cited
  lines, not complete lines, so the complete-line clause is **not** met and is recorded
  as a limitation rather than claimed.
- **QUALITY 98 (upstream version re-read on the release trigger).** The `recheck:` line
  names the trigger, the URL to re-open, the digest to compare and the action to take
  on a change.
- **QUALITY 103 (a tag line pin is not a host-build line).** The Limits section states
  explicitly that these are upstream tag lines and that no installed-build claim is
  made.
- **Not applicable to this note.** QUALITY 6 (a pacman action) and QUALITY 13 (root
  metadata) have no subject here: this note performs no operator action and inspects no
  metadata. QUALITY 81 (a non-author verdict per row) applies to the wave's reviewer
  artefact, not to this draft; this draft states no row as independently reviewed.

## Companion and provenance

- Matrix JSON: `corpus/knowledge/service-restart-matrix-r80.json` (companion; the draft
  bytes in this seat's directory are byte-exact with the frozen expected object).
- Source snapshot: `.ufo/waves/round-80/before/systemd.service.xml`, sha256
  `12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44`.
- Frozen expected object: `.ufo/waves/round-80/before/expected.json`, sha256
  `05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153`.
- Registry row: `S330` in `corpus/SOURCES.md` (to be added by the round's source-row
  seat; not present at the time this draft was written).
