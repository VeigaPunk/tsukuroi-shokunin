#!/usr/bin/env bash
# C38Ledger824 — C3 repair-scope attribution fixture.
#
# Read-only against the lane repo: the lane tree is exported with `git archive`
# (a read operation) into a private mktemp fixture repo; the lane's own
# SCORECARD.md blobs are read with `git show`. No lane git/jj write.
#
# Question the lane's own receipts raise: the C3 declaration scopes the repair
# to "append-only correction of the five current self-assessment count cells"
# and declares the after-value "mismatches 0, checked 27, exit 0". But the
# lane's receipt after-c3-d06ced.json (the commit that carried the five-cell
# correction) reads mismatches=2, and after-c3-5124bf.json reads
# CANNOT_EVALUATE (exit 2). This fixture replays the exact SCORECARD.md blob
# of every landed correction commit on top of the base tree export and scores
# each with the UNCHANGED checker, to attribute which edit produced which
# mismatch count.
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

ROOT=$(mktemp -d /tmp/c38-scope-XXXXXX)
trap 'rm -rf "$ROOT"' EXIT

git -C "$LANE" archive --format=tar "$BASE" | tar -xf - -C "$ROOT"

git -C "$ROOT" init -q .
TOPLEVEL=$(git -C "$ROOT" rev-parse --show-toplevel)
if [ "$(cd "$TOPLEVEL" && pwd)" != "$(cd "$ROOT" && pwd)" ]; then
  echo "FATAL: fixture top-level $TOPLEVEL != fixture root $ROOT" >&2
  exit 3
fi
echo "fixture-root-ok top-level=$TOPLEVEL"

git -C "$ROOT" add -A
git -C "$ROOT" commit -q -m "fixture: base tree export"

run_check () {  # run_check <label>
  local label=$1
  ( cd "$ROOT" && timeout 900 python3 tools/check-self-assessment.py --revision HEAD ) \
    > "$OUT/$label.json" 2> "$OUT/$label.err"
  local rc=$?
  echo "$rc" > "$OUT/$label.exit"
  python3 - "$OUT/$label.json" <<'PY'
import json,sys
try:
    d=json.load(open(sys.argv[1]))
except Exception as exc:
    print("  parse-error:", exc); raise SystemExit(0)
if d.get("status")=="CANNOT_EVALUATE":
    print("  CANNOT_EVALUATE: %s (%s)" % (d.get("error"), d.get("detail")))
else:
    print("  checked=%s mismatches=%s status=%s declaring_round=%s" % (
        d.get("checked"), d.get("mismatches"), d.get("status"), d.get("declaring_round")))
    for c in d.get("checks",[]):
        if c.get("status")!="match":
            print("  %s %s | %s" % (c["id"], c["status"], c["reason"][:165]))
PY
  echo "  exit=$rc"
}

echo "=== S0: base export, untouched"
run_check S0-base

# --- S1: base + ONLY the five-cell axes correction (no capabilities edit) ----
# The correction proposal: restate the five stale count cells of the operative
# axes table to the counts measured at this revision, and touch nothing else.
cp "$ROOT/SCORECARD.md" "$OUT/SCORECARD.base.md"
python3 - "$ROOT" <<'PY'
import os,sys
root=sys.argv[1]
sc=os.path.join(root,"SCORECARD.md")
text=open(sc,encoding="utf-8").read()
def count(pat):
    return len([p for p in os.listdir(os.path.join(root,pat)) if p.endswith(".md")])
notes=count("corpus/knowledge")
lessons=len(os.listdir(os.path.join(root,"corpus/lessons")))
skill=open(os.path.join(root,"SKILL.md"),encoding="utf-8").read()
skill_lines=skill.count("\n")
skill_tables=sum(1 for l in skill.split("\n") if l.startswith("|"))
readme=open(os.path.join(root,"corpus/README.md"),encoding="utf-8").read().count("\n")
out=[]
for line in text.split("\n"):
    if line.startswith("| depth |"):
        c=line.split("|"); c[3]=(" %d notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); "
            "`SKILL.md` %d `wc -l` / %d table lines (`grep -c '^|' SKILL.md`); "
            "`corpus/lessons/` %d files (`find corpus/lessons -type f | wc -l`); four standing rules near the top of SKILL cite no knowledge note; no ordinal move claimed."
            % (notes,skill_lines,skill_tables,lessons)); line="|".join(c)
    elif line.startswith("| coverage |"):
        c=line.split("|"); c[3]=(" `corpus/README.md` %d `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes; four declared round-1 read-only surfaces link knowledge; pacnew census arm C1 was not verified in round 35, no coverage ordinal move." % readme); line="|".join(c)
    out.append(line)
open(sc,"w",encoding="utf-8").write("\n".join(out))
print("  corrected counts: notes=%d lessons=%d skill_lines=%d skill_tables=%d readme=%d" % (notes,lessons,skill_lines,skill_tables,readme))
PY
git -C "$ROOT" add -A
git -C "$ROOT" commit -q -m "fixture: five-cell axes correction only"
echo "=== S1: base + five-cell axes correction ONLY (capabilities table untouched)"
run_check S1-axes-only

# --- S2..S4: replay the lane's own landed correction commits verbatim -------
for rev in d06cedb81fc568aa180f65f87343580bba3faa71 \
           ee36f9e829f640def6b3c6ab3e31c4ed7186c6eb \
           5124bf39341f48237516df9bf9f18f5fac3d5a1e \
           0e5f70fadba12bc9bbb9db564c2262c2c0194535; do
  short=${rev:0:7}
  git -C "$ROOT" checkout -q -- "$ROOT/SCORECARD.md" 2>/dev/null || true
  git -C "$LANE" show "$rev:SCORECARD.md" > "$ROOT/SCORECARD.md"
  git -C "$ROOT" add -A
  git -C "$ROOT" commit -q -m "fixture: overlay lane SCORECARD.md at $short"
  echo "=== S-lane-$short: base tree + lane SCORECARD.md at $short"
  run_check "S-lane-$short"
done

echo "=== attribution summary"
printf '%-18s %-6s %s\n' LABEL EXIT "checked/mismatches/status"
for f in "$OUT"/S*.json; do
  lbl=$(basename "$f" .json)
  [ "$lbl" = "S0-base" ] || true
  printf '%-18s %-6s ' "$lbl" "$(cat "$OUT/$lbl.exit" 2>/dev/null)"
  python3 -c "
import json
d=json.load(open('$f'))
print('%s/%s/%s' % (d.get('checked'), d.get('mismatches'), d.get('status')))" 2>/dev/null || echo "(unparsed)"
done
