# RevRowSH5: falsification of entry row SH5 (round 26, wave 2)

Verdict: partly holds. Every quoted line, capture line number, host reading and verdict in SH5 checks out against the pinned smartmontools 7.5 source, the frozen capture and the NVMe 2.4 text. The statement and the SKILL.md row overclaim: "otherwise" and "exactly when" leave out the case where smartctl prints no overall-health line at all. The S135 citation supports nothing in SH5, and the action's list of forbidden flags is shorter than the lane's own rule. No SH5 action changes the host.

## Findings

1. The words "FAILED! otherwise" and "exactly when" are not true in every case. [obs, by code reading]
   - Entry statement: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/storage-health-r26.md:71 says smartctl "prints PASSED when the controller's Critical Warning byte is zero and FAILED! otherwise". The same sentence is at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/storage-health-r26.json:229.
   - SKILL row: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md:2367 says "smartctl prints PASSED exactly when the Critical Warning byte is 0."
   - Code, in the snapshot /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S134.cpp. Three cases print no overall-health line:
     a. Neither -H nor -A was requested. Lines 772-778 print "NVMe device successfully opened" and return 0. The call at line 839 is guarded by options.smart_check_status.
     b. The Identify Controller read fails. Lines 786-788 return FAILID first.
     c. The SMART/Health log read fails. Lines 833-836 print "Read NVMe SMART/Health Information ... failed" and return FAILSMART. The print at line 840 never runs.
   - So "otherwise" is false for case c. "Exactly when" is false as a two-way condition: if the log cannot be read, the byte is unknown and PASSED is not printed.
   - Effect on the verdict: none. The capture shows PASSED after a successful read (capture.txt line 181).
   - Suggested wording: "When the SMART/Health log is read and -H is given, smartctl prints PASSED when the Critical Warning byte is 0 and FAILED! otherwise. When the log cannot be read, it prints no overall-health line."
   - Severity: low (wording). It is still a universal claim of the kind the brief asked to be checked.

2. The S135 citation is not used by any SH5 quote. [obs]
   - SH5 lists S134 and S135 as sources (storage-health-r26.md:79; storage-health-r26.json:233-236). Every SH5 quote is from S134 (storage-health-r26.json:237-253).
   - The only text that defines bit 0x01 is S135.txt lines 104-105: "Available Spare Capacity Below Threshold (ASCBT): If this bit is set to '1', then the available spare capacity has fallen below the threshold." SH5 does not quote it.
   - The S135 row, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:141, lists excerpt lines 13-15, 235, 237-258 and 270-276. That leaves out lines 48-50 and 104-105. Its "supports" text covers only the lifetime counters.
   - The excerpt is faithful. The pinned PDF (sha256 fe7647532c06859f2952d9db1f90165aa3e9375343d588d5444253f7dbb2c9bd, the same as the row) and its pdftotext rendering (sha256 c39f3403106ca496dff79a3b2b4860bf1b422a6695e49e7b5d9fef15787fe20e, the same as the row) contain the same sentence at rendering lines 21373-21374.
   - Fix: add an S135 quote for lines 104-105 to SH5, and list those lines in the S135 row.

3. The action's list of forbidden flags does not match the lane's rule, and the command drops -n. [obs]
   - storage-health-r26.md:77 and storage-health-r26.json:232 say "sudo smartctl -H -A <device> (read-only; never -t, -s or -X)".
   - The SKILL.md authority paragraph (SKILL.md:2359) and the lane's privileged-read list also forbid -i. The SKILL.md row (SKILL.md:2367) writes `sudo -n smartctl -H -A`.
   - Host effect: none. On NVMe, -H and -A only read Identify Controller and the SMART log (nvmeprint.cpp lines 786 and 827-840). On ATA, -H does not enable SMART unless -s on is given (ataprint.cpp lines 3930-3937). With SMART off, it refuses and says so (ataprint.cpp lines 3950-3951). So "read-only" holds on both paths.
   - Severity: low.

4. Wording in the triage paragraph. [obs] storage-health-r26.md:99 says "A zero PASSED from smartctl is a statement about one byte." PASSED is a result, not a zero. The sentence is also true only when the log was read (finding 1).

5. The checker does not verify the things SH5 depends on. [obs] This bears on claim C1.
   - The quote check (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-storage-health.py lines 711-714) tests only that the quote text occurs somewhere in the snapshot. The "location" fields, such as "line 451", are never read.
   - The SKILL check (check-storage-health.py lines 741-744) tests only that the ID SH5 appears in the SKILL.md section. The SKILL.md row's verdict and action are never compared with the JSON.
   - So a wrong line number, or a SKILL.md row that disagrees with the JSON, would still count as verified. I checked the line numbers by hand (see A below).

6. Adjacent sentence outside the SH5 row. [obs] SKILL.md:2374 (SE3) says "Media errors are a replacement question for the operator, never something to scrub around." SE3's trigger does not include media errors, and SH5 says media errors never decide PASSED or FAILED. "Replacement question" has no source. This is not a verdict error.

