VERDICT: draft

# ScribeLesson — item F-3, draft of `corpus/lessons/round-45.md` (round 45, wave a2w1)

Seat: ScribeLesson (scribe, axes discernment + lessons). Lane `tsukuroi-shokunin`. Read-only on lane content: the only
writes are this report and `.ufo/waves/round-45/a2w1/ScribeLesson/` (five receipts). Scratch
`/fast/scratch/hyaku/tsukuroi-r45/ScribeLesson` (removed at the end). No counter was run (the C1 counter's receipt at
`18389f44` was read from the wave's own seat, `.ufo/waves/round-45/a2w1/C1ExecRerun/c1-after-1.jsonl`). No subagent
was spawned. No tool installed.

**What this seat did.** It verified the two candidate mistakes in the item against committed bytes, corrected one of
them (the candidate drift list omits round 35), found and verified three further mistakes in this wave's own work, and
measured every round-44 routed defect D1-D10 at the implementation `18389f44`. The lesson text is §2 below, exact
Markdown; it is **not** written to `corpus/lessons/round-45.md` (the L1 lands it).

# 1. Evidence for the lesson's claims

## 1.1 Candidate mistake 1 — IN-109 `found_line` drift: verified, and the candidate list is incomplete

`git -C …/tsukuroi-shokunin log --oneline -- corpus/knowledge/adjacency-anchors-r19.json` lists the repin commits
(r32 `83b017c2`, r35 `199beb97`, r38 `02eeed07`, r39 `49cc53c7`, r39 `a2d7aad7`, r42 `78abb8b5`, r45 `ea6e0ee3`). The
decisive measurement is per census-touching commit: the anchored quote line versus the anchor's `found_line`
(receipt `ScribeLesson/drift-table.txt`, generated from `git show <r>:tools/tsukuroi-census.sh` and
`git show <r>:corpus/knowledge/adjacency-anchors-r19.json`):

| commit | round | quote line | `found_line` | state |
|---|---|---|---|---|
| `7cc59c8e` … `a90cefef` | 19-20 | 2216 | 2216 | match |
| `4ac5ebaa` | 32 | 2277 | 2216 | mismatch (repaired at `83b017c2` → 2277) |
| `e2f97e6e` | **35** | 2346 | 2277 | **mismatch — not in the candidate list** (repaired at `199beb97` → 2346) |
| `52ffd65f` | 38 | 2411 | 2346 | mismatch (repaired at `02eeed07`, which also moved the line → 2425) |
| `49cc53c7` | 39 | 2447 | 2447 | match (repin in the same commit) |
| `a2d7aad7` | 39 | 2452 | 2452 | match (same commit) |
| `44766208` | 42 | 2465 | 2452 | mismatch (repaired at `78abb8b5` → 2468) |
| `ab8aae16`, `071ab0d1`, `9608ebc3`, `8eee79db`, `fbfef071` | 44 | 2579 / 2580 / 2582 / 2582 / 2582 | 2468 | **mismatch, never repaired in the round** |
| `e9ca7ef6`, `5bbd5ff5` | 44 tip / r45 base | 2582 | 2468 | mismatch at the base the round inherited |
| `ea6e0ee3`, `18389f44` | 45 | 2582 | 2582 | match (D1 repin, committed with the declaration) |

So the anchor moved in **seven** census commits across six rounds (32, 35, 38, 39 ×2, 42, 44), and every round repaired
it except 44. The item's candidate list ("rounds 32, 38, 39 (twice), 42 and 44") omits round 35; the lesson text states
the fuller history. The fix mechanism is the round's C1 adjacency kill rule, and it is shown red then green:

- red — control C1-K7 inserts one comment line above the IN-109 selftest case: `.ufo/waves/round-45/controls/C1-K7.jsonl`
  line 2 reads `"adjacency": {"bytes_base": true, "exit": 1, "findings": ["INBOUND-CLASSIFICATION-WRONG"], "status":
  "FAIL"}, "adjacency_ok": 0` and the control line 1 reads `{"control": "K7", "expect": "FAIL", "exit": 1}`.
- green — `python3 tools/check-adjacency-anchors.py --revision 18389f44…` printed
  `{"… "findings": [], "revision": "18389f44…", "status": "PASS"}`, exit 0 (`ScribeLesson/adjacency-18389f44.json`);
  seat `a2w1/AdjPins.md` ran the same gate and reports the same PASS.

## 1.2 Candidate mistake 2 — the round-44 report's two missing sections: verified

- `grep -c '^## Sources & frontier' /home/vgpnk/Projects/shokunin/.ufo/reports/round-44/tsukuroi.md` → `0`
- `grep -c '^## Trend verdicts' …` → `0`
- headings present: `Outcome`, `Work performed`, `No-harm and checks`, `Incidents`, `Tooling`, `SHONEN`, `Next`
  (`grep -n '^#'` on the file).
- The template requires both (`templates/round-prompt.md:111` "**Sources & frontier** — `SOURCES.md` rows
  before→after with the counting command…", `:116` "**Trend verdicts** — one verdict each for `expansion`, `quality`,
  and `discernment`"), and its marker rule names exactly these two as *not* marker predicates (`:122-125`), which is
  why round 44 was graded `ok` plus a conformance defect. No mechanical gate exists for them: `:127-128` "The watchdog
  logs its Sources & frontier marker … it does not check trend verdicts". The lesson records this as the weakness of
  the fix, not as a passing check.

## 1.3 Mistake found this wave (a) — GR2's host reading is false, verified first-hand

Entry `corpus/knowledge/btrfs-scrub-grounding-r45.md:88-89` at `18389f44`: "The filesystem lists devid 1 only
(capture.txt:9) and the caller has no effective capabilities (capture.txt:1): **no replace or scrub state is observable
to this caller**, and the row is read from source." Read-only as uid 1000 on this host
(`ScribeLesson/host-replace-attrs.txt`):

```
/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/replace_target mode=444 owner=root value=0
/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/exclusive_operation mode=444 owner=root value=none
/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max mode=644 owner=root value=0
```

Three wave seats reached the same conclusion independently: `a2w1/C2ExecHostRecheck.md` §1 ("GR2's Host reading is
false in its deciding clause"), `a2w1/C2CritGR2.md` ("Host reading — 'no replace or scrub state is observable to this
caller' overreaches", with the same two attributes and `sysfs.c:1288,2007-2029`), and `a2w1/C2RevEntryWhole.md`
finding 2 (GR2's universal "any device" refusal). The counter cannot catch it: its `host_ok` leg "names existing,
non-empty capture.txt lines" only (`tools/check-scrub-grounding-r45.py:27`), so a true citation plus a false inference
passes. This is the same class as round 44's R44-C2-SR7-REPLACE-OMISSION.

## 1.4 Mistake found this wave (b) — AsmGate's id-census numbers do not reconcile with the registry

`a2w1/AsmGate.md` reports "183 registry ids, 147 staged ids, 30 intersections" at `18389f44`. Recomputed over the same
bytes (`ScribeLesson/id-census.txt`): lane `corpus/SOURCES.md` has **249** rows and 249 distinct ids (S001-S249, every
row 11 cells); staged `SOURCES.append.md` has 147 ids (S200-S346); the true intersection is **50** (S200-S249). The
kept receipt `a2w1/AsmGate/id-collisions.txt` holds 30 ids, of which S250, S251, S252, S262, S268 are not lane registry
ids at all, while 25 genuine collisions are missing (S203, S204, S207, S208, S212, S214-S221, S226, S227, S229,
S232-S234, S240, S241, S245-S248). The report's `reg-ids`/`staged-ids` files are not in `a2w1/AsmGate/` (the directory
holds `id-collisions.txt` and `quarantine-slice` only), so its 183 cannot be reproduced from its own receipts. The
verdict the seat drew (`Assimilation: none`) is unaffected — it does not rest on the collision count — but the number
and its receipt are wrong.

## 1.5 Mistake found this wave (c) — D7 closed at the file, not at the citation

`git ls-tree -r --name-only 18389f44 | grep -c 'round-44/.*ready'` → `4`; `raw.json.gz` and
`strace-rev-live1.log.gz` are committed. But the citing text still names the uncompressed path
(`ScribeLesson/disposition-checks.txt`):

```
$ git cat-file -e 18389f44:.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log ; echo rc=$?
fatal: path '.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log' does not exist in '18389f44'
rc=128
$ git cat-file -e 18389f44:.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log.gz ; echo rc=$?
rc=0
```

`w1/C1ExecLiveRead/commands.txt:26,81` and `w2/SkillReview.md:55` name `strace-rev-live1.log`; those citations still do
not resolve from a clean checkout.

## 1.6 Round-44 routed defects D1-D10 at `18389f44` (receipt `ScribeLesson/disposition-checks.txt`)

| Defect | State | Evidence |
|---|---|---|
| D1 IN-109 repin + adjacency receipt | **closed** | `inbound[108].found_line` = 2582 = quote line at `ea6e0ee3`/`18389f44`; adjacency gate `PASS`, `findings []` (`ScribeLesson/adjacency-18389f44.json`, exit 0) |
| D2 SKILL SR8 sweep | **open** | `SKILL.md:4225` still "`memparse` (K/M/G suffixes …)" as fact; `git diff --name-only 5bbd5ff5 18389f44 \| grep -c '^SKILL.md$'` → 0 |
| D3 C2 unadmitted mark | **partial** | entry marked (`btrfs-scrub-record-r44.md:153` "## Round-45 grounding and gate status"); `corpus/README.md:434` and `SKILL.md` unchanged from base |
| D4 planned row stale | **open** | `SCORECARD.md:2840-2844` ≡ `:2739-2743` (`diff` rc=0); no round-45 planned row (`grep -c 'Round 45 planned'` → 0) |
| D5 self-assessment tip receipt | **open** | `after/` empty; only `before/self-assessment-base.txt` (`requested_revision 5bbd5ff5…:363`) |
| D6 report sections | r44 closed as defect; r45 pending | round-44 headings greps are 0/0; `.ufo/reports/round-45/` holds eight other lanes' reports, no `tsukuroi.md` |
| D7 untracked r44 evidence | **partial** | evidence committed; three citations stale (§1.5) |
| D8 rejects in Gate | draft in this file | §2 Gate carries the reject table |
| D9 AsmGate locator | **closed in the dispatch text** | a2w1 AsmGate item: "note the staged entries sit under knowledge/corpus/knowledge/, round-44 closure D9"; no lane prose carries it (`grep -c knowledge/corpus/knowledge` on `18389f44:SKILL.md` → 0) |
| D10 LOG freshness line | **open** | `git show 18389f44:LOG.md \| grep -c 'round 45'` → 0; last entry `:1615 "## Round 44 …"` |

## 1.7 C2's counted state at drafting (not a verdict)

Counted seats with reports in `a2w1/`: `C2CritGR1` "ROW GR1 VERDICT: holds", `C2RevGR3` "ROW GR3 VERDICT: holds",
`C2CritGR3` "ROW GR3 VERDICT: holds", `C2CritGR2` "ROW GR2 VERDICT: partly". `C2RevGR1.md` and `C2RevGR2.md` do not
exist yet, so no row is bound at the time of this draft; the GR2 `partly` implies a residual seat in a2r1 (declaration,
"Round 45 — attempt-2 rebinding"). The lesson says this and nothing more.

# 2. Proposed text — `corpus/lessons/round-45.md` (exact Markdown; not written to the lane)

````markdown
# Round 45 — lesson (tsukuroi, hyaku run 9)

author: tsukuroi L1 (`TsukuroiR45a2`), 2026-10-27. Base `5bbd5ff588120fd8e7c744695351a6978b4241c1` (the lane tip at
round start), freeze `ea6e0ee38d8066663bb0871b53bade14441eb304` (declaration, frozen counters, pre-data controls,
frozen sources S246-S249), implementation `18389f44cf6ce414d7be205998b29c79fb0b490c`. Claims, controls and the
attempt-2 rebinding: `SCORECARD.md` "Round 45 — declaration" and "Round 45 — attempt-2 rebinding". One v2 wave,
`a2w1` (66 seats); attempt 1's `w1` died unfilled at the orchestrator session exit (14/66 spawned, 0 outputs, salvage
commit `5b3029bf`), so attempt 1 scored nothing. Seats are the lane, not outside reviewers (LEARNING.md); the
non-author closure is pending.

## Frozen claims

| Claim | Axis | Surface | Counter (sha256 at the implementation) | Predicate | Kill rule |
|---|---|---|---|---|---|
| C1 | operability | `tools/tsukuroi-census.sh`: the five production readers that keep the first line of a captured output take it by parameter expansion instead of `printf '%s\n' "$CAP_OUT" \| head -n1` (exit 141 under `set -euo pipefail` past the pipe buffer), plus six `(R45-C1)` selftest cases that put the deciding line before ~150 KB of padding (selftest 148 → 154) | `tools/score-census-readers-r45.py` `fe0e31e25c5b3c92…a3250bd50` (unchanged since the freeze) | `lexical_hits == 0 and sites_found == 5 and equiv_ok == 5 and selftest_pass == 1 and selftest_r45 >= 6 and revert_killed == 6 and adjacency_ok == 1` | any PLANE/HANDOFF/DRIFT/STORAGE/SCRUB/TSUKUROI_CENSUS line shape or live exit code changes base → IMPL (other than live drift recurring between two runs of one revision); a predecessor census counter PASS → FAIL; the census writes a file in live mode |
| C2 | depth (sourced) | `corpus/knowledge/btrfs-scrub-grounding-r45.md` rows GR1 (`memparse` parses the `scrub_speed_max` write), GR2 (device replace runs `btrfs_scrub_dev` with `is_dev_replace` true; non-replace scrubs refused with `EINPROGRESS` during a replace), GR3 (`systemctl stop` of the packaged scrub service under systemd v262: SIGINT to the control group, SIGCONT, SIGKILL after `TimeoutStopSec`, 5 s here) on S246-S249 | `tools/check-scrub-grounding-r45.py` `7e373196decd2de0…841eabf70d` at `18389f44`; `a1eb402dffae97fc…08d011331` from `057c1804` (attempt-2 rebinding of the two wave-name literals `w1`/`r1` → `a2w1`/`a2r1` only; predicate, kill rule and target unchanged) | `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1` | a counted seat verdict that falsifies a row; or the C2 control battery accepting a should-fail control |

Measured state while this draft was written (seat receipts; the L1's `.ufo/waves/round-45/after/` was still empty):

- **C1 PASS at `18389f44`** — `lexical_hits 0`, `sites_found 5`, `equiv_ok 5`, `selftest_pass 1`, `selftest_r45 6`,
  `revert_killed 6`, `adjacency_ok 1`, selftest line `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)`,
  census sha256 `237b21c9…31b5fcdc`
  (`.ufo/waves/round-45/a2w1/C1ExecRerun/c1-after-1.jsonl`; a second run, `c1-after-2.jsonl`, is field-identical).
  Base census `17c82406…0e81a35`, base selftest `PASS (148 cases…)` (`before/census-selftest-base.txt`). No counter
  receipt at base exists in the wave's records; base discrimination is established two ways: the pre-data control K0
  (do-nothing on base bytes) is red — `lexical_hits 5`, `equiv_ok 0`, `selftest_r45 0`, `revert_killed 0`,
  `adjacency_ok 0`, verdict `FAIL` (`controls/C1-K0.jsonl`), battery `should_fail_accepted 0`, `control_accepted 1`
  (`controls/battery-summary-c1.jsonl`); and the base-graft seat ran the six new cases on the base readers, where the
  five reader cases fail with exit 141 and the foreign-baseline case passes (`a2w1/C1ExecBaseKill.md`), i.e. that sixth
  case is a regression guard, not a base/impl discriminator.
- **C2 not counted at drafting** — four of the six counted seats had reports (`C2CritGR1` GR1 `holds`, `C2RevGR3` and
  `C2CritGR3` GR3 `holds`, `C2CritGR2` GR2 `partly`); `C2RevGR1`/`C2RevGR2` were absent, so no row was bound. The GR2
  `partly` implies a residual seat in a2r1.

## Gate

### New SOURCES rows <!-- F-1: exact Markdown from .ufo/waves/round-45/a2w1/SrcGateNew.md §2; that seat re-opened all four URLs at 2026-10-27T03:30:32Z and reported live bytes equal to frozen/src/SHA256SUMS -->

| Row | URL (access 2026-10-27) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S246 | <!-- F-1 --> | <!-- F-1 --> | <!-- F-1 --> |
| S247 | <!-- F-1 --> | <!-- F-1 --> | <!-- F-1 --> |
| S248 | <!-- F-1 --> | <!-- F-1 --> | <!-- F-1 --> |
| S249 | <!-- F-1 (own-work capture; capture.txt lines) --> | <!-- F-1 --> | <!-- F-1 --> |

Snapshot digests: <!-- F-1: `.ufo/waves/round-45/frozen/src/SHA256SUMS` (five src files + digests), fetch log
`FETCH.txt`, `capture.txt`/`capture.sh` digests, live re-fetch date -->

### Re-opened rows and rows touched old→new <!-- F-2: exact text from .ufo/waves/round-45/a2w1/SrcGateReopen.md §4 -->

| Row | Change (this round) | Log |
|---|---|---|
| S237 | `used-by` gains `btrfs-scrub-grounding-r45.md` (column 11 only) | <!-- F-2 --> |
| S242 | same | <!-- F-2 --> |
| S243 | same | <!-- F-2 --> |
| S244 | same | <!-- F-2 --> |

Rows 245 → 249: `git show <REV>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` prints 245 at
`5bbd5ff5` and 249 at `18389f44`; the four new rows are S246-S249 (each 11 cells).

### Reject rows (routed defect D8: rejects are recorded here, not only under spot-check candidates)
<!-- F-1 §3 -->

| Entry (staged id) | Rejected | Reason (source-checked) | Flip |
|---|---|---|---|
| `btrfs-ioctl-surface-r27.md` (staged S223) | <!-- F-1 §3 --> | <!-- F-1 §3 --> | <!-- F-1 §3 --> |
| `ext4-journal-guarantee-r32.md` (staged S269/S270) | <!-- F-1 §3 --> | <!-- F-1 §3 --> | <!-- F-1 §3 --> |

`initramfs-hook-api-r25.md` stays refused-conditional and is not a reject row.

Census (frozen commands): <!-- F-2 §5: sources-census validate exit code and W04 count, base → impl -->

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R45-LESSON-ADJ-IN109-DRIFT | gate discipline — a moved line with no repin | IN-109's `found_line` and the census line of its quote disagree after a census insertion unless repinned; seven commits across six rounds, measured per commit: 2216 (r19-20) → 2277 (`4ac5ebaa`, r32) → 2346 (`e2f97e6e`, r35) → 2411 (`52ffd65f`, r38) → 2425 (`02eeed07`) → 2447 (`49cc53c7`, r39) → 2452 (`a2d7aad7`, r39) → 2465 (`44766208`, r42) → 2468 (`78abb8b5`) → 2579/2580/2582 (`ab8aae16`, `071ab0d1`, `9608ebc3`, r44) with the anchor still at 2468 through `8eee79db`, `fbfef071`, `e9ca7ef6` and the base `5bbd5ff5`. `git log --oneline -- corpus/knowledge/adjacency-anchors-r19.json` shows a repin in every round but 44 | none for the class until round 45; round 44's seat CritNoHarmFinal captured the instance (`w2/CritNoHarmFinal/adjacency-tip.txt`, `status FAIL` at `8eee79db`) and the round routed it (closure D1) instead of landing it | D1 repin 2468 → 2582 at `ea6e0ee3`, plus C1's adjacency kill rule (`tools/score-census-readers-r45.py:313-328`: `check-adjacency-anchors.py --revision REV`, `adjacency_ok = rc == 0 and status == PASS`). Able to fail: control C1-K7 (one comment line inserted above the IN-109 case) scores `adjacency_ok 0`, `status FAIL`, `findings ["INBOUND-CLASSIFICATION-WRONG"]`, `exit 1` (`controls/C1-K7.jsonl`); the same leg prints `PASS`, `findings []` at `18389f44` |
| R45-REPORT-MINIMUM-SECTIONS | delivery — report conformance | The round-44 report has no `## Sources & frontier` and no `## Trend verdicts`: `grep -c '^## Sources & frontier' /home/vgpnk/Projects/shokunin/.ufo/reports/round-44/tsukuroi.md` → 0, `grep -c '^## Trend verdicts' …` → 0; its headings are Outcome, Work performed, No-harm and checks, Incidents, Tooling, SHONEN, Next | none until the round-44 closure (D6) | The report is assembled from the wave's report-seat drafts; the template names both sections as required minimum content (`templates/round-prompt.md:111,116`). Able to fail — weakly: the only check is a heading grep, because the marker rule exempts exactly these two sections (`:122-125`) and the watchdog "does not check trend verdicts" (`:127-128`); no gate goes red for this class |
| R45-C2-GR2-HOST-READING | depth-overreach — a true citation plus a false inference | `corpus/knowledge/btrfs-scrub-grounding-r45.md:88-89` says "the caller has no effective capabilities (capture.txt:1): no replace or scrub state is observable to this caller". As uid 1000, `devinfo/1/replace_target` (mode 444, value `0`) and `exclusive_operation` (mode 444, value `none`) read successfully. Three wave seats flag the sentence: `a2w1/C2ExecHostRecheck.md` §1/§3, `a2w1/C2CritGR2.md` (with `sysfs.c:1288,2007-2029`), `a2w1/C2RevEntryWhole.md` finding 2 (the universal "any device" refusal is also unsupported by the quoted lines) | wave a2w1 seats C2ExecHostRecheck, C2CritGR2, C2RevEntryWhole; the freeze did not catch it | Narrow the sentence to what the captured lines support (or cite the readable attributes), and narrow GR2's universal refusal to calls that pass the earlier device and writability checks. Able to fail: the attribute reads contradict the frozen sentence verbatim; the counter's `host_ok` leg cannot, because it binds only "existing, non-empty capture.txt lines" (`tools/check-scrub-grounding-r45.py:27`) — a recorded limit, not a passing check |
| R45-ASMGATE-IDCENSUS | evidence — a receipt that does not back its number | `a2w1/AsmGate.md` reports "183 registry ids, 147 staged ids, 30 intersections"; the same revision holds 249 registry rows/ids (S001-S249) and a true intersection of 50 (S200-S249). The kept `a2w1/AsmGate/id-collisions.txt` lists 5 ids that are not lane registry ids (S250, S251, S252, S262, S268) and omits 25 genuine collisions; the report's `reg-ids`/`staged-ids` files are absent from `a2w1/AsmGate/` | none in-wave; recomputed by the round-45 lesson seat | Recount with the lane extractor and keep both id lists beside the collision set. Able to fail: a recount against the kept receipt flags the five non-registry ids and the 25 missing ones |
| R45-D7-CITATION-HALF-CLOSED | repair closed at the file, not at the reference | `ea6e0ee3` commits the round-44 evidence (`raw.json.gz`, `strace-rev-live1.log.gz`, three tarballs, four `.ready` files), but `w1/C1ExecLiveRead/commands.txt:26,81` and `w2/SkillReview.md:55` still cite `strace-rev-live1.log`; `git cat-file -e 18389f44:<that path>` is `rc=128`, the `.log.gz` is `rc=0` | none; `a2w1/ScoutR44Defects.md` marks D7 "done" after testing the `.gz` path only | Point the three citations at the committed `.gz` (or commit the log uncompressed). Able to fail: `git cat-file -e <REV>:<cited path>` returns 128 for the cited path and 0 for the committed one |

## Round-44 routed defects — round-45 disposition

| Defect | State at `18389f44` | Evidence |
|---|---|---|
| D1 IN-109 repin + adjacency receipt | closed | `found_line` 2582 = census line 2582 at `ea6e0ee3` and `18389f44`; `check-adjacency-anchors.py --revision 18389f44…` → `status PASS`, `findings []`, `inbound_total 114`, `live_object_match 10` |
| D2 SKILL SR8 sweep | open | `SKILL.md:4225` still states "`memparse` (K/M/G suffixes, trailing whitespace skipped, else `-EINVAL`)" as fact; `git diff --name-only 5bbd5ff5 18389f44 \| grep -c '^SKILL.md$'` → 0 |
| D3 C2 unadmitted mark | partial | entry marked at `btrfs-scrub-record-r44.md:153` (gate FAILED, SR7-SR9 pending); `corpus/README.md:434` and the `SKILL.md` r44 section are byte-identical to base |
| D4 planned row stale | open, draft pending | `SCORECARD.md:2840-2844` ≡ `:2739-2743` (`diff` rc=0); no round-45 planned row (`grep -c 'Round 45 planned'` → 0) |
| D5 self-assessment tip receipt | open | `.ufo/waves/round-45/after/` empty; only `before/self-assessment-base.txt` (`requested_revision 5bbd5ff5…`, line 363) |
| D6 report sections | r44 closed as a defect; r45 pending | the two headings are absent from the round-44 report; `.ufo/reports/round-45/` holds eight other lanes' reports and no `tsukuroi.md` — the round-45 report is still to be written with both sections |
| D7 untracked r44 evidence | partial | four `.ready` files and the gz evidence committed; the citations still name the uncompressed log |
| D8 rejects in Gate | repaired in this lesson | the reject table above |
| D9 AsmGate locator / staged-id hazard | closed in the dispatch text, not in a lane file | the a2w1 AsmGate item names the staged location ("note the staged entries sit under knowledge/corpus/knowledge/, round-44 closure D9"); no lane prose carries it yet |
| D10 LOG freshness line | open | `git show 18389f44:LOG.md \| grep -c 'round 45'` → 0; the last entry is `:1615 "## Round 44 …"` |

Conflicts recorded verbatim for the canonical judge:

- `a2w1/ScoutR44Defects.md` marks D7 "done" ("the cited strace log and raw capture therefore resolve from that
  commit") after testing `<path>.log.gz`; the paths the two round-44 files cite are the uncompressed ones, which fail
  `git cat-file -e` (`rc=128`).
- `a2w1/ScoutR44Defects.md` marks D3 "done" on the entry alone; `corpus/README.md:434` and the `SKILL.md` row that D3
  also names are unchanged from base.
- `a2w1/AsmGate.md` reports 183 registry ids and 30 intersections; the same revision's `corpus/SOURCES.md` has 249 ids
  and the true intersection is 50.

## Spot-check candidates for the non-author closure

One admit per claim: C1 — the live read-only probe and the plane diff (`a2w1/C1ExecLiveRead.md`,
`a2w1/C1ExecPlaneDiff.md`) together with the counter's PASS at `18389f44`; C2 — GR1's executable `memparse` harness
(`a2w1/C2ExecMemparseHarness.md`) and GR2's caller table (`a2w1/C2ExecKernelGR2.md` §1). One reject candidate: the
staged `btrfs-ioctl-surface-r27.md` (S223), carried since round 42 — a nine-row ioctl table stated as closure against
64 dispatch labels at the lane's pinned tag.
````

# 3. Out of scope, not done, limits

- I did not run the C1 counter or the census selftest (the wave's own receipts at `18389f44` were cited instead); the
  L1's `after/` receipts are still empty, so the round's official numbers are not in this draft.
- I did not write `corpus/lessons/round-45.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, the round report, or anything else
  tracked; the Gate rows are placeholders because F-1/F-2 own that text (their reports exist and are named in the
  placeholders; I did not re-verify their live fetches).
- C2's counted verdicts are not mine to state: two counted seats had no report at drafting (§1.7), and I recorded no
  verdict of my own.
- The lesson's `Mistakes` rows quote wave seats' findings as findings; I verified the GR2 sysfs claim and the AsmGate id
  count myself and marked which parts rest on the seats.
- `AsmGate.md`'s `183` may come from an extractor I could not reconstruct; I report the mismatch with the recipe I ran
  rather than a cause.

## Receipts

- `.ufo/waves/round-45/a2w1/ScribeLesson/drift-table.txt` — per-commit IN-109 quote line vs `found_line`.
- `.ufo/waves/round-45/a2w1/ScribeLesson/adjacency-18389f44.json` — gate output at the implementation.
- `.ufo/waves/round-45/a2w1/ScribeLesson/id-census.txt` — registry/staged id counts and the collision diff.
- `.ufo/waves/round-45/a2w1/ScribeLesson/host-replace-attrs.txt` — read-only sysfs reads as uid 1000.
- `.ufo/waves/round-45/a2w1/ScribeLesson/disposition-checks.txt` — D1-D10 commands and outputs.
