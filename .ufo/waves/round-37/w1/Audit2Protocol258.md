# Audit2Protocol258 — read-only protocol/source audit, item 2/4 (round-37 w1)

seat: Audit2Protocol258 (scout/audit; L2 leaf; tsukuroi lane round 37 attempt 1, wave w1)
assignment (w1-spec.json item 2/4): inspect one distinct contract surface — scorecard claim
rules, SOURCES contract, assimilation package, quarantine slice, lessons/spot-check
requirements — record actionable evidence-based gaps in this seat file. No lane/fleet/source
writes.
date: 2026-10-25 (UTC via `date -u`; local -03:00 noted where relevant)
axes: operability / frontier / process

## 0. Method / provenance (read-only, nothing installed)

- RULES.md read (`~/.omp/agent/RULES.md`): no tool installed, updated or run by me; no
  pacman/host action; no git/jj/fleet/sibling mutation; no campaign tool; no network URL was
  opened this round — every citation below is a local file (path:line) read this round.
- Reads: `SCORECARD.md` (r37 declaration 1857-1974; r36 outcome 1761-1856; axes tables
  1976-2011; capability tables 2013-2041); `corpus/SOURCES.md` (registry rows S001-S199,
  search log 217-275); `tools/check-self-assessment.py` (K01-K27, lines 1-810);
  `tools/check-registry-coverage.py` (header); `corpus/lessons/round-36.md`,
  `corpus/lessons/round-36-verifier-spotcheck.md` (referenced), `LOG.md:1379`;
  `.ufo/waves/round-37/assimilation/{collisions,reg-ids,staged-ids}`;
  `.ufo/waves/round-37/before/c3-before.json`, `before/c3-before-exit.txt`;
  `.ufo/waves/round-37/after-c3-{d06ced,ee36f9,5124bf,0e5f70}.json`;
  `.ufo/waves/round-37/w1-plan.json`, `w1-spec.json`, `w1-dispatch.json`;
  `w1/Scribe2246.md`, `w1/Scribe8852.md`, `w1/Frontier4Errno428.md`;
  merge package `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/MERGE-REPORT.{md,json}`,
  `SOURCES.append.md` (147 rows), `knowledge/corpus/knowledge/{errno-name-discrimination-r25,
  mount-errno-contract-r26,errno-contract-variance-r37}.md`;
  capture files `/home/vgpnk/Projects/shokuknow/lanes/tsukuroi/round9/{host-errno-capture,
  lane-errno13-probe}.txt`.
- Executed (read-only, lane tool): `python3 tools/check-self-assessment.py --revision
  564db0b614b2914de5452f9ebd537a0653ae1de5` and `--revision 0e5f70fadba12bc9bbb9db564c2262c2c0194535`
  (reads via `git show`; writes only to sandbox temp dirs). No state mutated.

## 1. Findings

### F1 — C3 calibration: before-state reproduced exactly; after-state PASS at HEAD; but the
###      executed repair exceeded the declared "five cells" (scorecard claim rules)
- [OBS] My run at declared base `564db0b614`: `checked 27 / mismatches 5 / status FAIL / exit 1`;
  the five mismatched checks are exactly K07-K11 with stated/observed = 55/56 (notes),
  3009/3110 (SKILL lines), 784/839 (pipe lines), 46/49 (lessons), 256/269 (README lines) —
  identical to the C3 before-state in the declaration (SCORECARD.md:1959-1964).
- [OBS] My run at HEAD `0e5f70f` (declared branch tip): `checked 27 / mismatches 0 / PASS / exit 0`,
  matching the frozen predicate `mismatches == 0 && checked == 27 && exit == 0`.
