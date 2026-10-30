ROW GR1 VERDICT: holds
SECTION SHA256: 98fa4e07768d240eaf5ea2cce13ce0623fdb756054e5df9f7b9fe68ab2e63987

Seat R52CritGR1a (critic, one of the 18 counted seats of round 52 wave w1), claim C1, row GR1 of
`corpus/knowledge/btrfs-scrub-grounding-r45.md` at revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0. I did
not write the row and am not its author. No admission mark is written by this report.

## Section hash (confirmed, and reproduced independently)

`python3 tools/check-scrub-admission-r52.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0
--section-hash --no-base-check` printed `"section_sha256": {"GR1": "98fa4e07768d240eaf5ea2cce13ce0623fdb756054e5df9f7b9fe68ab2e63987",
"GR2": "9fd581a0c9d02b02100b6a15648b7c6e4be896ac746ed09303a88dc8a24f0ec5", "GR3":
"0405f38a5783c49b6c078b118c9868543eb494b43f8b1c5e6c14284a123b9eac"}` with `"problems": []` and
`"structural_ok": 1` (receipt: `w1/R52CritGR1a/section-hash.json`). I recomputed it myself from the extracted
row (LF-join of the `## GR1` lines, no trailing LF): same digest, 4792 bytes, span = entry lines 14-102
(receipt: `w1/R52CritGR1a/final-check.txt`, last line). The hash is also unchanged since the round-51
amendment: `git rev-parse 6abef5d0:corpus/knowledge/btrfs-scrub-grounding-r45.md` and
`ff9470ea:corpus/knowledge/btrfs-scrub-grounding-r45.md` both print blob
`86d7e802a0e0d61c7f053fd92d3874cb18cefa4a`, i.e. the row bytes are the AMENDMENT-1 bytes as the claim says.

## Snapshot provenance: digests verified before reading, and the S-row mapping

`sha256sum -c SHA256SUMS` passes for all five files of `.ufo/waves/round-45/frozen/src/` (cmdline.c,
dev-replace.c, kstrtox.c, systemd.kill.xml, vsprintf.c — receipts `w1/R52CritGR1a/digests-r45.txt`) and all
five of `.ufo/waves/round-44/frozen/src/` (scrub.c, sysfs.c, btrfs-scrub@.timer, btrfs-scrub@.service,
PKGBUILD — receipt `digests-r44.txt`). File-to-S-row map, matching `corpus/SOURCES.md:251-257` and the
snapshots' own `FETCH.txt` (all three fetch `?h=v7.2.11`, tag object 8316c24ec1b7, peeled
a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea; the systemd file is tag v262, peeled
8cc40e0c5e9234bf45084751ac53b1fbfe70b492):

- **S246** = round-45 `src/cmdline.c` (1af5ad98…ca9d), `src/vsprintf.c` (cabb648a…469ca),
  `src/kstrtox.c` (0c52ae02…d1ee4) — Linux v7.2.11 `lib/`.
- **S243** = round-44 `src/sysfs.c` (ce146120…31c43) — Linux v7.2.11 `fs/btrfs/sysfs.c`.
- **S242** = round-44 `src/scrub.c` (f347931b…ca5b8) — Linux v7.2.11 `fs/btrfs/scrub.c`.
- **S249** = round-45 `hostcap/capture.txt` (f5958a83…1e70) — own-work; I re-hashed it and it matches.
- (not cited by GR1: **S247** = round-45 `src/dev-replace.c`; **S248** = round-45 `src/systemd.kill.xml`;
  **S244** = round-44 timer/service/PKGBUILD.)

GR1 cites only S246/S243/S242/S249 files.

## Mechanical lint (the tool named in the brief)

`python3 tools/lint-grounding-r51.py --revision ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0` →
`"verdict": "PASS"`, `"lint_ok": 3`, `"quotes_ok"`-relevant `"quote_bad": 0` over `"quotes": 99`
(GR1: 30 quotes, 0 bad), `"cites": 96`, `"cite_bad": 0` (GR1: 27 prose citations, 0 bad),
`"gaps_computed": 98`, `"gap_ok": 1`, `"gap_missing": []`, `"gap_extra": []`, `"gap_dups": []`,
`"pin_problems": []`, `"snapshot_problems": []`, `"rows_clean": 3` (receipt: `w1/R52CritGR1a/lint.json`).
`--emit-gaps` reproduces the entry's `### Range gaps (R51)` block byte-for-byte, including
`- S246 kstrtox.c: 70, 75, 77` and `- S242 scrub.c: 1400-1401`, which are exactly GR1's out-of-range
citations (receipt `gaps-emitted.txt`). The lint checks quote/line/gap mechanics only; it does not check that
a clause is true, so the clause work below is mine.

