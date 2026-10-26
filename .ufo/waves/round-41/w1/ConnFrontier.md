VERDICT: draft

# ConnFrontier — Item X-3: frontier and round 42 (draft)

Assessment basis: round-41 declaration (`SCORECARD.md:2454-2493`, freeze `e479fdc5`, base `0e5805a1`),
implementation commits `568c397d` (C1) and `9cc9aa77` (C2), lane tip `71851d63` at dispatch. Round 41 is
mid-wave (no measured-outcome section exists yet). "Advances" below means *the declared claims move a Frontier
line*; admission is a separate, non-author-closure step I did not run.

---

## 1. Round 41's declared claims, in frontier terms

- **C1 (operability)**: the census `--selftest` (`run_selftest`; `probe_storage_arm` explicitly unchanged) gains
  four mount-table cases — a btrfs line whose mountpoint is not absolute, one whose source is not under `/dev`,
  one with no `subvol=` option, and a table with two btrfs lines — so the round-40 held-out survivors H5, H6, H9
  and the count-direction mutant H10 fail it (`SCORECARD.md:2465`). Implementation `568c397d` touches only
  `tools/tsukuroi-census.sh` (+27 lines, four `check` blocks inside `run_selftest`; `git diff 0e5805a1
  568c397d` shows no `probe_storage_arm` change). This is an **instrument repair on the Core census gate**: it
  pins the mount-table read's tested contract ("count every line whose third field is exactly `btrfs`, regardless
  of source shape, mountpoint shape, option keys, or how many btrfs lines a table has" — `w1/C1HeldOutMutants.md`
  from round 40, reading at `:185-208`), repairing the round-40 counter-sufficiency defect R40-ANSWER-KEY and
  §6.2 (stderr FAIL lines, neutral flakiness, scratch-on-Ctrl-C) (`corpus/lessons/round-40-verifier-spotcheck.md
  :143-149`).
- **C2 (depth, sourced)**: `corpus/knowledge/alpm-package-anatomy-r41.md` PA1–PA8 — the package-file side of the
  **Core pacman-state plane** (`PROVINCE.md` Core, "`.pkg.tar.zst` receipt discipline"; entry header
  `alpm-package-anatomy-r41.md:7-8`: "Scope: the package-file side of the pacman-state plane (`PROVINCE.md`
  Core)"). Rows S227–S236; the read is the per-row reviewer verdict files (QUALITY 81), not the lexical counter
  gates. Implementation `9cc9aa77` touches only that entry (3 lines, pre-dispatch refinement).
- The declaration explicitly takes **no adjacency claim**: "adjacency stays unclaimed and is not harmed"
  (`SCORECARD.md:2458-2459`).

## 2. Which frontier lines round 41 advances

**None of the named Frontier bullets (PROVINCE.md:75-80, 212-214, 234-236; corpus/README.md:28-42, 293-301,
313-317) is advanced by the declared claims.** Both claims work held Core ground (census gate; pacman-state
plane) and repair round-40 counter defects; neither moves a Frontier line to Core, closes a recipient/arbitration
gap, opens a new owned surface, or reads a signal that no census arm reads today.

One indirect effect, same as round 40's: C1's four new cases harden the *instrument* behind the round-39
"remaining limit" (`PROVINCE.md:234-236` — a census that detects the counter's namespace and behaves honestly only
there cannot be told apart on this host). The limit itself is untouched: nothing in C1 changes the live constant
answer (`HEALTHY 1/1/0`), adds a host-side injection, or exercises the production path without the
`TSUKUROI_PROC_MOUNTS` override seam.

## 3. Which frontier lines stay open (all of them)

