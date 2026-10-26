#!/bin/bash
# C2LabratArchive / round 41 / item C2-28 — exact recipe for the PA2 labrat probes.
# Everything runs under /fast/scratch/hyaku/tsukuroi-r41/C2LabratArchive (removed after the run).
# No pacman transaction, no install, no sudo: only `pacman -Qpi` / `-Qpl` (read-only file queries).
set +e
S=/fast/scratch/hyaku/tsukuroi-r41/C2LabratArchive
mkdir -p "$S/build/root/usr/share/toy"
cd "$S/build"
printf 'pkgname = toy\npkgver = 1.0-1\narch = any\npkgdesc = toy package for PA2 labrat\nurl = https://example.invalid/toy\nsize = 3\n' > .PKGINFO
printf 'toy data\n' > root/usr/share/toy/data.txt

# A — .PKGINFO only, no .BUILDINFO/.MTREE, .PKGINFO first
bsdtar -cf "$S/A-min-no-buildinfo-no-mtree.pkg.tar" -C "$S/build" .PKGINFO -C "$S/build/root" usr/share/toy/data.txt
# B — no .PKGINFO at all
bsdtar -cf "$S/B-nometa.pkg.tar" -C "$S/build/root" usr/share/toy/data.txt
# C — pkgver without a dash
printf 'pkgname = toy\npkgver = 1.0\narch = any\npkgdesc = toy without dash\nsize = 3\n' > .PKGINFO.badver
cp .PKGINFO .PKGINFO.good; cp .PKGINFO.badver .PKGINFO
bsdtar -cf "$S/C-badver.pkg.tar" -C "$S/build" .PKGINFO -C "$S/build/root" usr/share/toy/data.txt
cp .PKGINFO.good .PKGINFO
# D — order test: .PKGINFO last
bsdtar -cf "$S/D-info-last.pkg.tar" -C "$S/build/root" usr/share/toy/data.txt -C "$S/build" .PKGINFO
# E — .BUILDINFO present, no .MTREE
printf 'builddate = 1\npkgname = toy\npkgver = 1.0-1\n' > .BUILDINFO
bsdtar -cf "$S/E-with-buildinfo.pkg.tar" -C "$S/build" .PKGINFO .BUILDINFO -C "$S/build/root" usr/share/toy/data.txt
rm -f .BUILDINFO

# F/G/H — full-load probes: does -Qpi consume .MTREE?
printf '#mtree\n/set type=file uid=0 gid=0 mode=644\n./usr/share/toy/phantom.txt time=1700000000.0 size=7\n' > mt-py.raw
gzip -n -c mt-py.raw > .MTREE.F              # valid mtree listing a file NOT in the archive
printf '#mtree\n/set type=file uid=0 gid=0 mode=644\n' > mt-empty.raw
gzip -n -c mt-empty.raw > .MTREE.G          # valid mtree with no entries
printf 'this is not an mtree\n' > .MTREE.H  # garbage .MTREE
for tag in F G H; do cp ".MTREE.$tag" .MTREE
  bsdtar -cf "$S/$tag-mtree-$tag.pkg.tar" -C "$S/build" .PKGINFO .MTREE -C "$S/build/root" usr/share/toy/data.txt; done
rm -f .MTREE
# I — .INSTALL sets the scriptlet flag
printf 'post_install() { :; }\n' > .INSTALL
bsdtar -cf "$S/I-with-install.pkg.tar" -C "$S/build" .PKGINFO .INSTALL -C "$S/build/root" usr/share/toy/data.txt
rm -f .INSTALL

# J/K/L/N — sibling rejects and exact-name matching
printf 'pkgver = 1.0-1\narch = any\n' > .PKGINFO.J
printf 'pkgname = toy\narch = any\npkgver = \n' > .PKGINFO.K
printf 'pkgname = toy\npkgver = 1:1.0\narch = any\n' > .PKGINFO.N
mk() { cp "$1" .PKGINFO; bsdtar -cf "$S/$2.pkg.tar" -C "$S/build" .PKGINFO -C "$S/build/root" usr/share/toy/data.txt; }
mk .PKGINFO.J J-empty-name; mk .PKGINFO.K K-empty-version; mk .PKGINFO.N N-epoch-nodash
cp .PKGINFO .pkginfo; bsdtar -cf "$S/L-lowercase-info.pkg.tar" -C "$S/build" .pkginfo -C "$S/build/root" usr/share/toy/data.txt; rm -f .pkginfo
# M — unknown key in .PKGINFO
printf 'pkgname = toy\npkgver = 1.0-1\narch = any\ndesc = unknown key\n' > .PKGINFO.M; mk .PKGINFO.M M-cmt-epoch

# P — .MTREE before .PKGINFO
cp .MTREE.F .MTREE; cp .PKGINFO.good .PKGINFO
bsdtar -cf "$S/P-mtree-before-info.pkg.tar" -C "$S/build" .MTREE .PKGINFO -C "$S/build/root" usr/share/toy/data.txt
rm -f .MTREE

# Real makepkg package (offline, no sources, built in scratch) — reference shape
mkdir -p "$S/mk/dest" "$S/mk/build" "$S/mk/src" "$S/mk/tmp"
cd "$S/mk"
cat > PKGBUILD <<'PKG'
pkgname=toyl
pkgver=1.0
pkgrel=1
pkgdesc="toy package built by makepkg for PA2 labrat"
arch=('any')
license=('custom')
source=()
package() {
  install -Dm644 /dev/null "$pkgdir/usr/share/toyl/data.txt"
  printf 'toy data\n' > "$pkgdir/usr/share/toyl/data.txt"
}
PKG
export TMPDIR=$S/mk/tmp
makepkg -f -d --nocheck --nodeps --nosign
mkdir stage && bsdtar -xf "$S/mk/toyl-1.0-1-any.pkg.tar.zst" -C stage
# R — makepkg's own .PKGINFO, .MTREE and .BUILDINFO removed (real shape, zstd)
bsdtar --zstd -cf "$S/R-real-shape-pkginfo-only.pkg.tar.zst" -C stage .PKGINFO usr
# S — same tree without .PKGINFO
bsdtar --zstd -cf "$S/S-real-shape-no-pkginfo.pkg.tar.zst" -C stage usr

# Queries (read-only; no transaction, no install)
for f in "$S"/*.pkg.tar "$S"/*.pkg.tar.zst; do echo "== $f"; pacman -Qpi "$f"; echo "rc=$?"; pacman -Qpl "$f"; echo "rc=$?"; done
