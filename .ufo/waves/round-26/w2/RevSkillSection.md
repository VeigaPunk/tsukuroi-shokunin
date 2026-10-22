# RevSkillSection: review of SKILL.md "Storage integrity — round 26", SE1 to SE4, and the round-26 registry table

Verdict: Partly holds. The six SH rows match the entry JSON cell for cell on verdict, host reading and operator action, and the registry carries round 25 forward with only the two stated self-assessment cells changed and one storage-health row appended. It fails on the error patterns (SE2 and part of SE4 have no cited source, SE1's prefix has none either, and SE4's literal has the wrong spacing and overstates "no record" as "never run"), on two command cells that omit the commands behind cited readings, on one unsourced `btrfs filesystem df` reading, on a fourth verdict outside the fixed vocabulary, and on a dangling "named below" reference.

Basis: all SKILL.md, corpus, tool and capture line numbers are at revision 7dfea9244a84a0e2439f0698e54491e5d7b7c467. I read committed bytes from a git-archive copy at /fast/scratch/hyaku/tsuku26/w2/RevSkillSection/src/, and its SKILL.md is byte-identical to `git show` at that revision. I did not read the lane working tree. Upstream sources were fetched read-only over HTTPS.

## Findings

1. [fails] SE2 and part of SE4 have no cited source, and SE1's prefix has none either.
   - The literal `forced readonly` (SE2) appears in no registered snapshot. Searching /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/ finds only S132.c:354, a comment that reads "forced read-only" with a hyphen.
   - The literal is printed upstream: https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/messages.c line 176, `btrfs_info(fs_info, "forced readonly");`. That is info level, so an error-level filter would miss it. The SKILL does not say the level.
   - `no stats available` (SE4) appears in no snapshot. It is printed upstream: https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c line 321, `pr_default("\tno stats available\n");`.
   - The SE1 prefix `BTRFS error (device ...)` comes from https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/messages.c line 236, `"%dBTRFS %s (device %s%s): %pV\n"`. Only the body `bdev %s errs: wr ...` is in a registered snapshot (S132.c:8428-8429).
   - None of messages.c, fs/btrfs/fs.c, super.c, disk-io.c or btrfs-progs cmds/scrub.c has a row in corpus/SOURCES.md (rows S128 to S139, lines 134-145). The entry's source header (corpus/knowledge/storage-health-r26.md:1) lists S128-S135 and S139 only.
   - Fix: register those upstream files as SOURCES rows, cite them in SE1, SE2 and SE4, and state that SE2 is info level.

2. [fails] The SH2 zero count misses one kernel line form, and no SE pattern covers it.
   - messages.c lines 150-151 print `pr_crit("BTRFS: error (device %s%s) in %s:%d: errno=%d %s (%pV)\n", ...)`. The colon after BTRFS matters.
   - The capture's second grep (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt:157) is `BTRFS (error|critical|warning)|forced readonly`. A Python regex test of that pattern matches the bdev error line and the forced-readonly line, but not the `BTRFS: error (device ...) in` line. PCRE gives the same result for these literals [inf].
   - messages.c lines 166-170 return before the forced-readonly line when the filesystem is not yet mounted or is already read-only, so the `BTRFS:` line can appear alone [inf].
   - So "0 BTRFS error, critical, warning or forced-readonly lines" (SKILL.md:2364) is not exhaustive. Add a `BTRFS: error (device` pattern to SE1 or a new SE5, and to the SH2 command.

3. [fails] The SH2 command cell omits the second command behind its reading.
   - SKILL.md:2364 lists only `sudo -n journalctl --no-pager -o short-iso _TRANSPORT=kernel --grep 'BTRFS.*errs: wr'`.
   - The host reading's "0 BTRFS error, critical, warning or forced-readonly lines" comes from capture.txt:157-158, `--grep "BTRFS (error|critical|warning)|forced readonly" | grep -cE ...`, output `0`, exit 1.
   - The second command is read-only and inside the allow-list (`sudo -n journalctl --no-pager <read options>`), but a reader cannot reproduce the reading from the table.

