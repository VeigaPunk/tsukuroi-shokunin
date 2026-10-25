# Round 35 — verifier spot-check (hyaku closure)

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-23
lane: tsukuroi, round 35, attempt 1
base `b40c01df38eb26f74c095c471efc6d1649b00fd4` → tip `c535371b4570a869bdadcf46c4d85187e96d4900` (master; both verified ancestors of the branch ref)
report: `.ufo/reports/round-35/tsukuroi.md` (fleet commit `da506d92`, author `tsukuroi-shokunin <tsukuroi@shokunin.local>`)

## 1. Conformance (protocol step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-35/tsukuroi.md` (fleet root) | `tsukuroi-shokunin tsukuroi@shokunin.local da506d92…` | pass |
| Report lands after child-repo work | committer dates: lane tip `c535371b` 09:25:57-03:00; report `da506d92` 09:27:08-03:00 | report commit postdates tip; cited hash is ancestor of master at closure | pass |
| SHONEN heading, one line per box | report `## SHONEN` | 4 lines, all `[~]` with evidence pointers | pass |
| Cited commits exist + ancestor of branch | `git merge-base --is-ancestor <hash> master` for `6b4561e4 7186722b e2f97e6e 95684c65 199beb97 6f92080d c535371b` (+ base) | all 8 pass | pass |
| Lane pushed, no lane debt | `scripts/hyaku/jj-lane.sh state` | `ahead=0 behind=0`, tip `c535371b` | pass with defect |
| Leftover | `git status --porcelain` | 1 untracked: `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz` (see routed defect 1) | defect |
| Prompt carries template contract | diff of `.ufo/prompts/tsukuroi-round-35.md` vs `templates/round-prompt.md` | full template rendered (report path, commit-then-report order, SHONEN heading, hash-citation rule, write scope) + §6 hyaku addendum; prompt committed by lane (`32641a38`) | pass |
| Marker predicate | report substance | real report: work, evidence pointers, checkable hashes, Sources & frontier, trend verdicts | not a marker |

Watchdog digest (copied per closure prompt): `2026-10-23T07:41:44-03:00 launch tsukuroi round=35 pgid=450165 driver=hyaku-inline attempt=1`; `2026-10-23T09:27:34-03:00 complete tsukuroi round=35; hyaku-inline attempt=1`; `2026-10-23T15:03:26-03:00 complete tsukuroi round=35; hyaku-inline attempt=1`.

## 2. Claims

### C1 (coverage) — census pacnew/pacsave drift arm — NOT VERIFIED (honest stop; lane verdict re-derived, agreed)

Re-measured from committed bytes (commands and observed output):

- `git show c535371b:tools/tsukuroi-census.sh | grep -c probe_pacnew_arm` → `2`; base `b40c01df` → `0`. Seam `TSUKUROI_ETC_DIR` present (line 425); `DRIFT pacnew-plane` documented at `SKILL.md:3009`. Arm landed.
- Battery before, at `7186722b` (`grep -oE … .ufo/waves/round-35/w2/W2BeforeBattery/before-battery-7186722b.jsonl`): `candidate_matches 0, control_matches 24, of 24, should_fail 17, should_fail_accepted 0, harness_errors []`, exit 1 — matches the report byte-for-byte.
- Battery after, at `e2f97e6e` (`.ufo/waves/round-35/after/c1-after-battery-e2f97e6e.jsonl`): `candidate_matches 24, control_matches 24, of 24, should_fail_accepted 0`, exit 0 — matches the report.
- Kill rule, lane-declared and re-derived: `W2TreeKeyed/variant.jsonl` `candidate_matches 24 of 24` and `W2LogKeyed` `24 of 24` both met VERSION 2 before the change existed; late W2LiveOracle added two more meeting controls (`livecache-variant.jsonl`, `cwdgate-variant.jsonl`). A skip-work control meeting the frozen counter fires the declared kill rule → C1 reported not verified. The lane reported exactly this; honest stop, no overclaim.
- Gate evidence (verified, not executed — protocol §Gate standard closure consequence): selftest tally `.ufo/waves/round-35/l1/r35-st-after2.txt` ends `TSUKUROI_CENSUS_SELFTEST: PASS (105 cases, 105 passed, 0 failed)` (101 → 105 cases as claimed); gates at `199beb97` (`after/gates-199beb97/`): six gates exit 0; `check-pause-gate` exit 1 carrying the same `GATE-PREMISE` P3 as the base receipt (`w1/ExecGateBaselines/base-check-pause-gate.jsonl`) — inherited, not round-caused. The four round-caused reds at `95684c65` were repaired at `199beb97` (committed receipts in both directories).
- No-harm: `git diff --stat 7186722b e2f97e6e -- tools/` lists only `tools/tsukuroi-census.sh` (+115/−1); my append-only sweep `git diff -U0 b40c01df c535371b -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md | grep -E '^-[^-]'` prints nothing; SHONEN.md untouched; ordinals unchanged (depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8 — matches SCORECARD "Ordinal record, round 35").

