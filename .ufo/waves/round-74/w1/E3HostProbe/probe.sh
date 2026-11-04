#!/usr/bin/env bash
# unit-fragment-probe.sh — read-only probe of the systemd unit-fragment resolution surface (round 74, C1).
# Draft authored by seat E3HostProbe; not installed in tools/ (the L1 integrates).
#
# Emits exactly one grammar line per reading, and exactly one line per reading:
#   SEARCHPATH scope=<system|user> dirs=<n> first=<path> etc_before_usr=<0|1>
#   MASKED count=<n> targets=/dev/null:<n>
#   CAT unit=<unit> fragment=<path> masked=<0|1> dropins=<n>
#   TEMPLATE instance=<unit> fragment=<basename> template=<0|1>
#   ALIAS alias=<unit> target=<target> may_alias=<0|1>
#   UNITSTATE unit=<unit> file_state=<state> load_state=<load>
#   BLOCKED reading=<READING> reason=<tool-absent|bad-unit-name|bad-path|unparsable|unknown-unit|self-alias|incompatible-type>
#
# Closed grammar (QUALITY 84): every token printed after a `key=` is matched against a closed
# pattern first. A name read from the host or from a fixture that fails its pattern BLOCKS that
# reading with a fixed reason token and is never echoed — so a unit name carrying `|`, a space,
# tab, semicolon or a newline cannot forge a second line or escape.
#
# Read-only, unprivileged: `systemd-analyze unit-paths`, `systemctl cat`, `systemctl show`,
# `systemctl is-enabled`, `systemctl list-unit-files`, `readlink`. It never starts, stops,
# enables, disables, masks, unmasks or edits a unit, never talks to the bus for a mutation,
# and writes nothing.
#
# Usage: bash probe.sh [--reading NAME[:ARG]]... [--cat UNIT] [--template INSTANCE]
#                      [--alias UNIT] [--state UNIT] [--scope system|user]
#                      [--unit-dirs DIR[:DIR...]] [--selftest]
#
# Exit map: 0 all readings emitted; 1 at least one reading BLOCKED; 2 usage;
#           3 selftest failed; 4 selftest cannot evaluate ($TMPDIR unusable).
set -u
set -o pipefail
export LC_ALL=C

RE_N='^[0-9]{1,9}$'
RE_PATH='^/[A-Za-z0-9._/@+%,:-]+$'
RE_UNIT='^[-A-Za-z0-9:_.@\\]+\.(service|socket|device|mount|automount|swap|target|path|timer|slice|scope)$'
RE_LOAD='^(loaded|not-found|bad-setting|error|merged|masked)$'
RE_FILE_STATE='^(enabled|enabled-runtime|linked|linked-runtime|alias|masked|masked-runtime|static|disabled|indirect|generated|transient|bad|not-found)$'
MAX_UNIT_LEN=255

blocked=0
block() { printf 'BLOCKED reading=%s reason=%s\n' "$1" "$2"; blocked=$((blocked + 1)); }

is_n() { [[ ${1:-} =~ $RE_N ]]; }
is_path() { [[ ${1:-} =~ $RE_PATH ]]; }
is_load() { [[ ${1:-} =~ $RE_LOAD ]]; }
is_file_state() { [[ ${1:-} =~ $RE_FILE_STATE ]]; }
is_unit() {
    local n=${1:-}
    [ -n "$n" ] || return 1
    [ "${#n}" -le "$MAX_UNIT_LEN" ] || return 1
    case $n in .*) return 1 ;; esac
    [[ $n =~ $RE_UNIT ]]
}

unit_type() {
    local n=$1
    echo "${n##*.}"
}

unit_type_may_alias() {
    local t=$1
    case $t in
        service|socket|target|device|timer|path) return 0 ;;
        *) return 1 ;;
    esac
}

have() { command -v "$1" >/dev/null 2>&1; }

# run <tool> args... -> stdout, rc in $?; 127 never escapes (treated as absence by callers).
run() { "$@" 2>/dev/null; }

