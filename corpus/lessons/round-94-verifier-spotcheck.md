# Round 94 verifier spot-check — tsukuroi lane

author: hyaku closure (non-author integrator, @m_zfl)

Lane HEAD before the round: `add107e0cc15a15ac9736e17678831109feb678f`; after: `029f6629ab67402bea2f0651ea104912f948f324`
(cited in the closure brief and re-measured here). Driver digest (copied from the mutable
`.ufo/watchdog.log`): `2026-11-08T03:48:14-03:00 launch tsukuroi round=94 pgid=3007652
driver=hyaku-inline attempt=1`; `2026-11-08T06:28:56-03:00 complete tsukuroi round=94;
hyaku-inline attempt=1`.

## 1. Conformance (step 1)

- **Report landing and attribution**: in the fleet repo, `git log --format='%an %H' --
  .ufo/reports/round-94/tsukuroi.md` → `tsukuroi-shokunin 7e1950158b99f519165f8a42f4ee2bb75af16f6b`.
  Committed by the lane identity, not swept by an integrator. Pass.
- **`SHONEN` heading**: present (`## SHONEN`), four `[~]` lines, one per box, each with a pointer and
  no self-attested `[x]` (the promotion gate stays with the operator). Pass.
- **Cited lane commits**: `git -C …/tsukuroi-shokunin merge-base --is-ancestor <hash> refs/heads/master`
  → `eb3b3e51` OK, `a85796ac` OK, `b6447374` OK, `ef1dd190` OK; the pre-round `add107e0` is an ancestor
  of the tip. All four cited hashes exist. Pass.
- **Clean and pushed**: `scripts/hyaku/jj-lane.sh state tsukuroi-shokunin` →
  `branch=master local=029f6629 remote=029f6629 ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git -C … status --porcelain` → 0 lines; `git ls-remote origin refs/heads/master` → `029f6629…`.
  Pass.
- **Prompt fidelity**: `.ufo/prompts/tsukuroi-round-94.md` (989 lines, committed by
  `tsukuroi-shokunin 650f2da9`) reproduces `templates/round-prompt.md` rendered — `diff` of lines
  1-140 shows **only** `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions — and its hyaku
  addendum carries the rest: mission/axes (§1), the 1-3-claims rule (§2), the frontier step (§2b), the
  L2 floor "at least 8 L2 subagents in ONE batched AgentSwarm call" (§3), the report path and its
  required sections (§4), commit-then-push and push scope (§5), and the L0 side channel (§5). The five
  child-lane items are present: report path/filename (§4), commit-before-report (§5), `SHONEN` heading
  (§4), commit-hash citation (§4 "tied to the commit hash that carries it"), lane write scope
  (addendum item 3, prompt line 448). No L2 route map is quoted in §3 (it routes through the host
  table), so there is no `MISSION.md` bucket mismatch to test. Pass.
- **Marker test**: real report — work performed, per-item evidence pointers, changes tied to `LOG.md`
  ("Round 94 — freeze", "Round 94 — settle"), a checkable commit citation. Status `ok`.
- **Wave shape**: `w1-spec.json` `maxLanes 16`, 14 items; `w1-results.json` 14 seats; 14 seat report
  files under `w1/`; agents = 5 executor, 1 scout, 1 scribe, 1 connector, 2 reviewer, 2 critic,
  2 mutation-tester → 6/14 = 43% attack, 0 dead seats. Inside the run-15 band (8-16) and the L2 floor.

**Conformance defects found here (status-neutral, §6 routes them)**: the wave has no `.ready`
artifact (prior rounds 84-93 all commit `w1.ready` + `w1.ready.dispatched`; r94 has neither); the gate
registry in `SKILL.md` was not updated for the round's new tools; the freeze manifest no longer
verifies at the tip; three count/arithmetic slips in the frozen control sentences (below); the report
cites no commit later than `ef1dd190`, while the lane's final commit is `029f6629`.

## 2. Claims — re-derived by the closure

Commands run inside `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; every number below is re-parsed
from the committed receipts (`case_log` recomputed for error rows), not copied from the report.

### C1 — depth 8 (tied lowest non-retired axis) — **NOT MET as worded; honest stop**

