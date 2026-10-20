source: own-work row S069 — pointer census `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json` (schema tsukuroi-adjacency-pointers-r19-v1; lane_tip 452a054677f6b18284917d7c08c45361f91c25ac; counts inbound 114, outbound 10); (S069 also covers) the sibling `PROVINCE.md` snapshots `.ufo/waves/round-19/l1-capture/siblings/<lane>/<commit12>/PROVINCE.md` for kama/e75cf680b534, kagi/c2cab35bc92e, mado/a4046a821608, mori/91940fa339e3, kumitate/1770305fae20, kaidoku/d1d981d2cc04, revenger/cf02419276e5, tameshi/01d586ddbc5f; lane `PROVINCE.md` ADJ-01..07 table (lines 35-52) and handoff checklist (lines 54-68).
verified-at: 2026-10-20 lane 452a054 (census v2: v1 bytes plus four en-dash range corrections, IN-073..IN-076, re-extracted at the v1-pinned tips; v1 retained at `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.v1.json`)
recheck: 30d; procedure: `python3 tools/check-adjacency-anchors.py --revision <REV>`, where `<REV>` is a landed lane commit resolved under corpus/QUALITY.md criterion 27; re-read each sibling declaration before any later handoff.

# Adjacency anchors — round 19

## 1. Scope and counted claims

Two directions, one gate. Outbound: the ten sibling ownership pointers in
`PROVINCE.md` (line-range only) gain portable anchors: exact heading, exact
quote of at most 25 words, pinned sibling commit and blob sha256. Inbound: the
114 sibling-file pointers into tsukuroi files in the census are classified
RESOLVES, DRIFTED or UNRESOLVABLE against the current lane tip.

Counted sets, named so each count can be re-derived (corpus/QUALITY.md
criterion 30):

- outbound_portable 0 → 10 counts exactly census `outbound[]` records OUT-001..OUT-010.
- inbound_classified 0 → 114 counts exactly census `inbound[]` records IN-001..IN-114: line-numbered, repo-prefixed pointers in committed sibling tips (ReviewCensusExtract: line-less, `@rev`-qualified and bare-name citations are outside this census and not counted). 89 of them are dated `.ufo/` records; the operative subset is 25.

A count is a count of records that pass the gate. It is not a semantic proof
that each sibling sentence is correct.

## 2. Method

Outbound (per OUT record):

1. Open the snapshot path named by the census record.
2. Find the Markdown heading whose section holds the cited ownership text.
3. Choose an exact single-line quote of at most 25 words inside that section.
4. Record the 1-based snapshot line of the quote.
5. Confirm that the census `sibling_commit` and `sibling_blob_sha256` match the snapshot bytes.
6. Record whether the quote lies inside the cited range.

The heading plus quote is the locator. Line numbers are supplementary and are
valid only against the named snapshot.

Inbound (per IN record):

1. Read the current lane file at the record's `target_path`.
2. Locate the content the sibling sentence relies on by an exact quote.
3. Classify RESOLVES if `found_line` falls inside the record's target ranges.
4. Classify DRIFTED if the content exists at another line.
5. Classify UNRESOLVABLE if the content is absent. State the bounded search, for example `grep -nF '<quote>' <target_path>`, and its result.
6. Set `scope` to `operative` when `sibling_path` does not start with `.ufo/`, otherwise `historical`.

## 3. Scope limits

- Classification is relative to the current lane tip 452a054, not to the revision the sibling cited. A RESOLVES result says nothing about the sibling's pinned view of tsukuroi.
- Historical pointers (`sibling_path` under `.ufo/`) are dated records. They are classified and retained. They never become owner handoffs.
- Only operative DRIFTED or UNRESOLVABLE rows become owner handoffs (§4).
- Tsukuroi never edits sibling files. Siblings are read-only. A handoff is a report to the owner.
- A pointer is not proof of ownership. The cited text supplies ownership; a digest match is drift evidence only (as in `adjacency-handoffs-fleet-r1.md`).
- This entry is repository evidence only. It runs no host probe and no package, boot, service or configuration action.

## 4. Owner-handoff packet format

Each operative drift becomes one packet with:

- the ADJ row (ADJ-01..ADJ-07) selected by the question being asked, not by the binary or service name (`PROVINCE.md` lines 44-52);
- the IN id, sibling, `sibling_path`, pinned commit, `target_path`, cited range and `found_line`;
- the minimum evidence fields of that ADJ row (`PROVINCE.md` lines 46-52, last column);
- one question for the owner, with no instruction to change a sibling file.

Closure states follow the handoff checklist (`PROVINCE.md` lines 65-68):
`prepared`, `reported`, `acknowledged`, `accepted`, `resolved`.

- A new packet starts at `prepared`.
- It becomes `reported` only when the fleet report names the recipient.
- `acknowledged`, `accepted` and `resolved` need recipient-side durable evidence. None is claimed by this entry.
- Acknowledgement is not acceptance. Resolution requires owner-side closure evidence.

Packets for this round are in §7.

## 5. Records

### Outbound anchors

