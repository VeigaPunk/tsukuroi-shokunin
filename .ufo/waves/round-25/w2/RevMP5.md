Verdict: partly holds. The three defaults (60 percent, 30 seconds, 90 percent), the memory-and-swap conjunction, the 5 percent candidate floor and capture lines 106 to 108 all match the pinned systemd v262 bytes, but the MP5 row leaves out a second gate on the memory-pressure path and the kill scope of the swap rule, has no located quote for the 5 percent floor or for the "0 means use the default" rule, and the gate that counts MP5 as verified never compares a quote with source bytes.

# Pinned sources checked

Fetched by ordinary GET from public URLs and hashed locally. Copies are in /fast/scratch/hyaku/tsukuroi-r25/w2/RevMP5/.

- https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml, sha256 36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617. Matches the lane's S120 hash.
- .../v262/src/oom/oomd-manager.h, sha256 577eb8b46eab96395f61c9eeb90d34e4d8d9194826b79af19eb80a93feaa2f4b. Matches S124.
- .../v262/src/oom/oomd-manager.c, sha256 052f19b36d54997b78c4ca93fae17d8c8513ce7240b0b58a47a1efdad0da3a15. Matches S123.
- .../v262/src/oom/oomd-util.c, sha256 2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a.
- .../v262/src/oom/oomd-conf.c, sha256 2b3a3335118bf2a686bc3b3da3b2560ab1a53f7a1668ef817d1683321319fdac.
- .../v262/src/oom/oomd-util.h, sha256 79f3daac674b8fb1a5333576ff52f1b2ba1dfcc2416e7a4a73466839553a1ea9.
- .../v262/src/oom/oomd.conf, sha256 c4aafc5d01251d260a578a4a2bbf345a12aff281902bcfe77413f41e93f6a93c, 928 bytes.
- .../v262/man/systemd.resource-control.xml, sha256 d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8. Matches S121.
- Linux v7.2 Documentation/admin-guide/cgroup-v2.rst, sha256 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad. Matches the lane's S118 hash.
- https://man.archlinux.org/man/oomd.conf.5.txt, sha256 1da98cb11b784da7a061c5aa542f9f2a02735f745be8e8b6323b1125219e4a63. Footer reads "systemd 262.1".
- https://man.archlinux.org/man/systemd.resource-control.5.txt, sha256 7d16b3d5c5ca786e8756679792ae95d64ad1348245ae07687894ef77f8b14422.
- The v262.1 tag has the same bytes as v262 for oomd-manager.h, oomd-manager.c, oomd.conf.xml, oomd.conf, oomd-util.c, oomd-util.h, oomd-conf.c and systemd.resource-control.xml. I compared the hashes for all eight.

# What holds

H1. Defaults. oomd.conf.xml:172 reads "between 0% and 100%, inclusive. Defaults to 90%." (SwapUsedLimit). Line 190 reads "above. Defaults to 60%." (DefaultMemoryPressureLimit). Line 202 reads "Defaults to 30 seconds when unset or 0." (DefaultMemoryPressureDurationSec). The compiled-in constants are oomd-manager.h:25-27, and oomd-conf.c:68-71 applies them. oomd-conf.c:33-46 maps an empty or zero duration to 30 seconds. [obs]

H2. Conjunction. oomd.conf.xml:167 reads "the fraction of memory used and the fraction of swap used on the system are both more than", and line 168 continues "what is defined here". The code requires both arms at oomd-manager.c:478-479, using oomd_mem_available_below and oomd_swap_free_below with the same limit (10000 minus SwapUsedLimit in permyriad). The memory arm is MemAvailable below 10 percent of MemTotal (oomd-util.c:147-155). The swap arm is SwapFree below 10 percent of SwapTotal (oomd-util.c:157-165). Memory used is MemTotal minus MemAvailable (oomd-util.c:791). [obs]

H3. 5 percent floor. oomd.conf.xml:168-169 reads "greater than 5% of total swap". The code defines THRESHOLD_SWAP_USED_PERCENT 5 at oomd-manager.h:29-30, computes the threshold as swap_total times 5 over 100 at oomd-manager.c:496-497, and at oomd-util.c:639-640 skips any candidate whose swap_usage is at or below that threshold. This floor is per cgroup. It is not a share of system swap. [obs]