| receipt | runs | verdict | passed | failed_families | case errors |
|---|---|---|---|---|---|
| `after/c1-canonical.json` | 3 | `met` ×3 | 98/98 | `[]` | 0 |
| `w1/ExecReplicate/c1-gate.json` (clone) | 3 | `met` ×3 | 98/98 | `[]` | 0 |
| `after/bend-N01.json` | 3 | `unmet` ×3 | 97/98 | `REFUSAL-VERSIONS-10DIGIT` | 0 |
| `w1/ExecReplicate/N01-x3.json` | 3 | `unmet` ×3 | 97/98 | `REFUSAL-VERSIONS-10DIGIT` | 0 |
| `after/bend-N02.json`, `w1/ExecReplicate/N02-x3.json` | 3+3 | `unmet` ×6 | 97/98 | `AUTO-PROBE-SHAPES` | 0 |
| `after/bend-N03.json`, `w1/ExecReplicate/N03-x3.json` | 3+3 | `unmet` ×6 | 97/98 | `REFUSAL-VERSIONS-10DIGIT` | 0 |
| `after/bend-N04.json`, `w1/ExecReplicate/N04-x3.json` | 3+3 | **`met` ×6** | 98/98 | `[]` | 0 |

Roster measured, not asserted: `FAMILY_ROSTER` in `tools/limine-pin-battery-r94.py` → 98 names, 98
unique (96 + `REFUSAL-VERSIONS-10DIGIT` + `AUTO-PROBE-SHAPES`); the r93 control
`before/controls/do-nothing-battery-r93.py` → 96 names and **0** occurrences of either new family.
The two new families exist and bite: `REFUSAL_DIGIT10` is four X.Y.Z values with one ten-digit
component plus a `12.9.4` positive control (battery 1638, 1687-1694, usage leg 2000-2028), and the
`shapes` fake is the one script `echo "no version here"; echo "Limine 12.9.6-rc1"; echo "Limine
12.9.6" >&2` (battery 1916). Mutant correspondence (`w1/MutDigit10/results-r94.json`): `M01-bound-10`
and `M03-bound-11` are killed by `REFUSAL-VERSIONS-10DIGIT` alone, `M02-no-suffix-guard` and
`M06-read-stderr` by `AUTO-PROBE-SHAPES` alone; `M07`/`M09` survive at 98/98 (disclosed coverage
gaps).

The claim's frozen target includes "N04 `failed_families` is non-empty". N04 reads **`met` 98/98 in
all six runs**, so the kill rule ("`unmet` if any named bend does not read `unmet` in all three runs")
fires. The L1 says the same in the plan A3 (`C1 is NOT met … honest stop`) and in the report. The
round's real gains (two families, four mutant kills, the `--reference` leg) are recorded, not
credited — they are not the declared measure. **Verdict: unchanged** on depth (r84/r88 precedent: a
lane-disclosed falsified instrument is an honest stop).

### C2 — operability 9 (assurance arm; capability `installed-version-probe` becomes the default) — **met**

| receipt | observation |
|---|---|
| `after/live-c2-flagfree.json` | `limine_version 12.9.4`, `limine_version_source probe`, `visibility_era pre-12.9.5`, `rc 2`, `error "conf unreadable: [Errno 13] …'/boot/limine.conf'"` |
| `after/live-c2-root.json` | same version/source/era, `rc 1`, `error null`, `findings ["LP-MISMATCH line 30", "LP-MISMATCH line 38"]` |
| `w1/ExecLive/flagfree-real.json` | flag-free run against the real `/usr/bin/limine` on a scratch conf: `rc 1`, `12.9.4`/`probe`/`pre-12.9.5` — a flag-free rc-1 receipt that does not depend on `/boot` |
| `w1/ExecLive/leg1-probe.json` | three failure shapes (`no version here`, `Limine 12.9.6-rc1`, stderr-only) → probe `None`, and end-to-end `rc 64` / 0 stdout bytes each |
| `after/gate-selftest.txt` | `selftest PASS 39/39` |
| `after/usage-check.txt` | `verdict met`, 15/15 rows ok, incl. `999999999.0.0` accepted (rc 0) and the four ten-digit refusals (rc 64) |
| `after/battery-reference.txt` | `selftest PASS 18/18`, `reference-gate PASS families_passed=98` (the r93-routed `--reference` debt) |