| Line | Status after round 41 | Evidence |
|---|---|---|
| F1 Recipient acknowledgement / independent replay of handoffs unverified; author-side replay not promotion evidence | open | `PROVINCE.md:77-78`; `corpus/README.md:30-32`; adjacency ceiling `SCORECARD.md:2434` ("recipient acknowledgement and independent replay are unverified") |
| F2 Kaidoku/revenger shipped-artifact RE ownership contested; integrator arbitrates | open | `PROVINCE.md:79-80`; `corpus/README.md:33-34`; R20-OUT009 `PROVINCE.md:148-152` |
| F3 Boot: btrfs-overlayfs snapshot-boot path on a mkinitcpio 42.2 image untested; `/new_root` symlink watch on every mkinitcpio release | open | `corpus/README.md:38-39,151-153`; round-24 notice `corpus/README.md:223-231` |
| F4 Storage integrity: scrub record (SH3/SH4) and NVMe SMART (SH5/SH6) still Frontier, no census arm reads them; second NVMe device (xfs on `/tmp`/`/fast`) unread | open | `PROVINCE.md:212-214`; `corpus/README.md:295-301`; this round adds no `scrub`/`unshare` string to the census (probe receipt) |
| F5 Storage: census honesty indistinguishable on this host (live answer constant); no host-side injection authorized | open (C1 hardens the instrument only) | `PROVINCE.md:234-236`; round-38 known limit closed *for the absent-root rule* by round 39; C1's new cases pin the fixture-side contract, not the live-host distinction |
| OV4/OV5 conflicts with mori (OOMRules= qualifier; earlyoom option) | recorded, unresolved — need mori action | `PROVINCE.md:187-189` |
| ADJ-04 census handoff line (`state=prepared`; round 32) | no state transition possible: mori declares no intake format | `PROVINCE.md:193` |

## 4. Why the round-42 lowest-axis claim should be depth, not adjacency

Depth and adjacency are tied lowest at 8 (`SCORECARD.md:2458-2459`). Every avenue that would move adjacency
8→9 requires an actor outside this lane or outside the province: a recipient-side acknowledgement/replay (F1),
integrator arbitration (F2), mori intake-format or conflict resolution (ADJ-04; OV4/OV5). The round-40 and
round-41 declarations' reason stands — "a sibling acknowledgement cannot be produced by this lane". A
*self-producible* adjacency claim (re-checking sibling pins, counting handoff lines) has been measured before and
is freshness/quality work, not a new adjacency move; a do-nothing control would reach the same counter. So the
planned row works **depth** as the lowest axis and leaves adjacency declared-unchanged (no harm).

## 5. Best round-42 planned row (draft text)

Two claims on distinct axes; both target open Frontier lines (F4, F5); both fail at base (do-nothing-proof).

```
## Round 42 — declaration (planned row, draft)

Base: the round-41 measured tip (declared before the after-run). Ordinals at base: depth 8, coverage 9,
operability 9, freshness 9, calibration 9, adjacency 8; depth and adjacency are tied lowest; saturation 9 /
window 3 unchanged. No adjacency claim is attempted (a sibling acknowledgement cannot be produced by this lane;
adjacency stays unclaimed and is not harmed). C1 works depth on the storage-integrity frontier (the lowest
axis); C2 works operability on the same frontier's named residual limit.

| Claim | Axis | Surface moved | Counter (frozen; sha256) | Before at base | Target (predicate) | Kill rule |
|---|---|---|---|---|---|---|
| C1 | depth (sourced) | `corpus/knowledge/storage-health-r26.md` gains append-only rows SH7–SH10 closing the two unopened leads the round-26 correction explicitly left (`corpus/SOURCES.md` "Leads (unopened)" line 333; round-26 clarification line 338): btrfs-progs 7.x release notes and the ArchWiki Fwupd page. Rows pin the scrub-record mechanics — what `btrfs scrub status` reports per-filesystem (running/finished, timestamp, duration, status code, error sums), where the record lives (`/var/lib/btrfs/scrub.status.*`), how the shipped `btrfs-scrub@.timer` writes it (S131 held), and what an absent/stale record means — plus the NVMe SMART/Health field semantics beyond the Critical Warning byte (SH5/SH6 extension). Host cells recorded read-only: timer `inactive`/`disabled` (`systemctl show btrfs-scrub@-.timer`), status dir absent (`/var/lib/btrfs` ENOENT), second NVMe (xfs on `/tmp`/`/fast`) boundary. No census arm is claimed; the round-26 promotion condition is not met, so F4 stays Frontier | `python3 tools/check-storage-scrub-r42.py --revision <REV>` (frozen; sha256 TBD): reads the pinned source WINDOW per row, the host cells from the frozen capture, and per-row reviewer VERDICT files (same protocol as round-41 C2) | rows absent at base, FAIL exit 1 | `rules_verified == 4 and verdicts_ok == 4 and host_ok == 3 and novelty_base_hits == 0`, PASS exit 0 | a row judged `fails` by a reviewer seat, or a host cell not matching the frozen capture |
| C2 | operability | The census `--selftest` gains a namespace-honesty case class: run the STORAGE arm inside a private `unshare -rm` namespace — bind-mount a btrfs-backed dir so the namespace's `/proc/self/mounts` lists a btrfs line, then hide `/sys/fs/btrfs` (tmpfs) and expect `state=BLOCKED … detail=mounts:btrfs-without-sysfs`; inject nonzero `error_stats` under a masked sysfs root and expect DEGRADED. This exercises the production path (no `TSUKUROI_PROC_MOUNTS` override) against the view the round-39 "remaining limit" (`PROVINCE.md:234-236`) named, closing the "behaves honestly only there" trap for every constructible view | `python3 tools/score-storage-namespace-r42.py --revision <REV> --scratch <DIR>` (frozen; sha256 TBD): exports the census at <REV> into a scratch clone, runs the two namespace cases, checks the verdicts | no such case exists (grep `unshare` in `tools/tsukuroi-census.sh` has 0 hits), `ns_blocked 0, ns_degraded 0`, FAIL exit 1 | `ns_blocked == 1 and ns_degraded == 1 and selftest_pass == 1`, PASS exit 0 | the arm reads the override seam inside the namespace, or reports HEALTHY with a hidden sysfs root and a listed btrfs mount |

Controls, scored with the frozen counters before any seat (run_controls.py): per claim, do-nothing base, X-empty
(rule cells `RULE NOT SUPPLIED`), X-false (negation / wrong values), scripted writer (quote copied as rule plus
every frozen token) — each must FAIL, only the candidate PASSes.

Causal separability: C1 touches the storage-health entry and `corpus/SOURCES.md`; C2 touches only the census
`run_selftest`; neither counter reads the other's surface. No-harm: all six axes re-checked at the tip
(registry-coverage, knowledge-header, adjacency-anchors, section-citations, appended-notices, boot-writers,
recheck-commands, self-assessment gates PASS). Measured revision: the lane branch tip named in the round-42
outcome section, declared before the after-run.
```

