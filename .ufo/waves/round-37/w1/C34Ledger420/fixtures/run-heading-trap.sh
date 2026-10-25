#!/usr/bin/env bash
# C34Ledger420 — heading-level trap probe.
#
# The lane's OWN append-only repair idiom is a `###` subsection table appended
# under the last `## Capabilities` heading (that is what commit 5124bf3 did,
# and it made the checker exit 2 CANNOT_EVALUATE). This probe asks whether
# the SAME idiom, applied to the current passing tip, breaks the checker again.
#
# Read-only against the lane repo (git archive export only). Every fixture is a
# fresh mktemp repo; the top-level is verified equal to the fixture root before
# any commit. No lane Git state is written.
set -uo pipefail

LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
OUT=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-37/w1/C34Ledger420/fixtures/out
CHECKER="$LANE/tools/check-self-assessment.py"
TIP=0e5f70fadba12bc9bbb9db564c2262c2c0194535

mk() {
  local root; root=$(mktemp -d "/tmp/c34-$1-XXXXXX")
  git -C "$LANE" archive --format=tar "$TIP" | tar -x -C "$root"
  git -C "$root" init -q
  local top; top=$(git -C "$root" rev-parse --show-toplevel)
  if [ "$top" != "$root" ]; then echo "ABORT: top-level $top != $root" >&2; exit 3; fi
  git -C "$root" add -A
  git -C "$root" -c user.name=c34 -c user.email=c34@example.invalid commit -q -m "fixture: lane tip tree"
  echo "$root"
}
commit_extra() {
  git -C "$1" add -A
  git -C "$1" -c user.name=c34 -c user.email=c34@example.invalid commit -q -m "$2"
}
run() {
  local repo=$1 json=$2 rc
  ( cd "$repo" && python3 "$CHECKER" --revision HEAD --repo "$repo" ) > "$json" 2>/dev/null
  rc=$?
  python3 - "$json" "$rc" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception:
    print("exit=%s UNPARSEABLE" % sys.argv[2]); raise SystemExit(0)
print("exit=%s status=%s mismatches=%s checked=%s error=%s detail=%s" % (
    sys.argv[2], d.get("status"), d.get("mismatches"), d.get("checked"),
    d.get("error"), d.get("detail")))
PY
}

# ---- F10: tip + `###` one-row capabilities correction (the 5124bf3 idiom) --
R=$(mk f10-h3-partial-caps)
cat >> "$R/SCORECARD.md" <<'EOF'

### Round-37 capability evidence correction (append-only, heading level 3)

K17 requires the current host-census-gate capability row to state the selftest case count.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT line, with a hermetic selftest that prints PASS (105 cases, 105 passed, 0 failed) | `tools/tsukuroi-census.sh` and `.ufo/evidence/round-1-kaika/scout-live.md` | lane r2; demonstrated running fleet r1 |
EOF
commit_extra "$R" "fixture: + h3 partial capabilities correction table"
echo "F10 (tip + h3 one-row capabilities table): $(run "$R" "$OUT/F10-tip-plus-h3-partial-caps.json")"

# ---- F11: tip + `##` one-row capabilities correction (same table, level 2) --
R=$(mk f11-h2-partial-caps)
cat >> "$R/SCORECARD.md" <<'EOF'

## Capabilities — correction (round 37)

K17 requires the current host-census-gate capability row to state the selftest case count.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT line, with a hermetic selftest that prints PASS (105 cases, 105 passed, 0 failed) | `tools/tsukuroi-census.sh` and `.ufo/evidence/round-1-kaika/scout-live.md` | lane r2; demonstrated running fleet r1 |
EOF
commit_extra "$R" "fixture: + h2 one-row capabilities correction table"
echo "F11 (tip + h2 one-row capabilities table): $(run "$R" "$OUT/F11-tip-plus-h2-partial-caps.json")"

# ---- F12: tip + a `###` four-row capabilities correction (all rows kept) ---
R=$(mk f12-h3-full-caps)
cat >> "$R/SCORECARD.md" <<'EOF'

### Round-37 capability evidence correction (append-only, heading level 3, all rows)

All four capability rows retained; only the host-census-gate evidence cell is restated.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates where the lane learns: opened tier-scoped rows with anchors, rejections with flips, study paths, a search log and unopened leads; checked by frozen census commands | `corpus/SOURCES.md` | fleet r1 |
| host-census-gate | Emits a read-only six-plane host verdict and verdict-neutral DRIFT line, with a hermetic selftest that prints PASS (105 cases, 105 passed, 0 failed) | `tools/tsukuroi-census.sh` and `.ufo/evidence/round-1-kaika/scout-live.md` | lane r2; demonstrated running fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations even on package-probe failure; isolates fixtures and blocks unavailable/non-directory metadata without grading intentional 0555 policy | `.ufo/waves/round-12/resumed/after.json` | round 12 |
| boot-chain-audit | Audits limine entries read-only: extracts initramfs, types new_root, binds firmware-selected entry and emits per-entry next-boot verdict | `tools/boot-chain-audit.sh` and `.ufo/waves/round-17/l1-capture/audit-live.txt` | round 17 |
EOF
commit_extra "$R" "fixture: + h3 full capabilities correction table"
echo "F12 (tip + h3 four-row capabilities table): $(run "$R" "$OUT/F12-tip-plus-h3-full-caps.json")"

# ---- F13: tip + one appended line to the OPERATIVE axes table's depth row ----
# Editing the operative table in place (not appending) is what a future round
# would do; this shows the K07 count is coupled to the tree, not to prose.
R=$(mk f13-inline-edit)
python3 - "$R/SCORECARD.md" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
old = "| depth | 8 | 56 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`);"
new = "| depth | 8 | 57 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`);"
assert old in s, "anchor not found"
open(p, "w").write(s.replace(old, new, 1))
PY
commit_extra "$R" "fixture: operative depth row notes count edited 56 -> 57"
echo "F13 (tip, depth row edited 56 -> 57): $(run "$R" "$OUT/F13-tip-depth-row-edited-to-57.json")"

echo "DONE"
