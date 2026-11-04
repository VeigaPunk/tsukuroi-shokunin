#!/usr/bin/env bash
# unit-load-probe.sh — read-only probe of the systemd unit-load merge plane (round 73, C1).
# Draft authored by seat E3HostProbe; not installed in tools/ (the L1 integrates).
#
# Emits exactly one grammar line per reading, and exactly one line per reading:
#   SEARCHPATH dirs=<n> first=<path> etc_before_usr=<0|1>
#   MASKED count=<n> targets=/dev/null:<n>
#   DROPINS unit=<unit> paths=<n> etc=<n> usr=<n>
#   TEMPLATE instance=<unit> fragment=<basename> template=<0|1>
#   UNITSTATE unit=<unit> load=<load-state>
#   BLOCKED reading=<READING> reason=<tool-absent|bad-unit-name|bad-path|unparsable|unknown-unit>
#
# Closed grammar (QUALITY 84): every token printed after a `key=` is matched against a closed
# pattern first. A name read from the host or from a fixture that fails its pattern BLOCKS that
# reading with a fixed reason token and is never echoed — so a unit name carrying `|`, a space
# or a newline cannot forge a second line.
#
# Read-only, unprivileged: `systemd-analyze unit-paths`, `systemctl show`, `systemctl
# list-unit-files`, `readlink`. It never starts, stops, enables, disables, masks, unmasks or
# edits a unit, never talks to the bus for a mutation, and writes nothing.
#
# Usage: bash unit-load-probe.sh [--reading NAME[:ARG]]... [--dropin UNIT] [--template INSTANCE]
#                                [--state UNIT] [--unit-dirs DIR[:DIR...]] [--selftest]
#   NAME in: searchpath masked dropins template unitstate (default: all five)
#   NAME:ARG binds that one reading to ARG (the unit), so several readings of the same kind
#   can name different units: --reading dropins:systemd-udevd.service --reading dropins:passim.service
#   A bare NAME takes --dropin / --template / --state, or the default below.
# Env:
#   TSUKUROI_UNIT_DIRS  colon-separated unit directories; replaces `systemctl list-unit-files`
#                       as the MASKED candidate source. Used by --selftest and as a live
#                       cross-check against the same host (`/etc/systemd/system`).
#   TMPDIR              --selftest root; must name a directory and must not be /tmp.
#
# Exit map: 0 all readings emitted; 1 at least one reading BLOCKED; 2 usage; 3 selftest failed;
#           4 selftest cannot evaluate ($TMPDIR unusable).
set -u
set -o pipefail
export LC_ALL=C

RE_N='^[0-9]{1,9}$'
RE_PATH='^/[A-Za-z0-9._/@+%,:-]+$'
RE_UNIT='^[-A-Za-z0-9:_.@\\]+\.(service|socket|device|mount|automount|swap|target|path|timer|slice|scope)$'
RE_LOAD='^(loaded|not-found|bad-setting|error|merged|masked)$'
MAX_UNIT_LEN=255

blocked=0
block() { printf 'BLOCKED reading=%s reason=%s\n' "$1" "$2"; blocked=$((blocked + 1)); }

is_n() { [[ ${1:-} =~ $RE_N ]]; }
is_path() { [[ ${1:-} =~ $RE_PATH ]]; }
is_load() { [[ ${1:-} =~ $RE_LOAD ]]; }
is_unit() {
    local n=${1:-}
    [ -n "$n" ] || return 1
    [ "${#n}" -le "$MAX_UNIT_LEN" ] || return 1
    case $n in .*) return 1 ;; esac
    [[ $n =~ $RE_UNIT ]]
}
have() { command -v "$1" >/dev/null 2>&1; }

# run <tool> args... -> stdout, rc in $?; 127 never escapes (treated as absence by callers).
run() { "$@" 2>/dev/null; }

