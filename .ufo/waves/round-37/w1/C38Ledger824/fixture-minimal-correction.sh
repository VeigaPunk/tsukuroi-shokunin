#!/usr/bin/env bash
# C38Ledger824 — C3 minimal append-only correction fixture.
#
# Read-only against the lane repo: the lane tree is exported with `git archive`
# (a read operation) into a private mktemp fixture repo. No lane git/jj write.
#
# The C3 declaration scopes the repair to "append-only correction of the five
# current self-assessment count cells". The lane's landing instead ALSO
# appended a parallel `## Capabilities - current (round 37)` table. This
# fixture tests the minimal append-only correction against the UNCHANGED
# checker:
#
#   M0  base export, untouched                                  -> expect 5 / exit 1
#   M1  base + APPENDED new "## Axes - current self-assessment (round 37)"
#       section carrying the corrected five count cells,
#       capabilities section UNTOUCHED                         -> expect 0 / exit 0
#   M2  M1 + the round-37 change commit the declaration schedules
#       (lesson skeleton + knowledge note + SKILL.md registry row)
#                                                              -> expect drift
#   M3  M2 + the five count cells re-stated at M2's revision  -> expect 0 / exit 0
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

ROOT=$(mktemp -d /tmp/c38-min-XXXXXX)
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
    print("  checked=%s mismatches=%s status=%s declaring_round=%s axes=%r" % (
        d.get("checked"), d.get("mismatches"), d.get("status"), d.get("declaring_round"), d.get("axes_heading")))
    for c in d.get("checks",[]):
        if c.get("status")!="match":
            print("  %s %s | %s" % (c["id"], c["status"], c["reason"][:165]))
PY
  echo "  exit=$rc"
}

# Append the corrected axes section. Counts are measured at THIS revision.
append_axes () {  # append_axes <round-number>
  python3 - "$ROOT" "$1" <<'PY'
import os,sys
root,round_no=sys.argv[1],sys.argv[2]
sc=os.path.join(root,"SCORECARD.md")
notes=len([p for p in os.listdir(os.path.join(root,"corpus/knowledge")) if p.endswith(".md")])
lessons=len(os.listdir(os.path.join(root,"corpus/lessons")))
skill=open(os.path.join(root,"SKILL.md"),encoding="utf-8").read()
skill_lines=skill.count("\n")
skill_tables=sum(1 for l in skill.split("\n") if l.startswith("|"))
readme=open(os.path.join(root,"corpus/README.md"),encoding="utf-8").read().count("\n")
block = """

## Axes — current self-assessment (round %s)

Appended by the round-37 C3 repair as the minimal append-only correction of the
five stale count cells; the capabilities section is unchanged. Counts are
measured at the revision that adds this section.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | %d notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` %d `wc -l` / %d table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` %d files (`find corpus/lessons -type f | wc -l`); four standing rules near the top of SKILL cite no knowledge note; no ordinal move claimed. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` %d `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes; four declared round-1 read-only surfaces link knowledge; pacnew census arm C1 was not verified in round 35, no coverage ordinal move. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (105 cases, 105 passed, 0 failed); live run exits 1 with six-plane rollup; `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; dated round-1 D1-D5 rechecks and current recheck procedures remain recorded; captures are dated, not durable host state. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; C3 requires mismatches 0 at the measured round-37 tip; no ordinal uplift. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |
""" % (round_no, notes, skill_lines, skill_tables, lessons, readme)
with open(sc,"a",encoding="utf-8") as fh:
    fh.write(block)
print("  appended round-%s axes section: notes=%d lessons=%d skill_lines=%d skill_tables=%d readme=%d"
      % (round_no, notes, lessons, skill_lines, skill_tables, readme))
PY
}

echo "=== M0: base export, untouched"
run_check M0-base

append_axes 37
git -C "$ROOT" add -A
git -C "$ROOT" commit -q -m "fixture: append-only correction of the five count cells"
echo "=== M1: append-only five-cell correction (capabilities UNTOUCHED)"
run_check M1-minimal-corrected

# --- M2: the change commit the round-37 declaration schedules --------------
printf '# round-37 lesson skeleton\n\nfixture lesson body\n' > "$ROOT/corpus/lessons/round-37.md"
printf '# probe V8 note\n\nfixture probe note body\n' > "$ROOT/corpus/knowledge/probe-v8-note-r37.md"
printf '\n| round37 | probe V8 registry row |\n' >> "$ROOT/SKILL.md"
git -C "$ROOT" add -A
git -C "$ROOT" commit -q -m "fixture: simulated round-37 change commit"
echo "=== M2: M1 + scheduled change commit (lesson skeleton + note + registry row)"
run_check M2-after-change-commit

append_axes 37
git -C "$ROOT" add -A
git -C "$ROOT" commit -q -m "fixture: re-state the five count cells at the change-commit revision"
echo "=== M3: M2 + five count cells re-stated at the change-commit revision"
run_check M3-restated

echo "=== summary"
for f in M0-base M1-minimal-corrected M2-after-change-commit M3-restated; do
  printf '%-26s exit=%-3s ' "$f" "$(cat "$OUT/$f.exit")"
  python3 -c "
import json
d=json.load(open('$OUT/$f.json'))
print('checked=%s mismatches=%s status=%s' % (d.get('checked'),d.get('mismatches'),d.get('status')))" 2>/dev/null || echo "(unparsed)"
done
