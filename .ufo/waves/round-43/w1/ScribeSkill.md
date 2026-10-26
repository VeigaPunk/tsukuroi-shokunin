VERDICT: draft

# F-4 — two append-only SKILL.md sections (round 43): boot-input freshness, scrub record re-grounded

Seat `ScribeSkill` (L2, round 43 / hyaku 9, wave w1). Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`;
nothing in the lane was edited, added or deleted outside this report and its receipt dir. Read-only seat: no counter
was run, no clone was made, no scrub/ioctl/mount/package action was taken, no tool was installed (tooling
authorization unused). The before/after counter values below are quoted from the committed receipts, not re-observed
by me; the pins I did observe are in `.ufo/waves/round-43/w1/ScribeSkill/pins.txt`.

Where the proposed text would go: appended after the current last line, `SKILL.md:3956` (end of "Round-42 notes — C2
outcome and packaging offsets") — both sections are pure appends. Style copied from "Census early readers under pipefail — round
42" (`SKILL.md:3851-3896`) and "Scrub status record — round 42" (`SKILL.md:3898-3926`): appended-date line, defect id,
base/fix commits, evidence dir, a signal table, the rule, selftest/counter, limits.

## 1. Pins I observed (gates for the draft's citations)

- Counters frozen as declared: `sha256sum tools/score-bootinputs-r43.py tools/check-scrub-record-r43.py` →
  `886f92c8…e10f`, `b4602c56…9854` (`pins.txt:3-5`).
- Working tree equals the implementation commit for every surface the draft cites:
  `git diff --stat 717b716a8943151ace8657e0ca23d7d9b8434f26 -- corpus/knowledge/btrfs-scrub-record-r43.md SKILL.md
  tools/boot-chain-audit.sh` prints nothing (`pins.txt:6-7`). So a reader at the lane tip sees the same bytes.
- Base `tools/boot-chain-audit.sh`: `set -uo pipefail` at `:139`; `boot_inputs_newer` `:463-488` with the find
  pipeline at `:480-487`; call `newer=$(boot_inputs_newer)` at `:749`; gate `[ "$newer" = 0 ]` at `:761`
  (`pins.txt:8-34`). Fix `717b716a…`: `inputs_newer_than` `:463-475` (decision `hit=$(find …)`, `[ -n "$hit" ]` at
  `:469-470`), `boot_inputs_newer` `:477-497` delegating the same eight points at `:494-496`, gate at `:769-772`,
  three `R43-C1-*` cases at `:1232-1237` (`pins.txt:35-55`).
- Route text this section answers: `SKILL.md:3893-3896` —
  "Not fixed here (routed): `tools/boot-chain-audit.sh:480-487` `find … -quit | grep -q .` reads false under pipefail
  whenever `find` exits 1 on a missing start point, so `BOOTED-OBSERVED` can be awarded while an input is newer than
  boot start (wave-1 `C1SweepSites`)".
- Round-43 entry rows at their sections: SR1 `:17`, SR3 `:45`, SR6 `:80`; scope/triage/limits `:7`, `:114`, `:124`
  (`pins.txt:58-62`). Round-42 entry's supersession pointer present at `btrfs-scrub-record-r42.md:4`
  ("SC1 and SC3 below stand withdrawn … and are not a verified outcome").
- Receipt values quoted below: `before/c1-before.jsonl` — `verdict FAIL`, `cases 16`, `correct 8`,
  `selftest_line "TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=45 failed=0"`, `selftest_r43 0`, wrong ids
  `miss/etc/fstab-newer`, `miss/etc/crypttab-newer`, `miss/etc/mkinitcpio.conf-newer`,
  `miss/etc/mkinitcpio.conf.d-newer`, `miss/etc/default/limine-newer`,
  `miss/etc/limine-snapper-sync.conf-newer`, `multi-miss-deep-modules-newer`, `unreadable-dir-modules-newer` (each
  `expect 1, got 0`); `after/c1-after-717b716.jsonl` — `verdict PASS`, `correct 16`, `total=48`, `selftest_r43 3`,
  `wrong []`; `controls/battery-summary-c1.jsonl` — `should_fail_accepted 0, control_accepted 1` with per-control
  `correct` 8, 9, 14, 8, 8, 9, 12 (K0-K6, K6 also `selftest_pass 0`), K7 16 `PASS` recorded, K8 16, K9 16, K10 15.

## 2. Proposed text (a) — exact, append-only

```markdown
## Boot-input freshness under pipefail — round 43

