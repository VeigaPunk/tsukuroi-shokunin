#!/usr/bin/env bash
# C34Ledger420 — fixture builder for the C3 self-assessment-mismatch attack.
#
# Read-only against the lane repo: the lane tree is exported with `git archive`
# (no lane Git state is written). Every fixture is a FRESH mktemp repo created
# with `git -C <root> init`; the top-level is verified to equal the fixture
# root BEFORE any commit. All commits happen inside the fixture repo only.
#
# Usage: build-fixtures.sh <lane-repo> <outdir>
set -euo pipefail

LANE=$(cd "$1" && pwd)
OUT=$(cd "$2" && pwd)
CHECKER="$LANE/tools/check-self-assessment.py"

BASE=564db0b614b2914de5452f9ebd537a0653ae1de5   # round-37 declaration base
TIP=0e5f70fadba12bc9bbb9db564c2262c2c0194535   # lane tip when this seat ran

# ---- the proposed appended axes table (the correction proposal) -----------
# Literal phrases are chosen to satisfy the UNCHANGED checker's parsers:
#   K07 "N notes"          K08 "`SKILL.md` N `wc -l`"   K09 "N table lines"
#   K10 "corpus/lessons/ N files"
#   K11 "`corpus/README.md` N `wc -l`"
#   K12 "Core, Frontier and Adjacent sections present"
#   K13 "PASS (N cases, ...)"      K14 "`--identity` not landed"
#   K15 "formal overlap table present"
read -r -d '' PROPOSED_TABLE <<'EOF' || true
## Axes — current self-assessment (round 37)

