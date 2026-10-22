#!/usr/bin/env bash
# Read-only toward the lane: archive the measured revision, mutate private copies, run the committed tool.
set -u
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
REV=5e7c04ecb02735491456de2b8bc44550d0db4609
W=/fast/scratch/hyaku/tsukuroi-r25/w2/CritC1Construction
TOOL="$W/tool/check-self-assessment.py"
mkdir -p "$W/tool" "$W/out"
git -C "$LANE" show "$REV:tools/check-self-assessment.py" > "$TOOL"

mk() {  # mk <name> <python mutation snippet operating on dir d>
  local name=$1 snippet=$2 d="$W/sb/$1"
  rm -rf "$d"; mkdir -p "$d"
  git -C "$LANE" archive "$REV" | tar -x -C "$d"
  ( cd "$d" && python3 -c "$snippet" ) || { echo "$name mutation-failed"; return; }
  git -C "$d" init -q
  git -C "$d" add -A
  git -C "$d" -c user.name=crit -c user.email=crit@example.invalid commit -q -m "$name"
  python3 "$TOOL" --revision HEAD --repo "$d" > "$W/out/$name.json"
  local rc=$?
  python3 - "$name" "$rc" "$W/out/$name.json" <<'EOF'
import json, sys
name, rc, path = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(path))
bad = [(c["id"], c.get("observed_line"), c["reason"][:160]) for c in d["checks"] if c["status"] == "mismatch"]
ords = {c["id"]: c.get("observed_line") for c in d["checks"] if c["id"] in ("K01","K04","K05")}
print("%s exit=%s mismatches=%s ordinal_lines=%s" % (name, rc, d.get("mismatches"), ords))
for b in bad: print("   ", b)
EOF
  rm -rf "$d"
}

R='import re,io
p="SCORECARD.md"; s=open(p,encoding="utf-8").read()
def sub(a,b):
    global s
    assert s.count(a)==1, (a, s.count(a)); s=s.replace(a,b)
'
W_='
open(p,"w",encoding="utf-8").write(s)'

mk M0-unmodified 'pass'
mk M1-refinement-example "$R"'sub("`freshness (actual 9 → 9` is","`freshness (actual 7 → 7` is")'"$W_"
mk M2-planned-inflation "$R"'
head,sep,tail=s.partition("## Axes — current self-assessment (round 25)")
assert sep
for ax,old in (("depth",8),("coverage",9),("operability",9),("freshness",9),("calibration",9),("adjacency",8)):
    tail,n=re.subn(r"(\n\| %s \| )%d( \|)"%(ax,old), r"\g<1>10\2", tail, count=1); assert n==1, ax
s=head+sep+tail
s+="\nPlanned next round: depth 8 → 10, coverage 9 → 10, operability 9 → 10, freshness 9 → 10, calibration 9 → 10, adjacency 8 → 10.\n"'"$W_"
mk M3-false-pointers "$R"'sub("`## Frontier` at `PROVINCE.md:75`","`## Frontier` at `PROVINCE.md:999`")
sub("move-log row at `SCORECARD.md:30`","move-log row at `SCORECARD.md:1`")
sub("125 rows at round 25","999 rows at round 25")
sub("its selftest prints PASS total=45 failed=0","its selftest prints FAIL total=45 failed=45")'"$W_"
mk M4-underscore-token "$R"'s+="\nA note on depth_5 → 5 naming.\n"'"$W_"
mk M5-shonen-slash 'p="SHONEN.md"; s=open(p).read(); a="observation and request"; assert s.count(a)==1; open(p,"w").write(s.replace(a,"observation/request"))'
mk M6-contradicting-tokens "$R"'sub("D12 `--identity` not landed,","D12 `--identity` not landed and `--identity` landed,")'"$W_"
