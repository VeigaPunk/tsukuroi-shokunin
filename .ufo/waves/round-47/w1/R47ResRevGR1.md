ROW GR1 VERDICT: holds
SECTION SHA256: fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8

Reviewed row GR1 of corpus/knowledge/btrfs-scrub-grounding-r45.md at revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 (read via `git show 77e9e2b2e:corpus/knowledge/btrfs-scrub-grounding-r45.md`, extent `## GR1` up to exclusive `## GR2`; no other `## ` line inside — the frozen counter reports structural_ok 1, problems []).

Hash binding:
- Frozen counter (`python3 tools/check-scrub-admission-r47.py --revision 77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash`) prints GR1 = fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8; my independent re-derivation (sha256 over the LF-joined lines from `## GR1` to exclusive `## GR2`, no trailing newline) reproduces the same digest. (A naive `sed | sha256sum` including the trailing newline gives 998fdd2f… and does not match; the counter's split/join method is the canonical one and is what I bind.)
- Counter freeze verified: `git show 77e9e2b2e:tools/check-scrub-admission-r47.py | sha256sum` = e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b, matching the declared frozen digest.
- Snapshot digests verified with `sha256sum -c`: .ufo/waves/round-45/frozen/src/SHA256SUMS → cmdline.c OK, vsprintf.c OK, kstrtox.c OK; .ufo/waves/round-44/frozen/src/SHA256SUMS → sysfs.c OK. S249 capture.txt sha256 = f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70, matching the entry header's recorded digest.

Quote check (every `**Quote.**` text is on its cited line in the pinned snapshot):
- cmdline.c:147 (S246) carries "potentially suffixed with K, M, G, T, P, E." ✓
- cmdline.c:156 "unsigned long long ret = simple_strtoull(ptr, &endptr, 0);" ✓
- cmdline.c:159 "/* Consume valid suffix even in case of overflow. */" ✓
- cmdline.c:189 "if (shl && likely(ptr != endptr)) {" ✓
- cmdline.c:191 "if (unlikely(check_shl_overflow(ret, shl, &ret)))" ✓
- cmdline.c:192 "ret = ULLONG_MAX;" ✓
- vsprintf.c:86 (S246) "cp = _parse_integer_fixup_radix(startp, &base);" ✓
- kstrtox.c:29 "if (s[0] == '0') {" ✓; kstrtox.c:30 "if (_tolower(s[1]) == 'x' && isxdigit(s[2]))" ✓; kstrtox.c:33 "*base = 8;" ✓ (decimal-otherwise branch at kstrtox.c:34-35, hex branch at kstrtox.c:30-31)
- sysfs.c:2040 (S243) "limit = memparse(buf, &endptr);" ✓; sysfs.c:2043 "if (*endptr != 0)" ✓

Clause-by-clause review of the Statement:
- "a write to devinfo/<devid>/scrub_speed_max is parsed by memparse, which calls simple_strtoull with base 0": sysfs.c:2040 calls memparse(buf, &endptr); cmdline.c:156 shows memparse calling simple_strtoull(ptr, &endptr, 0). Supported.
- "simple_strtoull resolves base 0 through _parse_integer_fixup_radix": simple_strtoull (vsprintf.c:112-115) calls simple_strntoull (vsprintf.c:79-101), whose line 86 calls _parse_integer_fixup_radix(startp, &base). Supported.
- "hexadecimal for a leading 0x followed by a hex digit, octal for any other leading 0, and decimal otherwise": kstrtox.c:28-37 — base==0: s[0]=='0' → 'x'+isxdigit(s[2]) → base 16 (lines 30-31), else base 8 (line 33); no leading 0 → base 10 (lines 34-35); 0x prefix skipped only when base 16 (lines 36-37). Exact match.
- "After the digits, memparse takes at most one suffix letter, K, M, G, T, P or E in either case": cmdline.c:160-187 switch on *endptr covers exactly {'E','e','P','p','T','t','G','g','M','m','K','k'} and consumes exactly one char (single endptr++ at cmdline.c:193). Supported.
- "each step multiplying by a further 1024 (a 10-bit shift per step, so K is 1024, not 1000)": shl += 10 per fallthrough level (cmdline.c:163,167,171,175,179,183) and the shift is applied by check_shl_overflow(ret, shl, &ret) (cmdline.c:191), i.e. a left shift by shl bits; K ⇒ shl=10 ⇒ ×1024. Supported.
- "the suffix counts only when at least one digit came before it": cmdline.c:189 `if (shl && likely(ptr != endptr))` — the suffix is applied and consumed only when a suffix letter was seen AND ptr != endptr (at least one digit parsed). Supported.
- "a shifted value that overflows becomes ULLONG_MAX": cmdline.c:191-192. Supported (this covers the shift overflow; the row claims nothing about digit-parse overflow, whose FIXME at vsprintf.c:90-91 is correctly left unclaimed).
- "The sysfs store then skips whitespace and returns -EINVAL unless the text ends there": sysfs.c:2042 skip_spaces(endptr); 2043-2044 `if (*endptr != 0) return -EINVAL;`. Supported.
- Worked examples, each re-derived from the quoted code:
  - `100M` → 100<<20 = 104857600 ✓ (cmdline.c:177-179 'M' shl=20)
  - `100m` → same branch ✓
  - `010` → base 8 ⇒ 8 ✓ (kstrtox.c:32-33)
  - `0x10` → base 16, prefix skipped ⇒ 16 ✓ (kstrtox.c:30-31,36-37)
  - `10MB` → 'M' consumed as the one suffix, trailing 'B' left → store EINVAL ✓
  - `10 M` → space ends the digit parse, switch(' ') hits default (shl=0), store skip_spaces lands on 'M' → EINVAL ✓
  - `-1` → no digits parsed (ptr==endptr), '-' untouched → EINVAL ✓ (cmdline.c:189 guard; no sign handling in _parse_integer_limit)
  - bare newline → no digits, result 0, shl=0; store skip_spaces consumes '\n' → *endptr==0, accepted, limit=0 written (sysfs.c:2045) ✓
- "which removes the limit (0 means no limit, SR8)": the pinned snapshots confirm the write path and the written 0; the "0 = no limit" semantic is attributed to SR8, the entry's registered source for the round-44 memparse/scrub_speed_max inference (entry header scope paragraph names SR8 as "what memparse accepts when scrub_speed_max is written"). The attribution is the entry's own convention (QUALITY 86: each rule row cites an upstream source row); the claim is not presented as following from the pinned lines, and no [inference] mark is needed since it is sourced, not inferred.

Host reading:
- "The host's one btrfs device (devid 1) reads scrub_speed_max 0, mode 644, owner root (capture.txt:8)": capture.txt line 8 reads `scrub_speed_max 1d02a454-…/devinfo/1/scrub_speed_max mode=644 owner=root value=0`; capture.txt:9 lists `devids=1`. Supported.
- "as uid 1000 with no effective capabilities (capture.txt:1)": capture.txt line 1 reads `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000`. Supported.
- "no limit is set, and this caller cannot write one": value=0 plus mode 644 owner root with uid 1000 no caps ⇒ cannot write. Supported.
- "Nothing was written to test the parse; the examples above follow from the quoted code": consistent with the entry's Limits section and the read-only capture method; no contrary evidence in the pinned bytes.

No clause overreaches; every quote is verbatim on its cited line; no [inference] or [unknown] marks sit inside the row. Row GR1 is admissible knowledge as written.
