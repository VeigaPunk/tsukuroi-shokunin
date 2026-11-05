# Round 83 · wave w1 · seat ConnectorScope — sibling overlap and considerthese scan

Read-only. Nothing written outside this file. No sibling, fleet-root, or lane tree was modified. Scratch root `/fast/scratch/hyaku/tsukuroi-r83/ConnectorScope/` was created and is empty (no clones or fixtures). Tool outputs of `_grep` carry no exit code and are marked `tool`.

Excluded from every count: grep hits inside other seats' artifact dumps (file names like `<lane>--corpus__QUALITY.md.blob`, `*.receipt`, `*-narrow.txt`, `*-search.txt`, `*-grep-*.txt`). These are not sibling source and were not verified in the live trees. Example: a "mado QUALITY 137 / round83 C1 receipt" quote came from such a dump; `mado-shokunin/corpus/QUALITY.md` exists but I did not establish that criterion 137 says it.

## 0. Commands and exit codes

| # | Command (abbreviated) | Exit | Result |
|---|---|---|---|
| 0a | `mkdir -p $HYAKU_SCRATCH/tsukuroi-r83/ConnectorScope` | 0 | scratch created, empty |
| 0b | `ls -d /home/vgpnk/Projects/shokunin/*-shokunin/` | 0 | 20 sibling lanes plus tsukuroi. The fleet root also holds a typo dir `kumitate-shokinin/` (no PROVINCE.md); not a lane, not scanned |
| 0c | loop `ls <lane>/PROVINCE.md` over fleet root | (loop) | every lane has PROVINCE.md except the non-lane dirs (`exp-full/`, `research/`, `scripts/`, `templates/`, `tools/`) and the typo dir |
| 1a | `_grep` keyword set over sibling `tools/`, `PROVINCE.md`, `SKILL.md`, `README.md` (tool) | n/a | 29 files matched; first 20 read, remaining 9 not paged (round83-name collisions only, see §1c) |
| 1b | `_grep` `ordinal\|mutation-kill\|anchor-coordinate\|check-anchor` over sibling `tools/*.py`, `tools/*.sh`, `PROVINCE.md` (tool) | n/a | complete output (no paging footer); §1b |
| 1c | `_grep` `systemd\.mount\|mount-unit\|\.mount\b` over sibling `PROVINCE.md`, `tools/`, `corpus/knowledge` (tool) | n/a | complete output; kaidoku oracle TSV hits only (§1d) |
| 1d | `_grep` `check-anchor-coordinates\|check-ordinals\|check-scorecard-ordinals` over sibling `tools/*.py` | n/a | no sibling file of these names; the only hits are tsukuroi's own |
| 1e | `ls mado-shokunin/quality/check-anchor-cover.py tabi-shokunin/scripts/check-gate-mutants.mjs kengaku-shokunin/plans/anchor_*.py mori-shokunin/tools/mori-anchor-check.py` | 0 | all four exist (mado 7304 B; tabi path is `scripts/`, not `tools/`; kengaku `anchor_digest_check.py` and `anchor_line_check.py`; mori 13989 B) |
| 1f | `grep -n "check-anchor-cover\|quality/" mado PROVINCE.md SKILL.md` | 1 | no match: mado's checker is not named in mado's own province or registry |
| 1g | `grep -n "check-gate-mutants" tabi SKILL.md PROVINCE.md` | 0 | hits only in tabi SKILL.md:2549, :2558 (registry row `gate-mutants`); none in PROVINCE.md |
| 1h | `grep -n "mori-anchor-check" mori PROVINCE.md SKILL.md` | 0 | mori PROVINCE.md:547 and SKILL.md:1326 |
| 1i | `grep -n "anchor_line_check\|anchor_digest_check\|round54_c1_anchor" kengaku PROVINCE.md SKILL.md` | 0 | hits in kengaku SKILL.md:612, :631 (other gate), :674, :682, :799, :848; PROVINCE.md hits not printed (the grep combined both files and printed only SKILL.md lines) |
| 2a | `grep -n -i -E "unimplemented\|proposal-only\|proposal only\|not implemented" considerthese/*.md` | 1 | no match. Markers used in the files are "proposals only, not acted on" and similar. Phrase-match was broadened (§2) |
| 2b | `_grep` proposal-marker and proposal-heading scan over `considerthese/*.md` (tool) | n/a | 7 "Self-improvement ideas" sections found, 23 items total |
| 2c | `_grep` key-phrase set over `corpus/QUALITY.md`, `corpus/lessons/*.md`, `SKILL.md` (tool) | n/a | lessons glob had 75 files; first 20 shown per pattern. Results as stated in §2 |
| 2d | `_grep` `PATCH-OFFSET\|patch-offset\|util\.c\|host-build line` over `tools/*`, `corpus/lessons/round-69*.md`, `round-70*.md`, `SKILL.md`, `PROVINCE.md` | tool, "No matches found" | no detector for the patch-offset proposal |
| 2e | `sed -n '1382,1392p' SKILL.md` | 0 | the calibration ledger is a one-off round-10 claim-vs-realized ledger |
| 2f | `sed -n '200,216p' corpus/QUALITY.md` plus numbered-criterion grep | 0 | criteria 103, 108, 110, 112, 115 read in full |
| 3 | `cat MERGE-REPORT.md` (124 lines; `head -150`) and `ls -la` | 0 | read in full |
| 3b | `sed -n '150,400p' MERGE-REPORT.md \| grep -n -i -E "depth\|anchor\|ordinal\|calibrat\|mutation\|timeout\|digest\|coordinate"` | 1 | no match past line 150 (file is 124 lines) |
| 3c | `_grep` `depth\|anchor\|ordinal\|calibrat\|mutation\|digest\|coordinate\|systemd\|mount` over MERGE-REPORT.md (tool) | n/a | hits only at :21, :25, :33 (file titles: overlayfs-mount, mount-errno, plymouth/systemd-hook) |

