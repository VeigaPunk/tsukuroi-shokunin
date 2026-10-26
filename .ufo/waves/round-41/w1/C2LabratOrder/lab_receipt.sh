#!/bin/bash
# Consolidated ordering receipt, driven by /usr/bin/bash (bash $BASH_VERSION).
set -u
B=/fast/scratch/hyaku/tsukuroi-r41/C2LabratOrder
echo "## bash $BASH_VERSION  ($(command -v bash)); $(bash --version | head -1); $(bsdtar --version)"
echo "## host LANG=$LANG LC_ALL=${LC_ALL:-unset} LC_COLLATE=${LC_COLLATE:-unset}; $(ldd --version | head -1)"
list_package_files() {
	(
		export LC_COLLATE=C
		shopt -s dotglob globstar
		printf '%s\0' **/*
	)
}
echo
echo "### 1. treeA (requested fixture): .BUILDINFO .INSTALL .MTREE .PKGINFO + usr/bin/hello A/data _x/f Zeta/g"
cd "$B/treeA" || exit 1
list_package_files | tr '\0' '\n' | nl -ba
echo "### 2. treeB: legal top-level names whose first byte is below '.' (0x2E)"
cd "$B/treeB" || exit 1
list_package_files > "$B/treeB.body.nul"
echo "-- body order (%q, NUL-safe read, middle elided):"
i=0
while IFS= read -r -d '' n; do
	i=$((i+1)); printf '%2d %q\n' "$i" "$n"
done < "$B/treeB.body.nul" | sed -n '1,22p'
echo "-- whole list entry count: $(tr -cd '\0' < "$B/treeB.body.nul" | wc -c)"
echo "-- body order == LC_ALL=C byte sort of the same names (NUL-safe)?"
LC_ALL=C sort -z "$B/treeB.body.nul" > "$B/treeB.sort.nul"
cmp -s "$B/treeB.body.nul" "$B/treeB.sort.nul" && echo "IDENTICAL" || echo "DIFFERS"
echo "-- top-level entries with first byte < 46, with the byte value:"
while IFS= read -r -d '' n; do
	case $n in */*) continue;; esac
	first=$(printf '%s' "$n" | od -An -tu1 -N1 | tr -d ' ')
	if [ "$first" -lt 46 ]; then printf 'byte=%s\t%q\n' "$first" "$n"; fi
done < "$B/treeB.body.nul"
echo "-- metadata first bytes:"
for n in .BUILDINFO .INSTALL .MTREE .PKGINFO; do printf 'byte=%s\t%s\n' "$(printf '%s' "$n" | od -An -tu1 -N1 | tr -d ' ')" "$n"; done
echo
echo "### 3. treeD: byte sort of full paths vs per-directory grouped walk"
cd "$B/treeD" || exit 1
echo "-- body order:"; list_package_files | tr '\0' '\n' | nl -ba
echo "-- per-directory-grouped walk would be: .PKGINFO A A/b A-b A.b"
echo
echo "### 4. locale sensitivity on treeA (LC_COLLATE=C vs host LANG en_US.UTF-8)"
cd "$B/treeA" || exit 1
echo "-- LC_COLLATE=en_US.UTF-8, no C export (first 8):"
( export LC_COLLATE=en_US.UTF-8; shopt -s dotglob globstar; printf '%s\n' **/* ) | nl -ba | sed -n '1,8p'
echo
echo "### 5. treeE end-to-end package (archive built by create_package:617-626 commands)"
echo "-- archive member order:"; bsdtar -tf "$B/demo-1-1-x86_64.pkg.tar.zst" | nl -ba
echo "-- .MTREE self-exclusion: grep -c MTREE in zcat .MTREE = $(zcat "$B/treeE/.MTREE" | grep -c MTREE)"
