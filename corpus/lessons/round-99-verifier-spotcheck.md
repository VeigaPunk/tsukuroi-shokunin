# Round 99 verifier spot-check — tsukuroi lane (non-author integrator)

author: hyaku closure (non-author integrator, @m_zfl)

Lane `tsukuroi-shokunin` (operability + freshness), campaign hyaku, round 99, attempt 1.
Pre-round tip `f107da3afe511f7db8cdc30235a992b774903158`; freeze
`dd86287fd97592f24424e7de7c5461c599d3a754`; settle
`778f15fd8d56ca4fa61f1cd6d4b124271c9dfe23`; ledger
`efe5ba590b4a974958b911782ff71ad4ecfb90e9` (= lane `master` at closure).
Dispatch digest (`.ufo/watchdog.log`): `2026-11-08T10:45:14-03:00 launch tsukuroi round=99
pgid=2061128 driver=hyaku-inline attempt=1`; `2026-11-08T11:45:20-03:00 complete tsukuroi round=99;
hyaku-inline attempt=1`.

## 1. Conformance

- Report present at the contracted path and committed by the lane identity:
  `git log --format='%an <%ae> %H' -- .ufo/reports/round-99/tsukuroi.md` →
  `tsukuroi-shokunin <tsukuroi@shokunin.local> 814806fd65b7dd1937df2c857e310bfd46c9a3bb` and
  `… 7d4888341314f68afff0d6c59a1ef1f18aa199ac`. The second commit is an append-only correction of
  the cited tip (5 lines changed); the first-filed bytes are not rewritten. Pass.
- Every cited lane commit exists and is an ancestor of the lane branch ref (not `@{u}`):
  `git -C tsukuroi-shokunin merge-base --is-ancestor <hash> master` → YES for `dd86287f`,
  `778f15fd`, `efe5ba59`, `f107da3a`, `270ca298`, `5eb475cd`, `b492f17f`. Pass.
- Lane clean and pushed: `scripts/hyaku/jj-lane.sh state` →
  `branch=master local=efe5ba59 remote=efe5ba59 ahead=0 behind=0 head=detached tracked=0
  untracked=0`; `git -C tsukuroi-shokunin status --porcelain` → empty (before this spot-check file,
  which is the only path this closure writes). `git ls-remote origin refs/heads/master` →
  `efe5ba59…`. Pass.
- `SHONEN` heading at report line 139 with one line per box: four `[~]` lines, each carrying a
  resolvable evidence pointer; no `[x]`. `SHONEN.md` is byte-identical between
  `f107da3a` and `efe5ba59` (`git diff --quiet` → identical), so no non-author mark was written.
  Pass; the four boxes look checkable by a non-author from the cited evidence (see §8 note).
- Report contract: sections in order — Work performed (claims named first), Landed changes (each
  tied to a LOG entry and a commit), Before → after measurements (counting command + measured
  commit), Sources & frontier, Trend verdicts, `## SHONEN`; real report, not a marker (evidence
  pointers throughout, no placeholder text). Pass.
- Prompt fidelity: `.ufo/prompts/tsukuroi-round-99.md` (committed `dcc0e666`) is the rendered
  `templates/round-prompt.md` §1–§5 plus the hyaku §6 addendum and §7/§8 additions. It carries the
  MISSION/AXES binding, 1–3 claims on distinct axes with the lowest-axis obligation, the frontier
  step (SOURCES contract v1, census command, mined mistake, sourced claim), the L2 floor (≥8 in one
  batched swarm, role split, host route table, Godspeed lead), the report contract (path, section
  order, SHONEN, marker rule), commit/push scope and the L0 side channel. Pass.
- Wave: one v1 wave, 14 seats (`w1-spec.json` `maxLanes` 16, items 14); `w1-dispatch.json`
  `counts {"spawn":14,"resume":0,"total":14}`; `w1-validate.err` 0 bytes; 14 result records, none
  dead. Roles: 5 executors, 2 scouts, 2 scribes, 2 reviewers, 1 critic, 1 mutation-tester,
  1 connector — attack roles 4/14 = 28.6 %, connector 1 (limit 2). Pass.
- Misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain` → 11 paths at closure
  (other lanes/orchestrator `.scratch`), none naming `tsukuroi` or `round-99`. Nothing copied or
  deleted. Pass.

Status-neutral defects (routed in §7): the LOG round-99 headings still read `(pending)` and
`(pending-settle)` after the round settled; the census receipt records the before count but not the
before command's exit code; S395's anchor groups the two new `LIE_KINDS` members under one byte.

## 2. Prefile falsification ledger (addendum §8, Amendment 59)

`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tsukuroi
--round 99` → `PREFILE-FALSIFICATION: pass claims=2 rows=23 attack_seats=5 findings=0`, exit 0
(live re-run by this closure). The ledger `.ufo/waves/round-99/claim-falsification.tsv` has 23 rows
(C1 12, C2 11), covers both claims in `claims.json`, and reads all five attack seats:
`ReviewBattery`, `ReviewRegistry`, `CriticClaims`, `MutRegistry`, `ConnectorOverlap`. Six rows are
`falsifies-wording`; each names an amendment:

| Ledger row | Finding | Amendment | Closure adjudication |
|---|---|---|---|
| C1 `w1/ReviewBattery-9/receipts/09-lie-wording-summary.txt` | both metadata assertions disabled still read `unmet 100/105` / `98/105` | A7 | Real and reconciled: the lie-kind layer detects a field lie somewhere in the roster, not a per-family assertion; the per-family witness is the `Md`/M4 bend, re-read here (Y `check_era` removal makes N09 read `met 105/105`). |
| C1 `w1/ReviewBattery.md` | W1 roster-fit echo and W2 text-first-component era read `met 105/105` | A8 | Real and reconciled: the field closure is roster-finite and the X leg is a near-twin; A8 names both limits and the report/SCORECARD use the narrowed sentence. |
| C1 `w1/CriticClaims/receipts/17-b03-on-lieversion-runs1.txt` | Z `check_echo` removal still reads `unmet 94/105` with Z 4/4 green | A7 | Real and reconciled by the same A7 narrowing; re-read the receipt, counts match. |
| C2 `w1/ReviewRegistry.md` | five forged cell classes still read PASS on r99 | A1 | Real and reconciled: A1 narrows the capture to the measured classes and names the surviving alphabet limits (space/`;`/`+`/`/`/`and`, hybrid+clean, prose span, letter suffix) as r100 frontier. |
| C2 `w1/CriticClaims/receipts/10-xv2-space-extra.txt` | `VARIANTS N01-N03 N05` reads `PASS 7/7` | A1 | Real and reconciled by A1's named limits; the two committed fixtures (`hybrid`, `restated`) are unaffected and both fail closed. |
| C2 `w1/MutRegistry/receipts/C5-selftest.txt` | an ancestor case forced always-ok survives alone (`PASS 17/17`) | A2 | Real and reconciled: A2 states the `ancestor` case pins one branch; the compound M07 probe (skip the check and call the real CLI) kills it, and the pristine probe reads rc 2 `CANNOT-EVALUATE`. |

No failing row was left unreconciled and none is spurious. The related third-change finding
(battery/checker payload `schema` token `…-r97-v1` → `…-r99-v1`, plus the checker's tempdir rename
and one unreachable fixture sentinel) is not a ledger row but is reconciled by A4; the filed report
and SCORECARD use the narrowed "two behaviour-bearing changes" sentence, which the r98→r99 diff
supports (see §3).

## 3. Per-claim re-checks (committed evidence; no sibling gate executed)

Instrument integrity, run by this closure: `cd tsukuroi-shokunin && sha256sum -c
.ufo/waves/round-99/before/instruments.sha256` → **16 files OK**, rc 0. The gate
`tools/check-limine-pins.py` is `7d79ac29…` both in the working tree and at `f107da3a` (`git show
f107da3a:tools/check-limine-pins.py | sha256sum`), so the gate is byte-unchanged. The r98 battery
`8198bd84…` and r98 checker `5bb1441e…` equal their committed do-nothing controls.

### C1 (depth) — verified

Command run by this closure: a Python pass over the ten committed C1 battery artifacts
(`w1/ExecGateRuns/c1-gate-{canonical,clone}.json`, `w1/ExecBends/c1-bend-{N09,N11}-{canonical,clone}.json`,
`w1/ExecDoNothing/dn-{gate,n09,n11}-{canonical,clone}.json`, `w1/ExecGateRuns/c1-lie-{limine-version,visibility-era}.json`),
reading per run `verdict`, `families_passed/families_total`, `failed_families`, `cases`, and the
number of non-null error rows.

Observed: landed gate canonical `met 105/105 [] cases 420` ×3 and clone `met 105/105 [] cases 420`
×3, 0 error rows; N09 `unmet 104/105 [REFUSAL-VERSIONS-9DIGIT-Y]` ×3 both layouts, 0 error rows;
N11 `unmet 103/105 [EXPLICIT-VERSION-ERA, REFUSAL-VERSIONS-9DIGIT]` ×3 both layouts, 0 error rows;
do-nothing r98 control gate and N09 `met 105/105 []` ×3 both layouts and N11
`unmet 104/105 [EXPLICIT-VERSION-ERA]` ×3 both layouts, 0 error rows; `lie-limine-version`
`unmet 93/105` (12 failed families incl. X/Y/Z) and `lie-visibility-era` `unmet 95/105` (10 families
incl. X/Y/Z), 0 error rows. `--selftest` (no reference) receipt
`w1/ExecGateRuns/c1-selftest.txt` → `selftest PASS 5/5`; the reference leg was not run and is not
claimed (A6a). Roster `FAMILY_ROSTER` = 105 (re-derived from `tools/limine-pin-battery-r99.py`;
`CASES_PER_FAMILY` 4 → 420 cases).

Source re-derivation on the committed bytes: `c.check_echo = True` at bytes
79015/79893/81666/83173/84390 and `c.check_era = True` at 79039/80414/81690/83197/84414 —
the X family at 79015/79039 and the Y family at 81666/81690; `def meta_ok` at 99305, the echo
assertion at 99430 and the era assertion at 99523; `LIE_KINDS` gains `limine-version` (108455) and
`visibility-era` (108473). The r98→r99 instrument diff carries the two behaviour-bearing changes
(X/Y flags, two lie kinds) plus docstrings, the inert payload `schema` rename and no other
behaviour change (A4). The bends `diff-N09.txt`/`diff-N11.txt` are one changed line each against
the gate, keyed on the second/first component `999999999` respectively.

**C1 met as narrowed.** The literal frozen predicate's "exactly two changes" is narrowed by A4; the
reported target (landed gate, both bends, both controls, both lie kinds, selftest 5/5, instrument
digest gate) re-derives from committed bytes.

### C2 (freshness) — verified

Committed evidence re-read (no gate re-execution): `w1/ExecRegistry/c2-content-tip.json` and the r98
twin → `status PASS`, `bindings 7`, `findings []`, `rows 160`, `revision f107da3a…`; landing receipt
`before/c2-content-tip-f107da3a.json` agrees. `r99-selftest.txt` → `PASS 17/17` (cases include
`span-hybrid`, `span-restated`, `ancestor`); `r98-selftest.txt` → `PASS 14/14`. Hybrid fixture:
`fx-r98-hybrid.json` `PASS 7/7` → `fx-r99-hybrid.json` `FAIL` with exactly one
`RC-CELL-MISSING` at `SKILL.md:10`; restated: `PASS 7/7` → `FAIL` with exactly one
`RC-CELL-AMBIGUOUS`. M07 mutant on r99 → `selftest FAIL 16/17`, only `ancestor` red, rc 1, where
r98 reads `PASS 14/14` rc 0; the real two-branch probe reads pristine rc 2 `CANNOT-EVALUATE` and
mutant rc 0 `PASS` (`ancestor-probe-{pristine,mutant}.txt`). Coverage:
`w1/ExecRegistry/coverage-tip.json` and `before/r99-d1-coverage-tip-f107da3a.txt` →
`PASS`, `findings []`, `registered 160`, `rows_total 160`, `tools_total 160`; the r98-settle
`270ca298` receipt and the r97-settle `157/157` re-derivation are committed under `before/`.

Source re-derivation: the `RC-BEND-SPAN` binding is
`VARIANTS (N[0-9]+(?:-N[0-9]+|(?:,N[0-9]+)+))(?![0-9,-])` with `"unique": True`
(`tools/check-registry-content-r99.py` line 281–282); the ambiguity branch is at lines 339–340;
the selftest fixtures are registered at lines 498–499. The r98→r99 diff carries the guard, the
`unique` mark, the three selftest cases, and the inert schema/tempdir/one-dead-sentinel changes
(A4). **C2 met.**

### No axis harmed

`git diff f107da3a efe5ba59 -- SCORECARD.md` is a pure append (Round 99 declaration + measured
rows; 52 added lines, 0 removed); no axis score line is edited. `PROVINCE.md` and `SHONEN.md` are
byte-identical between the tips. The r98 battery, r98 checker and the gate keep their bytes and read
`met 105/105 []` / `PASS 7/7` / `PASS 160/160` as controls. `corpus/` is additive: one new knowledge
entry, one new lesson, one new SOURCES row, one README section; no knowledge entry is removed or
falsified. No harm found.

## 4. Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| depth | improved | C1 verified: the X/Y families now assert the two reported fields their clauses name, the Y-only era lie flips `met 105/105` → `unmet 104/105`, and both new lie kinds make the battery read unmet. Score unchanged at 8 (tied lowest), so no ordinal inflation. |
| freshness | improved | C2 verified: the guarded `unique` capture fail-closes the hybrid and restated shapes (r98 `PASS` → r99 `FAIL`, one frozen finding each), the ancestor case kills M07, and the tip/settle coverage receipts re-derive. Score unchanged at 9. |
| operability | unchanged | Two new instruments are registered in `SKILL.md` and run; no new capability row and no change to an existing executable surface's contract. |
| coverage | unchanged | Roster stays 105; no new domain surface; S395 is a deeper anchor on an existing surface, not a widening. |
| calibration | unchanged | Four `[~]` boxes with evidence pointers, six mistakes mined, limits named in A1/A2/A7/A8 and README frontier; no `[x]` claimed. |
| adjacency | unchanged | `PROVINCE.md` byte-identical; the connector sweep reports the tameshi method overlap without absorbing it; kaidoku/revenger ownership stays operator-owned and unruled as reported. |

No axis harmed. Admission is therefore not blocked by an axis trade.

## 5. Discernment spot-check (LEARNING.md)

Re-opened sources (live from this closure, 2026-11-08):

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S395 (new own-work row) | admit | `tools/limine-pin-battery-r99.py` at the landed tip (sha256 `c2e8c8fc…`) | agree | Byte-level re-measure: `def meta_ok` at 99305, the echo assertion `if c.check_echo and not (got[8] == c.version and got[9] == "flag")` at 99430 (13 words), the era assertion at 99523; the X/Y assignment sites at 79015/79039 and 81666/81690 and the gate's emission lines at 16931/17037 all reproduce. The row's `teaches` is 48 words but the Gate's located quote is 13 words — within the ≤25-word rule. |
| S392 (re-open, docs.python.org `int()`) | admit (re-open) | `https://docs.python.org/3/library/functions.html#int` | agree, with a re-pin note | At closure the URL 301-redirects to `/3/builtins/functions.html` and returns HTTP 200, 331022 bytes; the current page is the 14:27 UTC rebuild, sha256 `19487dfe…`, where the seat measured `d92580dd…` at ~14:11 UTC (same byte length; footer now reads "Last updated on Nov 08, 2026 (14:27 UTC)"). The three anchors re-measure unchanged: 153202 `id="int"`, 157767 `have leading zeros, be surrounded by whitespace`, 159315 `disallows leading zeros`. So the seat's "identical, no drift" was true at measurement; the page rebuilt afterwards. Not a lane defect — re-pin on the next sweep. |
| limine v12.9.6 `CONFIG.md` (rejected candidate) | reject | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md` | agree | Live fetch HTTP 200, 27609 bytes, sha256 `f44f3a19…`, 495 lines; `grep -c` for `limine_version`, `visibility_era`, `echo`, `version` → 0/0/0/0. The page documents config keys and grounds none of this round's propositions. |

Newly written `corpus/SOURCES.md` row (≤25-word quote): S395's Gate quote
`if c.check_echo and not (got[8] == c.version and got[9] == "flag")` is 13 words, grounded at BYTE
99430, and reproduces byte-exactly on the pinned instrument. The row's `scope` cell is 22 words and
its `teaches` cell 48 words (a learning benefit, not a quote).

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → `tsukuroi ok`,
58 warnings (57 W04 duplicate-url + 1 W01 tier-C mined), 0 errors, exit 0. Census rows: before
`git show f107da3a…:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'` → **394**; landed tree
→ **395**. The S395 row is `status mined`, `used-by` cites
`corpus/knowledge/limine-metadata-cap-families-r99.md` and `corpus/lessons/round-99.md`; both paths
exist.