## 1. Sibling overlap (scope: 20 sibling lanes; read-only)

### 1a. Anchor and mutation instruments in siblings (file-level overlap with this round's C1 and repair surfaces)

| lane:path:line | class | owned by sibling PROVINCE.md? | note |
|---|---|---|---|
| `kengaku-shokunin/plans/anchor_digest_check.py` (gate `anchor-digest-check`, `kengaku-shokunin/SKILL.md:612`; `:799`, `:848`) | anchor + digest | **No.** PROVINCE.md does not name `anchor_digest_check` or `anchor_line_check` (PROVINCE.md:778-783 narrates the r46 anchor-checker repair; :1136 names "Anchor-parser blind spot R82-F1" as retained backlog) | Closest precedent to C1 (digest-bound anchor counter). Different file, different corpus (kengaku SOURCES anchors). Not a conflict; not adopted |
| `kengaku-shokunin/plans/anchor_line_check.py` (gate `anchor-line-check`, `SKILL.md:682`) | anchor | No (as above) | same as above |
| `kengaku-shokunin/plans/round54_c1_anchor.py` (gate `round54-c1`, `SKILL.md:674`) | anchor | No | verifier for kengaku round-54 anchor claim |
| `mori-shokunin/tools/mori-anchor-check.py` (`PROVINCE.md:547`; `SKILL.md:1326`) | anchor, located-line | **Yes**, PROVINCE.md:547 | checks located-line source anchors and quote word counts against a local pin. Mori's own corpus |
| `mado-shokunin/quality/check-anchor-cover.py` (cited `LOG.md:2652`, `SCORECARD.md:2924`) | anchor coverage | **No.** `grep check-anchor-cover` in mado PROVINCE.md and SKILL.md returned exit 1 | exists (7304 B). Ownership gap inside mado; flag to whoever reviews mado, not this round |
| `tabi-shokunin/scripts/check-gate-mutants.mjs` (`tabi SKILL.md:2549`, `:2558`, registry row `gate-mutants`) | mutation-kill | Not named in PROVINCE.md (grep exit 0 but hits only in SKILL.md) | mutation-kill of a gate's own self-test. Method overlap with `tools/mutation-kill-r83.py`; different file, different language |
| `revenger-shokunin/SCORECARD.md:756-1156` and `SKILL.md:446` (criterion N "mutation-killed attribution pair") | mutation-kill (method) | revenger-owned | method-level only |

### 1b. Ordinal instruments in siblings

No sibling has `check-ordinals`, `check-scorecard-ordinals`, or any SCORECARD ordinal-dispute counter. `ordinal` hits in sibling code are positional indices with unrelated subjects:
- `kama-shokunin/tools/round74-province-host-drift.py:140-251`: ordinal-matched host blocks inside PROVINCE.md (kama-owned).
- `mori-shokunin/tools/mori-pin-check.py:628-783`: per-prefix ordinal pin bindings (mori-owned).
- `kotodama-shokunin/tools/assemble-culture-d3.py:209-214` and `check-evidence-coupling.py:1102-1107`: era ordinals in fictional data.
- `kotodama-shokunin/tools/check-paragraph-locator.py:197-199`: quote-occurrence ordinal.

