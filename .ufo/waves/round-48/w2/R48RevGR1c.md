ROW GR1 VERDICT: holds
SECTION SHA256: fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8
Reviewer R48RevGR1c, counted seat for claim C2, row GR1 (scrub_speed_max parse), judged as a stranger at ae99f021b76f8eb1c8805d32d80644464afb1ff6.

Hash: the checker's --section-hash printed fe77ac76...f9ca8 for GR1, and my own sha256 over the LF-joined lines from `## GR1` up to (exclusive) `## GR2`, with the trailing blank line kept, gave the same value.
Snapshots: sha256sum of cmdline.c (1af5ad98...), vsprintf.c (cabb648a...), kstrtox.c (0c52ae02...) matches round-45 SHA256SUMS; sysfs.c (ce146120...) and scrub.c (f347931b...) match round-44 SHA256SUMS. capture.txt is the host capture, digest in the entry header.
Quotes: all 13 quotes sit on their cited lines, checked by numbering the files: cmdline.c:147,156,159,189,191,192; vsprintf.c:86; kstrtox.c:29,30,33; sysfs.c:2040,2043.

Clause by clause:
1. memparse parses the sysfs write: sysfs.c:2040 `limit = memparse(buf, &endptr);` in btrfs_devinfo_scrub_speed_max_store. OK.
2. memparse calls simple_strtoull with base 0: cmdline.c:156. OK.
3. simple_strtoull reaches _parse_integer_fixup_radix: vsprintf.c:114 calls simple_strntoull, which calls the fixup at vsprintf.c:86 (that call is quoted; the one at 114 is visible just below it, unquoted). OK.
4. Radix choice: kstrtox.c:28-35. Base 16 for '0' then x/X then isxdigit (lines 29-31); else base 8 (line 33); non-zero first char gives base 10 (line 35). A lone leading 0 is base 8, so "any other leading 0" is right. OK.
5. Suffixes: cmdline.c:160-188 is a switch over E/e, P/p, T/t, G/g, M/m, K/k, each case adding shl += 10 and falling through. K is one step, so 1024; M is 2^20; "at most one letter" because the switch reads only *endptr once. OK.
6. Suffix counts only after a digit: cmdline.c:189 `shl && likely(ptr != endptr)`. ptr != endptr means at least one digit was consumed: _parse_integer_limit (kstrtox.c:65-78) breaks on a non-digit, and the fixup only skips 0x when a hex digit follows (kstrtox.c:30). OK.
7. Overflow gives ULLONG_MAX: cmdline.c:191-192. OK.
8. Store skips whitespace and returns -EINVAL unless the text ends: sysfs.c:2041-2044 (skip_spaces, then `*endptr != 0` returns -EINVAL), else the store writes the value and returns len (sysfs.c:2045-2046). OK.
9. Examples, each re-derived by hand: 100M is 100*2^20 = 104857600, and 100m takes the same case. "010" is base 8, so 8. "0x10" is base 16, so 16. "10MB": endptr moves past M (cmdline.c:193 area, endptr++), then 'B' is not NUL, so EINVAL. "10 M": endptr stops at the blank, shl is 0, skip_spaces reaches 'M', so EINVAL. "-1": _parse_integer_limit breaks at '-' (kstrtox.c:70-75), endptr equals ptr, '-' is not whitespace, so EINVAL. Bare newline: no digits, value 0, skip_spaces moves over the newline (sysfs.c:2041 comment says a trailing newline is expected), the text ends, and the store returns len. All follow.
10. 0 means no limit: scrub.c:1380-1382 (`bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit == 0) return;`) in the round-44 scrub.c snapshot; this is the SR8 cross-reference and is supported.

Host reading: capture.txt:8 reads `scrub_speed_max ... devinfo/1/scrub_speed_max mode=644 owner=root value=0`; capture.txt:9 shows devids=1 (one device, devid 1); capture.txt:1 shows uid=1000 CapEff=0000000000000000. Together these show no limit set and, by ordinary file permissions on a root-owned 644 file with no capabilities, no write for this caller. The row says "Nothing was written", consistent with the capture being read-only.

Residual, none rising to partly:
- The body of skip_spaces (isspace including newline) and the kernel's NUL termination of the sysfs buffer are not in any pinned snapshot. The newline example rests on the sysfs.c:2041 comment plus the standard kernel contract. The row has no [inference] mark there, and a strict reader could ask for one. The claim is true and the comment backs it, so I do not downgrade.
- "Cannot write" for uid 1000 is a permission-semantics step from capture.txt:8 and capture.txt:1, not a pinned source line. It is also unmarked and uncontroversial.
- I ran nothing against a kernel: no write, no memparse execution. The checks are by reading pinned bytes.
No inference marks appear in the row, and none seemed required for the pinned-code clauses; no clause overreaches those lines.
