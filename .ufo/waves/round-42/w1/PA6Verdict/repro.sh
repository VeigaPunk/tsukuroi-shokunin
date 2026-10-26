#!/bin/bash
# PA6Verdict round-42 w1 — first-hand reproduction of PA6 runtime claims.
# Read-only pacman queries with --dbpath/--root pointing into scratch. No installs.
set -u
S=/fast/scratch/hyaku/tsukuroi-r42/PA6Verdict
FIX="$S/fix"
rm -rf "$FIX" "$S/pkg" "$S/foo-1.0-1-x86_64.pkg.tar.gz"
mkdir -p "$FIX/db/local/foo-1.0-1" "$FIX/root/usr/bin"

cp /var/lib/pacman/local/ALPM_DB_VERSION "$FIX/db/local/ALPM_DB_VERSION"

printf '%%NAME%%\nfoo\n\n%%VERSION%%\n1.0-1\n\n%%BASE%%\nfoo\n' > "$FIX/db/local/foo-1.0-1/desc"
printf '%%FILES%%\nusr/\nusr/bin/\nusr/bin/foo\n' > "$FIX/db/local/foo-1.0-1/files"
echo 'content' > "$FIX/root/usr/bin/foo"

MTREE_OPTS='!all,use-set,type,uid,gid,mode,time,size,sha256,link'

echo "== P1: -Qkk, kept mtree ABSENT =="
pacman -Qkk --dbpath "$FIX/db" --root "$FIX/root" --color never foo
echo "rc=$?"

echo "== P2: -Qkk --quiet, kept mtree ABSENT =="
pacman -Qkk --dbpath "$FIX/db" --root "$FIX/root" --color never --quiet foo
echo "rc=$?"

echo "== P3: -Qk (level 1), kept mtree ABSENT =="
pacman -Qk --dbpath "$FIX/db" --root "$FIX/root" --color never foo
echo "rc=$?"

echo "== P4: -Qkk, kept mtree PRESENT but unopenable =="
printf 'not an mtree at all\n' > "$FIX/db/local/foo-1.0-1/mtree"
pacman -Qkk --dbpath "$FIX/db" --root "$FIX/root" --color never foo
echo "rc=$?"
rm -f "$FIX/db/local/foo-1.0-1/mtree"

# package file fixture with a readable .MTREE (makepkg recipe, makepkg.sh.in:615-618)
mkdir -p "$S/pkg/usr/bin"
echo 'content' > "$S/pkg/usr/bin/foo"
printf 'pkgname = foo\npkgbase = foo\npkgver = 1.0-1\npkgarch = x86_64\n' > "$S/pkg/.PKGINFO"
echo 'buildinfo' > "$S/pkg/.BUILDINFO"
(cd "$S/pkg" && printf '%s\0' .BUILDINFO .PKGINFO usr usr/bin usr/bin/foo \
  | LANG=C bsdtar -cnf - --format=mtree --options="$MTREE_OPTS" --null --files-from - --exclude .MTREE) \
  | gzip -c -f -n > "$S/pkg/.MTREE"
(cd "$S/pkg" && LANG=C bsdtar -czf "$S/foo-1.0-1-x86_64.pkg.tar.gz" .BUILDINFO .PKGINFO .MTREE usr)
echo "-- archive members:"
LANG=C bsdtar -tf "$S/foo-1.0-1-x86_64.pkg.tar.gz"

echo "== P5: -Qpl on the archive (filelist parsed from the archive's .MTREE) =="
pacman -Qpl --dbpath "$FIX/db" --root "$FIX/root" --color never "$S/foo-1.0-1-x86_64.pkg.tar.gz"
echo "rc=$?"

echo "== P6: -Qpkk on the same archive (notice although .MTREE present) =="
pacman -Qpkk --dbpath "$FIX/db" --root "$FIX/root" --color never "$S/foo-1.0-1-x86_64.pkg.tar.gz"
echo "rc=$?"

echo "== P7: -Qpkk --quiet on the same archive =="
pacman -Qpkk --dbpath "$FIX/db" --root "$FIX/root" --color never --quiet "$S/foo-1.0-1-x86_64.pkg.tar.gz"
echo "rc=$?"

echo "== P8: -Qkk with no target over the db holding only the mtree-less package =="
pacman -Qkk --dbpath "$FIX/db" --root "$FIX/root" --color never
echo "rc=$?"

echo "== P9: positive control — valid kept mtree, tampered root file =="
(cd "$FIX/root" && printf '%s\0' usr usr/bin usr/bin/foo \
  | LANG=C bsdtar -cnf - --format=mtree --options="$MTREE_OPTS" --null --files-from -) \
  | gzip -c -f -n > "$FIX/db/local/foo-1.0-1/mtree"
printf 'tampered\n' >> "$FIX/root/usr/bin/foo"
pacman -Qkk --dbpath "$FIX/db" --root "$FIX/root" --color never foo
echo "rc=$?"
