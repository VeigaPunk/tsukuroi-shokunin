# Round 19 — lesson (tsukuroi, 2026-10-20)

author: tsukuroi L1 (TsukuroiR19). Baseline `452a054677f6b18284917d7c08c45361f91c25ac`. Motivating evidence: `corpus/lessons/round-18-verifier-spotcheck.md` §5 (routed defects 1–6) and the `LOG.md` round19 entries. Claims: C1 adjacency (bidirectional anchors), C2 depth (/boot writer attribution, the sourced claim), C3 calibration (registry ↔ tools). Build wave: 68 seats (`.ufo/waves/round-19/build/`).

## Gate

| Candidate | Decision | Evidence and limits |
|---|---|---|
| Ten portable outbound ownership anchors (heading + ≤25-word quote + pinned commit + blob sha256) | admit author-side | Seats OutAnchor01–09; snapshot bytes equal the sibling git objects 10/10 (ReviewSnapshotBytes); quotes are the siblings' words, attributed, never a tsukuroi grant of authority (CritAdjBoundary); every heading is the sibling title heading because the cited text sits in the preamble |
| 114 inbound pointer classifications (97 RESOLVES, 17 DRIFTED, 0 UNRESOLVABLE; 25 operative, 89 historical) | admit author-side, bounded | Seats InClass001–105; mechanically recomputed by the gate; semantic choice of the relied-on quote is the seat's judgement, sampled by wave 2. Census form only: line-numbered repo-prefixed pointers (ReviewCensusExtract) |
| Seven operative drift handoffs (IN-067, IN-072 mori; IN-102, IN-104, IN-107, IN-109, IN-111 tameshi) | admit as `prepared` packets | Report-only pointer-drift notices; tsukuroi edits no sibling file and prescribes no text (`corpus/knowledge/adjacency-anchors-r19.md` §7) |
| Mori pacman.log detection handoff receipt | admit as `acknowledged` | ScoutMoriHandoff; acceptance/resolution not claimed |
| Seven /boot writer classes and 13 attributed limine.conf events | admit author-side | 10 journal events bound to `_SYSTEMD_UNIT` (S068), 3 ALPM-SCRIPTLET events (S067); hook identity for ALPM events is [inf] (ReviewEventUnits); W-WATCHER dormant |
| `tools/_revision.py` registry row (kind library) plus four corrected cells | admit author-side | RevRevisionLib, ScoutRegistryRowsA/B; update-recheck CLI never exits 1; recheck-commands exit-1 id list completed |
| QUALITY 31–33 | admit author-side | ScoutQualityGaps; each cites a `## Mistakes` row below |
| C2 declared count 0→12 | reject | The declared capture inputs hold 13 `Updated:` lines: the 2026-10-11 pacman.log line 2021 is in the whole-log grep (`host-capture-r19b.txt:1695`); the declaration used the tail-40 window (ScribeWritersEntry, CritWritersCircular) |
| W-WATCHER wrote /boot in the window | reject | Without inotifywait the watcher logs the fallback line and exits (`host-capture-r19b.txt:1365-1368`); all 10 journal events are on snapper-cleanup or limine-snapper-add units (RevWatcher) |
| The cleanup lock explains the 09:08:04 run with no Updated line | reject | The lock check is in the watcher only; the ExecStopPost path has none (ScribeWritersSkill E6). Cause stays [unk] |
| systemd.service(5) documents that ExecStopPost runs in the unit's cgroup | reject | The page has no such sentence (SrcSystemdService); cgroup membership is observed in S068 only |
| 99-limine.hook or 80-limine-efi-deploy.hook writes limine.conf | reject | Their Exec lines copy or deploy EFI binaries only; no Updated line in their spans (RevPacmanHooks, ScoutEntryToolDoc) |
| Pointer drift is an ADJ class; tsukuroi repoints sibling text | reject | Not one of the seven shared-work classes; report-only (CritAdjBoundary) |
| The 89 historical `.ufo/` pointers are owner handoffs | reject | Dated records; classified, never handed off (CritAdjVacuity) |
| ADJ-06 resolved by revenger `round-1` split proposal or MANIFEST tabi/kaidoku ruling | reject | Neither is an integrator ruling on kaidoku/revenger (ConnSiblingOverlapA); still unresolved |
| Issue #4 text as a SOURCES row for the hourly rewrite | reject | 18 issues screened, 0 document the rewrite; the fixing commit is the source (S076) (ConnFrontierLeads) |
| man.archlinux.org pages for systemd.service/timer, systemd-run, snapper are absent | reject | ECONNRESET transport failures; pinned upstream text used instead |
| SKILL.md tool pins (`:207`, `:568`, `:707`, `:1504`) are outbound ownership pointers | reject | Tool pins, not ownership handoffs; outbound scope stays PROVINCE.md (ReviewCensusExtract) |

