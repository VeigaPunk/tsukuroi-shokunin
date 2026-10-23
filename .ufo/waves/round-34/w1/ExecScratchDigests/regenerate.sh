#!/usr/bin/env bash
# Regenerate the five round-33 "mutant vs frozen" oversize diffs from committed
# lane bytes, in a disposable sandbox clone.  Lane is read-only throughout.
#
# Usage:  bash regenerate.sh [VARIANT ...]        (default: all five)
# Env:    WORK=<scratch dir>   (default /fast/scratch/hyaku/tsukuroi-r34/ExecScratchDigests/regen)
#
# For each variant:
#   1. clone the lane once (never push; push URL disabled), detach at LANDED
#   2. reset the clone to LANDED (c8fcfbf6) and apply the *committed*
#      mutation-only patch under .ufo/waves/round-33/a3w2/<Seat>/ (extracted with
#      `git show CLAIM_BASE:<path>`, so the bytes are committed bytes)
#   3. verify the mutated file's sha256 against the hash recorded in the seat's
#      committed evidence
#   4. commit in the clone with the sandbox identity
#   5. run exactly the command the seat recorded: git diff 9c89ff4f HEAD
#   6. print regenerated size + sha256 and compare with the oversize scratch file
#
# PathCopy is the one variant whose mutation was never committed as a patch; its
# mutation is the one-line edit committed in
# .ufo/waves/round-33/a3w2/MutAfterPathCopy.md and .../commands.txt:
#   clean_env() returned os.environ["PATH"] instead of the fixed "/usr/bin:/bin".
# Step 2 performs exactly that substitution on the committed c8fcfbf6 blob and
# then checks the result against the mutant sha256 committed in hashes.json.
set -euo pipefail

LANE=${LANE:-/home/vgpnk/Projects/shokunin/tsukuroi-shokunin}
WORK=${WORK:-/fast/scratch/hyaku/tsukuroi-r34/ExecScratchDigests/regen}
REPO=$WORK/repo
CLAIM_BASE=6de666c427ba9aa6b4350561980bde8d0e7c261d
BASE=9c89ff4f093d07a6f92925518310ca6a7c8a2fa0
LANDED=c8fcfbf662db6debc6d7128c166ced31ca3176cf
TARGET_DIR=${TARGET_DIR:-/fast/scratch/hyaku/tsukuroi-r33a3/oversize}

# name | committed mutation patch (or NONE) | expected mutated-file sha256 | mutated file | oversize target
ROWS=(
  "MutAfterDropGlobal|.ufo/waves/round-33/a3w2/MutAfterDropGlobal/mutant-vs-landed.patch|050ca5de4a78557af2b0db2e68d506b20f316937cf7118bd751fbdcb02e6602d|tools/_revision.py|.ufo_waves_round-33_a3w2_MutAfterDropGlobal_mutant-vs-frozen.patch"
  "MutAfterHomeKeep|.ufo/waves/round-33/a3w2/MutAfterHomeKeep/mutation-vs-landed.patch|212d5c011af71fc361751d92036abeb00bcd4620c1a5fb9c15f1dea50d4fa71f|tools/_revision.py|.ufo_waves_round-33_a3w2_MutAfterHomeKeep_variant-vs-frozen.patch"
  "MutAfterOneNameCopy|.ufo/waves/round-33/a3w2/MutAfterOneNameCopy/mutation-only.patch|557d9267577c1f87d219a75554b7e5cefadb5d3b2d75184cfcdd2dd7e887435b|tools/_revision.py|.ufo_waves_round-33_a3w2_MutAfterOneNameCopy_mutant-vs-frozen.patch"
  "MutAfterPathCopy|NONE|e1f49f1ed0bd2b10a450b10512cd72d8b036ca1beac77dc3e0c89e1bfd07d8c3|tools/_revision.py|.ufo_waves_round-33_a3w2_MutAfterPathCopy_frozen-to-mutant.patch"
  "MutAfterV4Spread|.ufo/waves/round-33/a3w2/MutAfterV4Spread/mutant-only.patch|16c354deb51360d5c1d357ddb8d784e62dfb669c3d5f3c137887626b4a5da133|tools/mutants-owed-statements-r29-v4shapes.py|.ufo_waves_round-33_a3w2_MutAfterV4Spread_variant-vs-frozen.patch"
)

