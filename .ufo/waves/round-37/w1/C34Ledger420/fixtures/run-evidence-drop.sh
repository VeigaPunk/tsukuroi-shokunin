#!/usr/bin/env bash
# C34Ledger420 — (a) rigorous named-path-set diff between the base capabilities
# table and the tip capabilities table, and (b) a corrected F13 that edits the
# OPERATIVE (last) axes table rather than the superseded one.
#
# Read-only against the lane repo. Fresh mktemp repos only; top-level verified
# equal to the fixture root before any commit.
set -uo pipefail

LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
OUT=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-37/w1/C34Ledger420/fixtures/out
CHECKER="$LANE/tools/check-self-assessment.py"
BASE=564db0b614b2914de5452f9ebd537a0653ae1de5
TIP=0e5f70fadba12bc9bbb9db564c2262c2c0194535

echo "===== (a) named-path-set diff, base capabilities table vs tip ====="
python3 - "$LANE" "$BASE" "$TIP" <<'PY'
import re, subprocess, sys
lane, base_rev, tip_rev = sys.argv[1], sys.argv[2], sys.argv[3]
def blob(rev):
    return subprocess.run(['git','-C',lane,'show',rev+':SCORECARD.md'],
                          capture_output=True,text=True).stdout.split('\n')
def split_cells(line):
    cells=[];cur=[];code=False
    for ch in line:
        if ch=='`': code=not code; cur.append(ch); continue
        if ch=='|' and not code: cells.append(''.join(cur)); cur=[]; continue
        cur.append(ch)
    cells.append(''.join(cur))
    if cells and not cells[0].strip(): cells=cells[1:]
    if cells and not cells[-1].strip(): cells=cells[:-1]
    return [c.strip() for c in cells]
def last_caps_table(lines):
    found=None
    for i,l in enumerate(lines):
        if re.match(r'^##\s+Capabilities\b',l): found=i
    end=len(lines)
    for j in range(found+1,len(lines)):
        if re.match(r'^##\s',lines[j]): end=j; break
    rows=None
    for l in lines[found+1:end]:
        if l.lstrip().startswith('|'): rows=split_cells(l)
    # rebuild the table (the loop above kept the last pipe row only) -> redo properly
    blocks=[];i=found+1
    while i<end:
        if lines[i].lstrip().startswith('|'):
            lo=i
            while i<end and lines[i].lstrip().startswith('|'): i+=1
            blocks.append([split_cells(r) for r in lines[lo:i]])
        else: i+=1
    for b in reversed(blocks):
        if b and b[0] and b[0][0].strip().lower()=='capability': return b
    return blocks[-1] if blocks else None
PATH_SUFFIXES=(".md",".json",".py",".sh",".txt")
CHARSET=re.compile(r"[A-Za-z0-9_.{},/-]+")
def path_candidates(text):
    out=[]
    for raw in CHARSET.findall(text or ""):
        t=raw.rstrip(".,;:)")
        if not t or t.startswith("/") or t.startswith("-"): continue
        if not re.fullmatch(r"[A-Za-z0-9_.{},/-]+",t): continue
        if "/" in t or t.endswith(PATH_SUFFIXES): out.append(t)
    return out
def named_paths(row):
    cell=" ".join(row[1:])
    toks=[]
    for span in re.findall(r"`([^`]*)`",cell): toks.extend(span.split())
    out=[]
    for t in toks:
        for c in path_candidates(t):
            if c not in out: out.append(c)
    return out
bt=last_caps_table(blob(base_rev)); tt=last_caps_table(blob(tip_rev))
bmap={r[0].strip().strip('`').lower(): named_paths(r) for r in bt[1:] if r}
tmap={r[0].strip().strip('`').lower(): named_paths(r) for r in tt[1:] if r}
tree=set(subprocess.run(['git','-C',lane,'ls-tree','-r','--name-only',tip_rev],
                         capture_output=True,text=True).stdout.split('\n'))
tree={t.rstrip('/') for t in tree if t.strip()}
print("%-26s %-3s %-3s %s" % ("capability","base","tip","delta"))
for k in bmap:
    b=bmap[k]; t=tmap.get(k,[])
    dropped=[x for x in b if x not in t]; added=[x for x in t if x not in b]
    still=[x for x in dropped if x in tree]
    print("%-26s %-3d %-3d dropped=%s (still in tip tree: %d/%d) added=%s"
          % (k,len(b),len(t),dropped,len(still),len(dropped),added))
