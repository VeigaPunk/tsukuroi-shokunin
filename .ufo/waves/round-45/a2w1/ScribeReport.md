VERDICT: defect-found

# Item X-9 — round-45 report skeleton (routed defect D6)

Routed defect **D6 R44C-REPORT-SECTIONS** (`corpus/lessons/round-44-verifier-spotcheck.md:181-183`, §1 table row
"Report minimum content (prompt §4)"): the round-44 report carried no **Sources & frontier** section, no **Trend
verdicts** section, no per-claim counting command, and no per-change `LOG.md` tie; its `## SHONEN` heading arrived
in a follow-up commit (`0e363a51`) instead of with the body.

This file drafts the round-45 report with every required section present **in the prompt's order**, filled from
**committed** receipts only, with every unlanded value marked `<PENDING — …>`. It is a draft: the L1 lands the
report at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-45/tsukuroi.md` (fleet repo) through
`fleet-commit.sh --as tsukuroi`, after the wave integration and the after-receipts exist. Nothing here is a
verdict on C1 or C2 beyond what the cited receipts already printed.

## 1. What the contract requires, and where the draft satisfies it

| Requirement | Source | Draft section |
|---|---|---|
| Opens by naming the round's 1-3 declared claims and their axes | prompt §4 | `## Work performed`, first paragraph |
| One bullet per work item with an evidence pointer | prompt §4 | `## Work performed` |
| Every change tied to a `LOG.md` entry and to its commit hash | prompt §4, D6 | `## Landed changes` (two columns: commit, LOG tie) |
| One measurement per claim with its counting command and measured commit | prompt §4, D6 | `## Before → after measurements` |
| `SOURCES.md` rows before→after with the counting command | prompt §4, §6 item 10 | `## Sources & frontier` |
| Assimilation line (or `Assimilation: none`) | prompt §6 item 10 | `## Sources & frontier`, last rows |
| One verdict each for `expansion`, `quality`, `discernment` | prompt §4 | `## Trend verdicts` |
| One line per `SHONEN.md` box, `[x]`/`[~]`/`[ ]` | prompt §4 | `## SHONEN` (4 boxes; `SHONEN.md:5,7,9,11`) |
| `Stale-lane` line | prompt §6 item 6 | `## Stale-lane` |
| Tool installs | prompt §6 item 6 | `## Tool installs` |
| Round shape, seat count, role mix, dead seats, residual, total | prompt §6 item 2 | `## Round shape, seats, routing, incidents` (after the contract sections, as in round 43) |

`SHONEN.md` boxes, verbatim (`grep -n '^- \[' SHONEN.md` → 4 lines, all `[~]`): line 5 "SKILL.md contains real
decision tables, error patterns, checklists, cited sources"; line 7 "At least one end-to-end domain task executed and
logged in LOG.md"; line 9 "Instructions executable by an agent without oral context"; line 11 "No cross-domain bleed
(PROVINCE.md still accurate)".

Two sections of the draft are **additions, not substitutes**: `## Outcome` (a one-table summary, as in the round-43 and
round-44 reports) sits before `## Work performed`, and `## Round shape, seats, routing, incidents` sits after
`## Tool installs` because prompt §6 item 2 requires the shape, seat count, role mix, dead seats, residual call and
round total in the report. Neither displaces a contract section, and the contract sections keep the prompt's order.

## 2. Draft — exact Markdown

Everything between the fences is the proposed report. `<PENDING — …>` is a placeholder the L1 replaces; a section
with a placeholder is not yet evidence.

````markdown
# tsukuroi — round 45 report (hyaku run 9, attempt 2)

L1: `TsukuroiR45a2` (canonical §3 planner seat; see "Round shape"). Lane repo
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, branch `master`.

- Base `5bbd5ff588120fd8e7c744695351a6978b4241c1` — the lane tip at round start as `jj-lane.sh state` printed it; it
  carries the round-44 non-author spot-check.
- Freeze `ea6e0ee38d8066663bb0871b53bade14441eb304` — declaration, both frozen counters, pre-data control batteries,
  frozen sources S246-S249, base gate receipts, the D1 IN-109 repin and the D7 round-44 evidence commit.
- Implementation `18389f44cf6ce414d7be205998b29c79fb0b490c` — C1 census readers and selftests, C2 entry and registry rows.
- Attempt-2 rebinding `057c1804`; wave `a2w1` spec/dispatch/registry `3c42f556`. Orchestrator salvage of attempt 1:
  `5b3029bf`.
