#!/usr/bin/env bash
# repro-c2-truncate.sh -- C1LabReplace, round 46, item C1-10 (c).
#
# DEFECT (smallest form): truncate the census in place immediately before its final
# `main "$@"`. bash has already buffered that call, so the whole 209 KB script executes and
# `--identity` runs -- but the fd now holds ZERO bytes, and the line reports
# `sha256=e3b0c442...` (SHA-256 of the empty string) `bytes=0 lines=0 ... verified=yes`.
# Nothing in the line warns that the executed code and the hashed bytes are different files.
#
# Usage:  ./repro-c2-truncate.sh <scratch-dir> [census-path]
set -u
S=${1:?usage: repro-c2-truncate.sh <scratch-dir> [census-path]}
SRC=${2:-/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh}
mkdir -p -- "$S" && cd -- "$S" || exit 2
export TMPDIR=$PWD

awk 'done!=1 && /^main "\$@"$/{print ": > \"$0\""; done=1} {print}' "$SRC" > census.sh
echo "injected: : > \"\$0\"   immediately before main \"\$@\""
out=$(bash ./census.sh --identity 2>&1); rc=$?
echo "rc=$rc"
echo "stdout: $out"
echo "bytes left in census.sh: $(wc -c < census.sh)"
echo "sha256 of the empty string: $(printf '' | sha256sum | cut -d' ' -f1)"
echo
echo 'CONTROL (same injection, truncating a different file):'
awk 'done!=1 && /^main "\$@"$/{print ": > \"${0%/*}/other\""; done=1} {print}' "$SRC" > control.sh
bash ./control.sh --identity; echo "control rc=$?"