Appended 2026-10-26 (round-43 C1; wave seat ScribeSkill drafted, the L1 integrates). Defect
R42-C1-COUNTER-AMEND item 5 (`corpus/lessons/round-42-verifier-spotcheck.md:201-207`), routed by the round-42
section above ("Not fixed here (routed)", `:3893-3896`). Base `6951ead90566b2d74f7c45b4efca29246badad64`; fix
`717b716a8943151ace8657e0ca23d7d9b8434f26`. Evidence: `.ufo/waves/round-43/` (`before/`, `after/`, `controls/`,
`w1/`).

`tools/boot-chain-audit.sh` runs under `set -uo pipefail` (`:139`). At the base `boot_inputs_newer` (`:463-488`)
asked `find <8 start points> -newermt "@$btime" -print -quit 2>/dev/null | grep -q .` and printed 1 only when the
pipeline succeeded. `find` exits 1 when a start point is missing or a directory is unreadable; under pipefail that
status outranks a matching `grep`, so the pipeline read false and the function printed 0 — "no input newer than boot
start" — while find had listed a newer input. The audit consumes that 0 in the BOOTED-OBSERVED gate
(`newer=$(boot_inputs_newer)` at `:749`, `[ "$newer" = 0 ]` at `:761`), so the fail-open awards
BOOTED-OBSERVED to an entry whose boot-chain inputs are newer than boot start:

| Where the pipeline sits | Signature | Seen at the base |
|---|---|---|
| a start point missing and the newer input listed after it in find's argument order | find exits 1, grep matched, the pipeline returns 1, the function prints 0 | six `miss/etc/*-newer` cases, expected 1 got 0 (`before/c1-before.jsonl`) |
| an unreadable directory before the match (`/etc/mkinitcpio.conf.d`, mode 0700, not the caller's) | find's error status masks the later match the same way | `unreadable-dir-modules-newer`, expected 1 got 0 |
| 2-4 `/etc` start points missing, a file three directories deep under `/usr/lib/modules` newer | same masking | `multi-miss-deep-modules-newer`, expected 1 got 0 |

Rule (any lane bash under `set -o pipefail` whose input set may contain a missing or unreadable path): decide on the
command's output, never on its status. Capture the text and test that —
`hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null); [ -n "$hit" ]` — or neutralise the failing command's
status before the pipe, `{ find … || true; } | grep -q .`, which passes the frozen counter as control K9. `2>/dev/null`
hides the error text, not the exit status; `|| true` after the command that may fail is what leaves the pipeline's
status to the reader.

Fix at `717b716`: new helper `inputs_newer_than <epoch> <paths…>` (`:463-475`) decides on
`hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)`; `boot_inputs_newer` (`:477-497`) calls it with the
same eight start points in the same order (`:494-496`); the gate reads the same 1/0. Three selftest cases —
`R43-C1-missing-start-point-none-newer`, `R43-C1-missing-start-point-deep-newer`, `R43-C1-all-present-deep-newer`
(`:1232-1237`) — take the selftest from 45 to 48 (`PASS total=48 failed=0`).

Counter: `python3 tools/score-bootinputs-r43.py --revision <REV> --scratch <DIR>` (sha256
`886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f`) — PASS iff `cases == 16 and correct == 16 and
identity_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r43 >= 2`. Sixteen production-path cases run
`boot_inputs_newer` in a private user+mount namespace (tmpfs over `/etc`, `/usr/lib/initcpio`, `/usr/lib/modules`,
values drawn per run) after `setpriv` at the caller's uid/gid, plus a live leg against an independent Python walk and
the script's own selftest. At the base: FAIL, `correct` 8 of 16; at the fix: PASS, `correct` 16, `selftest_r43` 3.
Receipts `before/c1-before.jsonl`, `after/c1-after-717b716.jsonl`.

Controls (`.ufo/waves/round-43/controls/`, `battery-summary-c1.jsonl`: `should_fail_accepted 0, control_accepted 1`):
K0 do-nothing, K1 constant 1, K2 `/etc` start points dropped, K3 uid-gated, K4 env-gated, K5 name-gated
(`/etc/crypttab`), K6 `-maxdepth 0`, K10 missing-point pre-filter each FAIL the counter; K8 candidate and K9
`{ find … || true; } | grep -q .` PASS. K7, a fix gated on tmpfs in `/proc/self/mountinfo`, also PASSes: the
namespace's mount table is the declared open channel, and `/proc/self/uid_map` and the `/mnt/bca-lib.sh` source path
are open with it (`tools/score-bootinputs-r43.py:35-39`).

Limits: the counter scores `boot_inputs_newer`'s value, not the verdict line; the gate plumbing is
`w1/C1ExecHandRepro.md` §1. The three selftest cases kill the decision-site mutants (decision inverted, anchor
swapped, status-vs-output) and leave list-membership and stderr-quietness mutants to the counter
(`w1/C1MutSelftest.md` §Survivors).
```

## 3. Proposed text (b) — exact, append-only

```markdown
## Scrub record re-grounded — round 43

Appended 2026-10-26 (round-43 C2; wave seat ScribeSkill drafted, the L1 integrates after the counted wave-2 reads).
Entry `corpus/knowledge/btrfs-scrub-record-r43.md` rows SR1, SR3, SR6 on S237 (btrfs-progs v7.1 `cmds/scrub.c`,
round-42 snapshot), S240 (Linux v7.2.11 `fs/btrfs/ioctl.c`) and S241 (own-work host capture). Rows SC2, SC4 (as
narrowed) and SC5 (as narrowed) of "Scrub status record — round 42" are not restated here. Nothing here runs a
scrub, writes `/var/lib/btrfs` or calls a privileged ioctl.

| Observation | Reading | Action |
|---|---|---|
| `scrub.status.<fsid>_tmp` beside the record | the staging file of every record update: opened `O_WRONLY\|O_CREAT` with no `O_TRUNC` (scrub.c:483, :517), written from the start, renamed over the record only when the write returned no error (scrub.c:917-925); no code in `scrub.c` unlinks a `_tmp` (its three `unlink` calls name the progress socket path, scrub.c:1485) (SR1) | not a second record; a `_tmp` left by a failed write or rename is reused by the next update, and a shorter later record can leave the older record's tail inside the renamed file [inference] (SR1) |
| a record that fails to parse after a failed or killed write | the leftover `_tmp` tail, not a device fault [inference] (SR1; entry "How this changes OS triage") | look for `scrub.status.<fsid>_tmp` before writing "corruption" |
| `btrfs scrub resume` | the same function as `start`, `scrub_start(…, true)` (scrub.c:1833); every record write passes each device through `scrub_resumed_stats`, which for a resumed device writes the interrupted record's counters added to the new run's, that record's `t_start` (scrub.c:823) and the two durations summed (scrub.c:864) (SR3) | do not subtract a previous reading: those counters and the start time are cumulative over the interrupted run and the resume (SR3) |
| record counters all zero | written by a fresh `start` with no `resumed` source — the "all-zero progress file for a start" (scrub.c:1502); only a fresh start writes zero counters (SR3) | read zero counters as a start baseline, not as a resume's history |
| a scrub whose recording failed exits 0 | a mid-run record-write failure prints "recording progress failed" (scrub.c:1698) and a failed final write "failed to record the result" (scrub.c:1706) only when `do_print` is set — false by default, set by `-B`, cleared when output is quiet (scrub.c:1249, :1295, :1333) — and neither branch assigns the command's `err` (SR3) | judge recording by the record file or a `-B` run, never by the exit status; a default start (no `-B`) fails to record silently |
| `btrfs scrub status` prints `running` | in the status command the running state comes only from `is_scrub_running_in_kernel` — `BTRFS_IOC_SCRUB_PROGRESS` once per device, 1 only when a call returns 0, any failed call reading as not running (scrub.c:1200-1201, :1946, :341) (SR6) | running is an elevation-gated reading: Linux v7.2.11 returns `-EPERM` before doing anything else without `CAP_SYS_ADMIN` (ioctl.c:3132-3133, dispatch ioctl.c:5582; start and cancel likewise, ioctl.c:3072, :3120), so an unprivileged `btrfs scrub status` never prints `running` |
| no `/var/lib/btrfs/scrub.status.<fsid>`, `no stats available` | no record on this host (capture.txt:7); as uid 1000 with no effective capabilities the probe failed `EPERM` (capture.txt:6) and `btrfs scrub status /` exited 0 printing `no stats available` (capture.txt:8, :10) (S241; SR1/SR3/SR6 host readings) | stored-data integrity stays `UNVERIFIED` (SH4); a user-level census reads the record's absence or its mode-0600 refusal, never the kernel's running state (SR6) |

Pointer: SC1 and SC3 of the round-42 entry stay withdrawn (`corpus/knowledge/btrfs-scrub-record-r42.md:4`,
"Corrections — round-42 wave 2"); their write-discipline, resume and failure-report points are the SR1 and SR3 rows
above, and SC4's running-state note is SR6. Do not cite the round-42 SC1/SC3 sentences as a verified outcome.

Counter: `python3 tools/check-scrub-record-r43.py --revision <REV>` (sha256
`b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854`) — PASS iff `rows == 3 and quotes_ok == 3 and
props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok ==
1`. `verdicts_ok` counts only the wave-2 `C2RevSR<n>`/`C2CritSR<n>` seats bound through `w2-dispatch.json` +
`w2-results.json` with the anchored line `ROW SR<n> VERDICT: holds|partly|fails`; wave-1 C2 reviews are first
falsifiers of the draft text, not verdicts. A wave-2 `fails` on a row withdraws that row from this table
(`r42.md:171-176` is the precedent).

Limits: upstream behaviour is pinned at btrfs-progs v7.1 and Linux v7.2.11 source lines; whether the Arch kernel
build patches `fs/btrfs/ioctl.c` is not checked. SR1's trailing-bytes consequence is read from the open flags and was
not reproduced (no record exists on this host and no scrub is run). No census arm reads the record.
```

## 4. Conflicts filed by wave-1 seats that bear on section (b)

These are first falsifiers, not counted verdicts, and none of them changes the text above (which stays inside the
entry's claims); they are the reasons the L1 must not integrate section (b) before the wave-2 reads land.

- **SR3, the resume mechanism is unreachable with self-written records.** `w1/C2DraftCritSR3.md`
  (VERDICT: defect-found) §F1: the writer emits `scrub_writev(fd, buf, sizeof(buf), "%lld", use->scrub_args.devid)
  || scrub_write_buf(fd, buf, ret)` at scrub.c:867-869 with `ret` still 0, so "the device id is never emitted"; the
  reader requires a digit after the fsid colon (scrub.c:693-698), so self-written records "parse with devid 0 and
  match no device", `last_dev_scrub` yields NULL, and resume prints "nothing to resume" (scrub.c:1452-1457,
  1727-1728). The same report calls this "a long-standing upstream behavior", not a freeze artifact. **The
  `btrfs scrub resume` row and the "only a fresh start writes zero counters" row in my table describe
  `scrub_resumed_stats` code that this finding says never engages for records this binary wrote.** Wave 2 must
  decide; if SR3 fails, drop both rows and keep the recording-failure row (§F3/F4 there confirm it: `do_print`
  default false / `-B` / quiet clearing, and "neither branch assigns `err`").
- **SR3 §F2** also narrows the zero-counters row: recording can be disabled (`do_record=false`, scrub.c:1335-1339,
  1505-1509) so no record is written at all, and a resume's pre-fork first record writes zeros for skipped devices.
- **SR1, three clauses overreach.** `w1/C2DraftCritSR1.md` §F1 (a killed writer: the progress thread defers
  cancellation across open→rename, :905/:941, and the parent ignores SIGINT, :426-434, so only uncatchable or
  default-terminate kills can leave a partial `_tmp`), §F2 ("mode 0600" is the mode argument, effective mode subject
  to the umask), §F4 (the trailing-bytes inference needs the next write *and* rename to succeed). My rows keep the
  entry's wording; a wave-2 `partly` should take those three narrowings.
- **SR1/SR3 interaction on parse failures.** `w1/C2DraftCritSR3.md` §F1 closing note: "`invalid data on line`
  warnings occur for every self-written record even with no trailing bytes, independent of the SR1 leftover-`_tmp`
  mechanism." That weakens the second row's "look for `_tmp` before writing corruption" as a complete reading.
- **SR6, scope and premises.** `w1/C2DraftCritSR6.md` (VERDICT: draft) §F1: "Whether a scrub is running comes only
  from the kernel" holds for the status command but not the CLI (the record gate `is_scrub_running_on_fs`,
  scrub.c:1392, and the progress socket, :1474-1476). My table row is scoped to `btrfs scrub status` for this reason.
  §F2: the success direction (a 0 from `BTRFS_IOC_SCRUB_PROGRESS` implies an active scrub) rests on
  `btrfs_scrub_progress` in `fs/btrfs/scrub.c`, which is not in the frozen set — the entry does not mark it
  `[inference]`. §F3: `capable()` is initial-userns-scoped, an inference not in the pinned set.

## 5. Other findings (outside the two drafts)

- **Registry coverage.** `w1/C1ExecBootTools.md` (VERDICT: defect-found) §5: `check-registry-coverage.py` goes PASS
  (66/66) → FAIL (66/68, two `REGISTRY-ROW-MISSING`) at the fix because `tools/score-bootinputs-r43.py` (and one
  other new tool) has no gate-registry row. Both new sections above name counters, so the integration should land
  with the registry rows from the gate-registry items, not only the prose.
- **Counter channels.** `w1/C1CritChannels.md` (VERDICT: defect-found) finds the C1 namespace leg distinguishable by
  `/proc/self/mountinfo`, `/proc/self/uid_map`, the `/mnt/bca-lib.sh` path, cwd `/mnt/home`, inherited stdin and the
  fixed case families; the frozen `channels_open` names only three of those. My section (a) inherits the entry's
  declared-open wording ("the mount table is the declared open channel, and uid_map and the source path are open with
  it") and should not be read as a claim that those are the only open channels.
- **Existing round-42 SKILL rows still cite withdrawn rows.** `SKILL.md:3908`, `:3910` and `:3913` cite SC1/SC3
  (and `:3917` SC4's running note), which `btrfs-scrub-record-r42.md:4` declares withdrawn. Section (b)'s table
  re-grounds the `_tmp`, recording-disabled and running rows on SR1/SR3/SR6; whether to mark those three older rows
  superseded is the L1's call (append-only; I did not draft that edit and did not touch `SKILL.md`).
- **Selftest coverage.** `w1/C1MutSelftest.md` (VERDICT: defect-found): of mutants (a)-(h), (b) drop `-quit`,
  (c) drop `2>/dev/null`, (d) `| head -n1`, (e) drop `/etc/crypttab`, (f) drop `/usr/lib/modules` survive the three
  `R43-C1` cases; (a), (g), (h) are killed. Section (a) states exactly the killed set and puts the rest on the
  counter.

## 6. What I did not do

No counter run (C1 or C2, battery or census), no clone or fixture, no `--selftest`, no scrub or ioctl, no `btrfs`
mutation, no git/jj mutation, no tool install. The C1 before/after numbers, the battery table and the C2 source
quotes are quoted from committed receipts and the pinned snapshots, not re-observed. I did not edit `SKILL.md`, the
knowledge entries, `SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md` or any tool; I did not draft the counter-lineage or
scoreboard rows (other seats' items).

Receipts: `.ufo/waves/round-43/w1/ScribeSkill/pins.txt` (observed commands and outputs, 94 lines).
Scratch `/fast/scratch/hyaku/tsukuroi-r43/ScribeSkill/` created and removed unused.
