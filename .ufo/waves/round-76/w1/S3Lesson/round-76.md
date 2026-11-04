# Round 76 — journald retention, routed repairs, and negative-claim drift

Draft for L1 integration; not a claim of committed closure. Declaration: `d5f0565bfb42a405ec024d8a5b0796514fb92002`; base: `865b38c96c23ec0bcace8ca3ee884f860693ce43`. Axes: C1 depth (8, tied lowest), C2 freshness (9); source census and the drift mistake are frontier duties, not another claim. Source snapshots and prior receipts were read, not re-executed by this scribe.

## Gate

All four sources were opened this round, accessed 2026-11-04; the pinned local snapshots were opened again for this draft. The round-start sources census reads exit 0 per the assignment; `before/census-start.txt:47` records `tsukuroi ok`. That receipt has no command or exit-code header, so this is attributed evidence, not this seat's execution. Duplicate-URL warnings remain visible. All `before/` paths below mean `.ufo/waves/round-76/before/`.

| Source | URL | Access date | Located quote (≤25 words) | Disposition |
|---|---|---|---|---|
| S318 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journald.conf.xml | 2026-11-04 | `journald.conf.xml:87`: “storage, all log data received will be dropped” | mined → `corpus/knowledge/journald-retention-plane-r76.md` |
| S319 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-config.c | 2026-11-04 | `journald-config.c:26`: `#define DEFAULT_RATE_LIMIT_BURST    10000` | mined → `corpus/knowledge/journald-retention-plane-r76.md` |
| S320 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c | 2026-11-04 | `journald-manager.c:170`: `space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use);` | mined → `corpus/knowledge/journald-retention-plane-r76.md` |
| S321 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | 2026-11-04 | `journalctl.xml:944`: “usage of all archived and active journal files.” | mined → `corpus/knowledge/journald-retention-plane-r76.md` |

Locations refer to `before/src/`; `SOURCES.json` and `SHA256SUMS` bind URL/tag/digest. Reproduction command (not run here): `sha256sum -c /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/before/src/SHA256SUMS` from that snapshot directory. Declaration `SCORECARD.md:6264-6274` attributes the original four successful digest checks.

## Search log

Question: what are journald v262's storage, size, rotation, rate-limit and vacuum rules?

Searched the four pinned snapshots: `journald.conf.xml`, `journald-config.c`, `journald-manager.c`, `journalctl.xml`. Screened 4, included 4, excluded 0, counted by the four named entries in `before/src/SOURCES.json`, not by web-search hits. Reproduction command (not run here): `jq 'keys | length' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/before/src/SOURCES.json` (4); the Gate's four mined dispositions account for included/excluded counts. Stop rationale: documentation supplies storage/rotation/vacuum semantics, compiled definitions supply defaults, and manager code supplies the space clamp/startup patch; no additional source is needed to locate those rules. This is a bounded search, not a claim of exhaustive upstream review.

Held-ground novelty comes from `before/held-ground.txt` and `SCORECARD.md:6252-6262`: the base's symbol sweep has no hits for the retention-rule vocabulary, while near-token hits are historical host observations or coredump rules. The declaration records the exact `git grep -nE` sweep and its exit 1. Do not treat the mechanical JD counter as understanding evidence.

Assimilation: **none**; the `merge/tsukuroi/` package stays quarantined under the open round-75 L0 id-drift question. Nothing is adopted.

## Mistakes

- **R76-JD-CONFIG-DRIFT** · class: a negative host-state claim survived roughly 70 rounds because no criterion required re-running it · evidence: “no retention policy configured anywhere” at `corpus/knowledge/degraded-triage-r4.md:70`; `/etc/systemd/journald.conf.d/size.conf`, born 2026-10-16 11:53:47 -03, sets `SystemMaxUse=256M` (`SCORECARD.md:6276-6278`; merged-config receipt `before/host.txt:60-64`). The approximate age is round distance, not a timed measurement. Captured-by: **none** — the corpus rule required a sweep at write time, not a recheck cadence · fix: QUALITY 109 plus appended errata on `journal-boot-plane.md`, `degraded-triage-r4.md`, and `boot-plane.md`. The recorded host commands are `systemd-analyze cat-config systemd/journald.conf` and `journalctl --disk-usage` (`before/host.txt:7,66`); the receipt has no birth-stat command, so birth provenance is the declaration, not a fabricated stat receipt. Effective-limit derivation is in the new note; 148.6M is an observed disk-usage capture, not a promised bound or a measurement of coredump storage.
- **R76-JD-CLAMP-WORDING** · class: frozen prose/source-formula conflict · evidence: the declaration says “used space plus the smaller of free space and `keep_free`”; `journald-manager.c:168` instead reads `avail = LESS_BY(vfs_avail, metrics->keep_free);` and `:170` reads `space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use);` · captured-by: this seat's located source read, not a checker run · fix: preserve the frozen sentence as historical evidence and route the discrepancy to L1/source reviewers for explicit disposition; no claim is silently weakened and no instrument is changed by this scribe. This row records a finding, not an adjudicated failure.

