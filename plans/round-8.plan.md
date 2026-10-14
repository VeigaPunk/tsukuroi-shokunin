# WWKD plan — tsukuroi round 8 (ufo-round-plan-v1)

Draft lane: PREP-S8 (2026-10-14, drafted during the round-7 wave). Design-time
state read by this lane, not taken from a record: HEAD `dc3436d` (round-6
commit, 2026-10-14 15:17:26 -03) with `git status --short` **empty at this
draft's freeze 18:22:28Z** — round 7 had landed nothing at the freeze, and the
round-6 artifact set (register, provenance receipt, verifier note, OOM note)
is committed and re-hashed here. Post-freeze shape observation (18:24:24–
18:27Z; **shape only, no content relied on**): `tools/tsukuroi-census.sh`
appeared modified and **still moving** in the worktree (1136 lines at 18:24:24Z
→ 1186 `wc -l`, md5 `821acc24…` at 18:24:45Z), `plans/round-7-record-draft.md`
appeared (405 `wc -l` → 426 by the next read, still growing), and
`corpus/knowledge/update-safety-v2.md` appeared untracked — **the name as
landed**, where the round-7 plan proposed `update-safety-plane.md`; the round-7
arm, note and scribe lanes are landing. **No pin is taken from the moving
revision**, and no gate run was made against it. Round 7's plan (md5 `bb915954…`,
160 `wc -l`)
is cited as a **plan**, never as landed state; every round-7 statement below is
a draft-time reading that Step 0 resolves.

Axis move: operability — the OOM/kill-event plane (round 6's note, 433 ln; its
kernel arm a bare class count inside the drivers plane) becomes **executable as
a watch**: **the OOM plane joins the census** as its next plane line, and its
content is **new-vs-baseline, fail-closed**. One move, one surface: the round-6
note's measured detection contract C1–C6 (`corpus/knowledge/oom-event-plane.md:355-375`)
becomes a runnable arm, and the two measured kill waves (`:21-52`) become its
declared rows. Freshness is served by the watch itself: every run re-measures
the retained window instead of quoting round 6's capture.

## Candidate decision (why this one)

Post-round-6 candidates were: (A) the OOM-plane watch in the census; (B) the
round-7 landing debt; (C) the coredump-storm watch; (D) unifying the baseline
mechanism.

