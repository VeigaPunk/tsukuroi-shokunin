# Round 45 — lesson (tsukuroi, hyaku run 9)

author: tsukuroi L1 (`TsukuroiR45a2`), 2026-10-27. Base `5bbd5ff588120fd8e7c744695351a6978b4241c1` (the lane tip at
round start), freeze `ea6e0ee38d8066663bb0871b53bade14441eb304` (declaration, frozen counters, pre-data controls,
frozen sources S246-S249), implementation `18389f44cf6ce414d7be205998b29c79fb0b490c`. Claims, controls and the
attempt-2 rebinding: `SCORECARD.md` "Round 45 — declaration" and "Round 45 — attempt-2 rebinding". One v2 wave,
`a2w1` (66 seats), and a residual call `a2r1` (5 reviewer/critic seats, not counted); attempt 1's `w1` died unfilled at the orchestrator session exit (14/66 spawned, 0 outputs, salvage
commit `5b3029bf`), so attempt 1 scored nothing. Seats are the lane, not outside reviewers (LEARNING.md); the
non-author closure is pending.

## Outcome (author-side; non-author closure pending)

Measured revision `44560592857660a20c6a2b296fa14fa7a90464b5` (integration of `a2w1` and `a2r1`); receipts `.ufo/waves/round-45/after/c1-final-44560592.jsonl`
and `c2-final-44560592.jsonl` (both via `tools/run-receipt.py`).

- **C1 operability — PASS.** `lexical_hits 0`, `sites_found 5`, `equiv_ok 5`, `selftest_pass 1`, `selftest_r45 6`,
  `revert_killed 6`, `adjacency_ok 1`; `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)`; census sha256
  `237b21c9…b5fcdc`, byte-identical to the implementation `18389f44`. Before: control K0 on the base bytes FAILs every
  leg (`lexical_hits 5`, `equiv_ok 0`, `selftest_r45 0`, `revert_killed 0`, `adjacency_ok 0`; `controls/C1-K0.jsonl`).
  Kill rules not fired: PLANE/HANDOFF lines and exit unchanged base vs implementation apart from memory counters that
  recur within one revision (`a2w1/C1ExecPlaneDiff.md`); predecessor counters PASS→PASS, `score-storage-arm-r38.py`
  FAIL at both (`a2w1/C1ExecPriorStorage.md`, `C1ExecPriorRecent.md`); no file written in live mode
  (`a2w1/C1ExecLiveRead.md`). The census bytes did not change after `18389f44`, so those receipts hold at `44560592`.
- **C2 depth — FAIL.** `rows 3`, `quotes_ok 3`, `props_ok 3`, `host_ok 3`, `sources_ok 1`, `novelty_base_hits 0`,
  `pointer_ok 1`, **`verdicts_ok 0`** (before: `rows 0`, `before/c2-before-a2.jsonl`). No counted verdict bound
  (R45-C2-BINDING-CHANNEL below); GR1-GR3 stay pending. The seats' report first lines read GR1 `holds` (critic only;
  the reviewer died), GR2 `partly`/`partly`, GR3 `holds`/`holds`; GR2 was narrowed twice at integration and read by
  the uncounted residual `a2r1/ResRevGR2` (`holds`) and `ResCritGR2` (one finding, applied). C2 kill rules: no bound
  `fails`; novelty 0; `check-scrub-record-r43.py` PASS at base and at `44560592`; S246-S248 re-fetched byte-identical
  (`a2w1/C2ExecLiveSources.md`).

## Gate

### New SOURCES rows (opened 2026-10-27 by wave a2w1; each quote located with `grep -n` in a live fetch whose bytes equal the frozen snapshot; drafted by seat SrcGateNew, checked by the L1)