## Every clause checked against the pinned bytes

I read only the `## GR1` section (entry lines 14-102) of the frozen entry, plus the `### Range gaps (R51)`
block and the Limits section for context, as instructed. Clauses, in order:

1. "a write to `devinfo/<devid>/scrub_speed_max` is parsed by `memparse` (sysfs.c:2040)" — sysfs.c:2040 is
   `limit = memparse(buf, &endptr);` inside `btrfs_devinfo_scrub_speed_max_store` (sysfs.c:2031-2047), the
   attribute registered by `BTRFS_ATTR_RW(devid, scrub_speed_max, …)` at sysfs.c:2048-2049; the path form
   `devinfo/<devid>/scrub_speed_max` is confirmed by the host capture at capture.txt:8
   (`…/devinfo/1/scrub_speed_max`). Holds.
2. "calls `simple_strtoull` with base 0 (cmdline.c:156)" — cmdline.c:156 is
   `unsigned long long ret = simple_strtoull(ptr, &endptr, 0);` in `memparse` (cmdline.c:153-200). Holds.
3. "`simple_strtoull` passes the base to `simple_strntoull` (vsprintf.c:114)" — vsprintf.c:114 is
   `return simple_strntoull(cp, endp, base, INT_MAX);`. Holds.
4. "resolves base 0 through `_parse_integer_fixup_radix` (vsprintf.c:86)" — vsprintf.c:86 is
   `cp = _parse_integer_fixup_radix(startp, &base);`, and the resolved base is what vsprintf.c:89 hands to
   `_parse_integer_limit`. Holds.
5. "hexadecimal for a leading `0x` or `0X` followed by a hex digit (kstrtox.c:30-31)" — kstrtox.c:30-31 are
   `if (_tolower(s[1]) == 'x' && isxdigit(s[2]))` / `*base = 16;`, inside `if (s[0] == '0') {` at
   kstrtox.c:29 (quoted by the row). `_tolower` is what makes `0X` work; `isxdigit(s[2])` is the "followed by
   a hex digit" qualifier. Holds.
6. "octal for any other leading `0` (kstrtox.c:33)" — kstrtox.c:33 `*base = 8;` is the `else` of the hex
   test inside the leading-zero branch, i.e. every leading `0` that is not `0x`+hex-digit. Holds.
7. "decimal otherwise (kstrtox.c:35)" — kstrtox.c:35 `*base = 10;` is the `else` of `if (s[0] == '0')`.
   Holds.
8. "the `0x` prefix is then skipped (kstrtox.c:37-38)" — kstrtox.c:37-38 are
   `if (*base == 16 && s[0] == '0' && _tolower(s[1]) == 'x')` / `s += 2;`. The `*base == 16` guard is visible
   in the row's own quote, so the skip is scoped to the hexadecimal case the clause is attached to. Holds.
9. "The digit scan stops at the first character that is not a digit of that base (kstrtox.c:70, kstrtox.c:75,
   kstrtox.c:77)" — kstrtox.c:70 `if ('0' <= c && c <= '9')`, :75 `break;` (the non-alphanumeric break),
   :77 `if (val >= base)` (the per-base bound; the `break;` it guards is kstrtox.c:78, inside the same
   three-line construct the row cites). True of the pinned code for every base the row names: base 8 rejects
   `8`/`9` (val ≥ 8), base 10 rejects `a`..`f` (val ≥ 10), base 16 accepts `a`..`f` (val 10-15 < 16, via
   kstrtox.c:72-73, and uppercase via the `_tolower(c)` at kstrtox.c:67). The row quotes `isxdigit(s[2])` at
   kstrtox.c:30, so its base-16 letter set is evidenced; see non-blocking note N1 for the one branch the row
   does not point at.
10. "the end pointer is advanced over the digits it took (vsprintf.c:91)" — vsprintf.c:91 is
    `cp += (rv & ~KSTRTOX_OVERFLOW);`, which advances by the consumed-digit count with the overflow bit
    masked out. Holds.
