# Seat ScribeFrontier — read-only derivation receipts (round 80, wave 1)

Execution class: **NO-EXEC**. No claim tool was run, no network call, no host
domain command, no git/jj mutation, no production edit. Everything below is a
read of committed/pinned bytes, re-derived in-session with the round-79 locator
rule (tag-stripped, whitespace-normalised token stream with per-token line
numbers) so a reader can reproduce every line number.

Source of truth: `.ufo/waves/round-80/before/systemd.service.xml` (upstream
systemd **tag v262**, `man/systemd.service.xml`).

## 1. Digests (measured, read-only)

| File | sha256 (measured) | Cross-check |
|---|---|---|
| `.ufo/waves/round-80/before/systemd.service.xml` | `12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44` | equals `snapshot_sha256` in `before/expected.json` and the SCORECARD Round-80 declaration |
| `.ufo/waves/round-80/before/expected.json` | `05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153` | equals the SCORECARD "expected object SHA256" |
| `.ufo/waves/round-80/w1/ScribeMatrix/data.json` | `05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153` | byte-identical to `before/expected.json` (parsed objects equal) |

`tools/measure-round80.py` (the frozen instrument) was **read** at
`SHA-256 688766756d0fb73ffb8f1d746e3377d58532bd4afa0a3aa92489c61165614d1d`
(as declared in `SCORECARD.md` and `before/controls.json`); it was **not
executed** by this seat.

## 2. Independent re-derivation of the 42 cells

The table was parsed structurally from the pinned bytes (`<row>` … `</row>`
inside `<table>` at `:913`–`:994`), not copied from `before/expected.json`:

- header cells (`:920`–`:929`) → `Restart settings/Exit causes`, then
  `no, always, on-success, on-failure, on-abnormal, on-abort, on-watchdog`
- six body rows, each 7 setting cells, `X` ⇒ true, empty ⇒ false:

| # | cause (source label, verbatim) | line | restart vector (no, always, on-success, on-failure, on-abnormal, on-abort, on-watchdog) |
|---|---|---|---|
| 1 | Clean exit code or signal | :933 | F T T F F F F |
| 2 | Unclean exit code | :943 | F T F T F F F |
| 3 | Unclean signal | :953 | F T F T T T F |
| 4 | Timeout | :963 | F T F T T F F |
| 5 | Watchdog | :973 | F T F T T F T |
| 6 | Termination due to OOM | :983 | F T F T T F F |

Derived `settings` list == `expected.json.settings`
(`["no","always","on-success","on-failure","on-abnormal","on-abort","on-watchdog"]`) — **True**.
Derived `rows` == `expected.json.rows` — **True** (deep equality, order-sensitive).
42 cells total, 18 marked true, 24 marked false.

## 3. Order divergence between the prose list and the table header (measured)

- Prose enumeration, `:885`–`:886`:
  `no, on-success, on-failure, on-abnormal, on-watchdog, on-abort, always`
- Table column order, `:921`–`:928`:
  `no, always, on-success, on-failure, on-abnormal, on-abort, on-watchdog`

The two orders differ (`always` is 7th in prose, 2nd in the table). The frozen
`expected.json` follows the **table** order. A re-derivation that read the
prose sentence instead of the table header would transpose six of seven columns.

## 3b. Column-divergence measurement (independent, read-only)

Per-row marked cells with the **line of each individual `<entry>` cell** (row
blocks start at `:920, :932, :942, :952, :962, :972, :982`; the label sits at
`start+1` and the seven policy cells at `start+2 … start+8`):

| cause | label line | always | on-success | on-failure | on-abnormal | on-abort | on-watchdog |
|---|---|---|---|---|---|---|---|
| Clean exit code or signal | :933 | :935 | :936 | — | — | — | — |
| Unclean exit code | :943 | :945 | — | :947 | — | — | — |
| Unclean signal | :953 | :955 | — | :957 | :958 | :959 | — |
| Timeout | :963 | :965 | — | :967 | :968 | :969 | — |
| Watchdog | :973 | :975 | — | :977 | :978 | :979 | :980 |
| Termination due to OOM | :983 | :985 | — | :987 | :988 | :989 | — |

Measured divergences:

- `on-abnormal` vs `on-abort` differ in **three** rows, not one: `Timeout`
  (:968 vs :969), `Watchdog` (:978 vs :979), `Termination due to OOM` (:988 vs
  :989). The other three rows agree. This independently reproduces the
  ReviewMatrix finding that a companion revision claiming the two columns
  "differ in exactly one place" was source-inconsistent.
- `on-failure` vs `on-abnormal` differ in exactly **one** row: `Unclean exit
  code` (marked `on-failure`, unmarked `on-abnormal`).
- The OOM row's marked set is identical to the `Timeout` row's marked set
  (`always, on-failure, on-abnormal`), **not** to `Unclean exit code`'s
  (`always, on-failure`). The page states the cell, not the mechanism behind
  it.