Appended 2026-10-25 by round 37; supersedes the round-35 table at `SCORECARD.md:1564`. Ordinals
unchanged. Counts re-derived at this revision; C3 measures the checker mismatch count, not an
ordinal uplift. No capabilities table is appended: the round-35 capability table at
`SCORECARD.md:1578` still names every evidence path it named, and all of them are present here.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 56 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3110 `wc -l` / 839 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 49 files (`find corpus/lessons -type f | wc -l`); four standing rules near the top of SKILL cite no knowledge note; no ordinal move claimed. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 269 `wc -l`; PROVINCE Core, Frontier and Adjacent sections present; six census planes; four declared round-1 read-only surfaces link knowledge; pacnew census arm C1 was not verified in round 35, no coverage ordinal move. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (105 cases, 105 passed, 0 failed); live run exits 1 with six-plane rollup; `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; dated round-1 D1-D5 rechecks and current recheck procedures remain recorded; captures are dated, not durable host state. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; C3 requires mismatches 0 at the measured round-37 tip; no ordinal uplift. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |
EOF

# ---- the restored capability rows (evidence kept, paths fully qualified) --
# Same content the round-35 table carried at the base, with every evidence
# path fully qualified so the path grammar resolves it. No pointer deleted.
read -r -d '' RESTORED_CAPS <<'EOF' || true
## Capabilities — current (round 37)

Append-only copy of the active round-35 capability rows at `SCORECARD.md:1578`. No capability row
is added, none is removed, and no evidence pointer is dropped: the two pointers that the first
round-37 attempt left as bare filenames are fully qualified here so the path grammar resolves them
to the paths that exist at this revision.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates where the lane learns: `corpus/SOURCES.md` holds opened, tier-scoped rows with anchors, rejections with flips, study paths, a search log and unopened leads, and the row set is checked by the frozen contract's census commands | `corpus/SOURCES.md`; the census commands and their outputs in `.ufo/evidence/round-1-kaika/after.md` (34 rows in that snapshot, malformed 0, no duplicate, enum or missing output; 125 rows at round 25) | fleet r1 (2026-10-19) |
| host-census-gate | Emits a read-only six-plane host verdict and one verdict-neutral `DRIFT pacnew-plane` line (TSUKUROI_CENSUS: HEALTHY, DEGRADED or BLOCKED; exit 0, 1 or 2) with a hermetic 105-case selftest that touches no live host surface | `tools/tsukuroi-census.sh` selftest prints PASS 105/105 rc=0 (105 cases, 105 passed, 0 failed); the live run exits 1 with a six-plane rollup; receipts `.ufo/evidence/round-1-kaika/scout-live.md` and `.ufo/evidence/round-1-kaika/after.md` | lane r2 (census-v1); demonstrated running fleet r1 |
| root-metadata-observer | Emits root mode, uid, gid and owner-bit observations even on package-probe failure; isolates fixtures and blocks unavailable or non-directory metadata without grading intentional 0555 policy | `.ufo/waves/round-12/resumed/after.json`, `.ufo/waves/round-12/resumed/selftest-after.json`, `.ufo/waves/round-12/resumed/mode-policy-mutant.json`; measured commit `70fede2a7a890cb50a72db2d4230ee541183bf7b` | round 12 |
| boot-chain-audit | Audits every limine entry live and read-only: copies each UKI with a read-only `sudo -n cat`, extracts its initramfs in a private mktemp directory, types the new_root path, binds the firmware-selected entry, and emits a per-entry next-boot verdict plus TSUKUROI_BOOTCHAIN | `tools/boot-chain-audit.sh` live run wrote `.ufo/waves/round-17/l1-capture/audit-live.txt` (6 entries, CONSISTENT, exit 0); its selftest prints PASS total=45 failed=0 | round 17 |
EOF

# ---- a deliberately mis-phrased variant (proves the phrase requirement) ---
read -r -d '' MISPHRASED_TABLE <<'EOF' || true
## Axes — current self-assessment (round 37)

Variant B of the correction proposal: the same five corrected counts, but the coverage row phrases
the README count the way the FIRST round-37 attempt did (number, then a word, then the command in
parens). Kept only as a negative control.

| Axis | Score | Evidence pointer (counting command) | Last change |
|---|---|---|---|
| depth | 8 | 56 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` 3110 `wc -l` / 839 table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 49 files (`find corpus/lessons -type f | wc -l`); four standing rules near the top of SKILL cite no knowledge note; no ordinal move claimed. | round 4 (move-log row at `SCORECARD.md:30`); unchanged |
| coverage | 9 | `corpus/README.md` 269 newline characters (`wc -l corpus/README.md`); PROVINCE Core, Frontier and Adjacent sections present; six census planes; four declared round-1 read-only surfaces link knowledge; pacnew census arm C1 was not verified in round 35, no coverage ordinal move. | round 11 (terminal closeout, `SCORECARD.md:37`); unchanged |
| operability | 9 | `bash tools/tsukuroi-census.sh --selftest` prints PASS (105 cases, 105 passed, 0 failed); live run exits 1 with six-plane rollup; `--identity` not landed. | round 11 (terminal closeout); unchanged |
| freshness | 9 | Each round record re-ran predecessor pins; dated round-1 D1-D5 rechecks and current recheck procedures remain recorded; captures are dated, not durable host state. | fleet round 1; unchanged |
| calibration | 9 | `python3 tools/check-self-assessment.py --revision <REV>` checks 27 fixed checks; C3 requires mismatches 0 at the measured round-37 tip; no ordinal uplift. | round 10; unchanged |
| adjacency | 8 | formal overlap table present (finding-to-owner ADJ-01..07) and portable OUT-001..010 anchors remain; recipient acknowledgement and independent replay are unverified. | fleet round 1; unchanged |
EOF

# ---------------------------------------------------------------- helpers --
make_repo() {           # $1 = name, $2 = source revision
  local name=$1 rev=$2 root
  root=$(mktemp -d "/tmp/c34-${name}-XXXXXX")
  git -C "$LANE" archive --format=tar "$rev" | tar -x -C "$root"
  git -C "$root" init -q
  local top; top=$(git -C "$root" rev-parse --show-toplevel)
  if [ "$top" != "$root" ]; then
    echo "ABORT: fixture $name top-level $top != root $root" >&2
    exit 3
  fi
  echo "$root"
}

commit() {             # $1 = root, $2 = message
  git -C "$1" add -A
  git -C "$1" -c user.name=c34 -c user.email=c34@example.invalid commit -q -m "$2"
}

