# C2RevEX7 receipts — 2026-10-26 (seat C2RevEX7, item C2-EX7)

## Upstream re-fetch
Scratch: /fast/scratch/hyaku/tsukuroi-r40/C2RevEX7/upstream (removed after receipts copied).
Access window (date -u): start 2026-10-26T07:15:31Z, end 2026-10-26T07:15:36Z.
URLs:
- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/hook.c
- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/trans.c
- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/util.c
- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/alpm-hooks.5.asciidoc
- https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/meson_options.txt
- https://gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/raw/7.1.0.r9.g54d9411-3/PKGBUILD

sha256 of fetched files (all six equal .ufo/waves/round-40/frozen/src/SHA256SUMS):
```
32d40dfd36919597b3d5b57c74d7f87ca8c463a7d10c00a87ff2149aa9ba67f4  PKGBUILD
2970cb35115a32a5d8a9652dfd795ad535d9354c36039fcc0d25929d9c3493d3  alpm-hooks.5.asciidoc
99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a  hook.c
89e5b350af2831f591334a580bfd08360f65aaff40336d6e677f5e956b55a65b  meson_options.txt
637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07  trans.c
381618b6054859ec76807956328b78b330237273bebe10022a559b243cb5bdd2  util.c
```
Supplementary fetches (not in SHA256SUMS; used only to confirm satisfier and log-surface semantics):
```
e42e6c015dbe22107b2f79bf4137fa550a16c83ad4eaffd785cba5f750b34e56  deps.c      (lib/libalpm/deps.c @ 54d9411)
9dadcc56465888f4fbd8e6bf69036296359f12ccc15d79f8e367d2506f7c2ce6  callback.c  (src/pacman/callback.c @ 54d9411)
1133b633a3bcf16971a77d5cc0bc1ee6a66132c7d4eb6f8812a1e17caf950558  log.c       (lib/libalpm/log.c @ 54d9411)
```

## Frozen pin integrity
`sha256sum -c .ufo/waves/round-40/frozen/src/SHA256SUMS` → PKGBUILD OK, alpm-hooks.5.asciidoc OK,
hook.c OK, meson_options.txt OK, trans.c OK, util.c OK (6/6).

## Revision check (lane, read-only)
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD`
→ f951f288483c1af0cef4afd458488b84cf7a2165
`git diff --stat f951f288483c1af0cef4afd458488b84cf7a2165 -- corpus/knowledge/pacman-exec-environment-r40.md`
→ empty output, exit 0 (judged row == row at dispatch revision).

## Quote byte-check (hook.c:513-514 joined with space, leading `_alpm_log(handle, ALPM_LOG_ERROR, ` outside quote)
```
joined: _alpm_log(handle, ALPM_LOG_ERROR, _("unable to run hook %s: %s\n"), hook->name, _("could not satisfy dependencies"));
QUOTE-VERBATIM-AT-513-514
```

## Host log check (read-only)
`grep -c 'could not satisfy dependencies' /var/log/pacman.log` → `0` (grep exit 1 = no match), run 2026-10-26.

## SOURCES cross-ref (read-only)
corpus/SOURCES.md:232 = S223 hook.c @54d9411, snapshot sha256 99f1044b…; :233 = S224
alpm-hooks.5.asciidoc @54d9411, snapshot sha256 2970cb35…. Both match the fetched hashes.