| Row | URL (access 2026-10-27) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S246 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/lib/cmdline.c?h=v7.2.11 (raw `plain/…?h=v7.2.11` for `lib/cmdline.c`, `lib/vsprintf.c`, `lib/kstrtox.c`; live bytes = `frozen/src/SHA256SUMS`) | "potentially suffixed with K, M, G, T, P, E."; "unsigned long long ret = simple_strtoull(ptr, &endptr, 0);"; "*base = 16;" / "*base = 8;" / "*base = 10;"; "ret = ULLONG_MAX;" | cmdline.c:147,156,192; kstrtox.c:31,33,35 |
| S247 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/dev-replace.c?h=v7.2.11 (raw `plain/…?h=v7.2.11`) | "the disk copy procedure reuses the scrub code"; "ret = btrfs_scrub_dev(fs_info, src_device->devid, 0," … "&dev_replace->scrub_progress, false, true);" | dev-replace.c:700,701,703; the continue path repeats it at :1265-1268 |
| S248 | https://github.com/systemd/systemd/blob/v262/man/systemd.kill.xml (raw `raw.githubusercontent.com/systemd/systemd/v262/man/systemd.kill.xml`) | "If set to control-group, all remaining processes in the control group of this unit will be killed on unit stop"; "the delay configured via the TimeoutStopSec= has passed"; "the termination request is repeated with the SIGKILL signal"; "right after sending the signal specified in this setting, systemd will always send SIGCONT"; "Defaults to control-group." | systemd.kill.xml:68-69, 91-92, 96, 114-115, 101 (tags elided, whitespace collapsed) |
| S249 | own-work capture `.ufo/waves/round-45/frozen/hostcap/` (`capture.sh`, run 2026-10-27T02:09:52Z, uid 1000) | "unit_show FinalKillSignal=9 … KillMode=control-group KillSignal=2 SendSIGKILL=yes TimeoutStopUSec=5s"; "stop_default …:2:DefaultTimeoutStopSec=5s"; "devinfo … devids=1" | capture.txt:3,4,9 (also :5 `dropin_owner … none`, :8 `scrub_speed_max … value=0`) |

Snapshot digests: `.ufo/waves/round-45/frozen/src/SHA256SUMS` (cmdline.c `1af5ad98…ca9d`, vsprintf.c `cabb648a…69ca`,
kstrtox.c `0c52ae02…1ee4`, dev-replace.c `f07ef0a0…4f3a`, systemd.kill.xml `44832283…0e72`), fetch log `FETCH.txt`
(2026-10-27T02:07:23Z); capture.txt `f5958a83…1e70`, capture.sh `c6d2c448…51fc`, captured 2026-10-27T02:09:52Z.
Live re-fetches by seat SrcGateNew at 2026-10-27T03:30:32Z were byte-identical to all five `src` digests.

### Re-opened rows and rows touched old→new (opened 2026-10-27 by wave-`a2w1` seat SrcGateReopen; column 11 only)

| Row | used-by old → new | Log |
|---|---|---|
| S237 | `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md` → `corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` | `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 5bbd5ff588120fd8e7c744695351a6978b4241c1 18389f44cf6ce414d7be205998b29c79fb0b490c -- corpus/SOURCES.md`; column 11 only; re-fetched 2026-10-27 byte-identical (`48df2e2f…0801`) |
| S242 | `corpus/knowledge/btrfs-scrub-record-r44.md` → `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` | same; column 11 only; re-fetched 2026-10-27 byte-identical (`f347931b…a5b8`) |
| S243 | `corpus/knowledge/btrfs-scrub-record-r44.md` → `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` | same; column 11 only; re-fetched 2026-10-27 byte-identical (`ce146120…1c43`) |
| S244 | `corpus/knowledge/btrfs-scrub-record-r44.md` → `corpus/knowledge/btrfs-scrub-record-r44.md, corpus/knowledge/btrfs-scrub-grounding-r45.md` | same; column 11 only; re-fetched 2026-10-27 byte-identical, three files (`9a0b6cc2…f8ad`, `eaa7af92…0252`, `3b803e8b…ce98`) |

Snapshot digests re-checked live 2026-10-27 against `.ufo/waves/round-42/frozen/src/SHA256SUMS` (S237) and
`.ufo/waves/round-44/frozen/src/SHA256SUMS` (S242-S244): `sha256sum` 6/6 match and `cmp` live-vs-frozen 6/6
identical. Tag pins re-resolved the same day: `refs/tags/v7.1^{}` `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`,
`refs/tags/v7.2.11^{}` `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`, `refs/tags/7.1-1^{}`
`0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0` — unchanged from `FETCH.txt`. Receipts:
`.ufo/waves/round-45/a2w1/SrcGateReopen/` (`sha256-live.txt`, `tags.txt`, `col-diff.json`, `commands.txt`).

