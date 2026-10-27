ROW GR1 VERDICT: holds

Item: C2-GR1-critic — adversarial read of row GR1 in `corpus/knowledge/btrfs-scrub-grounding-r45.md` at
18389f44cf6ce414d7be205998b29c79fb0b490c (read via `git show <rev>:corpus/knowledge/btrfs-scrub-grounding-r45.md`).

## Snapshot integrity (verified before reading)

- `sha256sum -c .ufo/waves/round-45/frozen/src/SHA256SUMS` in that dir: cmdline.c, dev-replace.c,
  systemd.kill.xml, kstrtox.c, vsprintf.c all `OK`.
- `sha256sum -c .ufo/waves/round-44/frozen/src/SHA256SUMS` in that dir: scrub.c, sysfs.c, btrfs-scrub@.timer,
  btrfs-scrub@.service, PKGBUILD all `OK` (S243 sysfs.c is the GR1 store source).
- capture.txt sha256 f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70 matches the
  header value in the row file.

## Quote-line audit (all 12 GR1 quotes located in the digest-checked snapshots)

- cmdline.c:147 `"potentially suffixed with K, M, G, T, P, E."` — exact, doc comment.
- cmdline.c:156 `"unsigned long long ret = simple_strtoull(ptr, &endptr, 0);"` — exact.
- cmdline.c:159 `"/* Consume valid suffix even in case of overflow. */"` — exact.
- cmdline.c:189 `"if (shl && likely(ptr != endptr)) {"` — exact.
- cmdline.c:191 `"if (unlikely(check_shl_overflow(ret, shl, &ret)))"` — exact.
- cmdline.c:192 `"ret = ULLONG_MAX;"` — exact.
- vsprintf.c:86 `"cp = _parse_integer_fixup_radix(startp, &base);"` — exact (inside `simple_strntoull`,
  which `simple_strtoull` calls at vsprintf.c:112-115).
- kstrtox.c:29 `"if (s[0] == '0') {"`, kstrtox.c:30 `"if (_tolower(s[1]) == 'x' && isxdigit(s[2]))"`,
  kstrtox.c:33 `"*base = 8;"` — exact, inside `_parse_integer_fixup_radix` (kstrtox.c:26-40).
- sysfs.c:2040 `"limit = memparse(buf, &endptr);"` — exact, inside `btrfs_devinfo_scrub_speed_max_store`
  (sysfs.c:2031-2047), bound to the attribute by `BTRFS_ATTR_RW(devid, scrub_speed_max, ...)` at
  sysfs.c:2048-2049 and the path comment sysfs.c:2105.
- sysfs.c:2043 `"if (*endptr != 0)"` — exact.

## Executable cross-check

A faithful simulation of `_parse_integer_fixup_radix` / `_parse_integer_limit` / `simple_strntoull` /
`memparse` / the sysfs.c:2040-2044 store check was compiled and run over 27 inputs (harness and output:
`.ufo/waves/round-45/a2w1/C2CritGR1/sim.c`, `sim-output.txt`; scratch run under
`/fast/scratch/hyaku/tsukuroi-r45/C2CritGR1/`). Every worked example in the row reproduces exactly
(values below); no counterexample found.

## Per-sentence verdicts