H4. Limit 0. systemd.resource-control.xml:1560-1561 reads "Defaults to 0%, which means to use the default set by oomd.conf(5)." Line 1563 reads "This property is ignored unless ManagedOOMMemoryPressure=kill." The code agrees. oomd-manager.c:124-125 drops an auto cgroup and skips its limit. oomd-manager.c:141-146 uses the default when the message limit is zero. The Arch 262.1 text at lines 1329-1330 says the same. [obs]

H5. Capture. capture.txt has sha256 e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136, which matches the declaration. Line 106 is "#SwapUsedLimit=90%", line 107 is "#DefaultMemoryPressureLimit=60%" and line 108 is "#DefaultMemoryPressureDurationSec=30s". Each of the three texts occurs exactly once in the capture. Capture lines 87 to 108 are byte-identical to lines 1 to 22 of the upstream oomd.conf (diff exit 0). Line 105 is "[OOM]" and line 83 is "1", as the row says. [obs]

H6. Host package state. capture.txt:9 reads "systemd 262 (262-1-arch)". Read-only `pacman -Q systemd` printed "systemd 262-1". `pacman -Qo /etc/systemd/oomd.conf` printed that the file is owned by systemd 262-1. `pacman -Qkk systemd` printed "systemd: 1995 total files, 2 altered files" and no line that mentions oomd. The host file is 928 bytes, the same size as the upstream file. So the file is the unmodified packaged default with no active key, and the row's statement about the shipped defaults holds. [obs]

H7. Numbers. capture.txt:66-69 gives MemTotal 31721800 kB, MemAvailable 23863792 kB, SwapTotal 31722876 kB and SwapFree 30005224 kB. My arithmetic gives memory used 24.77 percent and swap used 5.41 percent, which matches the row. [obs]

H8. Version. The v262.1 tag matches v262 for every MP5 source file, so the open 262.1 question in the lane notes is closed for these files. The Arch 262.1 text also gives 90, 60 and 30 at its lines 159, 176 and 187. [obs]

# Findings

1. Defect, medium. [obs] The row does not say what the swap action kills. The 5 percent floor selects one descendant cgroup, and oomd then sends SIGKILL to that cgroup and to all of its descendants. oomd-util.c:366 calls oomd_cgroup_kill with recurse set to true. oomd-util.c:273-283 uses cg_kill_kernel_sigkill, with cg_kill_recursive as the fallback. The dry-run message at oomd-util.c:511 says "kill %s and all its descendants". The kernel document cgroup-v2.rst:1055-1057 says: "Writing "1" to the file causes the cgroup and all descendant cgroups to be killed." The row says "only on descendant cgroups holding more than 5 percent of total swap" (memory-pressure-r25.md:268-269). A reader could take that to mean that smaller descendants are spared. The manual's sentence at oomd.conf.xml:168-169 has the same simplification, and the row copied it. Suggested wording: the rule selects one descendant with more than 5 percent of total swap and SIGKILLs it together with all of its descendants.

2. Defect, medium. [obs] The memory-pressure path has a second condition that the row never states. A cgroup that stays over the pressure limit for the duration is skipped unless it had reclaim activity in the last 30 seconds. oomd-manager.c:596 reads `if ((now(CLOCK_MONOTONIC) - t->last_had_mem_reclaim) > RECLAIM_DURATION_USEC) continue;`. RECLAIM_DURATION_USEC is 30 seconds (oomd-manager.h:32). last_had_mem_reclaim becomes the current time whenever the page-scan (reclaim) rate is above zero (oomd-util.c:826-827 and 859-860). After a pressure kill, a 15-second post-action delay applies (oomd-manager.h:33; oomd-manager.c:574-579). The manual mentions reclaim only as the order in which candidates are taken (oomd.conf.xml:186-187), not as a gate. None of the MP5 row, its JSON entry, SKILL.md line 2317 or the round-25 lesson mentions reclaim. As a result, 60 percent for 30 seconds does not by itself predict a pressure kill. The row's conjunction discussion covers only the swap arm.