Census (frozen command): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` exit 0,
`ok`, 40 W04, 249 rows (`grep -c '^| S[0-9]' corpus/SOURCES.md`) against 245 rows and the same 40 W04 at base
`.ufo/waves/round-45/before/sources-census-start.txt`; the warning sets are `diff`-empty.

### Reject rows (routed defect R44C-GATE-REJECT-ROW/D8: rejects recorded here, not only under spot-check candidates)

| Entry (staged id) | Rejected | Reason (source-checked) | Flip |
|---|---|---|---|
| `btrfs-ioctl-surface-r27.md` (staged S223; file sha256 `385097cb31823eff48384e33c0ca732b69d360eb11463c70f171a1c0f5101a1c`) | yes — P2/P3, carried from rounds 42-44; re-read this round | Its :14 "Together they close the btrfs ioctl surface" and :31-32 "a caller can be identified from its ioctl number alone" rest on a nine-row table (:20-28) while the lane-pinned v7.2.11 `ioctl.c` (sha256 `7b3488f2…ba01`) carries `grep -c "case BTRFS_IOC_"` = 64 dispatch labels, three of them the scrub trio at :5578-5583 that this round's C2 rows reason about; its source is tag v7.2 (not the lane's v7.2.11) and it carries no `## QUALITY check` (0 of 70 staged entries do) | none at this tag for the closed-surface sentence (false while the dispatch has 64 labels); an admissible re-use would need a table of all 64 labels at v7.2.11, a QUALITY block, and renumbering to S250+ (staged S200-S249 now collide, 50 ids) |
| `ext4-journal-guarantee-r32.md` (staged S269/S270) | yes — carried from rounds 43-44; first quote re-checked against live text this round | Its first quote is a splice: it prints "For performance reasons, ext4 by default only writes filesystem metadata" / "file data blocks are /not/ guaranteed to be in any consistent state after a crash", dropping "through the journal. This means that" from the live sentence (journal.html sha256 `2e6693a2…5649`, fetched 2026-10-27, identical to round 44's fetch); out of province — `findmnt -rno TARGET,FSTYPE` lists btrfs, vfat and xfs, no ext4, and `grep -ci ext4 PROVINCE.md` = 0; its btrfs "repairs corruption … from a replica" row is unscoped for this host's single-profile data mount; no `## QUALITY check` | an ext4 filesystem enters this host's province, plus a re-quote of the whole sentence at landing and a QUALITY block |
| `snapper-eacces-mechanism.md` (staged S230; `SOURCES.append.md:37`) | yes — intake refused by this wave's AsmGate (`.ufo/waves/round-45/a2w1/AsmGate.md`, "Reject at least") | The absent-defect register marks the row quarantined with "the gate block named no locator, so no quote was checked" (`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:367`); the staged row's source cell is the lane's own `corpus/knowledge/snapper-eacces-mechanism.md`, an own-work file with no external URL to re-open (`SOURCES.append.md:37`) | a landed Gate row that names a locator for the own-work claims (file line + quote), or an independent external source registered for the `errno:13` EACCES mechanism; the register's quarantine line then clears |

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R45-LESSON-ADJ-IN109-DRIFT | gate discipline — a moved line with no repin | IN-109's `found_line` and the census line of its quote disagree after a census insertion unless repinned; seven commits across six rounds, measured per commit: 2216 (r19-20) → 2277 (`4ac5ebaa`, r32) → 2346 (`e2f97e6e`, r35) → 2411 (`52ffd65f`, r38) → 2425 (`02eeed07`) → 2447 (`49cc53c7`, r39) → 2452 (`a2d7aad7`, r39) → 2465 (`44766208`, r42) → 2468 (`78abb8b5`) → 2579/2580/2582 (`ab8aae16`, `071ab0d1`, `9608ebc3`, r44) with the anchor still at 2468 through `8eee79db`, `fbfef071`, `e9ca7ef6` and the base `5bbd5ff5`. `git log --oneline -- corpus/knowledge/adjacency-anchors-r19.json` shows a repin in every round but 44 | none for the class until round 45; round 44's seat CritNoHarmFinal captured the instance (`w2/CritNoHarmFinal/adjacency-tip.txt`, `status FAIL` at `8eee79db`) and the round routed it (closure D1) instead of landing it | D1 repin 2468 → 2582 at `ea6e0ee3`, plus C1's adjacency kill rule (`tools/score-census-readers-r45.py:313-328`: `check-adjacency-anchors.py --revision REV`, `adjacency_ok = rc == 0 and status == PASS`). Able to fail: control C1-K7 (one comment line inserted above the IN-109 case) scores `adjacency_ok 0`, `status FAIL`, `findings ["INBOUND-CLASSIFICATION-WRONG"]`, `exit 1` (`controls/C1-K7.jsonl`); the same leg prints `PASS`, `findings []` at `18389f44` |
| R45-REPORT-MINIMUM-SECTIONS | delivery — report conformance | The round-44 report has no `## Sources & frontier` and no `## Trend verdicts`: `grep -c '^## Sources & frontier' /home/vgpnk/Projects/shokunin/.ufo/reports/round-44/tsukuroi.md` → 0, `grep -c '^## Trend verdicts' …` → 0; its headings are Outcome, Work performed, No-harm and checks, Incidents, Tooling, SHONEN, Next | none until the round-44 closure (D6) | The report is assembled from the wave's report-seat drafts; the template names both sections as required minimum content (`templates/round-prompt.md:111,116`). Able to fail — weakly: the only check is a heading grep, because the marker rule exempts exactly these two sections (`:122-125`) and the watchdog "does not check trend verdicts" (`:127-128`); no gate goes red for this class |
| R45-C2-GR2-HOST-READING | depth-overreach — a true citation plus a false inference | `corpus/knowledge/btrfs-scrub-grounding-r45.md:88-89` says "the caller has no effective capabilities (capture.txt:1): no replace or scrub state is observable to this caller". As uid 1000, `devinfo/1/replace_target` (mode 444, value `0`) and `exclusive_operation` (mode 444, value `none`) read successfully. Three wave seats flag the sentence: `a2w1/C2ExecHostRecheck.md` §1/§3, `a2w1/C2CritGR2.md` (with `sysfs.c:1288,2007-2029`), `a2w1/C2RevEntryWhole.md` finding 2 (the universal "any device" refusal is also unsupported by the quoted lines) | wave a2w1 seats C2ExecHostRecheck, C2CritGR2, C2RevEntryWhole; the freeze did not catch it | Applied at `0503400b`: the Host reading names the readable sysfs attributes (S243 sysfs.c:1288, :2015) and the Statement gains the earlier `-ENODEV`/`-EROFS`/`-EIO` checks and the suspended state; read by the uncounted residual `a2r1/ResRevGR2`. Able to fail: the attribute reads contradict the frozen sentence verbatim (`a2w1/ScribeLesson/host-replace-attrs.txt`); the counter's `host_ok` leg cannot, because it binds only "existing, non-empty capture.txt lines" (`tools/check-scrub-grounding-r45.py:27`) — a recorded limit, not a passing check |
| R45-ASMGATE-IDCENSUS | evidence — a receipt that does not back its number | `a2w1/AsmGate.md` reports "183 registry ids, 147 staged ids, 30 intersections"; the same revision holds 249 registry rows/ids (S001-S249) and a true intersection of 50 (S200-S249). The kept `a2w1/AsmGate/id-collisions.txt` lists 5 ids that are not lane registry ids (S250, S251, S252, S262, S268) and omits 25 genuine collisions; the report's `reg-ids`/`staged-ids` files are absent from `a2w1/AsmGate/` | none in-wave; recomputed by the round-45 lesson seat | Recount with the lane extractor and keep both id lists beside the collision set. Able to fail: a recount against the kept receipt flags the five non-registry ids and the 25 missing ones; the L1 recount with the prompt's 0-3-space extractor gives 249 / 147 / 50 (`.ufo/waves/round-45/assimilation/reg-ids`, `staged-ids`, `collisions`) |
| R45-D7-CITATION-HALF-CLOSED | repair closed at the file, not at the reference | `ea6e0ee3` commits the round-44 evidence (`raw.json.gz`, `strace-rev-live1.log.gz`, three tarballs, four `.ready` files), but `w1/C1ExecLiveRead/commands.txt:26,81` and `w2/SkillReview.md:55` still cite `strace-rev-live1.log`; `git cat-file -e 18389f44:<that path>` is `rc=128`, the `.log.gz` is `rc=0` | none; `a2w1/ScoutR44Defects.md` marks D7 "done" after testing the `.gz` path only | Point the three citations at the committed `.gz` (or commit the log uncompressed). Able to fail: `git cat-file -e <REV>:<cited path>` returns 128 for the cited path and 0 for the committed one |
| R45-C2-BINDING-CHANNEL | binding — counted verdicts written in shapes the frozen binding refuses, plus a lost record | Wave `a2w1`'s six counted C2 seats bound 0 rows: `C2RevGR1` died without a report or a yield (transcript ends on `429 Rate limit` then a provider prompt-flag error); `C2CritGR1`/`GR2`/`GR3` yielded JSON objects with a `verdict` key and no `verdict_line`; `C2RevGR2` yielded text opening "Report written and scratch removed. Final answer:"; `C2RevGR3` yielded "Receipts in place, scratch removed. Yielding the counted verdict."; and the orchestrator lost all 41 first outputs at a kernel restart (`a2w1-results.json` `output` null). Scored as recorded and with the six yields recovered verbatim from the transcripts, `verdicts_ok` is 0 both ways (`a2w1/L1-recovery/c2-asis-results-scratch.json`, `c2-recovered-outputs-scratch.json`). Round 44 lost SR7 the same way (a JSON-string output) | partly — QUALITY 81/89/90 fix the bindable shape, and every counted prompt said "Yield plain text, not a JSON object"; no pre-data control scored the shapes seats actually yield, and nothing checked a counted yield before the wave settled | QUALITY 93 (this round). Shown able to fail: the frozen counter refuses each of the five recovered shapes (`c2-recovered-outputs-scratch.json`, all rows `rev`/`crit` null); the remedy — a binding channel the seat writes verbatim (its report's first line, already identical in five of six reports) or a declared transcript-recovery rule — is routed to the next C2-style counter and is not counted here |
| R45-A2-COUNTER-WAVE-NAME | binding — a frozen counter bound to a dispatch name the dispatcher can retire | The C2 counter at the freeze `ea6e0ee3` named its counted wave `w1`/`r1`; attempt 1's `w1` died unfilled (14/66 spawned, 0 outputs) and the dispatcher never re-takes a spent `.ready`, so the frozen counter was reachable only through a post-freeze edit (`057c1804`: the two literals → `a2w1`/`a2r1`, before any seat scored) | none | The rebinding changed two literals only, the 30-control battery re-ran field-identical (`controls-a2/battery-summary-c2.jsonl`) and the declaration records it ("Round 45 — attempt-2 rebinding"). Able to fail: forged all-`holds` records under the old name `w1`, which PASS the frozen counter (attempt-1 control K3), score FAIL `verdicts_ok 0` under the rebound one (`controls-a2/w1-names-under-rebound-battery-summary.jsonl`: K3/K19/K26 FAIL) |