Before leg re-measured: the r93 control's argparse line is
`ap.add_argument("--limine-version", default="12.9.4")` (`do-nothing-gate-r93.py:495`); landed gate
line 503 is `default="auto"`. Host fact re-read by the closure: `limine --version` → `Limine 12.9.4`.
The do-nothing gate on the r94 roster reads `97/98 unmet`, `failed_families ['AUTO-PROBE-SHAPES']`
(`after/dn94-r93gate.json`, `w1/ExecBends/dn94.json`), i.e. the discriminant is
`limine_version_source: flag` vs `probe`, not the selftest tally (the r93 gate also selftests 39/39).
**Verdict: met (evidence-verified; the mechanism is the receipts' and ExecLive's syscall trace, not my
re-execution of the lane's gate).**

**Re-measured vs evidence-verified.** C1 and C2 numbers are re-measures *of the committed receipts*
(fresh parses of every run list, `case_log` error recompute, roster greps, mutant table) plus two host
facts (`limine --version`; upstream bytes). I did not execute `check-limine-pins.py`, the battery, the
bends or the do-nothing controls: Gate standard, Closure consequence — the closure verifies a gate's
committed evidence.

### 2b. Pre-file falsification ledger (addendum §8)

`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tsukuroi --round 94` →
`PREFILE-FALSIFICATION: pass claims=2 rows=14 attack_seats=7 findings=0`, exit **0**. Both claims
covered; all 7 attack seats (6 attack roles + the connector, which the ledger counts as attack) read;
every row's artifact resolves inside `.ufo/waves/round-94/`.

There are **4** `falsifies-wording` rows (`grep -c falsifies-wording claim-falsification.tsv` → 4), not
the "Three" the report says (§6 item 5). Adjudication of each:

| row | real? | ruling |
|---|---|---|
| C1 / `w1/CriticClaims.md` (F2 N04, F3/F4 enumerations, F5 ×3 counterexample, F1 the 102 freeze) | **real** | The N04 sentence is falsified by the round's own receipts (six `met` runs). A3 records it as the honest stop, not as a narrowing around it, and the report files C1 not met. The claim therefore does not verify — correctly declared, not saved. F1's 102 is an erratum served by A2/A3; F3/F4 are plan-prose forks the frozen `claims.json` does not share (I read `claims.json`: its digit10/probe-shape enumerations match the battery). |
| C1 / `w1/ReviewBattery.md` (F1 the `12.9.6.1` shape; F2 the accepted 9-digit boundary) | **spurious as a wording falsification; real as a coverage gap** | The C1 wording enumerates exactly the fake the battery sends (three lines, `-rc1`), so F1 tests a shape the claim never says it sends; F2's boundary is explicitly excluded by the claim ("the healthy `12.9.4` control row inside the same family"). Both are genuine battery-coverage gaps — routed (§6 item 9), not claim-falsifying. |
| C2 / `w1/CriticClaims.md` (F6 the kill sentence vs the unprivileged receipt) | **real** | The frozen kill ("`unmet` if the live receipt carries a non-null `error`") contradicts the very receipt the predicate's parenthetical blesses. It does not fire on the claim's own named receipt (`after/live-c2-root.json`: `error null`, `rc 1`), so C2 still verifies; A3's C2-1 records the field-not-nullness reading. Claim drafting defect, not a false claim. |
| C2 / `w1/CriticForgers.md` (f2: a source-reading forger scores 98/98, so the battery certifies the observable result, not the mechanism) | **real scope note** | The C2 predicate is about the JSON fields, and the mechanism is certified by ExecLive's syscall trace, as the plan/report say. Reconciled by disclosure; nothing in C2's wording claims the battery proves the probe's mechanism. |

The ledger PASS is therefore not a clean bill for the SCORECARD's control sentences: the do-nothing
numbers there are wrong by one family (§2c, §6 item 4).

### 2c. Gate standard (Closure consequence)

- **Self-test tallies verified from committed evidence**: gate `PASS 39/39` (`after/gate-selftest.txt`),
  battery `PASS 5/5` (`after/battery-selftest.txt`), battery `--reference` `PASS 18/18`
  (`after/battery-reference.txt`). Consistent.
- **Frozen run and revision named**: the receipts name `tools/check-limine-pins.py`; the SCORECARD
  names the freeze commit `eb3b3e51` and the instrument digests `7d79ac29…`/`d66b4a59…`/`3855743b…`,
  which match `before/freeze-manifest.sha256` and the tip bytes
  (`sha256sum -c .ufo/waves/round-94/before/instruments.sha256` → all 11 OK).
- **Freeze manifest at the tip**: `sha256sum -c .ufo/waves/round-94/before/freeze-manifest.sha256` →
  11 OK and **`.ufo/plans/round-94.md: FAILED`** (the plan is `5065cc91…` in the manifest, `078b8331…`
  at the tip). The manifest pins the pre-scoring plan; A3's post-scoring append changed it. But A3's
  own sentence says the manifest "still verifies 12/12 against the frozen plan line" — false of the
  bytes that ship it. The claim-void rule binds `instruments.sha256` (11 files, clean), so no receipt
  is voided; the sentence is a defect (§6 item 3).
- **Registry (Gate standard, Delivery/Registry)**: the round adds `tools/limine-pin-battery-r94.py` and
  `tools/make-r94-bends.py`, and `SKILL.md` was not touched this round
  (`git diff --name-only add107e0 029f6629 -- SKILL.md` → empty). `grep -n 'limine-pin-battery-r94' SKILL.md`
  → no row; the operative `limine-pins` row still documents "default `12.9.4`" and "37 fixtures" while
  the gate now defaults to `auto` and selftests 39/39. Per Gate standard, closure grades no gate
  conformant without its registry row → **conformance defect, status-neutral, routed** (§6 item 1). The
  lane's own `registry-coverage` gate (`SKILL.md:2082`, `REGISTRY-ROW-MISSING`) would be red at this
  tip; I name it, I do not run it.

## 3. Discernment spot-check (`corpus/lessons/round-94.md` `## Gate`)

Live sources re-opened by the closure on 2026-11-08; the lane's pinned copies compared byte-wise where
they exist.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S386 Limine `common/lib/config.c` v12.9.6 | admit | `raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/common/lib/config.c` → HTTP 200, sha256 `a940acae3a0a…` | **agree** | The quote `if (p > config_addr) { *(p - 1) = '\0'; }` is at raw 328-330 inside `create_menu_tree`, 10 words. Both v12.9.6 files I fetched hash exactly to the v12.9.5 counterparts (`a940acae…`, `4da21c7c…`), so the row's "byte-identical, the boundary is v12.9.5's code" teaching is exact. |
| S387 Limine ChangeLog v12.9.6 | admit | `…/v12.9.6/ChangeLog` → HTTP 200 | **agree** | The 12.9.6 `Miscellaneous:` block carries "A config whose first line is an entry has had no global options since 12.9.5, whereas every option in it used to count as global. Fixes #700." (15-word quote is a truncation of that sentence, locator correct). A documentation sentence, as the row says. |
| S388 Limine `host/limine.c` v12.9.6 | admit | `…/v12.9.6/host/limine.c` → HTTP 200, sha256 `4da21c7c…` | **agree** | `puts("Limine " LIMINE_VERSION);` at raw 2035, `puts(LIMINE_VERSION);` at 2031, `--version` dispatch 2089-2091. Identical to v12.9.5. |
| S385 Python docs (`-P`/`-I`), the r93 rule-1 row | admit | live `docs.python.org/3.15/using/cmdline.html` → title `1. Command line and environment — Python 3.15.2 documentation`, `id="cmdoption-P"` present; pinned copy `.ufo/waves/round-94/w1/ScoutSource/pins/python-3.15-cmdline.html` → sha256 `d3c50306…` reproduces | **agree, with a freshness caveat** | The ≤25-word title quote and the anchor resolve. A live fetch today is the same 171073 bytes but hashes `c089d660…`: the only diff is the page's own `Last updated on Nov 08, 2026 (07:53 UTC)` line vs the pin's `(06:12 UTC)`. The row is a snapshot pin, not a claim of stable bytes; no correction is owed, but a re-verify will never reproduce the hash. |
| `https://man.archlinux.org/man/limine.8` | reject | live fetch → **HTTP 404** | **agree** | "Page not found — Arch manual pages"; the lane registers no `limine(8)` page. Correctly not evidence. |
| `api.github.com/repos/Limine-Bootloader/Limine/releases/tags/v12.9.6` | reject | live fetch → HTTP 200, body = "Changelog can be found [here](…ChangeLog)" + tarball signing-key text | **agree** | The body states no Limine behaviour; keeping it as a wave-directory locator and not a SOURCES row is the right call. |

**SOURCES census**: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tsukuroi` → exit **0**, `tsukuroi ok …/corpus/SOURCES.md`; 57 `W04`
duplicate-URL warnings and 1 `W01` (`S381`, pre-existing). The three new rows S386-S388 each raise one
W04 of the standing class — three, not the "two new W04s" the report states (§6 item 5). Row count
`git show add107e0:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'` → 385; at the tip → 388.

## 4. Axis verdicts (diff `add107e0…029f6629`)

No axis score moved (`SCORECARD.md`: depth 8, coverage 9, operability 9, freshness 9, calibration 9,
adjacency 8; no retirement). The appended SCORECARD sections add no removed line, `corpus/knowledge/`
146 → 147 with no deletion, and no removed line in `corpus/` at all except the in-place `S385`
`used-by` cell that CORPUS rule 2 allows and the lesson logs old→new.

| axis | verdict | reason |
|---|---|---|
| depth (C1) | **unchanged** | Two sourced families and four mutant kills landed, but the claim's frozen target fails at N04 in all six runs; gains recorded, not credited. |
| operability (C2) | **improved** | `auto` is the default (`check-limine-pins.py:503`), flag-free receipts read `12.9.4`/`probe`/`pre-12.9.5`, the probe refuses rc 64 on three failure shapes, selftest 39/39, usage roster 15/15, `--reference` 18/18. |
| coverage | **unchanged** | No new surface class; the two families extend the owned battery. |
| freshness | **improved** | Upstream pins advanced to v12.9.6 with byte-identity receipts I re-derived (`a940acae…`, `4da21c7c…`), the v12.9.6 ChangeLog's one visibility sentence read, S385's rule-1 row supplied, census exit 0. |
| calibration | **unchanged** | The honest stop and the wave's self-catch are real, but the round froze an undelivered decoy, a `102/102` arithmetic slip that reached `SCORECARD.md`, and a do-nothing count (`96/98`) that no receipt shows; the r93 prose-count correction was not discharged and the same count class recurred. |
| adjacency | **unchanged** | `w1/ConnectorOverlap.md` found no sibling contradiction; the contested kaidoku/revenger RE ownership remains unruled (operator-owned). |

No axis is `harmed`: the 96 r93 families still pass on the landed gate (`after/dn93-r93battery.json` →
`96/96 met`, 384 cases), the census is clean, and nothing was removed from the corpus.

## 5. Trends

- **expansion — improved.** One admitted knowledge entry on ground the coverage map did not hold
  (`corpus/knowledge/limine-auto-default-r94.md`, present with the `source:`/`verified-at:`/`recheck:`
  trio) whose `source:` cites the three `mined` rows opened this round (S386-S388); `knowledge/`
  146 → 147, `SOURCES.md` 385 → 388, census exit 0, README round-94 section + Frontier bullets.
- **quality — improved.** The `installed-version-probe` capability is advanced from opt-in to the
  default with a live receipt; the r93-routed `--reference` leg is closed (18/18, 98 families); the r93
  survivor `M13` class is killed at family level (`M01`/`M03` mutants die on
  `REFUSAL-VERSIONS-10DIGIT`); QUALITY 139 lands with its lesson cite. C1's stop is not counted.
- **discernment — improved.** This spot-check agrees with the gate on all four admits and both rejects
  (§3), each re-opened at source; the attack seats produced four `falsifies-wording` rows and the round
  either narrowed them with a named amendment or stopped the claim honestly — none was filed as met.
  Caveat recorded under calibration: the same prose-count class the r93 closure routed recurred in this
  report.

## 6. Routed defects (the lane fixes these next round)

1. **Gate registry (Gate standard, Registry/Delivery).** Add rows at the `SKILL.md` registry home for
   `tools/limine-pin-battery-r94.py` and `tools/make-r94-bends.py`, and update the `limine-pins` row:
   the default is now `auto` (not `12.9.4`) and the selftest is 39 fixtures, not 37. The lane's own
   `registry-coverage` gate is red at the landed tip (`REGISTRY-ROW-MISSING`); run and cite it after
   the repair.
2. **Wave `.ready` bookkeeping.** r94 commits no `w1.ready`/`w1.ready.dispatched` while rounds 84-93
   do, yet the report says "one `.ready`". Commit the dispatch artifact (or state in the next report
   that this dispatch path carries none) — and give the `WAVE-DONE` line an artifact rather than a
   report-only sentence.
3. **Freeze manifest vs the plan.** A3 says the manifest "still verifies 12/12 against the frozen plan
   line"; at the tip it verifies 11/12 (`sha256sum -c` → `.ufo/plans/round-94.md: FAILED`). Pin a frozen
   copy of the plan under `before/` (or drop the plan from the manifest) and correct the sentence in
   the next round's report; reports are never rewritten.
4. **Do-nothing arithmetic and the stderr clause.** The plan's control sentence and the SCORECARD
   before-cell say the r93 gate reads `96/98 unmet` on the r94 roster and "answers a verdict … for the
   stderr fake"; both receipts say `97/98 unmet`, `failed_families ['AUTO-PROBE-SHAPES']`, and a
   stderr-only fake is refused by the r93 probe exactly as by the V4 probe (`p.stdout` only,
   `do-nothing-gate-r93.py:117`). A3's erratum both restates `96/98` and cites `97/98` in one
   paragraph. Correct the number and drop the stderr clause in the next report.
5. **Report prose counts.** "Three `falsifies-wording` rows" vs the TSV's 4, and "S386-S388 add two new
   W04s" vs the census's three. This is the class the r93 closure routed as its defect 1 (a prose count
   that disagrees with its own artifact); that correction was not discharged this round — carry it.
