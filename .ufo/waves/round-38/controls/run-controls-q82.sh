#!/usr/bin/env bash
# Round-38 pre-seat amendment controls (QUALITY 82): a fixture-gated arm and a cached-live arm, each
# scored by the frozen v1 counter and by the supplementary production-path counter. Same fixture
# discipline as run-controls.sh (scratch clone, origin removed, toplevel verified, fixture identity).
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r38/controls-q82
mkdir -p "$S"
D=$(mktemp -d "$S/clone.XXXXXX")
trap 'chmod -R u+rwx -- "$D" 2>/dev/null || true; rm -rf -- "$D"' EXIT
git clone -q --shared "$LANE" "$D/lane"
D="$D/lane"
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch" >&2; exit 3; }
git -C "$D" remote remove origin
git -C "$D" config user.name control
git -C "$D" config user.email control@fixture.invalid
ARM=52ffd65f868431f021b8615ab281efd87195eac6
export TMPDIR="$S"
prep() { cp "$LANE/tools/score-storage-arm-r38.py" "$LANE/tools/score-storage-arm-r38-q82.py" "$D/tools/"; }
commit() { git -C "$D" add -A && git -C "$D" commit -q -m "$1" && git -C "$D" rev-parse HEAD; }
v1() { python3 "$D/tools/score-storage-arm-r38.py" --repo "$D" --revision "$1" --scratch "$S" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(json.dumps({k:d.get(k) for k in ("fixtures_matched","live_match","six_planes_all","result","exit","error")}))' || true; }
q82() { python3 "$D/tools/score-storage-arm-r38-q82.py" --repo "$D" --revision "$1" --scratch "$S" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(json.dumps({k:d.get(k) for k in ("ns_views_matched","ns_available","seed","result","exit","error")}))' || true; }

for variant in fixture-gated cached-live real-arm; do
  git -C "$D" checkout -q -B master "$ARM"; prep
  case "$variant" in
    fixture-gated)
      python3 - "$D/tools/tsukuroi-census.sh" <<'PY'
import sys; p=sys.argv[1]; t=open(p).read()
anchor = "probe_storage_arm() {\n"
gate = anchor + "  if [ -z \"${TSUKUROI_BTRFS_SYSFS+x}\" ]; then STORAGE_LINE='STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'; return 0; fi\n"
assert anchor in t; open(p, 'w').write(t.replace(anchor, gate, 1))
PY
      ;;
    cached-live)
      python3 - "$D/tools/tsukuroi-census.sh" <<'PY'
import sys; p=sys.argv[1]; t=open(p).read()
anchor = "  probe_storage_arm\n  printf '%s\\n' \"$STORAGE_LINE\"\n"
assert anchor in t
open(p, 'w').write(t.replace(anchor, "  printf '%s\\n' 'STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0'\n", 1))
PY
      ;;
    real-arm) : ;;
  esac
  h=$(commit "control $variant")
  echo "{\"control\":\"C1-$variant\",\"v1\":$(v1 "$h"),\"q82\":$(q82 "$h")}"
done
