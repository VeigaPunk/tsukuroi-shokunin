# tsukuroi-shokunin — Province

**Domain:** host operability & system repair (繕, mending) — the OS
substrate itself: package state, systemd, drivers/firmware, boot health.

## Core

**Owns (surfaces, all read-only probes):** pacman state (`pacman -Qkk`
verify loops, foreign/AUR census, `.pkg.tar.zst` receipt discipline),
systemd user units & timers (`systemctl --user`, unit files, failed
states), journal/boot triage (`journalctl -b`, dmesg error classes),
driver/firmware plane (kernel modules, nvidia driver + GSP firmware
presence, `nvidia-smi` shape). Update-safety questions: what an -Syu
would touch, what pins/holds exist.

**Additional owned surfaces, documented in fleet round 1 (all read-only):**

| Surface | Boundary | Corpus entry |
|---|---|---|
| `Arch News` upgrade gate | Match official notices to local package/config evidence; a public feed read is not host state, and upgrade actions remain operator-owned. | `corpus/knowledge/arch-news-gate-2026.md` |
| `.pacnew` / `.pacsave` drift | Pair pacman-log history with current readable filesystem findings; report skipped unreadable paths. | `corpus/knowledge/pacnew-plane.md` |
| Initramfs v42 and boot recovery | Inspect effective mkinitcpio drop-ins, hooks and recovery stages; never rebuild or boot. | `corpus/knowledge/initramfs-v42-sysroot-recovery.md` |
| Snapper/rollback net | Diagnose filesystem mode and unit capability restrictions; report mechanism/falsifier, never attempt restore/config changes. | `corpus/knowledge/snapper-eacces-mechanism.md` |

**Refuses:** endpoint/model serving health (→ kama), secrets (→ kagi),
binary RE of drivers (→ kaidoku/revenger — tsukuroi tracks *state and
health*, not internals). Never installs, upgrades, or removes packages;
never restarts services. Detection and report; the operator remediates.

Host memory and kill-event measurements support OS triage; they do not
establish which fleet wave caused pressure or whether an endpoint works.
The existing census reports those signals; fleet correlation belongs to mori
(`../mori-shokunin/PROVINCE.md:6-16`).

## Adjacent — finding-to-owner handoffs

This table classifies seven shared-work classes, not every possible host
failure. A recipient is an analysis/report owner, **not permission to repair**.
Tsukuroi retains the OS finding. No row authorizes configuration writes,
service changes, credential reads, endpoint requests, or target execution.
Shared evidence is not shared ownership; unresolved ownership goes to the
protocol integrator, never to whichever lane answered first.

| ID | Finding / boundary trigger | Tsukuroi retains | Next analysis recipient | Minimum handoff evidence | Ownership source |
|---|---|---|---|---|---|
| ADJ-01 | A local model endpoint or served-model identity is wrong; GPU readiness alone cannot decide this | Kernel, driver, device and user-unit state | kama | Capture time; driver query and unit-state command/exit; reported endpoint symptom without credentials. Kama must obtain its own endpoint evidence; no endpoint diagnosis from `nvidia-smi` | `OUT-002` |
| ADJ-02 | A credential-bearing helper has a permission/ownership finding or an auth-flow question | Package owner/version and filesystem mode; package drift is not proof of credential exposure | kagi | Path, mode, uid/gid, package owner/version, command/exit and capture time only; no secret values, vault references, session bytes or helper invocation | `OUT-003` |
| ADJ-03 | Desktop rendering, bindings, menu or idle behavior needs configuration-level diagnosis | User-manager/unit, package and driver health; an active unit does not prove the UI works | mado | Observed UI symptom and time plus relevant OS probe/exit; identify configuration surface without copying its contents. Mado verifies file/screenshot behavior itself | `OUT-004` |
| ADJ-04 | Host pressure or a kill signal needs fleet/wave attribution, liveness or progress correlation | OS memory, journal and boot diagnosis; cumulative counters are not dated incidents | mori | Capture time, boot/window, exact counter or PSI command/exit and observed value; distinguish presence, cumulative count and dated event. Request correlation, not a claim that a wave caused OOM | `OUT-005` |
| ADJ-05 | Task/hub dispatch, routing or orchestration semantics are wrong, rather than merely a failed host unit | systemd and resource evidence; unit liveness cannot prove dispatch correctness | kumitate | Minimal reported dispatch symptom, task/wave identifier if non-sensitive, capture time and OS probe/exit; exclude tokens, environment and raw process arguments | `OUT-006`, `OUT-007` |
| ADJ-06 | Driver/firmware/package mechanism requires shipped-artifact reverse engineering beyond health inventory | Loaded version, package provenance and driver/boot symptoms; no binary-internals inference | protocol integrator — kaidoku/revenger ownership unresolved | Exact question, authorized artifact identity/path and digest when safely obtainable, capture time and relevant OS evidence. Request an ownership ruling before any RE work; do not invoke a target or forward raw cores | `OUT-008`, `OUT-009` |
| ADJ-07 | A census blind spot raises a reusable verification/mutation-testing question | Census bug, domain contract, implementation and repair in this repo | tameshi | Minimal failing behavior, command/exit, measured census revision and expected domain invariant; ask for method advice, not transfer of gate ownership or a general claim from one lane | `OUT-010` |

