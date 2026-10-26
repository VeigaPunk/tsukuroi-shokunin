VERDICT: holds
ROW: PA8
lines checked: frozen/src/version.c:39-75,219-260

Row read at commit 9cc9aa77e30e0e23de2d4d2697b3b218ada02969 (`git show 9cc9aa7…:corpus/knowledge/alpm-package-anatomy-r41.md`, 62-line file). PA8 rule cell: "libalpm compares two full versions in three steps: the epoch first, an absent epoch counting as 0, then the version, and the release only when both strings carry one; so any epoch 1 build outranks every epoch 0 build and `1.0` equals `1.0-5`".

## Snapshot and live-source identity
- `sha256sum -c SHA256SUMS` in `.ufo/waves/round-41/frozen/src/` → all 9 entries OK, including `fa769e3081d25d74132109ca35a1e272a44b1c5674c397f3f2a1acaf3b6ab833  version.c`.
- Live fetch 2026-10-26: `curl -fsSL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/version.c` → sha256 `fa769e30…b6ab833`, byte-identical to the frozen snapshot (`diff -q` silent, echo LIVE-EQUALS-FROZEN). `frozen/src/FETCH.txt:1,5` records the same URL fetched 2026-10-26.

## Rule cell vs code, clause by clause (all line refs = .ufo/waves/round-41/frozen/src/)
- "the epoch first": `version.c:249` `ret = rpmvercmp(epoch1, epoch2);` is the first comparison in `alpm_pkg_vercmp` (219-260).
- "an absent epoch counting as 0": `parseEVR` `version.c:39-75` — with no leading `[0-9]*:` prefix it takes the else branch: comment `/* different from RPM- always assume 0 epoch */` at `:61` and `epoch = "0"` at `:62`; an empty epoch (`:1.0`) also becomes `"0"` at `:57-59`. Document side agrees: PKGBUILD.5.asciidoc `*epoch*` block exactly 67-74, "default value if left unspecified is '0'" at `:71`.
- "then the version": `version.c:250-251` — `rpmvercmp(ver1, ver2)` runs only `if(ret == 0)` after the epoch compare, so the ordering is real short-circuit order.
- "the release only when both strings carry one": `version.c:252` `if(ret == 0 && rel1 && rel2)`; `parseEVR` sets `release = NULL` when the string carries no '-' (`version.c:68-70`).
- "any epoch 1 build outranks every epoch 0 build": consequence of `:249-250`; measured in the capture — `vercmp 1:1.0-1 2.0-1 = 1`, `vercmp 1.0-1 1:0.1-1 = -1`, `vercmp 2:0.1 1:9.9 = 1` (`frozen/hostcap/vercmp.txt:1,3,6`).
- "`1.0` equals `1.0-5`": epochs both "0", versions equal, `rel1` NULL so the release compare is skipped → 0 (`version.c:249-255`); measured `vercmp 1.0 1.0-5 = 0` (`vercmp.txt:4`).
- No clause overstates the code. The NULL-input and identical-string guards (`version.c:227-237`) sit outside "compares two full versions" and hide no condition the rule states differently.

## Source cell
- Cites S233 `version.c:39-255` with quote "/* different from RPM- always assume 0 epoch */". The quote is present at `version.c:61`, inside the cited range, which covers `parseEVR` (39-75) and the full comparison chain (249-255). `corpus/SOURCES.md:242` at 9cc9aa7 defines S233 with the same snapshot sha256 `fa769e30…` and ranges parseEVR 39-75 / alpm_pkg_vercmp 219-260 — both confirmed by raw reads.

## Host cell (stated as measured, and measured)
- The three quoted outputs are verbatim at `frozen/hostcap/vercmp.txt:1,2,4`; capture.sh:26-31 generated them by invoking `vercmp` directly (no sudo, no transaction); `sha256sum -c MANIFEST.sha256` in `frozen/hostcap/` → all 6 files OK; `capture-meta.txt:1-2`: captured 2026-10-26T16:14:04Z on pacman 7.1.0.r9.g54d9411-3.
- I reproduced the run 2026-10-26 (`for p in …; vercmp "$1" "$2"`): all six outputs identical to `vercmp.txt:1-6`; `pacman -Qo /usr/bin/vercmp` → "/usr/bin/vercmp is owned by pacman 7.1.0.r9.g54d9411-3", i.e. the pinned build. The cell claims nothing unmeasured; the entry states unmeasured only for PA2/PA3, consistent with its QUALITY 86 line.
- The supporting-note pointers behind PA8 check out exactly: PKGBUILD.5.asciidoc:67-74 is the `*epoch*` block and :439-441 is "Scripts are passed either one or two ``full version strings'', where a full version string is either 'pkgver-pkgrel' or 'epoch:pkgver-pkgrel', if epoch is non-zero." (raw reads; S232 at `corpus/SOURCES.md:241` cites the same two ranges).

## Residual gaps
- Only row PA8 judged (assignment scope): no other row, no counter run, no edits to tracked lane files, no tools installed.

Receipts: `.ufo/waves/round-41/w1/C2RevPA8/` (evidence-log.txt, live-version.c).
