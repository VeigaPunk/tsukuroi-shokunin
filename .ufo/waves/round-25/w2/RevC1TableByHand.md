Verdict: partly holds. Every number, ordinal and last-change pointer in the axes table re-derives at 5e7c04ecb02735491456de2b8bc44550d0db4609, but nine table statements are false or stale as written, and the C1 checker's 0-of-23 result does not cover them.

# RevC1TableByHand: hand re-derivation of the round-25 axes table

Method. I extracted 5e7c04ec into two scratch copies under /fast/scratch/hyaku/tsukuroi-r25/w2/RevC1TableByHand/ (`sandbox` and `verify`, from `git archive | tar`, with no .git and no remote). Every count, grep and selftest ran there, not in the lane working tree. The lane was touched only through read-only git (`rev-parse`, `log`, `status`). Line numbers below refer to SCORECARD.md, SKILL.md, PROVINCE.md and the other files as they stand at 5e7c04ec.

## Values that re-derive

| Table value | Re-derived at 5e7c04ec | Command and result |
|---|---|---|
| 47 notes | 47 | `ls corpus/knowledge/*.md \| wc -l` (plain pipe in the shell) gives 47 |
| SKILL.md 2355 lines | 2355 | `wc -l < SKILL.md` gives 2355; the file ends with a newline |
| 297 table lines | 297 | `grep -c '^\|' SKILL.md` gives 2355, but `grep -c '^|' SKILL.md` and `grep -cE '^\|' SKILL.md` give 297 (see finding 1) |
| 26 lesson files | 26 | `find corpus/lessons -type f \| wc -l` gives 26 |
| README 231 lines | 231 | `wc -l < corpus/README.md` gives 231 |
| 97 cases | 97 | `bash tools/tsukuroi-census.sh --selftest` gives rc 0 and `TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)` |
| Live run, six planes | rc 1 | `bash tools/tsukuroi-census.sh` gives rc 1 and six PLANE lines: packages, systemd, drivers, journal, update-safety, oom |
| Zero mutation | holds | `diff -rq` between the post-run copy and a fresh archive shows only my four output files; `find -name db.lck` finds nothing |
| `--identity` not landed | holds | no `--identity)` case arm in tools/tsukuroi-census.sh; SKILL.md:1469 and SKILL.md:1595 record D12 as not landed; closeout-r11.md:43 agrees |
| Core, Frontier, Adjacent sections | hold | PROVINCE.md:6, :35, :75 |
| Formal overlap table | holds | PROVINCE.md:44 is the header `\| ID \| Finding / boundary trigger ...`; ADJ-01 to ADJ-07 rows follow; OUT-001 to OUT-010 sit at PROVINCE.md:121 to :130 |
| Ordinal transitions agree with the six scores | hold | last recorded transitions: depth 8→8 at SCORECARD.md:793 (score 8); coverage 8→9 at :224 (score 9); operability 9→9 at :731 (score 9); freshness 8→9 at :240 and 9→9 at :807 (score 9); calibration 9→9 at :792 (score 9); adjacency 7→8 at :213 and 8→8 at :620 (score 8) |
| Last-change pointers | hold | SCORECARD.md:30 is the move-log row for round 4 (freshness and depth); :36 is round 10 calibration; :37 is round 11 operability; :213, :224 and :240 are the round-1 post-review corrections named in the table |
| Six planes have landed notes | hold | package-state-plane.md, systemd-user-plane.md, driver-firmware-plane.md, journal-boot-plane.md, update-safety-note.md and oom-event-plane.md all exist under corpus/knowledge/ |
| Four fleet-round-1 surfaces each link one note | hold | PROVINCE.md:20 to :23 link arch-news-gate-2026.md, pacnew-plane.md, initramfs-v42-sysroot-recovery.md and snapper-eacces-mechanism.md; all four exist |
| Seven erratum notes | 7 | seven notes carry a `## Erratum (2026-10-19, fleet round 1) — D[1-5]` heading |
| Capabilities path pointers (outside the axes table) | hold | all 17 paths that K16 to K23 read exist at 5e7c04ec (`test -e` in the archive); corpus/SOURCES.md has 125 rows (`grep -cE '^\| S[0-9]+'`) |

## Statements that are false or stale as written

