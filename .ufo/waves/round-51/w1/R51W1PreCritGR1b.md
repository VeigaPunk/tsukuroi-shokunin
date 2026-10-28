VERDICT: defect-found
SECTION SHA256: 8eff963765feccd759ac62e601776c8cc9ae07352b43d50c9e4d81e6b5178660

Seat R51W1PreCritGR1b, uncounted pre-read, critic, row GR1 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` at 2732ee6c06108c031c4d8043239b994e0504eb2f (entry lines 14-55). Section hash re-run: `check-scrub-admission-r51.py --section-hash --no-base-check` prints 8eff9637...78660 for GR1, matching the brief (receipt: `w1/R51W1PreCritGR1b/section-hash.txt`).

## Pinned-source provenance (digests re-run)

- `round-45/frozen/src/SHA256SUMS`, `sha256sum -c`: cmdline.c OK (1af5ad98…), vsprintf.c OK (cabb648a…), kstrtox.c OK (0c52ae02…), dev-replace.c OK (f07ef0a0…). These equal the digests in `corpus/SOURCES.md:255` (S246) and `:256` (S247).
- S243 is `round-44/frozen/src/sysfs.c` (ce146120…): `sha256sum -c` OK against `round-44/frozen/src/SHA256SUMS`; equals `corpus/SOURCES.md:252`. FETCH.txt:4 confirms tag v7.2.11.
- S242 (cited only in the D3 replacement) is `round-44/frozen/src/scrub.c` (f347931b…): `sha256sum -c` OK.
- S249 is `round-45/frozen/hostcap/capture.txt`, read directly.

## Lint (`lint-grounding-r51.py --revision 2732ee6c…`)

Observed: `"verdict": "PASS"`, `"lint_ok": 3`, `"gap_ok": 1`, `"gaps_computed": 62`, GR1 `cites: 2, quotes: 12, cite_bad: 0, quote_bad: 0`, `snapshot_problems: []`. The lint does not check clause truth; the defects below are not caught by it (receipt: `w1/R51W1PreCritGR1b/lint.json`).

## Defects (each: entry clause, pinned line that fails or is absent, exact replacement)

### D1. The derived examples cite no line for the digit scan

Entry line 54: "Nothing was written to test the parse; the examples above follow from the quoted code."
Entry lines 22-25 (the examples `0x10` → 16, `010` → 8, `10MB`, `10 M`, `-1` → EINVAL).

The row quotes nothing that makes these true. Four pinned lines carry the derivation and are not cited:
- `round-45/frozen/src/vsprintf.c:89` `rv = _parse_integer_limit(cp, base, &result, max_chars - prefix_chars);` and `:91` `cp += (rv & ~KSTRTOX_OVERFLOW);`. Without :91, endptr does not move past the digits, so the suffix and the trailing-text checks have nothing to act on.
- `round-45/frozen/src/kstrtox.c:37-38` `if (*base == 16 && s[0] == '0' && _tolower(s[1]) == 'x')` / `s += 2;`. This is what makes `0x10` parse as 16.
- `round-45/frozen/src/kstrtox.c:70` `if ('0' <= c && c <= '9')`, `:74-75` `else` / `break;`, `:77` `if (val >= base)`. This is what makes `-1` stop at the `-` and what makes `010` parse as octal 8 (`8`/`9` would stop it).

Replacement for entry line 54:
"Nothing was written to test the parse; the examples above follow from the quoted code and from the digit scan quoted below (`S246` vsprintf.c:89 and :91, kstrtox.c:37-38, :70, :74-75, :77)."

Add these quote lines after entry line 49:
**Quote.** `S246` vsprintf.c:89: "rv = _parse_integer_limit(cp, base, &result, max_chars - prefix_chars);"
**Quote.** `S246` vsprintf.c:91: "cp += (rv & ~KSTRTOX_OVERFLOW);"
**Quote.** `S246` kstrtox.c:37: "if (*base == 16 && s[0] == '0' && _tolower(s[1]) == 'x')"
**Quote.** `S246` kstrtox.c:70: "if ('0' <= c && c <= '9')"
**Quote.** `S246` kstrtox.c:77: "if (val >= base)"

Range note for the amendment: vsprintf.c:89-91 and kstrtox.c:37 are inside the declared S246 ranges (`corpus/SOURCES.md:255`: vsprintf 79-115, kstrtox 26-40). kstrtox.c:70 and :77 are outside them, so `--emit-gaps` must be re-run; the expected new S246 gap line is `S246 kstrtox.c: 70, 77`. The gap block is generated, so this is an edit to the generated block only.

### D2. "skips whitespace" is an unmarked inference; its citation is missing

Entry line 25-26: "The sysfs store then skips whitespace and returns -EINVAL unless the text ends there"; this underwrites the bare-newline clause (line 24) and the `10 M` rejection (line 23).

Pinned: `round-44/frozen/src/sysfs.c:2042` `endptr = skip_spaces(endptr);` is inside the S243 declared range 2021-2049 but is not cited by the row. The row cites :2040 and :2043 only. The body of `skip_spaces` is in no pinned snapshot. `grep -rn skip_spaces round-44/frozen/src round-45/frozen/src` finds only call sites (sysfs.c:208, :790, :1368, :2042; cmdline.c:283; vsprintf.c:3479, :3480, :3569, :3659). Whether it consumes `\n` is therefore not pinned.

Replacement for the sentence on entry line 25-26:
"The sysfs store then calls `skip_spaces` (S243 sysfs.c:2042, quoted below) and returns `-EINVAL` unless the text ends there (S243 sysfs.c:2043). [inference: the definition of `skip_spaces` is outside the pinned snapshots; taking it to skip `isspace()` characters, the newline of a bare `echo` is consumed and `10 M` leaves `M`.]"

Add the quote line:
**Quote.** `S243` sysfs.c:2042: "endptr = skip_spaces(endptr);"

Range note: 2042 is inside the declared S243 range 2021-2049, so the gap block is unchanged by this edit.

### D3. "0 means no limit" and "bytes per second" are not supported by any line the row cites

Entry line 24-25: "which removes the limit (0 means no limit, SR8)"; entry line 22: "set 104857600 bytes per second".

GR1 cites no S242 line. "SR8" points to the round-44 entry, not to pinned bytes in this row. The lines that carry both claims are in the round-44 snapshot named in line 1 of the entry:
- `round-44/frozen/src/scrub.c:1368-1369` "* Throttling of IO submission, bandwidth-limit based, the timeslice is 1" / "* second.  Limit can be set via /sys/fs/UUID/devinfo/devid/scrub_speed_max." (the one-second slice)
- `round-44/frozen/src/scrub.c:1381-1382` `if (bwlimit == 0)` / `return;` (zero is no throttle)
- `round-44/frozen/src/scrub.c:1400-1401` `sctx->throttle_sent += bio_size;` / `if (sctx->throttle_sent <= div_u64(bwlimit, div))` (the count the limit is compared with)

Replacement for "(0 means no limit, SR8)":
"(0 means no limit: `S242` scrub.c:1381, `if (bwlimit == 0)`, returns before any throttling)"

Replacement for "set 104857600 bytes per second":
"set 104857600 per second (the slice is one second, `S242` scrub.c:1368-1369; the count it is compared with is `bio_size`, scrub.c:1400, [inference: that `bio_size` is in bytes is not pinned by these lines])"

Add quote lines:
**Quote.** `S242` scrub.c:1381: "if (bwlimit == 0)"
**Quote.** `S242` scrub.c:1369: "second.  Limit can be set via /sys/fs/UUID/devinfo/devid/scrub_speed_max."

Range note: scrub.c:1368-1369, :1381, :1400-1401 are inside the declared S242 range 1365-1385 (entry line 253), so the gap block is unchanged.

## Minor (citation only, not a defect)

- Entry lines 51-52 "The host's one btrfs device (devid 1) reads scrub_speed_max 0 ... (capture.txt:8)". The "one device" claim is supported by `capture.txt:9` `devinfo ... devids=1`, and the enumeration is the glob `/sys/fs/btrfs/*/devinfo` (`hostcap/capture.sh:27-29`), so it is not an overreach. Cite `capture.txt:8-9` and `capture.sh:27-29`.
- Entry line 53 `[inference: ...]` is correctly placed: `capture.txt` does not exercise file-mode checks, and the mark says so.

## Claims checked and found supported (read against the pinned bytes)

- cmdline.c:156 `unsigned long long ret = simple_strtoull(ptr, &endptr, 0);`: memparse uses base 0. Quote verbatim.
- cmdline.c:147 with leader: ` *\tpotentially suffixed with K, M, G, T, P, E.`, so the quote `* potentially suffixed with K, M, G, T, P, E.` matches the whole line.
- cmdline.c:159, :189, :191, :192: quotes match verbatim. :189 `ptr != endptr` gives "suffix counts only when a digit came before it". :191-192 give "a shifted value that overflows becomes ULLONG_MAX". Both correct.
- cmdline.c:160-187: the switch falls through, adding 10 per step, with upper and lower-case letters K, M, G, T, P, E. K is shl 10 (1024), so "K is 1024" holds. The digit-count claim "each step multiplying by a further 1024" holds.
- cmdline.c:193 `endptr++;` is executed once, so "at most one suffix letter" holds.
- kstrtox.c:28-35: radix rules. `0x`/`0X` followed by a hex digit gives 16 (:30-31); other leading `0` gives 8 (:33); otherwise 10 (:35). The quotes at :29, :30, :33 match verbatim.
- vsprintf.c:86 `cp = _parse_integer_fixup_radix(startp, &base);` matches verbatim and supports "resolves base 0 through _parse_integer_fixup_radix" (the call at vsprintf.c:112-114 is the unquoted hop; it is minor).
- sysfs.c:2040 `limit = memparse(buf, &endptr);` and :2043 `if (*endptr != 0)` match verbatim. :2044 `return -EINVAL;` supports "returns -EINVAL".
- `100M` / `100m` → 104857600 is 100 × 2^20, correct. `10MB`: after the M, endptr is at `B` (cmdline.c:193), skip_spaces leaves `B` (D2 caveat), so EINVAL holds.
- `-1`: '-' is not a digit (kstrtox.c:70), so no digits; endptr stays at start; `-` is not a suffix; EINVAL holds (D1 caveat for the citation only).
- Bare newline: fixup gives base 10 (kstrtox.c:35), no digits gives 0 (cmdline.c:156), `\n` is no suffix (cmdline.c:160); acceptance holds only with the D2 inference.
- Host: `capture.txt:1` `uid=1000 CapEff=0000000000000000` supports "uid 1000 with no effective capabilities". `capture.txt:8` `value=0 mode=644 owner=root` supports the read and mode facts.
- The `[inference]` on entry line 53 (file-mode checks not exercised) is correctly marked.
- Words "only", "any", "each", "at most" in GR1 hold over the pinned code (see cmdline.c:189, :193; kstrtox.c:33; cmdline.c:182-184).

## Not done

- I did not check `skip_spaces` against a live kernel tree (not pinned here; out of scope for the snapshot bar); D2 is stated as an inference for that reason.
- I did not run `--emit-gaps` on a modified entry (no tracked-file writes); the Range-gap note in D1 is stated from the declared ranges in `corpus/SOURCES.md`.
- I did not read rows GR2 or GR3 (outside item C1-PREREAD).
