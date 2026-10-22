# RevMP1 — falsify review of C2 row MP1 (round 25, attempt 1, wave 2)

Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. Measured revision 5e7c04ecb02735491456de2b8bc44550d0db4609.

Verdict: Partly holds. The quotes, the three capture pointers and the arithmetic hold, and the claim that systemd-oomd reads the cgroup `full` line is true at systemd v262; but the row's inference bracket is contradicted by its own cited source, its "verified" verdict rests on code the row never registers, its action points at a file systemd-oomd does not read on this host and omits two of the rule's gates, and the registry sha for its systemd source is wrong.

## Findings, by severity

1. [obs] High. The row says the two systemd and kernel documents do not state the equivalence between the oomd limit and the `full` line. Its own cited source does.
   - The bracket: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md:52-54 reads "[inference from `oomd.conf(5)` ... the two documents do not state the equivalence in so many words]". The JSON notes repeat it at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.json:80.
   - The contradiction: upstream systemd v262 man/oomd.conf.xml (https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml, sha256 36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617, fetched copy /fast/scratch/hyaku/tsukuroi-r25/w2/RevMP1/oomd.conf.xml:95-96) describes the MemoryPressureAbove= option. Its rendered text includes "(PSI full avg10)", which names the `full` line and the avg10 field outright.
   - Effect: the conclusion is correct, but the stated evidence basis is wrong. The bracket should be replaced by a citation to oomd.conf.xml lines 95-96. The row cites lines 182-183 only, and those lines do not name `full`.

2. [obs] High. The verdict "verified" includes a claim the counted evidence does not reach, and no registered source covers the code that proves it.
   - The verdict reads "`verified` — the file on this host carries both lines, and the `full` line is the one the oomd rule reads" (memory-pressure-r25.md:58-59; JSON line 44).
   - The counted pointers (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/capture/capture.txt:14-15) show only that /proc/pressure/memory carries both lines. They say nothing about which line systemd-oomd reads.
   - The code that settles it is upstream v262 src/oom/oomd-util.c (sha256 2e94450aa337dd7d2062f2730e46e22ac00fc2c3195c11654047ddcaba487e7a; fetched copy /fast/scratch/hyaku/tsukuroi-r25/w2/RevMP1/oomd-util.c). Line 680 calls `cg_get_path(path, "memory.pressure", &p)`. Line 684 calls `read_resource_pressure(p, PRESSURE_TYPE_FULL, &ctx->memory_pressure);`. Line 105 tests `if (ctx->memory_pressure.avg10 > ctx->mem_pressure_limit) {`. psi-util.c at v262 maps PRESSURE_TYPE_FULL to the name "full" at lines 130-131.
   - No registry row covers oomd-util.c. A grep for "oomd-util" over corpus/SOURCES.md, corpus/lessons/round-25.md and both memory-pressure-r25 files returns nothing. S123 covers oomd-manager.c only; S124 covers oomd-manager.h only.
   - [obs] The clause is true for upstream v262. [unk] The installed package (262-1-arch, capture.txt:9) was not inspected. Under the entry's own definition, `verified` means the statement holds on this host on counted evidence, and this clause is a source-level claim. Fix: register oomd-util.c lines 105 and 684 with its sha, then either keep `verified` scoped to upstream v262 or use `scoped`.

3. [obs] Medium. The action's test ("whether systemd-oomd would have acted") points at a number systemd-oomd does not read on this host.
   - The counted pointers (capture.txt:14-15) are the system group, /proc/pressure/memory. The statement says the rule reads "that cgroup's memory pressure file" (memory-pressure-r25.md:52-53). Upstream oomd-util.c:680-684 reads the cgroup file.
   - On this host the root slice is `ManagedOOMMemoryPressure=auto` (capture.txt:138-140). Auto cgroups are removed from the monitored set (upstream oomd-manager.c:124-125 at v262). systemd-oomd is inactive (capture.txt:73, exit 3 at line 74).
   - So on this host the system line is not systemd-oomd's input, and no cgroup is monitored. The action should say that and cite MP4, which covers the auto state.
   - Related, and also medium: the action says "quote the `full` share", but the counted tokens are the `total=` values (lifetime totals). The rule compares `full avg10` (oomd-util.c:105; oomd.conf.xml:96). Neither the statement, the verdict nor the action names avg10. A reader who quotes the counted token would quote a lifetime total, which MP2 says the rule does not use.

