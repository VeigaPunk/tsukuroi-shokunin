#!/usr/bin/env bash
# round-72 after-measurement: every counting command the three claims name, at one revision.
# usage: bash .ufo/waves/round-72/measure.sh <REV> <OUTFILE>
set -u
REV="${1:?revision}"
OUT="${2:?output file}"
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
cd "$LANE" || exit 1
{
  echo "# round-72 measurements at $REV ($(date -Iseconds))"
  echo "## C1 counter"
  python3 tools/count-md-rows-r72.py --revision "$REV"; echo "rc=$?"
  echo "## C1 registry rows"
  git show "$REV:corpus/SOURCES.md" | grep -cE '^\| *S[0-9]{3,}'
  echo "## C1 knowledge notes"
  git ls-tree --name-only "$REV:corpus/knowledge" | grep -c '\.md$'
  echo "## C1 new rows schema"
  git show "$REV:corpus/SOURCES.md" | awk -F'|' '/^\| *S(301|302|303) /{print $2,"NF="NF}'
  echo "## C2 selftest"
  python3 tools/check-selftest-tally.py --selftest; echo "rc=$?"
  echo "## C2 existing self-demo"
  python3 tools/check-selftest-tally.py --receipt .ufo/waves/round-70/after/selftest-after.txt \
    --label R70-C2 --range 4035c1a0..40c35ee7 -- SCORECARD.md PROVINCE.md corpus/README.md SKILL.md
  echo "rc=$?"
  echo "## C2 named TMPDIR measurement (a set-but-missing TMPDIR must fail the suite, rc 2)"
  TMPDIR=/nonexistent/x python3 tools/check-selftest-tally.py --selftest >/dev/null 2>&1; echo "missing-TMPDIR rc=$?"
  echo "## C2 committed red-before recipe (must FAIL)"
  bash .ufo/waves/round-72/after/redbefore-mutant.sh >/dev/null 2>&1; echo "redbefore rc=$?"
  echo "## C2 /tmp write tokens in the tool (docstring/negative only)"
  grep -n '/tmp' tools/check-selftest-tally.py | sed 's/^/  /' || true
  echo "## C3 routed checker"
  python3 tools/check-r71-routed-r72.py --revision "$REV"; echo "rc=$?"
  echo "## canonical census"
  echo "command: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi"
  cd /home/vgpnk/Projects/shokunin
  ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi > /dev/null 2>&1
  echo "census validate rc=$?"
} > "$OUT" 2>&1
echo "wrote $OUT"