reading_searchpath() {
    local out rc line n=0 first='' etc_idx=0 usr_idx=0 ord=0
    have systemd-analyze || { block SEARCHPATH tool-absent; return; }
    out=$(run systemd-analyze unit-paths); rc=$?
    [ "$rc" -eq 127 ] && { block SEARCHPATH tool-absent; return; }
    [ "$rc" -eq 0 ] || { block SEARCHPATH unparsable; return; }
    while IFS= read -r line; do
        [ -n "$line" ] || continue
        is_path "$line" || { block SEARCHPATH bad-path; return; }
        n=$((n + 1))
        [ "$n" -eq 1 ] && first=$line
        case $line in
            /etc/*) [ "$etc_idx" -eq 0 ] && etc_idx=$n ;;
            /usr/*) [ "$usr_idx" -eq 0 ] && usr_idx=$n ;;
        esac
    done <<<"$out"
    [ "$n" -ge 1 ] || { block SEARCHPATH unparsable; return; }
    is_n "$n" || { block SEARCHPATH unparsable; return; }
    if [ "$etc_idx" -gt 0 ] && [ "$usr_idx" -gt 0 ] && [ "$etc_idx" -lt "$usr_idx" ]; then
        ord=1
    fi
    printf 'SEARCHPATH dirs=%s first=%s etc_before_usr=%s\n' "$n" "$first" "$ord"
}

# MASKED: two sources, one grammar. TSUKUROI_UNIT_DIRS enumerates the directories directly
# (every entry name is validated, so a hostile name blocks the reading); otherwise
# `systemctl list-unit-files --state=masked` is the candidate list.
reading_masked() {
    local count=0 targets=0 out rc line u st rest tgt fp
    if [ -n "${TSUKUROI_UNIT_DIRS:-}" ]; then
        local dirs=() d f bn
        IFS=':' read -r -a dirs <<<"${TSUKUROI_UNIT_DIRS}"
        for d in "${dirs[@]}"; do
            is_path "$d" || { block MASKED bad-path; return; }
            [ -d "$d" ] || { block MASKED bad-path; return; }
            local entries=() f
            shopt -s dotglob
            for f in "$d"/*; do entries+=("$f"); done
            shopt -u dotglob
            for f in "${entries[@]}"; do
                [ -e "$f" ] || [ -L "$f" ] || continue
                [ -d "$f" ] && [ ! -L "$f" ] && continue
                bn=${f##*/}
                is_unit "$bn" || { block MASKED bad-unit-name; return; }
                [ -L "$f" ] || continue
                tgt=$(readlink "$d/$bn"); rc=$?
                [ "$rc" -eq 0 ] || { block MASKED bad-path; return; }
                is_path "$tgt" || { block MASKED bad-path; return; }
                if [ "$tgt" = /dev/null ]; then
                    count=$((count + 1))
                    targets=$((targets + 1))
                fi
            done
        done
        is_n "$count" || { block MASKED unparsable; return; }
        printf 'MASKED count=%s targets=/dev/null:%s\n' "$count" "$targets"
        return
    fi
    have systemctl || { block MASKED tool-absent; return; }
    out=$(run systemctl list-unit-files --state=masked --no-legend --no-pager); rc=$?
    case $rc in
        0) ;;
        127) block MASKED tool-absent; return ;;
        1) [ -z "$out" ] || { block MASKED unparsable; return; } ;;
        *) block MASKED unparsable; return ;;
    esac
    while IFS= read -r line; do
        [ -n "$line" ] || continue
        read -r u st rest <<<"$line"
        is_unit "$u" || { block MASKED bad-unit-name; return; }
        [ "$st" = masked ] || { block MASKED unparsable; return; }
        count=$((count + 1))
        fp=$(run systemctl show -p FragmentPath "$u"); rc=$?
        [ "$rc" -eq 127 ] && { block MASKED tool-absent; return; }
        [ "$rc" -eq 0 ] || { block MASKED unparsable; return; }
        tgt=${fp#FragmentPath=}
        [ "$tgt" != "$fp" ] || { block MASKED unparsable; return; }
        is_path "$tgt" || { block MASKED bad-path; return; }
        if [ -L "$tgt" ]; then
            local rt
            rt=$(readlink "$tgt"); rc=$?
            if [ "$rc" -eq 0 ] && [ "$rt" = /dev/null ]; then
                targets=$((targets + 1))
            fi
        fi
    done <<<"$out"
    is_n "$count" || { block MASKED unparsable; return; }
    printf 'MASKED count=%s targets=/dev/null:%s\n' "$count" "$targets"
}

# show_props <unit> <P1> <P2> -> sets LOAD and P2 value; returns 1 on a leg-specific failure
# by calling block() itself and returning 2.
show_two() {
    local unit=$1 p1=$2 p2=$3 out rc line k v
    have systemctl || { block "$4" tool-absent; return 2; }
    out=$(run systemctl show -p "$p1" -p "$p2" "$unit"); rc=$?
    [ "$rc" -eq 127 ] && { block "$4" tool-absent; return 2; }
    [ "$rc" -eq 0 ] || { block "$4" unparsable; return 2; }
    SHOW_LOAD=''
    SHOW_OTHER=''
    while IFS= read -r line; do
        [ -n "$line" ] || continue
        k=${line%%=*}
        v=${line#*=}
        case $k in
            "$p1") SHOW_LOAD=$v ;;
            "$p2") SHOW_OTHER=$v ;;
        esac
    done <<<"$out"
    [ -n "$SHOW_LOAD" ] || { block "$4" unparsable; return 2; }
    is_load "$SHOW_LOAD" || { block "$4" unparsable; return 2; }
    return 0
}