None reads a SCORECARD block or disputes a `(round, axis)` score.

### 1c. round83 name collisions (not the same surface)

Round-number labels only: `kama tools/round83-pending-falls.py`, `round83-pin-rechecks.py` (kama PROVINCE.md:393, :398; `kama tools/pre-report-gate.py:261, :344`); `kaidoku tools/round-83/attribution-audit.py`, `source-bind.py`, `outer-cli-fixtures.py` (kaidoku SKILL.md:1972-1974); tameshi tool comments citing round-83 controls; `kake PROVINCE.md:673-675` (`.ufo/waves/round-83/c83_drift_class.py`); `mori PROVINCE.md:640-641`; `kengaku PROVINCE.md:1134`. None is an anchor or ordinal instrument.

No sibling file carries the names `check-anchor-coordinates*`, `check-ordinals*`, `check-scorecard-ordinals*`, or `mutation-kill*`. The round's names are unique in the fleet.

### 1d. systemd.mount / mount-unit / fstab

No sibling `systemd.mount` or mount-unit surface. Hits are non-systemd:
- `kaidoku-shokunin/tools/round-50/oracle/c6430.oracle.tsv:701` and `c6490.oracle.tsv:736`: `etc/init.d/rc.mount.sh`, an OpenWrt init script in a firmware oracle.
- kaidoku evidence oracle TSVs: `etc/fstab` firmware-file names.

Tsukuroi's own mount-unit plane (`corpus/knowledge/mount-unit-fstab-plane-r81.json`) has no sibling counterpart.

### 1e. Ownership summary for the L1
- No sibling owns a surface this round's C1 or C2 touches. No file name collides.
- Concept-level precedent exists in kengaku (`anchor_digest_check.py`) and mori (`mori-anchor-check.py`), each owned by its own lane.
- mado's `check-anchor-cover.py` is not named in mado's PROVINCE.md or SKILL.md. Ownership is unclear there; not this lane's to resolve.

## 2. considerthese scan (read-only)

Files: `considerthese/2026-10-19.md` … `2026-10-26.md` (7 files, 210 lines; `swarm-registry.json` is not a proposal). Each file has a "Self-improvement ideas (proposals only / not acted on)" section. 23 items in total.

Status key: **impl** = implemented, with criterion or section; **partial** = rule exists, instrument absent; **open** = no implementing text found.

| # | proposal (file:line) | status | evidence (criterion or section) |
|---|---|---|---|
| 1 | Daily pin-integrity check (2026-10-19.md:32) | open | no phrase match in QUALITY/lessons/SKILL |
| 2 | Draft-PR awareness with pin warnings (2026-10-19.md:43) | open | no phrase match |
| 3 | Author-versus-verifier calibration ledger (2026-10-20.md:47) | open in the specified form | no per-round running agreement-rate record. SKILL.md:1382 is a one-off ten-round claim-vs-realized ledger. Lessons carry prose verdicts ("discernment: improved", "agrees with the gate") without a count |
| 4 | Daily source-quote sampling (2026-10-20.md:50) | open | no phrase match; needs network re-open |
| 5 | Signal-first review path (2026-10-20.md:53) | open | no phrase match |
| 6 | Missed-run catch-up (2026-10-22.md:18) | open | no phrase match |
| 7 | Scope-violation trend line (2026-10-22.md:19) | open | no phrase match |
| 8 | Verified-rate ledger (2026-10-23.md:17) | open | no phrase match |
| 9 | Round-velocity awareness (2026-10-23.md:18) | open | no phrase match |
| 10 | Upstream release watch (2026-10-24.md:17) | open | no phrase match; adjacent to QUALITY 8 (`on-release` cadence) |
| 11 | Routed-debt carry-over check (2026-10-24.md:18) | open | no phrase match |
| 12 | Seat-loss tally (2026-10-24.md:19) | open | no phrase match. QUALITY 110 covers seat harm, not seat loss |
| 13 | Live-harm flag for env changes (2026-10-24.md:20) | open | no phrase match |
| 14 | Claim-arc length (2026-10-24.md:21) | open | no phrase match |
| 15 | Quiet-day mode (2026-10-25.md:17) | open | no phrase match |
| 16 | Next-round pickup sheet (2026-10-25.md:18) | open | no phrase match |
| 17 | Probe lineage table (2026-10-25.md:19) | **impl** | SKILL.md:3496 "Counter lineage — rounds 35-40" cites "considerthese/2026-10-25.md proposal 'Probe lineage table', item F-5"; extended at SKILL.md:3823 and :3928 |
| 18 | Evidence-weight watch (2026-10-25.md:20) | open | no phrase match |
| 19 | Burst-aware reading (2026-10-26.md:17) | **impl** | QUALITY 112 "Burst-aware reading starts with outcomes, not volume" |
| 20 | Counter-attack scoreboard (2026-10-26.md:18) | **impl** | QUALITY 115 (R82-SCOREBOARD), cites considerthese/2026-10-26.md |
| 21 | Seat-harm incident log (2026-10-26.md:19) | **impl** | QUALITY 110 (R79-SEAT-HARM-LOG), "the lane's adoption of … 'Seat-harm incident log'" |
| 22 | Downstream patch-offset check (2026-10-26.md:20) | **partial** | QUALITY 103 (R69-PATCH-OFFSET) states the rule. No detector: the grep for PATCH-OFFSET / patch-offset / util.c / host-build line returned nothing in `tools/`, the round-69/70 lessons, SKILL.md, or PROVINCE.md |
| 23 | Cross-note correction propagation map (2026-10-26.md:21) | **impl** | QUALITY 108 (R75-CORRECTION-PROPAGATION), "the lane's adoption of the considerthese/2026-10-26.md proposal" |