print()
print("total named paths: base=%d tip=%d" % (sum(len(v) for v in bmap.values()),
                                             sum(len(v) for v in tmap.values())))
PY

echo
echo "===== (b) corrected F13: edit the OPERATIVE (last) depth row ====="
ROOT=$(mktemp -d /tmp/c34-f13b-last-XXXXXX)
git -C "$LANE" archive --format=tar "$TIP" | tar -x -C "$ROOT"
git -C "$ROOT" init -q
TOP=$(git -C "$ROOT" rev-parse --show-toplevel)
if [ "$TOP" != "$ROOT" ]; then echo "ABORT: top-level $TOP != $ROOT" >&2; exit 3; fi
git -C "$ROOT" add -A
git -C "$ROOT" -c user.name=c34 -c user.email=c34@example.invalid commit -q -m "fixture: lane tip tree"
python3 - "$ROOT/SCORECARD.md" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
old="| depth | 8 | 56 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`);"
new="| depth | 8 | 57 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`);"
assert s.count(old)==2, "expected 2 occurrences, got %d" % s.count(old)
i=s.rfind(old)                      # the LAST occurrence is the operative table
open(p,"w").write(s[:i]+new+s[i+len(old):])
print("edited occurrence at char offset",i,"(the operative table)")
PY
git -C "$ROOT" add -A
git -C "$ROOT" -c user.name=c34 -c user.email=c34@example.invalid commit -q -m "fixture: operative depth row notes 56 -> 57"
( cd "$ROOT" && python3 "$CHECKER" --revision HEAD --repo "$ROOT" ) > "$OUT/F13b-tip-operative-depth-row-57.json" 2>/dev/null
rc=$?
python3 - "$OUT/F13b-tip-operative-depth-row-57.json" "$rc" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print("F13b exit=%s status=%s mismatches=%s checked=%s" % (sys.argv[2],d.get('status'),d.get('mismatches'),d.get('checked')))
for c in d.get('checks',[]):
    if c['status']=='mismatch': print("  MISMATCH",c['id'],'|',c['reason'][:150])
PY

echo
echo "===== (c) F14: append a NEW '## Axes' table with a WRONG count ====="
# Does the checker read the LAST '## Axes - ' table? A later round appending a
# fresh axes table with a stale count must be caught by the same K07.
ROOT=$(mktemp -d /tmp/c34-f14-newaxes-XXXXXX)
git -C "$LANE" archive --format=tar "$TIP" | tar -x -C "$ROOT"
git -C "$ROOT" init -q
TOP=$(git -C "$ROOT" rev-parse --show-toplevel)
if [ "$TOP" != "$ROOT" ]; then echo "ABORT: top-level $TOP != $ROOT" >&2; exit 3; fi
git -C "$ROOT" add -A
git -C "$ROOT" -c user.name=c34 -c user.email=c34@example.invalid commit -q -m "fixture: lane tip tree"
cat >> "$ROOT/SCORECARD.md" <<'EOF'

## Axes — current self-assessment (round 38)

A later round's axes table, appended in the same idiom.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 58 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3110 `wc -l` / 839 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 49 files (`find corpus/lessons -type f | wc -l`) | round 38 |
| coverage | 9 | `corpus/README.md` 269 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present | round 38 |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (105 cases, 105 passed, 0 failed); `--identity` not landed | round 38 |
| freshness | 9 | receipts | round 38 |
| calibration | 9 | receipts | round 38 |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) | round 38 |
EOF
git -C "$ROOT" add -A
git -C "$ROOT" -c user.name=c34 -c user.email=c34@example.invalid commit -q -m "fixture: + round-38 axes table with stale note count"
( cd "$ROOT" && python3 "$CHECKER" --revision HEAD --repo "$ROOT" ) > "$OUT/F14-tip-plus-round38-axes-table.json" 2>/dev/null
rc=$?
python3 - "$OUT/F14-tip-plus-round38-axes-table.json" "$rc" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print("F14 exit=%s status=%s mismatches=%s checked=%s axes_heading=%s declaring_round=%s"
      % (sys.argv[2],d.get('status'),d.get('mismatches'),d.get('checked'),d.get('axes_heading'),d.get('declaring_round')))
for c in d.get('checks',[]):
    if c['status']=='mismatch': print("  MISMATCH",c['id'],'|',c['reason'][:150])
PY
echo "DONE"
