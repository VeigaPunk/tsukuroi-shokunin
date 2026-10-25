#!/usr/bin/env bash
# C38Ledger824 — C3 re-statement fixture at the post-change-commit tip.
#
# Read-only against the lane repo: the lane tree is exported with `git archive`
# (a read operation) into a private mktemp fixture repo. No lane git/jj write.
#
# Finding under test: the C3 claim's after-value is "the same command at the
# measured round-37 branch-tip revision reports checked: 27, mismatches: 0,
# status: PASS, exit 0". The five count cells are revision-bound: any commit
# that adds a knowledge note, a lesson file, or a SKILL.md line invalidates
# them. This fixture tests whether an append-only re-statement of the five
# cells at the post-change-commit tip restores mismatches 0 under the
# UNCHANGED checker.
#
# Fixture Git contract (lane dispatch): fresh mktemp repo via git -C, and the
# repo top-level must equal the fixture root before any commit.

set -u

LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
BASE=564db0b614b2914de5452f9ebd537a0653ae1de5
TIP=$(git -C "$LANE" rev-parse HEAD)
SEAT="$(cd "$(dirname "$0")" && pwd)"
OUT="$SEAT/results"
mkdir -p "$OUT"

export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@example.invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@example.invalid

ROOT=$(mktemp -d /tmp/c38-tip-XXXXXX)
trap 'rm -rf "$ROOT"' EXIT

echo "exporting lane tip $TIP"
git -C "$LANE" archive --format=tar "$TIP" | tar -xf - -C "$ROOT"

git -C "$ROOT" init -q .
TOPLEVEL=$(git -C "$ROOT" rev-parse --show-toplevel)
if [ "$(cd "$TOPLEVEL" && pwd)" != "$(cd "$ROOT" && pwd)" ]; then
  echo "FATAL: fixture top-level $TOPLEVEL != fixture root $ROOT" >&2
  exit 3
fi
echo "fixture-root-ok top-level=$TOPLEVEL"

git -C "$ROOT" add -A
git -C "$ROOT" commit -q -m "fixture: tip tree export"

run_check () {
  local label=$1
  ( cd "$ROOT" && timeout 900 python3 tools/check-self-assessment.py --revision HEAD ) \
    > "$OUT/$label.json" 2> "$OUT/$label.err"
  local rc=$?
  echo "$rc" > "$OUT/$label.exit"
  python3 - "$OUT/$label.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1]))
print("  checked=%s mismatches=%s status=%s" % (d.get("checked"),d.get("mismatches"),d.get("status")))
for c in d.get("checks",[]):
    if c.get("status")!="match":
        print("  %s %s | %s" % (c["id"],c["status"],c["reason"][:170]))
PY
  echo "  exit=$rc"
}

echo "=== T0: tip export, untouched (the measured round-37 branch tip)"
run_check T0-tip-untouched

python3 - "$ROOT" <<'PY'
import os,sys
root=sys.argv[1]
sc=os.path.join(root,"SCORECARD.md")
notes=len([p for p in os.listdir(os.path.join(root,"corpus/knowledge")) if p.endswith(".md")])
lessons=len(os.listdir(os.path.join(root,"corpus/lessons")))
skill=open(os.path.join(root,"SKILL.md"),encoding="utf-8").read()
skill_lines=skill.count("\n")
skill_tables=sum(1 for l in skill.split("\n") if l.startswith("|"))
readme=open(os.path.join(root,"corpus/README.md"),encoding="utf-8").read().count("\n")
text=open(sc,encoding="utf-8").read()
out=[]
for line in text.split("\n"):
    if line.startswith("| depth |"):
        c=line.split("|"); c[3]=(" %d notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); "
            "`SKILL.md` %d `wc -l` / %d table lines (`grep -c '^|' SKILL.md`); "
            "`corpus/lessons/` %d files (`find corpus/lessons -type f | wc -l`); four standing rules near the top of SKILL cite no knowledge note; no ordinal move claimed."
            % (notes,skill_lines,skill_tables,lessons)); line="|".join(c)
    elif line.startswith("| coverage |") and "wc -l" in line:
        c=line.split("|"); c[3]=(" `corpus/README.md` %d `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes; four declared round-1 read-only surfaces link knowledge; pacnew census arm C1 was not verified in round 35, no coverage ordinal move." % readme); line="|".join(c)
    out.append(line)
open(sc,"w",encoding="utf-8").write("\n".join(out))
print("  re-stated: notes=%d lessons=%d skill_lines=%d skill_tables=%d readme=%d" % (notes,lessons,skill_lines,skill_tables,readme))
PY

git -C "$ROOT" add -A
git -C "$ROOT" commit -q -m "fixture: re-state the five count cells at the tip"
echo "=== T1: tip + re-stated five count cells"
run_check T1-tip-restated

echo "=== summary"
for f in T0-tip-untouched T1-tip-restated; do
  printf '%-22s exit=%-3s ' "$f" "$(cat "$OUT/$f.exit")"
  python3 -c "
import json
d=json.load(open('$OUT/$f.json'))
print('checked=%s mismatches=%s status=%s' % (d.get('checked'),d.get('mismatches'),d.get('status')))" 2>/dev/null || echo "(unparsed)"
done