- [OBS] The wave's own after-receipts show a non-linear repair trace:
  `after-c3-d06ced.json` (2 mismatches, K17+K18, capability rows naming absent paths),
  `after-c3-ee36f9.json` (1 mismatch, K17 "states None cases"), `after-c3-5124bf.json`
  (CANNOT_EVALUATE, missing capability row), `after-c3-0e5f70.json` (PASS). The C3
  declaration scopes the change as "append-only correction of the five current self-assessment
  count cells" and "only the self-assessment values may change" (SCORECARD.md:1962-1968);
  the executed rede simply also edited the *capability* rows (case-count phrase, evidence
  pointers — commits ee36f9e/5124bf3/0e5f70f). The checker bytes and 27-check population are
  unchanged, so the frozen predicate holds, but the declared change scope is narrower than the
  actual change. Actionable: restate the change scope as "self-assessment tables" (axes +
  capabilities), or document the capability-row edits as separate review-driven repairs before
  outcome scoring.

### F2 — C2 counter absent at base; "before at base = exit 1" not executable pre-change
###      (scorecard claim rules / operability)
- [OBS] `tools/check-journalctl-v262-corrections.py` (C2 counter, SCORECARD.md:1914-1919)
  does not exist at base, in `git log --all` history, or in the worktree; the change commit is
  what introduces it. The declared counting command `python3 tools/check-journalctl-v262-corrections.py
  --revision <REV>` therefore cannot produce "before at base = exit 1" at freeze time (the
  freeze commit precedes the change commit per the order at SCORECARD.md:1943-1948). It is
  reproducible only *after* the change, by pointing the new counter at the base revision, or
  via an undeclared draft harness. Actionable: state in the declaration that the before-value is
  measured post-change with `--revision <base>`, or commit the counter before the before-battery.

### F3 — Two competing "current" round-37 axes tables (scorecard claim rules / maintainability)
- [OBS] SCORECARD.md carries two `## Axes — current self-assessment (round 37)` tables
  (lines 1976 and 2000) with different phrasings and values; the first is stale relative to the
  second and carries no visual supersession marker. `check-self-assessment.py` passes because it
  parses only the *last* `## Axes - ` table (docstring lines 13-16). A human or non-positional
  reader citing the first "current" table gets wrong counts. Actionable: label superseded tables
  explicitly (e.g., "superseded") or remove the first table after the re-derivation is landed.

### F4 — Assimilation package ground truth: merge package exists outside the lane; declared rows
###      match the three entries (assimilation package / SOURCES contract)
- [OBS] The merge package is at `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/`
  (not inside the lane): `MERGE-REPORT.md` reports 147 proposed rows accepted, 0 refused,
  70 knowledge entries, first staged id S200; `SOURCES.append.md` carries 147 rows S200-S346.
- [OBS] The ten declared rows exist in `SOURCES.append.md` and correspond exactly to the three
  staged knowledge files' `source:` lines: S204/S205 → `errno-name-discrimination-r25.md`;
  S214/S220 → `mount-errno-contract-r26.md`; S279-S282/S286/S287 →
  `errno-contract-variance-r37.md`. `MERGE-REPORT.md` used-by pointer corrections (S279-S282,
  S286/S287 → errno-contract-variance-r37.md) match.
- [OBS] Collision guard state: `.ufo/waves/round-37/assimilation/collisions` is empty;
  `reg-ids` = S001-S199 (current registry), `staged-ids` = S200-S346 — disjoint, so
  "collision-guard proven" is consistent with observable state.
- [OBS] The two own-work captures cited by S286/S287 exist at
  `/home/vgpnk/Projects/shokuknow/lanes/tsukuroi/round9/{host-errno-capture,lane-errno13-probe}.txt`
  with content matching the rows (EACCES 13/EROFS 30; probe 0 matches, 6 retained boots).

### F5 — Partial admission deviates from the merge package's own adopt contract; 137 accepted
###      staged rows have no deferral record (SOURCES contract / process)
- [OBS] `MERGE-REPORT.md` Adopt checklist step 3 says "Append `SOURCES.append.md` to
  `corpus/SOURCES.md`", i.e., all 147 rows; the round-37 declaration admits only 10 rows
  (one theme, SCORECARD.md:1936-1941). The other 137 accepted staged rows are neither admitted,
  refused, nor explicitly deferred anywhere in the lane. Actionable: record the deferral (or a
  per-row disposition) in the change commit, so a later round does not treat the package as
  fully consumed.
