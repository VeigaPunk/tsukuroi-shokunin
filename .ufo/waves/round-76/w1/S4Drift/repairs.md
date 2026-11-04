# S4Drift — C2 prose repairs

Status: draft-only; no product file edited by this seat. During inspection, all three errata, criterion 109 and S322 were already present in the shared working tree. Do not append duplicates. The blocks below are integration candidates against the pre-repair anchors, not evidence that this seat landed them. All lane file paths below are absolute. All three errata and criterion 109 are append-only. S322 is a new registry row inserted after S321, preserving every existing line.

## 1. journal-boot-plane.md

File: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/journal-boot-plane.md`
Insertion anchor: after pre-repair EOF line 468 (now immediately before the existing round-76 erratum):

> Record observed values and unresolved questions separately. Uncaptured pending updates, signature validity, exact foreign/orphan classification, private mount views, historical provenance events and recovery feasibility remain unknown until their own authorized evidence is obtained. No installation, restart, rebuild, subvolume action or boot write is authorized.

Append-only candidate:

```markdown
## Round-76 erratum — journald retention configuration (append-only)

**R76-JD-CONFIG-DRIFT.** This supersedes §1.1's lines 51–52, "Rotation policy not proven" and "effective defaults not derived", and §11's lines 362–363, "Effective journald retention (`SystemMaxUse`, rotation date of boot −12): shipped config is defaults-only; effective value not derived", as claims about current configuration. The merged configuration includes `/etc/systemd/journald.conf.d/size.conf` with `SystemMaxUse=256M`; the derived system limits are `effective_limit=256M` and `SystemMaxFileSize=32M`. Evidence: `.ufo/waves/round-76/before/host.txt` (`systemd-analyze cat-config systemd/journald.conf`, `journalctl --disk-usage`, observed 148.6M), with derivation in `corpus/knowledge/journald-retention-plane-r76.md`, "Effective limits on this host". These current limits do not recover the rotation date of historical boot −12. Old lines remain as dated evidence. Recheck: `systemd-analyze cat-config systemd/journald.conf` and `journalctl --disk-usage`; cadence: each round touching this plane and after journald configuration changes.
```

## 2. degraded-triage-r4.md

File: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/degraded-triage-r4.md`
Insertion anchor: after pre-repair EOF line 667:

> Round-39 clarification (TO1, TO8): these hooks are PostTransaction hooks; they run after `transaction completed` is logged, within the same `pacman` command but not inside the logged `transaction started`…`completed` window, and none of them runs if the commit is interrupted or fails (`trans.c:230-239`, HO6); their output is logged as `[ALPM-SCRIPTLET]`. It qualifies the "in the transaction" / "in-transaction" / "in one transaction" wording above. Source: `corpus/knowledge/pacman-transaction-order-r39.md` TO1, TO8 (S216, S217).

Append-only candidate:

```markdown
## Round-76 erratum — J2 retention claim (append-only)

**R76-JD-CONFIG-DRIFT.** This supersedes line 70's J2 claim "no retention policy configured anywhere (merged coredump/journald conf = defaults only)" for current journald configuration. `/etc/systemd/journald.conf.d/size.conf` sets `SystemMaxUse=256M`; the derived system limits are `effective_limit=256M` and `SystemMaxFileSize=32M`. `.ufo/waves/round-76/before/host.txt` captures the merged configuration and `journalctl --disk-usage` reading 148.6M; `corpus/knowledge/journald-retention-plane-r76.md`, "Effective limits on this host", derives those limits. J2's old 3.9 G reading is historical; the journal reading does not measure stored coredump files or establish current coredump retention policy. Old lines stay. Recheck: `systemd-analyze cat-config systemd/journald.conf` and `journalctl --disk-usage`; cadence: each round touching this plane and after journald configuration changes.
```

## 3. boot-plane.md

File: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/boot-plane.md`
Insertion anchor: after pre-repair EOF line 318:

> supersedes the pointer-only recheck: line above.

Append-only candidate:

```markdown
## Round-76 erratum — effective journald retention (append-only)

**R76-JD-CONFIG-DRIFT.** This supersedes §1.4's lines 79–80, "effective journald retention not derived (round-3 open item)", and §6's line 240, "Effective journald retention beyond the 13 retained boots", insofar as they leave current size limits unknown. `/etc/systemd/journald.conf.d/size.conf` sets `SystemMaxUse=256M`; the derived system limits are `effective_limit=256M` and `SystemMaxFileSize=32M`. Evidence: `.ufo/waves/round-76/before/host.txt` and `corpus/knowledge/journald-retention-plane-r76.md`, "Effective limits on this host". A size budget does not guarantee a retention duration or reconstruct missing historical boots. Preserve the old lines as the earlier observation. Recheck: `systemd-analyze cat-config systemd/journald.conf` and `journalctl --disk-usage`; cadence: each round touching this plane and after journald configuration changes.
```

## 4. QUALITY criterion 109

File: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md`
Insertion anchor: after criterion 108, line 211, followed by its blank line 212. Exact last line to append after is blank line 212; the preceding criterion ends:

> Shown able to fail: the sweep itself returns non-zero lines for all three corrected propositions, and the map names the two carriers the round-74 records never mentioned (`.ufo/waves/round-74/w1-spec.json`, `w1-dispatch.json`).

Criterion 109 already occupies line 213; do not create a second 109. Append-only candidate, preserving the lane's command/count evidence rule without claiming an unrun gate:

```markdown
109. **A negative host-state claim names its recheck command and cadence, and the round-start host probe re-runs the ones its plane touches (R76-JD-CONFIG-DRIFT):** a knowledge claim that a host surface has no configuration, policy, writer or value carries the exact read-only `recheck` command and cadence beside the claim; the round-start host probe re-runs those claims whose plane it touches and records each command and observed result, with a count of claims checked and changed rather than an unsupported "all clear". Changed readings land as appended errata naming the superseded text. Red: `degraded-triage-r4.md:70` said "no retention policy configured anywhere", but the round-76 receipt shows `/etc/systemd/journald.conf.d/size.conf` setting `SystemMaxUse=256M`. Recheck for this surface: `systemd-analyze cat-config systemd/journald.conf` and `journalctl --disk-usage`; cadence: each round touching journald and after journald configuration changes. Evidence and mistake: `corpus/lessons/round-76.md`, `R76-JD-CONFIG-DRIFT`; host readings: `.ufo/waves/round-76/before/host.txt`. A stated total is admitted only beside its counting command and observed output.
```

## 5. SOURCES S322

File: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`
Insertion anchor: after line 332, the exact S321 row:

```markdown
| S321 | systemd v262 journalctl(1) — https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | docs | A | journalctl vacuum and disk-usage semantics for v262 | journalctl.xml at v262, lines 941-983 (disk-usage, vacuum-size/time/files, rotate); sha256 d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd | --vacuum-size deletes the oldest archived files until their disk use falls below the size; --disk-usage includes active files; --rotate archives active files first | mined | 2026-11-04 | on-release | corpus/knowledge/journald-retention-plane-r76.md |
```

S322 already occupies the next line. Candidate (11 cells; no internal cell pipes; same upstream URL and v262 provenance as S314, with graceful-helper ranges added to cover the scoped correction):

```markdown
| S322 | systemd v262 src/core/transaction.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/core/transaction.c | code | A | Scoped restart propagation correction to S314 | transaction.c at v262, lines 800-881 (transaction_activate), 1143-1217 (pull-in classes and PROPAGATE_STOP), 1220-1247 (graceful branch), and 999-1027 (graceful helper); sha256 c1c704bb4330ffee5203980219adf1ff1e11402a4a02092f471129ff7c5df2f3 | supersedes S314 — restart propagation only as try-restart is scoped to the PROPAGATE_STOP branch at 1199-1217; the graceful UNIT_ATOM_PROPAGATE_STOP_GRACEFUL branch calls the helper at 999-1027, which may enqueue a direct JOB_RESTART when a JOB_START already exists in the transaction, so the unqualified statement is over-broad | mined | 2026-11-04 | on-release | corpus/lessons/round-76.md |
```

S314 row read at line 325. Source checked directly: frozen round-75 `transaction.c:1199-1217`, `:999-1027`, `:1220-1247`. `:1015-1019` handles JOB_START by assigning JOB_RESTART; `:1228-1234` calls the helper then enqueues its result. This draft alone does not satisfy item 1: the lesson must also carry `R76-S314-SUPERSEDE`, S322 and a supersede verb in its 81-line token block.

## 6. SCORECARD axes restatement

**not needed** under this assignment's condition. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:6212-6230` already has `## Round 75 — axes table restated`; lines 6221–6226 name all six axes: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. Each carries a backticked command (depth: `python3 tools/count-jt-rows-r75.py --revision <REV>`; freshness: `python3 tools/check-r74-routed-r75.py --revision <REV>`). This is evidence of the requested textual shape, not a claim that those commands were re-run by this seat or measure round 76.

## Superseded-text grep evidence

Exact specialized grep invocation performed (not a shell command):

```json
{"pattern":"Rotation policy not proven|Effective journald retention|no retention policy configured anywhere|effective journald retention not","path":"/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/journal-boot-plane.md;/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/degraded-triage-r4.md;/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/boot-plane.md","case":true,"gitignore":false,"skip":0}
```

Observed original matches: journal-boot-plane.md:51 and :362 (continuations :52 and :363); degraded-triage-r4.md:70; boot-plane.md:79 (continuation :80) and :240. Existing appended correction matches also appeared at :472, :669/:671, and :322 respectively. EOF reads established the insertion anchors above.

## Checker scope and limits

Read, not executed: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-r75-routed-r76.py:11-31,112-130,185-206`. Each proposed erratum puts `R76-JD-CONFIG-DRIFT`, the size.conf path, `SystemMaxUse=256M` and `supersedes` together within the first token line, well within the token-plus-80-line window. Criterion 109 includes `round-76.md`, `recheck` and `cadence`. S322 puts `supersedes S314 —` first in teaches and names both PROPAGATE_STOP and graceful. These are static drafting observations, not a checker PASS. L1 must integrate only necessary differences, preserve append-only history, check adopted sentences against sources (QUALITY 91), and obtain the final committed-revision receipt.
