#!/usr/bin/env bash
# Produce receipt-bound round-36 C1 before and sensitivity runs.
set -euo pipefail

BASE=6d76fb20f6ecbc940e5c8fff36c74060c885e161
MUTANT_PARENT=879daa95b898b5c624c609eced31f7d0d5b933e8
ATTR_REV=7e624d9b34331272c0089c184332c45ea302ab8e
PATH_REV=d0cf31b0189a4e1cc503678dba10eebe4a509ce0
TIMEOUT=14400

if [[ $# -ne 1 ]]; then
    printf 'usage: %s <probe-path>\n' "$0" >&2
    exit 2
fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
LANE=$(realpath -- "$SCRIPT_DIR/../../../../..")
RUNNER="$LANE/tools/run-receipt.py"
CALLER_DIR=$PWD
MUTANT_EVIDENCE="$LANE/.ufo/waves/round-34/w2"

if [[ -f "$1" ]]; then
    PROBE_FILE=$(realpath -- "$1")
elif [[ -f "$LANE/$1" ]]; then
    PROBE_FILE=$(realpath -- "$LANE/$1")
else
    printf 'probe path is not a readable file: %s\n' "$1" >&2
    exit 2
fi
PROBE_REL=$(realpath --relative-to="$LANE" "$PROBE_FILE")
case "$PROBE_REL" in
    ../*|/*)
        printf 'probe must be inside the lane: %s\n' "$PROBE_FILE" >&2
        exit 2
        ;;
esac
PROBE_REV=$(git -C "$LANE" rev-parse HEAD)
if ! git -C "$LANE" cat-file -e "$PROBE_REV:$PROBE_REL" 2>/dev/null; then
    printf 'probe must be tracked at current HEAD: %s\n' "$PROBE_REL" >&2
    exit 2
fi
PROBE_SHA=$(sha256sum -- "$PROBE_FILE")
PROBE_SHA=${PROBE_SHA%% *}
COMMITTED_SHA=$(git -C "$LANE" show "$PROBE_REV:$PROBE_REL" | sha256sum)
COMMITTED_SHA=${COMMITTED_SHA%% *}
if [[ "$PROBE_SHA" != "$COMMITTED_SHA" ]]; then
    printf 'probe bytes differ from tracked HEAD (worktree=%s committed=%s)\n' "$PROBE_SHA" "$COMMITTED_SHA" >&2
    exit 2
fi
if ! git -C "$LANE" cat-file -e "$BASE^{commit}" 2>/dev/null; then
    printf 'base revision is not available: %s\n' "$BASE" >&2
    exit 2
fi

run_probe() {
    local receipt=$1 expected_rc=$2
    shift 2
    local rc=0
    if python3 "$RUNNER" --lane "$LANE" --revision "$BASE" --tool-revision "$PROBE_REV" \
        --out "$CALLER_DIR/$receipt.jsonl" --timeout "$TIMEOUT" -- "$PROBE_REL" "$@"; then
        rc=0
    else
        rc=$?
    fi
    if [[ $rc -ne $expected_rc ]]; then
        printf '%s: expected run-receipt exit %s; got %s (see %s/%s.jsonl)\n' \
            "$receipt" "$expected_rc" "$rc" "$CALLER_DIR" "$receipt" >&2
        return 1
    fi
}

# The probe runs every configured channel (names, quiet, source) for livefive.
run_probe before-livefive 1 --revision '{rev}' --lane '{lane}' --base '{rev}' --set livefive --json
run_probe sensitivity-claim 0 --revision '{rev}' --lane '{lane}' --base '{rev}' --set claim --json
run_probe sensitivity-r33claim 0 --revision '{rev}' --lane '{lane}' --base '{rev}' --set r33claim --json
run_probe sensitivity-regression 0 --revision '{rev}' --lane '{lane}' --base '{rev}' --set regression --json

missing=0
run_mutant() {
    local name=$1 revision=$2 repo=$3
    if ! git -C "$repo" cat-file -e "$revision^{commit}" 2>/dev/null; then
        printf 'DEPENDENCY MISSING: %s mutant commit %s is unavailable in %s; evidence directory: %s/%s\n' \
            "$name" "$revision" "$repo" "$MUTANT_EVIDENCE" "$name" >&2
        missing=1
        return 0
    fi
    run_probe "sensitivity-$name" 1 --revision "$revision" --lane "$repo" --base "$MUTANT_PARENT" --set claim --json
}

# The round-34 evidence stores receipts/patches in .ufo; the committed variant repos were
# created in the read-only scratch locations named in those reports.
run_mutant MutAttrgetterCopy "$ATTR_REV" /fast/scratch/hyaku/tsukuroi-r34/MutAttrgetterCopy/repo
run_mutant MutPathCopy "$PATH_REV" /fast/scratch/hyaku/tsukuroi-r34/MutPathCopy/repo

if [[ $missing -ne 0 ]]; then
    printf 'before and base sensitivity receipts exist under %s; mutant checks require restoration of the named sandboxes\n' "$CALLER_DIR" >&2
    exit 2
fi
printf 'C1 before and sensitivity receipts written under %s\n' "$CALLER_DIR"