## Round-44 routed defects — round-45 disposition (at the measured revision)

| Defect | State | Evidence |
|---|---|---|
| D1 IN-109 repin + adjacency receipt | closed | `found_line` 2582 = census line 2582 (`ea6e0ee3`); `check-adjacency-anchors.py` PASS at `18389f44` (`a2w1/ScribeLesson/adjacency-18389f44.json`) and inside the C1 counter's adjacency leg at the measured revision (`after/`) |
| D2 SKILL SR8 sweep | closed | `SKILL.md` "Correction — the round-44 scrub rows" block (appended `0503400b`): the SR8 suffix set, the stale "unpinned" replace tag, the stop outcome and the Limits fragments, each pointed at GR1-GR3 (sweep `a2w1/C2ExecSweep.md`) |
| D3 C2 unadmitted mark | closed | round-44 entry `## Round-45 grounding and gate status`; round-45 rows marked pending in the entry ("Gate status — round 45"), `SKILL.md` and `corpus/README.md` (`194a4523`) |
| D4 planned row stale | closed | `SCORECARD.md` "Round 45 — measured outcome" carries a new `planned (next round)` row |
| D5 self-assessment tip receipt | closed | `after/self-assessment-final.jsonl` at the measured revision |
| D6 report sections | closed for round 45 | the round-45 report carries `## Sources & frontier` and `## Trend verdicts` (`grep -c` 1 each) |
| D7 untracked r44 evidence | partial | evidence committed at `ea6e0ee3`; three round-44 citations still name the uncompressed `strace-rev-live1.log` (R45-D7-CITATION-HALF-CLOSED, routed) |
| D8 rejects in Gate | closed | the reject table above |
| D9 AsmGate locator / staged-id hazard | closed in this lesson | staged entries sit under `merge/tsukuroi/knowledge/corpus/knowledge/`; 50 staged ids collide with the lane registry (S200-S249), so any landing renumbers by document (`.ufo/waves/round-45/assimilation/collisions`) |
| D10 LOG freshness line | closed | `LOG.md` round-45 entry, "Re-verification of predecessor pins" |

