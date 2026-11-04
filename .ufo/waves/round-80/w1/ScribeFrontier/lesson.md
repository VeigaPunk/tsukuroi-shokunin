# Round 80 — restart documentation matrix and two gate self-invocation repairs (lesson draft)

Draft for the L1's `corpus/lessons/round-80.md`, written by seat
**ScribeFrontier** (wave w1). Format follows the round-79 lesson. Nothing in
the registry, `SKILL.md`, `LOG.md`, `SCORECARD.md`, `corpus/knowledge/` or
`corpus/lessons/` was edited by this seat.

Base `467a9b7891a5939dab8460ec6f591fbb16bd82e9`; frozen claim commit
`61ec89ec6e6f284b6fba2127721359e6931a5789`. Axes judged: **depth** and
**operability**. L1 holds the planner seat. C1 works depth (8, lowest
non-retired); C2 works operability (9). Neither claim pre-claims an ordinal
uplift, a coverage promotion or a capability.

C1 opened systemd v262 `man/systemd.service.xml` (upstream tag, not the
installed Arch build) and froze the 42-cell restart matrix (six exit causes ×
seven `Restart=` settings). The pinned snapshot is
`.ufo/waves/round-80/before/systemd.service.xml`, SHA-256
`12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44`; the
frozen expected object is SHA-256
`05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153`. C2 gives
two named tools real hermetic `--selftest` invocations with byte-bound
receipts.

## Gate

