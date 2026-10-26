#!/usr/bin/env bash
# C2ExecRecheckLive — read-only live-drift probe for the round-39 C2 capture.
# Writes only into its own seat dir. Run from the lane root.
set -u
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
SEAT=$LANE/.ufo/waves/round-39/w1/C2ExecRecheckLive
CAP=$LANE/.ufo/waves/round-39/frozen/txcapture
R38=$LANE/.ufo/waves/round-38/frozen/hooks-capture
S=$(mktemp -d /fast/scratch/hyaku/tsukuroi-r39/C2ExecRecheckLive/rr.XXXXXX)
trap 'rm -rf -- "$S"' EXIT
cd "$LANE" || exit 1

echo '### A. literal recheck line, as written in the entry'
printf '%s\n' 'python3 tools/check-transaction-order-r39.py --revision <REV>' > "$S/literal.sh"
bash -n "$S/literal.sh" 2>&1; echo "bash_n_exit=$?"

echo '### B. recheck with <REV> substituted (entry commit, lane tip, short hash)'
for rev in 4078eb236c7c67f343c76956c587d0a356e0bf5c 394e1ba4fab39a417abe66a7802f87cf1ff8dd61 4078eb2; do
  python3 tools/check-transaction-order-r39.py --revision "$rev" > "$SEAT/recheck-$rev.json" 2>&1
  echo "rev=$rev exit=$? result=$(python3 -c "import json,sys;d=json.load(open('$SEAT/recheck-$rev.json'));print(d.get('result'),d.get('rules_verified'),d.get('counts_ok'),d.get('source_ok'),d.get('duplicate_rows'),d.get('duplicate_headings'),d.get('oracle_violations'))")"
done

echo '### C. capture integrity against its own MANIFEST'
( cd "$CAP" && sha256sum -c MANIFEST.sha256 )
sha256sum "$CAP/MANIFEST.sha256"

echo '### D. live /var/log/pacman.log vs MANIFEST'
sha256sum /var/log/pacman.log
stat -c '%n mtime=%y size=%s' /var/log/pacman.log
tail -2 /var/log/pacman.log

echo '### E. host counts, live log vs frozen copy'
python3 - "$CAP/pacman.log" <<'PY'
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location('c', 'tools/check-transaction-order-r39.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
live = open('/var/log/pacman.log', encoding='utf-8', errors='replace').read().splitlines()
frozen = open(sys.argv[1], encoding='utf-8', errors='replace').read().splitlines()
print(json.dumps({'live': m.host_counts(live), 'frozen': m.host_counts(frozen),
                  'lines_live': len(live), 'lines_frozen': len(frozen)}, indent=1))
PY

echo '### F. hook owner map regenerated (capture-meta command) vs frozen — ambient locale'
for h in /usr/share/libalpm/hooks/*.hook /etc/pacman.d/hooks/*.hook; do
  printf '%s\t%s\n' "$h" "$(pacman -Qqo "$h" 2>/dev/null || echo -)"
done > "$SEAT/hook-owners.live.tsv"
diff -u "$CAP/hook-owners.tsv" "$SEAT/hook-owners.live.tsv" && echo 'hook-owners: BYTE-IDENTICAL'
sha256sum "$SEAT/hook-owners.live.tsv" "$CAP/hook-owners.tsv"
echo '--- same map as a set ---'
diff <(sort "$CAP/hook-owners.tsv") <(sort "$SEAT/hook-owners.live.tsv") && echo 'hook-owners: IDENTICAL as (path,value) set'

echo '### G. hook When map regenerated vs frozen — ambient locale'
for h in /usr/share/libalpm/hooks/*.hook /etc/pacman.d/hooks/*.hook; do
  printf '%s\t%s\n' "$h" "$(awk -F= '/^[[:space:]]*When[[:space:]]*=/ {v=$2; gsub(/^[[:space:]]+|[[:space:]]+$/,"",v); print v; exit}' "$h")"
done > "$SEAT/hook-when.live.tsv"
diff -u "$CAP/hook-when.tsv" "$SEAT/hook-when.live.tsv" && echo 'hook-when: BYTE-IDENTICAL'
sha256sum "$SEAT/hook-when.live.tsv" "$CAP/hook-when.tsv"
echo '--- same map as a set ---'
diff <(sort "$CAP/hook-when.tsv") <(sort "$SEAT/hook-when.live.tsv") && echo 'hook-when: IDENTICAL as (path,value) set'

echo '### F2/G2. both maps regenerated under LC_ALL=C'
( export LC_ALL=C
  for h in /usr/share/libalpm/hooks/*.hook /etc/pacman.d/hooks/*.hook; do
    printf '%s\t%s\n' "$h" "$(pacman -Qqo "$h" 2>/dev/null || echo -)"
  done ) > "$SEAT/hook-owners.live.C.tsv"
( export LC_ALL=C
  for h in /usr/share/libalpm/hooks/*.hook /etc/pacman.d/hooks/*.hook; do
    printf '%s\t%s\n' "$h" "$(awk -F= '/^[[:space:]]*When[[:space:]]*=/ {v=$2; gsub(/^[[:space:]]+|[[:space:]]+$/,"",v); print v; exit}' "$h")"
  done ) > "$SEAT/hook-when.live.C.tsv"
diff "$CAP/hook-owners.tsv" "$SEAT/hook-owners.live.C.tsv" && echo 'hook-owners under LC_ALL=C: BYTE-IDENTICAL'
diff "$CAP/hook-when.tsv" "$SEAT/hook-when.live.C.tsv" && echo 'hook-when under LC_ALL=C: BYTE-IDENTICAL'
sha256sum "$SEAT/hook-owners.live.C.tsv" "$SEAT/hook-when.live.C.tsv"
echo "ambient LANG=${LANG:-unset} LC_ALL=${LC_ALL:-unset} LC_COLLATE=${LC_COLLATE:-unset}"

echo '### H. hook file bytes vs the round-38 capture (the only hook-byte baseline in the lane)'
mkdir -p "$S/hooks-live/etc-pacman.d-hooks" "$S/hooks-live/usr-share-libalpm-hooks"
cp -a /etc/pacman.d/hooks/*.hook "$S/hooks-live/etc-pacman.d-hooks/"
cp -a /usr/share/libalpm/hooks/*.hook "$S/hooks-live/usr-share-libalpm-hooks/"
( cd "$S/hooks-live" && sha256sum -c "$R38/MANIFEST.sha256" > "$SEAT/r38-manifest-check.txt" 2>&1 )
echo "files_ok=$(grep -c ': OK$' "$SEAT/r38-manifest-check.txt") failures=$(grep -vc ': OK$' "$SEAT/r38-manifest-check.txt")"
diff -r "$R38/usr-share-libalpm-hooks" "$S/hooks-live/usr-share-libalpm-hooks" && echo 'usr-share-libalpm-hooks: IDENTICAL bytes'
diff -r "$R38/etc-pacman.d-hooks" "$S/hooks-live/etc-pacman.d-hooks" && echo 'etc-pacman.d-hooks: IDENTICAL bytes'
( cd /usr/share/libalpm/hooks && sha256sum *.hook; cd /etc/pacman.d/hooks && sha256sum *.hook ) > "$SEAT/hooks.live.sha256"
sha256sum "$SEAT/hooks.live.sha256"

echo '### I. installed pacman pin'
pacman -Q pacman
