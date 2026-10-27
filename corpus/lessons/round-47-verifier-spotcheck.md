# Round 47 — verifier spot-check (tsukuroi, hyaku run 10)

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-27
scope: lane tip `91601905…` → `4c0475ba…` (report); lane tip at closure `76819197…`
(orchestrator salvage of w1 seat reports, lane identity, on `origin/master`).

## 1. Step-1 conformance

| Check | Result |
|---|---|
| Report committed by lane identity | `git log -- .ufo/reports/round-47/tsukuroi.md` → `90369c70` author `tsukuroi-shokunin <tsukuroi@shokunin.local>` — PASS |
| `## SHONEN` heading, one line per box | 4 boxes, all `[~]` with pointers — PASS |
| Cited commits exist + ancestry | `3629c46a 77e9e2b2 e31070a9 f6bc6d05 c5397574 e1567211 31efd304 4c0475ba` all exist, all `merge-base --is-ancestor … master` — PASS |
| Lane pushed, no leftovers | `jj-lane.sh state` → `ahead=0`, `local=remote=76819197` on `origin/master` (ls-remote confirms). `status --porcelain`: 2 untracked files `.ufo/waves/round-47/w1/C1MutBinding/{mutant-M09-wrong-snapshot-quote.py,summary-M09-wrong-snapshot-quote.jsonl}` — receipts of a seat still live after the orchestrator salvage; DEFECT (left uncommitted, file before WAVE-DONE) |
| Prompt fidelity | `.ufo/prompts/tsukuroi-round-47.md` carries the canonical §1–5 contract + all five child-lane items + run-6..run-10 addenda; L2 route map matches the operator's run-10 map — PASS |
| Report is a real report, not a marker | Work performed, evidence pointers, landed changes tied to LOG entries, before→after, Sources & frontier, Trend verdicts, SHONEN, Stale-lane, wrap-limitation all present — status `ok` |

## 2. Claims — re-measured vs evidence-verified

Both claims rest on lane-owned frozen counters; per §Gate standard (closure
consequence) I verify committed evidence, never re-execute the sibling's gates.
Byte-level facts were re-derived directly.

**C1 / depth — admit GR1–GR3 with amended GR2: NOT VERIFIED (agree).**
Committed frozen receipt `after/c1-final-unsettled.jsonl` at revision `31efd304`:
`structural_ok=1, quotes_ok=3, verdicts_ok=0, marks_ok=0, FAIL` — matches the
report byte-for-byte. `w1-results.json` (64 results) exists only via the
post-report salvage commit `76819197`; at the measured revision the counted
cohort was unbound. K22 map defect verified: `controls/k22-s240-map.txt` prints
`(False, 'ioctl.c not a pinned snapshot file')` for `S240 ioctl.c:3190`.
Spot-read of salvaged `w1/R47CritGR2a.md` (commit `76819197`): verdict `partly`,
misattribution confirmed against its quoted dev-replace.c lines — the counted
critic's correction text is what the working-tree GR2 now carries.

**C2 / operability — selftest passes under spaced TMPDIR: target met, kill rule
fired — NOT VERIFIED (agree).** Committed receipt `before/selftest-space-after.txt`:
`TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)`, rc 0. The
before-state receipt `before/selftest-space-before.log` named in the report is
NOT committed (`ls before/` shows only 3 files); the before-state is still
corroborated by committed `controls/battery-summary-r47.jsonl` C2-K0
(`FAIL (162 cases, 13 passed, 149 failed)`, as expected). Byte check
`tools/tsukuroi-census.sh:2048-2057`: `st_base=${TMPDIR:-/tmp}`; on refused
characters `st_base=/tmp` — the frozen kill rule (no new hardcoded `/tmp` write)
fires on the implementation itself. Claim fails; fix routed (lane already
mined it as `R47-C2-TMPDIR-FALLBACK`).

**Control battery:** committed `controls/battery-summary-r47.jsonl` — 12 lines,
every `as_expected: true` (C1: K0/K1/K22a/K23a/F1a/F1b/F2a/F3a/K-pass; C2:
K0/K2/K-pass) — evidence-verified.
**GR2 amendment byte check** (`corpus/knowledge/btrfs-scrub-grounding-r45.md`
GR2): now attributes `btrfs_scrub_cancel` to `btrfs_dev_replace_cancel` ioctl
handling a suspended replace (`dev-replace.c:1126-1144`) and explicitly states
the unmount suspend path only sets SUSPENDED — matches the counted critic's
prescribed correction. Accuracy improved in committed bytes; the admission
itself stayed unsettled at the frozen measurement.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | unchanged | C1 predicate unmet; GR2 corrected in bytes but admission unsettled; ordinal unchanged |
| operability | unchanged | selftest now 164/164 under spaced TMPDIR but kill rule fired on `/tmp` fallback (routed defect); no admission |
| calibration | unchanged | round-46 self-corrections (C1 unverified, census-identity withdrawn, verdicts_ok 1) all landed honestly in SCORECARD + LOG; no new mis-assessment found this round, but Gate's missing reject section keeps the score unmoved |
| coverage | unchanged | no surface moved (SCORECARD diff read) |
| freshness | unchanged | S251 re-opened live and locator widened (72-81 → 72-81,84) fixing a stale citation — routine upkeep, no ordinal move |
| adjacency | unchanged | IN-109 anchor corrected 2582→2593 (`f6bc6d05`) |

