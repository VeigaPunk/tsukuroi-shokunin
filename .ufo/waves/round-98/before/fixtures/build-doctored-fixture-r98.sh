#!/bin/sh
# Round-98 C2 doctored-table fixtures D1 and D2 (+ lie twin). Reproducible from the lane root:
#   sh .ufo/waves/round-98/before/fixtures/build-doctored-fixture-r98.sh
# Each clone is a scratch `git clone --shared` off the pinned pre-round base; the checker rides at
# `fixture/` (NOT `tools/`, so the coverage gate's tool set and row set are unchanged and its
# verdict is comparable). Every commit is made inside the clone with the fixture identity only.
set -eu
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r98/fixture
D=$LANE/.ufo/waves/round-98/before/fixtures
C=$S/doctored-r98
ORIGIN=$S/origin-r98.git
mkdir -p "$S" "$D"
rm -rf "$C" "$ORIGIN"
BASE=b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a
git clone --shared --bare -q "$LANE" "$ORIGIN"
git -C "$ORIGIN" update-ref refs/heads/master "$BASE"
git clone -q "$ORIGIN" "$C"
[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ] || { echo "fixture toplevel mismatch" >&2; exit 1; }
mkdir -p "$C/fixture"
cp "$LANE/tools/check-registry-content-r98.py" "$C/fixture/check-registry-content-r98.py"
cp "$LANE/tools/check-registry-content.py" "$C/fixture/check-registry-content-r97.py"
# D1: SKILL.md content-only doctor (make-r96-bends row: contiguous span -> comma span).
python3 - "$C" <<'PY'
import sys
p = sys.argv[1] + "/SKILL.md"
s = open(p).read()
old, new = "r96 VARIANTS N01-N04", "r96 VARIANTS N01,N03"
assert s.count(old) == 1, (old, s.count(old))
s = s.replace(old, new)
open(p, "w").write(s)
PY
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local add -A
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local commit -q -m "round-98 fixture D1: comma-span doctor"
D1=$(git -C "$C" rev-parse HEAD)
git -C "$C" push -q origin master
echo "base $BASE" > "$D/doctored-r98-revision.txt"
echo "D1 $D1" >> "$D/doctored-r98-revision.txt"
# D2: VARIANTS keys N01,N03 (drop the N02 entry) + row states the comma span.
python3 - "$C" <<'PY'
import sys, subprocess
c = sys.argv[1]
subprocess.run(["git", "-C", c, "checkout", "b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a", "--", "SKILL.md"], check=True)
p = c + "/tools/make-r96-bends.py"
lines = open(p).read().splitlines(keepends=True)
out = []
skip = False
for ln in lines:
    if ln.startswith('    "N02-y-cap-8"') or ln.startswith('    "N04-extra-components"'):
        skip = True
        continue
    if skip:
        if ln.strip() == "),":
            skip = False
            continue
        continue
    out.append(ln)
assert not skip, "a dropped VARIANTS entry was not closed"
open(p, "w").write("".join(out))
sk = c + "/SKILL.md"
t = open(sk).read()
old2, new2 = "r96 VARIANTS N01-N04", "r96 VARIANTS N01,N03"
assert t.count(old2) == 1, (old2, t.count(old2))
t = t.replace(old2, new2)
open(sk, "w").write(t)
PY
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local add -A
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local commit -q -m "round-98 fixture D2: gap keys + comma row"
D2=$(git -C "$C" rev-parse HEAD)
git -C "$C" push -q -f origin master
echo "D2 $D2" >> "$D/doctored-r98-revision.txt"
# Lie twin: same gap keys, row back to the contiguous span.
python3 - "$C" <<'PY'
import sys
sk = sys.argv[1] + "/SKILL.md"
t = open(sk).read()
old2, new2 = "r96 VARIANTS N01,N03", "r96 VARIANTS N01-N03"
assert t.count(old2) == 1, (old2, t.count(old2))
t = t.replace(old2, new2)
open(sk, "w").write(t)
PY
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local add -A
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local commit -q -m "round-98 fixture D2-lie: gap keys + contiguous row"
D2L=$(git -C "$C" rev-parse HEAD)
git -C "$C" push -q -f origin master
echo "D2lie $D2L" >> "$D/doctored-r98-revision.txt"
git -C "$C" diff --stat "$BASE" "$D1" > "$D/doctored-r98-d1-diffstat.txt"
git -C "$C" diff --name-only "$BASE" "$D1" > "$D/doctored-r98-d1-files.txt"
git -C "$C" diff --stat "$BASE" "$D2" > "$D/doctored-r98-d2-diffstat.txt"
git -C "$C" diff --name-only "$BASE" "$D2" > "$D/doctored-r98-d2-files.txt"
echo "$D1" > "$D/doctored-r98-D1"
echo "$D2" > "$D/doctored-r98-D2"
echo "$D2L" > "$D/doctored-r98-D2lie"
echo "doctored fixtures OK: D1=$D1 D2=$D2 D2lie=$D2L"
