ROW GR1 VERDICT: holds
SECTION SHA256: 3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1

HASH CONVENTION (recomputed independently, not taken from the counter). Entry extracted with
`git -C <lane> show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:corpus/knowledge/btrfs-scrub-grounding-r45.md`
(287 lines). The GR1 section is entry.md:14 (`## GR1`) through entry.md:55, the blank line before `## GR2`
at entry.md:56 — 42 lines. Joining those 42 lines with LF and no trailing LF gives
3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1, exactly the value
`tools/check-scrub-admission-r49.py --revision 55c07cd3... --section-hash` printed (its JSON also reported
`"problems": []`, `structural_ok: 1`, and GR1/GR2/GR3 = 3a2ba180…/d4296085…/43430a14…). With a trailing LF the
digest would be 83f0cf47b109bf7605b1250c9860fbdd5a2dd6237837ea2a1f3708d61eb5314c, which does not match: the
tool's convention is therefore lines-to-blank-line-before-next-heading, joined with LF, no trailing LF, and my
independent recomputation agrees with the frozen claim.

SNAPSHOT MAPPING AND INTEGRITY. S246 = `.ufo/waves/round-45/frozen/src/{cmdline.c,vsprintf.c,kstrtox.c}`;
S247 = that directory's `dev-replace.c` (not used by GR1); S243 = `.ufo/waves/round-44/frozen/src/sysfs.c`;
S242 = that directory's `scrub.c`, used only for the "0 means no limit" clause. Provenance is recorded in
`.ufo/waves/round-45/frozen/src/FETCH.txt` (plain URLs at tag v7.2.11 for cmdline.c, dev-replace.c, kstrtox.c,
vsprintf.c; systemd.kill.xml at v262; peeled tag commits a2de78ee… / 8cc40e0c…). `sha256sum -c SHA256SUMS`
returned rc=0 for all five files in each snapshot directory (receipt `w1/R49RevGR1b/digests-round45.txt`).
So the bytes I read are the digest-verified pinned bytes.

CLAUSE-BY-CLAUSE (every citation re-read at its number in the pinned file).

1. memparse is the parser of that attribute. S243 sysfs.c:2040 is `limit = memparse(buf, &endptr);`, inside
   `btrfs_devinfo_scrub_speed_max_store` (sysfs.c:2031–2047), registered by `BTRFS_ATTR_RW(devid,
   scrub_speed_max, …)` at sysfs.c:2048. Quote exact; no range runs into a neighbouring function.
2. base 0. S246 cmdline.c:156 `unsigned long long ret = simple_strtoull(ptr, &endptr, 0);` — exact, third
   argument 0.
3. base-0 resolution reaches `_parse_integer_fixup_radix`. S246 vsprintf.c:86
   `cp = _parse_integer_fixup_radix(startp, &base);` sits in `simple_strntoull` (vsprintf.c:78–101), and
   `simple_strtoull` delegates: vsprintf.c:112–115 `return simple_strntoull(cp, endp, base, INT_MAX);`.
   The clause names `simple_strtoull`, and the chain is pinned end to end.
4. Radix selection. S246 kstrtox.c:28 `if (*base == 0) {`; :29 `if (s[0] == '0') {`; :30
   `if (_tolower(s[1]) == 'x' && isxdigit(s[2]))`; :31 `*base = 16;`; :33 `*base = 8;`; :35 `*base = 10;`.
   `_tolower` makes the `0X` spelling work, and `isxdigit(s[2])` is exactly the "followed by a hex digit"
   condition. The prefix is then skipped at kstrtox.c:37–38 (`if (*base == 16 && s[0] == '0' &&
   _tolower(s[1]) == 'x') s += 2;`), which is what makes the row's `0x10` = 16 arithmetic right.
5. At most one suffix letter, either case. S246 cmdline.c:160 `switch (*endptr) {` with paired cases at
   :161/:162 (E/e), :165/:166 (P/p), :169/:170 (T/t), :173/:174 (G/g), :177/:178 (M/m), :181/:182 (K/k), and a
   single advance `endptr++;` at :193. Nothing loops, so a second letter survives and is caught later.
6. 1024 per step, not 1000. cmdline.c:163, :167, :171, :175, :179, :183 each `shl += 10;` under `fallthrough;`
   (:164, :168, :172, :176, :180, :184), so E→60, P→50, T→40, G→30, M→20, K→10 — i.e. K = 2^10 = 1024 and
   100M = 100·2^20 = 104857600, exactly the row's number.
7. "the suffix counts only when at least one digit came before it". cmdline.c:189
   `if (shl && likely(ptr != endptr)) {`. The literal test is pointer advance; it is equivalent to "≥1 digit"
   for every reachable input because `_parse_integer_limit` consumes nothing when the first character is not a
   digit (kstrtox.c:65–75: the loop `break`s at :75 and returns `rv` = 0 at :94), and the only zero-digit
   advance in `_parse_integer_fixup_radix` (kstrtox.c:37–38) is gated on base 16, which itself required
   `isxdigit(s[2])` at :30 — a digit is therefore always consumed there, and `simple_strtoull` passes
   max_chars = INT_MAX (vsprintf.c:114), so the kstrtox.c:88 `prefix_chars < max_chars` guard cannot cut it off.
   I checked "0x" alone, "M" alone, "0xZ": none advance past a digit, and all fall through to the sysfs EINVAL
   path. Clause holds; the paraphrase is exact in effect.
