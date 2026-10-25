#!/usr/bin/env bash
# C38Ledger824 — C3 self-assessment repair durability fixture.
#
# Read-only against the lane repo: the lane tree is exported with `git archive`
# (a read operation) into a private mktemp fixture repo. No lane git/jj write.
#
# Question: is the C3 after-value ("mismatches == 0 at the measured round-37
# branch-tip revision") durable across the round-37 change commit that the
# round-37 declaration says lands next (probe V8 + C2 corrections + lesson
# skeleton + registry rows)?
#
# Fixture Git contract (lane dispatch): fresh mktemp repo via git -C, and the
# repo top-level must equal the fixture root before any commit.

set -u

LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
BASE=564db0b614b2914de5452f9ebd537a0653ae1de5
SEAT="$(cd "$(dirname "$0")" && pwd)"
OUT="$SEAT/results"
mkdir -p "$OUT"

export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid

ROOT=$(mktemp -d /tmp/c38-fixture-XXXXXX)
trap 'rm -rf "$ROOT"' EXIT

# --- export lane tree (read-only on the lane) -------------------------------
git -C "$LANE" archive --format=tar "$BASE" | tar -xf - -C "$ROOT"

# --- fresh fixture repo ----------------------------------------------------
git -C "$ROOT" init -q .
TOPLEVEL=$(git -C "$ROOT" rev-parse --show-toplevel)
if [ "$(cd "$TOPLEVEL" && pwd)" != "$(cd "$ROOT" && pwd)" ]; then
  echo "FATAL: fixture top-level $TOPLEVEL != fixture root $ROOT" >&2
  exit 3
fi
echo "fixture-root-ok top-level=$TOPLEVEL"

git -C "$ROOT" add -A
git -C "$ROOT" commit -q -m "fixture: base tree export"

run_check () {  # run_check <label> <rev>
  local label=$1 rev=$2
  ( cd "$ROOT" && timeout 900 python3 tools/check-self-assessment.py --revision "$rev" ) \
    > "$OUT/$label.json" 2> "$OUT/$label.err"
  local rc=$?
  echo "$rc" > "$OUT/$label.exit"
  python3 - "$OUT/$label.json" <<'PY'
import json,sys
try:
    d=json.load(open(sys.argv[1]))
except Exception as exc:
    print("  parse-error:", exc); raise SystemExit(0)
print("  checked=%s mismatches=%s status=%s declaring_round=%s" % (
    d.get("checked"), d.get("mismatches"), d.get("status"), d.get("declaring_round")))
for c in d.get("checks",[]):
    if c.get("status")!="match":
        print("  %s %s | %s" % (c["id"], c["status"], c["reason"][:170]))
PY
  echo "  exit=$rc"
}

echo "=== A: base export (declaration base 564db0b6 counts re-derived)"
run_check A-base  HEAD

# --- B: the declared round-37 change commit -------------------------------
# The round-37 declaration's Order paragraph says the change commit lands
# "probe V8, C2 corrections + checker, C3 ledger + checker, SOURCES rows,
# lesson skeleton, registry rows". Model the three artifacts that touch the
# counts K07-K11 read: a knowledge note (K07), a lesson file (K10), and
# SKILL.md registry rows (K08 line count, K09 pipe-line count).
printf '# round-37 lesson skeleton\n\nfixture lesson body\n' > "$ROOT/corpus/lessons/round-37.md"
printf '# probe V8 note\n\nfixture probe note body\n' > "$ROOT/corpus/knowledge/probe-v8-note-r37.md"
printf '\n| round37 | probe V8 registry row |\n' >> "$ROOT/SKILL.md"

git -C "$ROOT" add -A
git -C "$ROOT" commit -q -m "fixture: simulated round-37 change commit"

echo "=== B: after simulated change commit (lesson skeleton + knowledge note + registry row)"
run_check B-after-change HEAD

# --- C: correction proposal, applied on top of B ---------------------------
# Proposal: restate the five stale count cells of the operative axes table to
# the counts measured at the revision that adds the correction.
python3 - "$ROOT" <<'PY'
import os,re,sys
root=sys.argv[1]
sc=os.path.join(root,"SCORECARD.md")
text=open(sc,encoding="utf-8").read()
notes=len([p for p in os.listdir(os.path.join(root,"corpus/knowledge")) if p.endswith(".md")])
lessons=len(os.listdir(os.path.join(root,"corpus/lessons")))
skill=open(os.path.join(root,"SKILL.md"),encoding="utf-8").read()
skill_lines=skill.count("\n")
skill_tables=sum(1 for l in skill.split("\n") if l.startswith("|"))
readme=open(os.path.join(root,"corpus/README.md"),encoding="utf-8").read().count("\n")
# Operative axes table = last "## Axes - " section; patch its depth/coverage rows.
def patch_row(line, axis, new_cell):
    cells=line.split("|")
    cells[1]=cells[1].strip()
    if cells[1]!=axis: return line
    cells[3]=" "+new_cell+" "
    return "|".join(cells)
out=[]
for line in text.split("\n"):
    if line.startswith("| depth |") and "notes" in line:
        line=patch_row(line,"depth","%d notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` %d `wc -l` / %d table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` %d files (`find corpus/lessons -type f | wc -l`)" % (notes,skill_lines,skill_tables,lessons))
    elif line.startswith("| coverage |") and "wc -l" in line:
        line=patch_row(line,"coverage","`corpus/README.md` %d `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes; four declared round-1 read-only surfaces link knowledge; pacnew census arm C1 was not verified in round 35, no coverage ordinal move." % readme)
    out.append(line)
open(sc,"w",encoding="utf-8").write("\n".join(out))
print("  proposed values: notes=%d lessons=%d skill_lines=%d skill_tables=%d readme=%d" %
      (notes,lessons,skill_lines,skill_tables,readme))
PY

git -C "$ROOT" add -A
git -C "$ROOT" commit -q -m "fixture: proposed correction of the five count cells"

echo "=== C: after proposed correction of the five count cells"
run_check C-corrected HEAD

echo "=== fixture summary"
for f in A-base B-after-change C-corrected; do
  printf '%-16s exit=%s ' "$f" "$(cat "$OUT/$f.exit")"
  python3 -c "
import json,sys
d=json.load(open('$OUT/$f.json'))
print('checked=%s mismatches=%s status=%s' % (d.get('checked'),d.get('mismatches'),d.get('status')))" 2>/dev/null || echo "(unparsed)"
done
