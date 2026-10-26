VERDICT: draft

# Seat ConnRound44 — item N-11: round-44 planned row (draft)

Lane: tsukuroi-shokunin; round 43, wave w2. Basis: `SCORECARD.md:2648-2668` (round-43 declaration,
freeze fe357001, base 6951ead9, implementation 717b716a, wave-1 integration tip under test 8acf0b02),
`.ufo/waves/round-43/w1/ConnFrontier.md` (w1 draft), `corpus/lessons/round-43.md` (routed open items),
`PROVINCE.md` Frontier, and the live lane files listed below (all read at the working tree of 8acf0b02).
Read-only: no lane file written except this report; no counter, census, audit or host command run; nothing
installed; no subagent; scratch `/fast/scratch/hyaku/tsukuroi-r43/ConnRound44/` created and removed.

## 1. Verified anchors (evidence; all path:line at the tip)

- Ordinals at the round-43 base: depth 8, coverage 9, operability 9, freshness 9, calibration 9,
  adjacency 8; depth and adjacency tied lowest; adjacency stays unclaimed "a recipient action is not
  lane-producible" and must not be harmed; saturation 9 / window 3 (`SCORECARD.md:2654-2657`).
- Frontier: recipient acknowledgement and independently replayed handoffs not verified; author-side
  replay is not promotion evidence (`PROVINCE.md:77-79`); ADJ-06 recipient (kaidoku/revenger) unresolved
  (`PROVINCE.md:51,79-80`); mori declares no intake format for ADJ-04 (`PROVINCE.md:193`).
- Storage-integrity frontier: "Still Frontier: the scrub record … and NVMe SMART/Health — no census arm
  reads them" (`PROVINCE.md:212-214`); promotion condition "becomes Core only after a read-only census arm
  reads it" (`corpus/README.md:243`); round-42 note (`PROVINCE.md:239-244`) and round-43 note
  (`PROVINCE.md:246-254`: present record is mode-0600-root-only [inference], running state unreadable per
  SR6, promotion condition unchanged).
- The census's storage arm emits exactly one line kind `STORAGE btrfs-device-stats …`
  (`tools/tsukuroi-census.sh:1871-1931`, `:1928`, `:3198-3200`; grammar `:352-354`); the round-38/39
  counters require exactly one STORAGE line and six PLANE lines per run
  (`tools/score-storage-arm-r38.py:16-17,27-28,54-56,164-168`;
  `tools/score-storage-hidden-r39.py:31-33,150-153`). A second line starting `STORAGE ` breaks them.
- Mount-table guard: `TSUKUROI_PROC_MOUNTS` (default /proc/self/mounts), `tools/tsukuroi-census.sh:463`,
  used by `probe_storage_arm` at `:1916-1920`; env list `:407-408`.
- Census early readers (`head -n1` over produced streams): `tools/tsukuroi-census.sh:934,:972,:1054,
  :1429,:1504` (the five named by `R43-CENSUS-PROBE-COORDS`); selftest assert streams `:2178,:2188`.
  Foreign-baseline full read at `:746` with the comment "(round 42: an awk `exit` under pipefail killed
  the census on a large baseline)"; existing foreign cases use the 16-row embedded baseline
  (`:481-521`, `:2295-2322`) — no case drives a baseline past the pipe buffer (contrast the round-42
  update-candidates case at `:2559-2563`, ~100 KB, which covers `-Qu/-Sup/-Suu`, not this lookup).
- Round-43 lesson: items 4 (census `:743`/`:746` lookup selftest case) and 6 (single-line probe readers)
  of R42-C1-COUNTER-AMEND remain open — "they stay routed to a census-surface round"
  (`corpus/lessons/round-43.md:102-119`, `:111-115`).
- Round-43 counter gaps recorded in SKILL: C1 limits (`SKILL.md:3997-4000`), C2 binding limits — the
  binding accepts a padded or blank-line-prefixed verdict line and does not read a JSON `verdict` field
  beside `verdict_line` (`SKILL.md:4026-4029`) — and the K7 open channels (`SKILL.md:3994-3995`).
- The frozen r43 C2 counter demands `rows == 3` exactly (`tools/check-scrub-record-r43.py:44-46,90-91,
  323-326`; `SKILL.md:4023-4025`), and the r43 entry holds exactly SR1/SR3/SR6
  (`corpus/knowledge/btrfs-scrub-record-r43.md:17,:51,:97`). Appending rows to that file flips `rows`
  to 6 and breaks the no-harm recheck.