### R76-S314-SUPERSEDE

S322 supersedes S314's unqualified restart-propagation clause. The “only as try-restart” sentence applies to the `PROPAGATE_STOP` branch; the graceful branch (`PROPAGATE_STOP_GRACEFUL`) can enqueue a direct `JOB_RESTART` when `JOB_START` is already queued. `corpus/SOURCES.md:333` carries the append-only supersede row. S314 remains the original record, not the current unqualified rule.

### R76-JT5-COUNT

Supersedes the round-75 note's “nine comma items” count: JT5 has **eight comma-separated items**, but **ten labels**. Split method: split the statement after its colon on commas; then split the two compound items on the conjunction joining separate labelled steps: “a second collection and redundant drop” and “the destructive check and apply”. The original eighth label is spelled “Eights step”, so searching only “Eighth” is not an enumeration method. Correction: `corpus/knowledge/systemd-job-transaction-plane-r75.md:107-120`.

Count reproduction command (not run here): `python3 -c 'from pathlib import Path; p=Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/systemd-job-transaction-plane-r75.md"); row=next(s for s in p.read_text().splitlines() if s.startswith("| JT5 |")); items=row.split("|")[2].split(":",1)[1].split(","); print(len(items), len(items)+sum(" and " in s for s in items))'` → expected 8, 10. The upstream label locations are enumerated at the note's lines 98-103; this command counts the prose/split method, not execution steps.

### R76-R75-MISTAKE-COUNT

Supersedes the closure's conflated mistake total: round-75 has **five** rows in `## Mistakes`, plus **two owed** rows under `## Owed to the next round`. The five are `R75-DECL-PROPAGATE-SCOPE`, `R75-QUOTE-LEADER`, `R75-C2-LINEBREAK`, `R75-COUNTER-NONREADER`, `R75-WAVE-SIZE` (`corpus/lessons/round-75.md:55-80`). The two owed are `R75-JT2-REFRESH` and `R75-JT5-ENUM` (`:135-143`); their placement is not rewritten to retrofit the earlier count.

Count reproduction command (not run here): `python3 -c 'from pathlib import Path; t=Path("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-75.md").read_text(); a=t.split("## Mistakes",1)[1].split("\n## ",1)[0]; b=t.split("## Owed to the next round",1)[1]; print(sum(s.startswith("- **R75-") for s in a.splitlines()),sum(s.startswith("- **R75-") for s in b.splitlines()))'` → expected 5, 2.

### R76-R75-RECEIPT-REPOINT

Supersedes receipt attribution to `e5f5ca9e` for final round-75 evidence: `before/recheck-r75-at-tip.txt:1-11` names `bd0acc44` (`bd0acc444cd6c82823602ed7a49bd1ef11360d2d`). It records `count-jt-rows-r75.py --revision bd0acc44` → `JT_ROWS=6 JT_VERIFIED=6 JT_SOURCES=3 JT_SNAPSHOTS=3 JT_MALFORMED=0 met=1`, rc 0; and `check-r74-routed-r75.py --revision bd0acc44` → `ROUTED_STALE=0 ROUTED_OK=4/4`, rc 0. These are the captured producer command labels; this scribe did not run either instrument, and the receipt does not expose a full shell invocation.

### R76-WAVE-MARKERS

