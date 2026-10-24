#!/usr/bin/bash
set -euo pipefail
scratch=$1
uid=$2
gid=$3
shift 3
/usr/bin/mount --bind "$scratch" /fast/scratch/hyaku
exec /usr/bin/setpriv --reuid "$uid" --regid "$gid" --clear-groups "$@"