## 6. Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | Net +1 row (394 → 395, one A-tier own-work row) and one admitted knowledge entry on ground no lane entry held (the family's duty to *read* the fields it certifies; r98's entry covers the reported-fields contract, not the family obligations). No entry removed; the staged package's 147/147 id collision was measured and adoption kept closed. |
| quality | improved | Two frozen shapes and the ancestor branch now fail closed and are mutation-killed (r98 `PASS` → r99 `FAIL`; M07 `14/14` → `16/17`), the Y-only era lie flips from blind `met 105/105` to `unmet 104/105`, and both r98 instruments keep their bytes as controls. No admitted entry fails its re-check. |
| discernment | improved | The round's own overstatements were caught by its wave and narrowed before filing: A1/A2 (executed false-green cells), A4 (schema-token third change and dead sentinel), A7 (lie-kind granularity), A8 (roster-finite fields, X near-twin), A9 (a cited receipt that did not exist); the dropped twin bend and the disclosed seat harm are recorded. This closure's spot-check agrees with 2 admits and 1 reject. |

## 7. Routed defects (lane must fix next round)

1. **R99-D2 (status-neutral, bookkeeping).** `LOG.md` headings `Round 99 — freeze (pending)` and
   `Round 99 — measured (pending-settle)` are stale after settle; `LOG.md` is append-only, so append
   a correction entry naming the superseded headings (or use the round label only), never rewrite.
