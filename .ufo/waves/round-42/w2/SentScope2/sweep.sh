#!/usr/bin/env bash
# Read-only scope sweep for tsukuroi round-42 w2, seat SentScope2.
set -u
S=/fast/scratch/hyaku/tsukuroi-r42/SentScope2
T=${1:?tag}
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
F=/home/vgpnk/Projects/shokunin
M=$L/.ufo/waves/round-42/w2-context.txt
O=$S/$T
mkdir -p "$O"
export GIT_OPTIONAL_LOCKS=0
date -u +%FT%TZ > "$O/date.txt"

git -C "$F" status --porcelain > "$O/fleet-status.txt" 2>&1
git -C "$F" status --porcelain --ignored=matching > "$O/fleet-status-ignored.txt" 2>&1
find "$F" -maxdepth 2 -mindepth 1 \( -iname '*tsukuroi*' -o -iname '*r42*' \) -not -path "$L/*" -printf '%TY-%Tm-%Td %TH:%TM %10s %y %p\n' 2>/dev/null | sort > "$O/fleet-name-scan.txt"
find "$F" -maxdepth 1 -newer "$M" -printf '%TY-%Tm-%Td %TH:%TM %10s %y %p\n' 2>/dev/null | sort > "$O/fleet-root-newer.txt"

git -C "$L" status --porcelain > "$O/lane-status.txt" 2>&1
git -C "$L" rev-parse HEAD > "$O/lane-tip.txt" 2>&1
git -C "$L" diff --stat HEAD > "$O/lane-tracked-diff.txt" 2>&1
git -C "$L" diff --cached --stat HEAD > "$O/lane-staged-diff.txt" 2>&1
find "$L" -maxdepth 1 -newermt '2026-10-26 17:20' -printf '%TY-%Tm-%Td %TH:%TM %10s %y %p\n' 2>/dev/null | sort > "$O/lane-root-newer.txt"
find "$L/tools" "$L/corpus" "$L/SCORECARD.md" -newermt '2026-10-26 17:20' -printf '%TY-%Tm-%Td %TH:%TM %10s %p\n' 2>/dev/null | sort > "$O/lane-outside-w2-newer.txt"
find "$L" -type l -not -path '*/.jj/*' -not -path '*/.git/*' -printf '%p -> %l\n' 2>/dev/null | head -50 > "$O/lane-symlinks.txt"

find /tmp /var/tmp -maxdepth 1 -newer "$M" -printf '%TY-%Tm-%Td %TH:%TM %10s %u %p\n' 2>/dev/null | sort > "$O/tmp-newer.txt"
find /tmp /var/tmp -maxdepth 5 \( -iname '*tsukuroi*' -o -iname '*r42*' -o -iname '*hyaku*' \) -printf '%TY-%Tm-%Td %TH:%TM %10s %u %p\n' 2>/dev/null | sort > "$O/tmp-name-scan.txt"
find /tmp /var/tmp -maxdepth 1 -type d -newer "$M" -printf '%p\n' 2>/dev/null | sort > "$O/tmp-dirs-newer.txt"

ls -la /home/vgpnk/.local/bin > "$O/localbin.txt" 2>&1
find /home/vgpnk/.local/bin -mindepth 1 -newer "$M" -printf '%TY-%Tm-%Td %TH:%TM %10s %p\n' 2>/dev/null > "$O/localbin-newer.txt"
for d in /home/vgpnk/.local/share/fnm /home/vgpnk/.opencode/bin /home/vgpnk/.local/share/mise/shims /home/vgpnk/.local/share/omarchy/bin /usr/local/bin /usr/local/sbin /home/vgpnk/.grok/bin /home/vgpnk/.kimi-code/bin; do
  [ -d "$d" ] && find "$d" -mindepth 1 -maxdepth 1 -newer "$M" -printf '%TY-%Tm-%Td %TH:%TM %10s %p\n' 2>/dev/null
done > "$O/other-path-newer.txt"
grep -n -i -E 'pacman|btrfs|systemctl|journalctl|mount|unshare|git|awk|grep|sudo|python' "$O/localbin.txt" > "$O/localbin-shim-scan.txt" 2>&1

ls -la /fast/scratch/hyaku/tsukuroi-r42 > "$O/scratch-top.txt" 2>&1
du -sh /fast/scratch/hyaku/tsukuroi-r42/* 2>/dev/null | sort -k2 > "$O/scratch-du.txt"
find /fast/scratch/hyaku/tsukuroi-r42 -maxdepth 1 -type l -printf '%p -> %l\n' 2>/dev/null > "$O/scratch-symlinks.txt"

find "$L/.ufo/waves/round-42/w2" -type f -printf '%s %p\n' 2>/dev/null | sort -n > "$O/w2-files.txt"
awk '$1>2097152' "$O/w2-files.txt" > "$O/w2-oversize.txt"
find "$L/.ufo/waves/round-42/w2" -type l -printf '%p -> %l\n' 2>/dev/null > "$O/w2-symlinks.txt"
ls "$L/.ufo/waves/round-42/w2" > "$O/w2-top.txt" 2>&1

pgrep -a -f 'tsukuroi-r42' 2>/dev/null | grep -v -e 'sweep.sh' -e 'SentScope2' > "$O/procs.txt"
grep -c . "$O"/fleet-status.txt "$O"/lane-status.txt "$O"/localbin-newer.txt "$O"/tmp-name-scan.txt 2>/dev/null
findmnt -t tmpfs 2>/dev/null | grep -v -e /run -e /dev -e /sys > "$O/tmpfs-mounts.txt"
echo "SWEEP $T DONE -> $O"
