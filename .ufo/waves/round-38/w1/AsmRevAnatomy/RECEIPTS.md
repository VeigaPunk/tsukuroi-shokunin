# Receipts — seat AsmRevAnatomy (round 38, item A-6)

All four sources fetched 2026-10-26 (today) with `curl -fsSL` into seat scratch, copied here verbatim.

| File | URL | sha256 | bytes |
|---|---|---|---|
| `alpm-package.7.html` | https://man.archlinux.org/man/alpm-package.7 | 05ce740ecce3e79eeed22f4a30ca2d5b6fd4f401e8d98152c23e86312cae57b1 | 15643 |
| `PKGBUILD.5.html` | https://man.archlinux.org/man/PKGBUILD.5 | af56d68912cf8e83dffc72ec5c5ccf164e2af91606242ebaacc68ff6dd7c8529 | 37656 |
| `PKGBUILD.5.asciidoc-at-54d9411` | https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/PKGBUILD.5.asciidoc | 15e8007bb11829b4d0474e647b0d08c2bffdf5191ceac949336de3d14a621154 | 22840 |
| `makepkg.sh.in-at-54d9411` | https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/scripts/makepkg.sh.in | d588222586b2432b4169c82e6ebcd464acfdc20a663172fd444b8f98e1104e86 | 40453 |

Version footers observed in today's fetches:
- `PKGBUILD.5.html:606-607` — foot-date `2026-10-15`, foot-os `Pacman 7.1.0` (matches the staged S217 anchor).
- `alpm-package.7.html:278-287` — package `extra/alpm-docs`, version `0.13.0-1`, upstream `https://alpm.archlinux.page/` (matches the staged S215 anchor).

Reviewed bytes (sha256, recorded at review time):

| File | sha256 |
|---|---|
| shokuknow merge staged entry `alpm-package-anatomy-r26.md` (62 lines) | 3fa1b8098ee3398c4587f012bd84455f893a66d2a7ee00647c31279a0172d1a7 |
| shokuknow merge staged sibling `pacman-hook-timing-r25.md` | e18c146e733d3cab4bcc82c2ba30b9a571791ec132f7988cd93481b079f09324 |
| shokuknow merge `SOURCES.append.md` | 7914d3b93cea2015c00091d7db28ca2acd289d5097cb513ad1176dc0d7148406 |
| lane `corpus/QUALITY.md` | 40ea1f8a00151ec618e4962c3eab18fb2749fb7a424ff6c97a13e4a8aa28dc28 |
| lane `corpus/README.md` | a0b998a6dc46e981220946cad3f52873b14a536e0e6b7ed0e62e265f2f92bdaa |
| lane `corpus/SOURCES.md` | 516c1be45553754caa678a72f63427d63b879bb3722319248e755687411330c7 |
| lane `PROVINCE.md` | 1374f6583195c7b5a9d74079c3e7593dc8becb0bf3a8bc14c0de80ba0d1ccf7f |
| lane `corpus/knowledge/pacman-backup-files-r35.md` | 5853157ac4e17fd8dd3410c5eb6f8a8a733d0c6d9b508e8f9ef2c1307c3d24e5 |
| lane `corpus/lessons/round-37.md` | 7b4953823ffd1f4a4be2a2104ea581b2f586bce293f03af11240c609f2d21127 |
| lane `corpus/knowledge/pacman-hook-order-r38.md` | b56c90f1ebbdfa3d07f369e39b7580d6b0050da69eb9d4d2b560b58771c73f61 |

No tool was installed or upgraded (operator tooling authorization of 2026-10-19 unused; `curl`/`sha256sum` already present). Scratch `/fast/scratch/hyaku/tsukuroi-r38/AsmRevAnatomy` removed after this dir was populated.
