#!/usr/bin/env bash
# round-73 after-measurement: every counting command the report cites, written to stdout.
# Run from the lane root with the measured revision as $1 (default: the branch tip).
set -u
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
REV=${1:-$(git -C "$L" rev-parse refs/heads/master)}
cd "$L" || exit 2
echo "# round-73 measurements at revision $REV ($(date -Is))"
echo
echo '## C1 — the UL row counter (frozen; sha256 '"$(sha256sum tools/count-ul-rows-r73.py | cut -d' ' -f1)")"
python3 tools/count-ul-rows-r73.py --revision "$REV"; echo "rc=$?"
echo
echo '## C1 — registry rows, knowledge notes (git plumbing over the same revision)'
echo -n 'registry_rows='; git show "$REV:corpus/SOURCES.md" | grep -cE '^ {0,3}\| *S[0-9]{3,}'
echo -n 'knowledge_notes='; git ls-tree --name-only "$REV:corpus/knowledge" | grep -c '\.md$'
echo -n 'new_rows='; git show "$REV:corpus/SOURCES.md" | grep -cE '^\| *S30[4-6] *\|'
echo
echo '## C1 — canonical sources census'
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi | tail -1; echo "census_rc=${PIPESTATUS[0]}"
echo
echo '## C2 — the routed-defect checker (frozen; sha256 '"$(sha256sum tools/check-r72-routed-r73.py | cut -d' ' -f1)")"
python3 tools/check-r72-routed-r73.py --revision "$REV"; echo "rc=$?"
echo
echo '## selftest tallies (capability, not a measurement of the targets)'
TMPDIR="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r73/l1" python3 tools/count-ul-rows-r73.py --selftest | tail -1
TMPDIR="${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r73/l1" python3 tools/check-r72-routed-r73.py --selftest | tail -1
echo
echo '## the r72 instruments named in the C2 erratum (unchanged this round)'
sha256sum tools/check-r71-routed-r72.py tools/check-selftest-tally.py
