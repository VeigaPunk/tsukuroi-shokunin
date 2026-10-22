# S134 — smartmontools 7.5 `nvmeprint.cpp` (NVMe SMART/Health printing and overall-health derivation)

Verdict: done — the release-tag source was opened by plain curl, saved byte-for-byte as `S134.cpp` with a recorded sha256, and it *limits* the declared SH5 wording (only the Critical Warning byte decides the PASSED/FAILED verdict) while *supporting* SH6's field set as printed lifetime counters, with no contradiction against the frozen capture.

## 1. Snapshot provenance

- Release tag: `RELEASE_7_5` exists in `https://github.com/smartmontools/smartmontools`. [obs] `git ls-remote --tags https://github.com/smartmontools/smartmontools.git RELEASE_7_5` exited 0 and printed `f276b249fdc84019403491303479485030ac7c80	refs/tags/RELEASE_7_5`.
- The file **has moved**: at tag `RELEASE_7_5` the path `nvmeprint.cpp` at the repository root returns HTTP 404, and the file lives at `smartmontools/nvmeprint.cpp` (HTTP 200). [obs] The same root-path 404 / `smartmontools/`-subdirectory 200 split also holds at `RELEASE_7_3` and `RELEASE_7_4`; the tags `7.5` and `v7.5` do not exist (both 404).
- Fetched URL (raw, pinned to the tag): `https://raw.githubusercontent.com/smartmontools/smartmontools/RELEASE_7_5/smartmontools/nvmeprint.cpp` — HTTP 200, 38005 bytes.
- Canonical (browsable) URL for the same bytes: `https://github.com/smartmontools/smartmontools/blob/RELEASE_7_5/smartmontools/nvmeprint.cpp`.
- Saved snapshot: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S134.cpp`
  - sha256 `4770d9852c2b2b1d66ac2c195952f4f7087db9bc1951e0737c414033df0e4e98`
  - 959 lines (959 newline-terminated lines, file ends with `\n`; `awk END{print NR}` = 959, `wc -l` = 959)
  - 38005 bytes
- Independent cross-check: the tarball of the same tag (`https://codeload.github.com/smartmontools/smartmontools/tar.gz/refs/tags/RELEASE_7_5`) contains `smartmontools-RELEASE_7_5/smartmontools/nvmeprint.cpp` with the **same** sha256 `4770d9852c2b2b1d66ac2c195952f4f7087db9bc1951e0737c414033df0e4e98`. [obs] The temporary tarball and its extraction directory were deleted after the comparison; nothing outside my seat paths was written.
- Host match: `pacman -Q smartmontools` = `smartmontools 7.5-2`; `smartctl --version` = `smartctl 7.5 2025-04-30 r5714 [x86_64-linux-7.2.11-arch1-1] (local build)`. The tag matches the installed release line (7.5). [obs]

## 2. Proposed SOURCES row (11-column contract shape)

| S134 | smartmontools 7.5 `nvmeprint.cpp` — https://github.com/smartmontools/smartmontools/blob/RELEASE_7_5/smartmontools/nvmeprint.cpp | code | A | How smartmontools 7.5 prints the NVMe SMART/Health Information log (Log 0x02) and how the overall-health PASSED or FAILED verdict is derived from the Critical Warning byte | tag RELEASE_7_5 commit f276b249fdc84019403491303479485030ac7c80, path smartmontools/nvmeprint.cpp, lines 448-482 (health verdict and critical-warning bits), lines 484-533 (printed health fields), lines 838-843 (verdict call site), sha256 4770d9852c2b2b1d66ac2c195952f4f7087db9bc1951e0737c414033df0e4e98 | The NVMe overall-health verdict is derived from one byte only, the SMART log Critical Warning: zero prints PASSED and any set bit prints FAILED, and available spare below threshold is reported as critical-warning bit 0x01; Percentage Used, Media and Data Integrity Errors, Unsafe Shutdowns, Power Cycles and Error Information Log Entries are printed counters that do not enter the verdict | mined | 2026-10-22 | on-release | corpus/knowledge/storage-health-r26.md |

No `|` character appears inside any cell of that row.

## 3. Exact quotes from the saved snapshot

Each quote is copied byte-for-byte from `.ufo/waves/round-26/sources/S134.cpp`, with the line numbers of the snapshot. Whitespace-normalised, each is a substring of the saved file.

Quote 1 (grounds SH5, the verdict derivation) — lines 450 and 451:

```
  jout("SMART overall-health self-assessment test result: %s\n",
       (!w ? "PASSED" : "FAILED!"));
```