reading_searchpath() {
    local scope=${1:-system} out rc line n=0 first='' etc_idx=0 usr_idx=0 ord=0
    case $scope in
        system|user) ;;
        *) block SEARCHPATH bad-path; return ;;
    esac

    if [ -n "${TSUKUROI_UNIT_DIRS:-}" ]; then
        local dirs=() d
        IFS=':' read -r -a dirs <<<"${TSUKUROI_UNIT_DIRS}"
        for d in "${dirs[@]}"; do
            [ -n "$d" ] || continue
            is_path "$d" || { block SEARCHPATH bad-path; return; }
            n=$((n + 1))
            [ "$n" -eq 1 ] && first=$d
            case $d in
                /etc/*|*/etc/*) [ "$etc_idx" -eq 0 ] && etc_idx=$n ;;
                /usr/*|*/usr/*) [ "$usr_idx" -eq 0 ] && usr_idx=$n ;;
            esac
        done
        [ "$n" -ge 1 ] || { block SEARCHPATH unparsable; return; }
        if [ "$etc_idx" -gt 0 ] && [ "$usr_idx" -gt 0 ] && [ "$etc_idx" -lt "$usr_idx" ]; then
            ord=1
        fi
        printf 'SEARCHPATH scope=%s dirs=%s first=%s etc_before_usr=%s\n' "$scope" "$n" "$first" "$ord"
        return
    fi

    have systemd-analyze || { block SEARCHPATH tool-absent; return; }
    if [ "$scope" = "user" ]; then
        out=$(run systemd-analyze --user unit-paths); rc=$?
    else
        out=$(run systemd-analyze unit-paths); rc=$?
    fi
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
    printf 'SEARCHPATH scope=%s dirs=%s first=%s etc_before_usr=%s\n' "$scope" "$n" "$first" "$ord"
}

reading_masked() {
    local count=0 targets=0 out rc line u st rest tgt fp
    if [ -n "${TSUKUROI_UNIT_DIRS:-}" ]; then
        local dirs=() d f bn
        IFS=':' read -r -a dirs <<<"${TSUKUROI_UNIT_DIRS}"
        for d in "${dirs[@]}"; do
            is_path "$d" || { block MASKED bad-path; return; }
            [ -d "$d" ] || continue
            local entries=() f
            shopt -s dotglob
            for f in "$d"/*; do entries+=("$f"); done
            shopt -u dotglob
            for f in "${entries[@]}"; do
                [ -e "$f" ] || [ -L "$f" ] || continue
                [ -d "$f" ] && [ ! -L "$f" ] && continue
                bn=${f##*/}
                is_unit "$bn" || { block MASKED bad-unit-name; return; }
                if [ -L "$f" ]; then
                    tgt=$(readlink "$f") || continue
                    if [ "$tgt" = "/dev/null" ]; then
                        count=$((count + 1))
                        targets=$((targets + 1))
                    fi
                elif [ -f "$f" ]; then
                    # 0-byte file also counts as masked (null_or_empty in load-fragment.c)
                    if [ ! -s "$f" ]; then
                        count=$((count + 1))
                    fi
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
        [ "$st" = "masked" ] || { block MASKED unparsable; return; }
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
            if [ "$rc" -eq 0 ] && [ "$rt" = "/dev/null" ]; then
                targets=$((targets + 1))
            fi
        fi
    done <<<"$out"
    is_n "$count" || { block MASKED unparsable; return; }
    printf 'MASKED count=%s targets=/dev/null:%s\n' "$count" "$targets"
}