11. "so a leading `-` consumes nothing" — for `-1` the digit scan breaks at kstrtox.c:75 on the first
    character, so `rv == 0` and vsprintf.c:91 advances the end pointer by zero; the `-` is left in the
    buffer, which is why the value is later rejected. Holds.
12. "`memparse` takes at most one suffix letter (cmdline.c:193)" — cmdline.c:193 is `endptr++;`, a
    single-character advance, and the selector at cmdline.c:160 is `switch (*endptr)`, one character, so at
    most one letter can ever match. Holds.
13. "`K`, `M`, `G`, `T`, `P` or `E` in either case (cmdline.c:161-184)" — the range covers exactly the six
    case pairs `E/e`(161-162) `P/p`(165-166) `T/t`(169-170) `G/g`(173-174) `M/m`(177-178) `K/k`(181-182)
    and their shifts; it does not run into the next function (`memparse` ends at cmdline.c:200). Holds.
14. "each arm adding a 10-bit shift and falling through to the arms below it (cmdline.c:183 is the `K`
    arm's shift), so `K` is 1024, not 1000" — cmdline.c:183 is `shl += 10;` inside `case 'K': case 'k':`
    (181-183); every arm has its own `shl += 10;` and a `fallthrough;` to the arms below it, so `K` gets
    10 bits (2^10 = 1024) while `M` gets 20 bits (2^20) and `E` 60 bits (2^60). Holds.
15. "the suffix counts only when at least one digit came before it (cmdline.c:189)" — cmdline.c:189 is
    `if (shl && likely(ptr != endptr)) {`. I checked the equivalence the clause asserts: in the base-0 path
    `endptr` can advance past the `0x` prefix only when kstrtox.c:30-31 already found a hex digit at
    `s[2]`, and that digit is then consumed by the scan, so `ptr != endptr` ⟺ at least one digit of the
    chosen base was consumed. Holds.
16. "a shifted value that overflows becomes `ULLONG_MAX` (cmdline.c:191-192)" — cmdline.c:191-192 are
    `if (unlikely(check_shl_overflow(ret, shl, &ret)))` / `ret = ULLONG_MAX;`. The consequence is pinned;
    the antecedent is the named helper (see "verified but not re-derived"). Holds.
17. "The sysfs store then calls `skip_spaces` (sysfs.c:2042) … and returns `-EINVAL` (sysfs.c:2044) unless
    the text ends there (sysfs.c:2043)" — sysfs.c:2042 `endptr = skip_spaces(endptr);`, :2043
    `if (*endptr != 0)`, :2044 `return -EINVAL;`. The `[inference: skip_spaces is defined outside the pinned
    files …]` mark is correctly placed and correctly scoped: I grepped both snapshot `src/` directories and
    `skip_spaces` occurs only as a call site (cmdline.c:283, vsprintf.c:3479/3480/3569/3659); no definition
    is pinned. The store's own comment at sysfs.c:2041 ("There could be trailing '\n' …") corroborates the
    newline case. Holds.
18. The examples: "`100M` and `100m` both set the value 104857600 (100 times 2^20), `010` sets 8 and
    `0x10` sets 16; `10MB` (a second letter), `10 M` (a blank before the suffix) and `-1` are rejected with
    `EINVAL`". I did not eyeball these: I compiled the pinned function bodies (`kstrtox.c:26-40` and
    `57-95`, `vsprintf.c:78-101` and `111-115`, `cmdline.c:153-200`) verbatim into a harness
    (`w1/R52CritGR1a/harness.c`) with `check_shl_overflow`/`check_mul_overflow`/`check_add_overflow` mapped
    to the compiler builtins, and ran the store with `skip_spaces` modelled both ways (isspace-wide and
    newline-only). Observed (receipt `w1/R52CritGR1a/harness-run.txt`): `100M`→104857600, `100m`→104857600,
    `010`→8, `0x10`→16, `10MB`→EINVAL (endptr left on `B`), `10 M`→EINVAL, `-1`→EINVAL, `"\n"`→0 accepted,
    under both `skip_spaces` models. Extra probes behaved consistently with the row: `0X10`→16, `0x1f`→31,
    `1K`→1024, `1M`→1048576, `10G`→10737418240, `1E`→2^60, `99999999999999999999999K`→ULLONG_MAX, `0x`→EINVAL,
    `0K`→0 accepted, `K`→EINVAL, `M`→EINVAL, `08`→EINVAL. All eight of the row's examples reproduce; none is
    contradicted.
