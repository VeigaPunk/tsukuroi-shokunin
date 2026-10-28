#!/usr/bin/env bash
S=/fast/scratch/hyaku/tsukuroi-r48/TExecEdgeChars
mount -t tmpfs none /tmp || { echo "mount failed"; exit 9; }
echo "== /tmp at start: $(ls -A /tmp | wc -l) entries =="
echo "== control A: TMPDIR unset (documented: fixture in /tmp) =="
( cd "$S" && env -i PATH=/usr/bin:/bin LC_ALL=C timeout 300 bash "$S/census.sh" --selftest ) >"$S/out.ns-unset.log" 2>&1
echo "rc=$? last=$(tail -1 "$S/out.ns-unset.log")"
echo "tmp entries seen during/after: $(ls -A /tmp | wc -l): $(ls -A /tmp | head -3 | tr '\n' ' ')"
rm -rf /tmp/tsukuroi-r3-2-selftest.* 2>/dev/null
echo "== dirty tab TMPDIR (alias; must not touch /tmp) =="
val="$S/e1tab"$'\t'"x"
( cd "$S" && env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$val" timeout 300 bash "$S/census.sh" --selftest ) >"$S/out.ns-tab.log" 2>&1
echo "rc=$? last=$(tail -1 "$S/out.ns-tab.log")"
echo "tmp entries after dirty run: $(ls -A /tmp | wc -l): $(ls -A /tmp | head -3 | tr '\n' ' ')"