### Handoff checklist

1. Record the trigger, UTC capture time, boot/time window where relevant,
   exact read-only command, exit code and observed value. Mark inference
   and unknowns separately; do not infer a fresh kill from a cumulative counter.
2. Select the matching row by the **question being asked**, not the binary or
   service name. Split mixed questions: keep OS diagnosis here; name only the
   requested sibling analysis. If no row fits, report to the integrator.
3. Prepare a sanitized evidence packet using that row's minimum fields.
   Report it in the fleet lane report, including the recipient and remaining
   operator action. Never copy credentials, raw configs, raw cores or argv.
4. Track closure states separately: `prepared`, `reported`, `acknowledged`,
   `accepted`, `resolved`. Acknowledgement is not acceptance; resolution
   requires owner-side closure evidence. A missing substrate or disputed
   owner is an explicit limit, not a successful downstream handoff.

Sources were read on 2026-10-15; sibling declarations can drift. Source
fingerprints and an executed host-to-mori packet are in
`corpus/knowledge/adjacency-handoffs-fleet-r1.md`. Re-read the cited declaration
before a later handoff; the table does not freeze another lane's authority.

## Frontier

- Recipient acknowledgement and independently replayed handoffs are not
  verified. The round's author-side replay is not promotion evidence.
- Kaidoku and revenger both declare shipped-artifact RE. The integrator must
  arbitrate this shared scope; tsukuroi neither picks an owner nor absorbs it.

**Out of province → report, never absorb.**
Source re-check 2026-10-19T22:57:14Z (fleet round 1): committed sibling HEAD pins match the original 1/8 (mado); 7/8 drift. Re-reading the cited source ranges at those clean HEADs still finds all 8/8 route anchors in-range. The committed-kaika receipt sweep found one recipient-side packet response in mori; acceptance/resolution are not inferred. See `corpus/knowledge/adjacency-recheck-2026-10-19.md` for the pin table, receipt scope and exact evidence.

Round-12 refinement: root-directory metadata and create-failure DAC/ACL,
mount/namespace and configured-credential discrimination remain within the
existing host/rollback-net surface. The census owns detection only; no mode
repair, service restart, subvolume creation, boot or package transaction is
authorized by a finding. `corpus/knowledge/root-dac-decision-r12.md` refines
this existing core surface without absorbing sibling verification methods.

Round-13 correction R13-DAC-EXCLUSIVITY: the active refinement is now
`corpus/knowledge/root-dac-correction-r13.md` and `.json`; the round-12
entry is retained with an explicit supersession notice after outside
rejection. This remains the same host/rollback-net surface and grants
no namespace mutation, privileged inspection or sibling-method ownership.

