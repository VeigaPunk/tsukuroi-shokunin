VERDICT: supports

Opener of record for S246 at freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`. `corpus/SOURCES.md:255` (freeze `git show`, and the worktree line is byte-identical). `SOURCES.md` was not edited. Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ScoutCmd/` was removed after receipts were copied.

## 1. Fetch

Registry URL, copied from the S246 source cell: `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/lib/cmdline.c?h=v7.2.11`. `curl -fsSL --max-time 60` on 2026-10-28 (`date -u +%F`; clock `2026-10-28T17:20:18Z`): HTTP/2 200, `redirects=0`, `url_effective` equal to that URL, no `Location` header, `content-type: text/html; charset=UTF-8`, 25487 bytes. That response is the cgit page, not the pinned C bytes, so it was not `cmp`'d to the snapshot.

Byte URLs (the `plain/` form recorded in `.ufo/waves/round-45/frozen/src/FETCH.txt`, same tag query). Each `curl -fsSL --max-time 60 -D` on 2026-10-28: HTTP/2 200, `redirects=0`, `url_effective` equal to the request URL, no `Location`, `content-type: text/plain; charset=UTF-8`.

| file | URL | bytes | sha256 |
|---|---|---|---|
| cmdline.c | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/cmdline.c?h=v7.2.11` | 6330 | `1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d` |
| vsprintf.c | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/vsprintf.c?h=v7.2.11` | 92345 | `cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca` |
| kstrtox.c | `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/lib/kstrtox.c?h=v7.2.11` | 11483 | `0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4` |

`cmp -s` of each live body against `git show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:.ufo/waves/round-45/frozen/src/<file>`: identical (cmdline.c, vsprintf.c, kstrtox.c). Those three digests are the ones in the S246 anchor cell and in `.ufo/waves/round-45/frozen/src/SHA256SUMS` at the freeze.

`git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git refs/tags/v7.2.11 refs/tags/v7.2.11^{}`:

```
8316c24ec1b77dba19ba072ca4fe251b36dc65d3	refs/tags/v7.2.11
a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea	refs/tags/v7.2.11^{}
```

Same tag object and same peel as `FETCH.txt` and the S246 anchor (`a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`). `v7.2.11` is an annotated tag, not a branch; it has not moved.

Receipts: `.ufo/waves/round-49/w1/R49ScoutCmd/fetch.txt` and the four `*.hdr` files beside it.

## 2. Anchors in the live bytes

Live file equals the pin, so these line numbers are the live file's.

- `simple_strtoull(ptr, &endptr, 0)` in `memparse`: `cmdline.c:156` (function `memparse` at 153-200). Quote (8 words): `unsigned long long ret = simple_strtoull(ptr, &endptr, 0);`. Other `simple_strtoull` calls in this file (lines 64 and 66) are not `memparse`.

- Suffix switch: `cmdline.c:160-187`. Quote of lines 160-163 (10 words): `switch (*endptr) { case 'E': case 'e': shl += 10;`. The same `shl += 10` then `fallthrough` continues for `P`/`p` (165-168), `T`/`t` (169-172), `G`/`g` (173-176), `M`/`m` (177-180) and `K`/`k` (181-184); `default: break` is 185-186. Quote of the last arm, lines 181-183 (7 words): `case 'K': case 'k': shl += 10;`.

- `_parse_integer_fixup_radix` call on the `memparse` path: `vsprintf.c:86`, inside `simple_strntoull` (79-101). Quote (4 words): `cp = _parse_integer_fixup_radix(startp, &base);`. `simple_strtoull` (112-115) returns `simple_strntoull(cp, endp, base, INT_MAX);` (line 114). The function itself is `kstrtox.c:26`. A second call at `kstrtox.c:108` is not this path.

- `*base = 8` / `_tolower(s[1]) == 'x'`, the lines GR1 quotes: `kstrtox.c:30` and `kstrtox.c:33`, in `_parse_integer_fixup_radix` (26-40). Quote of line 30 (6 words): `if (_tolower(s[1]) == 'x' && isxdigit(s[2]))`. Quote of line 33 (3 words): `*base = 8;`. The true arm on line 31 is `*base = 16;`; line 35 is `*base = 10;`.

GR1's other S246 quote lines in `corpus/knowledge/btrfs-scrub-grounding-r45.md:27-45` (cmdline.c 147, 156, 159, 189, 191, 192; vsprintf.c 86; kstrtox.c 29, 30, 33) sit on those same live lines. Line 147 still reads `potentially suffixed with K, M, G, T, P, E.`

## 3. Cadence and pins

`status` `mined`, `opened` `2026-10-27`, `recheck` `on-release`, and `used-by` `corpus/knowledge/btrfs-scrub-grounding-r45.md` still read right: `on-release` fits an annotated tag that still peels to `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`, the three sha256 pins equal the live plain bytes, and that used-by file still cites S246 (`btrfs-scrub-grounding-r45.md:1` and the GR1 quotes).

## 4. Proposed `status` / `recheck` / `used-by` change

no change
