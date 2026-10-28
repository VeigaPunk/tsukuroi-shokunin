VERDICT: defect-found
SECTION SHA256: 8eff963765feccd759ac62e601776c8cc9ae07352b43d50c9e4d81e6b5178660

Seat R51W1PreCritGR1a (critic, uncounted pre-read, claim C1, row GR1 of corpus/knowledge/btrfs-scrub-grounding-r45.md at 2732ee6c06108c031c4d8043239b994e0504eb2f).

## Bottom line

No clause of GR1 is contradicted by the pinned bytes. Every defect below is one of three kinds: (a) a clause whose only support is an unadmitted row, (b) a clause whose cited lines do not contain its support (or no line is cited), (c) a pinned-code inference that is not marked. Each replacement is given as exact wording; each new `Quote` line is checked by the lint, and each new prose `file:line` in GR1 must also be checked against the gap block (see "Lint coupling").

## Checks run (what I did)

- Extracted the frozen entry: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/knowledge/btrfs-scrub-grounding-r45.md` (348 lines, 24976 bytes; scratch copy, receipt copied to `.ufo/waves/round-51/w1/R51W1PreCritGR1a/entry-2732ee6c.md`).
- Section hash: `check-scrub-admission-r51.py --revision 2732ee6c… --section-hash --no-base-check` printed `"GR1": "8eff963765feccd759ac62e601776c8cc9ae07352b43d50c9e4d81e6b5178660"` (structural_ok 1, problems []). Matches the item.
- Source digests (`sha256sum -c SHA256SUMS`), mapping S-row to file:
  - S246 (round-45 snapshot, Linux v7.2.11 lib/): `cmdline.c` 1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d OK, `vsprintf.c` cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca OK, `kstrtox.c` 0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4 OK (`round-45/frozen/src/SHA256SUMS`; FETCH.txt: lib/cmdline.c, lib/kstrtox.c, lib/vsprintf.c at tag v7.2.11).
  - S243 (round-44 snapshot): `sysfs.c` ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43 OK (`round-44/frozen/src/SHA256SUMS`; FETCH.txt: fs/btrfs/sysfs.c at v7.2.11).
  - S242 (round-44 snapshot): `scrub.c` f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8 OK (`round-44/frozen/src/SHA256SUMS` lists scrub.c; FETCH.txt: fs/btrfs/scrub.c at v7.2.11; the lint's SNAPSHOTS table has the same digest).
  - S249 (own-work): `hostcap/capture.txt` f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70 matches SOURCES.md S249 and the lint table.
- Lint: `lint-grounding-r51.py --revision 2732ee6c…` → verdict PASS, lint_ok 3, quotes 63 / quote_bad 0, cites 28 / cite_bad 0, gaps_computed 62, gap_ok 1. GR1 alone: quotes 12, cites 2, problems []. The lint does NOT check clause truth or support (its own docstring says so).
- Opened every cited line (cmdline.c:147,156,159,189,191,192; vsprintf.c:86; kstrtox.c:29,30,33; sysfs.c:2040,2043) and every uncited line the clauses depend on (cmdline.c:161-194; vsprintf.c:79-115; kstrtox.c:26-75; sysfs.c:2021-2049; scrub.c:1365-1402; capture.txt:1-9).
- Declared ranges (corpus/SOURCES.md rows S242, S243, S246): S242 scrub.c 1365-1385, 3140-3162, 3215-3226, 3321-3337; S243 sysfs.c 72-74, 2021-2049, 2113; S246 cmdline.c 142-201, vsprintf.c 79-115, kstrtox.c 26-40.
- No command wrote to the fleet, the lane, or any tracked file. No tool was installed.

## Defects

### D1 — "(SR8)" is an unadmitted row, and "0 means no limit" is cited to it
Entry words: "is parsed by `memparse` (SR8), which" (Statement) and "which removes the limit (0 means no limit, SR8)."
- SR8 is not a source row. It is a row of `corpus/knowledge/btrfs-scrub-record-r44.md:56` (`## SR8`), and the README states it is pending: `corpus/README.md:479` "SR7, SR8 and SR9 are pending, not admitted."
- The clause itself is true on the pinned bytes, but its support is at `.ufo/waves/round-44/frozen/src/scrub.c:1380-1382`: `bwlimit = READ_ONCE(device->scrub_speed_max);` / `if (bwlimit == 0)` / `return;`. Those lines are inside S242's declared range 1365-1385. GR1 quotes none of them.
- Replacement (1): delete " (SR8)" from the Statement, so it reads "is parsed by `memparse`, which".
- Replacement (2): "...which removes the limit (0 means no limit: the throttle returns at once when the limit is 0, the two S242 quotes below)." Add two Quote lines after the existing S243 quotes:
  `**Quote.** `S242` scrub.c:1381: "if (bwlimit == 0)"`
  `**Quote.** `S242` scrub.c:1382: "return;"`