## 4. Located quotes (token-stream locator; occurrence count over the whole file)

| Tag | Quote | words | located | occurrences in file |
|---|---|---|---|---|
| A_def | `Configures whether the service shall be restarted when the service process exits, is killed, or a timeout is reached.` | 19 | :877-878 | 1 |
| A_title | `Exit causes and the effect of the Restart= settings` | 9 | :914 | 1 |
| R_stop | `the service is stopped with systemctl stop or an equivalent operation.` | 11 | :999-1000 | 1 |
| R_opsd | `When the death of the process is a result of systemd operation (e.g. service stop or restart), the service will not be restarted.` | 23 | :881-882 | 1 |
| R_oneshot | `Type=oneshot services will never be restarted on a clean exit status,` | 11 | :909-910 | 1 |
| R_oneshot2 | `always and on-success are rejected for them.` | 7 | :910-911 | 1 |
| R_watchdog | `the service will be restarted only if the watchdog timeout for the service expires.` | 14 | :906-907 | 1 |
| R_prevent_scope | `this setting has no effect on processes configured via ExecStartPre=, ExecStartPost=, ExecStop=, ExecStopPost= or ExecReload=,` | 15 | :1126-1128 | 1 |
| C_prevent | `will prevent automatic service restarts, regardless of the restart setting configured with Restart=.` | 13 | :1108-1109 | 1 |
| C_force | `will force automatic service restarts, regardless of the restart setting configured with Restart=.` | 13 | :1140-1141 | 1 |
| C_rate | `service restart is subject to unit start rate limiting configured with StartLimitIntervalSec= and StartLimitBurst=,` | 14 | :1004-1006 | 1 |
| C_exc | `As exceptions to the setting above, the service will not be restarted if the exit code or signal is specified in RestartPreventExitStatus=` | 22 | :996-998 | 1 |
| C_clean | `a clean exit means any of the following:` | 8 | :889 | 1 |
| C_sig4 | `for types other than Type=oneshot, one of the signals SIGHUP, SIGINT, SIGTERM, or SIGPIPE;` | 14 | :892-894 | 1 |
| C_fail | `the service will be restarted when the process exits with a non-zero exit code,` | 14 | :899-900 | 1 |

Sweep scope: the whole 1977-line pinned snapshot, tag-stripped and
whitespace-normalised; "occurrences" is the count of that exact token span in
the whole file, so every cited span is unique in the file. No line outside the
cited ranges was used to support any statement in the Gate block.

## 5. Registry facts (read-only)

- `corpus/SOURCES.md`: 329 data rows, ids `S001`…`S329` contiguous; `S330`
  **unused**; max id `S329`.
- Registry table rows run `SOURCES.md:7`–`:340`; `## Paths` starts at `:342`.
  A new row must be appended inside the `## Registry` section (the census emits
  `E12` for a row outside it).
- `url_of()` on the source cell of the drafted row yields
  `raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml`,
  which is **not** the first URL of any existing row (only `S070` mentions a
  `systemd.service` page, and its first URL is the freedesktop one), so no
  `W04`/`E04` duplicate-URL finding is expected for the new row.
- `status` values across the registry: 291 `mined`, 33 `rejected`, 5 `queued`.
  The 33 rejected rows are untouched by this round.
- The frozen instrument greps the registry literally for a line starting
  `| S330 |` and requires exactly one such line with 13 `|`-split fields
  (11 cells), `kind=docs`, `tier=A`, `status=mined`, the URL inside the source
  cell, and `corpus/knowledge/service-restart-matrix-r80.json` inside the
  used-by cell. The id `S330` is therefore forced by the frozen instrument, not
  a free choice of this seat.
- The read-only staged package `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`
  already uses the bare id `S330` for a **different** document
  (`lanes/tsukuroi/round14/captures/mirror-language-list-capture.txt`, own-work
  mirror changelog capture). The package is **not adopted**; no renumbering is
  applied and no bytes are copied. Adjudication of that id collision is
  ConnectorScope's lane, not this seat's; this seat only records it.

## 6. Instrument reading (why the draft row is shaped as it is)

`tools/measure-round80.py:31`–`:47` (C1) evaluates in this order:
snapshot/expected digest → matrix equality → registry row → review binding.
`tools/measure-round80.py:49`–`:62` (C2) checks the `## Gate and probe registry
— round71 superseding current rows` section, the tool blob's `--selftest` /
`SELFTEST` tokens, and the receipt's `tool_sha256`/`argv`/`rc`/`passed`/`failed`.

Two consequences used by the draft row: the used-by cell must contain the
frozen `NOTE` path `corpus/knowledge/service-restart-matrix-r80.json`, and the
census (`scripts/sources-census.sh`, `usedby_findings`) requires every used-by
path of a `mined` row to exist on disk at census time — so the row and both
companions must land in the same integration step.