Round-14 source-scope erratum: R14-VALUE-DOMAIN and R14-COMMENT-ATTRIBUTION
(`corpus/knowledge/source-scope-correction-r14.md`/`.json`) supersede two
round-13 loci only — the ProtectSystem “value set is not exhaustive” cell
(`ProtectSystem=` is documented as a boolean argument or the special values
`full` or `strict`; mechanism non-exhaustiveness is separate, S044) and the
#8047 “self-described model-generated triage” attribution (verified account
fields only; VM execution unverified; second opinion and maintainer deferral
stand; #6629's disclaimer is not transferred, S045). Round-13 namespace
guidance remains active; no new surface, capability or host cause is claimed.

## Adjacent — portable ownership anchors (round 19)

Append-only. The line-range table under `## Adjacent — finding-to-owner handoffs`
(ADJ-01..ADJ-07) and the Core pointer retained above are not changed. Each row
below cites its ownership text by anchor id, exact heading and exact quote from
the pinned sibling snapshot, never by line number; OUT-001 is the Core pointer
(ADJ row shown as Core). The pinned commit and blob sha256 identify the bytes,
so an anchor is valid only for those bytes. Inbound classification and
owner-handoff packets are in `corpus/knowledge/adjacency-anchors-r19.md`. This
section grants no authority and is an ownership locator, not a repair mandate.

| Anchor | ADJ row | Sibling file @ commit | Heading | Quote | Proposition |
|---|---|---|---|---|---|
| OUT-001 | Core | `mori-shokunin/PROVINCE.md` @ `91940fa339e3` | `# mori-shokunin — Province` | `fabricated quote that exists in no sibling file` | Mori owns kill/OOM and cgroup memory evidence; fleet correlation of host pressure is mori's, not OS triage. |
| OUT-002 | ADJ-01 | `kama-shokunin/PROVINCE.md` @ `e75cf680b534` | `# kama-shokunin — Province` | `GET /v1/models` vs `--alias` vs the configured model id | Kama owns served-model identity reconciliation; an endpoint or served-model mismatch is kama's analysis, not a driver/GPU-readiness finding. |
| OUT-003 | ADJ-02 | `kagi-shokunin/PROVINCE.md` @ `c2cab35bc92e` | `# kagi-shokunin — Province` | **Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence | Kagi owns secrets and vault operations, the-janitor credential flows, and credential-hygiene evidence. |
| OUT-004 | ADJ-03 | `mado-shokunin/PROVINCE.md` @ `a4046a821608` | `# mado-shokunin — Province` | **Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules, | Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and screen/idle behavior. |
| OUT-005 | ADJ-04 | `mori-shokunin/PROVINCE.md` @ `91940fa339e3` | `# mori-shokunin — Province` | kill/OOM-related catalog-ID records and signal-11 coredump records | Mori owns kill/OOM catalog-ID and signal-11 coredump classification from separately labeled user/system journals; fleet attribution is its correlation, not tsukuroi's. |
| OUT-006 | ADJ-05 | `kumitate-shokunin/PROVINCE.md` @ `1770305fae20` | `# kumitate-shokunin — Province` | **Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime | Kumitate scopes OMP task/hub and orchestration tooling, so task/hub dispatch and routing semantics are its analysis, not tsukuroi's. |
| OUT-007 | ADJ-05 | `mori-shokunin/PROVINCE.md` @ `91940fa339e3` | `# mori-shokunin — Province` | **Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package, | Mori refuses dispatch and orchestration mechanism and routes it to kumitate, supporting ADJ-05's kumitate recipient. |
| OUT-008 | ADJ-06 | `kaidoku-shokunin/PROVINCE.md` @ `d1d981d2cc04` | `# kaidoku-shokunin — Province` | **Domain:** reverse engineering of shipped artifacts with REA on this Linux | Kaidoku declares shipped-artifact reverse engineering with REA as its domain, the scope ADJ-06 would hand to an RE owner. |
| OUT-009 | ADJ-06 | `revenger-shokunin/PROVINCE.md` @ `cf02419276e5` | `# revenger province` | Owns: reverse engineering of shipped artifacts | Revenger owns shipped-artifact reverse engineering (binaries, packages, APKs) with an observation/inference/unknown evidence ledger; tsukuroi tracks state only. |
| OUT-010 | ADJ-07 | `tameshi-shokunin/PROVINCE.md` @ `01d586ddbc5f` | `# tameshi-shokunin — Province` | **Owns:** the method, documented from the fleet's existing gates | Tameshi owns the reusable verification/mutation-testing method, applied to fleet gates as read-only primary surfaces; each lane keeps its own gate. |