### Sources opened this round

| Row | URL/path | Access date | Located quote (≤25 words) |
|---|---|---|---|
| S066 | `.ufo/waves/round-19/l1-capture/host-capture-r19.txt` | 2026-10-20 | line 260: “ExecStopPost=limine-snapper-sync”; lines 227-228: “OnBootSec=10m” / “OnUnitActiveSec=1h” |
| S067 | `.ufo/waves/round-19/l1-capture/host-capture-r19b.txt` | 2026-10-20 | line 1366: “inotifywait is not installed. Falling back to Snapper plugin integration.” |
| S068 | `.ufo/waves/round-19/l1-capture/host-capture-r19c.txt` | 2026-10-20 | line 13: “snapper-cleanup.service /system.slice/snapper-cleanup.service Updated: /boot/limine.conf” |
| S069 | `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json` | 2026-10-20 | `"lane_tip": "452a054677f6b18284917d7c08c45361f91c25ac"`; `"inbound": 114, "outbound": 10` |
| S070 | https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html (pinned v262.1 XML) | 2026-10-20 | ExecStopPost=: “Additional commands that are executed after the service is stopped.” |
| S071 | https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html | 2026-10-20 | OnUnitActiveSec=: “Defines a timer relative to when the unit the timer unit is activating was last activated.” |
| S072 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-run.xml | 2026-10-20 | lines 64-65: “systemd-run may be used to create and start a transient .service or .scope unit and run the specified COMMAND in it.” |
| S073 | https://raw.githubusercontent.com/openSUSE/snapper/v0.13.2/doc/snapper.xml.in | 2026-10-20 | PLUGINS: “snapper can execute external scripts after certain actions. Scripts have to be placed in /usr/lib/snapper/plugins.” |
| S074 | https://gitlab.com/Zesko/limine-snapper-sync/-/raw/1.32.1/README.md | 2026-10-20 | line 826: “Snapper plugin integration for snapshot create, modify, delete, and rollback events” |
| S075 | https://gitlab.com/Zesko/limine-entry-tool/-/raw/1.40.0/README.md | 2026-10-20 | line 258: “These packages provide hooks to automatically manage kernel installation and removal using `limine-entry-tool`.” |
| S076 | https://gitlab.com/Zesko/limine-snapper-sync/-/commit/754090077de4b5e9de8f09a870ae7301d56dec13 | 2026-10-20 | commit message: “Skip sync when cleanup is active”; CHANGELOG 1.12.0: “Sync runs afterward. (#4)” |

Mutable-field changes (logged old → new): S007 used-by `corpus/knowledge/degraded-triage-r4.md` → `corpus/knowledge/degraded-triage-r4.md, corpus/knowledge/boot-writers-r19.md`; S008 used-by the same old → new. No immutable cell changed. Registry 65 → 76 rows (eleven new, all tier A, status mined).

Outside admit/reject spot-check: pending the orchestrator's separate non-author closure. Swarm seats and this table are author-side.

## Mistakes