1. [obs] The depth row's counting command for 297 does not reproduce 297. The cell prints `grep -c '^\|' SKILL.md`. Run in the archive, that prints 2355, because GNU grep reads `\|` in a basic regular expression as alternation, so `^\|` matches every line. The literal `grep -c '^|' SKILL.md` prints 297. The number is right; the printed command is not. The C1 checker's K09 test uses the literal predicate, so it passes without testing the printed command. Evidence: SCORECARD.md:828 and the two command outputs above.

2. [obs] The depth row's command for 47 notes, `ls corpus/knowledge/*.md \| wc -l`, fails when copied from the file. Bash passes `|` to ls as a file name and prints `ls: cannot access '|': No such file or directory`. The backslash is a Markdown table escape, so the rendered cell probably shows a plain pipe and works [inf]. Evidence: SCORECARD.md:828 and the same `ls` run in the archive.

3. [obs] The intro says "each evidence pointer carries the command that re-derives the number it quotes", and the closing paragraph says the counting commands are "the only source of the quoted counts". Both are false. These quoted numbers have no command in their cell: "7 notes" and "25 of 25 per-note rechecks" (freshness row, SCORECARD.md:831; the 7 traces to the round-1 grep at :240 and the 25 to the round-1 record at :193); "six gate planes" and "four declared read-only surfaces" (coverage row, :829); "six-plane rollup" (operability row, :830, where the live command is not named); "ADJ-01 to ADJ-07" and "OUT-001 to OUT-010" (adjacency row, :833). Evidence: SCORECARD.md:815 to :837.

4. [obs] The depth row says "every rule in `SKILL.md` cites a `corpus/knowledge/*.md` note." That is false. The four standing rules at SKILL.md:13, :15, :16 and :18 cite no note; the first cites PROVINCE.md. I split SKILL.md into bullet blocks (a bullet line plus its continuation lines): 237 of 254 blocks contain no `corpus/knowledge` string and 17 do. The boundary rule cites notes by bare file name (SKILL.md:147, `systemd-user-plane.md:7`), which is not the stated form. Method: a short Python pass over the archive copy of SKILL.md.

5. [obs] The coverage row says "six gate planes equal the surfaces `PROVINCE.md` owns". They do not. The live census emits six planes: packages, systemd, drivers, journal, update-safety and oom (live run in the archive, rc 1). PROVINCE.md's owned list (Core, PROVINCE.md:8 to :15) names pacman state, systemd units and timers, journal and boot triage, driver and firmware, and update-safety questions. Memory appears only as a supporting measurement that "support[s] OS triage" (PROVINCE.md:30), so the oom plane has no owned-surface row. The four fleet-round-1 surfaces (PROVINCE.md:20 to :23) have no census plane; the only census match for their names is a fixture string at tools/tsukuroi-census.sh:2137. Each plane does have a note, so the "each with a landed note" half holds.

6. [obs] The freshness row says the fleet round-1 erratum rechecks, "(7 notes, 25 of 25 per-note rechecks)", "are the current floor". The 7 holds. The 25 does not re-derive. The round-1 record measured "date-or-cadence rechecks 0/25 → 25/25" over a 25-note base that the table never names (SCORECARD.md:193). At 5e7c04ec the corpus has 47 notes, and all 47 carry a `recheck:` line. A crude date-or-cadence test on the first such line (a date, an `Nd` interval, on-release, or a cadence word) passes 28 of 47 [inf]. The other 19 are pointers or commands, for example `recheck: §7.` in census-closeout-receipt-r10.md and `recheck: §5.` in closeout-r11.md. "Current floor" is stale framing: the 25-of-25 figure describes round 1's base, not the current corpus.

7. [obs] The calibration row says calibration-synthesis.md holds the loop "with its mismeasure rows". The word does not occur in that file; no mis-measure variant matches. "Mismeasure" appears in SKILL.md:1408 and :1414, the round-10 ledger. The file is also scoped to rounds 1 to 9 (its line 1). The loop itself (claim, re-measure, append, supersede) is present.

8. [obs] The calibration row says this round's C1 "is what the r10 ceiling asked for". No such ceiling is recorded. The word "ceiling" does not occur in LOG.md, closeout-r11.md, calibration-synthesis.md or SKILL.md. The calibration ceiling recorded at round 11 names only the D13 debts (SCORECARD.md:51). Calibration-synthesis §6 (lines 370 to 403) lists seven open debts, and none concerns the self-assessment table.