Limits (round-19 first falsifiers CritAdjBoundary/CritAdjVacuity): the quoted words are the sibling's, attributed to it, never a tsukuroi assertion of sibling authority; the pins are stale by design once a sibling commits again, so re-read the live declaration before any later handoff (the paragraph above `## Frontier` still governs). Every heading above is the sibling file's title heading because the cited ownership text sits in its preamble. Recheck: `python3 tools/check-adjacency-anchors.py --revision <REV>`.

Portable digests (appended 2026-10-21, round-19 falsify repair). Each anchor's full pinned
commit and blob sha256, so the locator is portable without the table's abbreviated commit:

- OUT-001 `mori-shokunin/PROVINCE.md` @ 91940fa339e38006f8db5bd7d78bb6f037f4d016 sha256 73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130
- OUT-002 `kama-shokunin/PROVINCE.md` @ e75cf680b53484a61709ee1b2787d8dbc6419f74 sha256 799432d748bd40bcf859de806cc2ef90df069da14c8e5c07bf72250ac411c7a6
- OUT-003 `kagi-shokunin/PROVINCE.md` @ c2cab35bc92e57e39e5489bac3386db078345b3f sha256 4a346e2df81f7b2e649914d0d99da974d6c484caf12fed1c6bd530d106a78523
- OUT-004 `mado-shokunin/PROVINCE.md` @ a4046a8216080d4004de3f268c62cf142095ac07 sha256 1b25bb1e980925b356663602d002c1c15307a0dfac8bfafd9988bd4d8df7464b
- OUT-005 `mori-shokunin/PROVINCE.md` @ 91940fa339e38006f8db5bd7d78bb6f037f4d016 sha256 73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130
- OUT-006 `kumitate-shokunin/PROVINCE.md` @ 1770305fae20826b39905a8251ddeca6b4957ac4 sha256 fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f
- OUT-007 `mori-shokunin/PROVINCE.md` @ 91940fa339e38006f8db5bd7d78bb6f037f4d016 sha256 73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130
- OUT-008 `kaidoku-shokunin/PROVINCE.md` @ d1d981d2cc041dda4656c5b01d2c8445d8d17124 sha256 63920930b77f9604c6ff7f5db8859344ef97fa50de9e4d0028897da4288859ac
- OUT-009 `revenger-shokunin/PROVINCE.md` @ cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97 sha256 63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f
- OUT-010 `tameshi-shokunin/PROVINCE.md` @ 01d586ddbc5fcd78659557c4e93a6ee8517b87d1 sha256 8006da5db27d2188ff2f3fc20ae402d0d30c7b5c5fcf9ca26c6793d2ff7e080f

## R20 ownership clarification — OUT-009

R20-OUT009: OUT-009 is Revenger's sibling declaration of reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, browser/Electron runtime evidence. It is not a tsukuroi grant of ownership. Kaidoku/Revenger arbitration remains unresolved; ask the protocol integrator before an internals handoff. No configuration, service, package, boot or sibling-file write is authorized.

This explicitly supersedes only the OUT-009 proposition's unqualified “Revenger owns” wording and its broad “packages” paraphrase. The original quoted declaration and pinned bytes remain historical evidence; “Electron/JavaScript packages” is the precise package scope, not arbitrary packages. ADJ-06's unresolved recipient and Frontier arbitration remain controlling. The other nine locators and all prepared/acknowledged handoff states are unchanged. Source: the pinned Revenger snapshot in `corpus/knowledge/adjacency-anchors-r19.json`; recheck: `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`.

## Round-26 frontier — storage integrity