Conflicts recorded verbatim for the canonical judge:

- `a2w1/ScoutR44Defects.md` marks D7 "done" ("the cited strace log and raw capture therefore resolve from that
  commit") after testing `<path>.log.gz`; the paths the two round-44 files cite are the uncompressed ones, which fail
  `git cat-file -e` (`rc=128`).
- `a2w1/ScoutR44Defects.md` marks D3 "done" on the entry alone; `corpus/README.md:434` and the `SKILL.md` row that D3
  also names are unchanged from base.
- `a2w1/AsmGate.md` reports 183 registry ids and 30 intersections; the same revision's `corpus/SOURCES.md` has 249 ids
  and the true intersection is 50.

## Assimilation and considerthese

Assimilation: none. Package `merge/tsukuroi/` read-only, no campaign tool run. Id check with the prompt's
0-3-space extractor: lane registry 249 ids, staged 147, collisions 50 (S200-S249) — `.ufo/waves/round-45/assimilation/`
(`reg-ids`, `staged-ids`, `collisions`); the guard is proved on a scratch registry with an indented `  | S002 |` row,
which the extractor reports as a collision (`assimilation/guard-proof.txt` = `S002`). Quarantine slice (register data
rows for `tsukuroi`): 12 rows (`assimilation/quarantine-slice`: S211 and S213 payload-absent; S225 unreachable;
S230, S231, S242-S244, S249-S252 no locator) — none hand-checked this round, so none is appendable and nothing was
appended. No staged theme fits the round's surfaces (`a2w1/AsmGate.md` "Theme fit"; its id counts are wrong,
R45-ASMGATE-IDCENSUS). Rejected from the set: staged S223 and S269/S270 (carried, re-checked) and S230 (table above).