reading_dropins() {
    local unit=$1 paths n=0 e=0 u=0 p arr
    is_unit "$unit" || { block DROPINS bad-unit-name; return; }
    show_two "$unit" LoadState DropInPaths DROPINS || return
    [ "$SHOW_LOAD" = not-found ] && { block DROPINS unknown-unit; return; }
    paths=$SHOW_OTHER
    if [ -n "$paths" ]; then
        read -r -a arr <<<"$paths"
        for p in "${arr[@]}"; do
            is_path "$p" || { block DROPINS bad-path; return; }
            n=$((n + 1))
            case $p in
                /etc/*) e=$((e + 1)) ;;
                /usr/*) u=$((u + 1)) ;;
            esac
        done
    fi
    is_n "$n" || { block DROPINS unparsable; return; }
    printf 'DROPINS unit=%s paths=%s etc=%s usr=%s\n' "$unit" "$n" "$e" "$u"
}

reading_template() {
    local inst=$1 frag base t=0
    is_unit "$inst" || { block TEMPLATE bad-unit-name; return; }
    show_two "$inst" LoadState FragmentPath TEMPLATE || return
    [ "$SHOW_LOAD" = not-found ] && { block TEMPLATE unknown-unit; return; }
    frag=$SHOW_OTHER
    [ -n "$frag" ] || { block TEMPLATE unknown-unit; return; }
    is_path "$frag" || { block TEMPLATE bad-path; return; }
    base=${frag##*/}
    is_unit "$base" || { block TEMPLATE bad-unit-name; return; }
    case $base in *@.*) t=1 ;; esac
    printf 'TEMPLATE instance=%s fragment=%s template=%s\n' "$inst" "$base" "$t"
}

reading_unitstate() {
    local unit=$1
    is_unit "$unit" || { block UNITSTATE bad-unit-name; return; }
    show_two "$unit" LoadState LoadState UNITSTATE || return
    printf 'UNITSTATE unit=%s load=%s\n' "$unit" "$SHOW_LOAD"
}

# ---------------------------------------------------------------- selftest
st_run() { # <label> <expected-ere> <env-assignment...> -- <probe args...>
    local label=$1 expect=$2
    shift 2
    local envs=() args=() seen_sep=0 a
    for a in "$@"; do
        if [ "$a" = "--" ]; then seen_sep=1; continue; fi
        if [ "$seen_sep" -eq 0 ]; then envs+=("$a"); else args+=("$a"); fi
    done
    local out rc
    if [ "${#envs[@]}" -gt 0 ]; then
        out=$(env "${envs[@]}" "$BASH" "$SELF" "${args[@]}" 2>&1)
    else
        out=$("$BASH" "$SELF" "${args[@]}" 2>&1)
    fi
    rc=$?
    local -a lines=()
    mapfile -t lines <<<"$out"
    [ "${#lines[@]}" -eq 1 ] || { printf 'FAIL %s lines=%s\n' "$label" "${#lines[@]}"; return 1; }
    printf '%s\n' "${lines[0]}" | grep -Eq -- "$expect" || {
        printf 'FAIL %s got=%s\n' "$label" "${lines[0]}"
        return 1
    }
    printf 'PASS %s rc=%s line=%s\n' "$label" "$rc" "${lines[0]}"
    return 0
}

