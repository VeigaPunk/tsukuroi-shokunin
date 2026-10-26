inputs_newer_than() { # <epoch> <start point>... -> 1 when find lists an entry newer than epoch, else 0
    # R43-C1: decide on find's output, never on its exit status. find exits 1 when a start
    # point is missing or a directory is unreadable; under `set -o pipefail` that status used
    # to mask a listed match (`find … | grep -q .`), so a newer input read as "none newer".
    local epoch=$1 hit
    shift
    hit=$(find "$@" -newermt "@$epoch" -print 2>/dev/null)
    if [ -n "$hit" ]; then
        printf '1\n'
    else
        printf '0\n'
    fi
}
