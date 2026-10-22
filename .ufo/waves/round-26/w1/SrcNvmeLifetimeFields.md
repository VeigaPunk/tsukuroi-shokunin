# S135 — NVMe SMART / Health Information lifetime fields (source seat report)

Verdict: holds — the NVM Express Base Specification PDF was opened by plain download with no form, login or challenge, and it grounds the declared row SH6; the one wording limit is that the current specification renames "Unsafe Shutdowns" to "Unexpected Power Losses".

## 1. What was opened, and how

1. [obs] The landing page `https://nvmexpress.org/specifications/` was fetched with plain `curl` and returned HTTP 200, 90,651 bytes. The page is JavaScript-rendered and carries no `.pdf` link in its HTML.
2. [obs] Its public JSON endpoint `https://nvmexpress.org/wp-json/vtm/v1/specifications` (referenced by the page's own `specifications.js` bundle as `wp-json/vtm/v1/specifications`) returned HTTP 200, 105,942 bytes, and names the current base specification as "NVM Express Base Specification, Revision 2.4 Ratified 2026.07.31" with `file` `NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf` and `url` `https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf`.
3. [obs] That PDF was downloaded by plain `curl` with no cookie, no login, no challenge and no form: HTTP 200, `content_type` `application/pdf`, 13,821,463 bytes, `file` reports "PDF document, version 1.7, 870 page(s)", sha256 `fe7647532c06859f2952d9db1f90165aa3e9375343d588d5444253f7dbb2c9bd`. The specification was therefore **opened**, not recorded unopened, and the Linux `include/linux/nvme.h` plus nvme-cli `smart-log` fallback was not needed for S135.
4. [obs] The archive page `https://nvmexpress.org/nvm-express-specification-archives/` also exposes 109 direct PDF links, including "NVM-Express-Base-Specification-Revision-2.3-2025.08.01-Ratified.pdf" (Revision 2.3, the previous revision). Revision 2.4 was used because the specifications page lists it as the current base specification.
5. [obs] The committed snapshot is the plain-text rendering of exactly those fetched PDF bytes, produced by `pdftotext` (poppler 26.08.0) with no layout flag: `.ufo/waves/round-26/sources/S135.txt`, 2,795,091 bytes, 70,737 lines, sha256 `c39f3403106ca496dff79a3b2b4860bf1b422a6695e49e7b5d9fef15787fe20e`.
6. [inf] The rendering, not the PDF itself, is the committed snapshot because the round-26 C1 counting rule requires each quote to be a whitespace-normalised substring of the committed snapshot `.ufo/waves/round-26/sources/<S###>.*` and requires a line count. The PDF's page text lives in compressed streams: a byte scan of the fetched PDF finds `Unsafe Shutdowns` 0 times and `Power Cycles (PWRC)` 0 times, so no quote could be a substring of the PDF bytes. The exact fetched PDF bytes are preserved unaltered at `.ufo/waves/round-26/w1/SrcNvmeLifetimeFields/S135.pdf`.
7. [unk] Whether the L1 wants the PDF bytes committed as `sources/S135.pdf` in addition to the rendering is a planner decision. Recommendation: keep one file per source id (the rendering) so that the anchor cell names exactly one digest and the quote-substring rule resolves to one file; copying the PDF into `sources/` would create two candidate snapshots for `S135.*` and put the PDF digest in play for the quote check.

## 2. Proposed SOURCES row (11-column contract shape)

```
| S135 | NVM Express Base Specification Revision 2.4, Ratified 2026-07-31, section 5.2.13.1.3 and Figure 213, SMART / Health Information log page — https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf | docs | A | The primary definition of the NVMe SMART / Health Information log page and its lifetime counters, reached from the specifications landing page by plain download with no form, login or challenge; the current base specification is named by the public endpoint https://nvmexpress.org/wp-json/vtm/v1/specifications | revision 2.4 (Ratified 2026-07-31), NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf, section 5.2.13.1.3 and Figure 213, lines 21282-21283, 21504, 21507, 21527 and 21539-21545 of the committed plain-text rendering .ufo/waves/round-26/sources/S135.txt (pdftotext of the fetched PDF); bytes sha256 c39f3403106ca496dff79a3b2b4860bf1b422a6695e49e7b5d9fef15787fe20e | The SMART / Health Information log page reports over the life of the controller and is retained across power cycles; Power Cycles, Unexpected Power Losses (the field previously named Unsafe Shutdowns), Media and Data Integrity Errors and Number of Error Information Log Entries are lifetime counters, so their values are not dated incidents | mined | 2026-10-22 | on-release | corpus/knowledge/storage-health-r26.md |
```

No `|` character occurs inside any cell. The row carries one digest only, the digest of the committed snapshot that holds the quotes.

## 3. Quotes (four, all at most 25 words, copied byte for byte from the committed snapshot)

Line numbers are lines of `.ufo/waves/round-26/sources/S135.txt` (sha256 `c39f3403…`). Each was verified as a whitespace-normalised substring of that file.

- Q1, lines 21282-21283, 19 words: "The information provided is over the life of the controller and is retained across power cycles unless otherwise specified."
- Q2, line 21504, 9 words: "Power Cycles (PWRC): Contains the number of power cycles."
- Q3, line 21527, 9 words: "Note that this field was previously named Unsafe Shutdowns."
- Q4, lines 21544-21545, 21 words: "Number of Error Information Log Entries (NEILE): Contains the number of Error Information Log Entries over the life of the controller."

Two further lines are cited in section 4 as decisive context (each also at most 25 words): line 21539-21540, 20 words, "Media and Data Integrity Errors (MDIE): Contains the number of occurrences where the controller detected an unrecovered data integrity error."; line 21507, 14 words, "Unexpected Power Losses (UPL): Contains a count of the number of unexpected power losses."

## 4. Does the source support, limit or contradict the declared SH6 wording?

Declared SH6 wording (SCORECARD.md:895): "SH6 the NVMe lifetime counters (unsafe shutdowns, power cycles, media errors, error log entries) are cumulative over the device's life, not dated incidents."

**Supports, decisively.** [obs] The log page is defined to carry lifetime information: "This log page is used to provide SMART and general health information. The information provided is over" / "the life of the controller and is retained across power cycles unless otherwise specified." (S135.txt:21282-21283, Q1). [obs] The error log entry counter states the lifetime semantics in its own definition: "Number of Error Information Log Entries (NEILE): Contains the number of Error Information Log" / "Entries over the life of the controller." (S135.txt:21544-21545, Q4). [obs] "Power Cycles (PWRC): Contains the number of power cycles." (S135.txt:21504, Q2) and "Media and Data Integrity Errors (MDIE): Contains the number of occurrences where the controller detected an unrecovered data integrity error." (S135.txt:21539-21540) are plain counts, with no time window in their definitions. [inf] Taken with the page-level statement, a non-zero value of any of the four counters is a cumulative total since the device's life began, so it cannot be read as a dated incident; that is exactly what SH6 claims.

**Limits, in three ways.** [obs] First, the current specification does not use the name "Unsafe Shutdowns" for the counter: the byte range 159:144 field is "Unexpected Power Losses (UPL): Contains a count of the number of unexpected power losses." (S135.txt:21507) and the specification adds "Note that this field was previously named Unsafe Shutdowns." (S135.txt:21527, Q3). The name in the declared row is the revision 1.4 and earlier name, and it is the name the host's tools print. [inf] The entry should therefore say that the counter read as "unsafe shutdowns" by smartctl is the specification's "Unexpected Power Losses" counter, so the declared wording is accurate about the tool output but not about the current specification's field name.
[obs] Second, the lifetime statement carries the qualifier "unless otherwise specified", and other fields of the same log page do carry such exceptions: the Endurance Group Critical Warning Summary "represent the current associated state and are not persistent." (S135.txt:21409), and the Critical Warning bits "represent the state at the time the Get Log Page command is processed" (S135.txt:21320). [obs] Third, the increment condition of the unexpected-power-loss counter is narrow: the count is incremented "if, and only if, main power is lost when" the controller does not report it ready to be powered off, or when the media was not in the shutdown state after an out-of-band Admin command that accesses media with the Ignore Shutdown bit set (S135.txt:21508-21525). [inf] A count of 200 therefore counts controller-detected unexpected power losses under those conditions, not 200 host-visible unclean shutdowns; the entry must not read it as a date-bearing incident count either way.
[obs] None of the four SH6 counters is among the fields the specification marks as not persistent or as state-at-read-time, so the exception clause does not undercut SH6 itself.

**Contradicts.** [obs] Nothing in the specification contradicts the declared SH6 wording. The only friction is the field-name rename described above, which is a naming limit, not a semantic contradiction.

## 5. Anything in the source that contradicts the frozen capture's host facts

The frozen capture `.ufo/waves/round-26/capture/capture.txt` was re-read and its digest re-verified as `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd`, matching the pinned value in SCORECARD.md:897.

- [obs] capture.txt:194 "Power Cycles:                       325" is consistent with "Power Cycles (PWRC): Contains the number of power cycles." (S135.txt:21504).
- [obs] capture.txt:197 "Media and Data Integrity Errors:    0" is consistent with the MDIE definition (S135.txt:21539-21540).
- [obs] capture.txt:198 "Error Information Log Entries:      0" is consistent with the NEILE definition (S135.txt:21544-21545); smartctl prints the label without the leading "Number of", a label difference only.
- [obs] capture.txt:196 "Unsafe Shutdowns:                   200" is the value of the field the current specification calls "Unexpected Power Losses" (S135.txt:21507, S135.txt:21527). The capture label is the revision 1.4 name; the counter and its semantics are the same field.
- [obs] capture.txt:184 "Critical Warning:                   0x00", capture.txt:186 "Available Spare:                    100%" and capture.txt:187 "Available Spare Threshold:          10%" are consistent with the specification's rules: "Available Spare (AVSP): Contains a normalized percentage (0% to 100%) of the remaining spare capacity available." (S135.txt:21383) and the Critical Warning bit 0 condition that the available spare has fallen below the threshold (S135.txt:21317, S135.txt:21320). With 100% spare against a 10% threshold, no such bit is due to be set, so a zero Critical Warning is consistent.
- [obs] capture.txt:188 "Percentage Used:                    2%" is a vendor estimate: "Percentage Used (PUSED): Contains a vendor specific estimate of the percentage of NVM subsystem life used based on the actual usage and the manufacturer's prediction of NVM life." and "This value shall be updated once per power-on hour" (S135.txt:21388, S135.txt:21392). [inf] A 2% reading is a coarse, hourly-updated estimate and is not a dated incident either; the entry should not treat it as one, and it is also not a measurement that SH6's four counters rest on.
- [obs] No line of the capture contradicts the specification. The only mismatch anywhere is the "Unsafe Shutdowns" versus "Unexpected Power Losses" label, and the capture's own output shows that the label comes from the tool: smartctl 7.5 prints "SMART/Health Information (NVMe Log 0x02, NSID 0xffffffff)" (capture.txt:183) with the specification's field names otherwise unchanged.

## 6. Artifact paths and digests

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S135.txt` — committed snapshot, plain-text rendering of the fetched specification PDF, 2,795,091 bytes, 70,737 lines, sha256 `c39f3403106ca496dff79a3b2b4860bf1b422a6695e49e7b5d9fef15787fe20e`.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/SrcNvmeLifetimeFields/S135.pdf` — the exact fetched PDF bytes, 13,821,463 bytes, 870 pages, sha256 `fe7647532c06859f2952d9db1f90165aa3e9375343d588d5444253f7dbb2c9bd`.
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/SrcNvmeLifetimeFields.md` — this report.

Reproduction commands (read-only, no host mutation):

```
curl -sL -o S135.pdf https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf
sha256sum S135.pdf            # fe7647532c06859f2952d9db1f90165aa3e9375343d588d5444253f7dbb2c9bd
pdftotext S135.pdf S135.txt   # poppler 26.08.0
sha256sum S135.txt            # c39f3403106ca496dff79a3b2b4860bf1b422a6695e49e7b5d9fef15787fe20e
wc -l S135.txt                # 70737
```

## 7. Out of scope for this seat

- [obs] No lane file outside this seat's own paths was written. No git or jj write command was run against the lane repository; no file under `.ufo/state/` or `.ufo/watchdog.log` was touched.
- [obs] No host command that mutates state was run. The capture was read, not re-run; no smartctl, nvme, btrfs or journalctl query was repeated on the host for this seat, and no scrub, balance, counter reset, service action, package transaction or configuration write occurred.
- [obs] The Linux v7.2 `include/linux/nvme.h` `struct nvme_smart_log` and the nvme-cli v3.1 `smart-log` documentation fallback was not fetched, because the primary specification opened; that fallback was assigned as the fallback only.
- [unk] Whether the round-26 entry wants the specification's Endurance Group SMART log page (a separate log page whose MDIE and NEILE fields are per Endurance Group, S135.txt:22856-22859) cited alongside the controller-level log page is a planner decision; the controller-level Figure 213 is the page the host's smartctl and nvme-cli read.

Scope: read=SCORECARD.md (round-26 declaration, C1 rows and counting rules), corpus/SOURCES.md (registry row shape), the frozen capture .ufo/waves/round-26/capture/capture.txt (NVMe health lines 170-215), https://nvmexpress.org/specifications/ and its public JSON endpoint, and the fetched specification PDF; wrote=.ufo/waves/round-26/sources/S135.txt, .ufo/waves/round-26/w1/SrcNvmeLifetimeFields/S135.pdf, .ufo/waves/round-26/w1/SrcNvmeLifetimeFields.md; executed=curl (nvmexpress.org specifications page, wp-json specifications endpoint, specification archives page, two PDF downloads), pdftotext (poppler 26.08.0), sha256sum, wc, python3 byte scan of the PDF, file.

Model: opencode-go/minimax-m3.1-flash-free

Installs: none