- (B) is not a round-8 candidate: it is Step 0's job, finished first as named
  debt against round-7's own contract — round 7 does the same for round 6
  (`plans/round-7.plan.md:96-101`), and the debt it inherited is measured, not
  suspected (round 6's baseline turn "specified, not landed", `SKILL.md:760-771`).
- (C) is deferred, not rejected: the coredump storm (census `coredump=270` at
  the 18:22Z live run) is app-level — godot/node/LOVE owners, the round-6 note's
  own boundary (`oom-event-plane.md:43-52`); a census arm could count it, but the
  class needs an app-level vocabulary and a second baseline before it can mean
  anything. Anchors recorded below for a future slot.
- (D) is folded into (A), not a separate move: the watch reuses the baseline
  mechanics round 7 lands for the foreign set — one mechanism, two readers; a
  second mechanism would be a defect.
- (A) is the move: it is the last landed note with no executable presence in the
  gate (rounds 2/3/5 made the other measured families runnable; round 7 the
  update-safety plane), the round-7 plan defers exactly it with anchors
  (`plans/round-7.plan.md:140-147`), and the live host still carries both waves
  and no new one (measured below) — the baseline can be seeded from state this
  draft points at, not from memory.

## Claim

(a) **The OOM/kill-event watch joins `tools/tsukuroi-census.sh`** (round-7's
    realized plane count + 1; expected 5→6, worst-plane rollup unchanged, plane
    key proposal `oom`, adjudicated at landing). Probe families, all read-only,
    all already exercised:
    - **kernel arm (C1)** — a **retained-window** scan, not just boot 0:
      `journalctl -k -g '<CLASS_OOM>' -o short-precise` (server-side `-g`;
      measured available and cheap on systemd 261: 0.19 s over all 13 boots).
      Boot-separator lines (`-- Boot <id> --`) are counted **out**, not as
      messages — observed in the window scan, and a counting trap to handle
      explicitly.
    - **attribution arm (C2)** — `journalctl -g 'kernel OOM killer killed some
      processes'`; waves are message **clusters** (A = 2 messages within 1 ms at
      2026-10-13 23:44:30; B = 1 at 2026-10-14 13:10:59.400591).
    - **kill9/teardown arm (C3)** — `status=9/KILL` / `Failed with result
      '(signal|oom-kill)'`, clustered by time; lines outside any cluster print as
      `stray=` and are never absorbed into a wave (the contract states whether
      `stray` moves the verdict; proposal: no, report-only — adjudicated).
    - **presence flags (C4)** — `memory.events[.local]` at `user.slice` /
      `user-1000.slice` (+ the current `user@1000.service`): printed as "an
      `oom_kill` has been accounted", **never as a count** (counter lifecycle
      `oom-event-plane.md:245-257`).
    - **pressure anchors (C5)** — `memory.swap.peak` vs `SwapTotal` (34.22 G /
      34.25 G = 99.9 % at draft), `memory.swap.events fail` (5 922 849),
      `pswpin/pswpout`, `sock_throttled` — rows, verdict-neutral.
    - **guards row** — `systemd-oomd` inactive+disabled, `earlyoom` absent,
      `MemoryHigh/Max` = max/infinity — a measured state row, verdict-neutral
      (operator-owned levers, `:337-353`).
    The plane's note line carries `window=` + waves-known-vs-new + the anchors;
    the realized string is quoted from an executed run at landing, never this
    proposal. New overrides for the hermetic selftest: `TSUKUROI_CGROUP_DIR`,
    `TSUKUROI_MEMINFO_FILE`, `TSUKUROI_OOM_BASELINE`, with dispatcher support.
(b) **New-vs-baseline, fail-closed.** `corpus/knowledge/oom-event-baseline.tsv`
    (name adjudicated at landing), one row per declared wave: cluster id, class,
    first/last seen (absolute timestamps **and** boot id — boot index is not
    identity), evidence pointer (note §), note. Env override in the `TSUKUROI_*`
    family (proposal `TSUKUROI_OOM_BASELINE`, default = the committed file;
    embedded-snapshot vs external-file per the **realized** round-7 mechanism —
    Step 0 reads which landed, never guesses). Rules, each with a selftest
    fixture:
    - observed cluster matching a row → `known`; a cluster **not** in the
      baseline → `new` → DEGRADED, cluster printed (time/class/units);
    - a declared wave absent **inside** the retained window → `missing` →
      DEGRADED (unexplained loss of declared evidence, never silently dropped);
      absent **outside** the window → `out_of_window=N` row, verdict unchanged
      (retention loss is a coverage fact, not a health fact);
    - baseline absent/unreadable → DEGRADED, never HEALTHY off a missing
      baseline (carried from rounds 6/7);
    - journal (`--list-boots` or the scans) unreadable → BLOCKED; an empty scan
      is only a pass if the window itself is measured (rc=0, ≥1 boot);
    - arm words and gate mapping **recorded, not silently applied** (proposal
      CLEAN → HEALTHY; NEW / DECLARED-MISSING / NO-BASELINE → DEGRADED;
      BLOCKED → BLOCKED; composition BLOCKED > {NEW, DECLARED-MISSING,
      NO-BASELINE} > CLEAN), adjudicated against the realized round-7 mapping
      mechanism.
    The **both-readings rule** is printed and never adjudicated: PID1's
    13:10:59 slice notice is a *late report* of the 23:44:30 kill under
    `boot-plane.md:228-229` and a session-SIGKILL attribution under
    `oom-event-plane.md:215-224` (H1–H3). The arm carries both rows verbatim;
    no round resolves H1–H3 (read-only unmeasurable).
