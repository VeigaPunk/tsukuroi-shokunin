#!/bin/bash
# usage: canary1.sh <tool> [args...]  (run from the sandbox clone; canary lives in this seat's scratch)
set -u
S=/fast/scratch/hyaku/tsukuroi-r29/CritAxisFraming
C=$(mktemp -d "$S/canary-XXXX")
G() { env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git "$@"; }
G init -q -b canary "$C"; echo canary > "$C/CANARY"; G -C "$C" add CANARY
G -C "$C" -c user.name=c -c user.email=c@invalid -c commit.gpgsign=false commit -qm canary
fp() { ( G -C "$C" rev-parse HEAD; G -C "$C" for-each-ref; cd "$C/.git" && find objects refs -type f | sort; sha256sum HEAD index config; ls "$C" ) | sha256sum; }
B=$(fp)
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 "$@" >/dev/null 2>&1; echo "control_rc=$?"
env GIT_DIR="$C/.git" GIT_WORK_TREE="$C" GIT_INDEX_FILE="$C/.git/index" python3 "$@" > "$C.out" 2>&1; echo "canary_rc=$?"
A=$(fp)
[ "$A" = "$B" ] && echo canary_changed=false || echo canary_changed=true
G -C "$C" log --oneline --all | head -5
