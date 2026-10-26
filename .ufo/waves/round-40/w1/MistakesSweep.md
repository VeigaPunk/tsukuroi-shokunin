VERDICT: defect-found

# MistakesSweep — Item M-1: candidate mistakes of rounds 37-39 not yet in a `## Mistakes` table

seat `MistakesSweep` (L2 scout, leaf) · 2026-10-26 · lane tip `f951f288483c1af0cef4afd458488b84cf7a2165` · read-only on lane
content; wrote only this file and `.ufo/waves/round-40/w1/MistakesSweep/` (`sweep-commands.txt`, `repro-mounts-at-tip.txt`).
No tool installed, no sudo, no pacman, no host change, no signal sent, no subagent. Scratch
`/fast/scratch/hyaku/tsukuroi-r40/MistakesSweep/` used for four fixture mount tables and removed.

**Result.** 25 round-39 wave reports carry `falsifies`/`defect-found`; the round-37/38/39 lessons hold 23 recorded rows
(R37: 5, R38: 11, R39 table: 7 — list in §1). I found **18 further candidates** (§3): **9 open at the lane tip** (Tier A, 1-9),
**9 closed in-round or by the closure but never given a row** (Tier B, 10-18 — except 13, which is open and repeats in round 40,
and 16/17, which are partly open/unverified). I re-checked at the tip myself: 1 and 2 (census runs), 3 (line 261), 4 and 6
(git), 13 and 16 (greps); the rest cite a seat report and say so. `R39-CONTROL-NO-RED-CHANNEL` was mined by a prior seat but
never promoted to a row (§2).