9. [obs] The depth row says rounds 12 to 24 "each record depth 8 to 8 with no change." The substance holds; the literal wording does not hold for rounds 19 and 20. Rounds 12 to 18 and 21 to 24 write depth 8→8 explicitly (for example :256, :324, :388, :424, :492, :517, :572, :658, :678, :698, :716, :730, :759). Round 19 names depth only as "tied-lowest 8" and says "No ordinal, declaration or refinement changes" (:612). Round 20 says "all ordinal deltas remain0" (:626).

10. [obs, outside the axes table] SKILL.md:1595 places the identity-comment hits at `:35` and `:46`. At 5e7c04ec they are tools/tsukuroi-census.sh:37 and :48. The operability row relies on the same fact, and its claim still holds.

## Residual risk for the L1

- The 23-check result (0 mismatches, exit 0, which I also ran and which agrees with every number above) tests numbers, ordinals and some tokens. It does not test the printed command strings (findings 1 and 2), the "every rule" claim (4), the plane-to-surface claim (5), the "25 of 25" figure (6), the "mismeasure" wording (7), the "r10 ceiling" attribution (8) or the depth wording (9). Read a PASS as a numbers-and-tokens pass only.
- Suggested repairs for the L1, not applied here: write the 297 command as `grep -c '^|' SKILL.md`; drop the pipe escape from the `ls` command; narrow "every rule" to the rules that cite notes, or drop it; say that the oom plane is supporting rather than owned, and that the four fleet-round-1 surfaces have no plane; recompute the recheck figure from the 47 notes or drop the 25; change "mismeasure rows" to SKILL.md section 1; drop the r10 attribution; fix the depth wording for rounds 19 and 20.

## Unknowns and verification gaps

- [unk] "each round's record re-ran its predecessor's pins" (freshness row). Not audited round by round.
- [unk] "the receipts ... hold the re-run evidence" (freshness row). The three receipt files exist (corpus/knowledge/aur-drift-receipt-r9.md, census-closeout-receipt-r10.md, closeout-r11.md section 5); their contents were not audited.
- [unk] "the K3 upstream delta (network read) still awaits an operator boundary ruling" (coverage row). The repository holds no ruling: SCORECARD.md:199 and corpus/lessons/round-1.md:71 to :74 are the only records. An out-of-repository ruling cannot be excluded.
- [inf] "the D13 verification debts stay open" (calibration row). The latest records are closeout-r11.md:240 and LOG.md:239; I found no closure.
- Not checked: the 34-row snapshot in .ufo/evidence/round-1-kaika/after.md; the boot-chain selftest count of 45; the root-metadata-observer commit pin. These are outside the axes table.
- [unk] "the r10 receipt's own pins were superseded inside its commit, recorded as drift and not smoothed" (freshness row). Repeated from the round-11 table at SCORECARD.md:50; not audited.
- [obs] The calibration row's errata examples (the r1 retractions, the 5-plane numerals, the AUD-X7 credit correction) have matching terms in calibration-synthesis.md ("retract" 3 hits, "5-plane" 2, "AUD-X7" 7). Their content was not audited.
- [obs] The adjacency row's reported-not-absorbed rows (coredump storm, walker-restart.hook root-exec to kagi, GSP selection to kaidoku and revenger) match LOG.md:164 to :166, SCORECARD.md:52 and SKILL.md:404 to :406 and :427 to :430 in wording. Each row's disposition was not audited.

Scope: read=SCORECARD.md, SKILL.md, PROVINCE.md, LOG.md, SHONEN.md, tools/tsukuroi-census.sh, corpus/ (knowledge, lessons, README.md, SOURCES.md) and the 5e7c04ec archive copies; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RevC1TableByHand.md (created the w2 directory), /fast/scratch/hyaku/tsukuroi-r25/w2/RevC1TableByHand/sandbox and /fast/scratch/hyaku/tsukuroi-r25/w2/RevC1TableByHand/verify; executed=git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD, log --oneline -3 and status --porcelain (read-only); git archive 5e7c04ecb02735491456de2b8bc44550d0db4609 | tar -x into the two scratch copies; in the sandbox copy, bash tools/tsukuroi-census.sh --selftest (rc 0, 97/97 PASS) and bash tools/tsukuroi-census.sh (rc 1); diff -rq between the two scratch copies; in the lane, python3 tools/check-self-assessment.py --revision 5e7c04ecb02735491456de2b8bc44550d0db4609 (rc 0, checked 23, mismatches 0); grep, wc, find, ls, sed, test -e and small python3 counts over the scratch copy
Model: anthropic/claude-haiku-5-5 (as stated in the host project context; not independently confirmed)
Installs: none