- w1 draft to refine: `.ufo/waves/round-43/w1/ConnFrontier.md:75-133`.

## 2. Synthesis (the one move)

Three claims on three distinct axes, worked from the round-43 frontier state, each with a do-nothing
control that fails under its frozen counter. C1 (coverage) closes the only true Frontier→Core promotion
available — the scrub-record arm over the subset SR6/SR8/SR9 prove readable — and is made honest by the
depth claim; C2 (depth, tied lowest) pins what the wave-1 falsifier proved unpinned (the ioctl success
direction, S242) and the read-surface matrix, and closes the two recorded C2 binding gaps; C3
(operability) discharges the two remaining R42-C1-COUNTER-AMEND bullets (4 and 6) with a red-before
regression case. Adjacency stays unclaimed: this lane cannot produce recipient-side acknowledgement,
acceptance or closure (section 1), so no round-44 adjacency claim has producible evidence.

## 3. Round-44 planned row — exact text

```
## Round 44 — declaration (planned row, draft)

Base: the round-43 measured tip (declared before the after-run). Ordinals at base: depth 8, coverage 9,
operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest; C2 works
depth; adjacency stays unclaimed — recipient-side acknowledgement, acceptance and closure cannot be
produced by this lane (`PROVINCE.md:77-79`), ADJ-06's recipient is unresolved (`PROVINCE.md:51,79-80`),
and mori declares no intake format for ADJ-04 (`PROVINCE.md:193`) — and must not be harmed. Saturation 9
/ window 3 unchanged. This round folds the remaining R42-C1-COUNTER-AMEND items 2, 3 and 6
(`corpus/lessons/round-43.md:102-119`): the C3 counter refuses to run without --scratch, handles SIGINT
by reaping its own children, and its frozen pre-data controls include the data-gated and padding-filter
arms (QUALITY 90 channels) beside the uid/env/name/mount arms; the C2 binding is the anchored
declared-verdict form (QUALITY 90 second clause, R42-VERDICT-FORM) and closes the two binding gaps
recorded at `SKILL.md:4026-4029` (a padded or blank-line-prefixed verdict line, and a contradictory JSON
`verdict` field beside `verdict_line`).

| Claim | Axis | Surface moved | Counter (frozen; sha256 named at freeze) | Before at base (expected) | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | coverage | The scrub-record line of the storage-integrity frontier (`PROVINCE.md:212-214`; `corpus/README.md:243`) moves Frontier → Core for the unprivileged-readable subset: the census gains a new verdict-neutral `SCRUB btrfs-scrub-record state=… filesystems=N records=N unreadable=N timers=N [detail=…]` line, emitted by a new `probe_scrub_record` (beside `probe_storage_arm`, after the DRIFT line), which for each btrfs fsid the round-39 mount-table guard lists (`TSUKUROI_PROC_MOUNTS`) stats `/var/lib/btrfs` (absent → `records=0`, SH4 semantics), stats each `scrub.status.<fsid>` file, reads `devinfo/<devid>/scrub_speed_max`, and reads the `btrfs-scrub@*.timer` unit state; a present record whose content is unreadable (open mode argument 0600 subject to the umask, S237:483, SR1) reads `state=BLOCKED detail=records:unreadable`; the arm never parses record content (SR1 [inference]) and never queries running state (SR6). The line uses the distinct `SCRUB` prefix because the round-38/39 storage counters require exactly one `STORAGE` line per run (`tools/score-storage-arm-r38.py:16-17,27-28`; `tools/score-storage-hidden-r39.py:31-33,150-153`) | `python3 tools/score-scrub-record-arm-r44.py --revision <REV> --scratch <DIR>`: fixtures (absent dir; present-unreadable 0600; present-readable in-namespace fixture; speed-max absent/present; timer absent/present; mount-table unreadable), a live leg, and the census selftest | FAIL: base census prints no `SCRUB btrfs-scrub-record` line (`line_present 0`) | **PASS iff fixtures == N and correct == N and live_agree == 1 and line_present == 1 and selftest_pass == 1** at the measured revision | any census change outside `probe_scrub_record`, its call site, the SCRUB emission block and the arm's selftest cases; or score-storage-arm-r38/r38-q82 or score-storage-hidden-r39 regress at the tip; or the census selftest regresses |
| C2 | depth (sourced: S242/S243 opened this round) | New entry `corpus/knowledge/btrfs-scrub-record-r44.md` rows SR7 (the ioctl success direction: `btrfs_scrub_progress` (Linux v7.2.11 `fs/btrfs/scrub.c:3321-3335`, S242) returns 0 with the device's `scrub_ctx` stat only while a scrub runs on that devid, `-ENOTCONN` when the device is idle, `-ENODEV` for an unknown devid; the status ioctl returns that value (S240 ioctl.c:3126-3133) — closing the SR6 wave-1 falsifier F2; F1/F3 scoping notes appended), SR8 (read-surface permission matrix: `/var/lib/btrfs` created by `mkdir_p(…, 0777)` (S237:1335,1160), record files opened mode argument 0600 (S237:483) and named `scrub.status.<fsid>`/`_tmp` (S237:446-470), `btrfs scrub status` distinguishes absent (exit 0, "no stats available", S241 capture.txt:8-10) from present-unreadable), SR9 (the promotion boundary: directory/stat/speed-max/timer reads are unprivileged; record content and running state are not; the arm reports `state=BLOCKED detail=records:unreadable` and omits `running`). Rows go in a NEW entry — not the r43 file, whose frozen counter requires `rows == 3` exactly (`tools/check-scrub-record-r43.py:44-46,90-91,323-326`; the r43 entry holds exactly SR1/SR3/SR6) — plus an append-only header pointer in the r43 entry naming the r44 entry (mirrors r42→r43; `pointer_ok`) | `python3 tools/check-scrub-record-r44.py --revision <REV>`: same conjunct shape as r43, plus the anchored binding checks (reject padded/blank-line-prefixed verdict lines; reject a JSON `verdict` field disagreeing with `verdict_line`) | FAIL: base `rows 0` (entry absent) | **PASS iff rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1 and binding_ok == 1** at the measured revision | any bound `fails`; a `partly` without a bound residual reading `holds`; an unbound counted seat; a quote outside its frozen source window; or check-scrub-record-r43.py regresses at the tip |
| C3 | operability | `tools/tsukuroi-census.sh`: (a) add a selftest case driving `TSUKUROI_FOREIGN_BASELINE` past the pipe buffer (~64 KiB, ≥2000 rows) asserting the packages plane still computes with the `:746` full-read form, so restoring the round-42 `awk … exit` form fails the case (exit 141); (b) convert the five single-line probe readers (`printf '%s\n' "$CAP_OUT" | head -n1 | …` at :934, :972, :1054, :1429, :1504) and the two selftest assert streams (:2178, :2188) to here-strings so no probe-buffer early reader remains | `python3 tools/score-census-readers-r44.py --revision <REV> --scratch <DIR>`: lexical conjunct (no early-reader regex hit in production probe paths), selftest PASS including the new case, the `awk … exit` revert mutant killed, neutral rewrites PASS; refuses to run without `--scratch`; SIGINT handler reaps its own children; pre-data controls include the data-gated and padding-filter arms | FAIL: base hits the early-reader lexical conjunct and lacks the large-baseline case (a revert mutant passes the base selftest) | **PASS iff lexical_clean == 1 and selftest_pass == 1 and case_large_baseline == 1 and revert_killed == 1 and neutrals_pass == 1 and should_fail_accepted == 0** at the measured revision | any census function body changes outside `probe_packages`' baseline read, the named reader call sites, and the selftest; or an early-reader pattern reappears in a production probe path; or score-storage-arm-r38/q82, score-storage-hidden-r39, score-size-invariance-r42, score-bootinputs-r43 regress at the tip; or the census selftest regresses |

Controls, scored with the frozen counters before any seat: C1 — K0 do-nothing base census (no SCRUB
line; must FAIL), K1 constant emitter, K2 count-only reader (stats without EACCES discrimination), K3
presence-denial (ignores BLOCKED detail), K4 fixture-gated arm, K5 cached-live arm, K6 present-0600
fixture must read BLOCKED (only the candidate PASSes). C2 — K0 do-nothing base (rows 0; must FAIL), K1
scripted writer, K2 line references shifted, K3 dropped source, K4 S242 absent, K5 mention-not-assertion
report, K6 padded verdict line, K7 contradictory JSON `verdict` field (each must FAIL under the anchored
binding; only the candidate PASSes). C3 — K0 do-nothing base plus the `awk … exit` revert variant (must
FAIL) and K1 the early-reader pattern (must FAIL); K2 data-gated fix, K3 padding-filter fix (must FAIL);
only the candidate PASSes. Battery lines: `should_fail_accepted 0, control_accepted 1` for each counter.

Causal separability: C1 touches the census (new probe + call site + SCRUB emission) and the promotion
paragraphs in PROVINCE/README; C2 touches corpus/knowledge (new r44 entry), `corpus/SOURCES.md` (new
S242/S243) and the r43 entry header pointer; C3 touches census `probe_packages` (baseline read), the
five reader call sites, and the selftest. C1 and C3 share the census file but touch disjoint functions
and are scored by independent counters; neither counter reads the other's surface. No-harm: all six axes
re-checked at the tip, including `score-storage-arm-r38.py`/`-q82`, `score-storage-hidden-r39.py`,
`score-size-invariance-r42.py`, `score-bootinputs-r43.py`, `check-scrub-record-r43.py` and the census
selftest still PASS.

Risks / second-order effects. (a) C1's live leg on this host is `records=0` (no `/var/lib/btrfs`,
S241 capture.txt:7-10), so the BLOCKED branch is carried by the fixture matrix, not the live leg
(mirrors the round-43 C1 namespace-evidence pattern). (b) The `SCRUB` line prefix is required: the
round-38/39 storage counters assert exactly one `STORAGE` line per run (section 1). (c) SR7 must not
restate SR6's overreach: it is scoped to `cmd_scrub_status`/the ioctl success direction, with F1/F3
notes appended. (d) C3 is the only claim with pre-existing code; its novelty is the regression guard —
the counter's do-nothing control is the missing case, and the revert mutant proves the case bites. (e)
The SIGINT-reaping behavior of the round-43 counter remains unverified; C3's counter must both handle
SIGINT and reap its children (reported under `--scratch` hygiene, not as a scored claim).
```

