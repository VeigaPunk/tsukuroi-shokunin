# Round 98 verifier spot-check — tsukuroi lane (non-author integrator)

author: hyaku closure (non-author integrator, @m_zfl)

Lane `tsukuroi-shokunin` (operability + freshness), campaign hyaku, round 98, attempt 1.
Pre-round tip `b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a`; freeze `1cfeb5d5`; settle
`270ca298d7aac4a3bd11c75900e3a9faa21098f7`; ledger repair `839954b79d8cda9564e181b1bd7dbe3bc9f51e77`
(= lane `master` at closure). Dispatch digest (`.ufo/watchdog.log`): `2026-11-08T09:34:03-03:00
launch tsukuroi round=98 pgid=4112028 driver=hyaku-inline attempt=1`; `2026-11-08T10:30:09-03:00
complete tsukuroi round=98; hyaku-inline attempt=1`.

## 1. Conformance

- Report committed in the fleet repo by the lane identity:
  `git log --format='%an %H' -- .ufo/reports/round-98/tsukuroi.md` → `tsukuroi-shokunin
  c0c486386941790610f58fea2fc98659727a4407`. Pass.
- `SHONEN` heading at report line 165 with four `[~]` lines citing resolvable evidence (SHA-N/a
  evidence pointers `SKILL.md` lines, `w1/` receipt dirs, `LOG.md` Round 98 entries; all four marked
  asserted-by-author, non-author verification still owed — consistent with no `[x]` without a named
  non-author verifier). Pass.
- Cited lane commits exist and are ancestors of the lane branch ref:
  `git -C tsukuroi-shokunin merge-base --is-ancestor {1cfeb5d5, 270ca298, 839954b7} master` →
  YES for all three. Pass.
- Lane repo clean and pushed: `jj-lane.sh state` → `branch=master local=839954b7 remote=839954b7
  ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git -C tsukuroi-shokunin status
  --porcelain` → empty (excluding this spot-check file, written after the check). Pass.
- Prompt carries the template contract: `.ufo/prompts/tsukuroi-round-98.md` contains the MISSION/AXES
  binding, 1–3 claims on distinct axes with a lowest-axis obligation, the frontier step (SOURCES.md
  contract v1, census command, mined mistake, sourced claim), the L2 floor (≥8 in one batched swarm,
  role split, host route table, godspeed lead), the report contract (path, section order, marker
  rule), commit/push scope and the L0 side channel, and the hyaku §6 addendum. Pass.
- Misroot sweep has no round-98 residue: fleet `git status --porcelain` shows 10 paths, none naming
  tsukuroi or round-98 (confirmed by `grep -E 'tsukuroi|round-98'` → empty). So the report's claim
  holds; count is 10 now vs 11 at filing (one orchestrator-owned `.scratch` path changed) —
  status-neutral chronology, no defect.
- The report is a real report (work performed with evidence pointers, landed changes tied to LOG
  entries, before→after measurements with counting commands, Sources & frontier, trend verdicts,
  SHONEN, prefile-falsification gate line), not a marker. Status `ok`/not-failed.
