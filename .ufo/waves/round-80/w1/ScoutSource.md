# Seat ScoutSource — round 80 w1

- Seat: `ScoutSource` (scout). Axes judged: **depth**, **operability**.
- Claim focus: **C1** (depth 8, sourced S330) — source-side independence.
- Execution class: **EXEC-AUTHORIZED** — limited to: curl / python urllib fetch of the pinned
  public URL `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml`,
  sha256 computation, XML table extraction, and read-only file comparisons.
  **No domain commands** (no `systemctl`, no `journalctl`), no builds/tests/formatters,
  no Git/JJ mutation, no production edits, no package installs (none needed).
- Base commit `467a9b7891a5939dab8460ec6f591fbb16bd82e9`; frozen commit
  `61ec89ec6e6f284b6fba2127721359e6931a5789`; working HEAD `aad05ef1` (read-only `git` inspection only).
- Scratch: `/fast/scratch/hyaku/tsukuroi-r80/ScoutSource/` — one live tree, **deleted before yield**
  after durable receipts were copied.
- Durable outputs: `.ufo/waves/round-80/w1/ScoutSource/` (13 files) + this binding report.

---

## 1. Headline

**The frozen expected matrix is source-correct.** Independently re-opening the pinned upstream
URL and re-deriving the six causes × seven policy cells by **four mutually independent methods**
produced a matrix identical to `before/expected.json` on all 42 cells, and identical to
systemd v262's **own implementation** in `src/core/service.c`. **No expected cell error found.**

