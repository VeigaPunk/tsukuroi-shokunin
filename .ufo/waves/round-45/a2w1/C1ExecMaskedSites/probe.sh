#!/usr/bin/env bash
# Instrument the exact pipeline text of each unclaimed reader, on the padded fixture bytes,
# and print PIPESTATUS immediately: this is the "is the producer actually SIGPIPE'd" leg.
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecMaskedSites
set -uo pipefail
ps_() { local -a st=("${PIPESTATUS[@]}"); printf 'PIPESTATUS=%s\n' "${st[*]}"; }

echo "== :707  mapfile names < <(printf|grep -v|head -n 8) [pq pad] =="
pq=$(cat "$S/fx/s707-pad/pq")
printf '%s\n' "$pq" | grep -v '^[[:space:]]*$' | head -n 8 >/dev/null; ps_
mapfile -t names < <(printf '%s\n' "$pq" | grep -v '^[[:space:]]*$' | head -n 8)
echo "mapfile rc=$? n=${#names[@]} first=${names[0]} last=${names[-1]}"
printf '%s\n' "$pq" | wc -c

echo "== :832  holds=\$(grep -hE HoldPkg|head -n1|sed ... || true) [pacman.conf pad] =="
conf="$S/fx/s832-pad/pacman.conf"
grep -hE '^[[:space:]]*HoldPkg' "$conf" | head -n1 | sed -E 's/^[[:space:]]*HoldPkg[[:space:]]*=[[:space:]]*//' >/dev/null; ps_
holds=$(grep -hE '^[[:space:]]*HoldPkg' "$conf" 2>/dev/null \
  | head -n1 | sed -E 's/^[[:space:]]*HoldPkg[[:space:]]*=[[:space:]]*//' || true)
echo "assignment rc=$? holds=[$holds] conf_bytes=$(wc -c < "$conf") matching_bytes=$(grep -hE '^[[:space:]]*HoldPkg' "$conf" | wc -c)"

echo "== :997  mapfile timers < <(printf|awk|head -n 12) [timerlist pad] =="
tl=$(cat "$S/fx/s997-pad/timerlist")
printf '%s\n' "$tl" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | head -n 12 >/dev/null; ps_
mapfile -t timers < <(printf '%s\n' "$tl" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | head -n 12)
echo "mapfile rc=$? n=${#timers[@]} enabled=$(printf '%s\n' "$tl" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | wc -l)"

echo "== :1196  done < <(find|sort|head -n 4000) [cgroup pad-a / pad-b] =="
for fx in s1196-pad-a s1196-pad-b; do
  cg="$S/fx/$fx/cgroup"
  find "$cg" -xdev \( -name memory.events -o -name memory.events.local \) -print 2>/dev/null | LC_ALL=C sort | head -n 4000 >/dev/null; ps_
  echo "$fx candidates=$(find "$cg" -xdev \( -name memory.events -o -name memory.events.local \) -print 2>/dev/null | wc -l) bytes=$(find "$cg" -xdev \( -name memory.events -o -name memory.events.local \) -print 2>/dev/null | wc -c)"
done

echo "== :1517  fh_names=\$(printf|grep -E|grep -oE|sort -u|head -n 6|paste -sd, - || true) [journal-err pad] =="
je=$(cat "$S/fx/s1517-pad/journal-err.json")
printf '%s\n' "$je" | grep -E "\"MESSAGE\":\"[^\"]*(Failed to |entered failed state|Failed with result)" \
  | grep -oE '[A-Za-z0-9_.@-]+\.(service|socket|timer|mount|target|device|path|scope|slice)' \
  | sort -u | head -n 6 | paste -sd, - >/dev/null; ps_
fh_names=$(printf '%s\n' "$je" \
  | grep -E "\"MESSAGE\":\"[^\"]*(Failed to |entered failed state|Failed with result)" \
  | grep -oE '[A-Za-z0-9_.@-]+\.(service|socket|timer|mount|target|device|path|scope|slice)' \
  | sort -u | head -n 6 | paste -sd, - || true)
echo "assignment rc=$? fh_names=[$fh_names] distinct_names=$(printf '%s\n' "$je" | grep -E 'Failed to ' | grep -oE '[A-Za-z0-9_.@-]+\.service' | sort -u | wc -l)"

echo "== :1531  mapfile timers < <(printf|awk|head -n 12) [journal timerlist pad] =="
tl2=$(cat "$S/fx/s1531-pad/timerlist")
printf '%s\n' "$tl2" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | head -n 12 >/dev/null; ps_

echo "== :1817  unk_names=\$(printf|grep '^?'|sed|head -n6|paste -sd, - || true) [fold of pm pad] =="
cl_out=$(awk 'NR == FNR { if (NF >= 2) cls[$1] = $2; next } NF { if ($1 in cls) print cls[$1]; else print "?" $1 }' \
  <(printf '%s\n' 'android-apktool-bin aur-local
obsidian-cli-inspector aur-local
elephant offline-exile
elephant-bluetooth offline-exile
elephant-calc offline-exile
elephant-clipboard offline-exile
elephant-desktopapplications offline-exile
elephant-files offline-exile
elephant-menus offline-exile
elephant-providerlist offline-exile
elephant-runner offline-exile
elephant-symbols offline-exile
elephant-todo offline-exile
elephant-unicode offline-exile
elephant-websearch offline-exile
omarchy-walker offline-exile') <(cat "$S/fx/s1817-pad/pm" | tr ' ' '\n'))
printf '%s\n' "$cl_out" | grep '^?' | sed 's/^?//' | head -n6 | paste -sd, - >/dev/null; ps_
echo "cl_out_bytes=$(printf '%s\n' "$cl_out" | wc -c) unknown_rows=$(printf '%s\n' "$cl_out" | grep -c '^?')"