2. **R99-D3 (status-neutral, corpus precision).** S395's anchor says "the two new `LIE_KINDS`
   members at BYTE 108455"; 108455 is `limine-version`, the second member is at 108473. A wider-scope
   or corrected row must take S396 (ids are never reused) and name both offsets; a narrow correction
   may land as a superseding row or a lesson note.
3. **R99-D4 (evidence completeness).** `before/census-before-after.txt` records the before/after
   counts and only the after exit code; the prompt requires both outputs and exit codes. Paste the
   before command and its exit code next round.
4. **Carried (already named by the lane; confirm they land in r100):** the owed full
   `--selftest --reference` leg (A6a/A7), the dead `("ANCESTOR", None, None)` fixture sentinel
   removal (A4), the X/Y echo spelling bends, the five surviving C2 cell classes (A1), and the C5
   always-ok ancestor survivor's compound-probe witness.
5. **Observation, not a defect:** S392's external pin is a mutable docs URL; the page rebuilt at
   14:27 UTC after the round's measurement. Re-pin the sha on the next freshness sweep (180d
   `recheck` stands).

## 8. Closure summary

Both claims verify against committed evidence re-derived by this closure: instrument hashes 16/16
OK; the gate is byte-unchanged; C1's ten battery JSONs carry the exact frozen verdicts and failed
family sets with 0 error rows in both layouts, and the source diff supports the narrowed
"two behaviour-bearing changes" sentence (A4); C2's landed run, 17/17 selftest, two capture
fixtures, M07 mutant, ancestor probe and 160/160 coverage all re-read as reported. The prefile
ledger passes (`claims=2 rows=23 attack_seats=5 findings=0`, rc 0) and every non-neutral row is
reconciled by A1/A2/A7/A8. The discernment spot-check agrees with both sampled admits and the
reject; the census validates at 395 rows, exit 0. No axis is harmed: SCORECARD is append-only,
PROVINCE/SHONEN are byte-identical, the r98 instruments and the gate keep their bytes, and the
corpus is additive.

Status-neutral defects are named in §7; none bars admission. The four `SHONEN` boxes are
evidence-pointed and plausibly checkable by a non-author from the cited artifacts; promotion and
`[x]` writes remain operator-owned.
