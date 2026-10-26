#!/usr/bin/env bash
# C1RevFix harness v2: compare base decision logic (6951ead) vs fix logic (717b716)
# verbatim under the script's own shell options (set -uo pipefail, fix.sh:139).
# v1 bug fixed: epoch is shifted out of "$@" before find; newline fixtures use $'\n'.
set -uo pipefail

FX=$1
mkdir -p -- "$FX"
cd "$FX" || exit 9

# ---- base decision shape (base.sh :480-488: paths, then -newermt "@$btime") --
old_decide() {
    local btime=$1
    shift
    if find "$@" -newermt "@$btime" -print -quit 2>/dev/null | grep -q .; then
        printf '1\n'
    else
        printf '0\n'
    fi
}
# ---- verbatim fix logic (fix.sh :463-475) ---------------------------------
new_decide() {
    local epoch=$1 hit
    shift
    hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)
    if [ -n "$hit" ]; then
        printf '1\n'
    else
        printf '0\n'
    fi
}
find_rc() { # <epoch> <paths...> -> find's own exit status for the same invocation
    local epoch=$1
    shift
    find "$@" -newermt "@$epoch" -print -quit 2>/dev/null
    local rc=$?
    printf 'find_rc=%s' "$rc"
}

nl=$'\n'
# fixtures: everything stamped @1000 unless noted
: >n1;                                    touch -d @1000 -- n1
mkdir -p dir1;  : >dir1/f;                touch -d @1000 -- dir1/f dir1
mkdir -p dir2;  : >dir2/g;                touch -d @3000 -- dir2/g; touch -d @1000 -- dir2
mkdir -p locked; : >locked/h;             touch -d @3000 -- locked/h; touch -d @1000 -- locked; chmod 000 locked
mkdir -p dir3;  : >"dir3/$nl";            touch -d @3000 -- "dir3/$nl"; touch -d @1000 -- dir3
mkdir -p dir4;  : >"dir4/ ";              touch -d @3000 -- "dir4/ "; touch -d @1000 -- dir4
: >"$nl";                                 touch -d @3000 -- "$nl"

case_run() { # <name> <epoch> <paths...>
    local name=$1 epoch=$2; shift 2
    local o n eq
    o=$(old_decide "$epoch" "$@")
    n=$(new_decide "$epoch" "$@")
    if [ "$o" = "$n" ]; then eq=EQUAL; else eq=DIVERGE; fi
    printf '%-30s old=%s new=%s %s [%s]\n' "$name" "$o" "$n" "$eq" "$(find_rc "$epoch" "$@")"
}

case_run 'c1 all-present-none-newer'    2000 n1 dir1
case_run 'c2 all-present-deep-newer'    2000 n1 dir2
case_run 'c3 missing-first-none-newer'  2000 missing n1 dir1
case_run 'c4 missing-first-deep-newer'  2000 missing dir2
case_run 'c5 missing-last-deep-newer'   2000 dir2 missing
case_run 'c6 unreadable-first-newer'    2000 locked dir2
case_run 'c7 empty-epoch'               ''   dir2
case_run 'c8 dash-epoch'                '-'  dir2
case_run 'c9 newline-file-in-dir'       2000 dir3
case_run 'c10 newline-file-as-start'    2000 "dir3/$nl"
case_run 'c13 space-filename'           2000 dir4
case_run 'c14 zero-paths'               2000

# c11: start point whose printed path is newline-only (relative, cwd=$FX)
o=$(old_decide 2000 "$nl"); n=$(new_decide 2000 "$nl")
[ "$o" = "$n" ] && eq=EQUAL || eq=DIVERGE
printf '%-30s old=%s new=%s %s\n' 'c11 bare-newline-start-point' "$o" "$n" "$eq"

# c12: same match reached via ./dir3
o=$(old_decide 2000 ./dir3); n=$(new_decide 2000 ./dir3)
[ "$o" = "$n" ] && eq=EQUAL || eq=DIVERGE
printf '%-30s old=%s new=%s %s\n' 'c12 relative-dir-newline-file' "$o" "$n" "$eq"

chmod -R u+rwx -- locked 2>/dev/null || true
