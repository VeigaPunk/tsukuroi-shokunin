# RevC1Capabilities: attack on the round-25 capabilities table at 5e7c04ec

Verdict: Partly holds. Every number and every pointer path in the appended capabilities table re-derives at 5e7c04ec (97 census cases, 45 boot-chain cases, 125 registry rows, six limine entries, nine pointer paths). But the boot-chain row's live receipt was produced by an older audit tool, the host-census-gate row cites receipts that say 80 cases where the row says 97, and the live census rollup rests on a 2026-10-19 receipt.

Measured revision: 5e7c04ecb02735491456de2b8bc44550d0db4609. Sandbox: /fast/scratch/hyaku/tsukuroi-r25/w2/RevC1Capabilities/ (git archive, empty git init, no remote). Table lines: /fast/scratch/hyaku/tsukuroi-r25/w2/RevC1Capabilities/SCORECARD.md:840-861 (rows at 852-855).

## Findings

1. [obs] Medium. The boot-chain row's only live receipt came from an older tool version.
   - Evidence: /fast/scratch/hyaku/tsukuroi-r25/w2/RevC1Capabilities/.ufo/waves/round-17/l1-capture/audit-live.txt line 2 records "tool sha256 495750fbced6218f1c137af3aef1232e59305ebf2f5ce9ab47dbd4546fe72ab1". `git show 90037c2:tools/boot-chain-audit.sh | sha256sum` gives 495750fb. `git show 5e7c04ec:tools/boot-chain-audit.sh | sha256sum` gives cd398e60, which matches the sandbox copy.
   - `git diff 90037c2 5e7c04ec -- tools/boot-chain-audit.sh` shows 13 insertions and 3 deletions. The rule-2 input set changes from /usr/lib/modules/$(uname -r) to every /usr/lib/modules tree (sandbox file line 482), and /etc/limine-snapper-sync.conf is added. An unparseable image under EFI/Linux now reports EVALUATION-ERROR instead of not-kernel (sandbox file lines 314-329). Commit 5a133bc (round 19) made both changes.
   - SCORECARD.md:612 mentions gate hardening at 5a133bc but not the audit rule change. Table line 855 still cites only the round-17 receipt.
   - Consequence: the sentence "6 entries, CONSISTENT, exit 0" attests the round-17 rules, not the rules the row now describes.

2. [obs] Medium. A newer live receipt from the same tool blob exists, and the row omits it.
   - /fast/scratch/hyaku/tsukuroi-r25/w2/RevC1Capabilities/.ufo/waves/round-24/l1/bootchain-live.txt line 8: "# counts entries=6 kernels=5 booted=0 path-aliased=3 pre42=1 untested=1 not-kernel=1 unknown=0 b2_mismatch=0"; line 9: "TSUKUROI_BOOTCHAIN: CONSISTENT". Its first data row shows selected=true and verdict PATH-ALIASED-EMULATED. The round-17 receipt's same row shows BOOTED-OBSERVED (audit-live.txt line 5).
   - The round-24 base f169b3ba and the claim base b9046016 both carry blob cd398e60, so this receipt most likely came from the measured tool [inf]. The round-24 receipts record no tool hash.
   - Meaning: on this host the audit binds the firmware-selected entry (selected=true), but the proven-booted rule does not fire (booted=0). The row's words "binds the firmware-selected entry" are true, but its evidence shows only the older, stronger result. The same counts appear in .ufo/waves/round-24/w1/ExecBootChainAudit/live.out under the same sandbox root.
   - Why rule 2 fails now is unknown [unk]. The round-19 widening of the /usr/lib/modules input is a plausible cause [inf].

3. [obs] Medium. The host-census-gate row attributes 97 cases to receipts that say 80.
   - SCORECARD.md:853 cites .ufo/evidence/round-1-kaika/scout-live.md and .ufo/evidence/round-1-kaika/after.md. after.md line 167 reads "TSUKUROI_CENSUS_SELFTEST: PASS (80 cases, 80 passed, 0 failed)". scout-live.md line 23 says the same, 80.
   - The 97 figure is supported by .ufo/waves/round-12/resumed/selftest-after.json (the text "97" appears in it) and by my re-run (finding 4). The cited receipts do not show it.

