#!/usr/bin/env bash
# round-70 gate battery. Read-only apart from its own receipts under
# .ufo/waves/round-70/after/. Usage: bash gates.sh <revision>
set -u
R=${1:?usage: gates.sh <revision>}
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
OUT=$L/.ufo/waves/round-70/after
mkdir -p "$OUT"
F=$OUT/gates-at-$R.txt
cd "$L" || exit 2
{
  echo "gates at revision $R — $(date -u +%Y-%m-%dT%H:%M:%SZ) — read-only except $F"
  echo "== C1 frozen counter =="
  python3 tools/count-xs-rows-r70.py --revision "$R"; echo "rc=$?"
  echo "== registry rows at $R =="
  git show "$R":corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'
  echo "== new rows S290-S296 cell counts (want NF=13) =="
  git show "$R":corpus/SOURCES.md | awk -F'|' '/^\| S(29[0-6]) /{print $2, "NF=" NF}'
  echo "== C2 label =="
  git show "$R":tools/tsukuroi-census.sh | grep -c 'XFS xfs-stats'
  echo "== census selftest =="
  bash tools/tsukuroi-census.sh --selftest > "$OUT/selftest-after.txt" 2>&1; echo "rc=$?"
  tail -1 "$OUT/selftest-after.txt"
  grep -c 'R70-C2' "$OUT/selftest-after.txt"
  echo "== live census =="
  bash tools/tsukuroi-census.sh > "$OUT/census-live-after.txt" 2>&1; echo "rc=$?"
  grep -c '^XFS xfs-stats ' "$OUT/census-live-after.txt"
  grep '^XFS xfs-stats ' "$OUT/census-live-after.txt"
  grep '^TSUKUROI_CENSUS:' "$OUT/census-live-after.txt"
  echo "== xfs mounts at the same moment =="
  findmnt -t xfs -o TARGET,SOURCE | tail -n +2
  echo "== error/log regular-file counts per filesystem =="
  for d in /sys/fs/xfs/*/; do
    [ -f "$d/stats/stats" ] || continue
    printf '%s error=%s log=%s stats_lines=%s\n' "${d%/}" \
      "$(find "$d/error" -type f 2>/dev/null | wc -l)" \
      "$(find "$d/log" -type f 2>/dev/null | wc -l)" \
      "$(wc -l < "$d/stats/stats")"
  done
  echo "== neutral diff vs base rollup =="
  diff <(grep '^TSUKUROI_CENSUS:' .ufo/waves/round-70/before/census-live-base.txt) \
       <(grep '^TSUKUROI_CENSUS:' "$OUT/census-live-after.txt") && echo "rollup identical rc=0"
  echo "== knowledge header gate =="
  python3 tools/check-knowledge-header.py --revision "$R"; echo "rc=$?"
  echo "== knowledge refs gate =="
  python3 tools/check-knowledge-refs-r68.py --revision "$R"; echo "rc=$?"
  echo "== cited-receipts gate, round 70 =="
  python3 tools/check-cited-receipts-r62.py --revision "$R" --round 70; echo "rc=$?"
  echo "== line-endings guard =="
  python3 tools/check-line-endings-r64.py --check --root "$L"; echo "rc=$?"
  echo "== scorecard unique sections =="
  python3 tools/check-scorecard-unique-sections.py; echo "rc=$?"
  echo "== canonical sources census =="
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin tsukuroi; echo "rc=$?"
} | tee "$F"