Claims re-measured vs evidence-verified: battery before/after and kill-rule receipts re-measured by me from committed bytes; census selftest and gate verdicts evidence-verified only (a sibling's gate is never executed).

### C2 (depth, exploratory) — `corpus/knowledge/pacman-backup-files-r35.md` — UNPROVABLE-BUT-BETTER (named non-author reviewer ruling: this closure)

Prior state verified: `grep -rlniE 'libalpm/add\.c|lib/libalpm/remove\.c' corpus/knowledge/ SKILL.md` outside the new note prints nothing — no prior entry read pacman's code for these branches; the claim's prior-state sentence holds.

Source re-open (committed snapshots at the pinned installed commit `54d94116164b`; host `pacman -Q pacman` reads `7.1.0.r9.g54d9411-3`, `pacman-contrib 1.13.1-1` — both confirmed live):

| Note claim | Re-opened source | Result |
|---|---|---|
| `.pacnew` written + `warning: %s installed as %s.pacnew` via `alpm_logaction` (S191) | `add.c:323,349-350` | verified |
| Six-branch MD5 decision table (S191 lines 352-404, S194) | `add.c:365-372,373-379,403-404` | verified; none/Y/Y installs without `.pacnew` confirmed |
| Silent `.pacnew` rewrite shows `[inf]`, only DEBUG on that path | `add.c:376-379` | verified as the note's own [inf] marking |
| NoUpgrade skips hash compare, existing file → `.pacnew` (S191, S195) | `add.c:302-304,341` | verified |
| Removal saves only when MD5 differs, `filehash` NULL → no save (S192) | `remove.c:529,536,548,559-560` | verified |
| `shift_pacsave` renames unlogged; only the new save logged (S192) | `remove.c:406,416` (bare `rename`, no `alpm_logaction`) | verified |
| `.pacorig` retired: 0 matches in add.c/remove.c at 54d9411; pacdiff still searches it (S193, S196) | `grep -c pacorig` → 0/0; `pacdiff.sh.in:228,232,235,244` | verified |

Review ruling (non-author): **unprovable-but-better**. Reasons: (1) the note adds mechanism ground — which branch makes which file, which events are logged — that no prior entry held, on an already-owned surface, so it is depth, not expansion; (2) every mechanism claim re-verified against the pinned installed-commit sources above, with line-level citations; (3) honesty marks are real: the two un-reproduced branches carry `[inf]` and an `[unk]` section states no host event was reproduced; (4) a falsifier section names the contrary evidence per statement; (5) provenance trio complete (`source:` S-rows, `verified-at:`, `recheck:` cadence naming the installed-commit re-open procedure, no package-manager action); (6) quote contract holds (see §3). This judgment is recorded per `AXES.md` exploratory-claim rule and `LEARNING.md` "Discernment is checked from outside".

## 3. Discernment spot-check (LEARNING.md) — gate sample re-opened

| Item | Lane decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S191 pacman `add.c` @54d9411 (`.pacnew` warning) | admit, mined, tier A | committed copy `.ufo/waves/round-35/w1/CritC2Absorb/sources/add.c` (`fd313629…` prefix recorded); quote at line 350, 7 words | agree | quote present verbatim at the recorded line; tier A is scoped to the 7.1.0 code decision branches, not host state — scoped sanely |
| S197 pacman `add.c` @master | **reject** (not the installed 7.1.0.r9.g54d9411) | `.ufo/waves/round-35/l1/src/add.c-master`, `sha256 = c63fb24d…` (matches the recorded prefix; full hash equals the value recorded at `corpus/SOURCES.md:203`) | agree | master differs materially (`get_install_time`/`SOURCE_DATE_EPOCH` path vs `time(NULL)` at 54d9411) and the host installs `7.1.0.r9.g54d9411-3`, confirmed by `pacman -Q`; a master copy cannot support a host statement. Rejection with flip ("host installs a later commit") is the correct call |
| S192–S196 admits | admit, mined, tier A | quote word counts from the Gate table: S192 9w, S193 10w, S194 18w, S195 15w, S196 5w — all ≤25 with location + sha256; `SOURCES.md` rows well-formed (11 cells each, S197 teaches opens `REJECTED:` with a flip) | agree | sampled via a second read-only seat and my own row read; quote contract holds for every new row |
| Census | `scripts/sources-census.sh validate --root … tsukuroi` | exit 0, last line `tsukuroi ok`, rows 190 → 197 (matches report; my count `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 197) | agree | 31 pre-existing W04 duplicate-url advisories, unchanged class, non-failing |

Discernment verdict support: the round's gate agrees with the outside spot-check on all sampled admits and the sampled reject; the lane applied its own kill rule against its claim (C1) — good-taste evidence. Held back from `improved`: the round's counter still fell to forced-shape keying (W2TreeKeyed/W2LogKeyed) after one redesign, four of its gates were run only after the outcome commit (repaired, lesson mined), and the round-34 timestamp defect recurred (see routed defects).

## 4. Axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| coverage | unchanged | C1 not verified under its declared kill rule; arm landed and measured (24/24 after, 105/105 selftest) but the claim's falsification condition fired; ordinal unmoved; no surface lost |
| depth | unprovable-but-better | C2 exploratory, admitted through this non-author reviewer's ruling (§2) |
| operability | unchanged | selftest 101 → 105 all passing (evidence-verified); capability table explicitly adds no row; ordinal 9 → 9 |
| freshness | improved | `pacnew-plane.md` R35-FRESHNESS re-measure verified live by me: `find /etc \( -name '*.pacnew' -o -name '*.pacsave' \) 2>&1 >/dev/null \| grep -ci 'Permission denied'` → **11** (supersedes the 12 of 2026-10-19, with the `/etc/cryptsetup-keys.d` removal traced in the journal); `pacman-contrib 1.13.1-1` installed, `/usr/bin/pacdiff` present (supersedes the "not found" reading); `coredump-count-unit-r34.md` correction block rechecked on systemd 262 (host runs 262; committed recheck output `.ufo/waves/round-35/w2/W2RevC2Remnants/recheck-rerun-output.txt`) |
| calibration | unchanged | honest self-assessment throughout (C1 declared not verified by the author); ordinal 9 → 9; the heading-time recurrence (below) is recorded by the lane as a mistake but is a second occurrence |
| adjacency | unchanged | `ConnSiblings.md` / `W2ConnAfter.md` find no crossing; not acknowledged by a sibling (named, not hidden); ordinal 8 → 8 |

## 5. Trend verdicts

- **expansion: unchanged.** C2 is deeper ground on an owned surface (`pacnew-plane`/`package-state-plane` already held the surface); C1 unverified; the seven new `SOURCES.md` rows are mined on owned ground; no `knowledge/` entry was admitted on uncovered coverage-map ground (my re-read of the coverage rows and the note's own "not a new surface" statement).
- **quality: improved.** Verified supersessions: the 12-unreadable and pacdiff-absent readings re-measured and superseded (my live counts above); the NoUpgrade-as-pin grouping superseded as a classification by the sourced note; the coredump note's three remnants corrected with a systemd-262 recheck. One defect kept it short of stronger: the supersession sweep did not reach every mention (routed defect 5).
- **discernment: unchanged.** Gate sample agrees with the outside re-open on ≥1 admit and the real reject; the kill rule was applied against the author's own claim. Against: VERSION 2's forced shapes were a label the controls exploited, the round's own gates ran after the outcome commit, and the round-34 timestamp defect recurred.

## 6. Routed defects for round 36 (lane must fix)

1. **Commit or remove the leftover tarball.** `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411.tar.gz` is untracked lane round work at closure (`jj-lane.sh state` `untracked=1`); the round-35 lesson cites the tarball's directory as the S191/S192 snapshot home while the committed snapshots live under `CritC2Absorb/sources/`. Commit it as evidence or delete it and point the lesson at committed bytes.
2. **Heading-time recurrence (R35-LOG-TIME-ESTIMATES, second occurrence).** I re-ran the lane's check: `7186722b`=08:37:49-03:00, `e2f97e6e`=08:52:40, `95684c65`=08:57:41, `199beb97`=09:00:35, `6f92080d`=09:25:23 against LOG headings "~11:40Z", "~12:00Z", "~12:00Z", "~12:05Z", "12:26Z" — five headings later than their commits. The recorded fix (paste `date -u +%H:%M:%SZ` at write time) must be enforced; a third occurrence routes to the operator.
3. **Counter debts before any re-claim** (lane's own planned list, re-affirmed): the round-34 untraced view and VERSION 6 normalisation fix; a pacnew counter whose forced shapes draw counts from a range including 0 and 2+, with the W2TreeKeyed, W2LogKeyed and the two W2LiveOracle live-gate patches added to its should-fail battery, and battery coverage of the ctime check and live view (W2MutCounter/W2ArmAuditA/B/W2RevCounterV2 findings); the five live-tool ambient copies (ExecAmbientA/B cancelled without output).
4. **Correction sweep incomplete for the NoUpgrade supersession.** `SKILL.md:397-399`, `update-safety-note.md:420-424`, `update-safety-v2.md:52` and `:198` still state `NoUpgrade`/`NoExtract` as version pins — superseded by `pacman-backup-files-r35.md` (file-extraction rules, not pins). Append correction rows naming the superseding note; do not rewrite history.
5. **Gate timing discipline.** Four round-caused gate reds at the outcome commit `95684c65` (self-assessment, registry kinds, recheck invocation, adjacency anchor) — repaired at `199beb97` with the lesson "Gates at the outcome commit" mined; keep the repaired shape (registry kinds `probe`, note recheck without `pacman`, IN-109 anchor re-pin) under the round-36 gates' first run.

## 7. Notes for the operator

- SHONEN boxes are all `[~]` (author-asserted). Boxes 1 (SKILL.md tables/patterns/sources — round35 registry at `SKILL.md:2945-3009` with cited commits) and 4 (no cross-domain bleed — `ConnSiblings.md`, `W2ConnAfter.md`) look fully checkable by a non-author reviewer with the cited evidence; promotion review is operator-owned.
- One fleet-root file `0` (31 bytes, "NF=13 cells=11 double_quotes=0", 12:09Z) looks like a misdirected shell redirect from a table-cell check; it names no lane. Left untouched per the lane's report; operator may delete.
- No capabilities added (capability table unchanged by the lane's own record; C1 unverified). No installs by this closure. No seats died in the round except the recorded provider hold K09HarnessSnoop (`cyber_policy`), item ended, not retried or rerouted — per standing rules.