**Round-26 frontier: storage integrity.** Btrfs device error counters, scrub
records and NVMe health enter this province as a frontier area of the OS
substrate. The lane reads the five per-device btrfs error counters (write,
read, flush, corruption, generation) as the filesystem exposes them in its
sysfs `error_stats` file and as the `btrfs device stats` query reports them;
it reads the scrub record the filesystem keeps (`btrfs scrub status` and the
shipped `btrfs-scrub@.timer` unit), and it reads the NVMe SMART/Health
lifetime fields (`smartctl -H -A`, `nvme smart-log`). Detection and report
only: the same boundary that governs the Core surfaces above applies here.
What stays out of the province — disk-space runway and free-capacity
reporting remain mori's (`../mori-shokunin/PROVINCE.md:26`, the `SURFACE disk`
row with its default `df -P` targets), and filesystem repair, running a
scrub, resetting an error counter and firmware updates remain operator-owned.
This area becomes Core only after a census arm exists; until then it is
Frontier and the knowledge entry is the record of the reading
(`corpus/knowledge/storage-health-r26.md`, rows SH1 to SH6; gate
`python3 tools/check-storage-health.py --revision <REV>`, field
`verified_rows`). No package, service, mount, scrub, counter-reset,
firmware or configuration action is authorized by this paragraph.

Round-26 frontier correction after wave 2 (appended 2026-10-22, RevProvinceReadme): "disk-space runway and free-capacity reporting remain mori's" overstates the split. Mori's disk surface covers the fleet root and `/tmp` (`../mori-shokunin/PROVINCE.md`, SURFACE disk); this lane already reports `/` and `/boot` free space for update safety (`SKILL.md` update-safety checklist, `corpus/knowledge/update-safety-note.md`). The split is by question: free space as fleet runway is mori's, free space as an upgrade or boot precondition is this lane's. The storage-integrity reads need privilege for SMART and the scrub status ioctl (`sudo -n`, read-only allow-list) and cover only the root's backing NVMe device; the second NVMe device (`/tmp`, `/fast`) is unread. The frontier becomes core when a committed read-only census plane reads these signals with a hermetic selftest and a registry row, and a later round admits it; until then the entry is the record.

## Adjacent — mori userspace OOM killers (round 27)

Overlap register against mori's admitted entry `corpus/knowledge/userspace-oom-killers-r26.md` at mori commit `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` (committed snapshot under `.ufo/waves/round-27/siblings/mori/`, sha256 `a5368ee7…0b29d`). Rows are reported, never absorbed: earlyoom behaviour and killer accounting are mori's; host unit state and the systemd-oomd reading in `memory-pressure-r25.md` are tsukuroi's. Full anchors and actions: `corpus/knowledge/adjacency-mori-oom-r27.json` and `.md`. A sibling citing this lane is not a recipient acknowledgement; the frontier bullet on acknowledgement stays open.

| id | owner | class | pointer |
|---|---|---|---|
| OV1 | tsukuroi | INBOUND-RESOLVES | mori F8 unit list → `memory-pressure-r25.md` lines 204-206, same at 157ee255 and the tip |
| OV2 | mori | INBOUND-DRIFTED | mori `PROVINCE.md:66` → lane PROVINCE lines now 30-33 and 44-53; mori re-pins |
| OV3 | tsukuroi | AGREES | meaning of `auto` (lane lines 201-202) |
| OV4 | tsukuroi | CONFLICTS | mori F8 drops the lane's OOMRules= qualifier (lane lines 387-390); reported to mori |
| OV5 | mori | CONFLICTS | lane line 382 relies on an earlyoom option mori's F7 says 1.9.0 lacks; lane notice points at mori |
| OV6 | mori | LANE-GAP | systemd-oomd cgroup accounting attributes; not absorbed |

## Adjacent — ADJ-04 handoff lines in the census (round 32)

Append-only; the ADJ-01 to ADJ-07 table above is unchanged. From round 32 the census prints a `HANDOFF ADJ-04 mori …` line for each of two evidence classes that ADJ-04 and OUT-005 route to mori: dated kill-event clusters in the oom plane's retained window, and boot-0 systemd-coredump entries (`SKILL.md` rows R32-H1 and R32-H2). The line carries `state=prepared`: the census prepared a packet line; it is not reported, acknowledged, accepted or resolved, and mori declares no intake format for it (mori `PROVINCE.md` at `a45850f0`, read by round-32 ScoutMoriHead). Tsukuroi keeps the OS finding on its journal and oom planes. Mori's own counts of the same events use MESSAGE_ID per journal scope; the census counts by message text and SYSLOG_IDENTIFIER over the merged journals, so the two values can differ (round-32 ConnSiblingOverlap finding 4). Recheck: `python3 tools/score-census-handoff-r32.py --revision <REV>`. No sibling file is written and no repair is authorized.

