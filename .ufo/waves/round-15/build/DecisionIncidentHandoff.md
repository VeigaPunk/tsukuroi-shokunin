# DecisionIncidentHandoff — sanitized incident packet (round 15)

Seat `TsukuroiR15.DecisionIncidentHandoff` · baseline `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2` · report-only, read-only research; no docs edits, no host queries, no package/service/sudo/credential action, no child or labrat dispatch. Tools installed/updated: **none**.

## Operator-facing summary

A logged transaction at `2026-10-20T04:25:16-0300` (`07:25:16Z`) upgraded installed `libinput 1.31.3-1 -> 1.32.0-1` and installed `libinput-tools 1.32.0-1` against sync metadata born `2026-10-18T17:11:00Z`, with 413 upgrades pending against that metadata. This is a documented unsupported partial-upgrade state; no repair, revert or refresh was attempted. Whether the running session is affected, whether input/display behavior changed, and whether the new library is compatible with the installed dependency set were **not measured** — this packet makes no such finding. The operator owns the keep-or-revert choice and any later full upgrade after the boot-hook compatibility gate; agents will make no package or service change.

## Packet `TSUKUROI-R15-INCIDENT-01`

| field | value | provenance |
|---|---|---|
| `packet_id` / `lifecycle` | `TSUKUROI-R15-INCIDENT-01`; **`prepared`** only — not `reported`, `acknowledged`, `accepted` or `resolved` | `PROVINCE.md` handoff checklist 4; `adjacency-handoffs-fleet-r1.md` §5 |
| **trigger** | Logged completed `-S` transaction (`pacman -S --needed --noconfirm libinput libinput-tools`, no `-y`/`-u`) at `07:25:16Z`, upgrading an installed target against sync DBs born 38.2 h earlier. Class: installed-target upgrade against newer sync metadata without a full upgrade — S047's unsupported shape; separation in time from the 10-18 refresh does not change the class. | snapshot `libinput_log`, `sync_metadata`; S047 |
| **action** (observed) | `[ALPM] upgraded libinput (1.31.3-1 -> 1.32.0-1)`; `[ALPM] installed libinput-tools (1.32.0-1)`; no later libinput line or sync marker in the captured extract. | snapshot-pinned lines 2429/2432/2436/2288 |
| `action.authorized` | **`[]` — none.** Recording a past transaction authorizes no `-S/-Sy/-Syu/-U/-R`, refresh, service, sudo, snapper or repair action. | `PROVINCE.md:25-28`; `SKILL.md:156-160` |
| **outcome** | `decision: BLOCKED_FOR_AGENT_PACKAGE_ACTION`; `epistemic: unknown` — not safe, not unsafe, not repaired. Fixed string, independent of any count or probe exit. | C2 JSON `decision`; ReviewIncidentObservation F11 |
| **operator** | Owes three decisions: (a) keep or revert `libinput 1.32.0-1`; (b) whether/when to run a full upgrade, only after the mkinitcpio-42 `/new_root`→`/sysroot` hook risk is cleared with a tested fallback; (c) restart/reboot timing to apply libraries. Named to identify the decision, not recommended; lane endorses and executes none; non-keep routes are downgrade/removal classes outside this lane. | `l0-questions.md:54-55`; ReviewIncidentBoundary F1/F3/F7 |
| `certifications` | `process: not_assessed` · `ui: not_assessed` · `abi: not_assessed` · `health: not_assessed` · `causation: not_assessed` · `boot: not_assessed`. Closed enum; a missing dimension invalidates the packet; no field may read `ok`/`true` from this snapshot. | this fragment |
| `evidence` | `.ufo/waves/round-15/build/host-snapshot.json`; 18,318 B; SHA256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81` (recomputed from raw bytes); `captured_at 2026-10-20T07:44:39Z`; five probes, all exit 0, all stderr empty; stdout rows 4/413/5/16/4. | snapshot; `HostSnapshot.md:5`; C2 JSON |
| `sources` | S047 ArchWiki System maintenance, oldid 885170, opened 2026-10-20: “That is why partial upgrades are **not supported**.” S048 pacman(8), Pacman 7.1.0 footer 2026-10-15: “Only print the targets instead of performing the actual operation (sync, remove or upgrade).” | `SOURCES.md` S047/S048; C2 MD |
| `sanitization` | Include: package names/versions, UTC times, exits/stderr-empty, DB birth/ctime, hook path+line, source IDs, log line numbers. Exclude: credential/auth/token/session/oauth material, environment, PIDs, live argv or `/proc`, journal bodies, `pacman.conf` Server lines, `/home/` paths, and seat/session identity (non-decisional); any future log token containing `://`, `@` or `/home/` is redacted before inclusion. Pending is stored as a **count, never the 413-row list**. | handoff checklist 1-3; SafetySecrets F1/R1; ReviewSnapshotPrivacy |
| `staleness` | Bound to `captured_at`; void on any later pacman transaction, sync marker or package-DB change. New state = new snapshot and new packet revision, never an edit to this one. | C2 limits |

