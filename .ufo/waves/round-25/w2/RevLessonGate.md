# RevLessonGate — round 25 lesson gate (non-author re-open)

Verdict: partly holds. Every one of the 18 Gate quotes is an exact, whitespace-normalised substring of the fetched upstream bytes at the claimed lines, and the registry change is append-only with no old row altered. But the lesson still fails the SOURCES contract on a canonical URL for the sibling row, the missing round-25 search log, unregistered Arch renders that the knowledge entry cites under the same S-id, unbacked used-by claims, candidates without flips or without any entry, three teaches elements with no quote, negative claims without sweeps, Mistakes rows whose fixes are not shown able to fail, a cited C1 receipt set that is not committed, and missing Mistakes rows for incidents the lesson itself records.

State checked. Committed revision 5e7c04ec (the measured revision), claim base b9046016, and the lane working copy as it stood when I read it. The working copy already contains L1 edits made during this wave: an errata section appended to the lesson (lines 69–84), and two registry rows added to corpus/SOURCES.md (S126, a digest correction superseding S120; S127, a mori row superseding S125). Findings below say which state they apply to. Upstream bytes were fetched by curl and hashed; my copies are under /fast/scratch/hyaku/tsukuroi-r25/w2/RevLessonGate/src/.

## Findings, by severity

### 1. [high] The sibling row has no canonical URL, and the Gate row has none either

- The contract says the source cell is a canonical URL or DOI, and that a repo path is only valid for own-work (corpus/SOURCES.md shape note, CORPUS.md line 90). S125 (committed corpus/SOURCES.md line 131, kind docs) and its replacement S127 (working copy line 133) both give only "mori-shokunin/corpus/knowledge/system-pressure-r24.md at commit 4f05dd5a" plus a git blob id.
- The lesson's Gate row for S125 (corpus/lessons/round-25.md line 30) also has no URL in its URL column.
- A public canonical URL exists and returns identical bytes. Evidence: `curl -fsSL https://raw.githubusercontent.com/VeigaPunk/mori-shokunin/4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e/corpus/knowledge/system-pressure-r24.md` then `sha256sum` gave 5d3a322aadb00c6ba3700b6c5b31d4e5b5305b404731f0eb37a5a3474c019ce5. `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 4f05dd5a:corpus/knowledge/system-pressure-r24.md` gives the same sha256. The blob id d4ccce42 is confirmed by `git rev-parse 4f05dd5a:corpus/knowledge/system-pressure-r24.md`. [obs]
- Fix: put that raw URL in S127 and in the Gate row, and keep the blob id as the pin.

### 2. [high] Used-by and status claims for the sibling row and for the lesson are not backed

- At 5e7c04ec, S125 is `mined` with used-by memory-pressure-r25.md and .json. Neither file contains the string S125. The md cites the sibling by path only (memory-pressure-r25.md lines 35–36, "mori-shokunin@4f05dd5a:corpus/knowledge/system-pressure-r24.md"). CORPUS status rule: mined means cited by at least one path in used-by. So the status is unsupported at 5e7c04ec. [obs]
- In the working copy the md now cites S127 by id (memory-pressure-r25.md line 392), which fixes the citation for S127. The json still says S125 in source_id_note (memory-pressure-r25.json line 39). [obs]
- S123 and S124 list both files as used-by, but the md never names them (grep: no S123 or S124 in the md; both appear in the json). [obs]
- The lesson cites all eleven rows (corpus/lessons/round-25.md lines 13–30), yet no used-by cell names corpus/lessons/round-25.md. CORPUS: used-by is the knowledge entries or lessons citing the row. [obs]
- Fix: add corpus/lessons/round-25.md to used-by for every row the lesson cites; make the md list only paths that name the row; repoint the json source_id_note to S127.

### 3. [high] The knowledge entry cites unregistered Arch renders under S121 and S122, with locations that match neither the row nor the Gate