| ID | Class | Evidence | Captured-by | Fix shown able to fail |
|---|---|---|---|---|
| R19-SEAT-DECLARE | scope | Fourth consecutive red: round-18 build 37/1/4/2, falsify 9/0/0/2 (`round-18-verifier-spotcheck.md` §5 item 1); round-19 build still 14 EXEC-UNAUTHORIZED + 1 UNDECLARED although each item said NO-EXEC (`python3 tools/check-seat-scope.py --wave .ufo/waves/round-19/build`). Instruction text alone does not stop read-only shell use | QUALITY 24 records deviations; no dispatch rule | QUALITY 31. Falsify wave items carry explicit EXEC-AUTHORIZED read-only command classes. The gate can fail: MutSeatScope's NO-EXEC fixture is red and the always-authorized mutant goes green (killed by the expected-red detector, `build/files/MutSeatScope.txt`); the build wave's red is measured at the landed hash, never re-labelled |
| R19-ADJ-POINTERS | reference-drift | PROVINCE.md cited all ten sibling ownership sources by line range only (`:33`, `:46-52`), violating the lane's own QUALITY 21; mori `PROVINCE.md:66` cites tsukuroi `:21-24,35-44` whose content moved (IN-067) | QUALITY 21, not enforced on PROVINCE | QUALITY 32 and `tools/check-adjacency-anchors.py`: baseline with the target registry is red, 10 ANCHOR-UNPUBLISHED + 114 INBOUND-UNPUBLISHED; selftest wrong-RESOLVES and wrong-DRIFTED fixtures are red |
| R19-REGISTRY-ROW | number-drift | 14 tools, 13 operative rows; `tools/_revision.py` selftest counted but unregistered (closure defect 2) | none | `tools/check-registry-coverage.py --revision 452a054…` exits 1 with REGISTRY-ROW-MISSING `tools/_revision.py` (`build/files/registry-gate-baseline.stdout`); selftest missing/orphan/duplicate rows red |
| R19-BOOT-ATTRIBUTION | attribution | One cleanup write attributed by inference in round 17 (`boot-chain-r17.md:34-36`); the hourly rewrite noted only as an operator note (closure §5 item 6); ExecStopPost absent from the corpus | none | QUALITY 33 and `tools/check-boot-writers.py`: baseline with the target registry is red, 13 EVENT-UNPUBLISHED + 7 WRITER-UNPUBLISHED; selftest extra-unclaimed-line and wrong-signature fixtures red |
| R19-DECLARED-COUNT | number-drift | The round-19 declaration said 0→12 events from a `tail -n 40` pacman.log window; the declared whole-log grep holds a third line (2026-10-11, pacman.log 2021) | QUALITY 30 (whole finite input set) | The gate enumerates its own denominator from declared probe blocks (`events_total` 13); a 12-event registry against the same captures is EVENT-UNATTRIBUTED red. The declaration stands as written; the refinement is appended |
| R19-CENSUS-ENDASH | number-drift | `extract-adjacency-r19.py` v1 accepted ASCII `-` only: IN-073..IN-076 stored as single lines (InClass068) | none | v2 regex accepts en-dash; re-extraction pinned to the v1 tips changes exactly those four records (`adjacency-pointers-r19.v1.json` retained); an unpinned re-run moved 114 → 118 pointers because siblings had committed, so the pin is required |
| R19-CAPTURE-OVERREACH | scope | capture-r19c v1 kept all sudo journal lines; capture A's tag-agnostic journal probe kept 20 operator sudo COMMAND records (ReviewCapturesSafety, MEDIUM) | none | c narrowed before commit; A's 20 records replaced in place by a redaction marker before commit, line count preserved (`grep -c 'COMMAND=' host-capture-r19.txt` → 0 committed). The unredacted bytes exist only in the L1 harness record |
| R19-EXECLOG-BOUND | scope | Round-18 exec-log covered one capture; the S065 pacman.log reads stayed outside (closure §5 item 3) | QUALITY 26 in part | All round-19 L1 host reads ran through `capture-r19{,b,c}.sh`; each capture is checked with `--exec-log`. MutExecLogR19: an injected `pacman -Qi` and a `bash -c 'pacman -Q …'` line each fire EXEC-STEER-VIOLATION, restored file PASS. Bound: one path per run, three runs |
| R19-LOAD-ORDER | process | Round-18 L1 read the canonical files late (closure §5 item 4); round 19 read them first, but only the L1's own statement shows the order (ReviewLoadOrder) | protocol only | No mechanical fix; the bound is stated in the report, not counted as a fix |

## Routed defects from round 18

1. Seat scope: build wave dispatched with explicit NO-EXEC or EXEC-AUTHORIZED per item; still red (14/0/0/1) and reported; falsify wave authorizes read-only inspection in every item. Both waves re-measured at a landed hash.
2. `_revision.py` row: C3 (registry row, kind library).
3. Exec-log scope: every L1 host read is inside the three committed captures; each is checked.
4. Load order: followed first; evidence bound stated.
5. Mori pointers: observed inbound as IN-067 and IN-072 and packaged as `prepared` handoffs; mori files untouched.
6. `/boot` automation: C2 attributes it; QUALITY 33.

## Inherited and non-author files

