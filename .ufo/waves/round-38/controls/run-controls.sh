#!/usr/bin/env bash
# Round-38 control receipts (§9 claim sizing): score the cheapest controls that skip the claimed work
# with the frozen counters, before any seat scores. A control that meets a target means the counter
# or the target is wrong. Fixture discipline: one scratch clone under $HYAKU_SCRATCH, every git call
# names -C "$D", the toplevel is verified before the first commit, origin is removed so the
# counters' landed-revision binding reads the clone's own master. Output: one JSON line per control.
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r38/controls
mkdir -p "$S"
D=$(mktemp -d "$S/clone.XXXXXX")
trap 'chmod -R u+rwx -- "$D" 2>/dev/null || true; rm -rf -- "$D"' EXIT
git clone -q --shared "$LANE" "$D/lane"
D="$D/lane"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch" >&2; exit 3; }
git -C "$D" remote remove origin
git -C "$D" config user.name control
git -C "$D" config user.email control@fixture.invalid
git -C "$D" checkout -q -B master 8bd001f58bfda29c92d90d2a7a413825c0ca9fcb
mkdir -p "$D/.ufo/waves/round-38/frozen" "$D/tools"
cp -a "$LANE/.ufo/waves/round-38/frozen/hooks-capture" "$D/.ufo/waves/round-38/frozen/"
cp "$LANE/tools/check-hook-order-r38.py" "$LANE/tools/score-storage-arm-r38.py" "$D/tools/"
export TMPDIR="$S"

prep() { mkdir -p "$D/.ufo/waves/round-38/frozen" "$D/tools"; cp -a "$LANE/.ufo/waves/round-38/frozen/hooks-capture" "$D/.ufo/waves/round-38/frozen/"; cp "$LANE/tools/check-hook-order-r38.py" "$LANE/tools/score-storage-arm-r38.py" "$D/tools/"; }
commit() { git -C "$D" add -A && git -C "$D" commit -q -m "$1" && git -C "$D" rev-parse HEAD; }
c2() { python3 "$D/tools/check-hook-order-r38.py" --repo "$D" --revision "$1" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(json.dumps({k:d.get(k) for k in ("rows_expected","rows_matched","mismatches","extra_rows","source_ok","result","exit","error")}))' || true; }
c1() { python3 "$D/tools/score-storage-arm-r38.py" --repo "$D" --revision "$1" --scratch "$S" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(json.dumps({k:d.get(k) for k in ("fixtures_matched","fixtures_expected","live_match","six_planes_all","result","exit","error")}))' || true; }

render() { # render <variant> -> writes the entry with a table built from the counter's own model, transformed
python3 - "$D" "$1" <<'PY'
import sys, importlib.util, functools
from pathlib import Path
D, variant = Path(sys.argv[1]), sys.argv[2]
s = importlib.util.spec_from_file_location('c2', D / 'tools/check-hook-order-r38.py'); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
rows = m.expected_rows(D)
if variant == 'plain-sort':        # full-name byte sort (suffix not ignored), positions recomputed
    rows = sorted(rows, key=lambda r: (r[0], r[2].encode()))
    out, pos = [], {}
    for r in rows:
        pos[r[0]] = pos.get(r[0], 0) + 1
        out.append((r[0], str(pos[r[0]])) + r[2:])
    rows = out
elif variant == 'no-override':     # every hook attributed to the system directory
    rows = [r[:3] + ('usr',) + r[4:] for r in rows]
src = 'source: S900 (control row)\n' if variant != 'no-source' else 'source: own capture only\n'
body = src + 'verified-at: control\nrecheck: control\n\n' + m.SECTION + '\n\n| when | pos | name | dir | abort | needs | exec |\n|---|---|---|---|---|---|---|\n'
body += ''.join('| %s |\n' % ' | '.join(r) for r in rows)
(D / m.ENTRY).write_text(body)
reg = (D / 'corpus/SOURCES.md').read_text()
row = '| S900 | control | docs | A | control | control | control | mined | 2026-10-26 | 90d | corpus/knowledge/pacman-hook-order-r38.md |\n'
if 'S900' not in reg:
    lines = reg.splitlines(keepends=True)
    idx = max(i for i, l in enumerate(lines) if l.startswith('| S'))
    lines.insert(idx + 1, row)
    (D / 'corpus/SOURCES.md').write_text(''.join(lines))
PY
}

base=8bd001f58bfda29c92d90d2a7a413825c0ca9fcb
echo "{\"control\":\"C2-do-nothing (base)\",\"score\":$(c2 $base)}"
for v in plain-sort no-override no-source correct; do
  git -C "$D" checkout -q -B master "$base"; prep
  render "$v"; h=$(commit "control $v")
  echo "{\"control\":\"C2-$v\",\"score\":$(c2 "$h")}"
done

git -C "$D" checkout -q -B master "$base"; prep
echo "{\"control\":\"C1-do-nothing (base)\",\"score\":$(c1 $base)}"
# constant emitter: prints the host's healthy reading without reading sysfs
python3 - "$D/tools/tsukuroi-census.sh" <<'PY'
import sys; p=sys.argv[1]; t=open(p).read()
t=t.replace("  local roll=HEALTHY\n", "  printf 'STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0\\n'\n  local roll=HEALTHY\n", 1)
open(p,'w').write(t)
PY
h=$(commit "control constant-storage"); echo "{\"control\":\"C1-constant-emitter\",\"score\":$(c1 "$h")}"
git -C "$D" checkout -q -B master "$base"; prep
# naive emitter: counts error_stats files and any nonzero digit; never BLOCKED
python3 - "$D/tools/tsukuroi-census.sh" <<'PY'
import sys; p=sys.argv[1]; t=open(p).read()
arm = r'''  local _sr=${TSUKUROI_BTRFS_SYSFS:-/sys/fs/btrfs} _fs=0 _dv=0 _nz=0 _st=HEALTHY _f
  for _f in "$_sr"/*-*-*-*-*; do [ -d "$_f" ] && _fs=$((_fs + 1)); done
  for _f in "$_sr"/*/devinfo/*/error_stats; do [ -e "$_f" ] || continue; _dv=$((_dv + 1)); _nz=$((_nz + $(grep -cE ' [1-9][0-9]*$' "$_f" 2>/dev/null || true))); done
  [ "$_nz" -gt 0 ] && _st=DEGRADED
  printf 'STORAGE btrfs-device-stats state=%s filesystems=%s devices=%s nonzero=%s\n' "$_st" "$_fs" "$_dv" "$_nz"
'''
t=t.replace("  local roll=HEALTHY\n", arm + "  local roll=HEALTHY\n", 1)
open(p,'w').write(t)
PY
h=$(commit "control naive-storage"); echo "{\"control\":\"C1-naive-emitter\",\"score\":$(c1 "$h")}"