| Anchor | Province pointer | Heading | Quote line | In cited range | Proposition |
|---|---|---|---|---|---|
| OUT-001 | `../mori-shokunin/PROVINCE.md:6-16` | `# mori-shokunin — Province` | 9 | true | Mori owns kill/OOM and cgroup memory evidence; fleet correlation of host pressure is mori's, not OS triage. |
| OUT-002 | `../kama-shokunin/PROVINCE.md:3-24` | `# kama-shokunin — Province` | 12 | true | Kama owns served-model identity reconciliation; an endpoint or served-model mismatch is kama's analysis, not a driver/GPU-readiness finding. |
| OUT-003 | `../kagi-shokunin/PROVINCE.md:3-6,10-17,32-34,54` | `# kagi-shokunin — Province` | 3 | true | Kagi owns secrets and vault operations, the-janitor credential flows, and credential-hygiene evidence. |
| OUT-004 | `../mado-shokunin/PROVINCE.md:3-16` | `# mado-shokunin — Province` | 6 | true | Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and screen/idle behavior. |
| OUT-005 | `../mori-shokunin/PROVINCE.md:3-16` | `# mori-shokunin — Province` | 8 | true | Mori owns kill/OOM catalog-ID and signal-11 coredump classification from separately labeled user/system journals; fleet attribution is its correlation, not tsukuroi's. |
| OUT-006 | `../kumitate-shokunin/PROVINCE.md:3-6` | `# kumitate-shokunin — Province` | 3 | true | Kumitate scopes OMP task/hub and orchestration tooling, so task/hub dispatch and routing semantics are its analysis, not tsukuroi's. |
| OUT-007 | `../mori-shokunin/PROVINCE.md:12-16` | `# mori-shokunin — Province` | 12 | true | Mori refuses dispatch and orchestration mechanism and routes it to kumitate, supporting ADJ-05's kumitate recipient. |
| OUT-008 | `../kaidoku-shokunin/PROVINCE.md:3-6,88-100` | `# kaidoku-shokunin — Province` | 3 | true | Kaidoku declares shipped-artifact reverse engineering with REA as its domain, the scope ADJ-06 would hand to an RE owner. |
| OUT-009 | `../revenger-shokunin/PROVINCE.md:3-7,19-25` | `# revenger province` | 3 | true | Revenger owns shipped-artifact reverse engineering (binaries, packages, APKs) with an observation/inference/unknown evidence ledger; tsukuroi tracks state only. |
| OUT-010 | `../tameshi-shokunin/PROVINCE.md:3-18` | `# tameshi-shokunin — Province` | 7 | true | Tameshi owns the reusable verification/mutation-testing method, applied to fleet gates as read-only primary surfaces; each lane keeps its own gate. |

### Inbound classification

