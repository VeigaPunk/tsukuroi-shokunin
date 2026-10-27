ROW GR1 VERDICT: holds
SECTION SHA256: fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8

Attack on GR1 of corpus/knowledge/btrfs-scrub-grounding-r45.md at revision
77e9e2b2e96b85d8f048ae2087e246a542b71611 (base 916019057147d7e9ba6b137647b2cee26decf4b8).

Row extent: lines 14-54 of the entry, from `## GR1` up to (exclusive) `## GR2`; no other
`## ` line inside the extent. Counter structural_ok = 1 confirms.

Section hash: `python3 tools/check-scrub-admission-r47.py --revision
77e9e2b2e96b85d8f048ae2087e246a542b71611 --section-hash` prints GR1
fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8 (matches the expected
value). Independent re-derivation: sha256 over the LF-joined entry lines 14..54 (41 lines,
first `## GR1`, last empty) yields the identical digest.

Snapshot digests verified: .ufo/waves/round-45/frozen/src/SHA256SUMS all OK for cmdline.c,
vsprintf.c, kstrtox.c; .ufo/waves/round-44/frozen/src/SHA256SUMS OK for sysfs.c;
.ufo/waves/round-45/frozen/hostcap/capture.txt sha256 =
f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70, matching the entry header.

Clause-by-clause attack (every file:line resolves in the pinned snapshots):

1. "a write to devinfo/<devid>/scrub_speed_max is parsed by memparse ... which calls
   simple_strtoull with base 0" — supported: sysfs.c:2040 `limit = memparse(buf, &endptr);`
   inside btrfs_devinfo_scrub_speed_max_store (sysfs.c:2031-2050); cmdline.c:156
   `unsigned long long ret = simple_strtoull(ptr, &endptr, 0);`.

2. "simple_strtoull resolves base 0 through _parse_integer_fixup_radix, which picks
   hexadecimal for a leading `0x` followed by a hex digit, octal for any other leading `0`,
   and decimal otherwise" — supported: simple_strtoull (vsprintf.c:112-115) calls
   simple_strntoull (vsprintf.c:79), which calls _parse_integer_fixup_radix at
   vsprintf.c:86; the fixup logic at kstrtox.c:26-37 is exactly: kstrtox.c:29
   `if (s[0] == '0') {`, kstrtox.c:30 `if (_tolower(s[1]) == 'x' && isxdigit(s[2]))` ->
   kstrtox.c:31 `*base = 16;`, kstrtox.c:32-33 `else *base = 8;`, kstrtox.c:34-35
   `else *base = 10;`.

3. "at most one suffix letter, K, M, G, T, P or E in either case, each step multiplying by
   a further 1024 (a 10-bit shift per step, so K is 1024, not 1000)" — supported:
   cmdline.c:159-187 is a single `switch (*endptr)` over one character with cases
   E,e/P,p/T,t/G,g/M,m/K,k (cmdline.c:161-183), each level adding 10 via fallthrough
   (cmdline.c:163,167,171,175,179,183); exactly one `endptr++` at cmdline.c:193. So K=2^10,
   M=2^20, ..., E=2^60.

4. "the suffix counts only when at least one digit came before it" — supported: cmdline.c:189
   `if (shl && likely(ptr != endptr)) {` — `ptr != endptr` holds iff simple_strtoull
   consumed at least one digit, because _parse_integer_limit (kstrtox.c:63-91) consumes
   only base-valid [0-9a-f] digits and nothing else (no sign, no prefix; the "0x" prefix is
   skipped inside the fixup only when a hexdigit follows, so a bare "0x" cannot advance the
   end pointer past the prefix either).

5. "a shifted value that overflows becomes ULLONG_MAX" — supported: cmdline.c:191
   `if (unlikely(check_shl_overflow(ret, shl, &ret)))` and cmdline.c:192 `ret = ULLONG_MAX;`.
   The row claims only the shifted case, which is exactly what these lines do; it does not
   overreach into the unshifted KSTRTOX_OVERFLOW path.

6. "The sysfs store then skips whitespace and returns -EINVAL unless the text ends there" —
   supported: sysfs.c:2041 comment, sysfs.c:2042 `endptr = skip_spaces(endptr);`,
   sysfs.c:2043 `if (*endptr != 0)` -> sysfs.c:2044 `return -EINVAL;`.

7. Worked examples all follow from the quoted code:
   - `100M` and `100m` = 100 << 20 = 104857600 (case-insensitive M: cmdline.c:177-179).
   - `010` = 8 (octal fixup kstrtox.c:33), `0x10` = 16 (hex fixup kstrtox.c:30-31).
   - `10MB`: memparse consumes `10` plus one suffix `M` (shl=20), endptr lands on `B`;
     sysfs.c:2043 sees `B` != 0 -> -EINVAL.
   - `10 M`: switch on ` ` hits default, shl stays 0, endptr stays at the blank; skip_spaces
     advances past the blank to `M`, which is != 0 -> -EINVAL.
   - `-1`: _parse_integer_limit has no sign handling (kstrtox.c:66-90), zero digits consumed,
     endptr stays at `-`, skip_spaces does not skip it -> -EINVAL.
   - bare newline: memparse returns 0 with endptr at `\n`; skip_spaces consumes `\n`;
     *endptr == 0 -> accepted and limit written as 0 (sysfs.c:2045-2046).

8. Host reading — supported: capture.txt:8 shows `scrub_speed_max ... mode=644 owner=root
   value=0`; capture.txt:1 shows `uid=1000 CapEff=0000000000000000`. A root-owned mode-0644
   sysfs attribute is not writable by uid 1000 with empty effective capabilities, and
   value=0 corroborates "no limit is set". The row explicitly states "Nothing was written to
   test the parse; the examples above follow from the quoted code" — the examples are
   code-derived, correctly scoped, no false provenance.

Quote verification (receipt: R47CritGR1a/quotes-check.txt): all 12 quoted strings appear on
their cited lines. cmdline.c:147 is a kernel-doc comment line ` *\tpotentially suffixed with
K, M, G, T, P, E.`; the quote reproduces the line's content after the ` *` marker. The
frozen counter checks normalized substring containment, which is a faithful-excerpt rule, so
this is sound quoting, not a defect. The counter independently reports GR1 quotes 12/12 ok,
bad=[] (receipt: R47CritGR1a/counter-gr1.json).

Inference marks: the GR1 statement carries no [inference] markers of its own; the two "(SR8)"
references carry the round-44 inference for "0 means no limit", declared in the entry header
scope. No clause states as fact anything beyond the quoted lines: every behavioural sentence
maps to a cited line or to the composition of cited lines shown above.

Counter legs at this revision: structural_ok=1, GR1 quotes 12/12, citations_ok=true,
citation_problems=[] (receipt: R47CritGR1a/counter-gr1.json).

No clause overreaches and no central clause is false. Verdict: holds.
