VERDICT: defect-found
SECTION SHA256: 8eff963765feccd759ac62e601776c8cc9ae07352b43d50c9e4d81e6b5178660

Seat: R51W1PreRevGR1b (reviewer, uncounted pre-read, item C1-PREREAD). Row GR1 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` at 2732ee6c06108c031c4d8043239b994e0504eb2f (entry extracted to scratch; section lines 14-55, `### Range gaps (R51)` lines 269-275, Limits lines 240-267).

## Checks run

- Section hash: `python3 tools/check-scrub-admission-r51.py --revision 2732ee6c… --section-hash --no-base-check` → `"GR1": "8eff963765feccd759ac62e601776c8cc9ae07352b43d50c9e4d81e6b5178660"`, `structural_ok` 1, `problems` []. Matches the brief.
- Snapshot digests: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-45/frozen/src/` → cmdline.c OK, kstrtox.c OK, vsprintf.c OK, dev-replace.c OK, systemd.kill.xml OK. In `.ufo/waves/round-44/frozen/src/` → sysfs.c OK (scrub.c, the two units and PKGBUILD also OK).
- Which snapshot is which S-row: S246 = `round-45/frozen/src/{cmdline.c,vsprintf.c,kstrtox.c}` (FETCH.txt line 2 names them; tag v7.2.11, peeled a2de78ee…; SOURCES.md:255 declares cmdline.c 142-201, vsprintf.c 79-115). S243 = `round-44/frozen/src/sysfs.c` (FETCH.txt; SOURCES.md:252 declares 72-74, 2021-2049, 2113). S242 (scrub.c, cited below for the throttle) = `round-44/frozen/src/scrub.c` (SOURCES.md:251 declares 1365-1385, 3140-3162, 3215-3226, 3321-3337).
- `lint-grounding-r51.py --revision 2732ee6c…` → verdict PASS; GR1: cites 2, quotes 12, cite_bad 0, quote_bad 0, problems []; gap_ok 1 (gaps_computed 62, gap_missing [], gap_extra []). The lint checks quotes and gap block mechanically; it does not check the clauses below.
- Host capture `round-45/frozen/hostcap/capture.txt`: line 1 `captured … uid=1000 CapEff=0000000000000000`; line 8 `scrub_speed_max … mode=644 owner=root value=0`; line 9 `devinfo … devids=1`.

## Quotes and cited lines (all opened; each supports the clause it is cited for)

- S246 cmdline.c:147 `* potentially suffixed with K, M, G, T, P, E.` — exact (leader `*` present).
- S246 cmdline.c:156 `unsigned long long ret = simple_strtoull(ptr, &endptr, 0);` — exact; supports "calls simple_strtoull with base 0".
- S246 cmdline.c:159 — exact; S246 cmdline.c:189 `if (shl && likely(ptr != endptr)) {` — exact; supports "suffix counts only when at least one digit came before it" (ptr != endptr; I checked that the 0x branch always has an isxdigit digit, so the equivalence holds); S246 cmdline.c:191-192 — exact; supports the ULLONG_MAX-on-overflow clause.
- S246 cmdline.c:160-187 (not quoted, read): switch is cumulative via fallthrough; `M` gives shl 20, `K` gives shl 10; cases cover K,M,G,T,P,E in both cases. Supports "at most one suffix letter … either case … each step a further 1024".
- S246 vsprintf.c:86 `cp = _parse_integer_fixup_radix(startp, &base);` — exact; sits inside `simple_strntoull` (vsprintf.c:79-101), see defect D5.
- S246 kstrtox.c:29-33 — `if (s[0] == '0') {`, `if (_tolower(s[1]) == 'x' && isxdigit(s[2]))`, `*base = 8;` all exact; supports 0x→16 needs a hex digit at s[2], leading-0 → 8, else 10.
- S243 sysfs.c:2040 `limit = memparse(buf, &endptr);` and sysfs.c:2043 `if (*endptr != 0)` — exact; sysfs.c:2042 `endptr = skip_spaces(endptr);` and 2044 `return -EINVAL;` support the -EINVAL clause.
- Derived examples, each traced through the pinned code by hand: `100M`/`100m` → 100<<20 = 104857600 (cmdline.c:178, 183 path); `010` → octal 8 (kstrtox.c:33; digits 0,1,0 base 8); `0x10` → 16 (kstrtox.c:30, fixup at vsprintf.c:86 skips "0x"); `10MB` → endptr at 'B' after the consumed suffix, then `*endptr != 0` → EINVAL (cmdline.c:193, sysfs.c:2043); `10 M` → endptr at ' ', default case, no shift, skip_spaces stops at 'M' → EINVAL; `-1` → `_parse_integer_limit` breaks on '-' (kstrtox.c:70-78, nothing consumed, no sign handling in simple_strntoull) → endptr at '-' → EINVAL. All true.
- "K is 1024, not 1000": cmdline.c:181-183 (shl 10). True.
- Word check: "only" (cmdline.c:189), "any other leading 0" (kstrtox.c:34-35), "at most one" (cmdline.c:160-187 default:break), "unless the text ends there" (sysfs.c:2043). All true over the pinned code.
- Host reading: uid 1000 with no effective capabilities (capture.txt:1), value 0, mode 644, owner root (capture.txt:8). True. The "cannot write one" sentence is marked `[inference: …]`; the mark is correct (file-mode reasoning, no ACL/LSM capture).

## Defects

D1 — Clause: "which removes the limit (0 means no limit, SR8)."
Problem: no pinned line cited in GR1 supports it. GR1 cites no scrub.c line; "SR8" points to the round-44 entry `corpus/knowledge/btrfs-scrub-record-r44.md:56-` (SR8), which is itself not a pinned source for this row. The pinned support exists, in S242 (declared range 1365-1385, SOURCES.md:251):
  `round-44/frozen/src/scrub.c:1380` `bwlimit = READ_ONCE(device->scrub_speed_max);`
  `round-44/frozen/src/scrub.c:1381` `if (bwlimit == 0)`
  `round-44/frozen/src/scrub.c:1382` `return;`
Replacement clause (replace the parenthetical): "which removes the limit: the throttle returns at once when the value is 0 (scrub.c:1380-1382)." Add a Quote line: "**Quote.** `S242` scrub.c:1381: "if (bwlimit == 0)"" (and the same for scrub.c:1382 "return;" if the row keeps both). Add 1380-1382 to the S242 row cites so the gap block is regenerated; 1380-1382 lie inside the declared 1365-1385, so no new gap line is expected, but re-run `lint-grounding-r51.py --emit-gaps` to confirm.

D2 — Clause: "`100M` and `100m` both set 104857600 bytes per second".
Problem: the unit "bytes per second" is not stated by any line the row cites. The nearest pinned text is `round-44/frozen/src/scrub.c:1369` `* second.  Limit can be set via /sys/fs/UUID/devinfo/devid/scrub_speed_max.` (a bandwidth-limit over a 1-second timeslice; `time_slice = 1000` at scrub.c:1374). The divisor at scrub.c:1388 `div = clamp(bwlimit / (16 * 1024 * 1024), 1, 64);` implies a byte count, but that is an inference.
Replacement: "both set the value 104857600 (`scrub_speed_max` is the throttle's bandwidth limit over a one-second timeslice, scrub.c:1369 and 1374; [inference: the unit is bytes per second, read from the 16 MiB divisor at scrub.c:1388])." Mark the unit as inference, or cite scrub.c:1388 in the Quote list.

D3 — Clause: "a write of a bare newline parses as 0 and is accepted".
Problem: "accepted" depends on the sysfs write buffer being NUL-terminated after the newline (sysfs.c:2043 `*endptr != 0` only passes if the byte after the whitespace is 0). No pinned file shows that: grep of every round-44/45 snapshot finds no `buf[len]` store (the kernfs write path is not in any pinned file). The parse to 0 itself is true by kstrtox.c:70-78 (no digit, nothing consumed) and the switch default (cmdline.c:185-186).
Replacement: "a write of a bare newline parses as 0 (kstrtox.c:70-78 consumes no digit; cmdline.c:185-186 takes no suffix) and, [inference: if the sysfs write buffer is NUL-terminated after the newline, which no pinned file shows], is accepted, which removes the limit (scrub.c:1381-1382)."

D4 — Clause: "The sysfs store then skips whitespace".
Problem: the definition of `skip_spaces` is in no pinned file (grep of round-44/45 snapshots finds only call sites, e.g. round-44 sysfs.c:208, 790, 1368). The name is the only evidence the reader gets from GR1.
Replacement: "The sysfs store then skips whitespace [inference: `skip_spaces` is defined outside the pinned files; sysfs.c:2042 is its only pinned call]". Alternatively pin it; no pinned source defines it.

D5 — Clause: "`simple_strtoull` resolves base 0 through `_parse_integer_fixup_radix`".
Problem (citation, not truth): the cited line vsprintf.c:86 is inside `simple_strntoull`, not `simple_strtoull`. The link that makes the clause true is vsprintf.c:112-114: `unsigned long long simple_strtoull(const char *cp, char **endp, unsigned int base)` / `return simple_strntoull(cp, endp, base, INT_MAX);` (line 114). Both lines lie inside S246's declared vsprintf.c 79-115.
Replacement: add "**Quote.** `S246` vsprintf.c:114: "return simple_strntoull(cp, endp, base, INT_MAX);"" and write the clause as: "`simple_strtoull` (vsprintf.c:114) calls `simple_strntoull`, which resolves base 0 through `_parse_integer_fixup_radix` (vsprintf.c:86)."

D6 — Clause: "The host's one btrfs device (devid 1) reads `scrub_speed_max` 0, mode 644, owner root (capture.txt:8)".
Problem (citation): "devid 1" and "one device" are on capture.txt:9 (`devinfo … devids=1`), not line 8.
Replacement: "The host's one btrfs device (devid 1, capture.txt:9) reads `scrub_speed_max` 0, mode 644, owner root (capture.txt:8)."

Optional (not defects; citation tightening): the `-1` rejection could cite kstrtox.c:70-78 (the '-' is not a digit and simple_strntoull has no sign handling, vsprintf.c:79-101). The claim is true as stated.
Optional: the "(SR8)" back-references in the Statement and the "(0 means no limit, SR8)" parenthetical name an unpinned round-44 entry; removing them (D1) is sufficient.

## Supported (read and checked, no defect)

- Statement opening: memparse called from sysfs store (sysfs.c:2040) → simple_strtoull base 0 (cmdline.c:156).
- Base rules: hex only for `0x`/`0X` + hex digit (kstrtox.c:29-31); octal for other leading 0 (kstrtox.c:33); decimal otherwise (kstrtox.c:35).
- Suffix set K,M,G,T,P,E, both cases, one letter, 10-bit steps (cmdline.c:160-187).
- Suffix counts only with a preceding digit (cmdline.c:189).
- Overflow → ULLONG_MAX, suffix consumed (cmdline.c:159, 191-192).
- Whitespace-then-end rule and -EINVAL (sysfs.c:2042-2044).
- `10MB`, `10 M`, `-1` → EINVAL; `100M`/`100m` → 104857600; `010` → 8; `0x10` → 16 (traced; see above).
- Host: uid 1000 no effective caps (capture.txt:1); value 0, mode 644, owner root (capture.txt:8); the write-denial is correctly marked [inference].
- Limits bullets naming GR1: "GR1's examples are derived from the quoted code, not from a write on this host" — true.
- Snapshot provenance: S246 and S243 file digests match their SHA256SUMS; FETCH tag/peel lines match the entry header.

## Residual risk / not done

- I did not run `--emit-gaps` (not in this item's command list); the gap block was checked only by the lint's PASS.
- I did not open kernfs, skip_spaces, or any non-pinned kernel file (no such command authorized); D3 and D4 are stated as unpinned, not as false.
- Nothing was written or executed on the host; the parse examples are derivations from the pinned code.
