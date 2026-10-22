#!/usr/bin/env bash
# Wave-2 runner for the C1 mutation-fixture set (tools/check-self-assessment.py).
#
# Seat: MutSelfAssessPlan.  Run from the lane repo root, or anywhere:
#
#   bash .ufo/waves/round-25/w1/MutSelfAssessPlan/run_wave2.sh [REVISION]
#
# What it does, in order:
#   1. regenerates the fixtures for REVISION (default: the lane's current HEAD),
#      so the baseline tables carry the counts that revision actually holds;
#   2. runs every fixture against the checker in a throwaway git repo built with
#      `git init` (no remote, so nothing can be pushed to the lane);
#   3. prints one line per fixture and a killed/survived summary.
#
# SAFETY
#   * the lane is read only: `git archive` and `git rev-parse` are the only lane
#     git commands, and neither writes;
#   * every scratch repo has NO remote; no push or fetch is ever issued;
#   * scratch repos live under /fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan/repos
#     and are deleted unless KEEP=1;
#   * nothing outside this seat's own directory is written.
set -euo pipefail

SEAT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANE="${LANE:-/home/vgpnk/Projects/shokunin/tsukuroi-shokunin}"
WORK="${WORK:-/fast/scratch/hyaku/tsukuroi-r25/MutSelfAssessPlan}"
FIXTURES="$WORK/fixtures"
TOOL="${TOOL:-$LANE/tools/check-self-assessment.py}"
REVISION="${1:-$(git -C "$LANE" rev-parse HEAD)}"

if [ ! -f "$TOOL" ]; then
  echo "TOOL_ABSENT: $TOOL not found; the checker has not been landed in the lane yet."
  echo "Point TOOL at the checker's own checkout, e.g."
  echo "  TOOL=/fast/scratch/hyaku/tsukuroi-r25/ExecSelfAssessTool/repo/tools/check-self-assessment.py \\"
  echo "    bash $0 $REVISION"
  exit 3
fi

echo "lane=$LANE"
echo "revision=$REVISION"
echo "tool=$TOOL"
echo "tool_sha256=$(sha256sum "$TOOL" | cut -d' ' -f1)"

echo "--- regenerating fixtures ---"
python3 "$SEAT_DIR/generate_fixtures.py" \
  --lane "$LANE" --revision "$REVISION" --mode "${MODE:-computed}" --out "$FIXTURES"

echo "--- running mutations ---"
KEEP_FLAG=""
if [ "${KEEP:-0}" = "1" ]; then KEEP_FLAG="--keep"; fi
python3 "$SEAT_DIR/run_mutations.py" \
  --lane "$LANE" --revision "$REVISION" --fixtures "$FIXTURES" --tool "$TOOL" \
  --workdir "$WORK/repos" --json "$WORK/results.json" $KEEP_FLAG

echo "--- results ---"
echo "json=$WORK/results.json"