## 0. Sweep commands (also in `MistakesSweep/sweep-commands.txt`)

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
ls corpus/lessons | grep -E 'round-3[789]'
grep -rn '^## Mistakes' corpus/lessons/*.md
grep -rhoE '^\| (R3[6-9]|R40)-[A-Z0-9-]+' corpus/lessons/ | sort | uniq -c
git grep -ohE 'R(39|40)-[A-Z0-9][A-Z0-9-]+' -- . ':!.ufo/waves/round-39/w1' ':!.ufo/waves/round-40/w1' | sort | uniq -c | sort -rn
(cd .ufo/waves/round-39/w1 && grep -H -m1 '^VERDICT' *.md | grep -E 'falsifies|defect-found')
# state at tip
grep -n 'PROC_MOUNTS=' tools/tsukuroi-census.sh ; grep -n 'b.\"--revision\"' tools/check-revision-binding.py
git log --format='%h %cI' -S'Round 39 — declaration (2026-10-26T06:20Z' -- SCORECARD.md
git log --format='%h %cI' -S'Round 39 — hyaku run 8, 2026-10-26T07:45Z' -- LOG.md
for r in a2d7aad7 a6ca8171 53b294a2 f951f288; do git ls-tree -r --name-only $r -- corpus/lessons | wc -l; done
python3 tools/check-self-assessment.py --revision f951f288483c1af0cef4afd458488b84cf7a2165
grep -c 'Scope: executed' .ufo/waves/round-40/w1-spec.json ; grep -c S217 corpus/knowledge/pacman-hook-order-r38.md
```

Observed (tip `f951f288`): `tools/tsukuroi-census.sh:462-463` `BTRFS_SYSFS=${TSUKUROI_BTRFS_SYSFS:-…}` /
`PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS:-…}`; `tools/check-revision-binding.py:261` `if b'"--revision"' in body.stdout:`;
`93fddb2 2026-10-26T02:59:31-03:00` (heading says 06:20Z = 03:20-03); `eeba342 2026-10-26T03:35:44-03:00` (heading says 07:45Z =
04:45-03); lessons dir 54 / 54 / 55 / 55 files; self-assessment `checked 27, mismatches 6 (K07 K08 K09 K10 K13 K17)`;
`Scope: executed` 0 hits in `.ufo/waves/round-40/w1-spec.json`; `S217` 0 hits in `pacman-hook-order-r38.md`.

## 1. Already recorded (do not re-add)

| Recorded ID | Table | Wave/closure evidence that matches it |
|---|---|---|
| R37-STALE-SELFASSESS-COUNTS, R37-ROLE-TAXONOMY-MISMATCH, R37-C2-COUNTER-REFERENCE-DRIFT, R37-MISROOT-NOTE-DRAFT, R37-SEAT-REPORT-COUNT | `round-37.md` (`:30-54`, `:99-103`) | — |
| R38-QUALITY-UNREAD, R38-REGISTRY-LAG, R38-ECHO-UNVALIDATED, R38-ANCHOR-SHIFT, R38-ABSENT-ROOT, R38-Q82-LEAK, R38-CLOSURE-DISAGREEMENT, R38-STREAK-SURVIVOR/-VACUOUS/-ATTRIBUTION/-LANDING | `round-38.md:80-95` | R38-STREAK-LANDING already holds the round-37 duplicate correction block and the twice-amended counter |
| R39-CONTENT-UNREAD | `round-39.md:66` table | C2CritAxis §A, C2CritControl V1-V3/V7 — **only the rule-cell half** (see candidate 9) |
| R39-FIXTURE-MONOCULTURE | same | C1CritControl VA-VC/VG, C1MutParse (a)(b), C1MutCrossCheck (d)(e) — **not** C1DetectHonest (candidate 8) |
| R39-VIEW-CONTROL-UNREACHABLE, R39-HOSTCELL-INFERRED-AS-SEEN | same | MistakeMiner rows 1-2 |
| R39-SEAT-PKILL, R39-ROLE-REFUSED, R38-C2-COUNTER-GAPS | same | C1SentMounts:208; dispatch validator |

`R36-PLACEHOLDER-TIME` (`round-36.md:112`) is the nearest earlier row for candidate 6.

## 2. Considered by a prior seat and never promoted

`R39-CONTROL-NO-RED-CHANNEL` (`MistakeMiner.md:171`, class attribution): `git grep` finds it only in `w1/MistakeMiner.md` and
`w1-results.json`. It is a candidate here as candidate 17.

## 3. Candidates

Row format follows the lesson tables: ID | class | evidence | captured-by | fix, shown able to fail. "Status" is mine.

### Tier A — open at the tip, no row anywhere

**1. R39-MOUNTS-NUL-JOIN** — class **survivor**. Status: **open; I reproduced it at the tip.**
Evidence: `w1/C1SentMounts.md` F2 (`nul-join`, `nul-join-mid`); my re-run (`MistakesSweep/repro-mounts-at-tip.txt`): table
`…ext4 rw,relatime 0 0\0rootfs / btrfs rw,relatime 0 0\n`, absent sysfs root → `STORAGE btrfs-device-stats state=HEALTHY
filesystems=0 devices=0 nonzero=0` plus stderr `tools/tsukuroi-census.sh: line 1911: warning: command substitution: ignored
null byte in input`; the same table with the NUL replaced by a newline → `BLOCKED … detail=mounts:btrfs-without-sysfs`. Round-39
hardened the FIFO and empty-table cases (the arm now reads `[ -f "$PROC_MOUNTS" ] && mtab=$(cat …) && [ -n "$mtab" ]`) but not this one.
Captured-by: none (the frozen r39 counter and the r39/r40 selftest feed NUL-free tables; C1's rule is "unparseable ⇒ BLOCKED", `census.sh:367`).
Fix: refuse a table containing a NUL (`LC_ALL=C grep -qP '\x00' -- "$PROC_MOUNTS"`, or compare `tr -d '\000'` output with the file) and map to
`mounts:unreadable`; add a selftest case with a NUL-joined fixture. Shown able to fail: the case reads HEALTHY at `f951f288` (red) and BLOCKED after the fix (green).
Scope note: round 40's C1 changes the selftest only (`probe_storage_arm` is unchanged by declaration), so this is next-round work, not a round-40 kill.

**2. R39-EMPTY-OVERRIDE-FALLBACK** — class **scope** (survivor of a lane precedent). Status: **open; re-confirmed at the tip.**
Evidence: `w1/C1RevBash.md` D1 — `${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}` and `${TSUKUROI_BTRFS_SYSFS:-/sys/fs/btrfs}`
(`census.sh:462-463`) read an explicitly empty override as unset; the lane ruled the opposite for `TSUKUROI_ROOT_DIR`
(`census.sh:431-437`, selftest `blocked-root-empty-override`). My run: `TSUKUROI_BTRFS_SYSFS=<absent> TSUKUROI_PROC_MOUNTS=` printed
`BLOCKED … detail=mounts:btrfs-without-sysfs` — the **live** table (this host lists btrfs) was read, not the empty override.
Captured-by: QUALITY 82's override-detection half covers hard-coded paths, not set-but-empty. Fix: `${VAR-default}` plus a `${VAR+set}` probe and fail closed
(`mounts:unreadable`), one selftest case per variable with `EXTRA_ENV=(TSUKUROI_PROC_MOUNTS=)`. Shown able to fail: the C1RevBash mutant case
`x-mt-empty-override` PASSed expecting BLOCKED on the shipped census (`C1RevBash/receipts/mutant-selftest.out`); it must FAIL when the fallback is restored.

**3. R39-REVBIND-DISCOVERY-HOLE** — class **vacuous**. Status: **open; line confirmed at the tip.**
Evidence: `tools/check-revision-binding.py:261` matches only `b'"--revision"'`; both round-39 counters and all three round-38 gates spell `'--revision'` in
single quotes (`w1/GateRevisionBind.md` §1: 36 tools carry only the single-quoted form, none discovered; "rows whose name contains r39: []"). The seat reports it
is the same hole the round-38 GateRevisionBind and the round-18 `ReviewJudge.md:9` found. Captured-by: none — the docstring (`:12-15`) documents the literal as the contract.
Fix: discover by `ast`/regex over both quote styles and require every counter row of the gate registry to be probed; also give the two counters' refusal JSON a `findings`
array (same report §2). Shown able to fail: `discovered` today omits every `*-r39.py`/`*-r38*.py`; after the fix the per-tool rows must name them, and a counter
spelled `'--revision'` with no refusal must read inconsistent. I did not re-run the judge.

**4. R39-K10-CLOSURE-FILE** (recurrence of R37-STALE-SELFASSESS-COUNTS) — class **number-drift**. Status: **open; measured.**
Evidence: lessons-dir file counts `a2d7aad7` 54, `a6ca8171` 54 (round-39 last commit, table says 54), `53b294a2` 55 (the non-author closure commit adds
`round-39-verifier-spotcheck.md`), `f951f288` 55. `check-self-assessment.py` K10 therefore reads stated 54, observed 55 at the round-40 base and at the
tip; the same event made K10 red at the round-39 base (52 → 53, `w1/GateRegistrySelf.md` §3) — so three consecutive round bases begin red on K10
because the closure lands after the calibration table. The r39 calibration cell "mismatches 0 required at the round-39 tip" (`SCORECARD.md:2268` region) is true only until the closure commit.
The other five tip reds (K07 60→61, K08 3322→3324, K09 885→887, K13 119→124, K17) are round-40 work landing before its own table — expected mid-round, not counted here.
Captured-by: QUALITY 83 binds the verdict to declared conjuncts; its binding half (explicit measured revision) does not cover a closure file landing afterwards.
Fix: state the measured revision in the calibration row and count `corpus/lessons/` excluding `*-verifier-spotcheck.md` (or restamp K10 in the next round's declaration commit).
Shown able to fail: the checker returns K10 FAIL at `53b294a2` today; it must return 0 mismatches at the base after the fix with a closure file present.

**5. R39-RECEIPT-PROVENANCE-OVERCLAIM** (recurrence of R38-STREAK-ATTRIBUTION) — class **attribution**. Status: **open (routed; seat RoutedProvenance owns it).**
Evidence: `SCORECARD.md:2245` still reads "each written by `tools/run-receipt.py` (revision, tool, tool_sha256, tool_revision `6a08925d`)"; `w1/RevReceiptBinding.md` §1
finds two unbound receipt-class files (`before/sources-census-start.txt`, `after/selftest-49cc53c.txt`); closure §6.5 repeats it.
Captured-by: QUALITY 77 asks revision-cited results to be receipts; it does not require the *sentence* to scope itself. Fix: append a correction scoping the sentence to the c1/c2 receipts, or bind the other classes; shown able to fail by a grep that lists the files under `after/` lacking `tool_sha256`.

**6. R39-FUTURE-DATED-HEADINGS** (recurrence of R36-PLACEHOLDER-TIME) — class **attribution**. Status: **open (routed; RoutedTimestamps/MistakeDateCheck own it).**
Evidence: `git log -S` — SCORECARD "Round 39 — declaration (2026-10-26T06:20Z" first appears at `93fddb2` 02:59:31-03 (= 05:59:31Z, 20 min ahead);
LOG "Round 39 — hyaku run 8, 2026-10-26T07:45Z" at `eeba342` 03:35:44-03 (= 06:35:44Z, 70 min ahead); both headings still in the tree.
Captured-by: none (R36-PLACEHOLDER-TIME says "omit a time stamp rather than placeholder it"; no gate reads heading times). Fix: append a named correction, and a checker that
compares each heading's ISO time with the introducing commit (M-2, seat MistakeDateCheck). Shown able to fail: it must flag these two headings.

**7. R39-GATES-ROW-UNSTATED** — class **attribution**. Status: **open (routed; RoutedGatesRow owns it).**
Evidence: `corpus/lessons/round-39-verifier-spotcheck.md:34-36`: `after/gates-final-a2d7aad.txt:2` is `check-self-assessment rc=1 … "mismatches": 7 … "declaring_round": 38`;
the report and SCORECARD name 7 gate rows PASS and do not name the 8th. Captured-by: none. Fix: append a correction naming the row and its supersession by `eeba342`
(27 checks, 0 mismatches). Shown able to fail: `grep -c 'rc=1' after/gates-final-*.txt` must be matched by a named row.

**8. R39-C1-DETECT-HONEST-PRODUCTION** — class **vacuous** (counter + selftest blind to the production default path). Status: **open; recorded in LOG/PROVINCE prose only, no row.**
Evidence: `w1/C1DetectHonest.md` §1-2 — arm V2 (`d68ed3c`, uid_map test then a literal `HEALTHY 1/1/0` on `/sys/fs/btrfs` + `/proc/self/mounts` defaults) scores PASS 2/3/5/1/1 on the
frozen counter and 117/117 on the selftest; `strace -f -e trace=%file` shows 0 reads of `/sys/fs/btrfs` or `/proc/self/mounts` against 12 for the honest arm.
`LOG.md:1469` and `PROVINCE.md:235` mention it; the R39-FIXTURE-MONOCULTURE row does not, and its fix (vary literals) cannot kill V2, which keys on the namespace, not a literal.
Captured-by: QUALITY 82 (production path) — satisfied in letter by the tmpfs views; QUALITY 87 (b) names only the one-literal arm. Fix: add a read-witness channel to the live leg
(strace/`bash -x` of the real `$BTRFS_SYSFS` read, or a differential against a root that changes under the run) and freeze V2 as a should-fail control. Shown able to fail: V2 reads 0 witness lines, the honest arm 12.
Round 40's C1 (selftest literals M1-M9) does not address this; it is declared out of scope by construction.

**9. R39-C2-COUNTER-SECONDARY-GAPS** — class **vacuous**. Status: **partly open — whether the round-40 counter closes each is unmeasured by me.**
Evidence beyond R39-CONTENT-UNREAD's rule cell: `counts_ok` is circular — the counter prints `host` before reading the entry and asks the entry only to contain the same
strings (`w1/C2CritAxis.md` §C; V6 `counts_ok 2` with false host cells); rows collected file-wide, not by section (V8 rows in an Appendix); one S-row whose title names two files authorises both (V10); duplicate S-id resolves last-wins and
reports nothing (V9, `w1/C2CritControl.md`); the `opened 2026-10-26` conjunct is pinned by no control — M5 survives all 7 committed controls (`w1/C2MutCounter.md`); dropping the uncited S218 from `source:` survives (`w1/C2MutEntry.md` M1a).
Captured-by: QUALITY 87 (content-free entry, one-literal arm); R38-C2-COUNTER-GAPS lists S218 only. Fix: run V6, V8, V9, V10, M5 and M1a as committed should-fail controls against the frozen round-40 counter
(`tools/check-exec-environment-r40.py`); a counter that passes any of them has the same gap. Shown able to fail: each variant already scores PASS on the r39 counter.

### Tier B — fixed in-round (or by the closure), never tabled

**10. R39-REOPEN-AS-NEW-DEPTH** — class **scope**. Evidence: `w1/C2CritAxis.md` §D — S213 add.c ≡ S191 (`fd313629…`), S215 remove.c ≡ S192 (`a052d455…`), S217 trans.c ≡ S210 (`637c1165…`); TO1 restates HO5+HO6;
so 3 of 5 code rows re-open mined bytes and X-ho (the held HO rules) passes 8/8. Captured-by: claim-sizing rule "re-scoring a rule the lane already holds is quality work" (round-39 prompt `:457-461`) — stated, not applied to the declaration.
Fix/status: the round-40 declaration adds a novelty term to its counter (SCORECARD "Round 40 — declaration", C2); I did not run it. Shown able to fail: the held-rows control must score 0/8 (declaration lists "rows re-pointed to held rows S208/S216/S217 0/8 FAIL").

**11. R39-ASSIM-EVIDENCE-STALE** — class **number-drift**. Evidence: `w1/AsmCollision.md` §4 (collisions file 13 ids vs 19 at the pinned tip; files stamped 02:50, the registry append `4078eb2` at 02:59:39; guard fixture not census-valid:
`validate --file` → `E12 S200 row outside Registry section`); `w1/ScoutQuarantine.md` (raw-id intersection {S213} ≠ the lesson's "none"). Captured-by: none. Fix: regenerate after the last registry append and record the registry sha;
`round-39.md:35` now says 19; the round-40 lesson ran the check after S219-S225 (`round-40.md` Gate). Shown able to fail: the 13 → 19 delta (S213-S218).

**12. R39-SIDE-EFFECT-UNSWEPT** — class **reference-drift**. Evidence: after `49cc53c` the census header still said "Known limit, recorded not repaired … next-round work" (`census.sh:377-379`) and "reads sysfs only" (`:372`);
`corpus/README.md:300-301`, `SKILL.md` round-38 row (`:3139` now), `PROVINCE.md:216-217` carried the old reading; the r38 gate row `SKILL.md:3113` advertised exit 0 while the counter exited 1 at the tip
(`w1/C1CritAxis.md` §1, `C1RevHelpText.md` F1-F4, `CritTrend.md` §3.2c). Captured-by: round-35 "gates at the outcome commit" class (R38-ANCHOR-SHIFT) — different surface, same miss: no sweep of the sentences the change falsifies.
Status: closed — header comment deleted (closure: 5 lines), supersession appended (`README.md:315`, SKILL/PROVINCE round-39 sections), `SKILL.md:3301` "Historical instrument pins — round 39". Fix to record: a declared sweep command for the removed claim's phrases; shown able to fail by the pre-fix greps above.

**13. R39-WAVE-NO-EXEC-MARKER** — class **scope/landing**. Status: **open and repeated in round 40.** Evidence: `w1/GateBoundary.md` §3.1 — 0 of 70 round-39 prompts carry `EXEC-AUTHORIZED`, 36 of 70 order execution, none is told to close with a `Scope:` trailer;
`check-seat-scope --worktree` reads 57 MISSING / 13 UNDECLARED; `--revision` is CANNOT_EVALUATE because `swarm-registry.json` and the spec are untracked. At the tip `grep -c 'Scope: executed' .ufo/waves/round-40/w1-spec.json` → 0
(and this seat's own prompt asks for a `Report:` path but no `Scope:` line). Captured-by: none. Fix: put the trailer rule and the marker in the wave context, land `swarm-registry.json` at integration; shown able to fail with GateBoundary's one-seat fixture (variant 1 exit 1, variant 2 exit 0). I did not run the gate.

**14. R39-STALE-PRIOR-NOTES-SCRIPTLET-TAG** — class **stale-premise**. Evidence: `w1/C2ScoutCorrections.md` findings 1-5 — "Only `alpm_logaction` lines reach `pacman.log` … exec failures are stderr-only" (`SKILL.md:3198-3200`, written by round 38), a DKMS build attributed to install scriptlets (`driver-firmware-plane.md:79-80`),
"in the transaction" for PostTransaction hooks in five notes, `[ALPM-SCRIPTLET]` read as scriptlet output in `boot-writers-r19`/`QUALITY.md:70`. Captured-by: QUALITY 66 (keep every branch the source states) would have caught the round-38 sentence; none applied.
Status: closed append-only in round 39 (TO1/TO8 corrections in 7 notes + 3 SKILL sections, closure re-read). Record the class: a limit sentence of the form "only X reaches Y" must cite the writer list at source.

**15. R39-TO5-BLANKET-BOUNDARY** — class **attribution** (limit stated stronger than the capture supports). Evidence: `w1/C2CritTO5.md` — the boundary bullet `pacman-transaction-order-r39.md:49-50` ("the capture cannot separate 'file absent' from 'triggers did not match'") is false for
`10-limine-snapper-lock.hook`: a same-hook control ran in Pre at `pacman.log:2131` while its owner was first installed at `:1344-1346`; 16 of 17 instances are vacuous. Captured-by: QUALITY 3 (observation/inference/unknown separate). Status: corrected append-only in the entry (SCORECARD outcome: "TO5's host column … corrected").

**16. R39-CITATION-CLOSURE** — class **reference-drift**. Evidence: S208 `used-by` omitted `boot-writers-r19.md:176-177` (`w1/C2RevSourcesRows.md`; now present in `corpus/SOURCES.md` S208 used-by); the r39 entry cited `corpus/lessons/round-39.md` before it existed (`w1/CritTrend.md:160`, `C2RevenStaged.md` (d));
**still open:** `grep -c S217 corpus/knowledge/pacman-hook-order-r38.md` → 0, though S217 supersedes S210's anchor — the entry's erratum (`:145-147`) says the row is "not rewritten" and points nowhere (`w1/CritTrend.md` §3.2b). Captured-by: none. Fix: add an append-only pointer to S217 in `pacman-hook-order-r38.md`; a used-by gate `grep -l 'S208' corpus/knowledge/*.md` against the cell.

**17. R39-CONTROLS-NO-RED-CHANNEL** — class **attribution**. Evidence: `w1/MistakeMiner.md:171` — `run-controls.sh:21` swallowed counter stderr/exit, `run.err` 0 bytes, 10 of 12 recorded `revision` values absent from the lane.
Status: I read `.ufo/waves/round-40/controls/run_controls.py:55-63` — it records `p.returncode` and, on a non-JSON stdout, `{'raw': …, 'stderr': …}`; that is a red channel for the counter's own output but I did not check clone-failure handling or whether recorded revisions resolve. Unverified for round 40.

**18. R37-GATE-ADMIT-MISCOUNT** (round 37; also R37-MANIFEST-NULL) — class **attribution / provider**. Evidence: `round-37.md:74` supersedes the Gate paragraph "two entries admitted from the package" (only `errno-contract-variance-r37.md` was a staged admit);
`round-37-verifier-spotcheck.md` §1 "the report says 'rejected 2 of 3 with flip conditions'; only one carries a flip" (routed §6.6, fixed in r38's erratum); `round-37.md:70` "result manifest has `output: null` on all 64 rows after an orchestrator-kernel restart" and `:88` "Attempt 1 … filed no report".
Captured-by: none. Fix: derive Gate counts from the decision table by a counting command (the R37-SEAT-REPORT-COUNT remedy), persist per-seat results as they settle; round 39 shows `w1-results.json` with outputs on all 70 seats. Shown able to fail: the round-37 text itself.

Smaller items not given rows: R38 S210 anchor `_alpm_trans_commit` (erratum only in lesson prose at the time, `round-38-verifier-spotcheck.md:32-34`; fixed by S217, `round-39.md` disposition #4); R38 `score-pacnew-arm-r35b.py` base-parity failures (disposition #6, pinned in `SKILL.md:3301`);
ConnClaims F2 `failedhist` counted over a replaced capture buffer (`census.sh:1474-1475` still computes `fh_n` from `$CAP_OUT`; I confirmed the line, not the overwrite — `w1/ConnClaims.md` F2, routed as debt, no row); ConnClaims F1 (8-name package prefix) is a disclosed trade, not a mistake.

## 4. Proposed text

Paste-ready rows are the §3 candidates; Tier A items 1-9 are the ones I recommend for the round-40 lesson `## Mistakes` table, ordered by harm: 1, 2, 3, 8 (open instrument/arm defects), 4 (three-round recurrence), 13 (repeats in this wave), 9, then 5-7 (routed; add only if their seats' corrections do not land).

## 5. Not done

- I ran no counter and no selftest; the only executions were four census runs on scratch mount tables (`repro-mounts-at-tip.txt`) and `check-self-assessment.py` at the tip.
- Candidates 3, 8, 9, 10, 13, 14, 15 rest on seat reports I read but did not re-derive; candidate 17 is half-read.
- I did not read round-38 wave reports (only the round-38 lesson and closure), so round-38 candidates beyond §3.18's smaller items may be missing.
- I did not judge whether the five other tip self-assessment reds (K07-K09, K13, K17) are defects; they track round-40's own unstamped counts.
