ROW GR1 VERDICT: holds
SECTION SHA256: fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8

Evidence, one bullet per clause of the Statement and Host reading of row GR1 at revision
77e9e2b2e96b85d8f048ae2087e246a542b71611 (row bytes = `## GR1` up to exclusive `## GR2`).

Hash and digests
- Section hash: frozen counter `python3 tools/check-scrub-admission-r47.py --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash` prints GR1 = fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8 (matches the value expected by this item). Independently re-derived: sha256 over the LF-joined bytes of the row from `## GR1` to exclusive `## GR2` (2242 bytes) = fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8. Match.
- Snapshot digests: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-45/frozen/src/` reports cmdline.c OK, vsprintf.c OK, kstrtox.c OK (plus dev-replace.c, systemd.kill.xml); in `.ufo/waves/round-44/frozen/src/` reports sysfs.c OK (plus scrub.c, service, timer, PKGBUILD). `sha256sum .ufo/waves/round-45/frozen/hostcap/capture.txt` = f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70, equal to the digest named in the entry header. Receipt: `.ufo/waves/round-47/w1/R47RevGR1a/verification-transcript.txt`.

Statement clauses
- "a write to devinfo/<devid>/scrub_speed_max is parsed by memparse" — sysfs.c:2040 `limit = memparse(buf, &endptr);` inside `btrfs_devinfo_scrub_speed_max_store`. Supported.
- "calls simple_strtoull with base 0" — cmdline.c:156 `unsigned long long ret = simple_strtoull(ptr, &endptr, 0);`. Supported.
- "resolves base 0 through _parse_integer_fixup_radix" — vsprintf.c:86 `cp = _parse_integer_fixup_radix(startp, &base);` (simple_strntoull, which simple_strtoull wraps). Supported.
- "hexadecimal for a leading 0x followed by a hex digit, octal for any other leading 0, decimal otherwise" — kstrtox.c:29 `if (s[0] == '0') {`, kstrtox.c:30 `if (_tolower(s[1]) == 'x' && isxdigit(s[2]))` then `*base = 16` (kstrtox.c:31-32), kstrtox.c:33 `*base = 8;` in the else branch, and `*base = 10;` (kstrtox.c:35) when s[0] != '0'. Supported.
- "takes at most one suffix letter, K, M, G, T, P or E in either case" — cmdline.c:160-187: a single `switch (*endptr)` with cases E/e, P/p, T/t, G/g, M/m, K/k and fallthrough accumulation; the suffix is consumed exactly once via the single `endptr++` at cmdline.c:194 inside the `if (shl && ...)` block. Supported.
- "each step multiplying by a further 1024 (a 10-bit shift per step, so K is 1024, not 1000)" — cmdline.c:161-186 each fallthrough step does `shl += 10;` and cmdline.c:191 applies `check_shl_overflow(ret, shl, &ret)`, i. a left shift of the accumulated bit count; entry at case 'M' accumulates two steps (shl=20). Supported.
- "the suffix counts only when at least one digit came before it" — cmdline.c:189 `if (shl && likely(ptr != endptr)) {`: ptr != endptr is exactly "at least one digit was parsed"; otherwise the suffix is not consumed and the switch's default path adds nothing. Supported.
- "a shifted value that overflows becomes ULLONG_MAX" — cmdline.c:191-192 `if (unlikely(check_shl_overflow(ret, shl, &ret)))` / `ret = ULLONG_MAX;`. Supported.
- "The sysfs store then skips whitespace and returns -EINVAL unless the text ends there" — sysfs.c:2042 `endptr = skip_spaces(endptr);`, sysfs.c:2043 `if (*endptr != 0)` with `return -EINVAL;` at sysfs.c:2044. Supported.

Worked examples (each re-derived from the quoted code)
- `100M` and `100m` both set 104857600: digits 100 (base 10), suffix M/m enters the switch at case M, two `shl += 10` steps (cmdline.c:171-184) give shl=20, `100 << 20` = 104857600; endptr++ consumed the one letter. Supported.
- `010` sets 8: kstrtox.c:29-33 route a leading 0 not followed by x+hexdigit to base 8; `010` octal = 8. Supported.
- `0x10` sets 16: kstrtox.c:30 hex branch; `0x10` hex = 16. Supported.
- `10MB` rejected EINVAL: memparse consumes the single suffix letter M (endptr++ at cmdline.c:194) leaving endptr at 'B'; sysfs.c:2042 skip_spaces does not move past 'B', sysfs.c:2043 `*endptr != 0` -> -EINVAL. Supported.
- `10 M` rejected EINVAL: blank is not a suffix case, the switch default leaves shl=0 and endptr at the blank (cmdline.c:189 block not entered); sysfs.c:2042 skip_spaces skips the blank, sysfs.c:2043 finds 'M' -> -EINVAL. Supported.
- `-1` rejected EINVAL: simple_strtoull parses no digits (minus is not a digit in any base), endptr stays at '-'; sysfs.c:2043 -> -EINVAL. Supported.
- Bare newline parses as 0 and is accepted: no digits parsed -> ret 0, endptr at '\n'; switch default; sysfs.c:2042 skip_spaces skips '\n' (isspace class) to the terminating NUL; sysfs.c:2043 passes, sysfs.c:2046 `WRITE_ONCE(device->scrub_speed_max, limit)` stores 0. Supported. "(0 means no limit, SR8)" is consistent with the pinned throttle code S242 scrub.c:1380-1381 `bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit == 0) return;` — zero skips throttling; the row's parenthetical cites SR8, which is a declared source of the entry.

Quote checks (all twelve)
- Each `**Quote.**` text was located with `grep -n` in the pinned snapshots and sits exactly on the cited line: cmdline.c:147, 156, 159, 189, 191, 192; vsprintf.c:86; kstrtox.c:29, 30, 33; sysfs.c:2040, 2043 (transcript in the seat receipt). No drift.

Host reading
- "the host's one btrfs device (devid 1) reads scrub_speed_max 0, mode 644, owner root" — capture.txt:8 `scrub_speed_max 1d02a454-.../devinfo/1/scrub_speed_max mode=644 owner=root value=0`. Supported.
- "as uid 1000 with no effective capabilities" — capture.txt:1 `uid=1000 CapEff=0000000000000000`. Supported; a mode-644 root-owned sysfs file is not writable by that caller, so "no limit is set, and this caller cannot write one" follows.
- "Nothing was written to test the parse; the examples above follow from the quoted code" — matches the Limits section ("GR1's examples are derived from the quoted code, not from a write on this host") and the capture's read-only nature. Honest scope.

Overreach check: every factual clause resolves to a quoted or pinned line; the only cross-reference beyond the quoted lines is "(0 means no limit, SR8)", which is attributed to a declared entry source and is independently corroborated by pinned scrub.c:1380-1381. No [inference] mark is needed in this row and none is missing. Row extent is `## GR1` to exclusive `## GR2`; no stray `## ` line inside the section.

Verdict: holds — every clause is supported by the cited lines, quotes are byte-exact on their lines, digests verify, and the section hash binds.