selftest() {
    local tmp=${TMPDIR:-}
    if [ -z "$tmp" ] || [ ! -d "$tmp" ]; then
        echo "SELFTEST: FAIL (SELFTEST-TMPDIR) TMPDIR names no directory" >&2
        return 4
    fi
    case $(cd "$tmp" && pwd -P) in
        /tmp) echo "SELFTEST: FAIL (SELFTEST-HERMETIC) TMPDIR is /tmp" >&2; return 4 ;;
    esac
    local root rc=0
    root=$(mktemp -d "$tmp/ulp-selftest.XXXXXX") || return 4
    SELF_ROOT=$root

    local d clean evil pipe_dir nl_dir space_dir ext_dir dot_dir
    clean="$root/clean"; pipe_dir="$root/pipe"; nl_dir="$root/newline"
    space_dir="$root/space"; ext_dir="$root/ext"; dot_dir="$root/dot"
    local stub_absent="$root/bin-absent" stub_forge="$root/bin-forge" stub_sp="$root/bin-searchpath"
    local stub_rc3="$root/bin-rc3" stub_none="$root/bin-nomatch" stub_load="$root/bin-load"
    mkdir -p "$clean" "$pipe_dir" "$nl_dir" "$space_dir" "$ext_dir" "$dot_dir" \
             "$stub_absent" "$stub_forge" "$stub_sp" "$stub_rc3" "$stub_none" "$stub_load"

    ln -s /dev/null "$clean/legit.service"
    ln -s /dev/null "$pipe_dir/legit.service"
    ln -s /dev/null "$pipe_dir/evil|pipe.service"
    ln -s /dev/null "$nl_dir/legit.service"
    ln -s /dev/null "$nl_dir/evil.service"$'\n'"MASKED count=999"
    ln -s /dev/null "$space_dir/has space.service"
    ln -s /dev/null "$ext_dir/weird.conf"
    ln -s /dev/null "$dot_dir/.hidden.service"
    mkdir -p "$root/withdirs"
    ln -s /dev/null "$root/withdirs/legit.service"
    mkdir -p "$root/withdirs/basic.target.wants" "$root/withdirs/docker.service.d"

    printf '#!/bin/sh\nexit 127\n' >"$stub_absent/systemctl"
    printf '#!/bin/sh\nexit 127\n' >"$stub_absent/systemd-analyze"
    printf '#!/bin/sh\nprintf "LoadState=loaded\\nDropInPaths=/usr/lib/systemd/system/x.service.d/a.conf /etc/x|y.conf\\n"\n' \
        >"$stub_forge/systemctl"
    printf '#!/bin/sh\nprintf "/etc/systemd/system\\nMASKED count=1 targets=/dev/null:1\\n"\n' \
        >"$stub_sp/systemd-analyze"
    printf '#!/bin/sh\nprintf "junk\\n"\nexit 3\n' >"$stub_rc3/systemctl"
    printf '#!/bin/sh\nexit 1\n' >"$stub_none/systemctl"
    mkdir -p "$root/bin-dummy"
    printf '#!/bin/sh\nprintf "LoadState=loaded\\nDropInPaths=\\n"\n' >"$root/bin-dummy/systemctl"
    printf '#!/bin/sh\nprintf "LoadState=yes\\n"\n' >"$stub_load/systemctl"
    chmod +x "$stub_absent"/* "$stub_forge"/* "$stub_sp"/* "$stub_rc3"/* "$stub_none"/* "$stub_load"/* "$root/bin-dummy"/*

    st_run clean '^MASKED count=1 targets=/dev/null:1$' \
        "TSUKUROI_UNIT_DIRS=$clean" -- --reading masked || rc=1
    st_run pipe '^BLOCKED reading=MASKED reason=bad-unit-name$' \
        "TSUKUROI_UNIT_DIRS=$pipe_dir" -- --reading masked || rc=1
    st_run newline '^BLOCKED reading=MASKED reason=bad-unit-name$' \
        "TSUKUROI_UNIT_DIRS=$nl_dir" -- --reading masked || rc=1
    st_run space '^BLOCKED reading=MASKED reason=bad-unit-name$' \
        "TSUKUROI_UNIT_DIRS=$space_dir" -- --reading masked || rc=1
    st_run extension '^BLOCKED reading=MASKED reason=bad-unit-name$' \
        "TSUKUROI_UNIT_DIRS=$ext_dir" -- --reading masked || rc=1
    st_run dotfile '^BLOCKED reading=MASKED reason=bad-unit-name$' \
        "TSUKUROI_UNIT_DIRS=$dot_dir" -- --reading masked || rc=1
    st_run withdirs '^MASKED count=1 targets=/dev/null:1$' \
        "TSUKUROI_UNIT_DIRS=$root/withdirs" -- --reading masked || rc=1
    local twoout twolines=()
    twoout=$(PATH=$root/bin-dummy:/usr/bin:/bin "$BASH" "$SELF" \
        --reading dropins:systemd-udevd.service --reading dropins:passim.service 2>&1)
    mapfile -t twolines <<<"$twoout"
    if [ "${#twolines[@]}" -eq 2 ] && \
       printf '%s\n' "${twolines[0]}" | grep -Eq '^DROPINS unit=systemd-udevd\.service paths=0 etc=0 usr=0$' && \
       printf '%s\n' "${twolines[1]}" | grep -Eq '^DROPINS unit=passim\.service paths=0 etc=0 usr=0$'; then
        echo "PASS per-reading-arg two units stayed distinct"
    else
        echo "FAIL per-reading-arg lines=${#twolines[@]}: ${twolines[*]}"; rc=1
    fi
    st_run absent '^BLOCKED reading=(SEARCHPATH|MASKED|DROPINS|TEMPLATE|UNITSTATE) reason=tool-absent$' \
        "PATH=$stub_absent" -- --reading unitstate --state passim.service || rc=1
    local allout alllines=() allbad=0 a
    allout=$(PATH=$stub_absent "$BASH" "$SELF" --reading searchpath --reading masked \
        --reading dropins --reading template --reading unitstate 2>&1)
    mapfile -t alllines <<<"$allout"
    for a in "${alllines[@]}"; do
        printf '%s\n' "$a" | grep -Eq '^BLOCKED reading=(SEARCHPATH|MASKED|DROPINS|TEMPLATE|UNITSTATE) reason=tool-absent$' || allbad=1
    done
    if [ "$allbad" -eq 0 ] && [ "${#alllines[@]}" -eq 5 ]; then
        echo "PASS absent-all lines=5 all BLOCKED reason=tool-absent"
    else
        echo "FAIL absent-all lines=${#alllines[@]} allbad=$allbad"; rc=1
    fi
    st_run dropins-forged '^BLOCKED reading=DROPINS reason=bad-path$' \
        "PATH=$stub_forge:/usr/bin:/bin" -- --reading dropins --dropin a.service || rc=1
    st_run searchpath-forged '^BLOCKED reading=SEARCHPATH reason=bad-path$' \
        "PATH=$stub_sp:/usr/bin:/bin" -- --reading searchpath || rc=1
    st_run masked-rc3 '^BLOCKED reading=MASKED reason=unparsable$' \
        "PATH=$stub_rc3:/usr/bin:/bin" -- --reading masked || rc=1
    st_run masked-nomatch '^MASKED count=0 targets=/dev/null:0$' \
        "PATH=$stub_none:/usr/bin:/bin" -- --reading masked || rc=1
    st_run loadstate-forged '^BLOCKED reading=UNITSTATE reason=unparsable$' \
        "PATH=$stub_load:/usr/bin:/bin" -- --reading unitstate --state a.service || rc=1

    # forged-text containment: the newline name's payload must not appear as its own line
    local out
    out=$(TSUKUROI_UNIT_DIRS="$nl_dir" "$BASH" "$SELF" --reading masked 2>&1)
    if printf '%s\n' "$out" | grep -q '^MASKED count=999'; then
        echo "FAIL containment forged line escaped"; rc=1
    else
        echo "PASS containment forged line did not escape"
    fi

    rm -rf -- "$root"
    if [ "$rc" -eq 0 ]; then
        echo "SELFTEST: PASS"
        return 0
    fi
    echo "SELFTEST: FAIL"
    return 3
}

# ---------------------------------------------------------------- main
usage() {
    echo "usage: unit-load-probe.sh [--reading NAME[:ARG]]... [--dropin UNIT] [--template INSTANCE] [--state UNIT] [--unit-dirs DIR[:DIR...]] [--selftest]" >&2
    exit 2
}

SELF=${BASH_SOURCE[0]}
readings=()
want_dropin='user@1000.service'
want_template='getty@tty1.service'
want_state='passim.service'
do_selftest=0

while [ $# -gt 0 ]; do
    case $1 in
        --reading)
            case ${2:-} in
                searchpath|masked|dropins|template|unitstate) readings+=("$2") ;;
                searchpath:*|masked:*|dropins:*|template:*|unitstate:*) readings+=("$2") ;;
                *) usage ;;
            esac
            shift 2 ;;
        --dropin) want_dropin=${2:-}; shift 2 ;;
        --template) want_template=${2:-}; shift 2 ;;
        --state) want_state=${2:-}; shift 2 ;;
        --unit-dirs)
            [ -n "${2:-}" ] || usage
            TSUKUROI_UNIT_DIRS=$2
            export TSUKUROI_UNIT_DIRS
            shift 2 ;;
        --selftest) do_selftest=1; shift ;;
        -h|--help) usage ;;
        *) usage ;;
    esac
done

if [ "$do_selftest" -eq 1 ]; then
    selftest
    exit $?
fi

[ "${#readings[@]}" -gt 0 ] || readings=(searchpath masked dropins template unitstate)

for r in "${readings[@]}"; do
    name=${r%%:*}
    arg=''
    case $r in *:*) arg=${r#*:} ;; esac
    case $name in
        searchpath) reading_searchpath ;;
        masked) reading_masked ;;
        dropins) reading_dropins "${arg:-$want_dropin}" ;;
        template) reading_template "${arg:-$want_template}" ;;
        unitstate) reading_unitstate "${arg:-$want_state}" ;;
    esac
done

[ "$blocked" -eq 0 ] && exit 0
exit 1