- Final lane hash `<PENDING — the wave-integration commit, read from jj-lane.sh state (local=…) and confirmed with git ls-remote origin refs/heads/master>`.

Wave evidence is `.ufo/waves/round-45/` in the lane (`W/` below), committed as wave evidence. Attempt 1 of this round
(L1 `TsukuroiR45`, wave `w1`) died with the orchestrator session at 2026-10-26 23:57:36 -03: 66 seats, 14 spawned,
0 outputs, 0 reports (`W/w1-results.json`); its `W/w1/` tree holds nothing citable and no seat scored. Attempt 2 is
this report's subject; what it inherited and re-verified is named under **Work performed**.

## Outcome

| Claim | Axis | Before (base `5bbd5ff5`) | After (`<PENDING measured hash>`) | Verdict |
|---|---|---|---|---|
| C1 — the five census first-line readers by parameter expansion, plus six `(R45-C1)` selftest cases | operability | FAIL — `lexical_hits 5, sites_found 5, equiv_ok 0, selftest_pass 1, selftest_r45 0, revert_killed 0, adjacency_ok 0` (`W/controls/C1-K0.jsonl`, the do-nothing control at base) | `<PENDING — the frozen counter at the wave-tip revision; at the implementation revision 18389f44 it already reads lexical_hits 0, sites_found 5, equiv_ok 5, selftest_pass 1, selftest_r45 6, revert_killed 6, adjacency_ok 1, selftest 154/154 (`W/a2w1/C1ExecRerun/c1-after-1.jsonl`, `-2.jsonl`)>` | `<PENDING — PASS iff the tip receipt repeats that line and no kill rule fires>` |
| C2 — `corpus/knowledge/btrfs-scrub-grounding-r45.md` rows GR1-GR3, each grounding one round-44 `[inference]` | depth (sourced: S246-S249) | FAIL — `rows 0` (`W/before/c2-before.jsonl`, exit 1) | `<PENDING — the frozen counter at the wave-tip revision; the predicate needs verdicts_ok 3, i.e. bound counted reads C2RevGR1-3 and C2CritGR1-3 in wave a2w1>` | `<PENDING — PASS iff rows 3, quotes 3, props 3, host 3, sources 1, verdicts 3, novelty 0, pointer 1>` |

Frozen counters (unchanged since the freeze except the C2 wave-name literals):

| Counter | sha256 | Note |
|---|---|---|
| `tools/score-census-readers-r45.py` | `fe0e31e25c5b3c92cc5aace48acc56bc6dab39b4b3c09b49708a715a3250bd50` | unchanged by the rebinding |
| `tools/check-scrub-grounding-r45.py` | `a1eb402dffae97fcefd9bd539529f1cacc5034419b6de06e1f8ac1c08d011331` | `7e373196…f70d` at the freeze → rebound `w1`/`r1` → `a2w1`/`a2r1` at `057c1804`; predicate, kill rule and target unchanged (`SCORECARD.md` "Round 45 — attempt-2 rebinding") |

## Work performed

The round declares two claims: **C1 operability** — the five production census readers that keep the first line of a
captured output stop using `printf '%s\n' "$CAP_OUT" | head -n1` inside an assignment (exit 141 under
`set -euo pipefail` once an output passes the pipe buffer) and take the first line by parameter expansion, with six
`(R45-C1)` selftest cases (148 → 154); **C2 depth** — a sourced entry grounding the three `[inference]` marks the
round-44 entry left, with counted reviewer and critic verdicts bound to each row. C1 moves operability, C2 moves
depth; adjacency is unclaimed and carried as C1's kill rule (`SCORECARD.md:2847-2891`).

