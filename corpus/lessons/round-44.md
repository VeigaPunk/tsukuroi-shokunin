# Round 44 — lesson (tsukuroi, hyaku run 9)

author: tsukuroi L1 (`TsukuroiR44`), 2026-10-26. Base `98020ece0674e0b569ee23aed10ffbee355b248e` — the lane tip at round
start as `jj-lane.sh state` printed it. Claims, controls and outcome: `SCORECARD.md` sections "Round 44 — declaration"
and "Round 44 — measured outcome". Waves: two v1 waves, `w1` (build + first falsifiers, 46 seats) and `w2`
(falsify, with the six counted C2 row verdicts); specs, dispatches and the orchestrator's results files are in
`.ufo/waves/round-44/`. Seats are the lane, not outside reviewers (LEARNING.md); this round's non-author closure is
pending.

The round-43 closure's spot-check is answered by `corpus/lessons/round-43-verifier-spotcheck.md`: §2 verified C1 and
C2; §5 routed R43-SR1-LIMITS-CONTRADICTION (fixed this round, below) and carried the C2 binding gaps (closed in the
round-44 counter) and the census readers (still routed).

## Gate

### New SOURCES rows (opened 2026-10-26 by this round's L1; each quote located with `grep -n` in the pinned snapshot; drafted by wave-1 seats SrcGateNew/SrcGateReopen, checked by the L1)

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S242 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/scrub.c?h=v7.2.11 (raw `plain/…?h=v7.2.11`; same bytes at https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/scrub.c) | "return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;" | scrub.c:3336 |
| S243 | https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/sysfs.c?h=v7.2.11 (raw `plain/…?h=v7.2.11`) | "return sysfs_emit(buf, "%llu\n", READ_ONCE(device->scrub_speed_max));" | sysfs.c:2028 |
| S244 | https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/tree/7.1-1 (raw files `btrfs-scrub@.timer`, `btrfs-scrub@.service`, `PKGBUILD` at tag 7.1-1, commit 0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0) | "install -Dm644 btrfs-scrub@.service "${pkgdir}/usr/lib/systemd/system/btrfs-scrub@.service"" | PKGBUILD:100 |
| S245 | own-work capture `.ufo/waves/round-44/frozen/hostcap/` (`capture.sh`, run 2026-10-26T23:53:22Z, uid 1000) | "var_lib_btrfs absent"; "scrub_speed_max …/devinfo/1/scrub_speed_max mode=644 owner=root value=0"; "wants_btrfs_scrub_instances 0" | capture.txt:3,4,5 |

Snapshot digests: `.ufo/waves/round-44/frozen/src/SHA256SUMS` (scrub.c `f347931b…5b8`, sysfs.c `ce146120…c43`,
units `9a0b6cc2…`/`eaa7af92…`, PKGBUILD `3b803e8b…`), fetch log `FETCH.txt`; capture.txt `efb52388…4900`,
capture.sh `6a297e4f…f6d`. Live re-fetches by wave-1 seats SrcGateNew/SrcGateReopen/C2ExecLiveSources were
byte-identical; tags peeled and listed in FETCH.txt.

### Re-opened rows and rows touched old→new

| Row | Change (this round) | Log |
|---|---|---|
| S237 | used-by gains `btrfs-scrub-record-r44.md` | `git diff 98020ece 7e081698 -- corpus/SOURCES.md`, column 11 only |
| S240 | used-by gains `btrfs-scrub-record-r44.md` | same; both rows re-fetched byte-identical (SrcGateReopen) |