4. [obs] Medium. The action leaves out two of the gates that decide whether oomd would have acted.
   - Duration: upstream oomd-util.c:111-112 requires `diff >= ctx->mem_pressure_duration_usec`.
   - Reclaim: upstream oomd-manager.c:591-597 skips any cgroup whose last reclaim is older than the window: `if ((now(CLOCK_MONOTONIC) - t->last_had_mem_reclaim) > RECLAIM_DURATION_USEC) continue;`. The window is 30 s (oomd-manager.h:32, `#define RECLAIM_DURATION_USEC (30 * USEC_PER_SEC)`).
   - Candidate choice: oomd-manager.c:614-616 selects by pgscan rate.
   - The entry never mentions reclaim or pgscan (zero hits in memory-pressure-r25.md and .json). MP2 and MP5 cover duration and the swap rule, not reclaim. The S124 registry row (corpus/SOURCES.md:130) covers lines 25-27 only, not line 32.
   - Effect: "quote the `full` share" does not answer the question it is attached to.

5. [obs] Medium. The systemd quote the statement relies on is missing from the lesson Gate, and the checker does not catch the gap.
   - The quote "the fraction of time in a 10 second window in which all tasks in the control group were delayed" appears at memory-pressure-r25.md:86 and memory-pressure-r25.json:92. `grep -n -i "fraction of time"` over corpus/lessons/round-25.md returns nothing. The Gate at lines 5-30 says every quote below was re-checked, so this one was not.
   - The row's machine-readable `sources` list is ["S115"] only (JSON lines 46-48). The checker's source rule therefore never reads the S120 registry row.
   - The checker's quote rule accepts any one Gate quote per row (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-memory-pressure.py:578-586, 603-607), and its pointer rule accepts any one counted pointer. I ran the checker read-only at the measured revision: exit 0, verified_rows 6, findings empty, MP1 `verified: True` with `sources: [S115]`.

6. [obs] Medium. The registry sha for the systemd source S120 is wrong.
   - corpus/SOURCES.md:126 records 36ae3e474a6e5632d4a61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617.
   - The fetched v262 bytes hash to 36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617. Hex characters 17 to 19 differ: the bytes have `a4d`, the registry has `d4a`. A string comparison returned DIFFERENT.
   - The entry's own memory-pressure-r25.md:85 has the correct value. The checker never compares source shas; its only sha checks concern the capture (tools/check-memory-pressure.py:22-23, 61, 472-477, 514-515). The Gate says the sha values sit in the SOURCES anchors (round-25.md:7), so the anchor is wrong.
   - The S115 sha (SOURCES.md:121) and the S124 sha (SOURCES.md:130) match the fetched bytes.

7. [inf] Low. The C2 count of "6 of 6" is an evidence-link count, not a check of the statement or the verdict. The checker's own docstring says so (tools/check-memory-pressure.py:34-36, "a count of evidence links in committed bytes"). This is why findings 1, 2, 5 and 6 pass the count.

8. [inf] Low. The thrashing advice is unsourced and omits the definition it argues against. The action says "Do not read a high lifetime `full`/`some` ratio as thrashing on its own" (memory-pressure-r25.md:62-63). Upstream psi.rst lines 50-51 (https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst) define the term: "a workload that spends extended time in this state is considered to be thrashing." The advice itself is defensible, since a lifetime ratio is not a windowed measure, but the row should cite the definition and use the windowed averages as its reason.

