ROW GR1 VERDICT: holds
SECTION SHA256: 3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1

# R50RevGR1c — claim C1, row GR1, counted reviewer verdict

Bytes under test: `git -C .../tsukuroi-shokunin show 8029cdba...:corpus/knowledge/btrfs-scrub-grounding-r45.md`,
extracted once to scratch `entry.md` (307 lines); GR1 = lines 14-55. Section hash confirmed two ways:
`tools/check-scrub-admission-r50.py --revision 8029cdba... --section-hash` printed
`"GR1": "3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1"` with `"problems": []` and
`"structural_ok": 1`, and an independent `hashlib.sha256` over the row's lines joined with LF reproduced the
same 64-hex value. Byte-convention note (not a defect): the tool's cut is lines 14..55 *including* the blank
separator line before `## GR2`, so the hashed string ends with LF; lines 14..54 without that blank line hash
`0b67bea0ed4960e3...` and do not match. The frozen value is reproduced, so the convention is consistent, only
the item's "no trailing LF" phrasing is loose.

Pinned sources verified before any reading: `sha256sum -c SHA256SUMS` is `OK` for all five files in
`.ufo/waves/round-45/frozen/src/` (cmdline.c, vsprintf.c, kstrtox.c, dev-replace.c, systemd.kill.xml) and all
five in `.ufo/waves/round-44/frozen/src/` (scrub.c, sysfs.c, ...). S-row mapping as the header states: S246 =
round-45 `lib/cmdline.c` (1af5ad98...), `lib/vsprintf.c` (cabb648a...), `lib/kstrtox.c` (0c52ae02...); S243 =
round-44 `sysfs.c` (ce146120...); S242 = round-44 `scrub.c` (f347931b...); S249 = round-45
`hostcap/capture.txt`, recomputed `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70`, equal to
the digest the row's front matter claims.

## Clause-by-clause

1. "`memparse` (SR8) calls `simple_strtoull` with base 0" — holds: `cmdline.c:156`
   `unsigned long long ret = simple_strtoull(ptr, &endptr, 0);`, inside `memparse` (`cmdline.c:153-200`).
2. "`simple_strtoull` resolves base 0 through `_parse_integer_fixup_radix`" — holds: `vsprintf.c:114`
   `return simple_strntoull(cp, endp, base, INT_MAX);` and `vsprintf.c:86`
   `cp = _parse_integer_fixup_radix(startp, &base);`. The quoted line sits in `simple_strntoull`, one call
   below `simple_strtoull`; the chain is real, so the citation supports the clause. Note only that the clause
   names the wrapper rather than the function holding line 86.
3. Radix rule — holds exactly: `kstrtox.c:29` `if (s[0] == '0') {`, `kstrtox.c:30`
   `if (_tolower(s[1]) == 'x' && isxdigit(s[2]))`, `kstrtox.c:31` `*base = 16;`, `kstrtox.c:33` `*base = 8;`,
   `kstrtox.c:35` `*base = 10;`, plus `kstrtox.c:37-38` skipping the `0x` pair only when base is 16. So hex
   requires `0x`/`0X` *and* a following hex digit; any other leading `0` is octal; else decimal. Every part of
   the sentence maps to a line.
4. Suffix set and single letter — holds: the `switch (*endptr)` at `cmdline.c:160-187` has cases `E/e P/p T/t
   G/g M/m K/k` only, and `cmdline.c:193` `endptr++;` advances exactly once, so at most one letter is consumed.
5. "10-bit shift per step, so `K` is 1024, not 1000" — holds: each case adds `shl += 10;` and falls through
   (`cmdline.c:163-183`), so `K` -> 10, `M` -> 20, ... `E` -> 60. `100M` = `100 << 20` = 104857600, as stated.
6. "suffix counts only when at least one digit came before it" — holds: `cmdline.c:189`
   `if (shl && likely(ptr != endptr)) {`. `endptr` can only advance past digits (plus the `0x` pair, which
   `kstrtox.c:30` admits only when a hex digit follows), so `ptr != endptr` is equivalent to "at least one digit".
   `M` alone leaves `endptr == ptr`, the suffix is not consumed, and the store rejects the residue.
7. "a shifted value that overflows becomes `ULLONG_MAX`" — holds as written at `cmdline.c:191-192`
   `if (unlikely(check_shl_overflow(ret, shl, &ret))) ret = ULLONG_MAX;`, reinforced by the comment at
   `cmdline.c:159` `/* Consume valid suffix even in case of overflow. */` (the `endptr++` at 193 is outside the
   overflow branch, so the suffix is still eaten on overflow, matching that comment).
