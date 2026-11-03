#!/usr/bin/env bash
# c2-mutant-battery.sh — hermetic mutant battery for tools/check-adjacency-anchors.py.
#
# Usage: c2-mutant-battery.sh TOOL [SIBLINGS_ROOT]
#   TOOL           path to check-adjacency-anchors.py (BASE or patched). It is copied into
#                  each sandbox clone, so the tool's ROOT is the clone, never the lane.
#   SIBLINGS_ROOT  root holding read-only <name>-shokunin sibling repos
#                  (default: /home/vgpnk/Projects/shokunin)
#
# Rows (one per mutant), printed as TSV: mutant<TAB>status<TAB>findings<TAB>live_checked<TAB>rc
#   H0  honest base revision, no mutant, real siblings root      (control: PASS, live 10)
#   M1  OUT-010 sibling_commit replaced by a fabricated full 40-hex id that resolves nowhere
#   M2  OUT-010 sibling_commit replaced by a 7-hex abbreviation of the real commit
#   M3  OUT-010 sibling_commit replaced by the UPPERCASE form of the real commit
#   M4  honest base revision, siblings root with tameshi-shokunin absent (rest symlinked)
# In every mutant the published PROVINCE.md portable-digest line carries the same mutated
# commit token and the original sha256, so ANCHOR-UNPUBLISHED never masks the live-object check.
#
# Every clone lives under this script's own mktemp -d inside the scratch dir and is deleted
# on exit (trap). No /tmp, no writes outside the scratch dir. Each case clones fresh and the
# previous clone is removed first, so at most one live clone exists.
#
# Env overrides (defaults are the round-67 lane): LANE, BASE_REV, C2_SCRATCH.
set -u

TOOL=${1:-}
SIBLINGS_ROOT=${2:-/home/vgpnk/Projects/shokunin}
LANE=${LANE:-/home/vgpnk/Projects/shokunin/tsukuroi-shokunin}
BASE_REV=${BASE_REV:-5abc31d995f53d8bd7283fab78fa6d4a51e97ea6}
SCRATCH=${C2_SCRATCH:-/fast/scratch/hyaku/tsukuroi-r67/E3Fixture}

# OUT-010 (tameshi) is the mutated record: its sibling dir exists and its commit is real.
MUT_OLD=01d586ddbc5fcd78659557c4e93a6ee8517b87d1
MUT_ABSENT_SIBLING=tameshi-shokunin
M1_NEW=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
M2_NEW=${MUT_OLD:0:7}
M3_NEW=01D586DDBC5FCD78659557C4E93A6EE8517B87D1

die() { printf '# ERROR %s\n' "$*" >&2; exit 2; }

[ -n "$TOOL" ] || die "usage: c2-mutant-battery.sh TOOL [SIBLINGS_ROOT]"
[ -f "$TOOL" ] || die "TOOL is not a file: $TOOL"
[ -d "$SIBLINGS_ROOT" ] || die "SIBLINGS_ROOT is not a directory: $SIBLINGS_ROOT"
[ -d "$LANE/.git" ] || die "LANE is not a git repository: $LANE"

mkdir -p "$SCRATCH" || die "cannot create scratch: $SCRATCH"
W=$(mktemp -d "$SCRATCH/c2bat.XXXXXX") || die "mktemp failed under $SCRATCH"
trap 'rm -rf -- "$W"' EXIT

printf '# c2-mutant-battery %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf '# tool=%s\n' "$TOOL"
printf '# lane=%s base_rev=%s siblings_root=%s\n' "$LANE" "$BASE_REV" "$SIBLINGS_ROOT"
printf '# columns: mutant status findings live_checked rc (findings "-" = none; "# live_match" carries live_object_match)\n'

# fresh sandbox clone at BASE_REV with the tool under test installed and origin/master removed
# (so a mutant commit on master binds: _revision only checks origin when the ref exists).
clone_fresh() { # name -> prints clone path
    local name=$1 c top
    c="$W/$name/lane"
    mkdir -p "$W/$name" || return 1
    git clone -q --shared "$LANE" "$c" || { printf '# ERROR clone failed %s\n' "$name" >&2; return 1; }
    top=$(git -C "$c" rev-parse --show-toplevel 2>/dev/null)
    [ "$top" = "$(cd "$c" && pwd -P)" ] || { printf '# ERROR toplevel mismatch %s: %s\n' "$name" "$top" >&2; return 1; }
    git -C "$c" update-ref -d refs/remotes/origin/master >/dev/null 2>&1
    git -C "$c" checkout -q -B master "$BASE_REV" || { printf '# ERROR checkout failed %s\n' "$name" >&2; return 1; }
    cp "$TOOL" "$c/tools/check-adjacency-anchors.py" || { printf '# ERROR tool copy failed %s\n' "$name" >&2; return 1; }
    # the tool's only local import: keep it at the version the tool under test expects
    if [ -f "$(dirname "$TOOL")/_revision.py" ]; then
        cp "$(dirname "$TOOL")/_revision.py" "$c/tools/_revision.py" \
            || { printf '# ERROR _revision copy failed %s\n' "$name" >&2; return 1; }
    fi
    printf '%s' "$c"
}