| Check | Result |
|---|---|
| Live fetch SHA256 vs frozen snapshot | **IDENTICAL** (`12770f86…d44`), 120642 bytes, `cmp` byte-identical |
| Upstream tag provenance (`v262` → commit → blob) | blob `57bb224c…` **matches** locally recomputed git blob sha1 |
| M1 ElementTree vs M2 XML-regex vs M3 roff (installed man) | **all three identical** (settings, labels, 42 cells) |
| M3 (host's installed man page) vs M1 | **identical** — host's systemd 262.1 docs carry the same table |
| Independent matrix vs frozen `expected.json` | **all 42 cells MATCH**; settings order matches; labels match |
| Prose entailment (39 derived assertions) | **0 mismatches** |
| Implementation entailment (42 cells vs `service_shall_restart()`) | **0 mismatches** |
| Cross-version stability (v262 / v262.1 / upstream `main`) | table **identical** in all three |
| Base registry rows (independent count) | **329** rows, S001–S329, no gaps/dupes, S330 free |
| Independent census re-derivation | **52 W04**, set-identical to frozen `before/census.txt` |

---

## 2. Independent re-derivation (not importing `measure-round80`)

Four independent code paths, none of which imports `tools/measure-round80.py`:

| # | Method | Code | Input | Result artifact |
|---|---|---|---|---|
| M1 | `xml.etree.ElementTree`, table located by `<title>` | `extract_table.py` | pinned v262 XML | `independent-matrix.json` |
| M2 | Pure regex over raw XML text (no XML parser) | `extract_table_regex.py` | pinned v262 XML | `independent-matrix-regex.json` |
| M3 | roff `T{…}T` cell parse | `extract_table_roff.py` | **installed** `/usr/share/man/man5/systemd.service.5.gz` | `independent-matrix-roff.json` |
| M4 | Implementation predicates from `service.c` + `ServiceResult` enum from `service.h` | `impl_check.py` | v262 `src/core/` | 42/42 agree |

M1 ≡ M2 ≡ M3 on settings order, the six cause labels, and all 42 boolean cells.
`compare.py independent-matrix.json before/expected.json` → **`VERDICT: MATCH`**
(settings order matches XML header order; 42/42 cells equal; true-cell count 18 = 18).

**M3 is the strongest single check**: it reads the *host's installed* man page — a different
rendering of the same upstream document — and reproduces the matrix exactly, so the matrix is not
an artifact of how I parsed the XML.

### Upstream tag provenance (not just a mutable-branch fetch)
`refs/tags/v262` → annotated tag object `1f7dffaf…` (tagger date `2026-09-22T13:12:43Z`) →
commit `8cc40e0c5e9234bf45084751ac53b1fbfe70b492`. GitHub's contents API reports
`man/systemd.service.xml` at that commit as blob sha1 `57bb224c24fd71e53a3a52fea9f35aed994d1ed9`,
size 120642. Recomputing the git blob sha1 locally from the fetched bytes gives
`57bb224c24fd71e53a3a52fea9f35aed994d1ed9` — **match**. The fetched bytes are the blob the
v262 tag points at, not a moving branch tip.

---

## 3. Independent semantic verification (depth axis)

### 3a. Prose entailment — 39/39
`prose_check.py` encodes the v262 `Restart=` prose definitions and checks each cell against them:
`on-success` only for a clean exit; `on-failure` for non-zero exit, unclean signal, operation
timeout, watchdog timeout; `on-abnormal` for unclean signal, timeout, watchdog timeout (**not**
non-zero exit code); `on-abort` only for an uncaught non-clean signal; `on-watchdog` only for the
watchdog timeout; `always` for everything; `no` for nothing. **39 assertions, 0 mismatches.**

### 3b. Implementation entailment — 42/42
The man page is documentation; `src/core/service.c:service_shall_restart()` is the behaviour.
`impl_check.py` encodes the six restart predicates verbatim and evaluates them against the
`ServiceResult` enum (`service.h`), mapping each cause to its result
(`SERVICE_SUCCESS`, `SERVICE_FAILURE_EXIT_CODE`, `SERVICE_FAILURE_SIGNAL`,
`SERVICE_FAILURE_TIMEOUT`, `SERVICE_FAILURE_WATCHDOG`, `SERVICE_FAILURE_OOM_KILL`).

**All 42 cells agree with the implementation.** This is the decisive answer to the OOM row:
the prose does **not** mention OOM at all, so the OOM row is table-only content and could not be
prose-checked — but the implementation *does* adjudicate it, and it agrees with the frozen cell
(`on-failure` T, `on-abnormal` T, `on-abort` **F**, `on-watchdog` F). `SERVICE_FAILURE_OOM_KILL`
is excluded from `ON_ABORT` (which admits only `SERVICE_FAILURE_SIGNAL` and
`SERVICE_FAILURE_CORE_DUMP`) and admitted by `ON_ABNORMAL` (which excludes only
`SERVICE_SUCCESS`/`SERVICE_FAILURE_EXIT_CODE`/`SERVICE_SKIP_CONDITION`). **The upstream table is
correct on this row; the frozen expected cell is not an error.**

### 3c. Surrounding qualifiers reviewed (each is *not* in the matrix, by design)
Per the SCORECARD, conditions belong in the companion, not the 42 cells. Verified present in the
pinned source and worth carrying:

- `Type=oneshot` services are never restarted on a clean exit status — `always` and `on-success`
  are rejected for them (service.c:1059 rejects them at verify time).
- `RestartPreventExitStatus=` suppresses restart regardless of the setting;
  `RestartForceExitStatus=` forces it regardless (service.c:2430-2449, checked **before** the
  `Restart=` switch).
- `systemctl stop` or equivalent operation suppresses restart.
- Death caused by systemd operation (service stop or restart) is not restarted.
- Start rate limiting (`StartLimitIntervalSec=`, `StartLimitBurst=`) applies to restarts.
- `RestartMode=` (`normal`/`direct`/`debug`, added v254) governs *how* the restart happens.
- `SuccessExitStatus=` widens what counts as a clean exit.
- Timeouts include the watchdog keep-alive deadline and start/reload/stop operation timeouts.
- `Restart=` also governs `ExecStartPre=`, `ExecStartPost=`, `ExecStop=`, `ExecStopPost=`,
  `ExecReload=` processes, not only the main process.

**Operational caveat on the matrix itself:** the upstream `<tgroup cols='2'>` declares two columns
and two `<colspec>` entries, but every row carries **eight** `<entry>` elements (the corner label
plus 7 policy cells). A parser that trusts `cols`/`colspec` silently drops six of eight cells per
row and yields an all-empty matrix. The table is also marked up with `<entry/>` self-closing
empty cells (24 in this table) rather than `<entry></entry>`. Both hazards are handled by the
extractors here; a future re-derivation must not trust the declared column count.

---

## 4. Independent base-registry count (bounded scope check)

Counted from `corpus/SOURCES.md` directly — **not** copied from the r79 report:

- rows matching `^| S[0-9]{3} |` = **329**; unique ids = 329; ids run **S001–S329 with no gaps and
  no duplicates**; **`S330` is absent and is the next free id**.
- Every row splits into exactly **13** pipe fields (no stray `|` in any cell) — matches the census
  `NF==13` requirement.
- tier: A=312, B=6, C=11. kind: docs=174, code=108, own-work=34, community=8, dataset=2, tool=2,
  spec=1. status: mined=291, queued=5, rejected=33.
- Verified at the base commit itself via read-only `git show 467a9b78:corpus/SOURCES.md` → **329
  rows**, S329 present, S330 absent.
- **Consistent with** the SCORECARD's "329 source rows" and with r79's `ScoutSources.md` line
  "lane registry currently holds 328 rows, ids S001–S328" (that was the r79 *pre-landing* state;
  S329 landed in r79's integration step, which is exactly what r79's `ReviewDeps.md` records).

### Independent census re-derivation
I re-implemented the frozen `scripts/sources-census.sh` validate-mode rules (E01–E12, W01–W04)
in Python and ran them read-only against the base registry:

- **BASE: 329 rows, 52 findings, all `W04` "duplicate url … across scopes", 0 E-level errors.**
- The **W04 id set is exactly the frozen `before/census.txt` W04 id set** (52 == 52, set-equal,
  same members). The frozen census also reports 52 W04 lines, one `ok` line, `exit=0`, 0 E-level
  errors — **my independent re-derivation reproduces the frozen census exactly.**
- **With a hypothetical S330 row inserted directly after S329: 330 rows, and the only new
  findings are two `E11`s** (`missing used-by corpus/knowledge/service-restart-matrix-r80.md` and
  `…-r80.json`). E11 fires because those two companion files do not exist on disk yet; it is
  expected until they land and is **not** a defect in the row's content. No E01/E03/E04/E05/E06/
  E07/E08/E09/E10/E12 and **no new W04**.
- **S330 URL uniqueness:** the census normalizes the *first* URL in the source cell. No existing
  row's first URL equals `raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml`,
  and **no registry row cites that URL anywhere** in its source cell. The only row citing any
  raw `systemd.service.xml` is **S070**, which cites **v262.1** (a different URL) with a different
  scope (`ExecStopPost=`) and whose first URL is `freedesktop.org` — so S070 does **not** collide
  with S330 under the census's first-URL key. The W04 census output already lists S070-era
  siblings (S126/S136/S137/S184) as cross-scope duplicates, so S330 is clean on this axis.

---

## 4b. Cross-check against sibling review artifacts (source-side adjudication)

While this seat ran, the `ReviewMatrix` seat landed two artifacts and the `ScribeMatrix` seat
landed a **revised** `note.md`. Both were checked against my independent matrix and the pinned
snapshot:

- `.ufo/waves/round-80/w1/ReviewMatrix/review-8a99e339.json` (older companion, sha `8a99e339…`)
  recorded six `fails` on two findings: (i) the companion claimed `on-abnormal` and `on-abort`
  separate in exactly one place, while the source shows three differing rows; (ii) a QUALITY 94
  label claimed complete cited lines were preserved while a quoted fragment was shorter than its
  source line.
- **Finding (i) is confirmed by my independent matrix.** `on-abort` is marked in exactly one row
  (`Unclean signal`); `on-abnormal` is marked in four (`Unclean signal`, `Timeout`, `Watchdog`,
  `Termination due to OOM`). The two columns therefore differ in **three** rows — `Timeout`,
  `Watchdog`, `Termination due to OOM` — which is what the source rows at `:968-969`, `:978-979`,
  `:988-989` show. My three-method extraction and the implementation cross-check agree with the
  three-row reading, so the older companion's "exactly one place" wording was the error, not the
  source.
- **The revised `note.md` (sha `1aae7b2a…`) already carries the corrected wording** ("The two
  columns therefore differ in three rows — Timeout, Watchdog and OOM", note.md:99-100) and states
  QUALITY 94 as **"Partial compliance, stated honestly"**, explicitly recording that the
  complete-line clause is **not** met (note.md:306-312). The reviewer's `verdict.json` binds that
  revised companion (`companion_sha256 = 1aae7b2a…`) with six `holds`. Both findings are therefore
  addressed in the current artifact; I record them as **resolved**, not as open defects.

Independent verification I ran against the revised companion (read-only, source-side):

- **All 114 distinct `:NNN` / `:NNN-NNN` line citations** in `note.md` resolve to non-blank,
  in-range lines of the frozen snapshot `before/systemd.service.xml`. Spot-checks land exactly
  where the note says: `:914` = the table `<title>`, `:920-929` = the header row,
  `:932-941` = the `Clean exit code or signal` row, `:963` = the `Timeout` label,
  `:982-991` = the `Termination due to OOM` row.
- **All 30 quoted fragments with an explicit `(:NNN, N words)` citation** were located
  **verbatim** inside their cited range after XML-markup stripping, and **every one has the exact
  word count claimed** (0 problems).
- `note.md`'s structural anchors match the snapshot: the `Restart=` entry at `:876-911`, the table
  at `:913-994`, the exception paragraph at `:996-1002`, the rate-limiting paragraph at
  `:1004-1008`, the recommendation paragraph at `:1010-1015`, the three exit-status entries at
  `:1064-1101` / `:1105-1133` / `:1137-1148`, the oneshot example at `:1779-1780`, and the OOM
  sentence in `OOMPolicy=` at `:1398` / `:1417-1418`.

---

## 5. C1 gate observations for the integrator (operability axis)

Read from `tools/measure-round80.py` (sha256 `688766756d0fb73ffb8f1d746e3377d58532bd4afa0a3aa92489c61165614d1d`,
matching the SCORECARD and the instrument's own claim):

- The C1 leg is **equality against a frozen answer key** (`json.loads(NOTE) != expected` → exit
  `matrix-mismatch`). It compares **parsed JSON**, not bytes, so the landed
  `corpus/knowledge/service-restart-matrix-r80.json` must be *semantically* equal to
  `before/expected.json` — key order and whitespace do not matter, but every field must match.
  **My independent matrix is semantically equal** (settings equal, rows equal), so a note built
  from it passes.
- `expected['url']` must appear in the S330 row's **source cell** (`row[2]`), and
  `corpus/knowledge/service-restart-matrix-r80.json` must appear in its **used-by cell**
  (`row[11]`); kind `docs`, tier `A`, status `mined`. **The row must carry exactly 13 pipe
  fields**, and there must be **exactly one** `| S330 |` line in the registry.
- The registry row must be inserted **inside the `## Registry` table block** — the frozen census
  only counts rows while `in_registry==1`, so appending S330 after the `## Paths` heading would
  both evade the census and fail the instrument. Inserting directly after S329 (line 340) is the
  correct position.
- The C1 leg additionally requires `.ufo/waves/round-80/w1/ReviewMatrix/verdict.json` to exist and
  to equal exactly `{'artifact_sha256': sha(NOTE), 'companion_sha256': sha(COMPANION),
  'verdicts': ['holds']*6}` — note **strict dict equality**: any extra key fails the leg.
  **Current state at my last read**: `verdict.json` **has landed** and binds
  `artifact_sha256 = 05abbf14…5153` (the frozen `expected.json` digest, i.e. the same bytes as
  `ScribeMatrix/data.json`) and `companion_sha256 = 1aae7b2a…` (the revised `note.md`) with six
  `holds`. The two **production** companions `corpus/knowledge/service-restart-matrix-r80.json`
  and `…-r80.md` and the **S330 registry row** did **not yet exist** in the working tree at my
  last read — they are the integrator's remaining step. Note that the C1 leg reads the NOTE and
  COMPANION at the *evaluated revision*, so the companions must be **committed**, and the
  `companion_sha256` in `verdict.json` must match the companion **as committed**.
- Note the C1 leg also requires the *snapshot* digests to be unaltered: `EXPECTED_SHA` and
  `SOURCE_SHA` are checked before anything else (`snapshot_tampered`). Both hold at the frozen
  commit.

---

## 6. Honest limits of this seat's evidence

- **The matrix is documentation, not observed restart behaviour.** My implementation cross-check
  is a *static* reading of v262's `service_shall_restart()` predicates against the documented
  cause→result mapping. It is strong corroboration, not a live restart test; I ran no domain
  commands and restarted nothing.
- **The cause→`ServiceResult` mapping is my mapping**, taken from the table's own row semantics.
  It agrees with the table on all 42 cells, which is the point of the check, but it is not
  independently derived from systemd's state machine for each cause.
- **The frozen `expected.json` is an answer key.** My confirmation is that the key faithfully
  transcribes the upstream source — that the key is *the* correct transcription of v262's table
  and implementation. It is not an authenticity proof that the reviewer will bind, nor a
  whole-registry conformance proof.
- **Registry row count (329) is a bounded scope check**, not a full census run: I re-derived the
  census's own validate-mode rules and reproduced its W04 set exactly, but I did not execute
  `scripts/sources-census.sh` itself (that is a fleet-root tool outside my assigned scope).
- **Live-behaviour qualifiers** (oneshot rejection, `RestartPreventExitStatus=`,
  `RestartForceExitStatus=`, `systemctl stop`, rate limiting, `RestartMode=`) were verified as
  *present in the pinned source and the v262 implementation source*, not exercised live.
- **No host package/tool was installed or updated** for this seat; nothing to record on that axis.

---

## 7. Scope statement

- Commands executed (all read-only or fetch; no domain commands; no Git/JJ mutation):
  `curl -sS -L --fail --max-time 60 -o live-systemd.service.xml <pinned URL>` and the same for the
  `v262.1` and `main` tags and `api.github.com/repos/systemd/systemd/…` (refs/tags/v262, git
  tags, contents); `sha256sum`, `cmp`, `wc -c` on the fetched and frozen files; `xxd` on one byte
  range; `zcat /usr/share/man/man5/systemd.service.5.gz`; `git rev-parse HEAD`, `git log --oneline`,
  `git show <rev>:<path>`, `git cat-file -t`, `git status --porcelain` (read-only);
  `python3 extract_table.py|extract_table_regex.py|extract_table_roff.py|compare.py|prose_check.py|impl_check.py`
  in scratch; a read-only Python re-implementation of the census validate rules over
  `corpus/SOURCES.md`.
- **No production file was created, modified, or deleted.** No sibling/fleet file was written.
  No `pacman`/package transaction, no `sudo`, no host service restarted, no secret or config read.
- Scratch tree `/fast/scratch/hyaku/tsukuroi-r80/ScoutSource/` deleted before yield after the 15
  durable receipts were copied to `.ufo/waves/round-80/w1/ScoutSource/`.
- Durable receipts written (15): `independent-matrix.json`, `independent-matrix-regex.json`,
  `independent-matrix-roff.json`, `matrix-v262_1.json`, `matrix-main.json`, `evidence-digests.txt`,
  `extract_table.py`, `extract_table_regex.py`, `extract_table_roff.py`, `compare.py`,
  `prose_check.py`, `impl_check.py`, `verify_companion_citations.py`, `service.c`, `service.h`.
- **Execution class: EXEC-AUTHORIZED.** No outside/non-author promotion authority is claimed.

Scope: executed=`curl -sS -L --fail --max-time 60 -o live-systemd.service.xml https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml` (plus the same fetch for tags `v262.1` and `main`, and `api.github.com/repos/systemd/systemd/{git/ref/tags/v262,git/tags/1f7dffaf…,contents/man?ref=8cc40e0c…}`); `sha256sum`/`cmp`/`wc -c` on fetched+frozen files; `xxd -s … -l 36 live-systemd.service.xml`; `zcat /usr/share/man/man5/systemd.service.5.gz`; `git rev-parse HEAD`, `git log --oneline -3`, `git cat-file -t 61ec89ec…`, `git show 61ec89ec…:.ufo/waves/round-80/before/{systemd.service.xml,expected.json}`, `git show 467a9b78…:corpus/SOURCES.md`, `git status --porcelain`; `python3 extract_table.py live-systemd.service.xml independent-matrix.json`; `python3 extract_table_regex.py live-systemd.service.xml independent-matrix-regex.json`; `python3 extract_table_roff.py installed-systemd.service.5 independent-matrix-roff.json`; `python3 extract_table.py live-v262.1.xml matrix-v262_1.json`; `python3 extract_table.py live-main.xml matrix-main.json`; `python3 compare.py independent-matrix.json .ufo/waves/round-80/before/expected.json`; `python3 prose_check.py live-systemd.service.xml independent-matrix.json`; `python3 impl_check.py independent-matrix.json`; `python3 .ufo/waves/round-80/w1/ScoutSource/verify_companion_citations.py .ufo/waves/round-80/before/systemd.service.xml .ufo/waves/round-80/w1/ScribeMatrix/note.md`; read-only Python re-implementation of the frozen census validate rules over `corpus/SOURCES.md`.
