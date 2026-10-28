VERDICT: defect-found
SECTION SHA256: 8eff963765feccd759ac62e601776c8cc9ae07352b43d50c9e4d81e6b5178660

Seat: R51W1PreRevGR1a (uncounted pre-read, claim C1, row GR1 at 2732ee6c06108c031c4d8043239b994e0504eb2f). Scope: GR1 section (entry.md lines 14-55), Limits (240-267) and Range gaps block (269-275) for context.

## Provenance and mechanical checks (all run by me)

- Entry extracted: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/knowledge/btrfs-scrub-grounding-r45.md`, 348 lines.
- `python3 tools/check-scrub-admission-r51.py --revision 2732ee6c... --section-hash --no-base-check` -> GR1 `8eff963765feccd759ac62e601776c8cc9ae07352b43d50c9e4d81e6b5178660` (matches the frozen hash). GR2 `27aa7abb...`, GR3 `43430a14...` also printed; `structural_ok: 1`, `problems: []`.
- `python3 tools/lint-grounding-r51.py --revision 2732ee6c...` -> `verdict: PASS`, `lint_ok: 3`, `rows_clean: 3`, `gap_ok: 1`, `gaps_computed: 62`, `quote_bad: 0` of 63 quotes; GR1: 12 quotes, 0 bad, 2 prose cites, 0 bad.
- Snapshot digests: `sha256sum -c SHA256SUMS` OK in round-45/frozen/src (cmdline.c, dev-replace.c, kstrtox.c, vsprintf.c, systemd.kill.xml) and round-44/frozen/src (sysfs.c, scrub.c, units). Row-to-file mapping: S246 = round-45 `cmdline.c` 1af5ad98..., `vsprintf.c` cabb648a..., `kstrtox.c` 0c52ae02... (match SOURCES.md S246 digests); S243 = round-44 `sysfs.c` ce146120... (matches S243); S242 = round-44 `scrub.c` f347931b... (matches S242). Provenance: round-45 FETCH.txt and round-44 FETCH.txt show the `?h=v7.2.11` URLs for these files.
- Host capture digest: `sha256sum round-45/frozen/hostcap/capture.txt` = f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70 (matches S249).

## Defects

### D1 - "0 means no limit" and "bytes per second" are uncited in GR1
Clause (GR1 Statement, last sentence): "...which removes the limit (0 means no limit, SR8)." and "...`100M` and `100m` both set 104857600 bytes per second".
Pinned line: `S242` scrub.c:1380-1382 (round-44/frozen/src/scrub.c): `bwlimit = READ_ONCE(device->scrub_speed_max);` / `if (bwlimit == 0)` / `return;`. The GR1 row's own citations are only S246 and S243; the "0 means no limit" clause rests on an earlier round's SR8 entry, not on any line this row cites. The lines 1380-1382 are inside the declared S242 range (1365-1385), so citing them adds nothing to the Range gaps block.
The unit clause: scrub.c:1369 says only "bandwidth-limit ... timeslice is 1 second"; scrub.c:1400 `sctx->throttle_sent += bio_size;` supports bytes, but 1400 is outside the declared S242 range, and I did not read the comparison of `bwlimit` against `throttle_sent` beyond line 1400.
Exact replacement for the sentence ending "...removes the limit (0 means no limit, SR8).":
  "...which removes the limit: `S242` scrub.c:1380-1382 returns at once from the throttle when `bwlimit == 0`."
Exact added Quote line (after the existing S243 quotes):
  "**Quote.** `S242` scrub.c:1381: "if (bwlimit == 0)""
Exact replacement for "104857600 bytes per second":
  "104857600 bytes per second [inference: the throttle's unit is bytes by the `bio_size` accounting at `S242` scrub.c:1400, outside the declared range; the bandwidth comparison at scrub.c:1401 onward was not read]"

### D2 - "either case" and "a 10-bit shift per step" rest on uncited case labels
Clause: "`memparse` takes at most one suffix letter, `K`, `M`, `G`, `T`, `P` or `E` in either case, each step multiplying by a further 1024 (a 10-bit shift per step, so `K` is 1024, not 1000)".
The only cited suffix line is `S246` cmdline.c:147, a doc comment that lists uppercase letters only. The case labels that support "either case" and the shift are at cmdline.c:160-187 (within the declared S246 range 142-201), which are not cited.
Pinned lines: cmdline.c:178 `	case 'm':`, cmdline.c:182 `	case 'k':`, cmdline.c:183 `		shl += 10;` (K sets shl to 10 at line 183, falls through; the `case 'M'`/`'m'` at 177-178 add another 10 at 179).
Exact added Quotes (no range change, no gap-block change):
  "**Quote.** `S246` cmdline.c:178: "case 'm':""
  "**Quote.** `S246` cmdline.c:182: "case 'k':""
  "**Quote.** `S246` cmdline.c:183: "shl += 10;"" (line 183 is the `K` branch; the same text recurs at 163, 167, 171, 175, 179; cite as "line 183" and keep the line number in the quote label)

### D3 - "-1 rejected with EINVAL" is correct but its mechanism is uncited and outside the declared range
Clause: "...`10 M` (a blank before the suffix) and `-1` are rejected with `EINVAL`". The Statement's examples "follow from the quoted code" (line 54), which is not true for `-1`: no quoted line covers sign handling.
Pinned mechanism: `S246` kstrtox.c:70 `if ('0' <= c && c <= '9')` and kstrtox.c:74-75 `else` / `break;` in `_parse_integer_limit` (kstrtox.c:57-95). For `-1` the leading `-` fails both digit tests, the loop breaks with zero characters consumed, `endptr` stays at `-`, `shl` is 0, and sysfs.c:2042-2043 then returns `-EINVAL` (I verified this chain by reading the code; it is a derivation, not an observed write).
Declared S246 kstrtox.c range is 26-40 (SOURCES.md S246), so kstrtox.c:70-75 is a range gap. Either:
  (a) Replacement wording (needs SOURCES.md S246 range widened to "lib/kstrtox.c lines 26-40, 57-95" and `lint-grounding-r51.py --emit-gaps` regenerated; that is the L1's decision): "...`10 M` (a blank before the suffix) and `-1` are rejected with `EINVAL`: a leading `-` is not a digit (`S246` kstrtox.c:70 `if ('0' <= c && c <= '9')`), so no digit is consumed and `S246`... [cite kstrtox.c:70 and 74-75 as quotes]."
  (b) Or drop `and `-1`` from the clause and the Statement, which removes the gap.
I recommend (a) because the clause is true.

### D4 - Limits cites the wrong capture line for "cannot write"
Limits line 244-245: "GR1's examples are derived from the quoted code, not from a write on this host (the caller cannot write the attribute, capture.txt:1)."
capture.txt:1 is `captured 2026-10-27T02:09:52Z uid=1000 CapEff=0000000000000000`; it shows the uid and capabilities, not the mode or owner. The mode and owner are at capture.txt:8 (`scrub_speed_max ... mode=644 owner=root value=0`).
Exact replacement: "(the caller is uid 1000 with no effective capabilities, capture.txt:1, and the attribute is mode 644 owner root, capture.txt:8; the write denial itself is an [inference], see GR1)."

### D5 (minor, cite the host device count) - "one btrfs device" cites :8 only
GR1 Host reading: "The host's one btrfs device (devid 1) reads ... (capture.txt:8)". The "one device" fact is capture.txt:9 (`devinfo ... devids=1`). Exact replacement: "(capture.txt:8, and `devids=1` at capture.txt:9)".

## Non-blocking notes (not defects; no change required, or optional)

- N1: "the sysfs store then skips whitespace" generalises `skip_spaces` (sysfs.c:2042), whose body is not pinned in any snapshot; the trailing-newline case is supported by the comment at sysfs.c:2041. Acceptable as stated; optional: say "skips trailing newline and spaces (sysfs.c:2041-2042)".
- N2: The overflow clause ("a shifted value that overflows becomes `ULLONG_MAX`") omits that a digit string beyond 2^64 also yields `ULLONG_MAX` (kstrtox.c:83-88, consumed via `rv & ~KSTRTOX_OVERFLOW` at vsprintf.c:91). Not false; the clause does not claim exhaustiveness.
- N3: "a bare newline parses as 0 and is accepted" is a derivation (cmdline.c:189 needs `shl`, which is 0 when no digit was consumed; sysfs.c:2042-2043 accepts a NUL after the newline). It depends on the sysfs buffer being NUL-terminated, which sysfs.c:2043 itself assumes; no uncited line contradicts it.
- N4: The octal/hex rules are correct on the 0X spelling (kstrtox.c:30 uses `_tolower(s[1]) == 'x'`) and the `0x` skip is at kstrtox.c:37-38 (inside the declared range, uncited). Optional to cite.
- N5: The entry's [inference] on "this caller cannot write one" is correctly marked: DAC is not in the pinned bytes, and capture.txt does not exercise ACL or LSM rules. The mode 644 itself is pinned at `S243` sysfs.c:74 (`__INIT_KOBJ_ATTR(_name, 0644, ...)`, round-44 snapshot), which could be cited so only the DAC step stays marked. Optional.

## Claims checked and found supported

- memparse calls `simple_strtoull(ptr, &endptr, 0)`: cmdline.c:156. ✓
- Suffix-only-after-digit: cmdline.c:189 `if (shl && likely(ptr != endptr))`. ✓ (`ptr != endptr` is equivalent here because only digits are consumed: kstrtox.c:70-78.)
- Overflow -> `ULLONG_MAX`: cmdline.c:191-192. ✓
- Overflow consumes the suffix: cmdline.c:159 comment. ✓
- simple_strtoull uses `_parse_integer_fixup_radix`: vsprintf.c:86 (inside `simple_strntoull`, 79-101), reached from `simple_strtoull` at vsprintf.c:112-115. ✓ (chain via 114; line 114 not cited, within declared range)
- Base-0 radix rules: kstrtox.c:28-35 (`0x`/`0X` + hex digit -> 16; other leading `0` -> 8; else 10). ✓ "any other leading `0`" includes `0x` with no hex digit (line 33 is the else). ✓
- `0x` prefix skip: kstrtox.c:37-38. ✓
- Store path: sysfs.c:2040 `limit = memparse(buf, &endptr);`, 2041 comment (trailing `\n`), 2042 `skip_spaces`, 2043-2044 `if (*endptr != 0) return -EINVAL;`. ✓
- `100M` and `100m` = 104857600 (100 x 2^20): arithmetic ✓; case `'m'` and `'M'` both reachable (cmdline.c:177-178). ✓
- `010` = 8 (octal, kstrtox.c:33). ✓ `0x10` = 16 (kstrtox.c:30-31, 37-38). ✓
- `10MB` -> `EINVAL`: after the suffix `endptr++` (cmdline.c:193) points at `B`; sysfs.c:2043 rejects. ✓
- `10 M` -> `EINVAL`: `*endptr == ' '` so `shl` is 0 (cmdline.c:189 not taken); skip_spaces lands on `M`; sysfs.c:2043 rejects. ✓
- "K is 1024": `shl += 10` once for K (cmdline.c:183) then shift at 191. ✓
- Universals: "at most one suffix letter" (cmdline.c:160-194 consumes one switch char), "any other leading 0" (kstrtox.c:33). No other unqualified "only/always/first/any" in the row. ✓
- Host: capture.txt:1 uid=1000 and CapEff=0 ✓; capture.txt:8 devid-1 `scrub_speed_max` mode=644 owner=root value=0 ✓; capture.txt:9 devids=1 ✓.
- [inference] mark on "this caller cannot write one" is placed on an undecided step (DAC/ACL/LSM not captured). ✓
- Range gap block (Range gaps R51 lines 271-275) is not affected by GR1's own citations (all GR1 cites fall inside declared ranges: S246 cmdline 142-201, vsprintf 79-115, kstrtox 26-40; S243 sysfs 2021-2049). The only GR1-citing gap is in D3 (kstrtox 70-75) and the D1 cite (S242 1380-1382) is inside its declared range. ✓
- The Statement's sysfs.c:2040 is in the S243 snapshot whose tag is v7.2.11 (round-44 FETCH.txt). ✓

## Residual verification gaps

- I did not write any value to a sysfs attribute (no write is permitted on this host); the examples are from code reading, as the entry itself says.
- I did not read scrub.c beyond line 1400 for the unit comparison (D1).
- The skip_spaces body and the kernfs NUL-termination are not in any pinned snapshot (N1, N3).