8. "The sysfs store then skips whitespace and returns `-EINVAL` unless the text ends there" — holds:
   `sysfs.c:2040` `limit = memparse(buf, &endptr);`, `sysfs.c:2042` `endptr = skip_spaces(endptr);`,
   `sysfs.c:2043` `if (*endptr != 0)` `return -EINVAL;` (2044), else `WRITE_ONCE` and `return len` (2045-2046).
   The whitespace skip is real and is exactly what makes the trailing `'\n'` (and a bare newline) legal, which
   the row's own comment reference at `sysfs.c:2041` corroborates.
9. Worked examples — all four re-derived against the bytes, none contradicted:
   `100M`/`100m` -> 104857600 (clauses 4-5); `010` -> base 8 at `kstrtox.c:33`, value 8; `0x10` -> base 16,
   prefix skipped at `kstrtox.c:37-38`, value 16; `10MB` -> suffix `M` eaten at 193, `endptr` lands on `B`,
   `sysfs.c:2043` rejects; `10 M` -> `*endptr` is a space at `cmdline.c:160`, no suffix, `skip_spaces` walks to
   `M`, rejected at `sysfs.c:2043`; `-1` -> `_parse_integer_limit` (`kstrtox.c:65-75`) consumes nothing for a
   non-digit, `endptr == ptr`, no suffix, `skip_spaces` leaves `-`, rejected. A bare newline -> zero digits, so
   `memparse` returns 0 with `endptr` on `'\n'`, `skip_spaces` lands on NUL, accepted with `limit = 0`.
10. "0 means no limit (SR8)" — holds against the pinned scrub side: `scrub.c:1380`
    `bwlimit = READ_ONCE(device->scrub_speed_max);` then `scrub.c:1381-1382` `if (bwlimit == 0) return;`, i.e.
    the throttle is a no-op at 0. So "removes the limit" is grounded, not an overreach.
11. Host reading — holds, and the unexercised part is marked: `capture.txt:8` reads
    `... /devinfo/1/scrub_speed_max mode=644 owner=root value=0` and `capture.txt:1` reads
    `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000`. "no limit is set" follows from value=0
    plus clause 10. The write-denial is explicitly bracketed `[inference: by ordinary file-mode checks, which
    the capture does not exercise; ACLs and LSM rules are not captured]`, which is the correct treatment for a
    statement the capture does not decide. "Nothing was written to test the parse" is consistent with the
    capture's contents (read-only probe lines only) and with the entry's own scope sentence.

Universal words checked for overreach: "at most one" (clause 4), "only when" (clause 6), "unless" (clause 8),
"no limit" (clause 10), "in either case" (clause 4, both cases present in the switch). None exceeds the quoted
code. Citation forms: GR1 uses only single-line `file:line` citations (no ranges), so the "range running into
the next function" defect class is not reachable here; all 14 cited locations (cmdline.c 147/156/159/189/191/192,
vsprintf.c 86, kstrtox.c 29/30/33, sysfs.c 2040/2043, capture.txt 1/8) exist in the pinned bytes.

## Defects

None. No clause is contradicted, no citation resolves nowhere, and every Quote is exact text on its cited line
(verified by substring test on the cited line, 12/12 OK, transcript in
`.ufo/waves/round-50/w1/R50RevGR1c/receipts.txt`). No replacement text is proposed because nothing needs one.

## Verified but not re-derived

- `check_shl_overflow` is referenced at `cmdline.c:191` but its definition is not in any pinned snapshot (grep
  over the round-45 and round-44 snapshot `.c` files finds only the call site). Clause 7 therefore rests on the
  call site, the `ULLONG_MAX` assignment, and the identifier's meaning; I did not read `include/linux/overflow.h`.
  This is a residual dependency of the pinned tree, not a defect in the row, which cites only `cmdline.c`.
- `skip_spaces` and `isxdigit`/`_tolower` bodies are likewise outside the snapshots; I relied on their standard
  semantics and on `sysfs.c:2041`'s own comment naming the trailing `'\n'` as expected input.
- Host capture digest equality was recomputed; I did not re-run `capture.sh` (it probes live sysfs, and the item
  did not authorize running it).

## Not done

- Did not run the full `check-scrub-admission-r50.py` predicate (only the `--section-hash` mode the item names);
  `structural_ok: 1` and an empty `problems` list came from that run, but `quotes_ok`/`verdicts_ok`/`seats_ok`/
  `marks_ok`/`corr_ok` were not evaluated by me. I also did not read GR2/GR3 or the round-49 critic's four
  defects — the item scopes this seat to GR1, and the four-correction sentence belongs to GR2, not to this row.
- Did not test the parse on a live kernel; no sysfs write was attempted, by design and by the host guard.
- Scratch `/fast/scratch/hyaku/tsukuroi-r50/R50RevGR1c/` removed after receipts were copied out.