## Adjacent — ADJ-04 per-class boundary note (round 33, exploratory)

Append-only; the ADJ-01 to ADJ-07 table and the round-32 handoff section above are unchanged. The seven kill and OOM evidence classes of `SKILL.md:1097-1107` are examined one by one against ADJ-04 and against mori's own declared scope at mori `24603186b555dddb88ebd607e415e27bdea747b4` in `corpus/knowledge/kill-oom-boundary-r33.md`: per class, what this lane retains, what ADJ-04 routes, and what mori declares (or `none declared`, with the grep that found nothing). It records boundaries; it adds no route, no intake and no new trigger.

## Round-38 promotion — R38-STORAGE-CORE: the btrfs error counters move Frontier → Core

Append-only; the round-26 frontier section and its wave-2 correction stay as written. The condition that
section set — "This area becomes Core only after a census arm exists" — is met for the per-device
error-counter reading only.

**Core now:** reading the five per-device counters (`write_errs`, `read_errs`, `flush_errs`,
`corruption_errs`, `generation_errs`) from `/sys/fs/btrfs/<fsid>/devinfo/<devid>/error_stats`, reported on
the census's verdict-neutral `STORAGE btrfs-device-stats ...` line (`probe_storage_arm` in
`tools/tsukuroi-census.sh`; `SKILL.md` "Storage integrity arm — round 38"). Unprivileged (sysfs 0444),
resets nothing, never enters `TSUKUROI_CENSUS`. A nonzero value is a stored lifetime total, not a dated
event (SH2, `corpus/knowledge/storage-health-r26.md`).

**Still Frontier:** the scrub record (`btrfs scrub status`, `/var/lib/btrfs/scrub.status.*`,
`btrfs-scrub@.timer`; SH3/SH4) and NVMe SMART/Health (`smartctl -H -A`, `nvme smart-log`; SH5/SH6) — no census
arm reads them. The second NVMe device (xfs on `/tmp`, `/fast`) has no btrfs counters and stays unread.
**Operator-owned:** running a scrub, enabling its timer, resetting a counter (`btrfs device stats -z`),
profile changes, firmware, LUKS and any repair. **Mori's:** disk-space runway as fleet capacity, under
the round-26 wave-2 split. **Known limit:** an absent sysfs root reads `HEALTHY 0/0/0`, so a namespace
hiding `/sys/fs/btrfs` gives a false all-clear (wave-1 C1CritAbsentRoot); next-round work.

Counted by `python3 tools/score-storage-arm-r38.py --revision <REV>` together with
`python3 tools/score-storage-arm-r38-q82.py --revision <REV>` at the round-38 measured revision
(`SCORECARD.md` "Round 38 — measured outcome"). No package, service, mount, scrub, counter-reset,
firmware or configuration action is authorized by this section.

## Round-39 limit closure — R38-ABSENT-ROOT: an absent or empty btrfs sysfs root is not a clean disk

Append-only; the round-38 promotion section above stays as written, and its **Known limit** sentence is
superseded here, not deleted. Since round-39 C1 (`tools/tsukuroi-census.sh` `probe_storage_arm`, commit
`49cc53c7`), a sysfs root that is absent or holds no fsid entry reads `HEALTHY 0/0/0` only when the mount table
(`/proc/self/mounts`, override `TSUKUROI_PROC_MOUNTS`) lists no btrfs mount; with a btrfs mount listed the STORAGE
line is `BLOCKED … detail=mounts:btrfs-without-sysfs`, and an unreadable table is `BLOCKED … detail=mounts:unreadable`.
The STORAGE line stays verdict-neutral. **Core now** additionally holds that one read of the mount table; the
mount table itself (what is mounted where, mount options, namespaces) is read for this guard only and is not a
new owned surface. **Still Frontier, unchanged:** the scrub record and NVMe SMART. **Remaining limit:** a census
that detects the counter's namespace and behaves honestly only there cannot be told apart on this host, whose
live answer is constant (`HEALTHY 1/1/0`); no host-side injection is authorized (read-only lane). Counted by
`python3 tools/score-storage-hidden-r39.py --revision <REV>` (`SCORECARD.md` "Round 39 — declaration").

