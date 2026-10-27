#!/usr/bin/env bash
# Per-site check: base statement (from 5bbd5ff5) vs impl statement (18389f44), same CAP_OUT.
set +e
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecFullLarge; F=$S/fx; B=$S/bin
export FX=$F PAD_LINES=4000
"$B/systemctl" --user is-system-running --no-pager > "$S/site-S1.txt"
"$B/systemctl" --user show ai-usage.timer -p Result --value --no-pager > "$S/site-S2.txt"
"$B/nvidia-smi" --query-gpu=name,driver_version --format=csv,noheader > "$S/site-S3.txt"
"$B/systemctl" is-active graphical.target --no-pager > "$S/site-S4.txt"
"$B/systemctl" --user show ai-usage.timer -p ActiveState --value --no-pager > "$S/site-S5.txt"
run_stmt() { # run_stmt label file statement
  local label=$1 f=$2 stmt=$3 rc out
  out=$(bash -c "set -euo pipefail; CAP_OUT=\$(cat '$f'); $stmt" 2>&1); rc=$?
  printf '%-14s rc=%s bytes_out=%s value=%s\n' "$label" "$rc" "${#out}" "$(printf '%s' "$out" | head -c 60)"
}
run_stmt 'base S1' "$S/site-S1.txt" "state=\$(printf '%s\\n' \"\$CAP_OUT\" | head -n1 | tr -d '\\r' | sed -E 's/[[:space:]]+\$//'); printf '%s' \"\$state\""
run_stmt 'impl S1' "$S/site-S1.txt" "state=\${CAP_OUT%%\$'\\n'*}; state=\${state//\$'\\r'/}; state=\${state%\"\${state##*[![:space:]]}\"}; printf '%s' \"\$state\""
run_stmt 'base S2' "$S/site-S2.txt" "r=\$(printf '%s\\n' \"\$CAP_OUT\" | head -n1 | tr -d '\\r'); printf '%s' \"\$r\""
run_stmt 'impl S2' "$S/site-S2.txt" "r=\${CAP_OUT%%\$'\\n'*}; r=\${r//\$'\\r'/}; printf '%s' \"\$r\""
run_stmt 'base S3' "$S/site-S3.txt" "driver=\$(printf '%s\\n' \"\$CAP_OUT\" | head -n1 | awk -F', *' '{print \$NF}'); printf '%s' \"\$driver\""
run_stmt 'impl S3' "$S/site-S3.txt" "driver=\${CAP_OUT%%\$'\\n'*}; driver=\$(printf '%s\\n' \"\$driver\" | awk -F', *' '{print \$NF}'); printf '%s' \"\$driver\""
run_stmt 'base S4' "$S/site-S4.txt" "t_word=\$(printf '%s\\n' \"\$CAP_OUT\" | head -n1 | tr -d '\\r' | sed -E 's/[[:space:]]+\$//'); printf '%s' \"\$t_word\""
run_stmt 'impl S4' "$S/site-S4.txt" "t_word=\${CAP_OUT%%\$'\\n'*}; t_word=\${t_word//\$'\\r'/}; t_word=\${t_word%\"\${t_word##*[![:space:]]}\"}; printf '%s' \"\$t_word\""
run_stmt 'base S5' "$S/site-S5.txt" "r=\$(printf '%s\\n' \"\$CAP_OUT\" | head -n1 | tr -d '\\r' | sed -E 's/[[:space:]]+\$//'); printf '%s' \"\$r\""
run_stmt 'impl S5' "$S/site-S5.txt" "r=\${CAP_OUT%%\$'\\n'*}; r=\${r//\$'\\r'/}; r=\${r%\"\${r##*[![:space:]]}\"}; printf '%s' \"\$r\""
printf '%s\n' "--- site input sizes (bytes)"; wc -c "$S"/site-S?.txt