19. "a write of a bare newline parses as 0 and is accepted [inference: that the sysfs write buffer is
    NUL-terminated after the newline …]" — the parse gives 0 (scan breaks at the newline, `rv == 0`), and
    acceptance needs `*endptr == 0` at sysfs.c:2043, which is exactly the assumption the mark names. Marked
    honestly and in the right place. Holds.
20. "which removes the limit: the throttle returns at once when the limit is 0 (scrub.c:1381-1382)" —
    scrub.c:1381 `if (bwlimit == 0)` / :1382 `return;`, in `scrub_throttle_dev_io` (scrub.c:1371-1420). The
    row's identity of "the limit" with the sysfs attribute is not merely asserted: the row's own quote of
    scrub.c:1369 reads "Limit can be set via /sys/fs/UUID/devinfo/devid/scrub_speed_max." Holds.
21. "The limit is a bandwidth limit over a one-second timeslice (scrub.c:1368-1369) [inference: the unit is
    bytes per second …]" — the cited lines are the upstream comment, quoted whole; the unit is marked as an
    inference with its reason (scrub.c:1400-1401 compares a byte count, `bio_size`, with it) and it says
    plainly that those lines are outside the declared range and not quoted — and indeed the entry's gap
    block enumerates `S242 scrub.c: 1400-1401`, so the disclosure is consistent. The aggregate rate does work
    out to bytes per second (`div` at scrub.c:1388, window `time_slice/div` ms at scrub.c:1374/1393, and
    `throttle_sent <= div_u64(bwlimit, div)` at scrub.c:1401). Holds; see non-blocking note N3.