reading_cat() {
    local unit=$1 out rc line frag='' masked=0 dropins=0
    is_unit "$unit" || { block CAT bad-unit-name; return; }

    if [ -n "${TSUKUROI_UNIT_DIRS:-}" ]; then
        local dirs=() d target_path=''
        IFS=':' read -r -a dirs <<<"${TSUKUROI_UNIT_DIRS}"
        # Priority order: search paths top-to-bottom
        for d in "${dirs[@]}"; do
            [ -d "$d" ] || continue
            if [ -L "$d/$unit" ] || [ -f "$d/$unit" ]; then
                target_path="$d/$unit"
                break
            fi
        done
        if [ -z "$target_path" ]; then
            block CAT unknown-unit; return
        fi
        frag=$target_path
        if [ -L "$target_path" ]; then
            local tgt
            tgt=$(readlink "$target_path")
            if [ "$tgt" = "/dev/null" ]; then
                masked=1
            fi
        elif [ -f "$target_path" ] && [ ! -s "$target_path" ]; then
            masked=1
        fi
        # Check drop-ins across search path
        for d in "${dirs[@]}"; do
            local dropdir="$d/$unit.d"
            if [ -d "$dropdir" ]; then
                local conf
                for conf in "$dropdir"/*.conf; do
                    [ -f "$conf" ] || continue
                    dropins=$((dropins + 1))
                done
            fi
        done
        printf 'CAT unit=%s fragment=%s masked=%s dropins=%s\n' "$unit" "$frag" "$masked" "$dropins"
        return
    fi

    have systemctl || { block CAT tool-absent; return; }
    out=$(run systemctl cat "$unit"); rc=$?
    [ "$rc" -eq 127 ] && { block CAT tool-absent; return; }
    if [ "$rc" -ne 0 ]; then
        block CAT unknown-unit; return
    fi

    while IFS= read -r line; do
        [ -n "$line" ] || continue
        if [[ $line =~ ^#\ Unit\ .*\ is\ masked\. ]]; then
            masked=1
            # For masked units, fragment path is in FragmentPath property
            local fp
            fp=$(run systemctl show -p FragmentPath "$unit")
            frag=${fp#FragmentPath=}
            break
        elif [[ $line =~ ^#\ (/.*) ]]; then
            local p="${BASH_REMATCH[1]}"
            is_path "$p" || { block CAT bad-path; return; }
            if [ -z "$frag" ]; then
                frag=$p
            else
                case $p in
                    *.conf) dropins=$((dropins + 1)) ;;
                esac
            fi
        fi
    done <<<"$out"

    [ -n "$frag" ] || {
        local fp
        fp=$(run systemctl show -p FragmentPath "$unit")
        frag=${fp#FragmentPath=}
    }
    is_path "$frag" || { block CAT bad-path; return; }
    printf 'CAT unit=%s fragment=%s masked=%s dropins=%s\n' "$unit" "$frag" "$masked" "$dropins"
}

reading_template() {
    local inst=$1 frag base t=0
    is_unit "$inst" || { block TEMPLATE bad-unit-name; return; }

    if [ -n "${TSUKUROI_UNIT_DIRS:-}" ]; then
        local dirs=() d target_path=''
        IFS=':' read -r -a dirs <<<"${TSUKUROI_UNIT_DIRS}"
        for d in "${dirs[@]}"; do
            [ -d "$d" ] || continue
            if [ -e "$d/$inst" ]; then
                target_path="$d/$inst"
                break
            fi
        done
        if [ -z "$target_path" ]; then
            # Check template fallback: if instance is foo@bar.service, check foo@.service
            if [[ $inst =~ ^([^@]+)@([^.]+)\.(.*)$ ]]; then
                local prefix="${BASH_REMATCH[1]}"
                local ext="${BASH_REMATCH[3]}"
                local tmpl="${prefix}@.${ext}"
                for d in "${dirs[@]}"; do
                    [ -d "$d" ] || continue
                    if [ -e "$d/$tmpl" ]; then
                        target_path="$d/$tmpl"
                        t=1
                        break
                    fi
                done
            fi
        fi
        if [ -z "$target_path" ]; then
            block TEMPLATE unknown-unit; return
        fi
        base=${target_path##*/}
        is_unit "$base" || { block TEMPLATE bad-unit-name; return; }
        printf 'TEMPLATE instance=%s fragment=%s template=%s\n' "$inst" "$base" "$t"
        return
    fi

    have systemctl || { block TEMPLATE tool-absent; return; }
    local out rc line fp='' ls=''
    out=$(run systemctl show -p LoadState -p FragmentPath "$inst"); rc=$?
    [ "$rc" -eq 127 ] && { block TEMPLATE tool-absent; return; }
    [ "$rc" -eq 0 ] || { block TEMPLATE unparsable; return; }
    while IFS= read -r line; do
        [ -n "$line" ] || continue
        case $line in
            LoadState=*) ls=${line#LoadState=} ;;
            FragmentPath=*) fp=${line#FragmentPath=} ;;
        esac
    done <<<"$out"
    [ -n "$ls" ] || { block TEMPLATE unparsable; return; }
    [ "$ls" = "not-found" ] && { block TEMPLATE unknown-unit; return; }
    [ -n "$fp" ] || { block TEMPLATE unknown-unit; return; }
    is_path "$fp" || { block TEMPLATE bad-path; return; }
    base=${fp##*/}
    is_unit "$base" || { block TEMPLATE bad-unit-name; return; }
    case $base in *@.*) t=1 ;; esac
    printf 'TEMPLATE instance=%s fragment=%s template=%s\n' "$inst" "$base" "$t"
}

