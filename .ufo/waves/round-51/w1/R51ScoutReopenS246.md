VERDICT: supports

S246 re-opened live at Linux tag v7.2.11. `lib/cmdline.c`, `lib/vsprintf.c` and `lib/kstrtox.c` are byte-identical to the round-45 snapshots and to the pin digests. Every cited line equals the snapshot line and sits inside the SOURCES.md anchor ranges. The freeze `--emit-gaps` block has no S246 line, matching that empty outside set.

Access window (UTC): 2026-10-28T21:13:53Z through 2026-10-28T21:13:54Z. Each response header says `date: Wed, 28 Oct 2026 21:13:54 GMT` (receipts `cmdline.c.headers`, `vsprintf.c.headers`, `kstrtox.c.headers`). No tools installed.

## Live fetch

Commands (cwd scratch, removed after copy; `curl --max-time 120`, rc 0 each):

- `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/cmdline.c?h=v7.2.11`
- `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/vsprintf.c?h=v7.2.11`
- `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/kstrtox.c?h=v7.2.11`

| file | bytes | lines | sha256 |
|---|---:|---:|---|
| cmdline.c | 6330 | 285 | `1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d` |
| vsprintf.c | 92345 | 3746 | `cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca` |
| kstrtox.c | 11483 | 442 | `0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4` |

`sha256sum` of the three snapshots under `.ufo/waves/round-45/frozen/src/` printed the same three digests. Those digests are the pins in that directory's `SHA256SUMS` (cmdline.c, vsprintf.c, kstrtox.c) and in `tools/lint-grounding-r51.py` `SNAPSHOTS['S246']`. `cmp -s` printed `BYTE_IDENTICAL` for each pair. `diff -q` printed no stdout and exited 0 for each pair, so there is no differing-line diff.

Receipts (lane-relative): `.ufo/waves/round-51/w1/R51ScoutReopenS246/live-cmdline.c`, `live-vsprintf.c`, `live-kstrtox.c`.

## Cited lines (live bytes)

Declared anchor, `git show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/SOURCES.md` line 255, anchor cell: cmdline.c 142-201, vsprintf.c 79-115, kstrtox.c 26-40. A line-by-line compare of the live files against the snapshots (`line-compare.txt`) marked every line below `EQUAL` and `INSIDE`. Summary line: `OUTSIDE (none)`.

cmdline.c 147-192 (all inside 142-201). Python `repr` of the live line:

- 147 `' *\tpotentially suffixed with K, M, G, T, P, E.'`
- 148 `' *'`
- 149 `' *\tReturn: The value as recognized by simple_strtoull() multiplied'`
- 150 `' *\tby the value as specified by suffix, if any.'`
- 151 `' */'`
- 152 `''`
- 153 `'unsigned long long memparse(const char *ptr, char **retptr)'`
- 154 `'{'`
- 155 `'\tchar *endptr;\t/* local pointer to end of parsed string */'`
- 156 `'\tunsigned long long ret = simple_strtoull(ptr, &endptr, 0);'`
- 157 `'\tunsigned int shl = 0;'`
- 158 `''`
- 159 `'\t/* Consume valid suffix even in case of overflow. */'`
- 160 `'\tswitch (*endptr) {'`
- 161 `"\tcase 'E':"`
- 162 `"\tcase 'e':"`
- 163 `'\t\tshl += 10;'`
- 164 `'\t\tfallthrough;'`
- 165 `"\tcase 'P':"`
- 166 `"\tcase 'p':"`
- 167 `'\t\tshl += 10;'`
- 168 `'\t\tfallthrough;'`
- 169 `"\tcase 'T':"`
- 170 `"\tcase 't':"`
- 171 `'\t\tshl += 10;'`
- 172 `'\t\tfallthrough;'`
- 173 `"\tcase 'G':"`
- 174 `"\tcase 'g':"`
- 175 `'\t\tshl += 10;'`
- 176 `'\t\tfallthrough;'`
- 177 `"\tcase 'M':"`
- 178 `"\tcase 'm':"`
- 179 `'\t\tshl += 10;'`
- 180 `'\t\tfallthrough;'`
- 181 `"\tcase 'K':"`
- 182 `"\tcase 'k':"`
- 183 `'\t\tshl += 10;'`
- 184 `'\t\tfallthrough;'`
- 185 `'\tdefault:'`
- 186 `'\t\tbreak;'`
- 187 `'\t}'`
- 188 `''`
- 189 `'\tif (shl && likely(ptr != endptr)) {'`
- 190 `'\t\t/* Have valid suffix with preceding number. */'`
- 191 `'\t\tif (unlikely(check_shl_overflow(ret, shl, &ret)))'`
- 192 `'\t\t\tret = ULLONG_MAX;'`

vsprintf.c:86, inside 79-115: `'\tcp = _parse_integer_fixup_radix(startp, &base);'`

kstrtox.c 29-33, inside 26-40:

- 29 `"\t\tif (s[0] == '0') {"`
- 30 `"\t\t\tif (_tolower(s[1]) == 'x' && isxdigit(s[2]))"`
- 31 `'\t\t\t\t*base = 16;'`
- 32 `'\t\t\telse'`
- 33 `'\t\t\t\t*base = 8;'`

Whitespace-collapsed, the ten GR1 S246 quotes in the freeze entry match these live lines (`quote_norm_match=True` in `line-compare.txt`). Entry quotes: `git show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/knowledge/btrfs-scrub-grounding-r45.md` lines 27, 29, 31, 33, 35, 37, 39, 41, 43, 45. Line 147's collapsed form is `* potentially suffixed with K, M, G, T, P, E.` (the `* ` leader is present).

## Range gaps

Lines outside the anchor ranges, among cmdline.c 147-192, vsprintf.c 86 and kstrtox.c 29-33: none.

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/lint-grounding-r51.py --revision 2732ee6c06108c031c4d8043239b994e0504eb2f --emit-gaps` wrote this block (rc 0; that flag returns 0 after printing, `tools/lint-grounding-r51.py` lines 307-309 — this seat did not run the lint verdict mode):

```
### Range gaps (R51)

- S237 scrub.c: 421, 439, 1546
- S240 ioctl.c: 3080, 3084-3085, 3088, 3093, 3109-3110, 3115, 3190
- S242 scrub.c: 3081, 3094-3139
- S243 sysfs.c: 1288, 2015
- S247 dev-replace.c: 1197
```

No S246 line. The same block is the entry's `### Range gaps (R51)` at grounding lines 269-275. The empty outside set for S246 agrees with that block.

## Gate

Access date: 2026-10-28

URL: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/cmdline.c?h=v7.2.11
sha256: 1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d

URL: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/vsprintf.c?h=v7.2.11
sha256: cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca

URL: https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/kstrtox.c?h=v7.2.11
sha256: 0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4

Quote (live `lib/cmdline.c:147`, 10 words, verbatim; GR1 line 27 rests on it): ` *	potentially suffixed with K, M, G, T, P, E.`

Python repr of that line: `' *\tpotentially suffixed with K, M, G, T, P, E.'`

## Not done

Did not fetch the registry `tree/` URL (HTML). Did not re-peel tag v7.2.11 to commit `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`. Did not run `lint-grounding-r51.py` without `--emit-gaps`, and did not run the admission counter. No differing-line `diff` because `diff -q` and `cmp -s` both reported identical files.
