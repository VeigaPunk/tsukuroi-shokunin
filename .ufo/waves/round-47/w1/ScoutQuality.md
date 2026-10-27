VERDICT: supports

Seat: ScoutQuality (F-6, QUALITY.md sweep). Wave w1, lane tsukuroi-shokunin, freeze revision
`77e9e2b2e96b85d8f048ae2087e246a542b71611`, base `916019057147d7e9ba6b137647b2cee26decf4b8`.
Scope: which numbered criteria in `corpus/QUALITY.md` the amended GR2 row
(`corpus/knowledge/btrfs-scrub-grounding-r45.md`), the new counter
(`tools/check-scrub-admission-r47.py`) and the TMPDIR fix (`tools/tsukuroi-census.sh`) touch, and
whether the current state complies. Receipts: `.ufo/waves/round-47/w1/ScoutQuality/sweep-receipts.txt`.

Sanity anchors (receipt lines 1-14):
- Frozen counter digest at `77e9e2b2` = `e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b`, matching the declared pin.
- `git diff 77e9e2b2 HEAD` over the entry, the counter and the census script is empty: the counted freeze bytes are intact at HEAD `f6bc6d05`.
- The two new GR2 quotes verify on the pinned snapshots: `.ufo/waves/round-44/frozen/src/scrub.c:3094-3095` reads `if (btrfs_fs_closing(fs_info))` / `return -EAGAIN;`; `.ufo/waves/round-45/frozen/src/dev-replace.c:1143-1144` reads `/* Scrub for replace must not be running in suspended state */` / `btrfs_scrub_cancel(fs_info);`.

## Named criteria

### 5 — "A rejection is kept, not silently dropped." — COMPLIANT (integration pending)
- The rejected pre-amendment GR2 wording survives: the entry's `## Limits` records what the round-46
  counted residual critic rejected (`.ufo/waves/round-46/r1/V46ResCritGR2.md`) and that the amended
  row was re-read by the counted round-47 seats (entry `## Limits`, last bullet).
- `corpus/lessons/round-47.md` keeps its three round Mistakes rows (R47-FRESHSTART-THREE-REJECTS,
  R47-C2-DIGEST-TRUNCATION, R47-GR2-AMENDMENT-CLASS); its `### Reject rows` reads
  "(none yet — updated at integration)" (lines 33-35). No rejection exists yet this round; the
  section is in place. Obligation: the L1 must complete it at integration if any candidate is refused.

### 8 — "[unknown] sweep; source:/verified-at:/recheck: on every knowledge entry." — COMPLIANT
- Entry header carries `source:` (S246-S249, S242/S243/S244/S237), `verified-at: 2026-10-27` and
  `recheck: on-release` with the exact re-measure commands.
- The only `[unknown]` string in the entry is inside its QUALITY-check prose describing the sweep
  itself (line 247); no `[unknown]` is kept in any row.

### 9 — "Every negative claim includes its bounded search/probe sweep command, scope and date." — COMPLIANT
- GR2's negative host claims anchor `capture.txt:1` (uid/CapEff) and `capture.txt:9` (devid list);
  the bounded sweep is `capture.sh` — its commands are recorded verbatim (id, /proc/self/status,
  sysfs devinfo listing; no package-manager binary) and its first output line carries the UTC date
  (2026-10-27). GR3's "no package owns that drop-in" rests on the sweep of
  `/var/lib/pacman/local/*/files` (capture.sh lines 18-22; capture.txt:5). The TMPDIR fix makes no
  host claim. The amendment did not alter any host reading.

### 10 — "Before a correction commit, sweep every mention in README.md, SKILL.md and corpus/knowledge/." — COMPLIANT
- The amended GR2's superseded sentences ("A suspended replace requests the cancellation of its
  scrub", "Both refusals come after the function has allocated") appear nowhere in `corpus/`,
  `SKILL.md` or `README.md` outside the entry itself (grep, receipt lines 30-32).
- The TMPDIR fix updated its own normative text in the same commit (3629c46a): the header comment
  (tsukuroi-census.sh:411-412) and the `--selftest` usage line (:602) now state the /tmp fallback.
  Remaining `tsukuroi-r3-2-selftest` mentions elsewhere (e.g. SKILL.md:1301) are historical
  round records describing past state, not superseded normative text. No Markdown table was touched
  by the amendment (the GR2 statement and Quote lines are prose; column counts unchanged — the
  3629c46a diff shows no table lines).

### 12 — "An absent tool does not make its mechanism unknown: read and cite its upstream source." — COMPLIANT
- The new mechanism wording (the filesystem-closing `-EAGAIN` check leading the ordering) is pinned
  by two new Quote lines to the digest-checked S242 snapshot, verified verbatim above; the narrowed
  suspend sentence keeps its dev-replace.c:1143-1144 quote.

### 86 — "A rule row verifies on an upstream source row, never on an own-work capture alone." — COMPLIANT
- GR2's rule content cites upstream rows S242 (scrub.c), S243 (sysfs.c), S247 (dev-replace.c); the
  own-work row S249 appears only in the Host reading beside them, carrying host values (capture.txt
  line anchors), exactly the separation criterion 86 requires. Same pattern in GR1/GR3.

## Counter / verdict / binding criteria (from the `counter|bind|verdict` grep)

### 38 — "Bind reviews to candidate bytes." — COMPLIANT
- Verdicts bind only when the seat's `SECTION SHA256:` equals the counter's SHA-256 of the row's
  bound extent recomputed from the entry bytes at the measured revision
  (check-scrub-admission-r47.py `section_hashes`, `bind`).

