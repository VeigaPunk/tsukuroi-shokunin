# WWKD plan — tsukuroi round 7 (ufo-round-plan-v1)

Draft lane: PREP-S7 (2026-10-14, drafted during the round-6 wave). Design-time
state read by this lane, not taken from a record: round 6 was in flight and
**nothing round-6 had landed** at this draft's freeze 17:40Z
(`plans/round-6-record-draft.md:19-22` — register absent, no baseline file,
census still the round-5 pin md5 `e9327046b05b5c71e07fe511ad7e82dd`, 1032 ln).
Post-freeze observation (17:44Z; shape, plus the receipt's head — no content is
relied on here): the first two
round-6 artifacts appeared untracked under the names they landed with —
`corpus/knowledge/aur-risk-plane.md` (S6-1 register; the round-6 plan's
draft name was `foreign-aur-risk-plane.md`) and
`corpus/knowledge/foreign-provenance-r6.md` (S6-2 receipt, 19 634 B) — while
the census and the baseline were still absent. Names as landed, not as
planned: another reason Step 0 resolves every path from the round-6 record.
Round 6's plan (md5 `81a9be07fecfbf2af7540ea958143d3a`, 38 ln) is therefore
cited as a **plan**, never as landed state; every pin below is a draft-time
capture — re-measure at dispatch, then run Step 0.

Axis move: operability — the fifth plane becomes executable: **update-safety
joins the census**, and the post-AUR fold is its content (the round-6
register's risk classes become its decision rows). One move, one surface: the
round-2 note's measured decision model (`corpus/knowledge/update-safety-note.md:19-72`,
`SKILL.md:358-400`) becomes a runnable arm, and the round-6 classes
(offline-exile / aur-local / unknown-provenance / out-of-reach —
`plans/round-6-record-draft.md:302-304`) gain their update-path truth: what
`-Syu` can reach, and what it can never reach.

## Candidate decision (why this one)

Post-AUR candidates were: (A) the AUR watch arm in the census; (B) the
OOM-plane watch; (C) update-safety v2 with the risk classes.

- (A) is **round 6's delivery**, not round 7's: register + the machine-readable
  baseline the census reads + ≥3 fail-closed fixtures (`plans/round-6.plan.md:7-25`;
  baseline contract proposal `plans/round-6-record-draft.md:252-293`). Round 7
  *verifies* it at Step 0 and finishes any unlanded part first as named debt —
  re-planning it here would double-book the round. Note also: the watch is
  **local-state-only** — no AUR RPC, no external site, in this or any round;
  the upstream AUR delta stays [unknown] by construction.
- (B) is deferred, not rejected: its anchors are recorded below for the next
  slot. It has no dependency on the register, so nothing is lost by ordering
  (C) first while the register is fresh; and the OOM root cause is
  cross-domain (owning workstreams) — the plane could only ever report state.
- (C) is the move: it is the *point* of round 6 (a register without a decision
  table is inert), it closes the last of the five owned surfaces with no
  executable presence (gate = packages/systemd/drivers/journal; update-safety
  = note only), and the model it needs is already measured — the round
  converts it, it does not invent it.

## Claim

(a) **The update-safety plane joins `tools/tsukuroi-census.sh`** (4→5 planes,
    worst-plane rollup unchanged). The plane's arm word (PASS · INERT ·
    REQUIRES-PREP · BLOCKED · UNKNOWN-UPSTREAM · DO-NOT; composition BLOCKED >
    UNKNOWN-UPSTREAM > REQUIRES-PREP > INERT > PASS — `SKILL.md:358-368`) is
    carried in the plane note line, and the gate-verdict mapping is
    **recorded, not silently applied** (proposal: INERT/PASS→HEALTHY,
    REQUIRES-PREP/UNKNOWN-UPSTREAM→DEGRADED, BLOCKED→BLOCKED; DO-NOT stays
    verb-level note content). Probes, all already-exercised read-only verbs:
    - candidates three ways — `pacman -Qu` (rc/emptiness) + `pacman -Sup
      --print-format '%n %v'` (count; the one allowed plan verb,
      `SKILL.md:408-413`); unreadable → BLOCKED, never a pass; candidates>0 →
      REQUIRES-PREP with count and names printed;
    - channel provenance — db births (`stat -c %w` on `$PACMAN_DB/sync/*.db`;
      the birth-vs-mtime trap stays a printed rule), `offline.db`
      presence/inertness, and the last refresh/upgrade commands from
      `/var/log/pacman.log` (bounded tail read; birth is authoritative, the
      log adds the command class; a log-window miss → `command=unknown` row,
      verdict unaffected);
    - risk-class fold — read the round-6 baseline (env override in the
      `TSUKUROI_*` family, default = the committed file; path resolved from
      the round-6 record, never guessed) + the register's classes; the plane
      line names exposure only: `classes=offline-exile:<n>,aur-local:<m>` (+
      `unknown-provenance` names if the packages arm reports `new`, +
      `unavailable` if the baseline is absent/unreadable → DEGRADED, never
      HEALTHY off a missing baseline);
    - pins/holds stay in the packages plane (no double-probe); this plane
      *references* their reading.
