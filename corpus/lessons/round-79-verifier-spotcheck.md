# Round 79 — non-author closure spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed 2026-11-04. Base `9086589a82f221d130ed6711fbe70b85f0d07aea`; delivered
revision `3d329c354d9020c0a1ba9d1ef41b50db12ab562a`. Status **ok**. Verdict
**rejected-honest-stop**: C1 did not meet its frozen predicate and the lane does
not claim admission; C2 verified; no owned axis is harmed. This is not a
promotion, capability or semantic-universality verdict.

Dispatch/completion digest (durable copy of the mutable log lines):

```text
2026-11-04T15:51:26-03:00 launch tsukuroi round=79 pgid=1239933 driver=hyaku-inline attempt=1
2026-11-04T16:54:45-03:00 complete tsukuroi round=79; hyaku-inline attempt=1
```

## Conformance

- Report attribution: `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H' -n1 -- .ufo/reports/round-79/tsukuroi.md`
  returned `tsukuroi-shokunin <tsukuroi@shokunin.local> 2e3ca258849e2d87dee5b4e895edda4c70a0e9fc`,
  committed 2026-11-04 16:54:04 -0300 — after lane tip 16:52:46, so commit-then-report
  ordering holds. The report carries a real round-work hash, not a marker.
- Cited commits: `git cat-file -e <hash>^{commit}` plus
  `git merge-base --is-ancestor <hash> master` (branch ref, never `@{u}`) returned
  6/6 ancestor: `afe1f26128bde87484001cd02ebf11fa524c4059`, `883aae6107cace30795d3163092b08498e8d4b73`,
  `c7dcd241cbdebbbfefebb3141aece97eb237ed3c`, `36336aac07c25cc9c36343e4a57146035b0592aa`,
  `7d5816aa188bc03ef6de630b7d0296495fad2cd0`, `3d329c354d9020c0a1ba9d1ef41b50db12ab562a`.
  Each carries author and committer `tsukuroi-shokunin <tsukuroi@shokunin.local>`.
- Lane state before this artifact:
  `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
  printed `state branch=master local=3d329c354d9020c0a1ba9d1ef41b50db12ab562a remote=3d329c354d9020c0a1ba9d1ef41b50db12ab562a ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` was empty. `git ls-remote origin refs/heads/master`
  printed `3d329c354d9020c0a1ba9d1ef41b50db12ab562a refs/heads/master`.
- Report contract: sections appear in the template order (Work performed; Landed
  changes; Before → after measurements; Sources & frontier; Trend verdicts;
  `## SHONEN`). `grep -c '^## SHONEN'` = `1`; four `[~]` box lines, zero `[x]`.
- Prompt fidelity: `.ufo/prompts/tsukuroi-round-79.md` (812 lines; commit
  `f7eef4ea2045750d0b6e1381989e09d6de50fb96`, lane identity) renders template
  sections 1–5 byte-identically except the documented substitutions
  (`{{FLEET_ROOT}}`, `{{AXES}}`, `{{LANE}}`, `{{ROUND}}`); `grep -c '{{'` = 0;
  §6 hyaku addendum and §7 scratch discipline are present; the L2 floor is quoted
  as ≥8 in one batched call and the wave used 12; the quoted route map is the
  run-15 split (`task.agentModelOverrides` authority), with no `model`/`modelId`
  key in `w1-spec.json` or `w1-dispatch.json` (`grep -c '"model"'` = 0 in both).
- `PROVINCE.md` and `SHONEN.md` are unchanged between base and tip; no promotion,
  capability row or ordinal uplift is claimed.
- Non-blocking deviations, named not smoothed: the wave's 12 seats contain no
  spawned `planner` seat (L1 held the planner role, as the report states), while
  prompt §3 lists a planner in the minimum split; and one of the three scribes
  (`ScribeLesson`) left no binding file, which the lane recorded as
  `R79-SCRIBELESSON-UNSETTLED` instead of reconstructing it.

## Claim re-checks

No lane gate, tool or selftest was executed. The lane instruments' receipts,
selftest tallies and frozen inputs were evidence-verified; the two claims were
re-derived with independent `git show`/`jq`/`awk` readers over committed bytes.

### C1 — depth (eight pinned dependency-propagation rows): **not verified (declared miss)**

- Target absence at base: `git cat-file -e 9086589a…:corpus/knowledge/systemd-dependency-propagation-r79.json`
  fails (`exists on disk, but not in '9086589a…'`), matching the base receipt
  `rows=0 met=0 reason=unreadable:FileNotFoundError` rc 1.
- Landed bytes at the measured revision and at tip:
  `jq '.rows|length'` = `8`; `jq -r '.source'` = `"S329"`;
  `sha256(corpus/knowledge/systemd-dependency-propagation-r79.json)` =
  `1b8f833df5d8138b63b0a9c57fef138d9613679ce62aae28acdc04021cc37d5a` and the
  `.md` = `8c6b3809aca948ccd1080692e71be50d0689870cdae6082cce40dc53d437eaca`.
  Both equal `w1/ReviewDeps/verdict.json`'s `artifact_sha256` / `companion_sha256`,
  and all eight verdicts are `holds`.