No axis harmed. No `unprovable-but-better`: both claims were measured claims,
not exploratory, and both missed their frozen predicates.

## 4. Spot-check (LEARNING.md — outside discernment)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| Gate admit S252 — mktemp(1) man7 | admit | live fetch `curl https://man7.org/linux/man-pages/man1/mktemp.1.html`, sha256 `74186433…073266` byte-identical to `frozen/src/mktemp.html` and the row's pin; located quote "if DIR is not specified, use $TMPDIR if set, else /tmp" present verbatim at raw HTML lines 94-99 | AGREE | row schema parses (11 cols), tier A docs, anchor exact, quote ≤25 words, used-by resolvable |
| SOURCES.md S252 row quote check | — | same re-open | AGREE | located quote ≤25 words (14), verbatim substring of snapshot lines 94-99 |
| Assimilation refusal (proxy reject — see defect R47-V1) | refuse-all | `.ufo/waves/round-47/assimilation/{collisions,reg-ids,staged-ids}`: 53 collisions (S200–S252), 252 registry ids, 147 staged ids — `wc -l` matches report | AGREE | §10 contract: nonempty `collisions` → nothing appends; refusal is the correct disposition; the `  \| S252 \|` indented-guard fixture caught S252, proving the guard works |

**Gate defect:** `corpus/lessons/round-47.md` `## Gate` records one admit and
`(none yet — updated at integration)` under reject rows — the round closed with
NO recorded reject, so the non-author sample lacks a gate reject. This is a
frontier-step conformance defect (routed below). The assimilation refusal was
used as the reject proxy.

## 5. Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | unchanged | no knowledge entry admitted; registry 251→252 rows is curation, not expansion (CORPUS rule 4) |
| quality | unchanged | real correctness fix landed (GR2 clause, selftest space handling) but C2 kill rule fired on the committed implementation and C1 admission unsettled |
| discernment | unchanged | Gate recorded no rejects; spot-check agrees on the admit and on the assimilation refusal, but with no gate reject to check the agreement record is partial — defect routed |

## 6. Conformance defects noted (status-neutral)

- R47-V1: `## Gate` has zero reject rows at wrap — the round closed without a
  gate rejection on record; next round must record ≥1 reject (a refusal counts).
- R47-V2: report cites `.ufo/waves/round-47/before/selftest-space-before.log` —
  the file is not committed (before-receipt missing; before-state corroborated
  by the battery C2-K0 line instead).
- R47-V3: report says "two W04 duplicate-URL warnings" for the end census; the
  committed `after-sources-census.txt` shows 40 W04 lines (exit 0, ok — warning
  count misstated, not the verdict).
- R47-V4: report filed before WAVE-DONE w1 (operator wrap instruction);
  orchestrator salvage commit `76819197` landed the seat reports + w1-results.json
  post-report; 1 seat (C1MutBinding) still live, 2 receipt files untracked.
- R47-V5: Godspeed directive bytes trimmed in w1-dispatch.json (lane-mined
  `R47-GODSPEED-DIRECTIVE-BYTES`).

## 7. Routed defects for the lane's next round

1. Remove the `/tmp` fallback in `run_selftest` (scratch-discipline §7.4 +
   C2's own kill rule): derive a whitespace-free alias inside the supplied
   TMPDIR or fail safe — lane already mined as `R47-C2-TMPDIR-FALLBACK`.
2. Add S240 `ioctl.c` snapshot + digest to the r47 counter's pinned map
   (`R47-K22-S240-MAP`, receipt `controls/k22-s240-map.txt`) before the next
   claim freeze.
3. Settle the w1 cohort: `w1-results.json` is now committed (64/64 outputs via
   `76819197`); C1MutBinding's mutant-M09 receipts are still untracked — land
   or discard them at the next round's start under inherited-state rules.
4. Record a gate reject row in the next lesson's `## Gate` (R47-V1).
5. Re-run the C1 admission counter against the now-settled cohort before
   re-declaring GR1–GR3 admission; the corrected GR2 bytes still need a
   counted residual re-read.

## 8. Verdict

`rejected-honest-stop`: real report, all conformance satisfied or noted, both
claims honestly reported unverified, no axis harmed. `admitted=false`,
`lanes.tsukuroi=ok`.
