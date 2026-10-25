#!/usr/bin/env bash
# C32Ledger218 — hermetic fixture for C3 falsification item 2/8 (self-assessment mismatch repair).
# Builds two fresh git repos at the seat: "before" = the operative state at the
# round-37 declaration/repair base (revision ee36f9e), "after" = the same tree
# with the single K17 self-assessment row corrected. Both are then evaluated with
# the UNCHANGED lane checker (tools/check-self-assessment.py). No lane/fleet/jj
# state is touched; all git operations are scoped to the fixture roots via -C.
set -euo pipefail

LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
REV=ee36f9e829f640def6b3c6ab3e31c4ed7186c6eb
SEAT=$LANE/.ufo/waves/round-37/w1/C32Ledger218
mkdir -p "$SEAT"

# --- 1. compute the exact set of repo paths the checker parses at REV --------
python3 - "$LANE" "$REV" "$SEAT/members.txt" <<'EOF'
import importlib.util, sys
lane, rev, out = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("csa", lane + "/tools/check-self-assessment.py")
csa = importlib.util.module_from_spec(spec); spec.loader.exec_module(csa)
blobs = {p: csa.show_blob(lane, rev, p) for p in
         ("SCORECARD.md", "SHONEN.md", "PROVINCE.md", "SKILL.md", "corpus/README.md")}
tree = csa.list_paths(lane, rev)
need = set()
for text in blobs.values():
    for t in csa.path_candidates(text):
        for p in csa.resolve_paths([t], tree):
            need.add(p)
# K07/K10 count subtrees; K16-K19 / SHONEN cites
for p in tree:
    if p.startswith("corpus/knowledge/") or p.startswith("corpus/lessons/") or p in (
            "SCORECARD.md", "SHONEN.md", "PROVINCE.md", "SKILL.md",
            "corpus/README.md", "corpus/SOURCES.md",
            "tools/tsukuroi-census.sh", "tools/boot-chain-audit.sh"):
        need.add(p)
members = sorted(p for p in need if p in tree)
open(out, "w").write("\n".join(members) + "\n")
print("members:", len(members))
EOF

# --- 2. helper: init fixture, verify top-level == fixture root, commit -------
init_commit() {
  local root=$1 msg=$2
  mkdir -p "$root"
  git -C "$root" init -q
  git -C "$root" config user.name "c32-fixture"
  git -C "$root" config user.email "c32-fixture@example.invalid"
  # verify top-level equals fixture root before any commit
  local top
  top=$(git -C "$root" rev-parse --show-toplevel)
  [ "$top" = "$root" ] || { echo "TOPLEVEL MISMATCH: $top != $root"; exit 1; }
  echo "verified toplevel $top == fixture root"
  git -C "$root" add -A
  git -C "$root" commit -q -m "$msg"
  git -C "$root" rev-parse HEAD
}

# --- 3. fixture-before: exact tree at REV ------------------------------------
BEFORE=$SEAT/fixture-before
mkdir -p "$BEFORE"
git -C "$LANE" archive "$REV" | tar -x -C "$BEFORE" -T "$SEAT/members.txt"
B=$(init_commit "$BEFORE" "c32 fixture before: round-37 base ee36f9e (K17 stale row)")
python3 "$LANE/tools/check-self-assessment.py" --repo "$BEFORE" --revision HEAD \
  > "$SEAT/before-check.json" 2> "$SEAT/before-check.err" || true
echo "before commit $B"

# --- 4. fixture-after: same tree, one corrected K17 row -----------------------
AFTER=$SEAT/fixture-after
cp -a "$BEFORE" "$AFTER"
python3 - "$AFTER/SCORECARD.md" <<'EOF'
import re, sys
p = sys.argv[1]
lines = open(p, encoding="utf-8").read().split("\n")
target = "with a hermetic census selftest"
repl = "with a hermetic selftest that prints PASS (105 cases, 105 passed, 0 failed)"
hits = 0
for i, line in enumerate(lines):
    if line.startswith("| host-census-gate |") and target in line:
        assert "105 cases" not in line, ("already corrected?", i)
        lines[i] = line.replace(target, repl, 1)
        hits += 1
assert hits == 1, ("expected exactly one host-census-gate row to patch", hits)
open(p, "w", encoding="utf-8").write("\n".join(lines))
print("patched row line", next(i for i, l in enumerate(lines, 1) if l.startswith("| host-census-gate |")))
EOF
git -C "$AFTER" add -A
A=$(init_commit "$AFTER" "c32 fixture after: one-line K17 self-assessment correction")
python3 "$LANE/tools/check-self-assessment.py" --repo "$AFTER" --revision HEAD \
  > "$SEAT/after-check.json" 2> "$SEAT/after-check.err" || true
echo "after commit $A"

echo "== before summary =="
python3 -c "
import json
d=json.load(open('$SEAT/before-check.json'))
m=[c for c in d['checks'] if c['status']=='mismatch']
print('exit_status', d['status'], 'checked', d['checked'], 'mismatches', d['mismatches'])
for c in m: print(c['id'], c['status'], 'stated=', c.get('stated'), 'observed=', c.get('observed'), '|', c['reason'])
"
echo "== after summary =="
python3 -c "
import json
d=json.load(open('$SEAT/after-check.json'))
m=[c for c in d['checks'] if c['status']=='mismatch']
print('exit_status', d['status'], 'checked', d['checked'], 'mismatches', d['mismatches'])
for c in m: print(c['id'], c['status'], c['reason'])
"