Supersedes treating untracked marker presence as committed closure. The carried paths are `.ufo/waves/round-66/w1.ready.dispatched`, `.ufo/waves/round-67/w1.ready.dispatched`, `.ufo/waves/round-73/w1-run.stderr`, `.ufo/waves/round-73/w1.ready.dispatched`, `.ufo/waves/round-74/w1.ready.dispatched`, `.ufo/waves/round-75/w1.ready`, and `.ufo/waves/round-75/w1.ready.dispatched`. `w1/E5MarkerAudit/markers.txt:2-8` records seven regular files absent at base, not committed-at-final evidence. Reproduction command (not run here): `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree -r --name-only <FINAL_REV> -- .ufo/waves/round-66/w1.ready.dispatched .ufo/waves/round-67/w1.ready.dispatched .ufo/waves/round-73/w1-run.stderr .ufo/waves/round-73/w1.ready.dispatched .ufo/waves/round-74/w1.ready.dispatched .ufo/waves/round-75/w1.ready .ufo/waves/round-75/w1.ready.dispatched`; all seven paths must appear. L1 supplies the final revision and result.

### R76-QUALITY-WORDING

Supersedes the over-broad quality claim with: **no admitted knowledge entry is left failing its own re-check**. This does not assert that every repository gate is green, that historical evidence was rewritten, or that this seat executed every note's re-check. Final closure must establish the narrowed sentence from the appropriate receipts rather than infer it from this paragraph's tokens.

## Correction propagation map

Round-76 proposition: the old defaults-only/no-retention-policy host claim is stale; the current merged journald config has the size.conf drop-in. Locations below are working-tree observations during drafting, not final-commit bindings.

| Carrier and location | Disposition | Scope |
|---|---|---|
| `corpus/knowledge/journal-boot-plane.md:51-52,362-363,373` | standing as falsified record | Historical all-commented/defaults-only and unresolved-limit wording; not current config evidence. |
| `corpus/knowledge/journal-boot-plane.md:470-472` | corrected | Appended R76-JD-CONFIG-DRIFT supersedes the old effective-limit claim. |
| `corpus/knowledge/degraded-triage-r4.md:70,276-285,544-545` | standing as falsified record | Original J2 and carried unknown; the journald correction does not establish coredump retention. |
| `corpus/knowledge/degraded-triage-r4.md:669-671` | corrected | Appended correction names size.conf and SystemMaxUse=256M. |
| `corpus/knowledge/boot-plane.md:79-80,240` | standing as falsified record | Original unresolved-limit wording; historical boot inventory remains a dated capture. |
| `corpus/knowledge/boot-plane.md:320-322` | corrected | Appended derivation pointer; no reconstruction of lost older boots claimed. |
| `corpus/README.md:13` | historical evidence | Round-3 index still describes effective retention as an unknown in that historical note; this map supplies the correction pointer. |
| `corpus/knowledge/oom-event-plane.md:189-190` | historical evidence | Dated all-commented/no-drop-in observation, not a current no-policy assertion; no causal loss conclusion is re-derived here. |
| `SCORECARD.md:6257-6262,6276-6281` | historical evidence | Explicitly records the old claim and new host capture; not an independent new reading. |

`SKILL.md` was searched with `defaults.only|retention policy|effective journald|retention.*derived|no retention|round-76|size.conf` (case-insensitive); no matching line was returned. Therefore no invented `file:line` is supplied for a repeated SKILL claim. This bounded negative search is not an exhaustive semantic audit. The base sweep and this working-tree search have different purposes and revisions.

## Attack ledger

L1 integration placeholder requested by the seat contract: insert the attack seats' final report rows and their exact commands, revision/digest bindings, outcomes, survivors and named limits. No seat's contract-only assignment constitutes execution evidence. This scribe observed the clamp wording/source discrepancy in Mistakes; it makes no final C1/C2 judgment. The frozen checker tests persistence/tokens; passing it alone cannot establish repair truth.

## Owed to the next round

L1 integration placeholder requested by the seat contract: replace this line with final attack-seat debt dispositions before publication; preserve unresolved items rather than invent closure.

- The open round-75 L0 id-drift question keeps `merge/tsukuroi/` quarantined; no assimilation credit.
- Carry forward the round-75 token-dump/non-reader limitations and anchor-widening debt unless final attack evidence actually closes them.
- Apply QUALITY 109's negative-host-state recheck cadence to future reuse; the write-time sweep alone did not catch size.conf drift.
- Resolve the exact clamp-formula conflict without altering the frozen claim in place; record the canonical disposition and any correction append-only.
- L1 supplies final attack reports, committed marker proof, final corpus census command/receipt, final claim measurements and the admission decision. These are integration obligations, not claimed completed results or silently deferred end-to-end acceptance.