3. Defect, medium. [obs] Two of the row's claims have no located quote. (a) The 5 percent floor. The row's quotes are S120 lines 167, 172, 190 and 201-202, plus the "Overrides" sentence from S121 (memory-pressure-r25.md:298-303; memory-pressure-r25.json:368-389 and 401-420). None of them is oomd.conf.xml:168-169 or oomd-manager.h:30. The lesson's Gate table (corpus/lessons/round-25.md:23-27) does not quote the floor either. The S120 row in SOURCES.md:126 states the 90, 60 and 30 defaults and the memory-with-swap pairing, but not the 5 percent floor. (b) "A unit's ManagedOOMMemoryPressureLimit=0 means use the default." The only S121 quote in the row says "Overrides the default memory pressure limit set by oomd.conf(5) for the cgroup of this unit." That sentence supports neither half of the rule. The text that does support it, systemd.resource-control.xml:1560-1561 and 1563, is not cited. The "ignored unless kill" half is backed by an S123 Gate quote, "if (message.mode == MANAGED_OOM_AUTO) {" at round-25.md:22 (oomd-manager.c:124), but the MP5 row does not cite S123. The checker needs only one qualifying quote per row (tools/check-memory-pressure.py:578-586 and 606-609), so these gaps pass.

4. Gap, low. [obs] The S121 location does not match the registered source. memory-pressure-r25.md:302-303 cites "systemd v262 man/systemd.resource-control.xml ... plain-text rendering lines 1325-1328". In the pinned XML the sentence is at lines 1558-1560. Lines 1327-1328 match only the Arch 262.1 plain-text page. memory-pressure-r25.json:414-418 gives the URL https://man.archlinux.org/man/systemd.resource-control.5, which the lane's own lesson says is not registered (corpus/lessons/round-25.md:34). The quoted wording is exact.

5. Gap, medium. [obs] The gate that marks MP5 verified never tests a quote against source bytes. tools/check-memory-pressure.py reads only the lane's own repository at a revision (lines 93-101, through git show). It compares entry quotes only with the lesson's Gate table (lines 603-605), and that comparison is non-blocking (blocking=False). A mismatch therefore cannot change `verified` (line 634). The entry's additional_located_quotes are never read: the only entry fields read are row.get('sources') at line 548 and row.get('quotes') at line 587. So "6 verified rows, exit 0" does not show that any MP5 quote appears in systemd v262. I checked the five quotes that the row counts, and all five appear at the stated lines. The gate would not have caught finding 4.

6. Observation, low. [obs] "The swap rule" is not scoped to the [OOM] SwapUsedLimit rule. A ruleset with SwapUsageMax= and no MemoryPressureAbove= acts on swap alone (oomd-manager.c:797-817). The manual combines the two conditions with AND only when both are set (oomd.conf.xml:86-88). Kill-by-swap rulesets use the same 5 percent floor (oomd-manager.c:755-756). The row should name the [OOM] rule.

7. Observation, low. [obs] The swap arm has no duration and no post-action delay. The swap handler at oomd-manager.c:447-524 never reads a duration. The duration is used only in the message parser (151-154 and 218), the pressure handler (591-642), and the dump (1372). Post-action delays appear only in the pressure path (574-579 and 635) and the ruleset path (958 and 996-1000). [inf] While both arms still hold, the swap rule may select another candidate on the next 150-millisecond tick (oomd-manager.h:13). I did not test this at runtime. The swap rule also needs at least one unit with ManagedOOMSwap=kill, because the swap timer stays off while the monitored map is empty (oomd-manager.c:222-224 and 452). That point belongs to MP4.

8. Observation, minor. [obs] memory-pressure-r25.md:291-292 says the "1" line "occurs twice" in the capture. Only capture.txt:83 has exactly "1". The count and its reading are correct, so no count changes.

9. Observation, minor. [obs] The row's "fraction of memory used" means (MemTotal minus MemAvailable) divided by MemTotal (oomd-util.c:791). It does not mean MemTotal minus MemFree, and it is not the "used" column of free. The row's 24.77 percent uses the code's formula, so the number is consistent. Readers who compare it with free will get a different figure.

# Quote check

| Quote as the lane cites it | Lane location | Pinned location | Result |
|---|---|---|---|
| "between 0% and 100%, inclusive. Defaults to 90%." | oomd.conf.xml:172 | line 172 | exact |
| "above. Defaults to 60%." | oomd.conf.xml:190 | line 190 | exact |
| "Must be set to 0, or at least 1 second. Defaults to 30 seconds when unset or 0." | :201-202 | line 202 | exact; the cited range is loose |
| "the fraction of memory used and the fraction of swap used on the system are both more than" | :167 | line 167 | exact, 18 words |
| "#define DEFAULT_MEM_PRESSURE_LIMIT_PERCENT 60" | oomd-manager.h:26 | line 26 | exact |
| "#define DEFAULT_SWAP_USED_LIMIT_PERCENT 90" | oomd-manager.h:27 | line 27 | exact |
| "Overrides the default memory pressure limit set by oomd.conf(5) for the cgroup of this unit." | "plain-text rendering lines 1325-1328" | XML 1558-1560; Arch 262.1 text 1327-1328 | wording exact; location not pinned |
| "if (message.mode == MANAGED_OOM_AUTO) {" (S123, not cited by MP5) | oomd-manager.c:124 | line 124 | exact |
| Capture lines 106, 107, 108 | capture.txt | lines 106-108 | exact, each unique |

# Residual risk and verification gaps

- [unk] There was no runtime test. Every finding rests on source text or capture bytes.
- [unk] I did not read cgroup-util.c. The recursion claim rests on oomd's own fallback function name and on the kernel's cgroup.kill description.
- [unk] I did not measure how often the reclaim gate or the swap repetition would matter on this host.
- [inf] The MP4 and MP5 rows can be read together. I checked only the MP5 touchpoints of MP4.
- I did not rerun tools/check-memory-pressure.py. My statements about its behaviour come from reading lines 93-101, 548, 578-587, 603-605, 606-609 and 634.

# Suggested corrections, not applied

1. Add to MP5 the kill scope from finding 1, the [OOM] scoping from finding 6, the reclaim gate and the 15-second delay from finding 2, and the absence of a duration on the swap arm from finding 7.
2. Add located quotes for the 5 percent floor (oomd.conf.xml:168-169 or oomd-manager.h:30) and for the 0 rule (systemd.resource-control.xml:1560-1561 and 1563). Cite S121 and S123 in the row's sources.
3. Correct the S121 location to pinned XML lines 1558-1560, and remove the Arch URL from the JSON additional quotes or register that page.
4. Make MP-QUOTE-MISMATCH blocking, and have the checker read additional_located_quotes. Better still, have it match each quote against the registered source bytes.

Scope: read=SCORECARD.md lines 784-812 (C2 declaration and refinements), corpus/knowledge/memory-pressure-r25.md lines 263-308, corpus/knowledge/memory-pressure-r25.json lines 333-420, corpus/SOURCES.md rows S118-S124, corpus/lessons/round-25.md lines 22-34 and 66, SKILL.md line 2317, corpus/knowledge/oom-event-plane.md line 344 and the appended notice from line 471, tools/check-memory-pressure.py lines 93-101, 548, 578-587, 603-609 and 634, .ufo/waves/round-25/capture/capture.txt lines 1-12, 59-155 and capture.sh, and the systemd v262, v262.1 and Arch manual copies listed above; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RevMP5.md and scratch copies under /fast/scratch/hyaku/tsukuroi-r25/w2/RevMP5/; executed=curl GET of the public raw and man URLs listed above, sha256sum, wc -c, diff, sed, grep, stat, pacman -Q systemd, pacman -Qo /etc/systemd/oomd.conf, pacman -Qkk systemd (all read-only), systemd-analyze cat-config systemd/oomd.conf (read-only), python3 arithmetic on capture values
Model: not exposed
Installs: none