reading_alias() {
    local alias_unit=$1 target='' may_alias=0
    is_unit "$alias_unit" || { block ALIAS bad-unit-name; return; }
    local src_type
    src_type=$(unit_type "$alias_unit")
    if ! unit_type_may_alias "$src_type"; then
        block ALIAS incompatible-type; return
    fi

    if [ -n "${TSUKUROI_UNIT_DIRS:-}" ]; then
        local dirs=() d symlink_path=''
        IFS=':' read -r -a dirs <<<"${TSUKUROI_UNIT_DIRS}"
        for d in "${dirs[@]}"; do
            [ -d "$d" ] || continue
            if [ -L "$d/$alias_unit" ]; then
                symlink_path="$d/$alias_unit"
                break
            fi
        done
        if [ -z "$symlink_path" ]; then
            block ALIAS unknown-unit; return
        fi
        local tgt
        tgt=$(readlink "$symlink_path")
        local tgt_base=${tgt##*/}
        is_unit "$tgt_base" || { block ALIAS bad-unit-name; return; }
        # Self-alias check: src == dst (ELOOP)
        if [ "$alias_unit" = "$tgt_base" ]; then
            block ALIAS self-alias; return
        fi
        # Target unit type match check (EXDEV)
        local dst_type
        dst_type=$(unit_type "$tgt_base")
        if [ "$src_type" != "$dst_type" ]; then
            block ALIAS incompatible-type; return
        fi
        target=$tgt_base
        may_alias=1
        printf 'ALIAS alias=%s target=%s may_alias=%s\n' "$alias_unit" "$target" "$may_alias"
        return
    fi

    have systemctl || { block ALIAS tool-absent; return; }
    local en_st
    en_st=$(run systemctl is-enabled "$alias_unit")
    local out rc line id='' names='' fp=''
    out=$(run systemctl show -p Id -p Names -p FragmentPath "$alias_unit"); rc=$?
    [ "$rc" -eq 127 ] && { block ALIAS tool-absent; return; }
    [ "$rc" -eq 0 ] || { block ALIAS unparsable; return; }
    while IFS= read -r line; do
        [ -n "$line" ] || continue
        case $line in
            Id=*) id=${line#Id=} ;;
            Names=*) names=${line#Names=} ;;
            FragmentPath=*) fp=${line#FragmentPath=} ;;
        esac
    done <<<"$out"
    [ -n "$id" ] || { block ALIAS unparsable; return; }
    is_unit "$id" || { block ALIAS bad-unit-name; return; }

    if [ "$en_st" != "alias" ] && [ ! -L "$fp" ]; then
        block ALIAS unknown-unit; return
    fi
    # If id is identical to alias_unit, check if it's really an alias or not
    if [ "$id" = "$alias_unit" ]; then
        # Check if FragmentPath points to a symlink or another file
        if [ -L "$fp" ]; then
            local symtgt
            symtgt=$(readlink "$fp")
            local symbase=${symtgt##*/}
            if [ "$symbase" = "$alias_unit" ]; then
                block ALIAS self-alias; return
            fi
            target=$symbase
        else
            # Try to find target from names
            target=$id
        fi
    else
        target=$id
    fi
    local dst_type
    dst_type=$(unit_type "$target")
    if [ "$src_type" != "$dst_type" ]; then
        block ALIAS incompatible-type; return
    fi
    may_alias=1
    printf 'ALIAS alias=%s target=%s may_alias=%s\n' "$alias_unit" "$target" "$may_alias"
}

reading_unitstate() {
    local unit=$1 file_state='' load_state=''
    is_unit "$unit" || { block UNITSTATE bad-unit-name; return; }

    if [ -n "${TSUKUROI_UNIT_DIRS:-}" ]; then
        local dirs=() d target_path=''
        IFS=':' read -r -a dirs <<<"${TSUKUROI_UNIT_DIRS}"
        for d in "${dirs[@]}"; do
            [ -d "$d" ] || continue
            if [ -e "$d/$unit" ] || [ -L "$d/$unit" ]; then
                target_path="$d/$unit"
                break
            fi
        done
        if [ -z "$target_path" ]; then
            file_state="not-found"
            load_state="not-found"
        else
            if [ -L "$target_path" ]; then
                local tgt
                tgt=$(readlink "$target_path")
                if [ "$tgt" = "/dev/null" ]; then
                    file_state="masked"
                    load_state="masked"
                elif [[ $target_path =~ ^/run/ ]]; then
                    file_state="enabled-runtime"
                    load_state="loaded"
                else
                    file_state="enabled"
                    load_state="loaded"
                fi
            elif [ -f "$target_path" ]; then
                if [ ! -s "$target_path" ]; then
                    file_state="masked"
                    load_state="masked"
                else
                    file_state="static"
                    load_state="loaded"
                fi
            fi
        fi
        printf 'UNITSTATE unit=%s file_state=%s load_state=%s\n' "$unit" "$file_state" "$load_state"
        return
    fi

    have systemctl || { block UNITSTATE tool-absent; return; }
    local out rc
    # Query is-enabled for UnitFileState
    out=$(run systemctl is-enabled "$unit"); rc=$?
    if [ "$rc" -eq 127 ]; then
        block UNITSTATE tool-absent; return
    fi
    file_state=$(echo "$out" | head -n 1)
    [ -n "$file_state" ] || file_state="unknown"
    is_file_state "$file_state" || file_state="disabled"

    # Query LoadState
    out=$(run systemctl show -p LoadState "$unit"); rc=$?
    [ "$rc" -eq 127 ] && { block UNITSTATE tool-absent; return; }
    [ "$rc" -eq 0 ] || { block UNITSTATE unparsable; return; }
    load_state=${out#LoadState=}
    is_load "$load_state" || { block UNITSTATE unparsable; return; }

    printf 'UNITSTATE unit=%s file_state=%s load_state=%s\n' "$unit" "$file_state" "$load_state"
}

# ---------------------------------------------------------------- selftest
st_run() {
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
    [ "${#lines[@]}" -eq 1 ] || { printf 'FAIL %s lines=%s got=%s\n' "$label" "${#lines[@]}" "$out"; return 1; }
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
        /tmp|/tmp/*|/var/tmp|/var/tmp/*)
            echo "SELFTEST: FAIL (SELFTEST-TMPDIR) TMPDIR must not be in /tmp" >&2
            return 4
            ;;
    esac

    local td
    td=$(mktemp -d "$tmp/st-unit-fragment-probe.XXXXXX") || return 4
    trap 'rm -rf "${td:-}"' EXIT

    mkdir -p "$td/bin" "$td/etc/systemd/system" "$td/usr/lib/systemd/system" "$td/run/systemd/system"
    local bin="$td/bin"
    local etc="$td/etc/systemd/system"
    local usr="$td/usr/lib/systemd/system"
    local run="$td/run/systemd/system"
    local udirs="$etc:$run:$usr"

    # Fixture: stub failing tools for tool-absent tests
    cat >"$bin/systemctl" <<'EOF'
#!/bin/sh
exit 127
EOF
    chmod +x "$bin/systemctl"
    cat >"$bin/systemd-analyze" <<'EOF'
#!/bin/sh
exit 127
EOF
    chmod +x "$bin/systemd-analyze"

    # Fixture 1: masked units (/dev/null symlink and 0-byte file)
    ln -s /dev/null "$etc/masked-null.service"
    touch "$etc/masked-empty.service"

    # Fixture 2: normal service in usr, with drop-in in etc
    cat >"$usr/worker.service" <<'EOF'
[Unit]
Description=Test Worker
[Service]
ExecStart=/bin/true
EOF
    mkdir -p "$etc/worker.service.d"
    cat >"$etc/worker.service.d/override.conf" <<'EOF'
[Service]
TimeoutStopSec=10s
EOF

    # Fixture 3: template and instance
    cat >"$usr/container@.service" <<'EOF'
[Unit]
Description=Test Container %i
[Service]
ExecStart=/bin/true %i
EOF

    # Fixture 4: aliases (valid, self-alias, incompatible type, unit type may not alias)
    ln -s worker.service "$usr/worker-alias.service"
    ln -s bad-self.service "$etc/bad-self.service"
    ln -s worker.service "$etc/bad-type.socket"
    ln -s other.slice "$etc/bad-mount.slice"

    # Fixture 5: searchpath precedence (first-seen name registration)
    cat >"$etc/shadow.service" <<'EOF'
[Unit]
Description=Higher Priority Shadow
EOF
    cat >"$usr/shadow.service" <<'EOF'
[Unit]
Description=Lower Priority Shadow
EOF

    local fails=0
    # Case 1: searchpath normal (dirs=3, first=etc, etc_before_usr=1)
    st_run "T01-searchpath-hermetic" '^SEARCHPATH scope=system dirs=3 first=.+/etc/systemd/system etc_before_usr=1$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading searchpath || fails=$((fails + 1))

    # Case 2: searchpath tool absent
    st_run "T02-searchpath-tool-absent" '^BLOCKED reading=SEARCHPATH reason=tool-absent$' \
        "PATH=$bin:/usr/bin" -- --reading searchpath || fails=$((fails + 1))

    # Case 3: masked units counted (count=2 targets=/dev/null:1)
    st_run "T03-masked-hermetic" '^MASKED count=2 targets=/dev/null:1$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading masked || fails=$((fails + 1))

    # Case 4: masked tool absent
    st_run "T04-masked-tool-absent" '^BLOCKED reading=MASKED reason=tool-absent$' \
        "PATH=$bin:/usr/bin" -- --reading masked || fails=$((fails + 1))

    # Case 5: cat normal with drop-ins (fragment in usr, dropins=1, masked=0)
    st_run "T05-cat-hermetic-worker" '^CAT unit=worker\.service fragment=.+/usr/lib/systemd/system/worker\.service masked=0 dropins=1$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading cat:worker.service || fails=$((fails + 1))

    # Case 6: cat masked service (/dev/null symlink)
    st_run "T06-cat-hermetic-masked" '^CAT unit=masked-null\.service fragment=.+/etc/systemd/system/masked-null\.service masked=1 dropins=0$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading cat:masked-null.service || fails=$((fails + 1))

    # Case 7: cat tool absent
    st_run "T07-cat-tool-absent" '^BLOCKED reading=CAT reason=tool-absent$' \
        "PATH=$bin:/usr/bin" -- --reading cat:worker.service || fails=$((fails + 1))

    # Case 8: cat unknown unit
    st_run "T08-cat-unknown" '^BLOCKED reading=CAT reason=unknown-unit$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading cat:nosuch-unit.service || fails=$((fails + 1))

    # Case 9: cat bad unit name (injection attempt with pipe)
    st_run "T09-cat-bad-unit-pipe" '^BLOCKED reading=CAT reason=bad-unit-name$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading 'cat:worker.service|forged' || fails=$((fails + 1))

    # Case 10: template resolution on instance
    st_run "T10-template-instance" '^TEMPLATE instance=container@app1\.service fragment=container@\.service template=1$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading template:container@app1.service || fails=$((fails + 1))

    # Case 11: template resolution on non-instance
    st_run "T11-template-plain" '^TEMPLATE instance=worker\.service fragment=worker\.service template=0$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading template:worker.service || fails=$((fails + 1))

    # Case 12: template bad unit name
    st_run "T12-template-bad-name" '^BLOCKED reading=TEMPLATE reason=bad-unit-name$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading 'template:bad name.service' || fails=$((fails + 1))

    # Case 13: alias valid (worker-alias.service -> worker.service)
    st_run "T13-alias-valid" '^ALIAS alias=worker-alias\.service target=worker\.service may_alias=1$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading alias:worker-alias.service || fails=$((fails + 1))

    # Case 14: alias self-alias rejection (UF2 ELOOP)
    st_run "T14-alias-self" '^BLOCKED reading=ALIAS reason=self-alias$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading alias:bad-self.service || fails=$((fails + 1))

    # Case 15: alias incompatible target type (UF2 EXDEV)
    st_run "T15-alias-incompatible-type" '^BLOCKED reading=ALIAS reason=incompatible-type$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading alias:bad-type.socket || fails=$((fails + 1))

    # Case 16: alias disallowed unit type (UF3 unit_type_may_alias rejects slice)
    st_run "T16-alias-disallowed-type" '^BLOCKED reading=ALIAS reason=incompatible-type$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading alias:bad-mount.slice || fails=$((fails + 1))

    # Case 17: unitstate static normal
    st_run "T17-unitstate-static" '^UNITSTATE unit=worker\.service file_state=static load_state=loaded$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading unitstate:worker.service || fails=$((fails + 1))

    # Case 18: unitstate masked normal
    st_run "T18-unitstate-masked" '^UNITSTATE unit=masked-null\.service file_state=masked load_state=masked$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading unitstate:masked-null.service || fails=$((fails + 1))

    # Case 19: unitstate non-existent unit
    st_run "T19-unitstate-not-found" '^UNITSTATE unit=nosuch\.service file_state=not-found load_state=not-found$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading unitstate:nosuch.service || fails=$((fails + 1))

    # Case 20: unitstate bad unit name
    st_run "T20-unitstate-bad-name" '^BLOCKED reading=UNITSTATE reason=bad-unit-name$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading 'unitstate:bad;inject.service' || fails=$((fails + 1))

    # Case 21: first-seen precedence (UF1: /etc/shadow.service shadows /usr/shadow.service)
    st_run "T21-first-seen-precedence" '^CAT unit=shadow\.service fragment=.+/etc/systemd/system/shadow\.service masked=0 dropins=0$' \
        "TSUKUROI_UNIT_DIRS=$udirs" -- --reading cat:shadow.service || fails=$((fails + 1))

    if [ "$fails" -eq 0 ]; then
        echo "SELFTEST: PASS (21 cases, 21 passed, 0 failed)"
        return 0
    else
        echo "SELFTEST: FAIL ($fails cases failed out of 21)" >&2
        return 3
    fi
}

# ---------------------------------------------------------------- main entry
BASH=${BASH:-/usr/bin/bash}
SELF=${BASH_SOURCE[0]}

READINGS=()
ARG_CAT="user@1000.service"
ARG_TEMPLATE="getty@tty1.service"
ARG_ALIAS="dbus.service"
ARG_STATE="systemd-remount-fs.service"
SCOPE="system"

while [ $# -gt 0 ]; do
    case $1 in
        --selftest)
            selftest
            exit $?
            ;;
        --reading)
            [ $# -ge 2 ] || { echo "Missing argument to --reading" >&2; exit 2; }
            READINGS+=("$2")
            shift 2
            ;;
        --cat)
            [ $# -ge 2 ] || { echo "Missing argument to --cat" >&2; exit 2; }
            ARG_CAT=$2
            shift 2
            ;;
        --template)
            [ $# -ge 2 ] || { echo "Missing argument to --template" >&2; exit 2; }
            ARG_TEMPLATE=$2
            shift 2
            ;;
        --alias)
            [ $# -ge 2 ] || { echo "Missing argument to --alias" >&2; exit 2; }
            ARG_ALIAS=$2
            shift 2
            ;;
        --state)
            [ $# -ge 2 ] || { echo "Missing argument to --state" >&2; exit 2; }
            ARG_STATE=$2
            shift 2
            ;;
        --scope)
            [ $# -ge 2 ] || { echo "Missing argument to --scope" >&2; exit 2; }
            SCOPE=$2
            shift 2
            ;;
        --unit-dirs)
            [ $# -ge 2 ] || { echo "Missing argument to --unit-dirs" >&2; exit 2; }
            TSUKUROI_UNIT_DIRS=$2
            shift 2
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 2
            ;;
    esac
done

if [ "${#READINGS[@]}" -eq 0 ]; then
    READINGS=(
        "searchpath"
        "masked"
        "cat:passim.service"
        "cat:user@1000.service"
        "template:getty@tty1.service"
        "alias:dbus.service"
        "unitstate:systemd-remount-fs.service"
        "unitstate:passim.service"
        "unitstate:getty@tty1.service"
    )
fi

for r in "${READINGS[@]}"; do
    case $r in
        searchpath)
            reading_searchpath "$SCOPE"
            ;;
        searchpath:*)
            reading_searchpath "${r#searchpath:}"
            ;;
        masked)
            reading_masked
            ;;
        cat)
            reading_cat "$ARG_CAT"
            ;;
        cat:*)
            reading_cat "${r#cat:}"
            ;;
        template)
            reading_template "$ARG_TEMPLATE"
            ;;
        template:*)
            reading_template "${r#template:}"
            ;;
        alias)
            reading_alias "$ARG_ALIAS"
            ;;
        alias:*)
            reading_alias "${r#alias:}"
            ;;
        unitstate)
            reading_unitstate "$ARG_STATE"
            ;;
        unitstate:*)
            reading_unitstate "${r#unitstate:}"
            ;;
        *)
            block "$r" bad-unit-name
            ;;
    esac
done

if [ "$blocked" -gt 0 ]; then
    exit 1
fi
exit 0