(c) **The contract lands where the executor reads it**: the `SKILL.md` round-8
    append (arm semantics, the recorded mapping, the counter rule, the
    both-readings rule, count restatements moved together — the standing rule at
    `SKILL.md:829-832`), the baseline file with evidence pointers, an append-only
    errata pointer in `oom-event-plane.md` ("implemented at <pin>; the realized
    contract supersedes §8 where it differs"), plus `corpus/README.md` row,
    SCORECARD move row (before: OOM plane note-only, `oom=` bare inside drivers
    → after: `PLANE oom` watch, baseline known-vs-new) and the LOG entry
    (scribe). The drivers plane's `oom=` class count **stays** (double-count
    precedent, round 3 — distinct value = attribution + kill9 + presence + swap
    rows, all invisible to the kernel arm by construction).

Step 0 (mechanical, before any edit): round-7 landing check against its own
measure — census revision landed (md5/line count/**selftest count from an
executed run**, round-7's `PASS (35+N, N≥4)`), the round-6 foreign baseline debt
landed in it (`foreign=` known-vs-new + ≥3 fixtures), v2 note — proposal
`update-safety-plane.md`; the untracked `update-safety-v2.md` seen at 18:27Z is
the landed name, so resolve it from the record, never the plan — present +
round-2 note errata pointer, README/SKILL/SCORECARD/LOG rows, the round-7
record (draft seen at 18:24Z as `plans/round-7-record-draft.md`; **the landed
name governs**). An unlanded part
is named debt finished first against the round-7 plan's contract, not
re-designed. Then re-measure every pin below; a mismatch is recorded, not
smoothed.

Anti-claim: the watch runs no mutating verb (journal/cgroup/proc read-only); no
external site; no AUR RPC; upstream state out of scope by construction; cgroup
counters are presence flags, never event counts; a new wave can never be
laundered — the baseline is operator-appended, append-only, and the arm never
auto-extends it; a missing baseline is DEGRADED, never HEALTHY; an unreadable
window is BLOCKED, never HEALTHY; the two event-B readings are carried, never
resolved; heap-OOM/coredump classes (V8 backtraces, the storm) stay with the
journal/coredump owners (`oom-event-plane.md:43-52`); root probes stay BLOCKED
(`dmesg_restrict=1`) and are not escalated; no round-6/7 artifact is re-measured
from memory — every citation is re-hashed at dispatch.

Measure: `--selftest` rc=0 with `PASS (N7+M cases, M≥4)` — the four new cases
being known-clean rollup, new-wave→DEGRADED, declared-missing-in-window→
DEGRADED, window-unreadable→BLOCKED (a fifth, baseline-absent→DEGRADED, if the
harness shape allows); live run prints the new plane line with a verbatim note
and the rollup line gains the plane key; zero mutation (fixture byte-unchanged +
`git status` byte-identical before/after); baseline file landed with md5/line
count pinned; SKILL/README/SCORECARD/LOG landed; ≥2 baseline rows spot-checked
by a **non-author** against live probes (re-executing the row's probe).
Suggested seats: arm seat (census + fixtures + baseline), note seat (SKILL +
errata pointer), non-author verifier, scribe (README/SCORECARD/LOG/commit).

Draft-time pins (this lane, 2026-10-14 18:22:28–18:24:46Z, read-only, non-root,
scratch `/tmp/w7-preps8-tsukuroi/`; re-run, never quote). Line counts are
`wc -l`; three artifacts carry an **unterminated final line** (census ends
`main "$@"`, SKILL.md and round-7.plan.md end `.`), so Read counts one more — a
pin must state its convention. HEAD `dc3436d`, tree clean at 18:22:28Z; census
(HEAD revision) md5 `e9327046b05b5c71e07fe511ad7e82dd`, 1032 `wc -l`, selftest
rc=0 `PASS (35 cases, 35 passed, 0 failed)`, live rc=1
`TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED
journal=DEGRADED)`, drivers `kerr=139 (oom=1 io=70 gpu=0 other=68)`, journal
`boots=13 err=433 (coredump=270 kernel=139 other=24)`, zero mutation
(`git status` 0 lines before/after). Extension shapes to find on the landed
revision: `CLASS_OOM` `:163`, `class_counts` `:236-245`, `probe_drivers`
`:396-507` (noise-floor tag `:499`), `probe_journal` `:509-625`, selftest
`:627-975` (dispatcher `:635-694`, `check()` `:744`, `ok()`/`bad()` `:693-694`,
PASS print `:971`), `PLANE` emitters `:1011-1014`, rollup `:1022`, exit map
`:1025-1030`, overrides `:145-161`, usage `:174-187`. OOM anchors (18:22:44Z):
boot 0 still `d7f0bc8d938e4249b4a1f250cbfacf58`; attribution = 3 (A:
23:44:30.574948 scope + .576028 `user@1000.service`; B: 13:10:59.400591
`user-1000.slice`); kernel OOM family over the window = 3 lines, all 23:44:30
(.570564 invoked oom-killer / .638184 oom-kill:constraint / .638238 Out of
memory); kill9 class = 3 lines; `-p err` json = 139, CLASS_OOM replay = 1; 95
`memory.events` files, nonzero `oom_kill` = 2 (slice + user-1000.slice = 1 each,
`.local` = 0), current `user@1000.service` `oom_kill` = 0 `sock_throttled` =
3320; slice `memory.peak` 30 699 745 280 B, `memory.swap.peak` 36 744 949 760 B
vs `SwapTotal` 35 917 176 kB = 99.9 %; `swap.events fail` 5 922 849; guards
`systemd-oomd` inactive+disabled, `earlyoom` absent, `oom_dump_tasks=1`,
`panic_on_oom=0`, `dmesg_restrict=1`; **no OOM-family entry since 14:46Z**;
bounds: journal 327 451 lines, window scan 0.19 s. Artifact pins: SKILL.md
`7b5dcf08…` 837, `oom-event-plane.md` `7e99d712…` 433 (third reproduction of
its re-cut pin), `aur-risk-plane.md` `1a584300…` 341, `foreign-provenance-r6.md`
`1b8f47a2…` 307, `round-7.plan.md` `bb915954…` 160.

Deferred candidate C (coredump-storm watch) anchors for a future draft: live
census `coredump=270` (18:22Z; 269 in the round-6 capture, 224 in round 3 —
storm drift, every value a capture); coredump dir 4.1 G (round 3);
`systemd-coredump` is a named journal entry class already; ownership godot/
node/LOVE app owners + journal workstream; needs an app-level vocabulary before
a baseline can exist.

Bounds & unknowns: round-7 landing state at dispatch [unknown — Step 0];
whether the census revision keeps which plane count and which baseline
mechanics it realizes [unknown — read the landed revision, never this draft];
whether retention still holds events A/B at dispatch (journal rotation)
[unknown — the `missing/out_of_window` rows are built for it]; H1–H3 and the
notice-lag reading of event B [unknown, read-only-unmeasurable — carried]; the
counter-lifecycle model Q2 [unknown — the presence-flag rule is the response];
event-B victim list beyond `oom-event-plane.md:326-335` [unknown, structural];
carried: V8 heap-OOM boundary, coredump storm ownership, `1password-beta`
provenance, `walker-restart.hook` (kagi/operator), root `-Qkk` delta, dkms
stale row, `snapper` empty.

Discipline (round 8): host read-only (`PROVINCE.md:16-17`); no external sites;
secrets shape-only; one move; append-only errata; observation / inference /
unknown separated; write scope = the named artifacts only (this draft wrote
only this file).