8. Overflow → ULLONG_MAX. cmdline.c:191 `if (unlikely(check_shl_overflow(ret, shl, &ret)))` then :192
   `ret = ULLONG_MAX;`. Branch and assignment pinned.
9. sysfs whitespace-and-end test. S243 sysfs.c:2042 `endptr = skip_spaces(endptr);`, :2043
   `if (*endptr != 0)`, :2044 `return -EINVAL;`, with the intent comment at :2041 "There could be trailing
   '\n', also catch any typos after the value." This decides both the "skips whitespace" half and the
   acceptance of a trailing newline.
10. The five worked examples, traced by hand through those lines: `100M`/`100m` (cmdline.c:179/:183) →
    104857600; `010` → base 8 (kstrtox.c:33) with digits 0,1,0 (kstrtox.c:70–71, base check :77) = 8;
    `0x10` → kstrtox.c:30 sets base 16 and :37–38 skips the prefix, "10"₁₆ = 16; `10MB` → after the single
    `endptr++` (cmdline.c:193) `endptr` points at `B`, so sysfs.c:2043 rejects; `10 M` → the switch reads `' '`
    (cmdline.c:160, `default:` :185–186) leaving shl = 0 and endptr on the blank, `skip_spaces` then lands on
    `M`, sysfs.c:2043 rejects; `-1` → `_parse_integer_limit` has no sign branch (kstrtox.c:70–78) so rv = 0 and
    `endptr == ptr`, `skip_spaces` leaves `-`, sysfs.c:2043 rejects. No clause of the statement is contradicted.
11. Bare newline accepted as 0 and meaning "no limit". The same path: rv = 0, shl = 0, `skip_spaces` consumes
    `\n`, `*endptr == 0` so sysfs.c:2045 `WRITE_ONCE(device->scrub_speed_max, limit)` stores 0. "0 means no
    limit" is pinned in S242 scrub.c:1380–1382: `bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit == 0)
    return;` — the throttle returns before any accounting, i.e. no limit.
12. The unit "bytes per second" is also grounded: S242 scrub.c:1368–1369 comment "bandwidth-limit based, the
    timeslice is 1 second"; per-interval budget scrub.c:1401 `sctx->throttle_sent <= div_u64(bwlimit, div)` with
    `div = clamp(bwlimit / (16 * 1024 * 1024), 1, 64)` at :1388 and the interval `time_slice / div` ms at :1393.
    For 104857600 div = 6, so 6 intervals/s × (104857600/6) B = 104857600 B/s: bytes per second, not per tick.
13. Host reading. capture.txt:1 `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000` (no effective
    capabilities) and capture.txt:8 `scrub_speed_max 1d02a454-…/devinfo/1/scrub_speed_max mode=644 owner=root
    value=0` (devid 1; capture.txt:9 `devids=1` shows it is the only device). The one step the capture does not
    decide — that uid 1000 cannot write a root-owned 644 file — is explicitly marked at entry.md:53 as
    `[inference: by ordinary file-mode checks, … ACLs and LSM rules are not captured]`, and the row also states
    at entry.md:54 that nothing was written to test the parse. Marking is correct and no unmarked host reading
    remains.

UNIVERSAL-WORD AUDIT. The row's absolutest words each survive the code: "takes at most one suffix letter"
(one `endptr++`, cmdline.c:193), "the suffix counts only when at least one digit came before it" (equivalent to
cmdline.c:189 for all reachable inputs, shown in item 7), "0 means no limit" (scrub.c:1381–1382 is an
unconditional early return). "octal for any other leading `0`" is exact because kstrtox.c:29–33 has no other
escape; e.g. `08` stops at `8` (kstrtox.c:77) and is then rejected by sysfs.c:2043, which the row does not
claim otherwise.

VERIFIED BUT NOT RE-DERIVED. (a) `check_shl_overflow` appears only at its call site cmdline.c:191; its body is
in include/linux/overflow.h, which is not in either pinned snapshot, so the phrase "a shifted value that
overflows becomes ULLONG_MAX" rests on cmdline.c:191–192 plus the helper's name. The row does not assert the
helper's internals, so no clause turns on it. Likewise `_tolower`/`isxdigit` (linux/ctype.h, included at
cmdline.c:15) and `skip_spaces` (linux/string.h) definitions are not pinned; both uses are standard and the row
does not characterise their internals. (b) I did not re-fetch the FETCH.txt URLs or diff the snapshots against
git.kernel.org; I only confirmed each snapshot file matches its recorded SHA256SUMS line. (c) I did not
execute the row's examples against a kernel — every example result above is a hand trace through the cited
lines; no sysfs write, scrub, ioctl or unit operation was performed. (d) I did not run the full C1 predicate
(the item scoped me to `--section-hash`); `structural_ok: 1` and `"problems": []` were observed in that run's
JSON, not re-tested. (e) I did not review GR2/GR3 (separate seats); the GR2 guidance in my item was not in my
row's scope. Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49RevGR1b/` removed; receipts under
`w1/R49RevGR1b/`. No defect found in GR1, so no replacement text is proposed.
