#!/bin/sh
# Round-97 C2 doctored-table fixture and fail-closed legs. Reproducible from the lane root:
#   sh .ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh
# The clone is a scratch `git clone --shared`; the checker rides at `fixture/` (NOT `tools/`, so the
# coverage gate's tool set and row set are unchanged and its verdict is comparable). Every commit is
# made inside the clone with the fixture identity only.
set -eu
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r97/fixture
D=$LANE/.ufo/waves/round-97/before/fixtures
C=$S/doctored
ORIGIN=$S/origin.git
mkdir -p "$S" "$D"
rm -rf "$C" "$ORIGIN"
# a synthetic bare origin in scratch, so the coverage gate's landed-revision rule
# (refs/remotes/origin/master) has a real remote to read; the lane repo is only read.
# The base is PINNED to the pre-round tip (the round's baseline), so the fixture is reproducible
# after the freeze commit added the round's own three tools.
BASE=f48d16428d8bb92fd6cf546a745bff5b624e3f18
git clone --shared --bare -q "$LANE" "$ORIGIN"
git -C "$ORIGIN" update-ref refs/heads/master "$BASE"
git clone -q "$ORIGIN" "$C"
[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ] || { echo "fixture toplevel mismatch" >&2; exit 1; }
BASE=$(git -C "$C" rev-parse master)
[ "$BASE" = f48d16428d8bb92fd6cf546a745bff5b624e3f18 ] || { echo "fixture base is not the pinned pre-round tip: $BASE" >&2; exit 1; }
mkdir -p "$C/fixture"
cp "$LANE/tools/check-registry-content.py" "$C/fixture/check-registry-content.py"
sha256sum "$LANE/tools/check-registry-content.py" | tee "$D/doctored-checker.sha256"
python3 - "$C" <<'PY'
import sys
p = sys.argv[1] + "/SKILL.md"
s = open(p).read()
subs = [("default `auto`", "default `12.9.4`"),
        ("(39 fixtures", "(88 fixtures"),
        ("roster 103 (", "roster 99 ("),
        ("FAMILY_ROSTER, 103,", "FAMILY_ROSTER, 99,"),
        ("--selftest` (7 cases", "--selftest` (29 cases"),
        ("r96 VARIANTS N01-N04", "r96 VARIANTS N01-N05")]
for old, new in subs:
    assert s.count(old) == 1, (old, s.count(old))
    s = s.replace(old, new)
open(p, "w").write(s)
PY
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local \
  add -A
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local \
  commit -q -m "round-97 fixture: six content-only SKILL.md cell doctors + the round checker at fixture/"
REV=$(git -C "$C" rev-parse HEAD)
git -C "$C" push -q origin master
[ "$(git -C "$C" rev-parse refs/remotes/origin/master)" = "$REV" ] || { echo "scratch origin did not take the fixture commit" >&2; exit 1; }
echo "base $BASE" > "$D/doctored-revision.txt"
echo "doctored $REV" >> "$D/doctored-revision.txt"
git -C "$C" diff --stat "$BASE" "$REV" > "$D/doctored-diffstat.txt"
git -C "$C" diff --name-only "$BASE" "$REV" > "$D/doctored-files.txt"
git -C "$C" diff "$BASE" "$REV" > "$D/doctored.diff"
cat > "$D/doctored-recipe.txt" <<'RECIPE'
Fixture recipe (round 97 C2; reproducible with build-doctored-fixture.sh):
1. git clone --shared <lane> <scratch>/doctored  (base = the lane's master at freeze)
2. mkdir <clone>/fixture; cp <lane>/tools/check-registry-content.py <clone>/fixture/
3. Six content-only substitutions in <clone>/SKILL.md, each asserted to match exactly once:
     "default `auto`"            -> "default `12.9.4`"
     "(39 fixtures"              -> "(88 fixtures"
     "roster 103 ("              -> "roster 99 ("
     "FAMILY_ROSTER, 103,"       -> "FAMILY_ROSTER, 99,"
     "--selftest` (7 cases"      -> "--selftest` (29 cases"
     "r96 VARIANTS N01-N04"      -> "r96 VARIANTS N01-N05"
4. Commit in the clone only, identity tsukuroi-fixture <fixture@shokunin.local>.
5. Legs:
     python3 <clone>/fixture/check-registry-content.py --revision <rev>
     python3 <clone>/tools/check-registry-coverage.py --revision <rev>
The checker rides at fixture/, not tools/, so the coverage gate's tool set stays 154 and its verdict
is a fair blindness reading.
RECIPE
set +e
python3 "$C/fixture/check-registry-content.py" --revision "$REV" --json "$D/../dev/c2-content-doctored.json" > "$D/../dev/c2-content-doctored.txt" 2>&1
echo "content rc=$?" >> "$D/../dev/c2-content-doctored.txt"
python3 "$C/tools/check-registry-coverage.py" --revision "$REV" > "$D/../dev/c2-coverage-doctored.json" 2>"$D/../dev/c2-coverage-doctored.err"
echo "coverage rc=$?" >> "$D/../dev/c2-content-doctored.txt"
# fail-closed: a revision on a side branch is not an ancestor of master -> rc 2
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local checkout -q -b side "$BASE"
echo "# side" >> "$C/SKILL.md"
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local commit -q -am "side"
SIDE=$(git -C "$C" rev-parse HEAD)
git -C "$C" -c user.name=tsukuroi-fixture -c user.email=fixture@shokunin.local checkout -q master
python3 "$C/fixture/check-registry-content.py" --revision "$SIDE" > "$D/../dev/c2-nonancestor.txt" 2>&1
echo "nonancestor rc=$?" >> "$D/../dev/c2-nonancestor.txt"
# fail-closed: a 7-column registry row -> rc 2
T=$S/badtable
rm -rf "$T"; mkdir -p "$T/tools"
cp "$LANE/tools/check-limine-pins.py" "$T/tools/"
printf '# fixture\n\n## Gate and probe registry — round1 superseding current rows\n\n| Name | Kind | Entry | Verdict | Self-test | Pinned | Scope |\n|---|---|---|---|---|---|---|\n| limine-pins | gate | `python3 tools/check-limine-pins.py` | 0;1;2 | `--selftest` | schema `x` | none |\n' > "$T/SKILL.md"
python3 "$LANE/tools/check-registry-content.py" --root "$T" > "$D/../dev/c2-badtable.txt" 2>&1
echo "badtable rc=$?" >> "$D/../dev/c2-badtable.txt"
set -e
rm -rf "$C" "$T" "$ORIGIN"
echo "fixture done rev=$REV"