Statement sentence 1 — "a write to `devinfo/<devid>/scrub_speed_max` is parsed by `memparse` (SR8),
which calls `simple_strtoull` with base 0": holds. Deciding lines sysfs.c:2040 (`limit = memparse(buf,
&endptr)` is the first statement of the store function) and cmdline.c:156.

Sentence 2 — "`simple_strtoull` resolves base 0 through `_parse_integer_fixup_radix`, which picks
hexadecimal for a leading `0x` followed by a hex digit, octal for any other leading `0`, and decimal
otherwise": holds. Deciding lines vsprintf.c:86 (simple_strntoull → fixup) and kstrtox.c:28-35 — the
code is literally `s[0]=='0'` → (`_tolower(s[1])=='x' && isxdigit(s[2])` → 16, else 8), non-`0` → 10.
Non-blocking note, not an overreach: the code is case-insensitive on the `x` via `_tolower`
(kstrtox.c:30, itself quoted by the row), so `0X10` also parses as 16 — the row's literal `0x` prose
does not spell that out, but the kernel's own doc comment (kstrtox.c:9-10) uses the same `0x`/`0`
shorthand and the row separately spells out case-insensitivity for suffixes only, matching upstream
convention; the sentence is a correct sufficient characterization and misleads on no worked example.

Sentence 3 — "after the digits, `memparse` takes at most one suffix letter, `K`, `M`, `G`, `T`, `P` or
`E` in either case, each step multiplying by a further 1024 (a 10-bit shift per step, so `K` is 1024,
not 1000)": holds. Deciding lines cmdline.c:160-187 (switch on `*endptr` — a single position — with
`shl += 10` per fallthrough level: K→10, M→20, G→30, T→40, P→50, E→60 bits), cmdline.c:191
(`check_shl_overflow(ret, shl, &ret)`), cmdline.c:193 (`endptr++` advances past exactly one letter).
Sim: `1E` → 1152921504606846976 = 2^60 confirms the per-step reading.

Sentence 4 — "the suffix counts only when at least one digit came before it": holds. Deciding line
cmdline.c:189 (`shl && likely(ptr != endptr)`). `endptr` passes `ptr` only when `_parse_integer_limit`
consumed ≥1 digit (kstrtox.c:65-92, advanced at vsprintf.c:91) or when a `0x`/`0X` prefix is skipped —
and the prefix is skipped only if `s[2]` is a hex digit (kstrtox.c:30, 37-38) which the digit loop then
consumes as a digit. So `ptr != endptr` ⟺ ≥1 digit consumed: the row's condition is exactly the code's.
Sim: bare `K\n` → EINVAL, `0xK\n` → EINVAL, `0XK\n` → EINVAL, `0000000000000000000000000K\n` → OK 0.

Sentence 5 — "a shifted value that overflows becomes `ULLONG_MAX`": holds. Deciding lines
cmdline.c:191-192. (Also true upstream of the shift: `_parse_integer_limit` saturates at ULLONG_MAX on
digit overflow, kstrtox.c:83-88; sim `18446744073709551616\n` → OK ULLONG_MAX — unstated but consistent.)

Sentence 6 — "the sysfs store then skips whitespace and returns `-EINVAL` unless the text ends there":
holds. Deciding lines sysfs.c:2042 (`endptr = skip_spaces(endptr)`) and 2043-2044 (`if (*endptr != 0)
return -EINVAL`). Sim: `10 M\n` EINVAL, `1 \n` OK — trailing whitespace skipped, interior non-digit text
rejected.

Worked examples — "`100M`/`100m` → 104857600, `010` → 8, `0x10` → 16; `10MB`, `10 M`, `-1` → EINVAL;
bare newline → 0 accepted and removes the limit (0 means no limit, SR8)": all hold. Sim output:
`100M\n` = 104857600 (100×2^20), `100m\n` = 104857600, `010\n` = 8 (octal), `0x10\n` = 16,
`10MB\n`/`10 M\n`/`-1\n` all EINVAL, `\n` → OK 0. The "0 means no limit" tail is grounded by the
cited SR8, which pins scrub.c:1380-1382 (`bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit ==
0) return;` in the throttle) — verified in the S242 digest-checked snapshot.

Host reading sentence 1 — "the host's one btrfs device (devid 1) reads `scrub_speed_max` 0, mode 644,
owner root (capture.txt:8), as uid 1000 with no effective capabilities (capture.txt:1): no limit is
set, and this caller cannot write one": holds. capture.txt:8 is
`scrub_speed_max 1d02a454-.../devinfo/1/scrub_speed_max mode=644 owner=root value=0`; capture.txt:1 is
`uid=1000 CapEff=0000000000000000`. "One btrfs device" is supported by complete enumeration:
capture.sh loops `/sys/fs/btrfs/*/devinfo/*/scrub_speed_max` and `/sys/fs/btrfs/*/devinfo` and each glob
produced exactly one line (capture.txt:8, capture.txt:9 `devids=1`). Mode 644 + owner root + CapEff=0 →
this caller cannot write.

Host reading sentence 2 — "nothing was written to test the parse; the examples above follow from the
quoted code": holds. Honest provenance marking; capture.txt contains only reads; consistent with the
host guard against sysfs writes.

## Counterexamples attempted and closed

- `0xK\n` (suffix with no parsed digit after a bare `0x`): predicted-ambiguous under the row's
  digit-before-suffix rule; actual code → EINVAL because `0x` is not prefix-skipped unless `s[2]` is a
  hex digit (kstrtox.c:30), and 'K' is not one. Row survives.
- `0X10` (uppercase prefix): parses as 16 via `_tolower` (kstrtox.c:30); the row's literal `0x` does not
  say so, but the quoted line itself carries `_tolower`, the row claims case-insensitivity for suffixes
  only in the same breath, and kernel docs (kstrtox.c:130-131) use identical shorthand. Inexactness at
  most, not a wrong sentence.
- `+1\n` → EINVAL (sign not consumed by `simple_strtoull`; consistent — row never claims `+` works).
- ` 1\n` → EINVAL (no leading-skip in memparse; consistent with the row's "then skips whitespace" only
  after the number).
- `10KK\n`, `0b10\n`, `1E9\n`, `0x\n` → EINVAL; `18446744073709551616\n` → OK ULLONG_MAX — all
  consistent with the stated rules.
- Persistence/other-write-path check: the only writer of `device->scrub_speed_max` in the pinned tree is
  this store (sysfs.c:2045 WRITE_ONCE); readers are sysfs.c:2028 show and scrub.c:1380 throttle.

## Scope note

The row's triage bullet ("a leading zero is octal and `K`/`M`/`G` are powers of 1024"; "a bare newline
written to the file clears it") and Limits bullet ("examples are derived from the quoted code, not from
a write on this host") are consistent with the findings above.

What I did not do: no sysfs write was attempted (host guard forbids it, and capture.txt:1 confirms the
caller cannot); the C simulation is a transcription of the pinned code, not a kernel run — the deciding
lines above are the authority.

Tool installs: none (gcc already present; used only inside my scratch dir).