### 72 + 73 — "A counter is offered as proof only after should-fail cases" / "the battery's count is the measure." — COMPLIANT
- `.ufo/waves/round-47/controls/battery.py` + `battery-summary-r47.jsonl`: 12 controls, every
  `as_expected: true` (receipt lines 38-41), matching the freeze commit message "controls battery
  12/12" (e31070a9). The freeze commit also fixed two battery rows after the 77e9e2b2 F1 closure
  (F1a's expect/observed semantics; C2-K0 re-measured against the base census). The SCORECARD
  declaration names this battery as the receipts.

### 77 — "A revision-cited gate or measurement is admissible only with a committed receipt naming that revision and the tool digest." — PARTIAL (flagged; precedent-consistent)
- The round-start before receipt `.ufo/waves/round-47/before/c1-before-base.jsonl` is a single raw
  counter JSON line: it names `revision`/`base` but has no run-receipt.py envelope (no
  `tool_sha256` header, no `exit_code` footer). LOG.md:1672-1682 cites it for the "C1 before-state
  at base" measurement. Round 46 set the same raw pattern (`round-46/before/c1-before-base.jsonl`)
  and its spot-check verified "committed receipts" without requiring the envelope. I did not find a
  round-47 receipt with the full envelope (grep for `tool_sha256` under `.ufo/waves/round-47/`
  finds none). The letter of criterion 77 is unmet for the before-state citation; the lane
  precedent treats these raw outputs as receipts. L1 decision needed at integration.

### 84 — "A one-line machine grammar echoes only validated tokens." — COMPLIANT
- The counter prints one JSON line with a closed key set; the census's `TSUKUROI_CENSUS:` /
  `TSUKUROI_CENSUS_SELFTEST:` grammars are untouched by the TMPDIR fix (the R47-C2 pinning cases add
  only fixed ok/bad counter lines).

### 88 — "A counter's acceptance implies the declaration's named content parameters, with a control that violates exactly one." — COMPLIANT
- Declaration names concrete parameters (SCORECARD round-47 table): the row extent bound to the
  expected next header; the 8-seat per-row universe; 164 = 162 + 2 cases; the six (R46-C1) cases
  kept; the `--identity` line shape. Each pre-data control violates exactly one: F1a (inner `## `
  line), F1b (duplicated `## GR2`), F2a (negating marks), K22a (nonexistent citation), K23a
  (byte-identical bodies), F3a (deep-nested dispatch JSON), C2-K2 (guard removed, pinning cases kept).

### 93 — "A counted verdict binds through a channel the counted seat writes verbatim." — COMPLIANT
- The binding channel is the seat's own report file: first line `ROW GR<n> VERDICT: …`, second line
  `SECTION SHA256: …`, both written verbatim by the seat. The SCORECARD C1 row declares this before
  data ("bind verdicts as the first two lines of their own reports"). A lost or malformed
  orchestrator record fails binding (exactly-one dispatch hit, exactly-one results entry; F3a
  exercises the malformed-record leg). Because binding is not through an orchestrator record, the
  yield-shape arms (JSON `verdict` key, preamble text, JSON-encoded string, null) are not required
  here; the counter names its counted wave in the `WAVES` const.

## Adjacent obligations the three artifacts also touch

- **60 — undisclosed in-place edits (PENDING integration):** the base→head sweep
  `git diff -U0 91601905 HEAD -- SCORECARD.md LOG.md SHONEN.md SKILL.md PROVINCE.md corpus/ | grep -E '^-[^-]'`
  prints removed lines in exactly two files: `corpus/knowledge/adjacency-anchors-r19.json` (2571 —
  the f6bc6d05 found_line rewrite caused by the R47-C2 census edit) and
  `corpus/knowledge/btrfs-scrub-grounding-r45.md` (11 — the pre-wave GR2 amendment at 3629c46a).
  Both are disclosed in their commit messages; the round-47 lesson must list them (and re-run the
  sweep over each consecutive commit pair) at integration.
- **61 — Gate record for new source rows (COMPLIANT):** S252 (mktemp(1)) has its Gate record in
  `corpus/lessons/round-47.md` `## Gate` with URL, access date 2026-10-27 and a ≤25-word located
  quote; SOURCES.md row S252 names tier A, `mined`, opened 2026-10-27.
- **70 — registry row (GAP, pending):** `tools/check-scrub-admission-r47.py` landed without a
  registry row; the highest operative table is `## Gate and probe registry — round46 superseding
  current rows` (SKILL.md:4467). The row and `check-registry-coverage.py` exit 0 are owed at the
  round's last lane commit.
- **91 — adopted text checked against the source (COMPLIANT):** the amendment adopts the counted
  round-46 residual critic's exact correction; its quotes verify on the pinned snapshots (above)
  and the amended row is re-read by the counted round-47 seats.
- **28 — one revision implementation (OBSERVATION):** the counter resolves `--revision` inline via
  `git rev-parse --verify <rev>^{commit}` rather than importing `tools/_revision.py` — the identical
  pattern in the r45/r46 counters of this family (check-scrub-admission-r46.py:213). Inherited
  convention, not introduced by this wave; noted for the L1.
- **82 — fixture-gated counter scored outside fixtures (IN FLIGHT):** the C2 kill rules carry the
  live-host leg (live census output digits-stripped byte-identical base vs final); seats
  C2ExecKillRules / C2ExecSelftest / C2ExecRerunA are dispatched for it.

## Not done
- I did not run `tools/check-registry-coverage.py` (a missing row is already visible by inspection;
  the round's last commit has not landed).
- I did not re-run the census selftest or the admission counter (cost guard; the battery and
  before-receipts already record their runs).
- Consecutive-commit-pair sweep for criterion 60 (per the R26 clarification) is the L1's at
  integration; base→head is recorded above.
