source: S329 — systemd v262 `man/systemd.unit.xml` (tier A, docs, mined) — https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml
verified-at: 2026-11-04; frozen v262 snapshot reading only; no live-host measurement
recheck: on-release; reopen systemd.unit.xml at the new tag, compare the digest, and run python3 tools/measure-unit-deps-r79.py --revision <REV>
companion: systemd-dependency-propagation-r79.json

# Systemd dependency propagation — eight pinned rows (round 79)

This entry holds eight pinned dependency-propagation rows (DP1–DP8) read from one
frozen upstream systemd v262 manual snapshot, and the companion JSON holds the same
eight rows as machine-readable objects. The rows are documentation readings, not
observations of a running manager: nothing here was measured on this host.

## (a) Source and boundary

- **Source.** systemd v262 `man/systemd.unit.xml`, upstream tag `v262`, read from
  `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml`,
  registry row **S329** (tier A, docs, mined).
- **Frozen snapshot.** `.ufo/waves/round-79/before/src/systemd.unit.xml`, sha256
  `eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6`. Every
  line number below is a line of that upstream tag file.
- **Upstream tag lines, not installed build lines.** These are the line numbers of
  the v262 tag's XML source. The host runs a distribution build of systemd, which
  may carry patches that shift lines; no line here is a host-build line number and
  nothing here is verified against the installed build (QUALITY 103).
- **Quotes are tag-stripped token spans.** A row's `quote` cell is the token span
  of the manual text after inline XML elements are removed and whitespace is
  normalized to single spaces; its `line` cell is the token line range that span
  occupies in the snapshot. The counter locates each quote by token position and
  requires the computed range to equal the recorded `line`. Quotes are therefore
  spans, not whole lines, and each is at most 25 words.
- **No live-host measurement.** No `systemctl`, `systemd-analyze`, `pacman` or
  journal read informed any row; the only inputs were the frozen snapshot and the
  frozen expected rows.

## (b) The eight rows

Each row is the companion object's `id`, `directive`, `statement`, `quote` and
`line` cell; `source` is S329 and `snapshot`/`digest` are the frozen snapshot
above for all eight.

| id | directive | statement | quote | line |
|---|---|---|---|---|
| DP1 | `Wants=` | A listed unit that fails to start, or cannot be added to the transaction, leaves the transaction valid and the configuring unit still starts. | "this has no impact on the validity of the transaction as a whole, and this unit will still be started." | 666-667 |
| DP2 | `Requires=` | With or without `After=`, the configuring unit is stopped or restarted when a listed unit is explicitly stopped or restarted. | "Besides, with or without specifying After=, this unit will be stopped (or restarted) if one of the other units is explicitly stopped (or restarted)." | 690-692 |
| DP3 | `Requisite=` | A listed unit that is not already started is not started by `Requisite=`, and the configuring unit's start fails immediately. | "if the units listed here are not started already, they will not be started and the starting of this unit will fail immediately." | 713-715 |
| DP4 | `BindsTo=` | Beyond `Requires=`, `BindsTo=` also stops the configuring unit when a listed unit stops unexpectedly, which includes failure. | "it also does so when a listed unit stops unexpectedly (which includes when it fails)." | 736-737 |
| DP5 | `PartOf=` | When systemd stops or restarts the units listed here, the action is propagated to this unit. | "When systemd stops or restarts the units listed here, the action is propagated to this unit." | 765-766 |
| DP6 | `Upholds=` | While the configuring unit is up, listed units found inactive or failed are started when no job is queued for them. | "as long as this unit is up, all units listed in Upholds= are started whenever found to be inactive or failed," | 783-785 |
| DP7 | `RequiresMountsFor=` | Adds `Requires=` and `After=` dependencies for every mount unit needed to access the specified paths. | "Automatically adds dependencies of type Requires= and After= for all mount units required to access the specified path." | 937-939 |
| DP8 | `After=` | The manual names including a unit in both `After=` and `Wants=` as a common pattern. | "It is a common pattern to include a unit name in both the After= and Wants= options," | 857-858 |

DP8's row is about `After=` because it is the `After=` entry's own text that
names the combined pattern; DP7's row is about `RequiresMountsFor=` because that
directive is what adds the `Requires=`/`After=` pair.

## (c) Requirement versus ordering