## Checked and holding

A. Quotes and line numbers. The JSON quotes at lines 240, 245 and 250, and storage-health-r26.md lines 79-80, match the snapshot text at S134 lines 451, 459 and 840 exactly. The snapshot's sha256 (4770d9852c2b2b1d66ac2c195952f4f7087db9bc1951e0737c414033df0e4e98) equals the upstream nvmeprint.cpp at commit f276b249fdc84019403491303479485030ac7c80. The GitHub API gives that commit as tag RELEASE_7_5. SOURCES.md:140 records the same sha256. [obs]

B. Capture lines. Lines 181 (PASSED), 184 (Critical Warning 0x00), 186 (Available Spare 100%), 187 (threshold 10%), 188 (Percentage Used 2%) and 197 (Media and Data Integrity Errors 0) match exactly. The frozen capture hashes to 002bef16bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd, as pinned. [obs]

C. Statement claims that hold.
   - "One byte": the health function takes "unsigned char w" (nvmeprint.cpp:448). smartctl.cpp lines 1677-1678 send every NVMe device to nvmePrintMain. Across the whole 7.5 tree, the NVMe overall-health line is printed only at nvmeprint.cpp lines 450-451. ATA prints its own lines (ataprint.cpp lines 4060-4135). smartd.cpp line 4180 masks the same byte for its own alerts. That is a different program, and it prints no PASSED line. [obs]
   - "Lists the set warning bits": lines 457-459 name each set bit. Lines 476-477 print an "unknown critical warning(s)" line for bits outside 0x3f. [obs]
   - "Not inputs": the health function takes only w (line 448), and the call at line 840 passes only critical_warning. Available Spare, Percentage Used and Media and Data Integrity Errors are printed at lines 501, 509 and 530. [obs]
   - "Bit 0x01 ... its threshold": lines 458-459 and the spec text in finding 2. [obs]

D. Verdict. HEALTHY follows. PASSED with a zero byte, spare 100% against a 10% threshold, Percentage Used 2% and zero media errors are all no-fault readings under the vocabulary at storage-health-r26.json lines 19-24. The verdict covers the overall-health line. The action correctly says PASSED does not judge wear or media errors. [inf]

E. SKILL.md row against the entry. The host reading, verdict and action text in SKILL.md:2367 match the entry. The only differences are "exactly when" (finding 1) and "-n" (finding 3). [obs]

F. Installed binary. /usr/bin/smartctl (smartmontools 7.5-2 per pacman -Q) contains the same message strings as the snapshot. These include "- available spare has fallen below threshold", "- unknown critical warning(s)" and "r5714". This is string evidence only. [inf]

G. Capture layout. The capture order (START OF SMART DATA SECTION, the PASSED line, a blank line, the SMART/Health header, the Critical Warning line) matches nvmePrintMain (nvmeprint.cpp lines 821-823, 839-840, 481 and 491). [obs]

H. Spec text. The pinned NVMe 2.4 text matches S135.txt lines 48-50 (rendering lines 21317-21320) and lines 104-105 (rendering lines 21373-21374). [obs]

## Residual risk and verification gaps

- I compared strings in the installed binary, not its compiled logic. [unk]
- The spec's Figure 213 byte column does not come through text extraction, so the rendering shows no byte offset for Critical Warning. "One byte" rests on the smartctl parameter type. [unk]
- The read-failure branch was not exercised on the host. Finding 1 rests on code reading. [inf]
- I did not check the Arch packaging of smartmontools 7.5-2 for patches. [unk]
- I did not run any host command. The frozen capture is the only host evidence used. [obs]

Scope: read=storage-health-r26.md and .json (SH5 and triage lines); SKILL.md lines 2357-2376 and 2415; capture.txt lines 180-198 and header; S134.cpp and S135.txt snapshots; SOURCES.md lines 140-141; tools/check-storage-health.py lines 367-423, 550, 614-625, 663-793 and its location and grep checks; the extracted smartmontools RELEASE_7_5 tree under /fast/scratch/hyaku/tsuku26/w2/RevRowSH5/tree; the NVMe 2.4 PDF and its text under /fast/scratch/hyaku/tsuku26/w2/RevRowSH5/; /usr/bin/smartctl bytes; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevRowSH5.md and /fast/scratch/hyaku/tsuku26/w2/RevRowSH5/ (nvmeprint.cpp, smartmontools-f276b249.tar.gz, tree/, nvme-2.4.pdf, nvme-2.4.txt); executed=curl (raw nvmeprint.cpp at f276b249, release archive for f276b249, GitHub API tag lookup, NVMe PDF HEAD and download), sha256sum, tar -xzf, pdftotext (no flags), ls, wc, pacman -Q smartmontools nvme-cli, and a Python read-only byte scan of /usr/bin/smartctl; no smartctl, nvme, checker or lane write command was run.
Model: anthropic/claude-haiku-5-5 (exposed by the session project context; not independently confirmed)
Installs: none
