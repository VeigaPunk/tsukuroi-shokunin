VERDICT: draft

# ConnFrontier — Item X-3: frontier and round 43 (draft)

Assessment basis: round-42 declaration (`SCORECARD.md:2560-2595`, base `c8efaa3f`, freeze `a84fc9de`), implementation
commits `447662088d` (C1) and `f50c28d8` (C2), lane tip `f50c28d8` at dispatch. Round 42 is mid-wave (no measured-outcome
section exists yet). "Advances" below means *the declared claims move a Frontier line*; admission is a separate,
non-author-closure step I did not run.

---

## 1. Round 42's declared claims, in frontier terms

- **C1 (operability)**: the census's early-reader pipelines on probe buffers (`printf … | grep -q`, `| grep -m1`,
  `| head`) under `set -euo pipefail` are replaced by here-strings / `awk 'NR <= 3'`/`'NR == 1'` at :692/:694 and
  :1621/:1635/:1641/:1652, plus two new selftest cases (`SCORECARD.md:2573`; R41-CENSUS-PIPEFAIL-692). This is an
  **instrument repair inside Core census planes** (`probe_packages`/`probe_update_safety`/`run_selftest`); no surface
  changes, no Frontier line is touched.
- **C2 (depth, sourced)**: `corpus/knowledge/btrfs-scrub-record-r42.md` rows SC1–SC5 on the btrfs scrub status record
  (S237 `cmds/scrub.c`, S238 `CHANGES`, S239 own-work host capture — `SCORECARD.md:2574`). The entry's own scope line
  says it "states upstream behaviour of btrfs-progs v7.1" and stays on the storage-integrity **Frontier**; its Limits
  section states the promotion condition is unmet: "No census arm reads the record; this entry stays on Frontier ground
  (`PROVINCE.md` promotion condition for the scrub record unchanged)" (`btrfs-scrub-record-r42.md:149-150`).

## 2. Which frontier lines round 42 advances

