ROW GR1 VERDICT: holds
SECTION SHA256: fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8

Critic seat R47CritGR1b, item C1-GR1-R47CritGR1b. Attack on row GR1 at revision 77e9e2b2e96b85d8f048ae2087e246a542b71611.

Section extent and hash
- Extracted the row (`## GR1` up to exclusive `## GR2`): 41 lines. `python3 tools/check-scrub-admission-r47.py --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash` printed GR1 = fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8 (structural_ok 1, no problems). Independent re-derivation (LF-join of the extent lines, no trailing newline, sha256) reproduces the same value.

Snapshot integrity
- `sha256sum -c` over the round-45 frozen src SHA256SUMS: cmdline.c OK, vsprintf.c OK, kstrtox.c OK; over round-44 frozen src SHA256SUMS: sysfs.c OK. capture.txt sha256 f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70 matches the digest declared in the entry header.

Clause-by-clause
- "a write to devinfo/<devid>/scrub_speed_max is parsed by memparse (SR8)": the store body at sysfs.c:2040 is `limit = memparse(buf, &endptr);`. Supported.
- "memparse calls simple_strtoull with base 0": cmdline.c:156 `unsigned long long ret = simple_strtoull(ptr, &endptr, 0);`. Supported.
- "simple_strtoull resolves base 0 through _parse_integer_fixup_radix": vsprintf.c:86 `cp = _parse_integer_fixup_radix(startp, &base);`. Supported.
- "hexadecimal for a leading 0x followed by a hex digit, octal for any other leading 0, decimal otherwise": kstrtox.c:29 `if (s[0] == '0')`, kstrtox.c:30 `if (_tolower(s[1]) == 'x' && isxdigit(s[2]))` -> kstrtox.c:31 `*base = 16;`, else branch kstrtox.c:33 `*base = 8;`, non-`0` first char -> kstrtox.c:35 `*base = 10;`. The statement matches the branch structure exactly.
- "at most one suffix letter K/M/G/T/P/E in either case, each step a further 1024": cmdline.c:160 `switch (*endptr)` lists both cases per letter with `shl += 10` per fallthrough rung (K=10 up to E=60 bits, i.e. 1024^n, so K is 1024 not 1000); endptr advances once inside cmdline.c:189 `if (shl && likely(ptr != endptr))` with cmdline.c:193 `endptr++;` executed at most once. Supported.
- "suffix counts only when at least one digit came before it": cmdline.c:189 `ptr != endptr` is exactly the digit-consumed test (simple_strtoull advances endptr only over consumed characters). Supported.
- "a shifted value that overflows becomes ULLONG_MAX": cmdline.c:191 `check_shl_overflow(ret, shl, &ret)` -> cmdline.c:192 `ret = ULLONG_MAX;`. Supported.
- "the sysfs store then skips whitespace and returns -EINVAL unless the text ends there": sysfs.c:2041 comment (`trailing '\n' ... typos`), sysfs.c:2042 `endptr = skip_spaces(endptr);`, sysfs.c:2043 `if (*endptr != 0)`, sysfs.c:2044 `return -EINVAL;`. Supported.

Worked examples traced against the quoted code
- `100M`/`100m` -> base 10, 100 << 20 = 104857600 (the M/m rung adds 20 shl): correct. `010` -> octal 8; `0x10` -> hex 16 (kstrtox.c:29-31): correct.
- `10MB`: after the single suffix step endptr sits at `B`; sysfs.c:2043 -> EINVAL: correct. `10 M`: ` ` is not a suffix so memparse leaves endptr at the blank; skip_spaces (sysfs.c:2042) exposes `M` -> EINVAL: correct.
- `-1`: simple_strtoull consumes nothing for a leading `-` (this path has no sign handling), endptr stays at `-` -> EINVAL via sysfs.c:2043: correct.
- bare `\n`: parses as 0, endptr at the newline; skip_spaces consumes it, *endptr==0 -> accepted, limit 0. "0 means no limit" is borne by scrub.c:1380-1381 (`bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit == 0) return;` — no throttle when zero). Correct.

Host reading
- capture.txt:8 `scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max mode=644 owner=root value=0` and capture.txt:1 `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000` support "no limit is set" and "this caller cannot write one" (mode 644 root-owned attribute, uid 1000, empty CapEff). "Nothing was written to test the parse" is consistent — and required, since the caller cannot write.

Quote audit
- All 12 `**Quote.**` texts verified byte-exact at their cited lines in the digest-checked snapshots: cmdline.c:147, cmdline.c:156, cmdline.c:159, cmdline.c:189, cmdline.c:191, cmdline.c:192, vsprintf.c:86, kstrtox.c:29, kstrtox.c:30, kstrtox.c:33, sysfs.c:2040, sysfs.c:2043.
- No [inference] marks inside GR1; every clause traces to quoted lines or is flagged as derived ("the examples above follow from the quoted code"). The `lib/`-patch assumption disclosed in `## Limits` is outside the row and does not affect these bytes.

Verdict: every clause of Statement and Host reading is supported by the pinned lines; holds.
