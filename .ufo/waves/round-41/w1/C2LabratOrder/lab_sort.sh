#!/bin/bash
# Decisive test: is the **/* order a global C sort of full paths, or a
# per-directory grouped walk? Discriminator: root has dir A (child b), and
# files A-b and A.b.  Global C sort -> A, A-b, A.b, A/b
# walk-grouped        -> A, A/b, A-b, A.b
set -u
B=/fast/scratch/hyaku/tsukuroi-r41/C2LabratOrder
TD=$B/treeD; rm -rf "$TD"; mkdir -p "$TD/A"; cd "$TD" || exit 1
printf 'x' > A/b; printf 'x' > A-b; printf 'x' > A.b
printf 'x' > .PKGINFO
echo "## bash $BASH_VERSION ; PWD=$PWD"
echo "## body order (globstar+dotglob, LC_COLLATE=C):"
( export LC_COLLATE=C; shopt -s dotglob globstar; printf '%s\n' **/* ) | nl -ba
echo "## global LC_ALL=C sort of the same names:"
( export LC_COLLATE=C; shopt -s dotglob globstar; printf '%s\n' **/* ) | LC_ALL=C sort | nl -ba
echo "## identical to global sort?"; diff -q \
  <( export LC_COLLATE=C; shopt -s dotglob globstar; printf '%s\n' **/* ) \
  <( export LC_COLLATE=C; shopt -s dotglob globstar; printf '%s\n' **/* | LC_ALL=C sort ) \
  && echo YES-GLOBALLY-SORTED || echo NO
# deeper discriminator: dir A/b/ (dir) with child zz, and file A/b.c
# global: A, A-b, A.b, A/b, A/b.c, A/b/zz ; grouped: A, A/b, A/b/zz, A-b, A.b
mkdir -p A/b; printf 'x' > A/b/zz; printf 'x' > A/b.c
echo "## deeper treeD body order:"
( export LC_COLLATE=C; shopt -s dotglob globstar; printf '%s\n' **/* ) | nl -ba
echo "## deeper global sort:"
( export LC_COLLATE=C; shopt -s dotglob globstar; printf '%s\n' **/* ) | LC_ALL=C sort | nl -ba