**Round-42 note — scrub record read from source (appended 2026-10-26).** The scrub record stays Frontier. Round 42
read what the record is from btrfs-progs v7.1 `cmds/scrub.c` (`corpus/knowledge/btrfs-scrub-record-r42.md` SC1-SC5:
its `_tmp`-then-rename write under `flock`, the `scrub status:1` line format, that only the userspace start process
writes it and when recording is switched off, how status folds device lines, the per-device `scrub_speed_max` limit).
The promotion condition (a read-only census arm) is unchanged; `btrfs scrub status /` reads the record unprivileged on
this host (wave-1 `C2ExecHostRecheck`), so an arm needs no privilege for the record itself.

**Round-43 note — scrub record re-grounded; correction to the round-42 note (appended 2026-10-26).** The scrub record
stays Frontier. Round 43 re-grounds the withdrawn SC1/SC3 of `corpus/knowledge/btrfs-scrub-record-r42.md` as SR1/SR3
and the running-state limit as SR6 in `corpus/knowledge/btrfs-scrub-record-r43.md`. The round-42 note's last
sentence overreaches (wave-1 `ConsiderMap` F-6/d): this host has no record, so `btrfs scrub status /` showed only the
no-record path (`no stats available`, S241 capture line 10); a present record is created with open mode argument
0600 and every open takes `flock(LOCK_EX|LOCK_NB)` (SR1), so a user-level arm can see the directory, stat the file
and read `scrub_speed_max`, but cannot be assumed to parse the record [inference: a record written by a root scrub
under the usual umask is root-only], and it cannot read the running state at all (SR6: `BTRFS_IOC_SCRUB_PROGRESS`
returns `EPERM` without `CAP_SYS_ADMIN`). The promotion condition (a read-only census arm) is unchanged.

## Round-44 promotion — R44-SCRUB-VIEW: the unprivileged scrub-record view moves Frontier → Core

Append-only; the round-38 promotion, the round-39 limit closure and the round-42 and round-43 notes above stay as
written. The condition those sections set — "it becomes Core only after a read-only census arm reads it"
(`corpus/README.md:243`) — is met for the part of the scrub record an unprivileged reader can see.