- The frozen expected tuple and the landed row differ in exactly the reviewed
  place: `before/expected.json` DP6 says "…are started." while the landed DP6
  says "…are started when no job is queued for them."; the source at
  `:783-785` reads "failed, and no job is queued for them", so the reviewer's
  first-pass `partly-holds` (`w1/ReviewDeps/review-first.md:62`) was correct and
  the landed statement is the faithful one. The frozen tuple was not edited:
  `sha256(before/expected.json)` = `0c09c7a4ad010dd19e99b47940b94030f945498a20b705981b581e308f3add21`
  at the freeze commit `afe1f261` and at tip; the snapshot digest
  `eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6` is
  identical at both, and a live re-fetch of
  `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml`
  returned http 200, 165445 bytes, the same digest.
- **Second blocking leg, not named by the round:** the frozen kill rule (SCORECARD
  r79 C1 row) also requires the review report digest to appear as
  `review_sha256=` in the unique reviewer-role ReviewDeps `w1-results.json`
  result. `jq -r '.results[].output' w1-results.json` is `null` for all 12 seats
  (kernel-restart note), and `tools/measure-unit-deps-r79.py:129` returns
  `result-digest` whenever the result output is not a string. The review-binding
  leg is therefore unreachable independent of DP6; the after receipt's
  `finite-content-mismatch` is only the first failing leg. Recorded as a routed
  defect, not retrofitted.
- Reported `rows=0 met=0` before and after: **agree**; C1 is a declared miss, so
  depth lands unchanged.

### C2 — operability (zero duplicate current rows, two gate-standard rows): **verified**

