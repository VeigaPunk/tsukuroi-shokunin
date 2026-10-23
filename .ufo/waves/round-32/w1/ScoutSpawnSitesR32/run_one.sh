#!/bin/bash
# usage: run_one.sh <mode A|B> <tool> [args...]
set -u
S=/fast/scratch/hyaku/tsukuroi-r32/ScoutSpawnSitesR32
mode=$1; tool=$2; shift 2
name=$(basename "$tool" .py)-$mode
work=$S/runs/$name
rm -rf "$work"; mkdir -p "$work/home/.config" "$work/tmp"
cp -a $S/tree "$work/tree"
cd "$work/tree"
start=$(date +%s)
if [ "$mode" = A ]; then
  env $(env | cut -d= -f1 | grep -E '^(GIT_|LD_|PYTHON)' | sed 's/^/-u /') PATH=/usr/bin:/bin LC_ALL=C HOME="$work/home" XDG_CONFIG_HOME="$work/home/.config" TMPDIR="$work/tmp" \
    timeout 1500 strace -f -qq -v -s 65536 -e trace=execve -o "$work/trace" -- /usr/bin/python3 "$work/tree/$tool" "$@" >"$work/stdout" 2>"$work/stderr"
else
  timeout 1500 env -i PATH=/usr/bin:/bin /usr/bin/python3 "$work/tree/$tool" "$@" >"$work/stdout" 2>"$work/stderr"
fi
rc=$?
end=$(date +%s)
norm=$(sed -e "s#$work#<WORK>#g" -e "s#$S#<ROOT>#g" -e 's#/tmp/[A-Za-z0-9_.-]*#<TMP>#g' "$work/stdout" | sed -E 's/[0-9a-f]{64}|[0-9a-f]{40}/<HEX>/g' | sha256sum | cut -c1-16)
echo "$name rc=$rc secs=$((end-start)) stdout_lines=$(wc -l <"$work/stdout") norm=$norm" | tee "$work/summary"
rm -rf "$work/tree"
