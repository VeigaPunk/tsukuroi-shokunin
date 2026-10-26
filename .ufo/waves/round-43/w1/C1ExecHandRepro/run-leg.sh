#!/bin/bash
# Outer launcher: creates the private user+mount namespace and runs ns-leg.sh in it.
#   run-leg.sh <scenario> [drop-uid]
# Privileged-in-namespace leg maps only our uid (unshare -r); the drop-uid leg adds the
# /etc/subuid range so a genuinely unprivileged in-namespace uid exists.
set -uo pipefail
SCEN=$1; DROP=${2:-}
NS=/fast/scratch/hyaku/tsukuroi-r43/C1ExecHandRepro/ns-leg.sh

if [ -z "$DROP" ]; then
    exec unshare --user --map-root-user --mount /usr/bin/bash "$NS" "$SCEN"
else
    exec unshare --user \
        --map-users=0:1000:1 --map-users=1:100000:65536 \
        --map-groups=0:1000:1 --map-groups=1:100000:65536 \
        --mount /usr/bin/bash "$NS" "$SCEN" "$DROP"
fi