Totals: 5 implemented (17, 19, 20, 21, 23); 1 partial (22); 17 open.

Note on the item-level grep: `grep -i -E "unimplemented|proposal-only|proposal only|not implemented"` (§0, 2a) returned exit 1. Strictly, no file marks a proposal as unimplemented. The "proposals only, not acted on" marker is the closest equivalent, and the table above applies it.

### 2b. The one still-open proposal that fits this round's claims

**Pick: #22 "Downstream patch-offset check" (`considerthese/2026-10-26.md:20`), status partial.**

- **Why it fits depth/anchors.** The proposal flags knowledge anchors that cite upstream line numbers for code the host runs as a patched build, so line pins stop drifting silently. That is line-coordinate exactness, the surface C1 measures. Source: "Round 40 found an Arch patch shifts util.c lines after :675 by +5."
- **Why it is not absorbed by C1.** C1's frozen legs measure digest-bound anchor coordinates against a committed snapshot. The patch-offset check needs a host-build measurement (the installed package bytes versus upstream tag), which is outside the frozen legs and would need its own declaration. Do not re-scope C1 to include it.
- **Gap confirmed.** QUALITY 103 is the rule. No tool in `tools/`, no SKILL or PROVINCE mention, no lesson instrument.
- **Rejected alternative.** #3 "Author-versus-verifier calibration ledger" is open and sits on the calibration axis, but it measures author-versus-outside verdict agreement, not positional ordinals. It does not fit C2's `check-ordinals` retirement logic.

## 3. Shared-knowledge package (read-only)

`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/MERGE-REPORT.md` (124 lines, read in full; `ls` exit 0). It is a staged corpus-expansion package (147 rows, 70 knowledge entries) from `corpus-expansion-1`, unadopted; the header states "Nothing was written into the lane repo."

- No theme matching depth-anchor or calibration-ordinal work. The keyword pass (§0 3b, 3c) hit only file titles: `:21` overlayfs-mount-contract-r25, `:25` mount-errno-contract-r26, `:33` plymouth/systemd-hook-cjk-r27. None concerns anchors, ordinals, calibration, or digests.
- The package's staged rows are round 1–16 world knowledge (initramfs, pacman hooks, errno, btrfs, zh/ja translations). No anchor counter, ordinal instrument, or mutation-kill item.
- Nothing copied or adopted.

## 4. Verdict

- Sibling overlap: no file-name or surface collision with this round's instruments. Concept-level precedent in kengaku (`anchor_digest_check.py`, `anchor_line_check.py`) and mori (`mori-anchor-check.py`). Mado's `check-anchor-cover.py` has an ownership gap in mado's PROVINCE.md and SKILL.md. Tabi's `check-gate-mutants.mjs` is the mutation-kill analogue.
- considerthese: 23 proposals; 5 implemented, 1 partial, 17 open. One still-open pick that fits the depth-anchor axis: #22, patch-offset detector, not for this round.
- merge package: no matching theme.
- Refused: nothing. Unrun checks: the remaining 9 of 29 files in the broad sibling keyword grep (§0 1a) were not paged; the 55 unread lessons in the key-phrase grep (§0 2c) were not paged. Neither set changes any verdict above, since the narrower greps (1b, 1c, 1d, 2d) were complete.