The page was opened before the freeze and pinned byte-exact:
`https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml`
→ `.ufo/waves/round-80/before/systemd.service.xml`, SHA-256 `12770f86…f66d44`.
Quotes below are located in the tag-stripped, whitespace-normalised snapshot by
token position (the round-79 instrument's own rule); every line number is an
upstream **v262 tag** line, not an installed Arch build line, and every quoted
span occurs exactly once in the 1977-line file. Occurrence counts and the
re-derivation receipts are in
`.ufo/waves/round-80/w1/ScribeFrontier/derivation.md`.

| Row / candidate | URL, access date, located quote (at most 25 words) | Decision / reason / flip |
|---|---|---|
| S330 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml ; 2026-11-04, :877-878: `Configures whether the service shall be restarted when the service process exits, is killed, or a timeout is reached.` | admit, tier A/docs/mined for the `Restart=` settings-to-exit-cause matrix and the conditions that qualify it only: the six-cause × seven-setting table at :913-994 (title :914, header :920-929, six cause rows :932-991), the clean-exit definition :889-897, the no-restart-after-stop sentences :881-882 and :996-1000, the `RestartPreventExitStatus=` / `RestartForceExitStatus=` overrides :1108-1109 and :1140-1141, the `Type=oneshot` exclusion :909-911, and the start rate limiting :1004-1006; 42 finite cells over documented semantics, not a live-host reading and not an installed-build equivalence claim |
| `Restart=always` restarts the service even after an operator's `systemctl stop` | same page, :999-1000: `the service is stopped with systemctl stop or an equivalent operation.` | reject: the page makes an explicit stop an exception to every setting, and separately says a death resulting from systemd operation is never restarted (:881-882) — so `always` cannot be read as "always". Flip: a located upstream passage stating that an explicit `systemctl stop` does not suppress the restart under `Restart=always` |
| `Restart=always` is accepted for `Type=oneshot` services | same page, :909-911: `Type=oneshot services will never be restarted on a clean exit status,` / `always and on-success are rejected for them.` | reject: the page rejects `always` and `on-success` for `Type=oneshot` outright, and `RestartForceExitStatus=` cannot override that for a success status (:1144-1146). Flip: a located upstream passage stating that `Restart=always` is allowed for `Type=oneshot` |
| `Restart=on-watchdog` restarts the service after an unclean exit code | same page, :906-907: `the service will be restarted only if the watchdog timeout for the service expires.` | reject: `on-watchdog` is scoped to the watchdog timeout alone; the table's `Unclean exit code` row (:942-951) marks no `on-watchdog` cell. Flip: a located upstream passage stating that `on-watchdog` also covers unclean exit codes |
| `RestartPreventExitStatus=` suppresses restarts caused by `ExecStopPost=` or `ExecReload=` processes | same page, :1126-1128: `this setting has no effect on processes configured via ExecStartPre=, ExecStartPost=, ExecStop=, ExecStopPost= or ExecReload=,` | reject: the option binds only the main service process; helper processes are outside it, so the override is narrower than "any status". Flip: a located upstream passage stating that the option applies to those helper processes as well |

S330 is a new row; no existing row's status, recheck or used-by changes. The
registry's 33 `rejected` rows and round 79's three Gate rejections stand
unchanged and are kept, not dropped (QUALITY 5). Id-collision caveat,
recorded and not smoothed: the read-only staged package
`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` already uses
the bare id `S330` for a different document (an own-work mirror changelog
capture; the package used `S329` for the same file). The package is not
adopted, no bytes are copied, and the lane registry is not renumbered — the
id is a document-scoped label, so the resolution is document context, never
arithmetic renumbering. **Assimilation: none; no package rows adopted; no
rows changed yet.**

**Landing status at the time of this draft.** The C1 review verdict exists
(`w1/ReviewMatrix/verdict.json`, six `holds`, bound to the final data and
companion digests), and the two companion drafts exist in the wave tree
(`w1/ScribeMatrix/data.json`, `w1/ScribeMatrix/note.md`) — but `S330` is **not
yet in `corpus/SOURCES.md`**, and the companions are **not yet landed** at
`corpus/knowledge/service-restart-matrix-r80.{json,md}`. The C1 count stays 0
until the row and both companions land together; the drafted row in
`ScribeFrontier/source-row.txt` is shaped to the frozen instrument's parser
and to the census's `E11`/`E12` rules so that the landing step needs no
further edit.

## Mistakes

| Class / id | Evidence | Captured-by | Fix shown able to fail |
|---|---|---|---|
| vacuous — R79-C1-EQUALITY-SHADOWS-DEEP-LEGS, still live in round 80 | r79: `w1/MutationCounter/matrix.json` survivors `c1-seven-rows-rowcount` and `c1-no-line-check` (`verdict: survived`); `tools/measure-unit-deps-r79.py:97` | QUALITY 81 (a scripted non-reader must read below the target) and QUALITY 87 (a counter reads the content it credits) | r79's frozen equality leg made `quote-location` and `row-shape` unreachable for data-side perturbations, so the per-row checks it named were answered by equality instead. **Round 80 repeats the shape at `tools/measure-round80.py:41-46`:** C1 evaluates snapshot digests → matrix equality (`matrix-mismatch`) → registry row (`source-row`) → review binding (`review-binding`), so a data-side perturbation dies at `matrix-mismatch` and never reaches the two deeper legs. `before/controls.json` shows exactly that split: `wrong-restart-cell` → `matrix-mismatch`, `forged-review` → `review-binding`; the two kills are mutually exclusive, so no single control exercises both. Declared limit, inherited not repaired: the frozen instrument is not editable this round. |
| source-entailment — R80-C1-NO-SOURCE-LEG (the r79 DP6 shape, re-measured) | `tools/measure-round80.py:41-46` — no leg compares the matrix to `before/systemd.service.xml`; `before/expected.json` is the sole content reference | QUALITY 81 (a depth row counts only with a committed non-author verdict) and QUALITY 66 (a row keeps every branch its quoted source states) | r79's DP6 defect was a frozen row statement that dropped the source's precondition ("and no job is queued for them"), which made the frozen C1 tuple a declared miss. Round 80's frozen object has the same class of exposure in a different place: `before/expected.json` carries only six cause labels and 42 booleans, so the conditions that qualify the table (manual stop :881-882/:996-1000, `RestartPreventExitStatus=`/`RestartForceExitStatus=` :1108-1109/:1140-1141, `Type=oneshot` :909-911, rate limiting :1004-1006) live only in the companion note. The scorecard says so ("Conditions … belong in the companion"), so the exposure is declared — but it is an exposure, not a closed hole: a reader of the JSON alone reads "always restarts on all six causes" without the exceptions. Mitigation is the companion plus the S330 `teaches` cell, and the independent re-derivation below. |
| reference-drift — R80-TABLE-HEADER-VS-PROSE-ORDER | measured: table header :920-929 orders the settings `no, always, on-success, on-failure, on-abnormal, on-abort, on-watchdog`; the prose enumeration at :885-886 orders them `no, on-success, on-failure, on-abnormal, on-watchdog, on-abort, always` | QUALITY 94 (a cited range accounts for every cited line) and QUALITY 2 (a claim carries a measured anchor) | The same page states the same seven settings in **two different orders**. The frozen expected object follows the *table* order. A re-derivation that read the prose sentence instead of the table header would transpose six of seven columns — and would look entirely plausible, because both lists contain the same seven tokens. This is the r79 DP6 class (a frozen statement that can be mis-derived because the source says the same thing twice in two orders) caught before the freeze, not after it. The fix is in the derivation receipts: the table is parsed structurally, the header row is read from the XML, and the derived rows are compared against `expected.json` as an independent check rather than assumed. |
| independence — R80-C1-ARTIFACT-EQUALS-ANSWER-KEY | measured: `w1/ScribeMatrix/data.json` SHA-256 `05abbf14…65153` is byte-identical to `before/expected.json` (as the seat was instructed) | QUALITY 81 (a scripted non-reader must read below the target) and QUALITY 87 (a content counter reads the content it credits) | The reviewed artifact's content is fixed by the frozen answer key, so a reviewer who reads `expected.json` to learn "the" matrix reads the answer key, not the source. Source entailment therefore has exactly one entrance: the reviewer must go to the pinned XML. This seat did that independently and read-only — the six table rows were parsed structurally out of the pinned bytes and the derived `settings` list and `rows` array are deep-equal to `expected.json` (42 cells, 18 marked true, 24 false) — but that is corroboration from a scribe, not the non-author verdict the predicate requires. The frozen counter only checks that the review file has six `holds` plus two digests, so a fabricated bundle passes; the scorecard admits this. |
| source-inconsistent-companion — R80-COMPANION-COLUMN-DIVERGENCE (independently reproduced) | ReviewMatrix's report (`.ufo/waves/round-80/w1/ReviewMatrix.md` §"Resolved before final C1 verdict") records that an earlier companion revision claimed the `on-abnormal` and `on-abort` columns "differ in exactly one place"; this seat measured it from the pinned bytes and confirms the claim was false: the two columns differ in **three** rows — `Timeout` (:968 vs :969), `Watchdog` (:978 vs :979), `Termination due to OOM` (:988 vs :989) — with the other three rows agreeing | QUALITY 94 (cited ranges account for every cited line) and QUALITY 66 (a row keeps every branch its quoted source states) | The failure was caught before the verdict, and the corrected companion was re-reviewed; the earlier failing review is preserved at `w1/ReviewMatrix/review-8a99e339.json` and is not promoted to a passing review. The generalisable defect is worth keeping: a *count* of divergences ("exactly one place") is a claim about the whole matrix, and a reviewer who checks only the rows named in the sentence cannot falsify it — the sweep has to enumerate all six rows. This seat's own receipts now enumerate all six rows with the line of every individual `<entry>` cell, so the same false count is falsifiable in one pass. |
| landing — R80-S330-USED-BY-E11 | `scripts/sources-census.sh` `usedby_findings` — a `mined` row's used-by paths must exist on disk; the census emits `E11` otherwise, and `E12` for a registry-shaped row outside `## Registry` | QUALITY 99 (a correction is re-derivable) and the round-80 census pattern | S330's used-by names two files this wave produces (`corpus/knowledge/service-restart-matrix-r80.md` and `.json`). If the row lands before either companion, the census reads `E11`; if the row lands outside the `## Registry` table, it reads `E12`. Both are ordering constraints on the L1's integration step, not defects in the drafted row. The drafted row was checked against the counter's own parser (exactly one line whose first cell is the id `S330`, 13 pipe-split fields, `kind=docs`, `tier=A`, `status=mined`, URL in the source cell, `corpus/knowledge/service-restart-matrix-r80.json` in the used-by cell) — the row shape is right; the landing order is the L1's call. |
| scope — R80-C2-STATIC-RECEIPT-NO-RERUN | `tools/measure-round80.py:49-62` — C2 checks the receipt's `tool_sha256`/`argv`/`rc`/`passed`/`failed` and greps the tool blob for `--selftest`/`SELFTEST`; it never re-executes the tool | QUALITY 87 (a counter reads the content it credits) and QUALITY 100 (a PASS counts each record it claims to check) | The C2 gate is a receipt-binding gate, not an execution gate: a fabricated receipt with the right shape and a matching digest passes without any selftest running. This is inherited from the frozen instrument and is disclosed rather than repaired. The receipts themselves do carry real execution evidence from the two executor seats (argv, rc, per-case stdout, and a red-before mutation control), which is why the receipts are the binding artifacts and the counter's static read is corroboration only. |

## Seat harm

| Round | Harmed seat | Causing seat | Evidence class | Effect | Fix |
|---|---|---|---|---|---|
| 80 | — | — | none observed by this seat: no kill signal, `pkill`/`killall`, or write outside a seat's own tree appears in any round-80 w1 seat report read by this seat (`ConnectorScope.md`, `ExecKR.md`, `ExecTransaction.md`, `ExecHost.md`, `ScoutSource.md`, `ScribeMatrix.md`, `ReviewMatrix.md`) | entries: none of the destructive kind observed (the round's `w1-results.json` does not exist yet, so the wave settlement is **PENDING**, not "none happened"); the two review-driven interactions below are recorded as resolved interactions, not as harm | none required |
| 80 (latent, not an incident) | ReviewMatrix (and ScribeMatrix) | ScribeMatrix | coupling identified by ConnectorScope's report §6 and independently visible in `tools/measure-round80.py:41-46`: C1 binds `artifact_sha256` and `companion_sha256` of the two landed companions | If ScribeMatrix edits `corpus/knowledge/service-restart-matrix-r80.{json,md}` after ReviewMatrix has hashed them, the counter aborts with `review-binding` (exit 1) even though the content is correct | ReviewMatrix hashes the final bytes; any later edit voids the binding and forces a re-issue, exactly as r79's `ReviewDeps`/`ScribeNote` row required. Recorded as a risk here, not as an observed harm. |
| 80 (review finding → author amendment → re-review, resolved) | ExecKR | ReviewMatrix | review disclosure in `w1/ReviewMatrix.md` (medium finding on `_selftest_env` copying ambient `os.environ`, then the PATH-inheritance concern, then the final resolution) | The reviewer's static finding on the KR selftest's environment isolation was notified to the author; the author replaced the environment copy with an explicit allowlist, pinned `PATH`, withdrew an unsupported confinement claim, and re-ran the selftest (10/10 green, rc 0) plus the red control (rc 3) under a new digest `908592d2…8ac97d` | ReviewMatrix re-read the amended copy at :152-176, independently calculated the final tool digest and matched it against the renewed receipt, and recorded that no unresolved actionable isolation finding remains. The earlier failing C1 review (`review-8a99e339.json`) is preserved, not promoted. Recorded as a *resolved* interaction, not an open harm. |
| 80 (author correction before the verdict, resolved) | ScribeMatrix | ReviewMatrix | review disclosure in `w1/ReviewMatrix.md` ("Resolved before final C1 verdict — companion source contradictions") and independently reproduced by this seat | An earlier companion revision asserted that the `on-abnormal` and `on-abort` columns "differ in exactly one place" (false: three rows) and described OOM as marked like `Unclean exit code` (false: OOM's marked set equals `Timeout`'s) | The author corrected the companion; ReviewMatrix re-reviewed the final bytes and issued six `holds` bound to the final digests. This seat independently re-derived both claims from the pinned XML and confirms the corrections are right (`ScribeFrontier/derivation.md` §3b). |