| Id | Sibling file:line | Pointer target | Scope | Class | Found line | Evidence quote |
|---|---|---|---|---|---|---|
| IN-001 | `kaidoku:.ufo/waves/luna-round-10/CB1.md:10` | `PROVINCE.md:42` | historical | DRIFTED | 51 | protocol integrator — kaidoku/revenger ownership unresolved |
| IN-002 | `kaidoku:.ufo/waves/luna-round-10/DB4.md:12` | `PROVINCE.md:42,70-71` | historical | DRIFTED | 51 | protocol integrator — kaidoku/revenger ownership unresolved |
| IN-003 | `kaidoku:.ufo/waves/luna-round-10/K1.md:9` | `PROVINCE.md:42,70-71` | historical | DRIFTED | 51 | protocol integrator — kaidoku/revenger ownership unresolved |
| IN-004 | `kaidoku:.ufo/waves/luna-round-10/K1.md:9` | `corpus/knowledge/adjacency-handoffs-fleet-r1.md:54` | historical | RESOLVES | 54 | Both declare shipped-artifact RE. No owner selected, no target run, no raw core forwarded. |
| IN-005 | `kaidoku:.ufo/waves/luna-round-10/QB3.md:5` | `PROVINCE.md:42,70-71` | historical | DRIFTED | 51 | protocol integrator — kaidoku/revenger ownership unresolved |
| IN-006 | `kaidoku:.ufo/waves/luna-round-10/SB4.md:12` | `PROVINCE.md:42,70-71` | historical | DRIFTED | 51 | protocol integrator — kaidoku/revenger ownership unresolved |
| IN-007 | `kaidoku:.ufo/waves/luna-round-6/K1.md:9` | `PROVINCE.md:8-24,35-37` | historical | RESOLVES | 8 | **Owns (surfaces, all read-only probes):** pacman state |
| IN-008 | `kaidoku:.ufo/waves/round-15/w1/SiblingBoundary.md:22` | `PROVINCE.md:8-14,25-28,51` | historical | RESOLVES | 8 | **Owns (surfaces, all read-only probes):** pacman state |
| IN-009 | `kaidoku:.ufo/waves/round-15/w1/SiblingBoundary.md:255` | `PROVINCE.md:25-28` | historical | RESOLVES | 26 | binary RE of drivers (→ kaidoku/revenger |
| IN-010 | `kaidoku:.ufo/waves/round-17/w1/ConnSiblingOverlap.md:15` | `PROVINCE.md:26` | historical | RESOLVES | 26 | binary RE of drivers (→ kaidoku/revenger |
| IN-011 | `kaidoku:.ufo/waves/round-17/w1/ConnSiblingOverlap.md:30` | `.ufo/waves/round-12/PackageBlind.md:110` | historical | RESOLVES | 110 | ./.BUILDINFO time=1760286101.0 mode=644 size=5270 |
| IN-012 | `kaidoku:.ufo/waves/round-18/w1/ConnSiblingOverlap.md:39` | `PROVINCE.md:79` | historical | RESOLVES | 79 | Kaidoku and revenger both declare shipped-artifact RE. The integrator must |
| IN-013 | `kama:.ufo/waves/round-17/build/advice/ConnectTsukuroi.md:20` | `PROVINCE.md:27-28` | historical | RESOLVES | 27 | Never installs, upgrades, or removes packages; |
| IN-014 | `kama:.ufo/waves/round-17/build/advice/ConnectTsukuroi.md:21` | `MINT.md:18-19` | historical | RESOLVES | 18 | read-only detection and report; never installs, |
| IN-015 | `kama:.ufo/waves/round-17/build/advice/ConnectTsukuroi.md:22` | `SKILL.md:144` | historical | RESOLVES | 144 | never installs, upgrades, removes, or restarts |
| IN-016 | `kama:.ufo/waves/round-17/falsify/advice/ConnectTsukuroi.md:42` | `corpus/QUALITY.md:13` | historical | RESOLVES | 13 | Every negative claim includes its bounded search/probe sweep command, scope and date |
| IN-017 | `kama:.ufo/waves/round-17/falsify/advice/ConnectTsukuroi.md:50` | `PROVINCE.md:27-28` | historical | RESOLVES | 27 | Never installs, upgrades, or removes packages; |
| IN-018 | `kama:.ufo/waves/round-17/falsify/advice/ConnectTsukuroi.md:50` | `SKILL.md:144-155` | historical | RESOLVES | 144 | never installs, upgrades, removes, or restarts |
| IN-019 | `kama:.ufo/waves/round-17/falsify/advice/ConnectTsukuroi.md:51` | `PROVINCE.md:8-14` | historical | RESOLVES | 8 | Owns (surfaces, all read-only probes): |
| IN-020 | `kama:.ufo/waves/round-17/falsify/advice/ConnectTsukuroi.md:59` | `PROVINCE.md:65-68` | historical | RESOLVES | 66 | Acknowledgement is not acceptance; resolution |
| IN-021 | `kotoba:.ufo/round-22/scouts/A6.md:47` | `.ufo/l0-questions.md:1-2` | historical | RESOLVES | 1 | Only operator/global-routing authority can provide these bindings. |
| IN-022 | `lore:.ufo/waves/round-87/K1.md:28` | `PROVINCE.md:3-19` | historical | RESOLVES | 3 | host operability & system repair |
| IN-023 | `mado:.ufo/evidence/round-12/l2-connector.md:13` | `SKILL.md:101,404,755,842` | historical | RESOLVES | 755 | (`omarchy-walker → walker` unversioned; walker moved 2.16.2-1 → 2.17.0-1 on 2026-10-11, and |
| IN-024 | `mado:.ufo/waves/round-13/w1/RegistryDraft.md:57` | `SKILL.md:1705-1715` | historical | RESOLVES | 1707 | \| Name \| Kind \| Entry command \| Verdict map \| Self-test \| Pinned values \| Write scope \| Owner \| |
| IN-025 | `mado:.ufo/waves/round-13/w1/ReviewRegistry.md:15` | `SKILL.md:1705` | historical | RESOLVES | 1705 | ### Gate registry |
| IN-026 | `mado:.ufo/waves/round-13/w1/reports/RegistryDraft.md:57` | `SKILL.md:1705-1715` | historical | RESOLVES | 1707 | \| Name \| Kind \| Entry command \| Verdict map \| Self-test \| Pinned values \| Write scope \| Owner \| |
| IN-027 | `mado:.ufo/waves/round-13/w1/reports/SiblingOverlap.md:28` | `PROVINCE.md:3-14` | historical | RESOLVES | 12 | driver/firmware plane (kernel modules, nvidia driver + GSP firmware |
| IN-028 | `mado:.ufo/waves/round-14/w1/SiblingOverlap.md:130` | `PROVINCE.md:6-14` | historical | RESOLVES | 12 | driver/firmware plane (kernel modules, nvidia driver + GSP firmware |
| IN-029 | `mado:.ufo/waves/round-14/w1/reports/SiblingOverlap.md:130` | `PROVINCE.md:6-14` | historical | RESOLVES | 12 | driver/firmware plane (kernel modules, nvidia driver + GSP firmware |
| IN-030 | `mado:.ufo/waves/round-15/w1/reports/ReviewSafety.md:65` | `PROVINCE.md:11-14` | historical | RESOLVES | 11 | journal/boot triage (`journalctl -b`, dmesg error classes), |
| IN-031 | `mado:.ufo/waves/round-15/w1/reports/ReviewSafety.md:65` | `PROVINCE.md:48` | historical | RESOLVES | 48 | configuration-level diagnosis \| User-manager/unit, package and driver health; an active unit does not prove the UI works \| mado |
| IN-032 | `mado:.ufo/waves/round-15/w1/reports/SiblingBoundary.md:155` | `PROVINCE.md:8-15` | historical | RESOLVES | 8 | **Owns (surfaces, all read-only probes):** pacman state (`pacman -Qkk` |
| IN-033 | `mado:.ufo/waves/round-16/w1/reports/SiblingBoundary.md:35` | `PROVINCE.md:8-14` | historical | RESOLVES | 8 | **Owns (surfaces, all read-only probes):** pacman state (`pacman -Qkk` |
| IN-034 | `mado:.ufo/waves/round-16/w1/reports/SiblingBoundary.md:36` | `PROVINCE.md:16-23` | historical | RESOLVES | 20 | \| `Arch News` upgrade gate \| Match official notices to local package/config evidence; a public feed read is not host state |
| IN-035 | `mado:.ufo/waves/round-16/w1/reports/SiblingBoundary.md:37` | `PROVINCE.md:25-28` | historical | RESOLVES | 28 | never restarts services. Detection and report; the operator remediates. |
| IN-036 | `mado:.ufo/waves/round-16/w1/reports/SiblingBoundary.md:38` | `PROVINCE.md:48` | historical | RESOLVES | 48 | User-manager/unit, package and driver health; an active unit does not prove the UI works |
| IN-037 | `mado:.ufo/waves/round-16/w1/reports/SiblingBoundary.md:39` | `PROVINCE.md:59-60` | historical | RESOLVES | 59 | 2. Select the matching row by the **question being asked**, not the binary or |
| IN-038 | `mado:.ufo/waves/round-16/w1/reports/SiblingBoundary.md:74` | `PROVINCE.md:27-28` | historical | RESOLVES | 28 | Detection and report; the operator remediates. |
| IN-039 | `mado:.ufo/waves/round-16/w1/reports/SiblingBoundary.md:84` | `PROVINCE.md:10-11` | historical | RESOLVES | 10 | systemd user units & timers (`systemctl --user`, unit files, failed |
| IN-040 | `mado:.ufo/waves/round-16/w1/reports/SiblingBoundary.md:93` | `PROVINCE.md:59-60` | historical | RESOLVES | 59 | Select the matching row by the **question being asked**, not the binary or |
| IN-041 | `mado:.ufo/waves/round-16/w1/reports/SiblingBoundary.md:98` | `PROVINCE.md:44-52` | historical | RESOLVES | 44 | \| ID \| Finding / boundary trigger \| Tsukuroi retains \| Next analysis recipient \| Minimum handoff evidence \| Ownership source \| |
| IN-042 | `mado:.ufo/waves/round-17/w1/reports/SiblingOverlap.md:135` | `SKILL.md:101,404,427,734-756` | historical | RESOLVES | 427 | Cross-domain: `walker-restart.hook` root-exec of a user-owned script → |
| IN-043 | `mado:.ufo/waves/round-18/w1/reports/SiblingOverlap18.md:317` | `SKILL.md:734-756` | historical | RESOLVES | 734 | **`offline-exile` (14: 13 `elephant-*` 2.21.0-1 + `omarchy-walker` 1.0.0-2)** — installed |
| IN-044 | `mado:.ufo/waves/round-18/w2/reports/ConnProvinceScope.md:50` | `PROVINCE.md:48` | historical | RESOLVES | 48 | diagnosis \| User-manager/unit, package and driver health; an active unit does not prove the UI works \| mado |
| IN-045 | `mado:.ufo/waves/round-19/w1/reports/ConnProvinceRoster.md:21` | `PROVINCE.md:48` | historical | RESOLVES | 48 | diagnosis \| User-manager/unit, package and driver health; an active unit does not prove the UI works \| mado |
| IN-046 | `mado:.ufo/waves/round-19/w2/reports/AtkProvinceLine.md:25` | `SKILL.md:47,50,108` | historical | RESOLVES | 50 | `[omarchy] SigLevel = Optional TrustAll` — soft-trust channel (`package-state-plane.md:9-41`) |
| IN-047 | `mado:.ufo/waves/round-20/w1/reports/ConnCriteriaFleet.md:37` | `corpus/QUALITY.md:40` | historical | RESOLVES | 40 | Named count corrections include the exact counted argv or other finite input set. |
| IN-048 | `mori:.ufo/waves/round-13/build/SiblingOverlap.md:27` | `PROVINCE.md:3-33` | historical | RESOLVES | 8 | **Owns (surfaces, all read-only probes):** pacman state (`pacman -Qkk` |
| IN-049 | `mori:.ufo/waves/round-13/build/SiblingOverlap.md:29` | `corpus/knowledge/oom-event-plane.md:215-258,291-312,344-375` | historical | RESOLVES | 256 | province. Q2. **Consequence for detection:** treat `memory.events oom_kill` as a *presence flag*, not as a |
| IN-050 | `mori:.ufo/waves/round-13/build/SiblingOverlap.md:33` | `corpus/knowledge/kill-event-deep-r8.md:26-37,83-100,120-135` | historical | RESOLVES | 31 | \| F2 \| **Message #3 is teardown-coincident, not kill-coincident**: it follows `user@1000.service: Consumed …` by **0.45 ms** |
| IN-051 | `mori:.ufo/waves/round-13/build/SiblingOverlap.md:37` | `PROVINCE.md:35-74` | historical | RESOLVES | 49 | \| ADJ-04 \| Host pressure or a kill signal needs fleet/wave attribution, liveness or progress correlation |
| IN-052 | `mori:.ufo/waves/round-13/build/SiblingOverlap.md:41` | `corpus/knowledge/adjacency-handoffs-fleet-r1.md:74-113` | historical | RESOLVES | 74 | ## 3. Executed observation packet — TSUKUROI-F1-MEM-01 |
| IN-053 | `mori:.ufo/waves/round-13/build/SiblingOverlap.md:43` | `corpus/knowledge/adjacency-recheck-2026-10-19.md:5-22,47,89-92` | historical | RESOLVES | 47 | \| ADJ-04 \| `prepared` \| `TSUKUROI-F1-MEM-01` is prepared |
| IN-054 | `mori:.ufo/waves/round-13/build/SiblingOverlap.md:174` | `corpus/knowledge/adjacency-handoffs-fleet-r1.md:74-113` | historical | RESOLVES | 74 | ## 3. Executed observation packet — TSUKUROI-F1-MEM-01 |
| IN-055 | `mori:.ufo/waves/round-14/build/SiblingBoundary.md:38` | `PROVINCE.md:1-33` | historical | RESOLVES | 25 | **Refuses:** endpoint/model serving health (→ kama), secrets (→ kagi), |
| IN-056 | `mori:.ufo/waves/round-15/build/ConnectSiblingOverlap.md:41` | `PROVINCE.md:3-15` | historical | RESOLVES | 3 | **Domain:** host operability & system repair (繕, mending) — the OS |
| IN-057 | `mori:.ufo/waves/round-15/build/ConnectSiblingOverlap.md:43` | `PROVINCE.md:27-28` | historical | RESOLVES | 28 | never restarts services. Detection and report; the operator remediates. |
| IN-058 | `mori:.ufo/waves/round-15/build/ConnectSiblingOverlap.md:45` | `PROVINCE.md:49` | historical | RESOLVES | 49 | Request correlation, not a claim that a wave caused OOM |
| IN-059 | `mori:.ufo/waves/round-15/build/ConnectSiblingOverlap.md:47` | `PROVINCE.md:49` | historical | RESOLVES | 49 | Capture time, boot/window, exact counter or PSI command/exit and observed value |
| IN-060 | `mori:.ufo/waves/round-15/build/ConnectSiblingOverlap.md:48` | `PROVINCE.md:38-42` | historical | RESOLVES | 38 | A recipient is an analysis/report owner, **not permission to repair**. |
| IN-061 | `mori:.ufo/waves/round-15/build/ConnectSiblingOverlap.md:66` | `PROVINCE.md:27-28` | historical | RESOLVES | 28 | never restarts services. Detection and report; the operator remediates. |
| IN-062 | `mori:.ufo/waves/round-16/build/ReviewRegistry.md:55` | `PROVINCE.md:19` | historical | DRIFTED | 28 | never restarts services. Detection and report; the operator remediates. |
| IN-063 | `mori:.ufo/waves/round-16/build/SiblingScope.md:18` | `PROVINCE.md:8-14,25-33,44-52` | historical | RESOLVES | 25 | **Refuses:** endpoint/model serving health (→ kama), secrets (→ kagi), |
| IN-064 | `mori:.ufo/waves/round-16/build/SiblingScope.md:59` | `PROVINCE.md:44-52` | historical | RESOLVES | 49 | \| ADJ-04 \| Host pressure or a kill signal needs fleet/wave attribution |
| IN-065 | `mori:.ufo/waves/round-17/build/CensusConsumers.md:98` | `.ufo/waves/round-17/falsify/outcome.json:15` | historical | DRIFTED | 107 | "dead_seats_labelled_provider_429_in_interim": [ |
| IN-066 | `mori:.ufo/waves/round-17/build/SiblingSeatDeathTools.md:91` | `tools/check-seat-scope.py:12-15` | historical | RESOLVES | 13 | SCOPE-TRAILER-MALFORMED (an annotated/ambiguous `none` is neither evidence of an |
| IN-067 | `mori:PROVINCE.md:66` | `PROVINCE.md:21-24,35-44` | operative | DRIFTED | 8 | **Owns (surfaces, all read-only probes):** pacman state (`pacman -Qkk` |
| IN-068 | `mori:PROVINCE.md:66` | `corpus/knowledge/oom-event-plane.md:231-257,279-281,301,344-367` | operative | RESOLVES | 344 | \| 1 \| `systemd-oomd` (userland PSI+swap monitor) \| unit present (`/usr/lib/systemd/system/systemd-oomd.service`); `is-active`=inactive, `is-enabled`=disabled; |
| IN-069 | `mori:PROVINCE.md:66` | `corpus/knowledge/kill-event-deep-r8.md:30-37,97,120-135` | operative | RESOLVES | 97 | All three carry `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`; the local catalog |
| IN-070 | `mori:PROVINCE.md:71` | `corpus/knowledge/adjacency-handoffs-fleet-r1.md:74-112` | operative | RESOLVES | 83 | - State in this child artifact: **prepared**. Report receipt is the later |
| IN-071 | `mori:PROVINCE.md:73` | `corpus/knowledge/adjacency-handoffs-fleet-r1.md:94-104` | operative | RESOLVES | 101 | absent, not zero; no cgroup subtree was enumerated. The packet demonstrates |
| IN-072 | `mori:SKILL.md:327` | `PROVINCE.md:19` | operative | DRIFTED | 28 | never restarts services. Detection and report; the operator remediates. |
| IN-073 | `mori:corpus/knowledge/kernel-oom-line-attribution-r12.md:8` | `corpus/knowledge/oom-event-plane.md:23-42,359-367` | operative | RESOLVES | 23 | The retained journal (13 boots, `journalctl --list-boots --no-pager`, 14:38) holds **one** kernel OOM dump and |
| IN-074 | `mori:corpus/knowledge/kill-classes-by-message-id-r12.md:8` | `corpus/knowledge/kill-event-deep-r8.md:97,120-135` | operative | RESOLVES | 97 | All three carry `MESSAGE_ID=fe6faa94e7774663a0da52717891d8ef`; the local catalog |
| IN-075 | `mori:corpus/knowledge/oom-kill-counter-kernel-only-r12.md:8` | `corpus/knowledge/oom-event-plane.md:245-257,359-367` | operative | RESOLVES | 245 | ### 4.2 The counter anomaly — two documented waves, surviving counter = 1 |
| IN-076 | `mori:corpus/knowledge/userspace-oom-killers-r12.md:8` | `corpus/knowledge/oom-event-plane.md:344-346,353-367` | operative | RESOLVES | 344 | \| 1 \| `systemd-oomd` (userland PSI+swap monitor) \| unit present (`/usr/lib/systemd/system/systemd-oomd.service`); `is-active`=inactive, `is-enabled`=disabled; |
| IN-077 | `revenger:.ufo/waves/kaika-r1/connector.md:18` | `PROVINCE.md:42` | historical | DRIFTED | 51 | \| ADJ-06 \| Driver/firmware/package mechanism requires shipped-artifact reverse engineering beyond health inventory |
| IN-078 | `revenger:.ufo/waves/kaika-r1/connector.md:18` | `corpus/knowledge/adjacency-handoffs-fleet-r1.md:54` | historical | RESOLVES | 54 | Both declare shipped-artifact RE. No owner selected, no target run, no raw core forwarded. |
| IN-079 | `revenger:.ufo/waves/kaika-r1/connector.md:72` | `PROVINCE.md:42` | historical | DRIFTED | 51 | \| ADJ-06 \| Driver/firmware/package mechanism requires shipped-artifact reverse engineering beyond health inventory |
| IN-080 | `revenger:.ufo/waves/kaika-r1/connector.md:74` | `corpus/knowledge/adjacency-handoffs-fleet-r1.md:54` | historical | RESOLVES | 54 | Both declare shipped-artifact RE. No owner selected, no target run, no raw core forwarded. |
| IN-081 | `souji:.ufo/waves/round-13/w1/Overlap.md:50` | `PROVINCE.md:3-48` | historical | RESOLVES | 8 | **Owns (surfaces, all read-only probes):** pacman state (`pacman -Qkk` |
| IN-082 | `souji:.ufo/waves/round-16/w1/SiblingOverlap.md:17` | `SKILL.md:706-709` | historical | RESOLVES | 708 | independent sweeps of one file = two pins, cited separately, never merged (record draft §1 |
| IN-083 | `souji:.ufo/waves/round-16/w1/SiblingOverlap.md:28` | `SKILL.md:706-709` | historical | RESOLVES | 709 | cross-lane note — `:70-78` in the revision seen); both pins must cite committed bytes. |
| IN-084 | `souji:.ufo/waves/round-16/w1/SiblingOverlap.md:66` | `PROVINCE.md:52` | historical | RESOLVES | 52 | measured census revision and expected domain invariant; ask for method advice, not transfer of gate ownership |
| IN-085 | `souji:.ufo/waves/round-18/w1/ConnFleetPointerTools.md:63` | `SKILL.md:1968` | historical | RESOLVES | 1968 | last recheck directive, pointer/direct command scope, R17/R18-RECHECK replacement; forbidden binary set |
| IN-086 | `souji:.ufo/waves/round-18/w1/ConnSiblingProcHygiene.md:34` | `SKILL.md:2` | historical | RESOLVES | 2 | name: tsukuroi-shokunin |
| IN-087 | `souji:.ufo/waves/round-18/w1/RevC3Province.md:13` | `PROVINCE.md:3-8,25-28,37-42` | historical | RESOLVES | 39 | Tsukuroi retains the OS finding. No row authorizes configuration writes, |
| IN-088 | `souji:.ufo/waves/round-18/w1/RevC3Province.md:14` | `PROVINCE.md:30-33,49` | historical | RESOLVES | 32 | The existing census reports those signals; fleet correlation belongs to mori |
| IN-089 | `souji:.ufo/waves/round-18/w1/RevC3Province.md:15` | `PROVINCE.md:62-64` | historical | RESOLVES | 64 | operator action. Never copy credentials, raw configs, raw cores or argv. |
| IN-090 | `souji:census/round-12/connector.md:29` | `PROVINCE.md:3,18` | operative | RESOLVES | 3 | **Domain:** host operability & system repair (繕, mending) — the OS |
| IN-091 | `souji:census/round-16/transcripts/w1/SiblingOverlap.txt:52` | `PROVINCE.md:1-60` | operative | RESOLVES | 1 | # tsukuroi-shokunin — Province |
| IN-092 | `tabi:.ufo/waves/round-16/drafts/DraftAdjacency.md:29` | `PROVINCE.md:8-14` | historical | RESOLVES | 8 | **Owns (surfaces, all read-only probes):** pacman state (`pacman -Qkk` |
| IN-093 | `tabi:.ufo/waves/round-16/w1/ConnSiblings.md:71` | `PROVINCE.md:8-14,27` | historical | RESOLVES | 27 | health*, not internals). Never installs, upgrades, or removes packages; |
| IN-094 | `tameshi:.ufo/waves/round-14/w1/FreshnessIntake.md:77` | `plans/round-5.plan.md:3-11` | historical | RESOLVES | 3 | Claim: (a) tameshi's mutate-and-run.sh is applied to tsukuroi's OWN census |
| IN-095 | `tameshi:.ufo/waves/round-14/w1/FreshnessIntake.md:192` | `plans/round-5.plan.md:3-11` | historical | RESOLVES | 4 | gate (read-only on the tool; copies in /tmp) — the lane measures its own |
| IN-096 | `tameshi:.ufo/waves/round-16/w1/CR13.md:78` | `plans/round-5-record-draft.md:445` | historical | RESOLVES | 445 | committed HEAD `084951be…78c5` (976 ln) vs worktree `aae45531…7df6` (1032 |
| IN-097 | `tameshi:.ufo/waves/round-16/w2/ContamA.md:67` | `plans/round-5-record-draft.md:323-324` | historical | DRIFTED | 347 | the worktree (26 → 35 by 17:07Z, §2 erratum) while `SKILL.md`'s census-v2 row |
| IN-098 | `tameshi:.ufo/waves/round-16/w2/ProvinceAppend.md:44` | `plans/round-5.plan.md:3-11` | historical | RESOLVES | 4 | gate (read-only on the tool; copies in /tmp) — the lane measures its own |
| IN-099 | `tameshi:.ufo/waves/round-16/w2/RunnerDiff.md:106` | `SKILL.md:568-570` | historical | RESOLVES | 569 | `26a27d352690e64b2396a4aabaf4ddf6` (1001 lines), sha256 `597e141989065e03…331b`. Anti-claim |
| IN-100 | `tameshi:.ufo/waves/round-17/w2/SiblingImpact.md:82` | `SKILL.md:565-570` | historical | RESOLVES | 568 | (`tameshi-shokunin/tools/mutate-and-run.sh:16-21,60`). Tool pin: r4-2, md5 |
| IN-101 | `tameshi:.ufo/waves/round-18/w1/C04GitEnvPriorArt.md:44` | `tools/_revision.py:62-72` | historical | RESOLVES | 62 | env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")} |
| IN-102 | `tameshi:corpus/knowledge/closeout-r11.md:259` | `SKILL.md:1059-1063` | operative | DRIFTED | 1067 | The shipped suite is **not** to be described |
| IN-103 | `tameshi:corpus/knowledge/fleet-suite-census.md:304` | `plans/round-5.plan.md:3-9` | operative | RESOLVES | 5 | suite's kill-rate and hardens whatever survives (new selftest cases land in |
| IN-104 | `tameshi:corpus/knowledge/mutation-case-tsukuroi-census.md:21` | `plans/round-5-record-draft.md:323-324` | operative | DRIFTED | 347 | the worktree (26 → 35 by 17:07Z, §2 erratum) while `SKILL.md`'s census-v2 row |
| IN-105 | `tameshi:corpus/knowledge/service-optin-protocol.md:36` | `plans/round-5.plan.md:3-11` | operative | RESOLVES | 4 | gate (read-only on the tool; copies in /tmp) — the lane measures its own |
| IN-106 | `tameshi:corpus/knowledge/service-optin-protocol.md:46` | `plans/round-5.plan.md:3-11` | operative | RESOLVES | 9 | the mutation manually per tameshi's published recipe (the adjacency claim |
| IN-107 | `tameshi:corpus/knowledge/service-optin-protocol.md:47` | `SKILL.md:558-568` | operative | DRIFTED | 570 | resolved as **fit, not gap**: the gate's `--selftest` satisfies the suite contract |
| IN-108 | `tameshi:corpus/knowledge/service-optin-protocol.md:51` | `plans/round-5-record-draft.md:70-79` | operative | RESOLVES | 76 | tameshi's is cited only as cross-reference if it lands — never merged, |
| IN-109 | `tameshi:corpus/knowledge/service-optin-protocol.md:153` | `tools/tsukuroi-census.sh:915-970` | operative | DRIFTED | 2216 | check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED |
| IN-110 | `tameshi:corpus/knowledge/service-optin-protocol.md:154` | `plans/round-5-record-draft.md:316-319` | operative | RESOLVES | 316 | **Hardening ledger skeleton:** survivor id \| site (swept revision line) \| why |
| IN-111 | `tameshi:corpus/knowledge/service-optin-protocol.md:158` | `SKILL.md:599-609` | operative | DRIFTED | 611 | MUTATE: DONE (target=tsukuroi-census-hardened defects=23 killed=23 survived=0 inconclusive=0 kill-rate=100%) |
| IN-112 | `tameshi:corpus/knowledge/service-optin-protocol.md:199` | `SKILL.md:611-617` | operative | RESOLVES | 616 | Adjudication rules kept for re-use: killed = suite red **and** the full case count still |
| IN-113 | `tameshi:corpus/knowledge/service-optin-protocol.md:224` | `plans/round-5.plan.md:3-11` | operative | RESOLVES | 3 | Claim: (a) tameshi's mutate-and-run.sh is applied to tsukuroi's OWN census |
| IN-114 | `tameshi:plans/round-9.plan.md:146` | `plans/round-8.plan.md:45-50` | operative | RESOLVES | 45 | - (D) is folded into (A), not a separate move: the watch reuses the baseline |

Totals (author-side, recomputed by the gate at the landed revision): inbound RESOLVES 97 (historical 79, operative 18), DRIFTED 17 (historical 10, operative 7), UNRESOLVABLE 0. Per-record notes (relied-on use, history of the move) are in the JSON registry. Classification seats: build wave InClass001..InClass105 (`.ufo/waves/round-19/build/`).


## 6. Recheck and bounded sweeps

- Gate: `python3 tools/check-adjacency-anchors.py --revision <REV>`; measured results are in `.ufo/waves/round-19/measure/` at the landed revision named in LOG.md.
- Pointer census (negative claim: exactly ten sibling-file pointers in the lane `PROVINCE.md`): `grep -nE '\.\./[a-z0-9-]+-shokunin/[^ )|]*\.md' PROVINCE.md`. Observed 2026-10-20 at the lane working tree: matches on lines 33, 46, 47, 48, 49, 50 (two), 51 (two) and 52, which is ten. Scope: `PROVINCE.md` only.
- No portable section yet (negative claim): `grep -n '^## Adjacent — portable' PROVINCE.md`. Observed 2026-10-20: no match. Scope: `PROVINCE.md` only.

## 7. Owner handoff packets (operative drifts) — state `prepared`; `reported` when the round-19 fleet report names the owner

These are pointer-drift reports, not one of the seven ADJ shared-work classes: the owner decides whether and how to repoint. Tsukuroi edits no sibling file and prescribes no replacement text; the suggested heading + quote is a locator offer only.

| Packet | Owner | Sibling locus @ commit | Cited tsukuroi locus | Content now at | Suggested portable locator |
|---|---|---|---|---|---|
| HP-IN-067 | mori | `PROVINCE.md:66` @ `91940fa339e3` | `PROVINCE.md:21-24,35-44` | line 8 | `PROVINCE.md` § `## Core` — **Owns (surfaces, all read-only probes):** pacman state |
| HP-IN-072 | mori | `SKILL.md:327` @ `91940fa339e3` | `PROVINCE.md:19` | line 28 | `PROVINCE.md` § `## Core` — never restarts services. Detection and report; the operator remediates. |
| HP-IN-102 | tameshi | `corpus/knowledge/closeout-r11.md:259` @ `01d586ddbc5f` | `SKILL.md:1059-1063` | line 1067 | `SKILL.md` § `### The verification — VER-S8` — Coverage debt, named — 9 clause sites un-exercised by the 49-case suite |
| HP-IN-104 | tameshi | `corpus/knowledge/mutation-case-tsukuroi-census.md:21` @ `01d586ddbc5f` | `plans/round-5-record-draft.md:323-324` | line 347 | `plans/round-5-record-draft.md` § `## 5. Record skeleton` — the worktree (26 → 35 by 17:07Z, §2 erratum) |
| HP-IN-107 | tameshi | `corpus/knowledge/service-optin-protocol.md:47` @ `01d586ddbc5f` | `SKILL.md:558-568` | line 570 | `SKILL.md` § `### Own-gate mutation — two revisions, never conflated (TSUKUROI-S5-1)` |
| HP-IN-109 | tameshi | `corpus/knowledge/service-optin-protocol.md:153` @ `01d586ddbc5f` | `tools/tsukuroi-census.sh:915-970` | line 2216 | `tools/tsukuroi-census.sh` marker `# ---- round-5 mutation hardening (lane S5-1, 2026-10-14)` |
| HP-IN-111 | tameshi | `corpus/knowledge/service-optin-protocol.md:158` @ `01d586ddbc5f` | `SKILL.md:599-609` | line 611 | `SKILL.md` round-5 own-gate mutation block, 23/23 re-sweep line |

Mori's round-18 closure pointers (`PROVINCE:66`, `SKILL:318`) are IN-067 and IN-072; the closure's `SKILL:318` is line 327 at mori `91940fa339e3` (the census reads the committed tip).

## 8. Inbound handoff receipt — mori → tsukuroi (detection only)

- **Received:** `../mori-shokunin/PROVINCE.md:111-117` reports a 09:15:30 `pacman -Syu` and a 13:23:08 `pacman -U …zcode…`, cites `PacmanTxnToday.md`/`PacmanActorTrace.md`, and routes package/boot-chain interpretation and recovery to tsukuroi/operator.
- **ADJ:** no outward row applies; the package/boot-chain question stays here (checklist step 2). State reached: `acknowledged` — this lane-side record is the durable recipient receipt. `accepted`/`resolved` not claimed; no owner-side closure exists.
- **Tsukuroi retains:** OS package and boot-chain diagnosis, with independent ALPM evidence: `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:59,82`; `.ufo/waves/round-18/l1-capture/pacman-events-r18.txt:11-13,40,97,100-101`; S065 `corpus/SOURCES.md:72`. That capture also shows a 09:31:03 elephant-family `-U` absent from the mori bullet.
- **Operator-owned:** all package, rollback, snapshot-boot and service action; zcode's human actor remains inferred, and ALPM records establish no clean client exit.

Recorded 2026-10-20 by the L1 from build seat ScoutMoriHandoff; state `acknowledged` only.

## 9. Contested scope reported, not absorbed (round-19 connectors)

- kaidoku `PROVINCE.md:50` (snapshot `d1d981d2cc04`) claims `pacman -Qkk` and the `.pkg.tar.zst` cache as archive inventory; tsukuroi Core owns `pacman -Qkk` verify loops and `.pkg.tar.zst` receipt discipline (`PROVINCE.md:8-9`). kaidoku `:123` maps GSP firmware regions; tsukuroi tracks GSP presence only. Reported to the integrator with ADJ-06; no owner is picked (ConnSiblingOverlapA, OutAnchor07).
- ADJ-06 kaidoku/revenger shared shipped-artifact RE remains unresolved: fleet `.ufo/l0-questions.md` carries the question with no answer, and no closure note rules it (ConnSiblingOverlapA). The revenger round-1 split proposal is a proposal, not a ruling.
- tameshi `PROVINCE.md:32-35` lists `tools/tsukuroi-census.sh` as a read-only tameshi Core surface; tsukuroi keeps census ownership and ADJ-07 transfers none (OutAnchor09).
- No sibling claims `/boot` writer attribution (ConnWritersMori: `limine|snapper|/boot` absent from all pinned and live sibling PROVINCE files except tsukuroi's).

## QUALITY check

Performed on this frame's bytes at authoring, 2026-10-20. Author-side only.
Not independent verification. It admits nothing. Instance-level checks wait
for the L1-filled tables and the gate run.

1. Falsifiable: an outbound row fails when its quote is absent at `quote_line` or when the commit or blob hash differs. An inbound row fails when `found_line` lies outside the cited range or the quote is absent. Gate run pending.
2. Source: every claim cites census record ids, snapshot paths, or lane `PROVINCE.md` lines named above.
3. Separation: census fields and the two grep results are observations. The RESOLVES, DRIFTED and UNRESOLVABLE labels are inferences against the tip. Whether a pinned sibling commit still contains its text is `[unk]` until the snapshot is checked.
4. Errata append-only: the line-range table in `PROVINCE.md` is retained. Corrections go in appended blocks.
5. Rejection kept: DRIFTED and UNRESOLVABLE rows stay in the inbound table. None is silently dropped.
7. External claims: none in this frame, and no `corpus/SOURCES.md` S### row is cited. Not applicable.
9. Negative claims: the two claims in §6 each carry the bounded search command, its scope and date. The rule that siblings are not edited is a scope rule, not a measured negative, and no sibling-state negative is asserted.
21. Portable locators: met by design. Each anchor is a heading, an exact quote of at most 25 words, a pinned commit and a blob sha256. Line numbers are supplementary. Per-row verification waits for the gate.
30. Whole-proposition counts: met by design. The 10 and 114 counts name their finite sets (OUT-001..OUT-010; IN-001..IN-114). Plural statements cite each record. Counts stay `[unk]` until gate output is recorded.
