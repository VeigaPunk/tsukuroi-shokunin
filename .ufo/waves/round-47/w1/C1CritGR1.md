VERDICT: supports

Seat: C1CritGR1 (wave w1, item C1-R9). Fresh, independent attack on GR1 of
`corpus/knowledge/btrfs-scrub-grounding-r45.md` at the freeze revision
77e9e2b2e96b85d8f048ae2087e246a542b71611 (extracted `## GR1` bytes from
`git show 77e9e2b2e96b85d8f048ae2087e246a542b71611:corpus/knowledge/btrfs-scrub-grounding-r45.md`,
row extent `## GR1`..exclusive `## GR2`). Not a counted seat; no ROW/hash header required.

# Method

1. Digest integrity: `sha256sum -c SHA256SUMS` run inside
   `.ufo/waves/round-45/frozen/src/` (cmdline.c, vsprintf.c, kstrtox.c, dev-replace.c, systemd.kill.xml all OK)
   and `.ufo/waves/round-44/frozen/src/` (scrub.c, sysfs.c, btrfs-scrub@.service, btrfs-scrub@.timer, PKGBUILD all OK).
2. Provenance: round-45 `FETCH.txt` shows S246 fetched from
   `git.kernel.org .../stable/linux.git/plain/lib/{cmdline.c,vsprintf.c,kstrtox.c}?h=v7.2.11`, tag v7.2.11 peeled
   `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`; round-44 `FETCH.txt` shows S242/S243 from the same tag.
   Header of the grounding doc states `verified-at: 2026-10-27 (Linux tag v7.2.11 ... host systemd 262 (262-1-arch), kernel 7.2.11-arch1-1)`.
3. Static clause-by-clause attack of the row against snapshot bytes (all cited line numbers anchor exactly; every quoted
   line verified byte-identical with `sed -n '<N>p'`).
4. Executable attack: a simulation harness (`w1/C1CritGR1/parse_sim.c`) transcribing verbatim from the snapshots —
   kstrtox.c:26-40 `_parse_integer_fixup_radix`, kstrtox.c:58-95 `_parse_integer_limit`, vsprintf.c:79-101
   `simple_strntoull`, vsprintf.c:112-115 `simple_strtoull`, cmdline.c:153-200 `memparse`, and the S243 store tail
   sysfs.c:2040-2046 — with kernel helpers (`_tolower`, `isxdigit`, `isspace`, `skip_spaces`, `check_shl_overflow`,
   `check_mul_overflow`, `check_add_overflow`) shimmed to linux/ctype.h and linux/overflow.h semantics. Compiled
   `gcc -std=gnu17 -O1` in scratch; observed output saved at `w1/C1CritGR1/parse_sim.out`. This is a transcription
   harness, not a kernel build; the parse-deciding core is character-for-character snapshot code.
5. Frozen counter state (informational for the L1, not my gate): at 77e9e2b the row shows
   `quotes: {ok: 12, quotes: 12, bad: []}`, `citations_ok: true`, `distinct_bodies: true`, `citation_problems: []`,
   `row_ok: false` solely because seats report `dispatched 0 times` (wave w1 still in flight). Full JSON at
   `w1/C1CritGR1/counter-r47-gr1-snapshot.json`.

# Seat-assigned probes

**Probe 1 — "does vsprintf.c really choose octal for `010`?"** YES, via indirection the row states correctly.
`simple_strtoull` (vsprintf.c:112-115) wraps `simple_strntoull` (vsprintf.c:79-101); line 86
`cp = _parse_integer_fixup_radix(startp, &base);` does the base-0 resolution, and the chooser body lives in kstrtox.c:26-40:
`0` + `tolower(s[1])=='x'` + `isxdigit(s[2])` -> 16; any other leading `0` -> 8; else 10. `010` -> base 8 -> digits "10" -> 8.
The row's wording "simple_strtoull resolves base 0 through `_parse_integer_fixup_radix`, which picks ..." is precise; the
vsprintf.c:86 quote sits in the correct function. Simulation: `010` -> ACCEPT limit=8. HOLD.

**Probe 2 — "does kstrtox.c prove the case-insensitive suffix?"** NO — and the row does not claim it does. kstrtox.c's
`_tolower` (line 30, 37) proves case-insensitivity of the `0x` PREFIX only. The suffix case-insensitivity ("K, M, G, T, P
or E in either case") is proven by cmdline.c:160-187 dual case labels (`'E'/'e'`, `'P'/'p'`, `'T'/'t'`, `'G'/'g'`,
`'M'/'m'`, `'K'/'k'`). The row's kstrtox.c quotes are mapped to the radix clauses, not the suffix clause — attribution is
clean. Simulation: `100M` and `100m` both -> ACCEPT limit=104857600. HOLD (with a precision note below).