- [OBS] Adopt checklist step 1 references `SOURCES-PROPOSED.md` ("read every `## Gate` evidence
  block"); that file exists neither in the lane nor in the merge package (glob: no match).
  Actionable: provide the file or drop/rewrite the step.

### F6 — Quarantine slice: declared but no artifact; per-row verdicts unverifiable
###      (quarantine slice / lessons-spot-check requirement)
- [OBS] The declaration states "Quarantine slice (12 data rows) hand-checked with a verdict per
  row" (SCORECARD.md:1940). No such artifact exists: `.ufo/waves/round-37/assimilation/`
  holds only `collisions`, `reg-ids`, `staged-ids`; a find over `.ufo/waves/round-37/` yields
  no quarantine/verdict file. Sibling-lane convention stores these slices and verdicts in the
  same assimilation dir (e.g., round-68 kotoba: "13-row quarantine slice ... hand-checked
  (7 payload-absent refused, …)", `.ufo/reports/round-68/kotoba.md:16`). As written, the
  hand-check claim cannot be audited. This also leaves the r36 gate requirement to record
  considered-and-rejected candidates (round-36-verifier-spotcheck §6 item 4) unattested.
- Actionable: produce `assimilation/quarantine-slice.md` with the 12 row ids, per-row verdict,
  and reason before the change commit, or amend the declaration.

### F7 — S286/S287 source paths resolve outside the lane repo (SOURCES contract)
- [OBS] The own-work rows S286/S287 anchor `lanes/tsukuroi/round9/*.txt`; those files exist
  only under `/home/vgpnk/Projects/shokuknow/lanes/...`, not under the lane root, so appended
  verbatim the anchor is unresolvable from the lane unless the sources-registry contract
  officially allows out-of-repo fleet paths (precedent exists: S030 uses an absolute path).
  Actionable: state the resolution rule for fleet-relative `lanes/` paths in the row or in
  `corpus/SOURCES.md` Paths.

### F8 — Lessons/spot-check routing: mapped defects present; LOG stamp typo still unrepaired
###      (lessons/spot-check requirements)
- [OBS] Round-36 verifier spot-check §6 routed defects 1-4 all map to declared r37 work
  (C1 S1/S3/S4 + source-param; C2 15-vs-16 terms/-F-vs-N/action-override; LOG stamp typo).
- [OBS] The declared LOG-stamp repair ("repaired by a LOG append", SCORECARD.md:1865) is not
  yet present: `LOG.md:1379` still reads `2026-10-24T04:4043Z`. Mid-wave, expected at change
  commit.
- [OBS] No `corpus/lessons/round-37.md` yet (expected at outcome per the order at
  SCORECARD.md:1943-1948); not a gap at this wave stage.

## 2. Gates / touched surfaces / out-of-scope

- Gates: wave spec/plan/dispatch consistent (64 seats, one batched task call). Census/sources
  gates not run by me.
- Touched surfaces: read-only lane files in §0; merge package read-only; no writes anywhere; no
  tool installed (RULES.md read; nothing to record); no delegation/background/wave spawns.
- Out-of-scope: no network URL opened; no probe/census execution; C1 V8 probe and mutants not
  inspected (do not exist yet, mid-wave); no verdicts on other seats' claims.

## 3. Artifact paths / limits

- This report: `.ufo/waves/round-37/w1/Audit2Protocol258.md`
- Key evidence read: paths in §0; receipts `before/c3-before.json`, `after-c3-*.json`;
  `assimilation/{collisions,reg-ids,staged-ids}`; merge package files.
- Limits: wave mid-flight (most w1 seats unfiled; final measured tip not fixed); C1 freeze/
  mutants pending; quarantine-slice verdicts absent; no live network re-open of staged source
  URLs (rows inspected as packaged, not re-fetched).