- Status-neutral conformance note (no defect): the report's header cites `git ls-remote origin
  refs/heads/master` as the filed-at-check; the lane branch is `master`. Verified equal at closure.
  `.ready` lives at `.ufo/waves/round-98/w1.ready` (not `.ready`); report says `.ready taken
  10:02:04` — file present in the settle. Cosmetic path shorthand, not a defect.

## 2. Prefile falsification ledger (§2b)

`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tsukuroi
--round 98` → `PREFILE-FALSIFICATION: pass claims=2 rows=18 attack_seats=5 findings=0` (exit 0;
live re-run matches the report's §Prefile falsification gate). Ledger: 18 rows, `cut -f1,3 | sort |
uniq -c` → `C1: 1 falsifies-wording + 12 neutral; C2: 1 falsifies-number + 2 falsifies-wording + 2
neutral`. All four non-neutral rows name a narrowing in `.ufo/waves/round-98/before/plan-amendments-r98.md`:

| Ledger row | Type | Amendment | Closure adjudication |
|---|---|---|---|
| C2 `w1/ReviewRegistry/receipts/10-a-to-e.txt` | falsifies-wording | A1 | Real and reconciled: the ordered alternation binds a hybrid cell's first arm (F1) and a second mention is dropped; the predicate's "accepts N-N or N[,N]" does not promise hybrid coverage, and A1 records the limit (named, routed r99) rather than extending the claim. |
| C2 `w1/CriticClaims/receipts/15-m08-selftest.txt` | falsifies-number | A2 | Real and reconciled: that receipt reads 2/14 — a comma-always (M10-like) mutant, not the frozen first-label-only M08. The M08 kill is carried by the L1 receipt `before/dev/c2-m08-selftest.txt` (12/14, exactly span-gap + span-gap-lie red) and `w1/ExecRegistry/07-m08-selftest.txt`, independently reproduced; this closure re-read both (see §3). |
| C1 `w1/ReviewBattery/g6-y-era-r98.json` | falsifies-wording | A4 | Real and reconciled: "lies in either field" as a universal is false for Y-cap spellings (`met 105/105` on both batteries); A4 narrows the predicate to Z/LZ spellings. Verified: G6 artifact is `passed=105/105 verdict=met failed_families=[]` against the r98 run; the Y family sets neither flag and EXPLICIT families never send Y spellings. |
| C2 `w1/CriticClaims/receipts/capture-audit.txt` | falsifies-wording | A3 | Real and reconciled: spaced/lowercase forms read `RC-CELL-MISSING` (fail-closed); A3 narrows the capture's stated alphabet to `N<digits>` with no space token. |

No spurious rows and no unreconciled falsification. Attack-role seats in the ledger: ReviewBattery,
ReviewRegistry, CriticClaims, MutRegistry, ConnectorOverlap (5 — matches report's 5/14 = 36%).

## 3. Per-claim re-checks (committed evidence; no gate re-execution)

Instrument integrity (evidence-verified, not re-run): `cd tsukuroi-shokunin && sha256sum -c
.ufo/waves/round-98/before/instruments.sha256` → **27 files OK, exit 0**. Gate bytes:
`sha256sum tools/check-limine-pins.py` → `7d79ac29…`, identical to `git show b3be3f90:tools/
check-limine-pins.py` — the gate is byte-unchanged across the round, so no axis lost ground through
gate drift. Do-nothing control identity: `w1/ExecDoNothing/sha256-battery-identity.txt` →
battery `e678c34f…` = `b3be3f90:tools/limine-pin-battery-r97.py` (re-derived here from git show).

### C1 (depth 8) — verified

Command run by this closure: a Python pass over the nine committed battery JSON artifacts
(`w1/ExecGateRuns/c1-gate-{canonical,clone}.json`, `w1/ExecBends/c1-bend-N07-era-field-lie-{canonical,
clone}.json`, `w1/ExecBends/c1-bend-N08-echo-norm-{canonical,clone}.json`, `w1/ExecDoNothing/dn-{
gate,N07-era-field-lie,N08-echo-norm}.json`), counting `families_passed/families_total`,
`failed_families`, `verdict`, and non-null `error` rows per run.

Observed: landed gate canonical `105/105 met []` ×3 and clone `105/105 met []` ×3, 0 error rows in every
file; N07 `103/105 unmet [LEADING-ZERO-NORMALIZE, REFUSAL-VERSIONS-9DIGIT-Z]` ×3 both layouts; N08
`104/105 unmet [LEADING-ZERO-NORMALIZE]` ×3 both layouts; do-nothing r97 battery `met 105/105` ×3 on
the gate, N07 and N08 (blindness — the new assertions are causal); roster `FAMILY_ROSTER len = 105`
(re-derived from `tools/limine-pin-battery-r98.py`); `check_echo`/`check_era` = 6 occurrences each;
LZ docstring names `12.000000009.000000005` with the era-A/int-12.9.5 direction. Field-coverage
attacks: g1 era-lie-everywhere `102/105` (three families), g2b fixed-echo `100/105`, g3 X-cap-only
`104/105 [EXPLICIT-VERSION-ERA]`, g4 source-probe `102/105`, g5b truncation `100/105`, g6 Y-cap-only
era lie `105/105 met []` (the A4-narrowed survivor, verified); B01/B02 killed by leg direction
(re-read `B01-N08`/`B02-N07`: `met 105/105` where the frozen leg expects `unmet`); B03: `B03-landed
105/105 met`, `B03-N07 103/105` byte-identical to pristine — a genuine Z-echo survivor (named limit,
r99). All match the report table. **C1 met.**

Note for the operator (§6 nudge): depth stays 8 and adjacency stays 8 (tied lowest, no claim).
Depth not moving while C1's improvement is real is honest — a sharper instrument, no ordinal uplift —
and the lane says so in SCORECARD. No defect.

### C2 (freshness 9) — verified

Committed evidence re-read (no gate re-execution, per §Gate-standard "Closure consequence"): `before/
dev/c2-selftest-r98.txt` → `selftest PASS 14/14` (`span-gap` + `span-gap-lie` present); `c2-selftest-
r97.txt` → `PASS 12/12`; `c2-m08-selftest.txt` → `FAIL 12/14` exactly the two gap cases red; D1 on r98
`FAIL` exactly one `RC-VALUE-MISMATCH` (states `N01,N03`, derives `N01-N04`) vs r97 `RC-CELL-MISSING`;
D2 r98 `PASS`, M08 `FAIL` one, r97 `RC-CELL-MISSING`; D2lie r98 `FAIL` one, M08 `PASS`; coverage
`PASS 157/157 findings 0` on every doctored revision (`c2-D{1,2,2lie}-coverage.json`); landed
`PASS 7/7 findings 0` on both checkers at base (`c2-content-landed-{r97,r98}.txt`); settled-tip
content `PASS 7/7` (`after/c2/content-freeze.txt`) at the freeze revision with a coverage FAIL at the
freeze tip naming exactly the three new r98 tools (rows land in the settle — by design, and the lesson
records it). **C2 met.**

Minor evidence-cascade defect (status-neutral, routed): the report and SCORECARD claim coverage
`PASS 160/160` "at the settled tip" and cite `after/c2/` receipts, but the committed `after/c2/`
holds only the freeze-time receipts (`content-freeze`, `coverage-freeze` at `1cfeb5d5`, the latter
FAIL 3 findings as designed); `.ufo/waves/round-98/after/report-draft.md` also references a
non-committed `after/c2/coverage-tip.json`. The `160/160` figure itself is consistent — 157 base rows
+ S393/S394 + the landed settle row = 160, and the wave's coverage blame is fully accounted — but the
receipt cited for it does not exist in the tree. The lane should commit the tip coverage JSON next
round (a one-line artifact drop); the claim verifies without it. Header gate `114/114` is supported
by the committed ScribeKnowledge receipts (`w1/ScribeKnowledge.md` gate table).

## 4. Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| depth | improved | C1 verified: the two r97 families assert the JSON fields their clauses name; N07/N08 bends and five field-attack shapes now fall where the r97 instrument was blind; no score inflation claimed (8→8). |
| freshness | improved | C2 verified: the comma-span capture is pinned by two selftest cases that kill the r97 M08 survivor; D1/D2/D2lie discriminate with the mutant inverting; no score inflation claimed (9→9). |
| operability | unchanged | No new executable surface; the three r98 instruments run through the existing registry rows (SKILL.md +3 rows, additive). |
| coverage | unchanged | Roster unchanged at 105; S394 supersedes S393 rather than widening. |
| calibration | unchanged | Four `[~]` boxes asserted honestly with evidence pointers; no `[x]` claimed. |
| adjacency | unchanged | PROVINCE.md byte-unchanged (`git diff --stat` between tips → empty); kaidoku/revenger ownership left unruled as reported. |

No axis harmed. Scope check: the round diff over `b3be3f90..839954b7` is additive in corpus and waves
plus three new tools, one SKILL.md registry block, SCORECARD/LOG edits; gate bytes unchanged; r97
instruments keep their landed bytes and read `105/105` / `PASS 12/12` as do-nothing controls.

## 5. Discernment spot-check (LEARNING.md)

Re-opened sources (live `curl` from this closure, 2026-11-08):

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S394 (own-work, supersedes S393) | admit | `tools/check-limine-pins.py` at the freeze (sha256 `7d79ac29…`) | agree | The ≥25-word quote was checked against bytes, not trusted: offset 4425 gives the `resolved \`limine_version\` and \`limine_version_source: "probe"\`` sentence; 16931/17037 hold the MAIN return's `"limine_version"` / `"visibility_era"` lines; 11230/11344 hold the CANNOT-EVALUATE early return's copies. S393's error (naming the early-return pair as the main return) is exactly what S394 corrects, and the lesson records the in-place change old→new. |
| S392 (re-open, docs/python.org `int()`) | admit (re-open, no drift) | https://docs.python.org/3/library/functions.html#int | agree | Live fetch returns 331022 bytes, sha256 `d92580dd…`; offsets re-measured: 157767 `have leading zeros, be surrounded by whitespace`, 153202 the `id="int"` heading, 159315 `disallows leading zeros`. Byte-identical to the r97 pin. |
| limine v12.9.6 `CONFIG.md` | reject | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md | agree | Live fetch returns HTTP 200, 27609 bytes, sha256 `f44f3a19…`; `grep -c` for `limine_version`, `visibility_era`, `echo`, `version` → 0/0/0/0. The page documents config keys, not the gate's JSON fields — it grounds none of this round's propositions, so the rejection is evidence of taste, not a miss. |

