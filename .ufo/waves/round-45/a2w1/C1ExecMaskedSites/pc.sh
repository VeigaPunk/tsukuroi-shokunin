#!/usr/bin/env bash
# Positive control: the SAME padded bytes, through the claimed-defect shape
# (`printf ... | head -n1` in an assignment, and the `|| true` assignments with the
# `|| true` removed), must kill a `set -euo pipefail` shell with 141. That is what makes
# the payload "past the pipe buffer"; the masked readers survive only because their status
# is ignored or `|| true`. Payloads are read from fixture files (paths only in argv/env:
# a 180 KB payload as an env string would hit MAX_ARG_STRLEN, not the pipe buffer).
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecMaskedSites
pc() { # pc LABEL SCRIPT   (child reads payloads from $S/fx/... itself)
  local label=$1 script=$2 rc
  S="$S" /usr/bin/bash -c 'set -euo pipefail; '"$script" >/dev/null 2>&1
  rc=$?
  printf 'PC %-56s rc=%s%s\n' "$label" "$rc" "$([ "$rc" -eq 141 ] && echo '  [killed by SIGPIPE]')"
}

pc ':707 x=$(printf|head -n1) in assignment' \
   'x=$(printf "%s\n" "$(cat "$S/fx/s707-pad/pq")" | head -n1); :'
pc ':707 x=$(printf|grep -v|head -n8) in assignment' \
   'x=$(printf "%s\n" "$(cat "$S/fx/s707-pad/pq")" | grep -v "^[[:space:]]*$" | head -n8); :'
pc ':832 holds=$(grep|head -n1|sed) with || true REMOVED' \
   'x=$(grep -hE "^[[:space:]]*HoldPkg" "$S/fx/s832-pad/pacman.conf" | head -n1 | sed -E "s/^[[:space:]]*HoldPkg[[:space:]]*=[[:space:]]*//"); :'
pc ':997 timers=$(printf|awk|head -n12) without process substitution' \
   'x=$(printf "%s\n" "$(cat "$S/fx/s997-pad/timerlist")" | awk "NF && \$1 ~ /\\.timer\$/ {print \$1}" | head -n 12); :'
pc ':1531 same, journal timerlist' \
   'x=$(printf "%s\n" "$(cat "$S/fx/s1531-pad/timerlist")" | awk "NF && \$1 ~ /\\.timer\$/ {print \$1}" | head -n 12); :'
pc ':1517 fh_names=$(...|sort -u|head -n6|paste) with || true REMOVED' \
   'x=$(printf "%s\n" "$(cat "$S/fx/s1517-pad/journal-err.json")" | grep -E "\"MESSAGE\":\"[^\"]*(Failed to )" | grep -oE "[A-Za-z0-9_.@-]+\.service" | sort -u | head -n 6 | paste -sd, -); :'
pc ':1817 unk_names=$(printf|grep ^?|sed|head -n6|paste) with || true REMOVED' \
   'x=$(printf "%s\n" "$(cat "$S/fx/s1817-pad/pm")" | tr " " "\n" | sed "s/^/?/" | grep "^?" | sed "s/^?//" | head -n6 | paste -sd, -); :'
pc ':1196 sweep=$(find|sort|head -n4000) as an assignment (pad-b, 637 KB)' \
   'x=$(find "$S/fx/s1196-pad-b/cgroup" -xdev \( -name memory.events -o -name memory.events.local \) -print 2>/dev/null | LC_ALL=C sort | head -n 4000); :'
pc 'CONTROL :707 sub-buffer payload (56 B) as the same assignment' \
   'x=$(printf "%s\n" "$(head -n8 "$S/fx/s707-small/pq")" | head -n1); :'

printf '\n-- masked forms, same padded payloads (must survive under set -euo pipefail) --\n'
/usr/bin/bash -c 'set -euo pipefail
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecMaskedSites
holds=$(grep -hE "^[[:space:]]*HoldPkg" "$S/fx/s832-pad/pacman.conf" | head -n1 | sed -E "s/^[[:space:]]*HoldPkg[[:space:]]*=[[:space:]]*//" || true)
printf "832 masked: rc=0 holds=[%s]\n" "$holds"
mapfile -t n < <(printf "%s\n" "$(cat "$S/fx/s707-pad/pq")" | grep -v "^[[:space:]]*$" | head -n 8)
printf "707 masked: rc=0 n=%s last=%s\n" "${#n[@]}" "${n[-1]}"
fh=$(printf "%s\n" "$(cat "$S/fx/s1517-pad/journal-err.json")" | grep -E "\"MESSAGE\":\"[^\"]*(Failed to )" | grep -oE "[A-Za-z0-9_.@-]+\.service" | sort -u | head -n 6 | paste -sd, - || true)
printf "1517 masked: rc=0 fh=[%s]\n" "$fh"
cl_out=$(awk '"'"'NR == FNR { if (NF >= 2) cls[$1] = $2; next } NF { if ($1 in cls) print cls[$1]; else print "?" $1 }'"'"' <(cat "$S/r6classes.txt") <(cut -d" " -f1 "$S/fx/s1817-pad/pm"))
unk=$(printf "%s\n" "$cl_out" | grep "^?" | sed "s/^?//" | head -n6 | paste -sd, - || true)
printf "1817 masked (census fold shape): rc=0 unk=[%s]\n" "$unk"'