22. Host reading — capture.txt:9 `devinfo … devids=1` (one device, devid 1), capture.txt:8
    `…/devinfo/1/scrub_speed_max mode=644 owner=root value=0`, capture.txt:1
    `uid=1000 CapEff=0000000000000000` (uid 1000, no effective capabilities): all three lines say exactly
    what the row says. "under the quoted code no limit is set" follows from value 0 plus scrub.c:1381-1382,
    and the kernel-identity step is marked `[inference: … carried from the Limits section]`. "this caller …
    cannot write one" is marked `[inference: by ordinary file-mode checks, which the capture does not
    exercise; ACLs and LSM rules are not captured]` — correct scope. "Nothing was written to test the parse"
    is true: I wrote nothing to any attribute. Holds.
23. Universals audit ("first", "only", "any", "always"): "at most one suffix letter" (single-char switch +
    single `endptr++`), "only when at least one digit came before it" (shown in clause 15),
    "hexadecimal for a leading `0x` or `0X` followed by a hex digit" (exactly the kstrtox.c:29-31
    condition), "octal for any other leading `0`" (exactly the else at kstrtox.c:32-33), "decimal otherwise"
    (kstrtox.c:34-35), "the digit scan stops at the first character that is not a digit of that base"
    (checked per base above), "a leading `-` consumes nothing" (clause 11). No universal overreaches.
24. Range check: no cited range runs into the next function — cmdline.c:161-184 sits inside `memparse`
    (153-200), kstrtox.c:30-31 and :37-38 inside `_parse_integer_fixup_radix` (26-40), kstrtox.c:70/75/77
    inside `_parse_integer_limit` (58-95), vsprintf.c:86/:91 inside `simple_strntoull` (79-101),
    vsprintf.c:114 inside `simple_strtoull` (112-115), sysfs.c:2040/:2042/:2043/:2044 inside
    `btrfs_devinfo_scrub_speed_max_store` (2031-2047), scrub.c:1368-1369/:1381-1382/:1400-1401 inside
    `scrub_throttle_dev_io` (1371-1420).

### Quotes

All 30 `**Quote.**` lines were checked against the pinned bytes by whole-line comparison (receipt
`w1/R52CritGR1a/final-check.txt` and `verify-citations.txt`): 30/30 match the cited line, 0 bad. Two are
whitespace-normalised rather than byte-identical — cmdline.c:147 (file ` *\tpotentially suffixed with K, M,
G, T, P, E.` vs the row's `* potentially suffixed with K, M, G, T, P, E.`) and scrub.c:1369 (file has two
spaces after `second.`, the row has one). Both keep the comment leader `* ` (the round-51 Limits section
records exactly that fix) and both are equal under the lane's whitespace normalisation, which is what
`lint-grounding-r51.py` applies and what QUALITY 94 (R50-PROVENANCE-COVERAGE) requires ("complete cited line
text, including a comment leader such as `* `"). Not a defect.

### Why this is `holds` and not `partly`

No clause is contradicted by the pinned bytes; no citation dangles or points at the wrong line; no quote
differs from its cited line; no `[inference]` mark is misplaced or missing (the three inferences — the
`skip_spaces` body, the NUL-terminated write buffer, the bytes-per-second unit — are exactly the three things
the pinned bytes do not decide, and the row marks the fourth, kernel-identity step too). The eight worked
examples reproduce exactly from a harness built out of the pinned bytes. The defects I can still name are
citation-completeness tightenings and scope notes, listed below; none of them makes a stated clause false, so
none of them is a defect that would force `partly`.

## Non-blocking notes (not defects; each with exact proposed text for the L1 if it wants it)

**N1 — the base-16 letter branch is not pointed at.** The digit-scan clause cites kstrtox.c:70, :75, :77 but
not the branch that admits `a`–`f` as base-16 digits, kstrtox.c:72-73
(`else if ('a' <= lc && lc <= 'f')` / `val = lc - 'a' + 10;`), and kstrtox.c:67 (`unsigned int lc =
_tolower(c);`) is what makes `A`–`F` work. The clause is TRUE of the pinned code, and the base-16 letter set
is already evidenced by the row's quote of `isxdigit(s[2])` at kstrtox.c:30; the deciding branch is two
lines below the cited kstrtox.c:70, in the same function. I therefore judge this a tightening, not a defect.
Optional replacement for the clause's citation parenthetical — "(kstrtox.c:70, kstrtox.c:72-73,
kstrtox.c:75, kstrtox.c:77)" — with two added quote lines
`**Quote.** `S246` kstrtox.c:72: "else if ('a' <= lc && lc <= 'f')"` and
`**Quote.** `S246` kstrtox.c:73: "val = lc - 'a' + 10;"`, and the gap block line regenerated (it would become
`- S246 kstrtox.c: 70, 72-73, 75, 77`, because S246's declared kstrtox.c range is 26-40 per
`corpus/SOURCES.md:255`).

**N2 — the assignment line for "set the value" is not cited.** "…both set the value 104857600" and "…which
removes the limit" both depend on the store writing the parsed value into the device field,
sysfs.c:2045 `WRITE_ONCE(device->scrub_speed_max, limit);`, which the row does not cite (it cites 2040 and
2042-2044). The identity of that field with the throttle's limit is carried by the row's quote of
scrub.c:1369, so the sentence is not unsupported; the line itself is merely unpointed-at. Optional
tightening: append "(sysfs.c:2045)" to the sentence "So `100M` and `100m` both set the value 104857600 …" and
add `**Quote.** `S243` sysfs.c:2045: "WRITE_ONCE(device->scrub_speed_max, limit);"`. sysfs.c:2045 is inside
S243's declared range 2021-2049, so the gap block would not change.

**N3 — "over a one-second timeslice" is the comment's framing.** The clause is sourced to the upstream
comment at scrub.c:1368-1369 ("bandwidth-limit based, the timeslice is 1 second"), quoted whole, and the
code agrees in aggregate (`time_slice = 1000` ms at scrub.c:1374; the window is `time_slice/div` ms at
scrub.c:1393 with `div = clamp(bwlimit / (16 * 1024 * 1024), 1, 64)` at scrub.c:1388, and the per-window
allowance `throttle_sent <= div_u64(bwlimit, div)` at scrub.c:1401), so the effective rate is bytes per
second. If the L1 wants the row to speak about code rather than comment, the precise replacement for the
sentence is: "The limit is a bandwidth limit over a one-second timeslice, divided by the code into windows of
`time_slice/div` milliseconds (scrub.c:1374, scrub.c:1388, scrub.c:1393), so the aggregate rate is the limit
in bytes per second [inference: the unit is bytes per second; scrub.c:1400-1401 compares a byte count,
`bio_size`, with it, outside the declared range and not quoted]." Note that scrub.c:1374/1388/1393 are inside
S242's declared range 1365-1385 except 1388 and 1393, which are outside it and would have to enter the gap
block.

**N4 — device-count scope (already litigated in rounds 49-51; unchanged, so not a new finding).** "The
host's one btrfs device (devid 1, capture.txt:9)" rests on capture.sh:23-30, which enumerates
`/sys/fs/btrfs/*/devinfo/*/scrub_speed_max` and `/sys/fs/btrfs/*/devinfo` — i.e. mounted btrfs filesystems
only; a device of an unmounted btrfs filesystem has no `scrub_speed_max` attribute and cannot appear. Within
the row's own domain (devices exposing the attribute) the enumeration is exhaustive, which is why the
round-50 seat treated it as a residual nit rather than a defect. Optional tightening if the L1 wants the
narrower wording: "The host's one btrfs device visible in `/sys/fs/btrfs` (devid 1, capture.txt:9)".

**N5 — the kernel-identity inference points at a Limits bullet that covers `fs/` but not `lib/` this round.**
GR1's `[inference: … carried from the Limits section]` refers to the Limits bullet "the Arch
7.2.11-arch1-1 patch touches no file under `fs/` or `lib/` [inference carried from round 43 for `fs/`; `lib/`
not re-checked this round]". The host sentence this inference supports ("under the quoted code no limit is
set") needs only the `fs/btrfs/` half (scrub.c:1381-1382, sysfs.c), which round 43 covered, so the inference
holds for what it is used for; but "this upstream code unchanged" read literally also covers the `lib/`
parse chain, whose patch status was not re-checked this round. Optional tightening: "under the quoted code no
limit is set [inference: that the Arch 7.2.11-arch1-1 kernel carries this upstream code unchanged is carried
from the Limits section, whose `lib/` half was not re-checked this round]".

## Verified but not re-derived (not defects)

- `check_shl_overflow`'s body (include/linux/overflow.h) is not in any pinned snapshot; I took the overflow
  predicate from its name and from the pinned consequence at cmdline.c:191-192, which the row states as
  "a shifted value that overflows becomes `ULLONG_MAX`" — the consequence is pinned, the antecedent is the
  named helper.
- `skip_spaces`'s body (lib/ctype.c / lib/string_helpers.c) is not pinned; the row marks this and its
  consequences. I showed the row's conclusions are insensitive to it: the harness produces the same eight
  example results with an isspace-wide skip and with a newline-only skip.
- `isxdigit`/`_tolower` semantics (lib/ctype.c) are not pinned; the row's "hex digit" and "0X" wording is
  carried by the quoted `isxdigit(s[2])` at kstrtox.c:30 and the quoted `_tolower(s[1]) == 'x'` at
  kstrtox.c:30.
- `btrfs_stripe_nr_to_offset` (scrub.c, the origin of the `bio_size` argument at scrub.c:1942-1943) is
  outside the declared ranges and uncited by the row; it is the thing the row's bytes-per-second inference
  rests on, and the row marks that unit as an inference.
- The Arch 7.2.11-arch1-1 patch list and the "host carries upstream code unchanged" premise are not pinned by
  any snapshot; the row marks the step as an inference (see N5).
- I did not re-fetch from git.kernel.org or github.com; the pinned digests and the snapshots' FETCH.txt were
  verified instead.

## What I did not do

- I did not run the full C1 counter predicate (`structural_ok == 1 and lint_ok == 3 and quotes_ok == 3 and
  verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3`): `verdicts_ok` needs the 18-seat wave results and
  `marks_ok` needs the L1's admission marks, neither of which exists yet. I ran only `--section-hash`.
- I did not judge GR2 or GR3 beyond noting their shared context; my seat's row is GR1.
- I did not write to any host sysfs attribute, start/stop/enable any unit, or run any scrub or replace; the
  host claim rests on the pinned capture.txt only, which I re-hashed (f5958a83…1e70).
- I did not run the capture script on this host (read-only seat, and the capture is a pinned artifact).
- I did not edit, add, delete, stage, commit or otherwise touch any tracked lane file, the lane's git index,
  any sibling lane, the fleet repo, or any operator config. Writes were confined to
  `.ufo/waves/round-52/w1/R52CritGR1a.md` (this report) and `.ufo/waves/round-52/w1/R52CritGR1a/`
  (receipts: digests-r44.txt, digests-r45.txt, entry-extracted.md, final-check.txt, gaps-emitted.txt,
  harness-run.txt, harness.c, lint.json, receipt-sha256.txt, section-hash.json, verify-citations.txt); the
  scratch tree /fast/scratch/hyaku/tsukuroi-r52/R52CritGR1a was removed afterwards.
- I wrote no admission mark and no gate status.
- No tool was installed or upgraded for this seat (no pacman, uv, npx or binary fetch; the Python 3
  interpreter and gcc already present were used).