Independent parser over committed `SKILL.md` bytes (own `awk`/Python reader; the
lane's checker was not imported or run): highest `## Gate and probe registry —
roundN superseding current rows` heading selects the operative table; every
8-column registry table after it is current unless the text between heading and
header carries `NON-OPERATIVE`; one `tools/…` path per row from the entry cell.

```text
9086589a82f221d130ed6711fbe70b85f0d07aea  rows=123  duplicates=6
  check-r72-routed-r73.py, check-r75-routed-r76.py, check-selftest-tally.py,
  count-jd-rows-r76.py, count-ul-rows-r73.py, measure-journal-arithmetic-r77.py
3d329c354d9020c0a1ba9d1ef41b50db12ab562a  rows=119  duplicates=0
```

- The tip has 119 operative rows, 119 distinct tool paths; `git diff … -- SKILL.md`
  adds exactly four `> NON-OPERATIVE` lines and removes none.
- Shape leg: at base `check-r71-routed-r72` and `count-md-rows-r72` carry
  `none: no self-test mode`, the verdict maps have no code 3, and both tool blobs
  contain zero `--selftest` (`grep -c` = 0 each). At tip both rows declare
  `--selftest` in the self-test cell, both verdict maps add "3 self-test failed
  (`--selftest`)", and each tool blob carries `--selftest` and a `SELFTEST` line.
  Shape 0/2 → 2/2.
- Reported `duplicates=6 shape_ok=0/2 met=0` → `duplicates=0 shape_ok=2/2 met=1`:
  **agree**, rc 1 → 0.

### Gate evidence (verified, not executed)

- C1 selftest receipt: `SELFTEST total=32 passed=32 failed=0`, exit 0. C2 selftest
  receipt: `SELFTEST total=8 passed=8 failed=0`, exit 0. The two repaired tools'
  selftests are 8/8 and 23/23 rc 0 with TMPDIR refusal rc 2 and mutated-copy
  red-before rc 3 in `w1/ExecInstrument/receipts.json`.
- Same-run support gates at `36336aac`: `check-registry-coverage` PASS
  `registered=119 rows_total=119 tools_total=119 findings=0`;
  `check-knowledge-refs-r68` `dangling_count: 0`, `finding_count: 0`, 97 notes;
  `check-line-endings` PASS (398 files, 0 violations); `check-knowledge-header`
  keeps two findings on `modprobe-config-plane-r72.md` and
  `module-parameter-plane-r71.md`, both untouched between base and tip.
- Structural counts re-measured over committed bytes: `SOURCES.md` rows
  328 → 329; tiers A 311 → 312, B 6, C 11; status mined 290 → 291, queued 5,
  rejected 33; malformed rows 0; knowledge `.md` 96 → 97; tracked `tools/`
  117 → 119. A single added `S###` line, zero removed.
- Both instruments import the shared `tools/_revision.py` validator
  (`QUALITY 28` routed item addressed for the new instruments; the frozen r78
  counter is not retrofitted). The declared limits — fabricated review-bundle
  acceptance and the data equality leg shadowing per-row quote/line clauses —
  remain disclosed limits of a finite predicate, not closed here.

## Outside discernment spot-check

Sources re-opened live on 2026-11-04; the pinned snapshot digest matches the URL.

| Item | Decision | Re-opened source | Result | Reason |
|---|---|---|---|---|
| S329 admit (A/docs/mined) | admit | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml — http 200, 165445 bytes, sha256 `eb9479be…` | agree | Row written after opening; the located quote at `:659`, `Configures (weak) requirement dependencies on other units.` (7 words), is exact and grounds the teaching; the anchor names tag v262 and the eight keyword ranges, not a bare homepage; `used-by` resolves. |
| `After=` pulls the unit in | reject | Same page `:855`: `Note that those settings are independent of and orthogonal to the requirement dependencies as configured by Requires=, Wants=, Requisite=, or BindsTo=.` (21 words) | agree | The passage states orthogonality; the same paragraph's combined `After=` + `Wants=` pattern shows the requirement directive does the pulling. The flip condition is the right one. |
| `Requires=` guarantees the listed unit stays active | reject | Same page `:698`: `Note that this dependency type does not imply that the other unit always has to be in active state when this unit is running.` (24 words) | agree | Direct contradiction; `Requires=` activates but does not pin active state. |
| `Upholds=` is a one-time pull-in | reject | Same page `:785-787`: `While a Wants= dependency on another unit has a one-time effect when this units started, a Upholds= dependency on it has a continuous effect,` (24 words) | agree | The manual contrasts `Wants=` (one-time) with `Upholds=` (continuous restart), the opposite of the candidate. |

Required census re-run:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
→ exit **0**, final line `tsukuroi ok …/tsukuroi-shokunin/corpus/SOURCES.md`,
W04 duplicate-URL warnings only (including the new S329/S304 shared URL).
Observed decisions: 1 admit + 3 rejects, all agreeing.

## Verdicts

| Owned axis | Verdict | Evidence |
|---|---|---|
| depth | unchanged | C1's frozen predicate is a declared miss (`rows=0 met=0` before and after); the landed entry is faithful but an unverified claim earns no move; ordinal 8 → 8. |
| operability | improved | C2 independently reproduced 6 → 0 duplicates and 0/2 → 2/2 shape, with two real hermetic selftests and truthful registry cells; ordinal 9 → 9. |
| coverage | unchanged | Existing systemd-unit ground deepened; `corpus/README.md` Round-79 says no coverage/frontier promotion. |
| freshness | unchanged | No prior note re-verified or superseded; the new source recheck is `on-release`. |
| calibration | unchanged | The report's own measurement and limits statements match observed state; no calibration move is claimed. |
| adjacency | unchanged | `PROVINCE.md` unchanged; ConnectorScope found no absorbed scope; the inherited ADJ-06/OUT-009 kaidoku/revenger arbitration remains open and is re-flagged, not ruled here. |

No owned axis is harmed. Measured ordinals stay depth 8 / coverage 9 / operability 9 /
freshness 9 / calibration 9 / adjacency 8.

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | unchanged | Rows 328 → 329 and one knowledge note, but it deepens the already-owned systemd-unit surface; no frontier row advanced and no capability entered. |
| quality | unchanged | The new entry landed reviewed and corrected, yet no prior entry was re-verified or superseded, and no admitted entry was found false or left stale. |
| discernment | improved | This non-author spot-check agrees on the one admit and all three rejects (4/4), resolving the lane's pending outside check; the round's own reviewer/critic catches are recorded as lesson rows, not smoothed. |

## Routed defects — tsukuroi round 80

1. **C1 predicate reachability.** The frozen kill rule carries a review-binding leg
   (`review_sha256=` in `w1-results.json`) that the delivered null-output results
   cannot satisfy; the stated miss names only DP6. Either freeze the binding on the
   committed `ReviewDeps/verdict.json` digest (a file the seat writes) or persist the
   seat output before freezing the predicate, and name both legs in `SCORECARD.md`.
2. **Seat-output durability.** `w1-results.json` delivered 12 `null` outputs with a
   kernel-restart note. Bind counters on files the seat writes and keep the result
   file as corroboration, per the run-13 counter rule.
3. **Gate-standard debt.** 36 of the operative table's 93 `gate` rows still declare
   no self-test (`awk` over the round-71 table: `gate=93 none_selftest=36`). This round
   repaired only the two routed rows; continue the sweep or reclassify with a
   justified registry note.
4. **C1 instrument limits.** Fabricated-bundle acceptance and the equality leg's
   shadowing of per-row quote/line clauses stay disclosed limits; do not treat a
   green future run as an authenticity proof.
5. **Planner seat.** The wave ran 12 seats with no spawned planner (L1 held it). Either
   spawn the planner or state the deviation before the wave, not only in the report.
6. **Promotion input (operator-owned).** SHONEN boxes 1, 2 and 4 look checkable from
   committed artifacts by a fresh non-author; box 3's whole-SKILL no-oral-context
   replay remains unexecuted. No `[x]` is written here; promotion is operator-owned.

## Support

Fresh read-only checks; no lane gate, tool or selftest was executed; no model
parameter was passed; no tools were installed or updated. Only this verifier
artifact and the closure `MANIFEST.json` entry are authored by this closure session.
