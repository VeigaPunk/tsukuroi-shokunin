#!/usr/bin/env bash
# Same as drive.sh but under the census's own option mode (set -euo pipefail).
set -euo pipefail
lib=$1
set +u
. "$lib"
set -u
s=${EPOCHREALTIME/./}
probe_scrub_record
e=${EPOCHREALTIME/./}
printf 'LINE %s\n' "$SCRUB_LINE"
printf 'MS %d\n' $(( (e - s) / 1000 ))