- Working copy memory-pressure-r25.md lines 237 and 246 cite https://man.archlinux.org/man/systemd.resource-control.5 and https://man.archlinux.org/man/systemd-oomd.service.8 as "the same page rendered for the host", with plain-text rendering lines 1319-1320, 1306-1309, 1314-1317, 23-24, and their own sha256 values. The row S121 and the Gate pin the upstream v262 XML (lines 1525–1548). [obs]
- memory-pressure-r25.json lines 333–336 record source S121 with url https://man.archlinux.org/man/systemd.resource-control.5 and location "plain-text rendering lines 1306-1309" for the quote "When set to kill, the unit becomes a candidate for monitoring by systemd-oomd." Lines 422–425 do the same with lines 1325-1328. [obs]
- The lesson says these Arch pages were "opened but not registered" (corpus/lessons/round-25.md line 34). So one S-id resolves to two URLs with two line systems, and one of them is a source the lesson disclaims. [obs]
- Fix: quote the knowledge entry from the pinned XML, citing XML lines, or register the Arch renders as their own rows with their own digests.

### 4. [medium-high] The round-25 search log (CORPUS rule 5) was not written

- The committed registry diff against b9046016 adds exactly 11 rows (corpus/SOURCES.md lines 121–131: S115 to S125) and no prose. A difflib check found zero non-row diff lines. The only 2026-10-22 search paragraph is the round-24 one (5e7c04ec line 194; working copy line 196). The working copy adds only S126 and S127 rows. [obs]
- Rule 5 requires question or query, where searched, date, identified, screened, included and excluded counts, exclusion reasons, and a stop rationale. The lesson's Gate gives seat names and a list, not those fields. Wave-1 reports show the search covered at least 40 candidate URLs (see item 5), so this is not a no-search case. [obs]
- Fix: write one round-25 search-log paragraph with those fields.

### 5. [medium] Rejected candidates lack flips, and many opened candidates are not named at all

- The rejected bullet for kernel/cgroup/cgroup.c, include/linux/psi_types.h, mm/memcontrol.c and mm/vmstat.c (corpus/lessons/round-25.md line 36) gives a reason ("no admitted statement rests on them alone") and no flip. The contract requires REJECTED: reason; flip: what would change the verdict. [obs]
- At least 13 URLs that wave-1 reports used are named nowhere in the Gate, neither as admitted nor as rejected. Pointers: src/oom/oomd.conf (v262) and src/oom/oomd-util.c (.ufo/waves/round-25/w1/CritC2Rows.md lines 119 and 122; RevMp4Semantics.md line 23); src/core/varlink.c (RevMp4Semantics.md line 9); src/core/cgroup.c, src/core/manager.c and src/oom/oomd-conf.c (ExecRecapture.md lines 61, 62, 66); units/user@.service.in (CritC2Rows.md line 123); man/systemd.exec.xml (RevengerOomHistory.md line 34); include/linux/vmstat.h, include/linux/vm_event_item.h and include/linux/memcontrol.h (SrcKernelOomCounter.md lines 130–132); the Arch earlyoom man page (ExecRecapture.md line 71); and the gregkh/linux v7.2.11 stable tree (SrcCgroupV2.md line 9). [obs]
- The registry convention keeps rejected sources as rows with status rejected (corpus/SOURCES.md line 35, S029; line 42, S036; CORPUS status rule "rejected (kept — a rejection is evidence of taste)"). The lesson keeps every rejection out of the registry. [obs]
- Fix: give each unregistered candidate a reason and a flip, or state that it was a verification read only, and decide whether rejections become rejected rows.

### 6. [medium] Several teaches sentences are only partly grounded by the Gate quotes

Every Gate quote matches its claimed lines, but the teaches sentence for these rows rests on text the Gate does not quote, or on text the quote truncates:

- S121 (teaches: "only kill, on the unit or an ancestor"). The Gate quote at line 1531 begins "the unit becomes a candidate" and drops "When set to kill,", which is the condition the teaches depends on. The ancestor clause (lines 1546–1548, "if an ancestor cgroup has one of these properties set to kill") is not quoted. Source: src/S121-systemd.resource-control.xml. [obs]
- S122 (teaches: "monitors only cgroups of units set to kill"). The Gate quote (lines 45–46) reads "...for the system and those cgroups..." and its antecedent is the sentence at lines 43–44 ("Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored."), which is not quoted. The clause "when it is not running it acts on nothing" has no source line and is an inference. Source: src/S122-systemd-oomd.service.xml. [obs] [inf]
- S123 (teaches: an auto cgroup "is removed from the monitored set"). The Gate quotes only the if line 124. The removal is line 125 (`hashmap_remove(monitor_hm, empty_to_root(message.path))`). Source: src/S123-oomd-manager.c. [obs]
- S124 (teaches: "30 seconds"). The Gate quotes lines 26 and 27 only. The 30-second value is line 25 (`#define DEFAULT_MEM_PRESSURE_DURATION_USEC (30 * USEC_PER_SEC)`). Source: src/S124-oomd-manager.h. [obs]
- S120 (teaches: "90 percent swap use with memory use also above it"). The "memory use also above it" element rests on lines 166–168 (both memory and swap fractions must exceed the limit), which are not quoted. The Gate quote "Defaults to 60%." (line 190) also does not name its setting, which is DefaultMemoryPressureLimit= (term at line 178). Source: src/S120-oomd.conf.xml. [obs]
- S118 (teaches: "Each non-root cgroup carries its own memory.pressure"). The quoted lines 1914 and 1507–1508 do not say non-root. The nearest text is lines 1077–1078 ("PSI accounts stalls for each cgroup separately"), not quoted. Source: src/S118-cgroup-v2.rst. [obs]
- S117 (teaches: "identical to /proc/pressure/memory"). The support is kernel/sched/psi.c line 1545 (`return psi_show(m, &psi_system, PSI_MEM);`), which is the S116 file and is not quoted under S117. [obs]
- S116 (teaches: "the total only grows within one boot"). Nothing in psi.c mentions boot. The within-one-boot element is an inference and is not marked as one. [inf]
- S115 (teaches: "one read never dates an incident"). No source line supports it, and it is not marked as an inference. [inf]

Fix: add the missing lines as Gate quotes, mark the inferences, and make each quote carry the setting or condition its teaches uses.

### 7. [medium] Negative claims were made without recorded sweeps (CORPUS rule: a negative claim carries its sweep)

- S116: "the only write to total" (registry row, corpus/SOURCES.md line 126 at 5e7c04ec). My sweep of src/S116-psi.c with the regex `total\s*\[|->total|\.total|total\s*(\+=|=)[^=]` returned 18 hits. Exactly one write goes to group->total (line 410, `+=`). The rest are reads or writes to avg_total and rtpoll_total. The claim holds on this sweep, but the sweep is not recorded anywhere in the lesson or registry. [obs]
- S119: "separate from pressure stall accounting". My sweep of src/S119-oom_kill.c for `psi|pressure|stall` (case-insensitive) returned 0 hits. The claim holds on this sweep; no sweep is recorded. [obs]
- S117: "not a sum of child cgroups" has no sweep. The root-identity support is psi.h line 39 plus psi.c line 1545; neither is a sum. [obs]

### 8. [medium] The Arch rejection reason is applied to the Arch pages only

- The lesson rejects the Arch renders because they render systemd 262.1 while the host runs 262-1 (corpus/lessons/round-25.md line 34). The host version holds: `pacman -Q systemd` returned `systemd 262-1` on 2026-10-22. [obs]
- The registry already relies on "systemd 262.1 man-page footer" for S025, S028, S039, S041, S044 and S046 (corpus/SOURCES.md, those rows at 5e7c04ec). The round neither extends the same version-scope reasoning to them nor records why it does not apply. [obs]
- Fix: state that the v262 wording is version-independent for those rows, with the evidence, or record the scope on them.

### 9. [medium] The Mistakes table: fixes are not all shown able to fail, and the cited receipts are not committed

