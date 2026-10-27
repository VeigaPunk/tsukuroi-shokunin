ROW GR1 VERDICT: holds
SECTION SHA256: fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8

Seat R47ResCritGR1 — counted verdict for row GR1 of corpus/knowledge/btrfs-scrub-grounding-r45.md at 77e9e2b2e96b85d8f048ae2087e246a542b71611 (judged on current bytes).

Section hash: `python3 tools/check-scrub-admission-r47.py --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash` printed GR1 fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8 (matches expected). Re-derived independently: sha256 of the LF-joined 41 lines from `## GR1` to (exclusive) `## GR2` gives the same value. No `## ` line other than the header occurs inside the row.

Snapshot digests verified by sha256sum -c against the pinned SHA256SUMS: cmdline.c, vsprintf.c, kstrtox.c (round-45/frozen/src) and sysfs.c (round-44/frozen/src) all OK. capture.txt sha256 f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70 matches the entry header.

Clause-by-clause attack on Statement:

- "a write to devinfo/<devid>/scrub_speed_max is parsed by memparse": sysfs.c:2040 `limit = memparse(buf, &endptr);` sits inside btrfs_devinfo_scrub_speed_max_store (sysfs.c:~2031-2047), bound by BTRFS_ATTR_RW at sysfs.c:2048-2049; the sysfs path is corroborated by capture.txt:8 (`.../devinfo/1/scrub_speed_max mode=644 owner=root value=0`). Supports.
- "calls simple_strtoull with base 0": cmdline.c:156 quoted exactly; memparse body confirmed at cmdline.c:151-199. Supports.
- "base 0 resolved through _parse_integer_fixup_radix; hex for leading 0x+hexdigit, octal for other leading 0, decimal otherwise": vsprintf.c:86 calls the fixup inside simple_strntoull; kstrtox.c:29-35 (`s[0]=='0'` → `s[1]=='x' && isxdigit(s[2])` → base 16, else `*base = 8`; else base 10 — read at kstrtox.c:41-80 context lines 20-45). Quotes on their cited lines. Supports.
- "at most one suffix letter K/M/G/T/P/E either case; +10-bit shift per step; K=1024": switch at cmdline.c:160-186 with fallthrough E/e→P/p→T/t→G/g→M/m→K/k, shl += 10 each, applied as ret << shl via check_shl_overflow; doc at cmdline.c:147 quoted exactly. Supports.
- "suffix counts only when at least one digit came before it": cmdline.c:189 `if (shl && likely(ptr != endptr))` — a bare letter leaves endptr==ptr so no shift and no endptr++; e.g. "K" reaches sysfs.c:2043 with *endptr=='K' → EINVAL. Supports.
- "overflow of the shifted value becomes ULLONG_MAX": cmdline.c:191-192 quoted exactly. Supports.
- "sysfs store skips whitespace, returns -EINVAL unless text ends": sysfs.c:2042 `endptr = skip_spaces(endptr);` plus sysfs.c:2043-2044 (`if (*endptr != 0) return -EINVAL;`). Supports.
- "100M and 100m both set 104857600": 100 << 20 = 104857600; 'M' and 'm' are separate identical cases (cmdline.c:181-184). Supports.
- "010 sets 8, 0x10 sets 16": kstrtox.c:29-33 radix fixup. Supports.
- "10MB rejected": 'M' consumed, endptr++ leaves 'B' → *endptr != 0. Supports.
- "10 M rejected": space at endptr matches no suffix case; skip_spaces then lands on 'M' → EINVAL. Supports.
- "-1 rejected with EINVAL": strongest counterexample checked — this snapshot's simple_strntoull/simple_strtoull (vsprintf.c:79-99, ~290) contain NO '-' handling; '-' handling lives only in signed simple_strtol/simple_strntoll (vsprintf.c:142, 158) and kstrtox.c:168 (kstrtoll). _parse_integer_limit (kstrtox.c:~57-80) accepts only 0-9/a-f → '-' is never consumed → endptr at '-' → EINVAL. Claim is true for this code (would be false if memparse used simple_strtoll — it does not, cmdline.c:156). Supports.
- "bare newline parses as 0 and is accepted, removing the limit": no digits → ret 0, endptr at '\n'; '\n' is not a suffix case; skip_spaces ('\n' is isspace) reaches NUL → accepted, limit 0. The "0 means no limit (SR8)" tag is satisfied by S242/S243 scrub.c:1380-1382 (`bwlimit = READ_ONCE(...); if (bwlimit == 0) return;`) — the throttler exits early on 0. Supports.
- "In Linux v7.2.11": consistent with header `verified-at` (tag v7.2.11, peeled a2de78ee…, host kernel 7.2.11-arch1-1).

Host reading clause:
- capture.txt:8 `scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max mode=644 owner=root value=0`; capture.txt:1 `uid=1000 CapEff=0000000000000000`; capture.txt:9 shows devids=1 (the "one btrfs device"). mode 644 root-owned ⇒ uid 1000 cannot write. "Nothing was written to test the parse" is a correct honest limit. Supports.

No clause overreaches the quoted lines; all quotes sit on their cited lines; there is no mislabeled inference (the row has no [inference] marks; the only forward reference — "0 means no limit, SR8" — is satisfied by the pinned scrub.c lines above). Verdict: holds.