### considerthese — seat-harm incident log (`considerthese/2026-10-26.md`, proposal "Seat-harm incident log")

Mined: "Seat-to-seat damage on the shared host (pkill, `/tmp` misroot, the round-37 fleet-root misroot) is now a
recurring class separate from seat loss. A running tally per round would show whether isolation fixes are actually
landing." Ten incidents over rounds 37-44, each row bound to the lane bytes carrying it: the checker refuses a row
whose `cite` is absolute or `{/tmp,/fast/scratch}`-rooted, whose quote is not on its line verbatim, whose `lesson`
id is absent from that line, whose `minted` id already occurs in `corpus/lessons/`, or whose `closed-able-to-fail`
state lacks a red-shape and a green-shape cite in one receipt. Receipts: `.ufo/waves/round-45/a2w1/ConsiderMine/`
(`seat-harm.jsonl`, `seat-harm-log.py`, `run-mutants.py`, 15 single-field mutants, `killed=15/15 survived=none`).
A round-44 wave had built an eight-row version of this ledger as a wave file
(`.ufo/waves/round-44/w1/ConsiderMine.md`); it was never adopted (`grep -ric seat-harm SKILL.md` → 0,
`grep -ril seat-harm corpus/lessons/` → 0), so this section re-derives the rows instead of citing it, and adds the
two process leaks the draft left out of scope.