R25-STALE-AXES-TABLE (lesson line 59):
- The lesson's red state is b9046016 versus 5e7c04ec. `git diff --stat` between those two revisions lists 130 files, so it is not a single-delta pair. [obs]
- The reverse single-delta test does isolate the fix: in a sandbox from 5e7c04ec with SCORECARD.md and SHONEN.md reverted to b9046016, `python3 tools/check-self-assessment.py --revision HEAD --repo <sandbox>` exits 1 with 13 mismatches, namely K02, K04, K06, K07, K08, K09, K10, K11, K12, K13, K15, K17 and K21. That is exactly the set the lesson lists. [obs]
- The forward test does not pass: b9046016 with only the new SCORECARD.md and SHONEN.md exits 1 with 4 mismatches (K07–K10: stated 47 notes against 46; 2355 against 2301 lines; 297 against 259 table lines; 26 against 25 lesson files). The fixed counts describe the post-round tree, so the fix is not self-sufficient on the base tree. [obs]
- Selftest: `--selftest` passes, and its stale-ordinal case (expects K02) and stale-count case (expects K07) each exit 1 as designed. The lesson's phrase "a stale-ordinal and a stale-count case that fail" is ambiguous: these are mutants the checker must flag, and the selftest passes. [obs]
- The receipts the lesson names (measure/c1-b9046016.json, c1-selftest.txt, exits.txt) are not committed. `git ls-tree -r --name-only 5e7c04ecb02735491456de2b8bc44550d0db4609 -- .ufo/waves/round-25/measure` lists only .ufo/waves/round-25/measure/census-before.txt, and `git check-ignore` returns exit 1 for the others, so they are untracked. CORPUS requires the observed failure text to be committed. [obs]
- The captured-by cell says "none". The working-copy errata (lesson lines 69–84) now say QUALITY 55 partly covered the same example. The table cell was not changed. [obs]
- The round-11 evidence command is itself wrong. SCORECARD.md line 47 at b9046016 says "55 table lines (`grep -c '^\|' SKILL.md`)". That command returns 2301 at b9046016 (every line, because the empty branch of the alternation matches all lines). The pipe-prefixed count `grep -c '^|' SKILL.md` gives 259. So the stale premise cannot be reproduced with its own command. [obs]

R25-SEAT-PUSH (lesson line 60):
- The incident evidence holds. The reflog of master shows four push entries at 07:31:03, 07:32:42, 07:32:51 and 07:32:51, and the L1 undo at 07:35:48 (`git reflog -n 12 master`). Commit authors are `t <t@x>` for d2e9a7a, 9e9a97d and d70cbd0, and `r20 <r20@example.invalid>` for d5e6481. The public GitHub master is 5e7c04ec (GitHub API branches/master, HTTP 200), and d5e6481 returns HTTP 422 from the commits endpoint, so the scratch commits never reached the public remote. [obs]
- The fix is not shown able to fail. The push-URL guard, the wave-context prohibition, and criterion 59 (corpus/QUALITY.md line 118) have no executable check and no red-before run; criterion 59 has no Check line. The only "shown able to fail" text, "ahead=4 before the repair and ahead=0 after", is not in any committed file: searching the 5e7c04ec tree finds it only in the lesson's own sentence. [obs]
- "Every executor clone now has push URL /nonexistent/no-push-to-lane" is not verified. I found no executor clone to inspect. [unk]

### 10. [medium] Mistakes the lesson records but does not list

CORPUS says one row per mistake. These are described in the lesson but have no row:
- Round-24 seats kept writing after round 24 ended; three tracked files were restored and two untracked files deleted (corpus/lessons/round-25.md line 64). [obs]
- capture.sh counted the [OOM] section header as an active setting, the "sentinel finding" (line 66). [obs]
- The frozen capture never read earlyoom (Process notes, same section). [obs]
- Routed defect 3, sequencing, marked "Not repaired" (line 48). [obs]

### 11. [medium-low] Counts without their commands

CORPUS: a count carries its command. The lesson gives counts without commands (for example "46 notes, 2301 lines, 259 table lines, 25 lesson files, 231 README lines, 97 census cases" at lines 59 and 55–60, and "four scratch commits" at line 60). I reproduced the b9046016 set at /fast/scratch/hyaku/tsukuroi-r25/w2/RevLessonGate/rev-b9046016 with: `ls corpus/knowledge/*.md | wc -l` gives 46; `wc -l < SKILL.md` gives 2301; `grep -c '^|' SKILL.md` gives 259; `ls corpus/lessons | wc -l` gives 25; `wc -l < corpus/README.md` gives 231; `bash tools/tsukuroi-census.sh --selftest` ends with `TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)`. The numbers are right and unlabelled. [obs]
- The knowledge entry's first line says "eight SOURCES rows for the primary pages below" (memory-pressure-r25.md line 1). The registry has ten primary rows, S115 to S124. [obs]

