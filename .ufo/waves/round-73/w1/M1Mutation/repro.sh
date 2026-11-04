#!/usr/bin/env bash
# Reproduce any M1Mutation row against the FROZEN round-73 instruments (declared bytes at 74937132).
# Usage:
#   bash repro.sh counter                  # full counter matrix + selftest-case table
#   bash repro.sh c2                       # full routed-checker matrix
#   bash repro.sh fixture NAME             # frozen counter on one clause-isolated fixture
#   bash repro.sh mutant UID FIXTURE       # one clause-disabled mutant on its fixture
#   bash repro.sh c2fixture NAME           # frozen checker on one fixture
#   bash repro.sh c2mutant CID FIXTURE     # one checker mutant on its fixture
#   bash repro.sh c1at REV                 # frozen counter over committed bytes at REV
#   bash repro.sh routed [REV]             # frozen checker over committed bytes at REV (default HEAD)
#   bash repro.sh absent                   # frozen counter with no data files (exit-map probe)
set -u
S=${S:-/fast/scratch/hyaku/tsukuroi-r73/M1Mutation}
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
W=$L/.ufo/waves/round-73/w1/M1Mutation
trap 'rm -rf -- "$S"' EXIT
mkdir -p "$S/lane/tools" "$S/lane/.ufo/waves/round-73/before/src"
git -C "$L" show 74937132:tools/count-ul-rows-r73.py > "$S/lane/tools/ul_pristine.py"
git -C "$L" show 74937132:tools/check-r72-routed-r73.py > "$S/lane/tools/c2_pristine.py"
cp "$L/.ufo/waves/round-73/before/src/systemd.unit.xml" \
   "$L/.ufo/waves/round-73/before/src/unit.c" \
   "$L/.ufo/waves/round-73/before/src/install.c" \
   "$S/lane/.ufo/waves/round-73/before/src/"
export S OUT=$W TMPDIR=$S

case "${1:-}" in
  absent)
    mkdir -p "$S/empty"
    exec python3 "$S/lane/tools/ul_pristine.py" --fixture "$S/empty"
    ;;
  routed)
    REV=${2:-HEAD}
    R=$S/routed-root
    rm -rf "$R"; mkdir -p "$R/corpus/lessons"
    git -C "$L" show "$REV:corpus/lessons/round-72.md" > "$R/corpus/lessons/round-72.md"
    git -C "$L" show "$REV:SCORECARD.md" > "$R/SCORECARD.md"
    exec python3 "$S/lane/tools/c2_pristine.py" --root "$R"
    ;;
  c1at)
    REV=${2:-HEAD}
    R=$S/c1-root
    rm -rf "$R"; mkdir -p "$R/corpus/knowledge" "$R/corpus" "$R/.ufo/waves/round-73/before/src"
    git -C "$L" show "$REV:corpus/knowledge/systemd-unit-load-plane-r73.md" > "$R/corpus/knowledge/systemd-unit-load-plane-r73.md" 2>/dev/null || true
    git -C "$L" show "$REV:corpus/SOURCES.md" > "$R/corpus/SOURCES.md" 2>/dev/null || true
    git -C "$L" show "$REV:.ufo/waves/round-73/before/src/SOURCES.json" > "$R/.ufo/waves/round-73/before/src/SOURCES.json" 2>/dev/null || true
    for f in systemd.unit.xml unit.c install.c; do
      git -C "$L" show "$REV:.ufo/waves/round-73/before/src/$f" > "$R/.ufo/waves/round-73/before/src/$f" 2>/dev/null || true
    done
    exec python3 "$S/lane/tools/ul_pristine.py" --fixture "$R"
    ;;
esac
exec python3 "$W/battery.py" "$@"
