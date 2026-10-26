#!/usr/bin/env bash
# Round-41 C2 host capture (read-only): the local ALPM database entries libalpm wrote at install time,
# the host `vercmp` ordering for epoch and release, and the host PKGBUILD(5) working-directory lines.
# Writes only into the directory given as $1 (default: this script's directory). No sudo, no pacman
# transaction, no network. Run: bash capture.sh <outdir>
set -euo pipefail
export LC_ALL=C MANWIDTH=80
out=${1:-$(cd "$(dirname "$0")" && pwd)}
db=/var/lib/pacman/local
{
  printf 'entry\tdesc\tfiles\tmtree\tinstall\tchangelog\tdotfiles\tmtree_gzip\tmtree_lists_self\n'
  for d in "$db"/*/; do
    d=${d%/}; n=${d##*/}
    has() { [ -f "$d/$1" ] && printf 1 || printf 0; }
    dots=$(find "$d" -mindepth 1 -maxdepth 1 -name '.*' | wc -l)
    gz=0; self=0
    if [ -f "$d/mtree" ]; then
      [ "$(head -c 2 "$d/mtree" | od -An -tx1 | tr -d ' \n')" = 1f8b ] && gz=1
      c=$(zcat -- "$d/mtree" 2>/dev/null | grep -c '^\./\.MTREE ' || true)
      [ "${c:-0}" -gt 0 ] && self=1
    fi
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$n" "$(has desc)" "$(has files)" "$(has mtree)" \
      "$(has install)" "$(has changelog)" "$dots" "$gz" "$self"
  done
} > "$out/localdb-anatomy.tsv"
{
  for p in '1:1.0-1 2.0-1' '0:2.0-1 2.0-1' '1.0-1 1:0.1-1' '1.0 1.0-5' '1.0-1 1.0-2' '2:0.1 1:9.9'; do
    set -- $p
    printf 'vercmp %s %s = %s\n' "$1" "$2" "$(vercmp "$1" "$2")"
  done
} > "$out/vercmp.txt"
man -P cat PKGBUILD 2>/dev/null | grep -n 'This function is run inside' > "$out/man-pkgbuild-runinside.txt" || true
p=$(ls -d "$db"/pacman-[0-9]*/ | head -n1)
zcat -- "$p/mtree" | sed -n 1,4p > "$out/mtree-pacman-head.txt"
{
  printf 'captured_utc %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'pacman %s\n' "$(pacman -Q pacman)"
  printf 'kernel %s\n' "$(uname -r)"
  printf 'alpm_db_version %s\n' "$(cat "$db/ALPM_DB_VERSION")"
} > "$out/capture-meta.txt"
(cd "$out" && sha256sum capture.sh capture-meta.txt localdb-anatomy.tsv vercmp.txt man-pkgbuild-runinside.txt \
  mtree-pacman-head.txt > MANIFEST.sha256)
