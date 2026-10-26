#!/usr/bin/env bash
# Sequential scorer: frozen C1 counter on each revision, then a standalone
# --selftest run of the script bytes at that revision.
set -u
S=/fast/scratch/hyaku/tsukuroi-r43/C1MutFinal
D=$(cat "$S/fx.path")
COUNTER=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-bootinputs-r43.py

run_one() {
    local name=$1 rev=$2
    printf '# %s %s\n' "$name" "$rev" >> "$S/runs.jsonl"
    python3 "$COUNTER" --lane "$D" --revision "$rev" --scratch "$S/csr" >> "$S/runs.jsonl" 2>>"$S/runs.err"
    echo "$? $name $rev" >> "$S/runs.rc"
    local sp="$S/st/$rev.sh"
    git -C "$D" show "$rev:tools/boot-chain-audit.sh" > "$sp"
    mkdir -p "$S/st/$rev-st"
    TMPDIR="$S/st/$rev-st" bash "$sp" --selftest > "$S/st/$rev.selftest.out" 2>&1
    echo "selftest_rc=$? $name $rev" >> "$S/runs.rc"
}

run_one baseline 8acf0b022586a0f3164c77659fb96ba5f90949b6
while read -r x sha; do
    run_one "$x" "$sha"
done < "$S/shas.tsv"
echo DONE