Quote 2 (grounds SH5, the spare threshold) — line 503:

```
  jout("Available Spare Threshold:          %u%%\n", smart_log.spare_thresh);
```

Quote 3 (grounds SH6, unsafe shutdowns) — line 528:

```
  jout("Unsafe Shutdowns:                   %s\n", le128_to_str(buf, smart_log.unsafe_shutdowns));
```

Quote 4 (grounds SH6, media and data integrity errors) — line 530:

```
  jout("Media and Data Integrity Errors:    %s\n", le128_to_str(buf, smart_log.media_errors));
```

Supporting lines cited without quoting (same file, same byte content): 491 `jout("Critical Warning:                   0x%02x\n", smart_log.critical_warning);`, 501 `jout("Available Spare:                    %u%%\n", smart_log.avail_spare);`, 509 `jout("Percentage Used:                    %u%%\n", smart_log.percent_used);`, 522 `jout("Power Cycles:                       %s\n", le128_to_str(buf, smart_log.power_cycles));`, 532 `jout("Error Information Log Entries:      %s\n", le128_to_str(buf, smart_log.num_err_log_entries));`, 459 `jout("- available spare has fallen below threshold\n");`, 840 `print_critical_warning(smart_log.critical_warning);`, 842 `retval |= FAILSTATUS;`.

## 4. Does the source support, limit or contradict the declared row wording?

### SH5 — "how `smartctl` derives the NVMe overall-health result and which fields (critical warning, available spare against its threshold, percentage used, media and data integrity errors) decide it"

**Limits the wording; one clause of it is contradicted.** [obs] The verdict is computed in `print_critical_warning(unsigned char w)` (lines 448-482) from a single argument, the Critical Warning byte: `(!w ? "PASSED" : "FAILED!")` (line 451). The call site confirms the only input — line 840 `print_critical_warning(smart_log.critical_warning);`, where `smart_log` is the NVMe SMART/Health log read by `nvme_read_smart_log` (lines 831-834) — and a non-zero byte also sets the exit status at line 842 `retval |= FAILSTATUS;`.

Consequences for the declared wording:

- **Critical warning** decides the result — **supported**. It is the sole input to the verdict.
- **Available spare against its threshold** decides it — **supported, but only indirectly**. The source never compares `avail_spare` with `spare_thresh`; it prints both separately (lines 501 and 503) and reports the condition through critical-warning bit 0x01, line 459 `jout("- available spare has fallen below threshold\n");` guarded by `if (w & 0x01)` (line 458). So the spare-threshold breach reaches the verdict only because the controller raised bit 0x01; smartmontools itself does not derive it.
- **Percentage used** decides it — **contradicted**. `percent_used` is printed (line 509) and mapped into the JSON as `endurance_used` (line 511), but it is never an input to `print_critical_warning` and never affects `retval`. It is an endurance indicator, not a health gate in this code.
- **Media and data integrity errors** decide it — **contradicted**. `media_errors` is printed (line 530) and stored in JSON (line 531); it never enters the verdict and never sets `FAILSTATUS`. Media read-only is reported only via critical-warning bit 0x08 (lines 467-469), again through the byte.

Decisive pair: line 451 (the whole verdict is one byte) against lines 509 and 530 (the two fields declared as deciding, both print-only). A corpus entry that claims "percentage used and media errors decide the overall-health result" would be falsified by this snapshot; the honest phrasing is "only the Critical Warning byte decides; percentage used and media/data integrity errors are printed indicators that smartctl does not use for the verdict".

### SH6 — "the NVMe lifetime counters (unsafe shutdowns, power cycles, media errors, error log entries) are cumulative over the device's life, not dated incidents"

**Supported in substance, but the source does not state the word "lifetime".** [obs] The four counters are read from the SMART/Health Information log and printed as unbounded 128-bit values: `le128_to_str(buf, smart_log.unsafe_shutdowns)` (line 528), `le128_to_str(buf, smart_log.power_cycles)` (line 522), `le128_to_str(buf, smart_log.media_errors)` (line 530) and `le128_to_str(buf, smart_log.num_err_log_entries)` (line 532). The struct fields are 128-bit counters with no time window in this file, and each is rendered as a plain count, never as a rate or an incident with a date. [inf] Because the counter values are cumulative totals read from the device's health log, a non-zero value denotes the device's lifetime total, not a dated incident; that inference is exactly the claim SH6 wants, but it rests on the NVMe log semantics (the primary definition of these fields, source S135) rather than on this file, which only prints them.

