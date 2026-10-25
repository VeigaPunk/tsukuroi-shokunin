#!/usr/bin/env bash
# Verifier2Claim262 — independent pre-data control audit item 2/4.
# C3 self-assessment mismatch repair claim (Build9C341, wave-level before/after
# receipts): frozen predicate = mismatches==0 && checked==27 && exit==0
# (Build9C341.md:41). Declared work = correcting the five stale
# round-35 axes cells K07-K11 in SCORECARD.md.
#
# Cheapest do-nothing control: run the checker on the committed baseline bytes
# (revision 564db0b, the round-36 verifier spot-check commit) WITHOUT applying
# any correction. Sandbox: fresh mktemp fixture repo; lane read-only via
# `git archive`; top-level verified == fixture root before the commit.
set -euo pipefail

LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
CHECKER="$LANE/tools/check-self-assessment.py"
BASE=564db0b614b2914de5452f9ebd537a0653ae1de5
SEAT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------- 1. fixture repo (fresh mktemp), top-level verified ----------
FIX="$(mktemp -d /tmp/v2-c3-donothing-XXXXXX)"
trap 'rm -rf "$FIX"' EXIT
git -C "$FIX" init -q -b main
git -C "$FIX" config user.name v2-fixture
git -C "$FIX" config user.email v2@fixture.local
TOP="$(git -C "$FIX" rev-parse --show-toplevel)"
if [ "$TOP" != "$FIX" ]; then
    echo "FATAL: top-level != fixture root ($TOP != $FIX)" >&2
    exit 3
fi
echo "fixture_root=$FIX"
echo "top_level_verified=$TOP"

# ---------- 2. committed baseline bytes at 564db0b --------------
BLOB_SHA="$(git -C "$LANE" rev-parse "$BASE:SCORECARD.md")"
echo "baseline_scorecard_blob=$BLOB_SHA"
git -C "$LANE" archive "$BASE" | tar -x -C "$FIX"
git -C "$FIX" add -A
git -C "$FIX" commit -qm "baseline fixture at $BASE"
BL="$(git -C "$FIX" rev-parse HEAD)"
echo "baseline_fixture_commit=$BL"

# ---------- 3. DO-NOTHING control: checker on committed baseline bytes,
#            no correction work applied (direct invocation, exact exit) ----
echo "== DO-NOTHING control (direct): python3 check-self-assessment.py --repo \$FIX --revision \$BL"
set +e
python3 "$CHECKER" --repo "$FIX" --revision "$BL" > "$SEAT/before-donothing.json" 2> "$SEAT/before-donothing.err"
RC=$?
set -e
echo "direct_exit=$RC"
python3 - "$SEAT/before-donothing.json" "$RC" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print("checked=%d mismatches=%d status=%s declaring_round=%s" % (
    d["checked"], d["mismatches"], d["status"], d.get("declaring_round")))
ids = [c["id"] for c in d["checks"] if c["status"] == "mismatch"]
print("mismatch_ids=%s" % ",".join(ids))
print("predicate_pass=%s" % (d["mismatches"] == 0 and d["checked"] == 27 and int(sys.argv[2]) == 0))
PY

# ---------- 4. replicate sibling harness shape (|| true + printf) to
#            explain the exit=0 observation in Build8C340/run.log -----------
set +e
out="$(python3 "$CHECKER" --repo "$FIX" --revision "$BL" 2>&1)" || true
rc_shape=$?
set -e
printf '%s' "$out" > "$SEAT/before-donothing-shape.json"
echo "sibling_shape_exit=$rc_shape (checker exit swallowed by '|| true' + printf)"
echo "DONE"