Newly written `corpus/SOURCES.md` row (≤25-word quote): S394's quote — `resolved \`limine_version\`
and \`limine_version_source: "probe"\`` (BYTE 4425) — is 2 words, well under the limit, and grounded
at the claimed offset; re-opened above. The row's `teaches` matches the landed-byte behavior
(field asserted at both emission sites).

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi` → `tsukuroi ok`, 58 warnings (57 W04 duplicate-url + 1 W01), 0 errors, exit 0. Census rows:
before `git show b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a:corpus/SOURCES.md | grep -cE`
`^|[[:space:]]S[0-9]{3,}` → **392**; after the landed tree → **394** (+2: S393 and its supersession
S394). Matches the report and lesson exactly.

## 6. Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | Net +2 rows (392 → 394); one knowledge entry (`limine-metadata-assertions-r98.md`) admitted on the gate's *reported* metadata — ground no lane entry held; S394 corrects S393's anchor with both sites named; S392 re-opened byte-identical. No admitted entry fails its re-check. |
| quality | improved | R97 A7 limit closed by two bends the r97 instrument reads blind (`105/105` → `103/105`/`104/105`); R97 M08 survivor killed by two selftest cases plus the D2/D2lie inversion; R97-D3 docstring defect corrected with its manifest relation stated; reviewers corrected B01/B02 direction and downgraded a mislabeled mutant rather than citing it for the kill. |
| discernment | improved | The lane's own anchor error was caught by a seat (ScoutSources §2) and corrected in the same round; the Y-cap survivor was narrowed by amendment A4 instead of being left under the universal sentence; the ledger names four falsifications with narrowing amendments, all reconciled above. |

## 7. Routed defects (lane must fix next round)

1. **R99-D1 (status-neutral, evidence cascade).** Commit the settled-tip coverage receipt (`after/c2/
   coverage-tip.json`-equivalent) so the `PASS 160/160` figure the report and SCORECARD cite is
   backed by a committed artifact, not by an unlanded file referenced from a report draft. Also
   remove or land the stale `after/report-draft.md` pointer.
2. **Routed wave limits already in the lane's queue (no action beyond the frontier's existing
   commitments):** Y-cap field fidelity (B03-class, no Z-echo witness bend), the battery selftest's
   missing echo/era lie kind, the checker M07 ancestor branch, hybrid and same-cell-restatement
   capture shapes, spaced/lowercase forms, the r98 battery's unchanged JSON schema token, and the
   carried unbound-row/co-doctoring/tally-parsing items — all recorded in `corpus/README.md` §
   "Frontier (round-98 addition)" and the lesson scoreboard; r99 should give each survivor a witness.

No other defects: no lane-authored leftovers, no SHONEN boxes fully checkable by a non-author beyond
what is already asserted `[~]`, no cross-domain bleed. The wave (14 seats, `w1-results.json`, 0 dead,
`w1-validate.err` 0 bytes, attack share 5/14 = 36%, 1 connector) conforms to the §3/§6 floor; the
two seats' time-bounded `--selftest --reference` legs are honestly recorded as not completed and
redundant with the landed-gate legs (r97 analogue 18/18) — status-neutral.

## 8. Closure summary

C1 and C2 both verify against committed evidence re-derived by this closure (instrument hashes
27/27 OK; C1 battery JSONs re-parsed with 0 error rows and exact failed-family sets; C2 selftest,
D-legs and coverage receipts re-read; FALSIFICATION pass 18 rows/5 seats/0 findings). Gate-standard
conditions hold: self-test tallies, frozen-run verdicts and measured revisions are committed;
no sibling gate was executed by this closure. The one shortfall — the unlanded `160/160` tip-coverage
receipt — is an evidence-cascade defect, status-neutral, routed as R99-D1, and does not bar
admission. All falsification rows are real and reconciled by amendments A1–A4. Verdicts and trends
above agree with the MANIFEST entry.
