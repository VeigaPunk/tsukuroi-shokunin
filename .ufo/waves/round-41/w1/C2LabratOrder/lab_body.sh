#!/bin/bash
# Verbatim function body from makepkg.sh.in:562-569 (frozen 54d9411), plus
# diagnostics around it. Usage: lab_body.sh <dir> [fmt]
set -u
cd "$1" || exit 1
fmt=${2:-%s\\n}
echo "## bash $BASH_VERSION; PWD=$PWD"
echo "## shopt before: $(shopt globstar dotglob | tr '\n' ' ')"
echo "## --- body verbatim ---"
list_package_files() {
	(
		export LC_COLLATE=C
		shopt -s dotglob globstar
		# bash 5.0 only works with combo directory + file globs
		printf '%s\0' **/*
	)
}
echo "## shopt inside check:"
( export LC_COLLATE=C; shopt -s dotglob globstar; shopt -p globstar dotglob )
echo "## NUL list -> lines:"
list_package_files | tr '\0' '\n'
echo "## rc(list_package_files)=$?"
echo "## same body with %s\\n (assignment literal):"
( export LC_COLLATE=C; shopt -s dotglob globstar; printf '%s\n' **/* )
echo "## end"