mkdir -p "$WORK/patches"
gel() { env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE "$@"; }
g() { gel git -C "$REPO" "$@"; }

if [ ! -d "$REPO/.git" ]; then
  gel git clone -q --no-local "$LANE" "$REPO"
  g remote set-url --push origin DISABLED
fi
g fetch -q origin 2>/dev/null || true
g checkout -q --detach "$CLAIM_BASE"

printf '%-22s %10s %-64s %-5s %10s\n' variant size sha256 match bytes
for row in "${ROWS[@]}"; do
  IFS='|' read -r name patch expect touched target <<<"$row"
  if [ "$#" -gt 0 ]; then
    wanted=0
    for arg in "$@"; do [ "$arg" = "$name" ] && wanted=1; done
    [ "$wanted" = 1 ] || continue
  fi

  g checkout -q --detach "$LANDED"
  g reset --hard -q "$LANDED"
  g clean -fdq

  if [ "$patch" = NONE ]; then
    # Documented one-line PathCopy mutation, derived from committed bytes.
    python3 - "$REPO/$touched" <<'PY'
import sys
p = sys.argv[1]
raw = open(p, 'rb').read()
old = b'"PATH": "/usr/bin:/bin"'
new = b'"PATH": os.environ["PATH"]'
assert raw.count(old) == 1, raw.count(old)
open(p, 'wb').write(raw.replace(old, new))
PY
    g add -- "$touched"
  else
    # Bytes come from the claim-base commit, not from the lane worktree.
    gel git -C "$REPO" show "$CLAIM_BASE:$patch" > "$WORK/patches/$name.mutation.patch"
    g apply --index "$WORK/patches/$name.mutation.patch"
  fi

  got_src=$(sha256sum "$REPO/$touched" | cut -d' ' -f1)
  if [ "$got_src" != "$expect" ]; then
    echo "$name: MUTATED-FILE MISMATCH expected=$expect got=$got_src" >&2
    exit 1
  fi

  g -c user.name=ctl -c user.email=ctl@sandbox -c commit.gpgsign=false \
    commit -q -m "regen $name from committed bytes"

  # The seat's recorded command (MutAfterHomeKeep/preparation.json, PathCopy/commands.txt)
  # with this host's global diff settings pinned so the bytes do not depend on ambient config.
  g -c diff.algorithm=histogram -c diff.mnemonicprefix=true -c diff.colormoved=plain \
    diff "$BASE" HEAD > "$WORK/patches/$name.vs-frozen.patch"

  size=$(stat -c%s "$WORK/patches/$name.vs-frozen.patch")
  got=$(sha256sum "$WORK/patches/$name.vs-frozen.patch" | cut -d' ' -f1)
  if [ -f "$TARGET_DIR/$target" ]; then
    tsha=$(sha256sum "$TARGET_DIR/$target" | cut -d' ' -f1)
    if [ "$got" = "$tsha" ]; then match=yes; else match=no; fi
  else
    tsha=absent; match=n/a
  fi
  printf '%-22s %10s %-64s %-5s %10s\n' "$name" "$size" "$got" "$match" "$(stat -c%s "$TARGET_DIR/$target" 2>/dev/null || echo -)"
  printf '    mutated-file-sha256 %s (committed evidence: %s)\n' "$got_src" "$expect"
  printf '    tree %s\n' "$(g rev-parse 'HEAD^{tree}')"
  printf '    target-sha256 %s\n' "$tsha"
done
echo "workdir: $WORK"