**One line, in depth only: F4's scrub-record knowledge.** C2 moves the scrub-record line of the storage-integrity
frontier from "unstated record mechanics" to a documented, counter-frozen statement (SC1 file name + `_tmp`-then-rename +
`flock LOCK_EX|LOCK_NB`; SC2 line format; SC3 who writes it / recording disabled / running state from the kernel ioctl;
SC4 how status folds device lines; SC5 per-device `scrub_speed_max`). It changes OS triage semantics: a missing record
reads `UNRECORDED`, not `NEVER SCRUBBED` (SC3; `btrfs-scrub-record-r42.md:136-137`). The **promotion condition is not
met**: no census arm reads the record, so the line stays Frontier (`PROVINCE.md:212-214` "Still Frontier … no census arm
reads them"; round-26 rule `PROVINCE.md:169-174`, corrected condition `PROVINCE.md:176`). NVMe SMART (SH5/SH6) and the
second NVMe device stay unread. C1 advances no frontier line.

Partial, indirect effect: SC5's host cell (`capture.txt:9`, `scrub_speed_max` 0) is the first *unprivileged* read of a
scrub-record-adjacent signal, and SC1 pins why the record file itself is not unprivileged-readable (open `0600` on
create, `scrub.c:483`). This is exactly the permission fact the round-41 planner said a round-43 arm would need
(round-41 `w1/ConnFrontier.md:110-112`).

## 3. Which frontier lines stay open

| Line | Status after round 42 | Evidence |
|---|---|---|
| F1 Recipient acknowledgement / independent replay of handoffs unverified; author-side replay not promotion evidence | open | `PROVINCE.md:77-78`; `corpus/README.md:30-32` |
| F2 Kaidoku/revenger shipped-artifact RE ownership contested; integrator arbitrates | open | `PROVINCE.md:79-80`; `corpus/README.md:33-34`; R20-OUT009 `PROVINCE.md:148-152` |
| F3 Boot: btrfs-overlayfs snapshot-boot path on a mkinitcpio 42.2 image untested; `/new_root` symlink watch | open | `corpus/README.md:38-39,151-153`; round-24 notice `corpus/README.md:223-231` |
| F4 Storage integrity, scrub-record line: documented (SC1–SC5) but still Frontier — no census arm reads it | open (knowledge advanced; Core promotion unmet) | `PROVINCE.md:212-214`; `btrfs-scrub-record-r42.md:149-150` |
| F4 Storage integrity, NVMe SMART line (SH5/SH6): no census arm; reads need privilege | open | `PROVINCE.md:212-214`; round-26 wave-2 correction `PROVINCE.md:176` |
| F4 second NVMe device (xfs on `/tmp`/`/fast`) unread | open | `PROVINCE.md:214` |
| F5 Storage: census honesty indistinguishable on this host (live answer constant); no host-side injection authorized | open | `PROVINCE.md:234-236`; round-39 limit closure `PROVINCE.md:225-237` |
| OV4/OV5 conflicts with mori (OOMRules= qualifier; earlyoom option) | recorded, unresolved — need mori action | `PROVINCE.md:187-189` |
| ADJ-04 census handoff line (`state=prepared`; round 32) | no state transition possible: mori declares no intake format | `PROVINCE.md:193` |

## 4. Why the round-43 lowest-axis claim should be depth, not adjacency

Depth and adjacency are tied lowest at 8 (`SCORECARD.md:2567`). Every avenue that would move adjacency 8→9 still
requires an actor outside this lane or outside the province: a recipient-side acknowledgement/replay (F1), integrator
arbitration (F2), mori intake-format or conflict resolution (ADJ-04; OV4/OV5). The round-40/41 reasoning stands — "a
sibling acknowledgement cannot be produced by this lane" (`SCORECARD.md:2295-2296,2458-2459`). A self-producible
adjacency claim (re-checking sibling pins, counting handoff lines) has been measured before and is freshness/quality
work, not a new adjacency move; a do-nothing control would reach the same counter. So the planned row works **depth** as
the lowest axis and leaves adjacency declared-unchanged (no harm). Branch for the L1: if round-42's measured outcome
moves depth to 9, the round-43 declaration re-derives ordinals (adjacency becomes sole lowest, still lane-internally
unreachable); the depth claim below remains the strongest self-producible move.

The item's hinted scrub-record census arm resolves on the **coverage** axis, not depth: the one precedent for a Frontier→Core
promotion via a verdict-neutral census arm is round 38's C1, declared **coverage** (`SCORECARD.md:2117` "C1 | coverage |
Storage integrity (btrfs per-device error counters) moves Frontier → Core … verdict-neutral census arm"). Coverage is 9 at
base, so the promotion claim does not discharge the lowest-axis duty; a depth claim on the same frontier line does.

## 5. Best round-43 planned row (draft text)

Two claims on distinct axes; both target the same open Frontier line (F4, scrub record); both fail at base
(do-nothing-proof); C1 mirrors the R38 promotion template (including the R38-Q82 production-path namespace conjunct) but
is honestly bounded to what an unprivileged census can read.

```
## Round 43 — declaration (planned row, draft)

Base: the round-42 measured tip (declared before the after-run). Ordinals at base: depth 8, coverage 9,
operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest; saturation 9 /
window 3 unchanged. No adjacency claim is attempted (a sibling acknowledgement cannot be produced by this lane;
adjacency stays unclaimed and is not harmed). C1 works coverage on the storage-integrity frontier's scrub-record
line (promotion condition `PROVINCE.md:169-174,176` met by a new verdict-neutral census arm, R38 precedent
`SCORECARD.md:2117`); C2 works depth (the lowest axis) on the same line.

| Claim | Axis | Surface moved | Counter (frozen; sha256) | Before at base | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | coverage | The scrub record (`btrfs scrub status`, `/var/lib/btrfs/scrub.status.*`, `btrfs-scrub@.timer`; SH3/SH4) moves Frontier → Core for the unprivileged-readable subset: the census gains a second verdict-neutral `STORAGE btrfs-scrub-record state=… files=N records=N unreadable=N speed_limits=N [detail=…]` line (`probe_scrub_record_arm`), which for each btrfs fsid the mount table lists (`/proc/self/mounts`, override `TSUKUROI_PROC_MOUNTS`) reads the record directory `/var/lib/btrfs` (absent → `records=0`, SC3 semantics: never "never scrubbed"), stats each `scrub.status.<fsid>` file, and reads `scrub_speed_max` per devinfo; a present record whose content is unreadable (SC1 mode 0600 root) reads `state=BLOCKED detail=records:unreadable`, a readable one is parsed with SC2's fields. Never in the rollup, no `PLANE`, no exit-code change, never enters `TSUKUROI_CENSUS`. PROVINCE.md gains "Round-43 promotion — R43-SCRUB-RECORD-CORE"; SKILL.md gains "Storage integrity arm — round 43"; corpus/README.md gains a round-43 Frontier notice. NVMe SMART stays Frontier (privilege-needed) | `python3 tools/score-scrub-record-arm-r43.py --revision <REV> --scratch <DIR>` (frozen; sha256 TBD): fixture legs use a fixture record-dir override; the live leg compares the census line to the counter's own direct reading; production-path legs run inside `unshare -rm` with a tmpfs mounted at the real `/var/lib/btrfs` and fixture records written in the frozen SC2 format (no `TSUKUROI_*` override) | `fixtures_matched 0/N, live_match 0, ns_views_matched 0/3, six_planes_all 1`, FAIL exit 1 | `fixtures_matched == FIXTURES_EXPECTED and live_match == 1 and ns_views_matched == VIEWS and six_planes_all == 1`, exit 0 | Any of: a fixture mismatches; the live line differs from the counter's own reading; any run prints other than six PLANE lines; a 0600 record scored HEALTHY or as absent; a census diff hunk outside probe_scrub_record_arm / run_selftest / the three doc surfaces; score-storage-arm-r38.py or score-storage-hidden-r39.py stops passing |
| C2 | depth (sourced) | `corpus/knowledge/btrfs-scrub-record-r42.md` gains append-only rows SC6–SC8: SC6 the kernel-side running-state API — `BTRFS_IOC_SCRUB_PROGRESS` (`linux/btrfs.h` lines 155-198, 1194-1195) and that it is an ioctl on an fd of the filesystem, so an unprivileged census cannot read running state (grounds SC3's "running state from the kernel ioctl"); SC7 the shipped `btrfs-scrub@.service`/`.timer` units (`ExecStart=/usr/bin/btrfs scrub start -B %f`, `ConditionPathIsMountPoint=%f`, `Nice=19`, `IOSchedulingClass=idle`, `KillSignal=SIGINT` ↔ S237 scrub.c:437-444 handler; monthly persistent timer) — what a scheduled scrub runs and how a stop writes the record; SC8 the host cell (timer disabled, no record dir) restated against SC3/SC7. Sources S240 (kernel uapi header snapshot) and S241 (unit files, own-work capture), frozen snapshots + capture land first | `python3 tools/check-scrub-record-r43.py --revision <REV>` (frozen; sha256 TBD): per-row quote on its named line of a digest-checked snapshot; lexical shape gates only, declared as such; verdicts bound through the orchestrator's dispatch + results records (QUALITY 89) | entry absent: `rows_matched 0/3, source_ok 0`, FAIL exit 1 | `rows_matched == 3 and source_ok == 1` and bound verdicts all `holds`, exit 0 | any SC6–SC8 row judged false against the pinned source at its cited lines; a snapshot digest mismatch |

Controls, scored with the frozen counters before any seat (run_controls_r43.py): C1 — do-nothing base, constant
emitter, count-only reader (dir presence without EACCES discrimination), presence-denial (ignores BLOCKED detail),
fixture-gated fix, cached-live, and a 0600-record control (must read BLOCKED): each must FAIL, only the candidate
PASSes. C2 — do-nothing base, scripted writer (quotes copied from the row windows), line references shifted, dropped
source: each must FAIL, only the candidate PASSes.

Causal separability: C1 touches the census and the three doc surfaces; C2 touches the knowledge entry and
`corpus/SOURCES.md`; neither counter reads the other's surface; C1 reuses the round-39 mount-table guard without
changing it. No-harm: all six axes re-checked at the tip (including `score-storage-arm-r38.py`,
`score-storage-hidden-r39.py` and `check-scrub-record-r42.py` still PASS). Measured revision: the lane branch tip named
in the round-43 outcome section, declared before the after-run.
```

Notes on the draft:

- **Why this promotion is honest and do-nothing-proof.** The record file is created 0600 root and every open takes
  `flock(LOCK_EX|LOCK_NB)` (`scrub.c:483,487`; SC1), so an unprivileged census **cannot parse record content** on a
  stock host; what it *can* read unprivileged is the directory (existence), file stat, and sysfs `scrub_speed_max`
  (proven by `capture.txt:9`). The claim therefore promotes the *unprivileged-readable subset* and encodes the
  unreadable case as `BLOCKED detail=records:unreadable` — never as HEALTHY and never as "never scrubbed" (SC3). The
  0600-record control makes the discrimination mandatory. This is narrower than the round-26 wave-2 correction's
  wording ("need privilege for SMART and the scrub status ioctl") which covers the *full* reading; the promotion is
  partial by design and says so in the PROVINCE paragraph.
- **C2 is the depth claim on the lowest axis**, on the same F4 line, and directly constrains C1's boundary (SC6 says
  why running state is out of reach; SC7 says what a timer-run scrub does). It is sourced from host-readable artifacts
  (`/usr/include/linux/btrfs.h:155-198,1194-1195`; `/usr/lib/systemd/system/btrfs-scrub@.{service,timer}`), no new
  privilege.
- **Third claims considered, dropped:** a freshness recheck of the F3 `/new_root` symlink watch (`tools/boot-chain-audit.sh`)
  would be procedural, not a move; an NVMe SMART arm needs privilege (`sudo -n` allow-list) which the lane does not use;
  adjacency is not lane-self-producible (§4). Two claims is the lean, no-harm row.

## 6. What I did not do

- I did not run the C1/C2 counters or the census (planning seat; only reads).
- I did not read sibling lane files (only citations inside lane files and the peer roster).
- I did not run `btrfs scrub status` or any scrub/limit command, and made no host mutation; the only writes are this
  report, its receipts, and my scratch (removed).
- Round-42 measured outcome and non-author closure do not exist yet; verdicts here are against the declaration.
- No tools were installed or upgraded (nothing was needed).