**Core now:** the census's verdict-neutral `SCRUB btrfs-scrub-record state=NONE|RECORDED|BLOCKED
dir=absent|present|unreadable records=N tmp=N sockets=N unreadable=N orphan=N limited=N timers=N [detail=...]`
line (`probe_scrub_record` in `tools/tsukuroi-census.sh`, printed after the `STORAGE` line and before
`TSUKUROI_CENSUS`; contract in that file's header paragraph "Round-44 addition (C1)"). It reads the record
directory by name and stat only: the record `scrub.status.<fsid>`, its `_tmp` staging file and the
`scrub.progress.<fsid>` socket under `/var/lib/btrfs` (override `TSUKUROI_SCRUB_DIR`), with an `unreadable` count
and an `orphan` count (a record whose fsid has no entry under `/sys/fs/btrfs`, so that filesystem is not mounted
now); each fsid's `devinfo/<devid>/scrub_speed_max` (a nonzero decimal is a limit and is listed in `detail`; SR8);
and the enabled instances `btrfs-scrub@<instance>.timer` under `/etc/systemd/system/timers.target.wants` (override
`TSUKUROI_TIMER_WANTS`; the bare template name is not an instance and is not counted; SR9). The arm reads no
record content, makes no ioctl, calls neither `btrfs` nor `systemctl`, needs no privilege and creates no file; the
line is never a rollup term and never an exit-code input.

**Still Frontier:** the record's content — a root-written record is mode 0600 and every open takes
`flock(LOCK_EX|LOCK_NB)` (SR1, round-43 note above), so the arm counts and stats it rather than parsing it; the
running state — `BTRFS_IOC_SCRUB_PROGRESS` needs `CAP_SYS_ADMIN` (SR6) and returns 0 only while `dev->scrub_ctx`
is attached, `-ENOTCONN` for an idle device (SR7), so a leftover progress socket is counted as `sockets=N` and is
not the running state; and NVMe SMART/Health (`smartctl -H -A`, `nvme smart-log`; SH5/SH6). The second NVMe device
(xfs on `/tmp`, `/fast`) still has no btrfs counters and stays unread.
**Operator-owned:** running, canceling, resuming or limiting a scrub, enabling its timer, resetting the error
counters (`btrfs device stats -z`), profile changes, firmware, LUKS and any repair. **Mori's, unchanged:**
disk-space runway as fleet capacity, under the round-26 wave-2 split. **Known limit:** an absent sysfs root with no
record reads `limited=0`, and the `STORAGE` line's mount-table guard is what flags a hidden sysfs
(`corpus/README.md:315`); a record's readability is counted, never its content; and the arm's namespace legs leave
the mount-table, `uid_map` and script-path channels open (QUALITY 90 "named open"; control C1-K7), while this host's
live answer is constant (`NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`),
so a census that behaves honestly only there cannot be told apart here; no host-side injection is authorized.

Counted by `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR>` (frozen; sha256
`1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388`; predicate `cases == 16 and correct == 16 and
identity_ok == 1 and wired_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r44 >= 6`) at the
round-44 measured revision (`SCORECARD.md` "Round 44 — measured outcome"). The census selftest reports 148 cases,
sixteen of them labelled `(R44-C1)`. No package, service, mount, scrub, timer, counter-reset, firmware or
configuration action is authorized by this section.

## Round 49 — the ownership-source column now cites portable anchors

Append-only note, 2026-10-28. The seven rows of `## Adjacent — finding-to-owner handoffs`
carried bare sibling line ranges in their **Ownership source** cell
(`../kama-shokunin/PROVINCE.md:3-24`, `../kagi-shokunin/PROVINCE.md:3-6,10-17,32-34,54`,
`../mado-shokunin/PROVINCE.md:3-16`, `../mori-shokunin/PROVINCE.md:3-16`,
`../kumitate-shokunin/PROVINCE.md:3-6` + `../mori-shokunin/PROVINCE.md:12-16`,
`../kaidoku-shokunin/PROVINCE.md:3-6,88-100` + `../revenger-shokunin/PROVINCE.md:3-7,19-25`,
`../tameshi-shokunin/PROVINCE.md:3-18`). That is the locator class QUALITY 32 / R19-ADJ-POINTERS
rules out: a line range is not a locator, and a quote that moved must resolve by quote plus pinned
blob. Each cell now names the `OUT-0NN` anchor of `## Adjacent — portable ownership anchors (round
19)` whose own **ADJ row** cell names that finding class (ADJ-01 → OUT-002, ADJ-02 → OUT-003,
ADJ-03 → OUT-004, ADJ-04 → OUT-005, ADJ-05 → OUT-006 and OUT-007, ADJ-06 → OUT-008 and OUT-009,
ADJ-07 → OUT-010). The old ranges are preserved only in this note; the anchor rows carry the pinned
sibling commit, exact heading, ≤25-word quote and the registry blob sha256, so the ownership pointer
now resolves by content. The round-19 rule "the line-range table is not changed" is superseded for
this column only; the finding classes, retains, recipients and handoff evidence are unchanged.
Nothing here grants write authority, and the kaidoku/revenger ownership arbitration stays open
(ADJ-06, integrator's call).

Counted by `python3 tools/check-adjacency-table-r49.py --revision <REV>` (predicate
`adj_rows == 7 and linked_rows == 7 and bare_ranges == 0 and anchors_ok == 7 and registry_ok == 7
and anchors_checker_rc == 0`; the existing `tools/check-adjacency-anchors.py` still re-checks the
anchors against the live sibling bytes).
