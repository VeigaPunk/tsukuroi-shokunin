#!/usr/bin/env bash
# round-71 C2 red-before receipt: the pre-fix selftest harness has no per-case bound.
# The selftest runs every case through `out=$(env ... "$BASH" "$SELF" 2>&1)`; when a probe
# blocks, that command substitution cannot return and the suite produces no case line at all.
# This receipt reproduces the same call shape with a blocking `pacman -Q` under an EXTERNAL
# `timeout`, so the run is bounded by us and the observation is the absence of any verdict.
set -uo pipefail
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
BASE=${TMPDIR:-/fast/scratch/hyaku}/tsukuroi-r71-redbefore
rm -rf -- "$BASE"; mkdir -p "$BASE/bin" "$BASE/fx"
mkfifo "$BASE/fx/fifo"
cat > "$BASE/bin/pacman" <<'STUB'
#!/usr/bin/env bash
# blocks forever: the pre-fix harness has nothing that can end this
read -r _ < "${TSUKUROI_FIXTURE:?}/fifo"
STUB
chmod +x "$BASE/bin/pacman"
printf 'blocking pacman stub installed at %s/bin/pacman; fifo at %s/fx/fifo\n' "$BASE" "$BASE"
start=$(date +%s)
set +e
out=$(timeout 20 env TSUKUROI_FIXTURE="$BASE/fx" TSUKUROI_PACMAN="$BASE/bin/pacman" \
      TSUKUROI_PACMAN_CONF="$BASE/bin/pacman-conf-absent" \
      TSUKUROI_PACMAN_CONF_FILE="$BASE/fx/pacman.conf" \
      TSUKUROI_PACMAN_DB="$BASE/fx/pacmandb" \
      "$BASH" "$LANE/tools/tsukuroi-census.sh" 2>&1)
rc=$?
set -e
elapsed=$(( $(date +%s) - start ))
printf 'rc=%s elapsed=%ss verdict_lines=%s\n' "$rc" "$elapsed" \
  "$(printf '%s\n' "$out" | grep -c '^TSUKUROI_CENSUS:' || true)"
printf 'output_tail=%s\n' "$(printf '%s' "$out" | tail -c 120 | tr '\n' '|')"
printf '\n## harness-absence sweep (pre-fix)\n'
printf 'R71-C2 labels: %s\n' "$(grep -c 'R71-C2' "$LANE/tools/tsukuroi-census.sh" || true)"
printf 'per-case timeout tokens (case_timeout|SELFTEST_CASE_TIMEOUT|kill -TERM): %s\n' \
  "$(grep -cE 'case_timeout|SELFTEST_CASE_TIMEOUT|kill -TERM' "$LANE/tools/tsukuroi-census.sh" || true)"
rm -rf -- "$BASE"
[ "$rc" -eq 124 ] && printf 'RED-BEFORE HOLDS: a blocking probe ends the run at the external bound with no verdict line\n'