4. [fails] The SH4 command cell omits the two commands behind two of its readings.
   - SKILL.md:2366 lists `sudo -n btrfs scrub status /` and `systemctl is-enabled btrfs-scrub@-.timer`.
   - "/var/lib/btrfs absent (line 127)" comes from `sudo -n ls -la /var/lib/btrfs` (capture.txt:126-128: "No such file or directory", exit 2).
   - "inactive (line 134)" comes from `systemctl is-active btrfs-scrub@-.timer` (capture.txt:133-135: "inactive", exit 3). The table lists only is-enabled.

5. [fails] The `btrfs filesystem df` leg of SH3 has no evidence.
   - SKILL.md:2365, corpus/knowledge/storage-health-r26.md:45 and storage-health-r26.json:131 all say "metadata and system profiles dup (`btrfs filesystem df` and sysfs allocation directories)".
   - No such command or output exists in capture.txt, and the round-26 lesson does not carry it. The claim appears only in the entry.
   - The sysfs leg is grounded: capture.txt:64 (single), :79 (dup under metadata), :100 (dup under system).
   - Fix: capture the command, or delete the leg.

6. [fails] UNVERIFIED is a fourth verdict outside the fixed vocabulary, and the section does not say so.
   - SKILL.md:25-27 fixes the vocabulary as `HEALTHY` | `DEGRADED` | `BLOCKED`, "three states, never a scalar score" (round 1).
   - The round-26 section uses `UNVERIFIED` for SH4 (SKILL.md:2366) and SE4 (SKILL.md:2375).
   - The round-25 section handles the same issue by stating that its verdict words are not the plane words (SKILL.md:2305). The round-26 section has no such statement.
   - The entry JSON does declare four states ("verdict_vocabulary" in storage-health-r26.json).

7. [fails] SE4 overstates, and its literal has the wrong spacing.
   - (a) SKILL.md:2375 says "no scrub has run". SH4 (SKILL.md:2366) and the upstream code support only "no scrub record". cmds/scrub.c lines 320-321 print "no stats available" when no status record was loaded (`!ss || !ss->t_start`) [inf].
   - (b) SKILL.md:2375 writes `Error summary: no errors found` with one space. The real line has four spaces: capture.txt:124 reads `Error summary:    no errors found`, S129.rst:180 has the same spacing, and cmds/scrub.c:238 and :249 print "Error summary:   " followed by " no errors found". A literal search with the SKILL's spacing matches neither file. A regex with four spaces matches both (Python test).

8. [fails, low] The "named below" reference dangles.
   - SKILL.md:2381 says "except the two cells of the `self-assessment` row named below". Nothing follows the table: the file ends at line 2415 with the storage-health row.
   - The two changed cells are column 3 (verdict map: "0 all 23 fixed checks match" becomes "0 all 27 fixed checks match") and column 5 (pinned values: "R25 fixed check set K01 to K23" becomes "R26 fixed check set K01 to K27").
   - Fix: name the two cells below the table.

9. [obs] The privileged-read list in the Authority line is not exhaustive. SKILL.md:2359 lists four commands. SH2 uses `sudo -n journalctl --no-pager ...` (SKILL.md:2364), and the SH4 absence check used `sudo -n ls -la` (capture.txt:126). Both are on the allow-list.

10. [obs] Some action forms are outside the allow-list form.
    - SH1's action (SKILL.md:2363) offers `btrfs device stats <mountpoint>` without sudo. The allow-listed form is `sudo -n btrfs device stats`, and the unprivileged form is not on the no-sudo list.
    - SH5's action (SKILL.md:2367) gives `sudo smartctl -H -A <device>` without `-n`.
    - SH6 uses `sudo -n nvme smart-log`, which nvme-cli 3.1-1 flags as deprecated (capture.txt:207: "WARNING: 'smart-log' is deprecated and will be removed in the next major version, use 'nvme log smart' instead"). The command is allowed and matches the capture, but the warning is worth noting.

11. [obs] Two sentences have no source or command.
    - SE3's "Media errors are a replacement question for the operator, never something to scrub around" (SKILL.md:2374): the word "replacement" appears in no entry, JSON file, capture or round-26 lesson.
    - SE1's "record ... its boot" (SKILL.md:2372) gives no read-only command that maps a journal line to a boot. capture.txt:160 uses `journalctl --list-boots`, which the SKILL does not list.

12. [obs] The SE1 to SE4 patterns cite no source identifier, so a reader cannot check grounding from the SKILL section alone.

## What holds

