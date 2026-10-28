#!/bin/sh
if [ "$#" -ge 4 ] && [ "$3" = "show" ] && [ "$4" = "${FORGE_REV:-x}:PROVINCE.md" ]; then cat "$FORGE_PROVINCE"; exit 0; fi
exec /usr/bin/git "$@"