4. [obs] Counts re-derived at 5e7c04ec. Most hold, with two wording gaps.
   - Census selftest, run in the sandbox: "TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)", rc=0 (census-selftest.out line 100). The file has 97 PASS lines, no FAIL lines, and two SKIP lines at lines 85-86 that sit outside the 97. The counter is PASS plus FAIL (tools/tsukuroi-census.sh:2608-2609).
   - The table says the selftest "prints PASS 97/97 rc=0". The printed text is the parenthesis form above, not "PASS 97/97" [obs] low. The C1 checker reads "(97 cases" and accepts it, so the count passes.
   - The table does not mention the two skipped root-fixture cases. Round 12 did (SCORECARD.md:258-259).
   - Boot-chain selftest: "TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=45 failed=0", rc=0 (bootchain-selftest.out line 1). The counter is the st_check call count (tools/boot-chain-audit.sh:815-816, 1217). Holds.
   - Boot-chain receipt: six TSV rows (audit-live.txt lines 5-10), "entries=6" (line 11), "TSUKUROI_BOOTCHAIN: CONSISTENT" (line 12), rc=0 (line 13). Holds for the row's figures, subject to finding 1.
   - Registry: 125 rows, S001 (corpus/SOURCES.md line 7) to S125 (line 131), contiguous, no duplicates, each row 13 fields. Tiers A=116, B=2, C=7. Statuses mined=111, queued=5, rejected=9. Holds.
   - The only receipt cited next to the registry count, after.md lines 6-7, says 34 rows. No receipt in that cell records 125 [obs] low.

5. [obs] Low to medium. "Checked by the frozen contract's census commands" holds for the contract, but not for the reverse citations.
   - after.md lines 6-37 hold the seven contract commands: row count, malformed rows, tier counts, status counts, duplicate ids, enum check, and missing used-by paths. I ran all seven on the 125-row file: rows 125, malformed 0, duplicates 0, enum violations none, missing paths none.
   - after.md lines 40-42 hold a command labelled "supplemental". It fails for 22 registry rows (23 row-file pairs): S055, S059 (two files), S064, S087-S090, S093, S094, S096-S098, S102, S103, S106-S108, S111, S112, S123-S125. Example: S123-S125 cite corpus/knowledge/memory-pressure-r25.md, which does not name them. The table does not mention this.

6. [obs] Medium. The live census claim was not re-measured this round.
   - scout-live.md line 24 reads "rc=1" with rollup DEGRADED, captured in round 1 (after.md line 3, 2026-10-19).
   - I did not run the live census. Its probes call pacman -Sup --print-format (tools/tsukuroi-census.sh:1518), pacman -Suu --print-format (:1542) and pacman -Sl (:1594). The host rules forbid running pacman -S this round.
   - Whether the live exit is still 1 today is unknown [unk].

7. [obs] Low. "Read-only" holds. "Touches no live host surface" holds for the census's own probe inputs, but not for every process in the run.
   - Static: no write redirection, tee, touch, mkdir or cp appears in the live path before the selftest (lines 1-1710). The selftest env block (tools/tsukuroi-census.sh:1918-1944) overrides every host seam named in the header (lines 317-329). The default host paths at lines 351-386 are covered, except TSUKUROI_VERCMP, which only compares version strings.
   - Dynamic: strace -f on the selftest in the sandbox (rc=0; trace at /fast/scratch/hyaku/tsukuroi-r25/w2/RevC1Capabilities/census-strace.txt) shows every pacman, systemctl, journalctl, dmesg, nvidia-smi, lsmod, expac and pacman-conf call going to /tmp/tsukuroi-r3-2-selftest.*/bin stubs. No census probe opened a host path.
   - Child tools still read some live host files. GNU sort read /sys/fs/cgroup/.../cpu.max, /sys/fs/cgroup/cgroup.controllers and /proc/self/cgroup, 372 times each, for its CPU-count default. grep read /proc/self/maps 2919 times. bash read /etc/passwd 2940 times. glibc read /etc/nsswitch.conf and /etc/ld.so.cache. The counts equal the sort, grep and bash execution counts from the same trace [inf]; I confirmed the reading pid is sort for four sampled cgroup reads. PATH lookups also stat files under ~/.local and ~/.grok, without reading contents.
   - Verdict for this row: the claim holds for what the census reads. It does not hold as a literal statement about every process in the run.

