VERDICT: supports

# C2-2 — executable harness for GR1 (`memparse` → `scrub_speed_max` store)

Seat `C2ExecMemparseHarness`, wave a2w1. Item: build a userspace C harness from the pinned bytes
(`memparse`, `simple_strtoull`/`simple_strntoull`, `_parse_integer_fixup_radix`, `_parse_integer_limit`,
`check_shl_overflow`, `skip_spaces`, and the store logic of `sysfs.c:2031-2047`), run it on the 17 named
inputs, and say whether every GR1 example holds. Result: the harness exists, every copied line is
byte-identical to its pinned source, and **all 45 probed inputs — the 17 required plus 28 depth probes —
behave as GR1's sentences say, with 0 mismatches against the expectations the row states or implies**.
GR1 states nothing wrongly. It leaves four behaviours unstated, listed in "Row gaps" below; none of them
contradicts the row, and one of them (digit-only overflow silently saturating) is operationally material.

Receipts (all under `.ufo/waves/round-45/a2w1/C2ExecMemparseHarness/`):

| file | sha256 | note |
|---|---|---|
| `harness.c` | `06763d4d7963a6ba7e4049adbafb478891470233aca00747e3da1ed5fa65df1d` | 18706 B, generated; 17 verbatim blocks + driver + 45-case table |
| `table.txt` | `21531b9f6e1a0bce77cf29a35809004da8acca98339b1571d5ae0e4eb96c6596` | harness stdout, byte-identical on rerun |
| `verify.log` | — | ends `OK: 0 failed check(s)` |
| `build.log` | — | 0 bytes: `gcc -std=gnu11 -O1 -Wall -Wextra` clean (GCC 16.2.1, glibc 2.44; `toolchain.txt`) |
| `manifest.sha256` | — | digest + line range per source file and block |
| `make_harness.py`, `verify_verbatim.py` | — | generator and re-extraction checker (seat dir rebuilds itself: no scratch path needed) |
| `src/` | — | the seven files this seat fetched (`overflow.h ctype.h ctype.c kstrtox.h string_helpers.c kernfs-file.c read_write.c`) |
| `FETCH-a2.txt` | — | URLs, timestamps, tag peel, per-file sha256 |

## 1. The copies are byte-exact, not retyped

`make_harness.py` assembles `harness.c` by extracting line ranges from the pinned files; `verify_verbatim.py`
re-extracts the same ranges and diffs them against the `@@BEGIN/@@END` blocks, then re-hashes every source:

- `verify.log` → 17 × `PASS <block> … (N lines, M bytes)` and `OK: 0 failed check(s)`; the manifest leg is
  17 × `PASS` over the sources (`ce146120…` sysfs.c, `1af5ad98…` cmdline.c, `cabb648a…` vsprintf.c,
  `0c52ae02…` kstrtox.c, plus this seat's fetches).
- Block map in `harness.c`: `:61` ctype masks, `:72` ctype macros, `:90` `_tolower`, `:101` `_ctype` table,
  `:129` `__must_check_overflow`, `:136` `check_add_overflow`, `:141` `check_mul_overflow`,
  `:146` `check_shl_overflow`, `:160` `KSTRTOX_OVERFLOW`, `:168` `_parse_integer_fixup_radix`,
  `:187` `_parse_integer_limit`, `:229` `_parse_integer`, `:237` `simple_strntoull`, `:264` `simple_strtoull`,
  `:272` `memparse`, `:323` `skip_spaces`, `:332` the store.
- `check_shl_overflow` is defined exactly as `include/linux/overflow.h:192-202`, fetched this seat:
  sha256 `2fe83917dd2718dec8a52c5eb0bb20b4e4bf6e2b2588c9e1a4d36c8a7d97dd3d`. Pin chain:
  `git ls-remote` → `v7.2.11` = `8316c24e…`, peel `^{}` = `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`
  (matches the wave's `FETCH.txt`); the same seven files re-fetched at `h=a2de78ee…` are `cmp`-identical
  (`FETCH-a2.txt`). `skip_spaces` is not in `lib/string.c` at this tag — it lives at
  `lib/string_helpers.c:846-851` (sha256 `674e41d0…`), which is what the harness copies.
- Hand-written text is limited to compiler annotations and the types the bodies name
  (`harness.c:20-57`: `likely`/`unlikely`, `fallthrough` = `__attribute__((__fallthrough__))`,
  `noinline`, `__must_check`, `kobject`, `kobj_attribute`, `btrfs_device`, `container_of`, `WRITE_ONCE`).
  No parse or store statement is hand-written; the store's `container_of` line is the copied one
  (`harness.c:337`) against a plain struct.

## 2. The 17 required inputs

`table.txt` line 8+n is case n; its column 3 is the hex of the bytes written. `-22` is `-EINVAL`; "end@" is the
offset of the byte `memparse` left behind.

| # | input | `memparse` | end@ | store ret | stored limit | GR1 says | match |
|---|---|---|---|---|---|---|---|
| 0 | `100M\n` | 104857600 | 4 `\n` | 5 | 104857600 | accepted, 2^20·100 | ok |
| 1 | `100m\n` | 104857600 | 4 `\n` | 5 | 104857600 | accepted, same | ok |
| 2 | `010\n` | 8 | 3 `\n` | 4 | 8 | octal → 8 | ok |
| 3 | `08\n` | 0 | 1 `8` | -22 | unchanged | (implied: `8` not octal) | ok |
| 4 | `0x10\n` | 16 | 4 `\n` | 5 | 16 | hex → 16 | ok |
| 5 | `0x\n` | 0 | 1 `x` | -22 | unchanged | (implied: no hex digit → base 8 stops at `x`) | ok |
| 6 | `10MB\n` | 10485760 | 3 `B` | -22 | unchanged | rejected | ok |
| 7 | `10 M\n` | 10 | 2 ` ` | -22 | unchanged | rejected | ok |
| 8 | `-1\n` | 0 | 0 `-` | -22 | unchanged | rejected | ok |
| 9 | `\n` | 0 | 0 `\n` | 1 | 0 | accepted, clears the limit | ok |
| 10 | *(empty)* | 0 | 0 `\0` | **0** | 0 | silent → see §4 | — |
| 11 | `16E\n` | ULLONG_MAX | 3 `\n` | 4 | ULLONG_MAX | shift overflow saturates | ok |
| 12 | `17E\n` | ULLONG_MAX | 3 `\n` | 4 | ULLONG_MAX | shift overflow saturates | ok |
| 13 | `15E\n` *(depth probe)* | 17293822569102704640 | 3 `\n` | 4 | same | largest `E` that fits | — |
| 14 | `18446744073709551615\n` | ULLONG_MAX | 20 `\n` | 21 | ULLONG_MAX | (implied: fits) | ok |
| 15 | `18446744073709551616\n` | ULLONG_MAX | 20 `\n` | 21 | ULLONG_MAX | silent → see §4 | — |
| 16 | `1k\n` | 1024 | 2 `\n` | 3 | 1024 | 1024, not 1000 | ok |
| 17 | ` 5\n` | 0 | 0 ` ` | -22 | unchanged | (implied: no leading-space skip) | ok |

`16E`/`17E` (cases 11, 12) saturate because the `case 'E'` chain falls through five more `shl += 10`, i.e. `E` is 60 bits:
`15E` = 17293822569102704640 (fits, case 13, `table.txt:21`) and `16E` = 2^64 exactly (saturates). My first
rendering of these two expectations used 50 bits and reported MISMATCH; that was my expectation being wrong,
not the kernel: the harness's own arithmetic exposed it and it is corrected in `make_harness.py:130-132`.

## 3. Sentence-by-sentence against GR1

1. "parsed by `memparse`, which calls `simple_strtoull` with base 0" — `harness.c:276` (copied from
   `cmdline.c:156`), exercised by every row.
2. base-0 resolution (hex for `0x`+hex digit, octal for any other leading `0`, else decimal) — cases 2, 4,
   5, 33 (`0X1f` → 31), 34 (`0x1f` → 31), 35 (`0b101` → `-EINVAL`, base 8 stops at `b`).
3. "at most one suffix letter, K M G T P E in either case" — `1G`/`1T`/`1P`/`1E` → 1073741824 /
   1099511627776 / 1125899906842624 / 1152921504606846976 (cases 23-26); `10MB` leaves `B` (case 6);
   `0x10K` → 16384 (case 22), so a suffix may follow a hex number.
4. "each step multiplying by a further 1024 (K is 1024, not 1000)" — `1k` = 1024, `1030K` = 1054720,
   `1000000000000K` = 1024000000000000 (cases 16, 43, 44).
5. "the suffix counts only when at least one digit came before it" — `K\n` → `-EINVAL` (case 18),
   `0xK\n` and `0XK\n` → `-EINVAL` (cases 19, 20), `0K\n` → accepted as 0 (case 21). The guard is
   `ptr != endptr` (`harness.c:308`); for base 0 that is equivalent to "≥1 digit", because the `0x` prefix
   is only consumed when a hex digit follows it (`kstrtox.c:30`). **Holds.**
6. "a shifted value that overflows becomes ULLONG_MAX" — `16E`, `17E`, `16384E`,
   `18446744073709551615K`, `17179869184E` all store ULLONG_MAX and are accepted (cases 11, 12, 28, 29, 30).
7. "the store skips whitespace and returns -EINVAL unless the text ends there" — `10MB`, `10 M`, `10\nx`
   rejected (cases 6, 7, 40); trailing whitespace of any `_S` kind accepted: `100M `, `100M\n\n`,
   `100M\r\n`, `5\t` (cases 37-39, 42), i.e. more than the "trailing `\n`" comment at `sysfs.c:2041`.
8. "100M and 100m both set 104857600" — cases 0, 1.
9. "010 sets 8 and 0x10 sets 16" — cases 2, 4.
10. "10MB, 10 M, -1 are rejected with EINVAL" — cases 6, 7, 8.
11. "a bare newline parses as 0 and is accepted, which removes the limit (0 means no limit)" — case 9, and
    the semantics are pinned: `scrub.c:1380-1382` `bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit == 0) return;`
    (round-44 `scrub.c`, S242) — zero skips throttling entirely.

**Nothing in GR1 is stated wrongly.** My two candidate defects did not survive the run:
`0xK` is *not* accepted through the prefix-only guard (base 8 is chosen, so the prefix is never consumed), and
the "at least one digit" phrasing is exact for base 0.

## 4. Row gaps (unstated, not falsified) — for a2r1 residual seats, not for a2w1 repair

1. **Digit-only overflow saturates silently.** `18446744073709551616\n` (exactly 2^64) and
   `99999999999999999999999\n` are **accepted** and store `ULLONG_MAX` (cases 15, 31): `_parse_integer_limit`
   sets `res = ULLONG_MAX` with `overflow = KSTRTOX_OVERFLOW` (`harness.c:215-218`) and `simple_strntoull`
   then strips the flag from the count (`harness.c:251`, `cp += (rv & ~KSTRTOX_OVERFLOW);`), so the store
   sees a clean end-of-string. GR1 only promises saturation for *shift* overflow. Operationally a
   mistyped 20+ digit value is not a typo the kernel refuses — it sets an enormous limit. Worth one
   sentence in GR1 the next time the row is opened.
2. **Only trailing whitespace is skipped.** ` 5\n` and `\t5\n` are `-EINVAL` (cases 17, 41) while `5\t\n`
   and `100M \n` are accepted (cases 42, 37): `skip_spaces` runs on `endptr` only (`harness.c:344`).
   Same for `+5\n` → `-EINVAL` (case 32): `simple_strtoull` has no `'+'` handling, unlike `kstrtoull`.
3. **An empty write is accepted as 0.** `store(buf, len = 0)` returns 0 and stores 0 (case 10, `table.txt:18`). Nothing
   upstream rejects a zero-length write: `vfs_write` has no `count == 0` short-circuit and `rw_verify_area`
   only rejects negative counts (`read_write.c:458-459`, `:667-697`), and `kernfs_fop_write_iter` takes
   `min_t(size_t, len, PAGE_SIZE)`, NUL-terminates and calls `ops->write` even for `len == 0`
   (`kernfs-file.c:307-345`). So a program issuing `write(fd, "", 0)` clears the limit exactly like a bare
   newline; a shell `> file` does not, because it issues no write. Source-derived, not tested on the host
   (no sysfs write is permitted to this seat).
4. **Digits that are invalid for the detected base are a hard error, not a partial parse**: `08` → `-EINVAL`
   (case 3) although `8` is a decimal digit; `0x` alone → `-EINVAL` (case 5). GR1 implies both; a reader
   writing `08` for "eight" gets a failed write.

## 5. Limits of this evidence

- No sysfs write, no `btrfs` call, no kernel execution: the harness is a userspace model of the pinned
  bodies. The host's own parse was not exercised (the caller cannot write the attribute — `capture.txt:1,8`:
  `CapEff=0`, `scrub_speed_max … value=0`).
- No independent oracle was run: `lib/cmdline_kunit.c` does not exist at v7.2.11 (HTTP 404, `FETCH-a2.txt`),
  so fidelity rests on byte-identity plus the trace columns (value, endptr offset, byte at endptr) being
  consistent with the copied code.
- `container_of`/`WRITE_ONCE` are the kernel bodies with type checks dropped; `kobj_attribute` is a stub
  (the store never dereferences `a`); `kobj` is a real struct so `container_of` lands on the right device.
- Not run by this seat: the C2 counter `check-scrub-grounding-r45.py` and any C1 counter (not this item).
- No tools were installed or upgraded (gcc 16.2.1 and glibc 2.44 were already present); no package manager
  was invoked.

Report path: `tsukuroi-shokunin/.ufo/waves/round-45/a2w1/C2ExecMemparseHarness.md`