# replace exactly one occurrence of the real commit token in a file
replace_once() { # file old new label
    python3 - "$1" "$2" "$3" "$4" <<'PY'
import pathlib, sys
path, old, new, label = sys.argv[1:5]
p = pathlib.Path(path)
text = p.read_text(encoding="utf-8")
count = text.count(old)
if count != 1:
    sys.exit(f"{label}: expected 1 occurrence of {old}, found {count}")
p.write_text(text.replace(old, new), encoding="utf-8")
PY
}

mutate_commit() { # clone new
    local c=$1 new=$2
    replace_once "$c/corpus/knowledge/adjacency-anchors-r19.json" "$MUT_OLD" "$new" registry || return 1
    replace_once "$c/PROVINCE.md" "$MUT_OLD" "$new" province || return 1
    git -C "$c" add -A >/dev/null 2>&1 || return 1
    GIT_AUTHOR_DATE=2026-01-01T00:00:00Z GIT_COMMITTER_DATE=2026-01-01T00:00:00Z \
    git -C "$c" -c user.name=c2-battery -c user.email=c2-battery@example.invalid \
        commit -q -m "c2-battery mutant" >/dev/null 2>&1 || return 1
}

run_row() { # name clone rev siblings_root
    local name=$1 c=$2 rev=$3 sib=$4 out rc parsed status findings checked match
    out=$(cd "$c" && python3 "$c/tools/check-adjacency-anchors.py" \
              --revision "$rev" --siblings-root "$sib" 2>"$W/$name.stderr")
    rc=$?
    parsed=$(printf '%s' "$out" | python3 -c '
import json, sys
raw = sys.stdin.read()
try:
    d = json.loads(raw)
except Exception:
    print("NOJSON\tparse-error\t-1\t-1")
    raise SystemExit(0)
ids = sorted({str(f.get("id")) for f in (d.get("findings") or [])})
c = d.get("counts") or {}
print("%s\t%s\t%s\t%s" % (d.get("status", "NOJSON"), ",".join(ids) if ids else "-",
                          c.get("live_object_checked", "-"), c.get("live_object_match", "-")))
')
    IFS=$'\t' read -r status findings checked match <<<"$parsed"
    printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$status" "$findings" "$checked" "$rc"
    printf '# live_match\t%s\t%s\n' "$name" "$match"
    printf '# rev\t%s\t%s\n' "$name" "$rev"
    if [ -s "$W/$name.stderr" ]; then
        awk 'NR<=3 {printf "# stderr %s: %s\n", name, $0}' name="$name" "$W/$name.stderr"
    fi
}

# scratch siblings root for M4: every sibling symlinked except the mutated record's sibling
mkdir -p "$W/m4-siblings" || die "cannot create M4 siblings root"
for p in "$SIBLINGS_ROOT"/*-shokunin; do
    [ -d "$p" ] || continue
    b=$(basename "$p")
    [ "$b" = "$MUT_ABSENT_SIBLING" ] && continue
    ln -s "$p" "$W/m4-siblings/$b" || die "cannot symlink $p"
done
[ ! -e "$W/m4-siblings/$MUT_ABSENT_SIBLING" ] || die "M4 siblings root still contains $MUT_ABSENT_SIBLING"

for name in H0 M1 M2 M3 M4; do
    rm -rf -- "$W/last" 2>/dev/null
    c=$(clone_fresh "$name") || { printf '%s\tCLONE-FAIL\t-\t-\t2\n' "$name"; continue; }
    case $name in
        H0) rev=$BASE_REV ;;
        M1) mutate_commit "$c" "$M1_NEW" || { printf '%s\tMUTATE-FAIL\t-\t-\t2\n' "$name"; rm -rf -- "$W/$name"; continue; }
            rev=$(git -C "$c" rev-parse HEAD) ;;
        M2) mutate_commit "$c" "$M2_NEW" || { printf '%s\tMUTATE-FAIL\t-\t-\t2\n' "$name"; rm -rf -- "$W/$name"; continue; }
            rev=$(git -C "$c" rev-parse HEAD) ;;
        M3) mutate_commit "$c" "$M3_NEW" || { printf '%s\tMUTATE-FAIL\t-\t-\t2\n' "$name"; rm -rf -- "$W/$name"; continue; }
            rev=$(git -C "$c" rev-parse HEAD) ;;
        M4) rev=$BASE_REV ;;
    esac
    sib=$SIBLINGS_ROOT
    [ "$name" = M4 ] && sib="$W/m4-siblings"
    run_row "$name" "$c" "$rev" "$sib"
    rm -rf -- "$W/$name"
done