No uncommitted lane state at dispatch (`jj-lane.sh state`: local=remote 452a054, ahead 0, tracked 0, untracked 0). `round-18-verifier-spotcheck.md` read and untouched. Host safety: no pacman, no sudo, no service action, no /boot read or write; L1 host reads only through the three capture scripts. No tool installed.

## Falsify wave (attempt 2, 72 seats) — findings and repairs

Wave evidence `.ufo/waves/round-19/falsify/`. 72 dispatched, 66 reports, 6 dead by provider 429 (FxCritC1, FxCritCensus, FxOut003, FxInCensusForm, FxWriterClasses, FxConnSiblingWrites), no replacement. 28 prepared attacks unexecuted under the 100-job packing cap.

Admitted after repair (all re-measured PASS at `5a133bcf8782ea731c1a2270ad28d2a2250fd213`):
- C1 gate hardening + published digests: PROVINCE publishes full commit and blob sha256 per anchor; the gate requires id+quote, id+commit, id+sha256 and the heading, and bounds inbound ranges by target length. Seats: FxProvinceSection, FxOut001/002/004/005/006/007/008/009/010, FxExecNegAdj, FxCritC3.
- C2 mechanism prose: every writer mechanism quote is published (appendix) and the gate rejects an unpublished/altered quote. Seats: FxMutWriters, FxQuality33, FxEventTable, FxEvent01/02/03.
- C3 row/verdict integrity: one tool per row, gates publish 0/1/2 (probes 0/2). Seats: FxMutRegistry, FxRevRegistryKinds, FxExecNegRegistry.
- Audit safety: all `/usr/lib/modules` trees count as boot inputs; an unevaluable `EFI/Linux` image is an error, not a non-kernel app. Seats: FxRevAuditRules, FxScoutAuditRules, FxRevBootTable.
- Record corrections: ten inbound `relied_on`/notes (IN-027, IN-039, IN-041, IN-049, IN-052, IN-058, IN-081, IN-085, IN-091, IN-096) and drift qualifications (IN-067, IN-102, IN-104).
- Capture hygiene: capture C redacts the operator user token; registry digest updated.

Refuted and not repaired as claims (bounded residuals, reported): SKILL.md ownership-routing statements are outside C1's PROVINCE scope (FxCritC1Scope); a hex-named ref can alias a non-object revision in `_revision.bind` (FxExecNegRevision; absent in the live lane); the exec-log `forbidden` list does not include `systemctl` (read-only verbs only in the captures; FxCritNoHarm); plymouth's version and the hook bodies were not re-read in round-19 captures (FxScoutHooks, INCONCLUSIVE).

## Mistakes (falsify wave)

| ID | Class | Evidence | Captured-by | Fix shown able to fail |
|---|---|---|---|---|
| R19-F-DIGEST | publication-incomplete | FxProvinceSection/FxOut001-010: table published heading+quote+12-hex only | none (gate checked two of four fields) | PROVINCE digest appendix; gate requires all four; selftest `unpublished-digest` red |
| R19-F-RANGE | gate-blind-spot | FxExecNegAdj: `[[999999,999999]]` passed in a 132-line file | none | range bound + selftest `range-beyond-file` red (2 findings) |
| R19-F-MECH | gate-blind-spot | FxMutWriters: ExecStopPost→ExecStartPost in the entry survived | QUALITY 33 claimed mechanism fidelity | mechanism appendix + MECHANISM-PROSE-MISSING; selftest `mechanism prose missing` red |
| R19-F-ROW | gate-blind-spot | FxCritC3/FxMutRegistry: discovered row masked a missing baseline row; 2→97 verdict code passed | none | one-tool-per-row + 0/1/2 codes; selftests `ambiguous-row` and `incomplete-verdict` red |
| R19-F-AUDIT | safety-input | FxRevAuditRules/FxScoutAuditRules: LTS module tree invisible; unevaluable EFI/Linux image counted not-kernel | none | `/usr/lib/modules` + EFI/Linux error classification; selftest 45/45 keeps the fixture harness |
| R19-F-CAPTUREC | privacy | FxScoutCapture: capture C kept 12 sudo `COMMAND=` records with the operator name | R19-CAPTURE-OVERREACH covered only capture A | redaction + digest update; `grep -c vgpnk` → 0 |
| R19-F-RELIED | paraphrase-drift | FxInRes04/05/06/07/08/09, FxInDriftA: ten `relied_on`/note overstatements | QUALITY 32 checks structure, not paraphrase | corrected records + qualification appendix |
