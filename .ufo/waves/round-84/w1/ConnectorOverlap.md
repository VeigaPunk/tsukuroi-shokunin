# ConnectorOverlap — round 84 / w1 — sibling-overlap scan, hibernate-resume surface

Seat: ConnectorOverlap (connector, leaf). Judged axis: **adjacency**; lane axes: operability + freshness.
Lane revision measured: `f19e73f3aa9817e76044e4e43a343c6ca6d929df` (`git -C tsukuroi-shokunin rev-parse master`,
rc 0; tip has moved past the ticket's `69915b86` through `c6941adb` and `f19e73f3`, row-registry repairs only).
Freeze `e0f42051`, candidate `c6ee78b2`, C1 re-declaration `69915b86` read as declared.
No tool was installed or updated for this seat. Scratch root `/fast/scratch/hyaku/tsukuroi-r84/ConnectorOverlap`
created, used only for the scan receipt, and removed on exit. No lane file edited; no git/jj mutation.

## Axes named

1. **adjacency** (judged) — does every hibernate-resume fact have a single named owner, with a stated split where a
   sibling reads the same bytes?
2. **freshness** — is the surface's dated-input story honest (config drift between captures)?
3. **operability** — does the surface land in PROVINCE where the gate can be found and run?

## Method and receipts (verbatim, exit codes)

Scan spec: `hibernat|resume_offset|map-swapfile|swapfile|/sys/power` in each sibling's `PROVINCE.md`, `SKILL.md`
and `corpus/knowledge`; then the semantic family (`swap`, `CommitLimit`, `memory pressure`) in sibling
`PROVINCE.md`; then `/swap/swapfile` in sibling `corpus/evidence`. 20 sibling `*-shokunin` dirs (all except
tsukuroi); non-lane dirs in the fleet root (`counters/`, `exp-full/`, `reports/`, `tools/`, …) skipped.

```
$ git -C tsukuroi-shokunin rev-parse master
f19e73f3aa9817e76044e4e43a343c6ca6d929df
rc=0

$ ls -d *-shokunin | grep -v tsukuroi | wc -l
20
rc=0

$ rg -n -i -e hibernat -e resume_offset -e map-swapfile -e swapfile -e /sys/power <lane>/PROVINCE.md <lane>/SKILL.md <lane>/corpus/knowledge   (all 20 siblings)
mori-shokunin/corpus/knowledge/uptime-win-r70.md:31:- **K4** — `S582.html:842` — "To obtain the time the system has spent in the working state since it was started, use the QueryUnbiasedInterruptTime function.": the doc's own pointer defines the boundary — this count is NOT working-state time and includes sleep/hibernation time; `count=biased` travels on every receipt line so the caveat cannot be lost in a copy.
mori-shokunin/corpus/knowledge/uptime-win-r70.md:41:`unavailable` with a reason, never zero. No `boot id`, no sleep/hibernation
mori-shokunin/corpus/knowledge/workstate-win-r71.md:23:uptime probe's count, which INCLUDES time asleep or hibernating per the
mori-shokunin/corpus/knowledge/workstate-win-r71.md:29:never attributes a sleep or hibernation episode, never names a boot
mori-shokunin/corpus/knowledge/workstate-win-r71.md:39:- **K5** — `S584.html:830` — "reflects only the time that the system is in the working state" and "not 'biased' by time the system spends in sleep or hibernation": the working-state boundary this probe reports. The pair (biased, unbiased) and their delta are printed as counts; the probe never decomposes the boot into episodes and never claims a sleep event — a strongly positive delta would bound accrued non-working time within the boot window, and nothing more.
mori-shokunin/corpus/knowledge/workstate-win-r71.md:56:attribution, no sleep/hibernation decomposition, no wake/sleep timestamps,
mori-shokunin/corpus/knowledge/workstate-win-r71.md:64:Boundaries: writing power configuration, diagnosing sleep/hibernation or
mori-shokunin/corpus/knowledge/workstate-win-r71.md:78:failed-call 26 words, sleep/hibernation 15 words). K1–K6 quote texts are
rc=0

$ rg -n -i -e '\bswap\b' -e 'CommitLimit' -e 'memory pressure' <lane>/PROVINCE.md   (all 20 siblings)
10:resource runway (disk on the fleet root and `/tmp`, memory pressure); lane silence grading (silent / progressing / progressing-weak).
276:  which today names memory pressure, to the one-shot system CPU/IO/IRQ/memory pressure
404:- **Core, commit-ledger runway read (`tools/mori-commit-runway.py`; round-53 C2):** reads `CommitLimit`,
411:  `overcommit_memory` 0 the two lines are printed but never compared, so `Committed_AS` above `CommitLimit` is
412:  normal (`over_limit_not_enforced`) and only a single request larger than RAM + swap is refused
414:  (read `MemAvailable`); under 2 the limit is enforced, `usable_kb = CommitLimit - Committed_AS -
446:  on the fleet root and `/tmp`, memory pressure)" — with VM commit accounting under the overcommit mode, a
552:| `tools/mori-commit-runway.py` | gate | commit runway (r53, C2) | Read CommitLimit and Committed_AS with the overcommit-mode enforcement context. |
rc=0
```

Every line of the second and third blocks is `mori-shokunin/PROVINCE.md` (the loop's `$d` prefix was trimmed for
width). The decisive negative: **0 hits** for `resume_offset`, `map-swapfile` or `/sys/power` in any sibling
`PROVINCE.md` or `SKILL.md`, and **0** in any sibling `corpus/knowledge` file. The resume chain is unheld sibling
ground.

```
$ rg -ln -e '/swap/swapfile' <lane>/corpus/evidence   (all 20 siblings)
kengaku-shokunin/corpus/evidence/round12-fleet/r12-endpoint-freshness.md
rc=0
```

## Hit table

| # | Lane | file:line | Quote (≤25 words) | Verdict | Handling |
|---|---|---|---|---|---|
| H1 | mori | `corpus/knowledge/workstate-win-r71.md:64-66` | "writing power configuration, diagnosing sleep/hibernation or boot state, and anything preceding the current boot are tsukuroi/operator ground" | tsukuroi-owned (sibling self-refusal naming this ground) | cite as the positive anchor for the whole r84 surface; report-not-absorb |
| H2 | mori | `PROVINCE.md:13` | "systemd unit, driver/firmware and boot state (→ tsukuroi)" | tsukuroi-owned | cite alongside H1; no handoff packet needed |
| H3 | mori | `corpus/knowledge/uptime-win-r70.md:31,41` | "includes sleep/hibernation time; `count=biased` travels on every receipt line" | no overlap (Windows uptime boundary; explicitly refuses episode attribution) | report-not-absorb; nothing to absorb |
| H4 | mori | `corpus/knowledge/workstate-win-r71.md:23,29,39,56,78` | "uptime probe's count, which INCLUDES time asleep or hibernating per the" | no overlap (same boundary class as H3) | report-not-absorb |
| H5 | mori | `PROVINCE.md:10` | "resource runway (disk on the fleet root and `/tmp`, memory pressure); lane silence grading" | shared evidence (capacity/pressure vs resume precondition) | split by question, below; report-not-absorb |
| H6 | mori | `PROVINCE.md:404-405,412,552` | "reads `CommitLimit`, `Committed_AS`, `MemTotal`, `SwapTotal` … from `/proc/meminfo`" / "only a single request larger than RAM + swap is refused" | shared evidence: `SwapTotal` is read by both lanes for different questions | report-not-absorb; `HR-SWAP-TOO-SMALL` is not a capacity alarm |
| H7 | mori | `PROVINCE.md:286-289` | "tsukuroi's census reads the same system `/proc/pressure/memory` file … Shared evidence is not shared ownership" | no overlap (different file: PSI, not swap) | reuse as the **precedent text** for H5/H6; no edit |
| H8 | kengaku | `corpus/evidence/round12-fleet/r12-endpoint-freshness.md:661-662` | "`/swap/swapfile file 30.3G 3G 0`" / "`/dev/zram0 partition 22.7G 21.4G 100`" | shared evidence (host `/proc/swaps` capture, 2026-09-29) | report-not-absorb; freshness note R2/R3 below |
| H9 | mado | `corpus/knowledge/idle-lock-plane.md:192` | "before suspend: `OMARCHY_LOCK_ONLY=true omarchy-system-lock` (lock without the DPMS half)" | no overlap on HR1-HR10; boundary note | mado owns the config that *triggers* a sleep transition; the disk-hibernation chain stays here |

Nothing in the hit set requires a handoff packet: H1/H2 already assign the ground, and H5/H6/H8 are shared
*evidence*, which the lane's own rule (`PROVINCE.md:41` "Shared evidence is not shared ownership") forbids
absorbing.

## The ownership question asked: mori (swap pressure) vs tsukuroi (boot/resume chain)

**HR5 — "the swap file must be active (`/proc/swaps`)" → tsukuroi-owned.**
The fact read is *membership* of the file that the cmdline's `resume=` device hosts — a boot precondition in the
same evidence class as `/proc/cmdline`, and the same class H1/H2 name as tsukuroi ground. Mori's two swap reads are
different questions: `SwapTotal` for overcommit accounting (H6, a capacity number over a ledger) and "memory
pressure" as a runway (H5, a rate over a window). Neither is a boolean "is this swap area active at capture".
The gate already keys family `HR-NO-ACTIVE-SWAP` on `swaps[]` emptiness, so the rule and the ownership agree.
Counter-case considered: H5's word "pressure" could be stretched to cover "swap in use"; it cannot, because a
pressure claim is a trend and HR5 is a precondition — and mori's own `COMMIT_LOW` text refuses to be a calibrated
alarm, the same discipline HR5 needs.

**HR10 and gate rule 7 `HR-SWAP-TOO-SMALL` → tsukuroi-owned as an *image-fit* finding; mori keeps free swap as
capacity/runway.**
`/sys/power/image_size` is a hibernation-kernel ABI value (S340 `sysfs-power:97-98`), and the finding asks "will
the image fit in the swap the resume device can hold", not "is the host short of swap". Both lanes read the same
numbers; that is the round-26 wave-2 disk split applied to swap: *free swap as hibernation-image fit is this
lane's, free swap as fleet capacity is mori's* (`PROVINCE.md:165-166` "disk-space runway and free-capacity
reporting remain mori's" + `:176` "The split is by question: free space as fleet runway is mori's, free space as
an upgrade or boot precondition is this lane's"; `corpus/README.md:244` "Disk-space runway stays with mori"). The r24 PSI
adjacency (H7) is the same shape and already accepted by both lanes.
**Stated contradiction, not smoothed:** the two lanes can print opposite verdicts over identical bytes — this gate
`HEALTHY` while mori's runway reads low — and both are correct because the claims differ. The report must not
compose them into one score; `HR-SWAP-TOO-SMALL` carries no capacity meaning and must never be quoted as one.

## Second-order finding — freshness (reported, not patched)

Gate rule 7 is frozen as `sum((size_kib - used_kib) * 1024) < image_size` over **all** `swaps[]` entries
(`tools/check-hibernate-resume.py:113-116`; frozen at `tools/resume-gate-battery-r84.py:23`). On the pinned capture
that is exactly one entry (`/swap/swapfile file 31722876 11942400 0`), so there is no live effect and **this is not
a C2 defect** — the gate implements the frozen rule faithfully. The risk is in the rule's domain: this lane's own
corpus holds `zram0` as an active 4 GiB priority-100 swap (`corpus/knowledge/kill-event-deep-r8.md:259`;
`corpus/knowledge/oom-event-plane.md:348`), kengaku's 2026-09-29 capture shows it at 22.7 GiB (H8), and today
`/proc/swaps` has one row with `zswap.enabled=1` on the cmdline (was `zswap.enabled=0`,
`oom-event-plane.md:348`). A hibernation image is written to the `resume=` device (S338
`swsusp-and-swap-files.rst:40-56`), so a compressed-RAM block device is not image-capable [INFERENCE from S338 +
zram's nature]. A future boot with a fresh zram swap device would therefore inflate rule 7's free sum and produce a
false `HEALTHY`. Recorded as a named limit for the next declaration — **no patch proposed and no rule changed**,
because amending a frozen rule after the candidate exists is exactly the r81/r82 root failure.

Same class: HR1's "its only swap area is a file" and HR10's "≈20.3 GB free swap" are *dated* host facts. The
recheck trigger is the `/proc/swaps` row count and per-row `type`, not only HR6's file birth time (`HR6` covers the
header move, not a new device appearing).

## Which round-84 surfaces should enter tsukuroi PROVINCE Core vs Frontier

Append point: `PROVINCE.md` is 573 lines, last section "Round 76"; the r84 section goes at EOF, append-only.
Promotion rule in force: a Frontier area becomes Core only after a runnable read-only arm reads it
(`corpus/README.md:244,383`; r76's `systemd-analyze cat-config`/`journalctl` arms entered Core on that reading).

**Core (propose):** one paragraph carrying the gate as the arm —
`resume=`/`resume_offset=` on `/proc/cmdline`; `/proc/swaps` active file swap and its type; `map-swapfile -r`
offset versus the cmdline value; the file's `C` attribute; `/sys/power/resume`, `/sys/power/resume_offset`,
`/sys/power/state`'s `disk` token, `/sys/power/disk`, `/sys/power/image_size`; mkinitcpio `HOOKS` order with
`resume` after `encrypt`. Arm: `python3 tools/check-hibernate-resume.py --live` (rc 0/1/2, 11 finding IDs;
registry `SKILL.md:5917`). Core also carries the one-sentence split: free swap as image fit is this lane's, free
swap as capacity is mori's (H5/H6), and `HR-SWAP-TOO-SMALL` is not a capacity alarm.
Operator-owned: hibernating, `swapon`/`swapoff`, `btrfs filesystem mkswapfile`, mkinitcpio, limine/UKI entry
regeneration, any `/sys/power/*` write.

**Frontier (no arm reads it):** HR3's `filefrag`-versus-`map-swapfile` discrimination (no rule reads `filefrag`;
HR2's cmdline-vs-`map-swapfile` half *is* gate rule 2, so cite HR2 Core and HR3 Frontier); HR4's mount-option
relation (`compress=zstd:3` with a NOCOW file — the gate reads only the attribute bit); HR6's birth-time recheck
trigger; HR7's claim that `systemd-hibernate-resume` *wrote* `/sys/power/resume` (an observed value is not the
write); HR8's "sysfs overrides cmdline" behaviour (the gate compares equality, rule 4); HR9's initramfs binary
presence (the UKI listing is a one-off receipt, not an arm); the live resume attempt and `PM: Image not found`
reading (`corpus/knowledge/journal-boot-plane.md:64`); and the zram/`image_size` limit above.

## Risks

- **R1** — the split is unacknowledged by mori or mado; `PROVINCE.md` Frontier already says recipient
  acknowledgement is unverified, so this report must not read as an accepted handoff. No packet prepared: no
  finding is being transferred.
- **R2** — rule 7's sum can include a non-image-capable swap; false `HEALTHY` in that configuration (above).
- **R3** — a sibling holds a *different* `/proc/swaps` picture of the same host (H8, 2026-09-29: two rows, zram
  21.4 GiB used) than the pinned r84 capture (one row). Neither contradicts the other; both are dated. Any text
  that treats "only swap is a file" as a standing property of this host is already stale.
- **R4** — H9: if the desktop idle chain is ever changed to hibernate rather than suspend, the resume chain becomes
  load-bearing for mado's plane. mado owns that config; this lane owns the chain it would exercise.

## Verification (read-only, reproducible)

1. Re-run the three scan blocks above at any revision; expect 8 mori lines, 1 kengaku evidence file, and 0 hits for
   `resume_offset|map-swapfile|/sys/power` outside tsukuroi. A new sibling hit is a new row to classify.
2. Pre-promotion check for the Core paragraph: `rg -n -i 'hibernat|resume_offset|map-swapfile' */PROVINCE.md
   */SKILL.md | grep -v tsukuroi` → empty (held-ground claim).
3. For R2 at the next capture: `cat /proc/swaps` (read-only) — more than one row, or any `partition` row, means
   rule 7's sum covers a device that cannot hold the image.
4. Quote the lane revision with any claim; `master` moved twice during this seat (`69915b86` → `c6941adb` →
   `f19e73f3`).

## Refusals

No lane file edited; no git/jj mutation; nothing written outside `.ufo/waves/round-84/w1/`. No subagent spawned.
No model chosen. No host state touched (the swap/zram readings above are the pinned receipts and sibling text,
not a new host probe).