- Lint coupling: a prose `scrub.c:` cite inside GR1 is silently skipped (lint-grounding-r51.py:238-240, PROSE['GR1'] has no scrub.c). The two Quote lines above are the form the lint does check; they are in SNAPSHOTS and in S242's declared 1365-1385, so no gap line is added.

### D2 — "at most one suffix letter ... in either case ... each step ... 10-bit shift" is not supported by any cited line
Entry words: "After the digits, `memparse` takes at most one suffix letter, `K`, `M`, `G`, `T`, `P` or `E` in either case, each step multiplying by a further 1024 (a 10-bit shift per step, so `K` is 1024, not 1000)."
- The only cited line in that sentence is cmdline.c:147, the doc comment, which lists uppercase letters only ("potentially suffixed with K, M, G, T, P, E.") and says nothing about "either case", "one letter" or the 10-bit shift.
- The support is at `cmdline.c:177-183`: `case 'M':` / `case 'm':` / `shl += 10;` / `case 'K':` / `case 'k':` / `shl += 10;` with `fallthrough;` between arms (cmdline.c:161-185), and at most one letter because the only pointer advance is `endptr++;` (cmdline.c:193).
- Replacement: "After the digits, `memparse` takes at most one suffix letter (`endptr++;`, cmdline.c:193), `K`, `M`, `G`, `T`, `P` or `E` in either case (`case 'm':`, cmdline.c:178), and each arm adds one 10-bit shift and falls through to the arms below it (`shl += 10;`, cmdline.c:179, :183), so `K` is 1024, not 1000."
- Add Quote lines:
  `**Quote.** `S246` cmdline.c:178: "case 'm':"`
  `**Quote.** `S246` cmdline.c:183: "shl += 10;"`
  `**Quote.** `S246` cmdline.c:193: "endptr++;"`
  (All in S246's declared 142-201; no gap.)

### D3 — "skips whitespace and returns -EINVAL" is not on the cited lines
Entry words: "The sysfs store then skips whitespace and returns `-EINVAL` unless the text ends there."
- Cited: sysfs.c:2040 and :2043 only. The whitespace skip is `.ufo/waves/round-44/frozen/src/sysfs.c:2042` `endptr = skip_spaces(endptr);`; the return is `:2044` `return -EINVAL;`.
- Replacement: "The sysfs store then skips whitespace (sysfs.c:2042) and returns `-EINVAL` (sysfs.c:2044) unless the text ends there (sysfs.c:2043)." Add Quote lines:
  `**Quote.** `S243` sysfs.c:2042: "endptr = skip_spaces(endptr);"`
  `**Quote.** `S243` sysfs.c:2044: "return -EINVAL;"`
  (Both in S243's declared 2021-2049.)

### D4 — "-1 rejected" and "bare newline ... parses as 0 and is accepted" have no support in the cited lines
Entry words: "`10MB` (a second letter), `10 M` (a blank before the suffix) and `-1` are rejected with `EINVAL`; and a write of a bare newline parses as 0 and is accepted".
- What makes `-1` fail and `\n` parse as 0 is the digit loop of `_parse_integer_limit`: `kstrtox.c:70` `if ('0' <= c && c <= '9')`, and `kstrtox.c:75` `break;` (a non-digit stops the scan with zero digits consumed; `vsprintf.c:91` `cp += (rv & ~KSTRTOX_OVERFLOW);` then leaves endptr at the sign or newline). `sysfs.c:2046` `return len;` is the accept.
- Those lines are outside S246's declared kstrtox.c range (26-40). The clause needs them, so the gap block must carry them.
- Replacement: "...and `-1` are rejected with `EINVAL` (the digit loop stops at a non-digit: kstrtox.c:70, :75, so the sign leaves `endptr` at `-`); and a write of a bare newline parses as 0 (the same loop stops at `\n`) and is accepted (sysfs.c:2046 `return len;`)." Add Quote lines:
  `**Quote.** `S246` kstrtox.c:70: "if ('0' <= c && c <= '9')"`
  `**Quote.** `S246` kstrtox.c:75: "break;"`
  `**Quote.** `S243` sysfs.c:2046: "return len;"`
- Gap block (lint coupling, mandatory): kstrtox.c 70 and 75 lie outside 26-40, so the entry's `### Range gaps (R51)` block must gain the line `- S246 kstrtox.c: 70, 75`. The L1 regenerates the block with `lint-grounding-r51.py --emit-gaps` rather than hand-editing.

### D5 — "0x10 sets 16" rests on uncited lines
Entry words: "`010` sets 8 and `0x10` sets 16".
- `010` → 8 is supported by kstrtox.c:33 (quoted). `0x10` → 16 needs the base-16 assignment (kstrtox.c:31 `*base = 16;`) and the prefix skip (kstrtox.c:37 `if (*base == 16 && s[0] == '0' && _tolower(s[1]) == 'x')`, :38 `s += 2;`). Without :37-38 the scan would stop at `x` and `0x10` would be EINVAL.
- Replacement: "...`010` sets 8 and `0x10` sets 16 (kstrtox.c:31 selects base 16; :37-38 skip the prefix)." Add Quote lines:
  `**Quote.** `S246` kstrtox.c:37: "if (*base == 16 && s[0] == '0' && _tolower(s[1]) == 'x')"`
  `**Quote.** `S246` kstrtox.c:38: "s += 2;"`
  (In S246's declared 26-40.)
- "decimal otherwise" is supported by kstrtox.c:35 `*base = 10;` (in range); optionally cite it.

### D6 — the path named in the Statement is not what the entry's citation says
Entry words: "`simple_strtoull` resolves base 0 through `_parse_integer_fixup_radix`".
- The resolving call is in `simple_strntoull` (vsprintf.c:79-101, call at :86), which `simple_strtoull` (vsprintf.c:112-115) calls at :114 `return simple_strntoull(cp, endp, base, INT_MAX);`. Read literally, the entry's sentence is true only through that wrapper.
- Replacement: "`simple_strtoull` passes base 0 to `simple_strntoull` (vsprintf.c:114), which resolves it through `_parse_integer_fixup_radix` (vsprintf.c:86)." Add Quote line `**Quote.** `S246` vsprintf.c:114: "return simple_strntoull(cp, endp, base, INT_MAX);"` (in declared 79-115).

### D7 — host "no limit is set" is an unmarked inference; host cite omits :9
Entry words: "The host's one btrfs device (devid 1) reads `scrub_speed_max` 0, mode 644, owner root (capture.txt:8), as uid 1000 with no effective capabilities (capture.txt:1): no limit is set, and this caller [inference: ...] cannot write one."
- capture.txt:8 confirms `scrub_speed_max 1d02…/devinfo/1/scrub_speed_max mode=644 owner=root value=0`. capture.txt:9 confirms `devids=1`, which is what "one btrfs device" rests on; it is not cited.
- capture.txt:1 confirms `uid=1000 CapEff=0000000000000000`.
- "no limit is set" is read through scrub.c:1381-1382 (D1) and applies to the Arch build `7.2.11-arch1-1` (capture.txt:2) only if that build carries the upstream code. Entry's Limits (entry lines 242-243) marks exactly that as an inference ("[inference carried from round 43 for `fs/`; ...]"), but the host reading does not mark it.
- Replacement: "The host's one btrfs device (devid 1; capture.txt:8-9) reads `scrub_speed_max` 0, mode 644, owner root, as uid 1000 with no effective capabilities (capture.txt:1): the value 0 is no limit under the upstream code quoted above [inference: the Arch 7.2.11-arch1-1 build carries that code unchanged; Limits marks the `fs/` carry as inference], and this caller [inference: by ordinary file-mode checks, which the capture does not exercise; ACLs and LSM rules are not captured] cannot write one."

### D8 — "bytes per second" is uncited and unmarked
Entry words: "so `100M` and `100m` both set 104857600 bytes per second".
- The unit comes from `throttle_sent += bio_size;` and `if (sctx->throttle_sent <= div_u64(bwlimit, div))` (scrub.c:1400-1401), and the slice is one second (scrub.c:1369 comment). Neither is cited in GR1, and 1400-1401 are outside S242's declared 1365-1385.
- Replacement: "...both set 104857600 bytes per second [inference: the throttle compares a byte count `bio_size` with the limit, scrub.c:1400-1401, which this row does not quote]." The arithmetic 100 x 2^20 = 104857600 is correct.

## Claims checked and found supported (the L1 can rely on these)

1. Section hash `8eff9637…8660` and lint counts above.
2. All 12 GR1 quotes equal the whole cited line after whitespace collapse (lint-grounding-r51.py:100 `' '.join(s.split())`): cmdline.c:147, 156, 159, 189, 191, 192; vsprintf.c:86; kstrtox.c:29, 30, 33; sysfs.c:2040, 2043. Byte check: cmdline.c:156 `unsigned long long ret = simple_strtoull(ptr, &endptr, 0);`, :189 `if (shl && likely(ptr != endptr)) {`, :191-192, sysfs.c:2040 `limit = memparse(buf, &endptr);`, :2043 `if (*endptr != 0)`.
3. Quote cmdline.c:147 is whitespace-equal to the file's line ` *\tpotentially suffixed with K, M, G, T, P, E.` (the file has a tab after `*`; see N1).
4. Statement "memparse calls simple_strtoull with base 0": cmdline.c:156 (memparse begins at :153).
5. Base selection "hex for leading `0x`/`0X` followed by hex digit, octal for any other leading `0`, decimal otherwise": kstrtox.c:28-35 (`else` at :32 is octal; `else` at :34 is decimal).
6. "suffix counts only when at least one digit came before it": cmdline.c:189 `ptr != endptr`. In the 0x case the consumed text always includes a digit (kstrtox.c:30 requires isxdigit(s[2])), so the equivalence holds.
7. "a shifted value that overflows becomes ULLONG_MAX": cmdline.c:191-192.
8. "K is 1024 ... 100M = 104857600": cmdline.c:181-183 shift 10 for K; 100 x 2^20 = 104857600.
9. "010 sets 8": kstrtox.c:29, 33; the scan reads 0,1,0 in base 8.
10. "10MB rejected": memparse leaves endptr at `B` (cmdline.c:193 advances once; the `B` is not consumed), skip_spaces is a no-op, sysfs.c:2043 `!= 0` → EINVAL.
11. "10 M rejected": endptr at the blank; sysfs.c:2042 skips to `M`; sysfs.c:2043 → EINVAL.
12. "0 means no limit" (the arithmetic that matters): scrub.c:1381-1382 returns before throttling when `bwlimit == 0` (see D1 for citation form).
13. Universal words: "only" (cmdline.c:189 gate), "any other leading `0`" (kstrtox.c:32-33 else), "unless" (sysfs.c:2043). No "first", "always", "every" in GR1.
14. Host: capture.txt:1 `uid=1000 CapEff=0000000000000000`; capture.txt:8 `mode=644 owner=root value=0` for devinfo/1; capture.txt:9 `devids=1`.
15. "Nothing was written to test the parse" (entry line 54): true for this seat too; nothing was written to the host.

## Notes (not defects; optional)

- N1: cmdline.c:147 is ` *\tpotentially...` (tab). The lint's whitespace collapse accepts the entry's space. A byte-exact reader sees a tab. Optional: write the quote with the tab.
- N2: In base 16, `E` is a hex digit (kstrtox.c:72-73), so `0x1E` is 30 and takes no suffix. The entry's suffix sentence is not false, but a reader could take `0x1E` as 1 EiB. Optional sentence: "(in base 16 `E` is a digit, kstrtox.c:72-73, so `0x1E` is 30)."
- N3 (lint blind spot): prose `file:line` cites in GR1 whose basename is not in PROSE['GR1'] (e.g. scrub.c, ioctl.c) are skipped (lint-grounding-r51.py:238-240). Only Quote lines of such files are checked and enter the gap computation. The L1 should not rely on a prose scrub.c cite passing the lint.
- N4: The Limits sentence (entry lines 242-243) marks the Arch-patch premise as inference; D7 asks the row to carry the same mark where it depends on it.
- N5: No tool was installed. Scratch dir `/fast/scratch/hyaku/tsukuroi-r51/R51W1PreCritGR1a/` removed after the receipt copy.

## Lint coupling for the pre-w2 amendment

If the L1 adopts D1-D8, the amendment must (a) add the Quote lines named above, (b) regenerate the gap block with `python3 tools/lint-grounding-r51.py --revision <REV> --emit-gaps` (expected new line: `- S246 kstrtox.c: 70, 75`; no other gap lines are added by D1-D8 because every other new cited line is inside a declared range), and (c) re-run the lint and the section-hash command. These are the only mechanical consequences I checked; I did not run the admission counter on a candidate, since that would require editing the lane.