The manual separates two orthogonal kinds of dependency, and says so at
`:855-856`: "those settings are independent of and orthogonal to the requirement
dependencies". The ordering pair `Before=`/`After=` only sequences; the
requirement family pulls units into a transaction or propagates actions.

- **Pull or propagate (requirement family).** `Requires=` activates the listed
  units when the configuring unit is activated (`:688`); `Wants=` starts the
  listed units when the configuring unit is started (`:665`); `BindsTo=` adds the
  unexpected-stop propagation to `Requires=` (DP4, `:736-737`); `PartOf=`
  propagates stop and restart actions to this unit (DP5, `:765-766`);
  `Upholds=` continuously keeps the listed units running (DP6, `:783-785`).
- **The family member that asserts instead of pulling.** `Requisite=` is
  described with `Requires=` but does the opposite of pulling: the listed unit
  "will not be started and the starting of this unit will fail immediately"
  (DP3, `:713-715`). It is recorded here as a precondition, not as a pull, so
  that no reader infers that a `Requisite=` unit is started by the transaction.
- **Order only.** `Before=`/`After=` do not pull anything in; ordering is
  configured with them, and requirement dependencies do not substitute for it:
  "requirement dependencies do not influence the order in which services are
  started or stopped" (`:670-671`), so ordering "has to be configured
  independently with the After= or Before= options" (`:671-672`).
- **The combined pattern.** "It is a common pattern to include a unit name in
  both the After= and Wants= options" (DP8, `:857-858`), "in which case the
  unit listed will be started before the unit that is configured with these
  options" (`:858-859`): the requirement directive pulls the unit in, the
  ordering directive sequences it, and the manual notes the two are independent
  (`:855-856`).

## (d) Triage reading — what each directive does not prove

- **A failed `Requires=` start without `After=` does not block this unit.**
  The manual conditions the blocking behaviour on ordering: "If one of the
  other units fails to activate, and an ordering dependency After= on the
  failing unit is set" (`:688-690`), and only then "this unit will not be
  started" (`:690`). Inference from that conditional: without `After=` on the
  failing unit, `Requires=` alone does not withhold this unit's start. The same
  entry states no converse; it recommends "Often, it is a better choice to use
  Wants= instead of Requires=" (`:694-696`). The sweep is limited to that entry,
  not the whole manual.
- **An active unit is not guaranteed by `Requires=`.** "this dependency type does
  not imply that the other unit always has to be in active state when this unit
  is running" (`:698-702`): failing condition checks do not fail the start job,
  and a unit that deactivates on its own does not propagate.
- **`PartOf=` is one-way.** "this is a one-way dependency — changes to this unit
  do not affect the listed units" (`:766-768`). `PartOf=` is also scoped: it
  configures dependencies "similar to Requires=, but limited to stopping and
  restarting of units" (`:763-764`). `PartOf=` propagates stop and
  restart actions inward only; it does not pull units in and it does not carry
  the `Requires=` start semantics.
- **`Upholds=` has a continuous restart effect, subject to the unit rate
  limit.** A `Wants=` dependency "has a one-time effect", while `Upholds=` "has a
  continuous effect, constantly restarting the unit if necessary", and "The
  restart happens without delay, and usual per-unit rate-limit applies"
  (`:785-789`). The same sentence conditions the start on "no job is queued
  for them" (`:785`): the uphold check acts only when no job is already queued
  for the unit. It does not say that no job results. So `Upholds=` is not a
  guarantee of uptime: the rate limit still bounds the restarts.
- **`RequiresMountsFor=` pulls mount units.** It "Automatically adds
  dependencies of type Requires= and After= for all mount units required to
  access the specified path" (DP7, `:937-939`), and a `noauto` mount point is
  "still honored for the purposes of this option, i.e. they will be pulled in by
  this unit" (`:941-944`). Its own framing is that it "Takes a space-separated
  list of absolute paths" (`:936-937`), so the paths must be absolute. It
  pulls the mounts the path needs; it says nothing about the mount being
  mounted successfully.
- **`Requisite=` proves neither start nor ordering.** DP3 (`:713-715`) and
  `:715-717`: it "does not imply an ordering dependency, even if both units are
  started in the same transaction", so `Requisite=` alone does not sequence the
  start either.

## (e) Limits

