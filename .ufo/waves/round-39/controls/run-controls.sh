#!/usr/bin/env bash
# Round-39 pre-seat controls (L1 TsukuroiR39). Scores do-nothing / skip-the-work / gaming variants
# with the FROZEN counters (freeze 6a08925d) in a scratch clone with origin removed, then the
# candidate. Usage: run-controls.sh <lane> <candidate-census-file> <candidate-entry-dir> <out-dir>
# Every git call names -C "$D"; the clone's toplevel is checked before the first commit.
set -euo pipefail
LANE=$1 CAND=$2 ENTRYDIR=$3 OUT=$4
FREEZE=6a08925daa30767809eb13bb4b01448ff954d46a
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r39/l1/controls
rm -rf -- "$S"; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT
D=$S/clone
git clone -q --no-local "$LANE" "$D"
git -C "$D" remote remove origin
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel mismatch" >&2; exit 2; }
git -C "$D" checkout -q -B master "$FREEZE"
gc() { git -C "$D" -c user.name=ctl -c user.email=ctl@scratch.invalid commit -q -m "$1"; }
C1=tools/score-storage-hidden-r39.py C2=tools/check-transaction-order-r39.py
score() { # score <label> <counter> -> one JSON line
  local label=$1 counter=$2 rev out
  rev=$(git -C "$D" rev-parse HEAD)
  out=$(TMPDIR=$S python3 "$D/$counter" --repo "$D" --revision "$rev" 2>/dev/null || true)
  OUT_JSON=$out python3 - "$label" "$counter" "$rev" "$(sha256sum "$D/$counter" | cut -d' ' -f1)" <<'EOF'
import json, sys
label, counter, rev, sha = sys.argv[1:5]
import os
r = json.loads(os.environ['OUT_JSON'])
keep = {k: r.get(k) for k in ('hidden_matched', 'views_matched', 'fixtures_matched', 'live_match', 'six_planes_all',
                              'rules_verified', 'duplicate_rows', 'duplicate_headings', 'source_ok', 'counts_ok',
                              'oracle_violations', 'result', 'exit', 'error') if k in r}
print(json.dumps({'control': label, 'counter': counter, 'counter_sha256': sha, 'revision': rev, **keep}))
EOF
}
census_variant() { # census_variant <variant name in c1_variant.py>
  git -C "$D" checkout -q -B "v-$1" "$FREEZE"
  python3 "$(dirname "$0")/c1_variant.py" "$1" "$CAND" "$D/tools/tsukuroi-census.sh"
  git -C "$D" add tools/tsukuroi-census.sh; gc "control $1"
  git -C "$D" branch -f master HEAD
  score "C1-$1" "$C1"
}
mkdir -p "$OUT"; : > "$OUT/controls.jsonl"
# ---- C1 ----
git -C "$D" checkout -q -B master "$FREEZE"; score C1-K0-do-nothing "$C1" >> "$OUT/controls.jsonl"
for v in K1-fixture-gated K2-over-block K3-mountinfo-keyed K4-candidate; do
  census_variant "$v" >> "$OUT/controls.jsonl"
done
# ---- C2 ----
git -C "$D" checkout -q -B master "$FREEZE"; score C2-K0-do-nothing "$C2" >> "$OUT/controls.jsonl"
for v in "$ENTRYDIR"/*/; do
  name=$(basename "$v")
  git -C "$D" checkout -q -B "e-$name" "$FREEZE"
  cp "$v/entry.md" "$D/corpus/knowledge/pacman-transaction-order-r39.md"
  cp "$v/SOURCES.md" "$D/corpus/SOURCES.md"
  git -C "$D" add corpus; gc "control $name"
  git -C "$D" branch -f master HEAD
  score "C2-$name" "$C2" >> "$OUT/controls.jsonl"
done
cat "$OUT/controls.jsonl"
