#!/usr/bin/env bash
# C3 self-assessment mismatch correction — isolated runnable check.
# Axis: calibration. Assignment: design item 8/12.
# Lane files remain read-only; all Git writes occur in a fresh, verified mktemp repo.
set -euo pipefail
LANE="${C3_LANE:-/home/vgpnk/Projects/shokunin/tsukuroi-shokunin}"
REV="${C3_BASELINE:-564db0b614b2914de5452f9ebd537a0653ae1de5}"
CHECKER="$LANE/tools/check-self-assessment.py"
SEAT_OUT="${SEAT_OUT:-}"
FIX="$(mktemp -d "${TMPDIR:-/tmp}/c3-fixture.XXXXXX")"
trap 'rm -rf "$FIX"' EXIT
step() { printf '\n=== %s ===\n' "$*"; }
json_get() { python3 -c 'import json,sys; d=json.load(sys.stdin); print(eval(sys.argv[1]))' "$2" <<<"$1"; }
run_check() {
    local out ec
    set +e
    out="$(python3 "$CHECKER" --repo "$FIX" --revision "$1" 2>&1)"
    ec=$?
    set -e
    printf '%s\n' "$ec" > "$FIX/.check-exit"
    printf '%s' "$out"
}

# Import an immutable lane revision into an isolated repo. Verify its root before commits.
step "fixture root: $FIX"
git -C "$FIX" init -q -b main
git -C "$FIX" config user.email seat@tsukuroi.local
git -C "$FIX" config user.name Build8C340
TOP="$(git -C "$FIX" rev-parse --show-toplevel)"
[ "$TOP" = "$FIX" ] || { echo "FATAL: fixture top-level mismatch: $TOP != $FIX" >&2; exit 3; }
echo "top-level verified: $TOP"
step "import lane tree at baseline $REV"
git -C "$LANE" archive --format=tar "$REV" | tar -x -C "$FIX"
git -C "$FIX" add -A
git -C "$FIX" commit -q -m "baseline tree at $REV"
BASE="$(git -C "$FIX" rev-parse HEAD)"
echo "baseline commit: $BASE"

# Baseline must match the frozen 27-check result: K07–K11 stale; all other checks match.
step "BEFORE: unchanged baseline"
BEFORE="$(run_check "$BASE")"
BEFORE_EXIT="$(cat "$FIX/.check-exit")"
[ -z "$SEAT_OUT" ] || printf '%s\n' "$BEFORE" > "$SEAT_OUT/before.json"
N="$(json_get "$BEFORE" 'd["mismatches"]')"
IDS="$(json_get "$BEFORE" '",".join(c["id"] for c in d["checks"] if c["status"]=="mismatch")')"
echo "exit=$BEFORE_EXIT status=$(json_get "$BEFORE" 'd["status"]') checked=$(json_get "$BEFORE" 'd["checked"]') mismatches=$N"
echo "mismatch_ids=$IDS"
[ "$BEFORE_EXIT" = 1 ] && [ "$N" = 5 ] && [ "$IDS" = K07,K08,K09,K10,K11 ] || { echo "FATAL: baseline must reproduce the five frozen mismatches" >&2; exit 3; }

# Apply a concrete SCORECARD correction in the fixture only. Select exact table rows
# and replace each measured stale scalar once; refuse if the expected old byte is absent.
step "apply five K07-K11 corrections in isolated SCORECARD.md"
python3 - "$FIX/SCORECARD.md" <<'PY'
import sys
p=sys.argv[1]
s=open(p, encoding='utf-8').read()
# The checker selects the last "## Axes - " section; require the round-35
# declaration table to be the sole target for each stated counter.
for old,new in [
    ('55 notes','56 notes'), ('3009 `wc -l`','3110 `wc -l`'),
    ('784 table lines','839 table lines'), ('(46 files)','(49 files)'),
    ('`corpus/README.md` 256 `wc -l`','`corpus/README.md` 269 `wc -l`')]:
    n=s.count(old)
    if n < 1:
        sys.exit('FATAL: no source occurrence of %r' % old)
    # Restrict edits to the last axes section and require exactly one table
    # row occurrence (the intro prose may repeat the stale value).
    start=s.rfind('## Axes — current self-assessment (round 35)')
    end=s.find('\\n## ', start+1)
    if start < 0:
        sys.exit('FATAL: round-35 axes heading missing')
    if end < 0: end=len(s)
    section=s[start:end]
    lines=section.splitlines(keepends=True)
    hits=[i for i,line in enumerate(lines) if line.startswith('| depth |') or line.startswith('| coverage |')]
    rowhits=[i for i in hits if old in lines[i]]
    if len(rowhits)!=1:
        sys.exit('FATAL: expected one parser-facing row occurrence of %r, found %d' % (old,len(rowhits)))
    i=rowhits[0]
    lines[i]=lines[i].replace(old,new,1)
    s=s[:start]+''.join(lines)+s[end:]
open(p,'w',encoding='utf-8').write(s)
print('corrected five parser-facing values (K07..K11)')
PY
git -C "$FIX" add SCORECARD.md
git -C "$FIX" commit -q -m "correct five stale self-assessment values"
AFTER_REV="$(git -C "$FIX" rev-parse HEAD)"
echo "correction commit: $AFTER_REV"

# The same checker must now evaluate all 27 fixed predicates and pass with no mismatch.
step "AFTER: corrected fixture revision"
AFTER="$(run_check "$AFTER_REV")"
AFTER_EXIT="$(cat "$FIX/.check-exit")"
[ -z "$SEAT_OUT" ] || printf '%s\n' "$AFTER" > "$SEAT_OUT/after.json"
N="$(json_get "$AFTER" 'd["mismatches"]')"
echo "exit=$AFTER_EXIT status=$(json_get "$AFTER" 'd["status"]') checked=$(json_get "$AFTER" 'd["checked"]') mismatches=$N"
[ "$AFTER_EXIT" = 0 ] && [ "$N" = 0 ] && [ "$(json_get "$AFTER" 'd["checked"]')" = 27 ] || { echo "FATAL: corrected state must be PASS with 27 checks and zero mismatches" >&2; exit 3; }
for id in K07 K08 K09 K10 K11; do
    printf '%s observed=%s status=%s\n' "$id" "$(json_get "$AFTER" "[c['observed'] for c in d['checks'] if c['id']=='$id'][0]")" "$(json_get "$AFTER" "[c['status'] for c in d['checks'] if c['id']=='$id'][0]")"
done
step "PASS: before=5 mismatches; after=0; same 27 fixed checks"
