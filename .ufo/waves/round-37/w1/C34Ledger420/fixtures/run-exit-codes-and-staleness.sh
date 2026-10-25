#!/usr/bin/env bash
# C34Ledger420 — true exit codes for the lane revisions and the six fixtures,
# plus the forward-staleness probes: does the round-37 repair survive the
# round's OWN next content commit?
#
# Read-only against the lane repo (git archive export only; no lane Git state
# is written). Every fixture is a fresh mktemp repo; the top-level is verified
# equal to the fixture root before any commit. No lane Git state is written.
set -uo pipefail

LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
OUT=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-37/w1/C34Ledger420/fixtures/out
CHECKER="$LANE/tools/check-self-assessment.py"
BASE=564db0b614b2914de5452f9ebd537a0653ae1de5
TIP=0e5f70fadba12bc9bbb9db564c2262c2c0194535

# run <repo> <rev> <json-out>  -> prints "<exit> <status> <mismatches> <checked>"
run() {
  local repo=$1 rev=$2 json=$3 rc
  ( cd "$repo" && python3 "$CHECKER" --revision "$rev" --repo "$repo" ) > "$json" 2>/dev/null
  rc=$?
  python3 - "$json" "$rc" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    print("%s UNPARSEABLE" % sys.argv[2]); raise SystemExit(0)
print("%s %s %s %s" % (sys.argv[2], d.get("status"), d.get("mismatches"), d.get("checked")))
PY
}

mismatches_of() {
  python3 - "$1" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print("\n".join("  MISMATCH %s | %s" % (c["id"], c["reason"][:150])
                for c in d.get("checks", []) if c["status"] == "mismatch") or "  (none)")
PY
}

echo "== lane revisions: checker exit / status / mismatches / checked =="
for rev in "$BASE" 083cd0c b8ededd d06cedb ee36f9e 5124bf3 "$TIP"; do
  printf "  %-10s %s\n" "$rev" "$(run "$LANE" "$rev" "$OUT/lane-${rev}.json")"
done

echo
echo "== fixture repos (checker run at HEAD) =="
for d in /tmp/c34-f0-base-* /tmp/c34-f1-base-proposed-* /tmp/c34-f2-base-proposed-caps-* \
         /tmp/c34-f3-base-misphrased-* /tmp/c34-f4-tip-* /tmp/c34-f5-tip-caps-restored-*; do
  [ -d "$d/.git" ] || continue
  label=$(basename "$d")
  printf "  %-42s %s\n" "$label" "$(run "$d" HEAD "$OUT/fixture-${label}.json")"
done

mk() {  # $1 = name ; fresh fixture root at the lane tip
  local root; root=$(mktemp -d "/tmp/c34-$1-XXXXXX")
  git -C "$LANE" archive --format=tar "$TIP" | tar -x -C "$root"
  git -C "$root" init -q
  local top; top=$(git -C "$root" rev-parse --show-toplevel)
  if [ "$top" != "$root" ]; then
    echo "ABORT: fixture $1 top-level $top != root $root" >&2; exit 3
  fi
  git -C "$root" add -A
  git -C "$root" -c user.name=c34 -c user.email=c34@example.invalid commit -q -m "fixture: lane tip tree"
  echo "$root"
}

commit_extra() {  # $1 = root, $2 = message
  git -C "$1" add -A
  git -C "$1" -c user.name=c34 -c user.email=c34@example.invalid commit -q -m "$2"
}

echo
echo "== forward-staleness probes on the repaired tip =="

R=$(mk f6-note)
printf '# round-37 staleness probe note\n\nprobe body\n' > "$R/corpus/knowledge/round-37-staleness-probe.md"
commit_extra "$R" "fixture: +1 corpus/knowledge note"
echo "F6 (tip + 1 corpus/knowledge note): $(run "$R" HEAD "$OUT/F6-tip-plus-one-knowledge-note.json")"
mismatches_of "$OUT/F6-tip-plus-one-knowledge-note.json"

R=$(mk f7-lesson)
printf '# round-37 staleness probe lesson\n\nprobe body\n' > "$R/corpus/lessons/round-37-staleness-probe.md"
commit_extra "$R" "fixture: +1 corpus/lessons file"
echo "F7 (tip + 1 corpus/lessons file): $(run "$R" HEAD "$OUT/F7-tip-plus-one-lesson-file.json")"
mismatches_of "$OUT/F7-tip-plus-one-lesson-file.json"

R=$(mk f8-skill)
printf '\n<!-- round-37 staleness probe -->\n' >> "$R/SKILL.md"
commit_extra "$R" "fixture: +1 SKILL.md line"
echo "F8 (tip + 1 SKILL.md line): $(run "$R" HEAD "$OUT/F8-tip-plus-one-skill-line.json")"
mismatches_of "$OUT/F8-tip-plus-one-skill-line.json"

R=$(mk f9-readme)
printf '\n<!-- round-37 staleness probe -->\n' >> "$R/corpus/README.md"
commit_extra "$R" "fixture: +1 corpus/README.md line"
echo "F9 (tip + 1 corpus/README.md line): $(run "$R" HEAD "$OUT/F9-tip-plus-one-readme-line.json")"
mismatches_of "$OUT/F9-tip-plus-one-readme-line.json"

echo "DONE"