- **A six-value requirement family plus two helpers, not an exhaustive
  enumeration.** The eight rows cover the six requirement-family directive
  values `Requires=`, `Wants=`, `Requisite=`, `BindsTo=`, `PartOf=`, `Upholds=`
  and the two helpers `After=` and `RequiresMountsFor=`. The same manual also
  documents `Conflicts=` (`:802-804`), `Triggers=`, `PropagatesStopTo=` and
  others; those are outside the frozen eight and no claim is made about them.
- **Hypothetical units.** The manual's own examples (`a.service`, `b.service`,
  `foo.service`, `bar.service`) are illustrative names, not units on this host
  and not units the note claims exist.
- **No live daemon state.** Nothing was observed at runtime. No row states that
  any unit here started, stopped, failed, was pulled in, was ordered, was
  restarted or was rate-limited; the rows are readings of documentation text.
- **No proof of installed-build equivalence.** Upstream v262 tag lines only
  (QUALITY 103). No row is a statement about the installed Arch build, and no
  host-side line number is cited.
- **Reverse-property forms.** `Upholds=` has a reverse property, `UpheldBy=`
  (`:791-793`, and the forward/reverse table at `:2266-2270`), but that reverse
  is an `[Install]`-section symlink creator: `WantedBy=`, `RequiredBy=` and
  `UpheldBy=` "cannot be used directly as a unit configuration setting"
  (`:2328-2331`). `RequiresMountsFor=` has no reverse-property entry at all —
  bounded sweep: `grep -n 'RequiresMountsFor' .ufo/waves/round-79/before/src/systemd.unit.xml`
  over the whole snapshot returns exactly two hits, `:934` (its own definition)
  and `:952` (the `WantsMountsFor=` entry that refers to it), and the
  forward/reverse table at `:2245-2300` contains no `RequiresMountsFor=` row.
  Scope: the one frozen snapshot file; date 2026-11-04. So neither `Upholds=`
  nor `RequiresMountsFor=` has a reverse form usable as a `[Unit]` directive.
- **Not an authenticity system.** A fabricated bundle could satisfy the numeric
  predicate; the companion rows and the source reading remain separate checks.
  Nothing here asserts that the round's claims pass.
- **`S329`'s registry row lands with this entry.** At the round-79 review
  revision `corpus/SOURCES.md` ends at `S328`; the S329 row is appended in the
  same integration step as this note. This entry names S329 and its URL anchor.
- **Lines cited outside the declared S329 anchor ranges.** The ranges named in
  the round-79 declaration are `Wants=` :663-673, `Requires=` :684-704,
  `Requisite=` :713-717, `BindsTo=` :734-748, `PartOf=` :764-772, `Upholds=`
  :783-791, `After=` :855-859, `RequiresMountsFor=` :934-940. Every DP1-DP8
  `line` cell falls inside its own range. This note also cites these lines
  outside those ranges, enumerated here per QUALITY 94: `:720-724`
  (`RequisiteOf=`); `:750-754` (`BoundBy=`); `:763` (the first line of the
  `PartOf=` entry, one line above its registered range); `:773-774`
  (`ConsistsOf=`); `:791-793` (the `UpheldBy=` note, of which only `:791` falls
  inside the registered `Upholds=` range); `:802-804` (`Conflicts=`);
  `:941-944` (the `noauto` clause of `RequiresMountsFor=`); `:952`
  (`WantsMountsFor=`, which refers back to `RequiresMountsFor=`); `:2245-2300`
  (the forward/reverse property table); `:2328-2335` (its closing notes).
  The S329 registry row should extend its anchor ranges over this list.
- **Row quotes are spans.** A row's quote is a token span inside its `line`
  range, not the complete text of the cited line; where the note quotes
  documentation outside a row it gives the complete line text.

## QUALITY check

Section (f) of this entry: the applicable numbered criteria of
`corpus/QUALITY.md`, each with the row, quote and line its statement rests on.
Criteria 1, 2, 3, 7, 9, 66, 86, 94 and 103 are the ones this entry can be
checked against; other criteria in the bar govern other artefact kinds and are
not claimed here.