Notes on the draft:
- **C1's surface is the storage-integrity frontier (F4), not Core**: it deepens `storage-health-r26.md` without
  claiming the round-26 Core-promotion condition (a census arm reading it) is met. It opens the two leads the
  round-26 correction explicitly left unopened (`corpus/README.md:246-248`; `corpus/SOURCES.md:338`). It is
  do-nothing-proof: the rows and new registry rows do not exist at base. It mirrors the round-41 C2 protocol
  (frozen source window + per-row reviewer verdict files), so the lane's own read discipline is reused.
- **C2 is the first claim that addresses F5 directly**: feasibility was probed read-only — inside
  `unshare -rm`, a bind-mount of a btrfs-backed dir appears in the namespace's `/proc/self/mounts` (5 btrfs
  lines) and a tmpfs over `/sys/fs/btrfs` hides the sysfs root (0 entries), both exit 0 (probe receipt). This is
  the only "injection" the lane allows (private namespace; no host mutation), and it exercises the real
  `/proc/self/mounts` path rather than the `TSUKUROI_PROC_MOUNTS` override seam.
- The scrub-record **census arm** (Frontier→Core for the unprivileged timer/status-dir subset, per the written
  promotion condition `PROVINCE.md:212-214`) was considered for C2 and is the strong alternative; it is heavier
  (production probe change, permission unknowns on a populated `/var/lib/btrfs`) and still needs a later round to
  admit the promotion, so the namespace-honesty claim is proposed first. It can be a round-43 C1 if round 42
  confirms the status-dir read's permissions.
- A third claim on freshness (re-running `tools/boot-chain-audit.sh --live` for the F3 `/new_root` watch item)
  was considered and dropped: the tool already exists, so the claim would be a recheck rather than a move, and
  the do-nothing control's failure would be procedural, not substantive.

## 6. What I did not do

- I did not run the C1/C2 counters or the census (planning seat; only reads).
- I did not read sibling lane files (only the citations inside lane files and the peer roster).
- Round-41 measured outcome and non-author closure do not exist yet; verdicts here are against the declaration.
- No tools were installed or upgraded; no host mutation (probes were read-only; the `unshare -rm` test exited
  with its namespace).
