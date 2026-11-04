# Round 79 — unit dependency propagation and the gate-standard registry

Base `9086589a82f221d130ed6711fbe70b85f0d07aea`; frozen claim commit
`afe1f26128bde87484001cd02ebf11fa524c4059`. LOG.md Round 79 motivates C1
depth (8, lowest non-retired) and C2 operability (9). Neither claim pre-claims
an ordinal uplift, coverage or a capability. L1 holds the planner seat.

C1 opened systemd v262 `man/systemd.unit.xml` and froze eight
dependency-propagation rows. The reviewer's first pass found that the frozen
DP6 statement dropped the source's precondition ("and no job is queued for
them"); the landed entry carries the corrected statement, so the **frozen C1
predicate is a declared miss** — its expected tuple cannot be altered after
data without being a different instrument. C2 marks the four current
continuation registry tables non-operative and gives the two routed round-72
gates real hermetic selftests; it verifies.

## Gate

L1 opened the exact upstream URL on 2026-11-04 and pinned it before the freeze
commit: `.ufo/waves/round-79/before/src/systemd.unit.xml`, SHA-256
`eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6`;
`before/expected.json` SHA-256
`0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21`.
ScoutSources reopened the URL independently (`curl` 200, 165445 bytes, same
digest) and re-derived every row line by three methods. Quotes are located in
the tag-stripped, whitespace-normalized snapshot by token position; line
numbers are upstream v262 tag lines, not installed Arch build lines.

| Row / candidate | URL, access date, located quote (at most 25 words) | Decision / reason / flip |
|---|---|---|
| S329 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml ; 2026-11-04, :659: `Configures (weak) requirement dependencies on other units.` | admit, tier A/docs/mined for the dependency-propagation and ordering keyword scope only: Wants= :657-679, Requires= :682-708, Requisite= :711-728, BindsTo= :731-758, PartOf= :761-778, Upholds= :781-797, Before=/After= :826-866, RequiresMountsFor= :934-947; eight finite DP rows over documented semantics, not a live-host reading and not an installed-build equivalence claim |
| `After=` pulls the unit in | same page, :855-857: `Note that those settings are independent of and orthogonal to the requirement dependencies as configured by Requires=, Wants=, Requisite=, or BindsTo=.` | reject: ordering and requirement dependencies are orthogonal — an `After=` line alone never creates a requirement dependency and never pulls a unit into the transaction. Flip: a located upstream passage stating that `After=` itself creates or implies a requirement/pull-in dependency |
| `Requires=` guarantees the listed unit stays active | same page, :698-699: `Note that this dependency type does not imply that the other unit always has to be in active state when this unit is running.` | reject: `Requires=` explicitly does not imply the other unit must remain active; the page directs `BindsTo=` with `After=` for that guarantee. Flip: a located upstream passage stating that `Requires=` guarantees continued active state of the listed unit |
| `Upholds=` is a one-time pull-in | same page, :785-787: `While a Wants= dependency on another unit has a one-time effect when this units started, a Upholds= dependency on it has a continuous effect,` | reject: the page contrasts `Wants=` (one-time effect) with `Upholds=` (continuous effect, constantly restarting the unit). Flip: a located upstream passage stating that `Upholds=` has only a one-time pull-in effect |

S329 is a new row; no existing row's status, recheck or used-by changed.
Census at round start and round end exits 0, W04 duplicate-URL warnings only
(the URL is also S304's for the unit-load merge plane; different scopes, so
W04 not E04). Id-collision caveat, recorded and not smoothed: the
read-only staged package `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`
already uses the bare id `S329` for a different document (an own-work
mirror/locale capture; package ids run S200–S346, intersection with this
registry S200–S328). The package is not adopted, and the frozen claim required
`S329` here; resolution is namespace/document context, never arithmetic
renumbering. The package stays unadopted.

## Mistakes