| Round | Incidents | Ids |
|---|---|---|
| 37 | 1 | `R37-MISROOT-NOTE-DRAFT` |
| 38 | 0 | — |
| 39 | 1 | `R39-SEAT-PKILL` |
| 40 | 1 | `R40-TMP-MISROOT` |
| 41 | 2 | `R41-TMP-MISROOT-REPEAT`, `R41-CAPTURE-FIFO` |
| 42 | 1 | `R42-C1-SCRATCH-FALLBACK-TMP` |
| 43 | 1 | `R43-L1-SCRATCH-STRAY` |
| 44 | 3 | `R44-L1-FLEET-ROOT-FIXTURE`, `R44-PYCACHE-RECUR`, `R44-COUNTER-FIFO-LEAK` |

| Class (n) | Landed as | Today | Deciding evidence |
|---|---|---|---|
| `fleet-root-write` (2) | repair ×2 | detector-only | `git status` at the fleet root is red while the tree exists and clean after quarantine (`round-37.md:102`, `round-44.md:44`); no rule stopped either write |
| `process-signal` (1) | none | rule-only | the sentence is in 8 of 11 wave-spec generators of rounds 37-45 and 0 in the round-39 one (`make-a2w1-spec.py:39`; `guard-presence-all.txt`); no receipt shows it firing |
| `scratch-tmp` (3) | routed ×2, closed ×1 | closed ×2 / open ×1 | old 1153 vs new 2 absolute `/tmp` mkdir calls (`round-41/w1/RoutedSelfAssessScratch.md:54`, `:56`); the round-42 counter still takes `--scratch` optionally and falls back (`tools/score-size-invariance-r42.py:296`, `:300`) |
| `process-leak` (2) | line-scoped guard ×1 | open | `round-41.md:74` guards one injected line; the class recurred as the counter's un-reaped process group (`round-44-verifier-spotcheck.md:210`) |
| `shared-scratch-stray` (1) | repair | open | round-44 root clean, round-45 root carries `base-census-r45.sh` + `impl-census-r45.sh` at top level (`round-root-strays.txt`) |
| `lane-pollution` (1) | none (removal only) | open | 6 `tools/__pycache__/*.pyc`, 3 born during round 45, invisible to `git status` (`.gitignore:2`) (`pycache-churn.txt`) |

Reading: the classes that stopped recurring are the ones whose fix is a tool argument or a per-seat path; the prose
rules did not stop theirs, and a removal did not stop `lane-pollution`. `R44-L1-FLEET-ROOT-FIXTURE` repeated
`R37-MISROOT-NOTE-DRAFT` seven rounds later while its own wave context already read "never create files at the fleet root … is
a misroot" (spec 21:04:47, misroot 21:08:59) — and the case that fired (`dev0 "$PWD/fx/…"` with cwd at the fleet root) is the one the sentence's
redirect example does not name. `R42-C1-SCRATCH-FALLBACK-TMP` was marked closed while its own counter still fell
back, which is the failure mode a tally must catch: a fix credited at a site it never touched. Rule: a seat-harm
fix counts as landed only when the incident's own site refuses the old shape and a receipt shows red before green;
prose is `rule-only`, a removal is not a fix, and the sweep must read ignored paths and the shared round root, not
only `git status`. Open: no gate reads this ledger — `git grep -l seat-harm -- tools SKILL.md corpus` exits 1 with no hits
(`ledger-gates.txt`) — so it is a checklist until one does.

## Spot-check candidates for the non-author closure

Admits: the new registry rows S246 (Linux v7.2.11 `lib/cmdline.c`, quote at cmdline.c:147/156/192) and S248 (systemd
v262 `man/systemd.kill.xml`, quote at :114-115), each re-fetched byte-identical to `frozen/src/SHA256SUMS`
(`a2w1/SrcGateNew.md`, `a2w1/C2ExecLiveSources.md`); C1's five conversions (`a2w1/C1ExecPlaneDiff.md`,
`a2w1/C1ExecFullLarge.md`). Rejects: the staged `btrfs-ioctl-surface-r27.md` (S223; a nine-row ioctl table stated as
closure against 64 dispatch labels at the lane's pinned tag) and staged S230 (no re-openable locator). Not an admit:
GR1-GR3 (depth gate FAILED, pending).
