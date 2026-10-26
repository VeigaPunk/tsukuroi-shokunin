#!/bin/bash
# Ordering matrix for makepkg list_package_files body (frozen 54d9411 makepkg.sh.in:562-569).
# Everything under /fast/scratch/hyaku/tsukuroi-r41/C2LabratOrder ; no host writes.
set -u
B=/fast/scratch/hyaku/tsukuroi-r41/C2LabratOrder
echo "## bash $BASH_VERSION"
echo "## PATH bash: $(command -v -a bash | tr '\n' ' ')"

list_package_files() {
	(
		export LC_COLLATE=C
		shopt -s dotglob globstar
		# bash 5.0 only works with combo directory + file globs
		printf '%s\0' **/*
	)
}
show() { list_package_files | tr '\0' '\n' | nl -ba; }

# ---------- B: legal top-level names with first byte below '.' (0x2E) ----------
TB=$B/treeB; rm -rf "$TB"; mkdir -p "$TB/A" "$TB/_x" "$TB/Zeta" "$TB/usr/bin"
cd "$TB" || exit 1
for f in .BUILDINFO .INSTALL .MTREE .PKGINFO A/data _x/f Zeta/g usr/bin/hello \
         -dash +plus '!bang' ' spaces' '#hash' '$dollar' '%pct' '&amp' "'quote" \
         '(open' ')close' '*star' ',comma' '"dq' 0digit 9nine ';semi' '=eq' '@at' '~tilde' '^caret' '`tick`'; do
	printf 'x' > "$f"
done
printf 'x' > $'\t'tabname
printf 'x' > $'\n'newname
echo
echo "## treeB top-level entries as bytes (LC_ALL=C sort):"
printf '%s\n' * .[!.]* | LC_ALL=C sort | head -40 | cat -A | sed -n '1,40p'
echo
echo "## treeB: body order (numbered; cat -A shows control bytes):"
list_package_files | tr '\0' '\n' | nl -ba | head -30 | cat -A
echo
echo "## treeB: how many body entries have a first byte < 0x2E at top level:"
list_package_files | tr '\0' '\n' | grep -v / | LC_ALL=C awk '{c=substr($0,1,1); printf "%s %d\n", $0, index(" !\"#$%&\047()*+,-", c)}' | LC_ALL=C awk '$NF>0' | cat -A

# ---------- C: is **/* globally C-sorted or a sorted depth-first walk? ----------
TC=$B/treeC; rm -rf "$TC"; mkdir -p "$TC/ab"; cd "$TC" || exit 1
printf 'x' > ab/x; printf 'x' > ab.x; printf 'x' > .PKGINFO; printf 'x' > ab0
echo
echo "## treeC body order:"
show
echo "## treeC global LC_ALL=C sort of same names:"
list_package_files | tr '\0' '\n' | LC_ALL=C sort | nl -ba

# ---------- D: locale sensitivity of the body ----------
TD=$B/treeA; cd "$TD" || exit 1
echo
echo "## treeA under LC_COLLATE=C (body as shipped):"
show
echo "## treeA same glob with LC_COLLATE=en_US.UTF-8 (no export of C):"
( export LC_COLLATE=en_US.UTF-8; shopt -s dotglob globstar; printf '%s\n' **/* ) | nl -ba
echo "## glibc sort keys under en_US.UTF-8 (sort -f? plain):"
printf '%s\n' * | LC_ALL=en_US.UTF-8 sort | nl -ba

# ---------- E: bsdtar end-to-end on treeB ----------
cd "$TB" || exit 1
echo
echo "## bsdtar archive built exactly as create_package does (--null --files-from -), member order:"
list_package_files | LANG=C bsdtar --no-fflags -cnf "$B/B.tar" --null --files-from -
bsdtar -tf "$B/B.tar" | nl -ba | head -30
echo "## .MTREE step (format=mtree, --exclude .MTREE) first 8 lines:"
list_package_files | LANG=C bsdtar -cnf - --format=mtree \
	--options='!all,use-set,type,uid,gid,mode,time,size,sha256,link' \
	--null --files-from - --exclude .MTREE | gzip -c -f -n > "$B/B.mtree.gz"
zcat "$B/B.mtree.gz" | sed -n '1,8p'
echo "## extract leading-dash and control-byte members from B.tar:"
mkdir -p "$B/x"; ( cd "$B/x" && bsdtar -xf "$B/B.tar" && ls -A | head -5 && echo "EXTRACT_OK" )
