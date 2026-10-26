#!/bin/sh
# ConsiderWeight (round-39 w1, item A-2) — exact commands behind the evidence-weight table.
# Run from /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. Read-only: git reads only.
set -e
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin

# R1. the round's commit span (--reverse: first line = round's first commit)
git log --first-parent --format='%h %ad %s' --date=short --grep '^round-36' master

# R1b. dispatched seat count for the round (items in the frozen wave spec)
git show master:.ufo/waves/round-36/w1-spec.json | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["items"]))'

# R2. evidence bytes in the round's dir (committed content as checked out, not pack size)
git ls-tree -r -l master -- .ufo/waves/round-36 | awk '{s+=$4} END{print s, NR}'

# R3. heaviest single files in that dir
git ls-tree -r -l master -- .ufo/waves/round-36 | sort -k4 -n | tail -3 | awk '{print $4, $5}'

# R4. knowledge growth over the round span (S = parent of first round commit, E = last round commit)
S=$(git rev-parse $(git log --first-parent --format=%H --grep '^round-36' --reverse master | head -1)^)
E=$(git log --first-parent --format=%H --grep '^round-36' master | head -1)
git ls-tree -r -l "$E" -- corpus | awk '{s+=$4} END{print s}'   # corpus at close
git ls-tree -r -l "$S" -- corpus | awk '{s+=$4} END{print s}'   # corpus at start
git ls-tree -r -l "$E"          | awk '{s+=$4} END{print s}'    # whole tree at close
git ls-tree -r -l "$S"          | awk '{s+=$4} END{print s}'    # whole tree at start

# R5. duplicate blobs under the wave dirs (git stores one copy; every checkout pays per path)
git ls-tree -r -l master -- .ufo/waves | awk '{print $3, $4}' | sort \
 | awk '{c[$1]++; s[$1]=$2} END{for(k in c) if(c[k]>1) e+=s[k]*(c[k]-1); print e}'

# R6. round-39 so far: committed, then live working tree (moves while seats write)
git ls-tree -r -l master -- .ufo/waves/round-39 | awk '{s+=$4;n++} END{print n, s}'
find .ufo/waves/round-39 -type f -printf '%s\n' | awk '{s+=$1;n++} END{print n, s}'

# R7. the single commit that added 87.7 MB, and its message
git show --stat --format='' fe24c4c | tail -1
git log -1 --format=%B fe24c4c

# R8. weight of one heavy capture file: gzip, and its stored pack size
git show master:.ufo/waves/round-36/w1/ExecLiveViewDesign/capture/base-final-6d76fb20/handoff.execve.log | gzip -9 | wc -c
git verify-pack -v .git/objects/pack/*.idx | grep '^61bae29e1d3d860fb95f0201b51a96b2b8a56c19 '
