VERDICT: supports

Row S246 live re-open (SRC-SScoutCmdline), accessed 2026-10-28 (UTC). Seats read frozen row from `git show ae99f021b76f8eb1c8805d32d80644464afb1ff6:corpus/SOURCES.md` line 255; GR1 quote lines from frozen `corpus/knowledge/btrfs-scrub-grounding-r45.md`.

## 1. Fetch, access date, digests, identity

- Row URL (SOURCES.md:255): `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/lib/cmdline.c?h=v7.2.11` — fetched 2026-10-28T12:02Z, HTTP 200, `num_redirects=0`, effective URL unchanged (receipt: `w2/SScoutCmdline/redirect.txt`). The row URL is the cgit *tree* page; the pinned byte snapshots come from the `plain/` endpoints recorded in `.ufo/waves/round-45/frozen/src/FETCH.txt`.
- Raw fetches (curl -fsSL --max-time 60, 2026-10-28), `?h=v7.2.11`:
  - `plain/lib/cmdline.c` sha256 `1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d`
  - `plain/lib/vsprintf.c` sha256 `cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca`
  - `plain/lib/kstrtox.c` sha256 `0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4`
  (receipts: `w2/SScoutCmdline/cmdline.c`, `vsprintf.c`, `kstrtox.c`, `live-sha256.txt`)
- Byte-identical to pinned snapshots: `cmp` vs `.ufo/waves/round-45/frozen/src/{cmdline,vsprintf,kstrtox}.c` — all three report identical; hashes match `SHA256SUMS` exactly. Upstream did NOT move: `git ls-remote` shows `refs/tags/v7.2.11` = `8316c24ec1b77dba19ba072ca4fe251b36dc65d3` peeling to `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`, the same peeled commit recorded in FETCH.txt and the SOURCES row. (`v7.2.11` is a tag, not a branch tip.)

## 2. Located anchors in the LIVE bytes (all match GR1 quotes)

- `cmdline.c:147` — "potentially suffixed with K, M, G, T, P, E."
- `cmdline.c:156` — "unsigned long long ret = simple_strtoull(ptr, &endptr, 0);"
- `cmdline.c:159` — "/* Consume valid suffix even in case of overflow. */"
- `cmdline.c:160-185` — memparse suffix switch: `switch (*endptr) { case 'E': ... case 'K':` with `shl += 10` per step (lines 161,163,165,167,169,171,173,175,177,179,181,183).
- `cmdline.c:189` — "if (shl && likely(ptr != endptr)) {"
- `cmdline.c:191` — "if (unlikely(check_shl_overflow(ret, shl, &ret)))"
- `cmdline.c:192` — "ret = ULLONG_MAX;"
- `vsprintf.c:86` — "cp = _parse_integer_fixup_radix(startp, &base);"
- `kstrtox.c:29` — "if (s[0] == '0') {"
- `kstrtox.c:30` — "if (_tolower(s[1]) == 'x' && isxdigit(s[2]))"
- `kstrtox.c:33` — "*base = 8;"

Every GR1 `S246` quote resolves at the same line number in the live bytes with identical text.

## 3. Recheck cadence / pins

The row pins tag v7.2.11 with the peeled commit, both re-verified live today, and the `on-release` recheck cell still reads right: it triggers the exact re-fetch-and-`sha256sum` comparison just performed (FETCH.txt + SHA256SUMS); newer stable tags exist upstream (ls-remote shows v7.2.12, v7.2.13) but the row is pinned to v7.2.11 = the host kernel `7.2.11-arch1-1`, so the pin itself is not stale — only a host kernel upgrade would argue for repinning, which is the `verified-at`/`on-release` cadence working as designed.

## 4. Proposed cell update

`no change` — status `mined`, verified `2026-10-27`, recheck `on-release`, used-by `corpus/knowledge/btrfs-scrub-grounding-r45.md` all still accurate against the live source; nothing is stale. (If the L1 wishes to stamp today's re-verification that is a bookkeeping choice, not a staleness fix.)