6. **Final commit not cited.** `029f6629` (claim-falsification path shape, pushed after the report) is
   in no report and no `LOG.md` entry. Name it in the next report; `PROTOCOL.md` forbids rewriting the
   filed one.
7. **r93 routed-item mapping.** The r94 lesson's "Spot-check result" maps r93 routed 1 to "the report's
   table is built from `git log --format`" — routed 1 was the prose-count correction (see D5), not the
   table. Two of its other mappings drift too (routed 5 is closed by `AUTO-PROBE-SHAPES`, not by
   `REFUSAL-VERSIONS-10DIGIT` as the lesson says; routed 4's M12 timeout survivor is not closed). Map
   the queue by its own text, and carry what did not close.
8. **Battery docstring vs its own fixture.** `fam_auto_probe_shapes` says "the stderr shape belongs to
   the gate's selftest, not this family", but the fixture emits `Limine 12.9.6` on stderr (battery
   1916) and `M06-read-stderr` is killed by this family. Also `REFUSAL_DIGIT9` (battery 1684) is
   declared and referenced nowhere — either send it (battery-level accepted boundary) or delete it and
   say the usage roster is the only accepted-side control (ReviewBattery F2).
9. **Coverage gaps to keep on the frontier** (ReviewBattery F1/F2, disclosed): the `12.9.6.1`
   extra-component shape is not exercised at battery level, and an over-strict `<= 8` gate scores
   `met` 98/98 (measured in `w1/MutDigit10/results-r94.json`).
10. **Contested scope** (carried): kaidoku/revenger reverse-engineering ownership is still unruled;
    operator-owned, reported not absorbed.

## 7. Notes for the operator

- Admission: **not admitted** — C1 does not verify as worded and the lane filed it as an honest stop;
  C2 verifies. Status `ok` (a real report with real, committed work).
- `SHONEN.md`: all four boxes are author-side `[~]`. Boxes 1 and 2 look mechanically checkable by a
  non-author (the pointers resolve to `SKILL.md` tables and a logged round-3 task), but box 3 states
  its own gap ("the whole-SKILL post-append no-oral-context retest remains unexecuted and no non-author
  has replayed it") and box 4 carries the unruled contested scope, so the checklist is **not** fully
  checkable as it stands. Promotion stays operator-owned.