**Probe 3 — "is the write path really the memparse one at sysfs.c:2040?"** YES. The store is
`btrfs_devinfo_scrub_speed_max_store` (S243 sysfs.c:2031-2047); line 2040 is exactly `limit = memparse(buf, &endptr);`,
registered by `BTRFS_ATTR_RW(devid, scrub_speed_max, ...)` at 2048-2049 and present in the devid attribute group at 2113.
The host-visible path shape is confirmed by S242 scrub.c:1369 comment `/sys/fs/UUID/devinfo/devid/scrub_speed_max`. HOLD.

# Per-clause verdicts

| # | Clause (as stated in the row) | Verdict | Evidence |
|---|---|---|---|
| A | write to `devinfo/<devid>/scrub_speed_max` parsed by memparse (SR8) | HOLDS | sysfs.c:2040, 2048-2049, 2113 |
| B | memparse calls `simple_strtoull` with base 0 | HOLDS | cmdline.c:156 (byte-exact quote) |
| C | base 0 -> hex for leading `0x` + hex digit, octal for other leading `0`, decimal else | HOLDS | kstrtox.c:26-40; vsprintf.c:86,112-115 |
| D | at most one suffix letter K/M/G/T/P/E, either case, x1024 per step (10-bit shift, K=1024 not 1000) | HOLDS | cmdline.c:160-187 switch with fallthrough `shl += 10` per level; E=60,P=40,T=30,G=20,M=10,K=... 'E' accumulates 60 = 2^60 = 1024^6. Sim `100M`=104857600 |
| E | suffix counts only when >=1 digit precedes | HOLDS | cmdline.c:189-194: `endptr++` is INSIDE the `if (shl && likely(ptr != endptr))` guard, so a bare suffix is neither consumed nor applied; sim `K` -> EINVAL (unconsumed 'K' fails the sysfs garbage check). Row's mechanism claim exact |
| F | shifted value that overflows becomes ULLONG_MAX | HOLDS | cmdline.c:191-192 (byte-exact); sim `16384E` -> ACCEPT limit=18446744073709551615 (2^14<<60 overflows) |
| G | sysfs store skips whitespace, -EINVAL unless text ends there | HOLDS | sysfs.c:2041-2044 `endptr = skip_spaces(endptr); if (*endptr != 0) return -EINVAL;` (2043 byte-exact) |
| H | `100M`, `100m` -> 104857600; `010` -> 8; `0x10` -> 16 | HOLDS | sim rows 1-4 |
| I | `10MB`, `10 M`, `-1` -> EINVAL | HOLDS | sim rows 5-7: trailing 'B'; 'M' after skipped space; '-' lands at endptr and fails the NUL check |
| J | bare newline parses as 0, accepted, removes the limit (0 = no limit, SR8) | HOLDS | sim row 8 (`\n` -> ACCEPT limit=0); SR8 confirmed in S242 scrub.c:1380-1382 `bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit == 0) return;` |

All twelve row quotes are byte-identical at their cited lines (verified individually with `sed -n '<N>p'` against the
snapshots). Host-reading tail of the row is consistent with S249 capture.txt:1 (`uid=1000 CapEff=0000000000000000`,
sha256 f5958a83... matches the doc's stated digest) and capture.txt:8 (`scrub_speed_max .../devinfo/1/scrub_speed_max
mode=644 owner=root value=0`); nothing in the row hinges on a write test, and none was performed.

# Strongest counterexamples tried (all consistent with the row)

- `K` (bare suffix, no digit) -> EINVAL — consistent with clause E; consequence the row does not state but does not contradict.
- ` 10` (leading space) -> EINVAL — memparse does not skip leading whitespace; the row's "the sysfs store then skips
  whitespace" refers to the trailing check only, and its examples do not claim leading-space tolerance. Not a defect.
- `18446744073709551616` (2^64, unshifted overflow) -> ACCEPT limit=ULLONG_MAX via `_parse_integer_limit`'s own cap
  (kstrtox.c:86-88). The row claims ULLONG_MAX only for the SHIFTED case; accurate, narrower than the code's full behavior.
- `0x\n`, `0xg` -> EINVAL: base falls back to 8 when no hex digit follows `0x`, leaving trailing 'x'. Exactly matches the
  row's "a leading `0x` followed by a hex digit" qualifier.
- `08` -> EINVAL ('8' invalid in base 8, trailing). `1e5` -> EINVAL ('e' eaten as exa suffix, '5' trailing). `10M `,
  `10\t\n` -> ACCEPT (skip_spaces). `010K` -> 8192 (octal x suffix). No falsifying input found.

# Precision observations (not defects; no amendment required for correctness)

1. kstrtox.c proves case-insensitivity of the `0x` prefix only; suffix case-insensitivity rests on cmdline.c:160-187
   dual case labels. The row's quote-to-clause mapping already reflects this — a reader skimming the quote list could
   conflate the two `_tolower` uses.
2. Clause F's ULLONG_MAX cap also applies to unshifted parse overflow (kstrtox.c:86-88). The row's "shifted value"
   phrasing is true and sufficient for its triage purpose.

Smallest safe correction: none. GR1 survives the fresh attack on all ten clauses.