## 4. Corrections to the w1 draft (`.ufo/waves/round-43/w1/ConnFrontier.md:75-133`)

1. **C1 line prefix.** The w1 draft named a second `STORAGE btrfs-scrub-record` line. The round-38/39
   storage counters count exactly one `STORAGE`-prefixed line per run
   (`tools/score-storage-arm-r38.py:16-17,27-28,164-168`;
   `tools/score-storage-hidden-r39.py:31-33,150-153`), so that form breaks the no-harm recheck. A
   distinct `SCRUB btrfs-scrub-record` prefix (same verdict-neutral convention as DRIFT) avoids touching
   the six-plane/STORAGE invariants.
2. **C2 target entry.** The w1 draft appended SR7-SR9 to `btrfs-scrub-record-r43.md`. The frozen r43
   counter requires `rows == 3` exactly (`tools/check-scrub-record-r43.py:44-46,90-91,323-326`), so
   appending flips `rows` to 6 and breaks `check-scrub-record-r43.py`. New rows go in a new
   `btrfs-scrub-record-r44.md` entry, with an append-only header pointer from the r43 entry (precedent:
   r42→r43, `pointer_ok`).
3. **C2 counter closes the recorded binding gaps.** The w1 draft used the round-43 binding form
   verbatim; the planned r44 counter additionally rejects padded/blank-line-prefixed verdict lines and a
   contradictory JSON `verdict` field (`SKILL.md:4026-4029`).
4. **C3 scoping.** The w1 draft folded the data-gated/padding-filter arms and SIGINT-reaping into the
   counter battery; this draft keeps them (routed items 2 and 3) and records SIGINT-reaping as a
   hygiene report, not a scored conjunct.

## 5. What I did not do

- I did not run any counter, census, selftest or audit (planning seat; read-only queries only), and did
  not fetch S242/S243 (byte-identity verification is round-44 freeze/L1 work).
- I did not freeze counter bytes or score K-batteries (L1 work); the sha256 values above are named at
  freeze, not measured.
- I did not read sibling lane files; only lane-internal files.
- No tools installed or upgraded; no host mutation; scratch dir created and removed; no lane file written
  other than this report.