- **Protocol load.** Shokunin and swarm skills; MISSION, AXES, PROTOCOL, CORPUS, LEARNING; the lane's `SKILL.md`,
  `PROVINCE.md`, `SCORECARD.md` (planned row), `corpus/QUALITY.md`, `corpus/README.md` "Frontier", the newest lessons,
  `corpus/lessons/round-44-verifier-spotcheck.md` and `considerthese/2026-10-26.md`. The declaration at
  `SCORECARD.md:2847-2891` answers D4 (its planned row is replaced, not restated) and names D1 as repaired inside the
  freeze commit; **D5** (a self-assessment receipt at the measured revision) and **D6** (this report's sections) are
  this round's remaining closure items, and D2/D3/D7-D10 are carried below or in the lesson.
- **Freeze `ea6e0ee3`.** Declaration, both frozen counters, pre-data controls, frozen sources with `SHA256SUMS` and
  `FETCH.txt`, base gate receipts, the **D1** IN-109 repin (2468 → 2582) and the **D7** round-44 untracked evidence.
  Evidence: `W/frozen/src/SHA256SUMS`, `W/frozen/hostcap/`, `W/before/`.
- **D1 adjacency repair (routed defect R44C-ADJ-IN109).** Base gate: `W/before/adjacency-base.txt` reads
  `status FAIL`, `INBOUND-CLASSIFICATION-WRONG` at `adjacency-anchors-r19.json:inbound[108]`. At the implementation
  revision: `python3 tools/check-adjacency-anchors.py --revision 18389f44…` reads `status: PASS`, `findings: []`,
  `inbound_total 114`, `outbound_total 10`, `live_object_match 10` (`W/a2w1/AdjPins.md`), and the C1 counter's
  `adjacency_ok` leg reads 1 (`W/a2w1/C1ExecRerun/c1-after-1.jsonl`).
- **Pre-data controls.** C1 battery K0-K10 and C2 battery K0-K29, scored with the frozen counters before any seat.
  Evidence: `W/controls/battery-summary-c1.jsonl`, `W/controls/battery-summary-c2.jsonl`, per-control receipts
  `W/controls/C1-K*.jsonl`, `W/controls/C2-K*.jsonl`, generators `W/controls/run_controls_c1.py`. Observed
  `should_fail_accepted 0, control_accepted 1` on both batteries: every must-FAIL control was refused and the
  candidate (and, for C1, the `sed -n 1p` full-read alternative K9) accepted.
- **Attempt-1 loss, salvage and rebinding.** `W/w1-results.json` records the orchestrator session exit and the
  14/66/0 numbers; the salvage commit `5b3029bf` holds them. The C2 counter's two wave-name literals were rebound to
  the live wave at `057c1804`: the battery re-run `W/controls-a2/battery-summary-c2.jsonl` is field-identical to the
  frozen one on all 30 controls (`should_fail_accepted 0`; K3/K19/K26 PASS), and the salvage tip scores FAIL
  `verdicts_ok 0` under both the frozen and the rebound counter (`W/controls-a2/salvage-tip-frozen-ea6e0ee3.jsonl`,
  `W/controls-a2/salvage-tip-amended.jsonl`) — attempt-1 records bind nothing.
- **Implementation `18389f44`.** Five readers converted at `tools/tsukuroi-census.sh:965` (`state`), `:1003` (timer
  `Result` `r`), `:1085` (`driver`), `:1460` (`t_word`), `:1535` (timer `ActiveState` `r`), each tagged `(R45-C1)`;
  six selftest cases at `:3342, :3347, :3355, :3360, :3365, :3374`, the sixth driving the foreign-baseline lookup past
  the pipe buffer. Evidence: the `selftest_line` in `W/a2w1/C1ExecRerun/c1-after-1.jsonl` reads
  `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)`; base receipt `W/before/census-selftest-base.txt`
  reads 148.
- **C2 entry `corpus/knowledge/btrfs-scrub-grounding-r45.md`.** GR1 `:14`, GR2 `:55`, GR3 `:91`, "How this changes OS
  triage" `:129`, "Limits" `:141`, "QUALITY check" `:150`; the round-44 entry gains the appended section
  `## Round-45 grounding and gate status` at `btrfs-scrub-record-r44.md:153` (spot-check D3).
- **Wave `a2w1` — one v2 wave.** 66 seats dispatched in one `task` call from `W/a2w1-dispatch.json` (spec
  `W/a2w1-spec.json`, ready marker `W/a2w1.ready` taken at `W/a2w1.ready.dispatched`). Role mix and dead seats:
  see **Round shape**.
- **Wave integration `<PENDING — commit hash>`.** `<PENDING — one bullet per integrated finding, each with the seat
  report path under W/a2w1/ and the source line or command that decides it>`.
- **Documentation `<PENDING — commit hash>`.** `<PENDING — PROVINCE promotion block, SKILL sections, corpus/README
  round-45 coverage note, round45 registry table (RegistryDraft)>`.
- **Scorecard, log, lesson, report `<PENDING — commit hashes>`.** `<PENDING — SCORECARD "Round 45 — measured
  outcome", axes and capabilities tables, LOG "Round 45", corpus/lessons/round-45.md>`.
- **Assimilation and considerthese.** Read-only evaluation of `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/`
  (`W/a2w1/AsmGate.md`): **adopt nothing** — 30 id collisions with the lane registry (S200-S202, S205, S206,
  S209-S211, S213, S222-S225, S228, S230, S231, S235-S239, S242-S244, S249-S252, S262, S268) including the staged
  S242-S249 subset, no theme fit to this round's three surfaces, a 13-row quarantine slice, and staged **S230**
  rejected for a citation with no locator. considerthese "Seat-harm incident log" mined into
  `<PENDING — corpus/lessons/round-45.md section>` (`W/a2w1/ConsiderMine/seat-harm.jsonl`).
- **No-harm checks `<PENDING — final receipts>`.** `<PENDING — plane diff, predecessor counters, live read-only leg,
  and the three receipts that must not move: check-self-assessment, check-adjacency-anchors, sources census>`.
  Known at the implementation revision: `check-self-assessment` FAIL 4 mismatches — K07 (`65 notes` stated vs 66 held),
  K10 (carried: `64 lesson files` vs 65), K13 and K17 (`148 cases` stated vs the selftest's 154)
  (`W/a2w1/SelfAssess/self-assessment-18389f44.jsonl`, base 1 mismatch in `W/a2w1/SelfAssess/self-assessment-base-5bbd5ff5.jsonl`);
  and the registry gap gate FAIL with 2 unregistered tools, 70/70 registered rows over 72 tools
  (`W/a2w1/RegistryDraft/gap-18389f44.json`). Both must be repaired or carried as recorded defects, not silently.

## Landed changes

Every row names the commit that carries it and the `LOG.md` entry that records it. `LOG.md` has no round-45 entry
yet, so the tie is a placeholder until the round-45 entry lands; a row without both is not landed evidence.

| Commit | Change | LOG tie |
|---|---|---|
| `ea6e0ee3` | Declaration and both frozen counters; C1 controls K0-K10 and C2 controls K0-K29; frozen S246-S249 (`SHA256SUMS`, `FETCH.txt`); base gate receipts; D1 IN-109 repin 2468 → 2582; D7 round-44 untracked evidence committed | `<PENDING — LOG.md "Round 45" lock>`, rows "freeze" |
| `18389f44` | C1: five census readers by parameter expansion, six `(R45-C1)` cases (148 → 154); C2: `btrfs-scrub-grounding-r45.md` GR1-GR3, r44 entry `## Round-45` append, SOURCES S246-S249 and used-by on S237/S242/S243/S244 | `<PENDING — LOG.md "Round 45" lock>`, rows "C1", "C2 draft" |
| `057c1804` | C2 counter wave-name rebinding `w1`/`r1` → `a2w1`/`a2r1`; C2 battery re-run (30/30 field-identical); salvage-tip receipts; SCORECARD rebinding note | `<PENDING — LOG.md "Round 45" lock>`, row "rebinding" |
| `3c42f556` | Wave `a2w1` generator, spec, validated v2 dispatch (66 seats), registry draft | `<PENDING — LOG.md "Round 45" lock>`, row "wave dispatch" |
| `5b3029bf` | Orchestrator salvage of the unlanded attempt-1 `w1` spec and results record (not a lane landing; recorded so the attempt-1 evidence is citable) | `<PENDING — LOG.md "Round 45" lock>`, row "attempt 1" |
| `<PENDING>` | Wave integration `<PENDING>` | `<PENDING>` |
| `<PENDING>` | Registry row(s) for the two new counters (gap 70/72 → 72/72) | `<PENDING>` |
| `<PENDING>` | PROVINCE, SKILL, `corpus/README.md` round-45 note | `<PENDING>` |
| `<PENDING>` | SCORECARD outcome + axes + capabilities; `LOG.md` "Round 45"; `corpus/lessons/round-45.md` | `<PENDING>` |

## Before → after measurements

One per claim. The command is paste-ready from the lane root; `--lane` selects a sandbox clone when the lane itself
must not be written.

**C1 — counting command.**

```sh
python3 tools/score-census-readers-r45.py --revision <REV> --scratch <SCRATCH>
# fixture clone: --lane <clone> --revision <sha> --scratch <DIR>
```

- Legs: lexical (`lexical_hits`), per-site equivalence against the base statement on drawn outputs, selftest,
  six revert mutants, adjacency gate.
- **Before, base `5bbd5ff5`:** `FAIL` — `lexical_hits 5, sites_found 5, equiv_ok 0, selftest_pass 1,
  selftest_r45 0, revert_killed 0, adjacency_ok 0`, census selftest `PASS (148 cases…)`
  (`W/controls/C1-K0.jsonl`, the do-nothing control; `W/before/census-selftest-base.txt`).
- **After, implementation `18389f44`:** `PASS` — `lexical_hits 0, sites_found 5, equiv_ok 5, selftest_pass 1,
  selftest_r45 6, revert_killed 6, adjacency_ok 1`, census selftest `PASS (154 cases, 154 passed, 0 failed)`,
  exit 0 (`W/a2w1/C1ExecRerun/c1-after-1.jsonl` and `-2.jsonl`, two independent runs).
- **After, measured revision `<PENDING>`:** `<PENDING — the receipt in W/after/c1-final-<rev>.jsonl and its exit code>`.
- **Kill rules:** `<PENDING — shape diff of every PLANE/HANDOFF/DRIFT/STORAGE/SCRUB/TSUKUROI_CENSUS line and the live
  exit code between base and the measured revision; the six predecessor counters; the live-mode no-write leg>`.

**C2 — counting command.**

```sh
python3 tools/check-scrub-grounding-r45.py --revision <REV>
# fixture clone: --lane <clone> --revision <sha>
```

- Predicate: `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and
  verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1`.
- **Before, base `5bbd5ff5`:** `FAIL`, `rows 0`, exit 1 (`W/before/c2-before.jsonl`).
- **After, measured revision `<PENDING>`:** `<PENDING — rows, quotes_ok, props_ok, host_ok, sources_ok, verdicts_ok,
  novelty_base_hits, pointer_ok; receipt W/after/c2-final-<rev>.jsonl and its exit code>`.
- **Counted verdicts:** `<PENDING — per row GR1/GR2/GR3, the bound reviewer and critic verdicts from the counted
  seats C2RevGR<n>/C2CritGR<n> in wave a2w1, with each seat's report path under W/a2w1/>`; a `partly` row without a
  bound residual `holds` (wave `a2r1`) is a FAIL under the frozen rule.

**Supporting counts (author-side, not claim measurements).**

| Count | Before (base `5bbd5ff5`) | After (measured `<PENDING>`) |
|---|---|---|
| Census selftest cases | 148 (`W/before/census-selftest-base.txt`) | `<PENDING>`; 154 at `18389f44` (`W/a2w1/C1ExecRerun/c1-after-1.jsonl`) |
| `corpus/SOURCES.md` rows | 245 (`git show 5bbd5ff5:corpus/SOURCES.md \| grep -cE '^\|\[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`) | `<PENDING>`; 249 at `3c42f556` (same command) |
| Adjacency anchors | FAIL, `IN-109` (`W/before/adjacency-base.txt`) | `<PENDING>`; PASS at `18389f44` (`W/a2w1/AdjPins.md`) |
| Self-assessment mismatches | 1 (K10) (`W/before/self-assessment-base.txt`) | `<PENDING>`; 4 at `18389f44` (K07, K10, K13, K17) (`W/a2w1/SelfAssess/self-assessment-18389f44.jsonl`) |
| Registry coverage | `<PENDING — gap at base>` | `<PENDING>`; 70/70 rows, 72 tools, 2 missing at `18389f44` (`W/a2w1/RegistryDraft/gap-18389f44.json`) |

## Sources & frontier

| Item | Value |
|---|---|
| Command | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` |
| Start (round start) | `tsukuroi ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`, exit 0, 40 `W04` (duplicate URL across scopes, all older rows), 245 rows (`W/before/sources-census-start.txt`; row count `git show 5bbd5ff5:corpus/SOURCES.md \| grep -cE '^\|\[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 245) |
| End (round end) | `<PENDING — paste the same command's output and exit code; exit 0 required; receipt W/after/sources-census-final.txt>` |
| Rows added by tier | `A: 4` — S246 `code` (Linux v7.2.11 `lib/cmdline.c`, `lib/vsprintf.c`, `lib/kstrtox.c`), S247 `code` (`fs/btrfs/dev-replace.c`), S248 `docs` (systemd v262 `man/systemd.kill.xml`), S249 `own-work` (round-45 host capture) — 245 → 249 |
| Rows touched old→new | S237 `used-by`: `…r42.md, …r43.md, …r44.md` → same plus `…btrfs-scrub-grounding-r45.md`; S242, S243, S244 `used-by`: `…btrfs-scrub-record-r44.md` → `…r44.md, …btrfs-scrub-grounding-r45.md` (`git diff 5bbd5ff5 18389f44 -- corpus/SOURCES.md`) |
| Frontier rows advanced | none moved Frontier → Core this round. The scrub-record line's three `[inference]` marks are grounded (GR1 `btrfs-scrub-grounding-r45.md:14`, GR2 `:55`, GR3 `:91`); the Frontier bullet on `errno:13` root-dir mode and the mkinitcpio/btrfs-overlayfs item are untouched |
| Sourced claim | C2 rests on S246, S247, S248 and S249, all opened this round; each Gate entry carries this round's access date and a ≤25-word located quote (`corpus/lessons/round-45.md` "Gate" — `<PENDING — lesson path and Gate lines>`) |
| Assimilation | **none** — read-only evaluation (`W/a2w1/AsmGate.md`): 30 id collisions with the lane registry including the staged S242-S249 subset, no theme fit to the round's three surfaces, 13-row quarantine slice, staged S230 rejected (citation with no locator). No campaign tool was run; nothing under `/home/vgpnk/Projects/shokuknow` was written |
| considerthese | mined "Seat-harm incident log" (`considerthese/2026-10-26.md`), per-round seat-harm tally rounds 37-44 → `<PENDING — corpus/lessons/round-45.md section>`, receipts `W/a2w1/ConsiderMine/seat-harm.jsonl` |

## Trend verdicts

Author-side verdicts; the non-author closure re-derives each from committed bytes. One verdict per trend, no scalar.

- **expansion: `<PENDING — improved \| harmed \| unchanged \| unprovable-but-better>`.** `<PENDING — reason:
  no Frontier → Core move was declared (C1 is operability inside the existing census arm, C2 is depth), and no new
  capability row is claimed; if the wave adds a capability row the verdict must say so>`.
- **quality: `<PENDING>`.** `<PENDING — reason: GR1-GR3 ground the three `[inference]` marks of the round-44 entry
  (SR7 `btrfs-scrub-record-r44.md:21`, SR8 `:63`, SR9 `:151`) at pinned source lines; the wave's narrowings and the
  D2 SKILL SR8 sweep decide whether the verdict is improved or harmed>`.
- **discernment: `<PENDING>`.** `<PENDING — reason: the pre-data controls refused every must-FAIL control
  (`should_fail_accepted 0` both batteries); the counted C2 verdicts and the wave's rejected claims decide the
  verdict; a rejected claim with source evidence is improvement credit, a gate that accepted a false claim is harm>`.

## SHONEN

One line per box of `SHONEN.md` (`:5, :7, :9, :11`). `[x]` only with a named non-author verifier; `[~]` only with a
resolvable evidence pointer; `[ ]` if untouched. No box changed state this round; `SHONEN.md` itself is unedited.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources.
  `<PENDING — the round-45 SKILL sections and their line numbers; author-side, the wave-2 skill review seat is the lane,
  not a non-author>`.
- [~] At least one end-to-end domain task executed and logged in LOG.md.
  `<PENDING — LOG.md "Round 45": the census readers red-before at base, PASS at the measured revision; non-author
  replay still pending>`.
- [~] Instructions executable by an agent without oral context.
  `<PENDING — the paste-ready commands in the round-45 SKILL sections; a whole-SKILL retest is not executed>`.
- [~] No cross-domain bleed (PROVINCE.md still accurate).
  `<PENDING — W/a2w1/ConnSiblings.md and AdjPins.md: no tracked sibling pin matched; PROVINCE round-45 block at
  <PENDING lines>>`.

## Stale-lane

Stale-lane: this lane is driven respawn-per-round (`hyaku-inline`); attempt 2 is the only live mission of tsukuroi and
no other mission of this lane is open.

## Tool installs

None. No seat of wave `a2w1` installed or upgraded a tool, `pacman` was paused host-wide throughout, and no
`~/.local/bin` or other PATH entry was written. `<PENDING — confirm against W/a2w1/*.md at finalization: grep -rnE
'uv tool install|npx -y|pacman -S|cargo install|npm -g' W/a2w1/ → expected empty; earlier sweep at drafting time was empty>`.

## Round shape, seats, routing, incidents

- **Shape:** one v2 wave under `scripts/hyaku/ufo-wave-policy-v2.json` (`sighting.dispatch.swarm.waveMinLanes` 64,
  `waveMaxLanes` 128, `maxLanes` 256) — wave `a2w1`, 66 seats, dispatched as exactly one validated `task` call
  (`W/a2w1-dispatch.json`; `W/a2w1.ready` taken at `W/a2w1.ready.dispatched`).
- **Attempt 1:** wave `w1`, 66 seats, 14 spawned, 0 outputs, settled by the orchestrator session exit
  (`W/w1-results.json`); no seat of it scored, so it contributes no evidence and no verdict.
- **Role mix (a2w1, 66 seats):** executor 23, critic 13, reviewer 10, scribe 8, connector 4, mutation-tester 3,
  scout 3, sentinel 2. Attack roles (reviewer, critic, mutation-tester, labrat) 26/66 = 39 %.
- **Planner seat:** the L1 holds the canonical §3 planner seat; the bounded planning data-walk rode scout and
  connector items (`ScoutR44Defects`, `AdjPins`, `ConnClaims`, `ConnSiblings`, `ConnFrontier`, `ConnLessonQuality`).
- **Routing:** no `model` was passed; the role map in `~/.omp/agent/config.yml` decided each seat's route, and a seat
  keeps the route it captured at spawn.
- **Dead seats:** `<PENDING — from W/a2w1-results.json, with each dead seat's last error text>`.
- **Residual:** `a2r1` runs only if a counted row reads `partly`; its seats count in the round total.
- **Round total:** 132 seats dispatched across the two attempts (66 + 66), 66 of them in the live wave; the round's
  evidence rests on the live wave only.
- **Incidents:** attempt-1 session exit (SIGHUP during an operator-requested `omp update`), recovered as
  `W/w1-results.json` + `5b3029bf`; `<PENDING — misroot sweep result: git -C /home/vgpnk/Projects/shokunin status
  --porcelain, and each fleet-root file copied byte-exact into the lane with cmp and removed>`.
- **L0 questions:** `<PENDING — none opened, or the appended .ufo/l0-questions.md lines>`.
````

## 3. Placeholder inventory

Every `<PENDING>` in the draft, with the committed or receipted source that fills it. The L1 fills all of them
before `fleet-commit.sh`; a placeholder left in the landed report is a §4 minimum-content defect (prompt §4 marker
rule).

| Placeholder | Filled from |
|---|---|
| Final lane hash | `scripts/hyaku/jj-lane.sh state <lane>` (`local=`) + `git -C <lane> ls-remote origin refs/heads/master` (prompt §4 pre-report gate) |
| C1/C2 after values and verdicts | `W/after/c1-final-<rev>.jsonl`, `W/after/c2-final-<rev>.jsonl` made with `tools/run-receipt.py` |
| C2 bound per-row verdicts | the counted seats' reports + `W/a2w1-results.json`; the counter's `verdicts_ok` leg |
| Wave integration / registry / docs / scorecard/log/lesson commits | `jj-lane.sh commit` → its `landed <hash>` line only |
| `LOG.md` ties | the round-45 `LOG.md` entry as committed |
| Sources census end | `sources-census.sh validate --root … tsukuroi` output + exit code, row-count command |
| Kill-rule and no-harm receipts | plane diff, six predecessor counters, live read-only leg, self-assessment, adjacency, registry gap |
| `SHONEN` pointers | round-45 SKILL sections, `LOG.md` "Round 45", `W/a2w1/ConnSiblings.md`, `AdjPins.md`, PROVINCE block |
| Trend verdicts | derived from the above; no scalar |
| Dead seats, incidents, L0 | `W/a2w1-results.json`; `git -C /home/vgpnk/Projects/shokunin status --porcelain`; `.ufo/l0-questions.md` |
| Tool installs | `grep -rnE 'uv tool install\|npx -y\|pacman -S\|cargo install\|npm -g' W/a2w1/` |

## 4. What draft-time receipts already establish (and what they do not)

Established, with the command that shows it:

- **Controls were scored before data.** `W/controls/battery-summary-c1.jsonl` last line
  `{"should_fail_accepted": 0, "control_accepted": 1}`; C1 verdicts K0-K7, K10 `FAIL`, K8/K9 `PASS`.
  `W/controls-a2/battery-summary-c2.jsonl` same summary; C2 `PASS` only K3, K19, K26, the other 27 `FAIL`.
  (Read with `python3` over the jsonl; the truncation in `cat` output does not affect the parse.)
- **The C1 claim already passes at the implementation revision**, twice: `W/a2w1/C1ExecRerun/c1-after-1.jsonl`
  (finished `2026-10-27T03:28:44Z`) and `-2.jsonl` (`03:34:02Z`), both `verdict PASS`, `exit_code 0`, selftest
  154/154, `tool_revision ea6e0ee3`.
- **The C2 claim was red at base**: `W/before/c2-before.jsonl` `rows 0`, `exit_code 1`.
- **The rebinding did not change the rule**: 30/30 controls field-identical between
  `W/controls/battery-summary-c2.jsonl` (frozen `7e373196…`) and `W/controls-a2/battery-summary-c2.jsonl`
  (rebound `a1eb402d…`); the salvage tip fails `verdicts_ok` under both.
- **Base gates**: adjacency FAIL (IN-109), self-assessment FAIL 1 mismatch (K10), census selftest PASS 148/148,
  sources census exit 0 with 40 `W04` and 245 rows (`W/before/`).

Not established at draft time, and therefore not stated as results anywhere above:

- the wave-tip C1 and C2 receipts (the wave was still running when this draft was written; `W/after/` is empty);
- the counted C2 per-row verdicts (the seat reports exist but the results record is not settled);
- any trend verdict — all three are placeholders;
- registry coverage, self-assessment repair, dead seats, misroot sweep, L0 lines, tool-install sweep;
- every `LOG.md` tie (no round-45 LOG entry exists yet).

## 5. Calibration notes for the L1

- The draft deliberately keeps C1's before row attributed to `W/controls/C1-K0.jsonl` (the do-nothing control at
  base `5bbd5ff5`), because `W/before/` holds no C1 base receipt; the do-nothing control *is* the base statement,
  and calling it a "before receipt" without that note would overstate it.
- The two `check-self-assessment` mismatches at the implementation revision (K13, K17: `148 cases` stated vs the
  selftest's 154) and the carried K10 are **facts the round must not hide**. They belong in the SCORECARD outcome
  and in the no-harm bullet, repaired if the round can, otherwise recorded as a defect.
- The registry gap (70/70 rows over 72 tools) is red at the implementation revision. If the round45 registry table
  does not land, the report must say so; a green statement about coverage would be false.
- `Assimilation: none` is a compliant answer under prompt §6 item 10 and needs the reason, which the draft carries
  from `W/a2w1/AsmGate.md`.
- Do not reuse round-43/44 wording for the trend verdicts. Each verdict must name this round's evidence.

## 6. Scope of this seat

Read-only over lane and fleet content; wrote exactly one file, this report
(`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-45/a2w1/ScribeReport.md`). No scratch directory
was created (no clone, counter, mutant or fixture was run, so `/fast/scratch/hyaku/tsukuroi-r45/ScribeReport/` does
not exist and nothing needs removing). No tool was installed or upgraded. No git/jj mutation, no commit, no push.
The L1 owns landing this draft into `.ufo/reports/round-45/tsukuroi.md`.

## 7. Findings

1. **D6 is a real, reproducible gap and the draft closes it structurally.** Round 44's report had no Sources &
   frontier section and no Trend verdicts section (`corpus/lessons/round-44-verifier-spotcheck.md:181-183`); the
   draft above has both, plus the per-claim counting commands and a LOG-tie column that makes an untied change
   visible as a placeholder rather than as a silent omission.
2. **Two D6 sub-defects recur inside this round's own evidence and must be handled, not repeated:** the
   `## SHONEN` heading must be in the report's first commit (round 44 needed `0e363a51`), and the pre-report
   `grep -c '^## SHONEN'` gate (prompt §4 item 4) prints 1 on this draft as written.
3. **State that is red at the implementation revision and that the report must carry honestly:**
   `check-self-assessment` 4 mismatches (K07, K10, K13, K17 — K10 carried from base, K07/K13/K17 new because the
   axes table still says 148 cases and 65 notes while the tree holds 154 cases and 66 entries) and the registry gap
   (2 of 72 tools unregistered). Neither is a claim, both are no-harm/surface-honesty items.
4. **The attempt-1 wave is not evidence.** It has 66 seats, 14 spawned, 0 outputs (`W/w1-results.json`), and the
   rebound counter scores the salvage tip `verdicts_ok 0` under both counter versions
   (`W/controls-a2/salvage-tip-*.jsonl`). Any report line treating it as a wave of this round would be false.