Census (frozen commands): start `tsukuroi ok`, exit 0, 40 W04, 241 rows; end exit 0, 245 rows
(`.ufo/waves/round-44/before/sources-census-start.txt`, `after/sources-census-final.txt`).

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R44-L1-FLEET-ROOT-FIXTURE | scope | Wave-1 seat C1ExecEdgeNames wrote a fixture tree `fx/A2-uppercase-fsid-sysfs/...` into the FLEET ROOT /home/vgpnk/Projects/shokunin (relative path, cwd = fleet root; orchestrator notice 2026-10-26T21:14Z moved it byte-unchanged to `.tower/quarantine/fleet-root-strays-20261026T2114/`; the seat disclosed it in its report) | host guard in every wave context ("never create files at the fleet root"; cd to scratch first) | The seat rebuilt fixtures under `/fast/scratch/hyaku/tsukuroi-r44/<seat>/`; the round's final sweep found no further fleet-root strays. Able to fail: `git -C /home/vgpnk/Projects/shokunin status --porcelain` printed the tree (red at 21:14), empty at close |
| R44-W1-UNREPORTED-SEATS | delivery | Two w1 seats settled without a report file: C1MutArm (scored mutants a-l; receipts `w1/C1MutArm/mut-*.json`; final text in its transcript) and SentMisroot (final text named a round-43 path; receipts `w1/SentMisroot/`) — both reconstructed by the L1 into `w1/C1MutArm.md` and `w1/SentMisroot.md` from their transcripts | round prompt §4/§6 (every seat settles with a report) | The L1 wrote the two reports from the transcripts (byte-exact final texts, path-corrected). Able to fail: the wave's results ledger lists the two seats with verified final outputs, and the reports exist |
| R44-L1-TIMERS-BRANCH | code | While integrating the C1 hardening the L1 first placed the timer-count loop inside the unreadable-wants branch (lost `blocked=1` and the `else`), so `timers=` was 0 for enabled instances; caught by the census selftest (scrub-timers failed; direct probe timers=0) | QUALITY: the selftest asserts contract behaviour | The branch was restored (unreadable wants → `timers:unreadable`; listable wants → count, excluding directories); selftest 148/148 and the C1 counter PASS. Able to fail: `bash tools/tsukuroi-census.sh --selftest` was FAIL before the fix, PASS after |
| R44-C2-SR7-REPLACE-OMISSION | depth-overreach | The first SR7 draft said a context is attached exactly while `btrfs_scrub_dev` runs; before w1 the L1 added the device-replace caller as an honest [inference] (dev-replace.c:701-703,1265-1268), and C2ExecKernelSR7/C2DraftCritSR7 confirmed the invariant and the locked window (attach 3159, clear 3222, no mid-run return) | none — a pre-freeze self-check (the L1 read dev-replace.c) | Narrowed wording integrated before w1 ended (wave-2 counted reads judge it). Able to fail: the pre-narrowing sentence fails C2DraftCritSR7's window check |
| R44-C2-CONTROL-K17-CATCH | calibration | The C2 counter's first `source:` check searched the whole line, so an S-id named only in the line's prose satisfied it; the pre-data control K17 (S244 dropped from the lead list) FAILed only after the counter was fixed | none — caught by the round's own control battery | The counter now parses the lead id list only. Able to fail: control C2-K17 is red on the unfixed counter |

## Round-43 routed defects — round-44 disposition

1. **R43-SR1-LIMITS-CONTRADICTION** — repaired: `btrfs-scrub-record-r43.md` gains "Corrections — round 44"
   (the trailing-bytes consequence was reproduced in a harness, not "not reproduced"); SKILL.md already read
   "[inference, reproduced in a harness]", PROVINCE.md carries no reproduction claim (ScoutR43Defects).
2. **Item 2 (C2 binding gaps)** — closed in `tools/check-scrub-record-r44.py`: padded lines, blank-prefixed
   outputs and a contradictory JSON `verdict` key all bind nothing (controls C2-K14/K15/K16). Still open, recorded:
   duplicate `verdict_line` keys (json last-wins, C2MutBinding F1) and malformed record files crash the counter
   (C2MutBinding F4); residual seats are forgeable like the main path; the C1 counter's live leg accepts a cached
   live answer (C1CritEvasion F1) and the open channels set is understated (C1CritChannels).
3. **Item 3 (census readers)** — still routed: the `:746` foreign-baseline lookup (now `:779`) and the five
   single-line probe readers (now `:967,:1005,:1087,:1462,...` by content) have no regression case; planned for a
   census-surface round (round-45 planned row).

## Spot-check candidates for the non-author closure

One admit per claim: C1 — the arm's live NONE line and the read-only strace (29 syscalls in the arm window,
`w1/C1ExecLiveRead.md`); C2 — SR7's `-ENOTCONN`/`-ENODEV` semantics against scrub.c:3336 and the replace caller
(dev-replace.c:701-703,1265-1268). One reject candidate: the staged `btrfs-ioctl-surface-r27.md` (S223; 64 ioctl
dispatch labels vs its nine-row table, wrong tag v7.2) — asmGate §4.