8. [obs] Holds. Root-metadata-observer row.
   - The root arm is composed into the packages line, and every selftest case asserts that (tools/tsukuroi-census.sh:1952-1953). That includes the early-return BLOCKED cases: "C1 root arm survives pacman=missing early return" (lines 2581-2584), and the db.lck, empty-db and sample-rc variants.
   - 0555 is report-only (lines 2500-2504). Unavailable, non-directory and unsafe-override metadata is BLOCKED (lines 2539-2576). The root_dir field-boundary check (lines 1954-1955) isolates the fixture.
   - The census script's blob hash is identical at 70fede2 (round 12) and 5e7c04ec (d17d32a3), so the round-12 receipts describe this code.

9. [obs] Low. Boot-chain row wording, clause by clause.
   - "copies each UKI with a read-only sudo -n cat": holds (tools/boot-chain-audit.sh:260-262 and :1287). The copy also covers the non-UKI fallback /EFI/BOOT/BOOTX64.EFI (audit-live.txt line 10).
   - "every limine entry": overstated. The parser emits one record per path: line (lines 545-561). An entry with no path: line is skipped silently.
   - "types the new_root path": holds. The image_new_root column classifies the type of /new_root (header lines 74-76). Round 11 wrote the token /new_root in backticks, and round 25 dropped it. That is not a misstatement, but the path grammar in the C1 checker would have read the token as a path.
   - "binds the firmware-selected entry": holds (efivar reads at lines 496-502; round-24 selected=true).
   - Note for the L1: live mode calls "sudo -n stat -c %Y", which is not the literal sudo form in the operator's read-only list ("sudo -n stat <path>"). This is the tool's design, not a table error.

10. [obs] Holds. Pointer paths. All nine pointer paths in the table exist at b9046016 and at 5e7c04ec (git cat-file -e). The preamble's statement that they were re-checked holds. The table has four rows with the same four names as the round-11 table (SCORECARD.md:159-164).

## Residual risk and verification gaps
- The live census and the live boot-chain audit were not run this round. The census live path needs pacman -S (finding 6). The audit's live mode needs a sudo stat form outside the listed allowance. Current host state is unmeasured.
- I did not read the round-13 to round-16 corrections touching the root arm (SCORECARD.md:286-500). I relied on the census blob hash being unchanged since round 12.
- The round-24 receipts carry no tool hash. The same-blob conclusion is an inference from the base commits.
- The strace is one run. It shows the path the 97 cases take, not every branch. The child-tool counts in finding 7 are inferred from matching counts, not from a full pid map.
- I did not run tools/check-self-assessment.py, which belongs to another seat. I read only its capability checks (the case-count check at lines 447-452 and 522-529, and the path checks at lines 582-591).

Scope: read=sandbox copy of 5e7c04ec (SCORECARD table, tools/tsukuroi-census.sh, tools/boot-chain-audit.sh, corpus/SOURCES.md, .ufo receipts from rounds 1, 12, 17 and 24), git history and blob hashes for 70fede2, 90037c2, 5a133bc, 5e7c04ec, b9046016 and f169b3ba, the host rules file ~/.omp/agent/RULES.md, and the godspeed skill file; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RevC1Capabilities.md (created the w2 directory with mkdir -p), /fast/scratch/hyaku/tsukuroi-r25/w2/RevC1Capabilities/ (sandbox, git init with no remote, census-selftest.out, census-selftest-traced.out, bootchain-selftest.out, census-strace.txt, census-paths.txt, host-reads-by-pid.tsv, host-read-pids.txt); executed=git -C lane archive 5e7c04ec | tar -x into the sandbox, then git -C sandbox init -q (rc 0); bash tools/tsukuroi-census.sh --selftest (rc 0, 97 cases); bash tools/boot-chain-audit.sh --selftest (rc 0, total=45); strace -f -qq -e trace=... bash tools/tsukuroi-census.sh --selftest (rc 0); git -C lane cat-file -e for 9 paths at 2 revisions; git -C lane show <rev>:<path> | sha256sum (read only); git -C lane log, diff --stat and diff (read only); the registry census commands from after.md lines 6-42 run against the sandbox corpus/SOURCES.md; grep, awk, sed, sort, wc and sha256sum reads; one background classification job (bg_5235) cancelled by me
Model: anthropic/claude-haiku-5-5 (host project-context value; not independently confirmed)
Installs: none