## Checks that hold

- psi.rst at v7.2: sha256 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692, matching corpus/SOURCES.md:121. Lines 45-46 contain "The "some" line indicates the share of time in which at least some tasks are stalled on a given resource." Lines 48-49 contain "The "full" line indicates the share of time in which all non-idle tasks are stalled on a given resource simultaneously." Both match exactly after whitespace normalization across the line break. The two Gate substrings (lesson lines 13-14) occur in these bytes.
- oomd.conf.xml lines 182-183: "the fraction of time in a 10 second window in which all tasks in the control group were delayed" matches exactly after whitespace normalization.
- Capture pointers: capture.txt:14 "some avg10=0.02 avg60=0.02 avg300=0.06 total=41385384" and capture.txt:15 "full avg10=0.02 avg60=0.02 avg300=0.06 total=40856373". Each text occurs once (grep -c gives 1), and neither is a header, command echo or exit line. The capture sha256 e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136 matches.
- Arithmetic: 40856373 / 41385384 = 0.98722, which rounds to 0.987. The averages at lines 14-15 are 0.02, 0.02 and 0.06, so "at or below 0.06 percent" holds.
- Supersedes: oom-event-plane.md:301 matches the JSON earlier_text exactly. The narrowing holds: that row does not say what the lines mean and does not say which line the rule reads.
- Sibling reading: the F2 section of mori system-pressure-r24.md at commit 4f05dd5a starts at line 69 (read with git show, read-only).
- "never by itself an oomd condition" holds at v262. The only memory PSI type read is FULL: a grep for PRESSURE_TYPE_SOME and read_resource_pressure over oomd-util.c and oomd-manager.c finds only oomd-util.c:684. The rules path compares the same full avg10 (oomd-manager.c:805).

## Residual risk and verification gaps

- [unk] The installed Arch package (systemd 262-1-arch) was not inspected. The oomd link rests on upstream v262 source only.
- [inf] psi-util.c's parser body was not read line by line. I read the name table and the call site only.
- The checker was run only at the measured revision 5e7c04ec. The b9046016 run was not repeated.
- No live systemd-oomd query and no host read beyond the frozen capture were made.
- MP2 through MP6 were reviewed only where MP1 depends on them.

## Suggested fixes for the L1 (not applied; this seat is read-only)

- Cite oomd.conf.xml lines 95-96 and register oomd-util.c lines 105 and 680-684 with its sha. Scope the verdict to upstream v262, or use `scoped`.
- Name `full avg10` as the input in the action. Point the "would systemd-oomd have acted" answer at monitored cgroups and at MP4's auto-state result, and add the duration and reclaim gates.
- Put the S120 quote into the Gate, add S120 to the row's `sources`, and correct corpus/SOURCES.md:126 to 36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617.
- Make the checker compare source shas and check every quote, not any one.

Scope: read=lane files memory-pressure-r25.md and .json, lessons/round-25.md, corpus/SOURCES.md, oom-event-plane.md, tools/check-memory-pressure.py and the frozen round-25 capture; upstream Linux v7.2 psi.rst and systemd v262 oomd.conf.xml, oomd-util.c, oomd-manager.c, oomd-manager.h, psi-util.c and systemd-oomd.service.xml by curl; sibling mori lane at 4f05dd5a by git show; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/RevMP1.md, /fast/scratch/hyaku/tsukuroi-r25/w2/RevMP1/ (fetched copies, checker output); executed=curl -fsSL of six upstream files, sha256sum, grep -n/-c/-F/-o, sed -n on git show of mori 4f05dd5a (read-only), python3 tools/check-memory-pressure.py --revision 5e7c04ecb02735491456de2b8bc44550d0db4609 (exit 0, read-only), python3 JSON parse of checker output, tr and grep normalization, sha string comparison
Model: anthropic/claude-haiku-5-5
Installs: none