- SH1 to SH6: the verdict, host reading and operator action cells equal the JSON rows after removing backticks and collapsing whitespace (6 of 6; Python comparison of SKILL.md:2363-2368 with storage-health-r26.json).
- Capture pointers in the SH cells match capture.txt: 40-44, 112-116, 64, 121, 127, 131, 134, 154-161, 181, 184, 186-188, 194, 196-198, 221, 223-225.
- SE3 literals match S134.cpp:450-451 (`SMART overall-health self-assessment test result: %s` with `FAILED!`), S134.cpp:491 (`Critical Warning:` with `0x%02x`) and S134.cpp:458-459 (bit 0x01 means spare below threshold). SH5's "PASSED exactly when the byte is 0" matches S134.cpp:448-451 and the call at S134.cpp:840.
- The SE1 body matches S132.c:8428-8429 exactly. The info-level mount line is suppressed when all counters are zero (S132.c:8446), as SH2 states.
- SH4's status-file path `/var/lib/btrfs/scrub.status.<UUID>` matches cmds/scrub.c:67 and scrub_datafile (lines 446-460: base name, dot, filesystem UUID).
- Every SH command is read-only, and none uses -z, -t, -s, -X or -i. `btrfs scrub start /` appears only as an operator suggestion (SKILL.md:2366).
- The checker reads git only through `git show` and `ls-tree` (tools/check-storage-health.py:243-262). Its selftest writes only inside TemporaryDirectory (lines 959-973).
- Registry row storage-health (SKILL.md:2415): the entry command, self-test command, pinned sha256 (002bef16..., equal to tools/check-storage-health.py:62 and to `sha256sum` of capture.txt), and verdict map match the checker. Exit 0 only when verified_rows equals 6 (lines 798-799); exit 2 for could-not-evaluate (lines 485, 496) and for usage errors (line 1319). The selftest run in the sandbox exited 0 with no failing case (/fast/scratch/hyaku/tsuku26/w2/RevSkillSection/selftest.out).
- Registry carry-forward: the header and separator are the same. The 28 round-25 rows (SKILL.md:2328-2355) are identical to the round-26 rows except self-assessment (line 2413), which changes in the two cells in finding 8. One row, storage-health, is appended at line 2415. The whole SKILL.md diff from e9f5356c to 7dfea92 is a pure 60-line insertion after line 2355 with no deletions, so the round-25 table is byte-identical to the claim base.

## Residual risk and verification gaps

- Residual risk: finding 2. An error that leaves the filesystem already read-only, or that occurs during mount, prints only the `BTRFS: error` line, and the SKILL's patterns would not flag it.
- [unk] I did not evaluate every entry JSON quote or capture pointer. C1's checker covers those. I ran only its selftest, not revision mode.
- [unk] I did not check the round-26 lesson's gate quotes, which are outside this seat.
- [unk] I ran no host command. All host readings come from the frozen capture.

Scope: read=SKILL.md 24-36 and 2300-2415 at 7dfea9244a84a0e2439f0698e54491e5d7b7c467 (git archive and git show); storage-health-r26.md and .json; tools/check-storage-health.py and tools/_revision.py; tools/check-self-assessment.py (grep only); corpus/SOURCES.md rows S128-S139; .ufo/waves/round-26/sources/*; .ufo/waves/round-26/capture/capture.txt; /home/vgpnk/.omp/agent/RULES.md; upstream linux v7.2 fs/btrfs messages.c, fs.c, super.c and disk-io.c, and btrfs-progs v7.1 cmds/scrub.c; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevSkillSection.md, /fast/scratch/hyaku/tsuku26/w2/RevSkillSection/ (sandbox, base copy, upstream copies, selftest.out), and a mkdir -p on the existing lane directory .ufo/waves/round-26/w2 that changed nothing; executed=git -C <lane> cat-file -t (3 objects), git -C <lane> archive piped to tar -x into the sandbox, git -C <lane> show (e9f5356c and 7dfea92 SKILL.md), git -C <lane> diff --stat (read-only), sha256sum, diff, cmp, wc, ls, grep -c, curl of five public URLs (one optional path returned 404), python3 tools/check-storage-health.py --selftest in the sandbox (exit 0), Python analysis scripts over copies only
Model: anthropic/claude-haiku-5-5
Installs: none