One limit worth stating: this file *also* reads the Error Information Log (lines 860-878), and each stored entry there is a dated event; only the **counter** `num_err_log_entries` (line 532) is a lifetime total. The declared SH6 wording covers "error log entries" as a counter, which is consistent, but an entry reader must not conflate the counter with the dated entries it counts.

### Overall

The snapshot **supports** the SH5 claim that `smartctl` derives the NVMe overall-health result and that critical warning and the spare threshold participate in it; it **limits** SH5 by showing percentage used and media/data integrity errors are printed but never decide; it **supports** the SH6 field list as cumulative counters. It **contradicts nothing** in the SCORECARD declaration outright, but a literal reading of the SH5 list would misstate what decides the verdict.

## 5. Comparison with the frozen capture's host facts

The capture is `.ufo/waves/round-26/capture/capture.txt` (sha256 `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd`); the relevant block is lines 175-204, headed by the command `sudo -n smartctl -H -A /dev/nvme0n1`.

- [obs] The capture line 181 `SMART overall-health self-assessment test result: PASSED` is produced by exactly the source line 450-451 of the snapshot; the string and the PASSED/FAILED! choice match byte-for-byte.
- [obs] Every printed label in the capture matches the source's own label strings: `Critical Warning:` (source line 491), `Available Spare:` (501), `Available Spare Threshold:` (503), `Percentage Used:` (509), `Power Cycles:` (522), `Unsafe Shutdowns:` (528), `Media and Data Integrity Errors:` (530), `Error Information Log Entries:` (532).
- [obs] The capture's `Available Spare: 100%` with `Available Spare Threshold: 10%` is consistent with the source's two separate fields (`avail_spare`, `spare_thresh`); because the capture's Critical Warning is `0x00` (line 184), the source would print no critical-warning sub-lines at all, exactly as the capture shows — no `- available spare has fallen below threshold` line appears.
- [obs] The capture's `Power Cycles: 325`, `Unsafe Shutdowns: 200`, `Media and Data Integrity Errors: 0` and `Error Information Log Entries: 0` are the values the source would render from the same four struct members.
- **No contradiction found.** [obs] Nothing in the snapshot conflicts with any host fact in the capture; the snapshot is device-agnostic printing and verdict code and asserts nothing about this host's values.
- One nuance, not a contradiction: the capture runs `smartctl -H -A` in a single invocation, so the verdict block and the attribute block come from one process; in the source the verdict is printed under `options.smart_check_status` (line 839) and the attribute block under `options.smart_vendor_attrib` (line 844), both from the same `smart_log` structure. Consistent.

## 6. Limits and unknowns

- [unk] Whether the installed Arch build `smartmontools 7.5-2` carries any distribution patch to `nvmeprint.cpp` is not established by this snapshot; the Arch package version matches the upstream 7.5 release line, and the reported `smartctl 7.5 2025-04-30 r5714` build string matches upstream 7.5, but the package's own patch list was not read (out of this seat's read scope).
- [unk] The definition of the `nvme_smart_log` struct members (`critical_warning`, `avail_spare`, `spare_thresh`, `percent_used`, `media_errors`, `unsafe_shutdowns`, `power_cycles`, `num_err_log_entries`) lives in `smartmontools/nvmecmds.h` at the same tag and belongs to source S135; this file only consumes them.
- [obs] The GitHub REST API was unreachable for tag listing (HTTP 403, unauthenticated rate limit); the tag was instead verified with `git ls-remote` (read-only, no repository written) and the file bytes with `raw.githubusercontent.com` plus a `codeload.github.com` tarball cross-check.
- [unk] No claim is made here about whether smartmontools' overall-health verdict is the only health signal `smartctl` prints for NVMe; other parts of smartctl (for example the JSON output, or `smartctl -x`) are outside this file.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md (round-26 declaration lines 874-908), /home/vgpnk/.omp/agent/RULES.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md (registry shape), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/capture/capture.txt (lines 175-207); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/sources/S134.cpp, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/SrcSmartNvmeprint.md; executed=curl raw.githubusercontent.com RELEASE_7_5 smartmontools/nvmeprint.cpp (HTTP 200), git ls-remote --tags https://github.com/smartmontools/smartmontools.git RELEASE_7_5 (exit 0), curl codeload tarball of the tag for the sha256 cross-check, sha256sum, wc -l, awk line extraction of the quoted lines, pacman -Q smartmontools, smartctl --version, no host-changing command.

Model: minimax-m3.1-flash-free (opencode-go/minimax-m3.1-flash-free)

Installs: none