```json
{"packet":"TSUKUROI-R15-INCIDENT-01","lifecycle":"prepared",
 "trigger":{"kind":"logged_no_refresh_transaction","at":"2026-10-20T07:25:16Z","sync_db_born":"2026-10-18T17:11:00Z","doctrine":"S047"},
 "action":{"observed":["libinput 1.31.3-1 -> 1.32.0-1","libinput-tools 1.32.0-1 installed"],"authorized":[]},
 "outcome":{"decision":"BLOCKED_FOR_AGENT_PACKAGE_ACTION","epistemic":"unknown"},
 "certifications":{"process":"not_assessed","ui":"not_assessed","abi":"not_assessed","health":"not_assessed","causation":"not_assessed","boot":"not_assessed"},
 "operator":{"decisions":["libinput keep-or-revert","full-upgrade timing after mkinitcpio-42 hook gate","restart/reboot timing"],"endorsement":"none","execution":"none"},
 "evidence":{"path":".ufo/waves/round-15/build/host-snapshot.json","bytes":18318,"sha256":"b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81","captured_at":"2026-10-20T07:44:39Z","pending_rows":413}}
```

## Non-obvious boundaries

- **Counts are context, not trigger.** 413 equals the historical pending413 figure, so it cannot prove freshness; a count-driven gate would flip on metadata substitution, and `-Qu` exit 1 is ambiguous between "no candidates" and a failed query. The decision is fixed so no count drop clears it.
- **`--needed` is not a no-upgrade switch.** S048's sentence skips only targets already up-to-date; installed 1.31.3 was behind the DB's 1.32.0, so it upgraded. No `-u` was requested, so this was not the full upgrade S047 directs.
- **Second-hand checks stay out.** Soname `.so.10` stability is a consumer-linking promise, not dependency-direction compatibility; `ldd -r` reports missing objects/functions for the checked object at that moment (ldd(1), man-pages 6.19, as quoted in AttackIncidentCause — not re-opened here); the running mapped version was not measured, so "Hyprland keeps 1.31.3" is a ~04:25 seat claim. Encoding any as a field would certify an unmeasured dimension.
- **Detection is not an upgrade arm.** `/sysroot` is the mkinitcpio-42 mount point, not a gate name; this lane never runs `-Syu`, and the always-on tooling directive's channel 1 is not authority over `PROVINCE.md` or the round ban.
- **No ADJ-03 ticket.** No visible UI/binding symptom was reported; package state stays with tsukuroi and the operator. A concrete visual symptom would create a new mado packet (symptom time, OS probe/exit, config pointer), not mutate this one.

## Recommendations for L1

1. Land this table or the summary paragraph in the fleet report; keep `prepared`. `reported` begins only with the committed fleet report; `acknowledged`/`accepted`/`resolved` require operator-side evidence.
2. Keep `certifications` closed. Any future process/UI/ABI measurement is a new packet revision naming probe, exit and time — never overwrite `not_assessed`.
3. Retain the three explicit non-authorizations in operator-facing text: L0 option 3, directive channel 1, `update-safety-v3.md:217` row 2; state the gate detects, never upgrades.
4. Add no health adjectives (`safe`, `harmless`, `compatible`, `caused`, `working`) to C2, LOG or the report; `unknown` is the whole verdict.
5. If delivered, attach the count plus pinned lines only — not the 413-row list, the 16-line extract, or the second-hand checks.

## Evidence retained, limits, tools

- Recomputed digest, byte size, probe exits/stderr and row counts match `HostSnapshot.md:5` and the C2 JSON; no probe was re-run. Sources read: `SOURCES.md` S046-S048 (S046 not used here), C2 MD/JSON, `HostSnapshot.md`, `IncidentTimeline.md`, `AttackIncidentCause.md`, `RuntimeMapping.md`, `ReviewIncidentBoundary.md`, `ReviewSnapshotPrivacy.md`, `SafetySecrets.md`, `update-safety-note.md` §2/§4, `update-safety-v3.md:217`, `PROVINCE.md` handoff checklist, `adjacency-handoffs-fleet-r1.md` §5, `SKILL.md:156-160`, `l0-questions.md:54-55`, fleet `mado.md:17-19`.
- Limits: 413 is a delta against the stale local DB only; no upstream, process, UI, ABI, health, causation or boot verdict. Boot risk is inference/unknown with an operator test-boot falsifier; running version unmeasured. The 2026-10-14 INERT/empty-`-Qu` reading is historical and superseded for current use (C2 MD; ReviewIncidentBoundary F5). C2 pair was not edited; no recipient acknowledgement; this is a derived fragment, not a second record.
- No verification, test, build, lint, formatter or smoke run; nothing is claimed passing. Tools installed/updated: none.