run_checker() {        # $1 = root, $2 = label
  local root=$1 label=$2
  ( cd "$root" && python3 "$CHECKER" --revision HEAD --repo "$root" ) \
    > "$OUT/${label}.json" 2> "$OUT/${label}.stderr" || true
  local rc=$?
  echo "$rc" > "$OUT/${label}.exit"
  python3 - "$OUT/${label}.json" "$OUT/${label}.summary.txt" <<'PY'
import json, sys
src, dst = sys.argv[1], sys.argv[2]
try:
    d = json.load(open(src))
except Exception as exc:
    open(dst, "w").write("UNPARSEABLE: %s\n" % exc); raise SystemExit(0)
lines = ["status=%s mismatches=%s checked=%s declaring_round=%s" % (
    d.get("status"), d.get("mismatches"), d.get("checked"), d.get("declaring_round")),
    "axes_heading=%s" % d.get("axes_heading")]
for c in d.get("checks", []):
    if c["id"] in ("K07", "K08", "K09", "K10", "K11", "K13", "K16", "K17", "K18", "K19"):
        lines.append("  %s %s stated=%r observed=%r | %s" % (
            c["id"], c["status"], c["stated"], c["observed"], c["reason"][:150]))
open(dst, "w").write("\n".join(lines) + "\n")
PY
}

# ============================================================ F0: base ====
# Control: the round-37 declaration base, unmodified.
ROOT=$(make_repo f0-base "$BASE")
commit "$ROOT" "fixture: lane tree at declaration base $BASE"
run_checker "$ROOT" "F0-base-control"
echo "F0=$ROOT"

# ================================== F1: base + proposed axes table only ==
# The correction proposal: append ONE axes table to the base tree. No
# capabilities table is touched.
ROOT=$(make_repo f1-base-proposed "$BASE")
printf '\n%s\n' "$PROPOSED_TABLE" >> "$ROOT/SCORECARD.md"
commit "$ROOT" "fixture: base + proposed round-37 axes table"
run_checker "$ROOT" "F1-base-plus-proposed-axes-table"
echo "F1=$ROOT"

# ===================================== F2: base + proposed + caps restored =
# Proposal plus a capabilities table that KEEPS every round-35 evidence
# pointer (fully qualified), instead of deleting the two unresolvable ones.
ROOT=$(make_repo f2-base-proposed-caps "$BASE")
printf '\n%s\n' "$PROPOSED_TABLE" >> "$ROOT/SCORECARD.md"
printf '\n%s\n' "$RESTORED_CAPS" >> "$ROOT/SCORECARD.md"
commit "$ROOT" "fixture: base + proposed axes table + restored capability rows"
run_checker "$ROOT" "F2-base-proposed-axes-plus-restored-caps"
echo "F2=$ROOT"

# ================================ F3: base + mis-phrased variant (negative)
# Same counts, coverage row phrased the way the first round-37 attempt was.
ROOT=$(make_repo f3-base-misphrased "$BASE")
printf '\n%s\n' "$MISPHRASED_TABLE" >> "$ROOT/SCORECARD.md"
commit "$ROOT" "fixture: base + mis-phrased coverage row (negative control)"
run_checker "$ROOT" "F3-base-misphrased-coverage-row"
echo "F3=$ROOT"

# ================================================= F4: lane tip, unmodified =
# Control: the lane tip as it stands.
ROOT=$(make_repo f4-tip "$TIP")
commit "$ROOT" "fixture: lane tree at tip $TIP"
run_checker "$ROOT" "F4-tip-control"
echo "F4=$ROOT"

# ============================== F5: tip + restored capability evidence ====
# The tip already reports zero mismatches. Does it still do so if the
# capability rows keep every evidence pointer instead of the reduced set?
ROOT=$(make_repo f5-tip-caps-restored "$TIP")
printf '\n%s\n' "$RESTORED_CAPS" >> "$ROOT/SCORECARD.md"
commit "$ROOT" "fixture: tip + capability rows with every evidence pointer kept"
run_checker "$ROOT" "F5-tip-plus-restored-caps"
echo "F5=$ROOT"

echo "ALL FIXTURES BUILT"
