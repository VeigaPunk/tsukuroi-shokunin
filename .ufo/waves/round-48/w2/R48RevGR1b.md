ROW GR1 VERDICT: holds
SECTION SHA256: fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8
Reviewer R48RevGR1b, row GR1 of corpus/knowledge/btrfs-scrub-grounding-r45.md at ae99f021b76f8eb1c8805d32d80644464afb1ff6.

Hash: the checker's --section-hash printed the expected fe77ac76... value for GR1. I re-derived it in Python as sha256 over the LF-joined lines from "## GR1" up to (not including) "## GR2", with no trailing newline, and got the same value.

Snapshot digests: sha256sum matches SHA256SUMS for cmdline.c (1af5ad98...), vsprintf.c (cabb648a...), kstrtox.c (0c52ae02...) in round 45, and for sysfs.c (ce146120...) in round 44.

Quotes: all 12 Quote lines sit on the cited line, checked with grep -n. These are cmdline.c:147, 156, 159, 189, 191, 192; vsprintf.c:86; kstrtox.c:29, 30, 33; sysfs.c:2040, 2043.

Statement, clause by clause:
1. Write goes to memparse, then simple_strtoull with base 0. sysfs.c:2040 calls memparse(buf, &endptr). cmdline.c:156 calls simple_strtoull(ptr, &endptr, 0). vsprintf.c:112-114 shows simple_strtoull calling simple_strntoull, and vsprintf.c:86 shows that function calling _parse_integer_fixup_radix. Supported.
2. Base 0 resolves to hex for "0x" plus a hex digit, octal for any other leading 0, decimal otherwise. kstrtox.c:29-35 show exactly these three branches (s[0]=='0'; _tolower(s[1])=='x' && isxdigit(s[2]) gives 16; else 8; else 10). Supported.
3. At most one suffix letter, K M G T P E in either case, each step a further 10-bit shift, so K is 1024. cmdline.c:140-186 is a switch with upper and lower case labels, and each case adds shl += 10 and falls through. Only *endptr is tested, so there is one letter. Supported.
4. The suffix counts only when a digit came first. cmdline.c:189 requires ptr != endptr. Supported.
5. A shifted overflow becomes ULLONG_MAX. cmdline.c:191-192. Supported.
6. The store skips whitespace and returns -EINVAL unless the text ends there. sysfs.c:2042 calls skip_spaces and sysfs.c:2043-2044 returns -EINVAL when *endptr != 0. Supported.
7. Examples, traced by hand.
   - 100M and 100m: 100 << 20 = 104857600. Supported.
   - 010: octal, so 8. Supported.
   - 0x10: hex, so 16. Supported.
   - 10MB: M is consumed, 'B' is left, so EINVAL. Supported.
   - "10 M": no suffix after the digits, because the blank ends the parse. skip_spaces then lands on 'M', so EINVAL. Supported.
   - -1: simple_strtoull has no sign handling. The sign handling is in the signed variant at vsprintf.c:159. So no digits are parsed, endptr stays at '-', and the result is EINVAL. Supported.
   - A bare newline: ptr == endptr gives 0 with no suffix. skip_spaces skips the newline and the text ends, so the write is accepted with limit 0. Supported.
8. "0 means no limit, SR8". This is not decided by the quoted lines but by the row's own cross-reference to SR8, in corpus/knowledge/btrfs-scrub-record-r44.md (lines 64-65). I also checked the pinned code: scrub.c:1380-1382 reads bwlimit = READ_ONCE(device->scrub_speed_max) and returns at once when it is 0. This is correctly given as a reference and carries no inference mark.

Host reading:
- capture.txt:8 reads "scrub_speed_max ... devinfo/1/scrub_speed_max mode=644 owner=root value=0". The row's value 0, mode 644, owner root and devid 1 match it. capture.txt:9 gives devids=1, so "one btrfs device" is right.
- capture.txt:1 reads "uid=1000 CapEff=0000000000000000". That matches "uid 1000 with no effective capabilities".
- "This caller cannot write one" follows from mode 644 and owner root with uid 1000 and CapEff 0. It uses ordinary file-permission semantics, which are not pinned in the bytes. That is standard and is a conclusion of the row, not an overreach.
- "Nothing was written to test the parse" is an honest limitation statement.

Marks: the row carries no [inference] marks. Every Statement clause is decided by the pinned bytes. The one unpinned assumption is that the sysfs store buffer is NUL-terminated, which sysfs.c:2043 itself relies on. This is a residual note only and not an overreach.

No clause overreaches and none is contradicted, so the verdict is holds. I did not run any code: I wrote nothing to sysfs and did not execute memparse. The examples are hand traces of the pinned source.