(b) **The v2 decision note lands** (`corpus/knowledge/update-safety-plane.md`;
    name adjudicated at landing; the round-2 note keeps its pins and gains a
    one-line errata pointer — append-only). Content: the class × update-path
    truth table using the register's operator-action vocabulary
    (accept-and-recheck · freeze/pin decision · replace-from-channel · remove ·
    route-out — `plans/round-6-record-draft.md:305-307`): offline-exile →
    `-Syu` reach = none (`pacman -Si` rc≠0), path = replace/remove/accept-frozen,
    recheck = the register's rows; aur-local → `-Syu` reach none, path
    out-of-band (yay, external, not the gate's), review-on-update discipline;
    unknown-provenance → the probe order from the register (pacman.log `-U`
    grep → yay cache dir → `pacman -Qi` validation → offline.db listing), never
    a guessed class; plus the re-measured round-2 pins, refreshed U1-U8 status,
    and the hazard rows (rollback net = `snapper list-configs` empty, dkms
    stale registration, cache size — full `du` stays in the checklist, never in
    the gate's latency budget).

Step 0 (mechanical, before any edit): round-6 landing check against its own
measure — register present, provenance/freshness receipt present, baseline
path/md5/line count pinned, census delta landed (`foreign=` known-vs-new + ≥3
fixtures), selftest count read from the executed run; an unlanded part is named
debt finished first (against the round-6 plan's contract, not re-designed).
Then re-measure every pin below; a mismatch is recorded, not smoothed.

Anti-claim: the gate never runs `-Sy`/`-Syu`/install/remove/restart (the only
mutation-free plan verb, re-stated); no external site, no yay transaction verb,
no AUR RPC — upstream delta is UNKNOWN-UPSTREAM by construction, never a false
pass; unreadable probes fail closed (BLOCKED); empty candidates never read as
"up to date" on an unmeasured channel; the fold cannot launder a DEGRADED
verdict to HEALTHY (carried from round 6); no class is claimed without the
register's measured trail; hazard rows are reported to operator/owning lanes,
never remediated; superseded pins stay visible (append-only errata); nothing
here re-measures round-6 artifacts from memory.

Measure: `--selftest` rc=0 with `PASS (35+N cases, N≥4)` — the four new cases
being inert-clean 5-plane rollup, candidates>0→REQUIRES-PREP, `-Qu`
unreadable→BLOCKED, baseline absent→DEGRADED-never-HEALTHY; live run prints the
5-plane rollup line with a verbatim `PLANE update-safety:` note; zero mutation
(fixture byte-unchanged + `git status` byte-identical before/after); note v2
lands with its `corpus/README.md` row + SKILL round-7 append + SCORECARD move
row (before: 4-plane gate, update-safety note-only → after: 5-plane gate) +
LOG entry; ≥3 note rows spot-checked by a non-author against live probes.
Suggested seats: arm seat (gate+fixtures), note seat (v2 + errata pointer),
non-author verifier, scribe (README/SKILL/SCORECARD/LOG/commit).

Draft-time pins (this lane, 2026-10-14T17:40:05Z, read-only, non-root, scratch
`/tmp/w6-preps7-tsukuroi/`; all reproduce the round-2 note's pins, re-measured
three days on): `pacman -Qu` rc=1 / 0 lines; `pacman -Sup --print-format` 0
lines rc=0; births core/extra/multilib/omarchy 2026-10-11 12:54:13.542054496,
offline.db 2026-10-03 17:41:33.994891750; IgnorePkg/IgnoreGroup empty rc=0;
`HoldPkg = pacman glibc`; `pacman -Qm` = 16 (13 elephant-* + omarchy-walker +
android-apktool-bin 3.0.3-1 + obsidian-cli-inspector 1.0.3-1);
`/var/log/pacman.log` readable (157 286 B, mtime 2026-10-13 16:37): last `-Sy`
12:54:13-0300 (`:1405`, second-exact with the births), last full `-Syu`
2026-10-11 16:13:19-0300 (`:1414`), the two `-U` yay-cache installs 2026-10-13
13:52:59 (`:2090`) / 16:21:20 (`:2097`); `yay --version` 13.0.1 (no
transaction verb run); `~/.cache/yay/` = 2 dirs; memcg `oom_kill 1`,
`memory.peak` 30 699 745 280 B, `memory.swap.peak` 36 744 949 760 B; boot 0
`d7f0bc8d938e4249b4a1f250cbfacf58` (still current). Live counts drift — re-run,
never quote.

Deferred candidate B (OOM-plane watch) anchors for the next draft: kernel ring
(`journalctl -k`; `dmesg_restrict=1`) `GpuWatchdog invoked oom-killer …
oom_score_adj=200` + `Out of memory: Killed process 1732581 (python3) …
anon-rss:27873696kB` at 2026-10-13 23:44:30; the notice-lag rule (P5 slice
notice 13:10:59 ≠ a kill — count from the kernel log / cgroup counter,
`corpus/knowledge/boot-plane.md:118-144,228-229`); today a new kill would only
move `oom=` inside the drivers plane's accepted [unknown] noise floor — the
watch's job would be new-vs-baseline, fail-closed.

Bounds & unknowns: round-6 landing state at dispatch [unknown — Step 0]; the
landed baseline path/format/env name [unknown — resolve from the record, never
guess]; upstream Arch/AUR delta [unknown, read-only-unmeasurable — carried];
whether `pacman.log` retains the last refresh event at dispatch (rotation)
[unknown — the arm's `command=` row is built to read `unknown`]; the plane
mapping adjudication (proposed above; the record states the realized one);
carried: `1password-beta` provenance (operator), `walker-restart.hook`
(kagi/operator), root `-Qkk` delta, dkms stale row, `snapper` empty.

Discipline (round 7): host read-only (`PROVINCE.md:16-17` — never
install/upgrade/remove/restart); no external sites; secrets shape-only; one
move; append-only errata; observation / inference / unknown separated; write
scope = the named artifacts only (this draft wrote only this file).