| Class / id | Evidence | Captured-by | Fix shown able to fail |
|---|---|---|---|
| stale-premise — R79-FROZEN-ROW-DP6 | `w1/ReviewDeps/review-first.md` (first review, DP6 `partly-holds`); source :783-785 | QUALITY 66 (keep every branch) and 94 (complete cited line) | The frozen statement stopped at "failed," and dropped the sentence's continuation "and no job is queued for them". The landed entry's DP6 statement carries the precondition; ReviewDeps' second review holds all eight. The frozen C1 tuple is not edited: `tools/measure-unit-deps-r79.py` at any revision reads `count=0` for the corrected data, which is the recorded miss. |
| reference-drift — R79-DUPLICATE-COUNT | r78 closure "seven re-registered tools"; `w1/ReviewRegistry/findings.md`; `tools/check-gate-standard-r79.py` base arm | QUALITY 104 (counts bind to receipts) | The measured count is **six** table rows; the seventh candidate (`count-uf-rows-r74`) is a prose sentence in the round-73 block, not a table row. A line-keyed counter would double-count prose, so the counter counts rows in 8-column tables only. Base receipt `duplicates=6`. |
| vacuous — R79-QUOTE-BOUNDARY | the first `before/expected.json` (superseded before freeze, digest `17851611…`); `before/controls.json` | QUALITY 80 (pre-data controls) | The first authored quotes were substring fragments that ended inside a token (`started` vs `started.`), so the token-boundary locator refused every row. The control run found it before any seat existed; the frozen expected file now carries token-exact quotes and its digest is `0c09c7a4…`. |
| scope — R79-C2-SHAPE-SCOPE | `w1/CriticFreeze/attacks.json` A13/A14; `w1/ReviewRegistry/findings.md` F1b | QUALITY 87 (a counter reads what it credits) | The shape leg checks the two routed rows only. Of the operative table's 93 `gate` rows, 36 still declare "none" in their self-test cell (measured over `SKILL.md` at the measured revision); that inherited debt is disclosed, not claimed closed. The attack fixtures show a self-test cell naming a nonexistent sibling tool still passes — a counter gap in the delivered bytes, not in the two rows. |
| landing — R79-S329-ID-AMBIGUITY | `w1/ConnectorScope/ids.json`; `w1/ScribeSources/sources-gate.md` | CORPUS.md rule 1 (a row is a claim) and the census pattern | The staged package's bare `S329` names a different artifact; no staged bytes are adopted, so no renumbering is applied and the ambiguity is recorded here and in the report. Flip: operator release of the package plus a document-scoped renumber map. |
| process — R79-SCRIBELESSON-UNSETTLED | wave settlement below | QUALITY 96 (write the binding file first) | The ScribeLesson seat produced no binding file and no report; the L1 wrote this lesson instead. The dead seat is recorded with its status, not replaced. |

## Seat harm

| Round | Harmed seat | Causing seat | Evidence class | Effect | Fix |
|---|---|---|---|---|---|
| 79 | — | — | — | entries: none observed in w1 settlement (source: `.ufo/waves/round-79/w1-results.json`) | none required |

## Domain task

`w1/ExecHost/handoff.md` is the round's real read-only host task. Capture
2026-11-04T19:08:44Z–19:09:59Z UTC, unprivileged, no unit touched. Directive
counts over `/etc/systemd` + `/usr/lib/systemd` unit files: After= 279,
Before= 240, Wants= 75, Requires= 70, PartOf= 24, RequiresMountsFor= 20,
BindsTo= 20, Upholds= 1 (729 matched lines, all under `/usr/lib/systemd`).
Zero counts are bounded grep results, not proof of non-use: drop-ins,
generated `/run` units, symlinked `/etc` unit files and `Requisite=` were not
in the sweep, and the handoff says so. Two user-scope transient
`systemd-run` scopes are failed with `Result=oom-kill`; system scope has zero
failed units. Neither failed scope carries `BindsTo=`/`PartOf=`/`Upholds=`,
so per DP4–DP6 nothing propagates and nothing will restart them — they are
inert until an operator acts. No restart, edit, vacuum or package transaction
is authorized by this record.

## Wave settlement and recovery

PENDING-SETTLEMENT — filled from `.ufo/waves/round-79/w1-results.json` and the
WAVE-DONE message; no seat count is asserted before they exist.

## Frontier, reflection and holds

Assimilation: none. The operator-held package and promotion remain unadopted;
the collision guard is reproduced by ConnectorScope (147 staged ids,
S200–S346; intersection S200–S328) and no staged row is appended. Latest
`considerthese/2026-10-26.md` proposal adopted: the "seat-harm incident log"
lands as QUALITY 110 and this lesson's `## Seat harm` table; the
counter-attack scoreboard, downstream patch-offset boundary and
correction-propagation map already have lane rules.

This is deeper existing systemd-unit ground, not a coverage-map promotion;
`PROVINCE.md` and `SHONEN.md` are unchanged. No capability row is entered:
the two counters are round-scoped instruments, not a new general-purpose mode.
C1 is a declared miss; C2 verifies. Outside round-79 closure remains pending.

## QUALITY check

This is the author's explicit check, not an admission.

- **1, 2, 3 (falsifiable / sourced / observation vs inference vs unknown):** every DP row names S329, a snapshot digest and a located quote; the statement is a reading of that quote; live-host claims are absent. The DP6 correction is recorded, not smoothed.
- **7 (tier and anchor):** S329 is tier A/docs for documented directive semantics only; S304's shared URL is a separate scope.
- **9 (negative claims carry sweeps):** the companion's negative readings are scoped to the pinned entry/file; the coexisting "does not say the opposite" sentence is bounded to the entry after review F4.
- **66 (every branch kept):** the landed DP6 statement carries "when no job is queued for them"; the other seven statements match their quoted sentence's scope, as the second review records.
- **86 (upstream, not own-work, for rules):** every row's `source` is S329 whose kind is `docs`; no row rests on an own-work capture.
- **94 (cited ranges accounted):** the eight quote spans are inside S329's registered ranges and the companion lists them; the DP1 `:665-667` vs `:666-667` slip was caught by review F7 and removed.
- **99 (append-only):** `SCORECARD.md`, `LOG.md`, `QUALITY.md`, `SOURCES.md` and `corpus/README.md` gain appended blocks only; the record sweep is in `after/record-sweep.json`.
- **103 (upstream line ≠ host line):** the entry states its lines are v262 tag lines, not installed-build lines.
- **110 (seat harm tally):** present above with an explicit empty verdict and its source.