## QUALITY check

This is the author's explicit check, not an admission.

- **1, 2, 3 (falsifiable / sourced / observation vs inference vs unknown):** every
  Gate row names S330, a located quote with its upstream tag line, and a
  measured occurrence count; the teaches cell is a reading of those lines.
  Live-host claims are absent. The one `[INFERENCE]` in this draft is labelled
  as such: the OOM row's `on-abnormal` cell is read as "the kernel-killed
  process is an unclean signal", which the page does not state in those words
  — the row's `on-abnormal` cell is stated, the mechanism behind it is not.
- **5 (a rejection is kept, not silently dropped):** this round's four
  rejections carry a reason and a flip condition; round 79's three rejections
  are carried forward by reference and explicitly not re-judged; the
  registry's 33 rejected rows are untouched.
- **7 (external claims cite an S### row with tier and anchor):** the only
  external claim in the draft is S330 (tier A, `docs`, anchor = the pinned
  v262 snapshot with its digest and line ranges). No claim rests on an
  own-work capture.
- **9 (a negative claim carries its bounded sweep):** each rejection is
  refuted by a located upstream sentence; the sweep that located every cited
  span is recorded with its scope (the whole 1977-line file, tag-stripped,
  token-exact) and its counts, in `ScribeFrontier/derivation.md`. The
  rejections are claims about documentation semantics, not about any host.
- **14 (a QUALITY check is performed, not promised):** this section.
- **66 (every branch of the quoted source is kept):** the S330 `teaches` cell
  carries the table *and* its four qualifying condition groups; the frozen
  JSON carries only the booleans, which is why the companion carries the
  conditions and why R80-C1-NO-SOURCE-LEG is recorded above as an open
  exposure rather than smoothed away.
- **80 (do-nothing controls show the target can fail):** the round's own
  `before/controls.json` holds eleven controls, including the actual base
  C1 0/rc1 and C2 0/rc1 and negatives for wrong cell, forged review,
  answer-copy-without-review, wrong interface and stale receipt. This seat
  read that file; it did not re-run it.
- **81 (a depth row counts only with a committed non-author verdict):**
  ReviewMatrix has issued `.ufo/waves/round-80/w1/ReviewMatrix/verdict.json`
  with the three required keys and six `holds`, bound to
  `artifact_sha256 05abbf14…65153` and `companion_sha256 1aae7b2a…67a0b`; the
  earlier failing review is preserved separately and not promoted. This seat
  issues no verdict and claims none. The independent re-derivation recorded
  here is corroboration from a scribe, explicitly not a substitute for that
  verdict.
- **86 / 94 (upstream source row; cited ranges accounted):** the row's kind is
  `docs` and every cited line lies inside the ranges the anchor cell
  declares; the anchor cell lists each range it relies on.
- **96 (a counted seat writes its binding file first):** this seat wrote
  `.ufo/waves/round-80/w1/ScribeFrontier.md` as its first write, before any
  deep derivation, and deepened it at the end.
- **103 (an upstream tag line is not a host-build line):** every line number in
  this draft is a v262 tag line in the pinned snapshot; the row and the
  companion both say the matrix is documentation, not installed-build or
  live-restart behaviour.
- **110 (per-round seat-harm tally):** the `## Seat harm` table is present
  above with an explicit empty verdict, its evidence source named, and the
  settlement marked PENDING because the wave results file does not exist yet.
