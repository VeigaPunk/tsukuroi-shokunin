#!/bin/bash
# G-4 input-provenance witnesses for the two round-39 counters, in a throwaway clone.
set -u
S=/fast/scratch/hyaku/tsukuroi-r39/GateRevisionBind
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
PX=$S/px
TIP=394e1ba4fab39a417abe66a7802f87cf1ff8dd61
PARENT=2e1c2a40c13dc52e155d89e72f3fdd560db7399a
PRE=93fddb2c37aed8227b4a0ff2417b104e01446a9d
rm -rf "$PX"
git clone -q --shared "$LANE" "$PX" || exit 1
git -C "$PX" remote remove origin
git -C "$PX" update-ref refs/remotes/origin/master "$TIP"
[ "$(git -C "$PX" rev-parse --show-toplevel)" = "$PX" ] || { echo "wrong toplevel"; exit 1; }
cd "$PX" || exit 1
export TMPDIR=$S/px-scratch; mkdir -p "$TMPDIR"
summ() {  # read JSON on stdin, print the fields that decide the predicate
  python3 -c 'import json,sys
d=json.load(sys.stdin)
keys=("revision","entry_present","rules_verified","duplicate_rows","duplicate_headings","source_ok",
      "counts_ok","oracle_violations","hidden_matched","views_matched","fixtures_matched",
      "live_match","six_planes_all","result","error")
print(" ".join("%s=%s"%(k,d[k]) for k in keys if k in d) or "NO-JSON")'
}

echo "=== C2 baseline at tip ==="
python3 tools/check-transaction-order-r39.py --repo . --revision "$TIP" > "$S/c2-base.json"; echo "rc=$?"
summ < "$S/c2-base.json"

echo "=== C2 (a) worktree entry has one appended bogus row ==="
printf '| TO9 | bogus | S213 trans.c:1-2 “x y z w” | n/a |\n' >> corpus/knowledge/pacman-transaction-order-r39.md
python3 tools/check-transaction-order-r39.py --repo . --revision "$TIP" > "$S/c2-a-entry.json"; echo "rc=$?"
summ < "$S/c2-a-entry.json"
git checkout -- corpus/knowledge/pacman-transaction-order-r39.md

echo "=== C2 (b) worktree frozen/src/trans.c altered ==="
printf '\n// tamper\n' >> .ufo/waves/round-39/frozen/src/trans.c
python3 tools/check-transaction-order-r39.py --repo . --revision "$TIP" > "$S/c2-b-src.json"; echo "rc=$?"
summ < "$S/c2-b-src.json"
git checkout -- .ufo/waves/round-39/frozen/src/trans.c

echo "=== C2 (c) worktree frozen/txcapture/pacman.log altered ==="
printf '\n[2026-10-26T00:00:00+0000] [ALPM] tamper\n' >> .ufo/waves/round-39/frozen/txcapture/pacman.log
python3 tools/check-transaction-order-r39.py --repo . --revision "$TIP" > "$S/c2-c-cap.json"; echo "rc=$?"
summ < "$S/c2-c-cap.json"
git checkout -- .ufo/waves/round-39/frozen/txcapture/pacman.log

echo "=== C2 (d) at pre-entry revision 93fddb2 ==="
python3 tools/check-transaction-order-r39.py --repo . --revision "$PRE" > "$S/c2-d-pre.json"; echo "rc=$?"
summ < "$S/c2-d-pre.json"

echo "=== C2 (e) tool copied away from its frozen tree ==="
mkdir -p "$S/c2-copy/tools"
cp tools/check-transaction-order-r39.py tools/_revision.py "$S/c2-copy/tools/"
python3 "$S/c2-copy/tools/check-transaction-order-r39.py" --repo . --revision "$TIP" > "$S/c2-e-copy.json"; echo "rc=$?"
summ < "$S/c2-e-copy.json"

echo "=== C1 baseline at tip ==="
python3 tools/score-storage-hidden-r39.py --repo . --revision "$TIP" --scratch "$S/c1-base-sc" > "$S/c1-base.json"; echo "rc=$?"
summ < "$S/c1-base.json"

echo "=== C1 (a) worktree tools/tsukuroi-census.sh replaced by a fabricated reporter ==="
git show "$TIP:tools/tsukuroi-census.sh" | sha256sum
cat > tools/tsukuroi-census.sh <<'EOF'
#!/bin/bash
for p in boot systemd kernel driver journal oom; do echo "PLANE $p state=OK"; done
echo "STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0"
echo "TSUKUROI_CENSUS: fabricated worktree reporter"
EOF
sha256sum tools/tsukuroi-census.sh
python3 tools/score-storage-hidden-r39.py --repo . --revision "$TIP" --scratch "$S/c1-a-sc" > "$S/c1-a-worktree.json"; echo "rc=$?"
summ < "$S/c1-a-worktree.json"
git checkout -- tools/tsukuroi-census.sh

echo "=== C1 (b) at pre-fix revision 93fddb2 ==="
python3 tools/score-storage-hidden-r39.py --repo . --revision "$PRE" --scratch "$S/c1-b-sc" > "$S/c1-b-pre.json"; echo "rc=$?"
summ < "$S/c1-b-pre.json"
echo "=== done ==="
