#!/usr/bin/env bash
# C3 checker red-before control (Build9C341, tsukuroi round-37 w1).
#
# Design item 9/12: an isolated, runnable control proving the C3 self-assessment
# checker is RED on the unchanged round-37 declaration baseline (revision
# 564db0b...), and that the precise five-cell correction makes it measure a
# GREEN after state (checked=27, mismatches=0, exit=0).
#
# Sandbox contract (per seat bounds):
#   * lane repo is read-only; extraction is `git archive` (read-only).
#   * all git writes happen only in a fresh mktemp fixture repo.
#   * top-level is verified to equal the fixture root before any commit.
#   * no pacman / host changes.
set -euo pipefail

LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
CHECKER="$LANE/tools/check-self-assessment.py"
BASE=564db0b614b2914de5452f9ebd537a0653ae1de5
SEAT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATCH_FILE="$SEAT_DIR/patch-r35-axes-C3.patch"

# ---------- 1. fixture repo (fresh mktemp) -------------------------------
FIXTURE="$(mktemp -d /tmp/c3-red-before-fixture-XXXXXX)"
trap 'rm -rf "$FIXTURE"' EXIT
git init -q "$FIXTURE"
TOP="$(git -C "$FIXTURE" rev-parse --show-toplevel)"
if [ "$TOP" != "$FIXTURE" ]; then
    echo "FAIL top-level mismatch: fixture=$FIXTURE toplevel=$TOP" >&2
    exit 90
fi

# Extract the baseline tree from the lane (read-only) into the fixture.
git -C "$LANE" archive "$BASE" | tar -x -C "$FIXTURE"

git -C "$FIXTURE" -c user.name=c3-fixture -c user.email=c3@fixture.local add -A
git -C "$FIXTURE" -c user.name=c3-fixture -c user.email=c3@fixture.local \
    commit -qm "baseline fixture at $BASE"
REV_BEFORE="$(git -C "$FIXTURE" rev-parse HEAD)"

# ---------- 2. RED-before control on the unchanged baseline ---------------
echo "== RED-before: running checker at fixture baseline $REV_BEFORE"
set +e
python3 "$CHECKER" --repo "$FIXTURE" --revision "$REV_BEFORE" > "$SEAT_DIR/before.json" 2> "$SEAT_DIR/before.err"
RC_BEFORE=$?
set -e
echo "before rc=$RC_BEFORE"

python3 - "$SEAT_DIR/before.json" "$RC_BEFORE" <<'PY'
import json, sys
path, rc = sys.argv[1], int(sys.argv[2])
d = json.load(open(path))
mm = d.get("mismatches"); ck = d.get("checked")
ids = [c["id"] for c in d.get("checks", []) if c.get("status") != "match"]
print("before status=%s checked=%s mismatches=%s ids=%s" % (d.get("status"), ck, mm, ids))
expected = {"K07","K08","K09","K10","K11"}
if rc != 1 or ck != 27 or mm != 5 or set(ids) != expected:
    print("CONTROL FAIL: baseline is not RED as expected (rc=%d checked=%s mm=%s ids=%s)" % (rc, ck, mm, ids))
    sys.exit(2)
print("RED-BEFORE OK: check exits 1 with 27 checked, 5 mismatches (K07..K11)")
PY

# ---------- 3. precise correction patch (five cells, axes table only) -----
python3 - "$FIXTURE/SCORECARD.md" <<'PY'
import re, sys
path = sys.argv[1]
lines = open(path, encoding="utf-8").read().split("\n")

# locate the LAST axes section (the table the checker reads at the base)
sec_start = sec_end = None
for i, ln in enumerate(lines):
    if re.match(r"^\s*##\s+Axes\s+[—\-]\s", ln):
        sec_start, sec_end = i, len(lines)
assert sec_start is not None, "no axes section at base"

def row_line(i):
    return lines[i].startswith("| ") and not lines[i].startswith("| ---")

depth_i = cov_i = None
for i in range(sec_start, sec_end):
    if row_line(i) and lines[i].startswith("| depth |"):
        depth_i = i
    elif row_line(i) and lines[i].startswith("| coverage |"):
        cov_i = i
assert depth_i is not None and cov_i is not None, "depth/coverage rows not found"

def sub(row, pairs):
    for old, new in pairs:
        assert old in row, "anchor not found: %r" % old
        row = row.replace(old, new, 1)
    return row

lines[depth_i] = sub(lines[depth_i], [
    ("55 notes", "56 notes"),
    ("3009 `wc -l`", "3110 `wc -l`"),
    ("784 table lines", "839 table lines"),
    ("(46 files)", "(49 files)"),
])
lines[cov_i] = sub(lines[cov_i], [
    ("`corpus/README.md` 256 `wc -l`", "`corpus/README.md` 269 `wc -l`"),
])
open(path, "w", encoding="utf-8").write("\n".join(lines))
print("patched depth row line %d, coverage row line %d" % (depth_i + 1, cov_i + 1))
PY

git -C "$FIXTURE" diff -- SCORECARD.md > "$PATCH_FILE"
echo "patch written: $PATCH_FILE ($(wc -l < "$PATCH_FILE") lines)"
git -C "$FIXTURE" -c user.name=c3-fixture -c user.email=c3@fixture.local add SCORECARD.md
git -C "$FIXTURE" -c user.name=c3-fixture -c user.email=c3@fixture.local \
    commit -qm "apply C3 correction (five measured cells)"
REV_AFTER="$(git -C "$FIXTURE" rev-parse HEAD)"

# ---------- 4. after-state measurement ------------------------------------
echo "== after: running checker at corrected fixture $REV_AFTER"
set +e
python3 "$CHECKER" --repo "$FIXTURE" --revision "$REV_AFTER" > "$SEAT_DIR/after.json" 2> "$SEAT_DIR/after.err"
RC_AFTER=$?
set -e
echo "after rc=$RC_AFTER"

python3 - "$SEAT_DIR/after.json" "$RC_AFTER" <<'PY'
import json, sys
path, rc = sys.argv[1], int(sys.argv[2])
d = json.load(open(path))
mm = d.get("mismatches"); ck = d.get("checked")
mism = [c["id"] for c in d.get("checks", []) if c.get("status") != "match"]
print("after status=%s checked=%s mismatches=%s remaining=%s" % (d.get("status"), ck, mm, mism))
if rc != 0 or ck != 27 or mm != 0:
    print("AFTER FAIL: correction did not reach green (rc=%d checked=%s mm=%s)" % (rc, ck, mm))
    sys.exit(3)
print("AFTER OK: check exits 0 with 27 checked, 0 mismatches")
PY

echo
echo "CONTROL SUMMARY: baseline exit=$RC_BEFORE (RED, 5 mismatches) -> corrected exit=$RC_AFTER (GREEN, 0 mismatches)"