### 12. [low] Smaller citation errors

- The lesson says the correction is "Appended correction after QUALITY 56" (line 51). The correction sits after criterion 59 at corpus/QUALITY.md line 120. [obs]
- The S120 registry digest is wrong: the row reads "…5632d4a6…" where the fetched bytes give "…5632a4d6…" (digest positions 16 and 18 differ). The working copy corrects this with a new row, S126, which is the contract's supersession form. The erratum (lesson lines 69–70) records it. Status: corrected by supersession. [obs]

## What holds

- Quotes: all 18 Gate quotes are exact, whitespace-normalised substrings at the claimed lines, each at most 18 words. Results: S115 lines 45–46, 48–49, 62–63; S116 lines 410–411; S117 line 39; S118 lines 1914 and 1507–1508; S119 line 935; S120 lines 172, 190, 202; S121 lines 1531 and 1545–1546; S122 lines 45–46; S123 line 124; S124 lines 26 and 27; S125 lines 45–46 under "## Scope" at line 43 of the mori blob. [obs]
- Digests: for S115 to S124 the fetched bytes match the registry anchors, except S120 (item 12). [obs]
- Access dates: every Gate row carries an opened date of 2026-10-22, which is today. [obs]
- Old-to-new log: at 5e7c04ec, 114 old rows are unchanged on full-row comparison and 11 rows are added. The working copy adds only S126 and S127. The empty recheck and used-by log in the lesson (line 38) is honest. [obs]
- Commit hashes named in the lesson resolve: b9046016, 5e7c04ec, 6c580b15, 0cd9b28b, and mori 4f05dd5a. [obs]
- Host version: the installed systemd is 262-1, as the lesson says. [obs]
- The knowledge entry opens with source, verified-at and recheck lines (memory-pressure-r25.md lines 1–3). [obs]

## Verification gaps and unknowns

- Executor clone push URLs (item 9). [unk]
- W04 = 21, the 593 and 364 line counts, the 15 and 19 probe lines, and the ordinal counts 9, 9 and 8 were not checked. [unk]
- The capture.sh sentinel claim (item 10) was not checked against the capture file. [unk]
- I did not search QUALITY criteria 1–56 for an earlier criterion that would have captured R25-STALE-AXES-TABLE, so "captured-by none" is unverified beyond the table. [unk]
- Spot-check: this file is a non-author re-open of every admitted URL and every Gate quote, not a sample. The lesson's Spot-check line (line 40) owes that closure to a non-author. I have not granted it. [obs]

Scope: read=corpus/lessons/round-25.md (committed and working copy); corpus/SOURCES.md (5e7c04ec, b9046016, working copy); /home/vgpnk/Projects/shokunin/CORPUS.md; corpus/QUALITY.md lines 110–120; corpus/knowledge/memory-pressure-r25.md and .json (committed and working copy); SCORECARD.md at b9046016; the w1 reports under .ufo/waves/round-25/w1 (URL sweep); the mori entry at 4f05dd5a; the ten upstream raw files and the mori raw URL; lane git metadata (refs, reflog, object types, tree listing, ignore status); GitHub API branch and commit lookups; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RevLessonGate.md and /fast/scratch/hyaku/tsukuroi-r25/w2/RevLessonGate/ (fetched sources, sandboxes rev-b9046016, rev-5e7c04ec, c1-fwd, c1-rev, selftest output, gh-master.json); executed=read-only git in the lane and the mori repo (cat-file, rev-parse, log, reflog, ls-tree, check-ignore, diff --stat, show, archive into sandboxes); pacman -Q systemd, earlyoom and mkinitcpio; curl of public raw URLs and the GitHub API; sha256sum; in-process Python quote matching and registry diffing; python3 tools/check-self-assessment.py against sandbox repositories (--revision HEAD --repo, and --selftest); sandbox-only git init, add and commit (identity r25w2); sandbox-only ls, wc, grep -c and tools/tsukuroi-census.sh --selftest
Model: anthropic/claude-haiku-5-5 (as exposed by the host project context)
Installs: none