- **1 — every claim falsifiable or marked opinion.** Each of the eight rows is
  falsifiable against the frozen snapshot: the counter locates the quote at the
  recorded `line` and refuses a mismatch (DP1 `:666-667`, DP2 `:690-692`,
  DP3 `:713-715`, DP4 `:736-737`, DP5 `:765-766`, DP6 `:783-785`, DP7
  `:937-939`, DP8 `:857-858`). The prose readings in sections (c) and (d) are
  readings of quoted text, and the one step that is an inference rather than a
  quoted sentence is marked "Inference" in (d).
- **2 — every claim carries a source anchor.** Every row carries `source=S329`,
  the snapshot name, the snapshot digest and a line range (DP1-DP8 table); every
  prose citation in (c), (d) and (e) gives a snapshot line. No claim rests on
  oral knowledge or on an unpinned file.
- **3 — observation, inference and unknown stay separate.** Observation: the
  eight quoted manual sentences and the reverse-property table rows (`:2245-2300`,
  `:2328-2335`). Inference: only the marked step in (d) about `Requires=`
  without `After=`. Unknown: everything about this host's runtime, the
  installed build's line equivalence, and the directives outside the frozen
  eight — all carried in (e), not asserted.
- **7 — external claims cite an exact S### row with its tier and anchor.** All
  external claims cite S329 (tier A, docs, mined) at
  `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml`,
  the upstream v262 tag. Tier A is the only tier used, so no tier-C sole support
  arises; no local configuration file is cited as an inactive/default source
  because no host file is cited at all. The row is pending this round's landing
  (see (e)).
- **9 — every negative claim carries its bounded sweep, scope and date.** The
  two negative readings are: `RequiresMountsFor=` has no reverse-property row
  (sweep `grep -n 'RequiresMountsFor' <snapshot>` → exactly `:934` and `:952`,
  and none in the reverse table `:2245-2300`; scope: that one snapshot file;
  date 2026-11-04) and the family is not exhaustive (`Conflicts=` `:802-804` is
  present and named as outside the frozen eight; the full directive list of the
  manual was read, and the eight-row set is the round's frozen choice). No
  negative host-state claim is made, so no host sweep is owed.
- **66 — an entry statement keeps every branch its quoted source states.**
  Met by the landed row set, with the correction recorded. The reviewer found
  that the originally frozen DP6 statement dropped the source's precondition
  "and no job is queued for them" (`:785`); the landed DP6 statement carries it,
  which is why the frozen C1 predicate is a declared miss rather than a pass:
  the frozen tuple cannot be widened after data without being a different
  instrument. The other seven statements match the scope of the sentence they
  quote: DP2's "If one of the other units fails to activate, and an ordering
  dependency After= on the failing unit is set" (`:688-690`) and "this unit will
  not be started" (`:690`) are stated in (d); DP5's scope clause "limited to
  stopping and restarting of units" (`:763-764`) and one-way clause
  (`:766-768`) are stated in (d); DP7's framing "Takes a space-separated list of
  absolute paths" (`:936-937`) and `noauto` clause (`:941-944`) are stated in
  (d); DP8's quote ends mid-sentence and its continuation (`:858-859`) is
  carried in (c). No row says "only", "exactly" or "otherwise" where the source
  does not, and where (d) draws a consequence beyond the quoted sentence it is
  labelled as inference.
- **86 — a rule row verifies on an upstream source row, not on an own-work
  capture.** Every row's `source` is S329, whose kind is `docs` and whose
  locator names the upstream v262 artifact `man/systemd.unit.xml`; the entry's
  `source:` line names S329 and no other id, so every id a row cites is named on
  that line. No row is carried by a lane path or an own-work capture.
- **94 — a source-range declaration accounts for every cited line.** The declared
  S329 anchor ranges are listed in (e), together with an explicit enumeration of
  every line this note cites outside them: `:720-724`, `:750-754`, `:763`,
  `:773-774`, `:791-793`, `:802-804`, `:941-944`, `:952`, `:2245-2300`,
  `:2328-2335`. The same list is repeated here so a reader does not have to
  reconcile two versions of it. The row quotes are token spans inside their
  recorded line ranges, and (e) says so where the two differ in kind.
- **103 — an upstream tag line is not a host-build line.** (a) states that the
  line numbers are v262 tag lines of the upstream XML, that the host runs a
  distribution build whose patches may shift lines, and that no line here is a
  host-build line. No row asserts host behaviour, so no host-side line number
  is cited; the `recheck:` line reopens the upstream file at the next tag and
  compares the digest rather than naming an installed-build line.
